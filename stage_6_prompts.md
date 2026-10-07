Stage 6 Prompt 1

You are performing **Stage 6 Prompt 17** for the repository:

`analyzer`

Stage 1–4 are frozen.

Stage 5 has now passed an independent adversarial validation and is frozen.

Your task is to perform a **READ-ONLY Stage 6 preflight** before any implementation.

## HARD FIREWALL

Work locally only.

Do NOT:

* access GitHub,
* use GitHub CLI/API,
* fetch/pull/push,
* modify remotes,
* create commits,
* create/delete/switch branches,
* modify Stage 1–5.

Do not perform broad repository exploration.

## READ THESE FIRST

Read:

* `PROJECT_HANDOFF_INSTRUCTIONS.md`
* `06_Stage6_Forecast_Evaluation.md`
* the Stage 5 Prompt 16 report in `temp_report.md`

Then inspect only the files directly relevant to determining the current Stage 6 implementation state.

Do not assume Stage 6 implementation exists merely because the specification exists.

## OBJECTIVE

Determine the actual current state of Stage 6.

Identify:

1. existing Stage 6 modules/classes/functions, if any;
2. existing database models/migrations related to forecast evaluation;
3. existing forecast/actual data structures that Stage 6 can legitimately consume;
4. existing PIT/query infrastructure reusable by Stage 6;
5. existing tests;
6. which specification requirements are already implemented;
7. which requirements are completely missing;
8. architectural conflicts or ambiguities;
9. dependencies on Stage 5 that can be consumed without modifying Stage 5.

Pay particular attention to:

* Forecast → Actual mapping,
* PIT evaluation,
* horizons,
* Model Version separation,
* MAPE,
* Bias,
* Seasonal Naive baseline,
* observation sufficiency,
* Reliability,
* Calibration,
* versioning,
* auditability.

Do NOT implement anything.

Do NOT create files.

Do NOT modify tests.

## REPORT

Append:

`REPORT — Stage 6 Prompt 17`

to `temp_report.md`.

Clearly separate:

* EXISTING
* MISSING
* PARTIAL
* BLOCKER
* REUSABLE INFRASTRUCTURE
* ARCHITECTURAL QUESTIONS

Do not propose speculative architecture merely for cleanliness.

End with:

`Stage 6 is NOT declared frozen.`

STOP after the preflight report.
====================================
Stage 6 Prompt 2

You are performing **Stage 6 Prompt 18** for:

`analyzer`

Use the completed Stage 6 Prompt 17 report in `temp_report.md` as the discovery result.

Stage 1–4 and Stage 5 are frozen.

## FIREWALL

Work locally only.

No GitHub, GitHub CLI/API, push, pull, remote changes, branches, commits, or Git history.

Do not modify Stage 1–5.

Inspect only files identified by P17 as necessary, plus directly referenced symbols.

## OBJECTIVE

Implement only the **Stage 6 evaluation data foundation**.

Based on the Stage 6 specification and P17 findings, establish the minimum auditable structures required to represent:

* forecast identity,
* company,
* metric,
* financial period,
* horizon,
* model version,
* forecast cutoff,
* forecast value,
* corresponding actual,
* actual report/version identity,
* publication timestamp,
* evaluation status,
* evaluation timestamp.

Preserve the distinction between:

* forecast cutoff,
* forecast timestamp,
* financial period,
* actual publication date.

Implement PIT-safe Forecast → Actual mapping.

An Actual must not simply be "the latest value in the database".

Do not use information unavailable at the relevant forecast cutoff when determining evaluation eligibility.

Preserve:

`NULL != 0`.

Do not implement:

* MAPE,
* Bias,
* Reliability,
* Calibration,
* Valuation,
* new forecasting logic.

Do not modify Stage 5.

Add focused behavioral tests for the data contract and PIT mapping.

Run only the relevant Stage 6 tests plus the existing Stage 5 focused suite if needed to verify no boundary regression.

## REPORT

Append:

`REPORT — Stage 6 Prompt 18`

Include files changed, PIT behavior, data contract, tests, and remaining Stage 6 gaps.

Do not claim Stage 6 complete.

End:

`Stage 6 is NOT declared frozen.`

STOP.
===============================
Stage 6 Prompt 3

You are performing **Stage 6 Prompt 19** for:

`analyzer`

Use the Stage 6 specification and the Prompt 17/18 reports in `temp_report.md`.

Stage 1–5 are frozen.

## FIREWALL

Local working tree only.

No GitHub, Git operations, commits, remotes, branches, or broad repository exploration.

