(analyzer) PS D:\winprojects\analyzer> python -m pytest src/tests/test_stage8_market.py src/tests/test_stage8_market_service.py -v
================================================= test session starts =================================================
platform win32 -- Python 3.12.9, pytest-9.1.1, pluggy-1.6.0 -- D:\winprojects\analyzer\Scripts\python.exe
cachedir: .pytest_cache
rootdir: D:\winprojects\analyzer
collected 94 items

src/tests/test_stage8_market.py::test_legacy_indicator_helpers_remain_available PASSED                           [  1%]
src/tests/test_stage8_market.py::test_core_market_indicators PASSED                                              [  2%]
src/tests/test_stage8_market.py::test_market_engine_returns_state_not_score PASSED                               [  3%]
src/tests/test_stage8_market.py::test_market_output_contract_includes_52w_volume_and_value_context PASSED        [  4%]
src/tests/test_stage8_market.py::test_trading_value_stability_is_coefficient_of_variation PASSED                 [  5%]
src/tests/test_stage8_market.py::test_close_fallback_is_explicitly_flagged PASSED                                [  6%]
src/tests/test_stage8_market.py::test_point_in_time_excludes_future_rows PASSED                                  [  7%]
src/tests/test_stage8_market.py::test_adjusted_close_drives_historical_returns PASSED                            [  8%]
src/tests/test_stage8_market.py::test_missing_benchmark_does_not_create_synthetic_relative_strength PASSED       [  9%]
src/tests/test_stage8_market.py::test_relative_strength_uses_same_horizon PASSED                                 [ 10%]
src/tests/test_stage8_market.py::test_negative_market_state_generates_context_alerts_not_decision PASSED         [ 11%]
src/tests/test_stage8_market.py::test_drawdown_moderate_non_recovering_is_not_labeled_recovering PASSED          [ 12%]
src/tests/test_stage8_market.py::test_drawdown_recovery_requires_rebound_from_recent_low PASSED                  [ 13%]
src/tests/test_stage8_market.py::test_drawdown_deep_and_new_low_states_remain_distinct PASSED                    [ 14%]
src/tests/test_stage8_market.py::test_legacy_api_is_compatibility_only PASSED                                    [ 15%]
src/tests/test_stage8_market.py::test_legacy_api_rejects_undated_prices_instead_of_inventing_dates PASSED        [ 17%]
src/tests/test_stage8_market.py::test_legacy_api_rejects_duplicate_dates PASSED                                  [ 18%]
src/tests/test_stage8_market.py::test_as_of_boundary_is_inclusive PASSED                                         [ 19%]
src/tests/test_stage8_market.py::test_observations_after_as_of_are_excluded_across_day_month_and_year PASSED     [ 20%]
src/tests/test_stage8_market.py::test_cutoff_compares_year_then_month_then_day_numerically PASSED                [ 21%]
src/tests/test_stage8_market.py::test_as_of_before_all_observations_is_insufficient_data PASSED                  [ 22%]
src/tests/test_stage8_market.py::test_empty_market_data_is_insufficient_data PASSED                              [ 23%]
src/tests/test_stage8_market.py::test_invalid_as_of_date_raises_value_error[(1405, 13, 1)] PASSED                [ 24%]
src/tests/test_stage8_market.py::test_invalid_as_of_date_raises_value_error[(1405, 0, 1)] PASSED                 [ 25%]
src/tests/test_stage8_market.py::test_invalid_as_of_date_raises_value_error[(1405, 2, 0)] PASSED                 [ 26%]
src/tests/test_stage8_market.py::test_invalid_as_of_date_raises_value_error[(1405, 7, 31)] PASSED                [ 27%]
src/tests/test_stage8_market.py::test_invalid_as_of_date_raises_value_error[(0, 1, 1)] PASSED                    [ 28%]
src/tests/test_stage8_market.py::test_invalid_as_of_date_raises_value_error[(-1405, 2, 11)] PASSED               [ 29%]
src/tests/test_stage8_market.py::test_invalid_as_of_date_raises_value_error[(1405, 2)] PASSED                    [ 30%]
src/tests/test_stage8_market.py::test_invalid_as_of_date_raises_value_error[(1405, 2, 11, 0)] PASSED             [ 31%]
src/tests/test_stage8_market.py::test_invalid_as_of_date_raises_value_error[[1405, 2, 11]] PASSED                [ 32%]
src/tests/test_stage8_market.py::test_invalid_as_of_date_raises_value_error['1405-02-11'] PASSED                 [ 34%]
src/tests/test_stage8_market.py::test_invalid_as_of_date_raises_value_error[(1405, 2, '11')] PASSED              [ 35%]
src/tests/test_stage8_market.py::test_invalid_as_of_date_raises_value_error[(1405.0, 2, 11)] PASSED              [ 36%]
src/tests/test_stage8_market.py::test_invalid_as_of_date_raises_value_error[(True, 2, 11)] PASSED                [ 37%]
src/tests/test_stage8_market.py::test_invalid_as_of_date_raises_value_error[datetime.datetime(2026, 5, 1, 0, 0)] PASSED [ 38%]
src/tests/test_stage8_market.py::test_invalid_as_of_date_raises_value_error[None] PASSED                         [ 39%]
src/tests/test_stage8_market.py::test_invalid_observation_date_raises_value_error_even_if_row_is_later[(1405, 13, 1)] PASSED [ 40%]
src/tests/test_stage8_market.py::test_invalid_observation_date_raises_value_error_even_if_row_is_later[(1405, 0, 1)] PASSED [ 41%]
src/tests/test_stage8_market.py::test_invalid_observation_date_raises_value_error_even_if_row_is_later[(1405, 2, 0)] PASSED [ 42%]
src/tests/test_stage8_market.py::test_invalid_observation_date_raises_value_error_even_if_row_is_later[(1405, 7, 31)] PASSED [ 43%]
src/tests/test_stage8_market.py::test_invalid_observation_date_raises_value_error_even_if_row_is_later[(0, 1, 1)] PASSED [ 44%]
src/tests/test_stage8_market.py::test_invalid_observation_date_raises_value_error_even_if_row_is_later[(-1405, 2, 11)] PASSED [ 45%]
src/tests/test_stage8_market.py::test_invalid_observation_date_raises_value_error_even_if_row_is_later[(1405, 2)] PASSED [ 46%]
src/tests/test_stage8_market.py::test_invalid_observation_date_raises_value_error_even_if_row_is_later[(1405, 2, 11, 0)] PASSED [ 47%]
src/tests/test_stage8_market.py::test_invalid_observation_date_raises_value_error_even_if_row_is_later[[1405, 2, 11]] PASSED [ 48%]
src/tests/test_stage8_market.py::test_invalid_observation_date_raises_value_error_even_if_row_is_later['1405-02-11'] PASSED [ 50%]
src/tests/test_stage8_market.py::test_invalid_observation_date_raises_value_error_even_if_row_is_later[(1405, 2, '11')] PASSED [ 51%]
src/tests/test_stage8_market.py::test_invalid_observation_date_raises_value_error_even_if_row_is_later[(1405.0, 2, 11)] PASSED [ 52%]
src/tests/test_stage8_market.py::test_invalid_observation_date_raises_value_error_even_if_row_is_later[(True, 2, 11)] PASSED [ 53%]
src/tests/test_stage8_market.py::test_invalid_observation_date_raises_value_error_even_if_row_is_later[datetime.datetime(2026, 5, 1, 0, 0)] PASSED [ 54%]
src/tests/test_stage8_market.py::test_invalid_observation_date_raises_value_error_even_if_row_is_later[None] PASSED [ 55%]
src/tests/test_stage8_market.py::test_missing_or_gregorian_row_date_is_rejected_not_skipped PASSED               [ 56%]
src/tests/test_stage8_market.py::test_duplicate_jalali_dates_raise_value_error PASSED                            [ 57%]
src/tests/test_stage8_market.py::test_duplicate_dates_after_as_of_do_not_block_earlier_history PASSED            [ 58%]
src/tests/test_stage8_market.py::test_ordering_and_repeated_execution_are_deterministic PASSED                   [ 59%]
src/tests/test_stage8_market.py::test_prepare_rows_does_not_mutate_input PASSED                                  [ 60%]
src/tests/test_stage8_market.py::test_benchmark_uses_the_same_jalali_cutoff PASSED                               [ 61%]
src/tests/test_stage8_market.py::test_benchmark_order_does_not_matter_and_boundary_is_inclusive PASSED           [ 62%]
src/tests/test_stage8_market.py::test_invalid_or_duplicate_benchmark_dates_fail_closed[industry_benchmark] PASSED [ 63%]
src/tests/test_stage8_market.py::test_invalid_or_duplicate_benchmark_dates_fail_closed[market_benchmark] PASSED  [ 64%]
src/tests/test_stage8_market.py::test_missing_benchmark_data_keeps_insufficient_data_states PASSED               [ 65%]
src/tests/test_stage8_market.py::test_missing_close_is_not_converted_to_zero_price PASSED                        [ 67%]
src/tests/test_stage8_market.py::test_missing_adjusted_close_falls_back_to_close_without_zero_fill PASSED        [ 68%]
src/tests/test_stage8_market.py::test_missing_volume_and_value_do_not_change_price_indicators PASSED             [ 69%]
src/tests/test_stage8_market.py::test_benchmark_with_missing_price_is_not_zero_filled PASSED                     [ 70%]
src/tests/test_stage8_market.py::test_result_as_of_date_is_the_requested_jalali_date PASSED                      [ 71%]
src/tests/test_stage8_market.py::test_calculation_timestamp_is_separate_from_as_of_date PASSED                   [ 72%]
src/tests/test_stage8_market.py::test_market_signal_result_as_of_date_is_typed_as_jalali_date PASSED             [ 73%]
src/tests/test_stage8_market.py::test_indicator_results_match_direct_indicator_functions_on_ordered_prices PASSED [ 74%]
src/tests/test_stage8_market.py::test_windows_count_observations_not_calendar_days PASSED                        [ 75%]
src/tests/test_stage8_market.py::test_equivalent_ordered_sequences_with_different_date_labels_are_identical PASSED [ 76%]
src/tests/test_stage8_market.py::test_stage8_core_has_no_gregorian_date_contract PASSED                          [ 77%]
src/tests/test_stage8_market.py::test_missing_volume_and_value_fail_closed_and_are_not_zero_filled FAILED        [ 78%]
src/tests/test_stage8_market.py::test_market_regime_uses_close_fallback_when_adjusted_close_is_none FAILED       [ 79%]
src/tests/test_stage8_market_service.py::test_adapter_runs_real_query_into_engine_with_jalali_as_of PASSED       [ 80%]
src/tests/test_stage8_market_service.py::test_adapter_delegates_selection_to_existing_query PASSED               [ 81%]
src/tests/test_stage8_market_service.py::test_adapter_as_of_boundary_is_inclusive_and_future_rows_are_excluded PASSED [ 82%]
src/tests/test_stage8_market_service.py::test_adapter_as_of_before_all_rows_and_no_rows_are_insufficient_data PASSED [ 84%]
src/tests/test_stage8_market_service.py::test_adapter_isolates_company_identity PASSED                           [ 85%]
src/tests/test_stage8_market_service.py::test_engine_rows_preserve_identity_source_dates_and_none_values PASSED  [ 86%]
src/tests/test_stage8_market_service.py::test_adapter_does_not_zero_fill_or_invent_missing_prices PASSED         [ 87%]
src/tests/test_stage8_market_service.py::test_adapter_duplicate_company_date_fails_explicitly PASSED             [ 88%]
src/tests/test_stage8_market_service.py::test_adapter_rejects_invalid_as_of_dates[bad_date0] PASSED              [ 89%]
src/tests/test_stage8_market_service.py::test_adapter_rejects_invalid_as_of_dates[bad_date1] PASSED              [ 90%]
src/tests/test_stage8_market_service.py::test_adapter_rejects_invalid_as_of_dates[bad_date2] PASSED              [ 91%]
src/tests/test_stage8_market_service.py::test_adapter_rejects_invalid_as_of_dates[bad_date3] PASSED              [ 92%]
src/tests/test_stage8_market_service.py::test_adapter_rejects_invalid_as_of_dates[1405-02-11] PASSED             [ 93%]
src/tests/test_stage8_market_service.py::test_adapter_rejects_invalid_as_of_dates[None] PASSED                   [ 94%]
src/tests/test_stage8_market_service.py::test_adapter_rejects_history_of_another_company PASSED                  [ 95%]
src/tests/test_stage8_market_service.py::test_adapter_fails_explicitly_on_invalid_observation_date_from_query PASSED [ 96%]
src/tests/test_stage8_market_service.py::test_adapter_benchmarks_use_the_same_jalali_cutoff PASSED               [ 97%]
src/tests/test_stage8_market_service.py::test_adapter_repeated_execution_is_deterministic PASSED                 [ 98%]
src/tests/test_stage8_market_service.py::test_adapter_has_no_gregorian_conversion PASSED                         [100%]

