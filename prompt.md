# P67 — Stage 7 Implementation Batch: Market Data Contract, Stage 8–9 Integration Readiness, and Safe Contract Fixes

You are working in the local project folder `analyzer`.

This is an implementation task, not a report-only audit. Use the current repository state and the latest findings recorded in `reply.md`, especially P66, together with `stepsForStage7.md` and `07_Stage7_Valuation.md`.

## 1. Mandatory operating constraints


- Do not run tests, the application, migrations, database initialization, or other execution commands. I will run tests myself.
- You may inspect source code and existing tests, modify implementation code, and add or update tests.
- Do not modify `stepsForStage7.md`, `07_Stage7_Valuation.md`, `reply.md`, or other planning/report files.
- Do not redesign or consolidate `src/valuation/engine.py`. Its redesign remains the final technical step of Stage 7.
- Do not invent financial data, schemas, model fields, database tables, industry mappings, thresholds, date policies, or parameter effective dates.
- Preserve Jalali market-date contracts and existing public interfaces unless a specific incompatibility is demonstrated.
- Never weaken or remove tests merely to obtain a passing result.
- Continue with independent, safe tasks if another task is blocked. Clearly distinguish implemented changes from findings and blockers.

## 2. Work package A — Establish the actual Stage 8 market-data contract

Inspect only the files necessary to trace the existing market-data path, including:

- `src/market/engine.py`
- `src/decision/service.py`
- `src/decision/engine.py`
- the existing market ORM models, repositories, and query functions
- `src/valuation/service.py` and the existing `MarketDaily` query path, where relevant
- relevant market and decision tests

Determine, using actual source definitions:

1. What market data is stored, in which tables/models, and with what date, symbol/company, and OHLCV fields?
2. Is there an existing repository or query that can provide the historical sequence required by `MarketEngine.analyze_market`?
3. Can the data be filtered to the requested company/instrument and as-of date without using future observations?
4. What date type and calendar does the market engine expect, and how does that compare with the persisted market-data contract?
5. What minimum input is required by `calculate_decision_as_of_jalali`, and which parts of its input must be prepared by its caller?

Do not treat the existence of `MarketDaily` as proof that it contains all the fields or history required by Stage 8. Verify the schema and actual query semantics.

## 3. Work package B — Implement only the real, bounded Stage 8 connection

If the existing schema and query paths provide sufficient evidence, implement the smallest compatible market-data service or repository integration needed to load the existing historical data and produce the `MarketSignalResult` expected by Stage 9.

Requirements:

- Reuse established models, repositories, session ownership, and date conventions.
- Filter records according to the actual as-of-date contract. Do not include observations after the requested date.
- Handle missing or insufficient market history using existing documented behavior. Do not invent financial fallback values or signals.
- Preserve existing service and result contracts unless a demonstrated defect makes a narrow correction necessary.
- Add focused tests for the real query/filtering contract, date boundary, missing data, and transfer of the resulting market signal to the existing decision service, as applicable.
- Use the existing test fixtures and models rather than synthetic production infrastructure.

If the source schema or date semantics are insufficient to implement this safely, do not create a speculative service. Instead, identify the exact missing field, source, or contract and explain the smallest prerequisite needed. Continue with work packages C and D.

## 4. Work package C — Verify and correct clear Stage 7/8/9 contract defects

Use P66 findings and the actual code to review the relevant service boundaries and tests.

- Verify the actual inputs and outputs for Stage 5 → Stage 7 and Stage 8 → Stage 9.
- Check that missing market data, invalid date ranges, or unavailable signals are handled consistently with existing contracts.
- Check that errors are not silently converted into fabricated market signals or financial outputs.
- Review whether the current decision-service orchestration passes through the actual Stage 7 result and supplied Stage 8 result without unintended replacement or recalculation.
- Review warning names and output channels only where an actual code-level inconsistency and its consumer impact can be demonstrated.
- Correct clear, specification-backed defects and add regression tests.
- Do not rename public warning tokens or alter output structures without checking known consumers and proving the required migration.

Do not build a new application entry point, general orchestrator, persistence model for final decisions, or new database schema as part of this batch. Those require a separately proven contract and must not be invented to make integration tests look complete.

## 5. Work package D — Preserve and test the approved V1 policies

Inspect existing tests and implementation for D1–D6. Add or correct focused regression tests where coverage is genuinely missing and the expected behavior is explicit.

- D1: Do not emit `ASSESSMENT_FLIP_RISK` without an approved, valid criterion.
- D2: Do not activate the unwired multiple-dependence threshold or invent a dependency formula.
- D3: Preserve Stage 5 EPS; do not recalculate EPS or introduce an unapproved EPS-dependence warning.
- D4: Do not emit margin-assumption risk without valid required inputs.
- D5: Keep `review_priority` separate from risk alerts.
- D6: Preserve the current EPS/target-P/E valuation contract; do not invent sector-specific formulas or mappings.

Keep the P61 scenario-dispersion behavior unchanged: preserve the existing `0.50` thresholds and strict `>` comparison semantics. Do not attempt to unify independent thresholds without an approved policy.

Do not force changes where existing implementation and tests already correctly enforce the policy. State which cases are already covered and which received new coverage.

## 6. Work package E — Verify and report test readiness

Without running any tests or application commands:

- Inspect the changed code and tests for consistency.
- Check imports, signatures, fixture usage, date types, and compatibility with existing callers by source inspection.
- List every changed file and explain its purpose.
- Provide exact PowerShell-compatible test commands for me to run.
- Separate focused tests from broader regression tests.
- Do not report any test as passed, and do not claim runtime behavior was verified.

Use the project virtual environment when giving commands if necessary. Do not assume the system Python has the project dependencies installed.

## 7. Required final report

Return a concise but evidence-based report with these headings:

1. **Implementation Summary**
2. **Market Data Contract — Verified Facts**
3. **Changes Made and Files Changed**
4. **Stage 8–9 Connection Status**
5. **D1–D6 Regression Coverage**
6. **Remaining Blockers and Exact Missing Contracts**
7. **PowerShell Test Commands for Owner Execution**
8. **Execution Confirmation**

For each claimed fix, identify the relevant file/function and the corresponding test added or updated. Explicitly state if the Stage 8 connection remains unimplemented because the necessary source contract is missing.

Confirm that no tests or application commands were executed and no Git or remote operations were performed.

## Acceptance criteria

This batch must produce real implementation/test progress wherever existing contracts support it, without fabricating data or architecture. If a safe connection cannot yet be built, the result must narrow the unresolved issue to concrete missing evidence or contract details. Stage 7 remains OPEN until the roadmap’s full exit criteria are met.