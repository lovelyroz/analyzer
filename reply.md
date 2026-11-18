
database\reports\DB_AUD_006_CODAL_PIPELINE_IMPLEMENTATION_READINESS_AUDIT.md:11:مسیر اجرایی CODAL موجود هنوز مسیر V1 
موردنیاز نیست. کد فعال بررسی‌شده صریحاً PDF-oriented است، در حالی که دامنهٔ V1 مصوب Excel است. Adapter و pipeline فعلی 
PDF را استخراج می‌کنند، خروجی `RawLineInput` می‌سازند و `ingest_codal_report()` آن را به `RawFinancialFact` ذخیره 
می‌کند. این مسیر mapping ساختاری/معنایی نسخه‌دار، ساخت FinancialMetric/approved dimensions، تخصیص مستقل دوره به هر 
fact، canonical INTEGER، provenance نسخهٔ استاندارد و writer متصل به NormalizedFinancialFact را در خود ندارد.
database\reports\DB_AUD_006_CODAL_PIPELINE_IMPLEMENTATION_READINESS_AUDIT.md:21:| CODAL service | 
`src/ingestion/service.py` | `RawLineInput`، `ingest_codal_report`، transaction و replay |
database\reports\DB_AUD_006_CODAL_PIPELINE_IMPLEMENTATION_READINESS_AUDIT.md:41:- `src/tests/test_codal_extraction.py` 
از `load_codal_pdf` و PDFهای fixture استفاده می‌کند.
database\reports\DB_AUD_006_CODAL_PIPELINE_IMPLEMENTATION_READINESS_AUDIT.md:61:در `ingest_codal_report()`:
database\reports\DB_AUD_006_CODAL_PIPELINE_IMPLEMENTATION_READINESS_AUDIT.md:82:- `Report` دارای یک 
`financial_period_id` است، درحالی‌که قرارداد منطقی می‌گوید یک ReportVersion می‌تواند چند دوره و هر FinancialFact دورهٔ 
خودش را داشته باشد.
database\reports\DB_AUD_006_CODAL_PIPELINE_IMPLEMENTATION_READINESS_AUDIT.md:83:- `ingest_codal_report()` یک period_id 
برای کل فایل می‌گیرد و همان را به همهٔ RawFinancialFactها اختصاص می‌دهد.
database\reports\DB_AUD_006_CODAL_PIPELINE_IMPLEMENTATION_READINESS_AUDIT.md:224:### 11.1 CODAL — `ingest_codal_report`
database\reports\DB_AUD_006_CODAL_PIPELINE_IMPLEMENTATION_READINESS_AUDIT.md:267:- 
`src/ingestion/codal/ingestion.py::ingest_codal_report` صرفاً facade سازگاری است و به 
`src/ingestion/service.py::ingest_codal_report` delegate می‌کند؛ transaction مستقل ندارد.
database\reports\DB_AUD_006_CODAL_PIPELINE_IMPLEMENTATION_READINESS_AUDIT.md:268:- 
`src/ingestion/codal/ingestion.py::ingest_codal_pdf` extraction را اجرا می‌کند و سپس به facade بالا می‌رسد. در 
extraction failure، Session را rollback و یک Run جدید FAILED commit می‌کند؛ پیش از extraction یک Run پایدار STARTED 
ایجاد نمی‌کند.
database\reports\DB_AUD_006_CODAL_PIPELINE_IMPLEMENTATION_READINESS_AUDIT.md:269:- 
`src/ingestion/codal/pipeline.py::load_codal_pdf` و `load_codal_pdf_from_url` acquisition، extraction و validation را 
پیش از فراخوانی writer مرکزی اجرا می‌کنند. `_audit_failed_run` در failure یک Run جدید FAILED می‌سازد؛ pipeline پیش از 
acquisition/extraction یک Run پایدار STARTED ایجاد نمی‌کند.
database\reports\DB_AUD_006_CODAL_PIPELINE_IMPLEMENTATION_READINESS_AUDIT.md:270:- 
`src/ingestion/service.py::ingest_codal_report` writer اصلی Report/ReportVersion/RawFinancialFact است. این تابع Run را 
STARTED و flush می‌کند؛ در success همان Run و writes را commit می‌کند. در exception، transaction را rollback و Run 
اولیه را از بین می‌برد، سپس Run جدید FAILED می‌سازد و commit می‌کند.
database\reports\DB_AUD_006_CODAL_PIPELINE_IMPLEMENTATION_READINESS_AUDIT.md:302:**مسیر بعدی پروژه:** ادامهٔ Phase 0 
از DB-PLAN-013 و بستن gateهای طراحی DB-DES-009 است؛ نه تکرار PDF dependency audit، RawFact linkage یا 
Normalized/Derived local linkage. اولین gate اجرایی-مستندی که باید بسته شود، inventory تمام مصرف‌کنندگان 
`reports.financial_period_id` پیش از nullable کردن/جابه‌جایی آن است. سپس gateهای ReportVersion source 
revision/standard binding، dimension scope، company-consistency و provenance granularity به‌ترتیب بررسی می‌شوند.
database\reports\DB_AUD_006_CODAL_PIPELINE_IMPLEMENTATION_READINESS_AUDIT.md:306:## 14. بررسی مصرف‌کنندگان 
`reports.financial_period_id` و مسیرهای فراخوانی CODAL — 2026-11-18
database\reports\DB_AUD_006_CODAL_PIPELINE_IMPLEMENTATION_READINESS_AUDIT.md:309:خروجی جست‌وجوی محلی کاربر برای 
`financial_period_id|FinancialPeriod` در کل فایل‌های `*.py` و `*.sql` زیر repository، موارد زیر را نشان داد:
database\reports\DB_AUD_006_CODAL_PIPELINE_IMPLEMENTATION_READINESS_AUDIT.md:310:- `src/models/report.py`: ستون 
`Report.financial_period_id` با `nullable=False` و FK به `financial_periods.period_id`.
database\reports\DB_AUD_006_CODAL_PIPELINE_IMPLEMENTATION_READINESS_AUDIT.md:312:- `src/forecast/queries.py`: query 
تولیدی Forecast، دوره را از `NormalizedFinancialFact.period_id` به `FinancialPeriod` join می‌کند؛ در این query از 
`Report.financial_period_id` استفاده نشده است.
database\reports\DB_AUD_006_CODAL_PIPELINE_IMPLEMENTATION_READINESS_AUDIT.md:313:- `src/evaluation/*` و بسیاری از 
تست‌های Stage 5/6: نام `financial_period_id` در DTOها و مدل‌های ارزیابی به‌عنوان شناسهٔ دورهٔ observation/forecast 
استفاده شده است؛ این موارد به‌تنهایی مصرف ستون `reports.financial_period_id` نیستند.
database\reports\DB_AUD_006_CODAL_PIPELINE_IMPLEMENTATION_READINESS_AUDIT.md:314:- تست‌های Stage 1 و CODAL، ساخت 
Report و قرارداد قدیمی را با `financial_period_id` اجباری می‌آزمایند؛ تست‌های PDF نیز رابطهٔ Report با FinancialPeriod 
را assert می‌کنند.
database\reports\DB_AUD_006_CODAL_PIPELINE_IMPLEMENTATION_READINESS_AUDIT.md:318:- `src/ingestion/codal/ingestion.py`: 
تابع عمومی `ingest_codal_report` یک facade سازگار با گذشته است و به `src.ingestion.service.ingest_codal_report` 
delegate می‌کند. تابع `ingest_codal_pdf` پس از extraction همین facade را فراخوانی می‌کند.
database\reports\DB_AUD_006_CODAL_PIPELINE_IMPLEMENTATION_READINESS_AUDIT.md:319:- `src/ingestion/codal/pipeline.py`: 
توابع `load_codal_pdf` و `load_codal_pdf_from_url` پس از acquisition/extraction/validation، writer مرکزی 
`src.ingestion.service.ingest_codal_report` را فراخوانی می‌کنند.
database\reports\DB_AUD_006_CODAL_PIPELINE_IMPLEMENTATION_READINESS_AUDIT.md:320:- `src/ingestion/excel/reader.py` و 
`src/ingestion/excel/dto.py`: در نسخهٔ بررسی‌شده، reader/DTO اکسل هیچ فراخوانی writer CODAL و هیچ ارجاعی به 
`financial_period_id` ندارند؛ این با یافتهٔ قبلی DB-AUD-013 مبنی بر نبود production Excel-to-canonical persistence 
هم‌راستا است.
database\reports\DB_AUD_006_CODAL_PIPELINE_IMPLEMENTATION_READINESS_AUDIT.md:326:1. `Report.financial_period_id` در 
حال حاضر یک فیلد الزامی و بخشی از قرارداد writer قدیمی CODAL است؛ حذف یا nullable کردن آن بدون جایگزینی قرارداد legacy 
باعث شکستن مسیر موجود و تست‌های مربوط می‌شود.
database\reports\DB_AUD_006_CODAL_PIPELINE_IMPLEMENTATION_READINESS_AUDIT.md:329:4. بنابراین مسیر جدید Excel باید 
writer/contract مستقل یا نسخهٔ توسعه‌یافته‌ای داشته باشد که برای هر Fact دورهٔ خودش را دریافت و اعتبارسنجی کند. 
`Report.financial_period_id` تا زمان تعیین تکلیف و بازنشستگی کنترل‌شدهٔ مسیر legacy باید حفظ شود؛ اگر در مدل نهایی 
باقی بماند، نقش آن باید صرفاً metadata دورهٔ اصلی/نمایشی گزارش باشد و نباید مرجع دورهٔ مقادیر تلقی شود.
database\reports\DB_AUD_006_CODAL_PIPELINE_IMPLEMENTATION_READINESS_AUDIT.md:335:## 14. تکمیل بررسی 
Report.financial_period_id و مرز writer قدیمی — 2026-11-18
database\reports\DB_AUD_006_CODAL_PIPELINE_IMPLEMENTATION_READINESS_AUDIT.md:340:- تنها writer مرکزی CODAL که در این 
مسیر مشاهده شد `src/ingestion/service.py::ingest_codal_report` است؛ facade در `codal/ingestion.py` به همین تابع 
delegate می‌کند و pipeline نیز همین writer را صدا می‌زند.
database\reports\DB_AUD_006_CODAL_PIPELINE_IMPLEMENTATION_READINESS_AUDIT.md:342:- برای Report موجود، company_id و 
`Report.financial_period_id` با ورودی مقایسه می‌شوند؛ اختلاف باعث رد عملیات می‌شود.
database\reports\DB_AUD_006_CODAL_PIPELINE_IMPLEMENTATION_READINESS_AUDIT.md:343:- برای Report جدید، 
`financial_period_id=period_id` ثبت می‌شود.
database\reports\DB_AUD_006_CODAL_PIPELINE_IMPLEMENTATION_READINESS_AUDIT.md:353:4. نقش نهایی 
Report.financial_period_id (حذف تدریجی، nullable و descriptive، یا جایگزینی با primary-period metadata) پس از 
inventory کامل call-siteها و physical design تعیین می‌شود.
database\reports\DB_AUD_009_ORM_MIGRATION_TEMPLATE_COMPATIBILITY_AUDIT.md:22:| `Report` / `reports` | Integer PK; FK 
`company_id`; free-text `report_type`; FK `financial_period_id` | Reuse, but report-type normalization is a 
prerequisite for the proposed `report_type_id` |
database\reports\DB_AUD_009_ORM_MIGRATION_TEMPLATE_COMPATIBILITY_AUDIT.md:24:| `FinancialPeriod` / `financial_periods` 
| Integer PK; FK `company_id`; period type and date/fiscal attributes | Reuse for reporting-period semantics; do not 
duplicate period fields in Template metadata |
database\reports\DB_AUD_011_LEGACY_RAW_FACT_PROVENANCE_DECISION.md:92:- `ingest_codal_report(...)` creates one 
`RawFinancialFact` object for each `RawLineInput` and calls `session.add_all(facts)`.
database\reports\DB_AUD_012_CODAL_PDF_PATH_DEPENDENCY_AUDIT.md:17:load_codal_pdf / load_codal_pdf_from_url  
database\reports\DB_AUD_012_CODAL_PDF_PATH_DEPENDENCY_AUDIT.md:21:→ ingest_codal_report  
database\reports\DB_AUD_012_CODAL_PDF_PATH_DEPENDENCY_AUDIT.md:35:| src/ingestion/codal/ingestion.py | facade شامل 
ingest_codal_pdf و facade سازگاری ingest_codal_report | بخش PDF-only + facade legacy |
database\reports\DB_AUD_012_CODAL_PDF_PATH_DEPENDENCY_AUDIT.md:36:| src/ingestion/service.py::ingest_codal_report | 
ساخت Report/ReportVersion و درج یک RawFinancialFact برای هر RawLineInput | persistence قدیمی CODAL؛ در فایل مشترک با 
FX و Market قرار دارد |
database\reports\DB_AUD_012_CODAL_PDF_PATH_DEPENDENCY_AUDIT.md:125:- `service.py::ingest_codal_report`: persistence 
قدیمی RawFinancialFact را انجام می‌دهد؛ با این حال همان فایل توابع مستقل FX/OHLC دارد و نباید حذف شود.
database\reports\DB_AUD_013_EXCEL_CANONICAL_PERSISTENCE_READINESS.md:45:- financial_period_id به‌عنوان primary report 
period
database\reports\DB_AUD_013_EXCEL_CANONICAL_PERSISTENCE_READINESS.md:53:- financial_period_id در مدل فعلی روی Report 
اجباری است، در حالی که قرارداد هدف می‌گوید یک ReportVersion می‌تواند چند FinancialPeriod داشته باشد و هر fact دوره 
واقعی خودش را تعیین کند؛ report-level period نباید دوره همه facts را تحمیل کند.
database\reports\DB_AUD_014_NORMALIZED_DERIVED_FACT_CONSUMER_AUDIT.md:49:The current CODAL path in 
`src/ingestion/service.py::ingest_codal_report`:
database\reports\DB_AUD_014_NORMALIZED_DERIVED_FACT_CONSUMER_AUDIT.md:103:    -> ingest_codal_report
database\reports\DB_DES_009_CANONICAL_FINANCIAL_FACT_PHYSICAL_MODEL.md:43:3. `financial_periods` — redesigned for 
authoritative Jalali dates and INSTANT/DURATION semantics.
database\reports\DB_DES_009_CANONICAL_FINANCIAL_FACT_PHYSICAL_MODEL.md:83:The report-level period is descriptive 
metadata only. A ReportVersion can publish facts for several actual periods, and every fact links to its own 
FinancialPeriod. The current NOT NULL `reports.financial_period_id` must not be allowed to impose one period on every 
fact.
database\reports\DB_DES_009_CANONICAL_FINANCIAL_FACT_PHYSICAL_MODEL.md:93:The new/updated `financial_periods` model 
must use Jalali components as authoritative values; no Gregorian conversion is required or permitted as a substitute.
database\reports\DB_DES_009_CANONICAL_FINANCIAL_FACT_PHYSICAL_MODEL.md:300:5. **Report primary period:** inspect 
consumers before making current `reports.financial_period_id` nullable or moving it.
database\reports\DB_DES_009_CANONICAL_FINANCIAL_FACT_PHYSICAL_MODEL.md:342:- `Report` نیز `company_id` و 
`financial_period_id` را جداگانه نگه می‌دارد؛ FKها به‌تنهایی تضمین نمی‌کنند که دورهٔ گزارش متعلق به همان شرکت باشد.
database\reports\DB_DES_009_CANONICAL_FINANCIAL_FACT_PHYSICAL_MODEL.md:359:3. پس از ایجاد Fact، تغییر هویت رابطه‌ای 
والدها نباید invariant را بی‌صدا خراب کند. سیاست پیشنهادی این است که تغییر `reports.company_id`، 
`report_versions.report_id` یا `financial_periods.company_id` تا وقتی Fact وابسته وجود دارد ممنوع باشد؛ اصلاح هویت با 
ساخت رکورد صحیح و مسیر اصلاح کنترل‌شده انجام شود، نه reassignment خام.
database\reports\DB_DES_009_CANONICAL_FINANCIAL_FACT_PHYSICAL_MODEL.md:360:4. اگر `Report.financial_period_id` در مدل 
نهایی به‌صورت optional metadata باقی بماند، trigger جداگانه باید در صورت non-NULL بودن، تطابق شرکت Report و 
FinancialPeriod را enforce کند؛ NULL بودن این metadata نباید مانع ثبت Fact دارای period_id مستقل شود.
database\reports\DB_PLAN_013_PDF_PATH_RETIREMENT_SEQUENCE.md:29:| \`src/ingestion/codal/pipeline.py\` | حذف 
pipelineهای load_codal_pdf و load_codal_pdf_from_url |
database\reports\DB_PLAN_013_PDF_PATH_RETIREMENT_SEQUENCE.md:41:| \`src/ingestion/service.py::ingest_codal_report\` | 
API قدیمی ایجاد Report/ReportVersion و ذخیره RawFinancialFact؛ هنوز جداسازی metadata persistence از raw persistence 
انجام نشده |
database\reports\DB_PLAN_013_PDF_PATH_RETIREMENT_SEQUENCE.md:42:| \`src/ingestion/codal/ingestion.py\` | facade قدیمی؛ 
پس از شناسایی callerها باید فقط facade PDF حذف و وضعیت ingest_codal_report جداگانه تعیین شود |
database\reports\DB_PLAN_013_PDF_PATH_RETIREMENT_SEQUENCE.md:45:| \`src/ingestion/__init__.py\` | exportهای قدیمی 
RawLineInput و ingest_codal_report فعلاً حفظ؛ بعداً با API جدید جایگزین یا صریحاً بازنشسته شوند |
database\reports\DB_PLAN_013_PDF_PATH_RETIREMENT_SEQUENCE.md:72:1. تابع فعلی \`ingest_codal_report\` را به دو مسئولیت 
تفکیک طراحی کن: ایجاد/انتخاب Report و ReportVersion، و ذخیره RawLineInput به RawFinancialFact.
database\reports\DB_STD_005_AND_DB_AUD_001_MARKET_FX_EVIDENCE_REVIEW.md:288:| `service.py::ingest_codal_report` | 
STARTED با flush؛ ساخت Report/ReportVersion/Facts؛ COMPL​ETED و canonical writes با یک commit؛ در exception rollback و 
سپس FAILED در commit جداگانه | الگوی کلی به atomicity نزدیک است؛ اما Run شروع‌شده در rollback از بین می‌رود و به‌جای 
update همان Run، رکورد FAILED جدید ساخته می‌شود. مسیر idempotent موجود بر اساس tracking ID و publication datetime، 
payload را مقایسه نمی‌کند و در صورت یافتن نسخه، شمارنده را در `records_updated` ثبت می‌کند |
database\reports\DB_STD_005_AND_DB_AUD_001_MARKET_FX_EVIDENCE_REVIEW.md:291:| `codal/ingestion.py::ingest_codal_pdf` و 
`codal/pipeline.py` | در خطای acquisition/extraction/validation، rollback و سپس درج FAILED و commit؛ مسیر PDF legacy 
است | audit شکست مستقل است، اما مسیر جاری V1 نیست و نباید مبنای قرارداد Excel تلقی شود |
database\reports\DB_STD_005_AND_DB_AUD_001_MARKET_FX_EVIDENCE_REVIEW.md:458:2. مسیر CODAL در 
`ingestion/service.py::ingest_codal_report` (تابع persistence گزارش CODAL) یک `ReportVersion` و مجموعه‌ای از 
`RawFinancialFact` ایجاد می‌کند. در همین تابع، ایجاد `MappingDecision`، ساخت `NormalizedFinancialFact` یا ایجاد 
bridgeهای `NormalizedFinancialFactInput` مشاهده نشد.
database\reports\DB_STD_005_AND_DB_AUD_001_MARKET_FX_EVIDENCE_REVIEW.md:481:| CODAL فقط Raw می‌نویسد | 
`ingest_codal_report` و Stage 5 query | Stage 5 مصرف‌کنندهٔ مستقیم خروجی CODAL نیست | طراحی/پیاده‌سازی pipeline 
استخراج، mapping و canonical validation مطابق DB-DES-001/002 |
database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:333:- `src/ingestion/service.py`: ورودی `ingest_codal_report` 
یک `period_id` برای کل گزارش می‌گیرد و همان را به همهٔ `RawFinancialFact`ها نسبت می‌دهد. `RawLineInput` فعلی اطلاعات 
دورهٔ مستقل برای هر مقدار/سلول ندارد.
database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:339:رابطهٔ فعلی Report و FinancialPeriod هنوز تعیین تکلیف 
نشده است: گزارش منطقی ممکن است در یک انتشار چند ستون زمانی داشته باشد، در حالی که سرویس فعلی یک `financial_period_id` 
را به کل Report و همهٔ ردیف‌های آن متصل می‌کند. پیش از تغییر مدل یا DTO باید تصمیم گرفته شود که هر مقدار canonical 
چگونه به دورهٔ واقعی خودش وصل می‌شود و نقش احتمالی دورهٔ اصلی گزارش چیست.
database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:351:| Period | `FinancialPeriod` | `financial_periods` |
database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:396:2. `Report.financial_period_id` اجباری است و 
`ingest_codal_report` یک period_id واحد را به تمام RawFinancialFactهای یک report version اختصاص می‌دهد.
database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:417:| `reports`, `report_versions`, `raw_financial_facts` | 
`src/ingestion/service.py::ingest_codal_report`؛ facadeها در `src/ingestion/codal/ingestion.py` و `pipeline.py` | در 
این مرحله، queryهای انتخاب نسخه و تمام مصرف‌کنندگان downstream هنوز فهرست نشده‌اند | یک `period_id` به Report و همهٔ 
raw lineها داده می‌شود؛ برای گزارش چنددوره‌ای ناکافی است. نسخهٔ جدید، current قبلی را غیرفعال و 
`supersedes_version_id` را به آخرین نسخه وصل می‌کند. |
database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:422:| `financial_periods` | در مسیر CODAL، period از قبل 
موجود فرض و با `session.get` خوانده می‌شود؛ writer مستقل در مسیرهای بررسی‌شده پیدا نشد | `src/ingestion/service.py` 
برای اعتبارسنجی وجود period و تطبیق company | منشأ ایجاد/مدیریت دوره هنوز باید در جست‌وجوی کامل call siteها مشخص شود. |
database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:460:5. ساختار فعلی `Report.financial_period_id` و 
`RawFinancialFact.period_id` همچنان هر گزارش/ردیف را به یک period محدود می‌کند؛ DTO و ingestion هیچ دورهٔ مستقل برای 
هر ستون/مقدار ارائه نمی‌کنند. برای گزارش چندستونه باید تخصیص period در سطح هر مقدار canonical تعریف شود؛ اینکه Report 
یک دورهٔ اصلی اختیاری/نمایشی داشته باشد یا رابطهٔ جداگانهٔ Report–Period لازم باشد، هنوز تصمیم طراحی نهایی می‌خواهد.
database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:476:3. `RawLineInput` در `src/ingestion/service.py` نیز همین 
محدودیت را دارد. متد `ingest_codal_report` یک `period_id` می‌گیرد و همان مقدار را برای همهٔ RawFinancialFactها ذخیره 
می‌کند.
database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:477:4. `Report.financial_period_id` هم اجباری است؛ بنابراین 
حتی مدل Report هم در حال حاضر فقط یک دورهٔ اصلی را نمایش می‌دهد. ReportVersion رابطهٔ دوره‌ای مستقل ندارد.
database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:496:**گزینهٔ معماری برای مرحلهٔ طراحی (پیشنهاد، نه تصمیم 
مصوب):** یک association در سطح ReportVersion برای دوره‌های پوشش‌داده‌شده، با حفظ source-column/header locator، و اتصال 
هر canonical input به period مشخص خودش. این طرح از نسبت‌دادن یک period واحد به کل Report جلوگیری می‌کند؛ اما شکل دقیق 
association، الزامی/اختیاری بودن `Report.financial_period_id` قدیمی و نگاشت نسخه‌های اصلاحی باید در Task 008 و Task 
006 نهایی شود. در این مرحله هیچ schema یا migration تغییر نمی‌کند.
database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1085:بررسی source code فعلی GitHub نشان داد 
`src/ingestion/service.py::ingest_codal_report` مستقیماً برای هر `RawLineInput` یک `RawFinancialFact` می‌سازد و با 
`session.add_all` در `raw_financial_facts` ذخیره می‌کند. این مسیر از `src/ingestion/codal/adapter.py` تغذیه می‌شود که 
صراحتاً مرز استخراج PDF است. بنابراین مسیر CODAL فعلی legacy/PDF-oriented است؛ وجود مسیر production مستقل 
Excel-to-canonical در این بررسی اثبات نشد. Runner نیز در source فعلی تا Migration 8 پیش می‌رود.
database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1112:بازبینی source فعلی نیز نشان می‌دهد مسیر 
`src/ingestion/codal/ingestion.py` و `src/ingestion/codal/pipeline.py` همچنان PDF را استخراج می‌کنند و در نهایت به 
`src/ingestion/service.py::ingest_codal_report` می‌رسند؛ این تابع برای هر RawLineInput یک RawFinancialFact می‌سازد و 
ذخیره می‌کند. در مقابل، `src/ingestion/excel` فعلاً DTO و Reader دارد و مسیر production مستقل Excel-to-canonical 
persistence در کد بررسی‌شده اثبات نشده است.
database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1131:بررسی source در branch فعلی زنجیره PDF را مشخص کرد: 
pipeline محلی/URL → acquisition → adapter و PDF extract → RawLineInput → persistence قدیمی در 
`service.py::ingest_codal_report` → RawFinancialFact.
database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1682:- `codal/ingestion.py::ingest_codal_report` فقط facade 
است و به writer مرکزی `service.py::ingest_codal_report` می‌رسد.
database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1683:- `codal/ingestion.py::ingest_codal_pdf` extraction و 
سپس persistence را انجام می‌دهد؛ extraction failure با Run جدید FAILED ثبت می‌شود و STARTED پایدار پیش از extraction 
ندارد.
database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1684:- `codal/pipeline.py::load_codal_pdf` و 
`load_codal_pdf_from_url` acquisition/extraction/validation را پیش از writer اجرا می‌کنند؛ failureهای این مراحل Run 
جدید FAILED ثبت می‌کنند، نه ادامهٔ یک STARTED پایدار.
database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1706:**قدم بعدی:** ادامهٔ Phase 0 از DB-PLAN-013 و بستن 
gateهای طراحی DB-DES-009. اولین مورد: inventory تمام مصرف‌کنندگان `reports.financial_period_id`، چون پیش از nullable 
کردن یا انتقال این فیلد باید تمام readerها/writerها مشخص شوند. پس از آن gateهای source revision و ReportVersion 
standard binding، dimension scope، company consistency و provenance granularity بررسی می‌شوند.
database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1710:### 8.73 بررسی مصرف‌کنندگان 
`reports.financial_period_id` و تفکیک قرارداد legacy CODAL از Excel — 2026-11-18
database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1714:- ستون `Report.financial_period_id` در ORM اجباری است 
(`nullable=False`) و writer قدیمی CODAL آن را مقداردهی و در replay identity validation می‌کند.
database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1715:- facade در `codal/ingestion.py` به writer مرکزی 
`service.py::ingest_codal_report` delegate می‌کند؛ PDF wrapper پس از extraction از آن استفاده می‌کند. مسیرهای 
`codal/pipeline.py` نیز پس از acquisition/extraction/validation مستقیماً writer مرکزی را فراخوانی می‌کنند.
database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1718:- نام `financial_period_id` در evaluation/forecast 
observation DTOها و تست‌های Stage 5/6 لزوماً به ستون `reports.financial_period_id` اشاره ندارد؛ این دو مفهوم باید در 
تحلیل وابستگی از هم جدا بمانند.
database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1721:**تصمیم طراحی موقت این gate:** مسیر legacy CODAL تا زمان 
retirement/migration کنترل‌شده به قرارداد فعلی نیاز دارد؛ بنابراین nullable کردن یا حذف فوری 
`Report.financial_period_id` مجاز نیست. مسیر جدید Excel باید دوره را در سطح هر Fact تعیین کند و نباید یک دورهٔ واحد را 
به تمام facts یک ReportVersion تحمیل کند. اگر فیلد Report در مدل نهایی باقی بماند، فقط metadata دورهٔ اصلی/نمایشی 
گزارش است و مرجع authoritative دورهٔ هر مقدار نیست.
database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1739:**توصیهٔ معماری:** برای `financial_facts` جدید، 
company_id را تکرار نکنیم. تطابق شرکت را با SQLite BEFORE INSERT و BEFORE UPDATE trigger روی Fact، به‌علاوه service 
validation enforce کنیم. برای جلوگیری از خراب شدن invariant پس از ثبت Fact، تغییر `reports.company_id`، 
`report_versions.report_id` و `financial_periods.company_id` تا وقتی Fact وابسته وجود دارد باید ممنوع باشد. اگر 
`Report.financial_period_id` به‌صورت optional metadata باقی ماند، در صورت non-NULL بودن تطابق شرکت آن نیز کنترل شود.
database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1876:### 8.84 بررسی اولیهٔ Gate 5 از DB-DES-009 — وابستگی 
writer قدیمی به Report.financial_period_id — 2026-11-18
database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1880:- `service.py::ingest_codal_report` writer مرکزی CODAL 
مشاهده‌شده است.
database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1883:- برای Report موجود، company_id و 
`Report.financial_period_id` باید با ورودی یکسان باشند؛ در غیر این صورت عملیات رد می‌شود.
prompts\10_Implementation_Status.md:81:| Format-agnostic core persistence | PASS | `ingest_fx_rates` / 
`ingest_codal_report` take DTOs |
prompts\10_Implementation_Status.md:83:| CODAL extraction outside core write | PASS | `ingest_codal_report` accepts 
`RawLineInput[]` only |
prompts\10_Implementation_Status.md:243:ingest_codal_report()
src\tests\final_validation_audit.md:140:  → ingest_codal_report()
src\tests\golden_audit_source_plan.md:15:ingest_codal_report()
src\tests\golden_audit_source_plan.md:115:- Report / ReportVersion / RawFinancialFact created by ingest_codal_report()
01_Stage1_Data_Foundation.md:278:financial_period_id
06_Stage6_Forecast_Evaluation.md:1112:**Owner-approved pointer (Prompt 34 — scenario persistence evidence, additive 
clarification only, 2026-10-09):** audit evidence — no evaluation-results persistence table exists in `src/models/*` 
(models cover industries/companies, financial_periods, reports/report_versions, raw 
facts/metrics/mapping/normalized/derived, fx, market_daily, share actions, forecast_versions/forecast_input_refs); 
`forecast_versions` persists scenario with a BEAR/BASE/BULL check constraint; evaluation verdicts are in-memory only; 
`EvaluationKey` carries scenario (default BASE) while aggregation is scenario-free by design (code-level gap recorded 
for the future implementation prompt, not changed here). Migration necessity is therefore NOT APPLICABLE/UNDETERMINED 
as framed — there is no evaluation persistence table to migrate; when evaluation persistence is built, scenario 
identity must be part of its contract per policy D3, with no cross-scenario pooling.
10_Production_Codal_Extraction_and_Data_Load.md:22:ingest_codal_report()
10_Production_Codal_Extraction_and_Data_Load.md:113:`extract → validate → RawLineInput[] → ingest_codal_report()`
11_Production_Data_Load_and_Foundation_Validation.md:136:ingest_codal_report()
12_Database_Architecture_V1.1.md:104:- `financial_periods`
12_Database_Architecture_V1.1.md:801:ingest_codal_report / ingest_ohlc_* / ingest_fx_rates
12_Database_Architecture_V1.1.md:810:- The Excel adapter must emit the same common financial input DTO contract 
consumed by `ingest_codal_report`; the existing downstream persistence boundary must remain format-independent.
99_Architecture_Change_Log.md:386:  ingest_codal_report / ingest_ohlc_* / ingest_fx_rates
99_Architecture_Change_Log.md:397:   Codal financial statements arrive as PDFs. Extraction (table/text/OCR as needed) 
is a **pre-ingestion** responsibility. `ingest_codal_report` receives already-extracted `RawLineInput` lines plus 
report metadata (tracking id, URL, publication datetime, version). The PDF itself may be referenced via `source_url` / 
tracking fields; the binary is not required inside the DB contract for V1.
PROJECT_HANDOFF_INSTRUCTIONS.md:252:    ingest_codal_report()
reply.md:4:PDF را استخراج می‌کنند، خروجی `RawLineInput` می‌سازند و `ingest_codal_report()` آن را به `RawFinancialFact` 
ذخیره 
reply.md:8:`src/ingestion/service.py` | `RawLineInput`، `ingest_codal_report`، transaction و replay |
reply.md:10:از `load_codal_pdf` و PDFهای fixture استفاده می‌کند.
reply.md:11:database\reports\DB_AUD_006_CODAL_PIPELINE_IMPLEMENTATION_READINESS_AUDIT.md:61:در `ingest_codal_report()`:
reply.md:13:`financial_period_id` است، درحالی‌که قرارداد منطقی می‌گوید یک ReportVersion می‌تواند چند دوره و هر 
FinancialFact دورهٔ 
reply.md:15:database\reports\DB_AUD_006_CODAL_PIPELINE_IMPLEMENTATION_READINESS_AUDIT.md:83:- `ingest_codal_report()` 
یک period_id 
reply.md:17:database\reports\DB_AUD_006_CODAL_PIPELINE_IMPLEMENTATION_READINESS_AUDIT.md:224:### 11.1 CODAL — 
`ingest_codal_report`
reply.md:19:`src/ingestion/codal/ingestion.py::ingest_codal_report` صرفاً facade سازگاری است و به 
reply.md:20:`src/ingestion/service.py::ingest_codal_report` delegate می‌کند؛ transaction مستقل ندارد.
reply.md:22:`src/ingestion/codal/ingestion.py::ingest_codal_pdf` extraction را اجرا می‌کند و سپس به facade بالا 
می‌رسد. در 
reply.md:26:`src/ingestion/codal/pipeline.py::load_codal_pdf` و `load_codal_pdf_from_url` acquisition، extraction و 
validation را 
reply.md:30:`src/ingestion/service.py::ingest_codal_report` writer اصلی Report/ReportVersion/RawFinancialFact است. این 
تابع Run را 
reply.md:36:`reports.financial_period_id` پیش از nullable کردن/جابه‌جایی آن است. سپس gateهای ReportVersion source 
reply.md:39:`reports.financial_period_id` و مسیرهای فراخوانی CODAL — 2026-11-18
reply.md:41:`financial_period_id|FinancialPeriod` در کل فایل‌های `*.py` و `*.sql` زیر repository، موارد زیر را نشان 
داد:
reply.md:43:`Report.financial_period_id` با `nullable=False` و FK به `financial_periods.period_id`.
reply.md:46:`Report.financial_period_id` استفاده نشده است.
reply.md:48:تست‌های Stage 5/6: نام `financial_period_id` در DTOها و مدل‌های ارزیابی به‌عنوان شناسهٔ دورهٔ 
observation/forecast 
reply.md:49:استفاده شده است؛ این موارد به‌تنهایی مصرف ستون `reports.financial_period_id` نیستند.
reply.md:51:Report و قرارداد قدیمی را با `financial_period_id` اجباری می‌آزمایند؛ تست‌های PDF نیز رابطهٔ Report با 
FinancialPeriod 
reply.md:54:تابع عمومی `ingest_codal_report` یک facade سازگار با گذشته است و به 
`src.ingestion.service.ingest_codal_report` 
reply.md:55:delegate می‌کند. تابع `ingest_codal_pdf` پس از extraction همین facade را فراخوانی می‌کند.
reply.md:57:توابع `load_codal_pdf` و `load_codal_pdf_from_url` پس از acquisition/extraction/validation، writer مرکزی 
reply.md:58:`src.ingestion.service.ingest_codal_report` را فراخوانی می‌کنند.
reply.md:61:`financial_period_id` ندارند؛ این با یافتهٔ قبلی DB-AUD-013 مبنی بر نبود production Excel-to-canonical 
persistence 
reply.md:63:database\reports\DB_AUD_006_CODAL_PIPELINE_IMPLEMENTATION_READINESS_AUDIT.md:326:1. 
`Report.financial_period_id` در 
reply.md:68:`Report.financial_period_id` تا زمان تعیین تکلیف و بازنشستگی کنترل‌شدهٔ مسیر legacy باید حفظ شود؛ اگر در 
مدل نهایی 
reply.md:71:Report.financial_period_id و مرز writer قدیمی — 2026-11-18
reply.md:73:مسیر مشاهده شد `src/ingestion/service.py::ingest_codal_report` است؛ facade در `codal/ingestion.py` به همین 
تابع 
reply.md:76:`Report.financial_period_id` با ورودی مقایسه می‌شوند؛ اختلاف باعث رد عملیات می‌شود.
reply.md:78:`financial_period_id=period_id` ثبت می‌شود.
reply.md:80:Report.financial_period_id (حذف تدریجی، nullable و descriptive، یا جایگزینی با primary-period metadata) پس 
از 
reply.md:83:`company_id`; free-text `report_type`; FK `financial_period_id` | Reuse, but report-type normalization is 
a 
reply.md:85:database\reports\DB_AUD_009_ORM_MIGRATION_TEMPLATE_COMPATIBILITY_AUDIT.md:24:| `FinancialPeriod` / 
`financial_periods` 
reply.md:88:database\reports\DB_AUD_011_LEGACY_RAW_FACT_PROVENANCE_DECISION.md:92:- `ingest_codal_report(...)` creates 
one 
reply.md:90:database\reports\DB_AUD_012_CODAL_PDF_PATH_DEPENDENCY_AUDIT.md:17:load_codal_pdf / load_codal_pdf_from_url 
 
reply.md:91:database\reports\DB_AUD_012_CODAL_PDF_PATH_DEPENDENCY_AUDIT.md:21:→ ingest_codal_report  
reply.md:93:ingest_codal_pdf و facade سازگاری ingest_codal_report | بخش PDF-only + facade legacy |
reply.md:94:database\reports\DB_AUD_012_CODAL_PDF_PATH_DEPENDENCY_AUDIT.md:36:| 
src/ingestion/service.py::ingest_codal_report | 
reply.md:97:database\reports\DB_AUD_012_CODAL_PDF_PATH_DEPENDENCY_AUDIT.md:125:- `service.py::ingest_codal_report`: 
persistence 
reply.md:99:database\reports\DB_AUD_013_EXCEL_CANONICAL_PERSISTENCE_READINESS.md:45:- financial_period_id به‌عنوان 
primary report 
reply.md:101:database\reports\DB_AUD_013_EXCEL_CANONICAL_PERSISTENCE_READINESS.md:53:- financial_period_id در مدل فعلی 
روی Report 
reply.md:105:`src/ingestion/service.py::ingest_codal_report`:
reply.md:106:database\reports\DB_AUD_014_NORMALIZED_DERIVED_FACT_CONSUMER_AUDIT.md:103:    -> ingest_codal_report
reply.md:107:database\reports\DB_DES_009_CANONICAL_FINANCIAL_FACT_PHYSICAL_MODEL.md:43:3. `financial_periods` — 
redesigned for 
reply.md:111:FinancialPeriod. The current NOT NULL `reports.financial_period_id` must not be allowed to impose one 
period on every 
reply.md:113:database\reports\DB_DES_009_CANONICAL_FINANCIAL_FACT_PHYSICAL_MODEL.md:93:The new/updated 
`financial_periods` model 
reply.md:116:consumers before making current `reports.financial_period_id` nullable or moving it.
reply.md:118:`financial_period_id` را جداگانه نگه می‌دارد؛ FKها به‌تنهایی تضمین نمی‌کنند که دورهٔ گزارش متعلق به همان 
شرکت باشد.
reply.md:121:`report_versions.report_id` یا `financial_periods.company_id` تا وقتی Fact وابسته وجود دارد ممنوع باشد؛ 
اصلاح هویت با 
reply.md:123:database\reports\DB_DES_009_CANONICAL_FINANCIAL_FACT_PHYSICAL_MODEL.md:360:4. اگر 
`Report.financial_period_id` در مدل 
reply.md:127:pipelineهای load_codal_pdf و load_codal_pdf_from_url |
reply.md:128:database\reports\DB_PLAN_013_PDF_PATH_RETIREMENT_SEQUENCE.md:41:| 
\`src/ingestion/service.py::ingest_codal_report\` | 
reply.md:132:پس از شناسایی callerها باید فقط facade PDF حذف و وضعیت ingest_codal_report جداگانه تعیین شود |
reply.md:134:RawLineInput و ingest_codal_report فعلاً حفظ؛ بعداً با API جدید جایگزین یا صریحاً بازنشسته شوند |
reply.md:135:database\reports\DB_PLAN_013_PDF_PATH_RETIREMENT_SEQUENCE.md:72:1. تابع فعلی \`ingest_codal_report\` را 
به دو مسئولیت 
reply.md:137:database\reports\DB_STD_005_AND_DB_AUD_001_MARKET_FX_EVIDENCE_REVIEW.md:288:| 
`service.py::ingest_codal_report` | 
reply.md:142:database\reports\DB_STD_005_AND_DB_AUD_001_MARKET_FX_EVIDENCE_REVIEW.md:291:| 
`codal/ingestion.py::ingest_codal_pdf` و 
reply.md:146:`ingestion/service.py::ingest_codal_report` (تابع persistence گزارش CODAL) یک `ReportVersion` و مجموعه‌ای 
از 
reply.md:150:`ingest_codal_report` و Stage 5 query | Stage 5 مصرف‌کنندهٔ مستقیم خروجی CODAL نیست | طراحی/پیاده‌سازی 
pipeline 
reply.md:152:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:333:- `src/ingestion/service.py`: ورودی 
`ingest_codal_report` 
reply.md:156:نشده است: گزارش منطقی ممکن است در یک انتشار چند ستون زمانی داشته باشد، در حالی که سرویس فعلی یک 
`financial_period_id` 
reply.md:159:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:351:| Period | `FinancialPeriod` | 
`financial_periods` |
reply.md:160:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:396:2. `Report.financial_period_id` اجباری است و 
reply.md:161:`ingest_codal_report` یک period_id واحد را به تمام RawFinancialFactهای یک report version اختصاص می‌دهد.
reply.md:163:`src/ingestion/service.py::ingest_codal_report`؛ facadeها در `src/ingestion/codal/ingestion.py` و 
`pipeline.py` | در 
reply.md:167:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:422:| `financial_periods` | در مسیر CODAL، 
period از قبل 
reply.md:170:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:460:5. ساختار فعلی `Report.financial_period_id` 
و 
reply.md:175:محدودیت را دارد. متد `ingest_codal_report` یک `period_id` می‌گیرد و همان مقدار را برای همهٔ 
RawFinancialFactها ذخیره 
reply.md:177:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:477:4. `Report.financial_period_id` هم اجباری 
است؛ بنابراین 
reply.md:182:association، الزامی/اختیاری بودن `Report.financial_period_id` قدیمی و نگاشت نسخه‌های اصلاحی باید در Task 
008 و Task 
reply.md:185:`src/ingestion/service.py::ingest_codal_report` مستقیماً برای هر `RawLineInput` یک `RawFinancialFact` 
می‌سازد و با 
reply.md:191:`src/ingestion/service.py::ingest_codal_report` می‌رسند؛ این تابع برای هر RawLineInput یک 
RawFinancialFact می‌سازد و 
reply.md:196:`service.py::ingest_codal_report` → RawFinancialFact.
reply.md:197:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1682:- `codal/ingestion.py::ingest_codal_report` 
فقط facade 
reply.md:198:است و به writer مرکزی `service.py::ingest_codal_report` می‌رسد.
reply.md:199:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1683:- `codal/ingestion.py::ingest_codal_pdf` 
extraction و 
reply.md:202:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1684:- `codal/pipeline.py::load_codal_pdf` و 
reply.md:203:`load_codal_pdf_from_url` acquisition/extraction/validation را پیش از writer اجرا می‌کنند؛ failureهای این 
مراحل Run 
reply.md:206:gateهای طراحی DB-DES-009. اولین مورد: inventory تمام مصرف‌کنندگان `reports.financial_period_id`، چون پیش 
از nullable 
reply.md:210:`reports.financial_period_id` و تفکیک قرارداد legacy CODAL از Excel — 2026-11-18
reply.md:211:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1714:- ستون `Report.financial_period_id` در ORM 
اجباری است 
reply.md:214:`service.py::ingest_codal_report` delegate می‌کند؛ PDF wrapper پس از extraction از آن استفاده می‌کند. 
مسیرهای 
reply.md:216:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1718:- نام `financial_period_id` در 
evaluation/forecast 
reply.md:217:observation DTOها و تست‌های Stage 5/6 لزوماً به ستون `reports.financial_period_id` اشاره ندارد؛ این دو 
مفهوم باید در 
reply.md:221:`Report.financial_period_id` مجاز نیست. مسیر جدید Excel باید دوره را در سطح هر Fact تعیین کند و نباید یک 
دورهٔ واحد را 
reply.md:227:`report_versions.report_id` و `financial_periods.company_id` تا وقتی Fact وابسته وجود دارد باید ممنوع 
باشد. اگر 
reply.md:228:`Report.financial_period_id` به‌صورت optional metadata باقی ماند، در صورت non-NULL بودن تطابق شرکت آن نیز 
کنترل شود.
reply.md:230:writer قدیمی به Report.financial_period_id — 2026-11-18
reply.md:231:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1880:- `service.py::ingest_codal_report` writer 
مرکزی CODAL 
reply.md:234:`Report.financial_period_id` باید با ورودی یکسان باشند؛ در غیر این صورت عملیات رد می‌شود.
reply.md:236:`ingest_codal_report` take DTOs |
reply.md:237:prompts\10_Implementation_Status.md:83:| CODAL extraction outside core write | PASS | 
`ingest_codal_report` accepts 
reply.md:239:prompts\10_Implementation_Status.md:243:ingest_codal_report()
reply.md:240:src\tests\final_validation_audit.md:140:  → ingest_codal_report()
reply.md:241:src\tests\golden_audit_source_plan.md:15:ingest_codal_report()
reply.md:242:src\tests\golden_audit_source_plan.md:115:- Report / ReportVersion / RawFinancialFact created by 
ingest_codal_report()
reply.md:243:01_Stage1_Data_Foundation.md:278:financial_period_id
reply.md:246:(models cover industries/companies, financial_periods, reports/report_versions, raw 
reply.md:253:10_Production_Codal_Extraction_and_Data_Load.md:22:ingest_codal_report()
reply.md:254:10_Production_Codal_Extraction_and_Data_Load.md:113:`extract → validate → RawLineInput[] → 
ingest_codal_report()`
reply.md:255:11_Production_Data_Load_and_Foundation_Validation.md:136:ingest_codal_report()
reply.md:256:12_Database_Architecture_V1.1.md:104:- `financial_periods`
reply.md:257:12_Database_Architecture_V1.1.md:801:ingest_codal_report / ingest_ohlc_* / ingest_fx_rates
reply.md:259:consumed by `ingest_codal_report`; the existing downstream persistence boundary must remain 
format-independent.
reply.md:260:99_Architecture_Change_Log.md:386:  ingest_codal_report / ingest_ohlc_* / ingest_fx_rates
reply.md:262:is a **pre-ingestion** responsibility. `ingest_codal_report` receives already-extracted `RawLineInput` 
lines plus 
reply.md:265:PROJECT_HANDOFF_INSTRUCTIONS.md:252:    ingest_codal_report()
reply.md:266:reply.md:4:PDF را استخراج می‌کنند، خروجی `RawLineInput` می‌سازند و `ingest_codal_report()` آن را به 
`RawFinancialFact` 
reply.md:268:reply.md:8:`src/ingestion/service.py` | `RawLineInput`، `ingest_codal_report`، transaction و replay |
reply.md:269:reply.md:10:از `load_codal_pdf` و PDFهای fixture استفاده می‌کند.
reply.md:270:reply.md:11:database\reports\DB_AUD_006_CODAL_PIPELINE_IMPLEMENTATION_READINESS_AUDIT.md:61:در 
`ingest_codal_report()`:
reply.md:271:reply.md:13:`financial_period_id` است، درحالی‌که قرارداد منطقی می‌گوید یک ReportVersion می‌تواند چند دوره 
و هر 
reply.md:273:reply.md:15:database\reports\DB_AUD_006_CODAL_PIPELINE_IMPLEMENTATION_READINESS_AUDIT.md:83:- 
`ingest_codal_report()` 
reply.md:276:`ingest_codal_report`
reply.md:277:reply.md:19:`src/ingestion/codal/ingestion.py::ingest_codal_report` صرفاً facade سازگاری است و به 
reply.md:278:reply.md:20:`src/ingestion/service.py::ingest_codal_report` delegate می‌کند؛ transaction مستقل ندارد.
reply.md:279:reply.md:22:`src/ingestion/codal/ingestion.py::ingest_codal_pdf` extraction را اجرا می‌کند و سپس به 
facade بالا 
reply.md:281:reply.md:26:`src/ingestion/codal/pipeline.py::load_codal_pdf` و `load_codal_pdf_from_url` acquisition، 
extraction و 
reply.md:283:reply.md:30:`src/ingestion/service.py::ingest_codal_report` writer اصلی 
Report/ReportVersion/RawFinancialFact است. این 
reply.md:285:reply.md:36:`reports.financial_period_id` پیش از nullable کردن/جابه‌جایی آن است. سپس gateهای 
ReportVersion source 
reply.md:286:reply.md:39:`reports.financial_period_id` و مسیرهای فراخوانی CODAL — 2026-11-18
reply.md:287:reply.md:41:`financial_period_id|FinancialPeriod` در کل فایل‌های `*.py` و `*.sql` زیر repository، موارد 
زیر را نشان 
reply.md:289:reply.md:43:`Report.financial_period_id` با `nullable=False` و FK به `financial_periods.period_id`.
reply.md:290:reply.md:46:`Report.financial_period_id` استفاده نشده است.
reply.md:291:reply.md:48:تست‌های Stage 5/6: نام `financial_period_id` در DTOها و مدل‌های ارزیابی به‌عنوان شناسهٔ دورهٔ 
reply.md:293:reply.md:49:استفاده شده است؛ این موارد به‌تنهایی مصرف ستون `reports.financial_period_id` نیستند.
reply.md:294:reply.md:51:Report و قرارداد قدیمی را با `financial_period_id` اجباری می‌آزمایند؛ تست‌های PDF نیز رابطهٔ 
Report با 
reply.md:296:reply.md:54:تابع عمومی `ingest_codal_report` یک facade سازگار با گذشته است و به 
reply.md:297:`src.ingestion.service.ingest_codal_report` 
reply.md:298:reply.md:55:delegate می‌کند. تابع `ingest_codal_pdf` پس از extraction همین facade را فراخوانی می‌کند.
reply.md:299:reply.md:57:توابع `load_codal_pdf` و `load_codal_pdf_from_url` پس از acquisition/extraction/validation، 
writer مرکزی 
reply.md:300:reply.md:58:`src.ingestion.service.ingest_codal_report` را فراخوانی می‌کنند.
reply.md:301:reply.md:61:`financial_period_id` ندارند؛ این با یافتهٔ قبلی DB-AUD-013 مبنی بر نبود production 
Excel-to-canonical 
reply.md:304:`Report.financial_period_id` در 
reply.md:305:reply.md:68:`Report.financial_period_id` تا زمان تعیین تکلیف و بازنشستگی کنترل‌شدهٔ مسیر legacy باید حفظ 
شود؛ اگر در 
reply.md:307:reply.md:71:Report.financial_period_id و مرز writer قدیمی — 2026-11-18
reply.md:308:reply.md:73:مسیر مشاهده شد `src/ingestion/service.py::ingest_codal_report` است؛ facade در 
`codal/ingestion.py` به همین 
reply.md:310:reply.md:76:`Report.financial_period_id` با ورودی مقایسه می‌شوند؛ اختلاف باعث رد عملیات می‌شود.
reply.md:311:reply.md:78:`financial_period_id=period_id` ثبت می‌شود.
reply.md:312:reply.md:80:Report.financial_period_id (حذف تدریجی، nullable و descriptive، یا جایگزینی با primary-period 
metadata) پس 
reply.md:314:reply.md:83:`company_id`; free-text `report_type`; FK `financial_period_id` | Reuse, but report-type 
normalization is 
reply.md:317:`financial_periods` 
reply.md:318:reply.md:88:database\reports\DB_AUD_011_LEGACY_RAW_FACT_PROVENANCE_DECISION.md:92:- 
`ingest_codal_report(...)` creates 
reply.md:320:reply.md:90:database\reports\DB_AUD_012_CODAL_PDF_PATH_DEPENDENCY_AUDIT.md:17:load_codal_pdf / 
load_codal_pdf_from_url 
reply.md:322:reply.md:91:database\reports\DB_AUD_012_CODAL_PDF_PATH_DEPENDENCY_AUDIT.md:21:→ ingest_codal_report  
reply.md:323:reply.md:93:ingest_codal_pdf و facade سازگاری ingest_codal_report | بخش PDF-only + facade legacy |
reply.md:325:src/ingestion/service.py::ingest_codal_report | 
reply.md:326:reply.md:97:database\reports\DB_AUD_012_CODAL_PDF_PATH_DEPENDENCY_AUDIT.md:125:- 
`service.py::ingest_codal_report`: 
reply.md:328:reply.md:99:database\reports\DB_AUD_013_EXCEL_CANONICAL_PERSISTENCE_READINESS.md:45:- financial_period_id 
به‌عنوان 
reply.md:330:reply.md:101:database\reports\DB_AUD_013_EXCEL_CANONICAL_PERSISTENCE_READINESS.md:53:- 
financial_period_id در مدل فعلی 
reply.md:332:reply.md:105:`src/ingestion/service.py::ingest_codal_report`:
reply.md:333:reply.md:106:database\reports\DB_AUD_014_NORMALIZED_DERIVED_FACT_CONSUMER_AUDIT.md:103:    -> 
ingest_codal_report
reply.md:334:reply.md:107:database\reports\DB_DES_009_CANONICAL_FINANCIAL_FACT_PHYSICAL_MODEL.md:43:3. 
`financial_periods` — 
reply.md:336:reply.md:111:FinancialPeriod. The current NOT NULL `reports.financial_period_id` must not be allowed to 
impose one 
reply.md:339:`financial_periods` model 
reply.md:340:reply.md:116:consumers before making current `reports.financial_period_id` nullable or moving it.
reply.md:341:reply.md:118:`financial_period_id` را جداگانه نگه می‌دارد؛ FKها به‌تنهایی تضمین نمی‌کنند که دورهٔ گزارش 
متعلق به همان 
reply.md:343:reply.md:121:`report_versions.report_id` یا `financial_periods.company_id` تا وقتی Fact وابسته وجود دارد 
ممنوع باشد؛ 
reply.md:346:`Report.financial_period_id` در مدل 
reply.md:347:reply.md:127:pipelineهای load_codal_pdf و load_codal_pdf_from_url |
reply.md:349:\`src/ingestion/service.py::ingest_codal_report\` | 
reply.md:350:reply.md:132:پس از شناسایی callerها باید فقط facade PDF حذف و وضعیت ingest_codal_report جداگانه تعیین شود 
|
reply.md:351:reply.md:134:RawLineInput و ingest_codal_report فعلاً حفظ؛ بعداً با API جدید جایگزین یا صریحاً بازنشسته 
شوند |
reply.md:352:reply.md:135:database\reports\DB_PLAN_013_PDF_PATH_RETIREMENT_SEQUENCE.md:72:1. تابع فعلی 
\`ingest_codal_report\` را 
reply.md:355:`service.py::ingest_codal_report` | 
reply.md:357:`codal/ingestion.py::ingest_codal_pdf` و 
reply.md:358:reply.md:146:`ingestion/service.py::ingest_codal_report` (تابع persistence گزارش CODAL) یک 
`ReportVersion` و مجموعه‌ای 
reply.md:360:reply.md:150:`ingest_codal_report` و Stage 5 query | Stage 5 مصرف‌کنندهٔ مستقیم خروجی CODAL نیست | 
طراحی/پیاده‌سازی 
reply.md:363:`ingest_codal_report` 
reply.md:365:`financial_period_id` 
reply.md:367:`financial_periods` |
reply.md:368:reply.md:160:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:396:2. `Report.financial_period_id` 
اجباری است و 
reply.md:369:reply.md:161:`ingest_codal_report` یک period_id واحد را به تمام RawFinancialFactهای یک report version 
اختصاص می‌دهد.
reply.md:370:reply.md:163:`src/ingestion/service.py::ingest_codal_report`؛ facadeها در 
`src/ingestion/codal/ingestion.py` و 
reply.md:372:reply.md:167:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:422:| `financial_periods` | در مسیر 
CODAL، 
reply.md:374:reply.md:170:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:460:5. ساختار فعلی 
`Report.financial_period_id` 
reply.md:376:reply.md:175:محدودیت را دارد. متد `ingest_codal_report` یک `period_id` می‌گیرد و همان مقدار را برای همهٔ 
reply.md:378:reply.md:177:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:477:4. `Report.financial_period_id` 
هم اجباری 
reply.md:380:reply.md:182:association، الزامی/اختیاری بودن `Report.financial_period_id` قدیمی و نگاشت نسخه‌های اصلاحی 
باید در Task 
reply.md:382:reply.md:185:`src/ingestion/service.py::ingest_codal_report` مستقیماً برای هر `RawLineInput` یک 
`RawFinancialFact` 
reply.md:384:reply.md:191:`src/ingestion/service.py::ingest_codal_report` می‌رسند؛ این تابع برای هر RawLineInput یک 
reply.md:386:reply.md:196:`service.py::ingest_codal_report` → RawFinancialFact.
reply.md:387:reply.md:197:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1682:- 
`codal/ingestion.py::ingest_codal_report` 
reply.md:389:reply.md:198:است و به writer مرکزی `service.py::ingest_codal_report` می‌رسد.
reply.md:390:reply.md:199:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1683:- 
`codal/ingestion.py::ingest_codal_pdf` 
reply.md:392:reply.md:202:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1684:- 
`codal/pipeline.py::load_codal_pdf` و 
reply.md:393:reply.md:203:`load_codal_pdf_from_url` acquisition/extraction/validation را پیش از writer اجرا می‌کنند؛ 
failureهای این 
reply.md:395:reply.md:206:gateهای طراحی DB-DES-009. اولین مورد: inventory تمام مصرف‌کنندگان 
`reports.financial_period_id`، چون پیش 
reply.md:397:reply.md:210:`reports.financial_period_id` و تفکیک قرارداد legacy CODAL از Excel — 2026-11-18
reply.md:398:reply.md:211:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1714:- ستون 
`Report.financial_period_id` در ORM 
reply.md:400:reply.md:214:`service.py::ingest_codal_report` delegate می‌کند؛ PDF wrapper پس از extraction از آن 
استفاده می‌کند. 
reply.md:402:reply.md:216:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1718:- نام `financial_period_id` در 
reply.md:404:reply.md:217:observation DTOها و تست‌های Stage 5/6 لزوماً به ستون `reports.financial_period_id` اشاره 
ندارد؛ این دو 
reply.md:406:reply.md:221:`Report.financial_period_id` مجاز نیست. مسیر جدید Excel باید دوره را در سطح هر Fact تعیین 
کند و نباید یک 
reply.md:408:reply.md:227:`report_versions.report_id` و `financial_periods.company_id` تا وقتی Fact وابسته وجود دارد 
باید ممنوع 
reply.md:410:reply.md:228:`Report.financial_period_id` به‌صورت optional metadata باقی ماند، در صورت non-NULL بودن 
تطابق شرکت آن نیز 
reply.md:412:reply.md:230:writer قدیمی به Report.financial_period_id — 2026-11-18
reply.md:413:reply.md:231:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1880:- 
`service.py::ingest_codal_report` writer 
reply.md:415:reply.md:234:`Report.financial_period_id` باید با ورودی یکسان باشند؛ در غیر این صورت عملیات رد می‌شود.
reply.md:416:reply.md:236:`ingest_codal_report` take DTOs |
reply.md:418:`ingest_codal_report` accepts 
reply.md:419:reply.md:239:prompts\10_Implementation_Status.md:243:ingest_codal_report()
reply.md:420:reply.md:240:src\tests\final_validation_audit.md:140:  → ingest_codal_report()
reply.md:421:reply.md:241:src\tests\golden_audit_source_plan.md:15:ingest_codal_report()
reply.md:423:ingest_codal_report()
reply.md:424:reply.md:243:01_Stage1_Data_Foundation.md:278:financial_period_id
reply.md:425:reply.md:246:(models cover industries/companies, financial_periods, reports/report_versions, raw 
reply.md:426:reply.md:253:10_Production_Codal_Extraction_and_Data_Load.md:22:ingest_codal_report()
reply.md:428:ingest_codal_report()`
reply.md:429:reply.md:255:11_Production_Data_Load_and_Foundation_Validation.md:136:ingest_codal_report()
reply.md:430:reply.md:256:12_Database_Architecture_V1.1.md:104:- `financial_periods`
reply.md:431:reply.md:257:12_Database_Architecture_V1.1.md:801:ingest_codal_report / ingest_ohlc_* / ingest_fx_rates
reply.md:432:reply.md:259:consumed by `ingest_codal_report`; the existing downstream persistence boundary must remain 
reply.md:434:reply.md:260:99_Architecture_Change_Log.md:386:  ingest_codal_report / ingest_ohlc_* / ingest_fx_rates
reply.md:435:reply.md:262:is a **pre-ingestion** responsibility. `ingest_codal_report` receives already-extracted 
`RawLineInput` 
reply.md:437:reply.md:265:PROJECT_HANDOFF_INSTRUCTIONS.md:252:    ingest_codal_report()
reply.md:438:reply.md:266:reply.md:4:PDF را استخراج می‌کنند، خروجی `RawLineInput` می‌سازند و `ingest_codal_report()` 
آن را به 
reply.md:440:reply.md:268:reply.md:8:`src/ingestion/service.py` | `RawLineInput`، `ingest_codal_report`، transaction و 
replay |
reply.md:441:reply.md:269:reply.md:10:از `load_codal_pdf` و PDFهای fixture استفاده می‌کند.
reply.md:443:`ingest_codal_report()`:
reply.md:444:reply.md:271:reply.md:13:`financial_period_id` است، درحالی‌که قرارداد منطقی می‌گوید یک ReportVersion 
می‌تواند چند دوره 
reply.md:447:`ingest_codal_report()` 
reply.md:448:reply.md:276:`ingest_codal_report`
reply.md:449:reply.md:277:reply.md:19:`src/ingestion/codal/ingestion.py::ingest_codal_report` صرفاً facade سازگاری است 
و به 
reply.md:450:reply.md:278:reply.md:20:`src/ingestion/service.py::ingest_codal_report` delegate می‌کند؛ transaction 
مستقل ندارد.
reply.md:451:reply.md:279:reply.md:22:`src/ingestion/codal/ingestion.py::ingest_codal_pdf` extraction را اجرا می‌کند و 
سپس به 
reply.md:453:reply.md:281:reply.md:26:`src/ingestion/codal/pipeline.py::load_codal_pdf` و `load_codal_pdf_from_url` 
acquisition، 
reply.md:455:reply.md:283:reply.md:30:`src/ingestion/service.py::ingest_codal_report` writer اصلی 
reply.md:457:reply.md:285:reply.md:36:`reports.financial_period_id` پیش از nullable کردن/جابه‌جایی آن است. سپس gateهای 
reply.md:459:reply.md:286:reply.md:39:`reports.financial_period_id` و مسیرهای فراخوانی CODAL — 2026-11-18
reply.md:460:reply.md:287:reply.md:41:`financial_period_id|FinancialPeriod` در کل فایل‌های `*.py` و `*.sql` زیر 
repository، موارد 
reply.md:462:reply.md:289:reply.md:43:`Report.financial_period_id` با `nullable=False` و FK به 
`financial_periods.period_id`.
reply.md:463:reply.md:290:reply.md:46:`Report.financial_period_id` استفاده نشده است.
reply.md:464:reply.md:291:reply.md:48:تست‌های Stage 5/6: نام `financial_period_id` در DTOها و مدل‌های ارزیابی به‌عنوان 
شناسهٔ دورهٔ 
reply.md:465:reply.md:293:reply.md:49:استفاده شده است؛ این موارد به‌تنهایی مصرف ستون `reports.financial_period_id` 
نیستند.
reply.md:466:reply.md:294:reply.md:51:Report و قرارداد قدیمی را با `financial_period_id` اجباری می‌آزمایند؛ تست‌های 
PDF نیز رابطهٔ 
reply.md:468:reply.md:296:reply.md:54:تابع عمومی `ingest_codal_report` یک facade سازگار با گذشته است و به 
reply.md:469:reply.md:297:`src.ingestion.service.ingest_codal_report` 
reply.md:470:reply.md:298:reply.md:55:delegate می‌کند. تابع `ingest_codal_pdf` پس از extraction همین facade را 
فراخوانی می‌کند.
reply.md:471:reply.md:299:reply.md:57:توابع `load_codal_pdf` و `load_codal_pdf_from_url` پس از 
acquisition/extraction/validation، 
reply.md:473:reply.md:300:reply.md:58:`src.ingestion.service.ingest_codal_report` را فراخوانی می‌کنند.
reply.md:474:reply.md:301:reply.md:61:`financial_period_id` ندارند؛ این با یافتهٔ قبلی DB-AUD-013 مبنی بر نبود 
production 
reply.md:476:reply.md:304:`Report.financial_period_id` در 
reply.md:477:reply.md:305:reply.md:68:`Report.financial_period_id` تا زمان تعیین تکلیف و بازنشستگی کنترل‌شدهٔ مسیر 
legacy باید حفظ 
reply.md:479:reply.md:307:reply.md:71:Report.financial_period_id و مرز writer قدیمی — 2026-11-18
reply.md:480:reply.md:308:reply.md:73:مسیر مشاهده شد `src/ingestion/service.py::ingest_codal_report` است؛ facade در 
reply.md:482:reply.md:310:reply.md:76:`Report.financial_period_id` با ورودی مقایسه می‌شوند؛ اختلاف باعث رد عملیات 
می‌شود.
reply.md:483:reply.md:311:reply.md:78:`financial_period_id=period_id` ثبت می‌شود.
reply.md:484:reply.md:312:reply.md:80:Report.financial_period_id (حذف تدریجی، nullable و descriptive، یا جایگزینی با 
primary-period 
reply.md:486:reply.md:314:reply.md:83:`company_id`; free-text `report_type`; FK `financial_period_id` | Reuse, but 
report-type 
reply.md:488:reply.md:317:`financial_periods` 
reply.md:490:`ingest_codal_report(...)` creates 
reply.md:491:reply.md:320:reply.md:90:database\reports\DB_AUD_012_CODAL_PDF_PATH_DEPENDENCY_AUDIT.md:17:load_codal_pdf 
/ 
reply.md:492:load_codal_pdf_from_url 
reply.md:493:reply.md:322:reply.md:91:database\reports\DB_AUD_012_CODAL_PDF_PATH_DEPENDENCY_AUDIT.md:21:→ 
ingest_codal_report  
reply.md:494:reply.md:323:reply.md:93:ingest_codal_pdf و facade سازگاری ingest_codal_report | بخش PDF-only + facade 
legacy |
reply.md:495:reply.md:325:src/ingestion/service.py::ingest_codal_report | 
reply.md:497:`service.py::ingest_codal_report`: 
reply.md:498:reply.md:328:reply.md:99:database\reports\DB_AUD_013_EXCEL_CANONICAL_PERSISTENCE_READINESS.md:45:- 
financial_period_id 
reply.md:501:financial_period_id در مدل فعلی 
reply.md:502:reply.md:332:reply.md:105:`src/ingestion/service.py::ingest_codal_report`:
reply.md:504:ingest_codal_report
reply.md:506:`financial_periods` — 
reply.md:507:reply.md:336:reply.md:111:FinancialPeriod. The current NOT NULL `reports.financial_period_id` must not be 
allowed to 
reply.md:509:reply.md:339:`financial_periods` model 
reply.md:510:reply.md:340:reply.md:116:consumers before making current `reports.financial_period_id` nullable or 
moving it.
reply.md:511:reply.md:341:reply.md:118:`financial_period_id` را جداگانه نگه می‌دارد؛ FKها به‌تنهایی تضمین نمی‌کنند که 
دورهٔ گزارش 
reply.md:513:reply.md:343:reply.md:121:`report_versions.report_id` یا `financial_periods.company_id` تا وقتی Fact 
وابسته وجود دارد 
reply.md:515:reply.md:346:`Report.financial_period_id` در مدل 
reply.md:516:reply.md:347:reply.md:127:pipelineهای load_codal_pdf و load_codal_pdf_from_url |
reply.md:517:reply.md:349:\`src/ingestion/service.py::ingest_codal_report\` | 
reply.md:518:reply.md:350:reply.md:132:پس از شناسایی callerها باید فقط facade PDF حذف و وضعیت ingest_codal_report 
جداگانه تعیین شود 
reply.md:520:reply.md:351:reply.md:134:RawLineInput و ingest_codal_report فعلاً حفظ؛ بعداً با API جدید جایگزین یا 
صریحاً بازنشسته 
reply.md:523:\`ingest_codal_report\` را 
reply.md:524:reply.md:355:`service.py::ingest_codal_report` | 
reply.md:525:reply.md:357:`codal/ingestion.py::ingest_codal_pdf` و 
reply.md:526:reply.md:358:reply.md:146:`ingestion/service.py::ingest_codal_report` (تابع persistence گزارش CODAL) یک 
reply.md:528:reply.md:360:reply.md:150:`ingest_codal_report` و Stage 5 query | Stage 5 مصرف‌کنندهٔ مستقیم خروجی CODAL 
نیست | 
reply.md:530:reply.md:363:`ingest_codal_report` 
reply.md:531:reply.md:365:`financial_period_id` 
reply.md:532:reply.md:367:`financial_periods` |
reply.md:533:reply.md:368:reply.md:160:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:396:2. 
`Report.financial_period_id` 
reply.md:535:reply.md:369:reply.md:161:`ingest_codal_report` یک period_id واحد را به تمام RawFinancialFactهای یک 
report version 
reply.md:537:reply.md:370:reply.md:163:`src/ingestion/service.py::ingest_codal_report`؛ facadeها در 
reply.md:539:reply.md:372:reply.md:167:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:422:| 
`financial_periods` | در مسیر 
reply.md:542:`Report.financial_period_id` 
reply.md:543:reply.md:376:reply.md:175:محدودیت را دارد. متد `ingest_codal_report` یک `period_id` می‌گیرد و همان مقدار 
را برای همهٔ 
reply.md:544:reply.md:378:reply.md:177:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:477:4. 
`Report.financial_period_id` 
reply.md:546:reply.md:380:reply.md:182:association، الزامی/اختیاری بودن `Report.financial_period_id` قدیمی و نگاشت 
نسخه‌های اصلاحی 
reply.md:548:reply.md:382:reply.md:185:`src/ingestion/service.py::ingest_codal_report` مستقیماً برای هر `RawLineInput` 
یک 
reply.md:550:reply.md:384:reply.md:191:`src/ingestion/service.py::ingest_codal_report` می‌رسند؛ این تابع برای هر 
RawLineInput یک 
reply.md:551:reply.md:386:reply.md:196:`service.py::ingest_codal_report` → RawFinancialFact.
reply.md:553:`codal/ingestion.py::ingest_codal_report` 
reply.md:554:reply.md:389:reply.md:198:است و به writer مرکزی `service.py::ingest_codal_report` می‌رسد.
reply.md:556:`codal/ingestion.py::ingest_codal_pdf` 
reply.md:558:`codal/pipeline.py::load_codal_pdf` و 
reply.md:559:reply.md:393:reply.md:203:`load_codal_pdf_from_url` acquisition/extraction/validation را پیش از writer 
اجرا می‌کنند؛ 
reply.md:562:`reports.financial_period_id`، چون پیش 
reply.md:563:reply.md:397:reply.md:210:`reports.financial_period_id` و تفکیک قرارداد legacy CODAL از Excel — 2026-11-18
reply.md:565:`Report.financial_period_id` در ORM 
reply.md:566:reply.md:400:reply.md:214:`service.py::ingest_codal_report` delegate می‌کند؛ PDF wrapper پس از extraction 
از آن 
reply.md:568:reply.md:402:reply.md:216:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1718:- نام 
`financial_period_id` در 
reply.md:569:reply.md:404:reply.md:217:observation DTOها و تست‌های Stage 5/6 لزوماً به ستون 
`reports.financial_period_id` اشاره 
reply.md:571:reply.md:406:reply.md:221:`Report.financial_period_id` مجاز نیست. مسیر جدید Excel باید دوره را در سطح هر 
Fact تعیین 
reply.md:573:reply.md:408:reply.md:227:`report_versions.report_id` و `financial_periods.company_id` تا وقتی Fact 
وابسته وجود دارد 
reply.md:575:reply.md:410:reply.md:228:`Report.financial_period_id` به‌صورت optional metadata باقی ماند، در صورت 
non-NULL بودن 
reply.md:577:reply.md:412:reply.md:230:writer قدیمی به Report.financial_period_id — 2026-11-18
reply.md:579:`service.py::ingest_codal_report` writer 
reply.md:580:reply.md:415:reply.md:234:`Report.financial_period_id` باید با ورودی یکسان باشند؛ در غیر این صورت عملیات 
رد می‌شود.
reply.md:581:reply.md:416:reply.md:236:`ingest_codal_report` take DTOs |
reply.md:582:reply.md:418:`ingest_codal_report` accepts 
reply.md:583:reply.md:419:reply.md:239:prompts\10_Implementation_Status.md:243:ingest_codal_report()
reply.md:584:reply.md:420:reply.md:240:src\tests\final_validation_audit.md:140:  → ingest_codal_report()
reply.md:585:reply.md:421:reply.md:241:src\tests\golden_audit_source_plan.md:15:ingest_codal_report()
reply.md:586:reply.md:423:ingest_codal_report()
reply.md:587:reply.md:424:reply.md:243:01_Stage1_Data_Foundation.md:278:financial_period_id
reply.md:588:reply.md:425:reply.md:246:(models cover industries/companies, financial_periods, reports/report_versions, 
raw 
reply.md:589:reply.md:426:reply.md:253:10_Production_Codal_Extraction_and_Data_Load.md:22:ingest_codal_report()
reply.md:590:reply.md:428:ingest_codal_report()`
reply.md:591:reply.md:429:reply.md:255:11_Production_Data_Load_and_Foundation_Validation.md:136:ingest_codal_report()
reply.md:592:reply.md:430:reply.md:256:12_Database_Architecture_V1.1.md:104:- `financial_periods`
reply.md:593:reply.md:431:reply.md:257:12_Database_Architecture_V1.1.md:801:ingest_codal_report / ingest_ohlc_* / 
ingest_fx_rates
reply.md:594:reply.md:432:reply.md:259:consumed by `ingest_codal_report`; the existing downstream persistence boundary 
must remain 
reply.md:595:reply.md:434:reply.md:260:99_Architecture_Change_Log.md:386:  ingest_codal_report / ingest_ohlc_* / 
ingest_fx_rates
reply.md:596:reply.md:435:reply.md:262:is a **pre-ingestion** responsibility. `ingest_codal_report` receives 
already-extracted 
reply.md:598:reply.md:437:reply.md:265:PROJECT_HANDOFF_INSTRUCTIONS.md:252:    ingest_codal_report()
reply.md:599:reply.md:438:reply.md:266:reply.md:4:PDF را استخراج می‌کنند، خروجی `RawLineInput` می‌سازند و 
`ingest_codal_report()` 
reply.md:601:reply.md:440:reply.md:268:reply.md:8:`src/ingestion/service.py` | `RawLineInput`، `ingest_codal_report`، 
transaction و 
reply.md:603:reply.md:441:reply.md:269:reply.md:10:از `load_codal_pdf` و PDFهای fixture استفاده می‌کند.
reply.md:604:reply.md:443:`ingest_codal_report()`:
reply.md:605:reply.md:444:reply.md:271:reply.md:13:`financial_period_id` است، درحالی‌که قرارداد منطقی می‌گوید یک 
ReportVersion 
reply.md:607:reply.md:447:`ingest_codal_report()` 
reply.md:608:reply.md:448:reply.md:276:`ingest_codal_report`
reply.md:609:reply.md:449:reply.md:277:reply.md:19:`src/ingestion/codal/ingestion.py::ingest_codal_report` صرفاً 
facade سازگاری است 
reply.md:611:reply.md:450:reply.md:278:reply.md:20:`src/ingestion/service.py::ingest_codal_report` delegate می‌کند؛ 
transaction 
reply.md:613:reply.md:451:reply.md:279:reply.md:22:`src/ingestion/codal/ingestion.py::ingest_codal_pdf` extraction را 
اجرا می‌کند و 
reply.md:615:reply.md:453:reply.md:281:reply.md:26:`src/ingestion/codal/pipeline.py::load_codal_pdf` و 
`load_codal_pdf_from_url` 
reply.md:617:reply.md:455:reply.md:283:reply.md:30:`src/ingestion/service.py::ingest_codal_report` writer اصلی 
reply.md:618:reply.md:457:reply.md:285:reply.md:36:`reports.financial_period_id` پیش از nullable کردن/جابه‌جایی آن 
است. سپس gateهای 
reply.md:619:reply.md:459:reply.md:286:reply.md:39:`reports.financial_period_id` و مسیرهای فراخوانی CODAL — 2026-11-18
reply.md:620:reply.md:460:reply.md:287:reply.md:41:`financial_period_id|FinancialPeriod` در کل فایل‌های `*.py` و 
`*.sql` زیر 
reply.md:622:reply.md:462:reply.md:289:reply.md:43:`Report.financial_period_id` با `nullable=False` و FK به 
reply.md:623:`financial_periods.period_id`.
reply.md:624:reply.md:463:reply.md:290:reply.md:46:`Report.financial_period_id` استفاده نشده است.
reply.md:625:reply.md:464:reply.md:291:reply.md:48:تست‌های Stage 5/6: نام `financial_period_id` در DTOها و مدل‌های 
ارزیابی به‌عنوان 
reply.md:627:reply.md:465:reply.md:293:reply.md:49:استفاده شده است؛ این موارد به‌تنهایی مصرف ستون 
`reports.financial_period_id` 
reply.md:629:reply.md:466:reply.md:294:reply.md:51:Report و قرارداد قدیمی را با `financial_period_id` اجباری 
می‌آزمایند؛ تست‌های 
reply.md:631:reply.md:468:reply.md:296:reply.md:54:تابع عمومی `ingest_codal_report` یک facade سازگار با گذشته است و به 
reply.md:632:reply.md:469:reply.md:297:`src.ingestion.service.ingest_codal_report` 
reply.md:633:reply.md:470:reply.md:298:reply.md:55:delegate می‌کند. تابع `ingest_codal_pdf` پس از extraction همین 
facade را 
reply.md:635:reply.md:471:reply.md:299:reply.md:57:توابع `load_codal_pdf` و `load_codal_pdf_from_url` پس از 
reply.md:637:reply.md:473:reply.md:300:reply.md:58:`src.ingestion.service.ingest_codal_report` را فراخوانی می‌کنند.
reply.md:638:reply.md:474:reply.md:301:reply.md:61:`financial_period_id` ندارند؛ این با یافتهٔ قبلی DB-AUD-013 مبنی بر 
نبود 
reply.md:640:reply.md:476:reply.md:304:`Report.financial_period_id` در 
reply.md:641:reply.md:477:reply.md:305:reply.md:68:`Report.financial_period_id` تا زمان تعیین تکلیف و بازنشستگی 
کنترل‌شدهٔ مسیر 
reply.md:643:reply.md:479:reply.md:307:reply.md:71:Report.financial_period_id و مرز writer قدیمی — 2026-11-18
reply.md:644:reply.md:480:reply.md:308:reply.md:73:مسیر مشاهده شد `src/ingestion/service.py::ingest_codal_report` است؛ 
facade در 
reply.md:645:reply.md:482:reply.md:310:reply.md:76:`Report.financial_period_id` با ورودی مقایسه می‌شوند؛ اختلاف باعث 
رد عملیات 
reply.md:647:reply.md:483:reply.md:311:reply.md:78:`financial_period_id=period_id` ثبت می‌شود.
reply.md:648:reply.md:484:reply.md:312:reply.md:80:Report.financial_period_id (حذف تدریجی، nullable و descriptive، یا 
جایگزینی با 
reply.md:650:reply.md:486:reply.md:314:reply.md:83:`company_id`; free-text `report_type`; FK `financial_period_id` | 
Reuse, but 
reply.md:652:reply.md:488:reply.md:317:`financial_periods` 
reply.md:653:reply.md:490:`ingest_codal_report(...)` creates 
reply.md:654:reply.md:491:reply.md:320:reply.md:90:database\reports\DB_AUD_012_CODAL_PDF_PATH_DEPENDENCY_AUDIT.md:17:lo
ad_codal_pdf 
reply.md:656:reply.md:492:load_codal_pdf_from_url 
reply.md:658:ingest_codal_report  
reply.md:659:reply.md:494:reply.md:323:reply.md:93:ingest_codal_pdf و facade سازگاری ingest_codal_report | بخش 
PDF-only + facade 
reply.md:661:reply.md:495:reply.md:325:src/ingestion/service.py::ingest_codal_report | 
reply.md:662:reply.md:497:`service.py::ingest_codal_report`: 
reply.md:664:financial_period_id 
reply.md:665:reply.md:501:financial_period_id در مدل فعلی 
reply.md:666:reply.md:502:reply.md:332:reply.md:105:`src/ingestion/service.py::ingest_codal_report`:
reply.md:667:reply.md:504:ingest_codal_report
reply.md:668:reply.md:506:`financial_periods` — 
reply.md:669:reply.md:507:reply.md:336:reply.md:111:FinancialPeriod. The current NOT NULL 
`reports.financial_period_id` must not be 
reply.md:671:reply.md:509:reply.md:339:`financial_periods` model 
reply.md:672:reply.md:510:reply.md:340:reply.md:116:consumers before making current `reports.financial_period_id` 
nullable or 
reply.md:674:reply.md:511:reply.md:341:reply.md:118:`financial_period_id` را جداگانه نگه می‌دارد؛ FKها به‌تنهایی تضمین 
نمی‌کنند که 
reply.md:676:reply.md:513:reply.md:343:reply.md:121:`report_versions.report_id` یا `financial_periods.company_id` تا 
وقتی Fact 
reply.md:678:reply.md:515:reply.md:346:`Report.financial_period_id` در مدل 
reply.md:679:reply.md:516:reply.md:347:reply.md:127:pipelineهای load_codal_pdf و load_codal_pdf_from_url |
reply.md:680:reply.md:517:reply.md:349:\`src/ingestion/service.py::ingest_codal_report\` | 
reply.md:681:reply.md:518:reply.md:350:reply.md:132:پس از شناسایی callerها باید فقط facade PDF حذف و وضعیت 
ingest_codal_report 
reply.md:683:reply.md:520:reply.md:351:reply.md:134:RawLineInput و ingest_codal_report فعلاً حفظ؛ بعداً با API جدید 
جایگزین یا 
reply.md:685:reply.md:523:\`ingest_codal_report\` را 
reply.md:686:reply.md:524:reply.md:355:`service.py::ingest_codal_report` | 
reply.md:687:reply.md:525:reply.md:357:`codal/ingestion.py::ingest_codal_pdf` و 
reply.md:688:reply.md:526:reply.md:358:reply.md:146:`ingestion/service.py::ingest_codal_report` (تابع persistence 
گزارش CODAL) یک 
reply.md:689:reply.md:528:reply.md:360:reply.md:150:`ingest_codal_report` و Stage 5 query | Stage 5 مصرف‌کنندهٔ مستقیم 
خروجی CODAL 
reply.md:691:reply.md:530:reply.md:363:`ingest_codal_report` 
reply.md:692:reply.md:531:reply.md:365:`financial_period_id` 
reply.md:693:reply.md:532:reply.md:367:`financial_periods` |
reply.md:695:`Report.financial_period_id` 
reply.md:696:reply.md:535:reply.md:369:reply.md:161:`ingest_codal_report` یک period_id واحد را به تمام 
RawFinancialFactهای یک 
reply.md:698:reply.md:537:reply.md:370:reply.md:163:`src/ingestion/service.py::ingest_codal_report`؛ facadeها در 
reply.md:700:`financial_periods` | در مسیر 
reply.md:701:reply.md:542:`Report.financial_period_id` 
reply.md:702:reply.md:543:reply.md:376:reply.md:175:محدودیت را دارد. متد `ingest_codal_report` یک `period_id` می‌گیرد 
و همان مقدار 
reply.md:705:`Report.financial_period_id` 
reply.md:706:reply.md:546:reply.md:380:reply.md:182:association، الزامی/اختیاری بودن `Report.financial_period_id` 
قدیمی و نگاشت 
reply.md:708:reply.md:548:reply.md:382:reply.md:185:`src/ingestion/service.py::ingest_codal_report` مستقیماً برای هر 
`RawLineInput` 
reply.md:710:reply.md:550:reply.md:384:reply.md:191:`src/ingestion/service.py::ingest_codal_report` می‌رسند؛ این تابع 
برای هر 
reply.md:712:reply.md:551:reply.md:386:reply.md:196:`service.py::ingest_codal_report` → RawFinancialFact.
reply.md:713:reply.md:553:`codal/ingestion.py::ingest_codal_report` 
reply.md:714:reply.md:554:reply.md:389:reply.md:198:است و به writer مرکزی `service.py::ingest_codal_report` می‌رسد.
reply.md:715:reply.md:556:`codal/ingestion.py::ingest_codal_pdf` 
reply.md:716:reply.md:558:`codal/pipeline.py::load_codal_pdf` و 
reply.md:717:reply.md:559:reply.md:393:reply.md:203:`load_codal_pdf_from_url` acquisition/extraction/validation را پیش 
از writer 
reply.md:719:reply.md:562:`reports.financial_period_id`، چون پیش 
reply.md:720:reply.md:563:reply.md:397:reply.md:210:`reports.financial_period_id` و تفکیک قرارداد legacy CODAL از 
Excel — 2026-11-18
reply.md:721:reply.md:565:`Report.financial_period_id` در ORM 
reply.md:722:reply.md:566:reply.md:400:reply.md:214:`service.py::ingest_codal_report` delegate می‌کند؛ PDF wrapper پس 
از extraction 
reply.md:725:`financial_period_id` در 
reply.md:727:`reports.financial_period_id` اشاره 
reply.md:728:reply.md:571:reply.md:406:reply.md:221:`Report.financial_period_id` مجاز نیست. مسیر جدید Excel باید دوره 
را در سطح هر 
reply.md:730:reply.md:573:reply.md:408:reply.md:227:`report_versions.report_id` و `financial_periods.company_id` تا 
وقتی Fact 
reply.md:732:reply.md:575:reply.md:410:reply.md:228:`Report.financial_period_id` به‌صورت optional metadata باقی ماند، 
در صورت 
reply.md:734:reply.md:577:reply.md:412:reply.md:230:writer قدیمی به Report.financial_period_id — 2026-11-18
reply.md:735:reply.md:579:`service.py::ingest_codal_report` writer 
reply.md:736:reply.md:580:reply.md:415:reply.md:234:`Report.financial_period_id` باید با ورودی یکسان باشند؛ در غیر این 
صورت عملیات 
reply.md:738:reply.md:581:reply.md:416:reply.md:236:`ingest_codal_report` take DTOs |
reply.md:739:reply.md:582:reply.md:418:`ingest_codal_report` accepts 
reply.md:740:reply.md:583:reply.md:419:reply.md:239:prompts\10_Implementation_Status.md:243:ingest_codal_report()
reply.md:741:reply.md:584:reply.md:420:reply.md:240:src\tests\final_validation_audit.md:140:  → ingest_codal_report()
reply.md:742:reply.md:585:reply.md:421:reply.md:241:src\tests\golden_audit_source_plan.md:15:ingest_codal_report()
reply.md:743:reply.md:586:reply.md:423:ingest_codal_report()
reply.md:744:reply.md:587:reply.md:424:reply.md:243:01_Stage1_Data_Foundation.md:278:financial_period_id
reply.md:745:reply.md:588:reply.md:425:reply.md:246:(models cover industries/companies, financial_periods, 
reports/report_versions, 
reply.md:747:reply.md:589:reply.md:426:reply.md:253:10_Production_Codal_Extraction_and_Data_Load.md:22:ingest_codal_rep
ort()
reply.md:748:reply.md:590:reply.md:428:ingest_codal_report()`
reply.md:749:reply.md:591:reply.md:429:reply.md:255:11_Production_Data_Load_and_Foundation_Validation.md:136:ingest_cod
al_report()
reply.md:750:reply.md:592:reply.md:430:reply.md:256:12_Database_Architecture_V1.1.md:104:- `financial_periods`
reply.md:751:reply.md:593:reply.md:431:reply.md:257:12_Database_Architecture_V1.1.md:801:ingest_codal_report / 
ingest_ohlc_* / 
reply.md:753:reply.md:594:reply.md:432:reply.md:259:consumed by `ingest_codal_report`; the existing downstream 
persistence boundary 
reply.md:755:reply.md:595:reply.md:434:reply.md:260:99_Architecture_Change_Log.md:386:  ingest_codal_report / 
ingest_ohlc_* / 
reply.md:757:reply.md:596:reply.md:435:reply.md:262:is a **pre-ingestion** responsibility. `ingest_codal_report` 
receives 
reply.md:759:reply.md:598:reply.md:437:reply.md:265:PROJECT_HANDOFF_INSTRUCTIONS.md:252:    ingest_codal_report()
reply.md:761:`ingest_codal_report()` 
reply.md:762:reply.md:601:reply.md:440:reply.md:268:reply.md:8:`src/ingestion/service.py` | `RawLineInput`، 
`ingest_codal_report`، 
reply.md:764:reply.md:603:reply.md:441:reply.md:269:reply.md:10:از `load_codal_pdf` و PDFهای fixture استفاده می‌کند.
reply.md:765:reply.md:604:reply.md:443:`ingest_codal_report()`:
reply.md:766:reply.md:605:reply.md:444:reply.md:271:reply.md:13:`financial_period_id` است، درحالی‌که قرارداد منطقی 
می‌گوید یک 
reply.md:768:reply.md:607:reply.md:447:`ingest_codal_report()` 
reply.md:769:reply.md:608:reply.md:448:reply.md:276:`ingest_codal_report`
reply.md:770:reply.md:609:reply.md:449:reply.md:277:reply.md:19:`src/ingestion/codal/ingestion.py::ingest_codal_report`
 صرفاً 
reply.md:772:reply.md:611:reply.md:450:reply.md:278:reply.md:20:`src/ingestion/service.py::ingest_codal_report` 
delegate می‌کند؛ 
reply.md:774:reply.md:613:reply.md:451:reply.md:279:reply.md:22:`src/ingestion/codal/ingestion.py::ingest_codal_pdf` 
extraction را 
reply.md:776:reply.md:615:reply.md:453:reply.md:281:reply.md:26:`src/ingestion/codal/pipeline.py::load_codal_pdf` و 
reply.md:777:`load_codal_pdf_from_url` 
reply.md:778:reply.md:617:reply.md:455:reply.md:283:reply.md:30:`src/ingestion/service.py::ingest_codal_report` writer 
اصلی 
reply.md:779:reply.md:618:reply.md:457:reply.md:285:reply.md:36:`reports.financial_period_id` پیش از nullable 
کردن/جابه‌جایی آن 
reply.md:781:reply.md:619:reply.md:459:reply.md:286:reply.md:39:`reports.financial_period_id` و مسیرهای فراخوانی CODAL 
— 2026-11-18
reply.md:782:reply.md:620:reply.md:460:reply.md:287:reply.md:41:`financial_period_id|FinancialPeriod` در کل فایل‌های 
`*.py` و 
reply.md:784:reply.md:622:reply.md:462:reply.md:289:reply.md:43:`Report.financial_period_id` با `nullable=False` و FK 
به 
reply.md:785:reply.md:623:`financial_periods.period_id`.
reply.md:786:reply.md:624:reply.md:463:reply.md:290:reply.md:46:`Report.financial_period_id` استفاده نشده است.
reply.md:787:reply.md:625:reply.md:464:reply.md:291:reply.md:48:تست‌های Stage 5/6: نام `financial_period_id` در DTOها 
و مدل‌های 
reply.md:790:`reports.financial_period_id` 
reply.md:791:reply.md:629:reply.md:466:reply.md:294:reply.md:51:Report و قرارداد قدیمی را با `financial_period_id` 
اجباری 
reply.md:793:reply.md:631:reply.md:468:reply.md:296:reply.md:54:تابع عمومی `ingest_codal_report` یک facade سازگار با 
گذشته است و به 
reply.md:794:reply.md:632:reply.md:469:reply.md:297:`src.ingestion.service.ingest_codal_report` 
reply.md:795:reply.md:633:reply.md:470:reply.md:298:reply.md:55:delegate می‌کند. تابع `ingest_codal_pdf` پس از 
extraction همین 
reply.md:797:reply.md:635:reply.md:471:reply.md:299:reply.md:57:توابع `load_codal_pdf` و `load_codal_pdf_from_url` پس 
از 
reply.md:798:reply.md:637:reply.md:473:reply.md:300:reply.md:58:`src.ingestion.service.ingest_codal_report` را 
فراخوانی می‌کنند.
reply.md:799:reply.md:638:reply.md:474:reply.md:301:reply.md:61:`financial_period_id` ندارند؛ این با یافتهٔ قبلی 
DB-AUD-013 مبنی بر 
reply.md:801:reply.md:640:reply.md:476:reply.md:304:`Report.financial_period_id` در 
reply.md:802:reply.md:641:reply.md:477:reply.md:305:reply.md:68:`Report.financial_period_id` تا زمان تعیین تکلیف و 
بازنشستگی 
reply.md:804:reply.md:643:reply.md:479:reply.md:307:reply.md:71:Report.financial_period_id و مرز writer قدیمی — 
2026-11-18
reply.md:805:reply.md:644:reply.md:480:reply.md:308:reply.md:73:مسیر مشاهده شد 
`src/ingestion/service.py::ingest_codal_report` است؛ 
reply.md:807:reply.md:645:reply.md:482:reply.md:310:reply.md:76:`Report.financial_period_id` با ورودی مقایسه می‌شوند؛ 
اختلاف باعث 
reply.md:809:reply.md:647:reply.md:483:reply.md:311:reply.md:78:`financial_period_id=period_id` ثبت می‌شود.
reply.md:810:reply.md:648:reply.md:484:reply.md:312:reply.md:80:Report.financial_period_id (حذف تدریجی، nullable و 
descriptive، یا 
reply.md:812:reply.md:650:reply.md:486:reply.md:314:reply.md:83:`company_id`; free-text `report_type`; FK 
`financial_period_id` | 
reply.md:814:reply.md:652:reply.md:488:reply.md:317:`financial_periods` 
reply.md:815:reply.md:653:reply.md:490:`ingest_codal_report(...)` creates 
reply.md:818:reply.md:656:reply.md:492:load_codal_pdf_from_url 
reply.md:819:reply.md:658:ingest_codal_report  
reply.md:820:reply.md:659:reply.md:494:reply.md:323:reply.md:93:ingest_codal_pdf و facade سازگاری ingest_codal_report 
| بخش 
reply.md:822:reply.md:661:reply.md:495:reply.md:325:src/ingestion/service.py::ingest_codal_report | 
reply.md:823:reply.md:662:reply.md:497:`service.py::ingest_codal_report`: 
reply.md:824:reply.md:664:financial_period_id 
reply.md:825:reply.md:665:reply.md:501:financial_period_id در مدل فعلی 
reply.md:826:reply.md:666:reply.md:502:reply.md:332:reply.md:105:`src/ingestion/service.py::ingest_codal_report`:
reply.md:827:reply.md:667:reply.md:504:ingest_codal_report
reply.md:828:reply.md:668:reply.md:506:`financial_periods` — 
reply.md:830:`reports.financial_period_id` must not be 
reply.md:831:reply.md:671:reply.md:509:reply.md:339:`financial_periods` model 
reply.md:832:reply.md:672:reply.md:510:reply.md:340:reply.md:116:consumers before making current 
`reports.financial_period_id` 
reply.md:834:reply.md:674:reply.md:511:reply.md:341:reply.md:118:`financial_period_id` را جداگانه نگه می‌دارد؛ FKها 
به‌تنهایی تضمین 
reply.md:836:reply.md:676:reply.md:513:reply.md:343:reply.md:121:`report_versions.report_id` یا 
`financial_periods.company_id` تا 
reply.md:838:reply.md:678:reply.md:515:reply.md:346:`Report.financial_period_id` در مدل 
reply.md:839:reply.md:679:reply.md:516:reply.md:347:reply.md:127:pipelineهای load_codal_pdf و load_codal_pdf_from_url |
reply.md:840:reply.md:680:reply.md:517:reply.md:349:\`src/ingestion/service.py::ingest_codal_report\` | 
reply.md:842:ingest_codal_report 
reply.md:843:reply.md:683:reply.md:520:reply.md:351:reply.md:134:RawLineInput و ingest_codal_report فعلاً حفظ؛ بعداً 
با API جدید 
reply.md:845:reply.md:685:reply.md:523:\`ingest_codal_report\` را 
reply.md:846:reply.md:686:reply.md:524:reply.md:355:`service.py::ingest_codal_report` | 
reply.md:847:reply.md:687:reply.md:525:reply.md:357:`codal/ingestion.py::ingest_codal_pdf` و 
reply.md:848:reply.md:688:reply.md:526:reply.md:358:reply.md:146:`ingestion/service.py::ingest_codal_report` (تابع 
persistence 
reply.md:850:reply.md:689:reply.md:528:reply.md:360:reply.md:150:`ingest_codal_report` و Stage 5 query | Stage 5 
مصرف‌کنندهٔ مستقیم 
reply.md:852:reply.md:691:reply.md:530:reply.md:363:`ingest_codal_report` 
reply.md:853:reply.md:692:reply.md:531:reply.md:365:`financial_period_id` 
reply.md:854:reply.md:693:reply.md:532:reply.md:367:`financial_periods` |
reply.md:855:reply.md:695:`Report.financial_period_id` 
reply.md:856:reply.md:696:reply.md:535:reply.md:369:reply.md:161:`ingest_codal_report` یک period_id واحد را به تمام 
reply.md:858:reply.md:698:reply.md:537:reply.md:370:reply.md:163:`src/ingestion/service.py::ingest_codal_report`؛ 
facadeها در 
reply.md:859:reply.md:700:`financial_periods` | در مسیر 
reply.md:860:reply.md:701:reply.md:542:`Report.financial_period_id` 
reply.md:861:reply.md:702:reply.md:543:reply.md:376:reply.md:175:محدودیت را دارد. متد `ingest_codal_report` یک 
`period_id` می‌گیرد 
reply.md:863:reply.md:705:`Report.financial_period_id` 
reply.md:864:reply.md:706:reply.md:546:reply.md:380:reply.md:182:association، الزامی/اختیاری بودن 
`Report.financial_period_id` 
reply.md:866:reply.md:708:reply.md:548:reply.md:382:reply.md:185:`src/ingestion/service.py::ingest_codal_report` 
مستقیماً برای هر 
reply.md:868:reply.md:710:reply.md:550:reply.md:384:reply.md:191:`src/ingestion/service.py::ingest_codal_report` 
می‌رسند؛ این تابع 
reply.md:870:reply.md:712:reply.md:551:reply.md:386:reply.md:196:`service.py::ingest_codal_report` → RawFinancialFact.
reply.md:871:reply.md:713:reply.md:553:`codal/ingestion.py::ingest_codal_report` 
reply.md:872:reply.md:714:reply.md:554:reply.md:389:reply.md:198:است و به writer مرکزی 
`service.py::ingest_codal_report` می‌رسد.
reply.md:873:reply.md:715:reply.md:556:`codal/ingestion.py::ingest_codal_pdf` 
reply.md:874:reply.md:716:reply.md:558:`codal/pipeline.py::load_codal_pdf` و 
reply.md:875:reply.md:717:reply.md:559:reply.md:393:reply.md:203:`load_codal_pdf_from_url` 
acquisition/extraction/validation را پیش 
reply.md:877:reply.md:719:reply.md:562:`reports.financial_period_id`، چون پیش 
reply.md:878:reply.md:720:reply.md:563:reply.md:397:reply.md:210:`reports.financial_period_id` و تفکیک قرارداد legacy 
CODAL از 
reply.md:880:reply.md:721:reply.md:565:`Report.financial_period_id` در ORM 
reply.md:881:reply.md:722:reply.md:566:reply.md:400:reply.md:214:`service.py::ingest_codal_report` delegate می‌کند؛ 
PDF wrapper پس 
reply.md:883:reply.md:725:`financial_period_id` در 
reply.md:884:reply.md:727:`reports.financial_period_id` اشاره 
reply.md:885:reply.md:728:reply.md:571:reply.md:406:reply.md:221:`Report.financial_period_id` مجاز نیست. مسیر جدید 
Excel باید دوره 
reply.md:887:reply.md:730:reply.md:573:reply.md:408:reply.md:227:`report_versions.report_id` و 
`financial_periods.company_id` تا 
reply.md:889:reply.md:732:reply.md:575:reply.md:410:reply.md:228:`Report.financial_period_id` به‌صورت optional 
metadata باقی ماند، 
reply.md:891:reply.md:734:reply.md:577:reply.md:412:reply.md:230:writer قدیمی به Report.financial_period_id — 
2026-11-18
reply.md:892:reply.md:735:reply.md:579:`service.py::ingest_codal_report` writer 
reply.md:893:reply.md:736:reply.md:580:reply.md:415:reply.md:234:`Report.financial_period_id` باید با ورودی یکسان 
باشند؛ در غیر این 
reply.md:895:reply.md:738:reply.md:581:reply.md:416:reply.md:236:`ingest_codal_report` take DTOs |
reply.md:896:reply.md:739:reply.md:582:reply.md:418:`ingest_codal_report` accepts 
reply.md:897:reply.md:740:reply.md:583:reply.md:419:reply.md:239:prompts\10_Implementation_Status.md:243:ingest_codal_r
eport()
reply.md:898:reply.md:741:reply.md:584:reply.md:420:reply.md:240:src\tests\final_validation_audit.md:140:  → 
ingest_codal_report()
reply.md:899:reply.md:742:reply.md:585:reply.md:421:reply.md:241:src\tests\golden_audit_source_plan.md:15:ingest_codal_
report()
reply.md:900:reply.md:743:reply.md:586:reply.md:423:ingest_codal_report()
reply.md:901:reply.md:744:reply.md:587:reply.md:424:reply.md:243:01_Stage1_Data_Foundation.md:278:financial_period_id
reply.md:902:reply.md:745:reply.md:588:reply.md:425:reply.md:246:(models cover industries/companies, 
financial_periods, 
reply.md:906:reply.md:748:reply.md:590:reply.md:428:ingest_codal_report()`
reply.md:909:reply.md:750:reply.md:592:reply.md:430:reply.md:256:12_Database_Architecture_V1.1.md:104:- 
`financial_periods`
reply.md:910:reply.md:751:reply.md:593:reply.md:431:reply.md:257:12_Database_Architecture_V1.1.md:801:ingest_codal_repo
rt / 
reply.md:912:reply.md:753:reply.md:594:reply.md:432:reply.md:259:consumed by `ingest_codal_report`; the existing 
downstream 
reply.md:914:reply.md:755:reply.md:595:reply.md:434:reply.md:260:99_Architecture_Change_Log.md:386:  
ingest_codal_report / 
reply.md:916:reply.md:757:reply.md:596:reply.md:435:reply.md:262:is a **pre-ingestion** responsibility. 
`ingest_codal_report` 
reply.md:918:reply.md:759:reply.md:598:reply.md:437:reply.md:265:PROJECT_HANDOFF_INSTRUCTIONS.md:252:    
ingest_codal_report()
reply.md:919:reply.md:761:`ingest_codal_report()` 
reply.md:921:`ingest_codal_report`، 
reply.md:922:reply.md:764:reply.md:603:reply.md:441:reply.md:269:reply.md:10:از `load_codal_pdf` و PDFهای fixture 
استفاده می‌کند.
reply.md:923:reply.md:765:reply.md:604:reply.md:443:`ingest_codal_report()`:
reply.md:924:reply.md:766:reply.md:605:reply.md:444:reply.md:271:reply.md:13:`financial_period_id` است، درحالی‌که 
قرارداد منطقی 
reply.md:926:reply.md:768:reply.md:607:reply.md:447:`ingest_codal_report()` 
reply.md:927:reply.md:769:reply.md:608:reply.md:448:reply.md:276:`ingest_codal_report`
reply.md:928:reply.md:770:reply.md:609:reply.md:449:reply.md:277:reply.md:19:`src/ingestion/codal/ingestion.py::ingest_
codal_report`
reply.md:930:reply.md:772:reply.md:611:reply.md:450:reply.md:278:reply.md:20:`src/ingestion/service.py::ingest_codal_re
port` 
reply.md:932:reply.md:774:reply.md:613:reply.md:451:reply.md:279:reply.md:22:`src/ingestion/codal/ingestion.py::ingest_
codal_pdf` 
reply.md:934:reply.md:776:reply.md:615:reply.md:453:reply.md:281:reply.md:26:`src/ingestion/codal/pipeline.py::load_cod
al_pdf` و 
reply.md:935:reply.md:777:`load_codal_pdf_from_url` 
reply.md:936:reply.md:778:reply.md:617:reply.md:455:reply.md:283:reply.md:30:`src/ingestion/service.py::ingest_codal_re
port` writer 
reply.md:938:reply.md:779:reply.md:618:reply.md:457:reply.md:285:reply.md:36:`reports.financial_period_id` پیش از 
nullable 
reply.md:940:reply.md:781:reply.md:619:reply.md:459:reply.md:286:reply.md:39:`reports.financial_period_id` و مسیرهای 
فراخوانی CODAL 
reply.md:942:reply.md:782:reply.md:620:reply.md:460:reply.md:287:reply.md:41:`financial_period_id|FinancialPeriod` در 
کل فایل‌های 
reply.md:944:reply.md:784:reply.md:622:reply.md:462:reply.md:289:reply.md:43:`Report.financial_period_id` با 
`nullable=False` و FK 
reply.md:946:reply.md:785:reply.md:623:`financial_periods.period_id`.
reply.md:947:reply.md:786:reply.md:624:reply.md:463:reply.md:290:reply.md:46:`Report.financial_period_id` استفاده نشده 
است.
reply.md:948:reply.md:787:reply.md:625:reply.md:464:reply.md:291:reply.md:48:تست‌های Stage 5/6: نام 
`financial_period_id` در DTOها 
reply.md:950:reply.md:790:`reports.financial_period_id` 
reply.md:951:reply.md:791:reply.md:629:reply.md:466:reply.md:294:reply.md:51:Report و قرارداد قدیمی را با 
`financial_period_id` 
reply.md:953:reply.md:793:reply.md:631:reply.md:468:reply.md:296:reply.md:54:تابع عمومی `ingest_codal_report` یک 
facade سازگار با 
reply.md:955:reply.md:794:reply.md:632:reply.md:469:reply.md:297:`src.ingestion.service.ingest_codal_report` 
reply.md:956:reply.md:795:reply.md:633:reply.md:470:reply.md:298:reply.md:55:delegate می‌کند. تابع `ingest_codal_pdf` 
پس از 
reply.md:958:reply.md:797:reply.md:635:reply.md:471:reply.md:299:reply.md:57:توابع `load_codal_pdf` و 
`load_codal_pdf_from_url` پس 
reply.md:960:reply.md:798:reply.md:637:reply.md:473:reply.md:300:reply.md:58:`src.ingestion.service.ingest_codal_report
` را 
reply.md:962:reply.md:799:reply.md:638:reply.md:474:reply.md:301:reply.md:61:`financial_period_id` ندارند؛ این با 
یافتهٔ قبلی 
reply.md:964:reply.md:801:reply.md:640:reply.md:476:reply.md:304:`Report.financial_period_id` در 
reply.md:965:reply.md:802:reply.md:641:reply.md:477:reply.md:305:reply.md:68:`Report.financial_period_id` تا زمان 
تعیین تکلیف و 
reply.md:967:reply.md:804:reply.md:643:reply.md:479:reply.md:307:reply.md:71:Report.financial_period_id و مرز writer 
قدیمی — 
reply.md:970:`src/ingestion/service.py::ingest_codal_report` است؛ 
reply.md:971:reply.md:807:reply.md:645:reply.md:482:reply.md:310:reply.md:76:`Report.financial_period_id` با ورودی 
مقایسه می‌شوند؛ 
reply.md:973:reply.md:809:reply.md:647:reply.md:483:reply.md:311:reply.md:78:`financial_period_id=period_id` ثبت 
می‌شود.
reply.md:974:reply.md:810:reply.md:648:reply.md:484:reply.md:312:reply.md:80:Report.financial_period_id (حذف تدریجی، 
nullable و 
reply.md:977:`financial_period_id` | 
reply.md:978:reply.md:814:reply.md:652:reply.md:488:reply.md:317:`financial_periods` 
reply.md:979:reply.md:815:reply.md:653:reply.md:490:`ingest_codal_report(...)` creates 
reply.md:980:reply.md:818:reply.md:656:reply.md:492:load_codal_pdf_from_url 
reply.md:981:reply.md:819:reply.md:658:ingest_codal_report  
reply.md:982:reply.md:820:reply.md:659:reply.md:494:reply.md:323:reply.md:93:ingest_codal_pdf و facade سازگاری 
ingest_codal_report 
reply.md:984:reply.md:822:reply.md:661:reply.md:495:reply.md:325:src/ingestion/service.py::ingest_codal_report | 
reply.md:985:reply.md:823:reply.md:662:reply.md:497:`service.py::ingest_codal_report`: 
reply.md:986:reply.md:824:reply.md:664:financial_period_id 
reply.md:987:reply.md:825:reply.md:665:reply.md:501:financial_period_id در مدل فعلی 
reply.md:988:reply.md:826:reply.md:666:reply.md:502:reply.md:332:reply.md:105:`src/ingestion/service.py::ingest_codal_r
eport`:
reply.md:989:reply.md:827:reply.md:667:reply.md:504:ingest_codal_report
reply.md:990:reply.md:828:reply.md:668:reply.md:506:`financial_periods` — 
reply.md:991:reply.md:830:`reports.financial_period_id` must not be 
reply.md:992:reply.md:831:reply.md:671:reply.md:509:reply.md:339:`financial_periods` model 
reply.md:994:`reports.financial_period_id` 
reply.md:995:reply.md:834:reply.md:674:reply.md:511:reply.md:341:reply.md:118:`financial_period_id` را جداگانه نگه 
می‌دارد؛ FKها 
reply.md:998:`financial_periods.company_id` تا 
reply.md:999:reply.md:838:reply.md:678:reply.md:515:reply.md:346:`Report.financial_period_id` در مدل 
reply.md:1000:reply.md:839:reply.md:679:reply.md:516:reply.md:347:reply.md:127:pipelineهای load_codal_pdf و 
load_codal_pdf_from_url |
reply.md:1001:reply.md:840:reply.md:680:reply.md:517:reply.md:349:\`src/ingestion/service.py::ingest_codal_report\` | 
reply.md:1002:reply.md:842:ingest_codal_report 
reply.md:1003:reply.md:843:reply.md:683:reply.md:520:reply.md:351:reply.md:134:RawLineInput و ingest_codal_report 
فعلاً حفظ؛ بعداً 
reply.md:1005:reply.md:845:reply.md:685:reply.md:523:\`ingest_codal_report\` را 
reply.md:1006:reply.md:846:reply.md:686:reply.md:524:reply.md:355:`service.py::ingest_codal_report` | 
reply.md:1007:reply.md:847:reply.md:687:reply.md:525:reply.md:357:`codal/ingestion.py::ingest_codal_pdf` و 
reply.md:1008:reply.md:848:reply.md:688:reply.md:526:reply.md:358:reply.md:146:`ingestion/service.py::ingest_codal_repo
rt` (تابع 
reply.md:1010:reply.md:850:reply.md:689:reply.md:528:reply.md:360:reply.md:150:`ingest_codal_report` و Stage 5 query | 
Stage 5 
reply.md:1012:reply.md:852:reply.md:691:reply.md:530:reply.md:363:`ingest_codal_report` 
reply.md:1013:reply.md:853:reply.md:692:reply.md:531:reply.md:365:`financial_period_id` 
reply.md:1014:reply.md:854:reply.md:693:reply.md:532:reply.md:367:`financial_periods` |
reply.md:1015:reply.md:855:reply.md:695:`Report.financial_period_id` 
reply.md:1016:reply.md:856:reply.md:696:reply.md:535:reply.md:369:reply.md:161:`ingest_codal_report` یک period_id واحد 
را به تمام 
reply.md:1017:reply.md:858:reply.md:698:reply.md:537:reply.md:370:reply.md:163:`src/ingestion/service.py::ingest_codal_
report`؛ 
reply.md:1019:reply.md:859:reply.md:700:`financial_periods` | در مسیر 
reply.md:1020:reply.md:860:reply.md:701:reply.md:542:`Report.financial_period_id` 
reply.md:1021:reply.md:861:reply.md:702:reply.md:543:reply.md:376:reply.md:175:محدودیت را دارد. متد 
`ingest_codal_report` یک 
reply.md:1023:reply.md:863:reply.md:705:`Report.financial_period_id` 
reply.md:1025:`Report.financial_period_id` 
reply.md:1026:reply.md:866:reply.md:708:reply.md:548:reply.md:382:reply.md:185:`src/ingestion/service.py::ingest_codal_
report` 
reply.md:1028:reply.md:868:reply.md:710:reply.md:550:reply.md:384:reply.md:191:`src/ingestion/service.py::ingest_codal_
report` 
reply.md:1030:reply.md:870:reply.md:712:reply.md:551:reply.md:386:reply.md:196:`service.py::ingest_codal_report` → 
RawFinancialFact.
reply.md:1031:reply.md:871:reply.md:713:reply.md:553:`codal/ingestion.py::ingest_codal_report` 
reply.md:1033:`service.py::ingest_codal_report` می‌رسد.
reply.md:1034:reply.md:873:reply.md:715:reply.md:556:`codal/ingestion.py::ingest_codal_pdf` 
reply.md:1035:reply.md:874:reply.md:716:reply.md:558:`codal/pipeline.py::load_codal_pdf` و 
reply.md:1036:reply.md:875:reply.md:717:reply.md:559:reply.md:393:reply.md:203:`load_codal_pdf_from_url` 
reply.md:1038:reply.md:877:reply.md:719:reply.md:562:`reports.financial_period_id`، چون پیش 
reply.md:1039:reply.md:878:reply.md:720:reply.md:563:reply.md:397:reply.md:210:`reports.financial_period_id` و تفکیک 
قرارداد legacy 
reply.md:1041:reply.md:880:reply.md:721:reply.md:565:`Report.financial_period_id` در ORM 
reply.md:1042:reply.md:881:reply.md:722:reply.md:566:reply.md:400:reply.md:214:`service.py::ingest_codal_report` 
delegate می‌کند؛ 
reply.md:1044:reply.md:883:reply.md:725:`financial_period_id` در 
reply.md:1045:reply.md:884:reply.md:727:`reports.financial_period_id` اشاره 
reply.md:1046:reply.md:885:reply.md:728:reply.md:571:reply.md:406:reply.md:221:`Report.financial_period_id` مجاز نیست. 
مسیر جدید 
reply.md:1049:`financial_periods.company_id` تا 
reply.md:1050:reply.md:889:reply.md:732:reply.md:575:reply.md:410:reply.md:228:`Report.financial_period_id` به‌صورت 
optional 
reply.md:1052:reply.md:891:reply.md:734:reply.md:577:reply.md:412:reply.md:230:writer قدیمی به 
Report.financial_period_id — 
reply.md:1054:reply.md:892:reply.md:735:reply.md:579:`service.py::ingest_codal_report` writer 
reply.md:1055:reply.md:893:reply.md:736:reply.md:580:reply.md:415:reply.md:234:`Report.financial_period_id` باید با 
ورودی یکسان 
reply.md:1057:reply.md:895:reply.md:738:reply.md:581:reply.md:416:reply.md:236:`ingest_codal_report` take DTOs |
reply.md:1058:reply.md:896:reply.md:739:reply.md:582:reply.md:418:`ingest_codal_report` accepts 
reply.md:1062:ingest_codal_report()
reply.md:1065:reply.md:900:reply.md:743:reply.md:586:reply.md:423:ingest_codal_report()
reply.md:1066:reply.md:901:reply.md:744:reply.md:587:reply.md:424:reply.md:243:01_Stage1_Data_Foundation.md:278:financi
al_period_id
reply.md:1068:financial_periods, 
reply.md:1069:reply.md:906:reply.md:748:reply.md:590:reply.md:428:ingest_codal_report()`
reply.md:1071:`financial_periods`
reply.md:1074:reply.md:912:reply.md:753:reply.md:594:reply.md:432:reply.md:259:consumed by `ingest_codal_report`; the 
existing 
reply.md:1077:ingest_codal_report / 
reply.md:1079:`ingest_codal_report` 
reply.md:1081:ingest_codal_report()
reply.md:1082:reply.md:919:reply.md:761:`ingest_codal_report()` 
reply.md:1083:reply.md:921:`ingest_codal_report`، 
reply.md:1084:reply.md:922:reply.md:764:reply.md:603:reply.md:441:reply.md:269:reply.md:10:از `load_codal_pdf` و 
PDFهای fixture 
reply.md:1086:reply.md:923:reply.md:765:reply.md:604:reply.md:443:`ingest_codal_report()`:
reply.md:1087:reply.md:924:reply.md:766:reply.md:605:reply.md:444:reply.md:271:reply.md:13:`financial_period_id` است، 
درحالی‌که 
reply.md:1089:reply.md:926:reply.md:768:reply.md:607:reply.md:447:`ingest_codal_report()` 
reply.md:1090:reply.md:927:reply.md:769:reply.md:608:reply.md:448:reply.md:276:`ingest_codal_report`
reply.md:1099:reply.md:935:reply.md:777:`load_codal_pdf_from_url` 
reply.md:1102:reply.md:938:reply.md:779:reply.md:618:reply.md:457:reply.md:285:reply.md:36:`reports.financial_period_id
` پیش از 
reply.md:1104:reply.md:940:reply.md:781:reply.md:619:reply.md:459:reply.md:286:reply.md:39:`reports.financial_period_id
` و مسیرهای 
reply.md:1106:reply.md:942:reply.md:782:reply.md:620:reply.md:460:reply.md:287:reply.md:41:`financial_period_id|Financi
alPeriod` در 
reply.md:1108:reply.md:944:reply.md:784:reply.md:622:reply.md:462:reply.md:289:reply.md:43:`Report.financial_period_id`
 با 
reply.md:1110:reply.md:946:reply.md:785:reply.md:623:`financial_periods.period_id`.
reply.md:1111:reply.md:947:reply.md:786:reply.md:624:reply.md:463:reply.md:290:reply.md:46:`Report.financial_period_id`
 استفاده نشده 
reply.md:1114:`financial_period_id` در DTOها 
reply.md:1115:reply.md:950:reply.md:790:`reports.financial_period_id` 
reply.md:1117:`financial_period_id` 
reply.md:1118:reply.md:953:reply.md:793:reply.md:631:reply.md:468:reply.md:296:reply.md:54:تابع عمومی 
`ingest_codal_report` یک 
reply.md:1120:reply.md:955:reply.md:794:reply.md:632:reply.md:469:reply.md:297:`src.ingestion.service.ingest_codal_repo
rt` 
reply.md:1121:reply.md:956:reply.md:795:reply.md:633:reply.md:470:reply.md:298:reply.md:55:delegate می‌کند. تابع 
`ingest_codal_pdf` 
reply.md:1123:reply.md:958:reply.md:797:reply.md:635:reply.md:471:reply.md:299:reply.md:57:توابع `load_codal_pdf` و 
reply.md:1124:`load_codal_pdf_from_url` پس 
reply.md:1125:reply.md:960:reply.md:798:reply.md:637:reply.md:473:reply.md:300:reply.md:58:`src.ingestion.service.inges
t_codal_report
reply.md:1127:reply.md:962:reply.md:799:reply.md:638:reply.md:474:reply.md:301:reply.md:61:`financial_period_id` 
ندارند؛ این با 
reply.md:1129:reply.md:964:reply.md:801:reply.md:640:reply.md:476:reply.md:304:`Report.financial_period_id` در 
reply.md:1130:reply.md:965:reply.md:802:reply.md:641:reply.md:477:reply.md:305:reply.md:68:`Report.financial_period_id`
 تا زمان 
reply.md:1132:reply.md:967:reply.md:804:reply.md:643:reply.md:479:reply.md:307:reply.md:71:Report.financial_period_id 
و مرز writer 
reply.md:1134:reply.md:970:`src/ingestion/service.py::ingest_codal_report` است؛ 
reply.md:1135:reply.md:971:reply.md:807:reply.md:645:reply.md:482:reply.md:310:reply.md:76:`Report.financial_period_id`
 با ورودی 
reply.md:1137:reply.md:973:reply.md:809:reply.md:647:reply.md:483:reply.md:311:reply.md:78:`financial_period_id=period_
id` ثبت 
reply.md:1139:reply.md:974:reply.md:810:reply.md:648:reply.md:484:reply.md:312:reply.md:80:Report.financial_period_id 
(حذف تدریجی، 
reply.md:1141:reply.md:977:`financial_period_id` | 
reply.md:1142:reply.md:978:reply.md:814:reply.md:652:reply.md:488:reply.md:317:`financial_periods` 
reply.md:1143:reply.md:979:reply.md:815:reply.md:653:reply.md:490:`ingest_codal_report(...)` creates 
reply.md:1144:reply.md:980:reply.md:818:reply.md:656:reply.md:492:load_codal_pdf_from_url 
reply.md:1145:reply.md:981:reply.md:819:reply.md:658:ingest_codal_report  
reply.md:1146:reply.md:982:reply.md:820:reply.md:659:reply.md:494:reply.md:323:reply.md:93:ingest_codal_pdf و facade 
سازگاری 
reply.md:1147:ingest_codal_report 
reply.md:1148:reply.md:984:reply.md:822:reply.md:661:reply.md:495:reply.md:325:src/ingestion/service.py::ingest_codal_r
eport | 
reply.md:1149:reply.md:985:reply.md:823:reply.md:662:reply.md:497:`service.py::ingest_codal_report`: 
reply.md:1150:reply.md:986:reply.md:824:reply.md:664:financial_period_id 
reply.md:1151:reply.md:987:reply.md:825:reply.md:665:reply.md:501:financial_period_id در مدل فعلی 
reply.md:1154:reply.md:989:reply.md:827:reply.md:667:reply.md:504:ingest_codal_report
reply.md:1155:reply.md:990:reply.md:828:reply.md:668:reply.md:506:`financial_periods` — 
reply.md:1156:reply.md:991:reply.md:830:`reports.financial_period_id` must not be 
reply.md:1157:reply.md:992:reply.md:831:reply.md:671:reply.md:509:reply.md:339:`financial_periods` model 
reply.md:1158:reply.md:994:`reports.financial_period_id` 
reply.md:1159:reply.md:995:reply.md:834:reply.md:674:reply.md:511:reply.md:341:reply.md:118:`financial_period_id` را 
جداگانه نگه 
reply.md:1161:reply.md:998:`financial_periods.company_id` تا 
reply.md:1162:reply.md:999:reply.md:838:reply.md:678:reply.md:515:reply.md:346:`Report.financial_period_id` در مدل 
reply.md:1163:reply.md:1000:reply.md:839:reply.md:679:reply.md:516:reply.md:347:reply.md:127:pipelineهای 
load_codal_pdf و 
reply.md:1164:load_codal_pdf_from_url |
reply.md:1165:reply.md:1001:reply.md:840:reply.md:680:reply.md:517:reply.md:349:\`src/ingestion/service.py::ingest_coda
l_report\` | 
reply.md:1166:reply.md:1002:reply.md:842:ingest_codal_report 
reply.md:1167:reply.md:1003:reply.md:843:reply.md:683:reply.md:520:reply.md:351:reply.md:134:RawLineInput و 
ingest_codal_report 
reply.md:1169:reply.md:1005:reply.md:845:reply.md:685:reply.md:523:\`ingest_codal_report\` را 
reply.md:1170:reply.md:1006:reply.md:846:reply.md:686:reply.md:524:reply.md:355:`service.py::ingest_codal_report` | 
reply.md:1171:reply.md:1007:reply.md:847:reply.md:687:reply.md:525:reply.md:357:`codal/ingestion.py::ingest_codal_pdf` 
و 
reply.md:1174:reply.md:1010:reply.md:850:reply.md:689:reply.md:528:reply.md:360:reply.md:150:`ingest_codal_report` و 
Stage 5 query | 
reply.md:1176:reply.md:1012:reply.md:852:reply.md:691:reply.md:530:reply.md:363:`ingest_codal_report` 
reply.md:1177:reply.md:1013:reply.md:853:reply.md:692:reply.md:531:reply.md:365:`financial_period_id` 
reply.md:1178:reply.md:1014:reply.md:854:reply.md:693:reply.md:532:reply.md:367:`financial_periods` |
reply.md:1179:reply.md:1015:reply.md:855:reply.md:695:`Report.financial_period_id` 
reply.md:1180:reply.md:1016:reply.md:856:reply.md:696:reply.md:535:reply.md:369:reply.md:161:`ingest_codal_report` یک 
period_id واحد 
reply.md:1184:reply.md:1019:reply.md:859:reply.md:700:`financial_periods` | در مسیر 
reply.md:1185:reply.md:1020:reply.md:860:reply.md:701:reply.md:542:`Report.financial_period_id` 
reply.md:1187:`ingest_codal_report` یک 
reply.md:1188:reply.md:1023:reply.md:863:reply.md:705:`Report.financial_period_id` 
reply.md:1189:reply.md:1025:`Report.financial_period_id` 
reply.md:1194:reply.md:1030:reply.md:870:reply.md:712:reply.md:551:reply.md:386:reply.md:196:`service.py::ingest_codal_
report` → 
reply.md:1196:reply.md:1031:reply.md:871:reply.md:713:reply.md:553:`codal/ingestion.py::ingest_codal_report` 
reply.md:1197:reply.md:1033:`service.py::ingest_codal_report` می‌رسد.
reply.md:1198:reply.md:1034:reply.md:873:reply.md:715:reply.md:556:`codal/ingestion.py::ingest_codal_pdf` 
reply.md:1199:reply.md:1035:reply.md:874:reply.md:716:reply.md:558:`codal/pipeline.py::load_codal_pdf` و 
reply.md:1200:reply.md:1036:reply.md:875:reply.md:717:reply.md:559:reply.md:393:reply.md:203:`load_codal_pdf_from_url` 
reply.md:1201:reply.md:1038:reply.md:877:reply.md:719:reply.md:562:`reports.financial_period_id`، چون پیش 
reply.md:1202:reply.md:1039:reply.md:878:reply.md:720:reply.md:563:reply.md:397:reply.md:210:`reports.financial_period_
id` و تفکیک 
reply.md:1204:reply.md:1041:reply.md:880:reply.md:721:reply.md:565:`Report.financial_period_id` در ORM 
reply.md:1205:reply.md:1042:reply.md:881:reply.md:722:reply.md:566:reply.md:400:reply.md:214:`service.py::ingest_codal_
report` 
reply.md:1207:reply.md:1044:reply.md:883:reply.md:725:`financial_period_id` در 
reply.md:1208:reply.md:1045:reply.md:884:reply.md:727:`reports.financial_period_id` اشاره 
reply.md:1209:reply.md:1046:reply.md:885:reply.md:728:reply.md:571:reply.md:406:reply.md:221:`Report.financial_period_i
d` مجاز نیست. 
reply.md:1211:reply.md:1049:`financial_periods.company_id` تا 
reply.md:1212:reply.md:1050:reply.md:889:reply.md:732:reply.md:575:reply.md:410:reply.md:228:`Report.financial_period_i
d` به‌صورت 
reply.md:1215:Report.financial_period_id — 
reply.md:1216:reply.md:1054:reply.md:892:reply.md:735:reply.md:579:`service.py::ingest_codal_report` writer 
reply.md:1217:reply.md:1055:reply.md:893:reply.md:736:reply.md:580:reply.md:415:reply.md:234:`Report.financial_period_i
d` باید با 
reply.md:1219:reply.md:1057:reply.md:895:reply.md:738:reply.md:581:reply.md:416:reply.md:236:`ingest_codal_report` 
take DTOs |
reply.md:1220:reply.md:1058:reply.md:896:reply.md:739:reply.md:582:reply.md:418:`ingest_codal_report` accepts 
reply.md:1221:reply.md:1062:ingest_codal_report()
reply.md:1222:reply.md:1065:reply.md:900:reply.md:743:reply.md:586:reply.md:423:ingest_codal_report()
reply.md:1225:reply.md:1068:financial_periods, 
reply.md:1226:reply.md:1069:reply.md:906:reply.md:748:reply.md:590:reply.md:428:ingest_codal_report()`
reply.md:1227:reply.md:1071:`financial_periods`
reply.md:1228:reply.md:1074:reply.md:912:reply.md:753:reply.md:594:reply.md:432:reply.md:259:consumed by 
`ingest_codal_report`; the 
reply.md:1230:reply.md:1077:ingest_codal_report / 
reply.md:1231:reply.md:1079:`ingest_codal_report` 
reply.md:1232:reply.md:1081:ingest_codal_report()
reply.md:1233:reply.md:1082:reply.md:919:reply.md:761:`ingest_codal_report()` 
reply.md:1234:reply.md:1083:reply.md:921:`ingest_codal_report`، 
reply.md:1235:reply.md:1084:reply.md:922:reply.md:764:reply.md:603:reply.md:441:reply.md:269:reply.md:10:از 
`load_codal_pdf` و 
reply.md:1237:reply.md:1086:reply.md:923:reply.md:765:reply.md:604:reply.md:443:`ingest_codal_report()`:
reply.md:1238:reply.md:1087:reply.md:924:reply.md:766:reply.md:605:reply.md:444:reply.md:271:reply.md:13:`financial_per
iod_id` است، 
reply.md:1240:reply.md:1089:reply.md:926:reply.md:768:reply.md:607:reply.md:447:`ingest_codal_report()` 
reply.md:1241:reply.md:1090:reply.md:927:reply.md:769:reply.md:608:reply.md:448:reply.md:276:`ingest_codal_report`
reply.md:1242:reply.md:1099:reply.md:935:reply.md:777:`load_codal_pdf_from_url` 
reply.md:1243:reply.md:1102:reply.md:938:reply.md:779:reply.md:618:reply.md:457:reply.md:285:reply.md:36:`reports.finan
cial_period_id
reply.md:1245:reply.md:1104:reply.md:940:reply.md:781:reply.md:619:reply.md:459:reply.md:286:reply.md:39:`reports.finan
cial_period_id
reply.md:1247:reply.md:1106:reply.md:942:reply.md:782:reply.md:620:reply.md:460:reply.md:287:reply.md:41:`financial_per
iod_id|Financi
reply.md:1249:reply.md:1108:reply.md:944:reply.md:784:reply.md:622:reply.md:462:reply.md:289:reply.md:43:`Report.financ
ial_period_id`
reply.md:1251:reply.md:1110:reply.md:946:reply.md:785:reply.md:623:`financial_periods.period_id`.
reply.md:1252:reply.md:1111:reply.md:947:reply.md:786:reply.md:624:reply.md:463:reply.md:290:reply.md:46:`Report.financ
ial_period_id`
reply.md:1254:reply.md:1114:`financial_period_id` در DTOها 
reply.md:1255:reply.md:1115:reply.md:950:reply.md:790:`reports.financial_period_id` 
reply.md:1256:reply.md:1117:`financial_period_id` 
reply.md:1258:`ingest_codal_report` یک 
reply.md:1262:`ingest_codal_pdf` 
reply.md:1263:reply.md:1123:reply.md:958:reply.md:797:reply.md:635:reply.md:471:reply.md:299:reply.md:57:توابع 
`load_codal_pdf` و 
reply.md:1264:reply.md:1124:`load_codal_pdf_from_url` پس 
reply.md:1267:reply.md:1127:reply.md:962:reply.md:799:reply.md:638:reply.md:474:reply.md:301:reply.md:61:`financial_per
iod_id` 
reply.md:1269:reply.md:1129:reply.md:964:reply.md:801:reply.md:640:reply.md:476:reply.md:304:`Report.financial_period_i
d` در 
reply.md:1270:reply.md:1130:reply.md:965:reply.md:802:reply.md:641:reply.md:477:reply.md:305:reply.md:68:`Report.financ
ial_period_id`
reply.md:1272:reply.md:1132:reply.md:967:reply.md:804:reply.md:643:reply.md:479:reply.md:307:reply.md:71:Report.financi
al_period_id 
reply.md:1274:reply.md:1134:reply.md:970:`src/ingestion/service.py::ingest_codal_report` است؛ 
reply.md:1275:reply.md:1135:reply.md:971:reply.md:807:reply.md:645:reply.md:482:reply.md:310:reply.md:76:`Report.financ
ial_period_id`
reply.md:1277:reply.md:1137:reply.md:973:reply.md:809:reply.md:647:reply.md:483:reply.md:311:reply.md:78:`financial_per
iod_id=period_
reply.md:1279:reply.md:1139:reply.md:974:reply.md:810:reply.md:648:reply.md:484:reply.md:312:reply.md:80:Report.financi
al_period_id 
reply.md:1281:reply.md:1141:reply.md:977:`financial_period_id` | 
reply.md:1282:reply.md:1142:reply.md:978:reply.md:814:reply.md:652:reply.md:488:reply.md:317:`financial_periods` 
reply.md:1283:reply.md:1143:reply.md:979:reply.md:815:reply.md:653:reply.md:490:`ingest_codal_report(...)` creates 
reply.md:1284:reply.md:1144:reply.md:980:reply.md:818:reply.md:656:reply.md:492:load_codal_pdf_from_url 
reply.md:1285:reply.md:1145:reply.md:981:reply.md:819:reply.md:658:ingest_codal_report  
reply.md:1286:reply.md:1146:reply.md:982:reply.md:820:reply.md:659:reply.md:494:reply.md:323:reply.md:93:ingest_codal_p
df و facade 
reply.md:1288:reply.md:1147:ingest_codal_report 
reply.md:1291:reply.md:1149:reply.md:985:reply.md:823:reply.md:662:reply.md:497:`service.py::ingest_codal_report`: 
reply.md:1292:reply.md:1150:reply.md:986:reply.md:824:reply.md:664:financial_period_id 
reply.md:1293:reply.md:1151:reply.md:987:reply.md:825:reply.md:665:reply.md:501:financial_period_id در مدل فعلی 
reply.md:1294:reply.md:1154:reply.md:989:reply.md:827:reply.md:667:reply.md:504:ingest_codal_report
reply.md:1295:reply.md:1155:reply.md:990:reply.md:828:reply.md:668:reply.md:506:`financial_periods` — 
reply.md:1296:reply.md:1156:reply.md:991:reply.md:830:`reports.financial_period_id` must not be 
reply.md:1297:reply.md:1157:reply.md:992:reply.md:831:reply.md:671:reply.md:509:reply.md:339:`financial_periods` model 
reply.md:1298:reply.md:1158:reply.md:994:`reports.financial_period_id` 
reply.md:1299:reply.md:1159:reply.md:995:reply.md:834:reply.md:674:reply.md:511:reply.md:341:reply.md:118:`financial_pe
riod_id` را 
reply.md:1301:reply.md:1161:reply.md:998:`financial_periods.company_id` تا 
reply.md:1302:reply.md:1162:reply.md:999:reply.md:838:reply.md:678:reply.md:515:reply.md:346:`Report.financial_period_i
d` در مدل 
reply.md:1304:load_codal_pdf و 
reply.md:1305:reply.md:1164:load_codal_pdf_from_url |
reply.md:1308:reply.md:1166:reply.md:1002:reply.md:842:ingest_codal_report 
reply.md:1310:ingest_codal_report 
reply.md:1311:reply.md:1169:reply.md:1005:reply.md:845:reply.md:685:reply.md:523:\`ingest_codal_report\` را 
reply.md:1312:reply.md:1170:reply.md:1006:reply.md:846:reply.md:686:reply.md:524:reply.md:355:`service.py::ingest_codal
_report` | 
reply.md:1313:reply.md:1171:reply.md:1007:reply.md:847:reply.md:687:reply.md:525:reply.md:357:`codal/ingestion.py::inge
st_codal_pdf` 
reply.md:1315:reply.md:1174:reply.md:1010:reply.md:850:reply.md:689:reply.md:528:reply.md:360:reply.md:150:`ingest_coda
l_report` و 
reply.md:1317:reply.md:1176:reply.md:1012:reply.md:852:reply.md:691:reply.md:530:reply.md:363:`ingest_codal_report` 
reply.md:1318:reply.md:1177:reply.md:1013:reply.md:853:reply.md:692:reply.md:531:reply.md:365:`financial_period_id` 
reply.md:1319:reply.md:1178:reply.md:1014:reply.md:854:reply.md:693:reply.md:532:reply.md:367:`financial_periods` |
reply.md:1320:reply.md:1179:reply.md:1015:reply.md:855:reply.md:695:`Report.financial_period_id` 
reply.md:1321:reply.md:1180:reply.md:1016:reply.md:856:reply.md:696:reply.md:535:reply.md:369:reply.md:161:`ingest_coda
l_report` یک 
reply.md:1323:reply.md:1184:reply.md:1019:reply.md:859:reply.md:700:`financial_periods` | در مسیر 
reply.md:1324:reply.md:1185:reply.md:1020:reply.md:860:reply.md:701:reply.md:542:`Report.financial_period_id` 
reply.md:1325:reply.md:1187:`ingest_codal_report` یک 
reply.md:1326:reply.md:1188:reply.md:1023:reply.md:863:reply.md:705:`Report.financial_period_id` 
reply.md:1327:reply.md:1189:reply.md:1025:`Report.financial_period_id` 
reply.md:1330:reply.md:1196:reply.md:1031:reply.md:871:reply.md:713:reply.md:553:`codal/ingestion.py::ingest_codal_repo
rt` 
reply.md:1331:reply.md:1197:reply.md:1033:`service.py::ingest_codal_report` می‌رسد.
reply.md:1332:reply.md:1198:reply.md:1034:reply.md:873:reply.md:715:reply.md:556:`codal/ingestion.py::ingest_codal_pdf`
 
reply.md:1333:reply.md:1199:reply.md:1035:reply.md:874:reply.md:716:reply.md:558:`codal/pipeline.py::load_codal_pdf` و 
reply.md:1334:reply.md:1200:reply.md:1036:reply.md:875:reply.md:717:reply.md:559:reply.md:393:reply.md:203:`load_codal_
pdf_from_url` 
reply.md:1335:reply.md:1201:reply.md:1038:reply.md:877:reply.md:719:reply.md:562:`reports.financial_period_id`، چون 
پیش 
reply.md:1338:reply.md:1204:reply.md:1041:reply.md:880:reply.md:721:reply.md:565:`Report.financial_period_id` در ORM 
reply.md:1341:reply.md:1207:reply.md:1044:reply.md:883:reply.md:725:`financial_period_id` در 
reply.md:1342:reply.md:1208:reply.md:1045:reply.md:884:reply.md:727:`reports.financial_period_id` اشاره 
reply.md:1345:reply.md:1211:reply.md:1049:`financial_periods.company_id` تا 
reply.md:1348:reply.md:1215:Report.financial_period_id — 
reply.md:1349:reply.md:1216:reply.md:1054:reply.md:892:reply.md:735:reply.md:579:`service.py::ingest_codal_report` 
writer 
reply.md:1352:reply.md:1219:reply.md:1057:reply.md:895:reply.md:738:reply.md:581:reply.md:416:reply.md:236:`ingest_coda
l_report` 
reply.md:1354:reply.md:1220:reply.md:1058:reply.md:896:reply.md:739:reply.md:582:reply.md:418:`ingest_codal_report` 
accepts 
reply.md:1355:reply.md:1221:reply.md:1062:ingest_codal_report()
reply.md:1356:reply.md:1222:reply.md:1065:reply.md:900:reply.md:743:reply.md:586:reply.md:423:ingest_codal_report()
reply.md:1357:reply.md:1225:reply.md:1068:financial_periods, 
reply.md:1358:reply.md:1226:reply.md:1069:reply.md:906:reply.md:748:reply.md:590:reply.md:428:ingest_codal_report()`
reply.md:1359:reply.md:1227:reply.md:1071:`financial_periods`
reply.md:1361:`ingest_codal_report`; the 
reply.md:1362:reply.md:1230:reply.md:1077:ingest_codal_report / 
reply.md:1363:reply.md:1231:reply.md:1079:`ingest_codal_report` 
reply.md:1364:reply.md:1232:reply.md:1081:ingest_codal_report()
reply.md:1365:reply.md:1233:reply.md:1082:reply.md:919:reply.md:761:`ingest_codal_report()` 
reply.md:1366:reply.md:1234:reply.md:1083:reply.md:921:`ingest_codal_report`، 
reply.md:1368:`load_codal_pdf` و 
reply.md:1369:reply.md:1237:reply.md:1086:reply.md:923:reply.md:765:reply.md:604:reply.md:443:`ingest_codal_report()`:
reply.md:1372:reply.md:1240:reply.md:1089:reply.md:926:reply.md:768:reply.md:607:reply.md:447:`ingest_codal_report()` 
reply.md:1373:reply.md:1241:reply.md:1090:reply.md:927:reply.md:769:reply.md:608:reply.md:448:reply.md:276:`ingest_coda
l_report`
reply.md:1374:reply.md:1242:reply.md:1099:reply.md:935:reply.md:777:`load_codal_pdf_from_url` 
reply.md:1383:reply.md:1251:reply.md:1110:reply.md:946:reply.md:785:reply.md:623:`financial_periods.period_id`.
reply.md:1386:reply.md:1254:reply.md:1114:`financial_period_id` در DTOها 
reply.md:1387:reply.md:1255:reply.md:1115:reply.md:950:reply.md:790:`reports.financial_period_id` 
reply.md:1388:reply.md:1256:reply.md:1117:`financial_period_id` 
reply.md:1389:reply.md:1258:`ingest_codal_report` یک 
reply.md:1390:reply.md:1262:`ingest_codal_pdf` 
reply.md:1392:`load_codal_pdf` و 
reply.md:1393:reply.md:1264:reply.md:1124:`load_codal_pdf_from_url` پس 
reply.md:1402:reply.md:1274:reply.md:1134:reply.md:970:`src/ingestion/service.py::ingest_codal_report` است؛ 
reply.md:1409:reply.md:1281:reply.md:1141:reply.md:977:`financial_period_id` | 
reply.md:1410:reply.md:1282:reply.md:1142:reply.md:978:reply.md:814:reply.md:652:reply.md:488:reply.md:317:`financial_p
eriods` 
reply.md:1411:reply.md:1283:reply.md:1143:reply.md:979:reply.md:815:reply.md:653:reply.md:490:`ingest_codal_report(...)
` creates 
reply.md:1412:reply.md:1284:reply.md:1144:reply.md:980:reply.md:818:reply.md:656:reply.md:492:load_codal_pdf_from_url 
reply.md:1413:reply.md:1285:reply.md:1145:reply.md:981:reply.md:819:reply.md:658:ingest_codal_report  
reply.md:1416:reply.md:1288:reply.md:1147:ingest_codal_report 
reply.md:1417:reply.md:1291:reply.md:1149:reply.md:985:reply.md:823:reply.md:662:reply.md:497:`service.py::ingest_codal
_report`: 
reply.md:1418:reply.md:1292:reply.md:1150:reply.md:986:reply.md:824:reply.md:664:financial_period_id 
reply.md:1419:reply.md:1293:reply.md:1151:reply.md:987:reply.md:825:reply.md:665:reply.md:501:financial_period_id در 
مدل فعلی 
reply.md:1420:reply.md:1294:reply.md:1154:reply.md:989:reply.md:827:reply.md:667:reply.md:504:ingest_codal_report
reply.md:1421:reply.md:1295:reply.md:1155:reply.md:990:reply.md:828:reply.md:668:reply.md:506:`financial_periods` — 
reply.md:1422:reply.md:1296:reply.md:1156:reply.md:991:reply.md:830:`reports.financial_period_id` must not be 
reply.md:1423:reply.md:1297:reply.md:1157:reply.md:992:reply.md:831:reply.md:671:reply.md:509:reply.md:339:`financial_p
eriods` model 
reply.md:1424:reply.md:1298:reply.md:1158:reply.md:994:`reports.financial_period_id` 
reply.md:1427:reply.md:1301:reply.md:1161:reply.md:998:`financial_periods.company_id` تا 
reply.md:1430:reply.md:1304:load_codal_pdf و 
reply.md:1431:reply.md:1305:reply.md:1164:load_codal_pdf_from_url |
reply.md:1432:reply.md:1308:reply.md:1166:reply.md:1002:reply.md:842:ingest_codal_report 
reply.md:1433:reply.md:1310:ingest_codal_report 
reply.md:1434:reply.md:1311:reply.md:1169:reply.md:1005:reply.md:845:reply.md:685:reply.md:523:\`ingest_codal_report\` 
را 
reply.md:1441:reply.md:1317:reply.md:1176:reply.md:1012:reply.md:852:reply.md:691:reply.md:530:reply.md:363:`ingest_cod
al_report` 
reply.md:1442:reply.md:1318:reply.md:1177:reply.md:1013:reply.md:853:reply.md:692:reply.md:531:reply.md:365:`financial_
period_id` 
reply.md:1443:reply.md:1319:reply.md:1178:reply.md:1014:reply.md:854:reply.md:693:reply.md:532:reply.md:367:`financial_
periods` |
reply.md:1444:reply.md:1320:reply.md:1179:reply.md:1015:reply.md:855:reply.md:695:`Report.financial_period_id` 
reply.md:1447:reply.md:1323:reply.md:1184:reply.md:1019:reply.md:859:reply.md:700:`financial_periods` | در مسیر 
reply.md:1448:reply.md:1324:reply.md:1185:reply.md:1020:reply.md:860:reply.md:701:reply.md:542:`Report.financial_period
_id` 
reply.md:1449:reply.md:1325:reply.md:1187:`ingest_codal_report` یک 
reply.md:1450:reply.md:1326:reply.md:1188:reply.md:1023:reply.md:863:reply.md:705:`Report.financial_period_id` 
reply.md:1451:reply.md:1327:reply.md:1189:reply.md:1025:`Report.financial_period_id` 
reply.md:1454:reply.md:1331:reply.md:1197:reply.md:1033:`service.py::ingest_codal_report` می‌رسد.
reply.md:1455:reply.md:1332:reply.md:1198:reply.md:1034:reply.md:873:reply.md:715:reply.md:556:`codal/ingestion.py::ing
est_codal_pdf`
reply.md:1457:reply.md:1333:reply.md:1199:reply.md:1035:reply.md:874:reply.md:716:reply.md:558:`codal/pipeline.py::load
_codal_pdf` و 
reply.md:1460:reply.md:1335:reply.md:1201:reply.md:1038:reply.md:877:reply.md:719:reply.md:562:`reports.financial_perio
d_id`، چون 
reply.md:1462:reply.md:1338:reply.md:1204:reply.md:1041:reply.md:880:reply.md:721:reply.md:565:`Report.financial_period
_id` در ORM 
reply.md:1463:reply.md:1341:reply.md:1207:reply.md:1044:reply.md:883:reply.md:725:`financial_period_id` در 
reply.md:1464:reply.md:1342:reply.md:1208:reply.md:1045:reply.md:884:reply.md:727:`reports.financial_period_id` اشاره 
reply.md:1465:reply.md:1345:reply.md:1211:reply.md:1049:`financial_periods.company_id` تا 
reply.md:1466:reply.md:1348:reply.md:1215:Report.financial_period_id — 
reply.md:1467:reply.md:1349:reply.md:1216:reply.md:1054:reply.md:892:reply.md:735:reply.md:579:`service.py::ingest_coda
l_report` 
reply.md:1471:reply.md:1354:reply.md:1220:reply.md:1058:reply.md:896:reply.md:739:reply.md:582:reply.md:418:`ingest_cod
al_report` 
reply.md:1473:reply.md:1355:reply.md:1221:reply.md:1062:ingest_codal_report()
reply.md:1474:reply.md:1356:reply.md:1222:reply.md:1065:reply.md:900:reply.md:743:reply.md:586:reply.md:423:ingest_coda
l_report()
reply.md:1475:reply.md:1357:reply.md:1225:reply.md:1068:financial_periods, 
reply.md:1476:reply.md:1358:reply.md:1226:reply.md:1069:reply.md:906:reply.md:748:reply.md:590:reply.md:428:ingest_coda
l_report()`
reply.md:1477:reply.md:1359:reply.md:1227:reply.md:1071:`financial_periods`
reply.md:1478:reply.md:1361:`ingest_codal_report`; the 
reply.md:1479:reply.md:1362:reply.md:1230:reply.md:1077:ingest_codal_report / 
reply.md:1480:reply.md:1363:reply.md:1231:reply.md:1079:`ingest_codal_report` 
reply.md:1481:reply.md:1364:reply.md:1232:reply.md:1081:ingest_codal_report()
reply.md:1482:reply.md:1365:reply.md:1233:reply.md:1082:reply.md:919:reply.md:761:`ingest_codal_report()` 
reply.md:1483:reply.md:1366:reply.md:1234:reply.md:1083:reply.md:921:`ingest_codal_report`، 
reply.md:1484:reply.md:1368:`load_codal_pdf` و 
reply.md:1485:reply.md:1369:reply.md:1237:reply.md:1086:reply.md:923:reply.md:765:reply.md:604:reply.md:443:`ingest_cod
al_report()`:
reply.md:1486:reply.md:1372:reply.md:1240:reply.md:1089:reply.md:926:reply.md:768:reply.md:607:reply.md:447:`ingest_cod
al_report()` 
reply.md:1489:reply.md:1374:reply.md:1242:reply.md:1099:reply.md:935:reply.md:777:`load_codal_pdf_from_url` 
reply.md:1490:reply.md:1383:reply.md:1251:reply.md:1110:reply.md:946:reply.md:785:reply.md:623:`financial_periods.perio
d_id`.
reply.md:1491:reply.md:1386:reply.md:1254:reply.md:1114:`financial_period_id` در DTOها 
reply.md:1492:reply.md:1387:reply.md:1255:reply.md:1115:reply.md:950:reply.md:790:`reports.financial_period_id` 
reply.md:1493:reply.md:1388:reply.md:1256:reply.md:1117:`financial_period_id` 
reply.md:1494:reply.md:1389:reply.md:1258:`ingest_codal_report` یک 
reply.md:1495:reply.md:1390:reply.md:1262:`ingest_codal_pdf` 
reply.md:1496:reply.md:1392:`load_codal_pdf` و 
reply.md:1497:reply.md:1393:reply.md:1264:reply.md:1124:`load_codal_pdf_from_url` پس 
reply.md:1498:reply.md:1402:reply.md:1274:reply.md:1134:reply.md:970:`src/ingestion/service.py::ingest_codal_report` 
است؛ 
reply.md:1499:reply.md:1409:reply.md:1281:reply.md:1141:reply.md:977:`financial_period_id` | 
reply.md:1502:reply.md:1411:reply.md:1283:reply.md:1143:reply.md:979:reply.md:815:reply.md:653:reply.md:490:`ingest_cod
al_report(...)
reply.md:1504:reply.md:1412:reply.md:1284:reply.md:1144:reply.md:980:reply.md:818:reply.md:656:reply.md:492:load_codal_
pdf_from_url 
reply.md:1505:reply.md:1413:reply.md:1285:reply.md:1145:reply.md:981:reply.md:819:reply.md:658:ingest_codal_report  
reply.md:1506:reply.md:1416:reply.md:1288:reply.md:1147:ingest_codal_report 
reply.md:1509:reply.md:1418:reply.md:1292:reply.md:1150:reply.md:986:reply.md:824:reply.md:664:financial_period_id 
reply.md:1510:reply.md:1419:reply.md:1293:reply.md:1151:reply.md:987:reply.md:825:reply.md:665:reply.md:501:financial_p
eriod_id در 
reply.md:1512:reply.md:1420:reply.md:1294:reply.md:1154:reply.md:989:reply.md:827:reply.md:667:reply.md:504:ingest_coda
l_report
reply.md:1513:reply.md:1421:reply.md:1295:reply.md:1155:reply.md:990:reply.md:828:reply.md:668:reply.md:506:`financial_
periods` — 
reply.md:1514:reply.md:1422:reply.md:1296:reply.md:1156:reply.md:991:reply.md:830:`reports.financial_period_id` must 
not be 
reply.md:1517:reply.md:1424:reply.md:1298:reply.md:1158:reply.md:994:`reports.financial_period_id` 
reply.md:1518:reply.md:1427:reply.md:1301:reply.md:1161:reply.md:998:`financial_periods.company_id` تا 
reply.md:1519:reply.md:1430:reply.md:1304:load_codal_pdf و 
reply.md:1520:reply.md:1431:reply.md:1305:reply.md:1164:load_codal_pdf_from_url |
reply.md:1521:reply.md:1432:reply.md:1308:reply.md:1166:reply.md:1002:reply.md:842:ingest_codal_report 
reply.md:1522:reply.md:1433:reply.md:1310:ingest_codal_report 
reply.md:1523:reply.md:1434:reply.md:1311:reply.md:1169:reply.md:1005:reply.md:845:reply.md:685:reply.md:523:\`ingest_c
odal_report\` 
reply.md:1531:reply.md:1444:reply.md:1320:reply.md:1179:reply.md:1015:reply.md:855:reply.md:695:`Report.financial_perio
d_id` 
reply.md:1532:reply.md:1447:reply.md:1323:reply.md:1184:reply.md:1019:reply.md:859:reply.md:700:`financial_periods` | 
در مسیر 
reply.md:1535:reply.md:1449:reply.md:1325:reply.md:1187:`ingest_codal_report` یک 
reply.md:1536:reply.md:1450:reply.md:1326:reply.md:1188:reply.md:1023:reply.md:863:reply.md:705:`Report.financial_perio
d_id` 
reply.md:1537:reply.md:1451:reply.md:1327:reply.md:1189:reply.md:1025:`Report.financial_period_id` 
reply.md:1538:reply.md:1454:reply.md:1331:reply.md:1197:reply.md:1033:`service.py::ingest_codal_report` می‌رسد.
reply.md:1547:reply.md:1463:reply.md:1341:reply.md:1207:reply.md:1044:reply.md:883:reply.md:725:`financial_period_id` 
در 
reply.md:1548:reply.md:1464:reply.md:1342:reply.md:1208:reply.md:1045:reply.md:884:reply.md:727:`reports.financial_peri
od_id` اشاره 
reply.md:1549:reply.md:1465:reply.md:1345:reply.md:1211:reply.md:1049:`financial_periods.company_id` تا 
reply.md:1550:reply.md:1466:reply.md:1348:reply.md:1215:Report.financial_period_id — 
reply.md:1555:reply.md:1473:reply.md:1355:reply.md:1221:reply.md:1062:ingest_codal_report()
reply.md:1558:reply.md:1475:reply.md:1357:reply.md:1225:reply.md:1068:financial_periods, 
reply.md:1561:reply.md:1477:reply.md:1359:reply.md:1227:reply.md:1071:`financial_periods`
reply.md:1562:reply.md:1478:reply.md:1361:`ingest_codal_report`; the 
reply.md:1563:reply.md:1479:reply.md:1362:reply.md:1230:reply.md:1077:ingest_codal_report / 
reply.md:1564:reply.md:1480:reply.md:1363:reply.md:1231:reply.md:1079:`ingest_codal_report` 
reply.md:1565:reply.md:1481:reply.md:1364:reply.md:1232:reply.md:1081:ingest_codal_report()
reply.md:1566:reply.md:1482:reply.md:1365:reply.md:1233:reply.md:1082:reply.md:919:reply.md:761:`ingest_codal_report()`
 
reply.md:1567:reply.md:1483:reply.md:1366:reply.md:1234:reply.md:1083:reply.md:921:`ingest_codal_report`، 
reply.md:1568:reply.md:1484:reply.md:1368:`load_codal_pdf` و 
reply.md:1573:reply.md:1489:reply.md:1374:reply.md:1242:reply.md:1099:reply.md:935:reply.md:777:`load_codal_pdf_from_ur
l` 
reply.md:1574:reply.md:1490:reply.md:1383:reply.md:1251:reply.md:1110:reply.md:946:reply.md:785:reply.md:623:`financial
_periods.perio
reply.md:1576:reply.md:1491:reply.md:1386:reply.md:1254:reply.md:1114:`financial_period_id` در DTOها 
reply.md:1577:reply.md:1492:reply.md:1387:reply.md:1255:reply.md:1115:reply.md:950:reply.md:790:`reports.financial_peri
od_id` 
reply.md:1578:reply.md:1493:reply.md:1388:reply.md:1256:reply.md:1117:`financial_period_id` 
reply.md:1579:reply.md:1494:reply.md:1389:reply.md:1258:`ingest_codal_report` یک 
reply.md:1580:reply.md:1495:reply.md:1390:reply.md:1262:`ingest_codal_pdf` 
reply.md:1581:reply.md:1496:reply.md:1392:`load_codal_pdf` و 
reply.md:1582:reply.md:1497:reply.md:1393:reply.md:1264:reply.md:1124:`load_codal_pdf_from_url` پس 
reply.md:1583:reply.md:1498:reply.md:1402:reply.md:1274:reply.md:1134:reply.md:970:`src/ingestion/service.py::ingest_co
dal_report` 
reply.md:1585:reply.md:1499:reply.md:1409:reply.md:1281:reply.md:1141:reply.md:977:`financial_period_id` | 
reply.md:1590:reply.md:1505:reply.md:1413:reply.md:1285:reply.md:1145:reply.md:981:reply.md:819:reply.md:658:ingest_cod
al_report  
reply.md:1591:reply.md:1506:reply.md:1416:reply.md:1288:reply.md:1147:ingest_codal_report 
reply.md:1592:reply.md:1509:reply.md:1418:reply.md:1292:reply.md:1150:reply.md:986:reply.md:824:reply.md:664:financial_
period_id 
reply.md:1599:reply.md:1514:reply.md:1422:reply.md:1296:reply.md:1156:reply.md:991:reply.md:830:`reports.financial_peri
od_id` must 
reply.md:1601:reply.md:1517:reply.md:1424:reply.md:1298:reply.md:1158:reply.md:994:`reports.financial_period_id` 
reply.md:1602:reply.md:1518:reply.md:1427:reply.md:1301:reply.md:1161:reply.md:998:`financial_periods.company_id` تا 
reply.md:1603:reply.md:1519:reply.md:1430:reply.md:1304:load_codal_pdf و 
reply.md:1604:reply.md:1520:reply.md:1431:reply.md:1305:reply.md:1164:load_codal_pdf_from_url |
reply.md:1605:reply.md:1521:reply.md:1432:reply.md:1308:reply.md:1166:reply.md:1002:reply.md:842:ingest_codal_report 
reply.md:1606:reply.md:1522:reply.md:1433:reply.md:1310:ingest_codal_report 
reply.md:1611:reply.md:1532:reply.md:1447:reply.md:1323:reply.md:1184:reply.md:1019:reply.md:859:reply.md:700:`financia
l_periods` | 
reply.md:1613:reply.md:1535:reply.md:1449:reply.md:1325:reply.md:1187:`ingest_codal_report` یک 
reply.md:1616:reply.md:1537:reply.md:1451:reply.md:1327:reply.md:1189:reply.md:1025:`Report.financial_period_id` 
reply.md:1617:reply.md:1538:reply.md:1454:reply.md:1331:reply.md:1197:reply.md:1033:`service.py::ingest_codal_report` 
می‌رسد.
reply.md:1618:reply.md:1547:reply.md:1463:reply.md:1341:reply.md:1207:reply.md:1044:reply.md:883:reply.md:725:`financia
l_period_id` 
reply.md:1622:reply.md:1549:reply.md:1465:reply.md:1345:reply.md:1211:reply.md:1049:`financial_periods.company_id` تا 
reply.md:1623:reply.md:1550:reply.md:1466:reply.md:1348:reply.md:1215:Report.financial_period_id — 
reply.md:1624:reply.md:1555:reply.md:1473:reply.md:1355:reply.md:1221:reply.md:1062:ingest_codal_report()
reply.md:1625:reply.md:1558:reply.md:1475:reply.md:1357:reply.md:1225:reply.md:1068:financial_periods, 
reply.md:1626:reply.md:1561:reply.md:1477:reply.md:1359:reply.md:1227:reply.md:1071:`financial_periods`
reply.md:1627:reply.md:1562:reply.md:1478:reply.md:1361:`ingest_codal_report`; the 
reply.md:1628:reply.md:1563:reply.md:1479:reply.md:1362:reply.md:1230:reply.md:1077:ingest_codal_report / 
reply.md:1629:reply.md:1564:reply.md:1480:reply.md:1363:reply.md:1231:reply.md:1079:`ingest_codal_report` 
reply.md:1630:reply.md:1565:reply.md:1481:reply.md:1364:reply.md:1232:reply.md:1081:ingest_codal_report()
reply.md:1631:reply.md:1566:reply.md:1482:reply.md:1365:reply.md:1233:reply.md:1082:reply.md:919:reply.md:761:`ingest_c
odal_report()`
reply.md:1633:reply.md:1567:reply.md:1483:reply.md:1366:reply.md:1234:reply.md:1083:reply.md:921:`ingest_codal_report`،
 
reply.md:1634:reply.md:1568:reply.md:1484:reply.md:1368:`load_codal_pdf` و 
reply.md:1635:reply.md:1573:reply.md:1489:reply.md:1374:reply.md:1242:reply.md:1099:reply.md:935:reply.md:777:`load_cod
al_pdf_from_ur
reply.md:1639:reply.md:1576:reply.md:1491:reply.md:1386:reply.md:1254:reply.md:1114:`financial_period_id` در DTOها 
reply.md:1642:reply.md:1578:reply.md:1493:reply.md:1388:reply.md:1256:reply.md:1117:`financial_period_id` 
reply.md:1643:reply.md:1579:reply.md:1494:reply.md:1389:reply.md:1258:`ingest_codal_report` یک 
reply.md:1644:reply.md:1580:reply.md:1495:reply.md:1390:reply.md:1262:`ingest_codal_pdf` 
reply.md:1645:reply.md:1581:reply.md:1496:reply.md:1392:`load_codal_pdf` و 
reply.md:1646:reply.md:1582:reply.md:1497:reply.md:1393:reply.md:1264:reply.md:1124:`load_codal_pdf_from_url` پس 
reply.md:1649:reply.md:1585:reply.md:1499:reply.md:1409:reply.md:1281:reply.md:1141:reply.md:977:`financial_period_id` 
| 
reply.md:1652:reply.md:1591:reply.md:1506:reply.md:1416:reply.md:1288:reply.md:1147:ingest_codal_report 
reply.md:1657:reply.md:1601:reply.md:1517:reply.md:1424:reply.md:1298:reply.md:1158:reply.md:994:`reports.financial_per
iod_id` 
reply.md:1658:reply.md:1602:reply.md:1518:reply.md:1427:reply.md:1301:reply.md:1161:reply.md:998:`financial_periods.com
pany_id` تا 
reply.md:1659:reply.md:1603:reply.md:1519:reply.md:1430:reply.md:1304:load_codal_pdf و 
reply.md:1660:reply.md:1604:reply.md:1520:reply.md:1431:reply.md:1305:reply.md:1164:load_codal_pdf_from_url |
reply.md:1661:reply.md:1605:reply.md:1521:reply.md:1432:reply.md:1308:reply.md:1166:reply.md:1002:reply.md:842:ingest_c
odal_report 
reply.md:1662:reply.md:1606:reply.md:1522:reply.md:1433:reply.md:1310:ingest_codal_report 
reply.md:1665:reply.md:1613:reply.md:1535:reply.md:1449:reply.md:1325:reply.md:1187:`ingest_codal_report` یک 
reply.md:1666:reply.md:1616:reply.md:1537:reply.md:1451:reply.md:1327:reply.md:1189:reply.md:1025:`Report.financial_per
iod_id` 
reply.md:1667:reply.md:1617:reply.md:1538:reply.md:1454:reply.md:1331:reply.md:1197:reply.md:1033:`service.py::ingest_c
odal_report` 
reply.md:1671:reply.md:1622:reply.md:1549:reply.md:1465:reply.md:1345:reply.md:1211:reply.md:1049:`financial_periods.co
mpany_id` تا 
reply.md:1672:reply.md:1623:reply.md:1550:reply.md:1466:reply.md:1348:reply.md:1215:Report.financial_period_id — 
reply.md:1673:reply.md:1624:reply.md:1555:reply.md:1473:reply.md:1355:reply.md:1221:reply.md:1062:ingest_codal_report()
reply.md:1674:reply.md:1625:reply.md:1558:reply.md:1475:reply.md:1357:reply.md:1225:reply.md:1068:financial_periods, 
reply.md:1675:reply.md:1626:reply.md:1561:reply.md:1477:reply.md:1359:reply.md:1227:reply.md:1071:`financial_periods`
reply.md:1676:reply.md:1627:reply.md:1562:reply.md:1478:reply.md:1361:`ingest_codal_report`; the 
reply.md:1677:reply.md:1628:reply.md:1563:reply.md:1479:reply.md:1362:reply.md:1230:reply.md:1077:ingest_codal_report 
/ 
reply.md:1678:reply.md:1629:reply.md:1564:reply.md:1480:reply.md:1363:reply.md:1231:reply.md:1079:`ingest_codal_report`
 
reply.md:1679:reply.md:1630:reply.md:1565:reply.md:1481:reply.md:1364:reply.md:1232:reply.md:1081:ingest_codal_report()
reply.md:1682:reply.md:1633:reply.md:1567:reply.md:1483:reply.md:1366:reply.md:1234:reply.md:1083:reply.md:921:`ingest_
codal_report`،
reply.md:1684:reply.md:1634:reply.md:1568:reply.md:1484:reply.md:1368:`load_codal_pdf` و 
reply.md:1687:reply.md:1639:reply.md:1576:reply.md:1491:reply.md:1386:reply.md:1254:reply.md:1114:`financial_period_id`
 در DTOها 
reply.md:1688:reply.md:1642:reply.md:1578:reply.md:1493:reply.md:1388:reply.md:1256:reply.md:1117:`financial_period_id`
 
reply.md:1689:reply.md:1643:reply.md:1579:reply.md:1494:reply.md:1389:reply.md:1258:`ingest_codal_report` یک 
reply.md:1690:reply.md:1644:reply.md:1580:reply.md:1495:reply.md:1390:reply.md:1262:`ingest_codal_pdf` 
reply.md:1691:reply.md:1645:reply.md:1581:reply.md:1496:reply.md:1392:`load_codal_pdf` و 
reply.md:1692:reply.md:1646:reply.md:1582:reply.md:1497:reply.md:1393:reply.md:1264:reply.md:1124:`load_codal_pdf_from_
url` پس 
reply.md:1693:reply.md:1649:reply.md:1585:reply.md:1499:reply.md:1409:reply.md:1281:reply.md:1141:reply.md:977:`financi
al_period_id` 
reply.md:1695:reply.md:1652:reply.md:1591:reply.md:1506:reply.md:1416:reply.md:1288:reply.md:1147:ingest_codal_report 
reply.md:1698:reply.md:1658:reply.md:1602:reply.md:1518:reply.md:1427:reply.md:1301:reply.md:1161:reply.md:998:`financi
al_periods.com
reply.md:1700:reply.md:1659:reply.md:1603:reply.md:1519:reply.md:1430:reply.md:1304:load_codal_pdf و 
reply.md:1701:reply.md:1660:reply.md:1604:reply.md:1520:reply.md:1431:reply.md:1305:reply.md:1164:load_codal_pdf_from_u
rl |
reply.md:1704:reply.md:1662:reply.md:1606:reply.md:1522:reply.md:1433:reply.md:1310:ingest_codal_report 
reply.md:1705:reply.md:1665:reply.md:1613:reply.md:1535:reply.md:1449:reply.md:1325:reply.md:1187:`ingest_codal_report`
 یک 
reply.md:1710:reply.md:1671:reply.md:1622:reply.md:1549:reply.md:1465:reply.md:1345:reply.md:1211:reply.md:1049:`financ
ial_periods.co
reply.md:1712:reply.md:1672:reply.md:1623:reply.md:1550:reply.md:1466:reply.md:1348:reply.md:1215:Report.financial_peri
od_id — 
reply.md:1713:reply.md:1673:reply.md:1624:reply.md:1555:reply.md:1473:reply.md:1355:reply.md:1221:reply.md:1062:ingest_
codal_report()
reply.md:1714:reply.md:1674:reply.md:1625:reply.md:1558:reply.md:1475:reply.md:1357:reply.md:1225:reply.md:1068:financi
al_periods, 
reply.md:1715:reply.md:1675:reply.md:1626:reply.md:1561:reply.md:1477:reply.md:1359:reply.md:1227:reply.md:1071:`financ
ial_periods`
reply.md:1716:reply.md:1676:reply.md:1627:reply.md:1562:reply.md:1478:reply.md:1361:`ingest_codal_report`; the 
reply.md:1717:reply.md:1677:reply.md:1628:reply.md:1563:reply.md:1479:reply.md:1362:reply.md:1230:reply.md:1077:ingest_
codal_report 
reply.md:1719:reply.md:1678:reply.md:1629:reply.md:1564:reply.md:1480:reply.md:1363:reply.md:1231:reply.md:1079:`ingest
_codal_report`
reply.md:1721:reply.md:1679:reply.md:1630:reply.md:1565:reply.md:1481:reply.md:1364:reply.md:1232:reply.md:1081:ingest_
codal_report()
reply.md:1724:reply.md:1684:reply.md:1634:reply.md:1568:reply.md:1484:reply.md:1368:`load_codal_pdf` و 
reply.md:1725:reply.md:1687:reply.md:1639:reply.md:1576:reply.md:1491:reply.md:1386:reply.md:1254:reply.md:1114:`financ
ial_period_id`
reply.md:1727:reply.md:1688:reply.md:1642:reply.md:1578:reply.md:1493:reply.md:1388:reply.md:1256:reply.md:1117:`financ
ial_period_id`
reply.md:1729:reply.md:1689:reply.md:1643:reply.md:1579:reply.md:1494:reply.md:1389:reply.md:1258:`ingest_codal_report`
 یک 
reply.md:1730:reply.md:1690:reply.md:1644:reply.md:1580:reply.md:1495:reply.md:1390:reply.md:1262:`ingest_codal_pdf` 
reply.md:1731:reply.md:1691:reply.md:1645:reply.md:1581:reply.md:1496:reply.md:1392:`load_codal_pdf` و 
reply.md:1732:reply.md:1692:reply.md:1646:reply.md:1582:reply.md:1497:reply.md:1393:reply.md:1264:reply.md:1124:`load_c
odal_pdf_from_
reply.md:1736:reply.md:1695:reply.md:1652:reply.md:1591:reply.md:1506:reply.md:1416:reply.md:1288:reply.md:1147:ingest_
codal_report 
reply.md:1739:reply.md:1700:reply.md:1659:reply.md:1603:reply.md:1519:reply.md:1430:reply.md:1304:load_codal_pdf و 
reply.md:1740:reply.md:1701:reply.md:1660:reply.md:1604:reply.md:1520:reply.md:1431:reply.md:1305:reply.md:1164:load_co
dal_pdf_from_u
reply.md:1742:reply.md:1704:reply.md:1662:reply.md:1606:reply.md:1522:reply.md:1433:reply.md:1310:ingest_codal_report 
reply.md:1743:reply.md:1705:reply.md:1665:reply.md:1613:reply.md:1535:reply.md:1449:reply.md:1325:reply.md:1187:`ingest
_codal_report`
reply.md:1755:reply.md:1716:reply.md:1676:reply.md:1627:reply.md:1562:reply.md:1478:reply.md:1361:`ingest_codal_report`
; the 
reply.md:1762:reply.md:1724:reply.md:1684:reply.md:1634:reply.md:1568:reply.md:1484:reply.md:1368:`load_codal_pdf` و 
reply.md:1767:reply.md:1729:reply.md:1689:reply.md:1643:reply.md:1579:reply.md:1494:reply.md:1389:reply.md:1258:`ingest
_codal_report`
reply.md:1769:reply.md:1730:reply.md:1690:reply.md:1644:reply.md:1580:reply.md:1495:reply.md:1390:reply.md:1262:`ingest
_codal_pdf` 
reply.md:1770:reply.md:1731:reply.md:1691:reply.md:1645:reply.md:1581:reply.md:1496:reply.md:1392:`load_codal_pdf` و 
reply.md:1775:reply.md:1739:reply.md:1700:reply.md:1659:reply.md:1603:reply.md:1519:reply.md:1430:reply.md:1304:load_co
dal_pdf و 
reply.md:1778:reply.md:1742:reply.md:1704:reply.md:1662:reply.md:1606:reply.md:1522:reply.md:1433:reply.md:1310:ingest_
codal_report 
reply.md:1781:reply.md:1755:reply.md:1716:reply.md:1676:reply.md:1627:reply.md:1562:reply.md:1478:reply.md:1361:`ingest
_codal_report`
reply.md:1783:reply.md:1762:reply.md:1724:reply.md:1684:reply.md:1634:reply.md:1568:reply.md:1484:reply.md:1368:`load_c
odal_pdf` و 
reply.md:1788:reply.md:1770:reply.md:1731:reply.md:1691:reply.md:1645:reply.md:1581:reply.md:1496:reply.md:1392:`load_c
odal_pdf` و 
STAGE7_MASTER_WORKING_PACKET.md:95:  | 1 — دادهٔ منبع | دادهٔ مالی ذخیره‌شده؛ `src/forecast/queries.py` آن را با 
`Session` می‌خواند | `ingest_codal_report` در `src/ingestion/service.py` ورودی منبع را می‌نویسد؛ خروجی تحلیلی تولید 
نمی‌کند | ingestion caller باید Session بدهد؛ سرویس در مسیر نوشتن commit/rollback می‌کند و آن را نمی‌بندد | Stage 5 
queryها می‌توانند facts را بخوانند؛ زنجیرهٔ کامل از ingestion تا مراحل بعد اثبات نشده |


