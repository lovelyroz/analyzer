# Package 5 — Regression, Audit & Stage 7 Closure

## بخش اول — دستورالعمل Agent

### 1. نوع و محدودهٔ کار

**Task Type:** REPORT-ONLY + TEST AUDIT + FINAL EXIT-CRITERIA REVIEW

این مأموریت صرفاً شامل ممیزی کد، مستندات، تست‌ها و معیارهای خروج Stage 7 است.

- هیچ کدی را تغییر نده.
- هیچ تستی را تغییر نده.
- هیچ مستندی را تغییر نده.
- هیچ تست یا فرمانی را اجرا نکن.
- هیچ فایل یا گزارشی را در GitHub یا مخزن ثبت نکن.
- گزارش نهایی را مستقیماً به کاربر تحویل بده.

### 2. محل اجرا و فایل‌های ورودی — الزام قطعی

کار را فقط روی نسخهٔ محلی پروژه با نام پوشهٔ `analyzer` انجام بده.

**GitHub منبع اجرای این مأموریت نیست.** فرض نکن به مخزن GitHub دسترسی داری و برای خواندن یا تغییر فایل‌ها از GitHub استفاده نکن.

تمام فایل‌های فهرست‌شده در بخش «فهرست فایل‌های ورودی» باید پیش از شروع کار، واقعاً داخل ZIP یا پوشهٔ کاری محلی در اختیار تو باشند.

پیش از شروع:

1. وجود تک‌تک فایل‌های فهرست‌شده را بررسی کن.
2. مسیر و وضعیت وجود فایل‌ها را گزارش کن.
3. اگر حتی یک فایل ضروری موجود نبود، کار وابسته به آن فایل را انجام نده و کمبود را دقیقاً اعلام کن.
4. اگر برای تکمیل مأموریت به فایلی خارج از فهرست نیاز داشتی، مسیر و دلیل ضرورت آن را اعلام کن و برای دریافت اجازه متوقف شو.
5. بدون اجازه، فایل دیگری را جست‌وجو یا بررسی نکن.

### 3. قواعد دسترسی و تغییر فایل‌ها

- تمام فایل‌های ورودی صرفاً **READ-ONLY** هستند.
- هیچ فایلی مجاز به تغییر نیست.
- `PROMPT.md` و `prompt.md` خارج از محدوده هستند و نباید بررسی شوند.
- هیچ Git commit، push، pull، branch یا remote operation انجام نده.
- تست‌ها را حذف، تضعیف، skip یا برای سبز شدن مصنوعی اصلاح نکن.
- وضعیت BLOCKED را با مستندسازی، توضیح یا تست غیرواقعی به DONE تبدیل نکن.
- یک مسیر E2E مصنوعی برای اثبات اتصال مراحل ایجاد یا فرض نکن.

### 4. فهرست فایل‌های ورودی

تمام فایل‌های زیر باید در بستهٔ محلی Agent موجود باشند.

**مستندات و تنظیمات**

- `WORKFLOW_RULES.md`
- `STAGE7_MASTER_WORKING_PACKET.md`
- `07_Stage7_Valuation.md`
- `05_Stage5_Forecast_Engine.md`
- `.github/workflows/tests.yml`
- `requirements.txt`

**کدهای مرتبط**

- `src/valuation/engine.py`
- `src/valuation/service.py`
- `src/valuation/schema.py`
- `src/valuation/models.py`
- `src/valuation/parameters.py`
- `src/forecast/service.py`
- `src/forecast/schema.py`
- `src/market/service.py`
- `src/ingestion/market/queries.py`
- `src/decision/service.py`

**تمام ۳۵ فایل تست**

