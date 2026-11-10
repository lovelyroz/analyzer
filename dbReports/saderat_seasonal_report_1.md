# Saderat Fiscal-Year Periodic Financial Report Workbook Inspection — DB-STD-003

## 1. Executive summary

`excel/saderat_seasonal.xlsx` is a one-sheet, Persian-language interim financial workbook for **شرکت بانک صادرات ایران** (Bank Saderat Iran), based on the title metadata and the directors' disclosure. The workbook identifies the report as audited interim financial statements for the six months ended **۱۴۰۳/۰۳/۳۱**. The title does not show a ticker. The workbook presents five financial statements and a board-members disclosure. Amounts in the principal financial statements are labeled million rials; earnings-per-share rows are explicitly in rials. The complete string-cell source-label inventory is included below.

The statement columns are not temporally uniform. Income, comprehensive income, and cash flows show the current six-month period, a restated corresponding six-month period, and a restated full-year comparative ended ۱۴۰۲/۰۹/۳۰, followed by a percentage-change column. The balance sheet instead compares three dates. Equity changes expose the fiscal-year opening date ۱۴۰۱/۱۰/۰۱, the year-end ۱۴۰۲/۰۹/۳۰, and the current six-month movement to ۱۴۰۳/۰۳/۳۱. This is strong evidence that the fiscal year begins ۱۴۰۱/۱۰/۰۱ and ends ۱۴۰۲/۰۹/۳۰ in the comparative cycle, but the report does not state a general fiscal calendar rule. No standalone-quarter amounts are explicitly labeled or separable from the reported six-month figures, so none are calculated.

No code, schema, migration, test, monthly standard, master document, or source workbook was changed. Only this inspection report was created.

## Terminology alignment with DB-STD-003

This workbook is classified under **Fiscal-Year Periodic Financial Reports** (Persian: «گزارش‌های مالی دوره‌ای سال مالی (تجمعی)»). It is the six-month (۱۴۰۳/۰۳/۳۱) member of that reporting family. The family covers reports issued at fiscal-year checkpoints such as 3, 6, 9, and 12 months; the 12-month member is the annual report, not an interim report.

“Cumulative/YTD” describes the temporal basis of applicable flow values (for example, income and cash flows), not every value in the workbook. Balance-sheet values remain point-in-time balances at their stated dates. A report’s periodic family classification therefore does not by itself determine the temporal meaning of each table column.

## 2. Workbook and worksheet inventory

| Property | Observed evidence |
|---|---|
| File / format | `excel/saderat_seasonal.xlsx`, 25,645 bytes, Excel workbook (`.xlsx`). |
| Worksheets | One sheet, in order: `Recovered_Sheet1` (visible). No hidden worksheet was found. |
| Used range / dimensions | `A1:L262` (262 rows × 12 columns); much of the range is blank spacing or merged statement headings. |
| Workbook properties | Title: `صورت‌های مالی میاندوره‌ای 6 ماهه منتهی به 1403/03/31 (حسابرسی شده)`; creator `Papa`; subject empty; created/modified metadata 2026-11-10. File metadata dates describe the workbook file, not the report publication date. |
| Structural features | 30 merged ranges, including statement headings and split two-row labels in the directors table; no formulas, defined names, Excel tables, or freeze panes found. No charts or images were detected. |
| Contents | One workbook containing five financial statements and one supplementary directors/board table, rather than multiple separate reports. |

Merged ranges are recorded in the workbook but are not individually material to the financial interpretation beyond the multi-row headings and board-table labels. The source-cell appendix records the text-bearing cells exactly as loaded from the workbook.

## 3. Report identity and period evidence

| Question | Finding and evidence |
|---|---|
| Company | The board disclosure names `بانک صادرات ایران` at `Recovered_Sheet1!A262`; workbook title gives the interim report context. The identity is therefore supported by workbook content. |
| Ticker | No ticker symbol was found in the title, statement labels, or board disclosure. |
| Report type | Workbook title states `صورت‌های مالی میاندوره‌ای 6 ماهه ... (حسابرسی شده)`; statement headings include income, comprehensive income, financial position, changes in equity, and cash flows. This supports audited six-month interim financial statements. |
| Current reporting endpoint | `۱۴۰۳/۰۳/۳۱` appears in the title and current-period headers (`B10`, `B56`, `B191`) and the balance-sheet date (`B83`). Dates are preserved in Jalali form. |
| Fiscal-year evidence | The equity statement identifies `مانده در ۱۴۰۱/۱۰/۰۱` (`A148`) and changes through `۱۴۰۲/۰۹/۳۰` (`A152`, `A167`), then changes in the six-month period ending `۱۴۰۳/۰۳/۳۱` (`A168`–`A180`). This supports a fiscal cycle beginning on ۱۴۰۱/۱۰/۰۱ and ending on ۱۴۰۲/۰۹/۳۰ for the prior year. The workbook does not separately declare a general fiscal-year policy. |
| Comparative periods | Income and cash-flow headers have restated ۱۴۰۲/۰۳/۳۱ and ۱۴۰۲/۰۹/۳۰ columns (`C10:D10`, `C191:D191`); comprehensive income has the same (`C56:D56`). Financial position has restated dates ۱۴۰۲/۰۹/۳۰ and ۱۴۰۱/۱۰/۰۱ (`C83:D83`). Equity statement explicitly shows opening, prior-year activity, and current six-month activity. |
| Publication date | Not established. Workbook creation/modification metadata is 2026-11-10 and is not evidence of publication. |

The phrase “دوره منتهي به” is not used alone to assign duration. The current six-month duration is evidenced directly by the workbook title and equity movement header (`A168`). The comparative date ۱۴۰۲/۰۳/۳۱ is treated as the corresponding six-month period by its date alignment and the equity statement's annual schedule; the ۱۴۰۲/۰۹/۳۰ comparative is treated as the prior full fiscal year because the equity statement labels changes for the year ending then (`A152`–`A167`).

## 4. Financial statement and major-table inventory

