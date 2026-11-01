# Stage 7 — Master Packet Update After Supplementary Audit

## نوع کار
DOCS-ONLY — فقط به‌روزرسانی `STAGE7_MASTER_WORKING_PACKET.md`.

## فایل‌های موردنیاز
1. `STAGE7_MASTER_WORKING_PACKET.md` — تنها فایل مجاز برای تغییر.
2. `WORKFLOW_RULES.md` — فقط برای رعایت قواعد جاری پروژه؛ READ-ONLY.
3. `reply.md` — منبع شواهد Supplementary Audit و نتیجهٔ اجرای تست PDF؛ READ-ONLY.

هیچ فایل دیگری را بررسی یا تغییر نده.
هیچ تست، برنامه، فرمان Git یا فرمان دیتابیس اجرا نکن.

## هدف
ثبت نتایج گزارش زیر در Master Packet و تهیهٔ فهرست دقیق کارهای باقی‌مانده:

`Supplementary Audit — Pytest Warnings, Skip Causes & Timestamp Safety`

## تغییرات الزامی

### 1. به‌روزرسانی Task 019 · S7-TEST-003
وضعیت را از OPEN به DONE تغییر بده؛ زیرا ممیزی Supplementary Audit علت هر دو Skip را مشخص کرده است:

- CODAL Golden PDF: نمونهٔ مناسب در مسیرهای candidate تست موجود یا معرفی نشده بود؛ وجود پوشهٔ `pdf/` به‌تنهایی تست Golden PDF را فعال نمی‌کند.
- openpyxl: بسته در interpreter اجرای تست محلی در دسترس نبوده و `pytest.importorskip()` آن را به Skip تبدیل کرده است؛ درحالی‌که dependency در `requirements.txt` وجود دارد و CI آن را نصب می‌کند.

DONE شدن Task 019 فقط به معنی تعیین علت Skipهاست؛ به معنی اصلاح کد یا حذف Skip نیست.

در داشبورد C-11 نیز همین وضعیت جدید ثبت شود. remediation مربوط به openpyxl به Task مستقل منتقل شود.

### 2. ثبت Supplementary Audit
در Master Packet یک بخش با عنوان مناسب برای این ممیزی اضافه کن و موارد زیر را ثبت کن:

- 153 رخداد `DeprecationWarning` در خروجی pytest.
- 24 محل `datetime.utcnow()` در سورس و تست‌ها.
- تفکیک تعداد Warningها از تعداد محل‌های کد.
- حفظ قرارداد فعلی `naive UTC`.
- عدم توصیه به تبدیل مستقیم timestampها به `aware UTC`.
- نیاز به regression test برای حفظ قرارداد زمانی در Audit، KPI و Trend.
- علت Skip مربوط به openpyxl و نیاز به تبدیل آن به dependency اجباری در تست.
- حفظ Skip مربوط به Golden PDF در محیط فاقد نمونهٔ واقعی مناسب؛ بدون انتخاب تصادفی PDF و بدون تضعیف معیار تست.

این بخش باید گزارش ممیزی را از کار اجرایی بعدی تفکیک کند.

### 3. ثبت کارهای اجرایی جدید
سه Task جدید با شماره‌های آزاد بعد از 057 ایجاد کن. پیش از انتخاب شماره و شناسه، کل Master Packet را بررسی کن تا هیچ شماره یا شناسه‌ای تکراری نباشد.

**Task A — Timestamp Warning Remediation**
- جایگزینی 24 محل `datetime.utcnow()` با روش سازگار با قرارداد فعلی naive UTC.
- اصلاح تست freeze مربوط به Trend.
- افزودن یا اصلاح regression test برای naive UTC.
- عدم تغییر فرمول‌های مالی، محاسبات KPI یا رفتار Trend.
- عدم filter یا مخفی‌کردن Warningها.
- اگر نیاز به helper مشترک وجود دارد، ابتدا layering و محل مناسب آن باید با شواهد بررسی شود.

**Task B — openpyxl Skip Remediation**
- تبدیل dependency اجباری openpyxl از رفتار `importorskip` به شکست روشن در صورت نصب نبودن.
- حفظ تست واقعی XLSX؛ حذف یا تضعیف تست ممنوع.
- نصب dependency و اجرای تست بر عهدهٔ کاربر است، نه Agent.

