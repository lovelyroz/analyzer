"""Stage 1 read access for the Stage 5 production path (spec sections 25, 29).

The forecast must see exactly the information a caller standing at the cutoff
could have seen. These helpers perform the point-in-time selection on Stage 1
tables and hand the result to the builder / adapter, which do the rest. Nothing
here computes a forecast quantity; every function only selects and converts
types.

``load_financial_facts`` resolves two collisions the normalized layer allows:
several report versions may carry the same fact, and several periods may be
available. The version published latest at or before the cutoff wins, because a
later publication is unknowable at the cutoff (spec section 25), and the most
recent period wins, because a forecast is built on the latest reported state.
"""

from datetime import date, datetime
from typing import Any, Dict, List, Optional, Sequence, Tuple

from sqlalchemy import and_, func, select
from sqlalchemy.orm import Session

from src.forecast.schema import ForecastInputRef, normalize_datetime
from src.models.entity import Company, Industry
from src.models.normalized import FinancialMetric, NormalizedFinancialFact
from src.models.period import FinancialPeriod
from src.models.report import ReportVersion
from src.models.share_action import CorporateAction, ShareCountHistory

FACT_SOURCE = "normalized_financial_facts"


def load_industry_code(session: Session, company_id: int) -> Optional[str]:
    """Industry classification Stage 5 needs to pick a forecast branch."""
    row = session.execute(
        select(Industry.industry_code)
        .select_from(Company)
        .join(Industry, Company.industry_id == Industry.industry_id)
        .where(Company.company_id == company_id)
    ).first()
    return row[0] if row is not None else None


def _period_rows(
    session: Session,
    company_id: int,
    *,
    cutoff: datetime,
    metric_codes: Sequence[str],
) -> List[Any]:
    """The PIT-restricted facts the production path may read, one row per fact.

    Every row is published at or before the cutoff, so nothing this returns can
    be look-ahead. ``load_financial_facts`` then picks the latest period and
    ``load_financial_fact_periods`` keeps the whole period ordering, because the
    two need the same restriction but a different selection (spec section 25).
    """
    cutoff_dt = normalize_datetime(cutoff)
    return list(session.execute(
        select(
            FinancialPeriod.period_id,
            FinancialPeriod.end_date,
            FinancialMetric.metric_code,
            NormalizedFinancialFact.value_irr,
            NormalizedFinancialFact.source_report_version_id,
            ReportVersion.publication_datetime,
        )
        .select_from(NormalizedFinancialFact)
        .join(FinancialMetric,
              NormalizedFinancialFact.metric_id == FinancialMetric.metric_id)
        .join(ReportVersion,
              NormalizedFinancialFact.source_report_version_id
              == ReportVersion.report_version_id)
        .join(FinancialPeriod,
              NormalizedFinancialFact.period_id == FinancialPeriod.period_id)
        .where(and_(
            NormalizedFinancialFact.company_id == company_id,
            FinancialMetric.metric_code.in_(tuple(metric_codes)),
            ReportVersion.publication_datetime <= cutoff_dt,
        ))
    ).all())


def _latest_per_metric(rows: Sequence[Any]) -> Dict[str, Tuple[Any, Any, datetime]]:
    """Newest publication at or before the cutoff, per metric code.

    A metric may be restated in a later report version of the same period. The
    version published latest at or before the cutoff is the one knowable then.
    """
    chosen: Dict[str, Tuple[Any, Any, datetime]] = {}
    for _period_id, _end_date, metric_code, value, report_version_id, published in rows:
        published_utc = normalize_datetime(published)
        current = chosen.get(metric_code)
        if current is None or published_utc > current[2]:
            chosen[metric_code] = (value, report_version_id, published_utc)
    return chosen


def load_financial_fact_periods(
    session: Session,
    company_id: int,
    *,
    cutoff: datetime,
    metric_codes: Sequence[str],
) -> List[Tuple[int, Optional[date], Dict[str, float], List[ForecastInputRef]]]:
    """Point-in-time facts grouped by reporting period, oldest period first.

    The production path reads more than the latest balance: beginning equity is
    the previous *reported* observation, prior-period revenue is the previous
    observation of the same metric, and both must clear the same cutoff as the
    latest one (spec section 25). Grouping by period keeps that ordering in the
    query rather than reconstructing it from a single-period result.

    Each period carries its own provenance, so a forecast built on the latest
    period can still name the earlier report version that supplied the opening
    balance or the prior revenue (spec section 29).

    Returns ``(period_id, period_end_date, facts, refs)`` per period, latest
    period last.
    """
    rows = _period_rows(session, company_id, cutoff=cutoff,
                        metric_codes=metric_codes)
    if not rows:
        return []

    periods: Dict[int, Optional[date]] = {
        period_id: end_date
        for period_id, end_date, _code, _value, _version, _published in rows
    }

    grouped: Dict[int, Dict[str, Tuple[Any, Any, datetime]]] = {}
    for period_id in periods:
        subset = [row for row in rows if row[0] == period_id]
        grouped[period_id] = _latest_per_metric(subset)

    ordered: List[Tuple[int, Optional[date], Dict[str, float],
                        List[ForecastInputRef]]] = []
    for period_id in sorted(periods):
        chosen = grouped[period_id]
        facts: Dict[str, float] = {}
        refs: List[ForecastInputRef] = []
        for metric_code, (value, report_version_id, published) \
                in sorted(chosen.items()):
            if value is None:
                continue
            facts[metric_code] = float(value)
            refs.append(ForecastInputRef(
                fact_key=metric_code,
                report_version_id=report_version_id,
                available_at=published,
                source=FACT_SOURCE,
            ))
        ordered.append((period_id, periods[period_id], facts, refs))
    return ordered


def load_financial_facts(
    session: Session,
    company_id: int,
    *,
    cutoff: datetime,
    metric_codes: Sequence[str],
) -> Tuple[Dict[str, float], List[ForecastInputRef]]:
    """Point-in-time-restricted normalized facts for one company.

    Returns one value per metric code from the most recent reporting period,
    taken from the newest report version published at or before ``cutoff``,
    plus the provenance reference that lets the forecast prove it did not look
    ahead (spec section 29).
    """
    periods = load_financial_fact_periods(session, company_id, cutoff=cutoff,
                                          metric_codes=metric_codes)
    if not periods:
        return {}, []
    return periods[-1][2], periods[-1][3]


def load_share_history(
    session: Session,
    company_id: int,
    *,
    cutoff: datetime,
) -> Tuple[List[Any], List[Any]]:
    """Share base in force at the cutoff, for the weighted-average builder.

    Corporate actions announced after the cutoff are excluded here as well as
    in the builder: an unannounced capital increase is not knowable at the
    cutoff (spec section 25), so it must not extend the share series.
    """
    cutoff_date = normalize_datetime(cutoff).date()

    history = list(session.execute(
        select(ShareCountHistory)
        .where(and_(
            ShareCountHistory.company_id == company_id,
            ShareCountHistory.effective_date <= cutoff_date,
        ))
        .order_by(ShareCountHistory.effective_date.asc())
    ).scalars().all())

    actions = list(session.execute(
        select(CorporateAction)
        .where(and_(
            CorporateAction.company_id == company_id,
            CorporateAction.effective_date <= cutoff_date,
            func.coalesce(CorporateAction.announcement_date, cutoff_date)
            <= cutoff_date,
        ))
        .order_by(CorporateAction.effective_date.asc())
    ).scalars().all())

    return history, actions
