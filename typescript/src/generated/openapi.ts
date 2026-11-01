// Generated from sdks/openapi.json (sha256 0b6844650fbfd985663c3a983b3e634b1533abfc4ca9da502bfa41fca758f8f0). Do not edit: run `pnpm sdk:generate`.
export interface paths {
  '/v1/whoami': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    /**
     * Who this key publishes as
     * @description Who this key publishes as: the workspace `handle`, `email`, `agent` name and `scope` (the artifacts it may change: its own, and those it is named Editor on), plus `liveRooms` where live rooms run (the limit and who holds one). Useful to confirm where a publish lands, or why an artifact answers `not_found`; no other tool needs it.
     */
    get: operations['whoami']
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/v1/help': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    /**
     * How the operations fit together
     * @description Plain-text notes for when it is unclear which tool, data store or argument shape does a job. Topics: `tools` (a line per tool), `data` (which store a page needs and how the page writes to it), `templates` (finding, building from, drafting, releasing), `collections` (content models and field types), `projects` (creating, ordering, sharing, rules), `batch` (what each tool takes in one call). Without `topic`: the full topic list, which names two more reached from results. Answers `{topic, text}`; not needed when a tool’s own description answers the question.
     */
    get: operations['getHelp']
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/v1/artifacts': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    /**
     * List your artifacts, newest first
     * @description Without `artifact`: your artifacts, newest first, with URLs and `live`. With `artifact`: its versions, which is published, their paths, and `declaration` (the published policy). Add `path` or `version` to read that file as text (default: published index.html); non-text or over 300,000 bytes: refused. `open: true` (with `artifact`, optional `version`) returns `url` and `expiresAt`: load `url` to see the artifact as a viewer, private included, for 10 minutes; visibility is unchanged, the URL opens only that artifact, 60/key/hour (`rate_limited`). Changing what an artifact serves, or who can open it, is super_artifact_set.
     */
    get: operations['listArtifacts']
    put?: never
    /**
     * Publish an artifact, or a new version of one
     * @description Publish a page at a stable URL; the same slug adds a new version, which the URL serves at once. Earlier versions stay and can be served again; nothing that existed before the call is deleted. Always give the person the url from the result, even on updates. Send `html`, or `values` for a template that carries a runtime, not both. Without `policy` a form, input or saved state stores nothing; CMS rows a page edits go in `policy.collections`. When retained storage is full it refuses with `plan_limit` and deletes nothing. A template becomes everybody’s through a release, not a publish.
     */
    post: operations['publishArtifact']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/v1/artifacts/{artifact}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    /**
     * One artifact: its versions, published version and declaration
     * @description Without `artifact`: your artifacts, newest first, with URLs and `live`. With `artifact`: its versions, which is published, their paths, and `declaration` (the published policy). Add `path` or `version` to read that file as text (default: published index.html); non-text or over 300,000 bytes: refused. `open: true` (with `artifact`, optional `version`) returns `url` and `expiresAt`: load `url` to see the artifact as a viewer, private included, for 10 minutes; visibility is unchanged, the URL opens only that artifact, 60/key/hour (`rate_limited`). Changing what an artifact serves, or who can open it, is super_artifact_set.
     */
    get: operations['getArtifact']
    put?: never
    post?: never
    /**
     * Delete an artifact with every version, permanently
     * @description Change one artifact. `version` serves an existing version (a pointer move; nothing rebuilt or deleted). `live` turns its live room on or off; off disconnects every visitor, and Free has one room at a time. `notifyOnSubmission` emails you for each new data submission (default off; edits send nothing; no answers in the mail). `phase` sets the live room’s phase. `visibility` widens or narrows who can open it; narrowing voids every viewer grant already issued, so each viewer is checked again. `collection` sets its gallery grouping label. `delete` removes the artifact with every version, share link and response, permanently; it needs `confirm: true` and goes alone. Fields apply in that order, and a refusal part-way names the ones already `applied`. Publishing a new version is super_publish.
     */
    delete: operations['deleteArtifact']
    options?: never
    head?: never
    /**
     * Change visibility, gallery label, live phase or submission email
     * @description Change one artifact. `version` serves an existing version (a pointer move; nothing rebuilt or deleted). `live` turns its live room on or off; off disconnects every visitor, and Free has one room at a time. `notifyOnSubmission` emails you for each new data submission (default off; edits send nothing; no answers in the mail). `phase` sets the live room’s phase. `visibility` widens or narrows who can open it; narrowing voids every viewer grant already issued, so each viewer is checked again. `collection` sets its gallery grouping label. `delete` removes the artifact with every version, share link and response, permanently; it needs `confirm: true` and goes alone. Fields apply in that order, and a refusal part-way names the ones already `applied`. Publishing a new version is super_publish.
     */
    patch: operations['updateArtifact']
    trace?: never
  }
  '/v1/artifacts/{artifact}/file': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    /**
     * Read one file of a version as text (default: the published index.html)
     * @description Without `artifact`: your artifacts, newest first, with URLs and `live`. With `artifact`: its versions, which is published, their paths, and `declaration` (the published policy). Add `path` or `version` to read that file as text (default: published index.html); non-text or over 300,000 bytes: refused. `open: true` (with `artifact`, optional `version`) returns `url` and `expiresAt`: load `url` to see the artifact as a viewer, private included, for 10 minutes; visibility is unchanged, the URL opens only that artifact, 60/key/hour (`rate_limited`). Changing what an artifact serves, or who can open it, is super_artifact_set.
     */
    get: operations['readArtifactFile']
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/v1/artifacts/{artifact}/open': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * A ten-minute viewer URL for an artifact, private included
     * @description Without `artifact`: your artifacts, newest first, with URLs and `live`. With `artifact`: its versions, which is published, their paths, and `declaration` (the published policy). Add `path` or `version` to read that file as text (default: published index.html); non-text or over 300,000 bytes: refused. `open: true` (with `artifact`, optional `version`) returns `url` and `expiresAt`: load `url` to see the artifact as a viewer, private included, for 10 minutes; visibility is unchanged, the URL opens only that artifact, 60/key/hour (`rate_limited`). Changing what an artifact serves, or who can open it, is super_artifact_set.
     */
    post: operations['openArtifact']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/v1/artifacts/{artifact}/versions/{version}/serve': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Serve an existing version again
     * @description Change one artifact. `version` serves an existing version (a pointer move; nothing rebuilt or deleted). `live` turns its live room on or off; off disconnects every visitor, and Free has one room at a time. `notifyOnSubmission` emails you for each new data submission (default off; edits send nothing; no answers in the mail). `phase` sets the live room’s phase. `visibility` widens or narrows who can open it; narrowing voids every viewer grant already issued, so each viewer is checked again. `collection` sets its gallery grouping label. `delete` removes the artifact with every version, share link and response, permanently; it needs `confirm: true` and goes alone. Fields apply in that order, and a refusal part-way names the ones already `applied`. Publishing a new version is super_publish.
     */
    post: operations['serveVersion']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/v1/artifacts/{artifact}/live': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Turn an artifact's live room on
     * @description Change one artifact. `version` serves an existing version (a pointer move; nothing rebuilt or deleted). `live` turns its live room on or off; off disconnects every visitor, and Free has one room at a time. `notifyOnSubmission` emails you for each new data submission (default off; edits send nothing; no answers in the mail). `phase` sets the live room’s phase. `visibility` widens or narrows who can open it; narrowing voids every viewer grant already issued, so each viewer is checked again. `collection` sets its gallery grouping label. `delete` removes the artifact with every version, share link and response, permanently; it needs `confirm: true` and goes alone. Fields apply in that order, and a refusal part-way names the ones already `applied`. Publishing a new version is super_publish.
     */
    post: operations['startLiveRoom']
    /**
     * Turn an artifact's live room off, disconnecting every visitor
     * @description Change one artifact. `version` serves an existing version (a pointer move; nothing rebuilt or deleted). `live` turns its live room on or off; off disconnects every visitor, and Free has one room at a time. `notifyOnSubmission` emails you for each new data submission (default off; edits send nothing; no answers in the mail). `phase` sets the live room’s phase. `visibility` widens or narrows who can open it; narrowing voids every viewer grant already issued, so each viewer is checked again. `collection` sets its gallery grouping label. `delete` removes the artifact with every version, share link and response, permanently; it needs `confirm: true` and goes alone. Fields apply in that order, and a refusal part-way names the ones already `applied`. Publishing a new version is super_publish.
     */
    delete: operations['stopLiveRoom']
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/v1/uploads': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Stage big files for a publish; PUT each to its URL
     * @description Stage images, video or big files for a publish without sending their bytes in a call. Declare each file’s `path` and exact `bytes`; the result carries an `uploadId` and one `url` per file. PUT each file to its URL (`curl -T`, no credentials), then super_publish with `uploads`. Not index.html: that is `html`; small assets can ride inline as the publish’s `files`. Same limits as `files`; a staged set expires after 30 minutes, and at most 5 wait unpublished at once.
     */
    post: operations['stageUploads']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/v1/artifacts/{artifact}/data': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    /**
     * Rows visitors submitted to one artifact, newest first
     * @description The rows visitors submitted to your artifacts, newest first, with each version's field schema; paged by `cursor`. Address exactly one: `artifact`; `dataset` (a catalog key; one shared by several artifacts is `ambiguous_dataset`); or `collection`, the gallery grouping label set at publish, not a content collection (≤20 artifacts over one window, kept per artifact, no `filter`). Entries of a content collection are super_entries; totals and averages are a query, not a read.
     */
    get: operations['listArtifactRows']
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/v1/artifacts/{artifact}/data/rows': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Write rows into an artifact you may edit
     * @description Write rows into an artifact this key may edit, through the validation and stream rules a page write gets; each row is attributed "<agent> (agent)". `rows` creates in `stream`. `ops` [{op: create|replace|delete, id, row, stream}] replaces or deletes only rows this agent wrote (writes: upsert); a deleted row cannot be restored by any tool. ≤50 a call; `atomic`: all or none, otherwise a partial batch answers `complete: false`. Visitor rows are never changed here; entries of a content collection are super_entries.
     */
    post: operations['writeArtifactRows']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/v1/data': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    /**
     * Rows submitted to a dataset or a gallery label
     * @description The rows visitors submitted to your artifacts, newest first, with each version's field schema; paged by `cursor`. Address exactly one: `artifact`; `dataset` (a catalog key; one shared by several artifacts is `ambiguous_dataset`); or `collection`, the gallery grouping label set at publish, not a content collection (≤20 artifacts over one window, kept per artifact, no `filter`). Entries of a content collection are super_entries; totals and averages are a query, not a read.
     */
    get: operations['listRows']
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/v1/data/query': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Aggregate what was collected: numbers, never rows
     * @description Numbers over what was collected, never rows (rows are super_data). Aggregate `measures` across the datasets in `scope`; datasets combine on the same measure in one base unit, results in the declared `unit`. Names come from the catalog; an unknown one errors with near misses. The answer has one row per `group_by` key (or one row) with a column per measure and `compute`, the datasets used and any skipped, and `truncated` when `limit` cut it. Or send `distributions` for one artifact: counts, per-version rates and per-field distributions (free text: answer rate and length only). A call with neither is `invalid_query`.
     */
    post: operations['queryData']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/v1/schema': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    /**
     * The data catalog: datasets and content collections, or a comparison
     * @description The data catalog, without rows. Read (the default): `datasets` your artifacts declared, with fields, units, measures and `since`/`deprecated` versions, and this workspace's content `collections`, with fields, rules and entry counts. `compare` (alone): two to ten artifacts' newest fields side by side, every type, unit and measure conflict named. `define` creates a content collection, or replaces the one with that `key` outright, name, display field and every field; a field left out is gone from the model, and a collection an artifact declared is refused with `conflict`. Refusals name field, rule and fix. Rows an artifact collected are super_data.
     */
    get: operations['getSchema']
    /**
     * Create or replace a content collection
     * @description The data catalog, without rows. Read (the default): `datasets` your artifacts declared, with fields, units, measures and `since`/`deprecated` versions, and this workspace's content `collections`, with fields, rules and entry counts. `compare` (alone): two to ten artifacts' newest fields side by side, every type, unit and measure conflict named. `define` creates a content collection, or replaces the one with that `key` outright, name, display field and every field; a field left out is gone from the model, and a collection an artifact declared is refused with `conflict`. Refusals name field, rule and fix. Rows an artifact collected are super_data.
     */
    put: operations['defineCollection']
    post?: never
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/v1/collections/{collection}/entries': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    /**
     * One page of a content collection's entries
     * @description Entries of a workspace content collection (a model defined in the catalog), not rows an artifact collected. With `values`: create one entry (an object) or up to 50 (an array, one outcome per row); values are coerced to declared types, undeclared fields are refused by name, and nothing existing is updated or deleted. Without: read one page, filtered and sorted in the database; references resolve to labels, sensitive fields read as answered-or-not. Rows visitors submitted are super_data.
     */
    get: operations['listEntries']
    put?: never
    /**
     * Create one entry, or a batch
     * @description Entries of a workspace content collection (a model defined in the catalog), not rows an artifact collected. With `values`: create one entry (an object) or up to 50 (an array, one outcome per row); values are coerced to declared types, undeclared fields are refused by name, and nothing existing is updated or deleted. Without: read one page, filtered and sorted in the database; references resolve to labels, sensitive fields read as answered-or-not. Rows visitors submitted are super_data.
     */
    post: operations['createEntries']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/v1/collections/{collection}/entries/{entry}/fields/{field}/use': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Call an approved API with a stored secret you cannot read (workspace keys)
     * @description Make one HTTPS request with a `pii: secret` value from a content collection entry. The platform puts the value into one header and calls the one host a person approved; you get back status, headers and body, already searched for the value. You never see the value: it is not in this input, not in any result, and a response that echoes it is withheld whole (`secret_echoed`). The first request for a field and host answers `approval_required` with `approvalUrl`: give the person that link, and once they approve, repeat the same request. A grant expires, caps its uses and can be revoked; every use is logged. Secrets are written with super_entries.
     */
    post: operations['useSecret']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/v1/templates': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    /**
     * Find, rank or list templates
     * @description With `request`: rank installed templates by content similarity; matches carry `band` (high: build from it; possible: judge it), `why` and unscored stats. `scope: marketplace`: released public templates, ranked by `request` or else the top by `sort`; `sort`, `limit` and the facets apply only here. Neither: the installed list. `slug`: one template in full, with its `installPrompt`; `history`: its changelog; `feedback`: its artifacts' comments as themes. `mine`: your published templates, with counts. Reading only: installing, rating and rolling back are super_template_action.
     */
    get: operations['listTemplates']
    put?: never
    /**
     * Create or revise a template draft
     * @description Write a template draft only you can publish from. Without `expectedVersion` it creates (refused if the slug exists); with it, it revises the head (refused if the head moved past it), and a revision that changes nothing cuts no version. A `json` slot needs `schema`. Runtime `files` (≤512 KiB decoded) need a `json` slot and an index.html with one `<script id="sa-template-values" type="application/json">`. Others build from it only once super_release_template releases it; a revision never changes a released version.
     */
    post: operations['saveTemplate']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/v1/templates/{slug}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    /**
     * One template in full, with its install prompt
     * @description With `request`: rank installed templates by content similarity; matches carry `band` (high: build from it; possible: judge it), `why` and unscored stats. `scope: marketplace`: released public templates, ranked by `request` or else the top by `sort`; `sort`, `limit` and the facets apply only here. Neither: the installed list. `slug`: one template in full, with its `installPrompt`; `history`: its changelog; `feedback`: its artifacts' comments as themes. `mine`: your published templates, with counts. Reading only: installing, rating and rolling back are super_template_action.
     */
    get: operations['getTemplate']
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/v1/templates/{slug}/history': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    /**
     * A template's changelog
     * @description With `request`: rank installed templates by content similarity; matches carry `band` (high: build from it; possible: judge it), `why` and unscored stats. `scope: marketplace`: released public templates, ranked by `request` or else the top by `sort`; `sort`, `limit` and the facets apply only here. Neither: the installed list. `slug`: one template in full, with its `installPrompt`; `history`: its changelog; `feedback`: its artifacts' comments as themes. `mine`: your published templates, with counts. Reading only: installing, rating and rolling back are super_template_action.
     */
    get: operations['getTemplateHistory']
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/v1/templates/{slug}/feedback': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    /**
     * Comments on a template's artifacts, as themes
     * @description With `request`: rank installed templates by content similarity; matches carry `band` (high: build from it; possible: judge it), `why` and unscored stats. `scope: marketplace`: released public templates, ranked by `request` or else the top by `sort`; `sort`, `limit` and the facets apply only here. Neither: the installed list. `slug`: one template in full, with its `installPrompt`; `history`: its changelog; `feedback`: its artifacts' comments as themes. `mine`: your published templates, with counts. Reading only: installing, rating and rolling back are super_template_action.
     */
    get: operations['getTemplateFeedback']
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/v1/templates/{slug}/actions': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Install, uninstall, rate, report, roll back or request verification
     * @description Act on one template; nothing here deletes a template, a version or a built artifact. `install`/`uninstall`: this workspace's installed set (uninstall removes only the install; built artifacts keep working); `install` returns its build prompt as `nextStep`. `rate`: the person's 1–5 `stars` on an installed template not yours (`cannot_rate_own`, `not_installed`, `rate_limited`); counts once this workspace built from it. `report`: `kind` and a `reason` (≤1000 chars) for a moderator; one per account; enough reports hide it. `rollback`: restore `version` as a new version, unless the runtime changed. `request_verification`: a moderator checks your released `version`; 3 per 30 days. Finding and reading templates is super_templates.
     */
    post: operations['actOnTemplate']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/v1/templates/{slug}/release': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Release one version of your template
     * @description Release one version of your template so others can build from it, live at once to the reach `visibility` sets; the result names its trust `tier` (Official, Verified or Community). Forward only (`release_moves_backwards`): earlier versions stay, and nothing is deleted. A private demo needs `demoConsent: true`. A runtime, prompt, parts or data change leaves a Verified badge behind. Public: account 7 days old (`publisher_too_new`), 10/day, 3/template/hour (`rate_limited`), 20 templates (`too_many_templates`), no tier words (`reserved_wording`), no credential (`secret_in_template`), paid plan (`plan_required`). Writing the draft is super_template_save.
     */
    post: operations['releaseTemplate']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/v1/projects': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    /**
     * Your projects
     * @description A project is an ordered set of your artifacts shown one at a time at /s/{slug}, with its own audience and share list. No `project`: `title` creates one (seeded from `artifacts`), else list yours. With `project`: add `artifacts`, `remove` one, `title` renames, set `visibility`, `order`/`move` reorder, a `rule` adds matches as they are published, or read it. `delete` with `confirm: true` removes the project, its order and its share list permanently; its artifacts stay. One change per call, or title with visibility. An artifact's gallery label is not a project: that is `collection` on super_artifact_set.
     */
    get: operations['listProjects']
    put?: never
    /**
     * Create a project, optionally seeded with artifacts
     * @description A project is an ordered set of your artifacts shown one at a time at /s/{slug}, with its own audience and share list. No `project`: `title` creates one (seeded from `artifacts`), else list yours. With `project`: add `artifacts`, `remove` one, `title` renames, set `visibility`, `order`/`move` reorder, a `rule` adds matches as they are published, or read it. `delete` with `confirm: true` removes the project, its order and its share list permanently; its artifacts stay. One change per call, or title with visibility. An artifact's gallery label is not a project: that is `collection` on super_artifact_set.
     */
    post: operations['createProject']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/v1/projects/{project}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    /**
     * One project and its items
     * @description A project is an ordered set of your artifacts shown one at a time at /s/{slug}, with its own audience and share list. No `project`: `title` creates one (seeded from `artifacts`), else list yours. With `project`: add `artifacts`, `remove` one, `title` renames, set `visibility`, `order`/`move` reorder, a `rule` adds matches as they are published, or read it. `delete` with `confirm: true` removes the project, its order and its share list permanently; its artifacts stay. One change per call, or title with visibility. An artifact's gallery label is not a project: that is `collection` on super_artifact_set.
     */
    get: operations['getProject']
    put?: never
    post?: never
    /**
     * Delete a project; its artifacts stay
     * @description A project is an ordered set of your artifacts shown one at a time at /s/{slug}, with its own audience and share list. No `project`: `title` creates one (seeded from `artifacts`), else list yours. With `project`: add `artifacts`, `remove` one, `title` renames, set `visibility`, `order`/`move` reorder, a `rule` adds matches as they are published, or read it. `delete` with `confirm: true` removes the project, its order and its share list permanently; its artifacts stay. One change per call, or title with visibility. An artifact's gallery label is not a project: that is `collection` on super_artifact_set.
     */
    delete: operations['deleteProject']
    options?: never
    head?: never
    /**
     * Rename, set visibility, reorder, move, fold groups or set a rule
     * @description A project is an ordered set of your artifacts shown one at a time at /s/{slug}, with its own audience and share list. No `project`: `title` creates one (seeded from `artifacts`), else list yours. With `project`: add `artifacts`, `remove` one, `title` renames, set `visibility`, `order`/`move` reorder, a `rule` adds matches as they are published, or read it. `delete` with `confirm: true` removes the project, its order and its share list permanently; its artifacts stay. One change per call, or title with visibility. An artifact's gallery label is not a project: that is `collection` on super_artifact_set.
     */
    patch: operations['updateProject']
    trace?: never
  }
  '/v1/projects/{project}/artifacts': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Add artifacts to a project
     * @description A project is an ordered set of your artifacts shown one at a time at /s/{slug}, with its own audience and share list. No `project`: `title` creates one (seeded from `artifacts`), else list yours. With `project`: add `artifacts`, `remove` one, `title` renames, set `visibility`, `order`/`move` reorder, a `rule` adds matches as they are published, or read it. `delete` with `confirm: true` removes the project, its order and its share list permanently; its artifacts stay. One change per call, or title with visibility. An artifact's gallery label is not a project: that is `collection` on super_artifact_set.
     */
    post: operations['addProjectArtifacts']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/v1/projects/{project}/artifacts/{remove}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    post?: never
    /**
     * Remove one artifact (or item) from a project
     * @description A project is an ordered set of your artifacts shown one at a time at /s/{slug}, with its own audience and share list. No `project`: `title` creates one (seeded from `artifacts`), else list yours. With `project`: add `artifacts`, `remove` one, `title` renames, set `visibility`, `order`/`move` reorder, a `rule` adds matches as they are published, or read it. `delete` with `confirm: true` removes the project, its order and its share list permanently; its artifacts stay. One change per call, or title with visibility. An artifact's gallery label is not a project: that is `collection` on super_artifact_set.
     */
    delete: operations['removeProjectArtifact']
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/v1/artifacts/{artifact}/shares': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Give named people access to an artifact
     * @description Give named people access to one of: an `artifact` (viewer; commenter also comments; editor also edits; new addresses are emailed), a `project` (viewer; each address is emailed) or a `workspace` (editor; returns accept links, sends no email). Someone already named moves to the role sent, so a lower role replaces a higher one; nobody is removed. Never changes visibility: public stays public; restrict with super_artifact_set. At most 20 addresses for an artifact, 50 for a project or workspace.
     */
    post: operations['shareArtifact']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/v1/projects/{project}/shares': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Give named people access to a project
     * @description Give named people access to one of: an `artifact` (viewer; commenter also comments; editor also edits; new addresses are emailed), a `project` (viewer; each address is emailed) or a `workspace` (editor; returns accept links, sends no email). Someone already named moves to the role sent, so a lower role replaces a higher one; nobody is removed. Never changes visibility: public stays public; restrict with super_artifact_set. At most 20 addresses for an artifact, 50 for a project or workspace.
     */
    post: operations['shareProject']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/v1/workspace/shares': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Invite editors to a workspace (returns accept links)
     * @description Give named people access to one of: an `artifact` (viewer; commenter also comments; editor also edits; new addresses are emailed), a `project` (viewer; each address is emailed) or a `workspace` (editor; returns accept links, sends no email). Someone already named moves to the role sent, so a lower role replaces a higher one; nobody is removed. Never changes visibility: public stays public; restrict with super_artifact_set. At most 20 addresses for an artifact, 50 for a project or workspace.
     */
    post: operations['shareWorkspace']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/v1/artifacts/{artifact}/comments': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    /**
     * Comment threads on an artifact, newest first
     * @description Comment threads people left inside an artifact, newest first (default `status: "open"`). Each carries its messages (author, body, `shot`), its `kind` (`page` has no anchor), its anchor (`sel`, `x`/`y`) and the version viewed. `respond`: reply to and/or resolve up to 20 threads in one call, one outcome each; `resolve: false` reopens, so nothing here is final. `screenshot`: one message's screenshot, as an image. An agent cannot open or delete a thread. `mentioned: true`: your @mentions, any artifact, oldest unseen first; listing marks them seen.
     */
    get: operations['listComments']
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/v1/artifacts/{artifact}/comments/responses': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Reply to and/or resolve threads, one outcome each
     * @description Comment threads people left inside an artifact, newest first (default `status: "open"`). Each carries its messages (author, body, `shot`), its `kind` (`page` has no anchor), its anchor (`sel`, `x`/`y`) and the version viewed. `respond`: reply to and/or resolve up to 20 threads in one call, one outcome each; `resolve: false` reopens, so nothing here is final. `screenshot`: one message's screenshot, as an image. An agent cannot open or delete a thread. `mentioned: true`: your @mentions, any artifact, oldest unseen first; listing marks them seen.
     */
    post: operations['respondToComments']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/v1/artifacts/{artifact}/comments/screenshots/{screenshot}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    /**
     * One message's screenshot, base64 in `image`
     * @description Comment threads people left inside an artifact, newest first (default `status: "open"`). Each carries its messages (author, body, `shot`), its `kind` (`page` has no anchor), its anchor (`sel`, `x`/`y`) and the version viewed. `respond`: reply to and/or resolve up to 20 threads in one call, one outcome each; `resolve: false` reopens, so nothing here is final. `screenshot`: one message's screenshot, as an image. An agent cannot open or delete a thread. `mentioned: true`: your @mentions, any artifact, oldest unseen first; listing marks them seen.
     */
    get: operations['getCommentScreenshot']
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/v1/mentions': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    /**
     * Where people @mentioned you; listing marks them seen
     * @description Comment threads people left inside an artifact, newest first (default `status: "open"`). Each carries its messages (author, body, `shot`), its `kind` (`page` has no anchor), its anchor (`sel`, `x`/`y`) and the version viewed. `respond`: reply to and/or resolve up to 20 threads in one call, one outcome each; `resolve: false` reopens, so nothing here is final. `screenshot`: one message's screenshot, as an image. An agent cannot open or delete a thread. `mentioned: true`: your @mentions, any artifact, oldest unseen first; listing marks them seen.
     */
    get: operations['listMentions']
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/v1/signatures': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    /**
     * An artifact's signature requests, newest first
     * @description Ask named people to sign one published version of an artifact, and follow the request. `request` with `artifact`, `signers` [{name, email, party?}] (≤10) and an optional `message` (≤500 characters) emails each signer a private link; the version must be one file of at most 2 MiB, and it is kept while the request is open and for good once it completes. `status` with `request` (one) or `artifact` (all, newest first). `withdraw` closes an open request. `remind` emails `signer` the link again, three times at most, a day apart. Only each signer can sign, in a browser, after a code sent to their address: an agent cannot.
     */
    get: operations['listSignatureRequests']
    put?: never
    /**
     * Ask named people to sign one version of an artifact
     * @description Ask named people to sign one published version of an artifact, and follow the request. `request` with `artifact`, `signers` [{name, email, party?}] (≤10) and an optional `message` (≤500 characters) emails each signer a private link; the version must be one file of at most 2 MiB, and it is kept while the request is open and for good once it completes. `status` with `request` (one) or `artifact` (all, newest first). `withdraw` closes an open request. `remind` emails `signer` the link again, three times at most, a day apart. Only each signer can sign, in a browser, after a code sent to their address: an agent cannot.
     */
    post: operations['requestSignatures']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/v1/signatures/{request}': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    /**
     * One signature request and its signers
     * @description Ask named people to sign one published version of an artifact, and follow the request. `request` with `artifact`, `signers` [{name, email, party?}] (≤10) and an optional `message` (≤500 characters) emails each signer a private link; the version must be one file of at most 2 MiB, and it is kept while the request is open and for good once it completes. `status` with `request` (one) or `artifact` (all, newest first). `withdraw` closes an open request. `remind` emails `signer` the link again, three times at most, a day apart. Only each signer can sign, in a browser, after a code sent to their address: an agent cannot.
     */
    get: operations['getSignatureRequest']
    put?: never
    post?: never
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/v1/signatures/{request}/remind': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Email a signer their link again
     * @description Ask named people to sign one published version of an artifact, and follow the request. `request` with `artifact`, `signers` [{name, email, party?}] (≤10) and an optional `message` (≤500 characters) emails each signer a private link; the version must be one file of at most 2 MiB, and it is kept while the request is open and for good once it completes. `status` with `request` (one) or `artifact` (all, newest first). `withdraw` closes an open request. `remind` emails `signer` the link again, three times at most, a day apart. Only each signer can sign, in a browser, after a code sent to their address: an agent cannot.
     */
    post: operations['remindSigner']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
  '/v1/signatures/{request}/withdraw': {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    get?: never
    put?: never
    /**
     * Close an open signature request
     * @description Ask named people to sign one published version of an artifact, and follow the request. `request` with `artifact`, `signers` [{name, email, party?}] (≤10) and an optional `message` (≤500 characters) emails each signer a private link; the version must be one file of at most 2 MiB, and it is kept while the request is open and for good once it completes. `status` with `request` (one) or `artifact` (all, newest first). `withdraw` closes an open request. `remind` emails `signer` the link again, three times at most, a day apart. Only each signer can sign, in a browser, after a code sent to their address: an agent cannot.
     */
    post: operations['withdrawSignatureRequest']
    delete?: never
    options?: never
    head?: never
    patch?: never
    trace?: never
  }
}
export type webhooks = Record<string, never>
export interface components {
  schemas: {
    Error: {
      error: {
        /** @description Stable, machine-readable. */
        code: string
        /** @description For a person. */
        message: string
        fix?: string
        retryAfterSeconds?: number
      } & {
        [key: string]: unknown
      }
    }
  }
  responses: {
    /** @description A refusal. 400 invalid arguments, 401 no or bad key, 402 plan limit, 403 forbidden or read-only key, 404 not found, 409 conflict, 413 body over 1 MiB, 429 rate limited (see Retry-After). */
    Error: {
      headers: {
        /** @description On 429: seconds to wait. */
        'Retry-After'?: number
        [name: string]: unknown
      }
      content: {
        'application/json': components['schemas']['Error']
      }
    }
  }
  parameters: never
  requestBodies: never
  headers: never
  pathItems: never
}
export type $defs = Record<string, never>
export interface operations {
  whoami: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Who this key publishes as */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': {
            [key: string]: unknown
          }
        }
      }
      default: components['responses']['Error']
    }
  }
  getHelp: {
    parameters: {
      query?: {
        topic?: 'tools' | 'data' | 'templates' | 'collections' | 'projects' | 'batch'
      }
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description How the operations fit together */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': {
            [key: string]: unknown
          }
        }
      }
      default: components['responses']['Error']
    }
  }
  listArtifacts: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description List your artifacts, newest first */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': {
            [key: string]: unknown
          }
        }
      }
      default: components['responses']['Error']
    }
  }
  publishArtifact: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': {
          /** @description Kebab-case, 3–63 chars, under your key’s handle: it updates one there you are Editor on. Another workspace’s artifact: publish from its dashboard. */
          slug: string
          /** @description One sentence on why; shown in the gallery. */
          prompt: string
          /** @description Complete self-contained index.html. */
          html?: string
          /** @description Filled slots for `template`'s runtime, by slot name; `json` slots are schema-checked. */
          values?: Record<string, unknown>
          /** @description Instead of `slug`/`values`: several pages of one `template`. */
          instances?: {
            slug: string
            values: Record<string, unknown>
            title?: string
          }[]
          /** @description The template built from (provenance); required with `values` or `instances`. */
          template?: {
            slug: string
            version?: number
          }
          /** @description Under 60 chars. Default: page <title>. */
          title?: string
          /** @description Link-preview sentence, under 200 chars. Default: `prompt`. */
          description?: string
          /**
           * @description Default `page`. `dashboard` labels a page of mostly live data.
           * @enum {string}
           */
          kind?: 'page' | 'slideshow' | 'survey' | 'tracker' | 'video' | 'tool' | 'dashboard'
          /** @description Gallery grouping label, not a content collection. */
          collection?: string
          /**
           * @description From version 1. Default: the workspace default; public is set after.
           * @enum {string}
           */
          visibility?: 'private' | 'organization'
          /** @description Data policy v1. Visitors submit to a sheet (perUser single, upsert, a field per question), a log (many, append-only) or a shared doc (shared, key). CMS rows: `collections`. See super_help data. */
          policy?: Record<string, unknown>
          /** @description With `values`: overrides the declaration's `dataset.key`. */
          dataset?: string
          /** @description With `values`: the dataset key this one succeeds. */
          continues?: string
          /** @description uploadId from super_upload; its files ship with the page. */
          uploads?: string
          /** @description With `uploads`: the staged JSON file to read `values` from. */
          valuesFile?: string
          /** @description With `html`: small assets. ≤200, 5 MiB each, 10 MiB total, decoded. */
          files?: {
            /** @description Relative, no leading slash. */
            path: string
            /** @description Base64 of the bytes. */
            content: string
            /** @description Default: from the extension. */
            contentType?: string
            /** @description Hex digest of the decoded bytes. */
            sha256?: string
          }[]
        }
      }
    }
    responses: {
      /** @description Publish an artifact, or a new version of one */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': {
            [key: string]: unknown
          }
        }
      }
      default: components['responses']['Error']
    }
  }
  getArtifact: {
    parameters: {
      query?: never
      header?: never
      path: {
        /** @description Artifact id or slug. */
        artifact: string
      }
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description One artifact: its versions, published version and declaration */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': {
            [key: string]: unknown
          }
        }
      }
      default: components['responses']['Error']
    }
  }
  deleteArtifact: {
    parameters: {
      query: {
        /** @description Repeat the artifact: deleting is permanent. */
        confirm: string
      }
      header?: never
      path: {
        /** @description Artifact id or slug. */
        artifact: string
      }
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Delete an artifact with every version, permanently */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': {
            [key: string]: unknown
          }
        }
      }
      default: components['responses']['Error']
    }
  }
  updateArtifact: {
    parameters: {
      query?: never
      header?: never
      path: {
        /** @description Artifact id or slug. */
        artifact: string
      }
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': {
          /**
           * @description private: Restricted (default). organization: anyone at the workspace. public: anyone with the link.
           * @enum {string}
           */
          visibility?: 'private' | 'organization' | 'public'
          /** @description Gallery grouping label, ≤ 60 chars. Empty clears it. */
          collection?: string
          /** @description The name a stream’s `revealAt` waits for; from then on that stream reads as public. */
          phase?: string
          notifyOnSubmission?: boolean
        }
      }
    }
    responses: {
      /** @description Change visibility, gallery label, live phase or submission email */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': {
            [key: string]: unknown
          }
        }
      }
      default: components['responses']['Error']
    }
  }
  readArtifactFile: {
    parameters: {
      query?: {
        path?: string
        version?: number
      }
      header?: never
      path: {
        /** @description Artifact id or slug. */
        artifact: string
      }
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Read one file of a version as text (default: the published index.html) */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': {
            [key: string]: unknown
          }
        }
      }
      default: components['responses']['Error']
    }
  }
  openArtifact: {
    parameters: {
      query?: never
      header?: never
      path: {
        /** @description Artifact id or slug. */
        artifact: string
      }
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': {
          version?: number
        }
      }
    }
    responses: {
      /** @description A ten-minute viewer URL for an artifact, private included */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': {
            [key: string]: unknown
          }
        }
      }
      default: components['responses']['Error']
    }
  }
  serveVersion: {
    parameters: {
      query?: never
      header?: never
      path: {
        /** @description Artifact id or slug. */
        artifact: string
        version: number
      }
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Serve an existing version again */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': {
            [key: string]: unknown
          }
        }
      }
      default: components['responses']['Error']
    }
  }
  startLiveRoom: {
    parameters: {
      query?: never
      header?: never
      path: {
        /** @description Artifact id or slug. */
        artifact: string
      }
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Turn an artifact's live room on */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': {
            [key: string]: unknown
          }
        }
      }
      default: components['responses']['Error']
    }
  }
  stopLiveRoom: {
    parameters: {
      query?: never
      header?: never
      path: {
        /** @description Artifact id or slug. */
        artifact: string
      }
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Turn an artifact's live room off, disconnecting every visitor */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': {
            [key: string]: unknown
          }
        }
      }
      default: components['responses']['Error']
    }
  }
  stageUploads: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': {
          files: {
            path: string
            /** @description Exact size. */
            bytes: number
            /** @description Hex; checked on upload. */
            sha256?: string
            /** @description Default: from the extension. */
            contentType?: string
          }[]
        }
      }
    }
    responses: {
      /** @description Stage big files for a publish; PUT each to its URL */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': {
            [key: string]: unknown
          }
        }
      }
      default: components['responses']['Error']
    }
  }
  listArtifactRows: {
    parameters: {
      query?: {
        /** @description ANDed 'field op value' clauses: 'reps >= 5', 'day in mon,tue', 'note is set'. Ops: = != > >= < <= contains in, is set, is unset. System: _version _at _status _visitor. */
        filter?: string[]
        /** @description ISO-8601 instant or window (7d, 24h). Or a version (v2) when addressing one artifact. */
        since?: string
        until?: string
        /** @description By collection time. */
        sort?: 'newest' | 'oldest'
        /** @description Per artifact. Default 50. */
        limit?: number
        /** @description The previous cursor.next. */
        cursor?: string
        fields?: string[]
      }
      header?: never
      path: {
        /** @description Artifact id or slug. */
        artifact: string
      }
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Rows visitors submitted to one artifact, newest first */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': {
            [key: string]: unknown
          }
        }
      }
      default: components['responses']['Error']
    }
  }
  writeArtifactRows: {
    parameters: {
      query?: never
      header?: never
      path: {
        /** @description Artifact id or slug. */
        artifact: string
      }
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': {
          stream?: string
          rows?: Record<string, unknown>[]
          ops?: Record<string, unknown>[]
          atomic?: boolean
        }
      }
    }
    responses: {
      /** @description Write rows into an artifact you may edit */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': {
            [key: string]: unknown
          }
        }
      }
      default: components['responses']['Error']
    }
  }
  listRows: {
    parameters: {
      query?: {
        dataset?: string
        /** @description The gallery grouping label set at publish, case-sensitive. Not a content collection. */
        collection?: string
        /** @description ANDed 'field op value' clauses: 'reps >= 5', 'day in mon,tue', 'note is set'. Ops: = != > >= < <= contains in, is set, is unset. System: _version _at _status _visitor. */
        filter?: string[]
        /** @description ISO-8601 instant or window (7d, 24h). Or a version (v2) when addressing one artifact. */
        since?: string
        until?: string
        /** @description By collection time. */
        sort?: 'newest' | 'oldest'
        /** @description Per artifact. Default 50. */
        limit?: number
        /** @description The previous cursor.next. */
        cursor?: string
        fields?: string[]
      }
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Rows submitted to a dataset or a gallery label */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': {
            [key: string]: unknown
          }
        }
      }
      default: components['responses']['Error']
    }
  }
  queryData: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': {
          /** @description The union of the forms given. */
          scope?: {
            series?: string
            datasets?: string[]
            /** @description All must match. */
            tags?: string[]
          }
          /** @description Catalog measure names, not field names. */
          measures?: string[]
          /** @enum {string} */
          agg?: 'sum' | 'avg' | 'min' | 'max' | 'count' | 'last'
          /** @description Derived columns, in order; operands name a measure or an earlier `as`. */
          compute?: {
            as: string
            /** @enum {string} */
            expr: 'a * b' | 'a / b' | 'a + b'
            operands: string[]
            unit?: string
          }[]
          /** @description ANDed 'field op value' clauses: 'reps >= 5', 'day in mon,tue', 'note is set'. Ops: = != > >= < <= in. Catalog fields only. */
          filter?: string[]
          /** @description One of dataset, day, week, month, visitor, or "field:{name}". */
          group_by?: (string | ('dataset' | 'day' | 'week' | 'month' | 'visitor') | unknown)[]
          /** @description ISO-8601 instant or window (7d, 24h). */
          since?: string
          until?: string
          limit?: number
          /** @description One artifact's per-field distributions instead of a scoped query. */
          distributions?: {
            /** @description Artifact id or slug. */
            artifact: string
            version?: number
            /** @description A choice, boolean or integer field. */
            group_by?: string
            /** @enum {string} */
            bucket?: 'day' | 'week'
          }
        }
      }
    }
    responses: {
      /** @description Aggregate what was collected: numbers, never rows */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': {
            [key: string]: unknown
          }
        }
      }
      default: components['responses']['Error']
    }
  }
  getSchema: {
    parameters: {
      query?: {
        series?: string
        /** @description All must match. */
        tags?: string[]
        /** @description Artifact id or slug. */
        artifact?: string
        /** @description Alone: 2+ ids or slugs; their fields side by side, conflicts named. */
        compare?: string[]
        /** @description ISO-8601 instant or window (7d, 24h). */
        since?: string
        /** @description Workspace handle. Omit for your own. */
        workspace?: string
      }
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description The data catalog: datasets and content collections, or a comparison */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': {
            [key: string]: unknown
          }
        }
      }
      default: components['responses']['Error']
    }
  }
  defineCollection: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': {
          /** @description A content collection definition: creates one, or replaces the one with this key. */
          define?: {
            /** @description Lowercase letters, digits, underscores; starts with a letter. */
            key: string
            /** @description 1–80 chars. */
            name: string
            description?: string
            /** @description Labels an entry. Default: first text field. */
            displayField?: string
            fields: {
              name: string
              /** @description text long_text rich_text email url phone color integer decimal rating measurement boolean date datetime time choice multi_choice json reference reference_list */
              type: string
              label?: string
              required?: boolean
              unique?: boolean
              /**
               * @description contact: masked for non-owners. sensitive: encrypted, no sort/filter/search. secret: write-only credential.
               * @enum {string}
               */
              pii: 'none' | 'contact' | 'sensitive' | 'secret'
              description?: string
              /** @description By type: minLength maxLength pattern; min max precision; scale; measure unit; after before; choices minChoices maxChoices; collection onDelete; maxItems; maxBytes. */
              rules?: Record<string, unknown>
            }[]
          }
          /** @description Workspace handle. Omit for your own. */
          workspace?: string
        }
      }
    }
    responses: {
      /** @description Create or replace a content collection */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': {
            [key: string]: unknown
          }
        }
      }
      default: components['responses']['Error']
    }
  }
  listEntries: {
    parameters: {
      query?: {
        /** @description Workspace handle. Omit for your own. */
        workspace?: string
        /** @description ANDed 'field op value' clauses: 'reps >= 5', 'day in mon,tue', 'note is set'. Ops: = != > >= < <= contains starts has in, is set, is empty. System: _created_at _updated_at _status _author. */
        filter?: string[]
        /** @description Case-insensitive, over text fields. */
        search?: string
        /** @description Field or system column. Default _created_at. */
        sort?: string
        direction?: 'asc' | 'desc'
        page?: number
        limit?: number
      }
      header?: never
      path: {
        /** @description Content collection key (a content model), not a gallery label. */
        collection: string
      }
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description One page of a content collection's entries */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': {
            [key: string]: unknown
          }
        }
      }
      default: components['responses']['Error']
    }
  }
  createEntries: {
    parameters: {
      query?: never
      header?: never
      path: {
        /** @description Content collection key (a content model), not a gallery label. */
        collection: string
      }
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': {
          /** @description Keyed by field name. An array writes a batch. */
          values?: Record<string, unknown> | Record<string, unknown>[]
          /**
           * @description Written entries. Default published.
           * @enum {string}
           */
          status?: 'draft' | 'published' | 'archived'
          /** @description Workspace handle. Omit for your own. */
          workspace?: string
        }
      }
    }
    responses: {
      /** @description Create one entry, or a batch */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': {
            [key: string]: unknown
          }
        }
      }
      default: components['responses']['Error']
    }
  }
  useSecret: {
    parameters: {
      query?: never
      header?: never
      path: {
        /** @description Content collection key (a content model), not a gallery label. */
        collection: string
        /** @description The entry id. */
        entry: string
        /** @description The `pii: secret` field whose value is sent. */
        field: string
      }
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': {
          /** @enum {string} */
          method: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE'
          /** @description https only; its host must be the approved one. Redirects are returned, never followed. */
          url: string
          /** @description Sent as given, except host, authorization, cookie, proxy-* and the grant’s own header. */
          headers?: {
            [key: string]: string
          }
          /** @description ≤64 KiB. */
          body?: string
          /** @description Where the value goes; asked for when no grant exists. The approved grant’s header wins. */
          header?: {
            /** @description e.g. authorization, x-api-key. */
            name: string
            /** @description Prefix before the value, e.g. "Bearer ". May be empty. */
            scheme?: string
          }
        }
      }
    }
    responses: {
      /** @description Call an approved API with a stored secret you cannot read (workspace keys) */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': {
            [key: string]: unknown
          }
        }
      }
      default: components['responses']['Error']
    }
  }
  listTemplates: {
    parameters: {
      query?: {
        /** @description What the person asked for, in their words. */
        request?: string
        /** @description Default installed. */
        scope?: 'installed' | 'marketplace'
        /** @description A label, not a capability. */
        kind?: 'page' | 'slideshow' | 'survey' | 'tracker' | 'video' | 'tool' | 'dashboard'
        /** @description Default relevance with `request`, else rating. */
        sort?: 'relevance' | 'rating' | 'uses' | 'installs' | 'recent'
        /** @description Default 5. */
        limit?: number
        /** @description Any of. */
        jobs?: (
          | 'track'
          | 'collect'
          | 'present'
          | 'report'
          | 'monitor'
          | 'prove'
          | 'document'
          | 'explain'
          | 'plan'
          | 'decide'
          | 'review'
          | 'learn'
          | 'prototype'
          | 'announce'
          | 'compute'
          | 'curate'
          | 'coordinate'
          | 'play'
        )[]
        /** @description Any of. */
        audience?: (
          | 'everyone'
          | 'engineering'
          | 'product'
          | 'design'
          | 'marketing'
          | 'sales'
          | 'ops'
          | 'people'
          | 'finance'
          | 'founders'
          | 'education'
          | 'personal'
          | 'community'
        )[]
        /** @description All of. `["runtime"]`: ships code. */
        needs?: ('runtime' | 'data' | 'comments' | 'live')[]
        /** @description fill: you send a document; write: you write the page; build: page and policy. */
        cost?: 'fill' | 'write' | 'build'
        /** @description Marketplace trust tier: Official, Verified or Community. */
        tier?: 'all' | 'official' | 'verified' | 'community'
        mine?: boolean
      }
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Find, rank or list templates */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': {
            [key: string]: unknown
          }
        }
      }
      default: components['responses']['Error']
    }
  }
  saveTemplate: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': {
          /** @description Kebab-case, 3–64 chars. Permanent. */
          slug: string
          title: string
          description: string
          /**
           * @description `dashboard`: a page that mostly shows live data — a label, not a capability.
           * @enum {string}
           */
          kind?: 'page' | 'slideshow' | 'survey' | 'tracker' | 'video' | 'tool' | 'dashboard'
          /** @description What a person hires it for; the first is primary. Create default: from `kind`. */
          jobs?: (
            | 'track'
            | 'collect'
            | 'present'
            | 'report'
            | 'monitor'
            | 'prove'
            | 'document'
            | 'explain'
            | 'plan'
            | 'decide'
            | 'review'
            | 'learn'
            | 'prototype'
            | 'announce'
            | 'compute'
            | 'curate'
            | 'coordinate'
            | 'play'
          )[]
          /** @description 1–3, or `everyone` alone (the default). */
          audience?: (
            | 'everyone'
            | 'engineering'
            | 'product'
            | 'design'
            | 'marketing'
            | 'sales'
            | 'ops'
            | 'people'
            | 'finance'
            | 'founders'
            | 'education'
            | 'personal'
            | 'community'
          )[]
          /** @description Things to build from it; the build prompt draws on them. */
          useCases?: {
            title: string
            prompt: string
          }[]
          /**
           * @description After install: `scenarios` (default) offers three builds; `explainer` builds one from the sample; `interview` asks three questions first.
           * @enum {string}
           */
          installArchetype?: 'scenarios' | 'explainer' | 'interview'
          /** @description Your note, appended to the build prompt as a suggestion. */
          installAfter?: string
          /** @description The sample may appear on the public listing page. */
          samplePublic?: boolean
          /**
           * @description Deprecated; read as `jobs` when `jobs` is absent.
           * @enum {string}
           */
          category?:
            | 'trackers'
            | 'surveys'
            | 'presentations'
            | 'dashboards'
            | 'documents'
            | 'tools'
            | 'games'
            | 'other'
          /** @description `slots`, `declaration` (every instance’s policy), optional `comments`, `keywords` (searched), `examplePrompts`. */
          spec: {
            /** @description The fill schema, an array: [{"name": "headline", "type": "text", "required": true, "max": 120}]. */
            slots?: {
              name: string
              type: string
            }[]
          }
          /** @description Optional notes for whoever fills it. */
          guidance?: string
          /** @description A prompt a person copies to ask for one. */
          prompt?: string
          /** @description `{"values": {…}}`, rendered in the preview. */
          sample?: Record<string, unknown>
          /** @description Slug of your artifact to link as the demo (linked once public). "" clears it. */
          demo?: string
          /** @description Runtime files, `index.html` required. Omitting them on a revision drops the runtime from that new draft version only. */
          files?: {
            path: string
            /** @description UTF-8 text, base64-ed for you. Send `text` or `content`. */
            text?: string
            /** @description Base64 of the bytes, for binaries. */
            content?: string
            contentType?: string
          }[]
          /** @description Extra artifacts each publish makes at {slug}-{role}, same values (e.g. a stage for a host). Bind the primary with `source: {artifact: "@primary", streams}`. Released: add, never remove. */
          companions?: {
            /** @description Kebab-case, unique, not "primary". */
            role: string
            title: string
            description?: string
            /** @enum {string} */
            kind?: 'page' | 'slideshow' | 'survey' | 'tracker' | 'video' | 'tool' | 'dashboard'
            /**
             * @description Default inherit: the primary’s.
             * @enum {string}
             */
            visibility?: 'inherit' | 'private' | 'public'
            /** @description This part’s policy, or omit. */
            declaration?: Record<string, unknown>
            /** @description Slot names whose values this part gets. Default all. */
            slots?: string[]
            /** @description Runtime files, `index.html` required. Omitting them on a revision drops the runtime from that new draft version only. */
            files: {
              path: string
              /** @description UTF-8 text, base64-ed for you. Send `text` or `content`. */
              text?: string
              /** @description Base64 of the bytes, for binaries. */
              content?: string
              contentType?: string
            }[]
          }[]
          /** @description The version you revised. Present: revise. Absent: create. */
          expectedVersion?: number
          /** @description Revisions: one line on why, for the changelog. */
          changeNote?: string
        }
      }
    }
    responses: {
      /** @description Create or revise a template draft */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': {
            [key: string]: unknown
          }
        }
      }
      default: components['responses']['Error']
    }
  }
  getTemplate: {
    parameters: {
      query?: {
        /** @description Default: the released one. */
        version?: number
      }
      header?: never
      path: {
        slug: string
      }
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description One template in full, with its install prompt */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': {
            [key: string]: unknown
          }
        }
      }
      default: components['responses']['Error']
    }
  }
  getTemplateHistory: {
    parameters: {
      query?: never
      header?: never
      path: {
        slug: string
      }
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description A template's changelog */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': {
            [key: string]: unknown
          }
        }
      }
      default: components['responses']['Error']
    }
  }
  getTemplateFeedback: {
    parameters: {
      query?: never
      header?: never
      path: {
        slug: string
      }
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Comments on a template's artifacts, as themes */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': {
            [key: string]: unknown
          }
        }
      }
      default: components['responses']['Error']
    }
  }
  actOnTemplate: {
    parameters: {
      query?: never
      header?: never
      path: {
        slug: string
      }
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': {
          /** @enum {string} */
          action: 'install' | 'uninstall' | 'rate' | 'report' | 'rollback' | 'request_verification'
          stars?: number
          version?: number
          /**
           * @description Report only.
           * @enum {string}
           */
          kind?: 'spam' | 'harmful' | 'broken' | 'misleading' | 'pii' | 'copyright' | 'other'
          /** @description Report only. */
          reason?: string
          /** @description Install only: true once the person agreed to this public template. Never set it unasked (`permission_required`). */
          confirmedByPerson?: boolean
        }
      }
    }
    responses: {
      /** @description Install, uninstall, rate, report, roll back or request verification */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': {
            [key: string]: unknown
          }
        }
      }
      default: components['responses']['Error']
    }
  }
  releaseTemplate: {
    parameters: {
      query?: never
      header?: never
      path: {
        slug: string
      }
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': {
          version: number
          /**
           * @description `unlisted` (default): by slug. `public`: marketplace. `workspace`: team shelf, members only.
           * @enum {string}
           */
          visibility?: 'public' | 'unlisted' | 'workspace'
          /** @description Default false. Makes the demo artifact, and its data, public. */
          demoConsent?: boolean
          /** @description true: show the sample on the public listing. Omit: unchanged. */
          sampleConsent?: boolean
        }
      }
    }
    responses: {
      /** @description Release one version of your template */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': {
            [key: string]: unknown
          }
        }
      }
      default: components['responses']['Error']
    }
  }
  listProjects: {
    parameters: {
      query?: {
        /** @description Workspace handle. Omit for your own. */
        workspace?: string
      }
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Your projects */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': {
            [key: string]: unknown
          }
        }
      }
      default: components['responses']['Error']
    }
  }
  createProject: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': {
          /** @description ≤ 120 chars. */
          title?: string
          /** @description Artifact ids or slugs, in order. */
          artifacts?: string[]
          /** @description Heading over these artifacts. */
          groupLabel?: string
          /**
           * @description organization: anyone at the workspace. Widening over private needs confirm.
           * @enum {string}
           */
          visibility?: 'private' | 'organization' | 'public'
          /** @description See super_help projects. null: manual. */
          rule?: Record<string, unknown> | null
          /** @description Needed to delete; also to add a private artifact to a shared project, or widen one holding private ones (`confirm_private`). */
          confirm?: boolean
          /** @description Workspace handle. Omit for your own. */
          workspace?: string
        }
      }
    }
    responses: {
      /** @description Create a project, optionally seeded with artifacts */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': {
            [key: string]: unknown
          }
        }
      }
      default: components['responses']['Error']
    }
  }
  getProject: {
    parameters: {
      query?: {
        /** @description Workspace handle. Omit for your own. */
        workspace?: string
      }
      header?: never
      path: {
        /** @description Project id, slug or exact title. */
        project: string
      }
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description One project and its items */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': {
            [key: string]: unknown
          }
        }
      }
      default: components['responses']['Error']
    }
  }
  deleteProject: {
    parameters: {
      query: {
        /** @description Repeat the project: deleting is permanent. */
        confirm: string
      }
      header?: never
      path: {
        /** @description Project id, slug or exact title. */
        project: string
      }
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Delete a project; its artifacts stay */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': {
            [key: string]: unknown
          }
        }
      }
      default: components['responses']['Error']
    }
  }
  updateProject: {
    parameters: {
      query?: never
      header?: never
      path: {
        /** @description Project id, slug or exact title. */
        project: string
      }
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': {
          /** @description ≤ 120 chars. */
          title?: string
          /**
           * @description organization: anyone at the workspace. Widening over private needs confirm.
           * @enum {string}
           */
          visibility?: 'private' | 'organization' | 'public'
          /** @description Every item once, in order: ids or slugs. */
          order?: string[]
          move?: {
            /** @description An artifact id or slug, or an item id. */
            artifact: string
            /** @description New position; 1 is first. */
            to: number
          }
          /** @description See super_help projects. null: manual. */
          rule?: Record<string, unknown> | null
          /** @description groupLabels shown folded. Whole set. */
          collapsedGroups?: string[]
          /** @description Needed to delete; also to add a private artifact to a shared project, or widen one holding private ones (`confirm_private`). */
          confirm?: boolean
          /** @description Workspace handle. Omit for your own. */
          workspace?: string
        }
      }
    }
    responses: {
      /** @description Rename, set visibility, reorder, move, fold groups or set a rule */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': {
            [key: string]: unknown
          }
        }
      }
      default: components['responses']['Error']
    }
  }
  addProjectArtifacts: {
    parameters: {
      query?: never
      header?: never
      path: {
        /** @description Project id, slug or exact title. */
        project: string
      }
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': {
          /** @description Artifact ids or slugs, in order. */
          artifacts?: string[]
          /** @description Heading over these artifacts. */
          groupLabel?: string
          /** @description Needed to delete; also to add a private artifact to a shared project, or widen one holding private ones (`confirm_private`). */
          confirm?: boolean
          /** @description Workspace handle. Omit for your own. */
          workspace?: string
        }
      }
    }
    responses: {
      /** @description Add artifacts to a project */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': {
            [key: string]: unknown
          }
        }
      }
      default: components['responses']['Error']
    }
  }
  removeProjectArtifact: {
    parameters: {
      query?: never
      header?: never
      path: {
        /** @description Project id, slug or exact title. */
        project: string
        /** @description An artifact id or slug, or an item id. */
        remove: string
      }
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Remove one artifact (or item) from a project */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': {
            [key: string]: unknown
          }
        }
      }
      default: components['responses']['Error']
    }
  }
  shareArtifact: {
    parameters: {
      query?: never
      header?: never
      path: {
        /** @description Artifact id or slug. */
        artifact: string
      }
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': {
          emails: string[]
          /**
           * @description Default viewer; editor for a workspace. An editor's key restores (super_artifact_set version), writes (super_data_write), publishes by slug in its workspace.
           * @enum {string}
           */
          role?: 'viewer' | 'commenter' | 'editor'
        }
      }
    }
    responses: {
      /** @description Give named people access to an artifact */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': {
            [key: string]: unknown
          }
        }
      }
      default: components['responses']['Error']
    }
  }
  shareProject: {
    parameters: {
      query?: never
      header?: never
      path: {
        /** @description Project id, slug or exact title. */
        project: string
      }
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': {
          emails: string[]
          /**
           * @description Default viewer; editor for a workspace. An editor's key restores (super_artifact_set version), writes (super_data_write), publishes by slug in its workspace.
           * @enum {string}
           */
          role?: 'viewer' | 'commenter' | 'editor'
          /** @description Project only: true shares a project that holds private artifacts (`confirm_private`). */
          confirm?: boolean
        }
      }
    }
    responses: {
      /** @description Give named people access to a project */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': {
            [key: string]: unknown
          }
        }
      }
      default: components['responses']['Error']
    }
  }
  shareWorkspace: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody: {
      content: {
        'application/json': {
          emails: string[]
          /**
           * @description Default viewer; editor for a workspace. An editor's key restores (super_artifact_set version), writes (super_data_write), publishes by slug in its workspace.
           * @enum {string}
           */
          role?: 'viewer' | 'commenter' | 'editor'
          /** @description A handle you administer, or "" for your own. */
          workspace?: string
        }
      }
    }
    responses: {
      /** @description Invite editors to a workspace (returns accept links) */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': {
            [key: string]: unknown
          }
        }
      }
      default: components['responses']['Error']
    }
  }
  listComments: {
    parameters: {
      query?: {
        status?: 'all' | 'open' | 'resolved'
        /** @description A path inside the artifact, e.g. "/pricing". Not pagination. */
        page?: string
        limit?: number
        /** @description The previous cursor.next. */
        cursor?: string
      }
      header?: never
      path: {
        /** @description Artifact id or slug. */
        artifact: string
      }
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Comment threads on an artifact, newest first */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': {
            [key: string]: unknown
          }
        }
      }
      default: components['responses']['Error']
    }
  }
  respondToComments: {
    parameters: {
      query?: never
      header?: never
      path: {
        /** @description Artifact id or slug. */
        artifact: string
      }
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': {
          respond?: {
            /** @description Thread id, not a message id. */
            thread: string
            /** @description A plain-text reply. */
            body?: string
            /** @description true resolves, false reopens. */
            resolve?: boolean
          }[]
        }
      }
    }
    responses: {
      /** @description Reply to and/or resolve threads, one outcome each */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': {
            [key: string]: unknown
          }
        }
      }
      default: components['responses']['Error']
    }
  }
  getCommentScreenshot: {
    parameters: {
      query?: never
      header?: never
      path: {
        /** @description Artifact id or slug. */
        artifact: string
        /** @description A message id, not a thread id. */
        screenshot: string
      }
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description One message's screenshot, base64 in `image` */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': {
            [key: string]: unknown
          }
        }
      }
      default: components['responses']['Error']
    }
  }
  listMentions: {
    parameters: {
      query?: {
        /** @description Artifact id or slug. */
        artifact?: string
        limit?: number
        /** @description The previous cursor.next. */
        cursor?: string
      }
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Where people @mentioned you; listing marks them seen */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': {
            [key: string]: unknown
          }
        }
      }
      default: components['responses']['Error']
    }
  }
  listSignatureRequests: {
    parameters: {
      query?: {
        /** @description Artifact id or slug. */
        artifact?: string
      }
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description An artifact's signature requests, newest first */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': {
            [key: string]: unknown
          }
        }
      }
      default: components['responses']['Error']
    }
  }
  requestSignatures: {
    parameters: {
      query?: never
      header?: never
      path?: never
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': {
          /** @description Artifact id or slug. */
          artifact?: string
          /** @description The version to sign. Default: the published one. */
          version?: number
          signers?: {
            name: string
            email: string
            /** @description Their role in the agreement, e.g. "Tenant". */
            party?: string
          }[]
          /** @description A note shown to every signer. */
          message?: string
        }
      }
    }
    responses: {
      /** @description Ask named people to sign one version of an artifact */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': {
            [key: string]: unknown
          }
        }
      }
      default: components['responses']['Error']
    }
  }
  getSignatureRequest: {
    parameters: {
      query?: never
      header?: never
      path: {
        /** @description A signature request id, from request or status. */
        request: string
      }
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description One signature request and its signers */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': {
            [key: string]: unknown
          }
        }
      }
      default: components['responses']['Error']
    }
  }
  remindSigner: {
    parameters: {
      query?: never
      header?: never
      path: {
        /** @description A signature request id, from request or status. */
        request: string
      }
      cookie?: never
    }
    requestBody?: {
      content: {
        'application/json': {
          /** @description A signer id, from status. For remind. */
          signer?: string
        }
      }
    }
    responses: {
      /** @description Email a signer their link again */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': {
            [key: string]: unknown
          }
        }
      }
      default: components['responses']['Error']
    }
  }
  withdrawSignatureRequest: {
    parameters: {
      query?: never
      header?: never
      path: {
        /** @description A signature request id, from request or status. */
        request: string
      }
      cookie?: never
    }
    requestBody?: never
    responses: {
      /** @description Close an open signature request */
      200: {
        headers: {
          [name: string]: unknown
        }
        content: {
          'application/json': {
            [key: string]: unknown
          }
        }
      }
      default: components['responses']['Error']
    }
  }
}
