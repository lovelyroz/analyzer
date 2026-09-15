from typing import Optional, Tuple


DECISION_STATES = (
    "STRONG_BUY",
    "BUY",
    "HOLD",
    "WATCH",
    "REDUCE",
    "SELL",
    "STRONG_SELL",
)

HOLDING_STATES = (
    "STRONG_HOLD",
    "HOLD",
    "HOLD_WITH_CAUTION",
    "REVIEW_HOLD",
    "EXIT_CANDIDATE",
)


VALUATION_ATTRACTIVE = {"VERY_ATTRACTIVE", "ATTRACTIVE"}
VALUATION_EXPENSIVE = {"VERY_EXPENSIVE", "EXPENSIVE"}


def classify_fundamental(score: Optional[float]) -> str:
    if score is None:
        return "INSUFFICIENT_DATA"
    if score >= 70:
        return "STRONG"
    if score <= 40:
        return "WEAK"
    return "ACCEPTABLE"


def classify_reliability(score: Optional[float]) -> str:
    if score is None:
        return "INSUFFICIENT_DATA"
    if score >= 75:
        return "HIGH"
    if score >= 60:
        return "MODERATE"
    if score >= 40:
        return "LOW"
    return "VERY_LOW"


def classify_valuation(status: Optional[str]) -> str:
    status = str(status or "INSUFFICIENT_DATA").upper()
    if status in VALUATION_ATTRACTIVE:
        return "ATTRACTIVE"
    if status in VALUATION_EXPENSIVE:
        return "EXPENSIVE"
    if status in {"FAIR", "FAIRLY_VALUED", "FAIR_VALUE", "FAIRLY VALUED"}:
        return "FAIR"
    if status in {"NOT_APPLICABLE", "INSUFFICIENT_DATA"}:
        return status
    # Preserve future Stage 7 status names without inventing a new valuation rule.
    return status


def is_positive_direction(state: Optional[str]) -> bool:
    return str(state or "").upper() in {
        "STRONG_IMPROVEMENT", "IMPROVING", "POSITIVE", "STRONG_POSITIVE",
        "UPTREND", "STRONG_UPTREND", "ACCELERATING", "ABOVE_AVERAGE", "STRONG",
    }


def is_negative_direction(state: Optional[str]) -> bool:
    return str(state or "").upper() in {
        "STRONG_DETERIORATION", "DETERIORATING", "NEGATIVE", "STRONG_NEGATIVE",
        "DOWNTREND", "STRONG_DOWNTREND", "DECELERATING", "WEAK", "BELOW_AVERAGE",
    }


def map_score_to_recommendation(*args, **kwargs) -> Tuple[str, float]:
    """Legacy entry point retained without restoring the obsolete allocation model.

    Stage 9 V1 has no position sizing. Callers using the old weighted-score API
    receive a HOLD decision and zero allocation rather than the obsolete logic.
    """
    return "HOLD", 0.0
