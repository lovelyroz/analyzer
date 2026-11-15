# DB-AUD-002 — Real Excel Financial Statement Temporal Structure Audit

**Mode:** Report only. No code, tests, database, migration, or workbook changes were made.  
**Inspection date:** 2026-11-08.  
**Source scope:** Only `.xlsx` files in `excel/`; original `.xls` files were not opened.

## Method and scope

Enumerated the `.xlsx` files recursively under `excel/` and inspected each workbook's worksheet names, used dimensions, visibility, merged ranges, hidden row/column flags, formula cells, worksheet text, and temporal/table headers. Loaded formula and cached-value views without evaluating formulas. The workbooks contain no formula cells, no hidden worksheets/rows/columns, and no Excel structured tables; the visible data are laid out as ordinary worksheet cell grids. Each workbook has one visible worksheet named `Recovered_Sheet1`.

The available inventory is small enough to inspect all four files. The file names were treated as labels only. Issuer identity is reported only where the workbook itself supports it; file names, creator metadata, and unrelated subsidiary lists are not treated as proof of issuer identity. Cell text below is transcribed as stored, including Persian script and spelling.

## Inventory and sample selection

| Workbook | Bytes | Worksheet / used dimension | Structural/report-type evidence | Selection |
|---|---:|---|---|---|
| `excel/cheshme.xlsx` | 25,115 | `Recovered_Sheet1`, A1:V222 (222 × 22) | Portfolio statements, realized dividend income, operating/investment income, investment roll-forward and industry summary. | Selected: snapshot/activity tables and narrative temporal disclosures. |
| `excel/fzar.xlsx` | 16,173 | `Recovered_Sheet1`, A1:Z63 (63 × 26) | Monthly activity; production and sales, purchases, energy, foreign currency. | Selected: monthly plus cumulative, adjusted cumulative and prior-year cumulative columns in one table. |
| `excel/fzar2.xlsx` | 69,387 | `Recovered_Sheet1`, A1:Z874 (874 × 26) | Workbook title property: `صورت‌های مالی میاندوره‌ای تلفیقی 6 ماهه منتهی به 1405/03/31 (حسابرسی شده)`; includes income statement, financial position and other appended schedules. | Selected: formal statements with multiple current/comparative dates and distinct period semantics. |
| `excel/samanBank.xlsx` | 41,393 | `Recovered_Sheet1`, A1:M489 (489 × 13) | Workbook title property: `صورت‌های مالی میاندوره‌ای 6 ماهه منتهی به 1405/06/31`; management interpretive report sections include balance-date and six-month periods. | Selected: date-pair columns, multiple independent tables and forecast dates. |

Workbook core properties do not name the reporting company in any of the four cases. Text in `fzar2.xlsx` and `samanBank.xlsx` supports the report types and the latter's banking subject matter, but not a definitive issuer name. `cheshme.xlsx` and `fzar.xlsx` also do not establish the issuer name in the inspected table headers. Thus the company identity is unresolved from these workbooks alone.

## Structural summary

| Workbook | Report type(s) | Temporal structure | Important limitation |
|---|---|---|---|
| `cheshme.xlsx` | Other: investment portfolio / monthly activity disclosure | Opening, change and closing snapshots; named one-month, YTD and prior-year periods in separate income columns; a table also pairs corrected YTD with the month and full prior fiscal year. | Many opening/closing portfolio tables have no explicit date in their own headers. The workbook's narrative/date context is needed. |
| `fzar.xlsx` | Production and Sales; monthly activity schedules | Prior cumulative to 1405/06/31, correction, corrected cumulative to 1405/06/31, one month to 1405/07/30, current cumulative to 1405/07/30, prior-year cumulative to 1404/07/30; further forecast columns. | Comparative columns have different durations/years alongside a single-month column. Product rows include measures as well as monetary values. |
| `fzar2.xlsx` | Income Statement, Balance Sheet / Statement of Financial Position, comprehensive income, and other schedules | Income statement has 1405/03/31, comparative 1404/03/31, and another restated 1404/09/30 column; balance sheet has three point-in-time dates. | A single worksheet combines duration-based and point-in-time statements. “دوره منتهي” by itself does not prove whether a flow is standalone or cumulative. |
| `samanBank.xlsx` | Other: management interpretive report with balance and flow schedules | Date pairs and repeated dates under grouped categories; explicit six-month periods, current/prior-year, estimates, and balance snapshots. | There are many independent tables in one sheet. Some columns combine measurement dates with forecast narrative rather than comparable actuals. |

