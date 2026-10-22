(analyzer) PS D:\winprojects\analyzer> .\.venv_test\Scripts\python.exe -m pytest -q .\src\tests\test_stage8_market.py .\src\tests\test_stage8_market_parameters.py
.................                                                                                                [100%]
================================================== warnings summary ===================================================
src/tests/test_stage8_market.py: 10 warnings
  D:\winprojects\analyzer\src\market\engine.py:137: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    calculation_timestamp=datetime.utcnow(),

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
17 passed, 10 warnings in 0.11s
(analyzer) PS D:\winprojects\analyzer> .venv\Scripts\python.exe -m pytest src/tests/test_stage7_valuation.py -v
================================================= test session starts =================================================
platform win32 -- Python 3.12.9, pytest-9.1.1, pluggy-1.6.0 -- D:\winprojects\analyzer\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: D:\winprojects\analyzer
collected 72 items

src/tests/test_stage7_valuation.py::test_valuation_models PASSED                                                 [  1%]
src/tests/test_stage7_valuation.py::test_valuation_engine_forward_pe_and_expected_fair_value PASSED              [  2%]
src/tests/test_stage7_valuation.py::test_industry_forward_pe_requires_eight_valid_peers PASSED                   [  4%]
src/tests/test_stage7_valuation.py::test_industry_ttm_is_fallback_after_historical_median PASSED                 [  5%]
src/tests/test_stage7_valuation.py::test_negative_eps_does_not_create_fake_pe_or_fair_value PASSED               [  6%]
src/tests/test_stage7_valuation.py::test_reliability_does_not_change_forward_pe_or_fair_value PASSED             [  8%]
src/tests/test_stage7_valuation.py::test_direct_probability_adjustments_are_rejected_in_favor_of_family_evidence PASSED [  9%]
src/tests/test_stage7_valuation.py::test_probability_evidence_is_family_level_and_equal_weighted PASSED          [ 11%]
src/tests/test_stage7_valuation.py::test_probability_evidence_rejects_unknown_or_incomplete_family_data PASSED   [ 12%]
src/tests/test_stage7_valuation.py::test_scenario_multiple_adjustments_require_economic_rationale_and_are_bounded PASSED [ 13%]
src/tests/test_stage7_valuation.py::test_alerts_include_severity_and_driver_focus PASSED                         [ 15%]
src/tests/test_stage7_valuation.py::test_p2_sensitivity_drivers_present_and_bounded PASSED                       [ 16%]
src/tests/test_stage7_valuation.py::test_p2_sensitivity_missing_data_empty_drivers PASSED                        [ 18%]
src/tests/test_stage7_valuation.py::test_p2_sensitivity_deterministic_repeated_runs PASSED                       [ 19%]
src/tests/test_stage7_valuation.py::test_p2_alert_severity_levels_valid PASSED                                   [ 20%]
src/tests/test_stage7_valuation.py::test_p2_alert_low_reliability_threshold_boundaries PASSED                    [ 22%]
src/tests/test_stage7_valuation.py::test_p2_alert_high_dispersion_threshold_boundaries PASSED                    [ 23%]
src/tests/test_stage7_valuation.py::test_p2_alert_divergence_ratios_boundaries PASSED                            [ 25%]
src/tests/test_stage7_valuation.py::test_v1_sector_examples_use_only_eps_and_target_pe_drivers PASSED            [ 26%]
src/tests/test_stage7_valuation.py::test_v1_uses_stage5_eps_without_recalculating_from_net_profit PASSED         [ 27%]
src/tests/test_stage7_valuation.py::test_v1_defers_undefined_flip_dependence_and_assumption_alerts PASSED        [ 29%]
src/tests/test_stage7_valuation.py::test_p3_sensitivity_recomputes_from_valuation_identity PASSED                [ 30%]
src/tests/test_stage7_valuation.py::test_p3_nan_eps_is_guarded_as_invalid PASSED                                 [ 31%]
src/tests/test_stage7_valuation.py::test_p3_zero_and_negative_price_guarded PASSED                               [ 33%]
src/tests/test_stage7_valuation.py::test_p3_nonfinite_benchmark_series_filtered PASSED                           [ 34%]
src/tests/test_stage7_valuation.py::test_p3_nonfinite_scores_fall_back_to_defaults PASSED                        [ 36%]
src/tests/test_stage7_valuation.py::test_p3_flip_dependence_alerts_remain_explicitly_unresolved PASSED           [ 37%]
src/tests/test_stage7_valuation.py::test_p4_peer_count_below_minimum_falls_back PASSED                           [ 38%]
src/tests/test_stage7_valuation.py::test_p4_peer_count_at_minimum_selects_industry_forward PASSED                [ 40%]
src/tests/test_stage7_valuation.py::test_p4_peer_count_above_minimum_and_median_provenance PASSED                [ 41%]
src/tests/test_stage7_valuation.py::test_p4_peer_count_filters_invalid_values PASSED                             [ 43%]
src/tests/test_stage7_valuation.py::test_p4_peer_count_empty_data_reports_zero_and_falls_back PASSED             [ 44%]
src/tests/test_stage7_valuation.py::test_p4_benchmark_fallback_ignores_forward_count_for_ttm PASSED              [ 45%]
src/tests/test_stage7_valuation.py::test_p5_nonfinite_price_yields_null_outputs PASSED                           [ 47%]
src/tests/test_stage7_valuation.py::test_p5_missing_eps_is_not_applicable_not_zero PASSED                        [ 48%]
src/tests/test_stage7_valuation.py::test_p5_nonfinite_reliability_echo_sanitized PASSED                          [ 50%]
src/tests/test_stage7_valuation.py::test_p5_nonfinite_probability_confidence_echo_finite PASSED                  [ 51%]
src/tests/test_stage7_valuation.py::test_p5_missing_data_quality_does_not_crash PASSED                           [ 52%]
src/tests/test_stage7_valuation.py::test_p5_nonfinite_multiple_adjustment_rejected PASSED                        [ 54%]
src/tests/test_stage7_valuation.py::test_p5_nan_probability_evidence_rejected PASSED                             [ 55%]
src/tests/test_stage7_valuation.py::test_p5_datetime_echoes_normalized_to_utc PASSED                             [ 56%]
src/tests/test_stage7_valuation.py::test_p5_default_cutoff_inherits_forecast_cutoff_normalized PASSED            [ 58%]
src/tests/test_stage7_valuation.py::test_p5_undated_benchmark_series_carry_no_provenance PASSED                  [ 59%]
src/tests/test_stage7_valuation.py::test_p6_production_path_real_stage5_forecast PASSED                          [ 61%]
src/tests/test_stage7_valuation.py::test_p6_cutoff_pit_limitation_pinned PASSED                                  [ 62%]
src/tests/test_stage7_valuation.py::test_p6_missing_benchmarks_yield_guarded_nulls PASSED                        [ 63%]
src/tests/test_stage7_valuation.py::test_p6_scenario_ordering_flag_and_probability_normalization PASSED          [ 65%]
src/tests/test_stage7_valuation.py::test_p6_invalid_eps_variants_never_fabricate_values PASSED                   [ 66%]
src/tests/test_stage7_valuation.py::test_p6_repeat_runs_identical_on_full_contract PASSED                        [ 68%]
src/tests/test_stage7_valuation.py::test_p6_regression_prior_behavior_preserved PASSED                           [ 69%]
src/tests/test_stage7_valuation.py::test_p10_expensive_base_upside_parameterized_outputs_unchanged PASSED        [ 70%]
src/tests/test_stage7_valuation.py::test_p10_expensive_threshold_consumed_from_parameters PASSED                 [ 72%]
src/tests/test_stage7_valuation.py::test_p12_calculation_timestamp_utc_aware_and_deterministic PASSED            [ 73%]
src/tests/test_stage7_valuation.py::test_p32_input_refs_before_cutoff_leave_results_unchanged PASSED             [ 75%]
src/tests/test_stage7_valuation.py::test_p32_input_ref_after_cutoff_rejected_on_valuation_path PASSED            [ 76%]
src/tests/test_stage7_valuation.py::test_p32_input_ref_at_cutoff_boundary_accepted PASSED                        [ 77%]
src/tests/test_stage7_valuation.py::test_p32_input_ref_missing_date_rejected PASSED                              [ 79%]
src/tests/test_stage7_valuation.py::test_p32_input_refs_absent_preserves_legacy_path PASSED                      [ 80%]
src/tests/test_stage7_valuation.py::test_p33_genesis_snapshot_matches_live_constants PASSED                      [ 81%]
src/tests/test_stage7_valuation.py::test_p33_result_carries_parameter_audit PASSED                               [ 83%]
src/tests/test_stage7_valuation.py::test_p33_resolve_exact_key_and_missing_raises PASSED                         [ 84%]
src/tests/test_stage7_valuation.py::test_p33_as_of_without_dated_records_raises PASSED                           [ 86%]
src/tests/test_stage7_valuation.py::test_p33_as_of_selection_mechanics PASSED                                    [ 87%]
src/tests/test_stage7_valuation.py::test_p33_as_of_overlap_raises_ambiguity PASSED                               [ 88%]
src/tests/test_stage7_valuation.py::test_p35_legacy_path_provenance_is_truthful_and_unchanged PASSED             [ 90%]
src/tests/test_stage7_valuation.py::test_p35_snapshot_reports_values_actually_consumed_when_module_constant_changes PASSED [ 91%]
src/tests/test_stage7_valuation.py::test_p35_as_of_selection_governs_calculation_and_snapshot_matches PASSED     [ 93%]
src/tests/test_stage7_valuation.py::test_p35_selected_set_governs_peers_alerts_and_scenario_weights PASSED       [ 94%]
src/tests/test_stage7_valuation.py::test_p35_missing_or_ambiguous_as_of_selection_fails_closed PASSED            [ 95%]
src/tests/test_stage7_valuation.py::test_p35_invalid_parameter_set_raises_without_fallback_to_constants PASSED   [ 97%]
src/tests/test_stage7_valuation.py::test_p35_isolation_from_global_mutation_and_snapshot_aliasing PASSED         [ 98%]
src/tests/test_stage7_valuation.py::test_p35_repeated_as_of_calculations_are_deterministic PASSED                [100%]

