import { ConnectionError, errorFor, SuperArtifactsError, TimeoutError } from './errors.js'

export const VERSION = '0.1.0'

const DEFAULT_BASE_URL = 'https://superartifacts.app'
const API_KEY_ENV = 'SUPERARTIFACTS_API_KEY'
/** Longer than any per-minute window. Past it the wait is an hour's, and the caller decides. */
const MAX_RETRY_AFTER_SECONDS = 60
const BACKOFF_BASE_MS = 500
const BACKOFF_MAX_MS = 8_000

export interface ClientOptions {
  /** Defaults to the SUPERARTIFACTS_API_KEY environment variable. */
  apiKey?: string
  baseUrl?: string
  /** Milliseconds per attempt. */
  timeout?: number
  maxRetries?: number
  fetch?: typeof globalThis.fetch
  /** The API refuses browsers, so this only helps behind your own proxy. */
  dangerouslyAllowBrowser?: boolean
}

export interface RequestOptions {
  /** Every POST gets a fresh one. `false` sends none, and a failed POST is then not retried. */
  idempotencyKey?: string | false
  timeout?: number
  signal?: AbortSignal
  headers?: Record<string, string>
}

/** One operation of the API, as the generated layer describes it. */
export interface Operation {
  method: string
  path: string
  /** The path names travel in the path and these in the query; the rest is the body. */
  query: readonly string[]
  /** A destructive DELETE repeats this path name as `?confirm=`. */
  confirm?: string
}

type Body<Op> = Op extends { requestBody?: { content: { 'application/json': infer B } } }
  ? B
  : object
type Path<Op> = Op extends { parameters: { path: infer P } } ? P : object
type Query<Op> = Op extends { parameters: { query?: infer Q } }
  ? [NonNullable<Q>] extends [never]
    ? object
    : NonNullable<Q>
  : object

/** Path, query and body fields of an operation, in one object. */
export type Params<Op> = Path<Op> & Query<Op> & Body<Op>
export type Result<Op> = Op extends {
  responses: { 200: { content: { 'application/json': infer R } } }
}
  ? R
  : unknown

const sleep = (ms: number, signal?: AbortSignal): Promise<void> =>
  new Promise((resolve, reject) => {
    const timer = setTimeout(resolve, ms)
    signal?.addEventListener(
      'abort',
      () => {
        clearTimeout(timer)
        reject(signal.reason)
      },
      { once: true },
    )
  })

const backoff = (attempt: number): number => {
  const ceiling = Math.min(BACKOFF_MAX_MS, BACKOFF_BASE_MS * 2 ** attempt)
  return ceiling / 2 + Math.random() * (ceiling / 2)
}

function isBrowser(): boolean {
  const scope = globalThis as { window?: unknown; document?: unknown }
  return scope.window !== undefined && scope.document !== undefined
}

export class Core {
  readonly #apiKey: string
  readonly #baseUrl: string
  readonly #timeout: number
  readonly #maxRetries: number
  readonly #fetch: typeof globalThis.fetch

  constructor(options: ClientOptions = {}) {
    if (isBrowser() && options.dangerouslyAllowBrowser !== true) {
      throw new Error(
        'The Super Artifacts API refuses requests from a browser, and a key on a page is a leaked key. Call it from your server. Behind your own proxy, pass dangerouslyAllowBrowser: true.',
      )
    }
    const apiKey = options.apiKey ?? globalThis.process?.env?.[API_KEY_ENV]
    if (!apiKey) {
      throw new Error(
        `No API key. Set ${API_KEY_ENV} or pass { apiKey }. Create one at https://superartifacts.app/settings/api-keys`,
      )
    }
    this.#apiKey = apiKey
    this.#baseUrl = (options.baseUrl ?? DEFAULT_BASE_URL).replace(/\/+$/, '')
    this.#timeout = options.timeout ?? 60_000
    this.#maxRetries = options.maxRetries ?? 2
    this.#fetch = options.fetch ?? globalThis.fetch
  }

