"""Stage 6 Prompt 21 behavioral tests: production integration + matrix.

Proves the complete production path on-path (never helpers alone):

Forecast Version -> PIT-safe Actual -> Error -> Accuracy/Bias
-> Baseline comparison -> Sufficiency -> Performance (withheld without
components) -> Reliability (withheld, B2/B7) -> Calibration
(NO_CALIBRATION, B3/B4) -> OOS boundary.

Contracts (spec, P17 AUTHORITATIVE material only; unresolved items are
fail-closed boundaries, never numeric defaults):

* Normal/under/over forecasts score with sign preserved.
* Zero-forecast and sign-change regimes quarantine (absolute error kept
  for audit, percentage metrics None, never zero).
* Actual=0 / Forecast!=0 is UNRESOLVED — quarantined, not scored.
* Horizons and model versions never mix, even over overlapping periods.
* Sufficiency bands apply to the scored count only.
* Baseline comparison from caller-supplied values; Seasonal Naive
  construction has no authority (B1) and is absent.
* Reliability withheld with reasons (B2/B7); calibration stays
  NO_CALIBRATION however suggestive the evidence (B3/B4).
* PIT leakage quarantines inputs; later-published Actuals score.
* Duplicates quarantine wholesale (B9); TTM observations are conserved
  exactly once, never double counted (spec Sections 16, 42).
* Records are never mutated; no Stage 5 writes; no Stage 7 logic;
  Forward P/E passes through untouched.

Layers (P20 MANDATORY MULTI-LAYER TESTING DOCTRINE):

* L1 unit: bands, identity guard, OOS projection arithmetic.
* L2 contract/boundary: PIT, isolation, NULL != 0, duplicates, quality.
* L3 production-path: every matrix row runs through
  run_evaluation_pipeline (or its OOS / P-E wrappers).
* L4 adversarial: forced defaults refused, overlap rejected, collisions
  quarantined, invented-methodology tokens absent from pipeline source.
* L5 regression: focused Stage 6 suite, then the full src/tests suite.
"""

from datetime import datetime, timezone
from pathlib import Path

import pytest

from src.evaluation.metrics import INVALID_REGIMES  # noqa: F401  (spec name pin)
from src.evaluation.observation import build_observation
from src.evaluation.pipeline import (
    evaluate_holdout_oos,
    prove_forward_pe_untouched,
    run_evaluation_pipeline,
)
from src.evaluation.reliability import (
    MISSING_CALIBRATION_TRANSITION,
    MISSING_PERSISTENCE_DEFINITION,
    MISSING_UNAVAILABLE_COMPONENT_RULE,
)
from src.evaluation.schema import ActualObservation
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


def _actual(period=101, value=1100.0, publication=AFTER, state="VALID"):
    return ActualObservation(
        company_id=7,
        financial_period_id=period,
        metric_code="REVENUE",
        value=value,
        report_version_id=55,
        publication_datetime=publication,
        data_quality_state=state,
    )


def _actual_map(periods, value=1100.0, **overrides):
    return {
        (7, period, "REVENUE"): _actual(period=period, value=value, **overrides)
        for period in periods
    }


def _run(records, actuals, baselines=None, ttm=None):
    return run_evaluation_pipeline(
        records=records,
        metric_codes=["REVENUE"],
        actuals=actuals,
        baselines=baselines,
        ttm_observations=ttm,
    )


def _baseline_map(periods, value, horizon="12M", version="V1.0"):
    # Stage 6 Prompt 25 (Part A): EvaluationKey is a 7-tuple with scenario
    # ("BASE") appended last.
    return {
        (7, "REVENUE", period, horizon, version, CUTOFF, "BASE"): value
        for period in periods
    }


def _verdict(result, horizon="12M", version="V1.0"):
    return result.verdicts[(7, "REVENUE", horizon, version)]


# --- L3: normal / under / over forecast --------------------------------------


