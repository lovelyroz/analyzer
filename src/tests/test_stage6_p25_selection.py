"""Stage 6 Prompt 25 (Part A): first-known-outcome selection + scenario key.

L1/L2 tests with exact values:

* ``select_actual``: earliest publication wins; publication ties break by
  version number then version id; invalid candidates (None id / None
  publication) are filtered and all-invalid yields None; single candidate
  passes through; result is independent of input order.
* B6 predicate ``is_scoring_eligible``: exact verdict per quality state.
* ``EvaluationKey``: 7-tuple exact equality with scenario appended last;
  scenario-distinct keys differ; ``forecast_id`` never affects the key.
"""

from datetime import datetime, timezone
from itertools import permutations

import pytest

from src.evaluation.observation import (
    build_observation,
    evaluation_key_for,
    select_actual,
)
from src.evaluation.schema import (
    ACTUAL_DATA_QUALITY_STATES,
    ActualObservation,
    is_scoring_eligible,
    is_valid_report_version,
)
from src.forecast.schema import ForecastRecord

CUTOFF = datetime(2024, 6, 30, tzinfo=timezone.utc)
STAMP = datetime(2024, 7, 1, tzinfo=timezone.utc)
EARLY = datetime(2024, 9, 30, tzinfo=timezone.utc)
MID = datetime(2024, 10, 31, tzinfo=timezone.utc)
LATE = datetime(2024, 12, 31, tzinfo=timezone.utc)


def _record(**overrides):
    fields = dict(
        forecast_id=1,
        forecast_version=1,
        company_id=7,
        forecast_period_id=101,
        industry_code="PETROCHEMICAL",
        forecast_horizon="12M",
        scenario="BASE",
        forecast_timestamp=STAMP,
        data_cutoff_datetime=CUTOFF,
        model_version="V1.0",
        forecast_method="M1",
        data_quality="VALID",
        baseline_method="SEASONAL_NAIVE",
        revenue=1000.0,
        operating_profit=200.0,
        operating_margin=0.2,
        net_profit=150.0,
        eps=15.0,
        roe=0.1,
        input_refs=(),
    )
    fields.update(overrides)
    return ForecastRecord(**fields)


def _actual(**overrides):
    fields = dict(
        company_id=7,
        financial_period_id=101,
        metric_code="REVENUE",
        value=1100.0,
        report_version_id=55,
        publication_datetime=MID,
    )
    fields.update(overrides)
    return ActualObservation(**fields)


# --- select_actual: earliest publication wins ---------------------------------


def test_selection_earliest_publication_wins():
    first = _actual(report_version_id=3, publication_datetime=EARLY)
    second = _actual(report_version_id=1, publication_datetime=MID)
    third = _actual(report_version_id=2, publication_datetime=LATE)
    assert select_actual([third, second, first]) is first


def test_selection_single_candidate_passthrough():
    only = _actual()
    assert select_actual([only]) is only


# --- select_actual: publication tie-breaks ------------------------------------


def test_selection_tie_break_by_version_number_then_id():
    low_version = _actual(
        report_version_id=99, report_version_number=1,
        publication_datetime=MID,
    )
    high_version = _actual(
        report_version_id=7, report_version_number=2,
        publication_datetime=MID,
    )
    assert select_actual([high_version, low_version]) is low_version


def test_selection_tie_break_by_id_when_version_number_equal():
    high_id = _actual(
        report_version_id=80, report_version_number=4,
        publication_datetime=MID,
    )
    low_id = _actual(
        report_version_id=12, report_version_number=4,
        publication_datetime=MID,
    )
    assert select_actual([high_id, low_id]) is low_id


def test_selection_none_version_number_sorts_as_zero():
    unnumbered = _actual(
        report_version_id=5, report_version_number=None,
        publication_datetime=MID,
    )
    numbered = _actual(
        report_version_id=6, report_version_number=1,
        publication_datetime=MID,
    )
    assert select_actual([numbered, unnumbered]) is unnumbered


# --- select_actual: invalid candidates ----------------------------------------


def test_selection_filters_none_id_and_none_publication():
    no_id = _actual(report_version_id=None, publication_datetime=EARLY)
    no_pub = _actual(report_version_id=1, publication_datetime=None)
    assert is_valid_report_version(no_id) is False
    assert is_valid_report_version(no_pub) is False
    good = _actual(report_version_id=2, publication_datetime=LATE)
    assert select_actual([no_id, no_pub, good]) is good


def test_selection_all_invalid_returns_none():
    assert select_actual([
        _actual(report_version_id=None, publication_datetime=EARLY),
        _actual(report_version_id=1, publication_datetime=None),
    ]) is None
    assert select_actual([]) is None


# --- select_actual: input-order independence -----------------------------------


def test_selection_is_input_order_independent():
    candidates = [
        _actual(report_version_id=3, publication_datetime=LATE, value=1.0),
        _actual(report_version_id=1, publication_datetime=EARLY, value=2.0),
        _actual(report_version_id=2, publication_datetime=MID, value=3.0),
    ]
    winners = [select_actual(order) for order in permutations(candidates)]
    assert winners
    assert all(winner is candidates[1] for winner in winners)


# --- B6 eligibility predicate ---------------------------------------------------


@pytest.mark.parametrize(
    ("state", "eligible"),
    [
        ("VALID", True),
        ("ESTIMATED", True),
        ("RESTATED", True),
        ("MISSING", False),
        ("SUSPICIOUS", False),
        ("UNMAPPED", False),
    ],
)
def test_scoring_eligibility_per_state(state, eligible):
    assert state in ACTUAL_DATA_QUALITY_STATES
    actual = _actual(data_quality_state=state)
    assert is_scoring_eligible(actual) is eligible


# --- EvaluationKey: scenario in identity ---------------------------------------


def test_key_is_7_tuple_with_scenario_last():
    key = evaluation_key_for(_record(), "REVENUE")
    assert key.as_tuple() == (
        7, "REVENUE", 101, "12M", "V1.0", CUTOFF, "BASE",
    )


def test_key_scenario_distinct_keys_differ():
    assert (
        evaluation_key_for(_record(scenario="BASE"), "REVENUE").as_tuple()
        != evaluation_key_for(_record(scenario="BULL"), "REVENUE").as_tuple()
    )


def test_key_forecast_id_does_not_affect_key():
    assert (
        evaluation_key_for(_record(forecast_id=1), "REVENUE").as_tuple()
        == evaluation_key_for(_record(forecast_id=999), "REVENUE").as_tuple()
    )


# --- build_observation: invalid ReportVersion -----------------------------------


def test_build_observation_invalid_report_version_status():
    observation = build_observation(
        _record(), "REVENUE", _actual(report_version_id=None)
    )
    assert observation.evaluation_status == "INVALID_REPORT_VERSION"
    assert observation.actual is not None
