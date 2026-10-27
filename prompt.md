# Stage 7 — Prompt 1: Evidence-Based Audit

## TASK TYPE
**AUDIT ONLY + DOCS ONLY**

- Inspect the current repository state and produce an evidence-based audit.
- Do not create, modify, or delete application code or test files.
- Documentation changes are permitted only for `WORKFLOW_RULES.md` and `stepsForStage7.md`.
- Do not run tests, application code, database commands, or Git commands.
- Do not perform GitHub, remote, commit, branch, push, or pull operations. I will handle repository operations and run tests myself.

## PROJECT
Local project folder: `analyzer`

This is a financial-data application. Financial correctness, auditability, point-in-time (PIT) correctness, deterministic behavior, and preservation of financial invariants take priority over speed or superficially passing tests.

## REQUIRED FILES

Inspect these files first. Do not perform a repository-wide scan.

**Roadmap and specifications**
- `stepsForStage7.md`
- `07_Stage7_Valuation.md`
- `05_Stage5_Forecast_Engine.md`
- `temp_report2.md`
- `reply.md`

**Stage 7**
- `src/valuation/engine.py`
- `src/valuation/service.py`
- `src/valuation/parameters.py`
- `src/valuation/schema.py`
- `src/valuation/models.py`
- `src/tests/test_stage7_valuation.py`

**Stage 5 and Stage 3**
- `src/forecast/service.py`
- `src/forecast/schema.py`
- `src/scoring/engine.py`

**Stage 8 and market data**
- `src/market/engine.py`
- `src/market/service.py`
- `src/ingestion/market/queries.py`
- `src/tests/test_stage8_market.py`
- `src/tests/test_stage8_market_service.py`
- `src/tests/test_stage8_market_parameters.py`

**Stage 9 and database boundary**
- `src/decision/service.py`
- `src/decision/engine.py`
- `src/core/database.py`
- `src/tests/test_stage9_decision.py`

If a listed file does not exist, report that fact; do not silently substitute another file.

### Conditional files
Inspect additional files only when necessary to verify a specific interface or data path. Examples: relevant database models/repositories, service-interface tests, or actual application entrypoints. For every additional file, state its path and why it was necessary. Do not broaden the audit unnecessarily.

## AUDIT OBJECTIVES

1. Compare the actual source code and tests against the roadmap, specifications, and relevant reports. Treat reports as secondary evidence; current code and tests take precedence.
2. Produce an evidence-based gap matrix covering:
   - D7/D9 requirements and parameter consumption.
   - PIT correctness, Jalali-date handling, data provenance, and benchmark/market-price sourcing.
   - Alert and decision contracts.
   - Whether a real, source-verifiable Stage 3 → Stage 5 → Stage 7 → Stage 8 → Stage 9 execution path exists.
3. For every claimed defect or missing connection, identify the exact file and relevant function/class. Distinguish:
   - Confirmed defect.
   - Confirmed missing implementation or caller.
   - Unverified claim requiring more evidence.
   - Documentation/report inconsistency.
4. Check whether historical parameters are actually selected and used in calculations. Do not assume that parameter selection guarantees parameter consumption.
5. Verify whether real callers supply dates and data to each stage. The mere existence of a function or data model does not prove production integration.
6. Identify the minimum justified next implementation tasks for Prompt 2, with exact target files and regression-test requirements.
7. Keep the final redesign/review of `src/valuation/engine.py` reserved for the final Stage 7 bundle. Do not redesign it in this prompt.

## STRICT CONSTRAINTS

- Do not invent formulas, thresholds, effective dates, industry mappings, data sources, callers, or financial values.
- Do not create mock production paths merely to make integration tests pass.
- Preserve existing financial invariants and EPS handling.
- The application requires the Persian/Jalali calendar; do not introduce a Gregorian-calendar requirement.
- Do not change application code or tests.
- Do not run tests. Give me exact test commands to run later if needed.
- If evidence is insufficient, explicitly say so rather than guessing.

## DOCUMENTATION WORK

1. If `WORKFLOW_RULES.md` does not exist, create it with concise, durable project rules based on the constraints above and the authoritative roadmap. If it already exists, inspect it and make only necessary corrections.
2. Update `stepsForStage7.md` only if the audit establishes that a roadmap correction is necessary. Preserve valid existing decisions and completed-work evidence. Do not duplicate long reports or mark Stage 7 complete without evidence.
3. Do not modify `temp_report2.md`, `reply.md`, specifications, source code, or tests.

## REQUIRED OUTPUT

Return a concise report containing:

1. **Files inspected** and any additional files opened with the reason.
2. **Gap matrix**: issue, evidence (file/function/test), confidence/status, and recommended next action.
3. **Verified execution path**: confirmed links between stages and precisely identified missing or unverified links.
4. **Prompt 2 implementation scope**: exact files, intended changes, and required tests.
5. **Documentation changes**: exact files changed and the reason for each.
6. **Commands for me to run later**, if applicable. Do not execute them.

Stop after this audit and permitted documentation work. Do not begin Prompt 2 implementation.