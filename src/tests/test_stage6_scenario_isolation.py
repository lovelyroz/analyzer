"""Stage 6 Prompt 35 Phase 3b: scenario-isolation tests (TEST FILES ONLY).

Proves Bear/Base/Bull stay separate end to end through the in-memory
evaluation path: EvaluationKey identity, per-scenario aggregation
(SeriesKey 5-tuple), same-scenario baseline pairing, fail-closed missing
scenario, and adversarial insertion/duplicate/empty boundaries.

Every test asserts BOTH the expected result AND the absence of
cross-scenario leakage where applicable.
"""

from datetime import datetime, timezone
from itertools import permutations

import pytest

from src.evaluation.aggregate import aggregate_observations
from src.evaluation.observation import (
    EvaluationKey,
    build_observation,
    evaluation_key_for,
    flag_duplicates,
)
from src.evaluation.pipeline import run_evaluation_pipeline
from src.evaluation.schema import ActualObservation
from src.forecast.schema import ForecastRecord

CUTOFF = datetime(2024, 6, 30, tzinfo=timezone.utc)
AFTER = datetime(2024, 9, 30, tzinfo=timezone.utc)
STAMP = datetime(2024, 7, 1, tzinfo=timezone.utc)

SCENARIOS = ("BEAR", "BASE", "BULL")


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


def _series_key(scenario, company=7, horizon="12M", version="V1.0"):
    return (company, "REVENUE", horizon, version, scenario)


# --- (a) key identity: all three pairs + hashing/set/dict --------------------


def test_keys_all_three_pairs_unequal():
    keys = {
        scenario: evaluation_key_for(_record(scenario=scenario), "REVENUE")
        for scenario in SCENARIOS
    }
    for first, second in permutations(SCENARIOS, 2):
        assert keys[first] != keys[second]
    # No cross-scenario equality in either direction: 3 distinct identities.
    assert len(set(keys.values())) == 3


def test_keys_preserve_canonical_scenario():
    for scenario in SCENARIOS:
        key = evaluation_key_for(_record(scenario=scenario), "REVENUE")
        assert key.scenario == scenario
        assert key.as_tuple()[-1] == scenario


def test_keys_hash_set_dict_behavior():
    keys = [
        evaluation_key_for(_record(scenario=scenario), "REVENUE")
        for scenario in SCENARIOS
    ]
    assert len(set(keys)) == 3
    by_key = {key: key.scenario for key in keys}
    assert sorted(by_key.values()) == ["BASE", "BEAR", "BULL"]
    # Equal keys collapse: same scenario hashes equal and dedupes.
    twins = [
        evaluation_key_for(_record(scenario="BASE"), "REVENUE"),
        evaluation_key_for(_record(scenario="BASE"), "REVENUE"),
    ]
    assert twins[0] == twins[1]
    assert hash(twins[0]) == hash(twins[1])
    assert len(set(twins)) == 1
    assert {twins[0]: "x", twins[1]: "y"} == {twins[0]: "y"}


# --- (b) three separate series, independent counts, unpooled inputs -----------


def test_three_scenarios_yield_three_series():
    observations = [_observation(scenario=scenario) for scenario in SCENARIOS]
    results = aggregate_observations(observations)
    assert set(results) == {_series_key(scenario) for scenario in SCENARIOS}
    for scenario in SCENARIOS:
        series = results[_series_key(scenario)]
        assert series.scenario == scenario
        assert series.observation_count == 1
        assert series.total_observations == 1
        # No leakage: each series holds only its own observation.
        assert {item.key.scenario for item in series.observations} == {scenario}


def test_mape_bias_inputs_not_pooled_across_scenarios():
    # Scenario-specific forecast values against a shared Actual: each series
    # must report its own MAPE/Bias, never a pooled mean.
    observations = [
        _observation(forecast_value=900.0, actual_value=1100.0, scenario="BEAR"),
        _observation(forecast_value=1000.0, actual_value=1100.0, scenario="BASE"),
        _observation(forecast_value=1100.0, actual_value=1100.0, scenario="BULL"),
    ]
    results = aggregate_observations(observations)
    bear = results[_series_key("BEAR")]
    base = results[_series_key("BASE")]
    bull = results[_series_key("BULL")]
    assert bear.mape == pytest.approx(200.0 / 9.0)
    assert bear.bias == pytest.approx(200.0 / 9.0)
    assert base.mape == pytest.approx(10.0)
    assert base.bias == pytest.approx(10.0)
    assert bull.mape == pytest.approx(0.0)
    assert bull.bias == pytest.approx(0.0)
    # Pooled MAPE would be (22.22 + 10 + 0) / 3 = 10.74 for every series;
    # none of the three equals the pooled value except by coincidence of BASE.
    assert bear.mape != pytest.approx((200.0 / 9.0 + 10.0 + 0.0) / 3.0)
    assert bull.mape != pytest.approx((200.0 / 9.0 + 10.0 + 0.0) / 3.0)


