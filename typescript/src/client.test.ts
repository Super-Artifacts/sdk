import { readFileSync } from 'node:fs'
import { afterEach, describe, expect, it, vi } from 'vitest'
import * as sdk from './index.js'
import { OPERATIONS, SuperArtifacts, VERSION } from './index.js'

const KEY = 'sa_test_key_never_printed'
const spec = JSON.parse(readFileSync(new URL('../../openapi.json', import.meta.url), 'utf8'))
const names: Record<string, { resource: string; method: string }> = JSON.parse(
  readFileSync(new URL('../../resources.json', import.meta.url), 'utf8'),
)

type Sent = { url: URL; method: string; headers: Headers; body: unknown }

function catchError(run: () => unknown): sdk.SuperArtifactsError {
  try {
    run()
  } catch (error) {
    return error as sdk.SuperArtifactsError
  }
  throw new Error('it did not throw')
}

/** A fetch that answers from a list and records what it was sent. The last answer repeats. */
function mock(...answers: (Response | Error)[]) {
  const sent: Sent[] = []
  const fetch = vi.fn(async (input: string | URL | Request, init: RequestInit = {}) => {
    sent.push({
      url: new URL(String(input)),
      method: init.method ?? 'GET',
      headers: new Headers(init.headers),
      body: typeof init.body === 'string' ? JSON.parse(init.body) : init.body,
    })
    const answer = answers[Math.min(sent.length - 1, answers.length - 1)]
    if (answer instanceof Error) throw answer
    return (answer as Response).clone()
  }) as unknown as typeof globalThis.fetch
  return { fetch, sent }
}

const ok = (body: unknown = {}) => Response.json(body)
const refused = (status: number, code: string, headers: Record<string, string> = {}) =>
  Response.json({ error: { code, message: `refused ${code}` } }, { status, headers })

const PAGE = { slug: 's', prompt: 'p', html: 'x' }

const client = (fetch: typeof globalThis.fetch, maxRetries = 2) =>
  new SuperArtifacts({ apiKey: KEY, fetch, maxRetries })

afterEach(() => {
  vi.useRealTimers()
  vi.unstubAllEnvs()
  vi.unstubAllGlobals()
})

type Schema = { type?: string; properties?: Record<string, Schema> }
type Parameter = { name: string; in: string; schema?: Schema }
type SpecOperation = {
  operationId: string
  parameters?: Parameter[]
  requestBody?: { content: { 'application/json': { schema: Schema } } }
}

describe('every operation in the spec', () => {
  const paths: Record<string, Record<string, SpecOperation>> = spec.paths
  const operations = Object.entries(paths).flatMap(([path, item]) =>
    Object.entries(item).map(([verb, op]) => ({ path, verb: verb.toUpperCase(), ...op })),
  )

  const sample = (schema: Schema | undefined, name: string) => {
    if (schema?.type === 'array') return [`${name}-1`, `${name}-2`]
    if (schema?.type === 'integer') return 7
    if (schema?.type === 'boolean') return true
    return `${name}-value`
  }

  it('covers all 48', () => {
    expect(operations).toHaveLength(Object.keys(OPERATIONS).length)
    expect(operations.length).toBeGreaterThanOrEqual(48)
  })

  it.each(operations.map((op) => [op.operationId, op] as const))('%s', async (id, op) => {
    const { fetch, sent } = mock(ok())
    const sa = client(fetch) as unknown as Record<
      string,
      Record<string, (params: object) => Promise<unknown>>
    >
    const { resource, method } = names[id] as { resource: string; method: string }

    const params: Record<string, unknown> = {}
    const parameters = (op.parameters ?? []).filter((p) => p.name !== 'confirm')
    for (const p of parameters) params[p.name] = sample(p.schema, p.name)
    const properties = op.requestBody?.content['application/json'].schema.properties ?? {}
    for (const [name, schema] of Object.entries(properties)) params[name] = sample(schema, name)

    await sa[resource]?.[method]?.(params)

    expect(sent).toHaveLength(1)
    const request = sent[0] as Sent
    expect(request.method).toBe(op.verb)

    const wantPath = op.path.replace(/\{(\w+)\}/g, (_: string, name: string) =>
      encodeURIComponent(String(params[name])),
    )
    expect(request.url.pathname).toBe(wantPath)

    const query = parameters.filter((p) => p.in === 'query')
    for (const p of query) {
      expect(request.url.searchParams.getAll(p.name)).toEqual([params[p.name]].flat().map(String))
    }
    const confirm = (op.parameters ?? []).some((p) => p.name === 'confirm')
    const wantKeys = query.map((p) => p.name).concat(confirm ? ['confirm'] : [])
    expect(new Set(request.url.searchParams.keys())).toEqual(new Set(wantKeys))

    const wantBody = Object.keys(properties).length
      ? Object.fromEntries(Object.keys(properties).map((name) => [name, params[name]]))
      : undefined
    expect(request.body).toEqual(wantBody)
  })
})