def test_normal_path_scores_end_to_end():
    periods = list(range(101, 109))
    records = [_record(forecast_period_id=p) for p in periods]
    verdict = _verdict(_run(records, _actual_map(periods)))
    assert verdict.series.observation_count == 8
    assert verdict.series.confidence_level == "MODERATE_CONFIDENCE"
    assert verdict.series.mape == pytest.approx(10.0)
    assert verdict.series.bias == pytest.approx(10.0)
    assert verdict.governance.reliability.reliability is None
    assert verdict.governance.performance is None
    assert verdict.governance.calibration.state == "NO_CALIBRATION"


def test_under_forecast_positive_bias():
    periods = list(range(101, 109))
    records = [_record(forecast_period_id=p, revenue=1000.0) for p in periods]
    verdict = _verdict(_run(records, _actual_map(periods, value=1300.0)))
    assert verdict.series.bias == pytest.approx(30.0)
    assert verdict.series.observations[0].error == pytest.approx(300.0)


def test_over_forecast_negative_bias():
    periods = list(range(101, 109))
    records = [_record(forecast_period_id=p, revenue=1100.0) for p in periods]
    verdict = _verdict(_run(records, _actual_map(periods, value=1000.0)))
    assert verdict.series.bias == pytest.approx(-100.0 / 11.0)
    assert verdict.series.observations[0].error == pytest.approx(-100.0)


# --- L3: zero / regime quarantine --------------------------------------------


def test_zero_forecast_quarantined_never_zeroed():
    verdict = _verdict(_run([_record(revenue=0.0)], _actual_map([101])))
    assert verdict.series.observation_count == 0
    assert verdict.series.quarantined == {"ZERO_BASE": 1}
    assert verdict.series.mape is None
    assert verdict.series.bias is None


def test_zero_actual_unresolved_quarantined():
    # Stage 6 Prompt 25 (Part B): A=0/F=1000 scores normally end to end —
    # Error = -1000, APE = 100, all 8 scored.
    records = [_record(forecast_period_id=p) for p in range(101, 109)]
    actuals = _actual_map(list(range(101, 109)), value=0.0)
    verdict = _verdict(_run(records, actuals))
    assert verdict.series.observation_count == 8
    assert verdict.series.quarantined == {}
    assert verdict.series.observations[0].error == -1000.0
    assert verdict.series.mape == 100.0


def test_loss_profit_regimes_quarantined():
    loss_to_profit = _record(forecast_period_id=101, revenue=-50.0)
    profit_to_loss = _record(forecast_period_id=102, revenue=50.0)
    actuals = {
        (7, 101, "REVENUE"): _actual(period=101, value=100.0),
        (7, 102, "REVENUE"): _actual(period=102, value=-100.0),
    }
    verdict = _verdict(_run([loss_to_profit, profit_to_loss], actuals))
    assert verdict.series.observation_count == 0
    assert verdict.series.quarantined == {
        "LOSS_TO_PROFIT": 1,
        "PROFIT_TO_LOSS": 1,
    }


def test_sign_change_name_pinned_no_percentage_metrics():
    assert "SIGN_CHANGE" in INVALID_REGIMES


# --- L3: horizon and version isolation ---------------------------------------


def test_each_horizon_independent_over_overlapping_periods():
    records = [
        _record(forecast_period_id=p, forecast_horizon=h)
        for h in ("1M", "3M", "6M", "12M")
        for p in (101, 102)
    ]
    result = _run(records, _actual_map([101, 102]))
    assert result.series_count == 4
    seen: set = set()
    for horizon in ("1M", "3M", "6M", "12M"):
        verdict = _verdict(result, horizon=horizon)
        assert verdict.series.observation_count == 2
        assert verdict.series.horizon == horizon
        ids = {id(item) for item in verdict.series.observations}
        assert not ids & seen
        seen |= ids


