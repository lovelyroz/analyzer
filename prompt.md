# P054–057 — Remove Forecast Output Persistence and Preserve Runtime Integration

**Repository:** `lovelyroz/analyzer`  
**Local project folder:** `analyzer`  
**Work type:** CODE-CHANGING + TEST AUTHORING + DATABASE MIGRATION DESIGN  
**Execution environment:** Local project files only

## 1. Mission

Implement the owner's approved R-05 / OA1.7 architecture across all four tasks:

- **054 · S7-T026** — Remove the production Forecast persistence write path.
- **055 · S7-T027** — Remove Forecast output persistence tables from the active database schema through a safe forward-only migration.
- **056 · S7-T028** — Replace persistence-oriented tests with strong no-persistence and runtime-contract regression tests.
- **057 · S7-T029** — Audit and preserve the actual runtime Forecast consumer path, including Stage 6 and Stage 7.

These four tasks form one coordinated change. Do not implement them as disconnected edits.

## 2. Authoritative architecture — non-negotiable

The owner has explicitly decided:

1. The application database stores raw source inputs and input data only.
2. Stage 5 Forecast outputs are generated at runtime.
3. Bear / Base / Bull outputs are consumed by downstream stages in memory.
4. No Forecast output, scenario record, Forecast version, or output-dependent provenance record may be persisted in application database tables.
5. No alternative history store, cache, or persistence mechanism may be introduced to replace the removed database persistence.
6. Runtime provenance and PIT evidence must remain available where required by downstream consumers.
7. Raw source inputs, normalized source facts, ReportVersion data, share history, and other input-side records must remain intact.
8. Forecast formulas, financial calculations, model parameters, scenario calculations, and financial invariants must not change as part of this task.

The corrected Stage 5 contract in `05_Stage5_Forecast_Engine.md` and OA1.7 in `07_Stage7_Valuation.md` are the governing policy.

## 3. Required files — inspect only these supplied files

All files listed below must be present in the supplied local `analyzer` project folder or ZIP.

### A. Governance and contracts — READ-ONLY

1. `STAGE7_MASTER_WORKING_PACKET.md`
2. `05_Stage5_Forecast_Engine.md`
3. `07_Stage7_Valuation.md`

### B. Stage 5 source — implementation scope

4. `src/forecast/__init__.py`
5. `src/forecast/service.py`
6. `src/forecast/schema.py`
7. `src/forecast/repo.py`
8. `src/forecast/adapter.py`
9. `src/forecast/builder.py`
10. `src/forecast/drivers.py`
11. `src/forecast/engine.py`
12. `src/forecast/queries.py`

### C. Models, database, and migration

13. `src/models/forecast.py`
14. `src/models/entity.py`
15. `src/models/normalized.py`
16. `src/models/normalized_provenance.py`
17. `src/models/period.py`
18. `src/models/report.py`
19. `src/models/share_action.py`
20. `src/core/database.py`
21. `src/migrations/runner.py`
22. `src/scripts/init_db.py`
23. `src/scripts/migrate_db.py`

### D. Downstream runtime consumers — READ-ONLY unless a directly necessary contract adjustment is demonstrated

24. `src/evaluation/__init__.py`
25. `src/evaluation/aggregate.py`
26. `src/evaluation/artifact.py`
27. `src/evaluation/metrics.py`
28. `src/evaluation/observation.py`
29. `src/evaluation/pipeline.py`
30. `src/evaluation/reliability.py`
31. `src/evaluation/schema.py`
32. `src/valuation/__init__.py`
33. `src/valuation/engine.py`
34. `src/valuation/schema.py`
35. `src/valuation/service.py`
36. `src/decision/__init__.py`
37. `src/decision/engine.py`
38. `src/decision/schema.py`
39. `src/decision/service.py`

### E. Tests

