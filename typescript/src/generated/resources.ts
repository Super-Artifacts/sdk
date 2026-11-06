// Generated from sdks/openapi.json (sha256 1b1714ff1a47bc8847fe6336951ca06d6d514f2d8567c9b4a8c759cc175b5288). Do not edit: run `pnpm sdk:generate`.
import { Core, type Operation, type Params, type RequestOptions, type Result } from '../core.js'
import type { operations } from './openapi.js'

export const OPERATIONS = {
  whoami: { method: 'GET', path: '/v1/whoami', query: [] },
  getHelp: { method: 'GET', path: '/v1/help', query: ['topic'] },
  listArtifacts: { method: 'GET', path: '/v1/artifacts', query: [] },
  publishArtifact: { method: 'POST', path: '/v1/artifacts', query: [] },
  getArtifact: { method: 'GET', path: '/v1/artifacts/{artifact}', query: [] },
  updateArtifact: { method: 'PATCH', path: '/v1/artifacts/{artifact}', query: [] },
  deleteArtifact: {
    method: 'DELETE',
    path: '/v1/artifacts/{artifact}',
    query: [],
    confirm: 'artifact',
  },
  readArtifactFile: {
    method: 'GET',
    path: '/v1/artifacts/{artifact}/file',
    query: ['path', 'version'],
  },
  openArtifact: { method: 'POST', path: '/v1/artifacts/{artifact}/open', query: [] },
  serveVersion: {
    method: 'POST',
    path: '/v1/artifacts/{artifact}/versions/{version}/serve',
    query: [],
  },
  startLiveRoom: { method: 'POST', path: '/v1/artifacts/{artifact}/live', query: [] },
  stopLiveRoom: { method: 'DELETE', path: '/v1/artifacts/{artifact}/live', query: [] },
  stageUploads: { method: 'POST', path: '/v1/uploads', query: [] },
  listArtifactRows: {
    method: 'GET',
    path: '/v1/artifacts/{artifact}/data',
    query: ['filter', 'since', 'until', 'sort', 'limit', 'cursor', 'fields'],
  },
  writeArtifactRows: { method: 'POST', path: '/v1/artifacts/{artifact}/data/rows', query: [] },
  listRows: {
    method: 'GET',
    path: '/v1/data',
    query: [
      'dataset',
      'collection',
      'filter',
      'since',
      'until',
      'sort',
      'limit',
      'cursor',
      'fields',
    ],
  },
  queryData: { method: 'POST', path: '/v1/data/query', query: [] },
  getSchema: {
    method: 'GET',
    path: '/v1/schema',
    query: ['series', 'tags', 'artifact', 'compare', 'since', 'workspace'],
  },
  defineCollection: { method: 'PUT', path: '/v1/schema', query: [] },
  listEntries: {
    method: 'GET',
    path: '/v1/collections/{collection}/entries',
    query: ['workspace', 'filter', 'search', 'sort', 'direction', 'page', 'limit'],
    conditionalRead: true,
  },
  createEntries: { method: 'POST', path: '/v1/collections/{collection}/entries', query: [] },
  useSecret: {
    method: 'POST',
    path: '/v1/collections/{collection}/entries/{entry}/fields/{field}/use',
    query: [],
  },
  listTemplates: {
    method: 'GET',
    path: '/v1/templates',
    query: [
      'request',
      'scope',
      'kind',
      'sort',
      'limit',
      'jobs',
      'audience',
      'needs',
      'cost',
      'tier',
      'mine',
    ],
  },
  saveTemplate: { method: 'POST', path: '/v1/templates', query: [] },
  getTemplate: { method: 'GET', path: '/v1/templates/{slug}', query: ['version'] },
  getTemplateHistory: { method: 'GET', path: '/v1/templates/{slug}/history', query: [] },
  getTemplateFeedback: { method: 'GET', path: '/v1/templates/{slug}/feedback', query: [] },
  actOnTemplate: { method: 'POST', path: '/v1/templates/{slug}/actions', query: [] },
  releaseTemplate: { method: 'POST', path: '/v1/templates/{slug}/release', query: [] },
  listProjects: { method: 'GET', path: '/v1/projects', query: ['workspace'] },
  createProject: { method: 'POST', path: '/v1/projects', query: [] },
  getProject: { method: 'GET', path: '/v1/projects/{project}', query: ['workspace'] },
  updateProject: { method: 'PATCH', path: '/v1/projects/{project}', query: [] },
  deleteProject: {
    method: 'DELETE',
    path: '/v1/projects/{project}',
    query: [],
    confirm: 'project',
  },
  addProjectArtifacts: { method: 'POST', path: '/v1/projects/{project}/artifacts', query: [] },
  removeProjectArtifact: {
    method: 'DELETE',
    path: '/v1/projects/{project}/artifacts/{remove}',
    query: [],
  },
  shareArtifact: { method: 'POST', path: '/v1/artifacts/{artifact}/shares', query: [] },
  shareProject: { method: 'POST', path: '/v1/projects/{project}/shares', query: [] },
  shareWorkspace: { method: 'POST', path: '/v1/workspace/shares', query: [] },
  listComments: {
    method: 'GET',
    path: '/v1/artifacts/{artifact}/comments',
    query: ['status', 'page', 'limit', 'cursor'],
  },
  respondToComments: {
    method: 'POST',
    path: '/v1/artifacts/{artifact}/comments/responses',
    query: [],
  },
  getCommentScreenshot: {
    method: 'GET',
    path: '/v1/artifacts/{artifact}/comments/screenshots/{screenshot}',
    query: [],
  },
  listMentions: { method: 'GET', path: '/v1/mentions', query: ['artifact', 'limit', 'cursor'] },
  listSignatureRequests: { method: 'GET', path: '/v1/signatures', query: ['artifact'] },
  requestSignatures: { method: 'POST', path: '/v1/signatures', query: [] },
  getSignatureRequest: { method: 'GET', path: '/v1/signatures/{request}', query: [] },
  remindSigner: { method: 'POST', path: '/v1/signatures/{request}/remind', query: [] },
  withdrawSignatureRequest: {
    method: 'POST',
    path: '/v1/signatures/{request}/withdraw',
    query: [],
  },
} as const satisfies Record<string, Operation>

