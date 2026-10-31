# Stage 7 — Resolve Decision Contracts and Complete Production-Path Audit

## Work Classification

**Documentation updates + repository architecture audit only.**

**NO Python code changes.**  
**NO model, schema, migration, database, or test changes.**  
**DO NOT execute tests.**  
**DO NOT run application code.**  
**DO NOT perform Git operations, commits, pushes, pulls, or branch changes.**

The user runs all tests locally. This task is limited to examining source, documenting approved architectural decisions, and recording verifiable findings.

Repository: `lovelyroz/analyzer`  
Default branch: `master`

## 1. Required Files

Read these files before making any change:

### Stage 7 governing documents
- `STAGE7_MASTER_WORKING_PACKET.md`
- `WORKFLOW_RULES.md`
- `07_Stage7_Valuation.md`
- `reply.md`

### Database and ingestion
- `src/core/database.py`
- `src/ingestion/service.py`
- `src/ingestion/market/queries.py`

### Stage 2–5
- `src/kpi/engine.py`
- `src/kpi/schema.py`
- `src/trend/engine.py`
- `src/trend/schema.py`
- `src/scoring/engine.py`
- `src/scoring/schema.py`
- `src/forecast/service.py`
- `src/forecast/queries.py`
- `src/forecast/schema.py`

### Stage 7–9
- `src/market/service.py`
- `src/market/engine.py`
- `src/market/schema.py`
- `src/valuation/parameters.py`
- `src/valuation/engine.py`
- `src/valuation/service.py`
- `src/valuation/schema.py`
- `src/decision/service.py`
- `src/decision/engine.py`
- `src/decision/schema.py`

### Relevant tests — inspect only; do not execute
- `src/tests/test_stage789_service_interface.py`
- `src/tests/test_stage9_decision.py`

You may identify additional files only when a direct import, call reference, application startup declaration, or entrypoint reference demonstrates that the file is necessary. For every additional file, report its exact path and why it was required.

For the production-entrypoint audit, inspect the repository root and `src/` for actual application startup files, CLI commands, web handlers, scheduled jobs, or other production callers. Do not conduct unrelated repository-wide exploration.

## 2. Task 029 — S7-T007: D9/PIT and Dated Parameters

Document the following approved architectural decisions:

1. Stage 7 V1 parameter registry is version-controlled in code. Do not introduce a database-backed analytical parameter registry.
2. Parameter versions must have genuine, evidence-backed effective dates before they can participate in historical as-of selection.
3. Never invent or backdate `effective_from`.
4. The undated Genesis snapshot must not be selected as a historical version.
5. Missing historical parameter versions must fail closed. Never silently substitute today's parameters.
6. Historical backtests may only use authentic parameter vintages and authentic point-in-time input evidence. Do not fabricate historical versions.
7. All output-affecting parameters, including weights, thresholds, sensitivity rules, and rounding/precision rules, must be tied to an immutable model version. A material change requires a new model version.
8. Do not approve the numerical Genesis values merely because they currently exist in source code. Their financial calibration remains unresolved until supported by valid evidence.

### Historical Forward P/E provenance contract

Document the minimum conceptual requirements for every observation:

- Same-company identity.
- Jalali observation date.
- Relevant financial period identity.
- Underlying financial and market source references.
- Source/version/revision identity where applicable.
- Actual publication or availability timestamp, when required to establish what was knowable at the analysis cutoff.
- A traceable relationship between the historical EPS and market-price observations used to derive the P/E.

The caller/provider supplies source provenance. Stage 7 must validate the supplied evidence and reject or fail closed when required provenance is absent or invalid.

A Jalali observation date alone does not prove publication/availability timing. Do not claim full PIT without that evidence.

### Task status

Do not mark S7-T007 DONE merely because the policy is documented. Distinguish:
- Architectural decisions now resolved.
- Historical parameter vintages still unavailable.
- Source-level provenance and runtime validation still requiring implementation/evidence.

Use PARTIAL or BLOCKED as appropriate and explain why.

## 3. Task 030 — S7-T008: Alert and Input Contracts

Document these decisions:

1. D1–D5 remain deferred and inactive in V1. Do not invent triggers, formulas, thresholds, severity levels, or missing-data behavior.
2. D6 remains limited to the currently documented EPS and TARGET_PE drivers. Do not invent sector-specific formulas or industry mappings.
3. D7 requires actual temporal provenance. No full PIT claim may be made from observation dates alone.
4. D8 uses the currently documented engine alert vocabulary as the canonical V1 vocabulary. Do not invent aliases or new alert tokens.
5. OA1.5 and OA1.6 remain required active behaviors and must be implemented under their existing execution tasks (S7-T015 and S7-T016). Do not treat documentation of these requirements as implementation.
6. A missing eligible market price remains fail-closed.
7. A selected older market-price observation must be reported with its actual Jalali date; it must not be silently represented as the analysis-date price.

Inspect the relevant specification sections and actual engine/service output. Identify any real mismatch between the approved contract and implementation. Do not change code.

### Task status

S7-T008 may be marked DONE only if its decision/contract scope is fully documented and the audit finds no unresolved contract-definition work inside this Task. OA1.5/OA1.6 implementation remains in their separate Tasks.

