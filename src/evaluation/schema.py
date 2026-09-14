from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime

@dataclass
class ForecastEvaluationResult:
    company_id: int
    period_id: int
    metric_code: str              # REVENUE, OPERATING_PROFIT, NET_PROFIT, EPS
    forecast_value: float
    actual_value: float
    error_amount: float           # Actual - Forecast
    percentage_error: float       # ((Forecast - Actual) / Actual) * 100
    absolute_percentage_error: float

@dataclass
class ReliabilityAssessment:
    company_id: int
    metric_code: str
    mape: float                   # Mean Absolute Percentage Error
    persistent_bias: str          # OVERESTIMATING, UNDERESTIMATING, NEUTRAL
    reliability_score: float      # امتیاز اعتبار ۰ تا ۱۰۰
    calibration_state: str        # NO_CALIBRATION, CALIBRATION_CANDIDATE, CALIBRATED
    underperforms_baseline: bool  # آیا از Baseline ساده‌تر ضعیف‌تر بوده؟
    calculation_timestamp: datetime