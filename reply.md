(analyzer) PS D:\winprojects\analyzer> python -m pytest src/tests/test_stage8_market.py -q
.............................................................................................                    [100%]
93 passed in 0.49s
(analyzer) PS D:\winprojects\analyzer> python -m pytest src/tests/test_stage8_market_service.py src/tests/
================================================= test session starts =================================================
platform win32 -- Python 3.12.9, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\winprojects\analyzer
collected 1227 items

src\tests\test_codal_acquisition.py ...                                                                          [  0%]
src\tests\test_codal_digit_normalization.py ..                                                                   [  0%]
src\tests\test_codal_extraction.py ............s                                                                 [  1%]
src\tests\test_codal_pdf_extraction.py ......................................................................... [  7%]
..........................................................                                                       [ 12%]
src\tests\test_ingestion_fx.py ......s.                                                                          [ 12%]
src\tests\test_ingestion_ohlc.py ..............                                                                  [ 13%]
src\tests\test_jalali_contract.py ....................                                                           [ 15%]
src\tests\test_market_history_query.py .................                                                         [ 16%]
src\tests\test_stage1_database_architecture.py .                                                                 [ 17%]
src\tests\test_stage1_database_integrity.py ...                                                                  [ 17%]
src\tests\test_stage1_rules.py .............                                                                     [ 18%]
src\tests\test_stage2_kpis.py .................                                                                  [ 19%]
src\tests\test_stage3_scoring.py .................                                                               [ 21%]
src\tests\test_stage4_trend.py ................................................................................. [ 27%]
.....................                                                                                            [ 29%]
src\tests\test_stage5_forecast.py .............................................................................. [ 35%]
................................................................................................................ [ 44%]
................................................................................................................ [ 54%]
..............................                                                                                   [ 56%]
src\tests\test_stage6_artifact_boundary.py ........                                                              [ 57%]
src\tests\test_stage6_artifact_identity.py ......................................                                [ 60%]
src\tests\test_stage6_evaluation.py .......                                                                      [ 60%]
src\tests\test_stage6_evaluation_foundation.py .............................                                     [ 63%]
src\tests\test_stage6_evaluation_metrics.py .......................                                              [ 65%]
src\tests\test_stage6_p25_adversarial.py ..................                                                      [ 66%]
src\tests\test_stage6_p25_selection.py ..................                                                        [ 67%]
src\tests\test_stage6_p38_closure.py .................                                                           [ 69%]
src\tests\test_stage6_p39_cutoff.py ...................                                                          [ 70%]
src\tests\test_stage6_p40_duplicates.py ...................                                                      [ 72%]
src\tests\test_stage6_p41_cutoff_identity.py .................                                                   [ 73%]
src\tests\test_stage6_production_pipeline.py ........................................                            [ 77%]
src\tests\test_stage6_reliability_governance.py ................................                                 [ 79%]
src\tests\test_stage6_scenario_isolation.py ......................                                               [ 81%]
src\tests\test_stage789_service_interface.py ....                                                                [ 81%]
src\tests\test_stage7_valuation.py ............................................................................. [ 88%]
.............                                                                                                    [ 89%]
src\tests\test_stage8_market.py ................................................................................ [ 95%]
.............                                                                                                    [ 96%]
src\tests\test_stage8_market_parameters.py ..                                                                    [ 96%]
src\tests\test_stage8_market_service.py ...................                                                      [ 98%]
src\tests\test_stage9_decision.py ...................                                                            [100%]

================================================== warnings summary ===================================================
src/tests/test_codal_pdf_extraction.py::test_malformed_pdf_is_rejected_and_ingestion_is_audited
  D:\winprojects\analyzer\src\ingestion\codal\ingestion.py:84: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    finished_at=datetime.utcnow(),

