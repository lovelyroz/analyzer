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


# The scenario spreads are declared Stage 5 model parameters. They are not
# derived from Stage 4's ±2% direction band, from momentum, from the
# Fundamental Score, from an arbitrary percentage of the forecast, or from a
# volatility estimate the engine invented out of a missing observation. Each
# one names its own basis on the record so an auditor can see it came from the
# declared model and not from an evidence stream the spec isolates (spec §16,
# §21, §23). The four keys below are the complete vocabulary of scenario
# uncertainty in this engine: a spread that is not one of them does not exist.
SCENARIO_SPREAD_KEYS = (
    "scenario_revenue_growth_spread",
    "scenario_operating_margin_spread",
    "scenario_net_margin_spread",
    "scenario_financial_growth_spread",
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
    def _trend_adjustment(context: Dict[str, Any], trend_state: Optional[str],
                          params: Dict[str, Any], low_base: bool = False
                          ) -> tuple[float, str]:
        """Translate Stage 4 trend evidence into a growth adjustment, or refuse to.

        Stage 4 is evidence only. An explicit ``model_parameters["trend_adjustments"]``
        entry is required before the evidence can move the forecast, and the
        adjustment is never derived from Stage 4's momentum percentage: the
        Stage 4 ``±2%`` band classifies trend direction, it is not a Stage 5
        forecast growth magnitude (spec section 16). Returns the adjustment and
        the reason it was or was not applied, so the audit trail can name it.
        """
        state = trend_state or context.get("trend_state")
        if low_base:
            return 0.0, "SUPPRESSED_LOW_BASE"
        mapping = params.get("trend_adjustments") or {}
        if state not in mapping:
            return 0.0, "NO_MODEL_PARAMETER"
        value = mapping[state]
        if not isinstance(value, (int, float)):
            return 0.0, "NO_MODEL_PARAMETER"
        return float(value), "MODEL_PARAMETER"

    # Stage 4 sign transitions, carried as semantic classifications and never
    # converted into percentage growth rates (spec section 19). A transition
    # across zero has no ordinary percentage reading: (new - old) / old is
    # meaningless when the prior period is the zero or the sign flip itself, so
    # these cases never travel through the ordinary growth path.
    SIGN_CHANGE_TRANSITIONS = frozenset({
        "LOSS_TO_PROFIT",
        "PROFIT_TO_LOSS",
        "SIGN_CHANGE",
    })

    @classmethod
    def _sign_change(cls, context: Dict[str, Any]) -> Optional[str]:
        return context.get("sign_change") if isinstance(
            context.get("sign_change"), str) else None

    @classmethod
    def _is_sign_transition(cls, context: Dict[str, Any]) -> bool:
        sign_change = cls._sign_change(context)
        return sign_change in cls.SIGN_CHANGE_TRANSITIONS

    @staticmethod
    def _safe_growth_rate(prior: Optional[float], current: Optional[float]
                          ) -> Optional[float]:
        """Percentage growth that is undefined across zero, never invented.

        ``None`` is returned whenever a percentage reading is not defined: a
        missing endpoint, either endpoint being zero (a zero-base transition is
        not a growth rate), or the two endpoints carrying different signs.
        Callers must treat ``None`` as "no ordinary percentage growth exists",
        not as zero.
        """
        if prior is None or current is None:
            return None
        if prior == 0 or current == 0:
            return None
        if (prior < 0) != (current < 0):
            return None
        return (current - prior) / abs(prior)

    # The Stage 4 low-base flag only names the condition; it is not itself a
    # recovery percentage or a growth rate. Stage 5 keeps it as a control that
    # disables the momentum-derived adjustment and records its own evidence
    # state, so the forecast stays anchored to the declared baseline hierarchy.
    @classmethod
    def _low_base_control(cls, context: Dict[str, Any]) -> tuple[bool, str]:
        """Classify a low base into: flag set, evidence state, or nothing to say.

        ``low_base`` stays ``False`` unless evidence actually supports it, so a
        caller-supplied flag cannot manufacture a low-base treatment the
        underlying numbers do not show. Returns the control and the evidence
        state recorded on the chain for the audit trail.
        """
        declared = bool(context.get("low_base") or context.get("LOW_BASE"))
        if cls._is_sign_transition(context):
            return True, "GROWTH_REFUSED_SIGN_TRANSITION"
        prior = ForecastEngine._number(context, "prior_revenue")
        current = ForecastEngine._number(context, "current_revenue")
        if prior is not None and prior <= 0 and current is not None and current > 0:
            return True, "GROWTH_REFUSED_ZERO_BASE"
        if prior is None or current is None:
            return declared, (
                "LOW_BASE_DECLARED_INSUFFICIENT_EVIDENCE" if declared
                else "NO_LOW_BASE_EVIDENCE")
        return declared, (
            "LOW_BASE_DECLARED" if declared else "NO_LOW_BASE_EVIDENCE")

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

    # Stage 5's EPS contract divides profit *attributable to common
    # shareholders* (05_Stage5_Forecast_Engine.md section 9). Stage 1 exposes
    # only NET_PROFIT, so whether that total is the attributable amount is the
    # caller's statement about its data, not the engine's assumption.
    _EPS_ATTRIBUTABLE_BASIS_KEY = "eps_attributable_basis"
    _UNVERIFIED_TOTAL_NET_PROFIT = "UNVERIFIED_TOTAL_NET_PROFIT"

    # The keys a caller may declare to make that statement.
    _ATTRIBUTABLE_AMOUNT_KEY = "net_profit_attributable"
    _ATTRIBUTABLE_EQUIVALENCE_KEY = "net_profit_is_attributable"

    @classmethod
    def _eps_attributable_basis(cls, context: Dict[str, Any]) -> str:
        """The basis on which net profit may be called attributable.

        ``UNVERIFIED_TOTAL_NET_PROFIT`` is not a basis the engine may divide on:
        it means the caller said nothing, and Stage 1 alone does not establish
        the equivalence (no NET_PROFIT_ATTRIBUTABLE metric, no documented
        equivalence, and no minority-interest fields to isolate the attributable
        portion by subtraction).
        """
        if ForecastEngine._number(context, cls._ATTRIBUTABLE_AMOUNT_KEY) is not None:
            return "CALLER_DECLARED_NET_PROFIT_ATTRIBUTABLE"
        if context.get(cls._ATTRIBUTABLE_EQUIVALENCE_KEY) is True:
            return "CALLER_DECLARED_EQUIVALENCE"
        return cls._UNVERIFIED_TOTAL_NET_PROFIT

    @classmethod
    def _attributable_net_profit(cls, context: Dict[str, Any],
                                 net_profit: Optional[float]) -> Optional[float]:
        """The EPS numerator, or ``None`` when its basis is unverified.

        Neither the total nor a minority-interest amount is invented: a caller
        who has the attributable figure hands it over, and a caller who knows
        their reporting regime publishes no minority interest says so. Anything
        else leaves the numerator unknown, so EPS records INSUFFICIENT rather
        than dividing an unverified total.
        """
        if net_profit is None:
            return None
        declared = ForecastEngine._number(context, cls._ATTRIBUTABLE_AMOUNT_KEY)
        if declared is not None:
            return declared
        if context.get(cls._ATTRIBUTABLE_EQUIVALENCE_KEY) is True:
            return net_profit
        return None

    @classmethod
    def _eps(cls, context: Dict[str, Any], net_profit: Optional[float],
             shares: Optional[float]) -> tuple[Optional[float], Optional[str]]:
        """EPS over the weighted-average share base, naming its own basis.

        Returns the EPS and the reason it is missing when it is, because a
        ``None`` here means two different things: no share base at all, or a
        numerator whose attributable basis the caller did not establish. Both
        keep EPS absent, but only the second is an insufficient-data condition
        on a chain that otherwise produced a forecast.
        """
        if shares is None or shares <= 0:
            return None, "missing_share_base"
        attributable = cls._attributable_net_profit(context, net_profit)
        if attributable is None:
            return None, "unverified_attributable_profit"
        return attributable / shares, None

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
    # Scenario uncertainty (spec section 21)
    # ------------------------------------------------------------------

    # Dispersion is never invented from a missing volatility observation: the
    # engine names the evidence it actually used, and reports the absence when
    # there is none. The defaults below are the already-established Stage 5
    # model parameters, not new arbitrary spreads.
    _UNCERTAINTY_EVIDENCE_KEYS = (
        "revenue_volatility",
        "historical_revenue_volatility",
        "earnings_volatility",
        "forecast_uncertainty",
    )

    @classmethod
    def _uncertainty_evidence(cls, context: Dict[str, Any]) -> Optional[float]:
        """An observed dispersion figure the caller declared, or nothing.

        Stage 5 never manufactures dispersion from thin air and never derives a
        spread from missing data. ``None`` means the evidence is unavailable and
        the caller must accept the model's declared default spread as the only
        dispersion there is.
        """
        return cls._baseline_value(context, *cls._UNCERTAINTY_EVIDENCE_KEYS)

    @classmethod
    def _scenario_spread(
        cls,
        params: Dict[str, Any],
        key: str,
        fallback_key: str,
        evidence: Optional[float],
        context: Dict[str, Any],
    ) -> tuple[float, str, Optional[str]]:
        """Resolve one scenario spread and name where it came from.

        The value follows the established resolution unchanged: the caller's
        declared model parameter when it names this key, otherwise the model's
        own value for the slot. What this method adds is a truthful basis:
        ``MODEL_PARAMETER`` only when the caller declared a value for this
        key, ``MODEL_DEFAULT`` when the model's own default stands. No Stage
        4 ±2% direction band, no momentum reading and no Fundamental Score is
        consulted at any point (spec §16, §21, §23).

        A declared volatility observation may widen or narrow either base —
        through the caller's own declared sensitivity, never through an
        invented multiplier — and missing evidence leaves the base untouched
        rather than being filled with a fabricated dispersion estimate.

        Returns the spread, its basis, and the evidence stream that did *not*
        contribute, so a stored record can always say which of the model's own
        parameters a scenario moved away from and which isolated inputs it
        ignored.
        """
        if key not in SCENARIO_SPREAD_KEYS:
            raise ValueError(f"unknown scenario spread parameter: {key!r}")
        declared = float(params.get(fallback_key, 0.0))
        parameter = params.get(key)
        if parameter is None or not isinstance(parameter, (int, float)):
            # No usable value for this key, so the model's own value for the
            # slot stands. Nothing else is consulted: no Stage 4 band, no
            # momentum reading and no Fundamental Score can fill that slot.
            return declared, "MODEL_DEFAULT", None
        if evidence is None:
            return float(parameter), "MODEL_PARAMETER", None
        sensitivity = ForecastEngine._number(context, "volatility_sensitivity")
        if not isinstance(sensitivity, (int, float)) or sensitivity <= 0:
            return float(parameter), "MODEL_PARAMETER", \
                "VOLATILITY_EVIDENCE_WITHOUT_DECLARED_SENSITIVITY"
        return float(parameter) * float(sensitivity) * float(evidence), \
            "VOLATILITY_EVIDENCE", None

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

    # Facts the engine reads as numbers. Provenance for one of these is not
    # optional decoration: a numeric value whose declared publication is after
    # the cutoff is look-ahead data, and dropping only the ref while keeping the
    # number would let a late fact into the calculation through a channel the
    # ref guard never touched (spec §25). Where a mandatory fact has no declared
    # provenance at all the engine records the absence rather than trusting the
    # value on its own.
    _PIT_GUARDED_FACT_KEYS = frozenset({
        "prior_revenue",
        "current_revenue",
        "seasonal_baseline_revenue",
        "recent_run_rate_revenue",
        "seasonal_naive_revenue",
        "driver_based_revenue",
        "driver_volume",
        "driver_price",
        "historical_operating_margin",
        "forecast_operating_margin",
        "recent_operating_margin",
        "historical_net_margin",
        "forecast_net_margin",
        "recent_net_margin",
        "beginning_equity",
        "forecast_ending_equity",
        "forecast_net_profit",
        "base_nii",
        "forecast_nii",
        "base_nav",
        "net_profit_attributable",
    })

    @staticmethod
    def _pit_guarded_context(
        context: Dict[str, Any],
        refs: List[ForecastInputRef],
        cutoff: datetime,
    ) -> tuple[Dict[str, Any], List[str]]:
        """Remove numeric facts whose own declared provenance is post-cutoff.

        Filtering the refs alone is not enough (Prompt 14 concern D): the number
        stays in the context and would still be read. This walks the refs a
        second time and drops the *value* for any guarded key that declared a
        publication later than the cutoff. Facts named by a ref whose
        ``available_at`` is absent are left in place — provenance is opt-in for
        the caller — but a key the model treats as mandatory is recorded so the
        audit trail can say it was used undeclared rather than silently trusted.
        """
        late = {
            ref.fact_key for ref in refs
            if ref.available_at is not None
            and normalize_datetime(ref.available_at) > normalize_datetime(cutoff)
        }
        if not late:
            return context, []
        guarded = dict(context)
        for key in late:
            if key in guarded:
                guarded.pop(key, None)
        return guarded, sorted(late)

    @staticmethod
    def _undeclared_mandatory_facts(
        context: Dict[str, Any],
        refs: List[ForecastInputRef],
    ) -> List[str]:
        """Guarded facts present as numbers but carrying no declared provenance."""
        provenanced = {ref.fact_key for ref in refs}
        return sorted(
            key for key in ForecastEngine._PIT_GUARDED_FACT_KEYS
            if key in context and key not in provenanced
        )

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
            "trend_adjustment_reason": context.get("__trend_adjustment_reason"),
            "low_base_control": bool(context.get("low_base") or context.get("LOW_BASE")),
            "low_base_evidence": context.get("__low_base_evidence"),
            "sign_change": ForecastEngine._sign_change(context),
            "growth_rate_basis": context.get("__growth_rate_basis"),
            "uncertainty_evidence": context.get("__uncertainty_evidence"),
            "uncertainty_basis": context.get("__uncertainty_basis"),
            "net_profit_method_hierarchy": list(NET_PROFIT_HIERARCHY),
            "eps_attributable_basis": self._eps_attributable_basis(context),
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

        # EPS needs the numerator, so the engine resolves the forecast net
        # profit here and passes the driver its already-computed EPS. The tiers
        # are the driver's own, in the driver's own order, so the two cannot
        # disagree about which net profit was built. The margin the engine
        # resolves must be the same margin the driver divides: the scenario's
        # own margin adjustment, not the unadjusted base level.
        scenario_margin = None if conversion is not None else (
            None if net_margin is None else net_margin + net_margin_adjustment)
        forecast_np = self._forecast_net_profit(
            context, revenue, revenue * op_margin,
            net_margin_override=scenario_margin)
        eps, eps_reason = self._eps(context, forecast_np, self._share_count(context))
        if eps_reason is not None and forecast_np is not None:
            scenario_assumptions["eps_reason"] = eps_reason
        return ForecastDriver.build_non_financial_chain(
            revenue=revenue,
            operating_margin=op_margin,
            share_count=self._share_count(context),
            non_operating_items=components["non_operating_items"],
            financial_costs=components["financial_costs"],
            tax=components["tax"],
            net_operating_conversion=conversion,
            net_margin=scenario_margin,
            beginning_equity=self._number(context, "beginning_equity"),
            ending_equity=self._number(context, "forecast_ending_equity"),
            method_hint=baseline_method,
            assumptions=scenario_assumptions,
            eps=eps,
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

    @staticmethod
    def _forecast_net_profit(
        context: Dict[str, Any],
        revenue: Optional[float],
        operating_profit: Optional[float],
        net_margin_override: Optional[float],
    ) -> Optional[float]:
        """Resolve the forecast net profit the driver's own hierarchy resolves.

        EPS needs the numerator, so the engine resolves it here and hands the
        driver its already-computed EPS. The tiers are the driver's, kept in the
        same order, so the two cannot drift apart.
        """
        components = ForecastEngine._net_profit_components(context)
        if all(v is not None for v in components.values()):
            return operating_profit + components["non_operating_items"] \
                - components["financial_costs"] - components["tax"]
        conversion = ForecastEngine._number(context, "historical_net_operating_conversion")
        if conversion is not None:
            return None if operating_profit is None else operating_profit * conversion
        if net_margin_override is not None and revenue is not None:
            return revenue * net_margin_override
        return ForecastEngine._number(context, "forecast_net_profit")

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
        sign_change = self._sign_change(financial_context)

        # Point-in-Time: a forecast may only use inputs published at or before
        # its cutoff (spec §25). Late inputs are dropped, never silently kept.
        raw_refs = self._raw_input_refs(financial_context)
        pit_ok, input_refs, violation = self._pit_safe(financial_context, raw_refs, cutoff)
        # Dropping the ref is not enough on its own (Prompt 14 concern D): the
        # numeric value would remain in the context and the engine would still
        # divide it. So the values behind late declarations are removed from the
        # context the calculation actually reads.
        guarded_context, late_values = self._pit_guarded_context(
            financial_context, raw_refs, cutoff)
        undeclared_mandatory = self._undeclared_mandatory_facts(
            guarded_context, input_refs)
        # Everything below reads the guarded context, so a numeric value whose
        # provenance is post-cutoff is absent from the calculation itself, not
        # merely absent from the audit trail.
        context = guarded_context

        # The low-base control is resolved after the PIT guard because it reads
        # the same prior/current revenue pair: a late fact must not be able to
        # manufacture a low-base reading either. A sign transition or a zero base
        # is a low-base condition and suppresses the momentum-derived adjustment
        # before that adjustment is ever computed.
        low_base_control, low_base_evidence = self._low_base_control(context)
        low_base = low_base_control or bool(
            context.get("low_base") or context.get("LOW_BASE"))
        trend_adj, trend_reason = self._trend_adjustment(
            context, trend_state, params, low_base=low_base)

        calculation_at = normalize_datetime(
            financial_context.get("calculation_timestamp")
        ) or datetime.now(timezone.utc)
        if calculation_at < cutoff:
            raise ValueError(
                "calculation_timestamp precedes data_cutoff_datetime: the forecast "
                "would be dated before the information it claims to see"
            )

        scenario_spread, spread_basis, spread_note = self._scenario_spread(
            params, "scenario_revenue_growth_spread", "scenario_revenue_growth_spread",
            self._uncertainty_evidence(context), context)
        financial_spread, financial_basis, financial_note = self._scenario_spread(
            params, "scenario_financial_growth_spread",
            "scenario_revenue_growth_spread", self._uncertainty_evidence(context),
            context)
        margin_spread, margin_basis, margin_note = self._scenario_spread(
            params, "scenario_operating_margin_spread",
            "scenario_operating_margin_spread", None, context)
        net_margin_spread, net_margin_basis, net_margin_note = self._scenario_spread(
            params, "scenario_net_margin_spread", "scenario_net_margin_spread",
            None, context)
        # Each spread carries its own basis, so an auditor never has to infer
        # which model parameter a scenario moved away from. The keys are the
        # model's complete spread vocabulary: anything not named here was never
        # consulted.
        spread_bases = {
            "revenue": spread_basis,
            "financial": financial_basis,
            "operating_margin": margin_basis,
            "net_margin": net_margin_basis,
        }
        spread_notes = {
            key: note for key, note in (
                ("revenue", spread_note),
                ("financial", financial_note),
                ("operating_margin", margin_note),
                ("net_margin", net_margin_note),
            ) if note is not None
        }
        margin_adjustment = float(params.get("operating_margin_adjustment", 0.0))

        benchmark = None
        resolved_fx = self._operational_fx(context)
        # FREE_MARKET and OPERATIONAL FX are separate concepts. A company that
        # actually carries FX exposure must not be priced at the free-market
        # rate when the operational rate is missing; a company with no declared
        # exposure has nothing to reprice, so the presence of a free-market rate
        # in its context is simply unused rather than a silent substitution.
        self._free_market_fx_is_never_used(context, resolved_fx)
        assumptions: Dict[str, Any] = {
            "model_parameters": params,
            "trend_evidence": trend_state or context.get("trend_state"),
            "sign_change": sign_change,
            "sign_transition": self._is_sign_transition(context),
            "trend_adjustment": trend_adj,
            "trend_adjustment_reason": trend_reason,
            "low_base": low_base,
            "operational_fx": resolved_fx.rate if resolved_fx is not None else None,
            "operational_fx_source": resolved_fx.source if resolved_fx is not None else None,
            "operational_fx_available": resolved_fx is not None,
            "operational_fx_estimated": (
                resolved_fx.estimated if resolved_fx is not None else None
            ),
            "operational_fx_confidence": (
                resolved_fx.confidence if resolved_fx is not None else None
            ),
            "fx_ladder": self._fx_ladder_snapshot(context, resolved_fx),
            "uncertainty_evidence": self._uncertainty_evidence(context),
            "uncertainty_basis": spread_basis,
            "scenario_revenue_growth_spread": scenario_spread,
            "scenario_financial_growth_spread": financial_spread,
            "scenario_operating_margin_spread": margin_spread,
            "scenario_net_margin_spread": net_margin_spread,
            "scenario_spread_bases": spread_bases,
            "scenario_spread_model_parameters": {
                key: params.get(key) for key in SCENARIO_SPREAD_KEYS
            },
            "scenario_spread_evidence_notes": spread_notes,
            # The evidence streams Stage 5 must never read as a spread. Naming
            # them here means a reviewer can confirm they were ignored rather
            # than having to prove a negative.
            "scenario_spread_excluded_inputs": (
                "stage4_trend_threshold",
                "momentum_12m_pct",
                "fundamental_score",
                "p_nav",
            ),
            "data_cutoff_datetime": cutoff.isoformat(),
            "pit_valid": pit_ok,
            "eps_attributable_basis": self._eps_attributable_basis(context),
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
        # A late numeric value is dropped with its ref, so both halves of the
        # same violation are named. An empty list means nothing was late.
        assumptions["pit_dropped_values"] = list(late_values)
        # Guarded facts that reached the calculation without any declared
        # provenance. Provenance is opt-in for the caller, so these are not
        # rejected — but they are never trusted silently either, and the record
        # says which mandatory inputs were used undeclared.
        assumptions["undeclared_mandatory_inputs"] = list(undeclared_mandatory)

        if industry_code in NON_FINANCIAL_INDUSTRIES:
            baseline_revenue, baseline_method = self._baseline_revenue(context)
            exposure = self._fx_exposure_share(context)
            seasonal_naive_revenue = self._number(context, "seasonal_naive_revenue")
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
                # Growth is resolved through the existing baseline/driver
                # hierarchy: the declared growth parameter, the zero-safe
                # reading of the historical arc, then flat. A sign transition
                # or a zero base never yields an ordinary percentage growth.
                low_base_control, low_base_evidence = self._low_base_control(
                    context)
                assumptions["low_base_evidence"] = low_base_evidence
                computed_growth = self._safe_growth_rate(
                    self._number(context, "prior_revenue"),
                    self._number(context, "current_revenue"))
                declared_growth = self._number(context, "baseline_revenue_growth")

                # ``baseline_revenue_growth`` is an explicit caller declaration,
                # not a model parameter and not a derived reading. It outranks
                # the historical arc because the caller is answerable for the
                # growth it declares, while the arc is only what the reported
                # numbers happened to show. Its precedence is recorded as
                # DECLARED_GROWTH_PARAMETER so a stored forecast always names
                # which of the two produced it, and it can never displace a
                # growth the engine computed: when it is absent the historical
                # arc, and only the historical arc, supplies the rate.
                if declared_growth is not None:
                    base_growth = declared_growth
                    growth_basis = "DECLARED_GROWTH_PARAMETER"
                elif computed_growth is not None:
                    base_growth = computed_growth
                    growth_basis = "ZERO_SAFE_GROWTH"
                elif self._is_sign_transition(context):
                    base_growth = 0.0
                    growth_basis = "FLAT_SIGN_TRANSITION"
                elif computed_growth is None and (
                        self._number(context, "prior_revenue") is None
                        or self._number(context, "current_revenue") is None):
                    base_growth = 0.0
                    growth_basis = "FLAT_INSUFFICIENT_EVIDENCE"
                elif computed_growth is None and (
                        self._number(context, "prior_revenue") <= 0
                        or self._number(context, "current_revenue") <= 0):
                    base_growth = 0.0
                    growth_basis = "FLAT_ZERO_BASE"
                else:
                    base_growth = 0.0
                    growth_basis = (
                        "FLAT_INSUFFICIENT_EVIDENCE"
                        if low_base_evidence == "LOW_BASE_DECLARED_INSUFFICIENT_EVIDENCE"
                        else "FLAT_NO_DECLARED_GROWTH")

                base_growth += trend_adj
                bear_growth = base_growth - scenario_spread
                bull_growth = base_growth + scenario_spread

                scenario_context = dict(context)
                scenario_context.update({
                    "__trend_adjustment_reason": trend_reason,
                    "__low_base_evidence": low_base_evidence,
                    "__growth_rate_basis": growth_basis,
                    "__growth_rate_prior_revenue": self._number(
                        context, "prior_revenue"),
                    "__growth_rate_current_revenue": self._number(
                        context, "current_revenue"),
                    "__uncertainty_evidence": self._uncertainty_evidence(context),
                    "__uncertainty_basis": spread_basis,
                })
                if low_base_control:
                    scenario_context["low_base"] = True

                bear = self._non_financial_scenario(scenario_context, baseline_revenue, baseline_method, bear_growth,
                                                    -margin_spread, -net_margin_spread, "BEAR", trend_adj)
                base = self._non_financial_scenario(scenario_context, baseline_revenue, baseline_method, base_growth,
                                                    0.0, 0.0, "BASE", trend_adj,
                                                    margin_adjustment_base=margin_adjustment)
                bull = self._non_financial_scenario(scenario_context, baseline_revenue, baseline_method, bull_growth,
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
            base_nii = self._number(context, "base_nii")
            nii_growth = self._number(context, "baseline_nii_growth")
            if nii_growth is None:
                nii_growth = 0.0
            nii_growth += trend_adj
            bear_g, base_g, bull_g = nii_growth - financial_spread, nii_growth, nii_growth + financial_spread
            bank_conversion = self._number(
                context, "bank_net_profit_nii_conversion")
            bank_forecast_np = self._number(context, "forecast_net_profit")
            bank_shares = self._share_count(context)

            def _bank_chain(growth: float, scenario: str) -> SingleForecastChain:
                nii = None if base_nii is None else base_nii * (1.0 + growth)
                chain_np = bank_forecast_np
                if chain_np is None and nii is not None and bank_conversion is not None:
                    chain_np = nii * bank_conversion
                eps, eps_reason = self._eps(context, chain_np, bank_shares)
                assumptions = {
                    "scenario": scenario,
                    "eps_attributable_basis": self._eps_attributable_basis(
                        context),
                }
                if eps_reason is not None and chain_np is not None:
                    assumptions["eps_reason"] = eps_reason
                return ForecastDriver.build_bank_chain(
                    base_nii, growth, bank_shares, assumptions=assumptions,
                    net_profit_conversion=bank_conversion,
                    forecast_net_profit=bank_forecast_np,
                    beginning_equity=self._number(context, "beginning_equity"),
                    ending_equity=self._number(context, "forecast_ending_equity"),
                    npl_ratio=self._number(context, "npl_ratio"),
                    nim=self._number(context, "nim"),
                    loan_growth=self._number(context, "loan_growth"),
                    deposit_growth=self._number(context, "deposit_growth"),
                    eps=eps,
                )

            scenarios = ScenarioForecastResult(
                _bank_chain(bear_g, "BEAR"),
                _bank_chain(base_g, "BASE"),
                _bank_chain(bull_g, "BULL"),
            )

        else:
            baseline_method = "HOLDING_SPECIALIZED"
            # NAV conversion carries no revenue-side FX exposure.
            exposure = None
            base_nav = self._number(context, "base_nav")
            nav_growth = self._number(context, "baseline_nav_growth")
            if nav_growth is None:
                nav_growth = 0.00
            nav_growth += trend_adj
            bear_g, base_g, bull_g = nav_growth - financial_spread, nav_growth, nav_growth + financial_spread
            shares = self._share_count(context)
            conversion = self._number(context, "holding_net_profit_nav_conversion")
            holding_forecast_np = self._number(context, "forecast_net_profit")

            def _holding_chain(growth: float, scenario: str) -> SingleForecastChain:
                chain_np = holding_forecast_np
                if chain_np is None and base_nav is not None \
                        and conversion is not None:
                    chain_np = base_nav * (1.0 + growth) * conversion
                eps, eps_reason = self._eps(context, chain_np, shares)
                assumptions = {
                    "scenario": scenario,
                    "eps_attributable_basis": self._eps_attributable_basis(
                        context),
                }
                if eps_reason is not None and chain_np is not None:
                    assumptions["eps_reason"] = eps_reason
                return ForecastDriver.build_holding_chain(
                    base_nav, growth, shares,
                    net_profit_conversion=conversion,
                    forecast_net_profit=holding_forecast_np,
                    beginning_equity=self._number(context, "beginning_equity"),
                    ending_equity=self._number(context, "forecast_ending_equity"),
                    assumptions=assumptions,
                    eps=eps,
                )

            scenarios = ScenarioForecastResult(
                _holding_chain(bear_g, "BEAR"),
                _holding_chain(base_g, "BASE"),
                _holding_chain(bull_g, "BULL"),
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
        if industry_code in NON_FINANCIAL_INDUSTRIES and baseline_revenue is not None:
            assumptions["low_base_evidence"] = low_base_evidence
            assumptions["growth_rate_basis"] = growth_basis

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
