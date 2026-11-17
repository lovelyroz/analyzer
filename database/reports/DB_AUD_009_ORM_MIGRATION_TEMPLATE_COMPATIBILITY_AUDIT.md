# DB-AUD-009 — ORM and Migration Compatibility Audit for Company Table Layout Template

**Status:** AUDIT COMPLETE — findings and implementation constraints; no code or schema changes  
**Date:** 2026-11-18  
**Scope:** Existing SQLAlchemy models, schema bootstrap, and ordered migration runner relevant to DB-DES-008  
**Compared design:** `DB_DES_008_COMPANY_TABLE_TEMPLATE_RELATIONAL_SCHEMA_PROPOSAL.md`

## 1. Executive result

The current repository has reusable Company, Report, ReportVersion, FinancialPeriod, and FinancialMetric entities, but **no existing ReportType catalog and no Company Table Layout Template / worksheet / table-layout entities**.

The project uses a custom ordered migration runner (`src/migrations/runner.py`) with migrations 1–8. The inspected source tree contains no Alembic environment or revision history. New schema work must extend the existing runner; do not introduce Alembic as a parallel migration system.

DB-DES-008 is broadly compatible with the current SQLAlchemy/SQLite architecture, but its logical key `company_id + report_type_id` cannot be implemented as written until ReportType is normalized. The current `reports.report_type` is a free-text `VARCHAR(100)`, not a foreign key.

## 2. Existing reusable ORM entities

| Existing entity / table | Current contract | Relevance to Template |
|---|---|---|
| `Industry` / `industries` | Integer PK; unique `industry_code`; Company points to it | Reuse as-is; no Template-specific industry FK is needed |
| `Company` / `companies` | Integer PK; non-null FK `industry_id`; ticker and company identity fields | Direct FK target for `company_table_template.company_id` |
| `Report` / `reports` | Integer PK; FK `company_id`; free-text `report_type`; FK `financial_period_id` | Reuse, but report-type normalization is a prerequisite for the proposed `report_type_id` |
| `ReportVersion` / `report_versions` | Integer PK; FK `report_id`; version number; publication datetime; restatement/current flags; self-FK supersedes | Natural historical attachment point for the exact Template version used during extraction |
| `FinancialPeriod` / `financial_periods` | Integer PK; FK `company_id`; period type and date/fiscal attributes | Reuse for reporting-period semantics; do not duplicate period fields in Template metadata |
| `FinancialMetric` / `financial_metrics` | Canonical metric catalog, unique metric code, industry/parent references | Reuse only in the later semantic mapping layer; it is not a physical Excel column-slot model |

### Important provenance limitation

The current `ReportVersion` model has no source-workbook SHA-256, source artifact fingerprint, or Template-version reference. `Report` has a `source_url`, but that is not equivalent to an immutable workbook fingerprint or exact extraction-template provenance.

DB-DES-008's proposed `source_workbook_sha256` on TemplateVersion remains necessary. A separate decision is required on the ReportVersion-to-TemplateVersion link.

## 3. Existing structures that must not be repurposed

- `RawFinancialFact` contains `source_section`, `source_row`, and `source_column`; these are coarse fact provenance fields, not a versioned worksheet/table layout model. Do not overload them to store template definitions or extraction spans.
- `MappingRule` and `MappingDecision` describe fact mapping decisions; they do not represent physical Header inheritance, column slots, or positive Gray extraction spans.
- `IngestionRun` is operational run tracking, not a template/version entity.
- Existing `FinancialMetric` is semantic. Do not use it as the identity of a physical column or table node.

No existing ORM table found is a safe substitute for the proposed Template entities.

## 4. Migration architecture and constraints

### 4.1 Current mechanism

- `src/migrations/runner.py` defines a custom `Migration(version, name, apply)` sequence.
- Current ordered migrations are versions **1 through 8**:
  1. baseline schema;
  2. mapping and derived schema;
  3. normalized fact multi-source provenance;
  4. one current ReportVersion per Report;
  5. Jalali components on MarketDaily;
  6. Jalali components on FXRate;
  7. forecast version repository;
  8. removal of forecast output persistence.
- Applied versions are recorded in `schema_migrations`.
- Baseline creation uses `Base.metadata.create_all`; later changes are explicit migration functions.
- All ORM models are imported in the runner before metadata-based table creation. Any new model modules must be imported there.
- `src/core/database.py` enables SQLite foreign-key enforcement on each connection using `PRAGMA foreign_keys=ON`.

