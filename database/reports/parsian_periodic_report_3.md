# Parsian Periodic Workbook — Independent Re-Audit Report 2

**Task ID:** DB-ING-006-AUDIT-02  
**Mode:** REPORT ONLY — evidence gathering. No template design, no code changes.  
**Report file:** `parsian_periodic_report_2.md`

## 1. Audit scope, workbook identity, and source SHA-256

| Item | Value |
|---|---|
| Source workbook | `parsian_periodic.xlsx` (uploaded path `/mnt/user-data/uploads/parsian_periodic.xlsx`) |
| SHA-256 | `69186f1ad2b0e481a3588f2731b7027b0a9d9a543d1ca17fd24fc71d8c5aca06` |
| File size | 35850 bytes |
| Package parts | xl/workbook.xml, xl/worksheets/sheet1.xml, xl/worksheets/sheet2.xml, xl/styles.xml, xl/sharedStrings.xml, xl/theme/theme1.xml, xl/printerSettings/printerSettings1.bin (no drawings, comments, tables, defined names, conditional formats, data validations, hyperlinks, external links) |
| Producer (docProps/app.xml) | Microsoft Excel, AppVersion 16.0300 |
| Inspection method | Fresh inspection from scratch of the original XLSX only. Primary method: direct OOXML parsing (Python `zipfile` + `lxml`) of `sheetN.xml`, `styles.xml` (cellXfs → fills / borders), `sharedStrings.xml` and `theme1.xml`; each cell's `s=` style index was resolved to its raw fill and border records. Cross-check: `openpyxl` 3.1.5 (`load_workbook`) for sheet names, dimensions, `rightToLeft`, merged ranges, non-empty / formula counts. |
| Why raw XML was primary | openpyxl replaces non-anchor cells of merged ranges with `MergedCell` objects that do not carry their stored style. Direct XML parsing keeps the fill/border of every stored cell, including non-anchor cells of merged ranges. (On the main sheet openpyxl reports 1258 filled cells in the used rectangle whereas the XML inventory finds 1294; the 36-cell difference are non-anchor cells of merged ranges — 3 Black, 4 Yellow, 29 Blue — see §12.) |
| Previous report | Not read and not used. `parsian_periodic_report_1.md` was neither opened nor modified. |
| Files written | Only this report. The source XLSX was opened read-only and not modified. |

### 1.1 Interpretation notes and limitations

- **No rendering was performed.** Colors and borders are reported from stored metadata only. "Visual appearance" statements are derived from metadata (e.g. theme colour + tint), not from a screenshot.
- **Theme colours** are resolved from `theme1.xml` only approximately: theme index 0 = `lt1` (window, FFFFFF), theme index 1 = `dk1` (windowText, 000000). Tint arithmetic is linear (exact for neutral colours). Raw `theme`/`tint` values are always preserved next to the approximation.
- **Border side naming:** the XML attributes `left`/`right`/`top`/`bottom` are reported exactly as stored. In the stored data the `left` attribute appears on the lowest-index column of each region and `right` on the highest-index column, i.e. consistent with column-index order. Whether Excel mirrors them on screen for the right-to-left worksheet was **not verified visually**. All edge statements below are therefore expressed in column-index terms ("min column edge", "max column edge") plus the stored attribute name.
- **Border ordinary vs. distinguishable:** 100 % of the "ordinary" border sides on both worksheets are `medium` with raw colour `rgb FFDDDDDD` (light grey). A border side is called **distinguishable** here only if its raw colour is **not** `FFDDDDDD` (observed: `indexed 64` = automatic, or `rgb FF000000`). This is an objective colour test, not an owner decision; style `thin`/`medium` was not used as a criterion.
- **Edge continuity** uses either the cell's own side or the facing side of the neighbouring cell outside the rectangle (source "own" / "neighbor" is reported).
- **Invisible characters** (ZWNJ U+200C, soft hyphen U+00AD, trailing spaces) are preserved in values as stored; values are shown verbatim.
- **Excel data type** is reported from the stored cell: `s` = shared string, `n` = number, "blank" = styled cell with no `<v>` value. No cell is of type formula, boolean, error or inline string.
- **Blank vs zero:** a blank cell (no `<v>`) is never reported as numeric `0`; cells containing a stored numeric `0` are listed separately in §11.
- **Colour roles.** Role assignment is by raw fill only: Red `FFFF0000`; Blue `FF0197C8` (and the distinct raw shade `FF0070C0`, reported separately and counted in the Blue role); Yellow `FFFFFF00`; Gray theme 0 tint −0.25; Black theme 1 tint 0.05 **and** theme 1 tint 0 (two raw shades, both counted as Black per owner clarification, reported separately); Green `FF00B050`; Uncolored = no fill.

## 2. Worksheet inventory

### 2.1 Worksheet `Recovered_Sheet1`

| Property | Observed |
|---|---|
| Exact worksheet name | `Recovered_Sheet1` (position 1; sheetId 1; state visible) |
| Used range (`<dimension>` and computed from stored cells) | `A1:L411` (identical) |
| `rightToLeft` property | True (`rightToLeft="1"` on `<sheetView>`) |
| Dimensions | 411 rows × 12 columns = 4932 cells in the used rectangle |
| Cells physically stored in XML (`<c>` elements) | 2125 |
| Used-rectangle cells with no `<c>` element (no value, no style) | 2807 |
| Non-empty cells (value stored) | 1384 (numbers 900, strings 484) |
| Bounding box of non-empty cells | A3:L411 |
| Styled blank cells (`<c>` with no value) | 741 |
| Formula cells | 0 (no `<f>` element anywhere; no coordinates to list) |
| Merged ranges | 101 |
| Hidden rows / hidden columns | none / none |
| Other properties | `tabSelected=1`, `topLeftCell=A7`, active cell `D378`; column widths set for A–L; page setup portrait with printerSettings1.bin; 314 `<row>` elements carry `thickBot="1"` (row-level attribute; no effect on cell-level border metadata audited here); no conditional formatting, data validation, autofilter, freeze panes. |
| Unusual properties affecting interpretation | Sheet name `Recovered_Sheet1` (the name itself suggests a recovered workbook; no further inference made). Right-to-left sheet: column A is the first column in column-index order. Many wide merged ranges (banner / text rows). |

**Merged ranges (all, sorted by row then column):** `A10:A11`, `E10:E11`, `A44:E44`, `A45:E45`, `A46:E46`, `A47:E47`, `A48:E48`, `A49:E49`, `A60:A61`, `E60:E61`, `A79:A80`, `E79:E80`, `A176:A177`, `E176:E177`, `A221:E221`, `A222:E222`, `A223:E223`, `A224:E224`, `A225:E225`, `A226:E226`, `A235:K235`, `A238:A239`, `B239:C239`, `D239:E239`, `F239:G239`, `H239:I239`, `J239:K239`, `A256:B256`, `C256:I256`, `A259:B259`, `C259:I259`, `A262:B262`, `C262:I262`, `A266:A267`, `B266:C266`, `D266:E266`, `F266:F267`, `D276:J276`, `B284:F284`, `A285:I285`, `A294:K294`, `D302:E302`, `D303:E303`, `D304:E304`, `D305:E305`, `D306:E306`, `D307:E307`, `D308:E308`, `B310:G310`, `F313:G313`, `F314:G314`, `F315:G315`, `F316:G316`, `F317:G317`, `F318:G318`, `F319:G319`, `F320:G320`, `F321:G321`, `F322:G322`, `F323:G323`, `F324:G324`, `F325:G325`, `F326:G326`, `F327:G327`, `F328:G328`, `F329:G329`, `F330:G330`, `F331:G331`, `F332:G332`, `A333:B333`, `C333:I333`, `D336:E336`, `D337:E337`, `D338:E338`, `D339:E339`, `D340:E340`, `A341:G341`, `A350:K350`, `A353:B354`, `C353:F353`, `G353:I353`, `J353:K354`, `A355:B355`, `J355:K355`, `A356:B356`, `J356:K356`, `A357:B357`, `J357:K357`, `A358:B358`, `J358:K358`, `A372:B372`, `C372:F372`, `A382:B382`, `C382:F382`, `A391:B391`, `C391:F391`, `A401:B401`, `C401:F401`, `B407:E407`, `A410:I410`, `A411:I411`

### 2.2 Worksheet `Sheet1`

| Property | Observed |
|---|---|
| Exact worksheet name | `Sheet1` (position 2; sheetId 2; state visible) |
| Used range (`<dimension>` and computed from stored cells) | `A1:E24` (identical) |
| `rightToLeft` property | False / not set (no `rightToLeft` attribute; openpyxl returns None) |
| Dimensions | 24 rows × 5 columns = 120 cells in the used rectangle |
| Cells physically stored in XML (`<c>` elements) | 59 |
| Used-rectangle cells with no `<c>` element (no value, no style) | 61 |
| Non-empty cells (value stored) | 49 (numbers 20, strings 29) |
| Bounding box of non-empty cells | A1:E24 |
| Styled blank cells (`<c>` with no value) | 10 |
| Formula cells | 0 (no `<f>` element anywhere; no coordinates to list) |
| Merged ranges | 2 |
| Hidden rows / hidden columns | none / none |
| Other properties | No `<sheetPr>`; `topLeftCell=A12`, active cell A14 (selection A14:E24); column widths set only for A–C; 22 `<row>` elements carry `thickBot="1"`; no conditional formatting, data validation, autofilter, freeze panes, page setup. |
| Unusual properties affecting interpretation | Left-to-right sheet (different from the first sheet). Very small range. No border colour other than the ordinary `FFDDDDDD`. |

**Merged ranges (all, sorted by row then column):** `A16:A17`, `E16:E17`

No worksheet was treated as a duplicate of the other; each was inspected independently.

## 3. Global raw color inventory

### 3.1 Distinct raw fill records found (every `<c>` in both worksheets)

| Role | fill type | color type | raw RGB | theme index | indexed | tint | bgColor (raw) | rendered colour (approx.) | Recovered_Sheet1 | Sheet1 | Total |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Red | solid | rgb | FFFF0000 | — | — | 0.0 | indexed:64 | FF0000 | 17 | 1 | 18 |
| Blue | solid | rgb | FF0197C8 | — | — | 0.0 | indexed:64 | 0197C8 | 125 | 10 | 135 |
| Blue (distinct darker raw shade) | solid | rgb | FF0070C0 | — | — | 0.0 | indexed:64 | 0070C0 | 4 | 0 | 4 |
| Yellow | solid | rgb | FFFFFF00 | — | — | 0.0 | indexed:64 | FFFF00 | 182 | 0 | 182 |
| Gray | solid | theme | — | 0 | — | -0.25 | indexed:64 | BFBFBF (approx., from theme+tint) | 459 | 0 | 459 |
| Black (shade 1: theme 1, tint 0.05) | solid | theme | — | 1 | — | 0.05 | indexed:64 | 0D0D0D (approx., from theme+tint) | 252 | 0 | 252 |
| Black (shade 2: theme 1, tint 0) | solid | theme | — | 1 | — | 0.0 | indexed:64 | 000000 (approx., from theme+tint) | 240 | 0 | 240 |
| Green | solid | rgb | FF00B050 | — | — | 0.0 | indexed:64 | 00B050 | 15 | 1 | 16 |

All solid fills carry `bgColor indexed 64` (Excel default, not a visible colour). Uncolored cells have `fill type none` (`patternType="none"`). No `gray125`, gradient, pattern-other-than-solid or `indexed`-foreground fills exist.

### 3.2 Per-worksheet and workbook-wide counts per color role

| Role | Recovered_Sheet1 | Sheet1 | Workbook |
|---|---|---|---|
| Red | 17 | 1 | 18 |
| Blue | 129 | 10 | 139 |
| Yellow | 182 | 0 | 182 |
| Gray | 459 | 0 | 459 |
| Black | 492 | 0 | 492 |
| Green | 15 | 1 | 16 |
| Uncolored (cell present in XML, no fill) | 831 | 47 | 878 |
| Total `<c>` cells stored in XML | 2125 | 59 | 2184 |
| Used-rectangle cells with no `<c>` (unformatted, empty) | 2807 | 61 | 2868 |
| Used-rectangle total | 4932 | 120 | 5052 |

Sub-counts of the two roles that have more than one raw shade:

| Raw shade | Recovered_Sheet1 | Sheet1 | Workbook |
|---|---|---|---|
| Blue `FF0197C8` | 125 | 10 | 135 |
| Blue `FF0070C0` (darker; cells A95:D95 only) | 4 | 0 | 4 |
| Black theme 1 tint 0.05 | 252 | 0 | 252 |
| Black theme 1 tint 0 (pure) | 240 | 0 | 240 |

Observed difference between the two black shades: raw colour is `theme 1` in both; tint is `0.05` (≈ `0D0D0D`) vs `0` (`000000`). Objectively these differ by about 5 % luminance toward white. They are **not** treated as separate roles. Blue `FF0070C0` vs `FF0197C8` are two clearly different raw RGB values (darker vs lighter blue); both are counted as Blue and listed separately.

### 3.3 Role × stored value-type matrix

| Sheet | Role | numeric | string | blank | total |
|---|---|---|---|---|---|
| Recovered_Sheet1 | Red | 0 | 17 | 0 | 17 |
| Recovered_Sheet1 | Blue | 0 | 100 | 29 | 129 |
| Recovered_Sheet1 | Yellow | 0 | 178 | 4 | 182 |
| Recovered_Sheet1 | Gray | 370 | 0 | 89 | 459 |
| Recovered_Sheet1 | Black | 324 | 49 | 119 | 492 |
| Recovered_Sheet1 | Green | 0 | 15 | 0 | 15 |
| Recovered_Sheet1 | Uncolored (cell present in XML, no fill) | 206 | 125 | 500 | 831 |
| Sheet1 | Red | 0 | 1 | 0 | 1 |
| Sheet1 | Blue | 0 | 8 | 2 | 10 |
| Sheet1 | Yellow | 0 | 0 | 0 | 0 |
| Sheet1 | Gray | 0 | 0 | 0 | 0 |
| Sheet1 | Black | 0 | 0 | 0 | 0 |
| Sheet1 | Green | 0 | 1 | 0 | 1 |
| Sheet1 | Uncolored (cell present in XML, no fill) | 20 | 19 | 8 | 47 |

## 4. Complete coordinate inventory of annotated cells (by worksheet and color)

Compact notation: `X1:Y2` = all cells of that rectangle; comma-separated; no coordinate is omitted. Per-cell tables give value, Excel type and blank flag. Raw fill/colour metadata of each role is in §3.1 (all cells of one raw shade share identical metadata; the shade of each cell is shown where more than one exists).

### 4.1 `Recovered_Sheet1`

#### Recovered_Sheet1 — Red (17 cells)

| Coordinate | Value (verbatim) | Excel data type | Blank? | Fill type | Color metadata |
|---|---|---|---|---|---|
| A8 | `صورت سود و زیان` | s (string) | no | solid | in §3.1 |
| A58 | `صورت سود و زیان جامع` | s (string) | no | solid | in §3.1 |
| A77 | `صورت وضعیت مالی` | s (string) | no | solid | in §3.1 |
| A128 | `صورت تغییرات در حقوق مالکانه` | s (string) | no | solid | in §3.1 |
| A174 | `صورت جریان های نقدی` | s (string) | no | solid | in §3.1 |
| A236 | `مانده تسهیلات اعطایی و ذخیره مطالبات مشکوک الوصول:` | s (string) | no | solid | in §3.1 |
| A264 | `مانده سپرده های دریافتی از مشتریان :` | s (string) | no | solid | in §3.1 |
| A277 | `اقلام زیر خط:` | s (string) | no | solid | in §3.1 |
| A300 | `اطلاعات حق الوکاله و کفایت سرمایه` | s (string) | no | solid | in §3.1 |
| A311 | `درآمد حاصل از تسهيلات اعطايي و سپرده گذاري` | s (string) | no | solid | in §3.1 |
| A334 | `خالص سود (زیان) سرمایه گذاری‌ ها` | s (string) | no | solid | in §3.1 |
| A351 | `وضعیت شرکتهای سرمایه پذیر:` | s (string) | no | solid | in §3.1 |
| A359 | `ساير درآمدها و هزینه های عملياتي:` | s (string) | no | solid | in §3.1 |
| A374 | `خالص ساير درآمدها و هزینه ها:` | s (string) | no | solid | in §3.1 |
| A384 | `هزینه های اداری و عمومی:` | s (string) | no | solid | in §3.1 |
| A393 | `هزینه مالی:` | s (string) | no | solid | in §3.1 |
| A403 | `برنامه شرکت در خصوص تقسیم سود` | s (string) | no | solid | in §3.1 |

#### Recovered_Sheet1 — Blue (129 cells)

| Coordinate | Value (verbatim) | Excel data type | Blank? | Fill type | Color metadata |
|---|---|---|---|---|---|
| A10 | `شرح` | s (string) | no | solid (FF0197C8) | in §3.1 |
| B10 | `دوره منتهي به ۱۴۰۳/۰۶/۳۱` | s (string) | no | solid (FF0197C8) | in §3.1 |
| D10 | `تجدید ارائه شده ۱۴۰۲/۱۲/۲۹` | s (string) | no | solid (FF0197C8) | in §3.1 |
| E10 | `درصد تغييرات` | s (string) | no | solid (FF0197C8) | in §3.1 |
| A11 |  | blank (no value stored) | yes | solid (FF0197C8) | in §3.1 |
| B11 | `حسابرسی نشده` | s (string) | no | solid (FF0197C8) | in §3.1 |
| D11 | `حسابرسی شده` | s (string) | no | solid (FF0197C8) | in §3.1 |
| E11 |  | blank (no value stored) | yes | solid (FF0197C8) | in §3.1 |
| A60 | `شرح` | s (string) | no | solid (FF0197C8) | in §3.1 |
| B60 | `دوره منتهي به ۱۴۰۳/۰۶/۳۱` | s (string) | no | solid (FF0197C8) | in §3.1 |
| D60 | `تجدید ارائه شده ۱۴۰۲/۱۲/۲۹` | s (string) | no | solid (FF0197C8) | in §3.1 |
| E60 | `درصد تغییر` | s (string) | no | solid (FF0197C8) | in §3.1 |
| A61 |  | blank (no value stored) | yes | solid (FF0197C8) | in §3.1 |
| B61 | `حسابرسی نشده` | s (string) | no | solid (FF0197C8) | in §3.1 |
| D61 | `حسابرسی شده` | s (string) | no | solid (FF0197C8) | in §3.1 |
| E61 |  | blank (no value stored) | yes | solid (FF0197C8) | in §3.1 |
| A79 | `شرح` | s (string) | no | solid (FF0197C8) | in §3.1 |
| B79 | `دوره منتهي به ۱۴۰۳/۰۶/۳۱` | s (string) | no | solid (FF0197C8) | in §3.1 |
| C79 | `تجدید ارائه شده ۱۴۰۲/۱۲/۲۹` | s (string) | no | solid (FF0197C8) | in §3.1 |
| D79 | `تجدید ارائه شده ۱۴۰۲/۰۱/۰۱` | s (string) | no | solid (FF0197C8) | in §3.1 |
| E79 | `درصد تغييرات` | s (string) | no | solid (FF0197C8) | in §3.1 |
| A80 |  | blank (no value stored) | yes | solid (FF0197C8) | in §3.1 |
| B80 | `حسابرسی نشده` | s (string) | no | solid (FF0197C8) | in §3.1 |
| C80 | `حسابرسی شده` | s (string) | no | solid (FF0197C8) | in §3.1 |
| D80 | `حسابرسی نشده` | s (string) | no | solid (FF0197C8) | in §3.1 |
| E80 |  | blank (no value stored) | yes | solid (FF0197C8) | in §3.1 |
| A95 | `حقوق مالکانه و بدهی‌ها ` | s (string) | no | solid (FF0070C0) | in §3.1 |
| B95 | `دوره منتهی به ۱۴۰۳/۰۶/۳۱ ` | s (string) | no | solid (FF0070C0) | in §3.1 |
| C95 | `تجدید ارائه شده ۱۴۰۲/۱۲/۲۹ ` | s (string) | no | solid (FF0070C0) | in §3.1 |
| D95 | `تجدید ارائه شده۱۴۰۲/۰۱/۰۱ ` | s (string) | no | solid (FF0070C0) | in §3.1 |
| A130 | `شرح` | s (string) | no | solid (FF0197C8) | in §3.1 |
| B130 | `سرمایه` | s (string) | no | solid (FF0197C8) | in §3.1 |
| C130 | `افزایش سرمایه در جریان` | s (string) | no | solid (FF0197C8) | in §3.1 |
| D130 | `صرف سهام` | s (string) | no | solid (FF0197C8) | in §3.1 |
| E130 | `صرف سهام خزانه` | s (string) | no | solid (FF0197C8) | in §3.1 |
| F130 | `اندوخته قانونی` | s (string) | no | solid (FF0197C8) | in §3.1 |
| G130 | `سایر اندوخته‌ها` | s (string) | no | solid (FF0197C8) | in §3.1 |
| H130 | `مازاد تجدید ارزیابی دارایی‌ها` | s (string) | no | solid (FF0197C8) | in §3.1 |
| I130 | `تفاوت تسعیر ارز عملیات خارجی` | s (string) | no | solid (FF0197C8) | in §3.1 |
| J130 | `سود انباشته` | s (string) | no | solid (FF0197C8) | in §3.1 |
| K130 | `سهام خزانه` | s (string) | no | solid (FF0197C8) | in §3.1 |
| L130 | `جمع کل` | s (string) | no | solid (FF0197C8) | in §3.1 |
| A176 | `شرح` | s (string) | no | solid (FF0197C8) | in §3.1 |
| B176 | `دوره منتهي به ۱۴۰۳/۰۶/۳۱` | s (string) | no | solid (FF0197C8) | in §3.1 |
| D176 | `تجدید ارائه شده۱۴۰۲/۱۲/۲۹` | s (string) | no | solid (FF0197C8) | in §3.1 |
| E176 | `درصد تغییر` | s (string) | no | solid (FF0197C8) | in §3.1 |
| A177 |  | blank (no value stored) | yes | solid (FF0197C8) | in §3.1 |
| B177 | `حسابرسی نشده` | s (string) | no | solid (FF0197C8) | in §3.1 |
| D177 | `حسابرسی شده` | s (string) | no | solid (FF0197C8) | in §3.1 |
| E177 |  | blank (no value stored) | yes | solid (FF0197C8) | in §3.1 |
| A238 | `شرح` | s (string) | no | solid (FF0197C8) | in §3.1 |
| C238 | `در تاریخ ۱۴۰۳/۰۶/۳۱` | s (string) | no | solid (FF0197C8) | in §3.1 |
| E238 | `در تاریخ ۱۴۰۳/۰۶/۳۱` | s (string) | no | solid (FF0197C8) | in §3.1 |
| G238 | `در تاریخ ۱۴۰۳/۰۶/۳۱` | s (string) | no | solid (FF0197C8) | in §3.1 |
| I238 | `در تاریخ ۱۴۰۳/۰۶/۳۱` | s (string) | no | solid (FF0197C8) | in §3.1 |
| J238 | `در تاریخ ۱۴۰۲/۱۲/۲۹` | s (string) | no | solid (FF0197C8) | in §3.1 |
| K238 | `در تاریخ ۱۴۰۳/۰۶/۳۱` | s (string) | no | solid (FF0197C8) | in §3.1 |
| A239 |  | blank (no value stored) | yes | solid (FF0197C8) | in §3.1 |
| B239 | `جاری` | s (string) | no | solid (FF0197C8) | in §3.1 |
| C239 |  | blank (no value stored) | yes | solid (FF0197C8) | in §3.1 |
| D239 | `سررسید گذشته` | s (string) | no | solid (FF0197C8) | in §3.1 |
| E239 |  | blank (no value stored) | yes | solid (FF0197C8) | in §3.1 |
| F239 | `معوق` | s (string) | no | solid (FF0197C8) | in §3.1 |
| G239 |  | blank (no value stored) | yes | solid (FF0197C8) | in §3.1 |
| H239 | `مشکوک الوصول` | s (string) | no | solid (FF0197C8) | in §3.1 |
| I239 |  | blank (no value stored) | yes | solid (FF0197C8) | in §3.1 |
| J239 | `جمع` | s (string) | no | solid (FF0197C8) | in §3.1 |
| K239 |  | blank (no value stored) | yes | solid (FF0197C8) | in §3.1 |
| A266 | `شرح` | s (string) | no | solid (FF0197C8) | in §3.1 |
| B266 | `مانده سپرده ها` | s (string) | no | solid (FF0197C8) | in §3.1 |
| C266 |  | blank (no value stored) | yes | solid (FF0197C8) | in §3.1 |
| D266 | `متوسط نرخ سود مانده سپرده ها` | s (string) | no | solid (FF0197C8) | in §3.1 |
| E266 |  | blank (no value stored) | yes | solid (FF0197C8) | in §3.1 |
| F266 | `برآورد مدیریت از تغییر در نرخ سود سپرده ها و تغییر در مانده سپرده های دریافتی از مشتریان` | s (string) | no | solid (FF0197C8) | in §3.1 |
| A267 |  | blank (no value stored) | yes | solid (FF0197C8) | in §3.1 |
| C267 | `در تاریخ ۱۴۰۳/۰۶/۳۱` | s (string) | no | solid (FF0197C8) | in §3.1 |
| D267 | `در تاریخ ۱۴۰۲/۱۲/۲۹` | s (string) | no | solid (FF0197C8) | in §3.1 |
| E267 | `در تاریخ ۱۴۰۳/۰۶/۳۱` | s (string) | no | solid (FF0197C8) | in §3.1 |
| F267 |  | blank (no value stored) | yes | solid (FF0197C8) | in §3.1 |
| A279 | `شرح` | s (string) | no | solid (FF0197C8) | in §3.1 |
| B279 | `۱۴۰۳/۰۶/۳۱` | s (string) | no | solid (FF0197C8) | in §3.1 |
| C279 | `۱۴۰۲/۱۲/۲۹` | s (string) | no | solid (FF0197C8) | in §3.1 |
| D279 | `شرح` | s (string) | no | solid (FF0197C8) | in §3.1 |
| E279 | `۱۴۰۳/۰۶/۳۱` | s (string) | no | solid (FF0197C8) | in §3.1 |
| F279 | `۱۴۰۲/۱۲/۲۹` | s (string) | no | solid (FF0197C8) | in §3.1 |
| A297 | `شرح` | s (string) | no | solid (FF0197C8) | in §3.1 |
| B297 | `در تاریخ ۱۴۰۲/۱۲/۲۹` | s (string) | no | solid (FF0197C8) | in §3.1 |
| C297 | `در تاریخ ۱۴۰۳/۰۶/۳۱` | s (string) | no | solid (FF0197C8) | in §3.1 |
| D297 | `برآورد در تاریخ ۱۴۰۳/۱۲/۳۰` | s (string) | no | solid (FF0197C8) | in §3.1 |
| A302 | `شرح` | s (string) | no | solid (FF0197C8) | in §3.1 |
| C302 | `دوره ۶ ماهه منتهی به ۱۴۰۳/۰۶/۳۱` | s (string) | no | solid (FF0197C8) | in §3.1 |
| D302 | `برآورد تغییر روند در دوره ۶ ماهه منتهی به ۱۴۰۳/۱۲/۳۰` | s (string) | no | solid (FF0197C8) | in §3.1 |
| E302 |  | blank (no value stored) | yes | solid (FF0197C8) | in §3.1 |
| A313 | `شرح` | s (string) | no | solid (FF0197C8) | in §3.1 |
| D313 | `دوره ۶ ماهه منتهی به ۱۴۰۳/۰۶/۳۱` | s (string) | no | solid (FF0197C8) | in §3.1 |
| E313 | `متوسط نرخ سود دوره ۶ ماهه منتهی به ۱۴۰۳/۰۶/۳۱ (درصد)` | s (string) | no | solid (FF0197C8) | in §3.1 |
| F313 | `برآورد تغییر روند در دوره ۶ ماهه منتهی به ۱۴۰۳/۱۲/۳۰` | s (string) | no | solid (FF0197C8) | in §3.1 |
| G313 |  | blank (no value stored) | yes | solid (FF0197C8) | in §3.1 |
| A336 | `شرح` | s (string) | no | solid (FF0197C8) | in §3.1 |
| C336 | `دوره ۶ ماهه منتهی به ۱۴۰۳/۰۶/۳۱` | s (string) | no | solid (FF0197C8) | in §3.1 |
| D336 | `برآورد تغییر روند در دوره ۶ ماهه منتهی به ۱۴۰۳/۱۲/۳۰` | s (string) | no | solid (FF0197C8) | in §3.1 |
| E336 |  | blank (no value stored) | yes | solid (FF0197C8) | in §3.1 |
| A353 | `نام شرکت` | s (string) | no | solid (FF0197C8) | in §3.1 |
| B353 |  | blank (no value stored) | yes | solid (FF0197C8) | in §3.1 |
| G353 | `دوره ۶ ماهه منتهي به ۱۴۰۳/۰۶/۳۱` | s (string) | no | solid (FF0197C8) | in §3.1 |
| H353 |  | blank (no value stored) | yes | solid (FF0197C8) | in §3.1 |
| I353 |  | blank (no value stored) | yes | solid (FF0197C8) | in §3.1 |
| J353 | `تشريح آخرين وضعيت و برنامه هاي آتي شرکت در شرکت سرمايه پذير` | s (string) | no | solid (FF0197C8) | in §3.1 |
| K353 |  | blank (no value stored) | yes | solid (FF0197C8) | in §3.1 |
| A354 |  | blank (no value stored) | yes | solid (FF0197C8) | in §3.1 |
| B354 |  | blank (no value stored) | yes | solid (FF0197C8) | in §3.1 |
| G354 | `درصد مالکيت` | s (string) | no | solid (FF0197C8) | in §3.1 |
| H354 | `بهاي تمام شده` | s (string) | no | solid (FF0197C8) | in §3.1 |
| I354 | `درآمد سرمايه گذاري` | s (string) | no | solid (FF0197C8) | in §3.1 |
| J354 |  | blank (no value stored) | yes | solid (FF0197C8) | in §3.1 |
| K354 |  | blank (no value stored) | yes | solid (FF0197C8) | in §3.1 |
| A361 | `شرح` | s (string) | no | solid (FF0197C8) | in §3.1 |
| C361 | `۱۴۰۳/۰۶/۳۱` | s (string) | no | solid (FF0197C8) | in §3.1 |
| A376 | `خالص ساير درآمدها و هزينه ها` | s (string) | no | solid (FF0197C8) | in §3.1 |
| C376 | `۱۴۰۳/۰۶/۳۱` | s (string) | no | solid (FF0197C8) | in §3.1 |
| A386 | `هزينه هاي اداري و عمومي` | s (string) | no | solid (FF0197C8) | in §3.1 |
| C386 | `۱۴۰۳/۰۶/۳۱` | s (string) | no | solid (FF0197C8) | in §3.1 |
| A395 | `هزينه‌هاي مالي` | s (string) | no | solid (FF0197C8) | in §3.1 |
| C395 | `۱۴۰۳/۰۶/۳۱` | s (string) | no | solid (FF0197C8) | in §3.1 |
| A404 | `مبلغ سود (زيان) انباشته پايان سال مالي گذشته` | s (string) | no | solid (FF0197C8) | in §3.1 |
| B404 | `سود سهام پيشنهادي هيئت مديره در سال مالي گذشته` | s (string) | no | solid (FF0197C8) | in §3.1 |
| C404 | `مبلغ سود (زيان) خالص سال مالي گذشته` | s (string) | no | solid (FF0197C8) | in §3.1 |
| D404 | `سود سهام مصوب مجمع سال مالي گذشته` | s (string) | no | solid (FF0197C8) | in §3.1 |
| E404 | `پيشنهاد هيئت مديره درخصوص درصد تقسيم سود سال مالي جاري` | s (string) | no | solid (FF0197C8) | in §3.1 |

