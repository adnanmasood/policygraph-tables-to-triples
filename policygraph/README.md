# PolicyGraph

PolicyGraph is a small, runnable semantic data engineering application. It shows
how fictional insurance CSV files can be profiled, converted into RDF, described
with an ontology, validated with SHACL, queried with SPARQL, and exposed through
a Python service layer and FastAPI API.

The project is intentionally tutorial-sized, but it is organized like production
software: source data, semantic artifacts, typed Python modules, command-line
entry points, tests, CI, documentation, and optional local SPARQL server support.

## What This Project Demonstrates

PolicyGraph answers a common data engineering question:

> How do we turn ordinary tabular operational data into a semantic graph that
> can be validated, queried, and reused by applications?

The source data starts as four CSV files:

- customers
- policies
- coverages
- claims

The application turns those rows into an RDF knowledge graph with explicit
business meaning:

- a `Policy` has a policyholder;
- a `Policy` has one or more coverages;
- a `Claim` is against a policy;
- policy, claim, and coverage codes are represented as controlled concepts;
- known data quality issues are preserved and then detected by validation and
  quality queries.

## Pipeline Overview

```text
CSV files
  -> profiling
  -> ontology
  -> RML mappings
  -> RDF materialization
  -> combined ontology + data graph
  -> SHACL validation
  -> SPARQL query catalog
  -> semantic service
  -> FastAPI API
  -> optional Fuseki SPARQL endpoint
```

Each stage has a clear input, output, command, and purpose. Generated artifacts
can be deleted and rebuilt from the checked-in source files.

## Quick Start

Use Python 3.11 or newer.

```bash
cd /Users/adnanmasood/Downloads/policygraph_codex_prompts/policygraph
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Run the full local pipeline:

```bash
make all
```

Or run the core commands one by one:

```bash
python -m policygraph.profile_tables
python -m policygraph.build_ontology
python -m policygraph.materialize_graph
python -m policygraph.validate_graph
python -m policygraph.query_graph active_policies
python -m policygraph.query_graph open_claims
pytest -q
```

`python -m policygraph.validate_graph` is expected to report that the sample data
does not conform. That is intentional. The tutorial dataset contains known data
quality issues so validation and quality queries have something meaningful to
detect.

## Repository Layout

```text
policygraph/
  data/
    raw/                 Source CSV files
    profiling/           Generated profiling reports
  ontology/              Generated OWL/RDFS ontology
  mappings/              RML mapping from CSV rows to RDF
  config/                Morph-KGC configuration
  rdf/                   Generated RDF data and combined graph files
  shapes/                SHACL shapes and generated validation reports
  queries/               Reusable SPARQL query catalog
  src/policygraph/       Python package, CLI modules, service, and API
  tests/                 pytest coverage
  docs/                  Additional developer and modeling notes
  scripts/               Optional Fuseki helper scripts
