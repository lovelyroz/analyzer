## گزارش اجرای Stage 7 — Package 1

**029 · S7-T007 — وضعیت: PARTIAL**

- در [پارامترها](</D:/winprojects/analyzer/src/valuation/parameters.py>) registry کد‌محور، انتخاب as-of فقط از نسخه‌های تاریخ‌دار و fail-closed در نبود نسخه وجود دارد. Genesis بدون تاریخ است؛ مسیر legacy آن را بدون ادعای PIT مصرف می‌کند.
- شواهد برای تاریخ‌های `effective_from`، vintageهای تاریخی واقعی یا اعتبار مالی Genesis در فایل‌های بررسی‌شده وجود ندارد. الزام نسخه‌بندی تغییرناپذیر مستند است، اما مکانیزم بررسی منشأ تاریخ یا الزام نسخهٔ تازه پس از هر تغییر مادی را اجرا نمی‌کند.
- در Master Packet ثبت شد که Genesis برای استفادهٔ مالی تأیید نشده و فقط برای اجرای فنی/آزمون provisional است؛ ادعای اعتبار تاریخی و full PIT مجاز نیست.

**030 · S7-T008 — وضعیت: PARTIAL**

- قراردادهای D1–D5، محدودبودن D6 در V1 به EPS و TARGET_PE، واژگان D8 و الزامات OA1.5/OA1.6 حفظ شدند. D6 حل‌نشده و Driverها و فرمول‌های sector-specific deferred باقی ماندند.
- در `engine.py` هشدارها دیده می‌شوند، اما ورودی benchmarkها float ساده و قیمت/تاریخ caller-supplied است؛ این مرز به‌تنهایی اجرای انتخاب مجموعهٔ کامل و معتبر OA1.5 یا انتخاب قیمت واجدشرایط و گزارش تاریخ واقعی OA1.6 را اثبات نمی‌کند.
- Master Packet اصلاح شد تا الزامات OA1.5/OA1.6 به‌اشتباه پیاده‌سازی‌شده تلقی نشوند.

**048 · S7-T020 — وضعیت: DONE، فقط برای ثبت تصمیم**

- تصمیم رسمی ثبت شد: مقادیر فعلی Genesis به‌عنوان financially calibrated یا validated **تأیید نمی‌شوند**. وجود مقدار در کد شاهد اعتبار مالی نیست؛ شواهد لازم برای calibration یا backtest معتبر در فایل‌های بررسی‌شده نبود.
- مقادیر فقط provisional/unapproved و برای اجرای فنی و آزمون باقی می‌مانند. این ثبت به معنی بازتنظیم یا تأیید مقدارها نیست.

**052 · S7-T024 — وضعیت: BLOCKED**

- مرز مسئولیت ثبت شد: Caller باید مشاهدات benchmark و provenance منبع‌محور، هویت شرکت و دوره، تاریخ مشاهدهٔ جلالی و شناسه‌ها و ارجاعات منبع را فراهم کند؛ برای ادعای PIT تاریخی، شواهد زمان انتشار/دسترس‌پذیری و پیوند EPS و قیمت را هم لازم دارد.
- Stage 7 باید provenance را اعتبارسنجی کند، موارد مفقود یا ناسازگار را رد یا fail-closed کند، زمان انتشار را از تاریخ مشاهده استنباط نکند و P/E تاریخی precomputed و اثبات‌نشده را نپذیرد.
- کد benchmarkها را به‌صورت float ساده می‌گیرد و این اعتبارسنجی‌ها را اجرا نمی‌کند؛ شواهد واقعی provenance زمانی نیز ارائه نشده است. بنابراین قرارداد مشخص است، اما پیاده‌سازی و شواهد لازم غایب‌اند.

## تغییرات و بررسی‌ها

- فایل‌های تغییرکرده: [STAGE7_MASTER_WORKING_PACKET.md](</D:/winprojects/analyzer/STAGE7_MASTER_WORKING_PACKET.md>) و [07_Stage7_Valuation.md](</D:/winprojects/analyzer/07_Stage7_Valuation.md>).
- وضعیت‌های نهایی در Master Packet: **029 PARTIAL، 030 PARTIAL، 048 DONE برای ثبت تصمیم، 052 BLOCKED**.
- فایل‌های بررسی‌شده: `PROMPT.md`، `WORKFLOW_RULES.md`، `STAGE7_MASTER_WORKING_PACKET.md`، `07_Stage7_Valuation.md`، `src/valuation/parameters.py`، `src/valuation/engine.py`، `src/valuation/schema.py` و `src/valuation/models.py`.
- هیچ کد تولیدی یا تستی تغییر نکرد و هیچ آزمونی اجرا نشد. `git diff --check` برای بررسی قالب تغییرات اجرا شد.
- تغییرات از پیش موجود در `prompt.md` و `ztest.txt` دست‌نخورده ماندند.
- پس از اصلاح مستندات، تناقض شناخته‌شده‌ای میان Master Packet و مشخصات Stage 7 باقی نماند. برای رفع موانع 029 و 052 هنوز vintageهای تاریخ‌دار و شواهد منبع‌دار PIT، به‌علاوهٔ اعتبارسنجی زمان اجرا، لازم است؛ این شواهد در محدودهٔ فایل‌های ارائه‌شده موجود نبودند.


## گزارش Package 2 — Implement Core OA1 Remediation

**022 · S7-T013 — BLOCKED**

Historical Forward P/E هنوز از ورودی `historical_pe_values` می‌آید؛ این آرایه هویت شرکت و دوره، تاریخ‌های مشاهده و provenance قابل‌اعتبارسنجی ندارد. قرارداد موجودی برای پیوند Forecastهای تاریخی به قیمت‌های متناظر پیدا نشد؛ سری تاریخی یا ارزیابی نسبی جدیدی نساختم.

**023 · S7-T014 — BLOCKED**

مدل‌های مالی فیلدهای شرکت، دوره، نسخهٔ گزارش و provenance را دارند، اما در فایل‌های مجاز نگاشت تأییدشده‌ای از `metric_code` به EPS یا قرارداد انتخاب EPS برای محاسبه پیدا نشد. بنابراین P/E تاریخی از این داده‌ها مشتق نشد.

