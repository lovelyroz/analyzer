# DB-AUD-010 — Runtime SQLite and Migration-History Reconciliation

**Status:** PARTIAL — runtime evidence received; source/migration drift unresolved  
**Date:** 2026-11-18  
**Scope:** Reconcile owner-provided local SQLite metadata with the current repository migration runner and DB-AUD-009  
**Mode:** Report-only; no code, ORM, migration, tests, or database rows changed

## 1. Owner-provided runtime evidence

The owner supplied the following local database observations:

- SQLite runtime version: `3.45.3`.
- Distinct `reports.report_type` values:
  - `CODAL_XLSX_TEMP_TEST` => 2 rows.
- Applied migration history:
  1. `baseline_schema`
  2. `mapping_and_derived_schema`
  3. `normalized_fact_multi_source_provenance`
  4. `one_current_report_version`
  5. `market_daily_jalali_components`
  6. `fx_rates_jalali_components`
  7. `forecast_version_repository`
  8. `remove_forecast_output_persistence`
  9. `codal_excel_source_metadata`

This is owner-supplied runtime evidence; it was not independently queried by this audit.

## 2. Confirmed compatibility implication

SQLite 3.45.3 is sufficiently recent for the SQLite features contemplated by DB-DES-008, including partial indexes and ordinary foreign-key constraints. The application must still keep `PRAGMA foreign_keys=ON` enabled per connection, as the current `src/core/database.py` already does.

The observed `CODAL_XLSX_TEMP_TEST` value is the only distinct legacy report_type value in the supplied query result, but its name explicitly signals a temporary/test value. It must not be promoted to a production ReportType code without an explicit owner decision and source/usage review. The two rows should be treated as test/legacy data pending classification, not as proof of the final report-type taxonomy.

## 3. Critical source-versus-database migration discrepancy

The current repository version of `src/migrations/runner.py` inspected for DB-AUD-009 defines migrations only through version 8. The owner-provided local `schema_migrations` history contains version 9 named `codal_excel_source_metadata`.

Therefore, at least one of the following is true and must be resolved:
- migration 9 exists in local/uncommitted source but is absent from the current GitHub branch;
- the local database was upgraded by a different code revision or migration mechanism;
- the current repository branch is behind the code used to upgrade the local database; or
- the recorded migration history and checked-out source do not correspond to the same deployment lineage.

No assumption is made about which explanation is correct. The exact migration-9 implementation and its schema effects are not established by the migration-history row alone.

**Implementation blocker:** Do not author migration 10, edit the migration runner, or build ORM relationships on the assumption that migration 9 is represented in the current repository. First obtain and compare the exact migration-9 source/function, its ORM imports, affected tables/columns/indexes/FKs, and the Git commit/revision used to apply it locally.

## 4. Impact on DB-DES-008 and DB-AUD-009

DB-AUD-009 remains valid as a source-code snapshot of the repository version it inspected, but its statement that the live SQLite version and applied migration state were unverified is now superseded by the owner-provided evidence above.

The following conclusions remain unchanged:
- Existing Company, Industry, Report, ReportVersion, FinancialPeriod, and FinancialMetric models are reusable within their stated roles.
- `reports.report_type` remains a free-text field in the inspected ORM source; no ReportType FK catalog was found there.
- No Company Table Layout Template ORM entities were found in the inspected source.
- The proposed ReportType catalog and ReportVersion-to-TemplateVersion provenance relationship remain design prerequisites, not implemented facts.

The migration-count conclusion must be stated carefully: repository runner source currently lists 1–8, while the local database reports 1–9. The repository and local database are not yet proven to be synchronized.

## 5. Required next action

Obtain the exact source for migration 9 `codal_excel_source_metadata` from the local working tree (or the commit that applied it), including:
- complete migration function and migration registration;
- all model imports added for it;
- schema objects it creates or alters;
- tests and migration invocation evidence;
- Git status/commit identifier showing whether those changes are committed.

Then reconcile the migration-9 source with the current GitHub branch and inspect its resulting tables/columns before deciding whether ReportType normalization is still wholly absent, partially implemented, or already represented by that migration.