export class AccountResource {
  constructor(protected readonly client: Core) {}

  /** Who this key publishes as */
  whoami(
    params?: Params<operations['whoami']>,
    options?: RequestOptions,
  ): Promise<Result<operations['whoami']>> {
    return this.client.call(OPERATIONS.whoami, params, options) as Promise<
      Result<operations['whoami']>
    >
  }

  /** How the operations fit together */
  help(
    params?: Params<operations['getHelp']>,
    options?: RequestOptions,
  ): Promise<Result<operations['getHelp']>> {
    return this.client.call(OPERATIONS.getHelp, params, options) as Promise<
      Result<operations['getHelp']>
    >
  }
}

export class ArtifactsResource {
  constructor(protected readonly client: Core) {}

  /** List your artifacts, newest first */
  list(
    params?: Params<operations['listArtifacts']>,
    options?: RequestOptions,
  ): Promise<Result<operations['listArtifacts']>> {
    return this.client.call(OPERATIONS.listArtifacts, params, options) as Promise<
      Result<operations['listArtifacts']>
    >
  }

  /** Publish an artifact, or a new version of one */
  publish(
    params: Params<operations['publishArtifact']>,
    options?: RequestOptions,
  ): Promise<Result<operations['publishArtifact']>> {
    return this.client.call(OPERATIONS.publishArtifact, params, options) as Promise<
      Result<operations['publishArtifact']>
    >
  }

  /** One artifact: its versions, published version and declaration */
  get(
    params: Params<operations['getArtifact']>,
    options?: RequestOptions,
  ): Promise<Result<operations['getArtifact']>> {
    return this.client.call(OPERATIONS.getArtifact, params, options) as Promise<
      Result<operations['getArtifact']>
    >
  }

