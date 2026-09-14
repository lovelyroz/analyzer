from typing import List, Optional

def calculate_sma(prices: List[float], window: int) -> Optional[float]:
    """محاسبه میانگین متحرک ساده (SMA)"""
    if len(prices) < window:
        return None
    return sum(prices[-window:]) / window

def calculate_rsi(prices: List[float], window: int = 14) -> Optional[float]:
    """محاسبه شاخص قدرت نسبی (RSI)"""
    if len(prices) < window + 1:
        return None
    
    gains = []
    losses = []
    for i in range(1, len(prices)):
        diff = prices[i] - prices[i - 1]
        if diff >= 0:
            gains.append(diff)
            losses.append(0.0)
        else:
            gains.append(0.0)
            losses.append(abs(diff))

    avg_gain = sum(gains[-window:]) / window
    avg_loss = sum(losses[-window:]) / window

    if avg_loss == 0:
        return 100.0
    
    rs = avg_gain / avg_loss
    return round(100.0 - (100.0 / (1.0 + rs)), 2)