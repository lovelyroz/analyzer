from typing import Tuple

def map_score_to_recommendation(
    composite_score: float, 
    margin_of_safety: float
) -> Tuple[str, float]:
    """
    نگاشت امتیاز تلفیقی و حاشیه امنیت به توصیه نهایی و وزن پیشنهادی در پرتفوی
    """
    if composite_score >= 80.0 and margin_of_safety >= 25.0:
        return "STRONG_BUY", 10.0  # حداکثر ۱۰٪ تخصیص
    elif composite_score >= 65.0 and margin_of_safety >= 10.0:
        return "BUY", 6.0          # تخصیص ۶٪
    elif composite_score <= 35.0 or margin_of_safety <= -25.0:
        return "STRONG_SELL", 0.0  # خروج کامل
    elif composite_score <= 45.0 or margin_of_safety < -10.0:
        return "SELL", 0.0         # پیشنهاد فروش
    else:
        return "HOLD", 2.0         # نگهداری / وزن کم