  /** Change visibility, gallery label, live phase or submission email */
  update(
    params: Params<operations['updateArtifact']>,
    options?: RequestOptions,
  ): Promise<Result<operations['updateArtifact']>> {
    return this.client.call(OPERATIONS.updateArtifact, params, options) as Promise<
      Result<operations['updateArtifact']>
    >
  }

  /** Delete an artifact with every version, permanently */
  delete(
    params: Omit<Params<operations['deleteArtifact']>, 'confirm'>,
    options?: RequestOptions,
  ): Promise<Result<operations['deleteArtifact']>> {
    return this.client.call(OPERATIONS.deleteArtifact, params, options) as Promise<
      Result<operations['deleteArtifact']>
    >
  }

  /** Read one file of a version as text (default: the published index.html) */
  readFile(
    params: Params<operations['readArtifactFile']>,
    options?: RequestOptions,
  ): Promise<Result<operations['readArtifactFile']>> {
    return this.client.call(OPERATIONS.readArtifactFile, params, options) as Promise<
      Result<operations['readArtifactFile']>
    >
  }

  /** A ten-minute viewer URL for an artifact, private included */
  open(
    params: Params<operations['openArtifact']>,
    options?: RequestOptions,
  ): Promise<Result<operations['openArtifact']>> {
    return this.client.call(OPERATIONS.openArtifact, params, options) as Promise<
      Result<operations['openArtifact']>
    >
  }

  /** Serve an existing version again */
  serveVersion(
    params: Params<operations['serveVersion']>,
    options?: RequestOptions,
  ): Promise<Result<operations['serveVersion']>> {
    return this.client.call(OPERATIONS.serveVersion, params, options) as Promise<
      Result<operations['serveVersion']>
    >
  }
}

export class LiveResource {
  constructor(protected readonly client: Core) {}

  /** Turn an artifact's live room on */
  start(
    params: Params<operations['startLiveRoom']>,
    options?: RequestOptions,
  ): Promise<Result<operations['startLiveRoom']>> {
    return this.client.call(OPERATIONS.startLiveRoom, params, options) as Promise<
      Result<operations['startLiveRoom']>
    >
  }

  /** Turn an artifact's live room off, disconnecting every visitor */
  stop(
    params: Params<operations['stopLiveRoom']>,
    options?: RequestOptions,
  ): Promise<Result<operations['stopLiveRoom']>> {
    return this.client.call(OPERATIONS.stopLiveRoom, params, options) as Promise<
      Result<operations['stopLiveRoom']>
    >
  }
}

export class UploadsResource {
  constructor(protected readonly client: Core) {}

  /** Stage big files for a publish; PUT each to its URL */
  stage(
    params: Params<operations['stageUploads']>,
    options?: RequestOptions,
  ): Promise<Result<operations['stageUploads']>> {
    return this.client.call(OPERATIONS.stageUploads, params, options) as Promise<
      Result<operations['stageUploads']>
    >
  }
}

export class DataResource {
  constructor(protected readonly client: Core) {}

  /** Rows visitors submitted to one artifact, newest first */
  listArtifactRows(
    params: Params<operations['listArtifactRows']>,
    options?: RequestOptions,
  ): Promise<Result<operations['listArtifactRows']>> {
    return this.client.call(OPERATIONS.listArtifactRows, params, options) as Promise<
      Result<operations['listArtifactRows']>
    >
  }

  /** Write rows into an artifact you may edit */
  writeArtifactRows(
    params: Params<operations['writeArtifactRows']>,
    options?: RequestOptions,
  ): Promise<Result<operations['writeArtifactRows']>> {
    return this.client.call(OPERATIONS.writeArtifactRows, params, options) as Promise<
      Result<operations['writeArtifactRows']>
    >
  }

  /** Rows submitted to a dataset or a gallery label */
  listRows(
    params?: Params<operations['listRows']>,
    options?: RequestOptions,
  ): Promise<Result<operations['listRows']>> {
    return this.client.call(OPERATIONS.listRows, params, options) as Promise<
      Result<operations['listRows']>
    >
  }

