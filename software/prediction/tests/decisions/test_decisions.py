import hashlib
import json
from datetime import datetime, timezone
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from src.decisions.adapters.sqlite_repository import SqliteDecisionRepository
from src.decisions.domain.decision import (
    Decision, DecisionType, DuplicateDecisionError, Role,
)
from src.service.app import app

SECRET = "test-secret"
GW = {"X-Green-Gateway-Secret": SECRET}
OPERATOR = {"X-Green-User-Id": "user-1", "X-Green-User-Role": "OPERATOR", **GW}
VIEWER = {"X-Green-User-Id": "user-2", "X-Green-User-Role": "VIEWER", **GW}


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("DECISIONS_DB_PATH", str(tmp_path / "sub" / "decisions.db"))
    monkeypatch.delenv("DECISIONS_ENABLED", raising=False)
    monkeypatch.setenv("GATEWAY_SHARED_SECRET", SECRET)
    return TestClient(app)


def make_rec(rec_id=None, execution_allowed=False):
    resource = {"type": "node", "id": "n1", "cluster": "lab"}
    return {
        "recommendationId": rec_id or str(uuid4()),
        "generatedAt": "2026-11-19T22:00:00Z", "predictionId": "p1", "inputDatasetId": "ds1",
        "predictedCpuPercent": 25.0, "telemetry": None, "resource": resource,
        "status": "not_evaluable", "action": "none", "executionAllowed": execution_allowed,
        "policy": {"mode": "demonstration", "cpuLowPercent": 30, "cpuHighPercent": 80,
                   "memoryMaxPercent": 85, "latencyP95MaxMs": 500, "errorRateMaxPercent": 1,
                   "freshnessSeconds": 300},
        "checks": [{"name": "prediction_freshness", "status": "unknown"}],
        "warnings": ["Requiere revisión humana."],
    }


def url(rec):
    return f"/v1/recommendations/{rec['recommendationId']}/decisions"


def post(client, rec, headers=OPERATOR, **extra):
    body = {"decision": "APPROVED", "comment": "ok", "recommendation": rec, **extra}
    return client.post(url(rec), json=body, headers=headers)


