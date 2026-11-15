# Parsian Quarterly Workbook Inspection — DB-STD-003

## 1. Executive summary

`excel/parsian_periodic.xlsx` is a one-sheet interim financial-report workbook with a reporting endpoint of ۱۴۰۳/۰۶/۳۱. The sheet contains an income statement, comprehensive income, statement of financial position, changes in equity, cash flows, and extensive management-report schedules. The workbook metadata has no title, subject, ticker, or named reporting entity. The filename suggests Parsian, but the workbook body does not name Parsian Bank as the reporting entity; the occurrence of Parsian in investee labels does not prove issuer identity. Treat reporting-entity identity as unconfirmed pending owner/source-filing confirmation.

Flow-statement headers show current period ending ۱۴۰۳/۰۶/۳۱, restated comparative ending ۱۴۰۲/۰۶/۳۱, and restated prior-year end ۱۴۰۲/۱۲/۲۹. A six-month duration is explicitly present in supplementary schedule headers (for example `C302` and `D313`) and is consistent with the current statement endpoint, but core income/cash-flow headers themselves say only "period ending." Comparative six-month duration is supported by corresponding Jalali endpoints, not explicitly stated in those headers. Balance-sheet columns are point-in-time dates. No standalone-quarter values are calculated.

All monetary amounts are labeled million rials in relevant table unit notes; EPS is in rials, with separate rate, percentage, count, and narrative fields throughout the supplemental schedules. The complete source text-cell inventory is included in Appendix A.

## 2. Workbook and worksheet inventory

| Property | Direct evidence |
|---|---|
| File and format | `excel/parsian_periodic.xlsx`, XLSX, 30,584 bytes. |
| Worksheet count/order | One worksheet: `Recovered_Sheet1`, visible. |
| Used range/dimensions | `A1:L411`, 411 rows x 12 columns. |
| Metadata | Title and subject empty; creator `Papa`; created/modified `2026-11-12 08:09:14`. These timestamps are file metadata, not report publication evidence. |
| Structure | 101 merged ranges; no formulas, defined names, freeze panes, hidden rows/columns, charts, images, or comments detected. |
| Contents | One financial-report workbook with five principal statement areas and management interpretive schedules/disclosures. |

## 3. Report identity and period

| Question | Evidence and conclusion |
|---|---|
| Reporting entity | Not identified in workbook metadata or an issuer-name field. Filename suggests Parsian, but that is not sufficient evidence. The investee table names `صرافي پارسيان` at `A355`; this does not establish the reporting entity. Owner confirmation or the original filing cover is needed. |
| Ticker | No ticker found. |
| Report type | Interim financial-report structure with period-end comparative statements. Six-month duration is explicitly stated in supplementary headers such as `C302`, `D313`, `C336`, and `D336`; core income/cash-flow headers do not repeat the duration. |
| Current endpoint | ۱۴۰۳/۰۶/۳۱, in `B10`, `B60`, `B79`, `B176` and other schedules. Preserve as Jalali text. |
| Comparative flow dates | Current B endpoint ۱۴۰۳/۰۶/۳۱; C comparative ۱۴۰۲/۰۶/۳۱; D comparative year-end ۱۴۰۲/۱۲/۲۹ (`B10:D10`, `B176:D176`). C as corresponding six months is supported by matching month/day one year earlier and explicit six-month schedule evidence. D as prior full year is supported by equity/cash roll-forwards. |
| Balance-sheet dates | B current endpoint, C restated ۱۴۰۲/۱۲/۲۹, D restated ۱۴۰۲/۰۱/۰۱ (`B79:D79`). These are stocks at dates, not period flows. |
| Fiscal-year cycle | Equity opens at ۱۴۰۲/۰۱/۰۱ (`A131`), shows restated opening (`A134`), and prior year-end at ۱۴۰۲/۱۲/۲۹ (`A151`). This directly shows the prior fiscal-year cycle. Current-year start ۱۴۰۴/۰۱/۰۱ is plausible but not explicitly labeled as the current opening balance. |
| Restatements | C/D comparative headers in statements are marked "restated" (`C10:D10`, `C60:D60`, `C79:D79`, `C176:D176`). Reason text is not present in the associated explanatory blocks (rows 44:48, 221:225). |

## 4. Financial statements and major-table inventory

| Sheet range | Table / title cells | Layout, unit and data type |
|---|---|---|
| `A3:E48` | Income statement, `A3`, repeated `A8` | Column headers `A10:E11`; detail/result lines 12:42; million rials (`A9`), EPS rows explicitly rial-based. Reason-for-change headings at A44/A46/A48. Flows, subtotals, EPS/derived values, and capital. |
| `A53:E68` | Comprehensive income, `A53`, repeated `A58` | Headers `A60:E61`, numeric rows 62:68; million rials (`A59`). Net income, OCI items, tax, comprehensive-income total. |
| `A72:E119` | Financial position, `A72`, repeated `A77` | Headers `A79:E80`; rows 81:119; million rials (`A78`). Asset, equity and liability stocks at three dates, plus percentage-change column. |
| `A123:L165` | Changes in equity, `A123`, repeated `A128` | Unit A129; component headers A130:L130; roll-forward rows 131:165; million rials. Equity component stocks and period movements; L is total. |
| `A169:E225` | Cash-flow statement, `A169`, repeated `A174` | Headers A176:E177; flow/reconciliation rows 178:213; unit A175; explanatory headings A221/A223/A225. Million-rial flows plus percentage comparison. |
| `A230:K253` | Management-report page 1 and loan/receivable-risk table | Scope/limitation text A230/A235; table title A236; unit A237; multilevel headers A238:A239; exposure by status, deductions, closing balances, collateral and reserve estimates through row 253. Million rials and percentage rates. |
| `A254:I261` | Management estimates for loan rates/balances and doubtful-receivable reserves | Period/narrative blocks at rows 255, 258, 261; estimates and qualitative text. |
| `A263:F276` | Customer deposits | Unit A264; headers A265:A267; deposit classes and totals 268:276. B/C point-in-time balances; D/E rates; F management forecast. |
| `A277:F283` | Off-balance-sheet items | Unit A278; date headers at A279:F279; customer and bank obligation descriptions and point-in-time values. |
| `A284:E285` | Significant-change explanation / forward-looking disclaimer | Heading A284; disclaimer A285. Descriptive text. |
| `A289:K294` | Management interpretive-report excerpt, page 2 | Page title A289; explanation of excerpt limits at A294. |
| `A295:D299` | Employee/branch status | Header row 297; branch/employee counts and estimate. Quantities. |
| `A300:D308` | Agency fee / capital adequacy | Header row 302; monetary amounts, ratio/rate and narrative estimate. Mixed measurements. |
| `A309:F333` | Strategy and facility/deposit income | Header row 313; loan-product, deposit and debt-security income with average rates and forecast narrative; explanation at A333. Million rials and percent. |
| `A334:D341` | Investment profit/loss | Header row 336; investment income/sale/impairment details, total and forecast text. |
| `A345:J358` | Investee-company disclosure | Page title A345; scope explanation A350; multilevel headers rows 353:354; ownership, cost, investee year, income, future plans. |
| `A359:C372` | Other operating income/expenses | Header row 361; detailed components and totals; forecast at 371:372. |
| `A374:C382` | Net other income/expenses | Header row 376; detail and total; estimate at 381:382. |
| `A384:C391` | Administrative/general expenses | Header row 386; expense/total; estimate rows 390:391. |
| `A393:C401` | Financial expenses | Header row 395; components/total; estimate rows 400:401. |
| `A403:E405` | Profit-distribution plan | Headers A404:E404; prior-year amounts and proposed distribution percentage. Mixed stock, flow and ratio. |
| `A406:B407` | Other significant plans | Forecast period and descriptive content. |
| `A409:I411` | Other significant explanations | Descriptive text and forward-looking disclaimer. |

Unit declarations recur at `A9`, `A59`, `A78`, `A129`, `A175`, `A237`, `A264`, `A278`, `A296`, `A301`, `A312`, `A335`, `A352`, `A360`, `A375`, `A385`, and `A394`; they say amounts are million rials, except where row/column labels identify other units such as rials per share, percentages, rates, or counts. Appendix A preserves exact unit strings and all other text labels.

