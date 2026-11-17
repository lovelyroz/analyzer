# Parsian Periodic Workbook — Annotation Map Draft

Status: **PROVISIONAL / NOT OWNER-APPROVED**  
Date: 2026-11-17  
Source workbook: `excel/parsian_periodic.xlsx`  
Source SHA-256: `95f94e739632e48ae6552c562ecbf6c3e8182848718d17977f69bc984a6638b0`  
Audit evidence: `database/reports/template_annotation_audit_parsian_final_output.txt`  
Audit report blob SHA: `6f1c2d4ba5c5f965d864c641b550f298316ef8c3`

## 1. Scope and provenance

The corrected audit reports exactly one worksheet:

- Worksheet: `Recovered_Sheet1`
- Used range: `A1:L411`
- Merged ranges: 101
- Reading direction: right-to-left
- Visual mapping: column A is displayed at the right; the visual right edge of a table beginning in A maps to the right border of its column-A cells.

The earlier `Sheet1` was a temporary test worksheet and was deleted by the owner. **All previous `Sheet1` findings are withdrawn and excluded.** This report supersedes earlier two-worksheet interpretations.

The audit was run by the owner and supplied as text. The assistant did not open the XLSX directly and did not run tests.

## 2. Annotation inventory

| Annotation | Cell count | Interpretation |
|---|---:|---|
| Red | 17 | Candidate top-level table titles |
| Blue | 96 | Header cells |
| Green | 15 | Sub-table title markers |
| Yellow | 178 | Row-description/label cells |
| Gray | 459 | Positive extraction cells |
| Black fill | 0 | No cells with the explicitly black annotation fill were found |

Gray-cell value states reported by the audit:

- 89 blank cells — owner rule: extract as numeric zero.
- 134 numeric zero cells — preserve as zero.
- 236 numeric nonzero cells — preserve the observed numeric value.
- Total: 459 gray extraction cells.

Uncolored cells remain excluded. The 0 count for black fill means no black annotation fill was detected in this audit; it does not convert transparent/no-fill cells into black annotations.

## 3. Candidate top-level sections

The row intervals below are **title-to-next-title review intervals**, not approved table bounds. A red title is a candidate parent-table identifier; it does not by itself prove the complete rectangle or column bounds.

| ID | Red title cell and observed title | Review row interval | Header cells / rows | Gray extraction coordinates |
|---|---|---:|---|---|
| T01 | A8 — صورت سود و زیان | 8–57 | A10:E11 | B,D rows 13–31, 33–34, 36–42 |
| T02 | A58 — صورت سود و زیان جامع | 58–76 | A60:E61 | B,D rows 62, 64–68 |
| T03 | A77 — صورت وضعیت مالی | 77–127 | A79:E80 | B:C rows 82–94, 97–107, 109–119 |
| T04 | A128 — صورت تغییرات در حقوق مالکانه | 128–173 | A130:L130 | B:L rows 153–165 |
| T05 | A174 — صورت جریان های نقدی | 174–235 | A176:E177 | B,D rows 179–181, 183–190, 192–213 |
| T06 | A236 — مانده تسهیلات اعطایی و ذخیره مطالبات مشکوک الوصول | 236–263 | A238:K239 | C,E,G,I rows 240–242, 245–253 |
| T07 | A264 — مانده سپرده های دریافتی از مشتریان | 264–276 | A266:F267 | C rows 269–275 |
| T08 | A277 — اقلام زیر خط | 277–299 | A279:F279; secondary header A297:D297 | B rows 280–283 |
| T09 | A300 — اطلاعات حق الوکاله و کفایت سرمایه | 300–310 | A302:D302 | C rows 303–308 |
| T10 | A311 — درآمد حاصل از تسهيلات اعطايي و سپرده گذاري | 311–333 | A313:G313 | D rows 315–332 |
| T11 | A334 — خالص سود (زیان) سرمایه گذاری ها | 334–350 | A336:D336 | C rows 337–339 |
| T12 | A351 — وضعیت شرکتهای سرمایه پذیر | 351–358 | A353:K354 | G:I rows 355–358 |
| T13 | A359 — ساير درآمدها و هزینه های عملياتي | 359–373 | A361:C361 | C363, C365, C367 |
| T14 | A374 — خالص ساير درآمدها و هزینه ها | 374–383 | A376:C376 | C377:C378 |
| T15 | A384 — هزینه های اداری و عمومی | 384–392 | A386:C386 | C387 |
| T16 | A393 — هزینه مالی | 393–402 | A395:C395 | C396:C398 |
| T17 | A403 — برنامه شرکت در خصوص تقسیم سود | 403–411 | A404:E404 | A405:E405 |

