"""Stage 6 Prompt 40 section 5: duplicate-observation invariant matrix.

Contracts (spec Section 7 invariant 16 / Section 42 / D5 + Section 3 rule 16):

* Canonical identity = EvaluationKey 7-tuple
  (company, metric, period, horizon, version, cutoff, scenario).
* Exact duplicates NEVER inflate anything: scored/valid counts, sufficiency,
  Bias/MAPE effective counts, baseline pairing, ttm_accounted.
* Same-identity collisions (exact or conflicting) quarantine WHOLESALE via
  the authorized path (P18 flag_duplicates -> DUPLICATE_QUARANTINED) — no
  silent winner-pick, no arbitrary preference.
* ttm_accounted counts DISTINCT canonical TTM identities per series.
* Distinct identities stay distinct; same numbers under different keys are
  NOT deduped; scenario/horizon/version isolate series.
* All P39 cutoff behaviors stay intact; rejections return no partial result.

Every row runs through run_evaluation_pipeline (L3 production path).
"""

from datetime import datetime, timezone

import pytest

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


def _actual(period=101, value=1100.0, state="VALID", **overrides):
    fields = dict(
        company_id=7,
        financial_period_id=period,
        metric_code="REVENUE",
        value=value,
        report_version_id=55,
        publication_datetime=AFTER,
        data_quality_state=state,
    )
    fields.update(overrides)
    return ActualObservation(**fields)


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


def _key(scenario="BASE", horizon="12M", version="V1.0"):
    return (7, "REVENUE", horizon, version, scenario)


def _run(records, actuals, baselines=None, ttm=None, exclude_estimated=False):
    return run_evaluation_pipeline(
        records=records,
        metric_codes=["REVENUE"],
        actuals=actuals,
        baselines=baselines,
        ttm_observations=ttm,
        exclude_estimated=exclude_estimated,
    )


def _baseline_map(periods, value=1050.0, horizon="12M", version="V1.0",
                  scenario="BASE"):
    return {
        (7, "REVENUE", period, horizon, version, CUTOFF, scenario): value
        for period in periods
    }


# --- one TTM counted once ----------------------------------------------------


def test_p40_01_single_ttm_counted_once():
    result = _run(
        [_record(forecast_period_id=101)],
        _actual_map([101, 201]),
        ttm=[_ttm(0, 201)],
    )
    verdict = result.verdicts[_key()]
    assert verdict.ttm_accounted == 1
    assert verdict.series.total_observations == 2
    assert verdict.series.observation_count == 2
    assert verdict.series.mape == pytest.approx(10.0)
    assert verdict.series.bias == pytest.approx(10.0)


def test_p40_02_two_distinct_ttm_counted_twice():
    result = _run(
        [],
        _actual_map([201, 202]),
        ttm=[_ttm(0, 201), _ttm(1, 202)],
    )
    verdict = result.verdicts[_key()]
    assert verdict.ttm_accounted == 2
    assert verdict.series.observation_count == 2
    assert verdict.series.mape == pytest.approx(10.0)


# --- exact-repeat TTM inflates nothing ----------------------------------------


def test_p40_03_exact_repeat_ttm_inflates_nothing():
    periods = [101, 102, 103]
    records = [
        _record(forecast_id=index + 1, forecast_period_id=period)
        for index, period in enumerate(periods)
    ]
    clean = _run(
        records,
        _actual_map(periods + [201]),
        _baseline_map(periods + [201]),
        ttm=[_ttm(0, 201)],
    )
    doubled = _run(
        records,
        _actual_map(periods + [201]),
        _baseline_map(periods + [201]),
        ttm=[_ttm(0, 201), _ttm(0, 201)],
    )
    clean_v = clean.verdicts[_key()]
    doubled_v = doubled.verdicts[_key()]
    # The repeat counts once and both colliding entries quarantine wholesale.
    assert clean_v.series.observation_count == 4
    assert clean_v.ttm_accounted == 1
    assert doubled_v.ttm_accounted == 1
    assert doubled_v.series.quarantined == {"DUPLICATE_QUARANTINED": 2}
    # Wholesale quarantine removes BOTH colliding copies from scoring, so the
    # doubled run scores exactly the 3 records — never the records plus one
    # silently-picked TTM copy (no winner-pick), never an inflated count.
    assert doubled_v.series.observation_count == 3
    assert doubled_v.series.total_observations == 5
    assert doubled_v.series.mape_effective_count == 3
    assert doubled_v.series.bias_eligible_count == 3
    # Nothing inflates: effective counts never exceed the clean run's,
    # sufficiency, MAPE/Bias values, baseline pairing identical.
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


