"""Stage 6 Prompt 41 Chunk A: canonical cutoff-identity tests (focused set).

Contract: canonical identity (EvaluationKey.forecast_cutoff_datetime) uses the
same authoritative normalization as the P39 guard
(src/evaluation/schema._normalize_datetime). Equivalent instants (naive-UTC,
tz-aware, valid ISO-8601) share one canonical identity; distinct instants stay
distinct; collisions quarantine wholesale via the existing DUPLICATE_QUARANTINED
path (never winner-pick). The P39 guard itself is untouched.
"""

from datetime import datetime, timedelta, timezone

from src.evaluation.observation import (
    EvaluationObservation,
    evaluation_key_for,
    flag_duplicates,
    build_observation,
)
from src.evaluation.pipeline import run_evaluation_pipeline
from src.evaluation.schema import ActualObservation
from src.forecast.schema import ForecastRecord

import pytest

CUTOFF = datetime(2024, 6, 30, tzinfo=timezone.utc)
NAIVE_CUTOFF = datetime(2024, 6, 30)
OFFSET_CUTOFF = datetime(2024, 6, 30, 2, 0, tzinfo=timezone(timedelta(hours=2)))
ISO_CUTOFF = "2024-06-30T00:00:00+00:00"
OTHER = datetime(2024, 3, 31, tzinfo=timezone.utc)
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


def test_p41_01_naive_and_aware_same_instant_share_identity():
    naive_key = evaluation_key_for(
        _record(forecast_id=1, data_cutoff_datetime=NAIVE_CUTOFF), "REVENUE"
    )
    aware_key = evaluation_key_for(
        _record(forecast_id=2, data_cutoff_datetime=CUTOFF), "REVENUE"
    )
    assert naive_key.as_tuple() == aware_key.as_tuple()
    assert naive_key.forecast_cutoff_datetime == CUTOFF
    assert naive_key.forecast_cutoff_datetime.tzinfo is not None


def test_p41_02_tz_offset_equivalent_shares_identity():
    offset_key = evaluation_key_for(
        _record(forecast_id=1, data_cutoff_datetime=OFFSET_CUTOFF), "REVENUE"
    )
    aware_key = evaluation_key_for(
        _record(forecast_id=2, data_cutoff_datetime=CUTOFF), "REVENUE"
    )
    assert offset_key.as_tuple() == aware_key.as_tuple()


def test_p41_03_iso_string_equivalent_shares_identity():
    iso_key = evaluation_key_for(
        _record(forecast_id=1, data_cutoff_datetime=ISO_CUTOFF), "REVENUE"
    )
    aware_key = evaluation_key_for(
        _record(forecast_id=2, data_cutoff_datetime=CUTOFF), "REVENUE"
    )
    assert iso_key.as_tuple() == aware_key.as_tuple()


def test_p41_04_distinct_instants_stay_distinct():
    key = evaluation_key_for(_record(data_cutoff_datetime=CUTOFF), "REVENUE")
    other = evaluation_key_for(
        _record(forecast_id=2, data_cutoff_datetime=OTHER), "REVENUE"
    )
    assert key.as_tuple() != other.as_tuple()


def test_p41_05_equivalent_cutoffs_collide_quarantine_wholesale():
    observations = [
        build_observation(
            _record(forecast_id=1, data_cutoff_datetime=NAIVE_CUTOFF),
            "REVENUE",
            _actual(),
        ),
        build_observation(
            _record(forecast_id=2, data_cutoff_datetime=CUTOFF),
            "REVENUE",
            _actual(),
        ),
    ]
    flagged = flag_duplicates(observations)
    assert all(o.duplicate_key is not None for o in flagged)
    assert flagged[0].duplicate_key == flagged[1].duplicate_key
    result = run_evaluation_pipeline(
        [
            _record(forecast_id=1, data_cutoff_datetime=NAIVE_CUTOFF),
            _record(forecast_id=2, data_cutoff_datetime=CUTOFF),
        ],
        ["REVENUE"],
        {(7, 101, "REVENUE"): _actual()},
    )
    verdict = result.verdicts[(7, "REVENUE", "12M", "V1.0", "BASE")]
    assert verdict.series.quarantined == {"DUPLICATE_QUARANTINED": 2}
    assert verdict.series.observation_count == 0


