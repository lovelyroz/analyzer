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