1. `src/tests/test_codal_acquisition.py`
2. `src/tests/test_codal_digit_normalization.py`
3. `src/tests/test_codal_extraction.py`
4. `src/tests/test_codal_pdf_extraction.py`
5. `src/tests/test_ingestion_fx.py`
6. `src/tests/test_ingestion_ohlc.py`
7. `src/tests/test_jalali_contract.py`
8. `src/tests/test_market_history_query.py`
9. `src/tests/test_stage1_database_architecture.py`
10. `src/tests/test_stage1_database_integrity.py`
11. `src/tests/test_stage1_rules.py`
12. `src/tests/test_stage2_kpis.py`
13. `src/tests/test_stage3_scoring.py`
14. `src/tests/test_stage4_trend.py`
15. `src/tests/test_stage5_forecast.py`
16. `src/tests/test_stage6_artifact_boundary.py`
17. `src/tests/test_stage6_artifact_identity.py`
18. `src/tests/test_stage6_evaluation.py`
19. `src/tests/test_stage6_evaluation_foundation.py`
20. `src/tests/test_stage6_evaluation_metrics.py`
21. `src/tests/test_stage6_p25_adversarial.py`
22. `src/tests/test_stage6_p25_selection.py`
23. `src/tests/test_stage6_p38_closure.py`
24. `src/tests/test_stage6_p39_cutoff.py`
25. `src/tests/test_stage6_p40_duplicates.py`
26. `src/tests/test_stage6_p41_cutoff_identity.py`
27. `src/tests/test_stage6_production_pipeline.py`
28. `src/tests/test_stage6_reliability_governance.py`
29. `src/tests/test_stage6_scenario_isolation.py`
30. `src/tests/test_stage789_service_interface.py`
31. `src/tests/test_stage7_valuation.py`
32. `src/tests/test_stage8_market.py`
33. `src/tests/test_stage8_market_parameters.py`
34. `src/tests/test_stage8_market_service.py`
35. `src/tests/test_stage9_decision.py`

### 5. وظایف ممیزی

#### Task 019 — S7-TEST-003: شناسایی دو تست Skip شده

علت دقیق دو تست Skip شده در اجرای قبلی مجموعهٔ کامل تست‌ها را بررسی کن.

شواهد موردنیاز:

- محل تعریف هر Skip در کد تست.
- شرط یا دلیل ثبت‌شده برای Skip.
- اینکه Skip دائمی است یا وابسته به محیط، تنظیمات یا پیش‌شرط خاص.
- آیا Skip از نظر طراحی قابل قبول است یا پوشش تست ضروری را حذف کرده است؟

**نکته:** توضیح موجود در سورس تست را با علت واقعی Skip شدن در اجرای محلی یکی فرض نکن. علت runtime فقط با خروجی واقعی pytest و گزینهٔ `-rs` قابل تأیید است. اگر خروجی اجرای جدید در اختیار تو نیست، این محدودیت را صریحاً گزارش کن.

#### Task 021 — S7-TEST-005: ممیزی پوشش تست‌های OA1

پوشش واقعی تست‌ها را در برابر الزامات OA1 بررسی کن.

حداقل این موارد باید بررسی شوند:

1. Historical Forward P/E بر اساس داده‌های خام همان شرکت.
2. استفاده از مشاهدات مالی و بازار همراه با provenance معتبر.
3. انتخاب آخرین مجموعهٔ کامل و معتبر اطلاعات مالی.
4. انتخاب قیمت بازار بر اساس تاریخ جلالی و تولید هشدار تاریخ واقعی انتخاب‌شده.
5. رد کردن P/E از پیش محاسبه‌شده در صورت فقدان provenance معتبر.
6. مستقل بودن مسیر ارزش‌گذاری از Industry P/E.
7. کنترل سازگاری هویت Forecast با شرکت و دورهٔ ارزش‌گذاری.
8. محافظت در برابر Overflow و مقادیر عددی غیرمتناهی.

برای هر الزام مشخص کن:

- تست مرتبط کدام است؟
- تست چه رفتاری را واقعاً اثبات می‌کند؟
- چه چیزی را اثبات نمی‌کند؟
- آیا تست مثبت و منفی کافی وجود دارد؟
- آیا تست صرفاً interface-level است یا رفتار واقعی مسیر اجرایی را پوشش می‌دهد؟

