# Super Artifacts SDKs

Open-source clients for the [Super Artifacts](https://superartifacts.app) REST API: publish
artifacts, read what visitors submitted, manage projects and templates, from your own code. Both
are generated from the API's OpenAPI document.

| Package | Install | Runtimes |
| --- | --- | --- |
| [`@superartifacts/sdk`](https://www.npmjs.com/package/@superartifacts/sdk) ([source](typescript)) | `npm install @superartifacts/sdk` | Node 20.3+, Bun, Deno, Cloudflare Workers |
| [`superartifacts`](https://pypi.org/project/superartifacts/) ([source](python)) | `pip install superartifacts` | Python 3.10+ |

Create a key in [Settings → API keys](https://superartifacts.app/settings/api-keys) and put it in
`SUPERARTIFACTS_API_KEY`.

```ts
import { SuperArtifacts } from '@superartifacts/sdk'
const sa = new SuperArtifacts()
await sa.artifacts.publish({ slug: 'hello', prompt: 'A hello page.', html: '<h1>Hello</h1>' })
```

```python
from superartifacts import SuperArtifacts
sa = SuperArtifacts()
sa.artifacts.publish(slug="hello", prompt="A hello page.", html="<h1>Hello</h1>")
```

**Server-side only.** The API refuses any request carrying an `Origin` header, which every browser
adds, and a key on a page is a leaked key.

## Docs

- [SDKs overview](https://superartifacts.app/docs/sdks)
- [TypeScript](https://superartifacts.app/docs/sdks/typescript)
- [Python](https://superartifacts.app/docs/sdks/python)
- [REST API reference](https://superartifacts.app/docs/reference/api)

## License

MIT

## About this repository

This repository is a mirror of the `sdks/` directory of the maintainers' private
monorepo, and every sync replaces its history. Pull requests and issues are
welcome here; an accepted change is ported to the monorepo and arrives in the
next sync. Both SDKs are generated from `openapi.json`.
