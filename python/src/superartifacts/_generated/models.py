# Generated from sdks/openapi.json, spec hash f1886b4302fd534ad9d18552806f52f6cee192f699da87d92a6b2d59e51a3288. Do not edit.

from __future__ import annotations

from typing import Annotated, Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, RootModel


class Error1(BaseModel):
    model_config = ConfigDict(
        extra='allow',
    )
    code: Annotated[str, Field(description='Stable, machine-readable.')]
    message: Annotated[str, Field(description='For a person.')]
    fix: Optional[str] = None
    retryAfterSeconds: Optional[int] = None


class Error(BaseModel):
    model_config = ConfigDict(
        extra='allow',
    )
    error: Error1


class V1WhoamiGetResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class V1HelpGetResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class V1WebhooksGetResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class V1WebhooksPostRequest(BaseModel):
    model_config = ConfigDict(
        extra='allow',
    )
    url: Annotated[Optional[str], Field(max_length=2048)] = None
    description: Annotated[Optional[str], Field(max_length=500)] = None
    eventTypes: Optional[List[str]] = None
    agent: Annotated[
        Optional[str],
        Field(description='On create or list: me, or an owned agent handle.'),
    ] = None


class V1WebhooksPostResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class V1WebhooksIdGetResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class V1WebhooksIdDeleteResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class V1WebhooksIdTestPostResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class V1WebhooksIdRotatePostResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class V1WebhookMessagesGetResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class V1ArtifactsGetResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class Instance(BaseModel):
    model_config = ConfigDict(
        extra='allow',
    )
    slug: str
    values: Dict[str, Any]
    title: Optional[str] = None


class Template(BaseModel):
    model_config = ConfigDict(
        extra='allow',
    )
    slug: str
    version: Annotated[Optional[int], Field(ge=1)] = None


class File(BaseModel):
    model_config = ConfigDict(
        extra='allow',
    )
    path: Annotated[str, Field(description='Relative, no leading slash.')]
    content: Annotated[str, Field(description='Base64 of the bytes.')]
    contentType: Annotated[
        Optional[str], Field(description='Default: from the extension.')
    ] = None
    sha256: Annotated[
        Optional[str], Field(description='Hex digest of the decoded bytes.')
    ] = None


class V1ArtifactsPostRequest(BaseModel):
    model_config = ConfigDict(
        extra='allow',
    )
    slug: Annotated[
        str,
        Field(
            description='Kebab-case, 3–63 chars, under your key’s handle: it updates one there you are Editor on. Another workspace’s artifact: publish from its dashboard.'
        ),
    ]
    prompt: Annotated[
        Optional[str],
        Field(description='Optional: the request it answers, on its card.'),
    ] = None
    html: Annotated[
        Optional[str], Field(description='Complete self-contained index.html.')
    ] = None
    values: Annotated[
        Optional[Dict[str, Any]],
        Field(
            description="Filled slots for `template`'s runtime, by slot name; `json` slots are schema-checked."
        ),
    ] = None
    instances: Annotated[
        Optional[List[Instance]],
        Field(
            description='Instead of `slug`/`values`: several pages of one `template`.',
            max_length=10,
        ),
    ] = None
    template: Annotated[
        Optional[Template],
        Field(
            description='The template built from (provenance); required with `values` or `instances`.'
        ),
    ] = None
    title: Annotated[
        Optional[str], Field(description='Under 60 chars. Default: page <title>.')
    ] = None
    description: Annotated[
        Optional[str],
        Field(description='Link-preview sentence, under 200 chars. Default: `prompt`.'),
    ] = None
    kind: Annotated[
        Optional[
            Literal[
                'page', 'slideshow', 'survey', 'tracker', 'video', 'tool', 'dashboard'
            ]
        ],
        Field(
            description='Default `page`. `dashboard` labels a page of mostly live data.'
        ),
    ] = None
    collection: Annotated[
        Optional[str],
        Field(description='Gallery grouping label, not a content collection.'),
    ] = None
    visibility: Annotated[
        Optional[Literal['private', 'organization']],
        Field(
            description='From version 1. Default: the workspace default; public is set after.'
        ),
    ] = None
    policy: Annotated[
        Optional[Dict[str, Any]],
        Field(
            description='Data policy v1. Visitors submit to a sheet (perUser single, upsert, a field per question), a log (many, append-only) or a shared doc (shared, key). CMS rows: `collections`. See super_help data.'
        ),
    ] = None
    triggers: Annotated[
        Optional[List[Dict[str, Any]]],
        Field(
            description='Declared agent triggers: key, prompt, optional label, on, who, agent, input, when, once. At most 8 and 12 KiB; omitted on redeploy keeps the previous set.',
            max_length=8,
        ),
    ] = None
    dataset: Annotated[
        Optional[str],
        Field(description="With `values`: overrides the declaration's `dataset.key`."),
    ] = None
    continues: Annotated[
        Optional[str],
        Field(description='With `values`: the dataset key this one succeeds.'),
    ] = None
    uploads: Annotated[
        Optional[str],
        Field(description='uploadId from super_upload; its files ship with the page.'),
    ] = None
    valuesFile: Annotated[
        Optional[str],
        Field(
            description='With `uploads`: the staged JSON file to read `values` from.'
        ),
    ] = None
    files: Annotated[
        Optional[List[File]],
        Field(
            description='With `html`: small assets. ≤200, 5 MiB each, 10 MiB total, decoded.'
        ),
    ] = None


