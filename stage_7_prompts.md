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
# P9 — Alert Contract and Naming Consistency Audit

Work only in the local project folder `analyzer`. Read the latest `temp_report2.md`, the locked Stage 7 specification, and only the relevant Stage 7 alert-generation, schema, parameter, and test code.

## Objective

Resolve what can be established from the existing contract about required alert names, emitted alert names, severity, and output representation—without inventing alert semantics.

## Tasks

1. Build a complete matrix of every alert required by the Stage 7 specification and every alert or flag currently emitted by the engine.
2. For each row, record:

   * Exact required name and specification section.
   * Current emitted name, if any.
   * Whether the mapping is an exact semantic match, a demonstrable naming mismatch, or an unresolved semantic gap.
   * Existing trigger condition, severity, evidence, and test coverage.
3. Pay particular attention to:

   * `VALUATION_BENCHMARK_DIVERGENCE`
   * Historical and industry valuation divergence names.
   * `INSUFFICIENT_PEER_DATA`
   * `POOR_DATA_QUALITY`
   * `NEGATIVE_EPS`
   * `SIGN_CHANGE`
   * `POINT_IN_TIME_WARNING`
   * The five unresolved sensitivity/dependence alerts from P7.
4. Determine whether any naming correction can be made without changing trigger semantics, severity, public output behavior, or the meaning of existing flags.
5. Implement a correction only if the mapping is unambiguous from the locked specification and existing behavior. If a correction requires a product or financial decision, leave the code unchanged and document the exact decision required.
6. Add focused tests for any genuinely unambiguous correction. Never remove, weaken, or rewrite an existing test merely to obtain a pass.

## Validation

Run the focused Stage 7 tests and the complete `src/tests/test_stage7_valuation.py` suite using the project's intended virtual environment. Record exact commands, collected/passed/failed/skipped counts, and any failures.

Report the six validation layers separately. Do not claim the overall Stage 7 blockers are resolved merely because a naming mismatch was corrected.

## Boundaries

No modifications to Stages 1–6 or 8–9. No dependency/config changes. No remote Git operations or GitHub/API. Do not declare Stage 7 frozen.

Append `P9 — Alert Contract and Naming Consistency Audit` to `temp_report2.md`, preserving all earlier content. Stop.
=============================================================
# P10 — Model Parameterization and Determinism Audit

Work only in local folder `analyzer`. Read the latest Stage 7 reports and inspect only the Stage 7 specification, `src/valuation/engine.py`, `models.py`, `parameters.py`, `schema.py`, and `src/tests/test_stage7_valuation.py`.

## Objective

Identify and, where explicitly justified by the existing specification, correct Stage 7 model constants that are hardcoded instead of versioned parameters. Preserve financial behavior unless the specification clearly requires a change.

## Tasks

1. Trace every model weight, threshold, score blend, cap, perturbation, normalization rule, and fallback default used by Stage 7.
2. Create a table containing:

   * Constant or formula.
   * Current value and source location.
   * Specification section and requirement.
   * Whether the value is versioned in `parameters.py`.
   * Whether the value is explicitly specified, indirectly supported, or unspecified.
   * Risk if changed or left hardcoded.
3. Investigate P7's finding that confidence/risk/dispersion blend weights and related constants are hardcoded.
4. Check whether parameter changes can preserve deterministic output and model-version traceability.
5. Implement only a strictly specification-backed parameterization correction that preserves existing outputs. Add tests proving that the default outputs are unchanged and that the intended parameter is actually consumed.
6. If a value or formula lacks a specification basis, do not select a replacement value. Record the required decision instead.
7. Do not attempt to solve the unresolved flip-risk, dependence, margin-risk, sector-mapping, or PIT contract blockers by inference.

## Validation

Run the focused Stage 7 test file and the relevant Stage 9 consumer test file. For any production change, compare representative pre-change and post-change outputs and report exact differences. If no safe change is justified, make no code changes and report why.

Report all six validation layers, marking each as executed, partial, absent, or blocked. Include exact test commands and results.

## Constraints

No changes to Stages 1–6 or 8–9. Do not change dependencies, migrations, or unrelated valuation code. No remote Git operations, GitHub/API, commits, pushes, pulls, or branch changes. Do not declare Stage 7 frozen.

Append `P10 — Model Parameterization and Determinism Audit` to `temp_report2.md`. Preserve earlier reports and stop.
=============================================================
# P11 — Stage 7 Consolidated Regression and Evidence Audit

Work in the local project folder `analyzer`. This is a bounded verification task, not a repository-wide review.

Read the latest `temp_report2.md` and inspect only the Stage 7 files changed or referenced by P2–P10, plus the specific test files needed to verify regression claims.

## Objective

Establish a reliable current baseline after P2–P10 and identify whether any claimed fix, regression result, or validation layer lacks direct evidence.

## Tasks

1. Reconcile all reported Stage 7 test counts from P2 through P10. Identify the exact current tests and expected outcomes; do not treat the two P2 failing-first tests as passing.
2. Verify whether the latest test code still contains:

   * `test_p2_sector_driver_decomposition_missing`
   * `test_p2_required_flip_dependence_alerts_missing`
     If either is absent or changed, investigate the exact diff and explain why. Do not restore or rewrite tests without evidence and a specific justification.
3. Run the full Stage 7 test file and the Stage 9 consumer tests using the intended virtual environment.
4. Run the full available test suite with the project's established command. If the PDF-extraction tests require a specific unavailable fixture, report the exact exclusion and reason. Do not substitute unrelated PDFs for a fixture with different expected content.
5. For every command, record the exact command, environment, collected count, passed, failed, skipped, errors, and duration when available.
6. For any failure, capture the exact test name and failure summary. Separate:

   * Current Stage 7 blockers.
   * Regressions caused by recent changes.
   * Unrelated pre-existing failures.
   * Environment or fixture limitations.
     Do not attribute failures to a category without evidence.
7. Reassess all six validation layers using fresh evidence where possible. Explicitly distinguish genuine Stage 5-to-Stage 7 integration from benchmark-series PIT verification.
8. Produce a final unresolved-findings register with severity, evidence, affected requirement, prerequisite decision, and the next bounded action.

## Constraints

* Prefer read-only verification; change code only to repair a newly proven regression caused by P2–P10, and only if the fix is narrow and specification-backed.
* Never weaken tests, invent formulas, suppress unexplained failures, or claim unexecuted tests passed.
* Do not modify Stages 1–6 or 8–9.
* No remote Git operations, GitHub/API, commits, pushes, pulls, or branch changes.
* Stage 7 must remain unfrozen unless a future independent audit explicitly approves it and the user separately authorizes the freeze decision.

Append `P11 — Stage 7 Consolidated Regression and Evidence Audit` to `temp_report2.md`, preserving all earlier reports. Stop.
========================================================
# P12 — Remove the UTC Deprecation Warning Safely

Work in the local project folder `analyzer`.

## Objective

Fix the documented `datetime.datetime.utcnow()` deprecation warning in Stage 7 without changing valuation behavior.

## Scope

* `src/valuation/engine.py`
* `src/tests/test_stage7_valuation.py`, only if a focused regression test is needed.

Inspect only the relevant datetime construction and normalization paths, their existing tests, and the latest `temp_report2.md`.

## Requirements

1. Locate every relevant `datetime.utcnow()` use in the scoped Stage 7 code.
2. Replace deprecated naive-UTC construction with timezone-aware UTC construction, preserving the existing output contract and normalization rules.
3. Do not change valuation dates, cutoff semantics, PIT behavior, calculation formulas, alert triggers, or model parameters.
4. Do not claim that this closes the PIT blocker. It only addresses datetime construction and code hygiene.
5. Add a focused test if needed to establish that generated timestamps remain UTC-aware and deterministic behavior remains unchanged apart from the wall-clock timestamp.
6. Do not modify existing tests to weaken assertions.

## Validation

Run the complete Stage 7 test file and Stage 9 consumer tests using the project virtual environment.

Record exact commands, environment, counts, failures, and warnings. Compare representative pre-change and post-change outputs, excluding only the wall-clock calculation timestamp where appropriate.

Report all six validation layers separately. Clearly identify any layer not freshly executed.

## Boundaries

Do not modify Stages 1–6 or 8–9, the Stage 7 specification, dependencies, migrations, or unrelated code. No remote Git operations, GitHub/API, commits, pushes, pulls, or branch changes. Do not declare Stage 7 frozen.

Append `P12 — UTC Deprecation Cleanup Report` to `temp_report2.md`, preserving all prior content. Stop.
================================================================
# P13 — Stage 7 Point-in-Time Contract Impact Assessment

Work in the local project folder `analyzer`.

## Objective

Prepare an evidence-based impact assessment for closing the Stage 7 point-in-time (PIT) blocker. Do not implement a new contract until its design is approved.

Read the latest `temp_report2.md`, the relevant sections of `07_Stage7_Valuation.md`, Stage 7 source/schema/tests, and only the upstream forecast interfaces and existing callers needed to trace benchmark inputs.

## Tasks

