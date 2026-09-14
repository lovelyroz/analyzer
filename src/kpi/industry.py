from src.kpi.schema import KPIResult
from datetime import datetime
from typing import Any, Dict, Optional


class IndustryKPIEngine:

    # ------------------ Bank (5 KPIs) ------------------
    @staticmethod
    def calc_bank_kpis(nii: Optional[float], nim: Optional[float], loan_growth: Optional[float], deposit_growth: Optional[float], npl: Optional[float], company_id: int, period_id: int) -> list:
        return [
            KPIResult(company_id, period_id, "BANK_NII", nii, "CURRENCY_IRR", "VALID" if nii is not None else "MISSING", datetime.utcnow()),
            KPIResult(company_id, period_id, "BANK_NIM", nim, "PERCENTAGE", "VALID" if nim is not None else "MISSING", datetime.utcnow()),
            KPIResult(company_id, period_id, "BANK_LOAN_GROWTH", loan_growth, "PERCENTAGE", "VALID" if loan_growth is not None else "MISSING", datetime.utcnow()),
            KPIResult(company_id, period_id, "BANK_DEPOSIT_GROWTH", deposit_growth, "PERCENTAGE", "VALID" if deposit_growth is not None else "MISSING", datetime.utcnow()),
            KPIResult(company_id, period_id, "BANK_NPL", npl, "PERCENTAGE", "VALID" if npl is not None else "MISSING", datetime.utcnow()),
        ]

    # ------------------ Investment / Holding (3 KPIs) ------------------
    @staticmethod
    def calc_holding_kpis(nav: Optional[float], nav_growth: Optional[float], p_nav: Optional[float], company_id: int, period_id: int) -> list:
        return [
            KPIResult(company_id, period_id, "HOLDING_NAV", nav, "CURRENCY_IRR", "VALID" if nav is not None else "MISSING", datetime.utcnow()),
            KPIResult(company_id, period_id, "HOLDING_NAV_GROWTH", nav_growth, "PERCENTAGE", "VALID" if nav_growth is not None else "MISSING", datetime.utcnow()),
            KPIResult(company_id, period_id, "HOLDING_P_NAV", p_nav, "RATIO", "VALID" if p_nav is not None else "MISSING", datetime.utcnow()),
        ]

    # ------------------ Cement / Food / Pharmaceutical (1 KPI each) ------------------
    @staticmethod
    def calc_sales_volume_kpi(sales_volume: Optional[float], company_id: int, period_id: int, industry_code: str) -> KPIResult:
        """Sales Volume is optional; missing data remains MISSING, never zero."""
        return KPIResult(
            company_id=company_id,
            period_id=period_id,
            kpi_code=f"{industry_code}_SALES_VOLUME",
            value=sales_volume,
            unit="QUANTITY",
            quality_status="VALID" if sales_volume is not None else "MISSING",
            calculation_timestamp=datetime.utcnow(),
        )

    @staticmethod
    def get_industry_kpis(industry_code: str, financial_data: Dict[str, Any], company_id: int, period_id: int) -> list:
        """Return only the Stage 2 Industry Core KPI inventory for the selected industry."""
        if industry_code == "BANK":
            return IndustryKPIEngine.calc_bank_kpis(
                financial_data.get("nii"), financial_data.get("nim"),
                financial_data.get("loan_growth"), financial_data.get("deposit_growth"),
                financial_data.get("npl"), company_id, period_id,
            )
        if industry_code in {"INVESTMENT", "HOLDING"}:
            return IndustryKPIEngine.calc_holding_kpis(
                financial_data.get("nav"), financial_data.get("nav_growth"),
                financial_data.get("p_nav"), company_id, period_id,
            )
        if industry_code in {"CEMENT", "FOOD", "PHARMA"}:
            return [IndustryKPIEngine.calc_sales_volume_kpi(
                financial_data.get("sales_volume"), company_id, period_id, industry_code,
            )]
        # PETROCHEMICAL/CHEMICAL and METALS/MINING intentionally have zero
        # Industry Core KPIs in Stage 2 V1.
        return []