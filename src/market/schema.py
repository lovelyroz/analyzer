from dataclasses import dataclass
from typing import Optional, Dict
from datetime import datetime

@dataclass
class TechnicalIndicatorsResult:
    sma_50: Optional[float]
    sma_200: Optional[float]
    rsi_14: Optional[float]
    individual_net_buy_irr: Optional[float]  # ورود/خروج پول حقیقی (ریال)

@dataclass
class MarketSignalResult:
    company_id: int
    as_of_date: datetime
    trend_alignment: str        # BULLISH, BEARISH, NEUTRAL
    rsi_status: str             # OVERSOLD, OVERBOUGHT, NEUTRAL
    money_flow_status: str      # INFLOW, OUTFLOW, NEUTRAL
    technical_score: float      # امتیاز تکنیکال ۰ تا ۱۰۰
    indicators: TechnicalIndicatorsResult
    calculation_timestamp: datetime