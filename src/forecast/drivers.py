from typing import Any, Dict, Optional

from src.forecast.schema import SingleForecastChain


class ForecastDriver:
    """Pure calculation helpers for Stage 5 forecast chains."""

    @staticmethod
    def _round(value: Optional[float]) -> Optional[float]:
        return None if value is None else round(float(value), 6)

    @staticmethod
    def _safe_growth(base: Optional[float], growth: Optional[float]) -> Optional[float]:
        if base is None or growth is None:
            return None
        return base * (1.0 + growth)

    @staticmethod
    def _quality(method: str, missing: bool = False) -> str:
        if missing:
            return "INSUFFICIENT_DATA"
        if method == "COMPONENT_BASED":
            return "HIGH"
        if method in {"SEASONAL_BASELINE", "RUN_RATE", "HISTORICAL_CONVERSION", "MARGIN"}:
            return "MEDIUM"
        return "LOW"

    @staticmethod
    def build_non_financial_chain(
        revenue: Optional[float],
        operating_margin: Optional[float],
        share_count: Optional[float],
        *,
        net_profit: Optional[float] = None,
        non_operating_items: Optional[float] = None,
        financial_costs: Optional[float] = None,
        tax: Optional[float] = None,
        net_operating_conversion: Optional[float] = None,
        net_margin: Optional[float] = None,
        beginning_equity: Optional[float] = None,
        ending_equity: Optional[float] = None,
        method_hint: str = "BASELINE",
        assumptions: Optional[Dict[str, Any]] = None,
    ) -> SingleForecastChain:
        """Revenue -> Operating Profit -> Net Profit -> EPS -> ROE."""
        if revenue is None or revenue < 0 or operating_margin is None:
            return SingleForecastChain(method="INSUFFICIENT_DATA", assumptions=assumptions or {})

        op_profit = revenue * operating_margin
        method = method_hint

        # Priority 1: component-based net profit.
        if all(v is not None for v in (non_operating_items, financial_costs, tax)):
            forecast_np = op_profit + non_operating_items - financial_costs - tax
            method = "COMPONENT_BASED"
        # Priority 2: historical operating-profit to net-profit conversion.
        elif net_operating_conversion is not None:
            forecast_np = op_profit * net_operating_conversion
            method = "HISTORICAL_CONVERSION"
        # Priority 3: revenue x net margin.
        elif net_margin is not None:
            forecast_np = revenue * net_margin
            method = "MARGIN"
        # Optional explicit net-profit input is accepted only as a precomputed
        # driver/base when no stronger method is available.
        elif net_profit is not None:
            forecast_np = net_profit
            method = "BASE_NET_PROFIT"
        else:
            return SingleForecastChain(
                revenue=ForecastDriver._round(revenue),
                operating_margin=ForecastDriver._round(operating_margin),
                operating_profit=ForecastDriver._round(op_profit),
                method="INSUFFICIENT_DATA",
                quality="INSUFFICIENT_DATA",
                assumptions=assumptions or {},
            )

        eps = None
        if share_count is not None and share_count > 0:
            eps = forecast_np / share_count

        roe = None
        if beginning_equity is not None and ending_equity is not None:
            avg_equity = (beginning_equity + ending_equity) / 2.0
            if avg_equity != 0:
                roe = forecast_np / avg_equity

        return SingleForecastChain(
            revenue=ForecastDriver._round(revenue),
            operating_margin=ForecastDriver._round(operating_margin),
            operating_profit=ForecastDriver._round(op_profit),
            net_profit=ForecastDriver._round(forecast_np),
            eps=ForecastDriver._round(eps),
            roe=ForecastDriver._round(roe),
            method=method,
            quality=ForecastDriver._quality(method),
            assumptions=assumptions or {},
        )

    @staticmethod
    def build_bank_chain(
        base_nii: Optional[float],
        nii_growth: Optional[float],
        share_count: Optional[float],
        *,
        forecast_nii: Optional[float] = None,
        net_profit_conversion: Optional[float] = None,
        forecast_net_profit: Optional[float] = None,
        beginning_equity: Optional[float] = None,
        ending_equity: Optional[float] = None,
        assumptions: Optional[Dict[str, Any]] = None,
    ) -> SingleForecastChain:
        """Loans/Deposits -> NII/NIM -> Net Profit -> EPS -> ROE."""
        nii = forecast_nii
        if nii is None and base_nii is not None and nii_growth is not None:
            nii = base_nii * (1.0 + nii_growth)
        if nii is None:
            return SingleForecastChain(method="INSUFFICIENT_DATA", assumptions=assumptions or {})

        if forecast_net_profit is not None:
            np = forecast_net_profit
            method = "BANK_COMPONENT_BASED"
        elif net_profit_conversion is not None:
            np = nii * net_profit_conversion
            method = "BANK_NII_CONVERSION"
        else:
            return SingleForecastChain(
                method="INSUFFICIENT_DATA",
                quality="INSUFFICIENT_DATA",
                assumptions=assumptions or {},
            )

        eps = np / share_count if share_count is not None and share_count > 0 else None
        roe = None
        if beginning_equity is not None and ending_equity is not None:
            avg_equity = (beginning_equity + ending_equity) / 2.0
            if avg_equity != 0:
                roe = np / avg_equity

        return SingleForecastChain(
            operating_profit=ForecastDriver._round(nii),
            net_profit=ForecastDriver._round(np),
            eps=ForecastDriver._round(eps),
            roe=ForecastDriver._round(roe),
            method=method,
            quality=ForecastDriver._quality(method),
            assumptions=assumptions or {},
        )

    @staticmethod
    def build_holding_chain(
        base_nav: Optional[float],
        nav_growth_rate: Optional[float],
        share_count: Optional[float],
        *,
        net_profit_conversion: Optional[float] = None,
        forecast_net_profit: Optional[float] = None,
        beginning_equity: Optional[float] = None,
        ending_equity: Optional[float] = None,
        assumptions: Optional[Dict[str, Any]] = None,
    ) -> SingleForecastChain:
        """NAV -> NAV Growth -> Net Profit -> EPS -> ROE; P/NAV is excluded."""
        if forecast_net_profit is not None:
            np = forecast_net_profit
            method = "HOLDING_COMPONENT_BASED"
        elif base_nav is not None and nav_growth_rate is not None and net_profit_conversion is not None:
            forecast_nav = base_nav * (1.0 + nav_growth_rate)
            np = forecast_nav * net_profit_conversion
            method = "HOLDING_NAV_CONVERSION"
        else:
            return SingleForecastChain(method="INSUFFICIENT_DATA", assumptions=assumptions or {})

        eps = np / share_count if share_count is not None and share_count > 0 else None
        roe = None
        if beginning_equity is not None and ending_equity is not None:
            avg_equity = (beginning_equity + ending_equity) / 2.0
            if avg_equity != 0:
                roe = np / avg_equity

        return SingleForecastChain(
            net_profit=ForecastDriver._round(np),
            eps=ForecastDriver._round(eps),
            roe=ForecastDriver._round(roe),
            method=method,
            quality=ForecastDriver._quality(method),
            assumptions=assumptions or {},
        )

    # Compatibility wrappers retained for existing callers; they no longer
    # inject hidden defaults or scenario assumptions.
    @staticmethod
    def build_general_chain(base_revenue: float, growth_rate: float, operating_margin: float,
                            net_margin: float, share_count: float) -> SingleForecastChain:
        revenue = base_revenue * (1.0 + growth_rate)
        return ForecastDriver.build_non_financial_chain(
            revenue=revenue,
            operating_margin=operating_margin / 100.0,
            share_count=share_count,
            net_margin=net_margin / 100.0,
            method_hint="RUN_RATE",
        )