وضعیت‌های قبلی را بدون شواهد جدید تغییر نده:

- Task 025 و 026 قبلاً DONE شده‌اند.
- Task 022، 023، 024 و 027 همچنان BLOCKED هستند، مگر اینکه شواهد واقعی و قابل بررسی خلاف آن را ثابت کند.

برای قراردادهای پیاده‌سازی‌نشده، تست صوری یا مصنوعی را به‌عنوان اثبات تکمیل معرفی نکن.

#### Task 037 — S7-PLAN-003: برنامهٔ اجرای تست نهایی

فرمان‌های دقیق لازم برای اجرای تست‌های هدفمند و سپس کل مجموعه را ارائه کن.

فرمان پیشنهادی تست‌های هدفمند:

```powershell
pytest src/tests/test_market_history_query.py src/tests/test_stage789_service_interface.py src/tests/test_stage7_valuation.py src/tests/test_stage8_market.py src/tests/test_stage9_decision.py -q -rs
```

فرمان مجموعهٔ کامل:

```powershell
pytest src/tests -q -rs
```

این فرمان‌ها را فقط پیشنهاد بده؛ اجرا نکن.

کاربر شخصاً تست‌ها را در محیط محلی خود اجرا می‌کند و خروجی واقعی را برای بررسی ارائه خواهد کرد.

#### Task 020 — S7-TEST-004: بررسی امکان E2E واقعی

مسیر واقعی اجرای برنامه را از شواهد موجود بررسی کن.

موارد لازم:

- آیا entrypoint واقعی برای اجرای زنجیرهٔ مراحل وجود دارد؟
- مالک Session و چرخهٔ عمر آن مشخص است؟
- اتصال واقعی Forecast، Fundamental، Market، Valuation و Decision اثبات شده است؟
- آیا تست E2E موجود واقعاً از مسیر تولید استفاده می‌کند یا نتایج مراحل قبلی را مستقیماً به‌صورت fixture/helper می‌سازد؟
- آیا می‌توان یک E2E واقعی و معتبر اجرا کرد؟

اگر مسیر تولید واقعی اثبات نشده است، Task 020 باید BLOCKED بماند.

وجود تستی که فقط interface سرویس‌ها را بررسی می‌کند، اثبات E2E واقعی نیست.

#### Task 034 — S7-T012: ممیزی معیارهای خروج Stage 7

تمام معیارهای خروج 040 تا 047 در بخش Exit Criteria فایل `STAGE7_MASTER_WORKING_PACKET.md` را جداگانه بررسی کن.

برای هر معیار ارائه بده:

- وضعیت: PASS / BLOCKED / OPEN
- شواهد دقیق از فایل، تابع، قرارداد یا تست
- شکاف باقی‌مانده
- Task مسئول رفع شکاف
- اینکه آیا شواهد واقعاً معیار را اثبات می‌کنند یا صرفاً ادعای انجام کار هستند

موارد زیر را با دقت ویژه بررسی کن:

- ادعای PIT بدون provenance و شواهد زمانی معتبر پذیرفته نیست.
- تاریخ مشاهده به‌تنهایی اثبات‌کنندهٔ زمان انتشار یا در دسترس بودن داده نیست.
- نبود vintage تاریخی نباید با پارامترهای فعلی جبران یا جعل شود.
- نبود منبع معتبر Historical P/E باید صریحاً ثبت شود.
- کامل بودن ورودی‌های مالی باید واقعاً اثبات شده باشد.
- اتصال E2E باید از مسیر واقعی تولید اثبات شود.
- تصمیم عدم ذخیره‌سازی خروجی‌های تحلیلی در DB همچنان باید رعایت شود.
- موارد Forecast Persistence و باقیماندهٔ OA1.7، به‌ویژه `053-10`، نباید نادیده گرفته شوند.
- متن قدیمی و متناقض OA1.7 در `07_Stage7_Valuation.md` باید در گزارش مشخص شود.

