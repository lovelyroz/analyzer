from src.market.engine import MarketEngine
from src.market.parameters import ABNORMAL_VOLUME_RATIO, MOMENTUM_STRONG_RETURN, TREND_STRONG_RETURN, VOLATILITY_EXTREME_RATIO


def test_model_version_parameters_are_the_source_of_market_thresholds():
    engine = MarketEngine()
    assert engine._trend_state(TREND_STRONG_RETURN, 0.001) == "STRONG_UPTREND"
    assert engine._momentum_state(MOMENTUM_STRONG_RETURN, MOMENTUM_STRONG_RETURN, MOMENTUM_STRONG_RETURN) == "STRONG_POSITIVE"
    assert engine._volatility_state(0.20, 0.20 / VOLATILITY_EXTREME_RATIO) == "EXTREME"
    assert engine._price_volume_state(0.10, ABNORMAL_VOLUME_RATIO) == "PRICE_VOLUME_CONFIRMATION"


def test_liquidity_state_distinguishes_relative_low_and_high_activity():
    engine = MarketEngine()
    assert engine._liquidity_state(5.0, [5.0] * 20 + [20.0] * 40) == "LOW"
    assert engine._liquidity_state(40.0, [10.0] * 60) == "HIGH"
