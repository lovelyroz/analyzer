"""Lookup helpers for idempotent upsert identity (CHANGE-005 / CHANGE-006)."""

from __future__ import annotations

from datetime import date
from typing import Optional

from sqlalchemy.orm import Session

from src.models.fx import FXRate
from src.models.market import MarketDaily


def find_fx_existing(
    session: Session,
    *,
    rate_type: str,
    c_from: str,
    c_to: str,
    rate_date: Optional[date],
    jy: Optional[int],
    jm: Optional[int],
    jd: Optional[int],
) -> Optional[FXRate]:
    q = session.query(FXRate).filter_by(
        currency_from=c_from,
        currency_to=c_to,
        rate_type=rate_type,
    )
    if jy is not None and jm is not None and jd is not None:
        return q.filter_by(jalali_year=jy, jalali_month=jm, jalali_day=jd).one_or_none()
    if rate_date is not None:
        return q.filter_by(rate_date=rate_date).one_or_none()
    return None


def find_market_daily_existing(
    session: Session,
    *,
    company_id: int,
    jy: int,
    jm: int,
    jd: int,
) -> Optional[MarketDaily]:
    return (
        session.query(MarketDaily)
        .filter_by(
            company_id=company_id,
            jalali_year=jy,
            jalali_month=jm,
            jalali_day=jd,
        )
        .one_or_none()
    )
