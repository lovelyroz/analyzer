from datetime import datetime
from statistics import pstdev
from typing import Any, Dict, List, Optional, Sequence

from src.market.indicators import (
    calculate_sma,
    cumulative_return,
    maximum_drawdown,
    price_position,
    realized_volatility,
    volume_ratio,
)
from src.market.parameters import (
    ABNORMAL_VOLUME_RATIO,
    AVERAGE_VOLUME_WINDOW,
    CONTRACT_VERSION,
    DISTANCE_FROM_52W_HIGH_WINDOW,
    DRAWDOWN_DEEP,
    DRAWDOWN_EXTREME,
    DRAWDOWN_NEAR_PEAK,
    DRAWDOWN_WINDOWS,
    LIQUIDITY_ACTIVE_DAY_MINIMUM,
    LIQUIDITY_HIGH_RELATIVE_VALUE,
    LIQUIDITY_LOW_RELATIVE_VALUE,
    MARKET_REGIME_RETURN_THRESHOLD,
    MA_WINDOWS,
    MODEL_VERSION,
    MOMENTUM_STRONG_RETURN,
    PRICE_POSITION_WINDOWS,
    PRICE_VOLUME_CONFIRMATION_RATIO,
    RECOVERY_FROM_LOW,
    RELATIVE_ABOVE_AVERAGE_GAP,
    RELATIVE_STRONG_RETURN_GAP,
    RETURN_HORIZONS,
    TRADING_VALUE_STABILITY_WINDOW,
    TREND_HORIZONS,
    TREND_STRONG_RETURN,
    VOLATILITY_EXTREME_RATIO,
    VOLATILITY_HIGH_RATIO,
    VOLATILITY_LOW_RATIO,
    VOLATILITY_WINDOWS,
)
from src.market.schema import MarketSignalResult, TechnicalIndicatorsResult


