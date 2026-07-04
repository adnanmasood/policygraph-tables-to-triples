"""Shared project paths."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROFILING_DIR = DATA_DIR / "profiling"
ONTOLOGY_DIR = PROJECT_ROOT / "ontology"
MAPPINGS_DIR = PROJECT_ROOT / "mappings"
CONFIG_DIR = PROJECT_ROOT / "config"
RDF_DIR = PROJECT_ROOT / "rdf"
SHAPES_DIR = PROJECT_ROOT / "shapes"
QUERIES_DIR = PROJECT_ROOT / "queries"