## Detailed workbook evidence

### `cheshme.xlsx` — portfolio and monthly activity disclosures

**Structure.** `Recovered_Sheet1` is visible, used range A1:V222, with 76 merged ranges. No hidden rows or columns and no formulas. Merged headers include `A9:A10`, `D9:F9`, `G9:I9`, `J9:O9`; later grouped headers include `A107:A109`, `B107:G107`, `H107:K107`, `J108:K108`, `A130:G130` is not merged as a whole, and `A194:V194` contains several grouped header merges. No Excel structured tables were defined.

**Portfolio snapshot/activity table, A9:O32.** Exact top-level headers are `D9='ابتدای دوره'`, `G9='تغییرات'`, `J9='انتهای دوره'`. The second header row has `D10='تعداد سهام'`, `E10='بهای تمام شده'`, `F10='ارزش بازار'`; change measures at G:I; and closing measures at J:O. Representative values: `D12=1437377936`, `E12=5195175`, `F12=34942657`; change `G12=0`, `H12=0`, `I12=6597565`; closing `K12=5195175`, `L12=41540222`, `O12=36345047`. These columns describe within-period movement and beginning/ending positions, not two dated financial-statement balances. Neither start nor end calendar dates are printed in this table. Start/end dates and fiscal year cannot be established from these headers alone; context elsewhere in the workbook identifies a one-month disclosure ending ۱۴۰۵/۰۷/۳۰, but tying this particular table to those dates is contextual inference, not an explicit table label.

**Other portfolio table, A44:K65.** Merged/group headers again divide `D44:E44='ابتدای دوره'`, `F44:G44='تغییرات'`, `H44:J44='انتهای دوره'` (with merged ranges including `D44:E45`, `F44:G45`, `H44:J44`). Example `D46=150`, `E46=15150`, `F46=0`, `G46=0`, `I46=15150`. Dates are absent from the table header. It cannot safely be assigned a precise duration from this table alone.

**Dividend income table, A107:K115.** Rows 107–108 contain multi-row/group headers: `B108='سال مالی شرکت سرمایه پذیر'`, `C108='تاریخ برگزاری مجمع'`, `D108='تعداد سهام در تاریخ مجمع'`, `H108='سود (زیان) هر سهم (ریال)'`, `I108='سود تقسیمی هر سهم (ریال)'`; `J108:K108` is `درآمد حاصل از سود سهام مجمع برگزار شده و سال مالی شناسایی درآمد`. Row 109 provides `J109='۱۴۰۵/۱۲/۲۹'` and `K109='* ۱۴۰۴/۱۲/۲۹'`. These are dates/years associated with dividend recognition buckets, not standalone quarterly periods. The corresponding actual row-level company cells are blank in this sample, while totals appear at `J110=0`, `K110=0`, `J113=0`, `K113=0`. Rows 114–115 separately label `درآمد سود سهام محقق شده از ابتدای سال مالی تا پایان ماه گذشته` and `... تا پایان ماه`; each has 750315 in J. Row 117 explicitly says `کادر توضيحي مربوط به اطلاعات دوره ۱ ماهه منتهي به ۱۴۰۵/۰۷/۳۰`; row 119 says `کادر توضيحي مربوط به اطلاعات تجمعي از ابتداي سال تا پايان تاريخ ۱۴۰۵/۰۷/۳۰`. Those establish one-month and cumulative YTD meanings for the narrative boxes; they do not independently assign dates to all portfolio tables.