class V1ArtifactsPostResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class V1ArtifactsArtifactGetResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class V1ArtifactsArtifactPatchRequest(BaseModel):
    model_config = ConfigDict(
        extra='allow',
    )
    visibility: Annotated[
        Optional[Literal['private', 'organization', 'public']],
        Field(
            description='private: Restricted (default). organization: anyone at the workspace. public: anyone with the link.'
        ),
    ] = None
    collection: Annotated[
        Optional[str],
        Field(description='Gallery grouping label, ≤ 60 chars. Empty clears it.'),
    ] = None
    phase: Annotated[
        Optional[str],
        Field(
            description='The name a stream’s `revealAt` waits for; from then on that stream reads as public.'
        ),
    ] = None
    notifyOnSubmission: Optional[bool] = None
    triggersEnabled: Optional[bool] = None


class V1ArtifactsArtifactPatchResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class V1ArtifactsArtifactDeleteResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class V1ArtifactsArtifactFileGetResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class V1ArtifactsArtifactOpenPostRequest(BaseModel):
    model_config = ConfigDict(
        extra='allow',
    )
    version: Annotated[Optional[int], Field(ge=1)] = None


class V1ArtifactsArtifactOpenPostResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class V1ArtifactsArtifactVersionsVersionServePostResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class V1ArtifactsArtifactLivePostResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class V1ArtifactsArtifactLiveDeleteResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class File1(BaseModel):
    model_config = ConfigDict(
        extra='allow',
    )
    path: str
    bytes: Annotated[int, Field(description='Exact size.', ge=1)]
    sha256: Annotated[Optional[str], Field(description='Hex; checked on upload.')] = (
        None
    )
    contentType: Annotated[
        Optional[str], Field(description='Default: from the extension.')
    ] = None


class V1UploadsPostRequest(BaseModel):
    model_config = ConfigDict(
        extra='allow',
    )
    files: List[File1]


class V1UploadsPostResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class V1ArtifactsArtifactDataGetResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class V1ArtifactsArtifactDataRowsPostRequest(BaseModel):
    model_config = ConfigDict(
        extra='allow',
    )
    stream: Optional[str] = None
    rows: Annotated[Optional[List[Dict[str, Any]]], Field(max_length=50)] = None
    ops: Annotated[Optional[List[Dict[str, Any]]], Field(max_length=50)] = None
    atomic: Optional[bool] = None


class V1ArtifactsArtifactDataRowsPostResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class V1DataGetResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class Scope(BaseModel):
    model_config = ConfigDict(
        extra='allow',
    )
    series: Optional[str] = None
    datasets: Annotated[Optional[List[str]], Field(max_length=20)] = None
    tags: Annotated[Optional[List[str]], Field(description='All must match.')] = None


class ComputeItem(BaseModel):
    model_config = ConfigDict(
        extra='allow',
    )
    as_: Annotated[str, Field(alias='as')]
    expr: Literal['a * b', 'a / b', 'a + b']
    operands: Annotated[List[str], Field(max_length=2, min_length=2)]
    unit: Optional[str] = None


class GroupBy(RootModel[str]):
    root: Annotated[str, Field(pattern='^field:.+$')]


