"""Stage 4 to Stage 5 adapter (spec section 15, 16).

Stage 4 produces TrendResult evidence. Stage 5 consumes a flat
financial_context dict. This module is the translation boundary between the
two. It never recomputes a Stage 4 figure: every value is carried over or set
to a flag, and the only arithmetic is a sign test.

TrendResult.trend_state is a direction, not a growth rate, so it is carried as
context and never converted into a forecast growth rate (spec section 16).
Any Stage-4-to-forecast translation must come from an explicit
model_parameters["trend_adjustments"] entry, which the engine already owns.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from src.forecast.schema import ForecastInputRef, normalize_datetime
from src.trend.schema import TrendResult


@dataclass(frozen=True)
class Stage4Context:
    """Stage 4 evidence translated into the Stage 5 input contract.

    Frozen so a caller can build a financial context from it and be sure the
    evidence cannot be mutated after the forecast was made.
    """

    trend_state: Optional[str]
    coverage: Optional[str]
    seasonal_baseline_revenue: Optional[float]
    seasonality_valid: bool
    seasonal_data_sufficiency: Optional[str]
    seasonal_naive_revenue: Optional[float]
    recent_run_rate_revenue: Optional[float]
    trend_direction: Optional[str]
    momentum_12m_pct: Optional[float]
    momentum_12m_strength: Optional[str]
    low_base: bool
    sign_change: Optional[str]
    data_sufficiency: Optional[str]
    trend_confidence: Optional[str]
    provenance: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Merge into a Stage 5 financial_context.

        Missing evidence is carried as None or False and never coerced to zero
        or to a fabricated number (spec section 27).
        """
        return {
            "trend_state": self.trend_state,
            "trend_coverage": self.coverage,
            "trend_confidence": self.trend_confidence,
            "seasonal_baseline_revenue": self.seasonal_baseline_revenue,
            "seasonality_valid": self.seasonality_valid,
            "seasonal_data_sufficiency": self.seasonal_data_sufficiency,
            "seasonal_naive_revenue": self.seasonal_naive_revenue,
            "recent_run_rate_revenue": self.recent_run_rate_revenue,
            "trend_direction": self.trend_direction,
            "momentum_12m_pct": self.momentum_12m_pct,
            "momentum_12m_strength": self.momentum_12m_strength,
            "low_base": self.low_base,
            "sign_change": self.sign_change,
            "data_sufficiency": self.data_sufficiency,
            "stage4_provenance": self.provenance,
        }


def _num(value: Any) -> Optional[float]:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return float(value)


def _momentum_pct(result: TrendResult, horizon: str) -> Optional[float]:
    momentum = result.momentum.get(horizon) if result.momentum else None
    return _num(momentum.pct_change) if momentum is not None else None


def _momentum_strength(result: TrendResult, horizon: str) -> Optional[str]:
    momentum = result.momentum.get(horizon) if result.momentum else None
    return momentum.relative_strength if momentum is not None else None


def _sign_change(result: TrendResult) -> Optional[str]:
    """LOSS_TO_PROFIT / PROFIT_TO_LOSS / SIGN_CHANGE, else None (spec section 19)."""
    if result.context is not None and result.context.sign_change:
        return result.context.sign_change
    # No Layer-4 context: fall back to the layer-1/2 flag vocabulary.
    flags = set()
    if result.historical is not None:
        flags.update(
            comparison.flag
            for comparison in result.historical.same_period_detail
            if comparison.flag
        )
    if result.seasonal is not None and result.seasonal.flag:
        flags.add(result.seasonal.flag)
    for candidate in ("LOSS_TO_PROFIT", "PROFIT_TO_LOSS", "SIGN_CHANGE"):
        if candidate in flags:
            return candidate
    return None


def _provenance(result: TrendResult) -> Dict[str, Any]:
    return {
        "stage": "STAGE_4",
        "metric_code": result.metric_code,
        "period_id": result.period_id,
        "trend_coverage": result.trend_coverage or result.coverage,
        "trend_confidence": result.trend_confidence,
        "calculation_timestamp": (
            result.calculation_timestamp.isoformat()
            if result.calculation_timestamp is not None else None
        ),
        "seasonal_observations": (
            result.seasonal.observation_count
            if result.seasonal is not None else None
        ),
    }