**Operating income, A130:G136.** The exact headers are `B130='از ابتدای سال مالی تا پایان دوره منتهی به ۱۴۰۵/۰۶/۳۱'`, `C130='اصلاحات'`, `D130='از ابتدای سال مالی تا پایان دوره منتهی به ۱۴۰۵/۰۶/۳۱ (اصلاح شده)'`, `E130='دوره ۱ ماهه منتهی به ۱۴۰۵/۰۷/۳۰'`, `F130='از ابتدای سال مالی تا پایان دوره منتهی به ۱۴۰۵/۰۷/۳۰'`, and `G130='سال مالی منتهی به ۱۴۰۴/۱۲/۲۹'`. Example row 135: `B135=14983890`, `C135=0`, `D135=14983890`, `E135=4123061`, `F135=19106951`, `G135=36789792`; total row 136: `B136=15792004`, `E136=4123061`, `F136=19915065`, `G136=51024631`. B and D are same-period YTD before/after corrections, E is a one-month flow, F is current fiscal YTD, G is prior full-year comparison. Start dates are not printed. That B+E=F on the total row is consistent with adjacent cumulative periods, but the semantic labels, not arithmetic, establish the period types.

**Investment carrying value table, A138:C148.** `B138='دوره مالی منتهی به ۱۴۰۵/۰۷/۳۰'`, `C138='سال مالی منتهی به ۱۴۰۴/۱۲/۲۹'`; subheader row 139 says `بهای تمام شده` for both. This is a current date and prior fiscal-year-end comparison; `B148=22252437` and `C148=22346983`. The end dates are explicit, but the period represented by carrying values is a snapshot, not a flow duration.

**Other-investment roll-forward, A160:K182.** Merged row 160 headers include `B160='ابتدای دوره'`, `E160='خالص خرید (فروش) طی دوره'`, `H160='انتهای دوره'`; row 161 splits quantities, costs, market value, and movement. Example `B163=403447`, `C163=400000`, `H163=403447`, `I163=400000`, `K163=1421`. Dates are missing in the table. Do not assign a precise beginning/end date or fiscal year from this table alone.

**Industry investment summary, A194:V216 and A217:V222.** In the first table, row 194 groups investee types, row 195 groups `ابتداي دوره`, `تغييرات`, and `انتهاي دوره`, and row 196 identifies measures such as `تعداد شرکت`, `بهاي تمام شده`, and `ارزش بازار`. A second similar block starts at row 217 with headers on rows 218–219. Merges span multiple columns and rows in the same sheet. These are period-relative roll-forwards without explicit dates in the table headers. The summaries confirm that a worksheet can contain multiple tables with repeated but not necessarily date-qualified semantics.

### `fzar.xlsx` — monthly production and sales

**Structure.** `Recovered_Sheet1` is visible, used range A1:Z63. It has 36 merged ranges and no hidden rows/columns or formula cells. The workbook has monthly report title `A3='گزارش فعالیت ماهانه'`. Section `A8='تولید و فروش'`. Header groups are merged: `C10:F10`, `G10:I10`, `J10:M10`, `N10:Q10`, `R10:U10`, `V10:Y10`; the final descriptor `Z10:Z11` is merged.

**Production and sales table, A10:Z31.** Exact temporal headers in row 10:

- `C10='از ابتدای سال مالی تا تاریخ ۱۴۰۵/۰۶/۳۱'` (current-year cumulative through ۱۴۰۵/۰۶/۳۱).
- `G10='اصلاحات'` (adjustment block, not an independent time period).
- `J10='از ابتدای سال مالی تا تاریخ ۱۴۰۵/۰۶/۳۱ (اصلاح شده)'` (restated same YTD period).
- `N10='دوره یک ماهه منتهی به ۱۴۰۵/۰۷/۳۰'` (one-month period ending ۱۴۰۵/۰۷/۳۰).
- `R10='از ابتدای سال مالی تا تاریخ ۱۴۰۵/۰۷/۳۰'` (current-year cumulative through ۱۴۰۵/۰۷/۳۰).
- `V10='از ابتدای سال مالی تا تاریخ ۱۴۰۴/۰۷/۳۰'` (prior-year cumulative through ۱۴۰۴/۰۷/۳۰).
- `Z10='وضعیت محصول-واحد'` is a status descriptor, not a period.

Row 11 defines subcolumns: for C:F, `تعداد تولید`, `تعداد فروش`, `نرخ فروش (ریال)`, `مبلغ فروش (میلیون ریال)`; the adjustment and restated groups have their own subcolumns; N:Q is the one-month group; R:U and V:Y are cumulative groups. Example product row 15 gives `C15=1333`, `D15=1914.87`, `F15=51423`; corrections `G15=0`, `H15=0`, `I15=0`; restated YTD `J15=1333`, `K15=1914.87`, `M15=51423`; one month `N15=955`, `O15=506.36`, `Q15=15824`; current YTD `R15=2288`, `S15=2421.23`, `U15=67247`; prior-year YTD `V15=3445.47`, `W15=4624.25`, `Y15=14000`. On this row, the reported current cumulative quantity/value follows the prior YTD plus the current month values (e.g. `R15=J15+N15`, `U15=M15+Q15`), which corroborates the explicit header labels. It does not establish any start date beyond the phrase “از ابتدای سال مالی”; fiscal year-end is not stated in these columns.

