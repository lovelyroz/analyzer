from dataclasses import dataclass, field
from typing import Optional, Dict, List, Tuple
from datetime import datetime

# Stage 4 trend states (specification section 13).
TREND_STATES = (
    "Strong Improvement",
    "Improving",
    "Stable",
    "Deteriorating",
    "Strong Deterioration",
    "INSUFFICIENT_DATA",
)

# Coverage / confidence of the trend state (specification section 14).
COVERAGE_LEVELS = ("FULL", "LIMITED", "INSUFFICIENT")


@dataclass
class ComparisonResult:
    horizon: str                  # MoM, QoQ, YoY, 3M, 6M, 12M
    pct_change: Optional[float]   # درصد تغییرات
    status: str                   # VALID, MISSING


@dataclass
class PeriodComparison:
    """One historical comparison with its contextual caveat.

    `flag` is set only when the percentage change is not expressible, using
    the specification's ZERO_BASE / SIGN_CHANGE / LOSS_TO_PROFIT /
    PROFIT_TO_LOSS / MISSING / LOW_BASE vocabulary.
    """
    label: str
    pct_change: Optional[float]
    flag: Optional[str] = None


@dataclass
class HistoricalResult:
    """Layer 1 - Historical Comparison.

    Same-period multi-year is exposed both as an ordered detail list and in
    summary form, so the most recent and the average same-period reading are
    individually distinguishable without walking the detail list.

    `period_months` records the granularity of the series the calendar
    comparisons were resolved against: on a quarterly series a one-month lag
    has no distinct observation and MoM degenerates to the previous quarter,
    so a consumer must read `period_months` to interpret MoM correctly.

    `sufficiency` is FULL when all three calendar comparisons (MoM, QoQ, YoY)
    resolved, LIMITED when at least one did, and INSUFFICIENT when none did.
    """
    mom: Optional[float] = None
    qoq: Optional[float] = None
    yoy: Optional[float] = None
    same_period_detail: List[PeriodComparison] = field(default_factory=list)
    same_period_latest: Optional[float] = None
    same_period_average: Optional[float] = None
    multi_year_trend: Optional[float] = None
    period_months: int = 1
    sufficiency: str = "INSUFFICIENT"


@dataclass
class SeasonalResult:
    """Layer 2 - Seasonal Analysis."""
    baseline: Optional[float] = None
    surprise: Optional[float] = None
    # FULL when at least 3 valid same-period observations exist, otherwise
    # INSUFFICIENT_DATA per specification section 5.
    data_sufficiency: str = "INSUFFICIENT_DATA"
    observation_count: int = 0
    flag: Optional[str] = None


@dataclass
class MomentumResult:
    """Layer 3 - Momentum / Trend for one horizon.

    Direction and relative strength are deliberately separate fields:
    direction is magnitude-vs-zero only, while strength is the
    company-relative percentile of absolute momentum.
    """
    pct_change: Optional[float] = None
    direction: Optional[str] = None        # Positive / Negative / Weak
    relative_strength: Optional[str] = None  # Weak / Normal / Strong
    percentile: Optional[float] = None
    status: str = "MISSING"


@dataclass
class ContextFlags:
    """Layer 4 - Context Flags (specification section 19 Context block)."""
    low_base: Optional[bool] = None        # True / False / None(UNKNOWN)
    sign_change: Optional[str] = None      # LOSS_TO_PROFIT / PROFIT_TO_LOSS / SIGN_CHANGE
    zero_base: bool = False
    one_off: bool = False
    one_off_reason: Optional[str] = None
    data_quality: str = "OK"               # OK / MISSING_INPUT / INSUFFICIENT_HISTORY
    data_sufficiency: str = "INSUFFICIENT"  # FULL / LIMITED / INSUFFICIENT


@dataclass
class TrendResult:
    company_id: int
    period_id: int
    metric_code: str
    trend_state: str              # Strong Improvement, Improving, Stable, Deteriorating, Strong Deterioration, INSUFFICIENT_DATA
    coverage: str                 # FULL, LIMITED, INSUFFICIENT
    low_base_flag: Optional[bool] # True / False / None(UNKNOWN)
    sign_change_flag: bool        # هشدار تغییر علامت
    comparisons: Dict[str, ComparisonResult]
    calculation_timestamp: datetime
    # --- Layer 1: Historical Comparison ---
    historical: Optional[HistoricalResult] = None
    # --- Layer 2: Seasonal Analysis ---
    seasonal: Optional[SeasonalResult] = None
    # --- Layer 3: Momentum / Trend, keyed by horizon (3M, 6M, 12M) ---
    momentum: Dict[str, MomentumResult] = field(default_factory=dict)
    # --- Layer 4: Context Flags ---
    context: Optional[ContextFlags] = None
    # Derived from `coverage`: FULL / LIMITED / INSUFFICIENT.
    trend_coverage: Optional[str] = None
    # HIGH when all three horizons are valid, MEDIUM for two, otherwise LOW.
    trend_confidence: Optional[str] = None
