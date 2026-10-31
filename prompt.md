# Agent Block — Task 049 · S7-T021 · R6 Decision Resolution

You are working on the `analyzer` project, a financial-data application.

This is a **DOCUMENTATION-ONLY task**. Do not modify application code, tests, database models, migrations, or runtime behavior.

## 1. Required files

You must receive and inspect these exact files:

1. `WORKFLOW_RULES.md`
2. `STAGE7_MASTER_WORKING_PACKET.md`
3. `07_Stage7_Valuation.md`
4. `reply.md`

Do not inspect any other repository files unless you first report the exact filename and explain why it is necessary. Do not assume that an unprovided file has been inspected.

`WORKFLOW_RULES.md` defines the workflow.  
`STAGE7_MASTER_WORKING_PACKET.md` is the authoritative Stage 7 task register.  
`07_Stage7_Valuation.md` is the valuation specification.  
`reply.md` is the interim report for this execution.

## 2. Task 1 — Resolve R6 decision

**049 · S7-T021 — R6: Determine the requirement for historical parameter versions and Backtesting**

Record and apply the following technical decision:

### 2.1 Historical Backtesting scope

Historical Backtesting is **not a mandatory V1 product capability**.

It is deferred from V1 scope. Do not introduce a requirement to reconstruct historical parameter versions solely to enable a V1 Backtesting feature.

This is a scope decision, not permission to use current parameters in historical calculations.

### 2.2 Point-in-Time requirements remain mandatory

The deferral of Backtesting must NOT weaken any existing Point-in-Time, historical as-of, or temporal-provenance requirements.

Whenever the application performs a historical as-of valuation or makes a Point-in-Time correctness claim:

- It must use a genuine historical parameter version whose effective date is supported by valid evidence.
- It must use input data with sufficient temporal provenance to establish that the data was available at the relevant historical cutoff.
- Observation dates alone must not be treated as proof of publication or availability time.
- It must not substitute current parameters for missing historical parameter versions.
- It must not fabricate, backdate, or infer historical parameter vintages.
- If the required historical parameter version or temporal provenance is unavailable, the operation must fail closed or explicitly report that the historical result cannot be established.

No historical correctness or full PIT claim may be made without the necessary evidence.

### 2.3 No implicit approval of Genesis parameters

This decision does not approve any numeric Genesis parameter values.

R5 / Task 048 / S7-T020 remains OPEN until the Genesis parameter values receive a separate explicit decision supported by the required evidence.

The existence of parameter values in source code is not evidence of financial calibration or owner approval.

## 3. Task 2 — Preserve dependencies and existing decisions

Review the relevant entries in `STAGE7_MASTER_WORKING_PACKET.md` and ensure the R6 decision is consistent with the existing decisions:

- **029 · S7-T007:** remains PARTIAL. The architectural policy is documented, but genuine historical parameter vintages, numeric Genesis approval, and runtime temporal-provenance validation remain unresolved.
- **048 · S7-T020 / R5:** remains OPEN. Do not approve Genesis numeric values.
- **050 · S7-T022 / R7:** remains DONE for the architecture decision that the V1 Parameter Registry is maintained in code under Git, not in the application database.
- **051 · S7-T023 / R8:** remains DONE for the immutable model-version rule covering all output-affecting parameters.
- **052 · S7-T024 / R9-D7:** remains BLOCKED until the temporal provenance contract and required evidence are resolved.

Do not change the status or scope of these Tasks merely because R6 has been decided.

In particular, do not mark Task 029 as DONE.

## 4. Task 3 — Update authoritative documentation

Update `STAGE7_MASTER_WORKING_PACKET.md`:

1. Replace the unresolved R6 decision wording under **049 · S7-T021** with the approved decision.
2. Mark Task 049 as `[x]` / DONE only for its actual scope: determining and documenting whether historical Backtesting is required.
3. Explain that Backtesting is deferred from V1, while historical as-of and PIT requirements remain subject to genuine historical parameter versions and temporal provenance.
4. Explicitly state that this decision does not close Task 029, approve R5, or resolve R9/D7.
5. Update any relevant task-status summary or dependency reference in the Master Packet so it does not continue to describe R6 as awaiting an owner decision.
6. Preserve all unrelated task statuses, numbering, identifiers, and historical evidence.

Review `07_Stage7_Valuation.md` for relevant references to Backtesting, historical parameters, and PIT. If an inconsistency with the approved R6 decision exists, correct only that inconsistency. Do not weaken existing financial or PIT requirements.

Do not make unnecessary edits to the specification.

## 5. Task 4 — Record the execution report

Append a concise, evidence-based report to `reply.md`.

The report must include:

- **049 · S7-T021 — R6**, with its final status.
- The exact decision recorded.
- Files changed.
- Relevant sections/headings updated in each file.
- Confirmation that R5 remains OPEN.
- Confirmation that 029 remains PARTIAL.
- Confirmation that R7 and R8 remain DONE within their documented architectural scope.
- Confirmation that R9/D7 remains BLOCKED.
- Any inconsistency found and how it was resolved.
- Any unresolved issue or missing evidence.

Do not claim that historical parameter vintages, Backtesting, or runtime PIT have been implemented or verified.

## 6. Strict scope restrictions

This task is documentation-only.

- Do not modify Python source code.
- Do not modify tests.
- Do not modify database models or migrations.
- Do not create historical parameter versions.
- Do not approve or alter Genesis numeric parameters.
- Do not implement Backtesting.
- Do not change runtime PIT behavior.
- Do not modify Forecast persistence Tasks **053–057**.
- Do not change unrelated Task statuses.
- Do not run tests.
- Do not claim that tests passed.
- Do not perform GitHub operations, commits, pushes, or branch changes.

If a required conclusion cannot be supported by the supplied files, report the exact missing evidence instead of guessing.

## 7. Required final report format

Return the results using these exact task identifiers:

1. **049 · S7-T021 — R6**
2. **029 · S7-T007 — Dependency status**
3. **048 · S7-T020 — R5 status**
4. **050 · S7-T022 — R7 status**
5. **051 · S7-T023 — R8 status**
6. **052 · S7-T024 — R9/D7 status**

For every item, state one of:

`DONE`, `PARTIAL`, `NOT DONE`, or `BLOCKED`

Provide concrete documentation evidence for each status.

Finish with:

- Files changed
- Files not changed
- Confirmation that no code or tests were modified
- Confirmation that no tests were run
- Any remaining blockers

Do not declare Stage 7 complete. This task resolves R6 only.