"""Focused P18 tests: Stage 6 evaluation data foundation (no scores).

Covers the P18 TESTS contract using only P17 AUTHORITATIVE material:

* Forecast→Actual identity (Stage 6 spec §4 key)
* Later-published Actual is eligible (PIT CONTRACT)
* PIT leakage in *inputs* is rejected; the outcome Actual never counts
* Invalid ReportVersion/publication handling
* Horizon isolation, model-version isolation
* Duplicate flagging without silent resolution (blocker B9)
* NULL vs zero preservation
* §41 data-quality states carried verbatim (blocker B6: no participation rule)

Forbidden by P18 and absent here: MAPE, Bias, Reliability, Calibration,
Valuation, forecasting logic, Stage 5 logic.
"""

from datetime import datetime, timezone

import pytest

from src.evaluation.observation import (
    build_observation,
    detect_pit_leakage,
    evaluation_key_for,
    evaluation_metadata,
    flag_duplicates,
    missing_provenance,
)
from src.evaluation.schema import (
    ACTUAL_DATA_QUALITY_STATES,
    ActualObservation,
)
from src.forecast.schema import ForecastInputRef, ForecastRecord

CUTOFF = datetime(2024, 6, 30, tzinfo=timezone.utc)
BEFORE = datetime(2024, 3, 31, tzinfo=timezone.utc)
AFTER = datetime(2024, 9, 30, tzinfo=timezone.utc)
STAMP = datetime(2024, 7, 1, tzinfo=timezone.utc)


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
        publication_datetime=AFTER,
    )
    fields.update(overrides)
    return ActualObservation(**fields)


def _ref(key="REVENUE", at=BEFORE):
    return ForecastInputRef(
        fact_key=key, report_version_id=9, available_at=at, source="stage1"
    )


# --- Forecast→Actual identity (§4) -------------------------------------------


def test_identity_key_carries_full_mapping_key():
    key = evaluation_key_for(_record(), "REVENUE")
    assert key.as_tuple() == (
        7, "REVENUE", 101, "12M", "V1.0", CUTOFF, "BASE",
    )


def test_identity_scenario_isolates_observations():
    assert (
        evaluation_key_for(_record(scenario="BASE"), "REVENUE").as_tuple()
        != evaluation_key_for(_record(scenario="BULL"), "REVENUE").as_tuple()
    )
    assert evaluation_key_for(_record(scenario="BULL"), "REVENUE").as_tuple()[-1] == "BULL"


def test_identity_differs_by_metric():
    assert (
        evaluation_key_for(_record(), "REVENUE").as_tuple()
        != evaluation_key_for(_record(), "NET_PROFIT").as_tuple()
    )


def test_identity_stable_for_same_series():
    assert (
        evaluation_key_for(_record(), "REVENUE").as_tuple()
        == evaluation_key_for(_record(), "REVENUE").as_tuple()
    )


# --- Later-published Actual is eligible (PIT CONTRACT) -----------------------


def test_later_published_actual_binds_ready():
    observation = build_observation(_record(), "REVENUE", _actual())
    assert observation.evaluation_status == "READY"
    assert observation.actual_value == 1100.0
    assert observation.forecast_value == 1000.0


def test_historical_actual_also_binds():
    observation = build_observation(
        _record(), "REVENUE", _actual(publication_datetime=BEFORE)
    )
    assert observation.evaluation_status == "READY"


def test_unbound_observation_waits_for_actual():
    observation = build_observation(_record(), "REVENUE")
    assert observation.evaluation_status == "PENDING_ACTUAL"
    assert observation.actual_value is None


# --- PIT leakage: inputs only, never the outcome ------------------------------


def test_leaked_input_freezes_observation():
    record = _record(input_refs=(_ref(at=AFTER),))
    observation = build_observation(record, "REVENUE", _actual())
    assert observation.evaluation_status == "PIT_INVALID_INPUT"


def test_later_actual_is_not_leakage():
    refs = (_ref(at=BEFORE),)
    assert detect_pit_leakage(CUTOFF, refs) == []
    observation = build_observation(
        _record(input_refs=refs), "REVENUE", _actual(publication_datetime=AFTER)
    )
    assert observation.evaluation_status == "READY"


def test_leak_detector_flags_only_post_cutoff_inputs():
    late = _ref("A", AFTER)
    early = _ref("B", BEFORE)
    assert detect_pit_leakage(CUTOFF, (early, late)) == [late]