def test_p41_06_pipeline_guard_accepts_equivalent_pair_single_cutoff():
    result = run_evaluation_pipeline(
        [
            _record(forecast_id=1, forecast_period_id=101,
                    data_cutoff_datetime=NAIVE_CUTOFF),
            _record(forecast_id=2, forecast_period_id=102,
                    data_cutoff_datetime=OFFSET_CUTOFF),
        ],
        ["REVENUE"],
        {
            (7, 101, "REVENUE"): _actual(period=101),
            (7, 102, "REVENUE"): _actual(period=102),
        },
    )
    assert result.artifact is not None
    assert result.artifact.evaluation_cutoff == CUTOFF
    assert result.verdicts[(7, "REVENUE", "12M", "V1.0", "BASE")].series.observation_count == 2


def _actual_map(periods, value=1100.0, **overrides):
    return {
        (7, period, "REVENUE"): _actual(period=period, value=value, **overrides)
        for period in periods
    }


def _ttm(index, period, cutoff=CUTOFF, **overrides):
    return build_observation(
        _record(
            forecast_id=100 + index,
            forecast_period_id=period,
            data_cutoff_datetime=cutoff,
            **overrides
        ),
        "REVENUE",
        _actual(period=period),
    )


def _ttm_null_cutoff(index, period):
    # Mirrors the P39 nearest public boundary: build_observation cannot mint a
    # null-cutoff TTM (construction-time PIT check asserts first), so direct
    # EvaluationObservation construction is the guard's public boundary.
    return EvaluationObservation(
        forecast=_record(
            forecast_id=100 + index,
            forecast_period_id=period,
            data_cutoff_datetime=None,
        ),
        metric_code="REVENUE",
        actual=_actual(period=period),
    )


def _key(scenario="BASE", horizon="12M", version="V1.0"):
    return (7, "REVENUE", horizon, version, scenario)


def _baseline_map(periods, value=1050.0, horizon="12M", version="V1.0",
                  scenario="BASE"):
    return {
        (7, "REVENUE", period, horizon, version, CUTOFF, scenario): value
        for period in periods
    }


# --- three equivalent representations: deterministic, no winner-pick ----------


def test_p41_07_three_equivalent_forms_collide_wholesale_no_winner_pick():
    observations = [
        build_observation(
            _record(forecast_id=1, data_cutoff_datetime=NAIVE_CUTOFF),
            "REVENUE",
            _actual(),
        ),
        build_observation(
            _record(forecast_id=2, data_cutoff_datetime=OFFSET_CUTOFF),
            "REVENUE",
            _actual(),
        ),
        build_observation(
            _record(forecast_id=3, data_cutoff_datetime=ISO_CUTOFF),
            "REVENUE",
            _actual(),
        ),
    ]
    keys = [o.key.as_tuple() for o in observations]
    assert keys[0] == keys[1] == keys[2]
    flagged = flag_duplicates(observations)
    assert all(o.duplicate_key is not None for o in flagged)
    assert flagged[0].duplicate_key == flagged[1].duplicate_key == flagged[2].duplicate_key
    result = run_evaluation_pipeline(
        [
            _record(forecast_id=1, data_cutoff_datetime=NAIVE_CUTOFF),
            _record(forecast_id=2, data_cutoff_datetime=OFFSET_CUTOFF),
            _record(forecast_id=3, data_cutoff_datetime=ISO_CUTOFF),
        ],
        ["REVENUE"],
        _actual_map([101]),
    )
    verdict = result.verdicts[_key()]
    assert verdict.series.total_observations == 3
    assert verdict.series.observation_count == 0
    assert verdict.series.quarantined == {"DUPLICATE_QUARANTINED": 3}
    assert verdict.series.mape is None
    assert verdict.series.bias is None
    assert verdict.series.mape_effective_count == 0
    assert verdict.series.bias_eligible_count == 0