====================================================== FAILURES =======================================================
__________________________ test_missing_volume_and_value_fail_closed_and_are_not_zero_filled __________________________

    def test_missing_volume_and_value_fail_closed_and_are_not_zero_filled():
        prices = list(range(1, 260))
        data = rows(prices)

        # Set volume and value to None in recent window
        for row in data[-5:]:
            row["volume"] = None
            row["value"] = None

>       result = MarketEngine().analyze_market(1, datetime(2026, 9, 16), data)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

src\tests\test_stage8_market.py:516:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\market\engine.py:64: in analyze_market
    as_of_date = validate_jalali_date(as_of_date, label="as_of_date")
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

value = datetime.datetime(2026, 9, 16, 0, 0), label = 'as_of_date'

    def validate_jalali_date(value: object, *, label: str) -> JalaliDate:
        """Return ``value`` unchanged if it is a valid ``JalaliDate``.

        Anything else (wrong container, non-``int`` parts including ``bool``,
        strings, or an impossible date) raises ``ValueError``.
        """
        if (
            not isinstance(value, tuple)
            or len(value) != 3
            or any(type(part) is not int for part in value)
        ):
>           raise ValueError(f"{label} must be a (year, month, day) integer tuple")
E           ValueError: as_of_date must be a (year, month, day) integer tuple

