# P74 - Consolidated completion (replaces all earlier P74 text in this file)

Earlier P74 reports in this file claimed the engine already used the shared validators and that tests had been added; inspection showed neither was true of the source at that time. Those statements, and the pasted pytest outputs that belonged to the earlier code, are removed. Nothing below claims a test result.

## 1. Exact changed files
- `src/market/engine.py` (source)
- `src/tests/test_stage8_market.py` (8 old P74 tests replaced by 28 test functions)
- `src/tests/test_stage8_market_service.py` (5 test functions appended)
- `P74.diff` (new, `diff -u`, covers exactly the three files above, relative to the uploaded archive)
- `temp_report2.md`, `reply.md` (documentation)

Unchanged: `src/market/schema.py` (already holds the finite validators), `indicators.py`, `service.py`, `src/valuation/engine.py`, all other stages.

## 2. Shared validation flow in the production engine
`MarketEngine.analyze_market`:
1. `validate_jalali_date` on `as_of_date`; `_prepare_rows` on primary data (dates, cutoff, duplicates).
2. For each of `industry_benchmark` / `market_benchmark`, if supplied: `_prepare_rows`, then `MarketEngine._price(row)` on every in-cutoff row. This happens before the insufficient-data early return.
3. Primary prices: `MarketEngine._price(row)` = `adjusted_close` unless `None`, else `close`; both `None` returns `None` (missing); any supplied value goes through `schema._price` (finite and > 0, else `ValueError`).
4. Volume and value: `schema._number` directly (`None` stays `None`, `0` stays valid, NaN/inf/non-numeric raise `ValueError`).
5. Early return only now if there are no rows or a price is missing; all of 2-4 have already run.
6. `_relative_strength` and `_market_regime` read benchmark prices via the same `_price(row)` adapter, so they reject non-finite prices even when called directly.

`analyze_market_signals` (legacy) feeds closes into `analyze_market`, so they take the same path.

## 3. Service boundary (`src/market/service.py`)
`market_history_to_engine_rows` copies `MarketHistoryObservation` attributes verbatim: no conversion, filtering, or zero-fill; `None` stays `None`; Decimals pass through unchanged. A non-finite value on an observation therefore reaches the engine and is rejected there. The test `test_adapter_maps_non_finite_values_verbatim_without_filtering_or_zero_fill` asserts identity of the values.

## 4. Tests added and what each proves
`test_stage8_market.py` (helper constants: non-finite floats, numeric strings `"NaN"`, `"inf"`, `"+inf"`, `"-inf"`, `"Infinity"`, `" nan "`, and `Decimal` NaN/inf; message patterns pin the numeric path):
- `test_shared_number_and_price_reject_non_finite_values`, `..._reject_zero_and_negative_values`, `..._reject_non_numeric_values`, `test_shared_validators_keep_none_zero_and_finite_values`: the shared contract (None, zero, finite, numeric strings/Decimal).
- `test_primary_non_finite_price_is_rejected_anywhere_in_the_series`: `close` (as consumed price) and `adjusted_close` x NaN/+inf/-inf/strings/Decimals, at the last and first row (first row is outside every indicator window).
- `test_primary_non_finite_price_is_rejected_when_data_is_insufficient`: same with 1, 3 and 20 rows.
- `test_primary_zero_and_negative_prices_are_rejected`, `test_primary_non_numeric_prices_are_rejected`.
- `test_close_is_not_consumed_when_adjusted_close_is_present`: documents the real contract; a NaN `close` is not read when a valid `adjusted_close` exists.
- `test_missing_price_is_missing_not_invalid`: `None` gives `INSUFFICIENT_DATA`; the same row with NaN/inf raises.
- `test_adjusted_close_fallback_to_valid_close_is_unchanged_by_validation` (P73 behavior).
- `test_legacy_analyze_market_signals_rejects_non_finite_close`.
- `test_non_finite_volume_or_value_is_rejected_independently`: volume and value tested separately (other field valid), first and last row.
- `test_non_finite_volume_or_value_is_rejected_when_data_is_insufficient`, `test_volume_and_value_are_validated_before_the_missing_price_early_return`.
- `test_non_numeric_volume_or_value_is_rejected_not_silently_missing`, `test_none_volume_or_value_stays_missing_while_non_finite_is_rejected`, `test_genuine_zero_volume_or_value_is_a_valid_observation` (0, 0.0, "0", Decimal 0), `test_finite_numeric_strings_decimals_and_ints_are_converted_not_rejected` (result equals the float baseline).
- `test_non_finite_benchmark_price_is_rejected_independently`: industry and market benchmark, `close`/`adjusted_close`, first/last row, other benchmark valid and absent; uses the real keyword arguments.
- `test_non_finite_benchmark_is_rejected_even_when_primary_data_is_insufficient` (empty, all-after-as-of, missing last price, 3-row primary; 5-row benchmark) plus control `test_valid_benchmark_with_insufficient_primary_data_does_not_raise` which asserts `INSUFFICIENT_DATA`, proving the early-return path is the one exercised.
- `test_zero_and_negative_benchmark_prices_are_rejected`, `test_non_numeric_benchmark_price_is_rejected`.
- `test_regime_and_relative_strength_cannot_consume_non_finite_benchmark_prices`: calls `_market_regime` and `_relative_strength` directly.
- `test_benchmark_none_prices_are_missing_not_invalid`.
- `test_non_finite_rows_after_the_as_of_cutoff_are_not_consumed` and `test_non_finite_future_primary_row_is_validated_when_point_in_time_is_disabled`: scope of validation relative to point-in-time.