describe('requests', () => {
  it('sends the key, a JSON content type and the SDK user agent', async () => {
    const { fetch, sent } = mock(ok({ handle: 'me' }))
    await expect(client(fetch).account.whoami()).resolves.toEqual({ handle: 'me' })
    const { headers, url } = sent[0] as Sent
    expect(headers.get('authorization')).toBe(`Bearer ${KEY}`)
    expect(headers.get('content-type')).toBe('application/json')
    expect(headers.get('user-agent')).toBe(`superartifacts-typescript/${VERSION}`)
    expect(url.origin).toBe('https://superartifacts.app')
  })

  it('reports the version package.json publishes', () => {
    const pkg = JSON.parse(readFileSync(new URL('../package.json', import.meta.url), 'utf8'))
    expect(VERSION).toBe(pkg.version)
  })

  it('takes a base URL and per-request headers', async () => {
    const { fetch, sent } = mock(ok())
    const sa = new SuperArtifacts({ apiKey: KEY, fetch, baseUrl: 'http://localhost:9/' })
    await sa.account.whoami({}, { headers: { 'X-Trace': 'a' } })
    expect(String((sent[0] as Sent).url)).toBe('http://localhost:9/v1/whoami')
    expect((sent[0] as Sent).headers.get('x-trace')).toBe('a')
  })

  it('escapes path values', async () => {
    const { fetch, sent } = mock(ok())
    await client(fetch).artifacts.get({ artifact: 'a/b c' })
    expect((sent[0] as Sent).url.pathname).toBe('/v1/artifacts/a%2Fb%20c')
  })

  it('refuses a missing path value rather than addressing the list', () => {
    const { fetch, sent } = mock(ok())
    const sa = client(fetch)
    expect(() => sa.artifacts.get({ artifact: '' })).toThrow(/needs artifact/)
    expect(sent).toHaveLength(0)
  })

  it('sets confirm from the id on the deletes that need it', async () => {
    const { fetch, sent } = mock(ok())
    const sa = client(fetch)
    await sa.artifacts.delete({ artifact: 'my-slug' })
    await sa.projects.delete({ project: 'p1' })
    expect((sent[0] as Sent).url.searchParams.getAll('confirm')).toEqual(['my-slug'])
    expect((sent[1] as Sent).url.searchParams.getAll('confirm')).toEqual(['p1'])
  })

  it('leaves a body confirm to the caller', async () => {
    const { fetch, sent } = mock(ok())
    await client(fetch).projects.update({ project: 'p1', title: 'T', confirm: true })
    expect((sent[0] as Sent).body).toEqual({ title: 'T', confirm: true })
    expect((sent[0] as Sent).url.search).toBe('')
  })

  it('passes a field the spec does not name on to the API', async () => {
    const { fetch, sent } = mock(ok())
    const sa = client(fetch)
    await sa.account.help({ nope: 1 } as object)
    await sa.projects.create({ nope: 1 } as object)
    expect((sent[0] as Sent).url.searchParams.get('nope')).toBe('1')
    expect((sent[1] as Sent).body).toEqual({ nope: 1 })
  })

  it('tolerates a 200 with no body and refuses one that is not JSON', async () => {
    await expect(client(mock(new Response('')).fetch).account.whoami()).resolves.toEqual({})
    await expect(client(mock(new Response('<html>')).fetch).account.whoami()).rejects.toMatchObject(
      { code: 'invalid_response' },
    )
  })
})

