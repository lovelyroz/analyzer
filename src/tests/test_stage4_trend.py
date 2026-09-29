from src.trend.utils import (
    DIRECTION_THRESHOLD,
    calculate_pct_change,
    classify_direction,
    detect_one_off,
    determine_trend_state,
    flow_momentum,
    historical_percentile_abs,
    is_low_base,
    is_sign_change,
    is_zero_base,
    momentum_history,
    multi_year_trend,
    period_comparison,
    relative_strength,
    same_period_multi_year,
    seasonal_baseline,
    seasonal_surprise,
    sign_change_kind,
    stock_momentum,
    trend_12m,
)
from src.trend.engine import TrendEngine
from src.trend.schema import TrendResult


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

def pytest_approx(value, tol=1e-9):
    class _Approx:
        def __eq__(self, other):
            return abs(other - value) <= tol
        def __repr__(self):
            return f"~{value}"
    return _Approx()


def _run(**kwargs):
    """Run the engine with every explicit-horizon default filled in."""
    engine = TrendEngine()
    defaults = dict(
        company_id=1,
        period_id=10,
        metric_code="REVENUE",
        val_3m_curr=110.0, val_3m_prev=100.0,
        val_6m_curr=220.0, val_6m_prev=200.0,
        val_12m_curr=440.0, val_12m_prev=400.0,
        historical_3m=None, historical_6m=None, historical_12m=None,
    )
    defaults.update(kwargs)
    return engine.evaluate_trend(**defaults)


# --------------------------------------------------------------------------
# 1-3. Seasonal baseline, median behaviour and surprise
# --------------------------------------------------------------------------

def test_seasonal_baseline_uses_median_of_same_period():
    assert seasonal_baseline([90.0, 100.0, 500.0]) == 100.0


def test_seasonal_baseline_median_robust_to_outlier():
    # The mean would be pulled up to 226.7; the median stays at 110.
    assert seasonal_baseline([100.0, 110.0, 470.0]) == 110.0


def test_seasonal_baseline_orders_unsorted_input():
    assert seasonal_baseline([500.0, 90.0, 100.0]) == 100.0


def test_seasonal_surprise_uses_median_baseline():
    baseline = seasonal_baseline([90.0, 100.0, 110.0])
    surprise, flag = seasonal_surprise(120.0, baseline)
    assert baseline == 100.0
    assert surprise == 20.0
    assert flag is None


def test_seasonal_surprise_negative_baseline_same_sign():
    # Same-sign negatives: a real decline, not a misleading positive growth.
    baseline = seasonal_baseline([-90.0, -100.0, -110.0])
    assert baseline == -100.0
    surprise, flag = seasonal_surprise(-120.0, baseline)
    assert surprise == pytest_approx(-20.0)
    assert flag is None


def test_seasonal_surprise_below_baseline_is_negative():
    baseline = seasonal_baseline([90.0, 100.0, 110.0])
    surprise, flag = seasonal_surprise(80.0, baseline)
    assert surprise == pytest_approx(-20.0)
    assert flag is None


def test_seasonal_baseline_zero_median_is_null_with_zero_base_flag():
    # Median of [0, 0, 10] is 0: the baseline is unusable, surprise is NULL
    # and a ZERO_BASE flag is emitted rather than a fabricated percentage.
    baseline = seasonal_baseline([0.0, 0.0, 10.0])
    assert baseline == 0.0
    surprise, flag = seasonal_surprise(120.0, baseline)
    assert surprise is None
    assert flag == "ZERO_BASE"


def test_seasonal_baseline_sign_incompatible_emits_sign_change():
    # Positive current against a negative baseline: no percentage, SIGN_CHANGE.
    surprise, flag = seasonal_surprise(120.0, -100.0)
    assert surprise is None
    assert flag == "SIGN_CHANGE"

    # Negative current against a positive baseline.
    surprise, flag = seasonal_surprise(-50.0, 100.0)
    assert surprise is None
    assert flag == "SIGN_CHANGE"


def test_seasonal_baseline_ignores_missing_observations():
    # MISSING != 0: None entries are dropped, not counted as zeros.
    assert seasonal_baseline([None, 100.0, 110.0, 120.0]) == 110.0
    # Two real observations after dropping None is still insufficient.
    assert seasonal_baseline([None, 100.0, 110.0]) is None


def test_seasonal_baseline_deterministic_across_runs():
    history = [90.0, 500.0, 100.0, 110.0, 470.0]
    first = seasonal_baseline(history)
    for _ in range(5):
        assert seasonal_baseline(history) == first
    # Order of the observations must not change the median.
    assert seasonal_baseline(history) == seasonal_baseline(list(reversed(history)))


def test_seasonal_engine_reconstructs_baseline_from_series():
    # Quarterly series; the same period is 4 observations back per year.
    # current = 200; same-period history = [80, 40] -> fewer than 3 -> insufficient.
    series = [10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 200.0]
    res = _run(flow_series=series)
    assert res.seasonal.data_sufficiency == "INSUFFICIENT_DATA"
    assert res.seasonal.baseline is None


