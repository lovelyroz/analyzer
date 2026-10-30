# Prompt S7-PARAM-04 — Complete Dated and Versioned Parameter Policy

## بخش اول — دستورالعمل ایجنت (Agent Instructions)

You are working on the financial-data project `analyzer`.

Your task is to complete the remaining work for Stage 7 Objective 4:

**Determine and establish the policy, requirements, and implementation readiness for dated and versioned valuation parameters.**

This is a financial application. Financial correctness, auditability, point-in-time correctness, deterministic behavior, and preservation of financial invariants take priority over implementation speed.

### 1. Scope and restrictions

Work exclusively on Stage 7 Objective 4.

Do not start or expand work on Objectives 1–3 or 5–18.

Do not:
- Invent historical parameter values or effective dates.
- Treat the current Genesis values as historically valid.
- Assume that the current parameter values have been formally approved.
- Introduce database persistence without architectural evidence.
- Change financial formulas, thresholds, weights, or parameter values.
- Modify production code or tests in this task.
- Run tests, application commands, database commands, or Git commands.
- Repeat audits already completed unless new evidence requires it.

This prompt is **AUDIT + DECISION ANALYSIS + DOCUMENTATION ONLY**. No code changes are authorized.

### 2. Required tasks

#### T1 — Verify the current parameter-versioning implementation

Inspect the supplied source and reports and establish the exact current state of:

- ParameterRecord
- ParameterSetVersion
- ParameterRegistry
- Genesis version and its records
- Exact-key version resolution
- Date-based version resolution
- Parameter consumption and validation
- Legacy parameter-consumption behavior
- Relationship between `data_cutoff_datetime`, `parameter_as_of`, and `parameter_registry`

For every conclusion, provide file and line-level evidence.

Distinguish implemented mechanisms from policies that have not been approved.

#### T2 — Establish the required versioning policy

Analyze and provide a precise recommendation for:

- Whether existing parameter versions must be immutable.
- When a new version must be created.
- How effective dates should be assigned.
- How overlapping or ambiguous effective dates should be handled.
- Whether historical calculations must fail when no valid dated version exists.
- Whether Genesis can ever be used for historical calculations.
- How the selected parameter version should be recorded in valuation output and audit metadata.

Separate technical recommendations from decisions requiring explicit owner approval.

Do not silently treat recommendations as approved policy.

#### T3 — Determine parameter coverage

Review the parameter registry and the values used by the valuation engine.

Produce a complete classification of:

1. Parameters registered and consumed.
2. Parameters registered but not consumed.
3. Financial rules or constants consumed outside the registry.
4. Values that are not yet formally approved or whose financial definition is unresolved.

For each item, state whether it must be versioned, whether further financial approval is needed, and the evidence supporting that conclusion.

Do not expand this into a general review of valuation formulas. The purpose is only to determine versioning coverage.

#### T4 — Determine historical-data requirements

Establish exactly what evidence is required to create valid dated parameter versions.

Address:

- Actual historical parameter values.
- Actual effective dates.
- Source and approval evidence for each historical version.
- Whether the current values have a verifiable effective date.
- Whether historical versions can be reconstructed from existing project records.

Also distinguish parameter-version history from the temporal provenance of benchmark P/E observations.

Do not invent or reconstruct unsupported historical values.

#### T5 — Determine registry storage requirements

Evaluate whether the existing in-code registry is sufficient for the application's current architecture or whether persistent external storage is demonstrably required.

Base the conclusion on actual source usage and architecture evidence.

If the available files are insufficient, identify the exact additional file required and explain why. Do not explore other files without permission.

#### T6 — Produce a final completion and blocker register

Create a concise, actionable table containing:

- Requirement
- Current status: DONE / OPEN / BLOCKED
- Evidence
- Remaining action
- Responsible party: engineering / project owner / data provider
- Exact information or approval required

Separate items that can be completed through engineering work from items that cannot be completed without genuine historical data or owner approval.

### 3. Documentation updates

Append the complete report to `temp_report2.md`. Do not overwrite or remove previous reports.

Update `reply.md` with the interim report for this prompt.

Update `tasksToDo.md` only if the evidence justifies a status or acceptance-criteria change for the relevant active task, particularly S7-T007.

Update `stepsForStage7.md` only if a genuine new decision or verified finding changes the Objective 4 roadmap or completion criteria.

Do not modify `STAGE7_MASTER_WORKING_PACKET.md` unless a demonstrated inconsistency with the current authoritative roadmap must be corrected. Explain any such change.

### 4. Evidence and reporting requirements

For each task T1–T6, report:

- Files examined.
- Exact findings and supporting file/line references.
- What is already implemented.
- What remains incomplete.
- Which conclusions are recommendations rather than approved decisions.
- Which items are blocked and the exact missing evidence or approval.

Do not report an item as DONE merely because a mechanism exists or an audit was performed.

Do not claim that historical PIT correctness has been established without valid historical parameter versions and supporting evidence.

Do not claim tests passed. No tests are to be run in this task.

Stop after completing the audit and documentation updates. Do not begin implementation.

