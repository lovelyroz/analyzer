# Parsian Periodic — Structural Review of Report 3

Status: **EVIDENCE REVIEW COMPLETE / TEMPLATE STILL PROVISIONAL**  
Date: 2026-11-17  
Source: `database/reports/parsian_periodic_report_3.md`  
Source blob SHA: `44d16ddcc2335128bf343db89f2ed9934b96f231`  
Workbook SHA recorded in report 3: `69186f1ad2b0e481a3588f2731b7027b0a9d9a543d1ca17fd24fc71d8c5aca06`  
Current corrected workbook SHA from the 2026-11-17 audit: `95f94e739632e48ae6552c562ecbf6c3e8182848718d17977f69bc984a6638b0`

## 1. Scope and provenance limitation

Report 3 is a direct OOXML re-audit of the earlier `parsian_periodic.xlsx`. It inspected two worksheets. The owner subsequently deleted the temporary `Sheet1`; only `Recovered_Sheet1` remains in the corrected workbook.

Report 3 is therefore **not a second-period workbook** and cannot validate layout drift between reporting periods. Its findings for `Recovered_Sheet1` are valuable detailed evidence for the sample, but the workbook SHA differs from the corrected workbook SHA. The available reports do not provide a sheet-XML hash proving byte-for-byte identity of the retained worksheet across the two workbook packages. Treat the report-3 bounds as strong historical structural evidence for the main sheet, subject to final confirmation against the corrected sample if any disputed coordinate affects approval.

All `Sheet1` findings, including S01 `A16:E24`, red `A14`, and green `A19`, are excluded as temporary-test-sheet noise.

## 2. Important correction: black fill detection

Report 3's direct OOXML inventory identifies **492 black cells on Recovered_Sheet1**:
- 252 cells: theme 1, tint 0.05
- 240 cells: theme 1, tint 0

It also identifies 459 gray cells (89 blank), 182 yellow, 129 blue (including 4 cells of a second blue shade), 17 red, and 15 green. Some counts include styled non-anchor cells inside merged ranges.

The corrected 2026-11-17 annotation audit reported zero black cells. This is a detection/classification gap: theme-based black fills were not included in its explicit black-fill count. Consequently:
- the statement “there are zero black cells” is withdrawn;
- the current annotation audit must not be treated as complete for theme-based fill roles;
- black-filled cells remain excluded under the owner's annotation convention;
- do not treat the 492 count as independently revalidated against the corrected workbook until the retained sheet is confirmed.

The same XML report distinguishes ordinary borders (`medium`, RGB `FFDDDDDD`) from non-ordinary table-edge borders (`medium` or `thin`, indexed 64). Border style name alone is not a valid discriminator.

## 3. Border-supported candidate table bounds

Report 3 found continuous distinguishable outer-edge evidence on all four sides of each of the following 17 main-sheet candidates. These are **evidence-supported sample bounds**, not yet owner-approved production Template bounds.

| ID | Red title cell | Candidate bounds | Dimensions | Border |
|---|---|---|---:|---|
| T01 | A8 | A10:D42 | 33 × 4 | medium |
| T02 | A58 | A60:D68 | 9 × 4 | medium |
| T03 | A77 | A79:C119 | 41 × 3 | medium |
| T04 | A128 | A130:L165 | 36 × 12 | medium |
| T05 | A174 | A176:D213 | 38 × 4 | medium |
| T06 | A236 | A238:I253 | 16 × 9 | medium |
| T07 | A264 | A266:C275 | 10 × 3 | medium |
| T08 | A277 | A279:B283 | 5 × 2 | medium |
| T09 | A300 | A302:C308 | 7 × 3 | medium |
| T10 | A311 | A313:D332 | 20 × 4 | medium |
| T11 | A334 | A336:C339 | 4 × 3 | medium |
| T12 | A351 | A353:I358 | 6 × 9 | medium |
| T13 | A359 | A361:C367 | 7 × 3 | medium |
| T14 | A374 | A376:C378 | 3 × 3 | medium |
| T15 | A384 | A386:C387 | 2 × 3 | medium |
| T16 | A393 | A395:C398 | 4 × 3 | thin |
| T17 | A403 | A404:E405 | 2 × 5 | thin |

