"""Database-to-engine boundary for Stage 8 (Jalali-native market analysis).

``select_market_history_as_of`` -> engine rows -> ``MarketEngine.analyze_market``.

This module only connects the existing read-side query to the engine. It owns
no Session, persists nothing, performs no Gregorian conversion, and never
creates, defaults or zero-fills an observation or a date.
"""

from typing import Any, Dict, List, Optional, Sequence

from sqlalchemy.orm import Session

from src.core.jalali import JalaliDate
from src.ingestion.market.queries import (
    MarketHistoryObservation,
    select_market_history_as_of,
)
from src.market.engine import MarketEngine
from src.market.schema import MarketSignalResult


def market_history_to_engine_rows(
    history: Sequence[MarketHistoryObservation],
) -> List[Dict[str, Any]]:
    """Map persisted observations to Stage 8 engine rows, field for field.

    Only attributes present on ``MarketHistoryObservation`` are copied. Missing
    source values stay ``None``. ``jalali_date`` is the stored source date
    (never converted); ``company_id`` and ``market_data_id`` keep row identity.
    """
    return [
        {
            "company_id": obs.company_id,
            "market_data_id": obs.market_data_id,
            "jalali_date": obs.jalali_date,
            "open": obs.open_price,
            "high": obs.high_price,
            "low": obs.low_price,
            "close": obs.close_price,
            "adjusted_close": obs.adjusted_close,
            "volume": obs.volume,
            "value": obs.value,
            "trade_count": obs.trade_count,
            "source": obs.source,
        }
        for obs in history
    ]


def analyze_market_as_of_jalali(
    session: Session,
    company_id: int,
    as_of_jalali_date: JalaliDate,
    *,
    industry_benchmark: Optional[Sequence[Dict[str, Any]]] = None,
    market_benchmark: Optional[Sequence[Dict[str, Any]]] = None,
) -> MarketSignalResult:
    """Run Stage 8 for one company from persisted history on or before a Jalali date.

    The caller owns ``session``. Benchmarks are optional, caller-supplied engine
    rows (``jalali_date`` plus price fields); no benchmark source exists in the
    repository, so none is looked up or invented here. An empty history yields
    the engine's established ``INSUFFICIENT_DATA`` result. Invalid as-of dates,
    duplicate dates, rows of another company or malformed benchmark rows raise
    ``ValueError``.
    """
    history = select_market_history_as_of(session, company_id, as_of_jalali_date)
    foreign = sorted({obs.company_id for obs in history if obs.company_id != company_id})
    if foreign:
        raise ValueError(
            f"market history for company_id={company_id} contains rows of other "
            f"companies: {foreign!r}"
        )
    return MarketEngine().analyze_market(
        company_id,
        as_of_jalali_date,
        market_history_to_engine_rows(history),
        industry_benchmark=industry_benchmark,
        market_benchmark=market_benchmark,
        point_in_time=True,
    )
