from dataclasses import dataclass
from typing import Optional, Dict
from datetime import datetime

@dataclass
class SingleForecastChain:
    """زنجیره مالی پیش‌بینی‌شده برای یک سناریوی خاص"""
    revenue: Optional[float]
    operating_profit: Optional[float]
    net_profit: Optional[float]
    eps: Optional[float]

@dataclass
class ScenarioForecastResult:
    """خروجی ۳ سناریوی اصلی پیش‌بینی (Bear / Base / Bull)"""
    bear: SingleForecastChain
    base: SingleForecastChain
    bull: SingleForecastChain

@dataclass
class CompanyForecastResult:
    company_id: int
    forecast_period_id: int
    data_cutoff_datetime: datetime
    industry_code: str
    scenario_forecasts: ScenarioForecastResult
    forecast_method: str          # RUN_RATE, SEASONAL_BASELINE, DRIVER_BASED
    model_version: str
    calculation_timestamp: datetime