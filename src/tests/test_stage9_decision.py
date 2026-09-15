from datetime import datetime

from src.market.schema import MarketSignalResult
from src.scoring.schema import FundamentalScoreResult
from src.valuation.schema import ValuationResult
from src.decision.engine import DecisionEngine


def make_fundamental(score):
    return FundamentalScoreResult(
        company_id=1,
        period_id=10,
        overall_score=score,
        category_scores={},
        kpi_scores=[],
        calculation_timestamp=datetime.utcnow(),
    )


def make_valuation(status="ATTRACTIVE", risk="LOW", reliability=85.0, dispersion=None):
    metadata = {}
    if dispersion is not None:
        metadata["scenario_dispersion"] = dispersion
    return ValuationResult(
        company_id=1,
        period_id=10,
        current_price=1000.0,
        expected_fair_value=1300.0,
        margin_of_safety_pct=30.0,
        valuation_status=status,
        valuation_confidence=85.0,
        valuation_risk_level=risk,
        scenarios={},
        model_version="STAGE7_V1",
        calculation_timestamp=datetime.utcnow(),
        forecast_reliability_score=reliability,
        valuation_data_quality=100.0,
        metadata=metadata,
    )


def make_market(trend="UPTREND", momentum="POSITIVE", liquidity="NORMAL"):
    return MarketSignalResult(
        company_id=1,
        as_of_date=datetime.utcnow(),
        trend_state=trend,
        momentum_state=momentum,
        liquidity_state=liquidity,
        market_data_quality="VALID",
    )


def test_strong_buy_requires_aligned_families():
    result = DecisionEngine().make_decision(
        1, 10, make_fundamental(85), make_valuation(), make_market(),
        forecast_reliability_score=85,
        trend_state="STRONG_IMPROVEMENT",
        forecast_direction="POSITIVE",
    )

    assert result.recommendation == "STRONG_BUY"
    assert result.holding_status == "STRONG_HOLD"
    assert result.decision_confidence >= 75
    assert result.metadata["market_score_used"] is False
    assert result.metadata["position_sizing_used"] is False


def test_value_trap_does_not_become_buy():
    result = DecisionEngine().make_decision(
        1, 10, make_fundamental(30), make_valuation("ATTRACTIVE"), make_market("DOWNTREND"),
        forecast_reliability_score=80,
        trend_state="DETERIORATING",
        forecast_direction="NEGATIVE",
    )

    assert result.recommendation == "WATCH"
    assert "CHEAP_BUT_WEAK" in result.conflicts


def test_strong_but_expensive_is_not_buy():
    result = DecisionEngine().make_decision(
        1, 10, make_fundamental(85), make_valuation("VERY_EXPENSIVE", "HIGH"), make_market(),
        forecast_reliability_score=85,
        trend_state="IMPROVING",
        forecast_direction="POSITIVE",
    )

    assert result.recommendation == "HOLD"
    assert result.holding_status in {"HOLD", "HOLD_WITH_CAUTION"}
    assert "STRONG_BUT_EXPENSIVE" in result.conflicts


def test_low_forecast_reliability_limits_strong_conviction():
    result = DecisionEngine().make_decision(
        1, 10, make_fundamental(85), make_valuation("ATTRACTIVE", "LOW", 35), make_market(),
        forecast_reliability_score=35,
        trend_state="IMPROVING",
        forecast_direction="POSITIVE",
    )

    assert result.recommendation == "WATCH"
    assert "POSITIVE_FORECAST_LOW_RELIABILITY" in result.conflicts
    assert result.decision_confidence < 75


def test_market_does_not_override_strong_fundamentals():
    result = DecisionEngine().make_decision(
        1, 10, make_fundamental(85), make_valuation(), make_market("DOWNTREND"),
        forecast_reliability_score=85,
        trend_state="IMPROVING",
        forecast_direction="POSITIVE",
    )

    assert result.recommendation == "STRONG_BUY"
    assert "STRONG_FUNDAMENTAL_WEAK_MARKET" in result.conflicts


def test_usd_share_value_is_context_not_a_new_score():
    result = DecisionEngine().make_decision(
        1, 10, make_fundamental(35), make_valuation("ATTRACTIVE"), make_market(),
        forecast_reliability_score=70,
        trend_state="STABLE",
        forecast_direction="NEUTRAL",
        usd_share_value_change_pct=12.0,
    )

    assert "POSITIVE_FX_NEGATIVE_FUNDAMENTAL" in result.conflicts
    assert result.usd_context["share_value_change_pct"] == 12.0


def test_negative_eps_valuation_is_not_reconstructed_by_stage9():
    result = DecisionEngine().make_decision(
        1, 10, make_fundamental(70), make_valuation("NOT_APPLICABLE"), make_market(),
        forecast_reliability_score=80,
        trend_state="IMPROVING",
        forecast_direction="POSITIVE",
    )

    assert result.recommendation in {"WATCH", "HOLD", "BUY"}
    assert "VALUATION_NOT_APPLICABLE" in result.conflicts
    assert result.metadata["upstream_recalculation"] is False


def test_no_position_sizing_contract():
    result = DecisionEngine().make_decision(
        1, 10, make_fundamental(60), make_valuation("FAIR"), make_market(),
        forecast_reliability_score=70,
        trend_state="STABLE",
        forecast_direction="NEUTRAL",
    )

    assert not hasattr(result, "suggested_allocation_pct")
    assert not hasattr(result, "composite_score")
