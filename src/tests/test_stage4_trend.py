import pytest
from src.trend.utils import calculate_pct_change, is_low_base, is_sign_change
from src.trend.engine import TrendEngine

def test_pct_change_and_flags():
    assert calculate_pct_change(150.0, 100.0) == 50.0
    assert calculate_pct_change(100.0, 0.0) is None
    assert is_low_base(0.5, threshold=1.0) is True
    assert is_sign_change(-10.0, 50.0) is True

def test_scenario_1_strong_growth():
    engine = TrendEngine()
    # 3M = +15%, 6M = +11%, 12M = +9% -> Strong Improvement
    res = engine.evaluate_trend(1, 10, "REVENUE", 115.0, 100.0, 222.0, 200.0, 436.0, 400.0)
    assert res.trend_state == "Strong Improvement"
    assert res.coverage == "FULL"

def test_scenario_3_stable():
    engine = TrendEngine()
    # 3M = +1%, 6M = +1%, 12M = +1% -> Stable
    res = engine.evaluate_trend(1, 10, "REVENUE", 101.0, 100.0, 202.0, 200.0, 404.0, 400.0)
    assert res.trend_state == "Stable"

def test_scenario_7_two_valid_horizons():
    engine = TrendEngine()
    # 3M = +10%, 6M = +7%, 12M = NULL -> Improving (Coverage: LIMITED)
    res = engine.evaluate_trend(1, 10, "REVENUE", 110.0, 100.0, 214.0, 200.0, None, 400.0)
    assert res.trend_state == "Improving"
    assert res.coverage == "LIMITED"

def test_scenario_8_one_valid_horizon_insufficient():
    engine = TrendEngine()
    # 3M = +10%, 6M = NULL, 12M = NULL -> INSUFFICIENT_DATA
    res = engine.evaluate_trend(1, 10, "REVENUE", 110.0, 100.0, None, 200.0, None, 400.0)
    assert res.trend_state == "INSUFFICIENT_DATA"
    assert res.coverage == "INSUFFICIENT"