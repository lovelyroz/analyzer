"""Stage 6 Prompt 38 closure regressions: fail-closed cutoff, Actual-zero
MAPE exclusion, independent Bias/MAPE counts, and adversarial combos.

Contracts (locked spec + Prompt 38 §4 conservative rule):

* D-c: one artifact = one unambiguous cutoff. A non-empty invocation
  mixing distinct non-null cutoffs raises ValueError BEFORE any scoring
  or artifact; empty input keeps evaluation_cutoff=None as explicitly
  empty only. No partial successful result on rejection.
* D-a: Actual-zero (A=0, F!=0) is excluded from ordinary MAPE with the
  dedicated ACTUAL_ZERO reason code; absolute error retained; Bias term
  stays eligible per §10 RB-2 (exactly -100% for F>0, +100% for F<0).
* D-b: independent Bias-eligible vs MAPE-effective counts;
  F=0/A=0 gets the BIAS_UNDEFINED_ZERO_ZERO status; paired same-event
  model/baseline Bias sets.
* Constraints preserved: Error=Actual-Forecast; PE/APE over |Forecast|;
  MAPE/Bias means over scored-only sets; sufficiency bands <5/5-7/8-11/
  >=12 on the scored-eligible count; improvement=(base-model)/base;
  scenario stays in keys; TTM counted once; Reliability stays None;
  no invented epsilons/weights; no DB/persistence; no valuation changes.
"""

from datetime import datetime, timezone

import pytest

from src.evaluation.aggregate import (
    aggregate_observations,
    score_observation,
)
from src.evaluation.observation import build_observation
from src.evaluation.pipeline import run_evaluation_pipeline
from src.evaluation.schema import ActualObservation
from src.forecast.schema import ForecastRecord

CUTOFF = datetime(2024, 6, 30, tzinfo=timezone.utc)
CUTOFF_OTHER = datetime(2024, 3, 31, tzinfo=timezone.utc)
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


def _actual(period=101, value=1100.0, **overrides):
    fields = dict(
        company_id=7,
        financial_period_id=period,
        metric_code="REVENUE",
        value=value,
        report_version_id=55,
        publication_datetime=AFTER,
    )
    fields.update(overrides)
    return ActualObservation(**fields)


def _series_key(scenario="BASE", horizon="12M", version="V1.0"):
    return (7, "REVENUE", horizon, version, scenario)


# --- D-c: mixed-cutoff rejection --------------------------------------------


def test_p38_mixed_cutoff_raises_before_scoring_no_partial_result():
    records = [
        _record(forecast_id=1, data_cutoff_datetime=CUTOFF),
        _record(forecast_id=2, data_cutoff_datetime=CUTOFF_OTHER),
    ]
    with pytest.raises(ValueError, match="mixed evaluation cutoffs"):
        run_evaluation_pipeline(
            records, ["REVENUE"], {(7, 101, "REVENUE"): _actual()}
        )


def test_p38_empty_input_keeps_explicit_empty_none_cutoff():
    result = run_evaluation_pipeline([], ["REVENUE"], {})
    assert result.artifact is not None
    assert result.artifact.evaluation_cutoff is None
    assert result.artifact.series_provenance == ()
    assert result.series_count == 0


def test_p38_single_cutoff_still_evaluates():
    result = run_evaluation_pipeline(
        [_record()], ["REVENUE"], {(7, 101, "REVENUE"): _actual()}
    )
    assert result.artifact is not None
    assert result.artifact.evaluation_cutoff == CUTOFF


def test_p38_mixed_cutoff_multi_scenario_raises():
    records = [
        _record(forecast_id=1, scenario="BASE", data_cutoff_datetime=CUTOFF),
        _record(forecast_id=2, scenario="BULL", data_cutoff_datetime=CUTOFF_OTHER),
    ]
    with pytest.raises(ValueError, match="mixed evaluation cutoffs"):
        run_evaluation_pipeline(
            records, ["REVENUE"], {(7, 101, "REVENUE"): _actual()}
        )


# --- D-a: Actual-zero MAPE exclusion + absolute-error retention --------------


