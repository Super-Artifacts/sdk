"""Behaviour reachable from the public surface, over httpx.MockTransport."""

import asyncio
import json
import re
from pathlib import Path

import httpx
import pytest

import superartifacts as sa
from superartifacts import AsyncSuperArtifacts, RateLimitError, SuperArtifacts

SDKS = Path(__file__).resolve().parents[2]
SPEC = json.loads((SDKS / "openapi.json").read_text())
NAMES = json.loads((SDKS / "resources.json").read_text())
KEY = "sa_test_do_not_print"
OPERATIONS = [
    (http, path, operation)
    for path, item in SPEC["paths"].items()
    for http, operation in item.items()
]


def snake(name):
    return re.sub(r"(?<=[a-z0-9])([A-Z])", r"_\1", name).lower()


def handler_for(*answers, seen=None):
    """Answer each request with the next response, repeating the last."""
    answers = list(answers)
    seen = [] if seen is None else seen

    def handle(request):
        seen.append(request)
        answer = answers.pop(0) if len(answers) > 1 else answers[0]
        if isinstance(answer, Exception):
            raise answer
        return answer

    return handle


def client(*answers, seen=None, **options):
    transport = httpx.MockTransport(handler_for(*answers, seen=seen))
    return SuperArtifacts(api_key=KEY, http_client=httpx.Client(transport=transport), **options)


def async_client(*answers, seen=None, **options):
    transport = httpx.MockTransport(handler_for(*answers, seen=seen))
    http = httpx.AsyncClient(transport=transport)
    return AsyncSuperArtifacts(api_key=KEY, http_client=http, **options)


@pytest.fixture(autouse=True)
def waits(monkeypatch):
    """No real sleeping; the list holds what each client asked to wait."""
    slept = []

    async def nap(seconds):
        slept.append(seconds)

    monkeypatch.setattr("superartifacts._client.time.sleep", slept.append)
    monkeypatch.setattr("superartifacts._client.asyncio.sleep", nap)
    return slept


def sample(schema, name):
    if "enum" in schema:
        return schema["enum"][0]
    kind = schema.get("type")
    if kind == "integer":
        return 7
    if kind == "boolean":
        return True
    if kind == "array":
        return [sample(schema.get("items", {}), name)]
    if kind == "object":
        return {"a": 1}
    return f"{name}-value"


def arguments(operation):
    """Every field of an operation, as keyword arguments and where each must land."""
    kwargs, path, query = {}, {}, {}
    for param in operation.get("parameters", []):
        value = sample(param["schema"], param["name"])
        if param["name"] == "confirm":
            continue
        kwargs[snake(param["name"])] = value
        (path if param["in"] == "path" else query)[param["name"]] = value
    body_schema = operation.get("requestBody", {}).get("content", {})
    body_schema = body_schema.get("application/json", {}).get("schema", {})
    body = {}
    for wire, schema in body_schema.get("properties", {}).items():
        body[wire] = kwargs[snake(wire)] = sample(schema, wire)
    return kwargs, path, query, body


@pytest.mark.parametrize(("http", "path", "operation"), OPERATIONS, ids=lambda v: None)
def test_every_operation_splits_its_arguments_by_the_spec(http, path, operation):
    entry = NAMES[operation["operationId"]]
    kwargs, in_path, query, body = arguments(operation)
    seen = []
    sync = client(httpx.Response(200, json={"ok": 1}), seen=seen)
    fn = getattr(getattr(sync, entry["resource"]), snake(entry["method"]))
    assert fn(**kwargs) == {"ok": 1}

    request = seen[0]
    assert request.method == http.upper()
    expected = path
    for name, value in in_path.items():
        expected = expected.replace("{" + name + "}", str(value))
    assert request.url.path == expected
    sent = {}
    for name in request.url.params:
        values = request.url.params.get_list(name)
        sent[name] = values
    if any(p["name"] == "confirm" for p in operation.get("parameters", [])):
        first = next(iter(in_path.values()))
        assert sent.pop("confirm") == [str(first)]
    assert sent == {
        name: [str(v).lower() if isinstance(v, bool) else str(v) for v in value]
        if isinstance(value, list)
        else [str(value).lower() if isinstance(value, bool) else str(value)]
        for name, value in query.items()
    }
    if "requestBody" in operation:
        assert json.loads(request.content) == body
    else:
        assert request.content == b""
    assert request.headers["authorization"] == f"Bearer {KEY}"
    assert ("idempotency-key" in request.headers) == (http == "post")

    # Same operation on the async client, same request.
    aseen = []
    amock = async_client(httpx.Response(200, json={"ok": 1}), seen=aseen)
    afn = getattr(getattr(amock, entry["resource"]), snake(entry["method"]))
    assert asyncio.run(afn(**kwargs)) == {"ok": 1}
    assert aseen[0].method == request.method and aseen[0].url == request.url


