"""Stage 6 Prompt 25 (Part B): L4 adversarial tests — 17 cases.

Exercises selection / eligibility / duplication through
``run_evaluation_pipeline`` (L3) where those behaviors are under test, and
through the helpers elsewhere. All expectations are explicit.
"""

from datetime import datetime, timezone

import pytest

from src.evaluation.aggregate import aggregate_observations, score_observation
from src.evaluation.observation import build_observation
from src.evaluation.pipeline import run_evaluation_pipeline
from src.evaluation.schema import ActualObservation
from src.forecast.schema import ForecastRecord

CUTOFF = datetime(2024, 6, 30, tzinfo=timezone.utc)
BEFORE = datetime(2024, 3, 31, tzinfo=timezone.utc)
AFTER = datetime(2024, 9, 30, tzinfo=timezone.utc)
EARLY = datetime(2024, 9, 30, tzinfo=timezone.utc)
MID = datetime(2024, 10, 31, tzinfo=timezone.utc)
LATE = datetime(2024, 12, 31, tzinfo=timezone.utc)
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
        publication_datetime=MID,
    )
    fields.update(overrides)
    return ActualObservation(**fields)


def _run(records, actuals):
    return run_evaluation_pipeline(
        records=records, metric_codes=["REVENUE"], actuals=actuals
    )


def _verdict(result, horizon="12M", version="V1.0"):
    return result.verdicts[(7, "REVENUE", horizon, version, "BASE")]


def _key(record):
    return (record.company_id, record.forecast_period_id, "REVENUE")


# --- (1) multi-RV, different publications: earliest wins -----------------------


def test_p25_01_multi_rv_earliest_publication_wins():
    record = _record(revenue=1000.0)
    candidates = [
        _actual(report_version_id=3, report_version_number=9,
                publication_datetime=LATE, value=9999.0),
        _actual(report_version_id=1, report_version_number=1,
                publication_datetime=EARLY, value=1100.0),
    ]
    result = _run([record], {_key(record): candidates})
    verdict = _verdict(result)
    assert verdict.series.observation_count == 1
    scored = verdict.series.observations[0]
    assert scored.error == 100.0  # the EARLY candidate's value won


# --- (2) same publication: lowest version_number wins; exact ties fail closed


def test_p25_02_same_publication_tie_break():
    record = _record(revenue=1000.0)
    high = _actual(report_version_id=99, report_version_number=2,
                   publication_datetime=MID, value=9000.0)
    low = _actual(report_version_id=7, report_version_number=1,
                  publication_datetime=MID, value=1100.0)
    result = _run([record], {_key(record): [high, low]})
    assert _verdict(result).series.observations[0].error == 100.0

    # Prompt 38 D-e / owner-approved D1: exact (publication,
    # version-number) ties fail closed — no database-ID fallback.
    record2 = _record(forecast_period_id=102)
    high_id = _actual(report_version_id=80, report_version_number=4,
                      financial_period_id=102, publication_datetime=MID,
                      value=9000.0)
    low_id = _actual(report_version_id=12, report_version_number=4,
                     financial_period_id=102, publication_datetime=MID,
                     value=1100.0)
    with pytest.raises(ValueError, match="no defensible ordering"):
        _run([record2], {_key(record2): [high_id, low_id]})


# --- (3) later restatement loses to first-known --------------------------------


def test_p25_03_restated_later_publication_loses_to_first_known():
    # A RESTATED Actual published later is hindsight, not the outcome:
    # first-known-outcome names the EARLY original as the winner.
    record = _record(revenue=1000.0)
    original = _actual(report_version_id=1, publication_datetime=EARLY,
                       value=1100.0)
    restatement = _actual(report_version_id=2, publication_datetime=LATE,
                          value=1050.0, data_quality_state="RESTATED",
                          restated=True)
    result = _run([record], {_key(record): [restatement, original]})
    assert _verdict(result).series.observations[0].error == 100.0


# --- (4) invalid version: INVALID_REPORT_VERSION, never scores -----------------


