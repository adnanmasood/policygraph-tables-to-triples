"""Application-facing semantic service over the PolicyGraph SPARQL catalog."""

from __future__ import annotations

from pathlib import Path

from rdflib import Graph

from policygraph.paths import QUERIES_DIR, RDF_DIR
from policygraph.query_graph import result_to_rows, run_construct_query

DEFAULT_GRAPH_PATH = RDF_DIR / "policygraph-combined.ttl"
DEFAULT_QUERIES_DIR = QUERIES_DIR


class PolicyGraphService:
    """Named application methods backed by SPARQL query files."""

    def __init__(
        self,
        graph_path: Path = DEFAULT_GRAPH_PATH,
        queries_dir: Path = DEFAULT_QUERIES_DIR,
    ) -> None:
        if not graph_path.exists():
            raise FileNotFoundError(
                f"Missing {graph_path}. Run python -m policygraph.materialize_graph first."
            )
        self.graph_path = graph_path
        self.queries_dir = queries_dir
        self.graph = Graph()
        self.graph.parse(graph_path, format="turtle")

    def _load_query(self, query_name: str) -> str:
        query_path = self.queries_dir / f"{query_name}.rq"
        if not query_path.exists():
            raise FileNotFoundError(f"Missing query file: {query_path}")
        return query_path.read_text(encoding="utf-8")

    def select(self, query_name: str) -> list[dict[str, str | None]]:
        return result_to_rows(self.graph.query(self._load_query(query_name)))

    def construct(self, query_name: str) -> str:
        query_path = self.queries_dir / f"{query_name}.rq"
        constructed = run_construct_query(self.graph, query_path)
        return constructed.serialize(format="turtle")

    def active_policies(self) -> list[dict[str, str | None]]:
        return self.select("active_policies")

    def open_claims(self) -> list[dict[str, str | None]]:
        return self.select("open_claims")

    def missing_policyholders(self) -> list[dict[str, str | None]]:
        return self.select("missing_policyholders")

    def claims_outside_policy_period(self) -> list[dict[str, str | None]]:
        return self.select("claims_outside_policy_period")

    def claims_with_unlisted_coverage_type(self) -> list[dict[str, str | None]]:
        return self.select("claims_with_unlisted_coverage_type")

    def account_context_for_customer_c001(self) -> str:
        return self.construct("account_context_construct")