#### Recovered_Sheet1 — Green (15 cells)

| Coordinate | Value (verbatim) | Excel data type | Blank? | Fill type | Color metadata |
|---|---|---|---|---|---|
| A12 | `عملیات در حال تداوم: ` | s (string) | no | solid | in §3.1 |
| A32 | `عملیات متوقف شده: ` | s (string) | no | solid | in §3.1 |
| A35 | `سود (زیان)پایه هر سهم (ريال) ` | s (string) | no | solid | in §3.1 |
| A63 | `سایر اقلام سود و زیان جامع: ` | s (string) | no | solid | in §3.1 |
| A81 | `دارایی ها ` | s (string) | no | solid | in §3.1 |
| A96 | `حقوق مالکانه ` | s (string) | no | solid | in §3.1 |
| A108 | `بدهی‌ها ` | s (string) | no | solid | in §3.1 |
| A152 | `تغییرات حقوق مالکانه در سال ۱۴۰۳/۰۶/۳۱ ` | s (string) | no | solid | in §3.1 |
| A178 | `جریان­های نقدی حاصل از فعاليت‌هاي عملياتي: ` | s (string) | no | solid | in §3.1 |
| A182 | `فعاليت‌هاي سرمایه‌گذاری ` | s (string) | no | solid | in §3.1 |
| A191 | `فعاليت‌هاي تأمين مالي ` | s (string) | no | solid | in §3.1 |
| A268 | `سپرده های ریالی: ` | s (string) | no | solid | in §3.1 |
| A314 | `درآمد تسهیلات اعطایی: ` | s (string) | no | solid | in §3.1 |
| A362 | `ساير درآمدهاي عملياتي: ` | s (string) | no | solid | in §3.1 |
| A366 | `ساير هزينه هاي عملياتي: ` | s (string) | no | solid | in §3.1 |

#### Recovered_Sheet1 — Yellow (182 cells)

| Coordinate | Value (verbatim) | Excel data type | Blank? | Fill type | Color metadata |
|---|---|---|---|---|---|
| A13 | `درآمد تسهيلات اعطايي و سپرده گذاری و اوراق بدهی ` | s (string) | no | solid | in §3.1 |
| A14 | `هزينه سود سپرده‌ها ` | s (string) | no | solid | in §3.1 |
| A15 | `خالص درآمد تسهیلات و سپرده گذاری ` | s (string) | no | solid | in §3.1 |
| A16 | `درآمد کارمزد ` | s (string) | no | solid | in §3.1 |
| A17 | `هزينه کارمزد ` | s (string) | no | solid | in §3.1 |
| A18 | `خالص درآمد کارمزد ` | s (string) | no | solid | in §3.1 |
| A19 | `خالص سود (زیان) سرمایه گذاری‌ها ` | s (string) | no | solid | in §3.1 |
| A20 | `خالص سود (زيان) مبادلات و معاملات ارزي ` | s (string) | no | solid | in §3.1 |
| A21 | `ساير درآمدها و هزینه های عملياتي ` | s (string) | no | solid | in §3.1 |
| A22 | `جمع درآمدهاي عملياتي ` | s (string) | no | solid | in §3.1 |
| A23 | `خالص ساير درآمدها و هزینه‌ها ` | s (string) | no | solid | in §3.1 |
| A24 | `هزينه‌هاي اداري و عمومي ` | s (string) | no | solid | in §3.1 |
| A25 | `هزينه مطالبات مشکوک الوصول ` | s (string) | no | solid | in §3.1 |
| A26 | `هزينه‌هاي مالي ` | s (string) | no | solid | in §3.1 |
| A27 | `هزينه استهلاک ` | s (string) | no | solid | in §3.1 |
| A28 | `سود(زیان) عملیات در حال تداوم قبل از مالیات ` | s (string) | no | solid | in §3.1 |
| A29 | `ماليات بر درآمد سال جاری ` | s (string) | no | solid | in §3.1 |
| A30 | `ماليات بر درآمد سال های قبل ` | s (string) | no | solid | in §3.1 |
| A31 | `سود (زيان) خالص عملیات در حال تداوم ` | s (string) | no | solid | in §3.1 |
| A33 | `سود(زیان) خالص عملیات متوقف شده ` | s (string) | no | solid | in §3.1 |
| A34 | `سود(زیان) خالص ` | s (string) | no | solid | in §3.1 |
| A36 | `عملياتي (ريال) ` | s (string) | no | solid | in §3.1 |
| A37 | `غيرعملياتي(ريال) ` | s (string) | no | solid | in §3.1 |
| A38 | `ناشی از عملیات در حال تداوم(ریال) ` | s (string) | no | solid | in §3.1 |
| A39 | `ناشي از عمليات متوقف شده(ريال) ` | s (string) | no | solid | in §3.1 |
| A40 | `سود(زیان) پایه هر سهم (ریال) ` | s (string) | no | solid | in §3.1 |
| A41 | `سود (زیان) خالص هر سهم– ریال ` | s (string) | no | solid | in §3.1 |
| A42 | `سرمایه ` | s (string) | no | solid | in §3.1 |
| A62 | `سود(زیان) خالص ` | s (string) | no | solid | in §3.1 |
| A64 | `مازاد تجديد ارزيابي دارايي‌ها ` | s (string) | no | solid | in §3.1 |
| A65 | `تفاوت تسعیر ارز عملیات خارجی ` | s (string) | no | solid | in §3.1 |
| A66 | `مالیات مربوط به سایر اقلام سود و زیان جامع ` | s (string) | no | solid | in §3.1 |
| A67 | `سایر اقلام سود و زیان جامع سال پس از کسر مالیات ` | s (string) | no | solid | in §3.1 |
| A68 | `سود(زيان) جامع سال ` | s (string) | no | solid | in §3.1 |
| A82 | `موجودي نقد ` | s (string) | no | solid | in §3.1 |
| A83 | `مطالبات از بانک ها و ساير موسسات اعتباري ` | s (string) | no | solid | in §3.1 |
| A84 | `مطالبات از دولت ` | s (string) | no | solid | in §3.1 |
| A85 | `تسهيلات اعطايي و مطالبات از اشخاص دولتي ` | s (string) | no | solid | in §3.1 |
| A86 | `تسهيلات اعطايي و مطالبات از اشخاص غير دولتي ` | s (string) | no | solid | in §3.1 |
| A87 | `سرمایه‌گذاری در سهام و ساير اوراق بهادار ` | s (string) | no | solid | in §3.1 |
| A88 | `مطالبات از شرکت‌های فرعی و وابسته ` | s (string) | no | solid | in §3.1 |
| A89 | `ساير حسابهاي دريافتني ` | s (string) | no | solid | in §3.1 |
| A90 | `دارایی‌هاي ثابت مشهود ` | s (string) | no | solid | in §3.1 |
| A91 | `دارایی‌هاي نا مشهود ` | s (string) | no | solid | in §3.1 |
| A92 | `سپرده قانونی ` | s (string) | no | solid | in §3.1 |
| A93 | `ساير دارایی‌ها ` | s (string) | no | solid | in §3.1 |
| A94 | `جمع دارایی‌ها ` | s (string) | no | solid | in §3.1 |
| A97 | `سرمايه ` | s (string) | no | solid | in §3.1 |
| A98 | `افزايش سرمايه در جريان ` | s (string) | no | solid | in §3.1 |
| A99 | `صرف سهام ` | s (string) | no | solid | in §3.1 |
| A100 | `اندوخته صرف سهام ` | s (string) | no | solid | in §3.1 |
| A101 | `اندوخته قانوني ` | s (string) | no | solid | in §3.1 |
| A102 | `ساير اندوخته‌ها ` | s (string) | no | solid | in §3.1 |
| A103 | `مازاد تجديد ارزيابي دارايي‌ها ` | s (string) | no | solid | in §3.1 |
| A104 | `تفاوت تسعیر ارز ` | s (string) | no | solid | in §3.1 |
| A105 | `سود (زيان) انباشته ` | s (string) | no | solid | in §3.1 |
| A106 | `سهام خزانه ` | s (string) | no | solid | in §3.1 |
| A107 | `جمع حقوق مالکانه ` | s (string) | no | solid | in §3.1 |
| A109 | `بدهي به بانكها و ساير موسسات اعتباري ` | s (string) | no | solid | in §3.1 |
| A110 | `سپرده‌هاي مشتریان ` | s (string) | no | solid | in §3.1 |
| A111 | `سود سهام پرداختني ` | s (string) | no | solid | in §3.1 |
| A112 | `اوراق بدهی ` | s (string) | no | solid | in §3.1 |
| A113 | `ذخيره ماليات عملکرد ` | s (string) | no | solid | in §3.1 |
| A114 | `ذخاير و ساير بدهی‌ها ` | s (string) | no | solid | in §3.1 |
| A115 | `ذخيره مزاياي پايان خدمت و تعهدات بازنشستگی کارکنان ` | s (string) | no | solid | in §3.1 |
| A116 | `جمع بدهی های قبل از حقوق صاحبان سپرده های سرمایه گذاری ` | s (string) | no | solid | in §3.1 |
| A117 | `حقوق صاحبان سپرده‌های سرمایه‌گذاری ` | s (string) | no | solid | in §3.1 |
| A118 | `جمع بدهی‌ها ` | s (string) | no | solid | in §3.1 |
| A119 | `جمع بدهی‌ها و حقوق مالکانه ` | s (string) | no | solid | in §3.1 |
| A153 | `سود خالص ۱۴۰۳/۰۶/۳۱ ` | s (string) | no | solid | in §3.1 |
| A154 | `سایر اقلام سود و زیان جامع پس از کسر مالیات ` | s (string) | no | solid | in §3.1 |
| A155 | `سود(زيان) جامع در ۱۴۰۳/۰۶/۳۱ ` | s (string) | no | solid | in §3.1 |
| A156 | `سود(زيان) سهام مصوب ` | s (string) | no | solid | in §3.1 |
| A157 | `افزایش سرمایه ` | s (string) | no | solid | in §3.1 |
| A158 | `افزایش سرمایه در جریان ` | s (string) | no | solid | in §3.1 |
| A159 | `خرید سهام خزانه ` | s (string) | no | solid | in §3.1 |
| A160 | `فروش سهام خزانه ` | s (string) | no | solid | in §3.1 |
| A161 | `سود (زیان) حاصل از فروش سهام خزانه ` | s (string) | no | solid | in §3.1 |
| A162 | `انتقال از سایر اقلام حقوق مالکانه به سود و زیان انباشته ` | s (string) | no | solid | in §3.1 |
| A163 | `تخصیص به اندوخته قانونی ` | s (string) | no | solid | in §3.1 |
| A164 | `تخصیص به سایر اندوخته‌ها ` | s (string) | no | solid | in §3.1 |
| A165 | `مانده در ۱۴۰۳/۰۶/۳۱ ` | s (string) | no | solid | in §3.1 |
| A179 | `نقد حاصل از عملیات ` | s (string) | no | solid | in §3.1 |
| A180 | `پرداخت‌های نقدی بابت مالیات بر درآمد ` | s (string) | no | solid | in §3.1 |
| A181 | `جريان ‌خالص ‌ورود‌ (خروج) ‌نقد حاصل از فعاليت‌هاي ‌عملياتي ` | s (string) | no | solid | in §3.1 |
| A183 | `وجوه پرداختي بابت تحصیل دارایی‌هاي ثابت مشهود ` | s (string) | no | solid | in §3.1 |
| A184 | `وجوه دریافتی بابت فروش دارایی‌هاي ثابت مشهود ` | s (string) | no | solid | in §3.1 |
| A185 | `وجوه پرداختي بابت تحصیل دارایی‌هاي نامشهود ` | s (string) | no | solid | in §3.1 |
| A186 | `وجوه دریافتی بابت فروش دارایی‌هاي نامشهود ` | s (string) | no | solid | in §3.1 |
| A187 | `وجوه پرداختي بابت تحصیل املاک و مستغلات غیر عملیاتی ` | s (string) | no | solid | in §3.1 |
| A188 | `وجوه دریافتی بابت فروش املاک و مستغلات غیر عملیاتی ` | s (string) | no | solid | in §3.1 |
| A189 | `جريان خالص ورود (خروج) وجه نقد ناشی از فعاليت‌هاي سرمایه‌گذاری ` | s (string) | no | solid | in §3.1 |
| A190 | `جريان خالص ورود (خروج) وجه نقد قبل از فعالیت‌های تامین مالی ` | s (string) | no | solid | in §3.1 |
| A192 | `دریافت‌های نقدی حاصل از افزايش سرمايه ` | s (string) | no | solid | in §3.1 |
| A193 | `دریافت‌های نقدی حاصل از صرف سهام ` | s (string) | no | solid | in §3.1 |
| A194 | `دریافت‌های نقدی حاصل از فروش سهام خزانه ` | s (string) | no | solid | in §3.1 |
| A195 | `پرداخت‌های نقدی برای خرید سهام خزانه ` | s (string) | no | solid | in §3.1 |
| A196 | `دریافت‌های نقدی حاصل از تسهيلات ` | s (string) | no | solid | in §3.1 |
| A197 | `پرداخت‌های نقدی بابت اصل تسهيلات ` | s (string) | no | solid | in §3.1 |
| A198 | `پرداخت‌های نقدی بابت سود تسهيلات ` | s (string) | no | solid | in §3.1 |
| A199 | `دریافت‌های نقدی حاصل از انتشار اوراق مشارکت ` | s (string) | no | solid | in §3.1 |
| A200 | `پرداخت‌های نقدی بابت اصل اوراق مشارکت ` | s (string) | no | solid | in §3.1 |
| A201 | `پرداخت‌های نقدی بابت سود اوراق مشارکت ` | s (string) | no | solid | in §3.1 |
| A202 | `دریافت‌های نقدی حاصل از انتشار اوراق خرید دین ` | s (string) | no | solid | in §3.1 |
| A203 | `پرداخت‌های نقدی بابت اصل اوراق خرید دین ` | s (string) | no | solid | in §3.1 |
| A204 | `پرداخت‌های نقدی بابت سود اوراق خرید دین ` | s (string) | no | solid | in §3.1 |
| A205 | `پرداخت‌های نقدی بابت اصل اقساط اجاره سرمایه‌ای ` | s (string) | no | solid | in §3.1 |
| A206 | `پرداخت‌های نقدی بابت سود اجاره سرمایه‌ای ` | s (string) | no | solid | in §3.1 |
| A207 | `پرداخت‌های نقدی بابت سود سهام ` | s (string) | no | solid | in §3.1 |
| A208 | `جريان خالص ورود (خروج) نقد حاصل از فعاليت‌هاي تامين مالي ` | s (string) | no | solid | in §3.1 |
| A209 | `خالص افزايش (کاهش) در موجودی نقد ` | s (string) | no | solid | in §3.1 |
| A210 | `مانده موجودی نقد در ابتدای سال ` | s (string) | no | solid | in §3.1 |
| A211 | `تاثير تغييرات نرخ ارز ` | s (string) | no | solid | in §3.1 |
| A212 | `مانده موجودی نقد در پايان سال ` | s (string) | no | solid | in §3.1 |
| A213 | `معاملات غيرنقدي ` | s (string) | no | solid | in §3.1 |
| A240 | `تسهیلات اعطایی و مطالبات از اشخاص دولتی ` | s (string) | no | solid | in §3.1 |
| A241 | `تسهیلات اعطایی و مطالبات از اشخاص غیر دولتی- ریالی ` | s (string) | no | solid | in §3.1 |
| A242 | `تسهیلات اعطایی و مطالبات از اشخاص غیر دولتی- ارزی ` | s (string) | no | solid | in §3.1 |
| A245 | `سود سالهای آتی ` | s (string) | no | solid | in §3.1 |
| A246 | `سایر ` | s (string) | no | solid | in §3.1 |
| A247 | `مانده تسهیلات پایان دوره ` | s (string) | no | solid | in §3.1 |
| A248 | `ارزش وثایق دریافتی ` | s (string) | no | solid | in §3.1 |
| A249 | `مانده مبنای محاسبه ذخیره اختصاصی ` | s (string) | no | solid | in §3.1 |
| A250 | `ضریب مبنای احتساب ذخیره اختصاصی (درصد) ` | s (string) | no | solid | in §3.1 |
| A251 | `ذخیره اختصاصی مطالبات مشکوک الوصول ` | s (string) | no | solid | in §3.1 |
| A252 | `مانده مبنای محاسبه ذخیره عمومی ` | s (string) | no | solid | in §3.1 |
| A253 | `ذخیره عمومی مطالبات مشکوک الوصول ` | s (string) | no | solid | in §3.1 |
| A269 | `سپرده های کوتاه مدت ` | s (string) | no | solid | in §3.1 |
| A270 | `سپرده های کوتاه مدت ویژه ` | s (string) | no | solid | in §3.1 |
| A271 | `سپرده های بلند مدت ` | s (string) | no | solid | in §3.1 |
| A272 | `جمع سپرده های هزینه زا ` | s (string) | no | solid | in §3.1 |
| A273 | `سپرده های غیر هزینه زا ` | s (string) | no | solid | in §3.1 |
| A274 | `جمع سپرده های ریالی ` | s (string) | no | solid | in §3.1 |
| A275 | `سپرده های ارزی ` | s (string) | no | solid | in §3.1 |
| A280 | `تعهدات مشتریان بابت اعتبارات اسنادی ` | s (string) | no | solid | in §3.1 |
| A281 | `تعهدات مشتریان بابت ضمانت نامه های صادره ` | s (string) | no | solid | in §3.1 |
| A282 | `ساير تعهدات مشتريان بانک ` | s (string) | no | solid | in §3.1 |
| A283 | `وجوه اداره شده و موارد مشابه ` | s (string) | no | solid | in §3.1 |
| A303 | `سهم بانک از درآمدهای مشاع ` | s (string) | no | solid | in §3.1 |
| A304 | `سهم سپرده گذاران از درآمدهای مشاع ` | s (string) | no | solid | in §3.1 |
| A305 | `نرخ حق الوکاله اعلام شده ` | s (string) | no | solid | in §3.1 |
| A306 | `مبلغ حق الوکاله اعمال شده ` | s (string) | no | solid | in §3.1 |
| A307 | `مابه التفاوت سود قابل پرداخت (مازاد سود پرداختی) به سپرده گذاران ` | s (string) | no | solid | in §3.1 |
| A308 | `نسبت کفایت سرمایه ` | s (string) | no | solid | in §3.1 |
| A315 | `فروش اقساطی ` | s (string) | no | solid | in §3.1 |
| A316 | `جعاله ` | s (string) | no | solid | in §3.1 |
| A317 | `اجاره به شرط تملیک ` | s (string) | no | solid | in §3.1 |
| A318 | `سلف ` | s (string) | no | solid | in §3.1 |
| A319 | `مضاربه ` | s (string) | no | solid | in §3.1 |
| A320 | `مشارکت مدنی ` | s (string) | no | solid | in §3.1 |
| A321 | `خرید دین ` | s (string) | no | solid | in §3.1 |
| A322 | `بدهکاران بابت اعتبارات اسنادی پرداخت شده ` | s (string) | no | solid | in §3.1 |
| A323 | `بدهکاران بابت ضمانت نامه های پرداخت شده ` | s (string) | no | solid | in §3.1 |
| A324 | `تسهیلات ارزی ` | s (string) | no | solid | in §3.1 |
| A325 | `تسهیلات قرض الحسنه ` | s (string) | no | solid | in §3.1 |
| A326 | `سایر درآمد تسهیلات اعطایی ` | s (string) | no | solid | in §3.1 |
| A327 | `جمع درآمد حاصل از تسهیلات اعطایی ` | s (string) | no | solid | in §3.1 |
| A328 | `جایزه سپرده قانونی ` | s (string) | no | solid | in §3.1 |
| A329 | `سود حاصل از سپرده گذاری در بانکها ` | s (string) | no | solid | in §3.1 |
| A330 | `جمع سود حاصل از سپرده گذاری ها ` | s (string) | no | solid | in §3.1 |
| A331 | `درآمد اوراق بدهی و سایر درآمدهای ناشی از سپرده گذاری ` | s (string) | no | solid | in §3.1 |
| A332 | `درآمد حاصل ازتسهیلات اعطایی و سپرده‌گذاری‌ها ` | s (string) | no | solid | in §3.1 |
| A337 | `درآمد حاصل از سرمایه گذاری در سهام ` | s (string) | no | solid | in §3.1 |
| A338 | `سود(زیان) حاصل از فروش سرمایه گذاری ` | s (string) | no | solid | in §3.1 |
| A339 | `سود (زیان) تعدیل ذخیره کاهش ارزش سرمایه گذاریها ` | s (string) | no | solid | in §3.1 |
| A355 | `صرافي پارسيان ` | s (string) | no | solid | in §3.1 |
| B355 |  | blank (no value stored) | yes | solid | in §3.1 |
| A356 | `ساير شرکتهاي خارج از بورس ` | s (string) | no | solid | in §3.1 |
| B356 |  | blank (no value stored) | yes | solid | in §3.1 |
| A357 | `گروه داده پردازي پارسيان ` | s (string) | no | solid | in §3.1 |
| B357 |  | blank (no value stored) | yes | solid | in §3.1 |
| A358 | `گروه مالي بانک پارسيان ` | s (string) | no | solid | in §3.1 |
| B358 |  | blank (no value stored) | yes | solid | in §3.1 |
| A363 | `ساير درآمدهاي عملياتي ` | s (string) | no | solid | in §3.1 |
| A365 | `جمع ساير درآمدهاي عملياتي ` | s (string) | no | solid | in §3.1 |
| A367 | `ساير هزينه هاي عملياتي ` | s (string) | no | solid | in §3.1 |
| A377 | `ساير درامدها ` | s (string) | no | solid | in §3.1 |
| A378 | `ساير هزينه ها ` | s (string) | no | solid | in §3.1 |
| A387 | `هزينه هاي اداري و عمومي ` | s (string) | no | solid | in §3.1 |
| A396 | `هزينه مالي تسهيلات دريافتي از ساير بانکها و موسسات اعتباري ` | s (string) | no | solid | in §3.1 |
| A397 | `جريمه اضافه برداشت از بانک مرکزي ` | s (string) | no | solid | in §3.1 |
| A398 | `ساير هزينه هاي مالي ` | s (string) | no | solid | in §3.1 |

