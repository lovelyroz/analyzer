# DB-IMPL-002 — Opt-in Canonical BANK Read Bridge for Stage 5/6

## نوع کار
**CODE CREATE/CHANGE + TESTS CREATE/CHANGE + DOCUMENTATION UPDATE**

هدف: ایجاد لایه خواندن سازگار و صریح از مدل canonical جلالی برای مصرف Stage 5 و Stage 6، بدون تغییر ناخواسته مسیر legacy و بدون فرض‌سازی درباره نگاشت‌های مالی بانک‌ها.

## تصمیم‌های قطعی
1. دامنه فقط صنعت BANK است.
2. گزارش دوره‌ای بانک (`PERIODIC_FINANCIAL`) مبنای YTD دارد. مقادیر مستقل فصل فقط در runtime و از تفاضل YTDهای سازگار محاسبه می‌شوند.
3. مقادیر محاسبه‌شده نباید در دیتابیس ذخیره شوند.
4. تاریخ و ترتیب دوره‌ها باید Jalali-native بماند؛ تبدیل Gregorian برای هویت یا مقایسه دوره ممنوع است.
5. انتخاب نسخه باید PIT-safe باشد و رتبه‌بندی حسابرسی/تجدید ارائه مصوب را حفظ کند.
6. ابعاد، واحد، ارز، مقیاس و ماهیت زمانی Fact باید صریح کنترل شوند. جمع‌زدن خودکار ابعاد یا تبدیل ضمنی واحد/ارز ممنوع است.
7. هیچ Metric ID یا نگاشت اقتصادی را از روی نام، شباهت یا حدس تعیین نکن.
8. مسیر legacy فعلی Stage 5/6 باید بدون تغییر رفتار باقی بماند.
9. انتخاب مسیر canonical باید opt-in و صریح باشد. اگر داده یا نگاشت لازم موجود نیست، مسیر canonical باید fail-closed عمل کند؛ حق fallback پنهانی به legacy ندارد.
10. هیچ DB واقعی، Migration، داده موجود یا `WORKFLOW_RULES.md` نباید تغییر کند.

## دامنه پیاده‌سازی

### A. بررسی قراردادهای موجود
فقط این فایل‌ها و وابستگی مستقیم لازم را بررسی کن:
- `src/forecast/canonical_queries.py`
- `src/forecast/queries.py`
- `src/forecast/service.py`
- `src/forecast/schema.py`
- `src/kpi/engine.py`
- `src/kpi/industry.py`
- `src/models/canonical.py`
- تست‌های Stage 5 و Stage 6 مرتبط

از بازبینی گسترده و نامرتبط کل `src/` خودداری کن.

### B. Canonical Stage 5 adapter
یک adapter مستقل و قابل‌آزمون بساز که:
- فقط برای شرکت BANK و گزارش `PERIODIC_FINANCIAL` قابل استفاده باشد.
- ورودی آن شامل نگاشت صریح و caller-supplied از کلیدهای مصرف‌کننده Stage 5 به `metric_id` و مشخصات مورد انتظار باشد؛ حداقل temporal type، unit، currency، scale و dimension selection.
- نگاشت ناقص، تکراری، ناسازگار یا دارای ابعاد مبهم را رد کند.
- برای Factهای DURATION/YTD از `derive_standalone_quarters()` استفاده کند.
- برای Factهای INSTANT، مقدار را به‌عنوان مانده در تاریخ خودش نگه دارد.
- دوره‌های جریان و مانده را فقط با هویت زمانی سازگار کنار هم قرار دهد.
- ترتیب دوره‌ها را با اجزای Jalali تعیین کند.
- برای هر Fact، `ForecastInputRef` با شناسه نسخه و زمان انتشار واقعی تولید کند.
- فقط پس از اعتبارسنجی واحد/ارز/مقیاس، مقدار را در مرز ورود به موتور Stage 5 به نوع عددی مورد انتظار آن تبدیل کند.
- نبود هر ورودی لازم را missing نگه دارد؛ صفر جایگزین نکند.
- هیچ Fact legacy را با canonical در یک مجموعه ترکیب نکند.

اتصال به `generate_forecast()` فقط در صورتی مجاز است که با یک پارامتر opt-in صریح انجام شود و فراخوانی‌های قبلی دقیقاً رفتار قبلی خود را حفظ کنند. اگر قرارداد فعلی Stage 5 برای دریافت دوره Jalali کافی نیست، آن را پنهانی به Gregorian تبدیل نکن؛ محدودیت را در adapter حل کن یا با یک خطای صریح متوقف شو.

