# Prompt 1-C-B — Comprehensive Evidence Closure for Stage 7
## Task IDs: S7-T001, S7-T002
## Work Type: AUDIT ONLY + REPORT/DOCUMENTATION UPDATES

You are auditing the current `lovelyroz/analyzer` repository snapshot for a financial-data application.

Your task is to close the remaining evidence gaps in:
- **S7-T001 — Verify the real production execution path**
- **S7-T002 — Verify Stage 9 persistence**

This is a source-evidence audit, not an implementation task.

## 1. Mandatory workflow and authority

Read and follow:
- `WORKFLOW_RULES.md`
- `tasksToDo.md`
- `stepsForStage7.md`
- `reply.md`
- `temp_report2.md`
- `07_Stage7_Valuation.md`
- `09_Stage9_Decision_Dashboard.md`
- `10_Production_Codal_Extraction_and_Data_Load.md`
- `11_Database_Architecture_Stage1.md`
- `12_Database_Architecture_V1.1.md`
- `00_a_Master_Architecture.md`
- `PROJECT_HANDOFF_INSTRUCTIONS.md`

Treat `stepsForStage7.md` as the authoritative Stage 7 roadmap and `tasksToDo.md` as the task register. Earlier reports are historical evidence, not unquestionable facts. Where an earlier conclusion conflicts with current source code, document the conflict and explain which evidence resolves it.

Stage 7 remains OPEN unless its actual exit criteria are later verified. This prompt does not authorize closing Stage 7.

## 2. Strict file-access boundary

You may examine only the files explicitly supplied for this prompt. Do not assume you can access the rest of the repository, hidden files, a local checkout, Git history, or remote search results.

The complete production Python file set to supply is listed below. These paths were enumerated from the repository's current directory structure. Supply every listed file, including files that appear unrelated at first glance, because a caller or persistence path may be located outside the obvious Stage 7/9 modules.

### Core, decision, evaluation, forecast

- `src/core/database.py`
- `src/core/jalali.py`
- `src/core/point_in_time.py`
- `src/decision/__init__.py`
- `src/decision/engine.py`
- `src/decision/rules.py`
- `src/decision/schema.py`
- `src/decision/service.py`
- `src/evaluation/__init__.py`
- `src/evaluation/aggregate.py`
- `src/evaluation/artifact.py`
- `src/evaluation/metrics.py`
- `src/evaluation/observation.py`
- `src/evaluation/pipeline.py`
- `src/evaluation/reliability.py`
- `src/evaluation/schema.py`
- `src/forecast/__init__.py`
- `src/forecast/adapter.py`
- `src/forecast/builder.py`
- `src/forecast/drivers.py`
- `src/forecast/engine.py`
- `src/forecast/queries.py`
- `src/forecast/repo.py`
- `src/forecast/schema.py`
- `src/forecast/service.py`

### Ingestion

- `src/ingestion/__init__.py`
- `src/ingestion/service.py`
- `src/ingestion/codal/__init__.py`
- `src/ingestion/codal/acquisition.py`
- `src/ingestion/codal/adapter.py`
- `src/ingestion/codal/ingestion.py`
- `src/ingestion/codal/numbers.py`
- `src/ingestion/codal/parser.py`
- `src/ingestion/codal/pdf_extract.py`
- `src/ingestion/codal/pipeline.py`
- `src/ingestion/codal/validator.py`
- `src/ingestion/common/__init__.py`
- `src/ingestion/common/idempotency.py`
- `src/ingestion/common/identity.py`
- `src/ingestion/common/parsing.py`
- `src/ingestion/common/run_tracker.py`
- `src/ingestion/common/validation.py`
- `src/ingestion/fx/__init__.py`
- `src/ingestion/fx/adapter.py`
- `src/ingestion/fx/ingestion.py`
- `src/ingestion/fx/validator.py`
- `src/ingestion/market/__init__.py`
- `src/ingestion/market/adapter.py`
- `src/ingestion/market/ingestion.py`
- `src/ingestion/market/queries.py`
- `src/ingestion/market/validator.py`

### KPI, market, migrations, models

- `src/kpi/__init__.py`
- `src/kpi/conditional.py`
- `src/kpi/engine.py`
- `src/kpi/industry.py`
- `src/kpi/period_utils.py`
- `src/kpi/schema.py`
- `src/kpi/universal.py`
- `src/market/__init__.py`
- `src/market/engine.py`
- `src/market/indicators.py`
- `src/market/parameters.py`
- `src/market/schema.py`
- `src/market/service.py`
- `src/migrations/__init__.py`
- `src/migrations/runner.py`
- `src/models/audit.py`
- `src/models/entity.py`
- `src/models/forecast.py`
- `src/models/fx.py`
- `src/models/market.py`
- `src/models/normalized.py`
- `src/models/normalized_provenance.py`
- `src/models/period.py`
- `src/models/report.py`
- `src/models/share_action.py`

### Scoring, scripts, trend, valuation

