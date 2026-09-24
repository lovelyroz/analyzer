# Golden Dataset Schema

## وضعیت

```text
GOLDEN DATA STATUS: BLOCKED
EXTERNAL INDEPENDENT SOURCE REQUIRED
```

این سند فقط schema و قواعد پیشنهادی Golden Dataset را تعریف می‌کند. هیچ مقدار مالی، fixture، JSON، CSV یا expected value در آن ثبت نشده است.

ساخت Golden Dataset تا زمانی مجاز نیست که برای هر رکورد، منبع مستقل و معتبر CODAL یا منبع رسمی مستقل دیگری شناسایی و قابل بازبینی باشد.

## 1. هدف و محدوده

Golden Dataset باید یک مرجع مستقل برای بررسی صحت داده‌های خام CODAL باشد. این dataset نباید از موارد زیر ساخته شود:

- خروجی extractor تولیدی؛
- رکوردهای production database؛
- fixtureهای synthetic؛
- parser دوم روی همان PDF؛
- بازسازی متن PDF؛
- حدس، برآورد یا رونویسی تأییدنشده؛
- تبدیل مقدار نامشخص به صفر.

این سند به Golden Accuracy test، persistence، mapping، KPI، scoring، forecast، valuation یا decision logic تعلق ندارد.

## 2. وضعیت شواهد فعلی چهار PDF

در زمان تهیه این schema، هیچ‌یک از چهار PDF دارای هویت رسمی CODAL، tracking/report ID رسمی، URL رسمی، یا منبع مستقل کافی برای ساخت expected values نیستند.

| PDF | SHA-256 محلی | هویت رسمی CODAL | ID رسمی | URL رسمی | وضعیت identity | امکان تأیید مستقل مقدار مالی |
|---|---|---|---|---|---|---|
| seo-codal-report (1).pdf | `2ac373cd19bcf64f95cba562a095c130def4d84a294ef3c5e39352db2efaa216` | ثبت نشده | ثبت نشده | ثبت نشده | `UNVERIFIED` | خیر |
| seo-codal-report (3).pdf | `fd043c49e04525f725fa6df6f603084566742f1a15694e0b44fea1d868257f19` | ثبت نشده | ثبت نشده | ثبت نشده | `UNVERIFIED` | خیر |
| seo-codal-report (10).pdf | `335acc828dfb1f1cb8283114388a08c3c08c2111a0035b3498d12a4e1aba35df` | ثبت نشده | ثبت نشده | ثبت نشده | `UNVERIFIED` | خیر |
| seo-codal-report (13).pdf | `b66d4d68170a5881025fddc337b7bfdde7926e0b42f39366302a8075f6c336d4` | ثبت نشده | ثبت نشده | ثبت نشده | `UNVERIFIED` | خیر |

### نتیجه فعلی برای هر PDF

برای هر چهار فایل، موارد زیر هنوز تأیید نشده است:

1. هویت دقیق گزارش رسمی CODAL؛
2. CODAL tracking/report ID؛
3. URL رسمی؛
4. هویت رسمی شرکت؛
5. عنوان رسمی گزارش؛
6. نوع رسمی گزارش؛
7. زمان رسمی انتشار؛
8. دوره مالی رسمی؛
9. وضعیت correction/restatement/version؛
10. اتصال بدون ابهام خود PDF به رکورد رسمی؛
11. امکان تأیید مستقل مقادیر مالی دقیق؛
12. امکان تأیید مستقل section/row/column provenance.

سرنخ‌های قابل مشاهده در PDF، از جمله نام شرکت، نوع گزارش و تاریخ، فقط supporting evidence هستند و به‌تنهایی هویت رسمی یا مقدار Golden را ثابت نمی‌کنند.

## 3. ساختار رکورد Golden Dataset

هر رکورد Golden باید حداقل فیلدهای زیر را داشته باشد. مقدار هر فیلد باید از منبع مستقل قابل ردیابی باشد؛ در این مرحله همه فیلدهای نمونه خالی باقی می‌مانند.

### 3.1 هویت فایل و گزارش