Do not modify Stage 1–5.

Inspect only Stage 6 files and directly referenced symbols.

## OBJECTIVE

Implement the Stage 6 **evaluation metrics layer** only.

Implement and behaviorally test:

### Forecast Error

`Error = Actual - Forecast`

### Percentage Error

`(Actual - Forecast) / abs(Forecast)`

### APE

`abs(Actual - Forecast) / abs(Forecast)`

### MAPE

Mean valid APE observations.

### Bias

Mean signed percentage error.

Respect the specification for:

* zero forecast,
* zero base,
* LOSS_TO_PROFIT,
* PROFIT_TO_LOSS,
* SIGN_CHANGE.

Do NOT produce misleading percentage metrics for those regimes.

Absolute error may remain available.

### Horizons

Keep:

* 1M
* 3M
* 6M
* 12M

independent.

Never mix horizons.

### Model Versions

Never mix Model Version observations.

### Minimum observations

Implement the specified:

* `<5` → INSUFFICIENT_DATA
* `5–7` → LOW_CONFIDENCE
* `8–11` → MODERATE_CONFIDENCE
* `>=12` → ADEQUATE

### Seasonal Naive Baseline

Implement the Stage 6 V1 baseline only if the required PIT-safe historical data is available.

Baseline must not use future information.

Implement:

* baseline value,
* baseline error,
* baseline MAPE,
* relative model improvement.

Do NOT implement Reliability or Calibration yet.

Do NOT modify Stage 5.

Add behavioral tests designed to catch:

* sign errors,
* zero denominators,
* horizon mixing,
* model-version mixing,
* duplicate observations,
* PIT leakage,
* invalid Actuals,
* invalid baseline inputs.

Run focused Stage 6 tests.

## REPORT

Append:

`REPORT — Stage 6 Prompt 19`

Include exact formulas implemented, PIT behavior, horizon/version isolation, baseline behavior, tests, and unresolved issues.

End:

`Stage 6 is NOT declared frozen.`

STOP.
================================

Stage 6 Prompt 4

You are performing **Stage 6 Prompt 20** for:

`analyzer`

Read the Stage 6 specification and Prompt 17–19 reports from `temp_report.md`.

Stage 1–5 are frozen.

## FIREWALL

Local only.

No GitHub, Git operations, commits, branches, remotes, or broad exploration.

Do not modify Stage 1–5.

## OBJECTIVE

Implement only:

1. Forecast Reliability
2. Calibration state
3. Calibration versioning

Do not change the underlying Stage 5 forecast engine.

## RELIABILITY

Reliability must remain distinct from Accuracy and Bias.

Use the Stage 6 V1 architecture:

`Accuracy + Bias Control + Baseline Advantage`
→ `Performance Score`
→ `Confidence Adjustment`
→ `Reliability 0–100`

Weights:

* Accuracy: 50%
* Bias Control: 20%
* Baseline Advantage: 30%

MAPE-to-score and other mapping thresholds must be versioned parameters, not permanent architectural truths.

Observation sufficiency must affect confidence.

Do not allow:

`Performance Score = Reliability`

without the required confidence adjustment.

## CALIBRATION

Implement:

* NO_CALIBRATION
* CALIBRATION_CANDIDATE
* CALIBRATED

Calibration requires evidence of persistent bias.

Do NOT calibrate from one observation.

Calibration must:

* create a new Model Version,
* never overwrite the previous version,
* preserve the original evaluation,
* remain auditable.

Do NOT directly do:

`Forecast × (1 + Bias)`

inside the existing model version.

Calibration must produce a versioned future model configuration.

## OUT-OF-SAMPLE

Represent the distinction between:

* calibration/training period,
* holdout/out-of-sample evaluation period.

Do not use holdout outcomes to create the calibration itself.

## TESTS

Add behavioral tests for:

* Reliability vs Accuracy distinction,
* observation confidence,
* persistent vs isolated bias,
* no-calibration case,
* calibration-candidate case,
* calibrated case,
* new model version,
* old version preserved,
* out-of-sample evaluation,
* no PIT leakage.

Do NOT connect Reliability to P/E.

Do NOT implement Stage 7.

## REPORT

Append:

`REPORT — Stage 6 Prompt 20`

Include architecture, formulas/parameters, versioning behavior, calibration behavior, tests, and remaining gaps.

End:

`Stage 6 is NOT declared frozen.`

STOP.
=================================

Stage 6 Prompt 5

You are performing **Stage 6 Prompt 21** for:

`analyzer`

