# Stage 6 Prompts — Forecast Evaluation

## Stage 6 Prompt 17 — Preflight + Methodology Authority Audit

You are performing **Stage 6 Prompt 17** for the repository:

`analyzer`

Stage 1–4 are frozen.

Stage 5 has passed an independent adversarial validation and is **genuinely frozen**. Do not reopen or modify Stage 5 unless a concrete Stage 6 investigation proves a pre-existing defect that makes the Stage 6 contract impossible to satisfy. If that occurs, stop and report it; do not fix Stage 5 here.

This prompt is a **READ-ONLY preflight and methodology-authority audit**. It exists to prevent later implementation prompts from inventing financial methodology.

### HARD FIREWALL

Work locally only.

Do NOT:

* access GitHub;
* use GitHub CLI/API;
* fetch/pull/push;
* modify remotes;
* create commits;
* create/delete/switch branches;
* inspect Git history.

Do not perform broad repository exploration.

Inspect only:

* `PROJECT_HANDOFF_INSTRUCTIONS.md`;
* `06_Stage6_Forecast_Evaluation.md`;
* the latest Stage 5 freeze section in `temp_report.md`;
* files/symbols directly necessary to determine the current Stage 6 state.

Do not read unrelated Stage 1–5 implementation files unless a directly referenced Stage 6 dependency requires a specific symbol.

### OBJECTIVE

Determine the actual current Stage 6 state **and whether the locked specification contains sufficient methodological authority for implementation**.

First identify:

1. existing Stage 6 modules/classes/functions, if any;
2. existing database models/migrations directly related to forecast evaluation;
3. forecast/actual data structures Stage 6 can legitimately consume;
4. reusable PIT/query infrastructure;
5. existing Stage 6 tests;
6. implemented vs missing specification requirements;
7. Stage 5 interfaces that Stage 6 may consume without modifying Stage 5;
8. architectural conflicts.

Then perform a dedicated **Methodology Authority Audit**.

For every item below, determine whether the repository/specification provides an authoritative, explicit rule that can be implemented without inventing thresholds, formulas, windows, fallback rules, or classifications.

Audit at minimum:

### A. Forecast → Actual semantics

Verify the exact meaning of:

* Forecast Cutoff;
* Forecast Timestamp;
* Financial Period;
* Actual Publication Timestamp;
* ReportVersion identity;
* eligibility of an Actual published after the forecast cutoff.

Explicitly distinguish:

**The Actual outcome may be published after the forecast cutoff and is the outcome being evaluated. PIT rules must prevent future information from entering the forecast or evaluation-input construction; they must NOT reject a valid later-published Actual merely because it was unavailable at forecast time.**

Determine whether the mapping key and tie-breaking rules are authoritative.

### B. Error and metric regimes

Verify authority for:

* Error;
* Percentage Error;
* APE;
* MAPE;
* Bias;
* ZERO_BASE;
* LOSS_TO_PROFIT;
* PROFIT_TO_LOSS;
* SIGN_CHANGE;
* NULL vs zero;
* invalid/suspicious/unmapped/restated Actual handling.

Do not invent percentage-metric behavior where the specification is silent.

### C. Observation sufficiency

Verify the authority for:

* minimum observations;
* confidence bands;
* duplicate handling;
* grouping by Company + Metric + Horizon + Model Version;
* whether invalid observations count.

### D. Seasonal Naive baseline

This is a critical authority audit.

Determine whether the specification/repository explicitly defines:

* the seasonal period/frequency for each supported metric/horizon;
* the exact Seasonal Naive formula;
* required historical observations;
* PIT construction rules;
* insufficient-history behavior;
* fallback behavior, if any;
* duplicate handling;
* whether the baseline is evaluated using the same eligible observation set as the model.

If any of these are not authoritative, classify the gap as **UNRESOLVED METHODOLOGY AUTHORITY**. Do not invent a seasonal period, fallback, or formula.

### E. Reliability methodology

Determine whether there is authoritative methodology for:

* AccuracyScore from MAPE;
* BiasControlScore from Bias;
* BaselineAdvantageScore from baseline improvement;
* Observation Confidence;
* Confidence Adjustment;
* Performance Score;
* Reliability 0–100;
* handling of unavailable components;
* bounds/clamping;
* versioning of all mapping parameters.

The specification's 50% / 20% / 30% weights are not by themselves sufficient authority for the mapping functions.

Do not invent thresholds or piecewise functions.

### F. Calibration methodology

Determine whether there is authoritative methodology for:

* persistent bias;
* minimum number of observations;
* bias magnitude threshold;
* consecutive/repeated observations;
* candidate vs calibrated transition;
* calibration scope;
* evidence period;
* training/calibration vs holdout/OOS separation;
* creation of a new Model Version;
* acceptance/rejection of a calibrated version.

Do not invent persistence thresholds.

### G. Data-quality eligibility

Determine authoritative rules for MISSING, ESTIMATED, SUSPICIOUS, UNMAPPED, RESTATED and whether/how each state can participate in evaluation.

### CLASSIFICATION

For every major item, classify it as exactly one of:

* AUTHORITATIVE
* IMPLEMENTED
* PARTIAL
* UNRESOLVED METHODOLOGY AUTHORITY
* BLOCKER
* REUSABLE INFRASTRUCTURE

A passing test is not methodology authority.

Do not convert an example, constant, existing implementation detail, or arbitrary current behavior into a financial rule merely because it exists in code.

### IMPLEMENTATION RULE

Do NOT implement anything in Prompt 17.

Do NOT create files.

Do NOT modify tests.

If methodology authority is missing, record the exact missing decision and stop. Do not propose an invented value as a substitute.

### REPORT

Append to `temp_report.md`:

`REPORT — Stage 6 Prompt 17`

Include:

* current Stage 6 implementation state;
* reusable infrastructure;
* exact methodology-authority matrix;
* blockers;
* architectural questions;
* Stage 5 boundary/dependency observations;
* exact decisions that must be resolved before implementation.

End with exactly:

`Stage 6 is NOT declared frozen.`

STOP.

====================================

## Stage 6 Prompt 18 — Evaluation Data Foundation

You are performing **Stage 6 Prompt 18** for:

`analyzer`

Use the completed **Stage 6 Prompt 17** report in `temp_report.md` as the discovery and authority result.

Stage 1–4 and Stage 5 are frozen.

### FIREWALL

Work locally only.

No GitHub, GitHub CLI/API, push, pull, remote changes, Git history, branches, or commits.

Do not modify Stage 1–5.

Do not perform broad repository exploration.

Inspect only files identified by P17 as necessary, plus directly referenced symbols.

### PRECONDITION

Do not invent any methodology marked **UNRESOLVED METHODOLOGY AUTHORITY** by P17.

If the evaluation data foundation itself depends on an unresolved methodological decision, isolate that dependency and report it rather than silently choosing a rule.

### OBJECTIVE

Implement only the **Stage 6 evaluation data foundation**.

Establish the minimum auditable structures required to represent:

* forecast identity;
* company;
* metric;
* financial period;
* forecast horizon;
* model version;
* forecast cutoff;
* forecast timestamp;
* forecast value;
* corresponding actual;
* actual ReportVersion identity;
* actual publication timestamp;
* evaluation status;
* evaluation timestamp.

Preserve the distinction between:

* Forecast Cutoff;
* Forecast Timestamp;
* Financial Period;
* Actual Publication Timestamp.

### FORECAST → ACTUAL PIT CONTRACT

A valid evaluation may use an Actual whose publication occurs **after** the forecast cutoff. That later publication is the outcome being evaluated.

PIT protection means:

* the forecast itself;
* baseline inputs;
* historical/evaluation inputs;
* ReportVersion selection;
* any other information used to construct or assess the forecast

must not use information unavailable at the forecast cutoff.

Do NOT reject a valid Actual merely because it was unavailable at forecast time.

Do NOT select an Actual merely because it is the latest database value.

Actual selection must use the authoritative identity/mapping rules established by P17 and the Stage 6 specification.

Preserve:

`NULL != 0`.

Do not silently substitute zero for missing Actuals.

Do not implement:

* MAPE;
* Bias;
* Reliability;
* Calibration;
* Valuation;
* new forecasting logic;
* new Stage 5 logic.

### TESTS

Add focused behavioral tests for:

* Forecast → Actual identity;
* later-published Actual being eligible as the evaluation outcome;
* PIT leakage into forecast/evaluation inputs being rejected;
* invalid ReportVersion/publication handling;
* horizon isolation;
* model-version isolation;
* duplicate observations;
* NULL vs zero;
* invalid/suspicious/unmapped/restated Actual handling according to P17 authority.

Run only focused Stage 6 tests.

### REPORT

Append:

`REPORT — Stage 6 Prompt 18`

Include:

* files changed;
* data contract;
* Forecast → Actual mapping;
* PIT behavior;
* tests;
* unresolved methodology/architecture gaps.

Do not claim Stage 6 complete.

End:

`Stage 6 is NOT declared frozen.`

STOP.

====================================

## Stage 6 Prompt 19 — Evaluation Metrics + Baseline

You are performing **Stage 6 Prompt 19** for:

`analyzer`

Use:

* `06_Stage6_Forecast_Evaluation.md`;
* Prompt 17 methodology-authority findings;
* Prompt 18 report

from `temp_report.md`.

Stage 1–5 are frozen.

### FIREWALL

Local working tree only.

No GitHub, Git operations, commits, remotes, branches, Git history, or broad repository exploration.

Do not modify Stage 1–5.

Inspect only Stage 6 files and directly referenced symbols.

### PRECONDITION

Do not invent financial methodology.

If P17 identified an unresolved authority gap for a specific metric or baseline rule, do not silently choose a threshold/formula/fallback. Implement only the portions whose methodology is authoritative and report the unresolved portion.

### OBJECTIVE

Implement the Stage 6 **evaluation metrics layer** and the authorized **Seasonal Naive baseline** only.

### FORECAST ERROR

`Error = Actual - Forecast`

### PERCENTAGE ERROR

`(Actual - Forecast) / abs(Forecast)`

### APE

`abs(Actual - Forecast) / abs(Forecast)`

### MAPE

Mean of valid APE observations only.

### BIAS

Mean signed percentage error.

Positive Bias = under-forecast.

Negative Bias = over-forecast.

Respect the authoritative regime rules for:

* zero forecast;
* zero base;
* LOSS_TO_PROFIT;
* PROFIT_TO_LOSS;
* SIGN_CHANGE.

Do not produce misleading percentage metrics for regimes where the specification says they are invalid. Absolute error may remain available.

Do not silently convert unavailable percentage metrics into zero.

### HORIZON ISOLATION

Keep:

* 1M;
* 3M;
* 6M;
* 12M

independent.

Never mix horizons.

### MODEL-VERSION ISOLATION

Never mix Model Version observations.

### OBSERVATION SUFFICIENCY

Implement exactly the authorized specification:

* <5 → INSUFFICIENT_DATA;
* 5–7 → LOW_CONFIDENCE;
* 8–11 → MODERATE_CONFIDENCE;
* >=12 → ADEQUATE.

Use valid, nonduplicate observations only, according to P17/P18 authority.

### SEASONAL NAIVE BASELINE

Implement Seasonal Naive **only according to an explicit authoritative methodology**.

The implementation must have an explicit, auditable:

* seasonal period;
* formula;
* required history;
* PIT construction;
* insufficient-history behavior;
* duplicate handling;
* eligible observation policy.

Do not invent any of these.

Implement, where authorized:

* baseline value;
* baseline error;
* baseline MAPE;
* relative model improvement.

If the Seasonal Naive methodology is still unresolved, stop that portion and report the exact blocker instead of inventing a baseline.

### TESTS

Add behavioral tests for:

* error sign;
* zero denominators;
* zero/sign-change regimes;
* horizon mixing;
* model-version mixing;
* duplicate observations;
* PIT leakage;
* invalid Actuals;
* invalid baseline inputs;
* baseline/model comparison;
* insufficient baseline history.

Run focused Stage 6 tests.

Do not implement Reliability or Calibration yet.

Do not connect anything to Stage 7.

### REPORT

Append:

`REPORT — Stage 6 Prompt 19`

Include:

* exact formulas;
* regime behavior;
* PIT behavior;
* horizon/version isolation;
* observation sufficiency;
* Seasonal Naive methodology actually used;
* baseline behavior;
* tests;
* unresolved authority gaps.

End:

`Stage 6 is NOT declared frozen.`

STOP.

====================================

## Stage 6 Prompt 20 — Reliability + Calibration Governance

You are performing **Stage 6 Prompt 20** for:

`analyzer`

Read:

* the Stage 6 specification;
* Prompt 17–19 reports in `temp_report.md`;
* only directly relevant Stage 6 implementation files.

Stage 1–5 are frozen.

### FIREWALL

Local only.

No GitHub, Git operations, commits, branches, remotes, Git history, or broad exploration.

Do not modify Stage 1–5.

### PRECONDITION

Do not invent Reliability or Calibration methodology.

If P17 identified missing authority for any mapping threshold, confidence adjustment, persistence criterion, or calibration transition, that rule must be resolved before implementation.

Existing constants or convenient thresholds are not automatically authoritative.

### OBJECTIVE

Implement only:

1. Forecast Reliability;
2. Calibration state;
3. Calibration versioning;
4. explicit training/calibration vs holdout/OOS separation.

### RELIABILITY ARCHITECTURE

Reliability must remain distinct from Accuracy and Bias.

Use the authorized V1 architecture:

`Accuracy + Bias Control + Baseline Advantage`
→ `Performance Score`
→ `Confidence Adjustment`
→ `Reliability 0–100`

Weights:

* Accuracy: 50%;
* Bias Control: 20%;
* Baseline Advantage: 30%.

However, the weights alone do NOT authorize arbitrary score mappings.

The following must be explicit and versioned:

* MAPE → AccuracyScore;
* Bias → BiasControlScore;
* Baseline Improvement → BaselineAdvantageScore;
* Observation Confidence;
* Confidence Adjustment;
* Reliability calculation;
* bounds/clamping;
* behavior when a component is unavailable.

Do not invent these mappings.

Do not allow:

`Performance Score = Reliability`

unless the authorized confidence-adjustment methodology explicitly makes them equal for that case.

### CALIBRATION

Implement:

* NO_CALIBRATION;
* CALIBRATION_CANDIDATE;
* CALIBRATED.

Calibration requires authoritative evidence of persistent/repeated systematic bias.

Do not calibrate from one observation.

Do not invent:

* minimum observation count;
* bias magnitude threshold;
* consecutive-observation requirement;
* confidence requirement;
* candidate/calibrated transition rule.

Calibration must:

* create a new Model Version;
* never overwrite the previous version;
* preserve original evaluations;
* remain auditable;
* have explicit scope where possible (Metric + Horizon + Model Version).

Do NOT directly do:

`Forecast × (1 + Bias)`

inside the existing model version.

Calibration must produce a versioned future model configuration.

### OUT-OF-SAMPLE

Represent the distinction between:

* calibration/training period;
* holdout/out-of-sample evaluation period.

Holdout outcomes must not create or qualify the calibration that is subsequently evaluated on that same holdout.

Preserve the temporal ordering.

### TESTING REQUIREMENT

Apply the MANDATORY MULTI-LAYER TESTING DOCTRINE below.

For P20 specifically, every newly authorized Reliability mapping, confidence adjustment, unavailable-component rule, calibration state transition, and model-version transition must have:
* Layer 1 unit/formula coverage;
* Layer 2 contract/boundary coverage;
* Layer 3 production-path coverage where the behavior is wired into the Stage 6 path;
* Layer 4 adversarial/negative coverage;
* Layer 5 focused regression coverage.

Do not write numeric expected values for B2/B7/B3/B4 while those methodology decisions remain unresolved. For unresolved rules, the required test is fail-closed behavior plus an explicit report of the missing authority.

### TESTS

Add behavioral tests for the authorized portions of:
* Reliability ≠ Accuracy;
* confidence adjustment;
* unavailable Reliability components;
* persistent vs isolated bias only if the persistence rule is authoritative; otherwise test that unresolved persistence cannot produce CALIBRATED;
* NO_CALIBRATION;
* CALIBRATION_CANDIDATE only when the transition rule is authoritative;
* CALIBRATED only when the transition rule is authoritative;
* new model version;
* old version preservation;
* calibration/training vs holdout isolation;
* PIT leakage.

Do not connect Reliability to P/E.

### MANDATORY MULTI-LAYER TESTING DOCTRINE

Testing in Stage 6 is a multi-layer verification requirement, not a single unit-test pass.

For every implemented Stage 6 behavior, apply all applicable layers:

1. Layer 1 — Unit / Formula
   * Test deterministic formulas, mappings, state transitions, boundary values, and edge cases.
   * Cover normal and pathological inputs.
   * Verify exact numeric results where methodology is authoritative.

2. Layer 2 — Contract / Boundary
   * Test PIT cutoff/publication semantics.
   * Test ReportVersion validity and Actual identity.
   * Test Forecast Horizon and Model Version isolation.
   * Test NULL != 0.
   * Test duplicate handling.
   * Test data-quality eligibility.
   * Test Stage 5 and Stage 7 boundaries.
   * Test unavailable/insufficient components fail closed rather than silently becoming zero or a fabricated score.

3. Layer 3 — Production-Path / Integration
   * At least one test for every critical invariant must exercise the actual Stage 6 production service/engine/orchestration path, not only a helper.
   * Prove that the production path actually uses the tested behavior.
   * Helper-level tests alone are not proof of production integration.

4. Layer 4 — Adversarial / Negative
   Intentionally attempt to violate the contract, including as applicable:
   * future information before cutoff;
   * later-published Actual incorrectly rejected;
   * invalid ReportVersion;
   * duplicate observations;
   * zero values;
   * sign-change regimes;
   * mixed horizons;
   * mixed Model Versions;
   * invalid/suspicious/unmapped/restated data;
   * unavailable components;
   * baseline leakage;
   * calibration holdout contamination;
   * attempts to turn unresolved methodology into a numeric default.
   Expected behavior must be explicit fail-closed behavior where methodology is unresolved.

5. Layer 5 — Regression
   * Run the focused Stage 6 suite first.
   * After focused tests are clean, run: pytest src/tests -v
   * Do not delete, weaken, bypass, or rewrite unrelated tests merely to obtain a green suite.
   * Classify failures as Stage 6 implementation defect, methodology-authority gap, or unrelated regression.

6. Layer 6 — Independent Audit
   * Prompt 22 must independently challenge both the implementation and the adequacy of the tests.
   * Passing tests alone are insufficient.
   * Re-run selected adversarial/production-path tests and inspect whether critical invariants are actually evidenced.

Evidence rule: Every critical invariant must have either (a) a behavioral/production-path test that genuinely proves it, or (b) an explicit structural proof. If only structurally verified, report it as structural—not behavioral—proof.

Anti-mirroring rule: Tests must not merely duplicate implementation internals. Critical tests must assert externally observable contract behavior, including at least one production-path test where applicable.

Methodology-authority rule: A passing test, existing constant, current implementation behavior, or convenient fallback is NOT authority for a financial methodology. If the required rule is unresolved, test and preserve the fail-closed boundary; do not manufacture a numeric expected value merely to make the test pass.


Do not implement Stage 7.

### REPORT

Append:

`REPORT — Stage 6 Prompt 20`

Include:

* architecture;
* exact authorized formulas/parameters;
* parameter versions;
* calibration behavior;
* versioning behavior;
* OOS separation;
* tests;
* unresolved methodology gaps.

End:

`Stage 6 is NOT declared frozen.`

STOP.

====================================

## Stage 6 Prompt 21 — Production Integration + Behavioral Matrix

You are performing **Stage 6 Prompt 21** for:

`analyzer`

Use the Stage 6 specification and Prompt 17–20 reports from `temp_report.md`.

Stage 1–5 are frozen.

### FIREWALL

Local only.

No GitHub, Git operations, commits, remotes, branches, Git history, or broad repository exploration.

Do not modify Stage 1–5.

Inspect only the Stage 6 implementation and directly referenced symbols.

### PRECONDITION

Do not integrate around unresolved methodology authority.

If a required Stage 6 rule remains unresolved, stop at that boundary and report the blocker. Do not invent a substitute.

### OBJECTIVE

Connect the implemented Stage 6 components into one auditable production path:

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
→ `New Model Version / OOS Evaluation`

Do NOT generate forecasts.

Do NOT alter Stage 5.

Do NOT implement Stage 7.

### MANDATORY MULTI-LAYER PRODUCTION-PATH TESTING

Apply the MANDATORY MULTI-LAYER TESTING DOCTRINE defined in Prompt 20.

P21 is the first prompt where the complete production path must be proven. Do not accept helper-level coverage as sufficient.

At minimum, the integrated path must be exercised behaviorally from:

Forecast Version → PIT-safe Actual → Error → Accuracy/Bias → Baseline → Sufficiency → Performance Score → Reliability → Calibration/OOS boundary

For every unresolved methodology blocker carried from P17–P20, the production path must demonstrate a safe fail-closed boundary rather than inventing a value.

### BEHAVIORAL TEST MATRIX

Ensure coverage for the following where authoritative; for unresolved methodology items, test the required fail-closed behavior instead:
* normal forecast/actual;
* under-forecast;
* over-forecast;
* zero forecast;
* zero actual where the current authority remains unresolved;
* LOSS_TO_PROFIT;
* PROFIT_TO_LOSS;
* SIGN_CHANGE;
* each horizon independently;
* separate model versions;
* insufficient observations;
* low/moderate/adequate confidence;
* baseline better than model;
* model better than baseline;
* zero baseline dispersion/error where applicable;
* persistent bias only if the persistence rule is authoritative;
* isolated bias;
* PIT cutoff;
* later-published Actual as outcome;
* invalid Actual;
* duplicate observation;
* invalid/suspicious/unmapped/restated data according to authorized rules;
* calibration training period;
* calibration holdout;
* old model-version preservation;
* Reliability component unavailability.

Verify:
* NULL != 0;
* no future information leaks into forecast/evaluation inputs;
* no horizon mixing;
* no model-version mixing;
* no baseline leakage;
* no TTM double counting;
* no double counting across overlapping evaluation horizons;
* no Reliability → Forward P/E numerical adjustment;
* no Stage 5 modification;
* no unresolved methodology gap is silently converted into a numeric default.

Run focused Stage 6 tests first.

Only after the focused suite is clean, run:

pytest src/tests -v

Do not modify unrelated failing tests.

### REPORT

Append:

`REPORT — Stage 6 Prompt 21`

Include:

* integrated production path;
* behavioral matrix coverage;
* focused test result;
* full-suite result;
* unresolved issues;
* proof limitations.

Do not freeze Stage 6.

End:

`Stage 6 is NOT declared frozen.`

STOP.

====================================

## Stage 6 Prompt 22 — Independent Final Audit

You are performing **Stage 6 Prompt 22** for:

`analyzer`

This is an **independent READ-ONLY final audit**.

Stage 1–5 are frozen.

Do not assume Stage 6 is correct because its tests pass.

### FIREWALL

Read-only.

No code changes.

No test changes.

No Git operations.

No GitHub.

No commits.

No branches/remotes.

No Git history.

No broad repository exploration.

Inspect only:

* `06_Stage6_Forecast_Evaluation.md`;
* Prompt 17–21 reports in `temp_report.md`;
* Stage 6 implementation;
* directly relevant tests;
* directly referenced dependencies required to verify Stage 6 boundaries.

### OBJECTIVE

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

### REQUIRED AUDIT AREAS

At minimum audit:

1. Forecast → Actual identity.
2. Later-published Actual semantics.
3. PIT correctness.
4. Forecast cutoff vs Actual publication timestamp.
5. horizon isolation.
6. model-version isolation.
7. zero/sign-change handling.
8. MAPE correctness.
9. Bias correctness.
10. Seasonal Naive methodology and PIT construction.
11. baseline comparison.
12. observation sufficiency.
13. Accuracy ≠ Bias.
14. Reliability ≠ Accuracy.
15. versioned Reliability parameters.
16. missing/unavailable Reliability components.
17. persistent-bias evidence.
18. calibration candidate/calibrated transitions.
19. calibration creates a new Model Version.
20. old Model Version preservation.
21. training/calibration vs holdout/OOS isolation.
22. no TTM double counting.
23. no future information leakage.
24. no horizon overlap/double counting.
25. no Stage 5 modification.
26. no Stage 7 logic.
27. full auditability to ReportVersion/publication timestamp.
28. Reliability does NOT numerically alter Forward P/E.

### METHODOLOGY AUTHORITY CHECK

Independently verify that no arbitrary or undocumented:

* thresholds;
* score mappings;
* seasonal periods;
* fallback rules;
* persistence criteria;
* calibration criteria;
* confidence adjustments

were introduced merely because implementation needed a value.

A test passing does not make an invented methodology authoritative.

### PROOF STATUS

For every major requirement classify it as exactly one of:

* BEHAVIORALLY PROVEN;
* STRUCTURALLY VERIFIED;
* NOT PROVEN.

Do not call something behaviorally proven merely because a unit test exists; inspect what the test actually proves and whether the production path uses the tested behavior.

### BLOCKER RULE

If a genuine blocker or unresolved methodology-authority issue is found:

STOP.

Do not fix it in this audit.

Report:

* exact blocker;
* affected requirement;
* why it is material;
* whether it is implementation defect or methodology-authority gap;
* exact evidence.

### MULTI-LAYER INDEPENDENT VERIFICATION

Apply the MANDATORY MULTI-LAYER TESTING DOCTRINE defined in Prompt 20, but act independently rather than trusting previous reports.

P22 must explicitly verify all six layers:
1. unit/formula correctness;
2. contract/boundary correctness;
3. production-path integration;
4. adversarial/negative behavior;
5. focused + full regression;
6. independent audit of test adequacy.

For each critical invariant, trace the requirement to actual evidence. A test that merely calls an internal helper is not sufficient proof of the production path. A green regression suite is not sufficient proof of methodology authority.

Before declaring PASS, challenge at least:
* future information injected before cutoff;
* later-published Actual incorrectly rejected;
* invalid ReportVersion;
* duplicate observations;
* NULL vs zero;
* zero/sign-change regimes;
* mixed horizons;
* mixed Model Versions;
* baseline leakage;
* unavailable Reliability component;
* unresolved methodology being forced into a numeric default;
* calibration holdout contamination;
* old Model Version overwrite;
* Reliability → Forward P/E leakage.

### TESTS

Run focused Stage 6 tests.

Inspect whether the focused tests genuinely exercise the production path and whether critical invariants have adequate adversarial coverage.

If and only if the focused suite is clean, run:

pytest src/tests -v

Do not weaken, delete, bypass, or rewrite tests merely to obtain a green suite.

If a failure is found, distinguish implementation defect, methodology-authority gap, and unrelated regression; do not fix anything in this read-only audit.

### REPORT

Append:

`REPORT — Stage 6 Prompt 22`

Include:

* files inspected;
* production path;
* methodology-authority audit;
* invariant audit;
* adversarial checks;
* focused result;
* full result;
* blockers;
* unresolved risks;
* proof-status classification.

Final classification must be exactly one:

`PASS — FREEZE ELIGIBLE`

or

`FAIL — REMEDIATION REQUIRED`

If and only if the final audit passes all freeze criteria:

`Stage 6 is frozen.`

Otherwise:

`Stage 6 is NOT declared frozen.`

Do not implement anything in this prompt.
======================================================

Stage 6 Prompt 23 - Legacy Methodology De-Authorization

You are continuing as the primary engineering agent for the repository:

`analyzer`

This is a financial-data application. Financial correctness, auditability, point-in-time correctness, deterministic behavior, and preservation of explicit methodology boundaries are more important than implementation speed.

## Stage 6 Context

Stage 6 is the Forecast Evaluation layer.

Stage 5 is FROZEN and MUST NOT be modified.

Stage 4 is FROZEN and MUST NOT be modified.

Stage 7 is outside the current scope and MUST NOT be modified.

The current Stage 6 production path introduced in Prompts 18–21 is intentionally fail-closed where methodology is not yet authorized.

Prompt 22 performed an independent final audit and identified one implementation blocker:

### B-LEGACY — Unauthorized Legacy Stage 6 Methodology Remains Executable

The new Stage 6 path behaves correctly and fails closed where methodology is unresolved.

However, older Stage 6 implementation paths remain executable and expose unauthorized methodology, including:

* `accuracy_score_from_mape(...)`
* `bias_score(...)`
* `baseline_advantage_score(...)`
* `confidence_multiplier(...)`
* `detect_persistent_bias(...)`
* `is_underperforming_baseline(...)`
* legacy Seasonal Naive behavior using `history[-lag]`
* legacy numeric Reliability calculation
* `CALIBRATION_CANDIDATE`
* creation of `V1.CAL1`
* related exports and tests that still treat these behaviors as valid methodology

The problem is NOT merely missing tests.

The problem is that unauthorized methodology remains executable.

This prompt exists ONLY to remove/de-authorize those legacy executable paths.

---

# 1. HARD CONTEXT FIREWALL

You MUST obey all of the following:

* Work ONLY in the local working tree.
* Do NOT access GitHub.
* Do NOT use GitHub CLI/API.
* Do NOT fetch.
* Do NOT pull.
* Do NOT push.
* Do NOT modify remotes.
* Do NOT create/delete/rename branches.
* Do NOT commit.
* Do NOT inspect Git history.
* Do NOT perform repository-wide audits.
* Do NOT scan the entire repository.
* Do NOT search unrelated Stage 1–5 or Stage 7 code.
* Do NOT reopen frozen stages.

The user handles Git operations separately.

If you encounter a required dependency outside the explicitly allowed scope below, STOP and report it rather than expanding the scope automatically.

---

# 2. PRIMARY OBJECTIVE

Remove or de-authorize the executable Legacy Stage 6 methodology identified by Prompt 22.

The objective is:

> After this prompt, no executable Stage 6 production path may calculate or expose unauthorized Reliability, Calibration Candidate, or legacy score methodology.

The new P18–P21 fail-closed production path MUST remain intact.

Do NOT invent replacement methodology.

Do NOT solve the unresolved Stage 6 methodology blockers B1–B9.

Do NOT freeze Stage 6.

---

# 3. EXPLICITLY ALLOWED INSPECTION SCOPE

Do NOT explore the repository broadly.

Start from the exact implementation/report references identified by Prompt 22 and inspect only the files containing these legacy symbols or their directly connected Stage 6 exports/tests.

Target symbols:

### Legacy score functions

* `accuracy_score_from_mape`
* `bias_score`
* `baseline_advantage_score`
* `confidence_multiplier`

### Legacy bias/calibration logic

* `detect_persistent_bias`
* `is_underperforming_baseline`
* `CALIBRATION_CANDIDATE`
* `V1.CAL1`

