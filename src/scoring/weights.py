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

# Industry KPI budget inside an affected axis. This is a redistribution budget,
# not an additive bonus. Universal weights are scaled to the remaining budget;
# industry KPIs share the industry budget equally within their mapped axis.
INDUSTRY_KPI_BUDGET = 0.20

# Industry KPI -> axis mapping. P/NAV remains valuation-only and is excluded.
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
}


def get_kpi_weights_for_industry(industry_code: str) -> Dict[str, Dict[str, float]]:
    """Return a complete Stage 3 KPI weighting profile for one industry.

    The universal profile is preserved for unaffected axes. On an affected axis,
    industry KPIs receive the fixed redistribution budget and universal KPIs are
    proportionally reduced. This guarantees each axis remains exactly 100%.
    """
    profile = {axis: dict(weights) for axis, weights in KPI_WEIGHTS.items()}
    mappings = INDUSTRY_KPI_AXES.get(industry_code, {})

    by_axis: Dict[str, list[str]] = {axis: [] for axis in AXIS_WEIGHTS}
    for code, axis in mappings.items():
        if axis in by_axis:
            by_axis[axis].append(code)

    for axis, industry_codes in by_axis.items():
        if not industry_codes:
            continue
        universal = profile[axis]
        remaining_budget = 1.0 - INDUSTRY_KPI_BUDGET
        profile[axis] = {
            code: weight * remaining_budget for code, weight in universal.items()
        }
        industry_weight = INDUSTRY_KPI_BUDGET / len(industry_codes)
        for code in industry_codes:
            profile[axis][code] = industry_weight

    return profile


# Backward-compatible name retained for existing imports.
CATEGORY_WEIGHTS = AXIS_WEIGHTS