### Special observations

1. T08 has a second blue header at A297:D297 and uncolored data rows 298–299. No gray extraction cells exist in those rows. Under the current rule, those uncolored cells are excluded; the blue header alone does not authorize extraction.
2. T09 has a mixed header fill: A302, C302 and D302 are blue; B302 is not blue. The extraction coordinates are only C303:C308. The non-gray B-column cells are not extraction cells.
3. T17 has blue header A404:E404 and gray extraction cells A405:E405, but no yellow description column. This is the owner-confirmed valid exception; absence of yellow must not reject it.
4. No black annotation cells were identified in this audit.
5. Blank gray cells occur in T04 and T06; they remain extraction cells and must become zero during semantic extraction.

## 4. Green-marker sub-table partitions

The green marker establishes a row partition within its parent candidate section. The following row ranges are mechanically derived from marker order and the next marker / parent review interval. They are **provisional row partitions only**. Exact sub-table column bounds, header association, and complete parent table bounds are not yet approved.

| Parent candidate | Green marker | Provisional sub-table row interval | Yellow label rows |
|---|---|---:|---|
| T01 | A12 — عملیات در حال تداوم | 12–31 | 13–31 |
| T01 | A32 — عملیات متوقف شده | 32–34 | 33–34 |
| T01 | A35 — سود (زیان) پایه هر سهم | 35–42 | 36–42 |
| T02 | A63 — سایر اقلام سود و زیان جامع | 63–68 | 64–68 |
| T03 | A81 — دارایی ها | 81–94 | 82–94 |
| T03 | A96 — حقوق مالکانه | 96–107 | 97–107 |
| T03 | A108 — بدهی ها | 108–119 | 109–119 |
| T04 | A152 — تغییرات حقوق مالکانه در سال ۱۴۰۳/۰۶/۳۱ | 152–165 | 153–165 |
| T05 | A178 — جریان های نقدی حاصل از فعالیت های عملیاتی | 178–181 | 179–181 |
| T05 | A182 — فعالیت های سرمایه گذاری | 182–190 | 183–190 |
| T05 | A191 — فعالیت های تأمین مالی | 191–213 | 192–213 |
| T07 | A268 — سپرده های ریالی | 268–275 | 269–275 |
| T10 | A314 — درآمد تسهیلات اعطایی | 314–332 | 315–332 |
| T13 | A362 — سایر درآمدهای عملیاتی | 362–365 | 363, 365 |
| T13 | A366 — سایر هزینه های عملیاتی | 366–367 | 367 |

The rule does not mean that every row in a sub-table partition is a value row. Marker rows and intervening structural rows remain part of the structural partition; only gray cells are extraction cells.

## 5. Border and geometry evidence

- `THICK_OUTSIDE_RECTANGLES count=0` means no rectangle with the exact literal `thick` style was detected.
- The audit reports 101 border-evidence ranges, and the observed border style is `medium`.
- Several border ranges are partial or internal row/column boundaries; the report does not establish a complete outer rectangle for every candidate section.
- Therefore, **do not infer final table bounds from the red-title intervals, gray-cell extents, or the mere presence of medium borders**. The exact complete table rectangles still require owner review against the workbook's visual layout.
- Annotation colors are authoring evidence for this representative workbook only. Later Parsian reports are matched by the approved template structure, not by requiring the same colors or borders.