# --------------------------------------------------------------------------
# 4. Seasonal insufficient-data behaviour
# --------------------------------------------------------------------------

def test_seasonal_insufficient_when_fewer_than_three_observations():
    assert seasonal_baseline([100.0, 110.0]) is None
    assert seasonal_baseline([]) is None
    assert seasonal_baseline(None) is None


def test_seasonal_engine_reports_insufficient_data():
    res = _run(same_period_history=[120.0, 110.0])
    assert res.seasonal.data_sufficiency == "INSUFFICIENT_DATA"
    assert res.seasonal.baseline is None
    assert res.seasonal.surprise is None
    assert res.seasonal.observation_count == 1
    # Insufficient seasonal data does not block the other analyses: the trend
    # state is still derived from the valid momentum horizons.
    assert res.trend_state in ("Improving", "Strong Improvement")
    assert res.coverage == "FULL"


def test_seasonal_engine_full_when_three_or_more_observations():
    res = _run(same_period_history=[120.0, 100.0, 110.0, 105.0])
    assert res.seasonal.data_sufficiency == "FULL"
    # 105 is the current period; the baseline is the median of [120, 100, 110].
    assert res.seasonal.baseline == 110.0
    assert res.seasonal.observation_count == 3


def test_seasonal_zero_base_baseline_is_null_with_flag():
    # The specification nulls the surprise only when the *baseline itself* is
    # zero. A zero merely appearing in the history does not: the median of
    # [0, 100, 110] is 100, so the baseline stays usable.
    res = _run(same_period_history=[0.0, 100.0, 110.0, 105.0])
    assert res.seasonal.baseline == 100.0
    assert res.seasonal.data_sufficiency == "FULL"
    assert res.seasonal.flag is None

    # Here the median really is zero. Three valid observations exist, so
    # sufficiency stays FULL; it is the *surprise* that becomes NULL, with a
    # ZERO_BASE flag, and no percentage is fabricated.
    res = _run(same_period_history=[0.0, 0.0, 10.0, 105.0])
    assert res.seasonal.baseline == 0.0
    assert res.seasonal.surprise is None
    assert res.seasonal.data_sufficiency == "FULL"
    assert res.seasonal.flag == "ZERO_BASE"
    assert res.context.zero_base is True


# --------------------------------------------------------------------------
# 5-7. MoM, QoQ, YoY
# --------------------------------------------------------------------------

def test_mom_via_engine():
    res = _run(val_mom=(150.0, 100.0))
    assert res.historical.mom == 50.0
    assert res.historical.qoq is None
    assert res.historical.yoy is None


def test_qoq_via_engine():
    res = _run(val_qoq=(90.0, 200.0))
    assert res.historical.qoq == -55.0


def test_yoy_via_engine():
    res = _run(val_yoy=(120.0, 100.0))
    assert res.historical.yoy == 20.0


def test_mom_missing_observations_stay_null():
    # A missing base observation produces no percentage: MISSING != 0.
    res = _run(val_mom=(150.0, None))
    assert res.historical.mom is None
    # The 3M/6M/12M horizons still resolved, but no supporting history was
    # supplied alongside them, so the run is flagged INSUFFICIENT_HISTORY.
    assert res.context.data_quality == "INSUFFICIENT_HISTORY"


# --------------------------------------------------------------------------
# 8. Same-period multi-year
# --------------------------------------------------------------------------

def test_same_period_multi_year_reports_each_year():
    rows = same_period_multi_year(130.0, [100.0, 110.0, 120.0])
    assert [r[0] for r in rows] == [1.0, 2.0, 3.0]
    assert rows[0][1] == 30.0
    assert rows[1][1] == pytest_approx(18.18181818181818)
    assert rows[2][1] == pytest_approx(8.333333333333334)


def test_same_period_multi_year_via_engine():
    res = _run(same_period_history=[100.0, 110.0, 120.0, 130.0])
    labels = [d.label for d in res.historical.same_period_detail]
    assert labels == ["Y-1", "Y-2", "Y-3"]
    # 130 vs 120 = +8.33...
    assert res.historical.same_period_latest == pytest_approx(8.333333333333334)
    assert res.historical.same_period_average is not None
    assert res.historical.same_period_average > 8.0


def test_same_period_multi_year_zero_base_flagged():
    rows = same_period_multi_year(130.0, [0.0, 110.0])
    assert rows[0][1] is None
    assert rows[0][2] == "ZERO_BASE"
    assert rows[1][1] == pytest_approx(18.18181818181818)


# --------------------------------------------------------------------------
# 8b. Calendar-aligned comparisons derived from the series (MoM / QoQ / YoY)
# --------------------------------------------------------------------------

