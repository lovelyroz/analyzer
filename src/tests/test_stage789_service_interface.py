"""Interface tests that run the real Stage 7 -> Stage 9 service path.

Unlike ``test_jalali_orchestration_passes_stage7_result_to_stage9`` these tests
do NOT monkeypatch ``calculate_valuation_as_of_jalali``: the real
``select_market_price_as_of`` query, the real ``ValuationEngine`` and the real
``DecisionEngine`` run against an in-memory SQLite database.

Scope limits (deliberate):
* The Stage 8 ``MarketSignalResult`` is supplied by the test, exactly as the
  production contract requires of the caller. These tests therefore prove the
  Stage 7 -> Stage 9 hand-off and the treatment of caller-supplied market
  evidence, not that Stage 8 is produced from the database.
* Nothing here asserts a particular recommendation; decision rules are covered
  by ``test_stage9_decision.py``.
"""

from datetime import datetime, timezone
from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.core.database import Base
from src.decision import service as decision_service
from src.decision.engine import DecisionEngine
from src.forecast.schema import (
    CompanyForecastResult,
    ScenarioForecastResult,
    SingleForecastChain,
)
from src.market.schema import MarketSignalResult
from src.models.entity import Company, Industry
from src.models.market import MarketDaily
from src.scoring.schema import FundamentalScoreResult
from src.valuation.service import MarketPriceUnavailableError

PERIOD_ID = 101
AS_OF = (1405, 2, 11)


def _utc_now_naive():
    return datetime.now(timezone.utc).replace(tzinfo=None)


@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        industry = Industry(industry_code="PETROCHEMICAL", industry_name="Petrochemical")
        session.add(industry)
        session.flush()
        company = Company(ticker="TEST", company_name="Test", industry_id=industry.industry_id)
        session.add(company)
        session.flush()
        yield session, company.company_id
    engine.dispose()


def _forecast(company_id, eps=(150.0, 180.0, 210.0)):
    bear, base, bull = eps
    return CompanyForecastResult(
        company_id=company_id,
        forecast_period_id=PERIOD_ID,
        data_cutoff_datetime=datetime(2026, 1, 1),
        industry_code="PETROCHEMICAL",
        scenario_forecasts=ScenarioForecastResult(
            bear=SingleForecastChain(1000.0, 200.0, bear, bear),
            base=SingleForecastChain(1200.0, 240.0, base, base),
            bull=SingleForecastChain(1400.0, 280.0, bull, bull),
        ),
        forecast_method="DRIVER_BASED",
        model_version="V1.0",
        calculation_timestamp=datetime(2026, 1, 1),
    )


def _fundamental(company_id, score=85):
    return FundamentalScoreResult(
        company_id=company_id,
        period_id=PERIOD_ID,
        overall_score=score,
        category_scores={},
        kpi_scores=[],
        calculation_timestamp=_utc_now_naive(),
    )


def _market(company_id, trend="UPTREND", momentum="POSITIVE", liquidity="NORMAL", quality="VALID"):
    return MarketSignalResult(
        company_id=company_id,
        as_of_date=AS_OF,  # Jalali (year, month, day); not an execution timestamp
        trend_state=trend,
        momentum_state=momentum,
        liquidity_state=liquidity,
        market_data_quality=quality,
    )


def _price_row(company_id, date, adjusted_close):
    year, month, day = date
    return MarketDaily(
        company_id=company_id,
        jalali_year=year,
        jalali_month=month,
        jalali_day=day,
        close_price=Decimal(adjusted_close),
        adjusted_close=Decimal(adjusted_close),
        source="CSV_PROVIDER",
    )


def _run(session, company_id, market=None, forecast=None):
    return decision_service.calculate_decision_as_of_jalali(
        session,
        forecast or _forecast(company_id),
        AS_OF,
        _fundamental(company_id),
        market or _market(company_id),
        valuation_options={"historical_pe_values": [7.0]},
    )


def test_real_service_path_preserves_stage5_eps_and_market_provenance(db):
    session, company_id = db
    session.add(_price_row(company_id, (1405, 2, 10), "1000.00"))
    session.flush()
    forecast = _forecast(company_id)

    result = _run(session, company_id, forecast=forecast)

    valuation, decision = result.valuation, result.decision
    assert [valuation.scenarios[name].eps_forecast for name in ("bear", "base", "bull")] == [150.0, 180.0, 210.0]
    assert valuation.current_price == 1000.0
    observation = valuation.metadata["market_price_observation"]
    assert observation["calendar"] == "JALALI"
    assert observation["as_of_jalali_date"] == AS_OF
    assert observation["source_jalali_date"] == (1405, 2, 10)
    assert observation["source"] == "CSV_PROVIDER"
    assert decision.company_id == company_id
    assert decision.period_id == PERIOD_ID
    assert decision.valuation_status == valuation.valuation_status
    assert decision.market_trend_state == "UPTREND"
    assert decision.metadata["upstream_recalculation"] is False
    assert decision.metadata["market_score_used"] is False


def test_real_service_path_does_not_leak_future_market_prices(db):
    session, company_id = db
    session.add_all([
        _price_row(company_id, (1405, 2, 10), "1000.00"),
        _price_row(company_id, (1405, 2, 12), "5000.00"),
        _price_row(company_id, (1406, 1, 1), "9000.00"),
    ])
    session.flush()

    result = _run(session, company_id)

    assert result.valuation.current_price == 1000.0
    assert result.valuation.metadata["market_price_observation"]["source_jalali_date"] == (1405, 2, 10)


def test_missing_price_fails_closed_before_stage9_runs(db, monkeypatch):
    session, company_id = db
    session.add(_price_row(company_id, (1405, 2, 20), "1000.00"))  # only a future row
    session.flush()

    def stage9_must_not_run(*args, **kwargs):
        raise AssertionError("Stage 9 must not run without an eligible Stage 7 price")

    monkeypatch.setattr(DecisionEngine, "make_decision", stage9_must_not_run)

    with pytest.raises(MarketPriceUnavailableError):
        _run(session, company_id)


def test_insufficient_market_evidence_is_not_presented_as_valid_market_analysis(db):
    session, company_id = db
    session.add(_price_row(company_id, (1405, 2, 10), "1000.00"))
    session.flush()

    valid = _run(session, company_id).decision
    insufficient = _run(
        session,
        company_id,
        market=_market(
            company_id,
            trend="INSUFFICIENT_DATA",
            momentum="INSUFFICIENT_DATA",
            liquidity="INSUFFICIENT_DATA",
            quality="INSUFFICIENT_DATA",
        ),
    ).decision

    assert insufficient.market_trend_state == "INSUFFICIENT_DATA"
    assert insufficient.market_momentum_state == "INSUFFICIENT_DATA"
    assert insufficient.liquidity_state == "INSUFFICIENT_DATA"
    assert insufficient.evidence_summary["market_trend"] == "INSUFFICIENT_DATA"
    assert insufficient.data_quality == "LIMITED"
    assert insufficient.decision_confidence < valid.decision_confidence
