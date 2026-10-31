# Package 3 — Real Production Execution Path and Stage Integration

Repository: `lovelyroz/analyzer`

## Execution classification

**REPORT-ONLY + MASTER PACKET DOCUMENTATION UPDATE**

- Do not modify application code.
- Do not create or modify tests.
- Do not execute tests or any commands.
- Do not create a synthetic orchestrator, entrypoint, dependency-injection layer, or substitute E2E pipeline.
- The only permitted file modification is the explicitly authorized status/evidence update to `STAGE7_MASTER_WORKING_PACKET.md`.
- Do not create a separate report file.

## 1. Objective

Investigate whether the repository currently contains a genuine production execution path connecting:

1. Stage 1 — persisted financial source data
2. Stage 3 — Fundamental Scoring
3. Stage 4 — Historical Trend
4. Stage 5 — Forecast
5. Stage 8 — Market Analysis
6. Stage 7 — Valuation
7. Stage 9 — Final Decision

The investigation must establish the actual application entrypoint, caller chain, input ownership, SQLAlchemy Session ownership and lifecycle, and runtime transfer of stage outputs.

The required outcome is one of:

- **PROVEN:** A genuine production execution path exists and can be traced through the relevant source code.
- **NOT PRESENT / BLOCKED:** The exact missing production component(s) are identified with source evidence.

Do not treat the existence of individual service functions as proof of an integrated production pipeline.

## 2. Required files

You may inspect only the following explicitly supplied files.

### A. Authoritative workflow and Stage 7 records

- `STAGE7_MASTER_WORKING_PACKET.md`
- `WORKFLOW_RULES.md`

### B. Stage specifications

- `03_Stage3_Fundamental_Scoring.md`
- `04_Stage4_Historical_Trend.md`
- `05_Stage5_Forecast_Engine.md`
- `07_Stage7_Valuation.md`
- `08_Stage8_Market_Engine.md`
- `09_Stage9_Decision_Dashboard.md`

### C. Application entrypoint and Session infrastructure

- `src/core/database.py`
- `src/scripts/init_db.py`
- `src/scripts/migrate_db.py`
- `src/ingestion/service.py`

### D. Stage execution and data boundaries

- `src/kpi/engine.py`
- `src/kpi/schema.py`
- `src/trend/engine.py`
- `src/trend/schema.py`
- `src/scoring/engine.py`
- `src/scoring/schema.py`
- `src/forecast/service.py`
- `src/forecast/queries.py`
- `src/forecast/schema.py`
- `src/market/service.py`
- `src/market/schema.py`
- `src/ingestion/market/queries.py`
- `src/valuation/service.py`
- `src/valuation/schema.py`
- `src/decision/service.py`
- `src/decision/schema.py`

### E. Existing integration and production-path test evidence

- `src/tests/test_stage1_database_architecture.py`
- `src/tests/test_stage3_scoring.py`
- `src/tests/test_stage4_trend.py`
- `src/tests/test_stage5_forecast.py`
- `src/tests/test_stage789_service_interface.py`
- `src/tests/test_stage8_market_service.py`
- `src/tests/test_stage9_decision.py`

If another file is necessary, do not inspect it automatically. Report its exact path and why it is necessary, then stop and request authorization.

Do not perform repository-wide exploration.

## 3. Required investigation tasks

### Task 031 · S7-T009 — Revalidate the production execution-path audit

The Master Packet already records this audit as DONE, based on the earlier finding that no complete production entrypoint was found.

Do not repeat a broad repository audit.

Revalidate the previous conclusion against the supplied current source files. Determine whether any genuine production caller or application entrypoint has appeared that changes the earlier finding.

Required evidence:

- Exact entrypoint path and callable/function name, if present.
- Exact caller-to-callee chain.
- Evidence that the caller is part of an actual application execution path, not a test or an isolated library service.
- Evidence showing where Stage 1 data is obtained and how it reaches subsequent stages.
- Evidence showing how Stage 3, Stage 4, Stage 5, Stage 8, Stage 7 and Stage 9 outputs are produced and transferred.

If no new evidence changes the previous finding, retain DONE for Task 031 as a completed audit. Do not interpret DONE as proof that a production pipeline exists.

### Task 032 · S7-T010 — Determine whether a genuine E2E test is possible

Establish whether the repository contains an actual production path that can be exercised by an end-to-end integration test.

Inspect the existing `test_stage789_service_interface.py` carefully.

Distinguish between:

