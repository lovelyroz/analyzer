# Golden Source Verification Report

## 1. Scope

هدف این گزارش تعیین این است که آیا برای هر یک از چهار PDF نماینده CODAL، شواهد مستقل و authoritative کافی برای ساخت یک Golden Dataset وجود دارد یا خیر.

این مرحله فقط verification منبع و آمادگی Golden Dataset است. در این مرحله:

- هیچ مقدار مالی Golden ساخته یا رونویسی نشده است؛
- هیچ fixture، JSON، CSV یا expected-value dictionary ایجاد نشده است؛
- از production extractor، production database یا parser دوم به‌عنوان منبع حقیقت استفاده نشده است؛
- کد production، persistence، مدل‌ها، migrationها، قرارداد DATABASE_CONTRACT_V1.3 و معماری ۹ مرحله‌ای تغییر نکرده‌اند.

## 2. Reports Investigated

### 2.1 seo-codal-report (1).pdf

SHA-256 محلی ثبت‌شده و بازبینی‌شده:

`2ac373cd19bcf64f95cba562a095c130def4d84a294ef3c5e39352db2efaa216`

| Field | Value | Evidence Class | Verification Status |
|---|---|---|---|
| Official CODAL tracking ID | NOT ESTABLISHED | MISSING | تأیید نشده |
| Official URL | NOT ESTABLISHED | MISSING | تأیید نشده |
| Company | سرنخ متن PDF: بانک ملت | SUPPORTING | هویت رسمی تأیید نشده |
| Report title | سرنخ متن PDF: گزارش فعالیت ماهانه | SUPPORTING | عنوان رسمی تأیید نشده |
| Report type | سرنخ متن PDF: monthly activity report | SUPPORTING | نوع رسمی تأیید نشده |
| Publication datetime | NOT ESTABLISHED؛ تاریخ‌های داخل سند publication datetime رسمی نیستند | MISSING | تأیید نشده |
| Financial period | سرنخ دوره/تاریخ داخل PDF | SUPPORTING | دوره رسمی تأیید نشده |
| Version/correction/restatement status | NOT ESTABLISHED | MISSING | تأیید نشده |
| PDF correspondence | اتصال به رکورد رسمی CODAL وجود ندارد | MISSING | بدون ابهام قابل اثبات نیست |
| Exact financial values available | فقط خروجی/متن PDF موجود است؛ منبع مستقل وجود ندارد | MISSING | قابل تأیید مستقل نیست |
| NULL vs 0 verifiable | خیر | MISSING | مستقل تأیید نشده |
| Unit verifiable | خیر | MISSING | مستقل تأیید نشده |
| Currency verifiable | خیر | MISSING | مستقل تأیید نشده |
| Source provenance verifiable | خیر | MISSING | مستقل تأیید نشده |

**وضعیت:** `GOLDEN_BLOCKED`

**دلیل:** نام شرکت و نوع گزارش فقط supporting clue هستند. tracking ID، URL، metadata رسمی، correspondence بدون ابهام و provenance مستقل وجود ندارد.

### 2.2 seo-codal-report (3).pdf

SHA-256 محلی ثبت‌شده و بازبینی‌شده:

`fd043c49e04525f725fa6df6f603084566742f1a15694e0b44fea1d868257f19`