# --- reorder-invariance of equivalent-cutoff inputs ----------------------------


def test_p41_08_reordered_equivalent_cutoffs_decide_identically():
    first = _record(forecast_id=1, forecast_period_id=101,
                    data_cutoff_datetime=NAIVE_CUTOFF)
    second = _record(forecast_id=2, forecast_period_id=102,
                     data_cutoff_datetime=ISO_CUTOFF)
    third = _record(forecast_id=3, forecast_period_id=103,
                    data_cutoff_datetime=OFFSET_CUTOFF)
    actuals = _actual_map([101, 102, 103])
    forward = run_evaluation_pipeline([first, second, third], ["REVENUE"], actuals)
    backward = run_evaluation_pipeline([third, second, first], ["REVENUE"], actuals)
    assert forward.artifact.evaluation_cutoff == CUTOFF
    assert backward.artifact.evaluation_cutoff == CUTOFF
    assert set(forward.verdicts) == set(backward.verdicts)
    for key in forward.verdicts:
        assert (
            forward.verdicts[key].series.observation_count
            == backward.verdicts[key].series.observation_count
        )
        assert (
            forward.verdicts[key].series.quarantined
            == backward.verdicts[key].series.quarantined
        )
    # Failure order-invariance: the mixed set fails either way round.
    other = _record(forecast_id=9, forecast_period_id=104, data_cutoff_datetime=OTHER)
    with pytest.raises(ValueError, match="mixed evaluation cutoffs"):
        run_evaluation_pipeline([first, other], ["REVENUE"], _actual_map([101, 104]))
    with pytest.raises(ValueError, match="mixed evaluation cutoffs"):
        run_evaluation_pipeline([other, first], ["REVENUE"], _actual_map([101, 104]))


# --- repeated TTM with equivalent cutoff cannot inflate anything ----------------


def test_p41_09_repeated_ttm_equivalent_forms_inflate_nothing():
    periods = [101, 102, 103]
    records = [
        _record(forecast_id=index + 1, forecast_period_id=period)
        for index, period in enumerate(periods)
    ]
    baselines = _baseline_map(periods + [201])
    clean = run_evaluation_pipeline(
        records, ["REVENUE"], _actual_map(periods + [201]),
        baselines=baselines, ttm_observations=[_ttm(0, 201, cutoff=NAIVE_CUTOFF)],
    )
    doubled = run_evaluation_pipeline(
        records, ["REVENUE"], _actual_map(periods + [201]),
        baselines=baselines,
        ttm_observations=[
            _ttm(0, 201, cutoff=NAIVE_CUTOFF),
            _ttm(0, 201, cutoff=ISO_CUTOFF),
        ],
    )
    clean_v = clean.verdicts[_key()]
    doubled_v = doubled.verdicts[_key()]
    assert clean_v.series.observation_count == 4
    assert clean_v.ttm_accounted == 1
    # The equivalent-form repeat counts once; both copies quarantine wholesale.
    assert doubled_v.ttm_accounted == 1
    assert doubled_v.series.quarantined == {"DUPLICATE_QUARANTINED": 2}
    assert doubled_v.series.total_observations == 5
    assert doubled_v.series.observation_count == 3
    assert doubled_v.series.mape_effective_count == 3
    assert doubled_v.series.bias_eligible_count == 3
    assert doubled_v.series.mape_effective_count <= clean_v.series.mape_effective_count
    assert doubled_v.series.bias_eligible_count <= clean_v.series.bias_eligible_count
    assert doubled_v.series.confidence_level == clean_v.series.confidence_level
    assert doubled_v.series.mape == pytest.approx(clean_v.series.mape)
    assert doubled_v.series.bias == pytest.approx(clean_v.series.bias)
    assert doubled_v.series.baseline_mape == pytest.approx(clean_v.series.baseline_mape)
    assert doubled_v.series.baseline_bias == pytest.approx(clean_v.series.baseline_bias)
    assert (
        doubled_v.series.relative_improvement
        == pytest.approx(clean_v.series.relative_improvement)
    )
    assert doubled_v.governance.reliability.reliability is None