40. `src/tests/test_stage5_forecast.py`
41. `src/tests/test_stage1_database_architecture.py`
42. `src/tests/test_stage1_database_integrity.py`
43. `src/tests/test_stage6_artifact_boundary.py`
44. `src/tests/test_stage6_artifact_identity.py`
45. `src/tests/test_stage6_evaluation.py`
46. `src/tests/test_stage6_evaluation_foundation.py`
47. `src/tests/test_stage6_evaluation_metrics.py`
48. `src/tests/test_stage6_p25_adversarial.py`
49. `src/tests/test_stage6_p25_selection.py`
50. `src/tests/test_stage6_p38_closure.py`
51. `src/tests/test_stage6_p39_cutoff.py`
52. `src/tests/test_stage6_p40_duplicates.py`
53. `src/tests/test_stage6_p41_cutoff_identity.py`
54. `src/tests/test_stage6_production_pipeline.py`
55. `src/tests/test_stage6_reliability_governance.py`
56. `src/tests/test_stage6_scenario_isolation.py`
57. `src/tests/test_stage789_service_interface.py`
58. `src/tests/test_stage7_valuation.py`
59. `src/tests/test_stage9_decision.py`

Do not inspect files outside this list, except for the narrowly permitted read-only dependency inspection described in Section 7.

If a reference, caller, migration dependency, or test dependency points to an unlisted file, do not silently expand the scope.

First report its exact path and why it is required. Obtain authorization before inspecting or modifying it.

## 4. Task execution order

The task IDs must remain unchanged in all reports. Execute the work in this order:

### Task 057 · S7-T029 — Runtime consumer and dependency audit

Perform this audit before changing the implementation.

Establish, with exact file/function evidence:

1. Every caller of the Stage 5 production service.
2. Every use of `generate_and_persist_forecast`.
3. Every use of `ForecastRecordRepository`.
4. Every use of `ForecastVersionStore`.
5. Every use of `ForecastRecord`, `CompanyForecastResult`, `records()`, and `to_record()`.
6. Every reference to `ForecastVersion`, `ForecastInputRefModel`, `forecast_versions`, and `forecast_input_refs`.
7. How Stage 6 receives Forecast outputs and which runtime fields it actually consumes.
8. How Stage 7 receives `CompanyForecastResult` and which fields it consumes.
9. Whether any production caller depends on a stored Forecast row or repository read.
10. Which references are production code, test-only fixtures, historical migration support, or documentation-only.

**Required evidence:**

- Exact file paths and function/class names.
- Relevant call chain and data flow.
- Exact runtime fields required by Stage 6 and Stage 7.
- Explicit identification of any unproven production integration.

Do not create a new orchestrator, application entrypoint, fake production caller, or synthetic E2E path.

If no production caller exists, report that fact clearly. Do not claim that a production end-to-end path has been established.

### Task 054 · S7-T026 — Remove Forecast persistence write path

After Task 057's initial audit:

1. Remove the production write path that calls `ForecastRecordRepository.save()` or any equivalent Forecast-output write.
2. Remove the `persist=True` default and the persistence option from the Stage 5 service API. The API must not offer an accidental persistence switch.
3. Replace the misleading `generate_and_persist_forecast` service name with a name that accurately describes runtime Forecast generation, such as `generate_forecast`, provided the audit confirms the change is safe.
4. Update all verified callers and exports within the supplied scope.
5. Remove the active repository dependency from the Stage 5 runtime service.
6. Remove the in-memory `ForecastVersionStore` and its history/revision-trend behavior. R-05 prohibits replacing database history with another history store or cache.
7. Preserve runtime Forecast results and the runtime provenance needed by actual downstream consumers.
8. Preserve Stage 5's ability to read raw inputs from the database. A read-only database Session may still be required to load source data; the prohibition concerns persistence of analytical outputs.
9. Do not modify Forecast formulas, model parameters, scenario logic, or financial calculations.

**Critical runtime boundary:**

`ForecastRecord` is currently consumed by Stage 6 as an in-memory input. Do not remove or redesign that contract merely because its historical implementation was coupled to persistence.

Retain only the runtime data and identity fields that downstream consumers demonstrably require. Remove obsolete persisted-version semantics where they are not part of an approved runtime contract.

Do not invent a replacement version number, database ID, history, cache, or persistent identity.

