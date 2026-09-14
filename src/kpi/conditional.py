from typing import Optional
from datetime import datetime
from src.kpi.schema import KPIResult

class ConditionalKPIEngine:
    
    @staticmethod
    def calc_financial_cost_pressure(
        financial_expenses: Optional[float], 
        operating_profit: Optional[float], 
        company_id: int, 
        period_id: int
    ) -> KPIResult:
        """
        محاسبه KPI مشروط: فشار هزینه مالی (Financial Cost Pressure)
        نسبت هزینه‌های مالی به سود عملیاتی
        """
        # اگر اطلاعات مالی موجود نباشد یا سود عملیاتی صفر/منفی باشد، مقدار به جای صفر شدن None می‌ماند
        if financial_expenses is None or operating_profit is None or operating_profit <= 0:
            val = None
            status = "MISSING"
        else:
            val = (abs(financial_expenses) / operating_profit) * 100.0
            status = "VALID"

        return KPIResult(
            company_id=company_id,
            period_id=period_id,
            kpi_code="FINANCIAL_COST_PRESSURE",
            value=val,
            unit="PERCENTAGE",
            quality_status=status,
            calculation_timestamp=datetime.utcnow(),
            metadata={"is_conditional": True}
        )