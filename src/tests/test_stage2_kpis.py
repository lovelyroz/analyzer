import pytest
from datetime import datetime
from src.kpi.period_utils import calculate_ttm, calculate_yoy_growth
from src.kpi.universal import UniversalKPIEngine
from src.kpi.conditional import ConditionalKPIEngine
from src.kpi.industry import IndustryKPIEngine
from src.kpi.engine import KPIEngine

# ----------------------------------------------------------------------
# 1. Period Utils Tests
# ----------------------------------------------------------------------
def test_calculate_ttm_valid():
    values = [100.0, 120.0, 110.0, 130.0]
    assert calculate_ttm(values) == 460.0


def test_calculate_ttm_insufficient_or_missing_data():
    assert calculate_ttm([100.0, 120.0, 110.0]) is None
    assert calculate_ttm([100.0, None, 110.0, 130.0]) is None


def test_calculate_yoy_growth():
    assert calculate_yoy_growth(150.0, 100.0) == 50.0
    assert calculate_yoy_growth(100.0, 0.0) is None
    assert calculate_yoy_growth(None, 100.0) is None

# ----------------------------------------------------------------------
# 2. Universal KPIs Tests (11 KPIs)
# ----------------------------------------------------------------------
def test_universal_growth_kpis():
    res = UniversalKPIEngine.calc_revenue_growth(150.0, 100.0, company_id=1, period_id=10)
    assert res.value == 50.0
    assert res.quality_status == "VALID"
    assert res.kpi_code == "REVENUE_GROWTH"

    res_missing = UniversalKPIEngine.calc_revenue_growth(None, 100.0, company_id=1, period_id=10)
    assert res_missing.value is None
    assert res_missing.quality_status == "MISSING"


def test_universal_growth_zero_base_is_not_zero_growth():
    for calculator in (
        UniversalKPIEngine.calc_revenue_growth,
        UniversalKPIEngine.calc_op_profit_growth,
        UniversalKPIEngine.calc_net_profit_growth,
        UniversalKPIEngine.calc_eps_growth,
    ):
        res = calculator(100.0, 0.0, company_id=1, period_id=10)
        assert res.value is None
        assert res.quality_status == "MISSING"


def test_universal_profitability_kpis():
    res = UniversalKPIEngine.calc_op_margin(20.0, 100.0, company_id=1, period_id=10)
    assert res.value == 20.0
    assert res.unit == "PERCENTAGE"

    res_roe = UniversalKPIEngine.calc_roe(50.0, 200.0, company_id=1, period_id=10)
    assert res_roe.value == 25.0


def test_universal_profitability_zero_denominators_are_missing():
    assert UniversalKPIEngine.calc_gross_margin(20.0, 0.0, 1, 10).value is None
    assert UniversalKPIEngine.calc_op_margin(20.0, 0.0, 1, 10).value is None
    assert UniversalKPIEngine.calc_net_margin(20.0, 0.0, 1, 10).value is None
    assert UniversalKPIEngine.calc_roa(20.0, 0.0, 1, 10).value is None
    assert UniversalKPIEngine.calc_roe(20.0, 0.0, 1, 10).value is None


def test_universal_risk_and_quality_kpis():
    # Locked specification defines Cash Earnings Conversion conceptually as OCF / Net Profit.
    res_cc = UniversalKPIEngine.calc_cash_conversion(120.0, 100.0, company_id=1, period_id=10)
    assert res_cc.value == 1.2
    assert res_cc.unit == "RATIO"
    assert res_cc.kpi_code == "CASH_CONVERSION"

    # Earnings Quality is a composite framework; no simplistic ratio is assumed in Stage 2.
    res_eq = UniversalKPIEngine.calc_earnings_quality(120.0, 100.0, company_id=1, period_id=10)
    assert res_eq.value is None
    assert res_eq.unit == "COMPOSITE"
    assert res_eq.quality_status == "MISSING"
    assert res_eq.metadata["framework"] == "composite"

# ----------------------------------------------------------------------
# 3. Conditional KPI Tests
# ----------------------------------------------------------------------
def test_conditional_financial_cost_pressure():
    res = ConditionalKPIEngine.calc_financial_cost_pressure(30.0, 100.0, company_id=1, period_id=10)
    assert res.value == 30.0
    assert res.unit == "PERCENTAGE"
    assert res.quality_status == "VALID"

    res_invalid = ConditionalKPIEngine.calc_financial_cost_pressure(30.0, -10.0, company_id=1, period_id=10)
    assert res_invalid.value is None
    assert res_invalid.quality_status == "MISSING"

# ----------------------------------------------------------------------
# 4. Industry Core KPIs Tests
# ----------------------------------------------------------------------
def test_bank_industry_kpis():
    results = IndustryKPIEngine.calc_bank_kpis(
        nii=500.0, nim=3.5, loan_growth=12.0, deposit_growth=15.0, npl=2.1,
        company_id=1, period_id=10
    )
    assert len(results) == 5
    codes = [r.kpi_code for r in results]
    assert "BANK_NII" in codes
    assert "BANK_NPL" in codes


def test_holding_industry_kpis():
    results = IndustryKPIEngine.calc_holding_kpis(
        nav=1000.0, nav_growth=20.0, p_nav=0.7,
        company_id=1, period_id=10
    )
    assert len(results) == 3
    codes = [r.kpi_code for r in results]
    assert "HOLDING_P_NAV" in codes


