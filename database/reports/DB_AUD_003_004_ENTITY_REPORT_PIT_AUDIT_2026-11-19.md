# DB-AUD-003 / DB-AUD-004 — Entity, ReportVersion and PIT implementation audit

**Date:** 2026-11-19  
**Branch:** `master`  
**Scope:** Read-only inspection of current tracked implementation. No ORM, schema, migration, data, code, or test changes. Tests were not run.

## Executive result

- **DB-AUD-003 — PARTIAL:** the current ORM materially exceeds or differs from the approved V1 Company/Industry contract. Industry parent-child support remains in the model; Company contains several fields excluded from the V1 fixed-identity list. The migration runner bootstraps current metadata but has no inspected dedicated Entity reconciliation/catalog-seed migration. Runtime catalog/data state was not accessible.
- **DB-AUD-004 — PARTIAL:** Report and ReportVersion have basic version numbering, publication timestamp, restatement flag, supersession pointer, and a one-current-version-per-report partial unique index. However, Report still owns a mandatory single FinancialPeriod; identity/idempotency is incomplete when CODAL tracking ID is absent; version ingestion makes the latest-ingested version current without comparing publication chronology; and no compliant PIT selector was evidenced in the inspected paths.

## Evidence inspected

1. `src/models/entity.py`
2. `src/models/report.py`
3. `src/migrations/runner.py`
4. `src/ingestion/service.py`
5. `src/ingestion/codal/adapter.py`
6. `src/ingestion/codal/ingestion.py`
7. `database/reports/DB_DES_003_REPORT_PERIOD_CONTRACT.md`
8. Master Packet §3.1, §3.3, §4.1–4.2 and Task definitions.

## DB-AUD-003 — Entity / Industry

### Observed implementation

- `Industry`: `industry_id`, unique non-null `industry_code`, non-null `industry_name`, and nullable self-FK `parent_industry_id` with `ON DELETE SET NULL`.
- `Company`: `company_id`, nullable unique `national_id`, non-null `ticker`, non-null `company_name`, non-null FK `industry_id`, nullable `codal_symbol`, nullable `fiscal_year_end`, non-null `status` defaulting to ACTIVE, non-null `is_active` defaulting true, and `created_at`.
- The approved V1 fixed Company identity is exactly `company_id`, `company_name`, `ticker`, and `industry_id`. The current model therefore has extra fields and overlapping status concepts (`status` and `is_active`); `national_id` and `codal_symbol` are not part of the approved fixed list.
- Industry's self-reference permits parent/sub-industry hierarchy even though parent/sub-industry is out of V1 scope.
- The model has no industry active/status field, despite the logical catalog description including a status attribute. This is a contract-to-model discrepancy to resolve in physical design; it is not permission to add a column.
- No uniqueness constraint on Company ticker was observed. The approved contract does not state that ticker itself is a stable company key; `company_id` is the stable identity.
- `src/migrations/runner.py` imports both models and baseline migration creates `Base.metadata`; the inspected migration list contains no explicit industry catalog seeding or Entity-contract reconciliation migration.
- The inspected CODAL persistence service accepts `company_id` and relies on a FinancialPeriod company match plus database FK behavior. No explicit pre-admission validation of an approved industry catalog or exact Company V1 identity was evidenced in this path.

### Impact / required follow-up

1. Decide how to reconcile legacy extra Company fields and Industry parent relation with the strict V1 contract without destructive deletion.
2. Confirm the authoritative seven-industry catalog seed and whether existing DBs contain unrecognized codes.
3. Inspect all Company/Industry readers, writers, imports, API/DTOs and existing database rows before proposing migration.
4. Verify that every ingestion entry point rejects missing/invalid Company and Industry, not only the CODAL persistence path inspected here.

### Data limitation

No live SQLite file, configured environment, schema snapshot, or row sample was available through this read-only GitHub file inspection. Existing parent rows, Company field population, duplicate tickers, invalid industry references, and actual catalog coverage remain unknown.

## DB-AUD-004 — Report / ReportVersion / PIT

### Observed implementation

