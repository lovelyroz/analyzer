# P44 — Stabilize Stage 7 → Stage 9 Integration and Validate Jalali Market Dates

You are continuing Stage 7 remediation in the local working directory `analyzer` for the GitHub repository `analyzer`.

Read `stepsForStage7.md` first. It defines the agreed work sequence. Follow it strictly: **do not redesign or refactor `src/decision/engine.py` or `src/valuation/engine.py` in this prompt.** Engine review and any justified redesign belong at the end of Stage 7, after the outstanding integration, specification, and validation issues have been resolved.

## Operating rules

- Work locally only. Do not use GitHub, GitHub CLI/API, remotes, pushes, commits, or branch operations.
- Do not run pytest, CI, or other test suites. I will run tests and provide the actual output.
- Do not edit `reply.md`, `temp_report.md`, `temp_report2.md`, `ClaudeReports/`, `stepsForStage7.md`, or `stage_7_prompts.md`.
- Avoid repository-wide scans. Inspect only the files and narrowly related entry points needed for this task.
- Preserve financial formulas, thresholds, weights, scenario probabilities, Stage 5 EPS, output contracts, and existing behavior unless a demonstrated defect requires a narrowly scoped correction.
- Do not invent financial inputs, date conversions, calendar rules, or claims of Point-in-Time correctness.
- Do not delete, skip, weaken, or rewrite unrelated tests merely to obtain passing results.
- Make concrete, minimal code changes wherever the evidence supports a safe fix. Do not stop at a report if a supported implementation is possible.

## Confirmed P43 findings

1. `src/decision/service.py` introduces `calculate_decision_as_of_jalali(...)`, which calls `calculate_valuation_as_of_jalali(...)` and passes that exact valuation result to `DecisionEngine.make_decision(...)`.
2. `src/tests/test_stage9_decision.py` has a new test named `test_jalali_orchestration_passes_stage7_result_to_stage9`.
3. My actual local test run reported **13 passed, 1 failed** in `src/tests/test_stage9_decision.py`. The failure is:
   `AttributeError: 'ValuationDecisionResult' object has no attribute 'metadata'`
   at these assertions:
   `assert result.metadata["market_score_used"] is False`
   `assert result.metadata["position_sizing_used"] is False`
   `ValuationDecisionResult` contains `valuation` and `decision`; the Stage 9 metadata belongs to `result.decision.metadata`.
4. P43 did not establish that the new orchestration function is called by the application's real execution path.
5. `src/ingestion/market/queries.py` filters stored Jalali components using broad month/day ranges. `parse_jalali_components` also checks numeric ranges, not full calendar validity. An impossible stored date could therefore be selected.
6. Do not convert Jalali dates to Gregorian dates to bypass this issue. Existing project behavior intentionally preserves Jalali dates without fabricating Gregorian values.

## Task A — Correct and strengthen the P43 regression test

Inspect only:
- `src/decision/service.py`
- `src/decision/schema.py`
- `src/decision/engine.py` where needed to confirm the result contract
- `src/tests/test_stage9_decision.py`

Correct the failing assertions to inspect the actual Stage 9 result contract, without changing that contract merely to satisfy the test.

Ensure the test verifies all of the following:
- The orchestration service calls the Stage 7 valuation boundary.
- The exact returned `ValuationResult` object is passed to Stage 9.
- The final wrapper returns that valuation and the Stage 9 decision.
- `market_score_used` and `position_sizing_used` are checked through the actual Stage 9 metadata location.
- Existing company and forecast-period identity checks remain intact.

Add or adjust only narrowly relevant tests if needed. Do not run them.

## Task B — Correctly handle impossible stored Jalali dates

Inspect:
- `src/ingestion/market/queries.py`
- `src/ingestion/market/adapter.py`
- `src/ingestion/common/parsing.py`
- the existing dependency declarations and directly relevant date/calendar utilities, if any

Determine whether the project already has a reliable Jalali calendar validator available. If it does, use it consistently and narrowly to prevent invalid persisted dates from being selected.

Requirements:
- Validate the full calendar date, not just `1 <= month <= 12` and `1 <= day <= 31`.
- Apply the validation to stored observations before selecting a price.
- Preserve the existing numeric Jalali ordering, company isolation, adjusted-close/close fallback, duplicate-date failure behavior, and provenance.
- Do not add a new calendar implementation or Gregorian conversion.
- Do not add a dependency without a clear justification and compatibility evidence.
- Add focused tests for impossible stored Jalali dates and valid dates near calendar boundaries.

If the repository has no reliable validator and a safe solution cannot be established from the existing dependencies, do not invent one. Make any independently safe fixes, then state the precise blocker and the smallest justified next step.

## Task C — Establish the actual application call path

Inspect the orchestration service and only the relevant application entry points/callers needed to determine whether there is a real route from forecast generation/retrieval through Stage 7 and into Stage 9.

The known interfaces are:
- Stage 5 forecast generation/retrieval produces a forecast result.
- Stage 7 accepts the forecast plus an as-of Jalali date and a database session for market-price selection.
- Stage 9 requires matching fundamental and market evidence in addition to the Stage 7 valuation.

Determine whether a real caller already has these inputs and can safely call `calculate_decision_as_of_jalali(...)`.

If a real caller exists, connect it with the smallest safe change and add a focused integration test that exercises the actual call path rather than mocking away the orchestration itself.

If no suitable caller exists, do not fabricate Stage 3/Stage 8 results, invent data, or claim the production path is connected. Implement only a safe, useful integration step that existing interfaces support, and identify exactly what real caller/input contract is missing.

Do not create a new application entry point merely to make a test pass unless its place in the existing architecture is justified by concrete evidence.

## Validation expectations

Do not execute tests. Add or update focused tests covering, where supported:
- The corrected Stage 9 metadata assertions.
- The same Stage 7 result reaching Stage 9.
- Company/period mismatch rejection.
- Missing eligible market price failing closed.
- Impossible stored Jalali dates not being selected.
- Existing valid Jalali-date selection and provenance remaining intact.
- The real application call path, only if an actual caller can be connected.

Do not claim the tests pass. Report the exact test commands I should run locally.

## Required final response

Report:
1. Each file changed and the reason.
2. The exact P43 test defect corrected.
3. Whether impossible stored Jalali dates are now reliably rejected and which validator provides that guarantee.
4. Whether a real application caller now invokes the Stage 7 → Stage 9 orchestration. Show the exact call path or the specific missing interface.
5. Tests added/modified and the exact commands for me to run.
6. Explicitly confirm that you did not run tests or CI.
7. Remaining financial-correctness, Point-in-Time, historical-parameter-versioning, or output-contract blockers.

Do not update reports or freeze Stage 7. Stage 7 remains NOT FROZEN until the documented blockers are resolved or explicitly accepted through the project's decision process.