| Field | Value | Evidence Class | Verification Status |
|---|---|---|---|
| Official CODAL tracking ID | NOT ESTABLISHED | MISSING | تأیید نشده |
| Official URL | NOT ESTABLISHED | MISSING | تأیید نشده |
| Company | سرنخ متن PDF: بانک ملت | SUPPORTING | هویت رسمی تأیید نشده |
| Report title | سرنخ متن PDF: اطلاعات و صورت‌های مالی | SUPPORTING | عنوان رسمی تأیید نشده |
| Report type | سرنخ متن PDF: financial statements | SUPPORTING | نوع رسمی تأیید نشده |
| Publication datetime | NOT ESTABLISHED؛ تاریخ‌های سند publication datetime رسمی نیستند | MISSING | تأیید نشده |
| Financial period | سرنخ دوره سالانه/میان‌دوره‌ای از متن PDF | SUPPORTING | دوره رسمی تأیید نشده |
| Version/correction/restatement status | NOT ESTABLISHED | MISSING | تأیید نشده |
| PDF correspondence | اتصال به رکورد رسمی CODAL وجود ندارد | MISSING | بدون ابهام قابل اثبات نیست |
| Exact financial values available | فقط داده مشتق از PDF/production path موجود است | MISSING | قابل تأیید مستقل نیست |
| NULL vs 0 verifiable | خیر | MISSING | مستقل تأیید نشده |
| Unit verifiable | خیر | MISSING | مستقل تأیید نشده |
| Currency verifiable | خیر | MISSING | مستقل تأیید نشده |
| Source provenance verifiable | خیر | MISSING | مستقل تأیید نشده |

**وضعیت:** `GOLDEN_BLOCKED`

**دلیل:** شواهد متن PDF گزارش مالی و دوره را به‌صورت clue نشان می‌دهند، اما هیچ رکورد رسمی CODAL، شناسه رسمی یا publication/version metadata برای تطبیق وجود ندارد.

### 2.3 seo-codal-report (10).pdf

SHA-256 محلی ثبت‌شده و بازبینی‌شده:

`335acc828dfb1f1cb8283114388a08c3c08c2111a0035b3498d12a4e1aba35df`

| Field | Value | Evidence Class | Verification Status |
|---|---|---|---|
| Official CODAL tracking ID | NOT ESTABLISHED | MISSING | تأیید نشده |
| Official URL | NOT ESTABLISHED | MISSING | تأیید نشده |
| Company | سرنخ متن PDF: صنایع مس شهید باهنر | SUPPORTING | هویت رسمی تأیید نشده |
| Report title | سرنخ متن PDF: اطلاعات و صورت‌های مالی میان‌دوره‌ای | SUPPORTING | عنوان رسمی تأیید نشده |
| Report type | سرنخ متن PDF: interim financial statements | SUPPORTING | نوع رسمی تأیید نشده |
| Publication datetime | NOT ESTABLISHED | MISSING | تأیید نشده |
| Financial period | سرنخ تاریخ‌های 1403/09/30 و 1403/12/30 | SUPPORTING | دوره رسمی تأیید نشده |
| Version/correction/restatement status | فقط سرنخ متن درباره تجدید ارائه/اصلاح؛ شناسه رسمی ندارد | SUPPORTING | نسخه رسمی تأیید نشده |
| PDF correspondence | اتصال به رکورد رسمی CODAL وجود ندارد | MISSING | بدون ابهام قابل اثبات نیست |
| Exact financial values available | فقط متن/خروجی implementation وجود دارد | MISSING | قابل تأیید مستقل نیست |
| NULL vs 0 verifiable | خیر | MISSING | مستقل تأیید نشده |
| Unit verifiable | خیر | MISSING | مستقل تأیید نشده |
| Currency verifiable | خیر | MISSING | مستقل تأیید نشده |
| Source provenance verifiable | خیر | MISSING | مستقل تأیید نشده |

**وضعیت:** `GOLDEN_BLOCKED`

**دلیل:** company/report/period clues برای جست‌وجوی آینده مفیدند، اما identity رسمی، version/correction، مقدار مستقل و provenance قابل بازبینی وجود ندارد.

### 2.4 seo-codal-report (13).pdf

SHA-256 محلی ثبت‌شده و بازبینی‌شده:

`b66d4d68170a5881025fddc337b7bfdde7926e0b42f39366302a8075f6c336d4`