| Sheet / location | Statement or table and exact title cells | Rows / columns and units | Contents and notes |
|---|---|---|---|
| `Recovered_Sheet1!A3:E44` | Income statement: `صورت سود و زیان` (`A3`, repeated `A8`) | Main header `A10:E11`; line items `A12:A38`; million rials (`A9`). EPS rows `A31:A37` explicitly say rials. | Revenue, cost of revenue, gross and operating profit, finance/tax/non-operating items, discontinued operations, EPS and capital. Explanatory-change headings at `A40`, `A42`, `A44`; no explanatory text was populated beneath them. `E` is percentage change, not money. |
| `Recovered_Sheet1!A49:E71` | Comprehensive income: `صورت سود و زیان جامع` (`A49`, repeated `A54`) | Header `A56:E57`; rows `A58:A70`; million rials (`A55`). | Net income, OCI items that will/will not be reclassified, tax on those items, totals. Explanatory heading at `A71`; no accompanying explanation text was populated. |
| `Recovered_Sheet1!A76:E136` | Statement of financial position: `صورت وضعیت مالی` (`A76`, repeated `A81`) | Header `A83:E84`; line items `A85:A136`; million rials (`A82`). | Assets, equity, liabilities, subtotals and totals; three point-in-time columns and percentage change. Blank row labels with numeric totals at `B101:E101` and `B132:E132` need interpretation. |
| `Recovered_Sheet1!A140:L180` | Statement of changes in equity: `صورت تغییرات در حقوق مالکانه` (`A140`, repeated `A145`) | Unit at `A146`; column headers `A147:L147`; rows `A148:A180`; million rials. | Opening balances, prior-year restatement and movements, then six-month current-period changes. No separate period-value column headers: periods are encoded in row labels. |
| `Recovered_Sheet1!A184:E243` | Cash-flow statement: `صورت جریان های نقدی` (`A184`, repeated `A189`) | Header `A191:E192`; rows `A193:A238`; million rials (`A190`). | Operating, investing, and financing cash flows, cash reconciliation, exchange-rate effect, noncash transactions. Explanatory-change headings at `A239`, `A241`, `A243`, with no explanation text populated. |
| `Recovered_Sheet1!A248:K262` | Board/directors disclosure: `اعضاي هيئت مديره` (`A248`) | Two-row headers `A257:K258`; values in `A260:K262`; unit note says amounts in million rials (`A253`), though the table primarily contains names, IDs and descriptive attributes. | Three director/member records; personal/company identifiers, role, employment status, education and field. This is supplementary descriptive information, not a financial statement. |

There are no populated narrative footnotes in the visible statement note blocks. The “reasons for changes” rows are labels only; their merged spaces below/around them contain no explanatory text. The supplementary directors table includes personal identifiers; those values are not repeated in this report because they are not needed to interpret the financial statements.

## 5. Complete source Header inventory

The full inventory of every non-empty text cell is provided in **Appendix A**, with exact cell address, exact source text, and contextual classification. This includes statement titles, units, column headers, row labels, section headings, notes/reason headings, and all text labels in the directors table. Numeric observations are not source Headers and are not duplicated as labels. Blank-label numeric rows at `B101:E101` and `B132:E132` are called out as unresolved instead of inventing a Header.

## 6. Temporal classification matrix

| Statement / exact headers | Columns or rows | Classification | Evidence and limitation |
|---|---|---|---|
| Income, `B10` `دوره منتهي به ۱۴۰۳/۰۳/۳۱` | B | Current six-month period, likely fiscal YTD | Six-month title; equity activity covers six months through the same endpoint (`A168`–`A180`). Standalone quarter is not supplied. |
| Income, `C10` `تجديد ارائه شده دوره منتهي به ۱۴۰۲/۰۳/۳۱` | C | Restated comparative six-month period | Same Jalali endpoint month/day one year earlier and annual equity schedule; report does not separately say “six-month” in this header. |
| Income, `D10` `تجديد ارائه شده دوره منتهي به ۱۴۰۲/۰۹/۳۰` | D | Restated prior full fiscal year | Equity statement labels changes for year ended ۱۴۰۲/۰۹/۳۰ (`A152`–`A167`); duration differs from B and C. |
| Income, `E10` `درصد تغيير` | E | Derived percentage comparison | Percentage values; observed values align with B compared with C (e.g. revenue 2,161,199 vs 1,614,748 yields about 34%). Not a monetary value column. |
| Comprehensive income, `B56:D56` | B, C, D | Same three period classes as income statement | Net income ties to income statement row 30 for each respective period (`A30`, `A58`). |
| Comprehensive income, `E56` `درصد تغيير` | E | Derived percentage comparison | E58/E70 are percentage-type values; no calculation of source values made. |
| Financial position, `B83` `به تاريخ ۱۴۰۳/۰۳/۳۱` | B | Closing point-in-time balance | Reporting date. |
| Financial position, `C83` `تجديد ارائه شده به تاريخ ۱۴۰۲/۰۹/۳۰` | C | Restated prior fiscal-year-end balance | Explicit date and “restated” wording. |
| Financial position, `D83` `تجديد ارائه شده به تاريخ ۱۴۰۱/۱۰/۰۱` | D | Restated opening point-in-time balance | Explicit opening date also appears in equity opening balance (`A148`). This is not a prior-year-end comparative. |
| Financial position, `E83` `درصد تغيير` | E | Derived percentage comparison | Percentage values, apparently comparing B with C; blank where unavailable. D is an additional opening balance, not the comparison basis inferred for E. |
| Changes in equity, `A148` `مانده در ۱۴۰۱/۱۰/۰۱` | Row 148 | Opening balance at fiscal-year start | Explicit date. |
| Changes in equity, `A149:A151` | Rows 149–151 | Restatement adjustments and restated opening balance | Labels identify correction of errors, accounting-policy changes, and restated opening balance. Values shown in the equity columns. |
| Changes in equity, `A152:A167` | Rows 152–167 | Movements during prior fiscal year through ۱۴۰۲/۰۹/۳۰ and closing balance | Period encoded in row labels, including reported/restated net income and ending restated balance. |
| Changes in equity, `A168:A180` | Rows 168–180 | Movement during current six-month period and closing balance | `A168` explicitly says six months ended ۱۴۰۳/۰۳/۳۱; `A180` is the closing balance at that date. |
| Cash flow, `B191` | B | Current six-month period | Six-month title and equity-period evidence. It is not an explicitly standalone quarter. |
| Cash flow, `C191` | C | Restated comparative six-month period | Header date ۱۴۰۲/۰۳/۳۱; corresponding period interpretation supported by dates and equity history. |
| Cash flow, `D191` | D | Restated prior full fiscal year | Date ۱۴۰۲/۰۹/۳۰ and annual equity schedule. |
| Cash flow, `E191` | E | Derived percentage comparison | Percentage-change values, apparently B vs C. Text `--` appears where no percentage is shown. |
| Cash flow, `B235:E237` | Cash reconciliation rows | Period-specific beginning/end cash and derived net movement | B opening cash 13,477 + net increase 69,262 = ending 82,739; C and D show their own comparative movements. `A235` says “beginning of year”; comparative duration basis should be confirmed for C/D. |
| Directors table, `A260:K262` | Descriptive fields | Point-in-time/identity and descriptive data | No financial reporting-period header is attached to the table. |

No standalone-quarter values were calculated. A six-month YTD total could theoretically comprise two quarters, but this workbook does not provide the first-quarter cumulative figure or a standalone quarter column from which to isolate a quarter.