**024 · S7-T015 — BLOCKED**

سرویس Stage 7 یک `CompanyForecastResult` دریافت می‌کند و رابطی برای انتخاب میان مجموعه‌ها یا نسخه‌های نامزد ندارد. قرارداد موجود نیز کامل‌بودن ورودی و فهرست دقیق موارد مفقود را تعریف نمی‌کند؛ قاعدهٔ تازه‌ای برای fallback نساختم.

**025 · S7-T016 — PARTIAL**

مسیر موجود قیمت واجدشرایط جلالی را انتخاب می‌کند و در نبود قیمت fail-closed می‌ماند. در [service.py](</D:/winprojects/analyzer/src/valuation/service.py>) هشدار `WARNING:MARKET_PRICE_DATE_MISMATCH` اضافه شد که تاریخ تحلیل و تاریخ واقعی قیمت انتخاب‌شده را نشان می‌دهد؛ تاریخ در قالب جلالی باقی می‌ماند.

تست‌هایی برای قیمت هم‌روز، قیمت قدیمی‌تر و هشدار تاریخ اضافه شدند. تست‌های موجود نیز قیمت آینده، نبود قیمت و تاریخ‌های تکراری یا نامعتبر را پوشش می‌دهند. اجرا نشدند.

**026 · S7-T017 — PARTIAL**

در [engine.py](</D:/winprojects/analyzer/src/valuation/engine.py>) Industry Forward/TTM P/E دیگر Target P/E را انتخاب نمی‌کند و هشدارهای مقایسه‌ای Industry و پرچم‌های فعال مربوط به تعداد peer حذف شدند. medianها و شمار peer فقط به‌صورت اطلاعات legacy باقی می‌مانند و metadata این وضعیت را مشخص می‌کند.

تست‌هایی برای استقلال Target P/E، وضعیت ارزانی/گرانی و هشدارها از ورودی Industry اضافه یا اصلاح شدند. اجرا نشدند.

**027 · S7-T018 — BLOCKED**

موتور هنوز آرایهٔ عددی `historical_pe_values` را می‌پذیرد و به‌عنوان historical context مصرف می‌کند؛ بنابراین رد precomputed P/E فاقد provenance پیاده نشده است. برای تکمیل این کار باید قرارداد ورودی مبتنی بر مشاهدات منبع‌دار مشخص باشد.

## فایل‌ها و راستی‌آزمایی

فایل‌های تغییرکرده:

- `src/valuation/engine.py`
- `src/valuation/service.py`
- `src/tests/test_stage7_valuation.py`
- `src/tests/test_stage789_service_interface.py`
- `STAGE7_MASTER_WORKING_PACKET.md`

فایل‌های بررسی‌شده:

`PROMPT.md`، `WORKFLOW_RULES.md`، `STAGE7_MASTER_WORKING_PACKET.md`، `07_Stage7_Valuation.md`، فایل‌های مجاز `src/valuation/`، `src/forecast/schema.py`، `src/ingestion/market/queries.py`، مدل‌های مجاز بازار و مالی، `src/core/jalali.py`، `src/core/database.py` و سه فایل تست تعیین‌شده در Prompt.

Master Packet به‌روزرسانی شد: **022، 023، 024 و 027 مسدود؛ 025 و 026 نیمه‌تمام و منتظر اجرای تست کاربر** هستند. هیچ کد persistence یا جدول تحلیلی اضافه نشد و دادهٔ تاریخی یا provenance ساختگی ایجاد نشد. هیچ تست، migration یا فرمان برنامه اجرا نشد؛ فقط `git diff --check` اجرا شد.

برای بازکردن Task 023، نگاشت/کاتالوگ معتبر EPS لازم است؛ مسیر دقیق آن از فایل‌های مجاز قابل‌شناسایی نبود و بیرون از scope جست‌وجو نشد. `prompt.md` که از قبل تغییر داشت، دست‌نخورده باقی ماند.

## Package 3 تکمیل شد؛ تنها فایل تغییر‌یافته [STAGE7_MASTER_WORKING_PACKET.md](D:/winprojects/analyzer/STAGE7_MASTER_WORKING_PACKET.md) است. آزمون یا اجرای برنامه انجام نشد، مطابق محدودیت‌های `PROMPT.md`.

### وضعیت Taskها

- **031 · S7-T009 — DONE (ممیزی):** بازاعتبارسنجی نشان داد یک مرز واقعی کتابخانه‌ای Stage 7→9 وجود دارد، اما مسیر کامل تولیدی تا Stage 9 ثابت نیست.
- **032 · S7-T010 — BLOCKED:** تست `test_stage789_service_interface.py` سرویس Stage 7→9 را با query واقعی قیمت بازار اجرا می‌کند، اما Forecast، Fundamental و Market را خودش می‌سازد؛ پس E2E مسیر تولیدی محسوب نمی‌شود.
- **036 · S7-PLAN-002 — BLOCKED:** entrypoint هماهنگ‌کننده و مالک چرخهٔ عمر Session در مسیر اجرای مراحل اثبات نشد.
- **020 · S7-TEST-004 — BLOCKED:** تا وقتی مسیر تولیدی واقعی وجود نداشته باشد، callable و فرمان معتبر برای تست E2E قابل تعیین نیست.

### شواهد و مرز نتیجه‌گیری

`calculate_decision_as_of_jalali` در `src/decision/service.py` Forecast، Fundamental، Market، Session و تاریخ جلالی را از caller می‌گیرد؛ سپس `calculate_valuation_as_of_jalali` را اجرا می‌کند و نتیجهٔ Valuation را به `DecisionEngine.make_decision` می‌دهد. این تابع handoff Stage 7→9 را ثابت می‌کند، اما تولید نتایج بالادست یا فراخوانی از برنامه/UI را ثابت نمی‌کند.