def test_period_comparison_quarterly_series_yoy():
    # Quarterly series: YoY is the observation 4 periods back.
    series = [100.0, 110.0, 120.0, 130.0, 156.0]
    # 156 vs 100 (4 periods earlier) = +56%.
    assert period_comparison(series, 12, 3) == pytest_approx(56.0)


def test_period_comparison_monthly_series_mom_and_qoq():
    # Monthly granularity: MoM = 1 period back, QoQ = 3 periods back.
    series = [10.0, 11.0, 12.0, 13.0, 14.0]
    assert period_comparison(series, 1, 1) == pytest_approx(7.6923076923076925)
    assert period_comparison(series, 3, 1) == pytest_approx(27.27272727272727)


def test_period_comparison_with_explicit_position():
    # position indexes the observation *after* the evaluation point, and
    # anything after it is ignored (no look-ahead).
    series = [100.0, 110.0, 120.0, 130.0, 999.0]
    # position=4 -> current is index 3 (130); 3 monthly periods back is 100.
    assert period_comparison(series, 3, 1, position=4) == 30.0


def test_period_comparison_lag_before_series_start_is_none():
    # There is no observation 12 months before the only quarter on record.
    assert period_comparison([100.0], 12, 3) is None
    assert period_comparison([100.0, 110.0], 12, 3) is None


def test_period_comparison_missing_observation_is_not_zero():
    assert period_comparison([None, 110.0], 1, 1) is None
    assert period_comparison([100.0, None], 1, 1) is None


def test_period_comparison_zero_base_is_not_fabricated():
    # A zero BASE (prior period) yields no percentage.
    assert period_comparison([0.0, 110.0], 1, 1) is None
    # A zero CURRENT value against a real base is a genuine -100%, not NULL.
    assert period_comparison([100.0, 0.0], 1, 1) == -100.0


def test_period_comparison_sign_change_is_not_misleading():
    # -100 -> +120 must not surface as a growth percentage.
    assert period_comparison([-100.0, 120.0], 1, 1) is None


def test_period_comparison_same_sign_negative_is_a_real_decline():
    # -100 -> -120 (chronological order) is a 20% deterioration.
    assert period_comparison([-100.0, -120.0], 1, 1) == pytest_approx(-20.0)


def test_engine_derives_yoy_from_quarterly_flow_series():
    series = [100.0, 110.0, 120.0, 130.0, 156.0, 166.0, 176.0, 186.0]
    res = _run(flow_series=series)
    # No explicit val_yoy pair, so YoY comes from the series: 186 vs 130.
    assert res.historical.yoy == pytest_approx(43.07692307692308)
    assert res.historical.period_months == 3


def test_engine_derives_mom_from_monthly_series():
    series = [100.0, 105.0, 110.0, 115.0, 120.0, 125.0]
    res = _run(flow_series=series, period_months=1)
    # MoM = 125 vs 120.
    assert res.historical.mom == pytest_approx(4.166666666666667)
    # QoQ on a monthly series = 3 periods back: 125 vs 110.
    assert res.historical.qoq == pytest_approx(13.636363636363635)
    assert res.historical.period_months == 1


def test_engine_explicit_pair_wins_over_series_derivation():
    # An explicit val_yoy overrides whatever the series would imply.
    res = _run(flow_series=[100.0, 110.0, 120.0], val_yoy=(120.0, 100.0))
    assert res.historical.yoy == 20.0


def test_engine_historical_sufficiency_states():
    # All three calendar comparisons resolve from a long enough series.
    res = _run(flow_series=[100.0, 110.0, 120.0, 130.0, 156.0, 166.0])
    assert res.historical.sufficiency == "FULL"

    # A short series: YoY cannot resolve (4-period lag), so sufficiency drops
    # to LIMITED. On a quarterly series the 1-month MoM and 3-month QoQ lags
    # both collapse to a single period, so both read the same 10%.
    res = _run(flow_series=[100.0, 110.0])
    assert res.historical.mom == 10.0
    assert res.historical.qoq == 10.0
    assert res.historical.yoy is None
    assert res.historical.sufficiency == "LIMITED"

    # Nothing to compare against at all.
    res = _run(flow_series=[100.0])
    assert res.historical.sufficiency == "INSUFFICIENT"


def test_engine_historical_sufficiency_reports_missing_as_insufficient():
    # Missing inputs and no series means no calendar comparison is possible.
    res = _run(val_3m_curr=None, val_3m_prev=None)
    assert res.historical.sufficiency == "INSUFFICIENT"


# --------------------------------------------------------------------------
# 9. Multi-year trend
# --------------------------------------------------------------------------

def test_multi_year_trend_between_earliest_and_latest_annual():
    assert multi_year_trend([100.0, 130.0, 169.0]) == 69.0


def test_multi_year_trend_requires_two_annual_observations():
    assert multi_year_trend([100.0]) is None
    assert multi_year_trend(None) is None


