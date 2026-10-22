# P42 — Connect Jalali Market-Price Selection to the Valuation Boundary

You are continuing Stage 7 remediation in the local project directory `analyzer`. The GitHub repository is `analyzer`.

## Objective

P41 implemented and the user manually validated `select_market_price_as_of(...)`. The focused OHLC test file now passes 12/12 tests.

The remaining issue is that the selector is not connected to the valuation calculation. `ValuationEngine.calculate_valuation(...)` still accepts `current_price` and a Gregorian-typed `market_price_date`, while the imported market observations use Jalali date components.

Implement the smallest defensible production integration. Do not stop after documenting that no caller exists: inspect the relevant boundaries and implement a reusable, tested integration interface where the available contracts permit it.

## Mandatory operating constraints

- Work only in the local directory `analyzer`.
- No GitHub API/CLI, remote operations, push, pull, commits, or branch changes.
- Do not execute pytest, any test runner, CI, or application workflows. The user will run tests and provide actual output.
- You may inspect source code and test code statically.
- Do not edit `reply.md`, `temp_report.md`, `temp_report2.md`, `ClaudeReports/`, or `stepsForStage7.md`.
- Do not declare Stage 7 frozen.
- Do not invent financial values, benchmark P/E series, formulas, calendar conversions, or unsupported provenance claims.
- Preserve existing public-call compatibility and existing financial calculation behavior when the new integration inputs are not supplied.

## Inspect only the relevant code

1. `src/ingestion/market/queries.py`
2. `src/ingestion/market/__init__.py`
3. `src/models/market.py`
4. `src/valuation/engine.py`
5. `src/valuation/schema.py`
6. Existing real valuation callers and orchestration/service modules discovered by targeted symbol search for `calculate_valuation`.
7. `src/tests/test_ingestion_ohlc.py` and `src/tests/test_stage7_valuation.py`.

Do not perform a repository-wide audit.

## Required implementation

### A. Establish the actual integration boundary

Trace where a real company forecast, market-price data, and Stage 7 valuation can meet. Distinguish a real production caller from a test-only call or an unused helper.

### B. Connect the Jalali selector without fabricating dates

Use `select_market_price_as_of(session, company_id, as_of_jalali_date)` at an appropriate database/service boundary.

- The selected observation must belong to the requested company.
- Its Jalali source date must be on or before the requested Jalali as-of date.
- Preserve the selected price, `source_jalali_date`, `source`, `price_basis`, and `market_data_id`.
- Do not convert the Jalali date into a fabricated Gregorian `datetime`.
- Do not silently use a future, undated, invalid, or cross-company observation.
- If no eligible observation exists, follow an explicit fail-closed result/error policy. Never substitute an arbitrary price.
- If duplicate observations make selection ambiguous, preserve the selector's explicit error behavior.

### C. Provide a real reusable valuation integration interface

If an existing production caller can be safely connected, implement that connection.

If no suitable caller exists, implement the smallest reusable service/orchestration function at an appropriate existing service boundary that accepts the real database session, company identity, Jalali as-of date, forecast result, and other genuinely required valuation inputs. It should select the market observation and pass the selected price to Stage 7 without requiring a fabricated Gregorian date.

Preserve the existing `calculate_valuation` call contract. Prefer an additive interface or adapter over changing existing positional parameters.

Carry the source-date and provenance information into an auditable result or metadata field without falsely populating the existing Gregorian `market_price_date`. Ensure the resulting contract is unambiguous about whether the date is Jalali.

Do not invent benchmark P/E observations. If valuation cannot produce a complete result without existing benchmark inputs, keep that limitation explicit; do not claim full Forecast → Stage 7 → Stage 9 production integration unless the actual path is implemented and verified statically.

### D. Add focused tests

Add tests for the new integration boundary, reusing the existing OHLC selector tests where appropriate. At minimum cover:

- A valid selected observation reaches valuation with the selected price.
- The Jalali source date and all available provenance are preserved.
- A future-only or missing eligible observation cannot produce a valuation using a fabricated fallback price.
- Company identity is preserved and cross-company data cannot leak into valuation.
- The existing valuation call path remains compatible when the new optional integration is not used.
- No false Gregorian market date is emitted from a Jalali source date.
- Errors from ambiguous duplicate observations are not silently swallowed.

Use existing fixtures and conventions. Do not add redundant copies of existing selector tests.

If the existing architecture makes any requirement impossible without a larger interface decision, implement the safe reusable portion and identify the precise missing interface or dependency. Do not use that limitation as a reason to make no code changes at all.

## Financial and compatibility invariants

- No look-ahead: never select a price after the requested Jalali as-of date.
- No cross-company contamination.
- No fabricated or undated price fallback.
- Deterministic selection and explicit ambiguity handling.
- Preserve EPS supplied by Stage 5; do not recalculate it.
- Do not change valuation formulas, thresholds, weights, or benchmark policy.
- Do not claim complete point-in-time correctness: selecting a price by date alone does not prove when that observation became available to the system.

## Before responding

Statically inspect the changed files and diff. Do not run tests.

Report directly in your response, not in project reports:

1. Exact production files changed.
2. The new integration function's name and signature.
3. The actual caller connected, or the precise reason no production caller could be connected.
4. Exact test names added or updated.
5. Exact PowerShell commands for the narrowest relevant tests first, followed by any additional necessary test command.
6. Confirmation that you did not execute tests.
7. Any remaining production integration or point-in-time limitations.

Do not declare Stage 7 frozen. Stop after delivering the code changes, test commands, and limitations; wait for the user to run the tests and provide the output.