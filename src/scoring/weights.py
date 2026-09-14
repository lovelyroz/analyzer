from typing import Dict

# وزن دسته‌های اصلی به تفکیک نوع صنعت
CATEGORY_WEIGHTS: Dict[str, Dict[str, float]] = {
    "GENERAL": {
        "GROWTH": 0.35,
        "PROFITABILITY": 0.45,
        "RISK_QUALITY": 0.20,
    },
    "BANK": {
        "GROWTH": 0.25,
        "PROFITABILITY": 0.35,
        "RISK_QUALITY": 0.15,
        "INDUSTRY": 0.25,  # شاخص‌های تخصصی بانک
    },
    "INVESTMENT": {
        "GROWTH": 0.20,
        "PROFITABILITY": 0.30,
        "RISK_QUALITY": 0.10,
        "INDUSTRY": 0.40,  # شاخص‌های تخصصی هلدینگ / NAV
    }
}