# Database Documentation Hub

این پوشه محل مرکزی اسناد، شواهد و ابزارهای مستندسازی مرتبط با طراحی و پیکربندی دیتابیس پروژه است.

## مرجع‌ها و سلسله‌مراتب

1. **[Database Architecture](../12_Database_Architecture_V1.1.md)** — مرجع معماری و قراردادهای مصوب دیتابیس.
2. **[Database Configuration Master Working Packet](DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md)** — تنها مرجع اجرایی Taskها، وضعیت پیشرفت، وابستگی‌ها و کارهای باقی‌مانده.
3. **[reports/](reports/)** — گزارش‌های بازرسی، شواهد، پیشنهادها، چک‌لیست‌ها و پیش‌نویس‌های تخصصی.
4. **[dictionaries/](dictionaries/)** — دیکشنری‌ها و کاتالوگ‌های ساختاری مورد استفاده در استانداردسازی.
5. **[archive/](archive/)** — اسناد معماری قدیمی که برای حفظ سابقه نگهداری می‌شوند و مرجع تصمیمات جاری نیستند.

## فهرست گزارش‌ها

| سند | کاربرد |
|---|---|
| [BANK_MASTER_STANDARD_WORKING_CHECKLIST.md](reports/BANK_MASTER_STANDARD_WORKING_CHECKLIST.md) | چک‌لیست جامع استانداردهای بانکی |
| [BANK_MONTHLY_SAMAN_DATA_INVENTORY_DRAFT.md](reports/BANK_MONTHLY_SAMAN_DATA_INVENTORY_DRAFT.md) | فهرست داده‌های گزارش ماهانه بانک سامان |
| [BANK_PERIODIC_METRIC_DIMENSION_MAPPING_PROPOSAL.md](reports/BANK_PERIODIC_METRIC_DIMENSION_MAPPING_PROPOSAL.md) | پیشنهاد Metric و Dimension برای گزارش دوره‌ای بانک |
| [BANK_SAMAN_DEPOSITS_METRIC_CATALOGUE_DRAFT.md](reports/BANK_SAMAN_DEPOSITS_METRIC_CATALOGUE_DRAFT.md) | پیش‌نویس کاتالوگ سپرده‌ها |
| [BANK_SAMAN_LOANS_METRIC_CATALOGUE_DRAFT.md](reports/BANK_SAMAN_LOANS_METRIC_CATALOGUE_DRAFT.md) | پیش‌نویس کاتالوگ تسهیلات |
| [BANK_SAMAN_MONTHLY_METRIC_DIMENSION_REGISTER_DRAFT.md](reports/BANK_SAMAN_MONTHLY_METRIC_DIMENSION_REGISTER_DRAFT.md) | ثبت Metric و Dimension گزارش ماهانه |
| [BANK_SAMAN_MONTHLY_STANDARD_WORKING_CHECKLIST.md](reports/BANK_SAMAN_MONTHLY_STANDARD_WORKING_CHECKLIST.md) | چک‌لیست استاندارد ماهانه بانک سامان |
| [BANK_webmellat_MONTHLY_STANDARD_WORKING.md](reports/BANK_webmellat_MONTHLY_STANDARD_WORKING.md) | بررسی گزارش ماهانه بانک ملت |
| [BANK_websader_MONTHLY_STANDARD_WORKING.md](reports/BANK_websader_MONTHLY_STANDARD_WORKING.md) | بررسی گزارش ماهانه بانک صادرات |
| [DB-AUD-002_REAL_EXCEL_TEMPORAL_AUDIT.md](reports/DB-AUD-002_REAL_EXCEL_TEMPORAL_AUDIT.md) | شواهد زمانی گزارش‌های Excel |
| [DB-STD-002_BANK_MONTHLY_SAMPLE_REVIEW.md](reports/DB-STD-002_BANK_MONTHLY_SAMPLE_REVIEW.md) | بررسی نمونه گزارش ماهانه بانک |
| [DB-STD-002_BANK_MONTHLY_SAMPLE_REVIEW_2.md](reports/DB-STD-002_BANK_MONTHLY_SAMPLE_REVIEW_2.md) | بررسی تکمیلی نمونه گزارش ماهانه بانک |
| [DB-STD-002_BANK_quarterly_SAMPLE_REVIEW.md](reports/DB-STD-002_BANK_quarterly_SAMPLE_REVIEW.md) | بررسی نمونه گزارش دوره‌ای بانک |
| [DB_DES_003_REPORT_PERIOD_CONTRACT.md](reports/DB_DES_003_REPORT_PERIOD_CONTRACT.md) | قرارداد منطقی دوره‌های مالی |
| [DB_DES_004_MARKET_FX_SHARE_CONTRACT.md](reports/DB_DES_004_MARKET_FX_SHARE_CONTRACT.md) | قرارداد منطقی بازار، FX، تعداد سهام و رویدادهای سرمایه‌ای |
| [DB_DES_005_INGESTION_ATOMICITY_CONTRACT.md](reports/DB_DES_005_INGESTION_ATOMICITY_CONTRACT.md) | قرارداد IngestionRun، مرز تراکنش و اتمیک بودن ورود داده |
| [DB_DES_006_CODAL_CANONICAL_INGESTION_PIPELINE.md](reports/DB_DES_006_CODAL_CANONICAL_INGESTION_PIPELINE.md) | قرارداد منطقی مسیر CODAL Excel تا FinancialFact canonical |
| [DB_DES_007_EXCEL_SOURCE_OBSERVATION_DTO_CONTRACT.md](reports/DB_DES_007_EXCEL_SOURCE_OBSERVATION_DTO_CONTRACT.md) | قرارداد DTO موقت مشاهدهٔ ساختار و مقادیر workbookهای Excel |
| [DB_AUD_007_EXCEL_OBSERVATION_DTO_EVIDENCE_FIT.md](reports/DB_AUD_007_EXCEL_OBSERVATION_DTO_EVIDENCE_FIT.md) | ارزیابی انطباق DTO اکسل با شواهد ساختاری و زمانی مستندشده |
| [DB_AUD_008_EXCEL_LIBRARY_CAPABILITY_ASSESSMENT.md](reports/DB_AUD_008_EXCEL_LIBRARY_CAPABILITY_ASSESSMENT.md) | مقایسهٔ قابلیت کتابخانه‌های Excel برای انتخاب reader مسیر CODAL |
| [DB_STD_005_AND_DB_AUD_001_MARKET_FX_EVIDENCE_REVIEW.md](reports/DB_STD_005_AND_DB_AUD_001_MARKET_FX_EVIDENCE_REVIEW.md) | مرور شواهد ورودی بازار/FX و شکاف‌های ممیزی ORM/مسیرها |
| [DB_AUD_006_CODAL_PIPELINE_IMPLEMENTATION_READINESS_AUDIT.md](reports/DB_AUD_006_CODAL_PIPELINE_IMPLEMENTATION_READINESS_AUDIT.md) | ممیزی آمادگی مسیر CODAL برای پیاده‌سازی canonical |
| [findingSubheaders.md](reports/findingSubheaders.md) | بررسی زیرعنوان‌ها و ساختار گزارش |
| [parsian_periodic_report_1.md](reports/parsian_periodic_report_1.md) | گزارش تحلیلی نمونه دوره‌ای بانک پارسیان |
| [parsian_table_inventory.json](reports/parsian_table_inventory.json) | خروجی ساختاری فهرست جداول پارسیان |
| [parsian_table_inventory.md](reports/parsian_table_inventory.md) | نسخه Markdown فهرست جداول پارسیان |
| [postbank_periodic_report_1.md](reports/postbank_periodic_report_1.md) | گزارش تحلیلی نمونه پست‌بانک |
| [saderat_seasonal_report_2.md](reports/saderat_seasonal_report_2.md) | بررسی گزارش فصلی بانک صادرات |
| [saman_reply_1.md](reports/saman_reply_1.md) | پاسخ‌ها و یادداشت‌های بررسی بانک سامان |

