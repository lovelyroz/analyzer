### Stage 7 — Prompt 1: Baseline Audit

You are working in the local project folder `analyzer`, a financial-data application where correctness, auditability, point-in-time (PIT) safety, deterministic behavior, and strict validation are mandatory.

## Objective

Perform a **bounded, read-only Stage 7 baseline audit**. Identify the single highest-priority unresolved implementation or validation gap. Do not implement fixes in this prompt.

## Read only these files

* `07_Stage7_Valuation.md`
* `src/valuation/engine.py`
* `src/valuation/models.py`
* `src/valuation/parameters.py`
* `src/valuation/schema.py`
* `src/tests/test_stage7_valuation.py`
* `06_Stage6_Forecast_Evaluation.md` only if needed to verify the Stage 6 input contract.

Do not scan the whole repository. Consult `temp_report.md` only if a specific historical Stage 7 decision is necessary; do not load the entire report.

## Required actions

1. Compare the existing Stage 7 implementation and tests against the locked Stage 7 specification.
2. Run:
   `python -m pytest src/tests/test_stage7_valuation.py -q`
3. Identify the highest-priority concrete gap, supported by exact file/function and test evidence. Distinguish a proven defect from missing coverage or an unverified assumption.
4. Briefly map the six validation layers: unit/formula, contract/boundary, production-path/integration, adversarial/negative, regression, and independent audit. State which layers have actual evidence and which still need work. Do not claim unexecuted tests passed.
5. Recommend one narrowly scoped next step. Do not modify source, tests, specifications, dependencies, or configuration.

## Non-negotiable boundaries

* Stage 1–6 are frozen. Do not change them.
* Do not modify Stage 8, Stage 9, or unrelated valuation code.
* Do not invent financial data, benchmark values, formulas, or missing-data defaults.
* No GitHub/API, remote Git operations, commits, pushes, pulls, or branch changes.
* Do not weaken or skip tests to obtain a pass.

## Reporting

Append a concise report to `temp_report2.md`; never overwrite existing content. Include files inspected, the exact test command and observed counts, the evidence-backed finding, six-layer status, scope confirmation, and the recommended next step.

Stop after the audit and report. Do not begin implementation.
==============================================================
### P2 — Sensitivity and Alert Test Design

Work only in the local project folder `analyzer`.

## Objective

Extend Stage 7 validation with focused, failing-first tests for the required sensitivity and alert behavior identified in the latest Stage 7 report in `temp_report2.md`.

## Inspect only

* `07_Stage7_Valuation.md`
* `src/valuation/engine.py`
* `src/valuation/parameters.py`
* `src/valuation/schema.py`
* `src/tests/test_stage7_valuation.py`
* The latest Stage 7 report in `temp_report2.md`

## Tasks

1. Inspect the definitions of `SENSITIVITY_PERTURBATION`, `high_dependence_share`, driver impact, driver uncertainty, and the required alerts in specification sections 41–53.
2. Add focused tests for behaviors whose formulas and acceptance criteria are explicitly defined by the existing specification and parameters.
3. Do not invent a formula, perturbation size, threshold, or sector-driver mapping when the specification does not define it. Record each such ambiguity as a specification blocker instead of silently choosing a value.
4. Tests must cover positive, negative, boundary, missing-data, and deterministic/repeated-run behavior where applicable.
5. Run the focused Stage 7 tests and report exact collected, passed, failed, and skipped counts. Expected failures are acceptable only if they expose the intended missing behavior; explain each one.

## Boundaries

* Do not modify production code, specification files, dependencies, or configuration.
* Do not weaken existing tests.
* Do not modify frozen Stages 1–6 or Stages 8–9.
* No remote Git operations or GitHub/API access.

Append the report to `temp_report2.md`. Include exact files changed, test command/results, ambiguities that block implementation, and a six-layer validation status. Stop after tests and reporting.
=====================================================
