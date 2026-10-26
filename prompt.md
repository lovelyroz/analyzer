# P74 — Reject or Fail Closed on Non-Finite Stage 8 Market Inputs

You are working in the local project folder `analyzer`, a financial-data application where correctness, auditability, deterministic behavior, and preservation of financial invariants take priority over convenience.

## Required reading

Read:
- `stepsForStage7.md`
- The P72 and P73 sections of `temp_report2.md`
- `src/market/engine.py`
- `src/market/schema.py`
- `src/tests/test_stage8_market.py`
- `src/tests/test_stage8_market_service.py`

## Objective

Inspect and correct the handling of non-finite numeric values in Stage 8 market inputs, specifically `NaN`, positive infinity, and negative infinity.

P73 addressed `None` values but explicitly left `NaN` unresolved. Do not assume that converting a value with `float()` makes it valid financial data.

### A. Establish explicit behavior

Inspect how `_number`, `_price`, market benchmark processing, and dependent calculations handle non-finite values.

Define and implement a consistent, fail-safe policy:

- Non-finite prices must never enter price-derived calculations as valid observations.
- Non-finite optional volume and trading-value observations must never be treated as genuine numeric observations or silently converted to zero.
- Non-finite benchmark prices must never distort relative-strength or market-regime results.
- Missing or invalid optional observations must not produce misleading volume, liquidity, or alert outputs.
- Preserve the distinction between a genuine numeric zero and missing or invalid data.

Follow existing contracts and error-handling conventions. Do not introduce silent row dropping if it would conceal invalid source data. Where the current contract does not clearly determine whether to raise an error or fail closed, report the ambiguity rather than inventing a broader policy.

### B. Regression tests

Add focused tests covering `NaN`, positive infinity, and negative infinity for:
- Primary price observations
- Optional volume and trading-value observations
- Benchmark price observations
- Dependent indicators and alerts

Include boundary cases and verify that ordinary finite values and genuine zeros retain their existing behavior.

### C. Strict exclusions

- Do not change financial formulas, thresholds, observation windows, or alert names.
- Do not change the Jalali date contract or add Gregorian conversion.
- Do not modify `src/valuation/engine.py`, Stage 5 EPS, Stage 7 valuation parameters, or `src/market/indicators.py` unless a specific, unavoidable dependency is demonstrated and reported before expanding scope.
- Do not change unrelated modules, dependencies, database schemas, or migrations.
- Do not run tests, the application, database commands, or Git commands. The project owner runs tests locally.

## Final report

Report:
1. The exact files changed and why.
2. The selected behavior for each non-finite input category.
3. Tests added and the exact commands the owner should run.
4. Any ambiguity or remaining limitation.
5. Explicitly state that tests were not run.

Keep the changes narrowly scoped and preserve all valid P73 behavior.