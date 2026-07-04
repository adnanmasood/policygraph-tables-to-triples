from __future__ import annotations

from rdflib import Graph
from rdflib.namespace import OWL, RDF, RDFS, SKOS, XSD

from policygraph.build_ontology import CODE, EX, OUTPUT_PATH
from tests.conftest import ensure_ontology


def ontology_graph() -> Graph:
    ensure_ontology()
    graph = Graph()
    graph.parse(OUTPUT_PATH, format="turtle")
    return graph


def test_core_classes_exist() -> None:
    graph = ontology_graph()
    for cls in [EX.Customer, EX.Policy, EX.Coverage, EX.Claim]:
        assert (cls, RDF.type, OWL.Class) in graph


def test_core_object_properties_have_domain_and_range() -> None:
    graph = ontology_graph()
    expectations = {
        EX.hasPolicyholder: (EX.Policy, EX.Customer),
        EX.hasCoverage: (EX.Policy, EX.Coverage),
        EX.claimAgainstPolicy: (EX.Claim, EX.Policy),
    }
    for prop, (domain, range_) in expectations.items():
        assert (prop, RDF.type, OWL.ObjectProperty) in graph
        assert (prop, RDFS.domain, domain) in graph
        assert (prop, RDFS.range, range_) in graph


def test_date_and_monetary_properties_use_expected_datatypes() -> None:
    graph = ontology_graph()
    for prop in [EX.policyStartDate, EX.policyEndDate, EX.lossDate, EX.reportedDate]:
        assert (prop, RDFS.range, XSD.date) in graph
    for prop in [EX.premiumAmount, EX.limitAmount, EX.deductibleAmount, EX.incurredAmount]:
        assert (prop, RDFS.range, XSD.decimal) in graph


def test_skos_concept_schemes_exist() -> None:
    graph = ontology_graph()
    for scheme in [CODE["policy-status"], CODE["claim-status"], CODE["coverage-type"]]:
        assert (scheme, RDF.type, SKOS.ConceptScheme) in graph
