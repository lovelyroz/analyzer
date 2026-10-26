from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional
import math

from src.core.jalali import JalaliDate


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
    # Jalali (year, month, day) market as-of date; never a Gregorian datetime.
    # Execution time lives separately in ``calculation_timestamp``.
    as_of_date: JalaliDate
    trend_alignment: str = "NEUTRAL"  # legacy field
    rsi_status: str = "NEUTRAL"  # legacy field; RSI is not Core V1
    money_flow_status: str = "NEUTRAL"  # legacy field
    technical_score: Optional[float] = None  # legacy field; Stage 8 V1 has no Market Score
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

def _number(val):
    if val is None:
        return None
    try:
        f = float(val)
    except (TypeError, ValueError):
        raise ValueError(f"Invalid numeric value: {val}")
    
    if not math.isfinite(f):
        raise ValueError(f"Non-finite numeric value (NaN/inf) is not permitted: {val}")
    
    return f

def _price(val):
    f = _number(val)
    if f is None or f <= 0:
        raise ValueError(f"Price must be a positive finite number: {val}")
    return f