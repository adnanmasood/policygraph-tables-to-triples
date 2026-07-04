"""FastAPI routes for the PolicyGraph semantic service."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException, Response

from policygraph.semantic_service import PolicyGraphService

app = FastAPI(title="PolicyGraph Semantic API")


def get_service() -> PolicyGraphService:
    return PolicyGraphService()


def _service_or_500() -> PolicyGraphService:
    try:
        return get_service()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "policygraph"}


@app.get("/policies/active")
def active_policies() -> list[dict[str, str | None]]:
    return _service_or_500().active_policies()


@app.get("/claims/open")
def open_claims() -> list[dict[str, str | None]]:
    return _service_or_500().open_claims()


@app.get("/quality/missing-policyholders")
def missing_policyholders() -> list[dict[str, str | None]]:
    return _service_or_500().missing_policyholders()


@app.get("/quality/claims-outside-policy-period")
def claims_outside_policy_period() -> list[dict[str, str | None]]:
    return _service_or_500().claims_outside_policy_period()


@app.get("/quality/claims-with-unlisted-coverage-type")
def claims_with_unlisted_coverage_type() -> list[dict[str, str | None]]:
    return _service_or_500().claims_with_unlisted_coverage_type()


@app.get("/accounts/C001/context.ttl")
def account_context_for_customer_c001() -> Response:
    turtle = _service_or_500().account_context_for_customer_c001()
    return Response(content=turtle, media_type="text/turtle")
