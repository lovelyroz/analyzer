Stage 5 — گزارش Preflight / Discovery

وضعیت: READ-ONLY. هیچ فایلی تغییر نکرد، هیچ commit‌ای ساخته نشد، فقط ۸ تست Stage 5 اجرا شد (همه PASS).

۱. خلاصه پیاده‌سازی فعلی

Stage 5 یک محاسبه‌گر خالص درون‌حافظه‌ای (in-memory) است که فقط دیکشنری‌های از پیش آماده‌شده را می‌پذیرد. سه ماژول: schema.py (Dataclassها + ثابت‌های صنعت)، drivers.py (زنجیره‌های محاسباتی خالص)، engine.py (ارکستراسیون Bear/Base/Bull). تمام کد از نظر منطقی موجود و ازstage_4ایزوله است، اما هیچ مسیر دادهای واقعی به آن وجود ندارد — صرفاً با تست‌ها فراخوانی می‌شود.

۲. آنچه واقعاً پیاده‌سازی شده
محدوده	وضعیت
Schema خروجی (۶ فیلد + method/quality/assumptions)	COMPLIANT
زنجیره غیرمالی Revenue→Margin→OpProfit→NetProfit→EPS→ROE	COMPLIANT
سلسله‌مراتب سود خالص: ۱ Component-Based → ۲ Net/Op Conversion → ۳ Margin	COMPLIANT
Bank Core (NII→NetProfit→EPS→ROE)	COMPLIANT
Holding Core (NAV→NAV Growth→NetProfit→EPS→ROE) بدون P/NAV	COMPLIANT
Low Base control (توقف trend_adj)	COMPLIANT
الگوی Bear ≤ Base ≤ Bull	COMPLIANT (رشد نامتقارن در غیرمالی، متقارن در بانک/هلدینگ)
Model parameters قابل تنظیم به‌جای هاردکد	COMPLIANT
جداسازی Stage 6 (فقط ذخیره cutoff/version، نه reliability)	COMPLIANT
Margins به‌صورت نسبت اعشاری، مستقل از revenue	COMPLIANT
کاهش سطح بازگشت به INSUFFICIENT_DATA	COMPLIANT
۳. آنچه ناقص است
محدوده	وضعیت	فاصله (Gap)
Forecast Versioning	REAL GAP	هیچ forecast table، model یا repository وجود ندارد. CompanyForecastResult یک dataclass درون‌حافظه‌ای است؛ چیزی برای overwrite نشدن آن وجود ندارد. Earnings Revision Trend غیرممکن است.
PIT / data_cutoff_datetime	REAL GAP	فیلد وجود دارد ولی هیچ فیلتری بر اساس تاریخ انتشار Report انجام نمی‌شود. data_cutoff_datetime فقط ذخیره می‌شود؛ look-ahead bias به‌طور فعال مسدود نمی‌شود.
بهینه‌سازی EPS / Share Count	REAL GAP	ShareCountHistory و CorporateAction جداول وجود دارند ولی هرگز کوئری نمی‌شوند. هیچ تابع سازنده‌ای برای weighted average shares وجود ندارد. کلید forecast_weighted_average_shares هرگز در کد تولید پر نمی‌شود.
بهینه‌سازی Stage 4	REAL GAP	TrendResult → کلیدهای ورودی Stage 5 برابر نیستند. هیچ مبدلی وجود ندارد: seasonality_valid، seasonal_baseline_revenue، recent_run_rate_revenue، seasonal_naive_revenue، baseline_revenue_growth، forecast_operating_margin همگی باید دستی پر شوند.
بهینه‌سازی Drivers	PARTIAL	driver_revenue_adjustment یک عدد خام واحد است. سناریوهای Volume/Price/Margin/FinancialCost §22 پیاده‌سازی نشده‌اند.
بهینه‌سازی Bank	PARTIAL	NPL به‌عنوان Context در نظر گرفته نمی‌شود — اصلاً به آن ارجاع داده نمی‌شود. NIM با وجود نام‌گذاری در مشخصات، یک ورودی نیست.
FX separation	REAL GAP	operational_fx فقط در assumptions لوگ می‌شود. هیچ مسیر محاسباتی، هیچ اعتبارسنجی، هیچ فیلتری روی استفاده از FX در پیش‌بینی وجود ندارد. هیچ اثری از operational FX در هیچ جای زنجیره وجود ندارد.
بهینه‌سازی Stage 6	PARTIAL	benchmark (Seasonal Naive) اضافه شد که خوب است، ولی Stage 6 در عوض data_cutoff_datetime را توقع دارد — ناسازگاری جزئی در نام‌گذاری.
بهینه‌سازی Stage 7	COMPLIANT	موتور ارزش‌گذاری scenario_forecasts + data_cutoff_datetime را به‌درستی می‌خواند.
Missing ≠ 0	COMPLIANT	None در طول زنجیره حفظ می‌شود، هرگز به ۰ تبدیل نمی‌شود.
سناریوهای ± دلخواه (§20/§22)	REAL GAP	فاصله‌ها هاردکد شده‌اند: ±۵٪ رشد، ±۲٪ حاشیه، ±۱٪ حاشیه سود خالص. برخلاف §۲۰ که می‌گوید "نباید با درصدهای کاملاً دلخواه مانند ±20% تعریف شوند". پارامتری شده‌اند ولی پیش‌فرض‌ها دلخواه و بدون ریشه در dispersion هستند.
بهینه‌سازی Sign Change	REAL GAP	§۱۹ می‌گوید باید مورد احترام قرار گیرد. پیاده‌سازی فقط آن را در assumptions لوگ می‌کند — هیچ کنترلی روی EXTRAPOLATION مکانیکی اعمال نمی‌کند.
زنجیره سلسله‌مراتب پایه (§17)	PARTIAL	الگوی ۳ سطحی وجود ندارد؛ فقط یک پایه انتخاب می‌شود.
افق‌های 1M/3M/6M/12M	PARTIAL	اعتبارسنجی می‌شود ولی افق به منطقی که محاسبه می‌شود، متصل نیست — 1M همان 12M را برمی‌گرداند.
هیچ Double-Counting	COMPLIANT	TTM/Fundamental Score به‌عنوان فاکتور مستقل وارد نمی‌شوند.
۴. آنچه نادرست است
generate_forecast در صورت فقدان baseline، یک chain خالی خالی (empty empty chain) بازمی‌گرداند. بهتر است یک chain واقعی با revenue خالی تولید شود. مشکلی حادی نیست.
ارزش net_margin هنگام موجود بودن conversion خاموش می‌شود (engine.py:117-119) — درخواست صریح به‌جای حالت پیش‌فرض پارامتر کلمه‌کلیدی. کار می‌کند ولی شکننده است.
build_general_chain compatibility wrapper —(wrapper سازگاری) فیلدها را به‌صورت positional در زنجیره قرار می‌دهد و سپس build_non_financial_chain را فراخوانی می‌کند. فیلد چهارم positional net_profit است، نه eps. آسیب‌زا نیست ولی یک تله برای تماس‌های جدید است.
data_quality در مسیر بانک/هلدینگ تنها در صورت quality تعریف‌شده در حوزه غیرمالی بازمی‌گردد — ارزش‌گذاری بانک/هلدینگ هرگز کیفیت پایه را گزارش نمی‌کند.
۵. BLOCKERS

