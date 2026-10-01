Stage 5 — گزارش نهایی: DATA MODEL / PIT / VERSIONING
۱. فایل‌های تغییر یافته
فایل	تغییرات
src/forecast/schema.py	+۲۶۰ خط
src/forecast/engine.py	+۱۰۹ خط
src/tests/test_stage5_forecast.py	+۳۸۱ خط

هیچ فایل دیگری (مستندات، status، models، migrations، Stage 4/6/7) دستکاری نشد.

۲. تغییرات دقیق

schema.py — مدل داده و versioning:

ForecastRecord: دیتاکلاس immutable (frozen=True) با تمام فیلدهای قرارداد §۲۸: forecast_id، forecast_version، company_id، forecast_period_id، industry_code، forecast_horizon، scenario، forecast_timestamp، data_cutoff_datetime، model_version، forecast_method، data_quality، baseline_method، شش متریک (revenue → roe) و assumptions + input_refs.
SingleForecastChain: فیلدهای scenario و forecast_horizon اضافه شد. چهار فیلد اول positional حفظ شدند (قرارداد Stage 7).
CompanyForecastResult.to_record(scenario, forecast_id) / .records(): فریز کردن زنجیره به رکورد قابل ذخیره.
ForecastInputRef (frozen): مسیر auditability §۲۹ — fact_key، report_version_id، available_at، source.
ForecastVersionStore: رجیستری append-only.
normalize_datetime()، filter_pit_inputs()، revision_trend().
is_missing(metric): None را None می‌گذارد، هرگز ۰ نمی‌کند (§۲۷).

engine.py:

_raw_input_refs(): نرمال‌سازی اعلامیه provenance از نوع ForecastInputRef یا mapping.
_pit_safe(): جدا کردن ورودی‌های منتشرشده بعد از cutoff.
cutoff همیشه به UTC نرمال می‌شود.
ValueError اگر calculation_timestamp < data_cutoff_datetime.
سناریوها در همه زنجیره‌ها (شامل Bank/Holding) برچسب‌گذاری شدند.
ثابت شد: engine قبلاً datetime.now() را مستقیماً تخصیص می‌داد و calculation_timestamp کانتکست را نادیده می‌گرفت.
۳. رفتار PIT
ورودی با available_at > cutoff حذف می‌شود، هرگز خاموش استفاده نمی‌شود.
رد آن در assumptions["pit_violation"] ثبت می‌شود (fact_key، available_at، cutoff، action).
ورودی‌های ردشده در رکورد حفظ می‌شوند تا رکورد بتواند شهادت دهد یک ورودی دیررس دیده و رد شده است.
read_at_cutoff(): جدیدترین رکوردِ قابل دسترس در آن لحظه؛ رکورد آلوده به داده‌های آینده قابل دسترس نیست.
pit_violations(): تشخیص سراسری look-ahead.
ورودی بدون تاریخ انتشار هرگز رد نمی‌شود (Stage 5 مالک لایه گزارش نیست).
timezone-aware و naive هر دو به UTC تبدیل می‌شوند.
۴. رفتار Versioning
save(): فقط append، هیچ مسیر UPDATE وجود ندارد.
تغییر → نسخه بعدی؛ نسخه قدیمی کامل حفظ می‌شود.
ذخیره مجدد رکورد یکسان → no-op (idempotent)، نسخه جدید ساخته نمی‌شود.
ForecastVersionExistsError برای نسخه caller-supplied متفاوت.
revision_trend(): UPWARD / DOWNWARD / MIXED / None (Earnings Revision Trend §۲۴).
هر سناریو (BEAR/BASE/BULL) یک سری جداگانه است.
۵. تست‌ها
pytest src/tests/test_stage5_forecast.py -v
31 passed in 0.10s

۸ تست قبلی (همه حفظ شدند) + ۲۳ تست جدید: فیلدهای قرارداد رکورد، فریز سه سناریو، horizon/timestamp، Missing != 0، UTC naive cutoff، رد calculation قبل از cutoff، auditability input_refs (هم نوع object هم mapping)، ورودی بدون تاریخ، input_refs نامعتبر، append/عدم overwrite، حفظ نسخه قدیمی، idempotency، تعارض نسخه، revision trend، جدایی سناریوها، filter_pit، flagging ورودی آینده، read_at_cutoff، تشخیص look-ahead سراسری، نرمال‌سازی timezone.

بررسی مرزهای Downstream (به دلیل تغییر schema): Stage 6 (۱۱) + Stage 7 (۱۱) + Stage 4 (۵۳) = ۱۲۴ passed.

۶. ناکامی‌های باقی‌مانده

هیچ. ۳۱/۳۱ تست Stage 5 pass، ۱۲۴/۱۲۴ تست مرزی pass.

باقی‌مانده‌های شناخته‌شده (از محدوده این کار خارج هستند): هنوز ForecastVersionStore در یک مدل دیتابیس/مهاجرت ثبت نشده (این درخواست صراحتاً فایل‌های models/migrations را از کار خارج می‌کرد)، و ForecastEngine هنوز توسط کد تولیدی فراخوانی نمی‌شود — مسیر Stage 4 → Stage 5 هنوز ساخته نشده است.

۷.

Stage 5 is NOT declared frozen.