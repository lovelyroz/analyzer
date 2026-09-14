from typing import Dict, Any, Optional
from datetime import datetime
from src.forecast.schema import CompanyForecastResult
from src.valuation.schema import ScenarioValuation, ValuationResult
from src.valuation.parameters import INDUSTRY_TARGET_PE, SCENARIO_WEIGHTS
from src.valuation.models import calculate_forward_pe_fair_value, calculate_nav_fair_value, calculate_margin_of_safety

class ValuationEngine:

    def calculate_valuation(
        self,
        company_id: int,
        period_id: int,
        industry_code: str,
        current_price: float,
        forecast_result: CompanyForecastResult,
        forecast_reliability_score: float = 80.0,
        nav_per_share: Optional[float] = None
    ) -> ValuationResult:
        
        target_ratio = INDUSTRY_TARGET_PE.get(industry_code, INDUSTRY_TARGET_PE["GENERAL"])
        scenarios: Dict[str, ScenarioValuation] = {}
        weighted_fair_value = 0.0
        total_weight = 0.0

        scenario_inputs = {
            "bear": forecast_result.scenario_forecasts.bear,
            "base": forecast_result.scenario_forecasts.base,
            "bull": forecast_result.scenario_forecasts.bull
        }

        for name, chain in scenario_inputs.items():
            if industry_code == "INVESTMENT" and nav_per_share is not None:
                fv = calculate_nav_fair_value(nav_per_share, target_ratio)
            else:
                fv = calculate_forward_pe_fair_value(chain.eps, target_ratio)

            if fv is not None:
                upside = calculate_margin_of_safety(fv, current_price)
                scenarios[name] = ScenarioValuation(
                    scenario_name=name,
                    target_pe=target_ratio,
                    eps_forecast=chain.eps or 0.0,
                    fair_value=fv,
                    upside_downside_pct=upside
                )
                weight = SCENARIO_WEIGHTS.get(name, 0.33)
                weighted_fair_value += fv * weight
                total_weight += weight

        expected_fv = round(weighted_fair_value / total_weight, 2) if total_weight > 0 else current_price
        mos = calculate_margin_of_safety(expected_fv, current_price)

        # تعیین وضعیت ارزشمندی
        if mos >= 20.0:
            status = "UNDERVALUED"
        elif mos <= -20.0:
            status = "OVERVALUED"
        else:
            status = "FAIRLY_VALUED"

        # ارزیابی میزان ریسک و اطمینان ارزش‌گذاری
        val_confidence = round(max(10.0, min(100.0, forecast_reliability_score * 0.9)), 2)
        risk_level = "LOW" if val_confidence >= 75 and abs(mos) <= 30 else ("HIGH" if val_confidence < 50 else "MEDIUM")

        return ValuationResult(
            company_id=company_id,
            period_id=period_id,
            current_price=current_price,
            expected_fair_value=expected_fv,
            margin_of_safety_pct=mos,
            valuation_status=status,
            valuation_confidence=val_confidence,
            valuation_risk_level=risk_level,
            scenarios=scenarios,
            model_version="V1.0",
            calculation_timestamp=datetime.utcnow()
        )