def test_multi_year_trend_via_engine():
    res = _run(annual_history=[100.0, 130.0, 169.0])
    assert res.historical.multi_year_trend == 69.0


# --------------------------------------------------------------------------
# 10. Zero-base handling
# --------------------------------------------------------------------------

def test_zero_base_handling():
    assert calculate_pct_change(100.0, 0.0) is None
    assert is_zero_base(100.0, 0.0) is True
    assert is_zero_base(100.0, 50.0) is False


def test_engine_emits_zero_base_context():
    res = _run(val_3m_curr=100.0, val_3m_prev=0.0)
    assert res.momentum["3M"].pct_change is None
    assert res.context.zero_base is True
    # A zero base must never be turned into a fabricated 0% change.
    assert res.comparisons["3M"].status == "MISSING"


# --------------------------------------------------------------------------
# 11. Sign-change handling
# --------------------------------------------------------------------------

def test_sign_change_handling():
    # -100 -> +120 must not be shown as a misleading percentage growth.
    assert calculate_pct_change(120.0, -100.0) is None
    assert calculate_pct_change(-50.0, 100.0) is None
    assert sign_change_kind(120.0, -100.0) == "LOSS_TO_PROFIT"
    assert sign_change_kind(-50.0, 100.0) == "PROFIT_TO_LOSS"
    assert is_sign_change(-10.0, 50.0) is True


def test_engine_emits_loss_to_profit_and_profit_to_loss():
    res = _run(val_3m_curr=120.0, val_3m_prev=-100.0)
    assert res.momentum["3M"].pct_change is None
    assert res.context.sign_change == "LOSS_TO_PROFIT"
    assert res.sign_change_flag is True

    res = _run(val_3m_curr=-50.0, val_3m_prev=100.0)
    assert res.context.sign_change == "PROFIT_TO_LOSS"


def test_same_sign_negative_growth_is_a_real_decline():
    # -120 vs -100 is a 20% deterioration, not a 20% gain.
    assert calculate_pct_change(-120.0, -100.0) == -20.0


# --------------------------------------------------------------------------
# 12. Relative strength minimum 8 observations
# --------------------------------------------------------------------------

def test_relative_strength_requires_eight_observations():
    assert historical_percentile_abs(10.0, [1, 2, 3, 4, 5, 6, 7]) is None
    assert historical_percentile_abs(10.0, [1, 2, 3, 4, 5, 6, 7, 8]) == 100.0


def test_relative_strength_bands():
    # Top of a 10-observation history -> Strong (percentile 100).
    assert relative_strength(10.0, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) == "Strong"
    # 6/10 -> 60th percentile -> Normal.
    assert relative_strength(6.0, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) == "Normal"
    # 1/10 -> 10th percentile -> Weak.
    assert relative_strength(1.0, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) == "Weak"


def test_relative_strength_is_company_relative_not_global():
    # The same absolute momentum is read against each company's own history.
    # A 2.5% reading is small for the volatile company but huge for the stable
    # one - no fixed global threshold could tell them apart.
    volatile = [2, 20, 3, 30, 4, 40, 5, 50]
    stable = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7]
    assert relative_strength(2.5, volatile) == "Weak"
    assert relative_strength(2.5, stable) == "Strong"


def test_engine_exposes_per_horizon_relative_strength():
    res = _run(historical_3m=[1, 2, 3, 4, 5, 6, 7, 8])
    assert res.momentum["3M"].relative_strength == "Strong"
    assert res.momentum["3M"].percentile == 100.0
    assert res.momentum["3M"].direction == "Positive"


def test_relative_strength_not_formal_below_eight_history_observations():
    res = _run(historical_3m=[1, 2, 3, 4, 5, 6, 7])
    assert res.momentum["3M"].relative_strength is None
    assert res.momentum["3M"].percentile is None
    # The trend state is still derived from direction alone; without formal
    # strength it resolves to Improving, not Strong Improvement (section 13).
    assert res.trend_state == "Improving"


# --------------------------------------------------------------------------
# 13. Trend direction exposure
# --------------------------------------------------------------------------

def test_classify_direction_uses_threshold_only_for_direction():
    assert classify_direction(5.0) == "Positive"
    assert classify_direction(-5.0) == "Negative"
    assert classify_direction(1.0) == "Weak"
    assert classify_direction(None) is None
    # The threshold is a direction threshold, not a Strong-Trend threshold.
    assert DIRECTION_THRESHOLD == 2.0


def test_engine_exposes_per_horizon_direction():
    res = _run(
        val_3m_curr=110.0, val_3m_prev=100.0,
        val_6m_curr=190.0, val_6m_prev=200.0,
        val_12m_curr=440.0, val_12m_prev=400.0,
    )
    assert res.momentum["3M"].direction == "Positive"
    assert res.momentum["6M"].direction == "Negative"
    assert res.momentum["12M"].direction == "Positive"


