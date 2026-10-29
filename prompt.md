# Prompt 1-D — Stage 7 Evidence Audit and Documentation Alignment

**Task IDs:** S7-T003, S7-T004, S7-T005, S7-T006  
**Work type:** AUDIT + DOCS ONLY  
**Code changes:** NOT AUTHORIZED  
**Test changes:** NOT AUTHORIZED  
**Test execution:** PROHIBITED

## 1. Mission

Continue Stage 7 remediation for the financial-data application in the local project folder `analyzer`.

Read and follow `WORKFLOW_RULES.md`, `tasksToDo.md`, and `stepsForStage7.md` before beginning. Use `tasksToDo.md` as the task-status register and `stepsForStage7.md` as the authoritative Stage 7 roadmap.

Complete the three remaining evidence audits:

- **S7-T003:** D9 and actual consumption of versioned valuation parameters.
- **S7-T004:** Point-in-Time (PIT), provenance, and input contracts.
- **S7-T005:** Alert and decision contracts D1–D8.

Then perform **S7-T006**, aligning `reply.md` and `stepsForStage7.md` only to conclusions supported by the completed audits.

This is an evidence-gathering and documentation task. Do not implement fixes or redesign the valuation engine.

## 2. Exact required files

The following files must be provided to you. Inspect only these files and any additional files explicitly listed below. Do not assume that you can inspect the rest of the repository.

### Workflow and prior evidence

- `WORKFLOW_RULES.md`
- `tasksToDo.md`
- `stepsForStage7.md`
- `reply.md`
- `temp_report2.md`
- `PROJECT_HANDOFF_INSTRUCTIONS.md`

### Specifications

- `05_Stage5_Forecast_Engine.md`
- `07_Stage7_Valuation.md`
- `08_Stage8_Market_Engine.md`
- `09_Stage9_Decision_Dashboard.md`
- `00_a_Master_Architecture.md`

### Stage 7 valuation package

- `src/valuation/__init__.py`
- `src/valuation/engine.py`
- `src/valuation/models.py`
- `src/valuation/parameters.py`
- `src/valuation/schema.py`
- `src/valuation/service.py`

### Forecast, scoring, market, decision, and PIT interfaces

- `src/forecast/schema.py`
- `src/forecast/service.py`
- `src/forecast/repo.py`
- `src/scoring/engine.py`
- `src/market/engine.py`
- `src/market/schema.py`
- `src/market/parameters.py`
- `src/market/service.py`
- `src/ingestion/market/queries.py`
- `src/core/point_in_time.py`
- `src/core/jalali.py`
- `src/core/database.py`
- `src/decision/engine.py`
- `src/decision/rules.py`
- `src/decision/schema.py`
- `src/decision/service.py`

### Directly relevant tests

- `src/tests/test_stage7_valuation.py`
- `src/tests/test_stage9_decision.py`
- `src/tests/test_stage789_service_interface.py`
- `src/tests/test_stage5_forecast.py`
- `src/tests/test_stage8_market.py`
- `src/tests/test_stage8_market_service.py`
- `src/tests/test_stage8_market_parameters.py`
- `src/tests/test_market_history_query.py`

If a listed file is unavailable, report its exact path and the specific acceptance criterion that cannot be verified. Do not silently omit it. If another file is necessary, name that exact path and explain why it is required; do not claim conclusions that depend on an unprovided file.

## 3. Mandatory restrictions

1. Do not run tests, application code, scripts, database commands, Git commands, or shell commands.
2. Do not use GitHub, GitHub CLI, remote APIs, commits, branches, pushes, or pulls.
3. Do not modify production code or test code.
4. Only the following documentation files may be changed:
   - `reply.md`
   - `stepsForStage7.md`
   - `tasksToDo.md`
5. Do not rewrite `src/valuation/engine.py`; it is reserved for S7-T011, the final technical task.
6. Do not invent financial formulas, alert thresholds, industry mappings, data sources, parameter values, effective dates, historical observations, or missing callers.
7. Do not treat a report's assertion as proof when the current source or tests can verify the claim.
8. Do not treat a report date, cutoff date, or model-version label alone as proof of PIT correctness.
9. Do not recompute Stage 5 EPS in Stage 7.
10. Preserve the existing Jalali date conventions and established financial contracts.
11. A missing item in the supplied file set is not proof that it is absent from the entire repository or from external deployment code.

## 4. S7-T003 — D9 and versioned parameter consumption

Inspect the current implementation and tests to determine:

- How valuation parameters are represented and versioned.
- How parameter selection is performed when an as-of Jalali date is supplied.
- What happens when no parameter version can be validly selected.
- Whether the selected parameter values actually influence the valuation calculation, or are merely attached to metadata.
- Whether metadata, model-version identifiers, and effective-date fields correspond to the parameters actually consumed by the calculation.
- Whether the tests exercise the real selection and consumption path, including the absence of a valid historical version.

### Required evidence

For each material conclusion, cite exact file paths, function/class names, relevant line ranges when available, and the associated test name or assertion.

Distinguish:

- Proven by current implementation.
- Proven by an existing test.
- Not demonstrated by the supplied code or tests.
- Requires an explicit owner decision or an approved financial contract.

Do not infer that Genesis/default parameters are valid for historical dates unless an explicit, approved contract supports that behavior. Do not invent an effective date or historical version.

