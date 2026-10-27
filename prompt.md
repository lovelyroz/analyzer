# P74 Consolidated Completion — Stage 8 Numeric Validation, Regression Tests, and Review Evidence

You are working locally in the `analyzer` project.

P74 has been reported as complete multiple times, but repository inspection still shows unresolved discrepancies between the report, implementation, and tests. This task is to complete and verify the entire P74 work package in one pass—not to produce another report-only update.

## A. Mandatory initial inspection

Inspect the current versions of these files before editing:

- `src/market/engine.py`
- `src/market/schema.py`
- `src/market/indicators.py`
- `src/market/service.py`
- `src/tests/test_stage8_market.py`
- `src/tests/test_stage8_market_service.py`
- `temp_report2.md`
- `reply.md`
- `P73.diff`, if present

Do not rely on previous reports as proof that the source code was changed. Inspect the actual implementation.

## B. Complete the shared numeric-validation implementation

1. Ensure the production `MarketEngine` path uses the shared numeric validation functions in `src/market/schema.py`, without shadowing them with duplicate unvalidated implementations.

2. Preserve the existing row-based `_price(row)` interface where needed by the engine:
   - Use `adjusted_close` when it is not `None`.
   - Otherwise fall back to `close`.
   - Preserve missing-price handling where the existing contract requires it.
   - Reject non-finite supplied prices and reject zero or negative prices according to the shared price-validation contract.

3. Ensure the production `_number` path for volume and trading value rejects `NaN`, positive infinity, and negative infinity. Preserve `None` as missing data and genuine zero values as valid observations.

4. Audit every actual Stage 8 consumption path for:
   - Primary market prices.
   - Volume.
   - Trading value.
   - Industry benchmark prices.
   - Market benchmark prices.

5. Validate supplied benchmark numeric values before an insufficient-primary-data early return can bypass benchmark validation. A malformed benchmark must not escape validation merely because the primary series is too short to calculate indicators.

6. Confirm that `_relative_strength` and `_market_regime` cannot consume non-finite benchmark prices. Avoid unnecessary duplicate validation logic and preserve the existing price fallback behavior.

7. Do not claim that opening, high, or low prices are validated by the engine unless the actual implementation consumes or explicitly validates them. Report the real contract accurately.

## C. Correct and strengthen the regression tests

Update `src/tests/test_stage8_market.py` so the tests prove numeric validation rather than passing for unrelated reasons.

Required conditions:

- Use the required `jalali_date` field and valid Jalali tuples throughout these tests.
- Use a valid Jalali `as_of_date`.
- Do not use a malformed Gregorian `"date"` key in a test intended to prove numeric rejection.
- Do not catch `TypeError` and retry a different benchmark argument. Use the actual supported `analyze_market` signature.
- Use valid primary market data when testing benchmark validation.
- Include cases that reach validation even when the available data is insufficient for full indicator calculations.

Add or correct tests for all of the following:

1. Primary `close` and `adjusted_close` inputs containing `NaN`, `+inf`, and `-inf`.
2. Volume and trading-value inputs containing non-finite values, tested independently.
3. Industry benchmark and market benchmark prices containing non-finite values, tested independently.
4. Numeric strings representing non-finite values where the contract accepts numeric strings for conversion.
5. Finite-value controls and genuine zero controls.
6. Missing values (`None`) remaining distinct from invalid non-finite numbers.
7. Existing P73 behavior, including adjusted-close fallback and missing volume/value handling.

Ensure each test would fail if the production validation were removed or bypassed. The test's expected `ValueError` must arise from the numeric-validation path, not from an invalid date, wrong argument, or unrelated setup error.

## D. Review the Stage 8 service boundary

Inspect `src/market/service.py` and the existing service tests to establish how database/history observations reach `MarketEngine`.

- Determine whether numeric values are transformed, filtered, or silently discarded before reaching the engine.
- Check whether any conversion could hide a non-finite value or turn missing data into zero.
- If a real service-to-engine path can carry non-finite values, add focused service-level regression coverage using the existing test fixtures and in-memory database conventions.
- Do not invent database schema changes or synthetic production pathways.
- Do not claim that service-level validation is proven unless a test actually exercises that path.

## E. Preserve financial and project invariants

Do not change:

- Financial formulas.
- Existing thresholds.
- Observation-window sizes or their boundaries.
- Point-in-time filtering semantics.
- The Jalali-only date contract.
- P73's intended missing-data and fallback behavior.

Do not redesign `src/valuation/engine.py`, modify unrelated stages, or declare Stage 7 complete.

## F. Produce reviewable evidence

After making the source and test changes:

1. Create or update `P74.diff` as a normal unified diff of the actual P74 source/test changes. Do not use Git commands. Ensure the diff reflects the real edited files rather than a hand-written description.
2. Update `temp_report2.md` with a concise, evidence-based P74 report.
3. Update `reply.md` with:
   - Exact changed files.
   - The shared validation flow through the production engine.
   - The specific tests added and what each proves.
   - Any remaining limitations or unverified paths.
   - The exact local test commands for the project owner.
4. Remove or correct earlier P74 statements that contradict the final implementation. Do not merely append another claim of completion while leaving inaccurate claims uncorrected.

## G. Execution restrictions

- Do not run tests.
- Do not run application or database commands.
- Do not run Git commands or access GitHub/remotes.
- The project owner will run tests locally and review the diff.
- Do not claim that tests passed unless the project owner supplies actual execution results.

## Required completion response

Return one consolidated report identifying the actual changed files, the validation and service-path findings, the test coverage, the diff artifact, and the exact commands the owner should run.

Do not stop after editing documentation. Do not report P74 as complete if the source implementation or regression tests remain incomplete.