## 7. Financial nature and row hierarchy

| Statement | Structure and financial nature |
|---|---|
| Income statement | Flows over periods: revenue (`A13`), cost of revenue (`A14`), expenses (`A16:A19`, `A21`, `A25:A26`), non-operating income/expense (`A22`), and discontinued/continuing operations. Subtotals/totals include gross profit (`A15`), operating profit (`A20`), continuing profit before tax (`A23`), continuing net profit (`A27`), net profit (`A30`). EPS (`A32:A37`) is per-share/derived disclosure; capital (`A38`) is a stock-like corporate amount, though the exact temporal convention for this row is not stated. |
| Comprehensive income | Period flows/derived totals: net profit (`A58`), OCI categories (`A60:A68`), after-tax OCI (`A69`), comprehensive income (`A70`). Section headings at `A59` and `A65` divide items by whether they may be reclassified into profit or loss in future periods. |
| Financial position | Point-in-time stocks: noncurrent/current assets (`A86:A103`), total assets (`A104`), equity (`A106:A117`), liabilities (`A118:A135`), and total equity and liabilities (`A136`). Parent totals include noncurrent assets (`A94`), current assets (`A103`), total assets (`A104`), equity (`A117`), current/noncurrent liabilities (`A124`, `A134`), and total liabilities (`A135`). |
| Changes in equity | Reconciliation of stock balances by component, including period flows (profit, OCI, capital increase, dividends, reserves) and opening/closing stocks. Column headers `B147:L147` are equity components; row labels encode dates and events. Total column L is presented alongside components and should be treated as a subtotal, not independent economic detail. |
| Cash flow | Period flows grouped into operating (`A193:A196`), investing (`A197:A215`), and financing (`A216:A233`), followed by net cash change, opening and closing cash, FX effect, and noncash transactions (`A234:A238`). Net section flows are subtotals. |
| Directors table | Descriptive and identity data; not financial flows, stocks, ratios, or quantities in the standard sense. |

The percentage-change columns and EPS are derived/ratio-like. Amounts are reported in million rials except per-share labels, which explicitly use rials. Negative cash-flow and expense numbers carry sign, but sign alone is not used to infer classification.

## 8. Summary/detail, restatement, and double-counting observations

- Net income in the income statement (`A30:B30`, `C30`, `D30`) is repeated as net income in comprehensive income (`A58:B58`, `C58`, `D58`) and included in comprehensive income totals (`A70`). These are linked presentations, not separate income streams.
- The income statement contains intermediate subtotals (`A15`, `A20`, `A23`, `A27`) and final net income (`A30`). Avoid adding subtotal rows to their component lines.
- Comprehensive-income subtotals (`A64`, `A68`, `A69`, `A70`) must not be added to their included OCI details or net profit again.
- The balance-sheet totals and subtotals (`A94`, `A103`, `A104`, `A117`, `A124`, `A134:A136`) aggregate component rows. Rows `101` and `132` contain values but no label; do not assign a metric or count these rows as extra categories until their role is clarified.
- Equity statement total column L duplicates the sum represented by the individual equity-component columns. Period net profit and comprehensive income rows are also reflected in retained earnings and the balance movement; these are reconciliations, not additional standalone income.
- Cash-flow net operating/investing/financing amounts and net cash movement (`A196`, `A214:A215`, `A233:A234`) summarize underlying cash-flow lines. Row 215 is cumulative cash before financing and should not be added to the activity section totals.
- Comparative columns explicitly say `تجديد ارائه شده` for prior values in the income, comprehensive-income, financial-position, and cash-flow statements. The workbook does not populate explanatory text below the “reasons for changes” headings (`A40:A44`, `A71`, `A239:A243`), so the reason and scope of restatement are unknown.
- Income/cash-flow comparison column D is annual while B/C are six-month periods; do not compare D as if it were same-duration. Percentage column E appears aligned to B versus C, not B versus D.
- EPS rows `A32:A37` overlap conceptually: operating/nonoperating, continuing/discontinued, basic EPS, and net EPS rows are all present. Their exact formula/relationship is not documented in the workbook; do not sum them.
- In the cash-flow statement, “cash generated from operations” (`A194`) is followed by income tax paid and net operating cash flow (`A196`); these are hierarchical. The investment and financing net cash rows similarly summarize components.

## 9. Ambiguities requiring clarification

1. **Comparative durations:** Confirm that `C10/C56/C191` represent the six months ended ۱۴۰۲/۰۳/۳۱ and `D10/D56/D191` the full prior fiscal year ended ۱۴۰۲/۰۹/۳۰. Dates, title, and equity roll-forward support this, but the C headers do not spell out duration.
2. **Fiscal-year policy:** Equity dates strongly support a ۱۴۰۱/۱۰/۰۱ opening and ۱۴۰۲/۰۹/۳۰ closing for the comparative year. Confirm whether this is the company's regular fiscal-year calendar and whether the current year began ۱۴۰۲/۱۰/۰۱.
3. **Blank-label totals:** Identify rows 101 and 132 in the financial-position statement (`B101:E101`, `B132:E132`). Their values match nearby subtotal structure, but the source label is blank.
4. **Restatement details:** Explain the restated comparative figures. The worksheet contains “reasons for changes” headings but no explanatory content in their associated areas.
5. **Percentage-change basis:** Confirm the formula and comparison basis of E columns, especially in the balance sheet where three dates appear but only one percent-change column is supplied. Observed statement values suggest B vs C.
6. **Income tax and special lines:** Expense and tax rows have zero values in this sample. Zero is an observed value; it does not establish that the item is conceptually absent.
7. **Capital row and EPS grouping:** Confirm the temporal definition of `سرمايه` at A38 and the intended computation/relationship among EPS labels A32:A37.
8. **Cash-flow comparative basis:** Confirm whether the start/end cash rows in comparative columns C and D follow six-month and full-year intervals respectively; the table's start-of-year wording is not expanded by separate column dates.
9. **Audit assurance scope:** “Audited” appears in title/column labels, but the workbook itself does not contain the audit opinion or auditor's report.

## 10. Recommended next inspection step

Have the report owner confirm the comparative-duration mapping, fiscal-year calendar, blank-label rows 101/132, restatement explanations, and percentage-change basis. Then inspect the original published filing or an unflattened source export for the missing explanatory notes and audit opinion. Keep all decisions as evidence-backed, owner-confirmed mappings; this inspection does not finalize DB-STD-003.

## Appendix A. Complete text-cell source Header and label inventory

This inventory is rebuilt directly from every non-empty string-valued source cell in `Recovered_Sheet1`, excluding populated director records (`A260:K262`) because those are data, not headers. Source wording is copied from workbook cells. Classification headings are readable English; no missing label is supplied.

