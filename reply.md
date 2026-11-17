MIGRATION 9 FULL LOCAL AUDIT
Repository: D:\winprojects\analyzer
Generated: 2026-11-18T00:51:09.967953


================================================================================
GIT STATUS
================================================================================

M reply.md


================================================================================
CURRENT COMMIT
================================================================================

2de04f411c6482cb6699556284cf615d45aedae5
docs(database): record runtime migration source drift


================================================================================
CURRENT BRANCH
================================================================================

master


================================================================================
UNCOMMITTED DIFF FILES
================================================================================

reply.md

STAGED:
(empty)


================================================================================
PROJECT-WIDE SOURCE SEARCH
================================================================================

Scanned text files: 5426
Matching lines: 27
12_Database_Architecture_V1.1.md:662 [schema_migrations]
    - `schema_migrations`
database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:97 [codal_excel]
    - برای ورودی‌های `.xls` مبتنی بر HTML، خروجی preprocessing باید XLSX واقعی و معتبر باشد؛ تغییر پسوند به‌تنهایی تبدیل محسوب نمی‌شود. این تبدیل عملیاتی در Packet مستقل `CODAL_EXCEL_PREPROCESSING_MASTER_WORKING_PACKET.md` تعریف شده است.
database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:359 [schema_migrations]
    جمعاً ۱۹ جدول در metadata فعال ORM شناسایی شد. (دو جدول Forecast legacy در metadata جداگانه‌اند و در این شمارش نیستند.) جدول `schema_migrations` را خود migration runner ایجاد می‌کند و در metadata مدل‌های فعال تعریف نشده است.
database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:434 [schema_migrations]
    7. مسیر legacy در `MigrationRunner.upgrade()` اگر هر جدول غیر از `schema_migrations` وجود داشته باشد و migration history خالی باشد، فقط رکورد baseline نسخهٔ ۱ را ثبت می‌کند و migration شمارهٔ ۱ را اجرا نمی‌کند. در نتیجه، اگر schema قدیمی ناقص باشد، runner لزوماً تمام جدول‌های baseline را ایجاد/ترمیم نمی‌کند؛ فقط تغییرات بعدی را اجرا می‌کند. این رفتار باید در طرح migration آینده لحاظ شود.
database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1017 [schema_migrations]
    - پروژه از Migration اختصاصی `src/migrations/runner.py` با نسخه‌های 1 تا 8 و جدول `schema_migrations` استفاده می‌کند؛ Alembic/revision chain در مسیر بررسی‌شده وجود ندارد. FKهای SQLite نیز در `src/core/database.py` برای هر connection فعال می‌شوند.
database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1033 [codal_excel_source_metadata, excel_source_metadata, codal_excel]
    مالک پروژه شواهد دیتابیس محلی را ارائه کرد: SQLite نسخه 3.45.3، تنها مقدار متمایز فعلی `reports.report_type` برابر `CODAL_XLSX_TEMP_TEST` با دو رکورد، و تاریخچه Migrationهای اعمال‌شده از نسخه 1 تا 9. نام Migration نهم `codal_excel_source_metadata` است.
database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1035 [schema_migrations]
    این شواهد با کد فعلی GitHub در `src/migrations/runner.py` مغایرت دارد؛ نسخه بررسی‌شده در مخزن Migrationها را فقط تا نسخه 8 ثبت کرده است. بنابراین source code مخزن و دیتابیس محلی هنوز هم‌نسخه و هم‌تبار اثبات نشده‌اند. صرف وجود ردیف Migration 9 در `schema_migrations` برای استنتاج ساختار ایجادشده یا تغییرات ORM کافی نیست.
database\reports\DB_AUD_009_ORM_MIGRATION_TEMPLATE_COMPATIBILITY_AUDIT.md:56 [schema_migrations]
    - Applied versions are recorded in `schema_migrations`.
database\reports\DB_AUD_010_RUNTIME_SQLITE_MIGRATION_RECONCILIATION.md:24 [codal_excel_source_metadata, excel_source_metadata, codal_excel]
    9. `codal_excel_source_metadata`
