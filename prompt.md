# EXECUTION PROMPT — Task 015 / DB-ING-002
## Canonical ingestion admission and persistence alignment — safe implementation increment

**Repository:** `analyzer`  
**Branch:** `master`  
**Authority:** `database/DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md`  
**Related implementation:** Task 014 / DB-ING-001

### Work mode
CODE IMPLEMENTATION + focused tests + evidence report.

This is an execution task, not a general audit. Implement the safe parts of DB-ING-002 that can be completed without changing the database schema or violating the approved architecture.

### 1. Required objective

Advance Task 015 by implementing a deterministic, fail-closed boundary between `CanonicalInputCandidate` and the existing canonical ingestion/persistence contracts.

The boundary must address:

- Complete-batch admission before any persistence is attempted.
- Required identity and provenance validation.
- Duplicate versus conflicting economic facts.
- Correction/report-version identity and preservation of prior versions.
- `OTHER_*` handling only where an explicit approved identity exists.
- `ZERO_FALLBACK` remaining distinguishable from an actual reported zero.
- Prohibition of raw-row and calculated-fact persistence.
- Atomicity requirements and explicit transaction ownership.

### 2. First inspect the exact current implementation

Read only the relevant files needed to establish the actual contracts, including:

- `src/ingestion/excel/canonical_input.py`
- `src/ingestion/excel/deterministic_matcher.py`
- `src/ingestion/service.py`
- `src/ingestion/codal/` relevant ingestion modules
- `src/models/normalized.py`
- `src/models/report.py`
- `src/models/period.py`
- `src/models/ingestion_run.py` (or the actual IngestionRun model location)
- Relevant identity, transaction and existing ingestion tests.
- `database/reports/DB_DES_001_CANONICAL_INPUT_CONTRACT.md` or the actual current DB-DES-001 contract location.
- `database/reports/DB_DES_005_INGESTION_ATOMICITY_CONTRACT.md`
- `database/reports/DB_DES_006_CODAL_CANONICAL_INGESTION_PIPELINE.md`

Do not assume filenames or model fields without reading their current definitions.

### 3. Implementation requirements

Implement a pure, deterministic admission/preparation component that accepts a complete batch of canonical candidates and produces either:

- A fully validated immutable persistence plan; or
- A deterministic rejection containing stable diagnostic codes.

At minimum:

1. Reject the entire batch if any candidate is invalid.
2. Never silently discard an invalid or ambiguous candidate.
3. Never convert missing values into zero.
4. Preserve actual zero separately from `ZERO_FALLBACK`.
5. Do not create or persist derived/calculated financial facts.
6. Do not persist raw workbook rows or raw observations.
7. Preserve company, report, report-version, period, Metric, unit/currency/scale and approval-reference identities.
8. Distinguish an identical existing economic fact from a conflicting payload.
9. Do not overwrite a conflicting existing fact.
10. Do not replace or delete previous report versions when a correction arrives.
11. Do not infer correction status, audit status, publication time or revision identity.
12. Make transaction ownership explicit: the preparation/admission layer must not commit or open a database transaction.

If the existing physical models cannot safely represent a required identity or invariant, reject that persistence path explicitly and document the exact incompatibility. Do not fabricate a workaround.

### 4. Schema and database restrictions

**Absolutely prohibited in this task:**

- ORM model changes.
- Schema changes.
- New or modified migrations.
- Database creation or modification.
- Running real ingestion.
- Writing to the owner's database.
- Changing `WORKFLOW_RULES.md`.
- Reopening already-approved owner decisions.

Migration 9 remains unresolved. Do not create Migration 10 or attempt to resolve Migration 9.

Do not claim production persistence is complete merely because a pure plan builder or synthetic test passes.

### 5. Tests

Add focused synthetic tests for:

- Fully valid batch.
- One invalid candidate rejects the complete batch.
- Identical duplicate versus conflicting payload.
- Explicit zero versus missing value.
- `ZERO_FALLBACK` versus actual zero.
- Correction version does not erase the previous version.
- Missing or ambiguous identity.
- Prohibited raw/calculated persistence.
- No commit/transaction side effects from the pure boundary.
- Deterministic output and stable diagnostics.

Use existing project test conventions. Do not run tests; the owner runs them.

### 6. Scope discipline

Do not spend this task repeating broad repository audits. Do not modify Task 014 unless a concrete integration defect prevents this task from proceeding; report such a defect with exact evidence instead.

Do not connect unapproved Parsian templates or production semantic mappings.

### 7. Required deliverables

1. Implemented pure admission/persistence-plan boundary, if compatible with the existing contracts.
2. Focused synthetic tests.
3. Report:
   `database/reports/DB_ING_002_CANONICAL_INGESTION_ALIGNMENT.md`
4. Update `reply.md`.
5. Update the relevant Task 015 entry and progress dashboard in the Master Packet only if the Task status genuinely changes.

The report must include:

- Exact changed-file list.
- Implemented behavior.
- Stable rejection codes.
- Test command for owner execution.
- Exact incompatibilities between the persistence plan and current ORM/schema.
- Which parts of DB-ING-002 remain open.
- Whether any production writer was actually connected (do not imply that it was if it was not).

### 8. Completion criteria

Task 015 must remain PARTIAL unless all required canonical persistence behavior is implemented and validated against an approved physical schema.

A pure preparation boundary is measurable progress, but it is not production persistence.

Do not mark `[x]` or DONE on the basis of synthetic tests alone.

At the end, report exactly:

- `DONE`
- `PARTIAL`
- `NOT DONE`
- `BLOCKED`

for Task 015, with evidence and remaining work.