src/tests/test_stage1_rules.py::test_ingestion_run_contract
  D:\winprojects\analyzer\src\tests\test_stage1_rules.py:234: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    run = IngestionRun(source="CODAL", status="COMPLETED", records_found=10, records_inserted=9, records_updated=1, records_failed=0, finished_at=datetime.utcnow())

src/tests/test_stage2_kpis.py::test_universal_growth_kpis
src/tests/test_stage2_kpis.py::test_universal_growth_kpis
src/tests/test_stage2_kpis.py::test_universal_growth_zero_base_is_not_zero_growth
src/tests/test_stage2_kpis.py::test_eps_growth_requires_share_count_corporate_action_comparability
src/tests/test_stage2_kpis.py::test_data_quality_status_propagates_from_stage1_inputs
src/tests/test_stage2_kpis.py::test_industry_kpi_data_quality_propagates
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
  D:\winprojects\analyzer\src\kpi\universal.py:12: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    return KPIResult(company_id, period_id, "REVENUE_GROWTH", val, "PERCENTAGE", "VALID" if val is not None else "MISSING", datetime.utcnow())

src/tests/test_stage2_kpis.py::test_universal_growth_zero_base_is_not_zero_growth
src/tests/test_stage2_kpis.py::test_eps_growth_requires_share_count_corporate_action_comparability
src/tests/test_stage2_kpis.py::test_data_quality_status_propagates_from_stage1_inputs
src/tests/test_stage2_kpis.py::test_industry_kpi_data_quality_propagates
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
  D:\winprojects\analyzer\src\kpi\universal.py:17: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    return KPIResult(company_id, period_id, "OP_PROFIT_GROWTH", val, "PERCENTAGE", "VALID" if val is not None else "MISSING", datetime.utcnow())

src/tests/test_stage2_kpis.py::test_universal_growth_zero_base_is_not_zero_growth
src/tests/test_stage2_kpis.py::test_eps_growth_requires_share_count_corporate_action_comparability
src/tests/test_stage2_kpis.py::test_data_quality_status_propagates_from_stage1_inputs
src/tests/test_stage2_kpis.py::test_industry_kpi_data_quality_propagates
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
  D:\winprojects\analyzer\src\kpi\universal.py:22: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    return KPIResult(company_id, period_id, "NET_PROFIT_GROWTH", val, "PERCENTAGE", "VALID" if val is not None else "MISSING", datetime.utcnow())

src/tests/test_stage2_kpis.py::test_universal_growth_zero_base_is_not_zero_growth
src/tests/test_stage2_kpis.py::test_eps_growth_requires_share_count_corporate_action_comparability
src/tests/test_stage2_kpis.py::test_data_quality_status_propagates_from_stage1_inputs
src/tests/test_stage2_kpis.py::test_industry_kpi_data_quality_propagates
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
  D:\winprojects\analyzer\src\kpi\universal.py:27: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    return KPIResult(company_id, period_id, "EPS_GROWTH", val, "PERCENTAGE", "VALID" if val is not None else "MISSING", datetime.utcnow())

src/tests/test_stage2_kpis.py::test_universal_profitability_kpis
src/tests/test_stage2_kpis.py::test_universal_profitability_zero_denominators_are_missing
src/tests/test_stage2_kpis.py::test_eps_growth_requires_share_count_corporate_action_comparability
src/tests/test_stage2_kpis.py::test_data_quality_status_propagates_from_stage1_inputs
src/tests/test_stage2_kpis.py::test_industry_kpi_data_quality_propagates
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
  D:\winprojects\analyzer\src\kpi\universal.py:38: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    return KPIResult(company_id, period_id, "OPERATING_MARGIN", val, "PERCENTAGE", "VALID" if val is not None else "MISSING", datetime.utcnow())

