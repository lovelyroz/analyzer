# P71 — Finalize the Stage 8 Jalali Date Contract (Read-Only)

You are reviewing the financial-data project in the local folder `analyzer`.

## Objective

Produce a final, implementation-ready contract proposal for Stage 8 date handling, based on P69 and P70 and the exact current `analyzer.zip`.

The technical direction is to prefer native Jalali date handling over inventing Gregorian dates. Your task is to specify the complete contract and identify compatibility risks, not to reopen the investigation from scratch.

## Required context

1. Read `stepsForStage7.md`, P69, and P70 in `reply.md`.
2. Verify the relevant current source in the supplied ZIP, particularly:
   - `src/market/engine.py`
   - `src/market/schema.py`
   - `src/ingestion/market/queries.py`
   - `src/models/market.py`
   - `src/tests/test_stage8_market.py`
   - `src/decision/service.py`
   - all other actual callers or consumers of `MarketSignalResult.as_of_date`, `analyze_market`, and `analyze_market_signals`.
3. Do not trust prior reports when the source can be checked directly.

## Proposed direction to evaluate

Use an explicit Jalali date contract for Stage 8:
- One documented Jalali date type, consistent with the existing `JalaliDate` tuple contract where appropriate.
- Market observation dates and the market as-of boundary use the same calendar and comparison semantics.
- The engine does not fabricate Gregorian `datetime` values from Jalali components.
- `MarketSignalResult.as_of_date` must accurately represent the approved date contract.
- `calculation_timestamp`, if retained as an execution timestamp, remains semantically distinct from the market as-of date.
- Industry and market benchmark rows must follow an explicit compatible date contract. Do not silently mix Jalali and Gregorian dates.

These are design constraints to evaluate and refine against the actual source, not authorization to change code.

## Tasks

### 1. Establish the complete public contract

Specify exact proposed types and meanings for:
- the Stage 8 as-of input;
- each market row's date field;
- industry and market benchmark row dates;
- `MarketSignalResult.as_of_date`;
- date values in metadata;
- `calculation_timestamp`.

Clarify inclusive as-of filtering, chronological ordering, duplicate-date handling, and invalid or missing dates. Do not invent calendar rules.

### 2. Determine backward-compatibility requirements

Identify all current callers and tests that supply `datetime` values or consume `MarketSignalResult.as_of_date`.

Recommend the safest migration strategy:
- a deliberate breaking change with all in-repository callers updated;
- or a temporary, explicitly documented compatibility layer, only if it can avoid ambiguous mixed-calendar comparisons.

Do not retain dual-mode support merely to avoid changing tests. Do not break known callers silently. If external callers cannot be discovered, state that limitation explicitly.

### 3. Define benchmark behavior

Specify what must be true of benchmark dates and the as-of boundary.

Do not invent benchmark sources or values. If benchmark observations are absent, preserve the engine's existing insufficient-data semantics. Do not claim that relative-strength or market-regime results are valid without the required data.

### 4. Provide a file-by-file implementation plan

For every proposed file change, explain:
- the exact function, field, or contract to change;
- why the change is necessary;
- expected impact on callers;
- tests required to demonstrate correctness.

Preserve existing financial calculations and observation-count window semantics such as `20D` and `252D`; do not reinterpret them as calendar-day windows.

Include tests for:
- Jalali as-of boundary inclusion and exclusion;
- chronological ordering and deterministic output;
- invalid and missing dates;
- duplicate dates;
- benchmark date alignment;
- missing OHLCV without zero-filling;
- `MarketSignalResult` provenance;
- compatibility or intentional migration of existing callers;
- unchanged indicator results for equivalent ordered price sequences.

### 5. Decide whether implementation can begin

End with one of:
- **Ready for implementation**, if the contract is fully specified from existing evidence;
- **Blocked**, with only the exact unresolved decisions that genuinely require owner approval.

Do not ask the owner to decide details that follow directly from the established project requirements and source behavior. Clearly separate a necessary owner decision from an implementation detail that the engineering plan can resolve.

## Strict restrictions

- Read-only. Do not edit code, tests, specifications, or reports.
- Do not run tests, the application, database commands, or Git commands.
- Do not invent Jalali-to-Gregorian conversion rules, historical dates, benchmarks, or financial formulas.
- Do not change `src/valuation/engine.py`.
- Preserve Stage 5 EPS and all Stage 7 financial/PIT constraints.
- Do not claim end-to-end integration or PIT correctness beyond the evidence.
- Do not modify `reply.md`.

## Required output

Return a concise but technically complete report with:
1. verified current contracts and source references;
2. the finalized proposed date contract;
3. compatibility analysis;
4. exact implementation sequence and test plan;
5. explicit implementation readiness status.

This is the final design review before any Stage 8 date-contract code changes. No implementation in this task.