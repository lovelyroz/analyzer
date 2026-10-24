# P54 — Correct Stage 7 Historical Parameter Selection (D9)

## Objective

Correct the unresolved D9 issue in the local `analyzer` project. The latest recorded full test run passed, but the current implementation still reports `data_cutoff_used_for_parameter_selection=False`. Do not treat that test result as proof that D9 is complete.

## Required file scope

Read all of these files before proposing changes:

- `stepsForStage7.md`
- `07_Stage7_Valuation.md`
- `src/valuation/parameters.py`
- `src/valuation/engine.py`
- `src/valuation/schema.py`
- `src/valuation/service.py`
- `src/tests/test_stage7_valuation.py`

Modify only `src/valuation/engine.py`, `src/valuation/parameters.py` if strictly necessary, and `src/tests/test_stage7_valuation.py`. Do not edit reports, specifications, handoff files, or other modules.

## Required behavior

1. Determine the effective valuation data cutoff before selecting the parameter set.
2. When a valid cutoff exists, use it as the governing timestamp for historical parameter selection.
3. Do not use `valuation_date` as a substitute when the effective data cutoff differs.
4. If a caller explicitly supplies `parameter_as_of` and it conflicts with the effective cutoff, reject the conflict clearly unless an already documented contract requires a different behavior. Do not silently select parameters using the conflicting timestamp.
5. A dated parameter version may be selected only when its `effective_from` is not later than the governing timestamp. Preserve deterministic handling of overlapping versions and missing historical versions.
6. Do not invent effective dates or retrofit dates onto the undated Genesis parameter set.
7. Preserve the legacy Genesis path where backward compatibility requires it, but mark it explicitly as historically unverified. Do not claim point-in-time parameter selection for that path.
8. If no eligible dated version exists, do not silently fall back to an undated or future-effective set and claim historical validity. Return an explicit error or limitation consistent with the existing API contract.
9. Ensure output metadata truthfully distinguishes dated, cutoff-governed selection from legacy Genesis selection. `data_cutoff_used_for_parameter_selection` must reflect what actually happened, not a hard-coded claim.
10. Preserve financial formulas, existing output contracts, parameter values, the 38-record Genesis registry, and the 33-consumed/5-recorded-not-consumed distinction.

## Required focused tests

Add or update tests for:

- Effective parameter selection using the valuation data cutoff.
- Exact `effective_from` boundary acceptance.
- Rejection of a future-effective version.
- Missing eligible dated versions.
- Overlapping eligible versions.
- Conflicting explicit `parameter_as_of` and effective cutoff.
- Metadata accurately distinguishing dated selection from legacy Genesis fallback.
- Deterministic repeated results.
- Backward compatibility of the legacy path without falsely claiming PIT verification.

Do not weaken or delete existing tests merely to obtain a passing result. Do not add speculative dates or parameter values.

## Execution and reporting restrictions

- Do not run pytest, CI, or any test command. The user will run tests locally.
- Do not perform repository-wide exploration.
- Do not use GitHub, GitHub CLI/API, remotes, push/pull, commits, or branch operations.
- Do not redesign `engine.py`; make only the minimal changes necessary for D9.
- Do not edit `reply.md`, `temp_report.md`, `temp_report2.md`, `stepsForStage7.md`, or `stage_7_prompts.md`.

## Deliverables

Provide:
1. A concise explanation of the actual code changes and why they resolve D9.
2. The exact files changed.
3. The exact focused pytest command for the user to run.
4. Any remaining limitation, especially where no historical parameter version exists.
5. A clear statement that tests were not executed by you.

Do not claim D9 complete until the user supplies actual test results and the resulting code behavior has been reviewed.