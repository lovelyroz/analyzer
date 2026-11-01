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

# Supplementary Audit — Pytest Warnings, Skip Causes & Timestamp Safety
## 1. Input File Verification

همهٔ 18 فایل مستندات، کد و تستی که Prompt نام برده موجودند. پوشهٔ محلی `pdf/` هم موجود است و دقیقاً این 19 فایل را دارد:

`seo-codal-report (1).pdf`, `(2)`, `(3)`, `(4)`, `(6)`, `(7)`, `(8)`, `(9)`, `(10)`, `(11)`, `(12)`, `(13)`, `(14)`, `(15)`, `(16)`, `(19)`, `(20)`, `(25)`, `(26)`.

نام‌ها با فهرست corpus قفل‌شده در `test_codal_pdf_extraction.py:29–50` مطابقت دارند. طبق محدودیت Prompt، محتوای هیچ PDFی باز یا تحلیل نشد. هیچ فایل تغییری نکرد و هیچ تست یا فرمان اجرایی اجرا نشد.

## 2. W-001 — Complete Warning Inventory

خروجی ارائه‌شدهٔ اجرای کامل pytest شامل **153 رخداد `DeprecationWarning`** است. سورس‌های مجاز، 24 محل فراخوانی `datetime.utcnow()` را در این فایل‌ها تأیید می‌کنند. تعداد 153، تعداد دفعات صدور هشدار در اجرای تست‌هاست؛ **تعداد محل‌های کد نیست**.

| فایل و محل | تابع / مسیر قابل‌تأیید | نوع و مصرف timestamp | تست مرتبط و ریسک تغییر |
|---|---|---|---|
| `src/ingestion/codal/ingestion.py:84` | `ingest_codal_pdf`، فقط شاخهٔ شکست استخراج، خطا را در `IngestionRun` ثبت و دوباره پرتاب می‌کند (`:47–88`). | `finished_at` برابر naive UTC؛ در مدل audit و DB ذخیره می‌شود. | `test_codal_extraction.py` مسیر ingestion و خطا را پوشش می‌دهد؛ `test_ingestion_fx.py:169` فقط وجود `finished_at` را بررسی می‌کند. aware کردن مقدار بدون بررسی ستون و خواندن مجدد ORM ممکن است قرارداد ذخیره را عوض کند. |
| `src/tests/test_stage1_rules.py:234` | fixture دادهٔ `IngestionRun` در `test_ingestion_run_contract`. | timestamp تستی naive UTC که در DB درج می‌شود؛ خود این خط هم Warning تولید می‌کند. | تست قرارداد DB مرتبط است؛ تغییر به aware بدون بررسی نوع برگشتی ستون، تست را وارد قرارداد زمانی متفاوتی می‌کند. |
| `src/kpi/universal.py:12,17,22,27,33,38,43,48,53,60,71` | به‌ترتیب `calc_revenue_growth`, `calc_op_profit_growth`, `calc_net_profit_growth`, `calc_eps_growth`, `calc_gross_margin`, `calc_op_margin`, `calc_net_margin`, `calc_roa`, `calc_roe`, `calc_cash_conversion`, `calc_earnings_quality`. | `KPIResult.calculation_timestamp` در خروجی dataclass؛ فایل‌های مجاز نشان نمی‌دهند که این مقدار در DB ذخیره یا از API سریالایز شود. مصرف‌کنندهٔ production بیرون از فهرست مجاز است و اینجا قابل‌تأیید نیست. | `test_stage2_kpis.py` KPIها و نتایجشان را پوشش می‌دهد؛ قرارداد schema فقط `datetime` را اعلام می‌کند و timezone را مشخص نمی‌کند. aware کردن ممکن است مقایسه یا سریال‌سازی مصرف‌کنندهٔ خارج از این محدوده را تغییر دهد. |
| `src/kpi/conditional.py:33` | `calc_financial_cost_pressure`. | `calculation_timestamp` در `KPIResult` برگشتی؛ مصرف DB/API از فایل‌های مجاز اثبات نشد. | `test_stage2_kpis.py` رفتار KPI شرطی را پوشش می‌دهد، اما قرارداد timezone را تثبیت نمی‌کند. |
| `src/kpi/industry.py:12–16,23–25,39` | `calc_bank_kpis` پنج مقدار؛ `calc_holding_kpis` سه مقدار؛ `calc_sales_volume_kpi` یک مقدار. | `calculation_timestamp` در KPIهای خروجی؛ مصرف downstream کامل از فایل‌های مجاز اثبات نشد. | `test_stage2_kpis.py` KPIهای صنعت را پوشش می‌دهد؛ تست timezone مشخصی در فایل‌های بررسی‌شده پیدا نشد. |
| `src/trend/engine.py:235` | `TrendEngine.evaluate_trend` نتیجهٔ `TrendResult` را می‌سازد. | `TrendResult.calculation_timestamp` در خروجی runtime؛ persistence یا API consumer از فایل‌های مجاز اثبات نشد. | `test_stage4_trend.py:816–846` timestamp را از snapshot تحلیلی جدا می‌کند و با ساعت جایگزین، مقدار frozen و **naive** را دقیقاً انتظار دارد؛ این مهم‌ترین شاهد قرارداد فعلی Trend است. |