def test_missing_horizon_reports_missing_direction():
    res = _run(val_3m_curr=None, val_3m_prev=100.0)
    assert res.momentum["3M"].direction is None
    assert res.momentum["3M"].status == "MISSING"


# --------------------------------------------------------------------------
# 14. Trend state rules (specification section 13 + section 15 scenarios)
# --------------------------------------------------------------------------

def test_trend_state_strong_improvement_requires_two_strong_and_all_positive():
    state, n = determine_trend_state(
        {"3M": "Positive", "6M": "Positive", "12M": "Positive"},
        {"3M": "Strong", "6M": "Strong", "12M": "Normal"},
    )
    assert state == "Strong Improvement"
    assert n == 3


def test_trend_state_strong_without_strength_is_improving():
    state, _ = determine_trend_state(
        {"3M": "Positive", "6M": "Positive", "12M": "Positive"},
        {"3M": "Normal", "6M": "Normal", "12M": "Normal"},
    )
    assert state == "Improving"


def test_trend_state_stable_when_all_weak():
    state, _ = determine_trend_state(
        {"3M": "Weak", "6M": "Weak", "12M": "Weak"},
        {"3M": "Weak", "6M": "Weak", "12M": "Weak"},
    )
    assert state == "Stable"


def test_trend_state_stable_when_no_majority_direction():
    state, _ = determine_trend_state(
        {"3M": "Positive", "6M": "Negative", "12M": "Weak"},
        {"3M": "Normal", "6M": "Normal", "12M": "Weak"},
    )
    assert state == "Stable"


def test_trend_state_deteriorating_and_strong_deterioration():
    state, _ = determine_trend_state(
        {"3M": "Negative", "6M": "Negative", "12M": "Positive"},
        {"3M": "Strong", "6M": "Strong", "12M": "Normal"},
    )
    assert state == "Deteriorating"

    state, _ = determine_trend_state(
        {"3M": "Negative", "6M": "Negative", "12M": "Negative"},
        {"3M": "Strong", "6M": "Strong", "12M": "Normal"},
    )
    assert state == "Strong Deterioration"


def test_trend_state_mixed_is_improving_not_strong():
    # Scenario 6: 3M +15% Strong, 6M -5% Normal, 12M +8% Strong.
    state, _ = determine_trend_state(
        {"3M": "Positive", "6M": "Negative", "12M": "Positive"},
        {"3M": "Strong", "6M": "Normal", "12M": "Strong"},
    )
    assert state == "Improving"


# --------------------------------------------------------------------------
# 15-17. One / two / three valid horizons
# --------------------------------------------------------------------------

def test_one_valid_horizon_is_insufficient():
    state, n = determine_trend_state({"3M": "Positive"}, {"3M": "Strong"})
    assert state == "INSUFFICIENT_DATA"
    assert n == 1


def test_two_valid_horizons_allowed_but_limited():
    state, n = determine_trend_state(
        {"3M": "Positive", "6M": "Positive"},
        {"3M": "Strong", "6M": "Strong"},
    )
    assert state == "Improving"
    assert n == 2


def test_three_horizons_complete():
    res = _run()
    # _run() supplies no relative-strength history, so no horizon can be
    # Strong and section 13's ">= 2 Strong" condition cannot be met: the
    # correct state for three positive horizons is Improving.
    assert res.trend_state == "Improving"
    assert res.coverage == "FULL"
    assert res.trend_coverage == "FULL"
    assert res.trend_confidence == "HIGH"
    for horizon in ("3M", "6M", "12M"):
        assert res.momentum[horizon].direction == "Positive"


def test_two_horizon_engine_run_reports_limited():
    res = _run(val_12m_curr=None, val_12m_prev=400.0)
    assert res.trend_state == "Improving"
    assert res.coverage == "LIMITED"
    assert res.trend_coverage == "LIMITED"
    assert res.trend_confidence == "MEDIUM"


def test_one_horizon_engine_run_reports_insufficient():
    res = _run(val_6m_curr=None, val_6m_prev=200.0, val_12m_curr=None, val_12m_prev=400.0)
    assert res.trend_state == "INSUFFICIENT_DATA"
    assert res.coverage == "INSUFFICIENT"
    assert res.trend_confidence == "LOW"


# --------------------------------------------------------------------------
# 18. Low-base robust-Z behaviour
# --------------------------------------------------------------------------

def test_low_base_requires_three_history_values_and_uses_robust_z():
    assert is_low_base(0.5, [10.0, 11.0, 12.0]) is True
    assert is_low_base(10.0, [10.0, 11.0]) is None
    assert is_low_base(10.0, None) is None
    assert is_low_base(None, [10.0, 11.0, 12.0]) is None


def test_low_base_unknown_below_three_observations_is_not_false():
    # Specification: insufficient evidence means UNKNOWN, not False.
    assert is_low_base(0.001, [1.0, 2.0]) is None


