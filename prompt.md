# P72 — Implement Native Jalali Date Contract for Stage 8

You are working in the local project folder `analyzer`.

This is a financial-data application. Financial correctness, point-in-time (PIT) integrity, auditability, deterministic behavior, and preservation of existing financial invariants take priority over speed.

## 1. Required context

Before editing, read:

- `stepsForStage7.md`
- The latest P71 report in `reply.md`
- `src/market/engine.py`
- `src/market/schema.py`
- `src/market/indicators.py`
- `src/ingestion/market/queries.py`
- `src/models/market.py`
- `src/ingestion/market/ingestion.py`
- `src/ingestion/market/adapter.py`
- `src/tests/test_market_history_query.py`
- `src/tests/test_stage8_market.py`
- `src/tests/test_stage9_decision.py`
- `src/tests/test_stage789_service_interface.py`

Inspect any additional direct caller or constructor that must change to preserve the contract. Do not perform a broad repository exploration.

Use the actual source files in the current `analyzer` snapshot. Do not rely on stale reports where they conflict with current source.

## 2. Authoritative design decision

Implement the native Jalali contract established in P71.

The public Stage 8 date contract must be consistent across the engine, its input rows, its output schema, and its database adapter.

- `JalaliDate` is a tuple `(year, month, day)` of integers.
- The market as-of date and every market or benchmark observation date use this same Jalali contract.
- Engine rows use `jalali_date`, not a Gregorian `"date"` field.
- Never construct or infer a Gregorian `datetime` from Jalali components.
- `MarketSignalResult.as_of_date` must represent the Jalali as-of date.
- `calculation_timestamp` remains a separate execution timestamp; it must not be substituted for the market as-of date.
- Existing in-repository callers must migrate deliberately to the new contract. Do not silently support ambiguous mixed-calendar comparisons.
- Existing `20D`, `252D`, and similar indicator windows retain their current observation-count semantics. Do not reinterpret them as calendar-day intervals.

If the repository already has an appropriate shared Jalali-date utility or type module, reuse it. Otherwise, introduce the smallest suitable shared definition and validation implementation without creating circular imports or making the market engine depend unnecessarily on the ingestion layer. Avoid duplicated, inconsistent validation logic.

## 3. Implementation scope

### A. `src/market/schema.py`

- Change `MarketSignalResult.as_of_date` to the agreed `JalaliDate` type.
- Keep `calculation_timestamp` separate and retain its existing meaning.
- Update metadata typing or representation only as required by the contract.

### B. `src/market/engine.py`

Migrate the public Stage 8 engine and its internal date-dependent helpers to native Jalali dates.

This includes, where applicable:

- `MarketEngine.analyze_market`
- `_prepare_rows`
- `_relative_strength`
- `_market_regime`
- `analyze_market_signals`
- Any other internal code that filters, orders, or serializes market observation dates.

Requirements:

1. Validate the as-of date and observation dates using the shared contract.
2. Apply an inclusive as-of boundary: retain observations with `jalali_date <= as_of_date`; exclude later observations.
3. Sort deterministically by Jalali date. If a secondary ordering key is required, use a real, stable key already available in the source data; do not invent one.
4. Reject duplicate observation dates for the same company or benchmark series with `ValueError`, consistent with the existing history-query contract. Do not silently deduplicate.
5. Reject or fail closed on invalid dates. Do not substitute the current date or manufacture a fallback date.
6. Apply the same date validation, cutoff, and ordering contract to benchmark observations.
7. Preserve existing missing-value behavior. Do not convert missing OHLCV values to zero or invent replacement prices.
8. Preserve existing market-data quality states and `INSUFFICIENT_DATA` behavior unless a narrowly required correction is demonstrated by source evidence.
9. Represent date provenance in metadata explicitly as Jalali, for example with a calendar identifier and the Jalali as-of tuple. Do not serialize a Jalali tuple as though it were a Gregorian ISO date.
10. Preserve the existing numerical indicator algorithms and their semantics. Do not modify `src/market/indicators.py` unless the new contract demonstrably requires it; if so, explain why in the report.

Review `analyze_market_signals` carefully. It must not create fake Gregorian-dated rows. Migrate it to the Jalali contract or remove/replace an obsolete compatibility path only if all actual callers are updated and the change is justified.

### C. Add a Stage 8 database adapter

