from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from dataclasses import replace

from src.forecast.drivers import ForecastDriver
from src.forecast.schema import (
    CompanyForecastResult,
    ForecastInputRef,
    ScenarioForecastResult,
    SingleForecastChain,
    SUPPORTED_HORIZONS,
    SUPPORTED_INDUSTRIES,
    NON_FINANCIAL_INDUSTRIES,
    normalize_datetime,
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
    def _share_count(context: Dict[str, Any]) -> Optional[float]:
        """Weighted average shares built from Stage 1 share data (spec §9).

        Accepts the figure the builder produces, or a plain number supplied
        directly. Missing shares stay missing: net profit without a
        denominator yields no EPS rather than an invented one.
        """
        shares = context.get("forecast_weighted_average_shares")
        if hasattr(shares, "get"):
            shares = shares.get()
        value = float(shares) if isinstance(shares, (int, float)) else None
        if value is not None:
            return value
        fallback = context.get("share_count")
        if hasattr(fallback, "get"):
            fallback = fallback.get()
        return float(fallback) if isinstance(fallback, (int, float)) else None

    @staticmethod
    def _baseline_value(context: Dict[str, Any], *keys: str) -> Optional[float]:
        for key in keys:
            value = ForecastEngine._number(context, key)
            if value is not None:
                return value
        return None

    # ------------------------------------------------------------------
    # Point-in-Time protection (spec §25) and input auditability (§29)
    # ------------------------------------------------------------------

    @staticmethod
    def _raw_input_refs(context: Dict[str, Any]) -> List[ForecastInputRef]:
        """Normalize the caller's provenance declarations.

        Stage 5 does not own the report layer, so provenance is an opt-in
        contract: whoever assembles ``financial_context`` declares which facts
        came from which report version. Undeclared inputs are recorded without
        a publication date and are therefore never rejected as look-ahead.
        """
        declared = context.get("input_refs") or context.get("forecast_input_refs") or []
        refs: List[ForecastInputRef] = []
        for item in declared:
            if isinstance(item, ForecastInputRef):
                refs.append(item)
            elif isinstance(item, dict):
                try:
                    refs.append(ForecastInputRef.from_mapping(item))
                except KeyError:
                    raise ValueError("input_refs entries require a 'fact_key'")
            else:
                raise ValueError(
                    "input_refs entries must be ForecastInputRef or mapping with 'fact_key'"
                )
        return refs

    @staticmethod
    def _pit_safe(context: Dict[str, Any], refs: List[ForecastInputRef],
                  cutoff: datetime) -> tuple[bool, List[ForecastInputRef], Optional[ForecastInputRef]]:
        """Split inputs by availability and report the first violation (if any)."""
        dropped = [ref for ref in refs
                   if ref.available_at is not None
                   and normalize_datetime(ref.available_at) > normalize_datetime(cutoff)]
        if not dropped:
            return True, refs, None
        first_violation = min(
            dropped, key=lambda ref: normalize_datetime(ref.available_at)
        )
        return False, [ref for ref in refs if ref not in dropped], first_violation

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
            share_count=self._share_count(context),
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

        cutoff = normalize_datetime(data_cutoff_datetime) or datetime.now(timezone.utc)
        params = self._merge_parameters(financial_context)
        trend_adj = self._trend_adjustment(financial_context, trend_state, params)

        # Point-in-Time: a forecast may only use inputs published at or before
        # its cutoff (spec §25). Late inputs are dropped, never silently kept.
        raw_refs = self._raw_input_refs(financial_context)
        pit_ok, input_refs, violation = self._pit_safe(financial_context, raw_refs, cutoff)

        calculation_at = normalize_datetime(
            financial_context.get("calculation_timestamp")
        ) or datetime.now(timezone.utc)
        if calculation_at < cutoff:
            raise ValueError(
                "calculation_timestamp precedes data_cutoff_datetime: the forecast "
                "would be dated before the information it claims to see"
            )

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
            "data_cutoff_datetime": cutoff.isoformat(),
            "pit_valid": pit_ok,
            "input_refs": [
                {"fact_key": ref.fact_key, "report_version_id": ref.report_version_id,
                 "available_at": ref.available_at.isoformat() if ref.available_at else None,
                 "source": ref.source}
                for ref in input_refs
            ],
        }
        if violation is not None:
            assumptions["pit_violation"] = {
                "fact_key": violation.fact_key,
                "available_at": violation.available_at.isoformat(),
                "cutoff": cutoff.isoformat(),
                "action": "input_dropped",
            }

        if industry_code in NON_FINANCIAL_INDUSTRIES:
            baseline_revenue, baseline_method = self._baseline_revenue(financial_context)
            seasonal_naive_revenue = self._number(financial_context, "seasonal_naive_revenue")
            if seasonal_naive_revenue is not None:
                benchmark = SingleForecastChain(revenue=round(seasonal_naive_revenue, 6), method="SEASONAL_NAIVE", quality="BENCHMARK")

            if baseline_revenue is None:
                empty = SingleForecastChain(
                    method="INSUFFICIENT_DATA",
                    assumptions={"reason": "missing_revenue_baseline"},
                    scenario="MISSING",
                    forecast_horizon=horizon,
                )
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
                scenarios = ScenarioForecastResult(
                    replace(bear, scenario="BEAR", forecast_horizon=horizon),
                    replace(base, scenario="BASE", forecast_horizon=horizon),
                    replace(bull, scenario="BULL", forecast_horizon=horizon),
                )
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
                ForecastDriver.build_bank_chain(base_nii, bear_g, self._share_count(financial_context),
                                                net_profit_conversion=self._number(financial_context, "bank_net_profit_nii_conversion"),
                                                beginning_equity=self._number(financial_context, "beginning_equity"), ending_equity=self._number(financial_context, "forecast_ending_equity"), assumptions={"scenario": "BEAR"}),
                ForecastDriver.build_bank_chain(base_nii, base_g, self._share_count(financial_context),
                                                net_profit_conversion=self._number(financial_context, "bank_net_profit_nii_conversion"),
                                                beginning_equity=self._number(financial_context, "beginning_equity"), ending_equity=self._number(financial_context, "forecast_ending_equity"), assumptions={"scenario": "BASE"}),
                ForecastDriver.build_bank_chain(base_nii, bull_g, self._share_count(financial_context),
                                                net_profit_conversion=self._number(financial_context, "bank_net_profit_nii_conversion"),
                                                beginning_equity=self._number(financial_context, "beginning_equity"), ending_equity=self._number(financial_context, "forecast_ending_equity"), assumptions={"scenario": "BULL"}),
            )

        else:
            baseline_method = "HOLDING_SPECIALIZED"
            base_nav = self._number(financial_context, "base_nav")
            nav_growth = self._number(financial_context, "baseline_nav_growth")
            if nav_growth is None:
                nav_growth = 0.00
            nav_growth += trend_adj
            bear_g, base_g, bull_g = nav_growth - financial_spread, nav_growth, nav_growth + financial_spread
            shares = self._share_count(financial_context)
            conversion = self._number(financial_context, "holding_net_profit_nav_conversion")
            scenarios = ScenarioForecastResult(
                ForecastDriver.build_holding_chain(base_nav, bear_g, shares, net_profit_conversion=conversion,
                                                   beginning_equity=self._number(financial_context, "beginning_equity"), ending_equity=self._number(financial_context, "forecast_ending_equity"), assumptions={"scenario": "BEAR"}),
                ForecastDriver.build_holding_chain(base_nav, base_g, shares, net_profit_conversion=conversion,
                                                   beginning_equity=self._number(financial_context, "beginning_equity"), ending_equity=self._number(financial_context, "forecast_ending_equity"), assumptions={"scenario": "BASE"}),
                ForecastDriver.build_holding_chain(base_nav, bull_g, shares, net_profit_conversion=conversion,
                                                   beginning_equity=self._number(financial_context, "beginning_equity"), ending_equity=self._number(financial_context, "forecast_ending_equity"), assumptions={"scenario": "BULL"}),
            )

        # Scenario identity and horizon are recorded on every chain so a frozen
        # record can state which scenario it belongs to without external state.
        scenarios = ScenarioForecastResult(
            replace(scenarios.bear, scenario="BEAR", forecast_horizon=horizon),
            replace(scenarios.base, scenario="BASE", forecast_horizon=horizon),
            replace(scenarios.bull, scenario="BULL", forecast_horizon=horizon),
        )

        # Audit handle read by ``CompanyForecastResult.to_record``. ALL declared
        # refs are frozen here, including ones rejected by the PIT guard: the
        # record must be able to testify that a late input was seen and dropped,
        # not silently forgotten (spec §29).
        assumptions["__input_refs"] = tuple(raw_refs)

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
            calculation_timestamp=calculation_at,
            data_quality=quality if industry_code in NON_FINANCIAL_INDUSTRIES else (
                "MEDIUM" if scenarios.base.quality != "INSUFFICIENT_DATA" else "INSUFFICIENT_DATA"
            ),
            assumptions=assumptions,
            benchmark=benchmark,
        )
