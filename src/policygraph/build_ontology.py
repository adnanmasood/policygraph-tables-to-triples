"""Generate the PolicyGraph OWL/RDFS ontology."""

from __future__ import annotations

from rdflib import BNode, Graph, Literal, Namespace, URIRef
from rdflib.namespace import DCTERMS, OWL, RDF, RDFS, SKOS, XSD

from policygraph.paths import ONTOLOGY_DIR

ONTOLOGY_IRI = URIRef("https://example.org/policygraph/ontology")
EX = Namespace("https://example.org/policygraph/ontology#")
CODE = Namespace("https://example.org/policygraph/code/")
OUTPUT_PATH = ONTOLOGY_DIR / "policygraph.ttl"


def bind_namespaces(graph: Graph) -> None:
    graph.bind("ex", EX)
    graph.bind("code", CODE)
    graph.bind("owl", OWL)
    graph.bind("rdf", RDF)
    graph.bind("rdfs", RDFS)
    graph.bind("skos", SKOS)
    graph.bind("xsd", XSD)
    graph.bind("dcterms", DCTERMS)


def add_class(graph: Graph, cls: URIRef, label: str, comment: str | None = None) -> None:
    graph.add((cls, RDF.type, OWL.Class))
    graph.add((cls, RDFS.label, Literal(label)))
    if comment:
        graph.add((cls, RDFS.comment, Literal(comment)))


def add_object_property(
    graph: Graph,
    prop: URIRef,
    label: str,
    domain: URIRef,
    range_: URIRef,
    comment: str | None = None,
) -> None:
    graph.add((prop, RDF.type, OWL.ObjectProperty))
    graph.add((prop, RDFS.label, Literal(label)))
    graph.add((prop, RDFS.domain, domain))
    graph.add((prop, RDFS.range, range_))
    if comment:
        graph.add((prop, RDFS.comment, Literal(comment)))


def add_datatype_property(
    graph: Graph,
    prop: URIRef,
    label: str,
    domain: URIRef,
    datatype: URIRef,
    comment: str | None = None,
) -> None:
    graph.add((prop, RDF.type, OWL.DatatypeProperty))
    graph.add((prop, RDFS.label, Literal(label)))
    graph.add((prop, RDFS.domain, domain))
    graph.add((prop, RDFS.range, datatype))
    if comment:
        graph.add((prop, RDFS.comment, Literal(comment)))


def add_some_values_from_restriction(
    graph: Graph,
    cls: URIRef,
    prop: URIRef,
    value_cls: URIRef,
) -> None:
    restriction = BNode()
    graph.add((restriction, RDF.type, OWL.Restriction))
    graph.add((restriction, OWL.onProperty, prop))
    graph.add((restriction, OWL.someValuesFrom, value_cls))
    graph.add((cls, RDFS.subClassOf, restriction))


def add_concept_scheme(graph: Graph, scheme: URIRef, label: str, concepts: dict[str, str]) -> None:
    graph.add((scheme, RDF.type, SKOS.ConceptScheme))
    graph.add((scheme, SKOS.prefLabel, Literal(label)))
    for notation, pref_label in concepts.items():
        concept = URIRef(f"{scheme}/{notation}")
        graph.add((concept, RDF.type, SKOS.Concept))
        graph.add((concept, SKOS.inScheme, scheme))
        graph.add((concept, SKOS.notation, Literal(notation)))
        graph.add((concept, SKOS.prefLabel, Literal(pref_label)))


