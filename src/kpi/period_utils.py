from typing import List, Optional

def calculate_ttm(quarterly_values: List[float]) -> Optional[float]:
    """محاسبه مجموع ۴ کوارتر اخیر (TTM) برای اقلام جریانی (FLOW)"""
    if len(quarterly_values) < 4 or any(v is None for v in quarterly_values):
        return None
    return sum(quarterly_values[-4:])

def calculate_yoy_growth(current_val: Optional[float], prior_val: Optional[float]) -> Optional[float]:
    """محاسبه درصد رشد سالانه (YoY)"""
    if current_val is None or prior_val is None or prior_val == 0:
        return None
    return ((current_val - prior_val) / abs(prior_val)) * 100.0