describe('construction', () => {
  it('falls back to the environment variable', async () => {
    vi.stubEnv('SUPERARTIFACTS_API_KEY', 'sa_from_env')
    const { fetch, sent } = mock(ok())
    await new SuperArtifacts({ fetch }).account.whoami()
    expect((sent[0] as Sent).headers.get('authorization')).toBe('Bearer sa_from_env')
  })

  it('says what to do when there is no key', () => {
    vi.stubEnv('SUPERARTIFACTS_API_KEY', '')
    expect(() => new SuperArtifacts()).toThrow(sdk.AuthenticationError)
    const error = catchError(() => new SuperArtifacts())
    expect(error).toBeInstanceOf(sdk.SuperArtifactsError)
    expect(error.status).toBe(0)
    expect(error.code).toBe('missing_api_key')
    expect(error.message).toBe(
      'No API key. Pass { apiKey } or set SUPERARTIFACTS_API_KEY. Create one at https://superartifacts.app/settings/api-keys.',
    )
  })

  it('refuses a browser unless told otherwise', () => {
    vi.stubGlobal('window', {})
    vi.stubGlobal('document', {})
    expect(() => new SuperArtifacts({ apiKey: KEY })).toThrow(/refuses requests from a browser/)
    expect(() => new SuperArtifacts({ apiKey: KEY, dangerouslyAllowBrowser: true })).not.toThrow()
  })
})

describe('errors', () => {
  it.each([
    [400, 'invalid_arguments', 'InvalidArgumentsError'],
    [400, 'invalid_filter', 'InvalidArgumentsError'],
    [401, 'unauthorized', 'AuthenticationError'],
    [402, 'plan_limit', 'PlanLimitError'],
    [403, 'forbidden', 'PermissionError'],
    [403, 'scope_required', 'ScopeRequiredError'],
    [404, 'not_found', 'NotFoundError'],
    [409, 'conflict', 'ConflictError'],
    [413, 'payload_too_large', 'PayloadTooLargeError'],
    [429, 'rate_limited', 'RateLimitError'],
    [500, 'internal', 'InternalError'],
    [503, 'workspace_busy', 'InternalError'],
  ])('%i %s is %s', async (status, code, name) => {
    const { fetch } = mock(refused(status, code))
    const error = await client(fetch, 0)
      .account.whoami()
      .catch((caught) => caught)
    expect(error).toBeInstanceOf(sdk[name as keyof typeof sdk])
    expect(error).toBeInstanceOf(sdk.SuperArtifactsError)
    expect(error).toMatchObject({ name, status, code, message: `refused ${code}` })
    expect(JSON.stringify({ ...error, message: error.message })).not.toContain(KEY)
  })

  it('tolerates a body that is not JSON', async () => {
    const { fetch } = mock(new Response('<html>bad gateway</html>', { status: 404 }))
    await expect(client(fetch).account.whoami()).rejects.toMatchObject({
      status: 404,
      code: 'http_error',
    })
  })

  it('keeps the rest of the error object', async () => {
    const body = { error: { code: 'x', message: 'm', approvalUrl: 'https://a' } }
    const { fetch } = mock(Response.json(body, { status: 403 }))
    await expect(client(fetch).account.whoami()).rejects.toMatchObject({
      details: { approvalUrl: 'https://a' },
    })
  })

  it('never puts the key in a connection failure', async () => {
    const { fetch } = mock(new TypeError('fetch failed'))
    const error = await client(fetch, 0)
      .account.whoami()
      .catch((caught) => caught)
    expect(error).toBeInstanceOf(sdk.ConnectionError)
    expect(error.message).not.toContain(KEY)
  })

  it('names a timeout', async () => {
    const hang = ((_: unknown, init: RequestInit) =>
      new Promise((_resolve, reject) => {
        init.signal?.addEventListener('abort', () => reject(init.signal?.reason))
      })) as typeof globalThis.fetch
    const sa = new SuperArtifacts({ apiKey: KEY, fetch: hang, timeout: 5, maxRetries: 0 })
    await expect(sa.account.whoami()).rejects.toBeInstanceOf(sdk.TimeoutError)
  })

  it('rethrows the caller abort and does not retry it', async () => {
    const controller = new AbortController()
    const { fetch, sent } = mock(new DOMException('aborted', 'AbortError'))
    controller.abort(new Error('stop'))
    const request = client(fetch).account.whoami({}, { signal: controller.signal })
    await expect(request).rejects.toThrow('stop')
    expect(sent).toHaveLength(1)
  })
})

