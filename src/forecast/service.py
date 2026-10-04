"""Stage 5 forecast production path (spec sections 9, 15-16, 24, 25, 29).

The single entry point that turns Stage 1 facts plus a Stage 4 ``TrendResult``
into persisted forecast versions:

    Stage 1 facts + Stage 4 TrendResult
        -> build_financial_context()
        -> ForecastEngine
        -> ForecastRecord
        -> ForecastRecordRepository
        -> persistent ForecastVersion / ForecastInputRef

Nothing here forecasts anything. Every step is an existing component: the
queries read Stage 1, the adapter carries Stage 4 across, the builder weights
the share base, the engine computes the scenarios and the repository stores
them. The service only orders those steps.

The caller owns the ``Session`` and therefore the transaction boundary, as in
``src/ingestion/service.py``; nothing here commits.

Stage 4 is authoritative for trend state, direction, seasonal and momentum
evidence, low base, sign change, data sufficiency and provenance. It enters
through ``build_financial_context`` exactly once and is never recalculated.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Sequence, Tuple

from sqlalchemy.orm import Session

from src.forecast.adapter import build_financial_context
from src.forecast.builder import build_weighted_average_shares
from src.forecast.engine import ForecastEngine
from src.forecast.queries import (
    load_financial_fact_periods,
    load_financial_facts,
    load_industry_code,
    load_share_history,
)
from src.forecast.repo import ForecastRecordRepository
from src.forecast.schema import (
    CompanyForecastResult,
    ForecastInputRef,
    SUPPORTED_INDUSTRIES,
    normalize_datetime,
)
from src.trend.schema import TrendResult

# The seeded Stage 1 metric vocabulary (src/scripts/seed_data.py). Stage 5 reads
# codes rather than inventing its own fact names.
DEFAULT_FACT_METRICS = (
    "REVENUE",
    "OPERATING_PROFIT",
    "NET_PROFIT",
    "TOTAL_EQUITY",
    "EPS",
)

FORECAST_SCENARIOS = ("bear", "base", "bull")

# The Stage 5 EPS contract divides profit *attributable to common shareholders*
# (05_Stage5_Forecast_Engine.md section 9). Stage 1 exposes only NET_PROFIT —
# "سود (زیان) خالص" — with no NET_PROFIT_ATTRIBUTABLE metric and no documented
# equivalence between the two — so the production path cannot assert its facts
# are attributable and does not divide an unverified total. See
# ``_eps_attributable_basis``.
EPS_ATTRIBUTABLE_PROVENANCE_KEY = "eps_attributable_basis"


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _to_context(facts: Dict[str, float]) -> Dict[str, Any]:
    """Rename the Stage 1 metric vocabulary into the engine's input names."""
    names = {
        "REVENUE": "recent_run_rate_revenue",
        "OPERATING_PROFIT": "recent_operating_profit",
        "NET_PROFIT": "recent_net_profit",
        "TOTAL_EQUITY": "forecast_ending_equity",
    }
    return {
        names[code]: value
        for code, value in facts.items()
        if code in names and value is not None
    }


def _ratio(numerator: Optional[float], denominator: Optional[float]
            ) -> Optional[float]:
    """A margin, or ``None`` when the division is not defined.

    A missing numerator or a missing / zero denominator is a missing ratio, not
    a zero one: a zero-revenue company has no margin to read off, and a missing
    input leaves nothing to divide.
    """
    if numerator is None or denominator is None or denominator == 0:
        return None
    return numerator / denominator


