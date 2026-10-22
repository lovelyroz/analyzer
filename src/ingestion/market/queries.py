"""Read-side selection helpers for persisted market observations."""

from dataclasses import dataclass
from decimal import Decimal
from typing import Optional, Tuple

from sqlalchemy import and_, or_, select
from sqlalchemy.orm import Session

from src.ingestion.common.parsing import parse_jalali_components
from src.models.market import MarketDaily

JalaliDate = Tuple[int, int, int]


@dataclass(frozen=True)
class MarketPriceObservation:
    """A selected daily price with its original Jalali date and source."""

    company_id: int
    price: Decimal
    price_basis: str
    source_jalali_date: JalaliDate
    source: Optional[str]
    market_data_id: int


def _validate_jalali_date(value: object, *, label: str) -> JalaliDate:
    if (
        not isinstance(value, tuple)
        or len(value) != 3
        or any(type(part) is not int for part in value)
    ):
        raise ValueError(f"{label} must be a (year, month, day) integer tuple")
    year, month, day = value
    parsed = parse_jalali_components(f"{year:04d}-{month:02d}-{day:02d}")
    if year < 1 or parsed != value:
        raise ValueError(f"{label} is not a valid Jalali date: {value!r}")
    return year, month, day


def select_market_price_as_of(
    session: Session,
    company_id: int,
    as_of_jalali_date: JalaliDate,
) -> Optional[MarketPriceObservation]:
    """Return the latest usable company price on or before a Jalali date.

    ``None`` means that no dated, positive price observation is available at
    the requested date. Invalid request dates raise ``ValueError``. Jalali
    date components are compared numerically; no Gregorian conversion occurs.
    Adjusted close follows the existing market-engine convention, with close
    as its fallback. If duplicate eligible rows share the newest Jalali date,
    fail explicitly because the ingestion upsert contract expects one row per
    company and Jalali date.
    """
    as_of = _validate_jalali_date(as_of_jalali_date, label="as_of_jalali_date")
    year, month, day = as_of

    stmt = (
        select(MarketDaily)
        .where(
            MarketDaily.company_id == company_id,
            MarketDaily.jalali_year >= 1,
            MarketDaily.jalali_month.between(1, 12),
            MarketDaily.jalali_day.between(1, 31),
            or_(
                MarketDaily.jalali_year < year,
                and_(MarketDaily.jalali_year == year, MarketDaily.jalali_month < month),
                and_(
                    MarketDaily.jalali_year == year,
                    MarketDaily.jalali_month == month,
                    MarketDaily.jalali_day <= day,
                ),
            ),
            or_(MarketDaily.adjusted_close > 0, MarketDaily.close_price > 0),
        )
        .order_by(
            MarketDaily.jalali_year.desc(),
            MarketDaily.jalali_month.desc(),
            MarketDaily.jalali_day.desc(),
            MarketDaily.market_data_id.asc(),
        )
    )
    rows = list(session.scalars(stmt))
    if not rows:
        return None

    selected = rows[0]
    selected_date = (
        selected.jalali_year,
        selected.jalali_month,
        selected.jalali_day,
    )
    same_date = [
        row for row in rows
        if (row.jalali_year, row.jalali_month, row.jalali_day) == selected_date
    ]
    if len(same_date) != 1:
        raise ValueError(
            "duplicate market observations for company/date: "
            f"company_id={company_id}, jalali_date={selected_date!r}"
        )

    if selected.adjusted_close is not None and selected.adjusted_close > 0:
        price = selected.adjusted_close
        price_basis = "ADJUSTED_CLOSE"
    else:
        price = selected.close_price
        price_basis = "CLOSE"

    return MarketPriceObservation(
        company_id=selected.company_id,
        price=price,
        price_basis=price_basis,
        source_jalali_date=selected_date,
        source=selected.source,
        market_data_id=selected.market_data_id,
    )