A compact local PowerShell evidence collection is sufficient; no new schema change is requested in this step.

## 6. Status

DB-AUD-010 records a runtime/source discrepancy and narrows the next investigation. It does not approve ReportType values, resolve the discrepancy, or authorize implementation. DB-DES-008 remains PROPOSED. Task 033 remains PARTIAL. No tests were run.


## 7. Follow-up audit of Migration 9 columns — 2026-11-18

A subsequent read-only audit of the owner's local SQLite database and Python source produced these results for `raw_financial_facts`:

| Column | Total rows | Non-null rows | Distinct non-null values |
|---|---:|---:|---:|
| `source_sheet` | 505 | 505 | 1 |
| `source_column_header` | 505 | 505 | 23 |

The sole `source_sheet` value is `Recovered_Sheet1`. The 23 observed `source_column_header` values contain period/header text from the source workbook. Thus, neither column is empty in the current local database. This is evidence of populated legacy provenance/context data, not proof that these fields belong in the final canonical fact schema.

The source-reference scan found the two names only in the temporary audit scripts then present under `src/scripts`; it did not establish active application/ORM usage. The audit script itself was excluded from any claim of application usage.

**Architectural assessment:** these columns must not be dropped or retained solely because they contain data. The new Excel ingestion design uses explicit template structure, canonical identifiers, and source locators/provenance at the appropriate report/template level. Before deciding their final disposition, determine whether the information they contain is represented elsewhere in the approved design and whether any existing service/report requires backward compatibility. Until then, preserve the columns and their values; do not run a destructive migration.

This follow-up resolves the earlier uncertainty about whether the two columns are populated, but does not recover the original Migration 9 implementation or prove its complete schema effects. The exact historical migration source remains unavailable in the checked-out repository.


## 8. Current-branch Migration 9 tooling cross-check — 2026-11-19

A read-only inspection of the current GitHub branch found:
- `src/migrations/runner.py` registers migrations 1 through 8 only.
- `src/scripts/audit_migration_9_database_state.py` opens the project-root `tehran_stock.db` in SQLite read-only mode and writes its report to root `reply.md`.
- `src/scripts/audit_migration_9_source.py` scans local `src/` and `tests/` Python files and local Git refs for Migration 9 source/history; it does not open the database.
- `src/scripts/cleanup_incomplete_migration_9.py` has a read-only default and a destructive `--apply` mode. The apply path requires the exact ledger row `(9, codal_excel_source_metadata)`, version 9 to be the highest migration, both target columns to exist, no indexes/triggers or other schema objects referencing them, and SQLite >= 3.35. It creates a backup, drops `source_column_header` and `source_sheet`, deletes the version-9 ledger row, and checks SQLite integrity and foreign keys.

The existing local evidence recorded in §7 reports that these two columns contain data in all 505 RawFinancialFact rows (source_sheet: 505 non-null, one distinct value; source_column_header: 505 non-null, 23 distinct values). Therefore, `cleanup_incomplete_migration_9.py --apply` is destructive to live schema/data representation even though it preserves a backup. It must not be run merely to make the local ledger match the current branch. First recover the exact local Migration 9 source/revision and determine whether these populated provenance values are represented elsewhere in the approved Excel ingestion design.

A further path discrepancy is confirmed: `src/core/database.py` configures relative `sqlite:///./tehran_stock.db`, whose resolved file depends on process working directory; the two Migration 9 DB scripts instead hard-code `ROOT / "tehran_stock.db"`. Their target may differ when the process is launched from another working directory. The scripts' output does not prove it inspected the same DB file used by the application unless the resolved paths are compared.

### Updated conclusion

The current repository migration chain is version 8, while the previously recorded owner-local database evidence reports version 9 and populated Migration 9 columns. The exact migration source and deployment lineage remain unreconciled. Do not run cleanup, add migration 10, or infer that the two columns are disposable. The next safe action is read-only local source/path reconciliation and explicit design mapping for both populated columns. No code, ORM, schema, migration, database, or tests were changed/run in this follow-up.