#### Recovered_Sheet1 — Gray (459 cells)

Raw metadata (all gray cells): fill `solid`, colour type `theme`, theme index `0`, tint `-0.25`, bgColor `indexed:64`; rgb `—`; indexed `—`.

- **Gray, literal numeric values: 370** — B13:B31, D13:D31, B33:B34, D33:D34, B36:B42, D36:D42, B62, D62, B64:B68, D64:D68, B82:C94, B97:C107, B109:C119, J153, L153:L165, H154:I155, B155:G155, J155:J158, K155, B157:B158, D157:E157, G157:I157, C158, K159:K160, E161:E162, H162:I162, J162:J165, F163, G164:G165, B165:F165, H165:I165, K165, B179:B181, D179:D181, B183:B190, D183:D190, B192:B213, D192:D213, C240:C242, E240:E242, G240:G242, I240:I242, C245:C247, E245:E253, G245:G253, I245:I253, C252:C253, C269:C275, B280:B283, C303:C308, D315:D332, C337:C339, G355:I358, C363, C365, C367, C377:C378, C387, C396:C398, A405:E405
- **Gray, literal text values: 0** — —
- **Gray, blank values (no value stored): 89** — B153:G154, H153:I153, K153:K154, J154, B156, C156:C157, D156:E156, F156:F162, G156:I156, K156:K158, D158:D164, E158:E160, G158:G163, H158:I161, B159:C164, J159:J161, K161:K164, E163:E164, H163:I164, F164, C248:C251
- **Gray, other data types: 0** — —

Gray numeric cells with values (`coordinate=value`, verbatim stored number; row-major):

`B13=147186330`, `D13=229849193`, `B14=-230307149`, `D14=-345542486`, `B15=-83120819`, `D15=-115693293`, `B16=24646669`, `D16=43403722`, `B17=-8624760`, `D17=-10854204`, `B18=16021909`, `D18=32549518`, `B19=402420`, `D19=2453194`, `B20=2072623`, `D20=3775645`, `B21=84513662`, `D21=151543669`, `B22=19889795`, `D22=74628733`, `B23=2192360`, `D23=43015355`, `B24=-28908689`, `D24=-52654898`, `B25=-11646662`, `D25=-50322016`, `B26=-5804157`, `D26=-20082491`, `B27=-918350`, `D27=-1161578`, `B28=-25195703`, `D28=-6576895`, `B29=0`, `D29=-2548000`, `B30=0`, `D30=0`, `B31=-25195703`, `D31=-9124895`, `B33=0`, `D33=0`, `B34=-25195703`, `D34=-9124895`, `B36=-152`, `D36=-237`, `B37=-22`, `D37=174`, `B38=-174`, `D38=-63`, `B39=0`, `D39=0`, `B40=-174`, `D40=-63`, `B41=-161`, `D41=-58`, `B42=156340000`, `D42=156340000`, `B62=-25195703`, `D62=-9124895`, `B64=0`, `D64=0`, `B65=0`, `D65=0`, `B66=0`, `D66=0`, `B67=0`, `D67=0`, `B68=-25195703`, `D68=-9124895`, `B82=347110539`, `C82=295173082`, `B83=686275365`, `C83=696743016`, `B84=2920800`, `C84=2925324`, `B85=5517538`, `C85=5024806`, `B86=2826181422`, `C86=2662958772`, `B87=263166697`, `C87=250958540`, `B88=107179477`, `C88=107851311`, `B89=462006254`, `C89=432339509`, `B90=23049146`, `C90=22273873`, `B91=23180530`, `C91=23237672`, `B92=291130716`, `C92=275811706`, `B93=101636499`, `C93=72855571`, `B94=5139354983`, `C94=4848153182`, `B97=156340000`, `C97=156340000`, `B98=0`, `C98=0`, `B99=0`, `C99=0`, `B100=0`, `C100=0`, `B101=7393601`, `C101=7393601`, `B102=985814`, `C102=985814`, `B103=0`, `C103=0`, `B104=0`, `C104=0`, `B105=-69959998`, `C105=-44764295`, `B106=-26884902`, `C106=-26163160`, `B107=67874515`, `C107=93791960`, `B109=867341907`, `C109=772033496`, `B110=3215472710`, `C110=3081957372`, `B111=324154`, `C111=1815045`, `B112=0`, `C112=0`, `B113=0`, `C113=2548000`, `B114=974455743`, `C114=883995351`, `B115=13885954`, `C115=12011958`, `B116=5071480468`, `C116=4754361222`, `B117=0`, `C117=0`, `B118=5071480468`, `C118=4754361222`, `B119=5139354983`, `C119=4848153182`, `J153=-25195703`, `L153=-25195703`, `H154=0`, `I154=0`, `L154=0`, `B155=0`, `C155=0`, `D155=0`, `E155=0`, `F155=0`, `G155=0`, `H155=0`, `I155=0`, `J155=-25195703`, `K155=0`, `L155=-25195703`, `J156=0`, `L156=0`, `B157=0`, `D157=0`, `E157=0`, `G157=0`, `H157=0`, `I157=0`, `J157=0`, `L157=0`, `B158=0`, `C158=0`, `J158=0`, `L158=0`, `K159=-721742`, `L159=-721742`, `K160=0`, `L160=0`, `E161=0`, `L161=0`, `E162=0`, `H162=0`, `I162=0`, `J162=0`, `L162=0`, `F163=0`, `J163=0`, `L163=0`, `G164=0`, `J164=0`, `L164=0`, `B165=156340000`, `C165=0`, `D165=0`, `E165=0`, `F165=7393601`, `G165=985814`, `H165=0`, `I165=0`, `J165=-69959998`, `K165=-26884902`, `L165=67874515`, `B179=-29363629`, `D179=-96174356`, `B180=-2548000`, `D180=0`, `B181=-31911629`, `D181=-96174356`, `B183=-1379698`, `D183=-7657549`, `B184=36457`, `D184=470555`, `B185=-293822`, `D185=-1183590`, `B186=582`, `D186=0`, `B187=-11630341`, `D187=-15217227`, `B188=261931`, `D188=47066880`, `B189=-13004891`, `D189=23479069`, `B190=-44916520`, `D190=-72695287`, `B192=0`, `D192=0`, `B193=0`, `D193=0`, `B194=0`, `D194=0`, `B195=-721743`, `D195=-1739980`, `B196=14552949`, `D196=8680859`, `B197=0`, `D197=-20082491`, `B198=0`, `D198=0`, `B199=0`, `D199=0`, `B200=0`, `D200=0`, `B201=0`, `D201=0`, `B202=0`, `D202=0`, `B203=0`, `D203=0`, `B204=0`, `D204=0`, `B205=0`, `D205=0`, `B206=0`, `D206=0`, `B207=-1490891`, `D207=-341`, `B208=12340315`, `D208=-13141953`, `B209=-32576205`, `D209=-85837240`, `B210=295173082`, `D210=229326967`, `B211=84513662`, `D211=151683355`, `B212=347110539`, `D212=295173082`, `B213=35419379`, `D213=40841096`, `C240=0`, `E240=5601562`, `G240=0`, `I240=0`, `C241=898771183`, `E241=280319073`, `G241=16190626`, `I241=241404928`, `C242=1469776118`, `E242=38793986`, `G242=46096435`, `I242=147254352`, `C245=145007474`, `E245=0`, `G245=0`, `I245=0`, `C246=4817501`, `E246=0`, `G246=0`, `I246=0`, `C247=2218722326`, `E247=324714621`, `G247=62287061`, `I247=388659280`, `E248=140833161`, `G248=2459935`, `I248=92049597`, `E249=464200531`, `G249=76017753`, `I249=538014611`, `E250=10`, `G250=20`, `I250=50`, `E251=14049291`, `G251=539710`, `I251=114730469`, `C252=2218722326`, `E252=310665330`, `G252=61747351`, `I252=273928811`, `C253=46762403`, `E253=84023`, `G253=0`, `I253=0`, `C269=470781277`, `C270=453951`, `C271=1678516940`, `C272=2149752168`, `C273=710993381`, `C274=2860745549`, `C275=418802062`, `B280=439498515`, `B281=705682218`, `B282=19498400`, `B283=547`, `C303=0`, `C304=112241232`, `C305=0`, `C306=0`, `C307=-78487638`, `C308=-3.38`, `D315=2134924`, `D316=613663`, `D317=0`, `D318=0`, `D319=0`, `D320=10538469`, `D321=1610763`, `D322=6889454`, `D323=148563`, `D324=25729592`, `D325=0`, `D326=82315994`, `D327=129981422`, `D328=1422354`, `D329=4580248`, `D330=6002602`, `D331=11202306`, `D332=147186330`, `C337=402420`, `C338=0`, `C339=0`, `G355=79`, `H355=1191004`, `I355=0`, `G356=1`, `H356=122338363`, `I356=0`, `G357=100`, `H357=36279443`, `I357=0`, `G358=100`, `H358=45109293`, `I358=0`, `C363=84513662`, `C365=84513662`, `C367=0`, `C377=2192360`, `C378=0`, `C387=-28908689`, `C396=0`, `C397=0`, `C398=-5804157`, `A405=-44764295`, `B405=0`, `C405=-9124895`, `D405=0`, `E405=0`

Gray blank cells (each listed individually; all have no `<v>`, number format General (id 0)): `B153`, `C153`, `D153`, `E153`, `F153`, `G153`, `H153`, `I153`, `K153`, `B154`, `C154`, `D154`, `E154`, `F154`, `G154`, `J154`, `K154`, `B156`, `C156`, `D156`, `E156`, `F156`, `G156`, `H156`, `I156`, `K156`, `C157`, `F157`, `K157`, `D158`, `E158`, `F158`, `G158`, `H158`, `I158`, `K158`, `B159`, `C159`, `D159`, `E159`, `F159`, `G159`, `H159`, `I159`, `J159`, `B160`, `C160`, `D160`, `E160`, `F160`, `G160`, `H160`, `I160`, `J160`, `B161`, `C161`, `D161`, `F161`, `G161`, `H161`, `I161`, `J161`, `K161`, `B162`, `C162`, `D162`, `F162`, `G162`, `K162`, `B163`, `C163`, `D163`, `E163`, `G163`, `H163`, `I163`, `K163`, `B164`, `C164`, `D164`, `E164`, `F164`, `H164`, `I164`, `K164`, `C248`, `C249`, `C250`, `C251`

#### Recovered_Sheet1 — Black (492 cells)

- **Black shade 1: theme 1, tint 0.05: 252** — A131:L151
  - numeric: 136 — B131:L134, J136:J139, L136:L151, B137:G139, H137:I141, K137:K139, B141:G141, J141:J144, K141, B143, D143:D144, E143, G143:G144, H143:I143, C144, K145:K146, E147:E148, H148:I148, J148:J151, F149, G150:G151, B151:F151, H151:I151, K151
  - string: 21 — A131:A151
  - blank: 95 — B135:I136, J135, K135:K136, L135, B140:G140, J140:K140, B142, C142:C143, D142:E142, F142:F148, G142:I142, K142:K144, B144:B150, E144:E146, H144:I147, C145:D150, G145:G149, J145:J147, K147:K150, E149:E150, H149:I150, F150
- **Black shade 2: theme 1, tint 0: 240** — C10:C42, C60:C68, C176:C213, B238, D238, F238, H238, B240:B253, D240:D253, F240:F253, H240:H253, B267:B275, B302:B308, B313:C332, B336:B339, C353:F358, B361:B367, B376:B378, B386:B387, B395:B398
  - numeric: 188 — C13:C31, C33:C34, C36:C42, C62, C64:C68, C179:C181, C183:C190, C192:C213, B240:B243, D240:D243, F240:F243, H240:H243, B245:B247, D245:D253, F245:F253, H245:H253, B252:B253, B269:B275, B303:B308, B315:C332, B337:B339, C355:D358, F355:F358, B363, B365, B367, B377:B378, B387, B396:B398
  - string: 28 — C10:C11, C60:C61, C176:C177, B238, D238, F238, H238, B267, B302, B313:C313, B336, C353:C354, D354, E354:E358, F354, B361, B376, B386, B395
  - blank: 24 — C12, C32, C35, C63, C178, C182, C191, B244, D244, F244, H244, B248:B251, B268, B314:C314, D353:F353, B362, B364, B366

Black cells with values (`coordinate=value`; not extracted, listed as observed):

`C10=تجدید ارائه شده ۱۴۰۲/۰۶/۳۱`, `C11=حسابرسی شده`, `C13=87074365`, `C14=-157273597`, `C15=-70199232`, `C16=17434558`, `C17=-4224997`, `C18=13209561`, `C19=1959054`, `C20=1773531`, `C21=18950145`, `C22=-34306941`, `C23=32333034`, `C24=-20919456`, `C25=-4854080`, `C26=-6988533`, `C27=-510281`, `C28=-35246257`, `C29=0`, `C30=0`, `C31=-35246257`, `C33=0`, `C34=-35246257`, `C36=-416`, `C37=174`, `C38=-242`, `C39=0`, `C40=-242`, `C41=-225`, `C42=156340000`, `C60=تجدید ارائه شده ۱۴۰۲/۰۶/۳۱`, `C61=حسابرسی شده`, `C62=-35246257`, `C64=0`, `C65=0`, `C66=0`, `C67=0`, `C68=-35246257`, `A131=مانده در ۱۴۰۲/۰۱/۰۱`, `B131=156340000`, `C131=0`, `D131=0`, `E131=0`, `F131=7393601`, `G131=985814`, `H131=0`, `I131=0`, `J131=-20295950`, `K131=-23976787`, `L131=120446678`, `A132=اصلاح اشتباهات`, `B132=0`, `C132=0`, `D132=0`, `E132=0`, `F132=0`, `G132=0`, `H132=0`, `I132=0`, `J132=-15789842`, `K132=0`, `L132=-15789842`, `A133=تغییر در رویه‌های حسابداری`, `B133=0`, `C133=0`, `D133=0`, `E133=0`, `F133=0`, `G133=0`, `H133=0`, `I133=0`, `J133=0`, `K133=0`, `L133=0`, `A134=مانده تجدید ارائه شده در ۱۴۰۲/`, `B134=156340000`, `C134=0`, `D134=0`, `E134=0`, `F134=7393601`, `G134=985814`, `H134=0`, `I134=0`, `J134=-36085792`, `K134=-23976787`, `L134=104656836`, `A135=تغییرات حقوق مالکانه در سال ۱۴`, `A136=سود(زيان) خالص گزارش شده در صو`, `J136=-9124895`, `L136=-9124895`, `A137=اصلاح اشتباهات`, `B137=0`, `C137=0`, `D137=0`, `E137=0`, `F137=0`, `G137=0`, `H137=0`, `I137=0`, `J137=0`, `K137=0`, `L137=0`, `A138=تغییر در رویه‌های حسابداری`, `B138=0`, `C138=0`, `D138=0`, `E138=0`, `F138=0`, `G138=0`, `H138=0`, `I138=0`, `J138=0`, `K138=0`, `L138=0`, `A139=سود خالص تجدید ارائه شده سال ۱`, `B139=0`, `C139=0`, `D139=0`, `E139=0`, `F139=0`, `G139=0`, `H139=0`, `I139=0`, `J139=-9124895`, `K139=0`, `L139=-9124895`, `A140=سایر اقلام سود و زیان جامع پس `, `H140=0`, `I140=0`, `L140=0`, `A141=سود(زيان) جامع سال ۱۴۰۲/۱۲/۲۹`, `B141=0`, `C141=0`, `D141=0`, `E141=0`, `F141=0`, `G141=0`, `H141=0`, `I141=0`, `J141=-9124895`, `K141=0`, `L141=-9124895`, `A142=سود سهام مصوب`, `J142=0`, `L142=0`, `A143=افزایش سرمایه`, `B143=0`, `D143=0`, `E143=0`, `G143=0`, `H143=0`, `I143=0`, `J143=0`, `L143=0`, `A144=افزایش سرمایه در جریان`, `C144=0`, `D144=0`, `G144=0`, `J144=0`, `L144=0`, `A145=خرید سهام خزانه`, `K145=-3561452`, `L145=-3561452`, `A146=فروش سهام خزانه`, `K146=1375079`, `L146=1375079`, `A147=سود (زیان) حاصل از فروش سهام خ`, `E147=0`, `L147=0`, `A148=انتقال از سایر اقلام حقوق مالک`, `E148=0`, `H148=0`, `I148=0`, `J148=446392`, `L148=446392`, `A149=تخصیص به اندوخته قانونی`, `F149=0`, `J149=0`, `L149=0`, `A150=تخصیص به سایر اندوخته‌ها`, `G150=0`, `J150=0`, `L150=0`, `A151=مانده تجدید ارائه شده در ۱۴۰۲/`, `B151=156340000`, `C151=0`, `D151=0`, `E151=0`, `F151=7393601`, `G151=985814`, `H151=0`, `I151=0`, `J151=-44764295`, `K151=-26163160`, `L151=93791960`, `C176=تجدید ارائه شده۱۴۰۲/۰۶/۳۱`, `C177=حسابرسی شده`, `C179=-110187888`, `C180=0`, `C181=-110187888`, `C183=-5726382`, `C184=75915`, `C185=-328217`, `C186=0`, `C187=-5837768`, `C188=34286189`, `C189=22469737`, `C190=-87718151`, `C192=0`, `C193=424904`, `C194=0`, `C195=-1120902`, `C196=17560550`, `C197=0`, `C198=-6988523`, `C199=0`, `C200=0`, `C201=0`, `C202=0`, `C203=0`, `C204=0`, `C205=0`, `C206=0`, `C207=-341`, `C208=9875688`, `C209=-77842463`, `C210=229326967`, `C211=19036184`, `C212=170520688`, `C213=3288472`, `B238=در تاریخ ۱۴۰۲/۱۲/۲۹`, `D238=در تاریخ ۱۴۰۲/۱۲/۲۹`, `F238=در تاریخ ۱۴۰۲/۱۲/۲۹`, `H238=در تاریخ ۱۴۰۲/۱۲/۲۹`, `B240=943937`, `D240=4080869`, `F240=0`, `H240=0`, `B241=870619839`, `D241=316695405`, `F241=5109498`, `H241=198375341`, `B242=1447241031`, `D242=33487649`, `F242=48988`, `H242=123135192`, `B243=2318804807`, `D243=354263923`, `F243=5158486`, `H243=321510533`, `B245=161368315`, `D245=0`, `F245=0`, `H245=0`, `B246=1`, `D246=0`, `F246=0`, `H246=0`, `B247=2157436491`, `D247=354263923`, `F247=5158486`, `H247=321510533`, `D248=23833161`, `F248=2459935`, `H248=92049597`, `D249=647188312`, `F249=7808050`, `H249=427836280`, `D250=10`, `F250=20`, `H250=50`, `D251=3049291`, `F251=539710`, `H251=114730469`, `B252=2157436491`, `D252=351214632`, `F252=4618776`, `H252=206780064`, `B253=32361761`, `D253=62145`, `F253=0`, `H253=0`, `B267=در تاریخ ۱۴۰۲/۱۲/۲۹`, `B269=449329293`, `B270=145711`, `B271=1634208566`, `B272=2083683570`, `B273=689131598`, `B274=2772815168`, `B275=360010761`, `B302=سال مالی منتهی به۱۴۰۲/۱۲/۲۹`, `B303=0`, `B304=194221502`, `B305=0`, `B306=0`, `B307=-69338916`, `B308=-3.4`, `B313=سال مالی منتهی به ۱۴۰۲/۱۲/۲۹`, `C313=متوسط نرخ سود سال مالی منتهی ب`, `B315=3892061`, `C315=0`, `B316=1753389`, `C316=0`, `B317=0`, `C317=0`, `B318=0`, `C318=0`, `B319=284`, `C319=0`, `B320=2232197`, `C320=0`, `B321=2392929`, `C321=0`, `B322=680668`, `C322=0`, `B323=571059`, `C323=0`, `B324=33918341`, `C324=0`, `B325=0`, `C325=0`, `B326=122234957`, `C326=0`, `B327=167675885`, `C327=0`, `B328=2326102`, `C328=0`, `B329=5443442`, `C329=0`, `B330=7769544`, `C330=0`, `B331=54403764`, `C331=0`, `B332=229849193`, `C332=0`, `B336=سال مالی منتهی به۱۴۰۲/۱۲/۲۹`, `B337=2453194`, `B338=0`, `B339=0`, `C353=سال مالي منتهي به ۱۴۰۲/۱۲/۲۹`, `C354=درصد مالکيت`, `D354=بهاي تمام شده`, `E354=سال مالي شرکت سرمايه پذير`, `F354=درآمد سرمايه گذاري`, `C355=79`, `D355=1191004`, `E355=۱۴۰۲/۱۰/۳۰`, `F355=237598`, `C356=1`, `D356=122338363`, `E356=۱۴۰۲/۱۰/۳۰`, `F356=20723284`, `C357=100`, `D357=36279443`, `E357=۱۴۰۲/۱۰/۳۰`, `F357=2339955`, `C358=100`, `D358=45109293`, `E358=۱۴۰۲/۱۰/۳۰`, `F358=19999990`, `B361=۱۴۰۲/۱۲/۲۹`, `B363=151543669`, `B365=151543669`, `B367=0`, `B376=۱۴۰۲/۱۲/۲۹`, `B377=43015355`, `B378=0`, `B386=۱۴۰۲/۱۲/۲۹`, `B387=-52654898`, `B395=۱۴۰۲/۱۲/۲۹`, `B396=0`, `B397=0`, `B398=-20082491`

#### Recovered_Sheet1 — Uncolored cells stored in XML (831 cells; value/blank summary)

- with a value: 331 — A3, A9, E13:E28, E31, E34, E36:E38, E40, E42, A44, A46, A48, A53, A59, E62, E68, A72, A78, D82:D94, E82:E95, D97:D107, E97, E101:E102, E105:E107, D109:D119, E109:E111, E113:E116, E118:E119, A123, A129, A169, A175, E179:E181, E183:E185, E187:E190, E193, E195:E196, E198, E207:E213, A221, A223, A225, A230, A235, A237, J240:K243, A243:A244, C243, E243, G243, I243, J245:K249, J251:K254, A254:A256, B254:I254, C256, A258:A259, C259, A261:A262, C262, A265, D269:F271, D273:F273, D275:F275, A276:C276, A278, C280:F283, A284:A285, A289, A294:A296, A298:D299, A301, D303:D308, A309:A310, B310, A312, E315:F332, A333, C333, A335, D337:D340, A340:A341, B340:C340, A345, A350, A352, J355:J358, A360, A369:A372, B369:C370, C372, A375, A380:A382, B380:C380, C382, A385, A389:A391, B389:C389, C391, A394, A399:A401, B399:C399, C401, A406:A407, B407, A409:A411
- blank: 500 — A1:L1, A5:L5, B12, D12:E12, E29:E30, B32, D32, E32:E33, B35, D35:E35, E39, E41, B44:E49, A45, A47, A49, A51:L51, A55:L55, B63, D63, E63:E67, A70:L70, A74:L74, B81:E81, B96:E96, E98:E100, E103:E104, B108:E108, E112, E117, A121:L121, A125:L125, B152:L152, A167:L167, A171:L171, B178, D178:E178, B182, D182:E182, E186, B191, D191, E191:E192, E194, E197, E199:E206, B221:E226, A222, A224, A226, A228:L228, A232:L232, B235:K235, C244, E244, G244, I244:K244, J250:K250, B256, D256:I256, B259, D259:I259, B262, D262:I262, C268:F268, D272:F272, D274:F274, D276:J276, B284:F285, G285:I285, A287:L287, A291:L291, B294:K294, E303:E308, C310:G310, D314:F314, G314:G333, B333, D333:F333, H333:I333, E337:E341, B341:D341, F341:G341, A343:L343, A347:L347, B350:K350, K355:K358, C362, A364, C364, C366, B372, D372:F372, B382, D382:F382, B391, D391:F391, B401, D401:F401, C407:E407, B410:I411
- used-rectangle cells with no `<c>` element: 2807

### 4.2 `Sheet1`

#### Sheet1 — Red (1 cells)

| Coordinate | Value (verbatim) | Excel data type | Blank? | Fill type | Color metadata |
|---|---|---|---|---|---|
| A14 | `صورت سود و زیان جامع` | s (string) | no | solid | in §3.1 |

#### Sheet1 — Blue (10 cells)

| Coordinate | Value (verbatim) | Excel data type | Blank? | Fill type | Color metadata |
|---|---|---|---|---|---|
| A16 | `شرح` | s (string) | no | solid (FF0197C8) | in §3.1 |
| B16 | `دوره منتهي به ۱۴۰۳/۰۶/۳۱` | s (string) | no | solid (FF0197C8) | in §3.1 |
| C16 | `تجدید ارائه شده ۱۴۰۲/۰۶/۳۱` | s (string) | no | solid (FF0197C8) | in §3.1 |
| D16 | `تجدید ارائه شده ۱۴۰۲/۱۲/۲۹` | s (string) | no | solid (FF0197C8) | in §3.1 |
| E16 | `درصد تغییر` | s (string) | no | solid (FF0197C8) | in §3.1 |
| A17 |  | blank (no value stored) | yes | solid (FF0197C8) | in §3.1 |
| B17 | `حسابرسی نشده` | s (string) | no | solid (FF0197C8) | in §3.1 |
| C17 | `حسابرسی شده` | s (string) | no | solid (FF0197C8) | in §3.1 |
| D17 | `حسابرسی شده` | s (string) | no | solid (FF0197C8) | in §3.1 |
| E17 |  | blank (no value stored) | yes | solid (FF0197C8) | in §3.1 |