def test_low_base_preserves_growth_without_scoring_it():
    # 100 -> 500 = +400% is preserved; LOW_BASE only annotates it.
    res = _run(
        val_3m_curr=500.0, val_3m_prev=100.0,
        historical_low_base_values=[1000.0, 1100.0, 1200.0],
    )
    assert res.momentum["3M"].pct_change == 400.0
    assert res.context.low_base is True
    # No score exists anywhere in the Stage 4 result.
    assert not hasattr(res, "score")


def test_low_base_false_when_base_is_normal():
    res = _run(historical_low_base_values=[100.0, 110.0, 120.0])
    assert res.context.low_base is False
    assert res.low_base_flag is False


def test_engine_low_base_unknown_without_history():
    res = _run()
    assert res.context.low_base is None
    assert res.low_base_flag is None


# --------------------------------------------------------------------------
# 19. Determinism
# --------------------------------------------------------------------------

def test_engine_is_deterministic():
    engine = TrendEngine()
    args = dict(
        company_id=1, period_id=10, metric_code="REVENUE",
        val_3m_curr=115.0, val_3m_prev=100.0,
        val_6m_curr=222.0, val_6m_prev=200.0,
        val_12m_curr=436.0, val_12m_prev=400.0,
        historical_3m=[1, 2, 3, 4, 5, 6, 7, 8],
        historical_6m=[1, 2, 3, 4, 5, 6, 7, 8],
        historical_12m=[1, 2, 3, 4, 5, 6, 7, 8],
        same_period_history=[90.0, 100.0, 110.0, 120.0],
        seasonal_history=[80.0, 90.0, 100.0, 110.0],
        annual_history=[100.0, 130.0, 169.0],
    )
    first = engine.evaluate_trend(**args)
    second = engine.evaluate_trend(**args)

    def _snapshot(result: TrendResult):
        return (
            result.trend_state,
            result.coverage,
            result.low_base_flag,
            result.sign_change_flag,
            {h: (c.pct_change, c.status) for h, c in result.comparisons.items()},
            (
                result.historical.mom,
                result.historical.qoq,
                result.historical.yoy,
                result.historical.same_period_latest,
                result.historical.same_period_average,
                result.historical.multi_year_trend,
                [d.label for d in result.historical.same_period_detail],
            ),
            (
                result.seasonal.baseline,
                result.seasonal.surprise,
                result.seasonal.data_sufficiency,
                result.seasonal.observation_count,
                result.seasonal.flag,
            ),
            {
                h: (m.pct_change, m.direction, m.relative_strength, m.percentile, m.status)
                for h, m in result.momentum.items()
            },
            (
                result.context.low_base,
                result.context.sign_change,
                result.context.zero_base,
                result.context.one_off,
                result.context.one_off_reason,
                result.context.data_quality,
                result.context.data_sufficiency,
            ),
            result.trend_coverage,
            result.trend_confidence,
        )

    # The timestamp is deliberately excluded: it is an audit field, and the
    # analytical values must reproduce bit-for-bit across repeated runs.
    assert _snapshot(first) == _snapshot(second)


def test_engine_has_no_randomness_or_clock_dependency(monkeypatch):
    # Neutralising the clock must not change any analytical value.
    import datetime as _datetime

    frozen = _datetime.datetime(2026, 1, 1, 12, 0, 0)
    monkeypatch.setattr(_datetime, "utcnow", lambda: frozen)
    res = _run(val_3m_curr=115.0, val_3m_prev=100.0)
    assert res.calculation_timestamp == frozen
    assert res.trend_state == "Improving"


def test_utils_are_deterministic_across_input_ordering():
    # Unordered input histories must yield identical percentiles: the rank
    # of an absolute momentum within a set is order-independent.
    a = historical_percentile_abs(5.0, [1, 2, 3, 4, 5, 6, 7, 8])
    b = historical_percentile_abs(5.0, [8, 7, 6, 5, 4, 3, 2, 1])
    assert a == b == 62.5


# --------------------------------------------------------------------------
# 20. Section 19 output-contract completeness
# --------------------------------------------------------------------------

REQUIRED_HISTORICAL = ["mom", "qoq", "yoy", "same_period_detail", "multi_year_trend"]
REQUIRED_SEASONAL = ["baseline", "surprise", "data_sufficiency"]
REQUIRED_MOMENTUM = ["pct_change", "direction", "relative_strength"]
# Tri-state outputs: a None here is the spec's explicit UNKNOWN / "no event"
# state, not an absent field, so presence is checked by attribute existence.
REQUIRED_CONTEXT = [
    "low_base", "sign_change", "zero_base", "one_off",
    "data_quality", "data_sufficiency",
]


