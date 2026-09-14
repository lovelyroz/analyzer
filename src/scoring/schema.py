from dataclasses import dataclass
from typing import Optional, Dict, List
from datetime import datetime

@dataclass
class KPIScoreResult:
    kpi_code: str
    raw_value: Optional[float]
    score: Optional[float]        # امتیاز نرمال‌شده بین ۰ تا ۱۰۰
    weight: float                 # وزن تخصیص‌یافته
    effective_weight: float       # وزن مؤثر پس از بازتوزیع داده‌های مفقود
    quality_status: str

@dataclass
class CategoryScoreResult:
    category_name: str            # GROWTH, PROFITABILITY, RISK_QUALITY, INDUSTRY
    score: Optional[float]        # امتیاز دسته بین ۰ تا ۱۰۰
    weight: float                 # وزن کل دسته

@dataclass
class FundamentalScoreResult:
    company_id: int
    period_id: int
    overall_score: Optional[float] # امتیاز نهایی بنیادی (۰ تا ۱۰۰)
    category_scores: Dict[str, CategoryScoreResult]
    kpi_scores: List[KPIScoreResult]
    calculation_timestamp: datetime