### C. Canonical Stage 6 adapter
یک adapter مستقل برای تبدیل Factهای canonical به ورودی `KPIEngine` بساز:
- فقط BANK را قبول کند.
- کلیدهای ورودی مانند `nii`، `nim`، `loan_growth`، `deposit_growth` و `npl` فقط از نگاشت صریح caller تأمین شوند.
- هیچ محاسبه اقتصادی جدید یا معادل‌سازی Metric انجام نده.
- وضعیت کیفیت و نبود مقدار را بدون تبدیل missing به zero منتقل کند.
- `period_id` canonical و provenance را در خروجی runtime حفظ کند.
- هیچ خروجی KPI یا Fact مشتق‌شده‌ای در DB ذخیره نشود.

### D. اصلاح canonical query API
در صورت نیاز، `load_canonical_financial_facts()` را به‌شکلی توسعه بده که فیلتر report type و dimension selection صریح داشته باشد. رفتار پیش‌فرض و تست‌های فعلی نباید شکسته شوند.

### E. تست‌ها
تست‌های جدید باید حداقل این موارد را پوشش دهند:
1. PIT cutoff: نسخه منتشرشده بعد از cutoff هرگز وارد خروجی نشود.
2. انتخاب رتبه کیفیت و رفع تساوی با انتشار جدیدتر.
3. تفاضل YTD فقط برای زنجیره کامل و سازگار.
4. عدم اختلاط report typeها و عدم پذیرش MONTHLY_ACTIVITY به‌عنوان PERIODIC_FINANCIAL.
5. جداسازی ابعاد؛ نبود انتخاب دقیق بُعد باید reject شود.
6. mismatch در unit/currency/scale باید reject شود.
7. نگاشت Metric ناقص یا تکراری باید reject شود.
8. Fact مانده و جریان با قواعد زمانی متفاوت پردازش شوند.
9. missing با zero اشتباه نشود.
10. مسیر canonical و legacy هرگز در یک فراخوانی مخلوط نشوند.
11. فراخوانی‌های قبلی Stage 5 و Stage 6 بدون پارامتر جدید، همان رفتار قبلی را حفظ کنند.
12. Stage 6 فقط ورودی‌های صریحاً نگاشت‌شده را دریافت کند.

از fixtureهای synthetic استفاده کن؛ هیچ نگاشت synthetic را به‌عنوان استاندارد تولیدی بانک ثبت نکن.

## فایل‌ها و اسناد
- ماژول‌های adapter جدید را در محل مناسب `src/forecast/` و `src/kpi/` ایجاد کن.
- تست‌های جدید را در فایل تست مستقل قرار بده.
- `database/reports/DB_IMPL_002_CANONICAL_STAGE5_STAGE6_READ_BRIDGE.md` را ایجاد کن.
- `database/DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md` را با نتیجه واقعی و محدودیت‌های باقی‌مانده به‌روزرسانی کن.
- `reply.md` فقط handoff موقت است؛ اطلاعات ماندگار باید در گزارش و Master Packet ثبت شود.
- `WORKFLOW_RULES.md` را تغییر نده.

## خارج از دامنه
- ساخت یا تأیید Metric mapping واقعی بانک‌ها
- تغییر فرمول‌های Stage 5/6
- تغییر مدل ORM یا Schema یا Migration
- مهاجرت داده یا dual-write
- تغییر مسیر پیش‌فرض legacy
- ساخت استاندارد برای صنایع غیر از BANK
- تغییر داده یا دیتابیس واقعی
- تغییر فایل‌های PDF یا احیای PDF extraction

## معیار پذیرش
- adapterهای مستقل و opt-in با تست‌های synthetic کامل باشند.
- مسیر legacy بدون تغییر رفتار باقی بماند.
- هیچ نگاشت تولیدی یا فرض مالی جدیدی ساخته نشده باشد.
- PIT، provenance، Jalali، dimension و temporal semantics در تست‌ها اثبات شوند.
- فرمان‌های دقیق تست برای اجرای مالک ارائه شوند؛ **ایجنت تست‌ها را اجرا نکند**.
- هیچ Task به DONE تغییر نکند مگر اینکه تمام معیارهای همان Task واقعاً بسته شده باشند.

در گزارش، فایل‌های تغییرکرده، محدودیت‌های فنی، تست‌های اضافه‌شده، فرمان دقیق اجرای تست و موارد باقی‌مانده را بنویس. ادعای production readiness نکن.