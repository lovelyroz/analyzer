from datetime import datetime
from typing import Dict, Any, Optional
from src.forecast.schema import CompanyForecastResult, ScenarioForecastResult, SingleForecastChain
from src.forecast.drivers import ForecastDriver

class ForecastEngine:

    def generate_forecast(
        self,
        company_id: int,
        forecast_period_id: int,
        industry_code: str,
        financial_context: Dict[str, Any],
        trend_state: Optional[str] = None,
        data_cutoff_datetime: Optional[datetime] = None
    ) -> CompanyForecastResult:
        
        cutoff = data_cutoff_datetime or datetime.utcnow()
        share_count = financial_context.get("share_count", 1.0)
        
        # ۱. تعیین نرخ رشد Base و ضریب تعدیل بر اساس Trend State (Stage 4 Output)
        base_growth = financial_context.get("base_growth_rate", 0.10) # فرض اولیه ۱۰٪ رشد
        
        # Adjustments بر اساس Trend State خروجی Stage 4
        trend_adjustment = 0.0
        if trend_state == "Strong Improvement":
            trend_adjustment = 0.05
        elif trend_state == "Strong Deterioration":
            trend_adjustment = -0.05

        effective_base_growth = base_growth + trend_adjustment

        # ۲. تعریف سناریوها
        bear_growth = effective_base_growth - 0.10
        base_growth_final = effective_base_growth
        bull_growth = effective_base_growth + 0.10

        # ۳. تولید پیش‌بینی بر اساس نوع صنعت
        if industry_code == "INVESTMENT":
            base_np = financial_context.get("base_net_profit", 1000.0)
            bear_chain = ForecastDriver.build_holding_chain(base_np, bear_growth, share_count)
            base_chain = ForecastDriver.build_holding_chain(base_np, base_growth_final, share_count)
            bull_chain = ForecastDriver.build_holding_chain(base_np, bull_growth, share_count)
        else:
            base_rev = financial_context.get("base_revenue", 10000.0)
            op_margin = financial_context.get("op_margin", 20.0)
            net_margin = financial_context.get("net_margin", 15.0)

            bear_chain = ForecastDriver.build_general_chain(base_rev, bear_growth, op_margin, net_margin, share_count)
            base_chain = ForecastDriver.build_general_chain(base_rev, base_growth_final, op_margin, net_margin, share_count)
            bull_chain = ForecastDriver.build_general_chain(base_rev, bull_growth, op_margin, net_margin, share_count)

        scenarios = ScenarioForecastResult(
            bear=bear_chain,
            base=base_chain,
            bull=bull_chain
        )

        return CompanyForecastResult(
            company_id=company_id,
            forecast_period_id=forecast_period_id,
            data_cutoff_datetime=cutoff,
            industry_code=industry_code,
            scenario_forecasts=scenarios,
            forecast_method="DRIVER_BASED",
            model_version="V1.0",
            calculation_timestamp=datetime.utcnow()
        )