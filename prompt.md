# P59 — Add Focused Stage 9 Dispersion Regression Tests

## Task Type
CODE CHANGE — test file only.

## Repository
Local working folder: `analyzer`

## Exact File Scope
The only file permitted to change is:
- `src/tests/test_stage9_decision.py`

Do not modify or create any other file.

## Objective
Add focused regression tests for the existing Stage 9 behavior that consumes `valuation_result.metadata["scenario_dispersion"]`.

Inspect `src/decision/engine.py` and the existing test file before editing. Do not assume the existing test helper provides coverage by itself.

## Required Test Coverage
Add tests that verify:

1. A numeric `scenario_dispersion` greater than `0.50` adds `HIGH_EXPECTED_UPSIDE_HIGH_BEAR_RISK` to the conflicts.
2. A value exactly equal to `0.50` does not trigger that conflict.
3. A value below `0.50` does not trigger that conflict.
4. The conflict directly causes the existing 10-point decision-confidence deduction, using a controlled comparison that holds all other inputs constant.
5. The conflict blocks `STRONG_BUY` under otherwise qualifying conditions.
6. Where practical, test the distinction between the conflict's own confidence penalty and the independent penalty for `valuation_risk_level` being `HIGH` or `EXTREME`.

Use existing fixtures/helpers and established test conventions where possible. Keep tests deterministic. Do not fabricate financial records or weaken existing assertions.

## Financial Policy Boundary
These tests document the current Stage 9 implementation behavior only. They do NOT ratify `0.50` as a financially approved threshold and do NOT establish that Stage 9 must dynamically share Stage 7's configurable threshold.

Do not change any threshold, production logic, recommendation rule, or specification. Do not unify the Stage 7 and Stage 9 threshold paths.

If a requested assertion cannot be isolated reliably with the current test helpers, do not force it or alter production code. Explain the limitation in the report.

## Restrictions
- Do not run tests or CI; the user will run them.
- Do not use GitHub, GitHub CLI/API, remotes, commits, pushes, pulls, or branch operations.
- Do not inspect the repository broadly.
- Do not edit `reply.md`, `stepsForStage7.md`, `temp_report.md`, `temp_report2.md`, `stage_7_prompts.md`, or anything under `ClaudeReports/`.
- Do not redesign `engine.py`.

## Required Report
Report:
1. Exact test functions added and the behavior each verifies.
2. The exact file changed.
3. Any requested assertion not added and why.
4. The focused pytest command for the user to run:
   `pytest src/tests/test_stage9_decision.py -q`
5. Explicitly state that tests were not run and no production code or thresholds were changed.

Stage 7 remains OPEN.