def test_p40_04_triple_repeat_still_counts_once():
    result = _run(
        [_record(forecast_period_id=101)],
        _actual_map([101, 201]),
        ttm=[_ttm(0, 201), _ttm(0, 201), _ttm(0, 201)],
    )
    verdict = result.verdicts[_key()]
    assert verdict.ttm_accounted == 1
    assert verdict.series.quarantined == {"DUPLICATE_QUARANTINED": 3}
    assert verdict.series.observation_count == 1
    assert verdict.series.mape == pytest.approx(10.0)


# --- reordered duplicates decide identically ----------------------------------


def test_p40_05_reordered_duplicates_same_decision():
    first = _record(forecast_id=1, forecast_period_id=101)
    second = _record(forecast_id=2, forecast_period_id=102)
    actuals = _actual_map([101, 102, 201, 202])
    ttm_a = [_ttm(0, 201), _ttm(1, 202)]
    ttm_b = [_ttm(1, 202), _ttm(0, 201)]
    forward = _run([first, second], actuals, ttm=ttm_a)
    backward = _run([second, first], actuals, ttm=ttm_b)
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
        assert forward.verdicts[key].ttm_accounted == (
            backward.verdicts[key].ttm_accounted
        )
    # Order-invariance holds for collisions too: the doubled supply
    # quarantines wholesale whichever copy arrives first.
    dup_a = _run([first], _actual_map([101, 201]),
                 ttm=[_ttm(0, 201), _ttm(0, 201)])
    dup_b = _run([first], _actual_map([101, 201]),
                 ttm=[_ttm(0, 201), _ttm(0, 201)][::-1])
    assert (
        dup_a.verdicts[_key()].series.quarantined
        == dup_b.verdicts[_key()].series.quarantined
        == {"DUPLICATE_QUARANTINED": 2}
    )


# --- Forecast/TTM same-identity overlap ---------------------------------------


def test_p40_06_forecast_ttm_same_identity_overlap_not_double_counted():
    # Record-built observation for period 201 shares the canonical identity
    # with the TTM observation for period 201 (same company/metric/period/
    # horizon/version/cutoff/scenario) — both quarantine wholesale.
    records = [
        _record(forecast_id=1, forecast_period_id=101),
        _record(forecast_id=2, forecast_period_id=102),
        _record(forecast_id=3, forecast_period_id=201),
    ]
    result = _run(
        records, _actual_map([101, 102, 201]), ttm=[_ttm(0, 201)]
    )
    verdict = result.verdicts[_key()]
    assert verdict.series.total_observations == 4
    assert verdict.series.observation_count == 2
    assert verdict.series.quarantined == {"DUPLICATE_QUARANTINED": 2}
    assert verdict.series.mape == pytest.approx(10.0)
    assert verdict.series.bias == pytest.approx(10.0)


# --- distinct observations stay distinct --------------------------------------


def test_p40_07_distinct_periods_stay_distinct():
    periods = [101, 102, 103, 104]
    records = [
        _record(forecast_id=index + 1, forecast_period_id=period)
        for index, period in enumerate(periods)
    ]
    result = _run(records, _actual_map(periods))
    verdict = result.verdicts[_key()]
    assert verdict.series.observation_count == 4
    assert verdict.series.total_observations == 4
    assert verdict.series.quarantined == {}
    assert verdict.series.mape == pytest.approx(10.0)


def test_p40_08_same_numbers_different_keys_not_deduped():
    # Identical forecast/actual VALUES under different periods are different
    # observations — value equality is never an identity rule.
    periods = [101, 102, 103]
    records = [
        _record(forecast_id=index + 1, forecast_period_id=period,
                revenue=1000.0)
        for index, period in enumerate(periods)
    ]
    result = _run(records, _actual_map(periods, value=1100.0))
    verdict = result.verdicts[_key()]
    assert verdict.series.observation_count == 3
    assert "DUPLICATE_QUARANTINED" not in verdict.series.quarantined
    keys = [item.key.as_tuple() for item in verdict.series.observations]
    assert len(set(keys)) == 3


# --- cross-dimension separation -----------------------------------------------


def test_p40_09_cross_scenario_separation():
    records = [
        _record(forecast_id=index + 1, scenario=scenario)
        for index, scenario in enumerate(("BEAR", "BASE", "BULL"))
    ]
    result = _run(records, _actual_map([101]))
    assert len(result.verdicts) == 3
    for scenario in ("BEAR", "BASE", "BULL"):
        verdict = result.verdicts[_key(scenario=scenario)]
        assert verdict.series.observation_count == 1
        assert verdict.series.mape == pytest.approx(10.0)


def test_p40_10_cross_horizon_separation():
    records = [
        _record(forecast_id=1, forecast_horizon="12M"),
        _record(forecast_id=2, forecast_horizon="6M"),
    ]
    result = _run(records, _actual_map([101]))
    assert len(result.verdicts) == 2
    for horizon in ("12M", "6M"):
        verdict = result.verdicts[_key(horizon=horizon)]
        assert verdict.series.observation_count == 1
        assert "DUPLICATE_QUARANTINED" not in verdict.series.quarantined