describe('retries', () => {
  it('waits out Retry-After on a 429, then succeeds', async () => {
    vi.useFakeTimers()
    const { fetch, sent } = mock(refused(429, 'rate_limited', { 'retry-after': '2' }), ok({ a: 1 }))
    const request = client(fetch).projects.update({ project: 'p', title: 't' })
    await vi.advanceTimersByTimeAsync(1_999)
    expect(sent).toHaveLength(1)
    await vi.advanceTimersByTimeAsync(1)
    await expect(request).resolves.toEqual({ a: 1 })
    expect(sent).toHaveLength(2)
  })

  it('stops at maxRetries', async () => {
    const { fetch, sent } = mock(refused(429, 'rate_limited', { 'retry-after': '0' }))
    await expect(client(fetch, 2).account.whoami()).rejects.toMatchObject({
      status: 429,
      retryAfter: 0,
    })
    expect(sent).toHaveLength(3)
  })

  it('does not sit out a Retry-After past the cap', async () => {
    const { fetch, sent } = mock(refused(429, 'rate_limited', { 'retry-after': '3600' }))
    await expect(client(fetch).account.whoami()).rejects.toMatchObject({ retryAfter: 3600 })
    expect(sent).toHaveLength(1)
  })

  it.each([502, 503, 504])('retries %i on a GET with backoff', async (status) => {
    vi.useFakeTimers()
    const { fetch, sent } = mock(refused(status, 'x'), ok())
    const request = client(fetch).account.whoami()
    await vi.advanceTimersByTimeAsync(249)
    expect(sent).toHaveLength(1)
    await vi.advanceTimersByTimeAsync(251)
    await request
    expect(sent).toHaveLength(2)
  })

  it('never retries a 500 or a 4xx other than 429', async () => {
    for (const status of [500, 400, 401, 404, 409]) {
      const { fetch, sent } = mock(refused(status, 'x'))
      await expect(client(fetch).account.whoami()).rejects.toMatchObject({ status })
      expect(sent).toHaveLength(1)
    }
  })

  it('retries a network error on a DELETE', async () => {
    vi.useFakeTimers()
    const { fetch, sent } = mock(new TypeError('fetch failed'), ok())
    const request = client(fetch).projects.delete({ project: 'p' })
    await vi.advanceTimersByTimeAsync(500)
    await request
    expect(sent).toHaveLength(2)
  })

  it('does not retry a POST with no key on a 5xx or a network error', async () => {
    for (const answer of [refused(503, 'x'), new TypeError('fetch failed')]) {
      const { fetch, sent } = mock(answer)
      await expect(
        client(fetch).artifacts.publish(PAGE, { idempotencyKey: false }),
      ).rejects.toBeInstanceOf(sdk.SuperArtifactsError)
      expect(sent).toHaveLength(1)
      expect((sent[0] as Sent).headers.has('idempotency-key')).toBe(false)
    }
  })

  it('retries a POST with its automatic key, the same key each time', async () => {
    vi.useFakeTimers()
    const { fetch, sent } = mock(refused(503, 'x'), refused(502, 'x'), ok())
    const sa = client(fetch)
    const request = sa.artifacts.publish(PAGE)
    await vi.advanceTimersByTimeAsync(3_000)
    await request
    expect(sent).toHaveLength(3)
    const keys = sent.map(({ headers }) => headers.get('idempotency-key'))
    expect(keys[0]).toMatch(/^[0-9a-f-]{36}$/)
    expect(new Set(keys).size).toBe(1)

    await sa.artifacts.publish(PAGE)
    expect((sent[3] as Sent).headers.get('idempotency-key')).not.toBe(keys[0])
  })

  it('sends the caller key when given one', async () => {
    const { fetch, sent } = mock(ok())
    await client(fetch).artifacts.publish(PAGE, { idempotencyKey: 'mine' })
    expect((sent[0] as Sent).headers.get('idempotency-key')).toBe('mine')
  })

  it('does not retry a PATCH on a 5xx, key or no key: the API honours keys on POST only', async () => {
    const { fetch, sent } = mock(refused(503, 'x'))
    const update = client(fetch).artifacts.update(
      { artifact: 'a', visibility: 'private' },
      { idempotencyKey: 'k' },
    )
    await expect(update).rejects.toMatchObject({ status: 503 })
    expect(sent).toHaveLength(1)
  })
})