1. Trace every caller that supplies:

   * `historical_pe_values`
   * `industry_forward_pe_values`
   * `industry_ttm_pe_values`
   * `valuation_date`
   * `market_price_date`
   * `data_cutoff_datetime`
2. For each caller, document the actual value shape, date/provenance information available, and whether the source can supply publication/availability timestamps and report versions.
3. Compare the two principal contract options:

   * **Option A:** Per-observation provenance records validated against the cutoff.
   * **Option B:** Explicit caller attestation of PIT validity, together with a defined valuation-date/cutoff policy.
4. Include Option C from P8: retain the V1 limitation and correct the specification and stress-test claims. Explain precisely which PIT guarantees would remain unavailable.
5. For each option, identify affected callers, schema/API compatibility risks, migration needs, test cases, and the smallest viable implementation boundary.
6. Determine whether Stage 7 can validate PIT correctness using current inputs alone. Separate verified facts from assumptions.
7. Recommend an option, but do not select or implement it on the user's behalf.
8. Do not modify frozen Stage 1–6 files. If an option would require changing a frozen interface, state that explicitly rather than making the change.

## Validation

This is an impact-assessment task. Do not claim runtime PIT enforcement or integration tests were executed unless they actually were. Report the six validation layers, marking design-only or unavailable layers explicitly.

## Constraints

Read-only: no source, test, schema, specification, parameter, dependency, or configuration modifications. No invented dates or provenance. No remote Git operations or GitHub/API. Do not declare Stage 7 frozen.

Append `P13 — Stage 7 PIT Contract Impact Assessment` to `temp_report2.md`, preserving all prior content. Stop.
=============================================================
# P14 — Stage 7 Parameter-Version Registry Design

Work in the local project folder `analyzer`.

## Objective

Design the smallest auditable mechanism for Stage 7 model-parameter versioning that addresses P8 D9 and P10 findings. This is a design-only task.

Read the latest `temp_report2.md` and inspect only the relevant Stage 7 specification sections 40 and 64–65, `src/valuation/parameters.py`, `src/valuation/engine.py`, `src/valuation/schema.py`, and focused tests.

## Required analysis

1. Distinguish:

   * Values already explicitly specified and versioned.
   * Values currently versioned but lacking numeric specification support.
   * Hardcoded formulas/weights that the specification says must be versioned.
   * Defaults, rounding rules, and numerical guards with no explicit specification basis.
2. Compare the P8 options:

   * In-code parameter registry.
   * Database-backed parameter table.
   * V1 methodology fixed in code with model-version changes only.
3. For each option, explain auditability, determinism, compatibility, persistence, implementation cost, and whether it requires touching frozen stages or migrations.
4. Address the required record fields from section 65:
   `model_version`, `parameter_name`, `parameter_value`, `effective_from`, and `description`.
5. Explain how historical parameter versions remain immutable and how the engine selects the effective version for a valuation date or cutoff. Do not assume the required selection rule is already defined if the specification does not say so.
6. Propose a minimal registry schema and a validation strategy, but label all new design choices as proposals requiring approval.
7. Do not invent replacement weights, thresholds, fallback defaults, rounding rules, or dispersion methodology.
8. Do not wire the dead `high_dependence_share` parameter until its dependence formula is decided.
9. Do not make code changes or modify the specification.

## Validation

This is a design-only task. Report the six validation layers and clearly mark runtime layers as not executed. Include proposed unit, boundary, immutability, version-selection, determinism, and regression tests for a future implementation.

## Constraints

No source, test, spec, dependency, migration, or configuration changes. No changes to Stages 1–6 or 8–9. No remote Git operations or GitHub/API. Do not declare Stage 7 frozen.

Append `P14 — Stage 7 Parameter-Version Registry Design` to `temp_report2.md`, preserving all earlier content. Stop.
=============================================================
# P15 — Post-P12 Regression Verification

You are working in the local project folder `analyzer`.

## Objective

Perform a fresh, read-only regression verification after P12's UTC timestamp change. Establish the current test baseline before any further Stage 7 implementation.

## Scope

* `src/valuation/engine.py`
* `src/valuation/parameters.py`
* `src/valuation/models.py`
* `src/valuation/schema.py`
* `src/tests/test_stage7_valuation.py`
* `src/tests/test_stage9_decision.py`
* The existing test suite, using the same PDF-test exclusion documented in `temp_report2.md`
* `temp_report2.md`, for appending the report only

Do not perform repository-wide exploration. Do not modify source code, tests, specifications, dependencies, or configuration. Do not modify frozen stages.

## Required work

1. Read the latest reports in `temp_report2.md`, especially P10-P14.

2. Verify that P12's UTC-aware `calculation_timestamp` change is still present and that the two known P2 failing-first tests remain intact.

3. Run these commands using the project's configured virtual-environment Python interpreter:

   * `python -m pytest src/tests/test_stage7_valuation.py -q`
   * `python -m pytest src/tests/test_stage9_decision.py -q`
   * `python -m pytest src/tests/ -q -rs --ignore=src/tests/test_codal_pdf_extraction.py`

   Run them from the project root and substitute the actual virtual-environment interpreter path if required. Do not use the system Python if it lacks project dependencies.

4. Record exact collected, passed, failed, skipped, and error counts for every command. Identify each failure by test name and compare it with the documented baseline.

5. Investigate whether any failure is new. Do not fix failures in this read-only task. Do not treat a skipped or excluded PDF test as passed, and do not substitute unrelated PDFs for missing fixtures.

6. Recheck deterministic output and the P12 timestamp test as part of the focused suite. Report any warning counts accurately.

## Six mandatory validation layers

Report each layer separately:

1. Unit/formula
2. Contract/boundary
3. Production-path/integration
4. Adversarial/negative
5. Regression/full suite
6. Independent audit

For each layer, label evidence as freshly executed, carried forward, static-only, unavailable, or blocked. Do not present carried-forward evidence as a fresh run.

## Reporting and safeguards

Append a `P15 — Post-P12 Regression Verification Report` section to `temp_report2.md`; preserve all existing content.

No remote Git, GitHub/API calls, commits, pushes, pulls, branch changes, or source edits. Do not weaken tests or claim Stage 7 is ready to freeze. Stop after reporting the results.
===================================================================
# P16 — Stage 7 Unresolved-Decision Gate

You are working in the local project folder `analyzer`.

## Objective

Produce a concise, evidence-backed decision package for unresolved Stage 7 specification and contract issues. This is a read-only analysis task; do not implement any proposed decision.

## Scope

Read only the relevant sections of:

* `temp_report2.md`, especially P8-P14 and the unresolved-findings register
* `07_Stage7_Valuation.md`, particularly sections 39-65, 69, and 85
* `src/valuation/engine.py`
* `src/valuation/parameters.py`
* `src/valuation/schema.py`
* `src/tests/test_stage7_valuation.py`

Do not inspect the whole repository or modify any source, test, specification, dependency, or configuration file.

## Required decision register

For each item below, report: current evidence, exact missing decision, feasible options, compatibility or financial-correctness risk, recommended default if a recommendation is justified, and tests required after approval.

D1. `ASSESSMENT_FLIP_RISK`: perturbation set, flip definition, and severity.
D2. `HIGH_MULTIPLE_DEPENDENCE`: definition of multiple-dependence share and threshold usage.
D3. `HIGH_EPS_DEPENDENCE`: EPS-dependence measure and interaction with D2.
D4. `MARGIN_ASSUMPTION_RISK`: required inputs and trigger definition.
D5. `HIGH_IMPACT_HIGH_UNCERTAINTY`: impact and uncertainty formulas, inputs, and thresholds.
D6. Sector-specific drivers for non-financial companies, banks, and holdings, including the missing industry mapping and NAV/P-NAV calculation contract.
D7. Point-in-Time correctness: provenance per benchmark observation versus caller attestation versus explicitly documented V1 limitation. Include the P13 finding that no production caller currently supplies the benchmark inputs.
D8. Alert-name mismatches between sections 49 and 54-55 and the names emitted by the engine. Distinguish naming changes from missing trigger semantics.
D9. Parameter registry and effective-version selection: compare P14's in-code registry proposal, a database-backed registry, and a fixed V1 approach. Explicitly identify the unresolved `as_of` rule for `effective_from` selection.

## Decision integrity

* Do not choose on the user's behalf.
* Do not invent formulas, thresholds, perturbation sizes, industry mappings, date policies, or severity rules.
* Separate decisions that can be made independently from decisions that depend on others.
* Identify any specification statements or stress-test PASS claims that currently overstate implemented behavior.
* Distinguish a proposal from a user-approved decision.
* Do not remove, weaken, or rewrite the two known failing-first tests.

## Six-layer validation

Report all six layers: unit/formula, contract/boundary, production-path/integration, adversarial/negative, regression/full suite, and independent audit. Clearly mark any layer that was not executed because this task is design-only.

## Report

Append a `P16 — Stage 7 Unresolved-Decision Gate Report` section to `temp_report2.md`, preserving all existing content. Include a short final table listing each decision as `REQUIRES USER DECISION`, `DEPENDENT ON ANOTHER DECISION`, or `DOCUMENTATION CORRECTION REQUIRED`.

