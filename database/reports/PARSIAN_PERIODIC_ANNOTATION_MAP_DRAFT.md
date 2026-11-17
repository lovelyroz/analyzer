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