def test_p40_11_cross_version_separation():
    records = [
        _record(forecast_id=1, model_version="V1.0"),
        _record(forecast_id=2, model_version="V2.0"),
    ]
    result = _run(records, _actual_map([101]))
    assert len(result.verdicts) == 2
    for version in ("V1.0", "V2.0"):
        verdict = result.verdicts[_key(version=version)]
        assert verdict.series.observation_count == 1
        assert "DUPLICATE_QUARANTINED" not in verdict.series.quarantined


# --- conflicting same-identity: wholesale quarantine, no winner-pick ----------


def test_p40_12_conflicting_same_identity_quarantines_wholesale():
    # Same canonical identity, DIFFERENT forecast values: no defensible
    # ordering exists, so both quarantine — never an arbitrary pick.
    records = [
        _record(forecast_id=1, forecast_period_id=101, revenue=1000.0),
        _record(forecast_id=2, forecast_period_id=101, revenue=1300.0),
    ]
    result = _run(records, _actual_map([101]))
    verdict = result.verdicts[_key()]
    assert verdict.series.total_observations == 2
    assert verdict.series.observation_count == 0
    assert verdict.series.quarantined == {"DUPLICATE_QUARANTINED": 2}
    assert verdict.series.mape is None
    assert verdict.series.bias is None
    assert verdict.series.mape_effective_count == 0
    assert verdict.series.bias_eligible_count == 0


def test_p40_13_conflict_does_not_touch_neighbors():
    records = [
        _record(forecast_id=1, forecast_period_id=101, revenue=1000.0),
        _record(forecast_id=2, forecast_period_id=101, revenue=1300.0),
        _record(forecast_id=3, forecast_period_id=102, revenue=1000.0),
        _record(forecast_id=4, forecast_period_id=103, revenue=1000.0),
    ]
    result = _run(records, _actual_map([101, 102, 103]))
    verdict = result.verdicts[_key()]
    assert verdict.series.observation_count == 2
    assert verdict.series.quarantined == {"DUPLICATE_QUARANTINED": 2}
    assert verdict.series.mape == pytest.approx(10.0)
    assert verdict.series.bias == pytest.approx(10.0)


# --- duplicates cannot inflate sufficiency / Bias / MAPE / baseline -----------


def test_p40_14_duplicates_cannot_inflate_sufficiency():
    # 4 distinct scored observations + an exact-duplicate pair on a 5th
    # period: sufficiency must see 4 (INSUFFICIENT_DATA), never 6.
    records = [
        _record(forecast_id=index + 1, forecast_period_id=period)
        for index, period in enumerate([101, 102, 103, 104])
    ]
    records += [
        _record(forecast_id=5, forecast_period_id=105),
        _record(forecast_id=6, forecast_period_id=105),
    ]
    result = _run(records, _actual_map([101, 102, 103, 104, 105]))
    verdict = result.verdicts[_key()]
    assert verdict.series.total_observations == 6
    assert verdict.series.observation_count == 4
    assert verdict.series.confidence_level == "INSUFFICIENT_DATA"
    assert verdict.series.quarantined == {"DUPLICATE_QUARANTINED": 2}


def test_p40_15_duplicate_leaves_remaining_pairing_intact():
    # Doubling ONE record quarantines exactly that pair; the surviving
    # observations pair with baselines exactly as a clean run of survivors.
    survivor_periods = [102, 103]
    records = (
        [_record(forecast_id=1, forecast_period_id=101)]
        + [
            _record(forecast_id=index + 2, forecast_period_id=period)
            for index, period in enumerate(survivor_periods)
        ]
        + [_record(forecast_id=9, forecast_period_id=101)]
    )
    baselines = _baseline_map([101, 102, 103])
    duped = _run(records, _actual_map([101, 102, 103]), baselines)
    clean = _run(
        [_record(forecast_id=2, forecast_period_id=102),
         _record(forecast_id=3, forecast_period_id=103)],
        _actual_map([102, 103]),
        _baseline_map([102, 103]),
    )
    duped_v = duped.verdicts[_key()]
    clean_v = clean.verdicts[_key()]
    assert duped_v.series.quarantined == {"DUPLICATE_QUARANTINED": 2}
    assert duped_v.series.observation_count == 2
    assert duped_v.series.mape == pytest.approx(clean_v.series.mape)
    assert duped_v.series.bias == pytest.approx(clean_v.series.bias)
    assert duped_v.series.baseline_mape == pytest.approx(clean_v.series.baseline_mape)
    assert duped_v.series.baseline_bias == pytest.approx(clean_v.series.baseline_bias)
    assert (
        duped_v.series.relative_improvement
        == pytest.approx(clean_v.series.relative_improvement)
    )