```

Generated profiling, RDF, and validation-report files are ignored by Git because
they can be regenerated from the source CSVs, ontology builder, mapping, and
SHACL shapes.

## Domain Model

The application uses fictional insurance data. It does not use real customer
data.

### Source Tables

| CSV file | Meaning | Primary identifier |
| --- | --- | --- |
| `data/raw/customers.csv` | Policyholders and account parties | `customer_id` |
| `data/raw/policies.csv` | Insurance policies issued to customers | `policy_id` |
| `data/raw/coverages.csv` | Coverage components on policies | `coverage_id` |
| `data/raw/claims.csv` | Claims filed against policies | `claim_id` |

### Semantic Classes

The ontology defines these core classes:

| Class | Meaning |
| --- | --- |
| `Customer` | A person or organization that holds policies |
| `Policy` | An insurance contract issued to a customer |
| `Coverage` | A coverage component included on a policy |
| `Claim` | A reported loss against an insurance policy |
| `PolicyStatus` | A controlled policy lifecycle status |
| `ClaimStatus` | A controlled claim handling status |
| `CoverageType` | A controlled type of policy coverage |

### Main Relationships

| Relationship | Meaning |
| --- | --- |
| `ex:hasPolicyholder` | Policy -> Customer |
| `ex:hasCoverage` | Policy -> Coverage |
| `ex:claimAgainstPolicy` | Claim -> Policy |
| `ex:hasPolicyStatus` | Policy -> PolicyStatus |
| `ex:hasClaimStatus` | Claim -> ClaimStatus |
| `ex:hasCoverageType` | Coverage -> CoverageType |
| `ex:claimInvolvesCoverageType` | Claim -> CoverageType |

### Namespaces

PolicyGraph uses stable example namespaces:

```text
Ontology terms: https://example.org/policygraph/ontology#
Entity IRIs:    https://example.org/policygraph/id/
Code IRIs:      https://example.org/policygraph/code/
```

Example entity IRIs:

```text
https://example.org/policygraph/id/customer/C001
https://example.org/policygraph/id/policy/P1001
https://example.org/policygraph/id/coverage/CVG9001
https://example.org/policygraph/id/claim/CLM7001
```

Example code IRIs:

```text
https://example.org/policygraph/code/policy-status/ACTIVE
https://example.org/policygraph/code/claim-status/OPEN
https://example.org/policygraph/code/coverage-type/AUTO_LIABILITY
```

## Intentional Data Quality Issues

The sample data intentionally contains three defects:

| Issue | Source row | Expected detection |
| --- | --- | --- |
| Policy references a missing customer | `P1004` -> `C999` | Profiling, SHACL, SPARQL quality query |
| Claim loss date is outside policy period | `CLM7003` against `P1003` | SHACL, SPARQL quality query |
| Claim uses coverage type not listed on policy | `CLM7004` uses `UNLISTED_COVERAGE` on `P1001` | SHACL, SPARQL quality query |

The materializer must not fix these rows. It faithfully converts the source
facts into RDF. Validation and query layers detect the defects afterward.

## Definitions

### RDF

RDF means Resource Description Framework. It represents data as triples:

```text
subject -> predicate -> object
```

Example:

```text
policy/P1001 -> hasPolicyholder -> customer/C001
```

This says policy `P1001` has customer `C001` as its policyholder.

### Triple

A triple is one RDF statement. The subject is the thing being described, the
predicate is the relationship or attribute, and the object is another resource or
literal value.

### Graph

An RDF graph is a set of triples. PolicyGraph creates a data graph from CSVs, an
ontology graph from Python code, and a combined graph used for SPARQL queries.

### IRI

An IRI is a globally scoped identifier for a resource. PolicyGraph uses readable
example IRIs like `https://example.org/policygraph/id/policy/P1001`.

### Ontology

An ontology defines the vocabulary and intended meaning of a domain. In this
project, `ontology/policygraph.ttl` defines classes such as `Policy` and
relationships such as `hasPolicyholder`.

### OWL and RDFS

OWL and RDFS are RDF vocabulary languages. PolicyGraph uses them to declare
classes, properties, labels, comments, domains, ranges, and a few open-world
semantic restrictions.

### SKOS

SKOS is a standard way to represent controlled vocabularies and concept schemes.
PolicyGraph uses SKOS for policy statuses, claim statuses, and coverage types.

### RML

RML means RDF Mapping Language. It describes how rows from source files become
RDF triples. PolicyGraph keeps its mapping in `mappings/policygraph.rml.ttl`.

### Morph-KGC

Morph-KGC is the preferred RML materialization engine used by PolicyGraph. It
reads `config/morph-kgc.ini` and `mappings/policygraph.rml.ttl` to generate RDF.
The local tutorial code also has a deterministic RDFLib fallback if Morph-KGC is
not available in a runtime.

### RDFLib

RDFLib is a Python library for creating, parsing, serializing, and querying RDF
graphs. PolicyGraph uses RDFLib for ontology generation, graph merging, query
execution, and fallback materialization.

### SHACL

SHACL means Shapes Constraint Language. It validates RDF graphs with closed-world
quality rules. PolicyGraph uses SHACL to check required fields, datatypes,
missing policyholders, claim dates, and claim coverage consistency.

### SPARQL

SPARQL is the query language for RDF graphs. PolicyGraph stores reusable SPARQL
queries in `queries/*.rq`.