class MarketEngine:
    """Stage 8 V1 state engine. It describes market behavior; it does not score or decide."""

    def analyze_market(
        self,
        company_id: int,
        as_of_date: datetime,
        market_data: Sequence[Dict[str, Any]],
        *,
        industry_benchmark: Optional[Sequence[Dict[str, Any]]] = None,
        market_benchmark: Optional[Sequence[Dict[str, Any]]] = None,
        point_in_time: bool = True,
    ) -> MarketSignalResult:
        rows = self._prepare_rows(market_data, as_of_date, point_in_time)
        prices = [self._price(row) for row in rows]
        volumes = [self._number(row.get("volume")) for row in rows]
        values = [self._number(row.get("value")) for row in rows]
        if not rows or any(price is None for price in prices):
            return MarketSignalResult(
                company_id=company_id,
                as_of_date=as_of_date,
                calculation_timestamp=datetime.utcnow(),
                market_data_quality="INSUFFICIENT_DATA",
            )

        prices = [float(x) for x in prices]
        volumes = [float(x or 0.0) for x in volumes]
        values = [float(x or 0.0) for x in values]
        price_basis = "ADJUSTED_CLOSE" if all(row.get("adjusted_close") is not None for row in rows) else "CLOSE_FALLBACK"

        returns = {name: cumulative_return(prices, n) for name, n in RETURN_HORIZONS.items()}
        positions = {name: price_position(prices, n) for name, n in PRICE_POSITION_WINDOWS.items()}
        ma = {name: self._price_vs_ma(prices, n) for name, n in MA_WINDOWS.items()}
        vol = {name: realized_volatility(prices, n, annualized=True) for name, n in VOLATILITY_WINDOWS.items()}
        dd = {name: maximum_drawdown(prices, n) for name, n in DRAWDOWN_WINDOWS.items()}

        peak_52w = max(prices[-DISTANCE_FROM_52W_HIGH_WINDOW:]) if len(prices) >= DISTANCE_FROM_52W_HIGH_WINDOW else None
        distance_52w_high = prices[-1] / peak_52w - 1.0 if peak_52w else None
        peak = max(prices)
        current_dd = prices[-1] / peak - 1.0 if peak else None

        vr = volume_ratio(volumes, AVERAGE_VOLUME_WINDOW)
        avg_volume = self._average(volumes, AVERAGE_VOLUME_WINDOW)
        avg_value = self._average(values, AVERAGE_VOLUME_WINDOW)
        trading_value_stability = self._coefficient_of_variation(values, TRADING_VALUE_STABILITY_WINDOW)

        trend_short = self._trend_state(returns.get("20D"), ma.get("MA20"))
        trend_medium = self._trend_state(returns.get("60D"), ma.get("MA60"))
        trend_long = self._trend_state(returns.get("120D"), ma.get("MA120"))
        trend_state = self._combine_trend(trend_short, trend_medium, trend_long)
        momentum = self._momentum_state(returns.get("20D"), returns.get("60D"), returns.get("120D"))
        acceleration = self._acceleration(returns.get("20D"), returns.get("60D"))
        volatility_state = self._volatility_state(vol.get("20D"), vol.get("60D"))
        drawdown_state = self._drawdown_state(current_dd, prices)
        liquidity_state = self._liquidity_state(avg_value, values)
        industry_rs = self._relative_strength(returns, industry_benchmark, as_of_date)
        market_rs = self._relative_strength(returns, market_benchmark, as_of_date)
        market_regime = self._market_regime(market_benchmark, as_of_date)
        price_volume = self._price_volume_state(returns.get("20D"), vr)
        alerts = self._alerts(
            trend_state,
            momentum,
            volatility_state,
            drawdown_state,
            liquidity_state,
            vr,
            industry_rs,
            market_rs,
        )

        indicators = TechnicalIndicatorsResult(
            sma_50=calculate_sma(prices, 50),
            sma_200=calculate_sma(prices, 200),
            returns=returns,
            price_position=positions,
            price_vs_ma=ma,
            volatility=vol,
            max_drawdown=dd,
            current_drawdown=current_dd,
            distance_from_52w_high=distance_52w_high,
            volume_ratio=vr,
            average_volume_20d=avg_volume,
            average_trading_value_20d=avg_value,
            trading_value_stability_20d=trading_value_stability,
        )

        return MarketSignalResult(
            company_id=company_id,
            as_of_date=as_of_date,
            trend_alignment=trend_state,
            indicators=indicators,
            calculation_timestamp=datetime.utcnow(),
            trend_state=trend_state,
            trend_short=trend_short,
            trend_medium=trend_medium,
            trend_long=trend_long,
            momentum_state=momentum,
            momentum_acceleration=acceleration,
            volatility_state=volatility_state,
            drawdown_state=drawdown_state,
            liquidity_state=liquidity_state,
            relative_strength_industry=industry_rs,
            relative_strength_market=market_rs,
            market_regime=market_regime,
            price_volume_state=price_volume,
            alerts=alerts,
            market_data_quality="VALID",
            market_contract_version=CONTRACT_VERSION,
            model_version=MODEL_VERSION,
            metadata={
                "market_score": None,
                "decision_signal": None,
                "point_in_time": point_in_time,
                "as_of_date": as_of_date.isoformat(),
                "price_basis": price_basis,
                "distance_from_52w_high_window": DISTANCE_FROM_52W_HIGH_WINDOW,
                "trading_value_stability_definition": "20D coefficient_of_variation",
            },
        )

    def analyze_market_signals(
        self,
        company_id: int,
        as_of_date: datetime,
        close_prices: List[float],
        individual_buy_vol: float = 0.0,
        individual_sell_vol: float = 0.0,
        close_price_today: float = 0.0,
    ) -> MarketSignalResult:
        """Compatibility adapter for the pre-V1 API; no Market Score is produced by V1."""
        rows = [
            {
                "date": as_of_date,
                "adjusted_close": price,
                "close": price,
                "volume": 0.0,
                "value": 0.0,
            }
            for price in close_prices
        ]
        result = self.analyze_market(company_id, as_of_date, rows, point_in_time=False)
        result.money_flow_status = (
            "INFLOW"
            if individual_buy_vol > individual_sell_vol
            else ("OUTFLOW" if individual_buy_vol < individual_sell_vol else "NEUTRAL")
        )
        return result

    @staticmethod
    def _prepare_rows(
        data: Sequence[Dict[str, Any]], as_of_date: datetime, point_in_time: bool
    ) -> List[Dict[str, Any]]:
        rows = []
        for row in data:
            date = row.get("date")
            if isinstance(date, str):
                try:
                    date = datetime.fromisoformat(date)
                except ValueError:
                    continue
            if date is None:
                continue
            if point_in_time and date > as_of_date:
                continue
            rows.append(dict(row, date=date))
        return sorted(rows, key=lambda r: r["date"])

    @staticmethod
    def _price(row: Dict[str, Any]) -> Optional[float]:
        value = row.get("adjusted_close")
        if value is None:
            value = row.get("close")
        return float(value) if value is not None else None

    @staticmethod
    def _number(value: Any) -> Optional[float]:
        try:
            return float(value) if value is not None else None
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _average(values: List[float], window: int) -> Optional[float]:
        if len(values) < window:
            return None
        return sum(values[-window:]) / float(window)

    @staticmethod
    def _coefficient_of_variation(values: List[float], window: int) -> Optional[float]:
        if len(values) < window:
            return None
        sample = values[-window:]
        mean = sum(sample) / float(window)
        if mean <= 0:
            return None
        return pstdev(sample) / mean

    @staticmethod
    def _price_vs_ma(prices: List[float], window: int) -> Optional[float]:
        ma = calculate_sma(prices, window)
        return None if ma in (None, 0) else prices[-1] / ma - 1.0

    @staticmethod
    def _trend_state(ret: Optional[float], ma_gap: Optional[float]) -> str:
        if ret is None or ma_gap is None:
            return "INSUFFICIENT_DATA"
        if ret >= TREND_STRONG_RETURN and ma_gap > 0:
            return "STRONG_UPTREND"
        if ret > 0.0 and ma_gap > 0:
            return "UPTREND"
        if ret <= -TREND_STRONG_RETURN and ma_gap < 0:
            return "STRONG_DOWNTREND"
        if ret < 0.0 and ma_gap < 0:
            return "DOWNTREND"
        return "NEUTRAL"

    @staticmethod
    def _combine_trend(short: str, medium: str, long: str) -> str:
        states = [short, medium, long]
        if any(x == "INSUFFICIENT_DATA" for x in states):
            return "INSUFFICIENT_DATA"
        up = sum(x in ("UPTREND", "STRONG_UPTREND") for x in states)
        down = sum(x in ("DOWNTREND", "STRONG_DOWNTREND") for x in states)
        if up == 3 and all(x == "STRONG_UPTREND" for x in states):
            return "STRONG_UPTREND"
        if down == 3 and all(x == "STRONG_DOWNTREND" for x in states):
            return "STRONG_DOWNTREND"
        if up >= 2 and down == 0:
            return "UPTREND"
        if down >= 2 and up == 0:
            return "DOWNTREND"
        return "NEUTRAL"

    @staticmethod
    def _momentum_state(r20: Optional[float], r60: Optional[float], r120: Optional[float]) -> str:
        vals = [x for x in (r20, r60, r120) if x is not None]
        if len(vals) < 2:
            return "INSUFFICIENT_DATA"
        avg = sum(vals) / len(vals)
        if avg >= MOMENTUM_STRONG_RETURN:
            return "STRONG_POSITIVE"
        if avg > 0.0:
            return "POSITIVE"
        if avg <= -MOMENTUM_STRONG_RETURN:
            return "STRONG_NEGATIVE"
        if avg < 0.0:
            return "NEGATIVE"
        return "NEUTRAL"

    @staticmethod
    def _acceleration(r20: Optional[float], r60: Optional[float]) -> str:
        if r20 is None or r60 is None:
            return "INSUFFICIENT_DATA"
        short_rate = r20
        medium_rate = r60 / 3.0
        if short_rate > 0 and short_rate > medium_rate:
            return "ACCELERATING"
        if short_rate > 0 and short_rate < medium_rate:
            return "DECELERATING"
        if short_rate < 0 and short_rate < medium_rate:
            return "DECELERATING"
        if short_rate < 0 and short_rate > medium_rate:
            return "ACCELERATING"
        return "STABLE"

    @staticmethod
    def _volatility_state(v20: Optional[float], v60: Optional[float]) -> str:
        if v20 is None or v60 is None:
            return "INSUFFICIENT_DATA"
        ratio = v20 / v60 if v60 else 1.0
        if ratio >= VOLATILITY_EXTREME_RATIO:
            return "EXTREME"
        if ratio >= VOLATILITY_HIGH_RATIO:
            return "HIGH"
        if ratio <= VOLATILITY_LOW_RATIO:
            return "LOW"
        return "NORMAL"

    @staticmethod
    def _drawdown_state(current: Optional[float], prices: List[float]) -> str:
        if current is None or not prices:
            return "INSUFFICIENT_DATA"
        recent_low = min(prices[-20:])
        if current >= DRAWDOWN_NEAR_PEAK:
            return "NEAR_PEAK"
        if current <= DRAWDOWN_EXTREME and prices[-1] == recent_low:
            return "NEW_LOW"
        if current <= DRAWDOWN_DEEP:
            return "DEEP_DRAWDOWN"
        if len(prices) >= 2:
            previous_peak = max(prices[:-1])
            previous_dd = prices[-2] / previous_peak - 1.0 if previous_peak else None
            current_is_improving = previous_dd is not None and current > previous_dd
            recovered_from_recent_low = prices[-1] >= recent_low * (1.0 + RECOVERY_FROM_LOW)
            if current_is_improving and recovered_from_recent_low:
                return "RECOVERING"
        return "STABLE_DRAWDOWN"

    @staticmethod
    def _liquidity_state(avg_value: Optional[float], values: List[float]) -> str:
        if avg_value is None or avg_value <= 0:
            return "INSUFFICIENT_DATA"
        active = sum(v > 0 for v in values[-20:]) / min(20, len(values))
        if active < LIQUIDITY_ACTIVE_DAY_MINIMUM:
            return "VERY_LOW"
        baseline_values = [v for v in values[-60:] if v > 0]
        if not baseline_values:
            return "VERY_LOW"
        baseline = sum(baseline_values) / len(baseline_values)
        ratio = avg_value / baseline if baseline else 1.0
        if ratio >= LIQUIDITY_HIGH_RELATIVE_VALUE:
            return "HIGH"
        if ratio <= LIQUIDITY_LOW_RELATIVE_VALUE:
            return "LOW"
        return "NORMAL"

    def _relative_strength(
        self,
        stock_returns: Dict[str, Optional[float]],
        benchmark: Optional[Sequence[Dict[str, Any]]],
        as_of_date: datetime,
    ) -> str:
        if not benchmark:
            return "INSUFFICIENT_DATA"
        rows = self._prepare_rows(benchmark, as_of_date, True)
        prices = [self._price(r) for r in rows]
        if any(x is None for x in prices):
            return "INSUFFICIENT_DATA"
        bench = [float(x) for x in prices]
        r20 = stock_returns.get("20D")
        b20 = cumulative_return(bench, RETURN_HORIZONS["20D"])
        if r20 is None or b20 is None:
            return "INSUFFICIENT_DATA"
        diff = r20 - b20
        if diff >= RELATIVE_STRONG_RETURN_GAP:
            return "STRONG"
        if diff > RELATIVE_ABOVE_AVERAGE_GAP:
            return "ABOVE_AVERAGE"
        if diff <= -RELATIVE_STRONG_RETURN_GAP:
            return "WEAK"
        if diff < -RELATIVE_ABOVE_AVERAGE_GAP:
            return "BELOW_AVERAGE"
        return "NEUTRAL"

    @staticmethod
    def _market_regime(benchmark: Optional[Sequence[Dict[str, Any]]], as_of_date: datetime) -> str:
        if not benchmark:
            return "INSUFFICIENT_DATA"
        rows = []
        for row in benchmark:
            date = row.get("date")
            if isinstance(date, str):
                try:
                    date = datetime.fromisoformat(date)
                except ValueError:
                    continue
            if date is not None and date <= as_of_date:
                rows.append(dict(row, date=date))
        rows.sort(key=lambda r: r["date"])
        prices = [
            float(r.get("adjusted_close", r.get("close")))
            for r in rows
            if r.get("adjusted_close", r.get("close")) is not None
        ]
        r20 = cumulative_return(prices, RETURN_HORIZONS["20D"])
        if r20 is None:
            return "INSUFFICIENT_DATA"
        if r20 >= MARKET_REGIME_RETURN_THRESHOLD:
            return "MARKET_UP"
        if r20 <= -MARKET_REGIME_RETURN_THRESHOLD:
            return "MARKET_DOWN"
        return "MARKET_NEUTRAL"

    @staticmethod
    def _price_volume_state(r20: Optional[float], vr: Optional[float]) -> str:
        if r20 is None or vr is None:
            return "INSUFFICIENT_DATA"
        if r20 > 0 and vr >= PRICE_VOLUME_CONFIRMATION_RATIO:
            return "PRICE_VOLUME_CONFIRMATION"
        if r20 > 0:
            return "WEAK_PRICE_VOLUME_CONFIRMATION"
        if r20 < 0 and vr >= PRICE_VOLUME_CONFIRMATION_RATIO:
            return "DOWN_MOVE_VOLUME_CONFIRMATION"
        return "NEUTRAL"

    @staticmethod
    def _alerts(
        trend: str,
        momentum: str,
        volatility: str,
        drawdown: str,
        liquidity: str,
        vr: Optional[float],
        industry_rs: str,
        market_rs: str,
    ) -> List[str]:
        alerts = []
        if volatility in ("HIGH", "EXTREME"):
            alerts.append("WARNING:HIGH_VOLATILITY")
        if liquidity in ("LOW", "VERY_LOW"):
            alerts.append("WARNING:LOW_LIQUIDITY")
        if drawdown in ("DEEP_DRAWDOWN", "NEW_LOW"):
            alerts.append("WARNING:DEEP_DRAWDOWN")
        if vr is not None and vr >= ABNORMAL_VOLUME_RATIO:
            alerts.append("INFO:ABNORMAL_VOLUME")
        if industry_rs == "WEAK" or market_rs == "WEAK":
            alerts.append("WATCH:WEAK_RELATIVE_STRENGTH")
        if trend == "STRONG_DOWNTREND" and momentum == "STRONG_NEGATIVE":
            alerts.append("WARNING:STRONG_NEGATIVE_MARKET_STATE")
        return sorted(set(alerts))
