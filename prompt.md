# Supplementary Audit — Pytest Warnings, Skip Causes & Timestamp Safety

## بخش اول — دستورالعمل Agent

### 1. نوع مأموریت

**REPORT-ONLY — NO CODE CHANGES**

این مأموریت برای ممیزی Warningهای خروجی تست، تعیین تکلیف دو Skip و ارائهٔ برنامهٔ اصلاح است.

- هیچ کدی را تغییر نده.
- هیچ تستی را تغییر نده.
- هیچ مستندی را تغییر نده.
- هیچ تست یا فرمانی اجرا نکن.
- هیچ Git operation انجام نده.
- هیچ فایلی را در GitHub یا مخزن ثبت نکن.
- گزارش را مستقیماً به کاربر تحویل بده.

### 2. محل اجرا و کنترل فایل‌ها

کار فقط روی نسخهٔ محلی پروژه `analyzer` انجام شود.

تمام فایل‌های زیر باید واقعاً در ZIP یا پوشهٔ کاری محلی Agent موجود باشند. پیش از شروع، وجود آن‌ها را بررسی کن.

فقط فایل‌های ارائه‌شده مجاز به بررسی هستند. اگر فایل دیگری ضروری بود، مسیر دقیق و دلیل نیاز را اعلام کن و متوقف شو.

`PROMPT.md` و `prompt.md` خارج از scope هستند.

تمام فایل‌های ورودی READ-ONLY هستند.

### 3. فایل‌های مجاز برای بررسی

**مستندات و تنظیمات**

- `WORKFLOW_RULES.md`
- `STAGE7_MASTER_WORKING_PACKET.md`
- `requirements.txt`
- `.github/workflows/tests.yml`

**کد**

- `src/ingestion/codal/ingestion.py`
- `src/models/audit.py`
- `src/kpi/universal.py`
- `src/kpi/conditional.py`
- `src/kpi/industry.py`
- `src/kpi/schema.py`
- `src/trend/engine.py`
- `src/trend/schema.py`

**تست‌ها**

- `src/tests/test_stage1_rules.py`
- `src/tests/test_stage2_kpis.py`
- `src/tests/test_stage4_trend.py`
- `src/tests/test_codal_extraction.py`
- `src/tests/test_ingestion_fx.py`
- `src/tests/test_codal_pdf_extraction.py`

**دادهٔ نمونه**

- تمام فایل‌های موجود در پوشهٔ محلی `pdf/`، فقط برای بررسی وجود و قابلیت استفاده به‌عنوان نمونهٔ PDF واقعی CODAL.

### 4. شواهد اجرای تست کاربر

این خروجی‌ها توسط کاربر اجرا شده‌اند و مبنای ممیزی هستند.

تست هدفمند:

```text
pytest src/tests/test_market_history_query.py src/tests/test_stage789_service_interface.py src/tests/test_stage7_valuation.py src/tests/test_stage8_market.py src/tests/test_stage9_decision.py -q -rs

862 passed in 5.54s
```

تست کامل:

```text
pytest src/tests -q -rs

1903 passed, 2 skipped, 153 warnings in 235.08s
```

علت Skipها در خروجی واقعی:

```text
SKIPPED [1] src\tests\test_codal_extraction.py:398:
real Codal sample PDF not available in CI

SKIPPED [1] src\tests\test_ingestion_fx.py:194:
could not import 'openpyxl': No module named 'openpyxl'
```

در Warning Summary، تمام Warningهای گزارش‌شده از نوع `DeprecationWarning` مربوط به `datetime.utcnow()` هستند.

محل‌های گزارش‌شده:

- `src/ingestion/codal/ingestion.py:84`
- `src/tests/test_stage1_rules.py:234`
- `src/kpi/universal.py:12, 17, 22, 27, 33, 38, 43, 48, 53, 60, 71`
- `src/kpi/conditional.py:33`
- `src/kpi/industry.py:12–16, 23–25, 39`
- `src/trend/engine.py:235`

این فهرست را با سورس واقعی تطبیق بده و اگر محل دیگری در Warning Summary وجود دارد، آن را نیز ثبت کن.

---

### 5. Task W-001 — ممیزی کامل 153 Warning