**Acceptance criterion:** The parameter-selection path, actual parameter consumption, invalid/missing-version behavior, and test coverage are reported with evidence. Do not mark D9 resolved merely because a version identifier exists.

## 5. S7-T004 — PIT, provenance, and input contracts

Trace the available evidence for the following inputs and interfaces:

- Stage 5 forecast and its provenance/reference information.
- Valuation market price and its Jalali as-of selection.
- Historical benchmark inputs and their timestamps/provenance.
- Stage 8 market signals and their actual source path.
- The as-of date and its propagation across relevant service boundaries.
- Any other input consumed by valuation that materially affects PIT correctness.

For each input, distinguish the date of the underlying observation or report from evidence that the information was actually available by the requested analysis date.

Determine whether the available source and tests prove:

1. The identity of the data being consumed.
2. The observation/report date, where applicable.
3. The availability/publication time, where required for PIT.
4. The as-of filtering rule.
5. The provenance linking the input to its source.
6. The behavior when the required temporal evidence is absent.

Do not assume that an as-of query alone establishes full PIT correctness. Do not classify metadata references as proof that the corresponding data were actually used.

**Acceptance criterion:** Provide an input-by-input evidence matrix with the actual contract, evidence, unresolved temporal/provenance gaps, and the exact missing file or owner decision needed to close each gap. Where the code cannot establish PIT correctness, report that limitation explicitly rather than inventing a remedy.

## 6. S7-T005 — Alert and decision contracts D1–D8

Compare the current source and direct tests against the approved policies in `stepsForStage7.md` and `07_Stage7_Valuation.md`.

Assess each decision separately:

- **D1 — `ASSESSMENT_FLIP_RISK`:** no new alert without a valid criterion for changes in assumptions/status.
- **D2 — `HIGH_MULTIPLE_DEPENDENCE`:** the current criterion is not approved as valid; keep the alert disabled pending validation.
- **D3 — `HIGH_EPS_DEPENDENCE`:** no new alert without a valid criterion; preserve Stage 5 EPS.
- **D4 — `MARGIN_ASSUMPTION_RISK`:** outside V1 until a valid, dated input exists.
- **D5 — `HIGH_IMPACT_HIGH_UNCERTAINTY`:** preserve `review_priority`; do not create an additional alert without an independent valid criterion.
- **D6 — Industry-specific models:** preserve existing EPS and TARGET_PE drivers; do not invent industry formulas or mappings.
- **D7 — PIT:** evaluate actual temporal evidence for every relevant input; a cutoff alone is insufficient.
- **D8 — Alert contract:** verify actual names, structures, producers, consumers, and tests before concluding that an alert is operationally supported.

For each D1–D8, report:

- Approved policy.
- Current implementation and exact relevant symbols.
- Evidence from direct tests.
- Actual consumer evidence, if any.
- Whether the behavior is implemented, intentionally deferred, partially evidenced, or unresolved.
- Any genuine discrepancy and the evidence needed to accept that discrepancy as a defect.

Do not label an intentionally deferred capability as a bug that must be implemented. Do not change alert names or schemas. Do not infer that an alert is consumed merely because it appears in a result schema.

**Acceptance criterion:** Every D1–D8 has an evidence-backed status. Deferred functionality remains deferred unless an explicit approved policy says otherwise.

## 7. S7-T006 — Documentation alignment

Only after S7-T003, S7-T004, and S7-T005 have been audited, update the documentation as justified by the evidence.

### `reply.md`

Append a clearly titled report for Prompt 1-D. Include:

- Prompt ID and Task IDs.
- Work type.
- Exact files actually inspected.
- Evidence-backed findings for T003, T004, and T005.
- Acceptance criteria and PASS / NOT PASS / UNVERIFIED outcomes.
- Exact file paths, symbols, test names, and line ranges when available.
- Any missing files and the conclusions they prevent.
- Owner decisions and contracts still required.
- Files changed and reasons.
- Explicit statement that no tests, application code, database commands, or Git commands were run.

Do not erase historical reports. Correct an earlier statement only when current evidence justifies the correction; document the correction rather than silently rewriting history.

### `stepsForStage7.md`

Update only the roadmap statements and statuses directly supported by this audit. Preserve all established policies and the four-package order. Do not declare Stage 7 complete.

### `tasksToDo.md`

Update the statuses of S7-T003, S7-T004, S7-T005, and S7-T006 only when their acceptance criteria are actually satisfied.

- A completed audit may be marked DONE even when it identifies an unresolved architectural or policy blocker, provided the audit itself meets its acceptance criteria.
- If evidence is insufficient, leave the affected task OPEN and explain precisely what is missing.
- Do not mark S7-T007, S7-T008, S7-T009, S7-T010, S7-T011, or S7-T012 DONE as part of this prompt.
- Do not change unrelated task statuses.

## 8. Final response format

Return a concise summary and a detailed audit report in `reply.md`.

Your final response must state:

1. The outcome of each of S7-T003, S7-T004, S7-T005, and S7-T006.
2. Which documentation files changed.
3. Which conclusions remain unverified or blocked and the exact evidence/owner decision required.
4. Confirmation that no code/tests were changed and no tests or commands were executed.
5. The exact next recommended Task IDs based on the findings, without prematurely advancing to the final engine review.

**Stage 7 must remain OPEN unless all actual exit criteria in `stepsForStage7.md` are independently satisfied.**