| Cell | Contextual classification | Exact source text |
|---|---|---|
| `A3` | Statement or table title | `صورت سود و زیان` |
| `A8` | Statement or table title | `صورت سود و زيان` |
| `A9` | Unit note | `کليه مبالغ به ميليون ريال است` |
| `A10` | Column header or subheader | `شرح` |
| `B10` | Column header or subheader | `دوره منتهي به ۱۴۰۳/۰۳/۳۱` |
| `C10` | Column header or subheader | `تجديد ارائه شده دوره منتهي به ۱۴۰۲/۰۳/۳۱` |
| `D10` | Column header or subheader | `تجديد ارائه شده دوره منتهي به ۱۴۰۲/۰۹/۳۰` |
| `E10` | Column header or subheader | `درصد تغيير` |
| `B11` | Column header or subheader | `حسابرسی شده` |
| `C11` | Column header or subheader | `حسابرسی شده` |
| `D11` | Column header or subheader | `حسابرسی شده` |
| `A12` | Row label, section heading, or explanatory label | `عمليات در حال تداوم: ` |
| `A13` | Row label, section heading, or explanatory label | `درآمدهاي عملياتي ` |
| `A14` | Row label, section heading, or explanatory label | `بهاى تمام شده درآمدهاي عملياتي ` |
| `A15` | Row label, section heading, or explanatory label | `سود(زيان) ناخالص ` |
| `A16` | Row label, section heading, or explanatory label | `هزينه‏ هاى فروش، ادارى و عمومى ` |
| `A17` | Row label, section heading, or explanatory label | `هزينه کاهش ارزش دريافتني‏ ها (هزينه استثنايي) ` |
| `A18` | Row label, section heading, or explanatory label | `ساير درآمدها ` |
| `A19` | Row label, section heading, or explanatory label | `ساير هزينه‌ها ` |
| `A20` | Row label, section heading, or explanatory label | `سود(زيان) عملياتى ` |
| `A21` | Row label, section heading, or explanatory label | `هزينه‏ هاى مالى ` |
| `A22` | Row label, section heading, or explanatory label | `ساير درآمدها و هزينه ‏هاى غيرعملياتى ` |
| `A23` | Row label, section heading, or explanatory label | `سود(زيان) عمليات در حال تداوم قبل از ماليات ` |
| `A24` | Row label, section heading, or explanatory label | `هزينه ماليات بر درآمد: ` |
| `A25` | Row label, section heading, or explanatory label | `سال جاري ` |
| `A26` | Row label, section heading, or explanatory label | `سال‌هاي قبل ` |
| `A27` | Row label, section heading, or explanatory label | `سود(زيان) خالص عمليات در حال تداوم ` |
| `A28` | Row label, section heading, or explanatory label | `عمليات متوقف شده: ` |
| `A29` | Row label, section heading, or explanatory label | `سود (زيان) خالص عمليات متوقف شده ` |
| `A30` | Row label, section heading, or explanatory label | `سود(زيان) خالص ` |
| `A31` | Row label, section heading, or explanatory label | `سود(زيان) پايه هر سهم: ` |
| `A32` | Row label, section heading, or explanatory label | `عملياتي (ريال) ` |
| `A33` | Row label, section heading, or explanatory label | `غيرعملياتي (ريال) ` |
| `A34` | Row label, section heading, or explanatory label | `ناشي از عمليات در حال تداوم ` |
| `A35` | Row label, section heading, or explanatory label | `ناشي از عمليات متوقف شده ` |
| `A36` | Row label, section heading, or explanatory label | `سود(زيان) پايه هر سهم ` |
| `A37` | Row label, section heading, or explanatory label | `سود (زيان) خالص هر سهم – ريال ` |
| `A38` | Row label, section heading, or explanatory label | `سرمايه ` |
| `A40` | Row label, section heading, or explanatory label | `دلايل تغييرات اطلاعات واقعي دوره منتهي به ۱۴۰۳/۰۳/۳۱ ` |
| `A42` | Row label, section heading, or explanatory label | `دلايل تغييرات اطلاعات واقعي دوره منتهي به ۱۴۰۲/۰۳/۳۱ ` |
| `A44` | Row label, section heading, or explanatory label | `دلايل تغييرات اطلاعات واقعي دوره منتهي به ۱۴۰۲/۰۹/۳۰ ` |
| `A49` | Statement or table title | `صورت سود و زیان جامع` |
| `A54` | Statement or table title | `صورت سود و زيان جامع` |
| `A55` | Unit note | `کليه مبالغ به ميليون ريال است` |
| `A56` | Column header or subheader | `شرح` |
| `B56` | Column header or subheader | `دوره منتهي به ۱۴۰۳/۰۳/۳۱` |
| `C56` | Column header or subheader | `تجديد ارائه شده دوره منتهي به ۱۴۰۲/۰۳/۳۱` |
| `D56` | Column header or subheader | `تجديد ارائه شده دوره منتهي به ۱۴۰۲/۰۹/۳۰` |
| `E56` | Column header or subheader | `درصد تغيير` |
| `B57` | Column header or subheader | `حسابرسی شده` |
| `C57` | Column header or subheader | `حسابرسی شده` |
| `D57` | Column header or subheader | `حسابرسی شده` |
| `A58` | Row label, section heading, or explanatory label | `سود(زيان) خالص ` |
| `A59` | Row label, section heading, or explanatory label | `ساير اقلام سود و زيان جامع که در دوره هاي آتي به صورت سود و زيان تجديد طبقه بندي نخواهد شد: ` |
| `A60` | Row label, section heading, or explanatory label | `مازاد تجديد ارزيابي دارايي‌هاي ثابت مشهود ` |
| `A61` | Row label, section heading, or explanatory label | `تفاوت تسعير ارز عمليات خارجي ` |
| `A62` | Row label, section heading, or explanatory label | `ساير ` |
| `A63` | Row label, section heading, or explanatory label | `ماليات بر درآمد اقلام فوق ` |
| `A64` | Row label, section heading, or explanatory label | `جمع ` |
| `A65` | Row label, section heading, or explanatory label | `ساير اقلام سود و زيان جامع که در دوره هاي آتي به صورت سود و زيان تجديد طبقه بندي خواهد شد: ` |
| `A66` | Row label, section heading, or explanatory label | `ساير ` |
| `A67` | Row label, section heading, or explanatory label | `ماليات بر درآمد اقلام فوق ` |
| `A68` | Row label, section heading, or explanatory label | `جمع ` |
| `A69` | Row label, section heading, or explanatory label | `ساير اقلام سود و زيان جامع سال پس از کسر ماليات ` |
| `A70` | Row label, section heading, or explanatory label | `سود(زيان) جامع سال ` |
| `A71` | Row label, section heading, or explanatory label | `توضيحات ` |
| `A76` | Statement or table title | `صورت وضعیت مالی` |
| `A81` | Statement or table title | `صورت وضعيت مالي` |
| `A82` | Unit note | `کليه مبالغ به ميليون ريال است` |
| `A83` | Column header or subheader | `شرح` |
| `B83` | Column header or subheader | `به تاريخ ۱۴۰۳/۰۳/۳۱` |
| `C83` | Column header or subheader | `تجديد ارائه شده به تاريخ ۱۴۰۲/۰۹/۳۰` |
| `D83` | Column header or subheader | `تجديد ارائه شده به تاريخ ۱۴۰۱/۱۰/۰۱` |
| `E83` | Column header or subheader | `درصد تغيير` |
| `B84` | Column header or subheader | `حسابرسی شده` |
| `C84` | Column header or subheader | `حسابرسی شده` |
| `D84` | Column header or subheader | `حسابرسی شده` |
| `A85` | Row label, section heading, or explanatory label | `دارايي‌ها ` |
| `A86` | Row label, section heading, or explanatory label | `دارايي‌هاي غيرجاري ` |
| `A87` | Row label, section heading, or explanatory label | `دارايي‌هاي ثابت مشهود ` |
| `A88` | Row label, section heading, or explanatory label | `سرمايه‌گذاري در املاک ` |
| `A89` | Row label, section heading, or explanatory label | `دارايي‌هاي نامشهود ` |
| `A90` | Row label, section heading, or explanatory label | `سرمايه‌گذاري‌هاي بلندمدت ` |
| `A91` | Row label, section heading, or explanatory label | `دريافتني‌هاي بلندمدت ` |
| `A92` | Row label, section heading, or explanatory label | `دارايي ماليات انتقالي ` |
| `A93` | Row label, section heading, or explanatory label | `ساير دارايي‌ها ` |
| `A94` | Row label, section heading, or explanatory label | `جمع دارايي‌هاي غيرجاري ` |
| `A95` | Row label, section heading, or explanatory label | `دارايي‌هاي جاري ` |
| `A96` | Row label, section heading, or explanatory label | `سفارشات و پيش‌پرداخت‌ها ` |
| `A97` | Row label, section heading, or explanatory label | `موجودي مواد و کالا ` |
| `A98` | Row label, section heading, or explanatory label | `دريافتني‌هاي تجاري و ساير دريافتني‌ها ` |
| `A99` | Row label, section heading, or explanatory label | `سرمايه‌گذاري‌هاي کوتاه‌مدت ` |
| `A100` | Row label, section heading, or explanatory label | `موجودي نقد ` |
| `A102` | Row label, section heading, or explanatory label | `دارايي‌هاي نگهداري شده براي فروش ` |
| `A103` | Row label, section heading, or explanatory label | `جمع دارايي‌هاي جاري ` |
| `A104` | Row label, section heading, or explanatory label | `جمع دارايي‌ها ` |
| `A105` | Row label, section heading, or explanatory label | `حقوق مالکانه و بدهي‌ها ` |
| `A106` | Row label, section heading, or explanatory label | `حقوق مالکانه ` |
| `A107` | Row label, section heading, or explanatory label | `سرمايه ` |
| `A108` | Row label, section heading, or explanatory label | `افزايش سرمايه در جريان ` |
| `A109` | Row label, section heading, or explanatory label | `صرف سهام ` |
| `A110` | Row label, section heading, or explanatory label | `صرف سهام خزانه ` |
| `A111` | Row label, section heading, or explanatory label | `اندوخته قانوني ` |
| `A112` | Row label, section heading, or explanatory label | `ساير اندوخته‌ها ` |
| `A113` | Row label, section heading, or explanatory label | `مازاد تجديدارزيابي دارايي‌ها ` |
| `A114` | Row label, section heading, or explanatory label | `تفاوت تسعير ارز عمليات خارجي ` |
| `A115` | Row label, section heading, or explanatory label | `سود(زيان) انباشته ` |
| `A116` | Row label, section heading, or explanatory label | `سهام خزانه ` |
| `A117` | Row label, section heading, or explanatory label | `جمع حقوق مالکانه ` |
| `A118` | Row label, section heading, or explanatory label | `بدهي‌ها ` |
| `A119` | Row label, section heading, or explanatory label | `بدهي‌هاي غيرجاري ` |
| `A120` | Row label, section heading, or explanatory label | `پرداختني‌هاي بلندمدت ` |
| `A121` | Row label, section heading, or explanatory label | `تسهيلات مالي بلندمدت ` |
| `A122` | Row label, section heading, or explanatory label | `بدهي ماليات انتقالي ` |
| `A123` | Row label, section heading, or explanatory label | `ذخيره مزاياي پايان خدمت کارکنان ` |
| `A124` | Row label, section heading, or explanatory label | `جمع بدهي‌هاي غيرجاري ` |
| `A125` | Row label, section heading, or explanatory label | `بدهي‌هاي جاري ` |
| `A126` | Row label, section heading, or explanatory label | `پرداختني‌هاي تجاري و ساير پرداختني‌ها ` |
| `A127` | Row label, section heading, or explanatory label | `ماليات پرداختني ` |
| `A128` | Row label, section heading, or explanatory label | `سود سهام پرداختني ` |
| `A129` | Row label, section heading, or explanatory label | `تسهيلات مالي ` |
| `A130` | Row label, section heading, or explanatory label | `ذخاير ` |
| `A131` | Row label, section heading, or explanatory label | `پيش‌دريافت‌ها ` |
| `A133` | Row label, section heading, or explanatory label | `بدهي‌هاي ‌مرتبط ‌با دارايي‌هاي نگهداري‌‌شده براي ‌فروش ` |
| `A134` | Row label, section heading, or explanatory label | `جمع بدهي‌هاي جاري ` |
| `A135` | Row label, section heading, or explanatory label | `جمع بدهي‌ها ` |
| `A136` | Row label, section heading, or explanatory label | `جمع حقوق مالکانه و بدهي‌ها ` |
| `A140` | Statement or table title | `صورت تغییرات در حقوق مالکانه` |
| `A145` | Statement or table title | `صورت تغييرات در حقوق مالکانه` |
| `A146` | Unit note | `کليه مبالغ به ميليون ريال است` |
| `A147` | Column header or subheader | `شرح` |
| `B147` | Column header or subheader | `سرمايه` |
| `C147` | Column header or subheader | `افزايش سرمايه در جريان` |
| `D147` | Column header or subheader | `صرف سهام` |
| `E147` | Column header or subheader | `صرف سهام خزانه` |
| `F147` | Column header or subheader | `اندوخته قانوني` |
| `G147` | Column header or subheader | `ساير اندوخته‌ها` |
| `H147` | Column header or subheader | `مازاد تجديد ارزيابي دارايي‌ها` |
| `I147` | Column header or subheader | `تفاوت تسعير ارز عمليات خارجي` |
| `J147` | Column header or subheader | `سود انباشته` |
| `K147` | Column header or subheader | `سهام خزانه` |
| `L147` | Column header or subheader | `جمع کل` |
| `A148` | Row label, section heading, or explanatory label | `مانده در ۱۴۰۱/۱۰/۰۱ ` |
| `A149` | Row label, section heading, or explanatory label | `اصلاح اشتباهات ` |
| `A150` | Row label, section heading, or explanatory label | `تغيير در رويه‌هاي حسابداري ` |
| `A151` | Row label, section heading, or explanatory label | `مانده تجديد ارائه شده در ۱۴۰۱/۱۰/۰۱ ` |
| `A152` | Row label, section heading, or explanatory label | `تغييرات حقوق مالکانه در سال ۱۴۰۲/۰۹/۳۰ ` |
| `A153` | Row label, section heading, or explanatory label | `سود(زيان) خالص گزارش شده در صورت‌هاي مالي سال ۱۴۰۲/۰۹/۳۰ ` |
| `A154` | Row label, section heading, or explanatory label | `اصلاح اشتباهات ` |
| `A155` | Row label, section heading, or explanatory label | `تغيير در رويه‌هاي حسابداري ` |
| `A156` | Row label, section heading, or explanatory label | `سود(زيان) خالص تجديد ارائه شده سال ۱۴۰۲/۰۹/۳۰ ` |
| `A157` | Row label, section heading, or explanatory label | `ساير اقلام سود و زيان جامع پس از کسر ماليات ` |
| `A158` | Row label, section heading, or explanatory label | `سود(زيان) جامع سال ۱۴۰۲/۰۹/۳۰ ` |
| `A159` | Row label, section heading, or explanatory label | `سود سهام مصوب ` |
| `A160` | Row label, section heading, or explanatory label | `افزايش سرمايه ` |
| `A161` | Row label, section heading, or explanatory label | `افزايش سرمايه در جريان ` |
| `A162` | Row label, section heading, or explanatory label | `خريد سهام خزانه ` |
| `A163` | Row label, section heading, or explanatory label | `فروش سهام خزانه ` |
| `A164` | Row label, section heading, or explanatory label | `انتقال از ساير اقلام حقوق مالکانه به سود و زيان انباشته ` |
| `A165` | Row label, section heading, or explanatory label | `تخصيص به اندوخته قانوني ` |
| `A166` | Row label, section heading, or explanatory label | `تخصيص به ساير اندوخته‌ها ` |
| `A167` | Row label, section heading, or explanatory label | `مانده تجديد ارائه شده در ۱۴۰۲/۰۹/۳۰ ` |
| `A168` | Row label, section heading, or explanatory label | `تغييرات حقوق مالکانه در دوره ۶ ماهه منتهي به ۱۴۰۳/۰۳/۳۱ ` |
| `A169` | Row label, section heading, or explanatory label | `سود (زيان) خالص در دوره ۶ ماهه منتهي به ۱۴۰۳/۰۳/۳۱ ` |
| `A170` | Row label, section heading, or explanatory label | `ساير اقلام سود و زيان جامع پس از کسر ماليات ` |
| `A171` | Row label, section heading, or explanatory label | `سود (زيان) جامع در دوره ۶ ماهه منتهي به ۱۴۰۳/۰۳/۳۱ ` |
| `A172` | Row label, section heading, or explanatory label | `سود سهام مصوب ` |
| `A173` | Row label, section heading, or explanatory label | `افزايش سرمايه ` |
| `A174` | Row label, section heading, or explanatory label | `افزايش سرمايه در جريان ` |
| `A175` | Row label, section heading, or explanatory label | `خريد سهام خزانه ` |
| `A176` | Row label, section heading, or explanatory label | `فروش سهام خزانه ` |
| `A177` | Row label, section heading, or explanatory label | `انتقال از ساير اقلام حقوق مالکانه به سود و زيان انباشته ` |
| `A178` | Row label, section heading, or explanatory label | `تخصيص به اندوخته قانوني ` |
| `A179` | Row label, section heading, or explanatory label | `تخصيص به ساير اندوخته‌ها ` |
| `A180` | Row label, section heading, or explanatory label | `مانده در ۱۴۰۳/۰۳/۳۱ ` |
| `A184` | Statement or table title | `صورت جریان های نقدی` |
| `A189` | Statement or table title | `صورت جريان‌هاي نقدي` |
| `A190` | Unit note | `کليه مبالغ به ميليون ريال است` |
| `A191` | Column header or subheader | `شرح` |
| `B191` | Column header or subheader | `دوره منتهي به ۱۴۰۳/۰۳/۳۱` |
| `C191` | Column header or subheader | `تجديد ارائه شده دوره منتهي به ۱۴۰۲/۰۳/۳۱` |
| `D191` | Column header or subheader | `تجديد ارائه شده دوره منتهي به ۱۴۰۲/۰۹/۳۰` |
| `E191` | Column header or subheader | `درصد تغيير` |
| `B192` | Column header or subheader | `حسابرسی شده` |
| `C192` | Column header or subheader | `حسابرسی شده` |
| `D192` | Column header or subheader | `حسابرسی شده` |
| `A193` | Row label, section heading, or explanatory label | `جريان­هاي نقدي حاصل از فعاليت‌هاي عملياتي: ` |
| `A194` | Row label, section heading, or explanatory label | `نقد حاصل از عمليات ` |
| `A195` | Row label, section heading, or explanatory label | `پرداخت‌هاي نقدي بابت ماليات بر درآمد ` |
| `A196` | Row label, section heading, or explanatory label | `جريان ‌خالص ‌ورود‌ (خروج) ‌نقد حاصل از فعاليت‌هاي ‌عملياتي ` |
| `A197` | Row label, section heading, or explanatory label | `جريان­هاي نقدي حاصل از فعاليت‌هاي سرمايه‌گذاري: ` |
| `A198` | Row label, section heading, or explanatory label | `دريافت‌هاي نقدي حاصل از فروش دارايي‌هاي ثابت مشهود ` |
| `A199` | Row label, section heading, or explanatory label | `پرداخت‌هاي نقدي براي خريد دارايي‌هاي ثابت مشهود ` |
| `A200` | Row label, section heading, or explanatory label | `دريافت‌هاي نقدي حاصل از فروش دارايي‌هاي غيرجاري نگهداري‌شده براي فروش ` |
| `A201` | Row label, section heading, or explanatory label | `دريافت‌هاي نقدي حاصل از فروش دارايي‌هاي نامشهود ` |
| `A202` | Row label, section heading, or explanatory label | `پرداخت‌هاي نقدي براي خريد دارايي‌هاي نامشهود ` |
| `E202` | Descriptive text label | `-- ` |
| `A203` | Row label, section heading, or explanatory label | `دريافت‌هاي نقدي حاصل از فروش سرمايه‌گذاري‌هاي بلندمدت ` |
| `A204` | Row label, section heading, or explanatory label | `پرداخت‌هاي نقدي براي تحصيل سرمايه‌گذاري‌هاي بلندمدت ` |
| `E204` | Descriptive text label | `-- ` |
| `A205` | Row label, section heading, or explanatory label | `دريافت‌هاي نقدي حاصل از فروش سرمايه‌گذاري در املاک ` |
| `A206` | Row label, section heading, or explanatory label | `پرداخت‌هاي نقدي براي تحصيل سرمايه‌گذاري‌ در املاک ` |
| `A207` | Row label, section heading, or explanatory label | `دريافت‌هاي نقدي حاصل از فروش سرمايه‌گذاري‌هاي کوتاه‌مدت ` |
| `A208` | Row label, section heading, or explanatory label | `پرداخت‌هاي نقدي براي تحصيل سرمايه‌گذاري‌هاي کوتاه‌مدت ` |
| `A209` | Row label, section heading, or explanatory label | `پرداخت‌هاي نقدي بابت تسهيلات اعطايي به ديگران ` |
| `A210` | Row label, section heading, or explanatory label | `دريافت‌هاي نقدي حاصل از استرداد تسهيلات اعطايي به ديگران ` |
| `A211` | Row label, section heading, or explanatory label | `دريافت‌هاي نقدي حاصل از سود تسهيلات اعطايي به ديگران ` |
| `A212` | Row label, section heading, or explanatory label | `دريافت‌هاي نقدي حاصل از سود‌ سهام ` |
| `A213` | Row label, section heading, or explanatory label | `دريافت‌هاي نقدي حاصل از سود ساير سرمايه‌گذاري‌ها ` |
| `A214` | Row label, section heading, or explanatory label | `جريان خالص ورود (خروج) نقد حاصل از فعاليت‌هاي سرمايه‌گذاري ` |
| `A215` | Row label, section heading, or explanatory label | `جريان خالص ورود (خروج) نقد قبل از فعاليت‌هاي تامين مالي ` |
| `A216` | Row label, section heading, or explanatory label | `جريان­هاي نقدي حاصل از فعاليت‌هاي تامين مالي: ` |
| `A217` | Row label, section heading, or explanatory label | `دريافت‌هاي نقدي حاصل از افزايش سرمايه ` |
| `A218` | Row label, section heading, or explanatory label | `دريافت‌هاي نقدي حاصل از صرف سهام ` |
| `A219` | Row label, section heading, or explanatory label | `دريافت‌هاي نقدي حاصل از فروش سهام خزانه ` |
| `A220` | Row label, section heading, or explanatory label | `پرداخت‌هاي نقدي براي خريد سهام خزانه ` |
| `A221` | Row label, section heading, or explanatory label | `دريافت‌هاي نقدي حاصل از تسهيلات ` |
| `E221` | Descriptive text label | `-- ` |
| `A222` | Row label, section heading, or explanatory label | `پرداخت‌هاي نقدي بابت اصل تسهيلات ` |
| `E222` | Descriptive text label | `-- ` |
| `A223` | Row label, section heading, or explanatory label | `پرداخت‌هاي نقدي بابت سود تسهيلات ` |
| `A224` | Row label, section heading, or explanatory label | `دريافت‌هاي نقدي حاصل از انتشار اوراق مشارکت ` |
| `A225` | Row label, section heading, or explanatory label | `پرداخت‌هاي نقدي بابت اصل اوراق مشارکت ` |
| `A226` | Row label, section heading, or explanatory label | `پرداخت‌هاي نقدي بابت سود اوراق مشارکت ` |
| `A227` | Row label, section heading, or explanatory label | `دريافت‌هاي نقدي حاصل از انتشار اوراق خريد دين ` |
| `A228` | Row label, section heading, or explanatory label | `پرداخت‌هاي نقدي بابت اصل اوراق خريد دين ` |
| `A229` | Row label, section heading, or explanatory label | `پرداخت‌هاي نقدي بابت سود اوراق خريد دين ` |
| `A230` | Row label, section heading, or explanatory label | `پرداخت‌هاي نقدي بابت اصل اقساط اجاره سرمايه‌اي ` |
| `A231` | Row label, section heading, or explanatory label | `پرداخت‌هاي نقدي بابت سود اجاره سرمايه‌اي ` |
| `A232` | Row label, section heading, or explanatory label | `پرداخت‌هاي نقدي بابت سود سهام ` |
| `E232` | Descriptive text label | `-- ` |
| `A233` | Row label, section heading, or explanatory label | `جريان خالص ورود (خروج) نقد حاصل از فعاليت‌هاي تامين مالي ` |
| `A234` | Row label, section heading, or explanatory label | `خالص افزايش (کاهش) در موجودي نقد ` |
| `A235` | Row label, section heading, or explanatory label | `مانده موجودي نقد در ابتداي سال ` |
| `A236` | Row label, section heading, or explanatory label | `تاثير تغييرات نرخ ارز ` |
| `A237` | Row label, section heading, or explanatory label | `مانده موجودي نقد در پايان سال ` |
| `A238` | Row label, section heading, or explanatory label | `معاملات غيرنقدي ` |
| `E238` | Descriptive text label | `-- ` |
| `A239` | Row label, section heading, or explanatory label | `دلايل تغييرات اطلاعات واقعي دوره منتهي به ۱۴۰۳/۰۳/۳۱ ` |
| `A241` | Row label, section heading, or explanatory label | `دلايل تغييرات اطلاعات واقعي دوره منتهي به ۱۴۰۲/۰۳/۳۱ ` |
| `A243` | Row label, section heading, or explanatory label | `دلايل تغييرات اطلاعات واقعي دوره منتهي به ۱۴۰۲/۰۹/۳۰ ` |
| `A248` | Statement or table title | `اعضاي هيئت مديره` |
| `A253` | Unit note | `کلیه مبالغ درج شده به میلیون ریال می باشد` |
| `A257` | Column header or subheader | `نام عضو حقیقی یا حقوقی` |
| `B257` | Column header or subheader | `نام عضو حقیقی یا حقوقی جدید هیئت مدیره` |
| `C257` | Column header or subheader | `شمارۀ ثبت / کد ملی` |
| `D257` | Column header or subheader | `نام نماینده قبلی عضو حقوقی` |
| `E257` | Column header or subheader | `نام نماینده جدید عضو حقوقی` |
| `F257` | Column header or subheader | `کد ملی` |
| `G257` | Column header or subheader | `سمت` |
| `H257` | Column header or subheader | `موظف/غیر موظف` |
| `I257` | Column header or subheader | `مقطع` |
| `J257` | Column header or subheader | `رشته` |
| `K257` | Column header or subheader | `امضا کننده صورت مالی` |
| `A258` | Column header or subheader | `قدیم هیئت مدیره` |
| `I258` | Column header or subheader | `تحصیلی` |
| `J258` | Column header or subheader | `تحصیلی` |
## Follow-up Evidence Review

