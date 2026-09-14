from typing import Optional

def calculate_forward_pe_fair_value(eps_forecast: Optional[float], target_pe: float) -> Optional[float]:
    """محاسبه قیمت منصفانه بر اساس EPS پیش‌بینی‌شده و P/E تارگت"""
    if eps_forecast is None or eps_forecast <= 0:
        return None
    return round(eps_forecast * target_pe, 2)

def calculate_nav_fair_value(nav_per_share: Optional[float], target_p_nav: float) -> Optional[float]:
    """محاسبه قیمت منصفانه شرکت‌های سرمایه‌گذاری/هلدینگ با ضریب P/NAV"""
    if nav_per_share is None or nav_per_share <= 0:
        return None
    return round(nav_per_share * target_p_nav, 2)

def calculate_margin_of_safety(fair_value: float, current_price: float) -> float:
    """محاسبه حاشیه امنیت (Margin of Safety): درصد تفاوت ارزش منصفانه نسبت به قیمت بازار"""
    if current_price <= 0:
        return 0.0
    return round(((fair_value - current_price) / current_price) * 100.0, 2)