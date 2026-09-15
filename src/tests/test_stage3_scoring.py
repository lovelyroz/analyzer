from datetime import datetime

from src.kpi.schema import KPIResult
from src.scoring.engine import FundamentalScoringEngine
from src.scoring.weights import AXIS_WEIGHTS, KPI_WEIGHTS, get_kpi_weights_for_industry


def kpi(code, value, status="VALID"):
    return KPIResult(
        company_id=1,
        period_id=10,
        kpi_code=code,
        value=value,
        unit="PERCENTAGE",
        quality_status=status,
        calculation_timestamp=datetime.utcnow(),
    )


def test_fixed_axis_weights_match_locked_spec():
    assert AXIS_WEIGHTS == {"GROWTH": 0.30, "PROFITABILITY": 0.45, "RISK_QUALITY": 0.25}
    assert sum(AXIS_WEIGHTS.values()) == 1.0
    assert sum(KPI_WEIGHTS["GROWTH"].values()) == 1.0
    assert sum(KPI_WEIGHTS["PROFITABILITY"].values()) == 1.0
    assert sum(KPI_WEIGHTS["RISK_QUALITY"].values()) == 1.0


def test_industry_profiles_keep_each_axis_at_one_hundred_percent():
    for industry in ["BANK", "HOLDING", "CEMENT", "FOOD", "PHARMACEUTICAL", "GENERAL"]:
        profile = get_kpi_weights_for_industry(industry)
        for axis in AXIS_WEIGHTS:
            assert abs(sum(profile[axis].values()) - 1.0) < 1e-12


def test_bank_industry_kpis_receive_redistributed_weight_not_bonus_weight():
    profile = get_kpi_weights_for_industry("BANK")
    assert profile["GROWTH"]["BANK_LOAN_GROWTH"] > 0
    assert profile["GROWTH"]["BANK_DEPOSIT_GROWTH"] > 0
    assert profile["PROFITABILITY"]["BANK_NII"] > 0
    assert profile["PROFITABILITY"]["BANK_NIM"] > 0
    assert profile["RISK_QUALITY"]["BANK_NPL"] > 0
    assert profile["GROWTH"]["REVENUE_GROWTH"] < KPI_WEIGHTS["GROWTH"]["REVENUE_GROWTH"]
    assert profile["RISK_QUALITY"]["CASH_CONVERSION"] < KPI_WEIGHTS["RISK_QUALITY"]["CASH_CONVERSION"]


def test_sales_volume_replaces_part_of_growth_weight():
    profile = get_kpi_weights_for_industry("CEMENT")
    assert profile["GROWTH"]["CEMENT_SALES_VOLUME"] == 0.20
    assert profile["GROWTH"]["REVENUE_GROWTH"] < KPI_WEIGHTS["GROWTH"]["REVENUE_GROWTH"]
    assert sum(profile["GROWTH"].values()) == 1.0


def test_industry_percentile_is_primary_when_peer_count_is_at_least_eight():
    engine = FundamentalScoringEngine()
    peers = [10, 20, 30, 40, 50, 60, 70, 80]
    result = engine.calculate_score(
        1, 10, "GENERAL",
        [kpi("REVENUE_GROWTH", 80)],
        peer_values={"REVENUE_GROWTH": peers},
    )
    item = result.kpi_scores[0]
    assert item.benchmark_method == "INDUSTRY_PERCENTILE"
    assert item.score == 100.0


def test_lower_is_better_direction_is_inverted_for_npl():
    engine = FundamentalScoringEngine()
    peers = [1, 2, 3, 4, 5, 6, 7, 8]
    result = engine.calculate_score(
        1, 10, "BANK",
        [kpi("BANK_NPL", 1)],
        peer_values={"BANK_NPL": peers},
    )
    item = result.kpi_scores[0]
    assert item.direction == "LOWER_IS_BETTER"
    assert item.score == 100.0


def test_lower_is_better_maximum_gets_zero():
    engine = FundamentalScoringEngine()
    peers = [1, 2, 3, 4, 5, 6, 7, 8]
    result = engine.calculate_score(
        1, 10, "BANK",
        [kpi("BANK_NPL", 8)],
        peer_values={"BANK_NPL": peers},
    )
    assert result.kpi_scores[0].score == 0.0