src\core\jalali.py:43: ValueError
_________________________ test_market_regime_uses_close_fallback_when_adjusted_close_is_none __________________________

    def test_market_regime_uses_close_fallback_when_adjusted_close_is_none():
        stock = rows(list(range(1, 260)))

        # Benchmark rows with adjusted_close = None and valid close
        benchmark = rows([x * 1.2 for x in range(1, 260)])
        for row in benchmark:
            row["adjusted_close"] = None

>       result = MarketEngine().analyze_market(
            1,
            datetime(2026, 9, 16),
            stock,
            market_benchmark=benchmark,
        )

src\tests\test_stage8_market.py:535:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\market\engine.py:64: in analyze_market
    as_of_date = validate_jalali_date(as_of_date, label="as_of_date")
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

value = datetime.datetime(2026, 9, 16, 0, 0), label = 'as_of_date'

    def validate_jalali_date(value: object, *, label: str) -> JalaliDate:
        """Return ``value`` unchanged if it is a valid ``JalaliDate``.

        Anything else (wrong container, non-``int`` parts including ``bool``,
        strings, or an impossible date) raises ``ValueError``.
        """
        if (
            not isinstance(value, tuple)
            or len(value) != 3
            or any(type(part) is not int for part in value)
        ):
>           raise ValueError(f"{label} must be a (year, month, day) integer tuple")
E           ValueError: as_of_date must be a (year, month, day) integer tuple

src\core\jalali.py:43: ValueError
=============================================== short test summary info ===============================================
FAILED src/tests/test_stage8_market.py::test_missing_volume_and_value_fail_closed_and_are_not_zero_filled - ValueError: as_of_date must be a (year, month, day) integer tuple
FAILED src/tests/test_stage8_market.py::test_market_regime_uses_close_fallback_when_adjusted_close_is_none - ValueError: as_of_date must be a (year, month, day) integer tuple
============================================ 2 failed, 92 passed in 3.24s