### Appendix A encoding correction

**Verified:** Appendix A previously had question marks in its column headings and contextual classifications. I rebuilt the appendix from the source workbook. Headings/classifications are now readable English; all 257 source labels are copied directly from workbook cells with original wording. No missing label was inferred. Populated director records (`A260:K262`) are data, not headers, and are excluded.

### Blank-label rows 101 and 132

**Direct values from `Recovered_Sheet1!A:E`:**

| Row | A | B | C | D | E |
|---|---|---:|---:|---:|---:|
| 101 | (blank) | 4006293 | 4228147 | 2613999 | -5 |
| 132 | (blank) | 1223059 | 629486 | 824739 | 94 |

Both rows are visible at 15.75 points and are not hidden. Columns A:E are visible. A101 and A132 are ordinary blank cells, not merged-cell placeholders; no merged range overlaps either row. Each has style id 5, matching neighboring cells, with no fill and medium borders. Formatting does not conceal or provide a label.

Neighboring labels: `A95:A104` includes the current-assets heading, named asset rows, A101, the held-for-sale asset row, and current-assets/total-assets rows. `A125:A136` includes the current-liabilities heading, payable/tax/dividend/loan/provision/advance rows, A132, the held-for-sale-liabilities row, and current-liability/total-liability/equity-and-liabilities totals. Exact neighboring source wording and addresses are retained in Appendix A.