def test_historical_benchmark_is_fallback_when_peer_count_is_below_eight():
    engine = FundamentalScoringEngine()
    result = engine.calculate_score(
        1, 10, "GENERAL",
        [kpi("REVENUE_GROWTH", 30)],
        peer_values={"REVENUE_GROWTH": [10, 20, 30]},
        historical_values={"REVENUE_GROWTH": [20, 30, 40]},
    )
    item = result.kpi_scores[0]
    assert item.benchmark_method == "HISTORICAL_FALLBACK"
    assert item.score == 50.0


def test_missing_kpi_is_not_zero_and_remaining_axis_weight_is_redistributed():
    engine = FundamentalScoringEngine()
    result = engine.calculate_score(
        1, 10, "GENERAL",
        [
            kpi("REVENUE_GROWTH", 50),
            kpi("OP_PROFIT_GROWTH", 50),
            kpi("NET_PROFIT_GROWTH", 50),
            kpi("EPS_GROWTH", None, "MISSING"),
        ],
        historical_values={code: [50] for code in ["REVENUE_GROWTH", "OP_PROFIT_GROWTH", "NET_PROFIT_GROWTH"]},
    )
    growth_items = [x for x in result.kpi_scores if x.axis == "GROWTH"]
    assert all(x.score == 50.0 for x in growth_items if x.kpi_code != "EPS_GROWTH")
    assert sum(x.effective_weight for x in growth_items) == 1.0
    assert result.category_scores["GROWTH"].coverage == 0.70
    assert result.category_scores["GROWTH"].score == 50.0


def test_axis_below_sixty_percent_is_insufficient_data():
    engine = FundamentalScoringEngine()
    result = engine.calculate_score(
        1, 10, "GENERAL",
        [kpi("REVENUE_GROWTH", 50)],
        historical_values={"REVENUE_GROWTH": [50]},
    )
    assert result.category_scores["GROWTH"].score is None
    assert result.category_scores["GROWTH"].coverage == 0.15
    assert result.overall_score is None
    assert result.score_data_quality == "INSUFFICIENT_DATA"


def test_three_axis_formula_and_missing_axis_renormalization():
    engine = FundamentalScoringEngine()
    results = engine.calculate_score(
        1, 10, "GENERAL",
        [
            kpi("REVENUE_GROWTH", 50), kpi("OP_PROFIT_GROWTH", 50), kpi("NET_PROFIT_GROWTH", 50), kpi("EPS_GROWTH", 50),
            kpi("GROSS_MARGIN", 60), kpi("OPERATING_MARGIN", 60), kpi("NET_MARGIN", 60), kpi("ROA", 60), kpi("ROE", 60),
            kpi("CASH_CONVERSION", 80), kpi("EARNINGS_QUALITY", 80),
        ],
        historical_values={
            "REVENUE_GROWTH": [50], "OP_PROFIT_GROWTH": [50], "NET_PROFIT_GROWTH": [50], "EPS_GROWTH": [50],
            "GROSS_MARGIN": [50], "OPERATING_MARGIN": [50], "NET_MARGIN": [50], "ROA": [50], "ROE": [50],
            "CASH_CONVERSION": [50], "EARNINGS_QUALITY": [50],
        },
    )
    assert results.category_scores["GROWTH"].score == 50.0
    assert results.category_scores["PROFITABILITY"].score == 60.0
    assert results.category_scores["RISK_QUALITY"].score == 80.0
    assert results.overall_score == 62.0


def test_valuation_and_market_inputs_are_not_scoring_inputs():
    engine = FundamentalScoringEngine()
    result = engine.calculate_score(
        1, 10, "HOLDING",
        [kpi("HOLDING_P_NAV", 0.8)],
        historical_values={"HOLDING_P_NAV": [0.7, 0.8, 0.9]},
    )
    assert result.kpi_scores == []
    assert result.overall_score is None


def test_output_contract_contains_traceability_and_version():
    engine = FundamentalScoringEngine()
    result = engine.calculate_score(
        1, 10, "GENERAL",
        [kpi("REVENUE_GROWTH", 50)],
        historical_values={"REVENUE_GROWTH": [50]},
    )
    assert result.scoring_method_version == "STAGE3_V1"
    assert result.score_data_quality == "INSUFFICIENT_DATA"
    item = result.kpi_scores[0]
    assert item.axis == "GROWTH"
    assert item.direction == "HIGHER_IS_BETTER"
    assert item.benchmark_method == "HISTORICAL_FALLBACK"
