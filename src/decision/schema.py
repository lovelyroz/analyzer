from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class FinalDecisionResult:
    """Stage 9 V1 decision and dashboard contract.

    Decision is a rule-based integration of upstream evidence. It is not a
    weighted score and does not contain position sizing.
    """
    company_id: int
    period_id: int
    recommendation: str
    holding_status: str
    decision_confidence: float
    risk_level: str
    fundamental_state: str = "INSUFFICIENT_DATA"
    fundamental_score: Optional[float] = None
    trend_state: str = "INSUFFICIENT_DATA"
    forecast_state: str = "INSUFFICIENT_DATA"
    forecast_reliability: Optional[float] = None
    valuation_status: str = "INSUFFICIENT_DATA"
    expected_upside: Optional[float] = None
    valuation_risk: Optional[str] = None
    valuation_confidence: Optional[float] = None
    market_trend_state: str = "INSUFFICIENT_DATA"
    market_momentum_state: str = "INSUFFICIENT_DATA"
    relative_strength_state: str = "INSUFFICIENT_DATA"
    liquidity_state: str = "INSUFFICIENT_DATA"
    fx_regime: Optional[str] = None
    fx_company_impact: Optional[str] = None
    usd_relative_valuation_context: Optional[str] = None
    free_market_fx: Optional[float] = None
    operational_fx: Optional[float] = None
    fx_gap: Optional[float] = None
    decision: Optional[str] = None
    decision_conflict: List[str] = field(default_factory=list)
    conflicts: List[str] = field(default_factory=list)
    rationale_pros: List[str] = field(default_factory=list)
    rationale_cons: List[str] = field(default_factory=list)
    evidence_summary: Dict[str, str] = field(default_factory=dict)
    usd_context: Dict[str, Optional[float]] = field(default_factory=dict)
    previous_decision: Optional[str] = None
    decision_change: Optional[str] = None
    decision_change_date: Optional[datetime] = None
    decision_change_reasons: List[str] = field(default_factory=list)
    decision_reasons: List[str] = field(default_factory=list)
    decision_risks: List[str] = field(default_factory=list)
    decision_ranking_eligibility: bool = False
    decision_rank_within_industry: Optional[int] = None
    ranking_inputs: Dict[str, object] = field(default_factory=dict)
    calculation_timestamp: datetime = field(default_factory=datetime.utcnow)
    decision_date: Optional[datetime] = None
    model_version: str = "STAGE9_V1"
    contract_version: str = "DECISION_CONTRACT_V1"
    data_cutoff_datetime: Optional[datetime] = None
    data_quality: str = "VALID"
    metadata: Dict[str, object] = field(default_factory=dict)

    # Backward-compatible aliases for the initial Stage 9 implementation.
    @property
    def ranking_eligibility(self) -> bool:
        return self.decision_ranking_eligibility

    @property
    def rank_within_industry(self) -> Optional[int]:
        return self.decision_rank_within_industry