def test_model_versions_never_mix():
    records = [_record(forecast_period_id=p, model_version="V1.0") for p in (101, 102)]
    records += [_record(forecast_period_id=p, model_version="V2.0") for p in (101, 102)]
    result = _run(records, _actual_map([101, 102]))
    assert result.series_count == 2
    assert _verdict(result, version="V1.0").series.observation_count == 2
    assert _verdict(result, version="V2.0").series.observation_count == 2


# --- L1/L3: sufficiency bands on the scored count -----------------------------


@pytest.mark.parametrize(
    "count,band",
    [
        (4, "INSUFFICIENT_DATA"),
        (6, "LOW_CONFIDENCE"),
        (9, "MODERATE_CONFIDENCE"),
        (12, "ADEQUATE"),
    ],
)
def test_sufficiency_bands_on_path(count, band):
    periods = list(range(101, 101 + count))
    records = [_record(forecast_period_id=p) for p in periods]
    verdict = _verdict(_run(records, _actual_map(periods)))
    assert verdict.series.observation_count == count
    assert verdict.series.confidence_level == band
    assert verdict.governance.confidence_level == band


# --- L3: baseline comparison (caller-supplied values only) --------------------


def test_model_better_than_baseline_positive_improvement():
    periods = list(range(101, 109))
    records = [_record(forecast_period_id=p) for p in periods]
    verdict = _verdict(
        _run(records, _actual_map(periods), baselines=_baseline_map(periods, 900.0))
    )
    assert verdict.series.baseline_mape == pytest.approx(200.0 / 9.0)
    assert verdict.series.relative_improvement is not None
    assert verdict.series.relative_improvement > 0


def test_baseline_better_than_model_negative_improvement():
    periods = list(range(101, 109))
    records = [_record(forecast_period_id=p) for p in periods]
    verdict = _verdict(
        _run(records, _actual_map(periods), baselines=_baseline_map(periods, 1080.0))
    )
    assert verdict.series.relative_improvement is not None
    assert verdict.series.relative_improvement < 0


def test_zero_baseline_error_yields_missing_improvement_not_zero():
    periods = list(range(101, 109))
    records = [_record(forecast_period_id=p) for p in periods]
    verdict = _verdict(
        _run(records, _actual_map(periods), baselines=_baseline_map(periods, 1100.0))
    )
    assert verdict.series.baseline_mape == pytest.approx(0.0)
    assert verdict.series.relative_improvement is None


def test_missing_baseline_yields_missing_comparison():
    periods = list(range(101, 109))
    records = [_record(forecast_period_id=p) for p in periods]
    verdict = _verdict(_run(records, _actual_map(periods)))
    assert verdict.series.baseline_mape is None
    assert verdict.series.relative_improvement is None


# --- L3/L4: calibration stays NO_CALIBRATION (B3/B4 fail-closed) --------------


def test_isolated_bias_stays_no_calibration():
    records = [_record(forecast_period_id=p) for p in range(101, 108)]
    records.append(_record(forecast_period_id=108))
    actuals = _actual_map(list(range(101, 108)), value=1000.0)
    actuals[(7, 108, "REVENUE")] = _actual(period=108, value=1300.0)
    verdict = _verdict(_run(records, actuals))
    assert verdict.series.observation_count == 8
    assert verdict.governance.calibration.state == "NO_CALIBRATION"


def test_unanimous_bias_still_no_calibration_names_missing_authority():
    periods = list(range(101, 111))
    records = [_record(forecast_period_id=p) for p in periods]
    verdict = _verdict(_run(records, _actual_map(periods, value=1300.0)))
    assert verdict.series.bias == pytest.approx(30.0)
    calibration = verdict.governance.calibration
    assert calibration.state == "NO_CALIBRATION"
    assert MISSING_PERSISTENCE_DEFINITION in calibration.missing_authority
    assert MISSING_CALIBRATION_TRANSITION in calibration.missing_authority


# --- L2/L3: PIT, later Actual, invalid Actuals, duplicates, NULL --------------