def test_p38_actual_zero_mape_excluded_error_retained():
    scored = score_observation(
        build_observation(_record(revenue=1000.0), "REVENUE", _actual(value=0.0))
    )
    assert scored.scored is True
    assert scored.error == -1000.0
    assert scored.ape is None
    assert scored.mape_exclusion_reason == "ACTUAL_ZERO"
    # RB-2 (1): positive forecast + zero Actual → Bias term exactly -100%.
    assert scored.percentage_error == -100.0


def test_p38_actual_zero_negative_forecast_bias_plus_one():
    scored = score_observation(
        build_observation(_record(revenue=-500.0), "REVENUE", _actual(value=0.0))
    )
    assert scored.scored is True
    assert scored.error == 500.0
    assert scored.ape is None
    assert scored.mape_exclusion_reason == "ACTUAL_ZERO"
    assert scored.percentage_error == 100.0


def test_p38_actual_zero_series_mape_null_bias_kept():
    observations = [
        build_observation(
            _record(forecast_id=i + 1, forecast_period_id=101 + i),
            "REVENUE",
            _actual(period=101 + i, value=0.0),
        )
        for i in range(4)
    ]
    series = aggregate_observations(observations)[_series_key()]
    assert series.observation_count == 4
    assert series.mape_effective_count == 0
    assert series.bias_eligible_count == 4
    assert series.quarantined == {"ACTUAL_ZERO": 4}
    assert series.mape is None
    assert series.bias == pytest.approx(-100.0)


# --- D-b: independent counts + F=0/A=0 status --------------------------------


def test_p38_zero_zero_is_bias_undefined_with_status():
    observations = [
        build_observation(
            _record(forecast_id=1, revenue=0.0),
            "REVENUE",
            _actual(value=0.0),
        ),
        build_observation(
            _record(forecast_id=2, forecast_period_id=102),
            "REVENUE",
            _actual(period=102),
        ),
    ]
    series = aggregate_observations(observations)[_series_key()]
    # F=0/A=0 quarantines as ZERO_BASE (unscored); the valid observation
    # scores. The Bias-undefined status path is pinned at unit level below.
    assert series.quarantined == {"ZERO_BASE": 1}
    assert series.observation_count == 1
    assert series.mape_effective_count == 1
    assert series.bias_eligible_count == 1


def test_p38_bias_undefined_zero_zero_excluded_from_bias_mean():
    # F=0/A=0 passes quarantine only via direct aggregate_series input;
    # prove the Bias-undefined branch excludes it from the Bias mean while
    # keeping MAPE-effective counting honest (ape None → not in mean).
    from src.evaluation.aggregate import ScoredObservation, aggregate_series
    from src.evaluation.observation import evaluation_key_for

    record = _record(revenue=0.0)
    key = evaluation_key_for(record, "REVENUE")
    zero_zero = ScoredObservation(
        key=key,
        forecast_value=0.0,
        actual_value=0.0,
        error=0.0,
        percentage_error=0.0,  # degenerate term a naive mean would absorb
        ape=None,
        regime=None,
        baseline_value=None,
        baseline_error=None,
        baseline_ape=None,
        scored=True,
    )
    valid = ScoredObservation(
        key=key,
        forecast_value=1000.0,
        actual_value=1100.0,
        error=100.0,
        percentage_error=10.0,
        ape=10.0,
        regime=None,
        baseline_value=None,
        baseline_error=None,
        baseline_ape=None,
        scored=True,
    )
    series = aggregate_series(7, "REVENUE", "12M", "V1.0", [zero_zero, valid], "BASE")
    assert series.observation_count == 2
    assert series.bias_eligible_count == 1
    assert series.bias_undefined == {"BIAS_UNDEFINED_ZERO_ZERO": 1}
    assert series.bias == pytest.approx(10.0)


