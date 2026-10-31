# Stage 7 — Package 1: Close Open Decisions and Contracts

## Agent Instructions

You are working on the financial-data application repository:

`lovelyroz/analyzer`

This is a financial application. Financial correctness, auditability, point-in-time correctness, deterministic behavior, and preservation of financial invariants take priority over convenience or implementation speed.

### 1. Work classification

**This is a documentation and contract-audit task.**

- No production code changes.
- No test code changes.
- Do not run tests.
- Do not modify formulas, thresholds, financial parameters, or runtime behavior.
- Do not invent missing financial definitions, dates, provenance, calibration evidence, or data sources.
- Do not create additional report files.
- The only authoritative Stage 7 status document is `STAGE7_MASTER_WORKING_PACKET.md`.

At the end, provide exact test commands only if you identify a specific future implementation that requires testing. Do not execute them.

### 2. Required files

The following files are explicitly provided and are the permitted inspection scope:

1. `STAGE7_MASTER_WORKING_PACKET.md`
2. `WORKFLOW_RULES.md`
3. `07_Stage7_Valuation.md`
4. `src/valuation/parameters.py`
5. `src/valuation/engine.py`
6. `src/valuation/schema.py`
7. `src/valuation/models.py`

Inspect only these files.

If another file is genuinely necessary, do not search for it independently. Report its exact path and explain why it is required. Wait for it to be provided.

### 3. Authoritative rules

- `STAGE7_MASTER_WORKING_PACKET.md` is the sole authority for Stage 7 task status, decisions, dependencies, execution order, and exit criteria.
- `WORKFLOW_RULES.md` governs the workflow.
- `07_Stage7_Valuation.md` is the Stage 7 specification and must be checked for consistency with the Master Packet.
- Existing code values are not proof of financial approval.
- An audit finding does not automatically complete the corresponding implementation task.
- `BLOCKED` must never be reported as `DONE`.
- Do not repeat or reopen decisions already completed in Tasks 049, 050, and 051.

### 4. Tasks

#### Task 1 — 029 · S7-T007: Parameter versioning, D9 and PIT contract

Audit the current documentation and the supplied parameter/valuation implementation.

Verify the following rules:

1. Parameter Registry is maintained in code and version-controlled through Git, not stored in the application database.
2. Historical parameter versions require evidence-backed `effective_from` dates.
3. Inventing or backdating effective dates is prohibited.
4. Undated Genesis must never be selected as a historical parameter version.
5. Missing historical versions must fail closed; current parameters must not silently substitute for historical versions.
6. Every parameter that materially affects the valuation output must belong to an immutable model version.
7. A material parameter change requires a new model version.
8. Numeric Genesis values are not financially approved merely because they exist in the source code.

Inspect the supplied implementation to establish what is actually enforced and what is only documented.

Explicitly distinguish:
- Implemented mechanism
- Documented policy
- Missing historical evidence
- Missing runtime enforcement
- Items that cannot be proven from the supplied files

**Decision to record:** Current Genesis numeric values remain unapproved for financial use. They may remain available for technical execution and testing, but must be explicitly labelled provisional/unapproved. No calibration or historical validity claim is permitted.

Do not change any numeric values or parameter implementation.

Acceptance:
- The Master Packet accurately distinguishes the implemented registry mechanism from missing historical vintages and runtime PIT evidence.
- No historical validity is claimed without evidence.
- Task 029 remains PARTIAL unless all of its original acceptance conditions are genuinely satisfied.

#### Task 2 — 030 · S7-T008: Alert and input contracts

Audit the alert and input contract decisions against the supplied specification and implementation.

Preserve these decisions:

1. D1–D5 remain deferred/inactive in V1. Do not invent triggers, formulas, thresholds, severities, or missing-data behavior.
2. D6 remains limited to the existing EPS and TARGET_PE drivers in V1.
3. Sector-specific drivers and formulas, including Bank and Holding formulas, remain deferred until valid financial definitions and supporting evidence exist.
4. D6 must not be described as fully resolved.
5. D7 requires actual temporal provenance. Observation date alone does not prove publication or availability.
6. D8 uses the existing canonical V1 alert vocabulary.
7. OA1.5 and OA1.6 are active implementation requirements, not merely documentation requirements. Their implementation belongs to the later OA1 implementation package.
8. Missing eligible market price must fail closed.
9. If an older eligible market price is used, its actual Jalali observation date must be reported.

Check whether the current documentation contradicts these rules or incorrectly presents deferred behavior as implemented.