#### Sheet1 — Green (1 cells)

| Coordinate | Value (verbatim) | Excel data type | Blank? | Fill type | Color metadata |
|---|---|---|---|---|---|
| A19 | `سایر اقلام سود و زیان جامع: ` | s (string) | no | solid | in §3.1 |

#### Sheet1 — Yellow (0 cells)

None.

#### Sheet1 — Gray (0 cells)

None. (No gray cell exists on this worksheet; therefore no blank gray cell exists here.)

#### Sheet1 — Black (0 cells)

None.

#### Sheet1 — Uncolored cells stored in XML (47 cells; value/blank summary)

- with a value: 39 — A1:A12, A15, A18:E18, A20:D24, E24
- blank: 8 — B19:D19, E19:E23
- used-rectangle cells with no `<c>` element: 61

## 5. Border inventory

### 5.1 Border styles stored (all cells, own sides)

**Recovered_Sheet1** — border sides stored by (style, colour): `medium` `rgb:FFDDDDDD` × 5296; `medium` `indexed:64` × 612; `thin` `rgb:FF000000` × 192; `thin` `indexed:64` × 32

**Sheet1** — border sides stored by (style, colour): `medium` `rgb:FFDDDDDD` × 224

Observation: `medium` + `rgb FFDDDDDD` is the ordinary border of the workbook (present on every `<c>` side that has a border on `Sheet1`, and on most of the main sheet). Sides with `indexed 64` / `rgb FF000000` are the non-ordinary ("distinguishable by colour") borders. Style names alone (`medium`/`thin`) do not separate the two: the ordinary border is itself `medium`.

### 5.2 Outer-edge evidence per candidate region

Edge cell series: top edge = min-row cells across the columns, bottom edge = max-row cells, left edge = min-column cells down the rows, right edge = max-column cells. A "distinguishable" side is counted as present if the cell's own side **or** the facing side of the outside neighbour is non-`FFDDDDDD`. "neighbor" lists coordinates whose edge was found only on the outside neighbour cell.

| ID | Bounds | Top | Bottom | Left | Right |
|---|---|---|---|---|---|
| T01 | `A10:D42` | **top**: 4/4 medium indexed:64; continuous | **bottom**: 4/4 medium indexed:64; continuous | **left (min column)**: 33/33 medium indexed:64; continuous | **right (max column)**: 33/33 medium indexed:64; continuous |
| T02 | `A60:D68` | **top**: 4/4 medium indexed:64; continuous | **bottom**: 4/4 medium indexed:64; continuous | **left (min column)**: 9/9 medium indexed:64; continuous | **right (max column)**: 9/9 medium indexed:64; continuous |
| T03 | `A79:C119` | **top**: 3/3 medium indexed:64; continuous | **bottom**: 3/3 medium indexed:64; continuous | **left (min column)**: 41/41 medium indexed:64; continuous | **right (max column)**: 41/41 medium indexed:64; continuous |
| T04 | `A130:L165` | **top**: 12/12 medium indexed:64; continuous | **bottom**: 12/12 medium indexed:64; continuous | **left (min column)**: 36/36 medium indexed:64; continuous | **right (max column)**: 36/36 medium indexed:64; continuous |
| T05 | `A176:D213` | **top**: 4/4 medium indexed:64; continuous | **bottom**: 4/4 medium indexed:64; continuous | **left (min column)**: 38/38 medium indexed:64; continuous | **right (max column)**: 38/38 medium indexed:64; continuous |
| T06 | `A238:I253` | **top**: 9/9 medium indexed:64; continuous | **bottom**: 9/9 medium indexed:64; continuous | **left (min column)**: 16/16 medium indexed:64; continuous | **right (max column)**: 16/16 medium indexed:64; continuous |
| T07 | `A266:C275` | **top**: 3/3 medium indexed:64; continuous | **bottom**: 3/3 medium indexed:64; continuous | **left (min column)**: 10/10 medium indexed:64; continuous | **right (max column)**: 10/10 medium indexed:64; continuous |
| T08 | `A279:B283` | **top**: 2/2 medium indexed:64; continuous | **bottom**: 2/2 medium indexed:64; continuous | **left (min column)**: 5/5 medium indexed:64; continuous | **right (max column)**: 5/5 medium indexed:64; continuous |
| U01 | `A297:D299` | no non-ordinary border side exists around this region |  |  |  |
| T09 | `A302:C308` | **top**: 3/3 medium indexed:64; continuous | **bottom**: 3/3 medium indexed:64; continuous | **left (min column)**: 7/7 medium indexed:64; continuous | **right (max column)**: 7/7 medium indexed:64; continuous |
| T10 | `A313:D332` | **top**: 4/4 medium indexed:64; continuous | **bottom**: 4/4 medium indexed:64; continuous | **left (min column)**: 20/20 medium indexed:64; continuous | **right (max column)**: 20/20 medium indexed:64; continuous |
| T11 | `A336:C339` | **top**: 3/3 medium indexed:64; continuous | **bottom**: 3/3 medium indexed:64; continuous | **left (min column)**: 4/4 medium indexed:64; continuous | **right (max column)**: 4/4 medium indexed:64; continuous |
| T12 | `A353:I358` | **top**: 9/9 medium indexed:64; continuous | **bottom**: 9/9 medium indexed:64; continuous | **left (min column)**: 6/6 medium indexed:64; continuous | **right (max column)**: 6/6 medium indexed:64; continuous |
| T13 | `A361:C367` | **top**: 3/3 medium indexed:64; continuous | **bottom**: 3/3 medium indexed:64; continuous | **left (min column)**: 7/7 medium indexed:64; continuous | **right (max column)**: 7/7 medium indexed:64; continuous |
| T14 | `A376:C378` | **top**: 3/3 medium indexed:64; continuous | **bottom**: 3/3 medium indexed:64; continuous | **left (min column)**: 3/3 medium indexed:64; continuous | **right (max column)**: 3/3 medium indexed:64; continuous |
| T15 | `A386:C387` | **top**: 3/3 medium indexed:64; continuous | **bottom**: 3/3 medium indexed:64; continuous | **left (min column)**: 2/2 medium indexed:64; continuous | **right (max column)**: 2/2 medium indexed:64; continuous |
| T16 | `A395:C398` | **top**: 3/3 thin indexed:64; continuous | **bottom**: 3/3 thin indexed:64; continuous | **left (min column)**: 4/4 thin indexed:64; continuous | **right (max column)**: 4/4 thin indexed:64; continuous |
| T17 | `A404:E405` | **top**: 5/5 thin indexed:64; continuous | **bottom**: 5/5 thin indexed:64; continuous | **left (min column)**: 2/2 thin indexed:64; continuous | **right (max column)**: 2/2 thin indexed:64; continuous |
| S01 | `A16:E24` | no non-ordinary border side exists around this region |  |  |  |

### 5.3 Formatted / bordered regions with non-ordinary borders that are not part of any candidate rectangle

**Recovered_Sheet1**: 195 cells with a non-ordinary border side outside all candidate rectangles.

| Row | Cells | Dark sides | Style / colour | Values on those cells |
|---|---|---|---|---|
| row 1 | A1:L1 | bottom × 12 | thin rgb:FF000000 × 12 | no values |
| row 5 | A5:L5 | bottom × 12 | thin rgb:FF000000 × 12 | no values |
| row 51 | A51:L51 | bottom × 12 | thin rgb:FF000000 × 12 | no values |
| row 55 | A55:L55 | bottom × 12 | thin rgb:FF000000 × 12 | no values |
| row 58 | A58 | left+top × 1 | thin indexed:64 × 2 | `صورت سود و زیان جامع` |
| row 59 | A59 | left × 1 | thin indexed:64 × 1 | `کلیه مبالغ درج شده به میلیون ریال می باشد` |
| row 68 | E68 | bottom × 1 | thin indexed:64 × 1 | `29` |
| row 70 | A70:L70 | bottom × 12 | thin rgb:FF000000 × 12 | no values |
| row 74 | A74:L74 | bottom × 12 | thin rgb:FF000000 × 12 | no values |
| row 121 | A121:L121 | bottom × 12 | thin rgb:FF000000 × 12 | no values |
| row 125 | A125:L125 | bottom × 12 | thin rgb:FF000000 × 12 | no values |
| row 167 | A167:L167 | bottom × 12 | thin rgb:FF000000 × 12 | no values |
| row 171 | A171:L171 | bottom × 12 | thin rgb:FF000000 × 12 | no values |
| row 228 | A228:L228 | bottom × 12 | thin rgb:FF000000 × 12 | no values |
| row 232 | A232:L232 | bottom × 12 | thin rgb:FF000000 × 12 | no values |
| row 287 | A287:L287 | bottom × 12 | thin rgb:FF000000 × 12 | no values |
| row 291 | A291:L291 | bottom × 12 | thin rgb:FF000000 × 12 | no values |
| row 343 | A343:L343 | bottom × 12 | thin rgb:FF000000 × 12 | no values |
| row 347 | A347:L347 | bottom × 12 | thin rgb:FF000000 × 12 | no values |

**Sheet1**: 0 cells with a non-ordinary border side outside all candidate rectangles.

None.

Neighbouring context (facts only): the full-width bottom-border rows are 1, 5, 51, 55, 70, 74, 121, 125, 167, 171, 228, 232, 287, 291, 343, 347 (A:L each). Rows 3, 53, 72, 123, 169, 230, 289, 345 each hold one uncolored title string in column A (e.g. A3 `صورت سود و زیان`, A230 `خلاصه اطلاعات گزارش تفسیری - صفحه 1`). No red/blue/yellow/gray/black/green annotation exists in these bands. Cells A58, A59 and E68 carry non-ordinary sides and belong to the surroundings of T02 (see §7). None of these is associated with a red main-table name as a table.

## 6. Main table candidates

Red cells found: **18** (17 on `Recovered_Sheet1`, 1 on `Sheet1`). Each is listed with its candidate region. A region is a *candidate* only; no claim is made that it is a valid extractable table. Rectangles are the outer boundary of the distinguishable border where one exists, otherwise the extent stated in the Basis column.

| ID | Sheet | Red name cell / value | Bounds | TL / BR | Rows×Cols | Red→top gap | Basis | Blue | Yellow | Gray | Black | Green | Uncolored in rect |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| T01 | Recovered_Sheet1 | A8 `صورت سود و زیان` | `A10:D42` | A10 / D42 | 33×4 | 2 row(s) before top | border | 6 | 28 | 56 (blank 0) | 33 | 3 | 6 |
| T02 | Recovered_Sheet1 | A58 `صورت سود و زیان جامع` | `A60:D68` | A60 / D68 | 9×4 | 2 row(s) before top | border | 6 | 6 | 12 (blank 0) | 9 | 1 | 2 |
| T03 | Recovered_Sheet1 | A77 `صورت وضعیت مالی` | `A79:C119` | A79 / C119 | 41×3 | 2 row(s) before top | border | 9 | 35 | 70 (blank 0) | 0 | 3 | 6 |
| T04 | Recovered_Sheet1 | A128 `صورت تغییرات در حقوق مالکانه` | `A130:L165` | A130 / L165 | 36×12 | 2 row(s) before top | border | 12 | 13 | 143 (blank 85) | 252 | 1 | 11 |
| T05 | Recovered_Sheet1 | A174 `صورت جریان های نقدی` | `A176:D213` | A176 / D213 | 38×4 | 2 row(s) before top | border | 6 | 33 | 66 (blank 0) | 38 | 3 | 6 |
| T06 | Recovered_Sheet1 | A236 `مانده تسهیلات اعطایی و ذخیره مطالبات مشکوک الوصول:` | `A238:I253` | A238 / I253 | 16×9 | 2 row(s) before top | border | 14 | 12 | 48 (blank 4) | 60 | 0 | 10 |
| T07 | Recovered_Sheet1 | A264 `مانده سپرده های دریافتی از مشتریان :` | `A266:C275` | A266 / C275 | 10×3 | 2 row(s) before top | border | 5 | 7 | 7 (blank 0) | 9 | 1 | 1 |
| T08 | Recovered_Sheet1 | A277 `اقلام زیر خط:` | `A279:B283` | A279 / B283 | 5×2 | 2 row(s) before top | border | 2 | 4 | 4 (blank 0) | 0 | 0 | 0 |
| U01 | Recovered_Sheet1 | — (no red cell) | `A297:D299` | A297 / D299 | 3×4 | — | no border; extent from blue header + contiguous valued rows | 4 | 0 | 0 (blank 0) | 0 | 0 | 8 |
| T09 | Recovered_Sheet1 | A300 `اطلاعات حق الوکاله و کفایت سرمایه` | `A302:C308` | A302 / C308 | 7×3 | 2 row(s) before top | border | 2 | 6 | 6 (blank 0) | 7 | 0 | 0 |
| T10 | Recovered_Sheet1 | A311 `درآمد حاصل از تسهيلات اعطايي و سپرده گذاري` | `A313:D332` | A313 / D332 | 20×4 | 2 row(s) before top | border | 2 | 18 | 18 (blank 0) | 40 | 1 | 1 |
| T11 | Recovered_Sheet1 | A334 `خالص سود (زیان) سرمایه گذاری‌ ها` | `A336:C339` | A336 / C339 | 4×3 | 2 row(s) before top | border | 2 | 3 | 3 (blank 0) | 4 | 0 | 0 |
| T12 | Recovered_Sheet1 | A351 `وضعیت شرکتهای سرمایه پذیر:` | `A353:I358` | A353 / I358 | 6×9 | 2 row(s) before top | border | 10 | 8 | 12 (blank 0) | 24 | 0 | 0 |
| T13 | Recovered_Sheet1 | A359 `ساير درآمدها و هزینه های عملياتي:` | `A361:C367` | A361 / C367 | 7×3 | 2 row(s) before top | border | 2 | 3 | 3 (blank 0) | 7 | 2 | 4 |
| T14 | Recovered_Sheet1 | A374 `خالص ساير درآمدها و هزینه ها:` | `A376:C378` | A376 / C378 | 3×3 | 2 row(s) before top | border | 2 | 2 | 2 (blank 0) | 3 | 0 | 0 |
| T15 | Recovered_Sheet1 | A384 `هزینه های اداری و عمومی:` | `A386:C387` | A386 / C387 | 2×3 | 2 row(s) before top | border | 2 | 1 | 1 (blank 0) | 2 | 0 | 0 |
| T16 | Recovered_Sheet1 | A393 `هزینه مالی:` | `A395:C398` | A395 / C398 | 4×3 | 2 row(s) before top | border | 2 | 3 | 3 (blank 0) | 4 | 0 | 0 |
| T17 | Recovered_Sheet1 | A403 `برنامه شرکت در خصوص تقسیم سود` | `A404:E405` | A404 / E405 | 2×5 | 1 row(s) before top | border | 5 | 0 | 5 (blank 0) | 0 | 0 | 0 |
| S01 | Sheet1 | A14 `صورت سود و زیان جامع` | `A16:E24` | A16 / E24 | 9×5 | 2 row(s) before top | no border; extent from blue header + contiguous valued rows | 10 | 0 | 0 (blank 0) | 0 | 1 | 34 |

Red cells and their position relative to the nearest bordered/annotated region (red row, first row of the bordered/annotated region):

| Sheet | Red cell | Value | Raw fill | Position relative to candidate |
|---|---|---|---|---|
| Recovered_Sheet1 | A8 | `صورت سود و زیان` | solid / rgb / FFFF0000 / tint 0.0 | T01 (rows 10–42); table top is 2 row(s) after the red row; red cell column index 1 = region min column 1 |
| Recovered_Sheet1 | A58 | `صورت سود و زیان جامع` | solid / rgb / FFFF0000 / tint 0.0 | T02 (rows 60–68); table top is 2 row(s) after the red row; red cell column index 1 = region min column 1 |
| Recovered_Sheet1 | A77 | `صورت وضعیت مالی` | solid / rgb / FFFF0000 / tint 0.0 | T03 (rows 79–119); table top is 2 row(s) after the red row; red cell column index 1 = region min column 1 |
| Recovered_Sheet1 | A128 | `صورت تغییرات در حقوق مالکانه` | solid / rgb / FFFF0000 / tint 0.0 | T04 (rows 130–165); table top is 2 row(s) after the red row; red cell column index 1 = region min column 1 |
| Recovered_Sheet1 | A174 | `صورت جریان های نقدی` | solid / rgb / FFFF0000 / tint 0.0 | T05 (rows 176–213); table top is 2 row(s) after the red row; red cell column index 1 = region min column 1 |
| Recovered_Sheet1 | A236 | `مانده تسهیلات اعطایی و ذخیره مطالبات مشکوک الوصول:` | solid / rgb / FFFF0000 / tint 0.0 | T06 (rows 238–253); table top is 2 row(s) after the red row; red cell column index 1 = region min column 1 |
| Recovered_Sheet1 | A264 | `مانده سپرده های دریافتی از مشتریان :` | solid / rgb / FFFF0000 / tint 0.0 | T07 (rows 266–275); table top is 2 row(s) after the red row; red cell column index 1 = region min column 1 |
| Recovered_Sheet1 | A277 | `اقلام زیر خط:` | solid / rgb / FFFF0000 / tint 0.0 | T08 (rows 279–283); table top is 2 row(s) after the red row; red cell column index 1 = region min column 1 |
| Recovered_Sheet1 | A300 | `اطلاعات حق الوکاله و کفایت سرمایه` | solid / rgb / FFFF0000 / tint 0.0 | T09 (rows 302–308); table top is 2 row(s) after the red row; red cell column index 1 = region min column 1 |
| Recovered_Sheet1 | A311 | `درآمد حاصل از تسهيلات اعطايي و سپرده گذاري` | solid / rgb / FFFF0000 / tint 0.0 | T10 (rows 313–332); table top is 2 row(s) after the red row; red cell column index 1 = region min column 1 |
| Recovered_Sheet1 | A334 | `خالص سود (زیان) سرمایه گذاری‌ ها` | solid / rgb / FFFF0000 / tint 0.0 | T11 (rows 336–339); table top is 2 row(s) after the red row; red cell column index 1 = region min column 1 |
| Recovered_Sheet1 | A351 | `وضعیت شرکتهای سرمایه پذیر:` | solid / rgb / FFFF0000 / tint 0.0 | T12 (rows 353–358); table top is 2 row(s) after the red row; red cell column index 1 = region min column 1 |
| Recovered_Sheet1 | A359 | `ساير درآمدها و هزینه های عملياتي:` | solid / rgb / FFFF0000 / tint 0.0 | T13 (rows 361–367); table top is 2 row(s) after the red row; red cell column index 1 = region min column 1 |
| Recovered_Sheet1 | A374 | `خالص ساير درآمدها و هزینه ها:` | solid / rgb / FFFF0000 / tint 0.0 | T14 (rows 376–378); table top is 2 row(s) after the red row; red cell column index 1 = region min column 1 |
| Recovered_Sheet1 | A384 | `هزینه های اداری و عمومی:` | solid / rgb / FFFF0000 / tint 0.0 | T15 (rows 386–387); table top is 2 row(s) after the red row; red cell column index 1 = region min column 1 |
| Recovered_Sheet1 | A393 | `هزینه مالی:` | solid / rgb / FFFF0000 / tint 0.0 | T16 (rows 395–398); table top is 2 row(s) after the red row; red cell column index 1 = region min column 1 |
| Recovered_Sheet1 | A403 | `برنامه شرکت در خصوص تقسیم سود` | solid / rgb / FFFF0000 / tint 0.0 | T17 (rows 404–405); table top is 1 row(s) after the red row; red cell column index 1 = region min column 1 |
| Sheet1 | A14 | `صورت سود و زیان جامع` | solid / rgb / FFFF0000 / tint 0.0 | S01 (rows 16–24); table top is 2 row(s) after the red row; red cell column index 1 = region min column 1 |

## 7. Detailed evidence for every candidate table

Legend: **observed facts** only. "Uncolored in rect" = `<c>` elements inside the rectangle with no fill; "absent" = rectangle positions with no `<c>` element. Values are verbatim.

### T01 — `Recovered_Sheet1` `A10:D42` — red name A8

| Evidence | Observed |
|---|---|
| Worksheet | `Recovered_Sheet1` (rightToLeft = True) |
| Exact bounds | `A10:D42`; top-left A10, bottom-right D42; 33 rows × 4 columns = 132 cells |
| Basis for bounds | border |
| Red main-name cell | A8 = `صورت سود و زیان` (raw fill `FFFF0000`); 2 row(s) above the region top |
| Blue header cells (6) | A10:B11, D10:D11 |
| Yellow description cells (28) | A13:A31, A33:A34, A36:A42 |
| Gray extraction cells (56): numeric 56, blank 0 | all: B13:B31, D13:D31, B33:B34, D33:D34, B36:B42, D36:D42; no blank gray |
| Black excluded cells (33) | C10:C42 |
| Green sub-table markers (3) | A12 `عملیات در حال تداوم: `, A32 `عملیات متوقف شده: `, A35 `سود (زیان)پایه هر سهم (ريال) ` |
| Uncolored cells in rect (6) | with value: —; blank: B12, D12, B32, D32, B35, D35 |
| Positions with no `<c>` in rect | 0 — — |
| Merged ranges intersecting | `A10:A11` (inside) |
| Border top (stored attribute top) | 4/4 medium indexed:64; continuous |
| Border bottom (stored attribute bottom) | 4/4 medium indexed:64; continuous |
| Border left (stored attribute left) | 33/33 medium indexed:64; continuous |
| Border right (stored attribute right) | 33/33 medium indexed:64; continuous |
| Distinguishable from ordinary cell borders? | Yes by colour test: every outer-edge side found is non-`FFDDDDDD` (medium indexed:64); ordinary interior sides are `medium` `rgb:FFDDDDDD` |
| Non-ordinary border sides on cells just OUTSIDE the rectangle | none |
| Non-ordinary border sides on interior (non-perimeter) positions | none |

**Cells outside the rectangle that appear related by position (listed, NOT included in the region):**

- Same rows, outside columns: E10:E11, E13:E28, E31, E34, E36:E38, E40, E42 (25 cells; first 25: E10[Blue]=`درصد تغييرات`, E11[Blue], E13[uncolored]=`69`, E14[uncolored]=`-46`, E15[uncolored]=`-18`, E16[uncolored]=`41`, E17[uncolored]=`-104`, E18[uncolored]=`21`, E19[uncolored]=`-79`, E20[uncolored]=`17`, E21[uncolored]=`346`, E22[uncolored]=`158`, E23[uncolored]=`-95`, E24[uncolored]=`-38`, E25[uncolored]=`-140`, E26[uncolored]=`17`, E27[uncolored]=`-80`, E28[uncolored]=`29`, E31[uncolored]=`29`, E34[uncolored]=`29`, E36[uncolored]=`63`, E37[uncolored]=`-113`, E38[uncolored]=`28`, E40[uncolored]=`28`, E42[uncolored]=`0`)
- Rows between red name and region top: A9 (1 cells; first 1: A9[uncolored]=`کلیه مبالغ درج شده به میلیون`)
- Contiguous rows immediately below: none

Column-wise roles inside the rectangle (column index order):

| Column | Blue | Yellow | Gray | Black | Green | Uncolored | Absent |
|---|---|---|---|---|---|---|---|
| A | 2 | 28 | 0 | 0 | 3 | 0 | 0 |
| B | 2 | 0 | 28 | 0 | 0 | 3 | 0 |
| C | 0 | 0 | 0 | 33 | 0 | 0 | 0 |
| D | 2 | 0 | 28 | 0 | 0 | 3 | 0 |

### T02 — `Recovered_Sheet1` `A60:D68` — red name A58

| Evidence | Observed |
|---|---|
| Worksheet | `Recovered_Sheet1` (rightToLeft = True) |
| Exact bounds | `A60:D68`; top-left A60, bottom-right D68; 9 rows × 4 columns = 36 cells |
| Basis for bounds | border |
| Red main-name cell | A58 = `صورت سود و زیان جامع` (raw fill `FFFF0000`); 2 row(s) above the region top |
| Blue header cells (6) | A60:B61, D60:D61 |
| Yellow description cells (6) | A62, A64:A68 |
| Gray extraction cells (12): numeric 12, blank 0 | all: B62, D62, B64:B68, D64:D68; no blank gray |
| Black excluded cells (9) | C60:C68 |
| Green sub-table markers (1) | A63 `سایر اقلام سود و زیان جامع: ` |
| Uncolored cells in rect (2) | with value: —; blank: B63, D63 |
| Positions with no `<c>` in rect | 0 — — |
| Merged ranges intersecting | `A60:A61` (inside) |
| Border top (stored attribute top) | 4/4 medium indexed:64; continuous |
| Border bottom (stored attribute bottom) | 4/4 medium indexed:64; continuous |
| Border left (stored attribute left) | 9/9 medium indexed:64; continuous |
| Border right (stored attribute right) | 9/9 medium indexed:64; continuous |
| Distinguishable from ordinary cell borders? | Yes by colour test: every outer-edge side found is non-`FFDDDDDD` (medium indexed:64); ordinary interior sides are `medium` `rgb:FFDDDDDD` |
| Non-ordinary border sides on cells just OUTSIDE the rectangle | A58 (left+top; thin indexed:64); A59 (left; thin indexed:64); E68 (bottom; thin indexed:64) |
| Non-ordinary border sides on interior (non-perimeter) positions | none |

**Cells outside the rectangle that appear related by position (listed, NOT included in the region):**

- Same rows, outside columns: E60:E62, E68 (4 cells; first 4: E60[Blue]=`درصد تغییر`, E61[Blue], E62[uncolored]=`29`, E68[uncolored]=`29`)
- Rows between red name and region top: A59 (1 cells; first 1: A59[uncolored]=`کلیه مبالغ درج شده به میلیون`)
- Contiguous rows immediately below: none

Column-wise roles inside the rectangle (column index order):

| Column | Blue | Yellow | Gray | Black | Green | Uncolored | Absent |
|---|---|---|---|---|---|---|---|
| A | 2 | 6 | 0 | 0 | 1 | 0 | 0 |
| B | 2 | 0 | 6 | 0 | 0 | 1 | 0 |
| C | 0 | 0 | 0 | 9 | 0 | 0 | 0 |
| D | 2 | 0 | 6 | 0 | 0 | 1 | 0 |

### T03 — `Recovered_Sheet1` `A79:C119` — red name A77