database\reports\DB_AUD_010_RUNTIME_SQLITE_MIGRATION_RECONCILIATION.md:36 [codal_excel_source_metadata, excel_source_metadata, codal_excel, schema_migrations]
    The current repository version of `src/migrations/runner.py` inspected for DB-AUD-009 defines migrations only through version 8. The owner-provided local `schema_migrations` history contains version 9 named `codal_excel_source_metadata`.
database\reports\DB_AUD_010_RUNTIME_SQLITE_MIGRATION_RECONCILIATION.md:62 [codal_excel_source_metadata, excel_source_metadata, codal_excel]
    Obtain the exact source for migration 9 `codal_excel_source_metadata` from the local working tree (or the commit that applied it), including:
database\reports\DB_STD_005_AND_DB_AUD_001_MARKET_FX_EVIDENCE_REVIEW.md:270 [schema_migrations]
    1. `MigrationRunner.upgrade()` هر migration را اجرا می‌کند و پس از بازگشت تابع `apply`، رکورد `schema_migrations` را در یک `engine.begin()` جداگانه درج می‌کند. بنابراین تغییر schema و ثبت شمارهٔ migration یک تراکنش واحد نیستند. اگر DDL موفق شود ولی درج version marker شکست بخورد، اجرای بعدی ممکن است migration را دوباره اجرا کند؛ idempotency برخی عملیات این خطر را کاهش می‌دهد، اما atomicity کلی را تضمین نمی‌کند.
src\migrations\runner.py:42 [schema_migrations]
    MIGRATION_TABLE = "schema_migrations"
src\migrations\runner.py:51 [schema_migrations]
    "INSERT INTO schema_migrations(version, name, applied_at) "
src\migrations\runner.py:59 [schema_migrations]
    "CREATE TABLE IF NOT EXISTS schema_migrations ("
src\migrations\runner.py:187 [schema_migrations]
    value = connection.execute(text("SELECT MAX(version) FROM schema_migrations")).scalar()
src\scripts\audit_migration_9.py:32 [codal_excel_source_metadata, excel_source_metadata, codal_excel]
    "codal_excel_source_metadata",