- `Report` has `company_id`, free-text `report_type`, optional unique `codal_tracking_id`, title, mandatory `financial_period_id`, source URL, optional self-reference `original_report_id`, `is_correction`, and creation timestamp.
- The mandatory Report-level `financial_period_id` conflicts with the approved multi-period contract: a single ReportVersion can publish multiple FinancialPeriods and each FinancialFact must attach to its own actual period. The Report primary period may remain descriptive only if separately reconciled; it cannot substitute for per-fact period identity.
- `ReportVersion` has `report_id`, `version_number`, non-null `publication_datetime`, `is_current_version`, `is_restated`, optional `supersedes_version_id`, and creation timestamp.
- A unique constraint exists on `(report_id, version_number)`; a partial unique index enforces at most one current version per report.
- Migration 4 checks for multiple current versions and fails rather than silently resolving them, then creates the partial unique index. This is a useful fail-closed migration guard.
- In `ingest_codal_report`, report lookup is by `codal_tracking_id` only when that ID is supplied. Without it, each call creates a new Report; no alternate logical identity/deduplication is applied in the inspected code.
- Existing-version replay detection requires a tracking ID and matches publication datetime; it does not compare a source payload fingerprint/content hash.
- When a new version is ingested, the previous current version is demoted and the newly ingested version is marked current. The code does not compare publication datetime against existing versions before changing current status. A late-arriving older publication can therefore become current.
- `supersedes_version_id` is assigned to the last version by version_number, not based on an explicit source correction/supersession identity check. `is_restated` is a caller-supplied boolean; the inspected adapter accepts it as metadata.
- The inspected paths did not establish a PIT query that first filters by `publication_datetime <= cutoff`, then applies the approved audit/restatement rank and publication-time tie-breaker, while selecting one coherent version per Report. No claim is made that no such query exists elsewhere; full repository call-site discovery remains open.
- `src/ingestion/codal/adapter.py` remains PDF-oriented and passes report metadata into the persistence facade; this audit does not alter the separate Excel-pivot work.

### Impact / required follow-up

1. Reconcile Report's primary-period field with the approved per-Fact FinancialPeriod contract.
2. Define and enforce stable logical Report identity when CODAL tracking ID is absent, and replay identity using source fingerprint/revision evidence.
3. Make current-version semantics independent from ingestion arrival order; preserve late-arriving historical versions without incorrectly replacing the current publication.
4. Audit all PIT/read/query consumers and prove cutoff-first filtering, quality ranking, publication tie-break, unknown-status handling, and coherent per-Report version selection.
5. Inspect existing report/version rows before any migration; retain all historical versions.

## Owner decisions required — consolidated batch

The following are genuine policy choices not inferable from the inspected implementation. No answer is assumed.

1. **Company V1 strictness:** Should legacy `national_id`, `codal_symbol`, `fiscal_year_end`, `status`, `is_active`, and `created_at` be retained as compatibility/operational fields outside the four-field fixed identity, or should the physical V1 model eventually contain only the four approved fields? Recommendation: preserve existing data and classify non-identity/legacy fields separately; do not delete in the first migration.
2. **Industry catalog lifecycle:** Should Industry retain an operational active flag/status even though the current ORM lacks one, and should the seven initial codes be inserted by a versioned seed/catalog step? Recommendation: versioned idempotent seed; never silently repurpose codes.
3. **Company ticker uniqueness:** May multiple Company rows share a ticker over time/market context, or must ticker be unique in V1? Since `company_id` is the stable key and no ticker-history table is planned, recommend allowing non-unique ticker unless an explicit market-scope uniqueness rule is approved.
4. **Report primary period:** Should the legacy `Report.financial_period_id` be retained only as an optional descriptive primary-period pointer, or removed from the target logical model once Fact-level period links are complete? Recommendation: descriptive/optional only, never authoritative for all facts.
5. **Missing CODAL tracking ID:** What source-stable attributes define logical Report identity and replay when CODAL tracking ID is absent? Recommendation: require a source-stable identifier or explicitly approved composite key plus payload fingerprint; otherwise fail closed rather than invent identity.
6. **Late-arriving publication:** If an older publication is ingested after a newer version, should it be stored as historical but not current? Recommendation: yes; current/latest must be determined by valid publication chronology and approved rank, not ingestion order.
7. **Unknown audit/restatement metadata:** Confirm that a version with unknown audit/restatement status remains unresolved for automatic ranking when it could change the winner, consistent with DB-DES-003 §7.1. Recommendation: keep the existing fail-closed rule.

## Completion criteria

DB-AUD-003 and DB-AUD-004 remain PARTIAL until repository-wide call-site/read-write inventory, actual DB/schema/data inspection, and PIT selector evidence are complete. No code, ORM, schema, migration, data, or test changes were made; tests were not run.