def test_series_evaluation_carries_scenario():
    observations = [_observation(scenario=scenario) for scenario in SCENARIOS]
    results = aggregate_observations(observations)
    for scenario in SCENARIOS:
        series = results[_series_key(scenario)]
        assert series.scenario == scenario
        assert series.company_id == 7
        assert series.metric_code == "REVENUE"


# --- (c) baseline pairing stays within the same scenario ----------------------


def test_baseline_pairing_stays_within_scenario():
    observations = [_observation(scenario=scenario) for scenario in SCENARIOS]
    baselines = {
        (7, "REVENUE", 101, "12M", "V1.0", CUTOFF, "BEAR"): 900.0,
        (7, "REVENUE", 101, "12M", "V1.0", CUTOFF, "BASE"): 1000.0,
        (7, "REVENUE", 101, "12M", "V1.0", CUTOFF, "BULL"): 1100.0,
    }
    results = aggregate_observations(observations, baselines)
    assert results[_series_key("BEAR")].baseline_mape == pytest.approx(200.0 / 9.0)
    assert results[_series_key("BASE")].baseline_mape == pytest.approx(10.0)
    assert results[_series_key("BULL")].baseline_mape == pytest.approx(0.0)
    # Cross-check: BEAR model MAPE equals its own baseline MAPE here, but the
    # BASE/BULL pairings differ from each other's baselines — no sharing.
    assert results[_series_key("BASE")].baseline_mape != results[_series_key("BEAR")].baseline_mape
    assert results[_series_key("BULL")].baseline_mape != results[_series_key("BASE")].baseline_mape


def test_baseline_absent_in_other_scenarios():
    observations = [_observation(scenario=scenario) for scenario in SCENARIOS]
    baselines = {(7, "REVENUE", 101, "12M", "V1.0", CUTOFF, "BASE"): 900.0}
    results = aggregate_observations(observations, baselines)
    assert results[_series_key("BASE")].baseline_mape == pytest.approx(200.0 / 9.0)
    assert results[_series_key("BEAR")].baseline_mape is None
    assert results[_series_key("BULL")].baseline_mape is None
    assert results[_series_key("BEAR")].relative_improvement is None
    assert results[_series_key("BULL")].relative_improvement is None


# --- (d) missing/empty scenario fails closed ----------------------------------


@pytest.mark.parametrize("bad", ["", None])
def test_missing_scenario_raises_fail_closed(bad):
    with pytest.raises(ValueError):
        EvaluationKey(
            company_id=7,
            metric_code="REVENUE",
            financial_period_id=101,
            forecast_horizon="12M",
            model_version="V1.0",
            forecast_cutoff_datetime=CUTOFF,
            scenario=bad,
        )


def test_empty_scenario_record_raises_fail_closed():
    # Never silently Base: the key construction itself refuses.
    with pytest.raises(ValueError):
        evaluation_key_for(_record(scenario=""), "REVENUE")


def test_noncanonical_scenario_preserved_verbatim_and_isolated():
    # A non-empty unknown scenario is not collapsed into any canonical one:
    # it stays verbatim and aggregates alone.
    key = evaluation_key_for(_record(scenario="SIDEWAYS"), "REVENUE")
    assert key.scenario == "SIDEWAYS"
    results = aggregate_observations(
        [_observation(scenario="SIDEWAYS"), _observation(scenario="BASE")]
    )
    assert set(results) == {_series_key("SIDEWAYS"), _series_key("BASE")}
    assert results[_series_key("SIDEWAYS")].observation_count == 1
    assert results[_series_key("BASE")].observation_count == 1


# --- (e) single-scenario numerics unchanged -----------------------------------


def test_single_scenario_values_unchanged():
    results = aggregate_observations([_observation(scenario="BASE")])
    assert set(results) == {_series_key("BASE")}
    series = results[_series_key("BASE")]
    assert series.mape == pytest.approx(10.0)
    assert series.bias == pytest.approx(10.0)
    assert series.observation_count == 1
    assert series.confidence_level == "INSUFFICIENT_DATA"


# --- (f) one event x three scenarios is not three observations ----------------


def test_three_scenarios_not_three_observations_in_shared_series():
    observations = [_observation(scenario=scenario) for scenario in SCENARIOS]
    results = aggregate_observations(observations)
    assert len(results) == 3
    for scenario in SCENARIOS:
        series = results[_series_key(scenario)]
        assert series.observation_count == 1
        assert series.confidence_level == "INSUFFICIENT_DATA"
    # Regression: a scenario-free grouping would pool to one series with
    # count 3; no series here holds more than its own single observation.
    assert all(series.total_observations == 1 for series in results.values())
    assert sum(series.observation_count for series in results.values()) == 3


# --- (g) adversarial ----------------------------------------------------------


