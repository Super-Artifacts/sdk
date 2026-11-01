/**
 * What a consumer writes, held to `pnpm typecheck` under strict, noUncheckedIndexedAccess and
 * exactOptionalPropertyTypes. It is compiled, never run.
 */
import { NotFoundError, type Result, SuperArtifacts } from './index.js'

export async function untypedResults() {
  const sa = new SuperArtifacts({ apiKey: 'unused' })

  const { artifacts } = await sa.artifacts.list()
  const slug: string = artifacts[0].slug

  for await (const row of sa.data.iterArtifactRows({ artifact: 'hello' })) {
    console.log(row.x.y)
  }

  try {
    await sa.artifacts.get({ artifact: 'nope' })
  } catch (e) {
    if (e instanceof NotFoundError) console.log(e.status)
  }

  return slug
}

type Described<R> = { responses: { 200: { content: { 'application/json': R } } } }

export function describedResultsKeepTheirSchema(
  closed: Result<Described<{ slug: string }>>,
  open: Result<Described<{ slug: string; [key: string]: unknown }>>,
) {
  // @ts-expect-error a declared property keeps its type
  closed.slug.nope
  // @ts-expect-error a declared schema is not widened by its index signature
  open.slug.nope
}
