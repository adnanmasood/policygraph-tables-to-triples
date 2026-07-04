from __future__ import annotations

from policygraph.validate_graph import run_validation
from tests.conftest import ensure_materialized_graph


def test_validation_reports_expected_non_conformance() -> None:
    ensure_materialized_graph()
    conforms, report_text = run_validation()
    assert conforms is False
    assert "Policy must point to an existing Customer resource" in report_text
    assert "Claim loss date is outside the policy effective period" in report_text
    assert "Claim coverage type is not listed as a coverage type on the policy" in report_text
