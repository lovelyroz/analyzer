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

فرمان‌های پیشنهادی برای اجرای محلی:

```powershell
pytest src/tests/test_stage7_valuation.py -q
pytest src/tests/test_stage789_service_interface.py -q
pytest src/tests/test_market_history_query.py -q
pytest src/tests -q
```


(analyzer) PS D:\winprojects\analyzer> pytest src/tests/test_stage7_valuation.py -q
...........................................................................................................      [100%]
107 passed in 0.85s
(analyzer) PS D:\winprojects\analyzer> pytest src/tests/test_stage789_service_interface.py -q
....                                                                                                             [100%]
4 passed in 0.70s
(analyzer) PS D:\winprojects\analyzer> pytest src/tests/test_market_history_query.py -q
.................                                                                                                [100%]
17 passed in 0.75s
(analyzer) PS D:\winprojects\analyzer> pytest src/tests -q
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
..............................................................................................................   [100%]
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
1900 passed, 2 skipped, 153 warnings in 231.60s (0:03:51)