## 6. Current decisions and unresolved work

### Confirmed from owner decisions / current audit

- Only `Recovered_Sheet1` is in scope.
- Red cells identify 17 candidate top-level table titles.
- Green cells identify 15 candidate sub-table markers.
- Gray cells are the only positive extraction signal; blank gray means zero.
- Yellow description cells are common but not mandatory.
- Uncolored cells are excluded.
- No black annotation fill was found.
- Medium border evidence must be preserved; exact `thick` style is not mandatory.

### Still unresolved — do not mark Template approved

1. Owner approval of the complete rectangular bounds for all 17 candidate tables, including column bounds.
2. Owner approval of each green-marker partition and its exact column bounds.
3. Whether T08's secondary header at A297:D297 is an intentionally non-extractable descriptive block or requires a separate annotation change. Under the current workbook annotation it remains excluded.
4. Exact header/body/footer bounds where merged cells and split header groups occur.
5. Deterministic worksheet matching and coordinate-drift rules for later Parsian reports.
6. Validation against a second, later Parsian periodic workbook. No second workbook has yet been identified in the project context; the existing reports 1–3 are audits of the same sample workbook, not independent layout-drift evidence.

## 7. Next gate

The next required evidence is a second Parsian periodic XLSX from a later reporting period. It must be compared against this sample's candidate structure to measure row/column shifts, inserted/deleted sections, merged-header changes, and table/sub-table inventory changes. Until that comparison and owner bounds approval are complete, this document remains a draft evidence map, not a production Template.


## 8. Superseding structural evidence from report 3 — 2026-11-17

This section supplements and supersedes the earlier statements in sections 2, 5 and 6 where the 2026-11-17 audit was interpreted as finding zero black cells or as providing no complete rectangular bounds.

### 8.1 Provenance limitation

`parsian_periodic_report_3.md` is a direct OOXML audit of the earlier two-sheet package with SHA-256 `69186f1ad2b0e481a3588f2731b7027b0a9d9a543d1ca17fd24fc71d8c5aca06`. The corrected one-sheet workbook has SHA-256 `95f94e739632e48ae6552c562ecbf6c3e8182848718d17977f69bc984a6638b0`. The owner removed the temporary `Sheet1`; all findings from that sheet are excluded. The report-3 findings below concern `Recovered_Sheet1`, but the available evidence does not include a worksheet XML hash proving byte-level identity with the retained sheet in the corrected workbook. Treat these as detailed historical evidence requiring final confirmation where material.

### 8.2 Border-supported candidate bounds

Report 3 found continuous distinguishable outer edges on all four sides of each main-sheet candidate:

| ID | Red title | Evidence bounds | Border style |
|---|---|---|---|
| T01 | A8 | A10:D42 | medium |
| T02 | A58 | A60:D68 | medium |
| T03 | A77 | A79:C119 | medium |
| T04 | A128 | A130:L165 | medium |
| T05 | A174 | A176:D213 | medium |
| T06 | A236 | A238:I253 | medium |
| T07 | A264 | A266:C275 | medium |
| T08 | A277 | A279:B283 | medium |
| T09 | A300 | A302:C308 | medium |
| T10 | A311 | A313:D332 | medium |
| T11 | A334 | A336:C339 | medium |
| T12 | A351 | A353:I358 | medium |
| T13 | A359 | A361:C367 | medium |
| T14 | A374 | A376:C378 | medium |
| T15 | A384 | A386:C387 | medium |
| T16 | A393 | A395:C398 | thin |
| T17 | A403 | A404:E405 | thin |

All four edges were reported continuous, without gaps. The ordinary grid border is also `medium`, but has RGB `FFDDDDDD`; the candidate perimeter uses indexed 64. Therefore style name alone is insufficient to distinguish table boundaries.

These are evidence-supported sample bounds, **not yet owner-approved production Template bounds**. Blue headers and uncolored values occur outside several rectangles; they do not authorize automatic expansion or extraction.

