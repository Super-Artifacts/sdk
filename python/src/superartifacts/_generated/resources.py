# Generated from sdks/openapi.json, spec hash 1b1714ff1a47bc8847fe6336951ca06d6d514f2d8567c9b4a8c759cc175b5288. Do not edit.
from __future__ import annotations

from typing import Any, AsyncIterator, Dict, Iterator, List, Literal, Optional

from .._helpers import OMIT, ArtifactHelper, AsyncArtifactHelper, AsyncUploadHelper, UploadHelper
from .._helpers import awalk_cursor, awalk_pages, walk_cursor, walk_pages


class _Resource:
    def __init__(self, client: Any) -> None:
        self._client = client


class Account(_Resource):

    def whoami(
        self,
        *,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Who this key publishes as.

        Who this key publishes as: the workspace `handle`, `email`, `agent` name and `scope`
        (the artifacts it may change: its own, and those it is named Editor on), plus
        `liveRooms` where live rooms run (the limit and who holds one). Useful to confirm where
        a publish lands, or why an artifact answers `not_found`; no other tool needs it.
        """
        return self._client._call(
            "GET",
            "/v1/whoami",
            timeout=timeout,
        )

    def help(
        self,
        *,
        topic: Optional[Literal["tools", "data", "templates", "collections", "projects", "batch"]] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """How the operations fit together.

        Plain-text notes for when it is unclear which tool, data store or argument shape does a
        job. Topics: `tools` (a line per tool), `data` (which store a page needs and how the
        page writes to it), `templates` (finding, building from, drafting, releasing),
        `collections` (content models and field types), `projects` (creating, ordering, sharing,
        rules), `batch` (what each tool takes in one call). Without `topic`: the full topic
        list, which names two more reached from results. Answers `{topic, text}`; not needed
        when a tool’s own description answers the question.
        """
        return self._client._call(
            "GET",
            "/v1/help",
            query={"topic": topic},
            timeout=timeout,
        )


class Artifacts(ArtifactHelper, _Resource):

    def list(
        self,
        *,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """List your artifacts, newest first.

        Without `artifact`: your artifacts, newest first, with URLs and `live`. With `artifact`:
        its versions, which is published, their paths, and `declaration` (the published policy).
        Add `path` or `version` to read that file as text (default: published index.html); non-
        text or over 300,000 bytes: refused. `open: true` (with `artifact`, optional `version`)
        returns `url` and `expiresAt`: load `url` to see the artifact as a viewer, private
        included, for 10 minutes; visibility is unchanged, the URL opens only that artifact,
        60/key/hour (`rate_limited`). Changing what an artifact serves, or who can open it, is
        super_artifact_set.
        """
        return self._client._call(
            "GET",
            "/v1/artifacts",
            timeout=timeout,
        )

    def publish(
        self,
        *,
        slug: str,
        prompt: Optional[str] = None,
        html: Optional[str] = None,
        values: Optional[Dict[str, Any]] = None,
        instances: Optional[List[Dict[str, Any]]] = None,
        template: Optional[Dict[str, Any]] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        kind: Optional[Literal["page", "slideshow", "survey", "tracker", "video", "tool", "dashboard"]] = None,
        collection: Optional[str] = None,
        visibility: Optional[Literal["private", "organization"]] = None,
        policy: Optional[Dict[str, Any]] = None,
        dataset: Optional[str] = None,
        continues: Optional[str] = None,
        uploads: Optional[str] = None,
        values_file: Optional[str] = None,
        files: Optional[List[Dict[str, Any]]] = None,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Publish an artifact, or a new version of one.

        Publish a page at a stable URL; the same slug adds a new version, which the URL serves
        at once. Earlier versions stay and can be served again; nothing that existed before the
        call is deleted. Always give the person the url from the result, even on updates. Send
        `html`, or `values` for a template that carries a runtime, not both. Without `policy` a
        form, input or saved state stores nothing; CMS rows a page edits go in
        `policy.collections`. When retained storage is full it refuses with `plan_limit` and
        deletes nothing. A template becomes everybody’s through a release, not a publish.
        """
        return self._client._call(
            "POST",
            "/v1/artifacts",
            body={"slug": slug, "prompt": prompt, "html": html, "values": values, "instances": instances, "template": template, "title": title, "description": description, "kind": kind, "collection": collection, "visibility": visibility, "policy": policy, "dataset": dataset, "continues": continues, "uploads": uploads, "valuesFile": values_file, "files": files},
            idempotency_key=idempotency_key,
            timeout=timeout,
        )

    def get(
        self,
        *,
        artifact: str,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """One artifact: its versions, published version and declaration.

        Without `artifact`: your artifacts, newest first, with URLs and `live`. With `artifact`:
        its versions, which is published, their paths, and `declaration` (the published policy).
        Add `path` or `version` to read that file as text (default: published index.html); non-
        text or over 300,000 bytes: refused. `open: true` (with `artifact`, optional `version`)
        returns `url` and `expiresAt`: load `url` to see the artifact as a viewer, private
        included, for 10 minutes; visibility is unchanged, the URL opens only that artifact,
        60/key/hour (`rate_limited`). Changing what an artifact serves, or who can open it, is
        super_artifact_set.
        """
        return self._client._call(
            "GET",
            "/v1/artifacts/{artifact}",
            path_params={"artifact": artifact},
            timeout=timeout,
        )

    def update(
        self,
        *,
        artifact: str,
        visibility: Optional[Literal["private", "organization", "public"]] = None,
        collection: Optional[str] = None,
        phase: Optional[str] = None,
        notify_on_submission: Optional[bool] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Change visibility, gallery label, live phase or submission email.

        Change one artifact. `version` serves an existing version (a pointer move; nothing
        rebuilt or deleted). `live` turns its live room on or off; off disconnects every
        visitor, and Free has one room at a time. `notifyOnSubmission` emails you for each new
        data submission (default off; edits send nothing; no answers in the mail). `phase` sets
        the live room’s phase. `visibility` widens or narrows who can open it; narrowing voids
        every viewer grant already issued, so each viewer is checked again. `collection` sets
        its gallery grouping label. `delete` removes the artifact with every version, share link
        and response, permanently; it needs `confirm: true` and goes alone. Fields apply in that
        order, and a refusal part-way names the ones already `applied`. Publishing a new version
        is super_publish.
        """
        return self._client._call(
            "PATCH",
            "/v1/artifacts/{artifact}",
            path_params={"artifact": artifact},
            body={"visibility": visibility, "collection": collection, "phase": phase, "notifyOnSubmission": notify_on_submission},
            timeout=timeout,
        )

    def delete(
        self,
        *,
        artifact: str,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Delete an artifact with every version, permanently.

        Change one artifact. `version` serves an existing version (a pointer move; nothing
        rebuilt or deleted). `live` turns its live room on or off; off disconnects every
        visitor, and Free has one room at a time. `notifyOnSubmission` emails you for each new
        data submission (default off; edits send nothing; no answers in the mail). `phase` sets
        the live room’s phase. `visibility` widens or narrows who can open it; narrowing voids
        every viewer grant already issued, so each viewer is checked again. `collection` sets
        its gallery grouping label. `delete` removes the artifact with every version, share link
        and response, permanently; it needs `confirm: true` and goes alone. Fields apply in that
        order, and a refusal part-way names the ones already `applied`. Publishing a new version
        is super_publish.
        """
        return self._client._call(
            "DELETE",
            "/v1/artifacts/{artifact}",
            path_params={"artifact": artifact},
            query={"confirm": artifact},
            timeout=timeout,
        )

    def read_file(
        self,
        *,
        artifact: str,
        path: Optional[str] = None,
        version: Optional[int] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Read one file of a version as text (default: the published index.html).

        Without `artifact`: your artifacts, newest first, with URLs and `live`. With `artifact`:
        its versions, which is published, their paths, and `declaration` (the published policy).
        Add `path` or `version` to read that file as text (default: published index.html); non-
        text or over 300,000 bytes: refused. `open: true` (with `artifact`, optional `version`)
        returns `url` and `expiresAt`: load `url` to see the artifact as a viewer, private
        included, for 10 minutes; visibility is unchanged, the URL opens only that artifact,
        60/key/hour (`rate_limited`). Changing what an artifact serves, or who can open it, is
        super_artifact_set.
        """
        return self._client._call(
            "GET",
            "/v1/artifacts/{artifact}/file",
            path_params={"artifact": artifact},
            query={"path": path, "version": version},
            timeout=timeout,
        )

    def open(
        self,
        *,
        artifact: str,
        version: Optional[int] = None,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """A ten-minute viewer URL for an artifact, private included.

        Without `artifact`: your artifacts, newest first, with URLs and `live`. With `artifact`:
        its versions, which is published, their paths, and `declaration` (the published policy).
        Add `path` or `version` to read that file as text (default: published index.html); non-
        text or over 300,000 bytes: refused. `open: true` (with `artifact`, optional `version`)
        returns `url` and `expiresAt`: load `url` to see the artifact as a viewer, private
        included, for 10 minutes; visibility is unchanged, the URL opens only that artifact,
        60/key/hour (`rate_limited`). Changing what an artifact serves, or who can open it, is
        super_artifact_set.
        """
        return self._client._call(
            "POST",
            "/v1/artifacts/{artifact}/open",
            path_params={"artifact": artifact},
            body={"version": version},
            idempotency_key=idempotency_key,
            timeout=timeout,
        )

    def serve_version(
        self,
        *,
        artifact: str,
        version: int,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Serve an existing version again.

        Change one artifact. `version` serves an existing version (a pointer move; nothing
        rebuilt or deleted). `live` turns its live room on or off; off disconnects every
        visitor, and Free has one room at a time. `notifyOnSubmission` emails you for each new
        data submission (default off; edits send nothing; no answers in the mail). `phase` sets
        the live room’s phase. `visibility` widens or narrows who can open it; narrowing voids
        every viewer grant already issued, so each viewer is checked again. `collection` sets
        its gallery grouping label. `delete` removes the artifact with every version, share link
        and response, permanently; it needs `confirm: true` and goes alone. Fields apply in that
        order, and a refusal part-way names the ones already `applied`. Publishing a new version
        is super_publish.
        """
        return self._client._call(
            "POST",
            "/v1/artifacts/{artifact}/versions/{version}/serve",
            path_params={"artifact": artifact, "version": version},
            idempotency_key=idempotency_key,
            timeout=timeout,
        )


class Live(_Resource):

    def start(
        self,
        *,
        artifact: str,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Turn an artifact's live room on.

        Change one artifact. `version` serves an existing version (a pointer move; nothing
        rebuilt or deleted). `live` turns its live room on or off; off disconnects every
        visitor, and Free has one room at a time. `notifyOnSubmission` emails you for each new
        data submission (default off; edits send nothing; no answers in the mail). `phase` sets
        the live room’s phase. `visibility` widens or narrows who can open it; narrowing voids
        every viewer grant already issued, so each viewer is checked again. `collection` sets
        its gallery grouping label. `delete` removes the artifact with every version, share link
        and response, permanently; it needs `confirm: true` and goes alone. Fields apply in that
        order, and a refusal part-way names the ones already `applied`. Publishing a new version
        is super_publish.
        """
        return self._client._call(
            "POST",
            "/v1/artifacts/{artifact}/live",
            path_params={"artifact": artifact},
            idempotency_key=idempotency_key,
            timeout=timeout,
        )

    def stop(
        self,
        *,
        artifact: str,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Turn an artifact's live room off, disconnecting every visitor.

        Change one artifact. `version` serves an existing version (a pointer move; nothing
        rebuilt or deleted). `live` turns its live room on or off; off disconnects every
        visitor, and Free has one room at a time. `notifyOnSubmission` emails you for each new
        data submission (default off; edits send nothing; no answers in the mail). `phase` sets
        the live room’s phase. `visibility` widens or narrows who can open it; narrowing voids
        every viewer grant already issued, so each viewer is checked again. `collection` sets
        its gallery grouping label. `delete` removes the artifact with every version, share link
        and response, permanently; it needs `confirm: true` and goes alone. Fields apply in that
        order, and a refusal part-way names the ones already `applied`. Publishing a new version
        is super_publish.
        """
        return self._client._call(
            "DELETE",
            "/v1/artifacts/{artifact}/live",
            path_params={"artifact": artifact},
            timeout=timeout,
        )


class Uploads(UploadHelper, _Resource):

    def stage(
        self,
        *,
        files: List[Dict[str, Any]],
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Stage big files for a publish; PUT each to its URL.

        Stage images, video or big files for a publish without sending their bytes in a call.
        Declare each file’s `path` and exact `bytes`; the result carries an `uploadId` and one
        `url` per file. PUT each file to its URL (`curl -T`, no credentials), then super_publish
        with `uploads`. Not index.html: that is `html`; small assets can ride inline as the
        publish’s `files`. Same limits as `files`; a staged set expires after 30 minutes, and at
        most 5 wait unpublished at once.
        """
        return self._client._call(
            "POST",
            "/v1/uploads",
            body={"files": files},
            idempotency_key=idempotency_key,
            timeout=timeout,
        )


class Data(_Resource):

    def list_artifact_rows(
        self,
        *,
        artifact: str,
        filter: Optional[List[str]] = None,
        since: Optional[str] = None,
        until: Optional[str] = None,
        sort: Optional[Literal["newest", "oldest"]] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        fields: Optional[List[str]] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Rows visitors submitted to one artifact, newest first.

        The rows visitors submitted to your artifacts, newest first, with each version's field
        schema; paged by `cursor`. Address exactly one: `artifact`; `dataset` (a catalog key;
        one shared by several artifacts is `ambiguous_dataset`); or `collection`, the gallery
        grouping label set at publish, not a content collection (≤20 artifacts over one window,
        kept per artifact, no `filter`). Entries of a content collection are super_entries;
        totals and averages are a query, not a read.
        """
        return self._client._call(
            "GET",
            "/v1/artifacts/{artifact}/data",
            path_params={"artifact": artifact},
            query={"filter": filter, "since": since, "until": until, "sort": sort, "limit": limit, "cursor": cursor, "fields": fields},
            timeout=timeout,
        )

    def iter_artifact_rows(self, **kwargs: Any) -> Iterator[Dict[str, Any]]:
        """Every item of `list_artifact_rows`, across pages. Takes the same arguments."""
        return walk_cursor(self.list_artifact_rows, "responses", kwargs)

    def write_artifact_rows(
        self,
        *,
        artifact: str,
        stream: Optional[str] = None,
        rows: Optional[List[Dict[str, Any]]] = None,
        ops: Optional[List[Dict[str, Any]]] = None,
        atomic: Optional[bool] = None,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Write rows into an artifact you may edit.

        Write rows into an artifact this key may edit, through the validation and stream rules a
        page write gets; each row is attributed "<agent> (agent)". `rows` creates in `stream`.
        `ops` [{op: create|replace|delete, id, row, stream}] replaces or deletes only rows this
        agent wrote (writes: upsert); a deleted row cannot be restored by any tool. ≤50 a call;
        `atomic`: all or none, otherwise a partial batch answers `complete: false`. Visitor rows
        are never changed here; entries of a content collection are super_entries.
        """
        return self._client._call(
            "POST",
            "/v1/artifacts/{artifact}/data/rows",
            path_params={"artifact": artifact},
            body={"stream": stream, "rows": rows, "ops": ops, "atomic": atomic},
            idempotency_key=idempotency_key,
            timeout=timeout,
        )

    def list_rows(
        self,
        *,
        dataset: Optional[str] = None,
        collection: Optional[str] = None,
        filter: Optional[List[str]] = None,
        since: Optional[str] = None,
        until: Optional[str] = None,
        sort: Optional[Literal["newest", "oldest"]] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        fields: Optional[List[str]] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Rows submitted to a dataset or a gallery label.

        The rows visitors submitted to your artifacts, newest first, with each version's field
        schema; paged by `cursor`. Address exactly one: `artifact`; `dataset` (a catalog key;
        one shared by several artifacts is `ambiguous_dataset`); or `collection`, the gallery
        grouping label set at publish, not a content collection (≤20 artifacts over one window,
        kept per artifact, no `filter`). Entries of a content collection are super_entries;
        totals and averages are a query, not a read.
        """
        return self._client._call(
            "GET",
            "/v1/data",
            query={"dataset": dataset, "collection": collection, "filter": filter, "since": since, "until": until, "sort": sort, "limit": limit, "cursor": cursor, "fields": fields},
            timeout=timeout,
        )

    def iter_rows(self, **kwargs: Any) -> Iterator[Dict[str, Any]]:
        """Every item of `list_rows`, across pages. Takes the same arguments."""
        return walk_cursor(self.list_rows, "responses", kwargs)

    def query(
        self,
        *,
        scope: Optional[Dict[str, Any]] = None,
        measures: Optional[List[str]] = None,
        agg: Optional[Literal["sum", "avg", "min", "max", "count", "last"]] = None,
        compute: Optional[List[Dict[str, Any]]] = None,
        filter: Optional[List[str]] = None,
        group_by: Optional[List[str]] = None,
        since: Optional[str] = None,
        until: Optional[str] = None,
        limit: Optional[int] = None,
        distributions: Optional[Dict[str, Any]] = None,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Aggregate what was collected: numbers, never rows.

        Numbers over what was collected, never rows (rows are super_data). Aggregate `measures`
        across the datasets in `scope`; datasets combine on the same measure in one base unit,
        results in the declared `unit`. Names come from the catalog; an unknown one errors with
        near misses. The answer has one row per `group_by` key (or one row) with a column per
        measure and `compute`, the datasets used and any skipped, and `truncated` when `limit`
        cut it. Or send `distributions` for one artifact: counts, per-version rates and per-
        field distributions (free text: answer rate and length only). A call with neither is
        `invalid_query`.
        """
        return self._client._call(
            "POST",
            "/v1/data/query",
            body={"scope": scope, "measures": measures, "agg": agg, "compute": compute, "filter": filter, "group_by": group_by, "since": since, "until": until, "limit": limit, "distributions": distributions},
            idempotency_key=idempotency_key,
            timeout=timeout,
        )


class Schema(_Resource):

    def get(
        self,
        *,
        series: Optional[str] = None,
        tags: Optional[List[str]] = None,
        artifact: Optional[str] = None,
        compare: Optional[List[str]] = None,
        since: Optional[str] = None,
        workspace: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """The data catalog: datasets and content collections, or a comparison.

        The data catalog, without rows. Read (the default): `datasets` your artifacts declared,
        with fields, units, measures and `since`/`deprecated` versions, and this workspace's
        content `collections`, with fields, rules and entry counts. `compare` (alone): two to
        ten artifacts' newest fields side by side, every type, unit and measure conflict named.
        `define` creates a content collection, or replaces the one with that `key` outright,
        name, display field and every field; a field left out is gone from the model, and a
        collection an artifact declared is refused with `conflict`. Refusals name field, rule
        and fix. Rows an artifact collected are super_data.
        """
        return self._client._call(
            "GET",
            "/v1/schema",
            query={"series": series, "tags": tags, "artifact": artifact, "compare": compare, "since": since, "workspace": workspace},
            timeout=timeout,
        )

    def define_collection(
        self,
        *,
        define: Optional[Dict[str, Any]] = None,
        workspace: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Create or replace a content collection.

        The data catalog, without rows. Read (the default): `datasets` your artifacts declared,
        with fields, units, measures and `since`/`deprecated` versions, and this workspace's
        content `collections`, with fields, rules and entry counts. `compare` (alone): two to
        ten artifacts' newest fields side by side, every type, unit and measure conflict named.
        `define` creates a content collection, or replaces the one with that `key` outright,
        name, display field and every field; a field left out is gone from the model, and a
        collection an artifact declared is refused with `conflict`. Refusals name field, rule
        and fix. Rows an artifact collected are super_data.
        """
        return self._client._call(
            "PUT",
            "/v1/schema",
            body={"define": define, "workspace": workspace},
            timeout=timeout,
        )


class Entries(_Resource):

    def list(
        self,
        *,
        collection: str,
        workspace: Optional[str] = None,
        filter: Optional[List[str]] = None,
        search: Optional[str] = None,
        sort: Optional[str] = None,
        direction: Optional[Literal["asc", "desc"]] = None,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        if_none_match: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """One page of a content collection's entries.

        Entries of a workspace content collection (a model defined in the catalog), not rows an
        artifact collected. With `values`: create one entry (an object) or up to 50 (an array,
        one outcome per row); values are coerced to declared types, undeclared fields are
        refused by name, and nothing existing is updated or deleted. Without: read one page,
        filtered and sorted in the database; references resolve to labels, sensitive fields read
        as answered-or-not. Rows visitors submitted are super_data.
        """
        return self._client._call(
            "GET",
            "/v1/collections/{collection}/entries",
            headers={"If-None-Match": if_none_match},
            path_params={"collection": collection},
            query={"workspace": workspace, "filter": filter, "search": search, "sort": sort, "direction": direction, "page": page, "limit": limit},
            timeout=timeout,
        )

    def iter(self, **kwargs: Any) -> Iterator[Dict[str, Any]]:
        """Every item of `list`, across pages. Takes the same arguments."""
        return walk_pages(self.list, "entries", kwargs)

    def create(
        self,
        *,
        collection: str,
        values: Optional[Any] = None,
        status: Optional[Literal["draft", "published", "archived"]] = None,
        workspace: Optional[str] = None,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Create one entry, or a batch.

        Entries of a workspace content collection (a model defined in the catalog), not rows an
        artifact collected. With `values`: create one entry (an object) or up to 50 (an array,
        one outcome per row); values are coerced to declared types, undeclared fields are
        refused by name, and nothing existing is updated or deleted. Without: read one page,
        filtered and sorted in the database; references resolve to labels, sensitive fields read
        as answered-or-not. Rows visitors submitted are super_data.
        """
        return self._client._call(
            "POST",
            "/v1/collections/{collection}/entries",
            path_params={"collection": collection},
            body={"values": values, "status": status, "workspace": workspace},
            idempotency_key=idempotency_key,
            timeout=timeout,
        )


class Secrets(_Resource):

    def use(
        self,
        *,
        collection: str,
        entry: str,
        field: str,
        method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"],
        url: str,
        headers: Optional[Dict[str, Any]] = None,
        body: Optional[str] = None,
        header: Optional[Dict[str, Any]] = None,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Call an approved API with a stored secret you cannot read (workspace keys).

        Make one HTTPS request with a `pii: secret` value from a content collection entry. The
        platform puts the value into one header and calls the one host a person approved; you
        get status, headers and body, scrubbed of it. You never see it, in input or result; a
        response echoing it is withheld whole (`secret_echoed`). A first request for a field and
        host answers `approval_required` with `approvalUrl`: give the person that link, then
        repeat the request once they approve. Grants expire, cap uses and can be revoked; every
        use is logged. The person types the secret into its dashboard entry; super_entries
        writes one only if they insist on pasting it.
        """
        return self._client._call(
            "POST",
            "/v1/collections/{collection}/entries/{entry}/fields/{field}/use",
            path_params={"collection": collection, "entry": entry, "field": field},
            body={"method": method, "url": url, "headers": headers, "body": body, "header": header},
            idempotency_key=idempotency_key,
            timeout=timeout,
        )


class Templates(_Resource):

    def list(
        self,
        *,
        request: Optional[str] = None,
        scope: Optional[Literal["installed", "marketplace"]] = None,
        kind: Optional[Literal["page", "slideshow", "survey", "tracker", "video", "tool", "dashboard"]] = None,
        sort: Optional[Literal["relevance", "rating", "uses", "installs", "recent"]] = None,
        limit: Optional[int] = None,
        jobs: Optional[List[Literal["track", "collect", "present", "report", "monitor", "prove", "document", "explain", "plan", "decide", "review", "learn", "prototype", "announce", "compute", "curate", "coordinate", "play"]]] = None,
        audience: Optional[List[Literal["everyone", "engineering", "product", "design", "marketing", "sales", "ops", "people", "finance", "founders", "education", "personal", "community"]]] = None,
        needs: Optional[List[Literal["runtime", "data", "comments", "live"]]] = None,
        cost: Optional[Literal["fill", "write", "build"]] = None,
        tier: Optional[Literal["all", "official", "verified", "community"]] = None,
        mine: Optional[bool] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Find, rank or list templates.

        With `request`: rank installed templates by content similarity; matches carry `band`
        (high: build from it; possible: judge it), `why` and unscored stats. `scope:
        marketplace`: released public templates, ranked by `request` or else the top by `sort`;
        `sort`, `limit` and the facets apply only here. Neither: the installed list. `slug`: one
        template in full, with its `installPrompt`; `history`: its changelog; `feedback`: its
        artifacts' comments as themes. `mine`: your published templates, with counts. Reading
        only: installing, rating and rolling back are super_template_action.
        """
        return self._client._call(
            "GET",
            "/v1/templates",
            query={"request": request, "scope": scope, "kind": kind, "sort": sort, "limit": limit, "jobs": jobs, "audience": audience, "needs": needs, "cost": cost, "tier": tier, "mine": mine},
            timeout=timeout,
        )

    def save(
        self,
        *,
        slug: str,
        title: str,
        description: str,
        spec: Dict[str, Any],
        kind: Optional[Literal["page", "slideshow", "survey", "tracker", "video", "tool", "dashboard"]] = None,
        jobs: Optional[List[Literal["track", "collect", "present", "report", "monitor", "prove", "document", "explain", "plan", "decide", "review", "learn", "prototype", "announce", "compute", "curate", "coordinate", "play"]]] = None,
        audience: Optional[List[Literal["everyone", "engineering", "product", "design", "marketing", "sales", "ops", "people", "finance", "founders", "education", "personal", "community"]]] = None,
        use_cases: Optional[List[Dict[str, Any]]] = None,
        install_archetype: Optional[Literal["scenarios", "explainer", "interview"]] = None,
        install_after: Optional[str] = None,
        sample_public: Optional[bool] = None,
        category: Optional[Literal["trackers", "surveys", "presentations", "dashboards", "documents", "tools", "games", "other"]] = None,
        guidance: Optional[str] = None,
        prompt: Optional[str] = None,
        sample: Optional[Dict[str, Any]] = None,
        demo: Optional[str] = None,
        files: Optional[List[Dict[str, Any]]] = None,
        companions: Optional[List[Dict[str, Any]]] = None,
        expected_version: Optional[int] = None,
        change_note: Optional[str] = None,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Create or revise a template draft.

        Write a template draft only you can publish from. Without `expectedVersion` it creates
        (refused if the slug exists); with it, it revises the head (refused if the head moved
        past it), and a revision that changes nothing cuts no version. A `json` slot needs
        `schema`. Runtime `files` (≤512 KiB decoded) need a `json` slot and an index.html with
        one `<script id="sa-template-values" type="application/json">`. Others build from it
        only once super_release_template releases it; a revision never changes a released
        version.
        """
        return self._client._call(
            "POST",
            "/v1/templates",
            body={"slug": slug, "title": title, "description": description, "kind": kind, "jobs": jobs, "audience": audience, "useCases": use_cases, "installArchetype": install_archetype, "installAfter": install_after, "samplePublic": sample_public, "category": category, "spec": spec, "guidance": guidance, "prompt": prompt, "sample": sample, "demo": demo, "files": files, "companions": companions, "expectedVersion": expected_version, "changeNote": change_note},
            idempotency_key=idempotency_key,
            timeout=timeout,
        )

    def get(
        self,
        *,
        slug: str,
        version: Optional[int] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """One template in full, with its install prompt.

        With `request`: rank installed templates by content similarity; matches carry `band`
        (high: build from it; possible: judge it), `why` and unscored stats. `scope:
        marketplace`: released public templates, ranked by `request` or else the top by `sort`;
        `sort`, `limit` and the facets apply only here. Neither: the installed list. `slug`: one
        template in full, with its `installPrompt`; `history`: its changelog; `feedback`: its
        artifacts' comments as themes. `mine`: your published templates, with counts. Reading
        only: installing, rating and rolling back are super_template_action.
        """
        return self._client._call(
            "GET",
            "/v1/templates/{slug}",
            path_params={"slug": slug},
            query={"version": version},
            timeout=timeout,
        )

    def get_history(
        self,
        *,
        slug: str,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """A template's changelog.

        With `request`: rank installed templates by content similarity; matches carry `band`
        (high: build from it; possible: judge it), `why` and unscored stats. `scope:
        marketplace`: released public templates, ranked by `request` or else the top by `sort`;
        `sort`, `limit` and the facets apply only here. Neither: the installed list. `slug`: one
        template in full, with its `installPrompt`; `history`: its changelog; `feedback`: its
        artifacts' comments as themes. `mine`: your published templates, with counts. Reading
        only: installing, rating and rolling back are super_template_action.
        """
        return self._client._call(
            "GET",
            "/v1/templates/{slug}/history",
            path_params={"slug": slug},
            timeout=timeout,
        )

    def get_feedback(
        self,
        *,
        slug: str,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Comments on a template's artifacts, as themes.

        With `request`: rank installed templates by content similarity; matches carry `band`
        (high: build from it; possible: judge it), `why` and unscored stats. `scope:
        marketplace`: released public templates, ranked by `request` or else the top by `sort`;
        `sort`, `limit` and the facets apply only here. Neither: the installed list. `slug`: one
        template in full, with its `installPrompt`; `history`: its changelog; `feedback`: its
        artifacts' comments as themes. `mine`: your published templates, with counts. Reading
        only: installing, rating and rolling back are super_template_action.
        """
        return self._client._call(
            "GET",
            "/v1/templates/{slug}/feedback",
            path_params={"slug": slug},
            timeout=timeout,
        )

    def act(
        self,
        *,
        slug: str,
        action: Literal["install", "uninstall", "rate", "report", "rollback", "request_verification"],
        stars: Optional[int] = None,
        version: Optional[int] = None,
        kind: Optional[Literal["spam", "harmful", "broken", "misleading", "pii", "copyright", "other"]] = None,
        reason: Optional[str] = None,
        confirmed_by_person: Optional[bool] = None,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Install, uninstall, rate, report, roll back or request verification.

        Act on one template; nothing here deletes a template, a version or a built artifact.
        `install`/`uninstall`: this workspace's installed set (uninstall removes only the
        install; built artifacts keep working); `install` returns its build prompt as
        `nextStep`. `rate`: the person's 1–5 `stars` on an installed template not yours
        (`cannot_rate_own`, `not_installed`, `rate_limited`); counts once this workspace built
        from it. `report`: `kind` and a `reason` (≤1000 chars) for a moderator; one per account;
        enough reports hide it. `rollback`: restore `version` as a new version, unless the
        runtime changed. `request_verification`: a moderator checks your released `version`; 3
        per 30 days. Finding and reading templates is super_templates.
        """
        return self._client._call(
            "POST",
            "/v1/templates/{slug}/actions",
            path_params={"slug": slug},
            body={"action": action, "stars": stars, "version": version, "kind": kind, "reason": reason, "confirmedByPerson": confirmed_by_person},
            idempotency_key=idempotency_key,
            timeout=timeout,
        )

    def release(
        self,
        *,
        slug: str,
        version: int,
        visibility: Optional[Literal["public", "unlisted", "workspace"]] = None,
        demo_consent: Optional[bool] = None,
        sample_consent: Optional[bool] = None,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Release one version of your template.

        Release one version of your template so others can build from it, live at once to the
        reach `visibility` sets; the result names its trust `tier` (Official, Verified or
        Community). Forward only (`release_moves_backwards`): earlier versions stay, and nothing
        is deleted. A private demo needs `demoConsent: true`. A runtime, prompt, parts or data
        change leaves a Verified badge behind. Public: account 7 days old (`publisher_too_new`),
        10/day, 3/template/hour (`rate_limited`), 20 templates (`too_many_templates`), no tier
        words (`reserved_wording`), no credential (`secret_in_template`), paid plan
        (`plan_required`). Writing the draft is super_template_save.
        """
        return self._client._call(
            "POST",
            "/v1/templates/{slug}/release",
            path_params={"slug": slug},
            body={"version": version, "visibility": visibility, "demoConsent": demo_consent, "sampleConsent": sample_consent},
            idempotency_key=idempotency_key,
            timeout=timeout,
        )


class Projects(_Resource):

    def list(
        self,
        *,
        workspace: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Your projects.

        A project is an ordered set of your artifacts shown one at a time at /s/{slug}, with its
        own audience and share list. No `project`: `title` creates one (seeded from
        `artifacts`), else list yours. With `project`: add `artifacts`, `remove` one, `title`
        renames, set `visibility`, `order`/`move` reorder, a `rule` adds matches as they are
        published, or read it. `delete` with `confirm: true` removes the project, its order and
        its share list permanently; its artifacts stay. One change per call, or title with
        visibility. An artifact's gallery label is not a project: that is `collection` on
        super_artifact_set.
        """
        return self._client._call(
            "GET",
            "/v1/projects",
            query={"workspace": workspace},
            timeout=timeout,
        )

    def create(
        self,
        *,
        title: Optional[str] = None,
        artifacts: Optional[List[str]] = None,
        group_label: Optional[str] = None,
        visibility: Optional[Literal["private", "organization", "public"]] = None,
        rule: Any = OMIT,
        confirm: Optional[bool] = None,
        workspace: Optional[str] = None,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Create a project, optionally seeded with artifacts.

        A project is an ordered set of your artifacts shown one at a time at /s/{slug}, with its
        own audience and share list. No `project`: `title` creates one (seeded from
        `artifacts`), else list yours. With `project`: add `artifacts`, `remove` one, `title`
        renames, set `visibility`, `order`/`move` reorder, a `rule` adds matches as they are
        published, or read it. `delete` with `confirm: true` removes the project, its order and
        its share list permanently; its artifacts stay. One change per call, or title with
        visibility. An artifact's gallery label is not a project: that is `collection` on
        super_artifact_set.
        """
        return self._client._call(
            "POST",
            "/v1/projects",
            body={"title": title, "artifacts": artifacts, "groupLabel": group_label, "visibility": visibility, "confirm": confirm, "workspace": workspace},
            nullable={"rule": rule},
            idempotency_key=idempotency_key,
            timeout=timeout,
        )

    def get(
        self,
        *,
        project: str,
        workspace: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """One project and its items.

        A project is an ordered set of your artifacts shown one at a time at /s/{slug}, with its
        own audience and share list. No `project`: `title` creates one (seeded from
        `artifacts`), else list yours. With `project`: add `artifacts`, `remove` one, `title`
        renames, set `visibility`, `order`/`move` reorder, a `rule` adds matches as they are
        published, or read it. `delete` with `confirm: true` removes the project, its order and
        its share list permanently; its artifacts stay. One change per call, or title with
        visibility. An artifact's gallery label is not a project: that is `collection` on
        super_artifact_set.
        """
        return self._client._call(
            "GET",
            "/v1/projects/{project}",
            path_params={"project": project},
            query={"workspace": workspace},
            timeout=timeout,
        )

    def update(
        self,
        *,
        project: str,
        title: Optional[str] = None,
        visibility: Optional[Literal["private", "organization", "public"]] = None,
        order: Optional[List[str]] = None,
        move: Optional[Dict[str, Any]] = None,
        rule: Any = OMIT,
        collapsed_groups: Optional[List[str]] = None,
        confirm: Optional[bool] = None,
        workspace: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Rename, set visibility, reorder, move, fold groups or set a rule.

        A project is an ordered set of your artifacts shown one at a time at /s/{slug}, with its
        own audience and share list. No `project`: `title` creates one (seeded from
        `artifacts`), else list yours. With `project`: add `artifacts`, `remove` one, `title`
        renames, set `visibility`, `order`/`move` reorder, a `rule` adds matches as they are
        published, or read it. `delete` with `confirm: true` removes the project, its order and
        its share list permanently; its artifacts stay. One change per call, or title with
        visibility. An artifact's gallery label is not a project: that is `collection` on
        super_artifact_set.
        """
        return self._client._call(
            "PATCH",
            "/v1/projects/{project}",
            path_params={"project": project},
            body={"title": title, "visibility": visibility, "order": order, "move": move, "collapsedGroups": collapsed_groups, "confirm": confirm, "workspace": workspace},
            nullable={"rule": rule},
            timeout=timeout,
        )

    def delete(
        self,
        *,
        project: str,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Delete a project; its artifacts stay.

        A project is an ordered set of your artifacts shown one at a time at /s/{slug}, with its
        own audience and share list. No `project`: `title` creates one (seeded from
        `artifacts`), else list yours. With `project`: add `artifacts`, `remove` one, `title`
        renames, set `visibility`, `order`/`move` reorder, a `rule` adds matches as they are
        published, or read it. `delete` with `confirm: true` removes the project, its order and
        its share list permanently; its artifacts stay. One change per call, or title with
        visibility. An artifact's gallery label is not a project: that is `collection` on
        super_artifact_set.
        """
        return self._client._call(
            "DELETE",
            "/v1/projects/{project}",
            path_params={"project": project},
            query={"confirm": project},
            timeout=timeout,
        )

    def add_artifacts(
        self,
        *,
        project: str,
        artifacts: Optional[List[str]] = None,
        group_label: Optional[str] = None,
        confirm: Optional[bool] = None,
        workspace: Optional[str] = None,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Add artifacts to a project.

        A project is an ordered set of your artifacts shown one at a time at /s/{slug}, with its
        own audience and share list. No `project`: `title` creates one (seeded from
        `artifacts`), else list yours. With `project`: add `artifacts`, `remove` one, `title`
        renames, set `visibility`, `order`/`move` reorder, a `rule` adds matches as they are
        published, or read it. `delete` with `confirm: true` removes the project, its order and
        its share list permanently; its artifacts stay. One change per call, or title with
        visibility. An artifact's gallery label is not a project: that is `collection` on
        super_artifact_set.
        """
        return self._client._call(
            "POST",
            "/v1/projects/{project}/artifacts",
            path_params={"project": project},
            body={"artifacts": artifacts, "groupLabel": group_label, "confirm": confirm, "workspace": workspace},
            idempotency_key=idempotency_key,
            timeout=timeout,
        )

    def remove_artifact(
        self,
        *,
        project: str,
        remove: str,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Remove one artifact (or item) from a project.

        A project is an ordered set of your artifacts shown one at a time at /s/{slug}, with its
        own audience and share list. No `project`: `title` creates one (seeded from
        `artifacts`), else list yours. With `project`: add `artifacts`, `remove` one, `title`
        renames, set `visibility`, `order`/`move` reorder, a `rule` adds matches as they are
        published, or read it. `delete` with `confirm: true` removes the project, its order and
        its share list permanently; its artifacts stay. One change per call, or title with
        visibility. An artifact's gallery label is not a project: that is `collection` on
        super_artifact_set.
        """
        return self._client._call(
            "DELETE",
            "/v1/projects/{project}/artifacts/{remove}",
            path_params={"project": project, "remove": remove},
            timeout=timeout,
        )


class Shares(_Resource):

    def add_to_artifact(
        self,
        *,
        artifact: str,
        emails: List[str],
        role: Optional[Literal["viewer", "commenter", "editor"]] = None,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Give named people access to an artifact.

        Give named people access to one of: an `artifact` (viewer; commenter also comments;
        editor also edits; new addresses are emailed), a `project` (viewer; each address is
        emailed) or a `workspace` (editor; returns accept links, sends no email). Someone
        already named moves to the role sent, so a lower role replaces a higher one; nobody is
        removed. Never changes visibility: public stays public; restrict with
        super_artifact_set. At most 20 addresses for an artifact, 50 for a project or workspace.
        """
        return self._client._call(
            "POST",
            "/v1/artifacts/{artifact}/shares",
            path_params={"artifact": artifact},
            body={"emails": emails, "role": role},
            idempotency_key=idempotency_key,
            timeout=timeout,
        )

    def add_to_project(
        self,
        *,
        project: str,
        emails: List[str],
        role: Optional[Literal["viewer", "commenter", "editor"]] = None,
        confirm: Optional[bool] = None,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Give named people access to a project.

        Give named people access to one of: an `artifact` (viewer; commenter also comments;
        editor also edits; new addresses are emailed), a `project` (viewer; each address is
        emailed) or a `workspace` (editor; returns accept links, sends no email). Someone
        already named moves to the role sent, so a lower role replaces a higher one; nobody is
        removed. Never changes visibility: public stays public; restrict with
        super_artifact_set. At most 20 addresses for an artifact, 50 for a project or workspace.
        """
        return self._client._call(
            "POST",
            "/v1/projects/{project}/shares",
            path_params={"project": project},
            body={"emails": emails, "role": role, "confirm": confirm},
            idempotency_key=idempotency_key,
            timeout=timeout,
        )

    def add_to_workspace(
        self,
        *,
        emails: List[str],
        role: Optional[Literal["viewer", "commenter", "editor"]] = None,
        workspace: Optional[str] = None,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Invite editors to a workspace (returns accept links).

        Give named people access to one of: an `artifact` (viewer; commenter also comments;
        editor also edits; new addresses are emailed), a `project` (viewer; each address is
        emailed) or a `workspace` (editor; returns accept links, sends no email). Someone
        already named moves to the role sent, so a lower role replaces a higher one; nobody is
        removed. Never changes visibility: public stays public; restrict with
        super_artifact_set. At most 20 addresses for an artifact, 50 for a project or workspace.
        """
        return self._client._call(
            "POST",
            "/v1/workspace/shares",
            body={"emails": emails, "role": role, "workspace": workspace},
            idempotency_key=idempotency_key,
            timeout=timeout,
        )


class Comments(_Resource):

    def list(
        self,
        *,
        artifact: str,
        status: Optional[Literal["all", "open", "resolved"]] = None,
        page: Optional[str] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Comment threads on an artifact, newest first.

        Threads: messages, anchor, viewed version (default `status: "open"`); status all
        includes resolved history. Publish the fix first, then respond with body explaining what
        changed and which version, plus resolve: true atomically. Reuse messageId on retry.
        Reports replied/resolved separately. resolve: false reopens. `screenshot` returns an
        image. Agents cannot open/delete threads. mentioned: true lists your @mentions, oldest
        unseen first, marking them seen.
        """
        return self._client._call(
            "GET",
            "/v1/artifacts/{artifact}/comments",
            path_params={"artifact": artifact},
            query={"status": status, "page": page, "limit": limit, "cursor": cursor},
            timeout=timeout,
        )

    def respond(
        self,
        *,
        artifact: str,
        respond: Optional[List[Dict[str, Any]]] = None,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Reply to and/or resolve threads, one outcome each.

        Threads: messages, anchor, viewed version (default `status: "open"`); status all
        includes resolved history. Publish the fix first, then respond with body explaining what
        changed and which version, plus resolve: true atomically. Reuse messageId on retry.
        Reports replied/resolved separately. resolve: false reopens. `screenshot` returns an
        image. Agents cannot open/delete threads. mentioned: true lists your @mentions, oldest
        unseen first, marking them seen.
        """
        return self._client._call(
            "POST",
            "/v1/artifacts/{artifact}/comments/responses",
            path_params={"artifact": artifact},
            body={"respond": respond},
            idempotency_key=idempotency_key,
            timeout=timeout,
        )

    def get_screenshot(
        self,
        *,
        artifact: str,
        screenshot: str,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """One message's screenshot, base64 in `image`.

        Threads: messages, anchor, viewed version (default `status: "open"`); status all
        includes resolved history. Publish the fix first, then respond with body explaining what
        changed and which version, plus resolve: true atomically. Reuse messageId on retry.
        Reports replied/resolved separately. resolve: false reopens. `screenshot` returns an
        image. Agents cannot open/delete threads. mentioned: true lists your @mentions, oldest
        unseen first, marking them seen.
        """
        return self._client._call(
            "GET",
            "/v1/artifacts/{artifact}/comments/screenshots/{screenshot}",
            path_params={"artifact": artifact, "screenshot": screenshot},
            timeout=timeout,
        )


class Mentions(_Resource):

    def list(
        self,
        *,
        artifact: Optional[str] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Where people @mentioned you; listing marks them seen.

        Threads: messages, anchor, viewed version (default `status: "open"`); status all
        includes resolved history. Publish the fix first, then respond with body explaining what
        changed and which version, plus resolve: true atomically. Reuse messageId on retry.
        Reports replied/resolved separately. resolve: false reopens. `screenshot` returns an
        image. Agents cannot open/delete threads. mentioned: true lists your @mentions, oldest
        unseen first, marking them seen.
        """
        return self._client._call(
            "GET",
            "/v1/mentions",
            query={"artifact": artifact, "limit": limit, "cursor": cursor},
            timeout=timeout,
        )

    def iter(self, **kwargs: Any) -> Iterator[Dict[str, Any]]:
        """Every item of `list`, across pages. Takes the same arguments."""
        return walk_cursor(self.list, "mentions", kwargs)


class Signatures(_Resource):

    def list(
        self,
        *,
        artifact: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """An artifact's signature requests, newest first.

        Ask named people to sign one published version of an artifact, and follow the request.
        `request` with `artifact`, `signers` [{name, email, party?}] (≤10) and an optional
        `message` (≤500 characters) emails each signer a private link; the version must be one
        file of at most 2 MiB, and it is kept while the request is open and for good once it
        completes. `status` with `request` (one) or `artifact` (all, newest first). `withdraw`
        closes an open request. `remind` emails `signer` the link again, three times at most, a
        day apart. Only each signer can sign, in a browser, after a code sent to their address:
        an agent cannot.
        """
        return self._client._call(
            "GET",
            "/v1/signatures",
            query={"artifact": artifact},
            timeout=timeout,
        )

    def request(
        self,
        *,
        artifact: Optional[str] = None,
        version: Optional[int] = None,
        signers: Optional[List[Dict[str, Any]]] = None,
        message: Optional[str] = None,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Ask named people to sign one version of an artifact.

        Ask named people to sign one published version of an artifact, and follow the request.
        `request` with `artifact`, `signers` [{name, email, party?}] (≤10) and an optional
        `message` (≤500 characters) emails each signer a private link; the version must be one
        file of at most 2 MiB, and it is kept while the request is open and for good once it
        completes. `status` with `request` (one) or `artifact` (all, newest first). `withdraw`
        closes an open request. `remind` emails `signer` the link again, three times at most, a
        day apart. Only each signer can sign, in a browser, after a code sent to their address:
        an agent cannot.
        """
        return self._client._call(
            "POST",
            "/v1/signatures",
            body={"artifact": artifact, "version": version, "signers": signers, "message": message},
            idempotency_key=idempotency_key,
            timeout=timeout,
        )

    def get(
        self,
        *,
        request: str,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """One signature request and its signers.

        Ask named people to sign one published version of an artifact, and follow the request.
        `request` with `artifact`, `signers` [{name, email, party?}] (≤10) and an optional
        `message` (≤500 characters) emails each signer a private link; the version must be one
        file of at most 2 MiB, and it is kept while the request is open and for good once it
        completes. `status` with `request` (one) or `artifact` (all, newest first). `withdraw`
        closes an open request. `remind` emails `signer` the link again, three times at most, a
        day apart. Only each signer can sign, in a browser, after a code sent to their address:
        an agent cannot.
        """
        return self._client._call(
            "GET",
            "/v1/signatures/{request}",
            path_params={"request": request},
            timeout=timeout,
        )

    def remind(
        self,
        *,
        request: str,
        signer: Optional[str] = None,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Email a signer their link again.

        Ask named people to sign one published version of an artifact, and follow the request.
        `request` with `artifact`, `signers` [{name, email, party?}] (≤10) and an optional
        `message` (≤500 characters) emails each signer a private link; the version must be one
        file of at most 2 MiB, and it is kept while the request is open and for good once it
        completes. `status` with `request` (one) or `artifact` (all, newest first). `withdraw`
        closes an open request. `remind` emails `signer` the link again, three times at most, a
        day apart. Only each signer can sign, in a browser, after a code sent to their address:
        an agent cannot.
        """
        return self._client._call(
            "POST",
            "/v1/signatures/{request}/remind",
            path_params={"request": request},
            body={"signer": signer},
            idempotency_key=idempotency_key,
            timeout=timeout,
        )

    def withdraw(
        self,
        *,
        request: str,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Close an open signature request.

        Ask named people to sign one published version of an artifact, and follow the request.
        `request` with `artifact`, `signers` [{name, email, party?}] (≤10) and an optional
        `message` (≤500 characters) emails each signer a private link; the version must be one
        file of at most 2 MiB, and it is kept while the request is open and for good once it
        completes. `status` with `request` (one) or `artifact` (all, newest first). `withdraw`
        closes an open request. `remind` emails `signer` the link again, three times at most, a
        day apart. Only each signer can sign, in a browser, after a code sent to their address:
        an agent cannot.
        """
        return self._client._call(
            "POST",
            "/v1/signatures/{request}/withdraw",
            path_params={"request": request},
            idempotency_key=idempotency_key,
            timeout=timeout,
        )


class SyncResources:
    def __init__(self) -> None:
        self.account = Account(self)
        self.artifacts = Artifacts(self)
        self.live = Live(self)
        self.uploads = Uploads(self)
        self.data = Data(self)
        self.schema = Schema(self)
        self.entries = Entries(self)
        self.secrets = Secrets(self)
        self.templates = Templates(self)
        self.projects = Projects(self)
        self.shares = Shares(self)
        self.comments = Comments(self)
        self.mentions = Mentions(self)
        self.signatures = Signatures(self)


class AsyncAccount(_Resource):

    async def whoami(
        self,
        *,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Who this key publishes as.

        Who this key publishes as: the workspace `handle`, `email`, `agent` name and `scope`
        (the artifacts it may change: its own, and those it is named Editor on), plus
        `liveRooms` where live rooms run (the limit and who holds one). Useful to confirm where
        a publish lands, or why an artifact answers `not_found`; no other tool needs it.
        """
        return await self._client._call(
            "GET",
            "/v1/whoami",
            timeout=timeout,
        )

    async def help(
        self,
        *,
        topic: Optional[Literal["tools", "data", "templates", "collections", "projects", "batch"]] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """How the operations fit together.

        Plain-text notes for when it is unclear which tool, data store or argument shape does a
        job. Topics: `tools` (a line per tool), `data` (which store a page needs and how the
        page writes to it), `templates` (finding, building from, drafting, releasing),
        `collections` (content models and field types), `projects` (creating, ordering, sharing,
        rules), `batch` (what each tool takes in one call). Without `topic`: the full topic
        list, which names two more reached from results. Answers `{topic, text}`; not needed
        when a tool’s own description answers the question.
        """
        return await self._client._call(
            "GET",
            "/v1/help",
            query={"topic": topic},
            timeout=timeout,
        )


class AsyncArtifacts(AsyncArtifactHelper, _Resource):

    async def list(
        self,
        *,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """List your artifacts, newest first.

        Without `artifact`: your artifacts, newest first, with URLs and `live`. With `artifact`:
        its versions, which is published, their paths, and `declaration` (the published policy).
        Add `path` or `version` to read that file as text (default: published index.html); non-
        text or over 300,000 bytes: refused. `open: true` (with `artifact`, optional `version`)
        returns `url` and `expiresAt`: load `url` to see the artifact as a viewer, private
        included, for 10 minutes; visibility is unchanged, the URL opens only that artifact,
        60/key/hour (`rate_limited`). Changing what an artifact serves, or who can open it, is
        super_artifact_set.
        """
        return await self._client._call(
            "GET",
            "/v1/artifacts",
            timeout=timeout,
        )

    async def publish(
        self,
        *,
        slug: str,
        prompt: Optional[str] = None,
        html: Optional[str] = None,
        values: Optional[Dict[str, Any]] = None,
        instances: Optional[List[Dict[str, Any]]] = None,
        template: Optional[Dict[str, Any]] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        kind: Optional[Literal["page", "slideshow", "survey", "tracker", "video", "tool", "dashboard"]] = None,
        collection: Optional[str] = None,
        visibility: Optional[Literal["private", "organization"]] = None,
        policy: Optional[Dict[str, Any]] = None,
        dataset: Optional[str] = None,
        continues: Optional[str] = None,
        uploads: Optional[str] = None,
        values_file: Optional[str] = None,
        files: Optional[List[Dict[str, Any]]] = None,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Publish an artifact, or a new version of one.

        Publish a page at a stable URL; the same slug adds a new version, which the URL serves
        at once. Earlier versions stay and can be served again; nothing that existed before the
        call is deleted. Always give the person the url from the result, even on updates. Send
        `html`, or `values` for a template that carries a runtime, not both. Without `policy` a
        form, input or saved state stores nothing; CMS rows a page edits go in
        `policy.collections`. When retained storage is full it refuses with `plan_limit` and
        deletes nothing. A template becomes everybody’s through a release, not a publish.
        """
        return await self._client._call(
            "POST",
            "/v1/artifacts",
            body={"slug": slug, "prompt": prompt, "html": html, "values": values, "instances": instances, "template": template, "title": title, "description": description, "kind": kind, "collection": collection, "visibility": visibility, "policy": policy, "dataset": dataset, "continues": continues, "uploads": uploads, "valuesFile": values_file, "files": files},
            idempotency_key=idempotency_key,
            timeout=timeout,
        )

    async def get(
        self,
        *,
        artifact: str,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """One artifact: its versions, published version and declaration.

        Without `artifact`: your artifacts, newest first, with URLs and `live`. With `artifact`:
        its versions, which is published, their paths, and `declaration` (the published policy).
        Add `path` or `version` to read that file as text (default: published index.html); non-
        text or over 300,000 bytes: refused. `open: true` (with `artifact`, optional `version`)
        returns `url` and `expiresAt`: load `url` to see the artifact as a viewer, private
        included, for 10 minutes; visibility is unchanged, the URL opens only that artifact,
        60/key/hour (`rate_limited`). Changing what an artifact serves, or who can open it, is
        super_artifact_set.
        """
        return await self._client._call(
            "GET",
            "/v1/artifacts/{artifact}",
            path_params={"artifact": artifact},
            timeout=timeout,
        )

    async def update(
        self,
        *,
        artifact: str,
        visibility: Optional[Literal["private", "organization", "public"]] = None,
        collection: Optional[str] = None,
        phase: Optional[str] = None,
        notify_on_submission: Optional[bool] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Change visibility, gallery label, live phase or submission email.

        Change one artifact. `version` serves an existing version (a pointer move; nothing
        rebuilt or deleted). `live` turns its live room on or off; off disconnects every
        visitor, and Free has one room at a time. `notifyOnSubmission` emails you for each new
        data submission (default off; edits send nothing; no answers in the mail). `phase` sets
        the live room’s phase. `visibility` widens or narrows who can open it; narrowing voids
        every viewer grant already issued, so each viewer is checked again. `collection` sets
        its gallery grouping label. `delete` removes the artifact with every version, share link
        and response, permanently; it needs `confirm: true` and goes alone. Fields apply in that
        order, and a refusal part-way names the ones already `applied`. Publishing a new version
        is super_publish.
        """
        return await self._client._call(
            "PATCH",
            "/v1/artifacts/{artifact}",
            path_params={"artifact": artifact},
            body={"visibility": visibility, "collection": collection, "phase": phase, "notifyOnSubmission": notify_on_submission},
            timeout=timeout,
        )

    async def delete(
        self,
        *,
        artifact: str,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Delete an artifact with every version, permanently.

        Change one artifact. `version` serves an existing version (a pointer move; nothing
        rebuilt or deleted). `live` turns its live room on or off; off disconnects every
        visitor, and Free has one room at a time. `notifyOnSubmission` emails you for each new
        data submission (default off; edits send nothing; no answers in the mail). `phase` sets
        the live room’s phase. `visibility` widens or narrows who can open it; narrowing voids
        every viewer grant already issued, so each viewer is checked again. `collection` sets
        its gallery grouping label. `delete` removes the artifact with every version, share link
        and response, permanently; it needs `confirm: true` and goes alone. Fields apply in that
        order, and a refusal part-way names the ones already `applied`. Publishing a new version
        is super_publish.
        """
        return await self._client._call(
            "DELETE",
            "/v1/artifacts/{artifact}",
            path_params={"artifact": artifact},
            query={"confirm": artifact},
            timeout=timeout,
        )

    async def read_file(
        self,
        *,
        artifact: str,
        path: Optional[str] = None,
        version: Optional[int] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Read one file of a version as text (default: the published index.html).

        Without `artifact`: your artifacts, newest first, with URLs and `live`. With `artifact`:
        its versions, which is published, their paths, and `declaration` (the published policy).
        Add `path` or `version` to read that file as text (default: published index.html); non-
        text or over 300,000 bytes: refused. `open: true` (with `artifact`, optional `version`)
        returns `url` and `expiresAt`: load `url` to see the artifact as a viewer, private
        included, for 10 minutes; visibility is unchanged, the URL opens only that artifact,
        60/key/hour (`rate_limited`). Changing what an artifact serves, or who can open it, is
        super_artifact_set.
        """
        return await self._client._call(
            "GET",
            "/v1/artifacts/{artifact}/file",
            path_params={"artifact": artifact},
            query={"path": path, "version": version},
            timeout=timeout,
        )

    async def open(
        self,
        *,
        artifact: str,
        version: Optional[int] = None,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """A ten-minute viewer URL for an artifact, private included.

        Without `artifact`: your artifacts, newest first, with URLs and `live`. With `artifact`:
        its versions, which is published, their paths, and `declaration` (the published policy).
        Add `path` or `version` to read that file as text (default: published index.html); non-
        text or over 300,000 bytes: refused. `open: true` (with `artifact`, optional `version`)
        returns `url` and `expiresAt`: load `url` to see the artifact as a viewer, private
        included, for 10 minutes; visibility is unchanged, the URL opens only that artifact,
        60/key/hour (`rate_limited`). Changing what an artifact serves, or who can open it, is
        super_artifact_set.
        """
        return await self._client._call(
            "POST",
            "/v1/artifacts/{artifact}/open",
            path_params={"artifact": artifact},
            body={"version": version},
            idempotency_key=idempotency_key,
            timeout=timeout,
        )

    async def serve_version(
        self,
        *,
        artifact: str,
        version: int,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Serve an existing version again.

        Change one artifact. `version` serves an existing version (a pointer move; nothing
        rebuilt or deleted). `live` turns its live room on or off; off disconnects every
        visitor, and Free has one room at a time. `notifyOnSubmission` emails you for each new
        data submission (default off; edits send nothing; no answers in the mail). `phase` sets
        the live room’s phase. `visibility` widens or narrows who can open it; narrowing voids
        every viewer grant already issued, so each viewer is checked again. `collection` sets
        its gallery grouping label. `delete` removes the artifact with every version, share link
        and response, permanently; it needs `confirm: true` and goes alone. Fields apply in that
        order, and a refusal part-way names the ones already `applied`. Publishing a new version
        is super_publish.
        """
        return await self._client._call(
            "POST",
            "/v1/artifacts/{artifact}/versions/{version}/serve",
            path_params={"artifact": artifact, "version": version},
            idempotency_key=idempotency_key,
            timeout=timeout,
        )


class AsyncLive(_Resource):

    async def start(
        self,
        *,
        artifact: str,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Turn an artifact's live room on.

        Change one artifact. `version` serves an existing version (a pointer move; nothing
        rebuilt or deleted). `live` turns its live room on or off; off disconnects every
        visitor, and Free has one room at a time. `notifyOnSubmission` emails you for each new
        data submission (default off; edits send nothing; no answers in the mail). `phase` sets
        the live room’s phase. `visibility` widens or narrows who can open it; narrowing voids
        every viewer grant already issued, so each viewer is checked again. `collection` sets
        its gallery grouping label. `delete` removes the artifact with every version, share link
        and response, permanently; it needs `confirm: true` and goes alone. Fields apply in that
        order, and a refusal part-way names the ones already `applied`. Publishing a new version
        is super_publish.
        """
        return await self._client._call(
            "POST",
            "/v1/artifacts/{artifact}/live",
            path_params={"artifact": artifact},
            idempotency_key=idempotency_key,
            timeout=timeout,
        )

    async def stop(
        self,
        *,
        artifact: str,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Turn an artifact's live room off, disconnecting every visitor.

        Change one artifact. `version` serves an existing version (a pointer move; nothing
        rebuilt or deleted). `live` turns its live room on or off; off disconnects every
        visitor, and Free has one room at a time. `notifyOnSubmission` emails you for each new
        data submission (default off; edits send nothing; no answers in the mail). `phase` sets
        the live room’s phase. `visibility` widens or narrows who can open it; narrowing voids
        every viewer grant already issued, so each viewer is checked again. `collection` sets
        its gallery grouping label. `delete` removes the artifact with every version, share link
        and response, permanently; it needs `confirm: true` and goes alone. Fields apply in that
        order, and a refusal part-way names the ones already `applied`. Publishing a new version
        is super_publish.
        """
        return await self._client._call(
            "DELETE",
            "/v1/artifacts/{artifact}/live",
            path_params={"artifact": artifact},
            timeout=timeout,
        )


class AsyncUploads(AsyncUploadHelper, _Resource):

    async def stage(
        self,
        *,
        files: List[Dict[str, Any]],
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Stage big files for a publish; PUT each to its URL.

        Stage images, video or big files for a publish without sending their bytes in a call.
        Declare each file’s `path` and exact `bytes`; the result carries an `uploadId` and one
        `url` per file. PUT each file to its URL (`curl -T`, no credentials), then super_publish
        with `uploads`. Not index.html: that is `html`; small assets can ride inline as the
        publish’s `files`. Same limits as `files`; a staged set expires after 30 minutes, and at
        most 5 wait unpublished at once.
        """
        return await self._client._call(
            "POST",
            "/v1/uploads",
            body={"files": files},
            idempotency_key=idempotency_key,
            timeout=timeout,
        )


class AsyncData(_Resource):

    async def list_artifact_rows(
        self,
        *,
        artifact: str,
        filter: Optional[List[str]] = None,
        since: Optional[str] = None,
        until: Optional[str] = None,
        sort: Optional[Literal["newest", "oldest"]] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        fields: Optional[List[str]] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Rows visitors submitted to one artifact, newest first.

        The rows visitors submitted to your artifacts, newest first, with each version's field
        schema; paged by `cursor`. Address exactly one: `artifact`; `dataset` (a catalog key;
        one shared by several artifacts is `ambiguous_dataset`); or `collection`, the gallery
        grouping label set at publish, not a content collection (≤20 artifacts over one window,
        kept per artifact, no `filter`). Entries of a content collection are super_entries;
        totals and averages are a query, not a read.
        """
        return await self._client._call(
            "GET",
            "/v1/artifacts/{artifact}/data",
            path_params={"artifact": artifact},
            query={"filter": filter, "since": since, "until": until, "sort": sort, "limit": limit, "cursor": cursor, "fields": fields},
            timeout=timeout,
        )

    def iter_artifact_rows(self, **kwargs: Any) -> AsyncIterator[Dict[str, Any]]:
        """Every item of `list_artifact_rows`, across pages. Takes the same arguments."""
        return awalk_cursor(self.list_artifact_rows, "responses", kwargs)

    async def write_artifact_rows(
        self,
        *,
        artifact: str,
        stream: Optional[str] = None,
        rows: Optional[List[Dict[str, Any]]] = None,
        ops: Optional[List[Dict[str, Any]]] = None,
        atomic: Optional[bool] = None,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Write rows into an artifact you may edit.

        Write rows into an artifact this key may edit, through the validation and stream rules a
        page write gets; each row is attributed "<agent> (agent)". `rows` creates in `stream`.
        `ops` [{op: create|replace|delete, id, row, stream}] replaces or deletes only rows this
        agent wrote (writes: upsert); a deleted row cannot be restored by any tool. ≤50 a call;
        `atomic`: all or none, otherwise a partial batch answers `complete: false`. Visitor rows
        are never changed here; entries of a content collection are super_entries.
        """
        return await self._client._call(
            "POST",
            "/v1/artifacts/{artifact}/data/rows",
            path_params={"artifact": artifact},
            body={"stream": stream, "rows": rows, "ops": ops, "atomic": atomic},
            idempotency_key=idempotency_key,
            timeout=timeout,
        )

    async def list_rows(
        self,
        *,
        dataset: Optional[str] = None,
        collection: Optional[str] = None,
        filter: Optional[List[str]] = None,
        since: Optional[str] = None,
        until: Optional[str] = None,
        sort: Optional[Literal["newest", "oldest"]] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        fields: Optional[List[str]] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Rows submitted to a dataset or a gallery label.

        The rows visitors submitted to your artifacts, newest first, with each version's field
        schema; paged by `cursor`. Address exactly one: `artifact`; `dataset` (a catalog key;
        one shared by several artifacts is `ambiguous_dataset`); or `collection`, the gallery
        grouping label set at publish, not a content collection (≤20 artifacts over one window,
        kept per artifact, no `filter`). Entries of a content collection are super_entries;
        totals and averages are a query, not a read.
        """
        return await self._client._call(
            "GET",
            "/v1/data",
            query={"dataset": dataset, "collection": collection, "filter": filter, "since": since, "until": until, "sort": sort, "limit": limit, "cursor": cursor, "fields": fields},
            timeout=timeout,
        )

    def iter_rows(self, **kwargs: Any) -> AsyncIterator[Dict[str, Any]]:
        """Every item of `list_rows`, across pages. Takes the same arguments."""
        return awalk_cursor(self.list_rows, "responses", kwargs)

    async def query(
        self,
        *,
        scope: Optional[Dict[str, Any]] = None,
        measures: Optional[List[str]] = None,
        agg: Optional[Literal["sum", "avg", "min", "max", "count", "last"]] = None,
        compute: Optional[List[Dict[str, Any]]] = None,
        filter: Optional[List[str]] = None,
        group_by: Optional[List[str]] = None,
        since: Optional[str] = None,
        until: Optional[str] = None,
        limit: Optional[int] = None,
        distributions: Optional[Dict[str, Any]] = None,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Aggregate what was collected: numbers, never rows.

        Numbers over what was collected, never rows (rows are super_data). Aggregate `measures`
        across the datasets in `scope`; datasets combine on the same measure in one base unit,
        results in the declared `unit`. Names come from the catalog; an unknown one errors with
        near misses. The answer has one row per `group_by` key (or one row) with a column per
        measure and `compute`, the datasets used and any skipped, and `truncated` when `limit`
        cut it. Or send `distributions` for one artifact: counts, per-version rates and per-
        field distributions (free text: answer rate and length only). A call with neither is
        `invalid_query`.
        """
        return await self._client._call(
            "POST",
            "/v1/data/query",
            body={"scope": scope, "measures": measures, "agg": agg, "compute": compute, "filter": filter, "group_by": group_by, "since": since, "until": until, "limit": limit, "distributions": distributions},
            idempotency_key=idempotency_key,
            timeout=timeout,
        )


class AsyncSchema(_Resource):

    async def get(
        self,
        *,
        series: Optional[str] = None,
        tags: Optional[List[str]] = None,
        artifact: Optional[str] = None,
        compare: Optional[List[str]] = None,
        since: Optional[str] = None,
        workspace: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """The data catalog: datasets and content collections, or a comparison.

        The data catalog, without rows. Read (the default): `datasets` your artifacts declared,
        with fields, units, measures and `since`/`deprecated` versions, and this workspace's
        content `collections`, with fields, rules and entry counts. `compare` (alone): two to
        ten artifacts' newest fields side by side, every type, unit and measure conflict named.
        `define` creates a content collection, or replaces the one with that `key` outright,
        name, display field and every field; a field left out is gone from the model, and a
        collection an artifact declared is refused with `conflict`. Refusals name field, rule
        and fix. Rows an artifact collected are super_data.
        """
        return await self._client._call(
            "GET",
            "/v1/schema",
            query={"series": series, "tags": tags, "artifact": artifact, "compare": compare, "since": since, "workspace": workspace},
            timeout=timeout,
        )

    async def define_collection(
        self,
        *,
        define: Optional[Dict[str, Any]] = None,
        workspace: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Create or replace a content collection.

        The data catalog, without rows. Read (the default): `datasets` your artifacts declared,
        with fields, units, measures and `since`/`deprecated` versions, and this workspace's
        content `collections`, with fields, rules and entry counts. `compare` (alone): two to
        ten artifacts' newest fields side by side, every type, unit and measure conflict named.
        `define` creates a content collection, or replaces the one with that `key` outright,
        name, display field and every field; a field left out is gone from the model, and a
        collection an artifact declared is refused with `conflict`. Refusals name field, rule
        and fix. Rows an artifact collected are super_data.
        """
        return await self._client._call(
            "PUT",
            "/v1/schema",
            body={"define": define, "workspace": workspace},
            timeout=timeout,
        )


class AsyncEntries(_Resource):

    async def list(
        self,
        *,
        collection: str,
        workspace: Optional[str] = None,
        filter: Optional[List[str]] = None,
        search: Optional[str] = None,
        sort: Optional[str] = None,
        direction: Optional[Literal["asc", "desc"]] = None,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        if_none_match: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """One page of a content collection's entries.

        Entries of a workspace content collection (a model defined in the catalog), not rows an
        artifact collected. With `values`: create one entry (an object) or up to 50 (an array,
        one outcome per row); values are coerced to declared types, undeclared fields are
        refused by name, and nothing existing is updated or deleted. Without: read one page,
        filtered and sorted in the database; references resolve to labels, sensitive fields read
        as answered-or-not. Rows visitors submitted are super_data.
        """
        return await self._client._call(
            "GET",
            "/v1/collections/{collection}/entries",
            headers={"If-None-Match": if_none_match},
            path_params={"collection": collection},
            query={"workspace": workspace, "filter": filter, "search": search, "sort": sort, "direction": direction, "page": page, "limit": limit},
            timeout=timeout,
        )

    def iter(self, **kwargs: Any) -> AsyncIterator[Dict[str, Any]]:
        """Every item of `list`, across pages. Takes the same arguments."""
        return awalk_pages(self.list, "entries", kwargs)

    async def create(
        self,
        *,
        collection: str,
        values: Optional[Any] = None,
        status: Optional[Literal["draft", "published", "archived"]] = None,
        workspace: Optional[str] = None,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Create one entry, or a batch.

        Entries of a workspace content collection (a model defined in the catalog), not rows an
        artifact collected. With `values`: create one entry (an object) or up to 50 (an array,
        one outcome per row); values are coerced to declared types, undeclared fields are
        refused by name, and nothing existing is updated or deleted. Without: read one page,
        filtered and sorted in the database; references resolve to labels, sensitive fields read
        as answered-or-not. Rows visitors submitted are super_data.
        """
        return await self._client._call(
            "POST",
            "/v1/collections/{collection}/entries",
            path_params={"collection": collection},
            body={"values": values, "status": status, "workspace": workspace},
            idempotency_key=idempotency_key,
            timeout=timeout,
        )


class AsyncSecrets(_Resource):

    async def use(
        self,
        *,
        collection: str,
        entry: str,
        field: str,
        method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"],
        url: str,
        headers: Optional[Dict[str, Any]] = None,
        body: Optional[str] = None,
        header: Optional[Dict[str, Any]] = None,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Call an approved API with a stored secret you cannot read (workspace keys).

        Make one HTTPS request with a `pii: secret` value from a content collection entry. The
        platform puts the value into one header and calls the one host a person approved; you
        get status, headers and body, scrubbed of it. You never see it, in input or result; a
        response echoing it is withheld whole (`secret_echoed`). A first request for a field and
        host answers `approval_required` with `approvalUrl`: give the person that link, then
        repeat the request once they approve. Grants expire, cap uses and can be revoked; every
        use is logged. The person types the secret into its dashboard entry; super_entries
        writes one only if they insist on pasting it.
        """
        return await self._client._call(
            "POST",
            "/v1/collections/{collection}/entries/{entry}/fields/{field}/use",
            path_params={"collection": collection, "entry": entry, "field": field},
            body={"method": method, "url": url, "headers": headers, "body": body, "header": header},
            idempotency_key=idempotency_key,
            timeout=timeout,
        )


class AsyncTemplates(_Resource):

    async def list(
        self,
        *,
        request: Optional[str] = None,
        scope: Optional[Literal["installed", "marketplace"]] = None,
        kind: Optional[Literal["page", "slideshow", "survey", "tracker", "video", "tool", "dashboard"]] = None,
        sort: Optional[Literal["relevance", "rating", "uses", "installs", "recent"]] = None,
        limit: Optional[int] = None,
        jobs: Optional[List[Literal["track", "collect", "present", "report", "monitor", "prove", "document", "explain", "plan", "decide", "review", "learn", "prototype", "announce", "compute", "curate", "coordinate", "play"]]] = None,
        audience: Optional[List[Literal["everyone", "engineering", "product", "design", "marketing", "sales", "ops", "people", "finance", "founders", "education", "personal", "community"]]] = None,
        needs: Optional[List[Literal["runtime", "data", "comments", "live"]]] = None,
        cost: Optional[Literal["fill", "write", "build"]] = None,
        tier: Optional[Literal["all", "official", "verified", "community"]] = None,
        mine: Optional[bool] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Find, rank or list templates.

        With `request`: rank installed templates by content similarity; matches carry `band`
        (high: build from it; possible: judge it), `why` and unscored stats. `scope:
        marketplace`: released public templates, ranked by `request` or else the top by `sort`;
        `sort`, `limit` and the facets apply only here. Neither: the installed list. `slug`: one
        template in full, with its `installPrompt`; `history`: its changelog; `feedback`: its
        artifacts' comments as themes. `mine`: your published templates, with counts. Reading
        only: installing, rating and rolling back are super_template_action.
        """
        return await self._client._call(
            "GET",
            "/v1/templates",
            query={"request": request, "scope": scope, "kind": kind, "sort": sort, "limit": limit, "jobs": jobs, "audience": audience, "needs": needs, "cost": cost, "tier": tier, "mine": mine},
            timeout=timeout,
        )

    async def save(
        self,
        *,
        slug: str,
        title: str,
        description: str,
        spec: Dict[str, Any],
        kind: Optional[Literal["page", "slideshow", "survey", "tracker", "video", "tool", "dashboard"]] = None,
        jobs: Optional[List[Literal["track", "collect", "present", "report", "monitor", "prove", "document", "explain", "plan", "decide", "review", "learn", "prototype", "announce", "compute", "curate", "coordinate", "play"]]] = None,
        audience: Optional[List[Literal["everyone", "engineering", "product", "design", "marketing", "sales", "ops", "people", "finance", "founders", "education", "personal", "community"]]] = None,
        use_cases: Optional[List[Dict[str, Any]]] = None,
        install_archetype: Optional[Literal["scenarios", "explainer", "interview"]] = None,
        install_after: Optional[str] = None,
        sample_public: Optional[bool] = None,
        category: Optional[Literal["trackers", "surveys", "presentations", "dashboards", "documents", "tools", "games", "other"]] = None,
        guidance: Optional[str] = None,
        prompt: Optional[str] = None,
        sample: Optional[Dict[str, Any]] = None,
        demo: Optional[str] = None,
        files: Optional[List[Dict[str, Any]]] = None,
        companions: Optional[List[Dict[str, Any]]] = None,
        expected_version: Optional[int] = None,
        change_note: Optional[str] = None,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Create or revise a template draft.

        Write a template draft only you can publish from. Without `expectedVersion` it creates
        (refused if the slug exists); with it, it revises the head (refused if the head moved
        past it), and a revision that changes nothing cuts no version. A `json` slot needs
        `schema`. Runtime `files` (≤512 KiB decoded) need a `json` slot and an index.html with
        one `<script id="sa-template-values" type="application/json">`. Others build from it
        only once super_release_template releases it; a revision never changes a released
        version.
        """
        return await self._client._call(
            "POST",
            "/v1/templates",
            body={"slug": slug, "title": title, "description": description, "kind": kind, "jobs": jobs, "audience": audience, "useCases": use_cases, "installArchetype": install_archetype, "installAfter": install_after, "samplePublic": sample_public, "category": category, "spec": spec, "guidance": guidance, "prompt": prompt, "sample": sample, "demo": demo, "files": files, "companions": companions, "expectedVersion": expected_version, "changeNote": change_note},
            idempotency_key=idempotency_key,
            timeout=timeout,
        )

    async def get(
        self,
        *,
        slug: str,
        version: Optional[int] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """One template in full, with its install prompt.

        With `request`: rank installed templates by content similarity; matches carry `band`
        (high: build from it; possible: judge it), `why` and unscored stats. `scope:
        marketplace`: released public templates, ranked by `request` or else the top by `sort`;
        `sort`, `limit` and the facets apply only here. Neither: the installed list. `slug`: one
        template in full, with its `installPrompt`; `history`: its changelog; `feedback`: its
        artifacts' comments as themes. `mine`: your published templates, with counts. Reading
        only: installing, rating and rolling back are super_template_action.
        """
        return await self._client._call(
            "GET",
            "/v1/templates/{slug}",
            path_params={"slug": slug},
            query={"version": version},
            timeout=timeout,
        )

    async def get_history(
        self,
        *,
        slug: str,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """A template's changelog.

        With `request`: rank installed templates by content similarity; matches carry `band`
        (high: build from it; possible: judge it), `why` and unscored stats. `scope:
        marketplace`: released public templates, ranked by `request` or else the top by `sort`;
        `sort`, `limit` and the facets apply only here. Neither: the installed list. `slug`: one
        template in full, with its `installPrompt`; `history`: its changelog; `feedback`: its
        artifacts' comments as themes. `mine`: your published templates, with counts. Reading
        only: installing, rating and rolling back are super_template_action.
        """
        return await self._client._call(
            "GET",
            "/v1/templates/{slug}/history",
            path_params={"slug": slug},
            timeout=timeout,
        )

    async def get_feedback(
        self,
        *,
        slug: str,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Comments on a template's artifacts, as themes.

        With `request`: rank installed templates by content similarity; matches carry `band`
        (high: build from it; possible: judge it), `why` and unscored stats. `scope:
        marketplace`: released public templates, ranked by `request` or else the top by `sort`;
        `sort`, `limit` and the facets apply only here. Neither: the installed list. `slug`: one
        template in full, with its `installPrompt`; `history`: its changelog; `feedback`: its
        artifacts' comments as themes. `mine`: your published templates, with counts. Reading
        only: installing, rating and rolling back are super_template_action.
        """
        return await self._client._call(
            "GET",
            "/v1/templates/{slug}/feedback",
            path_params={"slug": slug},
            timeout=timeout,
        )

    async def act(
        self,
        *,
        slug: str,
        action: Literal["install", "uninstall", "rate", "report", "rollback", "request_verification"],
        stars: Optional[int] = None,
        version: Optional[int] = None,
        kind: Optional[Literal["spam", "harmful", "broken", "misleading", "pii", "copyright", "other"]] = None,
        reason: Optional[str] = None,
        confirmed_by_person: Optional[bool] = None,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Install, uninstall, rate, report, roll back or request verification.

        Act on one template; nothing here deletes a template, a version or a built artifact.
        `install`/`uninstall`: this workspace's installed set (uninstall removes only the
        install; built artifacts keep working); `install` returns its build prompt as
        `nextStep`. `rate`: the person's 1–5 `stars` on an installed template not yours
        (`cannot_rate_own`, `not_installed`, `rate_limited`); counts once this workspace built
        from it. `report`: `kind` and a `reason` (≤1000 chars) for a moderator; one per account;
        enough reports hide it. `rollback`: restore `version` as a new version, unless the
        runtime changed. `request_verification`: a moderator checks your released `version`; 3
        per 30 days. Finding and reading templates is super_templates.
        """
        return await self._client._call(
            "POST",
            "/v1/templates/{slug}/actions",
            path_params={"slug": slug},
            body={"action": action, "stars": stars, "version": version, "kind": kind, "reason": reason, "confirmedByPerson": confirmed_by_person},
            idempotency_key=idempotency_key,
            timeout=timeout,
        )

    async def release(
        self,
        *,
        slug: str,
        version: int,
        visibility: Optional[Literal["public", "unlisted", "workspace"]] = None,
        demo_consent: Optional[bool] = None,
        sample_consent: Optional[bool] = None,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Release one version of your template.

        Release one version of your template so others can build from it, live at once to the
        reach `visibility` sets; the result names its trust `tier` (Official, Verified or
        Community). Forward only (`release_moves_backwards`): earlier versions stay, and nothing
        is deleted. A private demo needs `demoConsent: true`. A runtime, prompt, parts or data
        change leaves a Verified badge behind. Public: account 7 days old (`publisher_too_new`),
        10/day, 3/template/hour (`rate_limited`), 20 templates (`too_many_templates`), no tier
        words (`reserved_wording`), no credential (`secret_in_template`), paid plan
        (`plan_required`). Writing the draft is super_template_save.
        """
        return await self._client._call(
            "POST",
            "/v1/templates/{slug}/release",
            path_params={"slug": slug},
            body={"version": version, "visibility": visibility, "demoConsent": demo_consent, "sampleConsent": sample_consent},
            idempotency_key=idempotency_key,
            timeout=timeout,
        )


class AsyncProjects(_Resource):

    async def list(
        self,
        *,
        workspace: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Your projects.

        A project is an ordered set of your artifacts shown one at a time at /s/{slug}, with its
        own audience and share list. No `project`: `title` creates one (seeded from
        `artifacts`), else list yours. With `project`: add `artifacts`, `remove` one, `title`
        renames, set `visibility`, `order`/`move` reorder, a `rule` adds matches as they are
        published, or read it. `delete` with `confirm: true` removes the project, its order and
        its share list permanently; its artifacts stay. One change per call, or title with
        visibility. An artifact's gallery label is not a project: that is `collection` on
        super_artifact_set.
        """
        return await self._client._call(
            "GET",
            "/v1/projects",
            query={"workspace": workspace},
            timeout=timeout,
        )

    async def create(
        self,
        *,
        title: Optional[str] = None,
        artifacts: Optional[List[str]] = None,
        group_label: Optional[str] = None,
        visibility: Optional[Literal["private", "organization", "public"]] = None,
        rule: Any = OMIT,
        confirm: Optional[bool] = None,
        workspace: Optional[str] = None,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Create a project, optionally seeded with artifacts.

        A project is an ordered set of your artifacts shown one at a time at /s/{slug}, with its
        own audience and share list. No `project`: `title` creates one (seeded from
        `artifacts`), else list yours. With `project`: add `artifacts`, `remove` one, `title`
        renames, set `visibility`, `order`/`move` reorder, a `rule` adds matches as they are
        published, or read it. `delete` with `confirm: true` removes the project, its order and
        its share list permanently; its artifacts stay. One change per call, or title with
        visibility. An artifact's gallery label is not a project: that is `collection` on
        super_artifact_set.
        """
        return await self._client._call(
            "POST",
            "/v1/projects",
            body={"title": title, "artifacts": artifacts, "groupLabel": group_label, "visibility": visibility, "confirm": confirm, "workspace": workspace},
            nullable={"rule": rule},
            idempotency_key=idempotency_key,
            timeout=timeout,
        )

    async def get(
        self,
        *,
        project: str,
        workspace: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """One project and its items.

        A project is an ordered set of your artifacts shown one at a time at /s/{slug}, with its
        own audience and share list. No `project`: `title` creates one (seeded from
        `artifacts`), else list yours. With `project`: add `artifacts`, `remove` one, `title`
        renames, set `visibility`, `order`/`move` reorder, a `rule` adds matches as they are
        published, or read it. `delete` with `confirm: true` removes the project, its order and
        its share list permanently; its artifacts stay. One change per call, or title with
        visibility. An artifact's gallery label is not a project: that is `collection` on
        super_artifact_set.
        """
        return await self._client._call(
            "GET",
            "/v1/projects/{project}",
            path_params={"project": project},
            query={"workspace": workspace},
            timeout=timeout,
        )

    async def update(
        self,
        *,
        project: str,
        title: Optional[str] = None,
        visibility: Optional[Literal["private", "organization", "public"]] = None,
        order: Optional[List[str]] = None,
        move: Optional[Dict[str, Any]] = None,
        rule: Any = OMIT,
        collapsed_groups: Optional[List[str]] = None,
        confirm: Optional[bool] = None,
        workspace: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Rename, set visibility, reorder, move, fold groups or set a rule.

        A project is an ordered set of your artifacts shown one at a time at /s/{slug}, with its
        own audience and share list. No `project`: `title` creates one (seeded from
        `artifacts`), else list yours. With `project`: add `artifacts`, `remove` one, `title`
        renames, set `visibility`, `order`/`move` reorder, a `rule` adds matches as they are
        published, or read it. `delete` with `confirm: true` removes the project, its order and
        its share list permanently; its artifacts stay. One change per call, or title with
        visibility. An artifact's gallery label is not a project: that is `collection` on
        super_artifact_set.
        """
        return await self._client._call(
            "PATCH",
            "/v1/projects/{project}",
            path_params={"project": project},
            body={"title": title, "visibility": visibility, "order": order, "move": move, "collapsedGroups": collapsed_groups, "confirm": confirm, "workspace": workspace},
            nullable={"rule": rule},
            timeout=timeout,
        )

    async def delete(
        self,
        *,
        project: str,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Delete a project; its artifacts stay.

        A project is an ordered set of your artifacts shown one at a time at /s/{slug}, with its
        own audience and share list. No `project`: `title` creates one (seeded from
        `artifacts`), else list yours. With `project`: add `artifacts`, `remove` one, `title`
        renames, set `visibility`, `order`/`move` reorder, a `rule` adds matches as they are
        published, or read it. `delete` with `confirm: true` removes the project, its order and
        its share list permanently; its artifacts stay. One change per call, or title with
        visibility. An artifact's gallery label is not a project: that is `collection` on
        super_artifact_set.
        """
        return await self._client._call(
            "DELETE",
            "/v1/projects/{project}",
            path_params={"project": project},
            query={"confirm": project},
            timeout=timeout,
        )

    async def add_artifacts(
        self,
        *,
        project: str,
        artifacts: Optional[List[str]] = None,
        group_label: Optional[str] = None,
        confirm: Optional[bool] = None,
        workspace: Optional[str] = None,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Add artifacts to a project.

        A project is an ordered set of your artifacts shown one at a time at /s/{slug}, with its
        own audience and share list. No `project`: `title` creates one (seeded from
        `artifacts`), else list yours. With `project`: add `artifacts`, `remove` one, `title`
        renames, set `visibility`, `order`/`move` reorder, a `rule` adds matches as they are
        published, or read it. `delete` with `confirm: true` removes the project, its order and
        its share list permanently; its artifacts stay. One change per call, or title with
        visibility. An artifact's gallery label is not a project: that is `collection` on
        super_artifact_set.
        """
        return await self._client._call(
            "POST",
            "/v1/projects/{project}/artifacts",
            path_params={"project": project},
            body={"artifacts": artifacts, "groupLabel": group_label, "confirm": confirm, "workspace": workspace},
            idempotency_key=idempotency_key,
            timeout=timeout,
        )

    async def remove_artifact(
        self,
        *,
        project: str,
        remove: str,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Remove one artifact (or item) from a project.

        A project is an ordered set of your artifacts shown one at a time at /s/{slug}, with its
        own audience and share list. No `project`: `title` creates one (seeded from
        `artifacts`), else list yours. With `project`: add `artifacts`, `remove` one, `title`
        renames, set `visibility`, `order`/`move` reorder, a `rule` adds matches as they are
        published, or read it. `delete` with `confirm: true` removes the project, its order and
        its share list permanently; its artifacts stay. One change per call, or title with
        visibility. An artifact's gallery label is not a project: that is `collection` on
        super_artifact_set.
        """
        return await self._client._call(
            "DELETE",
            "/v1/projects/{project}/artifacts/{remove}",
            path_params={"project": project, "remove": remove},
            timeout=timeout,
        )


class AsyncShares(_Resource):

    async def add_to_artifact(
        self,
        *,
        artifact: str,
        emails: List[str],
        role: Optional[Literal["viewer", "commenter", "editor"]] = None,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Give named people access to an artifact.

        Give named people access to one of: an `artifact` (viewer; commenter also comments;
        editor also edits; new addresses are emailed), a `project` (viewer; each address is
        emailed) or a `workspace` (editor; returns accept links, sends no email). Someone
        already named moves to the role sent, so a lower role replaces a higher one; nobody is
        removed. Never changes visibility: public stays public; restrict with
        super_artifact_set. At most 20 addresses for an artifact, 50 for a project or workspace.
        """
        return await self._client._call(
            "POST",
            "/v1/artifacts/{artifact}/shares",
            path_params={"artifact": artifact},
            body={"emails": emails, "role": role},
            idempotency_key=idempotency_key,
            timeout=timeout,
        )

    async def add_to_project(
        self,
        *,
        project: str,
        emails: List[str],
        role: Optional[Literal["viewer", "commenter", "editor"]] = None,
        confirm: Optional[bool] = None,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Give named people access to a project.

        Give named people access to one of: an `artifact` (viewer; commenter also comments;
        editor also edits; new addresses are emailed), a `project` (viewer; each address is
        emailed) or a `workspace` (editor; returns accept links, sends no email). Someone
        already named moves to the role sent, so a lower role replaces a higher one; nobody is
        removed. Never changes visibility: public stays public; restrict with
        super_artifact_set. At most 20 addresses for an artifact, 50 for a project or workspace.
        """
        return await self._client._call(
            "POST",
            "/v1/projects/{project}/shares",
            path_params={"project": project},
            body={"emails": emails, "role": role, "confirm": confirm},
            idempotency_key=idempotency_key,
            timeout=timeout,
        )

    async def add_to_workspace(
        self,
        *,
        emails: List[str],
        role: Optional[Literal["viewer", "commenter", "editor"]] = None,
        workspace: Optional[str] = None,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Invite editors to a workspace (returns accept links).

        Give named people access to one of: an `artifact` (viewer; commenter also comments;
        editor also edits; new addresses are emailed), a `project` (viewer; each address is
        emailed) or a `workspace` (editor; returns accept links, sends no email). Someone
        already named moves to the role sent, so a lower role replaces a higher one; nobody is
        removed. Never changes visibility: public stays public; restrict with
        super_artifact_set. At most 20 addresses for an artifact, 50 for a project or workspace.
        """
        return await self._client._call(
            "POST",
            "/v1/workspace/shares",
            body={"emails": emails, "role": role, "workspace": workspace},
            idempotency_key=idempotency_key,
            timeout=timeout,
        )


class AsyncComments(_Resource):

    async def list(
        self,
        *,
        artifact: str,
        status: Optional[Literal["all", "open", "resolved"]] = None,
        page: Optional[str] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Comment threads on an artifact, newest first.

        Threads: messages, anchor, viewed version (default `status: "open"`); status all
        includes resolved history. Publish the fix first, then respond with body explaining what
        changed and which version, plus resolve: true atomically. Reuse messageId on retry.
        Reports replied/resolved separately. resolve: false reopens. `screenshot` returns an
        image. Agents cannot open/delete threads. mentioned: true lists your @mentions, oldest
        unseen first, marking them seen.
        """
        return await self._client._call(
            "GET",
            "/v1/artifacts/{artifact}/comments",
            path_params={"artifact": artifact},
            query={"status": status, "page": page, "limit": limit, "cursor": cursor},
            timeout=timeout,
        )

    async def respond(
        self,
        *,
        artifact: str,
        respond: Optional[List[Dict[str, Any]]] = None,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Reply to and/or resolve threads, one outcome each.

        Threads: messages, anchor, viewed version (default `status: "open"`); status all
        includes resolved history. Publish the fix first, then respond with body explaining what
        changed and which version, plus resolve: true atomically. Reuse messageId on retry.
        Reports replied/resolved separately. resolve: false reopens. `screenshot` returns an
        image. Agents cannot open/delete threads. mentioned: true lists your @mentions, oldest
        unseen first, marking them seen.
        """
        return await self._client._call(
            "POST",
            "/v1/artifacts/{artifact}/comments/responses",
            path_params={"artifact": artifact},
            body={"respond": respond},
            idempotency_key=idempotency_key,
            timeout=timeout,
        )

    async def get_screenshot(
        self,
        *,
        artifact: str,
        screenshot: str,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """One message's screenshot, base64 in `image`.

        Threads: messages, anchor, viewed version (default `status: "open"`); status all
        includes resolved history. Publish the fix first, then respond with body explaining what
        changed and which version, plus resolve: true atomically. Reuse messageId on retry.
        Reports replied/resolved separately. resolve: false reopens. `screenshot` returns an
        image. Agents cannot open/delete threads. mentioned: true lists your @mentions, oldest
        unseen first, marking them seen.
        """
        return await self._client._call(
            "GET",
            "/v1/artifacts/{artifact}/comments/screenshots/{screenshot}",
            path_params={"artifact": artifact, "screenshot": screenshot},
            timeout=timeout,
        )


class AsyncMentions(_Resource):

    async def list(
        self,
        *,
        artifact: Optional[str] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Where people @mentioned you; listing marks them seen.

        Threads: messages, anchor, viewed version (default `status: "open"`); status all
        includes resolved history. Publish the fix first, then respond with body explaining what
        changed and which version, plus resolve: true atomically. Reuse messageId on retry.
        Reports replied/resolved separately. resolve: false reopens. `screenshot` returns an
        image. Agents cannot open/delete threads. mentioned: true lists your @mentions, oldest
        unseen first, marking them seen.
        """
        return await self._client._call(
            "GET",
            "/v1/mentions",
            query={"artifact": artifact, "limit": limit, "cursor": cursor},
            timeout=timeout,
        )

    def iter(self, **kwargs: Any) -> AsyncIterator[Dict[str, Any]]:
        """Every item of `list`, across pages. Takes the same arguments."""
        return awalk_cursor(self.list, "mentions", kwargs)


class AsyncSignatures(_Resource):

    async def list(
        self,
        *,
        artifact: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """An artifact's signature requests, newest first.

        Ask named people to sign one published version of an artifact, and follow the request.
        `request` with `artifact`, `signers` [{name, email, party?}] (≤10) and an optional
        `message` (≤500 characters) emails each signer a private link; the version must be one
        file of at most 2 MiB, and it is kept while the request is open and for good once it
        completes. `status` with `request` (one) or `artifact` (all, newest first). `withdraw`
        closes an open request. `remind` emails `signer` the link again, three times at most, a
        day apart. Only each signer can sign, in a browser, after a code sent to their address:
        an agent cannot.
        """
        return await self._client._call(
            "GET",
            "/v1/signatures",
            query={"artifact": artifact},
            timeout=timeout,
        )

    async def request(
        self,
        *,
        artifact: Optional[str] = None,
        version: Optional[int] = None,
        signers: Optional[List[Dict[str, Any]]] = None,
        message: Optional[str] = None,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Ask named people to sign one version of an artifact.

        Ask named people to sign one published version of an artifact, and follow the request.
        `request` with `artifact`, `signers` [{name, email, party?}] (≤10) and an optional
        `message` (≤500 characters) emails each signer a private link; the version must be one
        file of at most 2 MiB, and it is kept while the request is open and for good once it
        completes. `status` with `request` (one) or `artifact` (all, newest first). `withdraw`
        closes an open request. `remind` emails `signer` the link again, three times at most, a
        day apart. Only each signer can sign, in a browser, after a code sent to their address:
        an agent cannot.
        """
        return await self._client._call(
            "POST",
            "/v1/signatures",
            body={"artifact": artifact, "version": version, "signers": signers, "message": message},
            idempotency_key=idempotency_key,
            timeout=timeout,
        )

    async def get(
        self,
        *,
        request: str,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """One signature request and its signers.

        Ask named people to sign one published version of an artifact, and follow the request.
        `request` with `artifact`, `signers` [{name, email, party?}] (≤10) and an optional
        `message` (≤500 characters) emails each signer a private link; the version must be one
        file of at most 2 MiB, and it is kept while the request is open and for good once it
        completes. `status` with `request` (one) or `artifact` (all, newest first). `withdraw`
        closes an open request. `remind` emails `signer` the link again, three times at most, a
        day apart. Only each signer can sign, in a browser, after a code sent to their address:
        an agent cannot.
        """
        return await self._client._call(
            "GET",
            "/v1/signatures/{request}",
            path_params={"request": request},
            timeout=timeout,
        )

    async def remind(
        self,
        *,
        request: str,
        signer: Optional[str] = None,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Email a signer their link again.

        Ask named people to sign one published version of an artifact, and follow the request.
        `request` with `artifact`, `signers` [{name, email, party?}] (≤10) and an optional
        `message` (≤500 characters) emails each signer a private link; the version must be one
        file of at most 2 MiB, and it is kept while the request is open and for good once it
        completes. `status` with `request` (one) or `artifact` (all, newest first). `withdraw`
        closes an open request. `remind` emails `signer` the link again, three times at most, a
        day apart. Only each signer can sign, in a browser, after a code sent to their address:
        an agent cannot.
        """
        return await self._client._call(
            "POST",
            "/v1/signatures/{request}/remind",
            path_params={"request": request},
            body={"signer": signer},
            idempotency_key=idempotency_key,
            timeout=timeout,
        )

    async def withdraw(
        self,
        *,
        request: str,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Close an open signature request.

        Ask named people to sign one published version of an artifact, and follow the request.
        `request` with `artifact`, `signers` [{name, email, party?}] (≤10) and an optional
        `message` (≤500 characters) emails each signer a private link; the version must be one
        file of at most 2 MiB, and it is kept while the request is open and for good once it
        completes. `status` with `request` (one) or `artifact` (all, newest first). `withdraw`
        closes an open request. `remind` emails `signer` the link again, three times at most, a
        day apart. Only each signer can sign, in a browser, after a code sent to their address:
        an agent cannot.
        """
        return await self._client._call(
            "POST",
            "/v1/signatures/{request}/withdraw",
            path_params={"request": request},
            idempotency_key=idempotency_key,
            timeout=timeout,
        )


class AsyncResources:
    def __init__(self) -> None:
        self.account = AsyncAccount(self)
        self.artifacts = AsyncArtifacts(self)
        self.live = AsyncLive(self)
        self.uploads = AsyncUploads(self)
        self.data = AsyncData(self)
        self.schema = AsyncSchema(self)
        self.entries = AsyncEntries(self)
        self.secrets = AsyncSecrets(self)
        self.templates = AsyncTemplates(self)
        self.projects = AsyncProjects(self)
        self.shares = AsyncShares(self)
        self.comments = AsyncComments(self)
        self.mentions = AsyncMentions(self)
        self.signatures = AsyncSignatures(self)