class Distributions(BaseModel):
    model_config = ConfigDict(
        extra='allow',
    )
    artifact: Annotated[str, Field(description='Artifact id or slug.')]
    version: Annotated[Optional[int], Field(ge=1)] = None
    group_by: Annotated[
        Optional[str], Field(description='A choice, boolean or integer field.')
    ] = None
    bucket: Optional[Literal['day', 'week']] = None


class V1DataQueryPostRequest(BaseModel):
    model_config = ConfigDict(
        extra='allow',
    )
    scope: Annotated[
        Optional[Scope], Field(description='The union of the forms given.')
    ] = None
    measures: Annotated[
        Optional[List[str]],
        Field(
            description='Catalog measure names, not field names.',
            max_length=6,
            min_length=1,
        ),
    ] = None
    agg: Optional[Literal['sum', 'avg', 'min', 'max', 'count', 'last']] = None
    compute: Annotated[
        Optional[List[ComputeItem]],
        Field(
            description='Derived columns, in order; operands name a measure or an earlier `as`.',
            max_length=4,
        ),
    ] = None
    filter: Annotated[
        Optional[List[str]],
        Field(
            description="ANDed 'field op value' clauses: 'reps >= 5', 'day in mon,tue', 'note is set'. Ops: = != > >= < <= in. Catalog fields only.",
            max_length=8,
        ),
    ] = None
    group_by: Annotated[
        Optional[
            List[Union[Literal['dataset', 'day', 'week', 'month', 'visitor'], GroupBy]]
        ],
        Field(
            description='One of dataset, day, week, month, visitor, or "field:{name}".',
            max_length=2,
        ),
    ] = None
    since: Annotated[
        Optional[str], Field(description='ISO-8601 instant or window (7d, 24h).')
    ] = None
    until: Optional[str] = None
    limit: Annotated[Optional[int], Field(ge=1, le=500)] = None
    distributions: Annotated[
        Optional[Distributions],
        Field(
            description="One artifact's per-field distributions instead of a scoped query."
        ),
    ] = None


class V1DataQueryPostResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class V1SchemaGetResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class FieldModel(BaseModel):
    model_config = ConfigDict(
        extra='allow',
    )
    name: str
    type: Annotated[
        str,
        Field(
            description='text long_text rich_text email url phone color integer decimal rating measurement boolean date datetime time choice multi_choice json image video file reference reference_list'
        ),
    ]
    label: Optional[str] = None
    required: Optional[bool] = None
    unique: Optional[bool] = None
    pii: Annotated[
        Literal['none', 'contact', 'sensitive', 'secret'],
        Field(
            description='contact: masked for non-owners. sensitive: encrypted, not queryable. secret: write-only.'
        ),
    ]
    description: Optional[str] = None
    rules: Annotated[
        Optional[Dict[str, Any]],
        Field(
            description='minLength maxLength pattern; min max precision; scale; measure unit; after before; choices minChoices maxChoices; collection onDelete; maxItems; maxBytes.'
        ),
    ] = None


class Define(BaseModel):
    model_config = ConfigDict(
        extra='allow',
    )
    key: Annotated[
        str,
        Field(
            description='Lowercase letters, digits, underscores; starts with a letter.'
        ),
    ]
    name: Annotated[str, Field(description='1–80 chars.')]
    description: Optional[str] = None
    displayField: Annotated[
        Optional[str], Field(description='Labels an entry. Default: first text field.')
    ] = None
    fields: Annotated[List[FieldModel], Field(max_length=60)]


class V1SchemaPutRequest(BaseModel):
    model_config = ConfigDict(
        extra='allow',
    )
    define: Annotated[
        Optional[Define],
        Field(
            description='A content collection definition: creates one, or replaces the one with this key.'
        ),
    ] = None
    workspace: Annotated[
        Optional[str], Field(description='Workspace handle. Omit for your own.')
    ] = None


class V1SchemaPutResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class V1CollectionsCollectionEntriesGetResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class V1CollectionsCollectionEntriesPostRequest(BaseModel):
    model_config = ConfigDict(
        extra='allow',
    )
    values: Annotated[
        Optional[List[Dict[str, Any]]],
        Field(description='Keyed by field name. An array writes a batch.'),
    ] = None
    status: Annotated[
        Optional[Literal['draft', 'published', 'archived']],
        Field(description='Written entries. Default published.'),
    ] = None
    workspace: Annotated[
        Optional[str], Field(description='Workspace handle. Omit for your own.')
    ] = None


class V1CollectionsCollectionEntriesPostResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class Header(BaseModel):
    model_config = ConfigDict(
        extra='allow',
    )
    name: Annotated[str, Field(description='e.g. authorization, x-api-key.')]
    scheme: Annotated[
        Optional[str],
        Field(description='Prefix before the value, e.g. "Bearer ". May be empty.'),
    ] = None


class V1CollectionsCollectionEntriesEntryFieldsFieldUsePostRequest(BaseModel):
    model_config = ConfigDict(
        extra='allow',
    )
    method: Literal['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    url: Annotated[
        str,
        Field(
            description='https only; its host must be the approved one. Redirects are returned, never followed.'
        ),
    ]
    headers: Annotated[
        Optional[Dict[str, str]],
        Field(
            description='Sent as given, except host, authorization, cookie, proxy-* and the grant’s own header.'
        ),
    ] = None
    body: Annotated[Optional[str], Field(description='≤64 KiB.')] = None
    header: Annotated[
        Optional[Header],
        Field(
            description='Where the value goes; asked for when no grant exists. The approved grant’s header wins.'
        ),
    ] = None


class V1CollectionsCollectionEntriesEntryFieldsFieldUsePostResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class V1TemplatesGetResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class UseCase(BaseModel):
    model_config = ConfigDict(
        extra='allow',
    )
    title: Annotated[str, Field(max_length=80)]
    prompt: Annotated[str, Field(max_length=280)]


class Slot(BaseModel):
    model_config = ConfigDict(
        extra='allow',
    )
    name: str
    type: str


class Spec(BaseModel):
    model_config = ConfigDict(
        extra='allow',
    )
    slots: Annotated[
        Optional[List[Slot]],
        Field(
            description='The fill schema, an array: [{"name": "headline", "type": "text", "required": true, "max": 120}].'
        ),
    ] = None


class File2(BaseModel):
    model_config = ConfigDict(
        extra='allow',
    )
    path: str
    text: Annotated[
        Optional[str],
        Field(description='UTF-8 text, base64-ed for you. Send `text` or `content`.'),
    ] = None
    content: Annotated[
        Optional[str], Field(description='Base64 of the bytes, for binaries.')
    ] = None
    contentType: Optional[str] = None


class Companion(BaseModel):
    model_config = ConfigDict(
        extra='allow',
    )
    role: Annotated[str, Field(description='Kebab-case, unique, not "primary".')]
    title: str
    description: Optional[str] = None
    kind: Optional[
        Literal['page', 'slideshow', 'survey', 'tracker', 'video', 'tool', 'dashboard']
    ] = None
    visibility: Annotated[
        Optional[Literal['inherit', 'private', 'public']],
        Field(description='Default inherit: the primary’s.'),
    ] = None
    declaration: Annotated[
        Optional[Dict[str, Any]], Field(description='This part’s policy, or omit.')
    ] = None
    slots: Annotated[
        Optional[List[str]],
        Field(description='Slot names whose values this part gets. Default all.'),
    ] = None
    files: Annotated[
        List[File2],
        Field(
            description='Runtime files, `index.html` required. Omitting them on a revision drops the runtime from that new draft version only.'
        ),
    ]