def test_create_201_with_hash(client):
    rec = make_rec()
    r = post(client, rec)
    assert r.status_code == 201
    body = r.json()
    assert body["recommendationId"] == rec["recommendationId"]
    assert body["decision"] == "APPROVED" and body["comment"] == "ok"
    assert body["decidedBy"] == "user-1" and body["decidedByRole"] == "OPERATOR"
    assert body["executionAllowed"] is False
    assert body["decidedAt"].endswith("Z")
    canonical = json.dumps(rec, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    assert body["recommendationSha256"] == hashlib.sha256(canonical.encode()).hexdigest()


@pytest.mark.parametrize("headers", [GW, {**GW, "X-Green-User-Id": "u"}, {**GW, "X-Green-User-Role": "ADMIN"}])
def test_401_without_identity_headers(client, headers):
    rec = make_rec()
    r = post(client, rec, headers=headers)
    assert r.status_code == 401
    assert r.headers["content-type"].startswith("application/problem+json")
    assert client.get(url(rec), headers=headers).status_code == 401


def test_403_viewer_post_but_viewer_can_get(client):
    rec = make_rec()
    r = post(client, rec, headers=VIEWER)
    assert r.status_code == 403
    assert r.headers["content-type"].startswith("application/problem+json")
    assert client.get(url(rec), headers=VIEWER).status_code == 200


def test_409_duplicate_by_user_but_other_user_allowed(client):
    rec = make_rec()
    assert post(client, rec).status_code == 201
    dup = post(client, rec)
    assert dup.status_code == 409
    assert dup.headers["content-type"].startswith("application/problem+json")
    assert dup.json()["status"] == 409
    other = {"X-Green-User-Id": "user-3", "X-Green-User-Role": "ADMIN", **GW}
    assert post(client, rec, headers=other).status_code == 201


def test_422_id_mismatch_and_execution_allowed(client):
    rec = make_rec()
    other = make_rec()
    r = client.post(url(rec), headers=OPERATOR,
                    json={"decision": "REJECTED", "recommendation": other})
    assert r.status_code == 422
    assert r.headers["content-type"].startswith("application/problem+json")
    assert post(client, make_rec(execution_allowed=True)).status_code == 422
    assert client.post("/v1/recommendations/not-a-uuid/decisions", headers=OPERATOR,
                       json={"decision": "APPROVED", "recommendation": rec}).status_code == 422
    assert post(client, rec, comment="x" * 501).status_code == 422
    assert client.post(url(rec), headers=OPERATOR,
                       json={"decision": "MAYBE", "recommendation": rec}).status_code == 422


def test_503_without_configured_secret_fails_closed(client, monkeypatch):
    monkeypatch.delenv("GATEWAY_SHARED_SECRET")
    rec = make_rec()
    r = post(client, rec)
    assert r.status_code == 503
    assert r.headers["content-type"].startswith("application/problem+json")
    assert "GATEWAY_SHARED_SECRET" in r.json()["detail"]
    assert client.get(url(rec), headers=OPERATOR).status_code == 503


@pytest.mark.parametrize("secret", [None, "", "wrong"])
def test_401_missing_or_wrong_gateway_secret(client, secret):
    rec = make_rec()
    headers = {"X-Green-User-Id": "u", "X-Green-User-Role": "ADMIN"}
    if secret is not None:
        headers["X-Green-Gateway-Secret"] = secret
    assert post(client, rec, headers=headers).status_code == 401
    assert client.get(url(rec), headers=headers).status_code == 401


def test_get_lists_decisions(client):
    rec = make_rec()
    assert client.get(url(rec), headers=OPERATOR).json() == {
        "recommendationId": rec["recommendationId"], "decisions": []}
    post(client, rec)
    post(client, rec, headers={"X-Green-User-Id": "user-9", "X-Green-User-Role": "ADMIN", **GW},
         decision="REJECTED")
    body = client.get(url(rec), headers=VIEWER).json()
    assert [d["decidedBy"] for d in body["decisions"]] == ["user-1", "user-9"]
    assert body["decisions"][1]["decision"] == "REJECTED"


def test_flag_disabled_returns_404(client, monkeypatch):
    monkeypatch.setenv("DECISIONS_ENABLED", "false")
    rec = make_rec()
    r = post(client, rec)
    assert r.status_code == 404
    assert r.headers["content-type"].startswith("application/problem+json")
    assert client.get(url(rec), headers=OPERATOR).status_code == 404


def test_repository_persists_between_instances(tmp_path):
    path = tmp_path / "d" / "decisions.db"
    d = Decision("id-1", "rec-1", DecisionType.APPROVED, None, "u1", Role.ADMIN,
                 datetime(2026, 11, 19, 22, 0, tzinfo=timezone.utc), "a" * 64)
    SqliteDecisionRepository(path).add(d)
    again = SqliteDecisionRepository(path)
    assert again.list_by_recommendation("rec-1") == [d]
    with pytest.raises(DuplicateDecisionError):
        again.add(Decision("id-2", "rec-1", DecisionType.REJECTED, "c", "u1", Role.ADMIN,
                           d.decided_at, "b" * 64))


def test_domain_rejects_execution_allowed():
    with pytest.raises(ValueError):
        Decision("i", "r", DecisionType.APPROVED, None, "u", Role.ADMIN,
                 datetime.now(timezone.utc), "a" * 64, execution_allowed=True)


def test_openapi_documents_decision_routes(client):
    paths = client.get("/openapi.json").json()["paths"]
    route = paths["/v1/recommendations/{recommendationId}/decisions"]
    assert {"get", "post"} <= set(route)
    assert {"201", "401", "403", "409", "422"} <= set(route["post"]["responses"])