# --- Forecast/TTM overlap when only the cutoff form differs ---------------------


def test_p41_10_forecast_ttm_overlap_on_cutoff_form_only():
    records = [
        _record(forecast_id=1, forecast_period_id=101),
        _record(forecast_id=2, forecast_period_id=102),
        _record(forecast_id=3, forecast_period_id=201,
                data_cutoff_datetime=NAIVE_CUTOFF),
    ]
    result = run_evaluation_pipeline(
        records, ["REVENUE"], _actual_map([101, 102, 201]),
        ttm_observations=[_ttm(0, 201, cutoff=ISO_CUTOFF)],
    )
    verdict = result.verdicts[_key()]
    assert verdict.series.total_observations == 4
    assert verdict.series.observation_count == 2
    assert verdict.series.quarantined == {"DUPLICATE_QUARANTINED": 2}
    assert verdict.series.mape == pytest.approx(10.0)
    assert verdict.series.bias == pytest.approx(10.0)


# --- distinct periods stay distinct under one canonical instant ------------------


def test_p41_11_distinct_periods_same_canonical_instant_stay_distinct():
    records = [
        _record(forecast_id=1, forecast_period_id=101,
                data_cutoff_datetime=NAIVE_CUTOFF),
        _record(forecast_id=2, forecast_period_id=102,
                data_cutoff_datetime=OFFSET_CUTOFF),
        _record(forecast_id=3, forecast_period_id=103,
                data_cutoff_datetime=ISO_CUTOFF),
    ]
    result = run_evaluation_pipeline(records, ["REVENUE"], _actual_map([101, 102, 103]))
    verdict = result.verdicts[_key()]
    assert verdict.series.observation_count == 3
    assert verdict.series.total_observations == 3
    assert verdict.series.quarantined == {}
    assert verdict.series.mape == pytest.approx(10.0)
    keys = [item.key.as_tuple() for item in verdict.series.observations]
    assert len(set(keys)) == 3


# --- scenario / horizon / version isolation with mixed equivalent forms ----------


def test_p41_12_scenario_isolation_with_mixed_equivalent_forms():
    records = [
        _record(forecast_id=1, scenario="BEAR", data_cutoff_datetime=NAIVE_CUTOFF),
        _record(forecast_id=2, scenario="BASE", data_cutoff_datetime=ISO_CUTOFF),
        _record(forecast_id=3, scenario="BULL", data_cutoff_datetime=OFFSET_CUTOFF),
    ]
    result = run_evaluation_pipeline(records, ["REVENUE"], _actual_map([101]))
    assert result.artifact.evaluation_cutoff == CUTOFF
    assert len(result.verdicts) == 3
    for scenario in ("BEAR", "BASE", "BULL"):
        verdict = result.verdicts[_key(scenario=scenario)]
        assert verdict.series.scenario == scenario
        assert verdict.series.observation_count == 1
        assert "DUPLICATE_QUARANTINED" not in verdict.series.quarantined
        assert verdict.governance.reliability.reliability is None


def test_p41_13_horizon_version_isolation_with_mixed_equivalent_forms():
    records = [
        _record(forecast_id=1, forecast_horizon="12M",
                data_cutoff_datetime=NAIVE_CUTOFF),
        _record(forecast_id=2, forecast_horizon="6M",
                data_cutoff_datetime=ISO_CUTOFF),
    ]
    result = run_evaluation_pipeline(records, ["REVENUE"], _actual_map([101]))
    assert len(result.verdicts) == 2
    for horizon in ("12M", "6M"):
        verdict = result.verdicts[_key(horizon=horizon)]
        assert verdict.series.observation_count == 1
        assert "DUPLICATE_QUARANTINED" not in verdict.series.quarantined
    versions = run_evaluation_pipeline(
        [
            _record(forecast_id=1, model_version="V1.0",
                    data_cutoff_datetime=OFFSET_CUTOFF),
            _record(forecast_id=2, model_version="V2.0",
                    data_cutoff_datetime=NAIVE_CUTOFF),
        ],
        ["REVENUE"],
        _actual_map([101]),
    )
    assert len(versions.verdicts) == 2
    for version in ("V1.0", "V2.0"):
        verdict = versions.verdicts[_key(version=version)]
        assert verdict.series.observation_count == 1
        assert "DUPLICATE_QUARANTINED" not in verdict.series.quarantined


