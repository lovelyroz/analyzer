# EXECUTION PROMPT — Task 017 Acceptance Record + Task 018 / DB-TEST-002

Repository: `analyzer`  
Branch: `master`

## نوع کار
**Code create/change — تست‌های خودکار و مستندات وضعیت Taskها.**

این اجرا باید Task 018 را واقعاً پیش ببرد؛ صرف بررسی فایل‌ها یا نوشتن گزارش، انجام Task محسوب نمی‌شود.

## بخش اول — ثبت پذیرش مالک برای Task 017

نتیجه اجرای مالک را عیناً ثبت کن:

```text
.\.venv\Scripts\python.exe -m pytest -q --basetemp .pytest_task017_20261120 src/tests/test_task017_model_constraints.py src/tests/test_stage1_database_integrity.py

23 passed in 76.32s (0:01:16)
```

در `reply.md` و بخش وضعیت Task 017 در `database/DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md` ثبت کن که اجرای تست توسط مالک موفق بوده است.

**Task 017 همچنان PARTIAL است.** موارد زیر نباید به‌عنوان حل‌شده اعلام شوند:
- نبود constraint جلالی برای FinancialPeriod در مدل فعلی؛
- محدودیت پوشش schemaهای پشتیبانی‌شده؛
- شکاف‌های uniqueness ناشی از NULL در SQLite؛
- تضمین‌های محیط production و concurrency.

فقط نتیجه پذیرش مالک را ثبت کن. Task 017 را DONE نکن.

## بخش دوم — اجرای Task 018 / DB-TEST-002

هدف: ساخت مجموعه تست‌های خودکار برای اثبات رفتار ingestion و Point-in-Time (PIT) بر اساس قراردادهای مصوب و مرزهای پیاده‌سازی موجود.

ابتدا فقط فایل‌های مرتبط زیر را بررسی کن و از تست‌ها و پیاده‌سازی‌های موجود استفاده مجدد کن:

- `src/ingestion/canonical_admission.py`
- `src/ingestion/excel/canonical_input.py`
- `src/ingestion/excel/adapter.py`
- `src/ingestion/excel/deterministic_matcher.py`
- `src/ingestion/market/ingestion.py`
- `src/ingestion/service.py`
- `src/ingestion/common/atomic.py`
- ماژول‌های موجود Report / ReportVersion / FinancialPeriod / NormalizedFinancialFact
- تست‌های موجود مربوط به همین ماژول‌ها، به‌ویژه تست‌های Task 014 تا 017 و تست‌های atomic ingestion.

از ایجاد تست تکراری که همان رفتار را قبلاً به‌طور مؤثر پوشش داده خودداری کن.

### 2.1 پوشش‌های الزامی

برای هر مورد، تست مثبت و منفی مناسب بنویس:

**A. Multi-period و Temporal semantics**
- گزارش دارای چند دوره و چند مقدار زمانی؛
- تمایز INSTANT و DURATION؛
- تمایز YTD و STANDALONE؛
- ممنوعیت duration_basis برای INSTANT؛
- رد period یا temporal mapping ناقص، مبهم یا ناسازگار؛
- جلوگیری از ترکیب ناخواسته دوره‌ها یا نسخه‌های ناسازگار.

**B. ReportVersion و correction**
- حفظ نسخه قبلی هنگام ورود correction؛
- correction به‌عنوان نسخه جدید و بدون overwrite نسخه قبلی؛
- replay همان نسخه با payload یکسان؛
- رد replay با payload متفاوت؛
- انتخاب نسخه هم‌رتبه جدیدتر بر اساس تاریخ انتشار معتبر؛
- عدم استفاده از نسخه‌ای که بعد از PIT منتشر شده است؛
- عدم انتخاب خودکار در نبود تاریخ انتشار معتبر یا ترتیب زمانی قابل اثبات.

**C. Provenance**
- حفظ ارتباط candidate و persistence plan با company، report، report version، metric، period، template/standard و approval references؛
- رد provenance ناقص یا متناقض؛
- جلوگیری از یکی‌گرفتن دو مقدار اقتصادی که provenance متفاوت دارند؛
- عدم ایجاد الزام دائمی برای exact workbook/sheet/cell locator، برخلاف تصمیم مالک.

**D. Atomicity و batch admission**
- اعتبارسنجی کامل batch پیش از پذیرش؛
- وجود یک ردیف نامعتبر باید کل batch را رد کند؛
- duplicate یکسان باید بدون درج مجدد تشخیص داده شود؛
- conflict باید کل batch را رد کند؛
- شکست در مراحل persistence/commit نباید partial canonical write باقی بگذارد؛
- وضعیت audit در حد تضمین واقعی پیاده‌سازی بررسی شود؛
- هیچ تستی نباید تضمین concurrency یا DB uniqueness را فراتر از توان schema فعلی ادعا کند.

**E. Mapping**
- فقط mapping صریح و approved پذیرفته شود؛
- mapping مفقود، چندمعنا، تکراری یا ناسازگار باید fail-closed باشد؛
- mappingهای پیشنهادی یا candidate-only نباید به‌عنوان mapping تولیدی پذیرفته شوند؛
- تطبیق صرفاً بر اساس شباهت متن یا حدس ممنوع است.