class V1TemplatesPostRequest(BaseModel):
    model_config = ConfigDict(
        extra='allow',
    )
    slug: Annotated[str, Field(description='Kebab-case, 3–64 chars. Permanent.')]
    title: str
    description: str
    kind: Annotated[
        Optional[
            Literal[
                'page', 'slideshow', 'survey', 'tracker', 'video', 'tool', 'dashboard'
            ]
        ],
        Field(
            description='`dashboard`: a page that mostly shows live data — a label, not a capability.'
        ),
    ] = None
    jobs: Annotated[
        Optional[
            List[
                Literal[
                    'track',
                    'collect',
                    'present',
                    'report',
                    'monitor',
                    'prove',
                    'document',
                    'explain',
                    'plan',
                    'decide',
                    'review',
                    'learn',
                    'prototype',
                    'announce',
                    'compute',
                    'curate',
                    'coordinate',
                    'play',
                ]
            ]
        ],
        Field(
            description='What a person hires it for; the first is primary. Create default: from `kind`.',
            max_length=2,
            min_length=1,
        ),
    ] = None
    audience: Annotated[
        Optional[
            List[
                Literal[
                    'everyone',
                    'engineering',
                    'product',
                    'design',
                    'marketing',
                    'sales',
                    'ops',
                    'people',
                    'finance',
                    'founders',
                    'education',
                    'personal',
                    'community',
                ]
            ]
        ],
        Field(
            description='1–3, or `everyone` alone (the default).',
            max_length=3,
            min_length=1,
        ),
    ] = None
    useCases: Annotated[
        Optional[List[UseCase]],
        Field(
            description='Things to build from it; the build prompt draws on them.',
            max_length=5,
        ),
    ] = None
    installArchetype: Annotated[
        Optional[Literal['scenarios', 'explainer', 'interview']],
        Field(
            description='After install: `scenarios` (default) offers three builds; `explainer` builds one from the sample; `interview` asks three questions first.'
        ),
    ] = None
    installAfter: Annotated[
        Optional[str],
        Field(
            description='Your note, appended to the build prompt as a suggestion.',
            max_length=1500,
        ),
    ] = None
    samplePublic: Annotated[
        Optional[bool],
        Field(description='The sample may appear on the public listing page.'),
    ] = None
    category: Annotated[
        Optional[
            Literal[
                'trackers',
                'surveys',
                'presentations',
                'dashboards',
                'documents',
                'tools',
                'games',
                'other',
            ]
        ],
        Field(description='Deprecated; read as `jobs` when `jobs` is absent.'),
    ] = None
    spec: Annotated[
        Spec,
        Field(
            description='`slots`, `declaration` (every instance’s policy), optional `comments`, `keywords` (searched), `examplePrompts`.'
        ),
    ]
    guidance: Annotated[
        Optional[str], Field(description='Optional notes for whoever fills it.')
    ] = None
    prompt: Annotated[
        Optional[str], Field(description='A prompt a person copies to ask for one.')
    ] = None
    sample: Annotated[
        Optional[Dict[str, Any]],
        Field(description='`{"values": {…}}`, rendered in the preview.'),
    ] = None
    demo: Annotated[
        Optional[str],
        Field(
            description='Slug of your artifact to link as the demo (linked once public). "" clears it.'
        ),
    ] = None
    files: Annotated[
        Optional[List[File2]],
        Field(
            description='Runtime files, `index.html` required. Omitting them on a revision drops the runtime from that new draft version only.'
        ),
    ] = None
    companions: Annotated[
        Optional[List[Companion]],
        Field(
            description='Extra artifacts each publish makes at {slug}-{role}, same values (e.g. a stage for a host). Bind the primary with `source: {artifact: "@primary", streams}`. Released: add, never remove.',
            max_length=3,
        ),
    ] = None
    expectedVersion: Annotated[
        Optional[int],
        Field(
            description='The version you revised. Present: revise. Absent: create.',
            ge=1,
        ),
    ] = None
    changeNote: Annotated[
        Optional[str],
        Field(description='Revisions: one line on why, for the changelog.'),
    ] = None


class V1TemplatesPostResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class V1TemplatesSlugGetResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class V1TemplatesSlugHistoryGetResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class V1TemplatesSlugFeedbackGetResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class V1TemplatesSlugActionsPostRequest(BaseModel):
    model_config = ConfigDict(
        extra='allow',
    )
    action: Literal[
        'install', 'uninstall', 'rate', 'report', 'rollback', 'request_verification'
    ]
    stars: Annotated[Optional[int], Field(ge=1, le=5)] = None
    version: Annotated[Optional[int], Field(ge=1)] = None
    kind: Annotated[
        Optional[
            Literal[
                'spam', 'harmful', 'broken', 'misleading', 'pii', 'copyright', 'other'
            ]
        ],
        Field(description='Report only.'),
    ] = None
    reason: Annotated[
        Optional[str], Field(description='Report only.', max_length=1000)
    ] = None
    confirmedByPerson: Annotated[
        Optional[bool],
        Field(
            description='Install only: true once the person agreed to this public template. Never set it unasked (`permission_required`).'
        ),
    ] = None


class V1TemplatesSlugActionsPostResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class V1TemplatesSlugReleasePostRequest(BaseModel):
    model_config = ConfigDict(
        extra='allow',
    )
    version: Annotated[int, Field(ge=1)]
    visibility: Annotated[
        Optional[Literal['public', 'unlisted', 'workspace']],
        Field(
            description='`unlisted` (default): by slug. `public`: marketplace. `workspace`: team shelf, members only.'
        ),
    ] = None
    demoConsent: Annotated[
        Optional[bool],
        Field(
            description='Default false. Makes the demo artifact, and its data, public.'
        ),
    ] = None
    sampleConsent: Annotated[
        Optional[bool],
        Field(
            description='true: show the sample on the public listing. Omit: unchanged.'
        ),
    ] = None


class V1TemplatesSlugReleasePostResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class V1ProjectsGetResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class V1ProjectsPostRequest(BaseModel):
    model_config = ConfigDict(
        extra='allow',
    )
    title: Annotated[Optional[str], Field(description='≤ 120 chars.')] = None
    artifacts: Annotated[
        Optional[List[str]], Field(description='Artifact ids or slugs, in order.')
    ] = None
    groupLabel: Annotated[
        Optional[str], Field(description='Heading over these artifacts.')
    ] = None
    visibility: Annotated[
        Optional[Literal['private', 'organization', 'public']],
        Field(
            description='organization: anyone at the workspace. Widening over private needs confirm.'
        ),
    ] = None
    rule: Annotated[
        Optional[Dict[str, Any]],
        Field(description='See super_help projects. null: manual.'),
    ] = None
    confirm: Annotated[
        Optional[bool],
        Field(
            description='Needed to delete; also to add a private artifact to a shared project, or widen one holding private ones (`confirm_private`).'
        ),
    ] = None
    workspace: Annotated[
        Optional[str], Field(description='Workspace handle. Omit for your own.')
    ] = None


class V1ProjectsPostResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class V1ProjectsProjectGetResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class Move(BaseModel):
    model_config = ConfigDict(
        extra='allow',
    )
    artifact: Annotated[
        str, Field(description='An artifact id or slug, or an item id.')
    ]
    to: Annotated[int, Field(description='New position; 1 is first.', ge=1)]


class V1ProjectsProjectPatchRequest(BaseModel):
    model_config = ConfigDict(
        extra='allow',
    )
    title: Annotated[Optional[str], Field(description='≤ 120 chars.')] = None
    visibility: Annotated[
        Optional[Literal['private', 'organization', 'public']],
        Field(
            description='organization: anyone at the workspace. Widening over private needs confirm.'
        ),
    ] = None
    order: Annotated[
        Optional[List[str]],
        Field(description='Every item once, in order: ids or slugs.'),
    ] = None
    move: Optional[Move] = None
    rule: Annotated[
        Optional[Dict[str, Any]],
        Field(description='See super_help projects. null: manual.'),
    ] = None
    collapsedGroups: Annotated[
        Optional[List[str]], Field(description='groupLabels shown folded. Whole set.')
    ] = None
    confirm: Annotated[
        Optional[bool],
        Field(
            description='Needed to delete; also to add a private artifact to a shared project, or widen one holding private ones (`confirm_private`).'
        ),
    ] = None
    workspace: Annotated[
        Optional[str], Field(description='Workspace handle. Omit for your own.')
    ] = None


class V1ProjectsProjectPatchResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class V1ProjectsProjectDeleteResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class V1ProjectsProjectArtifactsPostRequest(BaseModel):
    model_config = ConfigDict(
        extra='allow',
    )
    artifacts: Annotated[
        Optional[List[str]], Field(description='Artifact ids or slugs, in order.')
    ] = None
    groupLabel: Annotated[
        Optional[str], Field(description='Heading over these artifacts.')
    ] = None
    confirm: Annotated[
        Optional[bool],
        Field(
            description='Needed to delete; also to add a private artifact to a shared project, or widen one holding private ones (`confirm_private`).'
        ),
    ] = None
    workspace: Annotated[
        Optional[str], Field(description='Workspace handle. Omit for your own.')
    ] = None


class V1ProjectsProjectArtifactsPostResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class V1ProjectsProjectArtifactsRemoveDeleteResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class V1ArtifactsArtifactSharesPostRequest(BaseModel):
    model_config = ConfigDict(
        extra='allow',
    )
    emails: Annotated[List[str], Field(max_length=50, min_length=1)]
    role: Annotated[
        Optional[Literal['viewer', 'commenter', 'editor']],
        Field(
            description="Default viewer; editor for a workspace. An editor's key restores (super_artifact_set version), writes (super_data_write), publishes by slug in its workspace."
        ),
    ] = None
    artifactOnly: Annotated[
        Optional[bool], Field(description='Skip the team invite.')
    ] = None


class V1ArtifactsArtifactSharesPostResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class V1ProjectsProjectSharesPostRequest(BaseModel):
    model_config = ConfigDict(
        extra='allow',
    )
    emails: Annotated[List[str], Field(max_length=50, min_length=1)]
    role: Annotated[
        Optional[Literal['viewer', 'commenter', 'editor']],
        Field(
            description="Default viewer; editor for a workspace. An editor's key restores (super_artifact_set version), writes (super_data_write), publishes by slug in its workspace."
        ),
    ] = None
    confirm: Annotated[
        Optional[bool],
        Field(
            description='Project only: true shares a project that holds private artifacts (`confirm_private`).'
        ),
    ] = None


class V1ProjectsProjectSharesPostResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class V1WorkspaceSharesPostRequest(BaseModel):
    model_config = ConfigDict(
        extra='allow',
    )
    emails: Annotated[List[str], Field(max_length=50, min_length=1)]
    role: Annotated[
        Optional[Literal['viewer', 'commenter', 'editor']],
        Field(
            description="Default viewer; editor for a workspace. An editor's key restores (super_artifact_set version), writes (super_data_write), publishes by slug in its workspace."
        ),
    ] = None
    workspace: Annotated[
        Optional[str], Field(description='A handle you administer, or "" for your own.')
    ] = None


class V1WorkspaceSharesPostResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class V1ArtifactsArtifactCommentsGetResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class RespondItem(BaseModel):
    model_config = ConfigDict(
        extra='allow',
    )
    thread: Annotated[str, Field(description='Thread id, not a message id.')]
    body: Annotated[
        Optional[str], Field(description='Explain the outcome and published version.')
    ] = None
    messageId: Annotated[Optional[str], Field(description='UUID reused on retry.')] = (
        None
    )
    resolve: Annotated[
        Optional[bool], Field(description='true resolves, false reopens.')
    ] = None


class V1ArtifactsArtifactCommentsResponsesPostRequest(BaseModel):
    model_config = ConfigDict(
        extra='allow',
    )
    respond: Annotated[Optional[List[RespondItem]], Field(max_length=20)] = None


class V1ArtifactsArtifactCommentsResponsesPostResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class ReactItem(BaseModel):
    model_config = ConfigDict(
        extra='allow',
    )
    thread: str
    message: str
    emoji: str
    on: Optional[bool] = None


class V1ArtifactsArtifactCommentsReactionsPostRequest(BaseModel):
    model_config = ConfigDict(
        extra='allow',
    )
    react: Annotated[Optional[List[ReactItem]], Field(max_length=20)] = None


class V1ArtifactsArtifactCommentsReactionsPostResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class V1ArtifactsArtifactCommentsResolutionsPostRequest(BaseModel):
    model_config = ConfigDict(
        extra='allow',
    )
    resolve: Annotated[Optional[List[str]], Field(max_length=20)] = None


class V1ArtifactsArtifactCommentsResolutionsPostResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class V1ArtifactsArtifactCommentsScreenshotsScreenshotGetResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class V1MentionsGetResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class V1SignaturesGetResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class Signer(BaseModel):
    model_config = ConfigDict(
        extra='allow',
    )
    name: str
    email: str
    party: Annotated[
        Optional[str], Field(description='Their role in the agreement, e.g. "Tenant".')
    ] = None


class V1SignaturesPostRequest(BaseModel):
    model_config = ConfigDict(
        extra='allow',
    )
    artifact: Annotated[Optional[str], Field(description='Artifact id or slug.')] = None
    version: Annotated[
        Optional[int],
        Field(description='The version to sign. Default: the published one.', ge=1),
    ] = None
    signers: Annotated[Optional[List[Signer]], Field(max_length=10, min_length=1)] = (
        None
    )
    message: Annotated[
        Optional[str],
        Field(description='A note shown to every signer.', max_length=500),
    ] = None


class V1SignaturesPostResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class V1SignaturesRequestGetResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class V1SignaturesRequestRemindPostRequest(BaseModel):
    model_config = ConfigDict(
        extra='allow',
    )
    signer: Annotated[
        Optional[str], Field(description='A signer id, from status. For remind.')
    ] = None


class V1SignaturesRequestRemindPostResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )


class V1SignaturesRequestWithdrawPostResponse(BaseModel):
    pass
    model_config = ConfigDict(
        extra='allow',
    )