### Legacy evaluation behavior

* numeric Reliability calculation
* legacy Seasonal Naive implementation using `history[-lag]`
* related legacy Calibration construction

### Related exports/tests

Only inspect exports/imports/tests directly referencing the above symbols or behaviors.

Do NOT search for generic names such as `score`, `reliability`, `calibration`, or `baseline` across the whole repository.

Use targeted symbol/reference searches only.

---

# 4. FIRST STEP — TARGETED DISCOVERY ONLY

Before changing code:

1. Locate the exact definitions of the listed legacy symbols.
2. Locate their direct call sites.
3. Locate their direct exports/imports.
4. Locate tests that explicitly assert these legacy behaviors as valid.
5. Identify whether each symbol is:

   * production-executable,
   * test-only,
   * exported API,
   * or dead/unreachable.

Do NOT perform broader architecture exploration.

Do NOT inspect unrelated modules merely because they mention Stage 6 concepts.

Produce a short internal scope map before implementation.

If removing a symbol would require touching an unrelated module outside this explicit scope, STOP and report the dependency instead of expanding the task.

---

# 5. REQUIRED IMPLEMENTATION

For every confirmed legacy executable path:

## A. Remove or de-authorize unauthorized numeric scoring

The following MUST NOT remain executable as authoritative Stage 6 methodology:

* `accuracy_score_from_mape(...)`
* `bias_score(...)`
* `baseline_advantage_score(...)`
* `confidence_multiplier(...)`

Remove them from the production Stage 6 execution path.

If complete deletion is safe within the explicitly allowed scope, delete them.

If deletion would break unrelated infrastructure, de-authorize them so they cannot be used by the production Stage 6 path.

Do NOT replace them with invented mappings.

Do NOT create new numeric thresholds.

---

## B. Remove/de-authorize legacy persistent-bias thresholds

The following MUST NOT remain authoritative:

* `detect_persistent_bias(min=5, threshold=5%)`
* `is_underperforming_baseline(count>=5)`

These numeric criteria were not authorized by the locked Stage 6 methodology.

They MUST NOT determine Calibration state or Reliability.

Do NOT replace them with alternative thresholds.

Do NOT infer new persistence criteria.

---

## C. Remove/de-authorize legacy Calibration Candidate path

The following legacy behavior MUST no longer be executable as authoritative Stage 6 behavior:

* `CALIBRATION_CANDIDATE`
* automatic creation of `V1.CAL1`
* `holdout_passed` being sufficient to create a calibrated model/version
* any automatic calibration transition based on the unauthorized legacy thresholds

The authorized Stage 6 path currently supports:

* `NO_CALIBRATION`

while calibration methodology remains unresolved.

Preserve that fail-closed behavior.

Do NOT implement the missing calibration methodology in this prompt.

Do NOT create a new Calibration Candidate algorithm.

---

## D. Remove/de-authorize legacy numeric Reliability

The old path MUST NOT produce numeric Reliability using unauthorized mappings or thresholds.

The production behavior must remain:

* Reliability unavailable / `None` where the methodology is unresolved.

Do NOT substitute:

* `Performance Score`
* `Accuracy`
* `Bias`
* any other component

as Reliability.

Do NOT invent a fallback.

---

## E. Legacy Seasonal Naive

The legacy Seasonal Naive implementation using:

`history[-lag]`

MUST NOT remain an independently executable authoritative Stage 6 baseline if its seasonal period/history/PIT methodology is not explicitly authorized.

Do NOT invent a seasonal period.

Do NOT choose a fallback lag.

Do NOT create numeric expected values for the unresolved Seasonal Naive methodology.

If the new P19/P21 path already fails closed correctly, preserve that behavior.

Only remove/de-authorize the legacy executable path that bypasses the current methodology gate.

---

# 6. PRESERVE THE NEW P18–P21 PATH

This is critical.

Do NOT modify the architecture or behavior established by:

* Prompt 18 — Evaluation Data Foundation
* Prompt 19 — Metrics + Baseline
* Prompt 20 — Reliability + Calibration Governance
* Prompt 21 — Production Integration

The following behavior MUST remain intact:

* Forecast → Actual identity
* Actual may be published after Forecast Cutoff
* PIT applies to forecast/evaluation inputs, not the Actual outcome
* invalid ReportVersion is rejected
* horizon isolation
* model-version isolation
* duplicate handling
* NULL != 0
* invalid/suspicious/unmapped/restated handling
* exact Error semantics
* MAPE/Bias fail-closed behavior
* unresolved Seasonal Naive methodology remains unavailable
* unresolved Reliability methodology remains unavailable
* Calibration remains `NO_CALIBRATION` unless explicitly authorized
* no Forecast × (1 + Bias)
* no Reliability → Forward P/E
* no Stage 5 modification

---

# 7. TEST MIGRATION

Legacy tests that currently assert unauthorized methodology as correct MUST be changed.

They must NOT simply be deleted without replacement where doing so would leave the de-authorization unprotected.

Convert them into tests that prove the legacy methodology is no longer executable/authoritative.

Examples of acceptable assertions:

* legacy numeric scoring is no longer callable from the production Stage 6 path;
* legacy Calibration Candidate cannot be produced;
* unauthorized threshold logic cannot determine Calibration;
* legacy numeric Reliability cannot be produced;
* unresolved Seasonal Naive methodology fails closed;
* new production path remains unaffected.

Do NOT create numeric expected values for unresolved methodology.

Do NOT preserve old tests merely because they are green.

A test passing is not methodology authority.

---

# 8. SIX-LAYER TESTING REQUIREMENT

Use the Stage 6 multi-layer testing doctrine.

## Layer 1 — Unit / Formula

Verify removal/de-authorization of the targeted legacy functions and behaviors.

## Layer 2 — Contract / Boundary

Verify that unauthorized legacy methodology cannot cross into the Stage 6 production contract.

## Layer 3 — Production-Path / Integration

Exercise the actual Stage 6 production path and prove that:

* Reliability remains unavailable where methodology is unresolved;
* Calibration remains fail-closed;
* legacy score functions cannot affect the result.

## Layer 4 — Adversarial / Negative

Explicitly test attempts to trigger:

* legacy numeric Reliability;
* `CALIBRATION_CANDIDATE`;
* `V1.CAL1`;
* old persistent-bias thresholds;
* old baseline-underperformance threshold;
* legacy Seasonal Naive fallback.

These attempts must fail closed or be unreachable.

## Layer 5 — Regression

Run the relevant Stage 6 regression suite.

Then run:

`pytest src/tests -v`

Do not modify unrelated failing tests.

## Layer 6 — Independent Audit

Before completion, perform a narrow independent check of the exact legacy symbols listed in this prompt.

Confirm they are either:

* removed,
* unreachable from production Stage 6,
* explicitly de-authorized,
* or test-only with no production authority.

Do not perform a repository-wide audit.

---

# 9. EXPLICITLY FORBIDDEN IN THIS PROMPT

Do NOT:

* solve B1 Seasonal Naive methodology;
* solve B2 Reliability mappings;
* solve B3 persistence definition;
* solve B4 Calibration transition methodology;
* solve B5 ReportVersion tie-break methodology;
* solve B6 data-state participation;
* solve B7 unavailable Reliability methodology;
* solve B8 baseline-underperformance persistence;
* solve B9 duplicate-key methodology;
* solve `ZERO_ACTUAL_UNRESOLVED`;
* introduce new thresholds;
* introduce new score mappings;
* introduce new confidence multipliers;
* introduce new Calibration rules;
* introduce new Reliability fallback logic;
* modify Stage 5;
* modify Stage 4;
* modify Stage 7;
* modify valuation/P/E logic;
* modify Forecast Engine logic;
* redesign Stage 6 architecture.

This prompt is ONLY legacy de-authorization/removal.

---

# 10. STOP CONDITIONS

STOP immediately and report if:

1. A required dependency is outside the explicitly allowed Stage 6 legacy files/symbols.
2. Removing a legacy symbol would require changing Stage 5, Stage 4, or Stage 7.
3. The new P18–P21 production path would need architectural modification to complete the task.
4. A methodology decision is required that is not explicitly authorized by the Stage 6 specification.
5. You discover that the legacy behavior is actually required by the new production path.
6. You would need to invent a threshold, score mapping, seasonal period, persistence rule, or fallback.

Do NOT solve the blocker by expanding scope.

Report the exact dependency and stop.

---

# 11. REQUIRED FINAL REPORT

At the end, report:

### A. Legacy paths found

List the exact legacy symbols/behaviors discovered.

### B. De-authorized/removed

For each one, state exactly what changed.

### C. Preserved

Confirm that P18–P21 behavior remains intact.

### D. Tests

Report:

* Layer 1 result
* Layer 2 result
* Layer 3 result
* Layer 4 result
* Layer 5 result
* Layer 6 result
* focused Stage 6 test count
* full `pytest src/tests -v` result

### E. Remaining methodology blockers

Explicitly state that this prompt did NOT resolve:

* B1
* B2
* B3
* B4
* B5
* B6
* B7
* B8
* B9
* ZERO_ACTUAL_UNRESOLVED

unless a later authorized prompt resolves them.

### F. Stage 6 freeze status

The final status MUST remain:

**STAGE 6 NOT FROZEN**

Do NOT declare Stage 6 freeze eligibility from this prompt alone.

The purpose of this prompt is only to remove the B-LEGACY implementation blocker so that a later independent audit can reassess the remaining methodology blockers.

---

# 12. FINAL STOP CONDITION

After completing the targeted implementation and tests:

STOP.

Do not continue into methodology design.

Do not continue into a new Stage 6 prompt.

Do not modify any other stage.

Do not commit or push anything.

-----File Writing Rules (Critical — to prevent validation errors)-----
When using the Write tool, follow these rules strictly:

Never write a file all at once. Write a maximum of 150 lines per Write call.

Always complete the structure. The parameters file_path and content must both be sent as complete strings. If the content is long, split it into multiple parts and continue with the Edit tool.

Follow this pattern:

First: Write with the file header, imports, and main skeleton (maximum 100 lines).

Then: Edit to add each subsequent section (100–150 lines per call).

Finally: Edit to close the file and complete the remaining functions.

Before every Write, check whether the intended content exceeds 150 lines. If yes, divide it into logical chunks.

If a Write call fails, do not immediately retry. First check which parameter was incomplete, then continue with a smaller Write or use Edit.

For Python files: First write only the imports and def main(), then add functions one by one using Edit.
===========================================================

Stage 6 Prompt 24 - Independent Post-P23 De-authorization Audit

You are performing **Stage 6 Prompt 24** for the repository:

`lovelyroz/analyzer`

This is a financial-data application. Financial correctness, auditability, point-in-time correctness, deterministic behavior, and preservation of explicit methodology boundaries are more important than implementation speed.

## 1. PURPOSE

Prompt 23 removed the unauthorized Legacy Stage 6 methodology identified by Prompt 22.

Prompt 23 reported:

* `src/evaluation/engine.py` deleted;
* legacy scoring functions removed;
* legacy numeric Reliability path removed;
* legacy Seasonal Naive path removed;
* legacy Calibration Candidate path removed;
* legacy exports removed;
* legacy tests migrated to de-authorization tests;
* focused Stage 6: 126 passed;
* full suite: 810 passed, 2 skipped;
* B-LEGACY resolved.

This prompt is an **independent, READ-ONLY post-remediation audit**.

Its purpose is to independently verify that:

1. B-LEGACY is actually resolved;
2. no unauthorized Legacy Stage 6 executable path remains;
3. Prompt 23 did not accidentally weaken or bypass the P18–P21 production path;
4. the six-layer testing doctrine still holds;
5. the remaining B1–B9 methodology gaps are correctly classified and have NOT been silently converted into implementation rules.

This prompt MUST NOT implement any methodology.

This prompt MUST NOT modify code.

This prompt MUST NOT modify tests.

This prompt MUST NOT modify `temp_report.md`.

Do NOT freeze Stage 6 unless every required condition explicitly passes.

---

# 2. HARD FIREWALL

Work locally only.

Do NOT:

* access GitHub;
* use GitHub CLI/API;
* fetch;
* pull;
* push;
* modify remotes;
* create/delete/switch branches;
* commit;
* inspect Git history;
* perform repository-wide exploration.

Stage 1–5 are frozen.

Stage 4 MUST NOT be modified.

Stage 5 MUST NOT be modified.

Stage 7 MUST NOT be modified.

Do not inspect unrelated repository areas.

Do not perform a broad architecture review.

---

# 3. REQUIRED INPUTS

Read:

1. `06_Stage6_Forecast_Evaluation.md`
2. `temp_report.md`
3. the Prompt 22 report
4. the Prompt 23 report

Then inspect only the directly relevant current Stage 6 files.

The audit MUST be based on the current working tree, not merely on the claims in the Prompt 23 report.

Do not trust Prompt 23's conclusions without independently verifying them.

---

# 4. EXPLICIT AUDIT SCOPE

The primary audit scope is the current Stage 6 package and the exact legacy symbols/paths previously identified.

Inspect only the files necessary to verify:

### Legacy scoring

* `accuracy_score_from_mape`
* `bias_score`
* `baseline_advantage_score`
* `confidence_multiplier`

### Legacy persistence/bias

* `detect_persistent_bias`
* `is_underperforming_baseline`

### Legacy evaluation

* `ForecastEvaluationEngine`
* `evaluate_forecasts`
* `select_point_in_time_actual`
* `seasonal_naive_forecast`
* legacy numeric Reliability calculation

### Legacy calibration

* `CALIBRATION_CANDIDATE`
* `CALIBRATED`
* `calibration_model_version`
* `V1.CAL1`
* `holdout_passed`

### Legacy carriers/exports

* `ForecastEvaluationResult`
* `ReliabilityAssessment`
* package-level exports from `src/evaluation/__init__.py`

### New production path

Verify only the directly relevant P18–P21 path:

* `observation.py`
* `aggregate.py`
* `reliability.py`
* `pipeline.py`
* `schema.py`
* directly relevant Stage 6 tests

Do NOT search the whole repository for generic words such as:

* `reliability`
* `calibration`
* `score`
* `baseline`

Use targeted symbol/reference checks.

---

# 5. INDEPENDENT B-LEGACY VERIFICATION

Independently determine whether each of the following remains executable in production Stage 6:

| Legacy behavior                           | Required result            |
| ----------------------------------------- | -------------------------- |
| `accuracy_score_from_mape`                | absent / non-executable    |
| `bias_score`                              | absent / non-executable    |
| `baseline_advantage_score`                | absent / non-executable    |
| `confidence_multiplier`                   | absent / non-executable    |
| `detect_persistent_bias`                  | absent / non-executable    |
| `is_underperforming_baseline`             | absent / non-executable    |
| `ForecastEvaluationEngine`                | absent / non-executable    |
| `evaluate_forecasts`                      | absent / non-executable    |
| `select_point_in_time_actual`             | absent / non-executable    |
| `seasonal_naive_forecast`                 | absent / non-executable    |
| old numeric Reliability                   | absent                     |
| legacy `CALIBRATION_CANDIDATE` transition | unreachable                |
| `V1.CAL1` creation                        | unreachable                |
| `holdout_passed` → calibration            | not authoritative          |
| legacy result carriers                    | absent / non-authoritative |
| legacy package exports                    | absent                     |

Do NOT interpret a comment containing an old token as an executable implementation.

Distinguish:

* executable code;
* test-only code;
* comments/documentation;
* intentionally refused state literals.

---

# 6. CRITICAL CALIBRATION NUANCE

The current Stage 6 architecture may still contain:

* `CALIBRATION_CANDIDATE`
* `CALIBRATED`
* refusal states
* `derive_calibrated_version_name`
* `.CAL1` references

These are NOT automatically blockers.

The question is:

> Can an unresolved methodology currently cause a real production transition into CALIBRATION_CANDIDATE or CALIBRATED?

Verify behaviorally.

Acceptable current behavior while B3/B4 remain unresolved:

```text
NO_CALIBRATION
```

and/or an explicit refusal/unavailable state.

Unacceptable behavior:

```text
bias threshold
→ CALIBRATION_CANDIDATE
→ CALIBRATED
→ new model version
```

without authoritative methodology.

Do not remove legitimate refusal-state representations merely because their names exist.

---

# 7. CRITICAL RELIABILITY NUANCE

The current Stage 6 path intentionally withholds numeric Reliability while B2/B7 remain unresolved.

Verify that:

```text
Reliability = None
```

or equivalent explicit unavailable state remains the production result where the methodology is unresolved.

Verify that the system does NOT silently use:

* Performance Score;
* Accuracy;
* Bias;
* Observation Confidence;
* Baseline Improvement;
* arbitrary constants

as Reliability.

Do not invent a numeric expected Reliability.

---

# 8. NEW PRODUCTION PATH INTEGRITY

Independently trace:

```text
Forecast
→ Actual
→ PIT
→ Error
→ Accuracy/MAPE
→ Bias
→ Baseline Comparison
→ Observation Sufficiency
→ Reliability Governance
→ Calibration Governance
→ OOS
```

Verify that Prompt 23 did not break:

* later-published Actual semantics;
* PIT input protection;
* invalid ReportVersion handling;
* horizon isolation;
* Model Version isolation;
* duplicate quarantine;
* NULL != 0;
* zero/sign-change quarantine;
* MAPE;
* Bias;
* observation sufficiency;
* baseline comparison;
* OOS contamination protection;
* Forward P/E identity protection.

Do not redesign anything.

---

# 9. SIX-LAYER INDEPENDENT TEST AUDIT

Prompt 23 reported all six layers.

Independently inspect whether the tests actually prove the claims.

## Layer 1 — Unit / Formula

Verify that de-authorization tests actually establish absence/non-executability.

Do not accept a test that merely checks a comment or source string.

## Layer 2 — Contract / Boundary

Verify that removed legacy functionality cannot enter the public Stage 6 production contract through imports/exports.

## Layer 3 — Production Path

Verify that the actual `run_evaluation_pipeline` path remains fail-closed.

Do not accept helper-only tests as production proof.

## Layer 4 — Adversarial

Independently challenge attempts to trigger:

* legacy scoring;
* legacy numeric Reliability;
* legacy Seasonal Naive;
* `CALIBRATION_CANDIDATE`;
* `CALIBRATED`;
* `V1.CAL1`;
* old persistence thresholds;
* old baseline-underperformance threshold.

Expected result: absent, unreachable, or explicit fail-closed behavior.

## Layer 5 — Regression

Run:

```text
pytest <focused Stage 6 suite> -v
```

Then, only if focused tests pass:

```text
pytest src/tests -v
```

Do not modify tests.

Do not weaken tests.

Do not fix failures during this audit.

If tests fail, classify the failure and STOP.

## Layer 6 — Independent Audit

This prompt itself constitutes the independent audit layer.

Do not rely on Prompt 23's Layer 6 conclusion.

---

# 10. METHODOLOGY-AUTHORITY AUDIT

Confirm independently that Prompt 23 did NOT accidentally introduce any of the following:

* new numeric thresholds;
* new score mappings;
* new Reliability mappings;
* new confidence multipliers;
* new persistence criteria;
* new Calibration transition rules;
* new seasonal periods;
* new Seasonal Naive fallback rules;
* new ReportVersion tie-break rules;
* new data-state scoring rules;
* new duplicate-key rules;
* new baseline-selection rules.

Existing unresolved blockers remain:

* B1 — Seasonal Naive construction;
* B2 — Reliability mappings;
* B3 — persistence definition;
* B4 — Calibration transition;
* B5 — ReportVersion tie-break;
* B6 — data-state participation;
* B7 — unavailable Reliability components;
* B8 — baseline-underperformance persistence;
* B9 — duplicate-key definition;
* `ZERO_ACTUAL_UNRESOLVED`.

Do NOT solve them.

Classify each as:

* RESOLVED
* UNRESOLVED METHODOLOGY AUTHORITY
* IMPLEMENTATION DEFECT

Do not classify an unresolved methodology as resolved merely because the system fails closed.

---

# 11. STAGE 5 / STAGE 7 BOUNDARY CHECK

Verify that Prompt 23 did not modify:

* Stage 5 implementation;
* Stage 5 persistence;
* Stage 5 ForecastEngine;
* Stage 4 adapter/evidence logic;
* Stage 7 valuation;
* Forward P/E calculation.

This is a boundary verification only.

Do not reopen those stages.

---

# 12. REQUIRED PROOF CLASSIFICATION

For each major audit item classify exactly one:

* **BEHAVIORALLY PROVEN**
* **STRUCTURALLY VERIFIED**
* **NOT PROVEN**

Important:

A green test alone does NOT make methodology authoritative.

A deleted function may be structurally verified as absent.

A production-path behavior should be behaviorally proven only when the actual path is exercised.

An unresolved methodology must remain NOT PROVEN even if fail-closed behavior is proven.

---

# 13. BLOCKER RULE

If ANY of the following is discovered:

1. an executable unauthorized Legacy Stage 6 path remains;
2. Prompt 23 broke the P18–P21 production path;
3. a new unauthorized methodology was introduced;
4. Stage 5/Stage 4/Stage 7 was modified;
5. a methodology gap was silently converted into a numeric rule;
6. a regression failure is caused by Prompt 23;

then:

**STOP.**

Do not fix anything.

Report the exact blocker and classify it as:

* implementation defect;
* methodology-authority gap;
* regression;
* boundary violation.

---

# 14. FREEZE DECISION

Do NOT freeze Stage 6 merely because B-LEGACY is resolved.

For this prompt, the maximum acceptable result is:

### `PASS — B-LEGACY REMEDIATION VERIFIED`

This means:

* B-LEGACY independently verified as resolved;
* P18–P21 path preserved;
* no new unauthorized methodology;
* all six testing layers independently verified;
* remaining B1–B9 / ZERO_ACTUAL_UNRESOLVED remain explicitly unresolved.

If any of those conditions fail:

### `FAIL — REMEDIATION VERIFICATION FAILED`

Stage 6 remains NOT FROZEN.

Even a PASS in this prompt does NOT freeze Stage 6.

---

# 15. REQUIRED REPORT

Append to `temp_report.md`:

`REPORT — Stage 6 Prompt 24`

Include:

1. files inspected;
2. independent B-LEGACY verification;
3. legacy symbol status table;
4. new production-path verification;
5. six-layer testing audit;
6. methodology-authority audit;
7. Stage 5/Stage 7 boundary verification;
8. focused test result;
9. full regression result;
10. proof-status classification;
11. remaining blockers;
12. final classification.

The report MUST end with:

`Stage 6 is NOT declared frozen.`

---

# 16. FINAL STOP

This is a READ-ONLY audit.

Do not:

* modify code;
* modify tests;
* modify specifications;
* modify Stage 5;
* modify Stage 4;
* modify Stage 7;
* implement B1–B9;
* commit;
* push.

After writing the report, STOP.
-----File Writing Rules (Critical — to prevent validation errors)-----
When using the Write tool, follow these rules strictly:

Never write a file all at once. Write a maximum of 150 lines per Write call.

Always complete the structure. The parameters file_path and content must both be sent as complete strings. If the content is long, split it into multiple parts and continue with the Edit tool.

Follow this pattern:

First: Write with the file header, imports, and main skeleton (maximum 100 lines).

Then: Edit to add each subsequent section (100–150 lines per call).

Finally: Edit to close the file and complete the remaining functions.

Before every Write, check whether the intended content exceeds 150 lines. If yes, divide it into logical chunks.

If a Write call fails, do not immediately retry. First check which parameter was incomplete, then continue with a smaller Write or use Edit.

For Python files: First write only the imports and def main(), then add functions one by one using Edit.
===========================================================

Stage 6 Prompt 25 - Actual Outcome & Observation Eligibility Authority

You are performing **Stage 6 Prompt 25** for the repository:

`analyzer`

This is a financial-data application. Financial correctness, point-in-time correctness, auditability, deterministic behavior, and explicit methodology authority are more important than implementation speed.

Stage 6 Prompt 24 independently verified that:

* B-LEGACY is resolved;
* the unauthorized legacy Stage 6 paths are no longer executable;
* the P18–P21 production path remains intact;
* no new unauthorized methodology was introduced;
* focused Stage 6 tests pass;
* full regression passes.

Stage 6 is still NOT frozen.

The remaining methodology blockers include:

* B1 — Seasonal Naive construction;
* B2 — Reliability mappings;
* B3 — persistence definition;
* B4 — Calibration transition;
* B5 — ReportVersion tie-break;
* B6 — data-state participation;
* B7 — unavailable-component rule;
* B8 — baseline-underperformance persistence;
* B9 — duplicate-key definition;
* `ZERO_ACTUAL_UNRESOLVED`.

This prompt resolves ONLY:

1. B5 — ReportVersion tie-break;
2. B6 — data-state participation;
3. B9 — duplicate-key definition;
4. `ZERO_ACTUAL_UNRESOLVED`.

Do NOT solve B1, B2, B3, B4, B7, or B8.

---

# 1. HARD CONTEXT FIREWALL

Work ONLY in the local working tree.

Do NOT:

* access GitHub;
* use GitHub CLI/API;
* fetch;
* pull;
* push;
* modify remotes;
* create/delete/switch branches;
* commit;
* inspect Git history;
* perform repository-wide exploration.

Stage 1–5 are frozen.

Do NOT modify Stage 4.

Do NOT modify Stage 5.

Do NOT modify Stage 7.

Do NOT redesign Stage 6.

Do not inspect unrelated repository areas.

Inspect only:

* `06_Stage6_Forecast_Evaluation.md`;
* the P17–P24 sections of `temp_report.md`;
* current Stage 6 files directly responsible for:

  * Actual selection;
  * ReportVersion validation;
  * observation construction;
  * duplicate detection;
  * data-quality state handling;
  * zero/sign regime classification;
  * Stage 6 production pipeline;
  * directly related Stage 6 tests.

Use targeted symbol/reference searches only.

---

# 2. PRIMARY OBJECTIVE

Establish an explicit, auditable, deterministic methodology for:

```text
Forecast
→ corresponding Actual
→ ReportVersion selection
→ data-state eligibility
→ duplicate handling
→ zero/sign regime classification
```

The resulting rules must be authoritative and versioned/documented within Stage 6.

Then implement ONLY those rules in the Stage 6 production path.

Do not merely document the current implementation.

Do not treat existing behavior as authoritative unless the methodology is explicitly justified and recorded.

---

# 3. METHODOLOGY AUTHORITY RULE

This prompt is allowed to establish methodology authority for ONLY:

* B5;
* B6;
* B9;
* ZERO_ACTUAL_UNRESOLVED.

For these four items, you MUST explicitly define:

* rule;
* rationale;
* deterministic ordering;
* PIT implications;
* audit metadata;
* edge cases;
* tests.

Do NOT use arbitrary thresholds.

Do NOT use convenience-based behavior merely because the existing code already does it.

Every selected rule must be deterministic and financially defensible.

If an essential decision cannot be justified from:

1. the locked Stage 6 specification;
2. existing Stage 1 data semantics;
3. existing ReportVersion/publication semantics;
4. existing explicit project invariants;

then STOP and report the exact unresolved decision.

Do not invent a value merely to make the tests pass.

---

# 4. B5 — REPORTVERSION TIE-BREAK METHODOLOGY

Establish an explicit deterministic rule for selecting the Actual ReportVersion when multiple valid ReportVersions represent the same:

* company;
* metric;
* financial period.

The rule MUST address:

### A. Publication time

Determine how `publication_datetime` affects eligibility.

A ReportVersion published after the Forecast Cutoff MAY be used as the Actual outcome.

This is NOT PIT leakage.

PIT protects information used to construct the forecast/evaluation inputs.

The Actual is the eventual outcome.

### B. Restatement / multiple versions

When multiple valid ReportVersions exist for the same financial period, explicitly define which version represents the evaluation Actual.

The rule must prevent silent selection of:

* arbitrary database order;
* latest database row;
* surrogate ID merely because it is convenient;
* a future restatement when the methodology intends the first known outcome.

The selected rule MUST be deterministic.

### C. Recommended authority direction

Prefer an outcome definition that is:

* reproducible;
* auditable;
* independent of current database insertion order;
* resistant to hindsight/restatement leakage;
* compatible with later-published Actual semantics.

If the specification permits multiple defensible interpretations, document the chosen interpretation explicitly and explain why it is preferable for forecast evaluation.

### D. Audit metadata

The selected Actual MUST remain traceable to:

* ReportVersion identity;
* publication timestamp;
* financial period;
* company;
* metric.

Do not discard provenance.

---

# 5. B6 — DATA-QUALITY PARTICIPATION METHODOLOGY

Establish explicit participation rules for:

* `MISSING`;
* `ESTIMATED`;
* `SUSPICIOUS`;
* `UNMAPPED`;
* `RESTATED`.

For each state define exactly:

1. Can it participate in Actual selection?
2. Can it participate in Error?
3. Can it participate in MAPE?
4. Can it participate in Bias?
5. Can it count toward observation sufficiency?
6. Can it participate in baseline comparison?
7. Must it be quarantined?
8. Must it remain visible for audit purposes even when excluded?

Do NOT silently equate:

* unavailable with zero;
* suspicious with valid;
* unmapped with zero;
* missing with zero.

The methodology MUST distinguish:

### Valid outcome

An Actual that can legitimately be used for forecast evaluation.

### Invalid outcome

An Actual that must be excluded from scoring.

### Audit-visible but excluded outcome

A record that must remain traceable but must not affect evaluation metrics.

The resulting rules must be consistent across the Stage 6 pipeline.

Do not allow different Stage 6 modules to apply different eligibility rules.

---

# 6. ZERO ACTUAL METHODOLOGY

Explicitly resolve:

```text
Actual = 0
Forecast ≠ 0
```

This MUST NOT be treated as missing.

It MUST NOT be silently converted to zero error.

Use the existing Stage 6 definitions:

```text
Error = Actual - Forecast
```

Therefore:

```text
Actual = 0
Forecast ≠ 0
Error = -Forecast
```

The methodology MUST explicitly determine:

### A. Error

Absolute/signed error remains valid.

### B. Percentage Error

Determine whether the percentage-error denominator remains:

```text
abs(Forecast)
```

and whether the observation is eligible.

### C. APE / MAPE

Determine whether:

```text
APE = abs(Actual - Forecast) / abs(Forecast)
```

remains valid when Actual = 0 and Forecast ≠ 0.

If Forecast ≠ 0, there is no zero denominator in the percentage metric.

Do NOT incorrectly classify Actual=0 as ZERO_BASE merely because the Actual itself is zero.

### D. Sign regime

Explicitly distinguish:

* positive Forecast → zero Actual;
* negative Forecast → zero Actual;
* zero Forecast → zero Actual;
* zero Actual with non-zero Forecast.

