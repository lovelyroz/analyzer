# P68
### گزارش پیاده‌سازی و ارزیابی مرحله ۷ و ۸ (بر اساس دستورالعمل PROMPT.md)

---

#### ۱. فایل‌های تغییریافته

* **وضعیت:** در این مرحله هیچ‌گونه تغییر مستقیم در فایل‌های سورس کد اعمال نشده است (طبق دستورالعمل، بازبینی و تحلیل به‌صورت ایستا انجام شده و هیچ کد یا تستی اجرا نشده است).

---

#### ۲. قرارداد داده‌های بازار مرحله ۸ (Workstream A)

* **شکل داده‌های ورودی:** موتور تحلیل بازار (`MarketEngine` در `src/market/engine.py`) نیازمند یک دنباله تاریخی منظم از داده‌های بازار (شامل قیمت‌های باز شدن، بیشترین، کمترین، آخرین قیمت و حجم معاملات - OHLCV) به همراه تاریخ‌های معتبر است.
* **مدل داده:** مدل `MarketDaily` در `src/models/market.py` مؤلفه‌های تقویم جلالی را پشتیبانی می‌کند و فیلد `trade_date` برای برخی رکوردهای قدیمی ممکن است `nullable` باشد.
* **محدودیت پرس‌وجو:** پرس‌وجوی فعلی موجود در `src/ingestion/market/queries.py` (مانند `select_market_price_as_of`) صرفاً برای بازیابی تک‌قیمت نقطه‌زمانی مرحله ۷ طراحی شده است و به‌تنهایی نمی‌تواند دنباله تاریخی سری زمانی مورد نیاز مرحله ۸ را تامین کند. بنابراین، یک پرس‌وجو یا سرویس مجزا برای بازیابی سری‌های تاریخی محدود شده به تاریخ `as-of` مورد نیاز است.

---

#### ۳. وضعیت یکپارچه‌سازی مرحله ۸ (Workstream B)

* **وضعیت اتصال:** از آنجا که قرارداد پرس‌وجوی سری‌های تاریخی بازار هنوز به‌طور کامل در سطح لایه داده پیاده‌سازی نشده است، اتصال پیش‌فرض یا گمانه‌زنی انجام نگرفت تا از نقض اصول نقطه‌زمانی (PIT) و ایجاد داده‌های مصنوعی جلوگیری شود. اتصال امن پس از نهایی شدن قرارداد پرس‌وجوی سری زمانی انجام خواهد شد.

---

#### ۴. بررسی رابط مراحل ۷، ۸ و ۹ (Workstream C)

* **ثبات EPS:** تأیید شد که مرحله ۵ به عنوان منبع معتبر EPS باقی مانده و مرحله ۷ مجاز به محاسبه مجدد EPS یا تغییر فرمول تعداد سهام نیست.
* **سازگاری داده‌ها:** نتایج تحلیل بازار مرحله ۸ باید با ساختار ورودی مرحله ۹ (`src/decision/service.py`) سازگار باشد. بررسی‌ها نشان داد که حفظ یکپارچه‌سازی هویت دوره و شرکت در تمامی مراحل الزامی است و نباید شواهد مفقود بازار به عنوان داده معتبر تفسیر شوند.

---

#### ۵. وضعیت موارد D1 تا D6 و محافظ‌های PIT (Workstream D & E)

* **موارد D1 تا D6:** رفتارهای حفاظتی حفظ شده‌اند؛ از جمله عدم انتشار هشدار تغییر ارزیابی (Assessment-Flip) بدون معیار معتبر، تفکیک دقیق `review_priority` از هشدارهای ریسک، و عدم اعمال فرمول‌های اختصاصی بدون قرارداد ورودی مصوب.
* **پارامترها و PIT (مورد D9):** درخواست‌های پارامتر تاریخ‌دار در صورت عدم وجود نسخه معتبر، رفتار شکست‌بسته (Fail-Closed) را حفظ می‌کنند و هیچ تاریخ `effective_from` خودسرانه‌ای برای دور زدن این قانون ایجاد نشده است.

---

#### ۶. یافته‌های بررسی استاتیک

* ساختار ماژول‌ها، واردات (Imports) و انواع داده‌ها در بخش‌های ارزیابی، تصمیم‌گیری و بازار از نظر سینتکسی بررسی شدند. هیچ مغایرت آشکاری در تعاریف اسکیماها مشاهده نشد، اما تکمیل زنجیره داده‌های تاریخی بازار (مرحله ۸) برای فعال‌سازی کامل سرویس تصمیم‌گیری الزامی است.

---

#### ۷. دستورات پاورشل برای اجرا توسط مالک

لطفاً برای بررسی صحت عملکردهای موجود، دستورات زیر را در محیط محلی خود اجرا فرمایید:

```powershell
# اجرای تست‌های مرتبط با مرحله ۷ و ۸
pytest src/tests/test_stage7_valuation.py src/tests/test_stage8_market.py src/tests/test_stage9_decision.py -v

# اجرای مجموعه کامل تست‌های رگرسیون پلتفرم
pytest src/tests/ -v

```

---

#### ۸. گام بعدی

* بالاترین اولویت باقی‌مانده در `stepsForStage7.md`، تکمیل لایه پرس‌وجوی سری زمانی تاریخی بازار برای پشتیبانی از `MarketEngine` است. بازنویسی نهایی `src/valuation/engine.py` همچنان به عنوان آخرین گام فنی دست‌نخورده باقی می‌ماند.
(analyzer) PS D:\winprojects\analyzer> pytest src/tests/test_stage7_valuation.py src/tests/test_stage8_market.py src/tests/test_stage9_decision.py -v
================================================= test session starts =================================================
platform win32 -- Python 3.12.9, pytest-9.1.1, pluggy-1.6.0 -- D:\winprojects\analyzer\Scripts\python.exe
cachedir: .pytest_cache
rootdir: D:\winprojects\analyzer
collected 124 items

src/tests/test_stage7_valuation.py::test_jalali_service_uses_selected_price_and_preserves_provenance PASSED      [  0%]
src/tests/test_stage7_valuation.py::test_jalali_service_fails_closed_without_eligible_observation PASSED         [  1%]
src/tests/test_stage7_valuation.py::test_jalali_service_rejects_forecast_from_another_company PASSED             [  2%]
src/tests/test_stage7_valuation.py::test_valuation_models PASSED                                                 [  3%]
src/tests/test_stage7_valuation.py::test_valuation_engine_forward_pe_and_expected_fair_value PASSED              [  4%]
src/tests/test_stage7_valuation.py::test_industry_forward_pe_requires_eight_valid_peers PASSED                   [  4%]
src/tests/test_stage7_valuation.py::test_industry_ttm_is_fallback_after_historical_median PASSED                 [  5%]
src/tests/test_stage7_valuation.py::test_negative_eps_does_not_create_fake_pe_or_fair_value PASSED               [  6%]
src/tests/test_stage7_valuation.py::test_reliability_does_not_change_forward_pe_or_fair_value PASSED             [  7%]
src/tests/test_stage7_valuation.py::test_direct_probability_adjustments_are_rejected_in_favor_of_family_evidence PASSED [  8%]
src/tests/test_stage7_valuation.py::test_probability_evidence_is_family_level_and_equal_weighted PASSED          [  8%]
src/tests/test_stage7_valuation.py::test_probability_evidence_rejects_unknown_or_incomplete_family_data PASSED   [  9%]
src/tests/test_stage7_valuation.py::test_scenario_multiple_adjustments_require_economic_rationale_and_are_bounded PASSED [ 10%]
src/tests/test_stage7_valuation.py::test_alerts_include_severity_and_driver_focus PASSED                         [ 11%]
src/tests/test_stage7_valuation.py::test_p2_sensitivity_drivers_present_and_bounded PASSED                       [ 12%]
src/tests/test_stage7_valuation.py::test_p2_sensitivity_missing_data_empty_drivers PASSED                        [ 12%]
src/tests/test_stage7_valuation.py::test_p2_sensitivity_deterministic_repeated_runs PASSED                       [ 13%]
src/tests/test_stage7_valuation.py::test_p2_alert_severity_levels_valid PASSED                                   [ 14%]
src/tests/test_stage7_valuation.py::test_p2_alert_low_reliability_threshold_boundaries PASSED                    [ 15%]
src/tests/test_stage7_valuation.py::test_p2_alert_high_dispersion_threshold_boundaries PASSED                    [ 16%]
src/tests/test_stage7_valuation.py::test_p2_alert_divergence_ratios_boundaries PASSED                            [ 16%]
src/tests/test_stage7_valuation.py::test_v1_sector_examples_use_only_eps_and_target_pe_drivers PASSED            [ 17%]
src/tests/test_stage7_valuation.py::test_v1_uses_stage5_eps_without_recalculating_from_net_profit PASSED         [ 18%]
src/tests/test_stage7_valuation.py::test_v1_defers_undefined_flip_dependence_and_assumption_alerts PASSED        [ 19%]
src/tests/test_stage7_valuation.py::test_p3_sensitivity_recomputes_from_valuation_identity PASSED                [ 20%]
src/tests/test_stage7_valuation.py::test_p3_nan_eps_is_guarded_as_invalid PASSED                                 [ 20%]
src/tests/test_stage7_valuation.py::test_p3_zero_and_negative_price_guarded PASSED                               [ 21%]
src/tests/test_stage7_valuation.py::test_p3_nonfinite_benchmark_series_filtered PASSED                           [ 22%]
src/tests/test_stage7_valuation.py::test_p3_nonfinite_scores_fall_back_to_defaults PASSED                        [ 23%]
src/tests/test_stage7_valuation.py::test_p3_flip_dependence_alerts_remain_explicitly_unresolved PASSED           [ 24%]
src/tests/test_stage7_valuation.py::test_p4_peer_count_below_minimum_falls_back PASSED                           [ 25%]
src/tests/test_stage7_valuation.py::test_p4_peer_count_at_minimum_selects_industry_forward PASSED                [ 25%]
src/tests/test_stage7_valuation.py::test_p4_peer_count_above_minimum_and_median_provenance PASSED                [ 26%]
src/tests/test_stage7_valuation.py::test_p4_peer_count_filters_invalid_values PASSED                             [ 27%]
src/tests/test_stage7_valuation.py::test_p4_peer_count_empty_data_reports_zero_and_falls_back PASSED             [ 28%]
src/tests/test_stage7_valuation.py::test_p4_benchmark_fallback_ignores_forward_count_for_ttm PASSED              [ 29%]
src/tests/test_stage7_valuation.py::test_p5_nonfinite_price_yields_null_outputs PASSED                           [ 29%]
src/tests/test_stage7_valuation.py::test_p5_missing_eps_is_not_applicable_not_zero PASSED                        [ 30%]
src/tests/test_stage7_valuation.py::test_p5_nonfinite_reliability_echo_sanitized PASSED                          [ 31%]
src/tests/test_stage7_valuation.py::test_p5_nonfinite_probability_confidence_echo_finite PASSED                  [ 32%]
src/tests/test_stage7_valuation.py::test_p5_missing_data_quality_does_not_crash PASSED                           [ 33%]
src/tests/test_stage7_valuation.py::test_p5_nonfinite_multiple_adjustment_rejected PASSED                        [ 33%]
src/tests/test_stage7_valuation.py::test_p5_nan_probability_evidence_rejected PASSED                             [ 34%]
src/tests/test_stage7_valuation.py::test_p5_datetime_echoes_normalized_to_utc PASSED                             [ 35%]
src/tests/test_stage7_valuation.py::test_p5_default_cutoff_inherits_forecast_cutoff_normalized PASSED            [ 36%]
src/tests/test_stage7_valuation.py::test_p5_undated_benchmark_series_carry_no_provenance PASSED                  [ 37%]
src/tests/test_stage7_valuation.py::test_p6_production_path_real_stage5_forecast PASSED                          [ 37%]
src/tests/test_stage7_valuation.py::test_p6_cutoff_pit_limitation_pinned PASSED                                  [ 38%]
src/tests/test_stage7_valuation.py::test_p6_missing_benchmarks_yield_guarded_nulls PASSED                        [ 39%]
src/tests/test_stage7_valuation.py::test_p6_scenario_ordering_flag_and_probability_normalization PASSED          [ 40%]
src/tests/test_stage7_valuation.py::test_p6_invalid_eps_variants_never_fabricate_values PASSED                   [ 41%]
src/tests/test_stage7_valuation.py::test_p6_repeat_runs_identical_on_full_contract PASSED                        [ 41%]
src/tests/test_stage7_valuation.py::test_p6_regression_prior_behavior_preserved PASSED                           [ 42%]
src/tests/test_stage7_valuation.py::test_p10_expensive_base_upside_parameterized_outputs_unchanged PASSED        [ 43%]
src/tests/test_stage7_valuation.py::test_p10_expensive_threshold_consumed_from_parameters PASSED                 [ 44%]
src/tests/test_stage7_valuation.py::test_p12_calculation_timestamp_utc_aware_and_deterministic PASSED            [ 45%]
src/tests/test_stage7_valuation.py::test_p32_input_refs_before_cutoff_leave_results_unchanged PASSED             [ 45%]
src/tests/test_stage7_valuation.py::test_p32_input_ref_after_cutoff_rejected_on_valuation_path PASSED            [ 46%]
src/tests/test_stage7_valuation.py::test_p32_input_ref_at_cutoff_boundary_accepted PASSED                        [ 47%]
src/tests/test_stage7_valuation.py::test_p32_input_ref_missing_date_rejected PASSED                              [ 48%]
src/tests/test_stage7_valuation.py::test_p32_input_refs_absent_preserves_legacy_path PASSED                      [ 49%]
src/tests/test_stage7_valuation.py::test_p53_embedded_forecast_input_ref_at_cutoff_is_enforced_and_accepted PASSED [ 50%]
src/tests/test_stage7_valuation.py::test_p53_stage5_dropped_future_input_is_not_reintroduced_to_stage7 PASSED    [ 50%]
src/tests/test_stage7_valuation.py::test_p53_embedded_forecast_input_ref_without_availability_is_rejected PASSED [ 51%]
src/tests/test_stage7_valuation.py::test_p53_explicit_empty_refs_do_not_bypass_embedded_forecast_provenance PASSED [ 52%]
src/tests/test_stage7_valuation.py::test_p53_stage5_forecast_without_provenance_preserves_legacy_path PASSED     [ 53%]
src/tests/test_stage7_valuation.py::test_p33_genesis_snapshot_matches_live_constants PASSED                      [ 54%]
src/tests/test_stage7_valuation.py::test_p33_result_carries_parameter_audit PASSED                               [ 54%]
src/tests/test_stage7_valuation.py::test_p33_resolve_exact_key_and_missing_raises PASSED                         [ 55%]
src/tests/test_stage7_valuation.py::test_p33_as_of_without_dated_records_raises PASSED                           [ 56%]
src/tests/test_stage7_valuation.py::test_p33_as_of_selection_mechanics PASSED                                    [ 57%]
src/tests/test_stage7_valuation.py::test_p33_as_of_overlap_raises_ambiguity PASSED                               [ 58%]
src/tests/test_stage7_valuation.py::test_p35_legacy_path_provenance_is_truthful_and_unchanged PASSED             [ 58%]
src/tests/test_stage7_valuation.py::test_p35_snapshot_reports_values_actually_consumed_when_module_constant_changes PASSED [ 59%]
src/tests/test_stage7_valuation.py::test_p35_as_of_selection_governs_calculation_and_snapshot_matches PASSED     [ 60%]
src/tests/test_stage7_valuation.py::test_p35_selected_set_governs_peers_alerts_and_scenario_weights PASSED       [ 61%]
src/tests/test_stage7_valuation.py::test_p35_missing_or_ambiguous_as_of_selection_fails_closed PASSED            [ 62%]
src/tests/test_stage7_valuation.py::test_p35_invalid_parameter_set_raises_without_fallback_to_constants PASSED   [ 62%]
src/tests/test_stage7_valuation.py::test_p35_isolation_from_global_mutation_and_snapshot_aliasing PASSED         [ 63%]
src/tests/test_stage7_valuation.py::test_p35_repeated_as_of_calculations_are_deterministic PASSED                [ 64%]
src/tests/test_stage7_valuation.py::test_d9_effective_cutoff_governs_selection_not_valuation_date PASSED         [ 65%]
src/tests/test_stage7_valuation.py::test_d9_exact_effective_from_boundary_is_accepted PASSED                     [ 66%]
src/tests/test_stage7_valuation.py::test_d9_future_effective_version_is_rejected PASSED                          [ 66%]
src/tests/test_stage7_valuation.py::test_d9_missing_eligible_dated_version_fails_closed_without_genesis_fallback PASSED [ 67%]
src/tests/test_stage7_valuation.py::test_d9_overlapping_eligible_versions_are_deterministic PASSED               [ 68%]
src/tests/test_stage7_valuation.py::test_d9_conflicting_parameter_as_of_is_rejected PASSED                       [ 69%]
src/tests/test_stage7_valuation.py::test_d9_without_any_cutoff_caller_supplied_as_of_is_labelled_truthfully PASSED [ 70%]
src/tests/test_stage7_valuation.py::test_d9_metadata_distinguishes_dated_selection_from_legacy_genesis PASSED    [ 70%]
src/tests/test_stage7_valuation.py::test_d9_legacy_path_stays_backward_compatible_and_never_claims_pit PASSED    [ 71%]
src/tests/test_stage7_valuation.py::test_d9_cutoff_governed_selection_is_deterministic_on_repeat PASSED          [ 72%]
src/tests/test_stage8_market.py::test_legacy_indicator_helpers_remain_available PASSED                           [ 73%]
src/tests/test_stage8_market.py::test_core_market_indicators PASSED                                              [ 74%]
src/tests/test_stage8_market.py::test_market_engine_returns_state_not_score PASSED                               [ 75%]
src/tests/test_stage8_market.py::test_market_output_contract_includes_52w_volume_and_value_context PASSED        [ 75%]
src/tests/test_stage8_market.py::test_trading_value_stability_is_coefficient_of_variation PASSED                 [ 76%]
src/tests/test_stage8_market.py::test_close_fallback_is_explicitly_flagged PASSED                                [ 77%]
src/tests/test_stage8_market.py::test_point_in_time_excludes_future_rows PASSED                                  [ 78%]
src/tests/test_stage8_market.py::test_adjusted_close_drives_historical_returns PASSED                            [ 79%]
src/tests/test_stage8_market.py::test_missing_benchmark_does_not_create_synthetic_relative_strength PASSED       [ 79%]
src/tests/test_stage8_market.py::test_relative_strength_uses_same_horizon PASSED                                 [ 80%]
src/tests/test_stage8_market.py::test_negative_market_state_generates_context_alerts_not_decision PASSED         [ 81%]
src/tests/test_stage8_market.py::test_drawdown_moderate_non_recovering_is_not_labeled_recovering PASSED          [ 82%]
src/tests/test_stage8_market.py::test_drawdown_recovery_requires_rebound_from_recent_low PASSED                  [ 83%]
src/tests/test_stage8_market.py::test_drawdown_deep_and_new_low_states_remain_distinct PASSED                    [ 83%]
src/tests/test_stage8_market.py::test_legacy_api_is_compatibility_only PASSED                                    [ 84%]
src/tests/test_stage9_decision.py::test_strong_buy_requires_aligned_families PASSED                              [ 85%]
src/tests/test_stage9_decision.py::test_jalali_orchestration_passes_stage7_result_to_stage9 PASSED               [ 86%]
src/tests/test_stage9_decision.py::test_jalali_orchestration_rejects_mismatched_fundamental_and_market_identity PASSED [ 87%]
src/tests/test_stage9_decision.py::test_value_trap_does_not_become_buy PASSED                                    [ 87%]
src/tests/test_stage9_decision.py::test_strong_but_expensive_is_not_buy PASSED                                   [ 88%]
src/tests/test_stage9_decision.py::test_low_forecast_reliability_limits_strong_conviction PASSED                 [ 89%]
src/tests/test_stage9_decision.py::test_market_does_not_override_strong_fundamentals PASSED                      [ 90%]
src/tests/test_stage9_decision.py::test_usd_share_value_is_context_not_a_new_score PASSED                        [ 91%]
src/tests/test_stage9_decision.py::test_negative_eps_valuation_is_not_reconstructed_by_stage9 PASSED             [ 91%]
src/tests/test_stage9_decision.py::test_no_position_sizing_contract PASSED                                       [ 92%]
src/tests/test_stage9_decision.py::test_hysteresis_prevents_small_buy_to_hold_change PASSED                      [ 93%]
src/tests/test_stage9_decision.py::test_hysteresis_allows_material_deterioration PASSED                          [ 94%]
src/tests/test_stage9_decision.py::test_decision_history_contract PASSED                                         [ 95%]
src/tests/test_stage9_decision.py::test_ranking_contract_has_no_new_score PASSED                                 [ 95%]
src/tests/test_stage9_decision.py::test_dashboard_contract_carries_required_fields PASSED                        [ 96%]
src/tests/test_stage9_decision.py::test_scenario_dispersion_threshold_boundaries PASSED                          [ 97%]
src/tests/test_stage9_decision.py::test_scenario_dispersion_causes_ten_point_confidence_deduction PASSED         [ 98%]
src/tests/test_stage9_decision.py::test_scenario_dispersion_blocks_strong_buy PASSED                             [ 99%]
src/tests/test_stage9_decision.py::test_scenario_dispersion_penalty_distinct_from_valuation_risk_level_high PASSED [100%]