| Evidence | Observed |
|---|---|
| Worksheet | `Recovered_Sheet1` (rightToLeft = True) |
| Exact bounds | `A79:C119`; top-left A79, bottom-right C119; 41 rows × 3 columns = 123 cells |
| Basis for bounds | border |
| Red main-name cell | A77 = `صورت وضعیت مالی` (raw fill `FFFF0000`); 2 row(s) above the region top |
| Blue header cells (9) | A79:C80, A95:C95 — of which raw shade FF0070C0: A95:C95 |
| Yellow description cells (35) | A82:A94, A97:A107, A109:A119 |
| Gray extraction cells (70): numeric 70, blank 0 | all: B82:C94, B97:C107, B109:C119; no blank gray |
| Black excluded cells (0) | — |
| Green sub-table markers (3) | A81 `دارایی ها `, A96 `حقوق مالکانه `, A108 `بدهی‌ها ` |
| Uncolored cells in rect (6) | with value: —; blank: B81:C81, B96:C96, B108:C108 |
| Positions with no `<c>` in rect | 0 — — |
| Merged ranges intersecting | `A79:A80` (inside) |
| Border top (stored attribute top) | 3/3 medium indexed:64; continuous |
| Border bottom (stored attribute bottom) | 3/3 medium indexed:64; continuous |
| Border left (stored attribute left) | 41/41 medium indexed:64; continuous |
| Border right (stored attribute right) | 41/41 medium indexed:64; continuous |
| Distinguishable from ordinary cell borders? | Yes by colour test: every outer-edge side found is non-`FFDDDDDD` (medium indexed:64); ordinary interior sides are `medium` `rgb:FFDDDDDD` |
| Non-ordinary border sides on cells just OUTSIDE the rectangle | none |
| Non-ordinary border sides on interior (non-perimeter) positions | none |

**Cells outside the rectangle that appear related by position (listed, NOT included in the region):**

- Same rows, outside columns: D79:E80, D82:E95, D97:D107, E97, E101:E102, E105:E107, D109:D119, E109:E111, E113:E116, E118:E119 (69 cells; first 25: D79[Blue]=`تجدید ارائه شده ۱۴۰۲/۰۱/۰۱`, E79[Blue]=`درصد تغييرات`, D80[Blue]=`حسابرسی نشده`, E80[Blue], D82[uncolored]=`229326967`, E82[uncolored]=`18`, D83[uncolored]=`445765962`, E83[uncolored]=`-2`, D84[uncolored]=`3017721`, E84[uncolored]=`0`, D85[uncolored]=`21974278`, E85[uncolored]=`10`, D86[uncolored]=`2127527442`, E86[uncolored]=`6`, D87[uncolored]=`216322535`, E87[uncolored]=`5`, D88[uncolored]=`76148371`, E88[uncolored]=`-1`, D89[uncolored]=`308845970`, E89[uncolored]=`7`, D90[uncolored]=`15760214`, E90[uncolored]=`3`, D91[uncolored]=`22491788`, E91[uncolored]=`0`, D92[uncolored]=`212206595`)
- Rows between red name and region top: A78 (1 cells; first 1: A78[uncolored]=`کلیه مبالغ درج شده به میلیون`)
- Contiguous rows immediately below: none

Column-wise roles inside the rectangle (column index order):

| Column | Blue | Yellow | Gray | Black | Green | Uncolored | Absent |
|---|---|---|---|---|---|---|---|
| A | 3 | 35 | 0 | 0 | 3 | 0 | 0 |
| B | 3 | 0 | 35 | 0 | 0 | 3 | 0 |
| C | 3 | 0 | 35 | 0 | 0 | 3 | 0 |

### T04 — `Recovered_Sheet1` `A130:L165` — red name A128

| Evidence | Observed |
|---|---|
| Worksheet | `Recovered_Sheet1` (rightToLeft = True) |
| Exact bounds | `A130:L165`; top-left A130, bottom-right L165; 36 rows × 12 columns = 432 cells |
| Basis for bounds | border |
| Red main-name cell | A128 = `صورت تغییرات در حقوق مالکانه` (raw fill `FFFF0000`); 2 row(s) above the region top |
| Blue header cells (12) | A130:L130 |
| Yellow description cells (13) | A153:A165 |
| Gray extraction cells (143): numeric 58, blank 85 | all: B153:L165; **blank gray**: B153:G154, H153:I153, K153:K154, J154, B156, C156:C157, D156:E156, F156:F162, G156:I156, K156:K158, D158:D164, E158:E160, G158:G163, H158:I161, B159:C164, J159:J161, K161:K164, E163:E164, H163:I164, F164 |
| Black excluded cells (252) | A131:L151 |
| Green sub-table markers (1) | A152 `تغییرات حقوق مالکانه در سال ۱۴۰۳/۰۶/۳۱ ` |
| Uncolored cells in rect (11) | with value: —; blank: B152:L152 |
| Positions with no `<c>` in rect | 0 — — |
| Merged ranges intersecting | none intersect |
| Border top (stored attribute top) | 12/12 medium indexed:64; continuous |
| Border bottom (stored attribute bottom) | 12/12 medium indexed:64; continuous |
| Border left (stored attribute left) | 36/36 medium indexed:64; continuous |
| Border right (stored attribute right) | 36/36 medium indexed:64; continuous |
| Distinguishable from ordinary cell borders? | Yes by colour test: every outer-edge side found is non-`FFDDDDDD` (medium indexed:64); ordinary interior sides are `medium` `rgb:FFDDDDDD` |
| Non-ordinary border sides on cells just OUTSIDE the rectangle | none |
| Non-ordinary border sides on interior (non-perimeter) positions | none |

**Cells outside the rectangle that appear related by position (listed, NOT included in the region):**

- Same rows, outside columns: none
- Rows between red name and region top: A129 (1 cells; first 1: A129[uncolored]=`کلیه مبالغ درج شده به میلیون`)
- Contiguous rows immediately below: none

Column-wise roles inside the rectangle (column index order):

| Column | Blue | Yellow | Gray | Black | Green | Uncolored | Absent |
|---|---|---|---|---|---|---|---|
| A | 1 | 13 | 0 | 21 | 1 | 0 | 0 |
| B | 1 | 0 | 13 | 21 | 0 | 1 | 0 |
| C | 1 | 0 | 13 | 21 | 0 | 1 | 0 |
| D | 1 | 0 | 13 | 21 | 0 | 1 | 0 |
| E | 1 | 0 | 13 | 21 | 0 | 1 | 0 |
| F | 1 | 0 | 13 | 21 | 0 | 1 | 0 |
| G | 1 | 0 | 13 | 21 | 0 | 1 | 0 |
| H | 1 | 0 | 13 | 21 | 0 | 1 | 0 |
| I | 1 | 0 | 13 | 21 | 0 | 1 | 0 |
| J | 1 | 0 | 13 | 21 | 0 | 1 | 0 |
| K | 1 | 0 | 13 | 21 | 0 | 1 | 0 |
| L | 1 | 0 | 13 | 21 | 0 | 1 | 0 |

### T05 — `Recovered_Sheet1` `A176:D213` — red name A174

| Evidence | Observed |
|---|---|
| Worksheet | `Recovered_Sheet1` (rightToLeft = True) |
| Exact bounds | `A176:D213`; top-left A176, bottom-right D213; 38 rows × 4 columns = 152 cells |
| Basis for bounds | border |
| Red main-name cell | A174 = `صورت جریان های نقدی` (raw fill `FFFF0000`); 2 row(s) above the region top |
| Blue header cells (6) | A176:B177, D176:D177 |
| Yellow description cells (33) | A179:A181, A183:A190, A192:A213 |
| Gray extraction cells (66): numeric 66, blank 0 | all: B179:B181, D179:D181, B183:B190, D183:D190, B192:B213, D192:D213; no blank gray |
| Black excluded cells (38) | C176:C213 |
| Green sub-table markers (3) | A178 `جریان­های نقدی حاصل از فعاليت‌هاي عملياتي: `, A182 `فعاليت‌هاي سرمایه‌گذاری `, A191 `فعاليت‌هاي تأمين مالي ` |
| Uncolored cells in rect (6) | with value: —; blank: B178, D178, B182, D182, B191, D191 |
| Positions with no `<c>` in rect | 0 — — |
| Merged ranges intersecting | `A176:A177` (inside) |
| Border top (stored attribute top) | 4/4 medium indexed:64; continuous |
| Border bottom (stored attribute bottom) | 4/4 medium indexed:64; continuous |
| Border left (stored attribute left) | 38/38 medium indexed:64; continuous |
| Border right (stored attribute right) | 38/38 medium indexed:64; continuous |
| Distinguishable from ordinary cell borders? | Yes by colour test: every outer-edge side found is non-`FFDDDDDD` (medium indexed:64); ordinary interior sides are `medium` `rgb:FFDDDDDD` |
| Non-ordinary border sides on cells just OUTSIDE the rectangle | none |
| Non-ordinary border sides on interior (non-perimeter) positions | none |

**Cells outside the rectangle that appear related by position (listed, NOT included in the region):**

- Same rows, outside columns: E176:E177, E179:E181, E183:E185, E187:E190, E193, E195:E196, E198, E207:E213 (23 cells; first 23: E176[Blue]=`درصد تغییر`, E177[Blue], E179[uncolored]=`73`, E180[uncolored]=`-Infinity`, E181[uncolored]=`71`, E183[uncolored]=`76`, E184[uncolored]=`-52`, E185[uncolored]=`10`, E187[uncolored]=`-99`, E188[uncolored]=`-99`, E189[uncolored]=`-158`, E190[uncolored]=`49`, E193[uncolored]=`-100`, E195[uncolored]=`36`, E196[uncolored]=`-17`, E198[uncolored]=`100`, E207[uncolored]=`-437111`, E208[uncolored]=`25`, E209[uncolored]=`58`, E210[uncolored]=`29`, E211[uncolored]=`344`, E212[uncolored]=`104`, E213[uncolored]=`977`)
- Rows between red name and region top: A175 (1 cells; first 1: A175[uncolored]=`کلیه مبالغ به میلیون ریال اس`)
- Contiguous rows immediately below: none

Column-wise roles inside the rectangle (column index order):

| Column | Blue | Yellow | Gray | Black | Green | Uncolored | Absent |
|---|---|---|---|---|---|---|---|
| A | 2 | 33 | 0 | 0 | 3 | 0 | 0 |
| B | 2 | 0 | 33 | 0 | 0 | 3 | 0 |
| C | 0 | 0 | 0 | 38 | 0 | 0 | 0 |
| D | 2 | 0 | 33 | 0 | 0 | 3 | 0 |

### T06 — `Recovered_Sheet1` `A238:I253` — red name A236

| Evidence | Observed |
|---|---|
| Worksheet | `Recovered_Sheet1` (rightToLeft = True) |
| Exact bounds | `A238:I253`; top-left A238, bottom-right I253; 16 rows × 9 columns = 144 cells |
| Basis for bounds | border |
| Red main-name cell | A236 = `مانده تسهیلات اعطایی و ذخیره مطالبات مشکوک الوصول:` (raw fill `FFFF0000`); 2 row(s) above the region top |
| Blue header cells (14) | A238:A239, C238:C239, E238:E239, G238:G239, I238:I239, B239, D239, F239, H239 |
| Yellow description cells (12) | A240:A242, A245:A253 |
| Gray extraction cells (48): numeric 44, blank 4 | all: C240:C242, E240:E242, G240:G242, I240:I242, C245:C253, E245:E253, G245:G253, I245:I253; **blank gray**: C248:C251 |
| Black excluded cells (60) | B238, D238, F238, H238, B240:B253, D240:D253, F240:F253, H240:H253 |
| Green sub-table markers (0) | none |
| Uncolored cells in rect (10) | with value: A243:A244, C243, E243, G243, I243; blank: C244, E244, G244, I244 |
| Positions with no `<c>` in rect | 0 — — |
| Merged ranges intersecting | `A238:A239` (inside); `B239:C239` (inside); `D239:E239` (inside); `F239:G239` (inside); `H239:I239` (inside) |
| Border top (stored attribute top) | 9/9 medium indexed:64; continuous |
| Border bottom (stored attribute bottom) | 9/9 medium indexed:64; continuous |
| Border left (stored attribute left) | 16/16 medium indexed:64; continuous |
| Border right (stored attribute right) | 16/16 medium indexed:64; continuous |
| Distinguishable from ordinary cell borders? | Yes by colour test: every outer-edge side found is non-`FFDDDDDD` (medium indexed:64); ordinary interior sides are `medium` `rgb:FFDDDDDD` |
| Non-ordinary border sides on cells just OUTSIDE the rectangle | none |
| Non-ordinary border sides on interior (non-perimeter) positions | none |

**Cells outside the rectangle that appear related by position (listed, NOT included in the region):**

- Same rows, outside columns: J238:K243, J245:K249, J251:K253 (28 cells; first 25: J238[Blue]=`در تاریخ ۱۴۰۲/۱۲/۲۹`, K238[Blue]=`در تاریخ ۱۴۰۳/۰۶/۳۱`, J239[Blue]=`جمع`, K239[Blue], J240[uncolored]=`5024806`, K240[uncolored]=`5601562`, J241[uncolored]=`1390800083`, K241[uncolored]=`1436685810`, J242[uncolored]=`1603912860`, K242[uncolored]=`1701920891`, J243[uncolored]=`2999737749`, K243[uncolored]=`3144208263`, J245[uncolored]=`161368315`, K245[uncolored]=`145007474`, J246[uncolored]=`1`, K246[uncolored]=`4817501`, J247[uncolored]=`2838369433`, K247[uncolored]=`2994383288`, J248[uncolored]=`118342693`, K248[uncolored]=`235342693`, J249[uncolored]=`1082832642`, K249[uncolored]=`1078232895`, J251[uncolored]=`118319470`, K251[uncolored]=`129319470`, J252[uncolored]=`2720049963`)
- Rows between red name and region top: A237 (1 cells; first 1: A237[uncolored]=`کلیه مبالغ درج شده به میلیون`)
- Contiguous rows immediately below: A254:A256, B254:K254, C256 (14 cells; first 14: A254[uncolored]=`جمع`, B254[uncolored]=`2125074730`, C254[uncolored]=`2171959923`, D254[uncolored]=`351152487`, E254[uncolored]=`310581307`, F254[uncolored]=`4618776`, G254[uncolored]=`61747351`, H254[uncolored]=`206780064`, I254[uncolored]=`273928811`, J254[uncolored]=`2687626057`, K254[uncolored]=`2818217392`, A255[uncolored]=`برآورد شرکت از تغییرات در نر`, A256[uncolored]=`دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲`, C256[uncolored]=`با توجه به سیاستهای پولی و ب`)

Column-wise roles inside the rectangle (column index order):

| Column | Blue | Yellow | Gray | Black | Green | Uncolored | Absent |
|---|---|---|---|---|---|---|---|
| A | 2 | 12 | 0 | 0 | 0 | 2 | 0 |
| B | 1 | 0 | 0 | 15 | 0 | 0 | 0 |
| C | 2 | 0 | 12 | 0 | 0 | 2 | 0 |
| D | 1 | 0 | 0 | 15 | 0 | 0 | 0 |
| E | 2 | 0 | 12 | 0 | 0 | 2 | 0 |
| F | 1 | 0 | 0 | 15 | 0 | 0 | 0 |
| G | 2 | 0 | 12 | 0 | 0 | 2 | 0 |
| H | 1 | 0 | 0 | 15 | 0 | 0 | 0 |
| I | 2 | 0 | 12 | 0 | 0 | 2 | 0 |

### T07 — `Recovered_Sheet1` `A266:C275` — red name A264

| Evidence | Observed |
|---|---|
| Worksheet | `Recovered_Sheet1` (rightToLeft = True) |
| Exact bounds | `A266:C275`; top-left A266, bottom-right C275; 10 rows × 3 columns = 30 cells |
| Basis for bounds | border |
| Red main-name cell | A264 = `مانده سپرده های دریافتی از مشتریان :` (raw fill `FFFF0000`); 2 row(s) above the region top |
| Blue header cells (5) | A266:A267, B266, C266:C267 |
| Yellow description cells (7) | A269:A275 |
| Gray extraction cells (7): numeric 7, blank 0 | all: C269:C275; no blank gray |
| Black excluded cells (9) | B267:B275 |
| Green sub-table markers (1) | A268 `سپرده های ریالی: ` |
| Uncolored cells in rect (1) | with value: —; blank: C268 |
| Positions with no `<c>` in rect | 0 — — |
| Merged ranges intersecting | `A266:A267` (inside); `B266:C266` (inside) |
| Border top (stored attribute top) | 3/3 medium indexed:64; continuous |
| Border bottom (stored attribute bottom) | 3/3 medium indexed:64; continuous |
| Border left (stored attribute left) | 10/10 medium indexed:64; continuous |
| Border right (stored attribute right) | 10/10 medium indexed:64; continuous |
| Distinguishable from ordinary cell borders? | Yes by colour test: every outer-edge side found is non-`FFDDDDDD` (medium indexed:64); ordinary interior sides are `medium` `rgb:FFDDDDDD` |
| Non-ordinary border sides on cells just OUTSIDE the rectangle | none |
| Non-ordinary border sides on interior (non-perimeter) positions | none |

**Cells outside the rectangle that appear related by position (listed, NOT included in the region):**

- Same rows, outside columns: D266:F267, D269:F271, D273:F273, D275:F275 (21 cells; first 21: D266[Blue]=`متوسط نرخ سود مانده سپرده ها`, E266[Blue], F266[Blue]=`برآورد مدیریت از تغییر در نر`, D267[Blue]=`در تاریخ ۱۴۰۲/۱۲/۲۹`, E267[Blue]=`در تاریخ ۱۴۰۳/۰۶/۳۱`, F267[Blue], D269[uncolored]=`0`, E269[uncolored]=`0`, F269[uncolored]=`با توجه به سیاستهای پولی و ب`, D270[uncolored]=`0`, E270[uncolored]=`0`, F270[uncolored]=`با توجه به سیاستهای پولی و ب`, D271[uncolored]=`0`, E271[uncolored]=`0`, F271[uncolored]=`با توجه به سیاستهای پولی و ب`, D273[uncolored]=`0`, E273[uncolored]=`0`, F273[uncolored]=`با توجه به سیاستهای پولی و ب`, D275[uncolored]=`0`, E275[uncolored]=`0`, F275[uncolored]=`با توجه به سیاستهای پولی و ب`)
- Rows between red name and region top: A265 (1 cells; first 1: A265[uncolored]=`کلیه مبالغ درج شده به میلیون`)
- Contiguous rows immediately below: A276:A285, B276:C276, B279:F283 (37 cells; first 25: A276[uncolored]=`جمع سپرده های دریافتی`, B276[uncolored]=`3132825929`, C276[uncolored]=`3279547611`, A277[Red]=`اقلام زیر خط:`, A278[uncolored]=`کلیه مبالغ درج شده به میلیون`, A279[Blue]=`شرح`, B279[Blue]=`۱۴۰۳/۰۶/۳۱`, C279[Blue]=`۱۴۰۲/۱۲/۲۹`, D279[Blue]=`شرح`, E279[Blue]=`۱۴۰۳/۰۶/۳۱`, F279[Blue]=`۱۴۰۲/۱۲/۲۹`, A280[Yellow]=`تعهدات مشتریان بابت اعتبارات`, B280[Gray]=`439498515`, C280[uncolored]=`425497756`, D280[uncolored]=`تعهدات بانک بابت اعتبارات اس`, E280[uncolored]=`439498515`, F280[uncolored]=`425497756`, A281[Yellow]=`تعهدات مشتریان بابت ضمانت نا`, B281[Gray]=`705682218`, C281[uncolored]=`620594993`, D281[uncolored]=`تعهدات بانک بابت ضمانت نامه `, E281[uncolored]=`705682218`, F281[uncolored]=`620594993`, A282[Yellow]=`ساير تعهدات مشتريان بانک`, B282[Gray]=`19498400`)

Column-wise roles inside the rectangle (column index order):

| Column | Blue | Yellow | Gray | Black | Green | Uncolored | Absent |
|---|---|---|---|---|---|---|---|
| A | 2 | 7 | 0 | 0 | 1 | 0 | 0 |
| B | 1 | 0 | 0 | 9 | 0 | 0 | 0 |
| C | 2 | 0 | 7 | 0 | 0 | 1 | 0 |

### T08 — `Recovered_Sheet1` `A279:B283` — red name A277

| Evidence | Observed |
|---|---|
| Worksheet | `Recovered_Sheet1` (rightToLeft = True) |
| Exact bounds | `A279:B283`; top-left A279, bottom-right B283; 5 rows × 2 columns = 10 cells |
| Basis for bounds | border |
| Red main-name cell | A277 = `اقلام زیر خط:` (raw fill `FFFF0000`); 2 row(s) above the region top |
| Blue header cells (2) | A279:B279 |
| Yellow description cells (4) | A280:A283 |
| Gray extraction cells (4): numeric 4, blank 0 | all: B280:B283; no blank gray |
| Black excluded cells (0) | — |
| Green sub-table markers (0) | none |
| Uncolored cells in rect (0) | with value: —; blank: — |
| Positions with no `<c>` in rect | 0 — — |
| Merged ranges intersecting | none intersect |
| Border top (stored attribute top) | 2/2 medium indexed:64; continuous |
| Border bottom (stored attribute bottom) | 2/2 medium indexed:64; continuous |
| Border left (stored attribute left) | 5/5 medium indexed:64; continuous |
| Border right (stored attribute right) | 5/5 medium indexed:64; continuous |
| Distinguishable from ordinary cell borders? | Yes by colour test: every outer-edge side found is non-`FFDDDDDD` (medium indexed:64); ordinary interior sides are `medium` `rgb:FFDDDDDD` |
| Non-ordinary border sides on cells just OUTSIDE the rectangle | none |
| Non-ordinary border sides on interior (non-perimeter) positions | none |

**Cells outside the rectangle that appear related by position (listed, NOT included in the region):**

- Same rows, outside columns: C279:F283 (20 cells; first 20: C279[Blue]=`۱۴۰۲/۱۲/۲۹`, D279[Blue]=`شرح`, E279[Blue]=`۱۴۰۳/۰۶/۳۱`, F279[Blue]=`۱۴۰۲/۱۲/۲۹`, C280[uncolored]=`425497756`, D280[uncolored]=`تعهدات بانک بابت اعتبارات اس`, E280[uncolored]=`439498515`, F280[uncolored]=`425497756`, C281[uncolored]=`620594993`, D281[uncolored]=`تعهدات بانک بابت ضمانت نامه `, E281[uncolored]=`705682218`, F281[uncolored]=`620594993`, C282[uncolored]=`12748156`, D282[uncolored]=`سایر تعهدات بانک`, E282[uncolored]=`19498400`, F282[uncolored]=`12748156`, C283[uncolored]=`547`, D283[uncolored]=`وجوه اداره شده و موارد مشابه`, E283[uncolored]=`547`, F283[uncolored]=`547`)
- Rows between red name and region top: A278 (1 cells; first 1: A278[uncolored]=`کلیه مبالغ درج شده به میلیون`)
- Contiguous rows immediately below: A284:A285 (2 cells; first 2: A284[uncolored]=`توضیحات در خصوص تغییرات بااه`, A285[uncolored]=`«جملات آینده‌نگر نشان‌دهنده `)

Column-wise roles inside the rectangle (column index order):

| Column | Blue | Yellow | Gray | Black | Green | Uncolored | Absent |
|---|---|---|---|---|---|---|---|
| A | 1 | 4 | 0 | 0 | 0 | 0 | 0 |
| B | 1 | 0 | 4 | 0 | 0 | 0 | 0 |

### U01 — `Recovered_Sheet1` `A297:D299` — no red name

| Evidence | Observed |
|---|---|
| Worksheet | `Recovered_Sheet1` (rightToLeft = True) |
| Exact bounds | `A297:D299`; top-left A297, bottom-right D299; 3 rows × 4 columns = 12 cells |
| Basis for bounds | no border; extent from blue header + contiguous valued rows |
| Red main-name cell | none associated |
| Blue header cells (4) | A297:D297 |
| Yellow description cells (0) | — |
| Gray extraction cells (0): numeric 0, blank 0 | all: —; no blank gray |
| Black excluded cells (0) | — |
| Green sub-table markers (0) | none |
| Uncolored cells in rect (8) | with value: A298:D299; blank: — |
| Positions with no `<c>` in rect | 0 — — |
| Merged ranges intersecting | none intersect |
| Border evidence | No cell in this region has a non-ordinary border side; only ordinary `medium` `rgb:FFDDDDDD` borders (if any). |

**Cells outside the rectangle that appear related by position (listed, NOT included in the region):**

- Same rows, outside columns: none
- Rows between red name and region top: none
- Contiguous rows immediately below: A300:A341, B302:D308, E302, B310, B313:B332, C313:C333, D313:D332, E313:G313, E315:F332, B336:D340, E336 (181 cells; first 25: A300[Red]=`اطلاعات حق الوکاله و کفایت س`, A301[uncolored]=`کلیه مبالغ درج شده به میلیون`, A302[Blue]=`شرح`, B302[Black]=`سال مالی منتهی به۱۴۰۲/۱۲/۲۹`, C302[Blue]=`دوره ۶ ماهه منتهی به ۱۴۰۳/۰۶`, D302[Blue]=`برآورد تغییر روند در دوره ۶ `, E302[Blue], A303[Yellow]=`سهم بانک از درآمدهای مشاع`, B303[Black]=`0`, C303[Gray]=`0`, D303[uncolored]=`----------------------------`, A304[Yellow]=`سهم سپرده گذاران از درآمدهای`, B304[Black]=`194221502`, C304[Gray]=`112241232`, D304[uncolored]=`----------------------------`, A305[Yellow]=`نرخ حق الوکاله اعلام شده`, B305[Black]=`0`, C305[Gray]=`0`, D305[uncolored]=`----------------------------`, A306[Yellow]=`مبلغ حق الوکاله اعمال شده`, B306[Black]=`0`, C306[Gray]=`0`, D306[uncolored]=`----------------------------`, A307[Yellow]=`مابه التفاوت سود قابل پرداخت`, B307[Black]=`-69338916`)

Column-wise roles inside the rectangle (column index order):

| Column | Blue | Yellow | Gray | Black | Green | Uncolored | Absent |
|---|---|---|---|---|---|---|---|
| A | 1 | 0 | 0 | 0 | 0 | 2 | 0 |
| B | 1 | 0 | 0 | 0 | 0 | 2 | 0 |
| C | 1 | 0 | 0 | 0 | 0 | 2 | 0 |
| D | 1 | 0 | 0 | 0 | 0 | 2 | 0 |

### T09 — `Recovered_Sheet1` `A302:C308` — red name A300

