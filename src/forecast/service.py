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
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from src.forecast.adapter import build_financial_context
from src.forecast.builder import build_weighted_average_shares
from src.forecast.engine import ForecastEngine
from src.forecast.queries import (
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
    supply (margins, growth) and overrides them where both exist. It is the
    caller's declaration, not a second Stage 1 read.

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

    history, actions = load_share_history(
        session, company_id, cutoff=data_cutoff_datetime,
    )
    weighted_shares = build_weighted_average_shares(history, actions,
                                                    cutoff=data_cutoff_datetime)

    financial_context: Dict[str, Any] = {}
    financial_context.update(_to_context(facts))
    if extra_facts:
        financial_context.update(extra_facts)
    if model_parameters:
        financial_context["model_parameters"] = model_parameters
    if share_count is not None:
        financial_context["share_count"] = share_count
    financial_context["forecast_weighted_average_shares"] = weighted_shares
    financial_context["calculation_timestamp"] = calculation_timestamp or _utc_now()

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
