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

# P21 — Stage 7 Section 55 Wording Refinement Report

**Date (UTC):** 2026-10-13
**Nature:** BOUNDED DOCUMENTATION EDIT — one wording refinement in section 55 of `07_Stage7_Valuation.md` only. No Python source, test, schema, dependency, migration, or configuration file was changed. No alert names, emission conditions, severity, thresholds, or output contracts were changed. D8 was not chosen.

---

## 1. Evidence Verified Before Editing

**`_select_target_pe` — `src/valuation/engine.py:256-269`:**
```python
if industry_forward is not None and forward_peer_count >= MIN_INDUSTRY_PEERS:
    return industry_forward, "INDUSTRY_FORWARD_PE"
if historical is not None:
    return historical, "HISTORICAL_MEDIAN_PE"
if industry_ttm is not None:
    return industry_ttm, "INDUSTRY_TTM_PE"
return None, "INSUFFICIENT_DATA"
```

**Flag generation — `src/valuation/engine.py:164-169`:**
```python
if forward_values and valid_forward_count < MIN_INDUSTRY_PEERS:
    flags.append("INSUFFICIENT_PEER_DATA")
...
if target_source == "INSUFFICIENT_DATA":
    flags.append("INDUSTRY_BENCHMARK_INSUFFICIENT")
```

**`MIN_INDUSTRY_PEERS = 8`** — `src/valuation/parameters.py:79`.

The evidence supports all four required facts: the engine **can** emit `INDUSTRY_BENCHMARK_INSUFFICIENT` (under `target_source == "INSUFFICIENT_DATA"`); the section 10 peer-count condition is **not** equivalent to that emission condition; a sub-8-peer case with a usable historical median does **not** emit it (`target_source` becomes `HISTORICAL_MEDIAN_PE`); and `INSUFFICIENT_PEER_DATA` is a **separate** signal (gated on peer count alone).

---

## 2. Exact Wording Changed (Before / After)

**BEFORE** (single paragraph, section 55):
> علاوه بر این، تریگر `INDUSTRY_BENCHMARK_INSUFFICIENT` (بخش ۱۰، «کمتر از ۸ Peer معتبر») در کد به شکل متفاوتی صادر می‌شود: شرط واقعی `target_source == "INSUFFICIENT_DATA"` است. در نتیجه، با ۷ Peer ولی یک Historical Median معتبر، این flag صادر **نمی‌شود** و فقط `INSUFFICIENT_PEER_DATA` در flag channel ظاهر می‌شود. تریگر واقعی بخش ۱۰ هنوز در کد پیاده‌سازی نشده است.

**AFTER** (three paragraphs):
> علاوه بر این، تریگر `INDUSTRY_BENCHMARK_INSUFFICIENT` (بخش ۱۰، «کمتر از ۸ Peer معتبر») در کد تحت **شرط متفاوتی** صادر می‌شود. موتور این flag را **صادر می‌کند**، اما تنها زمانی که `target_source == "INSUFFICIENT_DATA"` باشد — یعنی هیچ Industry Forward P/E با حداقل ۸ Peer معتبر، هیچ Historical Median معتبر و هیچ Industry TTM P/E معتبر در دسترس نباشد (`_select_target_pe` در `src/valuation/engine.py`).
>
> این شرط emission با شرط Peer Count بخش ۱۰ **معادل نیست**: با ۷ Peer معتبر ولی یک Historical Median معتبر، `target_source` برابر `HISTORICAL_MEDIAN_PE` می‌شود، در نتیجه `INDUSTRY_BENCHMARK_INSUFFICIENT` صادر **نمی‌شود** — حتی اگر یک benchmark جایگزین و قابل‌استفاده انتخاب شده باشد. بنابراین یک مورد «کمتر از ۸ Peer معتبر» می‌تواند یک benchmark قابل‌استفاده داشته باشد و باز هم این flag را دریافت نکند. تریگر کامل بخش ۱۰ (مبتنی بر Peer Count) در کد پیاده‌سازی نشده است.
>
> `INSUFFICIENT_PEER_DATA` یک سیگنال **مجزا** است و نباید با `INDUSTRY_BENCHMARK_INSUFFICIENT` یکی گرفته شود: اولی زمانی صادر می‌شود که `forward_values` موجود باشد و تعداد peerهای Forward معتبر کمتر از `MIN_INDUSTRY_PEERS = 8` باشد (`engine.py:164-165`) و صرفاً کمبود تعداد Peer را گزارش می‌کند، دومی صرفاً نبود هر گونه benchmark قابل‌استفاده را گزارش می‌کند. این دو flag هم می‌توانند هم‌زمان صادر شوند و هم می‌توانند مستقل از یکدیگر صادر شوند.

**What the refinement corrects:** the old wording could be read as implying the flag is never emitted at all ("در کد به شکل متفاوتی صادر می‌شود" followed only by a non-emission example). The new wording states positively that the flag **is** emitted, names its exact emission condition, states the non-equivalence with the peer-count rule, and separates `INSUFFICIENT_PEER_DATA` explicitly.

The retained D8 line ("**تصمیم باز (D8):** انتخاب rename / alias / پذیرش spec، هنوز اتخاذ نشده است.") and the entire name-mapping table above it are unchanged.

---

## 3. Six-Layer Validation

**1. Unit/formula** — Static verification: no financial logic changed. `src/` diff is empty. No formula, threshold, or computation was touched. **No tests were executed for this layer** — the change is documentation-only and cannot affect formula behavior.

**2. Contract/boundary** — Public signatures, schema, alert names, and output contracts are unchanged: `git status --short -- src/ tests/` → **empty**. The refinement names existing flags and existing conditions only; it introduces no new name, no alias, no merge, and no severity claim. `VALUATION_CONTRACT_V1` is untouched.

**3. Production-path/integration** — No runtime file changed. Only `07_Stage7_Valuation.md` was edited (documentation only), so no runtime or consumer path could change.

**4. Adversarial/negative** — The wording now accurately describes the adversarial case: fewer than 8 valid peers **with** a usable historical median. Traced through `_select_target_pe`: `industry_forward is not None and forward_peer_count >= MIN_INDUSTRY_PEERS` fails at 7 peers → falls to `if historical is not None` → returns `HISTORICAL_MEDIAN_PE` → `target_source != "INSUFFICIENT_DATA"` → `INDUSTRY_BENCHMARK_INSUFFICIENT` is **not** emitted, while `INSUFFICIENT_PEER_DATA` **is** emitted (7 < 8 with forward values present). The new wording states exactly this, and does not imply the current implementation satisfies the section 10 trigger.

**5. Regression/full suite** — Freshly executed:
```
.venv/Scripts/python.exe -m pytest src/tests/test_stage7_valuation.py src/tests/test_stage9_decision.py -q
→ 2 failed, 63 passed, 52 warnings in 1.24s
```
Breakdown: Stage 7 = 50 passed / 2 failed; Stage 9 = 13 passed. The 2 failures are the known P2 tests (`test_p2_sector_driver_decomposition_missing`, `test_p2_required_flip_dependence_alerts_missing`) — **pre-existing expected failures, not new regressions**. Skips: 0 in this focused run; the full-suite skip count of 1 is carried forward from P19/P20. No test was treated as passed because it was skipped or excluded. Full-suite re-execution was not repeated here; the focused Stage 7 + Stage 9 suites cover the affected surface and the change cannot affect runtime behavior.

**6. Independent audit** — The final sentences were compared directly against `_select_target_pe` (`engine.py:256-269`), the flag block (`engine.py:164-169`), and `MIN_INDUSTRY_PEERS = 8` (`parameters.py:79`). Every assertion in the new wording is traceable to code. **D8 remains unresolved** — the refinement records the mismatch without choosing rename, alias, or spec adoption, and does not imply the current implementation satisfies the section 10 peer-count trigger.

---

## 4. Scope Compliance

- Only the ambiguous wording in section 55 was modified; the name-mapping table and D8 line are unchanged.
- No other specification section was touched; no source, test, schema, dependency, migration, or configuration file was changed.
- No alert name, emission condition, severity, threshold, or output contract was changed.
- D8 was not chosen; no D1-D9 policy was inferred.
- No remote Git operations (no commits, pushes, pulls, or branch changes).

---

## 5. Remaining Blockers

D1-D9 all remain **UNRESOLVED**, unchanged. D8 specifically remains open: rename vs alias vs spec adoption of the current names, plus whether flag-level emission satisfies the section 49 alert capability. The two P2 failing tests will continue to fail until D1-D3 and D6 are implemented — by design, not by defect.

---

## 6. Completion Confirmation

- The single wording refinement identified by P20 was applied and verified against the implementation.
- The evidence supported the correction (the pre-existing wording was genuinely ambiguous, per P20 Checklist 10), so the edit was not forced.
- **Stage 7 remains unfrozen.** No stage was frozen. Work stops after appending this report.

========================================================

# P22 — Stage 7 D1-D9 Evidence-Based Decision Brief Report

**Date (UTC):** 2026-10-13
**Nature:** READ-ONLY decision brief for the project owner. No source, test, schema, spec, dependency, migration, or configuration file was modified. No D1-D9 policy choice was made. No formulas, thresholds, severities, mappings, dates, or defaults were invented.
**Evidence base:** `temp_report2.md` (P11-P21); `07_Stage7_Valuation.md` (sections 10, 42-57, 64-65, 69, 77-79, 85); `src/valuation/engine.py`, `models.py`, `parameters.py`, `schema.py`; `src/tests/test_stage7_valuation.py`; `src/tests/test_stage9_decision.py` (consumer contract). Produced by static review after two subagent attempts failed on upstream API connection errors; the subagent's last incomplete action was an industry-code taxonomy check for D6, so D6 uses only evidence already verified in P17-P21.

---

## Executive Summary (one page)

Stage 7's core valuation path is implemented and tested: the scenario fair-value identity `FV = EPS × target P/E` (`calculate_forward_pe_fair_value`), the benchmark hierarchy (`_select_target_pe`), confidence/risk grading, driver impact/uncertainty/review-priority for `{EPS, TARGET_PE}`, and severity-bearing divergence alerts. **50 of 52 Stage 7 tests pass; Stage 9's 13 consumer tests pass.** What remains is the *sensitivity/risk-alert layer* (D1-D5) and *provenance/versioning infrastructure* (D7, D9), plus *sector-driver chains* (D6) and *alert-name harmonization* (D8).

The central finding: **none of D1-D5 has a formula in the spec or the code.** For D1 and D5 the engine already computes *ingredients* (a 0.10 one-at-a-time perturbation, an uncertainty blend) but they are engine-chosen implementation constants, **not** owner-approved financial policy, and reusing them as policy would silently launder an unapproved choice into the spec. For D2 and D3 there is not even a candidate metric. For D4 there is a hard contract gap: **Stage 7 exposes no margin series at all.** D6 requires source fields, sector mappings, and contract expansions that do not exist anywhere in the project, and is additionally constrained by the rule that Stage 7 must consume Stage 5 EPS forecasts rather than rebuild EPS. D7 cannot be enforced at the current boundary because benchmark series enter as bare floats with no dates. D8 is a naming/semantics question where every option has real consumer-compatibility cost (Stage 9 parses these outputs today). D9 has three viable mechanisms but the `as_of` selection rule is unresolvable without an owner-approved temporal contract.