Do not activate deferred behavior or change the alert engine.

Acceptance:
- The specification and Master Packet consistently describe the current V1 contract.
- D6 remains explicitly unresolved/deferred.
- OA1.5/OA1.6 are not marked implemented merely because their requirements are documented.
- Task 030 remains PARTIAL while D6 is unresolved.

#### Task 3 — 048 · S7-T020: Formal Genesis approval decision (R5)

Review the Genesis parameter definitions and the available evidence in the supplied files.

The decision is:

**Do not approve the current numeric Genesis parameter set as financially calibrated or validated.**

Reasons:
- Presence in source code is not financial validation.
- No calibration study, validated backtest, or sufficient source-backed calibration evidence is supplied.
- The values may remain provisional for technical execution and testing.
- No claim of financial approval, historical validity, or calibration quality is permitted.

Record this decision clearly in the Master Packet.

Do not modify the numeric parameters.

Do not invent a calibration study or claim that one exists.

Acceptance:
- Task 048 records the explicit non-approval decision and its rationale.
- The decision does not falsely imply that the parameter values have been recalibrated.
- Task 029 remains PARTIAL because historical vintages and runtime PIT evidence are separate requirements.

#### Task 4 — 052 · S7-T024: Temporal provenance contract for Benchmark P/E (R9/D7)

Formalize the technical responsibility boundary as follows:

**Caller responsibilities**
- Supply the benchmark observations and their source-backed provenance.
- Supply company identity.
- Supply Jalali observation date.
- Supply financial-period identity.
- Supply traceable source references and source/version/revision identifiers where available.
- Supply publication/availability timestamp evidence whenever historical point-in-time validity is claimed.
- Supply sufficient linkage between the relevant EPS and market-price observations.

**Stage 7 responsibilities**
- Validate that required provenance fields are present and internally consistent.
- Validate that the benchmark belongs to the correct company and financial period.
- Reject or fail closed when required provenance is missing, contradictory, or insufficient.
- Never infer publication or availability time from observation date alone.
- Never silently accept an unproven precomputed historical P/E series as valid PIT evidence.

Important:
This responsibility split defines the contract. It does not establish that real historical provenance data currently exists or that runtime validation is already implemented.

Audit the supplied files to determine:
- Which parts of this contract are already documented.
- Which parts are actually enforced in code.
- Which parts are missing.
- Which evidence is unavailable.

Acceptance:
- The Caller/Stage 7 responsibility boundary is unambiguous.
- No full PIT capability is claimed without actual temporal evidence and runtime validation.
- Task 052 remains BLOCKED if required external evidence or implementation is still absent.
- Task 029 remains PARTIAL as appropriate.

### 5. Documentation updates

After completing the audit:

1. Update `STAGE7_MASTER_WORKING_PACKET.md` as the sole authoritative status document.
2. Update `07_Stage7_Valuation.md` only where necessary to make its contracts consistent with the decisions above.
3. Do not create a new report file.
4. Do not change unrelated sections.
5. Preserve historical information where useful, but clearly label superseded or inactive rules.
6. Do not change the status of unrelated tasks.
7. Do not mark any task DONE solely because its decision has been documented.

The Master Packet must retain the exact task numbers and IDs:

- 029 · S7-T007
- 030 · S7-T008
- 048 · S7-T020
- 052 · S7-T024

### 6. Required final report

Provide a separate report for each task:

**029 · S7-T007**
- Status: DONE / PARTIAL / NOT DONE / BLOCKED
- Findings
- Evidence from supplied files
- Documentation changes
- Remaining blockers

**030 · S7-T008**
- Status: DONE / PARTIAL / NOT DONE / BLOCKED
- Findings
- Evidence from supplied files
- Documentation changes
- Remaining blockers

**048 · S7-T020**
- Status: DONE / PARTIAL / NOT DONE / BLOCKED
- Decision recorded
- Evidence and rationale
- Documentation changes

**052 · S7-T024**
- Status: DONE / PARTIAL / NOT DONE / BLOCKED
- Caller responsibilities
- Stage 7 responsibilities
- Actual implementation evidence
- Missing evidence and blockers

Also report:

1. Exact files changed.
2. Exact files inspected.
3. Confirmation that no production code or tests were changed.
4. Confirmation that no tests were executed.
5. Any additional files required, with exact paths and reasons.
6. Any remaining contradictions between the Master Packet and Stage 7 specification.
7. The updated Master Packet task statuses.

Do not claim that Package 1 or Stage 7 is complete unless the relevant acceptance criteria are actually satisfied.