## قواعد نگهداری

- هر سند جدید مرتبط با دیتابیس باید در همین پوشه یا یکی از زیرپوشه‌های آن ایجاد شود.
- Architecture در ریشه مخزن باقی می‌ماند و مرجع نهایی تصمیمات معماری است.
- وضعیت Taskها فقط در Master Working Packet به‌روزرسانی می‌شود.
- گزارش‌ها و شواهد تاریخی حذف نمی‌شوند؛ وضعیت پیش‌نویس/پیشنهاد/تأییدشده آن‌ها باید صریح بماند.
- فایل‌های Excel منبع، صرفاً به‌دلیل ارتباط با دیتابیس، در این پوشه کپی یا آرشیو نمی‌شوند؛ این ساختار برای مستندات متنی و دیکشنری‌های پروژه است.
- جابه‌جایی این اسناد نباید به معنی تأیید محتوای پیش‌نویس‌ها یا تغییر تصمیمات ثبت‌شده تلقی شود.| [DB_DES_008_COMPANY_TABLE_TEMPLATE_RELATIONAL_SCHEMA_PROPOSAL.md](reports/DB_DES_008_COMPANY_TABLE_TEMPLATE_RELATIONAL_SCHEMA_PROPOSAL.md) | پیشنهاد مدل رابطه‌ای فیزیکی و query-oriented برای Company Table Layout Template |
| [DB_DES_009_CANONICAL_FINANCIAL_FACT_PHYSICAL_MODEL.md](reports/DB_DES_009_CANONICAL_FINANCIAL_FACT_PHYSICAL_MODEL.md) | پیشنهاد مدل فیزیکی FinancialFact canonical، DimensionSet و provenance مسیر Excel |
| [DB_AUD_009_ORM_MIGRATION_TEMPLATE_COMPATIBILITY_AUDIT.md](reports/DB_AUD_009_ORM_MIGRATION_TEMPLATE_COMPATIBILITY_AUDIT.md) | ممیزی سازگاری مدل‌های ORM و Migrationهای موجود با Company Table Layout Template |
| [DB_AUD_010_RUNTIME_SQLITE_MIGRATION_RECONCILIATION.md](reports/DB_AUD_010_RUNTIME_SQLITE_MIGRATION_RECONCILIATION.md) | تطبیق شواهد SQLite محلی با Migration runner مخزن و ثبت مغایرت نسخه ۹ |

