from typing import List, Dict, Any
from src.kpi.schema import KPIResult
from src.kpi.universal import UniversalKPIEngine
from src.kpi.conditional import ConditionalKPIEngine
from src.kpi.industry import IndustryKPIEngine


class KPIEngine:
    """Coordinator for the Stage 2 KPI specification layer."""

    def calculate_all_kpis_for_company(
        self,
        company_id: int,
        period_id: int,
        industry_code: str,
        financial_data: Dict[str, Any],
    ) -> List[KPIResult]:
        results: List[KPIResult] = [
            UniversalKPIEngine.calc_revenue_growth(
                financial_data.get("revenue_curr"), financial_data.get("revenue_prev"), company_id, period_id
            ),
            UniversalKPIEngine.calc_op_profit_growth(
                financial_data.get("op_profit_curr"), financial_data.get("op_profit_prev"), company_id, period_id
            ),
            UniversalKPIEngine.calc_net_profit_growth(
                financial_data.get("net_profit_curr"), financial_data.get("net_profit_prev"), company_id, period_id
            ),
            UniversalKPIEngine.calc_eps_growth(
                financial_data.get("eps_curr"), financial_data.get("eps_prev"), company_id, period_id
            ),
            UniversalKPIEngine.calc_gross_margin(
                financial_data.get("gross_profit"), financial_data.get("revenue_curr"), company_id, period_id
            ),
            UniversalKPIEngine.calc_op_margin(
                financial_data.get("op_profit_curr"), financial_data.get("revenue_curr"), company_id, period_id
            ),
            UniversalKPIEngine.calc_net_margin(
                financial_data.get("net_profit_curr"), financial_data.get("revenue_curr"), company_id, period_id
            ),
            UniversalKPIEngine.calc_roa(
                financial_data.get("net_profit_ttm"), financial_data.get("avg_assets"), company_id, period_id
            ),
            UniversalKPIEngine.calc_roe(
                financial_data.get("net_profit_ttm"), financial_data.get("avg_equity"), company_id, period_id
            ),
            UniversalKPIEngine.calc_cash_conversion(
                financial_data.get("ocf"), financial_data.get("net_profit_curr"), company_id, period_id
            ),
            UniversalKPIEngine.calc_earnings_quality(
                financial_data.get("ocf"), financial_data.get("op_profit_curr"), company_id, period_id
            ),
            ConditionalKPIEngine.calc_financial_cost_pressure(
                financial_data.get("financial_expenses"), financial_data.get("op_profit_curr"), company_id, period_id
            ),
        ]

        results.extend(
            IndustryKPIEngine.get_industry_kpis(
                industry_code, financial_data, company_id, period_id
            )
        )
        return results