| Evidence | Observed |
|---|---|
| Worksheet | `Recovered_Sheet1` (rightToLeft = True) |
| Exact bounds | `A302:C308`; top-left A302, bottom-right C308; 7 rows × 3 columns = 21 cells |
| Basis for bounds | border |
| Red main-name cell | A300 = `اطلاعات حق الوکاله و کفایت سرمایه` (raw fill `FFFF0000`); 2 row(s) above the region top |
| Blue header cells (2) | A302, C302 |
| Yellow description cells (6) | A303:A308 |
| Gray extraction cells (6): numeric 6, blank 0 | all: C303:C308; no blank gray |
| Black excluded cells (7) | B302:B308 |
| Green sub-table markers (0) | none |
| Uncolored cells in rect (0) | with value: —; blank: — |
| Positions with no `<c>` in rect | 0 — — |
| Merged ranges intersecting | none intersect |
| Border top (stored attribute top) | 3/3 medium indexed:64; continuous |
| Border bottom (stored attribute bottom) | 3/3 medium indexed:64; continuous |
| Border left (stored attribute left) | 7/7 medium indexed:64; continuous |
| Border right (stored attribute right) | 7/7 medium indexed:64; continuous |
| Distinguishable from ordinary cell borders? | Yes by colour test: every outer-edge side found is non-`FFDDDDDD` (medium indexed:64); ordinary interior sides are `medium` `rgb:FFDDDDDD` |
| Non-ordinary border sides on cells just OUTSIDE the rectangle | none |
| Non-ordinary border sides on interior (non-perimeter) positions | none |

**Cells outside the rectangle that appear related by position (listed, NOT included in the region):**

- Same rows, outside columns: D302:D308, E302 (8 cells; first 8: D302[Blue]=`برآورد تغییر روند در دوره ۶ `, E302[Blue], D303[uncolored]=`----------------------------`, D304[uncolored]=`----------------------------`, D305[uncolored]=`----------------------------`, D306[uncolored]=`----------------------------`, D307[uncolored]=`----------------------------`, D308[uncolored]=`----------------------------`)
- Rows between red name and region top: A301 (1 cells; first 1: A301[uncolored]=`کلیه مبالغ درج شده به میلیون`)
- Contiguous rows immediately below: A309:A341, B310, B313:B332, C313:C333, D313:D332, E313:G313, E315:F332, B336:D340, E336 (150 cells; first 25: A309[uncolored]=`اهداف و راهبردهای آتی مدیریت`, A310[uncolored]=`اهداف و راهبردهای آتی مدیریت`, B310[uncolored]=`----------------------------`, A311[Red]=`درآمد حاصل از تسهيلات اعطايي`, A312[uncolored]=`کلیه مبالغ درج شده به میلیون`, A313[Blue]=`شرح`, B313[Black]=`سال مالی منتهی به ۱۴۰۲/۱۲/۲۹`, C313[Black]=`متوسط نرخ سود سال مالی منتهی`, D313[Blue]=`دوره ۶ ماهه منتهی به ۱۴۰۳/۰۶`, E313[Blue]=`متوسط نرخ سود دوره ۶ ماهه من`, F313[Blue]=`برآورد تغییر روند در دوره ۶ `, G313[Blue], A314[Green]=`درآمد تسهیلات اعطایی:`, B314[Black], C314[Black], D314[uncolored], A315[Yellow]=`فروش اقساطی`, B315[Black]=`3892061`, C315[Black]=`0`, D315[Gray]=`2134924`, E315[uncolored]=`0`, F315[uncolored]=`مبلغ درآمدسرمایه گذاریهای با`, A316[Yellow]=`جعاله`, B316[Black]=`1753389`, C316[Black]=`0`)

Column-wise roles inside the rectangle (column index order):

| Column | Blue | Yellow | Gray | Black | Green | Uncolored | Absent |
|---|---|---|---|---|---|---|---|
| A | 1 | 6 | 0 | 0 | 0 | 0 | 0 |
| B | 0 | 0 | 0 | 7 | 0 | 0 | 0 |
| C | 1 | 0 | 6 | 0 | 0 | 0 | 0 |

### T10 — `Recovered_Sheet1` `A313:D332` — red name A311

| Evidence | Observed |
|---|---|
| Worksheet | `Recovered_Sheet1` (rightToLeft = True) |
| Exact bounds | `A313:D332`; top-left A313, bottom-right D332; 20 rows × 4 columns = 80 cells |
| Basis for bounds | border |
| Red main-name cell | A311 = `درآمد حاصل از تسهيلات اعطايي و سپرده گذاري` (raw fill `FFFF0000`); 2 row(s) above the region top |
| Blue header cells (2) | A313, D313 |
| Yellow description cells (18) | A315:A332 |
| Gray extraction cells (18): numeric 18, blank 0 | all: D315:D332; no blank gray |
| Black excluded cells (40) | B313:C332 |
| Green sub-table markers (1) | A314 `درآمد تسهیلات اعطایی: ` |
| Uncolored cells in rect (1) | with value: —; blank: D314 |
| Positions with no `<c>` in rect | 0 — — |
| Merged ranges intersecting | none intersect |
| Border top (stored attribute top) | 4/4 medium indexed:64; continuous |
| Border bottom (stored attribute bottom) | 4/4 medium indexed:64; continuous |
| Border left (stored attribute left) | 20/20 medium indexed:64; continuous |
| Border right (stored attribute right) | 20/20 medium indexed:64; continuous |
| Distinguishable from ordinary cell borders? | Yes by colour test: every outer-edge side found is non-`FFDDDDDD` (medium indexed:64); ordinary interior sides are `medium` `rgb:FFDDDDDD` |
| Non-ordinary border sides on cells just OUTSIDE the rectangle | none |
| Non-ordinary border sides on interior (non-perimeter) positions | none |

**Cells outside the rectangle that appear related by position (listed, NOT included in the region):**

- Same rows, outside columns: E313:G313, E315:F332 (39 cells; first 25: E313[Blue]=`متوسط نرخ سود دوره ۶ ماهه من`, F313[Blue]=`برآورد تغییر روند در دوره ۶ `, G313[Blue], E315[uncolored]=`0`, F315[uncolored]=`مبلغ درآمدسرمایه گذاریهای با`, E316[uncolored]=`0`, F316[uncolored]=`مبلغ درآمدسرمایه گذاریهای با`, E317[uncolored]=`0`, F317[uncolored]=`مبلغ درآمدسرمایه گذاریهای با`, E318[uncolored]=`0`, F318[uncolored]=`مبلغ درآمدسرمایه گذاریهای با`, E319[uncolored]=`0`, F319[uncolored]=`مبلغ درآمدسرمایه گذاریهای با`, E320[uncolored]=`0`, F320[uncolored]=`مبلغ درآمدسرمایه گذاریهای با`, E321[uncolored]=`0`, F321[uncolored]=`مبلغ درآمدسرمایه گذاریهای با`, E322[uncolored]=`0`, F322[uncolored]=`مبلغ درآمدسرمایه گذاریهای با`, E323[uncolored]=`0`, F323[uncolored]=`مبلغ درآمدسرمایه گذاریهای با`, E324[uncolored]=`0`, F324[uncolored]=`مبلغ درآمدسرمایه گذاریهای با`, E325[uncolored]=`0`, F325[uncolored]=`مبلغ درآمدسرمایه گذاریهای با`)
- Rows between red name and region top: A312 (1 cells; first 1: A312[uncolored]=`کلیه مبالغ درج شده به میلیون`)
- Contiguous rows immediately below: A333:A341, C333, B336:D340, E336 (26 cells; first 25: A333[uncolored]=`ارائه توضیحات در خصوص نحوه م`, C333[uncolored]=`----------------------------`, A334[Red]=`خالص سود (زیان) سرمایه گذاری`, A335[uncolored]=`کلیه مبالغ درج شده به میلیون`, A336[Blue]=`شرح`, B336[Black]=`سال مالی منتهی به۱۴۰۲/۱۲/۲۹`, C336[Blue]=`دوره ۶ ماهه منتهی به ۱۴۰۳/۰۶`, D336[Blue]=`برآورد تغییر روند در دوره ۶ `, E336[Blue], A337[Yellow]=`درآمد حاصل از سرمایه گذاری د`, B337[Black]=`2453194`, C337[Gray]=`402420`, D337[uncolored]=`مبلغ درآمدسرمایه گذاریهای با`, A338[Yellow]=`سود(زیان) حاصل از فروش سرمای`, B338[Black]=`0`, C338[Gray]=`0`, D338[uncolored]=`مبلغ درآمدسرمایه گذاریهای با`, A339[Yellow]=`سود (زیان) تعدیل ذخیره کاهش `, B339[Black]=`0`, C339[Gray]=`0`, D339[uncolored]=`مبلغ درآمدسرمایه گذاریهای با`, A340[uncolored]=`جمع درآمدهای حاصل از سرمایه `, B340[uncolored]=`2453194`, C340[uncolored]=`402420`, D340[uncolored]=`مبلغ درآمدسرمایه گذاریهای با`)

Column-wise roles inside the rectangle (column index order):

| Column | Blue | Yellow | Gray | Black | Green | Uncolored | Absent |
|---|---|---|---|---|---|---|---|
| A | 1 | 18 | 0 | 0 | 1 | 0 | 0 |
| B | 0 | 0 | 0 | 20 | 0 | 0 | 0 |
| C | 0 | 0 | 0 | 20 | 0 | 0 | 0 |
| D | 1 | 0 | 18 | 0 | 0 | 1 | 0 |

### T11 — `Recovered_Sheet1` `A336:C339` — red name A334

| Evidence | Observed |
|---|---|
| Worksheet | `Recovered_Sheet1` (rightToLeft = True) |
| Exact bounds | `A336:C339`; top-left A336, bottom-right C339; 4 rows × 3 columns = 12 cells |
| Basis for bounds | border |
| Red main-name cell | A334 = `خالص سود (زیان) سرمایه گذاری‌ ها` (raw fill `FFFF0000`); 2 row(s) above the region top |
| Blue header cells (2) | A336, C336 |
| Yellow description cells (3) | A337:A339 |
| Gray extraction cells (3): numeric 3, blank 0 | all: C337:C339; no blank gray |
| Black excluded cells (4) | B336:B339 |
| Green sub-table markers (0) | none |
| Uncolored cells in rect (0) | with value: —; blank: — |
| Positions with no `<c>` in rect | 0 — — |
| Merged ranges intersecting | none intersect |
| Border top (stored attribute top) | 3/3 medium indexed:64; continuous |
| Border bottom (stored attribute bottom) | 3/3 medium indexed:64; continuous |
| Border left (stored attribute left) | 4/4 medium indexed:64; continuous |
| Border right (stored attribute right) | 4/4 medium indexed:64; continuous |
| Distinguishable from ordinary cell borders? | Yes by colour test: every outer-edge side found is non-`FFDDDDDD` (medium indexed:64); ordinary interior sides are `medium` `rgb:FFDDDDDD` |
| Non-ordinary border sides on cells just OUTSIDE the rectangle | none |
| Non-ordinary border sides on interior (non-perimeter) positions | none |

**Cells outside the rectangle that appear related by position (listed, NOT included in the region):**

- Same rows, outside columns: D336:D339, E336 (5 cells; first 5: D336[Blue]=`برآورد تغییر روند در دوره ۶ `, E336[Blue], D337[uncolored]=`مبلغ درآمدسرمایه گذاریهای با`, D338[uncolored]=`مبلغ درآمدسرمایه گذاریهای با`, D339[uncolored]=`مبلغ درآمدسرمایه گذاریهای با`)
- Rows between red name and region top: A335 (1 cells; first 1: A335[uncolored]=`کلیه مبالغ درج شده به میلیون`)
- Contiguous rows immediately below: A340:A341, B340:D340 (5 cells; first 5: A340[uncolored]=`جمع درآمدهای حاصل از سرمایه `, B340[uncolored]=`2453194`, C340[uncolored]=`402420`, D340[uncolored]=`مبلغ درآمدسرمایه گذاریهای با`, A341[uncolored]=`«جملات آینده‌نگر نشان‌دهنده `)

Column-wise roles inside the rectangle (column index order):

| Column | Blue | Yellow | Gray | Black | Green | Uncolored | Absent |
|---|---|---|---|---|---|---|---|
| A | 1 | 3 | 0 | 0 | 0 | 0 | 0 |
| B | 0 | 0 | 0 | 4 | 0 | 0 | 0 |
| C | 1 | 0 | 3 | 0 | 0 | 0 | 0 |

### T12 — `Recovered_Sheet1` `A353:I358` — red name A351

| Evidence | Observed |
|---|---|
| Worksheet | `Recovered_Sheet1` (rightToLeft = True) |
| Exact bounds | `A353:I358`; top-left A353, bottom-right I358; 6 rows × 9 columns = 54 cells |
| Basis for bounds | border |
| Red main-name cell | A351 = `وضعیت شرکتهای سرمایه پذیر:` (raw fill `FFFF0000`); 2 row(s) above the region top |
| Blue header cells (10) | A353:B354, G353:I354 |
| Yellow description cells (8) | A355:B358 |
| Gray extraction cells (12): numeric 12, blank 0 | all: G355:I358; no blank gray |
| Black excluded cells (24) | C353:F358 |
| Green sub-table markers (0) | none |
| Uncolored cells in rect (0) | with value: —; blank: — |
| Positions with no `<c>` in rect | 0 — — |
| Merged ranges intersecting | `A353:B354` (inside); `C353:F353` (inside); `G353:I353` (inside); `A355:B355` (inside); `A356:B356` (inside); `A357:B357` (inside); `A358:B358` (inside) |
| Border top (stored attribute top) | 9/9 medium indexed:64; continuous |
| Border bottom (stored attribute bottom) | 9/9 medium indexed:64; continuous |
| Border left (stored attribute left) | 6/6 medium indexed:64; continuous |
| Border right (stored attribute right) | 6/6 medium indexed:64; continuous |
| Distinguishable from ordinary cell borders? | Yes by colour test: every outer-edge side found is non-`FFDDDDDD` (medium indexed:64); ordinary interior sides are `medium` `rgb:FFDDDDDD` |
| Non-ordinary border sides on cells just OUTSIDE the rectangle | none |
| Non-ordinary border sides on interior (non-perimeter) positions | none |

**Cells outside the rectangle that appear related by position (listed, NOT included in the region):**

- Same rows, outside columns: J353:J358, K353:K354 (8 cells; first 8: J353[Blue]=`تشريح آخرين وضعيت و برنامه ه`, K353[Blue], J354[Blue], K354[Blue], J355[uncolored]=`سود نقدی سرمایه گذاری ها تا `, J356[uncolored]=`سود نقدی سرمایه گذاری ها تا `, J357[uncolored]=`سود نقدی سرمایه گذاری ها تا `, J358[uncolored]=`سود نقدی سرمایه گذاری ها تا `)
- Rows between red name and region top: A352 (1 cells; first 1: A352[uncolored]=`کلیه مبالغ درج شده به میلیون`)
- Contiguous rows immediately below: A359:A367, B361:C367 (23 cells; first 23: A359[Red]=`ساير درآمدها و هزینه های عمل`, A360[uncolored]=`کلیه مبالغ درج شده به میلیون`, A361[Blue]=`شرح`, B361[Black]=`۱۴۰۲/۱۲/۲۹`, C361[Blue]=`۱۴۰۳/۰۶/۳۱`, A362[Green]=`ساير درآمدهاي عملياتي:`, B362[Black], C362[uncolored], A363[Yellow]=`ساير درآمدهاي عملياتي`, B363[Black]=`151543669`, C363[Gray]=`84513662`, A364[uncolored], B364[Black], C364[uncolored], A365[Yellow]=`جمع ساير درآمدهاي عملياتي`, B365[Black]=`151543669`, C365[Gray]=`84513662`, A366[Green]=`ساير هزينه هاي عملياتي:`, B366[Black], C366[uncolored], A367[Yellow]=`ساير هزينه هاي عملياتي`, B367[Black]=`0`, C367[Gray]=`0`)

Column-wise roles inside the rectangle (column index order):

| Column | Blue | Yellow | Gray | Black | Green | Uncolored | Absent |
|---|---|---|---|---|---|---|---|
| A | 2 | 4 | 0 | 0 | 0 | 0 | 0 |
| B | 2 | 4 | 0 | 0 | 0 | 0 | 0 |
| C | 0 | 0 | 0 | 6 | 0 | 0 | 0 |
| D | 0 | 0 | 0 | 6 | 0 | 0 | 0 |
| E | 0 | 0 | 0 | 6 | 0 | 0 | 0 |
| F | 0 | 0 | 0 | 6 | 0 | 0 | 0 |
| G | 2 | 0 | 4 | 0 | 0 | 0 | 0 |
| H | 2 | 0 | 4 | 0 | 0 | 0 | 0 |
| I | 2 | 0 | 4 | 0 | 0 | 0 | 0 |

### T13 — `Recovered_Sheet1` `A361:C367` — red name A359

| Evidence | Observed |
|---|---|
| Worksheet | `Recovered_Sheet1` (rightToLeft = True) |
| Exact bounds | `A361:C367`; top-left A361, bottom-right C367; 7 rows × 3 columns = 21 cells |
| Basis for bounds | border |
| Red main-name cell | A359 = `ساير درآمدها و هزینه های عملياتي:` (raw fill `FFFF0000`); 2 row(s) above the region top |
| Blue header cells (2) | A361, C361 |
| Yellow description cells (3) | A363, A365, A367 |
| Gray extraction cells (3): numeric 3, blank 0 | all: C363, C365, C367; no blank gray |
| Black excluded cells (7) | B361:B367 |
| Green sub-table markers (2) | A362 `ساير درآمدهاي عملياتي: `, A366 `ساير هزينه هاي عملياتي: ` |
| Uncolored cells in rect (4) | with value: —; blank: C362, A364, C364, C366 |
| Positions with no `<c>` in rect | 0 — — |
| Merged ranges intersecting | none intersect |
| Border top (stored attribute top) | 3/3 medium indexed:64; continuous |
| Border bottom (stored attribute bottom) | 3/3 medium indexed:64; continuous |
| Border left (stored attribute left) | 7/7 medium indexed:64; continuous |
| Border right (stored attribute right) | 7/7 medium indexed:64; continuous |
| Distinguishable from ordinary cell borders? | Yes by colour test: every outer-edge side found is non-`FFDDDDDD` (medium indexed:64); ordinary interior sides are `medium` `rgb:FFDDDDDD` |
| Non-ordinary border sides on cells just OUTSIDE the rectangle | none |
| Non-ordinary border sides on interior (non-perimeter) positions | none |

**Cells outside the rectangle that appear related by position (listed, NOT included in the region):**

- Same rows, outside columns: none
- Rows between red name and region top: A360 (1 cells; first 1: A360[uncolored]=`کلیه مبالغ درج شده به میلیون`)
- Contiguous rows immediately below: none

Column-wise roles inside the rectangle (column index order):

| Column | Blue | Yellow | Gray | Black | Green | Uncolored | Absent |
|---|---|---|---|---|---|---|---|
| A | 1 | 3 | 0 | 0 | 2 | 1 | 0 |
| B | 0 | 0 | 0 | 7 | 0 | 0 | 0 |
| C | 1 | 0 | 3 | 0 | 0 | 3 | 0 |

### T14 — `Recovered_Sheet1` `A376:C378` — red name A374

| Evidence | Observed |
|---|---|
| Worksheet | `Recovered_Sheet1` (rightToLeft = True) |
| Exact bounds | `A376:C378`; top-left A376, bottom-right C378; 3 rows × 3 columns = 9 cells |
| Basis for bounds | border |
| Red main-name cell | A374 = `خالص ساير درآمدها و هزینه ها:` (raw fill `FFFF0000`); 2 row(s) above the region top |
| Blue header cells (2) | A376, C376 |
| Yellow description cells (2) | A377:A378 |
| Gray extraction cells (2): numeric 2, blank 0 | all: C377:C378; no blank gray |
| Black excluded cells (3) | B376:B378 |
| Green sub-table markers (0) | none |
| Uncolored cells in rect (0) | with value: —; blank: — |
| Positions with no `<c>` in rect | 0 — — |
| Merged ranges intersecting | none intersect |
| Border top (stored attribute top) | 3/3 medium indexed:64; continuous |
| Border bottom (stored attribute bottom) | 3/3 medium indexed:64; continuous |
| Border left (stored attribute left) | 3/3 medium indexed:64; continuous |
| Border right (stored attribute right) | 3/3 medium indexed:64; continuous |
| Distinguishable from ordinary cell borders? | Yes by colour test: every outer-edge side found is non-`FFDDDDDD` (medium indexed:64); ordinary interior sides are `medium` `rgb:FFDDDDDD` |
| Non-ordinary border sides on cells just OUTSIDE the rectangle | none |
| Non-ordinary border sides on interior (non-perimeter) positions | none |

**Cells outside the rectangle that appear related by position (listed, NOT included in the region):**

- Same rows, outside columns: none
- Rows between red name and region top: A375 (1 cells; first 1: A375[uncolored]=`کلیه مبالغ درج شده به میلیون`)
- Contiguous rows immediately below: none

Column-wise roles inside the rectangle (column index order):

| Column | Blue | Yellow | Gray | Black | Green | Uncolored | Absent |
|---|---|---|---|---|---|---|---|
| A | 1 | 2 | 0 | 0 | 0 | 0 | 0 |
| B | 0 | 0 | 0 | 3 | 0 | 0 | 0 |
| C | 1 | 0 | 2 | 0 | 0 | 0 | 0 |

### T15 — `Recovered_Sheet1` `A386:C387` — red name A384

| Evidence | Observed |
|---|---|
| Worksheet | `Recovered_Sheet1` (rightToLeft = True) |
| Exact bounds | `A386:C387`; top-left A386, bottom-right C387; 2 rows × 3 columns = 6 cells |
| Basis for bounds | border |
| Red main-name cell | A384 = `هزینه های اداری و عمومی:` (raw fill `FFFF0000`); 2 row(s) above the region top |
| Blue header cells (2) | A386, C386 |
| Yellow description cells (1) | A387 |
| Gray extraction cells (1): numeric 1, blank 0 | all: C387; no blank gray |
| Black excluded cells (2) | B386:B387 |
| Green sub-table markers (0) | none |
| Uncolored cells in rect (0) | with value: —; blank: — |
| Positions with no `<c>` in rect | 0 — — |
| Merged ranges intersecting | none intersect |
| Border top (stored attribute top) | 3/3 medium indexed:64; continuous |
| Border bottom (stored attribute bottom) | 3/3 medium indexed:64; continuous |
| Border left (stored attribute left) | 2/2 medium indexed:64; continuous |
| Border right (stored attribute right) | 2/2 medium indexed:64; continuous |
| Distinguishable from ordinary cell borders? | Yes by colour test: every outer-edge side found is non-`FFDDDDDD` (medium indexed:64); ordinary interior sides are `medium` `rgb:FFDDDDDD` |
| Non-ordinary border sides on cells just OUTSIDE the rectangle | none |
| Non-ordinary border sides on interior (non-perimeter) positions | none |

**Cells outside the rectangle that appear related by position (listed, NOT included in the region):**

- Same rows, outside columns: none
- Rows between red name and region top: A385 (1 cells; first 1: A385[uncolored]=`کلیه مبالغ درج شده به میلیون`)
- Contiguous rows immediately below: none

Column-wise roles inside the rectangle (column index order):

| Column | Blue | Yellow | Gray | Black | Green | Uncolored | Absent |
|---|---|---|---|---|---|---|---|
| A | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| B | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| C | 1 | 0 | 1 | 0 | 0 | 0 | 0 |

### T16 — `Recovered_Sheet1` `A395:C398` — red name A393

| Evidence | Observed |
|---|---|
| Worksheet | `Recovered_Sheet1` (rightToLeft = True) |
| Exact bounds | `A395:C398`; top-left A395, bottom-right C398; 4 rows × 3 columns = 12 cells |
| Basis for bounds | border |
| Red main-name cell | A393 = `هزینه مالی:` (raw fill `FFFF0000`); 2 row(s) above the region top |
| Blue header cells (2) | A395, C395 |
| Yellow description cells (3) | A396:A398 |
| Gray extraction cells (3): numeric 3, blank 0 | all: C396:C398; no blank gray |
| Black excluded cells (4) | B395:B398 |
| Green sub-table markers (0) | none |
| Uncolored cells in rect (0) | with value: —; blank: — |
| Positions with no `<c>` in rect | 0 — — |
| Merged ranges intersecting | none intersect |
| Border top (stored attribute top) | 3/3 thin indexed:64; continuous |
| Border bottom (stored attribute bottom) | 3/3 thin indexed:64; continuous |
| Border left (stored attribute left) | 4/4 thin indexed:64; continuous |
| Border right (stored attribute right) | 4/4 thin indexed:64; continuous |
| Distinguishable from ordinary cell borders? | Yes by colour test: every outer-edge side found is non-`FFDDDDDD` (thin indexed:64); ordinary interior sides are `medium` `rgb:FFDDDDDD` |
| Non-ordinary border sides on cells just OUTSIDE the rectangle | none |
| Non-ordinary border sides on interior (non-perimeter) positions | none |

**Cells outside the rectangle that appear related by position (listed, NOT included in the region):**

- Same rows, outside columns: none
- Rows between red name and region top: A394 (1 cells; first 1: A394[uncolored]=`کلیه مبالغ درج شده به میلیون`)
- Contiguous rows immediately below: A399:A401, B399:C399, C401 (6 cells; first 6: A399[uncolored]=`جمع هزينه‌هاي مالي`, B399[uncolored]=`-20082491`, C399[uncolored]=`-5804157`, A400[uncolored]=`برآورد شرکت از تغییرات هزینه`, A401[uncolored]=`دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲`, C401[uncolored]=`----------------------------`)

Column-wise roles inside the rectangle (column index order):

| Column | Blue | Yellow | Gray | Black | Green | Uncolored | Absent |
|---|---|---|---|---|---|---|---|
| A | 1 | 3 | 0 | 0 | 0 | 0 | 0 |
| B | 0 | 0 | 0 | 4 | 0 | 0 | 0 |
| C | 1 | 0 | 3 | 0 | 0 | 0 | 0 |

### T17 — `Recovered_Sheet1` `A404:E405` — red name A403

