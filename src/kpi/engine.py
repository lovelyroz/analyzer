from typing import List, Dict, Any
from src.kpi.schema import KPIResult
from src.kpi.universal import UniversalKPIEngine
from src.kpi.conditional import ConditionalKPIEngine
from src.kpi.industry import IndustryKPIEngine


class KPIEngine:
    """Coordinator for the Stage 2 KPI specification layer."""

    _KPI_INPUTS = {
        "REVENUE_GROWTH": ("revenue_curr", "revenue_prev"),
        "OP_PROFIT_GROWTH": ("op_profit_curr", "op_profit_prev"),
        "NET_PROFIT_GROWTH": ("net_profit_curr", "net_profit_prev"),
        "EPS_GROWTH": ("eps_curr", "eps_prev"),
        "GROSS_MARGIN": ("gross_profit", "revenue_curr"),
        "OPERATING_MARGIN": ("op_profit_curr", "revenue_curr"),
        "NET_MARGIN": ("net_profit_curr", "revenue_curr"),
        "ROA": ("net_profit_ttm", "avg_assets"),
        "ROE": ("net_profit_ttm", "avg_equity"),
        "CASH_CONVERSION": ("ocf", "net_profit_curr"),
        "EARNINGS_QUALITY": ("ocf", "op_profit_curr"),
        "FINANCIAL_COST_PRESSURE": ("financial_expenses", "op_profit_curr"),
        "BANK_NII": ("nii",),
        "BANK_NIM": ("nim",),
        "BANK_LOAN_GROWTH": ("loan_growth",),
        "BANK_DEPOSIT_GROWTH": ("deposit_growth",),
        "BANK_NPL": ("npl",),
        "HOLDING_NAV": ("nav",),
        "HOLDING_NAV_GROWTH": ("nav_growth",),
        "HOLDING_P_NAV": ("p_nav",),
    }

    @staticmethod
    def _propagate_quality_status(results: List[KPIResult], financial_data: Dict[str, Any]) -> None:
        """Propagate non-VALID Stage 1 input quality without changing KPI math."""
        quality = financial_data.get("quality_statuses", {}) or {}
        priority = {"VALID": 0, "ESTIMATED": 1, "RESTATED": 2, "SUSPICIOUS": 3, "UNMAPPED": 4, "MISSING": 5}
        for result in results:
            fields = KPIEngine._KPI_INPUTS.get(result.kpi_code, ())
            if result.kpi_code.endswith("_SALES_VOLUME"):
                fields = ("sales_volume",)
            statuses = [quality.get(field, "VALID") for field in fields]
            nonvalid = [status for status in statuses if status != "VALID"]
            if nonvalid:
                result.quality_status = max(nonvalid, key=lambda status: priority.get(status, 99))

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

        # EPS growth is comparable only when the EPS series has already been
        # normalized for share-count changes/corporate actions by Stage 1.
        if financial_data.get("eps_comparable", True) is False:
            eps_result = next(r for r in results if r.kpi_code == "EPS_GROWTH")
            eps_result.value = None
            eps_result.quality_status = "MISSING"
            eps_result.metadata = {"comparability_status": "UNRESOLVED_SHARE_COUNT_OR_CORPORATE_ACTION"}

        results.extend(
            IndustryKPIEngine.get_industry_kpis(
                industry_code, financial_data, company_id, period_id
            )
        )
        self._propagate_quality_status(results, financial_data)
        return results