src\scripts\audit_migration_9.py:33 [Migration(9]
    "Migration(9",
src\scripts\audit_migration_9.py:34 [version=9]
    "version=9",
src\tests\test_stage1_database_integrity.py:45 [schema_migrations]
    versions = connection.execute(text("SELECT version FROM schema_migrations ORDER BY version")).scalars().all()
src\tests\test_stage1_database_integrity.py:62 [schema_migrations]
    connection.execute(text("CREATE TABLE schema_migrations (version INTEGER PRIMARY KEY, name VARCHAR(200) NOT NULL, applied_at DATETIME NOT NULL)"))
src\tests\test_stage1_database_integrity.py:64 [schema_migrations]
    connection.execute(text("INSERT INTO schema_migrations (version, name, applied_at) VALUES (:v, :n, '2024-01-01')"), {"v": version, "n": f"migration_{version}"})
src\tests\test_stage1_database_integrity.py:87 [schema_migrations]
    versions = connection.execute(text("SELECT version FROM schema_migrations ORDER BY version")).scalars().all()
src\tests\test_stage1_rules.py:252 [schema_migrations]
    assert {"schema_migrations", "mapping_rules", "derived_financial_facts", "normalized_financial_fact_inputs"}.issubset(tables)
src\tests\test_stage1_rules.py:255 [schema_migrations]
    migration_rows = connection.execute(text("SELECT COUNT(*) FROM schema_migrations")).scalar_one()
src\tests\test_stage1_rules.py:256 [schema_migrations]
    versions = connection.execute(text("SELECT version FROM schema_migrations ORDER BY version")).scalars().all()
src\tests\test_stage7_valuation.py:1435 [version=9]
    _p32_ref(datetime(2025, 6, 15, tzinfo=timezone.utc), version=9),


================================================================================
DATABASE FILE DISCOVERY
================================================================================

DATABASE: tehran_stock.db
SIZE: 688128 bytes
MODIFIED: 2026-11-07 15:24:27.770882
SQLite version: 3.45.3

TABLES:
companies
corporate_actions
derived_financial_fact_inputs
derived_financial_facts
financial_metrics
financial_periods
fx_conversion_rules
fx_rates
industries
ingestion_runs
mapping_decisions
mapping_rules
market_daily
normalized_financial_fact_inputs
normalized_financial_facts
raw_financial_facts
report_versions
reports
schema_migrations
share_count_history

MIGRATION HISTORY:
1 | baseline_schema | 2026-11-07 11:15:33.002433
2 | mapping_and_derived_schema | 2026-11-07 11:15:33.284333
3 | normalized_fact_multi_source_provenance | 2026-11-07 11:15:33.552182
4 | one_current_report_version | 2026-11-07 11:15:33.861452
5 | market_daily_jalali_components | 2026-11-07 11:15:34.147308
6 | fx_rates_jalali_components | 2026-11-07 11:15:34.434280
7 | forecast_version_repository | 2026-11-07 11:15:35.767386
8 | remove_forecast_output_persistence | 2026-11-07 11:15:36.573913
9 | codal_excel_source_metadata | 2026-11-07 11:15:36.865524

MIGRATION TABLE STRUCTURE:
version | INTEGER | notnull=0 | pk=1
name | VARCHAR(200) | notnull=1 | pk=0
applied_at | DATETIME | notnull=1 | pk=0

TABLE STRUCTURE: report_versions
COLUMN report_version_id | INTEGER | notnull=1 | pk=1 default=None
COLUMN report_id | INTEGER | notnull=1 | pk=0 default=None
COLUMN version_number | INTEGER | notnull=1 | pk=0 default=None
COLUMN publication_datetime | DATETIME | notnull=1 | pk=0 default=None
COLUMN is_current_version | BOOLEAN | notnull=1 | pk=0 default=None
COLUMN is_restated | BOOLEAN | notnull=1 | pk=0 default=None
COLUMN supersedes_version_id | INTEGER | notnull=0 | pk=0 default=None
COLUMN created_at | DATETIME | notnull=0 | pk=0 default=None
FK supersedes_version_id -> report_versions.report_version_id
FK report_id -> reports.report_id
INDEX uq_report_current_version | unique=1
INDEX sqlite_autoindex_report_versions_1 | unique=1

TABLE STRUCTURE: reports
COLUMN report_id | INTEGER | notnull=1 | pk=1 default=None
COLUMN company_id | INTEGER | notnull=1 | pk=0 default=None
COLUMN report_type | VARCHAR(100) | notnull=1 | pk=0 default=None
COLUMN codal_tracking_id | VARCHAR(100) | notnull=0 | pk=0 default=None
COLUMN title | VARCHAR(300) | notnull=1 | pk=0 default=None
COLUMN financial_period_id | INTEGER | notnull=1 | pk=0 default=None
COLUMN source_url | VARCHAR(500) | notnull=0 | pk=0 default=None
COLUMN original_report_id | INTEGER | notnull=0 | pk=0 default=None
COLUMN is_correction | BOOLEAN | notnull=1 | pk=0 default=None
COLUMN created_at | DATETIME | notnull=0 | pk=0 default=None
FK original_report_id -> reports.report_id
FK financial_period_id -> financial_periods.period_id
FK company_id -> companies.company_id
INDEX sqlite_autoindex_reports_1 | unique=1

TABLE STRUCTURE: schema_migrations
COLUMN version | INTEGER | notnull=0 | pk=1 default=None
COLUMN name | VARCHAR(200) | notnull=1 | pk=0 default=None
COLUMN applied_at | DATETIME | notnull=1 | pk=0 default=None


================================================================================
END OF AUDIT
================================================================================

Read-only inspection. No database rows or project source files changed.