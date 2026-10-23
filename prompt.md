# P53 — Point-in-Time (D7) Evidence Audit and Safe Remediation

You are working in the local project folder `analyzer`, a financial-data application. Financial correctness, auditability, deterministic behavior, point-in-time (PIT) correctness, and preservation of existing financial invariants are mandatory.

## Objective

Execute Stage 7 plan Step 4: resolve the Point-in-Time limitation under D7 as far as the repository's actual evidence permits.

The governing rule in `stepsForStage7.md` is:

> A cutoff date alone does not prove historical data availability. Do not claim complete PIT correctness until the required temporal evidence exists.

This is a bounded engineering task, not a repository-wide audit. Inspect the actual data lineage and temporal contracts, make safe changes only when supported by existing evidence, and explicitly identify any limitation that cannot honestly be resolved.

## Required targeted reading

1. `stepsForStage7.md` — D7 and the Stage 7 execution sequence.
2. Relevant PIT sections in `07_Stage7_Valuation.md`. This specification was previously locked; do not edit it in this task unless a concrete contradiction makes a minimal, justified correction necessary.
3. `src/valuation/engine.py`, `src/valuation/schema.py`, and `src/valuation/parameters.py`.
4. Relevant market-data and ingestion schemas/services, including the code that selects market prices and represents dates.
5. Relevant forecast schemas/services, focusing on the provenance and temporal meaning of forecast EPS.
6. Existing targeted Stage 7 and market-ingestion tests.
7. Existing Stage 7 reports only where needed to confirm previously established findings, especially the lack of a proven end-to-end production path.

Follow direct dependencies only. Do not scan the entire repository.

## Work to perform

### 1. Establish the temporal evidence available for each input

For each relevant valuation input, identify the actual source fields and trace them only as far upstream as necessary:

- Valuation/reference date.
- Market price and its observation date.
- Financial-statement facts and their reporting period.
- Publication or actual availability timestamp, if present.
- Forecast EPS and its source, creation time, or validity period, if represented.
- Historical and industry valuation benchmarks.
- Parameter/model version and any supported validity dates.

For each input, distinguish clearly between:

- **Observation or reporting date** — when the value relates to.
- **Publication/availability time** — when the value became knowable to the system or market.
- **Valuation cutoff** — the date at which the historical decision is being evaluated.

Do not treat these dates as interchangeable.

A reporting period ending before the cutoff does not prove the report was published by the cutoff. A stored record timestamp does not automatically prove the source data was publicly available then.

Respect the repository's Jalali/Shamsi date conventions. Do not introduce Gregorian conversion or change existing date contracts unless an actual, proven requirement demands it.

### 2. Verify the current PIT enforcement

Determine whether the actual valuation path:

- Receives an explicit valuation cutoff.
- Can identify the relevant historical version of each input.
- Rejects or excludes inputs whose availability after the cutoff is established.
- Handles inputs whose availability time is unknown.
- Can distinguish historical reproducibility from merely rerunning the engine with current data.
- Has a real caller that supplies the temporal evidence required by the engine.

Cite exact file paths, functions, fields, and relevant conditions in your report. Do not infer production integration from the existence of an isolated function or schema.

### 3. Make only evidence-backed remediation

If existing data already provides reliable availability timestamps and the actual execution path can enforce the cutoff safely, implement the smallest compatible correction and add focused regression tests.

Tests should cover, as applicable:

- Data available on or before the cutoff.
- Data demonstrably available only after the cutoff.
- Data with unknown availability time.
- Boundary behavior at the cutoff.
- Deterministic behavior for equivalent inputs.

Do not invent historical timestamps or fabricate data sources to make the tests pass.

If the system lacks the necessary temporal evidence, do not manufacture a timestamp, infer publication time from a reporting period, or add a warning token without an approved trigger and contract. Instead, implement any independently safe safeguards that the existing contracts support, and report the remaining limitation precisely.

Do not silently change existing valuation outputs or financial formulas merely to make PIT checks pass. If safe enforcement requires a contract decision or a missing upstream capability, leave that part unchanged and identify the exact dependency.

### 4. Preserve the existing policies and boundaries

- Do not redesign, centralize, or broadly refactor `engine.py`; its final review belongs at the end of Stage 7.
- Do not recalculate or replace Stage 5 EPS.
- Do not invent formulas, thresholds, historical data, publication times, industry mappings, or parameter validity dates.
- Do not treat a model version identifier as complete historical parameter versioning.
- Do not claim PIT correctness from a cutoff date alone.
- Do not add `POINT_IN_TIME_WARNING` or any other alert unless its trigger and output contract are already validly established.
- Do not weaken, delete, or rewrite tests merely to obtain passing results.
- Do not change unrelated locked specifications or contracts.

### 5. Validation boundaries

You must not run tests or CI. The user will execute tests and provide the actual output.

You may inspect existing tests and add or update focused tests when justified. Clearly state which tests were changed and provide exact commands for the user to run.

Do not claim that tests passed when they were not executed.

## Scope restrictions

- Work only in local `analyzer`.
- No GitHub, GitHub CLI/API, remotes, push, pull, commits, or branch changes.
- Do not edit `reply.md`, `temp_report.md`, `temp_report2.md`, `ClaudeReports/`, `stepsForStage7.md`, or `stage_7_prompts.md`.
- Do not perform a repository-wide scan.
- Do not redesign `engine.py`.
- Complete all safe, independent work before reporting; do not stop at a generic list of blockers.

## Completion report

Report:

1. The exact files inspected and changed.
2. A compact temporal-evidence table for each relevant input: observation/reporting date, availability evidence, cutoff enforcement, and remaining uncertainty.
3. The actual valuation path examined and whether it proves PIT-safe behavior.
4. Each code change and the evidence justifying it.
5. Each test added or changed, with the exact command the user should run. State explicitly that you did not run tests or CI.
6. Remaining blockers, including missing upstream timestamps or missing historical versions, with exact file/field/interface evidence.
7. Whether PIT correctness is proven, partially enforceable, or unproven, and why.
8. The next step in the existing Stage 7 plan.

Stage 7 must remain OPEN unless its full acceptance criteria are independently satisfied. Never describe missing evidence as a successful PIT implementation.