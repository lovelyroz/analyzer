# P73 — Correct Missing-Data Handling in Stage 8



Read `stepsForStage7.md`, the P72 report in `temp_report2.md`, and the current implementations of:

- `src/market/engine.py`
- `src/market/indicators.py`
- `src/market/schema.py`
- `src/tests/test_stage8_market.py`
- `src/tests/test_stage8_market_service.py`



## Objective A — Stop zero-filling missing volume/value

In `src/market/engine.py`, the current conversion of missing volume and trading-value observations to `0.0` is inconsistent with the P72 data-integrity requirement.

Correct this without changing existing financial formulas, thresholds, or the meaning of indicator windows.

Requirements:

1. Preserve missing volume and value observations as missing internally.
2. Do not pass synthetic zeroes into volume or trading-value indicators.
3. For a metric whose required observation window contains missing values, return its established missing-data result (`None` for a numeric metric or `INSUFFICIENT_DATA` for its corresponding state), rather than computing a misleading result from zero-filled or silently incomplete data.
4. Respect the existing observation-count windows. Do not introduce a new lookback window, minimum-sample threshold, or financial threshold.
5. Keep price calculations unchanged.
6. Review volume ratio, average volume, average trading value, trading-value stability, liquidity state, and any related alerts so missing data cannot be misclassified as zero activity.
7. Add focused tests for missing volume and missing value in relevant windows. Assert that missing values are not treated as zero and that dependent metrics/states fail closed as specified.

Do not modify `src/market/indicators.py` unless necessary. If a change there is unavoidable, explain why and keep it narrowly scoped.

## Objective B — Make market-regime price fallback consistent

In `_market_regime`, use `adjusted_close` when it is not `None`; otherwise fall back to `close`, matching the established `_price` behavior.

Do not fall back when the adjusted close is an actual numeric value. Do not invent prices or change regime thresholds.

Add a regression test where benchmark rows have `adjusted_close=None` and valid `close` values. Verify that the regime calculation uses those close values and matches the expected existing formula. Also preserve behavior when both prices are missing.

## Strict exclusions

- Do not change the Jalali date contract or introduce Gregorian conversion.
- Do not change valuation formulas, Stage 5 EPS, Stage 7 parameters, alert thresholds, or unrelated stages.
- Do not edit `src/valuation/engine.py`.
- Do not add dependencies, persistence, or orchestration.
- Do not edit `stepsForStage7.md` or `temp_report2.md`.
- Do not run tests, launch the application, run database commands, or execute migrations.
- Do not run Git commands or perform Git/GitHub operations.

## Final review and report

Inspect the changed files and diff without Git commands. Report:

1. Exact files changed.
2. How missing volume/value now affect each dependent metric and state.
3. The `_market_regime` fallback correction.
4. Tests added and exact commands for the owner to run.
5. Any remaining uncertainty or unresolved behavior.
6. Explicit confirmation that tests were not run and no Git commands were used.

Do not claim the fixes are verified until the owner runs the tests. Keep the changes limited to these two defects.