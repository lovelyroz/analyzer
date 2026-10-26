# P70 — Stage 8 Jalali Date Contract Feasibility Audit (Read-Only)

You are reviewing the financial-data project in the local folder `analyzer`.

## Objective

Resolve the technical feasibility questions behind P69 decision D-A: how Stage 8 can consume persisted market history using the project's Jalali date contract without introducing an unsupported Gregorian conversion or weakening point-in-time correctness.

This is a read-only investigation. Do not implement a solution yet.

## Authoritative context

1. Read `stepsForStage7.md` first, then the latest P68-B and P69 reports in `reply.md`.
2. Inspect the exact current `analyzer.zip` supplied for this task. Verify relevant source files directly; do not rely solely on earlier reports or a potentially stale workspace.
3. The current audit reports that:
   - `src/ingestion/market/queries.py` defines `MarketHistoryObservation` and `select_market_history_as_of(...)`.
   - The query returns original Jalali date components and does not convert them to Gregorian dates.
   - `src/market/engine.py` currently accepts `as_of_date: datetime` and market rows represented as dictionaries with a `date` field.
   - No production adapter connecting the history query to `MarketEngine.analyze_market` has been demonstrated.
4. The project requires Jalali/Shamsi calendar support. Do not assume Gregorian conversion is acceptable or invent a conversion policy.
5. Preserve all Stage 7 rules, especially financial correctness, deterministic behavior, PIT limitations, and preservation of Stage 5 EPS.

## Investigation tasks

### 1. Verify the actual date and data contracts

Inspect the relevant definitions and callers in at least:

- `src/ingestion/market/queries.py`
- `src/models/market.py`
- `src/market/engine.py`
- `src/market/indicators.py`
- `src/market/schema.py`
- `src/tests/test_market_history_query.py`
- `src/tests/test_stage8_market.py`
- any existing market-ingestion code that writes `MarketDaily` dates

Record the exact source fields and types used for:
- Jalali year/month/day;
- `trade_date`, including its nullability and actual write behavior;
- `MarketHistoryObservation`;
- `MarketEngine.as_of_date`;
- the market-row `date` field;
- any industry or market benchmark date handling.

Do not assume that `trade_date` contains a valid or authoritative date merely because the field exists.

### 2. Trace how dates are actually used inside Stage 8

Follow `as_of_date` and each market row's date through the engine and its helper methods.

Determine whether dates are used only for filtering and provenance or whether calculations depend on Gregorian datetime semantics, timezone behavior, calendar-day differences, or benchmark alignment.

Identify every function that would need consideration if the engine were to accept Jalali dates directly.

### 3. Compare the feasible architecture options

Evaluate these options against the actual source code:

A. Adapt the persisted Jalali history to the existing datetime-based engine using an already-existing, authoritative date source, but only if the source and semantics are proven.

B. Modify the Stage 8 input contract so the engine and all relevant helpers can work with Jalali date components directly.

C. Another minimal approach, but only if supported by existing project contracts.

For each option, explain:
- which files and functions would need changes;
- whether it preserves a consistent as-of boundary;
- whether it can correctly handle benchmarks;
- how it treats missing `trade_date` and missing OHLCV;
- risks to determinism, historical correctness, and existing callers;
- what contract decision or additional evidence is still needed.

Do not select an option merely because it requires fewer code changes. Do not introduce a parallel date convention without justification.

### 4. Identify the safest recommendation

Recommend one option only if the evidence supports it. Otherwise, identify the precise unresolved question that prevents a safe decision.

Distinguish clearly between:
- verified current behavior;
- conclusions directly supported by source;
- proposed design;
- unresolved owner decisions.

Do not implement the adapter, change the engine, add tests, or edit specifications during this audit.

## Strict restrictions

- Read-only: no code, test, specification, or report edits.
- Do not run tests, the application, database commands, or Git commands.
- Do not invent Jalali-to-Gregorian conversion rules, dates, trading calendars, lookback windows, minimum sample counts, fallback prices, or benchmark data.
- Do not create synthetic observations to make the interface work.
- Do not claim full PIT correctness from a cutoff alone.
- Do not redesign `src/valuation/engine.py`.
- Do not repeat the claim that the market-history query is missing unless the supplied snapshot genuinely differs and direct source evidence proves it.
- Do not claim end-to-end integration has been verified.

## Required report

Return a concise but evidence-based report containing:

1. Exact snapshot and files inspected.
2. Current date contracts and actual date usage, with file/function references.
3. Comparison of options A, B, and C.
4. One recommendation, if justified, and why.
5. Exact unresolved decisions, if any.
6. Exact files likely to change in a later implementation and the contract tests required.
7. A clear statement of whether implementation can safely begin.

Return the report in your response for review. Do not modify `reply.md` or any repository file. Do not begin implementation.