## ممیزی‌های اخیر provenance و Migration

- [DB_AUD_010_RUNTIME_SQLITE_MIGRATION_RECONCILIATION.md](reports/DB_AUD_010_RUNTIME_SQLITE_MIGRATION_RECONCILIATION.md) — مغایرت Migration 9 دیتابیس محلی با runner فعلی مخزن.
- [DB_AUD_011_LEGACY_RAW_FACT_PROVENANCE_DECISION.md](reports/DB_AUD_011_LEGACY_RAW_FACT_PROVENANCE_DECISION.md) — ممیزی پنج فیلد provenance قدیمی، ارجاعات ORM/کد و تصمیم موقت حفظ داده‌ها.
- [DB_AUD_011_LEGACY_RAW_FACT_PROVENANCE_DECISION.md](reports/DB_AUD_011_LEGACY_RAW_FACT_PROVENANCE_DECISION.md) — ارزیابی پنج فیلد provenance قدیمی، وابستگی‌های downstream و مسیر persistence فعلی.


## ممیزی مسیر PDF در CODAL

- [DB_AUD_012_CODAL_PDF_PATH_DEPENDENCY_AUDIT.md](reports/DB_AUD_012_CODAL_PDF_PATH_DEPENDENCY_AUDIT.md) — ممیزی تکمیل‌شده مسیر PDF و inventory محلی؛ تفکیک اجزای PDF-only از قراردادهای legacy و schema.
- اسکریپت read-only: `src/scripts/audit_codal_pdf_dependencies.py`.
- [DB_PLAN_013_PDF_PATH_RETIREMENT_SEQUENCE.md](reports/DB_PLAN_013_PDF_PATH_RETIREMENT_SEQUENCE.md) — طرح مرحله‌ای بازنشستگی PDF با حفظ RawFinancialFact و persistence مشترک تا تصمیم مستقل.
- [DB_AUD_013_EXCEL_CANONICAL_PERSISTENCE_READINESS.md](reports/DB_AUD_013_EXCEL_CANONICAL_PERSISTENCE_READINESS.md) — مقایسه قرارداد FinancialFact هدف با ORM فعلی و شناسایی شکاف‌های Report/Version، Period، NormalizedFact و provenance.
- [DB_AUD_014_NORMALIZED_DERIVED_FACT_CONSUMER_AUDIT.md](reports/DB_AUD_014_NORMALIZED_DERIVED_FACT_CONSUMER_AUDIT.md) — inventory مصرف‌کنندگان runtime، وابستگی Stage 5 و گپ linkage جداول Derived.