| فیلد | نوع پیشنهادی | الزام | توضیح |
|---|---|---|---|
| `pdf_filename` | string | اجباری | نام فایل محلی نمونه؛ به‌تنهایی هویت رسمی نیست. |
| `pdf_sha256` | lowercase hex string | اجباری | هش دقیق bytes فایل محلی. |
| `official_codal_tracking_id` | string | اجباری | شناسه رسمی گزارش در CODAL؛ مقدار synthetic مجاز نیست. |
| `official_source_url` | URL | اجباری | URL رسمی CODAL یا منبع رسمی مستقل قابل بازبینی. |
| `company_id` | string | اجباری | شناسه شرکت از منبع رسمی؛ ticker به‌تنهایی کافی نیست. |
| `company_name` | string | اجباری | نام رسمی شرکت در منبع authoritative. |
| `official_report_title` | string | اجباری | عنوان رسمی گزارش. |
| `official_report_type` | string | اجباری | نوع رسمی گزارش، نه label تولیدی تست. |
| `publication_datetime` | timezone-aware datetime | اجباری | زمان رسمی انتشار/دسترس‌پذیری برای PIT. |
| `financial_period` | structured object | اجباری | دوره مالی، تاریخ شروع/پایان، نوع دوره، و در صورت وجود سال/فصل/ماه. |
| `version_status` | enum/object | اجباری | original/current/corrected/restated و شناسه یا توضیح نسخه. |

### 3.2 محل و هویت قلم خام

| فیلد | نوع پیشنهادی | الزام | توضیح |
|---|---|---|---|
| `source_section` | string/null | اجباری | بخش رسمی منبع؛ اگر وجود ندارد، `NULL` مستند شود. |
| `source_row` | string/integer/null | اجباری | ردیف رسمی یا شماره ردیف قابل ردیابی. |
| `source_column` | string/integer/null | اجباری | ستون رسمی یا شماره ستون قابل ردیابی. |
| `raw_item_name` | string | اجباری | نام خام دقیق همان‌گونه که در منبع رسمی ثبت شده است. |
| `raw_item_code` | string/null | اجباری | کد خام در صورت وجود؛ نبودن باید صریحاً `NULL` باشد. |
| `expected_value` | exact Decimal/null | اجباری | مقدار دقیق مستقل یا `NULL` واقعی؛ نباید به‌صورت float ذخیره شود. |
| `unit` | string/null | اجباری | واحد مستقل تأییدشده. |
| `currency` | string/null | اجباری | ارز مستقل تأییدشده، مانند IRR؛ نباید حدس زده شود. |

### 3.3 provenance و شواهد

| فیلد | نوع پیشنهادی | الزام | توضیح |
|---|---|---|---|
| `evidence_reference` | structured object/list | اجباری | لینک/شناسه منبع، صفحه یا بخش، تاریخ دسترسی، و روش تأیید. |
| `source_document_hash` | lowercase hex string/null | توصیه‌شده | هش سند رسمی دریافت‌شده، در صورت امکان. |
| `identity_match_evidence` | structured object/list | اجباری | شواهد اتصال دقیق PDF به گزارش رسمی. |
| `value_verification_method` | enum | اجباری | روش مستقل تأیید مقدار، بدون استفاده از extractor تولیدی. |
| `review_status` | enum | اجباری | `VERIFIED`, `PARTIALLY_VERIFIED`, یا `UNVERIFIED`. |
| `review_notes` | string | اجباری | ابهام‌ها، محدودیت‌ها و تصمیم reviewer. |

## 4. قالب پیشنهادی structured objectها

### 4.1 `financial_period`

```text
{
  "period_type": "QUARTER | MONTH | YEAR | YTD | OTHER",
  "start_date": "YYYY-MM-DD or Jalali source date",
  "end_date": "YYYY-MM-DD or Jalali source date",
  "fiscal_year": "exact official value",
  "fiscal_quarter": "exact official value or NULL",
  "months_length": "exact official value or NULL",
  "is_ytd": "true | false | NULL",
  "evidence_reference": "independent source reference"
}
```

قالب بالا فقط ساختار است و شامل مقدار واقعی گزارش‌ها نیست.

### 4.2 `version_status`

