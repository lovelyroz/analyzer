## جمع‌بندی P53

**PIT کامل اثبات نشده است.** داده‌های Stage 5 و ارجاع‌های زمانیِ اعلام‌شده تا حدی قابل کنترل‌اند، اما برای قیمت بازار، benchmarkها، همهٔ ورودی‌های EPS و پارامترهای تاریخی شواهد کافی وجود ندارد.

### اصلاح انجام‌شده

در [engine.py](D:/winprojects/analyzer/src/valuation/engine.py:115)، موتور Stage 7 اکنون ارجاع‌های پذیرفته‌شده‌ای را که Stage 5 در `forecast_result.assumptions["input_refs"]` قرار می‌دهد، خودکار بررسی می‌کند. ارجاع‌های بدون `available_at` یا بعد از cutoff رد می‌شوند؛ ارجاع دقیقاً روی cutoff پذیرفته می‌شود. این ارجاع‌ها حتی در صورت ارسال فهرست صریح خالی نیز بررسی می‌شوند.

چهار تست به [test_stage7_valuation.py](D:/winprojects/analyzer/src/tests/test_stage7_valuation.py:1364) اضافه شد:

- `test_p53_embedded_forecast_input_ref_at_cutoff_is_enforced_and_accepted`
- `test_p53_embedded_forecast_input_ref_after_cutoff_is_rejected`
- `test_p53_embedded_forecast_input_ref_without_availability_is_rejected`
- `test_p53_explicit_empty_refs_do_not_bypass_embedded_forecast_provenance`

آزمون‌ها اجرا نشدند.

### شواهد زمانی و محدودیت‌ها

| ورودی | تاریخ مشاهده یا گزارش | شواهد دسترس‌پذیری و اعمال cutoff | محدودیت باقی‌مانده |
|---|---|---|---|
| قیمت بازار | `MarketDaily.jalali_year/month/day`؛ انتخاب آخرین قیمت در یا پیش از تاریخ جلالی درخواستی | `select_market_price_as_of` تاریخ جلالی را مقایسه می‌کند و قیمت، منبع و شناسهٔ رکورد را در metadata نگه می‌دارد. | مدل قیمت بازار `available_at` ندارد؛ تاریخ معامله ثابت نمی‌کند قیمت در همان زمان برای سیستم یا بازار در دسترس بوده است. تاریخ انتخاب‌شده هم به فیلدهای `valuation_date` و `market_price_date` منتقل نمی‌شود؛ در metadata باقی می‌ماند. |
| facts صورت‌های مالی | `FinancialPeriod.end_date` از نوع `Date` | `src/forecast/queries.py` نسخه‌هایی را انتخاب می‌کند که `ReportVersion.publication_datetime <= cutoff` باشد و ارجاع publication را برای Stage 5 فراهم می‌کند. | `publication_datetime` هنگام ingestion به‌عنوان ورودی دریافت می‌شود؛ کد بررسی نمی‌کند که آن زمان از منبع مستقل و معتبر تأیید شده باشد. پایان دوره، زمان انتشار نیست. |
| Forecast EPS | `SingleForecastChain.eps` در `CompanyForecastResult`؛ همراه `forecast_timestamp`، `data_cutoff_datetime` و `model_version` | Stage 5 ارجاع‌های پذیرفته‌شده را در `assumptions["input_refs"]` می‌گذارد. اصلاح P53 این شواهد را به اعتبارسنجی Stage 7 وصل می‌کند. | فهرست ارجاع‌ها فقط آنچه اعلام شده را پوشش می‌دهد. نبود ارجاع، ورودی‌های اعلام‌نشده را اثباتاً تاریخی نمی‌کند؛ provenance کامل EPS تضمین نشده است. |
| benchmark تاریخی و صنعتی | ورودی‌های عددی `historical_pe_values`، `industry_forward_pe_values` و `industry_ttm_pe_values` | در موتور Stage 7 به median تبدیل می‌شوند. | این ورودی‌ها تاریخ، منبع، تاریخ دسترس‌پذیری یا provenance به‌ازای هر observation ندارند؛ cutoff روی آن‌ها اعمال نمی‌شود. |
| cutoff و تاریخ ارزش‌گذاری | `data_cutoff_datetime` اختیاری است؛ در نبود آن از cutoff Forecast استفاده می‌شود. `valuation_date` اختیاری است. | cutoff برای ارجاع‌های Forecast مقایسه می‌شود. | ترتیب cutoff، تاریخ ارزش‌گذاری و تاریخ قیمت در موتور کنترل نمی‌شود. انتخاب قیمت به تاریخ جلالی است و آن را بدون تبدیلِ اثبات‌شده نمی‌توان با cutoff از نوع `datetime` مقایسه کرد. |
| نسخه و پارامترهای مدل | `model_version` و snapshot پارامترها ثبت می‌شوند. | انتخاب تاریخ‌دار با `parameter_as_of` و registry صریح پشتیبانی می‌شود. | registry پیش‌فرض فقط مجموعهٔ genesis بدون `effective_from` دارد. cutoff خودکار مبنای انتخاب پارامتر نیست (`data_cutoff_used_for_parameter_selection=False`)؛ تاریخچهٔ پارامترهای معتبر برای بازآزمایی کامل در دسترس نیست. |