def test_unknown_provenance_is_gap_not_leakage():
    unknown = ForecastInputRef(fact_key="X", available_at=None)
    assert detect_pit_leakage(CUTOFF, (unknown,)) == []
    assert missing_provenance((unknown, _ref())) == [unknown]


# --- Invalid ReportVersion / publication handling ------------------------------


def test_unknown_quality_state_rejected():
    with pytest.raises(ValueError):
        _actual(data_quality_state="BOGUS")


def test_restated_actual_carried_not_decided():
    actual = _actual(data_quality_state="RESTATED", restated=True)
    assert actual.data_quality_state == "RESTATED"
    assert actual.restated is True
    observation = build_observation(_record(), "REVENUE", actual)
    assert observation.evaluation_status == "READY"


def test_missing_report_version_carried():
    # Stage 6 Prompt 25 (Part A): an Actual without a ReportVersion id is
    # INVALID_REPORT_VERSION — carried (actual attached for audit) but
    # quarantined downstream, never scored.
    actual = _actual(report_version_id=None)
    assert actual.report_version_id is None
    observation = build_observation(_record(), "REVENUE", actual)
    assert observation.evaluation_status == "INVALID_REPORT_VERSION"
    assert observation.actual is actual


# --- Horizon / model-version isolation ------------------------------------------


def test_horizon_isolates_series():
    assert (
        evaluation_key_for(_record(forecast_horizon="12M"), "REVENUE").as_tuple()
        != evaluation_key_for(_record(forecast_horizon="3M"), "REVENUE").as_tuple()
    )


def test_model_version_isolates_series():
    assert (
        evaluation_key_for(_record(model_version="V1.0"), "REVENUE").as_tuple()
        != evaluation_key_for(_record(model_version="V2.0"), "REVENUE").as_tuple()
    )


# --- Duplicates: flagged, never silently resolved (B9) ---------------------------


def test_duplicate_keys_share_flag_and_survive():
    first = build_observation(_record(), "REVENUE", _actual())
    second = build_observation(_record(), "REVENUE", _actual(value=1200.0))
    flagged = flag_duplicates([first, second])
    assert len(flagged) == 2
    assert flagged[0].duplicate_key is not None
    assert flagged[0].duplicate_key == flagged[1].duplicate_key
    assert flagged[0].actual_value == 1100.0
    assert flagged[1].actual_value == 1200.0


def test_unique_observations_unflagged():
    observations = [
        build_observation(_record(forecast_horizon="3M"), "REVENUE"),
        build_observation(_record(forecast_horizon="6M"), "REVENUE"),
    ]
    flagged = flag_duplicates(observations)
    assert all(observation.duplicate_key is None for observation in flagged)


# --- NULL vs zero -----------------------------------------------------------------


def test_missing_actual_value_is_none_not_zero():
    observation = build_observation(
        _record(), "REVENUE", _actual(value=None, data_quality_state="MISSING")
    )
    assert observation.actual_value is None
    assert observation.actual_value != 0.0


def test_zero_actual_preserved_as_zero():
    observation = build_observation(_record(), "REVENUE", _actual(value=0.0))
    assert observation.actual_value == 0.0
    assert observation.actual_value is not None


def test_missing_forecast_metric_is_none():
    record = _record(revenue=None)
    assert record.is_missing("revenue")
    observation = build_observation(record, "REVENUE")
    assert observation.forecast_value is None


def test_unknown_metric_code_is_missing_not_zero():
    observation = build_observation(_record(), "NO_SUCH_METRIC")
    assert observation.forecast_value is None


# --- §41 states carried verbatim (B6 unresolved) ------------------------------------


@pytest.mark.parametrize("state", ACTUAL_DATA_QUALITY_STATES)
def test_quality_states_recorded_verbatim(state):
    actual = _actual(data_quality_state=state, value=None if state == "MISSING" else 5.0)
    assert actual.data_quality_state == state


# --- Metadata aggregates without scores ----------------------------------------------


def test_metadata_counts_without_scoring():
    observations = flag_duplicates([
        build_observation(_record(), "REVENUE", _actual()),
        build_observation(_record(forecast_horizon="3M"), "REVENUE"),
        build_observation(_record(input_refs=(_ref(at=AFTER),)), "REVENUE"),
    ])
    metadata = evaluation_metadata(observations)
    assert metadata["observation_count"] == 3
    assert metadata["by_status"]["READY"] == 1
    assert metadata["by_status"]["PENDING_ACTUAL"] == 1
    assert metadata["by_status"]["PIT_INVALID_INPUT"] == 1
    assert sorted(metadata["horizons"]) == ["12M", "3M"]
    assert "mape" not in metadata and "bias" not in metadata