در مرزهای دیگر، `FundamentalScoringEngine.calculate_score` در `src/scoring/engine.py` KPIهای آماده می‌گیرد؛ `TrendEngine.evaluate_trend` در `src/trend/engine.py` سری تاریخی آماده می‌گیرد؛ `generate_and_persist_forecast` در `src/forecast/service.py` facts و `TrendResult` را مصرف می‌کند؛ و `analyze_market_as_of_jalali` در `src/market/service.py` برای Market از Session استفاده می‌کند. caller تولیدی که این مراحل را به هم وصل کند در فایل‌های مجاز بررسی‌شده اثبات نشد. `SessionLocal` در `src/core/database.py` فقط factory را تعریف می‌کند؛ اسکریپت‌های `init_db.py` و `migrate_db.py` برای ساخت یا ارتقای schema هستند.

در نتیجه، **مسیر کامل اجرای تولیدی تا Stage 9 اثبات نشد**. اجزای مفقود که ثبت شدند: caller برنامه‌ای برای تولید و انتقال ورودی‌های Stage 3/4/5/8، مدیریت lifecycle و transaction برای Session در اجرای مراحل، و مصرف برنامه‌ای خروجی Stage 9.

# Package 4 — Final Valuation Engine Review
# 033 · S7-T011 — بازبینی نهایی Valuation Engine: **PARTIAL**

کد و تست‌های موجود را در حوزه‌های محاسبات و گردکردن، ترتیب سناریوها، نرمال‌سازی احتمال‌ها، پارامترها و metadata، وضعیت ارزش‌گذاری، EPS و تغییر علامت، ورودی‌های نامعتبر، کنترل PIT، هشدارها و خروجی بررسی کردم.

دو ایراد مستقل از قراردادهای بالادستی اصلاح شد:

- **عدم تطبیق هویت Forecast:** `ValuationEngine.calculate_valuation` پیش از اصلاح می‌توانست Forecast متعلق به شرکت یا دوره‌ای دیگر را بپذیرد، در حالی که قرارداد OA1.5 اختلاط هویت شرکت و دوره را منع می‌کند. Engine اکنون در صورت اختلاف `company_id` یا `forecast_period_id` خطای `ValueError` می‌دهد. تست پارامتری برای هر دو حالت اضافه شد.
- **عدد صحیح خارج از محدودهٔ float:** `_finite_or_none` و `_clamp_score` مقدارهایی که تبدیلشان به float با `OverflowError` شکست می‌خورد، مدیریت نمی‌کردند. اکنون این خطا نیز مانند ورودی نامعتبر/غیرمتناهی guard می‌شود. تستی برای قیمت، EPS و کیفیت دادهٔ خارج از محدودهٔ float افزوده شد.

Task را کامل نمی‌بندم: `historical_pe_values` هنوز دنباله‌ای از P/E ازپیش‌محاسبه‌شده و فاقد provenance قابل‌تأیید است. اصلاح آن به OA1.2/OA1.3 و کارهای مسدود 022، 023 و 027 وابسته است؛ طبق prompt نباید برای آن قرارداد یا workaround بسازم. اعتبار زمانی کامل پارامترها و PIT نیز با توجه به وضعیت PARTIAL در Task 029 اثبات نمی‌شود. Industry P/E از انتخاب فعال Target P/E کنار گذاشته شده؛ رفتار legacy آن را به‌عنوان defect گزارش نکردم.

## 038 · S7-PLAN-004 — اصلاح کنترل‌شده و تست‌های رگرسیون: **PARTIAL**

فقط دو اصلاح بالا در `engine.py` انجام شد و تست‌های متمرکز برایشان به `test_stage7_valuation.py` اضافه شد. فرمول مالی، پارامترها، آستانه‌ها، وزن سناریوها و قواعد گردکردن تغییر نکردند. تست‌ها اجرا نشدند.

## کنترل فایل‌ها

فایل‌های بررسی‌شده: `PROMPT.md`، `WORKFLOW_RULES.md`، `STAGE7_MASTER_WORKING_PACKET.md`، `07_Stage7_Valuation.md`، `src/valuation/engine.py`، `src/valuation/models.py`، `src/valuation/parameters.py`، `src/valuation/schema.py`، `src/valuation/service.py`، `src/forecast/schema.py` و `src/tests/test_stage7_valuation.py`.

فایل‌های تغییر‌یافته:

- [src/valuation/engine.py](D:/winprojects/analyzer/src/valuation/engine.py)
- [src/tests/test_stage7_valuation.py](D:/winprojects/analyzer/src/tests/test_stage7_valuation.py)

فایل دیگری برای بررسی لازم نشد. Master Packet یا فایل دیگری تغییر نکرد. `PROMPT.md` را برای خواندن دستور Package خواندم، با اینکه خود prompt در محدودیتش گفته بود آن فایل بررسی نشود.

## ایمنی مالی

- فرمول مالی: **تغییر نکرد**.
- پارامتر، آستانه، وزن سناریو و قاعدهٔ گردکردن: **تغییر نکرد**.
- فرض مالی جدید: **وارد نشد**.
- ادعای PIT یا provenance: **تقویت نشد**.
- وابستگی حل‌نشده: **بله**؛ provenance و مشتق‌سازی تاریخی P/E، انتخاب مجموعهٔ کامل ورودی‌ها، و اثبات PIT کامل همچنان باز هستند.

## فرمان‌های آزمون برای کاربر

من آزمون یا فرمان اجرایی اجرا نکردم. لطفاً اجرا کنید:

```text
pytest src/tests/test_stage7_valuation.py -q
```

تغییرات این Package مرز سرویس Stage 7/9 را دست نزده‌اند؛ بنابراین فرمان تست رابط سرویس لازم نیست.

## نتیجه

دو guard فنی برای تطبیق هویت Forecast و اعداد خارج از محدودهٔ float اصلاح و برایشان تست اضافه شد. سایر رفتارها ممیزی شدند؛ موارد وابسته به قراردادهای حل‌نشده عمداً تغییر نکردند. **Task 033 هنوز قابل بستن نیست**؛ اجرای تست‌ها و تعیین تکلیف وابستگی‌های بالادستی باقی است.

