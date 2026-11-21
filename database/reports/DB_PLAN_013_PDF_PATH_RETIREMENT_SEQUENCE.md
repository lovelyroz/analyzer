

> **SUPERSEDED — 2026-11-21.** This staged plan is historical. The owner decided file inputs are Excel/CSV only, so its condition to retain PDF until Excel persistence is ready no longer applies. PDF retirement is implemented in database/reports/DB_CODAL_RETIRE_001_EXCEL_CSV_ONLY_RETIREMENT.md.
# DB-PLAN-013 — طرح مرحله‌ای بازنشستگی مسیر PDF در CODAL

**تاریخ:** 2026-11-18  
**وضعیت:** PROPOSAL — طرح اجرایی؛ هنوز هیچ تغییر کدی مجاز/اعمال نشده است.  
**مبنای ممیزی:** DB-AUD-011 و DB-AUD-012  
**دامنه:** حذف وابستگی استخراج/دریافت PDF از مسیر CODAL، بدون بازنشستگی هم‌زمان RawFinancialFact یا persistence مشترک FX/OHLC.

## 1. تصمیم راهبردی

بازنشستگی PDF و بازنشستگی RawFinancialFact دو پروژه جدا هستند.

- این طرح فقط قابلیت دریافت و استخراج PDF را هدف می‌گیرد.
- مدل، جدول، ستون‌ها، FKها و 505 رکورد فعلی RawFinancialFact در این طرح حفظ می‌شوند.
- توابع FX/OHLC در \`src/ingestion/service.py\` حفظ می‌شوند.
- مدل‌های FinancialMetric، MappingDecision، NormalizedFinancialFact، DerivedFinancialFact و provenance آن‌ها خارج از دامنه حذف‌اند.
- هیچ Migration یا تغییر schema در این طرح انجام نمی‌شود.

**محدودیت مهم:** مسیر production Excel-to-canonical persistence هنوز در source احراز نشده است. بنابراین نباید PDF را پیش از مشخص‌شدن و آزموده‌شدن مسیر جایگزین از جریان عملیاتی حذف کنیم. طراحی و پیاده‌سازی مسیر Excel باید پیش از قطع entry point عملیاتی PDF انجام شود؛ اما می‌توان طراحی بازنشستگی و جداسازی ماژول‌ها را از همین حالا آماده کرد.

## 2. طبقه‌بندی اجزا

### 2.1 PDF-only — هدف حذف پس از جایگزینی عملیاتی

| فایل | اقدام برنامه‌ریزی‌شده |
|---|---|
| \`src/ingestion/codal/acquisition.py\` | حذف دریافت فایل محلی/URL پس از حذف callerها |
| \`src/ingestion/codal/pdf_extract.py\` | حذف backendها و منطق استخراج PDF |
| \`src/ingestion/codal/adapter.py\` | حذف تبدیل PDF به RawLineInput |
| \`src/ingestion/codal/pipeline.py\` | حذف pipelineهای load_codal_pdf و load_codal_pdf_from_url |
| \`src/ingestion/codal/parser.py\` | حذف parser مبتنی بر pypdf؛ این parser عمومی Excel یا parser عمومی مالی نیست |
| \`src/tests/test_codal_acquisition.py\` | حذف یا جایگزینی تست‌های acquisition پس از حذف قابلیت |
| \`src/tests/test_codal_extraction.py\` | جداسازی تست‌های PDF از تست‌های قرارداد legacy؛ فقط تست‌های PDF حذف شوند |
| \`src/tests/test_codal_pdf_extraction.py\` | حذف تست‌های PDF؛ هر assertion مربوط به قرارداد مستقل باید پیش از حذف منتقل شود |

### 2.2 CODAL legacy — فعلاً حفظ، تصمیم مستقل

| فایل/نماد | دلیل حفظ موقت |
|---|---|
| \`src/ingestion/service.py::RawLineInput\` | DTO مورد استفاده persistence قدیمی و تست‌های Stage 1 |
| \`src/ingestion/service.py::ReportIngestionResult\` | نتیجه API قدیمی persistence |
| \`src/ingestion/service.py::ingest_codal_report\` | API قدیمی ایجاد Report/ReportVersion و ذخیره RawFinancialFact؛ هنوز جداسازی metadata persistence از raw persistence انجام نشده |
| \`src/ingestion/codal/ingestion.py\` | facade قدیمی؛ پس از شناسایی callerها باید فقط facade PDF حذف و وضعیت ingest_codal_report جداگانه تعیین شود |
| \`src/ingestion/codal/validator.py\` | اعتبارسنجی قرارداد RawLine؛ پس از قطع PDF ممکن است دیگر لازم نباشد، اما حذف آن باید هم‌زمان با تصمیم درباره RawLine انجام شود |
| \`src/ingestion/codal/numbers.py\` | تبدیل/parse متن مخصوص ورودی legacy؛ Excel Reader نباید از آن برای تبدیل native numeric استفاده کند. پس از حذف همه callerها قابل حذف است |
| \`src/ingestion/__init__.py\` | exportهای قدیمی RawLineInput و ingest_codal_report فعلاً حفظ؛ بعداً با API جدید جایگزین یا صریحاً بازنشسته شوند |
| \`src/ingestion/codal/__init__.py\` | exportهای عمومی باید همراه با callerها تغییر کنند، نه با حذف کورکورانه فایل |

### 2.3 Shared/schema — صریحاً خارج از دامنه

- \`src/ingestion/service.py\`: فقط توابع CODAL legacy در تغییرات بعدی قابل جداسازی‌اند؛ \`ingest_ohlc_csv\`، \`ingest_fx_rates\` و \`ingest_fx_xlsx\` نباید تغییر رفتاری کنند.
- \`src/models/normalized.py::RawFinancialFact\`: حفظ شود.
- \`src/models/normalized.py\` و \`src/models/normalized_provenance.py\`: مدل‌ها و FKهای دیگر حفظ شوند.
- \`src/migrations/runner.py\` و \`src/scripts/init_db.py\`: import مدل‌ها فعلاً حفظ شود تا schema bootstrap تغییر ناخواسته نکند.
- \`mapping_decisions.raw_fact_id\`، \`normalized_financial_facts.raw_fact_id\` و \`normalized_financial_fact_inputs.raw_fact_id\`: در این طرح دست‌نخورده.
- تست‌های \`test_stage1_rules.py\`، \`test_stage1_database_architecture.py\` و \`test_stage1_database_integrity.py\`: حذف نشوند؛ فقط بخش‌های PDF-specific احتمالی جدا شوند.
- \`test_stage5_forecast.py\`: snapshot حفظ ورودی‌های RawFinancialFact را نگه دارد یا فقط با تست معادل و تصمیم معماری صریح جایگزین شود.

## 3. ترتیب اجرای پیشنهادی

### Phase 0 — تثبیت قرارداد جایگزین Excel (پیش‌نیاز قطع PDF)

1. تعیین مسیر کامل Excel از workbook/observation تا استخراج بر اساس Company Table Layout Template و ذخیره canonical.
2. تعیین مدل مقصد ذخیره‌سازی و رابطه آن با Company، FinancialPeriod، Report و ReportVersion.
3. تعیین provenance دقیق source cell برای هر fact، شامل حالتی که یک مقدار از چند سلول تشکیل می‌شود.
4. تعیین اینکه چه metadataهایی از Report/ReportVersion قابل reuse هستند و کدام بخش فعلی به RawLine/RawFinancialFact گره خورده است.
5. تعریف تست end-to-end برای Excel: template selection، extraction، validation، persistence، idempotency و provenance.

**Gate:** تا وقتی مسیر Excel end-to-end و تست‌های قراردادی آن تأیید نشده‌اند، entry point عملیاتی PDF حذف/غیرفعال نشود.

### Phase 1 — جداسازی metadata persistence از RawFact persistence

1. تابع فعلی \`ingest_codal_report\` را به دو مسئولیت تفکیک طراحی کن: ایجاد/انتخاب Report و ReportVersion، و ذخیره RawLineInput به RawFinancialFact.
2. هیچ رفتار FX/OHLC در این refactor تغییر نکند.
3. قرارداد idempotency بر اساس CODAL tracking ID و publication datetime حفظ شود.
4. این مرحله هیچ داده legacy را migrate یا حذف نمی‌کند و schema را تغییر نمی‌دهد.
5. تست‌های Report/ReportVersion و RawFact persistence جدا شوند تا معلوم باشد کدام رفتار legacy است.

**Gate:** تست‌های جدید و قدیمی مرتبط باید پس از اجرای مالک سبز باشند؛ تست‌ها توسط مالک اجرا می‌شوند.

### Phase 2 — انتقال callerهای عملیاتی به Excel

1. ورودی عملیاتی جدید از Excel Reader و template مصوب استفاده کند.
2. Excel native numericها بدون stringification یا parse متنی حفظ شوند.
3. هیچ وابستگی به رنگ/بوردر workbookهای بعدی ایجاد نشود؛ template مصوب مرجع استخراج باشد.
4. ذخیره‌سازی فقط پس از validation کامل گزارش و جلوگیری از partial ingestion انجام شود.
5. callerها و UI/CLIهای عملیاتی به Excel منتقل شوند؛ هر caller بیرونی/مستندنشده باید پیش از حذف PDF تعیین تکلیف شود.

**Gate:** یک گزارش واقعی جدید از همان شرکت/report type باید با template استخراج و end-to-end persist شود و lineage قابل audit داشته باشد.

### Phase 3 — حذف مسیر PDF

پس از عبور از Gateهای بالا:
1. حذف entry pointهای PDF و exportهای مربوط.
2. حذف فایل‌های PDF-only مشخص‌شده در بخش 2.1.
3. حذف dependencyهای PDF از dependency manifest فقط اگر هیچ مصرف‌کننده دیگری در کل مخزن وجود نداشته باشد.
4. حذف/بازنویسی تست‌های PDF؛ تست‌های schema و legacy persistence حفظ شوند.
5. جست‌وجوی import/caller پس از حذف و اجرای suiteهای مرتبط توسط مالک.

### Phase 4 — بازبینی جداگانه RawFinancialFact (جزو این طرح نیست)

این مرحله بعداً و با طرح مستقل انجام می‌شود. پیش‌نیازهای آن:
- حل مغایرت Migration 9 و ثبت source revision دقیق؛
- تعیین تکلیف Report/ReportVersion و metadata لازم؛
- تعیین تکلیف سه FK legacy و تست‌های وابسته؛
- linkage audit روی دیتابیس دقیق مقصد و بررسی backupها/محیط‌ها؛
- migration طراحی‌شده با حفظ داده‌ها تا زمان تصمیم صریح؛
- جایگزینی تست‌های preservation و lineage با قرارداد جدید.

## 4. معیار پذیرش بازنشستگی PDF

- هیچ production import/caller به acquisition، pdf_extract، adapter، parser یا PDF pipeline باقی نماند.
- هیچ API عمومی ناخواسته PDF باقی نماند.
- dependencyهای PDF فقط در صورت نبود مصرف‌کننده دیگر حذف شوند.
- Excel مسیر عملیاتی کامل و آزموده‌شده داشته باشد.
- توابع FX/OHLC و رفتارشان بدون تغییر باقی بمانند.
- RawFinancialFact، 505 رکورد فعلی، ستون‌ها و FKها در این تغییر حفظ شوند.
- تست‌های schema، mapping، Report/ReportVersion و forecast input preservation بی‌دلیل حذف نشوند.
- هیچ Migration مربوط به حذف جدول در این تغییر انجام نشود.

## 5. وضعیت و اقدام بعدی

- طرح بازنشستگی PDF: **DRAFTED**.
- پیاده‌سازی: **NOT STARTED**.
- Excel-to-canonical persistence: **NOT ESTABLISHED**.
- RawFinancialFact retirement: **OUT OF SCOPE / NOT AUTHORIZED**.
- Migration 9 reconciliation: **OPEN**.
- تستی اجرا نشده است.

**گام بعدی فنی پیشنهادی:** Phase 0 را تکمیل کنیم؛ یعنی ابتدا مدل persistence مقصد برای Excel و نحوه reuse کردن Report/ReportVersion را طراحی و با معماری Company Table Layout Template تطبیق دهیم. این کار قبل از حذف هر ماژول PDF ضروری است.


## 6. نتیجه ممیزی Phase 0 — DB-AUD-013

گزارش: `database/reports/DB_AUD_013_EXCEL_CANONICAL_PERSISTENCE_READINESS.md`

- Report و ReportVersion موجود پایه قابل reuse هستند، اما ReportType catalog و source artifact fingerprint/standard-version binding کامل نیست.
- FinancialPeriod فعلی از Gregorian Date استفاده می‌کند و با قرارداد authoritative Jalali و INSTANT/DURATION هنوز منطبق نیست.
- NormalizedFinancialFact فعلی Numeric(30,4)، بدون dimension identity و بدون source unit/basis/value state/extraction-standard version کامل است؛ بنابراین مقصد آماده و مستقیم برای Excel نیست.
- NormalizedFinancialFactInput فعلی به RawFinancialFact و MappingDecision اجباری وابسته است و برای provenance جدید مناسب نیست.
- Company Table Layout Template ساختار workbook را حل می‌کند، اما به‌تنهایی semantic mapping و canonical persistence را تعریف نمی‌کند.

**نتیجه Phase 0:** شکاف persistence شناسایی شد؛ مسیر Excel-to-canonical هنوز آماده نیست. Report/ReportVersion را به‌عنوان پایه قابل توسعه نگه می‌داریم، اما NormalizedFinancialFact را بدون بازطراحی مقصد آماده تلقی نمی‌کنیم. هنوز هیچ کد، ORM، Migration یا داده‌ای تغییر نمی‌کند.

**گام بعدی:** طراحی فیزیکی مستقل canonical FinancialFact و provenance contract؛ تصمیم میان بازطراحی NormalizedFinancialFact و جایگزینی آن باید با مقایسه migration/compatibility گرفته شود. تا تکمیل این طراحی و مسیر Excel end-to-end، مسیر PDF عملیاتی قطع نمی‌شود.