Report 3 states that every outer edge is continuous, with no gaps, for all 17 candidates. T02 has a few additional border sides extending outside its rectangle; these do not alter the listed rectangle.

## 4. Extraction and exclusion evidence

- Gray extraction cells: 459 total; 89 are blank. Per the owner's explicit rule, blank gray cells map to numeric zero during semantic extraction, not NULL.
- The 89 blank gray cells are distributed across T04 (85) and T06 (4).
- Black-filled cells are excluded. Report 3 identifies black values in many tables, including interleaved black columns in T01/T02/T05/T06 and a full black block in T04 rows 131–151.
- The T04 black block spans A131:L151 and contains 136 numeric values. The owner's convention clearly excludes black-filled cells, but whether an entire black row block is an intended exclusion rather than a special presentation area should remain an explicit owner-confirmation item before final template approval.
- T17 is a valid no-yellow exception according to the owner's later clarification: A404:E404 blue header and A405:E405 gray extraction cells. It has a thin but continuous outer border.
- T08 contains a secondary blue header at A297:D297 and uncolored values at rows 298–299, outside the T08 border. These are not extraction cells under the current gray-only rule.
- U01 A297:D299 is a separate unbordered blue-header/uncolored-value region with no red table title. It is not promoted to an extractable table.
- Blue header cells and uncolored valued cells extend beyond the border on several candidates. They are not automatically included in table bounds or extraction. In particular, do not expand table bounds merely to include columns with uncolored values.

## 5. Sub-table and structural exceptions requiring explicit treatment

Report 3 confirms 15 green markers on the main sheet. The row-partition rule can be applied provisionally, but these cases need explicit handling:
- T03 marker A81 spans through row 95, where A95:C95 are blue and D95 lies outside the border. This may be a secondary header or a structural transition; do not treat row 95 as ordinary label/data rows without owner confirmation.
- T13 marker A362 spans rows 363–365, but A364 is uncolored between yellow label rows. Preserve it as an observed structural anomaly; do not infer its meaning.
- T02 has yellow row A62 before its first green marker A63. That row belongs to the parent table but not to a green-marker-defined sub-table under the current partition rule.
- Several bordered tables have yellow labels but no green markers (T06, T08, T09, T11, T12, T14, T15, T16). This is valid: green markers are optional, not a required property of every table.
- Merged ranges do not cross the 17 candidate table boundaries in report 3. However, merged non-anchor cells carry annotation fills; the annotation reader must preserve those styles rather than relying only on openpyxl anchor-cell values.

## 6. Unresolved owner decisions / risks

1. Confirm whether black-filled T04 rows 131–151 are wholly excluded, consistent with the general black-cell exclusion rule.
2. Confirm the role of T03 row 95 (blue secondary header / structural boundary).
3. Confirm whether T06 uncolored rows 243–244 and their uncolored numeric cells are intentionally excluded (gray-only rule currently excludes them).
4. Confirm that the four blank gray cells C248:C251 and 85 blank gray cells in T04 are zero-valued extraction cells, as already required by the general blank-gray rule; confirm the sparse T04 pattern is intentional.
5. Confirm T13 row 364's uncolored cells as a structural separator or simply excluded cells; no semantic inference is permitted.
6. Confirm the T02 border extensions around A58:A59 and E68 are decorative/adjacent evidence, not part of the table bounds.
7. Confirm the visual RTL interpretation of stored border-side attributes if physical edge orientation is material to authoring.

The columns outside several bordered rectangles contain blue headers and uncolored values. Under the current rule they remain excluded; expanding the table geometry to include them would require an explicit owner decision and revised annotation.

## 7. Result and next gate

The report supplies continuous border-supported candidate bounds for all 17 main-sheet tables, resolving the earlier uncertainty about whether complete rectangles could be established from available evidence. It also exposes a significant blind spot in the newer audit's theme-color classification.

Task DB-ING-006 / Task 033 remains **PARTIAL**:
- sample candidate bounds now have detailed historical border evidence;
- black/theme fill classification needs correction or a targeted re-audit;
- unresolved structural exceptions need owner decisions;
- the map remains provisional until owner approval;
- drift validation still requires a genuinely different Parsian periodic workbook from another reporting period.

No code was changed and no tests were run as part of this report review. The assistant reviewed the Markdown report only; it did not open the XLSX directly.