- `src/scoring/__init__.py`
- `src/scoring/engine.py`
- `src/scoring/functions.py`
- `src/scoring/schema.py`
- `src/scoring/weights.py`
- `src/scripts/init_db.py`
- `src/scripts/migrate_db.py`
- `src/scripts/seed_data.py`
- `src/trend/__init__.py`
- `src/trend/engine.py`
- `src/trend/schema.py`
- `src/trend/utils.py`
- `src/valuation/__init__.py`
- `src/valuation/engine.py`
- `src/valuation/models.py`
- `src/valuation/parameters.py`
- `src/valuation/schema.py`
- `src/valuation/service.py`

### Root-level/runtime and workflow references

- `debug_alerts.py`
- `requirements.txt`
- `.github/workflows/tests.yml`

### Required tests and specifications

- `src/tests/test_stage789_service_interface.py`
- `src/tests/test_stage9_decision.py`
- `src/tests/test_stage7_valuation.py`
- `src/tests/test_stage5_forecast.py`
- `src/tests/test_stage8_market_service.py`
- `src/tests/test_market_history_query.py`
- `src/tests/test_stage3_scoring.py`
- `src/tests/test_stage1_database_architecture.py`
- `src/tests/test_stage1_database_integrity.py`
- `src/tests/test_codal_extraction.py`
- `src/tests/test_stage8_market.py`
- `src/tests/test_stage8_market_parameters.py`
- `05_Stage5_Forecast_Engine.md`
- `08_Stage8_Market_Engine.md`
- `99_Architecture_Change_Log.md`

If any listed file is not supplied, do not pretend to have inspected it. List the exact missing path, explain which acceptance criterion it affects, and classify the relevant conclusion as UNVERIFIED. Do not replace a missing file with assumptions or a filename guess. Do not infer repository-wide absence merely because a symbol is absent from a subset of supplied files.

## 3. S7-T001 — Production execution path

Determine, from the supplied source code, whether the project contains a real production execution path connecting the relevant stages.

At minimum, trace these symbols and their actual callers:

- Stage 3: scoring production functions and their input requirements.
- Stage 5: `generate_and_persist_forecast` and any forecast retrieval/persistence functions.
- Stage 7: `calculate_valuation_as_of_jalali`.
- Stage 8: `analyze_market_as_of_jalali`.
- Stage 9: `calculate_decision_as_of_jalali` and `DecisionEngine.make_decision`.
- Database/session ownership, including `SessionLocal`, session creation, transaction boundaries, commit/rollback, and closure.
- Any executable entrypoint, CLI, API route, worker, scheduled task, orchestrator, pipeline runner, or application startup path present in the supplied files.

Search for direct imports and calls, indirect call chains, `if __name__ == "__main__"` blocks, and framework registration/dispatch where relevant. Inspect the complete supplied source set, not just the obvious service files.

Explicitly distinguish:

1. A function or service definition.
2. A service-to-service call.
3. A test-only caller.
4. A database utility or ingestion script that does not run the valuation/decision pipeline.
5. A real production caller.
6. A complete end-to-end path that supplies actual upstream outputs and carries the result through Stage 9.

For each claimed connection, provide:
- Exact file path and function/class/method name.
- The relevant call site or a short exact code excerpt.
- The inputs passed and where they originate.
- The returned output and its next consumer.
- Whether the path is production, test-only, utility-only, or unverified.
- Any missing link that prevents the next stage from being reached.

Do not treat the existence of `SessionLocal`, a service, a model, a passing unit test, or a mocked call as proof of a production pipeline.

Do not design or propose an implementation of a new orchestrator in this prompt. Report the smallest missing link or owner decision, if any.

### S7-T001 acceptance criteria

Accept the audit conclusion only if:
- Every supplied production Python file in the declared scope has been considered for callers/entrypoints.
- The actual caller chain for the named services is traced from source, not inferred from function names.
- Test callers are separated from production callers.
- Database session and transaction ownership are evidenced or explicitly unverified.
- Every claimed absence is bounded to the exact supplied source set.
- The report states whether a real Stage 3/5/7/8/9 end-to-end production path is verified, partially verified, or not found in the complete supplied source set.
- Any remaining uncertainty identifies the exact missing file or non-source evidence and why it is necessary.

If the complete supplied production source set contains no production caller, you may conclude that no such caller was found in that supplied source set. Do not claim that the application could never be invoked externally unless deployment/configuration evidence proves that broader claim.

## 4. S7-T002 — Stage 9 persistence

Determine whether `FinalDecisionResult` or the containing `ValuationDecisionResult` is persisted anywhere in the supplied application source.

Do not restrict this audit to whether a dedicated SQLAlchemy model exists. Check for all plausible persistence mechanisms evidenced by the supplied files, including:

- SQLAlchemy ORM models and table definitions.
- Repositories and database write paths.
- `session.add`, `flush`, `commit`, transaction handling, and repository calls.
- Serialization or output writers that store decision results to files or another configured destination.
- Migrations and model-registration/bootstrap logic.
- Any production caller that receives the Stage 9 result and then stores, publishes, or forwards it to a persistent destination.
- Existing persistence patterns for other stage outputs, so the report can distinguish a reusable pattern from actual Stage 9 persistence.

