"""Materialize PolicyGraph CSV data into RDF and a combined ontology/data graph."""

from __future__ import annotations

import csv
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, XSD

from policygraph.paths import CONFIG_DIR, ONTOLOGY_DIR, RAW_DIR, RDF_DIR

CONFIG_PATH = CONFIG_DIR / "morph-kgc.ini"
ONTOLOGY_TTL = ONTOLOGY_DIR / "policygraph.ttl"
DATA_NT = RDF_DIR / "policygraph-data.nt"
DATA_TTL = RDF_DIR / "policygraph-data.ttl"
COMBINED_TTL = RDF_DIR / "policygraph-combined.ttl"

EX = Namespace("https://example.org/policygraph/ontology#")
ID = Namespace("https://example.org/policygraph/id/")
CODE = Namespace("https://example.org/policygraph/code/")


def _bind_namespaces(graph: Graph) -> None:
    graph.bind("ex", EX)
    graph.bind("id", ID)
    graph.bind("code", CODE)
    graph.bind("xsd", XSD)


def _require_file(path: Path, hint: str | None = None) -> None:
    if not path.exists():
        message = f"Missing {path}."
        if hint:
            message = f"{message} {hint}"
        raise FileNotFoundError(message)


def _read_csv(path: Path) -> Iterable[dict[str, str]]:
    _require_file(path)
    with path.open(newline="", encoding="utf-8") as csv_file:
        yield from csv.DictReader(csv_file)


def _literal(value: str, datatype: URIRef) -> Literal:
    return Literal(value, datatype=datatype)


def _iri(namespace: Namespace, local: str) -> URIRef:
    return URIRef(namespace[local])


def _materialize_with_morph_kgc() -> Graph | None:
    """Try Morph-KGC first; return None when local runtime support is unavailable."""
    try:
        import morph_kgc  # type: ignore[import-not-found]
    except ImportError:
        return None

    try:
        graph_result: Any = morph_kgc.materialize(str(CONFIG_PATH))
    except Exception as exc:
        print(f"Morph-KGC materialization failed; using RDFLib fallback. Error: {exc}")
        return None

    graph = Graph()
    _bind_namespaces(graph)
    if isinstance(graph_result, Graph):
        graph += graph_result
    elif DATA_NT.exists():
        graph.parse(DATA_NT, format="nt")
    if len(graph) == 0:
        return None
    return graph


