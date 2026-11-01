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

# Task 053-10 — Reconcile Stale OA1.7 Documentation
### 053-10 — تکمیل اصلاح مستنداتی

پاراگراف قدیمی با عنوان **“Unresolved conflict (implementation/documentation)”** در بخش OA1.7 اصلاح شد. آن متن به‌اشتباه می‌گفت تعارض مستنداتی Stage 5 همچنان باز است.

متن جدید می‌گوید قرارداد مستنداتی Stage 5 با OA1.7 هم‌راستاست: Forecastها در زمان اجرا تولید و مصرف می‌شوند و خروجی تحلیلی در جداول DB برنامه ذخیره نمی‌شود. در عین حال، تعارض **اجرایی** مدل‌ها، جدول‌ها، repositoryها، write pathها و migrationها را باز نگه می‌دارد و به Taskهای 054 تا 057 ارجاع می‌دهد.

این متن با `05_Stage5_Forecast_Engine.md` مطابقت دارد و ممنوعیت persistence را حفظ می‌کند. عملیات اصلاح متن انجام شد؛ **053 همچنان PARTIAL می‌ماند** تا بررسی و بستن مستقل طبق پرامپت انجام شود.

فقط فایل [07_Stage7_Valuation.md](/D:/winprojects/analyzer/07_Stage7_Valuation.md) تغییر کرد. فایل دیگری، کد، تست یا تنظیمات تغییر نکرد و هیچ تست یا عملیات Git اجرا نشد.