## 5. Complete source Header inventory

Appendix A records every nonempty text-valued cell in the worksheet with its exact source address, wording, and broad contextual classification. This includes column headers, row labels, units, table titles, explanatory text, and forecast narratives so no candidate source Header is silently omitted. Numeric cells are excluded. Context and units for each table are cross-referenced in sections 4 and 6.

## 6. Temporal classification matrix

| Source header/address | Temporal meaning | Evidence / status |
|---|---|---|
| `B10` and `B176`: current period ending ۱۴۰۳/۰۶/۳۱ | Current period flow; six-month interpretation | Supplementary schedules explicitly use six-month terminology at `C302`, `D313`, `C336`; core headers only say period ending. Six-month duration supported by those headers and statement structure. |
| `C10`/`C176`: restated period ending ۱۴۰۲/۰۶/۳۱ | Comparative flow, likely corresponding six months | Matching Jalali month/day one year earlier; duration inferred, not explicit in core header. |
| `D10`/`D176`: restated period ending ۱۴۰۲/۱۲/۲۹ | Prior fiscal-year flow | Prior-year-end date; equity rows 135:151 and cash opening/closing balances support full-year comparison. |
| `B79:D79` | Point-in-time balances | Explicit endpoint/restated date headers; not flows. |
| `E10`, `E60`, `E79`, `E176` | Percentage-change / derived columns | Main-statement E values checked against B vs C using signed change divided by absolute C, rounded to integer, where C nonzero. They are not monetary values. |
| Equity rows `A131`, `A134`, `A135:A151`, `A152:A165` | Opening stock, restatement adjustment, prior-year movements/closing, current-period movements/closing | Dates and row labels encode the periods. Current opening date is not explicit. |
| Cash-flow rows `A209:A212` | Net change, opening cash, FX effect, closing cash | Each column reconciles with formula including FX effect; see below. |
| Supplementary tables | Depends on each exact header | Tables include point-in-time balances, annual/current six-month flows, forecasts, rates, percentages, counts, and narratives. See date and type headers in Appendix A. |

Cash reconciliation from `B209:D212`: B: 295,173,082 - 32,576,205 + 84,513,662 = 347,110,539; beginning matches balance-sheet C82 and ending matches B82. C: 229,326,967 - 77,842,463 + 19,036,184 = 170,520,688; beginning matches balance-sheet D82. D: 229,326,967 - 85,837,240 + 151,683,355 = 295,173,082; beginning matches D82 and ending matches C82. This supports D as prior full-year and C as a likely six-month comparative; the C ending balance is not a separate balance-sheet date column.

No standalone-quarter figures were calculated. Income/cash-flow headers do not label a standalone quarter, and the report's six-month figures must not be split by subtraction without separate evidence.

## 7. Financial nature, hierarchy, and double-counting risks

- **Flows:** income/expense statement rows 13:34; comprehensive-income rows 62:68; cash flows 179:213; detail income/expense schedules; equity movement rows.
- **Stocks:** balance-sheet assets/equity/liabilities 82:119; deposit balances 269:276; credit exposures/allowance bases; dated off-balance obligations; opening/closing cash and equity.
- **Ratios/derived measures:** percentage changes, EPS rows 35:41, average deposit/income rates, investee ownership percentages, capital adequacy, distribution percentage.
- **Counts:** branches and employees (`A298:A299`).
- **Descriptive/informational:** strategy, forecast commentary, reporting limitations, legal/forward-looking notes.
- Income subtotal row 22 and net result rows 28, 31, 34 should not be added to constituent rows. The same net result is carried into comprehensive income at row 62 and total comprehensive income row 68.
- Summary income row 13 is detailed in the management schedule at 313:332; investment result row 19 is detailed at 336:340 and linked with investee disclosures at 353:358. These are overlapping summary/detail presentations and must not be summed twice without reconciliation.
- Balance-sheet total rows 94, 107, 116, 118, 119 aggregate components. Equity total column L and its opening/movement/closing rows are a roll-forward, not additional income.
- Cash-flow totals rows 181, 189:190, 208:209 and cash reconciliation rows 210:212 summarize lower-level flows. The FX-effect row 211 materially contributes to closing cash; do not omit it from the reconciliation or double-count it as operating cash flow.
- Deposit totals rows 272, 274, 276 aggregate deposit groups. Rates and balance amounts are different measure types.
- Credit-risk schedule separates status buckets, deductions, collateral, reserve bases, reserve rates, and allowances. Do not add a percentage to a monetary amount or treat gross exposure and net closing balance as duplicate independent assets.
- Comparative statement values are explicitly marked restated; reason blocks at A44:A48 and A221:A225 have headings but no explanatory content.

## 8. Ambiguities requiring owner/ChatGPT review

1. Confirm the reporting entity and ticker. The workbook metadata is blank and no issuer name was located in statement labels; filename alone is insufficient.
2. Confirm whether C flow columns are corresponding six-month comparatives and D columns are full prior-year flows. Dates and equity/cash controls support this, but the headers do not fully spell out durations.
3. Confirm the current fiscal-year start. Prior-year cycle is explicit from ۱۴۰۲/۰۱/۰۱ to ۱۴۰۲/۱۲/۲۹; current opening balance/date ۱۴۰۴/۰۱/۰۱ is not explicitly shown.
4. Explain the restatements and provide the absent text for statement reason-for-change areas.
5. Confirm calculation basis for E percentages; core values generally match B vs C, but blanks, zero comparatives and irregular rows require source methodology.
6. Clarify the meanings of the "equity attributable to investment deposit holders" and related liability rows where values are zero; zero does not establish conceptual absence.
7. Confirm mapping of multi-tier headers in the credit-risk, customer-deposit, off-balance, and investee schedules.
8. Confirm the temporal basis and meaning of estimates dated ۱۴۰۳/۱۲/۳۰; the exact source headers call these six-month periods. Do not infer whether they indicate a second-half forecast or another horizon.

## 9. Recommended next inspection step

Compare this workbook with its original filing cover and source export to establish issuer identity, ticker, comparative duration, restatement notes, and current fiscal-year opening. Then review the multi-tier supplementary tables with the report owner before adopting any mappings. This report records evidence only and does not finalize DB-STD-003.

## Appendix A. Complete source text-cell inventory