  /** Call one operation with its fields in one object. The generated resources all land here. */
  call(
    operation: Operation,
    params: object = {},
    options: RequestOptions = {},
  ): Promise<Record<string, unknown>> {
    const { method } = operation
    const rest = new Map(Object.entries(params).filter(([, value]) => value !== undefined))
    const take = (name: string): unknown => {
      const value = rest.get(name)
      rest.delete(name)
      return value
    }

    const pathNames: string[] = []
    const path = operation.path.replace(/\{(\w+)\}/g, (_, name: string) => {
      const value = take(name)
      if (value === null || value === undefined || value === '') {
        throw new TypeError(`${method} ${operation.path} needs ${name}.`)
      }
      pathNames.push(name)
      return encodeURIComponent(String(value))
    })

    const url = new URL(`${this.#baseUrl}${path}`)
    for (const name of operation.query) {
      for (const value of [take(name)].flat()) {
        if (value !== undefined) url.searchParams.append(name, String(value))
      }
    }
    if (operation.confirm !== undefined) {
      take('confirm')
      url.searchParams.set('confirm', String(params[operation.confirm as keyof typeof params]))
    }

    // A field the spec does not name still goes out, so the API refuses it rather than this
    // client dropping it. A method without a body sends it as a query, for the same reason.
    const bodied = method !== 'GET' && method !== 'DELETE'
    if (!bodied) for (const [name, value] of rest) url.searchParams.append(name, String(value))
    const body = bodied && rest.size > 0 ? JSON.stringify(Object.fromEntries(rest)) : undefined

    const key =
      method === 'POST' ? (options.idempotencyKey ?? crypto.randomUUID()) : options.idempotencyKey
    const headers: Record<string, string> = {
      Authorization: `Bearer ${this.#apiKey}`,
      'Content-Type': 'application/json',
      ...(typeof key === 'string' ? { 'Idempotency-Key': key } : {}),
      ...options.headers,
    }
    // The API honours the key on POST only, so a key on a PATCH makes nothing safe to repeat.
    const repeatable = method === 'GET' || method === 'DELETE' || (method === 'POST' && !!key)
    return this.send(url, { method, headers, ...(body ? { body } : {}) }, repeatable, options)
  }

  /**
   * PUT staged bytes, one file at a time. The URL is the credential, so no key goes with
   * it, and it takes the same bytes twice, so it is always safe to repeat.
   */
  async putFiles(
    targets: readonly { url: string }[],
    files: readonly Blob[],
    options?: RequestOptions,
  ): Promise<void> {
    for (const [index, { url }] of targets.entries()) {
      await this.send(url, { method: 'PUT', body: files[index] ?? null }, true, options)
    }
  }

  /** One request with the retry rules. A 429 ran nothing, so it repeats whatever `repeatable` says. */
  protected async send(
    url: URL | string,
    init: RequestInit,
    repeatable: boolean,
    options: RequestOptions = {},
  ): Promise<Record<string, unknown>> {
    const headers = { 'User-Agent': `superartifacts-typescript/${VERSION}`, ...init.headers }
    for (let attempt = 0; ; attempt++) {
      const left = attempt < this.#maxRetries
      let failure: SuperArtifactsError
      let delay = backoff(attempt)
      let retry = left && repeatable
      try {
        const timeout = AbortSignal.timeout(options.timeout ?? this.#timeout)
        const signal = options.signal ? AbortSignal.any([timeout, options.signal]) : timeout
        const response = await this.#fetch(url, { ...init, headers, signal })
        const text = await response.text()
        if (response.ok) return parseAnswer(text, response.status)

        failure = errorFor(response.status, text, response.headers.get('retry-after'))
        const { status, retryAfter } = failure
        if (status === 429 || (retry && [502, 503, 504].includes(status))) {
          if (retryAfter !== undefined) delay = retryAfter * 1000
          retry = left && (retryAfter ?? 0) <= MAX_RETRY_AFTER_SECONDS
        } else {
          retry = false
        }
      } catch (cause) {
        if (options.signal?.aborted) throw options.signal.reason
        if (cause instanceof SuperArtifactsError) throw cause
        const timedOut = (cause as Error | undefined)?.name === 'TimeoutError'
        const message = timedOut
          ? 'The request timed out.'
          : `Could not reach the API: ${(cause as Error | undefined)?.message ?? 'unknown error'}`
        const ErrorClass = timedOut ? TimeoutError : ConnectionError
        const code = timedOut ? 'timeout' : 'connection_error'
        failure = new ErrorClass(0, code, message, undefined, {}, { cause })
      }
      if (!retry) throw failure
      await sleep(delay, options.signal)
    }
  }
}

function parseAnswer(text: string, status: number): Record<string, unknown> {
  if (text === '') return {}
  try {
    return JSON.parse(text) as Record<string, unknown>
  } catch (cause) {
    throw new SuperArtifactsError(
      status,
      'invalid_response',
      'The API answered with something that is not JSON.',
      undefined,
      {},
      { cause },
    )
  }
}