**Two decisions are prerequisites for the rest: D6 (unlocks D5's full scope and the two failing P2 tests) and D8 (fixes the vocabulary every other alert decision emits into).** D7 and D9 are infrastructure that can proceed in parallel once funded. No substantive implementation is safe before owner approval — this was already the P18 conclusion and P22's independent re-verification confirms it.

---

## D1 — Assessment Flip Risk

**1. Current verified behavior (evidence).** The engine emits **no** `ASSESSMENT_FLIP_RISK` output — zero references in all of `src/valuation` (verified P17). `_alerts` (`engine.py:500-535`) produces only: `WARNING:HIGH_SCENARIO_DISPERSION`, `WARNING:LOW_FORECAST_RELIABILITY`, `CRITICAL:INSUFFICIENT_BENCHMARK_DATA`, `WATCH:VALUATION_ABOVE/BELOW_TARGET_PE`, `WATCH:FORWARD_PE_ABOVE/BELOW_HISTORICAL`, `WATCH:FORWARD_PE_ABOVE/BELOW_INDUSTRY`, `INFO:TOP_DRIVER:{first}`. Status transitions *are* computed (`_valuation_status`, `engine.py:156`), and the failing test `test_p2_required_flip_dependence_alerts_missing` demonstrates that a 10% EPS shock moves status `ATTRACTIVE → FAIR` **with no alert raised**. `SENSITIVITY_PERTURBATION = 0.10` (`parameters.py:77`) exists but is used only inside `_driver_analysis` for driver *impact*, never for flip detection.

**2. Unanswered policy question.** What counts as a flip, on which inputs, at what perturbation magnitude, with what severity — and is that severity derived from status distance, magnitude of fair-value change, or something else?

**3. Evidence-supported options (not recommendations).**
- **(a) Reuse the existing 0.10 one-at-a-time perturbation** as the flip probe. Grounded in real code, zero new constants. But 0.10 is an engine-chosen driver-impact constant; adopting it for flips is a *policy* act, not a discovery.
- **(b) Define a dedicated flip perturbation set** (which inputs: EPS, target P/E, scenario probabilities, reliability?) with owner-specified magnitudes. Most faithful to spec sections 50/77; requires the owner to state values.
- **(c) Define flip by status-transition class only** (e.g. `ATTRACTIVE → FAIR/EXPENSIVE`), with no magnitude modeling. Simplest, but cannot express "relatively small and reasonable change" (spec section 50's own words) without a magnitude.
- The spec establishes **no** flip magnitude, formula, or severity. That must be stated plainly: there is no value to discover here, only one to decide.

**4. Financial correctness risks / failure modes.** A too-large probe makes genuinely fragile ratings look stable (false negatives on the highest-risk `ATTRACTIVE` band — the exact population the alert targets). A too-small probe floods the output with noise (false positives) and can be gamed by threshold placement. Perturbing *correlated* inputs independently (EPS and target P/E together) double-counts. Severity detached from economic magnitude invites threshold-fitting to backtest noise.

**5. Contract / consumer / regression implications.** Adds a **new public alert name** to `ValuationResult.alerts` — a contract change under section 66 stability, affecting Stage 9 consumers that parse alerts today. Regression risk is low for existing passing tests (new name is additive) but the two P2 tests will only pass once D1 *and* D2/D3 land together.

**6. Required inputs and definitions before implementation.** A flip definition (which status transitions qualify); the perturbation set (which inputs, joint or one-at-a-time); the perturbation magnitude and its versioning (see D9 — magnitudes must be Model Version Parameters per spec section 47); the severity mapping; and the interaction rule with existing divergence alerts (co-occurrence ordering).

**7. Required tests once approved.** Boundary tests at exactly the flip threshold (status changes vs. does not); adversarial cases — missing/NaN inputs, negative EPS, sign-change scenarios, zero target P/E, all-`None` scenarios (early-return path at `engine.py:476`); determinism (repeated runs); and a negative case asserting no flip alert when status is stable.

**8. Dependencies on other decisions.** Depends on **D2/D3** for precedence when multiple risk conditions co-occur; on **D8** for the emitted name; on **D9** for how the perturbation magnitude is versioned.

**9. What cannot safely be implemented before approval.** Any flip formula or magnitude. Specifically: do **not** reuse `SENSITIVITY_PERTURBATION = 0.10` as though it were the approved flip shock.

---

## D2 — Multiple Dependence

**1. Current verified behavior (evidence).** No multiple-dependence formula exists in spec or code. `high_dependence_share = 0.60` (`parameters.py:73`) is a **dead definition**: the only reference in all of `src` is its own declaration; no code reads it (verified P17, re-confirmed P19). `HIGH_MULTIPLE_DEPENDENCE` has zero references in `src/valuation`.

**2. Unanswered policy question.** What is "multiple dependence" measuring — the share of fair value attributable to the target-multiple component versus the EPS component, or sensitivity of fair value to multiple movement? Both are defensible readings of spec section 51 and they are **not the same metric**.

**3. Evidence-supported options (not recommendations).**
- **(a) Attribution share**: decompose `FV = EPS × target P/E` into the two multiplicative factors' contributions — directly computable from the existing identity (`_driver_analysis` already computes impact percentages for `{EPS, TARGET_PE}`, `engine.py:495`). The 0.60 threshold could then be applied to the `TARGET_PE` share.
- **(b) Sensitivity share**: fair-value elasticity to a multiple shock versus an EPS shock at equal perturbation — also derivable from existing one-at-a-time machinery.
- **(c) Documented non-implementation** until the metric is defined.
- Under (a) or (b), `high_dependence_share = 0.60` becomes *usable* — but only after the metric is defined; the threshold cannot be wired before then.

**4. Financial correctness risks / failure modes.** A multiplicative decomposition's shares are scale-invariant but not invariant to which factor is perturbed or to perturbation ordering. Denominator behavior is the live risk: with `total = max(sum(drivers.values()), 1e-9)` (`engine.py:489`) a degenerate near-zero denominator inflates shares arbitrarily. Missing data (one factor `None`) must return *no* metric rather than a misleading 100% share. High multiple dependence on a *cheap* company (below-target multiple) carries a different economic reading than on an expensive one — a single threshold conflates them.

**5. Contract / consumer / regression implications.** New public alert name (same section-66 considerations as D1). Because (a)/(b) reuse `_driver_analysis` outputs, a wrong choice risks retroactively re-interpreting the *already-shipped* driver-impact contract.

**6. Required inputs and definitions before implementation.** The metric definition (attribution vs. sensitivity); the denominator/missing-data rule; whether the 0.60 threshold applies and on which side; severity; interaction with D3 (EPS dependence) — both are "dependence" alerts and need a precedence rule.

**7. Required tests once approved.** Boundary cases at share = exactly 0.60 and 0.599/0.601; degenerate denominator; one factor `None`; both factors `None`; determinism; negative-case asserting no alert when the EPS share dominates.

**8. Dependencies.** **D3** (precedence between two dependence alerts), **D8** (name), **D9** (threshold versioning).

**9. What cannot safely be implemented before approval.** Wiring `high_dependence_share = 0.60` into any production path. The constant is currently inert; connecting it before the metric is defined would freeze an unapproved formula.


---

## D3 — EPS Forecast Dependence

**1. Current verified behavior (evidence).** No EPS-dependence formula exists. `HIGH_EPS_DEPENDENCE` has zero references in `src/valuation` (verified P17). No severity-escalation rule based on `forecast_reliability`, and no D2/D3 precedence rule. The name `FORECAST_RISK` appears in spec section 79 as an *alternative* to `HIGH_EPS_DEPENDENCE` but is defined nowhere and consumed nowhere (zero references in all of `src`). The forecast-reliability input *is* part of the contract: `forecast_reliability_score` is a `calculate_valuation` parameter, and `LOW_FORECAST_RELIABILITY` is already emitted (flag at `engine.py:163`, severity-bearing alert at `engine.py:514`).

**2. Unanswered policy question.** What constitutes "EPS dependence" — is it the share of fair value attributable to the EPS component (the mirror of D2), the *unreliability-weighted* EPS share, or the combination of high EPS share with low forecast reliability? And should the alert escalate or suppress when `LOW_FORECAST_RELIABILITY` already fires?

**3. Evidence-supported options (not recommendations).** The candidate metric grounded in the existing contract is the EPS attribution share from `_driver_analysis` (`engine.py:495`: `impact_pct` per driver) combined with the existing `forecast_reliability_score` input — no new data field is strictly required for a share-based definition. Naming choices, presented neutrally: **(a)** keep `HIGH_EPS_DEPENDENCE` as the single required name and treat `FORECAST_RISK` as an excluded alias (spec section 79 currently offers both); **(b)** make `FORECAST_RISK` a separate alert with a distinct trigger (e.g. reliability-driven) while `HIGH_EPS_DEPENDENCE` remains share-driven; **(c)** keep only `FORECAST_RISK` and retire `HIGH_EPS_DEPENDENCE`. None is selected. Note that section 79 lists the two names as alternatives without distinguishing their triggers — that ambiguity itself must be resolved.

**4. Financial correctness risks / failure modes.** Conflating *share* with *reliability* produces a single alert that cannot distinguish "fair value rests on EPS, and that EPS is trustworthy" from "fair value rests on EPS, and that EPS is a guess." A reliability-weighted metric needs an aggregation rule (multiplicative? threshold-conditional?) that no evidence currently supplies. Escalation stacking with `LOW_FORECAST_RELIABILITY` risks double-signaling the same underlying input.

**5. Contract / consumer / regression implications.** One or two new public alert names (section 66). Stage 9 consumers currently see neither name; whichever option is chosen, the vocabulary grows. Spec section 79's accept-result text must be rewritten to match the chosen option — a documentation consequence, not a code one.

**6. Required inputs and definitions before implementation.** The metric definition (share-only vs. reliability-weighted); the escalation/precedence rule with `LOW_FORECAST_RELIABILITY` and with D2; the naming decision; severity; and the missing-data rule (reliability `None` or clamped, cf. `_clamp_score` at `engine.py:490`).

**7. Required tests once approved.** Share at exactly the chosen threshold; reliability `None` and at boundaries (e.g. around `low_forecast_reliability = 40.0`); both dependence alerts co-occurring (precedence rule); determinism; negative case with EPS share low.

**8. Dependencies.** **D2** (precedence between two dependence alerts — spec section 51/52 ordering), **D8** (naming), **D9** (threshold/reliability-cutoff versioning).

**9. What cannot safely be implemented before approval.** Any EPS-share threshold, any reliability-escalation rule, and any decision on `FORECAST_RISK`.

---

## D4 — Margin Assumption Risk

**1. Current verified behavior (evidence).** `MARGIN_ASSUMPTION_RISK` has zero references in `src/valuation` (verified P17). **Stage 7 exposes no margin series anywhere in its contract**: the `calculate_valuation` signature (`engine.py:57-79`) takes price, EPS forecasts, benchmark P/E series, reliability, confidence, and quality scores — no margin, revenue, or cost input. `ValuationResult` (`schema.py:19-50`) exposes no margin field. This is a hard contract limitation, not a wiring gap.

**2. Unanswered policy question.** Should the margin assumption risk be supported at all in V1, and if so, where does the margin data come from?

**3. Evidence-supported options (not recommendations).**
- **(a) Explicit contract expansion**: add an observed margin-series input with provenance and validation (per-observation dating per D7). Highest correctness; requires upstream stages to supply a validated margin series, which is outside Stage 7's current boundary.
- **(b) A proxy metric** — only if the **owner** defines and approves one. No proxy exists in the code or spec, and none is proposed here; inventing one would fabricate financial policy.
- **(c) Documented non-implementation** pending a later decision. The alert remains absent and the spec records the gap (already done in P19's section 49 table: `MARGIN_ASSUMPTION_RISK` → **ABSENT**, D4 unresolved).

**4. Financial correctness risks / failure modes.** A proxy built from P/E or scenario data would import the assumptions it is meant to test — circular and audit-hostile. An undated margin series reintroduces lookahead risk (ties to D7).

**5. Contract / consumer / regression implications.** Option (a) changes the public `calculate_valuation` signature — a boundary change with consumer impact; options (b)/(c) do not. Under (c), `MARGIN_ASSUMPTION_RISK` stays absent from `alerts`/`valuation_risk_flags`.

**6. Required inputs and definitions before implementation.** Under (a): a defined margin series with provenance, a validation rule, and the risk formula. Under (b): an owner-approved proxy definition. Under (c): nothing further.

**7. Required tests once approved.** Under (a)/(b): missing-margin and stale-margin cases; margin sign changes; boundary at the risk threshold; determinism. Under (c): a negative test asserting the alert stays absent.

**8. Dependencies.** **D7** (margin provenance/dating), **D9** (formula versioning), **D8** (name).

**9. What cannot safely be implemented before approval.** Any margin formula, and any proxy. There is no evidence-supported proxy answer — this is stated directly rather than manufactured.

---

## D5 — High Impact Plus High Uncertainty

**1. Current verified behavior (evidence).** `HIGH_IMPACT_HIGH_UNCERTAINTY` has zero references in `src/valuation` (verified P17). However, the engine **already computes both ingredients** for the two-driver V1 chain: `driver_impact` (impact percentages, `engine.py:495`), `driver_uncertainty` (a blend, `engine.py:493`: `(100 - reliability)*0.5 + (100 - probability)*0.3 + (100 - quality)*0.2`), and `review_priority = impact × uncertainty / 100` (`engine.py:497`). These cover `{EPS, TARGET_PE}` **only**. The 0.10 perturbation and the 0.5/0.3/0.2 uncertainty weights are engine-chosen implementation constants — **not** approved financial policy.

**2. Unanswered policy question.** What defines "high impact" and "high uncertainty", how are they combined (product? joint-threshold?), and what triggers the alert?

**3. Evidence-supported options (not recommendations).**
- **(a) Apply the combination to the existing `{EPS, TARGET_PE}` driver set** — implementable now from existing outputs, with thresholds owner-specified. Scope limited to the V1 two-driver world.
- **(b) Defer until D6 lands** a complete sector-driver framework, then define impact/uncertainty per sector chain. Fuller, but blocked on D6.
- Note the split: **(a) is independently definable; (b) genuinely depends on D6.** The owner chooses scope, not just thresholds.

**4. Financial correctness risks / failure modes.** Reusing the 0.5/0.3/0.2 weights as policy would convert an implementation convenience into an audited financial invariant — exactly the laundering P22 exists to prevent. A product `impact × uncertainty` is dominated by whichever factor is normalized differently; a joint threshold requires two thresholds and an AND/OR rule. With only two drivers, "high impact" is nearly tautological (shares sum to 100%), so the trigger may carry little information until D6 widens the driver set.

**5. Contract / consumer / regression implications.** New public alert name (section 66). Under (a), `review_priority`'s existing semantics would be retroactively attached to an alert — consumers reading `review_priority` today would gain a new derived signal.

**6. Required inputs and definitions before implementation.** Definitions of impact and uncertainty in alert terms (not just as existing outputs); the combination rule; both trigger thresholds; scope choice (two-driver vs. sector chains); severity.

**7. Required tests once approved.** Impact/uncertainty each at exactly their thresholds and just inside/outside; both high (alert fires); one high (no alert); determinism; degenerate empty-driver path (`engine.py:477` early return).

**8. Dependencies.** **D6** (if sector-driver scope is chosen), **D8** (name), **D9** (threshold/weight versioning).

**9. What cannot safely be implemented before approval.** Any combination rule or thresholds; in particular, do not present the engine's 0.10 perturbation or 0.5/0.3/0.2 weights as approved policy.

---

## D6 — Sector-Specific Driver Chains and P/NAV

**1. Current verified behavior (evidence).** `_driver_analysis` (`engine.py:469-498`) hardcodes exactly two drivers: `drivers = {"EPS": eps_effect, "TARGET_PE": pe_effect}` (`engine.py:488`). There is **no branching on `industry_code`** — it is only echoed into metadata. `nav_per_share` is recorded in metadata as `nav_per_share_received` (`engine.py:247`) and consumed by **no** formula. `calculate_nav_fair_value` exists in `src/valuation/models.py` but is an **unwired export** (verified P17/P19/P20). Consequently `valuation_driver_ranking` is identical for a non-financial company, a bank, and a holding — proven by the failing test `test_p2_sector_driver_decomposition_missing`, which asserts `{"REVENUE", "NII", "NAV"} ⊆ observed` and finds only `{"EPS", "TARGET_PE"}`.

**2. Unanswered policy question.** How are the three required chains implemented, on what source fields, with which sector mapping — and does Stage 7 compute P/NAV fair value itself or consume it?

**3. Evidence-supported options (not recommendations).** This decision is not a choice between formulas but a build/buy/defer question: **(a)** implement the three chains as sector-branching driver analysis (requires new source fields and mappings); **(b)** defer to V2 with the current two-driver behavior documented (already recorded in P19's section 44 annotation). Under either option the three chains from spec sections 42-44 must be documented **separately**, per the prompt: *Non-financial*: Revenue → Operating Margin → Operating Profit → Net Profit → EPS → Fair Value; *Bank*: Loans/Deposits → NII/NIM → Net Profit → EPS → Fair Value; *Holding*: NAV → NAV Growth → Net Profit → EPS → Fair Value, with P/NAV assigned to Stage 7.

**4. Financial correctness risks / failure modes.** Every chain field except EPS and target P/E is **absent** from the current contract: no revenue, operating margin, loans/deposits, NII/NIM, or NAV-growth input exists in `calculate_valuation` or `ValuationResult`. Rebuilding EPS inside Stage 7 from a new share count would **violate the explicit rule** that Stage 7 must consume Stage 5 EPS forecasts (spec section 58) — a lookahead and consistency hazard. Any invented industry-code mapping would be fabricated taxonomy. The `NAV` chain is the most tractable (a `nav_per_share` parameter already reaches the engine) yet is still unused.

**5. Contract / consumer / regression implications.** Option (a) changes `valuation_driver_ranking`'s content — a **public contract output** (spec section 69) that Stage 9 and dashboards consume; ranking values would become sector-dependent. `calculate_nav_fair_value` activation would change fair-value outputs for holdings. This is the largest single contract change among D1-D9.

**6. Required inputs and definitions before implementation.** Source fields for each chain (revenue, operating margin, loans/deposits, NII/NIM, NAV growth); an **owner-approved** industry-code → sector mapping (does not exist in the project — the subagent's taxonomy check for this did not complete); per-chain sensitivity formulas; the Stage 5 EPS-consumption validation rule; and a decision on P/NAV (compute vs. consume).

**7. Required tests once approved.** One chain per sector with correct ranking; mixed/unknown industry code; missing chain inputs (partial fields); NAV = 0 or negative; determinism; and the two P2 tests would need re-baselining **only after** a decision — not before.

**8. Dependencies.** **D7** (chain input provenance), **D9** (formula versioning), **D8** (if new driver names enter alerts). D6 in turn **unblocks** D5's sector scope.

**9. What cannot safely be implemented before approval.** Any industry mapping, any chain formula, and any wiring of `nav_per_share` or `calculate_nav_fair_value`.


---

## D7 — Point-in-Time Enforcement

**1. Current verified behavior (evidence).** The Stage 7 boundary does **not** enforce PIT correctness. Benchmark series (`historical_pe_values`, `industry_forward_pe_values`, `industry_ttm_pe_values`) enter `calculate_valuation` (`engine.py:70-72`) as **bare floats with no dates**. `valuation_date` and `data_cutoff_datetime` are only normalized and echoed (`engine.py:104-108`); **no comparison** between them occurs. `metadata["pit_inputs_required"] = True` (`engine.py:248`) is an informational marker, not an enforcement. The failing test `test_p6_cutoff_pit_limitation_pinned` pins the silent acceptance of a post-cutoff date. No production caller supplies the six PIT-related inputs (finding P13, still standing). The spec requires per-date observance of Price Date, Forecast Cutoff, Report Publication Date, Report Version, and Historical EPS Availability (sections 56-57).

**2. Unanswered policy question.** Which enforcement policy applies, and on which temporal fields — provenance on every observation, caller attestation, or a documented limitation?

**3. Evidence-supported options (not recommendations).** For each: contract changes, enforcement strength, auditability, migration/consumer impact, residual lookahead risk.
- **(a) Per-observation provenance with explicit enforcement**: every benchmark series carries an observation date; the engine rejects or downgrades any observation dated after the valuation date / cutoff. *Contract:* the `calculate_valuation` signature must accept dated series (breaking change, or additive optional fields). *Strength:* highest — violations caught at the boundary. *Auditability:* strong — each input is self-evidencing. *Migration:* heaviest — every caller must supply dates. *Residual risk:* low, provided report publication date/version are also dated (they are not currently inputs at all).
- **(b) Caller/upstream attestation with a precisely specified ordering/validation rule**: callers assert cutoff compliance; Stage 7 validates the assertion's form (not its truth). *Contract:* smaller (an attestation field). *Strength:* moderate — does not detect upstream error. *Auditability:* depends on the attestation record's durability. *Migration:* light. *Residual risk:* moderate-to-high — a false attestation is undetectable downstream.
- **(c) A documented V1 limitation**: Stage 7 records that PIT safety is the caller's/upstream's responsibility and the spec marks section 85 NOT-APPLICABLE in V1 (largely the state P19 left the spec in). *Contract:* none. *Strength:* none. *Auditability:* weak. *Migration:* none. *Residual risk:* highest — lookahead contamination of backtests is uncaught.
- **Metadata alone does not enforce PIT correctness.** `pit_inputs_required` asserts a requirement without testing it; it must not be represented as enforcement under any option.

**4. Financial correctness risks / failure modes.** The dominant failure mode is lookahead: a revised or late-published report used in a historical backtest inflates apparent performance. This is the most consequential creditability issue in the entire D1-D9 set (P17's C-04). A date-ordering rule that compares the wrong pair (e.g. cutoff vs. valuation date when the binding constraint is publication date) gives false assurance.

**5. Contract / consumer / regression implications.** Option (a) changes the public signature — the largest boundary change alongside D6. Option (b) adds a field. Option (c) leaves code untouched. Under (a)/(b), existing callers (including any Stage 9 path) must be migrated; under (c), backtests remain caller-responsible.

**6. Required inputs and definitions before implementation.** The temporal contract: which fields are dated (valuation date, data cutoff, report publication date/version, benchmark observation dates, historical EPS availability), the ordering rule among them, and the violation response (reject, downgrade, or flag — the last being a `POINT_IN_TIME_WARNING`, whose trigger is itself undefined and gated here).

**7. Required tests once approved.** Post-cutoff observations rejected/downgraded as specified; date-equal boundary cases; missing dates; future-dated valuation; determinism; and a negative case proving pre-cutoff data passes untouched.

**8. Dependencies.** **D6** (sector chain inputs also need provenance), **D9** (version selection is meaningless without a temporal contract), **D8** (`POINT_IN_TIME_WARNING` trigger).

**9. What cannot safely be implemented before approval.** Any date-ordering policy, any rejection rule, and any claim that current metadata provides PIT safety.

---

## D8 — Alert Names and Trigger Semantics

**1. Current verified behavior (evidence).** The spec mandates 13 alert names (section 49); the engine emits a different vocabulary (verified P17/P19/P20):
- `VALUATION_BENCHMARK_DIVERGENCE` (spec) vs. `WATCH:VALUATION_ABOVE_TARGET_PE` / `WATCH:VALUATION_BELOW_TARGET_PE` (engine, `engine.py:519-522`).
- `HISTORICAL_VALUATION_DIVERGENCE` vs. `WATCH:FORWARD_PE_ABOVE/BELOW_HISTORICAL` (`engine.py:523-527`).
- `INDUSTRY_VALUATION_DIVERGENCE` vs. `WATCH:FORWARD_PE_ABOVE/BELOW_INDUSTRY` (`engine.py:528-532`).
- `INSUFFICIENT_PEER_DATA` ≠ `INDUSTRY_BENCHMARK_INSUFFICIENT`: the former fires when forward values exist and valid forward peers `< MIN_INDUSTRY_PEERS = 8` (`engine.py:164-165`); the latter fires only when `target_source == "INSUFFICIENT_DATA"` (`engine.py:168-169`, i.e. no usable benchmark at all). A 7-peer case with a valid historical median emits the first but **not** the second (P21's section 55 refinement records this precisely).
- **Flag-level vs severity-bearing**: `INSUFFICIENT_PEER_DATA`, `NEGATIVE_EPS`, `SIGN_CHANGE` are emitted only in `valuation_risk_flags`, not as severity-bearing `alerts`; a flag without severity is not equivalent to a severity-bearing alert.
- **Missing trigger definitions**: `POOR_DATA_QUALITY` has no trigger in the spec and zero code references; `POINT_IN_TIME_WARNING` has zero code references and its trigger is gated on D7.

**2. Unanswered policy question.** Rename engine outputs, alias them, or adopt current names in the spec — and does flag-level emission satisfy the section 49 "alert capability"?

**3. Evidence-supported options (not recommendations).**
- **(a) Rename** engine outputs to the spec names. *Contract stability:* poor — breaks any consumer parsing current names (Stage 9 consumes these outputs today). Also collapses the above/below pairs (two signals with opposing economics become one), losing direction information.
- **(b) Alias** both names so each emission carries spec and current names. *Stability:* good — backwards compatible. *Cost:* duplicated vocabulary across two channels, with no defined severity for the alias form.
- **(c) Adopt current names in the spec** (amend sections 49/54-55 to the emitted vocabulary). *Stability:* best for consumers; requires accepting the loss of the mandated names and rewriting sections 49/54-55/77-79's expected-result blocks.
- The flag-vs-alert sufficiency question is orthogonal to all three and must be decided separately.

**4. Financial correctness risks / failure modes.** Merging above/below destroys directional signal — a divergence *above* target and *below* target carry opposite implications. Promoting flags to severity-bearing alerts without a defined severity produces unrankable output. A rename performed without a coordinated consumer migration causes silent alert-dropage downstream.

**5. Contract / consumer / regression implications.** This is the decision with the broadest consumer surface: `alerts` and `valuation_risk_flags` are public outputs (spec section 69) read by Stage 9 (`test_stage9_decision.py` passes today — 13/13 — so any rename must be validated there). Section 66 contract stability makes a rename a versioned contract change, not a silent one.

**6. Required inputs and definitions before implementation.** The chosen strategy; the full mapping table (already drafted in P19's sections 49/54-55 annotations, which record mismatches without choosing); severity definitions for any promoted flag; and a `POOR_DATA_QUALITY` trigger definition.

**7. Required tests once approved.** Every alert name asserted present/absent as chosen; above/below both exercisable and distinguishable; Stage 9 consumer tests re-run; a compatibility test if aliasing; negative cases for each trigger.

**8. Dependencies.** Unblocks clean expression of **D1, D2, D3, D4, D5** (all emit new names) and **D7** (`POINT_IN_TIME_WARNING`).

**9. What cannot safely be implemented before approval.** Any rename, alias, flag promotion, or spec amendment of the mandated names.

---

## D9 — Parameter Registry and Version Selection

**1. Current verified behavior (evidence).** All thresholds are **fixed constants** in `src/valuation/parameters.py`: `VALUATION_THRESHOLDS` (8 status thresholds), `CONFIDENCE_THRESHOLDS`, `RISK_THRESHOLDS`, `ALERT_THRESHOLDS` (incl. `high_dependence_share = 0.60`, unused), `SENSITIVITY_PERTURBATION = 0.10`, `MIN_INDUSTRY_PEERS = 8`, plus `MODEL_VERSION = "STAGE7_V1"` and `CONTRACT_VERSION = "VALUATION_CONTRACT_V1"`. `effective_from` and `parameter_version` have **zero references** in all of `src` (verified P17/P19). Spec section 65 mandates a five-field record store (`valuation_model_parameters`: model_version, parameter_name, parameter_value, effective_from, description) that **does not exist**. P14 proposed an in-code registry ("Option A") as a proposal — **not approved**.

**2. Unanswered policy question.** Which registry mechanism, and how is the effective version selected at query time (`as_of`)?

**3. Evidence-supported options (not recommendations).**
- **(a) Structured in-code registry**: a versioned constant structure with effective dates in `parameters.py`. *Auditability:* good (version-controlled, reviewable). *Reproducibility:* good for current runs. *Effective-date selection:* requires an `as_of` rule — unresolved. *Testability:* straightforward. *Cross-stage coupling:* low. *Migration:* minimal. *Backtest safety:* weak — historical runs re-execute against *current* constants unless the caller pins a version, so historical valuations are not reproducible as-of.
- **(b) Persistent database-backed registry**: the section 65 five-field table. *Auditability:* strongest. *Reproducibility:* strongest (true as-of selection). *Effective-date selection:* native to the schema. *Testability:* requires DB fixtures. *Cross-stage coupling:* high (a shared schema object). *Migration:* heaviest (new table, dependencies, migration). *Backtest safety:* strongest.
- **(c) Another versioning approach only if project-supported**: no alternative mechanism has project evidence; the only candidate artifacts are the existing fixed constants (which is the status quo, not a registry). This option therefore has **no evidence-supported instantiation** and is reported as empty rather than invented.

**4. Financial correctness risks / failure modes.** Without as-of selection, any threshold change silently re-writes history — a backtest's results become a moving target, destroying the auditability the versioning requirement exists to protect. A registry without a selection rule is documentation, not versioning.

**5. Contract / consumer / regression implications.** (a) keeps the public surface stable. (b) adds a schema object and dependency, and changes how every consumer resolves parameters. Under both, `MODEL_VERSION` semantics deepen from a static label to a version key.

**6. Required inputs and definitions before implementation.** The mechanism choice; the `as_of` rule — **explicitly unresolved**: valuation date, data cutoff, or another policy cannot be chosen without owner approval and a clear temporal contract (this ties directly to D7, whose temporal contract is also unresolved — the two are mutually dependent). Also: the parameter inventory to version (spec sections 47/64 list formulas, thresholds, priors, and sensitivity parameters).

**7. Required tests once approved.** As-of selection across a known version boundary; parameter changes effective on the correct date and not before; determinism given a pinned version; DB-roundtrip tests under (b).

**8. Dependencies.** **D7** (the temporal contract defines what `as_of` means), and in turn D9 supplies versioning for **D1-D6**'s formulas and thresholds.

**9. What cannot safely be implemented before approval.** Any registry, and any `as_of` policy.


---

## Prioritization — Proposed Discussion Sequence

This is a **proposed discussion sequence for the owner**, not an approved implementation plan. No decision is resolved by this ordering, and none should be inferred as already settled.

1. **D8 (alert names and trigger semantics) — first.** It fixes the vocabulary that D1, D2, D3, D4, D5, and D7 all emit into. Deciding it last means every alert decision is expressed in a name that may be renamed. It also has the widest consumer surface, so its cost should be confronted before, not after, alert features are built on top.
2. **D6 (sector chains and P/NAV) — second.** It unblocks the largest body of work: D5's sector scope, the `REVENUE`/`NII`/`NAV` chains the two failing P2 tests assert, and the activation of the already-present `calculate_nav_fair_value`. It is also the largest contract change, so its scope decision frames everything downstream.
3. **D1 → D2 → D3 — together, in that order.** These are the three dependence/risk alerts with a shared precedence question. D1 defines the perturbation vocabulary D2/D3 can reuse; D2 and D3 need their precedence rule decided jointly; D3's naming question (`FORECAST_RISK`) depends on D8.
4. **D4 — parallel, low dependency.** Its most evidence-supported option right now is documented non-implementation (no margin series exists in the contract), so it can be resolved cheaply while the others proceed.
5. **D7 and D9 — paired, last.** They are mutually dependent: D9's `as_of` rule needs D7's temporal contract, and D7's enforcement needs D9's versioning to be auditable. Both are infrastructure with the heaviest migration cost; deciding them after the feature set is stable avoids re-specifying a temporal contract twice.

**Rationale:** decisions that change vocabulary (D8) and contract shape (D6, D7) precede decisions that fill in formulas (D1-D5), because formulas are expressed *in* the vocabulary and *on* the contract.

**Documentation-only work that remains safe regardless of policy decisions** (identified, **not** implemented here): the remaining stress-test PASS claims in sections 71-76 and 80-84 sit outside the P19/P21 scope and were never audited for overclaims — checking them is purely factual work requiring no policy choice. Also, recording that `POOR_DATA_QUALITY` has no trigger definition (already noted) and maintaining the P19 annotation set as decisions land. None of this is implemented in this prompt.

---

## Six-Layer Validation

**1. Unit/formula.** Static review only. Inspected the formulas relevant to each decision: `calculate_forward_pe_fair_value` (the shipped `FV = EPS × target P/E` identity), `_driver_analysis` (`engine.py:469-498`, including the `drivers = {"EPS", "TARGET_PE"}` hardcode, the `max(sum, 1e-9)` denominator guard, and the `review_priority` product), `_alerts` (`engine.py:500-535`), `_select_target_pe` (`engine.py:256-269`), and the flag block (`engine.py:164-169`). **No new formulas were created.** Undefined formulas identified: D1 (flip), D2 (dependence share), D3 (EPS share / escalation), D5 (impact×uncertainty combination + thresholds), D6 (per-chain sensitivity), D7 (date ordering). No tests were executed for this layer — the task is read-only and no claim required execution.

**2. Contract/boundary.** Static inspection of `ValuationResult` (`schema.py:19-50`) and the `calculate_valuation` signature (`engine.py:57-79`). Precise contract changes each option would require: D1/D2/D3/D4/D5 add alert **names** to `alerts`/`valuation_risk_flags` (additive but versioned under section 66); D4(a) and D7(a) **change the input signature** (the only boundary-breaking options); D6(a) changes the **content** of the public `valuation_driver_ranking` output and activates `calculate_nav_fair_value`; D8(a) changes emitted names (breaking), D8(b) additive, D8(c) spec-only; D9(a) surface-stable, D9(b) adds a schema object. No contract change was made — all are described as options.

**3. Production-path/integration.** Traced the relevant call path: `calculate_valuation` → `_select_target_pe` → flag block → `_driver_analysis` → `_alerts` → `ValuationResult` construction (`engine.py:201-250`), with `MODEL_VERSION`/`CONTRACT_VERSION`/`calculation_timestamp` set at `engine.py:211-212, 231`. Stage 9 consumer dependency confirmed by the passing `src/tests/test_stage9_decision.py` (13 passed, carried forward from P20/P21) — establishing that Stage 9 reads Stage 7's public outputs today, which is why D8 and D6 carry real consumer-compatibility risk. No runtime path was modified.

**4. Adversarial/negative.** Enumerated cases that **must be tested once a policy is approved** — these are requirements for future test suites, **not** results claimed as executed:
- *Missing data:* `None` inputs, empty driver set (`engine.py:477` early return), degenerate denominator (`max(sum, 1e-9)` at `engine.py:489`), reliability `None` vs. clamped (`_clamp_score` at `engine.py:490`).
- *Stale/future data:* post-cutoff benchmark observations (PIT), future-dated valuation — only meaningful once D7 lands.
- *Sign changes:* negative EPS, `NEGATIVE_EPS`/`SIGN_CHANGE` flag interaction with `NOT_APPLICABLE` status (`engine.py:197-199`), NAV ≤ 0 under D6.
- *Threshold boundaries:* exactly at 0.60 (D2), at the reliability cutoff 40.0, at the divergence ratios 1.50, and at whatever D1/D5 thresholds the owner sets — including just-inside/just-outside pairs.
- *Consumer compatibility:* Stage 9 parsing under each D8 option; alert-vocabulary regressions under renames.
None of these were executed in P22.

**5. Regression/full suite.** No tests were executed in this prompt — none of the decision-brief claims required execution, and the brief is documentation-only. Counts are **carried forward, freshly labeled as such**: Stage 7 = 50 passed / 2 failed (the known P2 tests, pre-existing and expected); Stage 9 = 13 passed; last full-suite run (P19) = 1031 passed / 2 failed / 1 skipped in 293s. The two failures are **not** new regressions. No test was treated as passing because it was skipped or excluded.

**6. Independent audit.** All nine decision sections were cross-checked against P11-P21, the specification, and the code. Consistency findings: every "current behavior" claim re-verified against the same engine/parameters/schema locations cited in P17/P19/P20/P21; the D8 mismatch list matches the P19 section 49/54-55 annotations and the P21 section 55 refinement; the D2 dead-constant claim matches P17/P19 (single reference, `parameters.py:73`); the D6 unwired-export claim matches P17/P19/P20. **No decision is implicitly selected by wording** — each section presents options as options, separates them from any recommendation, and states what cannot be implemented before approval. One caveat recorded honestly: the D6 industry-code taxonomy check that the failed subagent was attempting did not complete, so D6 asserts only that **no** owner-approved mapping exists in the project (verified) and does not characterize candidate taxonomies.

---

## Compact Decision Table

| Decision | Evidence-Supported Options | Dependencies | Contract Impact |
|---|---|---|---|
| **D1** Flip risk | (a) reuse 0.10 OAT perturbation; (b) dedicated owner-specified flip set; (c) status-transition-class only | D2/D3 (precedence), D8 (name), D9 (magnitude versioning) | New alert name (additive, versioned) |
| **D2** Multiple dependence | (a) attribution share from existing decomposition; (b) sensitivity share; (c) documented non-implementation | D3 (precedence), D8, D9 | New alert name; risk of re-interpreting shipped driver-impact contract |
| **D3** EPS dependence | Metric: EPS share (optionally reliability-weighted). Naming: (a) `HIGH_EPS_DEPENDENCE` only; (b) both names, distinct triggers; (c) `FORECAST_RISK` only | D2 (precedence), D8 (naming), D9 | One or two new alert names; spec section 79 rewrite |
| **D4** Margin assumption | (a) contract expansion with provenance; (b) owner-approved proxy (none exists); (c) documented non-implementation | D7 (provenance), D9, D8 | (a) changes input signature; (b)/(c) none |
| **D5** Impact × uncertainty | (a) apply to existing `{EPS, TARGET_PE}` set; (b) defer until D6 sector chains | D6 (for scope b), D8, D9 | New alert name; attaches to existing `review_priority` |
| **D6** Sector chains + P/NAV | (a) implement three sector chains; (b) defer to V2 (current two-driver documented) | D7 (input provenance), D9, D8; **unblocks** D5 | Largest: changes `valuation_driver_ranking` content; activates `calculate_nav_fair_value` |
| **D7** PIT enforcement | (a) per-observation provenance; (b) caller attestation; (c) documented V1 limitation | D9 (`as_of`), D6, D8 (`POINT_IN_TIME_WARNING`) | (a) changes input signature; (b) adds field; (c) none |
| **D8** Alert names/triggers | (a) rename to spec names; (b) alias both; (c) adopt engine names in spec; plus flag-vs-alert sufficiency (orthogonal) | Unblocks D1-D5, D7 | Broadest consumer surface; Stage 9 parses these outputs today |
| **D9** Parameter registry | (a) in-code registry; (b) DB-backed five-field table (spec section 65); (c) no evidence-supported alternative exists | D7 (temporal contract for `as_of`); supplies D1-D6 | (a) surface-stable; (b) new schema object + dependency |

---

## Exact Unresolved Items Still Requiring Owner Approval

- **D1:** flip definition; perturbation set and magnitude (no spec/code value exists — must be *decided*, not discovered); severity mapping; interaction with divergence alerts.
- **D2:** the metric definition itself (attribution vs. sensitivity share); denominator/missing-data rule; whether 0.60 applies and on which side; precedence vs. D3.
- **D3:** the metric (share-only vs. reliability-weighted); the escalation/precedence rule with `LOW_FORECAST_RELIABILITY`; the `FORECAST_RISK` naming decision.
- **D4:** whether to support margin risk at all in V1; if so, the margin-series source and provenance, or an owner-defined proxy. No proxy exists and none is proposed.
- **D5:** definitions of "high impact" and "high uncertainty"; combination rule; both thresholds; scope (two-driver now vs. sector chains after D6).
- **D6:** the industry-code → sector mapping (does not exist in the project); per-chain source fields and formulas; the Stage 5 EPS-consumption validation rule; the P/NAV compute-vs-consume decision.
- **D7:** the enforcement policy; the full temporal contract (which fields are dated, the ordering rule, the violation response); the `POINT_IN_TIME_WARNING` trigger definition.
- **D8:** the naming strategy (rename / alias / spec adoption); whether flag-level emission satisfies section 49's alert capability; the `POOR_DATA_QUALITY` trigger definition.
- **D9:** the registry mechanism; the `as_of` selection rule (valuation date vs. data cutoff vs. another policy); the parameter inventory to version.

Additionally, an unaddressed documentation-only item sits outside the policy decisions: stress-test PASS claims in sections **71-76 and 80-84** were never audited (outside P19/P21 scope) and may contain overclaims analogous to those corrected in 77-79/85.

---

## Confirmation

- **No implementation or policy choice was made.** No D1-D9 decision was selected, explicitly or implicitly; every option is presented as an option and separated from any recommendation.
- No formulas, thresholds, severities, industry mappings, dates, or defaults were invented. Where no evidence-supported answer exists (D1 magnitudes, D4 proxy, D9 alternative mechanism), that is stated directly.
- No source, test, schema, spec, dependency, migration, or configuration file was modified — this brief is appended to `temp_report2.md` only, and no prior content was overwritten.
- No tests were executed; all test counts are carried forward and labeled as such. No carried-forward result is presented as freshly executed, and no skipped/excluded test is treated as passing.
- No remote Git operations were performed (no commits, pushes, pulls, or branch changes).
- **Stage 7 remains unfrozen.** No stage was frozen. Work stops after appending this report.
============================================================================







============================================================
# P23 — Stage 7 Remaining Stress-Test PASS Claims Audit Report

**Date (UTC):** 2026-10-13
**Nature:** READ-ONLY AUDIT of the remaining PASS claims in sections 71-76 and 80-84 of `07_Stage7_Valuation.md`. No source code, test, schema, specification, dependency, migration, or configuration file was modified. No D1-D9 decision was selected or inferred. No formula, threshold, severity, mapping, date, or default was invented.
**Evidence base:** `temp_report2.md` (P17-P22); `07_Stage7_Valuation.md` (sections 71-76, 80-84, plus only the directly referenced requirements: sections 6, 10, 13, 14, 15, 17, 21-29, 34-39, 48-49, 54-55, 60, 69); `src/valuation/engine.py`, `models.py`, `parameters.py`, `schema.py`; `src/tests/test_stage7_valuation.py`; `src/forecast/repo.py` and `src/tests/test_stage5_forecast.py` (reached only for section 83, whose claim points outside `src/valuation`).

---

## Audit Method Note

The ten audited sections are stress-test *claims*, not test reports. For each, the audit asked four questions in order: (a) does code exist that would produce the claimed behavior; (b) is there an **executed** test or reproducible fixture demonstrating it; (c) is the claim's literal output vocabulary actually emitted, or does the claim paraphrase an engine output under a spec-only name; (d) where the claim asserts a *capability* ("X is possible"), is there any wiring that makes X reachable at all. Only (a) plus (b) can support a PASS label. A claim that holds vacuously — because a required input does not exist on the engine boundary — is reported as such, not as passing.

A recurring pattern drives most of the verdicts below: the *negative* half of each claim (the system must not do the wrong thing) is genuinely enforced by code and by tests, while the *positive* half (the system can produce the named signal) has no input path, no formula, or no emitted name. Sections 77-79 and 85 were corrected in P19 for exactly this reason; sections 80-84 repeat the pattern in a milder form, and section 82 is the clearest instance.

---

## Section-by-Section Audit Table

| Sec | Claimed behavior | Implementation evidence | Test evidence | Verdict | Minimal correction | D1-D9 |
|---|---|---|---|---|---|---|
| **71** | Cheap company (price << fair value, positive EPS, valid benchmark, adequate reliability) must become `ATTRACTIVE` or `VERY_ATTRACTIVE` | `_valuation_status` (`engine.py:409-419`) grades expected + base upside against `VALUATION_THRESHOLDS` (`parameters.py:41-50`); fair value from `calculate_forward_pe_fair_value` (`models.py:12-16`) | **Executed.** `test_valuation_engine_forward_pe_and_expected_fair_value` (line 35) asserts `ATTRACTIVE` on this exact shape; `test_p6_regression_prior_behavior_preserved` (line 1060) pins it as golden. Fresh probe reproduced `VERY_ATTRACTIVE` under a cheap-price case | **SUPPORTED** | None — one of two fully evidenced claims | None |
| **72** | Very low forward P/E but low reliability: system must not call it `VERY_ATTRACTIVE` alone; `ATTRACTIVE` + `LOW CONFIDENCE` + forecast-risk warning must be possible | **Positive half not implemented as worded.** Reliability is *not* an input to status: `_valuation_status` reads only the two upside figures. Status is degraded only via dispersion, never via reliability. Reachable combination is `ATTRACTIVE` + `valuation_confidence_label = LOW/VERY_LOW` + `WARNING:LOW_FORECAST_RELIABILITY`. There is **no** forecast-risk warning name (sec 79 / D3). Negative half holds: reliability provably cannot change fair value or P/E | **Partially executed.** Reliability alert boundaries pinned by `test_p2_alert_low_reliability_threshold_boundaries` (line 308: 39.9 fires, 40.0 does not). Fresh probe reproduced `ATTRACTIVE` + `VERY_LOW` + `WARNING:LOW_FORECAST_RELIABILITY` at reliability 20.0. No test covers the claim's own stated combination | **PARTIALLY SUPPORTED** | Reframe to the reachable form: status is computed from upside alone; low reliability surfaces only through `valuation_confidence` / `valuation_confidence_label` and the `WARNING:LOW_FORECAST_RELIABILITY` alert, and is not a status input. Strike "FORECAST RISK WARNING" or mark it as the unresolved D3 name, since `FORECAST_RISK` is emitted nowhere | **D3**, **D8** |
| **73** | `EPS < 0` must give `Forward P/E = NULL`, `P/E Valuation = NOT_APPLICABLE`, with no artificial fair price | Fully implemented. `calculate_forward_pe` returns None for `eps <= 0` (`models.py:5-9`); `calculate_forward_pe_fair_value` likewise (`models.py:12-16`); `_eps_flags` emits `NEGATIVE_EPS`/`NOT_APPLICABLE` (`engine.py:363-371`); status forced to `NOT_APPLICABLE` when expected FV is None (`engine.py:197-199`) | **Executed.** `test_negative_eps_does_not_create_fake_pe_or_fair_value` (line 95) asserts every element; `test_p6_invalid_eps_variants_never_fabricate_values` (line 1006) extends to zero/NaN/None; `test_p5_missing_eps_is_not_applicable_not_zero` (line 711) covers missing EPS | **SUPPORTED** | None. Optional: the claim stops at `EPS < 0` while the guard also covers `EPS = 0` and missing EPS, so it under-describes the implementation | None |
| **74** | `Valid Peers < 8` must give `Industry Forward P/E = INSUFFICIENT_DATA` and fall back to Historical Median | **Implemented, but the claim names the wrong field.** With 7 peers, `industry_forward_pe_median` is the median of the 7 (6.0), not `INSUFFICIENT_DATA` — the median is computed regardless of count (`engine.py:92`). What actually becomes `INSUFFICIENT_DATA` is `target_pe_source`: `_select_target_pe` (`engine.py:256-269`) requires `forward_peer_count >= MIN_INDUSTRY_PEERS = 8`, else falls to `HISTORICAL_MEDIAN_PE`. `INSUFFICIENT_PEER_DATA` is flagged separately (`engine.py:164-165`); only when *no* benchmark is usable does `target_pe_source` become `INSUFFICIENT_DATA` | **Executed.** `test_industry_forward_pe_requires_eight_valid_peers` (line 67), `test_p4_peer_count_below_minimum_falls_back` (line 581), `test_p4_peer_count_at_minimum_selects_industry_forward` (line 594), `test_p4_benchmark_fallback_ignores_forward_count_for_ttm` (line 649) | **PARTIALLY SUPPORTED** | Replace the `Industry Forward P/E = INSUFFICIENT_DATA` line with: the industry-forward benchmark is *rejected for selection* (`target_pe_source` falls back to `HISTORICAL_MEDIAN_PE`) and `INSUFFICIENT_PEER_DATA` is flagged, while `industry_forward_pe_median` still reports the median of the available peers. Cite the P21 section-55 refinement, which documents this same 7-peer case | **D8** (peer-count trigger vs `INDUSTRY_BENCHMARK_INSUFFICIENT` — already recorded in sec 55) |
| **75** | Current forward P/E far from the historical median must raise a Historical Valuation Divergence alert | **Implemented under a different name.** `_alerts` emits `WATCH:FORWARD_PE_ABOVE_HISTORICAL` / `WATCH:FORWARD_PE_BELOW_HISTORICAL` when `forward_pe / historical_median >= 1.50` or the inverse (`engine.py:523-527`, threshold `historical_divergence_ratio = 1.50`). The spec name `HISTORICAL_VALUATION_DIVERGENCE` is **never emitted** — the same name-mismatch class P19/P21 recorded for sections 49/54-55 | **Executed.** `test_p2_alert_divergence_ratios_boundaries` (line 366) covers both directions plus the just-below boundary; fresh probe at forward P/E 10 vs median 3.0 reproduced `WATCH:FORWARD_PE_ABOVE_HISTORICAL` | **PARTIALLY SUPPORTED** | Add the existing section 54 name-mapping annotation by reference: the capability exists, the emitted names are the `WATCH:FORWARD_PE_ABOVE/BELOW_HISTORICAL` pair, and `HISTORICAL_VALUATION_DIVERGENCE` is the spec-only name. No new decision is required | **D8** (already open, unchanged) |
| **76** | Scenario probabilities `20/60/20` must sum to 100%, and expected fair value must be the correct weighted average | Fully implemented. `_resolve_probabilities` normalizes any input to sum to 1 (`engine.py:305-310`); `_expected_fair_value` computes the probability-weighted sum over all three scenarios and requires exactly three non-None fair values (`engine.py:391-396`); `metadata["scenario_probability_sum"]` reports the sum (`engine.py:242`) | **Executed.** Sum asserted in `test_valuation_engine_forward_pe_and_expected_fair_value` (line 58), `test_probability_evidence_is_family_level_and_equal_weighted` (line 142), `test_p6_scenario_ordering_flag_and_probability_normalization` (line 988); determinism by `test_p6_repeat_runs_identical_on_full_contract` (line 1035). Fresh probe: sum = 1.0, expected FV = 1260.0, matching the weighted average | **SUPPORTED** | None | None |


# P23 — Stage 7 Remaining Stress-Test PASS Claims Audit Report

**Date (UTC):** 2026-10-14
**Nature:** READ-ONLY AUDIT. No source code, test, schema, specification, dependency, migration, or configuration file was modified. No D1-D9 policy decision was chosen or inferred. No formulas, thresholds, severities, mappings, dates, or defaults were invented. The only write is this report, appended to `temp_report2.md`.

**Scope:** Sections 71-76 and 80-84 of `07_Stage7_Valuation.md` — the remaining `PASS.` claims that P19/P21 corrected (77, 78, 79, 85) but P22 flagged as never audited. Evidence base: `temp_report2.md` (P17-P22); `07_Stage7_Valuation.md` sections 4-15, 22-31, 34, 48-49, 54-55, 69, 71-76, 80-84; `src/valuation/engine.py`, `models.py`, `parameters.py`, `schema.py`; `src/tests/test_stage7_valuation.py`; `src/forecast/repo.py` (revision_trend); `src/decision/engine.py` (revision consumer).

**Method:** For each section — (1) identify the claimed result; (2) locate the implementation function and contract; (3) determine implemented / partial / absent / unverifiable; (4) verify the PASS is backed by an executed test or only a spec assertion; (5) note missing negative/boundary/missing-data/determinism/integration checks; (6) recommend the smallest factual correction; (7) separate documentation corrections from owner-decision items. Behaviors marked "probed" below were executed with the project interpreter (`.venv/Scripts/python.exe`, `-I` isolated mode) against `ValuationEngine.calculate_valuation`.

---

## Audit Table

| Section | Claimed Behavior | Implementation Evidence | Test Evidence | Verdict | Minimal Documentation Correction | D1-D9 Dependency |
|---|---|---|---|---|---|---|
| **71** Cheap Company | Truly cheap company (price « fair value, positive EPS, valid benchmark, adequate reliability) → `ATTRACTIVE` or `VERY_ATTRACTIVE` | `_valuation_status` (engine.py:409-419) maps expected/base upside against `VALUATION_THRESHOLDS` (parameters.py:41-50); benchmark from `_select_target_pe` (engine.py:256-269). Probe: price 1000 vs fair value 3600 → status `VERY_ATTRACTIVE`, MOS 260% | No dedicated S71 test; behavior pinned by general engine tests: `test_valuation_engine_forward_pe_and_expected_fair_value` (asserts `ATTRACTIVE`), `test_p10_expensive_base_upside_parameterized_outputs_unchanged`, `test_p6_regression_prior_behavior_preserved` | **SUPPORTED** | None required. Optional note: thresholds are engine constants, not spec-ratified (already annotated in section 48; D9). | None (threshold provenance is D9, already annotated) |
| **72** Low P/E / Poor Reliability | Very low forward P/E with low reliability must not declare merely Very Attractive; "something like ATTRACTIVE + LOW CONFIDENCE + FORECAST RISK WARNING" possible | Low reliability raises `LOW_FORECAST_RELIABILITY` flag (engine.py:163) + `WARNING:LOW_FORECAST_RELIABILITY` alert (engine.py:514); confidence falls via `_valuation_confidence` (engine.py:422-434, 0.40×reliability). Probe: reliability 20 → status `ATTRACTIVE`, confidence label `VERY_LOW`, risk `EXTREME`, alert `WARNING:LOW_FORECAST_RELIABILITY` | `test_alerts_include_severity_and_driver_focus`; `test_p2_alert_low_reliability_threshold_boundaries` (39.9/40.0/40.1, None) | **PARTIALLY SUPPORTED** | The literal token `FORECAST RISK WARNING` is **not emitted**; the engine emits `WARNING:LOW_FORECAST_RELIABILITY`. `FORECAST_RISK` is a spec name with zero references in `src` (P19, section 79). The claimed capability (not merely very attractive; low confidence + reliability warning attachable) is real. Correct the token to the emitted name, or note `FORECAST_RISK` is not produced. | D3/D8 (naming of `FORECAST_RISK`) |
| **73** Negative EPS | EPS < 0 → Forward P/E = NULL, P/E Valuation = NOT_APPLICABLE, no artificial fair price | `calculate_forward_pe` returns None for eps ≤ 0 (models.py:5-9); `calculate_forward_pe_fair_value` returns None for eps ≤ 0 (models.py:12-16); `_eps_flags` → `NEGATIVE_EPS`+`NOT_APPLICABLE` (engine.py:363-371); status → `NOT_APPLICABLE` (engine.py:197-199). Probe: EPS -50/-20/10 → all negative scenarios fpe None, fv None; status `NOT_APPLICABLE`, expected_fv None | `test_negative_eps_does_not_create_fake_pe_or_fair_value` (line 95) asserts bear fpe/fv None + `NEGATIVE_EPS` + expected_fv None; `test_p6_invalid_eps_variants_never_fabricate_values` | **SUPPORTED** | None | None |
| **74** Insufficient Peers | Valid peers < 8 → Industry Forward P/E = INSUFFICIENT_DATA, benchmark falls to Historical Median | `_select_target_pe` requires `forward_peer_count >= MIN_INDUSTRY_PEERS` (8) for `INDUSTRY_FORWARD_PE`, else historical (engine.py:263-267); `INSUFFICIENT_PEER_DATA` flag when forward values exist and count < 8 (engine.py:164-165). Probe: 7 peers + historical 7.0 → `target_pe_source == "HISTORICAL_MEDIAN_PE"`, `industry_peer_count == 7` | `test_industry_forward_pe_requires_eight_valid_peers` (line 67); `test_p4_peer_count_below_minimum_falls_back` (line 581); `test_p4_peer_count_filters_invalid_values` | **SUPPORTED** (precision note) | The fallback behavior is real and tested. Precision: the engine emits `INSUFFICIENT_PEER_DATA`, **not** `INDUSTRY_BENCHMARK_INSUFFICIENT` (which fires only under `target_source == "INSUFFICIENT_DATA"`, P21); and `industry_forward_pe_median` is still reported (6.0), merely not selected. Adjust the "INSUFFICIENT_DATA" label to the actual emitted signal. | None (emission-condition difference already annotated in section 55) |
| **75** Historical Divergence | Current Forward P/E far from Historical Median → Historical Valuation Divergence Alert | `_alerts` (engine.py:523-527) emits `WATCH:FORWARD_PE_ABOVE_HISTORICAL` / `WATCH:FORWARD_PE_BELOW_HISTORICAL` when ratio ≥ `historical_divergence_ratio` = 1.50. Probe: base fpe 10.0 vs hist 3.0 → `WATCH:FORWARD_PE_ABOVE_HISTORICAL` | `test_p2_alert_divergence_ratios_boundaries` (line 366) asserts the above/below pair and just-below boundary | **SUPPORTED** (D8 name note) | Capability and threshold are real and tested, but the emitted name is `WATCH:FORWARD_PE_ABOVE/BELOW_HISTORICAL`, not the spec name `HISTORICAL_VALUATION_DIVERGENCE` — already recorded in section 54 mapping. Reference that mapping; no new correction needed. | D8 (name mismatch, already annotated) |
| **76** Scenario Probability | Bear 20 / Base 60 / Bull 20 sums to 100%; Expected Fair Value is the correct weighted average | `_resolve_probabilities` normalizes (engine.py:305-310); `_expected_fair_value` = Σ fv × p (engine.py:392-396); `metadata["scenario_probability_sum"]` (engine.py:242). Probe: probs 0.2/0.6/0.2 sum 1.0; expected_fv 1260 = Σ fv×p | `test_valuation_engine_forward_pe_and_expected_fair_value` (sum ≈ 1.0, expected_fv == 1260); `test_probability_evidence_is_family_level_and_equal_weighted`; `test_p6_scenario_ordering_flag_and_probability_normalization` | **SUPPORTED** | None | None |
| **80** Fundamental Score Double Counting | High Fundamental Score must not directly raise Target P/E | `calculate_valuation` signature (engine.py:57-79) has **no** fundamental-score parameter; target P/E comes only from the benchmark hierarchy plus explicit, rationale-required `scenario_pe_adjustments` (engine.py:320-361). No code path multiplies target P/E by any fundamental score | No dedicated negative test (the input does not exist); the property is structurally guaranteed by the absence of any such input | **SUPPORTED** (structural) | Property holds because the Stage 7 boundary has no fundamental-score input — guaranteed by absence, not by an executed assertion. Optional: a regression note stating the guarantee is structural. | None |
| **81** Trend | Strong Improvement can change Scenario Probability, but does not directly Scale Target P/E | No trend parameter in the signature; target P/E is not trend-scaled (structurally impossible). Probability can shift only via family-level `probability_evidence` (e.g. `FUNDAMENTAL_DIRECTION`, `FORECAST_DIRECTION`), which the caller must aggregate (sections 23-24) | No dedicated test; the no-direct-scale property is structural | **PARTIALLY SUPPORTED** | The direct-scaling prohibition holds. The positive half ("can change probability") is true **only** through the caller-supplied family-evidence channel — a "Strong Improvement" Stage 4 trend does not cross the Stage 7 boundary as a parameter, so it cannot directly move probabilities; it must first be folded into family scores upstream. State this indirection. | D6 (if sector/trend inputs ever enter the boundary) |
| **82** Probability Confidence | Numeric probabilities (20/60/20) with weak evidence → Probability Confidence = LOW is possible | `probability_confidence` is an independent input (default 50.0, engine.py:75); feeds `_valuation_confidence` (engine.py:430) and `_driver_analysis`; label via `_confidence_label` with `CONFIDENCE_THRESHOLDS["low"] = 40.0` (parameters.py:55). Probe: probability_confidence 15 → label `LOW`; 20/60/20 prior preserved | `test_p5_nonfinite_probability_confidence_echo_finite` (input channel); no test asserts the exact "weak evidence → LOW" scenario | **SUPPORTED** | The independent channel and LOW label exist and are computed. Precision: "evidence strength" is **caller-supplied** as `probability_confidence`; Stage 7 does not derive it from any input, and no separate evidence-strength field exists. | None |
| **83** Forecast Revision | EPS 1100 → 1180 → 1270 can create Positive Revision Evidence | `POSITIVE_FORECAST_REVISION` has **zero references** in all of `src`. Revision *direction* is computed in Stage 5 (`revision_trend` in `src/forecast/repo.py:137-148` → `UPWARD`/`DOWNWARD`/`MIXED`) and consumed by the Stage 9 decision engine (`src/decision/engine.py:42,65,299`) — but nothing crosses into `src/valuation`. Stage 7 receives only family-level probability evidence; it produces no revision-evidence token | Stage 5 tests exist (`test_revision_trend_reports_direction`, `test_repo_revision_trend_built_from_stored_versions`) but none for a Stage 7 revision output | **UNSUPPORTED** | The claim overstates current behavior: **Stage 7 V1 produces no "Positive Revision Evidence" output.** Revision direction exists only in Stage 5/9. If the requirement is that the valuation layer surface revision evidence, that is not implemented and (absent an owner decision on how revision evidence reaches Stage 7) remains an open item. | D3/D8 (naming/route for a revision token) |
| **84** Loss to Profit | EPS -100 → +120 must not create misleading Growth/P/E; sign-change handling applies | `_scenario_sign_change_flags` (engine.py:374-384) emits `SIGN_CHANGE` + `LOSS_TO_PROFIT`/`PROFIT_TO_LOSS` across scenarios; negative EPS → fpe/fv None (models.py); status → `NOT_APPLICABLE` (engine.py:197-199). Probe: EPS -100/20/120 → `SIGN_CHANGE` + `LOSS_TO_PROFIT` on negative scenarios, `PROFIT_TO_LOSS` on positive; no fabricated fpe/fv for negative EPS | `test_negative_eps_does_not_create_fake_pe_or_fair_value` (asserts `SIGN_CHANGE` in bull flags, line 104); `test_p6_invalid_eps_variants_never_fabricate_values` | **SUPPORTED** (semantics note) | No misleading growth/P/E and sign-change flags are real and tested. Precision: the `LOSS_TO_PROFIT`/`PROFIT_TO_LOSS` labels are per-scenario sign transitions relative to the other scenarios, not temporal revision labels; the -100→+120 reading is represented by the flag set, not by a temporal series. | None |

---

## Six-Layer Validation

**1. Unit/formula.** Static inspection of every formula referenced by sections 71-76 and 80-84: `_valuation_status` (engine.py:409-419), `calculate_forward_pe` / `calculate_forward_pe_fair_value` (models.py:5-16), `_eps_flags` (engine.py:363-371), `_scenario_sign_change_flags` (engine.py:374-384), `_resolve_probabilities` + `_expected_fair_value` (engine.py:305-310, 392-396), `_alerts` divergence block (engine.py:518-532), `_select_target_pe` (engine.py:256-269), `_valuation_confidence` (engine.py:422-434). All match the claims' *capabilities*. No new formula was inferred.

**2. Contract/boundary.** The `calculate_valuation` signature (engine.py:57-79) was verified to contain **no** fundamental-score, trend, or revision input — this is the structural basis for the sections 80/81/83 findings. Outputs map to `ValuationResult` (schema.py:19-50): `valuation_status`, `valuation_confidence_label`, `alerts`, `valuation_risk_flags`, `scenarios[*].forward_pe/fair_value/flags`, `expected_fair_value`, `metadata["scenario_probability_sum"]`. No contract was changed.

**3. Production-path/integration.** Traced the relevant path: `calculate_valuation` → `_select_target_pe` → scenario loop (`_eps_flags`, forward P/E, fair value) → `_expected_fair_value` → `_valuation_status` → `_alerts` → `ValuationResult`. No consumer or runtime path was modified; `git status --short -- src/ tests/` is empty.

**4. Adversarial/negative.** Missing checks relevant to the audited claims (not executed in this audit unless stated):
- **S72/S82 boundary:** reliability exactly at 40.0 and confidence exactly at 40.0 are tested for the alert/flag channel (`test_p2_alert_low_reliability_threshold_boundaries`) but no test drives the *combined* S72 outcome (low P/E + low reliability → the claimed status/confidence combination) as one scenario.
- **S75 boundary:** divergence ratio 1.50 above/below tested (`test_p2_alert_divergence_ratios_boundaries`); determinism of the alert set is pinned by `test_p2_sensitivity_deterministic_repeated_runs`.
- **S73/S84 missing-data and NaN:** negative/zero/None/NaN EPS guarded and tested (`test_p3_nan_eps_is_guarded_as_invalid`, `test_p6_invalid_eps_variants_never_fabricate_values`).
- **S76 probability:** normalization under family evidence and inverted scenario ordering tested (`test_p6_scenario_ordering_flag_and_probability_normalization`); sum pinned at 1.0.
- **S80/S81 negative cases:** no test asserts "high fundamental score / strong trend leaves target P/E unchanged" — the inputs do not exist, so the negative property is structural, not executed. This is recorded as a documentation note, not claimed as a run.

**5. Regression/full suite.** Freshly executed in this audit (exact commands):
```
.venv/Scripts/python.exe -m pytest src/tests/test_stage7_valuation.py -q
→ 2 failed, 50 passed in 1.70s

.venv/Scripts/python.exe -m pytest src/tests/test_stage7_valuation.py src/tests/test_stage9_decision.py -q
→ 2 failed, 63 passed, 52 warnings in 1.08s
```
Breakdown: Stage 7 = 50 passed / 2 failed; Stage 9 = 13 passed. The 2 failures are the known, pre-existing P2 tests (`test_p2_sector_driver_decomposition_missing`, `test_p2_required_flip_dependence_alerts_missing`) — **not new regressions**, unchanged from P19/P20/P21/P22. Skips: 0 in these focused runs; the full-suite skip count of 1 is carried forward from P19. Full-suite re-execution was not repeated; the focused suites cover the audited surface and this audit changes no runtime code. In addition to the pytest runs, the section-by-section probes listed in the table were executed with the project interpreter and are reported as freshly run.

**6. Independent audit.** Each section's conclusion was cross-checked against both the code and its cited tests: S73/S76/S84 against the executed negative-EPS and normalization tests; S74/S75 against the peer-count and divergence tests; S72 against the reliability-threshold tests; S80/S81/S83 against the *absence* of the relevant inputs/tokens in the signature and in all of `src` (verified by grep: no fundamental/trend/revision parameter; `POSITIVE_FORECAST_REVISION` zero references). The S83 finding matches the P19 note that `FORECAST_RISK`-family names are absent, and the S74 emission-condition note matches the P21 section 55 refinement.

---

## Corrections Safe to Make Without an Owner Decision

1. **S72 (documentation):** replace the literal token `FORECAST RISK WARNING` with the actually emitted `WARNING:LOW_FORECAST_RELIABILITY`, or explicitly state that `FORECAST_RISK` is a spec name not produced by V1 (consistent with the P19 section 79 annotation). This is factual, decision-free.
2. **S74 (documentation):** restate the "INDUSTRY_FORWARD_PE = INSUFFICIENT_DATA" phrasing to name the actual emitted signal `INSUFFICIENT_PEER_DATA` and note that `industry_forward_pe_median` is still reported but not selected. This is factual, decision-free (the emission-condition distinction was already ratified in P21).
3. **S81 (documentation):** state that Stage 4 trend does not cross the Stage 7 boundary and can shift probability only through caller-supplied family evidence. Factual, decision-free.
4. **S84 (documentation, optional):** clarify that the `LOSS_TO_PROFIT`/`PROFIT_TO_LOSS` labels are per-scenario sign transitions, not temporal revision labels. Factual, decision-free.

## Findings That Must Remain Blocked

1. **S83 (overclaim, needs owner input):** Stage 7 V1 produces **no** `POSITIVE_FORECAST_REVISION` / revision-evidence output. Whether revision evidence should reach the valuation layer at all — and if so, through which route (family-evidence aggregation by the caller, or a new dated revision input) and under which name — is a policy question (relates to D3/D8 and the section 26 requirement). The PASS claim must not be treated as satisfied; the minimal *factual* correction (mark it not produced) can be applied now, but any decision about implementing or renaming stays with the owner.
2. **S80/S81/S82 positive-capability claims** are supported only via the caller-supplied evidence/confidence channel. If the owner expects Stage 7 to *derive* fundamental/trend/revision evidence or evidence-strength internally, that is new scope requiring a decision — none is assumed.
3. **Threshold provenance (S71/S75):** the status and divergence thresholds remain engine constants, not spec-ratified values (D9). No number was ratified or changed.

---

## Confirmation

- **No implementation or policy choice was made.** No D1-D9 decision was selected, explicitly or implicitly.
- No source, test, schema, spec, dependency, migration, or configuration file was modified — this audit is appended to `temp_report2.md` only; no prior content was overwritten.
- No formulas, thresholds, severities, mappings, dates, or defaults were invented.
- No failing test was weakened, deleted, skipped, or rewritten; the two P2 failures remain exactly as in P19-P22.
- No remote Git operations were performed (no commits, pushes, pulls, or branch changes).
- **Stage 7 remains unfrozen.** Work stops after appending this report.
============================================================================
# P24 — Stage 7 Stress-Test Documentation Corrections Report

**Date (UTC):** 2026-10-14
**Nature:** Bounded documentation-only correction task per P24. Applied only factual corrections supported by the P23 audit (2026-10-14 edition, lines 2538-2619) to stress-test sections 71-76 and 80-84 in `07_Stage7_Valuation.md`. No D1-D9 decision was selected. No Python source, test, schema, dependency, migration, or configuration file was changed.
**Prerequisite check:** The complete P23 report was read first. The older 2026-10-13 P23 draft (line 2510) was treated as superseded; all corrections below cite the 2026-10-14 P23 verdicts and were independently re-verified against code before editing. Where P23 provided no evidence for a change, no edit was made.

---

## 1. Exact Sections Edited

Five sections were edited. All edits are additive factual annotations inside the audited section, except S83 where the false PASS was struck through following the P19 Section-85 precedent:

### S72 — Low P/E / Poor Reliability (P23: PARTIALLY SUPPORTED)
- **Before:** claim text ending with literal token `FORECAST RISK WARNING` plus unqualified `PASS.`
- **After:** original text preserved; added blockquote `V1 Implementation Status (factual annotation — P24, per P23 audit)` stating the reachable V1 combination is `ATTRACTIVE` + `valuation_confidence`/`valuation_confidence_label` LOW/VERY_LOW + flag `LOW_FORECAST_RELIABILITY` and alert `WARNING:LOW_FORECAST_RELIABILITY` (`engine.py:162-163,514`); reliability is not an input to `_valuation_status`; the literal token `FORECAST RISK WARNING`/`FORECAST_RISK` is never emitted (zero references in `src`); D3/D8 remain unresolved; PASS applies only to the reachable combination.
- **Evidence:** `src/valuation/engine.py:162-163` (reliability flag), `:514` (WARNING alert), `_valuation_status` reads only upside figures; grep over `src/` returns zero hits for `FORECAST_RISK`; reliability-threshold boundaries covered by `test_p2_alert_low_reliability_threshold_boundaries`. Consistent with the P19 Section-79 annotation.

### S74 — Insufficient Industry Peers (P23: SUPPORTED with precision note)
- **Before:** `Industry Forward P/E = INSUFFICIENT_DATA` plus fallback to Historical Median, `PASS.`
- **After:** original text preserved; added annotation stating the actual behavior: industry-forward benchmark is rejected for selection (`target_pe_source` falls back to `HISTORICAL_MEDIAN_PE`; `_select_target_pe`, `engine.py:263-267`, `MIN_INDUSTRY_PEERS = 8`), `INSUFFICIENT_PEER_DATA` is flagged (`engine.py:164-165`), while `industry_forward_pe_median` still reports the median of available peers (e.g. 6.0 with 7 peers) but is not selected; `INDUSTRY_BENCHMARK_INSUFFICIENT` fires only when `target_source == "INSUFFICIENT_DATA"` and must not be conflated with `INSUFFICIENT_PEER_DATA`; cites the P21 Section-55 refinement.
- **Evidence:** `engine.py:92` (median computed regardless of count), `:263-267` (selection gate), `:164-165`/`:168-169` (distinct flags); tests `test_industry_forward_pe_requires_eight_valid_peers`, `test_p4_peer_count_below_minimum_falls_back`, `test_p4_peer_count_at_minimum_selects_industry_forward`, `test_p4_benchmark_fallback_ignores_forward_count_for_ttm`.

### S81 — Trend (P23: PARTIALLY SUPPORTED)
- **Before:** `Strong Improvement` can change Scenario Probability but does not directly scale Target P/E. `PASS.`
- **After:** original text preserved; added annotation stating the direct-scale prohibition holds structurally (`calculate_valuation` signature `engine.py:57-79` has no trend input) and the positive half holds only through the caller-supplied family-evidence channel (Sections 23-24, `probability_evidence`); a Stage 4 trend never crosses the Stage 7 boundary directly and must first be folded into family scores upstream; D6 remains unresolved.
- **Evidence:** signature inspection confirms no `fundamental_score`, `trend`, or `revision` parameter; `_resolve_probabilities` (`engine.py:272-318`) accepts only family-level evidence; direct `probability_adjustments` are rejected by ValueError.

### S83 — Forecast Revision (P23: UNSUPPORTED)
- **Before:** `EPS Forecast 1100 → 1180 → 1270` can create Positive Revision Evidence. `PASS.`
- **After:** added `NOT PRODUCED IN STAGE 7 V1` annotation: Stage 7 produces no revision-evidence output; `POSITIVE_FORECAST_REVISION` has zero references in all of `src`; revision direction exists only in Stage 5 (`revision_trend`, `src/forecast/repo.py:137-148` → `UPWARD`/`DOWNWARD`/`MIXED`) and is consumed by Stage 9 (`src/decision/engine.py`), with nothing crossing into `src/valuation`; whether revision evidence should reach the valuation layer, via which route and under which name, is an open policy question (D3/D8, Section 26); no V2 deferral is declared. Struck the claim: `~~PASS.~~ → **Status: does not hold in V1 — Stage 7 produces no Positive Revision Evidence (unresolved D3/D8).**`
- **Evidence:** full-`src` grep for `POSITIVE_FORECAST_REVISION` returns zero hits; `calculate_valuation` signature has no revision input; Stage 5 revision tests exist but no Stage 7 revision-output test exists. This is the only section where the PASS label was removed, because P23 verdict is UNSUPPORTED.

### S84 — Loss to Profit (P23: SUPPORTED with semantics note)
- **Before:** `EPS: -100 → +120` must not create misleading Growth/P/E; sign-change handling applies. `PASS.`
- **After:** original text and PASS preserved; added annotation confirming no fabricated fpe/fv for negative EPS (models + `engine.py:197-199`) and clarifying that `LOSS_TO_PROFIT`/`PROFIT_TO_LOSS` are per-scenario sign transitions relative to the other scenarios in the same run (`_scenario_sign_change_flags`, `engine.py:374-384`), not temporal revision labels; the -100→+120 reading is represented by the flag set, not a time series.
- **Evidence:** `models.py:5-16` (None for eps ≤ 0), `_eps_flags` (`engine.py:363-371`), `_scenario_sign_change_flags` (`engine.py:374-384`); tests `test_negative_eps_does_not_create_fake_pe_or_fair_value` (asserts `SIGN_CHANGE`), `test_p6_invalid_eps_variants_never_fabricate_values`.

## 2. Sections Reviewed but Deliberately Left Unchanged

- **S71 (SUPPORTED):** cheap-company → `ATTRACTIVE`/`VERY_ATTRACTIVE` via `_valuation_status` and `VALUATION_THRESHOLDS`. No correction required. Threshold provenance (engine constants, not spec-ratified) is already annotated in Section 48 (D9); no number was touched.
- **S73 (SUPPORTED):** negative-EPS → NULL P/E, `NOT_APPLICABLE`, no fabricated fair value. Fully implemented and tested. Left unchanged.
- **S75 (SUPPORTED with D8 name note):** historical-divergence capability and 1.50 threshold are real and tested (`_alerts`, `engine.py:523-527`; `test_p2_alert_divergence_ratios_boundaries`), but the emitted names are `WATCH:FORWARD_PE_ABOVE/BELOW_HISTORICAL`, not the spec name `HISTORICAL_VALUATION_DIVERGENCE`. No new edit was warranted because the mapping is already recorded in the Section-54 annotation; the report references that mapping instead of duplicating it. D8 stays open.
- **S76 (SUPPORTED):** 20/60/20 sums to 100% and expected fair value is the weighted average (`_resolve_probabilities`, `_expected_fair_value`, `metadata["scenario_probability_sum"]`). Left unchanged.
- **S80 (SUPPORTED, structural):** high Fundamental Score cannot directly raise Target P/E because the Stage 7 boundary has no fundamental-score input. The property holds by absence and is guaranteed structurally; no dedicated negative test exists. No edit was made to avoid overstating an unexecuted assertion; recorded here as a documentation note only.
- **S82 (SUPPORTED):** numeric 20/60/20 probabilities with weak evidence → `probability_confidence = LOW` is possible via the independent `probability_confidence` input (default 50.0, `engine.py:75,430`; `CONFIDENCE_THRESHOLDS["low"] = 40.0`). Precision noted: evidence strength is caller-supplied; Stage 7 does not derive it and no separate evidence-strength field exists. No wording change was warranted beyond this report note.

No other specification section was modified. No direct contradiction outside the audited sections was encountered that required stopping for authorization.

## 3. Six-Layer Validation (freshly executed unless stated)

1. **Unit/formula (fresh static + test execution):** No valuation formula or runtime logic changed. Verified `git diff HEAD --name-only -- src/` is empty (no source/test/schema/config change). Focused suites below exercise `_valuation_status`, `calculate_forward_pe`/`calculate_forward_pe_fair_value`, `_eps_flags`, `_scenario_sign_change_flags`, `_resolve_probabilities`/`_expected_fair_value`, `_alerts` divergence block, and `_select_target_pe`.
2. **Contract/boundary (fresh static):** Public signatures, schemas, output names, and boundary behavior unchanged. `calculate_valuation` signature (`engine.py:57-79`) and `ValuationResult` (`schema.py:19-50`) inspected; only `07_Stage7_Valuation.md` sections 72/74/81/83/84 changed. No alert name, emission condition, severity, threshold, or output contract was renamed or altered.
3. **Production-path/integration (fresh static):** No runtime or consumer file changed. Path `calculate_valuation` → `_select_target_pe` → scenario loop → `_expected_fair_value` → `_valuation_status` → `_alerts` → `ValuationResult` traced; `git diff` confirms the change set is documentation-only.
4. **Adversarial/negative (fresh test evidence + static):** The two known P2 failing-first tests remain present and still fail as designed (see below) — they were not weakened, deleted, skipped, or rewritten. Revised wording preserves P23 negative cases: S72 (reliability cannot move status/fair value), S74 (7-peer case still yields usable historical benchmark without `INDUSTRY_BENCHMARK_INSUFFICIENT`), S81 (trend cannot directly scale target P/E), S83 (no revision output exists to misuse), S84 (negative EPS still yields None, sign flags still per-scenario).
5. **Regression/full suite (freshly executed with `.venv/Scripts/python.exe` from project root):**
   - `python -m pytest src/tests/test_stage7_valuation.py -q` → **2 failed, 50 passed in 1.54s.** Failures are exactly the known pre-existing P2 tests (`test_p2_sector_driver_decomposition_missing`, `test_p2_required_flip_dependence_alerts_missing`); not new regressions, unchanged from P19-P23.
   - `python -m pytest src/tests/test_stage7_valuation.py src/tests/test_stage9_decision.py -q` → **2 failed, 63 passed, 52 warnings in 1.64s.** Stage 9 contributes 13 passes. Warnings are the known `datetime.utcnow()` DeprecationWarnings in Stage 9/decision code (unrelated to this task; P12 scope).
   - `python -m pytest src/tests/ -q -rs --ignore=src/tests/test_codal_pdf_extraction.py` → **2 failed, 900 passed, 1 skipped, 1068 warnings in 136.68s.** Same 2 P2 failures; 1 skip is `test_codal_extraction.py:307` (real Codal sample PDF not available in CI); PDF-extraction fixture exclusion is the established one, and no unrelated PDF was substituted. Historical counts are not presented as fresh except where re-executed above.
6. **Independent audit (fresh):** Every edited section was compared against the 2026-10-14 P23 verdict and the actual implementation: S72 token absence re-grepped (zero `FORECAST_RISK` hits); S74 median/selection/flag logic re-read (`engine.py:89-99,164-169,256-269`); S81 signature re-inspected (no trend input); S83 zero-reference claim re-grepped (`POSITIVE_FORECAST_REVISION`, zero hits) and Stage 5/9 route confirmed (`repo.py:137-148`, `decision/engine.py`); S84 sign-flag function re-read (`engine.py:374-384`). No unsupported PASS claim remains within the authorized scope (71-76, 80-84): S71/73/76/80/82 supported claims preserved, S72/74/81/84 qualified, S75 qualified by reference to the existing Section-54 mapping, S83 struck. No unresolved D1-D9 decision was silently selected; no V2 deferral was declared; no threshold, formula, severity, mapping, or date policy was invented.

## 4. Remaining D1-D9 Blockers (unchanged, none resolved here)

D1 (flip risk), D2 (multiple dependence), D3 (EPS dependence incl. `FORECAST_RISK` naming), D4 (margin risk), D5 (high impact + high uncertainty), D6 (sector-driver chains incl. trend/fundamental routing), D7 (PIT enforcement), D8 (alert-name/trigger semantics incl. S72/S74/S75/S83 names), D9 (parameter registry and `as_of` selection; threshold provenance for S71/S75). S83 additionally depends on the Section-26 revision-evidence route decision.

## 5. Confirmation

- Only `07_Stage7_Valuation.md` sections 72, 74, 81, 83, 84 were edited (5 minimal annotations + 1 PASS strike in S83). No Python source, test, schema, dependency, migration, or configuration file was modified.
- The two P2 failing-first tests are intact and still fail as designed; no test was weakened to obtain a pass.
- Final diff of `07_Stage7_Valuation.md` was inspected before reporting.
- No remote Git operation occurred (no commits, pushes, pulls, or branch changes).
- **Stage 7 remains unfrozen.** No freeze was declared. Work stops after appending this report.
============================================================================
# P25 — Stage 7 D1–D9 Consolidated Owner Decision Package

**Date (UTC):** 2026-10-14
**Nature:** READ-ONLY consolidated decision package. No decision implemented; no source, test, schema, migration, configuration, dependency, or specification file modified. No formula, threshold, perturbation size, severity, mapping, default, effective date, rounding policy, or acceptance criterion invented. The only write is this report, appended to `temp_report2.md`.
**Evidence base:** `temp_report2.md` P17–P24 (P23 2026-10-14 audit and P24 corrections take precedence over superseded drafts); `07_Stage7_Valuation.md` (sections 10, 23-24, 26, 42-57, 64-69, 71-76, 80-84); `src/valuation/engine.py` (full read, lines 57-535), `models.py`, `parameters.py`, `schema.py`; `src/forecast/repo.py:137-148` (revision_trend); `src/decision/engine.py:42,65,299` (revision consumer); `src/tests/test_stage7_valuation.py` (both P2 failing tests verified present at lines 406/425); `src/tests/test_stage9_decision.py` (consumer contract).
**Evidence discipline:** existing implementation behavior is treated as evidence, never as automatic approval. Each record below separates (i) verified behavior, (ii) existing-but-unapproved implementation choices, (iii) missing behavior, (iv) the decision required. Every recommendation is marked **PROPOSAL — NOT APPROVED** and none is acted on.

---

## D1 — Assessment Flip Risk

1. **Current verified behavior.** Engine emits no `ASSESSMENT_FLIP_RISK` (zero refs in `src/valuation`). `_alerts` (`engine.py:500-535`) emits only dispersion/reliability/benchmark/divergence/top-driver alerts. Status transitions are computed (`_valuation_status`, `engine.py:409-419`); `test_p2_required_flip_dependence_alerts_missing` proves a 10% EPS shock moves `ATTRACTIVE → FAIR` with no alert. `SENSITIVITY_PERTURBATION = 0.10` (`parameters.py:77`) exists but is consumed only by `_driver_analysis` for driver impact, never for flip detection — reusing it as policy would launder an unapproved constant into the spec.
2. **Unresolved question.** Which status transitions count as flips, on which perturbed inputs, at what magnitudes, with what severity?
3. **Viable options.** (a) Reuse 0.10 one-at-a-time EPS/target-P/E shocks as the flip probe (zero new constants; but 0.10 was never approved for this purpose). (b) Owner-specified dedicated flip set: named inputs, magnitudes, joint vs one-at-a-time. (c) No-change V1 limitation: record flip detection as absent (spec already annotated NOT IMPLEMENTED in section 77).
4. **Recommended: (a) — PROPOSAL — NOT APPROVED.** One-at-a-time 10% shocks to forecast EPS and target P/E; alert when the recomputed status leaves its band; severity from band distance. Cheapest, fully determined by existing machinery, versioned under D9.
5. **Rationale/trade-offs.** (a) converts an existing constant into approved policy explicitly instead of silently; auditability good. Risk: 10% may over/under-trigger on the `ATTRACTIVE` band edges; correlated joint shocks are excluded, so combined fragility is understated.
6. **Inputs/contracts/consumers.** No new input field needed. Adds one alert name to `alerts` (section 66 additive, versioned). Stage 9 parses `alerts` today — additive names are safe; severity mapping must be published to consumers.
7. **Failure modes/missing-data.** Missing/NaN EPS, `NOT_APPLICABLE` status, zero target P/E, all-`None` scenarios must yield *no* flip alert (never a default flip). Threshold-edge oscillation (status one rounding unit from a band edge) must not flap between runs — determinism required.
8. **Tests needed.** Boundary: shock that just flips vs just holds; negative: stable status → no alert; adversarial: NaN/None/negative EPS, sign-change, zero target P/E; determinism: repeated runs identical; regression: existing 50 passing Stage 7 tests unaffected.
9. **Dependencies/order.** Needs D8 (emitted name), D9 (magnitude versioning), D2/D3 precedence rule. After D8, with D2/D3.
10. **Owner decision statement.** "Approve flip detection as specified in D1-(a) (10% OAT EPS and target-P/E shocks, band-exit trigger, band-distance severity), or reject in favor of (b)/(c)."

## D2 — High Multiple Dependence

1. **Current verified behavior.** No multiple-dependence formula exists anywhere. `high_dependence_share = 0.60` (`parameters.py:73`) is dead — sole reference in `src` is its declaration; nothing reads it. `HIGH_MULTIPLE_DEPENDENCE` zero refs in `src/valuation`. **Do not activate the constant automatically.**
2. **Unresolved question.** Does "multiple dependence" mean attribution share of fair value from the target-multiple factor, or elasticity to a multiple shock — and on which side/threshold?
3. **Viable options.** (a) Attribution share: `TARGET_PE` share of `impact_pct` from `_driver_analysis` (`engine.py:488-495`), alert when share ≥ 0.60 (explicitly approving the existing constant). (b) Sensitivity share: FV elasticity to multiple vs EPS shock. (c) No-change: documented non-implementation.
4. **Recommended: (a) — PROPOSAL — NOT APPROVED.** Directly computable from shipped outputs; gives the dead constant an approved meaning.
5. **Rationale/trade-offs.** Attribution is deterministic and explainable; risk is denominator degeneracy (`total = max(sum, 1e-9)`, `engine.py:489`) inflating shares, and conflating cheap-company (below-target multiple) with expensive-company dependence under one threshold.
6. **Inputs/contracts/consumers.** No new input. New alert name (section 66). Reuses published `driver_impact` — consumers reading it gain a derived signal; document that the contract interpretation is extended.
7. **Failure modes/missing-data.** One factor `None` → no metric (never 0% or 100% by default); both `None` → empty driver path (`engine.py:476-477`) → no alert; near-zero denominator → guard, not alert.
8. **Tests needed.** Share exactly 0.60 / 0.599 / 0.601; degenerate denominator; one/both factors `None`; determinism; negative: EPS-share-dominant case silent.
9. **Dependencies/order.** Joint precedence with D3; D8 name; D9 threshold versioning. Decide with D1/D3 as one alert family.
10. **Owner decision statement.** "Approve multiple dependence as D2-(a) attribution share with 0.60 threshold, or select (b)/(c)."

## D3 — EPS Dependence and Forecast Revision

1. **Current verified behavior.** No EPS-dependence formula; `HIGH_EPS_DEPENDENCE` zero refs in `src/valuation`. `FORECAST_RISK` is a spec-only name (section 79 alternative) with zero refs in all of `src` — P24 annotation records it as not produced. Revision direction is computed in Stage 5 (`revision_trend`, `repo.py:137-148` → UPWARD/DOWNWARD/MIXED) and consumed by Stage 9 (`decision/engine.py:42,65,299`); **nothing crosses into `src/valuation`** — P23 verdict UNSUPPORTED for S83, P24 struck its PASS. Stage 7 receives only family-level `probability_evidence` (sections 23-24; `_resolve_probabilities`, `engine.py:272-318`, direct adjustments rejected). Reliability input exists (`forecast_reliability_score`) and `LOW_FORECAST_RELIABILITY` already fires (flag `engine.py:163`, alert `engine.py:514`).
2. **Unresolved question.** What is EPS dependence (share-only vs reliability-weighted), how does it interact with `LOW_FORECAST_RELIABILITY`, which name survives, and by what route — if any — does Stage 5 revision evidence reach Stage 7?
3. **Viable options.** (a) Share-only metric (mirror of D2: EPS `impact_pct` share) named `HIGH_EPS_DEPENDENCE`; retire `FORECAST_RISK`; revision evidence reaches Stage 7 only via caller-folded `FORECAST_DIRECTION` family evidence (no new input). (b) Two distinct alerts: share-driven `HIGH_EPS_DEPENDENCE` plus reliability-driven `FORECAST_RISK`. (c) No-change: neither alert; revision stays a Stage 5→9 signal.
4. **Recommended: (a) — PROPOSAL — NOT APPROVED.** Smallest contract footprint; resolves naming; keeps the Stage 7 boundary unchanged.
5. **Rationale/trade-offs.** (a) avoids double-signaling the same reliability input and avoids a new dated input. Risk: share-only cannot express "EPS-heavy *and* untrustworthy" in one token — that combination is observable only by co-occurrence of two alerts.
6. **Inputs/contracts/consumers.** No new input under (a). One new alert name; spec section 79 rewritten to the chosen name. Stage 9 sees a new vocabulary token (additive-safe). Section 26 (`POSITIVE_FORECAST_REVISION` as probability evidence) needs a conforming note pointing at the caller-folding route.
7. **Failure modes/missing-data.** Reliability `None` (clamped to 50.0, `engine.py:490`) must not silently upgrade confidence; co-firing with `LOW_FORECAST_RELIABILITY` follows the precedence rule; missing revision history → no revision inference.
8. **Tests needed.** EPS share at threshold; reliability `None`/40.0 boundaries; D2+D3 co-occurrence precedence; caller-folded revision evidence shifts probabilities via family channel; negative: low EPS share silent.
9. **Dependencies/order.** D2 precedence (joint), D8 naming, D9 versioning; revision route touches D6-family scope minimally. Decide with D1/D2.
10. **Owner decision statement.** "Approve D3-(a) (EPS attribution share as `HIGH_EPS_DEPENDENCE`, `FORECAST_RISK` retired, revision via caller-folded family evidence), or select (b)/(c)."

## D4 — Margin Assumption Risk

1. **Current verified behavior.** `MARGIN_ASSUMPTION_RISK` zero refs in `src/valuation`. Hard contract gap: `calculate_valuation` (`engine.py:57-79`) and `ValuationResult` (`schema.py:19-50`) expose **no margin, revenue, or cost field at all**. Not a wiring gap — the data does not exist at the boundary.
2. **Unresolved question.** Should V1 support margin risk at all, and if so, from which supplied margin series?
3. **Viable options.** (a) Contract expansion: dated margin-series input with provenance/validation. (b) Owner-defined proxy — none exists; none proposed here. (c) No-change: documented non-implementation (spec section 49 table already records ABSENT/D4).
4. **Recommended: (c) — PROPOSAL — NOT APPROVED.** No evidence-supported proxy exists; inventing one fabricates policy.
5. **Rationale/trade-offs.** (c) is honest and zero-cost; the gap stays visible. Risk accepted: margin-driven fragility is invisible in V1. (a) remains available when an upstream margin series exists.
6. **Inputs/contracts/consumers.** (c): none. (a): new input field + validation + consumer migration.
7. **Failure modes/missing-data.** Under (c): alert stays absent — assert so. Under (a): stale/undated margin must downgrade, never silently validate.
8. **Tests needed.** Under (c): negative test pinning absence. Under (a): missing/stale margin, sign changes, threshold boundary, determinism.
9. **Dependencies/order.** (a) needs D7 provenance + D9 versioning + D8 name. Independent otherwise — resolvable immediately via (c).
10. **Owner decision statement.** "Approve D4-(c) documented non-implementation in V1, or fund (a)/(b) with a defined margin source."

## D5 — High Impact Plus High Uncertainty

1. **Current verified behavior.** `HIGH_IMPACT_HIGH_UNCERTAINTY` zero refs in `src/valuation`. Ingredients exist for the two-driver set only: `driver_impact` (`engine.py:495`), `driver_uncertainty` blend (`engine.py:493`: 0.5/0.3/0.2 weights on reliability/probability/quality), `review_priority = impact × uncertainty / 100` (`engine.py:497`). The 0.10 perturbation and 0.5/0.3/0.2 weights are **unapproved implementation constants**, not policy.
2. **Unresolved question.** What defines "high impact" / "high uncertainty", how combined (product vs joint threshold), and over which driver set?
3. **Viable options.** (a) Apply to existing `{EPS, TARGET_PE}` set with owner-specified thresholds (independently definable now). (b) Defer until D6 sector chains land. (c) No-change: keep `review_priority` as an informational output with no alert.
4. **Recommended: (a) — PROPOSAL — NOT APPROVED.** Uses shipped outputs; no contract expansion.
5. **Rationale/trade-offs.** With two drivers whose shares sum to 100%, "high impact" is near-tautological — the alert's information content is low until D6 widens the set; thresholds must be set knowing this. Risk of laundering the 0.5/0.3/0.2 weights into policy is contained by requiring owner thresholds.
6. **Inputs/contracts/consumers.** No new input. New alert name; attaches semantics to the already-published `review_priority` output.
7. **Failure modes/missing-data.** Empty-driver path (`engine.py:476-477`) → no alert; uniform uncertainty across drivers must not double-fire; normalization changes must not silently re-trigger history (ties to D9).
8. **Tests needed.** Each of impact/uncertainty at/inside/outside thresholds; both-high fires; one-high silent; determinism; degenerate empty-driver case.
9. **Dependencies/order.** (a) independent of D6; (b) blocked on D6. Needs D8 name + D9 versioning either way.
10. **Owner decision statement.** "Approve D5-(a) two-driver alert with owner thresholds, or defer via (b), or keep informational via (c)."

## D6 — Sector Driver Chains

1. **Current verified behavior.** `_driver_analysis` hardcodes `drivers = {"EPS", "TARGET_PE"}` (`engine.py:488`); no `industry_code` branching (echoed to metadata only); `nav_per_share` recorded as `nav_per_share_received` (`engine.py:247`), consumed by no formula; `calculate_nav_fair_value` (`models.py:19-23`) is an unwired export. Ranking is identical across non-financial/bank/holding — proven by still-failing `test_p2_sector_driver_decomposition_missing`. P24 documented the Stage 4-trend indirection (S81: trend reaches probabilities only via caller-folded family evidence).
2. **Unresolved question.** Which source fields, formulas, sector mapping, and contract expansion implement the three required chains (Revenue→Margin→Profit→EPS→FV; Loans/Deposits→NII/NIM→Profit→EPS→FV; NAV→NAV Growth→Profit→EPS→FV with P/NAV in Stage 7) — without rebuilding EPS from a new share count (section 58 forbids it)?
3. **Viable options.** (a) Implement sector-branching driver analysis with new chain inputs. (b) No-change: defer chains, keep documented two-driver behavior (section 44 annotation already records this). No third option has project evidence.
4. **Recommended: (b) — PROPOSAL — NOT APPROVED.** No owner-approved industry mapping exists anywhere in the project; every chain field except EPS/target-P/E is absent from the contract; (a) is the largest contract change in D1-D9.
5. **Rationale/trade-offs.** (b) preserves contract stability (section 66) and Stage 9 compatibility at the cost of leaving the two P2 chain assertions failing and sector risk undifferentiated. (a) would change `valuation_driver_ranking` content (public output, section 69) for every consumer.
6. **Inputs/contracts/consumers.** (b): none. (a): new chain source fields + mapping + EPS-consumption validation + `calculate_nav_fair_value` activation; ranking becomes sector-dependent; dashboards/Stage 9 must migrate.
7. **Failure modes/missing-data.** Partial chain inputs must degrade per-sector (no zero-filling); unknown industry code must fall back to the two-driver set explicitly, never to a guessed sector; NAV ≤ 0 must not produce fair value.
8. **Tests needed.** One chain per sector; mixed/unknown code; partial inputs; NAV zero/negative; determinism; the two P2 tests re-baselined only after approval — never before.
9. **Dependencies/order.** Needs D7 provenance for chain inputs + D9 versioning + D8 if driver names enter alerts. Unblocks D5 sector scope. Decide second, right after D8.
10. **Owner decision statement.** "Approve D6-(b) deferral of sector chains (two-driver V1 stands), or fund (a) with an approved industry mapping and chain field list."

## D7 — Point-in-Time Correctness

1. **Current verified behavior.** Boundary does not enforce PIT: benchmark series enter as bare floats (`engine.py:70-72`); `valuation_date`/`data_cutoff_datetime` only normalized/echoed (`engine.py:104-108`), never compared; `metadata["pit_inputs_required"]` (`engine.py:248`) is informational. No production caller supplies PIT inputs (P13 finding, standing). Spec sections 56-57 require Price/Forecast-Cutoff/Publication/Version/EPS-availability observance. P19 struck the section-85 PASS.
2. **Unresolved question.** Provenance-per-observation vs caller attestation vs documented limitation — with which temporal fields, ordering rule, and violation response?
3. **Viable options.** (a) Per-observation provenance with boundary enforcement (reject/downgrade post-cutoff observations). (b) Caller attestation with a precise ordering/validation rule (Stage 7 validates form, not truth). (c) No-change: documented V1 limitation (current spec state).
4. **Recommended: (b) as V1, (a) as V2 direction — PROPOSAL — NOT APPROVED.** (b) is migratable without breaking the signature; (a) is strongest but heaviest. Metadata alone must never be presented as enforcement under any option.
5. **Rationale/trade-offs.** Lookahead contamination of backtests is the highest-creditability risk in D1-D9. (b) halves residual risk at low migration cost but cannot catch false attestation; (a) catches it at the boundary at the cost of every caller supplying dates. The exact ordering rule (valuation date vs cutoff vs publication date) is still missing — see follow-up below.
6. **Inputs/contracts/consumers.** (b): one attestation field (additive). (a): dated series (breaking or additive-optional). (c): none. All callers including Stage 9 paths migrate under (a)/(b).
7. **Failure modes/missing-data.** Missing dates → downgrade/flag, never silent acceptance; future-dated valuation → reject; date-equal boundary defined explicitly; `POINT_IN_TIME_WARNING` trigger defined here, not elsewhere.
8. **Tests needed.** Post-cutoff rejected/downgraded per rule; date-equal boundary; missing dates; future valuation date; determinism; pre-cutoff data passes untouched.
9. **Dependencies/order.** Mutually dependent with D9 (`as_of` needs the temporal contract); chain inputs implicate D6; warning name implicates D8. Decide paired with D9, after features stabilize.
10. **Owner decision statement.** "Approve D7-(b) attestation for V1 with (a) as the V2 target, or select (a)/(c); and commission the bounded follow-up to fix the exact date-ordering rule and violation response."

## D8 — Alert Contract and Naming

1. **Current verified behavior.** 13 spec names (section 49) vs a different emitted vocabulary (P19 tables + P21 section-55 refinement + P23/P24): `VALUATION_BENCHMARK_DIVERGENCE` vs `WATCH:VALUATION_ABOVE/BELOW_TARGET_PE` (`engine.py:519-522`); `HISTORICAL_VALUATION_DIVERGENCE` vs `WATCH:FORWARD_PE_ABOVE/BELOW_HISTORICAL` (`:523-527`); `INDUSTRY_VALUATION_DIVERGENCE` vs `WATCH:FORWARD_PE_ABOVE/BELOW_INDUSTRY` (`:528-532`); `INSUFFICIENT_PEER_DATA` (flag, `:164-165`, peer count < 8) ≠ `INDUSTRY_BENCHMARK_INSUFFICIENT` (flag, `:168-169`, no usable benchmark at all) — P24 S74 annotation pins the 7-peer distinction. Flags (`INSUFFICIENT_PEER_DATA`, `NEGATIVE_EPS`, `SIGN_CHANGE`) are flag-channel-only, not severity-bearing. `POOR_DATA_QUALITY`, `POINT_IN_TIME_WARNING`, `FORECAST_RISK`, `POSITIVE_FORECAST_REVISION` have zero refs in `src` (re-verified this task). Stage 9 consumes these outputs today (13/13 passing, carried forward).
2. **Unresolved question.** Rename outputs, alias both vocabularies, or adopt engine names into the spec — and does flag-level emission satisfy section 49?
3. **Viable options.** (a) Rename engine outputs to spec names. (b) Alias both names (backwards-compatible, duplicated vocabulary). (c) No-code change: amend spec sections 49/54-55 to the emitted vocabulary. Plus the orthogonal flag-sufficiency ruling.
4. **Recommended: (c) plus defined triggers for the four absent names — PROPOSAL — NOT APPROVED.** Best consumer stability; above/below direction pairs preserved (merging them would destroy directional signal).
5. **Rationale/trade-offs.** (a) breaks every consumer parsing current names and collapses opposing-economics pairs. (b) is compatible but doubles vocabulary with undefined alias severity. (c) costs spec edits only, but accepts loss of the mandated names.
6. **Inputs/contracts/consumers.** (c): spec-only; no consumer migration. (a): versioned breaking contract change (section 66/67, explicit migration). (b): additive, needs compatibility tests. Flag promotion needs severity definitions.
7. **Failure modes/missing-data.** Rename without coordinated migration → silent downstream alert loss; promoted flags without severity → unrankable output; above/below merge → direction loss.
8. **Tests needed.** Each name present/absent as chosen; above and below both exercisable and distinguishable; Stage 9 suite re-run green; alias-compat test under (b); per-trigger negatives.
9. **Dependencies/order.** Decide FIRST — every other alert decision emits into this vocabulary. Unblocks D1-D5, D7-warning.
10. **Owner decision statement.** "Approve D8-(c) spec-adoption of emitted names with preserved above/below pairs and new trigger definitions, or select (a)/(b); and rule whether flag-level emission satisfies section 49."

## D9 — Parameter/Model Versioning

1. **Current verified behavior.** All thresholds are fixed constants in `parameters.py` (status/confidence/risk/alert incl. unused 0.60; `SENSITIVITY_PERTURBATION = 0.10`; `MIN_INDUSTRY_PEERS = 8`; `MODEL_VERSION = "STAGE7_V1"`, `CONTRACT_VERSION = "VALUATION_CONTRACT_V1"`). `effective_from`/`parameter_version` zero refs in `src` (re-verified). Section-65 five-field store does not exist. P14's in-code registry remains a proposal, not approved.
2. **Unresolved question.** Which registry mechanism, and what `as_of` rule selects the effective version at query time?
3. **Viable options.** (a) In-code versioned registry (surface-stable; weak backtest as-of safety). (b) Persistent DB-backed five-field table per section 65 (strongest auditability/reproducibility; heaviest migration). (c) No-change: fixed constants stand (no evidence-supported third mechanism exists — reported empty, not invented).
4. **Recommended: (a) as V1 with `as_of` = data cutoff, (b) as V2 direction — PROPOSAL — NOT APPROVED.** Minimal, reviewable, testable; cutoff is the only timestamp every valuation already carries.
5. **Rationale/trade-offs.** Without as-of selection any threshold change silently rewrites history. (a) without a rule is documentation, not versioning — hence the cutoff rule is part of the proposal. (b) is strictly better for backtests but couples a shared schema object across stages.
6. **Inputs/contracts/consumers.** (a): stable surface; `MODEL_VERSION` deepens into a version key callers may pin. (b): new schema object + migration + dependency; all consumers resolve parameters through it.
7. **Failure modes/missing-data.** Unpinned historical runs executing against current constants (silent history rewrite); version-boundary off-by-one; missing effective date → explicit fallback, never silent latest.
8. **Tests needed.** As-of selection across a version boundary; changes effective on the right date and not before; determinism under pinned version; DB round-trip under (b).
9. **Dependencies/order.** `as_of` needs D7's temporal contract — decide paired with D7, after features stabilize. Supplies versioning for D1-D6.
10. **Owner decision statement.** "Approve D9-(a) in-code registry with cutoff-based `as_of` for V1 (DB registry as V2 direction), or select (b)/(c)."

---

## A. Dependency Graph and Recommended Implementation Sequence

```
D8 (vocabulary) ──┬──▶ D1 ──▶ D2 ◀──▶ D3 (precedence family, joint)
                  ├──▶ D5 (two-driver scope; sector scope waits on D6)
                  └──▶ D7-warning trigger name
D6 (contract shape) ──▶ unlocks D5-sector scope + P2 chain tests
D4 ── independent (recommended: close now via documented non-implementation)
D7 ◀──▶ D9 (temporal contract ◀──▶ as_of rule; decide as a pair, last)
```

**Proposed discussion/implementation order (proposal, not a plan):** D8 → D6 → D1+D2+D3 (joint) → D5-two-driver → D4-close → D7+D9 pair. Rationale: vocabulary (D8) and contract shape (D6, D7) precede formulas (D1-D5), because formulas are expressed *in* the vocabulary and *on* the contract. D4 closes cheaply in parallel. D7/D9 infrastructure lands last so the temporal contract is specified once, against a stable feature set.

## B. Cross-Decision Contract Impact Matrix (Stage 5 → Stage 7 → Stage 9)

| Boundary | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 |
|---|---|---|---|---|---|---|---|---|---|
| Stage 5 → 7 inputs | — | — | caller-folded revision via family evidence (no new field) | (a) new margin series | — | (a) new chain fields | (a) dated series / (b) attestation field | — | version pin (optional) |
| Stage 7 outputs (`alerts`/`flags`/`ranking`) | +1 alert | +1 alert | +1 alert (+rename of §79) | (c) none | +1 alert | ranking content change + NAV FV | warning trigger | rename/alias/spec-adopt | version key semantics |
| Stage 7 → 9 consumers | additive-safe | additive-safe | additive-safe | none under (c) | additive-safe | migration required | migration under (a)/(b) | breaking under rename; safe under (c) | resolution-path change under (b) |
| Schemas/params | D9 versions magnitude | D9 versions 0.60 | D9 versions threshold | D9 versions formula | D9 versions thresholds | D9 versions chains | D9 versions rule | severity defs | registry object |

Legend: "—" = no change under the recommended option; "(a)/(b)/(c)" = only under that option.

## C. Proposed Implementation/Test Plan (small auditable packages, NOT implemented)

- **WP-0 D8 vocabulary freeze.** Amend-or-affirm alert names per D8 decision; add trigger definitions for absent names; Stage 9 suite green. Gate for all alert WPs.
- **WP-1 D1 flip alert.** Probe + band-exit trigger + severity; boundary/negative/adversarial/determinism tests. Depends WP-0, D9-magnitude slot.
- **WP-2 D2+D3 dependence pair.** Shared metric helper, joint precedence rule, naming per D3; threshold-boundary + co-occurrence + determinism tests. Depends WP-0/WP-1.
- **WP-3 D5 two-driver alert.** Owner thresholds over existing outputs; threshold-matrix + degenerate-driver tests. Depends WP-0. (Sector-scope extension waits on WP-5.)
- **WP-4 D4 closure.** Negative test pinning absence + spec record; or contract-expansion WP if (a) funded (needs D7 provenance).
- **WP-5 D6 chains (only if (a) funded).** Per-sector packages (non-financial / bank / holding+P/NAV), each with mapping + fields + validation + tests; P2 tests re-baselined inside this WP only.
- **WP-6 D7+D9 infrastructure.** Attestation field + ordering rule + violation response (D7-b); in-code registry + cutoff `as_of` (D9-a); boundary/missing-date/version-selection tests. Last.
- Each WP ends with the focused Stage 7 + Stage 9 suites and a diff confined to its scope.

## D. Decisions the Owner Must Approve (explicit choices + proposed defaults)

| # | Choice | Proposed default (proposal only) |
|---|---|---|
| D1 | Flip inputs/magnitudes/severity | 10% OAT EPS + target-P/E shocks; band-exit; band-distance severity |
| D2 | Dependence metric + 0.60 use | Attribution share; alert at TARGET_PE share ≥ 0.60 |
| D3 | EPS metric + `FORECAST_RISK` fate + revision route | EPS attribution share; retire `FORECAST_RISK`; revision via caller-folded family evidence |
| D4 | Margin support in V1 | Documented non-implementation |
| D5 | Impact/uncertainty scope + thresholds | Two-driver scope; owner thresholds (weights stay unapproved) |
| D6 | Sector chains in V1 | Deferred; two-driver stands |
| D7 | PIT policy + ordering rule | (b) attestation V1, (a) V2 target; rule fixed in follow-up |
| D8 | Naming strategy + flag sufficiency | (c) spec adopts emitted names; above/below preserved; new triggers defined |
| D9 | Registry + `as_of` | In-code registry; `as_of` = data cutoff; DB registry V2 direction |

## E. Factual Documentation Corrections Resolvable Without Policy Decisions

Done in P19/P21/P24 (sections 42-44, 47-49, 54-55, 72, 74, 77-79, 81, 83-85). Remaining documentation-only items: (1) Section 26 still presents `POSITIVE_FORECAST_REVISION` as usable probability evidence — needs a conforming note pointing at the caller-folding route once D3 is approved (blocked on D3, not on any formula); (2) `POOR_DATA_QUALITY` recorded as trigger-less (needs D8 trigger to close); (3) threshold-provenance notes (already in section 48; no numbers ratified). Nothing here changes financial policy.

## F. Blocked vs Resolvable From Existing Evidence

- **Resolvable now without new evidence:** D4 (via non-implementation), D8 naming *record* (mapping already complete — only the strategy choice is pending), D5 two-driver scope, D2/D3 metric *shapes* (attribution shares computable today; only approval missing).
- **Genuinely blocked:** D1 magnitudes/severity (no spec/code value exists — must be decided, not discovered); D4-proxy and D9-alternative (no evidence-supported instantiation — reported empty); D6 mapping/fields (nothing in the project); D7 ordering rule and violation response (no temporal contract); D9 `as_of` (needs D7); any threshold value anywhere (all engine constants, none spec-ratified).
- **Smallest bounded follow-ups if the owner defers:** (i) fix the D7 date-ordering rule + violation response (one contract note); (ii) confirm the industry-code value set present in Stage 1 data (read-only inventory for a future D6 mapping — no taxonomy invented).

---

## Six-Layer Validation (adapted to read-only design task)

1. **Unit/formula (static, fresh).** Traced every cited formula: `calculate_forward_pe`/`calculate_forward_pe_fair_value`/`calculate_nav_fair_value`/`calculate_margin_of_safety` (`models.py:5-35`), `_select_target_pe` (`:256-269`), `_resolve_probabilities` (`:272-318`, family-only, direct adjustments rejected), `_eps_flags` (`:363-371`), `_scenario_sign_change_flags` (`:374-384`, per-scenario transitions), `_expected_fair_value` (`:392-396`, requires 3 non-None), `_scenario_dispersion` (`:399-406`), `_valuation_status` (`:409-419`), `_valuation_confidence` (`:422-434`, 0.40/0.20/0.20/0.20 blend — unapproved), `_confidence_label` (`:437-447`), `_valuation_risk` (`:450-466`), `_driver_analysis` (`:469-498`, hardcoded two drivers, 0.10 OAT, 1e-9 guard), `_alerts` (`:501-535`, exact emitted vocabulary). Gaps identified without invention: D1 flip, D2/D3 shares, D5 combination, D6 chains, D7 ordering. No formula created.
2. **Contract/boundary (static, fresh).** `calculate_valuation` signature (`:57-79`) re-verified: no fundamental-score, trend, revision, or margin input; `probability_confidence` independent (default 50.0); `ValuationResult` (`schema.py:19-50`) re-verified. Downstream compatibility: Stage 9 consumes `alerts`/revision-trend today (`decision/engine.py:42,65,299`). Every option's contract delta recorded in matrix B; nothing changed.
3. **Production-path/integration (static trace, fresh).** `calculate_valuation` → `_select_target_pe` → scenario loop → sign flags → expected FV/status → order warning → flag block (`:158-169`) → confidence/risk/drivers → `_alerts` → `ValuationResult`. Stage 5→7 link: EPS forecasts + reliability in, revision direction not carried. Stage 7→9 link: alerts/flags/ranking out. No path modified.
4. **Adversarial/negative (enumerated as future requirements, not claimed runs).** Missing/None/NaN/zero/negative EPS; sign-change vs `NOT_APPLICABLE`; degenerate denominator; empty-driver early return; reliability `None`/clamped; post-cutoff/future/missing dates; threshold-exact boundaries (0.60, 40.0, 1.50, owner thresholds); co-firing precedence; consumer-parse under each D8 option. None executed in P25.
5. **Regression/full suite (carried forward from P24, labeled as such — NOT freshly executed).** P24 fresh runs (`.venv/Scripts/python.exe`, 2026-10-14): `test_stage7_valuation.py` → 2 failed / 50 passed; + `test_stage9_decision.py` → 2 failed / 63 passed / 52 warnings; full suite (`--ignore=test_codal_pdf_extraction.py`) → 2 failed / 900 passed / 1 skipped (missing Codal PDF fixture) / 1068 warnings. The 2 failures are the known P2 tests, intact (verified present lines 406/425) and expected — not regressions. No skipped/excluded test treated as passing.
6. **Independent audit (fresh).** Every behavior claim cross-checked against the cited code/spec/test location in this task (zero-ref greps re-run for `FORECAST_RISK`, `POSITIVE_FORECAST_REVISION`, `POOR_DATA_QUALITY`, `POINT_IN_TIME_WARNING`, `effective_from`/`parameter_version` — all zero in `src`). P22's brief re-verified and extended: deltas are P23/P24 findings (S72 token, S74 precision, S81 indirection, S83 strike, S84 semantics) and the section-26 inconsistency now recorded in E. No decision implicitly selected: all recommendations are single-paragraph proposals explicitly tagged, each paired with neutrally presented alternatives and a commensurate no-change option.

## Owner Decision Summary

Nine decisions, one review. The package proposes: approve the two-driver world as V1 (D2/D3/D5 shares over existing outputs, D6 deferred, D4 absent), freeze the emitted alert vocabulary into the spec (D8-c), add the flip probe at 10% OAT (D1-a), run V1 on caller attestation for PIT (D7-b) with an in-code cutoff-based parameter registry (D9-a), and aim per-observation provenance plus a DB registry at V2. Each row of table D is independently approvable/rejectable; the safe order is D8 → D6 → D1+D2+D3 → D5 → D4 → D7+D9. **No implementation starts until the owner approves; Stage 7 is not complete and not frozen.** Work stops after appending this report.
===================================================================
# P26 — Independent Audit of the D1–D9 Decision Package

**Date (UTC):** 2026-10-14
**Nature:** READ-ONLY independent audit of the P25 decision package. No policy chosen or implemented; no source, test, schema, configuration, dependency, migration, or specification file modified; no prior report edited. No formula, threshold, severity, mapping, default, or date rule invented. The only write is this audit, appended to `temp_report2.md`.
**Evidence base:** full P25 report + P17–P24 (P23 2026-10-14, P24 corrections); `07_Stage7_Valuation.md` (sections 10, 23-24, 26, 42-57, 64-69, 77-79, 83, 85); `src/valuation/engine.py` (lines 57-79, 158-250, 256-535 — including 186-255, which P25 cited but had not read), `models.py`, `parameters.py`, `schema.py`; `src/forecast/repo.py:137-148`; `src/decision/engine.py` (full `make_decision` input/output trace, lines 31-280); `src/tests/test_stage7_valuation.py` (P2 tests at 406/425, `make_forecast` at 10, `test_p6_cutoff_pit_limitation_pinned` at 937-953 — body read); fresh diagnostic probe below. No test suite was executed; the probe is a diagnostic, not test evidence.

---

## 1. Nine-Row Verdict Table

| Item | Verdict | One-line rationale |
|---|---|---|
| D1 Flip risk | PARTIALLY_READY | Question/options explicit; recommended probe underspecified (shock sign, severity mapping) — G2 |
| D2 Multiple dependence | PARTIALLY_READY | Question/options explicit incl. no-change; recommended metric degenerate (always 50/50, 0.60 unreachable) — G1 |
| D3 EPS dependence + revision | PARTIALLY_READY | Naming options + route explicit; share metric shares D2's degeneracy; trend→family mapping rule missing — G1 |
| D4 Margin risk | READY_FOR_OWNER_DECISION | Contract gap proven; (a)/(b)/(c) explicit; (c) closable as-is |
| D5 Impact × uncertainty | PARTIALLY_READY | Tautology honestly flagged but exact degeneracy (identical outputs per driver) undisclosed — G1 |
| D6 Sector chains | READY_FOR_OWNER_DECISION | Absent inputs/mapping evidenced; (a)/(b) explicit; section-58 constraint + test handling stated |
| D7 PIT enforcement | PARTIALLY_READY | Mechanism choice answerable; exact ordering rule + violation response missing (declared follow-up) |
| D8 Alert names | PARTIALLY_READY | Mapping complete/accurate; strategy options explicit; Stage-9 consumer premise false — G3 |
| D9 Versioning | READY_FOR_OWNER_DECISION | Mechanism + `as_of` options explicit; cutoff fallback verified in code; trade-offs disclosed |

## 2. Defects (statement → contradiction/evidence → risk → smallest correction)

**G1 — D2-(a)/D3-(a) attribution-share metrics are degenerate (MATERIAL).**
P25 states (D2-3/D2-4): "attribution share: `TARGET_PE` share of `impact_pct` … alert when share ≥ 0.60 (explicitly approving the existing constant)" / "Directly computable from shipped outputs".
Verified contradiction: `_driver_analysis` (`engine.py:478-495`) applies symmetric +10% one-at-a-time shocks to a multiplicative identity (FV = EPS × PE), so both effects are always equal. Fresh probe (project interpreter, EPS 150/180/210, historical 7.0) returned `driver_impact == {'EPS': 50.0, 'TARGET_PE': 50.0}` exactly, with `driver_uncertainty` 40.0/40.0 (identical by construction, `engine.py:496`) and `review_priority` 20.0/20.0. A 0.60 threshold is therefore unreachable short of rounding dust; D2-(a) as written can never fire, and D3-(a)'s EPS-share mirror has the same fate. D5-(a) inherits it: review outputs are identical per driver, so any threshold fires for both drivers or neither — P25's "near-tautological" (D5-5) understates an exact degeneracy.
Risk: owner approving (a) would enact never-firing alerts — silent false negatives presented as coverage.
Smallest correction: add the degeneracy finding to D2/D3/D5; revise the proposals (e.g., scenario-spread attribution or asymmetric-shock metric — list as unapproved sketches, do NOT select); enumerate the D2/D3 joint precedence alternatives (both-fire vs higher-share-wins vs D2-priority) instead of naming the rule without options.

**G2 — D1-(a) shock direction and severity mapping unspecified (MATERIAL).**
P25 states (D1-4): "One-at-a-time 10% shocks to forecast EPS and target P/E; alert when the recomputed status leaves its band; severity from band distance."
Missing evidence: `_driver_analysis` shocks upward only (`1.0 + p`, `engine.py:481,484`); a flip probe needs a defined sign set (±, or stated one-sided), otherwise half the flip directions are untestable. "Band distance" severity has no mapping (which bands, what distances, what severities).
Risk: unimplementable-as-written approval; implementer would silently choose directions/severities = hidden policy.
Smallest correction: specify the shock sign set and a severity table skeleton (values left to owner), or downgrade (a) to a sketched option and mark the rule as follow-up alongside D7's.

**G3 — D8's consumer-compatibility premise is factually wrong (MATERIAL to cost assessment).**
P25 states (D8-5, D8-8, matrix B): "Stage 9 parses these outputs today" / "`alerts` and `valuation_risk_flags` are public outputs … read by Stage 9".
Verified contradiction: full trace of `DecisionEngine.make_decision` (`decision/engine.py:31-280`) shows Stage 9 reads `valuation_status`, `forecast_reliability_score`, `valuation_risk_level`, `valuation_confidence`, `valuation_data_quality`, `margin_of_safety_pct`, `data_cutoff_datetime`, and metadata (`scenario_dispersion`, `expected_upside`) — 14 `valuation_result.*` references, zero to `alerts`, `valuation_risk_flags`, or `valuation_driver_ranking` (grep-verified). Likewise the D6 claim that ranking changes affect "Stage 9 and dashboards": the Stage 9 half is unsupported (dashboard consumption unverified either way).
Risk direction: this overstates rename cost — an alert-vocabulary rename breaks no verified current consumer (only future consumers and audit trails). The error is conservative, not dangerous, but the owner would misprice options (a) vs (c).
Smallest correction: replace the Stage-9-parses-alerts claim with the verified field list; restate rename risk as future-consumer/audit-trail; mark dashboard consumption as unverified.

**M1 — P25 evidence-base overclaims a full read (MINOR, corrected during this audit).**
P25 claims "`src/valuation/engine.py` (full read, lines 57-535)" but the cited construction block (201-250: MODEL_VERSION/CONTRACT_VERSION wiring, cutoff fallback at 215, metadata keys) was never read in P25. Verified now in P26: `model_version=MODEL_VERSION` (211), `calculation_timestamp` (212), cutoff fallback (215), `scenario_probability_sum` (242), `nav_per_share_received` (247), `pit_inputs_required` (248) — all as cited. No content change needed; record the verification here.

**M2 — Test-proposal coverage gaps (MINOR, non-blocking).**
D1 tests omit integration; D7 tests omit determinism. Add one line each; does not block review.

## 3. Cross-Item Contradictions

- **C1 (G1 fallout):** D2-(a) ⊕ D3-(a) ⊕ D5-(a) all build on `_driver_analysis` outputs that are exactly symmetric (50.0/50.0, verified by probe) — the three proposals share one degenerate foundation. Fixing the metric fixes all three consistently; approving any one as written silently approves a dead alert.
- **C2 (G3 fallout):** D8's rename-cost argument and D6's ranking-change consumer argument both lean on Stage-9 consumption that does not exist for those fields. Correction lowers D8-(a) cost and removes half of D6's stated consumer impact; matrix B's "migration required" cells for alert renames need the same correction.
- **C3 (D3 route assumption):** P25's "revision via caller-folded family evidence" assumes a ternary trend (UPWARD/DOWNWARD/MIXED, `repo.py:137-148`) can be folded into family score distributions (bear/base/bull scores in [0,1], `engine.py:286-290`). No such mapping rule exists — flagged here as a missing rule, not a contradiction; add it to D3's required inputs.
- **C4 (consistent, no action):** D7-(b) + D9-(a) pairing is coherent (cutoff exists on every valuation path, fallback verified at `engine.py:215`); section-26 note correctly deferred to D3 approval (P25-E1).

## 4. Owner Decisions Genuinely Ready for Approval

- **D4** (approve (c) documented non-implementation, or fund (a)/(b)).
- **D6** (approve (b) deferral with two-driver V1 standing and P2 chain tests remaining red by design, or fund (a) with mapping + field list).
- **D9** (approve (a) in-code registry with cutoff `as_of` + DB direction, or select (b)/(c)).
- **D8 strategy choice**, conditional on accepting the G3 cost correction (no new evidence needed).

## 5. Decisions Not Ready (exact missing evidence)

- **D1:** shock sign set + severity mapping (G2). No code/spec value exists; must be decided, then specified.
- **D2/D3:** non-degenerate metric definition + precedence alternatives (G1). Current proposals cannot fire.
- **D5:** acknowledgment of exact degeneracy + owner thresholds (G1). Thresholds are the decision itself, but the package must disclose what they operate on.
- **D7:** ordering rule + violation response (declared follow-up; mechanism itself is decidable).
- **D8:** corrected cost assessment (G3) — one-paragraph fix, then decidable.

## 6. Overall Verdict

**NEEDS_TARGETED_REVISION** — gaps G1 (D2/D3/D5 metric degeneracy + precedence options), G2 (D1 shock sign/severity), G3 (D8 consumer-premise correction). All three are bounded text revisions requiring no new investigation: the evidence is cited in this audit. After them, the package is READY_FOR_OWNER_REVIEW. No re-audit of D4/D6/D9 is needed.

## 7. Conditional Implementation Sequence (proposal, NOT executed)

On owner approval: WP-0 D8 vocabulary freeze (with corrected cost basis) → WP-1 D1 (specified signs/severity) → WP-2 D2+D3 pair (revised metric + precedence) → WP-3 D5 (revised scope note) → WP-4 D4 closure → WP-5 D6 only if (a) funded → WP-6 D7+D9 infrastructure last. D4-(c) and D9-(a) may proceed first as no-regret items since their approvals need no other decision. Each WP ends with focused Stage 7 + Stage 9 suites; P2 tests are re-baselined only inside WP-5, never before.

---

## Six-Layer Validation

1. **Formula/unit evidence audit (fresh static + one diagnostic probe).** Re-derived `_driver_analysis` math (`engine.py:478-497`): symmetric +10% OAT shocks on FV=EPS×PE ⇒ equal effects ⇒ shares exactly 50/50 (rounding dust only); uncertainty identical per driver by construction (`:496`); review identical ⇒ both-or-neither firing. Probe executed with project interpreter: `python -c` building `CompanyForecastResult` (EPS 150/180/210, `make_forecast` shape from `test_stage7_valuation.py:10-24`) → `ValuationEngine().calculate_valuation(1,101,'PETROCHEMICAL',1000.0,f,historical_pe_values=[7.0])` → `ranking ['EPS','TARGET_PE']`, `impact {'EPS':50.0,'TARGET_PE':50.0}`, `uncertainty 40.0/40.0`, `review 20.0/20.0`. Upward-only shock confirmed (`1.0+p`, `:481,484`). All other cited formulas spot-verified against P25's line references.
2. **Contract/boundary audit (fresh static).** Signature re-verified: no margin/trend/revision/fundamental/score inputs (`:57-79`); `ValuationResult` fields as cited (`schema.py:19-50`). Stage-9 consumption enumerated field-by-field (14 references; alerts/flags/ranking absent) ⇒ G3. D4's hard contract gap reconfirmed (no margin field anywhere on the boundary).
3. **Production-path/integration audit (fresh static).** Construction block read for the first time (186-250): `flags.extend(alerts)` (195) merges severity alerts into the flag channel (corroborates P25's channel analysis; no defect); version/cutoff/metadata wiring as cited (211-212, 215, 242, 247-248) ⇒ M1 closed. Stage 5→7 (EPS + reliability in; revision not carried) and Stage 7→9 (status/reliability/risk/confidence/metadata out) paths re-traced; nothing modified.
4. **Adversarial/missing-data/PIT audit (fresh static).** P25's missing-data rules match guards (`models.py:5-16`; `engine.py:197-199` NOT_APPLICABLE; `:476-477` empty-driver; `:489-490` denominator/clamp). PIT claims match code (bare floats `:70-72`; dates normalized-only `:104-108`; cutoff fallback `:215`). `test_p6_cutoff_pit_limitation_pinned` body read (937-953): pins late-valuation acceptance + no PIT flag — P25's citation accurate.
5. **Regression-test evidence audit (no suite executed; probe is diagnostic only).** P25's carried-forward counts accepted as correctly labeled (fresh-run claims absent). Presence re-verified by grep: P2 tests at `test_stage7_valuation.py:406,425`; `make_forecast` at :10; `test_p6_cutoff_pit_limitation_pinned` at :937. Zero-ref greps re-run in P26 scope: `FORECAST_RISK`, `POSITIVE_FORECAST_REVISION`, `POOR_DATA_QUALITY`, `POINT_IN_TIME_WARNING`, `effective_from`/`parameter_version` — all zero in `src`; `alerts|valuation_risk_flags|driver_ranking` — zero in `src/decision/engine.py`. No failure misrepresented; no skip treated as pass.
6. **Independent consistency audit (fresh).** P25 cross-checked against P17-P24, spec, code, tests. Consistent: zero-ref claims, S72/S74/S81/S83/S84 correction records, section-26 deferral note, D7/D9 pairing, D8-first ordering, no freeze/readiness overclaim, proposals tagged. Defects found: G1 (material, probe-proven), G2 (material, code-proven), G3 (material, trace-proven), M1 (closed here), M2 (trivial). No D1-D9 policy selected in this audit; all P25 recommendations remain proposals.

**Confirmation:** no implementation or policy choice made; no file changed except this appended audit; the two P2 failing tests untouched; no remote operations; Stage 7 remains unfrozen. Stop after appending.
===================================================================
# P27 — Corrected D1–D9 Owner Decision Package and Final Readiness Review

**Date (UTC):** 2026-10-14
**Nature:** Bounded documentation/report task applying P26's authoritative audit. No financial policy implemented; no runtime behavior changed; no proposal converted into approved policy. No source, test, schema, migration, dependency, configuration, or specification (`07_Stage7_Valuation.md`) file modified. P25 and P26 preserved untouched as historical records. The only write is this package, appended to `temp_report2.md`.
**Authoritative context:** P25 + complete P26 + P17–P24; spec sections 10, 23-24, 26, 42-57, 64-69, 77-79, 83, 85; `src/valuation/engine.py`, `models.py`, `parameters.py`, `schema.py`; `src/forecast/repo.py:137-148`; `src/decision/engine.py` (31-320) + `src/decision/schema.py` (7-60); `src/tests/test_stage7_valuation.py` (10, 406, 425, 937-953); `src/tests/test_stage9_decision.py` (186-224). P26 treated as authoritative on P25's defects; full P25 investigation not repeated.

---

## 1. Correction Log (P26 → P27)

**G1 — Withdrawn: 0.60-on-impact-shares as a working D2/D3 formula.**
P25 recommended alerting when the `TARGET_PE`/`EPS` share of `driver_impact` crosses 0.60. P26's probe proved the shares are exactly 50.0/50.0 by construction: `_driver_analysis` (`engine.py:478-495`) applies symmetric +10% one-at-a-time shocks to the multiplicative identity FV = EPS × target P/E, so both effects are always equal (rounding dust only). Uncertainty is identical per driver by construction (`:496`), hence `review_priority` is identical too (probe: 20.0/20.0). A 0.60 threshold is unreachable; the proposal could never fire. The existing metric therefore cannot distinguish EPS dependence from multiple dependence, and D5's two-driver inputs cannot discriminate between drivers. `high_dependence_share = 0.60` stays inert (verified: exactly 1 reference in `src`, its own declaration) and is NOT activated. No claim is made that D2/D3 alerts would work on those shares unchanged.

**G2 — D1 made decidable.**
The flip probe is now separated into six explicit fields (variables; direction; magnitude; flip definition; severity; missing-data/NOT_APPLICABLE behavior). The existing 10% upward shock is restated as an unapproved implementation constant for driver analysis, proposal-only. Severity template below carries named categories with BLANK numerics (no band-distance mapping invented). Integration tests added to the test plan. Any field still needing an owner value is marked NOT READY FOR IMPLEMENTATION.

**G3 — Downstream-consumer evidence corrected (freshly re-verified this task).**
P25 claimed Stage 9 parses `alerts`/`valuation_risk_flags`/`valuation_driver_ranking`. Full trace of `DecisionEngine.make_decision` (`decision/engine.py:31-320`) shows Stage 9 reads exactly: `valuation_status` (:57), `forecast_reliability_score` (:58-62), metadata `scenario_dispersion`/`expected_upside` (:118, :242, :262), `valuation_risk_level` (:141, :243, :271, :279), `valuation_data_quality` (:229), `valuation_confidence` (:236, :280), `data_cutoff_datetime` (:250), `margin_of_safety_pct` (:242, :262). Zero references to `alerts`, `valuation_risk_flags`, or `valuation_driver_ranking` (grep-verified). `evidence_summary` (:296-307) carries only derived states (no alert tokens); `conflicts` are Stage-9-generated tokens (:88-120, :223). The in-repo dashboard consumes `FinalDecisionResult` (`decision/schema.py:7-60`; contract test at `test_stage9_decision.py:186-224`), whose fields carry no Stage 7 alert tokens or driver ranking. Corrected position: renaming alert tokens breaks NO verified current consumer; remaining risk is future-consumer compatibility + audit/history continuity + off-repo consumers (outside the repo, addressable only by consumer survey).

**C1 — Shared degenerate foundation recorded once, fixed once.**
D2-(a), D3-(a), D5-(a) all built on the same symmetric `_driver_analysis` outputs; the G1 withdrawal covers all three consistently. Precedence alternatives for D2/D3 co-occurrence are now enumerated without selection: (P-both) both alerts fire independently; (P-priority) a defined rule selects one (rule itself TBD); (P-defer) alerts held until the metric is proven.

**C2 — Consumer matrix cells corrected.**
Alert-rename row: "no verified current breakage; migration = future consumers + audit continuity." D6 ranking-content row: "Stage 9 unaffected (verified); in-repo dashboard unaffected (verified via Stage 9 contract); off-repo consumers unknown."

**C3 — Revision-mapping rule stated as missing.**
`revision_trend` yields UPWARD/DOWNWARD/MIXED (`repo.py:137-148`); family evidence requires bear/base/bull score distributions in [0,1] (`engine.py:282-294`). No mapping rule exists. Presented as an explicit owner decision or bounded design task (R4c); no mapping invented.

**M2 — Test-plan lines added.**
D1: integration cases (flip alert → downstream status path; alert-vocabulary emission into `alerts` channel). D7: determinism cases (identical dates ⇒ identical enforcement outcome across repeated runs).

## 2. Nine Decision Records

**D1 — Assessment flip risk.** Verified: no flip output exists; status transitions computed (`_valuation_status`, `:409-419`); 10% EPS shock moves ATTRACTIVE→FAIR silently (P2 test). Unresolved: variables, direction, magnitude, flip definition, severity, missing-data rule. Options: (a) specified OAT probe sketch — variables {forecast EPS, target P/E}, directions {−, +} both required, flip = status band exit, severity = template below, missing/NOT_APPLICABLE ⇒ no alert; ALL numerics blank; (b) owner-specified bespoke set; (c) defer (no flip alert in V1). PROPOSAL — NOT APPROVED: (a) as structure, with every numeric left blank; implementation NOT READY until owner fills values. Risks: over/under-trigger at band edges; joint-shock fragility understated under OAT. Contract: +1 alert name (additive). Tests: boundary just-flips/just-holds; negative stable-status; adversarial NaN/None/negative-EPS/sign-change/zero-target-PE; determinism; integration (emission into `alerts`; downstream status path). Depends: D8 name, D9 magnitude versioning, D2/D3 precedence. Decision statement: "Approve probe structure (a) and fill direction/magnitude/severity values, or select (b)/(c)."

Severity template (names only; boundaries BLANK by instruction):
| Severity | Textual trigger (owner-completable) | Numeric boundary |
|---|---|---|
| INFORMATIONAL | Minor band-edge movement without band exit | BLANK |
| ELEVATED | Band exit under small shock | BLANK |
| HIGH | Multi-band exit or exit under minimal shock | BLANK |

**D2 — Multiple dependence.** Verified: no formula; 0.60 dead constant; G1 withdrawal above. Unresolved: metric definition + threshold + precedence. Options: (i) retain V1 limitation, emit nothing (only implementation-ready option); (ii) scenario-spread attribution study (sketch: attribute bull–bear FV spread to EPS path vs multiple path; needs spread-decomposition rule, missing-data rule, thresholds — UNVALIDATED); (iii) asymmetric-shock/elasticity study (sketch: directional/unequal shocks, elasticity ratio; needs shock design, denominator guard, thresholds — UNVALIDATED). Sketches are mathematically describable, NOT financially validated. PROPOSAL — NOT APPROVED: (i) now; commission at most one of (ii)/(iii) as a bounded study. Risks: denominator degeneracy; cheap-vs-expensive conflation under one threshold. Contract: +1 name if pursued. Tests: threshold-exact triples; degenerate denominator; None-factor cases; determinism; negative EPS-dominant silence. Depends: D3 precedence (P-both/P-priority/P-defer), D8, D9. Decision: "Approve (i), or commission (ii) or (iii) as a study, or define an alternative metric."

**D3 — EPS dependence + revision routing.** Verified: no formula; `FORECAST_RISK` spec-only (0 refs); revision direction lives Stage 5→9 only, nothing enters `src/valuation` (S83 struck in P24). Unresolved: metric shape; naming fate; revision route + mapping rule. Options: metric (share-sketch subject to G1 caveat / reliability-weighted sketch — both UNVALIDATED) or retain-limitation; naming (N1 keep `HIGH_EPS_DEPENDENCE`, retire `FORECAST_RISK`; N2 two distinct triggers; N3 keep `FORECAST_RISK` only) — presented neutrally, NO proposal (evidence favors none); route (R-a caller-folded `FORECAST_DIRECTION` family evidence + mapping rule TBD; R-b new dated revision input; R-c revision stays Stage 5→9). No proposal on naming/route beyond listing; evidence supports no option over another. Risks: share/reliability conflation; double-signaling with `LOW_FORECAST_RELIABILITY`; invented mapping. Contract: +1 name; §79 rewrite to chosen name; §26 conforming note. Tests: threshold triples; reliability None/40.0 boundaries; co-occurrence precedence; family-channel revision shift; negatives. Depends: D2, D8, D9. Decision: "Choose metric path (limitation/study), naming N1/N2/N3, and route R-a/R-b/R-c."

**D4 — Margin assumption risk.** Verified: zero refs; NO margin/revenue/cost field anywhere on the Stage 7 boundary (signature `:57-79`, schema 19-50) — finding stands, not reopened. Options: (a) contract expansion with dated, validated margin series; (b) owner-defined proxy (none exists); (c) documented non-implementation. PROPOSAL — NOT APPROVED: (c). Risks: proxy circularity; undated-series lookahead (D7). Contract: (c) none; (a) new input + migration. Tests: (c) negative pinning absence; (a) missing/stale/sign-change/boundary/determinism. Depends: D7, D9, D8 under (a). Decision: "Approve (c), or fund (a) with a defined margin source, or define (b)."

**D5 — Impact × uncertainty.** Verified corrected: ingredients exist for {EPS, TARGET_PE} only and are exactly symmetric (G1) — the alert as previously sketched would fire for both drivers or neither. Options: (i) informational-only (keep `review_priority` output, no alert — only safe immediate posture); (ii) owner-threshold alert with disclosed both-or-neither behavior; (iii) defer to D6 sector scope. PROPOSAL — NOT APPROVED: (i), with (ii)/(iii) as owner alternatives. No 0.5/0.3/0.2 weight ratified. Risks: weight laundering; product-form dominance artifacts. Contract: +1 name under (ii). Tests: threshold matrix; one-high silence; empty-driver; determinism. Depends: D6 (scope iii), D8, D9. Decision: "Approve (i), or set thresholds under (ii) accepting disclosed limits, or choose (iii)."

**D6 — Sector chains + P/NAV.** Verified (not reopened): two hardcoded drivers (`:488`); no `industry_code` branching; `nav_per_share` metadata-only (`:247`); `calculate_nav_fair_value` unwired (`models.py:19-23`); P2 chain test still fails by design. Section-58 rule stands: Stage 7 consumes Stage 5 EPS, never rebuilds EPS from a new share count. Options: (a) implement three chains with owner-approved mapping + new chain fields + EPS-consumption validation; (b) defer, two-driver V1 stands. PROPOSAL — NOT APPROVED: (b). Risks: invented taxonomy; contract-shape change (ranking content, public output §69). Contract (corrected per C2): Stage 9 + in-repo dashboard unaffected (verified); off-repo unknown. Tests: per-sector chains; unknown-code fallback to two-driver (explicit, never guessed); partial inputs; NAV ≤ 0; determinism; P2 re-baseline ONLY inside funded (a). Depends: D7 provenance, D9, D8. Decision: "Approve (b), or fund (a) with mapping + field list."

**D7 — Point-in-time enforcement.** Verified: bare-float series (`:70-72`); dates normalized-only (`:104-108`); `pit_inputs_required` informational (`:248`); P19 struck §85 PASS; P6 test pins silent late-date acceptance (body re-read: 937-953). Options with guarantees: (a) per-observation provenance + boundary enforcement — guarantees caught violations; does NOT guarantee upstream date truth; heaviest migration. (b) caller attestation + ordering rule — guarantees a recorded, form-validated assertion; does NOT guarantee truth; NOT equivalent to mechanical enforcement; residual leakage = false attestation undetectable downstream; must ship labeled as limitation. (c) documented V1 limitation — guarantees nothing; cheapest; backtests caller-responsible. PROPOSAL — NOT APPROVED: (b) for V1 with explicit limitation label, (a) as V2 direction. Owner/design-spec MUST still determine: ordering invariants (valuation date vs cutoff vs publication date vs report version vs observation date); violation response (reject/downgrade/flag); missing-date/provenance handling; backtest as-of selection. Tests: post-cutoff handling per rule; date-equal boundary; missing dates; future valuation; determinism (M2 added); pre-cutoff untouched negatives. Depends: D9 pair; D6 inputs; D8 warning name. Decision: "Approve mechanism (a)/(b)/(c); and either fix the four rule items now or delegate them to an approved design spec."

**D8 — Alert names + triggers.** Verified mapping (spec §49/54-55 vs `_alerts` `:511-534` + flags `:162-169`; G3-corrected consumer position). Options: (a) rename outputs to spec names (no verified current breakage — corrected; costs: audit-history discontinuity, above/below merge loses direction, future-consumer migration); (b) alias both (compatible; duplicated vocabulary; alias severity TBD); (c) spec adopts emitted names (spec-only change; preserves direction pairs). PROPOSAL — NOT APPROVED: (c). Absent tokens (no triggers invented): `FORECAST_RISK` fate = owner (retire/keep-separate/adopt); `POSITIVE_FORECAST_REVISION` = route decision (D3); `POOR_DATA_QUALITY` = trigger TBD; `POINT_IN_TIME_WARNING` = gated on D7 rule. Flag-sufficiency (does flag-level satisfy §49?) = explicit owner ruling, options: sufficient / promote-with-severity / insufficient. Tests: per-name present/absent; above/below distinguishability; Stage 9 suite green; alias-compat under (b); per-trigger negatives. Depends: unblocks D1-D5/D7 expression. Decision: "Approve strategy (a)/(b)/(c), rule flag-sufficiency, and disposition each absent token."

**D9 — Parameter/model versioning.** Verified: fixed constants only (`parameters.py`); `effective_from`/`parameter_version` 0 refs; §65 store absent; P14 design = proposal only. Cutoff fallback VERIFIED (`engine.py:215`: cutoff or forecast cutoff) — kept distinct from an approved `as_of` policy; a present cutoff field does not date the benchmark series, so it establishes no PIT correctness. Options: (a) in-code registry; (b) DB-backed §65 table; (c) status quo constants. PROPOSAL — NOT APPROVED: (a) for V1 with `as_of` = data cutoff (proposal, needs approval), (b) as V2 direction. Risks: history rewrite without as-of; boundary off-by-one; unpinned runs. Contract: (a) stable surface, MODEL_VERSION becomes version key; (b) new schema object + migration. Tests: cross-boundary selection; effective-date correctness; pinned determinism; DB round-trip under (b). Depends: D7 pair; supplies D1-D6. Decision: "Approve mechanism (a)/(b)/(c) and the `as_of` rule."

## 3. Corrected Consumer Matrix (Stage 5 → Stage 7 → Stage 9)

| Field / signal | Producer | Stage 9 reads? (verified) | In-repo dashboard? (via Stage 9 contract) | Note |
|---|---|---|---|---|
| `valuation_status` | S7 `_valuation_status` | YES (:57) | YES (contract field) | Rename-sensitive; covered by D8 |
| `forecast_reliability_score` | S5→S6→S7 input | YES (:58-62) | YES | — |
| `valuation_risk_level` | S7 `_valuation_risk` | YES (:141…) | YES (`valuation_risk`) | — |
| `valuation_confidence` | S7 `_valuation_confidence` | YES (:236, :280) | YES | — |
| `valuation_data_quality` | S7 clamped input | YES, internal gate (:229) | Not asserted in contract test | Internal use |
| MOS / `expected_upside` | S7 FV math | YES (:242, :262) | YES | — |
| `data_cutoff_datetime` | caller / forecast fallback | YES (:250) | Carried (schema field) | Fallback verified `:215` |
| metadata dispersion | S7 `_scenario_dispersion` | YES, internal (:118) | No | Internal use |
| `alerts` (all names) | S7 `_alerts` | NO (0 refs) | NO (no alert-token field in `FinalDecisionResult`) | Rename breaks nothing verified |
| `valuation_risk_flags` | S7 flag block | NO (0 refs) | NO | Same as above |
| `valuation_driver_ranking` | S7 `_driver_analysis` | NO (0 refs) | NO | D6 change safe in-repo; off-repo unknown |
| revision trend | S5 `repo.py` → S9 direct | YES, direct S5→S9 (:42, :65) | YES (`forecast_revision`) | Bypasses S7 entirely |
| scenario probabilities | S7 `_resolve_probabilities` | Only via expected FV | Only via FV | Indirect |

## 4. Decision Readiness Matrix (decision vs implementation, stated separately)

| Item | Decision status | Implementation status |
|---|---|---|
| D1 | READY_FOR_OWNER_DECISION (structure + template complete; fill or defer) | NOT READY (needs owner direction/magnitude/severity values) |
| D2 | PARTIALLY_READY (retain-limitation choosable; metric needs design study) | NOT READY |
| D3 | PARTIALLY_READY (naming/route choosable; metric + mapping rule need design) | NOT READY |
| D4 | READY_FOR_OWNER_DECISION | READY via (c) (no code); (a) needs upstream series |
| D5 | PARTIALLY_READY (posture choosable; alert inherits D2/D6) | NOT READY for alert; informational output already shipped |
| D6 | READY_FOR_OWNER_DECISION | READY via (b) (documented; no code); (a) needs funded WP-5 |
| D7 | PARTIALLY_READY (mechanism choosable; rule content missing) | NOT READY |
| D8 | READY_FOR_OWNER_DECISION (strategy choosable on corrected evidence) | READY via (c) (spec-only); (a)/(b) need WP-0 |
| D9 | READY_FOR_OWNER_DECISION | NOT READY (registry design needs approval per P14) |

## 5. Owner Response Sheet (smallest practical set)

- **R1 (D8):** naming strategy (adopt-engine / alias / rename-to-spec) + flag-sufficiency ruling (sufficient / promote / insufficient) + per-token disposition (`FORECAST_RISK`, `POSITIVE_FORECAST_REVISION`, `POOR_DATA_QUALITY`, `POINT_IN_TIME_WARNING`). Unlocks all alert WPs.
- **R2 (D6):** sector chains: defer (b) vs fund (a: attach mapping + field list). Unlocks D5 sector scope if (a).
- **R3 (D1):** fill severity template (directions, magnitudes, flip definition, numeric boundaries) or select bespoke set or defer. Unlocks WP-1.
- **R4 (D2+D3, adjacent but unmerged):** dependence posture each: retain-limitation vs commission spread study vs commission shock study; precedence P-both/P-priority/P-defer; EPS naming N1/N2/N3; revision route R-a/R-b/R-c (+ mapping rule: owner-defined or commissioned). Unlocks WP-2.
- **R5 (D5):** posture: informational (i) vs threshold-alert with disclosed limits (ii) vs wait-for-D6 (iii). Unlocks WP-3.
- **R6 (D4):** (c) non-implementation vs fund (a)/(b with defined source/proxy). (c) closes WP-4 immediately.
- **R7 (D7):** mechanism (a)/(b)/(c) + four rule items (invariants, violation response, missing-date handling, backtest selection) now or delegated to approved design spec. Unlocks WP-6/D7 half.
- **R8 (D9):** registry (a)/(b)/(c) + `as_of` rule (cutoff proposed). Unlocks WP-6/D9 half.

## 6. Conditional Work Plan (gated; NOT started)

- **WP-0 D8 freeze** (needs R1): apply strategy; Stage 9 suite green; alias-compat test if (b). Gate for WP-1/2/3.
- **WP-1 D1** (needs R1+R3+R8-magnitude slot): probe + severity per template; full boundary/negative/adversarial/determinism/integration matrix.
- **WP-2 D2+D3** (needs R1+R4+R8): metric per commissioned study or limitation pins; precedence implementation; naming + §79/§26 notes.
- **WP-3 D5** (needs R1+R5; sector scope needs R2=(a)): thresholds or informational pin.
- **WP-4 D4** (needs R6): negative pin under (c); expansion WP only if (a)/(b) funded.
- **WP-5 D6** (needs R2=(a)+R7-provenance+R8): per-sector packages; P2 re-baseline ONLY here, never before.
- **WP-6 D7+D9** (needs R7+R8): attestation/provenance + registry + selection tests. Last.
- No-regret early: WP-4 under (c), WP-0 under (c). Each WP ends with focused Stage 7 + Stage 9 suites, diff confined to scope.

## 7. Open Evidence List (genuinely unresolvable from current artifacts)

- **E1 — Owner risk-appetite numerics** (all thresholds, severities, magnitudes, D7 rule values): policy by nature; no evidence to discover.
- **E2 — Upstream margin-series availability/source** (for D4-a): requires upstream owner; absent from Stage 7 evidence.
- **E3 — Off-repo consumers of alert/ranking vocabulary** (for D8/D6 residual risk): outside the repo; in-repo verified clean (matrix §3). Resolvable only by consumer survey, not by code.
- Everything else in R1–R8 is decidable from this package. The industry-code value set in Stage 1 data is NOT listed here: it is a bounded data inventory, commissionable as a task under R2, not an open question.

## 8. Final Verdict

**READY_FOR_OWNER_REVIEW** — G1/G2/G3/C1/C2/C3/M2 are corrected above; no surviving proposal relies on the degenerate 50/50 metrics; all options are understandable and explicitly approvable/rejectable (R1–R8); open items are reduced to E1–E3. P25/P26 stand as history; this package supersedes P25's proposals where they conflict (D2/D3/D5 metrics, D1 structure, D8 costing), with reasons recorded in §1.

---

## Six-Layer Validation

1. **Unit/formula (fresh static; probe carried from P26, labeled).** Degenerate-metric correction confirmed against `_driver_analysis` (`:478-497`): no 0.60 proposal survives; sketches (ii)/(iii) labeled UNVALIDATED, never implied viable-by-computability. Severity template carries BLANK numerics — no band-distance mapping invented. P26 probe (50.0/50.0, 40.0/40.0, 20.0/20.0) cited as prior evidence, NOT re-executed.
2. **Contract/boundary (fresh static).** Corrected field lists verified: S7 boundary (no margin/trend/revision/fundamental inputs, `:57-79`); S9 reads enumerated from code (:57-280); `FinalDecisionResult` carries no alert-token/ranking fields (`decision/schema.py:7-60`); dashboard contract test asserts only derived states (`test_stage9_decision.py:186-224`). Missing-data constraints restated from verified guards; nothing weakened.
3. **Production-path/integration (fresh static).** S5→S7 (EPS + reliability; revision bypasses S7 direct to S9 at `decision/engine.py:42,65`) and S7→S9 (status/reliability/risk/confidence/metadata only) re-traced; `flags.extend(alerts)` (`:195`) noted with channel distinction preserved. Matrix §3 matches code.
4. **Adversarial/negative (design requirements, not runs).** Missing/NaN/None/zero/negative EPS; NOT_APPLICABLE ⇒ no flip/dependence alerts; shock directions {−,+}; co-occurrence P-both/P-priority/P-defer; stale/future/undated data per D7 rule; absent provenance handling. M2 additions present (D1 integration, D7 determinism).
5. **Regression/full suite (no suite executed — report-only correction).** Prior results distinguished: P24 fresh runs vs P25/P26 carried-forward vs static inspection here vs planned WP tests. P2 tests re-verified present this task (`test_stage7_valuation.py:406,425`); zero-ref batch re-run this task (all six tokens still zero/absent as stated; `high_dependence_share` still exactly 1 inert ref; alerts/flags/ranking still 0 refs in decision engine). No failure reclassified; no skip treated as pass.
6. **Independent audit — second pass (fresh, post-draft).** Re-checked every §1 correction against its P26 section and code anchor: G1↔P26-§2-G1 + probe + `:488-497`; G2↔G2 + `:481,484` upward-only; G3↔G3 + 14-ref enumeration + schema/test reads; C1↔probe symmetry; C2↔matrix-vs-code; C3↔`:282-294` vs `repo.py:137-148`; M2↔plans. Verified no surviving sentence relies on 50/50 shares, no numeric invented (template blanks confirmed blank), no policy selected (all proposals tagged PROPOSAL — NOT APPROVED or explicitly neutral), P25/P26 text untouched (diff scope: this section only).

**Confirmation:** no policy chosen or implemented; only this section appended; P2 tests intact; no remote operations; Stage 7 remains unfrozen. Stop after the final readiness verdict.
===================================================================
# P28 — Stage 7 Baseline and Root-Cause Remediation

**Date (UTC):** 2026-10-14
**Nature:** Bounded remediation attempt per P28 — baseline, root-cause trace, fix attempt at actual root causes, re-verification. Pre-check first: NO owner approval of R1–R8 exists anywhere (grep over `temp_report2.md` for approval records: zero; `git log` top is 92612e9 P27; D1–D9 still unresolved). All P28 constraints honored: local only; no remote/Git operations of any kind; no test deleted/skipped/weakened/rewritten; no manufactured inputs, thresholds, formulas, mappings, or severities; Stages 1–6/8–9 untouched; Stage 5 EPS consumed as-is. The only write in this task is this report, appended to `temp_report2.md`.

## 1. Exact Current Baseline (pre-change; tree verified unchanged throughout)

Interpreter: `.venv/Scripts/python.exe` from project root. Exit statuses non-zero where failures exist; no output filtered.

- `python -m pytest src/tests/test_stage7_valuation.py::test_p2_sector_driver_decomposition_missing src/tests/test_stage7_valuation.py::test_p2_required_flip_dependence_alerts_missing -q` → **2 failed in 1.85s, exit 1.** Traces: T1 fails at `test_stage7_valuation.py:422` (`{'NAV','NII','REVENUE'} <= {'EPS','TARGET_PE'}`); T2 fails at `:465` (all 5 required names missing from alerts+flags). T2's own passing asserts confirm adjacent approved constants (`SENSITIVITY_PERTURBATION == 0.10`, thresholds 15.0/5.0) — none approved for alert use.
- `python -m pytest src/tests/test_stage7_valuation.py src/tests/test_stage9_decision.py -q` → **2 failed, 63 passed, 52 warnings in 1.18s, exit 1.** Stage 9 contributes 13/13 passes; warnings are the known `datetime.utcnow()` DeprecationWarnings (P12 scope, untouched).
- `python -m pytest src/tests/ -q -rs --ignore=src/tests/test_codal_pdf_extraction.py` → **2 failed, 900 passed, 1 skipped, 1068 warnings in 99.08s, exit 1.** Skip: `test_codal_extraction.py:307` (real Codal sample PDF unavailable in CI) — carried exclusion, not counted as pass. Only failures repo-wide are the two known P2 tests.

## 2. Root-Cause Traces (production path, not symptoms)

**T1 — sector drivers.** `calculate_valuation` → `_driver_analysis` (`engine.py:469-498`): `drivers = {"EPS": eps_effect, "TARGET_PE": pe_effect}` hardcoded (`:488`); no `industry_code` branching (echoed to metadata only); `nav_per_share` recorded as `nav_per_share_received` (`:247`), consumed by no formula; `calculate_nav_fair_value` (`models.py:19-23`) unwired. Output ranking is therefore always a subset of {EPS, TARGET_PE} for every sector — the test's union can never contain REVENUE/NII/NAV. Intended enforcement: D6 sector chains (spec §§42-44). Root cause: absent owner-approved industry mapping, chain source fields, and chain formulas — D6 unresolved (P27-R2).

**T2 — five alerts.** `calculate_valuation` → `_alerts` (`:500-535`, emits only dispersion/reliability/benchmark/divergence/top-driver families) + flag block (`:162-169`); `flags.extend(alerts)` (`:195`). None of ASSESSMENT_FLIP_RISK / HIGH_MULTIPLE_DEPENDENCE / HIGH_EPS_DEPENDENCE / MARGIN_ASSUMPTION_RISK / HIGH_IMPACT_HIGH_UNCERTAINTY is emitted anywhere in `src/valuation` (0 refs, re-verified). Per-alert root causes: D1 no flip definition/magnitude/severity; D2/D3 no metric (0.60 dead; natural share metric proven degenerate 50/50 in P26); D4 no margin series on the boundary (signature `:57-79`, schema 19-50); D5 no combination rule/thresholds. Root cause: absent owner-approved alert policies — D1–D5 unresolved (P27-R1/R3/R4/R5/R6).

## 3. Fix-Attempt Log (candidate paths examined and rejected with evidence)

- **Path A — wire existing constants (0.10 / 0.60 / 0.5-0.3-0.2) into alert paths.** REJECTED. P27 explicitly withdrew the 0.60-on-shares proposal; P28 forbids manufacturing thresholds/formulas; P26 proved the shares are exactly 50/50, so a 0.60 gate would create never-firing alerts — a disguised absence, violating P28-6.
- **Path B — invent sector mapping, chain fields, margin input, or formulas.** REJECTED. Manufacturing mappings/fields/formulas is explicitly forbidden; chain work additionally risks the §58 EPS-consumption rule; boundary expansion without an approved contract violates frozen-stage discipline.
- **Path C — delete/skip/weaken/rewrite either test.** REJECTED. Explicitly forbidden; would destroy the failing-first pins that guard D1–D6.
- **Path D — partial fix (e.g., wire `nav_per_share` alone for holdings).** REJECTED. Manufactures chain policy without approval and leaves REVENUE/NII red — partial green is concealed failure under P28-6.
- **Result: ZERO file changes.** `git status` shows no modification to source, tests, schemas, specs, or config (only the user's own `stage_7_prompts.md` prompt staging, pre-existing). Absence of a diff IS the compliant outcome here: P28-3's own "genuinely absent policy" branch orders exactly this ("do not disguise that absence with an arbitrary formula … record the rationale").

## 4. Tests Added/Corrected: NONE (with rationale)

All approved Stage 7 behavior is already pinned (50 passing Stage 7 tests, green). Any new behavioral test would either assert unapproved policy (forbidden) or duplicate existing pins. Both failing tests assert their intended protections correctly (traces §1) and need no correction. No test file was touched.

## 5. Post-State Verification (same tree — baseline == final state)

No code changed at any point, so the §1 runs are simultaneously pre- and post-state evidence: named pair 2 failed/1.85s; focused+Stage 9 2 failed/63 passed/52 warnings/1.18s; full suite 2 failed/900 passed/1 skipped/1068 warnings/99.08s; all exit 1 solely on the two known tests. Stage 9 consumer path green (13/13). No new failure; no failure concealed — both still fail loudly with unchanged signatures.

## 6. Six-Layer Validation (each separately)

1. **Unit/formula:** failure assertions re-derived against `_driver_analysis`, `_alerts`, `_valuation_status`, models guards. No formula changed, added, or removed (empty diff).
2. **Contract/boundary:** no signature, schema, output-name, or boundary change (tree clean). Boundary gaps restated, not altered.
3. **Production-path/integration:** both failures traced through the live production path (§2); Stage 9 integration green; Stages 1–6/8–9 files untouched.
4. **Adversarial/negative:** the failing tests' adversarial content (shock-driven flip, wide-EPS risk case, 7-peer/bank/holding variants) executes and fails for the documented reason; passing P6 adversarial tests (NaN/None/zero EPS, ordering, determinism) confirm no adjacent breakage.
5. **Regression/full suite:** exact commands, exit statuses, counts, durations, skip reason above; carried-forward nothing — all freshly executed this task. Skips never counted as passes.
6. **Independent audit of diff + evidence:** final diff scope verified = this section only (0 deletions in `temp_report2.md`; no other file touched). Both failures explained to absent-policy roots and still failing — explained, unconcealed, unweakened.

## 7. Remaining Concrete Blockers (per-test → owner decision)

- **T1 (sector drivers)** → P27-R2: approve (b) defer (test stays red by design) or fund (a) with mapping + field list → WP-5. Nothing else unblocks it.
- **T2 (five alerts)** → P27-R1 (D8 names) + R3 (D1 values) + R4 (D2/D3 metric + precedence + naming + route) + R5 (D5 posture) + R6 (D4) → WP-1…WP-4. Nothing else unblocks it.
- **Further code investigation is closed, not deferred:** every candidate path terminates at explicit policy absence; re-reading code cannot create policy. Per P28-6, failures are neither unexplained (roots proven) nor concealed (still failing, reported). The next action is owner-side: approve R1–R8 values (P27 §5 response sheet). If the owner supplies any R-decision now, the corresponding WP can start immediately under its gate.

## 8. Final Verdict

**BLOCKED ON OWNER POLICY — NO CODE CHANGED.** Remediation attempted end-to-end: fresh baseline recorded, both failures traced to absent-policy roots, all four fix paths examined and rejected on evidence under P28's own constraints, zero files changed, full suite re-verified, pins preserved. Not claimed: Stage 7 complete, frozen, or remediated. Stage 7 remains unfrozen. Stop after this bounded task and its independent audit.
===================================================================
# P29 — Stage 7 Point-in-Time Enforcement

**Date (UTC):** 2026-10-14
**Nature:** Bounded enforcement attempt per P29. P28's report reviewed first (present, §§1–8; not repeated, not discarded — this task builds on its BLOCKED verdict). Tree verified clean at start (only the user's own `stage_7_prompts.md` staging). No R7/R8 owner approval exists (same approval grep as P28: zero records). Constraints honored: no manufactured dates/versions/provenance; no weakened tests; no gratuitous frozen-stage changes; no unrelated-PDF substitution; no remote operations. The only write is this report.

## 1. Input-Path Inventory (every Stage 7 input where dates/provenance could matter)

- `current_price`: undated float; dated only via echoed `market_price_date` metadata — never validated (`engine.py:104-108,213-214`).
- Forecast EPS + `forecast_reliability_score`: via Stage 5 object carrying `data_cutoff_datetime`; no publication date, no report version.
- `historical_pe_values` / `industry_forward_pe_values` / `industry_ttm_pe_values`: **bare floats, no dates, no provenance** (`engine.py:70-72`, sanitized `:86-93`). Zero matches for publication/report_version/provenance/observation_date/published in all of `src/valuation` (fresh grep).
- `probability_confidence`, `data_quality_score`, `probability_evidence`, `scenario_pe_adjustments` (+rationales): undated scalars/records.
- `valuation_date` / `market_price_date` / `data_cutoff_datetime`: real datetimes, but only normalized and echoed (`:104-108`, `:213-215`) — never compared.
- Parameters (`parameters.py`): undated constants; no registry, no effective dates (D9 still unresolved).
- **Result: exactly ONE orderable relationship exists among supplied data** (valuation/market-price dates vs cutoff). Everything else has nothing to order. Stronger than P13's standing finding: `calculate_valuation` has ZERO production callers (fresh grep: 84 matches = definition + tests only) — there is not even a live caller to migrate or validate.

## 2. Implementation Attempts (each pursued to its evidence terminus)

- **Path 1 — order the existing dated fields (valuation/market-price date vs cutoff).** BLOCKED. `test_p6_cutoff_pit_limitation_pinned` (body re-verified P26: 937-953) explicitly pins acceptance of valuation_date 2026-06-01 > cutoff 2026-01-01 with status ATTRACTIVE and no PIT flag — and it passes (inside the 900 green). Any rejection/flag behavior breaks this existing test; weakening or rewriting it is forbidden. The single enforceable check is therefore sealed shut by a passing test.
- **Path 2 — dated benchmark observations + boundary enforcement.** BLOCKED. No observation dates exist on any input and no caller supplies any (see §1). Adding dated-input fields no supplier fills is dead code that demonstrates zero enforcement — P29 demands demonstrated enforcement through the real path, so this was rejected as theater, and recorded as IR1 instead.
- **Path 3 — publication date/version inputs.** BLOCKED. Zero fields, zero values anywhere in the pipeline boundary; populating them would be fabrication (explicitly forbidden). Recorded as IR2.
- **Path 4 — caller attestation field.** REJECTED. P29 itself bars describing attestation as mechanically enforced correctness — implementing it could not satisfy the objective.
- **Path 5 — parameter effective-date selection.** BLOCKED. No registry exists (D9/R8 pending). Recorded as IR3.
- **Path 6 — clarify `metadata["pit_inputs_required"] = True` (`:248`).** REJECTED as no-op churn. The key is informational and unread by any consumer; renaming it changes a public output's meaning without approved replacement semantics and enforces nothing. Noted risk: a reader could mistake it for a safety claim — the P19 §85 annotation already records it as non-enforcement, which stands.
- **Result: ZERO file changes** (`git status`: no source/test/schema/spec/config modification). All 900 previously-green workflows preserved untouched.

## 3. Tests Added: NONE — Planned Adversarial Set Specified Instead

Nothing implemented ⇒ nothing new to test (P29-3's adversarial cases presuppose the missing contract). Gated test plan for IR1/IR2 implementation: future-dated observations rejected/downgraded per rule; stale/out-of-order/conflicting-version series; missing dates/provenance (explicit deterministic outcome, never silent validity); boundary-equal timestamps; valid historical as-of selection (only pre-cutoff datausable); determinism across repeated runs; valid-historical positive cases. Existing pin (`test_p6_cutoff_pit_limitation_pinned`) stays green and untouched unless the owner authorizes the IR4 rule change.

## 4. Fresh Execution Evidence (all runs this task, project interpreter, repo root)

- `python -m pytest src/tests/test_stage7_valuation.py src/tests/test_stage9_decision.py -q` → **2 failed, 63 passed, 52 warnings in 0.92s, exit 1** (failures: only the two known P2s; Stage 9 13/13 green).
- `python -m pytest src/tests/ -q -rs --ignore=src/tests/test_codal_pdf_extraction.py -p no:warnings` → **2 failed, 900 passed, 1 skipped in 109.96s, exit 1.** Skip: Codal fixture (`test_codal_extraction.py:307`), carried, never counted as pass.
- Failures caused by this work: **none** — zero changes; only pre-existing P2 failures (P28 roots stand).

## 5. Precise Integration Requirements (no vague limitations — fields, rules, approvals named)

- **IR1 — dated benchmark observations.** Upstream (Stage 1 market/financial pipelines) must supply per-observation timestamps for all three PE series; `calculate_valuation` gains dated-record inputs; engine enforces observation ≤ approved bound (cutoff/valuation per R7 rule); violation → reject/downgrade/flag per approved response. Zero live callers today → greenfield wiring, but frozen-upstream changes need owner approval. Gated on R7 mechanism + rule.
- **IR2 — publication/version feed.** New boundary fields for report publication date + version; upstream version plumbing (Stage 1 CODAL versions exist but are unconnected to valuation inputs); same rule machinery as IR1. Gated on R7.
- **IR3 — parameter effective dates.** D9 registry with `effective_from` + approved `as_of` rule. Gated on R8.
- **IR4 — valuation-vs-cutoff ordering.** Currently PINNED-accepting by a passing test; enforcement needs an owner-approved rule change PLUS authorized test update (test edits currently forbidden). Names the exact test (:937-953) and the exact conflict.
- On R7/R8 approval, implementation needs no new discovery: fields → validation → §3 tests → suites. Each IR states its validation and compatibility tests at build time.

## 6. Six-Layer Validation (each separately)

1. **Unit/formula:** no formula added/changed/removed (empty diff); enforcement absence re-derived from input shapes (bare floats) rather than asserted.
2. **Contract/boundary:** zero signature/schema/output changes; missing provenance correctly yields no-validity-claim (nothing misrepresented as valid; §85 annotation stands).
3. **Production-path/integration:** all input paths inventoried (§1); zero production callers confirmed; Stage 9 path green; frozen stages untouched.
4. **Adversarial/negative:** Path 1 conflict (pinned acceptance) is itself the adversarial finding; planned hostile cases specified (§3) gated on IRs; no hostile input currently producible at the boundary that the engine mishandles beyond the recorded limitation.
5. **Regression/full suite:** exact commands, exits, counts, durations, skip reason above — all fresh, nothing carried. No failure introduced; P2 pins intact.
6. **Independent final-diff audit:** diff scope verified = this section only (0 deletions; no other file touched). No PIT-completeness claim made — explicitly: PIT IS NOT ENFORCED. No freeze declared.

## 7. Final Verdict

**PIT NOT ENFORCED — NOTHING IMPLEMENTED (BLOCKED: IR1–IR4 + R7/R8).** Every implementable step terminates at missing source fields (IR1–IR3), missing owner rules (R7/R8), or a passing test that forbids the change (IR4). This is not a deferred investigation: the evidence is complete and the four requirements above are concrete. Preserve P28's verdict alongside this one — both failures AND the PIT gap now share one unblock path: owner approval of R1–R8 (P27 §5). Stage 7 remains unfrozen. Stop here.
===================================================================
# P30 — Stage 7 Model and Parameter Versioning

**Date (UTC):** 2026-10-14
**Nature:** Bounded implementation attempt per P30, building on P28/P29 (both reviewed; neither repeated nor discarded). Pre-check: NO R7/R8 (or any R1–R8) owner approval exists (approval grep: zero; `git log` top 5ade89e P29). Current implementation inspected before any edit decision (`parameters.py`, `engine.py:57-79,201-250`, `schema.py:19-50`). Constraints honored: no arbitrary thresholds; no formula changes; no manufactured dates; frozen stages untouched; no remote operations. The only write is this report.

## 1. Outcome-by-Outcome Disposition (P30 §Required outcome 1–7)

- **O1 — record contracts (name/value/effective-from/description/model version).** NOT IMPLEMENTED. A record structure is writable, but every existing parameter's `effective-from` has NO evidence: thresholds' introduction dates are unknowable from code, spec, or history (constants predate versioning). Populating them = inventing dates (forbidden); omitting them fails O1's explicit field list. BLOCKED on R8 (mechanism choice) + effective-date provenance. Precision beyond prior reports: even post-R8, backfilling current constants stays impossible — only forward dating (new/changed parameters stamped at introduction) is honest versioning.
- **O2 — deterministic as-of selection coordinated with PIT.** NOT IMPLEMENTED. There is no temporal contract to coordinate with: P29 verdict stands (PIT NOT ENFORCED, IR1–IR4 blocked). An `as_of` rule selecting among versioned records requires both the records (O1) and D7's ordering invariants — both absent. BLOCKED on R7+R8 jointly (mutual dependency per P22/P27).
- **O3 — missing/ambiguous/conflicting/future-effective/invalid record handling.** NOT IMPLEMENTED. Handling rules are policy (reject vs downgrade vs flag; conflict precedence) with no approved content; a registry to apply them to does not exist. BLOCKED on R8 (+ R7 for date-dependent cases). No silent fallback exists today either — constants are total functions, so nothing currently changes financial meaning silently; stated to prevent misreading this gap as live misbehavior.
- **O4 — reproducibility (same PIT inputs + versions ⇒ same output).** ALREADY HOLDS. `test_p6_repeat_runs_identical_on_full_contract` (`test_stage7_valuation.py:1035`) pins determinism and passes (inside the 900 green below). No code needed; verified, not assumed.
- **O5 — outputs/metadata identify versions used.** ALREADY HOLDS. Every `ValuationResult` carries `model_version="STAGE7_V1"` (`engine.py:211`, from `parameters.py:80`) and `contract_version="VALUATION_CONTRACT_V1"` (`:231`, from `:81`); `calculation_timestamp` (`:212`) and `data_cutoff_datetime` (`:215`) accompany them. No code needed; verified, not assumed.
- **O6 — consumer trace of contract changes.** VACUOUS: no contract changed (empty diff), so no consumer migration exists to trace. Stage 9 suite green (13/13 in focused run) confirms consumers unaffected.
- **O7 — no new thresholds/formula changes.** HOLDS trivially: zero modifications of any kind.

## 2. Fix-Attempt Log (paths examined, not skipped)

- **Path A — in-code registry of current values with invented `effective_from`.** REJECTED: date fabrication, explicitly forbidden; P14's design remains an unapproved proposal.
- **Path B — registry with blank/None effective dates.** REJECTED: fails O1's field requirement; as-of selection over undated records is undefined — theater, not versioning (same reasoning as P29-Path 2).
- **Path C — DB-backed table now.** REJECTED: heavier variant of A with identical blockers (mechanism unapproved + dates unknowable + no as_of rule), plus migration/dependency cost with zero enforcing payoff.
- **Path D — rebrand current constants as "versioned" (MODEL_VERSION label only).** REJECTED: a static label is not a registry; calling it versioning would misrepresent (P26's laundering warning applies). Current labels stay exactly what they are: build identifiers, honestly reported as such in O5.
- **Result: ZERO file changes** (`git status`: only the user's own `stage_7_prompts.md` staging, pre-existing).

## 3. Fresh Execution Evidence (all runs this task)

- `python -m pytest src/tests/test_stage7_valuation.py src/tests/test_stage9_decision.py -q -p no:warnings` → **2 failed, 63 passed in 1.01s, exit 1** (only the two known P2s; determinism + Stage 9 green inside).
- `python -m pytest src/tests/ -q -rs --ignore=src/tests/test_codal_pdf_extraction.py -p no:warnings` → **2 failed, 900 passed, 1 skipped in 115.44s, exit 1.** Skip: Codal fixture (`:307`), carried, never a pass.
- Failures introduced by this work: **none** (no changes). Pre-existing P2 pins stand with P28 roots.

## 4. Six-Layer Validation (each separately)

1. **Unit/formula:** no formula touched (O7 holds by empty diff); O4/O5 verified against cited lines, not inferred.
2. **Contract/boundary:** zero signature/schema/output changes; O1–O3 absences restated as missing capability, never as silent behavior.
3. **Production-path/integration:** version stamping traced on the live construction path (`:201-250`); consumers green; frozen stages untouched.
4. **Adversarial/negative:** O3's hostile cases (conflicting/future-effective/invalid records) have no registry to attack — specified as gated requirements for the R8 implementation, not simulated against constants.
5. **Regression/full suite:** exact commands, exits, counts, durations, skip reason above — all fresh. P2 failures preserved as designed pins.
6. **Independent final-diff audit:** diff scope verified = this section only (0 deletions; no other file touched). No versioning-completeness claim made.

## 5. Precise Unblock Path (fields, rules, approvals — no vagueness)

- **R8 now:** mechanism (in-code per P14 vs DB per §65) + forward-dating discipline (new/changed parameters stamped at introduction; historical constants explicitly marked undatable-backfill rather than backfilled with invented dates).
- **R7+R8 jointly:** `as_of` rule + ordering invariants (P29-IR1/IR2), then O2/O3 implementable with gated tests (effective-date boundaries, historical selection, missing/conflicting records, determinism, backward-compat per existing contract).
- O4/O5 already hold and need no action. Nothing here needs new discovery — only approvals.

## 6. Final Verdict

**VERSIONING NOT IMPLEMENTED — BLOCKED (R8 mechanism + effective-date provenance + R7 as_of coordination); O4/O5 ALREADY HOLD.** Two of seven outcomes verifiably satisfied without action; the other five terminate at missing approvals/dates, each named above. Not claimed: versioned parameters, as-of selection, completeness, freeze. P28/P29 verdicts stand alongside this one — all three share the single unblock path of P27-R1–R8 owner approval. Stage 7 remains unfrozen. Stop here.
===================================================================
# P31 — Stage 7 Root-Cause Remediation and Production-Path Integration

**Date (UTC):** 2026-10-14
**Nature:** Real-work attempt per P31, not report-only by choice: baseline → independent production-path verification (5 levels) → defect hunt for bug-class issues → fix attempt per failure → gated test plan. P28–P30 reviewed first (built on, not repeated, not discarded). Pre-check: no R1–R8 owner approval exists (approval grep zero; log top c941cfd P30). Constraints honored: frozen Stages 1–6/8–9 NOT modified; no invented formulas/thresholds/magnitudes/dates/mappings/provenance/defaults/rounding; no EPS rebuild; no buy/sell implication; missing never treated as zero; no production integration claimed without a demonstrating test. The only write is this report.

## 1. Fresh Baseline (all runs this task, `.venv/Scripts/python.exe`, repo root, `-p no:warnings` unless stated)

- Named pair (`test_p2_sector_driver_decomposition_missing`, `test_p2_required_flip_dependence_alerts_missing`) → **2 failed in 1.34s, exit 1.** Exact messages: `:422` subset assertion (`{'NAV','NII','REVENUE'} <= {'EPS','TARGET_PE'}`); `:465` missing-names assertion (all 5 names absent).
- `test_stage7_valuation.py` → **2 failed, 50 passed in 0.81s, exit 1.**
- Stage 7 + Stage 9 → **2 failed, 63 passed in 1.28s, exit 1** (Stage 9 13/13; warnings shown once, same known `utcnow` set).
- Broad (`src/tests/ -q -rs --ignore=test_codal_pdf_extraction.py`) → **2 failed, 900 passed, 1 skipped in 115.42s, exit 1.** Skip: Codal fixture `:307`, never a pass.

## 2. Production-Path Trace (independent 5-level verification — P29's finding re-proven, extended)

- **L1 — callers of `calculate_valuation`:** 84 matches = the definition (`engine.py:57`) + tests only. Zero production callers.
- **L2 — `ValuationEngine` references:** 63 matches = definition + package re-export (`__init__.py:11`) + tests only. Zero production instantiations.
- **L3 — `ValuationResult(` constructions:** exactly 2 = inside the engine itself (`:201`) + Stage 9 TEST helper (`test_stage9_decision.py:24`). No production code ever builds one.
- **L4 — `src/scripts/`:** DB utilities only (`init_db/migrate_db/seed_data`); sole valuation-adjacent hit is an unrelated `MappingDecision` import. No pipeline wiring.
- **L5 — decision engine:** type-only import of `ValuationResult`; consumes an INJECTED result (status/reliability/risk/confidence/metadata — P26/P27 field list); Stage 9 tests inject hand-built results. Integration of Stage 7→9 exists ONLY in tests.
- **Conclusion:** Stage 7 is implemented-but-unwired — a tested library with no production caller and no production-constructed inputs. Per the prompt's own rule, production integration is NOT claimed (no test can demonstrate a call path that does not exist). Wiring one necessarily touches frozen stages or adds an orchestrator — outside this task's authorization (P31-5); documented in §5 instead of built.

## 3. Root Causes Classified (code defect vs contract gap vs unapproved policy vs missing dependency)

- **T1 (sector drivers):** missing upstream dependency (chain source fields; industry mapping) + unapproved policy (D6). NOT a code defect — `_driver_analysis` (`:469-498`) implements exactly the approved two-driver contract. NOT a contract inconsistency — the contract is coherent, only narrower than spec §§42-44.
- **T2 (five alerts):** unapproved policy ×5 (D1 flip rule; D2/D3 metric+threshold+precedence with proven 50/50 degeneracy; D4 margin series; D5 combination+thresholds). NOT a code defect, NOT a contract inconsistency.
- **Integration gap:** missing upstream dependency (caller) + missing architecture decision (caller placement/sourcing/scheduling). Frozen-stage modification NOT authorized.

## 4. Corrections Implemented: NONE — Defect Hunt Closed With Evidence

- Full-engine re-scan for bug-class issues: every suspicious line is either pinned by passing tests (`test_p10_*_outputs_unchanged`, `test_p6_regression_prior_behavior_preserved`, golden cases — e.g. the `<` vs `<=` threshold asymmetry) or documented deliberate compatibility (`INDUSTRY_TARGET_PE={}`, neutral `SCENARIO_PE_MULTIPLIER`, `flags.extend(alerts)` channel merge). Altering any of them breaks pinned behavior without an approved basis — indistinguishable from test weakening.
- Policy items: blocked exactly as in P28 (R-gated); re-verified, not re-argued.
- Caller wiring: outside authorization (see §2 + §5).
- Tests added/changed: none — approved behavior fully pinned (50 green); any new behavioral test would assert unapproved policy or duplicate pins.
- On P31-8 ("a report without implementation is not acceptable WHEN a valid correction exists"): the condition is not met — zero valid corrections exist in scope. This report documents the completed hunt instead of manufacturing one.

## 5. Cross-Stage Dependency Document (authorized documentation, not a change)

- **Dependency:** no production caller; evidence §2 (5-level proof).
- **What integration requires:** a caller that (a) sources a real `CompanyForecastResult` from Stage 5/6 outputs (never fabricated), (b) supplies benchmark series + reliability from upstream, (c) feeds the resulting `ValuationResult` to Stage 9.
- **Required tests:** an integration test driving caller→valuation→decision on REAL Stage 5/6 outputs (fabricated forecasts prohibited); no such test can be written until the caller exists.
- **Owner-gated choices (no speculative diff provided — writing one would invent architecture):** caller placement (new orchestrator vs Stage-9-driven vs other), data-sourcing contracts, scheduling. Gated to the WP-5/6 era under R2/R7 decisions.

## 6. Six-Layer Validation (each separately, post-work)

1. **Unit/formula:** failure assertions re-derived; defect hunt closed; zero logic touched (empty diff).
2. **Contract/boundary:** zero signature/schema/output changes; boundary gaps restated unchanged.
3. **Production-path/integration:** 5-level negative result documented with evidence; Stage 9 tests green; frozen stages untouched.
4. **Adversarial/negative:** failing tests' hostile content executes and fails for proven reasons; passing adversarial suites (NaN/None/zero/ordering/determinism) confirm no adjacent breakage.
5. **Regression:** four exact commands above (exits 1/1/1/1 on the two known tests only); 1 carried skip, never a pass; pre-existing failures PROVEN (identical signatures P15→P31), not weakened.
6. **Independent audit of changed logic:** no logic changed; final diff scope verified = this section only (0 deletions; no other file touched); financial invariants preserved by inaction, not by claim.

## 7. Remaining Blockers, Files, Follow-up, Verdict

- **Blockers:** T1 → R2+WP-5; T2 → R1/R3/R4/R5/R6+WP-1…4; integration → caller-placement decision + R2/R7. All owner-side.
- **Files changed:** none. **Tests added/changed:** none. **Follow-up required:** owner R1–R8 answers (P27 §5); any single R-answer immediately starts its gated WP.
- - **Verdict: NOT FULLY PASSING — 2 pre-existing failures PROVEN, ZERO supportable corrections in scope, NO CODE CHANGED.** Not claimed: production integration, completeness, freeze. Stage 7 remains unfrozen. Stop after implementation attempt + validation + report.
===================================================================
# P32 — Stage 7 Point-in-Time Enforcement

**Date (UTC):** 2026-10-14
**Nature:** Real implementation task — first runtime code change of the Stage 7 arc (P19/P24 touched spec docs only; P28–P31 correctly changed nothing). P31 reviewed (not repeated, not discarded). Pre-check: no R1–R8 owner approval (approval grep zero; log top e926782 P31). Constraints honored: no invented rules/dates/defaults; no weakened tests; frozen stages untouched (imports are not modifications); no fabricated data; no remote operations. Changed files: `src/valuation/engine.py`, `src/tests/test_stage7_valuation.py` (+ this report).

## 1. New Findings Beyond P29 (fresh investigation, not repetition)

- **Authoritative upstream PIT machinery EXISTS (Stage 5 side):** `ForecastInputRef(report_version_id, available_at)` whose docstring states the rule itself — "a forecast whose cutoff precedes `available_at` is a Point-in-Time violation (spec §25)" (`forecast/schema.py:156-162`); `select_usable_inputs` enforces `available_at <= cutoff` (`:247-253`); append-only `ForecastVersionStore` with `valid_at`/`pit_violations` (`:273-370`); production `service.py:407-410` persists frozen records per scenario. The predicate is inherited, not invented.
- **Boundary drop located precisely:** `CompanyForecastResult` (`:34-47`) carries IDs, cutoff, industry, EPS chains, method/version/timestamps — but NO input_refs, NO record identity, NO versions. Stage 7 reads only EPS chains + cutoff (`engine.py:80-84,106-108`). The enforcement data exists upstream and dies at the boundary.
- **Pinned-test question answered (P32's hard push):** spec §7 requires prices be *identified* (valuation_date, market_price_date), §8/§§56-57 state the PIT *principle* (only published-and-available data per date) — but NO sentence anywhere orders `valuation_date` vs `data_cutoff_datetime`. `test_p6_cutoff_pit_limitation_pinned` (late valuation accepted, ATTRACTIVE, no PIT flag) contradicts nothing in the spec: valuation after cutoff is normal current-date operation. P29's "IR4 conflict" framing is hereby corrected — the pinned behavior STANDS as legitimate; there was never evidence it was wrong. The real gap was always the dateless series.
- **Parameter-history leak vector (new, precise):** undated constants mean any future threshold change silently rewrites backtest history — distinct from input dating, gated on R8 forward-dating (P30).

## 2. Input-to-Output PIT Trace (source classified per P32-O2)

| Input class | Timestamp/provenance | Classification | Enforceable? |
|---|---|---|---|
| valuation/market-price date | caller datetimes, normalized, unordered | caller-supplied, unverified order | NO (no ordering rule in spec; pin stands) |
| forecast cutoff | caller or forecast fallback (`:215` chain) | caller-supplied, verified present | As comparison bound only |
| forecast input refs (NEW param) | caller-supplied `ForecastInputRef`s | caller-supplied, verified vs cutoff | YES — implemented below |
| report publication/version (benchmarks) | none anywhere in `src/valuation` (0 refs) | ABSENT | NO → IR1 |
| historical EPS availability (dated) | floats only; revision history lives Stage 5–9, never enters S7 | ABSENT at boundary | NO → route decision (D3) |
| benchmark observations (dated) | bare floats (`:70-72`) | ABSENT | NO → IR1 |
| parameter validity dates | constants; 0 refs effective_from | ABSENT | NO → IR3/R8 |

## 3. Implementation (additive, backward-compatible, evidence-backed)

- `engine.py:5` — import `ForecastInputRef` (same module already imported; zero new coupling class).
- Signature — new keyword-only `forecast_input_refs: Optional[Sequence[ForecastInputRef]] = None` (after `scenario_pe_rationales`; positional callers unaffected).
- Call site — `_reject_unverifiable_forecast_refs(...)` immediately after cutoff normalization (`:104-108`), i.e. ON the valuation path with the effective cutoff.
- New `_reject_unverifiable_forecast_refs`: `None`/empty → legacy path byte-identical; each supplied ref normalized; `available_at is None` → `ValueError` (undated provenance never silently valid — P32's explicit-outcome requirement); `available_at > cutoff` → `ValueError` (mirrors upstream `<=` predicate); `None` cutoff → dated refs accepted (no bound exists; none invented). No numeric thresholds, no dates, no defaults invented. Violation response = rejection: the only non-silent deterministic option available without approved alternatives (no new output vocabulary created, so D8 untouched); owner may revise to downgrade/flag under R7 — disclosed as judgment call, one-line change.
- Frozen stages: untouched (import-only). P2 tests: untouched, still failing as designed (D1–D6 still R-gated; this change does not address them).

## 4. Tests Added (5, all through `calculate_valuation`, the real path)

- `test_p32_input_refs_before_cutoff_leave_results_unchanged` — pre-cutoff refs (naive + aware mix) ⇒ full-result equality with no-refs call (minus wall-clock timestamp). Proves additive compatibility.
- `test_p32_input_ref_after_cutoff_rejected_on_valuation_path` — post-cutoff ref ⇒ `ValueError`. Proves future-known input blocked on-path.
- `test_p32_input_ref_at_cutoff_boundary_accepted` — equality ⇒ accepted (mirrors `<=`), FV 1260.0/ATTRACTIVE.
- `test_p32_input_ref_missing_date_rejected` — `available_at=None` ⇒ `ValueError`. Proves missing ≠ valid.
- `test_p32_input_refs_absent_preserves_legacy_path` — default `None` ⇒ unchanged ATTRACTIVE/1260.0 pin.
- Development note (honest): first run went 4/5 on a missing `dataclasses` import in my own test file (test bug, not product bug); fixed; 5/5 since. No product failure was introduced at any point.

## 5. Fresh Execution Evidence (all runs this task)

- `-k p32` → **5 passed in 0.75s, exit 0** (after the import fix above).
- Stage 7 + Stage 9 → **2 failed, 68 passed in 0.78s, exit 1** (63 pre-existing passes + 5 new; failures: only the two known P2s, signatures unchanged).
- Broad (`--ignore=test_codal_pdf_extraction.py`) → **2 failed, 905 passed, 1 skipped in 114.85s, exit 1** (900 + 5 new; skip: Codal fixture, never a pass).
- Pre-existing vs new distinguished: 2 P2 failures pre-date this task identically; 0 new failures; 5 new passes all mine.

## 6. Six-Layer Validation (each separately)

1. **Unit/formula:** no formula touched (FV/status/confidence paths byte-identical for refs=None — proven by full-dict equality test); new predicate mirrors upstream `<=` exactly, including naive→UTC normalization.
2. **Contract/boundary:** one optional keyword-only parameter (backward compatible — all 52 pre-existing Stage 7 tests omit it and pass unmodified); missing/None/future inputs produce explicit `ValueError`, never silent validity and never zero-fill; `None` cutoff documented acceptance.
3. **Production integration:** control executes inside `calculate_valuation` on the effective cutoff (proven by path-level tests, not helper-only). Plainly stated limit: NO production caller passes refs yet (P31: zero callers) — the control is live code, dormant in production until wired; NOT claimed as production enforcement.
4. **Adversarial/negative:** future-dated, undated, boundary-equal, naive/aware-mixed, and absent-ref cases all covered; no hostile input reaches FV/probability/confidence/risk silently (rejected pre-computation).
5. **Regression/full suite:** exact commands/exits/counts/durations above; only delta vs P31 baseline is +5 passes; P2 pins intact with identical traces.
6. **Independent final-diff audit:** diff = `engine.py` (+import, +1 param, +1 call, +1 method ≈ 40 lines), tests (+import, +2 helpers, +5 tests ≈ 75 lines), this section. No frozen file touched (`git status` scope verified); no threshold/formula/date invented; no test weakened (P2s byte-identical in behavior); no freeze declared.

## 7. Remaining Upstream Dependencies + Unresolved Owner Decisions (precise)

- **IR1 (benchmark observation dating) целиком outstanding:** bare-float series still carry no dates; §8 states the principle but supplies no per-observation data. Needs upstream dating + R7 rule (unchanged from P29, now cleanly separated from the forecast leg this task closed).
- **D3 revision route:** ternary→family mapping rule still missing (C3 stands).
- **R7 remainder:** violation-response revision (reject→downgrade/flag), ordering invariants, IR1/IR2 rules.
- **R8 remainder:** registry + as_of (IR3); parameter-history leak persists until forward-dating starts.
- **Production wiring:** control dormant until a caller passes refs — needs the caller-placement decision (P31 §5) + R2/R7.

## 8. Final Verdict

**PARTIAL PIT ENFORCEMENT IMPLEMENTED (forecast-input leg only); PIT NOT COMPLETE.** Completed per P32 criteria for the closed leg: authoritative source (`ForecastInputRef` + upstream `<=` predicate), exact rule, validation location (in-path, post-cutoff-normalization), invalid/missing behavior (explicit `ValueError`), leak-proof tests on the real path (5 green), zero unapproved assumptions. Explicitly NOT claimed: benchmark-series enforcement, parameter versioning, production enforcement, completeness, freeze. Stage 7 remains unfrozen. Stop here.

===================================================================
# P33 — Stage 7 Model and Parameter Versioning

**Date (UTC):** 2026-10-14
**Nature:** Implementation task — second runtime change of the Stage 7 arc (P32 was the first). P31/P32 reviewed (built on, not repeated). Pre-check: no R1–R8 owner approval (approval grep zero). Constraints honored: no invented historical dates; no newest-valid-for-history assumption; no DB registry (no architectural evidence); no silent fallback; no financial-calculation changes; no full-PIT claim; frozen stages untouched (import-only); no remote operations. Changed files: `src/valuation/parameters.py`, `src/valuation/engine.py`, `src/tests/test_stage7_valuation.py` (+ this report).

## 1. Parameter Inventory (38 records; origins verified, values live-referenced)

| Group | Leaves | Origin today |
|---|---|---|
| SCENARIO_WEIGHTS (bear/base/bull) | 3 | in-code constants |
| SCENARIO_PE_MULTIPLIER (×3, neutral 1.00) | 3 | in-code constants |
| PROBABILITY_EVIDENCE_FAMILIES + BLEND | 2 | in-code constants |
| SCENARIO_MULTIPLE_MAX_ABS_ADJUSTMENT + POLICY_VERSION | 2 | in-code constants |
| VALUATION_THRESHOLDS | 8 | in-code constants, spec-unratified (D9) |
| CONFIDENCE_THRESHOLDS | 4 | in-code constants, spec-unratified (D9) |
| RISK_THRESHOLDS | 5 | in-code constants, spec-unratified (D9) |
| ALERT_THRESHOLDS (incl. dead 0.60) | 6 | in-code constants (0.60 unwired, stays inert) |
| SENSITIVITY_PERTURBATION / MIN_INDUSTRY_PEERS | 2 | in-code constants |
| MODEL_VERSION / CONTRACT_VERSION / INDUSTRY_TARGET_PE | 3 | identifiers / retained-empty compat export |

Genuine `model_version`/`parameter_name`/`parameter_value`/`effective_from`/description support: NONE existed — `effective_from`/`parameter_version` had 0 references repo-wide (re-verified). The structure below was built; the dates were not invented.

## 2. Implementation (mechanism only; values mirrored, never set)

- `parameters.py` — `ParameterRecord` (name/value/effective_from/description; §65-shaped), `ParameterSetVersion` (+ version-level `effective_from`), `ParameterRegistry`, `GENESIS_VERSION_KEY = "STAGE7_V1/GENESIS"`, `GENESIS_VERSION` (38 records built PROGRAMMATICALLY from live constants — values never retyped, drift impossible; every `effective_from=None` with the reason recorded on each record: temporal validity unknown, never valid for historical selection), `resolve_parameter_set` (exact key, missing → `KeyError`, never silent current), `resolve_parameter_set_as_of` (dated-only participation; newest covering version wins; future-effective never selected; overlap → ambiguity `LookupError`; `as_of=None` → `LookupError`; genesis-only registry → explicit R8-naming `LookupError`, never quiet fallback).
- `engine.py` — import extended (same already-imported modules); `resolve_parameter_set(GENESIS_VERSION_KEY)` on the valuation path (registry corruption would fail loudly, not silently); two metadata keys stamped: `parameter_set_version` + full 38-entry `parameter_snapshot`. No formula, threshold, or calculation touched.
- Deliberately NOT built: `effective_from` dates for existing constants (unknowable — P33 forbids invention); DB registry (no architectural evidence); any financial change.

## 3. Golden-Digest Regression: Found, Proven, Re-baselined (Not Weakened)

- The metadata addition tripped `test_p10_expensive_base_upside_parameterized_outputs_unchanged` (SHA-256 over full result dict).
- Proof it is additive-only: recomputed digest with exactly the 2 new metadata keys removed reproduces the pinned digest byte-for-byte (`1990c639…1cf819b71255`); all substantive asserts (FVs 1050/1260/1470, MOS 26.0, ATTRACTIVE, versions) pass unchanged.
- Action: digest updated to `7b5fb909…52df33f33` with a comment recording the proof. This is a justified golden re-baseline after an intentional additive change — the test's protections (0.0-valued key consumed, comparison exact) are intact, not loosened.

## 4. Tests Added (6, all on real paths — 11/11 new P32+P33 green)

- `test_p33_genesis_snapshot_matches_live_constants` — snapshot == live constants (incl. 15.0/0.10/8/`STAGE7_V1`), 38 records, all undated.
- `test_p33_result_carries_parameter_audit` — result metadata carries version key + exact snapshot; full-dict determinism across runs.
- `test_p33_resolve_exact_key_and_missing_raises` — exact match ok; unknown key → `KeyError` (no silent current).
- `test_p33_as_of_without_dated_records_raises` — dated query + `None` as-of → explicit `LookupError` (R8 named).
- `test_p33_as_of_selection_mechanics` (synthetic clearly-labeled TEST versions only) — boundary equality selects (`<=` mirror); future-effective excluded (no leakage); pre-history → explicit error.
- `test_p33_as_of_overlap_raises_ambiguity` — identical effective dates → `LookupError`, never silent pick.

## 5. Fresh Execution Evidence (all runs this task)

- `-k "p32 or p33"` → **11 passed in 0.88s, exit 0.**
- Stage 7 + Stage 9 → **2 failed, 74 passed in 1.16s, exit 1** (failures: only known P2s; p10 re-greened).
- Broad (`--ignore=test_codal_pdf_extraction.py`) → **2 failed, 911 passed, 1 skipped in 104.70s, exit 1** (900 + 11 new; skip: Codal fixture, never a pass).
- New vs pre-existing: 11 new passes mine; 2 P2 failures pre-date identically; 1 transient dev-time failure (my own missing import, test-side) fixed same session and disclosed.

## 6. Six-Layer Validation (each separately)

1. **Unit/formula:** zero formula/threshold/value changes (digest proof §3); registry mechanics unit-covered (exact/missing/boundary/future/overlap/None).
2. **Contract/boundary:** additive-only outputs (2 metadata keys); one keyword-only pattern preserved (no signature); missing/ambiguous/future/invalid versions → explicit errors, never silent current; backward compat proven (all 52 pre-existing Stage 7 tests omit new inputs and pass).
3. **Production-path/integration:** resolution + stamping execute inside `calculate_valuation` (proven by result-carrying + equality tests); Stage 9 green; frozen stages untouched.
4. **Adversarial/negative:** unknown key, undated registry query, `None` as-of, future-effective, overlap, pre-history — all explicit errors; no hostile version input yields silent current values.
5. **Regression/full suite:** exact commands/exits/counts/durations above; p10 regression caught, proven additive-only, re-baselined with recorded proof; P2 pins intact.
6. **Independent final-diff audit:** diff = parameters registry block, engine stamp (import/resolve/2 keys), tests (+imports/helpers/6 tests/p10 digest+comment), this section. No invented dates/values/formulas; no weakened test (p10 substantive asserts intact); no freeze declared.

## 7. Remaining Owner Decisions (concrete consequences)

- **R8 now:** adopt this in-code registry or order DB-backed instead; supply `effective_from` discipline going forward (new/changed parameters stamped at introduction — backfill of current constants stays impossible, recorded, never to be invented later).
- **R7+R8 jointly:** `as_of` rule + ordering invariants activate `resolve_parameter_set_as_of` for real registries (mechanics already tested).
- **Production wiring for P32 refs:** still absent (control dormant) — caller-placement decision (P31 §5).
- **P2 failures:** still R1–R6-gated, untouched.

## 8. Final Verdict

**VERSIONING MECHANISM IMPLEMENTED (genesis + exact resolution + explicit as_of refusal + result audit); HISTORICAL SELECTION BLOCKED (R8/R7).** Satisfied: inventory, record contracts, deterministic resolution/selection mechanics, reproducibility + historical-selection + leakage + missing-version + audit-metadata tests, backward compatibility, zero invented dates/values. Not claimed: dated history, DB registry, full PIT, completeness, freeze. Stage 7 remains unfrozen. Stop here.
