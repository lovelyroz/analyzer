

## Final status — historical audit, retirement completed 2026-11-21

The findings above describe the repository before retirement. The PDF acquisition/extraction path, public API, dependency, corpus, and PDF-only tests have now been removed. Shared persistence contracts were retained and are covered with synthetic parsed-row tests. See DB_CODAL_RETIRE_001_EXCEL_CSV_ONLY_RETIREMENT.md for exact file changes, residual-reference classification, validation limits, and owner command. This audit is no longer an active implementation gate.
# DB-AUD-012 — ممیزی وابستگی‌های مسیر PDF در CODAL

**تاریخ:** 2026-11-18  
**وضعیت:** PARTIAL — بررسی source فعلی انجام شده؛ جست‌وجوی کامل روی working tree محلی در انتظار اجرای اسکریپت است.  
**نوع کار:** Audit-only؛ بدون تغییر منطق برنامه، ORM، Migration یا داده.

## 1. هدف

تعیین مرز امن بازنشستگی استخراج PDF در CODAL و تفکیک اجزای PDF-only از اجزای مشترک ingestion. این ممیزی به‌خودی‌خود تصمیم حذف جدول raw_financial_facts یا داده‌های آن نیست.

## 2. یافته‌های قطعی از source فعلی GitHub

### 2.1 زنجیره اجرایی PDF

مسیر فعلی به این شکل است:

load_codal_pdf / load_codal_pdf_from_url  
→ acquisition  
→ extract_raw_lines_from_pdf  
→ RawLineInput[]  
→ ingest_codal_report  
→ RawFinancialFact[]  
→ raw_financial_facts

نقطه‌های ورود و فایل‌ها:

| فایل | نقش | طبقه‌بندی |
|---|---|---|
| src/ingestion/codal/pipeline.py | دو entry point برای PDF محلی و URL؛ acquisition، extraction، validation و persistence را به هم متصل می‌کند | PDF-only |
| src/ingestion/codal/acquisition.py | دریافت/کپی PDF محلی و دانلود PDF از URL | PDF-only |
| src/ingestion/codal/adapter.py | تبدیل PDF به RawLineInput | PDF-only |
| src/ingestion/codal/pdf_extract.py | backendهای pypdf و pdfplumber و استخراج متن/جدول | PDF-only |
| src/ingestion/codal/parser.py | parser متن و اعداد استخراج‌شده از PDF | PDF-only؛ میزان استفاده مستقل هنوز باید با inventory محلی تأیید شود |
| src/ingestion/codal/validator.py | اعتبارسنجی RawLineInput قبل از persistence | وابسته به قرارداد legacy RawLine |
| src/ingestion/codal/ingestion.py | facade شامل ingest_codal_pdf و facade سازگاری ingest_codal_report | بخش PDF-only + facade legacy |
| src/ingestion/service.py::ingest_codal_report | ساخت Report/ReportVersion و درج یک RawFinancialFact برای هر RawLineInput | persistence قدیمی CODAL؛ در فایل مشترک با FX و Market قرار دارد |
| src/ingestion/codal/numbers.py | تبدیل ارقام فارسی/عربی و parse مبلغ برای مسیر قدیمی CODAL | CODAL-specific؛ نباید به Reader جدید Excel تحمیل شود |

### 2.2 اجزایی که نباید یک‌جا حذف شوند

