from __future__ import annotations

from fastapi.testclient import TestClient

from policygraph.api import app
from tests.conftest import ensure_materialized_graph


def client() -> TestClient:
    ensure_materialized_graph()
    return TestClient(app)


def values(rows: list[dict[str, str | None]], key: str) -> set[str | None]:
    return {row[key] for row in rows}


def test_health_route() -> None:
    response = client().get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_business_and_quality_routes() -> None:
    test_client = client()

    active = test_client.get("/policies/active")
    assert active.status_code == 200
    assert "CA-2026-0001" in values(active.json(), "policyNumber")

    open_claims = test_client.get("/claims/open")
    assert open_claims.status_code == 200
    assert "CL-2026-10001" in values(open_claims.json(), "claimNumber")

    missing = test_client.get("/quality/missing-policyholders")
    assert missing.status_code == 200
    assert "PL-2026-0192" in values(missing.json(), "policyNumber")

    outside = test_client.get("/quality/claims-outside-policy-period")
    assert outside.status_code == 200
    assert "CL-2026-10003" in values(outside.json(), "claimNumber")

    unlisted = test_client.get("/quality/claims-with-unlisted-coverage-type")
    assert unlisted.status_code == 200
    assert "CL-2026-10004" in values(unlisted.json(), "claimNumber")


def test_account_context_route_returns_turtle() -> None:
    response = client().get("/accounts/C001/context.ttl")
    assert response.status_code == 200
    assert "text/turtle" in response.headers["content-type"]
    assert "C001" in response.text
    assert "P1001" in response.text