(analyzer) PS D:\winprojects\analyzer> pytest src/tests/test_stage7_valuation.py -q
..............................................................................................................   [100%]
110 passed in 1.13s

# Package 5 — Regression, Audit & Stage 7 Closure
1. Input File Verification
هر 51 فایل فهرست‌شده در مسیر محلی پروژه موجود است: 6 سند/تنظیم، 10 فایل کد و هر 35 فایل تست. فایل مفقودی نداریم.

برای بررسی حضور فایل‌ها از فهرست دقیق خود Prompt استفاده شد؛ جست‌وجوی بیرون از فهرست انجام نشد. یک انحراف از دستور Prompt هم باید شفاف باشد: برای خواندن دستور Package، PROMPT.md را باز کردم، با اینکه Prompt خودش گفته بود آن فایل بررسی نشود.

2. Task 019 — Skip Audit
در سورس تست‌ها دو محل Skip محتمل پیدا شد:

test_codal_extraction.py: تست PDF واقعی Codal با skipif اجرا نمی‌شود اگر هیچ‌یک از مسیرهای نمونهٔ محلی یا CODAL_SAMPLE_PDF فایل معتبری نداشته باشند. این Skip وابسته به محیط و نمونه‌داده است، نه دائمی. حذف این تست از اجرای محیطی که نمونه PDF ندارد قابل‌قبول است، اما آزمون واقعی استخراج PDF را در آن اجرا اثبات نمی‌کند.
test_ingestion_fx.py: تست XLSX با pytest.importorskip("openpyxl") به وجود کتابخانه در محیط اجرا وابسته است. openpyxl در requirements.txt فهرست شده و workflow CI وابستگی‌های فایل را نصب می‌کند؛ بنابراین در محیط استاندارد CI نباید Skip شود. نبود پکیج در اجرای محلی می‌تواند پوشش ورود XLSX را حذف کند.
علت runtime دو Skip اثبات نشده است. سابقهٔ اجرای کامل فقط 2 skipped را ثبت کرده و خروجی pytest -rs در دسترس نیست. برای تعیین علت واقعی باید کاربر اجرای جدید را همراه -rs ارائه کند. در وضعیت فعلی Task 019 باز می‌ماند.

3. Task 021 — OA1 Test Coverage Matrix

الزام OA1	شواهد تست و آنچه واقعاً ثابت می‌کند	شکاف / وضعیت
Historical Forward P/E از دادهٔ خام همان شرکت	تستی که محاسبهٔ تاریخی Forward P/E را از مشاهدات مالی و بازار شرکت بسازد پیدا نشد.	اثبات نشده؛ 022 و 023 BLOCKED هستند.
مشاهدات همراه provenance معتبر	تست‌های Stage 5، provenance ورودی Forecast را تا cutoff بررسی می‌کنند؛ تست‌های market query هویت ردیف، شناسه و تاریخ جلالی را حفظ می‌کنند. تست‌های Stage 7 نیز رد refهای آینده یا بدون تاریخ را پوشش می‌دهند.	این‌ها اعتبار زمانی مشاهده‌های تاریخی Forward P/E، زمان انتشار/availability بازار، یا رابطهٔ EPS و قیمت را ثابت نمی‌کنند.
انتخاب آخرین مجموعهٔ کامل و معتبر	تستی برای fallback به آخرین مجموعهٔ کامل، هشدار دادهٔ جدید ناقص و فهرست ورودی‌های مفقود وجود ندارد.	اثبات نشده؛ 024 BLOCKED است.
انتخاب قیمت با تاریخ جلالی و هشدار تاریخ واقعی	تست‌های query بازار مرز as-of و حذف قیمت آینده را پوشش می‌دهند؛ تست‌های Stage 7 سرویس، تاریخ انتخاب‌شده، هشدار اختلاف و fail-closed را بررسی می‌کنند.	برای رفتار انتخاب قیمت و هشدار شواهد مناسب وجود دارد؛ این تست‌ها زنجیرهٔ کامل production را ثابت نمی‌کنند. 025 DONE در محدودهٔ خودش.
رد P/E پیش‌محاسبه‌شده بدون provenance	Engine هنوز historical_pe_values را به صورت sequence عددی می‌پذیرد؛ تستی که آن را به‌دلیل فقدان provenance رد کند وجود ندارد. تست benchmark بدون provenance نیز محدودیت را تصریح می‌کند.	اثبات نشده؛ 027 BLOCKED است.
عدم وابستگی به Industry P/E	تست‌ها نشان می‌دهند ورودی Industry، Target P/E، وضعیت ارزندگی و هشدارهای نسبی را تغییر نمی‌دهد.	رفتار فعال این سیاست پوشش دارد؛ 026 DONE در محدودهٔ خودش.
تطبیق هویت Forecast با شرکت و دوره	تست پارامتری mismatch شرکت و دوره را بررسی می‌کند؛ Engine در mismatch خطا می‌دهد.	پوشش مستقیم منفی برای این guard وجود دارد؛ به‌تنهایی E2E نیست.
Overflow و مقادیر غیرمتناهی	تست‌های NaN/Inf برای قیمت، EPS و scoreها موجودند؛ regression test برای integer خارج از محدودهٔ float نیز اضافه شده است.	پوشش فنی ورودی عددی؛ اعتبار مالی یا provenance را ثابت نمی‌کند. Master Packet اجرای کاربر برای تست Stage 7 را 110 passed ثبت کرده است.
تست‌های query بازار و سرویس Stage 7→9 از اجزای واقعی همان مرز استفاده می‌کنند، اما service-interface test نتایج Forecast، Fundamental و Market را خودش به‌صورت helper/fixture می‌سازد. پس اثبات مسیر E2E تولیدی نیست.

4. Task 037 — Final Test Commands
این فرمان‌ها پیشنهاد هستند و اجرا نشده‌اند:

تست‌های هدفمند:

powershell
pytest src/tests/test_market_history_query.py src/tests/test_stage789_service_interface.py src/tests/test_stage7_valuation.py src/tests/test_stage8_market.py src/tests/test_stage9_decision.py -q -rs
کل مجموعه:

powershell
pytest src/tests -q -rs
گزینهٔ -rs برای ثبت علت runtime هر Skip لازم است.

5. Task 020 — E2E Audit
مسیر کامل تولیدی تا Stage 9 اثبات نشده است. calculate_decision_as_of_jalali handoff واقعی کتابخانه‌ای Stage 7→9 دارد، اما Forecast، Fundamental، Market، Session و تاریخ تحلیل را از caller می‌گیرد. یک entrypoint برنامه‌ای که Stageهای 3، 4، 5، 8، 7 و 9 را به هم وصل کند و مالک Session باشد، در فایل‌های مجاز اثبات نشده است.

تست test_stage789_service_interface.py این handoff و query قیمت واقعی را می‌آزماید، ولی نتایج Forecast، Fundamental و Market را خودش می‌سازد. در نتیجه، Task 020 همچنان BLOCKED و E2E واقعی فعلاً قابل اثبات نیست.

6. Task 034 — Exit Criteria Review

معیار	وضعیت	شواهد و مانع
040 · S7-EXIT-001 — سازگاری کد، مشخصات و تست با V1 و OA1	BLOCKED	OA1.1–1.3 و OA1.5 هنوز در پیاده‌سازی کامل نیستند؛ 022، 023، 024 و 027 مسدودند.
041 · S7-EXIT-002 — D7/D9 و PIT	BLOCKED	029 PARTIAL است؛ provenance زمانی و vintage معتبر تاریخی وجود ندارد. تاریخ مشاهده یا cutoff به‌تنهایی PIT کامل را ثابت نمی‌کند.
042 · S7-EXIT-003 — قرارداد هشدارها و مصرف‌کنندگان	BLOCKED	OA1.6 پیاده‌سازی و تست شده؛ اما رفتار OA1.5، یعنی انتخاب مجموعهٔ کامل و هشدار کمبود، هنوز پیاده‌سازی نشده است. 024 مسدود است.
043 · S7-EXIT-004 — مسیر واقعی تا Stage 9 یا ثبت شکاف و تصمیم	BLOCKED	شکاف معماری، نبود caller و اثر آن در Taskهای 031/032/036 ثبت شده؛ مسیر و تست E2E وجود ندارد و ثبت صریح تصمیم مالک برای نحوهٔ رفع این شکاف در شواهد فعلی دیده نمی‌شود.
044 · S7-EXIT-005 — خروجی تست‌های کاربر و علت Skipها	BLOCKED	نتایج قدیمی و هدفمند ثبت شده‌اند، از جمله 110 پاس Stage 7؛ اما خروجی کامل جدید با -rs و علت runtime Skipها موجود نیست.
045 · S7-EXIT-006 — بازنگری نهایی Engine	BLOCKED	Package 4 بازنگری مقدماتی و دو اصلاح داشته؛ Master Packet آن را به‌علت وابستگی‌های حل‌نشده، نهایی نمی‌داند.
046 · S7-EXIT-007 — تعیین تکلیف موانع بحرانی و Forecast persistence	BLOCKED	تصمیم R-05 منع ذخیره‌سازی خروجی تحلیلی را روشن کرده، اما Forecast هنوز در generate_and_persist_forecast با persist=True پیش‌فرض ذخیره می‌شود. اصلاح Stage 7 spec در 053-10 و remediation کد/مدل/تست در 054–057 باز است.
047 · S7-EXIT-008 — حذف Industry P/E و پیاده‌سازی same-company historical Forward P/E	BLOCKED	حذف Industry P/E از مسیر فعال تست شده؛ same-company historical Forward P/E هنوز پیاده‌سازی و تأیید نشده است. 022 مسدود است.
تعارض باقی‌ماندهٔ OA1.7
Stage 5 spec فعلی ذخیره‌سازی Forecast را صریحاً ممنوع و متن‌های قدیمی را superseded می‌داند. بااین‌حال OA1.7 در 07_Stage7_Valuation.md هنوز می‌گوید Stage 5 spec حفظ Forecast Versioning را الزام می‌کند و تعارض مستنداتی unresolved است. طبق Master Packet، اصلاح این ارجاع در 053-10 باز است.

جدا از متن سند، کد src/forecast/service.py همچنان نام generate_and_persist_forecast، پارامتر persist=True و فراخوانی ForecastRecordRepository.save() دارد. تصمیم R-05 معلوم است، اما remediation اجرایی و migration ایمن کامل نشده‌اند.

7. Task 039 — Final Stage 7 Disposition
OPEN — BLOCKED

مانع‌های تعیین‌کننده شامل نبود same-company historical Forward P/E و provenance معتبر، نبود latest-complete-input selection، نبود مسیر production تا Stage 9، تعارض عملی Forecast persistence با R-05، و نامشخص‌بودن علت runtime Skipها هستند. معیارهای حیاتی 040–047 همگی PASS نشده‌اند.

8. Task Status Summary
این‌ها وضعیت‌های پیشنهادی بر اساس شواهد بررسی‌شده‌اند؛ هیچ وضعیت یا Taskی در Master Packet تغییر نکرده است.