1. **src/ingestion/service.py فایل مشترک است.** همین فایل persistence مربوط به OHLC و FX را نیز دارد. بازنشستگی CODAL نباید باعث حذف یا بازنویسی توابع ingest_ohlc_csv، ingest_fx_rates و ingest_fx_xlsx شود. فقط بخش RawLine/CODAL باید جداگانه ارزیابی شود.
2. **src/ingestion/__init__.py API مختلط صادر می‌کند.** exportهای CODAL در کنار FX و OHLC هستند؛ در تغییر بعدی باید فقط exportهای قدیمی CODAL حذف/جایگزین شوند.
3. **src/models/normalized.py مدل مختلط دارد.** RawFinancialFact در کنار FinancialMetric، MappingDecision، NormalizedFinancialFact و مدل‌های derived قرار دارد. حذف فایل یا سایر مدل‌ها مجاز نیست.
4. **src/migrations/runner.py، RawFinancialFact را import می‌کند.** چون baseline از Base.metadata.create_all استفاده می‌کند، حذف ساده import می‌تواند شکل schema دیتابیس تازه را تغییر دهد. این موضوع باید در طرح Migration و پس از حل مغایرت Migration 9 تعیین تکلیف شود.
5. سه FK قدیمی همچنان در ORM/schema تعریف شده‌اند: mapping_decisions.raw_fact_id، normalized_financial_fact_inputs.raw_fact_id و normalized_financial_facts.raw_fact_id. صفر بودن ردیف‌های ارجاع‌دهنده در دیتابیس فعلی، خود FKها را حذف نمی‌کند.
6. package-level facadeها در src/ingestion/codal/__init__.py و src/ingestion/__init__.py باید همراه callerها بررسی شوند؛ حذف فایل بدون اصلاح importها می‌تواند import-time failure ایجاد کند.

### 2.3 تست‌های متصل به مسیر PDF و مدل legacy

فایل‌های زیر در source فعلی به مسیر PDF یا RawFinancialFact وابسته‌اند:

- src/tests/test_codal_acquisition.py
- src/tests/test_codal_digit_normalization.py
- src/tests/test_codal_extraction.py
- src/tests/test_codal_pdf_extraction.py
- src/tests/test_stage1_database_architecture.py
- src/tests/test_stage1_database_integrity.py

دو تست Stage 1 آخر فقط تست استخراج PDF نیستند؛ مدل و قیود schema، FKها و حفظ داده legacy را هم بررسی می‌کنند. بنابراین نباید کل آن‌ها را صرفاً به‌عنوان تست‌های PDF حذف کرد؛ assertions مربوط به مدل/مهاجرت باید جداگانه بازطراحی شوند.

### 2.4 وضعیت Excel

در src/ingestion/excel فعلاً DTO و Reader مشاهده شده است. در source بررسی‌شده، مسیر production مستقلی که observationهای Excel را به مدل canonical جدید persist کند، احراز نشد. بنابراین هنوز نباید فرض کنیم با حذف مسیر PDF، ingestion جدید Excel آماده جایگزینی end-to-end است.

## 3. محدودیت شواهد

- بررسی فوق بر فایل‌های شناخته‌شده در branch فعلی GitHub و محتوای آن‌ها استوار است.
- جست‌وجوی کامل تمام فایل‌های محلی، uncommitted changes، entry pointهای خارج از فایل‌های بررسی‌شده و مصرف‌کننده‌های بیرونی هنوز انجام نشده است.
- مغایرت Migration 9 بین دیتابیس محلی و runner مخزن همچنان باز است.
- فایل‌های PDF نمونه در پوشه pdf/ و corpus تست وجود دارند؛ این ممیزی درباره حذف آن فایل‌های شواهد/fixtures تصمیم نمی‌گیرد.

## 4. اسکریپت inventory محلی

فایل src/scripts/audit_codal_pdf_dependencies.py برای جست‌وجوی read-only تمام فایل‌های متنی/کد پروژه اضافه شده است. این اسکریپت:
- پایگاه داده را باز نمی‌کند؛
- فایل source را تغییر نمی‌دهد؛
- تست اجرا نمی‌کند؛
- referenceهای مسیر PDF، RawLineInput، RawFinancialFact، facadeها و helperهای مرتبط را همراه مسیر و شماره خط در reply.md می‌نویسد؛
- پوشه‌های محیط مجازی، .git، cache و خروجی build را نادیده می‌گیرد.

