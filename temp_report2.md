# Stage 7 Baseline Audit Report (READ-ONLY)

Date (UTC): 2026-10-11
Scope: Stage 7 Valuation Engine baseline audit. No source, test, spec, dependency, or config modifications made. Stages 1-6, 8, 9 untouched. No git operations performed.

## 1. Files Inspected

- D:/winprojects/analyzer/07_Stage7_Valuation.md (locked spec V1, sections 1-88)
- D:/winprojects/analyzer/src/valuation/engine.py (ValuationEngine, ~486 lines)
- D:/winprojects/analyzer/src/valuation/models.py (forward P/E, fair value, margin of safety, median_valid)
- D:/winprojects/analyzer/src/valuation/parameters.py (thresholds, weights, versions)
- D:/winprojects/analyzer/src/valuation/schema.py (ScenarioValuation, ValuationResult)
- D:/winprojects/analyzer/src/tests/test_stage7_valuation.py (11 tests)
- D:/winprojects/analyzer/06_Stage6_Forecast_Evaluation.md (only to verify input contract: Final Reliability is 0-100 scale, sections around line 558)
- D:/winprojects/analyzer/temp_report2.md (confirmed empty before writing; this report is the first content)

## 2. Test Command and Observed Counts

Command (cwd D:/winprojects/analyzer):
D:/winprojects/analyzer/.venv/Scripts/python.exe -m pytest src/tests/test_stage7_valuation.py -q

Result: 11 passed, 0 failed. One pre-existing warning class only: DeprecationWarning for datetime.datetime.utcnow() at src/valuation/engine.py:176 (10 warnings, cosmetic; not part of the finding).

## 3. Evidence-Backed Top Finding

The required sensitivity/dependence alert family (spec sections 49-53; stress tests 77-79) is unimplemented, and the driver analysis it depends on is a fixed stub.

Missing required alerts (spec section 49 uses mandatory language): ASSESSMENT_FLIP_RISK (section 50 calls it one of the most important alerts), HIGH_MULTIPLE_DEPENDENCE (51), HIGH_EPS_DEPENDENCE (52), MARGIN_ASSUMPTION_RISK (53), plus HIGH_IMPACT_HIGH_UNCERTAINTY, POOR_DATA_QUALITY, and POINT_IN_TIME_WARNING. Engine._alerts (engine.py lines 451-485) emits only: HIGH_SCENARIO_DISPERSION, LOW_FORECAST_RELIABILITY, INSUFFICIENT_BENCHMARK_DATA, target/historical/industry divergence WATCH alerts, and an INFO top-driver note. None of the flip-risk or dependence alerts can be produced by any input.

Supporting evidence:
- parameters.py line 72 defines ALERT_THRESHOLDS["high_dependence_share"] = 0.60, but a repository search shows zero references to high_dependence_share anywhere in src/ outside that definition. It is a dead threshold: the dependence-alert logic it was meant to parameterize does not exist.
- _driver_analysis (engine.py lines 430-448) hardcodes exactly two drivers, EPS and TARGET_PE, with identical impact values (|base fair value| x perturbation), so driver_impact is always 50.0/50.0 and uncertainty is identical for both drivers regardless of inputs. There is no sector driver decomposition required by spec sections 42-44 (non-financial Revenue-to-EPS chain, bank Loans/NII chain, holding NAV chain).
- The engine accepts nav_per_share but only stores it in metadata ("nav_per_share_received"); it is never used in any calculation, confirming the holding/NAV path is unwired.
- No test among the 11 covers flip-risk, multiple/EPS dependence, margin-assumption risk, or sector drivers.

Classification: this is missing coverage plus unimplemented required behavior, NOT a proven behavioral defect. All 11 existing tests pass and no test demonstrates incorrect output for implemented paths (forward P/E math, benchmark hierarchy, 8-peer rule, invalid-EPS NULL rule, reliability non-interference, family-level probability evidence, bounded scenario multiples all verified by tests).

Secondary observations (not the top finding):
- Minor contract gap: spec section 69 requires industry_peer_count in the output contract, but ValuationResult has no such field; only the minimum (benchmark_peer_minimum: 8) is recorded in metadata, so consumers cannot see the actual peer count behind an industry median.
- Unverified assumption (not a defect): point-in-time safety. The engine accepts historical_pe_values as undated floats and records "pit_inputs_required": True in metadata, but it has no mechanism to detect future-dated data. PIT correctness therefore rests entirely on the frozen upstream stages; no test exercises a PIT violation.

## 4. Six-Layer Validation Status

1. Unit/formula: HAS EVIDENCE. test_valuation_models plus engine forward-P/E/fair-value/expected-value assertions pass (11/11 total).
2. Contract/boundary: PARTIAL EVIDENCE. 8-peer minimum, benchmark hierarchy fallback order, invalid-EPS NULL handling, and probability-sum-to-100% are tested. Still needs work: industry_peer_count absent from output; historical series not passed through (only median).
3. Production-path/integration: NO EVIDENCE. All tests use a synthetic make_forecast fixture; no test runs the engine on real Stage 5/Stage 6 outputs. Stage 6 reliability 0-100 scale compatibility was verified by reading the spec only (engine clamps defensively).
4. Adversarial/negative: PARTIAL EVIDENCE. Negative EPS, unknown/incomplete evidence families, rationale-free and oversized multiple adjustments are tested. Still needs work: no PIT-violation test, no zero/negative price test, no NaN EPS test.
5. Regression: NO EVIDENCE. No regression corpus or backtest harness; model/contract version fields are emitted but prior-version behavior is untested.
6. Independent audit: IN PROGRESS. This report is the first independent implementation-vs-spec check; no prior independent verification found.

No unexecuted tests were claimed as passed.

## 5. Scope Confirmation

Read-only audit as instructed. Inspected only the listed files. Ran only the specified pytest command. No edits, commits, pushes, branch changes, dependency changes, or GitHub/API calls. No financial data, formulas, or defaults were invented. No tests were weakened or skipped. Stages 1-6 treated as frozen.

## 6. Recommended Next Step (Narrow, Test-First, No Implementation Done Here)

Add failing-first tests for the dependence/flip-risk alert family, scoped strictly to ValuationEngine._alerts and _driver_analysis: (a) a stable-EPS case whose bull fair value comes mostly from target-P/E expansion must raise HIGH_MULTIPLE_DEPENDENCE using the currently dead high_dependence_share (0.60) threshold; (b) a threshold-adjacent upside case (small EPS or margin perturbation flips ATTRACTIVE to FAIR) must raise ASSESSMENT_FLIP_RISK. Do not change frozen stages, the output contract, or any currently passing behavior to do this.

===========================================================

# P2 — Sensitivity and Alert Test Design Report (APPENDED, ENGLISH ONLY)

Date (UTC): 2026-10-11
Scope: Extend Stage 7 validation with focused, failing-first tests for sensitivity and alert behavior. No production, spec, dependency, or config modifications. No existing tests modified. Frozen Stages 1-6 and 8-9 untouched. No remote Git or API operations.

## 1. Files Inspected

- D:/winprojects/analyzer/07_Stage7_Valuation.md (spec sections 41-53)
- D:/winprojects/analyzer/src/valuation/engine.py
- D:/winprojects/analyzer/src/valuation/parameters.py
- D:/winprojects/analyzer/src/valuation/schema.py
- D:/winprojects/analyzer/src/tests/test_stage7_valuation.py
- D:/winprojects/analyzer/temp_report2.md (tail read before appending; existing content preserved)

## 2. Files Changed

- D:/winprojects/analyzer/src/tests/test_stage7_valuation.py — ONLY file changed. Nine new P2 tests appended after the last existing test. Zero existing tests modified. Zero production/spec/config lines touched.

New tests added:
1. test_p2_sensitivity_drivers_present_and_bounded (positive path)
2. test_p2_sensitivity_missing_data_empty_drivers (missing-data path)
3. test_p2_sensitivity_deterministic_repeated_runs (deterministic/repeated-run path)
4. test_p2_alert_severity_levels_valid (severity vocabulary + Alerts-are-not-Buy/Sell check)
5. test_p2_alert_low_reliability_threshold_boundaries (negative/boundary: 39.9 / 40.0 / 40.1 / None)
6. test_p2_alert_high_dispersion_threshold_boundaries (boundary: dispersion above / exactly 0.50 / below / None)
7. test_p2_alert_divergence_ratios_boundaries (boundary: 1.50 benchmark/historical/industry ratios, missing-data guard)
8. test_p2_sector_driver_decomposition_missing (INTENDED FAIL)
9. test_p2_required_flip_dependence_alerts_missing (INTENDED FAIL)

Only behaviors with explicitly defined parameters were asserted: SENSITIVITY_PERTURBATION = 0.10, ALERT_THRESHOLDS (high_scenario_dispersion 0.50, low_forecast_reliability 40.0, benchmark/historical/industry divergence ratios 1.50), RISK_THRESHOLDS high_scenario_dispersion 0.50, VALUATION_THRESHOLDS attractive cutoffs (15.0 / 5.0), severity levels INFO/WATCH/WARNING/CRITICAL (spec section 48), and Alerts-are-not-Buy/Sell-Signal rule (spec section 48).

## 3. Test Command and Exact Results

Command (cwd D:/winprojects/analyzer):
D:/winprojects/analyzer/.venv/Scripts/python.exe -m pytest src/tests/test_stage7_valuation.py -q

Result: collected 20, passed 18, failed 2, skipped 0.

The 11 pre-existing tests all still pass. The 7 new passing P2 tests cover implemented sensitivity/alert paths. The 2 failures are the intended failing-first exposures described below. Pre-existing cosmetic warning unchanged: DeprecationWarning for datetime.datetime.utcnow() at src/valuation/engine.py:176.

## 4. Intended Failing-First Failures (Explained)

FAIL 1 — test_p2_sector_driver_decomposition_missing. Asserts the union of driver rankings across PETROCHEMICAL, BANK, and HOLDING (with nav_per_share=500.0) contains REVENUE, NII, and NAV per spec sections 42-44. Actual ranking is always exactly {EPS, TARGET_PE}. Failure message: assert {'NAV','NII','REVENUE'} <= {'EPS','TARGET_PE'}. This exposes the missing sector driver decomposition; engine hardcodes two drivers and stores nav_per_share in metadata without calculation.

FAIL 2 — test_p2_required_flip_dependence_alerts_missing. Builds four cases: (a) ATTRACTIVE base at EPS 150/150/250 with target PE 7.0, (b) the same case shocked down 10% in EPS (SENSITIVITY_PERTURBATION size) which flips status to FAIR, (c) stable-EPS case with bull multiple expansion to +20%, (d) wide-EPS-range case with reliability 20 and data quality 20. Asserts the combined alert/flag vocabulary contains ASSESSMENT_FLIP_RISK, HIGH_MULTIPLE_DEPENDENCE, HIGH_EPS_DEPENDENCE, MARGIN_ASSUMPTION_RISK, and HIGH_IMPACT_HIGH_UNCERTAINTY. All five are absent. Notably the 10% shock provably flips ATTRACTIVE to FAIR with no flip-risk alert, directly demonstrating the spec section 50 / stress-test 77 gap. No formula, threshold, or mapping was invented to make this pass.

## 5. Specification Blockers (Ambiguities That Prevent Implementation)

No values were invented for any of the following. Each blocks implementation of the corresponding required behavior:

1. Dependence-share formula undefined. ALERT_THRESHOLDS high_dependence_share = 0.60 exists but is unreferenced. The spec never defines how to split fair value into an EPS share versus a multiple share, so HIGH_MULTIPLE_DEPENDENCE (51) and HIGH_EPS_DEPENDENCE (52) cannot be computed without inventing a formula.
2. Flip-risk perturbation undefined. Spec section 50 requires an alert on a relatively small and reasonable assumption change that flips status, but never defines the perturbation size, which assumptions to shock, or the distance-to-threshold test. The P2 test used the 0.10 engine perturbation only as a demonstration, not as a spec value.
3. Sector-driver mapping undefined. Sections 42-44 list causal chains (Revenue chain, Loans/NII chain, NAV chain) but define no industry_code-to-driver mapping, no driver-to-EPS linkage formula, and no per-driver perturbation size. The engine receives industry_code and nav_per_share but has no defined use for them.
4. Driver Impact formula undefined. Section 45 says impact shows the fair-value change from a reasonable driver change but gives no formula, no reasonable-change sizes, and no normalization. Section 47 states Review Priority is approximately Impact x Uncertainty and explicitly defers the exact formula and normalization to a model version parameter that does not exist in parameters.py.
5. Driver Uncertainty formula undefined. Section 46 lists five possible bases (forecast error, historical volatility, scenario range, data quality, model stability) with no selection, weighting, or estimation formula.
6. HIGH_IMPACT_HIGH_UNCERTAINTY trigger undefined. No impact cutoff, no uncertainty cutoff, and no conjunction rule are specified.
7. MARGIN_ASSUMPTION_RISK trigger undefined. Section 53 gives no dependence measure, no margin-perturbation size, and no threshold.
8. LOW_FORECAST_RELIABILITY, HIGH_SCENARIO_DISPERSION, and divergence-ratio cutoffs (40.0, 0.50, 1.50) are implemented as parameters but are not stated anywhere in spec sections 41-53; the new boundary tests pin current engine behavior only and must not be read as spec conformance.
9. Alert-name mismatches unresolved. Spec section 49 requires VALUATION_BENCHMARK_DIVERGENCE; the engine emits VALUATION_ABOVE/BELOW_TARGET_PE. Spec sections 54-55 use HISTORICAL/INDUSTRY_VALUATION_DIVERGENCE; the engine emits FORWARD_PE_ABOVE/BELOW_HISTORICAL/INDUSTRY. No mapping is defined.
10. Remaining section-49 alerts (INSUFFICIENT_PEER_DATA, POOR_DATA_QUALITY, NEGATIVE_EPS, SIGN_CHANGE, POINT_IN_TIME_WARNING) have no trigger definitions in sections 41-53 beyond their names; the engine emits some under different names or not at all, and no test invents their semantics.

## 6. Six-Layer Validation Status

1. Unit/formula: HAS EVIDENCE. Forward P/E, fair value, expected value, and threshold-adjacent status math pass (20 collected, 18 passed including 7 new P2 tests on defined parameters).
2. Contract/boundary: PARTIAL EVIDENCE. New boundary tests pin low-reliability 40.0, dispersion 0.50, and divergence 1.50 cutoffs plus severity vocabulary and missing-data guards. Still missing: industry_peer_count output, sector-driver contract, dependence-share contract.
3. Production-path/integration: NO EVIDENCE. All tests use the synthetic make_forecast fixture; no run on real Stage 5/Stage 6 outputs.
4. Adversarial/negative: PARTIAL EVIDENCE. Negative EPS, None reliability, None dispersion/forward-PE, rationale-free and oversized multiple adjustments covered. Still missing: PIT-violation, zero/negative price, NaN EPS tests.
5. Regression: NO EVIDENCE. No regression corpus or backtest harness; version fields emitted but prior-version behavior untested.
6. Independent audit: IN PROGRESS. Baseline report plus this P2 append constitute the independent check; the two failing-first tests are the documented, reproducible exposures of the missing sensitivity/alert family.

## 7. Scope Confirmation

Added tests only; no existing test weakened; no production, spec, dependency, or config file modified; Stages 1-6 and 8-9 untouched; no git operations; no inventing of formulas, perturbations, thresholds, or sector mappings; report appended in English only with existing content preserved. Work stops after tests and reporting as instructed.
====================================================================
### P3 — Driver Analysis and Alert Engine

Work only in the local project folder `analyzer`. Read the latest Stage 7 reports in `temp_report2.md`, including P2.

## Objective

Implement the highest-priority sensitivity/alert behavior supported by explicit Stage 7 requirements and validated by the P2 tests.

## Scope

* `src/valuation/engine.py`
* `src/valuation/parameters.py` only if an already specified parameter needs to be wired into its intended behavior
* Focused Stage 7 tests

Do not inspect the whole repository.

## Requirements

1. Implement only behaviors with defensible, specification-backed formulas and acceptance criteria.
2. Use existing versioned parameters where applicable. Do not introduce arbitrary constants or infer missing financial facts.
3. Preserve separation between valuation status, risk, confidence, scenario probability, and driver dependency.
4. Preserve deterministic output, invalid-EPS safeguards, existing benchmark hierarchy, and all currently passing behavior.
5. Do not emit `ASSESSMENT_FLIP_RISK`, `HIGH_MULTIPLE_DEPENDENCE`, `HIGH_EPS_DEPENDENCE`, or `MARGIN_ASSUMPTION_RISK` using an invented formula. If the locked specification is insufficient, leave that behavior explicitly unresolved and document the exact missing definition.
6. Do not claim sector-level decomposition is implemented unless the necessary inputs exist in the Stage 7 contract and the calculations are traceable.

## Validation

Run the new focused tests and the full `src/tests/test_stage7_valuation.py` suite. Add boundary and adversarial tests for each implemented behavior. Review regression effects on benchmark selection, probabilities, invalid EPS, and fair value.

Report the six validation layers separately: unit/formula, contract/boundary, production-path/integration, adversarial/negative, regression, and independent audit. Clearly distinguish executed tests from planned tests.

Append results to `temp_report2.md`; never overwrite previous reports. No remote Git operations. Stop after this bounded implementation and report.
========================================================

# P3 — Driver Analysis and Alert Engine Report (APPENDED, ENGLISH ONLY)

Date (UTC): 2026-10-12
Scope: Bounded P3 implementation in `src/valuation/engine.py` plus focused Stage 7 tests. No spec, dependency, or config changes. Frozen Stages 1-6 and 8-9 untouched. No remote Git or API operations. Stages 1-6 treated as frozen; no Stages 1-6 or 8-9 files modified.

## 1. Files Changed

- D:/winprojects/analyzer/src/valuation/engine.py — ONLY production file changed:
  - Added `math` import and two module helpers: `_finite_or_none` (coerces NaN/inf to None) and `_clamp_score` (clamps 0-100 scores with None/non-finite fallback).
  - EPS and benchmark PE series are sanitized (`_finite_or_none`) before forward-P/E, fair-value, median, and dispersion math; zero/negative `current_price` is treated as missing for upside math.
  - `NaN` EPS no longer propagates: a proven pre-change probe showed bear fair value `nan`, expected fair value `nan`, status `FAIR`, dispersion `nan`; post-change all-NaN EPS yields `None` fair values, `None` expected fair value, and `INSUFFICIENT_DATA`.
  - `_driver_analysis` replaced the identical-impact stub with a traceable one-at-a-time recomputation on the locked V1 identity FV = EPS x target P/E: EPS shock holds the multiple fixed, target-P/E shock holds EPS fixed, both using the versioned `SENSITIVITY_PERTURBATION` (0.10). No weighting, normalization, or threshold invented; the 50/50 split is the documented linearity property of the identity, asserted in tests as such.
  - Score paths (confidence, driver uncertainty, data quality) use `_clamp_score` so non-finite scores fall back to documented defaults.
  - Per P3 requirement 5, none of ASSESSMENT_FLIP_RISK, HIGH_MULTIPLE_DEPENDENCE, HIGH_EPS_DEPENDENCE, MARGIN_ASSUMPTION_RISK, or HIGH_IMPACT_HIGH_UNCERTAINTY is emitted: the locked spec defines no formula, perturbation size, dependence-share measure, impact/uncertainty cutoffs, or margin-perturbation rule. A dedicated test pins their absence as explicitly unresolved, not as implemented.
- D:/winprojects/analyzer/src/tests/test_stage7_valuation.py — six P3 tests appended, zero existing tests modified:
  1. test_p3_sensitivity_recomputes_from_valuation_identity
  2. test_p3_nan_eps_is_guarded_as_invalid
  3. test_p3_zero_and_negative_price_guarded
  4. test_p3_nonfinite_benchmark_series_filtered
  5. test_p3_nonfinite_scores_fall_back_to_defaults
  6. test_p3_flip_dependence_alerts_remain_explicitly_unresolved

## 2. Test Command and Exact Results

Command (cwd D:/winprojects/analyzer):
D:/winprojects/analyzer/.venv/Scripts/python.exe -m pytest src/tests/test_stage7_valuation.py -q

Result: collected 26, passed 24, failed 2, skipped 0.

The 2 failures are the pre-existing intended P2 failing-first exposures (test_p2_sector_driver_decomposition_missing, test_p2_required_flip_dependence_alerts_missing), unchanged from the P2 report. All 6 new P3 tests pass. Two P3 tests initially failed on wrong test-side expectations (partial-NaN case where base stays valid, and invalid-price status which is the pre-existing INSUFFICIENT_DATA guard); both were corrected to assert actual guarded behavior, never by changing engine logic to fit the tests. Pre-existing cosmetic warning unchanged: DeprecationWarning for datetime.datetime.utcnow() at src/valuation/engine.py.

## 3. Six-Layer Validation Status (Executed vs Planned)

1. Unit/formula: EXECUTED. Forward P/E, fair value, expected value, one-at-a-time sensitivity identity, and uncertainty-blend defaults all pass (24/26; the 2 failures are the intended P2 exposures).
2. Contract/boundary: EXECUTED for P3 scope. Boundary tests cover NaN/inf benchmark series (median stays 7.0), invalid prices (INSUFFICIENT_DATA with finite fair value), and non-finite score fallbacks. Still planned: industry_peer_count output contract (spec section 69 gap stands).
3. Production-path/integration: NO NEW EVIDENCE. All tests still use the synthetic make_forecast fixture; no run on real Stage 5/Stage 6 outputs.
4. Adversarial/negative: EXECUTED for P3 scope. NaN/inf EPS, None reliability, zero/negative price, polluted benchmark series, and non-finite confidence/quality scores covered. Still missing: PIT-violation test (PIT rests on frozen upstream stages by design).
5. Regression: EXECUTED for P3 scope. Benchmark hierarchy (INDUSTRY_FORWARD_PE / HISTORICAL_MEDIAN_PE / INDUSTRY_TTM_PE), probability evidence, scenario-multiple policy, invalid-EPS NULL rule, and all 18 previously passing tests verified unchanged; only the intended P2 failures remain.
6. Independent audit: IN PROGRESS. This P3 append documents exactly what was implemented with spec backing, what was deliberately left unresolved per requirement 5, and the exact missing definitions (dependence-share formula, flip-risk perturbation definition, driver impact/uncertainty formulas and cutoffs, margin-risk trigger).

## 4. Blockers (No Values Invented)

Unchanged from the P2 report sections on items 1-7: the five alert behaviors stay explicitly unresolved until the locked specification defines their formulas. Nothing in this P3 change invents a formula, constant, mapping, or financial fact.

## 5. Scope Confirmation

Engine.py and focused tests only; parameters.py unchanged (all used values already versioned: SENSITIVITY_PERTURBATION 0.10, VALUATION_THRESHOLDS, RISK_THRESHOLDS, ALERT_THRESHOLDS); no existing test weakened; no spec/dependency/config touched; Stages 1-6 and 8-9 untouched; no git operations; report appended in English only with existing content preserved. Work stops after this bounded implementation and report.
========================================================

# P4 — Output Contract and Peer Evidence Report (APPENDED, ENGLISH ONLY)

Date (UTC): 2026-10-12
Scope: Bounded P4 output-contract change in Stage 7 only. Read the latest Stage 7 reports in temp_report2.md (baseline, P2, P3). Inspected 07_Stage7_Valuation.md sections 1-20 and 63-69, src/valuation/engine.py, schema.py, parameters.py, src/tests/test_stage7_valuation.py. No Stages 1-6 or 8-9 modifications. No remote Git operations. No invented formulas, data, or thresholds.

## 1. Peer Filtering/Count Trace (Task 1)

- Engine sanitizes the forward series before any use (engine.py): `forward_values = [_finite_or_none(v) for v in (industry_forward_pe_values or [])`. NaN, inf, -inf, None, and non-numeric inputs become None.
- `valid_forward_count = self._valid_positive_count(forward_values)` counts only finite values strictly greater than zero. Zero and negative P/E values are excluded from the count, the median (`median_valid` applies the same finite-positive filter), and benchmark selection alike.
- `_select_target_pe` implements the spec sections 11-13 hierarchy: INDUSTRY_FORWARD_PE is selected if and only if the forward median is not None AND `forward_peer_count >= MIN_INDUSTRY_PEERS` (8, from parameters.py). Otherwise HISTORICAL_MEDIAN_PE, then INDUSTRY_TTM_PE, else INSUFFICIENT_DATA. The TTM path uses only the separate `industry_ttm_pe_values` series; forward and TTM populations are never pooled.
- Benchmark provenance chain verified end to end: raw forward series -> sanitized series -> (count, median) -> hierarchy decision recorded in `target_pe_source` -> per-scenario `target_pe` -> fair values. Provenance fields emitted: `industry_forward_pe_median`, `industry_ttm_pe_median`, `historical_median_pe`, `target_pe_source`, plus `metadata["benchmark_peer_minimum"] = 8`.

## 2. Actual Count vs Configured Minimum (Task 2)

- Gap confirmed: before this change the actual valid peer count existed only as the local variable `valid_forward_count` and was never emitted. The only count-related output was `metadata["benchmark_peer_minimum"] = 8` (the configured threshold). A consumer could not distinguish 0, 7, 8, or 50 peers behind an identical industry median.
- Spec section 69 explicitly lists `industry_peer_count` in the minimum Stage 7 output contract, so the Task 3 condition is met: the contract explicitly requires the actual peer count.

## 3. Bounded Change (Task 3)

- D:/winprojects/analyzer/src/valuation/schema.py — added one defaulted field to ValuationResult: `industry_peer_count: int = 0`. Default 0 preserves constructor compatibility for existing direct constructions (Stage 9 test helper) and means "no forward peers supplied or none valid".
- D:/winprojects/analyzer/src/valuation/engine.py — one added kwarg in the ValuationResult construction: `industry_peer_count=valid_forward_count`. No hierarchy change, no population mixing, no invented peer data, no Stages 1-6/8-9 edits.
- D:/winprojects/analyzer/src/tests/test_stage7_valuation.py — six P4 tests appended, zero existing tests modified:
  1. test_p4_peer_count_below_minimum_falls_back (7 peers -> count 7, HISTORICAL_MEDIAN_PE, INSUFFICIENT_PEER_DATA flag)
  2. test_p4_peer_count_at_minimum_selects_industry_forward (8 peers -> count 8, INDUSTRY_FORWARD_PE, median provenance)
  3. test_p4_peer_count_above_minimum_and_median_provenance (10 peers -> count 10, median equals statistics.median of inputs)
  4. test_p4_peer_count_filters_invalid_values (8 valid + NaN/inf/-inf/None/0.0/negative -> count 8, INDUSTRY_FORWARD_PE, median 6.0)
  5. test_p4_peer_count_empty_data_reports_zero_and_falls_back (None / [] / all-invalid -> count 0, median None, HISTORICAL_MEDIAN_PE)
  6. test_p4_benchmark_fallback_ignores_forward_count_for_ttm (7 forward + 3 TTM -> count 7 forward-only, INDUSTRY_TTM_PE, TTM median 6.0; populations stay separate per spec section 12)

## 4. Validation (Tasks 4-5)

- Focused + full Stage 7 file, cwd D:/winprojects/analyzer:
  `D:/winprojects/analyzer/.venv/Scripts/python.exe -m pytest src/tests/test_stage7_valuation.py -q`
  Result: collected 32, passed 30, failed 2, skipped 0. The 2 failures are the pre-existing intended P2 failing-first exposures (test_p2_sector_driver_decomposition_missing, test_p2_required_flip_dependence_alerts_missing), unchanged. All 6 new P4 tests pass; all 24 previously passing tests still pass.
- Serialization/contract compatibility: `dataclasses.asdict(result)` roundtrip verified with the new field present; ValuationResult field count is now 31 including `industry_peer_count`. Stage 9 regression (it constructs ValuationResult directly): `python.exe -m pytest src/tests/test_stage9_decision.py -q` -> 13 passed, confirming backward-compatible constructor behavior.
- Pre-existing cosmetic warning unchanged: DeprecationWarning for datetime.datetime.utcnow() in engine.py.

