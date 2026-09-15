from datetime import datetime, timezone
from typing import Any, Dict, Optional

from src.forecast.drivers import ForecastDriver
from src.forecast.schema import (
    CompanyForecastResult,
    ScenarioForecastResult,
    SingleForecastChain,
    SUPPORTED_HORIZONS,
    SUPPORTED_INDUSTRIES,
    NON_FINANCIAL_INDUSTRIES,
)


DEFAULT_MODEL_PARAMETERS = {
    "trend_adjustments": {},
    "scenario_revenue_growth_spread": 0.05,
    "scenario_operating_margin_spread": 0.02,
    "scenario_net_margin_spread": 0.01,
    "scenario_financial_growth_spread": 0.05,
}


class ForecastEngine:
    """Stage 5 Forecast Engine.

    The engine consumes prepared financial and Stage 4 context. It does not
    recalculate KPIs, trends, scores, valuation, or market signals.
    """

    @staticmethod
    def _number(context: Dict[str, Any], key: str) -> Optional[float]:
        value = context.get(key)
        return float(value) if isinstance(value, (int, float)) else None

    @staticmethod
    def _merge_parameters(context: Dict[str, Any]) -> Dict[str, Any]:
        params = dict(DEFAULT_MODEL_PARAMETERS)
        params.update(context.get("model_parameters") or {})
        return params

    @staticmethod
    def _trend_adjustment(context: Dict[str, Any], trend_state: Optional[str], params: Dict[str, Any]) -> float:
        # Stage 4 is evidence only. An explicit model parameter is required to
        # translate that evidence into a bounded forecast adjustment.
        state = trend_state or context.get("trend_state")
        if context.get("low_base") or context.get("LOW_BASE"):
            return 0.0
        mapping = params.get("trend_adjustments") or {}
        value = mapping.get(state, 0.0)
        return float(value) if isinstance(value, (int, float)) else 0.0

    @staticmethod
    def _baseline_revenue(context: Dict[str, Any]) -> tuple[Optional[float], str]:
        if context.get("seasonality_valid") and ForecastEngine._number(context, "seasonal_baseline_revenue") is not None:
            return ForecastEngine._number(context, "seasonal_baseline_revenue"), "SEASONAL_BASELINE"
        if ForecastEngine._number(context, "recent_run_rate_revenue") is not None:
            return ForecastEngine._number(context, "recent_run_rate_revenue"), "RUN_RATE"
        return None, "INSUFFICIENT_DATA"

    @staticmethod
    def _baseline_value(context: Dict[str, Any], *keys: str) -> Optional[float]:
        for key in keys:
            value = ForecastEngine._number(context, key)
            if value is not None:
                return value
        return None

    def _non_financial_scenario(
        self,
        context: Dict[str, Any],
        baseline_revenue: float,
        baseline_method: str,
        growth: float,
        margin_adjustment: float,
        net_margin_adjustment: float,
        scenario_name: str,
        trend_adjustment: float,
    ) -> SingleForecastChain:
        base_op_margin = self._baseline_value(
            context, "forecast_operating_margin", "historical_operating_margin", "recent_operating_margin"
        )
        if base_op_margin is None:
            return SingleForecastChain(method="INSUFFICIENT_DATA", assumptions={"reason": "missing_operating_margin"})

        # Margins are stored as decimal ratios in the Stage 5 input contract.
        op_margin = base_op_margin + margin_adjustment
        net_margin = self._baseline_value(
            context, "forecast_net_margin", "historical_net_margin", "recent_net_margin"
        )
        conversion = self._number(context, "historical_net_operating_conversion")

        scenario_assumptions = {
            "scenario": scenario_name,
            "baseline_method": baseline_method,
            "trend_adjustment": trend_adjustment,
            "low_base_control": bool(context.get("low_base") or context.get("LOW_BASE")),
        }

        # Explicit, traceable driver adjustments may be supplied by the caller.
        # No external/FX assumption is invented here.
        explicit_driver_adjustment = self._number(context, "driver_revenue_adjustment")
        if explicit_driver_adjustment is not None:
            growth += explicit_driver_adjustment
            scenario_assumptions["driver_revenue_adjustment"] = explicit_driver_adjustment

        revenue = baseline_revenue * (1.0 + growth)
        return ForecastDriver.build_non_financial_chain(
            revenue=revenue,
            operating_margin=op_margin,
            share_count=self._number(context, "forecast_weighted_average_shares")
            or self._number(context, "share_count"),
            non_operating_items=self._number(context, "forecast_non_operating_items"),
            financial_costs=self._number(context, "forecast_financial_costs"),
            tax=self._number(context, "forecast_tax"),
            net_operating_conversion=conversion,
            net_margin=None if conversion is not None else (
                None if net_margin is None else net_margin
            ),
            beginning_equity=self._number(context, "beginning_equity"),
            ending_equity=self._number(context, "forecast_ending_equity"),
            method_hint=baseline_method,
            assumptions=scenario_assumptions,
        )

    def generate_forecast(
        self,
        company_id: int,
        forecast_period_id: int,
        industry_code: str,
        financial_context: Dict[str, Any],
        trend_state: Optional[str] = None,
        data_cutoff_datetime: Optional[datetime] = None,
        horizon: str = "12M",
        model_version: str = "V1.0",
    ) -> CompanyForecastResult:
        if industry_code not in SUPPORTED_INDUSTRIES:
            raise ValueError(f"Unsupported Stage 5 industry: {industry_code}")
        if horizon not in SUPPORTED_HORIZONS:
            raise ValueError(f"Unsupported Stage 5 horizon: {horizon}")

        cutoff = data_cutoff_datetime or datetime.now(timezone.utc)
        params = self._merge_parameters(financial_context)
        trend_adj = self._trend_adjustment(financial_context, trend_state, params)

        scenario_spread = float(params.get("scenario_revenue_growth_spread", 0.05))
        financial_spread = float(params.get("scenario_financial_growth_spread", scenario_spread))
        margin_spread = float(params.get("scenario_operating_margin_spread", 0.02))
        net_margin_spread = float(params.get("scenario_net_margin_spread", 0.01))

        benchmark = None
        assumptions: Dict[str, Any] = {
            "model_parameters": params,
            "trend_evidence": trend_state or financial_context.get("trend_state"),
            "sign_change": financial_context.get("sign_change"),
            "low_base": bool(financial_context.get("low_base") or financial_context.get("LOW_BASE")),
            "operational_fx": financial_context.get("operational_fx"),
            "operational_fx_source": financial_context.get("operational_fx_source"),
        }

        if industry_code in NON_FINANCIAL_INDUSTRIES:
            baseline_revenue, baseline_method = self._baseline_revenue(financial_context)
            seasonal_naive_revenue = self._number(financial_context, "seasonal_naive_revenue")
            if seasonal_naive_revenue is not None:
                benchmark = SingleForecastChain(revenue=round(seasonal_naive_revenue, 6), method="SEASONAL_NAIVE", quality="BENCHMARK")

            if baseline_revenue is None:
                empty = SingleForecastChain(method="INSUFFICIENT_DATA", assumptions={"reason": "missing_revenue_baseline"})
                scenarios = ScenarioForecastResult(empty, empty, empty)
                quality = "INSUFFICIENT_DATA"
            else:
                base_growth = self._number(financial_context, "baseline_revenue_growth")
                if base_growth is None:
                    base_growth = 0.0
                base_growth += trend_adj
                bear_growth = base_growth - scenario_spread
                bull_growth = base_growth + scenario_spread

                bear = self._non_financial_scenario(financial_context, baseline_revenue, baseline_method, bear_growth,
                                                    -margin_spread, -net_margin_spread, "BEAR", trend_adj)
                base = self._non_financial_scenario(financial_context, baseline_revenue, baseline_method, base_growth,
                                                    0.0, 0.0, "BASE", trend_adj)
                bull = self._non_financial_scenario(financial_context, baseline_revenue, baseline_method, bull_growth,
                                                    margin_spread, net_margin_spread, "BULL", trend_adj)
                scenarios = ScenarioForecastResult(bear, base, bull)
                quality = "HIGH" if base.quality == "HIGH" else ("MEDIUM" if base.quality != "INSUFFICIENT_DATA" else "INSUFFICIENT_DATA")

        elif industry_code == "BANK":
            baseline_method = "BANK_SPECIALIZED"
            base_nii = self._number(financial_context, "base_nii")
            nii_growth = self._number(financial_context, "baseline_nii_growth")
            if nii_growth is None:
                nii_growth = 0.0
            nii_growth += trend_adj
            bear_g, base_g, bull_g = nii_growth - financial_spread, nii_growth, nii_growth + financial_spread
            scenarios = ScenarioForecastResult(
                ForecastDriver.build_bank_chain(base_nii, bear_g, self._number(financial_context, "forecast_weighted_average_shares") or self._number(financial_context, "share_count"),
                                                net_profit_conversion=self._number(financial_context, "bank_net_profit_nii_conversion"),
                                                beginning_equity=self._number(financial_context, "beginning_equity"), ending_equity=self._number(financial_context, "forecast_ending_equity"), assumptions={"scenario": "BEAR"}),
                ForecastDriver.build_bank_chain(base_nii, base_g, self._number(financial_context, "forecast_weighted_average_shares") or self._number(financial_context, "share_count"),
                                                net_profit_conversion=self._number(financial_context, "bank_net_profit_nii_conversion"),
                                                beginning_equity=self._number(financial_context, "beginning_equity"), ending_equity=self._number(financial_context, "forecast_ending_equity"), assumptions={"scenario": "BASE"}),
                ForecastDriver.build_bank_chain(base_nii, bull_g, self._number(financial_context, "forecast_weighted_average_shares") or self._number(financial_context, "share_count"),
                                                net_profit_conversion=self._number(financial_context, "bank_net_profit_nii_conversion"),
                                                beginning_equity=self._number(financial_context, "beginning_equity"), ending_equity=self._number(financial_context, "forecast_ending_equity"), assumptions={"scenario": "BULL"}),
            )

        else:
            baseline_method = "HOLDING_SPECIALIZED"
            base_nav = self._number(financial_context, "base_nav")
            nav_growth = self._number(financial_context, "baseline_nav_growth")
            if nav_growth is None:
                nav_growth = 0.0
            nav_growth += trend_adj
            bear_g, base_g, bull_g = nav_growth - financial_spread, nav_growth, nav_growth + financial_spread
            shares = self._number(financial_context, "forecast_weighted_average_shares") or self._number(financial_context, "share_count")
            conversion = self._number(financial_context, "holding_net_profit_nav_conversion")
            scenarios = ScenarioForecastResult(
                ForecastDriver.build_holding_chain(base_nav, bear_g, shares, net_profit_conversion=conversion,
                                                   beginning_equity=self._number(financial_context, "beginning_equity"), ending_equity=self._number(financial_context, "forecast_ending_equity"), assumptions={"scenario": "BEAR"}),
                ForecastDriver.build_holding_chain(base_nav, base_g, shares, net_profit_conversion=conversion,
                                                   beginning_equity=self._number(financial_context, "beginning_equity"), ending_equity=self._number(financial_context, "forecast_ending_equity"), assumptions={"scenario": "BASE"}),
                ForecastDriver.build_holding_chain(base_nav, bull_g, shares, net_profit_conversion=conversion,
                                                   beginning_equity=self._number(financial_context, "beginning_equity"), ending_equity=self._number(financial_context, "forecast_ending_equity"), assumptions={"scenario": "BULL"}),
            )

        forecast_method = scenarios.base.method
        return CompanyForecastResult(
            company_id=company_id,
            forecast_period_id=forecast_period_id,
            horizon=horizon,
            data_cutoff_datetime=cutoff,
            industry_code=industry_code,
            scenario_forecasts=scenarios,
            baseline_method=baseline_method,
            forecast_method=forecast_method,
            model_version=model_version,
            calculation_timestamp=datetime.now(timezone.utc),
            data_quality=quality if industry_code in NON_FINANCIAL_INDUSTRIES else (
                "MEDIUM" if scenarios.base.quality != "INSUFFICIENT_DATA" else "INSUFFICIENT_DATA"
            ),
            assumptions=assumptions,
            benchmark=benchmark,
        )