دستور اجرا از ریشه پروژه:

    python src/scripts/audit_codal_pdf_dependencies.py

## 5. تصمیم موقت و گام بعدی

1. فعلاً هیچ فایل PDF، facade، مدل، ستون، جدول یا migration حذف نشود.
2. persistence مشترک FX/OHLC در service.py باید حفظ شود.
3. مدل‌های FinancialMetric و normalized/derived نباید به دلیل هم‌مکانی با RawFinancialFact حذف شوند.
4. ابتدا خروجی inventory محلی بررسی شود تا callerهای خارج از branch/working tree و importهای غیرمنتظره مشخص شوند.
5. سپس یک طرح بازنشستگی مرحله‌ای تهیه شود: حذف entry pointهای PDF، تعیین تکلیف API قدیمی RawLine، تعیین تکلیف FKهای legacy و فقط پس از آن طرح Migration برای جدول/داده.
6. مسیر Excel باید مستقل و end-to-end طراحی و پیاده‌سازی شود؛ Reader به‌تنهایی جایگزین persistence قدیمی نیست.

**وضعیت نهایی این ممیزی در این مرحله:** مسیر PDF در source PRESENT؛ مرز اولیه اجزا مشخص؛ inventory کامل local هنوز PENDING؛ هیچ کد اجرایی/ORM/Migration/داده‌ای تغییر نکرده و هیچ تستی اجرا نشده است.


## 6. تکمیل inventory روی working tree محلی — خروجی 2026-11-18

مالک اسکریپت را از ریشه پروژه اجرا کرد و خروجی را در `reply.md` قرار داد.

- فایل‌های متنی/کد اسکن‌شده: **5,611**
- فایل‌های دارای حداقل یک تطبیق: **26**
- خطوط تطبیق در production source: **131**
- خطوط تطبیق در tests: **121**
- خطوط تطبیق در scripts: **24**
- تطبیق در root/config: **0**
- دیتابیس باز نشده، source تغییر نکرده و تستی اجرا نشده است.

این شمارش‌ها تعداد خطوط دارای تطبیق هستند، نه تعداد وابستگی‌های اجرایی مستقل؛ تطبیق‌های داخل comment/docstring نیز در شمارش خام حضور دارند و باید با توجه به کاربردشان تفسیر شوند.

### 6.1 یافته‌های تکمیلی و طبقه‌بندی دقیق‌تر

**الف) PDF-only و قابل بازنشستگی در مرحله مسیر استخراج**
- `acquisition.py`: دریافت PDF محلی/URL.
- `pdf_extract.py`: استخراج ساختار/متن از PDF.
- `adapter.py`: تبدیل خروجی PDF به RawLineInput.
- `pipeline.py`: اتصال acquisition، extraction، validation و persistence.
- `parser.py`: مستقیماً از `pypdf.PdfReader` استفاده می‌کند و توابعش PDF/text-extraction specific هستند؛ نباید به‌عنوان Reader عمومی Excel حفظ/استفاده شود.
- `codal/ingestion.py`: facade قدیمی که استخراج PDF را به persistence متصل می‌کند.

**ب) CODAL legacy، اما نه لزوماً PDF extractor**
- `validator.py`: قرارداد RawLineInput را اعتبارسنجی می‌کند.
- `numbers.py`: ارقام و مبلغ‌های متنی را برای مسیر قدیمی CODAL parse می‌کند. این منطق نباید به Excel Reader تحمیل شود؛ Excel باید مقادیر native را حفظ کند.
- `RawLineInput` و `ReportIngestionResult` در `service.py`: DTOهای قرارداد legacy هستند و باید در مرحله جداگانه درباره بازنشستگی آن‌ها تصمیم گرفت.
- `service.py::ingest_codal_report`: persistence قدیمی RawFinancialFact را انجام می‌دهد؛ با این حال همان فایل توابع مستقل FX/OHLC دارد و نباید حذف شود.

