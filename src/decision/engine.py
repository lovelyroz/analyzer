from datetime import datetime
from typing import Dict, List, Optional

from src.scoring.schema import FundamentalScoreResult
from src.valuation.schema import ValuationResult
from src.market.schema import MarketSignalResult
from src.decision.schema import FinalDecisionResult
from src.decision.rules import (
    classify_fundamental,
    classify_reliability,
    classify_valuation,
    is_negative_direction,
    is_positive_direction,
)


MODEL_VERSION = "STAGE9_V1"
CONTRACT_VERSION = "DECISION_CONTRACT_V1"


class DecisionEngine:
    """Stage 9 V1: rule-based evidence integration."""

    def make_decision(
        self,
        company_id: int,
        period_id: int,
        fundamental_result: FundamentalScoreResult,
        valuation_result: ValuationResult,
        market_result: MarketSignalResult,
        forecast_reliability_score: Optional[float] = None,
        *,
        trend_state: Optional[str] = None,
        forecast_direction: Optional[str] = None,
        forecast_revision_trend: Optional[str] = None,
        forecast_quality: Optional[str] = None,
        usd_share_value_change_pct: Optional[float] = None,
        fx_context: Optional[Dict[str, object]] = None,
        data_cutoff_datetime: Optional[datetime] = None,
    ) -> FinalDecisionResult:
        conflicts: List[str] = []
        pros: List[str] = []
        cons: List[str] = []

        fund_score = fundamental_result.overall_score
        fundamental_state = classify_fundamental(fund_score)
        valuation_state = classify_valuation(valuation_result.valuation_status)
        reliability = (
            forecast_reliability_score
            if forecast_reliability_score is not None
            else valuation_result.forecast_reliability_score
        )
        reliability_state = classify_reliability(reliability)

        future_state = (forecast_direction or trend_state or "INSUFFICIENT_DATA").upper()
        revision = (forecast_revision_trend or "INSUFFICIENT_DATA").upper()
        market_trend = (market_result.trend_state or market_result.trend_alignment or "INSUFFICIENT_DATA").upper()
        market_momentum = (market_result.momentum_state or "INSUFFICIENT_DATA").upper()
        market_liquidity = (market_result.liquidity_state or "INSUFFICIENT_DATA").upper()

        if fundamental_state == "STRONG":
            pros.append(f"Fundamental quality is strong ({fund_score})")
        elif fundamental_state == "WEAK":
            cons.append(f"Fundamental quality is weak ({fund_score})")
        else:
            cons.append("Fundamental evidence is incomplete or not decisive")

        if is_positive_direction(future_state):
            pros.append("Future/fundamental direction is positive or improving")
        elif is_negative_direction(future_state):
            cons.append("Future/fundamental direction is negative or deteriorating")

        if valuation_state == "ATTRACTIVE":
            pros.append("Valuation is attractive")
        elif valuation_state == "EXPENSIVE":
            cons.append("Valuation is expensive")
        elif valuation_state in {"NOT_APPLICABLE", "INSUFFICIENT_DATA"}:
            conflicts.append("VALUATION_NOT_APPLICABLE" if valuation_state == "NOT_APPLICABLE" else "INSUFFICIENT_DATA")

        if reliability_state in {"LOW", "VERY_LOW"}:
            conflicts.append("POSITIVE_FORECAST_LOW_RELIABILITY")
            cons.append("Forecast reliability is too low for strong conviction")
        elif reliability_state == "HIGH":
            pros.append("Forecast reliability is high")

        if valuation_state == "ATTRACTIVE" and fundamental_state == "WEAK" and is_negative_direction(future_state):
            conflicts.append("CHEAP_BUT_WEAK")
        if valuation_state == "EXPENSIVE" and fundamental_state == "STRONG" and is_positive_direction(future_state):
            conflicts.append("STRONG_BUT_EXPENSIVE")
        if fundamental_state == "STRONG" and is_negative_direction(future_state):
            conflicts.append("STRONG_FUNDAMENTAL_NEGATIVE_FUTURE")
        if fundamental_state == "WEAK" and is_positive_direction(future_state):
            conflicts.append("TURNAROUND")

        if fundamental_state == "STRONG" and market_trend in {"DOWNTREND", "STRONG_DOWNTREND"}:
            conflicts.append("STRONG_FUNDAMENTAL_WEAK_MARKET")
        if fundamental_state == "WEAK" and market_trend in {"UPTREND", "STRONG_UPTREND"}:
            conflicts.append("WEAK_FUNDAMENTAL_STRONG_MARKET")
        if market_liquidity in {"LOW", "VERY_LOW"}:
            conflicts.append("LOW_LIQUIDITY")

        if usd_share_value_change_pct is not None:
            if usd_share_value_change_pct < 0:
                cons.append("USD share value is declining")
            elif usd_share_value_change_pct > 0 and fundamental_state == "WEAK":
                conflicts.append("POSITIVE_FX_NEGATIVE_FUNDAMENTAL")
                pros.append("USD share value context is positive")

        scenario_dispersion = valuation_result.metadata.get("scenario_dispersion") if valuation_result.metadata else None
        if isinstance(scenario_dispersion, (int, float)) and scenario_dispersion > 0.50:
            conflicts.append("HIGH_EXPECTED_UPSIDE_HIGH_BEAR_RISK")

        if market_trend in {"UPTREND", "STRONG_UPTREND"} and is_positive_direction(future_state):
            pros.append("Market context confirms the positive direction")
        elif market_trend in {"DOWNTREND", "STRONG_DOWNTREND"} and is_negative_direction(future_state):
            cons.append("Market context confirms the negative direction")

        confidence = 100.0
        missing_families = sum(
            [
                fundamental_state == "INSUFFICIENT_DATA",
                future_state == "INSUFFICIENT_DATA",
                valuation_state == "INSUFFICIENT_DATA",
                market_trend == "INSUFFICIENT_DATA",
            ]
        )
        confidence -= missing_families * 15.0
        if reliability_state == "VERY_LOW":
            confidence -= 30.0
        elif reliability_state == "LOW":
            confidence -= 15.0
        elif reliability_state == "MODERATE":
            confidence -= 5.0
        if valuation_result.valuation_risk_level in {"HIGH", "EXTREME"}:
            confidence -= 10.0
        if "HIGH_EXPECTED_UPSIDE_HIGH_BEAR_RISK" in conflicts:
            confidence -= 10.0
        if "LOW_LIQUIDITY" in conflicts:
            confidence -= 5.0
        confidence = round(max(0.0, min(100.0, confidence)), 2)

        positive_future = is_positive_direction(future_state)
        negative_future = is_negative_direction(future_state)
        attractive = valuation_state == "ATTRACTIVE"
        expensive = valuation_state == "EXPENSIVE"
        reliable_for_strong = reliability is not None and reliability >= 75

        if (
            fundamental_state == "STRONG"
            and positive_future
            and attractive
            and reliable_for_strong
            and confidence >= 75
            and not any(c in {"CHEAP_BUT_WEAK", "STRONG_BUT_EXPENSIVE", "POSITIVE_FORECAST_LOW_RELIABILITY", "HIGH_EXPECTED_UPSIDE_HIGH_BEAR_RISK", "VALUATION_NOT_APPLICABLE"} for c in conflicts)
        ):
            recommendation = "STRONG_BUY"
        elif (
            fundamental_state in {"STRONG", "ACCEPTABLE"}
            and positive_future
            and valuation_state in {"ATTRACTIVE", "FAIR"}
            and (reliability is None or reliability >= 60)
            and confidence >= 55
        ):
            recommendation = "BUY"
        elif (
            fundamental_state == "WEAK"
            and positive_future
            and attractive
            and reliability is not None
            and reliability >= 60
            and confidence >= 60
        ):
            recommendation = "BUY" if market_trend in {"UPTREND", "STRONG_UPTREND"} else "WATCH"
        elif (
            fundamental_state == "WEAK"
            and negative_future
            and expensive
            and reliable_for_strong
            and confidence >= 75
        ):
            recommendation = "STRONG_SELL"
        elif (
            (fundamental_state == "WEAK" and negative_future and "CHEAP_BUT_WEAK" not in conflicts)
            or (expensive and negative_future)
            or (valuation_state == "EXPENSIVE" and fundamental_state == "ACCEPTABLE")
        ):
            recommendation = "SELL"
        elif (
            (fundamental_state in {"STRONG", "ACCEPTABLE"} and expensive)
            or (fundamental_state == "STRONG" and negative_future)
        ):
            recommendation = "REDUCE" if fundamental_state != "STRONG" or negative_future else "HOLD"
        elif (
            "CHEAP_BUT_WEAK" in conflicts
            or "POSITIVE_FORECAST_LOW_RELIABILITY" in conflicts
            or fundamental_state == "INSUFFICIENT_DATA"
            or future_state == "INSUFFICIENT_DATA"
            or valuation_state in {"INSUFFICIENT_DATA", "NOT_APPLICABLE"}
        ):
            recommendation = "WATCH"
        else:
            recommendation = "HOLD"

        if recommendation == "BUY" and "STRONG_BUT_EXPENSIVE" in conflicts:
            recommendation = "HOLD"
        if recommendation == "STRONG_SELL" and reliability_state in {"LOW", "VERY_LOW"}:
            recommendation = "SELL"

        if recommendation in {"STRONG_BUY", "BUY"}:
            holding_status = (
                "STRONG_HOLD"
                if recommendation == "STRONG_BUY" and fundamental_state == "STRONG" and valuation_state in {"ATTRACTIVE", "FAIR"} and not negative_future
                else "HOLD_WITH_CAUTION" if negative_future or expensive
                else "HOLD"
            )
        elif recommendation == "HOLD":
            holding_status = "HOLD_WITH_CAUTION" if negative_future or expensive else "HOLD"
        elif recommendation in {"WATCH", "REDUCE"}:
            holding_status = "REVIEW_HOLD"
        else:
            holding_status = "EXIT_CANDIDATE"

        if valuation_state == "NOT_APPLICABLE":
            conflicts.append("VALUATION_NOT_APPLICABLE")
        conflicts = sorted(set(conflicts))

        data_quality = "VALID"
        if fundamental_result.score_data_quality not in {"VALID", ""}:
            data_quality = fundamental_result.score_data_quality
        if valuation_result.valuation_data_quality < 60 or market_result.market_data_quality not in {"VALID", ""}:
            data_quality = "LIMITED"

        evidence_summary = {
            "fundamental_quality": fundamental_state,
            "future_direction": future_state,
            "forecast_revision": revision,
            "forecast_reliability": reliability_state,
            "valuation": valuation_state,
            "market_trend": market_trend,
            "market_momentum": market_momentum,
            "market_regime": market_result.market_regime,
            "forecast_quality": forecast_quality or "UNKNOWN",
        }

        cutoff = data_cutoff_datetime or valuation_result.data_cutoff_datetime
        usd_context = dict(fx_context or {})
        usd_context["share_value_change_pct"] = usd_share_value_change_pct

        return FinalDecisionResult(
            company_id=company_id,
            period_id=period_id,
            recommendation=recommendation,
            holding_status=holding_status,
            decision_confidence=confidence,
            risk_level=valuation_result.valuation_risk_level or "MEDIUM",
            conflicts=conflicts,
            rationale_pros=pros,
            rationale_cons=cons,
            evidence_summary=evidence_summary,
            usd_context=usd_context,
            calculation_timestamp=datetime.utcnow(),
            model_version=MODEL_VERSION,
            contract_version=CONTRACT_VERSION,
            data_cutoff_datetime=cutoff,
            data_quality=data_quality,
            metadata={
                "architecture": "RULE_BASED_EVIDENCE_INTEGRATION",
                "market_score_used": False,
                "position_sizing_used": False,
                "upstream_recalculation": False,
                "fundamental_dominance": True,
                "double_counting_control": "FAMILY_LEVEL",
                "forecast_reliability_affects_confidence_only": True,
            },
        )
