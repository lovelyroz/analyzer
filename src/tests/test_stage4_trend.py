from src.trend.utils import (
    calculate_pct_change,
    is_low_base,
    is_sign_change,
    historical_percentile_abs,
)
from src.trend.engine import TrendEngine


def test_pct_change_and_sign_change_rules():
    assert calculate_pct_change(150.0, 100.0) == 50.0
    assert calculate_pct_change(100.0, 0.0) is None
    assert calculate_pct_change(120.0, -100.0) is None
    assert calculate_pct_change(-50.0, 100.0) is None
    assert is_sign_change(-10.0, 50.0) is True


def test_low_base_requires_three_history_values_and_uses_robust_z():
    assert is_low_base(0.5, [10.0, 11.0, 12.0]) is True
    assert is_low_base(10.0, [10.0, 11.0]) is None
    assert is_low_base(10.0, None) is None


def test_relative_strength_requires_eight_observations():
    assert historical_percentile_abs(10.0, [1, 2, 3, 4, 5, 6, 7]) is None
    assert historical_percentile_abs(10.0, [1, 2, 3, 4, 5, 6, 7, 8]) == 100.0


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