def test_p25_04_invalid_report_version_never_scores():
    record = _record()
    bad = _actual(report_version_id=None)
    observation = build_observation(record, "REVENUE", bad)
    assert observation.evaluation_status == "INVALID_REPORT_VERSION"
    assert observation.actual is bad
    scored = score_observation(observation)
    assert scored.scored is False
    assert scored.exclusion_reason == "INVALID_REPORT_VERSION"
    result = _run([record], {_key(record): bad})
    verdict = _verdict(result)
    assert verdict.series.observation_count == 0
    assert verdict.series.quarantined == {"INVALID_REPORT_VERSION": 1}


# --- (5) missing actual value --------------------------------------------------


def test_p25_05_missing_actual_value_quarantines():
    record = _record()
    missing = _actual(value=None, data_quality_state="MISSING")
    scored = score_observation(build_observation(record, "REVENUE", missing))
    assert scored.scored is False
    assert scored.exclusion_reason == "DATA_QUALITY_QUARANTINED:MISSING"


# --- (6) estimated scores + limited_quality ------------------------------------


def test_p25_06_estimated_scores_with_limited_quality():
    record = _record()
    estimated = _actual(value=1100.0, data_quality_state="ESTIMATED")
    verdict = _verdict(_run([record], {_key(record): estimated}))
    assert verdict.series.observation_count == 1
    assert verdict.series.limited_quality is True
    assert verdict.series.observations[0].data_quality_state == "ESTIMATED"
    assert verdict.series.mape == 10.0


# --- (7) suspicious quarantines -----------------------------------------------


def test_p25_07_suspicious_quarantines_verbatim():
    record = _record()
    verdict = _verdict(
        _run([record], {_key(record): _actual(data_quality_state="SUSPICIOUS")})
    )
    assert verdict.series.observation_count == 0
    assert verdict.series.quarantined == {"DATA_QUALITY_QUARANTINED:SUSPICIOUS": 1}


# --- (8) unmapped quarantines --------------------------------------------------


def test_p25_08_unmapped_quarantines_verbatim():
    record = _record()
    verdict = _verdict(
        _run([record], {_key(record): _actual(data_quality_state="UNMAPPED")})
    )
    assert verdict.series.observation_count == 0
    assert verdict.series.quarantined == {"DATA_QUALITY_QUARANTINED:UNMAPPED": 1}


# --- (9) conflicting duplicates fail closed ------------------------------------


def test_p25_09_conflicting_duplicates_fail_closed():
    first = _record(forecast_id=1, forecast_period_id=101)
    second = _record(forecast_id=2, forecast_period_id=101)
    actuals = {(7, 101, "REVENUE"): _actual()}
    verdict = _verdict(_run([first, second], actuals))
    assert verdict.series.total_observations == 2
    assert verdict.series.observation_count == 0
    assert verdict.series.quarantined == {"DUPLICATE_QUARANTINED": 2}


# --- (10-12) dup-key stays horizon/version/cutoff isolated ---------------------


def test_p25_10_dup_key_across_horizons_does_not_collide():
    one = _record(forecast_period_id=101, forecast_horizon="12M")
    two = _record(forecast_period_id=101, forecast_horizon="3M")
    actuals = {(7, 101, "REVENUE"): _actual()}
    result = _run([one, two], actuals)
    assert result.series_count == 2
    assert _verdict(result, horizon="12M").series.observation_count == 1
    assert _verdict(result, horizon="3M").series.observation_count == 1


def test_p25_11_dup_key_across_versions_does_not_collide():
    one = _record(forecast_period_id=101, model_version="V1.0")
    two = _record(forecast_period_id=101, model_version="V2.0")
    actuals = {(7, 101, "REVENUE"): _actual()}
    result = _run([one, two], actuals)
    assert result.series_count == 2
    assert _verdict(result, version="V1.0").series.observation_count == 1
    assert _verdict(result, version="V2.0").series.observation_count == 1


