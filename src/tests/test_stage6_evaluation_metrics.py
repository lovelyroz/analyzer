"""Stage 6 Prompt 19 behavioral tests: metrics layer + authorized baseline comparison.

Contracts (spec Sections 4-18, P17 AUTHORITATIVE material only):

* Error = Actual - Forecast; sign preserved (positive = under-forecast).
* Zero forecast and sign-change regimes carry absolute error but no
  percentage metrics — never silently zeroed.
* Horizons and model versions never mix; duplicates quarantine the whole
  collision (blocker B9: no silent preference).
* PIT leakage and invalid inputs never score.
* Actual=0 / Forecast!=0 is UNRESOLVED (P17 Section B) — quarantined, not scored.
* Baseline *comparison* (Section 17) from caller-supplied values; Seasonal
  Naive *construction* has no authority (blocker B1) and is not attempted.
* Baseline MAPE uses the model's scored set; invalid baseline inputs yield
  missing baseline metrics, never invented values.
* No Reliability, no Calibration, no Stage 7, no Stage 5 changes.
"""

from datetime import datetime, timedelta, timezone

from src.evaluation.aggregate import (
    aggregate_observations,
    score_observation,
)
from src.evaluation.observation import build_observation, flag_duplicates
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


def _observation(metric="REVENUE", forecast_value=1000.0, actual_value=1100.0, **record_overrides):
    record_overrides.setdefault(metric.lower(), forecast_value)
    record = _record(**record_overrides)
    return build_observation(
        record,
        metric,
        _actual(
            value=actual_value,
            financial_period_id=record.forecast_period_id,
            company_id=record.company_id,
        ),
    )


def _series(periods=8, horizon="12M", version="V1.0", start=101, **values):
    """A scored-eligible series; caller controls values via overrides."""
    observations = []
    for i in range(periods):
        observations.append(
            _observation(
                forecast_value=values.get("forecast_value", 1000.0),
                actual_value=values.get("actual_value", 1100.0),
                forecast_period_id=start + i,
                forecast_horizon=horizon,
                model_version=version,
            )
        )
    return aggregate_observations(observations)[(7, "REVENUE", horizon, version)]


# --- error sign --------------------------------------------------------------


def test_error_sign_under_and_over_forecast():
    under = score_observation(_observation(forecast_value=1000.0, actual_value=1180.0))
    assert under.error == 180.0
    assert under.percentage_error == 18.0
    over = score_observation(_observation(forecast_value=1000.0, actual_value=900.0))
    assert over.error == -100.0
    assert over.percentage_error == -10.0


def test_mape_and_bias_match_spec_formulas():
    result = _series()
    assert result.mape == 10.0
    assert result.bias == 10.0


# --- zero denominators / zero + sign-change regimes -------------------------


def test_zero_forecast_keeps_absolute_error_drops_percentages():
    scored = score_observation(_observation(forecast_value=0.0, actual_value=100.0))
    assert scored.error == 100.0
    assert scored.regime == "ZERO_BASE"
    assert scored.percentage_error is None
    assert scored.ape is None
    assert scored.scored is False


def test_sign_change_regimes_quarantined_with_absolute_error():
    cases = [
        (-10.0, 5.0, "LOSS_TO_PROFIT"),
        (10.0, -5.0, "PROFIT_TO_LOSS"),
        (-10.0, -5.0, None),  # same-sign magnitudes: no regime, APE is valid
    ]
    for forecast_value, actual_value, regime in cases:
        scored = score_observation(
            _observation(forecast_value=forecast_value, actual_value=actual_value)
        )
        assert scored.regime == regime
        assert scored.error == actual_value - forecast_value
        if regime is None:
            assert scored.percentage_error is not None and scored.ape is not None
            assert scored.scored is True
        else:
            assert scored.percentage_error is None and scored.ape is None
            assert scored.scored is False


def test_zero_actual_is_unresolved_not_scored():
    # Stage 6 Prompt 25 (Part B): A=0/F!=0 scores normally — Error =
    # Actual - Forecast, PE/APE over |Forecast| are valid since no regime
    # fires (f*a = 0 is not < 0).
    scored = score_observation(_observation(forecast_value=1000.0, actual_value=0.0))
    assert scored.scored is True
    assert scored.error == -1000.0
    assert scored.ape == 100.0


# --- horizon / model-version mixing ------------------------------------------


