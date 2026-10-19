from src.valuation.engine import ValuationEngine
from src.tests.test_stage7_valuation import make_forecast

def make_forecast(eps_bear=150.0, eps_base=180.0, eps_bull=210.0):
    from datetime import datetime
    from src.forecast.schema import CompanyForecastResult, ForecastInputRef, ScenarioForecastResult, SingleForecastChain
    return CompanyForecastResult(
        company_id=1,
        forecast_period_id=101,
        data_cutoff_datetime=datetime(2026, 1, 1),
        industry_code="PETROCHEMICAL",
        scenario_forecasts=ScenarioForecastResult(
            bear=SingleForecastChain(1000.0, 200.0, eps_bear, eps_bear),
            base=SingleForecastChain(1200.0, 240.0, eps_base, eps_base),
            bull=SingleForecastChain(1400.0, 280.0, eps_bull, eps_bull),
        ),
        forecast_method="DRIVER_BASED",
        model_version="V1.0",
        calculation_timestamp=datetime(2026, 1, 1),
    )

engine = ValuationEngine()

print("=== flip_base ===")
flip_base = engine.calculate_valuation(
    1, 101, "PETROCHEMICAL", 1000.0,
    make_forecast(150.0, 150.0, 250.0), historical_pe_values=[7.0],
)
print(f"Status: {flip_base.valuation_status}")
print(f"Alerts: {flip_base.alerts}")
print(f"Risk flags: {flip_base.valuation_risk_flags}")

print("\n=== shocked ===")
shocked = engine.calculate_valuation(
    1, 101, "PETROCHEMICAL", 1000.0,
    make_forecast(135.0, 135.0, 225.0), historical_pe_values=[7.0],
)
print(f"Status: {shocked.valuation_status}")
print(f"Alerts: {shocked.alerts}")
print(f"Risk flags: {shocked.valuation_risk_flags}")

print("\n=== stable ===")
stable = engine.calculate_valuation(
    1, 101, "PETROCHEMICAL", 1000.0, make_forecast(180.0, 180.0, 180.0),
    historical_pe_values=[7.0],
    scenario_pe_adjustments={"bear": -0.10, "base": 0.0, "bull": 0.20},
    scenario_pe_rationales={
        "bear": "Higher risk compresses justified multiple.",
        "base": "Historical median is neutral.",
        "bull": "Better quality supports premium.",
    },
)
print(f"Status: {stable.valuation_status}")
print(f"Alerts: {stable.alerts}")
print(f"Risk flags: {stable.valuation_risk_flags}")

print("\n=== eps_risk ===")
eps_risk = engine.calculate_valuation(
    1, 101, "PETROCHEMICAL", 1000.0, make_forecast(80.0, 180.0, 320.0),
    forecast_reliability_score=20.0, historical_pe_values=[7.0],
    probability_confidence=50.0, data_quality_score=20.0,
)
print(f"Status: {eps_risk.valuation_status}")
print(f"Alerts: {eps_risk.alerts}")
print(f"Risk flags: {eps_risk.valuation_risk_flags}")

vocab = []
for result in (flip_base, shocked, stable, eps_risk):
    vocab.extend(result.alerts)
    vocab.extend(result.valuation_risk_flags)

print(f"\n=== Combined vocab ===")
print(f"Vocab: {sorted(set(vocab))}")

required = ["ASSESSMENT_FLIP_RISK", "HIGH_MULTIPLE_DEPENDENCE",
            "HIGH_EPS_DEPENDENCE", "MARGIN_ASSUMPTION_RISK",
            "HIGH_IMPACT_HIGH_UNCERTAINTY"]
print(f"\nRequired: {required}")
missing = [name for name in required if not any(name in item for item in vocab)]
print(f"Missing: {missing}")