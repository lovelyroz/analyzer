from src.kpi.schema import KPIResult
from datetime import datetime

class IndustryKPIEngine:

    # ------------------ صنعت بانک (BANK - 5 KPIs) ------------------
    @staticmethod
    def calc_bank_kpis(nii: float, nim: float, loan_growth: float, deposit_growth: float, npl: float, company_id: int, period_id: int) -> list:
        return [
            KPIResult(company_id, period_id, "BANK_NII", nii, "CURRENCY_IRR", "VALID" if nii is not None else "MISSING", datetime.utcnow()),
            KPIResult(company_id, period_id, "BANK_NIM", nim, "PERCENTAGE", "VALID" if nim is not None else "MISSING", datetime.utcnow()),
            KPIResult(company_id, period_id, "BANK_LOAN_GROWTH", loan_growth, "PERCENTAGE", "VALID" if loan_growth is not None else "MISSING", datetime.utcnow()),
            KPIResult(company_id, period_id, "BANK_DEPOSIT_GROWTH", deposit_growth, "PERCENTAGE", "VALID" if deposit_growth is not None else "MISSING", datetime.utcnow()),
            KPIResult(company_id, period_id, "BANK_NPL", npl, "PERCENTAGE", "VALID" if npl is not None else "MISSING", datetime.utcnow()),
        ]

    # ------------------ صنعت سرمایه‌گذاری / هلدینگ (INVESTMENT - 3 KPIs) ------------------
    @staticmethod
    def calc_holding_kpis(nav: float, nav_growth: float, p_nav: float, company_id: int, period_id: int) -> list:
        return [
            KPIResult(company_id, period_id, "HOLDING_NAV", nav, "CURRENCY_IRR", "VALID" if nav is not None else "MISSING", datetime.utcnow()),
            KPIResult(company_id, period_id, "HOLDING_NAV_GROWTH", nav_growth, "PERCENTAGE", "VALID" if nav_growth is not None else "MISSING", datetime.utcnow()),
            KPIResult(company_id, period_id, "HOLDING_P_NAV", p_nav, "RATIO", "VALID" if p_nav is not None else "MISSING", datetime.utcnow()),
        ]

    # ------------------ صنایع تولیدی (CEMENT, FOOD, PHARMA - هرکدام 1 KPI) ------------------
    @staticmethod
    def calc_sales_volume_kpi(sales_volume: float, company_id: int, period_id: int, industry_code: str) -> KPIResult:
        """مقدار فروش مقداری (Sales Volume) برای صنایع سیمان، غذایی و دارویی"""
        return KPIResult(
            company_id=company_id,
            period_id=period_id,
            kpi_code=f"{industry_code}_SALES_VOLUME",
            value=sales_volume,
            unit="QUANTITY",
            quality_status="VALID" if sales_volume is not None else "MISSING",
            calculation_timestamp=datetime.utcnow()
        )