#### Task 039 — S7-PLAN-005: تعیین وضعیت نهایی Stage 7

پس از بررسی تمام شواهد، دقیقاً یکی از وضعیت‌های زیر را برای Stage 7 انتخاب کن:

**CLOSED**

فقط زمانی مجاز است که تمام معیارهای خروج حیاتی با شواهد واقعی برآورده شده باشند.

**OPEN — BLOCKED**

وقتی تکمیل Stage 7 به علت فقدان قرارداد، مسیر تولید، داده، provenance یا شواهد ضروری ممکن نیست.

**OPEN — NOT COMPLETE**

وقتی کارهای ضروری هنوز انجام نشده‌اند، اما مانع خارجی یا وابستگی حل‌نشده‌ای وجود ندارد.

در تعیین وضعیت نهایی، تمام این موارد را صریحاً تعیین تکلیف کن:

- Tasks 019، 020 و 021
- Tasks 022 تا 027
- Tasks 029 تا 034
- Tasks 035 تا 039
- Tasks 053 تا 057، به‌ویژه باقیماندهٔ OA1.7 یعنی `053-10`

تفاوت بین «پیاده‌سازی انجام شده»، «تست موفق»، «ممیزی انجام شده» و «معیار خروج اثبات شده» را حفظ کن.

### 6. قالب گزارش نهایی

گزارش را با ساختار زیر تحویل بده:

1. **Input File Verification** — فهرست فایل‌های موجود و مفقود در بستهٔ محلی.
2. **Task 019 — Skip Audit** — علت و شواهد دو Skip.
3. **Task 021 — OA1 Test Coverage Matrix** — ماتریس پوشش الزامات و شکاف‌ها.
4. **Task 037 — Final Test Commands** — فرمان‌های هدفمند و کامل.
5. **Task 020 — E2E Audit** — نتیجهٔ بررسی مسیر واقعی تولید.
6. **Task 034 — Exit Criteria Review** — وضعیت تک‌تک معیارهای 040 تا 047.
7. **Task 039 — Final Stage 7 Disposition** — یکی از سه وضعیت مجاز همراه با دلیل.
8. **Task Status Summary** — وضعیت نهایی پیشنهادی تمام Taskهای مرتبط.
9. **Remaining Blockers** — فهرست دقیق موانع، وابستگی‌ها و مسئول هرکدام.
10. **User Execution Handoff** — فرمان‌هایی که کاربر باید اجرا کند و خروجی‌هایی که باید تحویل دهد.

گزارش باید مبتنی بر شواهد باشد. هرجا شواهد کافی نیست، صریحاً بنویس «اثبات نشده» یا «نیازمند خروجی اجرای کاربر».

**هیچ Task یا معیار خروجی را صرفاً برای بستن Stage 7 به DONE یا PASS تغییر نده.**

---

## بخش دوم — دستور کار کاربر

### Task List

- [ ] بررسی وجود تمام فایل‌های ورودی در بستهٔ محلی Agent.
- [ ] ممیزی دو تست Skip شده و علت آن‌ها.
- [ ] بررسی پوشش تست‌های OA1 و شکاف‌های باقی‌مانده.
- [ ] بررسی مسیر واقعی E2E و چرخهٔ عمر Session.
- [ ] بررسی جداگانهٔ معیارهای خروج 040 تا 047.
- [ ] تعیین وضعیت نهایی Stage 7 و تمام Taskهای باقی‌مانده.
- [ ] ارائهٔ فرمان‌های دقیق تست هدفمند و مجموعهٔ کامل.

### Expected Result

یک گزارش ممیزی نهایی مبتنی بر شواهد واقعی، شامل وضعیت هر Task، علت موانع باقی‌مانده، وضعیت معیارهای خروج و فرمان‌های اجرای تست توسط کاربر.

**این مأموریت هیچ تغییر کد یا مستندی ندارد و هیچ تستی توسط Agent اجرا نمی‌شود.**