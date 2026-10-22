# P46 — Trace and Complete the Real Application Path Through Stage 7 → Stage 9

You are continuing Stage 7 remediation in the local project directory `analyzer`.

## Confirmed state

P44 added and corrected tests for the callable Stage 7 → Stage 9 orchestration boundary.

P45 added `jdatetime` to `requirements.txt`, strengthened `parse_jalali_components`, and excluded impossible stored Jalali dates in `select_market_price_as_of`.

The user reports that all 14 tests in `src/tests/test_ingestion_ohlc.py` passed after P45.

The current orchestration boundary is `calculate_decision_as_of_jalali` in `src/decision/service.py`. It accepts a Stage 5 forecast and Stage 3/Stage 8 results, invokes the Stage 7 Jalali valuation service, and passes the resulting valuation to `DecisionEngine.make_decision`.

However, previous targeted inspection did not establish a real application caller for this orchestration boundary. A callable function and mock-based unit tests do not prove that the application's actual execution path reaches Stage 9.

## Mandatory operating constraints

- Work locally and only in `analyzer`.
- Do not use GitHub, GitHub CLI/API, remotes, push, pull, commit, or branch-changing operations.
- Do not run tests or CI. The user runs tests and shares the actual outputs.
- Do not edit `reply.md`, `temp_report.md`, `temp_report2.md`, `ClaudeReports/`, `stepsForStage7.md`, or `stage_7_prompts.md`.
- Do not scan the entire repository. Trace only the relevant application entry point(s), Stage 5 forecast service, Stage 3 fundamental result producer, Stage 8 market result producer, Stage 7 valuation service, Stage 9 decision service, and their directly relevant tests.
- Do not redesign `engine.py`; its comprehensive review is reserved for the end of Stage 7 as specified in `stepsForStage7.md`.
- Do not change valuation formulas, EPS behavior, financial thresholds, alert policy, or output contracts to make integration easier.
- Do not invent fundamental or market evidence, silently substitute missing inputs, or claim Point-in-Time guarantees without evidence.
- Do not weaken, delete, or skip existing tests.

## Task A — Trace the real execution path

Identify the actual entry point(s) through which the application performs analysis or generates a decision. Follow the relevant calls far enough to determine:

1. Whether a Stage 5 forecast is generated or retrieved.
2. Where the actual Stage 3 fundamental result is produced or retrieved.
3. Where the actual Stage 8 market result is produced or retrieved.
4. Whether the company identity and reporting/forecast period are consistent across those inputs.
5. Where the valuation and decision results are consumed or returned.
6. Whether the current execution path uses a Gregorian datetime boundary, a Jalali date boundary, or another explicit as-of contract.

Use targeted searches and inspect the smallest relevant set of files. Do not treat a test fixture, example, or mock as a production caller.

## Task B — Implement the smallest safe integration

If a genuine application execution path already supplies the required Stage 5, Stage 3, and Stage 8 results, connect it to `calculate_decision_as_of_jalali` with the smallest justified change.

Preserve existing interfaces where possible. Validate company and period identity before valuation. Ensure the selected market-price observation and its provenance reach Stage 7, and ensure the exact resulting valuation object reaches Stage 9 without Stage 9 recalculating or reconstructing the valuation.

Do not silently change date semantics or convert Jalali dates into Gregorian fields.

If a real execution path exists but lacks a required input, determine whether that input can be supplied from an existing authoritative producer or persisted record without fabricating evidence. Implement the safe connection if possible.

If no genuine application path or no authoritative producer for a required input exists, do not create a fake production flow or manufacture financial evidence. Report the exact missing producer/interface and the smallest justified next implementation step. Still implement any independent, safe integration work that is supported by existing code.

## Task C — Add integration-level regression coverage

Where a genuine entry point can be connected, add a test that exercises that entry point and the real service orchestration, using the project's existing test conventions and database fixtures where practical.

The test must establish that:

- The real entry point invokes the Stage 7 → Stage 9 boundary.
- Real application-produced or persisted inputs are passed through the relevant interfaces.
- Company and period mismatches fail closed.
- The selected market-price observation and provenance are preserved.
- The exact Stage 7 valuation result is passed to Stage 9.
- Missing required inputs cannot silently trigger a fabricated or unrelated valuation.

Use mocks only for external dependencies that genuinely need isolation. A test that directly calls `calculate_decision_as_of_jalali` with fabricated Stage 3/Stage 8 objects is not sufficient evidence of end-to-end application integration.

Do not claim an end-to-end test exists unless it traverses the actual application entry point.

## Task D — Review date and Point-in-Time limitations

Determine whether the real caller provides a defensible Jalali as-of date and whether the required upstream inputs have trustworthy observation/availability provenance.

Do not infer historical availability from the calculation cutoff alone. If the existing data model cannot prove Point-in-Time availability, preserve the current explicit limitation and identify what evidence or schema is missing.

Do not expand this task into full historical parameter versioning or the final `engine.py` review.

## Completion requirements

Make concrete, safe code changes wherever existing authoritative interfaces permit. Do not stop after producing an architectural report if a valid implementation is possible.

If full integration is blocked, provide exact evidence:
- the actual entry point inspected;
- the functions it calls;
- the required producer or interface that is missing;
- why creating a substitute would be financially unsafe;
- the minimum next change needed.

## Final response

Report:

1. The real execution path found, with exact file and function names.
2. Files changed and the specific behavior implemented.
3. Whether Stage 7 → Stage 9 is now called from a genuine application entry point, or why it remains blocked.
4. The integration tests added and exactly what they exercise.
5. The precise test commands the user should run.
6. Explicitly confirm that you did not run tests or CI.
7. Remaining Point-in-Time, historical parameter-versioning, alert-contract, and known Stage 7 test blockers.

Do not edit report files. Do not declare Stage 7 frozen.