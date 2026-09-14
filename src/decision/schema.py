from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class FinalDecisionResult:
    company_id: int
    period_id: int
    recommendation: str           # STRONG_BUY, BUY, HOLD, SELL, STRONG_SELL
    composite_score: float        # امتیاز تلفیقی ۰ تا ۱۰۰
    suggested_allocation_pct: float # درصد پیشنهادی از کل پرتفوی (مثلا ۰ تا ۱۰ درصد)
    risk_level: str               # LOW, MEDIUM, HIGH
    rationale_pros: List[str]     # دلایل مثبت پشتیبان سیگنال
    rationale_cons: List[str]     # دلایل منفی و ریسک‌های موجود
    model_version: str
    calculation_timestamp: datetime