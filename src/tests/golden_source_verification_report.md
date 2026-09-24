# Golden Source Verification Report

## 1. Scope

هدف این گزارش تعیین این است که آیا برای هر یک از ۱۹ فایل PDF موجود در پوشه `pdf/`، شواهد مستقل و authoritative کافی برای ساخت یک Golden Dataset وجود دارد یا خیر.

این مرحله فقط verification منبع و آمادگی Golden Dataset است. در این مرحله:

- هیچ مقدار مالی Golden ساخته یا رونویسی نشده است؛
- هیچ fixture، JSON، CSV یا expected-value dictionary ایجاد نشده است؛
- از production extractor، production database یا parser دوم به‌عنوان منبع حقیقت استفاده نشده است؛
- کد production، persistence، مدل‌ها، migrationها، قرارداد DATABASE_CONTRACT_V1.3 و معماری ۹ مرحله‌ای تغییر نکرده‌اند.

در بازبینی سختگیرانه فعلی، فایل‌های PDF به‌صورت کامل برای همه ۱۹ مورد بررسی شده‌اند و نتیجه یک‌دست است: هیچ‌کدام دارای source of truth مستقل و authoritative برای Golden values نیستند.

## 2. Reports Investigated

بازبینی سختگیرانه روی همه ۱۹ فایل PDF موجود در پوشه `pdf/` اجرا شد. نتیجه این است که هیچ‌کدام از این فایل‌ها، به‌صورت مستقل و authoritative، به یک source of truth رسمی برای Golden values متصل نیستند.

### 2.1 Full corpus review (19 PDFs)

| PDF | Local SHA-256 | Official CODAL ID | Official URL | Independent value evidence | Overall status |
|---|---|---|---|---|---|
| seo-codal-report (1).pdf | `2ac373cd19bcf64f95cba562a095c130def4d84a294ef3c5e39352db2efaa216` | NOT ESTABLISHED | NOT ESTABLISHED | NO | `GOLDEN_BLOCKED` |
| seo-codal-report (2).pdf | `add6d0c391c31a74944daf953251f389e67e28af4d3cb191e5810321a3a5f851` | NOT ESTABLISHED | NOT ESTABLISHED | NO | `GOLDEN_BLOCKED` |
| seo-codal-report (3).pdf | `fd043c49e04525f725fa6df6f603084566742f1a15694e0b44fea1d868257f19` | NOT ESTABLISHED | NOT ESTABLISHED | NO | `GOLDEN_BLOCKED` |
| seo-codal-report (4).pdf | `bf18b0c5749bbf0ff51b78b2d3479d61168d27d7ac7960262b5368d0de4c1001` | NOT ESTABLISHED | NOT ESTABLISHED | NO | `GOLDEN_BLOCKED` |
| seo-codal-report (6).pdf | `e244167e13a8d59394513d4236ef9a2c51e6ea4b85d52f6c1866a0a27288aaff` | NOT ESTABLISHED | NOT ESTABLISHED | NO | `GOLDEN_BLOCKED` |
| seo-codal-report (7).pdf | `a3309625b510f9dfbe4866befb8d04524d231aa8a5e1a330cc65bcfb2a125eba` | NOT ESTABLISHED | NOT ESTABLISHED | NO | `GOLDEN_BLOCKED` |
| seo-codal-report (8).pdf | `4ca9c59edf8f5ded5a458bf8356a2a5fa87d91d4964a6b8d82f9309b50375dbe` | NOT ESTABLISHED | NOT ESTABLISHED | NO | `GOLDEN_BLOCKED` |
| seo-codal-report (9).pdf | `ef5a3e8f6bc45b57cd07de674c9f65e8835607d15db7f5a8ea2806e6632a6358` | NOT ESTABLISHED | NOT ESTABLISHED | NO | `GOLDEN_BLOCKED` |
| seo-codal-report (10).pdf | `335acc828dfb1f1cb8283114388a08c3c08c2111a0035b3498d12a4e1aba35df` | NOT ESTABLISHED | NOT ESTABLISHED | NO | `GOLDEN_BLOCKED` |
| seo-codal-report (11).pdf | `552a7bf5b4a3210e38fbb74d6ca341bad3cf35142f89fa112ba7dc7c34d4a812` | NOT ESTABLISHED | NOT ESTABLISHED | NO | `GOLDEN_BLOCKED` |
| seo-codal-report (12).pdf | `33ff8ec02fc405170c14b66755a55893a5ab85273cfa99f3a694409c78505555` | NOT ESTABLISHED | NOT ESTABLISHED | NO | `GOLDEN_BLOCKED` |
| seo-codal-report (13).pdf | `b66d4d68170a5881025fddc337b7bfdde7926e0b42f39366302a8075f6c336d4` | NOT ESTABLISHED | NOT ESTABLISHED | NO | `GOLDEN_BLOCKED` |
| seo-codal-report (14).pdf | `70f5752422162e981cdc84d3f4cbfa4e834679c4f4b80a324406ac120288e928` | NOT ESTABLISHED | NOT ESTABLISHED | NO | `GOLDEN_BLOCKED` |
| seo-codal-report (15).pdf | `bd0e98d19d807b0dbea3e7ec724f0128660876e42c1ac343c09a57a2efd36fc4` | NOT ESTABLISHED | NOT ESTABLISHED | NO | `GOLDEN_BLOCKED` |
| seo-codal-report (16).pdf | `6afb76e7704b561bb2ca92c558aaf522f92168d2a18e9aadb6bfe0b88a7e6bc8` | NOT ESTABLISHED | NOT ESTABLISHED | NO | `GOLDEN_BLOCKED` |
| seo-codal-report (19).pdf | `78e6e065202617298b88b6f2cfed6edae7f5518c768fcdd5c3f97dfd48ce03f8` | NOT ESTABLISHED | NOT ESTABLISHED | NO | `GOLDEN_BLOCKED` |
| seo-codal-report (20).pdf | `be401fd3790a5b36e04fa1e548bfe4e04f846e782fc6d9c86e26a45b7feeea1d` | NOT ESTABLISHED | NOT ESTABLISHED | NO | `GOLDEN_BLOCKED` |
| seo-codal-report (25).pdf | `fb6ff6317f7f9bd2a26ff2b0e2dac571a80c077b7eab662ccb2f48353a49db32` | NOT ESTABLISHED | NOT ESTABLISHED | NO | `GOLDEN_BLOCKED` |
| seo-codal-report (26).pdf | `cc0a3c998f37ddcb4d036149b31ed5366aefab87c27e7af231255e32654e88eb` | NOT ESTABLISHED | NOT ESTABLISHED | NO | `GOLDEN_BLOCKED` |

