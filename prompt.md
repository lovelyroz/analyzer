# Task 034 — DB-ING-007
## هم‌راستاسازی Market/FX File Adapters

مرجع تصمیم‌ها:
- `database/DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md` §§9.31–9.32
- قراردادهای مصوب MarketDaily و FX

### هدف
اصلاح parser و preflight فایل‌های بازار و ارز مطابق تصمیم‌های قطعی مالک. این Task اجرایی است، نه تحقیقاتی.

### ۱. MarketDaily
فقط این ستون‌ها پردازش شوند:
- `J-Date`
- `Ticker`
- `Close`
- `Volume`
- `No`
- `Value`

ستون‌های `Open`، `High`، `Low` و `Final` نباید وارد mapping شوند.

### ۲. FX
- برای FREE_MARKET و EXCHANGE_CENTER دقیقاً یک parser مشترک استفاده شود.
- ساختار واقعی workbook و Headerها شناسایی شوند.
- فقط ستون فروش خوانده شود؛ ستون خرید وارد نرخ canonical نشود.
- EXCHANGE_CENTER: نرخ ریال، بدون تبدیل.
- FREE_MARKET: نرخ تومان، تبدیل دقیق ×۱۰ به ریال.
- هیچ منبع خارجی، URL، API یا download manifest مطالبه نشود.

### ۳. اعتبارسنجی
- تاریخ و مقادیر نامعتبر نباید بی‌صدا حذف شوند.
- Header یا ستون نامعتبر باید diagnostic مشخص داشته باشد.
- duplicateهای داخلی و payloadهای متعارض باید شناسایی شوند.
- نتیجهٔ validation باید قابل تکرار و deterministic باشد.

### ۴. محدودیت‌های غیرقابل مذاکره
- هیچ تغییر ORM، schema، migration یا دیتابیس انجام نشود.
- هیچ داده‌ای وارد دیتابیس واقعی نشود.
- هیچ overwrite یا partial persistence جدیدی پیاده‌سازی نشود.
- Migration 9 و cleanup آن دست‌نخورده بمانند.
- مسیر UI و ShareCountHistory/CorporateAction خارج از دامنه‌اند.
- هیچ تصمیم مصوب مالک دوباره به‌عنوان سؤال مطرح نشود.

### ۵. AGENT VERIFICATION
ایجنت باید تست‌های خودکار parser و preflight را در محیط ایزوله بنویسد و اجرا کند. فرمان دقیق، خروجی واقعی و تعداد تست‌های موفق و ناموفق گزارش شود.

### ۶. USER ACCEPTANCE TEST
ایجنت باید فرمان دقیق preflight برای فایل‌های زیر ارائه کند:
- `saman_price_history.csv`
- `dollar-history.xlsx`

همچنین حالت FREE_MARKET و تبدیل ×۱۰ باید با fixture آزمایشی بررسی شود.

کاربر تست پذیرش را اجرا می‌کند و خروجی را می‌فرستد. ایجنت حق ندارد پذیرش کاربر را انجام‌شده اعلام کند.

### ۷. معیار تکمیل
- mapping صحیح MarketDaily
- parser مشترک FX
- انتخاب صحیح ستون فروش
- تبدیل صحیح واحد FREE_MARKET
- تشخیص خطا و duplicate/conflict
- تست‌های خودکار موفق
- CLI و مستندات به‌روز
- بدون تغییر دیتابیس یا schema

در پایان، `reply.md` را با شواهد، فایل‌های تغییرکرده، فرمان‌ها و خروجی واقعی تست‌ها به‌روزرسانی کن. وضعیت Task را فقط بر اساس معیارهای بالا تعیین کن.