Do not use ordinary growth semantics here.

### E. Sufficiency

If the observation is otherwise valid, determine whether it counts toward observation sufficiency.

The rule must be deterministic and consistent.

---

# 7. B9 — DUPLICATE-KEY METHODOLOGY

Establish the exact Stage 6 evaluation observation identity.

The identity MUST be deterministic.

At minimum evaluate the conceptual dimensions:

```text
Company
Metric
Financial Period
Forecast Horizon
Model Version
Forecast Cutoff
```

and determine whether additional identity fields are required, such as:

* Forecast timestamp;
* Forecast version/id;
* scenario;
* ReportVersion;
* Actual identity.

Do NOT blindly assume the existing key is authoritative.

Do NOT use a database surrogate ID as the business definition of uniqueness.

Explicitly distinguish:

### True duplicate

Two observations representing the same evaluation event.

### Legitimately distinct observation

Two forecasts that differ in an authorized dimension and therefore must not be collapsed.

### Conflicting duplicate

Two records claim the same evaluation identity but contain different forecast/actual/provenance values.

Conflicting duplicates MUST NOT be silently averaged, overwritten, or selected arbitrarily.

Prefer fail-closed/quarantine behavior.

The rule must be deterministic and auditable.

---

# 8. CROSS-CONSISTENCY REQUIREMENT

After defining B5, B6, B9, and ZERO_ACTUAL:

Verify that they do not conflict.

Specifically verify:

```text
ReportVersion selection
        ↓
Actual eligibility
        ↓
Duplicate identity
        ↓
Error
        ↓
APE/MAPE/Bias
        ↓
Observation sufficiency
```

There must be exactly one coherent interpretation.

Do not allow:

* Actual selection to use one eligibility rule while aggregation uses another;
* duplicate detection to remove valid distinct forecasts;
* zero Actual to be treated as missing;
* excluded observations to count toward sufficiency;
* invalid data states to affect MAPE/Bias;
* ReportVersion choice to depend on arbitrary database ordering.

---

# 9. IMPLEMENTATION SCOPE

After the methodology is explicitly established:

Modify ONLY the Stage 6 modules directly responsible for:

* Actual selection;
* ReportVersion handling;
* observation construction;
* duplicate handling;
* data-state eligibility;
* zero/sign classification;
* aggregation where necessary to enforce the new contract.

Do NOT modify:

* Stage 5;
* Stage 4;
* Stage 7;
* Reliability mappings;
* Calibration methodology;
* Seasonal Naive;
* persistence methodology;
* baseline-underperformance methodology.

Do not create a new forecasting engine.

---

# 10. VERSIONED / AUDITABLE METHODOLOGY

The newly resolved rules MUST be discoverable and auditable.

Do not hide methodology inside arbitrary implementation branches.

Record:

* methodology name/version;
* B5 rule;
* B6 state policy;
* B9 identity;
* zero-Actual policy.

Use the project's existing methodology/versioning/audit pattern where one exists.

Do NOT invent a large new framework merely to document four rules.

A small explicit constant/enum/documented policy is preferable to duplicated magic behavior.

---

# 11. MULTI-LAYER TESTING — MANDATORY

All six layers are required.

## Layer 1 — Unit / Formula

Test:

* ReportVersion ordering;
* tie-break;
* data-state eligibility;
* duplicate identity;
* zero Actual;
* Error;
* Percentage Error;
* APE;
* MAPE;
* Bias;
* zero/sign regimes.

Use exact numeric expected values where the methodology is now authoritative.

---

## Layer 2 — Contract / Boundary

Test:

* later-published Actual is accepted;
* invalid ReportVersion is rejected;
* ReportVersion tie-break is deterministic;
* excluded data states cannot enter scoring;
* duplicate identity is deterministic;
* conflicting duplicates fail closed;
* Actual=0 is not treated as missing;
* NULL != 0.

---

## Layer 3 — Production Path / Integration

Exercise the actual Stage 6 production pipeline.

At minimum prove:

```text
Actual selection
→ eligibility
→ duplicate validation
→ Error
→ MAPE/Bias
→ observation sufficiency
```

using the real production path.

Helper-only tests are insufficient.

---

## Layer 4 — Adversarial / Negative

Attempt:

1. multiple ReportVersions with different publication times;
2. multiple ReportVersions with identical publication times;
3. restated Actual;
4. invalid ReportVersion;
5. missing Actual;
6. estimated Actual;
7. suspicious Actual;
8. unmapped Actual;
9. conflicting duplicates;
10. duplicate forecasts with different horizons;
11. duplicate forecasts with different Model Versions;
12. duplicate forecasts with different Forecast Cutoffs;
13. Actual=0 / Forecast>0;
14. Actual=0 / Forecast<0;
15. Actual=0 / Forecast=0;
16. Forecast=0 / Actual≠0;
17. zero Actual combined with a sign-change case.

Every case must have an explicit expected result.

---

## Layer 5 — Regression

Run:

1. focused Stage 6 tests;
2. only if focused tests pass:

```text
pytest src/tests -v
```

Do not weaken or delete unrelated tests.

If a regression appears, classify it.

Do not silently alter unrelated Stage 1–5 tests.

---

## Layer 6 — Independent Audit

Before finalizing:

Independently inspect the implementation and tests AGAIN.

Verify that the implementation actually matches the methodology written in the report.

Specifically challenge:

* database-order dependence;
* surrogate-ID dependence;
* hidden fallback selection;
* state-to-zero conversion;
* zero Actual → missing conversion;
* duplicate overwrite;
* duplicate averaging;
* restatement leakage;
* inconsistent eligibility between observation and aggregation.

Do not trust Layer 1 tests alone.

---

# 12. REQUIRED INVARIANTS

The following MUST remain true:

1. `NULL != 0`.
2. Actual=0 is a valid numeric value unless excluded for an independent reason.
3. Error remains:

```text
Actual - Forecast
```

4. Percentage Error uses the authorized denominator:

```text
abs(Forecast)
```

where valid.
5. No ordinary percentage growth is used for sign changes.
6. Later-published Actual is allowed as outcome.
7. Future information MUST NOT enter forecast/evaluation inputs.
8. Invalid ReportVersion cannot become a valid Actual.
9. Duplicate conflicts cannot be silently resolved.
10. Horizon isolation remains intact.
11. Model Version isolation remains intact.
12. Stage 5 remains untouched.
13. Reliability remains unavailable because B2/B7 are unresolved.
14. Calibration remains fail-closed because B3/B4 are unresolved.
15. No Seasonal Naive methodology is introduced.
16. No baseline-underperformance methodology is introduced.

---

# 13. EXPLICITLY FORBIDDEN

Do NOT resolve:

* B1 Seasonal Naive;
* B2 Reliability mappings;
* B3 persistence;
* B4 Calibration transition;
* B7 unavailable Reliability components;
* B8 baseline-underperformance persistence.

Do NOT introduce:

* Reliability numbers;
* Calibration thresholds;
* Seasonal periods;
* confidence multipliers;
* arbitrary observation thresholds;
* baseline fallback rules;
* new Forecast Engine behavior;
* valuation behavior;
* Forward P/E behavior.

Do NOT modify Stage 5.

Do NOT modify Stage 4.

Do NOT modify Stage 7.

---

# 14. STOP CONDITIONS

STOP immediately if:

1. B5 cannot be resolved deterministically without an unsupported financial assumption.
2. B6 requires a rule that conflicts with Stage 1 data semantics.
3. B9 requires an architectural redesign outside Stage 6.
4. resolving zero Actual would require changing Stage 5 or Stage 7.
5. an implementation decision would require inventing B1/B2/B3/B4/B7/B8.
6. a regression indicates an unrelated frozen-stage defect.
7. the proposed methodology would depend on current database insertion order.
8. conflicting duplicates cannot be deterministically quarantined.

If a stop condition occurs:

* do not implement a partial workaround;
* report the exact unresolved decision;
* classify it;
* STOP.

---

# 15. REQUIRED REPORT

Append:

`REPORT — Stage 6 Prompt 25`

Include:

### A. Methodology authority

Explicit final rules for:

* B5;
* B6;
* B9;
* ZERO_ACTUAL_UNRESOLVED.

### B. Rationale

Explain why each rule is:

* deterministic;
* auditable;
* PIT-safe;
* financially defensible.

### C. Implementation

List exact files and symbols changed.

### D. Production path

Show how the new rules flow through:

```text
Actual
→ ReportVersion
→ eligibility
→ duplicate identity
→ Error
→ MAPE/Bias
→ sufficiency
```

### E. Testing

Report all six layers.

Include:

* focused test count/result;
* full regression result.

### F. Remaining blockers

Explicitly confirm that:

* B1 remains unresolved;
* B2 remains unresolved;
* B3 remains unresolved;
* B4 remains unresolved;
* B7 remains unresolved;
* B8 remains unresolved.

### G. Freeze status

Do NOT freeze Stage 6.

The only acceptable final status is:

`Stage 6 is NOT declared frozen.`

---

# 16. FINAL STOP

After completing this prompt:

STOP.

Do not proceed to B1/B2/B3/B4/B7/B8.

Do not design Reliability.

Do not design Calibration.

Do not design Seasonal Naive.

Do not freeze Stage 6.

Do not commit or push.
======================================================================

stage 6 Prompt 6 - Independent Post 25 Methodology and Behavioral Audit.

You are the primary engineering agent for the repository:

`analyzer`

This is a financial-data application. Financial correctness, auditability, point-in-time correctness, deterministic behavior, and preservation of explicit financial invariants take priority over implementation speed.

# Stage 6 Prompt 26 — Independent Post-P25 Methodology and Behavioral Audit

## 1. Objective

Perform an **independent, read-only audit** of the Prompt 25 implementation.

Prompt 25 changed Actual selection, ReportVersion handling, data-quality eligibility, duplicate identity, scenario identity, and zero-Actual handling. These changes affect the foundation of every downstream Stage 6 result.

Your task is to determine whether each change is:

* explicitly authorized by the locked Stage 6 specification;
* consistent with the intended financial meaning of forecast evaluation;
* deterministic and auditable;
* behaviorally proven through the required testing layers;
* safe for downstream metrics, baseline comparison, Reliability, and Calibration governance.

**Do not implement fixes. Do not declare Stage 6 frozen.** If an issue is found, document the precise evidence and stop at the audit result.

## 2. Mandatory execution firewall

* Work only in the existing local working tree.
* Do not use GitHub, GitHub CLI/API, network access, fetch, pull, push, remotes, commits, branches, or Git history.
* Do not perform a repository-wide audit.
* Do not inspect unrelated stages or files.
* Do not modify source files, tests, specifications, or configuration.
* Do not run formatters or auto-fix tools.
* Do not treat a passing test, current implementation, existing constant, or prior report as proof of methodological authority.
* Do not infer approval from the fact that Prompt 25 implemented a rule.
* If evidence needed to authorize a decision is absent, classify it as an unresolved methodology-authority issue rather than inventing a rule.

## 3. Strict inspection scope

Read only the following:

1. `PROJECT_HANDOFF_INSTRUCTIONS.md`
2. `06_Stage6_Forecast_Evaluation.md`
3. The reports for Stage 6 Prompts 17–25 in `temp_report.md`
4. Current Stage 6 files directly responsible for:

   * Actual selection and ReportVersion validation;
   * observation construction and identity;
   * data-quality eligibility;
   * duplicate detection;
   * zero/sign-regime classification;
   * aggregation and production pipeline;
   * corresponding Stage 6 tests.

Inspect directly referenced dependencies only when necessary to establish a specific claim. Do not expand the scope to Stage 1–5 or Stage 7 implementations. For boundary checks, use targeted evidence and existing tests.

## 4. Audit A — Actual selection and ReportVersion policy (B5)

Prompt 25 introduced:

* `ACTUAL_SELECTION_POLICY = "FIRST_KNOWN_OUTCOME_P25"`
* selection order `(publication_datetime, report_version_number, report_version_id)`
* earliest-published valid ReportVersion selection;
* later-published restatements losing to earlier-published versions.

Independently verify:

1. What the locked Stage 6 specification explicitly requires about the Actual outcome and ReportVersion.
2. Whether the specification authorizes selecting the earliest-published version as the definitive evaluation outcome.
3. Whether the intended evaluation target is:

   * the first known published outcome;
   * the latest eligible/restated outcome;
   * or another explicitly authorized outcome.
4. Whether the selected policy distinguishes these possible evaluation objectives instead of silently treating them as equivalent.
5. Whether tie-breaks by version number and identifier have semantic authority, or merely provide deterministic ordering without proving that the selected outcome is financially correct.
6. Whether missing, malformed, conflicting, or otherwise invalid ReportVersion metadata fails closed.
7. Whether list order, database order, surrogate identifiers, or caller order can change the result.
8. Whether the selected Actual and its complete ReportVersion/publication metadata remain traceable in the final observation and audit chain.

Do not assume that “first published” or “latest restated” is universally correct. Determine whether the locked specification actually authorizes the implemented policy.

**If the intended Actual-outcome policy is not authorized, classify B5 as `UNRESOLVED METHODOLOGY AUTHORITY` or `BLOCKER`. Do not select a replacement policy.**

## 5. Audit B — Data-quality eligibility (B6)

Prompt 25 introduced these participation rules:

* Participating: `VALID`, `ESTIMATED`, `RESTATED`
* Quarantined: `MISSING`, `SUSPICIOUS`, `UNMAPPED`

It also introduced `is_scoring_eligible(actual)` and the `limited_quality` indicator.

Independently verify:

1. Whether the locked Stage 6 specification authorizes each state to participate or be excluded.
2. Whether a precedent elsewhere in the application is being mistaken for explicit Stage 6 authority.
3. Whether `ESTIMATED` and `RESTATED` observations can affect Error, MAPE, Bias, observation sufficiency, and baseline comparison.
4. Whether `limited_quality` is consistently propagated and cannot be mistaken for a fully validated observation.
5. Whether the same quality-state policy is applied consistently in every authorized aggregation path.
6. Whether missing, suspicious, and unmapped observations are excluded from scoring and sufficiency without being silently converted to zero.
7. Whether quarantine reasons and original data-quality states remain auditable.
8. Whether invalid ReportVersion handling takes precedence over any scoring eligibility decision that could otherwise admit the observation.
9. Whether any quality-state combination creates contradictory or ambiguous outcomes.

Passing tests prove implemented behavior, not authority. If the specification does not authorize a consequential participation decision, report the gap instead of inventing a rule.

## 6. Audit C — Observation identity, scenario, and duplicates (B9)

Prompt 25 added `scenario` to `EvaluationKey`, making the observation key a seven-part identity while leaving `SeriesKey` unchanged.

Independently verify:

1. The locked specification’s required evaluation identity and aggregation identity.
2. Whether scenario is explicitly required or otherwise justified as part of observation identity.
3. Whether scenario-distinct observations are legitimate distinct observations or could represent multiple alternative outcomes for one forecast that must not be counted together.
4. Whether placing multiple scenarios into one shared series can inflate observation counts, alter sufficiency bands, or affect MAPE/Bias and baseline comparisons.
5. Whether the one-Reliability-per-series interpretation is explicitly authorized and behaviorally consistent with the scenario structure.
6. Whether true duplicates are quarantined wholesale, without averaging, silent overwriting, or arbitrary winner selection.
7. Whether conflicts in Forecast value, Actual identity, ReportVersion, cutoff, or scenario are detected and handled safely.
8. Whether `forecast_id` and other surrogate identifiers can accidentally prevent detection of logical duplicates.
9. Whether TTM and same-period collisions remain protected against double counting.
10. Whether horizon and model-version isolation remain intact.

Do not change the locked specification or invent a new identity model. Report any unresolved identity or aggregation semantics precisely.

## 7. Audit D — Actual = 0 and sign regimes

Prompt 25 removed `ZERO_ACTUAL_UNRESOLVED` and allows numeric zero Actual values to enter ordinary scoring when the Forecast denominator is valid and no sign-change regime applies.

Independently verify the locked formulas:

* `Error = Actual - Forecast`
* `Percentage Error = (Actual - Forecast) / abs(Forecast) × 100`
* `APE = abs(Actual - Forecast) / abs(Forecast) × 100`
* `MAPE = mean(valid APEs)`
* `Bias = mean(valid signed percentage errors)`

Check at least these cases through the actual production path:

1. Forecast positive, Actual zero.
2. Forecast negative, Actual zero.
3. Forecast zero, Actual zero.
4. Forecast zero, Actual nonzero.
5. Loss-to-profit transition.
6. Profit-to-loss transition.
7. Other sign-change conditions covered by the specification.
8. Actual missing (`None`) versus Actual numerically equal to zero.
9. Mixed eligible and ineligible observations in one series.

Verify that:

* Absolute Error is retained where the specification allows it.
* Percentage metrics are unavailable where the denominator or regime makes them invalid.
* A zero Actual is not automatically misclassified as `ZERO_BASE`.
* A missing Actual is never converted to zero.
* Invalid percentage metrics do not silently enter MAPE or Bias.
* Observation sufficiency uses only the authorized valid-observation count.
* No metric-specific exception is introduced without authority.

Do not merely repeat Prompt 25’s test results. Inspect the current behavior and the relevant assertions independently.

## 8. Audit E — Cross-layer consistency

Trace the actual production path:

`Actual candidates → ReportVersion validation/selection → observation construction → eligibility → duplicate handling → Error and percentage metrics → sufficiency → baseline comparison → Reliability/Calibration governance`

For each transition, determine whether the upstream status and identity survive correctly downstream.

Specifically verify:

* No quarantined observation can affect MAPE, Bias, or sufficiency.
* `NULL != 0` remains true in all relevant paths.
* No unresolved Reliability mapping is bypassed.
* Reliability remains unavailable while its methodology blockers remain unresolved.
* Calibration cannot transition to an authorized/calibrated state through a legacy or alternate path.
* No unsupported Seasonal Naive result is produced.
* Baseline inputs cannot introduce future information.
* Forecast horizons and model versions are not mixed.
* TTM is not double-counted.
* Stage 5 forecast records are not modified.
* Reliability does not numerically alter Forward P/E.
* No Stage 4, Stage 5, or Stage 7 source changes are present from this work. Do not inspect those stages broadly; use the narrowest evidence available.

## 9. Mandatory six-layer audit

Apply all six layers to each critical Prompt 25 invariant:

1. **Layer 1 — Unit / Formula:** exact selection ordering, formulas, regime behavior, null handling, and state predicates.
2. **Layer 2 — Contract / Boundary:** identity, ReportVersion validity, metadata preservation, quality-state contracts, and invalid-input behavior.
3. **Layer 3 — Production-Path / Integration:** exercise the public Stage 6 evaluation path, not only internal helpers.
4. **Layer 4 — Adversarial / Negative:** reversed candidate order, tied publication times, malformed metadata, conflicting duplicates, mixed quality states, zero/sign edge cases, and scenario-count contamination.
5. **Layer 5 — Regression:** run the relevant focused Stage 6 tests, then the full regression suite if the local environment permits.
6. **Layer 6 — Independent Audit:** independently trace source behavior against the locked specification and confirm that tests genuinely exercise the claimed invariants.

Do not change tests. Record the exact commands and results. If a required test cannot be run, state that limitation explicitly.

A test is not proof of methodology authority. For every critical rule, distinguish:

* `BEHAVIORALLY PROVEN`
* `STRUCTURALLY VERIFIED`
* `SPECIFICATION-AUTHORIZED`
* `UNRESOLVED METHODOLOGY AUTHORITY`
* `BLOCKER`

Do not use one classification as a substitute for another.

## 10. Explicitly unresolved areas — do not implement or resolve

The following previously reported methodology blockers remain outside this prompt:

* **B1:** Seasonal Naive construction and seasonal-period authority.
* **B2:** MAPE-to-Accuracy, Bias-to-Bias-Control, and Baseline-Advantage score mappings.
* **B3:** persistence definition.
* **B4:** Calibration transition methodology.
* **B7:** unavailable-component handling in Reliability.
* **B8:** persistent baseline-underperformance flag methodology.

Do not add formulas, thresholds, fallback values, seasonal periods, Reliability scores, calibration transitions, or persistence criteria for these items.

Reliability must remain withheld while its required methodology is unresolved. Calibration must remain fail-closed.

## 11. Reporting requirements

Append a section to `temp_report.md` titled:

`REPORT — Stage 6 Prompt 26`

Include:

1. Exact files and symbols inspected.
2. Audit evidence for B5, B6, B9, and zero-Actual behavior.
3. For every consequential rule, separate:

   * specification authority;
   * observed implementation behavior;
   * behavioral test evidence;
   * unresolved ambiguity.
4. Results of the six testing layers.
5. Exact focused and full-suite commands and counts.
6. Any mismatch between the Prompt 25 report and the current source/tests.
7. Any defect, authority gap, or possible financial-semantic problem.
8. Whether each finding is an implementation defect, a specification-authority gap, a test-coverage gap, or a combination.
9. A concise list of the next blockers in priority order.

Do not report a rule as specification-authorized merely because it is documented in a Prompt 25 report or implemented in source code.

## 12. Stop conditions and final classification

This is an audit-only prompt. Do not remediate anything.

If the audit finds an implementation defect, specification conflict, material identity ambiguity, potential scenario-count contamination, or unauthorized financial methodology, document the evidence and stop.

Use exactly one final classification:

* `PASS — P25 IMPLEMENTATION AND AUTHORITY VERIFIED`
* `FAIL — REMEDIATION REQUIRED`
* `BLOCKED — METHODOLOGY AUTHORITY UNRESOLVED`

A PASS is permitted only if the implementation is independently verified **and** each consequential Prompt 25 decision has adequate specification authority. Passing tests alone is insufficient.

Regardless of classification:

`Stage 6 is NOT declared frozen.`

Stop after writing the report and providing a concise summary. Do not propose or implement fixes within this prompt.
====================================================================

stage 6 Prompt 27 - Methodology Decision Package for P25 Blocker

You are the primary engineering agent for the repository:

`analyzer`

This is a financial-data application. Financial correctness, auditability, point-in-time correctness, determinism, and explicit methodology authority take priority over implementation speed.

# Stage 6 Prompt 27 — Methodology Decision Package for P25 Blockers

## 1. Objective

Prepare a rigorous, evidence-based methodology decision package for the unresolved issues identified by the independent Prompt 26 audit.

This is a **read-only analysis and proposal task**. It is not an implementation task and does not authorize any methodology change.

The objective is to help the project owner make explicit, informed decisions about:

* B5 — Actual outcome and ReportVersion selection;
* B6 — Stage 6 data-quality-state participation;
* B9 — Scenario identity, observation counting, and aggregation;
* ZERO_ACTUAL — Actual equal to zero and percentage-metric eligibility.

For each issue, explain the available choices, financial/statistical implications, failure modes, interactions with other Stage 6 rules, and exact proposed specification amendments.

Do not choose a policy merely because it matches the current implementation. Do not silently resolve ambiguities.

## 2. Mandatory execution firewall

* Work only in the local working tree.
* No GitHub, GitHub CLI/API, network access, fetch, pull, push, remotes, commits, branches, or Git history.
* No repository-wide exploration.
* Do not modify source code, tests, the locked specification, configuration, or any other existing file.
* Do not run formatters or auto-fix tools.
* Do not implement, authorize, or activate a proposed policy.
* Do not treat a passing test, existing implementation, precedent from another stage, or prior report as methodology authority.
* Do not declare Stage 6 frozen.
* If the evidence does not establish a defensible answer, state exactly what remains unknown and what decision is required from the project owner.

## 3. Strict inspection scope

Read only:

1. `PROJECT_HANDOFF_INSTRUCTIONS.md`
2. `06_Stage6_Forecast_Evaluation.md`
3. The Stage 6 Prompt 17–26 reports in `temp_report.md`
4. The current Stage 6 implementation and tests directly related to B5, B6, B9, and ZERO_ACTUAL.

Inspect directly referenced dependencies only when necessary to support a specific claim.

Do not inspect unrelated stages. Do not expand the task into B1, B2, B3, B4, B7, or B8.

## 4. Decision package A — B5: Actual outcome and ReportVersion selection

The Prompt 26 audit found that the locked specification requires a valid ReportVersion and known publication date but does not explicitly authorize either earliest-published or latest/restated Actual selection.

Analyze the following possible policies without implementing any of them:

**Option A — First-known outcome**

Select the earliest eligible published Actual and preserve that outcome as the evaluation target.

**Option B — Latest eligible restated outcome**

Select the latest eligible published Actual under an explicit, deterministic ReportVersion policy.

**Option C — Separate evaluation objectives**

Keep first-known outcome and latest-restated outcome as distinct evaluation targets, with explicit labels and non-mixing rules.

If another policy is more defensible, present it as an additional option and explain why.

For every option, analyze:

1. What forecasting question it answers.
2. Whether it measures performance against information first available to users or against a subsequently revised financial outcome.
3. How restatements affect forecast error, MAPE, Bias, model comparison, and historical comparability.
4. How it interacts with Point-in-Time correctness without incorrectly excluding later-published Actual outcomes.
5. How ReportVersion ties, missing version numbers, conflicting metadata, and invalid publication timestamps should be handled.
6. Whether the policy supports reproducible historical evaluations when new ReportVersions arrive.
7. What information must be retained to reconstruct the exact evaluation outcome.
8. What tests would distinguish the options behaviorally.

Do not claim that either first-known or latest-restated is universally correct.

End this section with:

* a recommendation, if the evidence supports one;
* the reasons and trade-offs;
* the exact unresolved decision that requires owner approval.

## 5. Decision package B — B6: Data-quality-state participation

Prompt 25 implemented:

* Participating: `VALID`, `ESTIMATED`, `RESTATED`
* Quarantined: `MISSING`, `SUSPICIOUS`, `UNMAPPED`

The Prompt 26 audit found that the locked Stage 6 specification does not explicitly authorize this complete policy.

Analyze each state individually:

* `VALID`
* `ESTIMATED`
* `MISSING`
* `SUSPICIOUS`
* `UNMAPPED`
* `RESTATED`

For every state, provide a decision matrix covering:

1. Eligibility to serve as the selected Actual.
2. Eligibility for absolute Error.
3. Eligibility for Percentage Error and APE.
4. Eligibility for MAPE and Bias.
5. Contribution to observation sufficiency.
6. Eligibility for baseline comparison.
7. Required audit metadata and quality flags.
8. Expected behavior when the state changes after a later ReportVersion becomes available.

Distinguish carefully between:

* an Actual that can be retained as evidence;
* an Actual that can be selected as the evaluation outcome;
* an observation whose absolute error can be calculated;
* an observation eligible for percentage metrics;
* an observation eligible to count toward sufficiency and downstream evaluation.

Do not assume that all these permissions must be identical.

Do not borrow Stage 3 scoring rules as Stage 6 authority without explicit evidence that the rules are applicable.

Provide plausible policy alternatives for `ESTIMATED` and `RESTATED`, including the impact of including them with a quality flag versus excluding them from primary scoring.

If quality states cannot be resolved without an authoritative Data Foundation rule, state that limitation explicitly.

## 6. Decision package C — B9: Scenario identity and observation counting

Prompt 25 added `scenario` to the observation key but kept the aggregation series keyed by Company, Metric, Horizon, and Model Version.

The Prompt 26 audit identified a material risk: multiple scenarios may enter one shared series, inflate its observation count, and influence MAPE, Bias, and confidence bands.

Analyze at least these alternatives:

**Option A — Scenario-separated evaluation series**

Aggregate and evaluate each scenario independently. Explain how Reliability should be represented if the locked specification expects one Reliability value alongside multiple scenarios.

**Option B — Scenario-aware observation identity with controlled series aggregation**

Retain scenario as observation identity but define an explicit rule preventing scenario alternatives for the same underlying forecast target from inflating independent observation counts or being treated as independent evidence.

**Option C — One designated evaluation scenario**

Specify which scenario, if any, is eligible for primary historical evaluation and how other scenarios are retained without contaminating primary performance statistics.

If none is defensible from the existing specification, present the unresolved choice rather than inventing a policy.

For each alternative, analyze:

1. Observation identity and duplicate detection.
2. Whether Bear/Base/Bull outcomes represent independent observations or alternative outcomes for the same target.
3. Observation-count inflation and its effect on `<5`, `5–7`, `8–11`, and `≥12` sufficiency bands.
4. MAPE and Bias aggregation.
5. Baseline identity and comparability.
6. Model-version and horizon isolation.
7. TTM double-counting risks.
8. The relationship between per-scenario evaluation and Reliability.
9. Auditability and reconstruction of results.

Use a small, explicitly illustrative example to demonstrate how one underlying forecast target with three scenario forecasts could affect observation count and sufficiency under different policies. Label all example values as illustrative; do not present them as project data or methodology constants.

Conclude with a recommended policy only if supported by the specification and defensible reasoning. Identify the exact specification sections that must be amended.

## 7. Decision package D — Actual equal to zero

Prompt 25 allows `Actual = 0` to score when `Forecast != 0`, while retaining zero-denominator and sign-change exclusions.

The locked specification explicitly discusses `Forecast = 0` and sign-change regimes, but does not clearly state the treatment of every `Actual = 0` case.

Analyze these cases independently:

1. `Forecast > 0`, `Actual = 0`.
2. `Forecast < 0`, `Actual = 0`.
3. `Forecast = 0`, `Actual = 0`.
4. `Forecast = 0`, `Actual != 0`.
5. Positive Forecast with negative Actual.
6. Negative Forecast with positive Actual.
7. Missing Actual (`None`).
8. Actual zero with a non-`VALID` data-quality state.

For each case, distinguish:

* absolute Error validity;
* Percentage Error validity;
* APE validity;
* MAPE eligibility;
* Bias eligibility;
* regime classification;
* observation-count eligibility.

Explain why mathematical computability alone does not necessarily establish statistical comparability or methodology authorization.

Pay particular attention to the negative-Forecast/zero-Actual boundary: do not silently assume it is equivalent to every other zero-Actual case.

Recommend an explicit policy matrix and exact specification text. If a choice depends on the intended financial interpretation of a metric, identify the required owner decision.

## 8. Cross-policy consistency

Analyze the interactions among B5, B6, B9, and ZERO_ACTUAL.

The package must explicitly consider:

* whether a ReportVersion-selection policy changes which quality state is evaluated;
* whether a restatement can change the selected Actual and thereby change zero/sign classification;
* whether multiple scenarios can inflate sufficiency even if each observation individually passes eligibility;
* whether zero-Actual observations can alter MAPE, Bias, baseline comparison, or confidence bands;
* whether excluded observations remain auditable without entering scoring;
* whether any proposed rule changes the meaning of existing Stage 6 output fields;
* whether all decisions remain deterministic and reproducible.

Do not finalize each policy in isolation if their interaction creates an inconsistency.

