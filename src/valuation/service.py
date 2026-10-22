"""Production service boundary for date-based Stage 7 valuation."""

from dataclasses import replace
from typing import Any

from sqlalchemy.orm import Session

from src.forecast.schema import CompanyForecastResult
from src.ingestion.market.queries import JalaliDate, select_market_price_as_of
from src.valuation.engine import ValuationEngine
from src.valuation.schema import ValuationResult


class MarketPriceUnavailableError(LookupError):
    """No eligible persisted market price exists for the requested date."""


def calculate_valuation_as_of_jalali(
    session: Session,
    company_id: int,
    period_id: int,
    forecast_result: CompanyForecastResult,
    as_of_jalali_date: JalaliDate,
    **valuation_options: Any,
) -> ValuationResult:
    """Select an authoritative market observation and pass it to Stage 7.

    Jalali source dates are retained as provenance metadata. They are never
    converted or assigned to the engine's Gregorian datetime fields.
    """
    if forecast_result.company_id != company_id:
        raise ValueError("forecast company_id does not match valuation company_id")
    if forecast_result.forecast_period_id != period_id:
        raise ValueError("forecast period_id does not match valuation period_id")

    reserved = {
        "company_id", "period_id", "industry_code", "current_price",
        "forecast_result", "valuation_date", "market_price_date",
    }
    conflicts = reserved.intersection(valuation_options)
    if conflicts:
        names = ", ".join(sorted(conflicts))
        raise TypeError(f"valuation options cannot override service inputs: {names}")

    observation = select_market_price_as_of(session, company_id, as_of_jalali_date)
    if observation is None:
        raise MarketPriceUnavailableError(
            f"no market price for company_id={company_id} on or before "
            f"Jalali date {as_of_jalali_date!r}"
        )

    result = ValuationEngine().calculate_valuation(
        company_id=company_id,
        period_id=period_id,
        industry_code=forecast_result.industry_code,
        current_price=float(observation.price),
        forecast_result=forecast_result,
        **valuation_options,
    )
    metadata = dict(result.metadata)
    metadata["market_price_observation"] = {
        "calendar": "JALALI",
        "as_of_jalali_date": as_of_jalali_date,
        "source_jalali_date": observation.source_jalali_date,
        "price": str(observation.price),
        "price_basis": observation.price_basis,
        "source": observation.source,
        "market_data_id": observation.market_data_id,
    }
    return replace(result, metadata=metadata)
