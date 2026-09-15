from typing import Dict

# Stage 3 fixed top-level axis weights.
AXIS_WEIGHTS: Dict[str, float] = {
    "GROWTH": 0.30,
    "PROFITABILITY": 0.45,
    "RISK_QUALITY": 0.25,
}

# Default universal KPI weights inside each axis.
KPI_WEIGHTS: Dict[str, Dict[str, float]] = {
    "GROWTH": {
        "REVENUE_GROWTH": 0.15,
        "OP_PROFIT_GROWTH": 0.25,
        "NET_PROFIT_GROWTH": 0.30,
        "EPS_GROWTH": 0.30,
    },
    "PROFITABILITY": {
        "GROSS_MARGIN": 0.10,
        "OPERATING_MARGIN": 0.25,
        "NET_MARGIN": 0.20,
        "ROA": 0.20,
        "ROE": 0.25,
    },
    "RISK_QUALITY": {
        "CASH_CONVERSION": 0.40,
        "EARNINGS_QUALITY": 0.60,
    },
}

# Financial Cost Pressure is diagnostic/adjustment candidate only in V1.
# Industry KPIs are mapped to existing axes; exact profiles can be versioned later.
INDUSTRY_KPI_AXES: Dict[str, Dict[str, str]] = {
    "BANK": {
        "BANK_LOAN_GROWTH": "GROWTH",
        "BANK_DEPOSIT_GROWTH": "GROWTH",
        "BANK_NII": "PROFITABILITY",
        "BANK_NIM": "PROFITABILITY",
        "BANK_NPL": "RISK_QUALITY",
    },
    "INVESTMENT": {
        "HOLDING_NAV": "PROFITABILITY",
        "HOLDING_NAV_GROWTH": "GROWTH",
        # P/NAV is valuation-linked and is therefore not part of the
        # Stage 3 score despite being a Stage 2 industry KPI.
        "HOLDING_P_NAV": "VALUATION_EXCLUDED",
    },
    "HOLDING": {
        "HOLDING_NAV": "PROFITABILITY",
        "HOLDING_NAV_GROWTH": "GROWTH",
        "HOLDING_P_NAV": "VALUATION_EXCLUDED",
    },
    "CEMENT": {"CEMENT_SALES_VOLUME": "GROWTH"},
    "FOOD": {"FOOD_SALES_VOLUME": "GROWTH"},
    "PHARMACEUTICAL": {"PHARMACEUTICAL_SALES_VOLUME": "GROWTH"},
    "PHARMA": {"PHARMACEUTICAL_SALES_VOLUME": "GROWTH"},
}

# Backward-compatible name retained for existing imports.
CATEGORY_WEIGHTS = AXIS_WEIGHTS