**Additional temporal blocks.** Purchases in A33:T41 have `C33='از ابتدای سال مالی تا تاریخ ۱۴۰۵/۰۶/۳۱'`, `F33='اصلاحات'`, `I33='ازابتدای سال مالی تا تاریخ ۱۴۰۵/۰۶/۳۱ (اصلاح شده)'`, `L33='خرید دوره یک ماهه منتهی به ۱۴۰۵/۰۷/۳۰'`, `O33='مواد اولیه خریداری شده از ابتدای دوره تا پایان دوره منتهی به ۱۴۰۵/۰۷/۳۰'`, and `R33='از ابتدای سال مالی تا تاریخ ۱۴۰۴/۰۷/۳۰'`. Energy in A43:X48 adds a forecast `W43='مانده پیش بینی تا انتهای سال مالی ۱۴۰۵/۰۹/۳۰'`; the current YTD and one-month groups are separated across E:G, N:P, and Q:S, with prior-year date at T43. Currency resources in A50:W57 similarly distinguish current YTD, a one-month date `L50='دوره یکماهه ۱۴۰۵/۰۷/۳۰'`, current YTD, prior-year YTD and a year-end estimate. Hence table-specific group layouts vary even within the same report.

Narrative cells `A60='کادر توضیحات در مورد اصلاحات'`, `A61='کادر توضیحی مربوط به اطلاعات دوره ۱ ماهه منتهی به ۱۴۰۵/۰۷/۳۰'`, and `A62='کادر توضیحی مربوط اطلاعات تجمعی از ابتدای سال تا پایان مورخ ۱۴۰۵/۰۷/۳۰'` reinforce monthly vs cumulative labels. No standalone quarter is shown in this sample. Current/prior comparison is explicitly date-qualified at the cumulative group level; no start day is given.

### `fzar2.xlsx` — formal financial statements and appended schedules

**Structure.** `Recovered_Sheet1` is visible, used range A1:Z874, with 168 merged ranges. No hidden rows/columns or formulas. Its workbook title property identifies a consolidated interim six-month report ending 1405/03/31. There are multiple independent statement blocks on this single worksheet. The formal headers are not consistently merged: `A9:A10` and `E9:E10` are merged, while the date labels in B9:D9 are individual cells.

**Consolidated income statement, A9:E43.** Exact headers at row 9: `B9='دوره منتهي به ۱۴۰۵/۰۳/۳۱'`, `C9='تجديد ارائه شده دوره منتهي به ۱۴۰۴/۰۳/۳۱'`, `D9='تجديد ارائه شده دوره منتهي به ۱۴۰۴/۰۹/۳۰'`, `E9='درصد تغيير'`. Row 10 says `حسابرسی شده` under B, C, D. Example `B12=48780966`, `C12=19317656`, `D12=53952825`; `E12=153`. The workbook title calls the current report six-month, so B's six-month duration is confirmed by workbook metadata plus the statement end date; the header itself does not state the start date. C's same-date prior-year comparative is likely a six-month comparison by context (“تجديد ارائه شده دوره”), but its duration is not written in the cell. D is explicitly a different prior-period end date (۱۴۰۴/۰۹/۳۰), with no duration specified in the row header. It must not be interpreted as a same-duration comparative based on column position. The report does not label standalone quarter values here.

**Comprehensive income statement, A60:E80.** Same three period columns repeat exactly in `B60:D60`, with audit status in row 61. This is a second independent table with the same period structure; representative values `B62=66493934`, `C62=19184881`, `D62=51084741`. The same current/prior duration caveat applies.

