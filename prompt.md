# P43 — Verify and Complete the Real Stage 7 → Stage 9 Integration

You are continuing Stage 7 remediation in the local project directory `analyzer`. The GitHub repository name is `lovelyroz/analyzer`.

## Operating rules

- Work locally only. Do not use GitHub, GitHub CLI/API, push, pull, commit, or remote operations. Do not change branches.
- Do not run pytest or CI. The user will run tests and provide the actual output.
- Do not edit `reply.md`, `temp_report.md`, `temp_report2.md`, `ClaudeReports/`, `stepsForStage7.md`, or `stage_7_prompts.md`.
- Do not scan the entire repository. Inspect only the relevant files listed below and follow imports/calls only when needed.
- Do not redesign or centralize `src/valuation/engine.py`.
- Preserve financial formulas, thresholds, weights, Stage 5 EPS, output contracts, and existing behavior unless a demonstrated defect requires a narrowly scoped correction.
- Do not invent financial data, date conversions, industry mappings, or PIT guarantees.
- Do not claim production integration is complete unless an actual callable path is established and tested.

## Confirmed P42 baseline

`src/valuation/service.py` now defines `calculate_valuation_as_of_jalali(...)`. It selects a persisted market price using `select_market_price_as_of(...)`, checks company and forecast-period identity, passes the selected price to Stage 7, and stores the Jalali date, selected source date, price basis, source, and market-data record ID in result metadata.

The user ran these tests successfully:
- Three focused P42 tests: each passed.
- `pytest src/tests/test_stage7_valuation.py`: **75 passed, 3 warnings**.

These results establish the tested service behavior, not end-to-end production integration.

## Files to inspect first

1. `src/valuation/service.py`
2. `src/ingestion/market/queries.py`
3. `src/ingestion/market/adapter.py`
4. `src/models/market.py`
5. `src/forecast/service.py`
6. `src/forecast/repo.py`
7. `src/decision/engine.py`
8. `src/decision/schema.py`
9. Relevant existing Stage 7, Stage 9, and market-ingestion tests only.

Trace the actual callable path and identify whether any existing application/service boundary invokes valuation and passes the result to Stage 9. Do not infer a caller from imports or from the existence of a new function.

## Task A — Establish the real integration boundary

Determine whether the existing application flow can supply all required inputs to:
1. generate or retrieve the correct persisted forecast;
2. select a market price using the requested Jalali as-of date;
3. calculate Stage 7 valuation;
4. pass the resulting `ValuationResult` into Stage 9 with its required existing inputs.

If a real, appropriate caller exists, connect it to `calculate_valuation_as_of_jalali` using the actual existing interfaces and data. Preserve existing callers and their behavior where possible.

If no suitable caller exists, do not fabricate missing inputs or claim end-to-end integration. Implement the smallest safe, reusable orchestration boundary that is supported by existing interfaces, with focused tests. Explicitly identify what still prevents a complete Stage 7 → Stage 9 production path.

## Task B — Validate the market-price selector

Review `select_market_price_as_of` in `src/ingestion/market/queries.py`.

The selector must:
- isolate the requested company;
- never select an observation after the requested Jalali date;
- deterministically select the latest eligible observation;
- preserve selected price and provenance;
- fail closed for missing prices and ambiguous duplicate observations;
- not assign or fabricate Gregorian dates.

Check whether stored rows with impossible Jalali calendar dates (for example, a day that does not exist in the given month) can pass the SQL component-range filters and be selected. Use the existing Jalali parser/calendar validation; do not implement a new calendar or Gregorian conversion. If a real defect exists, fix it narrowly and add focused regression tests. Do not change valid existing Jalali ingestion behavior.

## Required integration and regression coverage

Add only tests justified by the inspected interfaces. Cover as applicable:

- the actual caller invokes the Jalali valuation service;
- the selected market price is the price used by Stage 7;
- selected Jalali date and source provenance remain auditable;
- missing prices fail closed without silently using an unrelated or stale fallback;
- company and forecast-period identity mismatches are rejected;
- future market observations cannot affect an earlier as-of valuation;
- impossible Jalali dates cannot be selected;
- the resulting valuation reaches Stage 9 if a real supported caller exists;
- existing direct `ValuationEngine.calculate_valuation` callers remain compatible;
- Gregorian date fields are not populated with fabricated Jalali dates.

Do not duplicate tests that already establish these exact behaviors. Do not weaken or delete existing tests.

## Validation and reporting

After making changes, perform static inspection only. Do not run tests.

Report:
1. Exact files changed and why.
2. The actual caller and call path, with function names, if one exists.
3. Whether Stage 7 → Stage 9 is now genuinely connected or what precise blocker remains.
4. Tests added and the behavior each test proves.
5. Exact PowerShell commands for the user to run.
6. Confirmation that you did not run tests or CI.
7. Any remaining financial-correctness, date, provenance, or PIT limitations.

Do not declare Stage 7 frozen. Stop after providing the implementation summary and test commands; wait for the user's actual test output.


