# Codex Build Notes

This repository was designed to be generated iteratively from the PolicyGraph
Codex prompt kit. The prompts are split by concern so each layer can be tested
before the next layer depends on it.

Recommended implementation order:

1. Repository bootstrap.
2. Sample data and table profiling.
3. Ontology builder and contract tests.
4. RML mapping and RDF materialization.
5. SHACL validation.
6. SPARQL query catalog.
7. Semantic service and query CLI.
8. FastAPI API.
9. Optional Docker/Fuseki local development.
10. Tests, CI, and quality gates.
11. Documentation and developer guide.
12. Final consistency review.

The separation prevents ontology generation, materialization, validation,
querying, and API behavior from being debugged as one large change.