هدف، تعیین منشأ دقیق تمام Warningها و مشخص‌کردن اصلاح ایمن آن‌هاست.

برای هر محل فراخوانی `datetime.utcnow()` مشخص کن:

1. فایل و شماره خط.
2. تابع و مسیر اجرایی‌ای که آن را فراخوانی می‌کند.
3. نوع timestamp تولیدشده.
4. آیا timestamp به DB، API، خروجی محاسباتی یا صرفاً metadata داخلی منتقل می‌شود؟
5. آیا مصرف‌کنندگان آن naive UTC یا timezone-aware UTC انتظار دارند؟
6. آیا تبدیل نوع timestamp می‌تواند روی مقایسه، serialization، persistence یا PIT اثر بگذارد؟
7. چه تست‌هایی رفتار فعلی را تثبیت کرده‌اند؟

**بررسی ویژهٔ timestampها**

در `src/models/audit.py` تابع `_utc_now_naive()` وجود دارد که زمان UTC را به naive تبدیل می‌کند.

بررسی کن:

- آیا این تابع قرارداد موجود پروژه را نشان می‌دهد؟
- آیا برای تمام موارد Warning مناسب است؟
- آیا لایه‌های KPI و Trend قرارداد زمانی یکسانی دارند؟
- آیا تبدیل به timezone-aware می‌تواند ناسازگاری با مدل‌های SQLAlchemy یا تست‌ها ایجاد کند؟
- آیا بهتر است تابع مشترک و مشخصی برای تولید UTC timestamp ایجاد شود یا قراردادهای فعلی حفظ شوند؟

هیچ جایگزینی را صرفاً به دلیل پیشنهاد Python انجام‌شده و صحیح فرض نکن.

**خروجی مورد انتظار:**

یک جدول کامل شامل تمام محل‌های Warning، نوع داده، مصرف‌کننده، ریسک تغییر و روش اصلاح پیشنهادی.

همچنین مشخص کن آیا هر 153 Warning از همین call siteها ناشی شده‌اند یا خیر. تعداد Warningها را با تعداد call siteها اشتباه نگیر.

### 6. Task W-002 — تعیین تکلیف Skip مربوط به CODAL PDF

تست زیر Skip شده است:

`src/tests/test_codal_extraction.py:398`

شرط `_candidate_real_codal_paths()` و متغیر `CODAL_SAMPLE_PDF` را بررسی کن.

موارد لازم:

- تست دقیقاً چه مسیرهایی را برای نمونهٔ PDF بررسی می‌کند؟
- آیا پوشهٔ `pdf/` پروژه در این مسیرها قرار دارد؟
- آیا نمونه‌های واقعی موجود در پروژه قابل استفاده‌اند؟
- آیا کاربر باید متغیر محیطی `CODAL_SAMPLE_PDF` را تنظیم کند؟
- آیا Skip فقط برای CI بدون نمونهٔ واقعی قابل قبول است؟
- آیا امکان اجرای واقعی این تست در محیط محلی کاربر وجود دارد؟

Skip را بدون بررسی نمونه‌های واقعی، قابل قبول اعلام نکن.

### 7. Task W-003 — تعیین تکلیف Skip مربوط به openpyxl

تست زیر Skip شده است:

`src/tests/test_ingestion_fx.py:194`

شرط `pytest.importorskip("openpyxl")` را بررسی کن.

موارد لازم:

- آیا `openpyxl` در `requirements.txt` وجود دارد؟
- آیا GitHub Actions آن را از طریق requirements نصب می‌کند؟
- آیا این وابستگی در پروژه mandatory است یا optional؟
- چرا اجرای محلی کاربر نتوانسته آن را import کند؟
- آیا استفاده از `importorskip` برای وابستگی‌ای که در requirements اجباری اعلام شده مناسب است؟
- رفتار صحیح تست در نبود وابستگی چیست: Skip، Fail یا رفتار دیگری؟

فرمان دقیق نصب یا بازسازی محیط را پیشنهاد بده، اما اجرا نکن.

### اصلاح بخش W-002 — تعیین تکلیف Skip مربوط به CODAL PDF

**محدودیت مهم مصرف توکن:**