  /** Aggregate what was collected: numbers, never rows */
  query(
    params?: Params<operations['queryData']>,
    options?: RequestOptions,
  ): Promise<Result<operations['queryData']>> {
    return this.client.call(OPERATIONS.queryData, params, options) as Promise<
      Result<operations['queryData']>
    >
  }
}

export class SchemaResource {
  constructor(protected readonly client: Core) {}

  /** The data catalog: datasets and content collections, or a comparison */
  get(
    params?: Params<operations['getSchema']>,
    options?: RequestOptions,
  ): Promise<Result<operations['getSchema']>> {
    return this.client.call(OPERATIONS.getSchema, params, options) as Promise<
      Result<operations['getSchema']>
    >
  }

  /** Create or replace a content collection */
  defineCollection(
    params?: Params<operations['defineCollection']>,
    options?: RequestOptions,
  ): Promise<Result<operations['defineCollection']>> {
    return this.client.call(OPERATIONS.defineCollection, params, options) as Promise<
      Result<operations['defineCollection']>
    >
  }
}

export class EntriesResource {
  constructor(protected readonly client: Core) {}

  /** One page of a content collection's entries */
  list(
    params: Params<operations['listEntries']>,
    options?: RequestOptions,
  ): Promise<Result<operations['listEntries']>> {
    return this.client.call(OPERATIONS.listEntries, params, options) as Promise<
      Result<operations['listEntries']>
    >
  }

  /** Create one entry, or a batch */
  create(
    params: Params<operations['createEntries']>,
    options?: RequestOptions,
  ): Promise<Result<operations['createEntries']>> {
    return this.client.call(OPERATIONS.createEntries, params, options) as Promise<
      Result<operations['createEntries']>
    >
  }
}

export class SecretsResource {
  constructor(protected readonly client: Core) {}

  /** Call an approved API with a stored secret you cannot read (workspace keys) */
  use(
    params: Params<operations['useSecret']>,
    options?: RequestOptions,
  ): Promise<Result<operations['useSecret']>> {
    return this.client.call(OPERATIONS.useSecret, params, options) as Promise<
      Result<operations['useSecret']>
    >
  }
}

export class TemplatesResource {
  constructor(protected readonly client: Core) {}

  /** Find, rank or list templates */
  list(
    params?: Params<operations['listTemplates']>,
    options?: RequestOptions,
  ): Promise<Result<operations['listTemplates']>> {
    return this.client.call(OPERATIONS.listTemplates, params, options) as Promise<
      Result<operations['listTemplates']>
    >
  }

  /** Create or revise a template draft */
  save(
    params: Params<operations['saveTemplate']>,
    options?: RequestOptions,
  ): Promise<Result<operations['saveTemplate']>> {
    return this.client.call(OPERATIONS.saveTemplate, params, options) as Promise<
      Result<operations['saveTemplate']>
    >
  }

  /** One template in full, with its install prompt */
  get(
    params: Params<operations['getTemplate']>,
    options?: RequestOptions,
  ): Promise<Result<operations['getTemplate']>> {
    return this.client.call(OPERATIONS.getTemplate, params, options) as Promise<
      Result<operations['getTemplate']>
    >
  }

  /** A template's changelog */
  getHistory(
    params: Params<operations['getTemplateHistory']>,
    options?: RequestOptions,
  ): Promise<Result<operations['getTemplateHistory']>> {
    return this.client.call(OPERATIONS.getTemplateHistory, params, options) as Promise<
      Result<operations['getTemplateHistory']>
    >
  }

  /** Comments on a template's artifacts, as themes */
  getFeedback(
    params: Params<operations['getTemplateFeedback']>,
    options?: RequestOptions,
  ): Promise<Result<operations['getTemplateFeedback']>> {
    return this.client.call(OPERATIONS.getTemplateFeedback, params, options) as Promise<
      Result<operations['getTemplateFeedback']>
    >
  }