def test_pit_leaking_input_quarantined_on_path():
    leaked = ForecastInputRef(
        fact_key="Q2_REVENUE", report_version_id=9, available_at=AFTER
    )
    record = _record(input_refs=(leaked,))
    verdict = _verdict(_run([record], _actual_map([101])))
    assert verdict.series.observation_count == 0
    assert verdict.series.quarantined == {"PIT_INVALID_INPUT": 1}


def test_later_published_actual_scores_as_outcome():
    verdict = _verdict(_run([_record()], _actual_map([101])))
    assert verdict.series.observation_count == 1
    assert verdict.series.mape == pytest.approx(10.0)


def test_unbound_forecast_never_scores():
    verdict = _verdict(_run([_record()], {}))
    assert verdict.series.observation_count == 0
    assert verdict.series.quarantined == {"PENDING_ACTUAL": 1}


@pytest.mark.parametrize(
    "state",
    ["SUSPICIOUS", "UNMAPPED"],
)
def test_nonvalid_actual_states_quarantined_verbatim(state):
    verdict = _verdict(_run([_record()], _actual_map([101], state=state)))
    assert verdict.series.observation_count == 0
    assert verdict.series.quarantined == {f"DATA_QUALITY_QUARANTINED:{state}": 1}


@pytest.mark.parametrize("state", ["ESTIMATED", "RESTATED"])
def test_limited_quality_states_score_with_flag(state):
    # Stage 6 Prompt 25 (Part B): ESTIMATED / RESTATED score and flag
    # limited_quality on the series.
    verdict = _verdict(_run([_record()], _actual_map([101], state=state)))
    assert verdict.series.observation_count == 1
    assert verdict.series.limited_quality is True
    assert verdict.series.mape == 10.0


def test_duplicate_observations_quarantined_wholesale():
    first = _record(forecast_id=1, forecast_period_id=101)
    second = _record(forecast_id=2, forecast_period_id=101)
    verdict = _verdict(_run([first, second], _actual_map([101])))
    assert verdict.series.observation_count == 0
    assert verdict.series.quarantined == {"DUPLICATE_QUARANTINED": 2}


def test_duplicate_forecast_id_only_still_collides():
    # forecast_id is a surrogate, not identity: same key, different id
    # still collides wholesale.
    first = _record(forecast_id=1, forecast_version=1, forecast_period_id=101)
    second = _record(forecast_id=999, forecast_version=9, forecast_period_id=101)
    verdict = _verdict(_run([first, second], _actual_map([101])))
    assert verdict.series.observation_count == 0
    assert verdict.series.quarantined == {"DUPLICATE_QUARANTINED": 2}


def test_duplicate_scenario_differs_does_not_collide():
    # Scenario is identity: BASE vs BULL is two distinct observations,
    # each scoring once (SeriesKey stays scenario-free per spec §14).
    base = _record(forecast_period_id=101, scenario="BASE")
    bull = _record(forecast_period_id=101, scenario="BULL")
    verdict = _verdict(_run([base, bull], _actual_map([101])))
    assert verdict.series.observation_count == 2
    assert verdict.series.quarantined == {}


def test_null_is_never_zero_on_path():
    missing_actual = _record(forecast_period_id=101)
    missing_forecast = _record(forecast_period_id=102, revenue=None)
    actuals = {(7, 101, "REVENUE"): _actual(period=101, value=None)}
    result = run_evaluation_pipeline(
        records=[missing_actual, missing_forecast],
        metric_codes=["REVENUE"],
        actuals=actuals,
    )
    verdict = _verdict(result)
    assert verdict.series.observation_count == 0
    assert verdict.series.quarantined == {"MISSING_VALUE": 1, "PENDING_ACTUAL": 1}
    assert verdict.series.mape is None


# --- L3/L4: TTM conservation — never double counted ----------------------------


