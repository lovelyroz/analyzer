"""Stage 6 Prompt 39 section 6: 19-case evaluation-cutoff test matrix.

Contracts (spec sections 2-3 + Prompt 38 section 4 conservative rule):

* One artifact = one validated cutoff. Every participating Forecast record
  must carry a valid, normalized, non-null ``data_cutoff_datetime`` and every
  supplied TTM observation a valid, normalized, non-null
  ``forecast_cutoff_datetime``; all must agree after normalization.
* Missing/invalid cutoffs fail closed with ``ValueError`` (never silently
  discarded); distinct cutoffs fail closed with ``ValueError``; no partial
  successful result is ever returned on rejection.
* Empty input (no records AND no TTM) keeps ``evaluation_cutoff=None`` as
  explicitly-empty only — never fabricated.
* Normalization folds naive datetimes onto UTC and converts tz-aware instants,
  so equivalent instants compare equal. Actual publication timestamps are
  never consulted by the guard: later-published valid Actuals stay eligible
  outcomes (Rule 10).
"""
from datetime import datetime, timedelta, timezone

import pytest

from src.evaluation.observation import EvaluationObservation, build_observation
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
    # build_observation CANNOT produce a null-cutoff TTM observation: its
    # construction-time PIT check asserts a non-null cutoff before the
    # pipeline guard ever runs. Direct EvaluationObservation construction is
    # therefore the nearest public boundary — the dataclass performs no
    # cutoff validation, so the pipeline guard must still fail closed here.
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


# --- Case 1: one valid record succeeds ----------------------------------------


def test_p39_01_single_valid_cutoff_succeeds():
    result = run_evaluation_pipeline(
        [_record()], ["REVENUE"], _actual_map([101])
    )
    assert result.artifact is not None
    assert result.artifact.evaluation_cutoff == CUTOFF
    assert result.verdicts[_key()].series.observation_count == 1


# --- Case 2: multiple records sharing one cutoff succeed ---------------------


def test_p39_02_multiple_same_cutoff_succeeds():
    records = [
        _record(forecast_id=1, forecast_period_id=101),
        _record(forecast_id=2, forecast_period_id=102),
        _record(forecast_id=3, forecast_period_id=103),
    ]
    result = run_evaluation_pipeline(
        records, ["REVENUE"], _actual_map([101, 102, 103])
    )
    assert result.artifact.evaluation_cutoff == CUTOFF
    assert result.verdicts[_key()].series.observation_count == 3


# --- Case 3: tz-aware equivalents normalize equal ----------------------------


def test_p39_03_equivalent_tz_aware_cutoffs_succeed():
    plus_two = timezone(timedelta(hours=2))
    records = [
        _record(forecast_id=1, data_cutoff_datetime=CUTOFF),
        # Naive folds onto UTC: midnight naive == midnight UTC.
        _record(forecast_id=2, data_cutoff_datetime=datetime(2024, 6, 30)),
        # 02:00 at +02:00 is the same instant as midnight UTC.
        _record(
            forecast_id=3,
            data_cutoff_datetime=datetime(2024, 6, 30, 2, 0, tzinfo=plus_two),
        ),
    ]
    result = run_evaluation_pipeline(
        records, ["REVENUE"], _actual_map([101])
    )
    assert result.artifact.evaluation_cutoff == CUTOFF


# --- Case 4: distinct non-null cutoffs fail -----------------------------------


def test_p39_04_distinct_non_null_cutoffs_fail():
    records = [
        _record(forecast_id=1, data_cutoff_datetime=CUTOFF),
        _record(forecast_id=2, data_cutoff_datetime=CUTOFF_OTHER),
    ]
    with pytest.raises(ValueError, match="mixed evaluation cutoffs"):
        run_evaluation_pipeline(records, ["REVENUE"], _actual_map([101]))


# --- Case 5: valid record + missing Forecast cutoff fails --------------------


def test_p39_05_valid_plus_missing_forecast_cutoff_fails():
    records = [
        _record(forecast_id=1, data_cutoff_datetime=CUTOFF),
        _record(forecast_id=2, data_cutoff_datetime=None),
    ]
    with pytest.raises(ValueError, match="missing evaluation cutoff"):
        run_evaluation_pipeline(records, ["REVENUE"], _actual_map([101]))


# --- Case 6: all-missing non-empty input fails --------------------------------