### SELECT Query

A SPARQL SELECT query returns table-like rows. PolicyGraph uses SELECT queries
for active policies, open claims, and data quality findings.

### CONSTRUCT Query

A SPARQL CONSTRUCT query returns RDF triples. PolicyGraph uses a CONSTRUCT query
to build an account context subgraph for customer `C001`.

### Semantic Service

The semantic service is the Python application layer in
`src/policygraph/semantic_service.py`. It hides RDFLib and SPARQL mechanics
behind named methods such as `active_policies()` and `open_claims()`.

### FastAPI

FastAPI is the web framework used for the HTTP API in `src/policygraph/api.py`.
The API route handlers are intentionally thin and delegate to the semantic
service.

### Fuseki

Apache Jena Fuseki is an optional local SPARQL server. PolicyGraph can load the
combined graph into Fuseki for querying outside RDFLib.

### Data Graph

The data graph contains explicit triples materialized from the CSV rows. In this
project it is generated as:

```text
rdf/policygraph-data.nt
rdf/policygraph-data.ttl
```

### Ontology Graph

The ontology graph contains domain vocabulary and semantic definitions. It is
generated as:

```text
ontology/policygraph.ttl
```

### Combined Graph

The combined graph merges the ontology graph and data graph. Application SPARQL
queries run against:

```text
rdf/policygraph-combined.ttl
```

### Shapes Graph

The shapes graph contains SHACL validation rules:

```text
shapes/policygraph.shacl.ttl
```

### Validation Report

The validation report is generated by pySHACL and explains whether the data graph
conforms to the shapes graph:

```text
shapes/validation-report.ttl
shapes/validation-report.txt
```

## How It Works

### 1. Source CSV Files

Inputs:

```text
data/raw/customers.csv
data/raw/policies.csv
data/raw/coverages.csv
data/raw/claims.csv
```

Command:

```text
No command required.
```

Outputs:

```text
None yet.
```

Inspect:

- customer IDs, policy IDs, coverage IDs, and claim IDs;
- foreign-key-like columns such as `customer_id` and `policy_id`;
- intentional data defects.

Why this step exists:

The CSV files are the operational source data. Everything else in the project is
generated from or checked against these files.

### 2. Table Profiling

Inputs:

```text
data/raw/*.csv
```

Command:

```bash
python -m policygraph.profile_tables
```

Outputs:

```text
data/profiling/table_profile.json
data/profiling/foreign_key_report.json
```

Inspect:

- row counts;
- column names;
- primary key uniqueness;
- missing parent value `C999`.

Why this step exists:

Profiling makes source structure and basic quality issues visible before any RDF
or ontology work begins.

### 3. Ontology Generation

Inputs:

```text
src/policygraph/build_ontology.py
```

Command:

```bash
python -m policygraph.build_ontology
```

Outputs:

```text
ontology/policygraph.ttl
```

Inspect:

- OWL classes;
- object properties;
- datatype properties;
- SKOS concept schemes.

Why this step exists:

The ontology gives business meaning to graph terms. It says what a `Policy` is,
what `hasPolicyholder` means, and which datatypes are expected for dates and
amounts.

### 4. RML Mapping

Inputs:

```text
mappings/policygraph.rml.ttl
config/morph-kgc.ini
data/raw/*.csv
```

Command:

```text
The mapping is consumed by the materialization command.
```

Outputs:

```text
No standalone output until materialization runs.
```

Inspect:

- subject IRI templates;
- CSV column references;
- datatype mappings;
- object-property mappings from foreign keys.

Why this step exists:

The RML mapping is the declarative contract between tabular rows and RDF triples.

### 5. RDF Materialization

Inputs:

```text
data/raw/*.csv
mappings/policygraph.rml.ttl
config/morph-kgc.ini
ontology/policygraph.ttl
```

Command:

```bash
python -m policygraph.materialize_graph
```

Outputs:

```text
rdf/policygraph-data.nt
rdf/policygraph-data.ttl
rdf/policygraph-combined.ttl
```

Inspect:

- policy `P1001` has policyholder `C001`;
- policy `P1001` has coverages `CVG9001` and `CVG9002`;
- claim `CLM7004` still references `UNLISTED_COVERAGE`.

Why this step exists:

Materialization turns CSV records into graph facts. It also creates the combined
graph used by application queries.

### 6. SHACL Validation

Inputs:

```text
rdf/policygraph-data.nt
shapes/policygraph.shacl.ttl
```

Command:

```bash
python -m policygraph.validate_graph
```

Strict mode:

```bash
python -m policygraph.validate_graph --strict
```

Outputs:

```text
shapes/validation-report.ttl
shapes/validation-report.txt
```

Inspect:

- `Policy must point to an existing Customer resource.`
- `Claim loss date is outside the policy effective period.`
- `Claim coverage type is not listed as a coverage type on the policy.`

Why this step exists:

SHACL performs closed-world quality checks against the explicit data graph. The
non-strict command prints the report and exits normally. Strict mode exits
non-zero when violations are found.

### 7. SPARQL Query Catalog

Inputs:

```text
rdf/policygraph-combined.ttl
queries/*.rq
```

Commands:

```bash
python -m policygraph.query_graph active_policies
python -m policygraph.query_graph open_claims
python -m policygraph.query_graph missing_policyholders
python -m policygraph.query_graph claims_outside_policy_period
python -m policygraph.query_graph claims_with_unlisted_coverage_type
python -m policygraph.query_graph account_context_construct --construct
```

Outputs:

```text
JSON rows for SELECT queries
Turtle for the CONSTRUCT query
```

Inspect:

- active policies include `CA-2026-0001`, `GL-2026-0088`, and `PL-2026-0192`;
- open claims include `CL-2026-10001`, `CL-2026-10003`, and `CL-2026-10004`;
- quality queries return the intentional defects.

Why this step exists:

SPARQL turns the graph into reusable application answers and quality reports.

### 8. Semantic Service

Inputs:

```text
rdf/policygraph-combined.ttl
queries/*.rq
```

Command:

```text
Used by tests and the API.
```

Public methods:

```text
active_policies()
open_claims()
missing_policyholders()
claims_outside_policy_period()
claims_with_unlisted_coverage_type()
account_context_for_customer_c001()
```

Outputs:

```text
JSON-compatible Python rows or Turtle strings
```

Inspect:

```text
src/policygraph/semantic_service.py
```

Why this step exists:

Applications should call named domain methods rather than embedding SPARQL
directly in route handlers or UI code.

### 9. FastAPI API

Inputs:

```text
rdf/policygraph-combined.ttl
PolicyGraphService
```

Command:

```bash
uvicorn policygraph.api:app --reload
```

Routes:

```text
GET /health
GET /policies/active
GET /claims/open
GET /quality/missing-policyholders
GET /quality/claims-outside-policy-period
GET /quality/claims-with-unlisted-coverage-type
GET /accounts/C001/context.ttl
```

Outputs:

```text
JSON responses for SELECT-backed routes
text/turtle response for the account context route
```

Inspect:

- `http://127.0.0.1:8000/health`
- `http://127.0.0.1:8000/policies/active`
- `http://127.0.0.1:8000/accounts/C001/context.ttl`

Why this step exists:

The API shows how a semantic graph can sit behind a normal application interface.

### 10. Optional Fuseki SPARQL Endpoint

Inputs:

```text
rdf/policygraph-combined.ttl
docker-compose.yml
scripts/load_fuseki.sh
scripts/query_fuseki.sh
```

Commands:

```bash
make fuseki-up
make fuseki-load
make fuseki-query-open-claims
make fuseki-down
```

Outputs:

```text
Local SPARQL endpoint at http://localhost:3030/policygraph/sparql
```

Inspect:

- Fuseki container status;
- query responses from `scripts/query_fuseki.sh`.

Why this step exists:

Fuseki is useful when you want to query the graph through a SPARQL server rather
than through RDFLib in Python. It is optional and not required for tests.

## Make Targets