No source or specification edits, no remote Git operations, no commits, pushes, pulls, or branch changes. Do not freeze Stage 7. Stop after appending the report.
======================================================================
# P17 — Stage 7 Specification Correction Draft (READ-ONLY)

You are working in the local project folder `analyzer`.

## Objective

Prepare an evidence-backed draft of the minimum documentation corrections needed to prevent the Stage 7 V1 specification from claiming behavior that the current implementation does not enforce.

## Scope

Inspect only:

* `temp_report2.md`, especially P11-P16
* Relevant passages in `07_Stage7_Valuation.md`: sections 42-57, 64-65, 69, and stress tests 77-79 and 85
* `src/valuation/engine.py`
* `src/valuation/schema.py`
* `src/tests/test_stage7_valuation.py`

Do not perform repository-wide exploration.

## Required analysis

1. Identify each specification statement or stress-test PASS claim that overstates implemented behavior.
2. For each item, provide:

   * Exact section or test identifier
   * Evidence from the current implementation and tests
   * Proposed replacement wording
   * Whether the change would defer a V1 requirement, narrow a guarantee, or merely correct a factual claim
   * Any financial-correctness or compatibility consequence
3. Cover at least:

   * Flip-risk and dependence alerts
   * Sector-driver decomposition and P/NAV
   * Point-in-Time provenance and stress test 85
   * Alert-name and trigger mismatches
   * Parameter-version registry requirements
4. Do not silently mark a required feature as implemented or remove a requirement merely because it is difficult.
5. Separate corrections that are factually mandatory from optional V1-to-V2 deferrals that require explicit user approval.
6. Do not modify the specification, tests, source, or configuration. Do not choose unresolved D1-D9 decisions on the user's behalf.

## Six-layer validation

Report all six layers: unit/formula, contract/boundary, production-path/integration, adversarial/negative, regression/full suite, and independent audit. Mark runtime testing as not applicable where appropriate for this documentation-only task; distinguish static verification from executed tests.

## Reporting

Append `P17 — Stage 7 Specification Correction Draft Report` to `temp_report2.md`. Include a proposed patch-style draft for review, but do not apply it.

No remote Git operations, commits, pushes, pulls, branch changes, or test weakening. Stage 7 remains unfrozen. Stop after reporting.
============================================================
# P18 — Stage 7 Decision-Independent Work Inventory (READ-ONLY)

You are working in the local project folder `analyzer`.

## Objective

Identify whether any meaningful Stage 7 implementation or validation work can proceed safely without resolving the outstanding decisions D1-D9.

## Scope

Use `temp_report2.md` P11-P17 and inspect only the Stage 7 specification passages, valuation implementation, schema, parameters, and focused tests necessary to verify each candidate.

Do not perform a repository-wide review.

## Required work

1. Build a candidate list of outstanding Stage 7 tasks.
2. For every candidate, classify it as exactly one of:

   * `SAFE TO IMPLEMENT NOW`: the required behavior, formula, and acceptance criteria are explicitly defined; no unresolved D1-D9 decision is needed.
   * `SAFE TO TEST ONLY`: behavior is specified, but implementation would require an additional investigation or contract confirmation.
   * `BLOCKED ON USER DECISION`: a formula, threshold, mapping, severity, contract change, date policy, or version-selection rule remains unresolved.
   * `DOCUMENTATION ONLY`: the change concerns correcting a false claim or accurately documenting a known limitation.
3. For each candidate, state:

   * Exact specification section
   * Relevant implementation location
   * Required scope and files
   * Dependencies on other decisions
   * Tests required, including boundary and adversarial cases
   * Whether a public output or contract version change may be required
4. Re-verify the two known P2 failing-first tests. Do not remove, weaken, skip, or rewrite them.
5. Do not implement anything in this prompt. In particular, do not infer missing financial formulas, thresholds, industry mappings, or PIT policy.
6. If no substantive implementation is safe without user decisions, state that explicitly rather than manufacturing work.

## Six-layer validation

Report unit/formula, contract/boundary, production-path/integration, adversarial/negative, regression/full suite, and independent audit separately. Clearly distinguish executed tests from static review, carried-forward evidence, and blocked work.

## Reporting

Append `P18 — Stage 7 Decision-Independent Work Inventory Report` to `temp_report2.md`, preserving all previous content.

No source, test, or specification changes. No remote Git operations, commits, pushes, pulls, or branch changes. Do not freeze Stage 7. Stop after reporting.
======================================================================

# P19 — Stage 7 Factual Specification Corrections (Bounded Implementation)

You are working locally in the `analyzer` folder on a financial-data application.

## Objective

Apply only the factual documentation corrections established by P17. Do not implement valuation logic and do not resolve any open D1-D9 decision.

## Context and mandatory safeguards

* Financial correctness, auditability, point-in-time correctness, deterministic behavior, and explicit financial invariants take priority over speed.
* Treat `temp_report2.md` as the evidence source for P17 and P18. Inspect the relevant report sections and the exact current text before editing.
* The specification is `07_Stage7_Valuation.md`; the relevant implementation files include `src/valuation/engine.py`, `src/valuation/schema.py`, and `src/valuation/parameters.py`.
* Do not modify Python source, tests, schemas, dependencies, migrations, configuration, or files belonging to frozen stages.
* Do not weaken, delete, skip, or rewrite failing tests to make the result appear successful.
* Do not access GitHub, remote APIs, remotes, branches, commits, pushes, or pulls.
* Append the final report to `temp_report2.md`; never overwrite existing content.
* Stage 7 remains unfrozen.

## Permitted work

Make narrowly scoped, evidence-backed corrections in `07_Stage7_Valuation.md` only:

1. **Stress test 77 / D1:** Replace the unsupported PASS claim with a factual statement that the required flip-risk alert is not implemented in the current implementation and D1 remains unresolved.
2. **Stress test 78 / D2:** Replace the unsupported PASS claim with a factual statement that the multiple-dependence formula is not implemented and D2 remains unresolved. Explain that the existing `high_dependence_share = 0.60` definition is not wired into a production formula.
3. **Stress test 79 / D3:** Replace the unsupported PASS claim with a factual statement that the required EPS-dependence behavior is not implemented and D3 remains unresolved. Identify `FORECAST_RISK` as an undefined/unimplemented alternative name unless the current specification contains evidence to the contrary.
4. **Stress test 85 / D7:** Remove the false claim that PIT protection has passed. State that the current Stage 7 boundary does not enforce report-publication/version provenance or date-safe benchmark selection. Explicitly label PIT enforcement as unresolved; do not declare caller responsibility to be the approved policy.
5. **Section 49 alert capability list:** Add an evidence-backed implementation-status annotation distinguishing implemented alerts, flag-only outputs, and absent/unimplemented capabilities. Do not silently treat a flag as equivalent to a severity-bearing alert. Preserve all existing required names and record naming mismatches rather than choosing a renaming strategy.
6. **Sections 42-44 / D6:** State factually that the current driver analysis emits only `EPS` and `TARGET_PE`, and that `industry_code` and `nav_per_share` do not currently drive sector-specific calculations. Do not decide whether these requirements are deferred to V2.
7. **Section 47 / D9:** Correct any wording that implies a versioned parameter record or selection mechanism already exists, where code inspection confirms that it does not. State that the required registry/selection mechanism is unresolved.
8. **Sections 54-55 / D8:** Add a concise mapping of required specification names versus the names actually emitted by the current engine. Preserve distinctions between above/below conditions. Do not rename outputs, add aliases, or change consumer-facing contracts.
9. **Unsupported trigger thresholds:** Where the specification implies that threshold values have been formally specified but evidence shows they exist only in implementation/tests, explicitly distinguish implementation behavior from specification-approved policy. Do not ratify or change numeric values.

## Decision firewall

D1-D9 remain unresolved. Do not:

* choose any formulas, shock sizes, perturbation sets, thresholds, severity rules, or precedence rules;
* select or implement an industry mapping or sector-driver formula;
* decide the PIT enforcement policy;
* decide between alert renaming, aliases, or specification adoption of current names;
* implement a parameter registry or select an `as_of` policy;
* mark any feature as deferred to V2 unless that deferral has already been explicitly authorized;
* change the meaning of a public contract.

If a proposed wording would implicitly make one of these decisions, leave that wording unchanged and document the blocker in the report.

## Validation requirements — six layers

Report all six layers separately, with exact commands and outcomes:

1. **Unit/formula:** Confirm no valuation formula or implementation changed; run focused tests if feasible.
2. **Contract/boundary:** Verify that no public Python signature, schema, output name, or boundary behavior changed.
3. **Production-path/integration:** Verify that only the specification file changed and no consumer or runtime behavior was altered.
4. **Adversarial/negative:** Confirm that the two known P2 failing tests remain present and were not weakened; identify their actual outcomes if executed.
5. **Regression/full suite:** Run the focused Stage 7 and Stage 9 tests, then the applicable full suite using the established project commands. Report exclusions and skips explicitly. If execution is blocked or too expensive, report that as blocked rather than claiming success.
6. **Independent audit:** Compare the final specification wording against the relevant engine implementation and the P17 findings. Check for accidental D1-D9 decisions and false PASS claims.