src/tests/test_stage2_kpis.py::test_universal_profitability_kpis
src/tests/test_stage2_kpis.py::test_universal_profitability_zero_denominators_are_missing
src/tests/test_stage2_kpis.py::test_eps_growth_requires_share_count_corporate_action_comparability
src/tests/test_stage2_kpis.py::test_data_quality_status_propagates_from_stage1_inputs
src/tests/test_stage2_kpis.py::test_industry_kpi_data_quality_propagates
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
  D:\winprojects\analyzer\src\kpi\universal.py:53: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    return KPIResult(company_id, period_id, "ROE", val, "PERCENTAGE", "VALID" if val is not None else "MISSING", datetime.utcnow())

src/tests/test_stage2_kpis.py::test_universal_profitability_zero_denominators_are_missing
src/tests/test_stage2_kpis.py::test_eps_growth_requires_share_count_corporate_action_comparability
src/tests/test_stage2_kpis.py::test_data_quality_status_propagates_from_stage1_inputs
src/tests/test_stage2_kpis.py::test_industry_kpi_data_quality_propagates
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
  D:\winprojects\analyzer\src\kpi\universal.py:33: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    return KPIResult(company_id, period_id, "GROSS_MARGIN", val, "PERCENTAGE", "VALID" if val is not None else "MISSING", datetime.utcnow())

src/tests/test_stage2_kpis.py::test_universal_profitability_zero_denominators_are_missing
src/tests/test_stage2_kpis.py::test_eps_growth_requires_share_count_corporate_action_comparability
src/tests/test_stage2_kpis.py::test_data_quality_status_propagates_from_stage1_inputs
src/tests/test_stage2_kpis.py::test_industry_kpi_data_quality_propagates
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
  D:\winprojects\analyzer\src\kpi\universal.py:43: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    return KPIResult(company_id, period_id, "NET_MARGIN", val, "PERCENTAGE", "VALID" if val is not None else "MISSING", datetime.utcnow())

src/tests/test_stage2_kpis.py::test_universal_profitability_zero_denominators_are_missing
src/tests/test_stage2_kpis.py::test_eps_growth_requires_share_count_corporate_action_comparability
src/tests/test_stage2_kpis.py::test_data_quality_status_propagates_from_stage1_inputs
src/tests/test_stage2_kpis.py::test_industry_kpi_data_quality_propagates
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
  D:\winprojects\analyzer\src\kpi\universal.py:48: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    return KPIResult(company_id, period_id, "ROA", val, "PERCENTAGE", "VALID" if val is not None else "MISSING", datetime.utcnow())

src/tests/test_stage2_kpis.py::test_universal_risk_and_quality_kpis
src/tests/test_stage2_kpis.py::test_eps_growth_requires_share_count_corporate_action_comparability
src/tests/test_stage2_kpis.py::test_data_quality_status_propagates_from_stage1_inputs
src/tests/test_stage2_kpis.py::test_industry_kpi_data_quality_propagates
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
  D:\winprojects\analyzer\src\kpi\universal.py:60: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    return KPIResult(company_id, period_id, "CASH_CONVERSION", val, "RATIO", "VALID" if val is not None else "MISSING", datetime.utcnow())

src/tests/test_stage2_kpis.py::test_universal_risk_and_quality_kpis
src/tests/test_stage2_kpis.py::test_eps_growth_requires_share_count_corporate_action_comparability
src/tests/test_stage2_kpis.py::test_data_quality_status_propagates_from_stage1_inputs
src/tests/test_stage2_kpis.py::test_industry_kpi_data_quality_propagates
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
  D:\winprojects\analyzer\src\kpi\universal.py:71: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    status, datetime.utcnow(),

src/tests/test_stage2_kpis.py::test_conditional_financial_cost_pressure
src/tests/test_stage2_kpis.py::test_conditional_financial_cost_pressure
src/tests/test_stage2_kpis.py::test_eps_growth_requires_share_count_corporate_action_comparability
src/tests/test_stage2_kpis.py::test_data_quality_status_propagates_from_stage1_inputs
src/tests/test_stage2_kpis.py::test_industry_kpi_data_quality_propagates
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
  D:\winprojects\analyzer\src\kpi\conditional.py:33: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    calculation_timestamp=datetime.utcnow(),