### 4.2 Consequences for the Template implementation

1. Add new ORM model modules to the runner's import list before using metadata-based table creation.
2. Add a new migration after version 8; do not edit historical migration behavior.
3. Prefer additive table creation and nullable/backfillable additions. Avoid destructive alteration of existing Report/ReportVersion records.
4. Existing migration runner uses SQLite-specific SQL and already creates a partial unique index for current ReportVersion. A partial unique index for one APPROVED TemplateVersion per logical Template is consistent with the current approach, subject to the project's supported SQLite version.
5. SQLite foreign-key enforcement is already enabled, but composite ownership constraints and any required parent/child consistency still need explicit schema design and tests.
6. There is no Alembic revision chain to reconcile.

## 5. Required design adjustments before implementation

### 5.1 Normalize ReportType first

DB-DES-008 requires `report_type_id`, but the current database has only `reports.report_type VARCHAR(100)`.

Recommended direction:
- introduce a controlled `report_types` catalog with a stable integer PK and unique stable code;
- add a nullable `report_type_id` FK to `reports` in an additive migration;
- backfill only through an explicit, reviewed mapping from existing distinct `reports.report_type` values to canonical codes;
- retain the legacy text column during transition; do not silently infer or fuzzy-normalize unknown values;
- enforce non-null for new canonical ingestion at the application/contract boundary until a safe database-wide migration can guarantee all legacy rows are mapped.

Do not create Template identities against free-text report-type labels: spelling variants would split logical templates or create accidental collisions.

### 5.2 Attach exact Template version to ReportVersion

Recommended direction: add a nullable FK `template_version_id` to `report_versions` (or a narrowly scoped association table only if one ReportVersion genuinely needs multiple Template versions).

Rationale:
- Template choice is an extraction-provenance fact for a specific report version;
- keeping the reference on ReportVersion allows historical report versions to retain the exact immutable layout version used;
- existing records can remain NULL during migration;
- new CODAL Excel ingestion must populate the reference before facts are accepted.

The write path must validate that the referenced TemplateVersion belongs to the same company and ReportType as the parent Report. A plain FK does not enforce this cross-table semantic consistency; decide whether to implement a composite FK/unique key or a strict transactional service-level validation. Do not silently accept mismatches.

### 5.3 Do not add `active_version_id` now

The existing ReportVersion model already demonstrates the project's partial-unique-index pattern. For Template, use the DB-DES-008 safe baseline: query the single APPROVED version and enforce at most one APPROVED version per logical Template with a partial unique index. Avoid a circular FK from Template to TemplateVersion unless a demonstrated query/performance need later justifies it.

### 5.4 Preserve Company and Period ownership rules

- Template logical identity references `companies.company_id`.
- ReportType is a separate catalog; Industry must not be substituted for ReportType.
- FinancialPeriod remains report/company temporal context; do not bind a Template to one FinancialPeriod.
- ReportVersion links through Report to Company/ReportType and separately to the exact TemplateVersion used.

## 6. Proposed implementation order

1. Decide canonical ReportType codes and review the distinct legacy `reports.report_type` values.
2. Define additive ReportType normalization migration and explicit backfill policy.
3. Finalize the ReportVersion-to-TemplateVersion provenance FK and cross-ownership integrity rule.
4. Finalize DB-DES-008 physical constraints, including uniqueness/ownership across TemplateVersion, worksheet, node, range, slot, and extraction span.
5. Add Template ORM models and import them in `src/migrations/runner.py`.
6. Add migration 9+ using the existing custom runner; preserve migration history.
7. Add migration/schema tests, including old-database upgrade, FK enforcement, approved-version uniqueness, ReportVersion provenance, and cross-company/report-type rejection.
8. Only after the separate Parsian approval and drift-validation gates, create production Template records.

## 7. Scope exclusions and unresolved evidence

This was a source-code/document audit only. It did not inspect or mutate a live SQLite database, existing production rows, or workbook files. Therefore:
- the actual distinct legacy `reports.report_type` values and their mapping remain unverified;
- the installed/runtime SQLite version and its exact feature floor remain unverified;
- existing database migration state and data quality remain unverified;
- no assumption is made that every historical ReportVersion can be assigned a TemplateVersion.

## 8. Status

DB-AUD-009 is an audit report, not an implementation. No Python code, ORM model, migration, test, or database data was changed. DB-DES-008 remains PROPOSED. Task 033 remains PARTIAL; no approval or drift-validation gate is closed by this audit.
