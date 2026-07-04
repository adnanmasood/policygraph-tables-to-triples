"""Run SHACL validation for the explicit PolicyGraph data graph."""

from __future__ import annotations

import argparse
import sys

from pyshacl import validate

from policygraph.paths import RDF_DIR, SHAPES_DIR

DATA_GRAPH = RDF_DIR / "policygraph-data.nt"
SHAPES_GRAPH = SHAPES_DIR / "policygraph.shacl.ttl"
REPORT_TTL = SHAPES_DIR / "validation-report.ttl"
REPORT_TXT = SHAPES_DIR / "validation-report.txt"


def run_validation() -> tuple[bool, str]:
    if not DATA_GRAPH.exists():
        raise FileNotFoundError(
            f"Missing {DATA_GRAPH}. Run python -m policygraph.materialize_graph first."
        )
    if not SHAPES_GRAPH.exists():
        raise FileNotFoundError(f"Missing {SHAPES_GRAPH}.")

    conforms, report_graph, report_text = validate(
        data_graph=str(DATA_GRAPH),
        shacl_graph=str(SHAPES_GRAPH),
        data_graph_format="nt",
        shacl_graph_format="turtle",
        inference="none",
        abort_on_first=False,
        allow_infos=True,
        allow_warnings=True,
        advanced=True,
        meta_shacl=False,
    )

    SHAPES_DIR.mkdir(parents=True, exist_ok=True)
    report_graph.serialize(destination=REPORT_TTL, format="turtle")
    REPORT_TXT.write_text(str(report_text), encoding="utf-8")
    return bool(conforms), str(report_text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate PolicyGraph RDF with SHACL.")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on violations.")
    args = parser.parse_args()

    conforms, report_text = run_validation()
    print(report_text)
    if args.strict and not conforms:
        sys.exit(1)


if __name__ == "__main__":
    main()