## 9. Proposed specification amendments

For each issue, provide proposed replacement or insertion text for `06_Stage6_Forecast_Evaluation.md`.

Requirements:

* Use precise, normative language suitable for a locked technical specification.
* Identify the exact existing section where the amendment would belong.
* Separate unconditional invariants from owner decisions that remain open.
* Do not edit the actual specification file.
* Do not present a proposed amendment as already approved.
* If multiple options remain viable, provide separate alternative text blocks instead of combining incompatible rules.

Include a concise decision table:

| Decision ID | Issue | Recommended option | Evidence | Main trade-off | Owner approval required? |
| ----------- | ----- | ------------------ | -------- | -------------- | ------------------------ |

If the recommendation is uncertain, use `NO RECOMMENDATION — OWNER DECISION REQUIRED`.

## 10. Validation and evidence standard

This prompt does not authorize code changes. Do not create tests or modify existing tests.

Nevertheless, specify the future six-layer validation plan for each proposed policy:

1. Unit/formula tests.
2. Contract/boundary tests.
3. Production-path/integration tests.
4. Adversarial/negative tests.
5. Regression tests.
6. Independent audit.

Every proposed policy must have at least one concrete test that would fail under a plausible competing policy. Avoid tests that merely reproduce the current implementation.

Passing tests must never be presented as proof of methodology authority.

## 11. Required output and report

Append a new section to `temp_report.md`:

`REPORT — Stage 6 Prompt 27`

Include:

1. Exact files inspected.
2. Separate analyses for B5, B6, B9, and ZERO_ACTUAL.
3. Alternative policies and their trade-offs.
4. Cross-policy consistency analysis.
5. Proposed specification amendments, clearly marked **PROPOSED — NOT APPROVED**.
6. The decision table.
7. Future six-layer validation plans.
8. Explicit unresolved questions requiring owner approval.
9. A concise priority order for the next implementation steps after decisions are approved.
10. A statement confirming that no source, test, specification, or configuration files were modified.

Do not append proposed policies to the locked specification itself. The report is the only file you may modify.

## 12. Stop conditions

Stop without implementation if:

* the available evidence does not support a definitive policy;
* two or more alternatives remain materially defensible;
* a proposed decision conflicts with the locked specification;
* the financial meaning of a metric cannot be established from available authoritative material.

Do not resolve B1, B2, B3, B4, B7, or B8 in this prompt.

Final status must explicitly state:

`Stage 6 is NOT declared frozen.`

Stop after appending the report and providing a concise summary of the decisions that require owner approval.
============================================================
Stage 6 Prompt 28 - Targeted Authority Trace for Unresolved Methodology Decisions

# Stage 6 Prompt 28 — Targeted Authority Trace for Unresolved Methodology Decisions

You are working locally in the `analyzer` repository, a financial-data application.

## Objective

Perform a narrow, read-only authority trace for the unresolved Stage 6 methodology decisions identified in `REPORT — Stage 6 Prompt 27`.

Determine whether existing authoritative project documents explicitly resolve any of these questions:

* **B5:** Actual selection across multiple ReportVersions, including restatements.
* **B6:** Stage 6 participation rules for VALID, ESTIMATED, RESTATED, MISSING, SUSPICIOUS, and UNMAPPED data-quality states.
* **B9:** Whether scenario forecasts are separate evaluation series, pooled with an authorized anti-inflation rule, or evaluated using a designated scenario.
* **ZERO_ACTUAL:** The statistical treatment of Actual = 0, including Forecast < 0 / Actual = 0.
* **Q7:** Whether observations excluded from MAPE contribute to the minimum-observation sufficiency threshold.
* **Q8:** Whether previously published evaluation results remain frozen after restatement or must be recalculated.

This is an authority-discovery task, not a design or implementation task.

## 1. Scope restrictions

Read `PROJECT_HANDOFF_INSTRUCTIONS.md`, `06_Stage6_Forecast_Evaluation.md`, and the Prompt 27 report in `temp_report.md` only as needed to establish the unresolved questions and the project's authority rules.

Then inspect only specifically relevant Data Foundation documentation, data-quality specifications, ReportVersion/financial-fact contracts, or existing methodology decision records that can plausibly govern these questions.

Do not conduct a repository-wide audit. Do not enumerate unrelated files. Do not inspect or modify Stage 1–5 implementation unless a specific authoritative document directly requires it; frozen stages must remain untouched.

Do not treat the following as methodology authority by themselves:

* Existing implementation behavior.
* Passing tests.
* Comments or docstrings that merely describe implementation.
* Stage 3 scoring conventions.
* A previous prompt's proposed option.
* A database ordering or surrogate-ID convention.

A source is authoritative only if its role and wording support the particular rule being claimed.

## 2. Required analysis

For each unresolved decision, report:

1. The exact source file and section, heading, or line range.
2. The relevant rule, accurately summarized.
3. Whether the rule is explicit, implicit, ambiguous, or absent.
4. Whether it resolves the decision fully, partially, or not at all.
5. Any conflict with the locked Stage 6 specification.
6. Whether an owner decision is still required.

Distinguish carefully between:

* Data-quality classification and permission to use a value as an evaluation outcome.
* A ReportVersion being valid and the policy for choosing between valid versions.
* Actual-value provenance and the definition of an evaluation observation.
* Arithmetic computability and authorization to include a result in MAPE, Bias, or sufficiency counts.
* Reproducibility requirements and substantive statistical policy.

Do not infer that a general data-quality rule automatically authorizes Stage 6 scoring.

## 3. Decision classification

Classify each question into one of these outcomes:

* `RESOLVED_BY_EXISTING_AUTHORITY`
* `PARTIALLY_RESOLVED`
* `OWNER_DECISION_REQUIRED`
* `CONFLICTING_AUTHORITY_FOUND`

For each outcome, explain the evidence and the precise boundary of the conclusion.

If no authoritative rule exists, say so explicitly. Do not fill the gap with a recommendation disguised as an existing rule.

Do not select between competing B5, B6, B9, ZERO_ACTUAL, Q7, or Q8 alternatives on the owner's behalf.

## 4. Deliverable

Append exactly one new section to `temp_report.md`:

`REPORT — Stage 6 Prompt 28: Targeted Authority Trace`

The report must include:

* Exact files and sections inspected.
* A decision-by-decision authority matrix.
* Supporting evidence and any conflicts.
* A final list of unresolved owner decisions.
* The smallest defensible next step based on the findings.

Modify no other files.

## 5. Prohibitions

* No source-code, test, specification, configuration, migration, or schema changes.
* No test execution is required for this read-only task.
* No GitHub, GitHub CLI/API, remote operations, commits, pushes, pulls, or branch changes.
* No Stage 6 freeze declaration.
* Do not resolve unrelated blockers B1, B2, B3, B4, B7, or B8.

If the evidence does not resolve a decision, stop at that conclusion rather than expanding the investigation indefinitely.

## 6. Final response

Summarize the decisions resolved by existing authority, the decisions still requiring owner approval, the exact file changed, and confirmation that no implementation or tests were changed or run.

`Stage 6 remains NOT FROZEN.`
================================================================
# Stage 6 Prompt 29 — Owner Decision Gate and Approval Record

You are working locally in the `lovelyroz/analyzer` repository, a financial-data application.

## Objective

Prepare a concise, auditable owner-decision record for the unresolved Stage 6 methodology questions identified in:

* `REPORT — Stage 6 Prompt 27`
* `REPORT — Stage 6 Prompt 28`

The authority trace is complete enough to establish which rules exist and which decisions remain unresolved. Do not repeat repository-wide discovery or attempt to resolve policy questions through implementation.

This prompt is a decision-preparation task only. It does not authorize any methodology choice, specification amendment, or code change.

## 1. Scope

Inspect only:

* `PROJECT_HANDOFF_INSTRUCTIONS.md`
* `06_Stage6_Forecast_Evaluation.md`, limited to the relevant sections already identified in Prompt 28
* The Prompt 27 and Prompt 28 reports in `temp_report.md`

Do not reopen the authority search unless a specific contradiction between those reports makes it strictly necessary.

## 2. Produce an owner decision record

Append exactly one section to `temp_report.md`:

`REPORT — Stage 6 Prompt 29: Owner Decision Gate`

The section must contain the following decision groups.

### D1 — Actual selection and restatements (B5 + Q8)

Present the mutually distinct options:

* First-known outcome for historical forecast evaluation.
* Latest-restated outcome.
* Two separately versioned objectives: first-known accuracy and latest-restated evaluation.

Explain that the existing authority supports preserving historical point-in-time states and prohibits silently rewriting history, but does not fully define the selection policy or republication convention.

For each option, identify:

* What question it answers.
* The treatment of later restatements.
* Whether a new version-pinned evaluation artifact is needed.
* The required audit trail.
* Any unresolved specification change.

Do not select an option.

### D2 — Data-quality participation (B6)

Separate the decisions for:

* `SUSPICIOUS` and `UNMAPPED`: proposed confirmation of quarantine from scoring, consistent with the existing Data Foundation boundary.
* `ESTIMATED`: score normally, score with mandatory quality flags and sensitivity analysis, or exclude from primary scoring.
* `RESTATED`: define its participation and provenance jointly with D1.

Do not treat Data Foundation classification as automatic authorization to score a value.

Do not select an option.

### D3 — Scenario evaluation (B9)

Present:

* A: separate Bear/Base/Bull evaluation series.
* B: shared reporting with a formally defined event-level anti-inflation and aggregation rule.
* C: score one designated scenario and retain the others as descriptive outputs.

For each option, identify consequences for sample sufficiency, MAPE, Bias, baseline comparison, Reliability, and auditability.

Do not select an option or invent aggregation weights.

### D4 — Actual-zero policy

Present the alternatives:

* Exclude Actual-zero observations from MAPE, with a distinct reason code and auditable absolute error.
* Evaluate them in a separate zero-Actual metric that is never pooled with ordinary MAPE.

In either case, explicitly require owner-approved rules for:

* Forecast > 0 and Actual = 0.
* Forecast < 0 and Actual = 0.
* Forecast = 0 and Actual = 0.
* Forecast = 0 and Actual ≠ 0.
* Missing Actual versus numerical zero.
* Sign-change cases and whether MAPE-null observations count toward sufficiency.

Do not assume arithmetic computability establishes statistical validity.

Do not select an option.

### D5 — Sufficiency rule (Q7)

Present the alternatives:

* Count only observations eligible for the relevant MAPE metric.
* Count all otherwise valid, nonduplicate forecast outcomes, while reporting the effective MAPE sample size separately.

Explain that this choice must be consistent with the scenario policy and zero-Actual policy.

Do not select an option.

## 3. Cross-decision dependencies

Explicitly identify these dependencies:

* D1 and D2 are coupled through the selection and provenance of RESTATED observations.
* D3 determines the identity and denominator of evaluation series and therefore affects D5.
* D4 affects MAPE, Bias interpretation, baseline comparison, and D5.
* D1 must preserve historical artifacts and specify how any later evaluation version is identified and audited.
* Reliability remains withheld until its authorized mappings and calculation method are resolved.
* B1, B2, B3, B4, B7, and B8 remain outside this task and unresolved unless prior evidence explicitly proves otherwise.

## 4. Approval protocol

For each decision, provide:

* Decision ID.
* Available options.
* Existing authoritative constraints.
* Consequences of each option.
* Required owner approval.
* A blank `OWNER DECISION: NOT YET APPROVED` field.

Clearly distinguish:

* Existing binding constraints.
* Proposed options.
* Decisions requiring explicit owner approval.

Do not interpret silence, existing code, test results, or an earlier proposal as approval.

Do not use a recommendation as a substitute for approval.

## 5. Restrictions

* Read-only with respect to source code, tests, locked specifications, schemas, migrations, and configuration.
* Append only the required report section to `temp_report.md`.
* Do not execute tests.
* Do not implement any option.
* Do not declare Stage 6 frozen.
* No GitHub, GitHub CLI/API, remote operations, commits, pushes, pulls, or branch changes.
* Do not expand into a repository-wide audit.

## 6. Final response

Summarize the decision groups prepared, confirm that no owner decision was silently selected, state the exact file modified, and confirm that no source code or tests were changed or run.

`Stage 6 remains NOT FROZEN.`
=====================================================================

# Stage 6 Prompt 30 — Apply Approved Methodology Decisions to the Locked Specification

You are the primary engineering agent for `analyzer`, a financial-data application where financial correctness, point-in-time integrity, deterministic behavior, auditability, and preservation of historical evaluation artifacts take priority over implementation speed.

## 1. Approved authority

The project owner has explicitly approved the five methodology policies proposed in Stage 6 Prompt 29:

* D1: first-known, point-in-time Actual selection; later restatements must not silently rewrite historical evaluation results.
* D2: quarantine `SUSPICIOUS` and `UNMAPPED`; allow `ESTIMATED` observations only with explicit quality flags and mandatory sensitivity analysis; handle `RESTATED` consistently with D1.
* D3: maintain separate evaluation series for Bear, Base, and Bull scenarios.
* D4: Actual-zero observations must not enter ordinary MAPE; retain absolute error and an explicit exclusion reason. Specify the treatment of the relevant forecast/actual zero combinations without conflating numerical zero with missing data.
* D5: count otherwise valid, nonduplicate forecast outcomes for general sufficiency, and report the effective MAPE-eligible sample size separately.

These are owner-approved policy decisions. They supersede the previously unapproved alternatives in Prompts 27–29. Do not ask the owner to approve these five decisions again.

However, approval of these high-level policies does not authorize inventing missing technical rules. Explicitly distinguish approved policy from technical details that still lack authority.

## 2. Strict scope

Inspect only:

1. `PROJECT_HANDOFF_INSTRUCTIONS.md` for operational constraints.
2. `06_Stage6_Forecast_Evaluation.md`, limited to the sections governing:

   * Actual selection and point-in-time requirements;
   * error, percentage error, APE, MAPE, and Bias;
   * evaluation series identity and sufficiency;
   * baseline comparison and Reliability;
   * data-quality states and auditability;
   * historical immutability and version-pinned evaluation artifacts.
3. The existing `temp_report.md` sections for Stage 6 Prompts 27, 28, and 29.

Do not perform a repository-wide search or inspect unrelated stages or modules. Use only the evidence in these bounded sources.

## 3. Required task

Amend `06_Stage6_Forecast_Evaluation.md` so the five approved policies become explicit, internally consistent normative requirements.

Preserve the document's existing structure and terminology where possible. Make the smallest defensible edits. Do not rewrite unrelated sections.

### D1 — First-known Actual and historical immutability

Specify that:

* Historical evaluation uses the earliest eligible, valid, known-publication-date Actual report version under the approved first-known policy.
* A later restatement must not silently replace the Actual or overwrite a previously published evaluation artifact.
* Every selected Actual must be traceable to its exact `actual_report_version`, publication timestamp, and selection-policy version.
* Candidate versions that are ineligible, invalid, missing required publication timestamps, or otherwise quarantined must remain auditable with reason codes.
* If multiple eligible candidates share the earliest publication timestamp and the authoritative sources provide no defensible ordering, do not resolve the tie using arbitrary database IDs or an unapproved tie-break. Mark the selection ambiguous and fail closed for that evaluation observation.
* Any authorized rerun must be an explicitly identified, version-pinned evaluation artifact with lineage; it must not mutate historical artifacts in place.

Do not imply that first-known means “latest database row” or “highest version number.”

### D2 — Actual data quality

Specify that:

* `SUSPICIOUS` and `UNMAPPED` Actuals are excluded from Actual selection and all scored evaluation paths, including error metrics, baseline comparison, and sufficiency counts. Preserve an auditable exclusion record.
* `ESTIMATED` Actuals may participate only with explicit quality/provenance flags and a mandatory sensitivity analysis that recomputes the relevant outputs excluding `ESTIMATED` observations.
* The primary and sensitivity results must remain distinguishable; never silently mix or relabel them.
* `RESTATED` handling must follow D1. A later restatement must not displace the selected first-known Actual in the primary historical evaluation.
* Missing, invalid, suspicious, unmapped, and estimated states must never be silently converted to zero.
* Apply quality eligibility before selecting among Actual candidates.

Do not introduce a new quality state or override Stage 1's data-quality definitions.

### D3 — Scenario-separated series

Specify that Bear, Base, and Bull are distinct evaluation series.

* Scenario identity must be represented in the evaluation series key and retained in audit/output records.
* Do not pool scenario observations into one MAPE, Bias, sufficiency count, baseline comparison, or Reliability result.
* Do not count the three scenarios for one forecast event as three independent observations in a shared series.
* Apply minimum-observation rules independently to each scenario-specific series.
* If the existing schema or output contract cannot preserve scenario identity, document the exact blocker. Do not silently change unrelated database structures in this prompt.

### D4 — Actual-zero treatment

Specify that:

* An Actual value of numerical zero is not missing data.
* Actual-zero observations are excluded from ordinary MAPE with a dedicated, explicit reason/status; their absolute error remains available and auditable.
* Address all relevant combinations explicitly: Forecast > 0 / Actual = 0; Forecast < 0 / Actual = 0; Forecast = 0 / Actual = 0; Forecast = 0 / Actual ≠ 0; and missing Actual.
* Preserve the existing authorized handling of zero Forecast and sign-change/zero-base regimes unless an explicitly approved amendment is strictly required.
* Never manufacture an ordinary percentage error by silently substituting an epsilon, arbitrary denominator, or constant.
* Keep metric-specific eligibility explicit: a null MAPE does not automatically mean that absolute error is null.

Important boundary: the owner's approval explicitly resolves ordinary MAPE treatment for Actual = 0. It does not independently authorize arbitrary changes to Bias, baseline formulas, or Reliability mappings. Preserve their already-authorized formulas where mathematically defined; where the approved policy and existing specification do not determine a behavior, document a precise unresolved rule instead of inventing one.

### D5 — Sufficiency and effective MAPE sample size

Specify that:

* General evaluation sufficiency counts valid, nonduplicate forecast outcomes after Actual selection and data-quality eligibility, even when an outcome is not eligible for ordinary MAPE.
* Report the general eligible outcome count and the effective MAPE-eligible count separately.
* Apply the existing locked minimum-observation thresholds to the general eligible outcome count, unless the authoritative specification explicitly states otherwise.
* Never represent general sufficiency as the number of MAPE-scored observations.
* Apply these counts independently to each scenario, horizon, metric, and model version according to the locked evaluation-series identity.
* A single forecast event must not be counted repeatedly within the same series due to duplicated records or scenario pooling.

## 4. Cross-cutting invariants

The amended specification must preserve all of the following:

* Historical point-in-time integrity and immutable published evaluation artifacts.
* Exact ReportVersion/publication-date provenance and reproducible, version-pinned reruns.
* `NULL` is not numerical zero.
* Forecasts and Actuals must match the same metric definition and financial period.
* No mixing of horizons, model versions, or scenarios within a series.
* No unauthorized Reliability mapping or calibration behavior. Reliability remains withheld until its formula and mappings receive explicit authority.
* No Stage 6 forecast generation and no feedback from later Actuals into historical Stage 5 forecast inputs.
* No direct Reliability adjustment to Forward P/E.
* No reopening of frozen Stages 1–5.
* No unapproved schema, migration, or database changes.

## 5. Resolve ambiguities conservatively

Before editing, build a compact internal checklist of the required changes and cross-references.

If the locked specification contains contradictory requirements, or if a technical detail cannot be determined from the approved decisions and authoritative sources:

1. Implement only the unambiguous, approved specification changes.
2. Do not invent a formula, weighting scheme, threshold, tie-break, or data-selection rule.
3. Record each remaining issue as a specific blocker, including the affected section, the missing rule, its downstream impact, and the exact decision or schema work still required.
4. Do not claim the specification is fully resolved or Stage 6 is ready to freeze.

Do not reopen the broad authority search. The targeted authority trace in Prompt 28 and the decision record in Prompt 29 are sufficient context for this bounded task.

## 6. Validation requirements

This is a specification-only prompt; do not implement runtime behavior yet.

Perform six-layer specification validation, adapted to documentation:

1. **Formula/definition audit:** verify definitions of Actual selection, error metrics, MAPE eligibility, and sample counts.
2. **Contract/boundary audit:** verify scenario identity, data-quality states, zero-versus-missing, and forecast/Actual matching.
3. **Production-path consistency audit:** trace cross-references between the amended sections and all relevant locked Stage 6 sections.
4. **Adversarial-case audit:** explicitly reason through tied publication timestamps, invalid timestamps, later restatements, estimated Actuals, suspicious/unmapped Actuals, all Actual-zero combinations, duplicate events, and three scenarios sharing one forecast event.
5. **Regression audit:** confirm the amendments do not contradict the existing locked Stage 6 rules or frozen Stages 1–5.
6. **Independent audit:** after editing, re-read the modified sections from the file and check for contradictions, missing cases, accidental broad edits, and claims that exceed owner approval.

Do not count a successful text edit as validation. No application test result may be claimed because runtime code is not being changed.

## 7. Reporting

Append exactly one new section to `temp_report.md`:

`REPORT — Stage 6 Prompt 30: Approved Methodology Specification Amendment`

Include:

* Approved decisions applied (D1–D5).
* Exact specification sections changed.
* A concise change summary for each decision.
* Results of each of the six validation layers.
* Remaining unresolved methodology or schema blockers, if any.
* Confirmation that Stages 1–5 were not changed.
* Confirmation that no source code, tests, schemas, migrations, or configuration were changed.
* Confirmation that no tests were run.
* Final status: `SPECIFICATION AMENDED — IMPLEMENTATION NOT YET AUTHORIZED` if any implementation-level ambiguity remains; otherwise `SPECIFICATION AMENDED — READY FOR IMPLEMENTATION REVIEW`.
* Explicit statement: `Stage 6 is NOT FROZEN.`

## 8. Prohibited actions

* No source-code changes.
* No test changes.
* No schema or migration changes.
* No changes to Stages 1–5.
* No repository-wide exploration.
* No GitHub, GitHub CLI/API, remote operations, commits, pushes, pulls, or branch changes.
* Do not implement any runtime behavior in this prompt.
* Do not declare Stage 6 frozen.

Make only the bounded specification amendment and the required report append. Then stop and report the result concisely.
===============================================================


# Stage 6 Prompt 31 — Record Explicit Owner Approval and Amend the Locked Specification

You are the primary engineering agent for `analyzer`, a financial-data application. Financial correctness, point-in-time integrity, deterministic behavior, auditability, and preservation of historical evaluation artifacts take priority over implementation speed.

## 1. Binding owner approval — supplied directly in this prompt

The project owner explicitly approved all five methodology policies D1–D5 in the active ChatGPT conversation on 2026-10-09, in response to the question asking whether those five proposed policies should be approved as the owner's methodology decisions.

The owner's answer was: **"موافقم"** ("I agree").

This direct owner approval is authoritative for this task. The approval does not need to have been recorded in an earlier repository report to be valid. Prompt 29's unapproved decision table reflects the state before this subsequent owner approval; it must not be treated as evidence that the owner has not approved the policies.

Prompt 30 was blocked because it relied solely on the older repository decision table. Its report accurately documents that no files were amended under Prompt 30, but its conclusion that owner approval is absent is superseded by the explicit owner approval supplied above.

Do not ask the owner to approve D1–D5 again. Do not fabricate a GitHub approval record, commit, signature, or approval timestamp other than the date supplied above. Record the source of approval as: **direct owner approval in the active ChatGPT conversation, 2026-10-09**.

## 2. Scope restrictions

Inspect only:

1. `PROJECT_HANDOFF_INSTRUCTIONS.md` for operational constraints.
2. `06_Stage6_Forecast_Evaluation.md`, limited to the sections governing Actual selection, error metrics, evaluation-series identity, sufficiency, baseline comparison, Reliability, data-quality states, auditability, and historical immutability.
3. The Prompt 27–30 reports in `temp_report.md`, using them as historical records rather than overriding the direct owner approval above.

Do not perform repository-wide exploration. Do not inspect unrelated modules or stages.

## 3. Approved methodology policies

Apply the following five owner-approved policies to `06_Stage6_Forecast_Evaluation.md`.

### D1 — First-known Actual and historical immutability

* Historical evaluation uses the earliest eligible, valid Actual report version with a known publication timestamp under the approved first-known policy.
* Later restatements must not silently replace the selected Actual or overwrite a previously published evaluation artifact.
* Preserve exact `actual_report_version`, publication timestamp, and selection-policy version in the audit record.
* Preserve candidate and exclusion provenance, with reason codes.
* If multiple eligible candidates share the earliest publication timestamp and authoritative sources provide no defensible ordering, mark selection ambiguous and fail closed. Do not break ties using arbitrary database IDs or an unapproved ordering.
* Any authorized rerun must be a separately identified, version-pinned evaluation artifact with explicit lineage. Historical artifacts must not be overwritten.
* Do not interpret first-known as latest database row or highest version number.

### D2 — Actual data quality

* `SUSPICIOUS` and `UNMAPPED` Actuals are excluded from Actual selection, scored metrics, baseline comparison, and sufficiency counts. Preserve auditable exclusion records.
* `ESTIMATED` Actuals may participate only with explicit quality/provenance flags and mandatory sensitivity analysis that recomputes the relevant outputs excluding `ESTIMATED` observations.
* Clearly distinguish primary and sensitivity outputs.
* `RESTATED` handling must follow D1. A later restatement cannot displace the first-known Actual in the primary historical evaluation.
* Apply quality eligibility before selecting among Actual candidates.
* Never convert missing or invalid data to numerical zero.
* Do not redefine Stage 1 quality states.

### D3 — Scenario-separated evaluation series

* Bear, Base, and Bull are separate evaluation series.
* Scenario identity must be present in the evaluation key and retained in audit/output records.
* Do not pool scenarios into a single MAPE, Bias, sufficiency count, baseline comparison, or Reliability result.
* Apply minimum-observation thresholds independently to each scenario-specific series.
* Do not count three scenarios for one forecast event as three independent observations in a shared series.
* If the current schema or output contract cannot preserve scenario identity, document the exact blocker. Do not change schemas or migrations in this prompt.

### D4 — Actual-zero treatment

* Numerical Actual zero is not missing data.
* Exclude Actual-zero observations from ordinary MAPE with a dedicated status/reason code; retain absolute error and its provenance.
* Explicitly document the relevant cases:

  1. Forecast > 0, Actual = 0.
  2. Forecast < 0, Actual = 0.
  3. Forecast = 0, Actual = 0.
  4. Forecast = 0, Actual ≠ 0.
  5. Actual missing.
  6. Sign-change and zero-base regimes.
* Preserve already-authorized zero-Forecast and sign-change handling unless the specification contains a genuine contradiction requiring a documented blocker.
* Never use epsilon, an arbitrary denominator, or a constant to manufacture ordinary percentage error.
* A null MAPE does not imply null absolute error.
* Do not infer authorization to change Bias, baseline formulas, or Reliability mappings from the Actual-zero decision. Where the existing specification and owner approval do not determine a rule, document the unresolved rule instead of inventing it.

### D5 — Sufficiency and effective MAPE sample size

* General sufficiency counts valid, nonduplicate forecast outcomes after Actual selection and quality eligibility, including outcomes that are not eligible for ordinary MAPE.
* Report the general eligible outcome count and effective MAPE-eligible count separately.
* Apply existing locked sufficiency thresholds to the general eligible outcome count, unless an authoritative specification explicitly says otherwise.
* Never label general sufficiency as the number of MAPE-scored observations.
* Apply these counts independently to each scenario, horizon, metric, and model version.
* Do not count duplicate records or pool scenarios.

## 4. Resolve cross-cutting requirements conservatively

Preserve:

* Historical point-in-time integrity and immutable published evaluation artifacts.
* ReportVersion/publication timestamp provenance and reproducible version-pinned reruns.
* `NULL` is not numerical zero.
* Forecast and Actual must match the same metric definition and financial period.
* No mixing of horizons, model versions, or scenarios.
* Reliability remains withheld until its authorized formula and mappings are resolved.
* Stage 6 must not generate forecasts or use later Actuals as historical Stage 5 forecast inputs.
* Reliability must not numerically adjust Forward P/E.
* Stages 1–5 remain frozen and unchanged.

If a technical detail is not determined by the approved policies and authoritative specification, do not invent a rule. Record the exact blocker and its downstream impact.

Do not reopen the broad authority search. Prompts 27–30 provide sufficient bounded context.

## 5. Required execution sequence

1. Read the latest Prompt 27–30 report sections and the relevant locked specification sections within the stated scope.
2. Append a short owner-approval clarification to `temp_report.md` explaining that D1–D5 were approved directly in the active ChatGPT conversation on 2026-10-09. Explicitly distinguish this approval from the still-unapproved technical details.
3. Amend `06_Stage6_Forecast_Evaluation.md` to encode the five approved policies as normative requirements. Preserve document structure and use minimal, targeted edits.
4. Re-read every modified specification section from disk.
5. Perform the six-layer validation below.
6. Append the final Prompt 31 report to `temp_report.md`.

Do not stop solely because Prompt 29's old decision table says `NOT YET APPROVED`. That table predates the direct owner approval. Update or supersede its decision status only through a clear, append-only clarification; do not erase the historical record.

## 6. Six-layer validation — mandatory

This is a specification-only task. Perform and document all six layers:

1. **Formula/definition audit:** Actual selection, error metrics, MAPE eligibility, and sample-count definitions.
2. **Contract/boundary audit:** scenario identity, quality states, zero-versus-missing, and Forecast/Actual matching.
3. **Production-path consistency audit:** cross-references among all relevant locked Stage 6 sections.
4. **Adversarial-case audit:** tied publication timestamps, invalid/missing timestamps, later restatements, ESTIMATED/SUSPICIOUS/UNMAPPED data, all Actual-zero combinations, duplicates, and three scenarios sharing one event.
5. **Regression audit:** no contradiction with unchanged locked requirements or frozen Stages 1–5.
6. **Independent audit:** re-read the actual modified file and check for omissions, contradictions, accidental broad edits, and claims exceeding owner approval.

Do not claim runtime tests passed. No application code is being changed, so do not run or report application tests as if they validate this documentation-only task.

## 7. Reporting

Append the following section to `temp_report.md`:

`REPORT — Stage 6 Prompt 31: Owner Approval Recorded and Specification Amendment`

Include:

* Direct owner approval source and date.
* Confirmation that D1–D5 are approved, while technical details not covered by that approval remain subject to evidence or explicit blocker reporting.
* Exact sections of `06_Stage6_Forecast_Evaluation.md` changed.
* Summary of each D1–D5 amendment.
* Results of all six validation layers.
* Remaining methodology, schema, or output-contract blockers.
* Confirmation that Stages 1–5 were not changed.
* Confirmation that no source code, tests, schemas, migrations, or configuration were changed.
* Confirmation that no runtime tests were run.
* Final status:

  * `SPECIFICATION AMENDED — READY FOR IMPLEMENTATION REVIEW` only if the amended specification is internally consistent and no implementation-blocking ambiguity remains; or
  * `SPECIFICATION AMENDED — IMPLEMENTATION BLOCKED` if unresolved blockers remain.
* Explicit statement: `Stage 6 is NOT FROZEN.`

## 8. Prohibited actions

* No source-code or test changes.
* No schema or migration changes.
* No changes to Stages 1–5.
* No repository-wide exploration.
* No GitHub, GitHub CLI/API, remote operations, commits, pushes, pulls, or branch changes.
* No runtime implementation.
* No unauthorized Reliability mappings or calibration behavior.
* Do not declare Stage 6 frozen.

Make only the targeted specification amendment and the required append-only report entries, then stop and report the outcome concisely.
============================================================


# Stage 6 Prompt 32 — Bounded Resolution Package for Remaining Implementation Blockers

You are the primary engineering agent for `analyzer`, a financial-data application. Financial correctness, point-in-time integrity, deterministic behavior, auditability, and preservation of historical artifacts take priority over implementation speed.

## 1. Current authoritative state

Stage 6 Prompt 31 amended `06_Stage6_Forecast_Evaluation.md` with the owner-approved policies D1–D5. Its report is:

`REPORT — Stage 6 Prompt 31: Owner Approval Recorded and Specification Amendment`

The report records:

* D1–D5 are approved by the owner.
* Specification changes were made and all six documentation-validation layers passed.
* Stage 6 remains NOT FROZEN.
* Implementation is blocked by RB-1 through RB-5.
* Reliability formula/mappings remain unauthorized.
* B1, B2, B3, B4, B7, and B8 remain unresolved unless separately evidenced as resolved.

Treat Prompt 31's report and the current locked specification as the starting state. Do not repeat completed work or re-litigate D1–D5.

## 2. Purpose

Prepare a compact, evidence-grounded resolution package for the remaining blockers before runtime implementation.

This is a read-only methodology and contract analysis. It must not make owner decisions, implement behavior, or change the locked specification.

## 3. Strict inspection scope

Inspect only:

1. `06_Stage6_Forecast_Evaluation.md`, limited to the amended sections and relevant existing sections governing:

   * §4 Forecast → Actual Mapping;
   * §§9 and 12 error metrics, MAPE, zero-base and sign-change handling;
   * §14 series identity and minimum observations;
   * §17 baseline comparison;
   * §37 scenario and Reliability;
   * §§39–41 outputs, auditability, and data quality.
2. `temp_report.md`, limited to the latest reports for Prompts 27–31.
3. Only if required to establish the current output contract, inspect the exact existing schema/output definitions already referenced by §39. Do not perform broad schema discovery.

Do not perform repository-wide searches. Do not inspect unrelated stages or modules.

## 4. Analyze these blockers independently

### RB-1 — Scenario identity in the output contract

The approved D3 policy requires separate Bear, Base, and Bull evaluation series, but the Prompt 31 report says §14/§39 do not yet carry scenario identity in the series key/output fields.

Determine, from the bounded evidence:

* The minimum exact fields/keys required to keep scenario identity separate through evaluation, persistence, and returned outputs.
* Whether this can be satisfied by an existing supported field or whether an output-contract/schema amendment is required.
* The exact contract boundary that currently prevents implementation.
* Whether a schema migration is genuinely necessary, or whether that conclusion cannot yet be established without broader inspection.

Do not invent a database field name or claim schema feasibility without evidence. Do not change schemas or migrations.

### RB-2 — Bias when Actual = 0

D4 excludes Actual-zero observations from ordinary MAPE but does not automatically decide their Bias treatment.

Read the exact currently locked Bias formula and identify:

* Whether the formula is mathematically defined for Forecast > 0 / Actual = 0.
* Whether it is mathematically defined for Forecast < 0 / Actual = 0.
* What happens for Forecast = 0 / Actual = 0.
* Whether Forecast = 0 / Actual ≠ 0 is already governed by the existing ZERO_BASE rule.
* Whether the locked specification defines Bias eligibility independently from MAPE eligibility.

Do not silently assume that excluding an observation from MAPE excludes it from Bias, or vice versa. Do not change the formula, introduce epsilon, or choose a new denominator.

Present only the smallest set of genuinely unresolved owner choices, with consequences for Bias interpretation, sufficiency reporting, and auditability.

### RB-3 — Baseline comparison with MAPE-ineligible outcomes

Inspect the exact baseline-comparison formula and the authorized Seasonal Naive baseline definition.

Determine:

* Whether baseline and model MAPE are calculated on exactly the same eligible forecast events within each scenario-specific series.
* How Actual-zero and other MAPE-ineligible outcomes affect the baseline's MAPE sample.
* Whether the current specification defines the baseline denominator and eligibility rules for this case.
* Whether any proposed change would alter the baseline forecast itself, as opposed to merely defining comparison eligibility.

Do not invent a weighting convention, a replacement baseline, or an improvement formula. Do not assume that a zero baseline error permits arbitrary division or a fabricated improvement percentage.

Present the smallest unresolved decision set needed to ensure a fair, reproducible comparison.

### RB-4 — Reliability

Reliability remains withheld until its formula and mappings are authorized.

Do not design or select a new Reliability formula in this prompt. Determine only which already identified missing authorities still block Reliability and whether any of them can be resolved from the bounded authoritative sources without inventing policy.

Explicitly preserve the invariant that Reliability must not numerically adjust Forward P/E.

### RB-5 — Version-pinned reruns and ESTIMATED sensitivity mechanics

The approved D1/D2 policies require separately identified, version-pinned reruns and mandatory sensitivity analysis excluding ESTIMATED observations.

Determine the minimum implementation contract needed to make these requirements auditable:

* evaluation artifact identity and version;
* linkage to the superseded artifact, if any;
* the selection-policy/specification version;
* the quality-policy version;
* primary versus ESTIMATED-excluded sensitivity result identity;
* exact Actual/report provenance;
* reproducibility and historical immutability.

Use existing authoritative output conventions where available. If a field or convention is missing, identify it as a proposed contract requirement, not as an existing feature. Do not invent names as though they already exist.

Separate essential requirements from optional implementation choices.

## 5. Required output

Append exactly one section to `temp_report.md`:

`REPORT — Stage 6 Prompt 32: Remaining Blocker Resolution Package`

Include:

1. A concise evidence table with columns:

   * Blocker;
   * authoritative text/section;
   * established facts;
   * genuinely unresolved question;
   * downstream risk;
   * minimum decision or contract amendment required.
2. For RB-1, the exact proposed series/output contract requirements, clearly labelled PROPOSAL — NOT YET APPROVED.
3. For RB-2 and RB-3, only the smallest set of owner choices necessary to resolve ambiguity. Explain consequences neutrally; do not select an option.
4. For RB-4, the missing authority list and confirmation that Reliability remains withheld.
5. For RB-5, minimum required audit/versioning invariants versus optional mechanics.
6. Explicit dependencies among RB-1–RB-5.
7. A final list of exact questions the owner must answer, numbered and answerable without reviewing code.
8. A recommended execution order, without treating a recommendation as approval.

## 6. Validation and safety requirements

Perform six-layer validation adapted to this read-only analysis:

1. **Formula/definition audit:** verify the actual locked formulas and their mathematical domains.
2. **Contract/boundary audit:** scenario identity, Actual-zero, MAPE/Bias eligibility, baseline eligibility, versioning.
3. **Production-path consistency audit:** trace only the bounded references between §14, §17, §37, §39, §40, and §41.
4. **Adversarial-case audit:** all Forecast/Actual zero combinations, MAPE-ineligible outcomes, three scenarios for one event, baseline perfect-zero-error case, later restatement, and primary versus sensitivity outputs.
5. **Regression audit:** preserve D1–D5, frozen Stages 1–5, and all previously locked invariants.
6. **Independent audit:** re-read the appended report and verify that facts, proposals, and owner decisions are clearly distinguished.

No runtime tests are expected because this prompt is read-only. Do not claim any tests passed.

## 7. Prohibited actions

* No source-code or test changes.
* No changes to `06_Stage6_Forecast_Evaluation.md`.
* No schema, migration, or configuration changes.
* No changes to Stages 1–5.
* No broad repository exploration.
* No GitHub, GitHub CLI/API, remote operations, commits, pushes, pulls, or branch changes.
* Do not invent or approve any methodology decision.
* Do not implement Reliability.
* Do not declare Stage 6 frozen.

Append the report, stop, and summarize the unresolved owner decisions.
=================================================================
# Stage 6 Prompt 33 — Apply Delegated Methodology Decisions and Amend the Locked Specification

You are working on the financial-data repository `analyzer`.

The user has explicitly delegated the remaining technical methodology choices to ChatGPT, requesting the technically correct and optimal choices rather than further questions. Treat the decisions explicitly enumerated below as authorized decisions for this prompt. Do not stop to ask the user to select among these options.

## 1. Mission

Resolve the bounded Stage 6 methodology blockers identified in:

* `temp_report.md` — Stage 6 Prompt 27 through Prompt 32 reports
* `06_Stage6_Forecast_Evaluation.md` — current locked specification and Prompt 31 amendments

Record the authorized decisions, amend the locked specification additively, and perform a strict documentation/contract audit.

This is a **methodology and specification amendment prompt only**. Do not implement evaluation logic, change schemas, create migrations, modify application code, or claim runtime validation.

Stage 6 must remain **NOT FROZEN**.

## 2. Scope and operational restrictions

Inspect only:

1. `06_Stage6_Forecast_Evaluation.md`
2. The exact Prompt 27–32 reports in `temp_report.md`
3. The smallest directly referenced schema/output-contract definitions needed to establish whether scenario identity already has a persistence location

Do not scan the repository broadly. Do not inspect unrelated stages or files unless a specific dependency is explicitly referenced and strictly necessary.

Stages 1–5 are frozen. Do not modify them.

No GitHub, GitHub CLI/API, remote operations, push, pull, commit, branch changes, or other Git mutations.

Append the final report to `temp_report.md`; do not overwrite previous reports.

## 3. Authorized decisions

### D1 — Scenario identity and separation (RB-1)

Approved policy:

* Bear, Base, and Bull are independent evaluation series.
* Scenario identity must be retained in evaluation keys, persisted evaluation/audit records, and returned scenario-specific outputs.
* MAPE, Bias, eligible observation counts, MAPE-effective counts, baseline comparisons, and any future Reliability result must not pool scenarios.
* Report both general valid-observation sufficiency and effective MAPE sample sufficiency separately for each scenario.
* One forecast event represented by three scenarios must never be counted as three observations in a shared series.

Inspect only the directly relevant existing schema/output definitions to determine whether the contract can support this without a migration.

Do not perform a migration. If a migration appears necessary, report the evidence and the smallest required contract change. Do not infer that a migration is required merely because §39 currently lacks a named scenario field.

### D2 — Bias eligibility and Actual-zero cases (RB-2)

Keep the existing authorized Bias formula:

`Bias = mean((Actual - Forecast) / abs(Forecast))`

Do not invent another formula, denominator, epsilon, or arbitrary adjustment.

Apply these rules:

1. `Forecast != 0` and `Actual = 0`: Bias is mathematically defined and remains eligible for Bias, subject to all other validity and pairing rules. Its term is exactly `-1` for a positive forecast and `+1` for a negative forecast.
2. `Forecast = 0` and `Actual = 0`: Bias is undefined. Exclude it from Bias with an explicit status/reason code. Retain Absolute Error and provenance.
3. `Forecast = 0` and `Actual != 0`: percentage Bias is undefined because its denominator is zero. Return NULL with the applicable ZERO_BASE status/reason. Retain Absolute Error and provenance.
4. Actual-zero exclusion from ordinary MAPE does not automatically exclude an observation from Bias.
5. Bias eligibility is independent of MAPE eligibility. Keep separate Bias-eligible and MAPE-effective observation counts.
6. Model and baseline Bias must use the same paired, Bias-eligible events within the same company, metric, horizon, model version, and scenario.
7. Preserve the distinction between absolute error, percentage error, APE, MAPE, and Bias. Never silently reuse one metric's eligibility predicate for another.
8. If the specification uses both “Bias” and “Percentage Bias,” clarify terminology without changing the authorized formula or behavior.

### D3 — Baseline comparison (RB-3)

Preserve the authorized Seasonal Naive baseline definition in §16. Do not replace it, invent a new benchmark, or change its forecasting formula.

Apply these rules:

1. Model and baseline comparisons must use the same eligible, paired forecast/actual events for the metric being compared, with scenario separation preserved.
2. MAPE comparison uses the same MAPE-effective event set for model and baseline.
3. Bias comparison uses the same Bias-eligible event set for model and baseline.
4. Keep absolute errors and other valid diagnostics available when MAPE is undefined.
5. If baseline MAPE is NULL, relative baseline improvement is NULL with an explicit non-computable reason.
6. If baseline MAPE is zero, relative baseline improvement is NULL with an explicit zero-denominator reason. Do not divide by zero, add epsilon, or substitute an arbitrary denominator.
7. If there are no eligible paired events, return the applicable NULL/status result rather than manufacturing a score.
8. These rules govern comparison eligibility and reporting only. They do not change the Seasonal Naive baseline forecast itself.
9. Do not invent weighting, interpolation, or fallback rules.

Preserve the existing relative-improvement formula whenever its denominator is valid.

### D4 — Reliability remains withheld (RB-4)

Reliability must remain **WITHHELD / NULL** until a separately authorized methodology defines:

* The complete Reliability formula
* Input-to-score mappings
* Bias and baseline-advantage mappings
* Observation-confidence handling
* Aggregation and scenario-specific calculation
* Calibration eligibility and mapping
* Required versioning and audit provenance

Do not create these formulas or mappings in this prompt. Do not infer them from performance weights alone.

Reliability must never numerically alter Forward P/E. Scenario separation must be preserved if Reliability is authorized in a later phase.

### D5 — Evaluation reruns, immutable artifacts, and sensitivity (RB-5)

Amend the specification to require the following invariants:

1. Every published evaluation result must have a stable, unique evaluation-artifact identity and version.
2. A rerun must create a separately identifiable artifact and must never overwrite or silently rescore an already published historical artifact.
3. A rerun must link to the artifact it supersedes or re-evaluates, where applicable.
4. Record the applicable Stage 6 specification/methodology version and data-quality-policy version.
5. Record exact Actual provenance, including `actual_report_version` and the Actual publication timestamp when applicable. Do not confuse publication timestamp with the forecast data cutoff.
6. Preserve candidate selection, exclusion, and quality flags with explicit reason codes.
7. Keep primary results and ESTIMATED-excluded sensitivity results independently identifiable and reproducible.
8. ESTIMATED observations may participate in the primary result only with an explicit quality flag and mandatory sensitivity recomputation excluding ESTIMATED observations.
9. RESTATED Actuals follow the approved first-known Actual policy for the primary historical evaluation. A later restatement must not rewrite a previously published historical state.
10. A rerun must be reproducible from its pinned inputs, policies, and versions. Where deterministic reproduction cannot be guaranteed, the limitation must be explicit.
11. Keep field names, version-string formats, storage representation, and linkage mechanics implementation-neutral unless existing authoritative contracts already define them. Do not invent an existing convention.

Label each contract requirement as one of:

* **EXISTING AND VERIFIED** — cite the exact existing field/section.
* **REQUIRED, CONTRACT AMENDMENT** — the requirement is authorized but the existing contract does not yet establish it.
* **IMPLEMENTATION DETAIL, DELEGATED** — the invariant is mandatory, while the representation is left to a later implementation prompt.

Do not claim an existing schema field or mechanism without inspecting the exact relevant definition.

## 4. Insufficient-history and MAPE-effective counts

Preserve the already approved minimum-observation thresholds:

* Fewer than 5 valid non-duplicate observations: insufficient
* 5–7: low
* 8–11: moderate
* 12 or more: adequate

Keep the general valid-observation count separate from the metric-specific effective count.

For each scenario series, report at least:

* General valid-observation count
* Bias-eligible count
* MAPE-effective count

Do not count a MAPE-ineligible observation as MAPE-effective. Do not assume that a single count is sufficient for every metric.

Do not invent new Reliability sufficiency mappings. Reliability remains withheld.

## 5. Required specification work

Make only additive, internally consistent amendments to `06_Stage6_Forecast_Evaluation.md`.

Update the appropriate existing sections, including the relevant sections among §§9, 10, 12, 14, 16, 17, 37, 39, 40, and 41. Do not blindly insert duplicated or contradictory rules.

Ensure that the specification unambiguously distinguishes:

* Scenario-specific evaluation identity
* Actual selection and immutability
* MAPE eligibility
* Bias eligibility
* Model-versus-baseline event pairing
* Zero or NULL baseline MAPE
* General versus metric-effective sample counts
* Primary versus sensitivity results
* Published artifacts versus rerun artifacts
* Reliability withholding

Preserve all previously approved D1–D5 policies from Prompt 31. Do not reopen them.

If a detail cannot be resolved without inventing a policy, leave it explicitly blocked and explain why. Do not let an unresolved implementation detail invalidate an already approved methodological invariant.

## 6. Mandatory six-layer validation

After editing, validate the resulting specification using all six layers:

1. **Formula/domain validation:** Check the exact Bias formula, zero-denominator cases, MAPE eligibility, baseline improvement, and NULL behavior.
2. **Contract/boundary validation:** Verify scenario identity, output fields, audit provenance, artifact identity, and versioning requirements.
3. **Production-path validation:** Trace how the written requirements would flow from Forecast and Actual matching through Error, metrics, baseline comparison, and outputs. This is a documentation trace only; do not implement it.
4. **Adversarial validation:** Explicitly check:

   * Positive forecast / zero actual
   * Negative forecast / zero actual
   * Zero forecast / zero actual
   * Zero forecast / nonzero actual
   * Baseline MAPE NULL
   * Baseline MAPE zero
   * No eligible paired events
   * Three scenarios sharing the same company, metric, horizon, and model version
   * ESTIMATED inclusion versus exclusion sensitivity
   * Later restatement after an evaluation artifact was published
   * Rerun versus original artifact identity
5. **Regression/invariant validation:** Confirm all Prompt 31 decisions, PIT correctness, frozen Stages 1–5, no scenario pooling, no TTM/horizon/model-version mixing, no future-data leakage, and no Reliability-to-Forward-P/E effect remain intact.
6. **Independent audit:** Re-read the amended sections and the final diff after the changes. Identify contradictions, duplicate rules, accidental scope expansion, and any unsupported claim that a contract field already exists.

Do not report a layer as PASS unless its check was actually performed.

## 7. Report requirements

Append this exact heading to `temp_report.md`:

`REPORT — Stage 6 Prompt 33: Delegated Methodology Decisions and Specification Amendment`

The report must include:

* Authorized decisions applied
* Exact specification sections changed
* Existing versus newly required contract elements
* Scenario/migration findings, based only on the bounded inspection
* The six-layer validation result, with evidence
* Remaining implementation blockers
* Confirmation that no application code, tests, schema, or migration was changed
* Confirmation that Stages 1–5 remain untouched
* Confirmation that Reliability remains withheld
* Confirmation that Stage 6 remains NOT FROZEN

Do not claim runtime tests were run. Do not claim a migration is or is not required unless the bounded inspection establishes that fact.

## 8. Completion criteria

This prompt is successful only if the authorized policies are recorded consistently, the specification is internally coherent, and the report distinguishes established facts from unresolved implementation details.

If an inconsistency cannot be resolved within the approved decisions, document it as a blocker rather than improvising.

Do not implement application logic. Do not freeze Stage 6. Do not perform Git or remote operations.

At the end, provide a concise Persian summary of the work and identify the next smallest implementation-ready step.
===========================================================
# Stage 6 Prompt 34 — Bounded Contract Audit, Specification Consistency, and Implementation Readiness

You are working on `analyzer`, a financial-data application where financial correctness, point-in-time integrity, determinism, and auditability take priority over implementation speed.

## 1. Objective

Perform a narrow, evidence-based audit following Stage 6 Prompt 33.

Resolve the following issues before any implementation prompt is authorized:

* Whether scenario identity can be persisted through the existing schema and output contract, or whether a migration investigation is necessary.
* The inconsistency between Stage 6's reported `NOT FROZEN` status and §45's `STATUS = LOCKED`.
* The inconsistent claims about whether minimum-observation thresholds are already established.
* Whether the specification's required status/reason-code semantics are complete enough for implementation without inventing financial methodology.

This is a bounded contract and documentation task. **Do not implement application logic.**

## 2. Strict scope

Inspect only:

1. `06_Stage6_Forecast_Evaluation.md`
2. The Prompt 31–33 reports in `temp_report.md`
3. Exact schema, persistence-model, or output-contract definitions directly relevant to the Stage 6 evaluation output and scenario identity

If locating the relevant definition requires exploration, use the smallest targeted search possible. Do not perform a repository-wide audit or reload the entire project.

Do not inspect unrelated financial stages unless an exact referenced authority must be verified.

No GitHub, GitHub CLI/API, remote operations, push, pull, commit, branch changes, or other Git mutations.

Stages 1–5 are frozen and must remain untouched.

## 3. Scenario identity and migration investigation

Inspect the actual relevant schema and output-contract definitions, not merely the list in §39.

Establish with evidence:

1. Where evaluation records are currently represented and persisted.
2. Whether an existing field or related key already carries scenario identity.
3. Whether scenario identity can be added compatibly at the authorized contract boundary.
4. Whether an actual database migration is necessary, optional, or not determinable from the inspected definitions.
5. Whether persisted records, evaluation keys, returned outputs, and audit records can all preserve scenario identity without pooling Bear, Base, and Bull.

Do not infer migration necessity merely because §39 lacks a scenario field.

Do not perform a migration, schema edit, or application-code change.

If evidence is insufficient, state precisely what is missing. Do not claim a migration-free solution or a migration requirement without evidence.

Preserve the approved policy: Bear, Base, and Bull are independent evaluation series throughout keys, persistence, outputs, observation counts, Bias, MAPE, and baseline comparisons. No cross-scenario pooling is permitted.

## 4. Resolve the specification's contradictory status

Inspect §45 and the exact Stage 6 status language in the Prompt 31–33 reports.

The current report says Stage 6 is `NOT FROZEN`, while §45 declares:

`STATUS = LOCKED`

Determine whether §45 is an obsolete intended final-state declaration or whether another authoritative status convention applies.

Amend the specification so it cannot simultaneously imply that Stage 6 is finally locked and not yet frozen.

Requirements:

* Preserve the locked methodological decisions already authorized.
* Distinguish a locked specification or approved policy from a frozen, implementation-complete Stage 6.
* Do not declare Stage 6 frozen.
* Do not imply that Reliability is available; it remains withheld.
* Do not reopen Stages 1–5.

Use explicit wording rather than relying on contextual interpretation.

## 5. Minimum-observation thresholds and counts

Trace the exact authority for these thresholds:

* Fewer than 5 valid non-duplicate observations: insufficient
* 5–7: low
* 8–11: moderate
* 12 or more: adequate

Prompt 33 reports these as existing and verified, while §41 also states that their owning-phase authority was not inspected in that phase.

Resolve this inconsistency using the narrowest authoritative source available.

If the thresholds are already established, cite the exact source and section in the report and remove the contradictory caveat.

If their authority cannot be verified within scope, retain them as previously specified but explicitly mark the authority-verification issue unresolved. Do not fabricate an authoritative source.

Preserve distinct per-scenario counts for:

* General valid observations
* Bias-eligible observations
* MAPE-effective observations

Do not introduce new Reliability sufficiency mappings.

## 6. Status and reason-code readiness

Audit the rules introduced in Prompt 33 for:

* `ZERO_BASE`
* Actual-zero exclusion from ordinary MAPE
* Undefined Bias
* Baseline MAPE `NULL`
* Baseline MAPE zero
* No eligible paired observations
* Excluded `SUSPICIOUS` or `UNMAPPED` Actuals
* `ESTIMATED` primary and sensitivity outputs

Determine whether the specification defines the semantic distinctions required for correct reporting, even if exact implementation identifiers remain delegated.

For each case, classify it as:

* **SEMANTICS COMPLETE** — behavior and reason are unambiguous; implementation may select a stable identifier consistent with the contract.
* **SEMANTICS INCOMPLETE** — the contract leaves a substantive behavior undecided; identify the exact unresolved question.
* **IMPLEMENTATION DETAIL** — the behavior is defined, but the exact identifier, serialization, or representation is legitimately delegated.

Do not invent new financial formulas or numerical fallbacks.

Do not force every NULL to share one reason. Different causes must remain distinguishable wherever the approved rules require that distinction.

Do not design Reliability formulas or mappings. Reliability remains `NULL`/withheld.

## 7. Specification changes

Make only the smallest additive corrections needed to resolve issues established by evidence.

Permitted:

* Correct the contradictory Stage 6 status declaration.
* Correct the thresholds-authority inconsistency.
* Clarify already-authorized status/reason semantics.
* Clarify the scenario output-contract requirement based on verified schema evidence.

Not permitted:

* Application-code changes
* Test changes
* Schema or migration changes
* New Reliability formulas or mappings
* Changes to the approved Seasonal Naive baseline
* Changes to Stages 1–5
* New weighting, fallback, epsilon, or scoring rules
* A Stage 6 freeze declaration

Do not duplicate existing rules unnecessarily. Re-read every changed section and its cross-references.

## 8. Mandatory six-layer validation

Complete all six layers and record concrete evidence for each:

1. **Formula/domain:** Confirm that the audit has not changed the approved Bias, MAPE, baseline-improvement, or zero-denominator behavior.
2. **Contract/boundary:** Verify scenario identity against actual inspected schema/output definitions and verify status/reason semantics.
3. **Production-path trace:** Trace Forecast → Actual selection → evaluation identity → errors/metrics → baseline comparison → scenario-specific output. Documentation trace only.
4. **Adversarial cases:** Verify three scenarios for one event; missing scenario identity; Baseline MAPE zero/NULL; no eligible events; every approved zero-Forecast/zero-Actual case; ESTIMATED sensitivity; later Actual restatement; rerun artifact versus historical artifact; and conflicting Stage 6 status declarations.
5. **Regression/invariants:** Confirm D1–D5 and Prompt 33 policies remain intact, Stages 1–5 are untouched, no future-data leakage or horizon/model-version mixing is introduced, and Reliability cannot change Forward P/E.
6. **Independent audit:** Re-read the final diff and affected cross-references. Check for contradictions, unsupported authority claims, scope expansion, and claims that exceed the inspected evidence.

A layer may be marked PASS only if the check was actually performed. If any layer fails, fix only the in-scope documentation defect or report it as a blocker.

## 9. Report

Append this exact heading to `temp_report.md`:

`REPORT — Stage 6 Prompt 34: Contract Audit and Implementation Readiness`

Include:

* Exact files and definitions inspected
* Scenario identity findings and migration conclusion, with evidence and limitations
* The §45 status correction
* The verified authority, or unresolved authority, for observation thresholds
* A table of status/reason-code readiness classifications
* Exact specification sections changed
* Six-layer validation results and evidence
* Remaining blockers, each separated into methodology, contract/schema, and implementation-detail categories
* Confirmation that no application code, tests, schema, or migration changed
* Confirmation that Stages 1–5 remain untouched
* Confirmation that Reliability remains withheld
* Confirmation that Stage 6 remains `NOT FROZEN`

Do not claim runtime tests were run.

## 10. Final decision gate

Conclude with exactly one status:

* `READY FOR A BOUNDED IMPLEMENTATION PROMPT`
* `BLOCKED — SPECIFICATION OR CONTRACT DECISION REQUIRED`

The first status is permitted only if the relevant scenario contract and status/reason semantics are sufficiently defined for a narrowly scoped implementation prompt without inventing methodology.

Even if ready, this prompt does not authorize implementation. The next prompt must separately define its implementation scope and require strict six-layer behavioral validation: unit/formula, contract/boundary, production-path/integration, adversarial/negative, regression, and independent audit.

Stage 6 must remain NOT FROZEN.

At completion, provide a concise Persian summary of findings and the recommended next step.
==========================================================
# Stage 6 Prompt 35 — Implement Scenario-Isolated Evaluation Identity and Aggregation

You are the primary engineering agent for `analyzer`, a financial-data application.

Financial correctness, deterministic behavior, point-in-time integrity, auditability, and preservation of explicit invariants take priority over implementation speed.

## 1. Objective

Implement one narrowly bounded Stage 6 behavior:

**Bear, Base, and Bull must remain separate throughout the existing in-memory evaluation path, from evaluation identity through aggregation and returned results.**

Prompt 34 established that the current evaluation verdicts are in-memory and no evaluation-results database table was found in the bounded inspection. It also established that scenario identity is represented in `EvaluationKey`, while `SeriesEvaluation` is scenario-free by design.

Verify these specific findings against the actual source before changing anything. Do not assume that the report is a substitute for inspecting the relevant code.

This prompt authorizes the minimal application-code and test changes required to enforce scenario separation in the existing evaluation path. It does not authorize persistent evaluation storage or a database migration.

## 2. Strict scope and repository discipline

Inspect only:

* The source definition of `EvaluationKey`
* The source definition and construction of `SeriesEvaluation`
* The directly connected aggregation and result-construction functions
* Their direct callers that pass scenario identity
* The focused Stage 6 tests for these behaviors
* Any directly relevant type or serialization contract

Locate these exact symbols using targeted searches. Do not scan or reload the entire repository.

Do not modify Stages 1–5 or unrelated Stage 6 behavior.

No GitHub, GitHub CLI/API, remote operations, push, pull, commit, branch changes, or other Git mutations.

## 3. Required implementation behavior

### A. Scenario-specific evaluation identity

Ensure scenario identity is part of the effective identity used by the existing evaluation pipeline.

The scenario dimension must distinguish Bear, Base, and Bull even when all other dimensions match:

* Company
* Metric
* Financial period
* Forecast horizon
* Model version
* Forecast cutoff, where required by the existing evaluation contract
* Scenario

Do not casually redesign the existing key or add unrelated dimensions. Preserve all existing authorized identity dimensions and add only what is necessary to enforce the scenario contract.

Inspect the existing `EvaluationKey` implementation and every directly affected call site before editing.

A missing scenario must not silently collapse a multi-scenario evaluation into Base. Inspect the existing `BASE` default and determine the smallest safe correction consistent with current callers. Update affected call sites and tests as needed. Preserve backward compatibility only where it is demonstrably safe and cannot silently misclassify or merge scenarios.

Do not invent a new scenario taxonomy. Use the repository's existing canonical scenario representation and enum/constants.

