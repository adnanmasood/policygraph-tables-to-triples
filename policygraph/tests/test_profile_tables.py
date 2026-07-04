from __future__ import annotations

import json

from policygraph.profile_tables import (
    FOREIGN_KEY_REPORT_JSON,
    PRIMARY_KEYS,
    check_foreign_keys,
    load_tables,
    main,
)


def test_all_tables_load() -> None:
    tables = load_tables()
    assert set(tables) == {"customers", "policies", "coverages", "claims"}


def test_expected_row_counts() -> None:
    tables = load_tables()
    assert len(tables["customers"]) == 3
    assert len(tables["policies"]) == 4


def test_primary_keys_are_unique() -> None:
    tables = load_tables()
    for table_name, primary_key in PRIMARY_KEYS.items():
        assert tables[table_name][primary_key].is_unique


def test_foreign_key_report_detects_missing_customer() -> None:
    report = check_foreign_keys(load_tables())
    customer_report = next(item for item in report if item["child_table"] == "policies")
    assert customer_report["missing_parent_values"] == ["C999"]


def test_main_writes_json_reports() -> None:
    main()
    report = json.loads(FOREIGN_KEY_REPORT_JSON.read_text(encoding="utf-8"))
    customer_report = next(item for item in report if item["child_table"] == "policies")
    assert customer_report["missing_parent_values"] == ["C999"]
