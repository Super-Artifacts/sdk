# @superartifacts/sdk

The TypeScript SDK for the [Super Artifacts](https://superartifacts.app) REST API. No runtime
dependencies. Node 20.3+, Bun, Deno and Cloudflare Workers.

```bash
npm install @superartifacts/sdk
```

**Server-side only.** The API refuses any request carrying an `Origin` header, which means every
browser, and a key on a page is a leaked key. The client throws if you construct it in a browser.

## Quickstart

Create a key in [Settings → API keys](https://superartifacts.app/settings/api-keys) and put it in
`SUPERARTIFACTS_API_KEY`.

```ts
import { SuperArtifacts } from '@superartifacts/sdk'

const sa = new SuperArtifacts()

const me = await sa.account.whoami()
console.log(me)

const published = await sa.artifacts.publish({
  slug: 'hello',
  title: 'Hello',
  prompt: 'A page that says hello.',
  html: '<h1>Hello</h1>',
})
console.log(published)

const { artifacts } = await sa.artifacts.list()
console.log(artifacts)

for await (const row of sa.data.iterArtifactRows({ artifact: 'hello' })) {
  console.log(row)
}
```

Every method takes one object holding the operation's path, query and body fields together, and an
optional second argument for this request alone:

```ts
await sa.artifacts.update({ artifact: 'hello', visibility: 'private' }, { timeout: 10_000 })
```

Resources: `account`, `artifacts`, `live`, `uploads`, `data`, `schema`, `entries`, `secrets`,
`templates`, `projects`, `shares`, `comments`, `mentions`, `signatures`.

## Configuration

```ts
new SuperArtifacts({
  apiKey: process.env.SUPERARTIFACTS_API_KEY, // the default
  baseUrl: 'https://superartifacts.app',      // the default
  timeout: 60_000,                            // milliseconds per attempt
  maxRetries: 2,
  fetch: globalThis.fetch,
})
```

Per request: `{ idempotencyKey, timeout, signal, headers }`.

## Errors

Every failure is a `SuperArtifactsError` with `status`, `code`, `message` and, when the API asked
you to wait, `retryAfter` in seconds. Anything else the API said is in `details`.

| Class | When |
| --- | --- |
| `InvalidArgumentsError` | 400 |
| `AuthenticationError` | 401 |
| `PlanLimitError` | 402 |
| `PermissionError` | 403 `forbidden` |
| `ScopeRequiredError` | 403 `scope_required`: a read key called a write |
| `NotFoundError` | 404 |
| `ConflictError` | 409 |
| `PayloadTooLargeError` | 413: over 1 MiB, see [Uploads](#uploads) |
| `RateLimitError` | 429 |
| `InternalError` | 5xx |
| `ConnectionError` | no answer arrived (`status` 0) |
| `TimeoutError` | the attempt ran out of time (`status` 0) |

```ts
import { NotFoundError } from '@superartifacts/sdk'

try {
  await sa.artifacts.get({ artifact: 'nope' })
} catch (error) {
  if (error instanceof NotFoundError) console.log(error.code)
  else throw error
}
```

## Retries

- A `429` is retried after its `Retry-After`. Past 60 seconds it is not waited out: the
  `RateLimitError` comes straight back with `retryAfter` set.
- `502`, `503`, `504`, timeouts and network errors are retried with backoff on `GET`, `DELETE` and
  any `POST` carrying an `Idempotency-Key`.
- Every `POST` carries one: a fresh UUID per call, reused across that call's retries, so a retried
  publish happens once. Pass your own with `{ idempotencyKey }` to make a call safe to repeat across
  restarts, or `{ idempotencyKey: false }` to send none, which turns these retries off.
- No other `4xx` is retried, and neither is a `PATCH` or `PUT`.

## Pagination

Operations that page have an iterator that fetches pages as you read:

```ts
for await (const row of sa.data.iterRows({ dataset: 'signups' })) console.log(row)
for await (const row of sa.data.iterArtifactRows({ artifact: 'hello' })) console.log(row)
for await (const entry of sa.entries.iter({ collection: 'posts' })) console.log(entry)
for await (const mention of sa.mentions.iter()) console.log(mention)
```

`sa.comments.list` returns one page.

## Uploads

A request body is capped at 1 MiB. Files bigger than that are staged, then published by id:

```ts
import { readFile } from 'node:fs/promises'

const { uploadId } = await sa.uploads.upload([
  { path: 'images/hero.png', data: await readFile('hero.png') },
])

await sa.artifacts.publish({
  slug: 'hello',
  prompt: 'A page with a hero image.',
  html: '<img src="images/hero.png">',
  uploads: uploadId,
})
```

One file may be 5 MiB and one upload 10 MiB. A staged set expires after 30 minutes.

## Links

- [SDK documentation](https://superartifacts.app/docs/sdks/typescript)
- [REST API reference](https://superartifacts.app/docs/reference/api)
- [OpenAPI document](https://superartifacts.app/v1/openapi.json)

## License

MIT