| Field | Value | Evidence Class | Verification Status |
|---|---|---|---|
| Official CODAL tracking ID | NOT ESTABLISHED | MISSING | تأیید نشده |
| Official URL | NOT ESTABLISHED | MISSING | تأیید نشده |
| Company | سرنخ متن PDF: صنایع مس ایران؛ نام رسمی CODAL تأیید نشده | SUPPORTING | هویت رسمی تأیید نشده |
| Report title | سرنخ متن PDF: consolidated financial statements | SUPPORTING | عنوان رسمی تأیید نشده |
| Report type | سرنخ متن PDF: consolidated statements | SUPPORTING | نوع رسمی تأیید نشده |
| Publication datetime | NOT ESTABLISHED | MISSING | تأیید نشده |
| Financial period | سرنخ تاریخ 1403/12/30 | SUPPORTING | دوره رسمی تأیید نشده |
| Version/correction/restatement status | سرنخ متن درباره تجدید ارائه/اصلاح؛ شناسه رسمی ندارد | SUPPORTING | نسخه رسمی تأیید نشده |
| PDF correspondence | اتصال به رکورد رسمی CODAL وجود ندارد | MISSING | بدون ابهام قابل اثبات نیست |
| Exact financial values available | فقط متن/خروجی implementation وجود دارد | MISSING | قابل تأیید مستقل نیست |
| NULL vs 0 verifiable | خیر | MISSING | مستقل تأیید نشده |
| Unit verifiable | خیر | MISSING | مستقل تأیید نشده |
| Currency verifiable | خیر | MISSING | مستقل تأیید نشده |
| Source provenance verifiable | خیر | MISSING | مستقل تأیید نشده |

**وضعیت:** `GOLDEN_BLOCKED`

**دلیل:** نوع گزارش، شرکت و دوره فقط supporting clue هستند. official identity، URL، ID، version/PIT و provenance مستقل وجود ندارد.

## 3. Evidence Classification

### AUTHORITATIVE

برای هیچ‌یک از چهار PDF، مدرک authoritative قابل بازبینی در repository یا artifactهای فعلی ثبت نشده است. به‌طور مشخص، هیچ‌کدام از موارد زیر موجود نیست:

- صفحه رسمی گزارش در CODAL؛
- CODAL tracking/report ID رسمی؛
- URL رسمی مرتبط با همان PDF؛
- metadata رسمی شامل title، type، company، publication datetime، period و version؛
- سند مستقل رسمی که مقدار، NULL/zero، unit، currency و محل source را تأیید کند.

### SUPPORTING

شواهد supporting موجود:

- نام شرکت قابل مشاهده در PDF؛
- عنوان یا نوع گزارش قابل مشاهده در PDF؛
- تاریخ‌ها و دوره‌های قابل مشاهده در PDF؛
- SHA-256 فایل‌های محلی؛
- embedded metadata مانند Chromium/Skia creation metadata.

این موارد می‌توانند برای کشف منبع کمک کنند، اما به‌تنهایی Golden evidence نیستند.

### INTERNAL_ONLY

موارد زیر فقط internal-only هستند و رد می‌شوند:

- filename محلی؛
- title و report_type ورودی تست؛
- `CODAL-PRODUCTION-SAMPLE-*` و سایر IDهای تولیدشده در تست؛
- `local://` و `example.invalid`؛
- publication datetime ساختگی در تست‌ها؛
- Report/ReportVersion/RawFinancialFact تولیدشده توسط application؛
- خروجی `extract_raw_lines_from_pdf()`؛
- هر مقدار استخراج‌شده یا normalized از production path؛
- fixture یا parser دوم مبتنی بر همان PDF.

### MISSING

برای هر چهار PDF، موارد زیر missing هستند:

- official tracking ID؛
- official URL؛
- official report identity؛
- publication datetime رسمی؛
- period و version/PIT رسمی؛
- تطبیق بدون ابهام PDF با گزارش رسمی؛
- exact independently verified financial values؛
- NULL versus zero؛
- unit و currency؛
- section/row/column provenance مستقل.

## 4. Independence Assessment

### استقلال از production extraction

وجود کد extraction و تست‌های deterministic فقط رفتار implementation را نشان می‌دهد. این خروجی‌ها از همان PDFهایی مشتق می‌شوند که قرار است audit شوند؛ بنابراین source of truth مستقل نیستند.

### استقلال از production persistence

Report، ReportVersion و RawFinancialFact خروجی persistence هستند. آن‌ها downstream production data هستند و نمی‌توانند expected values مستقل باشند.