Trace `FinalDecisionResult` from its definition, through `DecisionEngine.make_decision`, through `calculate_decision_as_of_jalali`, and into all callers found in the supplied source set.

Explicitly distinguish these outcomes:

- **PRESENT:** a concrete persistence path for the decision result is implemented and traceable.
- **PARTIAL:** only some data, metadata, or a transformed subset is persisted, or a persistence component exists without a proven end-to-end write path.
- **NOT FOUND IN SUPPLIED FILES:** no persistence path is evidenced within the complete supplied scope.
- **UNVERIFIED:** one or more required files or necessary evidence are missing.

A model or schema alone is not proof that data is saved. A `Session` parameter alone is not proof of persistence. The absence of `session.add()` inside the decision service alone is not proof that no caller persists the result.

Do not create a new ORM model, migration, repository, output writer, or persistence contract. Do not decide whether persistence is a product requirement; report the current implementation and the architectural decision that remains for the owner.

### S7-T002 acceptance criteria

Accept the audit conclusion only if:
- `FinalDecisionResult` and `ValuationDecisionResult` are traced to every caller found in the supplied production source.
- All supplied ORM models, model-registration paths, migrations, and relevant repositories have been checked.
- The report distinguishes database persistence from other forms of persistence.
- Any existing persistence claim is supported by the actual write call and the identity/fields being stored.
- Any absence claim is bounded to the exact supplied source set.
- The conclusion is one of PRESENT, PARTIAL, NOT FOUND IN SUPPLIED FILES, or UNVERIFIED, with supporting evidence and remaining uncertainty.

## 5. Cross-check and evidence discipline

Perform a second pass after the initial audit:
- Recheck every call-chain and persistence claim against the actual referenced file.
- Check whether any supplied file contradicts the first-pass conclusion.
- Check whether earlier statements in `reply.md` or `temp_report2.md` overstate what was inspected.
- Correct false or overly broad claims rather than copying them forward.
- Never infer that a test passed or failed from its name or from a historical report. Do not run tests.
- Never invent a file, function, caller, schema, data source, database table, or deployment path.
- Use precise terms: “not found in the supplied source set” is not interchangeable with “does not exist anywhere.”
- Keep financial correctness, auditability, determinism, and point-in-time correctness intact.

For every material conclusion, include:
1. The conclusion.
2. The exact evidence supporting it.
3. Why that evidence satisfies the criterion.
4. The scope limitation, if any.
5. What conclusion remains impermissible if the evidence is insufficient.

## 6. Permitted changes and prohibited operations

Permitted modifications:
- Append a clearly titled final section to `reply.md`, for example:
  `Prompt 1-C-B — Final Evidence Closure Report (S7-T001, S7-T002)`.
- Update only the S7-T001 and S7-T002 entries in `tasksToDo.md`, but only if their audit acceptance criteria are demonstrably satisfied. A verified implementation gap does not automatically mean the audit task is incomplete: record the audit task status according to the task register's definitions, and separately record the actual architecture/implementation gap. If evidence remains insufficient, leave the affected task OPEN and state exactly what is missing.

Do not modify `stepsForStage7.md` in this prompt. Do not change source code, tests, schemas, migrations, configurations, or financial formulas. Do not create files other than the permitted report/status updates.

Absolutely prohibited:
- Running tests, application code, scripts, migrations, database commands, or benchmarks.
- Running Git commands or changing branches, commits, remotes, or repository state.
- Any GitHub/Git CLI/API operation, push, pull, commit, or remote edit.
- Claiming that tests were run.
- Marking Stage 7 complete.

## 7. Required final report format

The appended section in `reply.md` must contain:

1. **Prompt ID / Task IDs / Work type**
2. **Exact files supplied and actually inspected**
3. **S7-T001 verdict** and evidence table:
   - connection
   - caller/call site
   - upstream input
   - downstream consumer
   - caller classification
   - evidence
   - limitation
4. **S7-T002 verdict** and evidence table:
   - output object
   - persistence mechanism checked
   - exact write site if present
   - stored fields/identity if present
   - conclusion
   - limitation
5. **Second-pass verification:** what claims were rechecked and whether any were corrected.
6. **Earlier report corrections:** quote or identify each materially overbroad claim and its corrected form.
7. **Acceptance criteria:** PASS/NOT PASS per criterion, with evidence.
8. **Task status changes:** previous status, new status, and reason for S7-T001/T002. Do not change unrelated task statuses.
9. **Remaining blockers and exact owner decisions/files required.**
10. **Files modified:** list only the files actually changed.
11. **Tests and commands:** explicitly state “No tests or application/database commands were run by the agent.”

Do not merely provide recommendations. Finish the audit to the maximum extent supported by the supplied evidence and produce the permitted report/status updates in the same execution. If evidence is still missing, make the exact gap explicit and leave the conclusion unverified rather than creating another speculative audit loop.