- فایل‌های PDF اصلی پروژه نباید داخل ZIP یا بستهٔ ورودی Agent قرار بگیرند.
- Agent اجازه ندارد PDFها را بازخوانی، استخراج متن یا تحلیل محتوایی کند.
- برای این Task، بررسی محتوای PDF ضروری نیست.

Agent فقط باید:

1. تابع `_candidate_real_codal_paths()` در `src/tests/test_codal_extraction.py` را بررسی کند.
2. مسیرهای جست‌وجوی نمونه PDF و متغیر محیطی `CODAL_SAMPLE_PDF` را مشخص کند.
3. ساختار پوشهٔ `pdf/` و صرفاً نام فایل‌های موجود در آن را بررسی کند.
4. تعیین کند آیا مسیر نمونه‌های موجود با مسیرهای مورد انتظار تست سازگار است یا خیر.
5. فرمان یا تنظیم محیطی لازم برای فعال‌کردن تست را پیشنهاد دهد.

اگر برای تشخیص مشکل واقعاً به محتوای PDF نیاز بود، Agent باید متوقف شود و نام فایل موردنیاز و دلیل ضرورت بررسی محتوای آن را اعلام کند.

در آن صورت، ابتدا فایل منتخب به Markdown تبدیل می‌شود و فقط نسخهٔ Markdown در اختیار Agent قرار خواهد گرفت.

**در این مأموریت هیچ PDF اصلی نباید به Agent تحویل داده شود.**

### 8. Task W-004 — برنامهٔ اصلاح و Regression

پس از ممیزی W-001 تا W-003، برنامهٔ اصلاح را ارائه بده.

برای هر اصلاح مشخص کن:

- فایل‌های دقیق مجاز برای تغییر در مرحلهٔ بعد.
- رفتار فعلی که باید حفظ شود.
- تست‌های رگرسیون لازم.
- خطر احتمالی تغییر قرارداد زمانی.
- فرمان‌های تست هدفمند.
- فرمان تست کامل.

در این مرحله هیچ اصلاحی انجام نده.

**ممنوعیت‌های مهم:**

- Warningها را با `filterwarnings` یا غیرفعال‌کردن Warningها پنهان نکن.
- تست‌ها را برای حذف Warning یا Skip ضعیف نکن.
- تست واقعی را حذف نکن.
- timestampها را بدون بررسی قرارداد مصرف‌کننده از naive به aware یا برعکس تبدیل نکن.
- برای رفع Warningها هیچ فرمول مالی، پارامتر، آستانه یا رفتار محاسباتی را تغییر نده.
- تعداد Warningها را صرفاً با کاهش خروجی گزارش‌شده کمتر اعلام نکن.

### 9. قالب گزارش

گزارش را دقیقاً با بخش‌های زیر تحویل بده:

1. **Input File Verification**
2. **W-001 — Complete Warning Inventory**
3. **Timestamp Contract & Compatibility Analysis**
4. **W-002 — CODAL PDF Skip Disposition**
5. **W-003 — openpyxl Skip Disposition**
6. **W-004 — Safe Remediation Plan**
7. **Exact Files to Change in the Next Phase**
8. **Required Regression Tests**
9. **Recommended Test Commands**
10. **Unresolved Risks and Dependencies**

برای هر نتیجه، فایل و شماره خط را ذکر کن.

اگر چیزی اثبات نشده است، صریحاً بنویس «اثبات نشده».

هیچ Taskی را در Master Packet تغییر نده؛ گزارش را مستقیماً به کاربر تحویل بده.

## بخش دوم — دستور کار کاربر

### Task List

- [ ] ممیزی کامل 153 Warning و تعیین منشأ آن‌ها.
- [ ] بررسی ایمنی قراردادهای UTC و timestampها.
- [ ] تعیین تکلیف Skip مربوط به نمونهٔ PDF واقعی CODAL.
- [ ] تعیین تکلیف Skip مربوط به `openpyxl`.
- [ ] ارائهٔ برنامهٔ اصلاح کد و تست‌های Regression بدون اجرای تست توسط Agent.

### Expected Result

گزارش دقیق منشأ Warningها و Skipها، همراه با برنامهٔ اصلاح ایمن و فهرست فایل‌های لازم برای مرحلهٔ بعد.

**این مأموریت REPORT-ONLY است و هیچ فایلی تغییر نمی‌کند.**