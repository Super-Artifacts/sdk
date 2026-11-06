import type { JsonObject, Params, RequestOptions, Result } from './core.js'
import type { operations } from './generated/openapi.js'
import {
  ArtifactsResource,
  DataResource,
  EntriesResource,
  MentionsResource,
  Resources,
  UploadsResource,
} from './generated/resources.js'

type Row = JsonObject
type Page = JsonObject

async function* byCursor(
  read: (cursor: string | undefined) => Promise<Page>,
  start: string | undefined,
  items: string,
  next: (page: Page) => unknown,
): AsyncGenerator<Row> {
  let cursor = start
  do {
    const page = await read(cursor)
    yield* (page[items] ?? []) as Row[]
    cursor = (next(page) as string | null | undefined) ?? undefined
  } while (cursor !== undefined)
}

const cursorNext = (page: Page): unknown => (page.cursor as { next?: unknown } | undefined)?.next

class Data extends DataResource {
  /** Every row `listArtifactRows` matches, page by page. */
  iterArtifactRows(
    params: Params<operations['listArtifactRows']>,
    options?: RequestOptions,
  ): AsyncGenerator<Row> {
    const read = (cursor?: string) =>
      this.listArtifactRows({ ...params, ...(cursor && { cursor }) }, options)
    return byCursor(read, params.cursor, 'responses', cursorNext)
  }

  /** Every row `listRows` matches, page by page. */
  iterRows(
    params: Params<operations['listRows']> = {},
    options?: RequestOptions,
  ): AsyncGenerator<Row> {
    const read = (cursor?: string) =>
      this.listRows({ ...params, ...(cursor && { cursor }) }, options)
    return byCursor(read, params.cursor, 'responses', cursorNext)
  }
}

class Entries extends EntriesResource {
  /** Every entry `list` matches, page by page from `params.page` (0 by default). */
  async *iter(
    params: Params<operations['listEntries']>,
    options?: RequestOptions,
  ): AsyncGenerator<Row> {
    for (let page = params.page ?? 0; ; page++) {
      const answer: Page = await this.list({ ...params, page }, options)
      const entries = (answer.entries ?? []) as Row[]
      yield* entries
      const { total, pageSize } = answer as { total?: number; pageSize?: number }
      if (entries.length === 0 || (page + 1) * (pageSize ?? entries.length) >= (total ?? 0)) return
    }
  }
}

class Mentions extends MentionsResource {
  /** Every mention, page by page. Listing marks them seen. */
  iter(
    params: Params<operations['listMentions']> = {},
    options?: RequestOptions,
  ): AsyncGenerator<Row> {
    const read = (cursor?: string) => this.list({ ...params, ...(cursor && { cursor }) }, options)
    return byCursor(read, params.cursor, 'mentions', (page) => page.cursorNext)
  }
}

export interface FileToUpload {
  /** Where the file lands in the artifact, e.g. `images/hero.png`. */
  path: string
  data: Uint8Array | Blob | string
  contentType?: string
}

class Uploads extends UploadsResource {
  /** Stage files and PUT their bytes. Pass the answer's `uploadId` to `artifacts.publish` as `uploads`. */
  async upload(
    files: FileToUpload[],
    options?: RequestOptions,
  ): Promise<{ uploadId: string; expiresAt: string }> {
    const blobs = files.map(({ data, contentType }) =>
      data instanceof Blob
        ? data
        : new Blob([data], contentType === undefined ? {} : { type: contentType }),
    )
    const stage = files.map(({ path, contentType }, index) => ({
      path,
      bytes: blobs[index]?.size ?? 0,
      ...(contentType === undefined ? {} : { contentType }),
    }))
    const staged = (await this.stage({ files: stage }, options)) as {
      uploadId: string
      expiresAt: string
      uploads: { url: string }[]
    }
    await this.client.putFiles(staged.uploads, blobs, options)
    return { uploadId: staged.uploadId, expiresAt: staged.expiresAt }
  }
}

type PublishParams = Params<operations['publishArtifact']>

/** What `publishFile` takes beside the path: any `publish` field, but `slug` may be left to the file's name. */
export type PublishFileParams = Omit<PublishParams, 'slug' | 'html' | 'files'> & { slug?: string }

const slugOf = (name: string) =>
  name
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '')

class Artifacts extends ArtifactsResource {
  /**
   * Publish a page you already made: an HTML file, or a folder with an `index.html`.
   *
   * The page comes from your own model, your own tools, your own build; this hosts it.
   * A folder's other files go up beside it, uploaded for you. `slug` defaults to the
   * file's name (the folder's name for a folder or an `index.html`).
   */
  async publishFile(
    path: string,
    params: PublishFileParams = {},
    options?: RequestOptions,
  ): Promise<Result<operations['publishArtifact']>> {
    const fs = await import('node:fs/promises')
    const nodePath = await import('node:path')
    const root = nodePath.resolve(path)
    const isFolder = (await fs.stat(root)).isDirectory()
    const slug =
      params.slug ??
      slugOf(
        isFolder || nodePath.basename(root) === 'index.html'
          ? nodePath.basename(isFolder ? root : nodePath.dirname(root))
          : nodePath.basename(root, nodePath.extname(root)),
      )
    if (slug === '') throw new Error(`Cannot name an artifact after ${root}: pass slug.`)
    if (!isFolder) {
      return this.publish({ ...params, slug, html: await fs.readFile(root, 'utf8') }, options)
    }

    const beside: FileToUpload[] = []
    const walk = async (dir: string): Promise<void> => {
      for (const entry of await fs.readdir(dir, { withFileTypes: true })) {
        if (entry.name.startsWith('.')) continue
        const full = nodePath.join(dir, entry.name)
        if (entry.isDirectory()) await walk(full)
        else if (entry.isFile()) {
          const rel = nodePath.relative(root, full).split(nodePath.sep).join('/')
          if (rel !== 'index.html') beside.push({ path: rel, data: await fs.readFile(full) })
        }
      }
    }
    await walk(root)
    const html = await fs.readFile(nodePath.join(root, 'index.html'), 'utf8').catch(() => {
      throw new Error(`${root} is not a file, or a folder with an index.html.`)
    })
    const uploads =
      beside.length === 0
        ? {}
        : { uploads: (await new Uploads(this.client).upload(beside, options)).uploadId }
    return this.publish({ ...params, ...uploads, slug, html }, options)
  }
}

/** The client for the Super Artifacts REST API. Server-side only. */
export class SuperArtifacts extends Resources {
  override readonly artifacts = new Artifacts(this)
  override readonly data = new Data(this)
  override readonly entries = new Entries(this)
  override readonly mentions = new Mentions(this)
  override readonly uploads = new Uploads(this)
}