def test_every_named_operation_is_in_the_spec():
    assert {operation["operationId"] for _, _, operation in OPERATIONS} == set(NAMES)


def test_a_snake_case_argument_goes_out_under_its_wire_name():
    seen = []
    client(httpx.Response(200, json={}), seen=seen).artifacts.publish(
        slug="s", prompt="p", values_file="proof.json"
    )
    assert json.loads(seen[0].content) == {"slug": "s", "prompt": "p", "valuesFile": "proof.json"}


def test_a_nullable_field_can_be_sent_as_null_and_left_out():
    seen = []
    projects = client(httpx.Response(200, json={}), seen=seen).projects
    projects.update(project="p", rule=None)
    projects.update(project="p", title="t")
    assert json.loads(seen[0].content) == {"rule": None}
    assert json.loads(seen[1].content) == {"title": "t"}


def test_headers_name_the_sdk():
    seen = []
    client(httpx.Response(200, json={}), seen=seen).account.whoami()
    assert seen[0].headers["user-agent"] == f"superartifacts-python/{sa.__version__}"
    assert seen[0].headers["accept"] == "application/json"
    assert "origin" not in seen[0].headers


@pytest.mark.parametrize(
    ("status", "code", "kind"),
    [
        (400, "invalid_filter", sa.InvalidArgumentsError),
        (401, "unauthorized", sa.AuthenticationError),
        (402, "plan_limit", sa.PlanLimitError),
        (403, "forbidden", sa.PermissionError),
        (403, "scope_required", sa.ScopeRequiredError),
        (404, "not_found", sa.NotFoundError),
        (409, "conflict", sa.ConflictError),
        (413, "payload_too_large", sa.PayloadTooLargeError),
        (500, "internal", sa.InternalError),
        (405, "method_not_allowed", sa.SuperArtifactsError),
    ],
)
def test_errors_map_by_status_and_code(status, code, kind):
    body = {"error": {"code": code, "message": "No.", "fix": "Do this."}}
    with pytest.raises(sa.SuperArtifactsError) as caught:
        client(httpx.Response(status, json=body), max_retries=0).account.whoami()
    assert type(caught.value) is kind
    assert (caught.value.status, caught.value.code) == (status, code)
    assert caught.value.message == "No."
    assert caught.value.details["fix"] == "Do this."


def test_a_non_json_error_body_still_raises_with_its_status():
    with pytest.raises(sa.InternalError) as caught:
        client(httpx.Response(502, text="<html>"), max_retries=0).account.whoami()
    assert caught.value.status == 502 and "502" in caught.value.message


def test_429_waits_retry_after_then_succeeds(waits):
    seen = []
    answers = (
        httpx.Response(429, headers={"retry-after": "7"}),
        httpx.Response(200, json={"a": 1}),
    )
    assert client(*answers, seen=seen).account.whoami() == {"a": 1}
    assert len(seen) == 2 and waits == [7]


def test_429_retry_after_past_a_minute_is_not_waited_out(waits):
    answers = (httpx.Response(429, headers={"retry-after": "9000"}), httpx.Response(200, json={}))
    with pytest.raises(RateLimitError) as caught:
        client(*answers).account.whoami()
    assert waits == [] and caught.value.retry_after == 9000


def test_429_is_retried_on_a_write_that_carries_no_key():
    seen = []
    answers = (httpx.Response(429, headers={"retry-after": "1"}), httpx.Response(200, json={}))
    client(*answers, seen=seen).artifacts.update(artifact="a", phase="x")
    assert len(seen) == 2


def test_429_gives_up_after_max_retries_with_retry_after():
    seen = []
    limited = httpx.Response(
        429, headers={"retry-after": "3"}, json={"error": {"code": "rate_limited", "message": "x"}}
    )
    with pytest.raises(sa.RateLimitError) as caught:
        client(limited, seen=seen, max_retries=2).account.whoami()
    assert len(seen) == 3 and caught.value.retry_after == 3


@pytest.mark.parametrize("status", [502, 503, 504])
def test_gateway_errors_retry_a_get_with_growing_backoff(status, waits):
    seen = []
    answers = (httpx.Response(status), httpx.Response(status), httpx.Response(200, json={}))
    client(*answers, seen=seen).account.whoami()
    assert len(seen) == 3
    assert 0.25 <= waits[0] <= 0.5 and 0.5 <= waits[1] <= 1


def test_500_is_not_retried():
    seen = []
    with pytest.raises(sa.InternalError):
        client(httpx.Response(500), seen=seen).account.whoami()
    assert len(seen) == 1