| Evidence | Observed |
|---|---|
| Worksheet | `Recovered_Sheet1` (rightToLeft = True) |
| Exact bounds | `A404:E405`; top-left A404, bottom-right E405; 2 rows × 5 columns = 10 cells |
| Basis for bounds | border |
| Red main-name cell | A403 = `برنامه شرکت در خصوص تقسیم سود` (raw fill `FFFF0000`); 1 row(s) above the region top |
| Blue header cells (5) | A404:E404 |
| Yellow description cells (0) | — |
| Gray extraction cells (5): numeric 5, blank 0 | all: A405:E405; no blank gray |
| Black excluded cells (0) | — |
| Green sub-table markers (0) | none |
| Uncolored cells in rect (0) | with value: —; blank: — |
| Positions with no `<c>` in rect | 0 — — |
| Merged ranges intersecting | none intersect |
| Border top (stored attribute top) | 5/5 thin indexed:64; continuous |
| Border bottom (stored attribute bottom) | 5/5 thin indexed:64; continuous |
| Border left (stored attribute left) | 2/2 thin indexed:64; continuous |
| Border right (stored attribute right) | 2/2 thin indexed:64; continuous |
| Distinguishable from ordinary cell borders? | Yes by colour test: every outer-edge side found is non-`FFDDDDDD` (thin indexed:64); ordinary interior sides are `medium` `rgb:FFDDDDDD` |
| Non-ordinary border sides on cells just OUTSIDE the rectangle | none |
| Non-ordinary border sides on interior (non-perimeter) positions | none |

**Cells outside the rectangle that appear related by position (listed, NOT included in the region):**

- Same rows, outside columns: none
- Rows between red name and region top: none
- Contiguous rows immediately below: A406:A407, B407 (3 cells; first 3: A406[uncolored]=`سایر برنامه های با اهمیت شرک`, A407[uncolored]=`دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲`, B407[uncolored]=`----------------------------`)

Column-wise roles inside the rectangle (column index order):

| Column | Blue | Yellow | Gray | Black | Green | Uncolored | Absent |
|---|---|---|---|---|---|---|---|
| A | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| B | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| C | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| D | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| E | 1 | 0 | 1 | 0 | 0 | 0 | 0 |

### S01 — `Sheet1` `A16:E24` — red name A14

| Evidence | Observed |
|---|---|
| Worksheet | `Sheet1` (rightToLeft = False) |
| Exact bounds | `A16:E24`; top-left A16, bottom-right E24; 9 rows × 5 columns = 45 cells |
| Basis for bounds | no border; extent from blue header + contiguous valued rows |
| Red main-name cell | A14 = `صورت سود و زیان جامع` (raw fill `FFFF0000`); 2 row(s) above the region top |
| Blue header cells (10) | A16:E17 |
| Yellow description cells (0) | — |
| Gray extraction cells (0): numeric 0, blank 0 | all: —; no blank gray |
| Black excluded cells (0) | — |
| Green sub-table markers (1) | A19 `سایر اقلام سود و زیان جامع: ` |
| Uncolored cells in rect (34) | with value: A18:E18, A20:D24, E24; blank: B19:D19, E19:E23 |
| Positions with no `<c>` in rect | 0 — — |
| Merged ranges intersecting | `A16:A17` (inside); `E16:E17` (inside) |
| Border evidence | No cell in this region has a non-ordinary border side; only ordinary `medium` `rgb:FFDDDDDD` borders (if any). |

**Cells outside the rectangle that appear related by position (listed, NOT included in the region):**

- Same rows, outside columns: none
- Rows between red name and region top: A15 (1 cells; first 1: A15[uncolored]=`کلیه مبالغ درج شده به میلیون`)
- Contiguous rows immediately below: none

Column-wise roles inside the rectangle (column index order):

| Column | Blue | Yellow | Gray | Black | Green | Uncolored | Absent |
|---|---|---|---|---|---|---|---|
| A | 2 | 0 | 0 | 0 | 1 | 6 | 0 |
| B | 2 | 0 | 0 | 0 | 0 | 7 | 0 |
| C | 2 | 0 | 0 | 0 | 0 | 7 | 0 |
| D | 2 | 0 | 0 | 0 | 0 | 7 | 0 |
| E | 2 | 0 | 0 | 0 | 0 | 7 | 0 |

## 8. Green sub-table marker inventory and provisional partitions

Rule applied (owner rule 4): in the reading order, the yellow description column immediately following a green marker begins that sub-table's label region and continues until the next green marker or the end of the parent candidate. Only the **same column** as the green marker was followed for yellow labels (all markers are in column A, the yellow column). A partition is stated as **clear** only if every row between the marker and the next marker/end has a yellow cell in that column; otherwise it is **ambiguous** and the non-yellow cells are listed. No missing annotation was invented.

| Sheet | Green cell | Value | Parent candidate (objective: marker inside rect) | Label-column span after marker (to next marker/end) | First / last yellow | # yellow | Next green | Boundary | Provisional range / notes |
|---|---|---|---|---|---|---|---|---|---|
| Recovered_Sheet1 | A12 | `عملیات در حال تداوم: ` | T01 | A13:A31 | A13 / A31 | 19 | A32 | clear | span rows 13–31; gray in span: 38 (B13:B31, D13:D31) |
| Recovered_Sheet1 | A32 | `عملیات متوقف شده: ` | T01 | A33:A34 | A33 / A34 | 2 | A35 | clear | span rows 33–34; gray in span: 4 (B33:B34, D33:D34) |
| Recovered_Sheet1 | A35 | `سود (زیان)پایه هر سهم (ريال) ` | T01 | A36:A42 | A36 / A42 | 7 | none (parent end) | clear | span rows 36–42; gray in span: 14 (B36:B42, D36:D42) |
| Recovered_Sheet1 | A63 | `سایر اقلام سود و زیان جامع: ` | T02 | A64:A68 | A64 / A68 | 5 | none (parent end) | clear | span rows 64–68; gray in span: 10 (B64:B68, D64:D68) |
| Recovered_Sheet1 | A81 | `دارایی ها ` | T03 | A82:A95 | A82 / A94 | 13 | A96 | AMBIGUOUS | span rows 82–95; gray in span: 26 (B82:C94); non-yellow cells in marker column inside span: A95[Blue] |
| Recovered_Sheet1 | A96 | `حقوق مالکانه ` | T03 | A97:A107 | A97 / A107 | 11 | A108 | clear | span rows 97–107; gray in span: 22 (B97:C107) |
| Recovered_Sheet1 | A108 | `بدهی‌ها ` | T03 | A109:A119 | A109 / A119 | 11 | none (parent end) | clear | span rows 109–119; gray in span: 22 (B109:C119) |
| Recovered_Sheet1 | A152 | `تغییرات حقوق مالکانه در سال ۱۴۰۳/۰۶/۳۱ ` | T04 | A153:A165 | A153 / A165 | 13 | none (parent end) | clear | span rows 153–165; gray in span: 143 (B153:L165) |
| Recovered_Sheet1 | A178 | `جریان­های نقدی حاصل از فعاليت‌هاي عملياتي: ` | T05 | A179:A181 | A179 / A181 | 3 | A182 | clear | span rows 179–181; gray in span: 6 (B179:B181, D179:D181) |
| Recovered_Sheet1 | A182 | `فعاليت‌هاي سرمایه‌گذاری ` | T05 | A183:A190 | A183 / A190 | 8 | A191 | clear | span rows 183–190; gray in span: 16 (B183:B190, D183:D190) |
| Recovered_Sheet1 | A191 | `فعاليت‌هاي تأمين مالي ` | T05 | A192:A213 | A192 / A213 | 22 | none (parent end) | clear | span rows 192–213; gray in span: 44 (B192:B213, D192:D213) |
| Recovered_Sheet1 | A268 | `سپرده های ریالی: ` | T07 | A269:A275 | A269 / A275 | 7 | none (parent end) | clear | span rows 269–275; gray in span: 7 (C269:C275) |
| Recovered_Sheet1 | A314 | `درآمد تسهیلات اعطایی: ` | T10 | A315:A332 | A315 / A332 | 18 | none (parent end) | clear | span rows 315–332; gray in span: 18 (D315:D332) |
| Recovered_Sheet1 | A362 | `ساير درآمدهاي عملياتي: ` | T13 | A363:A365 | A363 / A365 | 2 | A366 | AMBIGUOUS | span rows 363–365; gray in span: 2 (C363, C365); non-yellow cells in marker column inside span: A364[uncolored] |
| Recovered_Sheet1 | A366 | `ساير هزينه هاي عملياتي: ` | T13 | A367:A367 | A367 / A367 | 1 | none (parent end) | clear | span rows 367–367; gray in span: 1 (C367) |
| Sheet1 | A19 | `سایر اقلام سود و زیان جامع: ` | S01 | A20:A24 | no yellow cell | 0 | none (parent end) | AMBIGUOUS | span rows 20–24; gray in span: 0 (—); non-yellow cells in marker column inside span: A20[uncolored], A21[uncolored], A22[uncolored], A23[uncolored], A24[uncolored] |

Yellow rows that precede the first green marker of their candidate (belong to no marker by rule 4):

| Candidate | First marker | Yellow cells before first marker (if no marker: all yellow cells of the candidate) |
|---|---|---|
| T01 | first green at A12 | none |
| T02 | first green at A63 | A62 |
| T03 | first green at A81 | none |
| T04 | first green at A152 | none |
| T05 | first green at A178 | none |
| T06 | no green marker in this candidate | A240:A242, A245:A253 |
| T07 | first green at A268 | none |
| T08 | no green marker in this candidate | A280:A283 |
| T09 | no green marker in this candidate | A303:A308 |
| T10 | first green at A314 | none |
| T11 | no green marker in this candidate | A337:A339 |
| T12 | no green marker in this candidate | A355:B358 |
| T13 | first green at A362 | none |
| T14 | no green marker in this candidate | A377:A378 |
| T15 | no green marker in this candidate | A387 |
| T16 | no green marker in this candidate | A396:A398 |
| T17 | no green marker in this candidate | no yellow |

Provisional sub-table ranges (rows × table columns), stated only where yellow cells are contiguous and annotation geometry supports it:

| Candidate | Marker | Provisional range (full table width) | Label region |
|---|---|---|---|
| T01 | A12 | `A13:D31` | yellow A13:A31 |
| T01 | A32 | `A33:D34` | yellow A33:A34 |
| T01 | A35 | `A36:D42` | yellow A36:A42 |
| T02 | A63 | `A64:D68` | yellow A64:A68 |
| T03 | A96 | `A97:C107` | yellow A97:A107 |
| T03 | A108 | `A109:C119` | yellow A109:A119 |
| T04 | A152 | `A153:L165` | yellow A153:A165 |
| T05 | A178 | `A179:D181` | yellow A179:A181 |
| T05 | A182 | `A183:D190` | yellow A183:A190 |
| T05 | A191 | `A192:D213` | yellow A192:A213 |
| T07 | A268 | `A269:C275` | yellow A269:A275 |
| T10 | A314 | `A315:D332` | yellow A315:A332 |
| T13 | A366 | `A367:C367` | yellow A367 |

Sub-tables **not** given a provisional range (ambiguous or no yellow): see the AMBIGUOUS rows above and the anomaly register (§12).

## 9. Reading direction and column order

- `Recovered_Sheet1`: `rightToLeft` = **True**. `Sheet1`: `rightToLeft` = **False** (attribute absent).
- Column index order is reported below as stored (A = column index 1). In a worksheet with `rightToLeft=1`, Excel displays column A at the **right-most** position and higher columns progressively to the left; this is a property of the file format, but it was **not verified by rendering**, and `rightToLeft=True` is **not** taken as proof of the logical reading order.
- For each candidate the physical position is expressed through column indexes of the yellow and gray cells and the stored border sides.

| ID | Sheet direction | Column index order in rect | Yellow cols | Gray cols | Black cols | Blue cols | Green cols | Observed relation | Merged ranges affecting reading order |
|---|---|---|---|---|---|---|---|---|---|
| T01 | RTL=True | A, B, C, D | A | B, D | C | A, B, D | A | yellow column index < gray column indexes | inside: A10:A11 |
| T02 | RTL=True | A, B, C, D | A | B, D | C | A, B, D | A | yellow column index < gray column indexes | inside: A60:A61 |
| T03 | RTL=True | A, B, C | A | B, C | — | A, B, C | A | yellow column index < gray column indexes | inside: A79:A80 |
| T04 | RTL=True | A, B, C, D, E, F, G, H, I, J, K, L | A | B, C, D, E, F, G, H, I, J, K, L | A, B, C, D, E, F, G, H, I, J, K, L | A, B, C, D, E, F, G, H, I, J, K, L | A | yellow column index < gray column indexes | inside: none |
| T05 | RTL=True | A, B, C, D | A | B, D | C | A, B, D | A | yellow column index < gray column indexes | inside: A176:A177 |
| T06 | RTL=True | A, B, C, D, E, F, G, H, I | A | C, E, G, I | B, D, F, H | A, B, C, D, E, F, G, H, I | — | yellow column index < gray column indexes | inside: A238:A239, B239:C239, D239:E239, F239:G239, H239:I239 |
| T07 | RTL=True | A, B, C | A | C | B | A, B, C | A | yellow column index < gray column indexes | inside: A266:A267, B266:C266 |
| T08 | RTL=True | A, B | A | B | — | A, B | — | yellow column index < gray column indexes | inside: none |
| U01 | RTL=True | A, B, C, D | — | — | — | A, B, C, D | — | — | inside: none |
| T09 | RTL=True | A, B, C | A | C | B | A, C | — | yellow column index < gray column indexes | inside: none |
| T10 | RTL=True | A, B, C, D | A | D | B, C | A, D | A | yellow column index < gray column indexes | inside: none |
| T11 | RTL=True | A, B, C | A | C | B | A, C | — | yellow column index < gray column indexes | inside: none |
| T12 | RTL=True | A, B, C, D, E, F, G, H, I | A, B | G, H, I | C, D, E, F | A, B, G, H, I | — | yellow column index < gray column indexes | inside: A353:B354, C353:F353, G353:I353, A355:B355, A356:B356, A357:B357, A358:B358 |
| T13 | RTL=True | A, B, C | A | C | B | A, C | A | yellow column index < gray column indexes | inside: none |
| T14 | RTL=True | A, B, C | A | C | B | A, C | — | yellow column index < gray column indexes | inside: none |
| T15 | RTL=True | A, B, C | A | C | B | A, C | — | yellow column index < gray column indexes | inside: none |
| T16 | RTL=True | A, B, C | A | C | B | A, C | — | yellow column index < gray column indexes | inside: none |
| T17 | RTL=True | A, B, C, D, E | — | A, B, C, D, E | — | A, B, C, D, E | — | — | inside: none |
| S01 | RTL=False | A, B, C, D, E | — | — | — | A, B, C, D, E | A | — | inside: A16:A17, E16:E17 |

Observed: 16 of 17 bordered candidates contain yellow cells; in 16 of them (T01, T02, T03, T04, T05, T06, T07, T08, T09, T10, T11, T12, T13, T14, T15, T16) the yellow cells start in the lowest-index column of the rectangle (column A), and gray cells occupy higher-index columns. Candidates in which yellow spans more than one column index: T12 (columns A, B). Bordered candidates without yellow: T17. On the right-to-left main sheet, column A is displayed right-most (format property, not visually verified), so the yellow column would be the right-most column of each table and gray columns lie to its left. `Sheet1` (left-to-right) has no yellow and no gray cells.

## 10. Independent secondary worksheet analysis (`Sheet1`)

This worksheet was inspected on its own, from its own XML part (`xl/worksheets/sheet2.xml`), without relying on any earlier claim about its name, range, title, colours or contents. No statement below infers that it is, or is not, a duplicate of the other worksheet.

### 10.1 Required verifications

| Check | Result |
|---|---|
| Worksheet name / range / direction | `Sheet1`, used range `A1:E24`, `rightToLeft` = False (attribute absent) |
| Red main-table name exists? | **Yes** — A14 = `صورت سود و زیان جامع`; raw fill solid rgb `FFFF0000`, tint 0, bgColor indexed 64. Only one red cell on this worksheet. |
| Blue header cells exist? | **Yes** — 10 cells: A16:E17; raw fill solid rgb `FF0197C8`. Values: A16=`شرح`, B16=`دوره منتهي به ۱۴۰۳/۰۶/۳۱`, C16=`تجدید ارائه شده ۱۴۰۲/۰۶/۳۱`, D16=`تجدید ارائه شده ۱۴۰۲/۱۲/۲۹`, E16=`درصد تغییر`, B17=`حسابرسی نشده`, C17=`حسابرسی شده`, D17=`حسابرسی شده`. Blank blue cells: A17, E17 (A17 and E17 are non-anchor cells of merged ranges A16:A17 and E16:E17). |
| Yellow description cells exist? | **No** — 0 yellow cells. |
| Gray extraction cells exist? | **No** — 0 gray cells. |
| Any gray extraction cell blank? | **No** — there are no gray cells at all, hence no blank gray cell. |
| Green sub-table markers exist? | **Yes** — 1: A19 = `سایر اقلام سود و زیان جامع: `; raw fill solid rgb `FF00B050`. |
| Black excluded cells/columns exist? | **No** — 0 black cells. |
| Recognizable (non-ordinary) border exists? | **No** — every stored border side on this worksheet is `medium` `rgb:FFDDDDDD` (the ordinary border); 0 non-`FFDDDDDD` sides. Cells carrying ordinary sides: A1:A12, A16:E24. |

### 10.2 Complete cell dump of the worksheet (all 59 stored `<c>` elements)

| Coordinate | Value (verbatim) | Excel type | Role (raw fill) | Blank? |
|---|---|---|---|---|
| A1 | `عملیات در حال تداوم: ` | s (string) | uncolored | no |
| A2 | `عملیات متوقف شده: ` | s (string) | uncolored | no |
| A3 | `سود (زیان)پایه هر سهم (ريال) ` | s (string) | uncolored | no |
| A4 | `سایر اقلام سود و زیان جامع: ` | s (string) | uncolored | no |
| A5 | `دارایی ها ` | s (string) | uncolored | no |
| A6 | `حقوق مالکانه ` | s (string) | uncolored | no |
| A7 | `بدهی‌ها ` | s (string) | uncolored | no |
| A8 | `جریان­های نقدی حاصل از فعاليت‌هاي عملياتي: ` | s (string) | uncolored | no |
| A9 | `فعاليت‌هاي سرمایه‌گذاری ` | s (string) | uncolored | no |
| A10 | `فعاليت‌هاي تأمين مالي ` | s (string) | uncolored | no |
| A11 | `سپرده های ریالی: ` | s (string) | uncolored | no |
| A12 | `درآمد تسهیلات اعطایی: ` | s (string) | uncolored | no |
| A14 | `صورت سود و زیان جامع` | s (string) | Red | no |
| A15 | `کلیه مبالغ درج شده به میلیون ریال می باشد` | s (string) | uncolored | no |
| A16 | `شرح` | s (string) | Blue | no |
| B16 | `دوره منتهي به ۱۴۰۳/۰۶/۳۱` | s (string) | Blue | no |
| C16 | `تجدید ارائه شده ۱۴۰۲/۰۶/۳۱` | s (string) | Blue | no |
| D16 | `تجدید ارائه شده ۱۴۰۲/۱۲/۲۹` | s (string) | Blue | no |
| E16 | `درصد تغییر` | s (string) | Blue | no |
| A17 |  | blank (no value stored) | Blue | yes |
| B17 | `حسابرسی نشده` | s (string) | Blue | no |
| C17 | `حسابرسی شده` | s (string) | Blue | no |
| D17 | `حسابرسی شده` | s (string) | Blue | no |
| E17 |  | blank (no value stored) | Blue | yes |
| A18 | `سود(زیان) خالص ` | s (string) | uncolored | no |
| B18 | `-25195703` | n (number) | uncolored | no |
| C18 | `-35246257` | n (number) | uncolored | no |
| D18 | `-9124895` | n (number) | uncolored | no |
| E18 | `29` | n (number) | uncolored | no |
| A19 | `سایر اقلام سود و زیان جامع: ` | s (string) | Green | no |
| B19 |  | blank (no value stored) | uncolored | yes |
| C19 |  | blank (no value stored) | uncolored | yes |
| D19 |  | blank (no value stored) | uncolored | yes |
| E19 |  | blank (no value stored) | uncolored | yes |
| A20 | `مازاد تجديد ارزيابي دارايي‌ها ` | s (string) | uncolored | no |
| B20 | `0` | n (number) | uncolored | no |
| C20 | `0` | n (number) | uncolored | no |
| D20 | `0` | n (number) | uncolored | no |
| E20 |  | blank (no value stored) | uncolored | yes |
| A21 | `تفاوت تسعیر ارز عملیات خارجی ` | s (string) | uncolored | no |
| B21 | `0` | n (number) | uncolored | no |
| C21 | `0` | n (number) | uncolored | no |
| D21 | `0` | n (number) | uncolored | no |
| E21 |  | blank (no value stored) | uncolored | yes |
| A22 | `مالیات مربوط به سایر اقلام سود و زیان جامع ` | s (string) | uncolored | no |
| B22 | `0` | n (number) | uncolored | no |
| C22 | `0` | n (number) | uncolored | no |
| D22 | `0` | n (number) | uncolored | no |
| E22 |  | blank (no value stored) | uncolored | yes |
| A23 | `سایر اقلام سود و زیان جامع سال پس از کسر مالیات ` | s (string) | uncolored | no |
| B23 | `0` | n (number) | uncolored | no |
| C23 | `0` | n (number) | uncolored | no |
| D23 | `0` | n (number) | uncolored | no |
| E23 |  | blank (no value stored) | uncolored | yes |
| A24 | `سود(زيان) جامع سال ` | s (string) | uncolored | no |
| B24 | `-25195703` | n (number) | uncolored | no |
| C24 | `-35246257` | n (number) | uncolored | no |
| D24 | `-9124895` | n (number) | uncolored | no |
| E24 | `29` | n (number) | uncolored | no |

### 10.3 Table-like region on this worksheet

- Candidate **S01** `A16:E24` (basis: blue header A16:E17 immediately followed by contiguous valued rows 18–24; **no** border, **no** yellow, **no** gray, **no** black). Full evidence is in §7 (S01) and §6.
- Red name A14 is 2 rows above the blue header (row 15 holds the uncolored string A15 `کلیه مبالغ درج شده به میلیون ریال می باشد`).
- Green marker A19 lies directly below the first data row; rows 20–24 in column A are uncolored strings (no yellow); B20:D23 hold stored numeric `0` values in uncolored cells; B19:E19 and E20:E23 are blank uncolored cells; B18:E18 and B24:E24 hold uncolored numbers.
- Rows 1–12 hold uncolored label strings in column A only (A1:A12). Each of those 12 strings is identical to the value of a green cell on `Recovered_Sheet1`: A1=`Recovered_Sheet1`!A12, A2=`Recovered_Sheet1`!A32, A3=`Recovered_Sheet1`!A35, A4=`Recovered_Sheet1`!A63, A5=`Recovered_Sheet1`!A81, A6=`Recovered_Sheet1`!A96, A7=`Recovered_Sheet1`!A108, A8=`Recovered_Sheet1`!A178, A9=`Recovered_Sheet1`!A182, A10=`Recovered_Sheet1`!A191, A11=`Recovered_Sheet1`!A268, A12=`Recovered_Sheet1`!A314. In `Sheet1` these cells are uncolored. (Observation only.)

### 10.4 Facts about similarity to the first worksheet (no duplicate claim made)

Header-cell positional comparison (same relative positions: Sheet1 A16:E17 vs. first-sheet A60:E61, shown because the red-name text of the two sheets is identical):

| Sheet1 cell | Sheet1 value | First-sheet cell | First-sheet value | First-sheet role | Text vs. Sheet1 |
|---|---|---|---|---|---|
| Sheet1!A16 | `شرح` | Recovered_Sheet1!A60 | `شرح` | Blue | same |
| Sheet1!B16 | `دوره منتهي به ۱۴۰۳/۰۶/۳۱` | Recovered_Sheet1!B60 | `دوره منتهي به ۱۴۰۳/۰۶/۳۱` | Blue | same |
| Sheet1!C16 | `تجدید ارائه شده ۱۴۰۲/۰۶/۳۱` | Recovered_Sheet1!C60 | `تجدید ارائه شده ۱۴۰۲/۰۶/۳۱` | Black | same |
| Sheet1!D16 | `تجدید ارائه شده ۱۴۰۲/۱۲/۲۹` | Recovered_Sheet1!D60 | `تجدید ارائه شده ۱۴۰۲/۱۲/۲۹` | Blue | same |
| Sheet1!E16 | `درصد تغییر` | Recovered_Sheet1!E60 | `درصد تغییر` | Blue | same |
| Sheet1!A17 | (blank) | Recovered_Sheet1!A61 | (blank) | Blue | same |
| Sheet1!B17 | `حسابرسی نشده` | Recovered_Sheet1!B61 | `حسابرسی نشده` | Blue | same |
| Sheet1!C17 | `حسابرسی شده` | Recovered_Sheet1!C61 | `حسابرسی شده` | Black | same |
| Sheet1!D17 | `حسابرسی شده` | Recovered_Sheet1!D61 | `حسابرسی شده` | Blue | same |
| Sheet1!E17 | (blank) | Recovered_Sheet1!E61 | (blank) | Blue | same |

Red-name text `Sheet1!A14` is identical to `Recovered_Sheet1!A58`. Annotation differences (observed): the first sheet's T02 has yellow, gray, black, green, a non-ordinary border and a right-to-left direction; `Sheet1` has none of yellow, gray, black or a non-ordinary border and is left-to-right. Header text is identical position by position in all 10 compared cells (see table), while the role of C16:C17-equivalent cells on the first sheet (C60:C61) is Black and on `Sheet1` is Blue. These are observations; **no classification of `Sheet1` as table, duplicate, or non-table is made here**.

## 11. Blank gray cell inventory and zero interpretation

- Total gray cells (workbook): **459** (`Recovered_Sheet1` 459, `Sheet1` 0).
- Blank gray cells (no `<v>` stored; Excel value empty): **89** (`Recovered_Sheet1` 89, `Sheet1` 0). They are gray-filled (raw theme 0, tint −0.25) cells, so they are extraction cells by owner rule 7 and are **not** uncolored.
- Gray cells whose stored value is numeric `0`: **134** — B29:B30, D30, B33, D33, B39, D39, B64:B67, D64:D67, B98:C100, B103:C104, B112:B113, C112, B117:C117, H154:I155, L154, B155:G155, K155, J156:J158, L156:L158, B157:B158, D157:E157, G157:I157, C158, K160, L160:L164, E161:E162, H162:I162, J162:J164, F163, G164, C165:E165, H165:I165, D180, D186, B192:B194, D192:D194, B197:B206, D198:D206, C240, G240, I240, E245:E246, G245:G246, I245:I246, G253, I253, C303, C305:C306, D317:D319, D325, C338:C339, I355:I358, C367, C378, C396:C397, B405, D405:E405. These are *not* blank cells; a stored `0` is distinct from a blank.
- Owner rule 7 (not an observation): a blank gray cell is to be read as numeric `0`, not NULL/missing.