**Unresolved:** the source has no labels in A101 or A132. Their position and values do not establish their meaning.

### Temporal interpretation and comparative checks

| Statement | Direct evidence | Assessment |
|---|---|---|
| Income | B10 current period ends 1403/03/31; C10 is restated and ends 1402/03/31; D10 is restated and ends 1402/09/30; E10 says percentage change. B11:D11 each say audited. Net income row 30 is 303,991 / 334,885 / 820,811. | B is six months by workbook title and equity A168. C is reasonably inferred to be the corresponding six months from matching 03/31 endpoints. D is reasonably inferred as prior full fiscal year from equity A152:A167. |
| Comprehensive income | B56:D56 repeat the endpoint/restatement pattern; E56 is percentage change. Row 58 net income is 303,991 / 334,885 / 820,811 and matches income row 30. | B six months is supported; C six months and D full year are inferences supported by endpoint dates and equity schedule. |
| Financial position | B83 at 1403/03/31; C83 restated at 1402/09/30; D83 restated at 1401/10/01; E83 percentage change. | All are point-in-time balances. D is the opening-date balance, not a flow. |
| Cash flow | B191 current endpoint 1403/03/31; C191 restated endpoint 1402/03/31; D191 restated endpoint 1402/09/30; E191 percentage change. | B six months is supported by title/equity evidence; C corresponding six months is inferred; D prior full year is supported by cash and equity roll-forwards. |
| Changes in equity | A148 opening balance dated 1401/10/01; A152 identifies changes through 1402/09/30; A167 is restated balance at that date; A168 explicitly identifies six-month changes ending 1403/03/31; A180 is closing balance. | Prior-year cycle and current six-month movement are directly visible. No standalone-quarter column is present. |

