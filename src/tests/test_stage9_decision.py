from datetime import datetime, timezone
from types import SimpleNamespace

import pytest

from src.market.schema import MarketSignalResult
from src.scoring.schema import FundamentalScoreResult
from src.valuation.schema import ValuationResult
from src.decision.engine import DecisionEngine
from src.decision import service as decision_service


def utc_now_naive():
    return datetime.now(timezone.utc).replace(tzinfo=None)


def make_fundamental(score):
    return FundamentalScoreResult(
        company_id=1,
        period_id=10,
        overall_score=score,
        category_scores={},
        kpi_scores=[],
        calculation_timestamp=utc_now_naive(),
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
        calculation_timestamp=utc_now_naive(),
        forecast_reliability_score=reliability,
        valuation_data_quality=100.0,
        metadata=metadata,
    )


def make_market(trend="UPTREND", momentum="POSITIVE", liquidity="NORMAL"):
    return MarketSignalResult(
        company_id=1,
        as_of_date=utc_now_naive(),
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


def test_jalali_orchestration_passes_stage7_result_to_stage9(monkeypatch):
    valuation = make_valuation()
    stage7_calls = []

    def calculate_valuation(*args, **kwargs):
        stage7_calls.append((args, kwargs))
        return valuation

    monkeypatch.setattr(
        decision_service,
        "calculate_valuation_as_of_jalali",
        calculate_valuation,
    )
    original_make_decision = DecisionEngine.make_decision
    received = {}

    def capture_valuation(self, company_id, period_id, fundamental, valuation_result, market, reliability=None, **kwargs):
        received["valuation"] = valuation_result
        return original_make_decision(
            self, company_id, period_id, fundamental, valuation_result, market, reliability, **kwargs
        )

    monkeypatch.setattr(DecisionEngine, "make_decision", capture_valuation)
    forecast = SimpleNamespace(company_id=1, forecast_period_id=10)

    result = decision_service.calculate_decision_as_of_jalali(
        session=None,
        forecast_result=forecast,
        as_of_jalali_date=(1405, 2, 11),
        fundamental_result=make_fundamental(85),
        market_result=make_market(),
    )

    assert result.valuation is valuation
    assert received["valuation"] is valuation
    assert result.decision.valuation_status == valuation.valuation_status
    assert len(stage7_calls) == 1
    assert stage7_calls[0][0] == (None, 1, 10, forecast, (1405, 2, 11))
    assert result.decision.metadata["market_score_used"] is False
    assert result.decision.metadata["position_sizing_used"] is False


def test_jalali_orchestration_rejects_mismatched_fundamental_and_market_identity(monkeypatch):
    def stage7_must_not_run(*args, **kwargs):
        raise AssertionError("Stage 7 must not run when upstream identities disagree")

    monkeypatch.setattr(decision_service, "calculate_valuation_as_of_jalali", stage7_must_not_run)
    forecast = SimpleNamespace(company_id=1, forecast_period_id=10)

    wrong_period_fundamental = make_fundamental(85)
    wrong_period_fundamental.period_id = 11
    with pytest.raises(ValueError, match="fundamental result identity"):
        decision_service.calculate_decision_as_of_jalali(
            None, forecast, (1405, 2, 11), wrong_period_fundamental, make_market()
        )

    wrong_company_market = make_market()
    wrong_company_market.company_id = 2
    with pytest.raises(ValueError, match="market result company_id"):
        decision_service.calculate_decision_as_of_jalali(
            None, forecast, (1405, 2, 11), make_fundamental(85), wrong_company_market
        )


def test_value_trap_does_not_become_buy():
    result = DecisionEngine().make_decision(
        1, 10, make_fundamental(30), make_valuation("ATTRACTIVE"), make_market("DOWNTREND"),
        forecast_reliability_score=80, trend_state="DETERIORATING", forecast_direction="NEGATIVE",
    )
    assert result.recommendation == "WATCH"
    assert "CHEAP_BUT_WEAK" in result.conflicts


def test_strong_but_expensive_is_not_buy():
    result = DecisionEngine().make_decision(
        1, 10, make_fundamental(85), make_valuation("VERY_EXPENSIVE", "HIGH"), make_market(),
        forecast_reliability_score=85, trend_state="IMPROVING", forecast_direction="POSITIVE",
    )
    assert result.recommendation == "HOLD"
    assert result.holding_status in {"HOLD", "HOLD_WITH_CAUTION"}
    assert "STRONG_BUT_EXPENSIVE" in result.conflicts


def test_low_forecast_reliability_limits_strong_conviction():
    result = DecisionEngine().make_decision(
        1, 10, make_fundamental(85), make_valuation("ATTRACTIVE", "LOW", 35), make_market(),
        forecast_reliability_score=35, trend_state="IMPROVING", forecast_direction="POSITIVE",
    )
    assert result.recommendation == "WATCH"
    assert "POSITIVE_FORECAST_LOW_RELIABILITY" in result.conflicts
    assert result.decision_confidence < 75


def test_market_does_not_override_strong_fundamentals():
    result = DecisionEngine().make_decision(
        1, 10, make_fundamental(85), make_valuation(), make_market("DOWNTREND"),
        forecast_reliability_score=85, trend_state="IMPROVING", forecast_direction="POSITIVE",
    )
    assert result.recommendation == "STRONG_BUY"
    assert "STRONG_FUNDAMENTAL_WEAK_MARKET" in result.conflicts


def test_usd_share_value_is_context_not_a_new_score():
    result = DecisionEngine().make_decision(
        1, 10, make_fundamental(35), make_valuation("ATTRACTIVE"), make_market(),
        forecast_reliability_score=70, trend_state="STABLE", forecast_direction="NEUTRAL",
        usd_share_value_change_pct=12.0,
    )
    assert "POSITIVE_FX_NEGATIVE_FUNDAMENTAL" in result.conflicts
    assert result.usd_context["share_value_change_pct"] == 12.0


def test_negative_eps_valuation_is_not_reconstructed_by_stage9():
    result = DecisionEngine().make_decision(
        1, 10, make_fundamental(70), make_valuation("NOT_APPLICABLE"), make_market(),
        forecast_reliability_score=80, trend_state="IMPROVING", forecast_direction="POSITIVE",
    )
    assert result.recommendation in {"WATCH", "HOLD", "BUY"}
    assert "VALUATION_NOT_APPLICABLE" in result.conflicts
    assert result.metadata["upstream_recalculation"] is False


def test_no_position_sizing_contract():
    result = DecisionEngine().make_decision(
        1, 10, make_fundamental(60), make_valuation("FAIR"), make_market(),
        forecast_reliability_score=70, trend_state="STABLE", forecast_direction="NEUTRAL",
    )
    assert not hasattr(result, "suggested_allocation_pct")
    assert not hasattr(result, "composite_score")


def test_hysteresis_prevents_small_buy_to_hold_change():
    # Base rules produce HOLD here; previous BUY should persist because the
    # normal exit threshold is not breached by a material negative event.
    result = DecisionEngine().make_decision(
        1, 10, make_fundamental(60), make_valuation("FAIR"), make_market(),
        forecast_reliability_score=70, trend_state="STABLE", forecast_direction="NEUTRAL",
        previous_decision="BUY", previous_decision_confidence=80,
    )
    assert result.previous_decision == "BUY"
    assert result.recommendation == "BUY"
    assert result.decision_change == "UNCHANGED"
    assert result.metadata["hysteresis_enabled"] is True
    assert result.metadata["hysteresis_applied"] is True


def test_hysteresis_allows_material_deterioration():
    result = DecisionEngine().make_decision(
        1, 10, make_fundamental(30), make_valuation("EXPENSIVE", "HIGH"), make_market("DOWNTREND"),
        forecast_reliability_score=80, trend_state="DETERIORATING", forecast_direction="NEGATIVE",
        previous_decision="BUY", previous_decision_confidence=80,
    )
    assert result.recommendation in {"SELL", "STRONG_SELL", "WATCH"}
    assert result.decision_change == "CHANGED"
    assert result.decision_change_date is not None


def test_decision_history_contract():
    result = DecisionEngine().make_decision(
        1, 10, make_fundamental(60), make_valuation("FAIR"), make_market(),
        forecast_reliability_score=70, trend_state="STABLE", forecast_direction="NEUTRAL",
        previous_decision="HOLD",
    )
    assert result.previous_decision == "HOLD"
    assert result.decision_change == "UNCHANGED"
    assert result.decision_change_date is None
    assert result.decision_date is not None
    assert isinstance(result.decision_change_reasons, list)


def test_ranking_contract_has_no_new_score():
    result = DecisionEngine().make_decision(
        1, 10, make_fundamental(80), make_valuation("ATTRACTIVE"), make_market(),
        forecast_reliability_score=80, trend_state="IMPROVING", forecast_direction="POSITIVE",
    )
    assert result.decision_ranking_eligibility is True
    assert result.decision_rank_within_industry is None
    assert result.ranking_eligibility is True
    assert result.rank_within_industry is None
    assert result.ranking_inputs["within_industry"] is True
    assert result.ranking_inputs["new_ranking_score_created"] is False


def test_dashboard_contract_carries_required_fields():
    result = DecisionEngine().make_decision(
        1, 10, make_fundamental(80), make_valuation("ATTRACTIVE"), make_market(),
        forecast_reliability_score=80, trend_state="IMPROVING", forecast_direction="POSITIVE",
        fx_context={
            "fx_regime": "RISING",
            "fx_company_impact": "POSITIVE",
            "usd_relative_valuation_context": "POSITIVE",
            "free_market_fx": 120000.0,
            "operational_fx": 90000.0,
            "fx_gap": 0.3333,
        },
    )
    assert result.fundamental_state == "STRONG"
    assert result.fundamental_score == 80
    assert result.trend_state == "IMPROVING"
    assert result.forecast_state == "POSITIVE"
    assert result.forecast_reliability == 80
    assert result.valuation_status == "ATTRACTIVE"
    assert result.expected_upside == 30.0
    assert result.valuation_risk == "LOW"
    assert result.valuation_confidence == 85.0
    assert result.market_trend_state == "UPTREND"
    assert result.market_momentum_state == "POSITIVE"
    assert result.relative_strength_state == "INSUFFICIENT_DATA"
    assert result.liquidity_state == "NORMAL"
    assert result.fx_regime == "RISING"
    assert result.fx_company_impact == "POSITIVE"
    assert result.usd_relative_valuation_context == "POSITIVE"
    assert result.free_market_fx == 120000.0
    assert result.operational_fx == 90000.0
    assert result.fx_gap == 0.3333
    assert result.decision == result.recommendation
    assert result.decision_conflict == result.conflicts
    assert isinstance(result.decision_reasons, list)
    assert isinstance(result.decision_risks, list)
    assert result.decision_date is not None
    assert result.model_version == "STAGE9_V1"
    assert result.contract_version == "DECISION_CONTRACT_V1"


    def test_scenario_dispersion_threshold_boundaries():
        """Verify scenario_dispersion threshold boundaries (> 0.50, == 0.50, < 0.50, None)."""
        engine = DecisionEngine()

        # 1. Above threshold (> 0.50) -> triggers HIGH_EXPECTED_UPSIDE_HIGH_BEAR_RISK
        res_above = engine.make_decision(
            1,
            10,
            make_fundamental(85),
            make_valuation(dispersion=0.55),
            make_market(),
            forecast_reliability_score=85,
            trend_state="STRONG_IMPROVEMENT",
            forecast_direction="POSITIVE",
        )
        assert "HIGH_EXPECTED_UPSIDE_HIGH_BEAR_RISK" in res_above.conflicts

        # 2. Exactly at threshold (== 0.50) -> does NOT trigger conflict
        res_at = engine.make_decision(
            1,
            10,
            make_fundamental(85),
            make_valuation(dispersion=0.50),
            make_market(),
            forecast_reliability_score=85,
            trend_state="STRONG_IMPROVEMENT",
            forecast_direction="POSITIVE",
        )
        assert "HIGH_EXPECTED_UPSIDE_HIGH_BEAR_RISK" not in res_at.conflicts

        # 3. Below threshold (< 0.50) -> does NOT trigger conflict
        res_below = engine.make_decision(
            1,
            10,
            make_fundamental(85),
            make_valuation(dispersion=0.45),
            make_market(),
            forecast_reliability_score=85,
            trend_state="STRONG_IMPROVEMENT",
            forecast_direction="POSITIVE",
        )
        assert "HIGH_EXPECTED_UPSIDE_HIGH_BEAR_RISK" not in res_below.conflicts

        # 4. None dispersion -> does NOT trigger conflict
        res_none = engine.make_decision(
            1,
            10,
            make_fundamental(85),
            make_valuation(dispersion=None),
            make_market(),
            forecast_reliability_score=85,
            trend_state="STRONG_IMPROVEMENT",
            forecast_direction="POSITIVE",
        )
        assert "HIGH_EXPECTED_UPSIDE_HIGH_BEAR_RISK" not in res_none.conflicts


    def test_scenario_dispersion_causes_ten_point_confidence_deduction():
        """Verify that scenario_dispersion > 0.50 directly deducts 10 points from decision confidence."""
        engine = DecisionEngine()
        kwargs = dict(
            company_id=1,
            period_id=10,
            fundamental_result=make_fundamental(85),
            market_result=make_market(),
            forecast_reliability_score=85,
            trend_state="STRONG_IMPROVEMENT",
            forecast_direction="POSITIVE",
        )

        # Baseline without dispersion conflict
        base_res = engine.make_decision(
            valuation_result=make_valuation(dispersion=0.45), **kwargs
        )
        assert base_res.decision_confidence == 100.0

        # With dispersion > 0.50 -> 10-point penalty
        disp_res = engine.make_decision(
            valuation_result=make_valuation(dispersion=0.55), **kwargs
        )
        assert disp_res.decision_confidence == 90.0
        assert base_res.decision_confidence - disp_res.decision_confidence == 10.0


    def test_scenario_dispersion_blocks_strong_buy():
        """Verify that HIGH_EXPECTED_UPSIDE_HIGH_BEAR_RISK blocks STRONG_BUY recommendation."""
        engine = DecisionEngine()
        kwargs = dict(
            company_id=1,
            period_id=10,
            fundamental_result=make_fundamental(85),
            market_result=make_market(),
            forecast_reliability_score=85,
            trend_state="STRONG_IMPROVEMENT",
            forecast_direction="POSITIVE",
        )

        # Without dispersion conflict -> STRONG_BUY
        qualifying_res = engine.make_decision(
            valuation_result=make_valuation(dispersion=0.50), **kwargs
        )
        assert qualifying_res.recommendation == "STRONG_BUY"

        # With dispersion > 0.50 -> STRONG_BUY blocked, degraded to BUY
        blocked_res = engine.make_decision(
            valuation_result=make_valuation(dispersion=0.55), **kwargs
        )
        assert blocked_res.recommendation == "BUY"
        assert "HIGH_EXPECTED_UPSIDE_HIGH_BEAR_RISK" in blocked_res.conflicts


    def test_scenario_dispersion_penalty_distinct_from_valuation_risk_level_high():
        """Verify distinction between dispersion conflict penalty and valuation_risk_level penalty."""
        engine = DecisionEngine()
        kwargs = dict(
            company_id=1,
            period_id=10,
            fundamental_result=make_fundamental(85),
            market_result=make_market(),
            forecast_reliability_score=85,
            trend_state="STRONG_IMPROVEMENT",
            forecast_direction="POSITIVE",
        )

        # 1. Low risk, low dispersion -> 100.0 confidence, no conflict
        c1 = engine.make_decision(
            valuation_result=make_valuation(risk="LOW", dispersion=0.45), **kwargs
        )
        assert c1.decision_confidence == 100.0
        assert "HIGH_EXPECTED_UPSIDE_HIGH_BEAR_RISK" not in c1.conflicts

        # 2. Low risk, high dispersion -> 90.0 confidence, dispersion conflict present
        c2 = engine.make_decision(
            valuation_result=make_valuation(risk="LOW", dispersion=0.55), **kwargs
        )
        assert c2.decision_confidence == 90.0
        assert "HIGH_EXPECTED_UPSIDE_HIGH_BEAR_RISK" in c2.conflicts

        # 3. High risk, low dispersion -> 90.0 confidence, NO dispersion conflict
        c3 = engine.make_decision(
            valuation_result=make_valuation(risk="HIGH", dispersion=0.45), **kwargs
        )
        assert c3.decision_confidence == 90.0
        assert "HIGH_EXPECTED_UPSIDE_HIGH_BEAR_RISK" not in c3.conflicts

        # 4. High risk, high dispersion -> 80.0 confidence (both penalties apply)
        c4 = engine.make_decision(
            valuation_result=make_valuation(risk="HIGH", dispersion=0.55), **kwargs
        )
        assert c4.decision_confidence == 80.0
        assert "HIGH_EXPECTED_UPSIDE_HIGH_BEAR_RISK" in c4.conflicts