### 11.1 Blank gray cells — full list by candidate

| Candidate | Bounds | Blank gray | All gray in candidate | Blank gray coordinates |
|---|---|---|---|---|
| T04 | `A130:L165` | 85 | 143 | B153:G154, H153:I153, K153:K154, J154, B156, C156:C157, D156:E156, F156:F162, G156:I156, K156:K158, D158:D164, E158:E160, G158:G163, H158:I161, B159:C164, J159:J161, K161:K164, E163:E164, H163:I164, F164 |
| T06 | `A238:I253` | 4 | 48 | C248:C251 |

### 11.2 T04 gray block: per-row blank pattern (gray block `B153:L165`; columns B–L)

| Row | # blank gray | Blank gray columns | # numeric gray | Numeric gray columns |
|---|---|---|---|---|
| 153 | 9 | B, C, D, E, F, G, H, I, K | 2 | J, L |
| 154 | 8 | B, C, D, E, F, G, J, K | 3 | H, I, L |
| 155 | 0 | — | 11 | B, C, D, E, F, G, H, I, J, K, L |
| 156 | 9 | B, C, D, E, F, G, H, I, K | 2 | J, L |
| 157 | 3 | C, F, K | 8 | B, D, E, G, H, I, J, L |
| 158 | 7 | D, E, F, G, H, I, K | 4 | B, C, J, L |
| 159 | 9 | B, C, D, E, F, G, H, I, J | 2 | K, L |
| 160 | 9 | B, C, D, E, F, G, H, I, J | 2 | K, L |
| 161 | 9 | B, C, D, F, G, H, I, J, K | 2 | E, L |
| 162 | 6 | B, C, D, F, G, K | 5 | E, H, I, J, L |
| 163 | 8 | B, C, D, E, G, H, I, K | 3 | F, J, L |
| 164 | 8 | B, C, D, E, F, H, I, K | 3 | G, J, L |
| 165 | 0 | — | 11 | B, C, D, E, F, G, H, I, J, K, L |

### 11.3 Raw attributes of blank gray cells

| style index `s` | numFmtId | role | non-ordinary border sides | count |
|---|---|---|---|---|
| 90 | 0 | G | none | 89 |

Every blank gray cell is a `<c>` element with a style index and no `<v>`/no `t` attribute (Excel data type blank, number format General). Numeric gray cells use number formats `[$-3000401]#,##0` (id 164), `[$-3000401]0` (id 165) or `[$-3000401]0.##` (id 167).

## 12. Anomaly and conflict register

Each item lists exact coordinates. Items are observations; none is resolved by guessing.

**AN-01 — Red name without an identifiable (bordered) table.** On `Recovered_Sheet1` every red cell has a distinguishable-bordered region 1–2 rows below (A8, A58, A77, A128, A174, A236, A264, A277, A300, A311, A334, A351, A359, A374, A384, A393, A403). On `Sheet1`, red A14 has **no** bordered region: nearest annotated region is S01 `A16:E24` (blue header, one green marker, no border/yellow/gray). Table validity for S01 is **unresolved**.

**AN-02 — Table-like bordered region without a red name.** No rectangular bordered candidate without a red name was found. Non-ordinary border segments outside all candidates: full-width bottom borders on rows 1, 5, 51, 55, 70, 74, 121, 125, 167, 171, 228, 232, 287, 291, 343, 347 (A:L, `thin` `rgb:FF000000`, 192 sides); and A58 (left+top), A59 (left), E68 (bottom), all `thin` `indexed:64`, next to T02. Table-like but **unbordered** region without a red name: U01 `A297:D299` (blue header `A297:D297`, uncolored valued rows 298–299; preceding uncolored text A295 `وضعیت کارکنان:` and A296).

**AN-03 — Blue headers without gray extraction cells in their column** (blue cells, in the candidate rows, whose column has no gray cell in those rows; includes columns outside the bordered rectangle):

| Candidate | Blue cells without gray in column | Columns that do have gray in those rows |
|---|---|---|
| T01 | A10:A11, E10:E11 | B, D |
| T02 | A60:A61, E60:E61 | B, D |
| T03 | A79:A80, D79:E80, A95, D95 | B, C |
| T04 | A130 | B, C, D, E, F, G, H, I, J, K, L |
| T05 | A176:A177, E176:E177 | B, D |
| T06 | A238:A239, J238:K239, B239, D239, F239, H239 | C, E, G, I |
| T07 | A266:A267, B266, D266:F267 | C |
| T08 | A279, C279:F279 | B |
| U01 | A297:D297 | no gray in these rows |
| T09 | A302, D302:E302 | C |
| T10 | A313, E313:G313 | D |
| T11 | A336, D336:E336 | C |
| T12 | A353:B354, J353:K354 | G, H, I |
| T13 | A361 | C |
| T14 | A376 | C |
| T15 | A386 | C |
| T16 | A395 | C |
| S01 | A16:E17 | no gray in these rows |

**AN-04 — Gray cells without a yellow description in the same row.** See table.

| Sheet | Row | Gray cells in row |
|---|---|---|
| Recovered_Sheet1 | row 405 | A405:E405 |

**AN-05 — Blank gray cells.** 89 blank gray cells: B153:G154, H153:I153, K153:K154, J154, B156, C156:C157, D156:E156, F156:F162, G156:I156, K156:K158, D158:D164, E158:E160, G158:G163, H158:I161, B159:C164, J159:J161, K161:K164, E163:E164, H163:I164, F164, C248:C251. T04: B153:G154, H153:I153, K153:K154, J154, B156, C156:C157, D156:E156, F156:F162, G156:I156, K156:K158, D158:D164, E158:E160, G158:G163, H158:I161, B159:C164, J159:J161, K161:K164, E163:E164, H163:I164, F164; T06: C248:C251. Full detail §11.

**AN-06 — Yellow cells without a gray cell in the same row.** None found: every yellow cell shares its row with at least one gray cell. (Blank yellow cells B355:B358 are non-anchor cells of merged A355:B355…A358:B358 and share their rows with G:I gray cells.)

**AN-07 — Green markers without clear sub-table extents.** T03 A81: span 82–95, non-yellow in marker column: A95[Blue]; T13 A362: span 363–365, non-yellow in marker column: A364[uncolored]. `Sheet1` A19: no yellow cell exists on that worksheet (A20:A24 are uncolored). Yellow rows preceding the first green marker of their candidate (belong to no marker by the sub-table rule): T02: yellow A62 before first marker A63. Bordered candidates with yellow but no green marker at all: T06, T08, T09, T11, T12, T14, T15, T16.

**AN-08 — Black cells mixed with gray extraction cells in the same candidate.** Black stored values exist in these regions (numeric values counted in the last column); they are excluded by rule.

| Candidate | Black cells | Pattern | Gray columns | Interleaving | # black cells holding numbers |
|---|---|---|---|---|---|
| T01 | C10:C42 | black cols (≥70% of rows): C; wholly black rows: — | gray cols: B, D | black column(s) lie between gray columns: C | 28 |
| T02 | C60:C68 | black cols (≥70% of rows): C; wholly black rows: — | gray cols: B, D | black column(s) lie between gray columns: C | 6 |
| T04 | A131:L151 | black cols (≥70% of rows): —; wholly black rows: A131:L151 | gray cols: B, C, D, E, F, G, H, I, J, K, L | no black column; wholly black rows above the gray rows | 136 |
| T05 | C176:C213 | black cols (≥70% of rows): C; wholly black rows: — | gray cols: B, D | black column(s) lie between gray columns: C | 33 |
| T06 | B238, D238, F238, H238, B240:B253, D240:D253, F240:F253, H240:H253 | black cols (≥70% of rows): B, D, F, H; wholly black rows: — | gray cols: C, E, G, I | black column(s) lie between gray columns: D, F, H | 48 |
| T07 | B267:B275 | black cols (≥70% of rows): B; wholly black rows: — | gray cols: C | black column(s) lie between gray columns: no | 7 |
| T09 | B302:B308 | black cols (≥70% of rows): B; wholly black rows: — | gray cols: C | black column(s) lie between gray columns: no | 6 |
| T10 | B313:C332 | black cols (≥70% of rows): B, C; wholly black rows: — | gray cols: D | black column(s) lie between gray columns: no | 36 |
| T11 | B336:B339 | black cols (≥70% of rows): B; wholly black rows: — | gray cols: C | black column(s) lie between gray columns: no | 3 |
| T12 | C353:F358 | black cols (≥70% of rows): C, D, E, F; wholly black rows: — | gray cols: G, H, I | black column(s) lie between gray columns: no | 12 |
| T13 | B361:B367 | black cols (≥70% of rows): B; wholly black rows: — | gray cols: C | black column(s) lie between gray columns: no | 3 |
| T14 | B376:B378 | black cols (≥70% of rows): B; wholly black rows: — | gray cols: C | black column(s) lie between gray columns: no | 2 |
| T15 | B386:B387 | black cols (≥70% of rows): B; wholly black rows: — | gray cols: C | black column(s) lie between gray columns: no | 1 |
| T16 | B395:B398 | black cols (≥70% of rows): B; wholly black rows: — | gray cols: C | black column(s) lie between gray columns: no | 3 |

**AN-09 — Missing or incomplete borders.** Continuity result: **no gap** was found on any of the four outer edges of the 17 bordered candidates (§5.2, §7). Other border observations: (a) T16 `A395:C398` and T17 `A404:E405` use `thin` `indexed:64` for all four edges, all other bordered candidates use `medium` `indexed:64`; (b) T02: the stored left/top sides on A58 (red cell) and left side on A59 extend the left edge upward over rows 58–59, and E68 carries a bottom side outside the rectangle (all `thin` `indexed:64`); (c) U01 `A297:D299` and S01 `A16:E24` have no non-ordinary border; (d) colour-annotated cells exist outside the bordered rectangle in T01, T02, T03, T05, T06, T07, T08, T09, T10, T11, T12 (see "outside" lists in §7) — the border does not cover them.

Annotated and valued cells directly beside bordered rectangles (same rows, outside the border):

| Candidate | Annotated (colour) cells outside border | Uncolored cells with values outside border |
|---|---|---|
| T01 | E10:E11 | E13:E28, E31, E34, E36:E38, E40, E42 |
| T02 | E60:E61 | E62, E68 |
| T03 | D79:E80, D95 | D82:D94, E82:E95, D97:D107, E97, E101:E102, E105:E107, D109:D119, E109:E111, E113:E116, E118:E119 |
| T05 | E176:E177 | E179:E181, E183:E185, E187:E190, E193, E195:E196, E198, E207:E213 |
| T06 | J238:K239 | J240:K243, J245:K249, J251:K253 |
| T07 | D266:F267 | D269:F271, D273:F273, D275:F275 |
| T08 | C279:F279 | C280:F283 |
| T09 | D302:E302 | D303:D308 |
| T10 | E313:G313 | E315:F332 |
| T11 | D336:E336 | D337:D339 |
| T12 | J353:K354 | J355:J358 |

**AN-10 — Uncolored cells inside otherwise annotated regions.** Split into (i) uncolored cells located in the same row as a green marker and (ii) uncolored cells in other rows. Values are noted in §7.

| Candidate | Uncolored in green-marker rows | Uncolored in other rows | Value summary |
|---|---|---|---|
| T01 | B12, D12, B32, D32, B35, D35 | — | 0 with values |
| T02 | B63, D63 | — | 0 with values |
| T03 | B81:C81, B96:C96, B108:C108 | — | 0 with values |
| T04 | B152:L152 | — | 0 with values |
| T05 | B178, D178, B182, D182, B191, D191 | — | 0 with values |
| T06 | — | A243:A244, C243:C244, E243:E244, G243:G244, I243:I244 | 6 with values |
| T07 | C268 | — | 0 with values |
| T10 | D314 | — | 0 with values |
| T13 | C362, C366 | A364, C364 | 0 with values |

**AN-11 — Merged cells that complicate bounds or interpretation.** Total merges: 103 (`Recovered_Sheet1` 101, `Sheet1` 2). Merges crossing a candidate boundary: none. Merges whose cells carry different roles: none. Merges outside every candidate: Recovered_Sheet1!A411:I411, Recovered_Sheet1!A391:B391, Recovered_Sheet1!C391:F391, Recovered_Sheet1!A401:B401, Recovered_Sheet1!C401:F401, Recovered_Sheet1!B407:E407, Recovered_Sheet1!A410:I410, Recovered_Sheet1!J358:K358, Recovered_Sheet1!A372:B372, Recovered_Sheet1!C372:F372, Recovered_Sheet1!A382:B382, Recovered_Sheet1!C382:F382, Recovered_Sheet1!J355:K355, Recovered_Sheet1!J356:K356, Recovered_Sheet1!J357:K357, Recovered_Sheet1!D340:E340, Recovered_Sheet1!A341:G341, Recovered_Sheet1!A350:K350, Recovered_Sheet1!J353:K354, Recovered_Sheet1!A333:B333, Recovered_Sheet1!C333:I333, Recovered_Sheet1!D336:E336, Recovered_Sheet1!D337:E337, Recovered_Sheet1!D338:E338, Recovered_Sheet1!D339:E339, Recovered_Sheet1!F327:G327, Recovered_Sheet1!F328:G328, Recovered_Sheet1!F329:G329, Recovered_Sheet1!F330:G330, Recovered_Sheet1!F331:G331, Recovered_Sheet1!F332:G332, Recovered_Sheet1!F321:G321, Recovered_Sheet1!F322:G322, Recovered_Sheet1!F323:G323, Recovered_Sheet1!F324:G324, Recovered_Sheet1!F325:G325, Recovered_Sheet1!F326:G326, Recovered_Sheet1!F315:G315, Recovered_Sheet1!F316:G316, Recovered_Sheet1!F317:G317, Recovered_Sheet1!F318:G318, Recovered_Sheet1!F319:G319, Recovered_Sheet1!F320:G320, Recovered_Sheet1!D306:E306, Recovered_Sheet1!D307:E307, Recovered_Sheet1!D308:E308, Recovered_Sheet1!B310:G310, Recovered_Sheet1!F313:G313, Recovered_Sheet1!F314:G314, Recovered_Sheet1!A285:I285, Recovered_Sheet1!A294:K294, Recovered_Sheet1!D302:E302, Recovered_Sheet1!D303:E303, Recovered_Sheet1!D304:E304, Recovered_Sheet1!D305:E305, Recovered_Sheet1!D266:E266, Recovered_Sheet1!F266:F267, Recovered_Sheet1!D276:J276, Recovered_Sheet1!B284:F284, Recovered_Sheet1!A256:B256, Recovered_Sheet1!C256:I256, Recovered_Sheet1!A259:B259, Recovered_Sheet1!C259:I259, Recovered_Sheet1!A262:B262, Recovered_Sheet1!C262:I262, Recovered_Sheet1!A225:E225, Recovered_Sheet1!A226:E226, Recovered_Sheet1!A235:K235, Recovered_Sheet1!J239:K239, Recovered_Sheet1!A222:E222, Recovered_Sheet1!A223:E223, Recovered_Sheet1!A224:E224, Recovered_Sheet1!A48:E48, Recovered_Sheet1!A49:E49, Recovered_Sheet1!E60:E61, Recovered_Sheet1!E79:E80, Recovered_Sheet1!E10:E11, Recovered_Sheet1!A44:E44, Recovered_Sheet1!A45:E45, Recovered_Sheet1!A46:E46, Recovered_Sheet1!A47:E47, Recovered_Sheet1!E176:E177, Recovered_Sheet1!A221:E221.

Annotated non-anchor cells inside merged ranges (these cells carry a fill in the XML but would read as merged/empty cells in libraries that discard merged non-anchor styles, e.g. openpyxl):

| Sheet | Role | Count | Coordinates |
|---|---|---|---|
| Recovered_Sheet1 | Blue | 29 | A11, E11, A61, E61, A80, E80, A177, E177, A239, C239, E239, G239, I239, K239, C266, E266, A267, F267, E302, G313, E336, B353:B354, H353:I353, K353:K354, A354, J354 |
| Recovered_Sheet1 | Black | 3 | D353:F353 |
| Recovered_Sheet1 | Yellow | 4 | B355:B358 |
| Sheet1 | Blue | 2 | A17, E17 |

**AN-12 — Formula cells or unsupported cell types.** Formula cells: 0. Boolean, error, inline-string, date-typed cells: 0. Numeric-looking text stored as a string in an uncolored cell: E180 (E180 = `-Infinity `, stored as text; the cell is outside T05's border and uncolored). Annotated text cells containing invisible characters (ZWNJ U+200C / soft hyphen U+00AD): 59 cells (Recovered_Sheet1!A14, Recovered_Sheet1!A19, Recovered_Sheet1!A23, Recovered_Sheet1!A24, Recovered_Sheet1!A26, Recovered_Sheet1!A64, Recovered_Sheet1!A87, Recovered_Sheet1!A88, Recovered_Sheet1!A90, Recovered_Sheet1!A91, Recovered_Sheet1!A93, Recovered_Sheet1!A94, Recovered_Sheet1!A95, Recovered_Sheet1!A102, Recovered_Sheet1!A103, Recovered_Sheet1!A108, Recovered_Sheet1!A110, Recovered_Sheet1!A114, Recovered_Sheet1!A117, Recovered_Sheet1!A118, Recovered_Sheet1!A119, Recovered_Sheet1!G130, Recovered_Sheet1!H130, Recovered_Sheet1!A133, Recovered_Sheet1!A136, Recovered_Sheet1!A138, Recovered_Sheet1!A150, Recovered_Sheet1!A164, Recovered_Sheet1!A178, Recovered_Sheet1!A180, Recovered_Sheet1!A181, Recovered_Sheet1!A182, Recovered_Sheet1!A183, Recovered_Sheet1!A184, Recovered_Sheet1!A185, Recovered_Sheet1!A186, Recovered_Sheet1!A189, Recovered_Sheet1!A190, Recovered_Sheet1!A191, Recovered_Sheet1!A192, Recovered_Sheet1!A193, Recovered_Sheet1!A194, Recovered_Sheet1!A195, Recovered_Sheet1!A196, Recovered_Sheet1!A197, Recovered_Sheet1!A198, Recovered_Sheet1!A199, Recovered_Sheet1!A200, Recovered_Sheet1!A201, Recovered_Sheet1!A202, Recovered_Sheet1!A203, Recovered_Sheet1!A204, Recovered_Sheet1!A205, Recovered_Sheet1!A206, Recovered_Sheet1!A207, Recovered_Sheet1!A208, Recovered_Sheet1!A332, Recovered_Sheet1!A334, Recovered_Sheet1!A395).

**AN-13 — Discrepancy between expected visual appearance and raw metadata.** (a) Two raw blue shades: `FF0197C8` (135 cells) and `FF0070C0` (4 cells, A95:D95; A95:C95 inside the T03 border, D95 outside it). (b) Two raw black shades (theme 1 tint 0.05: 252 cells; theme 1 tint 0: 240 cells): T04 rows 131–151 use the lighter-tint shade; the tint-0 shade is used in the black columns of the other tables (listed in §4). (c) Gray and black fills are **theme** colours, not `rgb`; an `rgb`-only detector would not see them. (d) The ordinary cell border is `medium` `FFDDDDDD`; style name alone cannot separate it from the owner's outer border. (e) 36 filled cells on `Recovered_Sheet1` and 2 on `Sheet1` are non-anchor cells of merged ranges (see above). (f) Row-level `thickBot="1"` appears on 314 rows of `Recovered_Sheet1` and 22 rows of `Sheet1` without corresponding cell-level non-ordinary borders; it was not used as evidence. (g) Cells with non-default borders but no fill exist inside candidates (e.g. A364, C364, A243, A244).

**AN-14 — Uncolored numeric cells next to tables.** 206 uncolored numeric cells on `Recovered_Sheet1`: E13:E28, E31, E34, E36:E38, E40, E42, E62, E68, D82:E94, D97:D107, E97, E101:E102, E105:E107, D109:D119, E109:E111, E113:E116, E118:E119, E179, E181, E183:E185, E187:E190, E193, E195:E196, E198, E207:E213, J240:K243, C243, E243, G243, I243, J245:K249, J251:K254, B254:I254, D269:E271, D273:E273, D275:E275, B276:C276, C280:C283, E280:F283, B298:D299, E315:E332, B340:C340, B369:C370, B380:C380, B389:C389, B399:C399. By the owner rule these are not extracted; they lie in columns adjacent to table candidates (see "outside" lists in §7) and inside T06 (row 243: C243, E243, G243, I243).

**AN-15 — Red cell with identical text on both worksheets.** `Recovered_Sheet1!A58` = `صورت سود و زیان جامع` and `Sheet1!A14` = `صورت سود و زیان جامع` are identical strings in two different regions; no equivalence is asserted.

**AN-16 — Header-like row inside a bordered region.** T03: A95:C95 (blue `FF0070C0`) lie inside the border `A79:C119`; D95 is also `FF0070C0` outside the border; E95 is an uncolored string `درصد تغييرات `. The green-to-green span of A81 (rows 82–95) therefore contains a non-yellow, non-gray, blue row (row 95).

**AN-17 — Blue header row without red name, border, yellow or gray.** U01: A297:D297 = A297=`شرح`, B297=`در تاریخ ۱۴۰۲/۱۲/۲۹`, C297=`در تاریخ ۱۴۰۳/۰۶/۳۱`, D297=`برآورد در تاریخ ۱۴۰۳/۱۲/۳۰`; rows 298–299 hold uncolored values A298:D299.

**AN-18 — Table with gray cells and no yellow column.** T17 `A404:E405`: blue header A404:E404, gray A405:E405 (5 cells; none blank), no yellow, no green, no black; red name A403 is 1 row above (all other red names are 2 rows above their region).

**AN-19 — Region with an entire block of black rows.** T04 `A130:L165`: rows 131–151 (A131:L151, 252 cells, theme 1 tint 0.05) are black across **all** 12 columns including column A; yellow/gray/green start only at row 152 (A152 green) / 153. Black cells in rows 131–151 hold stored values (numeric and text, listed in §4).

## 13. Final factual summary and unresolved questions

### 13.1 Counts (reproducible from §4)

| Role | Recovered_Sheet1 | Sheet1 | Workbook |
|---|---|---|---|
| Red | 17 | 1 | 18 |
| Blue | 129 | 10 | 139 |
| Yellow | 182 | 0 | 182 |
| Gray | 459 | 0 | 459 |
| Black | 492 | 0 | 492 |
| Green | 15 | 1 | 16 |
| Uncolored (cell present in XML, no fill) | 831 | 47 | 878 |

Blank gray cells: **89** (`Recovered_Sheet1`: 89; `Sheet1`: 0).

### 13.2 Summary of facts

- Workbook SHA-256 `69186f1ad2b0e481a3588f2731b7027b0a9d9a543d1ca17fd24fc71d8c5aca06`; 2 worksheets inspected; 0 formula cells; 0 hidden sheets/rows/columns.
- 18 red cells: 17 on `Recovered_Sheet1`, 1 on `Sheet1`. All 17 on `Recovered_Sheet1` have a continuous non-ordinary outer border 1–2 rows below them (T01–T17). The red cell on `Sheet1` has no bordered region.
- Non-ordinary borders are `medium` `indexed:64` (15 candidates) or `thin` `indexed:64` (T16, T17); ordinary borders are `medium` `FFDDDDDD` everywhere else.
- Yellow description column = lowest-index column (A) in 16 of 17 bordered candidates (T12 uses A and B); T17 has none. Gray cells are in higher-index columns, black cells between or beside them.
- Blue headers extend beyond the bordered rectangle (without gray beneath) in T01, T02, T03, T05, T06, T07, T08, T09, T10, T11, T12; uncolored numeric/text cells occupy those outside columns.
- 89 blank gray cells exist, all on `Recovered_Sheet1` (T04: 85; T06: 4); none on `Sheet1`.
- `Sheet1` contains red A14, blue A16:E17, green A19, and no yellow, gray, black or non-ordinary border.

### 13.3 Unresolved questions for the owner (not resolved by guessing)

1. Do blue-header columns that lie **outside** the bordered rectangle and have uncolored data beneath (T01 E10:E11; T02 E60:E61; T03 D79:E80; T05 E176:E177; T06 J238:K239; T07 D266:F267; T08 C279:F279; T09 D302:E302; T10 E313:G313; T11 D336:E336; T12 J353:K354) belong to the table or not? Their data cells are uncolored.
2. T03: what is the role of the blue (`FF0070C0`) row A95:D95 (A95:C95 inside the border, D95 outside) — second header of the same table or boundary of sub-tables? The green A81 span reaches it.
3. T04: are black rows 131–151 (all columns A:L) intended as excluded rows? The owner convention speaks of black *columns*.
4. T06: rows 243–244 (A243 `جمع`, A244 `کسر می شود:`) and C243/E243/G243/I243 are uncolored inside the border. Are they intentionally excluded?
5. T06: four blank gray cells C248:C251 — confirm zero interpretation per rule 7 (they sit amid numeric gray cells of the same column).
6. T04: 85 blank gray cells in B153:K164 — confirm zero interpretation per rule 7, and whether the sparse pattern is intentional.
7. T08 `A279:B283`: C279:F279 are blue headers outside the border with uncolored data C280:F283 beneath; D279 repeats the header text `شرح`. One table or two?
8. U01 `A297:D299` (blue header, uncolored values, no red name, no border): is it an owner-intended table?
9. T13: row 364 (A364, C364 uncolored; B364 black) inside the border and between yellow rows: intentional separator?
10. T17 `A404:E405` has a red name, blue headers, gray values, `thin` border and no yellow: confirm it is the owner-annotated "no yellow column" exception (rule 8).
11. `Sheet1`: is red A14 + blue A16:E17 + green A19 a table, a stray copy, or leftover? It has no border, yellow, gray or black.
12. T02: the stored left/top border on A58–A59 and bottom border on E68 extend beyond `A60:D68`; intentional?
13. Right-to-left display: border side names are stored in column-index terms; mirrored display on the RTL sheet was not verified visually.

### 13.4 Inspection limitations

- No visual rendering was made; colours/borders are from stored metadata only; theme-colour RGB values are approximate (raw theme/tint preserved).
- Candidate rectangles for T01–T17 are from the stored non-ordinary borders; U01 and S01 rectangles are evidence-based extents (no border exists). Whether any candidate is a valid extractable table is **not decided** here.
- Only column A was followed for green-marker → yellow label regions (all markers sit in column A).
- Border side names are reported as stored (see §1.1).
- Everything else in the workbook package (styles, theme, strings) was readable; no part could not be inspected.
