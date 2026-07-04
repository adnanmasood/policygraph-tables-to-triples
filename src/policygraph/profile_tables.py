"""Profile source CSV tables and simple foreign-key-like relationships."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from policygraph.paths import PROFILING_DIR, RAW_DIR

TABLE_FILES = {
    "customers": RAW_DIR / "customers.csv",
    "policies": RAW_DIR / "policies.csv",
    "coverages": RAW_DIR / "coverages.csv",
    "claims": RAW_DIR / "claims.csv",
}

PRIMARY_KEYS = {
    "customers": "customer_id",
    "policies": "policy_id",
    "coverages": "coverage_id",
    "claims": "claim_id",
}

FOREIGN_KEYS = [
    {
        "child_table": "policies",
        "child_column": "customer_id",
        "parent_table": "customers",
        "parent_column": "customer_id",
    },
    {
        "child_table": "coverages",
        "child_column": "policy_id",
        "parent_table": "policies",
        "parent_column": "policy_id",
    },
    {
        "child_table": "claims",
        "child_column": "policy_id",
        "parent_table": "policies",
        "parent_column": "policy_id",
    },
]

TABLE_PROFILE_JSON = PROFILING_DIR / "table_profile.json"
FOREIGN_KEY_REPORT_JSON = PROFILING_DIR / "foreign_key_report.json"


def _require_file(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Missing {path}. Ensure the sample CSV files exist.")


def load_tables() -> dict[str, pd.DataFrame]:
    """Load all source CSVs as string data frames."""
    tables: dict[str, pd.DataFrame] = {}
    for table_name, path in TABLE_FILES.items():
        _require_file(path)
        tables[table_name] = pd.read_csv(path, dtype=str).fillna("")
    return tables


def profile_column(series: pd.Series) -> dict[str, Any]:
    """Return deterministic, JSON-compatible column profile facts."""
    present = series[series != ""]
    sample_values = sorted(present.drop_duplicates().astype(str).tolist())[:5]
    return {
        "rows": int(len(series)),
        "empty_count": int((series == "").sum()),
        "distinct_count": int(series.nunique(dropna=False)),
        "sample_values": sample_values,
        "is_unique_when_present": bool(present.is_unique),
    }


def profile_tables(tables: dict[str, pd.DataFrame]) -> dict[str, Any]:
    """Profile row counts, columns, and primary keys for every table."""
    profile: dict[str, Any] = {}
    for table_name in sorted(tables):
        frame = tables[table_name]
        primary_key = PRIMARY_KEYS[table_name]
        key_series = frame[primary_key]
        profile[table_name] = {
            "row_count": int(len(frame)),
            "column_count": int(len(frame.columns)),
            "columns": {column: profile_column(frame[column]) for column in frame.columns},
            "primary_key": {
                "column": primary_key,
                "missing_count": int((key_series == "").sum()),
                "is_unique": bool(key_series[key_series != ""].is_unique),
            },
        }
    return profile


def check_foreign_keys(tables: dict[str, pd.DataFrame]) -> list[dict[str, Any]]:
    """Check configured foreign-key-like relationships without mutating data."""
    reports: list[dict[str, Any]] = []
    for relationship in FOREIGN_KEYS:
        child_values = set(
            tables[relationship["child_table"]][relationship["child_column"]]
            .loc[lambda values: values != ""]
            .astype(str)
        )
        parent_values = set(
            tables[relationship["parent_table"]][relationship["parent_column"]]
            .loc[lambda values: values != ""]
            .astype(str)
        )
        missing_parent_values = sorted(child_values - parent_values)
        reports.append(
            {
                **relationship,
                "child_distinct_values": sorted(child_values),
                "parent_distinct_values": sorted(parent_values),
                "missing_parent_values": missing_parent_values,
                "missing_parent_count": len(missing_parent_values),
            }
        )
    return reports


def main() -> None:
    """Write profile and foreign-key reports."""
    tables = load_tables()
    PROFILING_DIR.mkdir(parents=True, exist_ok=True)
    TABLE_PROFILE_JSON.write_text(
        json.dumps(profile_tables(tables), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    FOREIGN_KEY_REPORT_JSON.write_text(
        json.dumps(check_foreign_keys(tables), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {TABLE_PROFILE_JSON}")
    print(f"Wrote {FOREIGN_KEY_REPORT_JSON}")


if __name__ == "__main__":
    main()
