
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
database\reports\DB_AUD_006_CODAL_PIPELINE_IMPLEMENTATION_READINESS_AUDIT.md:363:- تعریف و پیاده‌سازی writer مرکزی: 
src/ingestion/service.py::ingest_codal_report.
database\reports\DB_AUD_006_CODAL_PIPELINE_IMPLEMENTATION_READINESS_AUDIT.md:364:- API سازگاری 
src/ingestion/codal/ingestion.py::ingest_codal_report به writer مرکزی delegate می‌کند؛ ingest_codal_pdf نیز پس از 
استخراج آن API را صدا می‌زند.
database\reports\DB_AUD_006_CODAL_PIPELINE_IMPLEMENTATION_READINESS_AUDIT.md:365:- src/ingestion/codal/pipeline.py، 
تابع‌های load_codal_pdf و load_codal_pdf_from_url را دارد و هر دو مسیر در نهایت writer مرکزی را فراخوانی می‌کنند.
database\reports\DB_AUD_006_CODAL_PIPELINE_IMPLEMENTATION_READINESS_AUDIT.md:367:- جست‌وجوی financial_period_id 
کاربردهای جداگانه‌ای در src/evaluation نشان داد. در فایل‌های بازبینی‌شده، این شناسه در DTOها و قراردادهای 
observation/evaluation به دورهٔ داده اشاره دارد؛ نباید صرفاً به‌دلیل یکسان بودن نام، آن را مصرف ستون 
Report.financial_period_id تلقی کرد.
database\reports\DB_AUD_006_CODAL_PIPELINE_IMPLEMENTATION_READINESS_AUDIT.md:371:در محدودهٔ کدهای Python زیر src/ که 
با جست‌وجو و بازبینی فایل‌های مرتبط بررسی شدند، وابستگی اجرایی مستقیم ستون Report.financial_period_id در writer قدیمی 
متمرکز است؛ facadeها و pipelineهای PDF آن را از طریق همان writer به ارث می‌برند. مصرف‌کنندهٔ تولیدی مستقلی که جداگانه 
این ستون را بخواند، از شواهد این خروجی احراز نشد. این نتیجه را نباید به تمام محیط‌ها، اسکریپت‌های بیرونی، SQL یا 
فراخوانی‌های پویا تعمیم داد.
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
database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1896:خروجی جست‌وجوی PowerShell در تمام فایل‌های Python 
repository (به‌استثنای .git، محیط‌های مجازی و __pycache__) بررسی شد. writer مرکزی 
src/ingestion/service.py::ingest_codal_report است؛ facade در src/ingestion/codal/ingestion.py و pipelineهای PDF در 
src/ingestion/codal/pipeline.py به آن متصل‌اند. packageها این APIها را export می‌کنند. ارجاع‌های تستی نیز قرارداد فعلی 
را پوشش می‌دهند.
database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1898:کاربردهای financial_period_id در src/evaluation مربوط به 
دورهٔ observation/evaluation هستند و نباید بدون اثبات رابطه، مصرف ستون Report.financial_period_id شمرده شوند. در 
محدودهٔ فایل‌های Python بررسی‌شده، مصرف‌کنندهٔ تولیدی مستقلی برای ستون Report جدا از writer legacy احراز نشد؛ اما این 
نتیجه شامل فایل‌های غیر Python، کد بیرون repository یا فراخوانی پویا نیست.
database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1900:**نتیجه:** ستون Report.financial_period_id و قرارداد 
writer legacy فعلاً حفظ می‌شوند. writer جدید Excel باید period را در سطح هر observation/fact تعیین کند. نقش نهایی ستون 
Report و تصمیم nullable/remove هنوز باز است و به بررسی وابستگی‌های باقیمانده و طرح بازنشستگی legacy موکول می‌شود. این 
بررسی read-only بود؛ تست یا تغییر کد/مدل/schema/migration/DB انجام نشد.
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
reply.md:83:src/ingestion/service.py::ingest_codal_report.
reply.md:85:src/ingestion/codal/ingestion.py::ingest_codal_report به writer مرکزی delegate می‌کند؛ ingest_codal_pdf 
نیز پس از 
reply.md:88:تابع‌های load_codal_pdf و load_codal_pdf_from_url را دارد و هر دو مسیر در نهایت writer مرکزی را فراخوانی 
می‌کنند.
reply.md:89:database\reports\DB_AUD_006_CODAL_PIPELINE_IMPLEMENTATION_READINESS_AUDIT.md:367:- جست‌وجوی 
financial_period_id 
reply.md:92:Report.financial_period_id تلقی کرد.
reply.md:94:با جست‌وجو و بازبینی فایل‌های مرتبط بررسی شدند، وابستگی اجرایی مستقیم ستون Report.financial_period_id در 
writer قدیمی 
reply.md:99:`company_id`; free-text `report_type`; FK `financial_period_id` | Reuse, but report-type normalization is 
a 
reply.md:101:database\reports\DB_AUD_009_ORM_MIGRATION_TEMPLATE_COMPATIBILITY_AUDIT.md:24:| `FinancialPeriod` / 
`financial_periods` 
reply.md:104:database\reports\DB_AUD_011_LEGACY_RAW_FACT_PROVENANCE_DECISION.md:92:- `ingest_codal_report(...)` 
creates one 
reply.md:106:database\reports\DB_AUD_012_CODAL_PDF_PATH_DEPENDENCY_AUDIT.md:17:load_codal_pdf / 
load_codal_pdf_from_url  
reply.md:107:database\reports\DB_AUD_012_CODAL_PDF_PATH_DEPENDENCY_AUDIT.md:21:→ ingest_codal_report  
reply.md:109:ingest_codal_pdf و facade سازگاری ingest_codal_report | بخش PDF-only + facade legacy |
reply.md:110:database\reports\DB_AUD_012_CODAL_PDF_PATH_DEPENDENCY_AUDIT.md:36:| 
src/ingestion/service.py::ingest_codal_report | 
reply.md:113:database\reports\DB_AUD_012_CODAL_PDF_PATH_DEPENDENCY_AUDIT.md:125:- `service.py::ingest_codal_report`: 
persistence 
reply.md:115:database\reports\DB_AUD_013_EXCEL_CANONICAL_PERSISTENCE_READINESS.md:45:- financial_period_id به‌عنوان 
primary report 
reply.md:117:database\reports\DB_AUD_013_EXCEL_CANONICAL_PERSISTENCE_READINESS.md:53:- financial_period_id در مدل فعلی 
روی Report 
reply.md:121:`src/ingestion/service.py::ingest_codal_report`:
reply.md:122:database\reports\DB_AUD_014_NORMALIZED_DERIVED_FACT_CONSUMER_AUDIT.md:103:    -> ingest_codal_report
reply.md:123:database\reports\DB_DES_009_CANONICAL_FINANCIAL_FACT_PHYSICAL_MODEL.md:43:3. `financial_periods` — 
redesigned for 
reply.md:127:FinancialPeriod. The current NOT NULL `reports.financial_period_id` must not be allowed to impose one 
period on every 
reply.md:129:database\reports\DB_DES_009_CANONICAL_FINANCIAL_FACT_PHYSICAL_MODEL.md:93:The new/updated 
`financial_periods` model 
reply.md:132:consumers before making current `reports.financial_period_id` nullable or moving it.
reply.md:134:`financial_period_id` را جداگانه نگه می‌دارد؛ FKها به‌تنهایی تضمین نمی‌کنند که دورهٔ گزارش متعلق به همان 
شرکت باشد.
reply.md:137:`report_versions.report_id` یا `financial_periods.company_id` تا وقتی Fact وابسته وجود دارد ممنوع باشد؛ 
اصلاح هویت با 
reply.md:139:database\reports\DB_DES_009_CANONICAL_FINANCIAL_FACT_PHYSICAL_MODEL.md:360:4. اگر 
`Report.financial_period_id` در مدل 
reply.md:143:pipelineهای load_codal_pdf و load_codal_pdf_from_url |
reply.md:144:database\reports\DB_PLAN_013_PDF_PATH_RETIREMENT_SEQUENCE.md:41:| 
\`src/ingestion/service.py::ingest_codal_report\` | 
reply.md:148:پس از شناسایی callerها باید فقط facade PDF حذف و وضعیت ingest_codal_report جداگانه تعیین شود |
reply.md:150:RawLineInput و ingest_codal_report فعلاً حفظ؛ بعداً با API جدید جایگزین یا صریحاً بازنشسته شوند |
reply.md:151:database\reports\DB_PLAN_013_PDF_PATH_RETIREMENT_SEQUENCE.md:72:1. تابع فعلی \`ingest_codal_report\` را 
به دو مسئولیت 
reply.md:153:database\reports\DB_STD_005_AND_DB_AUD_001_MARKET_FX_EVIDENCE_REVIEW.md:288:| 
`service.py::ingest_codal_report` | 
reply.md:158:database\reports\DB_STD_005_AND_DB_AUD_001_MARKET_FX_EVIDENCE_REVIEW.md:291:| 
`codal/ingestion.py::ingest_codal_pdf` و 
reply.md:162:`ingestion/service.py::ingest_codal_report` (تابع persistence گزارش CODAL) یک `ReportVersion` و مجموعه‌ای 
از 
reply.md:166:`ingest_codal_report` و Stage 5 query | Stage 5 مصرف‌کنندهٔ مستقیم خروجی CODAL نیست | طراحی/پیاده‌سازی 
pipeline 
reply.md:168:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:333:- `src/ingestion/service.py`: ورودی 
`ingest_codal_report` 
reply.md:172:نشده است: گزارش منطقی ممکن است در یک انتشار چند ستون زمانی داشته باشد، در حالی که سرویس فعلی یک 
`financial_period_id` 
reply.md:175:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:351:| Period | `FinancialPeriod` | 
`financial_periods` |
reply.md:176:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:396:2. `Report.financial_period_id` اجباری است و 
reply.md:177:`ingest_codal_report` یک period_id واحد را به تمام RawFinancialFactهای یک report version اختصاص می‌دهد.
reply.md:179:`src/ingestion/service.py::ingest_codal_report`؛ facadeها در `src/ingestion/codal/ingestion.py` و 
`pipeline.py` | در 
reply.md:183:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:422:| `financial_periods` | در مسیر CODAL، 
period از قبل 
reply.md:186:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:460:5. ساختار فعلی `Report.financial_period_id` 
و 
reply.md:191:محدودیت را دارد. متد `ingest_codal_report` یک `period_id` می‌گیرد و همان مقدار را برای همهٔ 
RawFinancialFactها ذخیره 
reply.md:193:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:477:4. `Report.financial_period_id` هم اجباری 
است؛ بنابراین 
reply.md:198:association، الزامی/اختیاری بودن `Report.financial_period_id` قدیمی و نگاشت نسخه‌های اصلاحی باید در Task 
008 و Task 
reply.md:201:`src/ingestion/service.py::ingest_codal_report` مستقیماً برای هر `RawLineInput` یک `RawFinancialFact` 
می‌سازد و با 
reply.md:207:`src/ingestion/service.py::ingest_codal_report` می‌رسند؛ این تابع برای هر RawLineInput یک 
RawFinancialFact می‌سازد و 
reply.md:212:`service.py::ingest_codal_report` → RawFinancialFact.
reply.md:213:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1682:- `codal/ingestion.py::ingest_codal_report` 
فقط facade 
reply.md:214:است و به writer مرکزی `service.py::ingest_codal_report` می‌رسد.
reply.md:215:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1683:- `codal/ingestion.py::ingest_codal_pdf` 
extraction و 
reply.md:218:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1684:- `codal/pipeline.py::load_codal_pdf` و 
reply.md:219:`load_codal_pdf_from_url` acquisition/extraction/validation را پیش از writer اجرا می‌کنند؛ failureهای این 
مراحل Run 
reply.md:222:gateهای طراحی DB-DES-009. اولین مورد: inventory تمام مصرف‌کنندگان `reports.financial_period_id`، چون پیش 
از nullable 
reply.md:226:`reports.financial_period_id` و تفکیک قرارداد legacy CODAL از Excel — 2026-11-18
reply.md:227:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1714:- ستون `Report.financial_period_id` در ORM 
اجباری است 
reply.md:230:`service.py::ingest_codal_report` delegate می‌کند؛ PDF wrapper پس از extraction از آن استفاده می‌کند. 
مسیرهای 
reply.md:232:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1718:- نام `financial_period_id` در 
evaluation/forecast 
reply.md:233:observation DTOها و تست‌های Stage 5/6 لزوماً به ستون `reports.financial_period_id` اشاره ندارد؛ این دو 
مفهوم باید در 
reply.md:237:`Report.financial_period_id` مجاز نیست. مسیر جدید Excel باید دوره را در سطح هر Fact تعیین کند و نباید یک 
دورهٔ واحد را 
reply.md:243:`report_versions.report_id` و `financial_periods.company_id` تا وقتی Fact وابسته وجود دارد باید ممنوع 
باشد. اگر 
reply.md:244:`Report.financial_period_id` به‌صورت optional metadata باقی ماند، در صورت non-NULL بودن تطابق شرکت آن نیز 
کنترل شود.
reply.md:246:writer قدیمی به Report.financial_period_id — 2026-11-18
reply.md:247:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1880:- `service.py::ingest_codal_report` writer 
مرکزی CODAL 
reply.md:250:`Report.financial_period_id` باید با ورودی یکسان باشند؛ در غیر این صورت عملیات رد می‌شود.
reply.md:253:src/ingestion/service.py::ingest_codal_report است؛ facade در src/ingestion/codal/ingestion.py و 
pipelineهای PDF در 
reply.md:256:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1898:کاربردهای financial_period_id در 
src/evaluation مربوط به 
reply.md:257:دورهٔ observation/evaluation هستند و نباید بدون اثبات رابطه، مصرف ستون Report.financial_period_id شمرده 
شوند. در 
reply.md:260:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1900:**نتیجه:** ستون Report.financial_period_id 
و قرارداد 
reply.md:265:`ingest_codal_report` take DTOs |
reply.md:266:prompts\10_Implementation_Status.md:83:| CODAL extraction outside core write | PASS | 
`ingest_codal_report` accepts 
reply.md:268:prompts\10_Implementation_Status.md:243:ingest_codal_report()
reply.md:269:src\tests\final_validation_audit.md:140:  → ingest_codal_report()
reply.md:270:src\tests\golden_audit_source_plan.md:15:ingest_codal_report()
reply.md:271:src\tests\golden_audit_source_plan.md:115:- Report / ReportVersion / RawFinancialFact created by 
ingest_codal_report()
reply.md:272:01_Stage1_Data_Foundation.md:278:financial_period_id
reply.md:275:(models cover industries/companies, financial_periods, reports/report_versions, raw 
reply.md:282:10_Production_Codal_Extraction_and_Data_Load.md:22:ingest_codal_report()
reply.md:283:10_Production_Codal_Extraction_and_Data_Load.md:113:`extract → validate → RawLineInput[] → 
ingest_codal_report()`
reply.md:284:11_Production_Data_Load_and_Foundation_Validation.md:136:ingest_codal_report()
reply.md:285:12_Database_Architecture_V1.1.md:104:- `financial_periods`
reply.md:286:12_Database_Architecture_V1.1.md:801:ingest_codal_report / ingest_ohlc_* / ingest_fx_rates
reply.md:288:consumed by `ingest_codal_report`; the existing downstream persistence boundary must remain 
format-independent.
reply.md:289:99_Architecture_Change_Log.md:386:  ingest_codal_report / ingest_ohlc_* / ingest_fx_rates
reply.md:291:is a **pre-ingestion** responsibility. `ingest_codal_report` receives already-extracted `RawLineInput` 
lines plus 
reply.md:294:PROJECT_HANDOFF_INSTRUCTIONS.md:252:    ingest_codal_report()
reply.md:295:reply.md:4:PDF را استخراج می‌کنند، خروجی `RawLineInput` می‌سازند و `ingest_codal_report()` آن را به 
`RawFinancialFact` 
reply.md:297:reply.md:8:`src/ingestion/service.py` | `RawLineInput`، `ingest_codal_report`، transaction و replay |
reply.md:298:reply.md:10:از `load_codal_pdf` و PDFهای fixture استفاده می‌کند.
reply.md:299:reply.md:11:database\reports\DB_AUD_006_CODAL_PIPELINE_IMPLEMENTATION_READINESS_AUDIT.md:61:در 
`ingest_codal_report()`:
reply.md:300:reply.md:13:`financial_period_id` است، درحالی‌که قرارداد منطقی می‌گوید یک ReportVersion می‌تواند چند دوره 
و هر 
reply.md:302:reply.md:15:database\reports\DB_AUD_006_CODAL_PIPELINE_IMPLEMENTATION_READINESS_AUDIT.md:83:- 
`ingest_codal_report()` 
reply.md:305:`ingest_codal_report`
reply.md:306:reply.md:19:`src/ingestion/codal/ingestion.py::ingest_codal_report` صرفاً facade سازگاری است و به 
reply.md:307:reply.md:20:`src/ingestion/service.py::ingest_codal_report` delegate می‌کند؛ transaction مستقل ندارد.
reply.md:308:reply.md:22:`src/ingestion/codal/ingestion.py::ingest_codal_pdf` extraction را اجرا می‌کند و سپس به 
facade بالا 
reply.md:310:reply.md:26:`src/ingestion/codal/pipeline.py::load_codal_pdf` و `load_codal_pdf_from_url` acquisition، 
extraction و 
reply.md:312:reply.md:30:`src/ingestion/service.py::ingest_codal_report` writer اصلی 
Report/ReportVersion/RawFinancialFact است. این 
reply.md:314:reply.md:36:`reports.financial_period_id` پیش از nullable کردن/جابه‌جایی آن است. سپس gateهای 
ReportVersion source 
reply.md:315:reply.md:39:`reports.financial_period_id` و مسیرهای فراخوانی CODAL — 2026-11-18
reply.md:316:reply.md:41:`financial_period_id|FinancialPeriod` در کل فایل‌های `*.py` و `*.sql` زیر repository، موارد 
زیر را نشان 
reply.md:318:reply.md:43:`Report.financial_period_id` با `nullable=False` و FK به `financial_periods.period_id`.
reply.md:319:reply.md:46:`Report.financial_period_id` استفاده نشده است.
reply.md:320:reply.md:48:تست‌های Stage 5/6: نام `financial_period_id` در DTOها و مدل‌های ارزیابی به‌عنوان شناسهٔ دورهٔ 
reply.md:322:reply.md:49:استفاده شده است؛ این موارد به‌تنهایی مصرف ستون `reports.financial_period_id` نیستند.
reply.md:323:reply.md:51:Report و قرارداد قدیمی را با `financial_period_id` اجباری می‌آزمایند؛ تست‌های PDF نیز رابطهٔ 
Report با 
reply.md:325:reply.md:54:تابع عمومی `ingest_codal_report` یک facade سازگار با گذشته است و به 
reply.md:326:`src.ingestion.service.ingest_codal_report` 
reply.md:327:reply.md:55:delegate می‌کند. تابع `ingest_codal_pdf` پس از extraction همین facade را فراخوانی می‌کند.
reply.md:328:reply.md:57:توابع `load_codal_pdf` و `load_codal_pdf_from_url` پس از acquisition/extraction/validation، 
writer مرکزی 
reply.md:329:reply.md:58:`src.ingestion.service.ingest_codal_report` را فراخوانی می‌کنند.
reply.md:330:reply.md:61:`financial_period_id` ندارند؛ این با یافتهٔ قبلی DB-AUD-013 مبنی بر نبود production 
Excel-to-canonical 
reply.md:333:`Report.financial_period_id` در 
reply.md:334:reply.md:68:`Report.financial_period_id` تا زمان تعیین تکلیف و بازنشستگی کنترل‌شدهٔ مسیر legacy باید حفظ 
شود؛ اگر در 
reply.md:336:reply.md:71:Report.financial_period_id و مرز writer قدیمی — 2026-11-18
reply.md:337:reply.md:73:مسیر مشاهده شد `src/ingestion/service.py::ingest_codal_report` است؛ facade در 
`codal/ingestion.py` به همین 
reply.md:339:reply.md:76:`Report.financial_period_id` با ورودی مقایسه می‌شوند؛ اختلاف باعث رد عملیات می‌شود.
reply.md:340:reply.md:78:`financial_period_id=period_id` ثبت می‌شود.
reply.md:341:reply.md:80:Report.financial_period_id (حذف تدریجی، nullable و descriptive، یا جایگزینی با primary-period 
metadata) پس 
reply.md:343:reply.md:83:src/ingestion/service.py::ingest_codal_report.
reply.md:344:reply.md:85:src/ingestion/codal/ingestion.py::ingest_codal_report به writer مرکزی delegate می‌کند؛ 
ingest_codal_pdf 
reply.md:346:reply.md:88:تابع‌های load_codal_pdf و load_codal_pdf_from_url را دارد و هر دو مسیر در نهایت writer مرکزی 
را فراخوانی 
reply.md:349:financial_period_id 
reply.md:350:reply.md:92:Report.financial_period_id تلقی کرد.
reply.md:351:reply.md:94:با جست‌وجو و بازبینی فایل‌های مرتبط بررسی شدند، وابستگی اجرایی مستقیم ستون 
Report.financial_period_id در 
reply.md:353:reply.md:99:`company_id`; free-text `report_type`; FK `financial_period_id` | Reuse, but report-type 
normalization is 
reply.md:356:`financial_periods` 
reply.md:357:reply.md:104:database\reports\DB_AUD_011_LEGACY_RAW_FACT_PROVENANCE_DECISION.md:92:- 
`ingest_codal_report(...)` 
reply.md:359:reply.md:106:database\reports\DB_AUD_012_CODAL_PDF_PATH_DEPENDENCY_AUDIT.md:17:load_codal_pdf / 
reply.md:360:load_codal_pdf_from_url  
reply.md:361:reply.md:107:database\reports\DB_AUD_012_CODAL_PDF_PATH_DEPENDENCY_AUDIT.md:21:→ ingest_codal_report  
reply.md:362:reply.md:109:ingest_codal_pdf و facade سازگاری ingest_codal_report | بخش PDF-only + facade legacy |
reply.md:364:src/ingestion/service.py::ingest_codal_report | 
reply.md:365:reply.md:113:database\reports\DB_AUD_012_CODAL_PDF_PATH_DEPENDENCY_AUDIT.md:125:- 
`service.py::ingest_codal_report`: 
reply.md:367:reply.md:115:database\reports\DB_AUD_013_EXCEL_CANONICAL_PERSISTENCE_READINESS.md:45:- 
financial_period_id به‌عنوان 
reply.md:369:reply.md:117:database\reports\DB_AUD_013_EXCEL_CANONICAL_PERSISTENCE_READINESS.md:53:- 
financial_period_id در مدل فعلی 
reply.md:371:reply.md:121:`src/ingestion/service.py::ingest_codal_report`:
reply.md:372:reply.md:122:database\reports\DB_AUD_014_NORMALIZED_DERIVED_FACT_CONSUMER_AUDIT.md:103:    -> 
ingest_codal_report
reply.md:373:reply.md:123:database\reports\DB_DES_009_CANONICAL_FINANCIAL_FACT_PHYSICAL_MODEL.md:43:3. 
`financial_periods` — 
reply.md:375:reply.md:127:FinancialPeriod. The current NOT NULL `reports.financial_period_id` must not be allowed to 
impose one 
reply.md:378:`financial_periods` model 
reply.md:379:reply.md:132:consumers before making current `reports.financial_period_id` nullable or moving it.
reply.md:380:reply.md:134:`financial_period_id` را جداگانه نگه می‌دارد؛ FKها به‌تنهایی تضمین نمی‌کنند که دورهٔ گزارش 
متعلق به همان 
reply.md:382:reply.md:137:`report_versions.report_id` یا `financial_periods.company_id` تا وقتی Fact وابسته وجود دارد 
ممنوع باشد؛ 
reply.md:385:`Report.financial_period_id` در مدل 
reply.md:386:reply.md:143:pipelineهای load_codal_pdf و load_codal_pdf_from_url |
reply.md:388:\`src/ingestion/service.py::ingest_codal_report\` | 
reply.md:389:reply.md:148:پس از شناسایی callerها باید فقط facade PDF حذف و وضعیت ingest_codal_report جداگانه تعیین شود 
|
reply.md:390:reply.md:150:RawLineInput و ingest_codal_report فعلاً حفظ؛ بعداً با API جدید جایگزین یا صریحاً بازنشسته 
شوند |
reply.md:391:reply.md:151:database\reports\DB_PLAN_013_PDF_PATH_RETIREMENT_SEQUENCE.md:72:1. تابع فعلی 
\`ingest_codal_report\` را 
reply.md:394:`service.py::ingest_codal_report` | 
reply.md:396:`codal/ingestion.py::ingest_codal_pdf` و 
reply.md:397:reply.md:162:`ingestion/service.py::ingest_codal_report` (تابع persistence گزارش CODAL) یک 
`ReportVersion` و مجموعه‌ای 
reply.md:399:reply.md:166:`ingest_codal_report` و Stage 5 query | Stage 5 مصرف‌کنندهٔ مستقیم خروجی CODAL نیست | 
طراحی/پیاده‌سازی 
reply.md:402:`ingest_codal_report` 
reply.md:404:`financial_period_id` 
reply.md:406:`financial_periods` |
reply.md:407:reply.md:176:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:396:2. `Report.financial_period_id` 
اجباری است و 
reply.md:408:reply.md:177:`ingest_codal_report` یک period_id واحد را به تمام RawFinancialFactهای یک report version 
اختصاص می‌دهد.
reply.md:409:reply.md:179:`src/ingestion/service.py::ingest_codal_report`؛ facadeها در 
`src/ingestion/codal/ingestion.py` و 
reply.md:411:reply.md:183:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:422:| `financial_periods` | در مسیر 
CODAL، 
reply.md:413:reply.md:186:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:460:5. ساختار فعلی 
`Report.financial_period_id` 
reply.md:415:reply.md:191:محدودیت را دارد. متد `ingest_codal_report` یک `period_id` می‌گیرد و همان مقدار را برای همهٔ 
reply.md:417:reply.md:193:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:477:4. `Report.financial_period_id` 
هم اجباری 
reply.md:419:reply.md:198:association، الزامی/اختیاری بودن `Report.financial_period_id` قدیمی و نگاشت نسخه‌های اصلاحی 
باید در Task 
reply.md:421:reply.md:201:`src/ingestion/service.py::ingest_codal_report` مستقیماً برای هر `RawLineInput` یک 
`RawFinancialFact` 
reply.md:423:reply.md:207:`src/ingestion/service.py::ingest_codal_report` می‌رسند؛ این تابع برای هر RawLineInput یک 
reply.md:425:reply.md:212:`service.py::ingest_codal_report` → RawFinancialFact.
reply.md:426:reply.md:213:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1682:- 
`codal/ingestion.py::ingest_codal_report` 
reply.md:428:reply.md:214:است و به writer مرکزی `service.py::ingest_codal_report` می‌رسد.
reply.md:429:reply.md:215:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1683:- 
`codal/ingestion.py::ingest_codal_pdf` 
reply.md:431:reply.md:218:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1684:- 
`codal/pipeline.py::load_codal_pdf` و 
reply.md:432:reply.md:219:`load_codal_pdf_from_url` acquisition/extraction/validation را پیش از writer اجرا می‌کنند؛ 
failureهای این 
reply.md:434:reply.md:222:gateهای طراحی DB-DES-009. اولین مورد: inventory تمام مصرف‌کنندگان 
`reports.financial_period_id`، چون پیش 
reply.md:436:reply.md:226:`reports.financial_period_id` و تفکیک قرارداد legacy CODAL از Excel — 2026-11-18
reply.md:437:reply.md:227:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1714:- ستون 
`Report.financial_period_id` در ORM 
reply.md:439:reply.md:230:`service.py::ingest_codal_report` delegate می‌کند؛ PDF wrapper پس از extraction از آن 
استفاده می‌کند. 
reply.md:441:reply.md:232:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1718:- نام `financial_period_id` در 
reply.md:443:reply.md:233:observation DTOها و تست‌های Stage 5/6 لزوماً به ستون `reports.financial_period_id` اشاره 
ندارد؛ این دو 
reply.md:445:reply.md:237:`Report.financial_period_id` مجاز نیست. مسیر جدید Excel باید دوره را در سطح هر Fact تعیین 
کند و نباید یک 
reply.md:447:reply.md:243:`report_versions.report_id` و `financial_periods.company_id` تا وقتی Fact وابسته وجود دارد 
باید ممنوع 
reply.md:449:reply.md:244:`Report.financial_period_id` به‌صورت optional metadata باقی ماند، در صورت non-NULL بودن 
تطابق شرکت آن نیز 
reply.md:451:reply.md:246:writer قدیمی به Report.financial_period_id — 2026-11-18
reply.md:452:reply.md:247:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1880:- 
`service.py::ingest_codal_report` writer 
reply.md:454:reply.md:250:`Report.financial_period_id` باید با ورودی یکسان باشند؛ در غیر این صورت عملیات رد می‌شود.
reply.md:455:reply.md:253:src/ingestion/service.py::ingest_codal_report است؛ facade در 
src/ingestion/codal/ingestion.py و 
reply.md:457:reply.md:256:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1898:کاربردهای financial_period_id 
در 
reply.md:459:reply.md:257:دورهٔ observation/evaluation هستند و نباید بدون اثبات رابطه، مصرف ستون 
Report.financial_period_id شمرده 
reply.md:461:reply.md:260:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1900:**نتیجه:** ستون 
Report.financial_period_id 
reply.md:463:reply.md:265:`ingest_codal_report` take DTOs |
reply.md:465:`ingest_codal_report` accepts 
reply.md:466:reply.md:268:prompts\10_Implementation_Status.md:243:ingest_codal_report()
reply.md:467:reply.md:269:src\tests\final_validation_audit.md:140:  → ingest_codal_report()
reply.md:468:reply.md:270:src\tests\golden_audit_source_plan.md:15:ingest_codal_report()
reply.md:470:ingest_codal_report()
reply.md:471:reply.md:272:01_Stage1_Data_Foundation.md:278:financial_period_id
reply.md:472:reply.md:275:(models cover industries/companies, financial_periods, reports/report_versions, raw 
reply.md:473:reply.md:282:10_Production_Codal_Extraction_and_Data_Load.md:22:ingest_codal_report()
reply.md:475:ingest_codal_report()`
reply.md:476:reply.md:284:11_Production_Data_Load_and_Foundation_Validation.md:136:ingest_codal_report()
reply.md:477:reply.md:285:12_Database_Architecture_V1.1.md:104:- `financial_periods`
reply.md:478:reply.md:286:12_Database_Architecture_V1.1.md:801:ingest_codal_report / ingest_ohlc_* / ingest_fx_rates
reply.md:479:reply.md:288:consumed by `ingest_codal_report`; the existing downstream persistence boundary must remain 
reply.md:481:reply.md:289:99_Architecture_Change_Log.md:386:  ingest_codal_report / ingest_ohlc_* / ingest_fx_rates
reply.md:482:reply.md:291:is a **pre-ingestion** responsibility. `ingest_codal_report` receives already-extracted 
`RawLineInput` 
reply.md:484:reply.md:294:PROJECT_HANDOFF_INSTRUCTIONS.md:252:    ingest_codal_report()
reply.md:485:reply.md:295:reply.md:4:PDF را استخراج می‌کنند، خروجی `RawLineInput` می‌سازند و `ingest_codal_report()` 
آن را به 
reply.md:487:reply.md:297:reply.md:8:`src/ingestion/service.py` | `RawLineInput`، `ingest_codal_report`، transaction و 
replay |
reply.md:488:reply.md:298:reply.md:10:از `load_codal_pdf` و PDFهای fixture استفاده می‌کند.
reply.md:490:`ingest_codal_report()`:
reply.md:491:reply.md:300:reply.md:13:`financial_period_id` است، درحالی‌که قرارداد منطقی می‌گوید یک ReportVersion 
می‌تواند چند دوره 
reply.md:494:`ingest_codal_report()` 
reply.md:495:reply.md:305:`ingest_codal_report`
reply.md:496:reply.md:306:reply.md:19:`src/ingestion/codal/ingestion.py::ingest_codal_report` صرفاً facade سازگاری است 
و به 
reply.md:497:reply.md:307:reply.md:20:`src/ingestion/service.py::ingest_codal_report` delegate می‌کند؛ transaction 
مستقل ندارد.
reply.md:498:reply.md:308:reply.md:22:`src/ingestion/codal/ingestion.py::ingest_codal_pdf` extraction را اجرا می‌کند و 
سپس به 
reply.md:500:reply.md:310:reply.md:26:`src/ingestion/codal/pipeline.py::load_codal_pdf` و `load_codal_pdf_from_url` 
acquisition، 
reply.md:502:reply.md:312:reply.md:30:`src/ingestion/service.py::ingest_codal_report` writer اصلی 
reply.md:504:reply.md:314:reply.md:36:`reports.financial_period_id` پیش از nullable کردن/جابه‌جایی آن است. سپس gateهای 
reply.md:506:reply.md:315:reply.md:39:`reports.financial_period_id` و مسیرهای فراخوانی CODAL — 2026-11-18
reply.md:507:reply.md:316:reply.md:41:`financial_period_id|FinancialPeriod` در کل فایل‌های `*.py` و `*.sql` زیر 
repository، موارد 
reply.md:509:reply.md:318:reply.md:43:`Report.financial_period_id` با `nullable=False` و FK به 
`financial_periods.period_id`.
reply.md:510:reply.md:319:reply.md:46:`Report.financial_period_id` استفاده نشده است.
reply.md:511:reply.md:320:reply.md:48:تست‌های Stage 5/6: نام `financial_period_id` در DTOها و مدل‌های ارزیابی به‌عنوان 
شناسهٔ دورهٔ 
reply.md:512:reply.md:322:reply.md:49:استفاده شده است؛ این موارد به‌تنهایی مصرف ستون `reports.financial_period_id` 
نیستند.
reply.md:513:reply.md:323:reply.md:51:Report و قرارداد قدیمی را با `financial_period_id` اجباری می‌آزمایند؛ تست‌های 
PDF نیز رابطهٔ 
reply.md:515:reply.md:325:reply.md:54:تابع عمومی `ingest_codal_report` یک facade سازگار با گذشته است و به 
reply.md:516:reply.md:326:`src.ingestion.service.ingest_codal_report` 
reply.md:517:reply.md:327:reply.md:55:delegate می‌کند. تابع `ingest_codal_pdf` پس از extraction همین facade را 
فراخوانی می‌کند.
reply.md:518:reply.md:328:reply.md:57:توابع `load_codal_pdf` و `load_codal_pdf_from_url` پس از 
acquisition/extraction/validation، 
reply.md:520:reply.md:329:reply.md:58:`src.ingestion.service.ingest_codal_report` را فراخوانی می‌کنند.
reply.md:521:reply.md:330:reply.md:61:`financial_period_id` ندارند؛ این با یافتهٔ قبلی DB-AUD-013 مبنی بر نبود 
production 
reply.md:523:reply.md:333:`Report.financial_period_id` در 
reply.md:524:reply.md:334:reply.md:68:`Report.financial_period_id` تا زمان تعیین تکلیف و بازنشستگی کنترل‌شدهٔ مسیر 
legacy باید حفظ 
reply.md:526:reply.md:336:reply.md:71:Report.financial_period_id و مرز writer قدیمی — 2026-11-18
reply.md:527:reply.md:337:reply.md:73:مسیر مشاهده شد `src/ingestion/service.py::ingest_codal_report` است؛ facade در 
reply.md:529:reply.md:339:reply.md:76:`Report.financial_period_id` با ورودی مقایسه می‌شوند؛ اختلاف باعث رد عملیات 
می‌شود.
reply.md:530:reply.md:340:reply.md:78:`financial_period_id=period_id` ثبت می‌شود.
reply.md:531:reply.md:341:reply.md:80:Report.financial_period_id (حذف تدریجی، nullable و descriptive، یا جایگزینی با 
primary-period 
reply.md:533:reply.md:343:reply.md:83:src/ingestion/service.py::ingest_codal_report.
reply.md:534:reply.md:344:reply.md:85:src/ingestion/codal/ingestion.py::ingest_codal_report به writer مرکزی delegate 
می‌کند؛ 
reply.md:535:ingest_codal_pdf 
reply.md:536:reply.md:346:reply.md:88:تابع‌های load_codal_pdf و load_codal_pdf_from_url را دارد و هر دو مسیر در نهایت 
writer مرکزی 
reply.md:538:reply.md:349:financial_period_id 
reply.md:539:reply.md:350:reply.md:92:Report.financial_period_id تلقی کرد.
reply.md:541:Report.financial_period_id در 
reply.md:542:reply.md:353:reply.md:99:`company_id`; free-text `report_type`; FK `financial_period_id` | Reuse, but 
report-type 
reply.md:544:reply.md:356:`financial_periods` 
reply.md:546:`ingest_codal_report(...)` 
reply.md:547:reply.md:359:reply.md:106:database\reports\DB_AUD_012_CODAL_PDF_PATH_DEPENDENCY_AUDIT.md:17:load_codal_pdf
 / 
reply.md:548:reply.md:360:load_codal_pdf_from_url  
reply.md:549:reply.md:361:reply.md:107:database\reports\DB_AUD_012_CODAL_PDF_PATH_DEPENDENCY_AUDIT.md:21:→ 
ingest_codal_report  
reply.md:550:reply.md:362:reply.md:109:ingest_codal_pdf و facade سازگاری ingest_codal_report | بخش PDF-only + facade 
legacy |
reply.md:551:reply.md:364:src/ingestion/service.py::ingest_codal_report | 
reply.md:553:`service.py::ingest_codal_report`: 
reply.md:555:financial_period_id به‌عنوان 
reply.md:557:financial_period_id در مدل فعلی 
reply.md:558:reply.md:371:reply.md:121:`src/ingestion/service.py::ingest_codal_report`:
reply.md:560:ingest_codal_report
reply.md:562:`financial_periods` — 
reply.md:563:reply.md:375:reply.md:127:FinancialPeriod. The current NOT NULL `reports.financial_period_id` must not be 
allowed to 
reply.md:565:reply.md:378:`financial_periods` model 
reply.md:566:reply.md:379:reply.md:132:consumers before making current `reports.financial_period_id` nullable or 
moving it.
reply.md:567:reply.md:380:reply.md:134:`financial_period_id` را جداگانه نگه می‌دارد؛ FKها به‌تنهایی تضمین نمی‌کنند که 
دورهٔ گزارش 
reply.md:569:reply.md:382:reply.md:137:`report_versions.report_id` یا `financial_periods.company_id` تا وقتی Fact 
وابسته وجود دارد 
reply.md:571:reply.md:385:`Report.financial_period_id` در مدل 
reply.md:572:reply.md:386:reply.md:143:pipelineهای load_codal_pdf و load_codal_pdf_from_url |
reply.md:573:reply.md:388:\`src/ingestion/service.py::ingest_codal_report\` | 
reply.md:574:reply.md:389:reply.md:148:پس از شناسایی callerها باید فقط facade PDF حذف و وضعیت ingest_codal_report 
جداگانه تعیین شود 
reply.md:576:reply.md:390:reply.md:150:RawLineInput و ingest_codal_report فعلاً حفظ؛ بعداً با API جدید جایگزین یا 
صریحاً بازنشسته 
reply.md:579:\`ingest_codal_report\` را 
reply.md:580:reply.md:394:`service.py::ingest_codal_report` | 
reply.md:581:reply.md:396:`codal/ingestion.py::ingest_codal_pdf` و 
reply.md:582:reply.md:397:reply.md:162:`ingestion/service.py::ingest_codal_report` (تابع persistence گزارش CODAL) یک 
reply.md:584:reply.md:399:reply.md:166:`ingest_codal_report` و Stage 5 query | Stage 5 مصرف‌کنندهٔ مستقیم خروجی CODAL 
نیست | 
reply.md:586:reply.md:402:`ingest_codal_report` 
reply.md:587:reply.md:404:`financial_period_id` 
reply.md:588:reply.md:406:`financial_periods` |
reply.md:589:reply.md:407:reply.md:176:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:396:2. 
`Report.financial_period_id` 
reply.md:591:reply.md:408:reply.md:177:`ingest_codal_report` یک period_id واحد را به تمام RawFinancialFactهای یک 
report version 
reply.md:593:reply.md:409:reply.md:179:`src/ingestion/service.py::ingest_codal_report`؛ facadeها در 
reply.md:595:reply.md:411:reply.md:183:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:422:| 
`financial_periods` | در مسیر 
reply.md:598:`Report.financial_period_id` 
reply.md:599:reply.md:415:reply.md:191:محدودیت را دارد. متد `ingest_codal_report` یک `period_id` می‌گیرد و همان مقدار 
را برای همهٔ 
reply.md:600:reply.md:417:reply.md:193:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:477:4. 
`Report.financial_period_id` 
reply.md:602:reply.md:419:reply.md:198:association، الزامی/اختیاری بودن `Report.financial_period_id` قدیمی و نگاشت 
نسخه‌های اصلاحی 
reply.md:604:reply.md:421:reply.md:201:`src/ingestion/service.py::ingest_codal_report` مستقیماً برای هر `RawLineInput` 
یک 
reply.md:606:reply.md:423:reply.md:207:`src/ingestion/service.py::ingest_codal_report` می‌رسند؛ این تابع برای هر 
RawLineInput یک 
reply.md:607:reply.md:425:reply.md:212:`service.py::ingest_codal_report` → RawFinancialFact.
reply.md:609:`codal/ingestion.py::ingest_codal_report` 
reply.md:610:reply.md:428:reply.md:214:است و به writer مرکزی `service.py::ingest_codal_report` می‌رسد.
reply.md:612:`codal/ingestion.py::ingest_codal_pdf` 
reply.md:614:`codal/pipeline.py::load_codal_pdf` و 
reply.md:615:reply.md:432:reply.md:219:`load_codal_pdf_from_url` acquisition/extraction/validation را پیش از writer 
اجرا می‌کنند؛ 
reply.md:618:`reports.financial_period_id`، چون پیش 
reply.md:619:reply.md:436:reply.md:226:`reports.financial_period_id` و تفکیک قرارداد legacy CODAL از Excel — 2026-11-18
reply.md:621:`Report.financial_period_id` در ORM 
reply.md:622:reply.md:439:reply.md:230:`service.py::ingest_codal_report` delegate می‌کند؛ PDF wrapper پس از extraction 
از آن 
reply.md:624:reply.md:441:reply.md:232:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1718:- نام 
`financial_period_id` در 
reply.md:625:reply.md:443:reply.md:233:observation DTOها و تست‌های Stage 5/6 لزوماً به ستون 
`reports.financial_period_id` اشاره 
reply.md:627:reply.md:445:reply.md:237:`Report.financial_period_id` مجاز نیست. مسیر جدید Excel باید دوره را در سطح هر 
Fact تعیین 
reply.md:629:reply.md:447:reply.md:243:`report_versions.report_id` و `financial_periods.company_id` تا وقتی Fact 
وابسته وجود دارد 
reply.md:631:reply.md:449:reply.md:244:`Report.financial_period_id` به‌صورت optional metadata باقی ماند، در صورت 
non-NULL بودن 
reply.md:633:reply.md:451:reply.md:246:writer قدیمی به Report.financial_period_id — 2026-11-18
reply.md:635:`service.py::ingest_codal_report` writer 
reply.md:636:reply.md:454:reply.md:250:`Report.financial_period_id` باید با ورودی یکسان باشند؛ در غیر این صورت عملیات 
رد می‌شود.
reply.md:637:reply.md:455:reply.md:253:src/ingestion/service.py::ingest_codal_report است؛ facade در 
reply.md:639:reply.md:457:reply.md:256:database\DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md:1898:کاربردهای 
financial_period_id 
reply.md:642:Report.financial_period_id شمرده 
reply.md:644:Report.financial_period_id 
reply.md:645:reply.md:463:reply.md:265:`ingest_codal_report` take DTOs |
reply.md:646:reply.md:465:`ingest_codal_report` accepts 
reply.md:647:reply.md:466:reply.md:268:prompts\10_Implementation_Status.md:243:ingest_codal_report()
reply.md:648:reply.md:467:reply.md:269:src\tests\final_validation_audit.md:140:  → ingest_codal_report()
reply.md:649:reply.md:468:reply.md:270:src\tests\golden_audit_source_plan.md:15:ingest_codal_report()
reply.md:650:reply.md:470:ingest_codal_report()
reply.md:651:reply.md:471:reply.md:272:01_Stage1_Data_Foundation.md:278:financial_period_id
reply.md:652:reply.md:472:reply.md:275:(models cover industries/companies, financial_periods, reports/report_versions, 
raw 
reply.md:653:reply.md:473:reply.md:282:10_Production_Codal_Extraction_and_Data_Load.md:22:ingest_codal_report()
reply.md:654:reply.md:475:ingest_codal_report()`
reply.md:655:reply.md:476:reply.md:284:11_Production_Data_Load_and_Foundation_Validation.md:136:ingest_codal_report()
reply.md:656:reply.md:477:reply.md:285:12_Database_Architecture_V1.1.md:104:- `financial_periods`
reply.md:657:reply.md:478:reply.md:286:12_Database_Architecture_V1.1.md:801:ingest_codal_report / ingest_ohlc_* / 
ingest_fx_rates
reply.md:658:reply.md:479:reply.md:288:consumed by `ingest_codal_report`; the existing downstream persistence boundary 
must remain 
reply.md:659:reply.md:481:reply.md:289:99_Architecture_Change_Log.md:386:  ingest_codal_report / ingest_ohlc_* / 
ingest_fx_rates
reply.md:660:reply.md:482:reply.md:291:is a **pre-ingestion** responsibility. `ingest_codal_report` receives 
already-extracted 
reply.md:662:reply.md:484:reply.md:294:PROJECT_HANDOFF_INSTRUCTIONS.md:252:    ingest_codal_report()
reply.md:663:reply.md:485:reply.md:295:reply.md:4:PDF را استخراج می‌کنند، خروجی `RawLineInput` می‌سازند و 
`ingest_codal_report()` 
reply.md:665:reply.md:487:reply.md:297:reply.md:8:`src/ingestion/service.py` | `RawLineInput`، `ingest_codal_report`، 
transaction و 
reply.md:667:reply.md:488:reply.md:298:reply.md:10:از `load_codal_pdf` و PDFهای fixture استفاده می‌کند.
reply.md:668:reply.md:490:`ingest_codal_report()`:
reply.md:669:reply.md:491:reply.md:300:reply.md:13:`financial_period_id` است، درحالی‌که قرارداد منطقی می‌گوید یک 
ReportVersion 
reply.md:671:reply.md:494:`ingest_codal_report()` 
reply.md:672:reply.md:495:reply.md:305:`ingest_codal_report`
reply.md:673:reply.md:496:reply.md:306:reply.md:19:`src/ingestion/codal/ingestion.py::ingest_codal_report` صرفاً 
facade سازگاری است 
reply.md:675:reply.md:497:reply.md:307:reply.md:20:`src/ingestion/service.py::ingest_codal_report` delegate می‌کند؛ 
transaction 
reply.md:677:reply.md:498:reply.md:308:reply.md:22:`src/ingestion/codal/ingestion.py::ingest_codal_pdf` extraction را 
اجرا می‌کند و 
reply.md:679:reply.md:500:reply.md:310:reply.md:26:`src/ingestion/codal/pipeline.py::load_codal_pdf` و 
`load_codal_pdf_from_url` 
reply.md:681:reply.md:502:reply.md:312:reply.md:30:`src/ingestion/service.py::ingest_codal_report` writer اصلی 
reply.md:682:reply.md:504:reply.md:314:reply.md:36:`reports.financial_period_id` پیش از nullable کردن/جابه‌جایی آن 
است. سپس gateهای 
reply.md:683:reply.md:506:reply.md:315:reply.md:39:`reports.financial_period_id` و مسیرهای فراخوانی CODAL — 2026-11-18
reply.md:684:reply.md:507:reply.md:316:reply.md:41:`financial_period_id|FinancialPeriod` در کل فایل‌های `*.py` و 
`*.sql` زیر 
reply.md:686:reply.md:509:reply.md:318:reply.md:43:`Report.financial_period_id` با `nullable=False` و FK به 
reply.md:687:`financial_periods.period_id`.
reply.md:688:reply.md:510:reply.md:319:reply.md:46:`Report.financial_period_id` استفاده نشده است.
reply.md:689:reply.md:511:reply.md:320:reply.md:48:تست‌های Stage 5/6: نام `financial_period_id` در DTOها و مدل‌های 
ارزیابی به‌عنوان 
reply.md:691:reply.md:512:reply.md:322:reply.md:49:استفاده شده است؛ این موارد به‌تنهایی مصرف ستون 
`reports.financial_period_id` 
reply.md:693:reply.md:513:reply.md:323:reply.md:51:Report و قرارداد قدیمی را با `financial_period_id` اجباری 
می‌آزمایند؛ تست‌های 
reply.md:695:reply.md:515:reply.md:325:reply.md:54:تابع عمومی `ingest_codal_report` یک facade سازگار با گذشته است و به 
reply.md:696:reply.md:516:reply.md:326:`src.ingestion.service.ingest_codal_report` 
reply.md:697:reply.md:517:reply.md:327:reply.md:55:delegate می‌کند. تابع `ingest_codal_pdf` پس از extraction همین 
facade را 
reply.md:699:reply.md:518:reply.md:328:reply.md:57:توابع `load_codal_pdf` و `load_codal_pdf_from_url` پس از 
reply.md:701:reply.md:520:reply.md:329:reply.md:58:`src.ingestion.service.ingest_codal_report` را فراخوانی می‌کنند.
reply.md:702:reply.md:521:reply.md:330:reply.md:61:`financial_period_id` ندارند؛ این با یافتهٔ قبلی DB-AUD-013 مبنی بر 
نبود 
reply.md:704:reply.md:523:reply.md:333:`Report.financial_period_id` در 
reply.md:705:reply.md:524:reply.md:334:reply.md:68:`Report.financial_period_id` تا زمان تعیین تکلیف و بازنشستگی 
کنترل‌شدهٔ مسیر 
reply.md:707:reply.md:526:reply.md:336:reply.md:71:Report.financial_period_id و مرز writer قدیمی — 2026-11-18
reply.md:708:reply.md:527:reply.md:337:reply.md:73:مسیر مشاهده شد `src/ingestion/service.py::ingest_codal_report` است؛ 
facade در 
reply.md:709:reply.md:529:reply.md:339:reply.md:76:`Report.financial_period_id` با ورودی مقایسه می‌شوند؛ اختلاف باعث 
رد عملیات 
reply.md:711:reply.md:530:reply.md:340:reply.md:78:`financial_period_id=period_id` ثبت می‌شود.
reply.md:712:reply.md:531:reply.md:341:reply.md:80:Report.financial_period_id (حذف تدریجی، nullable و descriptive، یا 
جایگزینی با 
reply.md:714:reply.md:533:reply.md:343:reply.md:83:src/ingestion/service.py::ingest_codal_report.
reply.md:715:reply.md:534:reply.md:344:reply.md:85:src/ingestion/codal/ingestion.py::ingest_codal_report به writer 
مرکزی delegate 
reply.md:717:reply.md:535:ingest_codal_pdf 
reply.md:718:reply.md:536:reply.md:346:reply.md:88:تابع‌های load_codal_pdf و load_codal_pdf_from_url را دارد و هر دو 
مسیر در نهایت 
reply.md:720:reply.md:538:reply.md:349:financial_period_id 
reply.md:721:reply.md:539:reply.md:350:reply.md:92:Report.financial_period_id تلقی کرد.
reply.md:722:reply.md:541:Report.financial_period_id در 
reply.md:723:reply.md:542:reply.md:353:reply.md:99:`company_id`; free-text `report_type`; FK `financial_period_id` | 
Reuse, but 
reply.md:725:reply.md:544:reply.md:356:`financial_periods` 
reply.md:726:reply.md:546:`ingest_codal_report(...)` 
reply.md:727:reply.md:547:reply.md:359:reply.md:106:database\reports\DB_AUD_012_CODAL_PDF_PATH_DEPENDENCY_AUDIT.md:17:l
oad_codal_pdf
reply.md:729:reply.md:548:reply.md:360:load_codal_pdf_from_url  
reply.md:731:ingest_codal_report  
reply.md:732:reply.md:550:reply.md:362:reply.md:109:ingest_codal_pdf و facade سازگاری ingest_codal_report | بخش 
PDF-only + facade 
reply.md:734:reply.md:551:reply.md:364:src/ingestion/service.py::ingest_codal_report | 
reply.md:735:reply.md:553:`service.py::ingest_codal_report`: 
reply.md:736:reply.md:555:financial_period_id به‌عنوان 
reply.md:737:reply.md:557:financial_period_id در مدل فعلی 
reply.md:738:reply.md:558:reply.md:371:reply.md:121:`src/ingestion/service.py::ingest_codal_report`:
reply.md:739:reply.md:560:ingest_codal_report
reply.md:740:reply.md:562:`financial_periods` — 
reply.md:741:reply.md:563:reply.md:375:reply.md:127:FinancialPeriod. The current NOT NULL 
`reports.financial_period_id` must not be 
reply.md:743:reply.md:565:reply.md:378:`financial_periods` model 
reply.md:744:reply.md:566:reply.md:379:reply.md:132:consumers before making current `reports.financial_period_id` 
nullable or 
reply.md:746:reply.md:567:reply.md:380:reply.md:134:`financial_period_id` را جداگانه نگه می‌دارد؛ FKها به‌تنهایی تضمین 
نمی‌کنند که 
reply.md:748:reply.md:569:reply.md:382:reply.md:137:`report_versions.report_id` یا `financial_periods.company_id` تا 
وقتی Fact 
reply.md:750:reply.md:571:reply.md:385:`Report.financial_period_id` در مدل 
reply.md:751:reply.md:572:reply.md:386:reply.md:143:pipelineهای load_codal_pdf و load_codal_pdf_from_url |
reply.md:752:reply.md:573:reply.md:388:\`src/ingestion/service.py::ingest_codal_report\` | 
reply.md:753:reply.md:574:reply.md:389:reply.md:148:پس از شناسایی callerها باید فقط facade PDF حذف و وضعیت 
ingest_codal_report 
reply.md:755:reply.md:576:reply.md:390:reply.md:150:RawLineInput و ingest_codal_report فعلاً حفظ؛ بعداً با API جدید 
جایگزین یا 
reply.md:757:reply.md:579:\`ingest_codal_report\` را 
reply.md:758:reply.md:580:reply.md:394:`service.py::ingest_codal_report` | 
reply.md:759:reply.md:581:reply.md:396:`codal/ingestion.py::ingest_codal_pdf` و 
reply.md:760:reply.md:582:reply.md:397:reply.md:162:`ingestion/service.py::ingest_codal_report` (تابع persistence 
گزارش CODAL) یک 
reply.md:761:reply.md:584:reply.md:399:reply.md:166:`ingest_codal_report` و Stage 5 query | Stage 5 مصرف‌کنندهٔ مستقیم 
خروجی CODAL 
reply.md:763:reply.md:586:reply.md:402:`ingest_codal_report` 
reply.md:764:reply.md:587:reply.md:404:`financial_period_id` 
reply.md:765:reply.md:588:reply.md:406:`financial_periods` |
reply.md:767:`Report.financial_period_id` 
reply.md:768:reply.md:591:reply.md:408:reply.md:177:`ingest_codal_report` یک period_id واحد را به تمام 
RawFinancialFactهای یک 
reply.md:770:reply.md:593:reply.md:409:reply.md:179:`src/ingestion/service.py::ingest_codal_report`؛ facadeها در 
reply.md:772:`financial_periods` | در مسیر 
reply.md:773:reply.md:598:`Report.financial_period_id` 
reply.md:774:reply.md:599:reply.md:415:reply.md:191:محدودیت را دارد. متد `ingest_codal_report` یک `period_id` می‌گیرد 
و همان مقدار 
reply.md:777:`Report.financial_period_id` 
reply.md:778:reply.md:602:reply.md:419:reply.md:198:association، الزامی/اختیاری بودن `Report.financial_period_id` 
قدیمی و نگاشت 
reply.md:780:reply.md:604:reply.md:421:reply.md:201:`src/ingestion/service.py::ingest_codal_report` مستقیماً برای هر 
`RawLineInput` 
reply.md:782:reply.md:606:reply.md:423:reply.md:207:`src/ingestion/service.py::ingest_codal_report` می‌رسند؛ این تابع 
برای هر 
reply.md:784:reply.md:607:reply.md:425:reply.md:212:`service.py::ingest_codal_report` → RawFinancialFact.
reply.md:785:reply.md:609:`codal/ingestion.py::ingest_codal_report` 
reply.md:786:reply.md:610:reply.md:428:reply.md:214:است و به writer مرکزی `service.py::ingest_codal_report` می‌رسد.
reply.md:787:reply.md:612:`codal/ingestion.py::ingest_codal_pdf` 
reply.md:788:reply.md:614:`codal/pipeline.py::load_codal_pdf` و 
reply.md:789:reply.md:615:reply.md:432:reply.md:219:`load_codal_pdf_from_url` acquisition/extraction/validation را پیش 
از writer 
reply.md:791:reply.md:618:`reports.financial_period_id`، چون پیش 
reply.md:792:reply.md:619:reply.md:436:reply.md:226:`reports.financial_period_id` و تفکیک قرارداد legacy CODAL از 
Excel — 2026-11-18
reply.md:793:reply.md:621:`Report.financial_period_id` در ORM 
reply.md:794:reply.md:622:reply.md:439:reply.md:230:`service.py::ingest_codal_report` delegate می‌کند؛ PDF wrapper پس 
از extraction 
reply.md:797:`financial_period_id` در 
reply.md:799:`reports.financial_period_id` اشاره 
reply.md:800:reply.md:627:reply.md:445:reply.md:237:`Report.financial_period_id` مجاز نیست. مسیر جدید Excel باید دوره 
را در سطح هر 
reply.md:802:reply.md:629:reply.md:447:reply.md:243:`report_versions.report_id` و `financial_periods.company_id` تا 
وقتی Fact 
reply.md:804:reply.md:631:reply.md:449:reply.md:244:`Report.financial_period_id` به‌صورت optional metadata باقی ماند، 
در صورت 
reply.md:806:reply.md:633:reply.md:451:reply.md:246:writer قدیمی به Report.financial_period_id — 2026-11-18
reply.md:807:reply.md:635:`service.py::ingest_codal_report` writer 
reply.md:808:reply.md:636:reply.md:454:reply.md:250:`Report.financial_period_id` باید با ورودی یکسان باشند؛ در غیر این 
صورت عملیات 
reply.md:810:reply.md:637:reply.md:455:reply.md:253:src/ingestion/service.py::ingest_codal_report است؛ facade در 
reply.md:812:financial_period_id 
reply.md:813:reply.md:642:Report.financial_period_id شمرده 
reply.md:814:reply.md:644:Report.financial_period_id 
reply.md:815:reply.md:645:reply.md:463:reply.md:265:`ingest_codal_report` take DTOs |
reply.md:816:reply.md:646:reply.md:465:`ingest_codal_report` accepts 
reply.md:817:reply.md:647:reply.md:466:reply.md:268:prompts\10_Implementation_Status.md:243:ingest_codal_report()
reply.md:818:reply.md:648:reply.md:467:reply.md:269:src\tests\final_validation_audit.md:140:  → ingest_codal_report()
reply.md:819:reply.md:649:reply.md:468:reply.md:270:src\tests\golden_audit_source_plan.md:15:ingest_codal_report()
reply.md:820:reply.md:650:reply.md:470:ingest_codal_report()
reply.md:821:reply.md:651:reply.md:471:reply.md:272:01_Stage1_Data_Foundation.md:278:financial_period_id
reply.md:822:reply.md:652:reply.md:472:reply.md:275:(models cover industries/companies, financial_periods, 
reports/report_versions, 
reply.md:824:reply.md:653:reply.md:473:reply.md:282:10_Production_Codal_Extraction_and_Data_Load.md:22:ingest_codal_rep
ort()
reply.md:825:reply.md:654:reply.md:475:ingest_codal_report()`
reply.md:826:reply.md:655:reply.md:476:reply.md:284:11_Production_Data_Load_and_Foundation_Validation.md:136:ingest_cod
al_report()
reply.md:827:reply.md:656:reply.md:477:reply.md:285:12_Database_Architecture_V1.1.md:104:- `financial_periods`
reply.md:828:reply.md:657:reply.md:478:reply.md:286:12_Database_Architecture_V1.1.md:801:ingest_codal_report / 
ingest_ohlc_* / 
reply.md:830:reply.md:658:reply.md:479:reply.md:288:consumed by `ingest_codal_report`; the existing downstream 
persistence boundary 
reply.md:832:reply.md:659:reply.md:481:reply.md:289:99_Architecture_Change_Log.md:386:  ingest_codal_report / 
ingest_ohlc_* / 
reply.md:834:reply.md:660:reply.md:482:reply.md:291:is a **pre-ingestion** responsibility. `ingest_codal_report` 
receives 
reply.md:836:reply.md:662:reply.md:484:reply.md:294:PROJECT_HANDOFF_INSTRUCTIONS.md:252:    ingest_codal_report()
reply.md:838:`ingest_codal_report()` 
reply.md:839:reply.md:665:reply.md:487:reply.md:297:reply.md:8:`src/ingestion/service.py` | `RawLineInput`، 
`ingest_codal_report`، 
reply.md:841:reply.md:667:reply.md:488:reply.md:298:reply.md:10:از `load_codal_pdf` و PDFهای fixture استفاده می‌کند.
reply.md:842:reply.md:668:reply.md:490:`ingest_codal_report()`:
reply.md:843:reply.md:669:reply.md:491:reply.md:300:reply.md:13:`financial_period_id` است، درحالی‌که قرارداد منطقی 
می‌گوید یک 
reply.md:845:reply.md:671:reply.md:494:`ingest_codal_report()` 
reply.md:846:reply.md:672:reply.md:495:reply.md:305:`ingest_codal_report`
reply.md:847:reply.md:673:reply.md:496:reply.md:306:reply.md:19:`src/ingestion/codal/ingestion.py::ingest_codal_report`
 صرفاً 
reply.md:849:reply.md:675:reply.md:497:reply.md:307:reply.md:20:`src/ingestion/service.py::ingest_codal_report` 
delegate می‌کند؛ 
reply.md:851:reply.md:677:reply.md:498:reply.md:308:reply.md:22:`src/ingestion/codal/ingestion.py::ingest_codal_pdf` 
extraction را 
reply.md:853:reply.md:679:reply.md:500:reply.md:310:reply.md:26:`src/ingestion/codal/pipeline.py::load_codal_pdf` و 
reply.md:854:`load_codal_pdf_from_url` 
reply.md:855:reply.md:681:reply.md:502:reply.md:312:reply.md:30:`src/ingestion/service.py::ingest_codal_report` writer 
اصلی 
reply.md:856:reply.md:682:reply.md:504:reply.md:314:reply.md:36:`reports.financial_period_id` پیش از nullable 
کردن/جابه‌جایی آن 
reply.md:858:reply.md:683:reply.md:506:reply.md:315:reply.md:39:`reports.financial_period_id` و مسیرهای فراخوانی CODAL 
— 2026-11-18
reply.md:859:reply.md:684:reply.md:507:reply.md:316:reply.md:41:`financial_period_id|FinancialPeriod` در کل فایل‌های 
`*.py` و 
reply.md:861:reply.md:686:reply.md:509:reply.md:318:reply.md:43:`Report.financial_period_id` با `nullable=False` و FK 
به 
reply.md:862:reply.md:687:`financial_periods.period_id`.
reply.md:863:reply.md:688:reply.md:510:reply.md:319:reply.md:46:`Report.financial_period_id` استفاده نشده است.
reply.md:864:reply.md:689:reply.md:511:reply.md:320:reply.md:48:تست‌های Stage 5/6: نام `financial_period_id` در DTOها 
و مدل‌های 
reply.md:867:`reports.financial_period_id` 
reply.md:868:reply.md:693:reply.md:513:reply.md:323:reply.md:51:Report و قرارداد قدیمی را با `financial_period_id` 
اجباری 
reply.md:870:reply.md:695:reply.md:515:reply.md:325:reply.md:54:تابع عمومی `ingest_codal_report` یک facade سازگار با 
گذشته است و به 
reply.md:871:reply.md:696:reply.md:516:reply.md:326:`src.ingestion.service.ingest_codal_report` 
reply.md:872:reply.md:697:reply.md:517:reply.md:327:reply.md:55:delegate می‌کند. تابع `ingest_codal_pdf` پس از 
extraction همین 
reply.md:874:reply.md:699:reply.md:518:reply.md:328:reply.md:57:توابع `load_codal_pdf` و `load_codal_pdf_from_url` پس 
از 
reply.md:875:reply.md:701:reply.md:520:reply.md:329:reply.md:58:`src.ingestion.service.ingest_codal_report` را 
فراخوانی می‌کنند.
reply.md:876:reply.md:702:reply.md:521:reply.md:330:reply.md:61:`financial_period_id` ندارند؛ این با یافتهٔ قبلی 
DB-AUD-013 مبنی بر 
reply.md:878:reply.md:704:reply.md:523:reply.md:333:`Report.financial_period_id` در 
reply.md:879:reply.md:705:reply.md:524:reply.md:334:reply.md:68:`Report.financial_period_id` تا زمان تعیین تکلیف و 
بازنشستگی 
reply.md:881:reply.md:707:reply.md:526:reply.md:336:reply.md:71:Report.financial_period_id و مرز writer قدیمی — 
2026-11-18
reply.md:882:reply.md:708:reply.md:527:reply.md:337:reply.md:73:مسیر مشاهده شد 
`src/ingestion/service.py::ingest_codal_report` است؛ 
reply.md:884:reply.md:709:reply.md:529:reply.md:339:reply.md:76:`Report.financial_period_id` با ورودی مقایسه می‌شوند؛ 
اختلاف باعث 
reply.md:886:reply.md:711:reply.md:530:reply.md:340:reply.md:78:`financial_period_id=period_id` ثبت می‌شود.
reply.md:887:reply.md:712:reply.md:531:reply.md:341:reply.md:80:Report.financial_period_id (حذف تدریجی، nullable و 
descriptive، یا 
reply.md:889:reply.md:714:reply.md:533:reply.md:343:reply.md:83:src/ingestion/service.py::ingest_codal_report.
reply.md:890:reply.md:715:reply.md:534:reply.md:344:reply.md:85:src/ingestion/codal/ingestion.py::ingest_codal_report 
به writer 
reply.md:892:reply.md:717:reply.md:535:ingest_codal_pdf 
reply.md:893:reply.md:718:reply.md:536:reply.md:346:reply.md:88:تابع‌های load_codal_pdf و load_codal_pdf_from_url را 
دارد و هر دو 
reply.md:895:reply.md:720:reply.md:538:reply.md:349:financial_period_id 
reply.md:896:reply.md:721:reply.md:539:reply.md:350:reply.md:92:Report.financial_period_id تلقی کرد.
reply.md:897:reply.md:722:reply.md:541:Report.financial_period_id در 
reply.md:898:reply.md:723:reply.md:542:reply.md:353:reply.md:99:`company_id`; free-text `report_type`; FK 
`financial_period_id` | 
reply.md:900:reply.md:725:reply.md:544:reply.md:356:`financial_periods` 
reply.md:901:reply.md:726:reply.md:546:`ingest_codal_report(...)` 
reply.md:904:reply.md:729:reply.md:548:reply.md:360:load_codal_pdf_from_url  
reply.md:905:reply.md:731:ingest_codal_report  
reply.md:906:reply.md:732:reply.md:550:reply.md:362:reply.md:109:ingest_codal_pdf و facade سازگاری ingest_codal_report 
| بخش 
reply.md:908:reply.md:734:reply.md:551:reply.md:364:src/ingestion/service.py::ingest_codal_report | 
reply.md:909:reply.md:735:reply.md:553:`service.py::ingest_codal_report`: 
reply.md:910:reply.md:736:reply.md:555:financial_period_id به‌عنوان 
reply.md:911:reply.md:737:reply.md:557:financial_period_id در مدل فعلی 
reply.md:912:reply.md:738:reply.md:558:reply.md:371:reply.md:121:`src/ingestion/service.py::ingest_codal_report`:
reply.md:913:reply.md:739:reply.md:560:ingest_codal_report
reply.md:914:reply.md:740:reply.md:562:`financial_periods` — 
reply.md:916:`reports.financial_period_id` must not be 
reply.md:917:reply.md:743:reply.md:565:reply.md:378:`financial_periods` model 
reply.md:918:reply.md:744:reply.md:566:reply.md:379:reply.md:132:consumers before making current 
`reports.financial_period_id` 
reply.md:920:reply.md:746:reply.md:567:reply.md:380:reply.md:134:`financial_period_id` را جداگانه نگه می‌دارد؛ FKها 
به‌تنهایی تضمین 
reply.md:922:reply.md:748:reply.md:569:reply.md:382:reply.md:137:`report_versions.report_id` یا 
`financial_periods.company_id` تا 
reply.md:924:reply.md:750:reply.md:571:reply.md:385:`Report.financial_period_id` در مدل 
reply.md:925:reply.md:751:reply.md:572:reply.md:386:reply.md:143:pipelineهای load_codal_pdf و load_codal_pdf_from_url |
reply.md:926:reply.md:752:reply.md:573:reply.md:388:\`src/ingestion/service.py::ingest_codal_report\` | 
reply.md:928:ingest_codal_report 
reply.md:929:reply.md:755:reply.md:576:reply.md:390:reply.md:150:RawLineInput و ingest_codal_report فعلاً حفظ؛ بعداً 
با API جدید 
reply.md:931:reply.md:757:reply.md:579:\`ingest_codal_report\` را 
reply.md:932:reply.md:758:reply.md:580:reply.md:394:`service.py::ingest_codal_report` | 
reply.md:933:reply.md:759:reply.md:581:reply.md:396:`codal/ingestion.py::ingest_codal_pdf` و 
reply.md:934:reply.md:760:reply.md:582:reply.md:397:reply.md:162:`ingestion/service.py::ingest_codal_report` (تابع 
persistence 
reply.md:936:reply.md:761:reply.md:584:reply.md:399:reply.md:166:`ingest_codal_report` و Stage 5 query | Stage 5 
مصرف‌کنندهٔ مستقیم 
reply.md:938:reply.md:763:reply.md:586:reply.md:402:`ingest_codal_report` 
reply.md:939:reply.md:764:reply.md:587:reply.md:404:`financial_period_id` 
reply.md:940:reply.md:765:reply.md:588:reply.md:406:`financial_periods` |
reply.md:941:reply.md:767:`Report.financial_period_id` 
reply.md:942:reply.md:768:reply.md:591:reply.md:408:reply.md:177:`ingest_codal_report` یک period_id واحد را به تمام 
reply.md:944:reply.md:770:reply.md:593:reply.md:409:reply.md:179:`src/ingestion/service.py::ingest_codal_report`؛ 
facadeها در 
reply.md:945:reply.md:772:`financial_periods` | در مسیر 
reply.md:946:reply.md:773:reply.md:598:`Report.financial_period_id` 
reply.md:947:reply.md:774:reply.md:599:reply.md:415:reply.md:191:محدودیت را دارد. متد `ingest_codal_report` یک 
`period_id` می‌گیرد 
reply.md:949:reply.md:777:`Report.financial_period_id` 
reply.md:950:reply.md:778:reply.md:602:reply.md:419:reply.md:198:association، الزامی/اختیاری بودن 
`Report.financial_period_id` 
reply.md:952:reply.md:780:reply.md:604:reply.md:421:reply.md:201:`src/ingestion/service.py::ingest_codal_report` 
مستقیماً برای هر 
reply.md:954:reply.md:782:reply.md:606:reply.md:423:reply.md:207:`src/ingestion/service.py::ingest_codal_report` 
می‌رسند؛ این تابع 
reply.md:956:reply.md:784:reply.md:607:reply.md:425:reply.md:212:`service.py::ingest_codal_report` → RawFinancialFact.
reply.md:957:reply.md:785:reply.md:609:`codal/ingestion.py::ingest_codal_report` 
reply.md:958:reply.md:786:reply.md:610:reply.md:428:reply.md:214:است و به writer مرکزی 
`service.py::ingest_codal_report` می‌رسد.
reply.md:959:reply.md:787:reply.md:612:`codal/ingestion.py::ingest_codal_pdf` 
reply.md:960:reply.md:788:reply.md:614:`codal/pipeline.py::load_codal_pdf` و 
reply.md:961:reply.md:789:reply.md:615:reply.md:432:reply.md:219:`load_codal_pdf_from_url` 
acquisition/extraction/validation را پیش 
reply.md:963:reply.md:791:reply.md:618:`reports.financial_period_id`، چون پیش 
reply.md:964:reply.md:792:reply.md:619:reply.md:436:reply.md:226:`reports.financial_period_id` و تفکیک قرارداد legacy 
CODAL از 
reply.md:966:reply.md:793:reply.md:621:`Report.financial_period_id` در ORM 
reply.md:967:reply.md:794:reply.md:622:reply.md:439:reply.md:230:`service.py::ingest_codal_report` delegate می‌کند؛ 
PDF wrapper پس 
reply.md:969:reply.md:797:`financial_period_id` در 
reply.md:970:reply.md:799:`reports.financial_period_id` اشاره 
reply.md:971:reply.md:800:reply.md:627:reply.md:445:reply.md:237:`Report.financial_period_id` مجاز نیست. مسیر جدید 
Excel باید دوره 
reply.md:973:reply.md:802:reply.md:629:reply.md:447:reply.md:243:`report_versions.report_id` و 
`financial_periods.company_id` تا 
reply.md:975:reply.md:804:reply.md:631:reply.md:449:reply.md:244:`Report.financial_period_id` به‌صورت optional 
metadata باقی ماند، 
reply.md:977:reply.md:806:reply.md:633:reply.md:451:reply.md:246:writer قدیمی به Report.financial_period_id — 
2026-11-18
reply.md:978:reply.md:807:reply.md:635:`service.py::ingest_codal_report` writer 
reply.md:979:reply.md:808:reply.md:636:reply.md:454:reply.md:250:`Report.financial_period_id` باید با ورودی یکسان 
باشند؛ در غیر این 
reply.md:981:reply.md:810:reply.md:637:reply.md:455:reply.md:253:src/ingestion/service.py::ingest_codal_report است؛ 
facade در 
reply.md:982:reply.md:812:financial_period_id 
reply.md:983:reply.md:813:reply.md:642:Report.financial_period_id شمرده 
reply.md:984:reply.md:814:reply.md:644:Report.financial_period_id 
reply.md:985:reply.md:815:reply.md:645:reply.md:463:reply.md:265:`ingest_codal_report` take DTOs |
reply.md:986:reply.md:816:reply.md:646:reply.md:465:`ingest_codal_report` accepts 
reply.md:987:reply.md:817:reply.md:647:reply.md:466:reply.md:268:prompts\10_Implementation_Status.md:243:ingest_codal_r
eport()
reply.md:988:reply.md:818:reply.md:648:reply.md:467:reply.md:269:src\tests\final_validation_audit.md:140:  → 
ingest_codal_report()
reply.md:989:reply.md:819:reply.md:649:reply.md:468:reply.md:270:src\tests\golden_audit_source_plan.md:15:ingest_codal_
report()
reply.md:990:reply.md:820:reply.md:650:reply.md:470:ingest_codal_report()
reply.md:991:reply.md:821:reply.md:651:reply.md:471:reply.md:272:01_Stage1_Data_Foundation.md:278:financial_period_id
reply.md:992:reply.md:822:reply.md:652:reply.md:472:reply.md:275:(models cover industries/companies, 
financial_periods, 
reply.md:996:reply.md:825:reply.md:654:reply.md:475:ingest_codal_report()`
reply.md:999:reply.md:827:reply.md:656:reply.md:477:reply.md:285:12_Database_Architecture_V1.1.md:104:- 
`financial_periods`
reply.md:1000:reply.md:828:reply.md:657:reply.md:478:reply.md:286:12_Database_Architecture_V1.1.md:801:ingest_codal_rep
ort / 
reply.md:1002:reply.md:830:reply.md:658:reply.md:479:reply.md:288:consumed by `ingest_codal_report`; the existing 
downstream 
reply.md:1004:reply.md:832:reply.md:659:reply.md:481:reply.md:289:99_Architecture_Change_Log.md:386:  
ingest_codal_report / 
reply.md:1006:reply.md:834:reply.md:660:reply.md:482:reply.md:291:is a **pre-ingestion** responsibility. 
`ingest_codal_report` 
reply.md:1008:reply.md:836:reply.md:662:reply.md:484:reply.md:294:PROJECT_HANDOFF_INSTRUCTIONS.md:252:    
ingest_codal_report()
reply.md:1009:reply.md:838:`ingest_codal_report()` 
reply.md:1011:`ingest_codal_report`، 
reply.md:1012:reply.md:841:reply.md:667:reply.md:488:reply.md:298:reply.md:10:از `load_codal_pdf` و PDFهای fixture 
استفاده می‌کند.
reply.md:1013:reply.md:842:reply.md:668:reply.md:490:`ingest_codal_report()`:
reply.md:1014:reply.md:843:reply.md:669:reply.md:491:reply.md:300:reply.md:13:`financial_period_id` است، درحالی‌که 
قرارداد منطقی 
reply.md:1016:reply.md:845:reply.md:671:reply.md:494:`ingest_codal_report()` 
reply.md:1017:reply.md:846:reply.md:672:reply.md:495:reply.md:305:`ingest_codal_report`
reply.md:1018:reply.md:847:reply.md:673:reply.md:496:reply.md:306:reply.md:19:`src/ingestion/codal/ingestion.py::ingest
_codal_report`
reply.md:1020:reply.md:849:reply.md:675:reply.md:497:reply.md:307:reply.md:20:`src/ingestion/service.py::ingest_codal_r
eport` 
reply.md:1022:reply.md:851:reply.md:677:reply.md:498:reply.md:308:reply.md:22:`src/ingestion/codal/ingestion.py::ingest
_codal_pdf` 
reply.md:1024:reply.md:853:reply.md:679:reply.md:500:reply.md:310:reply.md:26:`src/ingestion/codal/pipeline.py::load_co
dal_pdf` و 
reply.md:1025:reply.md:854:`load_codal_pdf_from_url` 
reply.md:1026:reply.md:855:reply.md:681:reply.md:502:reply.md:312:reply.md:30:`src/ingestion/service.py::ingest_codal_r
eport` writer 
reply.md:1028:reply.md:856:reply.md:682:reply.md:504:reply.md:314:reply.md:36:`reports.financial_period_id` پیش از 
nullable 
reply.md:1030:reply.md:858:reply.md:683:reply.md:506:reply.md:315:reply.md:39:`reports.financial_period_id` و مسیرهای 
فراخوانی CODAL 
reply.md:1032:reply.md:859:reply.md:684:reply.md:507:reply.md:316:reply.md:41:`financial_period_id|FinancialPeriod` در 
کل فایل‌های 
reply.md:1034:reply.md:861:reply.md:686:reply.md:509:reply.md:318:reply.md:43:`Report.financial_period_id` با 
`nullable=False` و FK 
reply.md:1036:reply.md:862:reply.md:687:`financial_periods.period_id`.
reply.md:1037:reply.md:863:reply.md:688:reply.md:510:reply.md:319:reply.md:46:`Report.financial_period_id` استفاده 
نشده است.
reply.md:1038:reply.md:864:reply.md:689:reply.md:511:reply.md:320:reply.md:48:تست‌های Stage 5/6: نام 
`financial_period_id` در DTOها 
reply.md:1040:reply.md:867:`reports.financial_period_id` 
reply.md:1041:reply.md:868:reply.md:693:reply.md:513:reply.md:323:reply.md:51:Report و قرارداد قدیمی را با 
`financial_period_id` 
reply.md:1043:reply.md:870:reply.md:695:reply.md:515:reply.md:325:reply.md:54:تابع عمومی `ingest_codal_report` یک 
facade سازگار با 
reply.md:1045:reply.md:871:reply.md:696:reply.md:516:reply.md:326:`src.ingestion.service.ingest_codal_report` 
reply.md:1046:reply.md:872:reply.md:697:reply.md:517:reply.md:327:reply.md:55:delegate می‌کند. تابع `ingest_codal_pdf` 
پس از 
reply.md:1048:reply.md:874:reply.md:699:reply.md:518:reply.md:328:reply.md:57:توابع `load_codal_pdf` و 
`load_codal_pdf_from_url` پس 
reply.md:1050:reply.md:875:reply.md:701:reply.md:520:reply.md:329:reply.md:58:`src.ingestion.service.ingest_codal_repor
t` را 
reply.md:1052:reply.md:876:reply.md:702:reply.md:521:reply.md:330:reply.md:61:`financial_period_id` ندارند؛ این با 
یافتهٔ قبلی 
reply.md:1054:reply.md:878:reply.md:704:reply.md:523:reply.md:333:`Report.financial_period_id` در 
reply.md:1055:reply.md:879:reply.md:705:reply.md:524:reply.md:334:reply.md:68:`Report.financial_period_id` تا زمان 
تعیین تکلیف و 
reply.md:1057:reply.md:881:reply.md:707:reply.md:526:reply.md:336:reply.md:71:Report.financial_period_id و مرز writer 
قدیمی — 
reply.md:1060:`src/ingestion/service.py::ingest_codal_report` است؛ 
reply.md:1061:reply.md:884:reply.md:709:reply.md:529:reply.md:339:reply.md:76:`Report.financial_period_id` با ورودی 
مقایسه می‌شوند؛ 
reply.md:1063:reply.md:886:reply.md:711:reply.md:530:reply.md:340:reply.md:78:`financial_period_id=period_id` ثبت 
می‌شود.
reply.md:1064:reply.md:887:reply.md:712:reply.md:531:reply.md:341:reply.md:80:Report.financial_period_id (حذف تدریجی، 
nullable و 
reply.md:1066:reply.md:889:reply.md:714:reply.md:533:reply.md:343:reply.md:83:src/ingestion/service.py::ingest_codal_re
port.
reply.md:1067:reply.md:890:reply.md:715:reply.md:534:reply.md:344:reply.md:85:src/ingestion/codal/ingestion.py::ingest_
codal_report 
reply.md:1069:reply.md:892:reply.md:717:reply.md:535:ingest_codal_pdf 
reply.md:1070:reply.md:893:reply.md:718:reply.md:536:reply.md:346:reply.md:88:تابع‌های load_codal_pdf و 
load_codal_pdf_from_url را 
reply.md:1072:reply.md:895:reply.md:720:reply.md:538:reply.md:349:financial_period_id 
reply.md:1073:reply.md:896:reply.md:721:reply.md:539:reply.md:350:reply.md:92:Report.financial_period_id تلقی کرد.
reply.md:1074:reply.md:897:reply.md:722:reply.md:541:Report.financial_period_id در 
reply.md:1076:`financial_period_id` | 
reply.md:1077:reply.md:900:reply.md:725:reply.md:544:reply.md:356:`financial_periods` 
reply.md:1078:reply.md:901:reply.md:726:reply.md:546:`ingest_codal_report(...)` 
reply.md:1079:reply.md:904:reply.md:729:reply.md:548:reply.md:360:load_codal_pdf_from_url  
reply.md:1080:reply.md:905:reply.md:731:ingest_codal_report  
reply.md:1081:reply.md:906:reply.md:732:reply.md:550:reply.md:362:reply.md:109:ingest_codal_pdf و facade سازگاری 
ingest_codal_report 
reply.md:1083:reply.md:908:reply.md:734:reply.md:551:reply.md:364:src/ingestion/service.py::ingest_codal_report | 
reply.md:1084:reply.md:909:reply.md:735:reply.md:553:`service.py::ingest_codal_report`: 
reply.md:1085:reply.md:910:reply.md:736:reply.md:555:financial_period_id به‌عنوان 
reply.md:1086:reply.md:911:reply.md:737:reply.md:557:financial_period_id در مدل فعلی 
reply.md:1087:reply.md:912:reply.md:738:reply.md:558:reply.md:371:reply.md:121:`src/ingestion/service.py::ingest_codal_
report`:
reply.md:1088:reply.md:913:reply.md:739:reply.md:560:ingest_codal_report
reply.md:1089:reply.md:914:reply.md:740:reply.md:562:`financial_periods` — 
reply.md:1090:reply.md:916:`reports.financial_period_id` must not be 
reply.md:1091:reply.md:917:reply.md:743:reply.md:565:reply.md:378:`financial_periods` model 
reply.md:1093:`reports.financial_period_id` 
reply.md:1094:reply.md:920:reply.md:746:reply.md:567:reply.md:380:reply.md:134:`financial_period_id` را جداگانه نگه 
می‌دارد؛ FKها 
reply.md:1097:`financial_periods.company_id` تا 
reply.md:1098:reply.md:924:reply.md:750:reply.md:571:reply.md:385:`Report.financial_period_id` در مدل 
reply.md:1099:reply.md:925:reply.md:751:reply.md:572:reply.md:386:reply.md:143:pipelineهای load_codal_pdf و 
load_codal_pdf_from_url |
reply.md:1100:reply.md:926:reply.md:752:reply.md:573:reply.md:388:\`src/ingestion/service.py::ingest_codal_report\` | 
reply.md:1101:reply.md:928:ingest_codal_report 
reply.md:1102:reply.md:929:reply.md:755:reply.md:576:reply.md:390:reply.md:150:RawLineInput و ingest_codal_report 
فعلاً حفظ؛ بعداً 
reply.md:1104:reply.md:931:reply.md:757:reply.md:579:\`ingest_codal_report\` را 
reply.md:1105:reply.md:932:reply.md:758:reply.md:580:reply.md:394:`service.py::ingest_codal_report` | 
reply.md:1106:reply.md:933:reply.md:759:reply.md:581:reply.md:396:`codal/ingestion.py::ingest_codal_pdf` و 
reply.md:1107:reply.md:934:reply.md:760:reply.md:582:reply.md:397:reply.md:162:`ingestion/service.py::ingest_codal_repo
rt` (تابع 
reply.md:1109:reply.md:936:reply.md:761:reply.md:584:reply.md:399:reply.md:166:`ingest_codal_report` و Stage 5 query | 
Stage 5 
reply.md:1111:reply.md:938:reply.md:763:reply.md:586:reply.md:402:`ingest_codal_report` 
reply.md:1112:reply.md:939:reply.md:764:reply.md:587:reply.md:404:`financial_period_id` 
reply.md:1113:reply.md:940:reply.md:765:reply.md:588:reply.md:406:`financial_periods` |
reply.md:1114:reply.md:941:reply.md:767:`Report.financial_period_id` 
reply.md:1115:reply.md:942:reply.md:768:reply.md:591:reply.md:408:reply.md:177:`ingest_codal_report` یک period_id واحد 
را به تمام 
reply.md:1116:reply.md:944:reply.md:770:reply.md:593:reply.md:409:reply.md:179:`src/ingestion/service.py::ingest_codal_
report`؛ 
reply.md:1118:reply.md:945:reply.md:772:`financial_periods` | در مسیر 
reply.md:1119:reply.md:946:reply.md:773:reply.md:598:`Report.financial_period_id` 
reply.md:1120:reply.md:947:reply.md:774:reply.md:599:reply.md:415:reply.md:191:محدودیت را دارد. متد 
`ingest_codal_report` یک 
reply.md:1122:reply.md:949:reply.md:777:`Report.financial_period_id` 
reply.md:1124:`Report.financial_period_id` 
reply.md:1125:reply.md:952:reply.md:780:reply.md:604:reply.md:421:reply.md:201:`src/ingestion/service.py::ingest_codal_
report` 
reply.md:1127:reply.md:954:reply.md:782:reply.md:606:reply.md:423:reply.md:207:`src/ingestion/service.py::ingest_codal_
report` 
reply.md:1129:reply.md:956:reply.md:784:reply.md:607:reply.md:425:reply.md:212:`service.py::ingest_codal_report` → 
RawFinancialFact.
reply.md:1130:reply.md:957:reply.md:785:reply.md:609:`codal/ingestion.py::ingest_codal_report` 
reply.md:1132:`service.py::ingest_codal_report` می‌رسد.
reply.md:1133:reply.md:959:reply.md:787:reply.md:612:`codal/ingestion.py::ingest_codal_pdf` 
reply.md:1134:reply.md:960:reply.md:788:reply.md:614:`codal/pipeline.py::load_codal_pdf` و 
reply.md:1135:reply.md:961:reply.md:789:reply.md:615:reply.md:432:reply.md:219:`load_codal_pdf_from_url` 
reply.md:1137:reply.md:963:reply.md:791:reply.md:618:`reports.financial_period_id`، چون پیش 
reply.md:1138:reply.md:964:reply.md:792:reply.md:619:reply.md:436:reply.md:226:`reports.financial_period_id` و تفکیک 
قرارداد legacy 
reply.md:1140:reply.md:966:reply.md:793:reply.md:621:`Report.financial_period_id` در ORM 
reply.md:1141:reply.md:967:reply.md:794:reply.md:622:reply.md:439:reply.md:230:`service.py::ingest_codal_report` 
delegate می‌کند؛ 
reply.md:1143:reply.md:969:reply.md:797:`financial_period_id` در 
reply.md:1144:reply.md:970:reply.md:799:`reports.financial_period_id` اشاره 
reply.md:1145:reply.md:971:reply.md:800:reply.md:627:reply.md:445:reply.md:237:`Report.financial_period_id` مجاز نیست. 
مسیر جدید 
reply.md:1148:`financial_periods.company_id` تا 
reply.md:1149:reply.md:975:reply.md:804:reply.md:631:reply.md:449:reply.md:244:`Report.financial_period_id` به‌صورت 
optional 
reply.md:1151:reply.md:977:reply.md:806:reply.md:633:reply.md:451:reply.md:246:writer قدیمی به 
Report.financial_period_id — 
reply.md:1153:reply.md:978:reply.md:807:reply.md:635:`service.py::ingest_codal_report` writer 
reply.md:1154:reply.md:979:reply.md:808:reply.md:636:reply.md:454:reply.md:250:`Report.financial_period_id` باید با 
ورودی یکسان 
reply.md:1156:reply.md:981:reply.md:810:reply.md:637:reply.md:455:reply.md:253:src/ingestion/service.py::ingest_codal_r
eport است؛ 
reply.md:1158:reply.md:982:reply.md:812:financial_period_id 
reply.md:1159:reply.md:983:reply.md:813:reply.md:642:Report.financial_period_id شمرده 
reply.md:1160:reply.md:984:reply.md:814:reply.md:644:Report.financial_period_id 
reply.md:1161:reply.md:985:reply.md:815:reply.md:645:reply.md:463:reply.md:265:`ingest_codal_report` take DTOs |
reply.md:1162:reply.md:986:reply.md:816:reply.md:646:reply.md:465:`ingest_codal_report` accepts 
reply.md:1166:ingest_codal_report()
reply.md:1169:reply.md:990:reply.md:820:reply.md:650:reply.md:470:ingest_codal_report()
reply.md:1170:reply.md:991:reply.md:821:reply.md:651:reply.md:471:reply.md:272:01_Stage1_Data_Foundation.md:278:financi
al_period_id
reply.md:1172:financial_periods, 
reply.md:1173:reply.md:996:reply.md:825:reply.md:654:reply.md:475:ingest_codal_report()`
reply.md:1175:`financial_periods`
reply.md:1178:reply.md:1002:reply.md:830:reply.md:658:reply.md:479:reply.md:288:consumed by `ingest_codal_report`; the 
existing 
reply.md:1181:ingest_codal_report / 
reply.md:1183:`ingest_codal_report` 
reply.md:1185:ingest_codal_report()
reply.md:1186:reply.md:1009:reply.md:838:`ingest_codal_report()` 
reply.md:1187:reply.md:1011:`ingest_codal_report`، 
reply.md:1188:reply.md:1012:reply.md:841:reply.md:667:reply.md:488:reply.md:298:reply.md:10:از `load_codal_pdf` و 
PDFهای fixture 
reply.md:1190:reply.md:1013:reply.md:842:reply.md:668:reply.md:490:`ingest_codal_report()`:
reply.md:1191:reply.md:1014:reply.md:843:reply.md:669:reply.md:491:reply.md:300:reply.md:13:`financial_period_id` است، 
درحالی‌که 
reply.md:1193:reply.md:1016:reply.md:845:reply.md:671:reply.md:494:`ingest_codal_report()` 
reply.md:1194:reply.md:1017:reply.md:846:reply.md:672:reply.md:495:reply.md:305:`ingest_codal_report`
reply.md:1203:reply.md:1025:reply.md:854:`load_codal_pdf_from_url` 
reply.md:1206:reply.md:1028:reply.md:856:reply.md:682:reply.md:504:reply.md:314:reply.md:36:`reports.financial_period_i
d` پیش از 
reply.md:1208:reply.md:1030:reply.md:858:reply.md:683:reply.md:506:reply.md:315:reply.md:39:`reports.financial_period_i
d` و مسیرهای 
reply.md:1210:reply.md:1032:reply.md:859:reply.md:684:reply.md:507:reply.md:316:reply.md:41:`financial_period_id|Financ
ialPeriod` در 
reply.md:1212:reply.md:1034:reply.md:861:reply.md:686:reply.md:509:reply.md:318:reply.md:43:`Report.financial_period_id
` با 
reply.md:1214:reply.md:1036:reply.md:862:reply.md:687:`financial_periods.period_id`.
reply.md:1215:reply.md:1037:reply.md:863:reply.md:688:reply.md:510:reply.md:319:reply.md:46:`Report.financial_period_id
` استفاده 
reply.md:1218:`financial_period_id` در DTOها 
reply.md:1219:reply.md:1040:reply.md:867:`reports.financial_period_id` 
reply.md:1221:`financial_period_id` 
reply.md:1222:reply.md:1043:reply.md:870:reply.md:695:reply.md:515:reply.md:325:reply.md:54:تابع عمومی 
`ingest_codal_report` یک 
reply.md:1224:reply.md:1045:reply.md:871:reply.md:696:reply.md:516:reply.md:326:`src.ingestion.service.ingest_codal_rep
ort` 
reply.md:1225:reply.md:1046:reply.md:872:reply.md:697:reply.md:517:reply.md:327:reply.md:55:delegate می‌کند. تابع 
`ingest_codal_pdf` 
reply.md:1227:reply.md:1048:reply.md:874:reply.md:699:reply.md:518:reply.md:328:reply.md:57:توابع `load_codal_pdf` و 
reply.md:1228:`load_codal_pdf_from_url` پس 
reply.md:1231:reply.md:1052:reply.md:876:reply.md:702:reply.md:521:reply.md:330:reply.md:61:`financial_period_id` 
ندارند؛ این با 
reply.md:1233:reply.md:1054:reply.md:878:reply.md:704:reply.md:523:reply.md:333:`Report.financial_period_id` در 
reply.md:1234:reply.md:1055:reply.md:879:reply.md:705:reply.md:524:reply.md:334:reply.md:68:`Report.financial_period_id
` تا زمان 
reply.md:1236:reply.md:1057:reply.md:881:reply.md:707:reply.md:526:reply.md:336:reply.md:71:Report.financial_period_id 
و مرز writer 
reply.md:1238:reply.md:1060:`src/ingestion/service.py::ingest_codal_report` است؛ 
reply.md:1239:reply.md:1061:reply.md:884:reply.md:709:reply.md:529:reply.md:339:reply.md:76:`Report.financial_period_id
` با ورودی 
reply.md:1241:reply.md:1063:reply.md:886:reply.md:711:reply.md:530:reply.md:340:reply.md:78:`financial_period_id=period
_id` ثبت 
reply.md:1243:reply.md:1064:reply.md:887:reply.md:712:reply.md:531:reply.md:341:reply.md:80:Report.financial_period_id 
(حذف تدریجی، 
reply.md:1249:reply.md:1069:reply.md:892:reply.md:717:reply.md:535:ingest_codal_pdf 
reply.md:1250:reply.md:1070:reply.md:893:reply.md:718:reply.md:536:reply.md:346:reply.md:88:تابع‌های load_codal_pdf و 
reply.md:1251:load_codal_pdf_from_url را 
reply.md:1252:reply.md:1072:reply.md:895:reply.md:720:reply.md:538:reply.md:349:financial_period_id 
reply.md:1253:reply.md:1073:reply.md:896:reply.md:721:reply.md:539:reply.md:350:reply.md:92:Report.financial_period_id 
تلقی کرد.
reply.md:1254:reply.md:1074:reply.md:897:reply.md:722:reply.md:541:Report.financial_period_id در 
reply.md:1255:reply.md:1076:`financial_period_id` | 
reply.md:1256:reply.md:1077:reply.md:900:reply.md:725:reply.md:544:reply.md:356:`financial_periods` 
reply.md:1257:reply.md:1078:reply.md:901:reply.md:726:reply.md:546:`ingest_codal_report(...)` 
reply.md:1258:reply.md:1079:reply.md:904:reply.md:729:reply.md:548:reply.md:360:load_codal_pdf_from_url  
reply.md:1259:reply.md:1080:reply.md:905:reply.md:731:ingest_codal_report  
reply.md:1260:reply.md:1081:reply.md:906:reply.md:732:reply.md:550:reply.md:362:reply.md:109:ingest_codal_pdf و facade 
سازگاری 
reply.md:1261:ingest_codal_report 
reply.md:1262:reply.md:1083:reply.md:908:reply.md:734:reply.md:551:reply.md:364:src/ingestion/service.py::ingest_codal_
report | 
reply.md:1263:reply.md:1084:reply.md:909:reply.md:735:reply.md:553:`service.py::ingest_codal_report`: 
reply.md:1264:reply.md:1085:reply.md:910:reply.md:736:reply.md:555:financial_period_id به‌عنوان 
reply.md:1265:reply.md:1086:reply.md:911:reply.md:737:reply.md:557:financial_period_id در مدل فعلی 
reply.md:1268:reply.md:1088:reply.md:913:reply.md:739:reply.md:560:ingest_codal_report
reply.md:1269:reply.md:1089:reply.md:914:reply.md:740:reply.md:562:`financial_periods` — 
reply.md:1270:reply.md:1090:reply.md:916:`reports.financial_period_id` must not be 
reply.md:1271:reply.md:1091:reply.md:917:reply.md:743:reply.md:565:reply.md:378:`financial_periods` model 
reply.md:1272:reply.md:1093:`reports.financial_period_id` 
reply.md:1273:reply.md:1094:reply.md:920:reply.md:746:reply.md:567:reply.md:380:reply.md:134:`financial_period_id` را 
جداگانه نگه 
reply.md:1275:reply.md:1097:`financial_periods.company_id` تا 
reply.md:1276:reply.md:1098:reply.md:924:reply.md:750:reply.md:571:reply.md:385:`Report.financial_period_id` در مدل 
reply.md:1277:reply.md:1099:reply.md:925:reply.md:751:reply.md:572:reply.md:386:reply.md:143:pipelineهای 
load_codal_pdf و 
reply.md:1278:load_codal_pdf_from_url |
reply.md:1279:reply.md:1100:reply.md:926:reply.md:752:reply.md:573:reply.md:388:\`src/ingestion/service.py::ingest_coda
l_report\` | 
reply.md:1280:reply.md:1101:reply.md:928:ingest_codal_report 
reply.md:1281:reply.md:1102:reply.md:929:reply.md:755:reply.md:576:reply.md:390:reply.md:150:RawLineInput و 
ingest_codal_report 
reply.md:1283:reply.md:1104:reply.md:931:reply.md:757:reply.md:579:\`ingest_codal_report\` را 
reply.md:1284:reply.md:1105:reply.md:932:reply.md:758:reply.md:580:reply.md:394:`service.py::ingest_codal_report` | 
reply.md:1285:reply.md:1106:reply.md:933:reply.md:759:reply.md:581:reply.md:396:`codal/ingestion.py::ingest_codal_pdf` 
و 
reply.md:1288:reply.md:1109:reply.md:936:reply.md:761:reply.md:584:reply.md:399:reply.md:166:`ingest_codal_report` و 
Stage 5 query | 
reply.md:1290:reply.md:1111:reply.md:938:reply.md:763:reply.md:586:reply.md:402:`ingest_codal_report` 
reply.md:1291:reply.md:1112:reply.md:939:reply.md:764:reply.md:587:reply.md:404:`financial_period_id` 
reply.md:1292:reply.md:1113:reply.md:940:reply.md:765:reply.md:588:reply.md:406:`financial_periods` |
reply.md:1293:reply.md:1114:reply.md:941:reply.md:767:`Report.financial_period_id` 
reply.md:1294:reply.md:1115:reply.md:942:reply.md:768:reply.md:591:reply.md:408:reply.md:177:`ingest_codal_report` یک 
period_id واحد 
reply.md:1298:reply.md:1118:reply.md:945:reply.md:772:`financial_periods` | در مسیر 
reply.md:1299:reply.md:1119:reply.md:946:reply.md:773:reply.md:598:`Report.financial_period_id` 
reply.md:1301:`ingest_codal_report` یک 
reply.md:1302:reply.md:1122:reply.md:949:reply.md:777:`Report.financial_period_id` 
reply.md:1303:reply.md:1124:`Report.financial_period_id` 
reply.md:1308:reply.md:1129:reply.md:956:reply.md:784:reply.md:607:reply.md:425:reply.md:212:`service.py::ingest_codal_
report` → 
reply.md:1310:reply.md:1130:reply.md:957:reply.md:785:reply.md:609:`codal/ingestion.py::ingest_codal_report` 
reply.md:1311:reply.md:1132:`service.py::ingest_codal_report` می‌رسد.
reply.md:1312:reply.md:1133:reply.md:959:reply.md:787:reply.md:612:`codal/ingestion.py::ingest_codal_pdf` 
reply.md:1313:reply.md:1134:reply.md:960:reply.md:788:reply.md:614:`codal/pipeline.py::load_codal_pdf` و 
reply.md:1314:reply.md:1135:reply.md:961:reply.md:789:reply.md:615:reply.md:432:reply.md:219:`load_codal_pdf_from_url` 
reply.md:1315:reply.md:1137:reply.md:963:reply.md:791:reply.md:618:`reports.financial_period_id`، چون پیش 
reply.md:1316:reply.md:1138:reply.md:964:reply.md:792:reply.md:619:reply.md:436:reply.md:226:`reports.financial_period_
id` و تفکیک 
reply.md:1318:reply.md:1140:reply.md:966:reply.md:793:reply.md:621:`Report.financial_period_id` در ORM 
reply.md:1319:reply.md:1141:reply.md:967:reply.md:794:reply.md:622:reply.md:439:reply.md:230:`service.py::ingest_codal_
report` 
reply.md:1321:reply.md:1143:reply.md:969:reply.md:797:`financial_period_id` در 
reply.md:1322:reply.md:1144:reply.md:970:reply.md:799:`reports.financial_period_id` اشاره 
reply.md:1323:reply.md:1145:reply.md:971:reply.md:800:reply.md:627:reply.md:445:reply.md:237:`Report.financial_period_i
d` مجاز نیست. 
reply.md:1325:reply.md:1148:`financial_periods.company_id` تا 
reply.md:1326:reply.md:1149:reply.md:975:reply.md:804:reply.md:631:reply.md:449:reply.md:244:`Report.financial_period_i
d` به‌صورت 
reply.md:1329:Report.financial_period_id — 
reply.md:1330:reply.md:1153:reply.md:978:reply.md:807:reply.md:635:`service.py::ingest_codal_report` writer 
reply.md:1331:reply.md:1154:reply.md:979:reply.md:808:reply.md:636:reply.md:454:reply.md:250:`Report.financial_period_i
d` باید با 
reply.md:1335:reply.md:1158:reply.md:982:reply.md:812:financial_period_id 
reply.md:1336:reply.md:1159:reply.md:983:reply.md:813:reply.md:642:Report.financial_period_id شمرده 
reply.md:1337:reply.md:1160:reply.md:984:reply.md:814:reply.md:644:Report.financial_period_id 
reply.md:1338:reply.md:1161:reply.md:985:reply.md:815:reply.md:645:reply.md:463:reply.md:265:`ingest_codal_report` 
take DTOs |
reply.md:1339:reply.md:1162:reply.md:986:reply.md:816:reply.md:646:reply.md:465:`ingest_codal_report` accepts 
reply.md:1340:reply.md:1166:ingest_codal_report()
reply.md:1341:reply.md:1169:reply.md:990:reply.md:820:reply.md:650:reply.md:470:ingest_codal_report()
reply.md:1344:reply.md:1172:financial_periods, 
reply.md:1345:reply.md:1173:reply.md:996:reply.md:825:reply.md:654:reply.md:475:ingest_codal_report()`
reply.md:1346:reply.md:1175:`financial_periods`
reply.md:1347:reply.md:1178:reply.md:1002:reply.md:830:reply.md:658:reply.md:479:reply.md:288:consumed by 
`ingest_codal_report`; the 
reply.md:1349:reply.md:1181:ingest_codal_report / 
reply.md:1350:reply.md:1183:`ingest_codal_report` 
reply.md:1351:reply.md:1185:ingest_codal_report()
reply.md:1352:reply.md:1186:reply.md:1009:reply.md:838:`ingest_codal_report()` 
reply.md:1353:reply.md:1187:reply.md:1011:`ingest_codal_report`، 
reply.md:1354:reply.md:1188:reply.md:1012:reply.md:841:reply.md:667:reply.md:488:reply.md:298:reply.md:10:از 
`load_codal_pdf` و 
reply.md:1356:reply.md:1190:reply.md:1013:reply.md:842:reply.md:668:reply.md:490:`ingest_codal_report()`:
reply.md:1357:reply.md:1191:reply.md:1014:reply.md:843:reply.md:669:reply.md:491:reply.md:300:reply.md:13:`financial_pe
riod_id` است، 
reply.md:1359:reply.md:1193:reply.md:1016:reply.md:845:reply.md:671:reply.md:494:`ingest_codal_report()` 
reply.md:1360:reply.md:1194:reply.md:1017:reply.md:846:reply.md:672:reply.md:495:reply.md:305:`ingest_codal_report`
reply.md:1361:reply.md:1203:reply.md:1025:reply.md:854:`load_codal_pdf_from_url` 
reply.md:1366:reply.md:1210:reply.md:1032:reply.md:859:reply.md:684:reply.md:507:reply.md:316:reply.md:41:`financial_pe
riod_id|Financ
reply.md:1368:reply.md:1212:reply.md:1034:reply.md:861:reply.md:686:reply.md:509:reply.md:318:reply.md:43:`Report.finan
cial_period_id
reply.md:1370:reply.md:1214:reply.md:1036:reply.md:862:reply.md:687:`financial_periods.period_id`.
reply.md:1371:reply.md:1215:reply.md:1037:reply.md:863:reply.md:688:reply.md:510:reply.md:319:reply.md:46:`Report.finan
cial_period_id
reply.md:1373:reply.md:1218:`financial_period_id` در DTOها 
reply.md:1374:reply.md:1219:reply.md:1040:reply.md:867:`reports.financial_period_id` 
reply.md:1375:reply.md:1221:`financial_period_id` 
reply.md:1377:`ingest_codal_report` یک 
reply.md:1381:`ingest_codal_pdf` 
reply.md:1382:reply.md:1227:reply.md:1048:reply.md:874:reply.md:699:reply.md:518:reply.md:328:reply.md:57:توابع 
`load_codal_pdf` و 
reply.md:1383:reply.md:1228:`load_codal_pdf_from_url` پس 
reply.md:1384:reply.md:1231:reply.md:1052:reply.md:876:reply.md:702:reply.md:521:reply.md:330:reply.md:61:`financial_pe
riod_id` 
reply.md:1386:reply.md:1233:reply.md:1054:reply.md:878:reply.md:704:reply.md:523:reply.md:333:`Report.financial_period_
id` در 
reply.md:1387:reply.md:1234:reply.md:1055:reply.md:879:reply.md:705:reply.md:524:reply.md:334:reply.md:68:`Report.finan
cial_period_id
reply.md:1389:reply.md:1236:reply.md:1057:reply.md:881:reply.md:707:reply.md:526:reply.md:336:reply.md:71:Report.financ
ial_period_id 
reply.md:1391:reply.md:1238:reply.md:1060:`src/ingestion/service.py::ingest_codal_report` است؛ 
reply.md:1392:reply.md:1239:reply.md:1061:reply.md:884:reply.md:709:reply.md:529:reply.md:339:reply.md:76:`Report.finan
cial_period_id
reply.md:1394:reply.md:1241:reply.md:1063:reply.md:886:reply.md:711:reply.md:530:reply.md:340:reply.md:78:`financial_pe
riod_id=period
reply.md:1396:reply.md:1243:reply.md:1064:reply.md:887:reply.md:712:reply.md:531:reply.md:341:reply.md:80:Report.financ
ial_period_id 
reply.md:1398:reply.md:1249:reply.md:1069:reply.md:892:reply.md:717:reply.md:535:ingest_codal_pdf 
reply.md:1399:reply.md:1250:reply.md:1070:reply.md:893:reply.md:718:reply.md:536:reply.md:346:reply.md:88:تابع‌های 
load_codal_pdf و 
reply.md:1400:reply.md:1251:load_codal_pdf_from_url را 
reply.md:1401:reply.md:1252:reply.md:1072:reply.md:895:reply.md:720:reply.md:538:reply.md:349:financial_period_id 
reply.md:1402:reply.md:1253:reply.md:1073:reply.md:896:reply.md:721:reply.md:539:reply.md:350:reply.md:92:Report.financ
ial_period_id 
reply.md:1404:reply.md:1254:reply.md:1074:reply.md:897:reply.md:722:reply.md:541:Report.financial_period_id در 
reply.md:1405:reply.md:1255:reply.md:1076:`financial_period_id` | 
reply.md:1406:reply.md:1256:reply.md:1077:reply.md:900:reply.md:725:reply.md:544:reply.md:356:`financial_periods` 
reply.md:1407:reply.md:1257:reply.md:1078:reply.md:901:reply.md:726:reply.md:546:`ingest_codal_report(...)` 
reply.md:1408:reply.md:1258:reply.md:1079:reply.md:904:reply.md:729:reply.md:548:reply.md:360:load_codal_pdf_from_url  
reply.md:1409:reply.md:1259:reply.md:1080:reply.md:905:reply.md:731:ingest_codal_report  
reply.md:1410:reply.md:1260:reply.md:1081:reply.md:906:reply.md:732:reply.md:550:reply.md:362:reply.md:109:ingest_codal
_pdf و facade 
reply.md:1412:reply.md:1261:ingest_codal_report 
reply.md:1415:reply.md:1263:reply.md:1084:reply.md:909:reply.md:735:reply.md:553:`service.py::ingest_codal_report`: 
reply.md:1416:reply.md:1264:reply.md:1085:reply.md:910:reply.md:736:reply.md:555:financial_period_id به‌عنوان 
reply.md:1417:reply.md:1265:reply.md:1086:reply.md:911:reply.md:737:reply.md:557:financial_period_id در مدل فعلی 
reply.md:1418:reply.md:1268:reply.md:1088:reply.md:913:reply.md:739:reply.md:560:ingest_codal_report
reply.md:1419:reply.md:1269:reply.md:1089:reply.md:914:reply.md:740:reply.md:562:`financial_periods` — 
reply.md:1420:reply.md:1270:reply.md:1090:reply.md:916:`reports.financial_period_id` must not be 
reply.md:1421:reply.md:1271:reply.md:1091:reply.md:917:reply.md:743:reply.md:565:reply.md:378:`financial_periods` 
model 
reply.md:1422:reply.md:1272:reply.md:1093:`reports.financial_period_id` 
reply.md:1423:reply.md:1273:reply.md:1094:reply.md:920:reply.md:746:reply.md:567:reply.md:380:reply.md:134:`financial_p
eriod_id` را 
reply.md:1425:reply.md:1275:reply.md:1097:`financial_periods.company_id` تا 
reply.md:1426:reply.md:1276:reply.md:1098:reply.md:924:reply.md:750:reply.md:571:reply.md:385:`Report.financial_period_
id` در مدل 
reply.md:1428:load_codal_pdf و 
reply.md:1429:reply.md:1278:load_codal_pdf_from_url |
reply.md:1432:reply.md:1280:reply.md:1101:reply.md:928:ingest_codal_report 
reply.md:1434:ingest_codal_report 
reply.md:1435:reply.md:1283:reply.md:1104:reply.md:931:reply.md:757:reply.md:579:\`ingest_codal_report\` را 
reply.md:1436:reply.md:1284:reply.md:1105:reply.md:932:reply.md:758:reply.md:580:reply.md:394:`service.py::ingest_codal
_report` | 
reply.md:1437:reply.md:1285:reply.md:1106:reply.md:933:reply.md:759:reply.md:581:reply.md:396:`codal/ingestion.py::inge
st_codal_pdf` 
reply.md:1439:reply.md:1288:reply.md:1109:reply.md:936:reply.md:761:reply.md:584:reply.md:399:reply.md:166:`ingest_coda
l_report` و 
reply.md:1441:reply.md:1290:reply.md:1111:reply.md:938:reply.md:763:reply.md:586:reply.md:402:`ingest_codal_report` 
reply.md:1442:reply.md:1291:reply.md:1112:reply.md:939:reply.md:764:reply.md:587:reply.md:404:`financial_period_id` 
reply.md:1443:reply.md:1292:reply.md:1113:reply.md:940:reply.md:765:reply.md:588:reply.md:406:`financial_periods` |
reply.md:1444:reply.md:1293:reply.md:1114:reply.md:941:reply.md:767:`Report.financial_period_id` 
reply.md:1445:reply.md:1294:reply.md:1115:reply.md:942:reply.md:768:reply.md:591:reply.md:408:reply.md:177:`ingest_coda
l_report` یک 
reply.md:1447:reply.md:1298:reply.md:1118:reply.md:945:reply.md:772:`financial_periods` | در مسیر 
reply.md:1448:reply.md:1299:reply.md:1119:reply.md:946:reply.md:773:reply.md:598:`Report.financial_period_id` 
reply.md:1449:reply.md:1301:`ingest_codal_report` یک 
reply.md:1450:reply.md:1302:reply.md:1122:reply.md:949:reply.md:777:`Report.financial_period_id` 
reply.md:1451:reply.md:1303:reply.md:1124:`Report.financial_period_id` 
reply.md:1454:reply.md:1310:reply.md:1130:reply.md:957:reply.md:785:reply.md:609:`codal/ingestion.py::ingest_codal_repo
rt` 
reply.md:1455:reply.md:1311:reply.md:1132:`service.py::ingest_codal_report` می‌رسد.
reply.md:1456:reply.md:1312:reply.md:1133:reply.md:959:reply.md:787:reply.md:612:`codal/ingestion.py::ingest_codal_pdf`
 
reply.md:1457:reply.md:1313:reply.md:1134:reply.md:960:reply.md:788:reply.md:614:`codal/pipeline.py::load_codal_pdf` و 
reply.md:1458:reply.md:1314:reply.md:1135:reply.md:961:reply.md:789:reply.md:615:reply.md:432:reply.md:219:`load_codal_
pdf_from_url` 
reply.md:1459:reply.md:1315:reply.md:1137:reply.md:963:reply.md:791:reply.md:618:`reports.financial_period_id`، چون 
پیش 
reply.md:1462:reply.md:1318:reply.md:1140:reply.md:966:reply.md:793:reply.md:621:`Report.financial_period_id` در ORM 
reply.md:1465:reply.md:1321:reply.md:1143:reply.md:969:reply.md:797:`financial_period_id` در 
reply.md:1466:reply.md:1322:reply.md:1144:reply.md:970:reply.md:799:`reports.financial_period_id` اشاره 
reply.md:1469:reply.md:1325:reply.md:1148:`financial_periods.company_id` تا 
reply.md:1472:reply.md:1329:Report.financial_period_id — 
reply.md:1473:reply.md:1330:reply.md:1153:reply.md:978:reply.md:807:reply.md:635:`service.py::ingest_codal_report` 
writer 
reply.md:1476:reply.md:1335:reply.md:1158:reply.md:982:reply.md:812:financial_period_id 
reply.md:1477:reply.md:1336:reply.md:1159:reply.md:983:reply.md:813:reply.md:642:Report.financial_period_id شمرده 
reply.md:1478:reply.md:1337:reply.md:1160:reply.md:984:reply.md:814:reply.md:644:Report.financial_period_id 
reply.md:1479:reply.md:1338:reply.md:1161:reply.md:985:reply.md:815:reply.md:645:reply.md:463:reply.md:265:`ingest_coda
l_report` 
reply.md:1481:reply.md:1339:reply.md:1162:reply.md:986:reply.md:816:reply.md:646:reply.md:465:`ingest_codal_report` 
accepts 
reply.md:1482:reply.md:1340:reply.md:1166:ingest_codal_report()
reply.md:1483:reply.md:1341:reply.md:1169:reply.md:990:reply.md:820:reply.md:650:reply.md:470:ingest_codal_report()
reply.md:1484:reply.md:1344:reply.md:1172:financial_periods, 
reply.md:1485:reply.md:1345:reply.md:1173:reply.md:996:reply.md:825:reply.md:654:reply.md:475:ingest_codal_report()`
reply.md:1486:reply.md:1346:reply.md:1175:`financial_periods`
reply.md:1488:`ingest_codal_report`; the 
reply.md:1489:reply.md:1349:reply.md:1181:ingest_codal_report / 
reply.md:1490:reply.md:1350:reply.md:1183:`ingest_codal_report` 
reply.md:1491:reply.md:1351:reply.md:1185:ingest_codal_report()
reply.md:1492:reply.md:1352:reply.md:1186:reply.md:1009:reply.md:838:`ingest_codal_report()` 
reply.md:1493:reply.md:1353:reply.md:1187:reply.md:1011:`ingest_codal_report`، 
reply.md:1495:`load_codal_pdf` و 
reply.md:1496:reply.md:1356:reply.md:1190:reply.md:1013:reply.md:842:reply.md:668:reply.md:490:`ingest_codal_report()`:
reply.md:1499:reply.md:1359:reply.md:1193:reply.md:1016:reply.md:845:reply.md:671:reply.md:494:`ingest_codal_report()` 
reply.md:1500:reply.md:1360:reply.md:1194:reply.md:1017:reply.md:846:reply.md:672:reply.md:495:reply.md:305:`ingest_cod
al_report`
reply.md:1501:reply.md:1361:reply.md:1203:reply.md:1025:reply.md:854:`load_codal_pdf_from_url` 
reply.md:1506:reply.md:1370:reply.md:1214:reply.md:1036:reply.md:862:reply.md:687:`financial_periods.period_id`.
reply.md:1509:reply.md:1373:reply.md:1218:`financial_period_id` در DTOها 
reply.md:1510:reply.md:1374:reply.md:1219:reply.md:1040:reply.md:867:`reports.financial_period_id` 
reply.md:1511:reply.md:1375:reply.md:1221:`financial_period_id` 
reply.md:1512:reply.md:1377:`ingest_codal_report` یک 
reply.md:1513:reply.md:1381:`ingest_codal_pdf` 
reply.md:1515:`load_codal_pdf` و 
reply.md:1516:reply.md:1383:reply.md:1228:`load_codal_pdf_from_url` پس 
reply.md:1525:reply.md:1391:reply.md:1238:reply.md:1060:`src/ingestion/service.py::ingest_codal_report` است؛ 
reply.md:1532:reply.md:1398:reply.md:1249:reply.md:1069:reply.md:892:reply.md:717:reply.md:535:ingest_codal_pdf 
reply.md:1534:load_codal_pdf و 
reply.md:1535:reply.md:1400:reply.md:1251:load_codal_pdf_from_url را 
reply.md:1536:reply.md:1401:reply.md:1252:reply.md:1072:reply.md:895:reply.md:720:reply.md:538:reply.md:349:financial_p
eriod_id 
reply.md:1539:reply.md:1404:reply.md:1254:reply.md:1074:reply.md:897:reply.md:722:reply.md:541:Report.financial_period_
id در 
reply.md:1540:reply.md:1405:reply.md:1255:reply.md:1076:`financial_period_id` | 
reply.md:1541:reply.md:1406:reply.md:1256:reply.md:1077:reply.md:900:reply.md:725:reply.md:544:reply.md:356:`financial_
periods` 
reply.md:1542:reply.md:1407:reply.md:1257:reply.md:1078:reply.md:901:reply.md:726:reply.md:546:`ingest_codal_report(...
)` 
reply.md:1543:reply.md:1408:reply.md:1258:reply.md:1079:reply.md:904:reply.md:729:reply.md:548:reply.md:360:load_codal_
pdf_from_url  
reply.md:1544:reply.md:1409:reply.md:1259:reply.md:1080:reply.md:905:reply.md:731:ingest_codal_report  
reply.md:1547:reply.md:1412:reply.md:1261:ingest_codal_report 
reply.md:1548:reply.md:1415:reply.md:1263:reply.md:1084:reply.md:909:reply.md:735:reply.md:553:`service.py::ingest_coda
l_report`: 
reply.md:1549:reply.md:1416:reply.md:1264:reply.md:1085:reply.md:910:reply.md:736:reply.md:555:financial_period_id 
به‌عنوان 
reply.md:1550:reply.md:1417:reply.md:1265:reply.md:1086:reply.md:911:reply.md:737:reply.md:557:financial_period_id در 
مدل فعلی 
reply.md:1551:reply.md:1418:reply.md:1268:reply.md:1088:reply.md:913:reply.md:739:reply.md:560:ingest_codal_report
reply.md:1552:reply.md:1419:reply.md:1269:reply.md:1089:reply.md:914:reply.md:740:reply.md:562:`financial_periods` — 
reply.md:1553:reply.md:1420:reply.md:1270:reply.md:1090:reply.md:916:`reports.financial_period_id` must not be 
reply.md:1554:reply.md:1421:reply.md:1271:reply.md:1091:reply.md:917:reply.md:743:reply.md:565:reply.md:378:`financial_
periods` 
reply.md:1556:reply.md:1422:reply.md:1272:reply.md:1093:`reports.financial_period_id` 
reply.md:1559:reply.md:1425:reply.md:1275:reply.md:1097:`financial_periods.company_id` تا 
reply.md:1562:reply.md:1428:load_codal_pdf و 
reply.md:1563:reply.md:1429:reply.md:1278:load_codal_pdf_from_url |
reply.md:1564:reply.md:1432:reply.md:1280:reply.md:1101:reply.md:928:ingest_codal_report 
reply.md:1565:reply.md:1434:ingest_codal_report 
reply.md:1566:reply.md:1435:reply.md:1283:reply.md:1104:reply.md:931:reply.md:757:reply.md:579:\`ingest_codal_report\` 
را 
reply.md:1573:reply.md:1441:reply.md:1290:reply.md:1111:reply.md:938:reply.md:763:reply.md:586:reply.md:402:`ingest_cod
al_report` 
reply.md:1574:reply.md:1442:reply.md:1291:reply.md:1112:reply.md:939:reply.md:764:reply.md:587:reply.md:404:`financial_
period_id` 
reply.md:1575:reply.md:1443:reply.md:1292:reply.md:1113:reply.md:940:reply.md:765:reply.md:588:reply.md:406:`financial_
periods` |
reply.md:1576:reply.md:1444:reply.md:1293:reply.md:1114:reply.md:941:reply.md:767:`Report.financial_period_id` 
reply.md:1579:reply.md:1447:reply.md:1298:reply.md:1118:reply.md:945:reply.md:772:`financial_periods` | در مسیر 
reply.md:1580:reply.md:1448:reply.md:1299:reply.md:1119:reply.md:946:reply.md:773:reply.md:598:`Report.financial_period
_id` 
reply.md:1581:reply.md:1449:reply.md:1301:`ingest_codal_report` یک 
reply.md:1582:reply.md:1450:reply.md:1302:reply.md:1122:reply.md:949:reply.md:777:`Report.financial_period_id` 
reply.md:1583:reply.md:1451:reply.md:1303:reply.md:1124:`Report.financial_period_id` 
reply.md:1586:reply.md:1455:reply.md:1311:reply.md:1132:`service.py::ingest_codal_report` می‌رسد.
reply.md:1587:reply.md:1456:reply.md:1312:reply.md:1133:reply.md:959:reply.md:787:reply.md:612:`codal/ingestion.py::ing
est_codal_pdf`
reply.md:1589:reply.md:1457:reply.md:1313:reply.md:1134:reply.md:960:reply.md:788:reply.md:614:`codal/pipeline.py::load
_codal_pdf` و 
reply.md:1592:reply.md:1459:reply.md:1315:reply.md:1137:reply.md:963:reply.md:791:reply.md:618:`reports.financial_perio
d_id`، چون 
reply.md:1594:reply.md:1462:reply.md:1318:reply.md:1140:reply.md:966:reply.md:793:reply.md:621:`Report.financial_period
_id` در ORM 
reply.md:1595:reply.md:1465:reply.md:1321:reply.md:1143:reply.md:969:reply.md:797:`financial_period_id` در 
reply.md:1596:reply.md:1466:reply.md:1322:reply.md:1144:reply.md:970:reply.md:799:`reports.financial_period_id` اشاره 
reply.md:1597:reply.md:1469:reply.md:1325:reply.md:1148:`financial_periods.company_id` تا 
reply.md:1598:reply.md:1472:reply.md:1329:Report.financial_period_id — 
reply.md:1599:reply.md:1473:reply.md:1330:reply.md:1153:reply.md:978:reply.md:807:reply.md:635:`service.py::ingest_coda
l_report` 
reply.md:1601:reply.md:1476:reply.md:1335:reply.md:1158:reply.md:982:reply.md:812:financial_period_id 
reply.md:1602:reply.md:1477:reply.md:1336:reply.md:1159:reply.md:983:reply.md:813:reply.md:642:Report.financial_period_
id شمرده 
reply.md:1603:reply.md:1478:reply.md:1337:reply.md:1160:reply.md:984:reply.md:814:reply.md:644:Report.financial_period_
id 
reply.md:1606:reply.md:1481:reply.md:1339:reply.md:1162:reply.md:986:reply.md:816:reply.md:646:reply.md:465:`ingest_cod
al_report` 
reply.md:1608:reply.md:1482:reply.md:1340:reply.md:1166:ingest_codal_report()
reply.md:1609:reply.md:1483:reply.md:1341:reply.md:1169:reply.md:990:reply.md:820:reply.md:650:reply.md:470:ingest_coda
l_report()
reply.md:1610:reply.md:1484:reply.md:1344:reply.md:1172:financial_periods, 
reply.md:1611:reply.md:1485:reply.md:1345:reply.md:1173:reply.md:996:reply.md:825:reply.md:654:reply.md:475:ingest_coda
l_report()`
reply.md:1612:reply.md:1486:reply.md:1346:reply.md:1175:`financial_periods`
reply.md:1613:reply.md:1488:`ingest_codal_report`; the 
reply.md:1614:reply.md:1489:reply.md:1349:reply.md:1181:ingest_codal_report / 
reply.md:1615:reply.md:1490:reply.md:1350:reply.md:1183:`ingest_codal_report` 
reply.md:1616:reply.md:1491:reply.md:1351:reply.md:1185:ingest_codal_report()
reply.md:1617:reply.md:1492:reply.md:1352:reply.md:1186:reply.md:1009:reply.md:838:`ingest_codal_report()` 
reply.md:1618:reply.md:1493:reply.md:1353:reply.md:1187:reply.md:1011:`ingest_codal_report`، 
reply.md:1619:reply.md:1495:`load_codal_pdf` و 
reply.md:1620:reply.md:1496:reply.md:1356:reply.md:1190:reply.md:1013:reply.md:842:reply.md:668:reply.md:490:`ingest_co
dal_report()`:
reply.md:1621:reply.md:1499:reply.md:1359:reply.md:1193:reply.md:1016:reply.md:845:reply.md:671:reply.md:494:`ingest_co
dal_report()` 
reply.md:1624:reply.md:1501:reply.md:1361:reply.md:1203:reply.md:1025:reply.md:854:`load_codal_pdf_from_url` 
reply.md:1625:reply.md:1506:reply.md:1370:reply.md:1214:reply.md:1036:reply.md:862:reply.md:687:`financial_periods.peri
od_id`.
reply.md:1626:reply.md:1509:reply.md:1373:reply.md:1218:`financial_period_id` در DTOها 
reply.md:1627:reply.md:1510:reply.md:1374:reply.md:1219:reply.md:1040:reply.md:867:`reports.financial_period_id` 
reply.md:1628:reply.md:1511:reply.md:1375:reply.md:1221:`financial_period_id` 
reply.md:1629:reply.md:1512:reply.md:1377:`ingest_codal_report` یک 
reply.md:1630:reply.md:1513:reply.md:1381:`ingest_codal_pdf` 
reply.md:1631:reply.md:1515:`load_codal_pdf` و 
reply.md:1632:reply.md:1516:reply.md:1383:reply.md:1228:`load_codal_pdf_from_url` پس 
reply.md:1633:reply.md:1525:reply.md:1391:reply.md:1238:reply.md:1060:`src/ingestion/service.py::ingest_codal_report` 
است؛ 
reply.md:1634:reply.md:1532:reply.md:1398:reply.md:1249:reply.md:1069:reply.md:892:reply.md:717:reply.md:535:ingest_cod
al_pdf 
reply.md:1635:reply.md:1534:load_codal_pdf و 
reply.md:1636:reply.md:1535:reply.md:1400:reply.md:1251:load_codal_pdf_from_url را 
reply.md:1641:reply.md:1540:reply.md:1405:reply.md:1255:reply.md:1076:`financial_period_id` | 
reply.md:1644:reply.md:1542:reply.md:1407:reply.md:1257:reply.md:1078:reply.md:901:reply.md:726:reply.md:546:`ingest_co
dal_report(...
reply.md:1648:reply.md:1544:reply.md:1409:reply.md:1259:reply.md:1080:reply.md:905:reply.md:731:ingest_codal_report  
reply.md:1649:reply.md:1547:reply.md:1412:reply.md:1261:ingest_codal_report 
reply.md:1652:reply.md:1549:reply.md:1416:reply.md:1264:reply.md:1085:reply.md:910:reply.md:736:reply.md:555:financial_
period_id 
reply.md:1654:reply.md:1550:reply.md:1417:reply.md:1265:reply.md:1086:reply.md:911:reply.md:737:reply.md:557:financial_
period_id در 
reply.md:1656:reply.md:1551:reply.md:1418:reply.md:1268:reply.md:1088:reply.md:913:reply.md:739:reply.md:560:ingest_cod
al_report
reply.md:1657:reply.md:1552:reply.md:1419:reply.md:1269:reply.md:1089:reply.md:914:reply.md:740:reply.md:562:`financial
_periods` — 
reply.md:1658:reply.md:1553:reply.md:1420:reply.md:1270:reply.md:1090:reply.md:916:`reports.financial_period_id` must 
not be 
reply.md:1661:reply.md:1556:reply.md:1422:reply.md:1272:reply.md:1093:`reports.financial_period_id` 
reply.md:1662:reply.md:1559:reply.md:1425:reply.md:1275:reply.md:1097:`financial_periods.company_id` تا 
reply.md:1663:reply.md:1562:reply.md:1428:load_codal_pdf و 
reply.md:1664:reply.md:1563:reply.md:1429:reply.md:1278:load_codal_pdf_from_url |
reply.md:1665:reply.md:1564:reply.md:1432:reply.md:1280:reply.md:1101:reply.md:928:ingest_codal_report 
reply.md:1666:reply.md:1565:reply.md:1434:ingest_codal_report 
reply.md:1667:reply.md:1566:reply.md:1435:reply.md:1283:reply.md:1104:reply.md:931:reply.md:757:reply.md:579:\`ingest_c
odal_report\` 
reply.md:1675:reply.md:1576:reply.md:1444:reply.md:1293:reply.md:1114:reply.md:941:reply.md:767:`Report.financial_perio
d_id` 
reply.md:1676:reply.md:1579:reply.md:1447:reply.md:1298:reply.md:1118:reply.md:945:reply.md:772:`financial_periods` | 
در مسیر 
reply.md:1679:reply.md:1581:reply.md:1449:reply.md:1301:`ingest_codal_report` یک 
reply.md:1680:reply.md:1582:reply.md:1450:reply.md:1302:reply.md:1122:reply.md:949:reply.md:777:`Report.financial_perio
d_id` 
reply.md:1681:reply.md:1583:reply.md:1451:reply.md:1303:reply.md:1124:`Report.financial_period_id` 
reply.md:1682:reply.md:1586:reply.md:1455:reply.md:1311:reply.md:1132:`service.py::ingest_codal_report` می‌رسد.
reply.md:1691:reply.md:1595:reply.md:1465:reply.md:1321:reply.md:1143:reply.md:969:reply.md:797:`financial_period_id` 
در 
reply.md:1692:reply.md:1596:reply.md:1466:reply.md:1322:reply.md:1144:reply.md:970:reply.md:799:`reports.financial_peri
od_id` اشاره 
reply.md:1693:reply.md:1597:reply.md:1469:reply.md:1325:reply.md:1148:`financial_periods.company_id` تا 
reply.md:1694:reply.md:1598:reply.md:1472:reply.md:1329:Report.financial_period_id — 
reply.md:1697:reply.md:1601:reply.md:1476:reply.md:1335:reply.md:1158:reply.md:982:reply.md:812:financial_period_id 
reply.md:1704:reply.md:1608:reply.md:1482:reply.md:1340:reply.md:1166:ingest_codal_report()
reply.md:1707:reply.md:1610:reply.md:1484:reply.md:1344:reply.md:1172:financial_periods, 
reply.md:1710:reply.md:1612:reply.md:1486:reply.md:1346:reply.md:1175:`financial_periods`
reply.md:1711:reply.md:1613:reply.md:1488:`ingest_codal_report`; the 
reply.md:1712:reply.md:1614:reply.md:1489:reply.md:1349:reply.md:1181:ingest_codal_report / 
reply.md:1713:reply.md:1615:reply.md:1490:reply.md:1350:reply.md:1183:`ingest_codal_report` 
reply.md:1714:reply.md:1616:reply.md:1491:reply.md:1351:reply.md:1185:ingest_codal_report()
reply.md:1715:reply.md:1617:reply.md:1492:reply.md:1352:reply.md:1186:reply.md:1009:reply.md:838:`ingest_codal_report()
` 
reply.md:1716:reply.md:1618:reply.md:1493:reply.md:1353:reply.md:1187:reply.md:1011:`ingest_codal_report`، 
reply.md:1717:reply.md:1619:reply.md:1495:`load_codal_pdf` و 
reply.md:1722:reply.md:1624:reply.md:1501:reply.md:1361:reply.md:1203:reply.md:1025:reply.md:854:`load_codal_pdf_from_u
rl` 
reply.md:1723:reply.md:1625:reply.md:1506:reply.md:1370:reply.md:1214:reply.md:1036:reply.md:862:reply.md:687:`financia
l_periods.peri
reply.md:1725:reply.md:1626:reply.md:1509:reply.md:1373:reply.md:1218:`financial_period_id` در DTOها 
reply.md:1726:reply.md:1627:reply.md:1510:reply.md:1374:reply.md:1219:reply.md:1040:reply.md:867:`reports.financial_per
iod_id` 
reply.md:1727:reply.md:1628:reply.md:1511:reply.md:1375:reply.md:1221:`financial_period_id` 
reply.md:1728:reply.md:1629:reply.md:1512:reply.md:1377:`ingest_codal_report` یک 
reply.md:1729:reply.md:1630:reply.md:1513:reply.md:1381:`ingest_codal_pdf` 
reply.md:1730:reply.md:1631:reply.md:1515:`load_codal_pdf` و 
reply.md:1731:reply.md:1632:reply.md:1516:reply.md:1383:reply.md:1228:`load_codal_pdf_from_url` پس 
reply.md:1732:reply.md:1633:reply.md:1525:reply.md:1391:reply.md:1238:reply.md:1060:`src/ingestion/service.py::ingest_c
odal_report` 
reply.md:1736:reply.md:1635:reply.md:1534:load_codal_pdf و 
reply.md:1737:reply.md:1636:reply.md:1535:reply.md:1400:reply.md:1251:load_codal_pdf_from_url را 
reply.md:1738:reply.md:1641:reply.md:1540:reply.md:1405:reply.md:1255:reply.md:1076:`financial_period_id` | 
reply.md:1741:reply.md:1648:reply.md:1544:reply.md:1409:reply.md:1259:reply.md:1080:reply.md:905:reply.md:731:ingest_co
dal_report  
reply.md:1742:reply.md:1649:reply.md:1547:reply.md:1412:reply.md:1261:ingest_codal_report 
reply.md:1751:reply.md:1658:reply.md:1553:reply.md:1420:reply.md:1270:reply.md:1090:reply.md:916:`reports.financial_per
iod_id` must 
reply.md:1753:reply.md:1661:reply.md:1556:reply.md:1422:reply.md:1272:reply.md:1093:`reports.financial_period_id` 
reply.md:1754:reply.md:1662:reply.md:1559:reply.md:1425:reply.md:1275:reply.md:1097:`financial_periods.company_id` تا 
reply.md:1755:reply.md:1663:reply.md:1562:reply.md:1428:load_codal_pdf و 
reply.md:1756:reply.md:1664:reply.md:1563:reply.md:1429:reply.md:1278:load_codal_pdf_from_url |
reply.md:1757:reply.md:1665:reply.md:1564:reply.md:1432:reply.md:1280:reply.md:1101:reply.md:928:ingest_codal_report 
reply.md:1758:reply.md:1666:reply.md:1565:reply.md:1434:ingest_codal_report 
reply.md:1763:reply.md:1676:reply.md:1579:reply.md:1447:reply.md:1298:reply.md:1118:reply.md:945:reply.md:772:`financia
l_periods` | 
reply.md:1765:reply.md:1679:reply.md:1581:reply.md:1449:reply.md:1301:`ingest_codal_report` یک 
reply.md:1768:reply.md:1681:reply.md:1583:reply.md:1451:reply.md:1303:reply.md:1124:`Report.financial_period_id` 
reply.md:1769:reply.md:1682:reply.md:1586:reply.md:1455:reply.md:1311:reply.md:1132:`service.py::ingest_codal_report` 
می‌رسد.
reply.md:1770:reply.md:1691:reply.md:1595:reply.md:1465:reply.md:1321:reply.md:1143:reply.md:969:reply.md:797:`financia
l_period_id` 
reply.md:1774:reply.md:1693:reply.md:1597:reply.md:1469:reply.md:1325:reply.md:1148:`financial_periods.company_id` تا 
reply.md:1775:reply.md:1694:reply.md:1598:reply.md:1472:reply.md:1329:Report.financial_period_id — 
reply.md:1776:reply.md:1697:reply.md:1601:reply.md:1476:reply.md:1335:reply.md:1158:reply.md:982:reply.md:812:financial
_period_id 
reply.md:1777:reply.md:1704:reply.md:1608:reply.md:1482:reply.md:1340:reply.md:1166:ingest_codal_report()
reply.md:1778:reply.md:1707:reply.md:1610:reply.md:1484:reply.md:1344:reply.md:1172:financial_periods, 
reply.md:1779:reply.md:1710:reply.md:1612:reply.md:1486:reply.md:1346:reply.md:1175:`financial_periods`
reply.md:1780:reply.md:1711:reply.md:1613:reply.md:1488:`ingest_codal_report`; the 
reply.md:1781:reply.md:1712:reply.md:1614:reply.md:1489:reply.md:1349:reply.md:1181:ingest_codal_report / 
reply.md:1782:reply.md:1713:reply.md:1615:reply.md:1490:reply.md:1350:reply.md:1183:`ingest_codal_report` 
reply.md:1783:reply.md:1714:reply.md:1616:reply.md:1491:reply.md:1351:reply.md:1185:ingest_codal_report()
reply.md:1784:reply.md:1715:reply.md:1617:reply.md:1492:reply.md:1352:reply.md:1186:reply.md:1009:reply.md:838:`ingest_
codal_report()
reply.md:1786:reply.md:1716:reply.md:1618:reply.md:1493:reply.md:1353:reply.md:1187:reply.md:1011:`ingest_codal_report`
، 
reply.md:1787:reply.md:1717:reply.md:1619:reply.md:1495:`load_codal_pdf` و 
reply.md:1788:reply.md:1722:reply.md:1624:reply.md:1501:reply.md:1361:reply.md:1203:reply.md:1025:reply.md:854:`load_co
dal_pdf_from_u
reply.md:1792:reply.md:1725:reply.md:1626:reply.md:1509:reply.md:1373:reply.md:1218:`financial_period_id` در DTOها 
reply.md:1795:reply.md:1727:reply.md:1628:reply.md:1511:reply.md:1375:reply.md:1221:`financial_period_id` 
reply.md:1796:reply.md:1728:reply.md:1629:reply.md:1512:reply.md:1377:`ingest_codal_report` یک 
reply.md:1797:reply.md:1729:reply.md:1630:reply.md:1513:reply.md:1381:`ingest_codal_pdf` 
reply.md:1798:reply.md:1730:reply.md:1631:reply.md:1515:`load_codal_pdf` و 
reply.md:1799:reply.md:1731:reply.md:1632:reply.md:1516:reply.md:1383:reply.md:1228:`load_codal_pdf_from_url` پس 
reply.md:1802:reply.md:1736:reply.md:1635:reply.md:1534:load_codal_pdf و 
reply.md:1803:reply.md:1737:reply.md:1636:reply.md:1535:reply.md:1400:reply.md:1251:load_codal_pdf_from_url را 
reply.md:1804:reply.md:1738:reply.md:1641:reply.md:1540:reply.md:1405:reply.md:1255:reply.md:1076:`financial_period_id`
 | 
reply.md:1807:reply.md:1742:reply.md:1649:reply.md:1547:reply.md:1412:reply.md:1261:ingest_codal_report 
reply.md:1810:reply.md:1753:reply.md:1661:reply.md:1556:reply.md:1422:reply.md:1272:reply.md:1093:`reports.financial_pe
riod_id` 
reply.md:1811:reply.md:1754:reply.md:1662:reply.md:1559:reply.md:1425:reply.md:1275:reply.md:1097:`financial_periods.co
mpany_id` تا 
reply.md:1812:reply.md:1755:reply.md:1663:reply.md:1562:reply.md:1428:load_codal_pdf و 
reply.md:1813:reply.md:1756:reply.md:1664:reply.md:1563:reply.md:1429:reply.md:1278:load_codal_pdf_from_url |
reply.md:1814:reply.md:1757:reply.md:1665:reply.md:1564:reply.md:1432:reply.md:1280:reply.md:1101:reply.md:928:ingest_c
odal_report 
reply.md:1815:reply.md:1758:reply.md:1666:reply.md:1565:reply.md:1434:ingest_codal_report 
reply.md:1818:reply.md:1765:reply.md:1679:reply.md:1581:reply.md:1449:reply.md:1301:`ingest_codal_report` یک 
reply.md:1819:reply.md:1768:reply.md:1681:reply.md:1583:reply.md:1451:reply.md:1303:reply.md:1124:`Report.financial_per
iod_id` 
reply.md:1820:reply.md:1769:reply.md:1682:reply.md:1586:reply.md:1455:reply.md:1311:reply.md:1132:`service.py::ingest_c
odal_report` 
reply.md:1824:reply.md:1774:reply.md:1693:reply.md:1597:reply.md:1469:reply.md:1325:reply.md:1148:`financial_periods.co
mpany_id` تا 
reply.md:1825:reply.md:1775:reply.md:1694:reply.md:1598:reply.md:1472:reply.md:1329:Report.financial_period_id — 
reply.md:1828:reply.md:1777:reply.md:1704:reply.md:1608:reply.md:1482:reply.md:1340:reply.md:1166:ingest_codal_report()
reply.md:1829:reply.md:1778:reply.md:1707:reply.md:1610:reply.md:1484:reply.md:1344:reply.md:1172:financial_periods, 
reply.md:1830:reply.md:1779:reply.md:1710:reply.md:1612:reply.md:1486:reply.md:1346:reply.md:1175:`financial_periods`
reply.md:1831:reply.md:1780:reply.md:1711:reply.md:1613:reply.md:1488:`ingest_codal_report`; the 
reply.md:1832:reply.md:1781:reply.md:1712:reply.md:1614:reply.md:1489:reply.md:1349:reply.md:1181:ingest_codal_report 
/ 
reply.md:1833:reply.md:1782:reply.md:1713:reply.md:1615:reply.md:1490:reply.md:1350:reply.md:1183:`ingest_codal_report`
 
reply.md:1834:reply.md:1783:reply.md:1714:reply.md:1616:reply.md:1491:reply.md:1351:reply.md:1185:ingest_codal_report()
reply.md:1837:reply.md:1786:reply.md:1716:reply.md:1618:reply.md:1493:reply.md:1353:reply.md:1187:reply.md:1011:`ingest
_codal_report`
reply.md:1839:reply.md:1787:reply.md:1717:reply.md:1619:reply.md:1495:`load_codal_pdf` و 
reply.md:1842:reply.md:1792:reply.md:1725:reply.md:1626:reply.md:1509:reply.md:1373:reply.md:1218:`financial_period_id`
 در DTOها 
reply.md:1843:reply.md:1795:reply.md:1727:reply.md:1628:reply.md:1511:reply.md:1375:reply.md:1221:`financial_period_id`
 
reply.md:1844:reply.md:1796:reply.md:1728:reply.md:1629:reply.md:1512:reply.md:1377:`ingest_codal_report` یک 
reply.md:1845:reply.md:1797:reply.md:1729:reply.md:1630:reply.md:1513:reply.md:1381:`ingest_codal_pdf` 
reply.md:1846:reply.md:1798:reply.md:1730:reply.md:1631:reply.md:1515:`load_codal_pdf` و 
reply.md:1847:reply.md:1799:reply.md:1731:reply.md:1632:reply.md:1516:reply.md:1383:reply.md:1228:`load_codal_pdf_from_
url` پس 
reply.md:1848:reply.md:1802:reply.md:1736:reply.md:1635:reply.md:1534:load_codal_pdf و 
reply.md:1849:reply.md:1803:reply.md:1737:reply.md:1636:reply.md:1535:reply.md:1400:reply.md:1251:load_codal_pdf_from_u
rl را 
reply.md:1850:reply.md:1804:reply.md:1738:reply.md:1641:reply.md:1540:reply.md:1405:reply.md:1255:reply.md:1076:`financ
ial_period_id`
reply.md:1852:reply.md:1807:reply.md:1742:reply.md:1649:reply.md:1547:reply.md:1412:reply.md:1261:ingest_codal_report 
reply.md:1855:reply.md:1811:reply.md:1754:reply.md:1662:reply.md:1559:reply.md:1425:reply.md:1275:reply.md:1097:`financ
ial_periods.co
reply.md:1857:reply.md:1812:reply.md:1755:reply.md:1663:reply.md:1562:reply.md:1428:load_codal_pdf و 
reply.md:1858:reply.md:1813:reply.md:1756:reply.md:1664:reply.md:1563:reply.md:1429:reply.md:1278:load_codal_pdf_from_u
rl |
reply.md:1861:reply.md:1815:reply.md:1758:reply.md:1666:reply.md:1565:reply.md:1434:ingest_codal_report 
reply.md:1862:reply.md:1818:reply.md:1765:reply.md:1679:reply.md:1581:reply.md:1449:reply.md:1301:`ingest_codal_report`
 یک 
reply.md:1867:reply.md:1824:reply.md:1774:reply.md:1693:reply.md:1597:reply.md:1469:reply.md:1325:reply.md:1148:`financ
ial_periods.co
reply.md:1869:reply.md:1825:reply.md:1775:reply.md:1694:reply.md:1598:reply.md:1472:reply.md:1329:Report.financial_peri
od_id — 
reply.md:1870:reply.md:1828:reply.md:1777:reply.md:1704:reply.md:1608:reply.md:1482:reply.md:1340:reply.md:1166:ingest_
codal_report()
reply.md:1871:reply.md:1829:reply.md:1778:reply.md:1707:reply.md:1610:reply.md:1484:reply.md:1344:reply.md:1172:financi
al_periods, 
reply.md:1872:reply.md:1830:reply.md:1779:reply.md:1710:reply.md:1612:reply.md:1486:reply.md:1346:reply.md:1175:`financ
ial_periods`
reply.md:1873:reply.md:1831:reply.md:1780:reply.md:1711:reply.md:1613:reply.md:1488:`ingest_codal_report`; the 
reply.md:1874:reply.md:1832:reply.md:1781:reply.md:1712:reply.md:1614:reply.md:1489:reply.md:1349:reply.md:1181:ingest_
codal_report 
reply.md:1876:reply.md:1833:reply.md:1782:reply.md:1713:reply.md:1615:reply.md:1490:reply.md:1350:reply.md:1183:`ingest
_codal_report`
reply.md:1878:reply.md:1834:reply.md:1783:reply.md:1714:reply.md:1616:reply.md:1491:reply.md:1351:reply.md:1185:ingest_
codal_report()
reply.md:1881:reply.md:1839:reply.md:1787:reply.md:1717:reply.md:1619:reply.md:1495:`load_codal_pdf` و 
reply.md:1882:reply.md:1842:reply.md:1792:reply.md:1725:reply.md:1626:reply.md:1509:reply.md:1373:reply.md:1218:`financ
ial_period_id`
reply.md:1884:reply.md:1843:reply.md:1795:reply.md:1727:reply.md:1628:reply.md:1511:reply.md:1375:reply.md:1221:`financ
ial_period_id`
reply.md:1886:reply.md:1844:reply.md:1796:reply.md:1728:reply.md:1629:reply.md:1512:reply.md:1377:`ingest_codal_report`
 یک 
reply.md:1887:reply.md:1845:reply.md:1797:reply.md:1729:reply.md:1630:reply.md:1513:reply.md:1381:`ingest_codal_pdf` 
reply.md:1888:reply.md:1846:reply.md:1798:reply.md:1730:reply.md:1631:reply.md:1515:`load_codal_pdf` و 
reply.md:1889:reply.md:1847:reply.md:1799:reply.md:1731:reply.md:1632:reply.md:1516:reply.md:1383:reply.md:1228:`load_c
odal_pdf_from_
reply.md:1891:reply.md:1848:reply.md:1802:reply.md:1736:reply.md:1635:reply.md:1534:load_codal_pdf و 
reply.md:1892:reply.md:1849:reply.md:1803:reply.md:1737:reply.md:1636:reply.md:1535:reply.md:1400:reply.md:1251:load_co
dal_pdf_from_u
reply.md:1896:reply.md:1852:reply.md:1807:reply.md:1742:reply.md:1649:reply.md:1547:reply.md:1412:reply.md:1261:ingest_
codal_report 
reply.md:1899:reply.md:1857:reply.md:1812:reply.md:1755:reply.md:1663:reply.md:1562:reply.md:1428:load_codal_pdf و 
reply.md:1900:reply.md:1858:reply.md:1813:reply.md:1756:reply.md:1664:reply.md:1563:reply.md:1429:reply.md:1278:load_co
dal_pdf_from_u
reply.md:1902:reply.md:1861:reply.md:1815:reply.md:1758:reply.md:1666:reply.md:1565:reply.md:1434:ingest_codal_report 
reply.md:1903:reply.md:1862:reply.md:1818:reply.md:1765:reply.md:1679:reply.md:1581:reply.md:1449:reply.md:1301:`ingest
_codal_report`
reply.md:1915:reply.md:1873:reply.md:1831:reply.md:1780:reply.md:1711:reply.md:1613:reply.md:1488:`ingest_codal_report`
; the 
reply.md:1922:reply.md:1881:reply.md:1839:reply.md:1787:reply.md:1717:reply.md:1619:reply.md:1495:`load_codal_pdf` و 
reply.md:1927:reply.md:1886:reply.md:1844:reply.md:1796:reply.md:1728:reply.md:1629:reply.md:1512:reply.md:1377:`ingest
_codal_report`
reply.md:1929:reply.md:1887:reply.md:1845:reply.md:1797:reply.md:1729:reply.md:1630:reply.md:1513:reply.md:1381:`ingest
_codal_pdf` 
reply.md:1930:reply.md:1888:reply.md:1846:reply.md:1798:reply.md:1730:reply.md:1631:reply.md:1515:`load_codal_pdf` و 
reply.md:1933:reply.md:1891:reply.md:1848:reply.md:1802:reply.md:1736:reply.md:1635:reply.md:1534:load_codal_pdf و 
reply.md:1938:reply.md:1899:reply.md:1857:reply.md:1812:reply.md:1755:reply.md:1663:reply.md:1562:reply.md:1428:load_co
dal_pdf و 
reply.md:1941:reply.md:1902:reply.md:1861:reply.md:1815:reply.md:1758:reply.md:1666:reply.md:1565:reply.md:1434:ingest_
codal_report 
reply.md:1944:reply.md:1915:reply.md:1873:reply.md:1831:reply.md:1780:reply.md:1711:reply.md:1613:reply.md:1488:`ingest
_codal_report`
reply.md:1946:reply.md:1922:reply.md:1881:reply.md:1839:reply.md:1787:reply.md:1717:reply.md:1619:reply.md:1495:`load_c
odal_pdf` و 
reply.md:1951:reply.md:1930:reply.md:1888:reply.md:1846:reply.md:1798:reply.md:1730:reply.md:1631:reply.md:1515:`load_c
odal_pdf` و 
reply.md:1952:reply.md:1933:reply.md:1891:reply.md:1848:reply.md:1802:reply.md:1736:reply.md:1635:reply.md:1534:load_co
dal_pdf و 
STAGE7_MASTER_WORKING_PACKET.md:95:  | 1 — دادهٔ منبع | دادهٔ مالی ذخیره‌شده؛ `src/forecast/queries.py` آن را با 
`Session` می‌خواند | `ingest_codal_report` در `src/ingestion/service.py` ورودی منبع را می‌نویسد؛ خروجی تحلیلی تولید 
نمی‌کند | ingestion caller باید Session بدهد؛ سرویس در مسیر نوشتن commit/rollback می‌کند و آن را نمی‌بندد | Stage 5 
queryها می‌توانند facts را بخوانند؛ زنجیرهٔ کامل از ingestion تا مراحل بعد اثبات نشده |