def test_p39_06_all_missing_cutoffs_fail():
    records = [
        _record(forecast_id=1, data_cutoff_datetime=None),
        _record(forecast_id=2, data_cutoff_datetime=None),
    ]
    with pytest.raises(ValueError, match="missing evaluation cutoff"):
        run_evaluation_pipeline(records, ["REVENUE"], _actual_map([101]))
    # Nearest public boundary for "invalid": an unparseable cutoff string
    # reaches the same fail-closed ValueError via the ISO parser (a non-empty
    # invalid value is never silently treated as missing or skipped).
    bad = [_record(forecast_id=1, data_cutoff_datetime="not-a-datetime")]
    with pytest.raises(ValueError):
        run_evaluation_pipeline(bad, ["REVENUE"], _actual_map([101]))


# --- Case 7: valid Forecast + missing TTM cutoff fails ------------------------


def test_p39_07_valid_forecast_plus_missing_ttm_cutoff_fails():
    with pytest.raises(ValueError, match="missing evaluation cutoff"):
        run_evaluation_pipeline(
            [_record()],
            ["REVENUE"],
            _actual_map([101, 201]),
            ttm_observations=[_ttm_null_cutoff(0, 201)],
        )


# --- Case 8: distinct Forecast/TTM cutoffs fail -------------------------------


def test_p39_08_distinct_forecast_ttm_cutoffs_fail():
    with pytest.raises(ValueError, match="mixed evaluation cutoffs"):
        run_evaluation_pipeline(
            [_record()],
            ["REVENUE"],
            _actual_map([101, 201]),
            ttm_observations=[_ttm(0, 201, cutoff=CUTOFF_OTHER)],
        )


# --- Case 9: matching Forecast + TTM succeeds with correct cutoff -------------


def test_p39_09_matching_forecast_ttm_succeeds_correct_cutoff():
    result = run_evaluation_pipeline(
        [_record(forecast_period_id=101)],
        ["REVENUE"],
        _actual_map([101, 201]),
        ttm_observations=[_ttm(0, 201)],
    )
    assert result.artifact.evaluation_cutoff == CUTOFF
    verdict = result.verdicts[_key()]
    assert verdict.ttm_accounted == 1
    assert verdict.series.total_observations == 2


# --- Case 10: TTM-only valid invocation reports its cutoff --------------------


def test_p39_10_ttm_only_valid_reports_cutoff():
    result = run_evaluation_pipeline(
        [],
        ["REVENUE"],
        _actual_map([201]),
        ttm_observations=[_ttm(0, 201)],
    )
    assert result.artifact is not None
    assert result.artifact.evaluation_cutoff == CUTOFF
    verdict = result.verdicts[_key()]
    assert verdict.ttm_accounted == 1


# --- Case 11: TTM-only missing cutoff fails -----------------------------------


def test_p39_11_ttm_only_missing_cutoff_fails():
    with pytest.raises(ValueError, match="missing evaluation cutoff"):
        run_evaluation_pipeline(
            [],
            ["REVENUE"],
            _actual_map([201]),
            ttm_observations=[_ttm_null_cutoff(0, 201)],
        )


# --- Case 12: explicitly empty input keeps None -------------------------------


def test_p39_12_explicitly_empty_keeps_none_cutoff():
    result = run_evaluation_pipeline([], ["REVENUE"], {})
    assert result.artifact is not None
    assert result.artifact.evaluation_cutoff is None
    assert result.series_count == 0


# --- Case 13: rejection returns no partial successful result ------------------


def test_p39_13_rejected_invocation_returns_no_partial_result():
    records = [
        _record(forecast_id=1, data_cutoff_datetime=CUTOFF),
        _record(forecast_id=2, data_cutoff_datetime=CUTOFF_OTHER),
    ]
    result = None
    with pytest.raises(ValueError, match="mixed evaluation cutoffs"):
        result = run_evaluation_pipeline(
            records, ["REVENUE"], _actual_map([101])
        )
    assert result is None
    # No corrupted global state: a later valid invocation still succeeds.
    clean = run_evaluation_pipeline([_record()], ["REVENUE"], _actual_map([101]))
    assert clean.artifact.evaluation_cutoff == CUTOFF


# --- Case 14: reordered/interleaved inputs decide identically ------------------