### 8.3 Correction to black-fill inventory

Report 3's direct OOXML inspection found 492 black-filled cells on `Recovered_Sheet1`:
- 252 cells with theme 1, tint 0.05;
- 240 cells with theme 1, tint 0.

The newer annotation audit's `BLACK=0` result is incomplete because it did not classify these theme-based black fills. Withdraw the zero-black conclusion. Black-filled cells remain excluded under the owner's convention. T04 contains a fully black block `A131:L151` with 136 numeric values; confirm the intended exclusion of this whole block before final Template approval.

The 89 blank gray cells are distributed as 85 in T04 and 4 in T06. They remain extraction cells and map to numeric zero under the owner's rule.

### 8.4 Remaining structural review points

- T03 row 95: blue `A95:C95` inside the border and `D95` outside; role as secondary header/partition remains unresolved.
- T06 rows 243–244 and associated uncolored numeric cells remain excluded under the gray-only rule; confirm whether this is intentional.
- T13 row 364 contains uncolored cells between yellow rows; do not infer semantics.
- T02 has a few non-ordinary border sides extending outside its rectangle; confirm they are decorative/adjacent.
- Blue header columns and uncolored values outside the rectangles remain excluded unless the owner explicitly revises the annotation.
- T17 remains the owner-confirmed no-yellow exception.
- Green-marker partitions are provisional where they intersect unusual header/separator rows; notably T03 A81 through row 95 and T13 A362 through row 365.

Detailed analysis and all caveats are in `PARSIAN_PERIODIC_REPORT_3_STRUCTURAL_REVIEW.md`.

### 8.5 Current status

The 17 candidate bounds now have continuous border evidence in report 3, but Template approval is still blocked on owner confirmation, theme-fill audit coverage, and unresolved exceptions. Report 3 audits the same sample workbook, not a second reporting period; a genuinely separate Parsian periodic workbook is still required for layout-drift validation.


## 9. Owner clarifications — structural questions closed (2026-11-17)

This section records the owner's explicit decisions and supersedes the corresponding provisional questions in sections 5, 6, and 8.4.

- **T03 row 95:** B95 duplicates B79 and C95 duplicates C79. These repeated headers are redundant and are ignored; they are not a secondary header and do not create a structural partition. D95 is outside the T03 bounds `A79:C119` and is irrelevant.
- **T06 rows 243–244:** black-filled cells and uncolored cells inside the table are excluded from extraction. The same gray-only positive extraction rule applies throughout the table.
- **T13 row 364:** uncolored cells are excluded under the same rule; no semantic interpretation or special separator classification is needed.
- **T02 border extensions:** the red title cell is the table-identification signal. Border marks outside the candidate bounds do not expand the table. T02 remains `A60:D68`.
- **General extraction rule:** only gray-annotated cells are positive extraction targets. Black-filled and uncolored cells are excluded, including when they contain numeric values. A blank gray cell is different: it is an extraction target and maps to numeric zero.

The former owner-confirmation questions about T03 row 95, T06 rows 243–244, T13 row 364, and T02 border extensions are closed. These decisions do not by themselves approve all 17 table bounds or complete the separate-period layout-drift validation.


## 10. Consolidated coordinate draft for Company Table Layout Template — 2026-11-18

This section converts the report-3 evidence and owner clarifications into explicit A1-coordinate candidates. It is a normalized working draft, **not yet an owner-approved production Template**. All coordinates refer only to `Recovered_Sheet1`; the deleted test worksheet is excluded.

### 10.1 Top-level table candidates

