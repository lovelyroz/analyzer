# P36 — Correct and Verify Stage 7 Parameter Consumption

**Repository:** `lovelyroz/analyzer`
**Required branch:** `stage7/remediation-2026-10-14`
**Report file:** `temp_report2.md`
**Task type:** Focused implementation and verification — not a repository-wide redesign.

## 1. Critical Context and Known Discrepancy

The previous P35 report claims that `ValuationEngine.calculate_valuation` resolves the parameter set using:

`resolve_parameter_set_as_of(data_cutoff_datetime)`

However, direct inspection of the committed branch showed that `src/valuation/engine.py` still contains:

`resolve_parameter_set(GENESIS_VERSION_KEY)`

The implementation and report therefore disagree. Treat the actual committed source code as authoritative, not the previous report.

The previous incomplete local changes were discarded and were not uploaded. Do not attempt to recover them. Do not assume that P35's claimed implementation exists.

## 2. Branch and Repository Safety

Before editing:

1. Verify that the selected branch is exactly `stage7/remediation-2026-10-14`.
2. Record its current HEAD commit and working-tree state.
3. Do not switch to, commit to, or modify `master`.
4. Do not merge, rebase, or cherry-pick branches.
5. Do not modify frozen stages or unrelated files.
6. Inspect only the files needed for this task:

   * `src/valuation/engine.py`
   * `src/valuation/parameters.py`
   * `src/tests/test_stage7_valuation.py`
   * `src/tests/test_stage9_decision.py`
   * `07_Stage7_Valuation.md`, only where necessary to resolve the existing contract
   * relevant callers and parameter definitions, only as needed

If the required branch cannot be selected or verified, stop before editing and report the exact limitation.

## 3. Objective A — Correct Parameter Resolution

Trace the complete path from:

1. `data_cutoff_datetime` normalization and fallback;
2. parameter-registry selection;
3. every material valuation calculation that uses a parameter;
4. the emitted `parameter_set_version` and `parameter_snapshot`.

Determine the precise behavior supported by the existing specification and contracts.

Implement the smallest safe correction so that the selected parameter set actually governs the calculations and the audit snapshot records the same values used by those calculations.

Requirements:

* Do not merely change the resolver call while leaving calculations dependent on unrelated module-level constants.
* Do not claim successful parameterization unless the values consumed by calculations are demonstrably sourced from the resolved parameter set.
* Preserve existing formulas, financial invariants, Stage 5 EPS forecasts, deterministic behavior, missing-data semantics, and backward-compatibility requirements.
* Do not invent effective dates for existing parameters.
* Do not silently select an unapproved version.
* Do not silently fall back to `GENESIS_VERSION_KEY` when a dated selection is required but unavailable.
* Do not introduce new formulas, thresholds, defaults, rounding rules, or financial policies.
* Do not create synthetic production history to make historical selection pass.
* If the existing contract does not authorize a required behavior, do not guess. Document the exact blocker and complete any independent, contract-supported correction.

Pay particular attention to the distinction between:

* a parameter registry that merely exists;
* a registry that selects a version;
* a version whose values actually govern calculations;
* an audit snapshot that faithfully records the values actually consumed.

These are separate requirements.

## 4. Objective B — Add Decisive Regression Tests

Add focused tests to `src/tests/test_stage7_valuation.py` or the most appropriate existing test module.

Tests must prove, through the actual `calculate_valuation` execution path, that:

1. A dated parameter version is selected correctly at the supported cutoff boundary.
2. The selected parameter values actually govern the relevant calculations.
3. `parameter_set_version` identifies the selected version.
4. `parameter_snapshot` exactly matches the parameter values consumed by the calculation.
5. A missing, ambiguous, invalid, or unavailable version follows the explicit behavior already supported by the contract, without silent fallback.
6. Existing undated-call behavior is preserved only if that behavior is explicitly supported by the current contract.
7. Changing a supported test parameter produces the expected, deterministic change in the relevant output, without modifying the financial formula itself.

