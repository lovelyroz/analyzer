# P47 — Complete the Real Application Integration Path (Follow-up to P46)

You are continuing Stage 7 remediation in the local working directory `analyzer` for the financial-data application.

## Objective

P46 did not establish the real application execution path from upstream data production through Stage 7 valuation into Stage 9 decision-making. The current test `test_jalali_orchestration_passes_stage7_result_to_stage9` monkeypatches the Stage 7 valuation service and therefore does not prove real application integration.

Complete this task rather than repeating the previous report.

## Mandatory boundaries

- Work only in the existing local repository.
- Do not use GitHub, GitHub CLI/API, remote operations, push, pull, commit, or branch changes.
- Do not run tests. The user will run them and provide the actual output.
- Do not edit `reply.md`, `temp_report.md`, `temp_report2.md`, `ClaudeReports/`, `stepsForStage7.md`, or `stage_7_prompts.md`.
- Do not perform a repository-wide scan. Trace only the relevant application entry point and the specific upstream/downstream modules needed.
- Do not redesign or centralize `engine.py`; its review is reserved for the end of Stage 7.
- Do not change financial formulas, EPS behavior, thresholds, alert policies, output contracts, or established Jalali market-price semantics.
- Do not fabricate Stage 3, Stage 5, or Stage 8 data or treat mock-only tests as proof of production integration.
- Do not claim that tests, CI, or runtime flows passed when you did not execute them.

## Task 1 — Establish the actual execution path

Trace the narrowest real application entry point that should lead to a Stage 9 decision.

Follow actual imports and calls to establish:

1. How the application obtains or produces the Stage 5 `CompanyForecastResult`.
2. How the real Stage 3 `FundamentalScoreResult` is produced or retrieved.
3. How the real Stage 8 `MarketSignalResult` is produced or retrieved.
4. Where the database session and requested Jalali as-of date originate.
5. Whether the application invokes `calculate_decision_as_of_jalali`.
6. Whether the resulting Stage 9 decision is returned, persisted, or consumed by the actual caller.

Use the existing implementation and contracts. Do not infer a caller merely because a service function exists.

## Task 2 — Implement the real connection when supported

If the actual application has the authoritative inputs and interfaces needed, connect the real entry point to the existing orchestration boundary.

Preserve:
- company and forecast-period identity checks;
- fail-closed behavior when required inputs or an eligible market price are missing;
- the selected market-price provenance;
- the exact Stage 7 valuation result passed into Stage 9;
- existing financial calculations and output contracts.

Do not silently substitute mock data, stale results, or results from a different company or period.

If a required upstream producer or interface genuinely does not exist, do not invent one. Make any independently safe implementation changes, then identify the exact missing interface, its expected data contract, and why a safe connection cannot yet be made.

## Task 3 — Add meaningful integration coverage

Add a focused test that exercises the actual application entry point and its real orchestration path, using the project's existing fixtures and production interfaces wherever possible.

The test must distinguish actual integration from a unit test that directly calls the orchestration function with fabricated objects.

Verify, as applicable:
- the actual entry point reaches Stage 7 and Stage 9;
- upstream company/period mismatches fail closed;
- the as-of market price is selected from persisted eligible observations;
- market-price provenance survives into the valuation result;
- the same valuation result reaches Stage 9;
- missing mandatory inputs or missing eligible prices do not silently produce a decision.

Use mocks only for external boundaries that genuinely require isolation. Do not mock away the integration being tested.

If actual integration is impossible because a required producer or application entry point is absent, add only tests that can be grounded in existing real interfaces and explicitly document the missing piece. Do not label such tests end-to-end coverage.

## Task 4 — Keep scope controlled

Do not attempt to solve the entire historical Point-in-Time problem in this task. A Jalali as-of price selection is not proof that every upstream input was available at that time.

Do not claim complete historical parameter versioning. Do not alter the deferred D1–D6 policies or resolve the separate known Stage 7 policy/test blockers by weakening tests.

## Final response

Report:
1. The exact real application entry point and call chain found.
2. Every production file changed and why.
3. The exact integration test added and what real path it exercises.
4. The exact command(s) the user should run locally; do not run them yourself.
5. Any missing producer/interface that prevents a complete connection.
6. Remaining Point-in-Time, historical-versioning, alert-contract, and Stage 7 freeze blockers.

A report-only response is insufficient if a safe, supported implementation is possible. Do not claim completion without concrete code changes and a test that meaningfully verifies the connection.

Stage 7 must remain unfrozen until the documented requirements and blockers have been resolved or explicitly accepted.