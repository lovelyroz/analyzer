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
### P4 — Output Contract and Peer Evidence

Work only in the local project folder `analyzer`. Read the latest Stage 7 reports in `temp_report2.md`.

## Objective

Close the Stage 7 output-contract gap concerning actual industry peer count and verify benchmark provenance.

## Inspect only

* `07_Stage7_Valuation.md`, especially sections 1–20 and 63–69
* `src/valuation/engine.py`
* `src/valuation/schema.py`
* `src/valuation/parameters.py`
* `src/tests/test_stage7_valuation.py`

## Tasks

1. Trace how valid industry-forward-PE peers are filtered, counted, and used in benchmark selection.
2. Verify the distinction between actual valid peer count and the configured minimum of eight.
3. If the existing output contract explicitly requires the actual peer count, implement the smallest backward-compatible Stage 7-only change and add tests. Preserve existing constructor/API compatibility where feasible.
4. Test peer counts below, at, and above the minimum; invalid values; empty data; benchmark fallback; and consistency between the selected benchmark and reported count.
5. Do not mix Forward P/E and TTM P/E populations, change the benchmark hierarchy, or invent missing peer data.

## Validation

Run focused tests and the complete Stage 7 valuation test file. Check serialization/contract compatibility where supported by existing code. Record all six validation layers and identify any layer that cannot be verified with available infrastructure.

Append the report to `temp_report2.md`. Do not modify Stages 1–6, Stages 8–9, or unrelated contracts. No remote Git operations. Stop after the bounded change and report.
==========================================================
#### P5 — Point-in-Time and Adversarial Input Audit

Work only in the local project folder `analyzer`. Read the latest Stage 7 reports in `temp_report2.md`.

## Objective

Audit and close only demonstrable Stage 7 input-validation gaps involving PIT metadata and invalid numerical inputs.

## Inspect only

* `07_Stage7_Valuation.md`, especially sections 56–63
* `src/valuation/engine.py`
* `src/valuation/models.py`
* `src/valuation/schema.py`
* `src/tests/test_stage7_valuation.py`
* Stage 5/6 interfaces only if needed to verify the actual input contract; do not modify them.

## Tasks

1. Trace whether historical benchmark inputs carry dates, publication timestamps, report versions, and cutoff metadata, or arrive as undated numbers.
2. Test zero/negative prices, NaN/infinity, missing values, invalid reliability/data-quality values, and naive/aware datetime handling wherever these inputs are accepted.
3. Reject or explicitly flag invalid inputs when required by the existing contract. Do not silently convert missing values to zero or claim that undated historical values are PIT-safe.
4. Do not invent historical records, report versions, dates, or provenance. If the current interface cannot establish PIT validity, report the limitation and the smallest required contract decision; do not redesign upstream stages.
5. Preserve existing valid calculations and deterministic behavior.

## Validation

Use focused tests for each changed boundary, run the complete Stage 7 test file, and run any directly relevant existing contract tests without modifying them. Report exact commands and counts. Clearly separate verified PIT enforcement from metadata-only claims.

Append the report to `temp_report2.md`. Do not change the Stage 7 specification or frozen stages in this prompt. No remote Git operations. Stop after the audit/fix and report.
===========================================================
#### P6 — Production-Path, Adversarial and Regression Validation

Work only in the local project folder `analyzer`. Read the latest Stage 7 reports in `temp_report2.md`.

## Objective

Perform strict multi-layer validation of the cumulative Stage 7 changes without expanding implementation scope.

## Tasks

1. Inspect only the Stage 7 code/tests changed by P2–P5 and the actual Stage 5/6 output interfaces required to construct a valid integration test.
2. Add or run a production-path integration test using real pipeline-produced forecast objects if the repository supports it. Do not fabricate realistic-looking financial records or bypass production constructors. If genuine integration is impossible, document the precise blocker and test the strongest valid boundary instead.
3. Add adversarial cases for invalid EPS, missing benchmarks, peer-count boundaries, non-finite inputs, cutoff/PIT limitations, scenario ordering, probability normalization, and repeat-run determinism, as applicable to implemented contracts.
4. Run all Stage 7 tests, then the full suite `python -m pytest src/tests/ -q -p no:warnings -rs` using the project's intended local virtual environment.
5. Report all six layers separately. Include exact commands, collected/passed/failed/skipped counts, skip reasons, and whether each layer was freshly executed or carried forward from an earlier report.
6. Do not modify unrelated tests merely to obtain a pass. Investigate and fix any regression introduced by Stage 7 changes.