def adapt_stage4(
    result: TrendResult,
    *,
    seasonal_baseline_revenue: Optional[float] = None,
    seasonal_naive_revenue: Optional[float] = None,
    recent_run_rate_revenue: Optional[float] = None,
    momentum_horizon: str = "12M",
) -> Stage4Context:
    """Translate one Stage 4 TrendResult into Stage 5 financial context.

    Stage 4 is metric-scoped, so the monetary baselines are supplied by the
    caller (they come from Stage 1 facts, not from the trend engine). The
    adapter only carries across the Stage 4 quantities that Stage 5 needs.

    Seasonality is valid only when Stage 4 reported enough same-period
    observations to compute a baseline (spec section 14): a seasonal baseline
    without sufficient history is not allowed to outrank the run rate.
    """
    seasonal = result.seasonal
    seasonal_baseline = _num(seasonal.baseline) if seasonal is not None else None

    seasonal_sufficient = (
        seasonal is not None
        and seasonal.data_sufficiency == "FULL"
        and seasonal_baseline is not None
    )

    momentum_pct = _momentum_pct(result, momentum_horizon)
    run_rate = _num(recent_run_rate_revenue)

    return Stage4Context(
        trend_state=result.trend_state,
        coverage=result.trend_coverage or result.coverage,
        seasonal_baseline_revenue=seasonal_baseline_revenue,
        seasonality_valid=seasonal_sufficient,
        seasonal_data_sufficiency=(
            seasonal.data_sufficiency if seasonal is not None else None
        ),
        seasonal_naive_revenue=seasonal_naive_revenue,
        recent_run_rate_revenue=run_rate,
        trend_direction=_trend_direction(result, momentum_pct),
        momentum_12m_pct=momentum_pct,
        momentum_12m_strength=_momentum_strength(result, momentum_horizon),
        low_base=bool(result.low_base_flag),
        sign_change=_sign_change(result),
        data_sufficiency=(
            result.context.data_sufficiency
            if result.context is not None else result.coverage
        ),
        trend_confidence=result.trend_confidence,
        provenance=_provenance(result),
    )


def _trend_direction(result: TrendResult, momentum_pct: Optional[float]) -> Optional[str]:
    """Direction of the latest trend evidence, as Stage 4 already determined it.

    This is a translation, not a recalculation: Stage 4's own momentum layer
    classified the sign; Stage 5 only reads it back.
    """
    momentum = result.momentum.get("12M") if result.momentum else None
    if momentum is not None and momentum.direction:
        return momentum.direction
    if result.trend_state == "INSUFFICIENT_DATA":
        return None
    if momentum_pct is None:
        return None
    if momentum_pct > 0:
        return "Positive"
    if momentum_pct < 0:
        return "Negative"
    return "Weak"


def build_financial_context(
    stage4: Optional[TrendResult],
    financial_facts: Optional[Dict[str, Any]] = None,
    *,
    seasonal_baseline_revenue: Optional[float] = None,
    seasonal_naive_revenue: Optional[float] = None,
    recent_run_rate_revenue: Optional[float] = None,
    input_refs: Optional[List[ForecastInputRef]] = None,
    momentum_horizon: str = "12M",
) -> Dict[str, Any]:
    """Assemble the Stage 5 financial_context from Stage 4 evidence and Stage 1 facts.

    Stage 4 evidence overrides nothing the caller already supplied: this is a
    merge, so a caller can pass a pre-built context and only have the Stage 4
    keys filled in.
    """
    context: Dict[str, Any] = dict(financial_facts or {})

    if stage4 is not None:
        stage4_context = adapt_stage4(
            stage4,
            seasonal_baseline_revenue=seasonal_baseline_revenue,
            seasonal_naive_revenue=seasonal_naive_revenue,
            recent_run_rate_revenue=recent_run_rate_revenue,
            momentum_horizon=momentum_horizon,
        )
        for key, value in stage4_context.to_dict().items():
            context.setdefault(key, value)

    if input_refs is not None:
        context.setdefault("input_refs", list(input_refs))

    return context