### B. Scenario-specific aggregation

Ensure aggregation cannot merge observations from different scenarios.

`SeriesEvaluation` and any directly connected aggregate/result structure must retain scenario identity wherever the structure represents a scenario-specific series.

For otherwise identical Bear, Base, and Bull observations:

* Three scenario-specific series must remain distinguishable.
* Observation counts must be calculated independently.
* Bias and MAPE inputs must not be pooled across scenarios.
* Baseline comparisons must remain within the same scenario.
* No shared series may count one forecast event's three scenarios as three observations.
* Returned scenario-specific results must retain the correct scenario identity.

Do not calculate or implement Reliability. It remains withheld/NULL.

Do not implement persistence, artifact versioning, schema changes, or migrations in this prompt.

### C. Preserve existing financial methodology

Do not change the approved formulas or eligibility rules for:

* Absolute error
* Percentage error
* APE/MAPE
* Bias
* Actual-zero cases
* ZERO_BASE
* Baseline comparison
* Minimum-observation thresholds
* ESTIMATED sensitivity analysis
* First-known Actual selection
* PIT validity

Do not introduce epsilon, arbitrary weighting, new scoring rules, or fallback formulas.

Do not alter the authorized Seasonal Naive baseline.

Do not mix horizons or model versions.

Do not let Reliability affect Forward P/E.

## 4. Required tests — strict multi-layer validation

Add or update focused tests that prove the actual behavior, not merely the existence of a scenario field.

### Layer 1 — Unit and identity/formula tests

Verify:

1. Two otherwise identical evaluation keys with different scenarios are not equal.
2. Each canonical scenario is preserved by key construction.
3. Aggregation counts each scenario independently.
4. Existing metric calculations are unchanged when all observations belong to one scenario.
5. Equality, hashing, grouping, and dictionary/set behavior are correct wherever these mechanisms are used by the implementation.

### Layer 2 — Contract and boundary tests

Verify:

1. Scenario identity survives the complete supported construction and return path.
2. Scenario-specific output structures expose the correct canonical scenario.
3. Missing or invalid scenario input cannot silently become a different scenario in the multi-scenario evaluation path.
4. Existing valid single-scenario behavior remains compatible where compatibility is explicitly supported.
5. Serialization or conversion does not discard scenario identity if those operations exist in the inspected path.

Do not create a new public serialization format unless the existing contract requires it.

### Layer 3 — Production-path/integration tests

Exercise the real connected evaluation path, not just isolated constructors.

Provide otherwise identical input observations for Bear, Base, and Bull. Confirm that the actual production-path aggregation produces three separate scenario-specific results, with the expected observations and metric inputs assigned to each.

Include baseline comparison where the existing path supports it, proving that model and baseline observations are paired within the same scenario.

### Layer 4 — Adversarial and negative tests

At minimum, cover:

* One company, one metric, one horizon, one model version, and one financial period with all three scenarios.
* Different scenario insertion orders.
* Interleaved observations from multiple scenarios.
* Duplicate observations within one scenario.
* Identical values across different scenarios.
* Missing scenario input.
* Invalid or unsupported scenario input, if the existing type/interface permits it.
* A scenario present in the forecast but absent from the paired baseline or Actual inputs.
* Empty and single-scenario evaluation inputs.
* A regression case where scenario-free aggregation would incorrectly pool observations and inflate sufficiency counts.

Assert both the expected result and the absence of cross-scenario leakage.

Do not invent the expected behavior for an unsupported boundary that the existing contract does not define. Fail closed and document it if necessary.

### Layer 5 — Regression tests

Run the focused Stage 6 tests and the full repository test suite using the commands supported by the current Claude Desktop environment.

Confirm:

* All prior authorized Stage 6 methodology remains unchanged.
* Stages 1–5 remain untouched.
* Existing valid non-scenario-specific behavior remains correct where applicable.
* No new pooling, double counting, or horizon/model-version mixing is introduced.
* Reliability remains withheld.
* No persistence or migration was introduced.

Record exact commands and actual pass/fail/skip counts. Do not claim tests passed if they were not executed.

If tests fail, investigate and correct only defects within this prompt's scope. Do not weaken assertions merely to obtain a passing result.

### Layer 6 — Independent audit

After implementation and tests:

1. Re-read the final diff.
2. Trace scenario identity from key construction through aggregation and returned results.
3. Check every directly affected call site for implicit Base assignment or dropped scenario identity.
4. Inspect tests for false positives that only assert field existence.
5. Verify that the tests would fail if scenario identity were removed from the effective aggregation key.
6. Verify that no unrelated methodology, schema, persistence, or stage was changed.

If any required invariant remains unproven, report it as a blocker.

## 5. Change control

Before implementation, identify the smallest source and test files required.

Do not make changes outside that bounded set.

Do not create an evaluation database table or perform a migration. Prompt 34 did not establish a need or authorize one.

Do not implement evaluation-artifact identity/versioning, superseded-artifact linkage, publication-timestamp persistence, or the Reliability formula in this prompt. These remain separate work items.

Do not freeze Stage 6.

## 6. Required report

Append this exact heading to `temp_report.md`:

`REPORT — Stage 6 Prompt 35: Scenario-Isolated Evaluation Identity and Aggregation`

Include:

* Exact files inspected and changed
* The pre-change failure mode established by evidence
* The scenario-identity and aggregation changes
* How missing scenario inputs are handled
* Tests added, including the three-scenario adversarial case
* Exact focused and full-suite commands and results
* Six-layer validation results with evidence
* Any remaining defects or limitations
* Confirmation that no schema, migration, or evaluation-persistence layer was introduced
* Confirmation that Stages 1–5 remain untouched
* Confirmation that Reliability remains withheld
* Confirmation that Stage 6 remains NOT FROZEN
* A short next-step recommendation

Do not claim that scenario persistence has been implemented: this prompt addresses the existing in-memory path only.

## 7. Completion gate

Mark the prompt successful only if scenario identity is preserved end-to-end through the inspected in-memory evaluation path, cross-scenario pooling is prevented, and the six-layer validation is supported by actual evidence.

Otherwise report `BLOCKED` and identify the exact unmet invariant.

Stage 6 must remain NOT FROZEN.

At completion, provide a concise Persian summary.
=================================================================

# Stage 6 Prompt 36 — Implement Versioned Evaluation Artifact Identity and Provenance Contract

You are working in the financial-data repository `analyzer`.

## 1. Mission

Implement one narrowly scoped Stage 6 improvement: establish an explicit, versioned **in-memory evaluation artifact contract** that identifies an evaluation run and records the provenance needed to distinguish its primary result from reruns and sensitivity results.

Stage 6 remains **NOT FROZEN**.

Use the existing approved Stage 6 specification, particularly `06_Stage6_Forecast_Evaluation.md` §§10, 12, 14, 17, 37, 39, 40, 41 and 45, together with the latest Prompt 31–35 reports in `temp_report.md`. Do not perform a repository-wide review.

The owner delegated technical implementation choices to ChatGPT. Apply the existing locked methodology and make conservative, auditable engineering decisions within this prompt's scope. Do not claim that the owner personally selected individual formulas or implementation details.

## 2. Strict scope

Inspect only the following initially:

* The existing evaluation pipeline's public result boundary and result types.
* The relevant evaluation observation, aggregate and verdict types.
* The code that distinguishes primary evaluation results from the ESTIMATED-excluded sensitivity evaluation, if implemented.
* Direct callers and tests that construct or consume these result objects.
* The locked Stage 6 specification and the latest Prompt 31–35 report sections in `temp_report.md`.

Use targeted symbol searches to identify the relevant files. Do not reload or analyze the entire repository.

Implement the smallest coherent contract that captures, where the existing code and available source data support it:

1. A unique identity for each evaluation artifact/run.
2. An explicit artifact or contract version.
3. The applicable Stage 6 methodology/specification version.
4. The applicable data-quality-policy version.
5. Artifact purpose/type, distinguishing the primary result from the ESTIMATED-excluded sensitivity result.
6. The relevant evaluation cutoff, where defined by the existing pipeline.
7. Actual-data provenance: source `ReportVersion` identity and publication timestamp, where available from the existing matched Actual and its authoritative provenance.
8. A link to the prior artifact when a rerun explicitly supersedes an earlier artifact.
9. Scenario-separated evaluation results, preserving the Prompt 35 identity: company, metric, horizon, model version and scenario must never be collapsed across scenarios.
10. Enough explicit metadata to distinguish a new evaluation execution from an unchanged or repeated evaluation of the same inputs.

Before editing, establish which of these fields can be populated truthfully from existing types. Follow authoritative existing source objects rather than copying values into unrelated fields or fabricating provenance.

## 3. Hard boundaries

* Do **not** create an evaluation database table, database migration, storage backend or persistence mechanism. No evaluation-results persistence table currently exists.
* Do not claim that an in-memory contract provides durable historical immutability. It must instead make the identity and intended supersession relationship explicit so a future persistence layer can enforce that policy.
* Do not invent ReportVersion IDs, publication timestamps, cutoff values, hashes, source snapshots, version identifiers or provenance.
* If required source provenance is unavailable, represent it explicitly as unavailable/invalid according to the existing project conventions. Do not silently substitute the latest report or current timestamp.
* Do not change Stages 1–5, their files, formulas, contracts or frozen behavior.
* Do not modify the approved Stage 6 formulas, Actual selection policy, data-quality eligibility, scenario separation, sufficiency thresholds, baseline methodology, ZERO_BASE behavior, Actual-zero handling, Bias/MAPE eligibility or calibration policy.
* Do not implement a Reliability score or invent any numeric Reliability mapping. Reliability remains withheld.
* Do not change Forward P/E or any valuation formula.
* Do not introduce arbitrary hashing or claim that a hash guarantees reproducibility unless the necessary canonical inputs and serialization rules already exist and are validated.
* Do not add a generic framework, speculative abstractions or unrelated refactoring.
* No GitHub, GitHub CLI/API, remote operations, push, pull, commit, branch changes or other Git operations.

## 4. Required implementation approach

### A. Inspect before designing

Trace the current evaluation result from the pipeline entry point through observation matching, scoring, aggregation and the returned result.

Identify the actual sources for:

* Evaluation cutoff.
* Forecast model version.
* Scenario.
* Matched Actual and its ReportVersion/publication provenance.
* Primary versus sensitivity evaluation.
* Any existing rerun/supersession information.

Document which values are genuinely available and which are not.

### B. Define an explicit artifact contract

Use the smallest appropriate existing type or a new focused type. Keep the contract immutable where consistent with the project's existing design.

The contract must distinguish:

* Artifact identity from model version.
* Artifact version from methodology/specification version.
* Primary results from sensitivity results.
* Scenario identity from artifact identity.
* An explicit supersession relationship from ordinary creation of another artifact.

A rerun must not silently reuse an identity in a way that makes two distinct executions indistinguishable. If an artifact supersedes another, the relationship must be explicit and validated. Do not infer supersession merely because two artifacts share a model version or evaluation cutoff.

If deterministic identity cannot be established safely from existing canonical inputs, use an appropriate unique run identity instead. State its determinism limits clearly.

### C. Preserve scenario isolation

Use the scenario-aware key and aggregation path established by Prompt 35. Ensure that each artifact's evaluation records preserve Bear/Base/Bull separation.

Do not incorrectly require the Actual itself to have a scenario. One eligible Actual may be compared against each of several scenario-specific forecasts, but their evaluation records and aggregate statistics must remain separate.

### D. Handle unavailable provenance safely

Where a required provenance field cannot be supplied from the authoritative matched Actual:

* Do not fabricate it.
* Do not silently use a newer Actual or latest report.
* Do not claim the artifact has complete audit provenance.
* Fail closed at the relevant boundary if the locked contract requires that field for a valid evaluation; otherwise expose the limitation explicitly using established project conventions.

Do not broaden this prompt into redesigning Actual matching or the data foundation.

### E. Keep the public contract compatible where safe

Inspect all direct consumers before changing a result type. Preserve compatibility only where it does not discard provenance or silently merge distinct artifacts. If a breaking change is necessary to prevent ambiguity, update its direct callers and focused tests and explain why.

Do not add unused fields merely to make the type look complete.

## 5. Mandatory six-layer strict validation

All six layers below are required. Do not treat a passing unit-test suite as a substitute for the other layers.

### Layer 1 — Unit and identity tests

Test:

* Distinct execution identities remain distinct even when the evaluated inputs are identical, if unique run identity is the chosen policy.
* Artifact version, methodology version and quality-policy version remain distinct concepts.
* Primary and sensitivity artifacts cannot be confused.
* Explicit supersession references are preserved and invalid references are rejected according to the chosen contract.
* Scenario-specific result identity remains intact.
* Immutability and equality behavior are correct for the selected type.
* Missing provenance is represented exactly as designed.
* Existing financial formulas remain unchanged.

### Layer 2 — Contract and boundary tests

Test construction and return through the public evaluation boundary.

Prove that:

* Required metadata cannot silently disappear between pipeline construction and returned results.
* Missing required provenance cannot be replaced by fabricated defaults.
* A rerun cannot silently overwrite or impersonate an earlier artifact.
* Primary and sensitivity identities remain distinguishable.
* Scenario identity survives the entire returned-result contract.
* Serialization is tested only if an actual serialization boundary exists. Do not invent one solely for this prompt.

### Layer 3 — Production-path integration tests

Use the real evaluation pipeline with the smallest representative fixtures that exercise the actual production path.

Include:

* A primary evaluation artifact.
* An ESTIMATED-excluded sensitivity artifact, if that path currently exists.
* Multiple scenarios sharing the same matched Actual.
* Available ReportVersion/publication provenance.
* A rerun and an explicitly superseding rerun, if the selected contract supports both.

Assert the actual returned metadata and result identity, not just object construction or field existence.

### Layer 4 — Adversarial and negative tests

Include:

* Identical financial inputs across two distinct executions.
* Same company/metric/horizon/model version but different scenarios.
* Missing cutoff or Actual provenance.
* Missing, malformed or unsupported artifact metadata.
* Primary and sensitivity results accidentally assigned the same identity.
* Invalid or self-referential supersession.
* A rerun with no supersession claim.
* An Actual shared across scenarios without pooling the evaluation statistics.
* Empty results and partial provenance.
* Any relevant duplicate, ordering or equality edge case.

Do not invent unsupported requirements. Where a case is not applicable, explain why in the report.

### Layer 5 — Regression and full-suite validation

Run the focused Stage 6 tests and the full available test suite using the established local Python environment and commands appropriate to this repository.

The previously used full-suite command was:

`.venv/Scripts/python.exe -m pytest src/tests/ -q`

Record the exact commands and actual pass/fail/skip counts.

Verify that:

* Prompt 35 scenario isolation remains intact.
* Approved Stage 6 formulas and policies remain unchanged.
* No horizon/model-version mixing, TTM double counting or scenario pooling is introduced.
* Stages 1–5 remain untouched.
* Reliability remains withheld.
* No database schema, migration or persistence mechanism was added.

If a test fails, investigate and fix only an in-scope defect. Do not weaken an assertion or omit a failing test to obtain a pass.

### Layer 6 — Independent audit

After implementation and testing, independently re-read the complete diff and trace the contract through its actual call path.

Explicitly verify:

* Every populated field has an authoritative source.
* No timestamp, provenance, version or supersession relationship is fabricated.
* Distinct artifact identity is not confused with model version or scenario.
* Primary and sensitivity results remain identifiable.
* Scenario isolation from Prompt 35 is preserved.
* No false immutability or persistence guarantee is claimed.
* No unrelated methodology, Reliability or Stage 1–5 change slipped in.

Where practical, add or run a counterfactual regression test demonstrating that removing a critical identity/provenance distinction causes a relevant test to fail.

## 6. Reporting requirements

Append a new section to `temp_report.md`; do not overwrite earlier reports.

Use this exact heading:

`REPORT — Stage 6 Prompt 36: Versioned Evaluation Artifact Identity and Provenance Contract`

Include:

1. Files inspected and changed.
2. Existing result path and actual authoritative sources for each populated field.
3. The selected artifact identity/version design and its limitations.
4. How primary, sensitivity and rerun artifacts are distinguished.
5. Actual ReportVersion/publication provenance availability and handling of missing provenance.
6. How scenario isolation from Prompt 35 is preserved.
7. Tests added/changed and the adversarial cases exercised.
8. Exact test commands and actual pass/fail/skip counts.
9. Evidence for each of the six validation layers.
10. Any remaining blockers or fields that cannot yet be populated truthfully.
11. Explicit confirmation that no database table, migration or persistence mechanism was added.
12. Explicit confirmation that Stages 1–5 are untouched and Reliability remains withheld.
13. Final status: Stage 6 must remain **NOT FROZEN**.

## 7. Completion gate

Report `SUCCESS` only if the artifact contract is implemented at the actual result boundary, all populated provenance is grounded in authoritative sources, scenario isolation is preserved, and all six validation layers pass with recorded evidence.

Otherwise report `BLOCKED`, identify the precise blocker, and do not claim completion.

Do not proceed to Reliability scoring or Stage 6 freeze as part of this prompt.
===============================================================

# Stage 6 Prompt 37 — Enforce Evaluation Artifact Presence at the Production Boundary

You are working in the financial-data repository `analyzer`.

## 1. Mission

Perform a narrowly scoped contract-hardening task for the evaluation artifact introduced by Stage 6 Prompt 36.

Determine whether a real production call to `run_evaluation_pipeline` can return an `EvaluationPipelineResult` without a valid evaluation artifact. If it can, implement the smallest safe correction so that every successful production evaluation result carries a valid artifact, including an explicitly represented empty evaluation where supported.

Do not assume that the existing optional field is necessarily a defect: first distinguish actual production behavior from legacy constructors, fixtures and test-only uses.

Stage 6 remains **NOT FROZEN**.

## 2. Required targeted inspection

Inspect only:

* `src/evaluation/artifact.py`
* `src/evaluation/pipeline.py`
* Direct callers and constructors of `EvaluationPipelineResult`
* Tests for the pipeline and artifact contract
* The Prompt 35 and Prompt 36 reports in `temp_report.md`
* Relevant existing Stage 6 specification clauses only if needed to resolve a contract question

Use targeted symbol searches. Do not perform a repository-wide review.

Establish:

1. Whether `run_evaluation_pipeline` always builds and attaches an artifact on successful return.
2. Whether `artifact=None` is reachable through a real production path or only through direct legacy construction.
3. Whether callers can bypass artifact validation by constructing or modifying a result.
4. Whether empty results are valid outputs and, if so, how their artifact metadata is represented.
5. Whether any downstream production consumer assumes the artifact exists.

## 3. Implementation decision rules

### Case A — No production-path bypass exists

If every successful production pipeline result already carries a valid artifact and the optional default is needed only for legacy direct constructors or test fixtures:

* Do not make a breaking change merely for stylistic consistency.
* Add focused regression tests proving the production invariant.
* Document the remaining compatibility limitation precisely.
* Do not claim that every possible manually constructed `EvaluationPipelineResult` is guaranteed to contain an artifact.

### Case B — A production-path bypass exists

If a successful production pipeline result can lack an artifact, correct the narrowest responsible boundary.

Requirements:

* Every successful production evaluation result must carry a valid artifact.
* Missing or invalid required artifact metadata must not be silently accepted.
* Preserve backward compatibility only where it does not permit a successful production result to bypass the artifact contract.
* Update only direct callers and tests affected by the correction.
* Do not weaken tests or introduce unrelated refactoring.

### Case C — The contract cannot be enforced safely

If enforcing the invariant requires an unresolved methodology decision or a wider architectural change, do not guess. Report `BLOCKED`, provide the exact call path and explain the minimum decision or change required.

## 4. Cutoff and provenance semantics

Check the existing `evaluation_cutoff` behavior without redesigning evaluation methodology.

* Do not fabricate a cutoff for empty or mixed-cutoff batches.
* Do not substitute the current time or latest available report.
* Determine whether a mixed-cutoff batch can be a valid successful production evaluation under the existing contract.
* If the existing pipeline already rejects such batches, preserve that behavior.
* If mixed-cutoff batches are currently accepted and produce `evaluation_cutoff=None`, determine whether that is an intentional supported contract or an auditability defect. Change behavior only if the current specification and code provide sufficient authority.
* Preserve the existing treatment of ReportVersion IDs and publication timestamps. Never fabricate missing provenance.

Do not expand this task into redesigning Actual matching, PIT rules, artifact identity generation or persistence.

## 5. Scenario and financial invariants

Preserve all Prompt 35 and Prompt 36 behavior:

* Bear, Base and Bull remain isolated through aggregation and returned results.
* A shared Actual may be compared against multiple scenario forecasts, but their evaluation statistics must not be pooled.
* Artifact identity remains distinct from scenario, model version, artifact-contract version and methodology version.
* Primary and ESTIMATED-excluded sensitivity artifacts remain distinguishable.
* Explicit supersession remains explicit; do not infer it.
* Approved financial formulas, eligibility, MAPE/Bias behavior, ZERO_BASE rules, baseline comparisons and sufficiency thresholds remain unchanged.
* Reliability remains withheld.
* Forward P/E and valuation formulas remain untouched.
* Stages 1–5 remain untouched.
* Do not add database tables, migrations or persistence.

No GitHub, GitHub CLI/API, remote operations, push, pull, commit, branch changes or other Git operations.

## 6. Mandatory six-layer strict validation

### Layer 1 — Unit and invariant tests

Test artifact presence and validity at the correct boundary, artifact identity behavior, empty-result behavior where supported, and unchanged scenario isolation.

### Layer 2 — Contract and boundary tests

Exercise public pipeline returns, legacy direct constructors if still supported, invalid artifact inputs and any relevant result construction boundary.

Prove that compatibility does not silently weaken the production invariant.

### Layer 3 — Production-path integration tests

Run the real pipeline for representative non-empty and empty cases, as applicable. Inspect the returned artifact and its required metadata. Include primary and sensitivity cases if the affected behavior applies to both.

### Layer 4 — Adversarial and negative tests

Include:

* Missing artifact on a successful production return.
* Invalid or malformed artifact metadata.
* Empty results.
* Mixed cutoffs if the existing pipeline permits them.
* Primary versus sensitivity results.
* Multiple scenarios sharing the same Actual.
* Any legacy construction path that could accidentally bypass the invariant.

For any case that cannot occur through the real pipeline, state why and test the nearest meaningful boundary instead.

### Layer 5 — Regression and full-suite validation

Run the focused Stage 6 tests and the full test suite.

Use the established local environment:

`.venv/Scripts/python.exe -m pytest src/tests/ -q`

Record the exact command and actual pass/fail/skip counts. Do not report expected counts as measured results.

For the Stage 6 count, use an explicit list of Stage 6 test files and report the exact list and collection count. Compare the result with Prompt 36's reported 226 tests; explain any discrepancy using actual collection evidence rather than guessing.

### Layer 6 — Independent audit

Re-read the final diff and independently trace the successful production path from `run_evaluation_pipeline` to `EvaluationPipelineResult`.

Verify:

* The artifact invariant is enforced at the correct boundary.
* No test-only fix masks a production bypass.
* Empty and mixed-cutoff behavior follows established authority.
* Scenario isolation and provenance remain intact.
* No unrelated files or financial methodology were changed.
* The reported test counts match the commands actually run.

## 7. Reporting

Append a report to `temp_report.md`; do not overwrite prior reports.

Use this exact heading:

`REPORT — Stage 6 Prompt 37: Evaluation Artifact Production-Boundary Contract`

Include:

1. Files inspected and changed.
2. The actual production call path.
3. Whether `artifact=None` was reachable in successful production results.
4. The implementation decision under Case A, B or C.
5. Empty and mixed-cutoff behavior and its authority.
6. Tests added or changed.
7. Exact commands, explicit Stage 6 test-file list, collection counts and pass/fail/skip counts.
8. Evidence for all six validation layers.
9. Confirmation that scenario isolation, provenance and financial methodology are preserved.
10. Confirmation that Stages 1–5 are untouched, Reliability remains withheld, and no persistence or migration was added.
11. Remaining limitations and final status.

## 8. Completion gate

Report `SUCCESS` only if the production artifact invariant has been demonstrated by actual call-path evidence and all six validation layers pass, or if Case A is established with sufficient regression evidence and the remaining compatibility limitation is explicitly documented.

Otherwise report `BLOCKED`.

Stage 6 must remain **NOT FROZEN**. Do not implement Reliability scoring or proceed to the final Stage 6 freeze.
==================================================================
# Stage 6 Prompt 38 — Comprehensive Contract Closure, Remediation, and Final Readiness Gate

You are the primary engineering agent for `analyzer`, a financial-data application.

## 1. Mission: close the remaining work, not merely report it

Perform a comprehensive, evidence-based closure pass over Stage 6. Identify and fix all in-scope implementation defects, contract gaps, integration failures, and missing strict tests in one continuous task. Then rerun validation and independently audit the final result.

**Do not stop after identifying a defect. Do not return a partial report merely because an individual test layer passes.** Continue through diagnosis, implementation, regression testing, correction of failures, and final audit before writing the report.

The user has explicitly delegated technical implementation choices to ChatGPT. Make conservative, financially defensible choices within the locked specification and existing approved decisions. Do not repeatedly ask the user to choose between routine technical alternatives.

However, delegation is not permission to fabricate financial methodology or override an explicitly withheld decision. In particular, Reliability scoring remains unauthorized under the current Stage 6 decisions and must not be invented.

The final outcome must be one of:

* `READY FOR FINAL FREEZE GATE`: all authorized implementation work is complete, all mandatory tests pass, and the only remaining action is the final independent freeze approval.
* `BLOCKED — EXPLICIT AUTHORITY REQUIRED`: a specific unresolved matter genuinely cannot be decided from the locked specification or delegated technical authority.
* `BLOCKED — IMPLEMENTATION OR VALIDATION FAILURE`: a technical defect or required validation remains unresolved.

Do not report `SUCCESS`, `READY`, or equivalent while an actionable, authorized defect remains.

Stage 6 must remain **NOT FROZEN** during this task.

## 2. Authority and files to consult

Read the relevant existing authority before changing code:

1. `06_Stage6_Forecast_Evaluation.md`, especially §§10, 12, 14, 16, 17, 37, 39, 40, 41 and 45.
2. The latest reports in `temp_report.md` for Stage 6 Prompts 31–37, including the approved D1–D5 decisions and their subsequent clarifications.
3. The current implementation and tests under `src/evaluation/` and the Stage 6 test files under `src/tests/`.

Use the reports as evidence of prior work, not as a substitute for checking the current implementation. Inspect actual source and tests for every important claim.

Do not reload unrelated application areas or conduct an unrestricted repository-wide exploration. First inspect the Stage 6 file list and current call graph; then follow only the directly relevant dependencies.

## 3. Preserve these locked decisions

The following requirements are non-negotiable:

* Stages 1–5 are frozen and must not be changed.
* Stage 4 remains an adapter/evidence boundary. Stage 5 must not be recalculated or reinterpreted by Stage 6.
* Only information available at the forecast cutoff may be used as forecast/evaluation inputs. A later-published Actual may be used as the evaluation outcome, under the approved Actual-selection policy.
* Missing data is not zero. Do not fabricate facts, ReportVersion identifiers, publication timestamps, cutoffs, financial drivers, share counts, equity, provenance or history.
* First-known Actual selection and historical immutability policy must be preserved.
* `SUSPICIOUS` and `UNMAPPED` Actuals are excluded under the approved policy. `ESTIMATED` Actuals participate in the primary evaluation under the existing quality rules and are excluded in the separately identifiable sensitivity evaluation.
* Bear, Base and Bull remain separate through identity, aggregation, counts, Bias, MAPE, baseline comparison and returned results. A shared Actual may be compared with each scenario, but scenario statistics must never be pooled.
* Keep the existing approved Error, MAPE, APE, Bias, ZERO_BASE, Actual-zero, baseline-improvement and sufficiency rules. Do not invent epsilons, weights, fallbacks or alternative formulas.
* Keep the Seasonal Naive baseline methodology in §16 unchanged.
* Keep model versions and horizons separate. Prevent TTM double counting and overlapping-horizon double counting.
* Keep artifact identity, artifact-contract version, methodology version, quality-policy version, model version and scenario identity as distinct concepts.
* Reruns must receive distinct artifact identities. Supersession must be explicit; do not infer it. Do not claim durable immutability without persistence.
* Do not create a database table, migration, storage backend or persistence mechanism as a shortcut.
* Reliability must remain withheld/NULL until its numeric mappings and methodology receive valid authority. Do not create a substitute score or use Reliability to modify Forward P/E.
* No changes to valuation formulas or Stage 7 behavior.
* No GitHub, GitHub CLI/API, remote operations, push, pull, commit, branch changes or other Git operations.

## 4. Close the known mixed-cutoff ambiguity

Prompt 37 confirmed that `run_evaluation_pipeline` can currently accept observations with multiple distinct forecast cutoffs and return an artifact with `evaluation_cutoff=None`.

Do not assume that existing behavior is valid merely because it is implemented.

Inspect the actual observation matching and aggregation path and establish whether observations from different cutoffs can enter the same evaluation artifact.

**Default conservative rule:** one evaluation artifact must represent one unambiguous evaluation cutoff. If a single pipeline invocation mixes distinct non-null cutoffs, fail closed with a clear, stable error before returning any scored result or artifact that could be mistaken for a single-cutoff evaluation.

Apply the following distinctions:

* An empty evaluation may retain `evaluation_cutoff=None` if it is explicitly represented as empty and no cutoff is fabricated.
* A genuinely mixed-cutoff batch must not be treated as equivalent to an empty batch.
* Do not automatically partition mixed input into multiple artifacts unless the existing public contract already defines that behavior and the complete implementation can preserve pairing, duplicate handling, scenario separation, provenance and all metrics without ambiguity.
* If the authoritative specification explicitly contradicts the conservative rule above, follow the specification and document the exact authority. Do not resolve a genuine contradiction by guessing.

Add production-path tests proving that mixed cutoffs cannot silently produce an apparently valid single-cutoff result under the chosen contract. Verify that a rejected invocation returns no partial successful result.

## 5. Perform the comprehensive closure audit

Trace the complete authorized Stage 6 path:

Forecast → Actual matching → eligibility and data-quality handling → Error and percentage metrics → Bias and MAPE aggregation → baseline pairing and comparison → scenario-separated results → artifact identity and provenance → returned result.

For each boundary, verify actual code and behavior, not merely the presence of a field or function.

### A. Actual matching and point-in-time correctness

Verify:

* Forecast/Actual matching follows the locked conceptual key and existing implementation contract.
* The correct first-known Actual is selected; a later restatement cannot silently replace the historically selected outcome.
* ReportVersion identity and publication timestamps are preserved when available.
* Missing or invalid provenance is not fabricated or silently replaced with a newer report.
* Data-quality states follow the approved eligibility and sensitivity rules.
* A single Actual shared by several scenarios does not cause their evaluation records to merge.
* Cutoff validation is enforced at the correct production boundary.

If a real defect is found, fix it within the existing approved policy and add regression tests. Do not redesign the entire data foundation.

### B. Metrics, pairing and aggregation

Verify:

* Error, MAPE, Bias and absolute-error calculations preserve the approved formulas and status conventions.
* MAPE and Bias use their correct, independently eligible observations and counts.
* Actual-zero exclusions do not incorrectly remove observations from Bias where the approved rules allow Bias eligibility.
* ZERO_BASE and other non-computable cases retain their explicit status/reason.
* Baseline and model comparisons use appropriately paired observations and the same applicable scenario, metric and horizon.
* Empty sets, undefined denominators and insufficient observations produce the specified NULL/status behavior.
* No cross-scenario pooling, model-version mixing, horizon mixing, TTM double counting or duplicate-driven inflation of sufficiency counts occurs.
* Primary and ESTIMATED-excluded sensitivity results remain separately identifiable and reproducible.

Do not alter an approved formula simply to make more observations eligible.

### C. Evaluation artifact contract

Verify the implementation introduced by Prompts 35–37:

* `EvaluationPipelineResult` carries a valid artifact on every successful production return.
* Any optional artifact field retained for legacy direct constructors is demonstrably not a production bypass.
* Each execution receives a distinct run identity.
* Artifact-contract, methodology and quality-policy versions remain separate.
* Primary and sensitivity artifacts have explicit purposes.
* Cutoff semantics distinguish empty, single-cutoff and mixed-cutoff inputs.
* Provenance is based on authoritative matched Actual records.
* Multi-period provenance retains all applicable distinct ReportVersion identities and publication timestamps.
* Supersession is explicit and cannot be self-referential.
* Missing provenance is never disguised as complete provenance.
* The contract does not claim persistence, durable immutability or reproducibility guarantees it cannot provide.
* Scenario identity is preserved through the returned artifact and evaluation results.

Fix any defect discovered here and update affected direct callers and tests.

### D. Specification and implementation consistency

Compare implemented behavior against the locked Stage 6 specification and approved decisions. Search for obsolete or contradictory paths **within Stage 6 only**, including any legacy scoring, calibration, baseline, or result-construction path that can still affect production behavior.

Do not restore de-authorized legacy logic. Do not implement Reliability scoring.

Resolve implementation inconsistencies directly where authority exists. If a specification contradiction remains, document the exact clauses and their impact instead of pretending the system is ready.

## 6. Mandatory six-layer validation

Run all six layers as a single closure workflow. If any layer exposes a defect, correct it and repeat the affected layers plus regression validation. Do not stop after the first green run.

### Layer 1 — Unit and mathematical invariants

Verify exact formulas, eligibility, reason/status behavior, artifact identity, version separation, scenario-aware keys, equality/hash behavior, duplicate handling and sufficiency counts.

Use explicit numerical examples for boundary cases. Confirm that existing approved single-scenario metrics remain unchanged.

### Layer 2 — Contract and boundary validation

Test the real public contracts for:

* Forecast/Actual matching.
* Missing or invalid provenance.
* Empty and mixed-cutoff inputs.
* Invalid artifact metadata.
* Primary versus sensitivity identity.
* Reruns and explicit supersession.
* Missing or invalid scenario identity.
* NULL versus zero.
* Legacy construction where still supported.

Ensure no boundary silently repairs invalid data by inventing a default.

### Layer 3 — Production-path integration

Use the actual production evaluation pipeline, not only isolated helpers.

Cover representative:

* Valid non-empty single-cutoff evaluation.
* Empty evaluation.
* Mixed-cutoff rejection or the exact specification-authorized alternative.
* Bear/Base/Bull evaluations sharing the same Actual.
* Primary and ESTIMATED-excluded sensitivity results.
* Baseline comparisons.
* Valid and missing provenance.
* Reruns and explicit supersession.

Assert actual returned values, status codes, artifact fields, scenario separation and counts.

### Layer 4 — Adversarial and negative tests

Include combinations that are easy to miss when testing features independently:

* Three scenarios with identical company, metric, period, horizon and model version.
* Mixed scenarios plus duplicate observations.
* Mixed cutoffs plus multiple scenarios.
* Mixed cutoffs plus partial provenance.
* Actual-zero cases with independent MAPE and Bias eligibility.
* Invalid ReportVersion metadata.
* Reordered and interleaved observations.
* Missing scenario or invalid artifact metadata.
* Primary and sensitivity evaluations with identical financial inputs.
* A rerun with no supersession claim and a rerun with an explicit supersession link.
* Empty and insufficient-history inputs.
* Any discovered combination where one individually valid feature can invalidate another feature's assumptions.

For cases that cannot occur through the actual production path, prove why and test the nearest meaningful public boundary instead.

### Layer 5 — Regression and complete test suite

Run the explicit Stage 6 test-file list and the full suite. Use the existing Windows environment:

`.venv/Scripts/python.exe -m pytest src/tests/ -q`

The Stage 6 list must be explicit and include all relevant existing Stage 6 test files, including:

* `test_stage6_artifact_identity.py`
* `test_stage6_artifact_boundary.py`
* `test_stage6_evaluation.py`
* `test_stage6_evaluation_foundation.py`
* `test_stage6_evaluation_metrics.py`
* `test_stage6_p25_adversarial.py`
* `test_stage6_p25_selection.py`
* `test_stage6_production_pipeline.py`
* `test_stage6_reliability_governance.py`
* `test_stage6_scenario_isolation.py`

Add any new Stage 6 test files created during this task to the explicit list.

Record actual collection and execution counts. Do not use a stale expected count. Explain any change in the number of tests relative to Prompt 37 using measured collection evidence.

If tests fail:

1. Inspect the actual failure.
2. Fix the underlying in-scope defect.
3. Rerun the failing tests.
4. Rerun the complete Stage 6 set.
5. Rerun the full suite.

Never weaken assertions, delete meaningful tests, or exclude a failing test to obtain a green result.

### Layer 6 — Independent final audit

After all implementation and testing are complete, re-read the entire final diff and independently trace the production path again.

Verify that:

* Every identified, authorized defect was fixed or explicitly proved not to be a defect.
* No production bypass remains for the enforced contracts.
* No mixed-cutoff artifact can be mistaken for a valid single-cutoff evaluation.
* No provenance, timestamps, financial values, versions or supersession relationships were fabricated.
* Scenario isolation is preserved end-to-end.
* All six validation layers have concrete evidence.
* Test counts match the actual executed commands.
* No unrelated change, unauthorized methodology or scope expansion was introduced.
* Stages 1–5 remain untouched.
* Reliability remains withheld.
* No persistence or migration was added.

Do not treat the same initial implementation review as sufficient independent validation. Reinspect the final changed code and test results after remediation.

## 7. Continue until closure; no premature report

**This is a completion task, not a diagnostic-only task.**

Follow this loop internally until it converges:

1. Inspect the relevant contract and production path.
2. Enumerate the in-scope defects and missing validation.
3. Implement all corrections that are authorized by the locked specification and delegated technical authority.
4. Add regression tests for each correction.
5. Run all six validation layers.
6. Fix any newly discovered in-scope defect.
7. Rerun affected tests, the complete Stage 6 set and the full suite.
8. Re-read the final diff and verify all completion criteria.
9. Only then append the final report.

Do not append interim reports for intermediate attempts. Do not claim that a task is complete because one subset of tests passes. Do not defer an already identified, authorized fix to a later prompt.

If a true blocker remains, finish all other authorized work first. Then report the exact blocking authority issue, the relevant specification clauses, the attempted resolution, and the minimum decision required. Do not ask the user a series of routine engineering questions.

## 8. Reporting

Append exactly one consolidated section to `temp_report.md` after the final audit. Do not overwrite earlier reports.

Use this heading:

`REPORT — Stage 6 Prompt 38: Comprehensive Contract Closure and Final Readiness Gate`

Include:

1. A concise list of defects found and the fixes completed.
2. Files changed and why each change was necessary.
3. The final production call graph and the critical invariants enforced.
4. Mixed-cutoff decision, its authority, and test evidence.
5. Actual matching, PIT, provenance and quality-policy findings.
6. Metrics, baseline, scenario-isolation and artifact-contract findings.
7. Tests added or changed, including adversarial combinations.
8. Exact commands, explicit Stage 6 file list, collection counts and actual pass/fail/skip counts.
9. Evidence for each of the six validation layers.
10. Independent final-audit findings and remaining limitations.
11. Explicit confirmation that Stages 1–5 were untouched, Reliability remains withheld, and no persistence/migration was added.
12. One of the three final statuses specified in §1, with concrete evidence.

The report must distinguish:

* Implemented and tested.
* Verified already correct.
* Intentionally withheld by authority.
* Unresolved technical defect.
* Unresolved authority issue.

Do not label intentionally withheld Reliability as an implementation success, and do not claim Stage 6 is frozen.

## 9. Final completion gate

`READY FOR FINAL FREEZE GATE` is permitted only when:

* All authorized in-scope defects have been resolved.
* All six validation layers pass with recorded evidence.
* The full test suite passes, with any skips explained.
* The final independent audit finds no actionable authorized defect.
* The specification and implementation agree on every behavior claimed as complete.

If any authorized defect remains, continue working on it. If an actual authority blocker prevents safe completion, report `BLOCKED — EXPLICIT AUTHORITY REQUIRED` only after completing all other authorized work.

Stage 6 must remain **NOT FROZEN**. Do not implement Reliability scoring, invent methodology, or declare a freeze as part of this task.
=======================================================================

# Stage 6 Prompt 39 — Close Cutoff Completeness and Perform the Final Independent Readiness Audit

You are the primary engineering agent for the financial-data repository `analyzer`.

## 1. Mission

Complete the remaining Stage 6 closure work in one continuous execution:

1. Inspect and correct the evaluation-cutoff contract, including missing cutoffs and TTM observations.
2. Add strict regression and adversarial tests for every discovered boundary.
3. Run the complete six-layer validation workflow.
4. Fix any additional in-scope, authorized defect found during that workflow.
5. Run the Stage 6 suite and full test suite again after the final correction.
6. Independently re-audit the final diff and production call path.
7. Append one consolidated report only after the work is complete.

Do not stop after diagnosis or after the first successful test run. Do not defer an already identified, authorized correction to another prompt.

Stage 6 remains **NOT FROZEN** unless a separate authorized final freeze approval is explicitly granted. This prompt may establish readiness for that approval, but it must not declare the stage frozen.

## 2. Current evidence and the known defect

Prompt 38 reported:

* Stage 6: 252 passed.
* Full suite: 936 passed, 2 skipped, 0 failed.
* Mixed distinct non-null cutoffs are rejected before scoring.
* Empty evaluations are allowed with `evaluation_cutoff=None`.

Independent review identified a gap in the cutoff guard in `src/evaluation/pipeline.py`:

* The current guard discards `None` values before counting distinct cutoffs.
* A batch containing one non-null cutoff and another missing cutoff may therefore pass as if all inputs had one valid cutoff.
* TTM cutoffs are considered in the guard, but the returned `evaluation_cutoff` is calculated from Forecast records only. If TTM observations carry the only valid cutoff, the artifact may incorrectly report `None`.

Treat these as concrete defects to verify against the current code, not as assumptions to copy blindly. Inspect the implementation and prove the actual behavior with tests before editing.

## 3. Authoritative cutoff contract

A non-empty evaluation artifact must have one unambiguous cutoff shared by every Forecast record and every supplied TTM observation that participates in that evaluation.

Apply these rules unless a directly applicable authoritative specification clause explicitly contradicts them:

### A. Non-empty evaluation inputs

* Every participating Forecast record must have a valid, normalized, non-null `data_cutoff_datetime`.
* Every supplied TTM observation must have a valid, normalized, non-null `forecast_cutoff_datetime`.
* All participating cutoffs must be equal after applying the project's existing datetime normalization conventions.
* If any participating input has a missing or invalid cutoff, fail closed before scoring, aggregation, governance, artifact construction or any successful result return.
* If distinct cutoffs are present, fail closed before any partial successful result is returned.
* Raise a clear, stable exception consistent with existing project conventions. Its message must identify the cutoff-contract failure without leaking irrelevant data.
* Do not silently drop the input with a missing cutoff, infer its cutoff from another record, or substitute the current time.

### B. Empty evaluation

An explicitly empty evaluation may have `evaluation_cutoff=None` only when there are no Forecast records and no TTM observations.

Do not treat a non-empty batch containing missing cutoffs as an empty evaluation.

### C. TTM-only or TTM-inclusive evaluation

* When TTM observations are supplied, their cutoffs must participate in the same validation as Forecast record cutoffs.
* If the valid non-empty evaluation consists only of TTM observations, its artifact cutoff must reflect their single valid cutoff.
* If Forecast records and TTM observations are combined, all their cutoffs must agree.
* Do not count TTM observations twice or create an additional series merely to solve cutoff handling.

### D. Datetime normalization

Use the existing authoritative normalization conventions. Equivalent timezone-aware representations of the same instant must not be falsely classified as different cutoffs if the project's normalization contract says they are equivalent.

Naive or malformed datetime values must be handled according to existing project conventions. Do not silently invent a timezone or convert invalid data into a fabricated cutoff.

### E. Actual publication timestamps

Do not confuse the evaluation cutoff with an Actual's publication timestamp.

The Actual is the evaluation outcome and may be published after the forecast cutoff. Preserve the approved first-known Actual selection and provenance rules. Do not reject a valid later-published Actual merely because it postdates the forecast cutoff.

If a genuine conflict with an explicit specification clause is discovered, record the exact clause and its consequence. Do not override explicit authority by guesswork.

## 4. Targeted inspection

Inspect the current versions of:

* `src/evaluation/pipeline.py`
* `src/evaluation/observation.py`
* `src/evaluation/schema.py`
* `src/evaluation/aggregate.py`
* `src/evaluation/artifact.py`
* `src/evaluation/reliability.py`
* Direct callers and relevant tests for the cutoff contract.
* `06_Stage6_Forecast_Evaluation.md` clauses governing point-in-time correctness, forecast cutoffs, Actual publication times, artifacts and evaluation results.
* The latest Stage 6 Prompt 35–38 reports in `temp_report.md`.

Use targeted symbol searches and follow the actual production path. Do not conduct an unrelated repository-wide review.

## 5. Implementation requirements

### A. Enforce validation before evaluation work

Place the validation at the earliest correct public pipeline boundary, before scoring, aggregation, governance, provenance construction and artifact construction.

Do not merely add a check in the artifact builder if invalid observations have already been scored.

Validate the complete set of participating Forecast and TTM cutoffs once, using the project's normalization rules.

### B. Derive artifact cutoff from validated inputs

After successful validation, derive the artifact cutoff from the validated complete input set, not from Forecast records alone.

For a non-empty successful evaluation, the artifact cutoff must equal the single validated cutoff. For an explicitly empty evaluation, `None` remains valid.

There must be no alternate branch that returns a non-empty successful evaluation with a missing or ambiguous cutoff.

### C. Preserve compatibility only where safe

Search direct callers and tests affected by stricter validation. Update only the necessary Stage 6 callers and fixtures.

Do not weaken validation merely to preserve fixtures that contain invalid inputs. Correct those fixtures to express a valid case, or explicitly test the expected rejection.

Do not change Stage 5 or the ForecastRecord contract unless an existing authoritative contract proves that a narrowly scoped change is necessary and permitted. Prefer enforcing the Stage 6 boundary.

### D. Preserve all existing Stage 6 methodology

Do not change:

* Error, MAPE, APE or Bias formulas.
* Actual-zero or ZERO_BASE behavior.
* First-known Actual selection or exact-tie fail-closed behavior.
* Data-quality participation and sensitivity policy.
* Baseline methodology.
* Sufficiency thresholds and independent counts.
* Scenario separation.
* Artifact identity, purpose or supersession semantics.
* Reliability governance or calibration.
* Forward P/E or valuation logic.

Reliability remains withheld. Stages 1–5 remain frozen and untouched.

Do not introduce a database table, migration, persistence backend or unrelated refactoring.

No GitHub, GitHub CLI/API, remote operations, push, pull, commit, branch changes or other Git operations.

## 6. Mandatory regression and adversarial test matrix

Add focused tests in the appropriate Stage 6 test files. Tests must assert the actual behavior and returned artifact, not merely the presence of a validation function.

At minimum, cover the following cases:

1. One Forecast record with a valid cutoff succeeds and returns that cutoff.
2. Multiple Forecast records with the same normalized cutoff succeed.
3. Equivalent timezone-aware representations of the same instant follow the established normalization contract.
4. Multiple distinct non-null Forecast cutoffs fail before scoring.
5. One valid Forecast cutoff plus one missing Forecast cutoff fails closed.
6. All non-empty Forecast records missing cutoffs fail closed.
7. A valid Forecast cutoff plus a TTM observation with a missing cutoff fails closed.
8. Distinct Forecast and TTM cutoffs fail closed.
9. Matching Forecast and TTM cutoffs succeed and produce the correct artifact cutoff.
10. TTM-only evaluation with a valid cutoff produces that cutoff in its artifact.
11. TTM-only non-empty evaluation with a missing cutoff fails closed.
12. Explicitly empty evaluation succeeds with `evaluation_cutoff=None` and an explicitly empty result.
13. A rejected batch returns no partial successful result, scored aggregates or artifact.
14. Reordered and interleaved observations produce the same validity decision and cutoff result.
15. Scenario-separated Bear/Base/Bull observations sharing one cutoff remain separate after validation.
16. Scenario-separated inputs with mixed cutoffs fail closed without pooling or returning partial scenario results.
17. A later-published Actual remains eligible as an outcome when otherwise valid under the approved policy; it must not be confused with the forecast cutoff.
18. Existing artifact provenance, primary/sensitivity purpose and explicit supersession behavior remain unchanged.
19. TTM conservation and duplicate-handling invariants remain intact.

For each case, establish whether it is reachable through the public production pipeline. If a case cannot occur, explain why and test the nearest meaningful public boundary.

Add tests for any further cutoff edge case found during inspection. Do not weaken or remove existing meaningful tests.

## 7. Comprehensive Stage 6 closure audit

After implementing the cutoff fix, audit the connected Stage 6 contracts in the actual production path:

Forecast → Actual matching → eligibility/quality → scoring → aggregation → baseline comparison → scenario-separated verdicts → artifact identity/provenance → returned result.

Check the following and fix every in-scope defect that is authorized by the locked specification:

* First-known Actual selection, valid ReportVersion provenance and exact-tie fail-closed behavior.
* No fabricated publication timestamps, cutoffs, IDs, values or provenance.
* `SUSPICIOUS` and `UNMAPPED` exclusion; ESTIMATED primary/sensitivity separation.
* Correct independent valid, Bias-eligible and MAPE-effective counts.
* Correct Actual-zero and ZERO_BASE status behavior.
* Correct baseline pairing and NULL/status behavior for unavailable or zero baseline MAPE.
* Scenario identity in all series keys, aggregation results and artifacts.
* No cross-scenario pooling, horizon/model-version mixing, duplicate-driven sufficiency inflation or TTM double counting.
* Artifact identity distinct from artifact version, methodology version, quality-policy version, model version and scenario.
* Every successful production return carries its artifact.
* No accidental Reliability score or unauthorized calibration path.
* No Stage 1–5 changes.

Do not expand the task into a speculative redesign of the financial methodology. Resolve authorized implementation defects; if an actual authority conflict remains, document the precise conflict.

## 8. Six-layer validation — all required

### Layer 1: Unit and mathematical invariants

Test cutoff equality, missing-value rejection, datetime normalization, artifact cutoff derivation, scenario-aware identities, formulas and relevant status/count invariants.

### Layer 2: Contract and boundary validation

Test the public pipeline boundary, missing and malformed cutoffs, mixed cutoffs, empty inputs, TTM-only inputs, artifact construction and invalid-result rejection.

### Layer 3: Production-path integration

Use the real pipeline for valid, empty, Forecast-only, TTM-inclusive, TTM-only, sensitivity and multi-scenario cases. Verify the actual returned cutoff and artifact contents.

### Layer 4: Adversarial and negative validation

Run the full matrix in §6, including mixed cutoffs combined with missing cutoffs, TTM observations, multiple scenarios, duplicate records and reordered inputs.

### Layer 5: Regression and full suite

Run the explicit Stage 6 test-file list, including all current Stage 6 test files and any new test file added by this task. Record the exact filenames and collection counts.

Then run the full suite using the established local command:

`.venv/Scripts/python.exe -m pytest src/tests/ -q`

Record the actual pass/fail/skip counts. Do not copy expected counts from earlier reports.

If any test fails:

1. Inspect the actual failure.
2. Correct the underlying in-scope defect.
3. Rerun the failing tests.
4. Rerun the full explicit Stage 6 set.
5. Rerun the full test suite after the final code change.

Do not report completion from an intermediate green run.

### Layer 6: Independent final audit

After all changes and final test runs, re-read the entire final diff and trace the production path again.

Verify:

* Every non-empty successful evaluation has exactly one valid cutoff.
* Forecast and TTM cutoffs are validated together.
* The artifact cutoff derives from the complete validated input set.
* Empty evaluation is distinguishable from invalid non-empty evaluation.
* No rejected invocation can return partial success.
* Actual publication timestamps remain distinct from the cutoff.
* All other Stage 6 contracts and scenario isolation remain intact.
* Test counts match the executed commands.
* No unauthorized methodology, unrelated code, Stage 1–5 changes, persistence or migration was introduced.

Do not treat the earlier Prompt 38 audit as a substitute for independently auditing the final implementation.

## 9. Continue until the task is genuinely closed

Use this completion loop:

1. Inspect and prove the cutoff defect.
2. Implement the correction.
3. Add and run focused regression tests.
4. Audit all six validation layers.
5. Fix any additional authorized defect found during the closure audit.
6. Rerun the complete Stage 6 test set and full suite.
7. Independently review the final diff and production call path.
8. Append the report only after the final validation is complete.

Do not append interim reports. Do not defer a known authorized correction to Prompt 40.

If an authority blocker remains, finish every other authorized task first. Then report the exact specification clauses, the precise conflict, why delegated engineering judgment cannot resolve it safely, and the minimum decision needed.

## 10. Final report

Append exactly one consolidated report to `temp_report.md`. Do not overwrite prior reports.

Use this exact heading:

`REPORT — Stage 6 Prompt 39: Cutoff Completeness and Final Readiness Audit`

Include:

1. The confirmed defect and its concrete failure mode.
2. Files inspected and changed.
3. The final cutoff contract and its specification authority.
4. How Forecast and TTM cutoffs are validated and how the artifact cutoff is derived.
5. Empty, mixed, missing-cutoff and TTM-only behavior.
6. Actual publication-time versus forecast-cutoff handling.
7. Tests added or changed and the complete adversarial matrix results.
8. Exact commands, explicit Stage 6 file list, collection counts and actual pass/fail/skip counts.
9. Concrete evidence for all six validation layers.
10. Results of the comprehensive Stage 6 closure audit.
11. The independent final-diff audit.
12. Remaining limitations and any actual authority blocker.
13. Explicit confirmation that Stages 1–5 are untouched, Reliability remains withheld, no persistence/migration was added, and Stage 6 remains NOT FROZEN.

Classify every remaining item as one of:

* Verified correct.
* Fixed and tested.
* Deliberately withheld by authority.
* Unresolved technical defect.
* Unresolved authority blocker.

## 11. Final status gate

Report `READY FOR FINAL FREEZE GATE` only if:

* All authorized defects found during this task are fixed.
* The cutoff contract is enforced at the real production boundary.
* All six validation layers pass with evidence.
* The full test suite passes, with any skips explained.
* The final independent audit identifies no remaining actionable, authorized defect.

Otherwise report `BLOCKED — IMPLEMENTATION OR VALIDATION FAILURE`, or `BLOCKED — EXPLICIT AUTHORITY REQUIRED` if and only if a genuine authority conflict remains after all other work is complete.

Do not claim Stage 6 is frozen. Do not implement Reliability scoring. Do not issue an interim report before the final validation is complete.

================================================================
# Stage 6 Prompt 40 — Enforce Duplicate-Observation Invariants and Revalidate Closure

You are the primary engineering agent for `analyzer`, a financial-data application. Financial correctness, auditability, point-in-time correctness, deterministic behavior, and explicit financial invariants take priority over implementation speed.

## 1. Objective

Resolve an actionable Stage 6 specification violation discovered during independent review of Prompt 39.

The Prompt 39 test file, `src/tests/test_stage6_p39_cutoff.py`, currently asserts that supplying the same TTM observation twice should count it twice. This conflicts with the locked Stage 6 specification:

* Section 7, invariant 16: an independent additional TTM observation must not cause double counting.
* Section 42, No Double Counting: TTM must not be counted multiple times as an observation.
* The approved D5 policy: duplicate records must not be counted, and general sufficiency counts must use valid, non-duplicate observations.

Do not accept the current duplicate-counting behavior merely because its test passes. Correct the implementation and its tests, then perform the complete validation workflow below.

**Do not freeze Stage 6 in this prompt.**

## 2. Mandatory boundaries

* Stages 1–5 are frozen and must remain untouched.
* Do not modify valuation formulas or Stage 7 behavior.
* Do not invent a new financial methodology, observation identity, tie-breaker, or duplicate-resolution rule.
* Do not change approved Error, MAPE, Bias, ZERO_BASE, baseline, sufficiency, scenario-isolation, Actual-selection, or cutoff rules except where a change is strictly necessary to enforce the already-authorized duplicate invariant.
* Preserve the Prompt 39 cutoff fixes.
* Preserve Bear/Base/Bull separation, model-version and horizon separation, and the primary versus ESTIMATED-excluded sensitivity distinction.
* Reliability must remain withheld/NULL. Do not invent mappings or a substitute score.
* Do not add a database table, migration, persistence backend, or durable-immutability claim.
* Do not perform Git operations, GitHub operations, remote access, push, pull, commits, branch changes, or repository-history changes.
* Do not perform unrestricted repository-wide exploration.

## 3. Inspect only the necessary authority and implementation

Read the exact relevant clauses in `06_Stage6_Forecast_Evaluation.md`, especially Sections 7, 14, 42, and the approved D5 text. Review the latest Prompt 38 and Prompt 39 reports in `temp_report.md`.

Inspect only the directly relevant Stage 6 implementation and tests, including:

* `src/evaluation/pipeline.py`
* The existing canonical observation/series identity and aggregation implementation under `src/evaluation/`
* `src/tests/test_stage6_p39_cutoff.py`
* The existing Stage 6 tests that cover duplicate observations, TTM accounting, sufficiency counts, scenario isolation, and aggregation.

Do not assume every repeated-looking observation is a duplicate. Use the existing authoritative identity contract. Do not create an alternative identity merely to make the new tests pass.

## 4. Required correction

Complete all of the following:

1. Establish from the locked specification and current implementation what constitutes the same evaluation observation. Use the existing canonical key/identity and existing distinctions for company, metric, financial period, horizon, model version, forecast cutoff, and scenario as applicable. Do not pool scenarios or horizons.

2. Ensure that repeating the same TTM observation cannot inflate:

   * scored observation counts;
   * general valid-observation counts;
   * Bias-eligible or MAPE-effective counts;
   * sufficiency classifications;
   * baseline-comparison sample counts;
   * any other aggregate derived from the repeated observation.

3. Ensure that a duplicated observation is not counted once as a Forecast observation and again as an equivalent TTM observation where the locked identity contract says they represent the same evaluation outcome.

4. Preserve genuinely distinct observations, including distinct periods or other identity dimensions required by the existing contract. Do not broadly deduplicate records just because their numerical values happen to match.

5. If records collide under the authoritative identity but carry materially conflicting data, provenance, or values, do not silently choose an arbitrary winner. Follow an existing authoritative resolution rule if one exists; otherwise fail closed with a clear, deterministic error and document the exact unresolved distinction. Do not invent a new winner-selection policy.

6. Preserve Prompt 39 cutoff behavior:

   * every participating Forecast record and TTM observation must have a valid normalized cutoff;
   * all participating cutoffs in one artifact must agree;
   * missing, invalid, or mixed cutoffs fail before scoring and artifact construction;
   * empty input remains explicitly empty;
   * TTM-only input retains its validated cutoff;
   * later-published Actuals remain eligible evaluation outcomes under the approved policy.

7. Update the existing Prompt 39 test that incorrectly requires duplicate TTM observations to count twice. Replace that assertion with the behavior required by the locked specification. Do not weaken unrelated tests or remove coverage merely to obtain a green run.

## 5. Mandatory regression matrix

Add or revise focused tests that establish all of the following:

* One valid TTM observation is counted once.
* Repeating the exact same TTM observation does not increase any relevant count or sufficiency classification.
* Supplying the same TTM observation in a different input order produces the same result.
* An equivalent observation arriving through the Forecast and TTM paths is not double-counted when the canonical identity says it is the same outcome.
* Genuinely distinct observations remain distinct.
* Same numerical values for genuinely distinct identity keys do not cause accidental deduplication.
* Different scenarios remain separate; deduplication in one scenario cannot remove or merge an observation from another.
* Different horizons and model versions remain separate.
* Conflicting payloads or provenance under the same canonical identity follow an already-authorized rule or fail closed; no arbitrary selection.
* Duplicate observations cannot inflate general sufficiency, Bias-eligible counts, MAPE-effective counts, or baseline pairing counts.
* Primary and ESTIMATED-excluded sensitivity evaluations remain independently correct.
* All Prompt 39 cutoff tests continue to pass, including missing/invalid cutoff, mixed cutoff, TTM-only cutoff, empty input, and later-published Actual behavior.
* Rejected invocations return no partial successful result or misleading artifact.

For every test, assert actual results and counts, not merely that a function returns or an exception is raised.

## 6. Complete six-layer validation

Perform all six layers in one continuous workflow. If any layer finds a defect, correct it and repeat the affected layers plus regression validation. Do not stop after the first passing subset.

**Layer 1 — Unit and mathematical invariants**

* Validate canonical duplicate identity, unique-observation counts, sufficiency thresholds, and unchanged metric formulas.
* Confirm duplicates do not alter any result that should be based on unique observations.

**Layer 2 — Contract and boundary validation**

* Validate duplicate Forecast/TTM overlap, repeated TTM inputs, conflicting identity collisions, missing data, and preservation of the existing identity contract.
* Validate fail-closed behavior where a conflict has no authorized resolution.

**Layer 3 — Production-path integration**