Inventory: 484 populated string cells. The inventory preserves original source spelling and Persian/Jalali text verbatim at the stored cell location; numeric cells are not included.
| Cell | Contextual classification | Exact source text |
|---|---|---|
| `A3` | Statement/table title | `صورت سود و زیان` |
| `A8` | Statement/table title | `صورت سود و زیان` |
| `A9` | Unit note | `کلیه مبالغ درج شده به میلیون ریال می باشد` |
| `A10` | Column header/subheader | `شرح` |
| `B10` | Column header/subheader | `دوره منتهي به ۱۴۰۳/۰۶/۳۱` |
| `C10` | Column header/subheader | `تجدید ارائه شده ۱۴۰۲/۰۶/۳۱` |
| `D10` | Column header/subheader | `تجدید ارائه شده ۱۴۰۲/۱۲/۲۹` |
| `E10` | Column header/subheader | `درصد تغييرات` |
| `B11` | Column header/subheader | `حسابرسی نشده` |
| `C11` | Column header/subheader | `حسابرسی شده` |
| `D11` | Column header/subheader | `حسابرسی شده` |
| `A12` | Row label/section heading | `عملیات در حال تداوم: ` |
| `A13` | Row label/section heading | `درآمد تسهيلات اعطايي و سپرده گذاری و اوراق بدهی ` |
| `A14` | Row label/section heading | `هزينه سود سپرده‌ها ` |
| `A15` | Row label/section heading | `خالص درآمد تسهیلات و سپرده گذاری ` |
| `A16` | Row label/section heading | `درآمد کارمزد ` |
| `A17` | Row label/section heading | `هزينه کارمزد ` |
| `A18` | Row label/section heading | `خالص درآمد کارمزد ` |
| `A19` | Row label/section heading | `خالص سود (زیان) سرمایه گذاری‌ها ` |
| `A20` | Row label/section heading | `خالص سود (زيان) مبادلات و معاملات ارزي ` |
| `A21` | Row label/section heading | `ساير درآمدها و هزینه های عملياتي ` |
| `A22` | Row label/section heading | `جمع درآمدهاي عملياتي ` |
| `A23` | Row label/section heading | `خالص ساير درآمدها و هزینه‌ها ` |
| `A24` | Row label/section heading | `هزينه‌هاي اداري و عمومي ` |
| `A25` | Row label/section heading | `هزينه مطالبات مشکوک الوصول ` |
| `A26` | Row label/section heading | `هزينه‌هاي مالي ` |
| `A27` | Row label/section heading | `هزينه استهلاک ` |
| `A28` | Row label/section heading | `سود(زیان) عملیات در حال تداوم قبل از مالیات ` |
| `A29` | Row label/section heading | `ماليات بر درآمد سال جاری ` |
| `A30` | Row label/section heading | `ماليات بر درآمد سال های قبل ` |
| `A31` | Row label/section heading | `سود (زيان) خالص عملیات در حال تداوم ` |
| `A32` | Row label/section heading | `عملیات متوقف شده: ` |
| `A33` | Row label/section heading | `سود(زیان) خالص عملیات متوقف شده ` |
| `A34` | Row label/section heading | `سود(زیان) خالص ` |
| `A35` | Row label/section heading | `سود (زیان)پایه هر سهم (ريال) ` |
| `A36` | Row label/section heading | `عملياتي (ريال) ` |
| `A37` | Row label/section heading | `غيرعملياتي(ريال) ` |
| `A38` | Row label/section heading | `ناشی از عملیات در حال تداوم(ریال) ` |
| `A39` | Row label/section heading | `ناشي از عمليات متوقف شده(ريال) ` |
| `A40` | Row label/section heading | `سود(زیان) پایه هر سهم (ریال) ` |
| `A41` | Row label/section heading | `سود (زیان) خالص هر سهم– ریال ` |
| `A42` | Row label/section heading | `سرمایه ` |
| `A44` | Row label/section heading | `دلایل تغییرات اطلاعات واقعی دوره منتهی به ۱۴۰۳/۰۶/۳۱ ` |
| `A46` | Row label/section heading | `دلایل تغییرات اطلاعات واقعی دوره منتهی به ۱۴۰۲/۰۶/۳۱ ` |
| `A48` | Row label/section heading | `دلایل تغییرات اطلاعات واقعی دوره منتهی به ۱۴۰۲/۱۲/۲۹ ` |
| `A53` | Statement/table title | `صورت سود و زیان جامع` |
| `A58` | Statement/table title | `صورت سود و زیان جامع` |
| `A59` | Unit note | `کلیه مبالغ درج شده به میلیون ریال می باشد` |
| `A60` | Column header/subheader | `شرح` |
| `B60` | Column header/subheader | `دوره منتهي به ۱۴۰۳/۰۶/۳۱` |
| `C60` | Column header/subheader | `تجدید ارائه شده ۱۴۰۲/۰۶/۳۱` |
| `D60` | Column header/subheader | `تجدید ارائه شده ۱۴۰۲/۱۲/۲۹` |
| `E60` | Column header/subheader | `درصد تغییر` |
| `B61` | Column header/subheader | `حسابرسی نشده` |
| `C61` | Column header/subheader | `حسابرسی شده` |
| `D61` | Column header/subheader | `حسابرسی شده` |
| `A62` | Row label/section heading | `سود(زیان) خالص ` |
| `A63` | Row label/section heading | `سایر اقلام سود و زیان جامع: ` |
| `A64` | Row label/section heading | `مازاد تجديد ارزيابي دارايي‌ها ` |
| `A65` | Row label/section heading | `تفاوت تسعیر ارز عملیات خارجی ` |
| `A66` | Row label/section heading | `مالیات مربوط به سایر اقلام سود و زیان جامع ` |
| `A67` | Row label/section heading | `سایر اقلام سود و زیان جامع سال پس از کسر مالیات ` |
| `A68` | Row label/section heading | `سود(زيان) جامع سال ` |
| `A72` | Statement/table title | `صورت وضعیت مالی` |
| `A77` | Statement/table title | `صورت وضعیت مالی` |
| `A78` | Unit note | `کلیه مبالغ درج شده به میلیون ریال می باشد` |
| `A79` | Column header/subheader | `شرح` |
| `B79` | Column header/subheader | `دوره منتهي به ۱۴۰۳/۰۶/۳۱` |
| `C79` | Column header/subheader | `تجدید ارائه شده ۱۴۰۲/۱۲/۲۹` |
| `D79` | Column header/subheader | `تجدید ارائه شده ۱۴۰۲/۰۱/۰۱` |
| `E79` | Column header/subheader | `درصد تغييرات` |
| `B80` | Column header/subheader | `حسابرسی نشده` |
| `C80` | Column header/subheader | `حسابرسی شده` |
| `D80` | Column header/subheader | `حسابرسی نشده` |
| `A81` | Row label/section heading | `دارایی ها ` |
| `A82` | Row label/section heading | `موجودي نقد ` |
| `A83` | Row label/section heading | `مطالبات از بانک ها و ساير موسسات اعتباري ` |
| `A84` | Row label/section heading | `مطالبات از دولت ` |
| `A85` | Row label/section heading | `تسهيلات اعطايي و مطالبات از اشخاص دولتي ` |
| `A86` | Row label/section heading | `تسهيلات اعطايي و مطالبات از اشخاص غير دولتي ` |
| `A87` | Row label/section heading | `سرمایه‌گذاری در سهام و ساير اوراق بهادار ` |
| `A88` | Row label/section heading | `مطالبات از شرکت‌های فرعی و وابسته ` |
| `A89` | Row label/section heading | `ساير حسابهاي دريافتني ` |
| `A90` | Row label/section heading | `دارایی‌هاي ثابت مشهود ` |
| `A91` | Row label/section heading | `دارایی‌هاي نا مشهود ` |
| `A92` | Row label/section heading | `سپرده قانونی ` |
| `A93` | Row label/section heading | `ساير دارایی‌ها ` |
| `A94` | Row label/section heading | `جمع دارایی‌ها ` |
| `A95` | Column header/subheader | `حقوق مالکانه و بدهی‌ها ` |
| `B95` | Column header/subheader | `دوره منتهی به ۱۴۰۳/۰۶/۳۱ ` |
| `C95` | Column header/subheader | `تجدید ارائه شده ۱۴۰۲/۱۲/۲۹ ` |
| `D95` | Column header/subheader | `تجدید ارائه شده۱۴۰۲/۰۱/۰۱ ` |
| `E95` | Column header/subheader | `درصد تغييرات ` |
| `A96` | Row label/section heading | `حقوق مالکانه ` |
| `A97` | Row label/section heading | `سرمايه ` |
| `A98` | Row label/section heading | `افزايش سرمايه در جريان ` |
| `A99` | Row label/section heading | `صرف سهام ` |
| `A100` | Row label/section heading | `اندوخته صرف سهام ` |
| `A101` | Row label/section heading | `اندوخته قانوني ` |
| `A102` | Row label/section heading | `ساير اندوخته‌ها ` |
| `A103` | Row label/section heading | `مازاد تجديد ارزيابي دارايي‌ها ` |
| `A104` | Row label/section heading | `تفاوت تسعیر ارز ` |
| `A105` | Row label/section heading | `سود (زيان) انباشته ` |
| `A106` | Row label/section heading | `سهام خزانه ` |
| `A107` | Row label/section heading | `جمع حقوق مالکانه ` |
| `A108` | Row label/section heading | `بدهی‌ها ` |
| `A109` | Row label/section heading | `بدهي به بانكها و ساير موسسات اعتباري ` |
| `A110` | Row label/section heading | `سپرده‌هاي مشتریان ` |
| `A111` | Row label/section heading | `سود سهام پرداختني ` |
| `A112` | Row label/section heading | `اوراق بدهی ` |
| `A113` | Row label/section heading | `ذخيره ماليات عملکرد ` |
| `A114` | Row label/section heading | `ذخاير و ساير بدهی‌ها ` |
| `A115` | Row label/section heading | `ذخيره مزاياي پايان خدمت و تعهدات بازنشستگی کارکنان ` |
| `A116` | Row label/section heading | `جمع بدهی های قبل از حقوق صاحبان سپرده های سرمایه گذاری ` |
| `A117` | Row label/section heading | `حقوق صاحبان سپرده‌های سرمایه‌گذاری ` |
| `A118` | Row label/section heading | `جمع بدهی‌ها ` |
| `A119` | Row label/section heading | `جمع بدهی‌ها و حقوق مالکانه ` |
| `A123` | Statement/table title | `صورت تغییرات در حقوق مالکانه` |
| `A128` | Statement/table title | `صورت تغییرات در حقوق مالکانه` |
| `A129` | Unit note | `کلیه مبالغ درج شده به میلیون ریال می باشد` |
| `A130` | Column header/subheader | `شرح` |
| `B130` | Column header/subheader | `سرمایه` |
| `C130` | Column header/subheader | `افزایش سرمایه در جریان` |
| `D130` | Column header/subheader | `صرف سهام` |
| `E130` | Column header/subheader | `صرف سهام خزانه` |
| `F130` | Column header/subheader | `اندوخته قانونی` |
| `G130` | Column header/subheader | `سایر اندوخته‌ها` |
| `H130` | Column header/subheader | `مازاد تجدید ارزیابی دارایی‌ها` |
| `I130` | Column header/subheader | `تفاوت تسعیر ارز عملیات خارجی` |
| `J130` | Column header/subheader | `سود انباشته` |
| `K130` | Column header/subheader | `سهام خزانه` |
| `L130` | Column header/subheader | `جمع کل` |
| `A131` | Row label/section heading | `مانده در ۱۴۰۲/۰۱/۰۱ ` |
| `A132` | Row label/section heading | `اصلاح اشتباهات ` |
| `A133` | Row label/section heading | `تغییر در رویه‌های حسابداری ` |
| `A134` | Row label/section heading | `مانده تجدید ارائه شده در ۱۴۰۲/۰۱/۰۱ ` |
| `A135` | Row label/section heading | `تغییرات حقوق مالکانه در سال ۱۴۰۲/۱۲/۲۹ ` |
| `A136` | Row label/section heading | `سود(زيان) خالص گزارش شده در صورت‌هاي مالي سال ۱۴۰۲/۱۲/۲۹ ` |
| `A137` | Row label/section heading | `اصلاح اشتباهات ` |
| `A138` | Row label/section heading | `تغییر در رویه‌های حسابداری ` |
| `A139` | Row label/section heading | `سود خالص تجدید ارائه شده سال ۱۴۰۲/۱۲/۲۹ ` |
| `A140` | Row label/section heading | `سایر اقلام سود و زیان جامع پس از کسر مالیات ` |
| `A141` | Row label/section heading | `سود(زيان) جامع سال ۱۴۰۲/۱۲/۲۹ ` |
| `A142` | Row label/section heading | `سود سهام مصوب ` |
| `A143` | Row label/section heading | `افزایش سرمایه ` |
| `A144` | Row label/section heading | `افزایش سرمایه در جریان ` |
| `A145` | Row label/section heading | `خرید سهام خزانه ` |
| `A146` | Row label/section heading | `فروش سهام خزانه ` |
| `A147` | Row label/section heading | `سود (زیان) حاصل از فروش سهام خزانه ` |
| `A148` | Row label/section heading | `انتقال از سایر اقلام حقوق مالکانه به سود و زیان انباشته ` |
| `A149` | Row label/section heading | `تخصیص به اندوخته قانونی ` |
| `A150` | Row label/section heading | `تخصیص به سایر اندوخته‌ها ` |
| `A151` | Row label/section heading | `مانده تجدید ارائه شده در ۱۴۰۲/۱۲/۲۹ ` |
| `A152` | Row label/section heading | `تغییرات حقوق مالکانه در سال ۱۴۰۳/۰۶/۳۱ ` |
| `A153` | Row label/section heading | `سود خالص ۱۴۰۳/۰۶/۳۱ ` |
| `A154` | Row label/section heading | `سایر اقلام سود و زیان جامع پس از کسر مالیات ` |
| `A155` | Row label/section heading | `سود(زيان) جامع در ۱۴۰۳/۰۶/۳۱ ` |
| `A156` | Row label/section heading | `سود(زيان) سهام مصوب ` |
| `A157` | Row label/section heading | `افزایش سرمایه ` |
| `A158` | Row label/section heading | `افزایش سرمایه در جریان ` |
| `A159` | Row label/section heading | `خرید سهام خزانه ` |
| `A160` | Row label/section heading | `فروش سهام خزانه ` |
| `A161` | Row label/section heading | `سود (زیان) حاصل از فروش سهام خزانه ` |
| `A162` | Row label/section heading | `انتقال از سایر اقلام حقوق مالکانه به سود و زیان انباشته ` |
| `A163` | Row label/section heading | `تخصیص به اندوخته قانونی ` |
| `A164` | Row label/section heading | `تخصیص به سایر اندوخته‌ها ` |
| `A165` | Row label/section heading | `مانده در ۱۴۰۳/۰۶/۳۱ ` |
| `A169` | Statement/table title | `صورت جریان های نقدی` |
| `A174` | Statement/table title | `صورت جریان های نقدی` |
| `A175` | Unit note | `کلیه مبالغ به میلیون ریال است` |
| `A176` | Column header/subheader | `شرح` |
| `B176` | Column header/subheader | `دوره منتهي به ۱۴۰۳/۰۶/۳۱` |
| `C176` | Column header/subheader | `تجدید ارائه شده۱۴۰۲/۰۶/۳۱` |
| `D176` | Column header/subheader | `تجدید ارائه شده۱۴۰۲/۱۲/۲۹` |
| `E176` | Column header/subheader | `درصد تغییر` |
| `B177` | Column header/subheader | `حسابرسی نشده` |
| `C177` | Column header/subheader | `حسابرسی شده` |
| `D177` | Column header/subheader | `حسابرسی شده` |
| `A178` | Row label/section heading | `جریان­های نقدی حاصل از فعاليت‌هاي عملياتي: ` |
| `A179` | Row label/section heading | `نقد حاصل از عملیات ` |
| `A180` | Row label/section heading | `پرداخت‌های نقدی بابت مالیات بر درآمد ` |
| `E180` | Descriptive/forecast/explanatory text | `-Infinity ` |
| `A181` | Row label/section heading | `جريان ‌خالص ‌ورود‌ (خروج) ‌نقد حاصل از فعاليت‌هاي ‌عملياتي ` |
| `A182` | Row label/section heading | `فعاليت‌هاي سرمایه‌گذاری ` |
| `A183` | Row label/section heading | `وجوه پرداختي بابت تحصیل دارایی‌هاي ثابت مشهود ` |
| `A184` | Row label/section heading | `وجوه دریافتی بابت فروش دارایی‌هاي ثابت مشهود ` |
| `A185` | Row label/section heading | `وجوه پرداختي بابت تحصیل دارایی‌هاي نامشهود ` |
| `A186` | Row label/section heading | `وجوه دریافتی بابت فروش دارایی‌هاي نامشهود ` |
| `A187` | Row label/section heading | `وجوه پرداختي بابت تحصیل املاک و مستغلات غیر عملیاتی ` |
| `A188` | Row label/section heading | `وجوه دریافتی بابت فروش املاک و مستغلات غیر عملیاتی ` |
| `A189` | Row label/section heading | `جريان خالص ورود (خروج) وجه نقد ناشی از فعاليت‌هاي سرمایه‌گذاری ` |
| `A190` | Row label/section heading | `جريان خالص ورود (خروج) وجه نقد قبل از فعالیت‌های تامین مالی ` |
| `A191` | Row label/section heading | `فعاليت‌هاي تأمين مالي ` |
| `A192` | Row label/section heading | `دریافت‌های نقدی حاصل از افزايش سرمايه ` |
| `A193` | Row label/section heading | `دریافت‌های نقدی حاصل از صرف سهام ` |
| `A194` | Row label/section heading | `دریافت‌های نقدی حاصل از فروش سهام خزانه ` |
| `A195` | Row label/section heading | `پرداخت‌های نقدی برای خرید سهام خزانه ` |
| `A196` | Row label/section heading | `دریافت‌های نقدی حاصل از تسهيلات ` |
| `A197` | Row label/section heading | `پرداخت‌های نقدی بابت اصل تسهيلات ` |
| `A198` | Row label/section heading | `پرداخت‌های نقدی بابت سود تسهيلات ` |
| `A199` | Row label/section heading | `دریافت‌های نقدی حاصل از انتشار اوراق مشارکت ` |
| `A200` | Row label/section heading | `پرداخت‌های نقدی بابت اصل اوراق مشارکت ` |
| `A201` | Row label/section heading | `پرداخت‌های نقدی بابت سود اوراق مشارکت ` |
| `A202` | Row label/section heading | `دریافت‌های نقدی حاصل از انتشار اوراق خرید دین ` |
| `A203` | Row label/section heading | `پرداخت‌های نقدی بابت اصل اوراق خرید دین ` |
| `A204` | Row label/section heading | `پرداخت‌های نقدی بابت سود اوراق خرید دین ` |
| `A205` | Row label/section heading | `پرداخت‌های نقدی بابت اصل اقساط اجاره سرمایه‌ای ` |
| `A206` | Row label/section heading | `پرداخت‌های نقدی بابت سود اجاره سرمایه‌ای ` |
| `A207` | Row label/section heading | `پرداخت‌های نقدی بابت سود سهام ` |
| `A208` | Row label/section heading | `جريان خالص ورود (خروج) نقد حاصل از فعاليت‌هاي تامين مالي ` |
| `A209` | Row label/section heading | `خالص افزايش (کاهش) در موجودی نقد ` |
| `A210` | Row label/section heading | `مانده موجودی نقد در ابتدای سال ` |
| `A211` | Row label/section heading | `تاثير تغييرات نرخ ارز ` |
| `A212` | Row label/section heading | `مانده موجودی نقد در پايان سال ` |
| `A213` | Row label/section heading | `معاملات غيرنقدي ` |
| `A221` | Row label/section heading | `دلایل تغییرات اطلاعات واقعی دوره منتهی به ۱۴۰۳/۰۶/۳۱ ` |
| `A223` | Row label/section heading | `دلایل تغییرات اطلاعات واقعی دوره منتهی به ۱۴۰۲/۰۶/۳۱ ` |
| `A225` | Row label/section heading | `دلایل تغییرات اطلاعات واقعی دوره منتهی به ۱۴۰۲/۱۲/۲۹ ` |
| `A230` | Statement/table title | `خلاصه اطلاعات گزارش تفسیری - صفحه 1` |
| `A235` | Row label/section heading | `اطلاعات این فرم گزیده ای از اطلاعات گزارش تفسیری مدیریت می باشد که هیئت مدیره شرکت مطابق با مفاد دستورالعمل اجرایی افشای اطلاعات شرکتهای ثبت شده نزد سازمان موظف به ارائه آن در پیوست این اطلاعیه می باشد و این اطلاعات جایگزین گزارش مذکور نیست. ` |
| `A236` | Statement/table title | `مانده تسهیلات اعطایی و ذخیره مطالبات مشکوک الوصول:` |
| `A237` | Unit note | `کلیه مبالغ درج شده به میلیون ریال می باشد` |
| `A238` | Column header/subheader | `شرح` |
| `B238` | Column header/subheader | `در تاریخ ۱۴۰۲/۱۲/۲۹` |
| `C238` | Column header/subheader | `در تاریخ ۱۴۰۳/۰۶/۳۱` |
| `D238` | Column header/subheader | `در تاریخ ۱۴۰۲/۱۲/۲۹` |
| `E238` | Column header/subheader | `در تاریخ ۱۴۰۳/۰۶/۳۱` |
| `F238` | Column header/subheader | `در تاریخ ۱۴۰۲/۱۲/۲۹` |
| `G238` | Column header/subheader | `در تاریخ ۱۴۰۳/۰۶/۳۱` |
| `H238` | Column header/subheader | `در تاریخ ۱۴۰۲/۱۲/۲۹` |
| `I238` | Column header/subheader | `در تاریخ ۱۴۰۳/۰۶/۳۱` |
| `J238` | Column header/subheader | `در تاریخ ۱۴۰۲/۱۲/۲۹` |
| `K238` | Column header/subheader | `در تاریخ ۱۴۰۳/۰۶/۳۱` |
| `B239` | Column header/subheader | `جاری` |
| `D239` | Column header/subheader | `سررسید گذشته` |
| `F239` | Column header/subheader | `معوق` |
| `H239` | Column header/subheader | `مشکوک الوصول` |
| `J239` | Column header/subheader | `جمع` |
| `A240` | Row label/section heading | `تسهیلات اعطایی و مطالبات از اشخاص دولتی ` |
| `A241` | Row label/section heading | `تسهیلات اعطایی و مطالبات از اشخاص غیر دولتی- ریالی ` |
| `A242` | Row label/section heading | `تسهیلات اعطایی و مطالبات از اشخاص غیر دولتی- ارزی ` |
| `A243` | Row label/section heading | `جمع ` |
| `A244` | Row label/section heading | `کسر می شود: ` |
| `A245` | Row label/section heading | `سود سالهای آتی ` |
| `A246` | Row label/section heading | `سایر ` |
| `A247` | Row label/section heading | `مانده تسهیلات پایان دوره ` |
| `A248` | Row label/section heading | `ارزش وثایق دریافتی ` |
| `A249` | Row label/section heading | `مانده مبنای محاسبه ذخیره اختصاصی ` |
| `A250` | Row label/section heading | `ضریب مبنای احتساب ذخیره اختصاصی (درصد) ` |
| `A251` | Row label/section heading | `ذخیره اختصاصی مطالبات مشکوک الوصول ` |
| `A252` | Row label/section heading | `مانده مبنای محاسبه ذخیره عمومی ` |
| `A253` | Row label/section heading | `ذخیره عمومی مطالبات مشکوک الوصول ` |
| `A254` | Row label/section heading | `جمع ` |
| `A255` | Row label/section heading | `برآورد شرکت از تغییرات در نرخ سود تسهیلات اعطایی :` |
| `A256` | Row label/section heading | `دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ` |
| `C256` | Descriptive/forecast/explanatory text | `با توجه به سیاستهای پولی و بانکی انتظار در تغییر نرخ سود تسهیلات اعطایی در سال آتی پیش بینی نمی گردد. ` |
| `A258` | Row label/section heading | `برآورد شرکت از تغییرات در مانده تسهیلات :` |
| `A259` | Row label/section heading | `دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ` |
| `C259` | Descriptive/forecast/explanatory text | `با توجه به رشد منابع بانک در سال آتی پیش بینی می گردد مانده تسهیلات بانک افزایش یابد. ` |
| `A261` | Row label/section heading | `برآورد شرکت از تغییرات در مانده ذخایر مطالبات مشکوک الوصول :` |
| `A262` | Row label/section heading | `دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ` |
| `C262` | Descriptive/forecast/explanatory text | `با توجه به افزایش در حجم تسهیلات اعطایی پیش بینی می گردد مانده ذخیره مطالبات مشکوک الوصول عام افزایش و بر اساس روند وصول مطالبات ذخیره مطالبات مشکوک الوصول خاص تغییری نداشته باشد. ` |
| `A264` | Unit note | `مانده سپرده های دریافتی از مشتریان :` |
| `A265` | Column header/subheader | `کلیه مبالغ درج شده به میلیون ریال می باشد` |
| `A266` | Column header/subheader | `شرح` |
| `B266` | Column header/subheader | `مانده سپرده ها` |
| `D266` | Column header/subheader | `متوسط نرخ سود مانده سپرده ها` |
| `F266` | Column header/subheader | `برآورد مدیریت از تغییر در نرخ سود سپرده ها و تغییر در مانده سپرده های دریافتی از مشتریان` |
| `B267` | Column header/subheader | `در تاریخ ۱۴۰۲/۱۲/۲۹` |
| `C267` | Column header/subheader | `در تاریخ ۱۴۰۳/۰۶/۳۱` |
| `D267` | Column header/subheader | `در تاریخ ۱۴۰۲/۱۲/۲۹` |
| `E267` | Column header/subheader | `در تاریخ ۱۴۰۳/۰۶/۳۱` |
| `A268` | Row label/section heading | `سپرده های ریالی: ` |
| `A269` | Row label/section heading | `سپرده های کوتاه مدت ` |
| `F269` | Descriptive/forecast/explanatory text | `با توجه به سیاستهای پولی و بانکی تغییری درنرخ سود سپرده ها پیش بینی نمی گردد. ` |
| `A270` | Row label/section heading | `سپرده های کوتاه مدت ویژه ` |
| `F270` | Descriptive/forecast/explanatory text | `با توجه به سیاستهای پولی و بانکی تغییری درنرخ سود سپرده ها پیش بینی نمی گردد. ` |
| `A271` | Row label/section heading | `سپرده های بلند مدت ` |
| `F271` | Descriptive/forecast/explanatory text | `با توجه به سیاستهای پولی و بانکی تغییری درنرخ سود سپرده ها پیش بینی نمی گردد. ` |
| `A272` | Row label/section heading | `جمع سپرده های هزینه زا ` |
| `A273` | Row label/section heading | `سپرده های غیر هزینه زا ` |
| `F273` | Descriptive/forecast/explanatory text | `با توجه به سیاستهای پولی و بانکی تغییری درنرخ سود سپرده ها پیش بینی نمی گردد. ` |
| `A274` | Row label/section heading | `جمع سپرده های ریالی ` |
| `A275` | Row label/section heading | `سپرده های ارزی ` |
| `F275` | Descriptive/forecast/explanatory text | `با توجه به سیاستهای پولی و بانکی تغییری درنرخ سود سپرده ها پیش بینی نمی گردد. ` |
| `A276` | Row label/section heading | `جمع سپرده های دریافتی ` |
| `A277` | Row label/section heading | `اقلام زیر خط:` |
| `A278` | Unit note | `کلیه مبالغ درج شده به میلیون ریال می باشد` |
| `A279` | Column header/subheader | `شرح` |
| `B279` | Column header/subheader | `۱۴۰۳/۰۶/۳۱` |
| `C279` | Column header/subheader | `۱۴۰۲/۱۲/۲۹` |
| `D279` | Column header/subheader | `شرح` |
| `E279` | Column header/subheader | `۱۴۰۳/۰۶/۳۱` |
| `F279` | Column header/subheader | `۱۴۰۲/۱۲/۲۹` |
| `A280` | Column header/subheader | `تعهدات مشتریان بابت اعتبارات اسنادی ` |
| `D280` | Column header/subheader | `تعهدات بانک بابت اعتبارات اسنادی ` |
| `A281` | Row label/section heading | `تعهدات مشتریان بابت ضمانت نامه های صادره ` |
| `D281` | Descriptive/forecast/explanatory text | `تعهدات بانک بابت ضمانت نامه های صادره ` |
| `A282` | Row label/section heading | `ساير تعهدات مشتريان بانک ` |
| `D282` | Descriptive/forecast/explanatory text | `سایر تعهدات بانک ` |
| `A283` | Row label/section heading | `وجوه اداره شده و موارد مشابه ` |
| `D283` | Descriptive/forecast/explanatory text | `وجوه اداره شده و موارد مشابه ` |
| `A284` | Row label/section heading | `توضیحات در خصوص تغییرات بااهمیت: ` |
| `A285` | Row label/section heading | `«جملات آینده‌نگر نشان‌دهنده انتظارات، باورها یا پیش‌بینی‌های جاری از رویدادها و عملکرد مالی است. این جملات در معرض ریسک‌ها، عدم‌قطعیت‌ها و مفروضات غیرقطعی قرار دارند. بنابراین نتایج واقعی ممکن است متفاوت از نتایج مورد انتظار باشند.» ` |
| `A289` | Statement/table title | `خلاصه اطلاعات گزارش تفسیری - صفحه 2` |
| `A294` | Row label/section heading | `اطلاعات این فرم گزیده ای از اطلاعات گزارش تفسیری مدیریت می باشد که هیئت مدیره شرکت مطابق با مفاد دستورالعمل اجرایی افشای اطلاعات شرکتهای ثبت شده نزد سازمان موظف به ارائه آن در پیوست این اطلاعیه می باشد و این اطلاعات جایگزین گزارش مذکور نیست. ` |
| `A295` | Row label/section heading | `وضعیت کارکنان:` |
| `A296` | Unit note | `کلیه مبالغ درج شده به میلیون ریال می باشد` |
| `A297` | Column header/subheader | `شرح` |
| `B297` | Column header/subheader | `در تاریخ ۱۴۰۲/۱۲/۲۹` |
| `C297` | Column header/subheader | `در تاریخ ۱۴۰۳/۰۶/۳۱` |
| `D297` | Column header/subheader | `برآورد در تاریخ ۱۴۰۳/۱۲/۳۰` |
| `A298` | Row label/section heading | `تعداد شعب ` |
| `A299` | Row label/section heading | `تعداد کارکنان ` |
| `A300` | Row label/section heading | `اطلاعات حق الوکاله و کفایت سرمایه` |
| `A301` | Unit note | `کلیه مبالغ درج شده به میلیون ریال می باشد` |
| `A302` | Column header/subheader | `شرح` |
| `B302` | Column header/subheader | `سال مالی منتهی به۱۴۰۲/۱۲/۲۹` |
| `C302` | Column header/subheader | `دوره ۶ ماهه منتهی به ۱۴۰۳/۰۶/۳۱` |
| `D302` | Column header/subheader | `برآورد تغییر روند در دوره ۶ ماهه منتهی به ۱۴۰۳/۱۲/۳۰` |
| `A303` | Row label/section heading | `سهم بانک از درآمدهای مشاع ` |
| `D303` | Descriptive/forecast/explanatory text | `------------------------------------------------------------- ` |
| `A304` | Row label/section heading | `سهم سپرده گذاران از درآمدهای مشاع ` |
| `D304` | Descriptive/forecast/explanatory text | `------------------------------------------------------------- ` |
| `A305` | Row label/section heading | `نرخ حق الوکاله اعلام شده ` |
| `D305` | Descriptive/forecast/explanatory text | `------------------------------------------------------------- ` |
| `A306` | Row label/section heading | `مبلغ حق الوکاله اعمال شده ` |
| `D306` | Descriptive/forecast/explanatory text | `------------------------------------------------------------- ` |
| `A307` | Row label/section heading | `مابه التفاوت سود قابل پرداخت (مازاد سود پرداختی) به سپرده گذاران ` |
| `D307` | Descriptive/forecast/explanatory text | `------------------------------------------------------------- ` |
| `A308` | Row label/section heading | `نسبت کفایت سرمایه ` |
| `D308` | Descriptive/forecast/explanatory text | `------------------------------------------------------------- ` |
| `A309` | Row label/section heading | `اهداف و راهبردهای آتی مدیریت در خصوص فعالیت شرکت:` |
| `A310` | Row label/section heading | `اهداف و راهبردهای آتی مدیریت در خصوص فعالیت شرکت: ` |
| `B310` | Descriptive/forecast/explanatory text | `-------------------------------------------------------------------- ` |
| `A311` | Row label/section heading | `درآمد حاصل از تسهيلات اعطايي و سپرده گذاري` |
| `A312` | Unit note | `کلیه مبالغ درج شده به میلیون ریال می باشد` |
| `A313` | Column header/subheader | `شرح` |
| `B313` | Column header/subheader | `سال مالی منتهی به ۱۴۰۲/۱۲/۲۹` |
| `C313` | Column header/subheader | `متوسط نرخ سود سال مالی منتهی به ۱۴۰۲/۱۲/۲۹ (درصد)` |
| `D313` | Column header/subheader | `دوره ۶ ماهه منتهی به ۱۴۰۳/۰۶/۳۱` |
| `E313` | Column header/subheader | `متوسط نرخ سود دوره ۶ ماهه منتهی به ۱۴۰۳/۰۶/۳۱ (درصد)` |
| `F313` | Column header/subheader | `برآورد تغییر روند در دوره ۶ ماهه منتهی به ۱۴۰۳/۱۲/۳۰` |
| `A314` | Row label/section heading | `درآمد تسهیلات اعطایی: ` |
| `A315` | Row label/section heading | `فروش اقساطی ` |
| `F315` | Descriptive/forecast/explanatory text | `مبلغ درآمدسرمایه گذاریهای بانک درسال۱۴۰۳باافزایش مواجه گردد ` |
| `A316` | Row label/section heading | `جعاله ` |
| `F316` | Descriptive/forecast/explanatory text | `مبلغ درآمدسرمایه گذاریهای بانک درسال۱۴۰۳باافزایش مواجه گردد ` |
| `A317` | Row label/section heading | `اجاره به شرط تملیک ` |
| `F317` | Descriptive/forecast/explanatory text | `مبلغ درآمدسرمایه گذاریهای بانک درسال۱۴۰۳باافزایش مواجه گردد ` |
| `A318` | Row label/section heading | `سلف ` |
| `F318` | Descriptive/forecast/explanatory text | `مبلغ درآمدسرمایه گذاریهای بانک درسال۱۴۰۳باافزایش مواجه گردد ` |
| `A319` | Row label/section heading | `مضاربه ` |
| `F319` | Descriptive/forecast/explanatory text | `مبلغ درآمدسرمایه گذاریهای بانک درسال۱۴۰۳باافزایش مواجه گردد ` |
| `A320` | Row label/section heading | `مشارکت مدنی ` |
| `F320` | Descriptive/forecast/explanatory text | `مبلغ درآمدسرمایه گذاریهای بانک درسال۱۴۰۳باافزایش مواجه گردد ` |
| `A321` | Row label/section heading | `خرید دین ` |
| `F321` | Descriptive/forecast/explanatory text | `مبلغ درآمدسرمایه گذاریهای بانک درسال۱۴۰۳باافزایش مواجه گردد ` |
| `A322` | Row label/section heading | `بدهکاران بابت اعتبارات اسنادی پرداخت شده ` |
| `F322` | Descriptive/forecast/explanatory text | `مبلغ درآمدسرمایه گذاریهای بانک درسال۱۴۰۳باافزایش مواجه گردد ` |
| `A323` | Row label/section heading | `بدهکاران بابت ضمانت نامه های پرداخت شده ` |
| `F323` | Descriptive/forecast/explanatory text | `مبلغ درآمدسرمایه گذاریهای بانک درسال۱۴۰۳باافزایش مواجه گردد ` |
| `A324` | Row label/section heading | `تسهیلات ارزی ` |
| `F324` | Descriptive/forecast/explanatory text | `مبلغ درآمدسرمایه گذاریهای بانک درسال۱۴۰۳باافزایش مواجه گردد ` |
| `A325` | Row label/section heading | `تسهیلات قرض الحسنه ` |
| `F325` | Descriptive/forecast/explanatory text | `مبلغ درآمدسرمایه گذاریهای بانک درسال۱۴۰۳باافزایش مواجه گردد ` |
| `A326` | Row label/section heading | `سایر درآمد تسهیلات اعطایی ` |
| `F326` | Descriptive/forecast/explanatory text | `مبلغ درآمدسرمایه گذاریهای بانک درسال۱۴۰۳باافزایش مواجه گردد ` |
| `A327` | Row label/section heading | `جمع درآمد حاصل از تسهیلات اعطایی ` |
| `F327` | Descriptive/forecast/explanatory text | `مبلغ درآمدسرمایه گذاریهای بانک درسال۱۴۰۳باافزایش مواجه گردد ` |
| `A328` | Row label/section heading | `جایزه سپرده قانونی ` |
| `F328` | Descriptive/forecast/explanatory text | `مبلغ درآمدسرمایه گذاریهای بانک درسال۱۴۰۳باافزایش مواجه گردد ` |
| `A329` | Row label/section heading | `سود حاصل از سپرده گذاری در بانکها ` |
| `F329` | Descriptive/forecast/explanatory text | `مبلغ درآمدسرمایه گذاریهای بانک درسال۱۴۰۳باافزایش مواجه گردد ` |
| `A330` | Row label/section heading | `جمع سود حاصل از سپرده گذاری ها ` |
| `F330` | Descriptive/forecast/explanatory text | `مبلغ درآمدسرمایه گذاریهای بانک درسال۱۴۰۳باافزایش مواجه گردد ` |
| `A331` | Row label/section heading | `درآمد اوراق بدهی و سایر درآمدهای ناشی از سپرده گذاری ` |
| `F331` | Descriptive/forecast/explanatory text | `مبلغ درآمدسرمایه گذاریهای بانک درسال۱۴۰۳باافزایش مواجه گردد ` |
| `A332` | Row label/section heading | `درآمد حاصل ازتسهیلات اعطایی و سپرده‌گذاری‌ها ` |
| `F332` | Descriptive/forecast/explanatory text | `مبلغ درآمدسرمایه گذاریهای بانک درسال۱۴۰۳باافزایش مواجه گردد ` |
| `A333` | Row label/section heading | `ارائه توضیحات در خصوص نحوه محاسبه متوسط نرخ سود تسهیلات: ` |
| `C333` | Descriptive/forecast/explanatory text | `------------------------------------------------------------------------------------- ` |
| `A334` | Row label/section heading | `خالص سود (زیان) سرمایه گذاری‌ ها` |
| `A335` | Unit note | `کلیه مبالغ درج شده به میلیون ریال می باشد` |
| `A336` | Column header/subheader | `شرح` |
| `B336` | Column header/subheader | `سال مالی منتهی به۱۴۰۲/۱۲/۲۹` |
| `C336` | Column header/subheader | `دوره ۶ ماهه منتهی به ۱۴۰۳/۰۶/۳۱` |
| `D336` | Column header/subheader | `برآورد تغییر روند در دوره ۶ ماهه منتهی به ۱۴۰۳/۱۲/۳۰` |
| `A337` | Row label/section heading | `درآمد حاصل از سرمایه گذاری در سهام ` |
| `D337` | Descriptive/forecast/explanatory text | `مبلغ درآمدسرمایه گذاریهای بانک درسال ۱۴۰۳ باافزایش مواجه گردد ` |
| `A338` | Row label/section heading | `سود(زیان) حاصل از فروش سرمایه گذاری ` |
| `D338` | Descriptive/forecast/explanatory text | `مبلغ درآمدسرمایه گذاریهای بانک درسال ۱۴۰۳ باافزایش مواجه گردد ` |
| `A339` | Row label/section heading | `سود (زیان) تعدیل ذخیره کاهش ارزش سرمایه گذاریها ` |
| `D339` | Descriptive/forecast/explanatory text | `مبلغ درآمدسرمایه گذاریهای بانک درسال ۱۴۰۳ باافزایش مواجه گردد ` |
| `A340` | Row label/section heading | `جمع درآمدهای حاصل از سرمایه گذاری ` |
| `D340` | Descriptive/forecast/explanatory text | `مبلغ درآمدسرمایه گذاریهای بانک درسال ۱۴۰۳ باافزایش مواجه گردد ` |
| `A341` | Row label/section heading | `«جملات آینده‌نگر نشان‌دهنده انتظارات، باورها یا پیش‌بینی‌های جاری از رویدادها و عملکرد مالی است. این جملات در معرض ریسک‌ها، عدم‌قطعیت‌ها و مفروضات غیرقطعی قرار دارند. بنابراین نتایج واقعی ممکن است متفاوت از نتایج مورد انتظار باشند.» ` |
| `A345` | Statement/table title | `خلاصه اطلاعات گزارش تفسیری - صفحه 3` |
| `A350` | Row label/section heading | `اطلاعات اين فرم گزيده اي از اطلاعات گزارش تفسيري مديريت مي باشد که هيئت مديره شرکت مطابق با مفاد دستورالعمل اجرايي افشاي اطلاعات شرکتهاي ثبت شده نزد سازمان موظف به ارائه آن در پيوست اين اطلاعيه مي باشد و اين اطلاعات جايگزين گزارش مذکور نيست. ` |
| `A351` | Row label/section heading | `وضعیت شرکتهای سرمایه پذیر:` |
| `A352` | Unit note | `کلیه مبالغ درج شده به میلیون ریال می باشد` |
| `A353` | Column header/subheader | `نام شرکت` |
| `C353` | Column header/subheader | `سال مالي منتهي به ۱۴۰۲/۱۲/۲۹` |
| `G353` | Column header/subheader | `دوره ۶ ماهه منتهي به ۱۴۰۳/۰۶/۳۱` |
| `J353` | Column header/subheader | `تشريح آخرين وضعيت و برنامه هاي آتي شرکت در شرکت سرمايه پذير` |
| `C354` | Column header/subheader | `درصد مالکيت` |
| `D354` | Column header/subheader | `بهاي تمام شده` |
| `E354` | Column header/subheader | `سال مالي شرکت سرمايه پذير` |
| `F354` | Column header/subheader | `درآمد سرمايه گذاري` |
| `G354` | Column header/subheader | `درصد مالکيت` |
| `H354` | Column header/subheader | `بهاي تمام شده` |
| `I354` | Column header/subheader | `درآمد سرمايه گذاري` |
| `A355` | Row label/section heading | `صرافي پارسيان ` |
| `E355` | Descriptive/forecast/explanatory text | `۱۴۰۲/۱۰/۳۰ ` |
| `J355` | Descriptive/forecast/explanatory text | `سود نقدی سرمایه گذاری ها تا پایان سال جاری نسبت به سال ۱۴۰۳ افزایش می یابد ` |
| `A356` | Row label/section heading | `ساير شرکتهاي خارج از بورس ` |
| `E356` | Descriptive/forecast/explanatory text | `۱۴۰۲/۱۰/۳۰ ` |
| `J356` | Descriptive/forecast/explanatory text | `سود نقدی سرمایه گذاری ها تا پایان سال جاری نسبت به سال ۱۴۰۳ افزایش می یابد ` |
| `A357` | Row label/section heading | `گروه داده پردازي پارسيان ` |
| `E357` | Descriptive/forecast/explanatory text | `۱۴۰۲/۱۰/۳۰ ` |
| `J357` | Descriptive/forecast/explanatory text | `سود نقدی سرمایه گذاری ها تا پایان سال جاری نسبت به سال ۱۴۰۳ افزایش می یابد ` |
| `A358` | Row label/section heading | `گروه مالي بانک پارسيان ` |
| `E358` | Descriptive/forecast/explanatory text | `۱۴۰۲/۱۰/۳۰ ` |
| `J358` | Descriptive/forecast/explanatory text | `سود نقدی سرمایه گذاری ها تا پایان سال جاری نسبت به سال ۱۴۰۳ افزایش می یابد ` |
| `A359` | Row label/section heading | `ساير درآمدها و هزینه های عملياتي:` |
| `A360` | Unit note | `کلیه مبالغ درج شده به میلیون ریال می باشد` |
| `A361` | Column header/subheader | `شرح` |
| `B361` | Column header/subheader | `۱۴۰۲/۱۲/۲۹` |
| `C361` | Column header/subheader | `۱۴۰۳/۰۶/۳۱` |
| `A362` | Row label/section heading | `ساير درآمدهاي عملياتي: ` |
| `A363` | Row label/section heading | `ساير درآمدهاي عملياتي ` |
| `A365` | Row label/section heading | `جمع ساير درآمدهاي عملياتي ` |
| `A366` | Row label/section heading | `ساير هزينه هاي عملياتي: ` |
| `A367` | Row label/section heading | `ساير هزينه هاي عملياتي ` |
| `A369` | Row label/section heading | `جمع ساير هزينه هاي عملياتي ` |
| `A370` | Row label/section heading | `جمع ساير درآمدها و هزينه هاي عملياتي ` |
| `A371` | Row label/section heading | `برآورد شرکت از تغییرات خالص سایر درآمدها (هزینه ها)ی عملیاتی:` |
| `A372` | Row label/section heading | `دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ` |
| `C372` | Descriptive/forecast/explanatory text | `--------------------------------------------------------------------------- ` |
| `A374` | Row label/section heading | `خالص ساير درآمدها و هزینه ها:` |
| `A375` | Unit note | `کلیه مبالغ درج شده به میلیون ریال می باشد` |
| `A376` | Column header/subheader | `خالص ساير درآمدها و هزينه ها` |
| `B376` | Column header/subheader | `۱۴۰۲/۱۲/۲۹` |
| `C376` | Column header/subheader | `۱۴۰۳/۰۶/۳۱` |
| `A377` | Row label/section heading | `ساير درامدها ` |
| `A378` | Row label/section heading | `ساير هزينه ها ` |
| `A380` | Row label/section heading | `جمع خالص ساير درآمدها و هزينه ها ` |
| `A381` | Row label/section heading | `برآورد شرکت از تغییرات خالص ساير درآمدها و هزینه ها :` |
| `A382` | Row label/section heading | `دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ` |
| `C382` | Descriptive/forecast/explanatory text | `-------------------------------------------------------------------------------- ` |
| `A384` | Row label/section heading | `هزینه های اداری و عمومی:` |
| `A385` | Unit note | `کلیه مبالغ درج شده به میلیون ریال می باشد` |
| `A386` | Column header/subheader | `هزينه هاي اداري و عمومي` |
| `B386` | Column header/subheader | `۱۴۰۲/۱۲/۲۹` |
| `C386` | Column header/subheader | `۱۴۰۳/۰۶/۳۱` |
| `A387` | Row label/section heading | `هزينه هاي اداري و عمومي ` |
| `A389` | Row label/section heading | `جمع هزينه هاي اداري و عمومي ` |
| `A390` | Row label/section heading | `برآورد شرکت از تغییرات هزینه های اداری و عمومی :` |
| `A391` | Row label/section heading | `دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ` |
| `C391` | Descriptive/forecast/explanatory text | `-------------------------------------------------------------------------------- ` |
| `A393` | Row label/section heading | `هزینه مالی:` |
| `A394` | Unit note | `کلیه مبالغ درج شده به میلیون ریال می باشد` |
| `A395` | Column header/subheader | `هزينه‌هاي مالي` |
| `B395` | Column header/subheader | `۱۴۰۲/۱۲/۲۹` |
| `C395` | Column header/subheader | `۱۴۰۳/۰۶/۳۱` |
| `A396` | Row label/section heading | `هزينه مالي تسهيلات دريافتي از ساير بانکها و موسسات اعتباري ` |
| `A397` | Row label/section heading | `جريمه اضافه برداشت از بانک مرکزي ` |
| `A398` | Row label/section heading | `ساير هزينه هاي مالي ` |
| `A399` | Row label/section heading | `جمع هزينه‌هاي مالي ` |
| `A400` | Row label/section heading | `برآورد شرکت از تغییرات هزینه های مالی :` |
| `A401` | Row label/section heading | `دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ` |
| `C401` | Descriptive/forecast/explanatory text | `---------------------------------------------------------------------------------------- ` |
| `A403` | Row label/section heading | `برنامه شرکت در خصوص تقسیم سود` |
| `A404` | Column header/subheader | `مبلغ سود (زيان) انباشته پايان سال مالي گذشته` |
| `B404` | Column header/subheader | `سود سهام پيشنهادي هيئت مديره در سال مالي گذشته` |
| `C404` | Column header/subheader | `مبلغ سود (زيان) خالص سال مالي گذشته` |
| `D404` | Column header/subheader | `سود سهام مصوب مجمع سال مالي گذشته` |
| `E404` | Column header/subheader | `پيشنهاد هيئت مديره درخصوص درصد تقسيم سود سال مالي جاري` |
| `A406` | Row label/section heading | `سایر برنامه های با اهمیت شرکت` |
| `A407` | Row label/section heading | `دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ` |
| `B407` | Descriptive/forecast/explanatory text | `-------------------------------------------------------------------- ` |
| `A409` | Row label/section heading | `سایر توضیحات با اهمیت` |
| `A410` | Row label/section heading | `---------------------------------------------------------------------------------------------------------------------- ` |
| `A411` | Row label/section heading | `«جملات آينده‌نگر نشان‌دهنده انتظارات، باورها يا پيش‌بيني‌هاي جاري از رويدادها و عملکرد مالي است. اين جملات در معرض ريسک‌ها، عدم‌قطعيت‌ها و مفروضات غيرقطعي قرار دارند. بنابراين نتايج واقعي ممکن است متفاوت از نتايج مورد انتظار باشند.» ` |