  /** Install, uninstall, rate, report, roll back or request verification */
  act(
    params: Params<operations['actOnTemplate']>,
    options?: RequestOptions,
  ): Promise<Result<operations['actOnTemplate']>> {
    return this.client.call(OPERATIONS.actOnTemplate, params, options) as Promise<
      Result<operations['actOnTemplate']>
    >
  }

  /** Release one version of your template */
  release(
    params: Params<operations['releaseTemplate']>,
    options?: RequestOptions,
  ): Promise<Result<operations['releaseTemplate']>> {
    return this.client.call(OPERATIONS.releaseTemplate, params, options) as Promise<
      Result<operations['releaseTemplate']>
    >
  }
}

export class ProjectsResource {
  constructor(protected readonly client: Core) {}

  /** Your projects */
  list(
    params?: Params<operations['listProjects']>,
    options?: RequestOptions,
  ): Promise<Result<operations['listProjects']>> {
    return this.client.call(OPERATIONS.listProjects, params, options) as Promise<
      Result<operations['listProjects']>
    >
  }

  /** Create a project, optionally seeded with artifacts */
  create(
    params?: Params<operations['createProject']>,
    options?: RequestOptions,
  ): Promise<Result<operations['createProject']>> {
    return this.client.call(OPERATIONS.createProject, params, options) as Promise<
      Result<operations['createProject']>
    >
  }

  /** One project and its items */
  get(
    params: Params<operations['getProject']>,
    options?: RequestOptions,
  ): Promise<Result<operations['getProject']>> {
    return this.client.call(OPERATIONS.getProject, params, options) as Promise<
      Result<operations['getProject']>
    >
  }

  /** Rename, set visibility, reorder, move, fold groups or set a rule */
  update(
    params: Params<operations['updateProject']>,
    options?: RequestOptions,
  ): Promise<Result<operations['updateProject']>> {
    return this.client.call(OPERATIONS.updateProject, params, options) as Promise<
      Result<operations['updateProject']>
    >
  }

  /** Delete a project; its artifacts stay */
  delete(
    params: Omit<Params<operations['deleteProject']>, 'confirm'>,
    options?: RequestOptions,
  ): Promise<Result<operations['deleteProject']>> {
    return this.client.call(OPERATIONS.deleteProject, params, options) as Promise<
      Result<operations['deleteProject']>
    >
  }

  /** Add artifacts to a project */
  addArtifacts(
    params: Params<operations['addProjectArtifacts']>,
    options?: RequestOptions,
  ): Promise<Result<operations['addProjectArtifacts']>> {
    return this.client.call(OPERATIONS.addProjectArtifacts, params, options) as Promise<
      Result<operations['addProjectArtifacts']>
    >
  }

  /** Remove one artifact (or item) from a project */
  removeArtifact(
    params: Params<operations['removeProjectArtifact']>,
    options?: RequestOptions,
  ): Promise<Result<operations['removeProjectArtifact']>> {
    return this.client.call(OPERATIONS.removeProjectArtifact, params, options) as Promise<
      Result<operations['removeProjectArtifact']>
    >
  }
}

export class SharesResource {
  constructor(protected readonly client: Core) {}

  /** Give named people access to an artifact */
  addToArtifact(
    params: Params<operations['shareArtifact']>,
    options?: RequestOptions,
  ): Promise<Result<operations['shareArtifact']>> {
    return this.client.call(OPERATIONS.shareArtifact, params, options) as Promise<
      Result<operations['shareArtifact']>
    >
  }

  /** Give named people access to a project */
  addToProject(
    params: Params<operations['shareProject']>,
    options?: RequestOptions,
  ): Promise<Result<operations['shareProject']>> {
    return this.client.call(OPERATIONS.shareProject, params, options) as Promise<
      Result<operations['shareProject']>
    >
  }

  /** Invite editors to a workspace (returns accept links) */
  addToWorkspace(
    params: Params<operations['shareWorkspace']>,
    options?: RequestOptions,
  ): Promise<Result<operations['shareWorkspace']>> {
    return this.client.call(OPERATIONS.shareWorkspace, params, options) as Promise<
      Result<operations['shareWorkspace']>
    >
  }
}

