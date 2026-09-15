from dataclasses import dataclass
from typing import Optional, Dict, List
from datetime import datetime


@dataclass
class KPIScoreResult:
    kpi_code: str
    raw_value: Optional[float]
    score: Optional[float]
    weight: float
    effective_weight: float
    quality_status: str
    benchmark_method: str = "UNKNOWN"
    direction: str = "HIGHER_IS_BETTER"
    axis: str = "UNKNOWN"


@dataclass
class CategoryScoreResult:
    category_name: str
    score: Optional[float]
    weight: float
    coverage: float = 0.0


@dataclass
class FundamentalScoreResult:
    company_id: int
    period_id: int
    overall_score: Optional[float]
    category_scores: Dict[str, CategoryScoreResult]
    kpi_scores: List[KPIScoreResult]
    calculation_timestamp: datetime
    score_data_quality: str = "VALID"
    scoring_method_version: str = "STAGE3_V1"
