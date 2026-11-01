"""The two clients. One retry policy, written once, driven by two small loops."""

from __future__ import annotations

import asyncio
import os
import random
import time
import uuid
from importlib.metadata import PackageNotFoundError, version
from itertools import count
from typing import Any
from urllib.parse import quote

import httpx

from ._errors import (
    APIConnectionError,
    APITimeoutError,
    AuthenticationError,
    error_from,
    parse_seconds,
)
from ._generated.resources import AsyncResources, SyncResources
from ._helpers import OMIT

DEFAULT_BASE_URL = "https://superartifacts.app"
MAX_RETRY_AFTER = 60.0
BACKOFF_BASE = 0.5
BACKOFF_MAX = 8.0

try:
    __version__ = version("superartifacts")
except PackageNotFoundError:
    # Vendored without its metadata; only the User-Agent reads this.
    __version__ = "0.0.0"


def _backoff(attempt: int) -> float:
    """Exponential, jittered over the top half: 0.25-0.5 s, 0.5-1 s, ..., 4-8 s."""
    ceiling = min(BACKOFF_BASE * 2**attempt, BACKOFF_MAX)
    return random.uniform(ceiling / 2, ceiling)


def _connection_error(exc: httpx.TransportError) -> APIConnectionError:
    if isinstance(exc, httpx.TimeoutException):
        return APITimeoutError("The request timed out. Raise `timeout`, or try again.")
    return APIConnectionError(f"Could not reach the API ({type(exc).__name__}). Try again.")


def _answer(response: httpx.Response) -> dict[str, Any]:
    # An upload PUT may answer with no JSON at all; its status said what mattered.
    try:
        body = response.json()
    except ValueError:
        return {}
    return body if isinstance(body, dict) else {"data": body}


class _Base:
    def __init__(self, api_key: str | None, base_url: str, timeout: float, max_retries: int):
        key = api_key or os.environ.get("SUPERARTIFACTS_API_KEY")
        if not key:
            raise AuthenticationError(
                "No API key. Pass api_key= or set SUPERARTIFACTS_API_KEY. "
                "Create one at https://superartifacts.app/settings/api-keys."
            )
        self._api_key = key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries

    def _prepare(
        self,
        method: str,
        path: str,
        path_params: dict[str, Any] | None,
        query: dict[str, Any] | None,
        body: dict[str, Any] | None,
        nullable: dict[str, Any] | None,
        idempotency_key: str | None,
    ) -> tuple[str, dict[str, Any]]:
        """The URL and httpx arguments for one operation."""
        for name, value in (path_params or {}).items():
            path = path.replace("{" + name + "}", quote(str(value), safe=""))
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Accept": "application/json",
            "User-Agent": f"superartifacts-python/{__version__}",
        }
        # Made here, once, so every retry of this call carries the same key.
        if method == "POST":
            headers["Idempotency-Key"] = idempotency_key or str(uuid.uuid4())
        parts: dict[str, Any] = {"headers": headers}
        if query:
            parts["params"] = {k: v for k, v in query.items() if v is not None}
        if body is not None:
            parts["json"] = {k: v for k, v in body.items() if v is not None}
            parts["json"].update({k: v for k, v in (nullable or {}).items() if v is not OMIT})
        return self.base_url + path, parts

    def _retry_delay(
        self,
        method: str,
        parts: dict[str, Any],
        attempt: int,
        status: int | None = None,
        retry_after: str | None = None,
    ) -> float | None:
        """Seconds to wait before another try, or None to stop. `status` None is a network error."""
        if attempt >= self.max_retries:
            return None
        if status == 429:
            seconds = parse_seconds(retry_after)
            if seconds is None:
                return _backoff(attempt)
            # Past a minute (the hourly email limit) waiting it out would hang the caller:
            # the RateLimitError comes straight back with retry_after set, as in the TypeScript SDK.
            return seconds if seconds <= MAX_RETRY_AFTER else None
        if status not in (None, 502, 503, 504):
            return None
        safe = method in ("GET", "DELETE") or "Idempotency-Key" in parts.get("headers", {})
        return _backoff(attempt) if safe else None


class SuperArtifacts(_Base, SyncResources):
    """Synchronous client. Use it as a context manager, or call `close()`."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 60.0,
        max_retries: int = 2,
        http_client: httpx.Client | None = None,
    ) -> None:
        _Base.__init__(self, api_key, base_url, timeout, max_retries)
        SyncResources.__init__(self)
        self._owns_http = http_client is None
        self._http = http_client or httpx.Client()

    def _call(
        self,
        method: str,
        path: str,
        *,
        path_params: dict[str, Any] | None = None,
        query: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
        nullable: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
        timeout: float | None = None,
    ) -> dict[str, Any]:
        url, parts = self._prepare(
            method, path, path_params, query, body, nullable, idempotency_key
        )
        return self._request(method, url, timeout, parts)

    def _request(
        self, method: str, url: str, timeout: float | None, parts: dict[str, Any]
    ) -> dict[str, Any]:
        wait = self.timeout if timeout is None else timeout
        for attempt in count():
            try:
                response = self._http.request(method, url, timeout=wait, **parts)
            except httpx.TransportError as exc:
                delay = self._retry_delay(method, parts, attempt)
                if delay is None:
                    raise _connection_error(exc) from exc
            else:
                if response.is_success:
                    return _answer(response)
                delay = self._retry_delay(
                    method,
                    parts,
                    attempt,
                    response.status_code,
                    response.headers.get("retry-after"),
                )
                if delay is None:
                    raise error_from(response)
            time.sleep(delay)

    def close(self) -> None:
        """Close the HTTP client, unless it was passed in."""
        if self._owns_http:
            self._http.close()

    def __enter__(self) -> SuperArtifacts:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()


class AsyncSuperArtifacts(_Base, AsyncResources):
    """Asynchronous client, the same surface awaited. `async with`, or `await close()`."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 60.0,
        max_retries: int = 2,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        _Base.__init__(self, api_key, base_url, timeout, max_retries)
        AsyncResources.__init__(self)
        self._owns_http = http_client is None
        self._http = http_client or httpx.AsyncClient()

    async def _call(
        self,
        method: str,
        path: str,
        *,
        path_params: dict[str, Any] | None = None,
        query: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
        nullable: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
        timeout: float | None = None,
    ) -> dict[str, Any]:
        url, parts = self._prepare(
            method, path, path_params, query, body, nullable, idempotency_key
        )
        return await self._request(method, url, timeout, parts)

    async def _request(
        self, method: str, url: str, timeout: float | None, parts: dict[str, Any]
    ) -> dict[str, Any]:
        wait = self.timeout if timeout is None else timeout
        for attempt in count():
            try:
                response = await self._http.request(method, url, timeout=wait, **parts)
            except httpx.TransportError as exc:
                delay = self._retry_delay(method, parts, attempt)
                if delay is None:
                    raise _connection_error(exc) from exc
            else:
                if response.is_success:
                    return _answer(response)
                delay = self._retry_delay(
                    method,
                    parts,
                    attempt,
                    response.status_code,
                    response.headers.get("retry-after"),
                )
                if delay is None:
                    raise error_from(response)
            await asyncio.sleep(delay)

    async def close(self) -> None:
        """Close the HTTP client, unless it was passed in."""
        if self._owns_http:
            await self._http.aclose()

    async def __aenter__(self) -> AsyncSuperArtifacts:
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.close()