def test_ttm_observations_conserved_exactly_once():
    periods = [101, 102, 103]
    records = [_record(forecast_period_id=p) for p in periods]
    ttm = [
        build_observation(
            _record(forecast_id=100 + i, forecast_period_id=201 + i),
            "REVENUE",
            _actual(period=201 + i),
        )
        for i in range(2)
    ]
    result = _run(records, _actual_map(periods), ttm=ttm)
    verdict = _verdict(result)
    assert verdict.series.total_observations == 5
    assert verdict.series.observation_count == 5
    assert verdict.ttm_accounted == 2
    keys = [
        item.key.as_tuple()
        for series in result.verdicts.values()
        for item in series.series.observations
    ]
    assert len(keys) == 5
    assert len(set(keys)) == 5


def test_ttm_same_period_collision_quarantines_both():
    regular = _record(forecast_id=1, forecast_period_id=101)
    ttm = [
        build_observation(
            _record(forecast_id=2, forecast_period_id=101),
            "REVENUE",
            _actual(period=101),
        )
    ]
    verdict = _verdict(_run([regular], _actual_map([101]), ttm=ttm))
    assert verdict.series.total_observations == 2
    assert verdict.series.observation_count == 0
    assert verdict.series.quarantined == {"DUPLICATE_QUARANTINED": 2}


# --- L1/L3: OOS boundary -------------------------------------------------------


def test_holdout_projection_passes_only_holdout():
    projected = evaluate_holdout_oos(
        {1: 5.0, 2: 6.0, 3: 7.0}, evidence_periods=(1, 2), holdout_periods=(3,)
    )
    assert projected == {3: 7.0}


def test_overlapping_holdout_rejected_as_contamination():
    with pytest.raises(ValueError):
        evaluate_holdout_oos(
            {1: 5.0, 2: 6.0}, evidence_periods=(1, 2), holdout_periods=(2,)
        )


def test_inverted_holdout_rejected():
    with pytest.raises(ValueError):
        evaluate_holdout_oos(
            {1: 5.0, 3: 7.0}, evidence_periods=(3,), holdout_periods=(1,)
        )


# --- L2/L4: reliability unavailability, P/E, Stage 5/7 boundaries -------------


def test_regime_only_series_withholds_with_unavailable_named():
    records = [_record(forecast_period_id=p, revenue=0.0) for p in (101, 102)]
    verdict = _verdict(_run(records, _actual_map([101, 102])))
    reliability = verdict.governance.reliability
    assert reliability.reliability is None
    assert "UNAVAILABLE:MAPE" in reliability.withheld_because
    assert "UNAVAILABLE:BIAS" in reliability.withheld_because
    assert MISSING_UNAVAILABLE_COMPONENT_RULE in reliability.withheld_because


def test_forward_pe_passes_through_untouched():
    assert prove_forward_pe_untouched(18.5) == 18.5


def test_pipeline_never_mutates_stage5_records():
    periods = list(range(101, 109))
    records = [_record(forecast_period_id=p) for p in periods]
    snapshot = list(records)
    result = _run(
        records, _actual_map(periods), baselines=_baseline_map(periods, 900.0)
    )
    assert records == snapshot
    assert all(
        verdict.governance.calibration.state == "NO_CALIBRATION"
        for verdict in result.verdicts.values()
    )


def _pipeline_source() -> str:
    return (
        Path(__file__).parent.parent / "evaluation" / "pipeline.py"
    ).read_text(encoding="utf-8")


def test_pipeline_invents_no_methodology():
    source = _pipeline_source()
    for token in (
        "poor_mape",
        "unacceptable_bias",
        "full_advantage",
        "minimum_observations",
        "bias_threshold",
        "holdout_passed",
        "seasonal_naive_forecast",
        "history[-",
        "Forecast × (1",
    ):
        assert token not in source


def test_pipeline_has_no_stage5_writes_or_stage7_logic():
    source = _pipeline_source()
    for token in (
        "ForecastRecordRepository",
        "forecast_versions",
        ".to_record(",
        "db_session",
        ".commit(",
        "target_pe",
        "market_signal",
    ):
        assert token not in source