Task	وضعیت پیشنهادی	توضیح
019 · S7-TEST-003	OPEN	علت واقعی Skipها به خروجی -rs نیاز دارد.
020 · S7-TEST-004	BLOCKED	مسیر کامل تولیدی/E2E اثبات نشده است.
021 · S7-TEST-005	PARTIAL	ممیزی پوشش انجام شد؛ الزامات اصلی OA1 هنوز پیاده‌سازی/تأیید نشده‌اند.
022 · S7-T013	BLOCKED	قرارداد و provenance تاریخچهٔ Forward P/E موجود نیست.
023 · S7-T014	BLOCKED	نگاشت/قرارداد انتخاب EPS خام برای Historical P/E تصویب و اثبات نشده است.
024 · S7-T015	BLOCKED	قرارداد انتخاب مجموعهٔ کامل ورودی‌ها موجود نیست.
025 · S7-T016	DONE	انتخاب قیمت جلالی، هشدار تاریخ و fail-closed در محدودهٔ مصوب تست شده‌اند.
026 · S7-T017	DONE	Industry P/E از مسیر فعال حذف شده است.
027 · S7-T018	BLOCKED	ورودی عددی تاریخی بدون provenance هنوز رد نمی‌شود.
029 · S7-T007	PARTIAL	سیاست مستند است؛ vintage و PIT runtime کامل نیست.
030 · S7-T008	PARTIAL	OA1.5 و D6/قراردادهای مرتبط هنوز تعیین تکلیف اجرایی نشده‌اند.
031 · S7-T009	DONE، فقط ممیزی	audit کامل است؛ به معنی وجود مسیر تولیدی نیست.
032 · S7-T010	BLOCKED	تست E2E معتبر وابسته به مسیر واقعی است.
033 · S7-T011	BLOCKED	بازنگری مقدماتی انجام شده؛ وابستگی‌های لازم برای بستن نهایی بازند.
034 · S7-T012	OPEN	گزارش اینجا معیارها را ارزیابی می‌کند، اما معیارها PASS نشده و Master Packet به‌روزرسانی نشده است.
035 · S7-PLAN-001	OPEN / وابسته	اجرای اصلاحات PIT/قرارداد تا فراهم‌شدن شواهد معتبر متوقف می‌ماند.
036 · S7-PLAN-002	BLOCKED	caller واقعی و Session lifecycle تولیدی اثبات نشده است.
037 · S7-PLAN-003	OPEN	کاربر باید تست هدفمند و کامل را اجرا و خروجی ارائه کند.
038 · S7-PLAN-004	PARTIAL	دو اصلاح و تست رگرسیون ثبت شده؛ این Task بازنگری نهاییِ وابسته به سایر Taskها را جایگزین نمی‌کند.
039 · S7-PLAN-005	BLOCKED	تعیین وضعیت نهایی انجام شد؛ Stage 7 بسته نیست.
053 · S7-T025	PARTIAL	Stage 5 spec هم‌تراز شده؛ عملیات 053-10 در Stage 7 spec باز است.
054 · S7-T026	OPEN	write path Forecast persistence باقی است.
055 · S7-T027	OPEN	حذف schema با migration ایمن انجام نشده است.
056 · S7-T028	OPEN	تست‌های معماری no-persistence تکمیل نشده‌اند.
057 · S7-T029	OPEN	audit حفظ جریان runtime و مصرف‌کنندگان Forecast باقی است.
053-10	OPEN	ارجاع منسوخ OA1.7 در سند Stage 7 هنوز نیازمند اصلاح و بازخوانی است.
9. Remaining Blockers
022، 023، 027: قرارداد محاسبهٔ Historical P/E/Forward P/E از دادهٔ خام و provenance موردنیاز — نیازمند تعریف ورودی‌ها و شواهد معتبر.
024: تعریف completeness برای ورودی‌ها، انتخاب/fallback و گزارش کمبودها — نیازمند قرارداد محاسباتی.
029 و 035: vintage تاریخی پارامتر و provenance زمانی — نیازمند نسخه‌ها و شواهد معتبر؛ پارامتر جاری جایگزین نسخهٔ تاریخی نمی‌شود.
032 و 036: entrypoint تولیدی، هماهنگ‌کنندهٔ مراحل، مالک Session و مصرف‌کنندهٔ خروجی Stage 9 — نیازمند طراحی/تصمیم اجرایی معتبر.
033 و 038: بازنگری نهایی Engine — پس از تعیین تکلیف وابستگی‌های بالا.
053-10: اصلاح ادعای متناقض/منسوخ OA1.7 در Stage 7 spec.
054–057: حذف persistence اجرایی Forecast، migration ایمن، تست no-persistence و تأیید انتقال runtime بدون قطع مصرف‌کنندگان.
019 و 044: اجرای کاربر با -rs برای تشخیص علت واقعی Skipها و ارائهٔ نتیجهٔ تازهٔ مجموعهٔ کامل.
10. User Execution Handoff
برای بررسی Skipها و وضعیت فعلی تست‌های مرتبط، ابتدا فرمان هدفمند را اجرا کنید و خروجی کامل—including بخش short test summary و Skip reasons—را بفرستید؛ سپس مجموعهٔ کامل را اجرا کنید:

powershell
pytest src/tests/test_market_history_query.py src/tests/test_stage789_service_interface.py src/tests/test_stage7_valuation.py src/tests/test_stage8_market.py src/tests/test_stage9_decision.py -q -rs
powershell
pytest src/tests -q -rs
من این فرمان‌ها را اجرا نکردم. هیچ فایل یا statusای تغییر نکرده و Stage 7 بسته اعلام نمی‌شود

(analyzer) PS D:\winprojects\analyzer> pytest src/tests/test_market_history_query.py src/tests/test_stage789_service_interface.py src/tests/test_stage7_valuation.py src/tests/test_stage8_market.py src/tests/test_stage9_decision.py -q -rs
................................................................................................................ [ 12%]
................................................................................................................ [ 25%]
................................................................................................................ [ 38%]
................................................................................................................ [ 51%]
................................................................................................................ [ 64%]
................................................................................................................ [ 77%]
................................................................................................................ [ 90%]
..............................................................................                                   [100%]
862 passed in 5.54s
(analyzer) PS D:\winprojects\analyzer> pytest src/tests -q -rs
.................s.............................................................................................. [  5%]
...........................................s.................................................................... [ 11%]
................................................................................................................ [ 17%]
................................................................................................................ [ 23%]
................................................................................................................ [ 29%]
................................................................................................................ [ 35%]
................................................................................................................ [ 41%]
................................................................................................................ [ 47%]
................................................................................................................ [ 52%]
................................................................................................................ [ 58%]
................................................................................................................ [ 64%]
................................................................................................................ [ 70%]
................................................................................................................ [ 76%]
................................................................................................................ [ 82%]
................................................................................................................ [ 88%]
................................................................................................................ [ 94%]
................................................................................................................ [ 99%]
.                                                                                                                [100%]
================================================== warnings summary ===================================================
src/tests/test_codal_pdf_extraction.py::test_malformed_pdf_is_rejected_and_ingestion_is_audited
  D:\winprojects\analyzer\src\ingestion\codal\ingestion.py:84: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    finished_at=datetime.utcnow(),

