from dataclasses import replace
from datetime import datetime

from src.forecast.canonical_queries import (
    CanonicalFactAtCutoff, derive_standalone_quarters,
)


def _ytd(month, end_day, value, version):
    return CanonicalFactAtCutoff(
        company_id=1, report_type_id="PERIODIC_FINANCIAL", metric_id=7,
        period_id=month, temporal_type="DURATION",
        start_jalali=(1404, 1, 1), end_jalali=(1404, month, end_day),
        duration_basis="YTD", value_integer=value, value_state="REPORTED_VALUE",
        scenario="ACTUAL", source_unit="unit-rial", source_currency="currency-irr",
        source_scale="scale-unit", report_version_id=version,
        publication_datetime=datetime(2025, 1, month), is_audited=True,
        is_restated=False, dimensions=(), source_identity="source", revision_identity=str(version),
        source_coordinate=f"B{month}",
    )


def test_standalone_quarters_are_exact_runtime_differences_with_both_provenances():
    quarters = derive_standalone_quarters([
        _ytd(3, 31, 100, 11), _ytd(6, 31, 250, 12), _ytd(9, 30, 410, 13),
    ])
    assert [(item.quarter_number, item.value_integer) for item in quarters] == [
        (1, 100), (2, 150), (3, 160),
    ]
    assert quarters[1].source_report_version_ids == (11, 12)
    assert quarters[2].period_start_jalali == (1404, 7, 1)


def test_standalone_derivation_requires_a_contiguous_cumulative_chain():
    quarters = derive_standalone_quarters([_ytd(3, 31, 100, 11), _ytd(9, 30, 410, 13)])
    assert [(item.quarter_number, item.value_integer) for item in quarters] == [(1, 100)]


def test_standalone_derivation_ignores_other_report_types_and_temporal_bases():
    monthly = _ytd(3, 31, 100, 11)
    standalone = replace(monthly, report_type_id="MONTHLY_ACTIVITY")
    assert derive_standalone_quarters([standalone]) == []