describe('pagination', () => {
  it('walks data rows across cursors', async () => {
    const { fetch, sent } = mock(
      ok({ responses: [{ id: 1 }, { id: 2 }], cursor: { next: 'c2' } }),
      ok({ responses: [{ id: 3 }], cursor: { next: null } }),
    )
    const rows = await Array.fromAsync(client(fetch).data.iterRows({ dataset: 'd', limit: 2 }))
    expect(rows).toEqual([{ id: 1 }, { id: 2 }, { id: 3 }])
    expect((sent[0] as Sent).url.searchParams.has('cursor')).toBe(false)
    expect((sent[1] as Sent).url.search).toBe('?dataset=d&limit=2&cursor=c2')
  })

  it('walks one artifact from a given cursor', async () => {
    const { fetch, sent } = mock(ok({ responses: [{ id: 1 }], cursor: { next: null } }))
    const rows = client(fetch).data.iterArtifactRows({ artifact: 'a', cursor: 'start' })
    expect(await Array.fromAsync(rows)).toEqual([{ id: 1 }])
    expect((sent[0] as Sent).url.searchParams.get('cursor')).toBe('start')
  })

  it('walks mentions on cursorNext', async () => {
    const { fetch, sent } = mock(
      ok({ mentions: [{ id: 1 }], cursorNext: 'c2' }),
      ok({ mentions: [{ id: 2 }], cursorNext: null }),
    )
    expect(await Array.fromAsync(client(fetch).mentions.iter())).toEqual([{ id: 1 }, { id: 2 }])
    expect((sent[1] as Sent).url.searchParams.get('cursor')).toBe('c2')
  })

  it('walks collection entries by page and stops at the total', async () => {
    const { fetch, sent } = mock(
      ok({ entries: [{ id: 1 }, { id: 2 }], total: 3, page: 0, pageSize: 2 }),
      ok({ entries: [{ id: 3 }], total: 3, page: 1, pageSize: 2 }),
    )
    const entries = await Array.fromAsync(client(fetch).entries.iter({ collection: 'c' }))
    expect(entries).toHaveLength(3)
    expect(sent.map(({ url }) => url.searchParams.get('page'))).toEqual(['0', '1'])
  })
})

describe('uploads', () => {
  it('stages the declared sizes, then PUTs each file with no key', async () => {
    const stage = ok({
      uploadId: 'up_1',
      expiresAt: 'soon',
      uploads: [{ url: 'https://edge.test/uploads/a' }, { url: 'https://edge.test/uploads/b' }],
    })
    const { fetch, sent } = mock(stage, Response.json({ ok: true }, { status: 201 }))
    const answer = await client(fetch).uploads.upload([
      { path: 'a.txt', data: 'héllo', contentType: 'text/plain' },
      { path: 'b.bin', data: new Uint8Array(3) },
    ])

    expect(answer).toEqual({ uploadId: 'up_1', expiresAt: 'soon' })
    expect((sent[0] as Sent).body).toEqual({
      files: [
        { path: 'a.txt', bytes: 6, contentType: 'text/plain' },
        { path: 'b.bin', bytes: 3 },
      ],
    })
    expect(sent.slice(1).map(({ method, url }) => [method, url.pathname])).toEqual([
      ['PUT', '/uploads/a'],
      ['PUT', '/uploads/b'],
    ])
    for (const put of sent.slice(1)) expect(put.headers.has('authorization')).toBe(false)
    expect(await ((sent[1] as Sent).body as Blob).text()).toBe('héllo')
  })

  it('retries a PUT that hit a 502', async () => {
    vi.useFakeTimers()
    const stage = ok({
      uploadId: 'up_1',
      expiresAt: 'soon',
      uploads: [{ url: 'https://e.test/a' }],
    })
    const { fetch, sent } = mock(stage, refused(502, 'x'), ok())
    const request = client(fetch).uploads.upload([{ path: 'a', data: 'x' }])
    await vi.advanceTimersByTimeAsync(1_000)
    await request
    expect(sent.map(({ method }) => method)).toEqual(['POST', 'PUT', 'PUT'])
  })
})
