# PolicyGraph Codex Prompt Kit

This zip contains a sequential prompt kit for generating the **PolicyGraph** representative application described in Part 1 and Part 2 of the article series:

- Part 1: ontology design from tabular insurance data
- Part 2: RDF materialization, SHACL validation, SPARQL querying, and semantic service/API layer

The prompts are written to be copied into Codex one at a time. Each prompt assumes Codex is operating inside the repository root and can edit files, run commands, and summarize results.

## Recommended order

1. `prompts/00_master_application_spec.md`
2. `prompts/01_repo_bootstrap.md`
3. `prompts/02_sample_data_and_profiler.md`
4. `prompts/03_ontology_builder_and_contract_tests.md`
5. `prompts/04_rml_mapping_and_materialization.md`
6. `prompts/05_shacl_validation.md`
7. `prompts/06_sparql_query_catalog.md`
8. `prompts/07_semantic_service_and_cli.md`
9. `prompts/08_fastapi_api.md`
10. `prompts/09_docker_fuseki_local_dev.md`
11. `prompts/10_tests_ci_and_quality_gates.md`
12. `prompts/11_documentation_and_developer_guide.md`
13. `prompts/12_final_review_and_refactor.md`

Optional prompts:

- `prompts/13_single_pass_mvp_prompt.md` — one-shot MVP build prompt if you prefer a single Codex task.
- `prompts/14_production_hardening_prompt.md` — extension prompt after the tutorial application works.
- `prompts/15_agent_tooling_extension_prompt.md` — adds an agent/tool-facing layer for later GraphRAG or workflow integration.

## Usage pattern

For best results, paste the master spec first. Then paste one implementation prompt at a time. After each prompt, let Codex modify files and run the acceptance commands. If tests fail, ask Codex to inspect the failure and patch only the smallest necessary area.

The prompts intentionally separate concerns:

- Ontology generation is separate from RDF materialization.
- Materialization is separate from SHACL validation.
- SPARQL queries are separate from the service/API layer.
- Application code is separate from Docker/Fuseki local deployment.

This prevents Codex from trying to build the entire application in one large, hard-to-debug patch.

## Target application

PolicyGraph is a Python application that demonstrates this pipeline:

```text
CSV files
  -> profiling
  -> ontology
  -> RML mappings
  -> RDF materialization
  -> SHACL validation
  -> SPARQL query catalog
  -> semantic service
  -> optional FastAPI API
  -> optional Fuseki local deployment
```

The expected domain is fictional insurance data:

- Customers
- Policies
- Coverages
- Claims
- Policy statuses
- Claim statuses
- Coverage types

The project is intentionally small but structured like production software: typed Python modules, CLI entry points, tests, documentation, and repeatable local commands.