### 2.2 Evidence threshold applied

برای هر PDF، معیارهای زیر به‌صورت سختگیرانه اعمال شده است:

- فایل محلی قابل خواندن است؛
- SHA-256 محلی محاسبه و ثبت شده است؛
- official CODAL tracking ID وجود ندارد؛
- official source URL وجود ندارد؛
- company/report title/type فقط clue-based هستند؛
- publication datetime، period و version status از منبع رسمی تأیید نشده‌اند؛
- correspondence PDF → official record توسط هیچ سند مستقل ثابت نشده است؛
- exact value، NULL/zero، unit، currency، section/row/column provenance به‌صورت مستقل مستند نشده است.

در نتیجه، ۱۹/۱۹ فایلها در وضعیت `GOLDEN_BLOCKED` باقی می‌مانند.

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
| seo-codal-report (2).pdf | `GOLDEN_BLOCKED` | official source و provenance مستقل وجود ندارد. |
| seo-codal-report (3).pdf | `GOLDEN_BLOCKED` | official source، version/PIT و provenance مستقل وجود ندارد. |
| seo-codal-report (4).pdf | `GOLDEN_BLOCKED` | correspondence PDF → report رسمی و exact values تأیید نشده‌اند. |
| seo-codal-report (6).pdf | `GOLDEN_BLOCKED` | identity رسمی و جدول مالی مستقل ثابت نشده است. |
| seo-codal-report (7).pdf | `GOLDEN_BLOCKED` | source URL، ID و exact value بدون تایید مستقل وجود ندارد. |
| seo-codal-report (8).pdf | `GOLDEN_BLOCKED` | report metadata رسمی و unit/currency مستقل تأیید نشده‌اند. |
| seo-codal-report (9).pdf | `GOLDEN_BLOCKED` | PDF-only clues و official provenance کافی نیستند. |
| seo-codal-report (10).pdf | `GOLDEN_BLOCKED` | identity رسمی و مقدار مستقل، NULL/zero، unit/currency تأیید نشده‌اند. |
| seo-codal-report (11).pdf | `GOLDEN_BLOCKED` | هیچ سند رسمی یا correspondence محکم برای PDF وجود ندارد. |
| seo-codal-report (12).pdf | `GOLDEN_BLOCKED` | source of truth مستقل برای financial period و value وجود ندارد. |
| seo-codal-report (13).pdf | `GOLDEN_BLOCKED` | PDF correspondence و official provenance قابل اثبات نیست. |
| seo-codal-report (14).pdf | `GOLDEN_BLOCKED` | exact value و provenance رسمی برای این سند در دسترس نیست. |
| seo-codal-report (15).pdf | `GOLDEN_BLOCKED` | identity، version و financial evidence رسمی هرگز بررسی نشده‌اند. |
| seo-codal-report (16).pdf | `GOLDEN_BLOCKED` | report metadata رسمی و independent expected values معتبر نیستند. |
| seo-codal-report (19).pdf | `GOLDEN_BLOCKED` | source identity و financial value به‌صورت مستقل تأیید نشده‌اند. |
| seo-codal-report (20).pdf | `GOLDEN_BLOCKED` | هیچ URL/ID/metadata رسمی برای این فایل وجود ندارد. |
| seo-codal-report (25).pdf | `GOLDEN_BLOCKED` | exact value، unit و currency از منبع مستقل قابل بازبینی نیستند. |
| seo-codal-report (26).pdf | `GOLDEN_BLOCKED` | PDF-only evidence و source provenance برای Golden construction کافی نیست. |

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
