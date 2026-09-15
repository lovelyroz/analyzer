from typing import Optional, Sequence
from datetime import datetime
from src.trend.schema import ComparisonResult, TrendResult
from src.trend.utils import (
    calculate_pct_change,
    is_low_base,
    is_sign_change,
    relative_strength,
)


class TrendEngine:
    """Stage 4 historical direction engine.

    Fundamental scoring, forecasting, valuation and market signals are outside
    this engine. Historical relative strength is optional input because the
    engine itself does not own the historical data layer.
    """

    def evaluate_trend(
        self,
        company_id: int,
        period_id: int,
        metric_code: str,
        val_3m_curr: Optional[float], val_3m_prev: Optional[float],
        val_6m_curr: Optional[float], val_6m_prev: Optional[float],
        val_12m_curr: Optional[float], val_12m_prev: Optional[float],
        historical_3m: Optional[Sequence[float]] = None,
        historical_6m: Optional[Sequence[float]] = None,
        historical_12m: Optional[Sequence[float]] = None,
        historical_low_base_values: Optional[Sequence[float]] = None,
    ) -> TrendResult:
        changes = {
            "3M": calculate_pct_change(val_3m_curr, val_3m_prev),
            "6M": calculate_pct_change(val_6m_curr, val_6m_prev),
            "12M": calculate_pct_change(val_12m_curr, val_12m_prev),
        }
        histories = {
            "3M": historical_3m,
            "6M": historical_6m,
            "12M": historical_12m,
        }

        valid = {h: v for h, v in changes.items() if v is not None}
        if len(valid) < 2:
            state = "INSUFFICIENT_DATA"
            coverage = "INSUFFICIENT"
        else:
            coverage = "FULL" if len(valid) == 3 else "LIMITED"
            strengths = {h: relative_strength(v, histories[h]) for h, v in valid.items()}

            # Direction and relative strength are deliberately separate.
            # Direction comes from the sign of the current momentum; Strength
            # describes the magnitude relative to the same-horizon history.
            directions = {
                h: ("Positive" if v > 0 else "Negative" if v < 0 else "Weak")
                for h, v in valid.items()
            }

            positive = sum(d == "Positive" for d in directions.values())
            negative = sum(d == "Negative" for d in directions.values())
            all_positive = positive == len(valid)
            all_negative = negative == len(valid)
            all_weak_direction = all(directions[h] == "Weak" for h in valid)
            strong_positive = sum(
                directions[h] == "Positive" and strengths.get(h) == "Strong"
                for h in valid
            )
            strong_negative = sum(
                directions[h] == "Negative" and strengths.get(h) == "Strong"
                for h in valid
            )

            if all_positive and len(valid) == 3 and strong_positive >= 2:
                state = "Strong Improvement"
            elif all_negative and len(valid) == 3 and strong_negative >= 2:
                state = "Strong Deterioration"
            elif all_weak_direction or positive == negative:
                state = "Stable"
            elif positive > negative:
                state = "Improving"
            elif negative > positive:
                state = "Deteriorating"
            else:
                state = "Stable"

        comparisons = {
            h: ComparisonResult(
                h,
                changes[h],
                "VALID" if changes[h] is not None else "MISSING",
            )
            for h in ("3M", "6M", "12M")
        }

        # Stage 4 Low Base is based on comparable historical bases, not a
        # universal absolute threshold. If history is unavailable, UNKNOWN.
        low_base = is_low_base(
            val_3m_prev,
            historical_low_base_values,
        )

        return TrendResult(
            company_id=company_id,
            period_id=period_id,
            metric_code=metric_code,
            trend_state=state,
            coverage=coverage,
            low_base_flag=low_base,
            sign_change_flag=is_sign_change(val_3m_curr, val_3m_prev),
            comparisons=comparisons,
            calculation_timestamp=datetime.utcnow(),
        )