All P73 tests (fallback, missing volume/value windows, regime fallback) are left untouched. Each rejection test fails if the engine falls back to `float()` / the swallowing `_number`, because NaN/inf then pass through silently.

`test_stage8_market_service.py`:
- `test_adapter_maps_non_finite_values_verbatim_without_filtering_or_zero_fill`.
- `test_adapter_non_finite_observation_value_is_rejected_by_the_engine`: `close_price`, `adjusted_close`, `volume`, `value` x Decimal/float NaN/inf, through `analyze_market_as_of_jalali` (query result substituted by `MarketHistoryObservation` objects, same pattern as existing tests).
- `test_adapter_non_finite_benchmark_price_is_rejected_with_real_history`: in-memory DB history, bad benchmark.
- `test_adapter_non_finite_benchmark_is_rejected_even_without_company_history`: empty history (early-return path).
- `test_adapter_zero_and_missing_volume_and_value_remain_valid_observations`.

## 5. Behavior changes and limitations
- Supplied zero/negative/non-numeric prices now raise. Non-numeric volume/value (e.g. `"abc"`) used to become `None` silently and now raises.
- `open`, `high`, `low`, `trade_count` are not consumed by the engine and are not validated. Benchmark volume/value are not consumed and not validated.
- `close` is validated only when it is the consumed price. Rows after the as-of cutoff are not validated (they are not consumed) unless `point_in_time=False`.
- Legacy `individual_buy_vol` / `individual_sell_vol` are only compared and are not validated.
- Negative volume/value is not rejected (no such rule in the shared `_number`).
- Not verified: whether the database can store or return NaN/inf (model, query and `parameters`/`jalali` sources were not in the archive). Service tests prove the adapter-to-engine boundary only, not database behavior.
- No test, application, database or Git command was run by the assistant. Only syntax parsing (`ast.parse`) was done.

## 6. Commands for the project owner
```
pytest src/tests/test_stage8_market.py src/tests/test_stage8_market_service.py src/tests/test_stage8_market_parameters.py
pytest src/tests/test_stage8_market.py -k "non_finite or zero_and_negative or non_numeric or insufficient" 
```
Review the change with `P74.diff` (unified diff produced with `diff -u`, not Git).

(analyzer) PS D:\winprojects\analyzer> pytest src/tests/test_stage8_market.py src/tests/test_stage8_market_service.py src/tests/test_stage8_market_parameters.py
================================================= test session starts =================================================
platform win32 -- Python 3.12.9, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\winprojects\analyzer
collected 772 items

src\tests\test_stage8_market.py ................................................................................ [ 10%]
................................................................................................................ [ 24%]
................................................................................................................ [ 39%]
................................................................................................................ [ 53%]
................................................................................................................ [ 68%]
................................................................................................................ [ 82%]
........................................................................                                         [ 92%]
src\tests\test_stage8_market_service.py ..........................................................               [ 99%]
src\tests\test_stage8_market_parameters.py ..                                                                    [100%]

================================================= 772 passed in 5.67s =================================================
(analyzer) PS D:\winprojects\analyzer> pytest src/tests/test_stage8_market.py -k "non_finite or zero_and_negative or non_numeric or insufficient"
================================================= test session starts =================================================
platform win32 -- Python 3.12.9, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\winprojects\analyzer
collected 712 items / 109 deselected / 603 selected

src\tests\test_stage8_market.py ................................................................................ [ 13%]
................................................................................................................ [ 31%]
................................................................................................................ [ 50%]
................................................................................................................ [ 68%]
................................................................................................................ [ 87%]
...........................................................................                                      [100%]

========================================= 603 passed, 109 deselected in 3.23s