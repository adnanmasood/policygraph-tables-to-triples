from __future__ import annotations

import pytest

from policygraph.semantic_service import PolicyGraphService
from tests.conftest import ensure_materialized_graph


def service() -> PolicyGraphService:
    ensure_materialized_graph()
    return PolicyGraphService()


def values(rows: list[dict[str, str | None]], key: str) -> set[str | None]:
    return {row[key] for row in rows}


def test_named_select_methods_return_expected_records() -> None:
    semantic_service = service()
    assert "CA-2026-0001" in values(semantic_service.active_policies(), "policyNumber")
    assert "CL-2026-10001" in values(semantic_service.open_claims(), "claimNumber")
    assert "PL-2026-0192" in values(semantic_service.missing_policyholders(), "policyNumber")
    assert "CL-2026-10003" in values(
        semantic_service.claims_outside_policy_period(),
        "claimNumber",
    )
    assert "CL-2026-10004" in values(
        semantic_service.claims_with_unlisted_coverage_type(),
        "claimNumber",
    )


def test_account_context_returns_turtle() -> None:
    turtle = service().account_context_for_customer_c001()
    assert "C001" in turtle
    assert "P1001" in turtle


def test_missing_query_raises_file_not_found() -> None:
    with pytest.raises(FileNotFoundError):
        service().select("does_not_exist")
