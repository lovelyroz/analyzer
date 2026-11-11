# Saderat Fiscal-Year Periodic Financial Report Workbook Inspection — DB-STD-003

## 1. Executive summary

The current `excel/saderat_seasonal.xlsx` is an interim financial-report workbook whose filename suggests Saderat. The workbook itself does not identify the company by name; its metadata identifies a six-month report ending ۱۴۰۳/۰۶/۳۱; `Recovered_Sheet1!A262` begins the customer-deposit schedule, not a company identity field. No company name or ticker was found in the workbook content. The current-period columns are marked unaudited in the main income and cash-flow statements (`B11`, `B175`); comparative columns are marked audited. The sheet contains five main statement areas and extensive supplemental management schedules and narrative disclosures.

Flow statements show a current six-month period ending ۱۴۰۳/۰۶/۳۱, a confirmed corresponding six-month comparative ending ۱۴۰۲/۰۶/۳۱, and a confirmed prior full-year comparison ending ۱۴۰۲/۱۲/۲۹. The owner confirmed these column interpretations. The balance sheet uses point-in-time dates. The comprehensive-income area contains an application error message at A58 and lacks extractable statement values. No standalone-quarter amounts are calculated. No DB-STD-003 standard is finalized here.

## Terminology alignment with DB-STD-003

This workbook is assessed under **Fiscal-Year Periodic Financial Reports** (Persian: «گزارش‌های مالی دوره‌ای سال مالی (تجمعی)»). It is a six-month interim report ending ۱۴۰۳/۰۶/۳۱. The reporting family covers fiscal-year checkpoints such as 3, 6, 9, and 12 months; the 12-month member is the annual report, not an interim report.

“Cumulative/YTD” describes the temporal basis of applicable flow values, not every value in the workbook. Balance-sheet figures remain point-in-time balances at their stated dates. The periodic-report family classification therefore does not determine the temporal meaning of every table column.

## 2. Workbook inventory

| Property | Evidence |
|---|---|
| File and format | `excel/saderat_seasonal.xlsx`, XLSX, 35,157 bytes. |
| Worksheets | One worksheet in order: `Recovered_Sheet1`, visible. |
| Used range | `A1:L410`, 410 rows by 12 columns, with merged display regions and blank spacing. |
| Workbook metadata | Title exactly: `صورت‌های مالی میاندوره‌ای 6 ماهه منتهی به 1403/06/31`; creator `Papa`; subject empty; created/modified `2026-11-11 08:32:04`. File timestamps do not establish publication date. |
| Structural features | 99 merged ranges; no formulas, defined names, charts, images, comments, hidden rows, or hidden columns detected. |
| Workbook contents | One filing workbook with statements and supplementary management-report tables/disclosures; not separate files or report types. |

## 3. Identity and period evidence

- Company identity: the owner confirmed that the workbook belongs to Bank Saderat Iran. The name and ticker are not stated inside the workbook; company identity is supplied by the user's selection/ingestion context, not inferred from an in-workbook name.
- Current report: metadata title says six-month interim period. Current endpoint ۱۴۰۳/۰۶/۳۱ appears in `B10`, `B77`, and `B174`.
- Audit/restatement status in the main flow statements: B is unaudited and current; C and D are audited and marked restated. Other schedules may use different statuses; preserve their exact headers.
- Fiscal year: the owner confirmed the company's fiscal year begins on ۱۴۰۳/۰۱/۰۱ and ends at the end of Esfand; the prior fiscal year ended on ۱۴۰۲/۱۲/۲۹. The report's exact Jalali dates remain authoritative for each period.
- Comparative dates: flow headers `C10`/`C174` end ۱۴۰۲/۰۶/۳۱; D headers `D10`/`D174` end ۱۴۰۲/۱۲/۲۹. Balance sheet dates are in `B77:D77`: current date, restated year-end, and restated opening date. All dates are retained as presented.
- No ticker or publication date appears in the inspected workbook metadata or visible sheet.

## 4. Financial statements and major tables

| Worksheet range | Table / evidence | Structure, unit and data character |
|---|---|---|
| `A3:E48` | Income statement (`A3`, `A8`) | Headers `A10:E11`; rows 12:42; explanatory blocks at 44, 46, 48. Million rials (`A9`); EPS rows use rials. Flows, subtotals, EPS/derived values, capital. |
| `A53:E69` | Comprehensive income title at `A53` | `A58` contains an application error message; unit note A60 and other-info labels A64:A65 appear, but no usable numeric statement is exposed. Do not treat as zero. |
| `A70:E117` | Financial position (`A70`, `A75`) | Headers 77:78; balance lines 79:117; million rials (`A76`); point-in-time balances and percentage-change column. |
| `A121:L163` | Changes in equity (`A121`, `A126`) | Unit A127; component headers A128:L128; dated opening/restatement/prior-year/current movement rows 129:163; million rials. |
| `A167:E233` | Cash flows (`A167`, `A172`) | Headers 174:175; cash-flow rows 176:211; explanatory blocks from 219 onward. Million rials (`A173`); current/comparative period flows and percentage change. |
| `A228:K252` | Management summary and loans/allowance schedule | Intro/limitation at A228/A233; schedule title A234, unit A235, headers A236:A237; credit-quality categories and allowance calculations through row 252. Amounts million rials; rates are percentages. |
| `A253:I260` | Management estimates | Loan-rate, loan-balance, doubtful-receivable reserve estimates; forecast period/narrative at rows 254, 257, 260. Descriptive outlook, not realized amounts. |
| `A262:F274` | Customer-deposit status | Unit A263; multi-level headers 264:265; deposit categories and totals 266:274. D/E average rates; F forecast narrative. Balances dated ۱۴۰۲/۱۲/۲۹ and ۱۴۰۳/۰۶/۳۱. |
| `A275:F281` | Off-balance-sheet items | Unit A276; paired customer/bank obligations and managed funds by dates in row 277. Descriptive categories with monetary point-in-time values. |
| `A282:I283` | Significant changes / forward-looking caveat | Heading A282 and cautionary text A283. Narrative. |
| `A287:K292` | Management interpretive-report summary, page 2 | Page heading A287; limitation text A292. |
| `A293:D297` | Branch and employee status | Headers A295:D295; counts, historical/current/forecast dates; quantities, not money. |
| `A298:D306` | Agency fee and capital adequacy | Headers row 300; income/fee amounts, rates, capital-adequacy ratio and forecast narratives. Mixed measures. |
| `A307:F331` | Strategy and facility/deposit income | Headers row 311; annual and six-month income by product, average rates, forecast text; explanation A331. Money in million rials; rates in percent. |
| `A332:D339` | Investment profit/loss | Header row 334; investment income, sale gain/loss, impairment adjustment, total and outlook. |
| `A343:J356` | Investee companies | Headers rows 351:352; ownership, cost, investee fiscal-year end, income and outlook narrative. Mixed stocks, flows, ratios and descriptive data. |
| `A357:C372` | Other operating income/expenses | Date headers row 359; detailed income/costs, totals and estimate at 371:372. |
| `A374:C381` | Net other income/expenses | Header row 376; comparison, total and forecast text. |
| `A383:C390` | Administrative/general expense | Header row 385; expense/total and outlook. |
| `A392:C400` | Financial expense | Header row 394; expense categories/total and outlook. |
| `A402:E404` | Profit distribution plan | Header row 403; prior-year retained earnings, dividends and net profit, proposed current distribution percentage. |
| `A405:B406` | Other significant plans | Forecast period and narrative plan. |
| `A408:I410` | Other significant explanations | Narrative and forward-looking caution text. |