If a downstream consumer genuinely requires a field whose meaning becomes ambiguous after removing persistence, stop and report the exact conflict rather than silently changing its semantics.

### Task 055 · S7-T027 — Remove Forecast persistence schema safely

The currently identified persistence structures are:

- `ForecastVersion` / `forecast_versions`
- `ForecastInputRefModel` / `forecast_input_refs`

The second table is an output-dependent provenance bridge, not an independent raw-input table.

Requirements:

1. Remove both tables from the final active application database schema.
2. Remove their active ORM/repository usage.
3. Preserve the raw source-input and Stage 1 provenance tables.
4. Preserve all unrelated schema, constraints, indexes, and data.
5. Add a new forward-only migration, expected to be migration **8**, that removes the two obsolete tables.
6. Drop `forecast_input_refs` before `forecast_versions` because of the foreign-key dependency.
7. Make the migration safe when either table is already absent.
8. Verify the behavior for:
   - A fresh database.
   - An existing database whose recorded migration version is 7.
   - An existing database with the legacy tables and rows present.
   - Repeated migration execution.
9. Preserve migration history: do not rewrite, delete, renumber, or change the semantics of migrations 1–7.
10. Do not introduce a downgrade that recreates analytical-output persistence.
11. Do not copy Forecast outputs into another database table, cache, archive, or replacement history store.

**Important migration constraint:**

Migration 7 currently creates the Forecast persistence tables using the registered ORM metadata. The historical migration must remain executable for fresh installations and databases upgrading from earlier versions.

Design the model-registration and migration-8 arrangement so that:

- Migration 7 remains executable and unchanged in historical meaning.
- Migration 8 removes the obsolete tables.
- Normal application initialization does not recreate those tables.
- The final active schema does not contain either table.

Do not simply delete the ORM model definitions if doing so makes historical migration 7 fail. If the historical migration and active-schema requirements cannot both be satisfied within the supplied files, stop and report the exact conflict before making an unsafe change.

**Data preservation rule:**

The only tables authorized for deletion are `forecast_input_refs` and `forecast_versions`. Their contents are analytical Forecast outputs and output-dependent provenance, which the owner has explicitly prohibited from being stored.

Do not delete or rewrite raw facts, normalized facts, reports, report versions, periods, corporate actions, share-count history, or any other input-side records.

### Task 056 · S7-T028 — Redesign regression tests

Replace tests that expect Forecast persistence with tests that prove the new architecture.

Do not weaken or simply delete existing tests.

Required coverage:

**A. Runtime Forecast correctness**

- Stage 5 returns the expected runtime `CompanyForecastResult`.
- Bear, Base, and Bull outputs remain available.
- Existing financial calculations and scenario invariants remain unchanged.
- Missing values remain missing; no missing value is converted to zero.
- Runtime model version, cutoff, timestamp, and required metadata remain available.

**B. No persistence**

- Running the Stage 5 generation service performs no database writes.
- No Forecast output or scenario row is inserted or updated.
- No output-dependent provenance row is inserted.
- The service does not instantiate or call a Forecast repository.
- No in-memory history/version store is used as a replacement.

**C. Final schema**

- After the migration runner completes, neither `forecast_versions` nor `forecast_input_refs` exists.
- Migration version is 8.
- Migration history 1–7 remains intact.
- Migration execution is idempotent.

**D. Raw input preservation**

- Raw and normalized source facts remain present and readable after Forecast generation.
- Report and ReportVersion data remain intact.
- ShareCountHistory and CorporateAction inputs remain intact.
- The migration removes only the two obsolete output tables.
- Tests must verify actual rows or stable identifiers, not merely assert that unrelated table names exist.

**E. Runtime provenance and PIT**

- Existing input-side PIT filtering remains effective.
- Runtime Forecast provenance remains available to downstream consumers where required.
- Removing the output-dependent database bridge must not silently remove the runtime input references.
- Do not weaken PIT, cutoff, identity, or provenance tests.

**F. Stage 6 and Stage 7 integration contracts**

