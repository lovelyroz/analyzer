from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class SingleForecastChain:
    """Forecast chain for one scenario."""
    revenue: Optional[float] = None
    operating_margin: Optional[float] = None
    operating_profit: Optional[float] = None
    net_profit: Optional[float] = None
    eps: Optional[float] = None
    roe: Optional[float] = None
    method: str = "INSUFFICIENT_DATA"
    quality: str = "INSUFFICIENT_DATA"
    assumptions: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ScenarioForecastResult:
    """Bear/Base/Bull forecast set."""
    bear: SingleForecastChain
    base: SingleForecastChain
    bull: SingleForecastChain


@dataclass
class CompanyForecastResult:
    company_id: int
    forecast_period_id: int
    horizon: str
    data_cutoff_datetime: datetime
    industry_code: str
    scenario_forecasts: ScenarioForecastResult
    baseline_method: str
    forecast_method: str
    model_version: str
    calculation_timestamp: datetime
    data_quality: str = "VALID"
    assumptions: Dict[str, Any] = field(default_factory=dict)
    benchmark: Optional[SingleForecastChain] = None

    @property
    def scenarios(self) -> ScenarioForecastResult:
        return self.scenario_forecasts


@dataclass
class ForecastInput:
    """Normalized input contract for Stage 5 calculations."""
    values: Dict[str, Any]

    def get(self, key: str, default: Any = None) -> Any:
        return self.values.get(key, default)

    def has(self, key: str) -> bool:
        return self.values.get(key) is not None


SUPPORTED_HORIZONS = ("1M", "3M", "6M", "12M")

NON_FINANCIAL_INDUSTRIES = {
    "PETROCHEMICAL", "CHEMICAL", "METALS", "MINING", "CEMENT",
    "FOOD", "PHARMACEUTICAL", "PHARMA"
}

FINANCIAL_INDUSTRIES = {"BANK", "INVESTMENT", "HOLDING"}
SUPPORTED_INDUSTRIES = NON_FINANCIAL_INDUSTRIES | FINANCIAL_INDUSTRIES