src/tests/test_stage1_rules.py::test_ingestion_run_contract
  D:\winprojects\analyzer\src\tests\test_stage1_rules.py:234: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    run = IngestionRun(source="CODAL", status="COMPLETED", records_found=10, records_inserted=9, records_updated=1, records_failed=0, finished_at=datetime.utcnow())

src/tests/test_stage2_kpis.py::test_universal_growth_kpis
src/tests/test_stage2_kpis.py::test_universal_growth_kpis
src/tests/test_stage2_kpis.py::test_universal_growth_zero_base_is_not_zero_growth
src/tests/test_stage2_kpis.py::test_eps_growth_requires_share_count_corporate_action_comparability
src/tests/test_stage2_kpis.py::test_data_quality_status_propagates_from_stage1_inputs
src/tests/test_stage2_kpis.py::test_industry_kpi_data_quality_propagates
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
  D:\winprojects\analyzer\src\kpi\universal.py:12: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    return KPIResult(company_id, period_id, "REVENUE_GROWTH", val, "PERCENTAGE", "VALID" if val is not None else "MISSING", datetime.utcnow())

src/tests/test_stage2_kpis.py::test_universal_growth_zero_base_is_not_zero_growth
src/tests/test_stage2_kpis.py::test_eps_growth_requires_share_count_corporate_action_comparability
src/tests/test_stage2_kpis.py::test_data_quality_status_propagates_from_stage1_inputs
src/tests/test_stage2_kpis.py::test_industry_kpi_data_quality_propagates
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
  D:\winprojects\analyzer\src\kpi\universal.py:17: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    return KPIResult(company_id, period_id, "OP_PROFIT_GROWTH", val, "PERCENTAGE", "VALID" if val is not None else "MISSING", datetime.utcnow())

src/tests/test_stage2_kpis.py::test_universal_growth_zero_base_is_not_zero_growth
src/tests/test_stage2_kpis.py::test_eps_growth_requires_share_count_corporate_action_comparability
src/tests/test_stage2_kpis.py::test_data_quality_status_propagates_from_stage1_inputs
src/tests/test_stage2_kpis.py::test_industry_kpi_data_quality_propagates
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
  D:\winprojects\analyzer\src\kpi\universal.py:22: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    return KPIResult(company_id, period_id, "NET_PROFIT_GROWTH", val, "PERCENTAGE", "VALID" if val is not None else "MISSING", datetime.utcnow())

src/tests/test_stage2_kpis.py::test_universal_growth_zero_base_is_not_zero_growth
src/tests/test_stage2_kpis.py::test_eps_growth_requires_share_count_corporate_action_comparability
src/tests/test_stage2_kpis.py::test_data_quality_status_propagates_from_stage1_inputs
src/tests/test_stage2_kpis.py::test_industry_kpi_data_quality_propagates
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
  D:\winprojects\analyzer\src\kpi\universal.py:27: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    return KPIResult(company_id, period_id, "EPS_GROWTH", val, "PERCENTAGE", "VALID" if val is not None else "MISSING", datetime.utcnow())

src/tests/test_stage2_kpis.py::test_universal_profitability_kpis
src/tests/test_stage2_kpis.py::test_universal_profitability_zero_denominators_are_missing
src/tests/test_stage2_kpis.py::test_eps_growth_requires_share_count_corporate_action_comparability
src/tests/test_stage2_kpis.py::test_data_quality_status_propagates_from_stage1_inputs
src/tests/test_stage2_kpis.py::test_industry_kpi_data_quality_propagates
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
  D:\winprojects\analyzer\src\kpi\universal.py:38: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    return KPIResult(company_id, period_id, "OPERATING_MARGIN", val, "PERCENTAGE", "VALID" if val is not None else "MISSING", datetime.utcnow())

src/tests/test_stage2_kpis.py::test_universal_profitability_kpis
src/tests/test_stage2_kpis.py::test_universal_profitability_zero_denominators_are_missing
src/tests/test_stage2_kpis.py::test_eps_growth_requires_share_count_corporate_action_comparability
src/tests/test_stage2_kpis.py::test_data_quality_status_propagates_from_stage1_inputs
src/tests/test_stage2_kpis.py::test_industry_kpi_data_quality_propagates
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
  D:\winprojects\analyzer\src\kpi\universal.py:53: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    return KPIResult(company_id, period_id, "ROE", val, "PERCENTAGE", "VALID" if val is not None else "MISSING", datetime.utcnow())

src/tests/test_stage2_kpis.py::test_universal_profitability_zero_denominators_are_missing
src/tests/test_stage2_kpis.py::test_eps_growth_requires_share_count_corporate_action_comparability
src/tests/test_stage2_kpis.py::test_data_quality_status_propagates_from_stage1_inputs
src/tests/test_stage2_kpis.py::test_industry_kpi_data_quality_propagates
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
  D:\winprojects\analyzer\src\kpi\universal.py:33: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    return KPIResult(company_id, period_id, "GROSS_MARGIN", val, "PERCENTAGE", "VALID" if val is not None else "MISSING", datetime.utcnow())

src/tests/test_stage2_kpis.py::test_universal_profitability_zero_denominators_are_missing
src/tests/test_stage2_kpis.py::test_eps_growth_requires_share_count_corporate_action_comparability
src/tests/test_stage2_kpis.py::test_data_quality_status_propagates_from_stage1_inputs
src/tests/test_stage2_kpis.py::test_industry_kpi_data_quality_propagates
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
  D:\winprojects\analyzer\src\kpi\universal.py:43: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    return KPIResult(company_id, period_id, "NET_MARGIN", val, "PERCENTAGE", "VALID" if val is not None else "MISSING", datetime.utcnow())