- Stage 6 must continue to accept valid runtime Forecast records.
- Stage 6 must not read Forecast records from a database repository.
- Stage 7 must continue to receive and consume `CompanyForecastResult` through its existing runtime contract.
- Do not claim a real production E2E path where only test-created objects exist.

Update only the tests necessary for these requirements. Preserve the existing multi-layer test doctrine and all unrelated Stage 6/7 financial and evaluation assertions.

### Task 057 · S7-T029 — Final runtime-boundary audit

After implementation, repeat the dependency audit.

Confirm:

1. No production Stage 5 path writes Forecast outputs.
2. No production Stage 5 path imports or invokes `ForecastRecordRepository`.
3. No active runtime path depends on `forecast_versions` or `forecast_input_refs`.
4. No in-memory version/history store replaces the removed database persistence.
5. Stage 5 still reads source inputs correctly.
6. Stage 5 still returns runtime outputs.
7. Stage 6 still receives runtime Forecast records and required provenance.
8. Stage 7 still receives runtime `CompanyForecastResult`.
9. Test-only references are clearly separated from production references.
10. No new production caller or E2E claim has been fabricated.

Provide exact source evidence for every conclusion.

## 5. Files permitted to change

Only these files may be changed:

- `src/forecast/__init__.py`
- `src/forecast/service.py`
- `src/forecast/schema.py`
- `src/forecast/repo.py` — may be removed if the complete supplied-scope audit proves it has no remaining valid consumer.
- `src/models/forecast.py` — only if required to isolate legacy migration support from the active schema; preserve the ability to execute migration 7.
- `src/migrations/runner.py`
- `src/scripts/init_db.py` — only if necessary to prevent obsolete tables from being recreated.
- `src/tests/test_stage5_forecast.py`
- `src/tests/test_stage1_database_integrity.py`
- `src/tests/test_stage1_database_architecture.py`
- The supplied `src/tests/test_stage6_*.py` files, only where a directly affected runtime Forecast contract requires an update.

All other supplied files are READ-ONLY.

In particular, do not change:

- `src/forecast/engine.py`
- `src/forecast/builder.py`
- `src/forecast/drivers.py`
- `src/forecast/queries.py`
- Stage 6 calculation formulas or evaluation rules.
- Stage 7 valuation formulas or decision rules.
- Raw input models or their persistence contracts.
- Stage 5 financial formulas or model parameters.

Do not create additional files. If a new migration module or another file is genuinely necessary, stop and report its exact proposed path and reason before creating it.

## 6. Mandatory financial and data-integrity safeguards

- No financial formula changes.
- No changes to EPS, share-count, revenue, margin, profit, ROE, or scenario calculations.
- No weakening of missing-data behavior.
- No weakening of PIT or publication-availability checks.
- No mixing of companies, financial periods, scenarios, cutoffs, or model versions.
- No deletion of raw or normalized source data.
- No silent compatibility fallback to the old repository.
- No fake production caller or synthetic orchestration.
- No replacement persistence, cache, or history store.
- No test deletion without a meaningful replacement.

## 7. Execution restrictions and file inspection permissions

### 7.1. General principle

This task requires source-level inspection of the explicitly listed project files.

**Reading files is explicitly permitted and is NOT considered code execution, project modification, or a prohibited shell operation.**

The previous restriction against shell commands must NOT be interpreted as a prohibition on read-only file inspection.

The agent is explicitly authorized to use the minimum necessary read-only commands to inspect the supplied project.

### 7.2. Permitted read-only operations

The following operations are authorized:

- Reading file contents using `Get-Content`, `type`, `cat`, `sed`, or equivalent read-only commands.
- Listing explicitly relevant directories and filenames.
- Searching file contents using read-only commands such as `Select-String`, `grep`, or equivalent.
- Reading source code, tests, migration definitions, schemas, configuration, and documentation.
- Inspecting imports, function definitions, class definitions, references, and call sites.
- Reading directly referenced dependencies when necessary to establish a verified execution path or migration dependency, subject to the scope restrictions below.

The agent may use PowerShell, CMD, or another available local file-reading interface.

