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
