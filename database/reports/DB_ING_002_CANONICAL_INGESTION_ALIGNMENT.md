# DB-ING-002 — canonical ingestion admission and persistence alignment

**Task:** 015  
**Status:** PARTIAL  
**Date:** 2026-11-20

## Result

Added a pure, deterministic admission boundary in `src/ingestion/canonical_admission.py`. It accepts a complete tuple/list of `CanonicalInputCandidate` submissions plus explicit revision context and immutable snapshots of existing versions/facts. It either returns a frozen logical plan or rejects the complete batch with sorted, stable diagnostics. It has no ORM/session imports and cannot execute persistence. The plan explicitly records `transaction_owner=CALLER`, `atomicity_unit=REPORT_VERSION`, `execution_allowed=False`, and `physical_persistence_compatible=False` (`PHYSICAL_SCHEMA_INCOMPATIBLE`).

Focused synthetic tests were added in `src/tests/test_canonical_ingestion_admission.py`. **Tests were not run**, as PROMPT.md assigns execution to the owner. Owner command:

```powershell
.\.venv\Scripts\python.exe -m pytest -q --basetemp .pytest_task015_20261120 src/tests/test_canonical_ingestion_admission.py src/tests/test_excel_canonical_input.py
```

## Implemented behavior

- Admission is all-or-nothing. Missing or malformed context, candidate identity, source value, provenance, approvals or period causes rejection; no candidate is silently omitted.
- Source revision and artifact hash are explicit inputs. Correction identity is explicit through a new version and optional `supersedes_version_id`; neither correction status, publication time, audit state nor revision identity is inferred. Existing versions are only referenced and preserved.
- Fact identity in the logical plan is report-version + temporal period + Metric + dimensions. Identical duplicate submissions collapse deterministically; different payloads at the same identity reject. Replays against supplied existing snapshots are accepted as unchanged only when payload, revision, standard and source identity agree. Conflicts and incomplete replays reject.
- Exact source Decimal is retained, with the logical signed-64-bit integer computed using `ROUND_HALF_UP` and range checked. A source-reported zero remains `SOURCE_REPORTED`. `ZERO_FALLBACK` is a distinct origin and requires a blank source value, exact zero, and a unique explicit approved rule for the candidate Metric. Missing values are never automatically changed to zero.
- An `OTHER_*` Metric requires a unique explicit approved selection whose identity exactly matches that Metric. Raw-row and calculated submissions have explicit prohibition codes.
- The plan contains canonical identities, source/revision/artifact and template identities, period and duration basis, unit/currency/scale, value origin, and approval references; it excludes source text and cell/workbook-row observations.
- No connection to the legacy CODAL writer or database is made. This code opens no transaction and performs no commit. A future writer must own the DB-DES-005 `REPORT_VERSION` atomic unit: durable STARTED audit, validate complete batch, atomically write Report/Version/facts/audit COMPLETED, and record FAILED separately after rollback.

## Stable rejection codes

`BATCH_EMPTY`, `BATCH_CONTEXT_INVALID`, `CANDIDATE_TYPE_INVALID`, `RAW_ROW_PROHIBITED`, `CALCULATED_FACT_PROHIBITED`, `IDENTITY_MISSING`, `APPROVAL_REFERENCE_MISSING`, `MAPPING_AMBIGUOUS`, `REPORT_VERSION_MISMATCH`, `COMPANY_MISMATCH`, `SOURCE_ARTIFACT_MISMATCH`, `CANDIDATE_INVALID`, `VALUE_MISSING`, `VALUE_INVALID`, `SOURCE_NUMBER_MISMATCH`, `SOURCE_FLOAT_PRECISION_UNAVAILABLE`, `ZERO_FALLBACK_INVALID`, `ZERO_FALLBACK_APPROVAL_MISSING`, `OTHER_APPROVAL_MISSING`, `INTEGER_RANGE_EXCEEDED`, `INTRA_BATCH_CONFLICT`, `EXISTING_FACT_CONFLICT`, `EXISTING_VERSION_CONFLICT`, `SOURCE_REVISION_REUSED`, `SUPERSESSION_TARGET_MISSING`, `SUPERSESSION_IDENTITY_INVALID`, and `ZERO_FALLBACK_SOURCE_UNSUPPORTED`.

