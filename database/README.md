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
| [DB_STD_005_AND_DB_AUD_001_MARKET_FX_EVIDENCE_REVIEW.md](reports/DB_STD_005_AND_DB_AUD_001_MARKET_FX_EVIDENCE_REVIEW.md) | مرور شواهد ورودی بازار/FX و شکاف‌های ممیزی ORM/مسیرها |
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
- جابه‌جایی این اسناد نباید به معنی تأیید محتوای پیش‌نویس‌ها یا تغییر تصمیمات ثبت‌شده تلقی شود.