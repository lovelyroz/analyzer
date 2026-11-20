# Task 035 — DB-ING-008
## Market/FX Atomic Ingestion and Conflict Protection

این Task اجرایی است. هدف اصلاح کدهای موجود است، نه تهیه گزارش یا تکرار ممیزی‌های قبلی.

### مراجع
- `database/DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md`
- `database/reports/DB_DES_005_INGESTION_ATOMICITY_CONTRACT.md`
- `src/ingestion/market/ingestion.py`
- `src/ingestion/service.py`
- `src/ingestion/common/identity.py`
- `src/ingestion/common/validation.py`

### بخش A — اصلاح Market ingestion
1. کل فایل باید پیش از هر canonical write اعتبارسنجی شود.
2. اگر حتی یک ردیف دارای خطای سخت باشد، کل فایل رد شود.
3. داده‌های معتبر همان فایل نباید در صورت وجود ردیف نامعتبر ذخیره شوند.
4. اگر کلید اقتصادی موجود است:
   - payload یکسان: duplicate بدون تغییر؛
   - payload متفاوت: conflict و رد کل batch؛
   - overwrite ممنوع.
5. فیلدهای خارج از قرارداد MarketDaily نباید ذخیره شوند.
6. مقدار Value باید مستقل از Volume × Close حفظ شود.

### بخش B — اصلاح FX ingestion
1. اعتبارسنجی کامل تمام DTOها پیش از ثبت انجام شود.
2. خطای یک نرخ موجب رد کل batch شود.
3. کلید اقتصادی Jalali مطابق قرارداد بررسی شود.
4. نرخ تکراری با payload یکسان بدون تغییر پذیرفته شود.
5. نرخ متعارض برای کلید موجود موجب رد کل batch شود.
6. overwrite ممنوع باشد.
7. تبدیل واحد در adapter انجام می‌شود؛ service نباید دوباره ×۱۰ اعمال کند.

### بخش C — Atomicity و IngestionRun
1. هیچ commit داخل حلقهٔ رکوردها مجاز نیست.
2. canonical writes و وضعیت COMPLETED باید در یک transaction باشند.
3. در صورت شکست، تمام canonical writes همان batch rollback شوند.
4. وضعیت FAILED باید با transaction مستقل ثبت شود.
5. تعداد inserted، unchanged، rejected و failed باید معنای دقیق و سازگار داشته باشند.
6. exception خام، اطلاعات حساس یا مسیر خصوصی نباید در error_log ذخیره شود.
7. رفتار session پس از rollback و خطای audit نیز باید مشخص و تست شود.

### بخش D — محدودیت‌های قطعی
- هیچ ORM، schema، migration یا دیتابیس واقعی تغییر نکند.
- Migration 9 و cleanup مربوط به آن دست‌نخورده بمانند.
- هیچ عملیات ingestion روی دیتابیس مالک انجام نشود.
- CODAL خارج از دامنه این Task است.
- ShareCountHistory و CorporateAction خارج از دامنه‌اند.
- کلید یکتای فیزیکی Jalali بدون migration حل‌شده فرض نشود.
- در صورت نبود constraint فیزیکی، محدودیت concurrency و race condition صریحاً مستند شود؛ ادعای تضمین uniqueness هم‌زمان مجاز نیست.
- EXCHANGE_CENTER را در persistence معتبر فرض نکن؛ سازگاری CheckConstraint و مدل موجود را بررسی کن. اگر بدون schema change قابل حل نیست، آن را به‌عنوان مانع مشخص گزارش کن و workaround نساز.
- تصمیم‌های قطعی مالک دوباره سؤال نشوند.

### AGENT VERIFICATION
ایجنت باید تست‌های خودکار مستقل برای Market و FX بنویسد و اجرا کند. حداقل سناریوها:
- batch کاملاً معتبر
- خطای یک ردیف در میان چند ردیف معتبر
- duplicate یکسان
- duplicate متعارض
- کلید موجود با payload یکسان
- کلید موجود با payload متفاوت
- failure پس از حداقل یک write موقت و اثبات rollback
- عدم باقی‌ماندن canonical write پس از FAILED
- صحت counts و وضعیت IngestionRun
- خطای commit و rollback
- دو Session مستقل برای بررسی محدودیت concurrency

فرمان و خروجی واقعی تست‌ها گزارش شود.

### USER ACCEPTANCE TEST
پس از پیاده‌سازی، فرمان‌های دقیق تست پذیرش برای کاربر ارائه شود. تست‌ها باید روی دیتابیس آزمایشی و fixtureهای کنترل‌شده اجرا شوند؛ نه دیتابیس واقعی.

کاربر تست پذیرش را اجرا می‌کند. ایجنت نباید آن را اجراشده یا تأییدشده اعلام کند.

### مستندات و تحویل
- Master Packet را با نتیجهٔ Task 034 و پذیرش موفق کاربر به‌روزرسانی کن.
- Task 035 را با وضعیت واقعی ثبت کن.
- `reply.md` را با شواهد، فایل‌های تغییرکرده، تست‌ها و محدودیت‌های باقی‌مانده به‌روزرسانی کن.
- هیچ Task دیگری را صرفاً به‌دلیل تکمیل گزارش DONE نکن.

### معیار تکمیل
هر دو سرویس Market و FX باید در برابر خطای batch، duplicate و conflict رفتار امن و تست‌شده داشته باشند؛ هیچ partial canonical write یا overwrite غیرمجاز باقی نماند. محدودیت‌های نیازمند Migration جداگانه نیز دقیقاً ثبت شوند.