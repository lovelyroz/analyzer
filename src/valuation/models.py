from statistics import median
from typing import Iterable, Optional


def calculate_forward_pe(eps_forecast: Optional[float], current_price: Optional[float]) -> Optional[float]:
    """Forward P/E = current market price / forecast EPS."""
    if eps_forecast is None or current_price is None or eps_forecast <= 0 or current_price <= 0:
        return None
    return current_price / eps_forecast


def calculate_forward_pe_fair_value(eps_forecast: Optional[float], target_pe: Optional[float]) -> Optional[float]:
    """Fair value from forecast EPS and target P/E."""
    if eps_forecast is None or target_pe is None or eps_forecast <= 0 or target_pe <= 0:
        return None
    return round(eps_forecast * target_pe, 2)


def calculate_nav_fair_value(nav_per_share: Optional[float], target_p_nav: float) -> Optional[float]:
    """Legacy helper retained for compatibility; not part of the Stage 7 V1 primary axis."""
    if nav_per_share is None or nav_per_share <= 0 or target_p_nav <= 0:
        return None
    return round(nav_per_share * target_p_nav, 2)


def calculate_margin_of_safety(fair_value: Optional[float], current_price: Optional[float]) -> Optional[float]:
    """Percentage upside/downside from current price to fair value."""
    if fair_value is None or current_price is None or current_price <= 0:
        return None
    return round(((fair_value - current_price) / current_price) * 100.0, 2)


def median_valid(values: Iterable[Optional[float]]) -> Optional[float]:
    valid = [value for value in values if value is not None and value == value and value > 0]
    return median(valid) if valid else None