B1 — ForecastEngine هرگز در کد تولید فراخوانی نمی‌شود. بررسی شد: فقط test_stage5_forecast.py و خود __init__.py به آن ارجاع می‌دهند. بدون مبدل Stage 4→Stage 5 و بدون persistence، Stage 5 داده‌ای تولید نمی‌کند. Stage 6/7 به آن تکیه می‌کنند. این همان الگوی Stage 2 است که قبلاً پیدا کردیم (موتور متصل نشده).

B2 — forecast versioning اصلاً وجود ندارد. §24 یک قانون مسدودکننده است و هیچ جدولی برای آن وجود ندارد.

B3 — PIT enforcement وجود ندارد. §25 یک قانون مسدودکننده است و فقط یک timestamp است.

۶. NON-BLOCKERS
شاخص FX در حال حاضر بدون اثر است (هیچ محاسبه‌ای از آن استفاده نمی‌کند) — یک توضیح بصری بدون پیامد. اگر بعداً محاسبات FX اضافه شوند، حیاتی می‌شود.
فاصله‌های سناریو پیش‌فرض دلخواه هستند (§20) — بهتر است از dispersion Hist استفاده شود، ولی پارامتری شده‌اند.
کنترل Sign Change فقط لاگ می‌شود، جلوگیری نمی‌کند (§۱۹).
افق در محاسبه اعمال نمی‌شود.
NPL به‌عنوان ورودی بانکی لحاظ نمی‌شود (§11 می‌گوید context باقی می‌ماند — مفقود بودن آن ناسازگار نیست، ولی فیلد context در دسترس نیست).
هیچ تستی برای PIT cutoff، version preservation، share-count change، operational FX separation، Insufficient Seasonality، Holding/Bank ordering، یا revision trend وجود ندارد.
مشخصات می‌گوید "Stages 6-9 هنوز طراحی نشده‌اند" — نادرست؛ Stage 6/7/9 پیاده‌سازی شده‌اند.
۷. فایل‌هایی که نیاز به تغییر دارند
فایل	دلیل
src/models/ (فایل جدید forecast.py)	مدل‌های ForecastVersion / ForecastScenario
src/migrations/runner.py	ثبت مدل‌های جدید
src/forecast/repo.py (جدید)	persistence با PIT query + never-overwrite
src/forecast/builder.py (جدید)	ShareCountHistory+CorporateAction → weighted avg shares
src/forecast/adapter.py (جدید)	TrendResult → کلیدهای financial_context
src/forecast/engine.py	enforcement علامت تغییر، اعمال افق، کیفیت بانک/هلدینگ
src/tests/test_stage5_forecast.py	پوشش PIT، versioning، share-count، FX، sign-change
۸. ترتیب پیشنهادی پیاده‌سازی
مبدل Stage 4→Stage 5 (B1 — بدون آن هیچ چیزی کار نمی‌کند)
سازنده weighted-average-shares از ShareCountHistory/CorporateAction
مدل + repo پیش‌بینی با never-overwrite (B2)
اعمال‌سازی PIT query بر اساس publication_date (B3)
کنترل‌های Sign Change + اعمال افق
مسیر سیگنال FX + گزینه NPL context برای بانک
فاصله‌های سناریو مبتنی بر dispersion
تست‌ها برای هر کدام از موارد فوق
۹. تست‌های Stage 5 و پوشش واقعی

