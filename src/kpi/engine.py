from typing import List, Dict, Any
from src.kpi.schema import KPIResult
from src.kpi.universal import UniversalKPIEngine
from src.kpi.conditional import ConditionalKPIEngine
from src.kpi.industry import IndustryKPIEngine

class KPIEngine:
    """موتور هماهنگ‌کننده محاسبات KPI برای مرحله ۲"""

    def calculate_all_kpis_for_company(
        self, 
        company_id: int, 
        period_id: int, 
        industry_code: str, 
        financial_data: Dict[str, Any]
    ) -> List[KPIResult]:
        
        results: List[KPIResult] = []

        # ۱. محاسبات ۱۱ شاخص عمومی (Universal Core)
        # --------------------------------------------------
        # رشد (Growth)
        results.append(UniversalKPIEngine.calc_revenue_growth(
            financial_data.get("revenue_curr"), financial_data.get("revenue_prev"), company_id, period_id
        ))
        results.append(UniversalKPIEngine.calc_op_profit_growth(
            financial_data.get("op_profit_curr"), financial_data.get("op_profit_prev"), company_id, period_id
        ))
        results.append(UniversalKPIEngine.calc_net_profit_growth(
            financial_data.get("net_profit_curr"), financial_data.get("net_profit_prev"), company_id, period_id
        ))
        results.append(UniversalKPIEngine.calc_eps_growth(
            financial_data.get("eps_curr"), financial_data.get("eps_prev"), company_id, period_id
        ))

        # سودآوری (Profitability)
        results.append(UniversalKPIEngine.calc_gross_margin(
            financial_data.get("gross_profit"), financial_data.get("revenue_curr"), company_id, period_id
        ))
        results.append(UniversalKPIEngine.calc_op_margin(
            financial_data.get("op_profit_curr"), financial_data.get("revenue_curr"), company_id, period_id
        ))
        results.append(UniversalKPIEngine.calc_net_margin(
            financial_data.get("net_profit_curr"), financial_data.get("revenue_curr"), company_id, period_id
        ))
        results.append(UniversalKPIEngine.calc_roa(
            financial_data.get("net_profit_ttm"), financial_data.get("avg_assets"), company_id, period_id
        ))
        results.append(UniversalKPIEngine.calc_roe(
            financial_data.get("net_profit_ttm"), financial_data.get("avg_equity"), company_id, period_id
        ))

        # ریسک و کیفیت (Risk & Quality)
        results.append(UniversalKPIEngine.calc_cash_conversion(
            financial_data.get("ocf"), financial_data.get("net_profit_curr"), company_id, period_id
        ))
        results.append(UniversalKPIEngine.calc_earnings_quality(
            financial_data.get("ocf"), financial_data.get("op_profit_curr"), company_id, period_id
        ))

        # ۲. محاسبه شاخص مشروط (Conditional KPI)
        # --------------------------------------------------
        results.append(ConditionalKPIEngine.calc_financial_cost_pressure(
            financial_data.get("financial_expenses"), financial_data.get("op_profit_curr"), company_id, period_id
        ))

        # ۳. محاسبات شاخص‌های صنعتی (Industry Core)
        # --------------------------------------------------
        if industry_code == "BANK":
            bank_kpis = IndustryKPIEngine.calc_bank_kpis(
                financial_data.get("nii"), financial_data.get("nim"), 
                financial_data.get("loan_growth"), financial_data.get("deposit_growth"), 
                financial_data.get("npl"), company_id, period_id
            )
            results.extend(bank_kpis)

        elif industry_code == "INVESTMENT":
            holding_kpis = IndustryKPIEngine.calc_holding_kpis(
                financial_data.get("nav"), financial_data.get("nav_growth"), 
                financial_data.get("p_nav"), company_id, period_id
            )
            results.extend(holding_kpis)

        elif industry_code in ["CEMENT", "FOOD", "PHARMA"]:
            results.append(IndustryKPIEngine.calc_sales_volume_kpi(
                financial_data.get("sales_volume"), company_id, period_id, industry_code
            ))

        # صنایع PETROCHEMICAL و METALS طبق سند معماری ۰ شاخص صنعتی مجزا دارند
        
        return results