Diagnostics are deduplicated and sorted by code and identity, so rejection output does not depend on candidate ordering. Duplicate economic payloads now collapse only when complete plan provenance also matches: template ID/version/hash, source label/header identities and their approval references, extraction owner, and all other identity/reference pairs. Different provenance rejects with `DUPLICATE_PROVENANCE_CONFLICT`; no first-candidate provenance is selected or merged away. Existing-fact replay equality includes the same provenance.

Additional stable codes for this correction: `DUPLICATE_PROVENANCE_CONFLICT` at the batch boundary and `ZERO_FALLBACK_APPROVAL_INVALID` at the candidate builder boundary.

## Correction update — duplicate provenance and ZERO_FALLBACK builder path

`PlannedFact` retains extraction owner and exposes a normalized provenance key. The admission duplicate-collapse path compares both economic payload and that key. Synthetic cases cover a different template hash, a different header approval, a different label approval, and a different extraction owner; each is evaluated in both input orders and expects identical diagnostics. The old identical duplicate and conflicting-value cases remain.

The Excel builder now accepts an optional `zero_fallback_rule`. With no rule, BLANK still fails with `SOURCE_VALUE_MISSING`; a rule must be approved, unique, carry an approval reference, and match the selected Metric. Only then can it produce a candidate whose source kind remains `BLANK`, with no source text/native number and a logical Decimal zero. `build_candidate_submission()` binds that candidate to `ValueOrigin.ZERO_FALLBACK` and the exact rule. Populated cells reject a supplied fallback rule. A builder-to-submission-to-batch synthetic test exercises this full path and checks reported zero remains separate. This is a narrow, backward-compatible extension to the Task 014 builder boundary required to avoid manufacturing source evidence.

## Physical incompatibilities and open work

The logical plan is **not compatible with production persistence on the current ORM/schema**:

1. `NormalizedFinancialFact` uses `value_irr Numeric(30,4)` and a uniqueness key on `(company_id, period_id, metric_id, source_report_version_id)`. It does not represent the plan's canonical signed integer, explicit value origin/state, dimensions in the logical key, source currency/unit/scale, extraction-standard identity, or approval/provenance references. Its current raw/mapping foreign keys are optional and do not provide the required canonical identity.
2. `FinancialPeriod` stores Gregorian `Date` endpoints and period-wide `is_ytd`; it does not encode the Jalali period tuple plus the per-fact temporal type/duration basis required by the plan and DB-DES-011.
3. `ReportVersion` has version/publication/current/restatement/supersedes fields but no explicit source revision identity and source artifact hash to enforce the plan's idempotency boundary. `IngestionRun` does not supply the full required source/standard revision identity either.
4. The existing CODAL ingestion path writes raw financial facts and commits independently; it does not implement this boundary or DB-DES-005's report-version atomicity. It was not modified or invoked.

Accordingly the new plan sets `physical_persistence_compatible=False` and cannot be submitted to an ORM writer. Migration 9 remains unresolved. Open work includes approved physical schema/migration decisions, complete model mapping for these identities/invariants, authenticated approval resolution, writer integration with DB-DES-005 transaction/audit semantics, and owner-run execution of the focused suite. The original admission increment did not modify Task 014; this correction makes only the documented, backward-compatible builder extension for approved BLANK fallback. No Parsian template or production mapping was connected.

## Changed files

- `src/ingestion/canonical_admission.py` — pure admission and logical-plan boundary.
- `src/ingestion/excel/canonical_input.py` — explicit rule-gated BLANK candidate construction.
- `src/tests/test_canonical_ingestion_admission.py` — synthetic focused coverage; not executed.
- `database/reports/DB_ING_002_CANONICAL_INGESTION_ALIGNMENT.md` — this evidence report.
- `database/DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md` — Task 015 status, dashboard and evidence entry.
- `reply.md` — execution note.

No ORM, schema, migration, database, workbook, unrelated Task 014 behavior or production writer was changed or used. The narrow fallback-gated builder extension is described above.

**Final Task 015 status: PARTIAL.** Evidence: pure non-executable admission plan and synthetic tests added. Remaining: physical schema approval/compatibility, production writer and atomicity integration, and owner-run tests.

Correction update changed six files: `src/ingestion/canonical_admission.py`, `src/ingestion/excel/canonical_input.py`, `src/tests/test_canonical_ingestion_admission.py`, this report, `database/DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md` (evidence wording only; status/dashboard unchanged), and `reply.md`. Tests were not run.
