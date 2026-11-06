# Super Artifacts for Python

The official Python SDK for the [Super Artifacts](https://superartifacts.app) REST API: publish
artifacts, read what visitors submitted, manage projects and templates, from your own code.

Full docs: <https://superartifacts.app/docs/sdks/python>

## Install

```bash
pip install superartifacts
```

Python 3.10 or newer. Create a key in
[Settings → API keys](https://superartifacts.app/settings/api-keys).

## Quickstart

```python
import os

from superartifacts import SuperArtifacts

sa = SuperArtifacts(api_key=os.environ["SUPERARTIFACTS_API_KEY"])

print(sa.account.whoami()["handle"])

sa.artifacts.publish(
    slug="hello",
    html="<!doctype html><h1>Hello</h1>",
)

for artifact in sa.artifacts.list()["artifacts"]:
    print(artifact["slug"])

for row in sa.data.iter_artifact_rows(artifact="hello"):
    print(row)
```

`api_key` falls back to `SUPERARTIFACTS_API_KEY`, so `SuperArtifacts()` is enough.

Keyword arguments hold path, query and body fields together, in snake_case: the SDK splits them
as the API expects, so `values_file=` goes out as `valuesFile`. Values nested inside a dict keep
the API's spelling. Answers are plain dicts, as the
[API reference](https://superartifacts.app/docs/reference/api-endpoints) describes them.

**Server-side only.** The API refuses any request carrying an `Origin` header, which every browser
adds. Keep the key on a server.

## Async

`AsyncSuperArtifacts` is the same surface, awaited:

```python
import asyncio

from superartifacts import AsyncSuperArtifacts


async def main():
    async with AsyncSuperArtifacts() as sa:
        print(await sa.account.whoami())
        async for row in sa.data.iter_artifact_rows(artifact="hello"):
            print(row)


asyncio.run(main())
```

## Configuration

```python
SuperArtifacts(
    api_key=None,  # or SUPERARTIFACTS_API_KEY
    base_url="https://superartifacts.app",
    timeout=60.0,  # seconds
    max_retries=2,
    http_client=None,  # your own httpx.Client; yours to close
)
```

Every method also takes `timeout=` for that call, and every `POST` takes `idempotency_key=`.
Use the client as a context manager, or call `close()`.

## Errors

Everything raised is a `SuperArtifactsError`, with `.status`, `.code`, `.message`, `.retry_after`
and the full error object in `.details`.
A client-side failure has `.status` 0 and its own `.code`: a missing key is an `AuthenticationError`
with `missing_api_key`.

| Status | Exception |
| --- | --- |
| 400 | `InvalidArgumentsError` |
| 401 | `AuthenticationError` (also raised when there is no key) |
| 402 | `PlanLimitError` |
| 403 | `PermissionError`, or `ScopeRequiredError` when a read key tried a write |
| 404 | `NotFoundError` |
| 409 | `ConflictError` |
| 413 | `PayloadTooLargeError` |
| 429 | `RateLimitError` |
| 5xx | `InternalError` |
| none | `APIConnectionError`, `APITimeoutError` |

```python
from superartifacts import NotFoundError

try:
    sa.artifacts.get(artifact="missing")
except NotFoundError as error:
    print(error.code, error.message)
```

`superartifacts.PermissionError` is not the builtin of that name: import it by name when you
catch it.

## Retries

Up to `max_retries` more tries, two by default:

- A `429` is retried after its `Retry-After`. Past 60 seconds it is not waited out: the
  `RateLimitError` comes straight back with `retry_after` set.
- `502`, `503`, `504` and network errors are retried with exponential backoff and jitter, for
  `GET`, `DELETE` and `POST`.
- `PATCH` and `PUT` are retried on `429` only. `500` and every other `4xx` are never retried.

Every `POST` sends an `Idempotency-Key`, one per call and the same across its retries, so a retried
publish happens once. Pass `idempotency_key=` to choose your own, which also makes a retry of your
own code safe.

## Pagination

`iter_*` methods walk every page and yield one item at a time, taking the same arguments as the
list they wrap:

| Method | Wraps |
| --- | --- |
| `sa.data.iter_rows(...)` | `sa.data.list_rows(...)`, with `dataset=` or `collection=` |
| `sa.data.iter_artifact_rows(...)` | `sa.data.list_artifact_rows(...)` |
| `sa.entries.iter(...)` | `sa.entries.list(...)` |
| `sa.mentions.iter(...)` | `sa.mentions.list(...)` |

## Publish a page you made

Super Artifacts runs no model: you bring the inference. Make the page with your own model, write it
to a file, publish the file.

```python
from pathlib import Path

from anthropic import Anthropic
from superartifacts import SuperArtifacts

# Your model, your key. We run no inference.
msg = Anthropic().messages.create(
    model="claude-haiku-5-5",
    max_tokens=4000,
    messages=[{
        "role": "user",
        "content": "A launch checklist. HTML only.",
    }],
)
Path("checklist.html").write_text(
    msg.content[0].text
)

# We host the file. Reads SUPERARTIFACTS_API_KEY
sa = SuperArtifacts()
page = sa.artifacts.publish_file(
    "checklist.html"
)
print(page["url"])
```

`publish_file` takes an HTML file, or a folder with an `index.html` (its other files are uploaded
beside it). The slug defaults to the file's or folder's name. `prompt` is optional: send it only if
you want the request shown on the artifact's card; nothing is generated from it.

## Uploads

A JSON body stops at 1 MiB. Bigger files go through `uploads.upload`, which stages them and sends
the bytes straight to their upload URLs. It takes a mapping of path in the artifact to bytes or a
local file, within the limits of 5 MiB a file and 10 MiB a set:

```python
staged = sa.uploads.upload({"images/hero.png": "./hero.png", "notes.txt": b"hello"})

sa.artifacts.publish(
    slug="hello",
    html='<!doctype html><img src="images/hero.png">',
    uploads=staged["uploadId"],
)
```

## License

MIT
