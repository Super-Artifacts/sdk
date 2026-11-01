/**
 * Anything this SDK throws for a failed call. `status` is 0 when no answer arrived, and it
 * and `code` are absent when no request was made: an `AuthenticationError` for a missing key.
 */
export class SuperArtifactsError extends Error {
  readonly status?: number
  /** Stable and machine-readable; `message` is for a person. */
  readonly code?: string
  /** Seconds the API asked to wait. */
  readonly retryAfter?: number
  /** Everything else the API said, e.g. `fix` or `approvalUrl`. */
  readonly details: Record<string, unknown>

  constructor(
    status: number | undefined,
    code: string | undefined,
    message: string,
    retryAfter?: number,
    details: Record<string, unknown> = {},
    options?: ErrorOptions,
  ) {
    super(message, options)
    this.name = new.target.name
    if (status !== undefined) this.status = status
    if (code !== undefined) this.code = code
    if (retryAfter !== undefined) this.retryAfter = retryAfter
    this.details = details
  }
}

export class InvalidArgumentsError extends SuperArtifactsError {}
export class AuthenticationError extends SuperArtifactsError {}
export class PlanLimitError extends SuperArtifactsError {}
export class PermissionError extends SuperArtifactsError {}
export class ScopeRequiredError extends SuperArtifactsError {}
export class NotFoundError extends SuperArtifactsError {}
export class ConflictError extends SuperArtifactsError {}
export class PayloadTooLargeError extends SuperArtifactsError {}
export class RateLimitError extends SuperArtifactsError {}
export class InternalError extends SuperArtifactsError {}
/** The request never got an answer. */
export class ConnectionError extends SuperArtifactsError {}
export class TimeoutError extends SuperArtifactsError {}

function errorClass(status: number, code: string): typeof SuperArtifactsError {
  if (status >= 500) return InternalError
  if (status === 403) return code === 'scope_required' ? ScopeRequiredError : PermissionError
  const byStatus: Record<number, typeof SuperArtifactsError> = {
    400: InvalidArgumentsError,
    401: AuthenticationError,
    402: PlanLimitError,
    404: NotFoundError,
    409: ConflictError,
    413: PayloadTooLargeError,
    422: InvalidArgumentsError,
    429: RateLimitError,
  }
  return byStatus[status] ?? SuperArtifactsError
}

/** The error for an HTTP refusal. `text` may be anything: a proxy's HTML page is not `{error}`. */
export function errorFor(
  status: number,
  text: string,
  retryAfterHeader: string | null,
): SuperArtifactsError {
  let error: Record<string, unknown> = {}
  try {
    const parsed = JSON.parse(text) as { error?: unknown } | null
    if (typeof parsed?.error === 'object' && parsed.error !== null) {
      error = parsed.error as Record<string, unknown>
    }
  } catch {
    // Not JSON: status alone decides the class, and the message says what arrived.
  }
  const { code, message, retryAfterSeconds, ...details } = error
  const named = typeof code === 'string' ? code : 'http_error'
  const seconds = Number(retryAfterHeader ?? retryAfterSeconds)
  const retryAfter =
    (retryAfterHeader !== null || retryAfterSeconds !== undefined) && Number.isFinite(seconds)
      ? seconds
      : undefined
  return new (errorClass(status, named))(
    status,
    named,
    typeof message === 'string' ? message : `The API answered ${status} without an error body.`,
    retryAfter,
    details,
  )
}
