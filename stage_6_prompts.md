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