def test_industry_zero_kpis():
    for industry in ("PETROCHEMICAL", "CHEMICAL", "METALS", "MINING"):
        kpis = IndustryKPIEngine.get_industry_kpis(industry, {}, company_id=1, period_id=10)
        assert len(kpis) == 0


def test_optional_sales_volume_missing_is_not_zero():
    for industry in ("CEMENT", "FOOD", "PHARMACEUTICAL"):
        kpis = IndustryKPIEngine.get_industry_kpis(industry, {}, company_id=1, period_id=10)
        assert len(kpis) == 1
        assert kpis[0].value is None
        assert kpis[0].quality_status == "MISSING"

# ----------------------------------------------------------------------
# 5. Stage 2 Contract Tests: EPS comparability + Data Quality
# ----------------------------------------------------------------------
def test_eps_growth_requires_share_count_corporate_action_comparability():
    engine = KPIEngine()
    data = {
        "revenue_curr": 1000.0, "revenue_prev": 800.0,
        "op_profit_curr": 200.0, "op_profit_prev": 150.0,
        "net_profit_curr": 150.0, "net_profit_prev": 100.0,
        "eps_curr": 15.0, "eps_prev": 10.0,
        "gross_profit": 300.0, "net_profit_ttm": 150.0,
        "avg_assets": 1000.0, "avg_equity": 500.0,
        "ocf": 180.0, "financial_expenses": 20.0,
        "eps_comparable": False,
    }
    results = engine.calculate_all_kpis_for_company(1, 10, "PETROCHEMICAL", data)
    eps = next(r for r in results if r.kpi_code == "EPS_GROWTH")
    assert eps.value is None
    assert eps.quality_status == "MISSING"
    assert eps.metadata["comparability_status"] == "UNRESOLVED_SHARE_COUNT_OR_CORPORATE_ACTION"


def test_data_quality_status_propagates_from_stage1_inputs():
    engine = KPIEngine()
    data = {
        "revenue_curr": 1000.0, "revenue_prev": 800.0,
        "op_profit_curr": 200.0, "op_profit_prev": 150.0,
        "net_profit_curr": 150.0, "net_profit_prev": 100.0,
        "eps_curr": 15.0, "eps_prev": 10.0,
        "gross_profit": 300.0, "net_profit_ttm": 150.0,
        "avg_assets": 1000.0, "avg_equity": 500.0,
        "ocf": 180.0, "financial_expenses": 20.0,
        "quality_statuses": {"revenue_curr": "ESTIMATED", "op_profit_curr": "SUSPICIOUS"},
    }
    results = engine.calculate_all_kpis_for_company(1, 10, "PETROCHEMICAL", data)
    revenue_growth = next(r for r in results if r.kpi_code == "REVENUE_GROWTH")
    op_margin = next(r for r in results if r.kpi_code == "OPERATING_MARGIN")
    net_margin = next(r for r in results if r.kpi_code == "NET_MARGIN")
    assert revenue_growth.quality_status == "ESTIMATED"
    assert op_margin.quality_status == "SUSPICIOUS"
    assert net_margin.quality_status == "ESTIMATED"


def test_industry_kpi_data_quality_propagates():
    engine = KPIEngine()
    data = {
        "revenue_curr": 1000.0, "revenue_prev": 800.0,
        "op_profit_curr": 200.0, "op_profit_prev": 150.0,
        "net_profit_curr": 150.0, "net_profit_prev": 100.0,
        "eps_curr": 15.0, "eps_prev": 10.0,
        "gross_profit": 300.0, "net_profit_ttm": 150.0,
        "avg_assets": 1000.0, "avg_equity": 500.0,
        "ocf": 180.0, "financial_expenses": 20.0,
        "nii": 100.0, "nim": 4.0, "loan_growth": 10.0, "deposit_growth": 12.0, "npl": 1.5,
        "quality_statuses": {"nii": "RESTATED", "npl": "SUSPICIOUS"},
    }
    results = engine.calculate_all_kpis_for_company(1, 10, "BANK", data)
    nii = next(r for r in results if r.kpi_code == "BANK_NII")
    npl = next(r for r in results if r.kpi_code == "BANK_NPL")
    nim = next(r for r in results if r.kpi_code == "BANK_NIM")
    assert nii.quality_status == "RESTATED"
    assert npl.quality_status == "SUSPICIOUS"
    assert nim.quality_status == "VALID"

# ----------------------------------------------------------------------
# 6. KPI Engine Execution Test
# ----------------------------------------------------------------------
def test_kpi_engine_full_run():
    engine = KPIEngine()
    financial_data = {
        "revenue_curr": 1000.0, "revenue_prev": 800.0,
        "op_profit_curr": 200.0, "op_profit_prev": 150.0,
        "net_profit_curr": 150.0, "net_profit_prev": 100.0,
        "eps_curr": 15.0, "eps_prev": 10.0,
        "gross_profit": 300.0, "net_profit_ttm": 150.0,
        "avg_assets": 1000.0, "avg_equity": 500.0,
        "ocf": 180.0, "financial_expenses": 20.0
    }

    results = engine.calculate_all_kpis_for_company(
        company_id=1, period_id=10, industry_code="PETROCHEMICAL", financial_data=financial_data
    )
    assert len(results) == 12

    bank_data = {**financial_data, "nii": 100.0, "nim": 4.0, "loan_growth": 10.0, "deposit_growth": 12.0, "npl": 1.5}
    bank_results = engine.calculate_all_kpis_for_company(
        company_id=1, period_id=10, industry_code="BANK", financial_data=bank_data
    )
    assert len(bank_results) == 17