تعداد: ۸ تست، همه PASS (در ۰.۱۸ ثانیه). پوشش: زنجیره عمومی، baseline فصلی، Low Base، اولویت component-based، بازگشت به insufficient data، بانک، هلدینگ، horizon/industry نامعتبر.

شبیه‌سازی مشخصات §32 شانزده‌گانه: تست‌ها فقط ۳ تا را پوشش می‌دهند: فصل‌مندی/Low Base (#2/#11 جزئی)، بانک (#15)، هلدینگ (#16).

پوشش داده نشده — ۱۳ مورد از ۱۶: #1 رشد عادی (جزئی)، #3 Loss→Profit، #4 Profit→Loss، #5 رشد درآمد + کاهش حاشیه، #6 تغییر تعداد سهام، #7/#8 فاندامنتال در مقابل trend، #9 Missing Data (جزئی)، #10 Driver مفقود، #12 ترتیب Bear/Base/Bull، #13 Versioning پیش‌بینی، #14 PIT cutoff. وさらに: FX operational separation نیز وجود ندارد.

۱۰. طرح پیاده‌سازی (۱۰ خط)
1. TrendResult → مبدل financial_context: seasonal.baseline → seasonal_baseline_revenue،
   coverage/seasonality → seasonality_valid، momentum آخرین → recent_run_rate_revenue.
2. راه‌اندازی WeightedShareBuilder: آخرین ShareCountHistory تا cutoff + تناسب
   CorporateAction برای split‌های قبل از cutoff، نگه‌داشتن None در صورت عدم قطعیت.
3. ایجاد مدل‌های ForecastVersion/ForecastScenario (insert-only، بدون UPDATE path).
4. repo.save_forecast() که در صورت وجود (company, period, horizon, scenario) خطا می‌دهد
   به‌جای overwrite؛ لیست نسخه‌ها → Earnings Revision Trend.
5. repo.read_at_cutoff(cutoff): فیلتر ReportVersion publication_date <= cutoff،
   پرتاب کلیدها اگر گزارش‌های بعدی تنها منبع باشند.
6. engine: اگر sign_change در (LOSS_TO_PROFIT|PROFIT_TO_LOSS|SIGN_CHANGE) باشد،
   رشد baseline را به zero/درصد متوسط تاریخچه تبدیل کن، از extrapolation جلوگیری کن.
7. engine: ضرایب افق (1M/3M/6M/12M) به‌عنوان پارامتر مدل، اعمال روی رشد.
8. engine: گزینه operational_fx_rate به مسیر حاشیه درآمد FX-دار متصل شود،
   خطا روی جایگزینی free-market بدون پرچم estimated.
9. scenarios: spread پیش‌فرض بر اساس std-dev تاریخچه محاسبه شود (به‌جای 0.05).
10. تست‌ها: PIT cutoff، version preservation، تغییر تعداد سهام، تغییر علامت،
    FX operational، ترتیب بانک/هلدینگ، فصل‌مندی ناکافی.

Stage 5 فریز نشده. این یک کشف فقط خواندنی بود — هیچ فایلی تغییر نکرد، commit‌ای ساخته نشد، و خارج از لیست مجاز چیزی بررسی نشد.

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