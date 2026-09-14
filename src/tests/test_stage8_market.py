import pytest
from datetime import datetime
from src.market.indicators import calculate_sma, calculate_rsi
from src.market.engine import MarketEngine

def test_indicators():
    prices = [float(i) for i in range(1, 60)]  # 1 to 59
    assert calculate_sma(prices, 50) is not None
    assert calculate_rsi(prices, 14) == 100.0  # همواره صعودی

def test_market_engine():
    engine = MarketEngine()
    prices = [100.0 + i for i in range(200)]  # صعودی مداوم
    
    result = engine.analyze_market_signals(
        company_id=1,
        as_of_date=datetime.utcnow(),
        close_prices=prices,
        individual_buy_vol=500.0,
        individual_sell_vol=200.0,
        close_price_today=300.0
    )

    assert result.company_id == 1
    assert result.trend_alignment == "BULLISH"
    assert result.money_flow_status == "INFLOW"
    assert result.technical_score >= 60.0