- A real service-to-service handoff.
- A test that supplies upstream results itself.
- A genuine production-path E2E test.

An in-memory database does not automatically make a test synthetic. However, manually constructing Forecast, Fundamental and Market results inside the test does not prove that the application produces those results through its actual production execution path.

If the production entrypoint or required upstream callers do not exist, Task 032 must remain BLOCKED.

Do not write an alternative test to conceal the missing production path.

### Task 036 · S7-PLAN-002 — Establish execution-path and Session lifecycle evidence

Trace the actual ownership and lifecycle of the SQLAlchemy Session.

Answer these questions with source evidence:

1. Where is the Session created?
2. Which application component owns it?
3. Who closes it?
4. Who controls transaction boundaries?
5. Do stage services receive an existing Session or create one?
6. Are commits or rollbacks performed inside individual services?
7. Is there a single production caller that coordinates the relevant stages?
8. How are company identity, financial period identity and Jalali analysis date propagated?
9. How does the Stage 5 Forecast result reach Stage 7?
10. How do Stage 3 Fundamental and Stage 8 Market results reach Stage 9?
11. Does the final Decision result return to an actual application/UI caller?

For each stage, identify:

- Input producer.
- Input source.
- Execution function.
- Output type.
- Actual caller.
- Session dependency.
- Output consumer.

Use a compact execution matrix.

Do not assume that `SessionLocal` being defined establishes Session lifecycle ownership.

Do not assume that a service accepting `Session` establishes a production caller.

### Task 020 · S7-TEST-004 — Decide whether real E2E testing can be performed

This task is dependent on proof of the actual production execution path.

If a real path exists:

- Identify the exact callable that the E2E test must exercise.
- Identify the actual data/input requirements.
- Identify the actual Session lifecycle.
- Specify the narrowest valid test location and exact proposed test command.
- Do not implement or execute the test in this package.

If no real path exists:

- Keep this task BLOCKED.
- State exactly which production component is missing.
- Explain why existing unit, mock and service-integration tests cannot replace it.

## 4. Financial and architectural safeguards

The following constraints are mandatory:

- Do not invent financial inputs, provenance, dates, company identity or period identity.
- Do not manufacture Forecast, Fundamental or Market results to simulate production.
- Do not use test fixtures as evidence of production data flow.
- Do not introduce Gregorian date substitutions for Jalali analysis dates.
- Do not claim full Point-in-Time correctness merely because a service accepts a cutoff or as-of date.
- Do not introduce persistence for analytical outputs.
- The application database stores source inputs/raw source data only, according to the owner's approved architecture.
- Do not introduce a new Session owner or transaction policy based on assumption.
- Do not modify `src/forecast/service.py` or its persistence behavior in this package. Forecast persistence remediation is tracked separately under Tasks 053–057.
- Do not redesign any stage or change financial formulas.

## 5. Reporting requirements

Report each task separately, preserving the exact identifiers:

- 031 · S7-T009
- 032 · S7-T010
- 036 · S7-PLAN-002
- 020 · S7-TEST-004

For every task include:

1. Status: DONE, PARTIAL, NOT DONE, or BLOCKED.
2. Exact source files and functions inspected.
3. Concrete evidence supporting the status.
4. What the evidence proves.
5. What it does NOT prove.
6. Remaining dependency or missing component, if any.

Include a final execution-path matrix and one explicit conclusion:

**Either the genuine production execution path to Stage 9 is proven, or the exact missing production component(s) are identified.**

Do not use ambiguous language such as "mostly integrated", "production-ready", or "E2E available" without source-level proof.

## 6. Master Packet update

Update only `STAGE7_MASTER_WORKING_PACKET.md`.

- Preserve all existing decisions and historical evidence.
- Do not overwrite unrelated task statuses.
- Keep Task 031 DONE if the audit remains complete.
- Keep Task 032 BLOCKED if a real production path is absent.
- Update Task 036 based on the actual evidence.
- Keep Task 020 BLOCKED unless a genuine production E2E path is proven and the test is actually completed by the user.
- Update the relevant dashboard entry.
- Clearly distinguish a completed audit from a completed implementation.
- Do not mark any BLOCKED task as DONE.

No other files may be modified.

## 7. Prohibited actions

- No test execution.
- No command execution.
- No code modifications.
- No new tests.
- No synthetic orchestration.
- No repository-wide search.
- No inspection of files outside the supplied list.
- No Git commit, push, pull, branch or remote operations.

Return the complete task-by-task report and the exact proposed test command only if a genuine production path is proven.