**Consolidated statement of financial position, A92:E… (beginning at row 92).** Row 92 says `B92='به تاريخ ۱۴۰۵/۰۳/۳۱'`, `C92='تجديد ارائه شده به تاريخ ۱۴۰۴/۰۹/۳۰'`, `D92='تجديد ارائه شده به تاريخ ۱۴۰۳/۱۰/۰۱'`, `E92='درصد تغيير'`; row 93 has audit status. Example `B96=4980382`, `C96=4292782`, `D96=4292782`. These are point-in-time balances at three distinct dates, not duration flows. Dates are explicit, but duration does not apply. This also shows that “تجديد ارائه شده” columns need not refer to matching year-end dates.

The later worksheet contains additional statement/schedule areas, including statement of changes in equity and cash flows (visible section titles include `صورت جریان های نقدی` at A373/A378). In the cash flow block, `B380='دوره منتهی به۱۴۰۵/۰۶/۳۱'`, `C380='تجدید ارائه شده۱۴۰۴/۰۶/۳۱'`, `D380='درصد تغییر'`, with audit markers at B381/C381 and example `B383=310867468`, `C383=21130489`. The date-bearing statement header is at A380:D381; the precise start date is not supplied in the visible period labels, and the workbook's title period end differs from this appended block's date, so it cannot be assumed these appended schedules all share the title period. This is a strong example of needing local-table evidence rather than workbook-level defaults.

### `samanBank.xlsx` — management interpretive report schedules

**Structure.** `Recovered_Sheet1` is visible, used range A1:M489, with 103 merged ranges. No hidden rows/columns and no formulas. Workbook title property gives an interim six-month report ending 1405/06/31. It contains multiple independent tables and narrative sections; its first section is `A3='خلاصه اطلاعات گزارش تفسیری - صفحه 1'`. No Excel structured tables are defined.

**Loan balances, A11:K27.** Row 11 repeats date pairs by aging category: `B11='در تاریخ ۱۴۰۴/۱۲/۲۹'`, `C11='در تاریخ ۱۴۰۵/۰۶/۳۱'`; same pair at D:E, F:G, H:I and J:K. Row 12 groups each pair under `جاری`, `سررسید گذشته`, `معوق`, `مشکوک الوصول`, `جمع` through merges B12:C12, D12:E12, F12:G12, H12:I12, J12:K12. Example non-current loans `B14=3893946956`, `C14=5269432573`, and total `J14=3941336975`, `K14=5317234439`. These are two balance dates separated by about six months (dates explicit); the table is not a flow statement.

**Deposits, A39:F49.** Row 39 groups `B39:C39='مانده سپرده ها'`, `D39:E39='متوسط نرخ سود مانده سپرده ها'`, and F as forecast narrative. Row 40 separates each metric by `در تاریخ ۱۴۰۴/۱۲/۲۹` and `در تاریخ ۱۴۰۵/۰۶/۳۱`. Example `B42=2336402133`, `C42=2924929498`. Balance dates are explicit. F's narrative describes management expectations and is not a numerical period column.

**Off-balance sheet items, A52:F58.** Row 52 contains two side-by-side sets: A:B:C and D:E:F, each with date labels `۱۴۰۵/۰۶/۳۱` and `۱۴۰۴/۱۲/۲۹` under different obligation descriptions. Example `B53=81068897`, `C53=47501877`, `E53=81068897`, `F53=47501877`. Independent left/right tables share one worksheet row but describe different obligation groups.

**Six-month management KPIs, A70:D81 and A75:D80.** `B70='در تاریخ ۱۴۰۵/۰۶/۳۱'`, `C70='در تاریخ ۱۴۰۴/۰۶/۳۱'`, `D70='برآورد در تاریخ ۱۴۰۵/۱۲/۲۹'`: balance-date counts plus future estimate. At row 75, `B75='دوره ۶ ماهه منتهی به ۱۴۰۵/۰۶/۳۱'`, `C75='دوره ۶ ماهه منتهی به ۱۴۰۴/۰۶/۳۱'`, `D75='برآورد تغییر روند در دوره ۶ ماهه منتهی به ۱۴۰۵/۱۲/۲۹'`. These are explicit six-month current/prior-year flow periods and a forecast narrative/period. Example amounts `B76=49624172`, `C76=23107577`; `B79=56600082`, `C79=32115462`.