Use the Stage 6 specification and Prompt 17–20 reports from `temp_report.md`.

Stage 1–5 are frozen.

## FIREWALL

Local only.

No GitHub, Git operations, commits, remotes, branches, or broad exploration.

Do not modify Stage 1–5.

## OBJECTIVE

Connect the implemented Stage 6 components into one auditable evaluation path:

`Forecast Version`
→ `PIT-safe Actual`
→ `Forecast Error`
→ `Accuracy / Bias`
→ `Seasonal Naive Baseline`
→ `Baseline Comparison`
→ `Observation Sufficiency`
→ `Performance Score`
→ `Reliability`
→ `Calibration State`

Do NOT generate forecasts.

Do NOT alter Stage 5.

Do NOT implement Stage 7.

## TEST MATRIX

Ensure behavioral coverage for:

* normal forecast/actual,
* under-forecast,
* over-forecast,
* zero forecast,
* LOSS_TO_PROFIT,
* PROFIT_TO_LOSS,
* sign change,
* each horizon,
* separate model versions,
* insufficient observations,
* low/moderate/adequate confidence,
* baseline better than model,
* model better than baseline,
* persistent bias,
* isolated bias,
* PIT cutoff,
* invalid Actual,
* duplicate observation,
* calibration holdout,
* old model version preservation.

Verify:

* NULL != 0,
* no future information,
* no horizon mixing,
* no model-version mixing,
* no baseline leakage,
* no TTM double counting.

Run the focused Stage 6 suite.

Then run:

`pytest src/tests -v`

only after the focused suite is clean.

Do not modify unrelated failing tests.

## REPORT

Append:

`REPORT — Stage 6 Prompt 21`

Include integration path, test coverage, focused result, full result, and unresolved issues.

Do not freeze Stage 6.

End:

`Stage 6 is NOT declared frozen.`

STOP.
==============================
Stage 6 Prompt 6

You are performing **Stage 6 Prompt 22** for:

`analyzer`

This is an **independent READ-ONLY final audit**.

Stage 1–5 are frozen.

Do not assume Stage 6 is correct because its tests pass.

## FIREWALL

Read-only.

No code changes.

No test changes.

No Git operations.

No GitHub.

No commits.

No branches/remotes.

No broad repository exploration.

Inspect the Stage 6 specification, Prompt 17–21 reports, Stage 6 implementation, and directly relevant tests only.

## OBJECTIVE

Determine independently whether Stage 6 satisfies its locked specification.

Audit the complete path:

`Forecast`
→ `Actual`
→ `PIT`
→ `Error`
→ `Accuracy`
→ `Bias`
→ `Baseline`
→ `Reliability`
→ `Calibration`
→ `Out-of-Sample`

Challenge the implementation behaviorally where possible.

Pay particular attention to:

1. PIT correctness.
2. Forecast → Actual identity.
3. horizon isolation.
4. model-version isolation.
5. zero/sign-change handling.
6. MAPE correctness.
7. Bias correctness.
8. Seasonal Naive correctness.
9. baseline comparison.
10. observation sufficiency.
11. Accuracy ≠ Bias.
12. Reliability ≠ Accuracy.
13. versioned Reliability parameters.
14. calibration requiring persistent evidence.
15. calibration creating a new model version.
16. no overwrite of old versions.
17. holdout/out-of-sample isolation.
18. no TTM double counting.
19. no future information.
20. no Stage 5 modification.
21. no Stage 7 logic.
22. full auditability.

Also verify that Reliability does NOT directly alter Forward P/E.

## CRITICAL QUESTION

For every major requirement classify it as:

* BEHAVIORALLY PROVEN
* STRUCTURALLY VERIFIED
* NOT PROVEN

Do not call something proven merely because a unit test exists.

If a genuine blocker is found:

STOP.

Do not fix it in this audit.

Report the exact blocker and why it matters.

## TESTS

Run the focused Stage 6 tests.

If and only if they pass, run:

`pytest src/tests -v`

Do not weaken tests.

## REPORT

Append:

`REPORT — Stage 6 Prompt 22`

Include:

* files inspected,
* production path,
* invariant audit,
* adversarial checks,
* focused result,
* full result,
* blockers,
* unresolved risks,
* proof-status classification.

Final classification must be exactly one:

`PASS — FREEZE ELIGIBLE`

or

`FAIL — REMEDIATION REQUIRED`

If PASS:

`Stage 6 is frozen.`

If FAIL:

`Stage 6 is NOT declared frozen.`

Do not implement anything in this prompt.