No standalone-quarter values were calculated. C flow-column duration is supported by its corresponding 03/31 endpoint, but the C headers do not themselves state ?six months.?

#### Percentage-change column E

**Verified:** Every numeric E value in income rows 13:38, comprehensive rows 58:70, financial-position rows 87:136, and cash-flow rows 194:238 matches the nearest whole percentage from `(B - C) / abs(C) * 100` when C is nonzero. Examples: income revenue row 13 (2,161,199 vs 1,614,748) = 34%; balance row 91 (1,827,346 vs 422,695) = 332%; cash-flow row 234 (69,262 vs 2,067) = 3,251%. Populated E values therefore compare B with C, not D. Where C is zero, E is generally blank; some cash-flow rows show `--` (E202, E204, E221:E222, E232, E238).

#### Comparative cash opening and closing balances

| Column | Opening cash (row 235) | Net change (row 234) | Closing cash (row 237) | Cross-check |
|---|---:|---:|---:|---|
| B | 13,477 | 69,262 | 82,739 | 13,477 + 69,262 = 82,739; closing matches balance B100 and opening matches C100. |
| C | 54,473 | 2,067 | 56,540 | 54,473 + 2,067 = 56,540; opening matches D100. Ending balance is not separately present in the balance sheet at the C endpoint. |
| D | 54,473 | -40,996 | 13,477 | 54,473 - 40,996 = 13,477; opening matches D100 and closing matches C100. |