def test_p38_mape_bias_independent_counts_mixed_series():
    observations = [
        # Two fully effective observations.
        *[
            build_observation(
                _record(forecast_id=i + 1, forecast_period_id=101 + i),
                "REVENUE",
                _actual(period=101 + i),
            )
            for i in range(2)
        ],
        # Two Actual-zero: scored-eligible, MAPE-excluded, Bias-eligible.
        *[
            build_observation(
                _record(forecast_id=10 + i, forecast_period_id=110 + i),
                "REVENUE",
                _actual(period=110 + i, value=0.0),
            )
            for i in range(2)
        ],
        # One ZERO_BASE quarantine (F=0/A!=0): in neither count.
        build_observation(
            _record(forecast_id=20, forecast_period_id=120, revenue=0.0),
            "REVENUE",
            _actual(period=120, value=500.0),
        ),
    ]
    series = aggregate_observations(observations)[_series_key()]
    assert series.total_observations == 5
    assert series.observation_count == 4
    assert series.mape_effective_count == 2
    assert series.bias_eligible_count == 4
    assert series.quarantined == {"ZERO_BASE": 1, "ACTUAL_ZERO": 2}
    # MAPE over the 2 effective only; Bias over all 4 eligible
    # (10% + 10% - 100% - 100%) / 4 = -45%.
    assert series.mape == pytest.approx(10.0)
    assert series.bias == pytest.approx(-45.0)
    # Sufficiency band follows the scored-eligible count (4 → INSUFFICIENT).
    assert series.confidence_level == "INSUFFICIENT_DATA"


def test_p38_baseline_bias_paired_same_event_set():
    observations = [
        build_observation(
            _record(forecast_id=i + 1, forecast_period_id=101 + i),
            "REVENUE",
            _actual(period=101 + i),
        )
        for i in range(4)
    ]
    baselines = {
        observation.key.as_tuple(): 900.0 for observation in observations
    }
    # Corrupt one baseline to zero: its APE vanishes AND its Bias term
    # vanishes, proving pairing (same events, no silent substitution).
    zeroed_key = observations[0].key.as_tuple()
    baselines[zeroed_key] = 0.0
    series = aggregate_observations(observations, baselines)[_series_key()]
    assert series.mape_effective_count == 4
    assert series.bias_eligible_count == 4
    expected_mape = (200.0 / 900.0 * 100.0 * 3) / 4
    assert series.mape == pytest.approx(10.0)
    # Baseline MAPE uses only the 3 non-zero MAPE-effective baselines.
    assert series.baseline_mape == pytest.approx(200.0 / 900.0 * 100.0)
    # Baseline Bias uses only the 3 paired Bias-eligible Baseline terms:
    # (200/900*100)*3/3 — the zero baseline contributes no term.
    assert series.baseline_bias == pytest.approx(200.0 / 900.0 * 100.0)
    assert series.baseline_mape != pytest.approx(expected_mape)
    assert series.relative_improvement is not None


# --- Adversarial combos ------------------------------------------------------


def test_p38_three_scenarios_share_one_actual_no_pooling():
    shared = _actual()
    records = [
        _record(forecast_id=i + 1, scenario=scenario)
        for i, scenario in enumerate(("BEAR", "BASE", "BULL"))
    ]
    result = run_evaluation_pipeline(
        records, ["REVENUE"], {(7, 101, "REVENUE"): shared}
    )
    assert result.series_count == 3
    for scenario in ("BEAR", "BASE", "BULL"):
        series = result.verdicts[_series_key(scenario)].series
        assert series.observation_count == 1
        assert series.mape_effective_count == 1
        assert series.bias_eligible_count == 1


def test_p38_mixed_scenarios_plus_duplicates():
    from src.evaluation.observation import flag_duplicates

    base = build_observation(_record(), "REVENUE", _actual())
    base_dup = build_observation(_record(), "REVENUE", _actual())
    bull = build_observation(
        _record(forecast_id=2, scenario="BULL"), "REVENUE", _actual()
    )
    flagged = flag_duplicates([base, base_dup, bull])
    assert flagged[0].duplicate_key is not None
    assert flagged[2].duplicate_key is None
    results = aggregate_observations(flagged)
    base_series = results[_series_key("BASE")]
    bull_series = results[_series_key("BULL")]
    assert base_series.observation_count == 0
    assert base_series.quarantined == {"DUPLICATE_QUARANTINED": 2}
    assert bull_series.observation_count == 1
    assert bull_series.mape_effective_count == 1