def test_output_contract_full_run():
    res = _run(
        val_mom=(115.0, 100.0),
        val_qoq=(222.0, 200.0),
        val_yoy=(436.0, 400.0),
        same_period_history=[90.0, 100.0, 110.0, 120.0],
        seasonal_history=[80.0, 90.0, 100.0, 110.0],
        annual_history=[100.0, 130.0, 169.0],
        historical_3m=[1, 2, 3, 4, 5, 6, 7, 8],
        historical_6m=[1, 2, 3, 4, 5, 6, 7, 8],
        historical_12m=[1, 2, 3, 4, 5, 6, 7, 8],
        historical_low_base_values=[1000.0, 1100.0, 1200.0],
    )

    # --- Historical block ---
    for name in REQUIRED_HISTORICAL:
        assert getattr(res.historical, name) is not None, name
    assert res.historical.mom == 15.0
    assert res.historical.qoq == 11.0
    assert res.historical.yoy == 9.0
    assert len(res.historical.same_period_detail) == 3
    assert res.historical.multi_year_trend == 69.0

    # --- Seasonal block ---
    for name in REQUIRED_SEASONAL:
        assert getattr(res.seasonal, name) is not None, name
    assert res.seasonal.data_sufficiency == "FULL"

    # --- Trend block ---
    for horizon in ("3M", "6M", "12M"):
        assert horizon in res.momentum
        for name in REQUIRED_MOMENTUM:
            assert getattr(res.momentum[horizon], name) is not None, (horizon, name)
    assert res.trend_state in (
        "Strong Improvement", "Improving", "Stable",
        "Deteriorating", "Strong Deterioration",
    )

    # --- Context block ---
    # Every contract field must exist and be set to a real value. The
    # tri-state flags (low_base, sign_change) legitimately hold None for
    # UNKNOWN / "no transition", which is itself a distinguishable state.
    for name in REQUIRED_CONTEXT:
        assert hasattr(res.context, name), name
        assert getattr(res.context, name) is not None or name in ("low_base", "sign_change"), name
    assert res.context.data_quality == "OK"
    assert res.context.data_sufficiency == "FULL"
    assert res.context.zero_base is False

    # --- Coverage / confidence ---
    assert res.trend_coverage in ("FULL", "LIMITED", "INSUFFICIENT")
    assert res.trend_confidence in ("HIGH", "MEDIUM", "LOW")
    assert res.coverage == res.trend_coverage


def test_output_contract_sufficiency_states_are_not_collapsed():
    res = _run(val_6m_curr=None, val_12m_curr=None)
    assert res.context.data_sufficiency == "INSUFFICIENT"
    assert res.seasonal.data_sufficiency == "INSUFFICIENT_DATA"
    assert res.trend_coverage == "INSUFFICIENT"
    assert res.trend_confidence == "LOW"
    # Distinct concepts stay distinct.
    assert res.context.data_sufficiency != res.seasonal.data_sufficiency


def test_output_contract_zero_base_and_sign_change_contexts():
    res = _run(val_3m_curr=120.0, val_3m_prev=0.0)
    assert res.context.zero_base is True
    assert res.context.sign_change is None

    res = _run(val_3m_curr=120.0, val_3m_prev=-100.0)
    assert res.context.sign_change == "LOSS_TO_PROFIT"
    assert res.context.zero_base is False


def test_one_off_detection_is_conservative():
    # 4 robust-z against 3 observations with a real scale -> one-off.
    assert detect_one_off(1000.0, [10.0, 11.0, 12.0]) == (True, "ROBUST_Z_GT_4")
    # Not an outlier.
    assert detect_one_off(10.5, [10.0, 11.0, 12.0]) == (False, None)
    # Insufficient history -> not flagged rather than guessed.
    assert detect_one_off(1000.0, [10.0, 11.0]) == (False, None)
    assert detect_one_off(1000.0, None) == (False, None)


# --------------------------------------------------------------------------
# Flow vs stock treatment (specification sections 6-8)
# --------------------------------------------------------------------------

def test_flow_momentum_sums_windows():
    # Quarterly flow: 3M = 1 quarter, so Q(t)/Q(t-1) - 1.
    series = [100.0, 110.0, 120.0, 130.0]
    assert flow_momentum(series, 3) == 30.0


def test_stock_momentum_never_sums():
    # Quarterly stock: 12M = 4 periods apart.
    series = [100.0, 110.0, 120.0, 130.0, 156.0]
    assert stock_momentum(series, 12) == 56.0


def test_flow_and_stock_12m_differ():
    series = [100.0, 110.0, 120.0, 130.0, 140.0, 150.0, 160.0, 170.0]
    # Flow 12M: TTM(4..8) vs TTM(0..4) = 620/460 - 1.
    assert flow_momentum(series, 12) == pytest_approx(34.78260869565217)
    # Stock 12M: 170 vs 130 (4 periods apart).
    assert stock_momentum(series, 12) == pytest_approx(30.76923076923077)


