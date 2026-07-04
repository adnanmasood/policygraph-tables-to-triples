PYTHON ?= python

.PHONY: install profile ontology materialize validate validate-strict query-active-policies query-open-claims test lint format clean all fuseki-up fuseki-down fuseki-load fuseki-query-open-claims

install:
	$(PYTHON) -m pip install -e ".[dev]"

profile:
	$(PYTHON) -m policygraph.profile_tables

ontology:
	$(PYTHON) -m policygraph.build_ontology

materialize:
	$(PYTHON) -m policygraph.materialize_graph

validate:
	$(PYTHON) -m policygraph.validate_graph

validate-strict:
	$(PYTHON) -m policygraph.validate_graph --strict

query-active-policies:
	$(PYTHON) -m policygraph.query_graph active_policies

query-open-claims:
	$(PYTHON) -m policygraph.query_graph open_claims

test:
	$(PYTHON) -m pytest -q

lint:
	$(PYTHON) -m ruff check .

format:
	$(PYTHON) -m ruff format .

clean:
	rm -f data/profiling/*.json
	rm -f rdf/*.nt rdf/*.ttl
	rm -f shapes/validation-report.ttl shapes/validation-report.txt
	rm -rf .pytest_cache .mypy_cache .ruff_cache src/*.egg-info
	find . -type d -name __pycache__ -prune -exec rm -rf {} +

all: profile ontology materialize validate test

fuseki-up:
	docker compose up -d

fuseki-down:
	docker compose down

fuseki-load:
	scripts/load_fuseki.sh

fuseki-query-open-claims:
	scripts/query_fuseki.sh queries/open_claims.rq
