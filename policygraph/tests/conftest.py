from __future__ import annotations

from policygraph import build_ontology, materialize_graph, profile_tables, validate_graph


def ensure_profile_outputs() -> None:
    if (
        not profile_tables.TABLE_PROFILE_JSON.exists()
        or not profile_tables.FOREIGN_KEY_REPORT_JSON.exists()
    ):
        profile_tables.main()


def ensure_ontology() -> None:
    if not build_ontology.OUTPUT_PATH.exists():
        build_ontology.main()


def ensure_materialized_graph() -> None:
    ensure_ontology()
    if not materialize_graph.DATA_NT.exists() or not materialize_graph.COMBINED_TTL.exists():
        materialize_graph.main()


def ensure_validation_report() -> None:
    ensure_materialized_graph()
    if not validate_graph.REPORT_TXT.exists() or not validate_graph.REPORT_TTL.exists():
        validate_graph.run_validation()