# --- missing / invalid / mixed instants still fail closed ------------------------


def test_p41_14_missing_invalid_mixed_instants_fail_closed():
    with pytest.raises(ValueError, match="missing evaluation cutoff"):
        run_evaluation_pipeline(
            [_record(forecast_id=1, data_cutoff_datetime=None)],
            ["REVENUE"],
            _actual_map([101]),
        )
    with pytest.raises(ValueError):
        run_evaluation_pipeline(
            [_record(forecast_id=1, data_cutoff_datetime="not-a-datetime")],
            ["REVENUE"],
            _actual_map([101]),
        )
    with pytest.raises(ValueError, match="mixed evaluation cutoffs"):
        run_evaluation_pipeline(
            [
                _record(forecast_id=1, data_cutoff_datetime=NAIVE_CUTOFF),
                _record(forecast_id=2, data_cutoff_datetime=OTHER),
            ],
            ["REVENUE"],
            _actual_map([101]),
        )
    with pytest.raises(ValueError, match="missing evaluation cutoff"):
        run_evaluation_pipeline(
            [_record()], ["REVENUE"], _actual_map([101, 201]),
            ttm_observations=[_ttm_null_cutoff(0, 201)],
        )
    with pytest.raises(ValueError, match="mixed evaluation cutoffs"):
        run_evaluation_pipeline(
            [_record(forecast_id=1, data_cutoff_datetime=ISO_CUTOFF)],
            ["REVENUE"],
            _actual_map([101, 201]),
            ttm_observations=[_ttm(0, 201, cutoff=OTHER)],
        )


# --- empty + TTM-only --------------------------------------------------------------


def test_p41_15_empty_and_ttm_only_with_equivalent_forms():
    empty = run_evaluation_pipeline([], ["REVENUE"], {})
    assert empty.artifact is not None
    assert empty.artifact.evaluation_cutoff is None
    assert empty.series_count == 0
    ttm_only = run_evaluation_pipeline(
        [], ["REVENUE"], _actual_map([201]),
        ttm_observations=[_ttm(0, 201, cutoff=ISO_CUTOFF)],
    )
    assert ttm_only.artifact is not None
    assert ttm_only.artifact.evaluation_cutoff == CUTOFF
    assert ttm_only.verdicts[_key()].ttm_accounted == 1


# --- later-published Actuals stay eligible ------------------------------------------


def test_p41_16_later_published_actual_stays_eligible():
    assert AFTER > CUTOFF
    result = run_evaluation_pipeline(
        [_record(data_cutoff_datetime=NAIVE_CUTOFF)],
        ["REVENUE"],
        _actual_map([101]),
    )
    verdict = result.verdicts[_key()]
    assert verdict.series.observation_count == 1
    assert verdict.series.mape == pytest.approx(10.0)
    assert verdict.series.bias == pytest.approx(10.0)


# --- rejection returns no partial result ---------------------------------------------


def test_p41_17_rejected_equivalent_mixed_invocation_returns_no_partial():
    records = [
        _record(forecast_id=1, data_cutoff_datetime=ISO_CUTOFF),
        _record(forecast_id=2, data_cutoff_datetime=OTHER),
    ]
    result = None
    with pytest.raises(ValueError, match="mixed evaluation cutoffs"):
        result = run_evaluation_pipeline(records, ["REVENUE"], _actual_map([101]))
    assert result is None
    clean = run_evaluation_pipeline(
        [_record(data_cutoff_datetime=OFFSET_CUTOFF)],
        ["REVENUE"],
        _actual_map([101]),
    )
    assert clean.artifact.evaluation_cutoff == CUTOFF