def test_400_is_not_retried():
    seen = []
    with pytest.raises(sa.InvalidArgumentsError):
        client(httpx.Response(400), seen=seen).account.whoami()
    assert len(seen) == 1


def test_a_patch_is_not_retried_on_503():
    seen = []
    with pytest.raises(sa.InternalError):
        client(httpx.Response(503), seen=seen).artifacts.update(artifact="a", phase="x")
    assert len(seen) == 1


def test_a_post_without_a_key_is_not_retried():
    # Every generated POST carries a key, so only the rule itself can show this.
    sync = client(httpx.Response(503))
    assert sync._retry_delay("POST", {"headers": {}}, 0, 503) is None


def test_a_post_retries_on_503_under_one_automatic_key():
    seen = []
    answers = (httpx.Response(503), httpx.Response(503), httpx.Response(200, json={}))
    client(*answers, seen=seen).artifacts.publish(slug="s", prompt="p")
    keys = {request.headers["idempotency-key"] for request in seen}
    assert len(seen) == 3 and len(keys) == 1


def test_two_calls_get_two_keys_and_a_callers_key_wins():
    seen = []
    publish = client(httpx.Response(200, json={}), seen=seen).artifacts.publish
    publish(slug="s", prompt="p")
    publish(slug="s", prompt="p")
    publish(slug="s", prompt="p", idempotency_key="mine")
    keys = [request.headers["idempotency-key"] for request in seen]
    assert len(set(keys)) == 3 and keys[2] == "mine"


def test_a_network_error_retries_a_get_then_raises():
    seen = []
    with pytest.raises(sa.APIConnectionError) as caught:
        client(httpx.ConnectError("nope"), seen=seen, max_retries=1).account.whoami()
    assert len(seen) == 2
    assert (caught.value.status, caught.value.code) == (0, "connection_error")


def test_a_timeout_raises_its_own_error():
    with pytest.raises(sa.APITimeoutError) as caught:
        client(httpx.ReadTimeout("slow"), max_retries=0).account.whoami()
    assert (caught.value.status, caught.value.code) == (0, "timeout")


def test_a_network_error_is_not_retried_on_a_patch():
    seen = []
    with pytest.raises(sa.APIConnectionError):
        client(httpx.ConnectError("nope"), seen=seen).artifacts.update(artifact="a", phase="x")
    assert len(seen) == 1


def test_async_retries_share_the_rules(waits):
    seen = []
    answers = (
        httpx.Response(429, headers={"retry-after": "2"}),
        httpx.Response(200, json={"a": 1}),
    )
    assert asyncio.run(async_client(*answers, seen=seen).account.whoami()) == {"a": 1}
    assert len(seen) == 2 and waits == [2]


def test_async_post_keeps_its_key_across_retries():
    seen = []
    answers = (httpx.Response(504), httpx.Response(200, json={}))
    asyncio.run(async_client(*answers, seen=seen).artifacts.publish(slug="s", prompt="p"))
    assert seen[0].headers["idempotency-key"] == seen[1].headers["idempotency-key"]


def test_a_delete_repeats_its_id_as_confirm():
    seen = []
    sync = client(httpx.Response(200, json={}), seen=seen)
    sync.artifacts.delete(artifact="my-page")
    sync.projects.delete(project="my project")
    assert seen[0].url.params["confirm"] == "my-page"
    assert seen[1].url.params["confirm"] == "my project"
    assert seen[1].url.raw_path.startswith(b"/v1/projects/my%20project?")


def test_a_missing_key_says_what_to_do(monkeypatch):
    monkeypatch.delenv("SUPERARTIFACTS_API_KEY", raising=False)
    with pytest.raises(sa.AuthenticationError, match="SUPERARTIFACTS_API_KEY") as caught:
        SuperArtifacts()
    assert (caught.value.status, caught.value.code) == (0, "missing_api_key")
    assert caught.value.message == (
        "No API key. Pass api_key= or set SUPERARTIFACTS_API_KEY. "
        "Create one at https://superartifacts.app/settings/api-keys."
    )
    with pytest.raises(sa.AuthenticationError, match="SUPERARTIFACTS_API_KEY"):
        AsyncSuperArtifacts()


def test_the_key_comes_from_the_environment(monkeypatch):
    monkeypatch.setenv("SUPERARTIFACTS_API_KEY", KEY)
    with SuperArtifacts() as sync:
        assert sync._api_key == KEY


def test_the_key_is_never_in_a_repr_or_a_message():
    sync = client(httpx.Response(401, json={"error": {"code": "unauthorized", "message": "No."}}))
    with pytest.raises(sa.AuthenticationError) as caught:
        sync.account.whoami()
    assert KEY not in repr(sync) and KEY not in repr(caught.value) and KEY not in str(caught.value)