**جمع‌بندی تطبیق Warning Summary:** مکان‌های گزارش‌شده با سورس مجاز منطبق‌اند؛ محل اضافی `datetime.utcnow()` در این مجموعهٔ فایل‌ها پیدا نشد. شمارش سورس: ingestion یک، تست Stage 1 یک، KPI عمومی یازده، KPI شرطی یک، KPI صنعت نه، Trend یک؛ در مجموع 24 محل. 153 Warning از فراخوانی‌های تکرارشده در تست‌ها می‌آید، نه از 153 خط کد. شمارش اجرای pytest را اجرا نکردم و فقط به خروجی کاربر استناد می‌کنم.

## 3. Timestamp Contract & Compatibility Analysis

در `src/models/audit.py:6–8` تابع `_utc_now_naive()` زمان آگاه UTC را با `datetime.now(timezone.utc).replace(tzinfo=None)` به naive UTC تبدیل می‌کند. ستون‌های `started_at` و `finished_at` در `:16–17` از `DateTime` بدون `timezone=True` استفاده می‌کنند. بنابراین قرارداد موجود DB برای ingestion، **naive UTC** است.

این helper شاهدی از قرارداد DB audit است، نه اثبات اینکه همهٔ لایه‌ها قرارداد یکسان و مستند دارند. در KPI، schema فقط `datetime` می‌گوید (`src/kpi/schema.py:13`)؛ در Trend هم `datetime` است (`src/trend/schema.py:115`). بااین‌حال پیاده‌سازی `utcnow()` و تست ساعت Trend، خروجی naive را نشان می‌دهند. قرارداد زمانی KPI به‌اندازهٔ Trend در تست تثبیت نشده است.

جایگزینی مستقیم با `datetime.now(timezone.utc)`، نوع خروجی را از naive به aware تغییر می‌دهد. این می‌تواند روی مقایسهٔ datetimeهای aware و naive، ذخیره/بازیابی DB و مصرف‌کنندگان یا serialization اثر بگذارد. در محدودهٔ فایل‌های بررسی‌شده، هیچ الزام قراردادی برای aware UTC دیده نشد؛ پس تغییر آگاهانهٔ نوع timestamp توصیه نمی‌شود.

**روش کم‌ریسک پیشنهادی:** حفظ معنای فعلی با `datetime.now(timezone.utc).replace(tzinfo=None)` در محل‌های فراخوانی، یا استفاده از helper مشترکی با همین قرارداد روشن. `_utc_now_naive()` فعلی به‌دلیل جایگاهش در `models.audit` وابسته به لایهٔ مدل است؛ واردکردن آن در KPI یا Trend می‌تواند وابستگی لایه‌ای نامناسب بسازد. helper مشترک در لایهٔ core می‌تواند تمیزتر باشد، اما فایل چنین helperی در فهرست مجاز این ممیزی نیست؛ پیش از افزودن یا بررسی آن باید scope جداگانه تأیید شود.