**F. NULL، صفر و ZERO_FALLBACK**
- NULL/BLANK از صفر واقعی متمایز باشد؛
- صفر گزارش‌شده حفظ شود؛
- ZERO_FALLBACK فقط با approval صریح و منطبق پذیرفته شود؛
- نبود approval یا approval ناسازگار باید رد شود؛
- هیچ مقدار ساختگی نباید به‌عنوان مقدار گزارش‌شده ثبت شود.

**G. ممنوعیت raw/calculated persistence**
- raw rows و calculated facts نباید از مرز admission عبور کنند؛
- محاسبات runtime-only نباید به‌عنوان fact گزارش‌شده پذیرفته شوند؛
- plan باید غیرقابل‌اجرا باقی بماند (`execution_allowed=False`) تا writer و schema مصوب وجود داشته باشند؛
- تست‌ها نباید صرفاً با بررسی یک flag، نبود persistence ممنوع را در کل برنامه اثبات‌شده اعلام کنند. ادعا باید محدود به مرز واقعی تست‌شده باشد.

### 2.2 قواعد اجرای تست

- تست‌ها باید deterministic و مستقل از ترتیب اجرا باشند.
- برای تست‌های دیتابیسی فقط از temporary isolated database استفاده کن.
- هیچ دیتابیس واقعی یا owner database را باز نکن.
- هیچ داده واقعی یا production ingestion اجرا نکن.
- تست‌ها نباید به شبکه یا سرویس خارجی وابسته باشند.
- تست‌های موجود را بی‌دلیل حذف یا تضعیف نکن.
- اگر یک رفتار به‌علت محدودیت schema یا نبود writer قابل اثبات نیست، آن را صریحاً به‌عنوان GAP ثبت کن؛ با mock یا assertion صوری، PASS جعلی نساز.
- در صورت کشف bug واقعی در کد pure/service، فقط اصلاح محدود و ضروری همان بخش مجاز است؛ تغییر ORM، schema، migration یا database ممنوع است.

## محدودیت‌های غیرقابل‌مذاکره

- هیچ تغییری در ORM، schema، migration یا دیتابیس.
- Migration 9 را اجرا یا ایجاد نکن؛ Migration 10 نساز.
- هیچ cleanup یا ingestion واقعی اجرا نکن.
- هیچ Template یا mapping پیشنهادی را approved نکن.
- `WORKFLOW_RULES.md` را تغییر نده.
- قراردادهای مصوب مالک را دوباره باز نکن.
- تست‌ها را خودت اجرا نکن؛ اجرای تست با مالک است.

## فایل‌های مجاز برای تغییر

- تست‌های جدید یا موجود مرتبط با Task 018 در `src/tests/`
- اصلاح محدود کد pure/service فقط در صورت کشف bug اثبات‌شده
- `database/reports/DB_TEST_002_INGESTION_PIT_TESTS.md` (گزارش جدید)
- `database/DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md`
- `reply.md`

فایل‌های دیگر فقط در صورت ضرورت فنی و با توضیح دقیق؛ بدون تغییر سند معماری یا `WORKFLOW_RULES.md`.

## معیار پایان Task 018

Task 018 فقط زمانی DONE است که:
1. تمام هفت گروه پوشش بالا با تست‌های واقعی و معنادار پوشش داده شده باشند؛
2. تست‌ها در اختیار مالک برای اجرا قرار گرفته باشند؛
3. هیچ تستی به‌صورت mock یا assertion صوری، رفتار پیاده‌سازی‌نشده را PASS نکند؛
4. محدودیت‌ها و GAPهای اثبات‌نشده صریحاً ثبت شده باشند؛
5. فرمان اجرای کامل و دقیق تست‌ها ارائه شده باشد.

اگر هر بخش مهم به علت نبود writer، schema یا قرارداد اجرایی قابل تست نیست، Task را PARTIAL نگه دار و دقیقاً مشخص کن چه چیزی مانع تکمیل است.

## گزارش اجباری

در `reply.md` و گزارش مستقل، این موارد را ثبت کن:

1. وضعیت Task 017 و ثبت نتیجه پذیرش مالک: `23 passed in 76.32s`.
2. وضعیت Task 018: DONE یا PARTIAL با دلیل.
3. شناسه و عنوان دقیق تمام Taskهای اجراشده.
4. فهرست تست‌های اضافه/اصلاح‌شده و رفتار هرکدام.
5. فهرست فایل‌های تغییرکرده.
6. فرمان دقیق تست برای اجرای مالک.
7. GAPهای باقی‌مانده و اینکه هرکدام ناشی از تست، کد، schema یا نبود writer است.
8. تأیید صریح عدم تغییر ORM/schema/migration/DB و عدم اجرای تست توسط ایجنت.

در Master Packet:
- نتیجه پذیرش مالک Task 017 را ثبت کن.
- Task 017 را PARTIAL نگه دار.
- وضعیت Task 018 را بر اساس پوشش واقعی تعیین کن.
- داشبورد را بر اساس وضعیت واقعی Taskها دوباره محاسبه کن.
- هیچ Task دیگری را صرفاً به دلیل پیشرفت این اجرا DONE نکن.

**اولویت: تست‌های جدید و ارزشمند برای Task 018 بساز؛ ممیزی‌های تکراری و گزارش‌سازی بدون پیشرفت ممنوع.**