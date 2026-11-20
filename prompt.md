# اصلاح اجرای Task 035 — اجرای واقعی DB-ING-008 و اصلاح وضعیت Task 034

**نوع کار: کدنویسی و تغییر واقعی کد + تست خودکار + اصلاح مستندات. گزارش‌نویسی صرف پذیرفته نیست.**

در بررسی شاخه `master` مشخص شد:
- Task 034 / DB-ING-007 توسط مالک UAT شده است: 24 تست موفق و preflight با وضعیت WARNING.
- با این وجود، Master Packet هنوز Task 034 را انجام‌نشده معرفی می‌کند.
- کدهای `src/ingestion/market/ingestion.py` و `src/ingestion/service.py` هنوز partial commit و overwrite رکورد موجود را انجام می‌دهند.
- گزارش و تست مشخصی برای DB-ING-008 وجود ندارد.

## بخش اول — اصلاح مستندات Task 034

در Master Packet:
1. Task 034 را با استناد به UAT واقعی مالک DONE ثبت کن.
2. نتایج زیر را دقیق ثبت کن:
   - `24 passed`
   - preflight: `MarketDaily: WARNING`
   - `EXCHANGE_CENTER: WARNING`
   - `Overall: WARNING`
3. WARNINGهای باقی‌مانده را فقط در صورت ارتباط با provenance خارجی blocker تلقی نکن؛ تصمیم §9.31 مالک بر آن‌ها مقدم است.
4. متن قدیمی §9.32 را که Task 034 را انجام‌نشده معرفی می‌کند اصلاح کن. تاریخچه را حذف نکن؛ وضعیت جاری را صریح و بدون تناقض ثبت کن.

## بخش دوم — اجرای واقعی Task 035 / DB-ING-008

**هدف:** پیاده‌سازی atomic ingestion و جلوگیری از overwrite بی‌ضابطه در Market و FX.

فایل‌های اصلی:
- `src/ingestion/market/ingestion.py`
- `src/ingestion/service.py`
- `src/ingestion/common/identity.py`
- `src/ingestion/common/validation.py`
- مدل‌ها و تست‌های موجود فقط برای بررسی سازگاری

فایل‌های تست جدید/موجود را متناسب با ساختار پروژه ایجاد یا اصلاح کن.

### الزامات پیاده‌سازی

1. کل Batch باید پیش از نوشتن داده canonical اعتبارسنجی شود.
2. وجود حتی یک ردیف نامعتبر، کل Batch را رد کند؛ هیچ ردیف معتبری از همان Batch نباید ذخیره شود.
3. کلید اقتصادی موجود:
   - payload کاملاً یکسان: duplicate بدون تغییر.
   - payload متفاوت: conflict و رد کل Batch.
   - overwrite ممنوع.
4. برای Market از هویت جلالی موجود استفاده کن.
5. فیلد `Value` مستقل باقی بماند و از `Volume × Close` محاسبه نشود.
6. ستون‌های Open/High/Low/Final وارد قرارداد مصوب Market نشوند.
7. نرخ FX که Adapter قبلاً به Rial/USD تبدیل کرده، نباید در persistence دوباره ×10 شود.
8. `IngestionRun` باید تعداد رکوردهای پیدا‌شده، درج‌شده، تکراری، نامعتبر و وضعیت نهایی را درست منعکس کند.
9. ثبت STARTED باید از تراکنش داده canonical مستقل و پایدار باشد.
10. تمام canonical writes و وضعیت COMPLETED باید در یک تراکنش باشند.
11. در هر خطا یا شکست commit، تمام canonical writes rollback شوند و FAILED در تراکنش جداگانه ثبت شود.
12. هیچ commit داخل حلقه ردیف‌ها انجام نشود.
13. error log نباید payload حساس یا traceback خام غیرضروری را افشا کند.

### سناریوهای تست الزامی

- Batch معتبر چندردیفی
- یک ردیف نامعتبر در Batch چندردیفی و اثبات نبود هرگونه ذخیره جزئی
- duplicate با payload یکسان
- duplicate با payload متفاوت
- کلید از قبل موجود با payload یکسان
- کلید از قبل موجود با payload متفاوت
- شکست پس از ایجاد حداقل یک pending write و اثبات rollback
- ثبت صحیح FAILED و شمارنده‌ها
- شکست commit
- شکست ثبت audit
- رفتار دو Session مستقل و محدودیت concurrency

### محدودیت‌های قطعی

- هیچ ORM، schema، migration یا دیتابیس واقعی تغییر نکند.
- Migration 9 دست‌نخورده بماند.
- migration جدید ساخته نشود.
- cleanup یا ingestion واقعی اجرا نشود.
- CODAL و ShareCountHistory و CorporateAction خارج از دامنه‌اند.
- نبود unique constraint فیزیکی روی کلید جلالی را پنهان نکن. محدودیت concurrency را دقیق مستند کن و ادعای تضمین یکتایی هم‌زمان نداشته باش.
- اگر CheckConstraint یا مدل فعلی FX از `EXCHANGE_CENTER` پشتیبانی نمی‌کند و اصلاح آن به schema/migration نیاز دارد، آن را به‌عنوان blocker دقیق گزارش کن؛ constraint را دور نزن و schema را تغییر نده.

## بخش سوم — تست و تحویل

**AGENT VERIFICATION:** تست‌های خودکار را در محیط تست ایزوله اجرا کن. فرمان‌ها و خروجی واقعی را گزارش بده.

**USER ACCEPTANCE TEST:** فرمان‌های لازم برای بررسی مالک را جداگانه ارائه کن. مالک تست پذیرش را اجرا می‌کند؛ آن را انجام‌شده اعلام نکن.

فایل‌های تحویلی:
- کد اصلاح‌شده
- تست‌های خودکار
- گزارش `database/reports/DB_ING_008_MARKET_FX_ATOMIC_INGESTION.md`
- اصلاح Master Packet
- `reply.md` با گزارش اجرای واقعی

در `reply.md` برای هر Task شناسه و وضعیت دقیق را بنویس. فایل‌های تغییرکرده، سناریوهای تست، فرمان‌ها و خروجی واقعی را ثبت کن.

**مهم:** این بار Task را با تحلیل مجدد، گزارش provenance یا فهرست کارهای آینده جایگزین نکن. کار اصلی، تغییر کد و اثبات رفتار fail-closed با تست است. اگر بخشی واقعاً به تغییر schema نیاز دارد، همان بخش را مستند کن و بقیه دامنه قابل‌اجرا را تکمیل کن.