## 4. W-002 — CODAL PDF Skip Disposition

`_candidate_real_codal_paths()` در `src/tests/test_codal_extraction.py:384–395` فقط این موارد را بررسی می‌کند:

1. مسیر `CODAL_SAMPLE_PDF`، اگر متغیر تنظیم شده باشد؛
2. `/home/workdir/attachments/fzar_403_aban.pdf`؛
3. مسیر پروژه `fixtures/codal/fzar_403_aban.pdf`.

پوشهٔ `pdf/` در هیچ‌یک از این مسیرها نیست. وجود 19 فایل در آن پوشه، به‌تنهایی باعث فعال‌شدن تست `test_real_codal_monthly_activity_pdf` در خط 398 نمی‌شود. فایل‌های پوشه نام‌های عمومی `seo-codal-report (...)` دارند؛ با نام فایل به‌تنهایی نمی‌توان ثابت کرد یکی از آن‌ها نمونهٔ مناسب گزارش فعالیت ماهانهٔ مورد انتظار تست است. من محتوای فایل‌ها را بررسی نکردم.

Skip برای CIای که نمونهٔ واقعی مشخص‌شده را ندارد قابل‌قبول است؛ اما نباید آن را پوشش اجراشدهٔ آن نمونه دانست. یک تست جدا در `test_codal_pdf_extraction.py:25,54–64` پوشهٔ `pdf/` را به‌عنوان corpus 19تایی بررسی می‌کند، ولی این موضوع ثابت نمی‌کند هیچ‌کدام معادل نمونهٔ مشخص تست خط 398 هستند.

اگر کاربر نمونهٔ مناسب را می‌شناسد، می‌تواند مسیرش را در محیط همان اجرای pytest مشخص کند:

```powershell
$env:CODAL_SAMPLE_PDF = (Resolve-Path 'مسیر-نمونه-مناسب.pdf').Path
pytest src/tests/test_codal_extraction.py::test_real_codal_monthly_activity_pdf -q -rs
```

از روی شواهد مجاز، اینکه یکی از 19 PDF برای این تست مناسب است **اثبات نشده**.

## 5. W-003 — openpyxl Skip Disposition

- `openpyxl` در `requirements.txt:3` وجود دارد.
- workflow در `.github/workflows/tests.yml:22–23` فایل requirements را نصب می‌کند؛ پس در CI تعریف‌شده باید نصب باشد.
- تست `test_ingestion_fx.py:193–194` با `pytest.importorskip("openpyxl")`، نبود کتابخانه را به Skip تبدیل می‌کند.
- خروجی واقعی ارائه‌شده علت Skip را `No module named 'openpyxl'` گزارش می‌کند. بنابراین interpreter محیط محلیِ همان اجرای تست به بسته دسترسی نداشته؛ علت دقیق نصب‌نشدن آن در آن محیط از فایل‌های مجاز معلوم نیست.
- چون این وابستگی در requirements عادی آمده و workflow آن را نصب می‌کند، به‌نظر می‌رسد dependency اجباری پروژه باشد، نه optional. `importorskip` در این تست می‌تواند کمبود نصب را پنهان کند؛ برای وابستگی اجباری، شکست روشن تست از Skip مناسب‌تر است.

فرمان پیشنهادی نصب در همان محیط Python که pytest را اجرا می‌کند:

```powershell
python -m pip install -r requirements.txt
```

اگر `pytest` از interpreter دیگری اجرا شود، نصب باید در همان محیط انجام شود؛ اجرای `python -m pytest` پس از نصب کمک می‌کند interpreter یکی باشد.

## 6. W-004 — Safe Remediation Plan

