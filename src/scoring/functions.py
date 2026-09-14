from typing import Optional

def min_max_scale(
    value: Optional[float], 
    min_val: float, 
    max_val: float, 
    reverse: bool = False
) -> Optional[float]:
    """
    نگاشت خطی مقدار عددی به بازه ۰ تا ۱۰۰
    اگر reverse=True باشد، مقادیر کمتر امتیاز بالاتری می‌گیرند (مانند ریسک یا NPL)
    """
    if value is None:
        return None
    
    # محدودسازی مقدار (Clamping) در بازه min و max
    clamped_val = max(min_val, min(max_val, value))
    
    if max_val == min_val:
        return 50.0

    score = ((clamped_val - min_val) / (max_val - min_val)) * 100.0
    
    if reverse:
        score = 100.0 - score
        
    return round(score, 2)