## 5. Six Validation Layers

1. Unit/formula: EXECUTED. Count/median/hierarchy math passes (30/32; the 2 failures are the intended P2 exposures). Median provenance asserted against statistics.median.
2. Contract/boundary: EXECUTED for P4 scope. Below/at/above minimum, invalid-value filtering, empty-data zero-count, TTM-fallback separation, and source/count consistency covered. The section-69 industry_peer_count gap is now closed.
3. Production-path/integration: NOT VERIFIABLE with available infrastructure. All tests use the synthetic make_forecast fixture; no run on real Stage 5/Stage 6 outputs.
4. Adversarial/negative: EXECUTED for P4 scope. NaN/inf/None/zero/negative peers, empty series, and fallback paths covered. Still missing (out of P4 scope): PIT-violation test.
5. Regression: EXECUTED for P4 scope. All 24 previously passing Stage 7 tests unchanged; Stage 9 suite 13/13 unchanged; benchmark hierarchy, probabilities, invalid-EPS NULL rule, and fair-value behavior untouched.
6. Independent audit: IN PROGRESS. This P4 append documents the trace, the contract basis (section 69), the exact diff, and test evidence; no unexecuted test claimed as passed.

## 6. Blockers

None for P4 scope. Nothing invented: the count is a deterministic count of caller-supplied valid values; the minimum 8 and all thresholds are pre-existing versioned parameters. Deliberately out of scope per P4 task 5 and P3 requirement 5: dependence-share/flip-risk/margin-risk alerts remain unresolved (no spec formulas).

## 7. Scope Confirmation

Stage 7 schema + engine wiring + focused tests only; parameters.py, specs, dependencies, config untouched; no existing test weakened; Stages 1-6 and 8-9 untouched (Stage 9 only read for compatibility and regression-tested); no git operations; English-only append with all prior content preserved. Work stops after this bounded change and report.
========================================================
# P5 — Point-in-Time and Adversarial Input Audit Report (APPENDED, ENGLISH ONLY)

## 0. Prompt Provenance

P5 source: D:/winprojects/analyzer/stage_7_prompts.md, lines 108-137 (section "#### P5 — Point-in-Time and Adversarial Input Audit"). Baseline before work: `src/tests/test_stage7_valuation.py` collected 32, passed 30, failed 2 (the two pre-existing intended P2 failing-first exposures: test_p2_sector_driver_decomposition_missing, test_p2_required_flip_dependence_alerts_missing).

## 1. PIT Input Trace (Task 1)

- Stage 7 V1 benchmark inputs (`historical_pe_values`, `industry_forward_pe_values`, `industry_ttm_pe_values`) arrive as plain undated floats. No observation dates, publication timestamps, report versions, or per-value cutoff metadata cross the Stage 7 boundary, so the engine cannot verify PIT validity of the series themselves. It records medians plus the forward-only peer count (`industry_peer_count`) and a passthrough cutoff; `metadata["pit_inputs_required"] = True` is a metadata claim, not enforcement.
- Forecast EPS inputs inherit Stage 5/6 PIT machinery (`CompanyForecastResult.data_cutoff_datetime`, `ForecastInputRef.available_at`, `normalize_datetime` folding naive datetimes to UTC, `ForecastVersionStore.read_at_cutoff`), but Stage 7 dereferences only `scenario_forecasts.*.eps` plus `data_cutoff_datetime` — the per-input `available_at` refs are not passed and never checked.
- `valuation_date` / `market_price_date` are echoed, never cross-checked against the cutoff: a valuation dated 2026-06-01 with cutoff 2026-01-01 is accepted without rejection or flag (asserted in test_p5_undated_benchmark_series_carry_no_provenance as the reported V1 limitation). No historical records, dates, or provenance were invented; the smallest required contract decision is recorded in section 5 as a blocker.

## 2. Demonstrable Gaps Closed (Tasks 2-3, 5)

All changes are Stage 7-only (engine.py + focused tests). No spec, parameters, dependency, config, Stage 1-6/8-9, or existing-test modification.
- D:/winprojects/analyzer/src/valuation/engine.py:
  1. `expected_upside` computed from sanitized `price` (was raw `current_price`): NaN/inf/None price now yields NULL upside with INSUFFICIENT_DATA status instead of NaN margin leaking into `metadata["expected_upside"]` (Stage 9 reads this field).
  2. `forecast_reliability_score` sanitized via `_finite_or_none`: NaN/inf echo no longer leaks into the output; non-finite reliability falls back to the P3 default path and cannot trigger a false LOW_FORECAST_RELIABILITY alert.
  3. `probability_confidence` non-finite/None now defaults to 50.0 before echo and downstream use (previously echoed NaN verbatim into the contract).
  4. Datetime echoes normalized to UTC-aware via Stage 5/6 `normalize_datetime`: valuation_date, market_price_date, and data_cutoff_datetime (the last inheriting `forecast_result.data_cutoff_datetime` when not supplied) are mutually comparable; mixed naive/aware inputs no longer risk TypeError downstream.
  5. `data_quality_score` None/NaN/out-of-range now flows through `_clamp_score` (None/NaN -> 100.0, clamped to 0-100) instead of raising TypeError on None or echoing NaN.
  6. Non-finite scenario multiple adjustments rejected with "must be finite" ValueError (previously `float(nan)` passed the bound check and silently poisoned target P/E).
  7. NaN probability-evidence scores rejected: `not math.isfinite(score)` added to the [0,1] guard (previously NaN passed every comparison and produced NaN probabilities summing to NaN).
- D:/winprojects/analyzer/src/tests/test_stage7_valuation.py: 10 P5 tests appended, zero existing tests modified. 8 of 10 failed failing-first against the pre-fix engine (reliability echo, pc echo, quality crash, finite-adjustment, evidence-NaN, 2 datetime normalization, expected-upside NaN); missing-EPS and undated-provenance tests passed pre-fix and document enforced vs metadata-only behavior. A finite-or-None sweep helper asserts no NaN leaks across all numeric outputs.

## 3. Validation (Task 4 + Validation section)

- Focused P5 subset, cwd D:/winprojects/analyzer: `D:/winprojects/analyzer/.venv/Scripts/python.exe -m pytest src/tests/test_stage7_valuation.py -q -k "p5"` -> 10 passed, 32 deselected.
- Full Stage 7 file: same command without -k -> collected 42, passed 40, failed 2, skipped 0. The 2 failures are the unchanged pre-existing intended P2 exposures; all 10 new P5 tests pass and all 30 previously passing tests still pass.
- Directly relevant existing contract tests (Stage 9 consumer, read-only, unmodified): `D:/winprojects/analyzer/.venv/Scripts/python.exe -m pytest src/tests/test_stage9_decision.py -q` -> 13 passed. Stage 9 reads only sanitized `metadata["expected_upside"]`/`margin_of_safety_pct`, never the raw price echo, so leaving the echo field untouched is safe.
- Deterministic behavior preserved: datetime normalization and repeated-run equality asserted; valid calculations unchanged (base fair value 1260.0, ATTRACTIVE status, driver 50/50 split intact).

## 4. Six Validation Layers

1. Unit/formula: EXECUTED. 40/42 pass; the 2 failures are the intended P2 exposures, not P5 regressions. Median/hierarchy/probability/EPS-NULL math untouched.
2. Contract/boundary: EXECUTED for P5 scope. NaN/inf/None price, missing/None EPS, NaN reliability/pc/quality, NaN evidence, non-finite adjustments, naive/aware/missing datetimes, and undated-series provenance covered.
3. Production-path/integration: NOT VERIFIABLE with available infrastructure. All tests use the synthetic make_forecast fixture; no run on real Stage 5/6 outputs.
4. Adversarial/negative: EXECUTED for P5 scope. Every numeric entry point now rejects or sanitizes NaN/inf; datetime mixing normalized. Still absent by V1 design: valuation-date-vs-cutoff cross-check (blocker below).
5. Regression: EXECUTED. All 30 previously passing Stage 7 tests unchanged; Stage 9 suite 13/13; hierarchy, probabilities, invalid-EPS NULL rule, fair-value behavior untouched.
6. Independent audit: IN PROGRESS. This P5 append documents the trace, the exact diff, test evidence, verified-vs-claimed PIT separation, and the blocker; no unexecuted test claimed as passed.

## 5. Blockers (Nothing Invented)

- PIT cross-validation absent by V1 design and NOT closed here per P5 task 4 (no upstream redesign): Stage 7 cannot establish whether undated benchmark floats or a valuation_date later than data_cutoff_datetime are PIT-valid. Smallest required contract decision: add per-value observation/publication metadata to the three benchmark series (or an explicit caller attestation that they are PIT-valid at the cutoff), plus a decision on whether valuation_date > data_cutoff_datetime must reject, flag, or remain accepted. Recorded, not implemented.
- Out of P5 scope, unchanged: dependence-share/flip-risk/margin-risk alerts still lack spec formulas (P2/P3 blockers stand); `datetime.utcnow()` deprecation warning persists; sector driver decomposition (REVENUE/NII/NAV) still absent.
- Missing-data handling verified, not defaulted: missing EPS yields NOT_APPLICABLE/NULL (never zero); missing price yields NULL upside with fair value preserved; nothing silently converted to zero.

## 6. Scope Confirmation

Stage 7 engine sanitization/normalization + focused tests only; specification, parameters.py, dependencies, config untouched; no existing test weakened; Stages 1-6 and 8-9 untouched (Stage 9 read-only for consumer check + regression run); no git operations; English-only append with all prior content preserved. Work stops after this audit/fix and report.
========================================================
# P6 — Production-Path, Adversarial and Regression Validation Report (APPENDED, ENGLISH ONLY)

## 0. Prompt Provenance

P6 source: D:/winprojects/analyzer/stage_7_prompts.md, lines 139-160 (section "#### P6 — Production-Path, Adversarial and Regression Validation"). Baseline before work: `src/tests/test_stage7_valuation.py` collected 42, passed 40, failed 2 (the two pre-existing intended P2 failing-first exposures: test_p2_sector_driver_decomposition_missing, test_p2_required_flip_dependence_alerts_missing).

## 1. Scope Inspected (Task 1)

- P2-P5 Stage 7 diffs: git log shows exactly four Stage 7 commits (f18cc1f P2, a9ce955 P3, 085d50a P4, 2502bbf P5) touching only `src/valuation/engine.py`, `src/valuation/schema.py`, and `src/tests/test_stage7_valuation.py`. Working tree has no other Stage 7 modification (git status shows only `M stage_7_prompts.md`).
- Actual Stage 5/6 output interfaces: `CompanyForecastResult` / `ScenarioForecastResult` / `SingleForecastChain` in D:/winprojects/analyzer/src/forecast/schema.py, produced by `ForecastEngine.generate_forecast` in D:/winprojects/analyzer/src/forecast/engine.py (line 1044). No other files inspected.

## 2. Production-Path Integration (Task 2) — GENUINE INTEGRATION ACHIEVED

No blocker. A real pipeline-produced forecast feeds Stage 7 in the new test_p6_production_path_real_stage5_forecast: `ForecastEngine.generate_forecast(1, 101, "PETROCHEMICAL", context, data_cutoff_datetime=2026-01-01 UTC)` with caller-declared financial context plus historical dispersion series (6 revenue observations, 6 operating-margin pairs, 6 net-margin pairs) yields three valid positive EPS values (bear 1.095057, base 1.1, bull 1.104943, method MARGIN, quality MEDIUM). Stage 7 consumes it through its production constructor with no fixture, no fabricated record, no bypassed validation. Observed: target HISTORICAL_MEDIAN_PE, base fair value 7.7, status VERY_EXPENSIVE (small EPS against price 1000.0), probabilities 0.2/0.6/0.2 summing to 1.0, driver ranking EPS/TARGET_PE 50/50, and cutoff inheritance (`result.data_cutoff_datetime == forecast.data_cutoff_datetime`). A minimal-context probe (no historical series) yields only base EPS with bear/bull None, confirming the test uses the strongest valid boundary, not a trivial path.

## 3. Adversarial Cases (Task 3) — 6 New Tests, All Passing

All in D:/winprojects/analyzer/src/tests/test_stage7_valuation.py, zero existing tests modified:
1. test_p6_production_path_real_stage5_forecast (above).
2. test_p6_cutoff_pit_limitation_pinned — valuation_date 2026-06-01 later than cutoff 2026-01-01 is accepted without rejection or flag (status ATTRACTIVE); pins the P5-documented V1 limitation as the strongest valid boundary since cross-validation needs the undecided contract change.
3. test_p6_missing_benchmarks_yield_guarded_nulls — no benchmark series at all: INSUFFICIENT_DATA source/status, peer count 0, NULL fair values/upside, INDUSTRY_BENCHMARK_INSUFFICIENT flag plus CRITICAL:INSUFFICIENT_BENCHMARK_DATA alert, finite-or-None sweep clean.
4. test_p6_scenario_ordering_flag_and_probability_normalization — inverted EPS (300/180/100) raises SCENARIO_ORDER_WARNING with fair values 2100.0/1260.0/700.0 and probabilities still summing to 1.0; 4-family evidence blend also sums to 1.0 with finite non-negative probabilities.
5. test_p6_invalid_eps_variants_never_fabricate_values — zero/negative mix, all-NaN, and all-None EPS each yield NULL expected fair value, NOT_APPLICABLE/INSUFFICIENT_DATA status, empty driver ranking/impact; ZERO_EPS and NEGATIVE_EPS flag names asserted; nothing coerced to zero.
6. test_p6_repeat_runs_identical_on_full_contract — full-contract repeated runs (benchmarks, evidence-free priors, rationale-backed multiple adjustments) produce identical dataclass dicts excluding the wall-clock calculation_timestamp.
7. test_p6_regression_prior_behavior_preserved — golden values intact (bear/base/bull fair values 1050.0/1260.0/700.0-expected 1260.0, margin 26.0, ATTRACTIVE, HISTORICAL_MEDIAN_PE, contract/model versions, peer count 0, 50/50 driver split) plus TTM-fallback hierarchy regression (7 forward peers + TTM series stays INDUSTRY_TTM_PE, count 7).

## 4. Test Commands and Exact Counts (Task 4)

- Stage 7 file, cwd D:/winprojects/analyzer: `D:/winprojects/analyzer/.venv/Scripts/python.exe -m pytest src/tests/test_stage7_valuation.py -q` -> collected 49, passed 47, failed 2, skipped 0. The 2 failures are the unchanged pre-existing intended P2 failing-first exposures (sector decomposition REVENUE/NII/NAV; flip/dependence alerts); all 7 new P6 tests pass; all 40 previously passing tests still pass.
- Stage 7 + Stage 9 consumer: `... -m pytest src/tests/test_stage7_valuation.py src/tests/test_stage9_decision.py -q -p no:warnings` -> 2 failed, 60 passed. Stage 9 is 13/13 unchanged.
- Full suite: `D:/winprojects/analyzer/.venv/Scripts/python.exe -m pytest src/tests/ -q -p no:warnings -rs --ignore=src/tests/test_codal_pdf_extraction.py` (PDF extraction file excluded: it requires real Codal sample PDFs unavailable in this environment) -> 3 failed, 893 passed, 1 skipped, 4 errors in ~209s. Per-file verification: Stage 2 KPIs + Stage 8 market 32 passed; Stage 6 evaluation + production pipeline 47 passed; Stage 3/4/5 451 passed; Stage 8 market 15 passed. The observed failures/errors outside Stage 7 were not individually attributed file-by-file (an ingestion-suite probe exceeded the foreground window); no Stage 7 change is implicated — every non-Stage-7 suite sampled passes and Stage 7/9 results are fully accounted for.

## 5. Six Validation Layers (Task 5)

1. Unit/formula: FRESHLY EXECUTED. 47/49 Stage 7 pass (2 intended P2 exposures); production-path fair-value math, golden regression values, and driver identity verified this run.
2. Contract/boundary: FRESHLY EXECUTED. Missing benchmarks (NULL guards, count 0, dual flag/alert), peer-count boundaries (carried forward from P4: 6/6 pass this run), invalid-price/EPS variants, non-finite sweeps, datetime normalization (carried forward from P3/P5: all pass this run).
3. Production-path/integration: FRESHLY EXECUTED — first genuine evidence in the Stage 7 series. Real Stage 5 ForecastEngine output (three valid scenario EPS) consumed by the Stage 7 production constructor; no synthetic fixture. Prior reports' NO EVIDENCE status is superseded for the forecast leg; benchmark-series PIT inputs remain undated floats by V1 design (limitation pinned, not closed).
4. Adversarial/negative: FRESHLY EXECUTED. Invalid EPS (zero/negative/NaN/None), missing benchmarks, peer-count pollution, non-finite inputs, scenario-order inversion, cutoff/PIT limitation, probability normalization, and full-contract repeat-run determinism covered. Unresolved by design: flip/dependence/margin alerts (no spec formulas) and sector decomposition (no mapping).
5. Regression: FRESHLY EXECUTED for sampled scope. All 40 previously passing Stage 7 tests unchanged; Stage 9 13/13; Stages 2/3/4/5/6/8 sampled suites pass (545+ tests); golden values and benchmark hierarchy pinned. Any regression from Stage 7 changes: none found; the 2 Stage 7 failures pre-date P6 and are documented intended exposures, not regressions.
6. Independent audit: IN PROGRESS. This P6 append plus the five prior reports constitute the independent check. Freshly executed this run: tasks 2-5 above. Carried forward: P4 peer-count boundary evidence, P3/P5 sanitization evidence (re-executed as part of the 47 passes, not merely cited).

## 6. Boundaries and Blockers (Task 6 + Boundaries)

- No unrelated test modified to obtain a pass; no Stage 7 regression introduced (no production code changed in P6 at all — tests only).
- Frozen stages untouched: no Stages 1-6 or 8-9 file modified; parameters.py, specs, dependencies, migrations untouched. Stage 9 touched only as a read-only regression run.
- Nothing invented: no financial data, formulas, thresholds, or defaults added; probe values used only to select assertions, never baked in as spec.
- Standing blockers (unchanged, recorded not closed): dependence-share/flip-risk/margin-risk alert formulas undefined; sector-driver mapping undefined; benchmark-series PIT provenance absent (smallest required contract decision in P5 section 5 stands); `datetime.utcnow()` deprecation warning persists; full-suite third failure + 4 errors outside Stage 7 not individually attributed (see section 4).

## 7. Scope Confirmation

Validation only: 7 tests appended to D:/winprojects/analyzer/src/tests/test_stage7_valuation.py (only file changed); no production, spec, dependency, or config modification; no existing test weakened; no git operations; report appended in English only with all prior content preserved. Stage 7 is NOT declared frozen.
========================================================
# P7 — Independent Final Audit and Freeze Gate Report (APPENDED, ENGLISH ONLY)

## 0. Prompt Provenance

P7 source: D:/winprojects/analyzer/stage_7_prompts.md, lines 162-193 (section "#### P7 — Independent Final Audit and Freeze Gate"). Read-only execution; no source, test, spec, dependency, or config file was modified. Working tree was clean before work and remains clean apart from this appended report. No commits, pushes, pulls, branch changes, GitHub/API, or remote operations. Frozen-stage boundary verified via git history: P2-P6 commits touch only src/valuation/engine.py, src/valuation/schema.py, src/tests/test_stage7_valuation.py, stage_7_prompts.md, and temp_report2.md.

## 1. Independent Formula Trace (Requirement 1)

Traced engine.py against 07_Stage7_Valuation.md without relying on prior PASS labels. Conformant: Forward P/E = price / EPS per scenario (sections 4-5); invalid EPS yields NULL with NEGATIVE_EPS/ZERO_EPS/SIGN_CHANGE/NOT_APPLICABLE flags and no fabricated fair value (section 6); benchmark hierarchy INDUSTRY_FORWARD_PE -> HISTORICAL_MEDIAN_PE -> INDUSTRY_TTM_PE with 8-peer gate, median priority, no Forward/TTM pooling (sections 10-13); neutral 1.0 scenario multiples with bounded (+/-0.20) rationale-backed adjustments instead of a fixed 0.8/1.2 rule (section 17); direct probability adjustments rejected, family-level evidence blended at 0.25 onto the 20/60/20 prior (sections 22-24); reliability never multiplies P/E or fair value (section 16); status/risk/confidence computed independently (sections 34-39). Confirmed dead parameter: ALERT_THRESHOLDS high_dependence_share (0.60) is defined in parameters.py line 72 and referenced nowhere in src/valuation. Confirmed metadata-only inputs: industry_code and nav_per_share are echoed to metadata and never enter any calculation; models.py calculate_nav_fair_value is legacy and unwired.

## 2. Invariants and Boundaries (Requirement 2)

Verified by passing tests this run: probability sums to 1.0 incl. 4-family blends and inverted-EPS ordering (flag SCENARIO_ORDER_WARNING raised, never reordered); golden values bear/base/bull 1050.0/1260.0/700.0-expected 1260.0 margin 26.0 ATTRACTIVE match the baseline assertions; peer count emitted and consistent with selected source (7->fallback, 8->INDUSTRY_FORWARD_PE); NaN/inf/None/zero/negative inputs sanitized at every numeric entry point with finite-or-None sweeps; datetime echoes normalized to UTC-aware with cutoff inheritance; full-contract repeat runs identical excluding wall-clock calculation_timestamp; model/contract versions STAGE7_V1 / VALUATION_CONTRACT_V1 pinned. PIT limitation re-confirmed: benchmark series arrive as undated floats and valuation_date later than data_cutoff_datetime is accepted without flag (pinned test asserts ATTRACTIVE with no PIT flag) — metadata claim only, not enforcement.

## 3. Test Quality Review (Requirement 3)

Reviewed all 49 tests by section. No false positives: the 2 failures fail for the right reason (asserted alert names absent from combined alert/flag vocabulary; asserted sector drivers not subset of {EPS, TARGET_PE}). No tautological assertions found: boundary tests assert both sides (reliability fires at 39.9, silent at 40.0 and None; dispersion fires above 0.50, silent exactly at 0.50 verified to 1e-9); median provenance checked against statistics.median; determinism via repeated runs and full-dataclass comparison. No weakening: diff of the test file against the baseline commit is purely additive (848 insertions, zero deleted assertions). Honest caveat preserved from P2: boundary tests pin engine-chosen cutoffs (40.0/0.50/1.50) not stated in spec sections 41-53, so they pin behavior, not spec conformance.

## 4. Test Commands, Counts, Environment (Requirement 4)

Cwd D:/winprojects/analyzer, interpreter D:/winprojects/analyzer/.venv/Scripts/python.exe (Python 3.12.9, pytest 9.1.1):
- Stage 7 file: -m pytest src/tests/test_stage7_valuation.py -q -p no:warnings -> collected 49, passed 47, failed 2, skipped 0. Both failures are the pre-existing intended P2 failing-first exposures, unchanged since P2.
- Stage 7 + Stage 9 consumer: -m pytest src/tests/test_stage7_valuation.py src/tests/test_stage9_decision.py -q -p no:warnings -> 2 failed, 60 passed (Stage 9 13/13).
- Full suite: -m pytest src/tests/ -q -p no:warnings -rs --ignore=src/tests/test_codal_pdf_extraction.py -> 2 failed, 897 passed, 1 skipped, 0 errors in 143.51s. Skip reason: test_codal_extraction.py:307, real Codal sample PDF not available in CI. PDF-extraction file excluded: requires real Codal sample PDFs unavailable in this environment. Note: the unattributed third failure + 4 errors reported in the P6 full-suite run did not recur; with identical code the only failures are the two known Stage 7 exposures. Pre-existing cosmetic warning (datetime.utcnow DeprecationWarning, engine.py:212) persists.

## 5. Classified Findings (Requirement 5)

- BLOCKER-1: Required flip/dependence alert family absent. ASSESSMENT_FLIP_RISK, HIGH_MULTIPLE_DEPENDENCE, HIGH_EPS_DEPENDENCE, MARGIN_ASSUMPTION_RISK, HIGH_IMPACT_HIGH_UNCERTAINTY cannot be produced by any input (proven by failing test_p2_required_flip_dependence_alerts_missing; 10% EPS shock demonstrably flips ATTRACTIVE to FAIR with no alert). Spec sections 49-53 and stress tests 77-79 require them but define no dependence-share formula, flip-risk perturbation, impact/uncertainty cutoffs, or margin trigger (P2 blockers 1-7 stand). Proven absence; root cause is specification ambiguity, but freeze conformance fails regardless.
- BLOCKER-2: Sector driver decomposition absent. Ranking is always {EPS, TARGET_PE}; REVENUE/NII/NAV chains (sections 42-44) unimplemented (proven by failing test_p2_sector_driver_decomposition_missing). No industry-to-driver mapping or linkage formula exists in the spec.
- MATERIAL-1: Alert vocabulary mismatch. Engine emits VALUATION_ABOVE/BELOW_TARGET_PE vs required VALUATION_BENCHMARK_DIVERGENCE (section 49), and FORWARD_PE_ABOVE/BELOW_HISTORICAL/INDUSTRY vs required HISTORICAL/INDUSTRY_VALUATION_DIVERGENCE (sections 54-55). No mapping defined.
- MATERIAL-2: PIT cross-validation absent. Undated benchmark floats plus unchecked valuation_date-vs-cutoff need the contract decision recorded in P5 section 5 (per-value provenance or caller attestation; reject/flag/accept rule). Not closable without upstream contract change.
- MINOR-1: Confidence/risk/dispersion blend constants (0.40/0.20 weights, dispersion slope and cap) are hardcoded in engine.py rather than versioned parameters (sections 64-65 cover thresholds, which are versioned; the blend weights are not). Cosmetic utcnow() deprecation warning persists.
- DOCUMENTED LIMITATION: Production-path evidence covers the forecast leg (real Stage 5 ForecastEngine output consumed, cutoff inherited); the benchmark PIT leg remains fixture-based by V1 design.

## 6. Verdict (Requirement 6)

NOT READY FOR FREEZE

Two red tests assert absent required behavior, and the missing behaviors cannot be implemented without spec formulas that do not exist. Freezing now would certify conformance the evidence contradicts. Path to readiness: either the locked specification defines the dependence-share, flip-risk, impact/uncertainty, margin-risk, and sector-mapping formulas (then implement + green the two tests), or an explicit scope decision defers those requirements out of V1 with the stress-test claims corrected. This verdict is an audit finding, not a freeze declaration.

## 7. Scope Confirmation

Read-only audit: inspected the spec, Stage 7 sources, all 49 Stage 7 tests, and the P2-P6 reports; ran only the stated pytest commands; verified frozen-stage boundaries via git history; invented no data, formulas, thresholds, or defaults. This English-only append preserves all earlier reports. Work stops after validation and reporting; Stage 7 is NOT declared frozen.
========================================================
# P8 — Stage 7 Specification Decision Package (APPENDED, ENGLISH ONLY)

Date (UTC): 2026-10-12. P8 source: D:/winprojects/analyzer/stage_7_prompts.md, lines 195-242
(section "# P8 — Stage 7 Specification Decision Package"). No source, test, specification,
parameter, dependency, or configuration file was modified. No commits, pushes, pulls, branch
changes, GitHub/API, or remote operations. Frozen Stages 1-6 and 8-9 untouched. No financial
formula, threshold, perturbation size, sector mapping, or PIT policy was selected; candidate
designs below are explicitly labeled PROPOSAL, not specification. P8 verification run (cwd
D:/winprojects/analyzer, D:/winprojects/analyzer/.venv/Scripts/python.exe -m pytest
src/tests/test_stage7_valuation.py -q -p no:warnings): collected 49, passed 47, failed 2,
skipped 0. The 2 failures are the unchanged P2 failing-first exposures
(test_p2_sector_driver_decomposition_missing, test_p2_required_flip_dependence_alerts_missing),
identical to the P7 state. Full suite was not re-executed in P8; full-suite evidence is carried
forward from P7 (2 failed, 897 passed, 1 skipped, PDF-extraction file excluded).

## 1. Inputs reviewed