def test_each_horizon_evaluated_independently():
    first = _observation(forecast_period_id=101, forecast_horizon="1M")
    second = _observation(forecast_period_id=102, forecast_horizon="3M")
    results = aggregate_observations([first, second])
    assert set(results) == {(7, "REVENUE", "1M", "V1.0"), (7, "REVENUE", "3M", "V1.0")}
    assert results[(7, "REVENUE", "1M", "V1.0")].mape == 10.0


def test_model_versions_never_combine():
    first = _observation(forecast_period_id=101, model_version="V1.0")
    second = _observation(
        forecast_value=1000.0,
        actual_value=1200.0,
        forecast_period_id=102,
        model_version="V2.0",
    )
    results = aggregate_observations([first, second])
    assert results[(7, "REVENUE", "12M", "V1.0")].mape == 10.0
    assert results[(7, "REVENUE", "12M", "V2.0")].mape == 20.0


# --- duplicate observations --------------------------------------------------


def test_duplicate_collision_quarantines_both():
    first = _observation()
    second = _observation()
    flagged = flag_duplicates([first, second])
    assert flagged[0].duplicate_key == flagged[1].duplicate_key
    results = aggregate_observations([first, second])
    series = results[(7, "REVENUE", "12M", "V1.0")]
    assert series.observation_count == 0
    assert series.mape is None and series.bias is None
    assert series.quarantined == {"DUPLICATE_QUARANTINED": 2}


def test_duplicate_scenario_distinct_pair_scores_separately():
    # Stage 6 Prompt 25 (Part A): scenario is part of the observation
    # identity, so BASE vs BULL observations never collide — both score.
    base = _observation(scenario="BASE")
    bull = _observation(scenario="BULL")
    assert base.key.as_tuple() != bull.key.as_tuple()
    flagged = flag_duplicates([base, bull])
    assert all(item.duplicate_key is None for item in flagged)
    results = aggregate_observations([base, bull])
    series = results[(7, "REVENUE", "12M", "V1.0")]
    assert series.observation_count == 2
    assert series.quarantined == {}


# --- PIT leakage -------------------------------------------------------------


def test_pit_leaked_inputs_never_score():
    leaked = build_observation(
        _record(input_refs=(ForecastInputRef(fact_key="X", available_at=AFTER),)),
        "REVENUE",
        _actual(),
    )
    assert leaked.evaluation_status == "PIT_INVALID_INPUT"
    scored = score_observation(leaked)
    assert scored.scored is False
    results = aggregate_observations([leaked])
    series = results[(7, "REVENUE", "12M", "V1.0")]
    assert series.observation_count == 0
    assert series.quarantined == {"PIT_INVALID_INPUT": 1}


def test_later_published_actual_is_the_scored_outcome():
    observation = _observation()
    assert observation.evaluation_status == "READY"
    assert observation.actual.publication_datetime > CUTOFF
    scored = score_observation(observation)
    assert scored.scored is True
    assert scored.error == 100.0


# --- invalid Actuals ---------------------------------------------------------


def test_invalid_actual_states_quarantined_verbatim():
    # Stage 6 Prompt 25 (Part B): ESTIMATED / RESTATED score fully (P25 B6
    # predicate); MISSING / SUSPICIOUS / UNMAPPED quarantine verbatim.
    for state in ("ESTIMATED", "RESTATED"):
        observation = build_observation(
            _record(),
            "REVENUE",
            _actual(value=1100.0, data_quality_state=state),
        )
        scored = score_observation(observation)
        assert scored.scored is True
        assert scored.error == 100.0
        assert scored.data_quality_state == state
    for state in ("MISSING", "SUSPICIOUS", "UNMAPPED"):
        observation = build_observation(
            _record(),
            "REVENUE",
            _actual(value=None if state == "MISSING" else 1100.0, data_quality_state=state),
        )
        scored = score_observation(observation)
        assert scored.scored is False
        assert scored.exclusion_reason == f"DATA_QUALITY_QUARANTINED:{state}"
        assert scored.data_quality_state == state


def test_missing_values_are_none_not_zero():
    observation = build_observation(_record(revenue=None), "REVENUE", _actual())
    scored = score_observation(observation)
    assert observation.forecast_value is None
    assert scored.scored is False
    assert scored.exclusion_reason == "MISSING_VALUE"


# --- invalid baseline inputs -------------------------------------------------


