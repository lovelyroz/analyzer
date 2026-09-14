from typing import Optional

def calculate_pct_change(current_val: Optional[float], prior_val: Optional[float]) -> Optional[float]:
    """
    محاسبه درصد تغییرات با رعایت قوانین عدم تقسیم بر صفر و عدم تغییر علامت کاذب
    """
    if current_val is None or prior_val is None:
        return None
    if prior_val == 0:
        return None
    
    return ((current_val - prior_val) / abs(prior_val)) * 100.0

def is_low_base(prior_val: Optional[float], threshold: float = 1.0) -> bool:
    """تشخیص پایه کوچک برای جلوگیری از خطای رشد هیجانی کاذب"""
    if prior_val is None:
        return False
    return abs(prior_val) < threshold

def is_sign_change(current_val: Optional[float], prior_val: Optional[float]) -> bool:
    """تشخیص تغییر وضعیت سود/زیان (Regime Change)"""
    if current_val is None or prior_val is None:
        return False
    return (current_val >= 0 and prior_val < 0) or (current_val < 0 and prior_val >= 0)