def test_trend_12m_is_current_ttm_vs_ttm_twelve_months_earlier():
    # NOT prior-month TTM. TTM(5..8)=620 vs TTM(1..4)=460.
    series = [100.0, 110.0, 120.0, 130.0, 140.0, 150.0, 160.0, 170.0]
    assert trend_12m(series) == pytest_approx(34.78260869565217)
    # A prior-month TTM reading would have been 170/160 - 1 = 6.25%.
    assert trend_12m(series) != pytest_approx(6.25)


def test_engine_flow_series_end_to_end():
    series = [100.0, 110.0, 120.0, 130.0, 140.0, 150.0, 160.0, 170.0]
    res = _run(flow_series=series)
    assert res.momentum["3M"].pct_change == pytest_approx(6.25)
    assert res.momentum["6M"].pct_change == pytest_approx(13.636363636363635)
    assert res.momentum["12M"].pct_change == pytest_approx(34.78260869565217)
    assert res.context.data_quality == "OK"


def test_engine_stock_series_end_to_end():
    series = [100.0, 110.0, 120.0, 130.0, 140.0, 150.0, 160.0, 170.0]
    res = _run(stock_series=series)
    assert res.momentum["3M"].pct_change == pytest_approx(6.25)
    assert res.momentum["12M"].pct_change == pytest_approx(30.76923076923077)


def test_missing_observation_never_becomes_zero():
    # The missing observation sits inside the *current* 3M window, so the
    # window sum is undefined. It must never be read as a zero and summed.
    series = [100.0, 110.0, 120.0, 130.0, 140.0, 150.0, 160.0, None]
    res = _run(flow_series=series)
    assert res.momentum["3M"].pct_change is None
    assert res.momentum["3M"].status == "MISSING"
    # MISSING != 0 propagates to the trend state, not to a fabricated 0%.
    assert res.trend_state in ("INSUFFICIENT_DATA", "Improving", "Stable")


# --------------------------------------------------------------------------
# Preserved scenario behaviour (section 15)
# --------------------------------------------------------------------------

def test_scenario_1_strong_growth():
    engine = TrendEngine()
    history = [1, 2, 3, 4, 5, 6, 7, 8]
    res = engine.evaluate_trend(
        1, 10, "REVENUE",
        115.0, 100.0, 222.0, 200.0, 436.0, 400.0,
        history, history, history,
    )
    assert res.trend_state == "Strong Improvement"
    assert res.coverage == "FULL"


def test_scenario_2_moderate_improvement():
    engine = TrendEngine()
    history = [1, 2, 3, 4, 5, 6, 7, 8]
    res = engine.evaluate_trend(
        1, 10, "REVENUE",
        108.0, 100.0, 210.0, 200.0, 392.0, 400.0,
        history, history, history,
    )
    assert res.trend_state == "Improving"


def test_scenario_3_stable():
    engine = TrendEngine()
    weak_history = [1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
    res = engine.evaluate_trend(
        1, 10, "REVENUE",
        101.0, 100.0, 202.0, 200.0, 404.0, 400.0,
        weak_history, weak_history, weak_history,
    )
    assert res.trend_state == "Stable"


def test_scenario_4_gradual_deterioration():
    engine = TrendEngine()
    history = [8, 9, 10, 11, 12, 13, 14, 15]
    res = engine.evaluate_trend(
        1, 10, "REVENUE",
        96.0, 100.0, 188.0, 200.0, 372.0, 400.0,
        history, history, history,
    )
    assert res.trend_state == "Deteriorating"


def test_scenario_5_severe_deterioration():
    engine = TrendEngine()
    history = [1, 2, 3, 4, 5, 6, 7, 8]
    res = engine.evaluate_trend(
        1, 10, "REVENUE",
        84.0, 100.0, 174.0, 200.0, 356.0, 400.0,
        history, history, history,
    )
    assert res.trend_state == "Strong Deterioration"


def test_scenario_6_mixed():
    engine = TrendEngine()
    history = [1, 2, 3, 4, 5, 6, 7, 8]
    res = engine.evaluate_trend(
        1, 10, "REVENUE",
        115.0, 100.0, 190.0, 200.0, 432.0, 400.0,
        history, history, history,
    )
    assert res.trend_state == "Improving"


def test_scenario_7_two_valid_horizons():
    engine = TrendEngine()
    history = [1, 2, 3, 4, 5, 6, 7, 8]
    res = engine.evaluate_trend(
        1, 10, "REVENUE",
        110.0, 100.0, 214.0, 200.0, None, 400.0,
        history, history, history,
    )
    assert res.trend_state == "Improving"
    assert res.coverage == "LIMITED"


def test_scenario_8_one_valid_horizon_insufficient():
    engine = TrendEngine()
    history = [1, 2, 3, 4, 5, 6, 7, 8]
    res = engine.evaluate_trend(
        1, 10, "REVENUE",
        110.0, 100.0, None, 200.0, None, 400.0,
        history, history, history,
    )
    assert res.trend_state == "INSUFFICIENT_DATA"
    assert res.coverage == "INSUFFICIENT"