Distinguish freshly executed results from carried-forward results, static checks, and blocked work. Do not present the existing two P2 failures as new regressions if their status is unchanged.

## Report and completion

Append `P19 — Stage 7 Factual Specification Corrections Report` to `temp_report2.md`. Include:

* exact specification sections changed;
* a concise before/after description of each correction;
* confirmation that no source/test/configuration files changed;
* six-layer validation evidence;
* remaining D1-D9 blockers;
* confirmation that no remote Git operation occurred and Stage 7 remains unfrozen.

Inspect the final diff before reporting. Do not stop with a proposal: complete the permitted documentation corrections and validation, or clearly report any specific blocker preventing completion.
===========================================================
# P20 — Independent Audit of Stage 7 Specification Corrections

You are working locally in the `analyzer` folder on a financial-data application.

## Objective

Independently audit the completed P19 changes. Determine whether the specification now accurately describes the current Stage 7 implementation without implying that unresolved financial behavior is implemented or approved.

This is an audit task, not a feature implementation task.

## Required scope

Inspect only:

* `temp_report2.md`, including the P17, P18, and P19 reports;
* `07_Stage7_Valuation.md`, limited to the sections modified by P19 and the related sections 10, 42-57, 64-65, 69, 77-79, and 85;
* `src/valuation/engine.py`;
* `src/valuation/schema.py`;
* `src/valuation/parameters.py`;
* the two known failing test bodies in `src/tests/test_stage7_valuation.py`;
* relevant Stage 7 and Stage 9 test results, using the established commands.

Do not perform a repository-wide review.

## Audit checklist

1. Verify that stress-test PASS claims 77, 78, 79, and 85 no longer falsely imply that missing behavior is implemented.
2. Verify that the specification accurately distinguishes implemented alerts, flag-only outputs, and missing alert behavior.
3. Verify that required alert names and current emitted names are documented accurately without silently renaming, aliasing, or merging signals.
4. Verify that sector-driver and P/NAV limitations are described factually, without treating D6 as decided.
5. Verify that missing parameter-version registry behavior is described accurately, without selecting D9 or an `as_of` policy.
6. Verify that unsupported thresholds are not presented as formally approved merely because code or tests contain numeric values.
7. Verify that PIT limitations are stated accurately without silently adopting caller attestation or another D7 policy.
8. Confirm that P19 did not alter source code, tests, public contracts, schemas, dependencies, migrations, or configuration.
9. Confirm that the two known P2 failing tests remain intact and were not weakened, deleted, skipped, or rewritten to pass.
10. Check for inconsistencies introduced by P19 between the specification, code, and prior reports.

## Required validation — six layers

Report all six independently:

1. Unit/formula: static verification that no formulas or valuation code changed; report any focused tests freshly executed.
2. Contract/boundary: inspect the relevant signatures, schema, and public output names.
3. Production-path/integration: confirm whether runtime and consumer paths remain unchanged.
4. Adversarial/negative: verify the two known failing tests still expose the unresolved requirements; execute them if possible and report actual results.
5. Regression/full suite: run the established Stage 7, Stage 9, and applicable full-suite commands. Report exact counts, exclusions, skips, warnings, and failures. Clearly separate fresh results from earlier P15/P19 results.
6. Independent audit: compare the final documentation directly against the implementation and P17 findings. Identify any unsupported claim or accidental decision.

Do not fabricate test results. Do not call carried-forward results freshly executed. Do not treat a skipped or excluded test as passed.

## Remediation boundary

* Do not edit source code, tests, or the specification during the audit.
* Do not fix findings silently. If a discrepancy remains, list the exact section/file and proposed minimal correction.
* If P19 introduced an error, report it precisely and stop; wait for a follow-up correction prompt.
* Do not choose or infer any D1-D9 policy.
* Do not perform remote Git operations, commits, pushes, pulls, or branch changes.

## Report

Append `P20 — Independent Audit of Stage 7 Specification Corrections Report` to `temp_report2.md`, preserving all existing content.

Conclude with exactly one evidence-based status:

* `PASS — Documentation accurately describes current implementation; no audited overclaims remain.`
* `FAIL — Documentation still contains one or more material inaccuracies.`
* `BLOCKED — Audit could not be completed; list the precise blockers.`

A PASS applies only to the documentation audit. It does not mean Stage 7 is feature-complete or ready to freeze.

Confirm that Stage 7 remains unfrozen. Do not freeze any stage and do not perform remote Git operations.
====================================================================
# P21 — Stage 7 Section 55 Factual Wording Refinement

You are working locally in the `analyzer` folder on a financial-data application.

## Objective

Apply the one minor wording refinement identified by P20's independent audit in `07_Stage7_Valuation.md`, section 55, concerning `INDUSTRY_BENCHMARK_INSUFFICIENT`.

## Evidence to verify first

Read the P20 report in `temp_report2.md` and inspect:

* Section 55 of `07_Stage7_Valuation.md`;
* the relevant flag-generation logic in `src/valuation/engine.py`;
* the peer-count logic and `MIN_INDUSTRY_PEERS` definition.

Verify the current implementation before editing.

The wording must accurately distinguish these facts:

1. The engine can emit `INDUSTRY_BENCHMARK_INSUFFICIENT` when `target_source == "INSUFFICIENT_DATA"`.
2. The specification's peer-count condition (fewer than 8 valid peers) is not equivalent to that emission condition.
3. A case with fewer than 8 valid peers may have a usable historical benchmark and therefore may not emit `INDUSTRY_BENCHMARK_INSUFFICIENT`.
4. The existing `INSUFFICIENT_PEER_DATA` flag is a separate signal and must not be conflated with `INDUSTRY_BENCHMARK_INSUFFICIENT`.

## Strict scope

* Modify only the ambiguous wording in section 55 of `07_Stage7_Valuation.md`.
* Do not modify Python source, tests, schemas, dependencies, migrations, configuration, or any other specification section.
* Do not change alert names, emission conditions, severity, thresholds, or output contracts.
* Do not choose D8 or imply that the current implementation satisfies the specification's peer-count trigger.
* Do not access remote Git/GitHub/APIs or perform commits, pushes, pulls, or branch changes.
* Preserve all existing content in `temp_report2.md` and append the report only.

## Six-layer validation

Report all six layers separately:

1. **Unit/formula:** Verify that no financial logic changed; report any tests actually executed.
2. **Contract/boundary:** Confirm that public signatures, schema, alert names, and output contracts remain unchanged.
3. **Production-path/integration:** Confirm that no runtime file changed.
4. **Adversarial/negative:** Verify that the wording accurately describes the case where peer count is below 8 but a historical benchmark remains usable.
5. **Regression/full suite:** Run the focused Stage 7 and Stage 9 tests. Run the established full suite if feasible; report exact counts, skips, exclusions, and failures. Do not call existing P2 failures new regressions.
6. **Independent audit:** Compare the final sentence against the actual flag and peer-count logic. Confirm that D8 remains unresolved.

Clearly distinguish freshly executed tests from carried-forward results and static checks.

## Report and completion

Append `P21 — Stage 7 Section 55 Wording Refinement Report` to `temp_report2.md`.

Include the exact wording changed, the code evidence, all six validation layers, and confirmation that Stage 7 remains unfrozen. Inspect the final diff. If the existing wording is already accurate or the evidence does not support the proposed correction, do not force an edit; document the finding instead.
==============================================================
# P22 — Stage 7 D1-D9 Evidence-Based Decision Brief

You are working locally in the `analyzer` folder on a financial-data application.

## Objective

Prepare a concise but technically rigorous decision brief for the project owner covering unresolved Stage 7 decisions D1-D9.

This is a READ-ONLY analysis task. The report must help the owner make explicit policy choices before implementation. You must not make those choices on the owner's behalf.

## Context and constraints

* Financial correctness, auditability, point-in-time correctness, determinism, and explicit financial invariants take priority over speed.
* Review `temp_report2.md` reports P11-P21, especially the unresolved decision inventory, and inspect only the relevant sections of `07_Stage7_Valuation.md` and the specific implementation/tests needed to substantiate each decision.
* Relevant code includes `src/valuation/engine.py`, `models.py`, `parameters.py`, and `schema.py`.
* Relevant tests include `src/tests/test_stage7_valuation.py` and, where a consumer contract is implicated, `src/tests/test_stage9_decision.py`.
* Do not perform a repository-wide review.
* Do not modify source code, tests, schemas, specifications, dependencies, migrations, or configuration.
* Append the decision brief to `temp_report2.md` without overwriting prior reports.
* Do not access remote Git/GitHub/APIs or perform commits, pushes, pulls, or branch changes.
* Stage 7 remains unfrozen.

## Required output: nine separate decisions

Create one decision section for each item below. Do not merge decisions simply because they are related.

### D1 — Assessment flip risk

Document the unresolved choices concerning:

* what qualifies as a status/assessment flip;
* the perturbation method and which inputs are perturbed;
* how perturbation sizes should be established and versioned;
* how severity is determined;
* how the alert interacts with existing valuation outputs.

Do not invent shock percentages or formulas. If the existing specification/code does not establish a value, explicitly say so.

### D2 — Multiple dependence

Document:

* what "multiple dependence" must measure;
* the formula needed to calculate the dependence share;
* how `high_dependence_share = 0.60` would be used only after the metric is defined;
* missing-data and denominator behavior;
* the interaction with D3 and D1.

Do not wire the existing constant into code.

### D3 — EPS forecast dependence

Document:

* what constitutes EPS dependence;
* the candidate metric and required input data, if grounded in the existing contract;
* the relationship to D2 and any escalation/precedence rule;
* whether `FORECAST_RISK` should be a separate name, alias, or excluded requirement.

Present naming choices neutrally. Do not select one.

### D4 — Margin assumption risk

Document the current contract limitation: Stage 7 does not expose a defined margin series for the proposed risk calculation.

Compare only evidence-supported options:

* explicit contract expansion with provenance and validation;
* a proxy metric, only if the owner can define and approve one;
* documented non-implementation pending a later decision.

Do not create a proxy formula or imply that a proxy already exists.

### D5 — High impact plus high uncertainty

Document the missing definitions for impact, uncertainty, their combination, trigger thresholds, and input selection.

Explain the dependency on D6 if a complete sector-driver framework is required. Separate any work that is independently definable from work that genuinely depends on D6.

Do not reuse engine-chosen perturbation sizes or uncertainty weights as though they were approved financial policy.

### D6 — Sector-specific driver chains and P/NAV

Document the required chains separately:

* Non-financial: Revenue → Operating Margin → Operating Profit → Net Profit → EPS → Fair Value.
* Bank: Loans/Deposits → NII/NIM → Net Profit → EPS → Fair Value.
* Holding: NAV → NAV Growth → Net Profit → EPS → Fair Value, with P/NAV assigned to Stage 7.

Identify which source fields, formulas, sector mappings, and contract expansions are missing. Explicitly account for the rule that Stage 7 must use Stage 5 EPS forecasts rather than rebuild EPS using a new share count.

Do not invent industry-code mappings or valuation formulas. State any dependencies that cannot be resolved from current evidence.

### D7 — Point-in-Time enforcement

Compare these policy options without choosing one:

* per-observation provenance structures and explicit enforcement;
* caller/upstream attestation with a precisely specified ordering/validation rule;
* a documented V1 limitation.

For each option, identify contract changes, enforcement strength, auditability, migration/consumer impact, and residual lookahead risk. Do not claim that metadata alone enforces PIT correctness.

Explicitly account for valuation date, data cutoff, report publication date/version, benchmark observation dates, and historical EPS availability. Do not invent a date-ordering policy.

### D8 — Alert names and trigger semantics

Document the observed name mismatches, including:

* `VALUATION_BENCHMARK_DIVERGENCE` versus the current `WATCH:VALUATION_ABOVE/BELOW_TARGET_PE` family;
* `HISTORICAL_VALUATION_DIVERGENCE` versus the current historical above/below family;
* `INDUSTRY_VALUATION_DIVERGENCE` versus the current industry above/below family;
* the difference between `INSUFFICIENT_PEER_DATA` and `INDUSTRY_BENCHMARK_INSUFFICIENT`;
* the difference between flag-level signals and severity-bearing alerts;
* missing trigger definitions for `POOR_DATA_QUALITY` and `POINT_IN_TIME_WARNING`.

Compare renaming, aliases, and adopting current output names in the specification. Evaluate public-contract stability and consumer compatibility. Do not implement or select a strategy.

### D9 — Parameter registry and version selection

Compare:

* a structured in-code registry;
* a persistent database-backed registry;
* another versioning approach only if it is already supported by evidence in the project.

Assess auditability, reproducibility, effective-date selection, testability, cross-stage coupling, migration burden, and historical backtest safety.

Explicitly analyze why the selection timestamp (`as_of`) is unresolved: valuation date, data cutoff, or another policy cannot be chosen without owner approval and a clear temporal contract.

Do not build a registry or decide a timestamp policy.

## Decision quality requirements

For every D1-D9 section, include:

1. Current verified behavior and precise evidence (file/function/spec section or test).
2. The unanswered policy question.
3. Evidence-supported options, clearly separated from recommendations.
4. Financial correctness risks and possible failure modes.
5. Public contract, downstream consumer, and regression implications.
6. Required inputs and definitions before implementation.
7. Required tests once the owner approves a policy.
8. Explicit dependencies on other decisions.
9. What cannot safely be implemented before approval.

Do not invent missing formulas, data fields, thresholds, severities, mappings, dates, or defaults. If a decision has no evidence-supported answer, say so directly.

## Prioritization

Provide a dependency-aware ordering for discussing the decisions. Explain the rationale and mark any ordering as a proposed discussion sequence, not an approved implementation plan. Do not claim that one decision is already resolved.

Identify any factual/documentation-only task that remains safe regardless of policy decisions, but do not implement it in this prompt.

## Six-layer validation

Report all six layers, distinguishing static review from test execution:

1. **Unit/formula:** inspect relevant formulas and identify undefined ones; do not create new formulas.
2. **Contract/boundary:** inspect relevant input/output schemas and identify the precise contract changes each option would require.
3. **Production-path/integration:** trace only relevant call paths and Stage 9 consumer dependencies where needed.
4. **Adversarial/negative:** enumerate missing-data, stale/future data, sign-change, threshold-boundary, and consumer-compatibility cases that must be tested once a policy is approved. Do not claim these were executed unless they were.
5. **Regression/full suite:** this is read-only, so tests need not be run unless required to verify a specific claim. If tests are run, report exact commands and counts; otherwise label historical test counts as carried forward.
6. **Independent audit:** cross-check all nine decision sections against P11-P21, the specification, and the relevant code. Ensure no decision is implicitly selected by wording.

## Report format

Append `P22 — Stage 7 D1-D9 Evidence-Based Decision Brief Report` to `temp_report2.md`.

End with:

* a one-page executive summary of the nine decisions;
* a compact decision table with options, dependencies, and contract impact;
* a proposed discussion sequence;
* the exact unresolved items that still require owner approval;
* explicit confirmation that no implementation or policy choice was made.

Stage 7 must remain unfrozen. Stop after appending the report.
==================================================================
# P23 — Stage 7 Remaining Stress-Test PASS Claims Audit (READ-ONLY)

You are working locally in the `analyzer` folder on a financial-data application.

## Objective

Independently audit the remaining PASS claims in sections 71-76 and 80-84 of `07_Stage7_Valuation.md`. P19 corrected sections 77-79 and 85, but P22 identified these remaining sections as not yet audited for possible overclaims.

This task is READ-ONLY. Do not change the specification or any implementation files.

## Required scope

Inspect only:

* `temp_report2.md`, especially P17-P22;
* `07_Stage7_Valuation.md`, sections 71-76 and 80-84, plus only the directly referenced specification requirements;
* relevant functions in `src/valuation/engine.py`, `models.py`, `parameters.py`, and `schema.py`;
* the exact tests or test fixtures referenced by those stress-test sections.

Do not conduct a repository-wide review.

## Audit procedure

For every individual test section from 71 through 76 and 80 through 84:

1. Quote or precisely identify the current claimed result and expected behavior.
2. Identify the exact implementation function and relevant input/output contract.
3. Determine whether the behavior is implemented, partially implemented, absent, or impossible to verify from available evidence.
4. Verify whether the test's claimed PASS has actually been supported by an executed test, a reproducible test fixture, or only a specification assertion.
5. Identify any missing negative, boundary, missing-data, determinism, or integration checks relevant to that claim.
6. Recommend the smallest factual correction if the claim overstates current behavior.
7. Clearly separate factual documentation corrections from changes that would require an owner decision under D1-D9.

Do not infer implementation from a specification requirement alone. Do not infer test execution from the presence of a PASS label. Do not invent formulas, thresholds, data, or acceptance criteria.

## Decision firewall

* Do not implement missing financial logic.
* Do not select or infer any D1-D9 decision.
* Do not declare features deferred to V2 without explicit owner approval.
* Do not weaken, delete, skip, or rewrite tests to make claims pass.
* Do not change source code, tests, schemas, configuration, dependencies, migrations, or specification.
* Do not access remote Git/GitHub/APIs, and do not perform commits, pushes, pulls, or branch changes.

## Six-layer validation

Report all six layers separately:

1. **Unit/formula:** static inspection of formulas and exact test claims.
2. **Contract/boundary:** confirm the relevant inputs and outputs exist and match the claimed behavior.
3. **Production-path/integration:** trace only the relevant production path and consumer where applicable.
4. **Adversarial/negative:** identify whether negative, boundary, missing-data, and determinism checks exist; do not claim they ran unless they did.
5. **Regression/full suite:** no full suite is required for this read-only audit. If tests are executed to verify a claim, report exact commands, counts, failures, skips, and exclusions. Otherwise clearly label historical counts as carried forward.
6. **Independent audit:** cross-check every section's conclusion against both code and its cited tests.