def test_p25_12_dup_key_across_cutoffs_does_not_collide():
    # Stage 6 Prompt 38: distinct cutoffs never reach joint scoring — the
    # pipeline fails closed. The non-collision property itself is proved
    # at the flag_duplicates level (distinct 7-tuple identity keys).
    import pytest

    from src.evaluation.observation import flag_duplicates

    one = _record(forecast_period_id=101)
    other_cutoff = datetime(2024, 5, 31, tzinfo=timezone.utc)
    two = _record(forecast_period_id=101, data_cutoff_datetime=other_cutoff)
    actuals = {(7, 101, "REVENUE"): _actual()}
    flagged = flag_duplicates(
        [
            build_observation(one, "REVENUE", _actual()),
            build_observation(two, "REVENUE", _actual()),
        ]
    )
    assert all(item.duplicate_key is None for item in flagged)
    with pytest.raises(ValueError, match="mixed evaluation cutoffs"):
        _run([one, two], actuals)


# --- (13) A=0 / F=1000: scores -------------------------------------------------


def test_p25_13_zero_actual_positive_forecast_scores():
    # Stage 6 Prompt 38 (spec §9 D4-pointer + §12 D4): A=0/F=1000 stays
    # scored with absolute error retained and the Bias term eligible, but
    # is excluded from ordinary MAPE with the dedicated ACTUAL_ZERO code.
    record = _record(revenue=1000.0)
    scored = score_observation(
        build_observation(record, "REVENUE", _actual(value=0.0))
    )
    assert scored.scored is True
    assert scored.error == -1000.0
    assert scored.percentage_error == -100.0
    assert scored.ape is None
    assert scored.mape_exclusion_reason == "ACTUAL_ZERO"


# --- (14) A=0 / F=-500: scores -------------------------------------------------


def test_p25_14_zero_actual_negative_forecast_scores():
    # Stage 6 Prompt 38 (§10 RB-2 (1)): A=0/F<0 stays Bias-eligible with
    # term exactly +100%, while MAPE-excluded with ACTUAL_ZERO.
    record = _record(revenue=-500.0)
    scored = score_observation(
        build_observation(record, "REVENUE", _actual(value=0.0))
    )
    assert scored.scored is True
    assert scored.error == 500.0
    assert scored.percentage_error == 100.0
    assert scored.ape is None
    assert scored.mape_exclusion_reason == "ACTUAL_ZERO"


# --- (15) A=0 / F=0: ZERO_BASE -------------------------------------------------


def test_p25_15_zero_over_zero_is_zero_base():
    record = _record(revenue=0.0)
    scored = score_observation(
        build_observation(record, "REVENUE", _actual(value=0.0))
    )
    assert scored.scored is False
    assert scored.regime == "ZERO_BASE"
    assert scored.error == 0.0  # absolute error kept for audit
    assert scored.percentage_error is None
    assert scored.ape is None


# --- (16) F=0 / A=500: ZERO_BASE ----------------------------------------------


def test_p25_16_zero_forecast_is_zero_base():
    record = _record(revenue=0.0)
    scored = score_observation(
        build_observation(record, "REVENUE", _actual(value=500.0))
    )
    assert scored.scored is False
    assert scored.regime == "ZERO_BASE"
    assert scored.error == 500.0
    assert scored.percentage_error is None
    assert scored.ape is None


# --- (17) F>0 / A=0 with sign context: scores, regime None ---------------------


def test_p25_17_positive_forecast_zero_actual_regime_none():
    # classify_regime requires f*a < 0 for SIGN_CHANGE; here f*a = 0, so no
    # regime fires even though a naive sign reading sees "positive to zero".
    record = _record(revenue=1000.0)
    scored = score_observation(
        build_observation(record, "REVENUE", _actual(value=0.0))
    )
    assert scored.regime is None
    assert scored.scored is True
    assert scored.error == -1000.0
    # Prompt 38: MAPE-excluded (ACTUAL_ZERO) but Bias-eligible.
    assert scored.ape is None
    assert scored.mape_exclusion_reason == "ACTUAL_ZERO"
    assert scored.percentage_error == -100.0


# --- series-level: restated participation sets limited_quality -----------------


def test_p25_restated_series_flags_limited_quality():
    observations = [
        build_observation(
            _record(forecast_period_id=101 + i),
            "REVENUE",
            _actual(financial_period_id=101 + i,
                    data_quality_state="RESTATED", restated=True),
        )
        for i in range(8)
    ]
    series = aggregate_observations(observations)[(7, "REVENUE", "12M", "V1.0", "BASE")]
    assert series.observation_count == 8
    assert series.limited_quality is True
    assert series.mape == 10.0
