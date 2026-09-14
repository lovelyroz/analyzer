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
    # Less than 4 quarters
    assert calculate_ttm([100.0, 120.0, 110.0]) is None
    # None in values
    assert calculate_ttm([100.0, None, 110.0, 130.0]) is None

def test_calculate_yoy_growth():
    assert calculate_yoy_growth(150.0, 100.0) == 50.0
    # Zero or negative prior value handling
    assert calculate_yoy_growth(100.0, 0.0) is None
    assert calculate_yoy_growth(None, 100.0) is None

# ----------------------------------------------------------------------
# 2. Universal KPIs Tests (11 KPIs)
# ----------------------------------------------------------------------
def test_universal_growth_kpis():
    # Revenue Growth
    res = UniversalKPIEngine.calc_revenue_growth(150.0, 100.0, company_id=1, period_id=10)
    assert res.value == 50.0
    assert res.quality_status == "VALID"
    assert res.kpi_code == "REVENUE_GROWTH"

    # Missing Data Handling (Missing != Zero)
    res_missing = UniversalKPIEngine.calc_revenue_growth(None, 100.0, company_id=1, period_id=10)
    assert res_missing.value is None
    assert res_missing.quality_status == "MISSING"

def test_universal_profitability_kpis():
    # Operating Margin
    res = UniversalKPIEngine.calc_op_margin(20.0, 100.0, company_id=1, period_id=10)
    assert res.value == 20.0
    assert res.unit == "PERCENTAGE"

    # ROE
    res_roe = UniversalKPIEngine.calc_roe(50.0, 200.0, company_id=1, period_id=10)
    assert res_roe.value == 25.0

def test_universal_risk_and_quality_kpis():
    # Cash Conversion
    res_cc = UniversalKPIEngine.calc_cash_conversion(120.0, 100.0, company_id=1, period_id=10)
    assert res_cc.value == 120.0
    assert res_cc.kpi_code == "CASH_CONVERSION"

# ----------------------------------------------------------------------
# 3. Conditional KPI Tests
# ----------------------------------------------------------------------
def test_conditional_financial_cost_pressure():
    # Valid Case
    res = ConditionalKPIEngine.calc_financial_cost_pressure(30.0, 100.0, company_id=1, period_id=10)
    assert res.value == 30.0
    assert res.quality_status == "VALID"

    # Invalid / Missing / Operating profit <= 0
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

def test_commodity_industry_zero_kpis():
    # Petrochemical & Metals should return 0 special KPIs (Handled by Universal Core)
    kpis = IndustryKPIEngine.get_industry_kpis("PETROCHEMICAL", {}, company_id=1, period_id=10)
    assert len(kpis) == 0

# ----------------------------------------------------------------------
# 5. KPI Engine Execution Test
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
    
    # Run for General Industry (e.g. Petrochemical) -> 11 Universal + 1 Conditional = 12 KPIs
    results = engine.calculate_all_kpis_for_company(
        company_id=1, period_id=10, industry_code="PETROCHEMICAL", financial_data=financial_data
    )
    assert len(results) == 12

    # Run for Bank Industry -> 11 Universal + 1 Conditional + 5 Bank = 17 KPIs
    bank_data = {**financial_data, "nii": 100.0, "nim": 4.0, "loan_growth": 10.0, "deposit_growth": 12.0, "npl": 1.5}
    bank_results = engine.calculate_all_kpis_for_company(
        company_id=1, period_id=10, industry_code="BANK", financial_data=bank_data
    )
    assert len(bank_results) == 17