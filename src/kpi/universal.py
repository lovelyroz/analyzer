from typing import Optional
from src.kpi.schema import KPIResult
from datetime import datetime

class UniversalKPIEngine:

    # ------------------ ۱. رشد (GROWTH - 4 KPIs) ------------------
    @staticmethod
    def calc_revenue_growth(curr_rev: float, prev_rev: float, company_id: int, period_id: int) -> KPIResult:
        val = ((curr_rev - prev_rev) / abs(prev_rev) * 100) if prev_rev else None
        return KPIResult(company_id, period_id, "REV_GROWTH", val, "PERCENTAGE", "VALID" if val is not None else "MISSING", datetime.utcnow())

    @staticmethod
    def calc_op_profit_growth(curr_op: float, prev_op: float, company_id: int, period_id: int) -> KPIResult:
        val = ((curr_op - prev_op) / abs(prev_op) * 100) if prev_op else None
        return KPIResult(company_id, period_id, "OP_PROFIT_GROWTH", val, "PERCENTAGE", "VALID" if val is not None else "MISSING", datetime.utcnow())

    @staticmethod
    def calc_net_profit_growth(curr_np: float, prev_np: float, company_id: int, period_id: int) -> KPIResult:
        val = ((curr_np - prev_np) / abs(prev_np) * 100) if prev_np else None
        return KPIResult(company_id, period_id, "NET_PROFIT_GROWTH", val, "PERCENTAGE", "VALID" if val is not None else "MISSING", datetime.utcnow())

    @staticmethod
    def calc_eps_growth(curr_eps: float, prev_eps: float, company_id: int, period_id: int) -> KPIResult:
        val = ((curr_eps - prev_eps) / abs(prev_eps) * 100) if prev_eps else None
        return KPIResult(company_id, period_id, "EPS_GROWTH", val, "PERCENTAGE", "VALID" if val is not None else "MISSING", datetime.utcnow())

    # ------------------ ۲. سودآوری (PROFITABILITY - 5 KPIs) ------------------
    @staticmethod
    def calc_gross_margin(gross_profit: float, revenue: float, company_id: int, period_id: int) -> KPIResult:
        val = (gross_profit / revenue * 100) if revenue else None
        return KPIResult(company_id, period_id, "GROSS_MARGIN", val, "PERCENTAGE", "VALID" if val is not None else "MISSING", datetime.utcnow())

    @staticmethod
    def calc_op_margin(op_profit: float, revenue: float, company_id: int, period_id: int) -> KPIResult:
        val = (op_profit / revenue * 100) if revenue else None
        return KPIResult(company_id, period_id, "OPERATING_MARGIN", val, "PERCENTAGE", "VALID" if val is not None else "MISSING", datetime.utcnow())

    @staticmethod
    def calc_net_margin(net_profit: float, revenue: float, company_id: int, period_id: int) -> KPIResult:
        val = (net_profit / revenue * 100) if revenue else None
        return KPIResult(company_id, period_id, "NET_MARGIN", val, "PERCENTAGE", "VALID" if val is not None else "MISSING", datetime.utcnow())

    @staticmethod
    def calc_roa(net_profit_ttm: float, avg_assets: float, company_id: int, period_id: int) -> KPIResult:
        val = (net_profit_ttm / avg_assets * 100) if avg_assets else None
        return KPIResult(company_id, period_id, "ROA", val, "PERCENTAGE", "VALID" if val is not None else "MISSING", datetime.utcnow())

    @staticmethod
    def calc_roe(net_profit_ttm: float, avg_equity: float, company_id: int, period_id: int) -> KPIResult:
        val = (net_profit_ttm / avg_equity * 100) if avg_equity else None
        return KPIResult(company_id, period_id, "ROE", val, "PERCENTAGE", "VALID" if val is not None else "MISSING", datetime.utcnow())

    # ------------------ ۳. ریسک و کیفیت (RISK & QUALITY - 2 KPIs) ------------------
    @staticmethod
    def calc_cash_conversion(ocf: float, net_profit: float, company_id: int, period_id: int) -> KPIResult:
        val = (ocf / net_profit) if net_profit else None
        return KPIResult(company_id, period_id, "CASH_CONVERSION", val, "RATIO", "VALID" if val is not None else "MISSING", datetime.utcnow())

    @staticmethod
    def calc_earnings_quality(ocf: float, op_profit: float, company_id: int, period_id: int) -> KPIResult:
        val = (ocf / op_profit) if op_profit else None
        return KPIResult(company_id, period_id, "EARNINGS_QUALITY", val, "RATIO", "VALID" if val is not None else "MISSING", datetime.utcnow())