def test_p39_14_reordered_interleaved_inputs_same_decision():
    first = _record(forecast_id=1, forecast_period_id=101)
    second = _record(forecast_id=2, forecast_period_id=102)
    actuals = _actual_map([101, 102])
    forward = run_evaluation_pipeline([first, second], ["REVENUE"], actuals)
    backward = run_evaluation_pipeline([second, first], ["REVENUE"], actuals)
    assert forward.artifact.evaluation_cutoff == CUTOFF
    assert backward.artifact.evaluation_cutoff == CUTOFF
    assert set(forward.verdicts) == set(backward.verdicts)
    # Failure is order-invariant too: the mixed set fails either way round.
    other = _record(
        forecast_id=3, forecast_period_id=103, data_cutoff_datetime=CUTOFF_OTHER
    )
    with pytest.raises(ValueError, match="mixed evaluation cutoffs"):
        run_evaluation_pipeline([first, other], ["REVENUE"], _actual_map([101, 103]))
    with pytest.raises(ValueError, match="mixed evaluation cutoffs"):
        run_evaluation_pipeline([other, first], ["REVENUE"], _actual_map([101, 103]))


# --- Case 15: Bear/Base/Bull share one cutoff, stay separate ------------------


def test_p39_15_three_scenarios_one_cutoff_stay_separate():
    records = [
        _record(forecast_id=index + 1, scenario=scenario)
        for index, scenario in enumerate(("BEAR", "BASE", "BULL"))
    ]
    result = run_evaluation_pipeline(records, ["REVENUE"], _actual_map([101]))
    assert result.artifact.evaluation_cutoff == CUTOFF
    assert len(result.verdicts) == 3
    for scenario in ("BEAR", "BASE", "BULL"):
        verdict = result.verdicts[_key(scenario=scenario)]
        assert verdict.series.scenario == scenario
        assert verdict.series.observation_count == 1


# --- Case 16: multi-scenario mixed cutoffs fail closed, no partial ------------


def test_p39_16_multi_scenario_mixed_fails_closed_no_partial():
    records = [
        _record(forecast_id=1, scenario="BASE", data_cutoff_datetime=CUTOFF),
        _record(forecast_id=2, scenario="BULL", data_cutoff_datetime=CUTOFF_OTHER),
    ]
    result = None
    with pytest.raises(ValueError, match="mixed evaluation cutoffs"):
        result = run_evaluation_pipeline(
            records, ["REVENUE"], _actual_map([101])
        )
    assert result is None


# --- Case 17: later-published Actual stays eligible ----------------------------


def test_p39_17_later_published_actual_stays_eligible():
    # The Actual is published AFTER the forecast cutoff: it is the outcome
    # being evaluated (Rule 10), never PIT leakage — inputs are checked, the
    # outcome Actual is not.
    assert AFTER > CUTOFF
    result = run_evaluation_pipeline(
        [_record()], ["REVENUE"], _actual_map([101])
    )
    verdict = result.verdicts[_key()]
    assert verdict.series.observation_count == 1
    assert verdict.series.mape == pytest.approx(10.0)
    assert verdict.series.bias == pytest.approx(10.0)


# --- Case 18: provenance / purpose / supersession unchanged --------------------


def test_p39_18_provenance_purpose_supersession_unchanged():
    result = run_evaluation_pipeline(
        [_record()], ["REVENUE"], _actual_map([101]), supersedes="run-001"
    )
    artifact = result.artifact
    assert artifact is not None
    assert artifact.purpose == "PRIMARY"
    assert artifact.supersedes == "run-001"
    assert artifact.evaluation_cutoff == CUTOFF
    assert len(artifact.series_provenance) == 1
    provenance = artifact.series_provenance[0]
    assert provenance.report_version_ids == (55,)
    assert tuple(provenance.publication_datetimes) == (AFTER,)
    assert set(provenance.data_quality_states) == {"VALID"}


# --- Case 19: TTM conservation + duplicates intact ------------------------------


def test_p39_19_ttm_conservation_and_duplicates_intact():
    periods = [101, 102, 103]
    records = [
        _record(forecast_id=index + 1, forecast_period_id=period)
        for index, period in enumerate(periods)
    ]
    supplied = [_ttm(index, 201 + index) for index in range(2)]
    result = run_evaluation_pipeline(
        records,
        ["REVENUE"],
        _actual_map(periods + [201, 202]),
        ttm_observations=supplied,
    )
    verdict = result.verdicts[_key()]
    # Conservation: every supplied TTM scored exactly once, none dropped.
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
    # Duplicates pass through intact: the same TTM observation supplied twice
    # is conserved (counted twice), never silently deduped or dropped.
    doubled = run_evaluation_pipeline(
        records,
        ["REVENUE"],
        _actual_map(periods + [201]),
        ttm_observations=[_ttm(0, 201), _ttm(0, 201)],
    )
    doubled_verdict = doubled.verdicts[_key()]
    assert doubled_verdict.ttm_accounted == 2
    assert doubled_verdict.series.total_observations == 5