src/tests/test_stage2_kpis.py::test_universal_profitability_zero_denominators_are_missing
src/tests/test_stage2_kpis.py::test_eps_growth_requires_share_count_corporate_action_comparability
src/tests/test_stage2_kpis.py::test_data_quality_status_propagates_from_stage1_inputs
src/tests/test_stage2_kpis.py::test_industry_kpi_data_quality_propagates
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
  D:\winprojects\analyzer\src\kpi\universal.py:48: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    return KPIResult(company_id, period_id, "ROA", val, "PERCENTAGE", "VALID" if val is not None else "MISSING", datetime.utcnow())

src/tests/test_stage2_kpis.py::test_universal_risk_and_quality_kpis
src/tests/test_stage2_kpis.py::test_eps_growth_requires_share_count_corporate_action_comparability
src/tests/test_stage2_kpis.py::test_data_quality_status_propagates_from_stage1_inputs
src/tests/test_stage2_kpis.py::test_industry_kpi_data_quality_propagates
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
  D:\winprojects\analyzer\src\kpi\universal.py:60: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    return KPIResult(company_id, period_id, "CASH_CONVERSION", val, "RATIO", "VALID" if val is not None else "MISSING", datetime.utcnow())

src/tests/test_stage2_kpis.py::test_universal_risk_and_quality_kpis
src/tests/test_stage2_kpis.py::test_eps_growth_requires_share_count_corporate_action_comparability
src/tests/test_stage2_kpis.py::test_data_quality_status_propagates_from_stage1_inputs
src/tests/test_stage2_kpis.py::test_industry_kpi_data_quality_propagates
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
  D:\winprojects\analyzer\src\kpi\universal.py:71: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    status, datetime.utcnow(),

src/tests/test_stage2_kpis.py::test_conditional_financial_cost_pressure
src/tests/test_stage2_kpis.py::test_conditional_financial_cost_pressure
src/tests/test_stage2_kpis.py::test_eps_growth_requires_share_count_corporate_action_comparability
src/tests/test_stage2_kpis.py::test_data_quality_status_propagates_from_stage1_inputs
src/tests/test_stage2_kpis.py::test_industry_kpi_data_quality_propagates
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
  D:\winprojects\analyzer\src\kpi\conditional.py:33: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    calculation_timestamp=datetime.utcnow(),

src/tests/test_stage2_kpis.py::test_bank_industry_kpis
src/tests/test_stage2_kpis.py::test_industry_kpi_data_quality_propagates
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
  D:\winprojects\analyzer\src\kpi\industry.py:12: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    KPIResult(company_id, period_id, "BANK_NII", nii, "CURRENCY_IRR", "VALID" if nii is not None else "MISSING", datetime.utcnow()),

src/tests/test_stage2_kpis.py::test_bank_industry_kpis
src/tests/test_stage2_kpis.py::test_industry_kpi_data_quality_propagates
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
  D:\winprojects\analyzer\src\kpi\industry.py:13: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    KPIResult(company_id, period_id, "BANK_NIM", nim, "PERCENTAGE", "VALID" if nim is not None else "MISSING", datetime.utcnow()),

src/tests/test_stage2_kpis.py::test_bank_industry_kpis
src/tests/test_stage2_kpis.py::test_industry_kpi_data_quality_propagates
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
  D:\winprojects\analyzer\src\kpi\industry.py:14: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    KPIResult(company_id, period_id, "BANK_LOAN_GROWTH", loan_growth, "PERCENTAGE", "VALID" if loan_growth is not None else "MISSING", datetime.utcnow()),

src/tests/test_stage2_kpis.py::test_bank_industry_kpis
src/tests/test_stage2_kpis.py::test_industry_kpi_data_quality_propagates
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
  D:\winprojects\analyzer\src\kpi\industry.py:15: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    KPIResult(company_id, period_id, "BANK_DEPOSIT_GROWTH", deposit_growth, "PERCENTAGE", "VALID" if deposit_growth is not None else "MISSING", datetime.utcnow()),

src/tests/test_stage2_kpis.py::test_bank_industry_kpis
src/tests/test_stage2_kpis.py::test_industry_kpi_data_quality_propagates
src/tests/test_stage2_kpis.py::test_kpi_engine_full_run
  D:\winprojects\analyzer\src\kpi\industry.py:16: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    KPIResult(company_id, period_id, "BANK_NPL", npl, "PERCENTAGE", "VALID" if npl is not None else "MISSING", datetime.utcnow()),

src/tests/test_stage2_kpis.py::test_holding_industry_kpis
  D:\winprojects\analyzer\src\kpi\industry.py:23: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    KPIResult(company_id, period_id, "HOLDING_NAV", nav, "CURRENCY_IRR", "VALID" if nav is not None else "MISSING", datetime.utcnow()),

src/tests/test_stage2_kpis.py::test_holding_industry_kpis
  D:\winprojects\analyzer\src\kpi\industry.py:24: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    KPIResult(company_id, period_id, "HOLDING_NAV_GROWTH", nav_growth, "PERCENTAGE", "VALID" if nav_growth is not None else "MISSING", datetime.utcnow()),

src/tests/test_stage2_kpis.py::test_holding_industry_kpis
  D:\winprojects\analyzer\src\kpi\industry.py:25: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    KPIResult(company_id, period_id, "HOLDING_P_NAV", p_nav, "RATIO", "VALID" if p_nav is not None else "MISSING", datetime.utcnow()),

src/tests/test_stage2_kpis.py::test_optional_sales_volume_missing_is_not_zero
src/tests/test_stage2_kpis.py::test_optional_sales_volume_missing_is_not_zero
src/tests/test_stage2_kpis.py::test_optional_sales_volume_missing_is_not_zero
  D:\winprojects\analyzer\src\kpi\industry.py:39: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    calculation_timestamp=datetime.utcnow(),

src/tests/test_stage4_trend.py: 53 warnings
  D:\winprojects\analyzer\src\trend\engine.py:235: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    calculation_timestamp=datetime.utcnow(),

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=============================================== short test summary info ===============================================
SKIPPED [1] src\tests\test_codal_extraction.py:398: real Codal sample PDF not available in CI
SKIPPED [1] src\tests\test_ingestion_fx.py:194: could not import 'openpyxl': No module named 'openpyxl'
1903 passed, 2 skipped, 153 warnings in 235.08s (0:03:55)