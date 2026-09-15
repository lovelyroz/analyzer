from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class TechnicalIndicatorsResult:
    sma_50: Optional[float] = None  # legacy compatibility
    sma_200: Optional[float] = None  # legacy compatibility
    rsi_14: Optional[float] = None  # legacy compatibility; not Core V1
    individual_net_buy_irr: Optional[float] = None  # legacy compatibility
    returns: Dict[str, Optional[float]] = field(default_factory=dict)
    price_position: Dict[str, Optional[float]] = field(default_factory=dict)
    price_vs_ma: Dict[str, Optional[float]] = field(default_factory=dict)
    volatility: Dict[str, Optional[float]] = field(default_factory=dict)
    max_drawdown: Dict[str, Optional[float]] = field(default_factory=dict)
    current_drawdown: Optional[float] = None
    distance_from_52w_high: Optional[float] = None
    volume_ratio: Optional[float] = None
    average_volume_20d: Optional[float] = None
    average_trading_value_20d: Optional[float] = None
    trading_value_stability_20d: Optional[float] = None


@dataclass
class MarketSignalResult:
    company_id: int
    as_of_date: datetime
    trend_alignment: str = "NEUTRAL"  # legacy field
    rsi_status: str = "NEUTRAL"  # legacy field; RSI is not Core V1
    money_flow_status: str = "NEUTRAL"  # legacy field
    technical_score: float = 50.0  # legacy field; Stage 8 V1 does not use Market Score
    indicators: TechnicalIndicatorsResult = field(default_factory=TechnicalIndicatorsResult)
    calculation_timestamp: Optional[datetime] = None
    trend_state: str = "INSUFFICIENT_DATA"
    trend_short: str = "INSUFFICIENT_DATA"
    trend_medium: str = "INSUFFICIENT_DATA"
    trend_long: str = "INSUFFICIENT_DATA"
    momentum_state: str = "INSUFFICIENT_DATA"
    momentum_acceleration: str = "INSUFFICIENT_DATA"
    volatility_state: str = "INSUFFICIENT_DATA"
    drawdown_state: str = "INSUFFICIENT_DATA"
    liquidity_state: str = "INSUFFICIENT_DATA"
    relative_strength_industry: str = "INSUFFICIENT_DATA"
    relative_strength_market: str = "INSUFFICIENT_DATA"
    market_regime: str = "INSUFFICIENT_DATA"
    price_volume_state: str = "INSUFFICIENT_DATA"
    alerts: List[str] = field(default_factory=list)
    market_data_quality: str = "VALID"
    market_contract_version: str = "MARKET_CONTRACT_V1"
    model_version: str = "STAGE8_V1"
    metadata: Dict[str, object] = field(default_factory=dict)
