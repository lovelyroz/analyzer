from typing import Dict

# P/E تاریخی/تارگت پیش‌فرض صنایع
INDUSTRY_TARGET_PE: Dict[str, float] = {
    "GENERAL": 7.0,
    "PETROCHEMICAL": 6.5,
    "METALS": 6.0,
    "FOOD": 8.0,
    "PHARMA": 8.5,
    "CEMENT": 7.5,
    "BANK": 5.0,
    "INVESTMENT": 0.70  # برای هلدینگ‌ها این ضریب P/NAV است
}

# وزن سناریوها برای محاسبه Expected Fair Value
SCENARIO_WEIGHTS: Dict[str, float] = {
    "bear": 0.20,
    "base": 0.60,
    "bull": 0.20,
}