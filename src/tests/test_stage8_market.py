from datetime import datetime, timedelta

from src.market.engine import MarketEngine
from src.market.indicators import calculate_rsi, calculate_sma, cumulative_return, maximum_drawdown, price_position, realized_volatility


def rows(prices, volume=1000.0, value=100000.0, start=datetime(2026, 1, 1)):
    return [
        {"date": start + timedelta(days=i), "close": price, "adjusted_close": price, "volume": volume, "value": value}
        for i, price in enumerate(prices)
    ]


def test_legacy_indicator_helpers_remain_available():
    prices = [float(i) for i in range(1, 60)]
    assert calculate_sma(prices, 50) is not None
    assert calculate_rsi(prices, 14) == 100.0


def test_core_market_indicators():
    prices = list(range(1, 30))
    assert round(cumulative_return(prices, 5), 6) == round(29 / 24 - 1, 6)
    assert price_position(prices, 20) == 1.0
    assert maximum_drawdown(prices, 20) == 0.0
    assert realized_volatility(prices, 20) is not None


def test_market_engine_returns_state_not_score():
    prices = list(range(1, 260))
    result = MarketEngine().analyze_market(1, datetime(2026, 9, 16), rows(prices))
    assert result.model_version == "STAGE8_V1"
    assert result.market_contract_version == "MARKET_CONTRACT_V1.1"
    assert result.trend_state in {"UPTREND", "STRONG_UPTREND"}
    assert result.momentum_state in {"POSITIVE", "STRONG_POSITIVE"}
    assert result.metadata["market_score"] is None
    assert result.metadata["decision_signal"] is None
    assert result.indicators.returns["20D"] is not None
    assert result.indicators.price_vs_ma["MA20"] is not None
    assert result.indicators.max_drawdown["252D"] == 0.0


def test_market_output_contract_includes_52w_volume_and_value_context():
    prices = list(range(1, 260))
    result = MarketEngine().analyze_market(1, datetime(2026, 9, 16), rows(prices, volume=2000.0, value=100000.0))
    assert result.indicators.distance_from_52w_high == 0.0
    assert result.indicators.average_volume_20d == 2000.0
    assert result.indicators.average_trading_value_20d == 100000.0
    assert result.indicators.trading_value_stability_20d == 0.0
    assert result.metadata["price_basis"] == "ADJUSTED_CLOSE"


def test_trading_value_stability_is_coefficient_of_variation():
    data = rows(list(range(1, 260)), value=100000.0)
    for i, row in enumerate(data[-20:]):
        row["value"] = 100000.0 * (1.0 + i / 20.0)
    result = MarketEngine().analyze_market(1, datetime(2026, 9, 16), data)
    assert result.indicators.trading_value_stability_20d is not None
    assert result.indicators.trading_value_stability_20d > 0.0
    assert result.metadata["trading_value_stability_definition"] == "20D coefficient_of_variation"


def test_close_fallback_is_explicitly_flagged():
    data = rows(list(range(1, 260)))
    for row in data:
        row.pop("adjusted_close")
    result = MarketEngine().analyze_market(1, datetime(2026, 9, 16), data)
    assert result.metadata["price_basis"] == "CLOSE_FALLBACK"


def test_point_in_time_excludes_future_rows():
    prices = list(range(1, 260))
    data = rows(prices)
    data.append({"date": datetime(2027, 1, 1), "close": 100000.0, "adjusted_close": 100000.0, "volume": 1.0, "value": 1.0})
    result = MarketEngine().analyze_market(1, datetime(2026, 9, 16), data, point_in_time=True)
    assert result.indicators.returns["20D"] == (259 / 239 - 1)


def test_adjusted_close_drives_historical_returns():
    data = rows(list(range(1, 260)))
    for row in data:
        row["close"] = row["adjusted_close"] * 2
    result = MarketEngine().analyze_market(1, datetime(2026, 9, 16), data)
    assert result.indicators.returns["20D"] == (259 / 239 - 1)


def test_missing_benchmark_does_not_create_synthetic_relative_strength():
    result = MarketEngine().analyze_market(1, datetime(2026, 9, 16), rows(list(range(1, 260))))
    assert result.relative_strength_industry == "INSUFFICIENT_DATA"
    assert result.relative_strength_market == "INSUFFICIENT_DATA"
    assert result.market_regime == "INSUFFICIENT_DATA"


def test_relative_strength_uses_same_horizon():
    stock = rows(list(range(1, 260)))
    industry = rows([x * 1.5 for x in range(1, 260)])
    result = MarketEngine().analyze_market(1, datetime(2026, 9, 16), stock, industry_benchmark=industry)
    assert result.relative_strength_industry == "NEUTRAL"


def test_negative_market_state_generates_context_alerts_not_decision():
    prices = list(range(260, 0, -1))
    result = MarketEngine().analyze_market(1, datetime(2026, 9, 16), rows(prices))
    assert result.trend_state in {"DOWNTREND", "STRONG_DOWNTREND"}
    assert result.momentum_state in {"NEGATIVE", "STRONG_NEGATIVE"}
    assert any("DOWNTREND" in alert or "DRAWDOWN" in alert for alert in result.alerts)
    assert all(not alert.startswith("BUY") and not alert.startswith("SELL") for alert in result.alerts)


def test_drawdown_moderate_non_recovering_is_not_labeled_recovering():
    prices = [100.0] * 30
    prices[-1] = 90.0
    assert MarketEngine._drawdown_state(-0.10, prices) == "STABLE_DRAWDOWN"


def test_drawdown_recovery_requires_rebound_from_recent_low():
    prices = [100.0] * 18 + [80.0, 85.0]
    assert MarketEngine._drawdown_state(-0.15, prices) == "RECOVERING"


def test_drawdown_deep_and_new_low_states_remain_distinct():
    deep = [100.0] * 19 + [80.0]
    extreme_low = [100.0] * 19 + [50.0]
    assert MarketEngine._drawdown_state(-0.20, deep) == "DEEP_DRAWDOWN"
    assert MarketEngine._drawdown_state(-0.50, extreme_low) == "NEW_LOW"


def test_legacy_api_is_compatibility_only():
    result = MarketEngine().analyze_market_signals(1, datetime(2026, 9, 16), list(range(1, 260)), 100, 50)
    assert result.metadata["market_score"] is None
    assert result.money_flow_status == "INFLOW"
    assert result.trend_state != ""
