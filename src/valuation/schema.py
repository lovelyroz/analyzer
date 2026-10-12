from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class ScenarioValuation:
    scenario_name: str
    target_pe: Optional[float]
    eps_forecast: Optional[float]
    forward_pe: Optional[float]
    fair_value: Optional[float]
    upside_downside_pct: Optional[float]
    probability: float = 0.0
    flags: List[str] = field(default_factory=list)


@dataclass
class ValuationResult:
    company_id: int
    period_id: int
    current_price: float
    expected_fair_value: Optional[float]
    margin_of_safety_pct: Optional[float]
    valuation_status: str
    valuation_confidence: float
    valuation_risk_level: str
    scenarios: Dict[str, ScenarioValuation]
    model_version: str
    calculation_timestamp: datetime
    valuation_date: Optional[datetime] = None
    market_price_date: Optional[datetime] = None
    data_cutoff_datetime: Optional[datetime] = None
    target_pe_source: str = "INSUFFICIENT_DATA"
    historical_median_pe: Optional[float] = None
    industry_forward_pe_median: Optional[float] = None
    industry_ttm_pe_median: Optional[float] = None
    industry_peer_count: int = 0
    forecast_reliability_score: Optional[float] = None
    probability_confidence: float = 0.0
    valuation_confidence_label: str = "INSUFFICIENT_DATA"
    valuation_risk_flags: List[str] = field(default_factory=list)
    alerts: List[str] = field(default_factory=list)
    valuation_driver_ranking: List[str] = field(default_factory=list)
    driver_impact: Dict[str, float] = field(default_factory=dict)
    driver_uncertainty: Dict[str, float] = field(default_factory=dict)
    review_priority: Dict[str, float] = field(default_factory=dict)
    valuation_data_quality: float = 0.0
    contract_version: str = "VALUATION_CONTRACT_V1"
    metadata: Dict[str, object] = field(default_factory=dict)