## Boundaries

Do not change Stages 1–6, Stages 8–9, valuation logic outside the approved Stage 7 scope, dependencies, or migrations. No remote Git operations.

Append the report to `temp_report2.md`. Do not declare Stage 7 frozen. Stop after validation and reporting.
=========================================================
#### P7 — Independent Final Audit and Freeze Gate

Work only in the local project folder `analyzer`.

## Objective

Perform a read-only independent audit of Stage 7 after P2–P6. Decide whether the evidence supports readiness for an explicit freeze decision.

## Inspect only

* `07_Stage7_Valuation.md`
* Stage 7 source files and tests changed during P2–P6
* The P2–P6 reports in `temp_report2.md`
* Relevant Stage 5/6 interface definitions only where needed to verify boundaries

Do not re-run broad repository exploration.

## Audit requirements

1. Independently trace the implemented formulas and alert conditions against the locked specification. Do not rely solely on prior agents' PASS labels.
2. Check financial invariants, invalid/missing data behavior, benchmark hierarchy and peer counts, scenario probability sum, deterministic behavior, version metadata, PIT limitations, and the frozen-stage boundaries.
3. Review test quality for false positives, tautological assertions, insufficient edge cases, and accidental weakening. Verify that each claimed validation layer has concrete evidence.
4. Run the Stage 7 test suite and full test suite using the intended local virtual environment. Record exact commands, counts, skip reasons, and environment details.
5. Classify every remaining finding as BLOCKER, MATERIAL GAP, MINOR GAP, or DOCUMENTED LIMITATION. Separate proven defects from specification ambiguity and missing infrastructure.
6. Return exactly one verdict: `APPROVED FOR EXPLICIT FREEZE DECISION` or `NOT READY FOR FREEZE`. Approval is not itself a freeze declaration.

## Boundaries

Read-only only. Do not edit source, tests, specifications, or reports except appending this audit report to `temp_report2.md`. No commits, pushes, pulls, branch changes, GitHub/API, or other remote operations.

Append the report, preserve all earlier reports, and stop.
===========================================================

# P8 — Stage 7 Specification Decision Package

You are working in the local project folder `analyzer`, a financial-data application.

Read only the Stage 7 specification, relevant Stage 7 source/tests, and the latest reports in `temp_report2.md`. Do not reload or audit the entire repository.

## Objective

Convert the unresolved P7 findings into a precise, evidence-backed decision package. Do not implement speculative formulas.

## Required work

1. Review the two failing P2 tests and the P7 BLOCKER-1 and BLOCKER-2 findings.
2. For each unresolved requirement, identify:

   * The exact specification section.
   * What is explicitly required.
   * What formula, trigger, input, mapping, or acceptance criterion is missing.
   * The smallest specification amendment needed to make implementation testable.
3. Cover at minimum:

   * `ASSESSMENT_FLIP_RISK`
   * `HIGH_MULTIPLE_DEPENDENCE`
   * `HIGH_EPS_DEPENDENCE`
   * `MARGIN_ASSUMPTION_RISK`
   * `HIGH_IMPACT_HIGH_UNCERTAINTY`
   * Sector-driver chains for non-financial companies, banks, and holdings.
   * Benchmark point-in-time provenance and the valuation-date/cutoff relationship.
   * Required alert names versus currently emitted names.
   * Hardcoded model weights or thresholds that should be versioned.
4. For each issue, provide viable alternatives and their financial consequences. Distinguish direct specification evidence from your proposed design choices.
5. Do not select a financial formula, threshold, perturbation size, sector mapping, or PIT policy on the user's behalf.
6. Identify which requirements could be explicitly deferred from V1 and what specification or stress-test claims would then need correction.

## Constraints

* No source, test, specification, parameter, dependency, or configuration modifications.
* Do not alter existing tests or make the two failing tests pass artificially.
* Do not invent financial data or use external assumptions as if they were project requirements.
* Do not modify Stages 1–6 or 8–9.
* No GitHub/API, remote Git, commits, pushes, pulls, branch changes, or remote operations.

## Report

Append a section titled `P8 — Stage 7 Specification Decision Package` to `temp_report2.md`. Include a compact decision table with issue, evidence, missing definition, alternatives, consequences, and required user decision. Report the six validation layers, clearly distinguishing executed from not executed. Do not claim any behavior was implemented or validated when it was not.

Stop after appending the report.
===================================================