If any contract or consumer behavior remains unverified, retain PARTIAL/BLOCKED and explain the exact missing evidence.

## 4. Task 031 — S7-T009: Actual Production Path and Stage 9 Architecture

Perform a bounded, source-based audit.

Establish whether a real production execution path connects:

- Stage 1 source/input data
- Stage 2 KPI calculation
- Stage 3 fundamental scoring
- Stage 4 trend evidence
- Stage 5 Forecast generation
- Stage 7 Valuation
- Stage 8 market analysis
- Stage 9 Decision

Trace actual callers, not merely exported functions or package imports.

Specifically establish:

1. The actual application entrypoint, if one exists.
2. The real caller of `generate_and_persist_forecast`, if any.
3. The real producer/caller of `FundamentalScoringEngine.calculate_score`.
4. The real producer/caller of `MarketEngine` / `analyze_market_as_of_jalali`.
5. Whether `calculate_decision_as_of_jalali` has a production caller.
6. Who creates and owns the SQLAlchemy Session.
7. Whether one Session is passed through the relevant services.
8. How company identity, financial period identity, and Jalali as-of date are selected and propagated.
9. Whether Stage 5, Stage 3, and Stage 8 results are actually produced by upstream production services or merely supplied by an external caller.
10. How the Stage 9 runtime result is returned to its actual consumer.
11. Whether any code attempts to persist Stage 9 analytical output. Such persistence is prohibited by owner rule R-05.

### Important distinction

The existence of `src/decision/service.py` does not prove a complete production path.

The existence of `src/tests/test_stage789_service_interface.py` does not prove an end-to-end production path. Inspect its fixtures and helpers to identify which upstream results are constructed or supplied by the test.

Do not describe a test-created `CompanyForecastResult`, `FundamentalScoreResult`, or `MarketSignalResult` as a real production-generated result.

### If no full production path exists

Do not create an orchestrator, entrypoint, service, or test.

Instead, document:

- The exact existing service boundaries.
- The missing production caller or orchestration boundary.
- The missing Session ownership/lifecycle decision, if applicable.
- Which stage outputs currently need to be supplied externally.
- The exact architectural work required before a real E2E test can exist.
- Why a mock-based test cannot close this gap.

Task 031's acceptance permits a completed audit that conclusively records the architecture gap and the exact decisions/work required. Do not confuse completion of the audit with completion of the production path.

## 5. Master Packet Updates

Update `STAGE7_MASTER_WORKING_PACKET.md` only where required to record the decisions and verified findings above.

At minimum:

- Update Task 029 and Task 030 descriptions/statuses to distinguish resolved policy from remaining implementation/evidence.
- Update Task 031 based on the completed production-path audit.
- Update dashboard entries C-03, C-04, and C-05.
- Update R5–R9/D7 Task references only where the decisions above genuinely resolve their acceptance criteria.
- Keep numerical Genesis approval unresolved.
- Keep Task 032 blocked if a real production path is not established.
- Keep Task 033 blocked until its dependencies are satisfied.
- Keep Task 034 open.
- Preserve all existing Task numbers and permanent IDs.
- Do not mark implementation or E2E tasks DONE based on documentation.

Do not modify unrelated Task packages, particularly Forecast persistence remediation Tasks 053–057.

## 6. Stage 7 Specification Updates

Update `07_Stage7_Valuation.md` only where its current statements conflict with verified facts or the decisions above.

In particular, inspect the existing D9 statements that claim the parameter registry/version-selection mechanism does not exist. The current source contains a Parameter Registry and effective-date selection mechanism. Correct stale descriptions without claiming that historical parameter data or full PIT is now available.

Update D7/D8 wording only to reflect the decisions above. Preserve historical notes with clear HISTORICAL/SUPERSEDED labels where needed.

Do not modify formulas, numerical parameters, financial thresholds, or active code.

## 7. Reporting

Append a detailed report to `reply.md`. Do not overwrite its existing Task 053 report.

The report must include:

- Work classification and explicit confirmation of no code changes.
- Exact files examined.
- Exact additional files examined and reasons.
- For every relevant finding, exact file path, function/class, and line references.
- Actual call graph, if one exists.
- Session ownership and lifecycle evidence.
- Production caller evidence or a documented search result showing the missing caller.
- Clear distinction between real production calls and test-only calls.
- Decisions recorded for Tasks 029 and 030.
- Status for each of:
  - 029 · S7-T007
  - 030 · S7-T008
  - 031 · S7-T009
- Any affected R5–R9/D7 Task statuses, with reasons.
- Exact documentation files and sections changed.
- Remaining blockers and their dependencies.
- Confirmation that no tests were executed.
- Confirmation that no code, models, migrations, or tests were changed.

Use the exact permanent Task IDs. Do not omit or rename any requested Task.

## 8. Final Restrictions

- Do not execute tests.
- Do not modify Python source.
- Do not modify ORM models or migrations.
- Do not modify tests.
- Do not invent production callers, data sources, financial formulas, dates, parameter values, or provenance.
- Do not claim full PIT or E2E without direct evidence.
- Do not change unrelated documentation or Task packages.
- If a required file is unavailable, report its exact path and stop short of conclusions that depend on it.