All columns reconcile arithmetically. B and D opening/closing balances align with balance-sheet dates. C is consistent with six months based on its period endpoint, but that duration remains an inference.

### Fiscal-year start evidence

**Verified:** Equity A148 opens at 1401/10/01, A167 closes the restated year at 1402/09/30, and A168 labels the current six-month movement through 1403/03/31.

**Inference:** the current cycle likely began 1402/10/01. No cell explicitly labels the current opening date as 1402/10/01 or states a general fiscal-year policy. Owner confirmation remains necessary.

### Restatement and explanatory-note areas

| Area | Direct cell evidence | Structure and finding |
|---|---|---|
| A40:A44 | A40, A42, A44 contain explanation headings; A41 and A43 are blank. | Rows 40:45 are each merged A:F; no other values or non-text content in those ranges. Visible rows/columns. Headings exist, explanation cells are empty. |
| A71 | A71 contains an explanations heading; row 72 is blank. | A71:F71 and A72:F72 are merged; no non-text content; visible. |
| A239:A243 | A239, A241, A243 contain explanation headings; A240/A242 are blank; paired row 244 is also blank. | Rows 239:244 are merged A:F; no other values or non-text content; visible. |

The worksheet has no hidden rows or columns, images, charts, or comments. The missing explanatory text cannot be recovered from these areas, so reasons for comparative restatement remain unknown.

### Evidence status and remaining ambiguities

- **Verified:** cell labels and values, blank cells, merge ranges, row visibility/heights, percentage checks, and cash reconciliation arithmetic.
- **Reasonable inferences:** C flow columns are corresponding prior six-month periods; D flow columns are the prior full fiscal year; current fiscal-year start is likely 1402/10/01.
- **Unresolved:** confirmation of comparative durations and current-year start; meanings of rows 101 and 132; restatement explanations; regular fiscal-year policy.