**ج) وابستگی‌های schema و compatibility که با خاموش‌کردن PDF خودبه‌خود حذف نمی‌شوند**
- `src/models/normalized.py`: تعریف RawFinancialFact و FKهای مرتبط.
- `src/models/normalized_provenance.py`: FK به raw_financial_facts.
- `src/migrations/runner.py` و `src/scripts/init_db.py`: import مدل برای ثبت SQLAlchemy metadata و ساخت schema.
- `src/ingestion/__init__.py` و `src/ingestion/codal/__init__.py`: exportهای عمومی API legacy.
- سه FK به RawFinancialFact در مدل‌های MappingDecision، NormalizedFinancialFact و NormalizedFinancialFactInput.

**د) تست‌ها: دو گروه متفاوت**
1. PDF/extraction tests: `test_codal_acquisition.py`، `test_codal_extraction.py` و `test_codal_pdf_extraction.py`؛ این‌ها مستقیماً به قابلیت PDF وابسته‌اند.
2. legacy model/persistence/schema tests: `test_stage1_rules.py`، `test_stage1_database_architecture.py` و `test_stage1_database_integrity.py`؛ این‌ها قرارداد RawFinancialFact، mapping، FK و migration/data preservation را هم آزمایش می‌کنند و نباید صرفاً به‌عنوان تست PDF حذف شوند.
3. `test_stage5_forecast.py` در بخش snapshot ورودی‌های production، RawFinancialFact را می‌خواند تا اطمینان دهد اجرای forecast داده‌های منبع را تغییر نمی‌دهد. این وابستگی تست به جدول است، نه به استخراج PDF؛ تا زمان تغییر آگاهانه قرارداد source lineage باید حفظ یا با تست معادل جایگزین شود.

### 6.2 نتیجه معماری

دو تصمیم/کار باید جدا بمانند:

1. **بازنشستگی قابلیت استخراج و دریافت PDF:** حذف entry pointها، adapterها، parser و وابستگی‌های مخصوص PDF، پس از بررسی callerها و اصلاح facadeها و تست‌های PDF.
2. **بازنشستگی RawFinancialFact و schema legacy:** تصمیم مستقل درباره DTO/persistence، مدل، سه FK، migration runner، bootstrap و جایگزینی تست‌های قرارداد/حفظ provenance. صفر بودن لینک‌ها در snapshot محلی به‌تنهایی برای این کار کافی نیست.

در نتیجه، خاموش‌کردن PDF نباید به حذف فوری RawFinancialFact منجر شود. در کوتاه‌مدت می‌توان مسیر PDF را از persistence جدا کرد و جدول/مدل را دست‌نخورده نگه داشت؛ اما حتی این تغییر نیز باید با توجه به public API و تست‌های فعلی در یک تغییر کد مستقل طراحی شود.

### 6.3 وضعیت نهایی ممیزی

- Inventory محلی: **COMPLETE**.
- مرز اولیه PDF-only در برابر legacy/shared/schema: **IDENTIFIED**.
- بازنشستگی PDF: **NOT IMPLEMENTED**.
- بازنشستگی RawFinancialFact: **NOT AUTHORIZED**.
- مسیر production Excel-to-canonical: **NOT ESTABLISHED**.
- Migration 9 reconciliation: **OPEN**.
- هیچ source/ORM/Migration/data تغییر نکرده و هیچ تستی اجرا نشده است.

### 6.4 گام بعدی

تهیه یک طرح اجرایی مرحله‌ای برای بازنشستگی PDF به‌تنهایی، با فهرست دقیق فایل‌ها و APIهایی که حذف یا اصلاح می‌شوند، callerها و تست‌هایی که باید تغییر کنند، و مواردی که صریحاً باید حفظ شوند. این طرح باید از حذف جدول و مدل RawFinancialFact خارج از دامنه این مرحله پرهیز کند.