| Target | What it does |
| --- | --- |
| `make install` | Install the package with development dependencies |
| `make profile` | Run CSV profiling |
| `make ontology` | Generate `ontology/policygraph.ttl` |
| `make materialize` | Generate RDF data and combined graph files |
| `make validate` | Run non-strict SHACL validation |
| `make validate-strict` | Run SHACL validation and exit non-zero on violations |
| `make query-active-policies` | Run the active policies query |
| `make query-open-claims` | Run the open claims query |
| `make test` | Run pytest |
| `make lint` | Run Ruff checks |
| `make format` | Format Python files with Ruff |
| `make clean` | Remove generated profiling, RDF, validation, and cache files |
| `make all` | Run profile, ontology, materialize, validate, and test |
| `make fuseki-up` | Start optional local Fuseki container |
| `make fuseki-down` | Stop optional local Fuseki container |
| `make fuseki-load` | Load combined graph into Fuseki |
| `make fuseki-query-open-claims` | Query open claims through Fuseki |

## API Usage

Build the graph first:

```bash
python -m policygraph.build_ontology
python -m policygraph.materialize_graph
```

Start the API:

```bash
uvicorn policygraph.api:app --reload
```

Example requests:

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/policies/active
curl http://127.0.0.1:8000/claims/open
curl http://127.0.0.1:8000/quality/missing-policyholders
curl http://127.0.0.1:8000/accounts/C001/context.ttl
```

The API loads the combined graph from `rdf/policygraph-combined.ttl`. If that
file is missing, graph-backed routes return an HTTP 500 with a message telling
the developer to run materialization first.

## Quality Gates

Run the normal local gate:

```bash
make all
ruff check .
```

Run strict validation when you want a shell-level failure for the tutorial
violations:

```bash
python -m policygraph.validate_graph --strict
```

Expected result:

```text
exit code 1
```

This is not a broken build. It confirms the intentionally invalid sample data is
being detected.

## Troubleshooting

### `Missing rdf/policygraph-combined.ttl`

The graph has not been generated yet. Run:

```bash
python -m policygraph.build_ontology
python -m policygraph.materialize_graph
```

### `validate_graph --strict` fails

This is expected with the tutorial dataset. The sample data intentionally
contains three violations. Use non-strict validation for the normal pipeline:

```bash
python -m policygraph.validate_graph
```

### Morph-KGC is missing or fails in a local runtime

Morph-KGC is the preferred RML engine. The tutorial materializer attempts to use
it first. If it cannot be imported or fails locally, the code uses an equivalent
RDFLib fallback so the tutorial pipeline can still run.

### API route returns a graph-not-built error

Run materialization before starting or calling graph-backed routes:

```bash
python -m policygraph.build_ontology
python -m policygraph.materialize_graph
uvicorn policygraph.api:app --reload
```

### Fuseki is not running

Fuseki is optional. The Python tests and core tutorial workflow do not require
Docker. To use Fuseki:

```bash
make fuseki-up
make fuseki-load
make fuseki-query-open-claims
```

Then shut it down:

```bash
make fuseki-down
```

### Generated files are missing after `make clean`

That is expected. `make clean` removes generated profiling, RDF, validation, and
cache files. Rebuild them with:

```bash
make all
```

## Additional Documentation

The README is designed to be self-contained. More focused notes are available in
`docs/`:

- `docs/competency_questions.md`: maps business questions to queries, service
  methods, and API routes.
- `docs/modeling_notes.md`: explains modeling choices and open-world versus
  closed-world assumptions.
- `docs/pipeline_walkthrough.md`: gives a step-by-step pipeline walkthrough.
- `docs/semantic_artifacts.md`: explains each semantic artifact.
- `docs/codex_build_notes.md`: records the prompt-driven build sequence.

## Current Known Behavior

- The tutorial dataset is intentionally non-conforming.
- `validate_graph` without `--strict` exits normally after printing the report.
- `validate_graph --strict` exits non-zero for the tutorial dataset.
- Docker and Fuseki are optional local development tools, not required pipeline
  dependencies.
- The readable example IRIs are appropriate for a tutorial. Production systems
  should use governed namespaces and avoid putting sensitive data in identifiers.
