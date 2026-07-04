# Pipeline Walkthrough

## 1. Source CSV Files

- Inputs: `data/raw/customers.csv`, `policies.csv`, `coverages.csv`, `claims.csv`
- Command: none
- Inspect: row values and the intentional data issues.

## 2. Profiling Outputs

- Inputs: `data/raw/*.csv`
- Outputs: `data/profiling/table_profile.json`, `foreign_key_report.json`
- Command: `python -m policygraph.profile_tables`
- Inspect: missing parent value `C999`.

## 3. Ontology Generation

- Inputs: `src/policygraph/build_ontology.py`
- Output: `ontology/policygraph.ttl`
- Command: `python -m policygraph.build_ontology`
- Inspect: classes, object properties, datatype properties, and SKOS schemes.

## 4. RML Mapping

- Input: `mappings/policygraph.rml.ttl`
- Output: mapping declarations consumed by the materializer
- Command: none
- Inspect: subject IRI templates and datatype/object property maps.

## 5. RDF Materialization

- Inputs: `data/raw/*.csv`, `mappings/policygraph.rml.ttl`, `config/morph-kgc.ini`
- Outputs: `rdf/policygraph-data.nt`, `rdf/policygraph-data.ttl`
- Command: `python -m policygraph.materialize_graph`
- Inspect: policyholder, coverage, and claim triples.

## 6. Combined Graph

- Inputs: `ontology/policygraph.ttl`, `rdf/policygraph-data.nt`
- Output: `rdf/policygraph-combined.ttl`
- Command: `python -m policygraph.materialize_graph`
- Inspect: ontology and data triples in one graph.

## 7. SHACL Validation

- Inputs: `rdf/policygraph-data.nt`, `shapes/policygraph.shacl.ttl`
- Outputs: `shapes/validation-report.ttl`, `validation-report.txt`
- Command: `python -m policygraph.validate_graph`
- Inspect: the three expected validation messages.

## 8. SPARQL Queries

- Inputs: `rdf/policygraph-combined.ttl`, `queries/*.rq`
- Outputs: SELECT rows or CONSTRUCT Turtle on stdout
- Commands: `python -m policygraph.query_graph active_policies`,
  `python -m policygraph.query_graph account_context_construct --construct`
- Inspect: active policies, open claims, and quality query results.

## 9. Semantic Service

- Inputs: combined graph and query catalog
- Output: JSON-compatible rows or Turtle strings from named methods
- Command: exercised through tests or API routes
- Inspect: `src/policygraph/semantic_service.py`.

## 10. API

- Inputs: `PolicyGraphService`
- Output: HTTP JSON and Turtle responses
- Command: `uvicorn policygraph.api:app --reload`
- Inspect: `/health`, `/policies/active`, and quality endpoints.