* Exercise the actual `run_evaluation_pipeline` path through matching, eligibility, scoring, aggregation, baseline comparison, scenario results, and artifact construction.
* Confirm duplicate handling occurs before duplicate records can distort aggregate results or sufficiency counts.

**Layer 4 — Adversarial and negative testing**

* Test repeated, reordered, interleaved, cross-scenario, cross-horizon, and cross-model-version inputs.
* Test Forecast/TTM overlap and conflicting duplicate payloads.
* Confirm deterministic behavior and no partial successful results after rejection.

**Layer 5 — Regression and full suite**

* Run the complete focused Stage 6 test set, including Prompt 39 and all existing tests covering duplicate handling, TTM accounting, metrics, baseline comparison, sufficiency, scenarios, and artifacts.

* Run the full test suite using the established project command:

  `.venv/Scripts/python.exe -m pytest src/tests/ -q`

* After any fix, rerun the affected focused tests and the full suite. Record exact collected, passed, failed, and skipped counts. Investigate all failures; do not misrepresent environmental skips as passes.

**Layer 6 — Independent diff and invariant audit**

* Re-read every changed source and test hunk.
* Independently verify that duplicate TTM observations cannot inflate counts and that legitimate distinct observations remain intact.
* Verify that the Prompt 39 cutoff guard and artifact cutoff behavior remain correct.
* Verify no changes to Stages 1–5, Stage 7, valuation, Reliability methodology, or persistence.
* Verify that tests have not been weakened, skipped, or altered to conceal failures.
* Verify no Git or remote operations were performed.

## 7. Completion and reporting

Do not stop at diagnosis or leave authorized fixes for a later prompt. Complete the correction, tests, regression run, and final diff audit before reporting.

Append one consolidated report to `temp_report.md`; never overwrite existing reports. Use this heading:

`REPORT — Stage 6 Prompt 40: Duplicate-Observation Invariant Closure`

The report must include:

1. The exact specification clauses governing duplicate observations.
2. The canonical identity used and the source establishing it.
3. Root cause of the incorrect Prompt 39 duplicate test and any implementation defect found.
4. Every changed file and the reason for each change.
5. The behavior for exact duplicates, Forecast/TTM overlap, conflicting collisions, and genuinely distinct observations.
6. The focused regression matrix and exact per-test or grouped results.
7. All six validation layers with commands and measured results.
8. Exact focused Stage 6 and full-suite collected/passed/failed/skipped counts.
9. Final diff audit and confirmation that Stages 1–5 and Stage 7 remain untouched.
10. Confirmation that Reliability remains withheld/NULL, no persistence or migration was added, and no Git/remote operations were performed.
11. Any unresolved defect or authority blocker, with the exact reason.

Use one of these final statuses:

* `READY FOR FINAL FREEZE GATE` only if the duplicate-observation violation and all other authorized defects found during this workflow are resolved, all six layers pass, and the full regression suite has zero failures.
* `BLOCKED — IMPLEMENTATION OR VALIDATION FAILURE` if any actionable authorized defect or required validation remains unresolved.
* `BLOCKED — EXPLICIT AUTHORITY REQUIRED` only if a genuine unresolved policy ambiguity cannot be resolved from the locked specification or already-delegated decisions.

Even if the result is `READY FOR FINAL FREEZE GATE`, **Stage 6 remains NOT FROZEN**. A separate independent final freeze gate is still required.
=============================================================

# Stage 6 Prompt 41 — Normalize Cutoff Identity and Revalidate Duplicate Invariants

You are the primary engineering agent for `analyzer`, a financial-data application. Financial correctness, auditability, point-in-time correctness, deterministic behavior, and explicit financial invariants are mandatory.

## 1. Objective

Resolve a newly identified Stage 6 identity-consistency risk before the final freeze gate.

Prompt 39 normalizes cutoffs for artifact-level validation. However, `src/evaluation/observation.py` currently constructs `EvaluationKey` using the raw `record.data_cutoff_datetime`. This creates a potential mismatch between:

* cutoff equality used by the Prompt 39 validation guard; and
* cutoff equality used by canonical observation identity and duplicate detection.

For example, the same instant represented once as a naive datetime interpreted under the existing UTC-normalization contract and once as an equivalent timezone-aware datetime may pass the cutoff guard as equal but fail to compare equal inside the canonical identity.

**Verify this against the current implementation before changing anything. If confirmed, fix it at the canonical identity boundary, preserve the existing authority, and complete all validation in this prompt. Do not stop after diagnosis.**

Stage 6 must remain NOT FROZEN.

## 2. Locked constraints

* Stages 1–5 remain frozen and must not be modified.
* Stage 4 remains an adapter/evidence boundary; Stage 5 must not be recalculated.
* Preserve the existing canonical `EvaluationKey` dimensions: company, metric, financial period, forecast horizon, model version, forecast cutoff, and scenario.
* Preserve the approved cutoff normalization semantics from Prompt 39.
* Preserve the authorized duplicate policy: canonical identity collisions are handled by the existing wholesale `DUPLICATE_QUARANTINED` path; never silently select a winner.
* Duplicate observations must not inflate scored observations, general valid counts, Bias-eligible counts, MAPE-effective counts, sufficiency, or baseline pairing.
* Distinct identity dimensions must remain distinct. Do not deduplicate merely because values match.
* Bear/Base/Bull, horizons, and model versions must remain isolated.
* Preserve Actual-selection and provenance rules, including eligibility of later-published Actual outcomes.
* Reliability remains withheld/NULL. Do not invent scoring mappings.
* No valuation or Stage 7 changes.
* No database table, migration, persistence backend, or unsupported durability claims.
* No Git, GitHub, remote, commit, push, pull, or branch operations.
* Do not conduct unrestricted repository-wide exploration.

## 3. Inspect the minimum necessary code

Read the exact relevant authority in `06_Stage6_Forecast_Evaluation.md`, including Sections 4, 7, 14, and 42, plus the approved duplicate and cutoff decisions recorded in `temp_report.md`.

Inspect only these relevant Stage 6 files and direct dependencies:

* `src/evaluation/observation.py`
* `src/evaluation/schema.py`
* `src/evaluation/pipeline.py`
* `src/tests/test_stage6_p39_cutoff.py`
* `src/tests/test_stage6_p40_duplicates.py`
* Existing Stage 6 tests directly covering key equality, duplicate detection, cutoff normalization, TTM accounting, and scenario/horizon/model-version separation.

Confirm the actual behavior of `evaluation_key_for`, `EvaluationKey.as_tuple()`, the cutoff normalizer, and the duplicate aggregation path.

## 4. Required implementation

If the suspected inconsistency is confirmed:

1. Ensure canonical observation identity uses the same authoritative cutoff normalization contract as the Prompt 39 guard. Equivalent instants must yield equivalent canonical cutoff identity, regardless of whether their original representation is naive UTC-normalized, timezone-aware, or a valid ISO-8601 representation accepted by the existing contract.

2. Do not weaken the cutoff guard or change its fail-closed rules. Invalid or missing cutoffs must still fail before scoring.

3. Ensure the canonical identity remains immutable and deterministic. Preserve all non-cutoff identity dimensions unchanged.

4. Keep the existing duplicate policy intact. If two observations collide after canonical normalization, the existing duplicate-handling path must quarantine the collision wholesale rather than pick a winner.

5. Ensure genuinely different instants remain different identities and that scenario, horizon, model version, company, metric, and financial period still distinguish observations as required.

6. Inspect all direct consumers of `EvaluationKey` and its tuple representation within Stage 6. Update affected callers/tests if necessary, without changing unrelated interfaces or Stages 1–5.

7. Do not add an alternate identity or a special-case workaround in only the pipeline. Fix the canonical identity contract at its proper boundary.

If the concern is not reproducible, document the exact code-level reason and prove equivalence using production-path tests. Do not make unnecessary source changes merely to create a diff.

## 5. Mandatory regression matrix

Add or update tests proving:

* Naive UTC-normalized and UTC-aware representations of the same instant produce the same canonical cutoff identity.
* Equivalent instants represented with different timezone offsets produce the same canonical identity.
* Valid equivalent ISO-8601 and datetime representations behave consistently with the existing normalizer.
* Genuinely distinct instants remain distinct identities.
* Two otherwise identical observations with equivalent cutoff representations trigger the existing duplicate quarantine behavior and cannot both contribute to aggregate counts.
* Three equivalent cutoff representations are handled deterministically, with no winner-pick.
* Reordering equivalent-cutoff inputs does not change the result.
* A repeated TTM observation represented with an equivalent cutoff cannot inflate `ttm_accounted` or any scored/effective/sufficiency/baseline count.
* Forecast/TTM overlap is detected when the only representational difference is the equivalent cutoff form.
* Distinct financial periods remain distinct even when all other values and cutoff instants match.
* Different scenarios, horizons, and model versions remain isolated.
* Missing, invalid, or mixed actual cutoff instants still fail closed under Prompt 39.
* Empty and TTM-only behavior remains correct.
* Later-published Actuals remain eligible outcomes under the approved policy.
* No rejected invocation returns a partial successful result or misleading artifact.

Assert actual identities, quarantine reasons, result values, and counts. Merely asserting that functions return or exceptions are raised is insufficient.

## 6. Mandatory six-layer validation

Complete all six layers in one continuous workflow. Fix any discovered defect and repeat affected layers plus regression validation. Do not stop at the first green run.

**Layer 1 — Unit and identity invariants**

* Test canonical cutoff normalization and key equality directly.
* Verify equivalent representations compare equal and distinct instants remain distinct.
* Verify unchanged identity dimensions.

**Layer 2 — Contract and boundary validation**

* Test missing, invalid, equivalent, and genuinely mixed cutoffs.
* Test conflicting canonical identities and confirm existing wholesale quarantine behavior.
* Verify that invalid cutoffs never enter scoring.

**Layer 3 — Production-path integration**

* Run observations through `run_evaluation_pipeline`, duplicate detection, aggregation, baseline comparison, scenario results, and artifact construction.
* Prove equivalent representations cannot bypass duplicate detection.

**Layer 4 — Adversarial and negative testing**

* Exercise reordered inputs, three-way duplicates, Forecast/TTM overlap, equivalent timezone representations, and cross-scenario/horizon/version cases.
* Verify deterministic outcomes and no partial result on rejection.

**Layer 5 — Regression and full suite**

* Run the complete focused Stage 6 suite, including all Prompt 39 and Prompt 40 tests and existing direct identity/normalization tests.

* Run the full suite using:

  `.venv/Scripts/python.exe -m pytest src/tests/ -q`

* If a test fails, investigate and fix the underlying issue; do not weaken tests or conceal failures.

* Rerun affected focused tests and the full suite after fixes.

* Report exact collected, passed, failed, and skipped counts, with reasons for skips.

**Layer 6 — Independent diff and invariant audit**

* Re-read all changed source and test hunks.
* Independently verify that cutoff normalization and canonical identity now agree.
* Verify no duplicate inflation, no arbitrary winner selection, and no accidental merging of distinct observations.
* Verify Prompt 39 cutoff completeness and artifact-cutoff behavior remain intact.
* Verify Stages 1–5 and Stage 7 remain untouched, Reliability remains withheld, and no persistence or Git/remote operations were introduced.

## 7. Reporting and completion

Do not stop after diagnosis. Complete authorized corrections, tests, regression runs, and the final diff audit before reporting.

Append one consolidated report to `temp_report.md`; never overwrite prior reports. Use this exact heading:

`REPORT — Stage 6 Prompt 41: Canonical Cutoff Identity Closure`

Include:

1. Whether the suspected inconsistency was confirmed and how it was demonstrated.
2. The authoritative normalization function and canonical identity path.
3. The root cause and exact code correction, or the evidence supporting a no-change conclusion.
4. Every changed file and the reason for each change.
5. The complete equivalent-versus-distinct cutoff regression matrix and results.
6. The six validation layers, commands, and measured outcomes.
7. Focused Stage 6 and full-suite collected/passed/failed/skipped counts.
8. The independent diff audit and confirmation that duplicate, cutoff, scenario, horizon, and model-version invariants remain intact.
9. Confirmation that Stages 1–5 and Stage 7 were untouched, Reliability remains withheld/NULL, no persistence/migration was added, and no Git/remote operations were performed.
10. Every unresolved defect or authority blocker, if any.

Choose exactly one status:

* `READY FOR FINAL FREEZE GATE` only if the suspected issue is either fixed or conclusively disproved, all authorized invariants are verified, all six validation layers pass, and the full suite has zero failures.
* `BLOCKED — IMPLEMENTATION OR VALIDATION FAILURE` if an authorized defect or required validation remains unresolved.
* `BLOCKED — EXPLICIT AUTHORITY REQUIRED` only if a genuine unresolved policy ambiguity cannot be resolved from the locked specification or existing delegated decisions.

Even if ready, Stage 6 remains NOT FROZEN. A separate independent final freeze gate is still required.
=============================================================
# Stage 6 Prompt 42 — Independent Final Freeze Gate

You are the primary engineering agent for `analyzer`, a financial-data application where correctness, auditability, point-in-time integrity, deterministic behavior, and explicit financial invariants take priority over speed.

## Mission

Perform the **independent final freeze gate for Stage 6** following Prompt 41. Decide whether Stage 6 is demonstrably safe to freeze.

This is not another implementation phase. Begin with a read-only audit. Do not assume that a previous report's READY verdict proves correctness. Verify the critical claims against the actual specification, implementation, tests, and recorded results.

If and only if this audit discovers a concrete, reproducible defect within the authorized Stage 6 scope, correct it completely and rerun the required validation. Do not stop at diagnosis, a proposed fix, or a partially passing test set.

## 1. Hard boundaries

* Stages 1–5 are frozen. Do not modify them.
* Do not modify Stage 7, valuation, or unrelated functionality.
* Do not perform GitHub, GitHub CLI/API, remote, push, pull, commit, branch, or other Git operations. Read-only local status/diff inspection is permitted.
* Do not create a database table, migration, persistence layer, or durability guarantee.
* Do not invent methodology, mappings, thresholds, weights, defaults, or financial values.
* Do not change approved D1–D5 decisions, financial formulas, quality policies, scenario separation, baseline rules, or point-in-time rules to make tests pass.
* Do not weaken, delete, skip, or rewrite existing tests merely to obtain a green result.
* Do not declare Stage 6 frozen if a material blocker remains, a required test cannot be run, or the evidence is insufficient.
* Keep the inspection narrowly scoped. Do not reload or audit the entire repository.

## 2. Required inspection scope

Read `temp_report.md` sections for Stage 6 Prompts 17–41, concentrating on the latest reports and unresolved findings from P38–P41. Use the reports as claims to verify, not as unquestionable authority.

Inspect only the relevant sections of `06_Stage6_Forecast_Evaluation.md`, especially the specification's identity, cutoff, matching, aggregation, quality, baseline, artifact, and invariant requirements.

Inspect the implementation and directly relevant tests for:

* `src/evaluation/observation.py`
* `src/evaluation/schema.py`
* `src/evaluation/pipeline.py`
* The evaluation artifact, metric, baseline, and governance modules directly called by the production evaluation pipeline
* The Stage 6 tests covering P38, P39, P40, P41, and the existing Stage 6 regression suite

Do not expand into unrelated subsystems unless a concrete dependency is necessary to verify a specific invariant.

## 3. Mandatory independent audit

Verify the following directly from code and tests:

1. **Canonical identity:** cutoff normalization used by `EvaluationKey` and the P39 cutoff guard agrees. Equivalent instants share one identity; distinct instants remain distinct. Invalid or missing cutoffs fail closed.
2. **Duplicate handling:** every same-identity collision is quarantined wholesale. No winner-picking, silent merging, order-dependent scoring, or duplicate-driven inflation is possible.
3. **TTM accounting:** repeated canonical TTM identities count once in `ttm_accounted`; duplicate observations do not inflate scored counts, MAPE/Bias eligibility, sufficiency, baseline pairing, or other aggregates.
4. **Evaluation isolation:** company, metric, financial period, horizon, model version, cutoff, and scenario are respected. Bear/Base/Bull are never pooled. No missing scenario silently defaults to Base.
5. **Forecast–Actual matching and PIT:** first-known valid Actual selection remains intact; Actual publication after the forecast cutoff is not automatically treated as input leakage; unavailable or invalid input provenance is not silently treated as clean.
6. **Financial formulas and eligibility:** Error, Percentage Error, APE, MAPE, Bias, zero-base/sign-change exclusions, independent MAPE/Bias eligible counts, and minimum-observation classifications match the approved specification. No epsilon substitution or missing-as-zero behavior.
7. **Baseline comparison:** paired observations and scenarios remain aligned. NULL or zero baseline MAPE produces the approved non-computable result and reason; no arbitrary fallback.
8. **Artifact contract:** unique run identity, distinct version concepts, methodology/quality-policy versioning, cutoff, provenance, reason codes, primary-versus-sensitivity distinction, and explicit supersession metadata are preserved. Do not claim durable immutability or persisted history when the implementation is in-memory only.
9. **Governance:** Reliability remains withheld unless authoritative numeric mappings exist; Calibration remains `NO_CALIBRATION` where required. No unauthorized scoring or valuation coupling.
10. **Boundary and regressions:** no Stage 1–5 behavior or frozen Stage 5 forecast is recalculated or altered by Stage 6.

For every item, record the exact implementation/test evidence and whether the invariant passes. A test that only checks a helper is insufficient where the production path can behave differently.

## 4. If a concrete defect is found

Do not stop after documenting it.

* Establish a failing test that reproduces the defect.
* Implement the smallest complete correction within the authorized Stage 6 boundary.
* Add adversarial regression coverage for the defect and its important neighboring cases.
* Preserve all approved methodology and frozen-stage boundaries.
* Reinspect the actual diff to ensure that no unrelated changes or weakened tests were introduced.
* Rerun all six validation layers below after the final source change.

If no concrete defect is found, keep the implementation unchanged. Do not refactor merely for style or speculative future concerns.

## 5. Mandatory six-layer validation

Complete all six layers; a single successful unit-test run is not sufficient.

* **L1 — Unit/formula:** verify canonical identity and normalization, financial formulas, eligibility, and aggregation invariants.
* **L2 — Contract/boundary:** verify invalid, missing, mixed, and conflicting data; fail-closed behavior; frozen-stage and specification boundaries.
* **L3 — Production-path/integration:** exercise the real Stage 6 pipeline, including Forecast, Actual, TTM, artifact construction, scenario isolation, and baseline integration.
* **L4 — Adversarial/negative:** test equivalent time representations, duplicate pairs and triples, reordered inputs, conflicting duplicates, distinct periods, cross-scenario/horizon/version cases, and rejected invocations that must not return partial results.
* **L5 — Regression/full suite:** run the complete Stage 6 regression suite and the full repository test suite using the repository's established local environment. At minimum, use the established command:
  `.venv/Scripts/python.exe -m pytest src/tests/ -q`
* **L6 — Independent audit:** reread the final diff and relevant source/tests after testing. Independently check for weakened tests, hidden scope changes, contradictory identity rules, count inflation, policy drift, or any mismatch between the reported results and the actual command output.

Record exact commands and collected, passed, failed, and skipped counts. Identify environmental skips individually and explain why they are not test failures. Do not report a test as passed if it was not executed. If any code changes during remediation, rerun the relevant focused tests, all six layers, and the full suite after the last change.

## 6. Freeze decision

Issue exactly one of these verdicts:

* `APPROVED FOR STAGE 6 FREEZE` — only if all required invariants are independently verified, all six layers pass, the full suite has zero failures, and no material blocker remains.
* `NOT APPROVED — DEFECT REMAINS` — if a reproducible defect remains unresolved.
* `NOT APPROVED — INSUFFICIENT EVIDENCE` — if a required test or audit cannot be completed, or evidence is inadequate.

A skipped environmental test must be disclosed. If a skip prevents verification of a material invariant, do not approve the freeze.

A freeze approval is a technical gate verdict, not permission to perform any Git or remote operation. Do not commit, push, tag, or modify branches.

## 7. Reporting

Append a new section to `temp_report.md`; never overwrite earlier reports.

Use this exact heading:

`REPORT — Stage 6 Prompt 42: Independent Final Freeze Gate`

Include:

1. Final verdict and concise rationale.
2. Files inspected and the purpose of each inspection.
3. Invariant-by-invariant audit results with specific test/source evidence.
4. Any defect found, its root cause, correction, and regression coverage—or an explicit statement that no implementation changes were necessary.
5. Exact six-layer commands and results.
6. Stage 6 focused-suite and full-suite counts, with every skip identified.
7. Final diff/scope audit, including confirmation that Stages 1–5 and Stage 7 were not modified.
8. Explicit confirmation of whether Reliability remains withheld, Calibration status is preserved, and no persistence/migration or Git/remote operation occurred.
9. Remaining blockers, limitations, or required owner decisions. Do not label any unresolved material issue as harmless.

Do not write the report until the audit and all required validation are complete. Do not claim completion if the process stopped early.

**Important:** Do not freeze Stage 6 merely because Prompts 38–41 reported READY. Freeze approval must be earned by this independent audit. If approved, state clearly that the code is approved for freeze but no Git or remote action was performed.
=============================================================

# Stage 6 — Prompt 43: Resolve Skipped-Test Evidence and Complete Final-Gate Documentation

You are working in the local repository `analyzer`, a financial-data application where correctness, auditability, deterministic behavior, and preservation of explicit financial invariants take priority over speed.

## Objective

Perform a narrowly scoped follow-up to the Stage 6 Prompt 42 Independent Final Freeze Gate.

Prompt 42 reported:

* Stage 6 test set: 307 passed, 0 failed, 0 skipped.
* Full suite: 991 passed, 0 failed, 2 skipped.
* Skipped tests:

  1. `test_codal_extraction.py:307` — “real Codal sample PDF not available in CI”.
  2. `test_ingestion_fx.py:194` — “could not import openpyxl: No module named openpyxl”.

The repository owner reports that:

* Nineteen sample CODAL PDF files are present in the repository’s `pdf` folder.
* `openpyxl` is installed in the local project virtual environment.

Do not automatically accept the two skips as unavoidable environmental limitations. Determine whether the tests are using the intended files, working directory, Python interpreter, and dependencies.

## Mandatory boundaries

1. Do not modify application source code or test code in this prompt.
2. Do not modify Stage 1–5, Stage 7, valuation logic, or any frozen component.
3. Do not create database tables or migrations.
4. Do not change Reliability or Calibration policy.
5. Do not weaken, bypass, delete, or rewrite tests to obtain a passing result.
6. Do not use GitHub, GitHub CLI/API, remotes, push, pull, commit, branch changes, or other remote Git operations.
7. Read-only local Git status and diff inspection are permitted.
8. Append a new, clearly titled addendum to `temp_report.md`. Do not overwrite or rewrite the existing Prompt 42 report.
9. Do not claim that a test passed unless it was actually executed and its result observed.
10. Keep this task limited to diagnosis, validation, and reporting. If a source or test change is needed to resolve a skip, report the exact cause and proposed minimal fix, but do not implement it in this prompt.

## Task A — Diagnose the CODAL PDF skip

1. Inspect the exact test and fixture/path-resolution logic around `test_codal_extraction.py:307`.
2. Locate and count the nineteen PDFs in the repository’s `pdf` folder. Record their actual local paths and whether they are readable. Do not dump unnecessary PDF contents.
3. Determine the exact path the test expects and how that path is constructed.
4. Check whether the test’s expected sample filename, directory, working directory, or environment condition differs from the available files.
5. Run the narrowest relevant test using the project’s intended local environment.
6. Record the exact command, interpreter/environment used, and observed result.
7. If the test remains skipped, establish the actual reason with evidence. The mere presence of PDFs does not prove they are valid fixtures for this specific test.

## Task B — Diagnose the openpyxl skip

1. Inspect the exact test and import/skip logic around `test_ingestion_fx.py:194`.
2. Identify the Python executable used to run pytest.
3. Using that same interpreter, verify whether `openpyxl` can be imported and report its installed version if available.
4. Compare this with the project’s intended virtual environment. Do not rely on a package listing from a different interpreter.
5. Run the narrowest relevant ingestion test using the intended local environment.
6. Record the exact command and observed result.
7. If the test still skips, establish why. Do not install packages, alter dependencies, or modify source/test code as part of this prompt.

## Task C — Six-layer validation evidence

Clarify the validation evidence for all six required layers:

1. Unit/formula validation.
2. Contract and boundary validation.
3. Production-path/integration validation.
4. Adversarial and negative validation.
5. Regression/full-suite validation.
6. Independent audit.

For each layer, state:

* The exact command actually executed, if one exists.
* The concrete test files or test cases that provide evidence.
* The observed pass/fail/skip counts, when available.
* Any limitation or evidence that remains unverified.

Do not invent separate layer-specific commands if those commands were not run. If one Stage 6 command covers multiple layers, explicitly say so and map the relevant tests to those layers. Clearly distinguish commands actually executed from suggested commands.

## Task D — Decide whether further validation is needed

Based on observed results:

* If the CODAL and openpyxl tests now execute successfully, record that they were exercised and passed.
* If either still skips, record the proven cause and whether it is genuinely unavoidable in the current local environment.
* If a failure occurs, preserve the failure details and report the minimal next action. Do not fix it in this prompt.
* If the targeted tests pass, run the full suite only if needed to substantiate a changed full-suite result or the final freeze evidence. Avoid unnecessary repetition of already verified expensive runs.
* Do not declare Stage 6 frozen or perform any freeze operation. Prompt 42’s freeze recommendation remains a recommendation pending this evidence clarification.

## Reporting

Append a new section to `temp_report.md` titled:

`REPORT — Stage 6 Prompt 43: Skipped-Test Diagnosis and Final-Gate Evidence Addendum`

Include:

* CODAL PDF diagnosis and evidence.
* `openpyxl` interpreter/environment diagnosis and evidence.
* Exact commands and observed results.
* Six-layer evidence mapping.
* Any unresolved blockers or required follow-up.
* A clear conclusion stating whether Prompt 42’s technical freeze recommendation remains supported, requires additional validation, or must be withheld pending remediation.

Do not retroactively alter Prompt 42’s recorded results. Distinguish the original Prompt 42 run from all Prompt 43 observations.

Finally, inspect the local diff and status to verify that only the intended report file changed. Report the exact result and explicitly confirm that no application code, test code, frozen stage, remote Git state, commit, or push was changed.
============================================================

# Stage 6 / Repository Validation — Prompt 44: Revalidate openpyxl and Close the CODAL Fixture Decision

You are working locally in `analyzer`, a financial-data application. Correctness, reproducibility, auditability, and preservation of test contracts take priority over speed.

## Objective

Reconcile the environment findings from Prompt 43 with the repository owner's latest information:

* The owner reports that `openpyxl` has now been installed in all project virtual environments.
* The repository's `pdf` directory contains 19 PDFs named `seo-codal-report (N).pdf`.
* Prompt 43 found that these PDFs do not satisfy the content contract of `test_real_codal_monthly_activity_pdf`, which specifically expects a FZAR monthly production/sales report.

This prompt is a fresh, narrowly scoped verification. Do not assume Prompt 43's environment results are still current.

## Mandatory boundaries

1. Do not modify application source code or existing tests.
2. Do not weaken, skip, delete, or rewrite any test.
3. Do not substitute an SEO PDF into the FZAR-specific regression test merely to make it execute.
4. Do not install, uninstall, or upgrade dependencies in this prompt.
5. Do not modify Stage 1–5, Stage 7, valuation, database schemas, or migrations.
6. Do not perform GitHub, GitHub CLI/API, remote Git, commit, push, pull, or branch operations.
7. Read-only local Git status/diff inspection is allowed.
8. Append a new report section to `temp_report.md`; preserve all existing reports.
9. Do not claim success without actually executing the relevant command and observing its result.

## Task A — Revalidate openpyxl after the owner's update

1. Identify the repository root and the intended Python virtual environment(s) using the actual local project configuration. Do not assume the previously reported interpreter is still the only relevant one.
2. For each relevant environment, record:

   * Exact Python executable.
   * `sys.executable`.
   * Whether `import openpyxl` succeeds.
   * Installed `openpyxl` version when import succeeds.
3. Run the following test with the intended project interpreter:

   `src/tests/test_ingestion_fx.py::test_ingest_fx_xlsx_toman_and_rial`

   Use the interpreter explicitly, e.g. `python -m pytest`, so that the test runner uses that interpreter.
4. Record the exact command, collected count, and observed outcome.
5. If the test passes, state that the dependency-related skip is resolved in that environment.
6. If it still skips, compare the actual test interpreter with the environment where the owner installed the package. Do not install anything or change project files.
7. If it fails rather than skips, preserve the actual failure details. Do not misclassify a failure as an environment skip.

## Task B — Preserve the CODAL regression contract

1. Reinspect `_candidate_real_codal_paths()` and `test_real_codal_monthly_activity_pdf` in `src/tests/test_codal_extraction.py`.
2. Confirm whether the expected `fzar_403_aban.pdf` is available anywhere in the repository or through the configured `CODAL_SAMPLE_PDF` path.
3. Do not use `seo-codal-report (1).pdf` or another SEO PDF as a replacement unless its actual contents meet the existing test's monthly-activity assertions.
4. Keep the current FZAR-specific test and its assertions unchanged.
5. If the expected fixture remains absent, retain the existing skip behavior and report the exact missing fixture/path requirement.
6. Do not add a generic test based on an untracked local PDF in this prompt. Such a test would create an undeclared dependency on the developer's local filesystem and would not be reproducible in CI.

## Task C — Validation evidence and scope

Record:

* The exact targeted commands executed and their observed outcomes.
* Whether `openpyxl` is now available to the intended test interpreter.
* Whether the FZAR-specific PDF fixture is available.
* Whether either finding requires a separate, explicitly authorized follow-up.
* The status of the six-layer Stage 6 evidence from Prompts 38–42. Do not claim that this prompt reran those six layers; this prompt does not require another Stage 6 full-suite run.

## Reporting

Append a section titled:

`REPORT — Stage 6 Prompt 44: Environment Revalidation and CODAL Fixture Closure`

Include:

* Interpreter and dependency evidence.
* Exact test command and outcome.
* CODAL fixture availability and why the provided SEO PDFs are or are not suitable for the existing test.
* Remaining follow-up, if any.
* Explicit confirmation that application code and tests were not modified and no Git remote operation was performed.

Finish with a concise status:

* `OPENPYXL SKIP RESOLVED`, or
* `OPENPYXL SKIP STILL UNRESOLVED`,
  and independently:
* `CODAL FIXTURE AVAILABLE`, or
* `CODAL FIXTURE STILL MISSING`.

Do not declare Stage 6 frozen. Do not rewrite Prompt 42 or Prompt 43 reports.
=====================================================