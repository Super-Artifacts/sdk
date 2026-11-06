"""The hand-written parts of the resources: paging, the upload round trip and publishing a file."""

from __future__ import annotations

import os
import re
from collections.abc import AsyncIterator, Callable, Iterator, Mapping
from pathlib import Path
from typing import Any

from ._errors import SuperArtifactsError

OMIT: Any = object()
"""Leave a field out, where None would send a null that means something."""

Files = Mapping[str, "bytes | str | os.PathLike[str]"]


def _items(page: dict[str, Any], key: str) -> list[Any]:
    items = page.get(key)
    if items is None:
        raise SuperArtifactsError(f"This read answered no {key!r} to page through.")
    return items


def _next_cursor(page: dict[str, Any]) -> str | None:
    # Data reads answer `cursor.next`, mentions answer `cursorNext`.
    cursor = page.get("cursor")
    return cursor.get("next") if isinstance(cursor, dict) else page.get("cursorNext")


def _last_page(page: dict[str, Any], number: int, items: list[Any]) -> bool:
    return not items or (number + 1) * page.get("pageSize", len(items)) >= page.get("total", 0)


def walk_cursor(fetch: Callable[..., Any], key: str, args: dict[str, Any]) -> Iterator[Any]:
    args = dict(args)
    while True:
        page = fetch(**args)
        yield from _items(page, key)
        args["cursor"] = _next_cursor(page)
        if not args["cursor"]:
            return


async def awalk_cursor(
    fetch: Callable[..., Any], key: str, args: dict[str, Any]
) -> AsyncIterator[Any]:
    args = dict(args)
    while True:
        page = await fetch(**args)
        for item in _items(page, key):
            yield item
        args["cursor"] = _next_cursor(page)
        if not args["cursor"]:
            return


def walk_pages(fetch: Callable[..., Any], key: str, args: dict[str, Any]) -> Iterator[Any]:
    args = dict(args)
    args.setdefault("page", 0)
    while True:
        page = fetch(**args)
        items = _items(page, key)
        yield from items
        if _last_page(page, args["page"], items):
            return
        args["page"] += 1


async def awalk_pages(
    fetch: Callable[..., Any], key: str, args: dict[str, Any]
) -> AsyncIterator[Any]:
    args = dict(args)
    args.setdefault("page", 0)
    while True:
        page = await fetch(**args)
        items = _items(page, key)
        for item in items:
            yield item
        if _last_page(page, args["page"], items):
            return
        args["page"] += 1


def _read(files: Files) -> dict[str, bytes]:
    return {
        path: bytes(source) if isinstance(source, (bytes, bytearray)) else Path(source).read_bytes()
        for path, source in files.items()
    }


def _declare(blobs: dict[str, bytes]) -> list[dict[str, Any]]:
    return [{"path": path, "bytes": len(blob)} for path, blob in blobs.items()]


class UploadHelper:
    def upload(self, files: Files, *, timeout: float | None = None) -> dict[str, Any]:
        """Stage `{path in the artifact: bytes or local file}` and PUT each file.

        Returns what `stage` answered; pass its `uploadId` to
        `artifacts.publish(uploads=...)`. The URLs are the credential, so the
        API key is not sent with the bytes.
        """
        blobs = _read(files)
        staged = self.stage(files=_declare(blobs), timeout=timeout)  # type: ignore[attr-defined]
        # The answer lists the files in the order they were declared.
        for upload, blob in zip(staged["uploads"], blobs.values(), strict=True):
            self._client._request("PUT", upload["url"], timeout, {"content": blob})  # type: ignore[attr-defined]
        return staged


class AsyncUploadHelper:
    async def upload(self, files: Files, *, timeout: float | None = None) -> dict[str, Any]:
        """Stage `{path in the artifact: bytes or local file}` and PUT each file.

        Returns what `stage` answered; pass its `uploadId` to
        `artifacts.publish(uploads=...)`. The URLs are the credential, so the
        API key is not sent with the bytes.
        """
        blobs = _read(files)
        staged = await self.stage(files=_declare(blobs), timeout=timeout)  # type: ignore[attr-defined]
        for upload, blob in zip(staged["uploads"], blobs.values(), strict=True):
            await self._client._request("PUT", upload["url"], timeout, {"content": blob})  # type: ignore[attr-defined]
        return staged


def _slug_of(path: Path) -> str:
    name = path.parent.name if path.name == "index.html" else path.stem if path.is_file() else path.name
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def _gather(path: str | os.PathLike[str], slug: str | None) -> tuple[str, str, dict[str, Path]]:
    """Resolve `path` to (slug, index.html text, every other file by its path in the artifact)."""
    root = Path(path).resolve()
    slug = slug or _slug_of(root)
    if not slug:
        raise SuperArtifactsError(f"Cannot name an artifact after {str(root)!r}: pass slug=.")
    if root.is_file():
        return slug, root.read_text(encoding="utf-8"), {}
    if not (root / "index.html").is_file():
        raise SuperArtifactsError(f"{str(root)!r} is not a file, or a folder with an index.html.")
    beside = {
        file.relative_to(root).as_posix(): file
        for file in sorted(root.rglob("*"))
        if file.is_file() and not any(part.startswith(".") for part in file.relative_to(root).parts)
    }
    html = beside.pop("index.html").read_text(encoding="utf-8")
    return slug, html, beside


class ArtifactHelper:
    def publish_file(
        self,
        path: str | os.PathLike[str],
        *,
        slug: str | None = None,
        timeout: float | None = None,
        **fields: Any,
    ) -> dict[str, Any]:
        """Publish a page you already made: an HTML file, or a folder with an `index.html`.

        The page comes from your own model, your own tools, your own build; this
        hosts it. A folder's other files go up beside it, uploaded for you. `slug`
        defaults to the file's name (the folder's name for a folder or an
        `index.html`); every other field is what `publish` takes.
        """
        slug, html, beside = _gather(path, slug)
        if beside:
            staged = self._client.uploads.upload(beside, timeout=timeout)  # type: ignore[attr-defined]
            fields["uploads"] = staged["uploadId"]
        return self.publish(slug=slug, html=html, timeout=timeout, **fields)  # type: ignore[attr-defined]


class AsyncArtifactHelper:
    async def publish_file(
        self,
        path: str | os.PathLike[str],
        *,
        slug: str | None = None,
        timeout: float | None = None,
        **fields: Any,
    ) -> dict[str, Any]:
        """Publish a page you already made: an HTML file, or a folder with an `index.html`.

        The page comes from your own model, your own tools, your own build; this
        hosts it. A folder's other files go up beside it, uploaded for you. `slug`
        defaults to the file's name (the folder's name for a folder or an
        `index.html`); every other field is what `publish` takes.
        """
        slug, html, beside = _gather(path, slug)
        if beside:
            staged = await self._client.uploads.upload(beside, timeout=timeout)  # type: ignore[attr-defined]
            fields["uploads"] = staged["uploadId"]
        return await self.publish(slug=slug, html=html, timeout=timeout, **fields)  # type: ignore[attr-defined]
