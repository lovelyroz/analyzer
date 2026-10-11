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

---

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