## Report

Append `P23 — Stage 7 Remaining Stress-Test PASS Claims Audit Report` to `temp_report2.md`.

Include a table with one row per audited section and these columns:

* section;
* claimed behavior;
* implementation evidence;
* test evidence;
* verdict (`SUPPORTED`, `PARTIALLY SUPPORTED`, `UNSUPPORTED`, or `UNVERIFIABLE`);
* minimal documentation correction, if needed;
* D1-D9 dependency, if any.

Conclude with the exact set of corrections safe to make without an owner decision, and the findings that must remain blocked.

Stage 7 remains unfrozen. Preserve all prior report content and stop after appending the audit report.
====================================================================
# P24 — Stage 7 Evidence-Backed Stress-Test Documentation Corrections

You are working locally in the `analyzer` folder on a financial-data application.

## Objective

Apply only factual documentation corrections supported by the completed P23 audit for stress-test sections 71-76 and 80-84 in `07_Stage7_Valuation.md`.

## Mandatory prerequisite

Read the complete P23 report from `temp_report2.md` first.

If P23 is missing, incomplete, or does not provide specific code/test evidence for a proposed correction, do not guess. Record the blocker in the report and make no speculative edit.

## Scope

For each of sections 71-76 and 80-84:

1. Compare its current claim against the P23 verdict and evidence.
2. Correct a claim only if P23 demonstrates that the wording materially overstates or misrepresents actual behavior.
3. Preserve claims that P23 found to be supported.
4. Where behavior depends on an unresolved D1-D9 decision, state the verified current limitation and leave the policy undecided.
5. Do not label a feature deferred to V2 unless the owner has explicitly approved that deferral.
6. Do not convert an unexecuted test into an executed PASS claim.

Modify only the minimum necessary text in `07_Stage7_Valuation.md` for the audited sections. Do not modify other specification sections unless P23 identifies a direct contradiction that cannot be corrected within the audited section; if so, report it and stop for authorization.

## Prohibited changes

* No Python source, tests, schemas, dependencies, migrations, or configuration changes.
* No new financial formulas, thresholds, severities, mappings, defaults, or date-ordering policies.
* No D1-D9 decision selection or implementation.
* No deletion, weakening, skipping, or rewriting of failing tests.
* No remote Git/GitHub/API access; no commits, pushes, pulls, or branch changes.
* Do not overwrite or truncate `temp_report2.md`.

## Six-layer validation

Report all six layers separately:

1. **Unit/formula:** prove that no formula or runtime logic changed.
2. **Contract/boundary:** confirm public signatures, schemas, output names, and boundary behavior are unchanged.
3. **Production-path/integration:** confirm no runtime or consumer files changed.
4. **Adversarial/negative:** check that the revised wording preserves the actual limits and negative cases identified in P23.
5. **Regression/full suite:** run the focused Stage 7 and Stage 9 tests. Run the applicable full suite if feasible. Report exact commands, counts, warnings, skips, exclusions, and failures. Do not describe historical results as freshly executed.
6. **Independent audit:** compare every edited section against P23 and the actual implementation. Confirm that no unsupported PASS claim remains within the authorized scope and no unresolved decision was silently selected.

If no correction is warranted, leave the specification unchanged and explain why.

## Completion and report

Append `P24 — Stage 7 Stress-Test Documentation Corrections Report` to `temp_report2.md`.

Include:

* the exact sections edited, if any;
* before/after wording for each edit;
* why each correction is supported by evidence;
* sections reviewed but deliberately left unchanged;
* six-layer validation results;
* remaining D1-D9 blockers;
* confirmation that Stage 7 remains unfrozen and no remote Git operation occurred.

Inspect the final diff and stop after reporting. Do not implement any valuation feature as part of this task.
========================================================================
# P25 — Stage 7 D1–D9 Consolidated Owner Decision Package

You are working in the existing local project folder `analyzer`, a financial-data application. Use OpenCode Desktop's available local workspace tools. Do not assume Claude Code-specific capabilities.

## Objective

Prepare one comprehensive, evidence-backed owner decision package covering **all unresolved Stage 7 decisions D1–D9**, so the project owner can make informed decisions in one review instead of repeated exploratory rounds.

This is a READ-ONLY analysis task. Do not implement any decision or modify source code, tests, schemas, migrations, configuration, dependencies, or Stage 7 specifications.

## Context and strict boundaries

1. Read `temp_report2.md`, focusing on P17–P24, including the latest P23 and P24 reports. Treat any explicitly superseded draft as superseded.
2. Read only the relevant sections of `07_Stage7_Valuation.md` and the directly relevant implementation/contracts/tests, including as needed:

   * `src/valuation/engine.py`
   * `src/valuation/models.py`
   * `src/valuation/parameters.py`
   * `src/valuation/schema.py`
   * `src/forecast/repo.py`
   * `src/decision/engine.py`
   * `src/tests/test_stage7_valuation.py`
   * `src/tests/test_stage9_decision.py`
3. Do not perform a repository-wide review. Follow dependencies only when required to answer a specific D1–D9 question.
4. Preserve the existing known failures:

   * `test_p2_sector_driver_decomposition_missing`
   * `test_p2_required_flip_dependence_alerts_missing`

   Do not weaken, delete, skip, rewrite, or mask them.
5. Do not perform GitHub/API/remote operations, commits, pushes, pulls, or branch changes.
6. Do not invent financial formulas, thresholds, perturbation sizes, severities, mappings, defaults, effective dates, rounding policies, or acceptance criteria.
7. Existing implementation behavior is evidence, not automatic approval of that behavior as financial policy. Clearly distinguish:

   * existing verified behavior;
   * existing but unapproved implementation choices;
   * missing behavior;
   * decisions requiring owner approval.
8. Stage 7 remains unfrozen.

## Required decision coverage

Prepare a decision record for every item below:

* **D1 — Assessment flip risk:** What constitutes a meaningful valuation-assessment flip, how it is measured, and which conditions/severity should trigger an alert.
* **D2 — High multiple dependence:** Definition and calculation of multiple dependence; assess the existing `high_dependence_share = 0.60` and whether it has any live use. Do not activate it automatically.
* **D3 — EPS dependence and forecast revision:** Define the unresolved EPS-dependence concept, its relation to `FORECAST_RISK`, and whether/how Stage 5 revision evidence should reach Stage 7. Account for P23/P24's finding that Stage 7 currently does not produce `POSITIVE_FORECAST_REVISION`.
* **D4 — Margin assumption risk:** Identify the missing data/contract requirements and possible implementation boundary. Do not fabricate a margin series or infer it from unavailable data.
* **D5 — High impact plus high uncertainty:** Identify existing sensitivity/uncertainty mechanisms, distinguish implementation constants from approved policy, and specify which decisions are required before an alert can be implemented.
* **D6 — Sector driver chains:** Assess the required non-financial, bank, and holding chains. Identify evidenced inputs, absent inputs, source-of-truth requirements, and safe integration boundaries. Stage 7 must consume Stage 5 EPS forecasts and must not rebuild EPS using a new share count.
* **D7 — Point-in-time correctness:** Evaluate dated benchmark observations, historical availability, report publication/version dates, forecast cutoffs, and backtest leakage. Compare viable enforcement approaches and identify required caller/contract changes.
* **D8 — Alert contract and naming:** Reconcile required specification names with actual emitted flags/alerts, including `FORECAST_RISK`, `POSITIVE_FORECAST_REVISION`, `INSUFFICIENT_PEER_DATA`, `INDUSTRY_BENCHMARK_INSUFFICIENT`, and the P21/P23/P24 findings. Consider Stage 9 consumer compatibility. Do not rename outputs yet.
* **D9 — Parameter/model versioning:** Evaluate the current parameter implementation against Section 64/65 requirements, including `effective_from`, `model_version`, and the unresolved as-of selection rule. Compare an in-code registry with a persistent registry only to the extent supported by the existing architecture.

## Required format for EACH D1–D9 decision

Provide one compact but substantive table row or clearly labeled record containing:

1. Current verified behavior, with file/function/section/test evidence.
2. Exact unresolved policy question.
3. Two or three viable options, including a no-change/V1-limitation option when legitimate.
4. Recommended option, explicitly marked **PROPOSAL — NOT APPROVED**.
5. Rationale and financial correctness/auditability trade-offs.
6. Required inputs, data provenance, contract changes, and downstream consumers.
7. Failure modes and missing-data behavior; missing must not silently become zero.
8. Focused positive, boundary, negative, adversarial, determinism, and regression tests needed.
9. Dependencies on other D-items and a safe implementation order.
10. A concise owner decision statement that can be approved or rejected without another discovery round.

Do not force a decision when evidence is insufficient. State precisely what evidence is missing and propose the smallest bounded follow-up investigation.

## Consolidated design requirements

After the nine individual decision records, provide:

A. A dependency graph and recommended implementation sequence, explaining which items can proceed independently and which must wait for decisions.