```text
{
  "version_kind": "ORIGINAL | CURRENT | CORRECTED | RESTATED | UNKNOWN",
  "version_number": "exact official value or NULL",
  "is_current": "true | false | NULL",
  "supersedes_tracking_id": "official ID or NULL",
  "correction_reference": "official reference or NULL",
  "evidence_reference": "independent source reference"
}
```

### 4.3 `evidence_reference`

```text
{
  "source_class": "AUTHORITATIVE | SUPPORTING | INTERNAL_ONLY",
  "source_url": "official URL or NULL",
  "source_identifier": "official record/document identifier",
  "retrieved_at": "timestamp",
  "document_hash": "SHA-256 or NULL",
  "location": "page/section/row/column or NULL",
  "reviewer": "review identity",
  "review_action": "how the evidence was independently checked"
}
```

`INTERNAL_ONLY` هرگز برای اثبات Golden identity یا Golden value کافی نیست.

## 5. سلسله‌مراتب منابع

### A. AUTHORITATIVE

منابع قابل قبول برای ساخت Golden Dataset:

- صفحه رسمی گزارش در CODAL؛
- metadata رسمی CODAL؛
- official tracking/report ID؛
- سند رسمی منتشرشده با ارتباط قابل اثبات به همان گزارش؛
- داده رسمی مستقل که title، company، period، version و value را قابل بازبینی ارائه کند.

### B. SUPPORTING

منابعی که به تطبیق کمک می‌کنند اما به‌تنهایی کافی نیستند:

- نام شرکت در PDF؛
- عنوان یا نوع گزارش قابل مشاهده؛
- تاریخ یا دوره قابل مشاهده؛
- PDF hash؛
- metadata تولید فایل؛
- گزارش حسابرس یا سند پشتیبان، فقط در صورت اتصال صریح به گزارش رسمی.

### C. INTERNAL_ONLY

منابعی که هرگز نباید Golden evidence محسوب شوند:

- نام فایل محلی؛
- synthetic metadata تست‌ها؛
- `local://` و `example.invalid`؛
- CODAL ID تولیدشده در تست؛
- خروجی extractor تولیدی؛
- رکوردهای database تولیدشده توسط application؛
- fixtureهای ساخته‌شده از خروجی سیستم؛
- parser دوم روی همان PDF.

## 6. قواعد مقایسه و تطبیق

### 6.1 مقایسه Decimal دقیق

- مقدارها باید با نوع decimal دقیق ذخیره شوند.
- مقایسه باید بدون float conversion انجام شود.
- scale و sign باید طبق منبع رسمی حفظ شوند، مگر اینکه قاعده‌ای مستقل و مستند اعمال شود.
- جداکننده هزارگان و رقم‌های فارسی/عربی باید فقط طبق یک قاعده مستند تبدیل شوند؛ این تبدیل به‌تنهایی اعتبار منبع را ایجاد نمی‌کند.

### 6.2 تفاوت NULL و صفر

- `NULL` یعنی مقدار در منبع رسمی موجود یا قابل گزارش نیست.
- صفر یعنی منبع رسمی صراحتاً صفر گزارش کرده است.
- `NULL != 0` و هیچ مقدار نامشخصی نباید به صفر تبدیل شود.
- مقدار خالی، خط تیره، نامشخص یا غیرقابل خواندن باید فقط با شواهد رسمی به `NULL` تبدیل شود.

### 6.3 تطبیق deterministic

هر رکورد باید با کلید ترکیبی زیر به‌صورت deterministic قابل تطبیق باشد:

```text
(pdf_sha256,
 official_codal_tracking_id,
 version_status,
 financial_period,
 source_section,
 source_row,
 source_column,
 raw_item_name,
 raw_item_code)
```

اگر این کلید کامل یا یکتا نباشد، رکورد نباید به‌عنوان Golden verified پذیرفته شود و باید با وضعیت مناسب review علامت‌گذاری شود.

## 7. الزامات provenance

برای هر expected value باید مسیر زیر قابل بازسازی باشد:

```text
local PDF hash
  → official CODAL record identity
  → official source document/version
  → section / row / column
  → raw item name/code
  → exact Decimal or explicit NULL
  → unit and currency
  → independent evidence reference
```

نبودن هر حلقه‌ای از این زنجیره باید به failure classification منجر شود، نه به حدس یا تکمیل دستی.

