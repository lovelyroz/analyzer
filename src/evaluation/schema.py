from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class ForecastEvaluationResult:
    company_id: int
    period_id: int
    metric_code: str
    forecast_value: float
    actual_value: float
    error_amount: float
    percentage_error: Optional[float]
    absolute_percentage_error: Optional[float]
    horizon: str = "12M"
    model_version: str = "UNKNOWN"
    forecast_cutoff_datetime: Optional[datetime] = None
    actual_publication_datetime: Optional[datetime] = None
    regime_status: Optional[str] = None
    actual_report_version_id: Optional[int] = None
    point_in_time_valid: bool = True
    baseline_value: Optional[float] = None
    baseline_error_amount: Optional[float] = None
    baseline_percentage_error: Optional[float] = None
    baseline_absolute_percentage_error: Optional[float] = None
    duplicate_key: Optional[str] = None


@dataclass
class ReliabilityAssessment:
    company_id: int
    metric_code: str
    horizon: str
    model_version: str
    observation_count: int
    confidence_level: str
    mape: Optional[float]
    bias: Optional[float]
    persistent_bias: str
    baseline_mape: Optional[float]
    relative_improvement: Optional[float]
    model_underperforms_baseline: bool
    accuracy_score: float
    bias_score: float
    baseline_advantage_score: float
    performance_score: float
    reliability_score: float
    calibration_state: str
    calibration_reason: Optional[str] = None
    calculation_timestamp: datetime = field(default_factory=datetime.utcnow)
    model_parameters_version: str = "STAGE6_V1"
    metadata: Dict[str, Any] = field(default_factory=dict)

    # Compatibility with the original field name.
    @property
    def underperforms_baseline(self) -> bool:
        return self.model_underperforms_baseline
