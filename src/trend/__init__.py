"""
Historical, Seasonal & Trend Engine (Stage 4)
"""

from src.trend.schema import ComparisonResult, TrendResult
from src.trend.utils import calculate_pct_change, is_low_base, is_sign_change
from src.trend.engine import TrendEngine

__all__ = [
    "ComparisonResult",
    "TrendResult",
    "calculate_pct_change",
    "is_low_base",
    "is_sign_change",
    "TrendEngine",
]