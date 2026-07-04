from __future__ import annotations

from rdflib import Graph, Namespace

from policygraph.materialize_graph import COMBINED_TTL
from policygraph.paths import QUERIES_DIR
from policygraph.query_graph import run_construct_query, run_select_query
from tests.conftest import ensure_materialized_graph

EX = Namespace("https://example.org/policygraph/ontology#")


def graph() -> Graph:
    ensure_materialized_graph()
    result = Graph()
    result.parse(COMBINED_TTL, format="turtle")
    return result


def values(rows: list[dict[str, str | None]], key: str) -> set[str | None]:
    return {row[key] for row in rows}


def test_active_policies_query() -> None:
    rows = run_select_query(graph(), QUERIES_DIR / "active_policies.rq")
    assert {"CA-2026-0001", "GL-2026-0088", "PL-2026-0192"} <= values(rows, "policyNumber")


def test_open_claims_query() -> None:
    rows = run_select_query(graph(), QUERIES_DIR / "open_claims.rq")
    assert {"CL-2026-10001", "CL-2026-10003", "CL-2026-10004"} <= values(rows, "claimNumber")


def test_quality_queries() -> None:
    rdf_graph = graph()
    missing = run_select_query(rdf_graph, QUERIES_DIR / "missing_policyholders.rq")
    outside = run_select_query(rdf_graph, QUERIES_DIR / "claims_outside_policy_period.rq")
    unlisted = run_select_query(rdf_graph, QUERIES_DIR / "claims_with_unlisted_coverage_type.rq")
    assert "PL-2026-0192" in values(missing, "policyNumber")
    assert "CL-2026-10003" in values(outside, "claimNumber")
    assert "CL-2026-10004" in values(unlisted, "claimNumber")


def test_account_context_construct_query() -> None:
    constructed = run_construct_query(graph(), QUERIES_DIR / "account_context_construct.rq")
    turtle = constructed.serialize(format="turtle")
    assert len(constructed) > 0
    assert "C001" in turtle
    assert "P1001" in turtle
    assert (None, EX.policyNumber, None) in constructed