src/tests/test_stage2_kpis.py::test_bank_industry_kpis
src/tests/test_stage2_kpis.py::test_industry_kpi_data_quality_propagates
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
  D:\winprojects\analyzer\src\kpi\industry.py:12: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    KPIResult(company_id, period_id, "BANK_NII", nii, "CURRENCY_IRR", "VALID" if nii is not None else "MISSING", datetime.utcnow()),

src/tests/test_stage2_kpis.py::test_bank_industry_kpis
src/tests/test_stage2_kpis.py::test_industry_kpi_data_quality_propagates
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
  D:\winprojects\analyzer\src\kpi\industry.py:13: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    KPIResult(company_id, period_id, "BANK_NIM", nim, "PERCENTAGE", "VALID" if nim is not None else "MISSING", datetime.utcnow()),

src/tests/test_stage2_kpis.py::test_bank_industry_kpis
src/tests/test_stage2_kpis.py::test_industry_kpi_data_quality_propagates
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
  D:\winprojects\analyzer\src\kpi\industry.py:14: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    KPIResult(company_id, period_id, "BANK_LOAN_GROWTH", loan_growth, "PERCENTAGE", "VALID" if loan_growth is not None else "MISSING", datetime.utcnow()),

src/tests/test_stage2_kpis.py::test_bank_industry_kpis
src/tests/test_stage2_kpis.py::test_industry_kpi_data_quality_propagates
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
  D:\winprojects\analyzer\src\kpi\industry.py:15: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    KPIResult(company_id, period_id, "BANK_DEPOSIT_GROWTH", deposit_growth, "PERCENTAGE", "VALID" if deposit_growth is not None else "MISSING", datetime.utcnow()),

src/tests/test_stage2_kpis.py::test_bank_industry_kpis
src/tests/test_stage2_kpis.py::test_industry_kpi_data_quality_propagates
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
  D:\winprojects\analyzer\src\kpi\industry.py:16: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    KPIResult(company_id, period_id, "BANK_NPL", npl, "PERCENTAGE", "VALID" if npl is not None else "MISSING", datetime.utcnow()),

src/tests/test_stage2_kpis.py::test_holding_industry_kpis
  D:\winprojects\analyzer\src\kpi\industry.py:23: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    KPIResult(company_id, period_id, "HOLDING_NAV", nav, "CURRENCY_IRR", "VALID" if nav is not None else "MISSING", datetime.utcnow()),

src/tests/test_stage2_kpis.py::test_holding_industry_kpis
  D:\winprojects\analyzer\src\kpi\industry.py:24: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    KPIResult(company_id, period_id, "HOLDING_NAV_GROWTH", nav_growth, "PERCENTAGE", "VALID" if nav_growth is not None else "MISSING", datetime.utcnow()),

src/tests/test_stage2_kpis.py::test_holding_industry_kpis
  D:\winprojects\analyzer\src\kpi\industry.py:25: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    KPIResult(company_id, period_id, "HOLDING_P_NAV", p_nav, "RATIO", "VALID" if p_nav is not None else "MISSING", datetime.utcnow()),

src/tests/test_stage2_kpis.py::test_optional_sales_volume_missing_is_not_zero
src/tests/test_stage2_kpis.py::test_optional_sales_volume_missing_is_not_zero
src/tests/test_stage2_kpis.py::test_optional_sales_volume_missing_is_not_zero
  D:\winprojects\analyzer\src\kpi\industry.py:39: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    calculation_timestamp=datetime.utcnow(),

src/tests/test_stage4_trend.py: 53 warnings
  D:\winprojects\analyzer\src\trend\engine.py:235: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    calculation_timestamp=datetime.utcnow(),

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
============================== 1225 passed, 2 skipped, 153 warnings in 171.08s (0:02:51)