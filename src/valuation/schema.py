from dataclasses import dataclass
from typing import Optional, Dict
from datetime import datetime

@dataclass
class ScenarioValuation:
    scenario_name: str           # Bear, Base, Bull
    target_pe: float
    eps_forecast: float
    fair_value: float
    upside_downside_pct: float   # درصد فاصله قیمت فعلی تا Fair Value سناریو

@dataclass
class ValuationResult:
    company_id: int
    period_id: int
    current_price: float
    expected_fair_value: float   # ارزش منصفانه وزنی
    margin_of_safety_pct: float  # حاشیه امنیت (درصد)
    valuation_status: str        # UNDERVALUED, FAIRLY_VALUED, OVERVALUED
    valuation_confidence: float  # امتیاز اطمینان ارزش‌گذاری (۰ تا ۱۰۰)
    valuation_risk_level: str    # LOW, MEDIUM, HIGH
    scenarios: Dict[str, ScenarioValuation]
    model_version: str
    calculation_timestamp: datetime