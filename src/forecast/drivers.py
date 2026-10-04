from typing import Any, Dict, Optional

from dataclasses import replace

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
        eps: Optional[float] = None,
    ) -> SingleForecastChain:
        """Revenue -> Operating Profit -> Net Profit -> EPS -> ROE.

        ``eps`` is the already-resolved EPS numerator-and-denominator decision.
        The driver only divides; it does not decide whether the net profit it
        built is attributable to common shareholders, because that depends on
        the reporting regime rather than on this chain.
        """
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

        # ROE is net profit over the average of opening and closing equity.
        # Both ends are required: closing equity alone is not the specified
        # denominator, and a missing opening balance is never fabricated and
        # never substituted with the closing balance.
        roe = None
        if beginning_equity is not None and ending_equity is not None:
            equity_base = (beginning_equity + ending_equity) / 2.0
            if equity_base != 0:
                roe = forecast_np / equity_base

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
        npl_ratio: Optional[float] = None,
        nim: Optional[float] = None,
        loan_growth: Optional[float] = None,
        deposit_growth: Optional[float] = None,
        assumptions: Optional[Dict[str, Any]] = None,
        eps: Optional[float] = None,
    ) -> SingleForecastChain:
        """Loans/Deposits -> NII/NIM -> Net Profit -> EPS -> ROE.

        Banking drivers are never routed through the non-financial revenue
        model. NPL and NIM are credit/margin *context*: they describe the
        quality of the loan book, and no unvalidated NPL->profit relationship
        exists here, so an NPL ratio never multiplies or scales net profit. It
        is carried into the assumptions as evidence for a later reader, and a
        missing NPL leaves the chain unchanged — missing stays missing.
        """
        nii = forecast_nii
        if nii is None and base_nii is not None and nii_growth is not None:
            nii = base_nii * (1.0 + nii_growth)
        if nii is None:
            return SingleForecastChain(
                method="INSUFFICIENT_DATA",
                assumptions=ForecastDriver._with_bank_context(
                    assumptions, npl_ratio, nim, loan_growth, deposit_growth,
                    reason="missing_nii_driver",
                ),
            )

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
                assumptions=ForecastDriver._with_bank_context(
                    assumptions, npl_ratio, nim, loan_growth, deposit_growth,
                    reason="missing_net_profit_conversion",
                    nii=nii,
                ),
            )

        eps = np / share_count if share_count is not None and share_count > 0 else None
        roe = None
        if beginning_equity is not None and ending_equity is not None:
            avg_equity = (beginning_equity + ending_equity) / 2.0
            if avg_equity != 0:
                roe = np / avg_equity

        # Context only: recorded, and never converted into a profit factor.
        bank_context = ForecastDriver._bank_context(
            npl_ratio, nim, loan_growth, deposit_growth
        )

        return SingleForecastChain(
            operating_profit=ForecastDriver._round(nii),
            net_profit=ForecastDriver._round(np),
            eps=ForecastDriver._round(eps),
            roe=ForecastDriver._round(roe),
            method=method,
            quality=ForecastDriver._quality(method),
            assumptions=ForecastDriver._with_bank_context(
                assumptions, npl_ratio, nim, loan_growth, deposit_growth,
                bank_context=bank_context, np=np,
            ),
        )

    @staticmethod
    def _bank_context(
        npl_ratio: Optional[float],
        nim: Optional[float],
        loan_growth: Optional[float],
        deposit_growth: Optional[float],
    ) -> Dict[str, Any]:
        """Credit and margin evidence, carried verbatim and never priced.

        NPL describes the loan book; it has no calibrated profit multiplier in
        this model, so it stays a reported observation.
        """
        return {
            "npl_ratio": ForecastDriver._round(npl_ratio),
            "npl_role": "CONTEXT_ONLY",
            "nim": ForecastDriver._round(nim),
            "loan_growth": ForecastDriver._round(loan_growth),
            "deposit_growth": ForecastDriver._round(deposit_growth),
        }

    @staticmethod
    def _holding_evidence(
        assumptions: Optional[Dict[str, Any]],
        base_nav: Optional[float],
        nav_growth_rate: Optional[float],
    ) -> Dict[str, Any]:
        """NAV evidence, plus the valuation inputs this chain refuses to read."""
        resolved_nav = None
        if base_nav is not None and nav_growth_rate is not None:
            resolved_nav = base_nav * (1.0 + nav_growth_rate)
        merged = dict(assumptions or {})
        merged["forecast_nav"] = ForecastDriver._round(resolved_nav)
        merged["nav_growth_rate"] = ForecastDriver._round(nav_growth_rate)
        merged["excluded_inputs"] = ["p_nav", "price_to_nav"]
        return merged

    @staticmethod
    def _with_bank_context(
        assumptions: Optional[Dict[str, Any]],
        npl_ratio: Optional[float],
        nim: Optional[float],
        loan_growth: Optional[float],
        deposit_growth: Optional[float],
        *,
        reason: Optional[str] = None,
        bank_context: Optional[Dict[str, Any]] = None,
        nii: Optional[float] = None,
        np: Optional[float] = None,
    ) -> Dict[str, Any]:
        merged = dict(assumptions or {})
        if reason is not None:
            merged["reason"] = reason
        if nii is not None:
            merged["resolved_nii"] = ForecastDriver._round(nii)
        if np is not None:
            merged["resolved_net_profit"] = ForecastDriver._round(np)
        merged["bank_context"] = bank_context if bank_context is not None \
            else ForecastDriver._bank_context(npl_ratio, nim, loan_growth, deposit_growth)
        return merged

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
        eps: Optional[float] = None,
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
            return SingleForecastChain(
                method="INSUFFICIENT_DATA",
                assumptions=ForecastDriver._holding_evidence(
                    assumptions, base_nav, nav_growth_rate
                ),
            )

        eps = np / share_count if share_count is not None and share_count > 0 else None
        roe = None
        if beginning_equity is not None and ending_equity is not None:
            avg_equity = (beginning_equity + ending_equity) / 2.0
            if avg_equity != 0:
                roe = np / avg_equity

        # The forecast NAV and its growth are the chain's own drivers, so they
        # are recorded as evidence. Valuation is Stage 7: P/NAV is not an input
        # to this chain and is named as excluded for the audit trail.
        resolved_nav = None
        if base_nav is not None and nav_growth_rate is not None:
            resolved_nav = base_nav * (1.0 + nav_growth_rate)

        merged = ForecastDriver._holding_evidence(assumptions, base_nav, nav_growth_rate)

        return SingleForecastChain(
            net_profit=ForecastDriver._round(np),
            eps=ForecastDriver._round(eps),
            roe=ForecastDriver._round(roe),
            method=method,
            quality=ForecastDriver._quality(method),
            assumptions=merged,
        )

    # Compatibility wrappers retained for existing callers; they no longer
    # inject hidden defaults or scenario assumptions.
    @staticmethod
    def build_general_chain(base_revenue: float, growth_rate: float, operating_margin: float,
                            net_margin: float, share_count: float,
                            net_profit_is_attributable: bool = True) -> SingleForecastChain:
        revenue = base_revenue * (1.0 + growth_rate)
        chain = ForecastDriver.build_non_financial_chain(
            revenue=revenue,
            operating_margin=operating_margin / 100.0,
            share_count=share_count,
            net_margin=net_margin / 100.0,
            method_hint="RUN_RATE",
        )
        if net_profit_is_attributable:
            return replace(chain, eps=ForecastDriver._round(
                chain.net_profit / share_count))
        return replace(chain, eps=None)