# --- primary vs sensitivity independently correct ------------------------------


def test_p40_16_primary_vs_sensitivity_independently_correct():
    records = [
        _record(forecast_id=1, forecast_period_id=101),
        _record(forecast_id=2, forecast_period_id=102),
        _record(forecast_id=3, forecast_period_id=103),
    ]
    actuals = {
        (7, 101, "REVENUE"): _actual(period=101, state="VALID"),
        (7, 102, "REVENUE"): _actual(period=102, state="ESTIMATED"),
        (7, 103, "REVENUE"): _actual(period=103, state="VALID"),
        (7, 201, "REVENUE"): _actual(period=201, state="VALID"),
    }
    ttm = [_ttm(0, 201), _ttm(0, 201)]
    primary = _run(records, actuals, ttm=ttm, exclude_estimated=False)
    sensitivity = _run(records, actuals, ttm=ttm, exclude_estimated=True)
    primary_v = primary.verdicts[_key()]
    sensitivity_v = sensitivity.verdicts[_key()]
    # PRIMARY: ESTIMATED scores fully; the TTM repeat quarantines wholesale.
    assert primary_v.series.observation_count == 3
    assert primary_v.series.limited_quality is True
    assert primary_v.series.quarantined == {"DUPLICATE_QUARANTINED": 2}
    assert primary_v.ttm_accounted == 1
    # SENSITIVITY: ESTIMATED quarantines under its own reason; duplicates
    # still quarantine as duplicates — neither path borrows the other's rule.
    assert sensitivity_v.series.observation_count == 2
    assert sensitivity_v.series.quarantined == {
        "SENSITIVITY_ESTIMATED_EXCLUDED": 1,
        "DUPLICATE_QUARANTINED": 2,
    }
    assert sensitivity_v.series.limited_quality is False
    assert sensitivity_v.series.mape == pytest.approx(10.0)
    # Reliability stays withheld on both paths.
    assert primary_v.governance.reliability.reliability is None
    assert sensitivity_v.governance.reliability.reliability is None


# --- P39 cutoff behaviors intact ----------------------------------------------


def test_p40_17_cutoff_rejections_still_fail_closed():
    # Missing Forecast cutoff.
    with pytest.raises(ValueError, match="missing evaluation cutoff"):
        _run(
            [_record(forecast_id=1, data_cutoff_datetime=None)],
            _actual_map([101]),
        )
    # Invalid (unparseable) cutoff string.
    with pytest.raises(ValueError):
        _run(
            [_record(forecast_id=1, data_cutoff_datetime="not-a-datetime")],
            _actual_map([101]),
        )
    # Mixed distinct cutoffs.
    with pytest.raises(ValueError, match="mixed evaluation cutoffs"):
        _run(
            [
                _record(forecast_id=1, data_cutoff_datetime=CUTOFF),
                _record(forecast_id=2, data_cutoff_datetime=CUTOFF_OTHER),
            ],
            _actual_map([101]),
        )
    # Missing TTM cutoff fails even with a valid Forecast side.
    from src.evaluation.observation import EvaluationObservation

    null_ttm = EvaluationObservation(
        forecast=_record(forecast_id=100, forecast_period_id=201,
                         data_cutoff_datetime=None),
        metric_code="REVENUE",
        actual=_actual(period=201),
    )
    with pytest.raises(ValueError, match="missing evaluation cutoff"):
        _run([_record()], _actual_map([101, 201]), ttm=[null_ttm])


def test_p40_18_ttm_only_empty_later_actual_intact():
    # TTM-only invocation still reports its cutoff.
    ttm_only = _run([], _actual_map([201]), ttm=[_ttm(0, 201)])
    assert ttm_only.artifact.evaluation_cutoff == CUTOFF
    assert ttm_only.verdicts[_key()].ttm_accounted == 1
    # Explicitly empty input still keeps None.
    empty = _run([], {})
    assert empty.artifact.evaluation_cutoff is None
    assert empty.series_count == 0
    # Later-published Actual stays an eligible outcome (Rule 10).
    assert AFTER > CUTOFF
    result = _run([_record()], _actual_map([101]))
    verdict = result.verdicts[_key()]
    assert verdict.series.observation_count == 1
    assert verdict.series.mape == pytest.approx(10.0)
    assert verdict.series.bias == pytest.approx(10.0)


def test_p40_19_rejections_return_no_partial_result():
    records = [
        _record(forecast_id=1, data_cutoff_datetime=CUTOFF),
        _record(forecast_id=2, data_cutoff_datetime=CUTOFF_OTHER),
    ]
    result = None
    with pytest.raises(ValueError, match="mixed evaluation cutoffs"):
        result = _run(records, _actual_map([101]))
    assert result is None
    clean = _run([_record()], _actual_map([101]))
    assert clean.artifact.evaluation_cutoff == CUTOFF