1. **رفع Warningهای تولیدی بدون تغییر قرارداد زمانی:** جایگزینی محل‌های `datetime.utcnow()` با تولید زمان UTC و سپس حذف timezone برای حفظ خروجی naive. `src/models/audit.py` هم‌اکنون این الگو را برای ستون DB اجرا می‌کند.
2. **رفع Warning تست Stage 1:** خط fixture در `test_stage1_rules.py:234` هم باید از `utcnow()` خارج شود؛ در غیر این صورت حتی پس از اصلاح کد تولیدی Warning باقی می‌ماند.
3. **ساعت آزمایشی Trend:** تست freeze در `test_stage4_trend.py:821–846` باید API ساعت جدید را فراهم کند و همچنان خروجی naive را pin کند.
4. **openpyxl:** در مرحلهٔ بعد، تبدیل `importorskip` به import اجباری داخل تست می‌تواند نبود dependency را به خطای روشن تبدیل کند. این تغییر فقط پس از هماهنگی با کاربر برای نصب requirements انجام شود؛ تست ضعیف یا Skip نشود.
5. **CODAL PDF:** Skip را حفظ کنید؛ تست فقط با مسیر نمونهٔ واقعیِ مناسب از طریق `CODAL_SAMPLE_PDF` فعال شود. PDF تصادفی از corpus انتخاب نشود و معیار تست تغییر نکند.
6. Warningها با filter خاموش نشوند؛ فرمول مالی یا رفتار محاسباتی هم تغییری نکند.

## 7. Exact Files to Change in the Next Phase

برای اصلاح Warningها و تثبیت قرارداد naive UTC:

- `src/ingestion/codal/ingestion.py`
- `src/kpi/universal.py`
- `src/kpi/conditional.py`
- `src/kpi/industry.py`
- `src/trend/engine.py`
- `src/tests/test_stage1_rules.py`
- `src/tests/test_stage2_kpis.py`
- `src/tests/test_stage4_trend.py`

برای تبدیل Skip وابستگی اجباری به خطای واضح:

- `src/tests/test_ingestion_fx.py`

`src/models/audit.py` را می‌توان بدون تغییر نگه داشت؛ helper فعلی قرارداد `DateTime` مدل audit را رعایت می‌کند. فایل‌های CODAL PDF نیازی به تغییر ندارند؛ فعال‌سازی نمونه با تنظیم محیطی است. اگر تصمیم به ساخت helper مشترک در `src/core` گرفته شود، مسیر دقیق و فایل‌های وابسته باید جداگانه بررسی و به scope اضافه شوند.

## 8. Required Regression Tests

- **Stage 1 audit timestamp:** تست ثبت/خواندن `IngestionRun` باید پس از ذخیره نشان دهد `started_at` و `finished_at` به شکل naive UTC باقی می‌مانند.
- **CODAL extraction failure:** تست شاخهٔ شکست `ingest_codal_pdf` باید ثبت `FAILED` و `finished_at` naive را همراه با re-raise خطای extraction حفظ کند.
- **KPI timestamps:** تست `KPIResult`های عمومی، شرطی و صنعت، `calculation_timestamp` را naive UTC بررسی کند، بدون تغییر نتایج مالی KPI.
- **Trend timestamp:** تست ساعت کنترل‌شده با API جدید باید timestamp خروجی را همچنان naive و deterministic pin کند؛ snapshot محاسبات روند بدون timestamp همچنان یکسان بماند.
- **openpyxl:** تست XLSX باید واقعاً اجرا شود؛ نبود بسته باید خطای dependency بدهد، نه Skip.
- **CODAL golden sample:** با `CODAL_SAMPLE_PDF` معتبر، تست نمونهٔ واقعی اجرا شود؛ تست corpus 19تایی نیز بدون تغییر باقی بماند.

## 9. Recommended Test Commands

تست‌های هدفمند پس از اصلاح:

```powershell
pytest src/tests/test_stage1_rules.py src/tests/test_stage2_kpis.py src/tests/test_stage4_trend.py src/tests/test_codal_extraction.py src/tests/test_ingestion_fx.py src/tests/test_codal_pdf_extraction.py -q -rs
```

برای فعال‌کردن تست golden PDF، ابتدا `CODAL_SAMPLE_PDF` را به نمونهٔ واقعی مناسب تنظیم کنید و سپس:

```powershell
pytest src/tests/test_codal_extraction.py::test_real_codal_monthly_activity_pdf -q -rs
```

کل مجموعه:

```powershell
pytest src/tests -q -rs
```

همهٔ فرمان‌ها فقط پیشنهاد هستند؛ هیچ‌کدام توسط من اجرا نشدند.

## 10. Unresolved Risks and Dependencies

- علت runtime دو Skip طبق خروجی کاربر معلوم است؛ یکی ناشی از نبود نمونهٔ خاص golden PDF در مسیرهای جست‌وجوشده و دیگری نبود `openpyxl` در interpreter محلی. وجود `pdf/` این دو علت را رفع نمی‌کند.
- مناسب‌بودن هرکدام از 19 PDF برای تست golden CODAL از نام فایل **اثبات نشده**؛ محتوا طبق دستور بررسی نشد.
- مصرف‌کنندگان downstream برای timestampهای KPI/Trend در فایل‌های مجاز حاضر نیستند؛ اثر بر serialization/API بیرون از این scope قابل‌تأیید نیست.
- تبدیل timestampها به aware UTC توصیه نمی‌شود مگر قرارداد schema، DB و مصرف‌کنندگان جداگانه بررسی و تغییر آن تأیید شود.
- helper مشترک UTC در لایهٔ مناسب وجودش در فایل‌های مجاز بررسی نشده؛ ساخت آن نیازمند scope/بررسی جداگانه است.
- تعداد 153 رخداد مطابق خروجی کاربر گزارش شده؛ آزمون برای بازشماری Warningها اجرا نشد.

(analyzer) PS D:\winprojects\analyzer> $env:CODAL_SAMPLE_PDF = "D:\winprojects\analyzer\pdf\Fzar.pdf"
(analyzer) PS D:\winprojects\analyzer> pytest src/tests/test_codal_extraction.py::test_real_codal_monthly_activity_pdf -q -rs
F                                                                                                                [100%]
====================================================== FAILURES =======================================================
________________________________________ test_real_codal_monthly_activity_pdf _________________________________________

    @pytest.mark.skipif(not _candidate_real_codal_paths(), reason="real Codal sample PDF not available in CI")
    def test_real_codal_monthly_activity_pdf():
        """Regression against representative monthly production/sales Codal form."""
        path = _candidate_real_codal_paths()[0]
        result = extract_raw_lines_from_pdf(
            path,
            title="گزارش فعالیت ماهانه تولید و فروش",
            report_type="MONTHLY_ACTIVITY",
            publication_datetime=datetime(2024, 11, 20),
            codal_tracking_id="FZAR-403-ABAN",
        )
        assert result.extraction_backend in {"pdfplumber_tables", "pypdf_text"}
        assert len(result.raw_lines) >= 5
        names = " ".join(r.item_name for r in result.raw_lines)
>       assert any(k in names for k in ("تراورتن", "کانسنگ", "طلا", "فروش", "تن"))
E       assert False
E        +  where False = any(<generator object test_real_codal_monthly_activity_pdf.<locals>.<genexpr> at 0x0000023DD1A7B5E0>)

src\tests\test_codal_extraction.py:412: AssertionError
1 failed in 1.02s

### گزارش شکست تست PDF فزر

- **فایل نمونه درست به تست رسیده** و تست از حالت `skip` خارج شده است.
- استخراج حداقل ۵ ردیف تولید کرده، اما هیچ‌کدام از واژه‌های مورد انتظار مثل «طلا» یا «فروش» در `item_name` نیستند؛ بنابراین تست در خط ۴۱۲ شکست می‌خورد.
- پس ایراد در تشخیص مسیر فایل نیست. احتمالاً متن یا جدول PDF درست استخراج نشده، یا داده‌های استخراج‌شده درست به `item_name` نگاشت نشده‌اند.
- برای تعیین علت دقیق باید زنجیره استخراج و تبدیل داده‌ها بررسی شود. فعلاً بدون آن بررسی نمی‌شود گفت کدام بخش ایراد دارد.