### استقلال از database فعلی

هر metadata ثبت‌شده در database یا تست‌ها مانند company، period، title، date و CODAL IDهای نمونه از application/test setup آمده و authoritative CODAL evidence محسوب نمی‌شود.

### استقلال از generated fixtures

fixtureهای فعلی برای بررسی ingestion، idempotency، PIT و persistence ساخته شده‌اند. آن‌ها برای Golden Accuracy طراحی نشده‌اند و expected-value authority ندارند.

## 5. Golden Readiness

| PDF | وضعیت | دلیل اصلی |
|---|---|---|
| seo-codal-report (1).pdf | `GOLDEN_BLOCKED` | identity رسمی و exact independently verified values وجود ندارد. |
| seo-codal-report (3).pdf | `GOLDEN_BLOCKED` | official source، version/PIT و provenance مستقل وجود ندارد. |
| seo-codal-report (10).pdf | `GOLDEN_BLOCKED` | identity رسمی و مقدار مستقل، NULL/zero، unit/currency تأیید نشده‌اند. |
| seo-codal-report (13).pdf | `GOLDEN_BLOCKED` | PDF correspondence و official provenance قابل اثبات نیست. |

هیچ گزارشی `GOLDEN_READY` نیست.

## 6. Overall Status

```text
GOLDEN SOURCE STATUS: BLOCKED
```

### Evidence required to unblock

برای هر گزارش حداقل این شواهد خارجی لازم است:

1. official CODAL tracking/report ID؛
2. canonical official CODAL URL یا سند رسمی قابل بازبینی؛
3. official company، title، report type و publication datetime؛
4. financial period و version/correction/restatement metadata؛
5. مدرک اتصال unambiguous بین bytes PDF محلی و همان گزارش رسمی، ترجیحاً با hash یا download provenance؛
6. source document رسمی که raw item name و raw item code را نشان دهد؛
7. exact numeric value یا explicit NULL؛
8. unit و currency؛
9. section، row و column قابل بازسازی؛
10. مدرک مستقل برای PIT و نسخه‌ای که در cutoff مربوطه قابل دسترس بوده است.

بدون این موارد، Golden Dataset نباید ساخته شود.

## 7. Prohibited Evidence

شواهد زیر صراحتاً برای Golden construction رد شدند:

- خروجی `extract_raw_lines_from_pdf()` و هر production extractor؛
- RawFinancialFact و سایر رکوردهای production database؛
- metadata synthetic تست‌ها؛
- `local://`، `example.invalid` و generated CODAL IDs؛
- filename و local path؛
- PDF text reconstruction به‌عنوان expected source مستقل؛
- parser دوم روی همان PDF برای تولید expected values؛
- مقادیر تخمینی، حدسی، دستی یا تبدیل missing به zero؛
- توافق چند implementation داخلی بدون منبع authoritative مستقل؛
- تست سبز یا deterministic extraction به‌عنوان شواهد financial correctness.

## 8. Next-Step Gate

```text
NEXT STEP: OBTAIN/VERIFY INDEPENDENT AUTHORITATIVE SOURCE
```

تا زمانی که حداقل یک گزارش تمام الزامات identity، correspondence، value، NULL/zero، unit، currency، provenance و PIT/version را از منبع authoritative مستقل برآورده نکند، ساخت Golden Dataset و Golden Accuracy test نباید آغاز شود.

## 9. Architecture and Change Audit

این گزارش تغییری در موارد زیر ایجاد نکرده است:

- کد production؛
- acquisition یا extraction؛
- persistence؛
- database models یا migrations؛
- `DATABASE_CONTRACT_V1.3`؛
- معماری ۹ مرحله‌ای؛
- Stage 1 boundary؛
- منطق KPI، scoring، forecasting، valuation یا decision؛
- تست‌های موجود.

```text
PRODUCTION CODE CHANGED: NO
GOLDEN VALUES INVENTED: NO
TESTS WEAKENED: NO
ARCHITECTURE CHANGED: NO
DATABASE_CONTRACT_V1.3 CHANGED: NO
```