- اسکریپت read-only برای تکمیل linkage جداول Normalized/Derived: `src/scripts/audit_normalized_derived_fact_links.py` — اجرا از ریشه پروژه با `python src/scripts/audit_normalized_derived_fact_links.py`؛ خروجی در `reply.md`.
- [DB_AUD_015_LOCAL_NORMALIZED_DERIVED_FACT_LINKAGE_RESULTS.md](reports/DB_AUD_015_LOCAL_NORMALIZED_DERIVED_FACT_LINKAGE_RESULTS.md) — نتایج شمارش و linkage جداول Normalized/Derived در دیتابیس محلی (snapshot مورخ 2026-11-18).
- [DB_DES_010_STAGE5_FINANCIAL_FACT_QUERY_MIGRATION_CONTRACT.md](reports/DB_DES_010_STAGE5_FINANCIAL_FACT_QUERY_MIGRATION_CONTRACT.md) — قرارداد انتقال Stage 5 به FinancialFact با PIT، ابعاد، دوره‌های Jalali و provenance.

| [DB_DES_011_FINANCIAL_PERIOD_TEMPORAL_BASIS_CONTRACT.md](reports/DB_DES_011_FINANCIAL_PERIOD_TEMPORAL_BASIS_CONTRACT.md) | قرارداد پیشنهادی تاریخ‌های جلالی، INSTANT/DURATION و تفکیک YTD از بازه مالی |

- [DB_AUD_016_TEMPORAL_CONTRACT_RECONCILIATION.md](reports/DB_AUD_016_TEMPORAL_CONTRACT_RECONCILIATION.md) — تطبیق Architecture V1.3 و قراردادهای زمانی؛ تعارض مالکیت YTD و موارد باز months_length و Fiscal Calendar.

- [DB_DES_011_FINANCIAL_PERIOD_TEMPORAL_BASIS_CONTRACT.md](reports/DB_DES_011_FINANCIAL_PERIOD_TEMPORAL_BASIS_CONTRACT.md) — قرارداد پذیرفته‌شده مالکیت fact-level برای YTD/Standalone و دوره‌های جلالی.
- [DB_AUD_016_TEMPORAL_CONTRACT_RECONCILIATION.md](reports/DB_AUD_016_TEMPORAL_CONTRACT_RECONCILIATION.md) — ممیزی تطبیق قراردادهای زمانی و ثبت gateهای باقی‌مانده.

- [DB_AUD_017_FISCAL_CALENDAR_SOURCE_AND_LIFECYCLE_AUDIT.md](reports/DB_AUD_017_FISCAL_CALENDAR_SOURCE_AND_LIFECYCLE_AUDIT.md) — ممیزی شواهد منبع، مدل فعلی Company و چرخه عمر سال مالی اختصاصی هر شرکت.

- [DB_DES_012_COMPANY_FISCAL_YEAR_LOGICAL_MODEL.md](reports/DB_DES_012_COMPANY_FISCAL_YEAR_LOGICAL_MODEL.md) — مدل منطقی سال مالی واقعی هر شرکت، شواهد، تغییر سال مالی و ارتباط با FinancialPeriod.