**Income from facilities/deposits, A85:F105.** Row 85 contains current and prior periods (`B85='دوره ۶ ماهه منتهی به ۱۴۰۵/۰۶/۳۱'`, `D85='دوره ۶ ماهه منتهی به ۱۴۰۴/۰۶/۳۱'`) interleaved with average-rate columns (`C85`, `E85`) and forecast narrative in F. This is a multi-measure header, not a simple contiguous set of period columns. Example `B87=12849695`, `D87=6871282`.

**Investment income, A107:D111.** `B107='دوره ۶ ماهه منتهی به ۱۴۰۵/۰۶/۳۱'`, `C107='دوره ۶ ماهه منتهی به ۱۴۰۴/۰۶/۳۱'`, `D107='برآورد تغییر روند در دوره ۶ ماهه منتهی به ۱۴۰۵/۱۲/۲۹'`. Examples: `B108=11253110`, `C108=2536016`. Explicit six-month flow comparison plus forecast.

**Investee-company returns, A124:J134.** Top-level dates grouped as `C124:F124='دوره ۶ ماهه منتهي به ۱۴۰۵/۰۶/۳۱'` and `G124:I124='دوره ۶ ماهه منتهي به ۱۴۰۴/۰۶/۳۱'`; row 125 defines ownership, carrying cost, investee fiscal year, and income. Example `F128=0`, `I128=0`, with investee-year-end date `E128='۱۴۰۵/۰۹/۳۰'`. Current and prior six-month columns are explicit; investee year end is a separate attribute and must not be mistaken for the data column's end date.

**Other income/expense, A137:C146.** Row 137 uses point dates `B137='۱۴۰۵/۰۶/۳۱'`, `C137='۱۴۰۴/۰۶/۳۱'`; it is less clear from the header alone whether these values are snapshot balances or period flows. The section label at A135 is `سایر درآمدها و هزینه های عملياتي`, which indicates flow semantics, while date-only labels omit `دوره منتهی به`. This is an example where nearby table/section context is needed and a strict date-header parser would misclassify or leave unresolved.

Other later sections list subsidiary/associate information and dates for each investee's fiscal year, inclusion/exclusion, and status; these dates are entity attributes, not column periods. The worksheet title says page 1 while the sheet holds numerous later sections. This confirms that multiple report pages/sections and unrelated date meanings coexist in one worksheet.

## Answers to critical questions

**A. Are temporal headers consistent across companies and statement types?** No. Examples range from merged beginning/change/ending labels (`cheshme.xlsx`, D9/J9), explicit current-month and cumulative date phrases (`fzar.xlsx`, N10/R10), formal flow-period and restatement columns (`fzar2.xlsx`, B9:D9), and repeated balance-date pairs by category (`samanBank.xlsx`, B11:K12).

**B. Can each value's period be determined from its column header alone?** Sometimes. Explicit labels determine the period kind and end date for `fzar.xlsx` monthly/YTD columns and `samanBank.xlsx` six-month KPIs. Snapshot tables often give only dates or only beginning/ending semantics. The `fzar2.xlsx` income statement's start date is absent, and the appended cash flow end date differs from the workbook title. Local context and, at times, external report metadata would be required; absent that, retain unresolved.

**C. Can one table contain different durations or semantics?** Yes. `fzar.xlsx` row 10 combines YTD through two dates, an adjustment block, one month, prior-year YTD and forecast/status data. `samanBank.xlsx` rows 70/75 and 85 mix balance dates, six-month flows, rates, and forecast narrative. `fzar2.xlsx` has two prior comparative dates in the same income statement, and a separate balance sheet uses three snapshots.

**D. Can standalone-quarter and cumulative/YTD values be distinguished reliably?** Only when explicit wording says so. `fzar.xlsx` says `دوره یک ماهه` versus `از ابتدای سال مالی`; `cheshme.xlsx` similarly labels one month and cumulative information. No sample establishes a generic rule for unlabeled tables, and none demonstrates an explicit standalone-quarter column. Do not infer quarter semantics from publication frequency or column order.

**E. How are current-year and prior-year comparative columns represented?** Several forms occur: explicit prior-year cumulative ending on the same calendar date (`fzar.xlsx`, V10); same-length named six-month current/prior columns (`samanBank.xlsx`, B75/C75); restated prior-year period columns (`fzar2.xlsx`, C9); same-period prior full fiscal year alongside monthly/YTD (`cheshme.xlsx`, G130); and date-paired point-in-time balances (`samanBank.xlsx`, B11/C11). They are not interchangeable.