def test_insertion_order_all_six_permutations():
    observations = [_observation(scenario=scenario) for scenario in SCENARIOS]
    expected_keys = {_series_key(scenario) for scenario in SCENARIOS}
    for order in permutations(observations):
        results = aggregate_observations(list(order))
        assert set(results) == expected_keys
        for scenario in SCENARIOS:
            series = results[_series_key(scenario)]
            assert series.observation_count == 1
            assert series.mape == pytest.approx(10.0)
            assert {item.key.scenario for item in series.observations} == {scenario}


def test_interleaved_multi_company_inputs():
    interleaved = [
        _observation(scenario="BEAR", company_id=7),
        _observation(scenario="BULL", company_id=9),
        _observation(scenario="BASE", company_id=7),
        _observation(scenario="BEAR", company_id=9),
        _observation(scenario="BULL", company_id=7),
        _observation(scenario="BASE", company_id=9),
    ]
    results = aggregate_observations(interleaved)
    assert len(results) == 6
    for company in (7, 9):
        for scenario in SCENARIOS:
            series = results[_series_key(scenario, company=company)]
            assert series.observation_count == 1
            assert series.company_id == company
            assert series.scenario == scenario
            assert series.mape == pytest.approx(10.0)
            assert {item.key.scenario for item in series.observations} == {scenario}


def test_duplicate_within_one_scenario_quarantines_only_that_scenario():
    # Two identical BASE observations collide; the BULL observation must be
    # untouched: same-scenario keys collide, cross-scenario keys never do.
    first = _observation(scenario="BASE")
    second = _observation(scenario="BASE")
    bull = _observation(scenario="BULL")
    flagged = flag_duplicates([first, second, bull])
    assert flagged[0].duplicate_key == flagged[1].duplicate_key
    assert flagged[2].duplicate_key is None
    results = aggregate_observations([first, second, bull])
    base = results[_series_key("BASE")]
    bull_series = results[_series_key("BULL")]
    assert base.observation_count == 0
    assert base.quarantined == {"DUPLICATE_QUARANTINED": 2}
    assert base.mape is None and base.bias is None
    assert bull_series.observation_count == 1
    assert bull_series.quarantined == {}
    assert bull_series.mape == pytest.approx(10.0)


def test_identical_values_across_scenarios_still_separate():
    observations = [
        _observation(forecast_value=1000.0, actual_value=1100.0, scenario=scenario)
        for scenario in SCENARIOS
    ]
    results = aggregate_observations(observations)
    assert len(results) == 3
    for scenario in SCENARIOS:
        series = results[_series_key(scenario)]
        assert series.observation_count == 1
        assert series.mape == pytest.approx(10.0)
        assert series.quarantined == {}


def test_empty_input_empty_result():
    assert aggregate_observations([]) == {}


def test_single_scenario_input_one_series():
    results = aggregate_observations([_observation(scenario="BULL")])
    assert set(results) == {_series_key("BULL")}
    assert results[_series_key("BULL")].observation_count == 1


# --- production path: three scenarios end to end ------------------------------


def _pipeline_run(records, baselines=None):
    return run_evaluation_pipeline(
        records=records,
        metric_codes=["REVENUE"],
        actuals={(7, 101, "REVENUE"): _actual()},
        baselines=baselines,
    )


def test_pipeline_three_scenarios_end_to_end():
    records = [
        _record(scenario="BEAR", revenue=900.0),
        _record(scenario="BASE", revenue=1000.0),
        _record(scenario="BULL", revenue=1100.0),
    ]
    result = _pipeline_run(records)
    assert result.series_count == 3
    bear = result.verdicts[_series_key("BEAR")].series
    base = result.verdicts[_series_key("BASE")].series
    bull = result.verdicts[_series_key("BULL")].series
    assert (bear.scenario, base.scenario, bull.scenario) == ("BEAR", "BASE", "BULL")
    assert bear.observation_count == base.observation_count == bull.observation_count == 1
    assert bear.mape == pytest.approx(200.0 / 9.0)
    assert base.mape == pytest.approx(10.0)
    assert bull.mape == pytest.approx(0.0)


def test_pipeline_baseline_pairing_per_scenario():
    records = [_record(scenario=scenario) for scenario in SCENARIOS]
    baselines = {
        (7, "REVENUE", 101, "12M", "V1.0", CUTOFF, scenario): value
        for scenario, value in (("BEAR", 900.0), ("BASE", 1000.0), ("BULL", 1100.0))
    }
    result = _pipeline_run(records, baselines=baselines)
    assert result.series_count == 3
    assert result.verdicts[_series_key("BEAR")].series.baseline_mape == pytest.approx(200.0 / 9.0)
    assert result.verdicts[_series_key("BASE")].series.baseline_mape == pytest.approx(10.0)
    assert result.verdicts[_series_key("BULL")].series.baseline_mape == pytest.approx(0.0)