B. A cross-decision contract impact matrix covering Stage 5 → Stage 7 → Stage 9, schemas, alerts, parameters, and point-in-time data.

C. A proposed implementation/test plan divided into small, independently auditable work packages. Do not implement them.

D. A list of decisions the owner must approve, with explicit choices and proposed defaults. Mark every default as a proposal, not an existing requirement.

E. A list of items that can be resolved through factual documentation correction without changing financial policy, separated from policy decisions.

F. A clear statement of which decisions are genuinely blocked and which can be resolved from existing evidence.

## Validation and reporting

Apply all six validation layers, adapted to this read-only task:

1. **Unit/formula:** trace existing relevant formulas and identify formula gaps without inventing replacements.
2. **Contract/boundary:** inspect required inputs, outputs, types, missing-data behavior, and downstream compatibility.
3. **Production-path/integration:** trace only the relevant Stage 5/7/9 paths.
4. **Adversarial/negative:** identify boundary, missing-data, stale-data, leakage, and conflicting-evidence cases.
5. **Regression/full-suite:** inspect existing test evidence. Do not claim tests were run unless they were actually executed in this task; do not run the full suite merely for a read-only design report unless needed to resolve a specific factual question.
6. **Independent audit:** cross-check every recommendation and claimed current behavior against code/spec/test evidence. Separate verified facts from assumptions and proposals.

Append the complete report to `temp_report2.md` under the heading:

`P25 — Stage 7 D1–D9 Consolidated Owner Decision Package`

Never overwrite previous reports. Include the date, exact files inspected, evidence references, unresolved questions, and whether any tests were freshly executed. Make no other file changes.

Finish with a concise owner decision summary. Do not start implementation, do not declare Stage 7 complete or frozen, and stop after reporting.
=================================================================
# P26 — Independent Audit of the D1–D9 Decision Package

You are working in the existing local project folder `analyzer` using OpenCode Desktop.

## Objective

Independently audit the newly appended report `P25 — Stage 7 D1–D9 Consolidated Owner Decision Package` in `temp_report2.md`.

The goal is to deliver a decision package that is complete enough for the owner to approve or reject the proposed choices in one review. This is a READ-ONLY audit, not an implementation task.

## Scope

1. Read the entire P25 report and relevant P17–P24 findings in `temp_report2.md`.
2. Verify disputed or material claims against the exact relevant passages in `07_Stage7_Valuation.md`, the directly relevant Stage 7/Stage 5/Stage 9 implementation, schemas, parameters, and tests.
3. Do not repeat the whole P25 investigation unless necessary to verify a material claim.
4. Do not perform a repository-wide review.
5. Do not modify source code, tests, schemas, configuration, dependencies, migrations, or specification files.
6. Do not perform remote Git/GitHub/API operations, commits, pushes, pulls, or branch changes.
7. Do not choose or implement any owner policy. Recommendations remain proposals requiring explicit approval.
8. Preserve the two known P2 failing tests; never weaken, delete, skip, or rewrite them.
9. Stage 7 remains unfrozen.

## Audit checklist

For every D1–D9 item, assign exactly one verdict:

* `READY_FOR_OWNER_DECISION`
* `PARTIALLY_READY`
* `NOT_READY`

Verify that:

* Every recommendation is distinguishable from verified existing behavior.
* No formula, threshold, severity, perturbation size, default, mapping, or effective-date rule is presented as approved without evidence.
* All unresolved owner choices are explicit and answerable.
* Missing data is not implicitly treated as zero or as valid evidence.
* Point-in-time constraints and provenance are addressed wherever relevant.
* Stage 7 consumes Stage 5 EPS forecasts without rebuilding EPS using a new share count.
* Alert changes account for Stage 9 compatibility.
* D-item dependencies and implementation ordering are coherent.
* Test proposals cover positive, boundary, negative, adversarial, determinism, integration, and regression behavior where applicable.
* No known failure is misrepresented as a passing test.
* No unsupported claim of production readiness, completeness, or freeze is made.

## Required output

Append a new section to `temp_report2.md` titled:

`P26 — Independent Audit of the D1–D9 Decision Package`

Include:

1. A nine-row verdict table, one row per D1–D9 item.
2. For each defect, the exact P25 statement/section involved, the verified contradiction or missing evidence, its financial or integration risk, and the smallest correction needed.
3. A list of cross-item contradictions, especially D1–D5 dependencies, D3/D8 revision naming and routing, D6 sector inputs, D7 point-in-time enforcement, and D9 parameter selection.
4. A concise list of owner decisions that are genuinely ready for approval.
5. A separate list of decisions that are not ready, with the exact missing evidence.
6. A final overall verdict:

   * `READY_FOR_OWNER_REVIEW` only if the package is internally consistent and all material choices are explicitly presented;
   * otherwise `NEEDS_TARGETED_REVISION`, identifying only the specific gaps that prevent review.
7. A proposed next implementation sequence conditional on owner approval, without executing it.

## Six-layer validation

Explicitly report:

1. Formula/unit evidence audit.
2. Contract/boundary audit.
3. Production-path/integration audit.
4. Adversarial/missing-data/PIT audit.
5. Regression-test evidence audit, clearly distinguishing freshly run tests from prior report results and static inspection.
6. Independent consistency audit.

Do not run unrelated tests simply to produce activity. If execution is required to verify a material claim, use the project's existing environment and report the exact command and outcome.

Do not edit P25 or any prior report. Append this audit only to `temp_report2.md`. Do not change any other file.

Stop after appending the report. Do not begin implementation, do not declare Stage 7 complete or frozen, and do not perform remote operations.
===========================================================================
# P27 — Targeted Repair and Final Readiness Review of Stage 7 D1–D9 Decisions

You are working in the existing local project folder `analyzer` using OpenCode Desktop.

## Objective

Produce one corrected, internally consistent, owner-ready decision package for Stage 7 decisions D1–D9, using the independent findings in P26.

This is a bounded documentation/report task. Do not implement financial policy or change runtime behavior.

The objective is to avoid another discovery round: correct the known defects, verify material claims, and produce explicit options that the owner can approve or reject.

## Authoritative context

Read:

* `temp_report2.md`: P25 and the complete P26 independent audit, plus relevant earlier findings P17–P24.
* Only the specification, implementation, and tests necessary to verify disputed claims.

Treat P26 as the authoritative audit of P25's defects. Do not redo the full P25 investigation. Recheck underlying code where required to verify a correction.

## Strict boundaries

* Do not modify source code, tests, schemas, migrations, dependencies, configuration, or `07_Stage7_Valuation.md`.
* Do not edit or rewrite P25 or P26; preserve both as historical records.
* Append new material only to `temp_report2.md`.
* No GitHub/API/remote operations, commits, pushes, pulls, or branch changes.
* Do not invent financial formulas, thresholds, severity mappings, defaults, dates, rounding rules, industry mappings, or acceptance criteria.
* Do not convert any proposal into an approved policy.
* Preserve the known P2 failures:

  * `test_p2_sector_driver_decomposition_missing`
  * `test_p2_required_flip_dependence_alerts_missing`
* Never weaken, delete, skip, rewrite, or mask those tests.
* Stage 7 remains unfrozen.

## Required corrections

### 1. D2, D3 and D5 — Correct the exact metric degeneracy

P26 verified that the current symmetric +10% one-at-a-time shocks to the multiplicative valuation `EPS × target P/E` produce equal `EPS` and `TARGET_PE` impacts in the tested path: 50% each. Their current uncertainty and review-priority values are also identical by construction.

Therefore:

* Explicitly withdraw the P25 recommendation to use the current `driver_impact` shares with a 0.60 threshold as a working dependence-alert formula.
* Explain why the existing metric cannot reliably distinguish EPS dependence from multiple dependence.
* Do not activate `high_dependence_share = 0.60`.
* Do not claim that D2/D3 alerts will work if implemented using those shares unchanged.
* Correct D5 to acknowledge that its current two-driver inputs cannot meaningfully discriminate between the drivers using the existing impact/uncertainty outputs.

Present a small set of genuinely distinct options for D2/D3, for example:

* retain the current V1 limitation and do not emit the new alerts;
* investigate a scenario-spread or other non-degenerate attribution approach;
* investigate an asymmetric-shock or elasticity approach.

These are research/design options only. Do not present an unverified sketch as an implemented or financially validated formula. For each option, identify the additional policy choices, inputs, and tests needed.

For D2/D3 alert co-occurrence, explicitly present the alternatives: both alerts may fire, a defined precedence rule may select one, or alerts may be deferred. Do not silently select precedence.

For D3 forecast revisions, make clear that `UPWARD`/`DOWNWARD`/`MIXED` cannot be mapped into family-level bear/base/bull probability evidence without a defined mapping rule. Present this as an explicit owner decision or a bounded design task. Do not invent the mapping.

### 2. D1 — Make the flip-risk proposal decidable

Correct the D1 record so that it no longer describes an incomplete rule as implementation-ready.

Explicitly separate:

* shock variables;
* shock direction (positive, negative, or both);
* shock magnitude;
* what constitutes a status flip;
* severity assignment;
* missing-data and `NOT_APPLICABLE` behavior.