def test_p38_actual_zero_with_independent_eligibility_mixed():
    observations = [
        build_observation(
            _record(forecast_id=1, forecast_period_id=101),
            "REVENUE",
            _actual(period=101, value=0.0),
        ),
        build_observation(
            _record(forecast_id=2, forecast_period_id=102, revenue=-500.0),
            "REVENUE",
            _actual(period=102, value=0.0),
        ),
        build_observation(
            _record(forecast_id=3, forecast_period_id=103),
            "REVENUE",
            _actual(period=103),
        ),
    ]
    series = aggregate_observations(observations)[_series_key()]
    assert series.observation_count == 3
    assert series.mape_effective_count == 1
    assert series.bias_eligible_count == 3
    # Bias = (-100 + 100 + 10) / 3 = 10/3.
    assert series.bias == pytest.approx(10.0 / 3.0)
    assert series.mape == pytest.approx(10.0)


def test_p38_reordered_observations_stable():
    def _make(order):
        observations = [
            build_observation(
                _record(forecast_id=i + 1, forecast_period_id=101 + i),
                "REVENUE",
                _actual(
                    period=101 + i,
                    value=0.0 if i in (1, 3) else 1100.0,
                ),
            )
            for i in order
        ]
        return aggregate_observations(observations)[_series_key()]

    forward = _make([0, 1, 2, 3, 4])
    reversed_series = _make([4, 3, 2, 1, 0])
    for series in (forward, reversed_series):
        assert series.observation_count == 5
        assert series.mape_effective_count == 3
        assert series.bias_eligible_count == 5
        assert series.quarantined == {"ACTUAL_ZERO": 2}
    assert forward.mape == pytest.approx(reversed_series.mape)
    assert forward.bias == pytest.approx(reversed_series.bias)


def test_p38_reliability_stays_none_and_sufficiency_bands():
    from src.evaluation.metrics import observation_confidence

    assert observation_confidence(4) == "INSUFFICIENT_DATA"
    assert observation_confidence(5) == "LOW_CONFIDENCE"
    assert observation_confidence(8) == "MODERATE_CONFIDENCE"
    assert observation_confidence(12) == "ADEQUATE"
    periods = list(range(101, 109))
    records = [_record(forecast_period_id=p) for p in periods]
    actuals = {(7, p, "REVENUE"): _actual(period=p) for p in periods}
    result = run_evaluation_pipeline(records, ["REVENUE"], actuals)
    verdict = result.verdicts[_series_key()]
    assert verdict.series.confidence_level == "MODERATE_CONFIDENCE"
    assert verdict.governance.reliability.reliability is None


# --- D-e: D1-compliant Actual tie-break (fail closed, no DB-ID fallback) ------


def test_p38_exact_actual_tie_fails_closed_version_order_still_works():
    from src.evaluation.observation import select_actual

    # Version-number ordering still resolves publication ties.
    low = _actual(
        report_version_id=99, report_version_number=1,
        publication_datetime=AFTER,
    )
    high = _actual(
        report_version_id=7, report_version_number=2,
        publication_datetime=AFTER,
    )
    assert select_actual([high, low]) is low
    # Exact (publication-timestamp, version-number) ties fail closed per
    # owner-approved D1 (temp_report.md:4727) — no arbitrary database-ID
    # ordering, through select_actual and through the pipeline path.
    tied_a = _actual(
        report_version_id=80, report_version_number=4,
        publication_datetime=AFTER,
    )
    tied_b = _actual(
        report_version_id=12, report_version_number=4,
        publication_datetime=AFTER,
    )
    with pytest.raises(ValueError, match="no defensible ordering"):
        select_actual([tied_a, tied_b])
    with pytest.raises(ValueError, match="no defensible ordering"):
        run_evaluation_pipeline(
            [_record()], ["REVENUE"], {(7, 101, "REVENUE"): [tied_a, tied_b]}
        )
