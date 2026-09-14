from dataclasses import dataclass
from typing import Optional, Dict
from datetime import datetime

@dataclass
class ComparisonResult:
    horizon: str                  # MoM, QoQ, YoY, 3M, 6M, 12M
    pct_change: Optional[float]   # درصد تغییرات
    status: str                   # STRONG_IMPROVEMENT, IMPROVING, STABLE, DETERIORATING, STRONG_DETERIORATION, INSUFFICIENT_DATA

@dataclass
class TrendResult:
    company_id: int
    period_id: int
    metric_code: str
    trend_state: str              # Strong Improvement, Improving, Stable, Deteriorating, Strong Deterioration, Mixed, INSUFFICIENT_DATA
    coverage: str                 # FULL, LIMITED, INSUFFICIENT
    low_base_flag: bool           # هشدار base کوچک
    sign_change_flag: bool        # هشدار تغییر علامت (زیان به سود یا بالعکس)
    comparisons: Dict[str, ComparisonResult]
    calculation_timestamp: datetime