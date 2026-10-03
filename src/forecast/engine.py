from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from dataclasses import replace

from src.forecast.drivers import ForecastDriver
from src.forecast.schema import (
    CompanyForecastResult,
    ForecastInputRef,
    OperationalFx,
    ScenarioForecastResult,
    SingleForecastChain,
    SUPPORTED_HORIZONS,
    SUPPORTED_INDUSTRIES,
    NON_FINANCIAL_INDUSTRIES,
    normalize_datetime,
)

# The single net-profit hierarchy every non-financial industry uses. Declared
# once so a stored record can state which path it took and in what order the
# others would have applied.
NET_PROFIT_HIERARCHY = (
    "COMPONENT_BASED",
    "HISTORICAL_CONVERSION",
    "NET_MARGIN",
    "INSUFFICIENT_DATA",
)


DEFAULT_MODEL_PARAMETERS = {
    "trend_adjustments": {},
    "scenario_revenue_growth_spread": 0.05,
    "scenario_operating_margin_spread": 0.02,
    "scenario_net_margin_spread": 0.01,
    "scenario_financial_growth_spread": 0.05,
    # Operating margin moves on its own evidence, not on revenue growth. The
    # base level is read from the margin hierarchy; this is the scenario spread
    # around it.
    "operating_margin_adjustment": 0.0,
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
    def _driver_based_revenue(context: Dict[str, Any]) -> Optional[float]:
        """Tier-3 baseline: an explicit driver decomposition declared by the caller.

        Stage 5 never invents the decomposition. Either the caller hands over the
        revenue level its drivers imply (``driver_based_revenue``), or the two
        driver facts themselves (``driver_volume`` x ``driver_price``), which is
        the volume/price split these industries actually forecast against. A
        non-positive level is not a baseline, and is refused rather than being
        carried forward as a silent zero (spec section 27).
        """
        explicit = ForecastEngine._number(context, "driver_based_revenue")
        if explicit is not None:
            return explicit if explicit > 0 else None
        volume = ForecastEngine._number(context, "driver_volume")
        price = ForecastEngine._number(context, "driver_price")
        if volume is not None and price is not None and volume > 0 and price > 0:
            return volume * price
        return None

    @staticmethod
    def _baseline_revenue(context: Dict[str, Any]) -> tuple[Optional[float], str]:
        # Tier 1: a seasonal/historical baseline Stage 4 validated as sufficient.
        if context.get("seasonality_valid") and ForecastEngine._number(context, "seasonal_baseline_revenue") is not None:
            return ForecastEngine._number(context, "seasonal_baseline_revenue"), "SEASONAL_BASELINE"
        # Tier 2: the recent run rate.
        if ForecastEngine._number(context, "recent_run_rate_revenue") is not None:
            return ForecastEngine._number(context, "recent_run_rate_revenue"), "RUN_RATE"
        # Tier 3: an explicit driver-based level, when neither history nor run
        # rate is available.
        driver_based = ForecastEngine._driver_based_revenue(context)
        if driver_based is not None:
            return driver_based, "DRIVER_BASED"
        return None, "INSUFFICIENT_DATA"

    # Operating margin is forecast on its own evidence, never derived from
    # revenue growth (spec section 22): the two may move in opposite directions.
    _OPERATING_MARGIN_KEYS = (
        ("forecast_operating_margin", "FORECAST_OPERATING_MARGIN"),
        ("recent_operating_margin", "RECENT_OPERATING_MARGIN"),
        ("historical_operating_margin", "HISTORICAL_OPERATING_MARGIN"),
    )

    @classmethod
    def _baseline_operating_margin(cls, context: Dict[str, Any]) -> tuple[Optional[float], str]:
        for key, method in cls._OPERATING_MARGIN_KEYS:
            value = ForecastEngine._number(context, key)
            if value is not None:
                return value, method
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
    # Operational FX (spec §30)
    # ------------------------------------------------------------------

    # The proxy ladder is explicit and approved one rung at a time. Each lower
    # rung is a *declared* substitute for the missing operational rate, never an
    # invented one, so the forecast can always say which currency price it used.
    _OPERATIONAL_FX_KEYS = ("operational_fx_rate", "operational_fx")

    @staticmethod
    def _operational_fx(context: Dict[str, Any]) -> Optional[OperationalFx]:
        """Resolve the operational / company FX rate.

        FREE_MARKET FX is a different concept from OPERATIONAL FX and is never
        read here. When no operational rate exists, an *explicitly declared*
        proxy may stand in — but only if the caller names it and only as an
        estimate. An undeclared gap resolves to ``None``: missing is not zero
        and is not the free-market rate.
        """
        for key in ForecastEngine._OPERATIONAL_FX_KEYS:
            value = context.get(key)
            if isinstance(value, OperationalFx):
                return value
            # An explicit None is a declared gap, not an undeclared key: it is
            # recorded on the ladder so the audit trail can name it.
            if value is None and key in context:
                break
            number = ForecastEngine._number(context, key)
            if number is not None:
                return OperationalFx(
                    rate=number,
                    source=context.get("operational_fx_source") or "DECLARED_OPERATIONAL",
                    estimated=False,
                    confidence="HIGH",
                )

        # Explicit proxy ladder. Each rung must be declared by the caller; none
        # of these is ever read on the engine's own initiative.
        proxy = context.get("operational_fx_proxy")
        if isinstance(proxy, OperationalFx):
            return proxy
        for key, basis, confidence in (
            ("operational_fx_proxy_rate", "DECLARED_PROXY", "LOW"),
            ("operational_fx_reference_rate", "DECLARED_REFERENCE_RATE", "LOW"),
        ):
            number = ForecastEngine._number(context, key)
            if number is not None:
                return OperationalFx(
                    rate=number,
                    source=context.get("operational_fx_proxy_source")
                    or "DECLARED_PROXY",
                    estimated=True,
                    proxy_basis=basis,
                    confidence=confidence,
                )
        return None

    @staticmethod
    def _free_market_fx_is_never_used(
        context: Dict[str, Any], resolved: Optional[OperationalFx]
    ) -> None:
        """Assert the free-market rate never slipped into the operational slot.

        ``free_market_fx_rate`` is a separate Stage 9 input. Reaching for it
        here would be the silent substitution the spec forbids. Where a company
        actually carries FX exposure and a free-market rate is present, the
        engine refuses to produce a forecast that could be priced at the wrong
        currency: the caller must declare an operational rate or an approved
        proxy. Without declared exposure there is nothing to reprice, so a
        free-market rate in the context is simply unused.
        """
        if resolved is not None:
            return
        if context.get("free_market_fx_rate") is None:
            return
        if ForecastEngine._fx_exposure_share(context) is None:
            return
        raise ValueError(
            "operational FX is missing while a FREE_MARKET rate is present and "
            "FX exposure is declared: the operational rate must not be "
            "silently substituted"
        )

    @staticmethod
    def _fx_ladder_snapshot(
        context: Dict[str, Any], resolved: Optional[OperationalFx]
    ) -> List[str]:
        """Which FX rungs were available, and which one was used.

        Names only what was declared: it reports the free-market rate's
        presence as an explicitly-unused input, never as a candidate.
        """
        ladder: List[str] = []
        for key in ForecastEngine._OPERATIONAL_FX_KEYS:
            if key in context:
                ladder.append(
                    f"{key}:DECLARED" if context.get(key) is not None
                    else f"{key}:DECLARED_MISSING"
                )
        if "operational_fx_proxy" in context:
            ladder.append(
                "operational_fx_proxy:DECLARED"
                if context.get("operational_fx_proxy") is not None
                else "operational_fx_proxy:DECLARED_MISSING"
            )
        for key in ("operational_fx_proxy_rate", "operational_fx_reference_rate"):
            if context.get(key) is not None:
                ladder.append(f"{key}:DECLARED")
        if context.get("free_market_fx_rate") is not None:
            ladder.append("free_market_fx_rate:PRESENT_UNUSED")
        if resolved is not None:
            ladder.append(f"resolved:{resolved.source}")
        return ladder

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
        margin_adjustment_base: float = 0.0,
    ) -> SingleForecastChain:
        """One non-financial scenario of the common chain.

        Revenue and operating margin are resolved from two independent evidence
        hierarchies (spec section 22): the margin is never read off revenue
        growth, so revenue may rise while margin falls — and operating profit
        may fall while revenue rises.

        ``margin_adjustment_base`` shifts the whole margin hierarchy. It is the
        caller's declared view of margin direction, distinct from the scenario
        ``margin_adjustment`` spread, so a margin move is expressible without
        having to pretend it is a revenue effect.
        """
        base_op_margin, margin_method = self._baseline_operating_margin(context)
        if base_op_margin is None:
            return SingleForecastChain(method="INSUFFICIENT_DATA",
                                       assumptions={"reason": "missing_operating_margin"})

        # Margins are stored as decimal ratios in the Stage 5 input contract.
        op_margin = base_op_margin + margin_adjustment + margin_adjustment_base
        net_margin = self._baseline_value(
            context, "forecast_net_margin", "historical_net_margin", "recent_net_margin"
        )
        conversion = self._number(context, "historical_net_operating_conversion")
        components = self._net_profit_components(context)

        scenario_assumptions = {
            "scenario": scenario_name,
            "baseline_method": baseline_method,
            "operating_margin_method": margin_method,
            "trend_adjustment": trend_adjustment,
            "low_base_control": bool(context.get("low_base") or context.get("LOW_BASE")),
            "net_profit_method_hierarchy": list(NET_PROFIT_HIERARCHY),
        }

        # Explicit, traceable driver adjustments may be supplied by the caller.
        # No external/FX assumption is invented here.
        explicit_driver_adjustment = self._number(context, "driver_revenue_adjustment")
        if explicit_driver_adjustment is not None:
            growth += explicit_driver_adjustment
            scenario_assumptions["driver_revenue_adjustment"] = explicit_driver_adjustment

        revenue = baseline_revenue * (1.0 + growth)

        # Operating earnings that are genuinely FX-linked are repriced on the
        # operational rate only (spec §30). Only the caller-declared exposed
        # share of revenue moves, and a genuinely missing operational rate
        # leaves the whole FX effect unapplied rather than priced at the
        # free-market rate.
        exposure = self._fx_exposure_share(context)
        fx = self._operational_fx(context)
        if fx is not None and exposure is not None and fx.rate is not None:
            if exposure > 0.0:
                fx_move = self._fx_move(context, fx)
                if fx_move is not None:
                    revenue, fx_applied = self._apply_fx_to_revenue(
                        revenue, exposure, fx_move
                    )
                    scenario_assumptions["fx"] = fx_applied
                    scenario_assumptions["operational_fx_provenance"] = fx.provenance()

        return ForecastDriver.build_non_financial_chain(
            revenue=revenue,
            operating_margin=op_margin,
            share_count=self._share_count(context),
            non_operating_items=components["non_operating_items"],
            financial_costs=components["financial_costs"],
            tax=components["tax"],
            net_operating_conversion=conversion,
            net_margin=None if conversion is not None else (
                None if net_margin is None else net_margin + net_margin_adjustment
            ),
            beginning_equity=self._number(context, "beginning_equity"),
            ending_equity=self._number(context, "forecast_ending_equity"),
            method_hint=baseline_method,
            assumptions=scenario_assumptions,
        )

    @staticmethod
    def _fx_exposure_share(context: Dict[str, Any]) -> Optional[float]:
        """Share of revenue genuinely exposed to the operational FX rate."""
        for key in ("fx_exposed_revenue_share", "fx_revenue_share"):
            value = ForecastEngine._number(context, key)
            if value is not None:
                return value
        return None

    @staticmethod
    def _fx_base_rate(context: Dict[str, Any]) -> Optional[float]:
        return ForecastEngine._number(context, "operational_fx_base_rate")

    @staticmethod
    def _fx_move(context: Dict[str, Any], fx: OperationalFx) -> Optional[float]:
        """FX move as a decimal revenue effect.

        Declared as ``fx_revenue_sensitivity``, which is how much revenue moves
        for a 1% move in the rate. The engine never assumes a pass-through.
        """
        sensitivity = ForecastEngine._number(context, "fx_revenue_sensitivity")
        if sensitivity is None:
            return None
        base_rate = ForecastEngine._fx_base_rate(context)
        if base_rate is None or base_rate == 0 or fx.rate is None:
            return None
        pct_move = (fx.rate - base_rate) / abs(base_rate)
        return pct_move * sensitivity

    @staticmethod
    def _apply_fx_to_revenue(
        revenue: float, exposure: float, fx_move: Optional[float]
    ) -> tuple[float, Optional[Dict[str, Any]]]:
        if fx_move is None:
            return revenue, None
        exposed = revenue * exposure
        adjusted = revenue + exposed * fx_move
        return adjusted, {
            "exposure_share": round(float(exposure), 6),
            "fx_move": round(float(fx_move), 6),
            "exposed_revenue": ForecastDriver._round(exposed),
            "operational_fx_source": "OPERATIONAL",
        }

    @staticmethod
    def _net_profit_components(context: Dict[str, Any]) -> Dict[str, Optional[float]]:
        """Component-based net profit inputs, as declared and never invented.

        The component path is only taken when every component is present, so a
        partially-supplied set degrades to the historical conversion instead of
        silently filling the gap with a fabricated tax or financial cost.
        """
        return {
            name: ForecastEngine._number(context, key)
            for name, key in (
                ("non_operating_items", "forecast_non_operating_items"),
                ("financial_costs", "forecast_financial_costs"),
                ("tax", "forecast_tax"),
            )
        }

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
        margin_adjustment = float(params.get("operating_margin_adjustment", 0.0))

        benchmark = None
        resolved_fx = self._operational_fx(financial_context)
        # FREE_MARKET and OPERATIONAL FX are separate concepts. A company that
        # actually carries FX exposure must not be priced at the free-market
        # rate when the operational rate is missing; a company with no declared
        # exposure has nothing to reprice, so the presence of a free-market rate
        # in its context is simply unused rather than a silent substitution.
        self._free_market_fx_is_never_used(financial_context, resolved_fx)
        assumptions: Dict[str, Any] = {
            "model_parameters": params,
            "trend_evidence": trend_state or financial_context.get("trend_state"),
            "sign_change": financial_context.get("sign_change"),
            "low_base": bool(financial_context.get("low_base") or financial_context.get("LOW_BASE")),
            "operational_fx": resolved_fx.rate if resolved_fx is not None else None,
            "operational_fx_source": resolved_fx.source if resolved_fx is not None else None,
            "operational_fx_available": resolved_fx is not None,
            "operational_fx_estimated": (
                resolved_fx.estimated if resolved_fx is not None else None
            ),
            "operational_fx_confidence": (
                resolved_fx.confidence if resolved_fx is not None else None
            ),
            "fx_ladder": self._fx_ladder_snapshot(financial_context, resolved_fx),
            "data_cutoff_datetime": cutoff.isoformat(),
            "pit_valid": pit_ok,
            "input_refs": [
                {"fact_key": ref.fact_key, "report_version_id": ref.report_version_id,
                 "available_at": ref.available_at.isoformat() if ref.available_at else None,
                 "source": ref.source}
                for ref in input_refs
            ],
        }
        if resolved_fx is not None and resolved_fx.is_proxy():
            assumptions["operational_fx_proxy"] = resolved_fx.provenance()
        if violation is not None:
            assumptions["pit_violation"] = {
                "fact_key": violation.fact_key,
                "available_at": violation.available_at.isoformat(),
                "cutoff": cutoff.isoformat(),
                "action": "input_dropped",
            }

        if industry_code in NON_FINANCIAL_INDUSTRIES:
            baseline_revenue, baseline_method = self._baseline_revenue(financial_context)
            exposure = self._fx_exposure_share(financial_context)
            seasonal_naive_revenue = self._number(financial_context, "seasonal_naive_revenue")
            if seasonal_naive_revenue is not None:
                benchmark = SingleForecastChain(revenue=round(seasonal_naive_revenue, 6), method="SEASONAL_NAIVE", quality="BENCHMARK")

            if baseline_revenue is None:
                exposure = None
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
                                                    0.0, 0.0, "BASE", trend_adj,
                                                    margin_adjustment_base=margin_adjustment)
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
            # The bank never enters the non-financial revenue model. NII is its
            # own baseline; loans/deposits and credit quality ride along as
            # context and never as profit multipliers. The bank carries no
            # revenue-side FX exposure, so the free-market guard cannot apply.
            exposure = None
            base_nii = self._number(financial_context, "base_nii")
            nii_growth = self._number(financial_context, "baseline_nii_growth")
            if nii_growth is None:
                nii_growth = 0.0
            nii_growth += trend_adj
            bear_g, base_g, bull_g = nii_growth - financial_spread, nii_growth, nii_growth + financial_spread
            bank_kwargs = {
                "net_profit_conversion": self._number(financial_context, "bank_net_profit_nii_conversion"),
                "forecast_net_profit": self._number(financial_context, "forecast_net_profit"),
                "beginning_equity": self._number(financial_context, "beginning_equity"),
                "ending_equity": self._number(financial_context, "forecast_ending_equity"),
                "npl_ratio": self._number(financial_context, "npl_ratio"),
                "nim": self._number(financial_context, "nim"),
                "loan_growth": self._number(financial_context, "loan_growth"),
                "deposit_growth": self._number(financial_context, "deposit_growth"),
            }
            scenarios = ScenarioForecastResult(
                ForecastDriver.build_bank_chain(base_nii, bear_g, self._share_count(financial_context),
                                                assumptions={"scenario": "BEAR"}, **bank_kwargs),
                ForecastDriver.build_bank_chain(base_nii, base_g, self._share_count(financial_context),
                                                assumptions={"scenario": "BASE"}, **bank_kwargs),
                ForecastDriver.build_bank_chain(base_nii, bull_g, self._share_count(financial_context),
                                                assumptions={"scenario": "BULL"}, **bank_kwargs),
            )

        else:
            baseline_method = "HOLDING_SPECIALIZED"
            # NAV conversion carries no revenue-side FX exposure.
            exposure = None
            base_nav = self._number(financial_context, "base_nav")
            nav_growth = self._number(financial_context, "baseline_nav_growth")
            if nav_growth is None:
                nav_growth = 0.00
            nav_growth += trend_adj
            bear_g, base_g, bull_g = nav_growth - financial_spread, nav_growth, nav_growth + financial_spread
            shares = self._share_count(financial_context)
            conversion = self._number(financial_context, "holding_net_profit_nav_conversion")
            holding_kwargs = {
                "forecast_net_profit": self._number(financial_context, "forecast_net_profit"),
                "beginning_equity": self._number(financial_context, "beginning_equity"),
                "ending_equity": self._number(financial_context, "forecast_ending_equity"),
            }
            scenarios = ScenarioForecastResult(
                ForecastDriver.build_holding_chain(base_nav, bear_g, shares, net_profit_conversion=conversion,
                                                   assumptions={"scenario": "BEAR"}, **holding_kwargs),
                ForecastDriver.build_holding_chain(base_nav, base_g, shares, net_profit_conversion=conversion,
                                                   assumptions={"scenario": "BASE"}, **holding_kwargs),
                ForecastDriver.build_holding_chain(base_nav, bull_g, shares, net_profit_conversion=conversion,
                                                   assumptions={"scenario": "BULL"}, **holding_kwargs),
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

        # Provenance Stage 5 does not own: the caller's declarations are stored
        # verbatim so a stored record can still name its inputs. Kept under a
        # leading underscore to keep it out of the round-tripped assumptions
        # payload, where it belongs to the stored input_refs instead.
        provenance = financial_context.get("stage4_provenance")
        if provenance:
            assumptions["__stage4_provenance"] = dict(provenance)
        declared_refs = financial_context.get("input_refs")
        if declared_refs:
            assumptions["__declared_input_refs"] = tuple(
                ref if isinstance(ref, ForecastInputRef)
                else ForecastInputRef.from_mapping(ref)
                for ref in declared_refs
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
            calculation_timestamp=calculation_at,
            data_quality=quality if industry_code in NON_FINANCIAL_INDUSTRIES else (
                "MEDIUM" if scenarios.base.quality != "INSUFFICIENT_DATA" else "INSUFFICIENT_DATA"
            ),
            assumptions=assumptions,
            benchmark=benchmark,
        )