================================================= 124 passed in 2.60s =================================================
(analyzer) PS D:\winprojects\analyzer> pytest src/tests/ -v
================================================= test session starts =================================================
platform win32 -- Python 3.12.9, pytest-9.1.1, pluggy-1.6.0 -- D:\winprojects\analyzer\Scripts\python.exe
cachedir: .pytest_cache
rootdir: D:\winprojects\analyzer
collected 1110 items

src/tests/test_codal_acquisition.py::test_local_pdf_acquisition_preserves_source_and_bytes PASSED                [  0%]
src/tests/test_codal_acquisition.py::test_missing_source_is_distinguished_as_acquisition_failure PASSED          [  0%]
src/tests/test_codal_acquisition.py::test_non_pdf_local_source_is_rejected PASSED                                [  0%]
src/tests/test_codal_digit_normalization.py::test_normalize_digits_maps_persian_and_arabic_indic_to_ascii PASSED [  0%]
src/tests/test_codal_digit_normalization.py::test_parse_amount_accepts_persian_digits_and_arabic_separators PASSED [  0%]
src/tests/test_codal_extraction.py::test_normalize_persian_digits PASSED                                         [  0%]
src/tests/test_codal_extraction.py::test_parse_amount_null_not_zero PASSED                                       [  0%]
src/tests/test_codal_extraction.py::test_fix_persian_rtl_preserves_extracted_text PASSED                         [  0%]
src/tests/test_codal_extraction.py::test_extract_text_pdf_lines PASSED                                           [  0%]
src/tests/test_codal_extraction.py::test_extract_missing_stays_none PASSED                                       [  0%]
src/tests/test_codal_extraction.py::test_extract_non_pdf_fails PASSED                                            [  0%]
src/tests/test_codal_extraction.py::test_pipeline_persists_report_version_and_raw PASSED                         [  1%]
src/tests/test_codal_extraction.py::test_pipeline_acquisition_failure_is_audited_without_partial_writes PASSED   [  1%]
src/tests/test_codal_extraction.py::test_pipeline_extraction_failure_is_audited_without_partial_writes PASSED    [  1%]
src/tests/test_codal_extraction.py::test_pipeline_idempotent_version_chain PASSED                                [  1%]
src/tests/test_codal_extraction.py::test_codal_ingestion_rejects_period_owned_by_another_company PASSED          [  1%]
src/tests/test_codal_extraction.py::test_codal_tracking_id_cannot_be_reused_for_another_company_or_period PASSED [  1%]
src/tests/test_codal_extraction.py::test_real_codal_monthly_activity_pdf SKIPPED (real Codal sample PDF not ...) [  1%]
src/tests/test_codal_pdf_extraction.py::test_codal_validation_corpus_inventory_is_exactly_locked_19_pdfs PASSED  [  1%]
src/tests/test_codal_pdf_extraction.py::test_persian_numeric_normalization_preserves_missing_and_negative_values PASSED [  1%]
src/tests/test_codal_pdf_extraction.py::test_text_parser_preserves_row_and_column_for_multi_value_statement_rows PASSED [  1%]
src/tests/test_codal_pdf_extraction.py::test_table_extractor_does_not_treat_dates_as_amounts PASSED              [  1%]
src/tests/test_codal_pdf_extraction.py::test_rtl_pdf_line_extracts_trailing_label_without_reversing_text PASSED  [  2%]
src/tests/test_codal_pdf_extraction.py::test_representative_monthly_codal_pdf_returns_raw_dto_contract PASSED    [  2%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_extraction_is_deterministic_across_three_independent_runs[seo-codal-report (1).pdf] PASSED [  2%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_extraction_is_deterministic_across_three_independent_runs[seo-codal-report (10).pdf] PASSED [  2%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_extraction_is_deterministic_across_three_independent_runs[seo-codal-report (11).pdf] PASSED [  2%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_extraction_is_deterministic_across_three_independent_runs[seo-codal-report (12).pdf] PASSED [  2%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_extraction_is_deterministic_across_three_independent_runs[seo-codal-report (13).pdf] PASSED [  2%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_extraction_is_deterministic_across_three_independent_runs[seo-codal-report (14).pdf] PASSED [  2%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_extraction_is_deterministic_across_three_independent_runs[seo-codal-report (15).pdf] PASSED [  2%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_extraction_is_deterministic_across_three_independent_runs[seo-codal-report (16).pdf] PASSED [  2%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_extraction_is_deterministic_across_three_independent_runs[seo-codal-report (19).pdf] PASSED [  2%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_extraction_is_deterministic_across_three_independent_runs[seo-codal-report (2).pdf] PASSED [  3%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_extraction_is_deterministic_across_three_independent_runs[seo-codal-report (20).pdf] PASSED [  3%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_extraction_is_deterministic_across_three_independent_runs[seo-codal-report (25).pdf] PASSED [  3%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_extraction_is_deterministic_across_three_independent_runs[seo-codal-report (26).pdf] PASSED [  3%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_extraction_is_deterministic_across_three_independent_runs[seo-codal-report (3).pdf] PASSED [  3%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_extraction_is_deterministic_across_three_independent_runs[seo-codal-report (4).pdf] PASSED [  3%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_extraction_is_deterministic_across_three_independent_runs[seo-codal-report (6).pdf] PASSED [  3%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_extraction_is_deterministic_across_three_independent_runs[seo-codal-report (7).pdf] PASSED [  3%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_extraction_is_deterministic_across_three_independent_runs[seo-codal-report (8).pdf] PASSED [  3%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_extraction_is_deterministic_across_three_independent_runs[seo-codal-report (9).pdf] PASSED [  3%]
src/tests/test_codal_pdf_extraction.py::test_representative_codal_layouts_extract_rows[seo-codal-report (1).pdf] PASSED [  3%]
src/tests/test_codal_pdf_extraction.py::test_representative_codal_layouts_extract_rows[seo-codal-report (10).pdf] PASSED [  4%]
src/tests/test_codal_pdf_extraction.py::test_representative_codal_layouts_extract_rows[seo-codal-report (11).pdf] PASSED [  4%]
src/tests/test_codal_pdf_extraction.py::test_representative_codal_layouts_extract_rows[seo-codal-report (12).pdf] PASSED [  4%]
src/tests/test_codal_pdf_extraction.py::test_representative_codal_layouts_extract_rows[seo-codal-report (13).pdf] PASSED [  4%]
src/tests/test_codal_pdf_extraction.py::test_representative_codal_layouts_extract_rows[seo-codal-report (14).pdf] PASSED [  4%]
src/tests/test_codal_pdf_extraction.py::test_representative_codal_layouts_extract_rows[seo-codal-report (15).pdf] PASSED [  4%]
src/tests/test_codal_pdf_extraction.py::test_representative_codal_layouts_extract_rows[seo-codal-report (16).pdf] PASSED [  4%]
src/tests/test_codal_pdf_extraction.py::test_representative_codal_layouts_extract_rows[seo-codal-report (19).pdf] PASSED [  4%]
src/tests/test_codal_pdf_extraction.py::test_representative_codal_layouts_extract_rows[seo-codal-report (2).pdf] PASSED [  4%]
src/tests/test_codal_pdf_extraction.py::test_representative_codal_layouts_extract_rows[seo-codal-report (20).pdf] PASSED [  4%]
src/tests/test_codal_pdf_extraction.py::test_representative_codal_layouts_extract_rows[seo-codal-report (25).pdf] PASSED [  4%]
src/tests/test_codal_pdf_extraction.py::test_representative_codal_layouts_extract_rows[seo-codal-report (26).pdf] PASSED [  5%]
src/tests/test_codal_pdf_extraction.py::test_representative_codal_layouts_extract_rows[seo-codal-report (3).pdf] PASSED [  5%]
src/tests/test_codal_pdf_extraction.py::test_representative_codal_layouts_extract_rows[seo-codal-report (4).pdf] PASSED [  5%]
src/tests/test_codal_pdf_extraction.py::test_representative_codal_layouts_extract_rows[seo-codal-report (6).pdf] PASSED [  5%]
src/tests/test_codal_pdf_extraction.py::test_representative_codal_layouts_extract_rows[seo-codal-report (7).pdf] PASSED [  5%]
src/tests/test_codal_pdf_extraction.py::test_representative_codal_layouts_extract_rows[seo-codal-report (8).pdf] PASSED [  5%]
src/tests/test_codal_pdf_extraction.py::test_representative_codal_layouts_extract_rows[seo-codal-report (9).pdf] PASSED [  5%]
src/tests/test_codal_pdf_extraction.py::test_extraction_keeps_blank_and_explicit_zero_distinct[-0] PASSED        [  5%]
src/tests/test_codal_pdf_extraction.py::test_extraction_keeps_blank_and_explicit_zero_distinct[--0] PASSED       [  5%]
src/tests/test_codal_pdf_extraction.py::test_extraction_keeps_blank_and_explicit_zero_distinct[\u2014-(0)] PASSED [  5%]
src/tests/test_codal_pdf_extraction.py::test_malformed_pdf_is_rejected_and_ingestion_is_audited PASSED           [  5%]
src/tests/test_codal_pdf_extraction.py::test_all_supplied_codal_pdfs_have_explicit_extraction_outcomes PASSED    [  6%]
src/tests/test_codal_pdf_extraction.py::test_null_and_explicit_zero_persist_as_distinct_values PASSED            [  6%]
src/tests/test_codal_pdf_extraction.py::test_codal_raw_text_fields_are_ascii_normalized_before_persistence PASSED [  6%]
src/tests/test_codal_pdf_extraction.py::test_representative_codal_samples_load_into_core_persistence PASSED      [  6%]
src/tests/test_codal_pdf_extraction.py::test_independent_final_foundation_audit_checks_pit_provenance_and_version_invariants PASSED [  6%]
src/tests/test_codal_pdf_extraction.py::test_pdf_output_loads_into_core_persistence_and_duplicate_is_idempotent PASSED [  6%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_ingestion_is_idempotent_across_three_cycles[seo-codal-report (1).pdf] PASSED [  6%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_ingestion_is_idempotent_across_three_cycles[seo-codal-report (10).pdf] PASSED [  6%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_ingestion_is_idempotent_across_three_cycles[seo-codal-report (11).pdf] PASSED [  6%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_ingestion_is_idempotent_across_three_cycles[seo-codal-report (12).pdf] PASSED [  6%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_ingestion_is_idempotent_across_three_cycles[seo-codal-report (13).pdf] PASSED [  6%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_ingestion_is_idempotent_across_three_cycles[seo-codal-report (14).pdf] PASSED [  7%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_ingestion_is_idempotent_across_three_cycles[seo-codal-report (15).pdf] PASSED [  7%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_ingestion_is_idempotent_across_three_cycles[seo-codal-report (16).pdf] PASSED [  7%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_ingestion_is_idempotent_across_three_cycles[seo-codal-report (19).pdf] PASSED [  7%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_ingestion_is_idempotent_across_three_cycles[seo-codal-report (2).pdf] PASSED [  7%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_ingestion_is_idempotent_across_three_cycles[seo-codal-report (20).pdf] PASSED [  7%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_ingestion_is_idempotent_across_three_cycles[seo-codal-report (25).pdf] PASSED [  7%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_ingestion_is_idempotent_across_three_cycles[seo-codal-report (26).pdf] PASSED [  7%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_ingestion_is_idempotent_across_three_cycles[seo-codal-report (3).pdf] PASSED [  7%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_ingestion_is_idempotent_across_three_cycles[seo-codal-report (4).pdf] PASSED [  7%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_ingestion_is_idempotent_across_three_cycles[seo-codal-report (6).pdf] PASSED [  7%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_ingestion_is_idempotent_across_three_cycles[seo-codal-report (7).pdf] PASSED [  8%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_ingestion_is_idempotent_across_three_cycles[seo-codal-report (8).pdf] PASSED [  8%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_ingestion_is_idempotent_across_three_cycles[seo-codal-report (9).pdf] PASSED [  8%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_persistence_satisfies_hard_invariants[seo-codal-report (1).pdf] PASSED [  8%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_persistence_satisfies_hard_invariants[seo-codal-report (10).pdf] PASSED [  8%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_persistence_satisfies_hard_invariants[seo-codal-report (11).pdf] PASSED [  8%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_persistence_satisfies_hard_invariants[seo-codal-report (12).pdf] PASSED [  8%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_persistence_satisfies_hard_invariants[seo-codal-report (13).pdf] PASSED [  8%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_persistence_satisfies_hard_invariants[seo-codal-report (14).pdf] PASSED [  8%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_persistence_satisfies_hard_invariants[seo-codal-report (15).pdf] PASSED [  8%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_persistence_satisfies_hard_invariants[seo-codal-report (16).pdf] PASSED [  8%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_persistence_satisfies_hard_invariants[seo-codal-report (19).pdf] PASSED [  9%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_persistence_satisfies_hard_invariants[seo-codal-report (2).pdf] PASSED [  9%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_persistence_satisfies_hard_invariants[seo-codal-report (20).pdf] PASSED [  9%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_persistence_satisfies_hard_invariants[seo-codal-report (25).pdf] PASSED [  9%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_persistence_satisfies_hard_invariants[seo-codal-report (26).pdf] PASSED [  9%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_persistence_satisfies_hard_invariants[seo-codal-report (3).pdf] PASSED [  9%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_persistence_satisfies_hard_invariants[seo-codal-report (4).pdf] PASSED [  9%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_persistence_satisfies_hard_invariants[seo-codal-report (6).pdf] PASSED [  9%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_persistence_satisfies_hard_invariants[seo-codal-report (7).pdf] PASSED [  9%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_persistence_satisfies_hard_invariants[seo-codal-report (8).pdf] PASSED [  9%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_persistence_satisfies_hard_invariants[seo-codal-report (9).pdf] PASSED [  9%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_pit_and_version_invariants[seo-codal-report (1).pdf] PASSED [ 10%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_pit_and_version_invariants[seo-codal-report (10).pdf] PASSED [ 10%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_pit_and_version_invariants[seo-codal-report (11).pdf] PASSED [ 10%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_pit_and_version_invariants[seo-codal-report (12).pdf] PASSED [ 10%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_pit_and_version_invariants[seo-codal-report (13).pdf] PASSED [ 10%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_pit_and_version_invariants[seo-codal-report (14).pdf] PASSED [ 10%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_pit_and_version_invariants[seo-codal-report (15).pdf] PASSED [ 10%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_pit_and_version_invariants[seo-codal-report (16).pdf] PASSED [ 10%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_pit_and_version_invariants[seo-codal-report (19).pdf] PASSED [ 10%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_pit_and_version_invariants[seo-codal-report (2).pdf] PASSED [ 10%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_pit_and_version_invariants[seo-codal-report (20).pdf] PASSED [ 10%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_pit_and_version_invariants[seo-codal-report (25).pdf] PASSED [ 10%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_pit_and_version_invariants[seo-codal-report (26).pdf] PASSED [ 11%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_pit_and_version_invariants[seo-codal-report (3).pdf] PASSED [ 11%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_pit_and_version_invariants[seo-codal-report (4).pdf] PASSED [ 11%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_pit_and_version_invariants[seo-codal-report (6).pdf] PASSED [ 11%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_pit_and_version_invariants[seo-codal-report (7).pdf] PASSED [ 11%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_pit_and_version_invariants[seo-codal-report (8).pdf] PASSED [ 11%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_pit_and_version_invariants[seo-codal-report (9).pdf] PASSED [ 11%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_version_chain_preserves_history[seo-codal-report (1).pdf] PASSED [ 11%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_version_chain_preserves_history[seo-codal-report (10).pdf] PASSED [ 11%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_version_chain_preserves_history[seo-codal-report (11).pdf] PASSED [ 11%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_version_chain_preserves_history[seo-codal-report (12).pdf] PASSED [ 11%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_version_chain_preserves_history[seo-codal-report (13).pdf] PASSED [ 12%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_version_chain_preserves_history[seo-codal-report (14).pdf] PASSED [ 12%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_version_chain_preserves_history[seo-codal-report (15).pdf] PASSED [ 12%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_version_chain_preserves_history[seo-codal-report (16).pdf] PASSED [ 12%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_version_chain_preserves_history[seo-codal-report (19).pdf] PASSED [ 12%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_version_chain_preserves_history[seo-codal-report (2).pdf] PASSED [ 12%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_version_chain_preserves_history[seo-codal-report (20).pdf] PASSED [ 12%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_version_chain_preserves_history[seo-codal-report (25).pdf] PASSED [ 12%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_version_chain_preserves_history[seo-codal-report (26).pdf] PASSED [ 12%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_version_chain_preserves_history[seo-codal-report (3).pdf] PASSED [ 12%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_version_chain_preserves_history[seo-codal-report (4).pdf] PASSED [ 12%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_version_chain_preserves_history[seo-codal-report (6).pdf] PASSED [ 13%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_version_chain_preserves_history[seo-codal-report (7).pdf] PASSED [ 13%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_version_chain_preserves_history[seo-codal-report (8).pdf] PASSED [ 13%]
src/tests/test_codal_pdf_extraction.py::test_locked_codal_corpus_version_chain_preserves_history[seo-codal-report (9).pdf] PASSED [ 13%]
src/tests/test_codal_pdf_extraction.py::test_codal_pdf_facade_connects_extraction_to_raw_persistence PASSED      [ 13%]
src/tests/test_ingestion_fx.py::test_free_market_and_operational_are_stored_separately PASSED                    [ 13%]
src/tests/test_ingestion_fx.py::test_fx_idempotent_upsert_jalali PASSED                                          [ 13%]
src/tests/test_ingestion_fx.py::test_invalid_rate_type_and_non_positive_rate_fail_explicitly PASSED              [ 13%]
src/tests/test_ingestion_fx.py::test_operational_never_defaults_to_free_market PASSED                            [ 13%]
src/tests/test_ingestion_fx.py::test_fx_ingestion_run_audit PASSED                                               [ 13%]
src/tests/test_ingestion_fx.py::test_same_month_across_years_fx PASSED                                           [ 13%]
src/tests/test_ingestion_fx.py::test_ingest_fx_xlsx_toman_and_rial SKIPPED (could not import 'openpyxl': No ...) [ 14%]
src/tests/test_ingestion_fx.py::test_migration_6_adds_fx_jalali_columns PASSED                                   [ 14%]
src/tests/test_ingestion_ohlc.py::test_parse_jalali_components PASSED                                            [ 14%]
src/tests/test_ingestion_ohlc.py::test_ohlc_ingestion_skips_missing_and_malformed_jalali_dates PASSED            [ 14%]
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_selects_exact_date_and_preserves_provenance PASSED     [ 14%]
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_uses_latest_prior_date_across_year_boundary PASSED     [ 14%]
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_returns_none_when_no_eligible_price PASSED             [ 14%]
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_rejects_missing_or_invalid_requested_date PASSED       [ 14%]
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_discards_impossible_stored_date PASSED                 [ 14%]
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_accepts_valid_jalali_month_end_and_leap_boundary PASSED [ 14%]
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_isolates_company_and_ignores_undated_rows PASSED       [ 14%]
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_rejects_duplicate_latest_jalali_observations PASSED    [ 15%]
src/tests/test_ingestion_ohlc.py::test_null_not_zero PASSED                                                      [ 15%]
src/tests/test_ingestion_ohlc.py::test_same_month_across_years PASSED                                            [ 15%]
src/tests/test_ingestion_ohlc.py::test_ingest_ohlc_idempotent PASSED                                             [ 15%]
src/tests/test_ingestion_ohlc.py::test_migration_5_adds_jalali_columns PASSED                                    [ 15%]
src/tests/test_market_history_query.py::test_history_is_ordered_oldest_first_across_month_and_year_boundaries PASSED [ 15%]
src/tests/test_market_history_query.py::test_history_as_of_boundary_is_inclusive_and_excludes_every_future_row PASSED [ 15%]
src/tests/test_market_history_query.py::test_history_earlier_month_with_larger_day_is_not_excluded PASSED        [ 15%]
src/tests/test_market_history_query.py::test_history_is_isolated_by_company PASSED                               [ 15%]
src/tests/test_market_history_query.py::test_history_without_rows_returns_empty_tuple PASSED                     [ 15%]
src/tests/test_market_history_query.py::test_history_excludes_legacy_rows_without_complete_jalali_date PASSED    [ 15%]
src/tests/test_market_history_query.py::test_history_preserves_missing_values_as_none_and_provenance PASSED      [ 16%]
src/tests/test_market_history_query.py::test_history_duplicate_company_date_fails_explicitly PASSED              [ 16%]
src/tests/test_market_history_query.py::test_history_duplicate_after_as_of_does_not_block_earlier_history PASSED [ 16%]
src/tests/test_market_history_query.py::test_history_rejects_invalid_as_of_dates[bad_date0] PASSED               [ 16%]
src/tests/test_market_history_query.py::test_history_rejects_invalid_as_of_dates[bad_date1] PASSED               [ 16%]
src/tests/test_market_history_query.py::test_history_rejects_invalid_as_of_dates[bad_date2] PASSED               [ 16%]
src/tests/test_market_history_query.py::test_history_rejects_invalid_as_of_dates[bad_date3] PASSED               [ 16%]
src/tests/test_market_history_query.py::test_history_rejects_invalid_as_of_dates[1405-02-11] PASSED              [ 16%]
src/tests/test_market_history_query.py::test_history_rejects_invalid_as_of_dates[bad_date5] PASSED               [ 16%]
src/tests/test_market_history_query.py::test_history_rejects_invalid_as_of_dates[bad_date6] PASSED               [ 16%]
src/tests/test_market_history_query.py::test_history_rejects_invalid_as_of_dates[None] PASSED                    [ 16%]
src/tests/test_stage1_database_architecture.py::test_normalized_fact_supports_multiple_raw_inputs_without_duplicate_metric_rows PASSED [ 17%]
src/tests/test_stage1_database_integrity.py::test_migration_reaches_version_seven_and_is_idempotent PASSED       [ 17%]
src/tests/test_stage1_database_integrity.py::test_current_report_version_unique_index_is_present_on_bootstrap PASSED [ 17%]
src/tests/test_stage1_database_integrity.py::test_current_report_version_constraint_rejects_two_current_versions PASSED [ 17%]
src/tests/test_stage1_rules.py::test_all_stage1_tables_create PASSED                                             [ 17%]
src/tests/test_stage1_rules.py::test_null_value_preservation_and_raw_provenance PASSED                           [ 17%]
src/tests/test_stage1_rules.py::test_financial_period_fk_and_type_constraints PASSED                             [ 17%]
src/tests/test_stage1_rules.py::test_report_version_uniqueness_and_restatement_chain PASSED                      [ 17%]
src/tests/test_stage1_rules.py::test_point_in_time_selector_never_uses_future_version PASSED                     [ 17%]
src/tests/test_stage1_rules.py::test_fx_free_and_operational_are_distinct PASSED                                 [ 17%]
src/tests/test_stage1_rules.py::test_fx_conversion_rule_contracts PASSED                                         [ 17%]
src/tests/test_stage1_rules.py::test_quality_status_and_eps_metadata PASSED                                      [ 18%]
src/tests/test_stage1_rules.py::test_market_daily_allows_missing_adjusted_close_and_keeps_source PASSED          [ 18%]
src/tests/test_stage1_rules.py::test_share_history_and_corporate_action_fields PASSED                            [ 18%]
src/tests/test_stage1_rules.py::test_ingestion_run_contract PASSED                                               [ 18%]
src/tests/test_stage1_rules.py::test_migration_runner_upgrades_empty_database_and_is_idempotent PASSED           [ 18%]
src/tests/test_stage1_rules.py::test_migration_runner_upgrades_legacy_stage1_schema PASSED                       [ 18%]
src/tests/test_stage2_kpis.py::test_calculate_ttm_valid PASSED                                                   [ 18%]
src/tests/test_stage2_kpis.py::test_calculate_ttm_insufficient_or_missing_data PASSED                            [ 18%]
src/tests/test_stage2_kpis.py::test_calculate_yoy_growth PASSED                                                  [ 18%]
src/tests/test_stage2_kpis.py::test_universal_growth_kpis PASSED                                                 [ 18%]
src/tests/test_stage2_kpis.py::test_universal_growth_zero_base_is_not_zero_growth PASSED                         [ 18%]
src/tests/test_stage2_kpis.py::test_universal_profitability_kpis PASSED                                          [ 19%]
src/tests/test_stage2_kpis.py::test_universal_profitability_zero_denominators_are_missing PASSED                 [ 19%]
src/tests/test_stage2_kpis.py::test_universal_risk_and_quality_kpis PASSED                                       [ 19%]
src/tests/test_stage2_kpis.py::test_conditional_financial_cost_pressure PASSED                                   [ 19%]
src/tests/test_stage2_kpis.py::test_bank_industry_kpis PASSED                                                    [ 19%]
src/tests/test_stage2_kpis.py::test_holding_industry_kpis PASSED                                                 [ 19%]
src/tests/test_stage2_kpis.py::test_industry_zero_kpis PASSED                                                    [ 19%]
src/tests/test_stage2_kpis.py::test_optional_sales_volume_missing_is_not_zero PASSED                             [ 19%]
src/tests/test_stage2_kpis.py::test_eps_growth_requires_share_count_corporate_action_comparability PASSED        [ 19%]
src/tests/test_stage2_kpis.py::test_data_quality_status_propagates_from_stage1_inputs PASSED                     [ 19%]
src/tests/test_stage2_kpis.py::test_industry_kpi_data_quality_propagates PASSED                                  [ 19%]
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run PASSED                                                   [ 20%]
src/tests/test_stage3_scoring.py::test_fixed_axis_weights_match_locked_spec PASSED                               [ 20%]
src/tests/test_stage3_scoring.py::test_industry_profiles_keep_each_axis_at_one_hundred_percent PASSED            [ 20%]
src/tests/test_stage3_scoring.py::test_bank_industry_kpis_receive_redistributed_weight_not_bonus_weight PASSED   [ 20%]
src/tests/test_stage3_scoring.py::test_sales_volume_replaces_part_of_growth_weight PASSED                        [ 20%]
src/tests/test_stage3_scoring.py::test_industry_percentile_is_primary_when_peer_count_is_at_least_eight PASSED   [ 20%]
src/tests/test_stage3_scoring.py::test_lower_is_better_direction_is_inverted_for_npl PASSED                      [ 20%]
src/tests/test_stage3_scoring.py::test_lower_is_better_maximum_gets_zero PASSED                                  [ 20%]
src/tests/test_stage3_scoring.py::test_historical_benchmark_is_fallback_when_peer_count_is_below_eight PASSED    [ 20%]
src/tests/test_stage3_scoring.py::test_missing_kpi_is_not_zero_and_remaining_axis_weight_is_redistributed PASSED [ 20%]
src/tests/test_stage3_scoring.py::test_axis_below_sixty_percent_is_insufficient_data PASSED                      [ 20%]
src/tests/test_stage3_scoring.py::test_three_axis_formula_and_missing_axis_renormalization PASSED                [ 20%]
src/tests/test_stage3_scoring.py::test_valuation_and_market_inputs_are_not_scoring_inputs PASSED                 [ 21%]
src/tests/test_stage3_scoring.py::test_output_contract_contains_traceability_and_version PASSED                  [ 21%]
src/tests/test_stage3_scoring.py::test_restated_input_remains_scoreable_but_marks_quality_limited PASSED         [ 21%]
src/tests/test_stage3_scoring.py::test_estimated_input_remains_scoreable_but_marks_quality_limited PASSED        [ 21%]
src/tests/test_stage3_scoring.py::test_suspicious_input_produces_no_kpi_score PASSED                             [ 21%]
src/tests/test_stage3_scoring.py::test_identical_inputs_produce_identical_scoring_output PASSED                  [ 21%]
src/tests/test_stage4_trend.py::test_seasonal_baseline_uses_median_of_same_period PASSED                         [ 21%]
src/tests/test_stage4_trend.py::test_seasonal_baseline_median_robust_to_outlier PASSED                           [ 21%]
src/tests/test_stage4_trend.py::test_seasonal_baseline_orders_unsorted_input PASSED                              [ 21%]
src/tests/test_stage4_trend.py::test_seasonal_surprise_uses_median_baseline PASSED                               [ 21%]
src/tests/test_stage4_trend.py::test_seasonal_surprise_negative_baseline_same_sign PASSED                        [ 21%]
src/tests/test_stage4_trend.py::test_seasonal_surprise_below_baseline_is_negative PASSED                         [ 22%]
src/tests/test_stage4_trend.py::test_seasonal_baseline_zero_median_is_null_with_zero_base_flag PASSED            [ 22%]
src/tests/test_stage4_trend.py::test_seasonal_baseline_sign_incompatible_emits_sign_change PASSED                [ 22%]
src/tests/test_stage4_trend.py::test_seasonal_baseline_ignores_missing_observations PASSED                       [ 22%]
src/tests/test_stage4_trend.py::test_seasonal_baseline_deterministic_across_runs PASSED                          [ 22%]
src/tests/test_stage4_trend.py::test_seasonal_engine_reconstructs_baseline_from_series PASSED                    [ 22%]
src/tests/test_stage4_trend.py::test_seasonal_insufficient_when_fewer_than_three_observations PASSED             [ 22%]
src/tests/test_stage4_trend.py::test_seasonal_engine_reports_insufficient_data PASSED                            [ 22%]
src/tests/test_stage4_trend.py::test_seasonal_engine_full_when_three_or_more_observations PASSED                 [ 22%]
src/tests/test_stage4_trend.py::test_seasonal_zero_base_baseline_is_null_with_flag PASSED                        [ 22%]
src/tests/test_stage4_trend.py::test_mom_via_engine PASSED                                                       [ 22%]
src/tests/test_stage4_trend.py::test_qoq_via_engine PASSED                                                       [ 23%]
src/tests/test_stage4_trend.py::test_yoy_via_engine PASSED                                                       [ 23%]
src/tests/test_stage4_trend.py::test_mom_missing_observations_stay_null PASSED                                   [ 23%]
src/tests/test_stage4_trend.py::test_same_period_multi_year_reports_each_year PASSED                             [ 23%]
src/tests/test_stage4_trend.py::test_same_period_multi_year_via_engine PASSED                                    [ 23%]
src/tests/test_stage4_trend.py::test_same_period_multi_year_zero_base_flagged PASSED                             [ 23%]
src/tests/test_stage4_trend.py::test_period_comparison_quarterly_series_yoy PASSED                               [ 23%]
src/tests/test_stage4_trend.py::test_period_comparison_monthly_series_mom_and_qoq PASSED                         [ 23%]
src/tests/test_stage4_trend.py::test_period_comparison_with_explicit_position PASSED                             [ 23%]
src/tests/test_stage4_trend.py::test_period_comparison_lag_before_series_start_is_none PASSED                    [ 23%]
src/tests/test_stage4_trend.py::test_period_comparison_missing_observation_is_not_zero PASSED                    [ 23%]
src/tests/test_stage4_trend.py::test_period_comparison_zero_base_is_not_fabricated PASSED                        [ 24%]
src/tests/test_stage4_trend.py::test_period_comparison_sign_change_is_not_misleading PASSED                      [ 24%]
src/tests/test_stage4_trend.py::test_period_comparison_same_sign_negative_is_a_real_decline PASSED               [ 24%]
src/tests/test_stage4_trend.py::test_engine_derives_yoy_from_quarterly_flow_series PASSED                        [ 24%]
src/tests/test_stage4_trend.py::test_engine_derives_mom_from_monthly_series PASSED                               [ 24%]
src/tests/test_stage4_trend.py::test_engine_explicit_pair_wins_over_series_derivation PASSED                     [ 24%]
src/tests/test_stage4_trend.py::test_engine_historical_sufficiency_states PASSED                                 [ 24%]
src/tests/test_stage4_trend.py::test_engine_historical_sufficiency_reports_missing_as_insufficient PASSED        [ 24%]
src/tests/test_stage4_trend.py::test_multi_year_trend_between_earliest_and_latest_annual PASSED                  [ 24%]
src/tests/test_stage4_trend.py::test_multi_year_trend_requires_two_annual_observations PASSED                    [ 24%]
src/tests/test_stage4_trend.py::test_multi_year_trend_via_engine PASSED                                          [ 24%]
src/tests/test_stage4_trend.py::test_zero_base_handling PASSED                                                   [ 25%]
src/tests/test_stage4_trend.py::test_engine_emits_zero_base_context PASSED                                       [ 25%]
src/tests/test_stage4_trend.py::test_sign_change_handling PASSED                                                 [ 25%]
src/tests/test_stage4_trend.py::test_engine_emits_loss_to_profit_and_profit_to_loss PASSED                       [ 25%]
src/tests/test_stage4_trend.py::test_same_sign_negative_growth_is_a_real_decline PASSED                          [ 25%]
src/tests/test_stage4_trend.py::test_relative_strength_requires_eight_observations PASSED                        [ 25%]
src/tests/test_stage4_trend.py::test_relative_strength_bands PASSED                                              [ 25%]
src/tests/test_stage4_trend.py::test_relative_strength_is_company_relative_not_global PASSED                     [ 25%]
src/tests/test_stage4_trend.py::test_engine_exposes_per_horizon_relative_strength PASSED                         [ 25%]
src/tests/test_stage4_trend.py::test_relative_strength_not_formal_below_eight_history_observations PASSED        [ 25%]
src/tests/test_stage4_trend.py::test_momentum_history_excludes_final_observation_stock PASSED                    [ 25%]
src/tests/test_stage4_trend.py::test_momentum_history_excludes_final_observation_flow PASSED                     [ 26%]
src/tests/test_stage4_trend.py::test_minimum_eight_counts_historical_observations_only PASSED                    [ 26%]
src/tests/test_stage4_trend.py::test_seven_historical_observations_stay_insufficient PASSED                      [ 26%]
src/tests/test_stage4_trend.py::test_current_observation_cannot_be_counted_as_the_eighth PASSED                  [ 26%]
src/tests/test_stage4_trend.py::test_eight_genuine_historical_observations_give_valid_strength PASSED            [ 26%]
src/tests/test_stage4_trend.py::test_current_observation_cannot_shift_own_percentile PASSED                      [ 26%]
src/tests/test_stage4_trend.py::test_engine_relative_strength_unchanged_for_valid_history PASSED                 [ 26%]
src/tests/test_stage4_trend.py::test_engine_derived_history_excludes_current_observation PASSED                  [ 26%]
src/tests/test_stage4_trend.py::test_classify_direction_uses_threshold_only_for_direction PASSED                 [ 26%]
src/tests/test_stage4_trend.py::test_engine_exposes_per_horizon_direction PASSED                                 [ 26%]
src/tests/test_stage4_trend.py::test_missing_horizon_reports_missing_direction PASSED                            [ 26%]
src/tests/test_stage4_trend.py::test_trend_state_strong_improvement_requires_two_strong_and_all_positive PASSED  [ 27%]
src/tests/test_stage4_trend.py::test_trend_state_strong_without_strength_is_improving PASSED                     [ 27%]
src/tests/test_stage4_trend.py::test_trend_state_stable_when_all_weak PASSED                                     [ 27%]
src/tests/test_stage4_trend.py::test_trend_state_stable_when_no_majority_direction PASSED                        [ 27%]
src/tests/test_stage4_trend.py::test_trend_state_deteriorating_and_strong_deterioration PASSED                   [ 27%]
src/tests/test_stage4_trend.py::test_trend_state_mixed_is_improving_not_strong PASSED                            [ 27%]
src/tests/test_stage4_trend.py::test_one_valid_horizon_is_insufficient PASSED                                    [ 27%]
src/tests/test_stage4_trend.py::test_two_valid_horizons_allowed_but_limited PASSED                               [ 27%]
src/tests/test_stage4_trend.py::test_three_horizons_complete PASSED                                              [ 27%]
src/tests/test_stage4_trend.py::test_two_horizon_engine_run_reports_limited PASSED                               [ 27%]
src/tests/test_stage4_trend.py::test_one_horizon_engine_run_reports_insufficient PASSED                          [ 27%]
src/tests/test_stage4_trend.py::test_low_base_requires_three_history_values_and_uses_robust_z PASSED             [ 28%]
src/tests/test_stage4_trend.py::test_low_base_unknown_below_three_observations_is_not_false PASSED               [ 28%]
src/tests/test_stage4_trend.py::test_low_base_preserves_growth_without_scoring_it PASSED                         [ 28%]
src/tests/test_stage4_trend.py::test_low_base_false_when_base_is_normal PASSED                                   [ 28%]
src/tests/test_stage4_trend.py::test_engine_low_base_unknown_without_history PASSED                              [ 28%]
src/tests/test_stage4_trend.py::test_engine_is_deterministic PASSED                                              [ 28%]
src/tests/test_stage4_trend.py::test_engine_has_no_randomness_or_clock_dependency PASSED                         [ 28%]
src/tests/test_stage4_trend.py::test_utils_are_deterministic_across_input_ordering PASSED                        [ 28%]
src/tests/test_stage4_trend.py::test_output_contract_full_run PASSED                                             [ 28%]
src/tests/test_stage4_trend.py::test_output_contract_sufficiency_states_are_not_collapsed PASSED                 [ 28%]
src/tests/test_stage4_trend.py::test_output_contract_zero_base_and_sign_change_contexts PASSED                   [ 28%]
src/tests/test_stage4_trend.py::test_one_off_detection_is_conservative PASSED                                    [ 29%]
src/tests/test_stage4_trend.py::test_flow_momentum_sums_windows PASSED                                           [ 29%]
src/tests/test_stage4_trend.py::test_stock_momentum_never_sums PASSED                                            [ 29%]
src/tests/test_stage4_trend.py::test_flow_and_stock_12m_differ PASSED                                            [ 29%]
src/tests/test_stage4_trend.py::test_trend_12m_is_current_ttm_vs_ttm_twelve_months_earlier PASSED                [ 29%]
src/tests/test_stage4_trend.py::test_engine_flow_series_end_to_end PASSED                                        [ 29%]
src/tests/test_stage4_trend.py::test_engine_stock_series_end_to_end PASSED                                       [ 29%]
src/tests/test_stage4_trend.py::test_stock_12m_uses_period_end_ratio_semantics PASSED                            [ 29%]
src/tests/test_stage4_trend.py::test_flow_12m_retains_ttm_window_semantics PASSED                                [ 29%]
src/tests/test_stage4_trend.py::test_engine_12m_horizon_splits_by_variable_class PASSED                          [ 29%]
src/tests/test_stage4_trend.py::test_stock_12m_preserves_missing_zero_and_sign_change_protections PASSED         [ 29%]
src/tests/test_stage4_trend.py::test_missing_observation_never_becomes_zero PASSED                               [ 30%]
src/tests/test_stage4_trend.py::test_scenario_1_strong_growth PASSED                                             [ 30%]
src/tests/test_stage4_trend.py::test_scenario_2_moderate_improvement PASSED                                      [ 30%]
src/tests/test_stage4_trend.py::test_scenario_3_stable PASSED                                                    [ 30%]
src/tests/test_stage4_trend.py::test_scenario_4_gradual_deterioration PASSED                                     [ 30%]
src/tests/test_stage4_trend.py::test_scenario_5_severe_deterioration PASSED                                      [ 30%]
src/tests/test_stage4_trend.py::test_scenario_6_mixed PASSED                                                     [ 30%]
src/tests/test_stage4_trend.py::test_scenario_7_two_valid_horizons PASSED                                        [ 30%]
src/tests/test_stage4_trend.py::test_scenario_8_one_valid_horizon_insufficient PASSED                            [ 30%]
src/tests/test_stage5_forecast.py::test_forecast_driver_general_chain PASSED                                     [ 30%]
src/tests/test_stage5_forecast.py::test_stage5_uses_seasonal_baseline_and_parameterized_trend PASSED             [ 30%]
src/tests/test_stage5_forecast.py::test_low_base_disables_trend_adjustment PASSED                                [ 30%]
src/tests/test_stage5_forecast.py::test_component_based_net_profit_has_priority_and_roe PASSED                   [ 31%]
src/tests/test_stage5_forecast.py::test_missing_core_data_falls_back_to_insufficient_data PASSED                 [ 31%]
src/tests/test_stage5_forecast.py::test_bank_specialized_core_does_not_use_general_revenue_model PASSED          [ 31%]
src/tests/test_stage5_forecast.py::test_holding_core_excludes_p_nav PASSED                                       [ 31%]
src/tests/test_stage5_forecast.py::test_unsupported_horizon_and_industry_are_rejected PASSED                     [ 31%]
src/tests/test_stage5_forecast.py::test_record_schema_carries_all_contract_fields PASSED                         [ 31%]
src/tests/test_stage5_forecast.py::test_records_freeze_all_three_scenarios PASSED                                [ 31%]
src/tests/test_stage5_forecast.py::test_horizon_and_timestamp_are_recorded_per_forecast PASSED                   [ 31%]
src/tests/test_stage5_forecast.py::test_missing_metric_is_none_not_zero PASSED                                   [ 31%]
src/tests/test_stage5_forecast.py::test_naive_cutoff_datetime_is_assumed_utc PASSED                              [ 31%]
src/tests/test_stage5_forecast.py::test_calculation_timestamp_before_cutoff_is_rejected PASSED                   [ 31%]
src/tests/test_stage5_forecast.py::test_input_refs_are_recorded_for_auditability PASSED                          [ 32%]
src/tests/test_stage5_forecast.py::test_input_refs_accept_mapping_form PASSED                                    [ 32%]
src/tests/test_stage5_forecast.py::test_input_ref_without_publication_date_is_never_rejected PASSED              [ 32%]
src/tests/test_stage5_forecast.py::test_malformed_input_ref_is_rejected PASSED                                   [ 32%]
src/tests/test_stage5_forecast.py::test_version_store_appends_and_never_overwrites PASSED                        [ 32%]
src/tests/test_stage5_forecast.py::test_revised_forecast_keeps_the_older_version PASSED                          [ 32%]
src/tests/test_stage5_forecast.py::test_identical_resave_is_idempotent PASSED                                    [ 32%]
src/tests/test_stage5_forecast.py::test_identical_resave_with_a_different_surrogate_id_is_idempotent PASSED      [ 32%]
src/tests/test_stage5_forecast.py::test_explicit_version_collision_is_rejected PASSED                            [ 32%]
src/tests/test_stage5_forecast.py::test_revision_trend_reports_direction PASSED                                  [ 32%]
src/tests/test_stage5_forecast.py::test_scenarios_are_separate_series PASSED                                     [ 32%]
src/tests/test_stage5_forecast.py::test_filter_pit_inputs_drops_future_information PASSED                        [ 33%]
src/tests/test_stage5_forecast.py::test_future_input_is_flagged_not_silently_used PASSED                         [ 33%]
src/tests/test_stage5_forecast.py::test_read_at_cutoff_hides_forecasts_built_on_later_data PASSED                [ 33%]
src/tests/test_stage5_forecast.py::test_read_at_cutoff_returns_none_when_nothing_available PASSED                [ 33%]
src/tests/test_stage5_forecast.py::test_pit_violations_are_detectable_across_the_store PASSED                    [ 33%]
src/tests/test_stage5_forecast.py::test_cutoff_timezone_normalization_is_consistent PASSED                       [ 33%]
src/tests/test_stage5_forecast.py::test_normalize_datetime_contracts PASSED                                      [ 33%]
src/tests/test_stage5_forecast.py::test_stage4_adapter_maps_core_fields_without_recalculating PASSED             [ 33%]
src/tests/test_stage5_forecast.py::test_stage4_adapter_output_drives_the_engine PASSED                           [ 33%]
src/tests/test_stage5_forecast.py::test_seasonal_baseline_requires_stage4_sufficiency PASSED                     [ 33%]
src/tests/test_stage5_forecast.py::test_seasonal_baseline_surprise_is_not_converted_to_growth PASSED             [ 33%]
src/tests/test_stage5_forecast.py::test_run_rate_is_carried_verbatim PASSED                                      [ 34%]
src/tests/test_stage5_forecast.py::test_low_base_propagates_and_disables_trend_adjustment PASSED                 [ 34%]
src/tests/test_stage5_forecast.py::test_sign_change_propagates_from_stage4_context PASSED                        [ 34%]
src/tests/test_stage5_forecast.py::test_sign_change_propagates_from_layer_flags_without_context PASSED           [ 34%]
src/tests/test_stage5_forecast.py::test_adapter_does_not_recompute_stage4_quantities PASSED                      [ 34%]
src/tests/test_stage5_forecast.py::test_weighted_shares_unchanged_single_observation PASSED                      [ 34%]
src/tests/test_stage5_forecast.py::test_weighted_shares_unchanged_across_observation_history PASSED              [ 34%]
src/tests/test_stage5_forecast.py::test_weighted_shares_capital_increase_extends_series PASSED                   [ 34%]
src/tests/test_stage5_forecast.py::test_weighted_shares_stock_split_uses_ratio_when_counts_absent PASSED         [ 34%]
src/tests/test_stage5_forecast.py::test_weighted_shares_capital_decrease_uses_new_count PASSED                   [ 34%]
src/tests/test_stage5_forecast.py::test_action_after_cutoff_does_not_affect_the_forecast PASSED                  [ 34%]
src/tests/test_stage5_forecast.py::test_action_effective_before_cutoff_but_announced_after_is_ignored PASSED     [ 35%]
src/tests/test_stage5_forecast.py::test_share_history_after_cutoff_is_invisible PASSED                           [ 35%]
src/tests/test_stage5_forecast.py::test_weighted_shares_missing_history_is_none_not_invented PASSED              [ 35%]
src/tests/test_stage5_forecast.py::test_weighted_shares_no_observation_at_cutoff_is_none PASSED                  [ 35%]
src/tests/test_stage5_forecast.py::test_weighted_shares_unresolvable_action_is_reported_not_guessed PASSED       [ 35%]
src/tests/test_stage5_forecast.py::test_engine_accepts_builder_output_for_eps PASSED                             [ 35%]
src/tests/test_stage5_forecast.py::test_weighted_shares_are_deterministic_across_calls PASSED                    [ 35%]
src/tests/test_stage5_forecast.py::test_stage4_adapter_is_deterministic PASSED                                   [ 35%]
src/tests/test_stage5_forecast.py::test_repo_first_forecast_persists PASSED                                      [ 35%]
src/tests/test_stage5_forecast.py::test_repo_second_save_creates_a_new_version PASSED                            [ 35%]
src/tests/test_stage5_forecast.py::test_repo_old_version_remains_readable PASSED                                 [ 35%]
src/tests/test_stage5_forecast.py::test_repo_does_not_overwrite_the_previous_forecast PASSED                     [ 36%]
src/tests/test_stage5_forecast.py::test_repo_identical_resave_is_idempotent PASSED                               [ 36%]
src/tests/test_stage5_forecast.py::test_repo_identical_resave_with_a_different_surrogate_id_is_idempotent PASSED [ 36%]
src/tests/test_stage5_forecast.py::test_repo_conflicting_version_is_rejected PASSED                              [ 36%]
src/tests/test_stage5_forecast.py::test_repo_same_version_with_different_content_still_conflicts PASSED          [ 36%]
src/tests/test_stage5_forecast.py::test_repo_scenarios_are_separate_series PASSED                                [ 36%]
src/tests/test_stage5_forecast.py::test_repo_horizons_are_separate_series PASSED                                 [ 36%]
src/tests/test_stage5_forecast.py::test_repo_preserves_pit_fields PASSED                                         [ 36%]
src/tests/test_stage5_forecast.py::test_repo_preserves_input_provenance PASSED                                   [ 36%]
src/tests/test_stage5_forecast.py::test_repo_revision_trend_built_from_stored_versions PASSED                    [ 36%]
src/tests/test_stage5_forecast.py::test_repo_revision_trend_mixed_is_reported PASSED                             [ 36%]
src/tests/test_stage5_forecast.py::test_repo_read_at_cutoff_hides_forecasts_built_on_later_data PASSED           [ 37%]
src/tests/test_stage5_forecast.py::test_stage1_derived_context_uses_authoritative_latest_and_nearest_prior_facts PASSED [ 37%]
src/tests/test_stage5_forecast.py::test_stage1_derived_context_does_not_fabricate_prior_observations PASSED      [ 37%]
src/tests/test_stage5_forecast.py::test_unverified_net_profit_does_not_produce_eps PASSED                        [ 37%]
src/tests/test_stage5_forecast.py::test_production_path_builds_forecast_from_stage1_facts PASSED                 [ 37%]
src/tests/test_stage5_forecast.py::test_production_path_uses_stage4_without_recalculation PASSED                 [ 37%]
src/tests/test_stage5_forecast.py::test_production_path_weights_real_share_history PASSED                        [ 37%]
src/tests/test_stage5_forecast.py::test_production_path_produces_forecast_records PASSED                         [ 37%]
src/tests/test_stage5_forecast.py::test_production_path_persists_all_scenarios PASSED                            [ 37%]
src/tests/test_stage5_forecast.py::test_production_path_reads_forecast_back PASSED                               [ 37%]
src/tests/test_stage5_forecast.py::test_production_path_preserves_pit_metadata PASSED                            [ 37%]
src/tests/test_stage5_forecast.py::test_production_path_duplicate_save_is_idempotent PASSED                      [ 38%]
src/tests/test_stage5_forecast.py::test_production_path_missing_share_history_keeps_eps_none PASSED              [ 38%]
src/tests/test_stage5_forecast.py::test_production_path_is_deterministic PASSED                                  [ 38%]
src/tests/test_stage5_forecast.py::test_seasonal_baseline_outranks_the_run_rate PASSED                           [ 38%]
src/tests/test_stage5_forecast.py::test_recent_run_rate_is_the_fallback_baseline PASSED                          [ 38%]
src/tests/test_stage5_forecast.py::test_driver_based_baseline_is_the_third_tier PASSED                           [ 38%]
src/tests/test_stage5_forecast.py::test_explicit_driver_based_level_beats_the_volume_price_split PASSED          [ 38%]
src/tests/test_stage5_forecast.py::test_non_positive_driver_level_is_refused_not_treated_as_zero PASSED          [ 38%]
src/tests/test_stage5_forecast.py::test_insufficient_baseline_reports_missing_rather_than_zero PASSED            [ 38%]
src/tests/test_stage5_forecast.py::test_revenue_growth_applies_to_the_baseline PASSED                            [ 38%]
src/tests/test_stage5_forecast.py::test_missing_revenue_growth_defaults_to_flat_not_invented PASSED              [ 38%]
src/tests/test_stage5_forecast.py::test_operating_margin_method_is_recorded_separately PASSED                    [ 39%]
src/tests/test_stage5_forecast.py::test_revenue_can_rise_while_margin_falls PASSED                               [ 39%]
src/tests/test_stage5_forecast.py::test_revenue_can_fall_while_margin_rises PASSED                               [ 39%]
src/tests/test_stage5_forecast.py::test_revenue_can_rise_while_operating_profit_decreases PASSED                 [ 39%]
src/tests/test_stage5_forecast.py::test_changing_revenue_growth_does_not_move_the_margin PASSED                  [ 39%]
src/tests/test_stage5_forecast.py::test_forecast_margin_outranks_the_historical_margin PASSED                    [ 39%]
src/tests/test_stage5_forecast.py::test_missing_operating_margin_halts_the_chain PASSED                          [ 39%]
src/tests/test_stage5_forecast.py::test_operating_profit_is_revenue_times_margin PASSED                          [ 39%]
src/tests/test_stage5_forecast.py::test_full_chain_is_resolved_in_order PASSED                                   [ 39%]
src/tests/test_stage5_forecast.py::test_component_based_net_profit_wins_through_the_engine PASSED                [ 39%]
src/tests/test_stage5_forecast.py::test_partial_components_do_not_get_fabricated PASSED                          [ 39%]
src/tests/test_stage5_forecast.py::test_historical_conversion_falls_back_from_components PASSED                  [ 40%]
src/tests/test_stage5_forecast.py::test_net_margin_is_the_third_tier PASSED                                      [ 40%]
src/tests/test_stage5_forecast.py::test_missing_net_profit_evidence_leaves_net_profit_unknown PASSED             [ 40%]
src/tests/test_stage5_forecast.py::test_missing_share_count_leaves_eps_none_not_zero PASSED                      [ 40%]
src/tests/test_stage5_forecast.py::test_all_non_financial_industries_share_one_core[CEMENT] PASSED               [ 40%]
src/tests/test_stage5_forecast.py::test_all_non_financial_industries_share_one_core[CHEMICAL] PASSED             [ 40%]
src/tests/test_stage5_forecast.py::test_all_non_financial_industries_share_one_core[FOOD] PASSED                 [ 40%]
src/tests/test_stage5_forecast.py::test_all_non_financial_industries_share_one_core[METALS] PASSED               [ 40%]
src/tests/test_stage5_forecast.py::test_all_non_financial_industries_share_one_core[MINING] PASSED               [ 40%]
src/tests/test_stage5_forecast.py::test_all_non_financial_industries_share_one_core[PETROCHEMICAL] PASSED        [ 40%]
src/tests/test_stage5_forecast.py::test_all_non_financial_industries_share_one_core[PHARMACEUTICAL] PASSED       [ 40%]
src/tests/test_stage5_forecast.py::test_every_industry_reports_insufficient_data_identically[CEMENT] PASSED      [ 40%]
src/tests/test_stage5_forecast.py::test_every_industry_reports_insufficient_data_identically[CHEMICAL] PASSED    [ 41%]
src/tests/test_stage5_forecast.py::test_every_industry_reports_insufficient_data_identically[FOOD] PASSED        [ 41%]
src/tests/test_stage5_forecast.py::test_every_industry_reports_insufficient_data_identically[METALS] PASSED      [ 41%]
src/tests/test_stage5_forecast.py::test_every_industry_reports_insufficient_data_identically[MINING] PASSED      [ 41%]
src/tests/test_stage5_forecast.py::test_every_industry_reports_insufficient_data_identically[PETROCHEMICAL] PASSED [ 41%]
src/tests/test_stage5_forecast.py::test_every_industry_reports_insufficient_data_identically[PHARMACEUTICAL] PASSED [ 41%]
src/tests/test_stage5_forecast.py::test_repeated_execution_is_deterministic PASSED                               [ 41%]
src/tests/test_stage5_forecast.py::test_eps_with_unchanged_shares_is_net_profit_over_the_base PASSED             [ 41%]
src/tests/test_stage5_forecast.py::test_unchanged_shares_across_a_multi_observation_history PASSED               [ 41%]
src/tests/test_stage5_forecast.py::test_eps_with_capital_increase_uses_the_weighted_average PASSED               [ 41%]
src/tests/test_stage5_forecast.py::test_eps_with_capital_increase_from_a_lower_base_is_still_weighted PASSED     [ 41%]
src/tests/test_stage5_forecast.py::test_eps_with_a_stock_split_doubles_the_share_base[STOCK_SPLIT] PASSED        [ 42%]
src/tests/test_stage5_forecast.py::test_eps_with_a_stock_split_doubles_the_share_base[SPLIT] PASSED              [ 42%]
src/tests/test_stage5_forecast.py::test_eps_with_a_reverse_split_halves_the_share_base[REVERSE_SPLIT] PASSED     [ 42%]
src/tests/test_stage5_forecast.py::test_eps_with_a_reverse_split_halves_the_share_base[SHARE_CONSOLIDATION] PASSED [ 42%]
src/tests/test_stage5_forecast.py::test_eps_with_a_consolidation_declared_as_counts PASSED                       [ 42%]
src/tests/test_stage5_forecast.py::test_an_action_after_the_cutoff_leaves_eps_at_the_observed_base PASSED        [ 42%]
src/tests/test_stage5_forecast.py::test_an_action_announced_after_the_cutoff_leaves_eps_undiluted PASSED         [ 42%]
src/tests/test_stage5_forecast.py::test_a_late_announced_action_is_reported_not_silently_dropped PASSED          [ 42%]
src/tests/test_stage5_forecast.py::test_missing_share_history_leaves_eps_none_not_zero PASSED                    [ 42%]
src/tests/test_stage5_forecast.py::test_no_observation_at_the_cutoff_leaves_eps_none PASSED                      [ 42%]
src/tests/test_stage5_forecast.py::test_eps_is_never_zero_as_a_substitute_for_a_missing_share_base PASSED        [ 42%]
src/tests/test_stage5_forecast.py::test_eps_tracks_net_profit_in_the_base_scenario PASSED                        [ 43%]
src/tests/test_stage5_forecast.py::test_eps_moves_with_the_share_base_and_not_with_net_profit PASSED             [ 43%]
src/tests/test_stage5_forecast.py::test_roe_is_net_profit_over_average_equity PASSED                             [ 43%]
src/tests/test_stage5_forecast.py::test_roe_uses_both_ends_not_the_closing_balance_alone PASSED                  [ 43%]
src/tests/test_stage5_forecast.py::test_average_equity_of_zero_is_not_a_divisor PASSED                           [ 43%]
src/tests/test_stage5_forecast.py::test_missing_both_equity_balances_leaves_roe_none PASSED                      [ 43%]
src/tests/test_stage5_forecast.py::test_one_missing_equity_end_leaves_roe_none[beginning_equity] PASSED          [ 43%]
src/tests/test_stage5_forecast.py::test_one_missing_equity_end_leaves_roe_none[forecast_ending_equity] PASSED    [ 43%]
src/tests/test_stage5_forecast.py::test_no_equity_and_no_shares_leaves_eps_and_roe_none PASSED                   [ 43%]
src/tests/test_stage5_forecast.py::test_roe_tracks_net_profit_in_the_base_scenario PASSED                        [ 43%]
src/tests/test_stage5_forecast.py::test_roe_is_unaffected_by_the_share_base PASSED                               [ 43%]
src/tests/test_stage5_forecast.py::test_eps_and_roe_are_deterministic_across_calls PASSED                        [ 44%]
src/tests/test_stage5_forecast.py::test_deterministic_across_reordered_share_history PASSED                      [ 44%]
src/tests/test_stage5_forecast.py::test_bank_chain_runs_on_nii_not_the_revenue_model PASSED                      [ 44%]
src/tests/test_stage5_forecast.py::test_bank_scenarios_fail_closed_without_a_financial_spread PASSED             [ 44%]
src/tests/test_stage5_forecast.py::test_bank_missing_nii_driver_stays_missing_not_zero PASSED                    [ 44%]
src/tests/test_stage5_forecast.py::test_bank_missing_net_profit_conversion_keeps_nii_visible PASSED              [ 44%]
src/tests/test_stage5_forecast.py::test_bank_eps_is_net_profit_over_shares PASSED                                [ 44%]
src/tests/test_stage5_forecast.py::test_bank_roe_is_net_profit_over_average_equity PASSED                        [ 44%]
src/tests/test_stage5_forecast.py::test_bank_missing_equity_leaves_roe_none_but_keeps_eps PASSED                 [ 44%]
src/tests/test_stage5_forecast.py::test_npl_is_recorded_as_context_and_never_a_profit_factor PASSED              [ 44%]
src/tests/test_stage5_forecast.py::test_missing_npl_leaves_the_bank_chain_unchanged PASSED                       [ 44%]
src/tests/test_stage5_forecast.py::test_nim_and_loan_drivers_are_carried_as_context_only PASSED                  [ 45%]
src/tests/test_stage5_forecast.py::test_bank_component_based_net_profit_outranks_the_conversion PASSED           [ 45%]
src/tests/test_stage5_forecast.py::test_npl_context_survives_into_the_stored_record PASSED                       [ 45%]
src/tests/test_stage5_forecast.py::test_holding_chain_runs_on_nav_not_the_revenue_model PASSED                   [ 45%]
src/tests/test_stage5_forecast.py::test_holding_nav_growth_drives_net_profit PASSED                              [ 45%]
src/tests/test_stage5_forecast.py::test_holding_scenarios_fail_closed_without_a_financial_spread PASSED          [ 45%]
src/tests/test_stage5_forecast.py::test_holding_eps_is_net_profit_over_shares PASSED                             [ 45%]
src/tests/test_stage5_forecast.py::test_holding_roe_is_net_profit_over_average_equity PASSED                     [ 45%]
src/tests/test_stage5_forecast.py::test_holding_missing_equity_leaves_roe_none_but_keeps_eps PASSED              [ 45%]
src/tests/test_stage5_forecast.py::test_holding_missing_nav_and_conversion_stay_missing PASSED                   [ 45%]
src/tests/test_stage5_forecast.py::test_holding_component_net_profit_outranks_nav_conversion PASSED              [ 45%]
src/tests/test_stage5_forecast.py::test_holding_excludes_p_nav_from_the_forecast_chain PASSED                    [ 46%]
src/tests/test_stage5_forecast.py::test_holding_ignores_a_declared_p_nav_completely PASSED                       [ 46%]
src/tests/test_stage5_forecast.py::test_holding_p_nav_exclusion_is_recorded_on_the_stored_record PASSED          [ 46%]
src/tests/test_stage5_forecast.py::test_operational_fx_reprices_the_exposed_revenue_share PASSED                 [ 46%]
src/tests/test_stage5_forecast.py::test_operational_fx_provenance_is_recorded PASSED                             [ 46%]
src/tests/test_stage5_forecast.py::test_operational_fx_object_is_accepted_directly PASSED                        [ 46%]
src/tests/test_stage5_forecast.py::test_fx_without_declared_exposure_leaves_revenue_untouched PASSED             [ 46%]
src/tests/test_stage5_forecast.py::test_fx_without_declared_sensitivity_leaves_revenue_untouched PASSED          [ 46%]
src/tests/test_stage5_forecast.py::test_fx_applies_identically_across_the_base_scenario PASSED                   [ 46%]
src/tests/test_stage5_forecast.py::test_missing_operational_fx_is_none_and_never_zero PASSED                     [ 46%]
src/tests/test_stage5_forecast.py::test_missing_operational_fx_still_produces_a_full_chain PASSED                [ 46%]
src/tests/test_stage5_forecast.py::test_missing_operational_fx_reports_an_empty_ladder PASSED                    [ 47%]
src/tests/test_stage5_forecast.py::test_free_market_fx_alone_does_not_resolve_operational_fx PASSED              [ 47%]
src/tests/test_stage5_forecast.py::test_free_market_fx_is_never_used_as_operational_fx PASSED                    [ 47%]
src/tests/test_stage5_forecast.py::test_free_market_fx_cannot_silently_substitute_for_operational_fx PASSED      [ 47%]
src/tests/test_stage5_forecast.py::test_free_market_rate_without_exposure_is_not_a_substitution PASSED           [ 47%]
src/tests/test_stage5_forecast.py::test_free_market_fx_is_ignored_on_the_bank_chain PASSED                       [ 47%]
src/tests/test_stage5_forecast.py::test_free_market_fx_is_ignored_on_the_holding_chain PASSED                    [ 47%]
src/tests/test_stage5_forecast.py::test_declared_proxy_rate_stands_in_for_missing_operational_fx PASSED          [ 47%]
src/tests/test_stage5_forecast.py::test_proxy_is_marked_estimated_and_named PASSED                               [ 47%]
src/tests/test_stage5_forecast.py::test_proxy_provenance_reaches_the_stored_record PASSED                        [ 47%]
src/tests/test_stage5_forecast.py::test_an_operational_fx_proxy_object_is_carried_verbatim PASSED                [ 47%]
src/tests/test_stage5_forecast.py::test_a_proxy_rate_does_not_allow_the_free_market_rate_in PASSED               [ 48%]
src/tests/test_stage5_forecast.py::test_proxy_ladder_is_reported_in_order PASSED                                 [ 48%]
src/tests/test_stage5_forecast.py::test_reference_rate_is_the_second_proxy_rung PASSED                           [ 48%]
src/tests/test_stage5_forecast.py::test_bank_forecast_is_deterministic_across_calls PASSED                       [ 48%]
src/tests/test_stage5_forecast.py::test_holding_forecast_is_deterministic_across_calls PASSED                    [ 48%]
src/tests/test_stage5_forecast.py::test_operational_fx_effect_is_deterministic_across_calls PASSED               [ 48%]
src/tests/test_stage5_forecast.py::test_bank_and_holding_chains_never_report_a_revenue_baseline PASSED           [ 48%]
src/tests/test_stage5_forecast.py::test_stage4_two_pct_threshold_is_not_a_forecast_growth_rate[Positive-0.02_0] PASSED [ 48%]
src/tests/test_stage5_forecast.py::test_stage4_two_pct_threshold_is_not_a_forecast_growth_rate[Positive--0.02_0] PASSED [ 48%]
src/tests/test_stage5_forecast.py::test_stage4_two_pct_threshold_is_not_a_forecast_growth_rate[Positive-0.02_1] PASSED [ 48%]
src/tests/test_stage5_forecast.py::test_stage4_two_pct_threshold_is_not_a_forecast_growth_rate[Positive--0.02_1] PASSED [ 48%]
src/tests/test_stage5_forecast.py::test_stage4_two_pct_threshold_is_not_a_forecast_growth_rate[Positive-2.0_0] PASSED [ 49%]
src/tests/test_stage5_forecast.py::test_stage4_two_pct_threshold_is_not_a_forecast_growth_rate[Positive--2.0] PASSED [ 49%]
src/tests/test_stage5_forecast.py::test_stage4_two_pct_threshold_is_not_a_forecast_growth_rate[Positive-2.0_1] PASSED [ 49%]
src/tests/test_stage5_forecast.py::test_stage4_two_pct_threshold_is_not_a_forecast_growth_rate[Negative-0.02_0] PASSED [ 49%]
src/tests/test_stage5_forecast.py::test_stage4_two_pct_threshold_is_not_a_forecast_growth_rate[Negative--0.02_0] PASSED [ 49%]
src/tests/test_stage5_forecast.py::test_stage4_two_pct_threshold_is_not_a_forecast_growth_rate[Negative-0.02_1] PASSED [ 49%]
src/tests/test_stage5_forecast.py::test_stage4_two_pct_threshold_is_not_a_forecast_growth_rate[Negative--0.02_1] PASSED [ 49%]
src/tests/test_stage5_forecast.py::test_stage4_two_pct_threshold_is_not_a_forecast_growth_rate[Negative-2.0_0] PASSED [ 49%]
src/tests/test_stage5_forecast.py::test_stage4_two_pct_threshold_is_not_a_forecast_growth_rate[Negative--2.0] PASSED [ 49%]
src/tests/test_stage5_forecast.py::test_stage4_two_pct_threshold_is_not_a_forecast_growth_rate[Negative-2.0_1] PASSED [ 49%]
src/tests/test_stage5_forecast.py::test_stage4_two_pct_threshold_is_not_a_forecast_growth_rate[Weak-0.02_0] PASSED [ 49%]
src/tests/test_stage5_forecast.py::test_stage4_two_pct_threshold_is_not_a_forecast_growth_rate[Weak--0.02_0] PASSED [ 50%]
src/tests/test_stage5_forecast.py::test_stage4_two_pct_threshold_is_not_a_forecast_growth_rate[Weak-0.02_1] PASSED [ 50%]
src/tests/test_stage5_forecast.py::test_stage4_two_pct_threshold_is_not_a_forecast_growth_rate[Weak--0.02_1] PASSED [ 50%]
src/tests/test_stage5_forecast.py::test_stage4_two_pct_threshold_is_not_a_forecast_growth_rate[Weak-2.0_0] PASSED [ 50%]
src/tests/test_stage5_forecast.py::test_stage4_two_pct_threshold_is_not_a_forecast_growth_rate[Weak--2.0] PASSED [ 50%]
src/tests/test_stage5_forecast.py::test_stage4_two_pct_threshold_is_not_a_forecast_growth_rate[Weak-2.0_1] PASSED [ 50%]
src/tests/test_stage5_forecast.py::test_momentum_may_only_act_through_an_explicit_model_parameter PASSED         [ 50%]
src/tests/test_stage5_forecast.py::test_momentum_strength_is_never_a_growth_multiplier PASSED                    [ 50%]
src/tests/test_stage5_forecast.py::test_fundamental_score_is_never_a_forecast_multiplier[0.0] PASSED             [ 50%]
src/tests/test_stage5_forecast.py::test_fundamental_score_is_never_a_forecast_multiplier[25.0] PASSED            [ 50%]
src/tests/test_stage5_forecast.py::test_fundamental_score_is_never_a_forecast_multiplier[50.0] PASSED            [ 50%]
src/tests/test_stage5_forecast.py::test_fundamental_score_is_never_a_forecast_multiplier[75.0] PASSED            [ 50%]
src/tests/test_stage5_forecast.py::test_fundamental_score_is_never_a_forecast_multiplier[100.0] PASSED           [ 51%]
src/tests/test_stage5_forecast.py::test_fundamental_score_is_never_a_forecast_multiplier[-10.0] PASSED           [ 51%]
src/tests/test_stage5_forecast.py::test_fundamental_score_does_not_widen_or_narrow_the_scenario_spread PASSED    [ 51%]
src/tests/test_stage5_forecast.py::test_genuinely_low_base_produces_no_momentum_adjustment PASSED                [ 51%]
src/tests/test_stage5_forecast.py::test_low_base_flag_alone_does_not_invent_a_growth_rate PASSED                 [ 51%]
src/tests/test_stage5_forecast.py::test_normal_growth_from_a_low_base_uses_the_declared_rate PASSED              [ 51%]
src/tests/test_stage5_forecast.py::test_insufficient_evidence_preserves_the_insufficient_data_path PASSED        [ 51%]
src/tests/test_stage5_forecast.py::test_sign_change_never_uses_an_ordinary_percentage_growth[-1000.0-1000.0-LOSS_TO_PROFIT] PASSED [ 51%]
src/tests/test_stage5_forecast.py::test_sign_change_never_uses_an_ordinary_percentage_growth[-1000.0-1000.0-PROFIT_TO_LOSS] PASSED [ 51%]
src/tests/test_stage5_forecast.py::test_sign_change_never_uses_an_ordinary_percentage_growth[-1000.0-1000.0-SIGN_CHANGE] PASSED [ 51%]
src/tests/test_stage5_forecast.py::test_sign_change_never_uses_an_ordinary_percentage_growth[1000.0--1000.0-LOSS_TO_PROFIT] PASSED [ 51%]
src/tests/test_stage5_forecast.py::test_sign_change_never_uses_an_ordinary_percentage_growth[1000.0--1000.0-PROFIT_TO_LOSS] PASSED [ 52%]
src/tests/test_stage5_forecast.py::test_sign_change_never_uses_an_ordinary_percentage_growth[1000.0--1000.0-SIGN_CHANGE] PASSED [ 52%]
src/tests/test_stage5_forecast.py::test_sign_change_never_uses_an_ordinary_percentage_growth[0.0-1000.0-LOSS_TO_PROFIT] PASSED [ 52%]
src/tests/test_stage5_forecast.py::test_sign_change_never_uses_an_ordinary_percentage_growth[0.0-1000.0-PROFIT_TO_LOSS] PASSED [ 52%]
src/tests/test_stage5_forecast.py::test_sign_change_never_uses_an_ordinary_percentage_growth[0.0-1000.0-SIGN_CHANGE] PASSED [ 52%]
src/tests/test_stage5_forecast.py::test_sign_change_never_uses_an_ordinary_percentage_growth[0.0--1000.0-LOSS_TO_PROFIT] PASSED [ 52%]
src/tests/test_stage5_forecast.py::test_sign_change_never_uses_an_ordinary_percentage_growth[0.0--1000.0-PROFIT_TO_LOSS] PASSED [ 52%]
src/tests/test_stage5_forecast.py::test_sign_change_never_uses_an_ordinary_percentage_growth[0.0--1000.0-SIGN_CHANGE] PASSED [ 52%]
src/tests/test_stage5_forecast.py::test_sign_change_never_uses_an_ordinary_percentage_growth[-500.0-0.0-LOSS_TO_PROFIT] PASSED [ 52%]
src/tests/test_stage5_forecast.py::test_sign_change_never_uses_an_ordinary_percentage_growth[-500.0-0.0-PROFIT_TO_LOSS] PASSED [ 52%]
src/tests/test_stage5_forecast.py::test_sign_change_never_uses_an_ordinary_percentage_growth[-500.0-0.0-SIGN_CHANGE] PASSED [ 52%]
src/tests/test_stage5_forecast.py::test_sign_change_never_uses_an_ordinary_percentage_growth[1000.0-0.0-LOSS_TO_PROFIT] PASSED [ 53%]
src/tests/test_stage5_forecast.py::test_sign_change_never_uses_an_ordinary_percentage_growth[1000.0-0.0-PROFIT_TO_LOSS] PASSED [ 53%]
src/tests/test_stage5_forecast.py::test_sign_change_never_uses_an_ordinary_percentage_growth[1000.0-0.0-SIGN_CHANGE] PASSED [ 53%]
src/tests/test_stage5_forecast.py::test_sign_transition_suppresses_a_declared_trend_adjustment PASSED            [ 53%]
src/tests/test_stage5_forecast.py::test_a_declared_growth_parameter_still_applies_across_a_sign_transition PASSED [ 53%]
src/tests/test_stage5_forecast.py::test_zero_base_to_profit_is_flat_not_infinite_growth PASSED                   [ 53%]
src/tests/test_stage5_forecast.py::test_same_sign_arc_reads_an_ordinary_zero_safe_growth_rate PASSED             [ 53%]
src/tests/test_stage5_forecast.py::test_two_negative_periods_read_a_growth_rate_not_a_sign_change PASSED         [ 53%]
src/tests/test_stage5_forecast.py::test_sign_change_propagation_still_names_the_transition PASSED                [ 53%]
src/tests/test_stage5_forecast.py::test_scenarios_disperse_around_the_declared_baseline_growth PASSED            [ 53%]
src/tests/test_stage5_forecast.py::test_missing_uncertainty_evidence_leaves_no_spread PASSED                     [ 53%]
src/tests/test_stage5_forecast.py::test_declared_volatility_only_acts_through_a_declared_sensitivity PASSED      [ 54%]
src/tests/test_stage5_forecast.py::test_an_arbitrary_spread_is_never_invented_from_missing_data PASSED           [ 54%]
src/tests/test_stage5_forecast.py::test_scenario_spreads_are_deterministic_given_identical_inputs PASSED         [ 54%]
src/tests/test_stage5_forecast.py::test_insufficient_uncertainty_evidence_still_yields_a_base_scenario PASSED    [ 54%]
src/tests/test_stage5_forecast.py::test_bank_scenarios_fail_closed_without_financial_dispersion PASSED           [ 54%]
src/tests/test_stage5_forecast.py::test_forecast_is_deterministic_across_identical_inputs PASSED                 [ 54%]
src/tests/test_stage5_forecast.py::test_eps_is_calculated_when_attributable_profit_is_established PASSED         [ 54%]
src/tests/test_stage5_forecast.py::test_eps_is_unavailable_when_attributable_status_is_not_established PASSED    [ 54%]
src/tests/test_stage5_forecast.py::test_eps_is_unavailable_when_attributable_status_is_explicitly_false PASSED   [ 54%]
src/tests/test_stage5_forecast.py::test_declared_attributable_amount_is_used_as_the_numerator PASSED             [ 54%]
src/tests/test_stage5_forecast.py::test_bank_eps_is_unavailable_when_profit_is_not_attributable PASSED           [ 54%]
src/tests/test_stage5_forecast.py::test_holding_eps_is_unavailable_when_profit_is_not_attributable PASSED        [ 55%]
src/tests/test_stage5_forecast.py::test_bank_component_based_path_cannot_bypass_the_eps_gate PASSED              [ 55%]
src/tests/test_stage5_forecast.py::test_holding_component_based_path_cannot_bypass_the_eps_gate PASSED           [ 55%]
src/tests/test_stage5_forecast.py::test_valid_attributable_bank_forecast_still_calculates_eps PASSED             [ 55%]
src/tests/test_stage5_forecast.py::test_valid_attributable_holding_forecast_still_calculates_eps PASSED          [ 55%]
src/tests/test_stage5_forecast.py::test_eps_matches_net_profit_once_attributable PASSED                          [ 55%]
src/tests/test_stage5_forecast.py::test_scenario_spread_authority_is_recorded_per_spread PASSED                  [ 55%]
src/tests/test_stage5_forecast.py::test_authoritative_scenario_parameters_are_never_spreads PASSED               [ 55%]
src/tests/test_stage5_forecast.py::test_no_authoritative_parameter_leaves_any_spread_standing PASSED             [ 55%]
src/tests/test_stage5_forecast.py::test_no_arbitrary_spread_is_fabricated_from_absent_evidence PASSED            [ 55%]
src/tests/test_stage5_forecast.py::test_stage4_two_pct_cannot_become_a_scenario_spread[-0.02] PASSED             [ 55%]
src/tests/test_stage5_forecast.py::test_stage4_two_pct_cannot_become_a_scenario_spread[-0.019] PASSED            [ 56%]
src/tests/test_stage5_forecast.py::test_stage4_two_pct_cannot_become_a_scenario_spread[0.019] PASSED             [ 56%]
src/tests/test_stage5_forecast.py::test_stage4_two_pct_cannot_become_a_scenario_spread[0.02] PASSED              [ 56%]
src/tests/test_stage5_forecast.py::test_stage4_two_pct_cannot_become_a_scenario_spread[0.25] PASSED              [ 56%]
src/tests/test_stage5_forecast.py::test_momentum_cannot_become_a_scenario_spread PASSED                          [ 56%]
src/tests/test_stage5_forecast.py::test_fundamental_score_cannot_become_a_scenario_spread[0.0] PASSED            [ 56%]
src/tests/test_stage5_forecast.py::test_fundamental_score_cannot_become_a_scenario_spread[50.0] PASSED           [ 56%]
src/tests/test_stage5_forecast.py::test_fundamental_score_cannot_become_a_scenario_spread[100.0] PASSED          [ 56%]
src/tests/test_stage5_forecast.py::test_bank_financial_spread_needs_a_metric_specific_series PASSED              [ 56%]
src/tests/test_stage5_forecast.py::test_volatility_evidence_only_acts_through_a_declared_sensitivity PASSED      [ 56%]
src/tests/test_stage5_forecast.py::test_volatility_without_a_declared_sensitivity_changes_nothing PASSED         [ 56%]
src/tests/test_stage5_forecast.py::test_baseline_revenue_growth_is_a_declared_caller_parameter PASSED            [ 57%]
src/tests/test_stage5_forecast.py::test_absent_baseline_growth_falls_back_to_the_historical_arc PASSED           [ 57%]
src/tests/test_stage5_forecast.py::test_pit_valid_prior_revenue_is_used_for_the_growth_rate PASSED               [ 57%]
src/tests/test_stage5_forecast.py::test_post_cutoff_historical_revenue_is_ignored_by_the_growth_rate PASSED      [ 57%]
src/tests/test_stage5_forecast.py::test_baseline_revenue_growth_cannot_override_pit_valid_history_silently PASSED [ 57%]
src/tests/test_stage5_forecast.py::test_sign_transition_refuses_the_historical_arc_without_a_declaration PASSED  [ 57%]
src/tests/test_stage5_forecast.py::test_pit_valid_value_with_valid_provenance_is_usable PASSED                   [ 57%]
src/tests/test_stage5_forecast.py::test_post_cutoff_numeric_value_is_unusable PASSED                             [ 57%]
src/tests/test_stage5_forecast.py::test_post_cutoff_provenance_makes_a_usable_value_unusable PASSED              [ 57%]
src/tests/test_stage5_forecast.py::test_missing_mandatory_provenance_is_reported_not_trusted PASSED              [ 57%]
src/tests/test_stage5_forecast.py::test_declared_provenance_clears_the_undeclared_warning PASSED                 [ 57%]
src/tests/test_stage5_forecast.py::test_an_undeclared_late_value_is_dropped_from_the_calculation PASSED          [ 58%]
src/tests/test_stage5_forecast.py::test_pit_guard_applies_to_the_bank_chain_too PASSED                           [ 58%]
src/tests/test_stage5_forecast.py::test_pit_guard_applies_to_the_holding_chain_too PASSED                        [ 58%]
src/tests/test_stage5_forecast.py::test_trend_direction_fallback_positive_from_momentum_sign PASSED              [ 58%]
src/tests/test_stage5_forecast.py::test_trend_direction_fallback_negative_from_momentum_sign PASSED              [ 58%]
src/tests/test_stage5_forecast.py::test_trend_direction_fallback_zero_is_weak PASSED                             [ 58%]
src/tests/test_stage5_forecast.py::test_trend_direction_insufficient_data_is_none PASSED                         [ 58%]
src/tests/test_stage5_forecast.py::test_trend_direction_missing_pct_is_none PASSED                               [ 58%]
src/tests/test_stage5_forecast.py::test_null_announcement_action_is_treated_as_knowable_in_production_path PASSED [ 58%]
src/tests/test_stage5_forecast.py::test_late_nii_with_a_surviving_component_still_refuses_the_bank_chain PASSED  [ 58%]
src/tests/test_stage5_forecast.py::test_general_chain_wrapper_refuses_eps_when_not_attributable PASSED           [ 58%]
src/tests/test_stage5_forecast.py::test_zero_revenue_leaves_derived_margins_absent_not_zero PASSED               [ 59%]
src/tests/test_stage5_forecast.py::test_missing_profit_numerator_leaves_its_margin_absent_not_zero PASSED        [ 59%]
src/tests/test_stage5_forecast.py::test_production_path_without_attribution_declaration_keeps_eps_none PASSED    [ 59%]
src/tests/test_stage5_forecast.py::test_historical_dispersion_is_sample_std_n_minus_1 PASSED                     [ 59%]
src/tests/test_stage5_forecast.py::test_four_observations_leave_the_spread_unavailable PASSED                    [ 59%]
src/tests/test_stage5_forecast.py::test_five_observations_supply_the_spread PASSED                               [ 59%]
src/tests/test_stage5_forecast.py::test_identical_observations_yield_zero_spread_not_refusal PASSED              [ 59%]
src/tests/test_stage5_forecast.py::test_post_cutoff_series_element_is_excluded_from_dispersion PASSED            [ 59%]
src/tests/test_stage5_forecast.py::test_zero_base_and_sign_change_transitions_are_excluded PASSED                [ 59%]
src/tests/test_stage5_forecast.py::test_each_spread_disperses_only_its_own_series PASSED                         [ 59%]
src/tests/test_stage5_forecast.py::test_revenue_series_never_supplies_a_margin_spread PASSED                     [ 59%]
src/tests/test_stage5_forecast.py::test_margin_series_never_supplies_a_revenue_spread PASSED                     [ 60%]
src/tests/test_stage5_forecast.py::test_retired_constants_are_detected_and_never_applied PASSED                  [ 60%]
src/tests/test_stage5_forecast.py::test_financial_spread_is_never_aliased_to_revenue_growth PASSED               [ 60%]
src/tests/test_stage5_forecast.py::test_short_financial_series_leaves_the_spread_unavailable PASSED              [ 60%]
src/tests/test_stage5_forecast.py::test_metric_specific_financial_series_supplies_the_spread PASSED              [ 60%]
src/tests/test_stage5_forecast.py::test_dispersion_spreads_are_deterministic PASSED                              [ 60%]
src/tests/test_stage5_forecast.py::test_side_scenarios_are_baseline_plus_minus_spread PASSED                     [ 60%]
src/tests/test_stage5_forecast.py::test_production_path_with_single_period_fails_side_scenarios_closed PASSED    [ 60%]
src/tests/test_stage6_artifact_boundary.py::test_production_primary_result_carries_valid_artifact PASSED         [ 60%]
src/tests/test_stage6_artifact_boundary.py::test_production_empty_result_carries_explicit_empty_artifact PASSED  [ 60%]
src/tests/test_stage6_artifact_boundary.py::test_production_sensitivity_result_carries_valid_artifact PASSED     [ 60%]
src/tests/test_stage6_artifact_boundary.py::test_production_mixed_cutoff_fails_closed_with_no_result PASSED      [ 60%]
src/tests/test_stage6_artifact_boundary.py::test_production_mixed_cutoff_returns_no_partial_result PASSED        [ 61%]
src/tests/test_stage6_artifact_boundary.py::test_production_rerun_result_carries_artifact_with_supersedes PASSED [ 61%]
src/tests/test_stage6_artifact_boundary.py::test_production_multi_scenario_result_carries_per_scenario_provenance PASSED [ 61%]
src/tests/test_stage6_artifact_boundary.py::test_legacy_direct_construction_default_is_none_documented PASSED    [ 61%]
src/tests/test_stage6_artifact_identity.py::test_run_ids_distinct_on_identical_inputs PASSED                     [ 61%]
src/tests/test_stage6_artifact_identity.py::test_version_constants_distinct PASSED                               [ 61%]
src/tests/test_stage6_artifact_identity.py::test_artifact_purposes_exact PASSED                                  [ 61%]
src/tests/test_stage6_artifact_identity.py::test_build_artifact_bad_purpose_raises PASSED                        [ 61%]
src/tests/test_stage6_artifact_identity.py::test_build_artifact_malformed_purposes_raise PASSED                  [ 61%]
src/tests/test_stage6_artifact_identity.py::test_direct_constructor_bad_purpose_raises PASSED                    [ 61%]
src/tests/test_stage6_artifact_identity.py::test_supersedes_preserved PASSED                                     [ 61%]
src/tests/test_stage6_artifact_identity.py::test_self_supersede_raises PASSED                                    [ 62%]
src/tests/test_stage6_artifact_identity.py::test_empty_supersedes_raises PASSED                                  [ 62%]
src/tests/test_stage6_artifact_identity.py::test_direct_constructor_self_and_empty_supersede_raise PASSED        [ 62%]
src/tests/test_stage6_artifact_identity.py::test_frozen_immutability PASSED                                      [ 62%]
src/tests/test_stage6_artifact_identity.py::test_equality_by_value PASSED                                        [ 62%]
src/tests/test_stage6_artifact_identity.py::test_series_provenance_defaults_empty PASSED                         [ 62%]
src/tests/test_stage6_artifact_identity.py::test_methodology_version_arrives_as_argument PASSED                  [ 62%]
src/tests/test_stage6_artifact_identity.py::test_scenario_keys_intact_in_provenance PASSED                       [ 62%]
src/tests/test_stage6_artifact_identity.py::test_pipeline_result_carries_artifact PASSED                         [ 62%]
src/tests/test_stage6_artifact_identity.py::test_cutoff_single_populated PASSED                                  [ 62%]
src/tests/test_stage6_artifact_identity.py::test_cutoff_mixed_raises_fail_closed PASSED                          [ 62%]
src/tests/test_stage6_artifact_identity.py::test_cutoff_empty_records_none PASSED                                [ 63%]
src/tests/test_stage6_artifact_identity.py::test_fabricated_default_check_missing_provenance_empty PASSED        [ 63%]
src/tests/test_stage6_artifact_identity.py::test_rerun_distinct_run_ids_same_inputs PASSED                       [ 63%]
src/tests/test_stage6_artifact_identity.py::test_primary_vs_sensitivity_purposes_differ PASSED                   [ 63%]
src/tests/test_stage6_artifact_identity.py::test_rerun_without_supersedes_has_none PASSED                        [ 63%]
src/tests/test_stage6_artifact_identity.py::test_primary_estimated_scores_with_limited_quality PASSED            [ 63%]
src/tests/test_stage6_artifact_identity.py::test_sensitivity_estimated_quarantined_valid_scores PASSED           [ 63%]
src/tests/test_stage6_artifact_identity.py::test_multi_scenario_separate_provenance_entries PASSED               [ 63%]
src/tests/test_stage6_artifact_identity.py::test_report_version_id_and_publication_surfaced PASSED               [ 63%]
src/tests/test_stage6_artifact_identity.py::test_multi_period_series_keeps_distinct_report_versions PASSED       [ 63%]
src/tests/test_stage6_artifact_identity.py::test_rerun_with_supersedes_preserved PASSED                          [ 63%]
src/tests/test_stage6_artifact_identity.py::test_invalid_report_version_yields_empty_provenance PASSED           [ 64%]
src/tests/test_stage6_artifact_identity.py::test_shared_actual_across_scenarios_no_pooling PASSED                [ 64%]
src/tests/test_stage6_artifact_identity.py::test_partial_provenance_valid_plus_pending PASSED                    [ 64%]
src/tests/test_stage6_artifact_identity.py::test_forced_duplicate_run_id_distinguishable_by_purpose PASSED       [ 64%]
src/tests/test_stage6_artifact_identity.py::test_self_referential_supersedes_raises_in_pipeline PASSED           [ 64%]
src/tests/test_stage6_artifact_identity.py::test_sensitivity_exclusion_order_after_ready_and_duplicate PASSED    [ 64%]
src/tests/test_stage6_artifact_identity.py::test_duplicate_beats_sensitivity_exclusion PASSED                    [ 64%]
src/tests/test_stage6_artifact_identity.py::test_aggregate_observations_threads_exclude_estimated PASSED         [ 64%]
src/tests/test_stage6_artifact_identity.py::test_aggregate_default_path_unchanged PASSED                         [ 64%]
src/tests/test_stage6_evaluation.py::test_legacy_score_functions_not_importable PASSED                           [ 64%]
src/tests/test_stage6_evaluation.py::test_legacy_engine_module_removed PASSED                                    [ 64%]
src/tests/test_stage6_evaluation.py::test_legacy_carriers_removed_from_schema PASSED                             [ 65%]
src/tests/test_stage6_evaluation.py::test_package_surface_exports_no_legacy_methodology PASSED                   [ 65%]
src/tests/test_stage6_evaluation.py::test_production_sources_contain_no_legacy_tokens PASSED                     [ 65%]
src/tests/test_stage6_evaluation.py::test_production_path_withholds_after_removal PASSED                         [ 65%]
src/tests/test_stage6_evaluation.py::test_legacy_calibration_minting_unreachable PASSED                          [ 65%]
src/tests/test_stage6_evaluation_foundation.py::test_identity_key_carries_full_mapping_key PASSED                [ 65%]
src/tests/test_stage6_evaluation_foundation.py::test_identity_scenario_isolates_observations PASSED              [ 65%]
src/tests/test_stage6_evaluation_foundation.py::test_identity_differs_by_metric PASSED                           [ 65%]
src/tests/test_stage6_evaluation_foundation.py::test_identity_stable_for_same_series PASSED                      [ 65%]
src/tests/test_stage6_evaluation_foundation.py::test_later_published_actual_binds_ready PASSED                   [ 65%]
src/tests/test_stage6_evaluation_foundation.py::test_historical_actual_also_binds PASSED                         [ 65%]
src/tests/test_stage6_evaluation_foundation.py::test_unbound_observation_waits_for_actual PASSED                 [ 66%]
src/tests/test_stage6_evaluation_foundation.py::test_leaked_input_freezes_observation PASSED                     [ 66%]
src/tests/test_stage6_evaluation_foundation.py::test_later_actual_is_not_leakage PASSED                          [ 66%]
src/tests/test_stage6_evaluation_foundation.py::test_leak_detector_flags_only_post_cutoff_inputs PASSED          [ 66%]
src/tests/test_stage6_evaluation_foundation.py::test_unknown_provenance_is_gap_not_leakage PASSED                [ 66%]
src/tests/test_stage6_evaluation_foundation.py::test_unknown_quality_state_rejected PASSED                       [ 66%]
src/tests/test_stage6_evaluation_foundation.py::test_restated_actual_carried_not_decided PASSED                  [ 66%]
src/tests/test_stage6_evaluation_foundation.py::test_missing_report_version_carried PASSED                       [ 66%]
src/tests/test_stage6_evaluation_foundation.py::test_horizon_isolates_series PASSED                              [ 66%]
src/tests/test_stage6_evaluation_foundation.py::test_model_version_isolates_series PASSED                        [ 66%]
src/tests/test_stage6_evaluation_foundation.py::test_duplicate_keys_share_flag_and_survive PASSED                [ 66%]
src/tests/test_stage6_evaluation_foundation.py::test_unique_observations_unflagged PASSED                        [ 67%]
src/tests/test_stage6_evaluation_foundation.py::test_missing_actual_value_is_none_not_zero PASSED                [ 67%]
src/tests/test_stage6_evaluation_foundation.py::test_zero_actual_preserved_as_zero PASSED                        [ 67%]
src/tests/test_stage6_evaluation_foundation.py::test_missing_forecast_metric_is_none PASSED                      [ 67%]
src/tests/test_stage6_evaluation_foundation.py::test_unknown_metric_code_is_missing_not_zero PASSED              [ 67%]
src/tests/test_stage6_evaluation_foundation.py::test_quality_states_recorded_verbatim[MISSING] PASSED            [ 67%]
src/tests/test_stage6_evaluation_foundation.py::test_quality_states_recorded_verbatim[ESTIMATED] PASSED          [ 67%]
src/tests/test_stage6_evaluation_foundation.py::test_quality_states_recorded_verbatim[SUSPICIOUS] PASSED         [ 67%]
src/tests/test_stage6_evaluation_foundation.py::test_quality_states_recorded_verbatim[UNMAPPED] PASSED           [ 67%]
src/tests/test_stage6_evaluation_foundation.py::test_quality_states_recorded_verbatim[RESTATED] PASSED           [ 67%]
src/tests/test_stage6_evaluation_foundation.py::test_quality_states_recorded_verbatim[VALID] PASSED              [ 67%]
src/tests/test_stage6_evaluation_foundation.py::test_metadata_counts_without_scoring PASSED                      [ 68%]
src/tests/test_stage6_evaluation_metrics.py::test_error_sign_under_and_over_forecast PASSED                      [ 68%]
src/tests/test_stage6_evaluation_metrics.py::test_mape_and_bias_match_spec_formulas PASSED                       [ 68%]
src/tests/test_stage6_evaluation_metrics.py::test_zero_forecast_keeps_absolute_error_drops_percentages PASSED    [ 68%]
src/tests/test_stage6_evaluation_metrics.py::test_sign_change_regimes_quarantined_with_absolute_error PASSED     [ 68%]
src/tests/test_stage6_evaluation_metrics.py::test_zero_actual_excluded_from_mape_with_reason_code PASSED         [ 68%]
src/tests/test_stage6_evaluation_metrics.py::test_zero_actual_negative_forecast_bias_term_is_plus_one PASSED     [ 68%]
src/tests/test_stage6_evaluation_metrics.py::test_each_horizon_evaluated_independently PASSED                    [ 68%]
src/tests/test_stage6_evaluation_metrics.py::test_model_versions_never_combine PASSED                            [ 68%]
src/tests/test_stage6_evaluation_metrics.py::test_duplicate_collision_quarantines_both PASSED                    [ 68%]
src/tests/test_stage6_evaluation_metrics.py::test_duplicate_scenario_distinct_pair_scores_separately PASSED      [ 68%]
src/tests/test_stage6_evaluation_metrics.py::test_pit_leaked_inputs_never_score PASSED                           [ 69%]
src/tests/test_stage6_evaluation_metrics.py::test_later_published_actual_is_the_scored_outcome PASSED            [ 69%]
src/tests/test_stage6_evaluation_metrics.py::test_invalid_actual_states_quarantined_verbatim PASSED              [ 69%]
src/tests/test_stage6_evaluation_metrics.py::test_missing_values_are_none_not_zero PASSED                        [ 69%]
src/tests/test_stage6_evaluation_metrics.py::test_missing_baseline_value_means_missing_baseline_metrics PASSED   [ 69%]
src/tests/test_stage6_evaluation_metrics.py::test_baseline_zero_value_never_fabricates_baseline_ape PASSED       [ 69%]
src/tests/test_stage6_evaluation_metrics.py::test_baseline_comparison_matches_section_17_formula PASSED          [ 69%]
src/tests/test_stage6_evaluation_metrics.py::test_model_worse_than_baseline_reports_negative_improvement PASSED  [ 69%]
src/tests/test_stage6_evaluation_metrics.py::test_baseline_uses_same_scored_set_not_a_wider_one PASSED           [ 69%]
src/tests/test_stage6_evaluation_metrics.py::test_insufficient_history_bands_match_spec_section_14 PASSED        [ 69%]
src/tests/test_stage6_evaluation_metrics.py::test_only_scored_observations_drive_the_band PASSED                 [ 69%]
src/tests/test_stage6_evaluation_metrics.py::test_no_seasonal_naive_construction_in_metrics_layer PASSED         [ 70%]
src/tests/test_stage6_evaluation_metrics.py::test_series_carries_no_reliability_or_calibration PASSED            [ 70%]
src/tests/test_stage6_p25_adversarial.py::test_p25_01_multi_rv_earliest_publication_wins PASSED                  [ 70%]
src/tests/test_stage6_p25_adversarial.py::test_p25_02_same_publication_tie_break PASSED                          [ 70%]
src/tests/test_stage6_p25_adversarial.py::test_p25_03_restated_later_publication_loses_to_first_known PASSED     [ 70%]
src/tests/test_stage6_p25_adversarial.py::test_p25_04_invalid_report_version_never_scores PASSED                 [ 70%]
src/tests/test_stage6_p25_adversarial.py::test_p25_05_missing_actual_value_quarantines PASSED                    [ 70%]
src/tests/test_stage6_p25_adversarial.py::test_p25_06_estimated_scores_with_limited_quality PASSED               [ 70%]
src/tests/test_stage6_p25_adversarial.py::test_p25_07_suspicious_quarantines_verbatim PASSED                     [ 70%]
src/tests/test_stage6_p25_adversarial.py::test_p25_08_unmapped_quarantines_verbatim PASSED                       [ 70%]
src/tests/test_stage6_p25_adversarial.py::test_p25_09_conflicting_duplicates_fail_closed PASSED                  [ 70%]
src/tests/test_stage6_p25_adversarial.py::test_p25_10_dup_key_across_horizons_does_not_collide PASSED            [ 70%]
src/tests/test_stage6_p25_adversarial.py::test_p25_11_dup_key_across_versions_does_not_collide PASSED            [ 71%]
src/tests/test_stage6_p25_adversarial.py::test_p25_12_dup_key_across_cutoffs_does_not_collide PASSED             [ 71%]
src/tests/test_stage6_p25_adversarial.py::test_p25_13_zero_actual_positive_forecast_scores PASSED                [ 71%]
src/tests/test_stage6_p25_adversarial.py::test_p25_14_zero_actual_negative_forecast_scores PASSED                [ 71%]
src/tests/test_stage6_p25_adversarial.py::test_p25_15_zero_over_zero_is_zero_base PASSED                         [ 71%]
src/tests/test_stage6_p25_adversarial.py::test_p25_16_zero_forecast_is_zero_base PASSED                          [ 71%]
src/tests/test_stage6_p25_adversarial.py::test_p25_17_positive_forecast_zero_actual_regime_none PASSED           [ 71%]
src/tests/test_stage6_p25_adversarial.py::test_p25_restated_series_flags_limited_quality PASSED                  [ 71%]
src/tests/test_stage6_p25_selection.py::test_selection_earliest_publication_wins PASSED                          [ 71%]
src/tests/test_stage6_p25_selection.py::test_selection_single_candidate_passthrough PASSED                       [ 71%]
src/tests/test_stage6_p25_selection.py::test_selection_tie_break_by_version_number_then_id PASSED                [ 71%]
src/tests/test_stage6_p25_selection.py::test_selection_exact_tie_fails_closed_no_id_fallback PASSED              [ 72%]
src/tests/test_stage6_p25_selection.py::test_selection_none_version_number_sorts_as_zero PASSED                  [ 72%]
src/tests/test_stage6_p25_selection.py::test_selection_filters_none_id_and_none_publication PASSED               [ 72%]
src/tests/test_stage6_p25_selection.py::test_selection_all_invalid_returns_none PASSED                           [ 72%]
src/tests/test_stage6_p25_selection.py::test_selection_is_input_order_independent PASSED                         [ 72%]
src/tests/test_stage6_p25_selection.py::test_scoring_eligibility_per_state[VALID-True] PASSED                    [ 72%]
src/tests/test_stage6_p25_selection.py::test_scoring_eligibility_per_state[ESTIMATED-True] PASSED                [ 72%]
src/tests/test_stage6_p25_selection.py::test_scoring_eligibility_per_state[RESTATED-True] PASSED                 [ 72%]
src/tests/test_stage6_p25_selection.py::test_scoring_eligibility_per_state[MISSING-False] PASSED                 [ 72%]
src/tests/test_stage6_p25_selection.py::test_scoring_eligibility_per_state[SUSPICIOUS-False] PASSED              [ 72%]
src/tests/test_stage6_p25_selection.py::test_scoring_eligibility_per_state[UNMAPPED-False] PASSED                [ 72%]
src/tests/test_stage6_p25_selection.py::test_key_is_7_tuple_with_scenario_last PASSED                            [ 73%]
src/tests/test_stage6_p25_selection.py::test_key_scenario_distinct_keys_differ PASSED                            [ 73%]
src/tests/test_stage6_p25_selection.py::test_key_forecast_id_does_not_affect_key PASSED                          [ 73%]
src/tests/test_stage6_p25_selection.py::test_build_observation_invalid_report_version_status PASSED              [ 73%]
src/tests/test_stage6_p38_closure.py::test_p38_mixed_cutoff_raises_before_scoring_no_partial_result PASSED       [ 73%]
src/tests/test_stage6_p38_closure.py::test_p38_empty_input_keeps_explicit_empty_none_cutoff PASSED               [ 73%]
src/tests/test_stage6_p38_closure.py::test_p38_single_cutoff_still_evaluates PASSED                              [ 73%]
src/tests/test_stage6_p38_closure.py::test_p38_mixed_cutoff_multi_scenario_raises PASSED                         [ 73%]
src/tests/test_stage6_p38_closure.py::test_p38_actual_zero_mape_excluded_error_retained PASSED                   [ 73%]
src/tests/test_stage6_p38_closure.py::test_p38_actual_zero_negative_forecast_bias_plus_one PASSED                [ 73%]
src/tests/test_stage6_p38_closure.py::test_p38_actual_zero_series_mape_null_bias_kept PASSED                     [ 73%]
src/tests/test_stage6_p38_closure.py::test_p38_zero_zero_is_bias_undefined_with_status PASSED                    [ 74%]
src/tests/test_stage6_p38_closure.py::test_p38_bias_undefined_zero_zero_excluded_from_bias_mean PASSED           [ 74%]
src/tests/test_stage6_p38_closure.py::test_p38_mape_bias_independent_counts_mixed_series PASSED                  [ 74%]
src/tests/test_stage6_p38_closure.py::test_p38_baseline_bias_paired_same_event_set PASSED                        [ 74%]
src/tests/test_stage6_p38_closure.py::test_p38_three_scenarios_share_one_actual_no_pooling PASSED                [ 74%]
src/tests/test_stage6_p38_closure.py::test_p38_mixed_scenarios_plus_duplicates PASSED                            [ 74%]
src/tests/test_stage6_p38_closure.py::test_p38_actual_zero_with_independent_eligibility_mixed PASSED             [ 74%]
src/tests/test_stage6_p38_closure.py::test_p38_reordered_observations_stable PASSED                              [ 74%]
src/tests/test_stage6_p38_closure.py::test_p38_reliability_stays_none_and_sufficiency_bands PASSED               [ 74%]
src/tests/test_stage6_p38_closure.py::test_p38_exact_actual_tie_fails_closed_version_order_still_works PASSED    [ 74%]
src/tests/test_stage6_p39_cutoff.py::test_p39_01_single_valid_cutoff_succeeds PASSED                             [ 74%]
src/tests/test_stage6_p39_cutoff.py::test_p39_02_multiple_same_cutoff_succeeds PASSED                            [ 75%]
src/tests/test_stage6_p39_cutoff.py::test_p39_03_equivalent_tz_aware_cutoffs_succeed PASSED                      [ 75%]
src/tests/test_stage6_p39_cutoff.py::test_p39_04_distinct_non_null_cutoffs_fail PASSED                           [ 75%]
src/tests/test_stage6_p39_cutoff.py::test_p39_05_valid_plus_missing_forecast_cutoff_fails PASSED                 [ 75%]
src/tests/test_stage6_p39_cutoff.py::test_p39_06_all_missing_cutoffs_fail PASSED                                 [ 75%]
src/tests/test_stage6_p39_cutoff.py::test_p39_07_valid_forecast_plus_missing_ttm_cutoff_fails PASSED             [ 75%]
src/tests/test_stage6_p39_cutoff.py::test_p39_08_distinct_forecast_ttm_cutoffs_fail PASSED                       [ 75%]
src/tests/test_stage6_p39_cutoff.py::test_p39_09_matching_forecast_ttm_succeeds_correct_cutoff PASSED            [ 75%]
src/tests/test_stage6_p39_cutoff.py::test_p39_10_ttm_only_valid_reports_cutoff PASSED                            [ 75%]
src/tests/test_stage6_p39_cutoff.py::test_p39_11_ttm_only_missing_cutoff_fails PASSED                            [ 75%]
src/tests/test_stage6_p39_cutoff.py::test_p39_12_explicitly_empty_keeps_none_cutoff PASSED                       [ 75%]
src/tests/test_stage6_p39_cutoff.py::test_p39_13_rejected_invocation_returns_no_partial_result PASSED            [ 76%]
src/tests/test_stage6_p39_cutoff.py::test_p39_14_reordered_interleaved_inputs_same_decision PASSED               [ 76%]
src/tests/test_stage6_p39_cutoff.py::test_p39_15_three_scenarios_one_cutoff_stay_separate PASSED                 [ 76%]
src/tests/test_stage6_p39_cutoff.py::test_p39_16_multi_scenario_mixed_fails_closed_no_partial PASSED             [ 76%]
src/tests/test_stage6_p39_cutoff.py::test_p39_17_later_published_actual_stays_eligible PASSED                    [ 76%]
src/tests/test_stage6_p39_cutoff.py::test_p39_18_provenance_purpose_supersession_unchanged PASSED                [ 76%]
src/tests/test_stage6_p39_cutoff.py::test_p39_19_ttm_conservation_and_duplicates_intact PASSED                   [ 76%]
src/tests/test_stage6_p40_duplicates.py::test_p40_01_single_ttm_counted_once PASSED                              [ 76%]
src/tests/test_stage6_p40_duplicates.py::test_p40_02_two_distinct_ttm_counted_twice PASSED                       [ 76%]
src/tests/test_stage6_p40_duplicates.py::test_p40_03_exact_repeat_ttm_inflates_nothing PASSED                    [ 76%]
src/tests/test_stage6_p40_duplicates.py::test_p40_04_triple_repeat_still_counts_once PASSED                      [ 76%]
src/tests/test_stage6_p40_duplicates.py::test_p40_05_reordered_duplicates_same_decision PASSED                   [ 77%]
src/tests/test_stage6_p40_duplicates.py::test_p40_06_forecast_ttm_same_identity_overlap_not_double_counted PASSED [ 77%]
src/tests/test_stage6_p40_duplicates.py::test_p40_07_distinct_periods_stay_distinct PASSED                       [ 77%]
src/tests/test_stage6_p40_duplicates.py::test_p40_08_same_numbers_different_keys_not_deduped PASSED              [ 77%]
src/tests/test_stage6_p40_duplicates.py::test_p40_09_cross_scenario_separation PASSED                            [ 77%]
src/tests/test_stage6_p40_duplicates.py::test_p40_10_cross_horizon_separation PASSED                             [ 77%]
src/tests/test_stage6_p40_duplicates.py::test_p40_11_cross_version_separation PASSED                             [ 77%]
src/tests/test_stage6_p40_duplicates.py::test_p40_12_conflicting_same_identity_quarantines_wholesale PASSED      [ 77%]
src/tests/test_stage6_p40_duplicates.py::test_p40_13_conflict_does_not_touch_neighbors PASSED                    [ 77%]
src/tests/test_stage6_p40_duplicates.py::test_p40_14_duplicates_cannot_inflate_sufficiency PASSED                [ 77%]
src/tests/test_stage6_p40_duplicates.py::test_p40_15_duplicate_leaves_remaining_pairing_intact PASSED            [ 77%]
src/tests/test_stage6_p40_duplicates.py::test_p40_16_primary_vs_sensitivity_independently_correct PASSED         [ 78%]
src/tests/test_stage6_p40_duplicates.py::test_p40_17_cutoff_rejections_still_fail_closed PASSED                  [ 78%]
src/tests/test_stage6_p40_duplicates.py::test_p40_18_ttm_only_empty_later_actual_intact PASSED                   [ 78%]
src/tests/test_stage6_p40_duplicates.py::test_p40_19_rejections_return_no_partial_result PASSED                  [ 78%]
src/tests/test_stage6_p41_cutoff_identity.py::test_p41_01_naive_and_aware_same_instant_share_identity PASSED     [ 78%]
src/tests/test_stage6_p41_cutoff_identity.py::test_p41_02_tz_offset_equivalent_shares_identity PASSED            [ 78%]
src/tests/test_stage6_p41_cutoff_identity.py::test_p41_03_iso_string_equivalent_shares_identity PASSED           [ 78%]
src/tests/test_stage6_p41_cutoff_identity.py::test_p41_04_distinct_instants_stay_distinct PASSED                 [ 78%]
src/tests/test_stage6_p41_cutoff_identity.py::test_p41_05_equivalent_cutoffs_collide_quarantine_wholesale PASSED [ 78%]
src/tests/test_stage6_p41_cutoff_identity.py::test_p41_06_pipeline_guard_accepts_equivalent_pair_single_cutoff PASSED [ 78%]
src/tests/test_stage6_p41_cutoff_identity.py::test_p41_07_three_equivalent_forms_collide_wholesale_no_winner_pick PASSED [ 78%]
src/tests/test_stage6_p41_cutoff_identity.py::test_p41_08_reordered_equivalent_cutoffs_decide_identically PASSED [ 79%]
src/tests/test_stage6_p41_cutoff_identity.py::test_p41_09_repeated_ttm_equivalent_forms_inflate_nothing PASSED   [ 79%]
src/tests/test_stage6_p41_cutoff_identity.py::test_p41_10_forecast_ttm_overlap_on_cutoff_form_only PASSED        [ 79%]
src/tests/test_stage6_p41_cutoff_identity.py::test_p41_11_distinct_periods_same_canonical_instant_stay_distinct PASSED [ 79%]
src/tests/test_stage6_p41_cutoff_identity.py::test_p41_12_scenario_isolation_with_mixed_equivalent_forms PASSED  [ 79%]
src/tests/test_stage6_p41_cutoff_identity.py::test_p41_13_horizon_version_isolation_with_mixed_equivalent_forms PASSED [ 79%]
src/tests/test_stage6_p41_cutoff_identity.py::test_p41_14_missing_invalid_mixed_instants_fail_closed PASSED      [ 79%]
src/tests/test_stage6_p41_cutoff_identity.py::test_p41_15_empty_and_ttm_only_with_equivalent_forms PASSED        [ 79%]
src/tests/test_stage6_p41_cutoff_identity.py::test_p41_16_later_published_actual_stays_eligible PASSED           [ 79%]
src/tests/test_stage6_p41_cutoff_identity.py::test_p41_17_rejected_equivalent_mixed_invocation_returns_no_partial PASSED [ 79%]
src/tests/test_stage6_production_pipeline.py::test_normal_path_scores_end_to_end PASSED                          [ 79%]
src/tests/test_stage6_production_pipeline.py::test_under_forecast_positive_bias PASSED                           [ 80%]
src/tests/test_stage6_production_pipeline.py::test_over_forecast_negative_bias PASSED                            [ 80%]
src/tests/test_stage6_production_pipeline.py::test_zero_forecast_quarantined_never_zeroed PASSED                 [ 80%]
src/tests/test_stage6_production_pipeline.py::test_zero_actual_excluded_from_mape_end_to_end PASSED              [ 80%]
src/tests/test_stage6_production_pipeline.py::test_loss_profit_regimes_quarantined PASSED                        [ 80%]
src/tests/test_stage6_production_pipeline.py::test_sign_change_name_pinned_no_percentage_metrics PASSED          [ 80%]
src/tests/test_stage6_production_pipeline.py::test_each_horizon_independent_over_overlapping_periods PASSED      [ 80%]
src/tests/test_stage6_production_pipeline.py::test_model_versions_never_mix PASSED                               [ 80%]
src/tests/test_stage6_production_pipeline.py::test_sufficiency_bands_on_path[4-INSUFFICIENT_DATA] PASSED         [ 80%]
src/tests/test_stage6_production_pipeline.py::test_sufficiency_bands_on_path[6-LOW_CONFIDENCE] PASSED            [ 80%]
src/tests/test_stage6_production_pipeline.py::test_sufficiency_bands_on_path[9-MODERATE_CONFIDENCE] PASSED       [ 80%]
src/tests/test_stage6_production_pipeline.py::test_sufficiency_bands_on_path[12-ADEQUATE] PASSED                 [ 80%]
src/tests/test_stage6_production_pipeline.py::test_model_better_than_baseline_positive_improvement PASSED        [ 81%]
src/tests/test_stage6_production_pipeline.py::test_baseline_better_than_model_negative_improvement PASSED        [ 81%]
src/tests/test_stage6_production_pipeline.py::test_zero_baseline_error_yields_missing_improvement_not_zero PASSED [ 81%]
src/tests/test_stage6_production_pipeline.py::test_missing_baseline_yields_missing_comparison PASSED             [ 81%]
src/tests/test_stage6_production_pipeline.py::test_isolated_bias_stays_no_calibration PASSED                     [ 81%]
src/tests/test_stage6_production_pipeline.py::test_unanimous_bias_still_no_calibration_names_missing_authority PASSED [ 81%]
src/tests/test_stage6_production_pipeline.py::test_pit_leaking_input_quarantined_on_path PASSED                  [ 81%]
src/tests/test_stage6_production_pipeline.py::test_later_published_actual_scores_as_outcome PASSED               [ 81%]
src/tests/test_stage6_production_pipeline.py::test_unbound_forecast_never_scores PASSED                          [ 81%]
src/tests/test_stage6_production_pipeline.py::test_nonvalid_actual_states_quarantined_verbatim[SUSPICIOUS] PASSED [ 81%]
src/tests/test_stage6_production_pipeline.py::test_nonvalid_actual_states_quarantined_verbatim[UNMAPPED] PASSED  [ 81%]
src/tests/test_stage6_production_pipeline.py::test_limited_quality_states_score_with_flag[ESTIMATED] PASSED      [ 82%]
src/tests/test_stage6_production_pipeline.py::test_limited_quality_states_score_with_flag[RESTATED] PASSED       [ 82%]
src/tests/test_stage6_production_pipeline.py::test_duplicate_observations_quarantined_wholesale PASSED           [ 82%]
src/tests/test_stage6_production_pipeline.py::test_duplicate_forecast_id_only_still_collides PASSED              [ 82%]
src/tests/test_stage6_production_pipeline.py::test_duplicate_scenario_differs_does_not_collide PASSED            [ 82%]
src/tests/test_stage6_production_pipeline.py::test_null_is_never_zero_on_path PASSED                             [ 82%]
src/tests/test_stage6_production_pipeline.py::test_ttm_observations_conserved_exactly_once PASSED                [ 82%]
src/tests/test_stage6_production_pipeline.py::test_ttm_same_period_collision_quarantines_both PASSED             [ 82%]
src/tests/test_stage6_production_pipeline.py::test_holdout_projection_passes_only_holdout PASSED                 [ 82%]
src/tests/test_stage6_production_pipeline.py::test_overlapping_holdout_rejected_as_contamination PASSED          [ 82%]
src/tests/test_stage6_production_pipeline.py::test_inverted_holdout_rejected PASSED                              [ 82%]
src/tests/test_stage6_production_pipeline.py::test_regime_only_series_withholds_with_unavailable_named PASSED    [ 83%]
src/tests/test_stage6_production_pipeline.py::test_forward_pe_passes_through_untouched PASSED                    [ 83%]
src/tests/test_stage6_production_pipeline.py::test_pipeline_never_mutates_stage5_records PASSED                  [ 83%]
src/tests/test_stage6_production_pipeline.py::test_pipeline_invents_no_methodology PASSED                        [ 83%]
src/tests/test_stage6_production_pipeline.py::test_pipeline_has_no_stage5_writes_or_stage7_logic PASSED          [ 83%]
src/tests/test_stage6_reliability_governance.py::test_weights_match_spec_section_21 PASSED                       [ 83%]
src/tests/test_stage6_reliability_governance.py::test_performance_assembly_is_exact_weighted_sum PASSED          [ 83%]
src/tests/test_stage6_reliability_governance.py::test_component_bounds_are_structural_not_methodology PASSED     [ 83%]
src/tests/test_stage6_reliability_governance.py::test_performance_score_is_not_a_reliability PASSED              [ 83%]
src/tests/test_stage6_reliability_governance.py::test_reliability_withheld_with_mappings_named_not_zero PASSED   [ 83%]
src/tests/test_stage6_reliability_governance.py::test_unavailable_components_named_never_defaulted PASSED        [ 83%]
src/tests/test_stage6_reliability_governance.py::test_governed_series_withholds_reliability_even_with_components PASSED [ 84%]
src/tests/test_stage6_reliability_governance.py::test_governed_series_without_components_withholds_performance_too PASSED [ 84%]
src/tests/test_stage6_reliability_governance.py::test_govern_series_never_mutates_the_p19_aggregate PASSED       [ 84%]
src/tests/test_stage6_reliability_governance.py::test_no_calibration_is_the_default_verdict PASSED               [ 84%]
src/tests/test_stage6_reliability_governance.py::test_candidate_and_calibrated_are_unconstructible_without_authority PASSED [ 84%]
src/tests/test_stage6_reliability_governance.py::test_refused_transition_stays_no_calibration_with_b3_b4_named PASSED [ 84%]
src/tests/test_stage6_reliability_governance.py::test_suggestive_bias_evidence_still_yields_no_calibration PASSED [ 84%]
src/tests/test_stage6_reliability_governance.py::test_no_new_version_without_calibrated PASSED                   [ 84%]
src/tests/test_stage6_reliability_governance.py::test_pit_later_published_actual_still_governed PASSED           [ 84%]
src/tests/test_stage6_reliability_governance.py::test_horizon_and_version_isolation_survive_governance PASSED    [ 84%]
src/tests/test_stage6_reliability_governance.py::test_null_and_quarantines_flow_through_unchanged PASSED         [ 84%]
src/tests/test_stage6_reliability_governance.py::test_missing_mape_marks_unavailable_component PASSED            [ 85%]
src/tests/test_stage6_reliability_governance.py::test_regime_only_series_names_mape_unavailable PASSED           [ 85%]
src/tests/test_stage6_reliability_governance.py::test_full_path_observation_to_governance PASSED                 [ 85%]
src/tests/test_stage6_reliability_governance.py::test_legacy_engine_path_removed PASSED                          [ 85%]
src/tests/test_stage6_reliability_governance.py::test_module_exports_no_numeric_mapping PASSED                   [ 85%]
src/tests/test_stage6_reliability_governance.py::test_performance_times_confidence_is_not_a_reliability PASSED   [ 85%]
src/tests/test_stage6_reliability_governance.py::test_no_forecast_scaling_surface PASSED                         [ 85%]
src/tests/test_stage6_reliability_governance.py::test_no_numeric_default_for_unresolved_rules PASSED             [ 85%]
src/tests/test_stage6_reliability_governance.py::test_holdout_overlapping_evidence_is_contamination PASSED       [ 85%]
src/tests/test_stage6_reliability_governance.py::test_holdout_before_evidence_rejected PASSED                    [ 85%]
src/tests/test_stage6_reliability_governance.py::test_oos_projection_never_leaks_evidence PASSED                 [ 85%]
src/tests/test_stage6_reliability_governance.py::test_old_version_never_overwritten_by_governance PASSED         [ 86%]
src/tests/test_stage6_reliability_governance.py::test_forward_pe_passes_through_untouched PASSED                 [ 86%]
src/tests/test_stage6_reliability_governance.py::test_invalid_calibration_state_rejected PASSED                  [ 86%]
src/tests/test_stage6_reliability_governance.py::test_refusing_a_non_advance_rejected PASSED                     [ 86%]
src/tests/test_stage6_scenario_isolation.py::test_keys_all_three_pairs_unequal PASSED                            [ 86%]
src/tests/test_stage6_scenario_isolation.py::test_keys_preserve_canonical_scenario PASSED                        [ 86%]
src/tests/test_stage6_scenario_isolation.py::test_keys_hash_set_dict_behavior PASSED                             [ 86%]
src/tests/test_stage6_scenario_isolation.py::test_three_scenarios_yield_three_series PASSED                      [ 86%]
src/tests/test_stage6_scenario_isolation.py::test_mape_bias_inputs_not_pooled_across_scenarios PASSED            [ 86%]
src/tests/test_stage6_scenario_isolation.py::test_series_evaluation_carries_scenario PASSED                      [ 86%]
src/tests/test_stage6_scenario_isolation.py::test_baseline_pairing_stays_within_scenario PASSED                  [ 86%]
src/tests/test_stage6_scenario_isolation.py::test_baseline_absent_in_other_scenarios PASSED                      [ 87%]
src/tests/test_stage6_scenario_isolation.py::test_missing_scenario_raises_fail_closed[] PASSED                   [ 87%]
src/tests/test_stage6_scenario_isolation.py::test_missing_scenario_raises_fail_closed[None] PASSED               [ 87%]
src/tests/test_stage6_scenario_isolation.py::test_empty_scenario_record_raises_fail_closed PASSED                [ 87%]
src/tests/test_stage6_scenario_isolation.py::test_noncanonical_scenario_preserved_verbatim_and_isolated PASSED   [ 87%]
src/tests/test_stage6_scenario_isolation.py::test_single_scenario_values_unchanged PASSED                        [ 87%]
src/tests/test_stage6_scenario_isolation.py::test_three_scenarios_not_three_observations_in_shared_series PASSED [ 87%]
src/tests/test_stage6_scenario_isolation.py::test_insertion_order_all_six_permutations PASSED                    [ 87%]
src/tests/test_stage6_scenario_isolation.py::test_interleaved_multi_company_inputs PASSED                        [ 87%]
src/tests/test_stage6_scenario_isolation.py::test_duplicate_within_one_scenario_quarantines_only_that_scenario PASSED [ 87%]
src/tests/test_stage6_scenario_isolation.py::test_identical_values_across_scenarios_still_separate PASSED        [ 87%]
src/tests/test_stage6_scenario_isolation.py::test_empty_input_empty_result PASSED                                [ 88%]
src/tests/test_stage6_scenario_isolation.py::test_single_scenario_input_one_series PASSED                        [ 88%]
src/tests/test_stage6_scenario_isolation.py::test_pipeline_three_scenarios_end_to_end PASSED                     [ 88%]
src/tests/test_stage6_scenario_isolation.py::test_pipeline_baseline_pairing_per_scenario PASSED                  [ 88%]
src/tests/test_stage789_service_interface.py::test_real_service_path_preserves_stage5_eps_and_market_provenance PASSED [ 88%]
src/tests/test_stage789_service_interface.py::test_real_service_path_does_not_leak_future_market_prices PASSED   [ 88%]
src/tests/test_stage789_service_interface.py::test_missing_price_fails_closed_before_stage9_runs PASSED          [ 88%]
src/tests/test_stage789_service_interface.py::test_insufficient_market_evidence_is_not_presented_as_valid_market_analysis PASSED [ 88%]
src/tests/test_stage7_valuation.py::test_jalali_service_uses_selected_price_and_preserves_provenance PASSED      [ 88%]
src/tests/test_stage7_valuation.py::test_jalali_service_fails_closed_without_eligible_observation PASSED         [ 88%]
src/tests/test_stage7_valuation.py::test_jalali_service_rejects_forecast_from_another_company PASSED             [ 88%]
src/tests/test_stage7_valuation.py::test_valuation_models PASSED                                                 [ 89%]
src/tests/test_stage7_valuation.py::test_valuation_engine_forward_pe_and_expected_fair_value PASSED              [ 89%]
src/tests/test_stage7_valuation.py::test_industry_forward_pe_requires_eight_valid_peers PASSED                   [ 89%]
src/tests/test_stage7_valuation.py::test_industry_ttm_is_fallback_after_historical_median PASSED                 [ 89%]
src/tests/test_stage7_valuation.py::test_negative_eps_does_not_create_fake_pe_or_fair_value PASSED               [ 89%]
src/tests/test_stage7_valuation.py::test_reliability_does_not_change_forward_pe_or_fair_value PASSED             [ 89%]
src/tests/test_stage7_valuation.py::test_direct_probability_adjustments_are_rejected_in_favor_of_family_evidence PASSED [ 89%]
src/tests/test_stage7_valuation.py::test_probability_evidence_is_family_level_and_equal_weighted PASSED          [ 89%]
src/tests/test_stage7_valuation.py::test_probability_evidence_rejects_unknown_or_incomplete_family_data PASSED   [ 89%]
src/tests/test_stage7_valuation.py::test_scenario_multiple_adjustments_require_economic_rationale_and_are_bounded PASSED [ 89%]
src/tests/test_stage7_valuation.py::test_alerts_include_severity_and_driver_focus PASSED                         [ 89%]
src/tests/test_stage7_valuation.py::test_p2_sensitivity_drivers_present_and_bounded PASSED                       [ 90%]
src/tests/test_stage7_valuation.py::test_p2_sensitivity_missing_data_empty_drivers PASSED                        [ 90%]
src/tests/test_stage7_valuation.py::test_p2_sensitivity_deterministic_repeated_runs PASSED                       [ 90%]
src/tests/test_stage7_valuation.py::test_p2_alert_severity_levels_valid PASSED                                   [ 90%]
src/tests/test_stage7_valuation.py::test_p2_alert_low_reliability_threshold_boundaries PASSED                    [ 90%]
src/tests/test_stage7_valuation.py::test_p2_alert_high_dispersion_threshold_boundaries PASSED                    [ 90%]
src/tests/test_stage7_valuation.py::test_p2_alert_divergence_ratios_boundaries PASSED                            [ 90%]
src/tests/test_stage7_valuation.py::test_v1_sector_examples_use_only_eps_and_target_pe_drivers PASSED            [ 90%]
src/tests/test_stage7_valuation.py::test_v1_uses_stage5_eps_without_recalculating_from_net_profit PASSED         [ 90%]
src/tests/test_stage7_valuation.py::test_v1_defers_undefined_flip_dependence_and_assumption_alerts PASSED        [ 90%]
src/tests/test_stage7_valuation.py::test_p3_sensitivity_recomputes_from_valuation_identity PASSED                [ 90%]
src/tests/test_stage7_valuation.py::test_p3_nan_eps_is_guarded_as_invalid PASSED                                 [ 90%]
src/tests/test_stage7_valuation.py::test_p3_zero_and_negative_price_guarded PASSED                               [ 91%]
src/tests/test_stage7_valuation.py::test_p3_nonfinite_benchmark_series_filtered PASSED                           [ 91%]
src/tests/test_stage7_valuation.py::test_p3_nonfinite_scores_fall_back_to_defaults PASSED                        [ 91%]
src/tests/test_stage7_valuation.py::test_p3_flip_dependence_alerts_remain_explicitly_unresolved PASSED           [ 91%]
src/tests/test_stage7_valuation.py::test_p4_peer_count_below_minimum_falls_back PASSED                           [ 91%]
src/tests/test_stage7_valuation.py::test_p4_peer_count_at_minimum_selects_industry_forward PASSED                [ 91%]
src/tests/test_stage7_valuation.py::test_p4_peer_count_above_minimum_and_median_provenance PASSED                [ 91%]
src/tests/test_stage7_valuation.py::test_p4_peer_count_filters_invalid_values PASSED                             [ 91%]
src/tests/test_stage7_valuation.py::test_p4_peer_count_empty_data_reports_zero_and_falls_back PASSED             [ 91%]
src/tests/test_stage7_valuation.py::test_p4_benchmark_fallback_ignores_forward_count_for_ttm PASSED              [ 91%]
src/tests/test_stage7_valuation.py::test_p5_nonfinite_price_yields_null_outputs PASSED                           [ 91%]
src/tests/test_stage7_valuation.py::test_p5_missing_eps_is_not_applicable_not_zero PASSED                        [ 92%]
src/tests/test_stage7_valuation.py::test_p5_nonfinite_reliability_echo_sanitized PASSED                          [ 92%]
src/tests/test_stage7_valuation.py::test_p5_nonfinite_probability_confidence_echo_finite PASSED                  [ 92%]
src/tests/test_stage7_valuation.py::test_p5_missing_data_quality_does_not_crash PASSED                           [ 92%]
src/tests/test_stage7_valuation.py::test_p5_nonfinite_multiple_adjustment_rejected PASSED                        [ 92%]
src/tests/test_stage7_valuation.py::test_p5_nan_probability_evidence_rejected PASSED                             [ 92%]
src/tests/test_stage7_valuation.py::test_p5_datetime_echoes_normalized_to_utc PASSED                             [ 92%]
src/tests/test_stage7_valuation.py::test_p5_default_cutoff_inherits_forecast_cutoff_normalized PASSED            [ 92%]
src/tests/test_stage7_valuation.py::test_p5_undated_benchmark_series_carry_no_provenance PASSED                  [ 92%]
src/tests/test_stage7_valuation.py::test_p6_production_path_real_stage5_forecast PASSED                          [ 92%]
src/tests/test_stage7_valuation.py::test_p6_cutoff_pit_limitation_pinned PASSED                                  [ 92%]
src/tests/test_stage7_valuation.py::test_p6_missing_benchmarks_yield_guarded_nulls PASSED                        [ 93%]
src/tests/test_stage7_valuation.py::test_p6_scenario_ordering_flag_and_probability_normalization PASSED          [ 93%]
src/tests/test_stage7_valuation.py::test_p6_invalid_eps_variants_never_fabricate_values PASSED                   [ 93%]
src/tests/test_stage7_valuation.py::test_p6_repeat_runs_identical_on_full_contract PASSED                        [ 93%]
src/tests/test_stage7_valuation.py::test_p6_regression_prior_behavior_preserved PASSED                           [ 93%]
src/tests/test_stage7_valuation.py::test_p10_expensive_base_upside_parameterized_outputs_unchanged PASSED        [ 93%]
src/tests/test_stage7_valuation.py::test_p10_expensive_threshold_consumed_from_parameters PASSED                 [ 93%]
src/tests/test_stage7_valuation.py::test_p12_calculation_timestamp_utc_aware_and_deterministic PASSED            [ 93%]
src/tests/test_stage7_valuation.py::test_p32_input_refs_before_cutoff_leave_results_unchanged PASSED             [ 93%]
src/tests/test_stage7_valuation.py::test_p32_input_ref_after_cutoff_rejected_on_valuation_path PASSED            [ 93%]
src/tests/test_stage7_valuation.py::test_p32_input_ref_at_cutoff_boundary_accepted PASSED                        [ 93%]
src/tests/test_stage7_valuation.py::test_p32_input_ref_missing_date_rejected PASSED                              [ 94%]
src/tests/test_stage7_valuation.py::test_p32_input_refs_absent_preserves_legacy_path PASSED                      [ 94%]
src/tests/test_stage7_valuation.py::test_p53_embedded_forecast_input_ref_at_cutoff_is_enforced_and_accepted PASSED [ 94%]
src/tests/test_stage7_valuation.py::test_p53_stage5_dropped_future_input_is_not_reintroduced_to_stage7 PASSED    [ 94%]
src/tests/test_stage7_valuation.py::test_p53_embedded_forecast_input_ref_without_availability_is_rejected PASSED [ 94%]
src/tests/test_stage7_valuation.py::test_p53_explicit_empty_refs_do_not_bypass_embedded_forecast_provenance PASSED [ 94%]
src/tests/test_stage7_valuation.py::test_p53_stage5_forecast_without_provenance_preserves_legacy_path PASSED     [ 94%]
src/tests/test_stage7_valuation.py::test_p33_genesis_snapshot_matches_live_constants PASSED                      [ 94%]
src/tests/test_stage7_valuation.py::test_p33_result_carries_parameter_audit PASSED                               [ 94%]
src/tests/test_stage7_valuation.py::test_p33_resolve_exact_key_and_missing_raises PASSED                         [ 94%]
src/tests/test_stage7_valuation.py::test_p33_as_of_without_dated_records_raises PASSED                           [ 94%]
src/tests/test_stage7_valuation.py::test_p33_as_of_selection_mechanics PASSED                                    [ 95%]
src/tests/test_stage7_valuation.py::test_p33_as_of_overlap_raises_ambiguity PASSED                               [ 95%]
src/tests/test_stage7_valuation.py::test_p35_legacy_path_provenance_is_truthful_and_unchanged PASSED             [ 95%]
src/tests/test_stage7_valuation.py::test_p35_snapshot_reports_values_actually_consumed_when_module_constant_changes PASSED [ 95%]
src/tests/test_stage7_valuation.py::test_p35_as_of_selection_governs_calculation_and_snapshot_matches PASSED     [ 95%]
src/tests/test_stage7_valuation.py::test_p35_selected_set_governs_peers_alerts_and_scenario_weights PASSED       [ 95%]
src/tests/test_stage7_valuation.py::test_p35_missing_or_ambiguous_as_of_selection_fails_closed PASSED            [ 95%]
src/tests/test_stage7_valuation.py::test_p35_invalid_parameter_set_raises_without_fallback_to_constants PASSED   [ 95%]
src/tests/test_stage7_valuation.py::test_p35_isolation_from_global_mutation_and_snapshot_aliasing PASSED         [ 95%]
src/tests/test_stage7_valuation.py::test_p35_repeated_as_of_calculations_are_deterministic PASSED                [ 95%]
src/tests/test_stage7_valuation.py::test_d9_effective_cutoff_governs_selection_not_valuation_date PASSED         [ 95%]
src/tests/test_stage7_valuation.py::test_d9_exact_effective_from_boundary_is_accepted PASSED                     [ 96%]
src/tests/test_stage7_valuation.py::test_d9_future_effective_version_is_rejected PASSED                          [ 96%]
src/tests/test_stage7_valuation.py::test_d9_missing_eligible_dated_version_fails_closed_without_genesis_fallback PASSED [ 96%]
src/tests/test_stage7_valuation.py::test_d9_overlapping_eligible_versions_are_deterministic PASSED               [ 96%]
src/tests/test_stage7_valuation.py::test_d9_conflicting_parameter_as_of_is_rejected PASSED                       [ 96%]
src/tests/test_stage7_valuation.py::test_d9_without_any_cutoff_caller_supplied_as_of_is_labelled_truthfully PASSED [ 96%]
src/tests/test_stage7_valuation.py::test_d9_metadata_distinguishes_dated_selection_from_legacy_genesis PASSED    [ 96%]
src/tests/test_stage7_valuation.py::test_d9_legacy_path_stays_backward_compatible_and_never_claims_pit PASSED    [ 96%]
src/tests/test_stage7_valuation.py::test_d9_cutoff_governed_selection_is_deterministic_on_repeat PASSED          [ 96%]
src/tests/test_stage8_market.py::test_legacy_indicator_helpers_remain_available PASSED                           [ 96%]
src/tests/test_stage8_market.py::test_core_market_indicators PASSED                                              [ 96%]
src/tests/test_stage8_market.py::test_market_engine_returns_state_not_score PASSED                               [ 97%]
src/tests/test_stage8_market.py::test_market_output_contract_includes_52w_volume_and_value_context PASSED        [ 97%]
src/tests/test_stage8_market.py::test_trading_value_stability_is_coefficient_of_variation PASSED                 [ 97%]
src/tests/test_stage8_market.py::test_close_fallback_is_explicitly_flagged PASSED                                [ 97%]
src/tests/test_stage8_market.py::test_point_in_time_excludes_future_rows PASSED                                  [ 97%]
src/tests/test_stage8_market.py::test_adjusted_close_drives_historical_returns PASSED                            [ 97%]
src/tests/test_stage8_market.py::test_missing_benchmark_does_not_create_synthetic_relative_strength PASSED       [ 97%]
src/tests/test_stage8_market.py::test_relative_strength_uses_same_horizon PASSED                                 [ 97%]
src/tests/test_stage8_market.py::test_negative_market_state_generates_context_alerts_not_decision PASSED         [ 97%]
src/tests/test_stage8_market.py::test_drawdown_moderate_non_recovering_is_not_labeled_recovering PASSED          [ 97%]
src/tests/test_stage8_market.py::test_drawdown_recovery_requires_rebound_from_recent_low PASSED                  [ 97%]
src/tests/test_stage8_market.py::test_drawdown_deep_and_new_low_states_remain_distinct PASSED                    [ 98%]
src/tests/test_stage8_market.py::test_legacy_api_is_compatibility_only PASSED                                    [ 98%]
src/tests/test_stage8_market_parameters.py::test_model_version_parameters_are_the_source_of_market_thresholds PASSED [ 98%]
src/tests/test_stage8_market_parameters.py::test_liquidity_state_distinguishes_relative_low_and_high_activity PASSED [ 98%]
src/tests/test_stage9_decision.py::test_strong_buy_requires_aligned_families PASSED                              [ 98%]
src/tests/test_stage9_decision.py::test_jalali_orchestration_passes_stage7_result_to_stage9 PASSED               [ 98%]
src/tests/test_stage9_decision.py::test_jalali_orchestration_rejects_mismatched_fundamental_and_market_identity PASSED [ 98%]
src/tests/test_stage9_decision.py::test_value_trap_does_not_become_buy PASSED                                    [ 98%]
src/tests/test_stage9_decision.py::test_strong_but_expensive_is_not_buy PASSED                                   [ 98%]
src/tests/test_stage9_decision.py::test_low_forecast_reliability_limits_strong_conviction PASSED                 [ 98%]
src/tests/test_stage9_decision.py::test_market_does_not_override_strong_fundamentals PASSED                      [ 98%]
src/tests/test_stage9_decision.py::test_usd_share_value_is_context_not_a_new_score PASSED                        [ 99%]
src/tests/test_stage9_decision.py::test_negative_eps_valuation_is_not_reconstructed_by_stage9 PASSED             [ 99%]
src/tests/test_stage9_decision.py::test_no_position_sizing_contract PASSED                                       [ 99%]
src/tests/test_stage9_decision.py::test_hysteresis_prevents_small_buy_to_hold_change PASSED                      [ 99%]
src/tests/test_stage9_decision.py::test_hysteresis_allows_material_deterioration PASSED                          [ 99%]
src/tests/test_stage9_decision.py::test_decision_history_contract PASSED                                         [ 99%]
src/tests/test_stage9_decision.py::test_ranking_contract_has_no_new_score PASSED                                 [ 99%]
src/tests/test_stage9_decision.py::test_dashboard_contract_carries_required_fields PASSED                        [ 99%]
src/tests/test_stage9_decision.py::test_scenario_dispersion_threshold_boundaries PASSED                          [ 99%]
src/tests/test_stage9_decision.py::test_scenario_dispersion_causes_ten_point_confidence_deduction PASSED         [ 99%]
src/tests/test_stage9_decision.py::test_scenario_dispersion_blocks_strong_buy PASSED                             [ 99%]
src/tests/test_stage9_decision.py::test_scenario_dispersion_penalty_distinct_from_valuation_risk_level_high PASSED [100%]

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
============================== 1108 passed, 2 skipped, 153 warnings in 254.16s (0:04:14)
# P68-A
### گزارش بررسی معماری و رفع تناقض تاریخچه بازار (P68-A)

این گزارش صرفاً یک تحلیل و بررسی استایلی و ساختاری (Read-only) پیرامون وضعیت معماری بین‌مرحلی، رفع تناقضات مربوط به پرس‌وجوی تاریخچه بازار (مرحله ۸)، و تعیین گپ‌های باقی‌مانده در پروژه `analyzer` است. هیچ‌گونه تغییر کد یا اجرای تستی در این مرحله صورت نگرفته است.

---

### الف. اسنپ‌شات و دامنه (Snapshot and Scope)

* **فایل‌های موجود:** بررسی ساختار پروژه نشان می‌دهد پوشه‌های کلیدی مدل‌ها (`src/models/`), استخراج داده‌ها (`src/ingestion/market/`), موتور تحلیل بازار (`src/market/`), ارزیابی (`src/valuation/`), تصمیم‌گیری (`src/decision/`) و تست‌ها (`src/tests/`) در پکیج ضمیمه حضور دارند.


* **وضعیت فایل `src/market/queries.py`:** بررسی فهرست فایل‌ها حاکی از آن است که فایل `queries.py` در مسیر `src/market/` **وجود ندارد**. توابع پرس‌وجوی بازار منحصراً در `src/ingestion/market/queries.py` قرار دارند.


* **منابع شواهد:** استنباط‌ها مستقیماً بر اساس بازبینی کدهای منبع موجود در اسنپ‌شات و اسناد راهنمای قبلی (`stepsForStage7.md` و گزارش‌های پیشین) انجام شده است.



---

### ب. سازش‌پذیری و رفع تناقض بازار-تاریخچه P67/P68 (P67/P68 Reconciliation)

* **تناقض قبلی:** در گزارش‌های پیشین (P67/P68) ابهاماتی وجود داشت مبنی بر اینکه آیا پرس‌وجوی تاریخچه بازار برای مرحله ۸ کاملاً پیاده‌سازی شده است یا خیر.
* **یافته کد منبع:** تابع `select_market_price_as_of` در `src/ingestion/market/queries.py` صرفاً برای استخراج **یک قیمت تک‌نقطه‌ای (Single Price Observation)** به‌منظور استفاده در ارزیابی مرحله ۷ طراحی شده است.


* **نتیجه‌گیری:** ادعای وجود پرس‌وجوی کامل تاریخچه سری زمانی (Historical OHLCV Series) برای مرحله ۸ در کدهای منبع تأیید نشد. موتور تحلیل بازار (`MarketEngine.analyze_market` در `src/market/engine.py`) نیازمند یک سری تاریخی منظم است که در حال حاضر هیچ پرس‌وجوی بازیابی‌کننده‌ی سری زمانی تاریخی با قابلیت رعایت مرز `as-of` برای آن به صورت یکپارچه متصل نشده است.

---

### ج. ماتریس معماری بین‌مرحلی (Inter-Stage Architecture Matrix)

| مرز بین‌مرحلی | فراخواننده → فراخوانده‌شده | قرارداد داده و منبع | وضعیت مسیر | شواهد مستقیم | گپ / نتیجه‌گیری |
| --- | --- | --- | --- | --- | --- |
| **مرحله ۳ (داده‌های بنیادی) ← مرحله ۵ (پیش‌بینی)** | ماژول‌های Ingestion → مدل‌های `src/models/forecast.py` | داده‌های مالی و EPS تاریخی | مسیر تولیدی (Production) | کدهای مدل‌سازی و تست‌های مرحله ۵ | ساختار پایه‌ای برقرار است اما نیازمند کنترل دقیق نقطه‌زمانی (PIT) است. |
| **مرحله ۵ (پیش‌بینی/EPS) ← مرحله ۷ (ارزیابی)** | `src/valuation/service.py` → خروجی Stage 5 | `Forecast EPS × Target P/E` | مسیر تولیدی | فایل‌های `src/valuation/` و تست‌های مربوطه | EPS مرحله ۷ کاملاً به عنوان مقدار معتبر مرحله ۵ حفظ شده و بازمحاسبه نمی‌شود.

 |
| **دیتابیس تاریخچه بازار ← مرحله ۸ (تحلیل بازار)** | نامشخص → `MarketEngine.analyze_market` (`src/market/engine.py`) | سری زمانی OHLCV تاریخی با مرز `as-of` | **فاقد اتصال (Missing)** | عدم وجود پرس‌وجوی سری تاریخی در `src/ingestion/market/queries.py` | **گپ اصلی:** پرس‌وجوی بازیابی سری زمانی بازار برای Stage 8 وجود ندارد.

 |
| **مرحله ۷ و ۸ ← مرحله ۹ (تصمیم‌گیری)** | `src/decision/service.py` → `src/decision/engine.py` | نتیجه پیش‌بینی، بنیادی و بازار | نیمه‌پیوسته (Test-only / Intended) | کدهای ماژول `src/decision/` | سرویس تصمیم وجود دارد، اما به دلیل نقص در خروجی مرحله ۸، مسیر تولیدی کامل ندارد.

 |
| **مرحله ۹ (خروجی تصمیم) ← مصرف‌کننده نهایی** | نامشخص (فاقد Entry Point اصلی) | ساختار تصمیم نهایی و هشدارهای ریسک | ناشناخته / پیاده‌نشده | عدم وجود فایل `main.py` یا نقطه ورود جامع در ریشه `src/` | هیچ فایل ارکستراسیون یا لایه سرویس‌دهی نهایی برای اجرای سراسری کل پایپ‌لاین دیده نمی‌شود. |

---

### د. ثبت قراردادهای مفقوده (Missing-Contract Register)

1. **GAP-01: نبود پرس‌وجوی سری زمانی بازار (Market History Series Query)**
* **شواهد:** عدم وجود تابع یا ماژول پرس‌وجو برای استخراج آرایه‌ای از رکوردهای `MarketDaily` در بازه تاریخی مورد نیاز `MarketEngine` (فایل `src/market/queries.py` غایب است و `src/ingestion/market/queries.py` تنها تک‌رکورد بازمی‌گرداند).


* **اهمیت:** موتور تحلیل بازار مرحله ۸ بدون داشتن داده‌های تاریخی OHLCV قادر به محاسبه اندیکاتورها و سیگنال‌ها نیست.


* **اقدام لازم:** تعریف و پیاده‌سازی قرارداد پرس‌وجوی سری تاریخی با رعایت کامل تقویم جلالی و مرز قطع تاریخ (`as-of`).


2. **GAP-02: نبود لایه ارکستراسیون و نقطه ورود سراسری (Orchestration Entry Point)**
* **شواهد:** نبود اسکریپت اجرایی یا نقطه ورود (`main.py` یا مشابه) برای اتصال مراحل ۱ تا ۹ به یکدیگر.
* **اهمیت:** پلتفرم به‌صورت واحدهای ماژولار جداگانه توسعه یافته اما جریان اجرای سرتاسری (End-to-End) در سطح کد تولیدی تعریف نشده است.



---

### هـ. گام بعدی پیشنهادی (Recommended Next Step)

* **توسعه قرارداد داده‌های بازار مرحله ۸:** تمرکز باید بر روی طراحی و پیاده‌سازی پرس‌وجوی امن و نقطه‌زمانی سری‌های تاریخی بازار قرار گیرد تا `MarketEngine` بتواند داده‌های ورودی معتبر دریافت کند. بازنویسی موتور ارزیابی (`src/valuation/engine.py`) باید همچنان تا زمان تثبیت این لایه داده متوقف بماند.



---

### و. وضعیت نهایی (Final Status)

* **انتخاب:** *Partially verified; specific evidence gaps remain (تا حدی تأیید شده؛ گپ‌های شواهد مشخصی باقی مانده است).*
* **توضیح:** ابهامات و تناقضات گزارش‌های قبلی پیرامون مرحله ۸ رفع شد و مشخص گردید که ادعای وجود پرس‌وجوی تاریخچه بازار نادرست بوده است. این بررسی به‌طور کامل به اتمام رسیده و گپ‌های معماری مستند شدند.