**Task C — Fzar PDF Extraction Failure Audit**
- نتیجهٔ اجرای واقعی کاربر برای `Fzar.pdf` ثبت شود.
- تست از Skip خارج شده و حداقل 5 ردیف استخراج کرده، اما assertion مربوط به وجود واژه‌های مورد انتظار در `item_name` شکست خورده است.
- علت دقیق هنوز مشخص نیست: استخراج متن/جدول یا نگاشت داده به `item_name`.
- این Task در ابتدا REPORT-ONLY/AUDIT است؛ تا پیش از اثبات علت، هیچ اصلاح کد یا تغییر معیار تست مجاز نیست.
- مناسب‌بودن فایل Fzar برای نمونهٔ Golden نیز باید از نظر محتوای واقعی گزارش بررسی شود؛ از روی نام فایل نتیجه‌گیری نکن.

برای هر Task جدید، شماره، شناسهٔ ثابت، وضعیت، وابستگی‌ها و معیار پذیرش را ثبت کن.

### 4. ثبت خروجی واقعی Fzar
این فرمان و نتیجهٔ آن را در بخش شواهد تست ثبت کن:

```powershell
$env:CODAL_SAMPLE_PDF = "D:\winprojects\analyzer\pdf\Fzar.pdf"
pytest src/tests/test_codal_extraction.py::test_real_codal_monthly_activity_pdf -q -rs
```

نتیجه:
- 1 failed
- تست از Skip خارج شد.
- حداقل 5 raw line استخراج شد.
- assertion خط 412 در `test_codal_extraction.py` شکست خورد؛ هیچ‌کدام از واژه‌های مورد انتظار در `item_name` نبودند.

این نتیجه را PASS یا مشکل حل‌شده ثبت نکن.

### 5. حفظ وضعیت Taskهای قبلی
صرفاً به دلیل تکمیل پنج بستهٔ ممیزی، Taskهای اجرایی را DONE نکن.

وضعیت‌های زیر باید حفظ شوند، مگر اینکه شواهد تازه و صریح در `reply.md` خلاف آن را اثبات کند:

- 022، 023، 024، 027: BLOCKED
- 029: PARTIAL
- 030: PARTIAL
- 032: BLOCKED
- 033: BLOCKED
- 034: OPEN
- 036: BLOCKED
- 037: OPEN
- 038: PARTIAL
- 039: BLOCKED
- 052: BLOCKED
- 053: PARTIAL؛ عملیات 053-10 باز است.
- 054 تا 057: OPEN

همچنین:
- 021 تا زمان اجرای تست‌های OA1 توسط کاربر OPEN بماند.
- 044 تا ارائهٔ شواهد کامل تست‌های لازم توسط کاربر OPEN بماند.
- 053-10، 054–057 و سایر موانع حیاتی در نقشهٔ کار باقی بمانند.

### 6. نقشهٔ اجرایی
در Master Packet یک خلاصهٔ اولویت‌بندی‌شده اضافه کن:

1. تکمیل اصلاح مستنداتی 053-10.
2. اجرای remediation مربوط به Forecast persistence در 054–057.
3. اصلاح Timestamp Warningها.
4. اصلاح Skip مربوط به openpyxl.
5. ممیزی علت شکست Fzar و سپس، فقط در صورت اثبات نقص، تعریف اصلاح کد.
6. تعیین تکلیف موانع OA1 و provenance تاریخی.
7. تعیین تکلیف مسیر واقعی تولیدی تا Stage 9 و E2E.
8. بازنگری نهایی engine پس از رفع یا تعیین تکلیف وابستگی‌ها.
9. اجرای تست‌های هدفمند و full suite توسط کاربر و سپس بستن معیارهای پایان Stage 7.

### 7. محدودیت‌های نهایی
- وضعیت کلی Stage 7 همچنان OPEN بماند.
- هیچ Task مسدودی صرفاً برای کوتاه‌شدن فهرست DONE نشود.
- هیچ فرمول مالی، threshold یا قرارداد provenance جدیدی اختراع نشود.
- `reply.md` و `WORKFLOW_RULES.md` تغییر نکنند.
- فقط `STAGE7_MASTER_WORKING_PACKET.md` تغییر کند.
- تاریخ آخرین بازنگری و خلاصهٔ تغییرات به‌روزرسانی شود.

## خروجی مورد انتظار
- نسخهٔ به‌روزشدهٔ Master Packet.
- فهرست Taskهای تغییر وضعیت‌یافته و دلیل هر تغییر.
- فهرست Taskهای جدید و وابستگی‌هایشان.
- خلاصهٔ نقشهٔ کار باقی‌مانده.

هیچ تستی اجرا نکن و هیچ ادعای اجرای تست نداشته باش.