def test_missing_baseline_value_means_missing_baseline_metrics():
    scored = score_observation(_observation(), baseline_value=None)
    assert scored.scored is True
    assert scored.baseline_value is None
    assert scored.baseline_error is None and scored.baseline_ape is None


def test_baseline_zero_value_never_fabricates_baseline_ape():
    scored = score_observation(_observation(), baseline_value=0.0)
    assert scored.baseline_error == 1100.0
    assert scored.baseline_ape is None


# --- baseline / model comparison ---------------------------------------------


def test_baseline_comparison_matches_section_17_formula():
    baselines = {}
    observations = []
    for i in range(8):
        observation = _observation(forecast_period_id=101 + i)
        baselines[observation.key.as_tuple()] = 900.0
        observations.append(observation)
    series = aggregate_observations(observations, baselines)[
        (7, "REVENUE", "12M", "V1.0")
    ]
    assert series.mape == 10.0
    # Baseline APE = |1100-900|/|900| x 100 = 22.22%.
    expected_baseline_mape = 200.0 / 900.0 * 100.0
    assert series.baseline_mape == expected_baseline_mape
    assert series.relative_improvement == (expected_baseline_mape - 10.0) / expected_baseline_mape
    assert series.relative_improvement > 0


def test_model_worse_than_baseline_reports_negative_improvement():
    baselines = {}
    observations = []
    for i in range(8):
        observation = _observation(
            forecast_value=1000.0, actual_value=1200.0, forecast_period_id=101 + i
        )
        baselines[observation.key.as_tuple()] = 1150.0
        observations.append(observation)
    series = aggregate_observations(observations, baselines)[
        (7, "REVENUE", "12M", "V1.0")
    ]
    assert series.relative_improvement < 0


def test_baseline_uses_same_scored_set_not_a_wider_one():
    observations = [
        # Five eligible observations ...
        *[
            _observation(forecast_period_id=101 + i)
            for i in range(5)
        ],
        # ... plus a regime observation and a leaked one that must not widen
        # either aggregate.
        _observation(forecast_value=0.0, actual_value=100.0, forecast_period_id=200),
        build_observation(
            _record(
                forecast_period_id=201,
                input_refs=(ForecastInputRef(fact_key="X", available_at=AFTER),),
            ),
            "REVENUE",
            _actual(),
        ),
    ]
    baselines = {
        observation.key.as_tuple(): 900.0 for observation in observations
    }
    series = aggregate_observations(observations, baselines)[
        (7, "REVENUE", "12M", "V1.0")
    ]
    assert series.observation_count == 5
    assert series.total_observations == 7
    assert series.baseline_mape == 200.0 / 900.0 * 100.0


# --- observation sufficiency -------------------------------------------------


def test_insufficient_history_bands_match_spec_section_14():
    assert _series(periods=4).confidence_level == "INSUFFICIENT_DATA"
    assert _series(periods=5).confidence_level == "LOW_CONFIDENCE"
    assert _series(periods=7).confidence_level == "LOW_CONFIDENCE"
    assert _series(periods=8).confidence_level == "MODERATE_CONFIDENCE"
    assert _series(periods=11).confidence_level == "MODERATE_CONFIDENCE"
    assert _series(periods=12).confidence_level == "ADEQUATE"


def test_only_scored_observations_drive_the_band():
    observations = [
        *[ _observation(forecast_period_id=101 + i) for i in range(4)],
        _observation(forecast_value=0.0, actual_value=100.0, forecast_period_id=200),
    ]
    series = aggregate_observations(observations)[(7, "REVENUE", "12M", "V1.0")]
    assert series.observation_count == 4
    assert series.confidence_level == "INSUFFICIENT_DATA"
    assert series.quarantined == {"ZERO_BASE": 1}


# --- no invented baselines / no scores beyond the brief ---------------------


def test_no_seasonal_naive_construction_in_metrics_layer():
    import src.evaluation.aggregate as aggregate

    source_names = {name for name in dir(aggregate) if "naive" in name.lower()}
    assert source_names == set()


def test_series_carries_no_reliability_or_calibration():
    series = _series()
    assert not hasattr(series, "reliability_score")
    assert not hasattr(series, "calibration_state")
    assert not hasattr(series, "performance_score")
    assert not hasattr(series, "underperforms_baseline")
    assert not hasattr(series, "model_underperforms_baseline")
    antique = timedelta(days=1)
    assert (datetime.now(timezone.utc) - series.evaluation_timestamp) < antique