### مسیر بررسی‌شده

مسیر قابل‌ترکیب در کد از سرویس Forecast و داده‌های مالیِ فیلترشده بر اساس publication شروع می‌شود؛ `calculate_valuation_as_of_jalali` قیمت را با تاریخ جلالی انتخاب می‌کند و به `ValuationEngine` می‌دهد؛ `calculate_decision_as_of_jalali` نتیجهٔ Stage 7 را به `DecisionEngine` می‌رساند. بااین‌حال، در کد محلی فراخوانِ برنامه‌ای برای orchestrator مرحلهٔ تصمیم پیدا نشد؛ استفادهٔ قابل‌مشاهده از آن در تست‌هاست. بنابراین وجود این توابع به‌تنهایی مسیر production یا PIT تاریخیِ سرتاسری را اثبات نمی‌کند.

**نتیجه:** enforcement برای ارجاع‌های Forecast که واقعاً همراه نتیجه اعلام شده‌اند تقویت شد؛ کنترل cutoff قیمت فقط بر اساس تاریخ مشاهده انجام می‌شود. صحت PIT کل ارزش‌گذاری و بازآزمایی تاریخی همچنان **اثبات‌نشده** است.

### فایل‌ها، آزمون‌ها و گام بعدی

فایل‌های تغییرکرده:

- `src/valuation/engine.py` — اتصال provenance موجود Forecast به اعتبارسنجی Stage 7.
- `src/tests/test_stage7_valuation.py` — چهار تست متمرکز برای مرز cutoff، دادهٔ آینده، availability نامعلوم، و جلوگیری از دورزدن بررسی با فهرست صریح خالی.

ترتیب پیشنهادی اجرای تست‌ها:

```bash
python -m pytest src/tests/test_stage7_valuation.py -q -k "p53_embedded_forecast_input_ref or p53_explicit_empty_refs"
python -m pytest src/tests/test_stage7_valuation.py -q
```

این فایل‌ها و بخش‌های مرتبط از کد و تست‌های Forecast، market ingestion، مدل‌های Report/Period/Market، پارامترهای Stage 7 و سرویس تصمیم بررسی شدند. تست یا CI اجرا نکردم و فایل گزارش یا مشخصات قفل‌شده را تغییر ندادم. **گام بعدی برنامه** رفع محدودیت D7 است: منبع معتبر `available_at` برای قیمت بازار، provenance تاریخ‌دار benchmarkها و نسخه‌های مؤثر تاریخی پارامترها لازم است. Stage 7 همچنان **OPEN** است.