Use clearly labeled synthetic registry records only for isolated unit tests of registry mechanics. Never present synthetic dates or values as genuine historical records.

Do not test only the resolver in isolation. At least one test must prove that a selected parameter changes a real calculation result or a directly observable calculation decision.

Do not weaken, delete, skip, or relax any existing test, including the known failing tests.

## 5. Objective C — Verify Point-in-Time Boundaries

Inspect the existing `forecast_input_refs` enforcement and its relationship to `data_cutoff_datetime`.

Preserve the existing check that rejects undated input references and references with `available_at` later than the effective cutoff, where the current contract requires it.

Do not claim complete point-in-time correctness: benchmark observation dating, production caller wiring, and any other previously documented gaps remain open unless this task independently verifies and resolves them under existing contracts.

Do not expand this task into an unsupported PIT redesign.

## 6. Mandatory Validation

Run and record the exact commands, exit codes, durations, and test counts. Use the repository's actual supported test environment.

Run in this order:

1. Newly added focused tests.
2. `python3 -m pytest src/tests/test_stage7_valuation.py -v`
3. `python3 -m pytest src/tests/test_stage9_decision.py -v`
4. `python3 -m pytest src/tests/test_stage7_valuation.py src/tests/test_stage9_decision.py -v`
5. `python3 -m pytest src/tests -v`, if the environment supports it.
6. Independently inspect the final diff and the parameter flow from resolution through calculation to audit metadata.

If the repository requires a different Python or pytest invocation, use the correct command and document why. Do not report tests as executed if they were not actually run.

Apply all six validation layers:

1. Unit and formula correctness.
2. Contract and boundary validation.
3. Actual execution-path integration.
4. Adversarial and negative testing.
5. Regression and broader-suite testing.
6. Independent final-diff audit.

The known tests below must remain intact:

* `test_p2_sector_driver_decomposition_missing`
* `test_p2_required_flip_dependence_alerts_missing`

Investigate their outcomes, but do not invent owner-controlled financial policy to force them to pass. Report them accurately as failures if they still fail.

Do not describe a suite as passing if any test fails. Distinguish fresh executions, historical results, skipped tests, blocked tests, and static inspections.

## 7. Reporting

Append a new section titled:

`# P36 — Correct and Verify Stage 7 Parameter Consumption`

to the end of `temp_report2.md`. Never overwrite or rewrite historical report sections.

Include:

* Starting branch and commit.
* Actual discrepancy found in the committed P35 implementation.
* Exact files changed.
* The parameter-selection behavior implemented and its contract basis.
* A parameter-by-parameter trace showing which calculations consume resolved values.
* Evidence that the audit snapshot equals the values actually consumed.
* New regression tests and what each proves.
* Exact test commands, exit codes, counts, and durations.
* Known failures, skips, and remaining PIT or integration gaps.
* Independent final-diff audit.
* A clear verdict: COMPLETE FOR THE IMPLEMENTED SCOPE, PARTIAL, or BLOCKED.

Do not modify earlier reports to make P35 appear correct retrospectively.

## 8. Completion Conditions

Do not stop after writing an investigation report if a bounded, contract-supported correction can be implemented and validated.

Do not declare this task complete merely because the resolver call was changed or new tests pass in isolation.

P36 is complete only if:

* the committed code contains the correction;
* resolved parameters govern the relevant calculations;
* the audit snapshot accurately reflects consumed values;
* decisive regression tests exercise the actual calculation path;
* validation evidence is fresh and accurately reported;
* the final diff has been independently reviewed.

If a required contract or owner decision is missing, stop only the blocked portion, document the exact missing decision, and finish all independent work that can safely be completed.

Do not merge the branch. Do not freeze Stage 7. Return a concise summary with the branch, commit, changed files, verified test results, and remaining blockers.