Use the simplest available method. Do not execute a script merely to read a file.

### 7.3. Strictly prohibited operations

Unless explicitly authorized by the owner, the agent MUST NOT:

- Execute application code.
- Run Python scripts or application entry points.
- Run pytest or any other tests.
- Execute database migrations.
- Create, modify, or delete database records.
- Install or update dependencies.
- Run formatters, auto-fix tools, or code generators.
- Execute commands that modify project files outside the explicitly authorized implementation scope.
- Execute Git commands that modify repository state.
- Commit, push, pull, merge, or modify branches.
- Access or modify GitHub or any remote repository.
- Execute shell commands that run application logic or modify system/project state.

### 7.4. Scope of file inspection

Inspect every required file in Section 3 before making implementation decisions.

If a listed file references another file that is essential to verify:

- The Forecast production call chain,
- The Stage 6 or Stage 7 runtime contract,
- The migration dependency,
- The active ORM registration,
- The database initialization path,

the agent must first identify the exact unlisted file and explain why it is necessary.

Do not silently expand the inspection scope.

Do not perform repository-wide exploration.

### 7.5. Implementation authorization

Code changes are authorized only within the explicitly permitted file list in Section 5.

Reading a file does not authorize modifying it.

The agent must not modify any file outside Section 5.

If a necessary change requires an unlisted file, stop before making that change and report:

1. Exact file path.
2. Why the change is necessary.
3. Which task depends on it.
4. The proposed minimal modification.

### 7.6. Failure handling

If a required file cannot be accessed:

1. Identify its exact path.
2. Explain which verification depends on it.
3. Continue all independent inspections that remain possible.
4. Report the unresolved dependency.

Do NOT stop the entire task merely because one file is inaccessible.

If a required dependency cannot be inspected safely, do not guess its behavior.

### 7.7. Test execution boundary

The user will run all tests locally and provide the actual output.

The agent must:

- Author and update the required tests.
- Review the test code statically.
- Provide exact recommended test commands.
- Identify expected test coverage.

The agent MUST NOT execute tests or claim that tests passed.

### 7.8. Reporting boundary

- Work only in the supplied local folder `analyzer`.
- Do not access or edit GitHub or any remote repository.
- Do not modify the Master Packet or any governance document.
- Do not write the report into `reply.md`, `temp_report2.md`, or any other file.
- Do not create additional files.
- Report directly to the user.

The agent may use read-only shell commands for file inspection, but must not execute tests, application code, migrations, database commands, Git operations, or other prohibited commands.

## 8. Required completion report

Report directly to the user. Do not create or modify a report file.

Report each task separately, preserving its exact number and ID:

### 057 · S7-T029

- Initial audit findings.
- Final audit findings.
- Every verified production caller and test-only caller.
- Stage 6 and Stage 7 runtime data flow.
- Whether any real production caller exists.
- Evidence for the absence of persistence dependencies.

### 054 · S7-T026

- Exact service API before and after.
- Exact write path removed.
- Runtime contract preserved.
- All changed files.

### 055 · S7-T027

- Migration number and name.
- Confirmation migrations 1–7 were not rewritten.
- Exact drop order.
- Fresh database and existing-v7 migration behavior covered by tests.
- Confirmation that only the two authorized tables are removed.
- Confirmation that raw input tables are preserved.

### 056 · S7-T028

- Tests removed or rewritten, with reasons.
- New tests added and the invariant each one proves.
- Runtime provenance/PIT tests preserved.
- Exact commands recommended for the user.

For each task, report one of:

`DONE`, `PARTIAL`, `NOT DONE`, `BLOCKED`

Do not mark implementation/test tasks DONE merely because code was edited. Since you are prohibited from running tests, explicitly state that test execution remains pending user verification.

Also provide:

- Exact files inspected.
- Exact files changed or deleted.
- Any unmodified but potentially relevant files.
- Any unresolved dependencies or limitations.
- Confirmation that no tests, application code, migrations, database operations, or Git operations were executed.
- Confirmation that only authorized read-only file inspection commands were used.

Do not claim success without source-level evidence.