================================================= 72 passed in 0.72s 
(analyzer) PS D:\winprojects\analyzer> .venv\Scripts\python.exe -m pytest src/tests/test_stage9_decision.py -v
================================================= test session starts =================================================
platform win32 -- Python 3.12.9, pytest-9.1.1, pluggy-1.6.0 -- D:\winprojects\analyzer\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: D:\winprojects\analyzer
collected 13 items

src/tests/test_stage9_decision.py::test_strong_buy_requires_aligned_families PASSED                              [  7%]
src/tests/test_stage9_decision.py::test_value_trap_does_not_become_buy PASSED                                    [ 15%]
src/tests/test_stage9_decision.py::test_strong_but_expensive_is_not_buy PASSED                                   [ 23%]
src/tests/test_stage9_decision.py::test_low_forecast_reliability_limits_strong_conviction PASSED                 [ 30%]
src/tests/test_stage9_decision.py::test_market_does_not_override_strong_fundamentals PASSED                      [ 38%]
src/tests/test_stage9_decision.py::test_usd_share_value_is_context_not_a_new_score PASSED                        [ 46%]
src/tests/test_stage9_decision.py::test_negative_eps_valuation_is_not_reconstructed_by_stage9 PASSED             [ 53%]
src/tests/test_stage9_decision.py::test_no_position_sizing_contract PASSED                                       [ 61%]
src/tests/test_stage9_decision.py::test_hysteresis_prevents_small_buy_to_hold_change PASSED                      [ 69%]
src/tests/test_stage9_decision.py::test_hysteresis_allows_material_deterioration PASSED                          [ 76%]
src/tests/test_stage9_decision.py::test_decision_history_contract PASSED                                         [ 84%]
src/tests/test_stage9_decision.py::test_ranking_contract_has_no_new_score PASSED                                 [ 92%]
src/tests/test_stage9_decision.py::test_dashboard_contract_carries_required_fields PASSED                        [100%]

================================================== warnings summary ===================================================
src/tests/test_stage9_decision.py: 13 warnings
  D:\winprojects\analyzer\src\tests\test_stage9_decision.py:16: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    calculation_timestamp=datetime.utcnow(),

src/tests/test_stage9_decision.py: 13 warnings
  D:\winprojects\analyzer\src\tests\test_stage9_decision.py:35: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    calculation_timestamp=datetime.utcnow(),

src/tests/test_stage9_decision.py: 13 warnings
  D:\winprojects\analyzer\src\tests\test_stage9_decision.py:45: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    as_of_date=datetime.utcnow(),

src/tests/test_stage9_decision.py: 13 warnings
  D:\winprojects\analyzer\src\decision\engine.py:260: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    calculation_timestamp = datetime.utcnow()

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================================== 13 passed, 52 warnings in 0.62s