export class CommentsResource {
  constructor(protected readonly client: Core) {}

  /** Comment threads on an artifact, newest first */
  list(
    params: Params<operations['listComments']>,
    options?: RequestOptions,
  ): Promise<Result<operations['listComments']>> {
    return this.client.call(OPERATIONS.listComments, params, options) as Promise<
      Result<operations['listComments']>
    >
  }

  /** Reply to and/or resolve threads, one outcome each */
  respond(
    params: Params<operations['respondToComments']>,
    options?: RequestOptions,
  ): Promise<Result<operations['respondToComments']>> {
    return this.client.call(OPERATIONS.respondToComments, params, options) as Promise<
      Result<operations['respondToComments']>
    >
  }

  /** One message's screenshot, base64 in `image` */
  getScreenshot(
    params: Params<operations['getCommentScreenshot']>,
    options?: RequestOptions,
  ): Promise<Result<operations['getCommentScreenshot']>> {
    return this.client.call(OPERATIONS.getCommentScreenshot, params, options) as Promise<
      Result<operations['getCommentScreenshot']>
    >
  }
}

export class MentionsResource {
  constructor(protected readonly client: Core) {}

  /** Where people @mentioned you; listing marks them seen */
  list(
    params?: Params<operations['listMentions']>,
    options?: RequestOptions,
  ): Promise<Result<operations['listMentions']>> {
    return this.client.call(OPERATIONS.listMentions, params, options) as Promise<
      Result<operations['listMentions']>
    >
  }
}

export class SignaturesResource {
  constructor(protected readonly client: Core) {}

  /** An artifact's signature requests, newest first */
  list(
    params?: Params<operations['listSignatureRequests']>,
    options?: RequestOptions,
  ): Promise<Result<operations['listSignatureRequests']>> {
    return this.client.call(OPERATIONS.listSignatureRequests, params, options) as Promise<
      Result<operations['listSignatureRequests']>
    >
  }

  /** Ask named people to sign one version of an artifact */
  request(
    params?: Params<operations['requestSignatures']>,
    options?: RequestOptions,
  ): Promise<Result<operations['requestSignatures']>> {
    return this.client.call(OPERATIONS.requestSignatures, params, options) as Promise<
      Result<operations['requestSignatures']>
    >
  }

  /** One signature request and its signers */
  get(
    params: Params<operations['getSignatureRequest']>,
    options?: RequestOptions,
  ): Promise<Result<operations['getSignatureRequest']>> {
    return this.client.call(OPERATIONS.getSignatureRequest, params, options) as Promise<
      Result<operations['getSignatureRequest']>
    >
  }

  /** Email a signer their link again */
  remind(
    params: Params<operations['remindSigner']>,
    options?: RequestOptions,
  ): Promise<Result<operations['remindSigner']>> {
    return this.client.call(OPERATIONS.remindSigner, params, options) as Promise<
      Result<operations['remindSigner']>
    >
  }

  /** Close an open signature request */
  withdraw(
    params: Params<operations['withdrawSignatureRequest']>,
    options?: RequestOptions,
  ): Promise<Result<operations['withdrawSignatureRequest']>> {
    return this.client.call(OPERATIONS.withdrawSignatureRequest, params, options) as Promise<
      Result<operations['withdrawSignatureRequest']>
    >
  }
}

export class Resources extends Core {
  readonly account = new AccountResource(this)
  readonly artifacts = new ArtifactsResource(this)
  readonly live = new LiveResource(this)
  readonly uploads = new UploadsResource(this)
  readonly data = new DataResource(this)
  readonly schema = new SchemaResource(this)
  readonly entries = new EntriesResource(this)
  readonly secrets = new SecretsResource(this)
  readonly templates = new TemplatesResource(this)
  readonly projects = new ProjectsResource(this)
  readonly shares = new SharesResource(this)
  readonly comments = new CommentsResource(this)
  readonly mentions = new MentionsResource(this)
  readonly signatures = new SignaturesResource(this)
}