def _materialize_with_rdflib() -> Graph:
    graph = Graph()
    _bind_namespaces(graph)

    for row in _read_csv(RAW_DIR / "customers.csv"):
        customer = _iri(ID, f"customer/{row['customer_id']}")
        graph.add((customer, RDF.type, EX.Customer))
        graph.add((customer, EX.customerIdentifier, _literal(row["customer_id"], XSD.string)))
        graph.add((customer, EX.legalName, _literal(row["legal_name"], XSD.string)))
        graph.add((customer, EX.emailAddress, _literal(row["email"], XSD.string)))
        graph.add((customer, EX.stateCode, _literal(row["state"], XSD.string)))

    for row in _read_csv(RAW_DIR / "policies.csv"):
        policy = _iri(ID, f"policy/{row['policy_id']}")
        graph.add((policy, RDF.type, EX.Policy))
        graph.add((policy, EX.policyIdentifier, _literal(row["policy_id"], XSD.string)))
        graph.add((policy, EX.policyNumber, _literal(row["policy_number"], XSD.string)))
        graph.add((policy, EX.productCode, _literal(row["product_code"], XSD.string)))
        graph.add((policy, EX.policyStartDate, _literal(row["start_date"], XSD.date)))
        graph.add((policy, EX.policyEndDate, _literal(row["end_date"], XSD.date)))
        graph.add((policy, EX.premiumAmount, _literal(row["premium_amount"], XSD.decimal)))
        graph.add((policy, EX.premiumCurrency, _literal(row["premium_currency"], XSD.string)))
        graph.add((policy, EX.hasPolicyholder, _iri(ID, f"customer/{row['customer_id']}")))
        graph.add((policy, EX.hasPolicyStatus, _iri(CODE, f"policy-status/{row['status']}")))

    for row in _read_csv(RAW_DIR / "coverages.csv"):
        coverage = _iri(ID, f"coverage/{row['coverage_id']}")
        policy = _iri(ID, f"policy/{row['policy_id']}")
        graph.add((coverage, RDF.type, EX.Coverage))
        graph.add((coverage, EX.coverageIdentifier, _literal(row["coverage_id"], XSD.string)))
        graph.add((coverage, EX.limitAmount, _literal(row["limit_amount"], XSD.decimal)))
        graph.add((coverage, EX.deductibleAmount, _literal(row["deductible_amount"], XSD.decimal)))
        graph.add((coverage, EX.coverageCurrency, _literal(row["currency"], XSD.string)))
        graph.add(
            (
                coverage,
                EX.hasCoverageType,
                _iri(CODE, f"coverage-type/{row['coverage_type']}"),
            )
        )
        graph.add((policy, EX.hasCoverage, coverage))

    for row in _read_csv(RAW_DIR / "claims.csv"):
        claim = _iri(ID, f"claim/{row['claim_id']}")
        graph.add((claim, RDF.type, EX.Claim))
        graph.add((claim, EX.claimIdentifier, _literal(row["claim_id"], XSD.string)))
        graph.add((claim, EX.claimNumber, _literal(row["claim_number"], XSD.string)))
        graph.add((claim, EX.lossDate, _literal(row["loss_date"], XSD.date)))
        graph.add((claim, EX.reportedDate, _literal(row["reported_date"], XSD.date)))
        graph.add((claim, EX.incurredAmount, _literal(row["incurred_amount"], XSD.decimal)))
        graph.add((claim, EX.paidAmount, _literal(row["paid_amount"], XSD.decimal)))
        graph.add((claim, EX.claimCurrency, _literal(row["currency"], XSD.string)))
        graph.add((claim, EX.claimAgainstPolicy, _iri(ID, f"policy/{row['policy_id']}")))
        graph.add((claim, EX.hasClaimStatus, _iri(CODE, f"claim-status/{row['claim_status']}")))
        graph.add(
            (
                claim,
                EX.claimInvolvesCoverageType,
                _iri(CODE, f"coverage-type/{row['coverage_type']}"),
            )
        )

    return graph


def materialize_data_graph() -> Graph:
    """Materialize source CSV data into an RDF data graph."""
    _require_file(CONFIG_PATH)
    _require_file(
        ONTOLOGY_TTL,
        "Run python -m policygraph.build_ontology first.",
    )
    RDF_DIR.mkdir(parents=True, exist_ok=True)
    return _materialize_with_morph_kgc() or _materialize_with_rdflib()


def build_combined_graph(data_graph: Graph) -> Graph:
    """Merge ontology triples and explicit data triples."""
    _require_file(
        ONTOLOGY_TTL,
        "Run python -m policygraph.build_ontology first.",
    )
    combined = Graph()
    _bind_namespaces(combined)
    combined.parse(ONTOLOGY_TTL, format="turtle")
    for triple in data_graph:
        combined.add(triple)
    return combined


def main() -> None:
    data_graph = materialize_data_graph()
    combined_graph = build_combined_graph(data_graph)
    RDF_DIR.mkdir(parents=True, exist_ok=True)
    data_graph.serialize(destination=DATA_NT, format="nt")
    data_graph.serialize(destination=DATA_TTL, format="turtle")
    combined_graph.serialize(destination=COMBINED_TTL, format="turtle")
    print(f"Wrote {DATA_NT} with {len(data_graph)} data triples")
    print(f"Wrote {DATA_TTL}")
    print(f"Wrote {COMBINED_TTL} with {len(combined_graph)} combined triples")


if __name__ == "__main__":
    main()