Create a minimal service or adapter in the most appropriate existing location, preferably `src/market/service.py` if that matches repository conventions.

Its responsibility is to connect the real history query to the Stage 8 engine:

`select_market_history_as_of(...)` → validated Jalali engine rows → `MarketEngine.analyze_market(...)`

Requirements:

- Use the existing `select_market_history_as_of` query rather than reimplementing its filtering or database access.
- Respect the existing caller-owned SQLAlchemy `Session` pattern.
- Preserve company identity and the source observation dates.
- Map only fields actually provided by `MarketHistoryObservation`; do not invent OHLCV values, benchmark data, or dates.
- Preserve `None` for missing source values.
- Do not add Gregorian conversion.
- Do not add persistence, a new application entry point, or full-pipeline orchestration in this task.
- If the query result cannot satisfy the engine contract, fail explicitly rather than silently creating synthetic observations.

Inspect the actual observation schema before implementing the mapping. Do not assume field names based only on this prompt.

### D. Update all affected in-repository callers and tests

Update:

- `src/tests/test_stage8_market.py`
- `src/tests/test_stage9_decision.py`
- `src/tests/test_stage789_service_interface.py`
- Any additional directly affected caller or constructor found during the scoped inspection.
- Existing query tests only if the shared type or validator refactor requires it.

Do not weaken or delete existing assertions simply to make the migration pass.

Add focused tests for the database adapter and the new date contract. Include, at minimum:

1. The as-of boundary is inclusive.
2. Observations after the as-of date are excluded.
3. An as-of date before all observations produces the established empty-data behavior.
4. Invalid Jalali dates fail with `ValueError`.
5. Duplicate Jalali dates fail with `ValueError`.
6. Ordering and repeated execution are deterministic.
7. Benchmark observations use the same Jalali cutoff.
8. Missing benchmark data preserves the established `INSUFFICIENT_DATA` behavior.
9. Missing OHLCV values are not converted to zero.
10. `MarketSignalResult.as_of_date` equals the requested Jalali as-of date.
11. `calculation_timestamp` remains separate from the as-of date.
12. Equivalent ordered price/volume sequences preserve the existing numerical indicator results.
13. The adapter preserves company identity and source Jalali dates.
14. No ambiguous Gregorian `"date"` contract remains in the Stage 8 core or in migrated in-repository callers.

Use the actual project conventions and existing test fixtures. Do not fabricate database records as production data; synthetic data is acceptable inside isolated unit tests.

## 4. Strict exclusions

Do not:

- Edit `src/valuation/engine.py`.
- Change Stage 5 EPS or recompute EPS in Stage 7.
- Change financial formulas, thresholds, alert contracts, or valuation parameters.
- Introduce a new Gregorian conversion policy.
- Change the Stage 8 observation-count meaning of indicator windows.
- Implement the complete orchestrator or decide how Stage 9 results will be persisted.
- Add new dependencies unless indispensable and explicitly justified.
- Run tests, launch the application, run database commands, or execute migrations.
- Run Git commands or make any Git/GitHub remote, branch, commit, push, or pull changes.
- Edit `stepsForStage7.md` or append to `reply.md`.
- Claim that tests pass when they have not been run.

## 5. Final verification without executing tests

After editing, inspect the changed files and review the diff directly without using Git commands.

Check for:

- Remaining datetime comparisons in the Stage 8 market-date path.
- Remaining construction of synthetic Gregorian dates.
- Mismatched signatures and outdated `MarketSignalResult` constructors.
- Circular imports or duplicated Jalali validation.
- Accidental changes to financial formulas, indicator behavior, or unrelated stages.
- Incomplete adapter mapping or missing tests.

Do not execute the tests. The repository owner will run them locally.

## 6. Required report

Return a concise but evidence-based report containing:

1. Files changed and the purpose of each change.
2. The final public Jalali date contract.
3. How the database adapter connects the existing query to the engine.
4. How invalid, duplicate, future, and missing observations are handled.
5. All in-repository callers migrated.
6. Tests added or updated, with exact commands the owner should run.
7. Any unresolved issue, with the exact file/function and evidence.
8. Confirmation that tests were **not run** and that no Git commands were used.

Do not claim end-to-end integration is complete. This task is limited to the native Jalali Stage 8 contract and its database adapter.

The implementation must be complete within this scope; do not leave known, in-scope contract mismatches unresolved.