| Table | Red title cell | Candidate table bounds | Header evidence | Status |
|---|---|---|---|---|
| T01 | A8 | `A10:D42` | `A10:D11` | Candidate |
| T02 | A58 | `A60:D68` | `A60:D61` | Candidate |
| T03 | A77 | `A79:C119` | `A79:C80`; ignore redundant `B95:C95` | Candidate |
| T04 | A128 | `A130:L165` | `A130:L130` | Candidate |
| T05 | A174 | `A176:D213` | `A176:D177` | Candidate |
| T06 | A236 | `A238:I253` | `A238:I239` | Candidate |
| T07 | A264 | `A266:C275` | `A266:C267` | Candidate |
| T08 | A277 | `A279:B283` | `A279:B279`; separate blue region `A297:D297` is not part of this table | Candidate |
| T09 | A300 | `A302:C308` | A302 and C302 are blue; B302 is not blue; D302 lies outside the candidate bounds | Candidate |
| T10 | A311 | `A313:D332` | `A313:D313` | Candidate |
| T11 | A334 | `A336:C339` | `A336:C336` | Candidate |
| T12 | A351 | `A353:I358` | `A353:I354` | Candidate |
| T13 | A359 | `A361:C367` | `A361:C361` | Candidate |
| T14 | A374 | `A376:C378` | `A376:C376` | Candidate |
| T15 | A384 | `A386:C387` | `A386:C386` | Candidate |
| T16 | A393 | `A395:C398` | `A395:C395` | Candidate |
| T17 | A403 | `A404:E405` | `A404:E404` | Candidate; owner-confirmed no-yellow exception |

The red title coordinate identifies the corresponding table section. The candidate rectangle is taken from report-3 structural evidence and is not expanded to include external borders, adjacent formatting, blue cells, or uncolored values. In particular, T02 remains `A60:D68`; its external border marks do not extend the table.

### 10.2 Green-marker sub-table coordinate candidates

The following exact A1 ranges are mechanically derived by combining each green-marker row interval with its parent candidate table's column span. The marker row is included as the sub-table's title row. These are candidate structural partitions; they do not imply that every cell in the rectangle is extractable.

| Parent | Green marker | Candidate sub-table bounds |
|---|---|---|
| T01 | A12 | `A12:D31` |
| T01 | A32 | `A32:D34` |
| T01 | A35 | `A35:D42` |
| T02 | A63 | `A63:D68` |
| T03 | A81 | `A81:C94` |
| T03 | A96 | `A96:C107` |
| T03 | A108 | `A108:C119` |
| T04 | A152 | `A152:L165` |
| T05 | A178 | `A178:D181` |
| T05 | A182 | `A182:D190` |
| T05 | A191 | `A191:D213` |
| T07 | A268 | `A268:C275` |
| T10 | A314 | `A314:D332` |
| T13 | A362 | `A362:C365` |
| T13 | A366 | `A366:C367` |

Sub-table columns are inherited from the parent table candidate. Green-marker partitions define structural ranges only. Extraction remains cell-based: gray cells are extracted; black and uncolored cells are excluded; blank gray cells become numeric zero. T03 row 95 is not part of any secondary header or sub-table partition; B95/C95 duplicate B79/C79 and are ignored, while D95 lies outside T03.

### 10.3 Explicit non-extraction and special cases

- Black-filled cells are excluded, including theme-based black fills. The earlier corrected-audit count of zero black cells is not authoritative; report 3 found theme-based black fills. No theme-fill re-audit is being performed in this step.
- Uncolored cells are excluded even when they contain numeric values, including T06 rows 243–244 and T13 row 364.
- Blank gray cells are extraction targets and map to numeric zero.
- T04 black-filled block `A131:L151` is excluded under the general black-cell rule.
- T08's blue region `A297:D297` and uncolored rows 298–299 do not create an additional table or extraction region.
- T09's B302 is not blue; its presence inside the candidate rectangle does not make it a header cell.
- T17 remains valid without a yellow description column.

### 10.4 Approval boundary

This coordinate draft resolves the four owner questions recorded in section 9 and provides explicit candidate A1 bounds for the 17 tables and 15 green-marker partitions. It does **not** silently convert historical report-3 evidence into owner approval. The next owner-review gate is to accept or correct the listed table rectangles and the mechanically derived sub-table ranges. Header/body/footer segmentation and deterministic matching of later workbooks remain separate design work. Theme-fill re-audit and second-period drift validation remain deferred as previously agreed.
