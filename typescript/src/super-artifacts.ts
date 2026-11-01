import type { JsonObject, Params, RequestOptions } from './core.js'
import type { operations } from './generated/openapi.js'
import {
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

/** The client for the Super Artifacts REST API. Server-side only. */
export class SuperArtifacts extends Resources {
  override readonly data = new Data(this)
  override readonly entries = new Entries(this)
  override readonly mentions = new Mentions(this)
  override readonly uploads = new Uploads(this)
}
