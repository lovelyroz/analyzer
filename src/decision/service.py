"""Reusable orchestration boundary from Jalali-priced valuation to Stage 9."""

from dataclasses import dataclass
from typing import Any, Dict, Optional

from sqlalchemy.orm import Session

from src.decision.engine import DecisionEngine
from src.decision.schema import FinalDecisionResult
from src.forecast.schema import CompanyForecastResult
from src.ingestion.market.queries import JalaliDate
from src.market.schema import MarketSignalResult
from src.scoring.schema import FundamentalScoreResult
from src.valuation.schema import ValuationResult
from src.valuation.service import calculate_valuation_as_of_jalali


@dataclass(frozen=True)
class ValuationDecisionResult:
    """Keep both upstream valuation and downstream decision available."""

    valuation: ValuationResult
    decision: FinalDecisionResult


def calculate_decision_as_of_jalali(
    session: Session,
    forecast_result: CompanyForecastResult,
    as_of_jalali_date: JalaliDate,
    fundamental_result: FundamentalScoreResult,
    market_result: MarketSignalResult,
    *,
    forecast_reliability_score: Optional[float] = None,
    valuation_options: Optional[Dict[str, Any]] = None,
    decision_options: Optional[Dict[str, Any]] = None,
) -> ValuationDecisionResult:
    """Value from a Stage 5 result and feed that same result into Stage 9.

    Forecast generation/retrieval and Stage 3/8 evidence production remain
    with their existing callers; this boundary refuses mixed identities.
    """
    company_id = forecast_result.company_id
    period_id = forecast_result.forecast_period_id
    if fundamental_result.company_id != company_id or fundamental_result.period_id != period_id:
        raise ValueError("fundamental result identity does not match forecast")
    if market_result.company_id != company_id:
        raise ValueError("market result company_id does not match forecast")

    valuation_kwargs = dict(valuation_options or {})
    if "forecast_reliability_score" in valuation_kwargs:
        raise TypeError("forecast_reliability_score must be supplied once to the orchestration service")
    decision_kwargs = dict(decision_options or {})
    if "forecast_reliability_score" in decision_kwargs:
        raise TypeError("forecast_reliability_score must be supplied once to the orchestration service")

    valuation = calculate_valuation_as_of_jalali(
        session,
        company_id,
        period_id,
        forecast_result,
        as_of_jalali_date,
        forecast_reliability_score=forecast_reliability_score,
        **valuation_kwargs,
    )
    decision = DecisionEngine().make_decision(
        company_id,
        period_id,
        fundamental_result,
        valuation,
        market_result,
        forecast_reliability_score,
        **decision_kwargs,
    )
    return ValuationDecisionResult(valuation=valuation, decision=decision)