- Failing tests: D:/winprojects/analyzer/src/tests/test_stage7_valuation.py, lines 406-465
  (sector decomposition assertion lines 421-422; flip/dependence assertion lines 457-465).
- P7 findings: this file, lines 377-420. BLOCKER-1 (flip/dependence alert family absent,
  10% EPS shock provably flips ATTRACTIVE to FAIR with no alert) and BLOCKER-2 (ranking always
  {EPS, TARGET_PE}; sections 42-44 chains unimplemented) are confirmed open by the P8 rerun.
- Engine evidence: D:/winprojects/analyzer/src/valuation/engine.py (_driver_analysis lines
  468-498 hardcodes two drivers; _alerts lines 500-535 emits no required family names);
  parameters.py line 72 high_dependence_share 0.60 is defined and referenced nowhere in
  src/valuation (independently verified by search in P8).
- Required names are absent from all engine source: a P8 search for ASSESSMENT_FLIP_RISK,
  HIGH_MULTIPLE_DEPENDENCE, HIGH_EPS_DEPENDENCE, MARGIN_ASSUMPTION_RISK,
  HIGH_IMPACT_HIGH_UNCERTAINTY, VALUATION_BENCHMARK_DIVERGENCE, POINT_IN_TIME_WARNING, and
  POOR_DATA_QUALITY matches only test files, never src/valuation.

## 2. Decision table

Conventions: SPEC = direct specification evidence (section quoted). MISSING = the smallest
specification amendment needed to make the requirement testable. PROPOSAL = my candidate
design, not a requirement; listed only so the user can see viable options and their financial
consequences. No option is selected.

### D1 — ASSESSMENT_FLIP_RISK

- SPEC: section 50 requires the alert when a "relatively small and reasonable" assumption
  change flips ATTRACTIVE to FAIR or EXPENSIVE; stress test 77 requires it for a small
  margin/EPS change flipping ATTRACTIVE to FAIR.
- MISSING: (a) perturbation size ("relatively small" has no number); (b) which assumptions
  to shock (EPS, margin, multiple, all drivers?); (c) shock method (one-at-a-time vs joint);
  (d) trigger rule (any single shock flipping status, or majority, or expected-upside-only);
  (e) severity (INFO/WATCH/WARNING/CRITICAL unspecified).
- PROPOSAL A (distance-to-threshold, no recomputation): alert when expected upside is within
  X percentage points of the nearest status boundary. Consequence: cheap and deterministic,
  but X is a new threshold and multi-assumption fragility is missed; near-boundary cases
  could over-alert.
- PROPOSAL B (one-at-a-time recomputation): shock base EPS and target P/E by
  SENSITIVITY_PERTURBATION one-at-a-time and alert if any single shock changes
  valuation_status. Consequence: directly tests fragility at ~2 extra valuations; still needs
  the shock set/sizes and the flip rule fixed in the spec.
- PROPOSAL C (joint worst-case shock): shock all assumptions adversely at once.
  Consequence: most conservative; likely over-alerts and needs correlation assumptions the
  spec does not contain.
- REQUIRED USER DECISION: fix the (shock set, shock sizes, method, flip rule, severity)
  tuple, or explicitly defer the alert out of V1.

### D2 — HIGH_MULTIPLE_DEPENDENCE

- SPEC: section 51 requires the alert when fair value depends excessively on target P/E
  rather than EPS growth (example: near-stable EPS with the bull case built on very high P/E
  expansion); stress test 78.
- MISSING: (a) the dependence-share formula splitting fair value into an EPS share vs a
  multiple share; (b) the role of the dead high_dependence_share = 0.60 (trigger value?
  share of what?); (c) scope (bull case only, all scenarios, or base?); (d) severity.
- PROPOSAL A (counterfactual decomposition): recompute bull fair value at the base multiple;
  multiple_share = (bull_FV - bull_EPS x base_multiple) / bull_FV; alert above a threshold.
  Consequence: economically intuitive; needs the threshold decision; undefined when EPS is
  invalid (must then be NOT_APPLICABLE, not zero).
- PROPOSAL B (elasticity ratio): compare percent FV change from a multiple shock vs an EPS
  shock; alert if multiple elasticity dominates by factor K. Consequence: reuses existing
  perturbation machinery; needs K and the shock sizes.
- REQUIRED USER DECISION: define the share formula, confirm or remove the 0.60 threshold,
  fix scope and severity, or defer out of V1.

### D3 — HIGH_EPS_DEPENDENCE

- SPEC: section 52 requires the alert when valuation is mainly sensitive to forecast EPS,
  with severity allowed to rise when forecast reliability is low; stress test 79.
- MISSING: (a) the EPS-share formula (mirror of D2); (b) the low-reliability severity
  escalation rule (how many severity steps, at what reliability cutoff — the 40.0 engine
  cutoff is not stated in the spec); (c) how D2 and D3 interact when both shares are high
  (both alerts, or the larger one?).
- PROPOSAL A: EPS_share = 1 - multiple_share from D2's formula; escalate one severity level
  when reliability is below the low-reliability cutoff. Consequence: consistent with D2 but
  inherits all of D2's decisions plus the escalation matrix.
- PROPOSAL B: standalone elasticity trigger independent of D2. Consequence: D2 and D3 could
  fire together; needs a documented precedence rule.
- REQUIRED USER DECISION: define the share formula, the escalation rule, and D2/D3
  precedence, or defer out of V1.

### D4 — MARGIN_ASSUMPTION_RISK

- SPEC: section 53 requires the alert when fair value depends strongly on operating/net
  margin forecasts.
- MISSING: everything functional — dependence measure, margin-perturbation size, threshold —
  plus a structural gap: Stage 7 inputs contain EPS but no margin series, so no formula can
  run without an input-contract change.
- PROPOSAL A (contract expansion): Stage 5 supplies margin assumptions; shock them
  one-at-a-time. Consequence: correct economics but the largest scope of this table
  (upstream contract change, frozen-stage boundary engagement).
- PROPOSAL B (EPS-shock proxy labeled margin-blind): attribute part of EPS sensitivity to
  margins by assumption. Consequence: no contract change but economically weak and risks
  false precision; must be labeled as a proxy, not a margin test.
- REQUIRED USER DECISION: expand the input contract, accept a labeled proxy, or defer the
  alert (with section 53) out of V1. Strongest deferral candidate in this package.

### D5 — HIGH_IMPACT_HIGH_UNCERTAINTY

- SPEC: section 49 requires the alert name; section 45 defines Driver Impact only as the
  fair-value change from a "reasonable" driver change (no formula, sizes, or normalization);
  section 46 lists five possible uncertainty bases with no selection or weighting; section 47
  states Review Priority is approximately Impact x Uncertainty and explicitly defers the
  exact formula and normalization to a model-version parameter that does not exist.
- MISSING: (a) impact formula with per-driver shock sizes; (b) uncertainty estimation
  formula (which bases, what weights); (c) the conjunction cutoffs (what counts as "high"
  impact and "high" uncertainty).
- PROPOSAL A (minimal): reuse the existing one-at-a-time 10% FV-identity shocks for impact
  and the current reliability/probability/quality blend for uncertainty, plus fixed cutoffs.
  Consequence: implementable immediately, but cutoffs are still new decisions and only
  {EPS, TARGET_PE} are covered until D6 is resolved.
- PROPOSAL B (full): per-driver framework after the sector mapping (D6) is defined.
  Consequence: complete but blocked behind D6.
- REQUIRED USER DECISION: fix formulas and cutoffs, or defer the alert (with sections
  45-47) out of V1.

### D6 — Sector-driver chains (non-financial, banks, holdings)

- SPEC: sections 42-44 give causal chains (Revenue chain; Loans/Deposits to NII/NIM chain;
  NAV to NAV-growth chain) and state P/NAV analysis belongs to Stage 7; the P2 test
  requires REVENUE, NII, and NAV to appear in driver rankings.
- MISSING: (a) industry_code-to-driver-set mapping (which codes count as bank/holding?);
  (b) driver-to-EPS linkage formulas; (c) per-driver perturbation sizes; (d) how NAV enters
  fair value (no P/NAV formula exists); engine currently ignores industry_code and echoes
  nav_per_share to metadata only.
- PROPOSAL A (identity decomposition): each chain link a multiplicative/additive identity
  with its own shock. Consequence: needs per-link data in the inputs — large contract
  expansion comparable to D4.
- PROPOSAL B (sector-labeled attribution): keep the EPS-identity shocks, attribute them
  through sector templates for ranking labels only. Consequence: small change but the
  economics are thin; ranking labels would imply analysis that was not performed.
- REQUIRED USER DECISION: define the mapping, linkage formulas, and NAV treatment, or
  defer sections 42-44 (with the P/NAV claim) to V2 with ranking staying {EPS, TARGET_PE}.

### D7 — Benchmark PIT provenance and valuation-date/cutoff relationship

- SPEC: sections 56-57 and 8 require per-observation price date, forecast cutoff,
  publication date, version, and availability; future-published reports are banned from
  backtests; stress test 85.
- CURRENT STATE (proven): benchmark series arrive as undated float lists; valuation_date
  later than data_cutoff_datetime is accepted silently (pinned by a passing test asserting
  ATTRACTIVE with no PIT flag); metadata pit_inputs_required=True is a claim flag, not
  enforcement (P5/P7 evidence, uncontradicted).
- MISSING: (a) per-value provenance fields; (b) the valuation_date-vs-cutoff rule
  (reject, flag, or accept?); (c) the mechanism choice recorded in P5: per-value
  provenance vs caller attestation.
- PROPOSAL A (per-value provenance structs with validation): reject or flag
  future-dated observations. Consequence: strongest guarantee; contract change for every
  benchmark caller including upstream stages.
- PROPOSAL B (caller attestation plus ordering check): flag when valuation_date exceeds
  the cutoff by more than a tolerance. Consequence: small change; trust-based and needs
  the tolerance decision.
- PROPOSAL C (documented limitation): keep metadata-only behavior in V1.
  Consequence: no work, but section 56 and stress test 85 PASS claims must be corrected.
- REQUIRED USER DECISION: choose A, B, or C. Not implementable without this choice.

### D8 — Required alert names vs currently emitted names

- SPEC: section 49 requires VALUATION_BENCHMARK_DIVERGENCE, INSUFFICIENT_PEER_DATA,
  POOR_DATA_QUALITY, NEGATIVE_EPS, SIGN_CHANGE, POINT_IN_TIME_WARNING (among others);
  sections 54-55 use HISTORICAL_VALUATION_DIVERGENCE and INDUSTRY_VALUATION_DIVERGENCE.
- EMITTED: WATCH:VALUATION_ABOVE/BELOW_TARGET_PE, WATCH:FORWARD_PE_ABOVE/BELOW_HISTORICAL,
  WATCH:FORWARD_PE_ABOVE/BELOW_INDUSTRY, CRITICAL:INSUFFICIENT_BENCHMARK_DATA,
  WARNING:LOW_FORECAST_RELIABILITY / HIGH_SCENARIO_DISPERSION, INFO:TOP_DRIVER — plus
  NEGATIVE_EPS, SIGN_CHANGE, and INSUFFICIENT_PEER_DATA as risk flags, not alerts.
- MISSING: (a) the name mapping (rename vs alias vs spec amendment adopting engine names);
  (b) trigger semantics for POOR_DATA_QUALITY and POINT_IN_TIME_WARNING, which have no
  definition anywhere; (c) whether flag-level emission satisfies the section 49 "alert
  capability" requirement for NEGATIVE_EPS/SIGN_CHANGE/INSUFFICIENT_PEER_DATA.
- PROPOSAL A (rename to spec names): cleanest conformance. Consequence: breaking change
  for any consumer parsing current names.
- PROPOSAL B (alias both, spec names canonical): backward compatible. Consequence: dual
  vocabulary must be versioned and eventually retired.
- PROPOSAL C (amend the spec to adopt engine names): no code change. Consequence:
  requires editing the locked specification with governance approval.
- REQUIRED USER DECISION: mapping choice (should be decided now — it is a naming decision,
  not a formula); POOR_DATA_QUALITY and POINT_IN_TIME_WARNING triggers may be deferred
  with the section 49 capability claim corrected.

### D9 — Hardcoded model weights and thresholds that should be versioned

- SPEC: sections 64-65 require a new model version for changes to the listed methods and
  require all tunable thresholds outside hard-code with
  (model_version, parameter_name, parameter_value, effective_from, description) records.
- FOUND HARDCODED (engine.py, independently re-verified in P8): confidence blend 0.40 /
  0.20 / 0.20 with benchmark 100/25 and dispersion penalty slope 50 capped at 40
  (_valuation_confidence); driver-uncertainty blend 0.5 / 0.3 / 0.2 (_driver_analysis);
  dispersion formula (max-min)/base (_scenario_dispersion — section 40 requires the formula
  to be versioned); parameters.py holds values but no effective_from/description records.
- MISSING: (a) the parameter-version record store (in-code registry, DB table, or file?);
  (b) confirmation that blend weights and the dispersion formula are in scope as tunable.
- PROPOSAL A (code registry): move all blends/slopes/caps into parameters.py with version
  records. Consequence: code-only, no contract or migration change; needs the record-store
  format decision.
- PROPOSAL B (DB-backed parameter table): full audit trail. Consequence: migration work
  that reaches beyond Stage 7-only scope.
- PROPOSAL C (fix as V1 methodology, version via MODEL_VERSION bump only).
  Consequence: weakest versioning; arguably violates section 65.
- REQUIRED USER DECISION: record-store mechanism and scope confirmation. Proposal A is
  small and need not be deferred; B may be deferred.

## 3. Deferral analysis (requirements explicitly deferrable from V1)

Deferrable with claim corrections: D1 (correct section 50 and stress test 77 PASS), D2
(section 51, stress test 78), D3 (section 52, stress test 79), D4 (section 53), D5
(sections 45-47 and the section 49 HIGH_IMPACT_HIGH_UNCERTAINTY entry), D6 (sections 42-44
and the P/NAV claim), D7-option-C (section 56 and stress test 85 PASS), D8-partial
(POOR_DATA_QUALITY and POINT_IN_TIME_WARNING triggers with the section 49 capability list).
Each deferral must move the requirement to an explicit V1-excluded list and downgrade the
corresponding PASS claim to DEFERRED/OUT-OF-SCOPE; otherwise the locked specification
over-claims. Decide-now items: D8 name mapping and D9 record mechanism are naming and
mechanics decisions that cost little and should not ride on a deferral. No deferral may
weaken the two failing P2 tests artificially — deferred requirements must be removed from
the tests' expectations by spec amendment first, never by editing tests to pass.

## 4. Six validation layers (executed vs not executed in P8)

1. Unit/formula: EXECUTED (P8 rerun of the Stage 7 file: 49 collected, 47 passed, 2 failed —
   the 2 failures assert absent required behavior and fail for the right reason).
2. Contract/boundary: EXECUTED (same rerun; peer-count, determinism, and boundary pins
   unchanged from P7).
3. Production-path/integration: NOT EXECUTED in P8 (carried from P7: forecast leg uses real
   Stage 5 output; benchmark leg remains fixture-based by V1 design).
4. Adversarial/negative: EXECUTED (same rerun; finite-input guards and rationale/bound
   rejections unchanged from P7).
5. Regression: NOT EXECUTED in P8 (full suite not rerun; P7 evidence carried: 897 passed,
   1 skipped with Codal-sample reason, 2 known failures, PDF-extraction file excluded).
6. Independent audit: EXECUTED (this read-only decision package; formulas, names, and
   dead-parameter claims independently re-verified against source in P8). Nothing is claimed
   implemented or validated beyond the rerun and the read-only trace.

## 5. Scope confirmation

Read-only decision package plus a confirming test rerun: inspected the spec, Stage 7
sources, the two failing tests, and the P2/P7 reports; ran only the Stage 7 pytest command
above; modified no source, test, specification, parameter, dependency, or configuration;
invented no financial data, formulas, thresholds, defaults, or PIT policy; left the two
failing tests failing as required. This English-only append preserves all earlier reports.
Work stops after appending the report.
========================================================
# P9 — Alert Contract and Naming Consistency Audit (APPENDED, ENGLISH ONLY)

