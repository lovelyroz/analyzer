from typing import List, Optional, Tuple

def calculate_pe(forecast: float, actual: float) -> Optional[float]:
    """محاسبه درصد خطا (Percentage Error)"""
    if actual == 0:
        return None
    return ((forecast - actual) / abs(actual)) * 100.0

def calculate_mape(errors: List[float]) -> float:
    """محاسبه میانگین قدر مطلق درصد خطا (MAPE)"""
    if not errors:
        return 0.0
    abs_errors = [abs(e) for e in errors]
    return sum(abs_errors) / len(abs_errors)

def detect_persistent_bias(errors: List[float], threshold: float = 10.0) -> str:
    """
    تشخیص تورش سیستماتیک در پیش‌بینی‌ها
    اگر اکثر خطاها مثبت باشند -> بیش‌برآورد (OVERESTIMATING)
    اگر اکثر خطاها منفی باشند -> کم‌برآورد (UNDERESTIMATING)
    """
    if len(errors) < 3:
        return "NEUTRAL"
    
    avg_error = sum(errors) / len(errors)
    if avg_error > threshold:
        return "OVERESTIMATING"
    elif avg_error < -threshold:
        return "UNDERESTIMATING"
    
    return "NEUTRAL"