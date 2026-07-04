from __future__ import annotations

from rdflib import Graph, Namespace
from rdflib.namespace import RDF

from policygraph.materialize_graph import COMBINED_TTL
from tests.conftest import ensure_materialized_graph

EX = Namespace("https://example.org/policygraph/ontology#")
ID = Namespace("https://example.org/policygraph/id/")
CODE = Namespace("https://example.org/policygraph/code/")


def combined_graph() -> Graph:
    ensure_materialized_graph()
    graph = Graph()
    graph.parse(COMBINED_TTL, format="turtle")
    return graph


def test_policy_and_policyholder_triples_exist() -> None:
    graph = combined_graph()
    assert (ID["policy/P1001"], RDF.type, EX.Policy) in graph
    assert (ID["policy/P1001"], EX.hasPolicyholder, ID["customer/C001"]) in graph


def test_policy_coverages_exist() -> None:
    graph = combined_graph()
    assert (ID["policy/P1001"], EX.hasCoverage, ID["coverage/CVG9001"]) in graph
    assert (ID["policy/P1001"], EX.hasCoverage, ID["coverage/CVG9002"]) in graph


def test_claim_policy_link_exists() -> None:
    graph = combined_graph()
    assert (ID["claim/CLM7001"], EX.claimAgainstPolicy, ID["policy/P1001"]) in graph


def test_bad_claim_coverage_type_is_preserved() -> None:
    graph = combined_graph()
    assert (
        ID["claim/CLM7004"],
        EX.claimInvolvesCoverageType,
        CODE["coverage-type/UNLISTED_COVERAGE"],
    ) in graph
