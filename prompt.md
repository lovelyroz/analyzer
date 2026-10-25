# P60 — Fix Stage 9 Dispersion Test Discovery

**Task type: CODE CHANGE — tests only**

## Objective

Correct the four P59 regression tests so that pytest discovers them as independent test functions. The current definitions are indented inside `test_dashboard_contract_carries_required_fields`, so they are not independently collected.

## Allowed file

- `src/tests/test_stage9_decision.py` — the only file permitted to change.
- Create no files.

## Required changes

1. Move these four test functions to the module's top level, using the same indentation as the other top-level test functions:
   - `test_scenario_dispersion_threshold_boundaries`
   - `test_scenario_dispersion_causes_ten_point_confidence_deduction`
   - `test_scenario_dispersion_blocks_strong_buy`
   - `test_scenario_dispersion_penalty_distinct_from_valuation_risk_level_high`

2. Preserve the existing assertions and test intent. Do not weaken or remove assertions to make the tests pass.

3. Confirm by static inspection that all four functions are defined at module scope and are not nested inside another function.

4. Do not modify production code, threshold values, recommendation rules, financial formulas, specifications, or unrelated tests.

## Restrictions

- Do not run tests or CI. The user will run the tests locally.
- Do not use GitHub, GitHub CLI/API, remotes, commits, pushes, pulls, or branch changes.
- Do not perform repository-wide exploration.
- Do not edit `reply.md`, `temp_report.md`, `temp_report2.md`, `stepsForStage7.md`, `stage_7_prompts.md`, or anything in `ClaudeReports/`.
- Do not claim the tests pass or have been executed.

## Required response

Report:
- The exact file changed.
- Confirmation that all four functions are now at module scope.
- Confirmation that no production code or threshold values changed.
- The exact command the user should run:

`.venv\Scripts\python.exe -m pytest src/tests/test_stage9_decision.py -q`

Do not report a test result. Stop after the correction and static inspection.