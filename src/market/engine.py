from typing import List, Optional, Dict, Any
from datetime import datetime
from src.market.schema import TechnicalIndicatorsResult, MarketSignalResult
from src.market.indicators import calculate_sma, calculate_rsi

class MarketEngine:

    def analyze_market_signals(
        self,
        company_id: int,
        as_of_date: datetime,
        close_prices: List[float],
        individual_buy_vol: float = 0.0,
        individual_sell_vol: float = 0.0,
        close_price_today: float = 0.0
    ) -> MarketSignalResult:
        
        sma50 = calculate_sma(close_prices, 50)
        sma200 = calculate_sma(close_prices, 200)
        rsi = calculate_rsi(close_prices, 14)

        # ۱. وضعیت روند (Trend Alignment)
        if close_price_today > 0 and sma50 and sma200:
            if close_price_today > sma50 > sma200:
                trend = "BULLISH"
            elif close_price_today < sma50 < sma200:
                trend = "BEARISH"
            else:
                trend = "NEUTRAL"
        else:
            trend = "NEUTRAL"

        # ۲. وضعیت RSI
        if rsi is not None:
            if rsi <= 30.0:
                rsi_stat = "OVERSOLD"
            elif rsi >= 70.0:
                rsi_stat = "OVERBOUGHT"
            else:
                rsi_stat = "NEUTRAL"
        else:
            rsi_stat = "NEUTRAL"

        # ۳. ورود/خروج پول حقیقی
        net_flow = individual_buy_vol - individual_sell_vol
        money_flow = "INFLOW" if net_flow > 0 else ("OUTFLOW" if net_flow < 0 else "NEUTRAL")

        # ۴. محاسبه امتیاز تکنیکال (۰ تا ۱۰۰)
        tech_score = 50.0
        if trend == "BULLISH": tech_score += 25.0
        elif trend == "BEARISH": tech_score -= 25.0

        if rsi_stat == "OVERSOLD": tech_score += 15.0
        elif rsi_stat == "OVERBOUGHT": tech_score -= 15.0

        if money_flow == "INFLOW": tech_score += 10.0
        elif money_flow == "OUTFLOW": tech_score -= 10.0

        tech_score = max(0.0, min(100.0, tech_score))

        indicators = TechnicalIndicatorsResult(
            sma_50=sma50,
            sma_200=sma200,
            rsi_14=rsi,
            individual_net_buy_irr=net_flow
        )

        return MarketSignalResult(
            company_id=company_id,
            as_of_date=as_of_date,
            trend_alignment=trend,
            rsi_status=rsi_stat,
            money_flow_status=money_flow,
            technical_score=tech_score,
            indicators=indicators,
            calculation_timestamp=datetime.utcnow()
        )