def _stage1_derived_context(
    periods: Sequence[Tuple[int, Any, Dict[str, float], List[ForecastInputRef]]],
) -> Tuple[Dict[str, Any], List[ForecastInputRef]]:
    """Derive the inputs the engine needs from the Stage 1 facts themselves.

    Gaps A, B, C and E all have the same shape: the engine expects a margin, an
    opening balance or a prior period, and the production path used to supply
    none of them, so the chain only ran because a caller injected them through
    ``extra_facts``. Every one of these is computable from facts already read
    under the same cutoff, so it is derived here rather than required.

    The latest period supplies the numerators and denominators. The previous
    reported period supplies the opening equity and the prior revenue, and it
    clears the same cutoff/publication rules because it comes from the same
    PIT-restricted read.

    Nothing is fabricated: a ratio with no defined division, or an opening
    balance with no prior observation, stays absent and the engine records the
    absence rather than substituting the closing balance or a flat growth.
    """
    if not periods:
        return {}, []

    latest_facts = periods[-1][2]
    derived: Dict[str, Any] = {}
    refs: List[ForecastInputRef] = []

    revenue = latest_facts.get("REVENUE")
    operating_profit = latest_facts.get("OPERATING_PROFIT")
    net_profit = latest_facts.get("NET_PROFIT")

    # Operating margin moves on its own evidence (05_Stage5 section 7), so the
    # historical level the engine's margin hierarchy reads is the reported
    # operating profit over the reported revenue it was earned against.
    operating_margin = _ratio(operating_profit, revenue)
    if operating_margin is not None:
        derived["historical_operating_margin"] = operating_margin
        refs.append(ForecastInputRef(
            fact_key="DERIVED_OPERATING_MARGIN",
            report_version_id=None,
            available_at=_latest_publication(periods[-1][3], "REVENUE"),
            source="derived_from_" + FACT_SOURCE,
        ))

    net_margin = _ratio(net_profit, revenue)
    if net_margin is not None:
        derived["historical_net_margin"] = net_margin
        refs.append(ForecastInputRef(
            fact_key="DERIVED_NET_MARGIN",
            report_version_id=None,
            available_at=_latest_publication(periods[-1][3], "REVENUE"),
            source="derived_from_" + FACT_SOURCE,
        ))

    # Beginning equity must be the nearest earlier valid observation, not
    # merely the immediately preceding reporting period. A period may legitimately
    # omit equity while an older PIT-valid balance still establishes the opening
    # point for the latest reported ending equity.
    if len(periods) > 1:
        for _prior_id, _prior_end, prior_facts, prior_refs in reversed(periods[:-1]):
            prior_equity = prior_facts.get("TOTAL_EQUITY")
            if prior_equity is not None:
                derived["beginning_equity"] = prior_equity
                for ref in prior_refs:
                    if ref.fact_key == "TOTAL_EQUITY":
                        refs.append(ForecastInputRef(
                            fact_key="BEGINNING_EQUITY",
                            report_version_id=ref.report_version_id,
                            available_at=ref.available_at,
                            source=ref.source,
                        ))
                        break
                break

    # Historical revenue growth uses the nearest earlier actual observation.
    # Missing revenue in an intervening period must not force a fabricated
    # percentage or a false zero-base interpretation.
    if revenue is not None:
        for _prior_id, _prior_end, prior_facts, prior_refs in reversed(periods[:-1]):
            prior_revenue = prior_facts.get("REVENUE")
            if prior_revenue is not None:
                derived["prior_revenue"] = prior_revenue
                derived["current_revenue"] = revenue
                for ref in prior_refs:
                    if ref.fact_key == "REVENUE":
                        refs.append(ForecastInputRef(
                            fact_key="PRIOR_REVENUE",
                            report_version_id=ref.report_version_id,
                            available_at=ref.available_at,
                            source=ref.source,
                        ))
                        break
                break

    return derived, refs


def _latest_publication(refs: Sequence[ForecastInputRef], fact_key: str
                        ) -> Optional[datetime]:
    for ref in refs:
        if ref.fact_key == fact_key:
            return ref.available_at
    return None


def _eps_attributable_basis(extra_facts: Optional[Dict[str, Any]]) -> str:
    """Whether the net profit reaching EPS can be called attributable.

    The Stage 5 EPS contract divides profit attributable to common shareholders
    (05_Stage5_Forecast_Engine.md section 9). Stage 1 exposes NET_PROFIT —
    "سود (زیان) خالص", the bottom line of the consolidated statement — with no
    NET_PROFIT_ATTRIBUTABLE metric in its seeded vocabulary and no documented
    statement that the two are the same amount. Stage 1 also carries no minority
    interest fields, so the attributable portion cannot be isolated by
    subtraction either.

    So the data contract does not guarantee attributable profit, and the
    production path refuses to pretend it does: it does not divide an unverified
    total, does not invent a minority-interest amount to subtract, and does not
    treat NET_PROFIT and attributable profit as identical by default.

    A caller who has the attributable amount declares it, either as the amount
    itself or as an explicit equivalence for a reporting regime that publishes
    no minority interest. Both are the caller's own statement about its data,
    made through the override the API already exposes — never an assumption the
    engine makes on its own.
    """
    if not extra_facts:
        return "UNVERIFIED_TOTAL_NET_PROFIT"
    if extra_facts.get("net_profit_attributable") is not None:
        return "CALLER_DECLARED_NET_PROFIT_ATTRIBUTABLE"
    if extra_facts.get("net_profit_is_attributable") is True:
        return "CALLER_DECLARED_EQUIVALENCE"
    return "UNVERIFIED_TOTAL_NET_PROFIT"