def test_a_passed_http_client_stays_open_and_an_owned_one_closes():
    http = httpx.Client(transport=httpx.MockTransport(handler_for(httpx.Response(200, json={}))))
    with SuperArtifacts(api_key=KEY, http_client=http):
        pass
    assert not http.is_closed
    owned = SuperArtifacts(api_key=KEY)
    owned.close()
    assert owned._http.is_closed


def rows(*ids, next_cursor=None):
    return httpx.Response(
        200,
        json={"responses": [{"id": i} for i in ids], "cursor": {"next": next_cursor}},
    )


def test_iter_rows_walks_the_cursor():
    seen = []
    sync = client(rows(1, 2, next_cursor="c2"), rows(3), seen=seen)
    assert [r["id"] for r in sync.data.iter_rows(dataset="d", limit=2)] == [1, 2, 3]
    assert "cursor" not in seen[0].url.params
    assert seen[1].url.params["cursor"] == "c2" and seen[1].url.params["dataset"] == "d"


def test_async_iter_rows_walks_the_cursor():
    seen = []

    async def walk():
        mock = async_client(rows(1, next_cursor="c2"), rows(2), seen=seen)
        return [row["id"] async for row in mock.data.iter_artifact_rows(artifact="a")]

    assert asyncio.run(walk()) == [1, 2]
    assert seen[1].url.params["cursor"] == "c2"


def test_mentions_page_by_cursor_next():
    first = httpx.Response(200, json={"mentions": [{"id": 1}], "cursorNext": "c2"})
    last = httpx.Response(200, json={"mentions": [{"id": 2}], "cursorNext": None})
    seen = []
    assert [m["id"] for m in client(first, last, seen=seen).mentions.iter()] == [1, 2]
    assert seen[1].url.params["cursor"] == "c2"


def entries(page, *ids):
    body = {"entries": [{"id": i} for i in ids], "page": page, "pageSize": 2, "total": 3}
    return httpx.Response(200, json=body)


def test_entries_walk_pages_and_stop_at_the_total():
    seen = []
    found = client(entries(0, 1, 2), entries(1, 3), seen=seen).entries.iter(collection="c")
    assert [e["id"] for e in found] == [1, 2, 3]
    assert [request.url.params["page"] for request in seen] == ["0", "1"]


def test_async_entries_walk_pages():
    async def walk():
        mock = async_client(entries(0, 1, 2), entries(1, 3))
        return [entry["id"] async for entry in mock.entries.iter(collection="c")]

    assert asyncio.run(walk()) == [1, 2, 3]


def test_an_answer_without_the_list_is_an_error_not_an_empty_walk():
    sync = client(httpx.Response(200, json={"artifacts": []}))
    with pytest.raises(sa.SuperArtifactsError, match="responses"):
        list(sync.data.iter_rows(collection="c"))


STAGED = {
    "uploadId": "up_1",
    "uploads": [
        {"path": "a.bin", "bytes": 3, "url": "https://up.example/a"},
        {"path": "b.txt", "bytes": 5, "url": "https://up.example/b"},
    ],
}


def test_upload_stages_then_puts_without_the_key(tmp_path):
    local = tmp_path / "b.txt"
    local.write_bytes(b"hello")
    seen = []
    answers = (httpx.Response(200, json=STAGED), httpx.Response(200))
    staged = client(*answers, seen=seen).uploads.upload({"a.bin": b"abc", "b.txt": local})

    assert staged["uploadId"] == "up_1"
    assert json.loads(seen[0].content) == {
        "files": [{"path": "a.bin", "bytes": 3}, {"path": "b.txt", "bytes": 5}]
    }
    assert [(r.method, str(r.url), r.content) for r in seen[1:]] == [
        ("PUT", "https://up.example/a", b"abc"),
        ("PUT", "https://up.example/b", b"hello"),
    ]
    assert all("authorization" not in request.headers for request in seen[1:])


def test_a_refused_put_raises():
    answers = (httpx.Response(200, json=STAGED), httpx.Response(400))
    with pytest.raises(sa.InvalidArgumentsError):
        client(*answers).uploads.upload({"a.bin": b"abc", "b.txt": b"hello"})


def test_async_upload_puts_without_the_key():
    seen = []
    answers = (httpx.Response(200, json=STAGED), httpx.Response(200))
    mock = async_client(*answers, seen=seen)
    asyncio.run(mock.uploads.upload({"a.bin": b"abc", "b.txt": b"hello"}))
    assert [r.method for r in seen] == ["POST", "PUT", "PUT"]
    assert "authorization" not in seen[1].headers
