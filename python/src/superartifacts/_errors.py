"""What a refused or failed call raises."""

from __future__ import annotations

from typing import Any

import httpx


class SuperArtifactsError(Exception):
    """Base of every error here. `code` is stable; `message` is for a person."""

    def __init__(
        self,
        message: str,
        *,
        status: int | None = None,
        code: str | None = None,
        retry_after: float | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status = status
        self.code = code
        self.retry_after = retry_after
        self.details = details or {}


class InvalidArgumentsError(SuperArtifactsError):
    """400: the request was refused as written."""


class AuthenticationError(SuperArtifactsError):
    """401, or no key to send."""


class PlanLimitError(SuperArtifactsError):
    """402: the account's plan does not allow this."""


class PermissionError(SuperArtifactsError):
    """403 forbidden."""


class ScopeRequiredError(PermissionError):
    """403 scope_required: a read key called a write."""


class NotFoundError(SuperArtifactsError):
    """404."""


class ConflictError(SuperArtifactsError):
    """409."""


class PayloadTooLargeError(SuperArtifactsError):
    """413: over 1 MiB of JSON. Use `uploads.upload` for files."""


class RateLimitError(SuperArtifactsError):
    """429 after the retries ran out. `retry_after` is in seconds."""


class InternalError(SuperArtifactsError):
    """5xx."""


class APIConnectionError(SuperArtifactsError):
    """The request never got an answer."""


class APITimeoutError(APIConnectionError):
    """The request took longer than `timeout`."""


_BY_STATUS = {
    400: InvalidArgumentsError,
    401: AuthenticationError,
    402: PlanLimitError,
    403: PermissionError,
    404: NotFoundError,
    409: ConflictError,
    413: PayloadTooLargeError,
    429: RateLimitError,
}


def parse_seconds(value: Any) -> float | None:
    """A Retry-After in seconds; the HTTP-date form and junk read as absent."""
    try:
        seconds = float(value)
    except (TypeError, ValueError):
        return None
    return seconds if seconds >= 0 else None


def error_from(response: httpx.Response) -> SuperArtifactsError:
    """The error for a non-2xx answer, whatever its body turned out to be."""
    try:
        body = response.json()
    except ValueError:
        # A proxy's HTML page rather than the API: the status is all there is.
        body = None
    error = body.get("error") if isinstance(body, dict) else None
    error = error if isinstance(error, dict) else {}

    status = response.status_code
    code = error.get("code") if isinstance(error.get("code"), str) else None
    message = error.get("message")
    if not isinstance(message, str):
        message = f"The API answered {status} {response.reason_phrase}".strip()

    if status == 403 and code == "scope_required":
        kind = ScopeRequiredError
    elif status >= 500:
        kind = InternalError
    else:
        kind = _BY_STATUS.get(status, SuperArtifactsError)

    retry_after = parse_seconds(response.headers.get("retry-after"))
    if retry_after is None:
        retry_after = parse_seconds(error.get("retryAfterSeconds"))
    return kind(message, status=status, code=code, retry_after=retry_after, details=error)