**F. Are there tables without explicit temporal headers?** Yes. Portfolio roll-forward tables use `ابتدای دوره`/`انتهای دوره` without dates (`cheshme.xlsx`, A9:O32; A160:K182; A194:V216). Some tables use section context or plain date values without “period ending” wording (`samanBank.xlsx`, A137:C146).

**G. Are temporal headers merged or split across rows?** Both. `cheshme.xlsx` uses multi-column merges and nested header rows, including A9:A10 and D9:F9. `fzar.xlsx` merges date headings across measure subcolumns, then lists the measure headers in row 11. `fzar2.xlsx` has a merged label in column A across rows 9–10 but separate period cells. `samanBank.xlsx` merges category labels over date-pair subcolumns (B12:C12 etc.).

**H. Can one worksheet contain multiple independent tables with different period structures?** Yes, in all four. Particularly clear in `cheshme.xlsx` (portfolio snapshots, dividends, income flows, investment values) and `samanBank.xlsx` (loan balances, deposits, off-balance items, KPIs, income and investee schedules).

**I. Does the same workbook contain multiple worksheets representing periods/types?** No for these samples: each has exactly one worksheet, `Recovered_Sheet1`. However, that single sheet contains multiple statement types/period structures. No conclusion about multi-sheet source reports can be made from these four files.

**J. Can a one-period-per-report ingestion assumption correctly represent these samples?** No, if it assigns one period to all values in each workbook/report. It would collapse distinct periods within one table and across sections, including month vs YTD vs prior YTD in `fzar.xlsx`, balance snapshots vs flows in `samanBank.xlsx`, and restated/multiple comparative dates in `fzar2.xlsx`. A report-level primary period may be stored as metadata, but value-level period semantics must be retained for every table/column. Unresolved semantics should be quarantined rather than assigned by heuristic.

## Safe automation and unresolved cases

Safe to automate when an exact header explicitly specifies a date and period kind, with the relevant measure-column mapping intact: for example `دوره یک ماهه منتهی به ...`, `از ابتدای سال مالی تا تاریخ ...`, or `دوره ۶ ماهه منتهی به ...`. Keep adjustments and restated values distinct, and treat point-in-time `به تاريخ` / `در تاریخ` headers as snapshots rather than durations. Repeated grouped date pairs must remain attached to their group labels.

Reject or quarantine period assignments when only `ابتدای دوره` / `انتهای دوره` is present without a date; when a plain date's role is ambiguous; when the workbook title conflicts with a local section date; or when a comparative column's duration/start date is unstated. Do not derive standalone versus cumulative status from column order, arithmetic coincidence, or monthly publication cadence. Dates in investee metadata, forecast narratives, and footnotes must not be silently treated as table periods.

Unresolved from these samples: definitive issuer identity for each workbook; exact fiscal-year start dates for YTD headers; whether `fzar2.xlsx` comparative D9 is a comparable duration (only its end date is explicit); the temporal assignment for undated opening/closing portfolio tables; and the exact accounting period represented by some date-only sections in `samanBank.xlsx`. The samples do not show a clearly labeled standalone quarter.

## Exact inspection list

All workbooks were structurally scanned over their full used ranges (including cell values, merged ranges, hidden state and formula presence). Focused temporal evidence was read in these worksheet ranges:

- `excel/cheshme.xlsx` — `Recovered_Sheet1`: full used range A1:V222; focused tables A9:O32, A44:K65, A107:K119, A130:G148, A160:K182, A194:V216, A217:V222.
- `excel/fzar.xlsx` — `Recovered_Sheet1`: full used range A1:Z63; focused tables A10:Z31, A33:T41, A43:X48, A50:W57, A60:A63.
- `excel/fzar2.xlsx` — `Recovered_Sheet1`: full used range A1:Z874; focused statement ranges A9:E43, A60:E80, A92:E112, and cash flow header/evidence A373:D421.
- `excel/samanBank.xlsx` — `Recovered_Sheet1`: full used range A1:M489; focused ranges A11:K27, A39:F49, A52:F58, A70:D81, A85:F105, A107:D111, A124:J134, A135:C146.

No workbook contents were modified.
