import pytest
from datetime import datetime
from src.scoring.schema import FundamentalScoreResult
from src.valuation.schema import ValuationResult
from src.market.schema import MarketSignalResult, TechnicalIndicatorsResult
from src.decision.rules import map_score_to_recommendation
from src.decision.engine import DecisionEngine

def test_decision_rules():
    assert map_score_to_recommendation(85.0, 30.0) == ("STRONG_BUY", 10.0)
    assert map_score_to_recommendation(30.0, -15.0) == ("STRONG_SELL", 0.0)

def test_decision_engine_integration():
    engine = DecisionEngine()

    fund_res = FundamentalScoreResult(
        company_id=1, period_id=10, overall_score=80.0, category_scores={}, kpi_scores=[], calculation_timestamp=datetime.utcnow()
    )
    val_res = ValuationResult(
        company_id=1, period_id=10, current_price=1000.0, expected_fair_value=1350.0,
        margin_of_safety_pct=35.0, valuation_status="UNDERVALUED", valuation_confidence=80.0,
        valuation_risk_level="LOW", scenarios={}, model_version="V1.0", calculation_timestamp=datetime.utcnow()
    )
    market_res = MarketSignalResult(
        company_id=1, as_of_date=datetime.utcnow(), trend_alignment="BULLISH", rsi_status="NEUTRAL",
        money_flow_status="INFLOW", technical_score=75.0, indicators=TechnicalIndicatorsResult(None, None, None, None),
        calculation_timestamp=datetime.utcnow()
    )

    result = engine.make_decision(
        company_id=1, period_id=10, fundamental_result=fund_res, valuation_result=val_res, market_result=market_res
    )

    assert result.company_id == 1
    assert result.recommendation == "STRONG_BUY"
    assert result.suggested_allocation_pct == 10.0
    assert len(result.rationale_pros) >= 2
    assert result.risk_level == "LOW"