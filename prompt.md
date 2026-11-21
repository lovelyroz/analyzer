# Task DB-TEST-002-CORRECTION — Align Stage 6 Test Fixtures with Runtime ForecastRecord

## نوع کار
**Code change + test correction**

## هدف
رفع ۴۲ خطای ثبت‌شده در `zErrors.md` با هماهنگ‌کردن fixtureهای تست Stage 6 با قرارداد فعلی `ForecastRecord`.

علت اصلی شناسایی‌شده:
- تست‌ها هنوز `forecast_id` را به `ForecastRecord` می‌فرستند.
- تست‌ها هنوز `forecast_version` را به `ForecastRecord` می‌فرستند.
- هیچ‌کدام از این دو فیلد در dataclass فعلی `src/forecast/schema.py` تعریف نشده‌اند.
- `ForecastRecord` یک runtime record است و شناسه دیتابیسی یا version assignment ندارد.

## فایل‌های مجاز برای تغییر

1. `src/tests/test_stage6_p25_selection.py`
2. `src/tests/test_stage6_p25_adversarial.py`
3. `src/tests/test_stage6_evaluation_foundation.py`

ابتدا `src/forecast/schema.py` و تمام failureهای مربوط به این سه فایل در `zErrors.md` را بررسی کن.

## الزامات اجرایی

### 1. اصلاح fixtureها
در تابع `_record()` هر سه فایل:
- `forecast_id` را حذف کن.
- `forecast_version` را حذف کن.
- سایر فیلدها را دقیقاً مطابق قرارداد فعلی `ForecastRecord` نگه دار.
- تمام overrideهای تست‌ها را بررسی کن تا هیچ تستی به‌صورت غیرمستقیم این دو فیلد را ارسال نکند.

### 2. حفظ معنای تست‌ها
صرفاً حذف دو آرگومان کافی نیست. تمام تست‌هایی را که به شناسه یا نسخه پیش‌بینی وابسته‌اند بررسی کن.

به‌خصوص:
- تست `test_key_forecast_id_does_not_affect_key` را با قرارداد فعلی بازنویسی کن.
- چون `ForecastRecord` شناسه دیتابیسی ندارد، تست باید نشان دهد هویت EvaluationKey به فیلدهای قراردادی ForecastRecord وابسته است و نه شناسه دیتابیسی فرضی.
- اگر یک assertion دیگر با قرارداد فعلی بی‌معنا شده، آن را با تستی معنادار و منطبق با تصمیم معماری جایگزین کن.
- تست‌های PIT، انتخاب Actual، سناریو، Horizon، Model Version، کیفیت داده و quarantine را حفظ کن.
- assertionها را برای سبزشدن مصنوعی تست ضعیف نکن.

### 3. محدودیت‌های مهم
- هیچ فایل production را تغییر نده.
- `src/forecast/schema.py` را تغییر نده.
- هیچ شناسه یا فیلد حذف‌شده‌ای را به مدل برنگردان.
- قرارداد Stage 6، Stage 5 یا EvaluationKey را بدون ضرورت تغییر نده.
- تست‌های نامرتبط را حذف یا skip نکن.
- هیچ تغییر ORM، schema، migration یا database انجام نده.
- فایل `WORKFLOW_RULES.md` مطلقاً نباید تغییر کند.
- تست‌ها را اجرا نکن؛ اجرای تست با مالک پروژه است.

## کنترل نهایی

قبل از تحویل:
1. هر سه فایل را برای باقی‌ماندن `forecast_id` و `forecast_version` در سازنده `ForecastRecord` بررسی کن.
2. تمام محل‌های استفاده از این دو نام را بررسی کن؛ صرفاً حذف کورکورانه کافی نیست.
3. اطمینان بده که هیچ تستی به‌خاطر این اصلاح حذف یا غیرفعال نشده است.
4. تغییرات را با diff بررسی کن.

## گزارش تحویل

گزارش را در `database/reports/DB_TEST_002_CORRECTION.md` ایجاد کن و شامل این موارد باشد:
- علت دقیق ۴۲ خطا
- فایل‌های تغییرکرده
- تعداد و نوع تست‌های اصلاح‌شده
- توضیح تغییر تست وابسته به `forecast_id`
- تأیید عدم تغییر production و schema
- دستور دقیق تست برای اجرای مالک پروژه
- وضعیت: `READY_FOR_OWNER_TEST`

`reply.md` و `database/DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md` را نیز به‌روزرسانی کن:
- این اصلاح را به‌عنوان correction برای Task DB-TEST-002 ثبت کن.
- تا قبل از موفقیت تست مالک، Task را DONE اعلام نکن.
- آمار داشبورد را بدون محاسبه و بررسی واقعی تغییر نده.

## خروجی نهایی ایجنت

در پاسخ نهایی دقیقاً اعلام کن:
- `DONE` یا `PARTIAL`
- فایل‌های تغییرکرده
- خلاصه اصلاحات
- تأیید اینکه تست اجرا نکرده‌ای
- دستور تست مالک
- هر مانع یا مورد باز باقی‌مانده

هیچ ادعای موفقیت تست بدون اجرای واقعی و خروجی معتبر مجاز نیست.