## 5. Complete source Header inventory

Appendix A inventories every nonempty string-valued cell in the sheet, with source address and a readable contextual classification. It includes exact Persian wording for headers, row labels, units, titles and narrative/descriptive cells; numeric cells are not included. This broad inventory avoids silently omitting candidate headers in the supplemental pages. Text in merged cells is recorded at its stored anchor cell.

## 6. Temporal classification matrix

| Source header / address | Classification | Evidence and status |
|---|---|---|
| `B10` and `B174`, ending ۱۴۰۳/۰۶/۳۱ | Current six-month flow | Six-month metadata title and current equity movement schedule. Current columns are marked unaudited in rows 11 and 175. |
| `C10` and `C174`, ending ۱۴۰۲/۰۶/۳۱ | Corresponding six-month comparative flow | Confirmed by owner; marked audited and restated. |
| `D10` and `D174`, ending ۱۴۰۲/۱۲/۲۹ | Prior full-year flow | Confirmed by owner; marked audited and restated. |
| `B77:D77` | Point-in-time balances | Explicit current, restated year-end, and restated opening dates. |
| `E10`, `E77`, `E174` | Percentage change / derived measure | Main statement E values generally match B-versus-C percentage changes; not monetary. |
| `A129`, `A132`; `A149`; `A150:A163` | Equity opening stock, restatement, movements, current closing stock | Dates and movement labels are row-based; the fiscal-year convention was confirmed by the owner. |
| `B208:D210` | Opening cash, net cash change, closing cash | Each column reconciles arithmetically; cross-check details below. |
| Schedules with headers such as row 264, 277, 295, 300, 311, 334, 351, 359, 376, 385, 394 and 403 | Mixed: historical annual, current six-month, dated balance, forecast, rate, count, or narrative | Interpret each header independently; Appendix A preserves exact wording. Do not apply a single temporal meaning to all columns. |

Cash reconciliation: B opening 810,361,408 plus change -37,741,397 equals closing 772,620,011; these match balance-sheet C80 and B80 respectively. C opening 348,012,225 plus change -20,215,766 equals 327,796,459; opening matches balance D80. D opening 348,012,225 plus change 462,349,183 equals closing 810,361,408; these match balance D80 and C80. This supports D as a full prior-year flow; C as a corresponding six-month period remains inferred because its closing balance is not a separate financial-position column.

Every numeric E percentage in the core statements was checked against rounded `(B-C)/abs(C)*100` for nonzero C; populated values match. Examples: income row 13 gives 56%; balance row 80 gives -5%; cash row 207 gives -87%. Some E cells are blank when C is zero. In other supplemental tables, percentage columns may instead be rates or ownership shares, as their exact headers specify.

No standalone-quarter value is calculated. The main statements provide six-month values and comparisons, not a separately labeled three-month column.

## 7. Financial nature and row hierarchy

- Income statement rows 13:34 contain revenue, expense, operating/nonoperating result, taxes and net results; rows 36:41 present overlapping per-share measures; row 42 is capital. Treat intermediate sums and final results as totals, not additional components.
- Financial position rows 80:117 contain point-in-time assets, equity and liabilities. Totals aggregate component rows.
- Equity schedule columns B:K are equity components; L is total. Opening, corrections, prior-year/current movements and closing balances form a roll-forward. Do not double count total L or movement rows as independent income.
- Cash-flow rows 177:210 contain operating, investing and financing flows plus cash reconciliation. Subtotals A179, A187:A188, A206:A207 aggregate lower-level flows.
- The income summary row 13 is supported by detailed facility/deposit/debt-security income at rows 309:330; row 19 investment result has further details at 332:338 and investee data at 349:356. These may overlap and need reconciliation before aggregation.
- Customer-deposit totals at rows 270, 272, 274 aggregate categories. Rates and balances are separate measures.
- Credit-risk schedule rows 238:252 contains exposure by status, collateral, reserve bases, rates and specific/general allowances. These are related but distinct measures; rates are not amounts.
- Supplemental schedules include nonfinancial counts (branches/workers), ratios, forecasts and narrative disclosures. Do not convert narrative forecasts into numeric metrics.
- The comprehensive-income system error at A58 is a technical limitation, not a zero or an absent economic item.

## 8. Remaining ambiguities requiring clarification

The owner has confirmed the company identity (Bank Saderat Iran), fiscal-year start (۱۴۰۳/۰۱/۰۱; year-end at the end of Esfand), and the temporal meaning of columns B, C, and D in the main flow statements. These items are resolved and are not open questions.

3. Recover the comprehensive-income table from the original filing or source export; A58 currently shows a system error.
4. Explain why comparative amounts are marked restated and provide the absent explanation text in the merged reason-for-change blocks.
5. Confirm forecast-period semantics: estimates include six-month periods ending . Preserve those source dates; do not infer whether they indicate a second-half forecast or a full-year horizon.
6. Confirm intended parent-child mapping for multi-tier loan/allowance, deposit, investee, and off-balance-sheet tables.
7. Keep money, EPS, rates, ratios, counts and narrative as separate measurement types; units are not uniform across all schedules.
8. Confirm whether management interpretive-report summaries are in scope for DB-STD-003 as supplementary disclosures within the same report.

## 9. Recommended next inspection step

Compare this workbook with the original published filing/export, especially the comprehensive-income error area, the reason/support for the restated comparative columns, and multi-tier supplementary tables. The owner confirmations for fiscal-year start and the meanings of columns B/C/D are complete; use them as fixed sample facts when drafting the temporal mapping. This is evidence for review and does not declare DB-STD-003 complete.

## Appendix A. Complete source string-cell inventory


