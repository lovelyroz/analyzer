from typing import Optional
from src.kpi.schema import KPIResult
from datetime import datetime


class UniversalKPIEngine:

    # ------------------ 1. Growth (4 KPIs) ------------------
    @staticmethod
    def calc_revenue_growth(curr_rev: Optional[float], prev_rev: Optional[float], company_id: int, period_id: int) -> KPIResult:
        val = ((curr_rev - prev_rev) / abs(prev_rev) * 100) if curr_rev is not None and prev_rev else None
        return KPIResult(company_id, period_id, "REVENUE_GROWTH", val, "PERCENTAGE", "VALID" if val is not None else "MISSING", datetime.utcnow())

    @staticmethod
    def calc_op_profit_growth(curr_op: Optional[float], prev_op: Optional[float], company_id: int, period_id: int) -> KPIResult:
        val = ((curr_op - prev_op) / abs(prev_op) * 100) if curr_op is not None and prev_op else None
        return KPIResult(company_id, period_id, "OP_PROFIT_GROWTH", val, "PERCENTAGE", "VALID" if val is not None else "MISSING", datetime.utcnow())

    @staticmethod
    def calc_net_profit_growth(curr_np: Optional[float], prev_np: Optional[float], company_id: int, period_id: int) -> KPIResult:
        val = ((curr_np - prev_np) / abs(prev_np) * 100) if curr_np is not None and prev_np else None
        return KPIResult(company_id, period_id, "NET_PROFIT_GROWTH", val, "PERCENTAGE", "VALID" if val is not None else "MISSING", datetime.utcnow())

    @staticmethod
    def calc_eps_growth(curr_eps: Optional[float], prev_eps: Optional[float], company_id: int, period_id: int) -> KPIResult:
        val = ((curr_eps - prev_eps) / abs(prev_eps) * 100) if curr_eps is not None and prev_eps else None
        return KPIResult(company_id, period_id, "EPS_GROWTH", val, "PERCENTAGE", "VALID" if val is not None else "MISSING", datetime.utcnow())

    # ------------------ 2. Profitability (5 KPIs) ------------------
    @staticmethod
    def calc_gross_margin(gross_profit: Optional[float], revenue: Optional[float], company_id: int, period_id: int) -> KPIResult:
        val = (gross_profit / revenue * 100) if gross_profit is not None and revenue else None
        return KPIResult(company_id, period_id, "GROSS_MARGIN", val, "PERCENTAGE", "VALID" if val is not None else "MISSING", datetime.utcnow())

    @staticmethod
    def calc_op_margin(op_profit: Optional[float], revenue: Optional[float], company_id: int, period_id: int) -> KPIResult:
        val = (op_profit / revenue * 100) if op_profit is not None and revenue else None
        return KPIResult(company_id, period_id, "OPERATING_MARGIN", val, "PERCENTAGE", "VALID" if val is not None else "MISSING", datetime.utcnow())

    @staticmethod
    def calc_net_margin(net_profit: Optional[float], revenue: Optional[float], company_id: int, period_id: int) -> KPIResult:
        val = (net_profit / revenue * 100) if net_profit is not None and revenue else None
        return KPIResult(company_id, period_id, "NET_MARGIN", val, "PERCENTAGE", "VALID" if val is not None else "MISSING", datetime.utcnow())

    @staticmethod
    def calc_roa(net_profit_ttm: Optional[float], avg_assets: Optional[float], company_id: int, period_id: int) -> KPIResult:
        val = (net_profit_ttm / avg_assets * 100) if net_profit_ttm is not None and avg_assets else None
        return KPIResult(company_id, period_id, "ROA", val, "PERCENTAGE", "VALID" if val is not None else "MISSING", datetime.utcnow())

    @staticmethod
    def calc_roe(net_profit_ttm: Optional[float], avg_equity: Optional[float], company_id: int, period_id: int) -> KPIResult:
        val = (net_profit_ttm / avg_equity * 100) if net_profit_ttm is not None and avg_equity else None
        return KPIResult(company_id, period_id, "ROE", val, "PERCENTAGE", "VALID" if val is not None else "MISSING", datetime.utcnow())

    # ------------------ 3. Risk & Quality (2 KPIs) ------------------
    @staticmethod
    def calc_cash_conversion(ocf: Optional[float], net_profit: Optional[float], company_id: int, period_id: int) -> KPIResult:
        # Locked specification defines OCF / Net Profit conceptually as a ratio.
        val = (ocf / net_profit) if ocf is not None and net_profit else None
        return KPIResult(company_id, period_id, "CASH_CONVERSION", val, "RATIO", "VALID" if val is not None else "MISSING", datetime.utcnow())

    @staticmethod
    def calc_earnings_quality(ocf: Optional[float], op_profit: Optional[float], company_id: int, period_id: int) -> KPIResult:
        # Stage 2 defines Earnings Quality as a composite framework. Its final
        # methodology is intentionally not invented here; a simple OCF/Operating
        # Profit ratio would violate the locked specification.
        val = None
        status = "MISSING"
        return KPIResult(
            company_id, period_id, "EARNINGS_QUALITY", val, "COMPOSITE",
            status, datetime.utcnow(),
            metadata={"framework": "composite", "methodology_status": "DEFERRED"}
        )