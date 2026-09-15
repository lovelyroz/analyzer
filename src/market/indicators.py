from math import sqrt
from statistics import mean, pstdev
from typing import List, Optional


def calculate_sma(prices: List[float], window: int) -> Optional[float]:
    if window <= 0 or len(prices) < window:
        return None
    return sum(prices[-window:]) / window


def calculate_rsi(prices: List[float], window: int = 14) -> Optional[float]:
    """Legacy helper retained for compatibility; RSI is excluded from Stage 8 Core V1."""
    if len(prices) < window + 1:
        return None
    gains, losses = [], []
    for i in range(1, len(prices)):
        diff = prices[i] - prices[i - 1]
        gains.append(max(diff, 0.0))
        losses.append(max(-diff, 0.0))
    avg_gain = sum(gains[-window:]) / window
    avg_loss = sum(losses[-window:]) / window
    if avg_loss == 0:
        return 100.0
    return round(100.0 - (100.0 / (1.0 + avg_gain / avg_loss)), 2)


def cumulative_return(prices: List[float], horizon: int) -> Optional[float]:
    if len(prices) <= horizon or prices[-1] is None or prices[-1 - horizon] in (None, 0):
        return None
    return prices[-1] / prices[-1 - horizon] - 1.0


def price_position(prices: List[float], window: int) -> Optional[float]:
    if len(prices) < window:
        return None
    values = prices[-window:]
    lo, hi = min(values), max(values)
    if hi == lo:
        return None
    return (values[-1] - lo) / (hi - lo)


def realized_volatility(prices: List[float], window: int, annualized: bool = True) -> Optional[float]:
    if len(prices) < window + 1:
        return None
    returns = [prices[i] / prices[i - 1] - 1.0 for i in range(len(prices) - window, len(prices)) if prices[i - 1] != 0]
    if len(returns) < 2:
        return None
    value = pstdev(returns)
    return value * sqrt(252.0) if annualized else value


def maximum_drawdown(prices: List[float], window: int) -> Optional[float]:
    if len(prices) < window:
        return None
    values = prices[-window:]
    peak = values[0]
    worst = 0.0
    for value in values:
        peak = max(peak, value)
        if peak != 0:
            worst = min(worst, value / peak - 1.0)
    return worst


def volume_ratio(volumes: List[float], window: int = 20) -> Optional[float]:
    if len(volumes) < window + 1:
        return None
    avg = mean(volumes[-window - 1:-1])
    if avg == 0:
        return None
    return volumes[-1] / avg