**Inventory count: 447 populated text cells.** All stored textual content is listed, including exact Persian labels, explanatory narratives, and forecast language; numeric cells are excluded. This is intentionally broader than labels alone.
| Cell | Contextual classification | Exact source text |
|---|---|---|
| `A3` | Statement or table title | `صورت سود و زیان` |
| `A8` | Statement or table title | `صورت سود و زیان` |
| `A9` | Unit note | `کلیه مبالغ درج شده به میلیون ریال می باشد` |
| `A10` | Column header or subheader | `شرح` |
| `B10` | Column header or subheader | `دوره منتهي به ۱۴۰۳/۰۶/۳۱` |
| `C10` | Column header or subheader | `تجدید ارائه شده ۱۴۰۲/۰۶/۳۱` |
| `D10` | Column header or subheader | `تجدید ارائه شده ۱۴۰۲/۱۲/۲۹` |
| `E10` | Column header or subheader | `درصد تغييرات` |
| `B11` | Column header or subheader | `حسابرسی نشده` |
| `C11` | Column header or subheader | `حسابرسی شده` |
| `D11` | Column header or subheader | `حسابرسی شده` |
| `A12` | Row label or section heading | `عملیات در حال تداوم: ` |
| `A13` | Row label or section heading | `درآمد تسهيلات اعطايي و سپرده گذاری و اوراق بدهی ` |
| `A14` | Row label or section heading | `هزينه سود سپرده‌ها ` |
| `A15` | Row label or section heading | `خالص درآمد تسهیلات و سپرده گذاری ` |
| `A16` | Row label or section heading | `درآمد کارمزد ` |
| `A17` | Row label or section heading | `هزينه کارمزد ` |
| `A18` | Row label or section heading | `خالص درآمد کارمزد ` |
| `A19` | Row label or section heading | `خالص سود (زیان) سرمایه گذاری‌ها ` |
| `A20` | Row label or section heading | `خالص سود (زيان) مبادلات و معاملات ارزي ` |
| `A21` | Row label or section heading | `ساير درآمدها و هزینه های عملياتي ` |
| `A22` | Row label or section heading | `جمع درآمدهاي عملياتي ` |
| `A23` | Row label or section heading | `خالص ساير درآمدها و هزینه‌ها ` |
| `A24` | Row label or section heading | `هزينه‌هاي اداري و عمومي ` |
| `A25` | Row label or section heading | `هزينه مطالبات مشکوک الوصول ` |
| `A26` | Row label or section heading | `هزينه‌هاي مالي ` |
| `A27` | Row label or section heading | `هزينه استهلاک ` |
| `A28` | Row label or section heading | `سود(زیان) عملیات در حال تداوم قبل از مالیات ` |
| `A29` | Row label or section heading | `ماليات بر درآمد سال جاری ` |
| `A30` | Row label or section heading | `ماليات بر درآمد سال های قبل ` |
| `A31` | Row label or section heading | `سود (زيان) خالص عملیات در حال تداوم ` |
| `A32` | Row label or section heading | `عملیات متوقف شده: ` |
| `A33` | Row label or section heading | `سود(زیان) خالص عملیات متوقف شده ` |
| `A34` | Row label or section heading | `سود(زیان) خالص ` |
| `A35` | Row label or section heading | `سود (زیان)پایه هر سهم (ريال) ` |
| `A36` | Row label or section heading | `عملياتي (ريال) ` |
| `A37` | Row label or section heading | `غيرعملياتي(ريال) ` |
| `A38` | Row label or section heading | `ناشی از عملیات در حال تداوم(ریال) ` |
| `A39` | Row label or section heading | `ناشي از عمليات متوقف شده(ريال) ` |
| `A40` | Row label or section heading | `سود(زیان) پایه هر سهم (ریال) ` |
| `A41` | Row label or section heading | `سود (زیان) خالص هر سهم– ریال ` |
| `A42` | Row label or section heading | `سرمایه ` |
| `A44` | Row label or section heading | `دلایل تغییرات اطلاعات واقعی دوره منتهی به ۱۴۰۳/۰۶/۳۱ ` |
| `A46` | Row label or section heading | `دلایل تغییرات اطلاعات واقعی دوره منتهی به ۱۴۰۲/۰۶/۳۱ ` |
| `A48` | Row label or section heading | `دلایل تغییرات اطلاعات واقعی دوره منتهی به ۱۴۰۲/۱۲/۲۹ ` |
| `A53` | Statement or table title | `صورت سود و زیان جامع` |
| `A58` | Row label or section heading | `عملیات با اشکال مواجه گردید. لطفا مدیر سیستم را در جریان قرار دهید` |
| `A60` | Unit note | `کلیه مبالغ درج شده به میلیون ریال می باشد` |
| `A64` | Row label or section heading | `سایر اطلاعات:` |
| `A65` | Row label or section heading | `lblCoverText` |
| `A70` | Statement or table title | `صورت وضعیت مالی` |
| `A75` | Statement or table title | `صورت وضعیت مالی` |
| `A76` | Unit note | `کلیه مبالغ درج شده به میلیون ریال می باشد` |
| `A77` | Column header or subheader | `شرح` |
| `B77` | Column header or subheader | `دوره منتهي به ۱۴۰۳/۰۶/۳۱` |
| `C77` | Column header or subheader | `تجدید ارائه شده ۱۴۰۲/۱۲/۲۹` |
| `D77` | Column header or subheader | `تجدید ارائه شده ۱۴۰۲/۰۱/۰۱` |
| `E77` | Column header or subheader | `درصد تغييرات` |
| `B78` | Column header or subheader | `حسابرسی نشده` |
| `C78` | Column header or subheader | `حسابرسی شده` |
| `D78` | Column header or subheader | `حسابرسی نشده` |
| `A79` | Row label or section heading | `دارایی ها ` |
| `A80` | Row label or section heading | `موجودي نقد ` |
| `A81` | Row label or section heading | `مطالبات از بانک ها و ساير موسسات اعتباري ` |
| `A82` | Row label or section heading | `مطالبات از دولت ` |
| `A83` | Row label or section heading | `تسهيلات اعطايي و مطالبات از اشخاص دولتي ` |
| `A84` | Row label or section heading | `تسهيلات اعطايي و مطالبات از اشخاص غير دولتي ` |
| `A85` | Row label or section heading | `سرمایه‌گذاری در سهام و ساير اوراق بهادار ` |
| `A86` | Row label or section heading | `مطالبات از شرکت‌های فرعی و وابسته ` |
| `A87` | Row label or section heading | `ساير حسابهاي دريافتني ` |
| `A88` | Row label or section heading | `دارایی‌هاي ثابت مشهود ` |
| `A89` | Row label or section heading | `دارایی‌هاي نا مشهود ` |
| `A90` | Row label or section heading | `سپرده قانونی ` |
| `A91` | Row label or section heading | `ساير دارایی‌ها ` |
| `A92` | Row label or section heading | `جمع دارایی‌ها ` |
| `A93` | Column header or subheader | `حقوق مالکانه و بدهی‌ها ` |
| `B93` | Column header or subheader | `دوره منتهی به ۱۴۰۳/۰۶/۳۱ ` |
| `C93` | Column header or subheader | `تجدید ارائه شده ۱۴۰۲/۱۲/۲۹ ` |
| `D93` | Column header or subheader | `تجدید ارائه شده۱۴۰۲/۰۱/۰۱ ` |
| `E93` | Column header or subheader | `درصد تغييرات ` |
| `A94` | Row label or section heading | `حقوق مالکانه ` |
| `A95` | Row label or section heading | `سرمايه ` |
| `A96` | Row label or section heading | `افزايش سرمايه در جريان ` |
| `A97` | Row label or section heading | `صرف سهام ` |
| `A98` | Row label or section heading | `اندوخته صرف سهام ` |
| `A99` | Row label or section heading | `اندوخته قانوني ` |
| `A100` | Row label or section heading | `ساير اندوخته‌ها ` |
| `A101` | Row label or section heading | `مازاد تجديد ارزيابي دارايي‌ها ` |
| `A102` | Row label or section heading | `تفاوت تسعیر ارز ` |
| `A103` | Row label or section heading | `سود (زيان) انباشته ` |
| `A104` | Row label or section heading | `سهام خزانه ` |
| `A105` | Row label or section heading | `جمع حقوق مالکانه ` |
| `A106` | Row label or section heading | `بدهی‌ها ` |
| `A107` | Row label or section heading | `بدهي به بانكها و ساير موسسات اعتباري ` |
| `A108` | Row label or section heading | `سپرده‌هاي مشتریان ` |
| `A109` | Row label or section heading | `سود سهام پرداختني ` |
| `A110` | Row label or section heading | `اوراق بدهی ` |
| `A111` | Row label or section heading | `ذخيره ماليات عملکرد ` |
| `A112` | Row label or section heading | `ذخاير و ساير بدهی‌ها ` |
| `A113` | Row label or section heading | `ذخيره مزاياي پايان خدمت و تعهدات بازنشستگی کارکنان ` |
| `A114` | Row label or section heading | `جمع بدهی های قبل از حقوق صاحبان سپرده های سرمایه گذاری ` |
| `A115` | Row label or section heading | `حقوق صاحبان سپرده‌های سرمایه‌گذاری ` |
| `A116` | Row label or section heading | `جمع بدهی‌ها ` |
| `A117` | Row label or section heading | `جمع بدهی‌ها و حقوق مالکانه ` |
| `A121` | Statement or table title | `صورت تغییرات در حقوق مالکانه` |
| `A126` | Statement or table title | `صورت تغییرات در حقوق مالکانه` |
| `A127` | Unit note | `کلیه مبالغ درج شده به میلیون ریال می باشد` |
| `A128` | Column header or subheader | `شرح` |
| `B128` | Column header or subheader | `سرمایه` |
| `C128` | Column header or subheader | `افزایش سرمایه در جریان` |
| `D128` | Column header or subheader | `صرف سهام` |
| `E128` | Column header or subheader | `صرف سهام خزانه` |
| `F128` | Column header or subheader | `اندوخته قانونی` |
| `G128` | Column header or subheader | `سایر اندوخته‌ها` |
| `H128` | Column header or subheader | `مازاد تجدید ارزیابی دارایی‌ها` |
| `I128` | Column header or subheader | `تفاوت تسعیر ارز عملیات خارجی` |
| `J128` | Column header or subheader | `سود انباشته` |
| `K128` | Column header or subheader | `سهام خزانه` |
| `L128` | Column header or subheader | `جمع کل` |
| `A129` | Row label or section heading | `مانده در ۱۴۰۲/۰۱/۰۱ ` |
| `A130` | Row label or section heading | `اصلاح اشتباهات ` |
| `A131` | Row label or section heading | `تغییر در رویه‌های حسابداری ` |
| `A132` | Row label or section heading | `مانده تجدید ارائه شده در ۱۴۰۲/۰۱/۰۱ ` |
| `A133` | Row label or section heading | `تغییرات حقوق مالکانه در سال ۱۴۰۲/۱۲/۲۹ ` |
| `A134` | Row label or section heading | `سود(زيان) خالص گزارش شده در صورت‌هاي مالي سال ۱۴۰۲/۱۲/۲۹ ` |
| `A135` | Row label or section heading | `اصلاح اشتباهات ` |
| `A136` | Row label or section heading | `تغییر در رویه‌های حسابداری ` |
| `A137` | Row label or section heading | `سود خالص تجدید ارائه شده سال ۱۴۰۲/۱۲/۲۹ ` |
| `A138` | Row label or section heading | `سایر اقلام سود و زیان جامع پس از کسر مالیات ` |
| `A139` | Row label or section heading | `سود(زيان) جامع سال ۱۴۰۲/۱۲/۲۹ ` |
| `A140` | Row label or section heading | `سود سهام مصوب ` |
| `A141` | Row label or section heading | `افزایش سرمایه ` |
| `A142` | Row label or section heading | `افزایش سرمایه در جریان ` |
| `A143` | Row label or section heading | `خرید سهام خزانه ` |
| `A144` | Row label or section heading | `فروش سهام خزانه ` |
| `A145` | Row label or section heading | `سود (زیان) حاصل از فروش سهام خزانه ` |
| `A146` | Row label or section heading | `انتقال از سایر اقلام حقوق مالکانه به سود و زیان انباشته ` |
| `A147` | Row label or section heading | `تخصیص به اندوخته قانونی ` |
| `A148` | Row label or section heading | `تخصیص به سایر اندوخته‌ها ` |
| `A149` | Row label or section heading | `مانده تجدید ارائه شده در ۱۴۰۲/۱۲/۲۹ ` |
| `A150` | Row label or section heading | `تغییرات حقوق مالکانه در سال ۱۴۰۳/۰۶/۳۱ ` |
| `A151` | Row label or section heading | `سود خالص ۱۴۰۳/۰۶/۳۱ ` |
| `A152` | Row label or section heading | `سایر اقلام سود و زیان جامع پس از کسر مالیات ` |
| `A153` | Row label or section heading | `سود(زيان) جامع در ۱۴۰۳/۰۶/۳۱ ` |
| `A154` | Row label or section heading | `سود(زيان) سهام مصوب ` |
| `A155` | Row label or section heading | `افزایش سرمایه ` |
| `A156` | Row label or section heading | `افزایش سرمایه در جریان ` |
| `A157` | Row label or section heading | `خرید سهام خزانه ` |
| `A158` | Row label or section heading | `فروش سهام خزانه ` |
| `A159` | Row label or section heading | `سود (زیان) حاصل از فروش سهام خزانه ` |
| `A160` | Row label or section heading | `انتقال از سایر اقلام حقوق مالکانه به سود و زیان انباشته ` |
| `A161` | Row label or section heading | `تخصیص به اندوخته قانونی ` |
| `A162` | Row label or section heading | `تخصیص به سایر اندوخته‌ها ` |
| `A163` | Row label or section heading | `مانده در ۱۴۰۳/۰۶/۳۱ ` |
| `A167` | Statement or table title | `صورت جریان های نقدی` |
| `A172` | Statement or table title | `صورت جریان های نقدی` |
| `A173` | Unit note | `کلیه مبالغ به میلیون ریال است` |
| `A174` | Column header or subheader | `شرح` |
| `B174` | Column header or subheader | `دوره منتهي به ۱۴۰۳/۰۶/۳۱` |
| `C174` | Column header or subheader | `تجدید ارائه شده۱۴۰۲/۰۶/۳۱` |
| `D174` | Column header or subheader | `تجدید ارائه شده۱۴۰۲/۱۲/۲۹` |
| `E174` | Column header or subheader | `درصد تغییر` |
| `B175` | Column header or subheader | `حسابرسی نشده` |
| `C175` | Column header or subheader | `حسابرسی شده` |
| `D175` | Column header or subheader | `حسابرسی شده` |
| `A176` | Row label or section heading | `جریان­های نقدی حاصل از فعاليت‌هاي عملياتي: ` |
| `A177` | Row label or section heading | `نقد حاصل از عملیات ` |
| `A178` | Row label or section heading | `پرداخت‌های نقدی بابت مالیات بر درآمد ` |
| `A179` | Row label or section heading | `جريان ‌خالص ‌ورود‌ (خروج) ‌نقد حاصل از فعاليت‌هاي ‌عملياتي ` |
| `A180` | Row label or section heading | `فعاليت‌هاي سرمایه‌گذاری ` |
| `A181` | Row label or section heading | `وجوه پرداختي بابت تحصیل دارایی‌هاي ثابت مشهود ` |
| `A182` | Row label or section heading | `وجوه دریافتی بابت فروش دارایی‌هاي ثابت مشهود ` |
| `A183` | Row label or section heading | `وجوه پرداختي بابت تحصیل دارایی‌هاي نامشهود ` |
| `A184` | Row label or section heading | `وجوه دریافتی بابت فروش دارایی‌هاي نامشهود ` |
| `A185` | Row label or section heading | `وجوه پرداختي بابت تحصیل املاک و مستغلات غیر عملیاتی ` |
| `A186` | Row label or section heading | `وجوه دریافتی بابت فروش املاک و مستغلات غیر عملیاتی ` |
| `A187` | Row label or section heading | `جريان خالص ورود (خروج) وجه نقد ناشی از فعاليت‌هاي سرمایه‌گذاری ` |
| `A188` | Row label or section heading | `جريان خالص ورود (خروج) وجه نقد قبل از فعالیت‌های تامین مالی ` |
| `A189` | Row label or section heading | `فعاليت‌هاي تأمين مالي ` |
| `A190` | Row label or section heading | `دریافت‌های نقدی حاصل از افزايش سرمايه ` |
| `A191` | Row label or section heading | `دریافت‌های نقدی حاصل از صرف سهام ` |
| `A192` | Row label or section heading | `دریافت‌های نقدی حاصل از فروش سهام خزانه ` |
| `A193` | Row label or section heading | `پرداخت‌های نقدی برای خرید سهام خزانه ` |
| `A194` | Row label or section heading | `دریافت‌های نقدی حاصل از تسهيلات ` |
| `A195` | Row label or section heading | `پرداخت‌های نقدی بابت اصل تسهيلات ` |
| `A196` | Row label or section heading | `پرداخت‌های نقدی بابت سود تسهيلات ` |
| `A197` | Row label or section heading | `دریافت‌های نقدی حاصل از انتشار اوراق مشارکت ` |
| `A198` | Row label or section heading | `پرداخت‌های نقدی بابت اصل اوراق مشارکت ` |
| `A199` | Row label or section heading | `پرداخت‌های نقدی بابت سود اوراق مشارکت ` |
| `A200` | Row label or section heading | `دریافت‌های نقدی حاصل از انتشار اوراق خرید دین ` |
| `A201` | Row label or section heading | `پرداخت‌های نقدی بابت اصل اوراق خرید دین ` |
| `A202` | Row label or section heading | `پرداخت‌های نقدی بابت سود اوراق خرید دین ` |
| `A203` | Row label or section heading | `پرداخت‌های نقدی بابت اصل اقساط اجاره سرمایه‌ای ` |
| `A204` | Row label or section heading | `پرداخت‌های نقدی بابت سود اجاره سرمایه‌ای ` |
| `A205` | Row label or section heading | `پرداخت‌های نقدی بابت سود سهام ` |
| `A206` | Row label or section heading | `جريان خالص ورود (خروج) نقد حاصل از فعاليت‌هاي تامين مالي ` |
| `A207` | Row label or section heading | `خالص افزايش (کاهش) در موجودی نقد ` |
| `A208` | Row label or section heading | `مانده موجودی نقد در ابتدای سال ` |
| `A209` | Row label or section heading | `تاثير تغييرات نرخ ارز ` |
| `A210` | Row label or section heading | `مانده موجودی نقد در پايان سال ` |
| `A211` | Row label or section heading | `معاملات غيرنقدي ` |
| `A219` | Row label or section heading | `دلایل تغییرات اطلاعات واقعی دوره منتهی به ۱۴۰۳/۰۶/۳۱ ` |
| `A221` | Row label or section heading | `دلایل تغییرات اطلاعات واقعی دوره منتهی به ۱۴۰۲/۰۶/۳۱ ` |
| `A223` | Row label or section heading | `دلایل تغییرات اطلاعات واقعی دوره منتهی به ۱۴۰۲/۱۲/۲۹ ` |
| `A228` | Statement or table title | `خلاصه اطلاعات گزارش تفسیری - صفحه 1` |
| `A233` | Row label or section heading | `اطلاعات این فرم گزیده ای از اطلاعات گزارش تفسیری مدیریت می باشد که هیئت مدیره شرکت مطابق با مفاد دستورالعمل اجرایی افشای اطلاعات شرکتهای ثبت شده نزد سازمان موظف به ارائه آن در پیوست این اطلاعیه می باشد و این اطلاعات جایگزین گزارش مذکور نیست. ` |
| `A234` | Statement or table title | `مانده تسهیلات اعطایی و ذخیره مطالبات مشکوک الوصول:` |
| `A235` | Unit note | `کلیه مبالغ درج شده به میلیون ریال می باشد` |
| `A236` | Column header or subheader | `شرح` |
| `B236` | Column header or subheader | `در تاریخ ۱۴۰۲/۱۲/۲۹` |
| `C236` | Column header or subheader | `در تاریخ ۱۴۰۳/۰۶/۳۱` |
| `D236` | Column header or subheader | `در تاریخ ۱۴۰۲/۱۲/۲۹` |
| `E236` | Column header or subheader | `در تاریخ ۱۴۰۳/۰۶/۳۱` |
| `F236` | Column header or subheader | `در تاریخ ۱۴۰۲/۱۲/۲۹` |
| `G236` | Column header or subheader | `در تاریخ ۱۴۰۳/۰۶/۳۱` |
| `H236` | Column header or subheader | `در تاریخ ۱۴۰۲/۱۲/۲۹` |
| `I236` | Column header or subheader | `در تاریخ ۱۴۰۳/۰۶/۳۱` |
| `J236` | Column header or subheader | `در تاریخ ۱۴۰۲/۱۲/۲۹` |
| `K236` | Column header or subheader | `در تاریخ ۱۴۰۳/۰۶/۳۱` |
| `B237` | Column header or subheader | `جاری` |
| `D237` | Column header or subheader | `سررسید گذشته` |
| `F237` | Column header or subheader | `معوق` |
| `H237` | Column header or subheader | `مشکوک الوصول` |
| `J237` | Column header or subheader | `جمع` |
| `A238` | Row label or section heading | `تسهیلات اعطایی و مطالبات از اشخاص دولتی ` |
| `A239` | Row label or section heading | `تسهیلات اعطایی و مطالبات از اشخاص غیر دولتی- ریالی ` |
| `A240` | Row label or section heading | `تسهیلات اعطایی و مطالبات از اشخاص غیر دولتی- ارزی ` |
| `A241` | Row label or section heading | `جمع ` |
| `A242` | Row label or section heading | `کسر می شود: ` |
| `A243` | Row label or section heading | `سود سالهای آتی ` |
| `A244` | Row label or section heading | `سایر ` |
| `A245` | Row label or section heading | `مانده تسهیلات پایان دوره ` |
| `A246` | Row label or section heading | `ارزش وثایق دریافتی ` |
| `A247` | Row label or section heading | `مانده مبنای محاسبه ذخیره اختصاصی ` |
| `A248` | Row label or section heading | `ضریب مبنای احتساب ذخیره اختصاصی (درصد) ` |
| `A249` | Row label or section heading | `ذخیره اختصاصی مطالبات مشکوک الوصول ` |
| `A250` | Row label or section heading | `مانده مبنای محاسبه ذخیره عمومی ` |
| `A251` | Row label or section heading | `ذخیره عمومی مطالبات مشکوک الوصول ` |
| `A252` | Row label or section heading | `جمع ` |
| `A253` | Row label or section heading | `برآورد شرکت از تغییرات در نرخ سود تسهیلات اعطایی :` |
| `A254` | Row label or section heading | `دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ` |
| `C254` | Descriptive, forecast, or explanatory text | `تغییر نرخ سود تسهیلات بر اساس مصوبات شورای پول و اعتبار و بخشنامه های بانک مرکزی ج.ا.ا صورت می پذیرد. ` |
| `A256` | Row label or section heading | `برآورد شرکت از تغییرات در مانده تسهیلات :` |
| `A257` | Row label or section heading | `دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ` |
| `C257` | Descriptive, forecast, or explanatory text | `از آنجا که عزم مدیریت بانک بر دست یابی به سود عملیاتی و سود خالص می باشد، در نتیجه افزایش پرداخت تسهیلات و بهبود پرتفوی تسهیلاتی در دستور کار قرار دارد. آمار تسهیلات پرداختی نیز موید این رویکرد می باشد. ` |
| `A259` | Row label or section heading | `برآورد شرکت از تغییرات در مانده ذخایر مطالبات مشکوک الوصول :` |
| `A260` | Row label or section heading | `دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ` |
| `C260` | Descriptive, forecast, or explanatory text | `هدف مدیریت بانک در این خصوص کاهش مطالبات غیر جاری می باشد ` |
| `A262` | Row label or section heading | `مانده سپرده های دریافتی از مشتریان :` |
| `A263` | Unit note | `کلیه مبالغ درج شده به میلیون ریال می باشد` |
| `A264` | Column header or subheader | `شرح` |
| `B264` | Column header or subheader | `مانده سپرده ها` |
| `D264` | Column header or subheader | `متوسط نرخ سود مانده سپرده ها` |
| `F264` | Column header or subheader | `برآورد مدیریت از تغییر در نرخ سود سپرده ها و تغییر در مانده سپرده های دریافتی از مشتریان` |
| `B265` | Column header or subheader | `در تاریخ ۱۴۰۲/۱۲/۲۹` |
| `C265` | Column header or subheader | `در تاریخ ۱۴۰۳/۰۶/۳۱` |
| `D265` | Column header or subheader | `در تاریخ ۱۴۰۲/۱۲/۲۹` |
| `E265` | Column header or subheader | `در تاریخ ۱۴۰۳/۰۶/۳۱` |
| `A266` | Row label or section heading | `سپرده های ریالی: ` |
| `A267` | Row label or section heading | `سپرده های کوتاه مدت ` |
| `F267` | Descriptive, forecast, or explanatory text | `تغییر نرخ سپرده ها تابع سیاست های بانک مرکزی می باشد ` |
| `A268` | Row label or section heading | `سپرده های کوتاه مدت ویژه ` |
| `F268` | Descriptive, forecast, or explanatory text | `تغییر نرخ سپرده ها تابع سیاست های بانک مرکزی می باشد ` |
| `A269` | Row label or section heading | `سپرده های بلند مدت ` |
| `F269` | Descriptive, forecast, or explanatory text | `تغییر نرخ سپرده ها تابع سیاست های بانک مرکزی می باشد ` |
| `A270` | Row label or section heading | `جمع سپرده های هزینه زا ` |
| `A271` | Row label or section heading | `سپرده های غیر هزینه زا ` |
| `A272` | Row label or section heading | `جمع سپرده های ریالی ` |
| `A273` | Row label or section heading | `سپرده های ارزی ` |
| `F273` | Descriptive, forecast, or explanatory text | `تغییر نرخ سپرده ها تابع سیاست های بانک مرکزی می باشد ` |
| `A274` | Row label or section heading | `جمع سپرده های دریافتی ` |
| `A275` | Row label or section heading | `اقلام زیر خط:` |
| `A276` | Unit note | `کلیه مبالغ درج شده به میلیون ریال می باشد` |
| `A277` | Column header or subheader | `شرح` |
| `B277` | Column header or subheader | `۱۴۰۳/۰۶/۳۱` |
| `C277` | Column header or subheader | `۱۴۰۲/۱۲/۲۹` |
| `D277` | Column header or subheader | `شرح` |
| `E277` | Column header or subheader | `۱۴۰۳/۰۶/۳۱` |
| `F277` | Column header or subheader | `۱۴۰۲/۱۲/۲۹` |
| `A278` | Row label or section heading | `تعهدات مشتریان بابت اعتبارات اسنادی ` |
| `D278` | Descriptive, forecast, or explanatory text | `تعهدات بانک بابت اعتبارات اسنادی ` |
| `A279` | Row label or section heading | `تعهدات مشتریان بابت ضمانت نامه های صادره ` |
| `D279` | Descriptive, forecast, or explanatory text | `تعهدات بانک بابت ضمانت نامه های صادره ` |
| `A280` | Row label or section heading | `ساير تعهدات مشتريان بانک ` |
| `D280` | Descriptive, forecast, or explanatory text | `سایر تعهدات بانک ` |
| `A281` | Row label or section heading | `وجوه اداره شده و موارد مشابه ` |
| `D281` | Descriptive, forecast, or explanatory text | `وجوه اداره شده و موارد مشابه ` |
| `A282` | Row label or section heading | `توضیحات در خصوص تغییرات بااهمیت: ` |
| `A283` | Row label or section heading | `«جملات آینده‌نگر نشان‌دهنده انتظارات، باورها یا پیش‌بینی‌های جاری از رویدادها و عملکرد مالی است. این جملات در معرض ریسک‌ها، عدم‌قطعیت‌ها و مفروضات غیرقطعی قرار دارند. بنابراین نتایج واقعی ممکن است متفاوت از نتایج مورد انتظار باشند.» ` |
| `A287` | Statement or table title | `خلاصه اطلاعات گزارش تفسیری - صفحه 2` |
| `A292` | Row label or section heading | `اطلاعات این فرم گزیده ای از اطلاعات گزارش تفسیری مدیریت می باشد که هیئت مدیره شرکت مطابق با مفاد دستورالعمل اجرایی افشای اطلاعات شرکتهای ثبت شده نزد سازمان موظف به ارائه آن در پیوست این اطلاعیه می باشد و این اطلاعات جایگزین گزارش مذکور نیست. ` |
| `A293` | Row label or section heading | `وضعیت کارکنان:` |
| `A294` | Unit note | `کلیه مبالغ درج شده به میلیون ریال می باشد` |
| `A295` | Column header or subheader | `شرح` |
| `B295` | Column header or subheader | `در تاریخ ۱۴۰۲/۱۲/۲۹` |
| `C295` | Column header or subheader | `در تاریخ ۱۴۰۳/۰۶/۳۱` |
| `D295` | Column header or subheader | `برآورد در تاریخ ۱۴۰۳/۱۲/۳۰` |
| `A296` | Row label or section heading | `تعداد شعب ` |
| `A297` | Row label or section heading | `تعداد کارکنان ` |
| `A298` | Row label or section heading | `اطلاعات حق الوکاله و کفایت سرمایه` |
| `A299` | Unit note | `کلیه مبالغ درج شده به میلیون ریال می باشد` |
| `A300` | Column header or subheader | `شرح` |
| `B300` | Column header or subheader | `سال مالی منتهی به۱۴۰۲/۱۲/۲۹` |
| `C300` | Column header or subheader | `دوره ۶ ماهه منتهی به ۱۴۰۳/۰۶/۳۱` |
| `D300` | Column header or subheader | `برآورد تغییر روند در دوره ۶ ماهه منتهی به ۱۴۰۳/۱۲/۳۰` |
| `A301` | Row label or section heading | `سهم بانک از درآمدهای مشاع ` |
| `D301` | Descriptive, forecast, or explanatory text | `مابه التفاوت سود قابل پرداخت به سپرده گذاران بر اساس بخشنامه بانک مرکزی محاسبه می گردد ` |
| `A302` | Row label or section heading | `سهم سپرده گذاران از درآمدهای مشاع ` |
| `D302` | Descriptive, forecast, or explanatory text | `مابه التفاوت سود قابل پرداخت به سپرده گذاران بر اساس بخشنامه بانک مرکزی محاسبه می گردد ` |
| `A303` | Row label or section heading | `نرخ حق الوکاله اعلام شده ` |
| `A304` | Row label or section heading | `مبلغ حق الوکاله اعمال شده ` |
| `A305` | Row label or section heading | `مابه التفاوت سود قابل پرداخت (مازاد سود پرداختی) به سپرده گذاران ` |
| `D305` | Descriptive, forecast, or explanatory text | `مابه التفاوت سود قابل پرداخت به سپرده گذاران بر اساس بخشنامه بانک مرکزی محاسبه می گردد ` |
| `A306` | Row label or section heading | `نسبت کفایت سرمایه ` |
| `D306` | Descriptive, forecast, or explanatory text | `در صورت تحقق هدف ترسیمی در خصوص کسب سود، انتظار می رود این نسبت بهبود یابد ` |
| `A307` | Row label or section heading | `اهداف و راهبردهای آتی مدیریت در خصوص فعالیت شرکت:` |
| `A308` | Row label or section heading | `اهداف و راهبردهای آتی مدیریت در خصوص فعالیت شرکت: ` |
| `A309` | Row label or section heading | `درآمد حاصل از تسهيلات اعطايي و سپرده گذاري` |
| `A310` | Unit note | `کلیه مبالغ درج شده به میلیون ریال می باشد` |
| `A311` | Column header or subheader | `شرح` |
| `B311` | Column header or subheader | `سال مالی منتهی به ۱۴۰۲/۱۲/۲۹` |
| `C311` | Column header or subheader | `متوسط نرخ سود سال مالی منتهی به ۱۴۰۲/۱۲/۲۹ (درصد)` |
| `D311` | Column header or subheader | `دوره ۶ ماهه منتهی به ۱۴۰۳/۰۶/۳۱` |
| `E311` | Column header or subheader | `متوسط نرخ سود دوره ۶ ماهه منتهی به ۱۴۰۳/۰۶/۳۱ (درصد)` |
| `F311` | Column header or subheader | `برآورد تغییر روند در دوره ۶ ماهه منتهی به ۱۴۰۳/۱۲/۳۰` |
| `A312` | Row label or section heading | `درآمد تسهیلات اعطایی: ` |
| `A313` | Row label or section heading | `فروش اقساطی ` |
| `A314` | Row label or section heading | `جعاله ` |
| `A315` | Row label or section heading | `اجاره به شرط تملیک ` |
| `A316` | Row label or section heading | `سلف ` |
| `A317` | Row label or section heading | `مضاربه ` |
| `A318` | Row label or section heading | `مشارکت مدنی ` |
| `A319` | Row label or section heading | `خرید دین ` |
| `A320` | Row label or section heading | `بدهکاران بابت اعتبارات اسنادی پرداخت شده ` |
| `A321` | Row label or section heading | `بدهکاران بابت ضمانت نامه های پرداخت شده ` |
| `A322` | Row label or section heading | `تسهیلات ارزی ` |
| `A323` | Row label or section heading | `تسهیلات قرض الحسنه ` |
| `A324` | Row label or section heading | `سایر درآمد تسهیلات اعطایی ` |
| `A325` | Row label or section heading | `جمع درآمد حاصل از تسهیلات اعطایی ` |
| `A326` | Row label or section heading | `جایزه سپرده قانونی ` |
| `A327` | Row label or section heading | `سود حاصل از سپرده گذاری در بانکها ` |
| `A328` | Row label or section heading | `جمع سود حاصل از سپرده گذاری ها ` |
| `A329` | Row label or section heading | `درآمد اوراق بدهی و سایر درآمدهای ناشی از سپرده گذاری ` |
| `A330` | Row label or section heading | `درآمد حاصل ازتسهیلات اعطایی و سپرده‌گذاری‌ها ` |
| `A331` | Row label or section heading | `ارائه توضیحات در خصوص نحوه محاسبه متوسط نرخ سود تسهیلات: ` |
| `C331` | Descriptive, forecast, or explanatory text | `براساس میانگین هفتگی تسهیلات و سود دریافتی نرخ بازده تسهیلات محاسبه گردیده است ` |
| `A332` | Row label or section heading | `خالص سود (زیان) سرمایه گذاری‌ ها` |
| `A333` | Unit note | `کلیه مبالغ درج شده به میلیون ریال می باشد` |
| `A334` | Column header or subheader | `شرح` |
| `B334` | Column header or subheader | `سال مالی منتهی به۱۴۰۲/۱۲/۲۹` |
| `C334` | Column header or subheader | `دوره ۶ ماهه منتهی به ۱۴۰۳/۰۶/۳۱` |
| `D334` | Column header or subheader | `برآورد تغییر روند در دوره ۶ ماهه منتهی به ۱۴۰۳/۱۲/۳۰` |
| `A335` | Row label or section heading | `درآمد حاصل از سرمایه گذاری در سهام ` |
| `D335` | Descriptive, forecast, or explanatory text | `واگذاری شرکت ها در دستور کار قرار دارد. ` |
| `A336` | Row label or section heading | `سود(زیان) حاصل از فروش سرمایه گذاری ` |
| `D336` | Descriptive, forecast, or explanatory text | `واگذاری شرکت ها در دستور کار قرار دارد. ` |
| `A337` | Row label or section heading | `سود (زیان) تعدیل ذخیره کاهش ارزش سرمایه گذاریها ` |
| `A338` | Row label or section heading | `جمع درآمدهای حاصل از سرمایه گذاری ` |
| `A339` | Row label or section heading | `«جملات آینده‌نگر نشان‌دهنده انتظارات، باورها یا پیش‌بینی‌های جاری از رویدادها و عملکرد مالی است. این جملات در معرض ریسک‌ها، عدم‌قطعیت‌ها و مفروضات غیرقطعی قرار دارند. بنابراین نتایج واقعی ممکن است متفاوت از نتایج مورد انتظار باشند.» ` |
| `A343` | Statement or table title | `خلاصه اطلاعات گزارش تفسیری - صفحه 3` |
| `A348` | Row label or section heading | `اطلاعات اين فرم گزيده اي از اطلاعات گزارش تفسيري مديريت مي باشد که هيئت مديره شرکت مطابق با مفاد دستورالعمل اجرايي افشاي اطلاعات شرکتهاي ثبت شده نزد سازمان موظف به ارائه آن در پيوست اين اطلاعيه مي باشد و اين اطلاعات جايگزين گزارش مذکور نيست. ` |
| `A349` | Row label or section heading | `وضعیت شرکتهای سرمایه پذیر:` |
| `A350` | Unit note | `کلیه مبالغ درج شده به میلیون ریال می باشد` |
| `A351` | Column header or subheader | `نام شرکت` |
| `C351` | Column header or subheader | `سال مالي منتهي به ۱۴۰۲/۱۲/۲۹` |
| `G351` | Column header or subheader | `دوره ۶ ماهه منتهي به ۱۴۰۳/۰۶/۳۱` |
| `J351` | Column header or subheader | `تشريح آخرين وضعيت و برنامه هاي آتي شرکت در شرکت سرمايه پذير` |
| `C352` | Column header or subheader | `درصد مالکيت` |
| `D352` | Column header or subheader | `بهاي تمام شده` |
| `E352` | Column header or subheader | `سال مالي شرکت سرمايه پذير` |
| `F352` | Column header or subheader | `درآمد سرمايه گذاري` |
| `G352` | Column header or subheader | `درصد مالکيت` |
| `H352` | Column header or subheader | `بهاي تمام شده` |
| `I352` | Column header or subheader | `درآمد سرمايه گذاري` |
| `A353` | Row label or section heading | `هلدينگ غدير ` |
| `E353` | Descriptive, forecast, or explanatory text | `۱۴۰۳/۱۲/۳۰ ` |
| `J353` | Descriptive, forecast, or explanatory text | `واگذاری سرمایه گذاری ها در دستور کار قرار دارد. ` |
| `A354` | Row label or section heading | `فولاد مبارکه اصفهان ` |
| `E354` | Descriptive, forecast, or explanatory text | `۱۴۰۳/۱۲/۳۰ ` |
| `J354` | Descriptive, forecast, or explanatory text | `واگذاری سرمایه گذاری ها در دستور کار قرار دارد. ` |
| `A355` | Row label or section heading | `سرمايه گذاري گروه مالي سپهر صادرات ` |
| `E355` | Descriptive, forecast, or explanatory text | `۱۴۰۳/۱۲/۳۰ ` |
| `J355` | Descriptive, forecast, or explanatory text | `واگذاری سرمایه گذاری ها در دستور کار قرار دارد. ` |
| `A356` | Row label or section heading | `ساير شرکتهاي خارج از بورس ` |
| `E356` | Descriptive, forecast, or explanatory text | `۱۴۰۳/۱۲/۳۰ ` |
| `J356` | Descriptive, forecast, or explanatory text | `واگذاری سرمایه گذاری ها در دستور کار قرار دارد. ` |
| `A357` | Row label or section heading | `ساير درآمدها و هزینه های عملياتي:` |
| `A358` | Unit note | `کلیه مبالغ درج شده به میلیون ریال می باشد` |
| `A359` | Column header or subheader | `شرح` |
| `B359` | Column header or subheader | `۱۴۰۲/۱۲/۲۹` |
| `C359` | Column header or subheader | `۱۴۰۳/۰۶/۳۱` |
| `A360` | Row label or section heading | `ساير درآمدهاي عملياتي: ` |
| `A361` | Row label or section heading | `وجه التزام دريافتي از محل ساير مطالبات ` |
| `A362` | Row label or section heading | `درآمد شعب خارج از کشور ` |
| `A363` | Row label or section heading | `ساير ` |
| `A365` | Row label or section heading | `جمع ساير درآمدهاي عملياتي ` |
| `A366` | Row label or section heading | `ساير هزينه هاي عملياتي: ` |
| `A367` | Row label or section heading | `ساير هزينه ها ` |
| `A369` | Row label or section heading | `جمع ساير هزينه هاي عملياتي ` |
| `A370` | Row label or section heading | `جمع ساير درآمدها و هزينه هاي عملياتي ` |
| `A371` | Row label or section heading | `برآورد شرکت از تغییرات خالص سایر درآمدها (هزینه ها)ی عملیاتی:` |
| `A372` | Row label or section heading | `دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ` |
| `C372` | Descriptive, forecast, or explanatory text | `بهبود درآمد مورد انتظار است ` |
| `A374` | Row label or section heading | `خالص ساير درآمدها و هزینه ها:` |
| `A375` | Unit note | `کلیه مبالغ درج شده به میلیون ریال می باشد` |
| `A376` | Column header or subheader | `خالص ساير درآمدها و هزينه ها` |
| `B376` | Column header or subheader | `۱۴۰۲/۱۲/۲۹` |
| `C376` | Column header or subheader | `۱۴۰۳/۰۶/۳۱` |
| `A377` | Row label or section heading | `ساير درامدها و هزينه ها ` |
| `A379` | Row label or section heading | `جمع خالص ساير درآمدها و هزينه ها ` |
| `A380` | Row label or section heading | `برآورد شرکت از تغییرات خالص ساير درآمدها و هزینه ها :` |
| `A381` | Row label or section heading | `دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ` |
| `C381` | Descriptive, forecast, or explanatory text | `بهبود درآمد مورد انتظار است ` |
| `A383` | Row label or section heading | `هزینه های اداری و عمومی:` |
| `A384` | Unit note | `کلیه مبالغ درج شده به میلیون ریال می باشد` |
| `A385` | Column header or subheader | `هزينه هاي اداري و عمومي` |
| `B385` | Column header or subheader | `۱۴۰۲/۱۲/۲۹` |
| `C385` | Column header or subheader | `۱۴۰۳/۰۶/۳۱` |
| `A386` | Row label or section heading | `هزينه هاي اداري و عمومي ` |
| `A388` | Row label or section heading | `جمع هزينه هاي اداري و عمومي ` |
| `A389` | Row label or section heading | `برآورد شرکت از تغییرات هزینه های اداری و عمومی :` |
| `A390` | Row label or section heading | `دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ` |
| `C390` | Descriptive, forecast, or explanatory text | `مدیریت هزینه ها در این بخش مورد توجه و تاکید می باشد. ` |
| `A392` | Row label or section heading | `هزینه مالی:` |
| `A393` | Unit note | `کلیه مبالغ درج شده به میلیون ریال می باشد` |
| `A394` | Column header or subheader | `هزينه‌هاي مالي` |
| `B394` | Column header or subheader | `۱۴۰۲/۱۲/۲۹` |
| `C394` | Column header or subheader | `۱۴۰۳/۰۶/۳۱` |
| `A395` | Row label or section heading | `هزينه مالي تسهيلات دريافتي از ساير بانکها و موسسات اعتباري ` |
| `A396` | Row label or section heading | `جريمه اضافه برداشت از بانک مرکزي ` |
| `A397` | Row label or section heading | `ساير هزينه هاي مالي ` |
| `A398` | Row label or section heading | `جمع هزينه‌هاي مالي ` |
| `A399` | Row label or section heading | `برآورد شرکت از تغییرات هزینه های مالی :` |
| `A400` | Row label or section heading | `دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ` |
| `C400` | Descriptive, forecast, or explanatory text | `با توجه به شرایط موجود کنترل هزینه ها بیش از پیش مورد انتظار است. ` |
| `A402` | Row label or section heading | `برنامه شرکت در خصوص تقسیم سود` |
| `A403` | Column header or subheader | `مبلغ سود (زيان) انباشته پايان سال مالي گذشته` |
| `B403` | Column header or subheader | `سود سهام پيشنهادي هيئت مديره در سال مالي گذشته` |
| `C403` | Column header or subheader | `مبلغ سود (زيان) خالص سال مالي گذشته` |
| `D403` | Column header or subheader | `سود سهام مصوب مجمع سال مالي گذشته` |
| `E403` | Column header or subheader | `پيشنهاد هيئت مديره درخصوص درصد تقسيم سود سال مالي جاري` |
| `A405` | Row label or section heading | `سایر برنامه های با اهمیت شرکت` |
| `A406` | Column header or subheader | `دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ` |
| `B406` | Column header or subheader | `افزایش سهم بازار، بهبود ترکیب منابع سپرده ای، افزایش سهم بازار منابع ارزان قیمت، کاهش بهای تمام شده پول، کاهش مطالبات غیر جاری، افزایش عملیات بانکداری الکترونیک. ` |
| `A408` | Row label or section heading | `سایر توضیحات با اهمیت` |
| `A409` | Row label or section heading | `افزایش سهم بازار، بهبود ترکیب منابع سپرده ای، افزایش سهم بازار منابع ارزان قیمت، کاهش بهای تمام شده پول، کاهش مطالبات غیر جاری، افزایش عملیات بانکداری الکترونیک. ` |
| `A410` | Row label or section heading | `«جملات آينده‌نگر نشان‌دهنده انتظارات، باورها يا پيش‌بيني‌هاي جاري از رويدادها و عملکرد مالي است. اين جملات در معرض ريسک‌ها، عدم‌قطعيت‌ها و مفروضات غيرقطعي قرار دارند. بنابراين نتايج واقعي ممکن است متفاوت از نتايج مورد انتظار باشند.» ` |