The existing 10% upward shock is an implementation constant used for driver analysis, not approved flip-risk policy. Present it only as a proposal requiring approval.

Provide an owner-answerable severity mapping template with named severity categories but leave unapproved numeric boundaries blank. Do not invent a mapping from band distance to severity.

Include integration tests in the proposed test plan. If a complete decision still requires an owner-specified value, mark it `NOT READY FOR IMPLEMENTATION`, rather than filling the gap by inference.

### 3. D8 — Correct the downstream-consumer evidence

Use P26's verified trace of `DecisionEngine.make_decision` in `src/decision/engine.py`.

Correct all P25 statements and matrix cells that claim Stage 9 currently consumes `alerts`, `valuation_risk_flags`, or `valuation_driver_ranking`.

State only the verified consumer fields, including the relevant valuation status, reliability, risk, confidence, data-quality, margin-of-safety, cutoff, and metadata fields confirmed in P26.

Distinguish:

* verified current Stage 9 dependencies;
* future-consumer compatibility risk;
* audit/history implications of renaming;
* dashboard consumption, which remains unverified.

Do not claim that renaming alert tokens currently breaks Stage 9 when no such dependency was found.

Present D8 options and their trade-offs using the corrected evidence. Include the treatment of absent or mismatched tokens such as `FORECAST_RISK`, `POSITIVE_FORECAST_REVISION`, `POOR_DATA_QUALITY`, and `POINT_IN_TIME_WARNING`. Do not invent triggers for those alerts.

### 4. D6 — Correct the consumer-impact assessment

Remove the unsupported claim that Stage 9 consumes `valuation_driver_ranking`. Keep dashboard usage explicitly unverified.

Preserve the verified contract gap and the restriction that Stage 7 must consume Stage 5 EPS forecasts without rebuilding EPS using a new share count.

Keep sector-chain implementation conditional on an explicit owner decision and evidence-backed input/mapping definitions. Do not invent industry codes or source fields.

### 5. D7 — Make point-in-time choices explicit

Present the viable enforcement options and state what each guarantees and does not guarantee.

Explicitly require the owner or a later approved design specification to determine:

* date-ordering invariants between valuation date, cutoff, publication date, forecast version, and benchmark observation date;
* behavior when an invariant is violated;
* handling of missing dates and missing provenance;
* backtest selection of information available at the historical date.

Do not describe caller attestation as equivalent to mechanically enforced point-in-time correctness. If attestation is proposed for V1, label it as a limitation and identify the residual leakage risk.

### 6. D9 — Preserve the verified evidence and remaining choices

Keep the verified cutoff fallback behavior identified in P26 distinct from a formally approved `as_of` policy.

Present the registry options, version-selection rule, effective-date requirements, and interaction with D7. Do not assume that the existence of a cutoff field by itself establishes complete point-in-time correctness.

### 7. Preserve the valid P25 conclusions

Do not reopen already verified findings without contradictory evidence. In particular:

* D4's absent margin contract is supported.
* D6's required sector inputs/mapping are not currently established.
* D9's registry/versioning decision remains separate from implementation approval.
* The P23/P24 stress-test documentation corrections remain historical evidence.
* The two known P2 failures remain intact and must not be reclassified as passing.

## Required final package

Append the following section to `temp_report2.md`:

`P27 — Corrected D1–D9 Owner Decision Package and Final Readiness Review`

Include:

1. **Correction log:** each P26 finding G1, G2, G3, C1, C2, C3 and M2, with the correction made and the evidence supporting it.
2. **Nine decision records:** for each D1–D9, state verified behavior, unresolved policy, distinct viable options, a clearly labeled proposal if evidence supports one, risks, contract impact, required tests, dependencies, and an owner-answerable decision statement.
3. **Corrected consumer matrix:** verified Stage 5 → Stage 7 → Stage 9 dependencies, separating actual fields from future or unverified consumers.
4. **Decision readiness matrix:** assign exactly one status to each D-item:

   * `READY_FOR_OWNER_DECISION`
   * `PARTIALLY_READY`
   * `NOT_READY`

   A decision can be ready for the owner to choose a direction while remaining not ready for implementation. State this distinction explicitly.
5. **Owner response sheet:** list the smallest practical set of explicit choices the owner must make. Group related D1–D3 choices where appropriate, but do not merge decisions that have different financial meanings. Include a `defer/no new alert in V1` option where legitimate.
6. **Conditional work plan:** small, auditable implementation packages ordered by dependencies. State which packages cannot start until a specific owner decision is approved.
7. **Open evidence list:** only questions that genuinely cannot be resolved from current code, spec, or reports. Do not request a broad new investigation when the gap is a policy choice.
8. **Final verdict:** `READY_FOR_OWNER_REVIEW` only if all material options are understandable, the P26 defects are corrected, and no recommendation relies on the degenerate metrics. Otherwise `NEEDS_TARGETED_REVISION`, naming only the remaining blocking defects.

## Six-layer validation

Perform and report all six layers:

1. Unit/formula evidence: confirm the degenerate-metric correction and do not imply the old 0.60 proposal is viable.
2. Contract/boundary: verify the corrected fields, inputs, outputs, and missing-data constraints.
3. Production-path/integration: verify the Stage 5/7/9 consumer claims against actual code.
4. Adversarial/negative: cover missing values, NaN, non-applicable valuations, shock directions, alert co-occurrence, stale/future data, and absent provenance as design requirements.
5. Regression/full suite: do not run unrelated tests for a report-only correction. Distinguish prior test results, fresh executions, static inspection, and planned tests.
6. Independent audit: after drafting P27, perform a separate verification pass against P26 and the relevant code. Check every material correction and every consumer claim. Do not merely restate the first-pass findings.

Do not claim that a test was executed unless it actually was. Do not describe a design proposal as financially validated merely because it is mathematically computable.

Append the report; never overwrite previous content. No other file changes. Stop after the final readiness verdict. Stage 7 remains unfrozen.
==========================================================
# P28 — تثبیت خط مبنا و رفع دو آزمون ناموفق شناخته‌شده
You are the engineering agent working on the local project folder `analyzer`, a financial-data application.

## Objective

Start Stage 7 remediation with the highest-priority task: establish a fresh, reproducible test baseline and fix the two known Stage 7 failures at their actual root causes.

Known failing tests:

* `test_p2_sector_driver_decomposition_missing`
* `test_p2_required_flip_dependence_alerts_missing`

Relevant evidence is in `temp_report2.md`, especially P26 and P27. Read only the relevant report sections, `07_Stage7_Valuation.md`, and the specific implementation and test files needed for these failures. Do not explore the entire repository.

## Non-negotiable constraints

* Work only in local `analyzer`.
* Do not use GitHub, remote APIs, Git operations, commits, pushes, pulls, or branch changes.
* Never delete, skip, weaken, or rewrite an existing test merely to make it pass.
* Do not manufacture financial inputs, thresholds, formulas, sector mappings, or severity rules.
* Preserve frozen Stages 1–6 and 8–9. Modify their files only if a demonstrated Stage 7 integration defect makes a minimal change strictly necessary; explain the evidence first.
* Stage 7 must consume Stage 5 EPS forecasts. Do not rebuild EPS using an invented share count.
* Alerts are risk/review signals, not buy/sell recommendations.
* Append the report to `temp_report2.md`; never overwrite its history.

## Required execution

1. Record the exact current test baseline before making changes. Run both named tests individually and inspect their complete failure traces. Run the focused Stage 7 suite if practical.
2. Trace each failure through the actual production path, relevant specification, models, and test fixtures. Establish what behavior the test is intended to enforce.
3. Implement the smallest complete root-cause correction supported by existing approved requirements. If a required financial policy is genuinely absent, do not disguise that absence with an arbitrary formula. Derive the most defensible implementation from existing project contracts and documented financial invariants, record the rationale, and add boundary tests. Do not stop at a report-only analysis.
4. Add or correct tests for positive behavior, missing data, invalid inputs, boundary conditions, deterministic repeated runs, and regression behavior. Preserve the two tests and their intended protections.
5. Re-run the exact previously failing tests, the complete Stage 7 suite, and relevant Stage 9 consumer tests. Run the full test suite if feasible.
6. If any failure remains, continue investigating and correcting the same root cause. Do not declare success while known failures are unexplained or concealed.

## Six-layer validation — report each layer separately

1. Unit/formula correctness.
2. Contract and boundary behavior.
3. Production-path/integration behavior.
4. Adversarial and negative cases.
5. Regression and full-suite results.
6. Independent audit of the final diff and test evidence.

For every test command, report the exact command, exit status, passed/failed/skipped counts, and whether it was freshly executed. Separate execution evidence from static inspection. Never count skipped tests as passing.

## Reporting

Append a section titled:

`P28 — Stage 7 Baseline and Root-Cause Remediation`

Include files changed, root causes, implementation rationale, test commands and counts, six-layer results, remaining concrete blockers, and a precise final verdict. Do not claim the entire Stage 7 is complete or frozen. Stop after this bounded task and its independent audit.
