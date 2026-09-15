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
    conflicts: List[str] = field(default_factory=list)
    rationale_pros: List[str] = field(default_factory=list)
    rationale_cons: List[str] = field(default_factory=list)
    evidence_summary: Dict[str, str] = field(default_factory=dict)
    usd_context: Dict[str, Optional[float]] = field(default_factory=dict)
    calculation_timestamp: datetime = field(default_factory=datetime.utcnow)
    model_version: str = "STAGE9_V1"
    contract_version: str = "DECISION_CONTRACT_V1"
    data_cutoff_datetime: Optional[datetime] = None
    data_quality: str = "VALID"
    metadata: Dict[str, object] = field(default_factory=dict)
