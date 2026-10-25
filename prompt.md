# P65 — Stage 7 D9 Parameter Governance: Decision-Preparation Audit

## Role and Project Context

You are auditing the Stage 7 valuation parameter-governance gap in the local project folder:

`analyzer`

This is a financial-data application. Financial correctness, auditability, point-in-time (PIT) correctness, deterministic behavior, and preservation of financial invariants take priority over implementation speed.

This task is an evidence-based audit and decision-preparation exercise only. You must not make financial policy decisions on behalf of the project owner.

## Authoritative Context

Treat the following files as the primary sources:

1. `stepsForStage7.md` — authoritative Stage 7 plan and unresolved D9 status.
2. `07_Stage7_Valuation.md` — Stage 7 specification, especially the previously identified relevant sections 47, 48, 65, 85, and 87.
3. `src/valuation/parameters.py` — current parameter registry, version-selection logic, legacy behavior, and related provenance metadata.

Use other files only if necessary to verify a specific claim. Do not perform a repository-wide exploration.

## Established Findings — Verify, Do Not Assume

Previous audits reported the following findings. Verify them against the specified files and correct any discrepancy with exact file and section/line references.

- `DEFAULT_REGISTRY` contains a Genesis version whose `effective_from` is `None`.
- Historical as-of selection considers dated parameter versions and fails closed when no eligible dated version exists.
- The legacy path can use current hardcoded constants, but its metadata explicitly states that historical PIT validity has not been verified.
- The valuation metadata snapshot records consumed parameter values but does not prove that those values were financially approved or historically valid.
- No authoritative project specification currently approves `2026-01-01T00:00:00Z` as the Genesis effective date.
- Existing hardcoded parameter values must not automatically be treated as financially approved merely because they are implemented in code.
- The available model does not appear to record a separate knowledge/recorded timestamp for when a parameter value became known to the system. Verify this before concluding.
- `parameter_as_of` and `data_cutoff_datetime` are separate concepts. Do not merge them or assume one supplies the other’s policy meaning without explicit contractual evidence.

## Required Investigation

### 1. Establish the exact D9 obligation

Read D9 in `stepsForStage7.md` and the relevant Stage 7 specification sections.

Explain precisely:

- What D9 requires the system to guarantee.
- Which parts are technical implementation requirements and which require an explicit financial/business decision.
- Which acceptance criteria can be verified now and which cannot be satisfied without approved parameter policy or authoritative evidence.
- Whether D9 requires only effective-dated parameter selection or also requires historical knowledge-time/recorded-time tracking. If the specification is silent or ambiguous, state that explicitly; do not invent a requirement.

### 2. Separate the decisions that must not be conflated

Analyze these questions independently:

A. **Approval of parameter values:** Are the currently implemented parameter values financially approved, or are they only provisional code defaults?

B. **Effective date:** If a parameter set is approved, from what date and time is it valid? Is there authoritative evidence supporting that date?

C. **Historical coverage:** Is the approved set valid only prospectively, or is there evidence supporting its validity for earlier dates? Do not infer historical validity from a current approval.

D. **Knowledge/recorded time:** Does the project require reconstructing what parameter values were known or recorded at a historical point in time, separately from when they were economically effective? Identify the specification evidence, or lack of it, for this distinction.

E. **Parameter-level changes:** Must all parameters in a set share one effective date, or can individual parameters change independently? Report what the existing specification actually establishes. If unresolved, flag it as a policy/schema question.

F. **Missing historical evidence:** What must the system do when a requested valuation date precedes all approved effective-dated parameter versions or when no approved historical version exists?

For each question, classify the status as one of:
- Explicitly specified and supported by evidence
- Partially specified
- Unresolved; project-owner decision required

Do not convert an unresolved question into an assumed requirement.

### 3. Assess evidence and approval requirements

Identify what evidence would be sufficient to approve a parameter version and its effective date. Distinguish:

- Project specification or signed-off financial policy
- Authoritative financial source or documented calculation
- Implementation constants and tests
- Historical source data or records
- An approval statement from the project owner

Explain what each type of evidence can and cannot establish. Tests proving that a constant is consumed correctly do not prove that the constant is financially correct.

Do not search the internet or introduce external market assumptions. Use only the repository evidence and clearly identified missing evidence.

### 4. Prepare a minimal owner decision record

Provide a compact, fillable decision-record template for the project owner. It must capture only information genuinely needed to resolve D9, including, as applicable:

- Parameter-set identifier and the exact parameter names and values being approved
- Whether approval covers current values only or also a specified historical period
- Approved effective-from date/time and its evidentiary basis
- Whether historical validity before that date is established, unknown, or unsupported
- Whether recorded/knowledge-time tracking is required
- Whether parameter validity is versioned as a whole set or per parameter
- Approval status, approving authority, and approval reference/date
- Explicit handling of valuation requests for dates without a supported parameter version

For each field, state whether it is mandatory to resolve D9 now, optional, or dependent on a confirmed specification requirement. Do not require the owner to make unrelated technical implementation decisions.

Do not fill in unknown financial values or dates. Do not prepopulate an assumed date such as `2026-01-01T00:00:00Z`.

### 5. Recommend safe behavior while decisions remain unresolved

Based on the existing specification and implementation, describe the safest behavior that preserves auditability and avoids falsely claiming PIT correctness.

Distinguish the current as-of path from the legacy path. Do not recommend weakening fail-closed behavior or silently assigning an effective date to Genesis.

If the specification does not fully define a behavior, label it as a recommendation requiring approval rather than presenting it as an existing requirement.

### 6. Define the next implementation gate

Provide explicit, testable conditions that must be met before D9 can be considered resolved and implementation or integration work can rely on the parameter registry.

Separate:
- Owner/policy approval prerequisites
- Specification/documentation prerequisites
- Code changes, if any
- Tests that the user should run later

Do not perform those future actions in this task.

## Strict Guardrails

- Do not modify any files.
- Do not write or change application code, tests, schemas, migrations, CI, or documentation.
- Do not execute tests or other project commands that change repository state.
- Do not create commits, branches, or perform GitHub, remote, push, pull, or Git operations.
- Do not invent parameter values, approval decisions, effective dates, historical coverage, or financial policy.
- Do not treat implementation behavior as proof of financial approval.
- Do not redesign `engine.py`. Its redesign remains the last Stage 7 task.
- Do not begin Stage 7 production integration as part of P65.
- Keep the investigation within the named files unless a narrowly targeted verification is essential.

## Required Report

Return a concise but complete decision brief with these headings:

1. **D9 Requirement and Evidence**
2. **Decision Matrix** — questions A–F, status, evidence, and required resolution
3. **Evidence Needed for Approval**
4. **Project-Owner Decision Record Template**
5. **Safe Behavior Until Approval**
6. **D9 Exit Criteria and Next Gate**
7. **Files Inspected and Verification Limits**

Cite exact file paths and section headings or line ranges for material findings. Clearly separate facts, interpretations, and recommendations. Identify any conflict between the specification and implementation instead of silently resolving it.

At the end, state explicitly:
- Whether D9 is resolved or remains open.
- Which specific owner decisions are still required.
- Whether any files were changed or tests were run. The expected answer for this task is **no changes and no tests**.

The report is for review in the conversation. Do not append it to repository files or create a report file.