def build_graph() -> Graph:
    graph = Graph()
    bind_namespaces(graph)

    graph.add((ONTOLOGY_IRI, RDF.type, OWL.Ontology))
    graph.add((ONTOLOGY_IRI, DCTERMS.title, Literal("PolicyGraph Ontology")))
    graph.add(
        (
            ONTOLOGY_IRI,
            DCTERMS.description,
            Literal(
                "A representative ontology for transforming insurance policy, coverage, "
                "customer, and claim CSV files into an RDF knowledge graph."
            ),
        )
    )

    add_class(graph, EX.Customer, "Customer", "A person or organization that holds policies.")
    add_class(graph, EX.Policy, "Policy", "An insurance contract issued to a customer.")
    add_class(graph, EX.Coverage, "Coverage", "A coverage component included on a policy.")
    add_class(graph, EX.Claim, "Claim", "A reported loss against an insurance policy.")
    add_class(graph, EX.PolicyStatus, "Policy status", "A controlled policy lifecycle status.")
    add_class(graph, EX.ClaimStatus, "Claim status", "A controlled claim handling status.")
    add_class(graph, EX.CoverageType, "Coverage type", "A controlled type of policy coverage.")

    object_properties = [
        (EX.hasPolicyholder, "has policyholder", EX.Policy, EX.Customer),
        (EX.hasCoverage, "has coverage", EX.Policy, EX.Coverage),
        (EX.claimAgainstPolicy, "claim against policy", EX.Claim, EX.Policy),
        (EX.hasPolicyStatus, "has policy status", EX.Policy, EX.PolicyStatus),
        (EX.hasClaimStatus, "has claim status", EX.Claim, EX.ClaimStatus),
        (EX.hasCoverageType, "has coverage type", EX.Coverage, EX.CoverageType),
        (
            EX.claimInvolvesCoverageType,
            "claim involves coverage type",
            EX.Claim,
            EX.CoverageType,
        ),
    ]
    for prop, label, domain, range_ in object_properties:
        add_object_property(
            graph,
            prop,
            label,
            domain,
            range_,
            f"Relates a {domain.split('#')[-1]} to a {range_.split('#')[-1]}.",
        )

    datatype_properties = [
        (EX.customerIdentifier, "customer identifier", EX.Customer, XSD.string),
        (EX.legalName, "legal name", EX.Customer, XSD.string),
        (EX.emailAddress, "email address", EX.Customer, XSD.string),
        (EX.stateCode, "state code", EX.Customer, XSD.string),
        (EX.policyIdentifier, "policy identifier", EX.Policy, XSD.string),
        (EX.policyNumber, "policy number", EX.Policy, XSD.string),
        (EX.productCode, "product code", EX.Policy, XSD.string),
        (EX.policyStartDate, "policy start date", EX.Policy, XSD.date),
        (EX.policyEndDate, "policy end date", EX.Policy, XSD.date),
        (EX.premiumAmount, "premium amount", EX.Policy, XSD.decimal),
        (EX.premiumCurrency, "premium currency", EX.Policy, XSD.string),
        (EX.coverageIdentifier, "coverage identifier", EX.Coverage, XSD.string),
        (EX.limitAmount, "limit amount", EX.Coverage, XSD.decimal),
        (EX.deductibleAmount, "deductible amount", EX.Coverage, XSD.decimal),
        (EX.coverageCurrency, "coverage currency", EX.Coverage, XSD.string),
        (EX.claimIdentifier, "claim identifier", EX.Claim, XSD.string),
        (EX.claimNumber, "claim number", EX.Claim, XSD.string),
        (EX.lossDate, "loss date", EX.Claim, XSD.date),
        (EX.reportedDate, "reported date", EX.Claim, XSD.date),
        (EX.incurredAmount, "incurred amount", EX.Claim, XSD.decimal),
        (EX.paidAmount, "paid amount", EX.Claim, XSD.decimal),
        (EX.claimCurrency, "claim currency", EX.Claim, XSD.string),
    ]
    for prop, label, domain, datatype in datatype_properties:
        add_datatype_property(graph, prop, label, domain, datatype)

    # These are open-world OWL semantics; closed-world quality checks live in SHACL.
    add_some_values_from_restriction(graph, EX.Policy, EX.hasPolicyholder, EX.Customer)
    add_some_values_from_restriction(graph, EX.Policy, EX.hasCoverage, EX.Coverage)
    add_some_values_from_restriction(graph, EX.Claim, EX.claimAgainstPolicy, EX.Policy)

    add_concept_scheme(
        graph,
        CODE["policy-status"],
        "Policy status",
        {"ACTIVE": "Active", "EXPIRED": "Expired", "CANCELLED": "Cancelled"},
    )
    add_concept_scheme(
        graph,
        CODE["claim-status"],
        "Claim status",
        {"OPEN": "Open", "CLOSED": "Closed"},
    )
    add_concept_scheme(
        graph,
        CODE["coverage-type"],
        "Coverage type",
        {
            "AUTO_LIABILITY": "Auto liability",
            "PHYSICAL_DAMAGE": "Physical damage",
            "GENERAL_LIABILITY": "General liability",
            "PERSONAL_AUTO": "Personal auto",
        },
    )
    return graph


def main() -> None:
    graph = build_graph()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    graph.serialize(destination=OUTPUT_PATH, format="turtle")
    print(f"Wrote {OUTPUT_PATH} with {len(graph)} triples")


if __name__ == "__main__":
    main()