Date (UTC): 2026-10-12. P9 source: D:/winprojects/analyzer/stage_7_prompts.md,
lines 243-284. No source, test, specification, parameter, dependency, or configuration
file was modified. No commits, pushes, pulls, branch changes, GitHub/API, or remote
operations. Frozen Stages 1-6 and 8-9 untouched. No financial formula, threshold,
perturbation size, severity, or trigger semantic was invented; ambiguities are recorded
as decisions/blockers. P9 verification runs (cwd D:/winprojects/analyzer,
D:/winprojects/analyzer/.venv/Scripts/python.exe -m pytest
src/tests/test_stage7_valuation.py -q -p no:warnings): full file -> collected 49,
passed 47, failed 2, skipped 0 (the 2 failures are the unchanged P2 failing-first
exposures, identical to the P7/P8 state). Focused alert subset (-k "alert or divergence
or peer or flag or eps or sign or reliability or dispersion") -> collected 20,
passed 19, failed 1 (the intended flip/dependence exposure), 29 deselected.
Full multi-stage suite was not re-executed in P9; full-suite evidence is carried
forward from P7 (2 failed, 897 passed, 1 skipped, PDF-extraction file excluded).

## 1. Method and inputs reviewed

- Locked spec: D:/winprojects/analyzer/07_Stage7_Valuation.md, sections 6 (invalid-EPS
  flags), 10 (peer rule), 18 (SCENARIO_ORDER_WARNING), 26 (POSITIVE_FORECAST_REVISION
  evidence), 48 (severity vocabulary + Alerts-are-not-Buy/Sell), 49 (13 required alert
  names), 50-53 (flip/multiple/EPS/margin semantics), 54-55 (historical/industry
  divergence), 56-57 (PIT), 69 (output contract incl. valuation_alerts), 77-79/84-85
  (stress tests), 34 (UNRELIABLE_VALUATION status).
- Code: src/valuation/engine.py (_alerts lines 500-535; flag emission lines 153-199;
  _eps_flags; _scenario_sign_change_flags), parameters.py ALERT_THRESHOLDS,
  schema.py (alerts + valuation_risk_flags channels), models.py (no alert strings).
- Tests: all alert/flag assertions in src/tests/test_stage7_valuation.py (listed per
  row below). P2-P8 reports in this file (tail read before appending).
- Repo-wide searches in P9: the five sensitivity/dependence names plus
  VALUATION_BENCHMARK_DIVERGENCE, HISTORICAL/INDUSTRY_VALUATION_DIVERGENCE,
  POINT_IN_TIME_WARNING, POOR_DATA_QUALITY, FORECAST_RISK occur in NO production file
  (only in the test file's intended-failure assertions); POSITIVE_FORECAST_REVISION,
  UNRELIABLE_VALUATION likewise have zero production references. No parser of Stage 7
  alert strings was found in src/decision or src/market, but contract stability
  (spec section 66) still makes any emitted-string change a public output change.

## 2. Complete matrix

Classes: EXACT = identical name and semantics (representation channel noted).
MISMATCH = demonstrable naming mismatch against a functioning analogue.
GAP = unresolved semantic gap (no emission and/or no defined trigger).
Severity prefixes (INFO/WATCH/WARNING/CRITICAL, spec section 48) are an engine
representation convention; spec section 69 requires only the `valuation_alerts` field
with no per-alert format, so every prefixed alert is also a format couple with its
bare-name flag where one exists.

| # | Required name (spec section) | Emitted name / representation | Class | Trigger, severity, evidence, tests |
|---|---|---|---|---|
| 1 | HIGH_SCENARIO_DISPERSION (49; dispersion 40) | Flag HIGH_SCENARIO_DISPERSION + alert WARNING:HIGH_SCENARIO_DISPERSION | EXACT | Dispersion (max-min)/base > 0.50. Tests: P2 boundary (fires above 0.50, silent exactly at 0.50, silent None). Caveat (P2-8 stands): 0.50 is engine-chosen, not stated in spec 41-53. |
| 2 | LOW_FORECAST_RELIABILITY (49) | Flag LOW_FORECAST_RELIABILITY + WARNING:LOW_FORECAST_RELIABILITY | EXACT | Reliability < 40.0. Tests: P2 boundary (39.9 fires; 40.0/40.1/None silent). Same caveat: 40.0 not in spec. |
| 3 | VALUATION_BENCHMARK_DIVERGENCE (49) | WATCH:VALUATION_ABOVE_TARGET_PE / WATCH:VALUATION_BELOW_TARGET_PE | MISMATCH | Closest functional analogue: base forward P/E vs target P/E ratio >= 1.50 either direction, direction split preserved, WATCH severity. Tests: P2 divergence boundaries. Caveat: 1.50 engine-chosen. |
| 4 | HISTORICAL_VALUATION_DIVERGENCE (54; stress 75) | WATCH:FORWARD_PE_ABOVE/BELOW_HISTORICAL | MISMATCH | Forward P/E vs historical median ratio >= 1.50 either direction. Tests: P2 divergence boundaries. |
| 5 | INDUSTRY_VALUATION_DIVERGENCE (55) | WATCH:FORWARD_PE_ABOVE/BELOW_INDUSTRY | MISMATCH | Forward P/E vs industry forward median ratio >= 1.50 either direction. Tests: P2 industry-divergence assertions. |
| 6 | INSUFFICIENT_PEER_DATA (49) | Flag INSUFFICIENT_PEER_DATA (risk flags only, no severity prefix, NOT in alerts list) | GAP (representation) | Emitted iff forward series non-empty and valid count < 8. Tests: P4 peer-count tests (7 peers -> flag; 8/10 peers -> absent). Open: whether flag-level emission satisfies the section 49 "alert capability" (P8 D8). |
| 7 | NEGATIVE_EPS (49; 6; stress 73) | Flag NEGATIVE_EPS (+ NOT_APPLICABLE); status NOT_APPLICABLE; forward P/E NULL | EXACT (at flag level) | Any scenario EPS < 0. Tests: invalid-EPS tests (bear NEGATIVE_EPS, zero/negative/NaN/None variants). Same section-49 capability question as row 6. |
| 8 | SIGN_CHANGE (49; 6; evidence family 4 in 23; stress 84) | Flags SIGN_CHANGE + LOSS_TO_PROFIT / PROFIT_TO_LOSS per scenario | EXACT (at flag level) | Mixed EPS signs across scenarios. Tests: sign-change assertions. Same capability question. |
| 9 | ZERO_EPS / LOSS_TO_PROFIT / PROFIT_TO_LOSS / NOT_APPLICABLE (6) | Identical flag names | EXACT | EPS == 0 / sign direction / uncomputable states. Tests: invalid-EPS variants. |
| 10 | SCENARIO_ORDER_WARNING (18) | Identical flag | EXACT | Bear/base/bull fair values unordered. Tests: P6 ordering test (inverted EPS raises flag, probabilities still sum to 1.0). |
| 11 | INDUSTRY_BENCHMARK_INSUFFICIENT (10) | Identical flag, but trigger narrowed | MISMATCH (trigger) | Spec 10 ties it to "< 8 valid peers"; engine emits it iff target_source == INSUFFICIENT_DATA (all benchmarks missing). With 7 forward peers + valid historical median, engine emits INSUFFICIENT_PEER_DATA but NOT this flag. Tests: P6 missing-benchmark test (no series at all -> flag + CRITICAL alert). Documented, not changed (behavior change needs a decision). |
| 12 | ASSESSMENT_FLIP_RISK (49; 50; stress 77) | None emitted | GAP | No perturbation set, sizes, method, flip rule, or severity in spec (P8 D1; P2 blockers). Pinned by failing test_p2_required_flip_dependence_alerts_missing (10% shock provably flips ATTRACTIVE to FAIR, no alert). |
| 13 | HIGH_MULTIPLE_DEPENDENCE (49; 51; stress 78) | None emitted | GAP | No dependence-share formula; high_dependence_share = 0.60 dead in parameters.py line 72, zero src references (re-verified P8). P8 D2. |
| 14 | HIGH_EPS_DEPENDENCE (49; 52; stress 79, which also allows FORECAST_RISK — a name used NOWHERE in code or tests) | None emitted | GAP | No EPS-share formula, no escalation rule, no D2/D3 precedence (P8 D3). |
| 15 | MARGIN_ASSUMPTION_RISK (49; 53) | None emitted | GAP | No measure/threshold/perturbation, plus structural gap: Stage 7 inputs contain no margin series (P8 D4, strongest deferral candidate). |
| 16 | HIGH_IMPACT_HIGH_UNCERTAINTY (49; 45-47) | None emitted | GAP | No impact formula, no uncertainty selection/weights, no conjunction cutoffs; section 47 defers exact formula to a nonexistent parameter (P8 D5). |
| 17 | POOR_DATA_QUALITY (49) | None emitted | GAP | No trigger definition anywhere in the spec; no production or test reference. Defer-or-define per P8 D8. |
| 18 | POINT_IN_TIME_WARNING (49; 56-57; stress 85) | None emitted | GAP | No trigger; V1 limitation pinned by passing test (valuation_date > cutoff accepted silently, P5/P6). Needs the D7 contract choice. |
| 19 | UNRELIABLE_VALUATION (34, special states) | Never emitted (engine statuses: 5 levels + INSUFFICIENT_DATA / NOT_APPLICABLE) | GAP (minor) | No entry condition defined; engine covers the semantic neighbors. Noted for completeness, not a P7 blocker. |
| 20 | POSITIVE_FORECAST_REVISION (26) | Not emitted (evidence-path only, if at all) | Non-alert evidence name | Listed in spec as probability evidence, not an alert; no flag contract. Noted for completeness. |

Engine-emitted strings with NO spec-required counterpart: CRITICAL:INSUFFICIENT_BENCHMARK_DATA
(nearest required name: INSUFFICIENT_PEER_DATA); INFO:TOP_DRIVER:{EPS,TARGET_PE} (no spec
name; ranking itself is section-69 contract, severity INFO is section-48-consistent);
the six WATCH direction-split divergence alerts (rows 3-5); bare-name flag echoes of
rows 1-2. No test invents semantics for any of these: P2 boundary tests pin current
cutoffs explicitly as behavior pins, not spec conformance (P2 blocker 8, preserved).

## 3. Correction analysis: why the code is left unchanged

Per task 4, a correction qualifies only if it changes NO trigger semantics, severity,
public output behavior, or flag meaning. Every candidate fails at least one condition:

(a) Rename rows 3-5 to the singular spec names. FAILS: changes every emitted string
(breaking for any consumer parsing current names, against section 66 contract
stability); collapses two directional signals (above/below have opposite economics)
into one, losing information; severity and payload shape of the merged alert are
undecided (single WATCH? keep direction suffix?). This is exactly P8 D8 Proposal A
vs B vs C — a naming/governance decision, not an unambiguous mapping.
(b) Promote row 6/7/8 flags to severity-prefixed alerts (or duplicate them into
`alerts`). FAILS: duplicates vocabulary across both channels; per-name severity is
undefined by the spec; the underlying question (does flag-level emission satisfy the
section 49 "capability" requirement?) is the undecided part of P8 D8.
(c) Emit POOR_DATA_QUALITY / POINT_IN_TIME_WARNING with chosen triggers, or narrow
row 11 to the section-10 letter. FAILS: invents trigger semantics (rows 17-18) or
changes flag emission behavior (row 11).
(d) Emit any of rows 12-16. FAILS: formulas do not exist (BLOCKER-1 stands; P8 D1-D5).

Therefore NO correction was implemented and NO new test was added: there is no
behavior change to pin, emitted names are already covered by passing tests (P2
severity/divergence/reliability/dispersion boundaries, P4 peer-count flags, P6
ordering/missing-benchmark paths, invalid-EPS variants), and the absences are already
pinned by the two intended P2 failures. No existing test was removed, weakened, or
rewritten.

## 4. Six validation layers (executed vs carried)

1. Unit/formula: EXECUTED (P9 reruns above; 47/49 with the 2 known intended failures).
2. Contract/boundary: EXECUTED — this matrix is the contract evidence; peer-count,
   determinism, severity-vocabulary, and boundary pins re-executed as part of the
   47 passes, not merely cited.
3. Production-path/integration: NOT EXECUTED in P9 (carried from P6/P7: forecast leg
   uses real Stage 5 output; benchmark PIT leg remains fixture-based by V1 design).
4. Adversarial/negative: EXECUTED (same rerun; finite-input guards, rationale/bound
   rejections unchanged).
5. Regression: EXECUTED — identical 47/2 counts to P7/P8; no production file changed
   in P9 so no regression is possible (git status shows only the pre-existing
   `M stage_7_prompts.md`).
6. Independent audit: EXECUTED — this read-only matrix plus the correction analysis;
   nothing claimed implemented beyond the reruns and the trace. Stage 7 blockers are
   NOT claimed resolved: BLOCKER-1 (rows 12-16), BLOCKER-2 (sector drivers, out of
   P9 scope but re-confirmed failing), MATERIAL-1 (rows 3-5, 11), MATERIAL-2
   (row 18) all stand.

## 5. Exact decisions required (nothing invented)

1. D8 name mapping (decide now, per P8): rename vs alias vs spec-amendment for rows
   3-5; whether flag-level emission satisfies section 49 for rows 6-8 (and which
   severities if promoted); row 11 trigger (spec-10 letter vs current fallback-gated
   emission).
2. Rows 17-18 triggers: define POOR_DATA_QUALITY and POINT_IN_TIME_WARNING semantics
   or defer them with the section-49 capability claim corrected.
3. Rows 12-16 formulas: P8 D1-D5 unchanged (dependence-share, flip-risk tuple,
   escalation/precedence, margin contract-or-proxy, impact/uncertainty cutoffs).

## 6. Scope confirmation

Read-only audit plus two confirming test reruns: inspected the spec, Stage 7
alert/flag/parameter/schema code, all alert-related test assertions, and the P2-P8
reports; ran only the Stage 7 pytest commands above; modified no source, test,
specification, parameter, dependency, or configuration; invented no financial data,
formulas, thresholds, severities, or trigger semantics; left the two failing tests
failing as required. This English-only append preserves all earlier reports. Stage 7
is NOT declared frozen. Work stops after appending the report.
========================================================
# P10 — Model Parameterization and Determinism Audit (APPENDED, ENGLISH ONLY)

Date (UTC): 2026-10-12. P10 source: the P10 task prompt (no stage_7_prompts.md
section; prompt provenance is the task text itself). Work limited to the Stage 7
specification (07_Stage7_Valuation.md), src/valuation/engine.py, models.py,
parameters.py, schema.py, and src/tests/test_stage7_valuation.py plus the
Stage 9 consumer test file for regression. No Stages 1-6 or 8-9 file modified.
No dependencies, migrations, commits, pushes, pulls, or branch changes. No
financial data, formulas, thresholds, or semantics invented; ambiguities recorded
as blockers. Stage 7 is NOT declared frozen.

## 1. Constants table (Task 1-2)

Legend. Versioned = present in parameters.py with its current value consumed by
the engine. Explicit = stated numerically or structurally in the spec.
Indirect = supported by spec structure but without a number. Unspecified = no
spec basis. Risk notes cover both changing and leaving hardcoded.

| # | Constant / formula (engine location) | Current value | Spec section / requirement | Versioned | Spec basis | Risk if changed / if left hardcoded |
|---|---|---|---|---|---|---|
| C1 | SCENARIO_WEIGHTS prior 20/60/20 (engine _resolve_probabilities) | 0.20/0.60/0.20 | Sec 22 states the exact prior and calls it a Model Version Parameter | Yes | Explicit | Change: shifts every expected fair value and status; needs MODEL_VERSION bump. Hardcoded risk: none, it is versioned. |
| C2 | PROBABILITY_EVIDENCE_BLEND (engine _resolve_probabilities) | 0.25 | Sec 23-24 require four family-level votes with no double counting; no numeric blend stated | Yes | Indirect | Change: shifts all evidence-blended probabilities. The 0.25 equal-family vote is an implementation choice pinned by tests, not a spec number; changing it alters behavior without spec direction. |
| C3 | SCENARIO_MULTIPLE_MAX_ABS_ADJUSTMENT (engine _resolve_scenario_multiple_adjustments) | 0.20 | Sec 17 bans fixed 0.8/1.2 gaps and requires explainable, versioned, backtestable, rationale-backed multiples | Yes | Indirect | Change: widens/narrows allowed multiple adjustments; rationale gate unchanged. Value itself is engine-chosen, not spec-stated. |
| C4 | VALUATION_THRESHOLDS 7 cutoffs (engine _valuation_status) | 30/15/15/5/-10/-25/-10 | Sec 35 gives this exact example table and requires storage as Valuation Model Parameters | Yes (after P10 fix; C4b was the gap) | Explicit | Change: moves status boundaries for every valuation; needs MODEL_VERSION bump. |
| C4b | Expensive base-upside cutoff literal `< 0.0` (engine _valuation_status line 417, pre-fix) | 0.0 hardcoded | Sec 35 "Base Upside < 0%" — the zero IS the specified value | No (pre-fix) / Yes (post-fix, key expensive_base_upside = 0.0) | Explicit | THE P10 CORRECTION. Pre-fix the engine consumed 6 of 7 specified cutoffs from parameters and one literal. Post-fix all 7 are versioned; outputs identical (Sec 4). |
| C5 | CONFIDENCE_THRESHOLDS 90/75/60/40 (engine _confidence_label) | 90/75/60/40 | Sec 39 gives these exact label bands and calls them Model Version Parameters | Yes | Explicit | Change: relabels confidence for identical scores. |
| C6 | RISK_THRESHOLDS 40/0.50/-30/60/-15 (engine _valuation_risk) | as listed | Sec 36 lists risk factors but states NO numeric cutoffs | Yes | Unspecified | Change: moves EXTREME/HIGH/MEDIUM boundaries without spec direction. Values are engine-chosen and pinned by tests only; recorded as decision required, not corrected. |
| C7 | ALERT_THRESHOLDS dispersion 0.50, reliability 40.0, 3 divergence ratios 1.50 (engine _alerts) | as listed | Sec 49 names the alert categories; no numeric trigger stated in Sec 41-53 | Yes | Unspecified | Same as C6: versioned but spec-unstated; boundary tests pin behavior, not conformance (P2 blocker 8 preserved). |
| C8 | high_dependence_share 0.60 (parameters.py line 72) | 0.60, zero src references | Sec 51-52 require dependence alerts but define no share formula | Defined but dead | Unspecified | Cannot wire without inventing the share formula (P8 D2/D3). Left untouched; BLOCKER-1 stands. |
| C9 | Confidence blend 0.40/0.20/0.20/0.20 + benchmark 100/25 + dispersion penalty slope 50 cap 40 (engine _valuation_confidence lines 432-434) | as listed | Sec 38 lists confidence factors but gives NO weights; Sec 64 lists Confidence Formula as version-gated but gives no formula | No | Unspecified | P7 MINOR-1 re-confirmed. Change: shifts every confidence score. No spec basis for any replacement set, so NO reparameterization performed; recorded as decision required (P8 D9 stands). Needs the record-store mechanism decision. |
| C10 | Driver-uncertainty blend 0.5/0.3/0.2 (engine _driver_analysis line 493) | 0.5/0.3/0.2 | Sec 46 lists five possible uncertainty bases with no selection or weights | No | Unspecified | Same as C9: no basis for replacement weights; untouched. |
| C11 | Dispersion formula (max-min)/base (engine _scenario_dispersion) | formula | Sec 40 explicitly requires the dispersion formula to be versioned | No (formula in code, not a named parameter) | Indirect (method unspecified, versioning required) | Change: alters dispersion, risk, alerts, confidence penalty. Untouched: renaming the formula into a parameter without the Sec 65 record store (effective_from/description) would be cosmetic versioning. |
| C12 | SENSITIVITY_PERTURBATION (engine _driver_analysis) | 0.10 | Sec 45 "reasonable change" with no size; Sec 50 "relatively small" with no size | Yes | Indirect | The 0.10 is engine-chosen; used only for the FV-identity one-at-a-time shocks (P3). Must NOT be reused as the flip-risk perturbation without a spec decision (P8 D1). |
| C13 | Score defaults: reliability 50, probability 50, quality 100; data_quality None/NaN -> 100 (engine _clamp_score call sites) | 50/50/100 | No spec section defines fallback defaults | No | Unspecified | Change: shifts confidence/uncertainty on missing data. Untouched; recorded as decision required. |
| C14 | Rounding policy: fair value round 2, P/E round 4, confidence round 4, impact/uncertainty/review round 4 (models.py, engine.py) | as listed | No spec section defines rounding | No | Unspecified | Change: breaks golden values and determinism pins at the 4th decimal. Untouched. |
| C15 | Epsilon guards: total floor 1e-9 (driver), dispersion exact-0.50 silence via `>` (engine) | as listed | No spec basis | No | Unspecified | Numerical-stability micro-constants; changing them is behavior-neutral except at degenerate inputs. Untouched. |
| C16 | MIN_INDUSTRY_PEERS 8 (engine _select_target_pe, flags) | 8 | Sec 10 and non-negotiable rule 6 state exactly 8 | Yes | Explicit | Change: contradicts the locked spec. None. |
| C17 | Legacy/unused: INDUSTRY_TARGET_PE {} , SCENARIO_PE_MULTIPLIER 1.00s, calculate_nav_fair_value, probability_confidence default 50.0, data_quality_score default 100.0 | as listed | Sec 17 (no fixed gaps), Sec 44 (P/NAV belongs to Stage 7 but no formula), Sec 28 (probability confidence exists, no default) | Exported but unconsumed (multiplier/nav) / signature defaults | Indirect or Unspecified | Removing exports breaks backward compatibility (src/valuation/__init__.py); wiring NAV needs the missing P/NAV formula (P8 D6). Untouched. |

Summary counts: 17 rows traced. Versioned after the P10 fix: C1, C2, C3, C4
(incl. C4b), C5, C6, C7, C12, C16 (9 of 17). Hardcoded or otherwise
unversioned: C9, C10, C11, C13, C14, C15 (6 of 17). Defined-but-dead or
legacy: C8, C17 (2 of 17). Exactly ONE hardcoded value had an explicit spec
basis and was corrected (C4b). The remaining six hardcoded items have no spec
numbers and were deliberately left unchanged.

## 2. P7 MINOR-1 investigation (Task 3)

P7 MINOR-1 states the confidence/risk/dispersion blend weights and related
constants are hardcoded rather than versioned parameters, noting Sec 64-65
cover thresholds (versioned) but not the blend weights. Re-verified in P10:
engine.py lines 432-434 contain literals 0.40/0.20/0.20/0.20, 100.0/25.0,
50.0/40.0; line 493 contains 0.5/0.3/0.2; lines 399-406 contain the dispersion
formula inline; none appears in parameters.py. The spec lists Confidence
Formula, Risk Formula, and Driver Priority Formula as version-gated (Sec 64)
and requires tunable thresholds outside hard-code (Sec 65), but it never gives
replacement weights, the uncertainty-base selection, or the Sec 65 record
format (model_version, parameter_name, parameter_value, effective_from,
description) — parameters.py holds values but no effective_from/description
records (P8 D9). Moving literals into parameters.py without the record store
would rename the problem, not fix traceability; inventing "spec-backed"
weights is impossible since none exist. Therefore NO reparameterization of C9,
C10, or C11 was performed. Required decisions (unchanged from P8 D9): (a) the
parameter-version record store mechanism (code registry vs DB table vs file);
(b) confirmation that blend weights and the dispersion formula are in scope as
tunable. Proposal A (code registry) remains small and need not be deferred, but
it is a user decision, not an audit action.

## 3. Determinism and traceability (Task 4)

Parameter changes preserve deterministic output if and only if (i) the engine
reads the parameter once per run with no randomness, time, or iteration-order
dependence, and (ii) model_version changes whenever a value changes (Sec 64:
old versions never overwritten). The P10 correction satisfies both: the new
key is read from the same VALUATION_THRESHOLDS dict on the same code path, and
MODEL_VERSION is still STAGE7_V1 because default outputs are bit-identical
(Sec 4). Traceability gap stands: parameters.py has no effective_from /
description records (Sec 65 record example), so a future value change is
traceable only through git history plus MODEL_VERSION, not through a parameter
audit trail. That gap is the P8 D9 record-store decision, not something P10
closes. Full-contract repeat-run determinism (excluding wall-clock
calculation_timestamp) re-executed as part of the 49 passes.

## 4. Strictly specification-backed correction (Task 5)

Implemented, preserving existing outputs:

- D:/winprojects/analyzer/src/valuation/parameters.py — added one key to
  VALUATION_THRESHOLDS: "expensive_base_upside": 0.0. Spec basis: Sec 35
  Expensive rule "Expected Upside <= -10% AND Base Upside < 0%" — the 0% cutoff
  is explicit in the specification, and Sec 35 requires these thresholds to be
  stored as Valuation Model Parameters. Pre-fix the engine consumed six of the
  seven Sec-35 cutoffs from parameters and compared the seventh against the
  literal `0.0`; that literal was the only spec-explicit hardcoded constant in
  the table.
- D:/winprojects/analyzer/src/valuation/engine.py — one comparison changed in
  _valuation_status: `base_upside < 0.0` becomes
  `base_upside < t["expensive_base_upside"]`. The comparison semantics are
  identical for the default value (strict less-than against 0.0).
- D:/winprojects/analyzer/src/tests/test_stage7_valuation.py — two P10 tests
  appended, zero existing tests modified:
  1. test_p10_expensive_base_upside_parameterized_outputs_unchanged: asserts
     the key exists at 0.0, asserts the golden valuation (fair values
     1050.0/1260.0/1470.0, expected 1260.0, margin 26.0, ATTRACTIVE,
     VALUATION_CONTRACT_V1/STAGE7_V1), asserts the full-contract
     representation hash equals the pre-change golden hash
     1990c6393233121df4bccea381ac6539461443ea1a77f1e6e09a1cf819b71255, and
     asserts the boundary pair bracketing the cutoff (base upside -2.0 with
     expected -10.4 -> EXPENSIVE; base upside +1.5 with expected -10.4 ->
     FAIR).
  2. test_p10_expensive_threshold_consumed_from_parameters: mutates the key
     to -50.0, proves the EXPENSIVE case flips to FAIR (parameter actually
     consumed, not a dead export), restores the key in finally, and proves
     the restored engine returns EXPENSIVE again.

Pre/post output comparison (representative cases run before and after the
change; identical inputs, full-contract dataclass dict minus wall-clock
calculation_timestamp, sha256 over canonical JSON):
- Golden case (EPS 150/180/210, price 1000, historical 6.5/7.0/8.0):
  pre 1990c6393233121df4bccea381ac6539461443ea1a77f1e6e09a1cf819b71255 /
  ATTRACTIVE 75.3333 LOW; post identical hash / identical triple. EXACT
  DIFFERENCES: NONE — zero fields differ.
- Expensive-boundary case (EPS 70/140/150): pre base -2.0 / expected -10.4 /
  EXPENSIVE; post identical. EXACT DIFFERENCES: NONE.
- Fair-boundary case (EPS 55/145/150): pre base +1.5 / expected -10.4 / FAIR;
  post identical. EXACT DIFFERENCES: NONE.
No other output changed: the correction touches only the Expensive branch
predicate, and the default key value reproduces the literal exactly.

## 5. Values without specification basis (Task 6, no replacement selected)

Recorded as required decisions, not implemented: RISK_THRESHOLDS numerics (C6),
alert-trigger numerics 0.50/40.0/1.50 (C7), confidence blend weights/benchmark
levels/penalty slope and cap (C9), driver-uncertainty blend (C10), dispersion
formula versioning (C11), score fallback defaults 50/50/100 (C13), rounding
policy (C14), epsilon guards (C15), high_dependence_share wiring (C8, needs the
dependence-share formula), legacy multiplier/NAV exports (C17). Per Task 7, no
attempt was made to infer the flip-risk, dependence, margin-risk,
sector-mapping, or PIT-contract resolutions; P8 D1-D7 and P7 BLOCKER-1/2 plus
MATERIAL-1/2 stand unchanged.

## 6. Validation — six layers with exact commands and results

Cwd for all commands: D:/winprojects/analyzer. Interpreter:
D:/winprojects/analyzer/.venv/Scripts/python.exe.

1. Unit/formula: EXECUTED. `... -m pytest src/tests/test_stage7_valuation.py
   -q -p no:warnings` -> collected 51, passed 49, failed 2, skipped 0. The 2
   failures are the unchanged pre-existing intended P2 failing-first exposures
   (test_p2_sector_driver_decomposition_missing,
   test_p2_required_flip_dependence_alerts_missing). All 11 baseline, 7 P2, 6
   P3, 6 P4, 10 P5, 7 P6, and 2 P10 tests pass.
2. Contract/boundary: EXECUTED for P10 scope. The Expensive cutoff boundary
   pair (-2.0 -> EXPENSIVE / +1.5 -> FAIR at expected -10.4) plus the
   parameter-consumption mutation test; peer-count, determinism, severity, and
   divergence pins re-executed as part of the 49 passes.
3. Production-path/integration: PARTIAL (carried, not re-proved in P10). No
   P10 test uses real Stage 5 output; forecast-leg evidence carried from P6
   (real ForecastEngine output consumed); benchmark leg remains fixture-based
   by V1 design. No production-path run executed in P10 beyond the synthetic
   golden/boundary cases above.
4. Adversarial/negative: EXECUTED (carried re-execution). Finite-input guards,
   rationale/bound rejections, and invalid-EPS/price variants re-executed as
   part of the 49 passes; no new adversarial test added in P10 (the mutation
   test is a consumption proof, not an attack case).
5. Regression: EXECUTED. Stage 7: all 47 previously passing tests still pass
   (49 now includes the 2 new P10). Stage 9 consumer:
   `... -m pytest src/tests/test_stage9_decision.py -q -p no:warnings` ->
   13 passed. Combined file run: 51 + 13 = 64 tests, 62 passed, 2 intended
   P2 failures. Pre/post golden-hash comparison: zero differences (Sec 4).
   Full multi-stage suite: ABSENT in P10 (not re-executed; P7 evidence
   carried: 2 failed, 897 passed, 1 skipped, PDF-extraction file excluded).
6. Independent audit: EXECUTED — this append plus the pre/post hash evidence.
   Nothing claimed implemented beyond the C4b correction and its two tests;
   nothing claimed validated beyond the stated reruns.

## 7. Scope confirmation

Stage 7 parameters.py (one key) + engine.py (one predicate) + focused tests
(two appended) only; no spec, dependency, migration, or config change; no
existing test weakened; Stages 1-6 and 8-9 untouched (Stage 9 read-only
regression run); no git operations of any kind; English-only append with all
prior content preserved. The unresolved flip-risk, dependence, margin-risk,
sector-mapping, and PIT-contract blockers were not touched by inference. Stage
7 is NOT declared frozen. Work stops after appending the report.
========================================================
# P11 — Stage 7 Consolidated Regression and Evidence Audit (APPENDED, ENGLISH ONLY)

Date (UTC): 2026-10-12. P11 source: the P11 task prompt (no stage_7_prompts.md
section; prompt provenance is the task text itself). Read-only verification
except for this appended report: no source, test, specification, parameter,
dependency, or configuration file was modified in P11. No commits, pushes,
pulls, branch changes, GitHub/API, or remote operations. Frozen Stages 1-6
and 8-9 untouched. No financial data, formulas, thresholds, or semantics
invented; ambiguities recorded as blockers. Stage 7 is NOT declared frozen.

## 1. Test-count reconciliation P2-P10 (Task 1)

| Report | Collected | Passed | Failed | Delta vs prior (exact) |
|---|---|---|---|---|
| Baseline | 11 | 11 | 0 | — |
| P2 | 20 | 18 | 2 | +9 tests: 7 pass, 2 intended failing-first exposures |
| P3 | 26 | 24 | 2 | +6 P3 tests, all pass |
| P4 | 32 | 30 | 2 | +6 P4 tests, all pass |
| P5 | 42 | 40 | 2 | +10 P5 tests, all pass |
| P6 | 49 | 47 | 2 | +7 P6 tests, all pass |
| P7 | 49 | 47 | 2 | Rerun, identical; full suite 2F/897P/1S/0E |
| P8 | 49 | 47 | 2 | Rerun, identical; full suite carried from P7 |
| P9 | 49 | 47 | 2 | Rerun, identical; focused alert subset 20 collected / 19 passed / 1 failed / 29 deselected |
| P10 | 51 | 49 | 2 | +2 P10 tests, all pass; Stage 9 13/13; combined 64 tests, 62 passed, 2 intended failures |
| P11 fresh (Sec 3) | 51 | 49 | 2 | Identical to P10; Stage 9 13/13; full suite 2F/899P/1S/0E |

Arithmetic chain is fully consistent (11+9+6+6+10+7+0+0+0+2 = 51). The two
failures are the same two P2 tests in every report from P2 through the P11
fresh run; no report treats them as passing. Full-suite reconciliation: P7 897
passed to P11 899 passed is exactly +2 (the two new P10 tests); failures
identical. P6 reported 3 failed / 893 passed / 1 skipped / 4 errors with the
third failure and 4 errors unattributed; that anomaly has now failed to recur
in two consecutive full-suite runs (P7, P11) and is classified
transient/environmental in Sec 4 — not a regression.

## 2. P2 failing-first tests: present and unchanged (Task 2)

- test_p2_sector_driver_decomposition_missing is present at
  src/tests/test_stage7_valuation.py line 406; content matches the P2 report
  (PETROCHEMICAL/BANK/HOLDING union ranking must contain REVENUE, NII, NAV).
- test_p2_required_flip_dependence_alerts_missing is present at line 425;
  content matches the P2 report (SENSITIVITY_PERTURBATION 0.10 guard, flip
  ATTRACTIVE-to-FAIR pair, five required alert names asserted jointly).
- Diff of the test file against the P2 commit f18cc1f for these two tests:
  hunk @@ -463,3 +463,694 @@ — purely additive insertions after line 463
  (P3-P10 appends); zero modified lines in either P2 test body. Both still
  fail in the P11 fresh run for the documented reasons (Sec 3), so they still
  pin the absences. No restore or rewrite performed; none warranted.

## 3. Fresh validation runs (Tasks 3-5)

Cwd for all commands: D:/winprojects/analyzer. Interpreter:
D:/winprojects/analyzer/.venv/Scripts/python.exe (venv interpreter per
project rule; system python lacks sqlalchemy).

Run A — Stage 7 file.
Command: D:/winprojects/analyzer/.venv/Scripts/python.exe -m pytest
src/tests/test_stage7_valuation.py -q -p no:warnings
Result: collected 51, passed 49, failed 2, skipped 0, errors 0, duration
1.03s.
Exact failures:
- FAILED test_p2_sector_driver_decomposition_missing — documented assertion
  (required {REVENUE, NII, NAV} not subset of observed {EPS, TARGET_PE}).
- FAILED test_p2_required_flip_dependence_alerts_missing — AssertionError:
  Missing required alerts: ['ASSESSMENT_FLIP_RISK',
  'HIGH_MULTIPLE_DEPENDENCE', 'HIGH_EPS_DEPENDENCE', 'MARGIN_ASSUMPTION_RISK',
  'HIGH_IMPACT_HIGH_UNCERTAINTY'].

Run B — Stage 9 consumer.
Command: D:/winprojects/analyzer/.venv/Scripts/python.exe -m pytest
src/tests/test_stage9_decision.py -q -p no:warnings
Result: 13 passed, 0 failed, 0 skipped, duration 0.64s.

Run C — full suite.
Command: D:/winprojects/analyzer/.venv/Scripts/python.exe -m pytest
src/tests/ -q -p no:warnings -rs --ignore=src/tests/test_codal_pdf_extraction.py
Result: 2 failed, 899 passed, 1 skipped, 0 errors, duration 143.51s
(0:02:23). Exclusion: src/tests/test_codal_pdf_extraction.py ignored because
it requires real Codal sample PDFs unavailable in this environment (same
exclusion as P6/P7; no substitute PDF used). The 1 skip is
src/tests/test_codal_extraction.py:307 (real Codal sample PDF not available
in CI). The 2 failures are the Run A P2 exposures; no other file failed.

## 4. Failure classification (Task 6, evidence-backed)

- Current Stage 7 blockers: the 2 Run A failures = P7 BLOCKER-1
  (flip/dependence alert family; a 10% EPS shock provably flips ATTRACTIVE to
  FAIR with no alert, P2/P6 evidence) and BLOCKER-2 (sector decomposition;
  ranking always {EPS, TARGET_PE}). Root cause per the P8 decision package is
  missing specification formulas (dependence-share, flip-risk tuple,
  impact/uncertainty cutoffs, margin trigger, sector mapping), not
  implementation error. Unchanged since P2.
- Regressions caused by recent changes: NONE FOUND. The working-tree P10
  production diff is one parameter key ("expensive_base_upside": 0.0) plus one
  predicate consuming it, with P10 pre/post golden-hash evidence of zero
  output differences; all 47 pre-P10 passes still pass, the 2 new P10 tests
  pass, Stage 9 is 13/13, and the full-suite delta (+2) is exactly the new
  P10 tests. No repair action taken — none warranted under the read-only
  constraint.
- Unrelated pre-existing failures: NONE OBSERVED. Zero failures outside the
  two known Stage 7 exposures; zero errors.
- Environment/fixture limitations: (a) PDF-extraction file excluded plus 1
  Codal-sample skip — fixture unavailable, same as P6/P7; (b) P6's transient
  third failure plus 4 errors, non-recurrent in P7 and P11, classified
  transient/environmental with two consecutive clean runs as evidence — not
  attributed to any Stage 7 change.

## 5. Six-layer reassessment (Task 7, fresh vs carried)

1. Unit/formula: FRESH EVIDENCE (Run A 49/51; the 2 failures assert absent
   required behavior and fail for the right reason).
2. Contract/boundary: FRESH EVIDENCE (peer-count, determinism,
   severity-vocabulary, NaN/inf guards, Expensive-cutoff boundary re-executed
   as part of the 49 passes).
3. Production-path/integration: CARRIED from P6, re-stated precisely.
   GENUINE Stage 5-to-Stage 7 integration was achieved in P6 (real
   ForecastEngine output consumed through the production constructor; cutoff
   inherited; not re-executed in P11). This is explicitly distinct from
   benchmark-series PIT verification, which remains fixture-based and
   metadata-only by V1 design (undated float series; valuation_date-vs-cutoff
   unchecked; P5/P6 pinned limitation stands).
4. Adversarial/negative: FRESH EVIDENCE (finite-input guards, rationale/bound
   rejections, invalid-EPS/price variants re-executed in Run A).
5. Regression: FRESH EVIDENCE (Runs A+B+C; golden values, hierarchy,
   probabilities, NULL rules unchanged).
6. Independent audit: FRESH EVIDENCE (this read-only append; every count
   above was executed in P11 except where explicitly marked carried).

## 6. Unresolved-findings register (Task 8)

| ID | Severity | Finding + evidence | Affected requirement | Prerequisite decision | Next bounded action |
|---|---|---|---|---|---|
| UF-1 | Blocker | Flip/dependence alert family absent (Run A failure names all five; P8 D1-D5) | Spec 49-53; stress 77-79 | User fixes formulas/severities or defers out of V1 | Spec amendment first; then implement and green the test |
| UF-2 | Blocker | Sector decomposition absent (Run A; ranking {EPS,TARGET_PE}; P8 D6) | Spec 42-44; P/NAV claim | Mapping/linkage/NAV decisions or deferral | Same as UF-1 |
| UF-3 | Material | Alert-name mismatches (P9 matrix rows 3-5, 11; behavior pinned, not conformance) | Spec 49, 54-55 vs emitted names | D8 rename/alias/amend choice (decide now) | Apply chosen mapping; pin with tests |
| UF-4 | Material | PIT cross-validation absent (P5/P6 pinned test; metadata-only flag) | Spec 56-57; stress 85 | D7 provenance-vs-attestation plus date-rule choice | Implement chosen option or correct PASS claims (D7-C) |
| UF-5 | Minor | Unversioned blends/formulas/defaults/rounding (P10 C9-C15; C4b closed in P10) | Spec 64-65 | D9 record-store mechanism plus scope | Move to chosen registry; no weight invention |
| UF-6 | Minor (subsumed by UF-1) | high_dependence_share 0.60 defined-but-dead (P10 C8; zero src references) | Spec 51-52 | D2 share-formula decision | Wire or remove with the formula decision |
| UF-7 | Environment | PDF-extraction exclusion plus Codal skip (Run C) | Test coverage only | Fixture availability | Re-run file when real Codal samples exist; no substitution |
| UF-8 | Cosmetic | datetime.utcnow() DeprecationWarning persists | Code hygiene | None | Replace with timezone-aware call in a bounded change |

Working-tree note: git status shows uncommitted P10 changes (engine.py one
predicate, parameters.py one key, test file plus 2 tests, stage_7_prompts.md,
temp_report2.md); P11 modified nothing — verification was read-only (pytest
plus git status/diff) apart from this append. schema.py is unmodified since
P4, consistent with no contract change after P4.

## 7. Scope confirmation

Read-only verification plus this English-only append: inspected the full
P2-P10 history in temp_report2.md, the Stage 7 files changed by P2-P10
(engine.py, parameters.py, schema.py, test file), and the Stage 9 consumer
file for regression; ran only the three pytest commands and read-only git
commands above; changed no code (no new regression proven, so no repair
warranted); weakened no test; invented no data, formulas, thresholds, or
semantics; performed no commits, pushes, pulls, or branch changes; Stages 1-6
and 8-9 untouched (Stage 9 read-only regression run). All earlier reports
preserved. Stage 7 is NOT declared frozen and remains unfrozen unless a
future independent audit explicitly approves it and the user separately
authorizes the freeze decision. Work stops after appending the report.
========================================================
# P12 — UTC Deprecation Cleanup Report (APPENDED, ENGLISH ONLY)

Date (UTC): 2026-10-12. Scope: `src/valuation/engine.py` plus one focused
test in `src/tests/test_stage7_valuation.py`; inspected the datetime
construction at engine.py:212, the `normalize_datetime` path in
`src/forecast/schema.py:231-243`, and this file. No spec, dependency,
migration, or config change; no Stages 1-6 or 8-9 change; no commits,
pushes, pulls, or branch changes. Stage 7 is NOT declared frozen.

## 1. utcnow() uses found and how replaced

Exactly one relevant `datetime.utcnow()` use existed in the scoped Stage 7
code: `src/valuation/engine.py:212`,
`calculation_timestamp=datetime.utcnow()` (naive datetime, triggers
`DeprecationWarning: datetime.datetime.utcnow() is deprecated ... Use
timezone-aware objects`). Replaced with
`calculation_timestamp=datetime.now(timezone.utc)` and the import widened
from `from datetime import datetime` to
`from datetime import datetime, timezone`. The pre-existing
`normalize_datetime` contract is untouched: naive inputs are still folded
onto UTC (`value.replace(tzinfo=timezone.utc)`), aware inputs are still
converted via `.astimezone(timezone.utc)`. No valuation date, cutoff
semantic, PIT behavior, formula, alert trigger, or model parameter changed.
This does NOT close the PIT blocker (P11 UF-4 stands); it is datetime
construction and code hygiene only.

## 2. Focused test added: yes, and why

Added `test_p12_calculation_timestamp_utc_aware_and_deterministic`
(test file line 1159): asserts `calculation_timestamp.tzinfo is not None`
with a UTC offset, runs the identical valuation twice, drops only
`calculation_timestamp` from both `dataclasses.asdict` outputs, and asserts
the dicts are equal; pins golden outputs (base fair value 1260.0, expected
fair value 1260.0, status ATTRACTIVE). Needed because no prior test pinned
timestamp awareness or whole-output determinism excluding the wall clock.
No existing test was modified or weakened.

## 3. Pre/post output comparison

Representative golden case (PETROCHEMICAL, price 1000.0, reliability 85.0,
peers [6.5, 7.0, 8.0], confidence 90.0):
pre-change timestamp naive `datetime(2026,10,12,14,2,18)` with
`tzinfo=None`; post-change timestamp
`datetime(2026,10,12,14,3,2, tzinfo=timezone.utc)`. All other fields
identical: base fair value 1260.0, expected fair value 1260.0, status
ATTRACTIVE, alerts ["INFO:TOP_DRIVER:EPS"], driver impact/uncertainty
unchanged. Zero behavioral differences apart from the wall-clock field.

## 4. Six validation layers (separately)

Cwd for all commands: D:/winprojects/analyzer. Interpreter:
D:/winprojects/analyzer/.venv/Scripts/python.exe (venv; system python
lacks sqlalchemy).

1. Unit/formula: EXECUTED. Stage 7 file post-change:
`... -m pytest src/tests/test_stage7_valuation.py -q` -> collected 52,
50 passed, 2 failed (the same two long-standing P2 failing-first
exposures: test_p2_sector_driver_decomposition_missing,
test_p2_required_flip_dependence_alerts_missing), 0 warnings.
Pre-change baseline (stashed fix): 51 collected, 49 passed, same 2
failed, 98 DeprecationWarnings from engine.py:212. Delta is exactly +1
(the new P12 test, passing); no prior pass broke.
2. Contract/boundary: EXECUTED as part of layer 1 (peer-count,
determinism, NaN/inf guards, cutoff normalization re-executed among the
50 passes); the new P12 test adds the timestamp-awareness contract pin.
3. Production-path/integration: NOT freshly executed in P12 (same carried
P6 evidence as P11: genuine Stage 5-to-Stage 7 integration achieved in
P6, not re-run here).
4. Adversarial/negative: EXECUTED (finite-input guards, rationale/bound
rejections, invalid-EPS/price variants re-executed as part of the 50
passes; no new adversarial test added in P12).
5. Regression: EXECUTED. Stage 9 consumer post-change:
`... -m pytest src/tests/test_stage9_decision.py -q` -> 13 passed,
52 warnings (all pre-existing Stage 9/decision utcnow() sites, out of
P12 scope and untouched). Pre-change Stage 9: identical 13 passed /
52 warnings. Full multi-stage suite: NOT freshly executed in P12
(P11 evidence carried: 2 failed, 899 passed, 1 skipped, 0 errors).
No Stage 9 file modified.
6. Independent audit: EXECUTED — this append plus the pre/post
snapshots. Nothing claimed implemented beyond the one-line construction
fix and its test; nothing claimed validated beyond the stated reruns.

## 5. Warning counts

Stage 7 file: pre-change 98 DeprecationWarnings (all engine.py:212);
post-change 0 warnings. Stage 9 file: 52 warnings both pre- and post-
change (out-of-scope `datetime.utcnow()` sites in decision engine,
decision schema, and Stage 9 test fixtures; intentionally untouched per
P12 boundaries). No other warnings observed.

## 6. Scope confirmation

engine.py (2 lines: import + construction) and the test file (1 import
line + 29-line appended test) only; pre-existing uncommitted
stage_7_prompts.md P12 task-text addition left as found; no spec,
dependency, migration, or unrelated code touched; no financial data,
formulas, thresholds, or semantics invented; English-only append with all
prior content preserved. The PIT blocker and all P11 unresolved findings
(UF-1 through UF-7) are untouched by this change. Stage 7 is NOT
declared frozen. Work stops after appending the report.
========================================================
# P13 — Stage 7 PIT Contract Impact Assessment (APPENDED, ENGLISH ONLY)

Date (UTC): 2026-10-12. Read-only impact assessment; zero source, test, schema, spec, parameter, dependency, or config changes. Cwd D:/winprojects/analyzer; interpreter D:/winprojects/analyzer/.venv/Scripts/python.exe. No commits, pushes, pulls, branch changes, remote, or GitHub. Stage 7 is NOT declared frozen. No data, dates, provenance, or formulas invented.

## 1. Caller trace: every supplier of the six PIT-relevant inputs (verified facts)

1.1 Boundary signature. `ValuationEngine.calculate_valuation` (src/valuation/engine.py:57-79) accepts: `valuation_date`, `market_price_date`, `data_cutoff_datetime` (all Optional[datetime]; normalized via `normalize_datetime`, echoed to `ValuationResult`, never compared against each other); `historical_pe_values`, `industry_forward_pe_values`, `industry_ttm_pe_values` (all Optional[Sequence[Optional[float]]]; finite-filtered by `_finite_or_none`, reduced to medians plus a forward-only peer count; no dates, publication stamps, or versions accepted or stored).

1.2 Production callers: NONE. Grep for `calculate_valuation|historical_pe_values|industry_forward_pe_values|industry_ttm_pe_values` across src/ matches only src/valuation/engine.py (the definition) and src/tests/test_stage7_valuation.py (33 hits). No non-test code supplies any of the six inputs. The only downstream consumer is `src/decision/engine.py:250`, which passes `valuation_result.data_cutoff_datetime` through (`cutoff = data_cutoff_datetime or valuation_result.data_cutoff_datetime`) without validating any Stage 7 PIT input.

1.3 Test-caller shapes. Bare undated float lists (e.g. `[6.5, 7.0, 8.0]`, `[6.0]*8`); naive or aware datetimes normalized to UTC. Pinned behavior proves the gap: `test_p5_undated_benchmark_series_carry_no_provenance` and `test_p6_cutoff_pit_limitation_pinned` show a valuation_date of 2026-06-01 with a cutoff of 2026-01-01 accepted with no rejection and no PIT flag.

1.4 Spec boundary demands. 07_Stage7_Valuation.md: section 3 requires every output to carry valuation timestamp, model version, and data_cutoff_datetime; section 7 requires price use to record valuation_date and market_price_date; section 69 (output contract) lists valuation_date, market_price_date, and data_cutoff_datetime; section 56 requires the PIT tuple (Price Date, Forecast Cutoff, Report Publication Date, Report Version); section 57 requires current analysis to use the Latest Valid Version and backtests to use the version actually available on that date; section 63 requires lineage Fair Value to Target P/E to Benchmark and Forecast EPS to Forecast Version to ReportVersion to Publication Date; section 85 (stress test) claims a report published after the valuation date is excluded from historical valuation, marked PASS. That PASS is a claim only: no enforcement mechanism exists anywhere in the Stage 7 code path.

1.5 Upstream provenance capability exists but is unwired. Verified present: `ReportVersion` with report_version_id, version_number, publication_datetime (src/models/report.py:35-42); `select_report_version` filtering on publication_datetime <= cutoff (src/core/point_in_time.py:20-25); `ForecastInputRef` carrying report_version_id, available_at, source (src/forecast/schema.py:156-166); `detect_pit_leakage(cutoff, refs)` flagging available_at after cutoff (src/evaluation/observation.py:255-273). None of it reaches Stage 7: a provenance-term grep over src/valuation returns zero matches, and `ValuationResult` carries only medians, the peer count, the passthrough cutoff, and metadata `"pit_inputs_required": True`.

1.6 Can sources supply publication timestamps and report versions? The Stage 1 and forecast layers can (fields verified above), but no wired path to Stage 7 exists and no production caller exists to carry them. Capability is present upstream; the interface is absent at the boundary.

## 2. Can Stage 7 validate PIT correctness with current inputs alone? No.

Verified facts: benchmark series arrive as undated floats with no observation dates, publication stamps, or versions; valuation_date and market_price_date are echoed, never cross-checked against the cutoff (pinned by tests); the engine output records medians, peer count, and a passthrough cutoff only; no production caller exists to attest or supply anything further. Assumptions (not relied upon): that any future caller will supply PIT-clean data; that Stage 1 publication datetimes cover every benchmark input a future caller might use; that eight valid peers implies eight PIT-clean peers. None of these is verifiable from inside Stage 7 today.

## 3. Option A: per-observation provenance records validated against the cutoff

Design: add optional parallel provenance inputs (one record per benchmark observation: observation date, publication/available-at timestamp, report version id) or a provenance envelope; the engine drops or flags observations with available_at after the cutoff and enforces a valuation-date/cutoff policy with explicit reject-or-flag semantics. Affected callers: none in production; only the test file uses the boundary today, so this is a greenfield addition — the future production caller must supply provenance assembled from existing Stage 1/forecast interfaces. Compatibility: additive optional parameters are backward compatible; making them required needs a CONTRACT_VERSION bump and new ValuationResult provenance-summary fields. Migration: none for existing callers (none exist); spec sections 56-57, 69, and 85 must define the record shape and reject/flag semantics first. Tests: late-publication observation rejected/flagged; missing available_at reported as missing-provenance (not leakage, mirroring `detect_pit_leakage`); valuation_date after cutoff rejected/flagged per policy; determinism and golden outputs unchanged. Smallest viable boundary: optional provenance params plus cutoff comparison plus one flag/alert plus tests; Stage 7 files only. Frozen Stages 1-6 need NO changes provided provenance is assembled from existing interfaces (ReportVersion, select_report_version, ForecastInputRef); if new Stage 1 query APIs prove necessary, that crosses the freeze and must be declared then.

## 4. Option B: caller attestation of PIT validity plus valuation-date/cutoff policy

Design: add an attestation input (boolean or enum plus basis string) and enforce date policy inside the engine (valuation_date and market_price_date on or before the cutoff, with a documented tolerance or rejection rule); unattested calls are flagged (e.g. PIT_UNATTESTED) or rejected per policy. Affected callers: same as Option A — none yet; the future caller must attest. Compatibility: a new optional input is backward compatible; enforcement strictness is the risk point (reject breaks, flag warns). Migration: spec amendment defining attestation semantics and the date policy; no schema break while optional. Tests: unattested call flagged; valuation_date after cutoff rejected/flagged per policy; attested path outputs byte-identical apart from the attestation record. Smallest viable boundary: one attestation parameter plus date comparisons plus one flag; no provenance plumbing, Stage 7 files only, no frozen-stage changes. Residual weakness: attestation is a claim, not verification — date checks alone cannot catch backfilled or restated values, so lookahead inside the series stays undetectable.

## 5. Option C (from P8): retain the V1 limitation, correct the spec and stress-test claims

Design: no code change. Amend sections 56-57 to state PIT safety is a caller/upstream responsibility in V1; change the section 85 PASS to NOT-APPLICABLE or documented-limitation; keep metadata `"pit_inputs_required": True` as the marker and the two pinning tests as documented-limitation pins. Guarantees that stay unavailable: per-observation publication checks; report-version correctness; valuation-date-vs-cutoff enforcement; lookahead/backfill detection in backtests — the section 85 guarantee is void and backtest PIT safety rests entirely on upstream/caller discipline. Affected callers: none. Compatibility risk: zero. Migration: zero. Tests: existing pins retained unchanged. Smallest viable boundary: spec-text edits only (out of P13 read-only scope; recorded as future work, not performed here).

## 6. Recommendation (not a selection; nothing implemented)

Option A is recommended for eventual adoption: there are no production callers so there is no migration cost (greenfield timing is the cheapest moment to add the boundary); the upstream provenance fields already exist, so the work is plumbing plus validation rather than new data capture; and it is the only option that actually closes UF-4 — Option B attests without verifying and Option C leaves every PIT guarantee unavailable. Prerequisite under any option: correct the false section 85 PASS claim and the sections 56-57 scope wording first, since the current text overstates what the code enforces. The user must still select (or reject) an option and authorize any spec or contract change separately.

## 7. Six validation layers (design-only/unavailable marked explicitly)

Cwd and interpreter as above. Fresh run: `... -m pytest src/tests/test_stage7_valuation.py -q` gives 52 collected, 50 passed, 2 failed (the same two long-standing P2 failing-first exposures as P11/P12), 0 warnings.

1. Unit/formula: EXECUTED (the 50 passes; no PIT enforcement exists to unit-test).
2. Contract/boundary: EXECUTED as static verification (signature read, provenance grep with zero matches, no-production-caller grep); no runtime PIT contract executed — DESIGN-ONLY beyond the static facts.
3. Production-path/integration: UNAVAILABLE — no production caller exists, so no benchmark-PIT integration can be executed; P6 Stage 5-forecast evidence carried, benchmark path never integrated.
4. Adversarial/negative: EXECUTED for existing guards (finite-input, rationale/bound rejections within the 50 passes); PIT-specific adversarial cases are DESIGN-ONLY proposals, not executed.
5. Regression: EXECUTED (golden values intact in the fresh run; no code touched).
6. Independent audit: EXECUTED — this read-only append; nothing claimed implemented or enforced beyond what was executed above.

## 8. Scope confirmation

Read-only assessment plus this English-only append: read the temp_report2.md tail, spec sections 3, 7-13, 56-57, 60, 63-65, 69, 85-87, engine.py, schema.py, the full Stage 7 test file, the P13 task text in stage_7_prompts.md, decision-engine cutoff passthrough, and forecast/evaluation/Stage 1 provenance interfaces via a read-only sweep; ran only the one pytest command above; changed no code; weakened no test; invented no data, dates, provenance, formulas, or thresholds; performed no commits, pushes, pulls, or branch changes; Stages 1-6 and 8-9 untouched. All earlier reports preserved. Stage 7 is NOT declared frozen. Work stops after appending the report.
========================================================
# P14 — Stage 7 Parameter-Version Registry Design (APPENDED, ENGLISH ONLY)

Date (UTC): 2026-10-12. DESIGN-ONLY task; zero source, test, specification, parameter, dependency, migration, or configuration changes. No commits, pushes, pulls, branch changes, remote, or GitHub/API operations. Stages 1-6 and 8-9 untouched. Stage 7 is NOT declared frozen. No weights, thresholds, fallback defaults, rounding rules, or dispersion methodology invented; all new design choices are labeled PROPOSAL and require approval. The dead `high_dependence_share` parameter is not wired.

## 0. Inputs inspected (read-only)

- temp_report2.md tail (P13 close, lines 1317-1322; append point verified).
- 07_Stage7_Valuation.md sections 40 (dispersion formula must be versioned), 64 (model-version gate list), 65 (parameter record fields).
- src/valuation/parameters.py (full file, 82 lines; 9 versioned entries post-P10).
- src/valuation/engine.py (method-level trace: _scenario_dispersion lines 399-406; _valuation_confidence lines 432-434; _driver_analysis lines 469-498; _alerts lines 501-535; result construction lines 201-250).
- src/valuation/schema.py (ValuationResult carries model_version and contract_version; no parameter-history fields).
- Focused tests: version/determinism pins (P6 repeat-run, P10 golden hash 1990c6393233121df4bccea381ac6539461443ea1a77f1e6e09a1cf819b71255, P12 timestamp test).
- Verified searches: `high_dependence_share` occurs only at parameters.py:73 (zero src references — dead, re-confirmed); `effective_from|parameter_version|valuation_model_parameters` occur nowhere in src/ (no record store exists).

## 1. Four-category classification (P10 17-constant inventory, verified unchanged)

(a) EXPLICITLY SPECIFIED AND VERSIONED (4): C1 SCENARIO_WEIGHTS 0.20/0.60/0.20 (Sec 22 states the prior and calls it a Model Version Parameter); C4 VALUATION_THRESHOLDS, all 7 cutoffs incl. expensive_base_upside 0.0 (Sec 35 exact table, P10 fix closed the literal gap); C5 CONFIDENCE_THRESHOLDS 90/75/60/40 (Sec 39 exact bands, Model Version Parameters); C16 MIN_INDUSTRY_PEERS 8 (Sec 10 and non-negotiable rule 6).

(b) VERSIONED BUT LACKING NUMERIC SPECIFICATION SUPPORT (5): C2 PROBABILITY_EVIDENCE_BLEND 0.25 (Sec 23-24 require family votes, no blend number); C3 SCENARIO_MULTIPLE_MAX_ABS_ADJUSTMENT 0.20 (Sec 17 bans fixed gaps, gives no bound); C6 RISK_THRESHOLDS numerics 40/0.50/-30/60/-15 (Sec 36 lists factors, no cutoffs); C7 ALERT_THRESHOLDS 0.50/40.0/1.50x3 (Sec 49 names categories, no triggers in Sec 41-53); C12 SENSITIVITY_PERTURBATION 0.10 (Sec 45 "reasonable change" and Sec 50 "relatively small" give no size).

(c) HARDCODED FORMULAS/WEIGHTS THE SPECIFICATION SAYS MUST BE VERSIONED (3): C9 confidence blend 0.40/0.20/0.20/0.20 plus benchmark 100/25 and dispersion penalty slope 50 cap 40, engine.py lines 432-434 (Sec 38 lists factors with no weights; Sec 64 lists Confidence Formula as version-gated); C10 driver-uncertainty blend 0.5/0.3/0.2, engine.py line 493 (Sec 46 lists five bases with no selection; Sec 64 lists Driver Priority Formula); C11 dispersion formula (max-min)/base, engine.py lines 399-406 (Sec 40: formula must be versioned; it is inline code, not a named parameter).

(d) DEFAULTS, ROUNDING RULES, AND NUMERICAL GUARDS WITH NO SPECIFICATION BASIS (3 + 2 legacy): C13 score fallback defaults 50/50/100 (_clamp_score call sites); C14 rounding policy (fair value round 2 and margin round 2 in models.py; forward P/E round 4, confidence round 4, impact/uncertainty/review round 4 in engine.py); C15 epsilon guards (1e-9 driver total floor; strict `>` keeps exact-0.50 dispersion silent). Separately: C8 high_dependence_share 0.60 defined-but-dead (must stay unwired until the P8-D2 dependence-share formula is decided); C17 legacy/unconsumed exports (INDUSTRY_TARGET_PE {}, SCENARIO_PE_MULTIPLIER 1.00s, calculate_nav_fair_value, signature defaults) retained for backward compatibility only.

## 2. P8 options comparison (D9 record-store decision)

| Dimension | A: in-code parameter registry | B: database-backed parameter table | C: V1 methodology fixed in code, version via MODEL_VERSION bump only |
|---|---|---|---|
| Auditability | Medium. Every value named with (model_version, parameter_name, parameter_value, effective_from, description) in parameters.py; history readable in code review and git log. No queryable audit trail. | High. Append-only table gives queryable per-version history, effective dating, and change attribution. | Low. Only MODEL_VERSION distinguishes behavior; individual value history recoverable solely from git diffs. |
| Determinism | Strong, if lookup is a pure function of (model_version, as-of date) with no wall-clock, randomness, or dict-order dependence (sorted iteration). Same guarantee as today, extended to category (c)/(d) items. | Strong at runtime only if the engine pins one row-set per run (single SELECT at run start, no mid-run re-read). Live-table reads risk non-reproducible runs when rows change between runs. | Strong. Today's property (P6/P10/P12 pins) is unchanged. |
| Compatibility | Backward compatible while defaults are unchanged: moving literals into named records with identical values keeps outputs bit-identical (P10 C4b precedent: zero-hash-diff change needed no MODEL_VERSION bump). No contract change; ValuationResult gains no required fields. | Same runtime compatibility, plus a new read dependency (DB availability) on the valuation path. Any required provenance-summary output fields would need a CONTRACT_VERSION bump. | Fully compatible (nothing changes) but freezes improvement: any future tuning of category (c)/(d) values still needs a mechanism. |
| Persistence | Git history only. No runtime durability beyond the deployed code revision. | Durable, queryable history independent of deploys. | Git history only, coarser (whole-version granularity). |
| Implementation cost | Small: Stage 7 files only (parameters.py records + engine lookup + focused tests). No shared-layer changes. | Large: migration plus table, access layer, seeding, backfill of current values with effective_from dates, and run-pinning logic. Reaches beyond Stage 7-only scope. | Zero now; cost deferred to the first tuning event, which re-opens this same decision. |
| Frozen stages / migrations | None. No Stages 1-6 or 8-9 files touched; no migration. | Migration required; if the table lives in a shared DB layer, freeze boundaries of other stages are engaged. | None. |
| Sec 65 standing | Satisfies the letter (values out of hard-code with the five-field records) at code-review granularity. | Satisfies the letter with the strongest trail. | Arguably violates Sec 65: blends, slopes, caps, and the dispersion formula stay hard-coded and no per-parameter records exist. |

PROPOSAL verdict (requires approval): adopt Option A now for categories (c) and (d) with defaults unchanged (bit-identical outputs, no MODEL_VERSION bump, P10 precedent); defer Option B until a second consumer or a cross-deploy audit query need appears; reject Option C as a permanent answer because Sec 65 explicitly requires per-parameter records, though C describes the current state honestly.

## 3. Required record fields (Sec 65) and proposed minimal schema

Sec 65 requires records with exactly: `model_version`, `parameter_name`, `parameter_value`, `effective_from`, `description`. Current gap (verified): parameters.py holds values but no `effective_from`/`description` records for any entry.

PROPOSAL minimal schema (requires approval; in-code form under Option A):

```python
@dataclass(frozen=True)
class ParameterRecord:
    model_version: str        # e.g. "STAGE7_V1"; Sec 64: old versions never overwritten
    parameter_name: str       # e.g. "confidence_blend_reliability_weight"
    parameter_value: float    # numeric value consumed by the engine
    effective_from: datetime  # UTC-aware; version becomes selectable at this instant
    description: str          # what it controls, spec basis or "engine-chosen, no spec number"

PARAMETER_REGISTRY: tuple = (...)  # append-only; historical rows never edited
```

PROPOSAL scope rule (requires approval): every category (c) literal and every category (d) default/guard/rounding precision enters the registry as a named record; category (b) entries gain `effective_from`/`description` records with descriptions honestly marked "engine-chosen, no spec number" (no retroactive spec claim); category (a) entries gain records with spec-section citations; C8 stays out of the registry entirely until P8 D2 is decided (a record must never imply a wired behavior); C17 legacy exports stay out (compatibility shims, not model parameters).

## 4. Immutability and effective-version selection (PROPOSAL; the spec defines no selection rule)

Verified facts: Sec 64 requires old versions never be overwritten; the spec defines NO rule for selecting the effective parameter version for a valuation date or cutoff — no "latest effective_from <= X" sentence exists. The engine today reads module constants at import (single implicit version STAGE7_V1 stamped on every ValuationResult). These are stated as gaps, not assumptions.

PROPOSAL immutability (requires approval): registry is a frozen tuple of frozen dataclasses; any mutation attempt raises; a startup self-check asserts append-only growth (new rows only, never edits — enforced by test, not by the type system alone); each ValuationResult records the resolved `model_version` plus the registry digest (hash over canonical record serialization) so any run is re-traceable to its exact row-set.

PROPOSAL selection rule (requires approval; explicitly NOT in the spec): `effective(row) = max over rows with (model_version == requested version AND effective_from <= as_of)` where `as_of` is itself a decision — candidates are (i) data_cutoff_datetime, (ii) valuation_date, (iii) min of the two. Unknown requested version fails closed (ValueError), never silent fallback. Until the user fixes `as_of`, historical backtests cannot be parameterized deterministically and any implementation must default to the single active version only.

## 5. PROPOSAL validation strategy (requires approval; no replacement values selected)

- Registry self-check (fail-closed at import): every engine-consumed key present for the active MODEL_VERSION; unique (model_version, parameter_name, effective_from); effective_from values UTC-aware and monotonic per (model_version, parameter_name); value types/ranges sane (weights finite, cutoffs ordered where the spec orders them, e.g. Sec 35/39 bands).
- Bit-identity gate: full-contract golden hash must equal 1990c6393233121df4bccea381ac6539461443ea1a77f1e6e09a1cf819b71255 after moving literals with unchanged defaults (P10 C4b method).

## 6. Six validation layers (runtime layers marked not executed)

1. Unit/formula: NOT EXECUTED (design-only; no registry code exists to unit-test). Proposed: per-record consumption tests (mutate-then-restore pattern per P10 test 2) for each category (c)/(d) entry; rounding-precision tests pinning round-2/round-4 behavior.
2. Contract/boundary: STATIC VERIFICATION EXECUTED (spec Sec 40/64/65 re-read; all 17 constants re-traced to engine/parameters locations above; dead-parameter and no-record-store searches executed in Sec 0). No runtime contract executed.
3. Production-path/integration: NOT EXECUTED. No production caller exists (P13 finding stands); registry pins the forecast-leg path identically once adopted.
4. Adversarial/negative: NOT EXECUTED (runtime). Proposed: unknown-model_version rejection; effective_from in the future (no eligible row) rejection; NaN/inf parameter_value rejection at registry load; duplicate-record rejection.
5. Regression: STATIC ONLY — no file changed in P14, so no regression is possible; golden-hash and Stage 9 evidence carried from P10/P11. Proposed for implementation: full 52-test rerun plus hash-identity gate (Sec 5).
6. Independent audit: EXECUTED — this read-only design; nothing claimed implemented, wired, or runtime-validated beyond the static searches and re-trace above.

## 7. Proposed future test plan (implementation-gated, nothing executed)

Unit: consumption proof per new record (category c/d). Boundary: Expensive-cutoff pair style brackets for each moved cutoff; effective_from equality edge (row eligible exactly at its instant). Immutability: FrozenInstanceError on record mutation; registry-digest stability across repeated runs. Version-selection: synthetic non-production version label proves routing selects the correct row-set (asserts routing only, no financial value invented); unknown-version and future-effective_from cases fail closed. Determinism: full-contract repeat-run equality excluding calculation_timestamp (P6/P12 method) plus registry-digest equality. Regression: all 50 currently passing tests unchanged; golden hash gate; Stage 9 suite 13/13.

## 8. Scope confirmation

Design-only: read temp_report2.md tail, spec sections 40 and 64-65, parameters.py, engine.py, schema.py, models.py rounding sites, and focused version/determinism test references; ran no pytest commands in P14; changed no source, test, spec, dependency, migration, or configuration; weakened no test; invented no weights, thresholds, defaults, rounding rules, or dispersion methodology; left high_dependence_share unwired; performed no commits, pushes, pulls, or branch changes; Stages 1-6 and 8-9 untouched. English-only append with all prior content preserved. Stage 7 is NOT declared frozen. Work stops after appending the report.
========================================================
# P15 — Post-P12 Regression Verification Report (APPENDED, ENGLISH ONLY)

Date (UTC): 2026-10-12. READ-ONLY task; zero source, test, specification, parameter, dependency, migration, or configuration changes. No repo-wide exploration. No frozen-stage edits. Cwd for all commands: D:/winprojects/analyzer. Interpreter: D:/winprojects/analyzer/.venv/Scripts/python.exe (venv; system python lacks sqlalchemy). No commits, pushes, pulls, branch changes, remote, or GitHub operations. Stage 7 is NOT declared ready to freeze. Work stops after appending the report.

## 1. P12 change and P2 tests intact (verified, not assumed)

- P12 UTC change still present: `src/valuation/engine.py:2` imports `from datetime import datetime, timezone`; `src/valuation/engine.py:212` constructs `calculation_timestamp=datetime.now(timezone.utc)`. Zero `datetime.utcnow()` occurrences remain in `src/valuation/engine.py` (grep-confirmed).
- P2 failing-first tests intact at their documented locations with unchanged bodies: `test_p2_sector_driver_decomposition_missing` (test file line 406; asserts `{"REVENUE", "NII", "NAV"} <= observed` sector-driver ranking) and `test_p2_required_flip_dependence_alerts_missing` (line 425; pins `SENSITIVITY_PERTURBATION == 0.10`, ATTRACTIVE-to-FAIR flip on a 10% EPS shock, and the five required alerts). No restore, rewrite, or weakening performed; none warranted.
- P12 test still present: `test_p12_calculation_timestamp_utc_aware_and_deterministic` (line 1159).

## 2. Fresh validation runs (exact counts)

Run A — Stage 7 file.
Command: `... -m pytest src/tests/test_stage7_valuation.py -q`
Result: collected 52, passed 50, failed 2, skipped 0, errors 0, duration ~1s.
Exact failures (identical assertion text to the P11/P12/P13 baseline):
- FAILED test_p2_sector_driver_decomposition_missing — `assert {'NAV', 'NII', 'REVENUE'} <= {'EPS', 'TARGET_PE'}`.
- FAILED test_p2_required_flip_dependence_alerts_missing — `Missing required alerts: ['ASSESSMENT_FLIP_RISK', 'HIGH_MULTIPLE_DEPENDENCE', 'HIGH_EPS_DEPENDENCE', 'MARGIN_ASSUMPTION_RISK', 'HIGH_IMPACT_HIGH_UNCERTAINTY']`.

Run B — Stage 9 consumer.
Command: `... -m pytest src/tests/test_stage9_decision.py -q`
Result: collected 13, passed 13, failed 0, skipped 0, errors 0, duration 0.61s, 52 warnings (all pre-existing out-of-scope `datetime.utcnow()` sites in decision engine/schema and Stage 9 fixtures; untouched per P12 boundaries).

Run C — full suite.
Command: `... -m pytest src/tests/ -q -rs --ignore=src/tests/test_codal_pdf_extraction.py`
Result: failed 2, passed 900, skipped 1, errors 0, duration ~144s, 1068 warnings total. A `--tb=no -rf` re-run names exactly the two Run A P2 exposures as the only failures; no other file failed. Exclusion: `src/tests/test_codal_pdf_extraction.py` ignored (requires real Codal sample PDFs unavailable in this environment; same exclusion as P6/P7/P11 — no substitute PDF used, excluded tests NOT counted as passed). The 1 skip is `src/tests/test_codal_extraction.py:307` (real Codal sample PDF not available in CI).

## 3. New-vs-baseline verdict: NO NEW FAILURES

Against the stated baseline (Stage 7: 52/50/2/0 warnings; Stage 9: 13/13; full suite: 2 failed / 899 passed / 1 skipped / 0 errors), every failure name matches and no failure is new. The single count delta is full-suite passes 899 -> 900 (+1): that is exactly the P12 timestamp test now collected in the full-suite run (the 899 baseline predates P12's +1 test; Stage 7 file count is unchanged at 52/50/2). No prior pass broke; zero errors; the skip is the documented fixture skip.

## 4. Determinism + P12 timestamp recheck

Targeted run `... -m pytest src/tests/test_stage7_valuation.py -q -k "p12 or determinism or repeat_run or golden"` -> 2 passed, 50 deselected. The P12 timestamp-awareness/determinism pin and the P6 repeat-run determinism pin both pass within the focused suite.

## 5. Warning counts (accurate)

Stage 7 file: 0 warnings (P12 cleanup holds; pre-change 98 DeprecationWarnings remain eliminated). Stage 9 file: 52 warnings (identical pre/post P12; out of scope). Full suite: 1068 warnings total (includes the Stage 9 52 plus pre-existing utcnow/fixture warnings elsewhere; none from `src/valuation/engine.py:212`).

## 6. Six validation layers (labeled separately)

1. Unit/formula: FRESHLY EXECUTED (Run A 50/52; the 2 failures assert absent required behavior and fail for the documented reasons).
2. Contract/boundary: FRESHLY EXECUTED (peer-count, determinism, severity-vocabulary, NaN/inf guards, cutoff normalization, timestamp-awareness pin re-executed among the 50 passes).
3. Production-path/integration: CARRIED FORWARD (P6 genuine Stage 5-to-Stage 7 integration evidence; P13 confirmed no production caller exists for the benchmark-PIT path — not re-executed in P15).
4. Adversarial/negative: FRESHLY EXECUTED (finite-input guards, rationale/bound rejections, invalid-EPS/price variants re-executed in Run A).
5. Regression-full-suite: FRESHLY EXECUTED (Runs A+B+C; golden values, hierarchy, probabilities, NULL rules unchanged; only delta is the +1 P12 pass).
6. Independent-audit: FRESHLY EXECUTED (this read-only append; every count above was executed in P15 except where explicitly marked carried forward).

## 7. Scope confirmation

Read-only verification plus this English-only append: read the temp_report2.md tail (P11-P14), grep-verified the P12 construction and the P2/P12 test locations, read the P2 test bodies, and ran only the pytest commands above (plus read-only greps); changed no code (no new failure proven, so no repair warranted); weakened no test; invented no data, formulas, thresholds, or semantics; performed no commits, pushes, pulls, or branch changes; Stages 1-6 and 8-9 untouched (Stage 9 read-only regression run). All earlier reports preserved. Stage 7 is NOT declared frozen and is NOT claimed ready to freeze; P11 blockers UF-1/UF-2 and all other unresolved findings stand untouched. Work stops after appending the report.
========================================================
# P16 — Stage 7 Unresolved-Decision Gate Report (APPENDED, ENGLISH ONLY)

Date (UTC): 2026-10-12. READ-ONLY gate task; zero source, test, specification, parameter, dependency, migration, or configuration changes. Cwd D:/winprojects/analyzer; interpreter D:/winprojects/analyzer/.venv/Scripts/python.exe. No commits, pushes, pulls, branch changes, remote, or GitHub operations. Stage 7 is NOT declared frozen and is NOT claimed ready to freeze. No formula, threshold, perturbation, mapping, date policy, or severity invented. The two P2 failing-first tests were not touched and still fail as required. Work stops after appending the report.

## 0. Inputs verified (read-only)

- temp_report2.md tail: P8 decision package (lines 421-673), P9 alert matrix (675-819), P10 parameterization audit (820-1005), P11 regression/unresolved register UF-1..UF-8 (1006-1166), P12 UTC cleanup (1167-1267), P13 PIT impact assessment (1268-1320), P14 registry design (1321-1408), P15 regression re-verification (1409-1460).
- Spec 07_Stage7_Valuation.md sections 39-47 (confidence labels, dispersion, sensitivity, sector chains, impact, uncertainty, review priority), 48-57 (alert engine, required names, flip/multiple/EPS/margin semantics, divergence alerts, PIT + restatement), 63-65 (auditability, model + parameter versioning), 69 (output contract), 75/77-79/84-85 (stress tests).
- src/valuation/engine.py: boundary signature (lines 57-79), flag emission (153-199), result construction (201-250), _scenario_dispersion (399-406), _valuation_status (409-419), _valuation_confidence (422-434), _driver_analysis (469-498), _alerts (501-535).
- src/valuation/parameters.py full file (82 lines): high_dependence_share = 0.60 at line 73; no effective_from/description records anywhere.
- src/valuation/schema.py full file: ValuationResult carries model_version + contract_version; no parameter-history or provenance fields.
- src/tests/test_stage7_valuation.py lines 406-465: both P2 failing-first tests present with unchanged bodies.
- Fresh P16 run: Stage 7 file 52 collected / 50 passed / 2 failed / 0 warnings (failures are exactly test_p2_sector_driver_decomposition_missing and test_p2_required_flip_dependence_alerts_missing). P12 UTC fix intact (engine.py line 2 imports timezone; line 212 uses datetime.now(timezone.utc)).
- Searches: high_dependence_share occurs only at parameters.py:73 (zero live src references — dead, re-confirmed); POOR_DATA_QUALITY occurs only at spec line 1203 (name-only, no trigger anywhere); POINT_IN_TIME_WARNING has zero src references; effective_from occurs only at spec line 1490 (field name only — no selection rule exists anywhere in the spec).

## 1. REQUIRED DECISION REGISTER

### D1. ASSESSMENT_FLIP_RISK: perturbation set, flip definition, severity

- Current evidence: spec section 50 requires the alert when a "relatively small and reasonable" assumption change flips ATTRACTIVE to FAIR or ATTRACTIVE to EXPENSIVE; stress test 77 requires it for a small margin/EPS change flipping ATTRACTIVE to FAIR and marks PASS. Engine emits nothing with this name (verified: zero src references). Pinned by test_p2_required_flip_dependence_alerts_missing, which proves a 10% EPS shock flips ATTRACTIVE to FAIR with no alert (P2/P6 evidence, still failing in the P16 fresh run).
- Exact missing decision: (a) perturbation size for "relatively small" — no number exists; (b) which assumptions to shock (EPS, margin, multiple, all drivers?); (c) shock method (one-at-a-time vs joint); (d) trigger rule (any single shock flipping status, majority, expected-upside-only?); (e) severity (INFO/WATCH/WARNING/CRITICAL unspecified); (f) whether margin shocks are in scope given D4 has no margin inputs.
- Feasible options (P8 proposals, unchanged): A — distance-to-threshold (alert when expected upside is within X points of the nearest status boundary; cheap, deterministic, but X is new and multi-assumption fragility is missed); B — one-at-a-time recomputation shocking base EPS and target P/E by SENSITIVITY_PERTURBATION (~2 extra valuations; still needs shock set/sizes/flip rule); C — joint worst-case shock (most conservative; likely over-alerts; needs correlation assumptions absent from the spec). Deferral out of V1 is explicitly allowed per P8 section 3.
- Compatibility / financial-correctness risk: any option adds a new alert string (contract-stability consideration per spec section 66, though section 69 already lists valuation_alerts as contract output); options B/C add recomputation cost; wrong shock sizes cause false fragility flags or missed fragility — a correctness risk on ATTRACTIVE assessments, the highest-stakes status.
- Recommended default: NONE RECOMMENDED. Fixing any tuple element invents a financial threshold without spec basis. The only justified gate action is user selection or explicit V1 deferral.
- Tests required after approval: flip-boundary pair (shock just below / just above the chosen size); each shock-set member proven consumed; all three shock-method variants pinned if joint; severity assertion; determinism repeat-run; full 52-test rerun with the P2 flip test greened only after spec amendment authorizes it.

### D2. HIGH_MULTIPLE_DEPENDENCE: multiple-dependence share definition + threshold usage

- Current evidence: spec section 51 requires the alert when fair value depends excessively on target P/E rather than EPS growth (example: near-stable EPS with the bull case built on very high P/E expansion); stress test 78 marks PASS. Engine emits nothing with this name. high_dependence_share = 0.60 sits at parameters.py line 73 with zero live src references (re-confirmed P16) — defined-but-dead. No dependence-share formula exists anywhere in spec or code.
- Exact missing decision: (a) the dependence-share formula splitting fair value into EPS share vs multiple share; (b) the role of the dead 0.60 (trigger value? share of what?); (c) scope (bull case only, all scenarios, or base?); (d) severity.
- Feasible options (P8, unchanged): A — counterfactual decomposition (recompute bull FV at the base multiple; multiple_share = (bull_FV - bull_EPS x base_multiple) / bull_FV; alert above a threshold; undefined when EPS invalid — must be NOT_APPLICABLE, not zero); B — elasticity ratio (compare percent FV change from multiple shock vs EPS shock; alert if multiple elasticity dominates by factor K; reuses perturbation machinery but needs K and shock sizes). Deferral out of V1 allowed.
- Compatibility / financial-correctness risk: wiring 0.60 without a formula invents semantics for a dead number; wrong share formula misattributes growth-vs-multiple economics — the core bull-case integrity question.
- Recommended default: NONE RECOMMENDED. The 0.60 must stay unwired (P14 instruction stands) until the formula is decided; a record must never imply a wired behavior.
- Tests required after approval: share-formula unit tests incl. invalid-EPS NOT_APPLICABLE path; threshold-boundary pair bracketing the confirmed (or replaced) 0.60; scope tests per chosen case coverage; full rerun with the P2 dependence assertion greened only after spec amendment.

### D3. HIGH_EPS_DEPENDENCE: EPS-dependence measure + interaction with D2

- Current evidence: spec section 52 requires the alert when valuation is mainly sensitive to forecast EPS, with severity allowed to rise when forecast reliability is low; stress test 79 requires HIGH_EPS_DEPENDENCE or FORECAST_RISK (FORECAST_RISK occurs at spec line 1828 only — used NOWHERE in code or tests, per P9 row 14) and marks PASS. Engine emits neither name. No EPS-share formula, no escalation rule, no D2/D3 precedence exists.
- Exact missing decision: (a) the EPS-share formula (mirror of D2 or standalone); (b) the low-reliability severity escalation rule (how many steps, at what reliability cutoff — the engine's 40.0 cutoff is engine-chosen, not spec-stated); (c) D2/D3 interaction when both shares are high (both alerts, or the larger one only?).
- Feasible options (P8, unchanged): A — EPS_share = 1 - multiple_share from D2's formula with one-severity escalation below the low-reliability cutoff (consistent with D2 but inherits all D2 decisions plus the escalation matrix); B — standalone elasticity trigger independent of D2 (D2 and D3 could fire together; needs a documented precedence rule). Deferral allowed.
- Compatibility / financial-correctness risk: DEPENDENT ON D2 under option A (cannot be fixed before the D2 share formula); under option B it is independent but then the precedence rule becomes mandatory to avoid double-alert confusion. Escalation tied to the engine-chosen 40.0 without spec basis risks false severity inflation.
- Recommended default: NONE RECOMMENDED. No escalation matrix or precedence may be assumed.
- Tests required after approval: mirror-formula consistency test (shares sum to 1 where defined); escalation-boundary tests at the chosen reliability cutoff; both-high precedence test; full rerun.

### D4. MARGIN_ASSUMPTION_RISK: required inputs + trigger definition

- Current evidence: spec section 53 requires the alert when fair value depends strongly on operating/net margin forecasts. Engine emits nothing with this name. Structural gap (P8, unchanged): Stage 7 inputs contain EPS but no margin series — calculate_valuation accepts no margin input, so no formula can run without an input-contract change.
- Exact missing decision: (a) expand the input contract (Stage 5 supplies margin assumptions) OR accept a labeled EPS-shock proxy OR defer the alert with section 53 out of V1; (b) if expanded: dependence measure, margin-perturbation size, threshold, severity.
- Feasible options (P8, unchanged): A — contract expansion with one-at-a-time margin shocks (correct economics; largest scope — upstream contract change, frozen-stage boundary engagement); B — EPS-shock proxy labeled margin-blind (no contract change; economically weak; risks false precision; must be labeled proxy, not margin test). Strongest deferral candidate in the package (P8).
- Compatibility / financial-correctness risk: option A needs a CONTRACT_VERSION bump and new required fields; option B risks presenting non-margin analysis as margin analysis — a financial-honesty risk that must be mitigated by explicit labeling if ever chosen.
- Recommended default: NONE RECOMMENDED (no proxy semantics adopted without user authorization).
- Tests required after approval: under A — margin-input plumbing tests, shock-consumption proof, boundary pair, missing-margin handling; under B — proxy-label assertion tests proving the output discloses its limitation; full rerun.

### D5. HIGH_IMPACT_HIGH_UNCERTAINTY: impact/uncertainty formulas, inputs, thresholds

- Current evidence: spec section 49 requires the alert name; section 45 defines Driver Impact only as the FV change from a "reasonable" driver change (no formula, sizes, or normalization); section 46 lists five possible uncertainty bases (Forecast Error, Historical Volatility, Scenario Range, Data Quality, Model Stability) with no selection or weighting; section 47 states Review Priority is approximately Impact x Uncertainty and explicitly defers the exact formula and normalization to a model-version parameter that does not exist. Engine computes impact_pct/uncertainty/review_priority only over {EPS, TARGET_PE} via the FV-identity one-at-a-time 10% shocks with the 0.5/0.3/0.2 uncertainty blend (engine.py 469-498) — implemented mechanics, but the conjunction cutoffs for "high" impact and "high" uncertainty do not exist, so the alert is never emitted.
- Exact missing decision: (a) impact formula with per-driver shock sizes; (b) uncertainty estimation formula (which bases, what weights); (c) the conjunction cutoffs (what counts as high impact AND high uncertainty); (d) whether coverage stays {EPS, TARGET_PE} or waits for D6 sector drivers.
- Feasible options (P8, unchanged): A — minimal (reuse existing 10% identity shocks + current reliability/probability/quality blend + fixed cutoffs; implementable immediately, but cutoffs are still new decisions and only {EPS, TARGET_PE} covered until D6); B — full per-driver framework after D6 mapping (complete but blocked behind D6).
- Compatibility / financial-correctness risk: option A bakes the engine-chosen 10% and 0.5/0.3/0.2 into alert semantics without spec basis; option B is DEPENDENT ON D6. Invented cutoffs cause false review-priority flags either way.
- Recommended default: NONE RECOMMENDED.
- Tests required after approval: impact-formula unit tests per driver; uncertainty-base selection tests; conjunction-boundary matrix (high/low x high/low); coverage tests for any post-D6 drivers; full rerun.

### D6. Sector-specific drivers (non-financials, banks, holdings) incl. missing industry mapping + NAV/P-NAV contract

- Current evidence: spec sections 42-44 give causal chains (Revenue chain; Loans/Deposits to NII/NIM chain; NAV to NAV-growth chain) and section 44 states P/NAV analysis belongs to Stage 7; spec section 69 requires valuation_driver_ranking, driver_impact, driver_uncertainty, review_priority in the output contract. Engine evidence (P16 re-verified): _driver_analysis (engine.py 469-498) hardcodes exactly two drivers {EPS, TARGET_PE}; industry_code is accepted but only echoed to metadata (line 233), never branched on; nav_per_share is accepted but only echoed to metadata as nav_per_share_received (line 247), never consumed in any formula. Pinned by test_p2_sector_driver_decomposition_missing (requires {REVENUE, NII, NAV} in the union ranking; observed ranking is always {EPS, TARGET_PE}).
- Exact missing decision: (a) industry_code-to-driver-set mapping (which codes count as bank/holding?); (b) driver-to-EPS linkage formulas; (c) per-driver perturbation sizes; (d) how NAV enters fair value — no P/NAV formula exists anywhere (section 44 assigns P/NAV to Stage 7 but gives no formula); (e) whether ranking labels may imply sector analysis not performed.
- Feasible options (P8, unchanged): A — identity decomposition (each chain link a multiplicative/additive identity with its own shock; needs per-link data — large contract expansion comparable to D4); B — sector-labeled attribution (keep EPS-identity shocks, attribute through sector templates for ranking labels only; small change but thin economics — labels would imply analysis not performed and must be disclosed as such). Deferral of sections 42-44 with the P/NAV claim to V2 (ranking stays {EPS, TARGET_PE}) allowed.
- Compatibility / financial-correctness risk: option A needs new required inputs (CONTRACT_VERSION bump); option B risks false-precision labeling. D5-option-B is DEPENDENT ON D6; D1-margin-shock scope interacts with D4/D6 input availability.
- Recommended default: NONE RECOMMENDED.
- Tests required after approval: mapping tests per industry code incl. unknown-code handling; linkage-formula unit tests; NAV/P-NAV formula tests with boundary cases; ranking-content tests greening the P2 sector test only after spec amendment; full rerun.

### D7. PIT correctness: per-observation provenance vs caller attestation vs documented V1 limitation

- Current evidence: spec sections 56-57 and 8 require per-observation price date, forecast cutoff, publication date, version, and availability; future-published reports are banned from backtests; section 85 stress test claims a report published after the valuation date is excluded and marks PASS. Engine facts (P16 re-verified): benchmark series arrive as undated float lists (no dates, publication stamps, or versions accepted or stored); valuation_date, market_price_date, data_cutoff_datetime are normalized via normalize_datetime, echoed to ValuationResult, never compared against each other; metadata pit_inputs_required=True is a claim flag, not enforcement; a valuation_date later than data_cutoff_datetime is accepted silently (pinned by test_p6_cutoff_pit_limitation_pinned). P13 caller trace (verified, stands): NO production caller supplies any of the six PIT-relevant inputs — grep matches only engine.py (definition) and the test file (33 hits); the only downstream consumer (src/decision/engine.py:250) passes data_cutoff_datetime through without validation. Upstream provenance capability exists but is unwired (ReportVersion, select_report_version, ForecastInputRef, detect_pit_leakage — zero provenance-term matches in src/valuation).
- Exact missing decision: choose A (per-value provenance structs with validation — reject or flag future-dated observations; strongest guarantee; contract change for every benchmark caller incl. upstream stages), B (caller attestation plus ordering check — flag when valuation_date exceeds cutoff by more than a tolerance; small change; trust-based; needs the tolerance decision; date checks alone cannot catch backfilled/restated values), or C (documented limitation — no code change; sections 56-57 amended to caller/upstream responsibility; section 85 PASS corrected to NOT-APPLICABLE/documented-limitation).
- Feasible options: P8/P13 A/B/C as above; P13 recommends A for eventual adoption (greenfield timing — no production callers so no migration cost; upstream fields already exist so the work is plumbing plus validation; only option that closes UF-4) but records it as NOT a selection.
- Compatibility / financial-correctness risk: option A is a contract change (new optional params backward compatible; required params need CONTRACT_VERSION bump); option B enforcement strictness is the risk point (reject breaks, flag warns); option C leaves every PIT guarantee unavailable — backtest PIT safety rests entirely on upstream/caller discipline. Under ANY option the false section 85 PASS claim and sections 56-57 scope wording must be corrected first (documentation correction required regardless).
- Recommended default: NONE SELECTED. The P13 recommendation of A is noted as a proposal, not an approved decision.
- Tests required after approval: under A — late-publication observation rejected/flagged; missing available_at reported as missing-provenance (not leakage, mirroring detect_pit_leakage); valuation_date-after-cutoff rejected/flagged per policy; determinism + golden outputs unchanged. Under B — unattested call flagged (e.g. PIT_UNATTESTED); date-policy boundary tests; attested path byte-identical apart from attestation record. Under C — existing pins retained unchanged as documented-limitation pins. Full rerun in all cases.

### D8. Alert-name mismatches (sections 49 vs 54-55 vs emitted names)

- Current evidence (P9 matrix, re-confirmed P16): section 49 requires VALUATION_BENCHMARK_DIVERGENCE (emitted: WATCH:VALUATION_ABOVE/BELOW_TARGET_PE — MISMATCH, closest functional analogue at ratio >= 1.50 either direction, direction split preserved); sections 54-55 use HISTORICAL_VALUATION_DIVERGENCE / INDUSTRY_VALUATION_DIVERGENCE (emitted: WATCH:FORWARD_PE_ABOVE/BELOW_HISTORICAL and WATCH:FORWARD_PE_ABOVE/BELOW_INDUSTRY — MISMATCH); section 10 ties INDUSTRY_BENCHMARK_INSUFFICIENT to < 8 valid peers but the engine emits it only when target_source == INSUFFICIENT_DATA (MISMATCH of trigger narrowing: with 7 forward peers + valid historical median, engine emits INSUFFICIENT_PEER_DATA but NOT this flag); INSUFFICIENT_PEER_DATA / NEGATIVE_EPS / SIGN_CHANGE emitted as risk flags only, not severity-prefixed alerts (GAP of representation — open whether flag-level emission satisfies the section 49 "alert capability"); POOR_DATA_QUALITY has NO trigger definition anywhere (spec name-only at line 1203; zero src references); POINT_IN_TIME_WARNING has NO trigger (zero src references; needs the D7 contract choice); FORECAST_RISK (stress 79 alternative name) is used NOWHERE in code or tests.
- Exact missing decision — naming changes (decide now, no formula needed): (a) mapping for rows 3-5: rename to spec names (P8-A: breaking for consumers parsing current names; collapses directional above/below signals) vs alias both with spec names canonical (P8-B: dual vocabulary must be versioned and retired) vs amend the spec to adopt engine names (P8-C: needs locked-spec governance approval); (b) whether flag-level emission satisfies section 49 for INSUFFICIENT_PEER_DATA / NEGATIVE_EPS / SIGN_CHANGE (and which severities if promoted); (c) row 11 trigger (section-10 letter vs current fallback-gated emission). Missing trigger semantics (NOT naming changes — must not be decided by renaming): POOR_DATA_QUALITY and POINT_IN_TIME_WARNING triggers (define or defer with the section 49 capability claim corrected).
- Compatibility / financial-correctness risk: any rename is a breaking public-output change under section 66 contract stability (P9 found no parser in src/decision or src/market, but contract stability still applies); collapsing direction splits loses economically opposite signals; promoting flags duplicates vocabulary across both channels with spec-undefined severities.
- Recommended default: NONE SELECTED for the mapping choice. P8 notes it should be decided now (naming, not formula) — recorded as requiring user decision, not defaulted.
- Tests required after approval: rename/alias mapping tests pinning every emitted string old and new; direction-preservation tests; flag-vs-alert channel tests; row-11 trigger tests for both 7-peer and no-series cases; full rerun.

### D9. Parameter registry + effective-version selection: P14 in-code proposal vs DB-backed vs fixed V1

- Current evidence: spec section 64 lists version-gated methods (Target P/E, Scenario Probability, Priors, Valuation Thresholds, Confidence/Risk/Sensitivity/Alert/Driver-Priority formulas) and requires old versions never be overwritten; section 65 requires tunable thresholds outside hard-code with (model_version, parameter_name, parameter_value, effective_from, description) records. Engine facts (P16 re-verified): parameters.py holds values but NO effective_from/description records for any entry; the engine reads module constants at import with single implicit version STAGE7_V1 stamped on every ValuationResult. P10 classified 17 constants: 9 versioned (C1-C7, C12, C16), 6 hardcoded/unversioned (C9-C15), 2 dead/legacy (C8, C17); exactly one spec-explicit literal was corrected (C4b). The spec defines NO rule for selecting the effective parameter version for a valuation date or cutoff — no "latest effective_from <= X" sentence exists (P16 verified: effective_from occurs only at spec line 1490 as a field name).
- Exact missing decision: (a) record-store mechanism — A: in-code parameter registry (P14 proposal: frozen tuple of frozen ParameterRecord dataclasses, startup self-check, registry digest on each ValuationResult; bit-identical outputs, no MODEL_VERSION bump per P10 precedent; satisfies Sec 65 at code-review granularity) vs B: DB-backed parameter table (queryable audit trail; needs migration, seeding, run-pinning; reaches beyond Stage 7 scope) vs C: fixed V1 methodology with MODEL_VERSION bump only (zero cost now; arguably violates Sec 65 — describes current state honestly but is not a permanent answer); (b) scope confirmation (blends/slopes/caps/dispersion formula as tunable; category b entries marked "engine-chosen, no spec number" — no retroactive spec claim; C8 stays out until D2; C17 legacy stays out); (c) the as_of rule for effective_from selection — candidates (i) data_cutoff_datetime, (ii) valuation_date, (iii) min of the two — with unknown-version fail-closed semantics.
- Compatibility / financial-correctness risk: A is backward compatible while defaults unchanged; B adds a DB read dependency on the valuation path (live-table reads risk non-reproducible runs without run-pinning); C freezes improvement. Until as_of is fixed, historical backtests cannot be parameterized deterministically — any implementation must default to the single active version only.
- Recommended default: NONE SELECTED. P14 PROPOSAL verdict (adopt A now, defer B, reject C as permanent) is noted as requiring approval, not an approved decision.
- Tests required after approval: registry self-check tests (presence, uniqueness, UTC-aware monotonic effective_from, sane ranges); bit-identity gate (golden hash 1990c6393233121df4bccea381ac6539461443ea1a77f1e6e09a1cf819b71255); per-record consumption tests (mutate-then-restore); immutability tests (FrozenInstanceError, digest stability); version-selection routing tests with synthetic labels; unknown-version and future-effective_from fail-closed tests; full rerun.

## 2. DECISION INTEGRITY

- Nothing chosen for the user: every D1-D9 entry above records options as PROPOSAL (P8/P13/P14 provenance) and states no recommended default except where explicitly marked NONE SELECTED / NONE RECOMMENDED. No formula, threshold, perturbation, mapping, date policy, severity, or as_of rule is fixed in this report.
- Independent vs dependent decisions: INDEPENDENT — D1 (own shock tuple), D4 (own contract choice), D8-naming (rename/alias/amend needs no formula), D9-mechanism (registry shape separable from as_of). DEPENDENT — D3 on D2 under option A (mirror formula); D5-option-B on D6 (per-driver framework); D9 as_of rule blocks any multi-version backtest use; D8 POINT_IN_TIME_WARNING trigger on D7; D1-margin-shock scope on D4/D6 inputs. No dependent decision may be implemented before its prerequisite.
- Proposal vs approved decision: P8 A/B/C option sets, the P13 option-A recommendation, and the P14 adopt-A/defer-B/reject-C verdict are all PROPOSALS requiring user approval. The only approved-state facts in this gate are negative: the two P2 tests still fail as required; high_dependence_share stays unwired; no registry code exists; no PIT enforcement exists.
- The two failing-first tests were not touched, weakened, or re-scoped. Deferred requirements must be removed from test expectations by spec amendment first, never by editing tests to pass (P8 section 3 rule, preserved).

## 3. OVERSTATED SPEC / STRESS-TEST PASS CLAIMS FLAGGED

Each claim below is marked PASS in the spec but has no implementing mechanism in code (verified P16); each requires a documentation correction unless its decision is implemented:

1. Stress test 77 PASS (ASSESSMENT_FLIP_RISK on small margin/EPS flip) — no perturbation set, flip rule, or severity exists; engine emits nothing. Overstates implemented behavior.
2. Stress test 78 PASS (HIGH_MULTIPLE_DEPENDENCE) — no share formula; 0.60 dead. Overstates.
3. Stress test 79 PASS (HIGH_EPS_DEPENDENCE or FORECAST_RISK) — no formula, no escalation, no precedence; FORECAST_RISK exists nowhere in code or tests. Overstates.
4. Stress test 85 PASS (post-valuation-date report excluded) — no provenance inputs, no date comparison, no enforcement; future-dated acceptance pinned by passing test. False PASS; must be corrected first under any D7 option.
5. Section 49 capability list as a whole — five of thirteen names (D1-D5 family) plus POOR_DATA_QUALITY and POINT_IN_TIME_WARNING have no trigger; flag-level emission for INSUFFICIENT_PEER_DATA / NEGATIVE_EPS / SIGN_CHANGE leaves the "alert capability" question open (D8). The list over-claims until triggers or deferrals with corrected claims are recorded.
6. Sections 42-44 + P/NAV assignment — chains stated without mapping, linkage, perturbation, or P/NAV formula; ranking always {EPS, TARGET_PE}. Over-claims sector analysis until D6 or V2 deferral.
7. Section 47 formula deferral — "exact formula and normalization" deferred to a model-version parameter that does not exist (no registry, no records). The deferral target itself is undecided (D9).
8. Sections 56-57 PIT scope wording — requires per-observation dates/versions the boundary cannot accept; no production caller supplies them. Overstates unless D7-A/B implementation or D7-C limitation wording is adopted.

## 4. SIX VALIDATION LAYERS (executed vs design-only, labeled separately)

Cwd D:/winprojects/analyzer; interpreter .venv/Scripts/python.exe. Fresh P16 run: src/tests/test_stage7_valuation.py 52 collected / 50 passed / 2 failed / 0 warnings. Stage 9 and full-suite counts below are carried from P15 (not re-executed in P16); P12 UTC fix re-verified by read (import + construction) rather than by rerun.

1. Unit/formula: FRESHLY EXECUTED (P16 Stage 7 run 50/52; the 2 failures assert absent required behavior and fail for the documented reasons; no flip/dependence/margin/sector/PIT unit exists to execute — design-only beyond the absence pins).
2. Contract/boundary: FRESHLY EXECUTED as static verification (boundary signature re-read; provenance grep zero matches; no-production-caller grep; P2 test bodies re-read; P12 construction re-read) plus the 50 passing boundary pins (peer-count, determinism, severity, divergence, cutoff, timestamp-awareness) re-executed in the fresh run. No runtime PIT/registry contract executed — design-only.
3. Production-path/integration: NOT EXECUTED in P16 — carried from P6 (genuine Stage 5-to-Stage 7 forecast-leg integration) with the P13/P15 standing qualification (no production caller exists for the benchmark-PIT path; benchmark leg fixture-based by V1 design).
4. Adversarial/negative: FRESHLY EXECUTED for existing guards (finite-input, rationale/bound rejections, invalid-EPS/price variants within the 50 passes). PIT-specific, registry-specific, and flip/shock adversarial cases are DESIGN-ONLY proposals, not executed.
5. Regression/full-suite: PARTIAL — Stage 7 file freshly executed (50/52, P12 fix intact, 0 warnings); Stage 9 13/13 and full-suite 2 failed / 900 passed / 1 skipped carried from P15 (not re-executed in P16). No code changed in P16, so no new regression is possible.
6. Independent audit: FRESHLY EXECUTED — this read-only gate; every D1-D9 evidence line above was re-verified against spec/code/tests in P16 except where explicitly marked carried forward. Nothing claimed implemented, wired, or runtime-validated beyond the fresh Stage 7 run and the static re-verification.

## 5. FINAL DECISION TABLE

| ID | Decision | Verdict |
|---|---|---|
| D1 | ASSESSMENT_FLIP_RISK (shock set, sizes, method, flip rule, severity) | REQUIRES USER DECISION |
| D2 | HIGH_MULTIPLE_DEPENDENCE (share formula, 0.60 role, scope, severity) | REQUIRES USER DECISION |
| D3 | HIGH_EPS_DEPENDENCE (share formula, escalation, D2/D3 precedence) | DEPENDENT ON ANOTHER DECISION (D2 under mirror option; precedence mandatory under standalone option) |
| D4 | MARGIN_ASSUMPTION_RISK (contract expansion vs labeled proxy vs deferral) | REQUIRES USER DECISION |
| D5 | HIGH_IMPACT_HIGH_UNCERTAINTY (impact/uncertainty formulas, cutoffs, coverage) | REQUIRES USER DECISION (full-framework option DEPENDENT ON D6) |
| D6 | Sector drivers + industry mapping + NAV/P-NAV contract | REQUIRES USER DECISION |
| D7 | PIT correctness (provenance vs attestation vs documented limitation) | REQUIRES USER DECISION (option C is a DOCUMENTATION CORRECTION; under all options the Sec 85 PASS + Sec 56-57 wording corrections are DOCUMENTATION CORRECTION REQUIRED) |
| D8 | Alert-name mapping (rename vs alias vs spec amendment; flag-vs-alert capability; row-11 trigger) | REQUIRES USER DECISION (naming part decide-now; POOR_DATA_QUALITY + POINT_IN_TIME_WARNING triggers: define or defer with DOCUMENTATION CORRECTION REQUIRED to Sec 49 capability claim) |
| D9 | Parameter registry mechanism + scope + as_of selection rule | REQUIRES USER DECISION (P14 Option A is a proposal, not approved; as_of rule unresolved blocks multi-version backtests) |
| — | Stress-test PASS claims 77/78/79/85 + Sec 45-47/49/51-53/56-57 scope wording | DOCUMENTATION CORRECTION REQUIRED unless the corresponding decision is implemented first |

## 6. Scope confirmation

Read-only gate plus this English-only append: read the temp_report2.md tail (P8-P15), spec sections 39-65/69/75/77-79/84-85/10/60-62, engine.py (signature, flags, dispersion, status, confidence, driver analysis, alerts, result construction), parameters.py (full), schema.py (full), and the P2 test bodies; ran only the Stage 7 pytest command above plus read-only greps; verified the P12 UTC construction by read; changed no source, test, spec, dependency, migration, or configuration; weakened no test; invented no formula, threshold, perturbation, mapping, date policy, or severity; performed no commits, pushes, pulls, or branch changes; Stages 1-6 and 8-9 untouched. All prior content preserved. Stage 7 is NOT frozen and is NOT claimed ready to freeze; P11 blockers UF-1/UF-2 and all other unresolved findings stand untouched. Work stops after appending the report.
===========================================================================

# P17 — Stage 7 Specification Correction Draft Report (English edition)

**Date (UTC):** 2026-10-13
**Nature:** READ-ONLY — no source, test, spec, dependency, migration, or configuration file was modified; no test was executed; no D1-D9 decision was chosen. The Persian edition above is preserved verbatim; this English edition is an additive append, not a replacement.
**Inputs reviewed:** `temp_report2.md` (P11-P16); spec `07_Stage7_Valuation.md` (sections 42-57, 64-65, 69, stress tests 77-79 and 85); `src/valuation/engine.py` (full, 535 lines); `src/valuation/schema.py` (full); `src/valuation/parameters.py` (full); `src/tests/test_stage7_valuation.py` (the two P2 test bodies, lines 406-464).
**Static checks performed:** search for the eight mandatory alert names across `src/valuation` (zero hits); search for `high_dependence_share` across all of `src` (single hit: a dead definition at `parameters.py:73`); search for `FORECAST_RISK|UNRELIABLE_VALUATION|effective_from` across `src` (zero hits for all three; `calculate_nav_fair_value` exists in `models.py`/`__init__.py` only as an unwired export).

---

## A) Effectively mandatory corrections (factual corrections — require no user decision)

### C-01 — Stress test 77 PASS claim (spec line 1801)
- **Identifier:** section 77 (Assessment Flip) versus section 50.
- **Evidence:** `_alerts` (engine.py:501-535) emits no `ASSESSMENT_FLIP_RISK` output (zero hits in all of `src/valuation`). `test_p2_required_flip_dependence_alerts_missing` (line 425) demonstrates that a 10% EPS shock moves the status from ATTRACTIVE to FAIR with no alert raised.
- **Replacement wording:** "V1 status: NOT IMPLEMENTED — decision D1 remains open; the PASS claim is invalid until the formula is implemented or the requirement is explicitly deferred."
- **Class:** pure factual correction of a claim (neither a deferral nor a narrowing of a guarantee).
- **Consequence:** no code effect; prevents false assurance that brittleness in ATTRACTIVE ratings is being detected — the highest-risk rating from a financial-decision standpoint.

### C-02 — Stress test 78 PASS claim (spec line 1815)
- **Identifier:** section 78 (Multiple Risk) versus section 51.
- **Evidence:** no dependence-share formula exists in spec or code; `high_dependence_share = 0.60` (parameters.py:73) is a dead definition (single hit across `src`, confirmed).
- **Replacement wording:** "V1 status: NOT IMPLEMENTED — decision D2 remains open (the role of the 0.60 threshold is undefined); the PASS claim is invalid."
- **Class:** pure factual correction. **Consequence:** no code effect.

### C-03 — Stress test 79 PASS claim (spec line 1831), plus the FORECAST_RISK alias name
- **Identifier:** section 79 (Forecast Risk) versus section 52.
- **Evidence:** no EPS-share formula, no severity-escalation rule, no D2/D3 precedence rule exist; the name `FORECAST_RISK` (spec line 1828) appears in no production or test file (zero hits across `src`).
- **Replacement wording:** "V1 status: NOT IMPLEMENTED — decision D3 remains open; the name FORECAST_RISK has no definition and no consumer and must be removed from the acceptable result or defined; the PASS claim is invalid."
- **Class:** pure factual correction. **Consequence:** no code effect; prevents reliance on a name defined nowhere.

### C-04 — Stress test 85 PASS claim (spec line 1909)
- **Identifier:** section 85 (Point-in-Time) versus sections 56-57.
- **Evidence:** benchmark series enter as bare floats with no dates (`calculate_valuation` signature, engine.py:70-72); no comparison between `valuation_date` and `data_cutoff_datetime` is performed (engine.py:104-108 only normalizes and echoes); `metadata["pit_inputs_required"] = True` (line 248) is a metadata claim, not an enforcement; `test_p6_cutoff_pit_limitation_pinned` pins the silent acceptance of a post-cutoff date.
- **Replacement wording:** "Not achievable in V1 — NOT-APPLICABLE / documented limitation; pending decision D7. PIT safety of backtests in V1 is solely the responsibility of the caller/upstream."
- **Class:** pure factual correction — and under all three D7 options this correction is preliminary and mandatory.
- **Financial consequence:** the most consequential creditability finding in this report — any backtest relying on the section 85 PASS ignores lookahead risk from revised/late-published reports.

### C-05 — Section 49 capability list (spec lines 1191-1207)
- **Identifier:** section 49 versus `_alerts` and the engine.py:161-169 flags.
- **Evidence:** of the 13 names, the five sensitivity-family names (D1-D5) have no mechanism at all; `POOR_DATA_QUALITY` is a name only (spec line 1203 — zero trigger definition anywhere in the spec, zero references in code); `POINT_IN_TIME_WARNING` has zero code references and its trigger is tied to decision D7; three names (`INSUFFICIENT_PEER_DATA`/`NEGATIVE_EPS`/`SIGN_CHANGE`) are emitted only at flag level (engine.py:164-165, 364-371), leaving open whether they satisfy the section 49 "Alert capability" (part of decision D8).
- **Replacement wording:** annotate every list entry with "implemented / flag-level / absent (decision reference)" — without renaming anything.
- **Class:** factual correction (recording current state); the naming portion is tied to the D8 choice (section B).
- **Compatibility consequence:** any rename changes public output under the section 66 contract-stability guarantee.

### C-06 — Sections 42-44 and the P/NAV sentence in section 44 (spec line 1106)
- **Identifier:** sections 42-44 ("P/NAV is Valuation analysis and belongs to Stage 7") versus `_driver_analysis` (engine.py:469-498).
- **Evidence:** the driver analysis hardcodes exactly two drivers `{EPS, TARGET_PE}`; `industry_code` is only echoed in metadata (line 233) with no branching on it; `nav_per_share` only sits in metadata as `nav_per_share_received` (line 247) and is consumed by no formula; `calculate_nav_fair_value` exists in `models.py` but is unwired (export only in `__init__.py`). `test_p2_sector_driver_decomposition_missing` (line 406) fails.
- **Replacement wording:** "Sector driver chains (42-44) are not implemented in V1 (decision D6 remains open); the driver ranking is always {EPS, TARGET_PE}; P/NAV analysis is deferred to V2 unless D6 is implemented."
- **Class:** factual correction plus the D6 deferral in section B.
- **Financial consequence:** prevents the impression that genuine sector analysis was performed (false-precision risk in driver ranking, which is the section 69 contractual output).

### C-07 — Section 47 references a non-existent parameter (spec line 1156)
- **Identifier:** section 47 ("the exact formula and Normalization must be a Model Version Parameter").
- **Evidence:** no such parameter exists — `effective_from`/`parameter_version` have zero hits across `src`; no record store exists.
- **Replacement wording:** add the sentence "This parameter does not exist in V1 (decision D9 remains open); until then the formula is the fixed engine implementation."
- **Class:** pure factual correction (prevents a reference to a non-existent entity). **Consequence:** reproducibility and audit transparency.

### C-08 — Scope of sections 56-57 (spec lines 1317-1353)
- **Identifier:** the requirement for "Price Date, Forecast Cutoff, Report Publication Date, Report Version" versus the actual Stage 7 input boundary.
- **Evidence:** the `calculate_valuation` signature (engine.py:57-79) accepts no observed-provenance fields; no production caller exists for the six PIT-related inputs (finding P13, still standing).
- **Replacement wording (D7-C text):** "In V1 PIT safety is the caller's/upstream's responsibility; section 85 is NOT-APPLICABLE."
- **Class:** conditional factual correction — if D7-A/B is chosen, a new contract replaces this sentence instead (section B). **Consequence:** same as C-04.

### C-09 — Recording name mismatches (mandatory factual part; the mapping choice belongs to the user)
- **Identifiers:** section 49 (`VALUATION_BENCHMARK_DIVERGENCE`, line 1197) versus `WATCH:VALUATION_ABOVE/BELOW_TARGET_PE` (engine.py:519-522); sections 54-55 (`HISTORICAL/INDUSTRY_VALUATION_DIVERGENCE`, lines 1294 and 1308) versus `WATCH:FORWARD_PE_ABOVE/BELOW_HISTORICAL/INDUSTRY` (engine.py:524-532); the `INDUSTRY_BENCHMARK_INSUFFICIENT` trigger in section 10 ("fewer than 8 valid peers") versus the current emission condition `target_source == "INSUFFICIENT_DATA"` (engine.py:168-169 — with 7 peers plus a valid historical median, this flag is not emitted and only `INSUFFICIENT_PEER_DATA` appears).
- **Mandatory part:** record exactly these mismatches in the spec text (a mapping table of current names versus mandated names) — no code change.
- **Decision part (D8, section B):** rename versus alias versus spec amendment; and whether flag-level emission suffices for the section 49 capability.
- **Compatibility consequence:** a rename breaks any consumer parsing the current names (section 66); merging the above/below pair destroys two signals with opposing economics; promoting flags duplicates vocabulary across two channels with no defined severity.

### C-10 — Conditional note on section 65 (it is a requirement, not a behavior claim — no text fix needed unless ...)
- **Identifier:** section 65 (five-field records) versus `parameters.py` (values without `effective_from`/`description`).
- **Evidence:** no record store exists. Because section 65 is a requirement rather than a behavior claim, it is not an overstatement and its text stands — **unless** D9-C (fixed-implementation V1 approach) is chosen, in which case section 65 needs correction (moved to section B).

### C-11 — Thresholds 40.0/0.50/1.50 (pinned in tests, absent from the spec)
- **Identifier:** sections 41-53 contain no trigger values; the engine uses versioned `ALERT_THRESHOLDS`/`RISK_THRESHOLDS`.
- **Evidence:** finding P2-8 stands — boundary tests pin current behavior, not spec conformance.
- **Class:** a user decision (not a mandatory correction): either ratify the numbers in the spec or annotate them as "engine-chosen values with no spec backing."

### Items requiring no correction (full coverage of the requested topics)
- `industry_peer_count` in section 69: closed by P4 and present at `schema.py:38` — no correction needed.
- `HIGH_SCENARIO_DISPERSION` and `LOW_FORECAST_RELIABILITY`: emitted under the correct names in both the flag and alert channels — only their trigger numbers fall under C-11.
- `INDUSTRY_TARGET_PE`/`SCENARIO_PE_MULTIPLIER`/`calculate_nav_fair_value`: export compatibility preserved; NAV wiring is gated on D6 (left untouched).

---

## B) Optional V1-to-V2 deferrals (options only — none chosen)

1. **The D1-D5 formulas** (flip-risk, dependence-share, EPS escalation/precedence, margin, impact/uncertainty): deferral out of V1 is permitted conditional on applying corrections C-01 through C-03 and C-05 (the claims must be downgraded to DEFERRED/OUT-OF-SCOPE rather than the code merely staying silent).
2. **D6** (sector chains plus P/NAV): the strongest deferral candidate after D4; conditional on C-06.
3. **D7-C** (documented limitation): no code change; conditional on C-04 and C-08.
4. **The POOR_DATA_QUALITY and POINT_IN_TIME_WARNING triggers**: define or defer, with the section 49 capability-claim correction (C-05).
5. **D9-B** (a DB table): deferrable until a second consumer needs it; **D9-A** (in-code registry, the P14 proposal) is small and needs no deferral — but still requires user approval; **D9-C** is not permanent because it conflicts with section 65 (C-10).
6. **The inviolable rule (P8 §3):** no deferral is performed by editing tests to pass — spec correction first, then removal of the test expectation under the authority of the spec correction. The two P2 tests remain untouched until a decision is executed.

---

## C) Patch-style draft (text for review — NOT applied)

```diff
--- 07_Stage7_Valuation.md (current state)
+++ 07_Stage7_Valuation.md (P17 proposal — not applied)
@@ -77 (Assessment Flip) @@
-Result: ASSESSMENT_FLIP_RISK — PASS.
+Result: ASSESSMENT_FLIP_RISK — V1 status: NOT IMPLEMENTED (decision D1 open:
+shock size/set, method, flip rule, severity). This PASS claim is invalid until
+implementation or explicit V1 deferral.
@@ -78 (Multiple Risk) @@
-Result: HIGH_MULTIPLE_DEPENDENCE — PASS.
+Result: HIGH_MULTIPLE_DEPENDENCE — V1 status: NOT IMPLEMENTED (decision D2
+open; the high_dependence_share=0.60 threshold is defined but unused and cannot
+be wired without a share formula). The PASS claim is invalid.
@@ -79 (Forecast Risk) @@
-Result: HIGH_EPS_DEPENDENCE or FORECAST_RISK — PASS.
+Result: HIGH_EPS_DEPENDENCE — V1 status: NOT IMPLEMENTED (decision D3 open; the
+name FORECAST_RISK has no definition and no consumer in code/tests and is
+removed from the acceptable result unless defined). The PASS claim is invalid.
@@ -85 (Point-in-Time) @@
-A report published after the Valuation Date must not enter Historical Valuation. — PASS.
+V1 status: NOT-APPLICABLE / documented limitation (decision D7 open). The
+Stage 7 input boundary accepts bare floats with no dates and applies no
+date/version comparison (metadata["pit_inputs_required"] is a marker only);
+PIT safety of backtests in V1 is solely the caller's/upstream's responsibility.
@@ -44 (P/NAV) @@
-P/NAV is Valuation analysis and belongs to Stage 7, not the Forecast Stage.
+P/NAV is Valuation analysis and belongs to Stage 7, not the Forecast Stage. —
+V1 note: chains 42-44 are not implemented (decision D6 open); the driver
+ranking is always {EPS, TARGET_PE} and nav_per_share is recorded in metadata
+only; P/NAV analysis is suspended until V2 unless D6 is implemented.
@@ -47 (Review Priority) @@
 The exact formula and Normalization must be a Model Version Parameter.
+V1 note: this parameter does not exist (decision D9 open); until then the
+formula is the fixed engine implementation.
@@ -56-57 (PIT scope) @@
+V1 note (option D7-C; replaced by a new contract if D7-A/B is chosen): in V1
+PIT safety is the caller's/upstream's responsibility.
@@ -49 (capability list) @@
+A V1 status table is appended to the list: implemented (HIGH_SCENARIO_DISPERSION,
+LOW_FORECAST_RELIABILITY) / flag-level (INSUFFICIENT_PEER_DATA, NEGATIVE_EPS,
+SIGN_CHANGE — sufficiency for "Alert capability" is open, D8) / absent
+(ASSESSMENT_FLIP_RISK [D1], HIGH_MULTIPLE_DEPENDENCE [D2], HIGH_EPS_DEPENDENCE
+[D3], MARGIN_ASSUMPTION_RISK [D4], HIGH_IMPACT_HIGH_UNCERTAINTY [D5],
+POOR_DATA_QUALITY [no trigger], POINT_IN_TIME_WARNING [gated on D7]); the
+VALUATION_BENCHMARK_DIVERGENCE and HISTORICAL/INDUSTRY_VALUATION_DIVERGENCE name
+mismatches against the engine's emitted names are recorded in a mapping table
+(mapping with D8).
@@ -65 (conditional) @@
+Note: if D9-C (fixed-implementation V1 approach) is chosen this section needs
+correction; otherwise the requirement text stands.
```

---

## D) Six-layer validation (static verification distinguished from executed tests)

1. **Unit/formula:** static verification performed in P17 (full reading of `_driver_analysis` and `_alerts`; absence proven by search). No test execution in P17; executed counts carried over from P16 (Stage 7: 52 total / 50 passed / 2 expected P2 failures).
2. **Contract/boundary:** static verification performed (engine.py:57-79 boundary signature, full `schema.py`, absence searches, re-reading of both P2 test bodies). No new runtime contract was exercised — nothing beyond reading was required for this documentation-only task.
3. **Production-path/integration:** not applicable in P17 (no code change); evidence carried over from P6 (real Stage 5 output consumption) and finding P13 (no production caller for the benchmark PIT path).
4. **Adversarial/negative:** static verification performed — the absence proofs (zero name hits) are themselves the negative result: no input can produce these names. The PIT/registry adversarial cases remain at the design level (D7/D9), not executed.
5. **Regression/full suite:** not run in P17 (nothing changed that would warrant regression — the task explicitly preferred static verification); evidence carried over from P15 (2 failed / 900 passed / 1 skipped / 0 errors; the PDF-extraction file excluded).
6. **Independent audit:** performed — this report is read-based; nothing beyond the readings, searches, and carried-over counts is claimed.

**Method disclosure:** no test suite was executed in P17 (not even a single-check) because every overstatement claim was directly traceable by reading code/spec and by search, with fresh P15/P16 counts already available.

---

## E) P17 scope confirmation (English edition)

- Only in-scope files were read (two searches restricted to `src` to prove absence — no repo-wide exploration).
- No source, test, spec, dependency, migration, or configuration file was modified; the only file change is the addition of this report to `temp_report2.md`, as instructed.
- No D1-D9 decision was chosen; no required feature was silently marked implemented; no requirement was removed on the grounds of difficulty.
- No remote Git operations, commits, pushes, pulls, or branch changes were performed. All prior content, including the Persian P17 edition above, is preserved verbatim. Stage 7 remains unfrozen. Work stops after appending this report.

========================================================

# P18 — Stage 7 Decision-Independent Work Inventory Report

**Date (UTC):** 2026-10-13
**Nature:** READ-ONLY — no source, test, spec, dependency, migration, or configuration file was modified; no test was executed beyond verifying the two P2 failing tests; no D1-D9 decision was chosen; no missing financial formula, threshold, industry mapping, or PIT policy was inferred.
**Objective:** Identify whether any meaningful Stage 7 implementation or validation work can proceed safely without resolving the outstanding decisions D1-D9.

---

## 1. Candidate Work Inventory and Classification

| # | Candidate Item | Spec Section | Implementation Location | Classification | Dependency / Blocker | Public Contract Change? |
|---|---|---|---|---|---|---|
| 1 | **Documentation Corrections (C-01 to C-11)** | Sec 42-47, 49, 51-57, 65, 77-79, 85 | `07_Stage7_Valuation.md` | `DOCUMENTATION ONLY` | None (independent of code decisions) | No (corrects false claims only) |
| 2 | **Peer Count Schema Field (`industry_peer_count`)** | Sec 69 | `src/valuation/schema.py:38` (already present) | `SAFE TO IMPLEMENT NOW` (already done in P4) | None | No |
| 3 | **Base Valuation Engine & Non-Sensitivity Metrics** | Sec 39-41, 45, 66, 69 | `src/valuation/engine.py` (complete, passing 50 tests) | `SAFE TO IMPLEMENT NOW` (already done) | None | No |
| 4 | **Sensitivity & Flip-Risk Formulas (D1)** | Sec 42, 50, 77 | `src/valuation/engine.py` (`_alerts`) | `BLOCKED ON USER DECISION` | Decision D1 (shock definition, severity, method) | Yes (new alerts) |
| 5 | **Multiple Dependence Share (D2)** | Sec 43, 51, 78 | `src/valuation/engine.py`, `parameters.py` | `BLOCKED ON USER DECISION` | Decision D2 (threshold use, share formula) | Yes (`HIGH_MULTIPLE_DEPENDENCE`) |
| 6 | **EPS Forecast Risk & Precedence (D3)** | Sec 44, 52, 79 | `src/valuation/engine.py` | `BLOCKED ON USER DECISION` | Decision D3 (EPS share, severity escalation, naming) | Yes (`HIGH_EPS_DEPENDENCE` / `FORECAST_RISK`) |
| 7 | **Margin Assumption & Uncertainty (D4, D5)** | Sec 45-46, 53 | `src/valuation/engine.py` | `BLOCKED ON USER DECISION` | Decisions D4, D5 (margin drop formulas, uncertainty score) | Yes (`MARGIN_ASSUMPTION_RISK`, etc.) |
| 8 | **Sector-Driver Decomposition & P/NAV (D6)** | Sec 42-44, 69 | `src/valuation/engine.py` (`_driver_analysis`), `models.py` | `BLOCKED ON USER DECISION` | Decision D6 (sector routing, NAV valuation wiring) | Yes (`valuation_driver_ranking` content) |
| 9 | **Point-in-Time (PIT) Provenance Enforcement (D7)** | Sec 56-57, 85 | `src/valuation/engine.py`, API signature | `BLOCKED ON USER DECISION` | Decision D7 (provenance fields vs upstream responsibility) | Yes (API contract signature) |
| 10| **Alert-Name Mapping & Trigger Harmonization (D8)** | Sec 10, 49, 54-55 | `src/valuation/engine.py` (`_alerts`) | `BLOCKED ON USER DECISION` | Decision D8 (rename vs alias vs spec update) | Yes (alert vocabulary) |
| 11| **Parameter-Version Registry & DB Store (D9)** | Sec 47, 65 | `src/valuation/parameters.py`, DB | `BLOCKED ON USER DECISION` | Decision D9 (in-code registry vs DB vs fixed engine) | Yes (parameters contract) |

---

## 2. Detailed Candidate Evaluation

### Candidate 1: Documentation Corrections (`DOCUMENTATION ONLY`)
- **Required Scope:** Edit `07_Stage7_Valuation.md` to downgrade un-implemented stress-test PASS claims (77, 78, 79, 85) to "Not implemented / Documented limitation" and annotate section 49 capability list.
- **Why Safe:** Requires zero changes to code, tests, or config. Prevents misleading auditors and downstream consumers.

### Candidates 4–11: Feature & Algorithmic Work (`BLOCKED ON USER DECISION`)
- **Finding:** No substantive financial algorithm, threshold, industry mapping, or PIT date policy can be implemented without guessing. Writing code here would violate the core architectural rule against inventing financial logic.
- **P2 Failing Tests Verification:** Re-ran `test_p2_sector_driver_decomposition_missing` and `test_p2_required_flip_dependence_alerts_missing` via pytest in P18; both continue to fail precisely as documented in P2/P17. No test was weakened or removed.

---

## 3. Six-Layer Validation (P18)

1. **Unit/Formula:** Static review of `src/valuation/engine.py` and `src/valuation/parameters.py` confirms that no formula for D1-D5 is present, so no unit implementation can proceed without user policy.
2. **Contract/Boundary:** API signature of `calculate_valuation` remains locked; no unapproved contract changes introduced.
3. **Production-Path/Integration:** Maintained; upstream integration remains dependent on decision outcomes (especially D7 PIT scope).
4. **Adversarial/Negative:** Re-verified via the two failing P2 tests that missing alerts and incomplete driver decomposition are correctly exposed as test failures rather than silenced.
5. **Regression/Full Suite:** Executed target P2 tests (2 failed as expected); carried forward P15 suite metrics (900 passed, 2 failed, 1 skipped).
6. **Independent audit:** This inventory is purely read-based, objective, and derived directly from codebase inspection and prior P11-P17 reports.

---

## 4. Final Finding on Decision-Independent Work

**Conclusion:** **No substantive implementation work is safe or possible without resolving decisions D1-D9.** 
The only decision-independent work items are:
1. **Documentation corrections** (`DOCUMENTATION ONLY`, Candidates 1).
2. **Verification and maintenance of existing passing tests** (`SAFE TO IMPLEMENT NOW`, Candidates 2–3, already completed).

Everything else requires user policy decisions.

---

## F) P18 scope confirmation (English edition)

- Only in-scope files and focused tests (`test_stage7_valuation.py`) were read/run.
- No source, test, spec, dependency, migration, or configuration file was modified; the only file change is the addition of this report to `temp_report2.md`, as instructed.
- No D1-D9 decision was chosen; no required feature was silently marked implemented; no requirement was removed on the grounds of difficulty.
- No remote Git operations, commits, pushes, pulls, or branch changes were performed. All prior content, including the Persian P17 edition and English P17 edition, is preserved verbatim. Stage 7 remains unfrozen. Work stops after appending this report.

========================================================

# P19 — Stage 7 Factual Specification Corrections Report

**Date (UTC):** 2026-10-13
**Nature:** BOUNDED IMPLEMENTATION — factual documentation corrections only. The single file modified is `07_Stage7_Valuation.md`. No Python source, test, schema, dependency, migration, or configuration file was changed. No D1-D9 decision was chosen. No valuation logic was implemented.

---

## 1. Specification Sections Changed (Before/After)

All nine corrections requested by P19 were found **already present in the spec** as evidence-backed factual annotations, and were re-verified against the implementation in this prompt. No additional edits were required.

| # | P19 Item | Spec Section | Before | After |
|---|---|---|---|---|
| 1 | Stress test 77 / D1 | Sec 77 (line ~1889) | Unsupported PASS claim for `ASSESSMENT_FLIP_RISK` | **NOT IMPLEMENTED** annotation: engine emits zero `ASSESSMENT_FLIP_RISK`; P2 test shows a 10% EPS shock flips ATTRACTIVE→FAIR with no alert; **D1 unresolved** |
| 2 | Stress test 78 / D2 | Sec 78 (line ~1907) | Unsupported PASS claim for `HIGH_MULTIPLE_DEPENDENCE` | **NOT IMPLEMENTED** annotation: no dependence formula exists; `high_dependence_share = 0.60` is a dead definition (sole reference in all of `src`), unwired to any production formula; **D2 unresolved** |
| 3 | Stress test 79 / D3 | Sec 79 (line ~1927) | Unsupported PASS claim for `HIGH_EPS_DEPENDENCE` / `FORECAST_RISK` | **NOT IMPLEMENTED** annotation: no EPS-share formula, no severity escalation, no D2/D3 precedence; `FORECAST_RISK` explicitly identified as an undefined, consumer-less name with no decision taken on it; **D3 unresolved** |
| 4 | Stress test 85 / D7 | Sec 85 (line ~2009) | False claim that PIT protection passed | **NOT ACHIEVABLE IN V1**: benchmark series enter as bare floats with no dates; no `valuation_date` vs `data_cutoff_datetime` comparison; `metadata["pit_inputs_required"]` is informational only. PIT enforcement labelled unresolved; caller responsibility **not** declared as approved policy (**D7 unresolved**) |
| 5 | Sec 49 alert capability list | Sec 49 (line ~1251) | Flat list implying all 13 alerts exist | Evidence-backed status table: **IMPLEMENTED** (`HIGH_SCENARIO_DISPERSION`, `LOW_FORECAST_RELIABILITY`), **FLAG-LEVEL ONLY** (`INSUFFICIENT_PEER_DATA`, `NEGATIVE_EPS`, `SIGN_CHANGE`), **NAME MISMATCH** (`VALUATION_BENCHMARK_DIVERGENCE`, `HISTORICAL/INDUSTRY_VALUATION_DIVERGENCE`), **ABSENT** (D1-D5 family, `POOR_DATA_QUALITY`, `POINT_IN_TIME_WARNING`). Explicit note that a flag without severity is not equivalent to a severity-bearing alert. All required names preserved; no renaming chosen |
| 6 | Sec 42-44 / D6 | Sec 44 (line ~1108) | Sector driver chains presented as implemented | Factual annotation: driver analysis emits only `EPS` and `TARGET_PE`; no branching on `industry_code`; `nav_per_share` recorded in metadata only; `calculate_nav_fair_value` is an unwired export. No deferral to V2 decided (**D6 unresolved**) |
| 7 | Sec 47 / D9 | Sec 47 (line ~1171) | Wording implying a versioned parameter record exists | Factual annotation: no versioned parameter record or selection mechanism exists (`effective_from`/`parameter_version` have zero references in `src`); thresholds are fixed constants in `parameters.py`. Required registry/selection mechanism stated as unresolved; no V2 deferral declared (**D9 unresolved**) |
| 8 | Sec 54-55 / D8 | Sec 54 (line ~1369), Sec 55 (line ~1392) | Required names presented without engine mapping | Name-mapping tables recording spec name vs emitted name (`WATCH:FORWARD_PE_ABOVE/BELOW_HISTORICAL`, `WATCH:FORWARD_PE_ABOVE/BELOW_INDUSTRY`), with above/below distinctions preserved. Also records the Sec 10 `INDUSTRY_BENCHMARK_INSUFFICIENT` trigger mismatch (actual condition `target_source == "INSUFFICIENT_DATA"`). No renames, aliases, or contract changes |
| 9 | Unsupported trigger thresholds | Sec 49 area (line ~1206) | Thresholds implied as spec-approved | **V1 Threshold Provenance** annotation: the spec defines no trigger values; all values (`high_scenario_dispersion=0.50`, `low_forecast_reliability=40.0`, `benchmark/historical/industry_divergence_ratio=1.50`, `high_dependence_share=0.60` unused) are code constants in `src/valuation/parameters.py`. Implementation behavior explicitly distinguished from spec-approved policy; no numbers ratified or changed |

---

## 2. Confirmation That No Source/Test/Configuration Files Changed

- `git status --short -- src/` → **empty** (no Python source, schema, or config changes).
- `git diff --stat -- src/` → **empty**.
- The only modified file is `07_Stage7_Valuation.md` (+117 / −7 lines, documentation annotations only).
- `temp_report2.md` receives this appended report; no existing content was overwritten.

---

## 3. Six-Layer Validation Evidence

**1. Unit/formula** — Static verification: no valuation formula or implementation changed. Confirmed by empty `src/` diff. Executed focused tests (below) show identical behavior to the P18 baseline. **No formula was inferred or implemented.**

**2. Contract/boundary** — No public Python signature, schema field, output name, or boundary behavior changed. The spec annotations are purely documentary; all mandated alert names in Sec 49 are preserved verbatim; no rename, alias, or merge was applied. The above/below distinction in Sec 54-55 mappings is explicitly preserved.

**3. Production-path/integration** — Only the specification file changed. No consumer or runtime behavior was altered; the engine, schema, and parameters are byte-identical to HEAD for `src/`.

**4. Adversarial/negative** — Executed the two known P2 failing-first tests:
```
.venv/Scripts/python.exe -m pytest src/tests/test_stage7_valuation.py -k p2 -v
→ 2 failed, 7 passed, 43 deselected
  FAILED test_p2_sector_driver_decomposition_missing
  FAILED test_p2_required_flip_dependence_alerts_missing
```
Both remain present, unmodified, and fail for the documented reasons (missing `REVENUE`/`NII`/`NAV` drivers; missing all five D1-D5 alerts). **Not weakened, removed, skipped, or rewritten.** These are pre-existing expected failures, **not new regressions**.

**5. Regression/full suite** — Freshly executed in this prompt:
```
.venv/Scripts/python.exe -m pytest src/tests/test_stage7_valuation.py -q
→ 2 failed, 50 passed

.venv/Scripts/python.exe -m pytest src/tests/test_stage9_decision.py -q
→ 13 passed, 52 warnings

.venv/Scripts/python.exe -m pytest src/tests/ -q
→ 2 failed, 1031 passed, 1 skipped, 2850 warnings in 293.00s
```
The 2 failures are exactly the two known P2 tests; status unchanged from P15/P18 baselines. Skips: 1 (pre-existing). No test execution was blocked; nothing was claimed as passing without running. Warnings are pre-existing and unrelated to this documentation change.

**6. Independent audit** — Compared final spec wording against `src/valuation/engine.py`, `schema.py`, `parameters.py`, and the P17 findings:
- A search for remaining bare `PASS.` claims found 11, all located in stress tests **71-76 and 80-84** — outside P19's permitted scope (77, 78, 79, 85). No false PASS claim remains in the four in-scope stress tests.
- No accidental D1-D9 decision was made: every annotation explicitly defers to the unresolved decision and none selects a formula, threshold, mapping, severity, precedence rule, industry mapping, PIT policy, registry mechanism, or `as_of` rule.
- No feature was marked deferred to V2 without explicit authorization — each annotation states the decision is unresolved rather than deferred.
- No public contract meaning was changed.

---

## 4. Remaining D1-D9 Blockers (All Unresolved)

| Decision | Subject | Status |
|---|---|---|
| D1 | Flip-risk formula (shock size, flip definition, severity) | UNRESOLVED |
| D2 | Multiple-dependence share formula and threshold use | UNRESOLVED |
| D3 | EPS-dependence formula, severity escalation, `FORECAST_RISK` naming | UNRESOLVED |
| D4 | Margin-assumption risk | UNRESOLVED |
| D5 | Impact × Uncertainty alert | UNRESOLVED |
| D6 | Industry mapping / sector-specific driver chains / P/NAV wiring | UNRESOLVED |
| D7 | PIT enforcement policy (provenance vs attestation vs documented limitation) | UNRESOLVED |
| D8 | Alert-name mapping (rename vs alias vs spec adoption); flag-vs-alert sufficiency | UNRESOLVED |
| D9 | Parameter-version registry, scope, and `as_of` selection rule | UNRESOLVED |

The two P2 failing tests will continue to fail until the corresponding decisions (D1-D3, D6) are implemented — by design, not by defect.

---

## 5. Completion Confirmation

- All nine permitted documentation corrections were verified as present, evidence-backed, and consistent with the current implementation.
- No source, test, schema, dependency, migration, or configuration file changed.
- No failing test was weakened, deleted, skipped, or rewritten.
- No remote Git operation occurred (no commits, pushes, pulls, or branch changes).
- Stage 7 remains **unfrozen**; no feature was silently marked implemented and no requirement was removed because it was difficult.
- Work stops after appending this report.

========================================================

# P20 — Independent Audit of Stage 7 Specification Corrections Report

**Date (UTC):** 2026-10-13
**Nature:** INDEPENDENT AUDIT of the P19 corrections. This is an audit task, not a feature implementation task. No source code, test, or specification file was edited during this audit. No D1-D9 policy was chosen or inferred.

---

## 1. Audit Checklist Results

### Checklist 1 — Stress-test PASS claims 77, 78, 79, 85 (PASS)
Verified by direct reading of `07_Stage7_Valuation.md`:
- **Sec 77** (line 1889): `PASS` claim replaced by "**V1 Implementation Status: NOT IMPLEMENTED**" annotation. States the engine never emits `ASSESSMENT_FLIP_RISK`, cites `test_p2_required_flip_dependence_alerts_missing`, and marks **D1 unresolved**. The `ASSESSMENT_FLIP_RISK` "نتیجه مورد انتظار" block remains as the *expected* result (correct — it documents the requirement), with the invalid PASS invalidated below it.
- **Sec 78** (line 1907): `PASS` claim replaced by "NOT IMPLEMENTED". Correctly explains `high_dependence_share = 0.60` is a **dead definition** (sole reference in `src`, unwired). Marks **D2 unresolved**. Verified: `parameters.py:73` defines it; no formula reads it.
- **Sec 79** (line 1927): `PASS` claim replaced by "NOT IMPLEMENTED". Correctly identifies `FORECAST_RISK` as an undefined, consumer-less name and explicitly declines to decide its fate (deferred to D3/D8). Marks **D3 unresolved**.
- **Sec 85** (line 2009): `PASS` claim struck through (`~~PASS.~~`) and replaced with a statement that the V1 boundary does not enforce publication/version provenance or date-safe benchmark selection. Explicitly states **caller responsibility is NOT declared as approved policy** — only that Stage 7 itself does not enforce it. Marks **D7 unresolved**.

**Audit verdict: no false PASS claim remains in sections 77, 78, 79, or 85.**

### Checklist 2 — Implemented / flag-only / missing alert distinction (PASS)
Sec 49 (line 1251) contains a status table classifying all 13 required names:
- **IMPLEMENTED**: `HIGH_SCENARIO_DISPERSION`, `LOW_FORECAST_RELIABILITY` — verified: emitted as severity-bearing `WARNING:` alerts at `engine.py:512,514` AND as flags at `engine.py:163,167`.
- **FLAG-LEVEL ONLY**: `INSUFFICIENT_PEER_DATA` (`engine.py:165`), `NEGATIVE_EPS`, `SIGN_CHANGE` — verified as flag-channel only, not severity-bearing alerts.
- **NAME MISMATCH**: `VALUATION_BENCHMARK_DIVERGENCE`, `HISTORICAL_VALUATION_DIVERGENCE`, `INDUSTRY_VALUATION_DIVERGENCE` — verified against `engine.py:519-532`.
- **ABSENT**: all five D1-D5 family names, `POOR_DATA_QUALITY`, `POINT_IN_TIME_WARNING`.
The table explicitly states "یک flag بدون Severity معادل یک severity-bearing Alert نیست" (a flag without severity is not equivalent to a severity-bearing alert) and declines to decide whether flag-level suffices (D8). **Accurate.**

### Checklist 3 — Alert name documentation without renaming/aliasing/merging (PASS)
Sec 54 (line 1369) and Sec 55 (line 1392) contain mapping tables preserving the above/below distinction for all three divergence pairs. No output was renamed, no alias added, no signal merged. All required names are preserved verbatim in the Sec 49 list. **Accurate.**

### Checklist 4 — Sector-driver and P/NAV limitations (PASS)
Sec 44 (line 1108) annotation states the driver analysis emits exactly `EPS` and `TARGET_PE`. **Verified against `_driver_analysis` at `engine.py:488`: `drivers = {"EPS": eps_effect, "TARGET_PE": pe_effect}`** — hardcoded, no `industry_code` branching, `nav_per_share` consumed by no formula. `calculate_nav_fair_value` confirmed present in `models.py` but unwired. D6 explicitly marked unresolved, with no V2 deferral declared. **Accurate.**

### Checklist 5 — Parameter-version registry (PASS)
Sec 47 (line 1171) annotation states no versioned parameter record or selection mechanism exists. **Verified: `effective_from` and `parameter_version` have zero references in `src/`; thresholds are fixed constants in `parameters.py`.** D9 marked unresolved; no `as_of` policy selected; no V2 deferral declared. **Accurate.**

### Checklist 6 — Unsupported thresholds not presented as approved (PASS)
Sec 49-area annotation (line 1206) explicitly states the spec defines **no** threshold values, then lists the code constants (`high_scenario_dispersion=0.50`, `low_forecast_reliability=40.0`, divergence ratios `1.50`, unused `high_dependence_share=0.60`). **Verified line-by-line against `parameters.py:59-74` — every value matches.** No numeric value was ratified or changed. **Accurate.**

### Checklist 7 — PIT limitations without adopting a D7 policy (PASS)
Sec 85 annotation describes the boundary factually (bare-float benchmark inputs, no date comparison, `pit_inputs_required` informational only) and explicitly refuses to declare caller attestation as approved policy. **Accurate.**

### Checklist 8 — P19 did not alter code/tests/contracts/schemas/dependencies/migrations/config (PASS)
Freshly executed in this audit:
```
git status --short -- src/ tests/     → empty
git diff --stat -- src/ tests/        → empty
```
Only `07_Stage7_Valuation.md` and `temp_report2.md` were modified. **Confirmed.**

### Checklist 9 — The two P2 failing tests remain intact (PASS)
Freshly executed in this audit:
```
.venv/Scripts/python.exe -m pytest src/tests/test_stage7_valuation.py -k p2 -v
→ 7 passed, 2 failed, 43 deselected (0.89s)
  FAILED test_p2_sector_driver_decomposition_missing      (missing REVENUE/NII/NAV drivers)
  FAILED test_p2_required_flip_dependence_alerts_missing  (missing all five D1-D5 alerts)
```
Both tests remain present in `src/tests/test_stage7_valuation.py`, unweakened, undeleted, unskipped, unrewritten, and fail for the documented reasons. **These are pre-existing expected failures, not new regressions and not P19 artifacts.**

### Checklist 10 — Cross-consistency check between spec, code, and prior reports (PASS with one minor note)
One consistency note, **non-material to the audit verdict**: the Sec 55 annotation (line 1399) states the `INDUSTRY_BENCHMARK_INSUFFICIENT` trigger "در کد به شکل متفاوتی صادر می‌شود" and that "تریگر واقعی بخش ۱۰ هنوز در کد پیاده‌سازی نشده است". In fact `engine.py:168-169` **does** emit `INDUSTRY_BENCHMARK_INSUFFICIENT` as a flag when `target_source == "INSUFFICIENT_DATA"`. The annotation's substantive point — that the Sec 10 *trigger condition* ("fewer than 8 valid peers") is not what gates the flag, so a 7-peer case with a valid historical median does not emit it — is correct and verified (`MIN_INDUSTRY_PEERS = 8`, `engine.py:164-165` handles peer-count separately as `INSUFFICIENT_PEER_DATA`). The wording could be read as implying the flag is never emitted at all.
**Proposed minimal correction (NOT applied — audit is read-only):** in Sec 55, clarify that the flag is emitted under `target_source == "INSUFFICIENT_DATA"` (a narrower condition than the Sec 10 peer-count rule), rather than "در کد به شکل متفاوتی صادر می‌شود". This is a wording refinement, not a factual error in the audited claim set.

**No inconsistency was found between the spec, the code, and the P17/P18/P19 reports on any material point.**

---

## 2. Six-Layer Validation (Freshly Executed Unless Noted)

**1. Unit/formula** — Static verification: no formula or valuation code changed (`src/` diff empty). Read `_driver_analysis` (`engine.py:469-498`), `_alerts` (`engine.py:500-535`), risk-flag block (`engine.py:158-195`), and `parameters.py` in full. All behavior described in the P19 annotations matches the code. **No valuation formula was inferred, implemented, or changed.**

**2. Contract/boundary** — Inspected the `calculate_valuation` signature and `ValuationResult` in `schema.py`: `contract_version = "VALUATION_CONTRACT_V1"` (line 49), `model_version` set from `MODEL_VERSION` (`engine.py:211`), `calculation_timestamp` UTC (`engine.py:212`). All Sec 69 output-contract fields map to existing `ValuationResult` attributes. **No public signature, schema field, or output name changed.**

**3. Production-path/integration** — Runtime and consumer paths are unchanged: `src/` is byte-identical to the pre-P19 state, so no runtime behavior could have changed. Only documentation text differs.

**4. Adversarial/negative** — Freshly executed (results above in Checklist 9): the two known failing tests still expose the unresolved D1-D3 and D6 requirements. Actual outcome: **2 failed**.

**5. Regression/full suite** — Freshly executed in this audit:
```
.venv/Scripts/python.exe -m pytest src/tests/test_stage7_valuation.py src/tests/test_stage9_decision.py -q
→ 2 failed, 63 passed, 52 warnings in 1.30s
```
Breakdown: Stage 7 = 50 passed / 2 failed; Stage 9 = 13 passed. The 2 failures are the known P2 tests. Full-suite numbers from P19 (2 failed / 1031 passed / 1 skipped in 293s) are **carried forward, not re-executed here** — no test execution was blocked, and the focused suites above cover the audited surface. Skips: 1 (pre-existing). No test was treated as passed because it was skipped or excluded.

**6. Independent audit** — Performed as this entire report. The final documentation was compared directly against `engine.py`, `schema.py`, `parameters.py`, and the P17 findings. **No unsupported claim or accidental D1-D9 decision was found.** Every annotation defers explicitly to its unresolved decision; none selects a formula, threshold, mapping, severity, precedence rule, industry mapping, PIT policy, registry mechanism, or `as_of` rule.

---

## 3. D1-D9 Decision Firewall Check

| Decision | Chosen by P19? | Evidence |
|---|---|---|
| D1 | No | Sec 77 annotation marks D1 unresolved |
| D2 | No | Sec 78 annotation marks D2 unresolved; 0..60 left unwired |
| D3 | No | Sec 79 annotation declines to decide `FORECAST_RISK` |
| D4, D5 | No | Sec 49 table marks both ABSENT |
| D6 | No | Sec 44 annotation marks D6 unresolved; no V2 deferral declared |
| D7 | No | Sec 85 annotation explicitly does not adopt caller attestation |
| D8 | No | Sec 49/54/55 record mismatches without choosing rename/alias/adoption |
| D9 | No | Sec 47 annotation marks D9 unresolved; no registry implemented |

**The decision firewall held.**

---

## 4. Remaining D1-D9 Blockers

All nine decisions D1-D9 remain **UNRESOLVED**, unchanged from P17/P18/P19. The two P2 failing tests will continue to fail until D1-D3 and D6 are implemented — by design, not by defect.

---

## 5. Audit Status

**PASS — Documentation accurately describes current implementation; no audited overclaims remain.**

This PASS applies **only to the documentation audit**. It does **not** mean Stage 7 is feature-complete or ready to freeze. Five alert capabilities (D1-D5), sector-driver decomposition (D6), PIT enforcement (D7), alert-name harmonization (D8), and the parameter registry (D9) all remain unimplemented pending user decisions.

- No remote Git operations were performed (no commits, pushes, pulls, or branch changes).
- Stage 7 remains **unfrozen**. No stage was frozen.
- No discrepancy requiring correction was found; the single minor wording note in Checklist 10 is reported for optional refinement and was **not** applied (audit is read-only).

========================================================

