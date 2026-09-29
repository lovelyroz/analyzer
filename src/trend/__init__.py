"""
Historical, Seasonal & Trend Engine (Stage 4)
"""

from src.trend.schema import (
    ComparisonResult,
    ContextFlags,
    HistoricalResult,
    MomentumResult,
    PeriodComparison,
    SeasonalResult,
    TrendResult,
)
from src.trend.utils import (
    calculate_pct_change,
    classify_direction,
    detect_one_off,
    determine_trend_state,
    flow_momentum,
    historical_percentile_abs,
    is_low_base,
    is_sign_change,
    is_zero_base,
    momentum_history,
    multi_year_trend,
    relative_strength,
    same_period_multi_year,
    seasonal_baseline,
    seasonal_surprise,
    sign_change_kind,
    stock_momentum,
    trend_12m,
)
from src.trend.engine import TrendEngine

__all__ = [
    "ComparisonResult",
    "ContextFlags",
    "HistoricalResult",
    "MomentumResult",
    "PeriodComparison",
    "SeasonalResult",
    "TrendResult",
    "calculate_pct_change",
    "classify_direction",
    "detect_one_off",
    "determine_trend_state",
    "flow_momentum",
    "historical_percentile_abs",
    "is_low_base",
    "is_sign_change",
    "is_zero_base",
    "momentum_history",
    "multi_year_trend",
    "relative_strength",
    "same_period_multi_year",
    "seasonal_baseline",
    "seasonal_surprise",
    "sign_change_kind",
    "stock_momentum",
    "trend_12m",
    "TrendEngine",
]