def generate_and_persist_forecast(
    session: Session,
    company_id: int,
    forecast_period_id: int,
    *,
    trend_result: Optional[TrendResult],
    data_cutoff_datetime: datetime,
    horizon: str = "12M",
    model_version: str = "V1.0",
    model_parameters: Optional[Dict[str, Any]] = None,
    extra_facts: Optional[Dict[str, Any]] = None,
    share_count: Optional[float] = None,
    calculation_timestamp: Optional[datetime] = None,
    persist: bool = True,
) -> CompanyForecastResult:
    """Run the Stage 5 production path for one company and forecast period.

    ``trend_result`` is the Stage 4 output for the same metric the caller is
    forecasting; pass ``None`` when Stage 4 has nothing to say and the engine
    will record the absence rather than invent evidence.

    ``extra_facts`` supplements Stage 1 with inputs the normalized layer cannot
    supply, and overrides them where both exist. It is the caller's declaration,
    not a second Stage 1 read. Margins, the opening equity and the prior revenue
    arc are derived from the Stage 1 facts themselves, so they are optional here
    rather than required; what cannot be derived from Stage 1 is the EPS
    attributable-profit basis, which the caller must state explicitly (see
    ``_eps_attributable_basis``).

    ``share_count`` is the caller's escape hatch for a share base that cannot be
    derived from ``ShareCountHistory``; it never supplants the weighted average
    the builder produced.

    ``calculation_timestamp`` dates the forecast. Re-running the path with the
    same inputs and the same timestamp yields the identical record, which is
    what makes a repeat run idempotent rather than a new version; when it is
    omitted the current UTC instant is used, so a genuine re-forecast is still
    recorded as one.

    Returns the engine result; the persisted records are reachable from it via
    ``records()``.
    """
    industry_code = load_industry_code(session, company_id)
    if industry_code is None:
        raise ValueError(f"no Stage 1 company found for company_id={company_id}")
    if industry_code not in SUPPORTED_INDUSTRIES:
        raise ValueError(
            f"unsupported Stage 5 industry for company_id={company_id}: "
            f"{industry_code!r}"
        )

    facts, input_refs = load_financial_facts(
        session, company_id,
        cutoff=data_cutoff_datetime,
        metric_codes=DEFAULT_FACT_METRICS,
    )

    # Inputs the engine needs and Stage 1 already supplies. Reading them here
    # keeps ``extra_facts`` an override rather than a silent requirement.
    periods = load_financial_fact_periods(
        session, company_id,
        cutoff=data_cutoff_datetime,
        metric_codes=DEFAULT_FACT_METRICS,
    )
    derived, derived_refs = _stage1_derived_context(periods)
    input_refs = [*input_refs, *derived_refs]

    history, actions = load_share_history(
        session, company_id, cutoff=data_cutoff_datetime,
    )
    weighted_shares = build_weighted_average_shares(history, actions,
                                                    cutoff=data_cutoff_datetime)

    financial_context: Dict[str, Any] = {}
    financial_context.update(_to_context(facts))
    # The Stage 1 derivations are the baseline. ``extra_facts`` is applied after
    # them, so a caller's explicit declaration still wins and the derivation
    # only ever fills a gap Stage 1 can itself close.
    financial_context.update(derived)
    if extra_facts:
        financial_context.update(extra_facts)
    if model_parameters:
        financial_context["model_parameters"] = model_parameters
    if share_count is not None:
        financial_context["share_count"] = share_count
    financial_context["forecast_weighted_average_shares"] = weighted_shares
    financial_context["calculation_timestamp"] = calculation_timestamp or _utc_now()
    financial_context[EPS_ATTRIBUTABLE_PROVENANCE_KEY] = \
        _eps_attributable_basis(extra_facts)

    financial_context = build_financial_context(
        trend_result,
        financial_context,
        input_refs=input_refs or None,
    )

    forecast = ForecastEngine().generate_forecast(
        company_id,
        forecast_period_id,
        industry_code,
        financial_context,
        trend_state=(
            trend_result.trend_state if trend_result is not None else None
        ),
        data_cutoff_datetime=data_cutoff_datetime,
        horizon=horizon,
        model_version=model_version,
    )

    if persist:
        repository = ForecastRecordRepository(session)
        for scenario in FORECAST_SCENARIOS:
            repository.save(forecast.to_record(scenario, forecast_id=1))

    return forecast