## 8. الزامات version و PIT

- `publication_datetime` باید از منبع رسمی بیاید، نه از test fixture یا زمان اجرای ingestion.
- گزارش منطقی و نسخه منتشرشده باید جداگانه حفظ شوند.
- correction/restatement نباید نسخه قبلی را حذف یا overwrite کند.
- Golden record باید مشخص کند در زمان cutoff مربوطه کدام نسخه قابل دسترس بوده است.
- اگر نسخه رسمی یا رابطه supersession نامعلوم باشد، مقدار `version_status` نباید حدس زده شود.

## 9. استقلال منبع

ساخت Golden Dataset فقط وقتی مجاز است که:

1. identity رسمی گزارش مستقل از production pipeline تأیید شده باشد؛
2. خود PDF با hash مشخص به همان گزارش رسمی متصل شده باشد؛
3. expected value از منبع authoritative یا سند مستقل قابل بازبینی به‌دست آمده باشد؛
4. مقدار، `NULL`/صفر، unit، currency و provenance مستقل تأیید شده باشند؛
5. reviewer بتواند نتیجه را بدون اعتماد به extractor یا database production بازتولید کند.

تشابه نام شرکت، عنوان، دوره یا تاریخ به‌تنهایی کافی نیست.

## 10. طبقه‌بندی شکست

هر رکورد Golden یا بررسی identity باید دقیقاً یکی از وضعیت‌های زیر را داشته باشد:

- `VERIFIED`: هویت، منبع authoritative، مقدار دقیق، provenance، unit/currency و PIT/version همگی مستقل تأیید شده‌اند.
- `PARTIALLY_VERIFIED`: هویت یا بخشی از metadata با شواهد قوی پشتیبانی می‌شود، اما حداقل یک الزام authoritative یا مقدار دقیق هنوز تأیید نشده است. این رکورد برای expected-value fixture قابل استفاده نیست.
- `UNVERIFIED`: هویت یا منبع authoritative قابل اثبات نیست.
- `SOURCE_MISSING`: منبع رسمی مورد نیاز در دسترس نیست.
- `IDENTITY_MISMATCH`: شواهد PDF و منبع رسمی با یکدیگر منطبق نیستند.
- `VALUE_UNVERIFIED`: هویت روشن است اما مقدار دقیق، NULL/صفر، unit/currency یا محل provenance مستقل نیست.
- `PROVENANCE_INCOMPLETE`: مقدار ممکن است دیده شود اما section/row/column یا زنجیره evidence کامل نیست.
- `VERSION_UNRESOLVED`: نسخه، اصلاحیه یا PIT قابل تعیین نیست.

فقط رکورد `VERIFIED` با تمام شواهد لازم می‌تواند بعداً برای ساخت Golden expected fixture بررسی شود؛ این سند هیچ رکوردی با این وضعیت ایجاد نمی‌کند.

## 11. معیار آمادگی

```text
GOLDEN DATA STATUS: READY
```

فقط زمانی مجاز است که حداقل یک PDF نماینده:

- به یک رکورد رسمی CODAL با ID و URL قابل بازبینی متصل شده باشد؛
- اتصال PDF به همان رکورد بدون ابهام باشد؛
- identity، period، publication datetime و version/PIT تأیید شده باشد؛
- values، NULL/zero، unit، currency و provenance section/row/column از منبع مستقل قابل تأیید باشد.

وضعیت فعلی این معیار را ندارد. بنابراین:

```text
GOLDEN DATA STATUS: BLOCKED
EXTERNAL INDEPENDENT SOURCE REQUIRED
```

## 12. محدوده تغییرات و ایمنی معماری

این سند هیچ تغییری در موارد زیر ایجاد نمی‌کند:

- کد production؛
- acquisition یا extraction؛
- persistence؛
- مدل‌ها یا migrationها؛
- معماری ۹ مرحله‌ای؛
- Stage 1 boundary؛
- `DATABASE_CONTRACT_V1.3`؛
- منطق KPI، scoring، forecasting، valuation یا decision؛
- تست‌های موجود.

Golden Dataset، expected-value fixture و Golden Accuracy test در این مرحله ایجاد نشده‌اند.
