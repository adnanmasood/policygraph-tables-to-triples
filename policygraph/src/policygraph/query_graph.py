"""Run named SPARQL queries against the combined PolicyGraph RDF graph."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from rdflib import Graph, Literal
from rdflib.query import Result

from policygraph.paths import QUERIES_DIR, RDF_DIR

COMBINED_GRAPH = RDF_DIR / "policygraph-combined.ttl"


def load_graph(path: Path = COMBINED_GRAPH) -> Graph:
    if not path.exists():
        raise FileNotFoundError(
            f"Missing {path}. Run python -m policygraph.materialize_graph first."
        )
    graph = Graph()
    graph.parse(path, format="turtle")
    return graph


def term_to_json(term: Any) -> str | None:
    if term is None:
        return None
    if isinstance(term, Literal):
        return str(term)
    return str(term)


def result_to_rows(result: Result) -> list[dict[str, str | None]]:
    rows: list[dict[str, str | None]] = []
    variables = [str(variable) for variable in result.vars or []]
    for row in result:
        rows.append({name: term_to_json(row[name]) for name in variables})
    return rows


def _read_query(query_path: Path) -> str:
    if not query_path.exists():
        raise FileNotFoundError(f"Missing query file: {query_path}")
    return query_path.read_text(encoding="utf-8")


def run_select_query(graph: Graph, query_path: Path) -> list[dict[str, str | None]]:
    return result_to_rows(graph.query(_read_query(query_path)))


def run_construct_query(graph: Graph, query_path: Path) -> Graph:
    result = graph.query(_read_query(query_path))
    constructed = Graph()
    for prefix, namespace in graph.namespaces():
        constructed.bind(prefix, namespace)
    for triple in result:
        constructed.add(triple)
    return constructed


def _query_path(query_name: str) -> Path:
    filename = query_name if query_name.endswith(".rq") else f"{query_name}.rq"
    return QUERIES_DIR / filename


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a PolicyGraph SPARQL query.")
    parser.add_argument("query_name", help="Query name such as active_policies.")
    parser.add_argument("--construct", action="store_true", help="Run as CONSTRUCT query.")
    args = parser.parse_args()

    graph = load_graph()
    query_path = _query_path(args.query_name)
    if args.construct:
        print(run_construct_query(graph, query_path).serialize(format="turtle"))
        return

    for row in run_select_query(graph, query_path):
        print(json.dumps(row, sort_keys=True))


if __name__ == "__main__":
    main()
