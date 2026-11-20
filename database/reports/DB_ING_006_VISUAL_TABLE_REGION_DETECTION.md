# DB-ING-006 — Conservative Visual Table-Region Detection

**Date:** 2026-11-15  
**Task:** 033  
**Status:** PARTIAL — implementation and owner-run automated tests passed; representative-workbook review remains pending.  
**Related:** DB-ING-004 / Task 031; DB-ING-005 / Task 032; DB-DES-007; DB-AUD-007; DB-AUD-008.

## 1. Scope and boundary

This increment adds a separate visual table-region candidate detector over the transient `WorkbookObservation` produced by the Excel source reader.

The detector is structural only. It does not:
- assign Metric, FinancialPeriod, Unit, currency, dimension, stock/flow, YTD, subtotal, total, forecast, or other financial meaning;
- classify a row as header/detail/total;
- normalize or parse source text;
- persist observations or alter ORM/schema/migrations;
- convert a candidate into a resolved table.

Declared Excel structured tables remain the only `RESOLVED` table structures. Visual regions are emitted as `CANDIDATE` or `AMBIGUOUS`.

## 2. Implementation

Files added/updated:
- `src/ingestion/excel/table_detector.py` — `detect_visual_table_candidates(observation)`.
- `src/ingestion/excel/__init__.py` — exports the detector.
- `src/tests/test_excel_table_detector.py` — owner-run tests.
- This report.

The function is pure with respect to its input: it returns a new immutable `WorkbookObservation`; source cells and the input observation are not mutated.

## 3. Conservative detection rules — version 1

1. Only populated literal-text cells participate in visual occupancy. Blank observations, including merged placeholders, are not treated as populated values.
2. A visual candidate must contain at least two occupied rows, at least two occupied columns, and at least three populated text cells. Single-row captions, notes, and labels are not promoted to tables.
3. A fully empty row or column is a segmentation signal. Occupied row/column bands are grouped deterministically; separate bands can produce multiple candidates in one worksheet.
4. A single blank row or column is a weak separator, not proof that two independent tables exist. Candidates adjacent to such a separator receive `AMBIGUOUS` status and `EXCEL_TABLE_SINGLE_BLANK_SEPARATOR`.
5. A merged range that crosses a proposed candidate boundary causes `AMBIGUOUS` status and `EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE`.
6. A nearby merged heading (up to two rows above a candidate, overlapping its columns) may be retained in `title_fragments` as source evidence. It does not expand the table bounds and is not asserted to be a caption.
7. Candidate bounds are the occupied text-cell extents. Row/column references preserve occupied indexes; no missing cell values are synthesized.
8. A visual candidate overlapping an already declared structured table is suppressed to avoid duplicate or conflicting structures.
9. Stable ordering follows worksheet order, then row/column position. Detection method/version are `conservative_blank_band_v1` / `1`.

## 4. Candidate status interpretation

| Status | Meaning | Downstream rule |
|---|---|---|
| `CANDIDATE` | Structural evidence meets the conservative minimum and no known boundary ambiguity was detected | Still requires later table/header interpretation; never treated as semantically resolved |
| `AMBIGUOUS` | A weak one-cell-wide separator or a merged range makes the proposed boundary uncertain | Must not be silently promoted; requires stronger evidence or review |
| `RESOLVED` | Reserved for explicit structured Excel tables currently observed by the reader | No visual detector output is marked resolved |

The detector intentionally does not emit `UNSUPPORTED` in this increment; unsupported workbook constructs remain the reader/contract layer's responsibility.

## 5. Owner-run tests authored

`src/tests/test_excel_table_detector.py` covers:
- two vertically separated candidate regions;
- side-by-side regions separated by an empty column;
- nearby merged caption evidence without expanding bounds;
- a merged range crossing a proposed boundary;
- rejection of single-row captions/notes as table candidates;
- repeatability and input immutability;
- a stronger separator consisting of two blank rows.

Owner-run validation result: `33 passed in 1.47s` for the combined DTO, reader, and detector suite. The assistant did not run tests. Owner command:

```powershell
pytest src/tests/test_excel_observation_dto.py src/tests/test_excel_source_reader.py src/tests/test_excel_table_detector.py -q
```

## 6. Known limitations and validation required

- Blank-band segmentation is a deliberately narrow first-pass heuristic. A genuinely blank row/column inside one logical table may split it; a one-cell gap is therefore marked ambiguous, but multiple blank rows/columns are treated as stronger separators. Real workbooks must validate whether this is sufficiently conservative.
- Tables with fewer than two occupied rows or columns, or fewer than three populated text cells, are not emitted as candidates. This avoids promoting captions/notes but can miss very small legitimate tables.
- Sparse regions whose internal empty rows/columns resemble separators can be fragmented; the current detector does not attempt to infer continuity from formatting, borders, styles, formulas, or numeric patterns.
- Merged title evidence is captured only for nearby merged headings overlapping the candidate columns. Unmerged captions and more distant contextual notes are not attached in V1.
- No real XLSX workbook was inspected by the assistant. The owner must validate the candidate bounds/statuses against the source workbooks and Markdown audits before treating the heuristic as accepted for production ingestion.

## 7. Acceptance status

Implementation and test definitions are present. Task 033 remains PARTIAL until:
1. **DONE:** the owner-run combined test command passed (`33 passed in 1.47s`);
2. the owner checks the output against representative real source workbooks, including multiple tables, captions, merged headers, sparse layouts, and blank gaps;
3. any false split, missed table, or wrongly certain boundary is corrected or explicitly documented as a V1 limitation.

Tests were run by the owner only; the assistant did not run tests. No ORM, schema, migration, database data, or dependency was changed.


## 8. Markdown-evidence review and owner-run source validation utility

A focused review was performed against the existing Markdown evidence only:
- `reports/DB-AUD-002_REAL_EXCEL_TEMPORAL_AUDIT.md` (cheshme, fzar, fzar2, samanBank);
- `reports/parsian_periodic_report_1.md` (Parsian periodic workbook).

No XLSX file was opened by the assistant. The review supports the reader's need to preserve one worksheet as a collection of independent local regions, but it also exposes a material limitation in the current detector's blank-band-only segmentation.

### 8.1 Findings from documented table ranges

- The five reports describe many independent tables in each single worksheet, with merged headers and different local column layouts. This supports retaining worksheet coordinates and merged-range evidence and keeping table detection separate from financial interpretation.
- In the Parsian report, several independent table ranges are directly adjacent by row: customer deposits `A263:F276` and off-balance items `A277:F283`; employee/branch status `A295:D299` and agency-fee/capital-adequacy `A300:D308`; strategy/facility income `A309:F333` and investment profit/loss `A334:D341`; investee disclosure `A345:J358` and other operating income/expenses `A359:C372`; profit-distribution plan `A403:E405` and other significant plans `A406:B407`.
- The current detector joins all contiguous occupied rows into one row band. Therefore, where adjacent independent tables have no fully empty row between them, the current algorithm cannot separate them using its present row segmentation. This is a known likely false-merge mode, not a verified detector output on the XLSX.
- The Fzar report documents several independent blocks separated by only one blank row (for example production/sales `A10:Z31`, purchases `A33:T41`, energy `A43:X48`, and currency resources `A50:W57`). The detector should conservatively mark the resulting boundaries ambiguous, as designed; actual candidate bounds/statuses still need owner-run confirmation.
- The Parsian report also documents boundaries with a single blank row, as well as boundaries with larger blank gaps. This provides useful positive and ambiguous-boundary cases for the source validation run.
- Adjacent merged title rows, unmerged titles, and sparse side-by-side layouts may require additional structural evidence. The current report evidence is not sufficient to determine the exact candidate output or safely design a generalized split rule.

### 8.2 Next validation step

Added `src/scripts/excel_table_detector_review.py`, a read-only owner-run utility. It invokes the production reader and detector for each supplied workbook and prints a compact Markdown inventory of candidate bounds, status, title evidence, diagnostics, source fingerprint, and reader result. It does not alter workbooks or persist observations.

Owner command from the repository root:

```powershell
python src/scripts/excel_table_detector_review.py excel/cheshme.xlsx excel/fzar.xlsx excel/fzar2.xlsx excel/samanBank.xlsx excel/parsian_periodic.xlsx
```

Paste the complete Markdown output into `reply.md`. If the real source files are stored under different paths, pass their actual paths instead. A reader rejection or missing file must be retained in the output rather than silently omitted.

### 8.3 Acceptance status

The Markdown review is complete, but it is not a substitute for running the detector on source workbook bytes. Task 033 remains PARTIAL. The next implementation decision must be based on the owner-run candidate output, with particular attention to:
1. adjacent independent tables that the current row-band algorithm may merge;
2. one-blank-row boundaries that should remain explicitly ambiguous;
3. merged and unmerged titles and multi-level headers;
4. side-by-side tables and sparse regions;
5. accidental splitting of a single logical table.

No tests or XLSX inspection were performed by the assistant. No ORM, schema, migration, database data, or dependency was changed.


### 8.4 Reader contract violations observed during owner validation attempt

The owner reported that the initial utility output was dominated by repeated `EXCEL_TEXT_ONLY_NON_TEXT_CELL` diagnostics. This means the Reader rejected the workbooks before the original utility could print detector candidates. It does **not** indicate a table-detector failure; it indicates that the actual cell storage types in at least some source workbooks differ from the confirmed V1 text-only contract.

The review utility was updated to keep the evidence useful without weakening ingestion rules:
- summarize the total number of contract-violating cells, counts by worksheet, and counts by cell kind / Excel data type;
- print only a bounded sample of offending coordinates (default 12 per workbook), including data type, number format, and a shortened observed value;
- run the detector over literal-text observations in the rejected workbook as a clearly labelled **DIAGNOSTIC PREVIEW ONLY**;
- continue to mark the Reader result as REJECTED. This preview must never be interpreted as admission or permission to ingest a contract-invalid workbook.

Updated utility: `src/scripts/excel_table_detector_review.py`.

Owner command (same workbook paths; compact output):

```powershell
python src/scripts/excel_table_detector_review.py excel/cheshme.xlsx excel/fzar.xlsx excel/fzar2.xlsx excel/samanBank.xlsx excel/parsian_periodic.xlsx
```

If more examples are needed, increase the sample limit with `--sample-limit 30`. Paste the compact output into `reply.md`.

**Important decision gate:** do not relax the text-only contract and do not coerce numbers/dates into strings. First inspect the reported coordinates and determine whether these are genuinely numeric/date/formula cells or whether the source-generation/export process has changed. If they are genuine non-text populated cells, the owner must explicitly revise the input contract before any Reader behavior is changed. Task 033 remains PARTIAL, and Reader contract alignment is now a separate issue to resolve before production acceptance.


### 8.5 Owner-run validation results — 2026-11-15

The owner reran the review utility against all five representative workbooks and supplied the complete output in repository `reply.md`.

**Reader contract outcome:** all five workbooks were rejected. Every reported violation is `UNEXPECTED_NON_TEXT` with Excel `data_type='n'`; no formula or error-cell violations were reported in this run.

| Workbook | Observed cells | Numeric-type contract violations |
|---|---:|---:|
| `cheshme.xlsx` | 2,153 | 928 |
| `fzar.xlsx` | 953 | 384 |
| `fzar2.xlsx` | 6,063 | 2,036 |
| `samanBank.xlsx` | 2,753 | 914 |
| `parsian_periodic.xlsx` | 2,183 | 920 |
| **Total** | **14,105** | **5,182** |

The samples include ordinary positive, negative, and zero numeric values with number formats such as `[$-3000401]#,##0` and `[$-3000401]0`. This is evidence of literal numeric-typed Excel cells, not evidence that those cells contain formulas. It conflicts with the currently approved *text-typed cell* input contract. The distinction must be resolved explicitly by the owner; the reader must not stringify or otherwise coerce these values under the current contract.

**Diagnostic-preview outcome:** because the reader rejected each workbook, all detector output below is diagnostic-only and is based on the literal-text subset, not the complete worksheet contents.

| Workbook | Preview regions | CANDIDATE | AMBIGUOUS |
|---|---:|---:|---:|
| `cheshme.xlsx` | 9 | 0 | 9 |
| `fzar.xlsx` | 4 | 0 | 4 |
| `fzar2.xlsx` | 33 | 0 | 33 |
| `samanBank.xlsx` | 16 | 2 | 14 |
| `parsian_periodic.xlsx` | 15 | 1 | 14 |
| **Total** | **77** | **3** | **74** |

Most preview regions are ambiguous because of single-blank separators and/or merged ranges crossing proposed boundaries. These counts do not validate the detector against the complete numeric-containing workbooks. In addition, the previously documented adjacent-table false-merge risk remains unresolved: a text-only preview cannot establish whether the detector correctly separates all independent financial tables.

**Decision gate / next action:**

1. The owner must clarify whether the normative source contract means (A) every populated cell must have Excel string type, or (B) populated cells may be literal text *or literal numeric values*, while formulas remain prohibited.
2. If (A), the five current source workbooks are invalid under the approved contract and must be regenerated/exported as text-typed workbooks upstream; Reader behavior remains unchanged.
3. If (B), this is an explicit contract revision. Before changing the Reader, define the exact numeric observation representation, precision/round-trip guarantees, treatment of dates and booleans, and whether preserving the numeric value exposed by openpyxl is sufficient. Do not silently stringify numbers or infer numeric semantics at the reader layer.
4. After the contract is settled and a valid full observation is available, revisit table segmentation against the real workbooks. Do not treat the present diagnostic preview as acceptance evidence.

Task 033 remains PARTIAL. The automated test result remains owner-reported as 33 passed; the real-workbook validation is not complete. The assistant did not inspect XLSX files or run tests.


### 8.6 Owner clarification supersedes the earlier text-only interpretation — 2026-11-15

The owner clarified that "text" in the earlier decision meant direct literal cell content (which may be numbers, alphabetic text, and permitted characters), not Excel's string storage type. The original intent was **no formulas**, not "all cells must have Excel data_type='s'". The prior conclusion that the 5,182 numeric-typed cells violated the owner's contract was incorrect and is withdrawn.

The owner-run counts in Section 8.5 remain factual evidence of the five workbook cell types, but they are not contract violations. The 5,182 cells are numeric literals and should be accepted by the Reader. The 77-region diagnostic previews in Section 8.5 are superseded and must not be used for table-detector acceptance because they excluded numeric cells.

Corrective implementation now in progress:
- DTO adds `PRESENT_NUMBER` and `numeric_value` for literal numeric cells.
- Reader accepts native numeric int/float cells without stringification or parsing; formulas remain rejected.
- Visual detector counts both `PRESENT_TEXT` and `PRESENT_NUMBER` for occupancy; merged title fragments remain text-only.
- Boolean/date-typed and Excel error cells remain unsupported pending explicit scope confirmation if encountered.

The owner must rerun the updated review utility on all five source workbooks. The expected outcome is that ordinary numeric cells no longer reject the workbook; any remaining rejection must identify the actual unsupported cell kind (for example formula, Boolean, date-typed, or Excel error). Once the reader accepts a workbook, its full detector output—not the old text-only preview—can be reviewed against the workbook evidence. Task 033 remains PARTIAL until that full validation and any required detector corrections are complete. The assistant did not inspect XLSX files or run tests.


### 8.7 Owner-run validation after literal numeric support — 2026-11-15

The owner reran the combined test suite after the DTO/Reader/Detector correction:

```text
pytest src/tests/test_excel_observation_dto.py src/tests/test_excel_source_reader.py src/tests/test_excel_table_detector.py -q
36 passed in 3.01s
```

The owner then ran `src/scripts/excel_table_detector_review.py` against all five representative workbooks. The Reader accepted every workbook:

| Workbook | Reader | Worksheets | Observed cells | Preview regions |
|---|---:|---:|---:|---:|
| cheshmeh.xlsx | ACCEPTED | 1 | 2,153 | 16 |
| fzar.xlsx | ACCEPTED | 1 | 953 | 5 |
| fzar2.xlsx | ACCEPTED | 1 | 6,063 | 36 |
| samanBank.xlsx | ACCEPTED | 1 | 2,753 | 19 |
| parsian_periodic.xlsx | ACCEPTED | 2 | 2,183 | 18 |

Across 94 preview regions, only 3 were `CANDIDATE`; 91 were `AMBIGUOUS`. Ambiguity is primarily caused by merged ranges crossing proposed bounds and single-blank-row/column separators. The results confirm that the current detector is highly conservative, but not yet operationally useful for identifying independent financial tables.

Most importantly, the Parsian output contains broad merged regions in worksheet 1, including `A294:F341`, `A350:J363`, and `A365:C367` through `A403:E407`. Earlier Markdown evidence identifies independent adjacent tables inside some of these broad areas (for example the employee/branch-status and agency-fee/capital-adequacy tables, and the strategy/facility-income and investment-profit/loss tables). Therefore the present blank-band segmentation cannot reliably separate adjacent tables without a stronger boundary signal. This is an observed mismatch between the candidate output and documented workbook structure; it is not evidence that the XLSX itself was directly inspected by the assistant.

**Disposition:** DTO and Reader validation are complete. DB-ING-006 remains `PARTIAL`. Do not treat `AMBIGUOUS` regions as accepted table bounds or proceed to semantic extraction from them. The next detector increment must investigate structural signals beyond blank bands (for example cell styles/borders, merged-range topology, repeated header geometry, and row/column density transitions), define deterministic evidence thresholds, and add regression fixtures for adjacent tables, merged headings, sparse layouts, and true single-table regions. Any style/border signal must remain structural evidence only; it must not infer financial meaning. The assistant did not run tests or directly inspect XLSX files.


### 8.8 Structural-formatting evidence collection for detector V2 — 2026-11-15

The V1 owner-run output confirms that blank-band segmentation alone cannot separate some adjacent independent tables. The next increment is therefore an evidence-collection step, not an unvalidated automatic split rule.

**Observation contract extension:** CellObservation now optionally preserves:
- workbook-local style_id;
- top, bottom, left, and right border style names;
- fill pattern type;
- bold-font flag.

The Reader captures these attributes for observed populated cells and styled blank cells. These fields are structural formatting evidence only. They do not assign header, detail, subtotal, metric, period, unit, or any other financial meaning. Literal cell values remain untouched. The DTO additions are optional and do not change the literal-value acceptance contract.

**New owner-run audit utility:** src/scripts/excel_table_boundary_audit.py. It reports row-level literal occupancy and formatting signatures, plus transitions between consecutive populated/styled rows. It includes column-set similarity, style-ID similarity, matching bottom/top border columns, and border locations. Styled blank cells are included in border/style evidence, but they do not count as occupied literal values. The utility is read-only and does not split regions or promote any boundary to a table boundary.

Run the combined regression suite:

```powershell
pytest src/tests/test_excel_observation_dto.py src/tests/test_excel_source_reader.py src/tests/test_excel_table_detector.py -q
```

Then run the structural audit:

```powershell
python src/scripts/excel_table_boundary_audit.py --limit-per-sheet 100 excel/cheshme.xlsx excel/fzar.xlsx excel/fzar2.xlsx excel/samanBank.xlsx excel/parsian_periodic.xlsx
```

Paste the complete output into reply.md.

**V2 design gate:** do not split tables merely because style_id, font, fill, or border changes. Style IDs are workbook-local and may differ because of number formats or presentation choices. The next detector design must evaluate combinations of independent evidence, establish deterministic thresholds against actual source files, and keep uncertain boundaries AMBIGUOUS. In particular, investigate the documented Parsian adjacent pairs around rows 295/300, 309/334, 358/359, and 405/406. A formatting boundary is a structural signal, not proof by itself that two financial tables are independent.

Task 033 remains PARTIAL. No table segmentation behavior was changed in this increment. The assistant did not run tests or inspect the XLSX workbooks directly.


### 8.9 Owner-run validation and Reader formatting-evidence fix — 2026-11-15

The owner ran the combined regression command and reported **37 passed, 1 failed**. The single failure was `test_reader_captures_cell_border_fill_font_and_style_evidence`: the fixture defined only a bottom border, while openpyxl exposes an unset border side as `None`; the Reader incorrectly dereferenced `.style` on that absent side and wrapped the resulting AttributeError as `EXCEL_WORKBOOK_STRUCTURE_UNREADABLE`.

The Reader was corrected to read each border side defensively, returning `None` when that side is absent. This preserves the intended optional formatting-evidence contract and does not change cell-value acceptance, table detection, or financial semantics. The fix is committed in `src/ingestion/excel/reader.py` (commit `7a67f02b77cc5ba9b79c8681257a8cdd5ba9dd01`).

**Required owner action:** rerun the same combined regression command. The structural boundary audit output was not present in this `reply.md` result, so after the tests pass, run the audit command from section 8.8 and place its complete output in `reply.md`. Task 033 remains PARTIAL. The assistant did not run tests or inspect XLSX files directly.



### 8.10 Targeted source-cell audit for documented adjacent-table boundaries — 2026-11-15

The owner supplied the complete transcript of `excel_table_boundary_audit.py` in `reply.md`. The transcript confirms that the Reader accepted all five workbooks and that the Parsian workbook has two worksheets. The broad formatting report is not sufficient to decide the documented table boundaries: many consecutive Parsian rows carry the same `medium` border pattern across their occupied columns, and the style profiles repeat extensively. In particular, border presence and workbook-local style IDs do not distinguish the suspected adjacent tables reliably.

To obtain the missing evidence without asking the owner to copy large XLSX regions manually, a narrow read-only utility was added:

`src/scripts/excel_table_targeted_row_audit.py`

It reads the workbook through the existing Excel Reader and prints literal cell coordinates/values plus merged-range topology for selected row windows. It does not classify headers, infer financial semantics, split tables, or modify the source workbook. Its default windows cover the documented Parsian boundaries with nearby context:

- rows 292–302 (the adjacent table pair around 295/300);
- rows 306–337 (the adjacent table pair around 309/334);
- rows 355–362 (the suspected boundary around 358/359);
- rows 402–409 (the suspected boundary around 405/406).

**Owner-run command** (from the repository root):

```powershell
python src/scripts/excel_table_targeted_row_audit.py excel/parsian_periodic.xlsx
```

For a complete transcript in PowerShell:

```powershell
Start-Transcript -Path "D:\\Winprojects\\analyzer\\targeted_row_audit.txt" -Force
python src/scripts/excel_table_targeted_row_audit.py excel/parsian_periodic.xlsx
Stop-Transcript
```

Place the resulting `targeted_row_audit.txt` content in `reply.md`. If the first worksheet is not the intended source sheet, the utility supports `--sheet-ordinal 2`; row windows can be overridden with `--ranges "START:END,START:END"`.

**Current disposition:** this is evidence collection only. No V2 split rule or threshold has been adopted. Task 033 remains PARTIAL until the actual cell content/merged topology is reviewed and any detector change is supported by regression tests and owner-run validation. The assistant did not run tests or inspect the XLSX workbook directly.


### 8.11 Targeted content and merged-range review — 2026-11-15

The owner supplied the complete output of `src/scripts/excel_table_targeted_row_audit.py` in `reply.md` for Parsian worksheet 1 (`Recovered_Sheet1`). The audit reports workbook cells through the Reader; the assistant did not open the XLSX directly.

The observed rows support the following boundaries and internal structure:

| Rows | Observed structure | Finding |
|---|---|---|
| 295–300 | Row 295 is a one-cell section title; rows 297–299 form a four-column employee/branch table; row 300 is a new one-cell title, followed by a unit note and a four-cell header on row 302. | Two adjacent tables are supported. |
| 309–334 | Row 309 is a section heading; row 310 contains a merged heading/line; row 311 is the facility-income table title; row 312 is a unit note; row 313 is a six-column all-text header followed by data rows 314–332. Row 334 starts another titled table, with a unit note on 335 and a four-cell header on 336. | The broad region contains multiple structural sections and at least two separate tabular blocks. Row 314 is a one-cell subsection label inside the first table, so a one-cell-row split rule would be unsafe. |
| 358–359 | Rows 355–358 are populated investment rows; row 359 is a one-cell title, followed by a unit note and a three-cell all-text header on row 361. | A new table begins after row 358. |
| 405–406 | Row 405 contains five numeric values; row 406 is a one-cell section title, followed by a period/description row and a blank row. | A section boundary is visible, but this excerpt does not establish a following table start. |

**Important structural distinction:** one-cell text rows occur both as table/section titles (for example rows 300, 311, 334 and 359) and as in-table subsection labels (row 314). Therefore, neither one-cell occupancy nor merged-range presence is a sufficient split criterion. A potentially useful *candidate pattern* is a title-like single-cell row followed by an optional one-cell note and then a multi-cell all-text row, but it is not yet an approved rule. The same pattern must be checked against counterexamples and the other representative workbooks before implementation. The detector must not infer financial meaning from Persian label text.

**Next action:** run the new read-only cross-workbook audit:

```powershell
python src/scripts/excel_table_row_pattern_audit.py excel/cheshme.xlsx excel/fzar.xlsx excel/fzar2.xlsx excel/samanBank.xlsx excel/parsian_periodic.xlsx
```

The utility `src/scripts/excel_table_row_pattern_audit.py` enumerates single-cell literal-text rows in each worksheet and prints nearby populated rows, row occupancy/value-kind counts, literal values, and merged-range geometry. It labels structural patterns only (for example single-text → optional single-text note → multi-cell all-text row, or single-text → mixed row). It performs no table splitting and does not infer financial meaning. The default limit is 100 contexts per worksheet; increase it with `--max-per-sheet` if the output reports omitted contexts. Put the complete output in `reply.md`.

Use the result to test the proposed pattern across all five workbooks and identify false positives such as Parsian row 314. No detector behavior is changed in this increment.

Task 033 remains PARTIAL. Do not promote AMBIGUOUS regions or feed them to semantic extraction. The assistant did not run tests or inspect XLSX files directly.


### 8.12 Cross-workbook row-pattern audit review and correction — 2026-11-15

The owner-run output was supplied in `reply.md`. It covers all five representative workbooks. The first version of `excel_table_row_pattern_audit.py` selected the next populated rows, not the next physical worksheet rows. Consequently, rows separated by blank rows could be presented as if they formed a nearby sequence. Its pattern labels/counts are **not valid evidence of physical adjacency** and must not be used to approve a split rule.

The output nevertheless illustrates why a generic single-cell-row rule is unsafe:
- Cheshmeh and Fzar2 contain one-cell labels that are followed by mixed text/numeric data rows, consistent with in-table section labels as well as possible section boundaries.
- Fzar, Saman and Parsian show examples of a title row, a one-cell unit note and a multi-cell text header. These are useful examples, not proof that the pattern is universal.
- Several one-cell rows are explanatory notes, repeated report titles, narrative disclosures, subsection labels or merged explanatory text. A row's one-cell occupancy alone cannot distinguish these roles.
- Parsian worksheet 2 contains many one-cell text rows in a compact financial-statement layout; this is additional counterexample material, not a basis for treating every such row as a table boundary.

**Audit utility correction:** the script was revised to inspect the next three *physical* worksheet rows after each anchor, explicitly print empty rows, report merged ranges on each physical row, and classify only direct-next-row / next-row-note / one-blank-row structural patterns. The earlier audit output is superseded for adjacency analysis.

Owner-run the corrected version with the same command:

```powershell
Start-Transcript -Path "D:\\Winprojects\\analyzer\\row_pattern_audit_v2.txt" -Force
python src/scripts/excel_table_row_pattern_audit.py excel/cheshme.xlsx excel/fzar.xlsx excel/fzar2.xlsx excel/samanBank.xlsx excel/parsian_periodic.xlsx
Stop-Transcript
```

Place the complete `row_pattern_audit_v2.txt` output in `reply.md`. The corrected audit remains diagnostic only; it does not split tables, assign financial meaning, or change the Detector. Task 033 remains PARTIAL. The assistant did not run tests or inspect XLSX files directly.


### 8.13 Corrected physical-row pattern audit across five workbooks — 2026-11-15

The owner supplied the corrected-version transcript in `reply.md` (blob SHA `2ef381fc9c60b5c237cafb72e5708ed5987b6c5d`). This version inspects physical worksheet rows, prints empty rows explicitly, and reports merged-range geometry on each row. The assistant reviewed the Markdown transcript only; it did not open the XLSX files directly.

The output contains the following single-text-row anchor classifications:

| Workbook | No match in next 2 physical rows | Direct next row all-text | Direct next row mixed | Single-text note, then all-text row |
|---|---:|---:|---:|---:|
| cheshmeh.xlsx | 19 | 9 | 5 | 0 |
| fzar.xlsx | 12 | 4 | 1 | 1 |
| fzar2.xlsx | 40 | 18 | 33 | 9 |
| samanBank.xlsx | 26 | 27 | 17 | 15 |
| parsian_periodic.xlsx | 35 | 28 | 18 | 18 |

**Coverage caveat:** the Fzar2 worksheet reports 162 single-text rows, while the utility's default maximum is 100 contexts per worksheet. Its 100 printed contexts are therefore not a complete audit of all 162 anchors. The other listed worksheets have no more than 100 single-text rows. Counts above are audit-pattern counts, not counts of confirmed table boundaries.

The audit confirms useful but non-conclusive structural signatures:

- The sequence *single-cell title → single-cell unit note → multi-cell all-text row* appears in Fzar, Fzar2, Saman and Parsian. Examples include Fzar rows 8–10, Fzar2 rows 334–336 and 361–363, Saman rows 9–11 and 37–39, and Parsian rows 8–10 and 58–60. These are strong **table-start candidates**, but the audit does not establish a universal rule or prove that every such sequence is an independent table.
- A single-cell text row followed immediately by a mixed row appears in all five workbooks. Many such rows are in-table section/subsection labels rather than table boundaries. Examples include Cheshmeh rows 11–12 and 162–163, Fzar rows 12–13, Fzar2 rows 11–12 and 26–27, Saman rows 41–42 and 86–87, and Parsian rows 12–13, 32–33 and 35–36. Parsian row 314, previously identified by the targeted audit, is a further in-table subsection-label counterexample.
- A direct all-text successor is not by itself decisive: it can be a multi-row table header, a unit note preceding a header, or other structural text. Merged ranges provide useful topology but do not independently establish table identity.
- The corrected audit did not identify a one-blank-row-then-all-text pattern among the emitted classifications. This does not prove that blank rows are never relevant; it only means this particular pattern was not demonstrated by these anchor contexts.

**Decision:** no generic V2 split rule is approved from this evidence. In particular, do not split on single-cell occupancy, a direct all-text successor, or a single-text-note/all-text sequence alone. The title → optional unit note → all-text header sequence may be retained as a *candidate signal* for a future multi-signal classifier, not as an automatic split or promotion rule. The current Detector must continue to return AMBIGUOUS where it cannot establish boundaries safely; no AMBIGUOUS region may enter semantic extraction.

**Next technical step:** inspect and model the *header structure itself* as a distinct structural signal, including multi-row headers, merged-cell coverage, populated-column footprint, and the transition from header rows to subsequent data rows. Any proposed combination must be evaluated against the in-table subsection-label examples above and the incomplete Fzar2 coverage. Do not use Persian label meaning or financial semantics in this structural phase. Before implementation, obtain complete Fzar2 anchor coverage (for example, rerun with `--max-per-sheet 200`) and define exact positive/negative regression fixtures from the owner-provided evidence.

Task 033 remains PARTIAL. The owner has not yet rerun tests for a new Detector implementation because no implementation change is made in this increment. The assistant did not run tests or inspect XLSX files directly.



### 8.14 Completion of Fzar2 coverage and Cheshmeh follow-up — 2026-11-15

The owner supplied a full Fzar2-only run of the corrected physical-row audit with `--max-per-sheet 200`, then a separate Cheshmeh-only run. The assistant reviewed the Markdown transcripts in the conversation; it did not inspect XLSX files directly.

The Fzar2 worksheet contains 162 single-cell literal-text anchors. The full 200-context run classified them as follows:

| Pattern | Count |
|---|---:|
| No match in next 2 physical rows | 75 |
| Direct next row all-text | 34 |
| Direct next row mixed | 33 |
| Single-text note, then all-text row | 20 |
| **Total** | **162** |

The separate Cheshmeh run was complete (33 anchors): 19 no-match, 9 direct-all-text, 5 direct-mixed, and 0 note-then-all-text. Its observed examples reinforce that all-text rows can be multi-level headers (e.g. rows 9–10, 44–45, 107–109, 160–161, 194–196), while one-cell rows followed by mixed rows can be in-table section labels (e.g. rows 11–12 and 162–163). The Cheshmeh output contains no demonstrated one-blank-row-then-all-text case.

This closes the previously noted Fzar2 coverage gap. The earlier five-workbook aggregate table in section 8.13 remains a snapshot of the 100-context run and should not be used as the complete Fzar2 counts. The completed Fzar2 counts above supersede that partial Fzar2 row for any further aggregate analysis.

**Decision unchanged:** no generic split rule is supported. A multi-cell all-text row is a useful header-structure candidate, not proof of a table boundary. Adjacent all-text rows may form a multi-level header, and merged ranges may span several header rows. One-cell section labels can occur within existing data tables.

### 8.15 Header-band structural audit utility — 2026-11-15

Added read-only utility `src/scripts/excel_table_header_band_audit.py`. It groups physically adjacent rows containing at least two populated literal-text cells and no numeric/other populated cells, then prints:
- the complete physical row band;
- configurable physical context before and after the band, including explicit empty rows;
- populated column footprints;
- literal cell values and merged-range geometry.

It does not call these bands confirmed headers, infer financial meaning, split regions, mutate workbooks, or alter Detector output. The purpose is to inspect multi-row header topology and the transition from text-only header-like rows to mixed data rows, including cases where the title row is not a single-cell anchor.

Owner-run command:

```powershell
Start-Transcript -Path "D:\\Winprojects\\analyzer\\header_band_audit.txt" -Force
python src/scripts/excel_table_header_band_audit.py --max-bands 200 excel/cheshme.xlsx excel/fzar.xlsx excel/fzar2.xlsx excel/samanBank.xlsx excel/parsian_periodic.xlsx
Stop-Transcript
```

Place the complete transcript in `reply.md`. Review must identify positive header-band examples and counterexamples (narrative/all-text rows, notes, and in-table section labels) before any Detector rule or regression fixture is approved.

Task 033 remains PARTIAL. No tests were run by the assistant, and XLSX files were not directly inspected.


### 8.16 Review of owner-run header-band audit across five workbooks — 2026-11-15

The owner supplied the complete transcript in `reply.md` (current blob SHA `f68528aa775f99e1641715bc281b43ae31b3f9ff`). The assistant reviewed the Markdown transcript only; it did not open the XLSX files directly.

All five workbooks were accepted by the Reader. The audit covered six worksheets and reported 113 adjacent all-text bands in total:

| Workbook | Worksheet coverage | Adjacent all-text bands |
|---|---:|---:|
| cheshmeh.xlsx | 1 | 10 |
| fzar.xlsx | 1 | 4 |
| fzar2.xlsx | 1 | 37 |
| samanBank.xlsx | 1 | 32 |
| parsian_periodic.xlsx | 2 | 30 |
| **Total** | **6** | **113** |

**Positive header evidence:** the audit exposes genuine multi-row header structures, including Cheshmeh rows 9–10, 44–45, 107–109, 160–161 and 194–196; Fzar rows 10–11, 33–34 and 43–44; Fzar2 rows 9–10, 60–61 and 92–93; Saman rows 11–12 and 39–40; and Parsian rows 10–11, 60–61, 79–80, 176–177 and 238–239. These examples show that merged-cell geometry and column footprints can encode hierarchical headers, and that a valid header may span one, two or more physical rows.

**Counterexamples and limitations:**
- The band predicate is not a header classifier. In Saman, bands such as rows 29, 32 and 35 contain management forecasts/narrative text, not column headers. Similar explanatory/narrative bands appear elsewhere.
- One-cell section labels and subsection labels remain present around otherwise valid tables. For example, Saman row 86 is an in-table subsection label after the header at row 85; Parsian row 314 was previously confirmed as an in-table subsection label.
- A multi-cell all-text band can be a narrative/description row, not a table header. Conversely, a header may be one row high, or be followed by additional mixed/numeric content within a shared report region.
- The audit's grouping rule requires at least two literal-text cells and excludes numeric/other populated cells. Therefore it deliberately does not capture every possible header form, especially headers interleaved with numeric/text mixed content. The 113 count is a count of detected bands, not a count of tables or confirmed headers.
- Merged ranges and populated-column footprints are useful structural evidence, but no single one of them establishes a table boundary. The audit does not provide a universal transition signature that separates table headers from narrative bands and in-table labels.

**Decision:** the header-band audit improves the evidence base but does not support a deterministic, generic table-splitting rule. Do not split or promote a region solely because it contains a multi-cell all-text band, adjacent all-text rows, merged ranges, or a particular column footprint. Do not pass AMBIGUOUS regions to semantic extraction. No Detector implementation or regression fixtures are approved from this audit alone.

**Next technical step:** move from row-pattern heuristics to an explicit structural model of a *table candidate*: header-band candidate(s), merged-range coverage, column-footprint continuity, and the transition into subsequent populated rows. The model must permit single-row and multi-row headers, while retaining narrative bands and in-table subsection labels as negative cases. Before implementing it, define a small set of exact positive and negative regression fixtures from the owner-provided transcript and establish how each fixture maps to observed coordinates/regions. If the available observations cannot distinguish a boundary deterministically, preserve AMBIGUOUS rather than guessing.

Task 033 remains PARTIAL. No tests were run by the assistant, no XLSX files were directly inspected, and no Detector behavior was changed in this increment.

### 8.17 Header-to-body column-continuity audit utility — 2026-11-15

Added read-only utility `src/scripts/excel_table_header_transition_audit.py` to measure structural continuity from every detected all-text band into the following physical rows.

For each band, the utility reports:
- the union of populated columns across the band and the per-row column footprints;
- each subsequent physical row (default lookahead: six rows), including explicit empty rows;
- populated text/number/other counts and the row's populated columns;
- intersection count and Jaccard similarity between each following row's populated columns and the band's column union;
- merged ranges touching the band/lookahead rows and merged ranges crossing the final band row into subsequent rows;
- literal values and cell coordinates for owner review.

The Jaccard value is descriptive evidence only. A high or low value is not interpreted as a header/body decision, a table boundary, or a split threshold. The utility deliberately does not classify headers, assign financial meaning, split candidates, mutate workbooks, or change Detector behavior.

Owner-run command (from repository root):

```powershell
Start-Transcript -Path "D:\\Winprojects\\analyzer\\header_transition_audit.txt" -Force
python src/scripts/excel_table_header_transition_audit.py --max-bands 200 --lookahead-rows 6 excel/cheshme.xlsx excel/fzar.xlsx excel/fzar2.xlsx excel/samanBank.xlsx excel/parsian_periodic.xlsx
Stop-Transcript
```

Place the complete transcript in `reply.md`. Preserve the full output; it is needed to compare positive header/body transitions against narrative bands, unit notes, in-table subsection labels, and adjacent-table boundaries. Do not reduce the evidence to aggregate Jaccard averages: inspect representative row sequences and merged geometry.

**Review questions:**
1. Do genuine header bands transition into repeated mixed/numeric rows with stable populated-column footprints?
2. Are those same continuity patterns also present after narrative/all-text bands or in-table subsection labels?
3. Do adjacent independent tables show a meaningful change in column footprint, merged geometry, or row-type sequence?
4. Are there valid tables whose data rows have sparse or shifting columns, such that a strict continuity threshold would create false negatives?
5. Does any combination provide a deterministic boundary signal across the five workbooks, or must the detector retain AMBIGUOUS?

Task 033 remains PARTIAL. No split rule, Jaccard threshold, or promotion rule is approved. The assistant did not run tests or inspect XLSX files directly.


### 8.18 Review of owner-run header-to-body column-transition audit — 2026-11-15

The owner supplied the complete transcript in `reply.md` (blob SHA `804b3ca1b701e52aef9bff348b9cc575bd831d16`). The assistant reviewed the Markdown transcript only; it did not open XLSX files directly. All five workbooks were accepted by the Reader. The report covers six worksheets and repeats the 113 all-text bands previously identified by the header-band audit: Cheshmeh 10, Fzar 4, Fzar2 37, Saman 32, and Parsian 30 across its two worksheets.

**What the transition evidence confirms:**
- Genuine header-like bands commonly transition into populated mixed/numeric rows whose column footprints overlap strongly with the band footprint. Examples include Cheshmeh 130→131 (Jaccard 1.000), Fzar 43:44→45 (0.958), Fzar2 556→557 (1.000), Saman 11:12→13 (1.000), and Parsian 313→315 (the intermediate row 314 is an in-table subsection label).
- Headers can be single-row or multi-row, and the first data row need not immediately follow the band. A section title or unit note may intervene. Examples include Fzar 10:11→12 (section title)→13 (data), Saman 85→86 (in-table subsection label)→87 (data), and Parsian 310→311 (section title)→312 (unit note)→313 (header)→314 (subsection label)→315 (data).
- Sparse or changing populated columns occur in otherwise valid data. The continuity score is therefore descriptive and should not be used as a hard minimum or maximum.

**False-positive / non-boundary evidence:**
- A high Jaccard score is not a table-boundary signal. In Cheshmeh, row 162 is an in-table section label after the header band 160:161; row 163 resumes populated data with Jaccard 1.000. In Saman, row 86 is an in-table subsection label after header row 85; row 87 resumes the data with Jaccard 1.000. In Parsian, row 314 is an in-table subsection label after header row 313; row 315 resumes the data with Jaccard 1.000.
- All-text bands followed by numeric/mixed rows also occur in narrative or descriptive report structures. A band-to-body transition cannot by itself prove that the preceding rows are a new independent table.
- Adjacent independent Parsian tables remain difficult: the previously established sequences around rows 295/300, 309/334 and 358/359 show that a valid header→body transition may occur inside a broader visually contiguous report region, but this audit does not provide a unique structural signature that separates a new table from a subsection or repeated header within an existing table.
- The audit's Jaccard values compare occupied-cell column sets only. They do not account for semantic roles, and merged-cell geometry does not remove the ambiguity. No threshold is supported by the observed positive and negative examples.

**Decision:** this increment does not establish a deterministic, generic table-boundary rule. Do not split, resolve, or promote a region based on Jaccard, column-footprint continuity, an all-text band, a merged-range pattern, or a combination of these signals without a separately validated rule. In particular, do not interpret Jaccard=1.000 as proof of a new table. Keep unresolved regions AMBIGUOUS and block them from semantic extraction. No Detector implementation or regression fixture is approved from this audit alone.

**Next technical step:** stop adding scalar row-similarity heuristics. Build a small, explicit boundary-evidence matrix from the known adjacent Parsian table pairs and the in-table subsection counterexamples (Cheshmeh 162/163, Saman 85–87, Parsian 313–315), recording for each proposed boundary: preceding body footprint, intervening title/unit/header rows, merged-range topology, following body footprint, and whether the boundary is independently established by the owner-provided report evidence. Use that matrix to specify exactly which boundary facts are observable structurally and which are not. If the same observable structure occurs on both sides of a true boundary and a non-boundary, the automatic Detector must not decide between them; preserve AMBIGUOUS or require an explicit report-specific mapping/confirmation. Do not use Persian label meaning or financial semantics to manufacture a structural distinction.

Task 033 remains PARTIAL. No Detector behavior changed, no tests were run by the assistant, and no XLSX files were directly inspected.


### 8.19 Boundary-evidence matrix: adjacent Parsian tables vs. in-table subsection labels — 2026-11-15

Using the targeted Parsian row audit (section 8.11), the row-pattern audits (sections 8.13–8.14), and the header-transition audit (section 8.18), the following evidence matrix was assembled. It is based only on owner-provided Markdown reports; no XLSX file was opened directly.

| Case | Observed sequence | Evidence-supported interpretation | Structural implication |
|---|---|---|---|
| Parsian rows 295–302 | Row 295 section title; rows 297–299 employee/branch data; row 300 next section title; row 301 unit note; row 302 multi-cell all-text header; data follows | Two adjacent independent tables are supported by the targeted report | A new title + optional unit note + fresh header band after prior data is a useful boundary-candidate signature |
| Parsian rows 309–341 | Rows 311–312 title/unit context; row 313 multi-cell header; row 314 one-cell subsection label; rows 315–332 data; next section starts around row 333/334, followed by unit/header rows 335–336 and data from 337 | First table contains an in-table subsection label; a second table follows in the same contiguous report area | A one-cell label after a header is not a boundary; the appearance of a subsequent new header band after a new section context is stronger evidence |
| Parsian rows 355–361 | Rows 355–358 investment data; row 359 next section title; row 360 unit note; row 361 new multi-cell header; data follows | Two adjacent independent tables are supported by the targeted report | Same candidate signature as rows 295–302, without requiring a blank row |
| Cheshmeh rows 160–163 | Header band 160–161; row 162 one-cell subsection label; row 163 data resumes with Jaccard 1.000 | In-table subsection, not a new table | Header→label→data can occur inside one table; column continuity cannot decide a split |
| Saman rows 85–87 | Header row 85; row 86 one-cell subsection label; row 87 data resumes with Jaccard 1.000 | In-table subsection, not a new table | Same negative pattern as Cheshmeh |
| Parsian rows 313–315 | Header row 313; row 314 one-cell subsection label; row 315 data resumes with Jaccard 1.000 | In-table subsection, not a new table | Same negative pattern inside the same workbook containing true adjacent-table cases |

**Interim conclusion:** the combined sequence *prior populated table body → new section/title row(s) → optional unit note → a new all-text header band → subsequent mixed/numeric body* is more discriminating than any single-cell, blank-row, merged-range, or Jaccard feature. The known subsection counterexamples do not show a fresh header band between the subsection label and resumed data. This is a promising **candidate-boundary signature**, not yet an approved automatic rule: the current audits were designed around header bands and do not provide a complete exhaustive search for all occurrences of the compound sequence, nor prove that no in-table nested header can produce it.

**Next technical step:** add a read-only boundary-signature audit that prints configurable physical context *before and after* every all-text band, identifies only structural row classes (empty / single-cell literal text / multi-cell all-text / mixed or numeric-populated), and flags occurrences of the compound sequence without deciding or splitting. Run it across all five workbooks. Review every flagged occurrence and a sample of unflagged known boundaries, narrative bands, and subsection labels. Only if false positives and false negatives are understood should this signature be considered for exact regression fixtures and a conservative candidate-boundary rule. Until then, Task 033 remains PARTIAL and AMBIGUOUS regions remain excluded from semantic extraction.

No code or Detector behavior changed in this increment. The assistant did not run tests or inspect XLSX files directly.


### 8.20 Compound boundary-signature audit utility — 2026-11-15

Added read-only utility `src/scripts/excel_table_boundary_signature_audit.py` (verified blob SHA `cffc854b46b95c73b31b3c6ffc3a90300683085b`). It groups the same physically adjacent multi-cell all-text bands used by the prior header audits, then prints configurable physical context before and after every band (default six rows on each side).

Each physical row is classified only by observed cell kinds: `EMPTY`, `SINGLE_TEXT`, `MULTI_TEXT`, `MIXED_NUMERIC`, or `OTHER`. It flags `COMPOUND_CANDIDATE` only when its bounded context contains (a) a prior mixed/numeric-populated row followed by one or more single-text rows before the all-text band, and (b) a subsequent mixed/numeric-populated row after the band with only single-text/empty rows intervening. This is deliberately a broad structural flag, not a header classifier or boundary decision. Output includes physical context, literal cell coordinates/values, merged ranges, and per-sheet candidate counts. It does not split regions, mutate workbooks, or change Detector behavior.

Owner-run command:

```powershell
Start-Transcript -Path "D:\\Winprojects\\analyzer\\boundary_signature_audit.txt" -Force
python src/scripts/excel_table_boundary_signature_audit.py --max-bands 200 --context-before 6 --context-after 6 excel/cheshme.xlsx excel/fzar.xlsx excel/fzar2.xlsx excel/samanBank.xlsx excel/parsian_periodic.xlsx
Stop-Transcript
```

Commit the complete transcript in `reply.md`. Review every flagged occurrence against known adjacent-table cases and in-table subsection/narrative counterexamples; also inspect unflagged known boundaries for false negatives. A candidate count is not a table count and must not be treated as detector accuracy.

Task 033 remains PARTIAL. No tests were run by the assistant, no XLSX files were directly inspected, and no Detector behavior changed.


### 8.21 Header-to-body column-transition audit results — 2026-11-16

The owner ran `src/scripts/excel_table_header_transition_audit.py` against all five representative workbooks and committed the complete transcript to `reply.md` (blob SHA `804b3ca1b701e52aef9bff348b9cc575bd831d16`). Reader accepted all five workbooks. The six worksheets contain 113 all-text bands in total: Cheshmeh 10, Fzar 4, Fzar2 37, Saman Bank 32, and Parsian periodic 30 (29 on the first worksheet and 1 on the second).

A structural count of the **immediately following physical row** for each band gives:

| Workbook | Mixed/numeric row | Single-text row | Empty row | No following row in audit context | Total |
|---|---:|---:|---:|---:|---:|
| Cheshmeh | 7 | 3 | 0 | 0 | 10 |
| Fzar | 2 | 2 | 0 | 0 | 4 |
| Fzar2 | 20 | 10 | 7 | 0 | 37 |
| Saman Bank | 13 | 9 | 9 | 1 | 32 |
| Parsian periodic | 13 | 9 | 8 | 0 | 30 |
| **Total** | **55** | **33** | **24** | **1** | **113** |

These are transition counts, not header-detection precision/recall. The 55 direct mixed/numeric transitions include genuine header-to-body examples, but also all-text rows/bands whose role is not established by this structural audit. The 33 single-text transitions include section headings and in-table subsection labels; some are followed by data, while others introduce a later header band. Empty-row transitions likewise do not prove a boundary.

Important counterexamples and confirmations from the row-level transcript:
- Cheshmeh rows 160–163: the 160–161 header band is followed by one-cell subsection label row 162 and then data row 163; row 163 has Jaccard 1.000 against the band footprint. This is an in-table continuation, not evidence for a split.
- Parsian rows 313–315: the six-cell all-text header row 313 is followed by one-cell subsection label row 314 and then mixed data row 315. This confirms that a one-cell row between a header and data can be an internal label.
- Saman rows 85–87 show the same header → one-cell label → data pattern.
- Parsian row 336 is a multi-cell all-text header followed immediately by mixed row 337; row 313 is also a multi-cell all-text header, but its immediate successor is an in-table label. Thus even the same general header-band shape can have different legitimate transitions within one workbook.
- Cheshmeh rows 9–10 are followed by a one-cell section title (row 11) and then mixed data (row 12). A direct-next-row test would miss this genuine header-to-body sequence unless it skips the intervening title, but skipping one-cell rows also risks treating internal subsection labels as boundary evidence.
- Several one-row all-text bands in Parsian (for example rows 361, 376, 386, and 395) are followed by mixed rows. Their column continuity is high, but the audit alone cannot establish that those bands are independent table headers rather than in-table labels or other text rows.

Jaccard and column-footprint continuity remain descriptive only. A value of 1.000 occurs both in legitimate header/body continuity and in known in-table subsection continuations. No Jaccard threshold, merged-range rule, or direct/indirect transition rule is justified by these results. No Detector behavior or table segmentation changed.

**Next step:** execute the already-added read-only compound boundary-signature audit documented in section 8.20, then review every flagged and unflagged occurrence against the known adjacent Parsian table boundaries and in-table/narrative counterexamples. The signature must remain a candidate flag, not a table count or automatic split. Task 033 remains PARTIAL; AMBIGUOUS regions remain excluded from semantic extraction.

The assistant did not run tests and did not inspect XLSX files directly; analysis used the owner-provided `reply.md` transcript only.


### 8.22 Compound boundary-signature audit results — 2026-11-16

The owner ran `src/scripts/excel_table_boundary_signature_audit.py` with six physical context rows before and after each all-text band and committed the transcript to `reply.md` (blob SHA `9bdd1cb5bd25f7a165e919b92234819b78efe69a`). The transcript reports these worksheet summaries:

| Workbook / worksheet | Bands printed | `COMPOUND_CANDIDATE` |
|---|---:|---:|
| Fzar (initial transcript segment; workbook heading and beginning of segment are absent) | 4 | 3 |
| Fzar2 | 37 | 9 |
| Saman Bank | 32 | 3 |
| Parsian periodic, worksheet 1 | 29 | 3 |
| Parsian periodic, worksheet 2 | 1 | 0 |

The transcript does **not** contain a separately identifiable Cheshmeh workbook section. Therefore the run does not establish coverage of all five requested workbooks. The initial segment appears to be Fzar from its row content and four-band summary, but its workbook heading and beginning are missing; do not treat the transcript as complete evidence for that file either.

The compound signature correctly flags several previously known adjacent-table examples:
- Parsian rows 295–303: band at row 302 is flagged after the employee/branch data and the new title/unit rows.
- Parsian rows 355–363: band at row 361 is flagged after the preceding investment data and title/unit rows.
- Saman rows 49–53 and 72–76: the bands at rows 52 and 75 are flagged after the preceding table data and new section/unit context.
- Fzar2 contains further plausible table starts, including bands at rows 556, 605–607, 632–635, 719–720, 745, 750–752, 762–764, 799, and 810. These remain candidate occurrences, not independently confirmed table boundaries.

The audit also exposes an important **known false negative**. The Parsian transition around rows 309–341 contains a real adjacent-table sequence: prior table body through row 308, followed by section/title context at rows 309–312, a header at row 313, an in-table subsection label at row 314, and data from row 315; a further table header occurs at row 336 after the next section context. The compound-signature implementation rejects the row-313 band because the prior gap includes a `MULTI_TEXT` row (the merged heading at row 310), while its rule permits only `SINGLE_TEXT` and `EMPTY` between prior body and band. The known true boundary therefore demonstrates that the current signature is not exhaustive. The band at row 336 is likewise not promoted by the current strict prior-gap rule where the context includes a multi-text row.

Known in-table subsection counterexamples remain important negatives: Saman row 86 and Parsian row 314 are single-text labels within continuing tables, not table boundaries. The signature's current candidate condition does not by itself establish table bounds or semantic eligibility; the owner transcript does not provide an independently adjudicated false-positive/false-negative rate.

**Decision:** do not implement `COMPOUND_CANDIDATE` as an automatic split or promotion rule. It is a useful review prioritizer, but the observed missed Parsian case proves that its current gap grammar is too restrictive, and expanding the grammar to admit `MULTI_TEXT` without a new negative-case audit would be speculative. Keep AMBIGUOUS regions out of semantic extraction and Task 033 PARTIAL.

**Next step:** obtain the missing Cheshmeh audit as a separate run, then perform a focused Parsian audit of rows 295–341 that compares the known true boundaries (295/300 and 309/334) with the internal subsection at 314. Specifically inspect the role and merged-range geometry of row 310 and the complete context around row 336, without using Persian label meaning or financial semantics to manufacture a structural distinction. Only then decide whether to extend the candidate grammar or require report-specific confirmation.

The assistant did not run tests and did not inspect XLSX files directly; analysis used only the owner-provided `reply.md` transcript.


### 8.23 مالک استاندارد بصری جدول‌ها در نمونهٔ مرجع Parsian — 2026-11-16

مالک تصریح کرد که مسئلهٔ تشخیص مرز جدول‌ها قبلاً از طریق استانداردسازی بصری در workbook نمونهٔ `parsian_periodic.xlsx` حل شده، اما این تصمیم در مستندات/زمینهٔ کاری ثبت نشده بود. این استاندارد فعلاً فقط روی همین فایل نمونه اعمال شده است و نباید فرض شود سایر workbookها نیز همین قالب‌بندی را دارند.

**استاندارد اعلام‌شدهٔ مالک:**
1. **مرز بیرونی جدول:** کل محدودهٔ هر جدول دارای `thick outside border` است؛ بنابراین لبهٔ آغاز و پایان جدول با Border ضخیم بیرونی مشخص می‌شود.
2. **نام جدول (`table name`):** در یک سلول با رنگ متن قرمز درج می‌شود. این سلول خارج از محدودهٔ جدول و در فاصلهٔ یک یا دو سلول پیش از جدول قرار می‌گیرد.
3. **سرستون (`header`):** با رنگ آبی مشخص می‌شود.
4. **نام زیربخش (`sub table name`):** در برخی جدول‌ها وجود دارد و با رنگ سبز مشخص می‌شود.

**تفسیر برای DB-ING-006:** این قواعد، شواهد ساختاری/قالب‌بندی صریح‌تری نسبت به heuristicهای قبلی مبتنی بر blank band، شمارش سلول، Jaccard یا نوع ردیف فراهم می‌کنند. در نتیجه مسیر بعدی باید از حدس‌زدن مرز از محتوای سلول‌ها به خواندن و اعتبارسنجی annotationهای بصری مالک تغییر کند. باید بررسی شود Reader و DTO فعلی تمام اجزای لازم را حفظ می‌کنند: رنگ واقعی/نوع رنگ Font، رنگ و نوع Fill، Borderهای هر چهار ضلع و نحوهٔ تشخیص outline بیرونی در حضور merged cells. وجود `border_top/bottom/left/right` و `font_bold/fill_type` فعلی به‌تنهایی قرارداد کامل این استاندارد را پوشش نمی‌دهد؛ رنگ Font و جزئیات لازم برای تشخیص thick outside border هنوز در DTO ثبت نشده‌اند.

**محدودیت دامنه:** فقط `parsian_periodic.xlsx` به‌عنوان نمونه استانداردسازی‌شده معرفی شده است. هیچ ادعایی دربارهٔ اعمال استاندارد روی چهار workbook دیگر وجود ندارد. تا زمان پیاده‌سازی و اعتبارسنجی، این استاندارد نباید به‌عنوان شواهد موجود در فایل‌های دیگر فرض شود و نباید بر اساس آن‌ها مرز خودکار ساخته شود.

**تصمیم و گام بعدی:** ابتدا یک ممیزی read-only هدفمند روی خود نمونهٔ استانداردشده انجام شود تا رنگ‌های واقعی قرمز/آبی/سبز، ضخامت و موقعیت Borderهای بیرونی، سلول‌های عنوان و header و subsection، و رفتار merged ranges به‌صورت دقیق گزارش شود. سپس یک جدول مستقل دیگر در `parsian_periodic.xlsx` که این نشانه‌ها را دارد به‌عنوان نمونهٔ دوم انتخاب و ممیزی شود؛ اگر الگو در هر دو جدول یکسان و قابل استخراج باشد، برای یک جدول از workbook دیگر نیز همین استانداردسازی بصری را انجام دهیم تا معلوم شود قرارداد بین فایل‌ها قابل تعمیم است یا صرفاً قرارداد annotation مخصوص نمونهٔ Parsian است. مالک هنوز تأیید نکرده که استاندارد روی فایل دیگری اعمال شده است.

این تصمیم، هنوز به معنی تغییر Detector، تصویب split خودکار، یا تکمیل Task 033 نیست. Task 033 همچنان PARTIAL می‌ماند تا شواهد قالب‌بندی از فایل نمونه استخراج، در DTO/Reader پوشش داده، و با fixtureهای مثبت و منفی اعتبارسنجی شوند. دستیار XLSX را مستقیماً باز نکرد و تست اجرا نکرد؛ این ثبت بر اساس توضیح صریح مالک است.


### 8.24 اصلاح معماری: استاندارد شرکت‌محورِ محدودهٔ جدول‌ها، نه تشخیص مرز در هر گزارش — 2026-11-16

مالک روشن کرد که هر شرکت یک workbook نمونه را استانداردسازی می‌کند و محدودهٔ جدول‌های آن به‌عنوان مرجع ثبت می‌شود؛ گزارش‌های دیگر همان شرکت از نظر ساختار مشابه‌اند. بنابراین استاندارد بصری بخش 8.23 صرفاً ابزار/راهنمای annotation در فایل نمونه برای تعیین و ثبت محدوده‌هاست، نه قرارداد قالب‌بندی برای گزارش‌های بعدی و نه شرط runtime extraction.

**تصمیم معماری صحیح:**
1. برای هر شرکت یک `Company Table Layout Template` مستقل و نسخه‌بندی‌شده تعریف می‌شود که از workbook نمونهٔ همان شرکت استخراج/تأیید شده است.
2. Template باید برای هر جدول، هویت شرکت و نسخهٔ الگو، worksheet، شناسه/نام پایدار جدول (`table name`)، محدودهٔ دقیق سلولی جدول در نمونه (حداقل start/end row و column)، محدوده/ساختار header، و در صورت وجود نام و محدوده/ساختار sub-tableها را ثبت کند. رابطهٔ header و sub-table با جدول والد باید صریح باشد.
3. Border ضخیم بیرونی و رنگ‌های قرمز/آبی/سبز در فایل نمونه برای تعیین و کنترل محدوده‌ها به کار می‌روند. این نشانه‌ها در گزارش‌های بعدی لازم نیستند و نباید شرط پذیرش یا استخراج باشند.
4. در گزارش‌های بعدی همان شرکت، استخراج باید با تطبیق ساختار گزارش با Template مصوب و محدوده/الگوی جدول‌های ثبت‌شده انجام شود، نه با جست‌وجوی Border یا رنگ در هر workbook. هرگونه جابه‌جایی ردیف/ستون، تغییر نام شیت، اضافه/حذف جدول یا تغییر ساختار باید با قواعد تطبیق صریح و اعتبارسنجی کنترل شود؛ نباید فرض شود مختصات مطلق نمونه بدون بررسی در تمام دوره‌ها ثابت می‌ماند.
5. Templateها دادهٔ مرجعِ ساختار گزارش‌اند و باید مستقل از محتوای مالی هر ReportVersion نگهداری و version شوند. هر تغییر الگو باید نسخهٔ جدید بسازد؛ تفسیر تاریخی templateهای قبلی نباید بی‌صدا تغییر کند.

**تفکیک دو مرحله:**
- **مرحلهٔ استانداردسازی (یک‌بار برای هر شرکت/نمونه):** شناسایی جدول‌ها و ثبت دقیق bounds، header و sub-table relationships با کمک annotationهای بصری نمونه.
- **مرحلهٔ استخراج (برای هر گزارش بعدی شرکت):** شناسایی/تطبیق جدول‌ها با template همان شرکت و استخراج بر اساس قرارداد ساختاری ثبت‌شده؛ Border و رنگ، اگر در فایل بعدی وجود نداشتند، مانع استخراج نیستند.

**اثر بر کار جاری:** heuristicهای عمومی قبلی برای حدس‌زدن مرزها (blank bands، row classes، Jaccard و compound signature) مسیر اصلی حل مسئله نیستند. آن‌ها نباید برای جایگزینی template یا split خودکار در گزارش‌های بعدی به کار روند. Task 033 باید از «visual table-region detection عمومی» به «استخراج و ثبت Company Table Layout Template از workbook نمونه، سپس طراحی template-based matching» بازتعریف شود. وضعیت PARTIAL باقی می‌ماند؛ ابتدا باید مدل دقیق template و قواعد تطبیق گزارش‌های بعدی مشخص شود و سپس با یک شرکت/نمونه end-to-end اعتبارسنجی گردد.

**دامنهٔ فعلی:** مالک گفته است `parsian_periodic.xlsx` نمونهٔ استانداردشدهٔ فعلی است. این ثبت، تصمیم معماری را مستند می‌کند؛ دستیار فایل XLSX را مستقیماً باز نکرده، محدوده‌های واقعی جدول‌ها را استخراج نکرده و تست اجرا نکرده است. همچنین هنوز تأیید نشده که مختصات جدول‌ها بین گزارش‌های زمانی همان شرکت ثابت است یا ممکن است جابه‌جا شوند؛ این موضوع باید هنگام طراحی matcher با شواهد نمونه و گزارش‌های دیگر تعیین شود.


### 8.25 نتیجهٔ Cheshmeh و بازگشت از heuristic به Template — 2026-11-16

مالک transcript اجرای مستقل `excel_table_boundary_signature_audit.py` روی `cheshme.xlsx` را در `reply.md` قرار داد (blob SHA `9bdd1cb5bd25f7a165e919b92234819b78efe69a`). Reader فایل را پذیرفت؛ worksheet با used range برابر `A1:V222` دارای 10 all-text band بود. فقط band ردیف‌های 138–139 به‌عنوان `COMPOUND_CANDIDATE` گزارش شد؛ 9 band دیگر `NO_MATCH` بودند. Headerهای نمونه در ردیف‌های 9–10، 44–45، 77، 94، 107–109، 130، 160–161 و 194–196 عمدتاً با signature شناسایی نشدند. این نتیجه، به‌همراه false negativeهای Parsian و subsectionهای داخلی ثبت‌شده در بخش 8.22، استفاده از compound signature یا سایر heuristicهای ردیفی به‌عنوان الگوریتم مرزبندی را منتفی می‌کند. از این پس این ممیزی‌ها صرفاً سابقهٔ تحقیق‌اند و نباید مسیر پیاده‌سازی باشند.

**معماری مصوب مالک (تأکید):** یک workbook نمونه برای هر شرکت استاندارد می‌شود؛ محدودهٔ دقیق همهٔ جدول‌ها در همان نمونه با annotation بصری مشخص و به‌عنوان Company Table Layout Template نسخه‌بندی‌شده ثبت می‌شود. گزارش‌های بعدی همان شرکت با Template تطبیق داده شده و بر اساس محدوده/ساختار تعریف‌شده استخراج می‌شوند. Border و رنگ در فایل‌های بعدی نه لازم‌اند و نه معیار استخراج.

**پاک‌سازی کد و فایل‌های موقت:** ابزارهای موقت ممیزی زیر از `src/scripts` حذف شدند:
- `excel_table_boundary_audit.py`
- `excel_table_boundary_signature_audit.py`
- `excel_table_detector_review.py`
- `excel_table_header_band_audit.py`
- `excel_table_header_transition_audit.py`
- `excel_table_row_pattern_audit.py`
- `excel_table_targeted_row_audit.py`

همچنین `src/ingestion/excel/table_detector.py` و `src/tests/test_excel_table_detector.py` حذف شدند؛ این detector مبتنی بر blank-band heuristic با معماری مصوب template-based هم‌راستا نبود و هیچ ارجاع کدی به تابع آن در جست‌وجوی مخزن یافت نشد. سایر فایل‌های ingestion اصلی حذف نشدند.

**وضعیت تغییرات در کد اصلی (شفاف‌سازی):**
- `src/ingestion/excel/reader.py` و `dto.py` تغییرات اصلی دارند. پذیرش و نگهداری native literal numeric values بخشی از قرارداد مصوب Excel است و حفظ می‌شود.
- شواهد قالب‌بندی اضافه‌شده به `CellObservation` شامل `border_top/bottom/left/right`، `fill_type` و `font_bold` است؛ Reader این شواهد را برای سلول‌های populated و سلول‌های blank دارای style حفظ می‌کند. `style_id` از قبل وجود داشت.
- رنگ واقعی Font و Fill هنوز در DTO/Reader ثبت نمی‌شود؛ برای خواندن annotationهای قرمز/آبی/سبز باید این قابلیت در گام ابزار استخراج Template تکمیل شود. این metadata فقط برای استانداردسازی نمونه مصرف می‌شود، نه برای extraction گزارش‌های بعدی.
- `table_detector.py` و تست آن حذف شده‌اند؛ تست‌های DTO و Reader حفظ شده‌اند. دستیار هیچ تستی اجرا نکرده است.

**گام بعدی اجرایی:** پیش از matcher، قرارداد Template باید مشخص و پیاده‌سازی شود: شناسهٔ پایدار شرکت و report-template، نسخهٔ immutable، worksheet identity، table ID/name، exact source bounds، header bounds/levels، sub-table bounds و parent-child relation، و fingerprint ساختاری لازم برای کنترل تغییرات. سپس ابزار one-time annotation reader باید در workbook نمونه، table name قرمز، header آبی، sub-table name سبز و thick outside border را بخواند و محدوده‌ها را به یک Template قابل بازبینی تبدیل کند. پس از تأیید bounds واقعی Parsian، matcher گزارش‌های بعدی همان شرکت جداگانه طراحی می‌شود. مختصات مطلق نمونه نباید بدون شواهد ثبات، به‌عنوان مختصات ثابت تمام گزارش‌های بعدی فرض شود.

Task 033 همچنان PARTIAL است. دستیار فقط transcript موجود در `reply.md` را بررسی کرده؛ XLSX را مستقیماً باز نکرده و تست اجرا نکرده است. بخش 8.24 مرجع تصمیم معماری است؛ این بخش نتیجهٔ Cheshmeh، پاک‌سازی و وضعیت دقیق کد را تکمیل می‌کند.


### 8.26 گام بعدی: قرارداد Template شرکت/نوع گزارش — 2026-11-16

سند طراحی اولیهٔ `database/reports/COMPANY_TABLE_LAYOUT_TEMPLATE_SPEC.md` ایجاد شد. کلید منطقی Template به‌صورت شرکت + نوع/خانوادهٔ گزارش تعریف شده است؛ هر نسخه immutable است و شامل هویت worksheetها، table ID/name، bounds دقیق نمونه، سلول نام جدول، header bounds/levels، body/footer در صورت نیاز، sub-tableها و رابطهٔ parent-child، ترتیب و fingerprint ساختاری خواهد بود.

این سند همچنین تفکیک را تثبیت می‌کند: annotationهای قرمز/آبی/سبز و thick outside border فقط برای authoring/validation یک‌بارهٔ نمونه استفاده می‌شوند؛ گزارش‌های بعدی با Template تطبیق داده می‌شوند و به همان formatting نیاز ندارند. Matcher باید deterministic باشد؛ missing/duplicate/ambiguous یا تغییر ساختاری تأییدنشده باعث توقف و رد کل گزارش می‌شود، نه fuzzy matching یا ingestion جزئی.

**تصمیم‌های باز که باید با شواهد نمونه پاسخ داده شوند:** ثبات نام/ترتیب worksheet، ثبات یا جابه‌جایی مختصات مطلق جدول‌ها در گزارش‌های بعدی، مدل‌سازی دقیق offset سلول table name، bounds header/body/footer، و محل ذخیره‌سازی/versioning Template. این موارد هنوز پیاده‌سازی نشده‌اند.

گام اجرایی بعدی: توسعهٔ ابزار one-time annotation reader برای workbook نمونهٔ Parsian. Reader باید font/fill color را با حفظ نوع رنگ (RGB/indexed/theme) و Border side styles را برای سلول‌های populated و styled blank گزارش کند؛ سپس با قواعد رنگی و thick outside border، پیشنهاد bounds/table-name/header/sub-table بسازد تا مالک بتواند آن‌ها را تأیید کند. بعد از تأیید، bounds به Template نسخه‌دار تبدیل می‌شوند. برای runtime matcher باید یک گزارش دوره‌ای دیگر از همان شرکت مقایسه شود تا میزان drift مختصات معلوم گردد.

Task 033 PARTIAL است؛ هنوز bounds واقعی Parsian استخراج نشده‌اند. دستیار تست اجرا نکرده و XLSX را مستقیماً باز نکرده است.


### 8.27 ابزار پایدار ممیزی Annotation نمونه — 2026-11-16

ابزار `src/scripts/excel_template_annotation_audit.py` اضافه شد (read-only و مخصوص مرحلهٔ authoring نمونه، نه runtime extraction). ابزار ابتدا workbook را با Reader اصلی اعتبارسنجی می‌کند و سپس با openpyxl موارد زیر را گزارش می‌دهد:
- مستطیل‌هایی که هر چهار ضلع کامل آن‌ها از Border style برابر `thick` تشکیل شده باشد؛
- سلول‌های دارای رنگ غیرپیش‌فرض Font/Fill با حفظ نوع و مقدار خام RGB/indexed/theme/tint؛
- سلول‌های دارای thick border و ضلع مربوط؛
- تمام merged ranges هر worksheet؛
- worksheet bounds و SHA-256 منبع.

ابزار هیچ workbook را تغییر نمی‌دهد، رنگ را به قرمز/آبی/سبز تبدیل یا تفسیر نمی‌کند، و مستطیل‌های گزارش‌شده را بدون بازبینی مالک به‌عنوان جدول قطعی ثبت نمی‌کند. مستطیل‌های thick فقط پیشنهاد مرز هستند؛ رنگ‌ها نیز به‌صورت metadata خام ارائه می‌شوند تا نقش table name/header/sub-table با شواهد و تأیید مشخص شود.

فرمان اجرای مالک در PowerShell:
```powershell
Start-Transcript -Path "D:\Winprojects\analyzer\template_annotation_audit_parsian.txt" -Force
python src/scripts/excel_template_annotation_audit.py --max-color-cells 2000 excel/parsian_periodic.xlsx
Stop-Transcript
```
Transcript کامل باید در `reply.md` ثبت شود. خروجی آن مبنای استخراج bounds و ساخت اولین Company Table Layout Template خواهد بود.

این ابزار پس از ایجاد از نظر محتوا در GitHub بازخوانی شد؛ دستیار تست یا اجرای محلی انجام نداده و XLSX را مستقیماً باز نکرده است. Task 033 PARTIAL باقی است.


### 8.28 نتیجهٔ اولین ممیزی annotation در Parsian — 2026-11-16

مالک فرمان زیر را اجرا و transcript را در `reply.md` ثبت کرد:
```powershell
python src/scripts/excel_template_annotation_audit.py --max-color-cells 2000 excel/parsian_periodic.xlsx
```
Reader اجرای workbook را بدون گزارش rejection خاتمه داد؛ transcript دارای traceback یا خطای اجرایی نیست. با این حال، transcript در ابتدای خروجی شیت اول از میانهٔ رکوردهای سلولی شروع می‌شود و بخش ابتدایی آن (از جمله metadata کامل شیت اول و ابتدای فهرست رنگ‌ها) در نسخهٔ ثبت‌شده قابل مشاهده نیست؛ بنابراین نباید آن را transcript کامل و قابل اتکا برای همهٔ سلول‌های شیت اول فرض کرد.

شواهد مستقیم قابل مشاهده:
- برای شیت دوم، عنوان `Sheet1` و used range برابر `A1:E24` ثبت شده و دو merged range برابر `A16:A17` و `E16:E17` گزارش شده‌اند.
- در شیت دوم، عنوان قرمز در `A14` با متن «صورت سود و زیان جامع»، header آبی در ردیف‌های 16–17 و یک نشانهٔ سبز در `A19` دیده می‌شود. این با الگوی نام جدول/سرستون/زیرجدول سازگار است؛ اما محدودهٔ کل جدول از این نشانه‌ها به‌تنهایی قابل اثبات نیست.
- در شیت اول، نمونه‌هایی از عنوان‌های قرمز در `A236`, `A264`, `A277`, `A300`, `A311`, `A334`, `A351`, `A359`, `A374`, `A384` و `A393` و سرستون‌های آبی در ردیف‌های متناظر 238–239، 266–267، 279، 302، 313، 336، 353–354، 361، 376، 386 و 395 قابل مشاهده‌اند. نمونه‌هایی از برچسب‌های سبز نیز در شیت اول گزارش شده‌اند؛ به‌علت ناقص بودن ابتدای transcript، فهرست کامل آن‌ها در این مرحله ثبت نمی‌شود.
- برای هر دو شیت، `THICK_OUTSIDE_RECTANGLES count=0` و `THICK_BORDER_CELLS_COUNT=0` گزارش شده است. بنابراین در فایل ممیزی‌شده هیچ ضلع ضخیم با style دقیق `thick` ثبت نشده و قاعدهٔ اعلام‌شدهٔ thick outside border در دادهٔ قابل ممیزی حاضر نیست.

**نتیجهٔ معماری/اجرایی:** فعلاً هیچ exact table bounds تأیید یا وارد Template نمی‌شود. عنوان قرمز و header آبی برای تعیین نقاط شروع نامزد مفیدند، اما بدون مرز بیرونی مشخص، انتهای body، footer و جداسازی جدول‌های مجاور قابل استنتاج قطعی نیست. از روی رنگ یا متن، محدودهٔ جدول را حدس نمی‌زنیم.

**گام بعدی لازم از مالک:** فایل نمونهٔ `excel/parsian_periodic.xlsx` را مطابق قرارداد annotation تکمیل کند: برای هر جدول، thick outside border پیوسته روی چهار ضلع کل محدوده؛ رنگ قرمز برای سلول نام جدول؛ آبی برای کل header؛ سبز برای نام sub-table در صورت وجود. سپس همان audit را دوباره اجرا کند و transcript کامل را در `reply.md` ثبت کند. برای جلوگیری از خروجی حجیم و ثبت ناقص، اجرای بعدی باید ابتدا با `--max-color-cells 1` برای تأیید metadata و summary border انجام شود؛ سپس transcript کاملِ نسخهٔ نهایی annotation با سقف رنگ کافی ثبت گردد. اگر فایل از قبل thick border دارد، به‌جای تغییر مجدد، باید خود فایل/نسخهٔ دقیق مورد ممیزی و style واقعی border بررسی شود.

Task 033 همچنان PARTIAL است. دستیار فقط محتوای ثبت‌شده در `reply.md` را تحلیل کرده؛ XLSX را مستقیماً باز نکرده و هیچ تستی اجرا نکرده است.


## 8.29 — اصلاح ممیزی Border با لحاظ جهت راست‌به‌چپ شیت

پس از روشن‌شدن اینکه گزارش‌های فارسی در Excel به‌صورت راست‌به‌چپ نمایش داده می‌شوند، ابزار ممیزی توسعه یافت. این اصلاح صرفاً گزارش شواهد خام را دقیق‌تر می‌کند و هیچ قاعده‌ای برای تشخیص خودکار یا پذیرش مرز جدول تغییر نمی‌دهد.

تغییرات در `src/scripts/excel_template_annotation_audit.py`:
- مقدار `worksheet.sheet_view.rightToLeft` برای هر شیت گزارش می‌شود.
- نگاشت لبهٔ بصری به ضلع سلول توضیح داده می‌شود: در شیت RTL ستون A در سمت راست نمایش داده می‌شود؛ بنابراین لبهٔ بصری راست جدول آغازشونده از A با `border.right` سلول‌های ستون A متناظر است. در شیت LTR، لبهٔ بصری چپ با `border.left` متناظر است.
- شمارش تعداد styleهای واقعی Border برای هر چهار ضلع `top/bottom/left/right`، مستقل از اینکه style برابر `thick` باشد یا نه، اضافه شد.
- مختصات تمام سلول‌هایی که روی هر ضلع Border دارند گزارش می‌شود.
- شواهد style ضلع‌های پیرامونی merged ranges جداگانه گزارش می‌شود.
- تشخیص سخت‌گیرانهٔ `THICK_OUTSIDE_RECTANGLES` حفظ شده و هنوز فقط مستطیل‌هایی را پیدا می‌کند که هر چهار ضلع کامل آن‌ها دقیقاً `thick` باشد؛ این خروجی به‌تنهایی اثبات نبودن مرز بصری با styleهای دیگر نیست.

نکتهٔ فنی: سلول‌های ستون A از نظر مدل Excel می‌توانند `border.left` داشته باشند؛ راست‌به‌چپ بودن شیت نام ضلع‌های فیزیکی در مدل سلول را جابه‌جا نمی‌کند، بلکه محل نمایش ستون‌ها را تغییر می‌دهد. بنابراین ابزار جهت نمایش و ضلع واقعی سلول را جداگانه گزارش می‌کند.

**گام بعدی مالک:** همان فرمان ممیزی را دوباره روی فایل نمونه اجرا و خروجی کامل را در `reply.md` ثبت کند:

```powershell
python src/scripts/excel_template_annotation_audit.py --max-color-cells 2000 excel/parsian_periodic.xlsx
```

این تغییر هنوز روی workbook اجرا یا با تست تأیید نشده است؛ دستیار تست اجرا نکرده و XLSX را مستقیماً باز نکرده است. Task 033 همچنان PARTIAL باقی می‌ماند تا bounds واقعی جدول‌ها از نمونهٔ تأییدشده استخراج شوند.


## 8.30 — تحلیل ممیزی دوم Parsian و اصلاح خروجی Color

transcript مالک در `reply.md` (blob SHA: `0059dbe82da192c9332354b1051259ef1e8b6b4c`) بررسی شد.

**شواهد قابل اتکا از شیت دوم:**
- عنوان شیت در transcript: `Sheet1`، used range برابر `A1:E24` و دو merged range برابر `A16:A17` و `E16:E17`.
- تنظیم ثبت‌شدهٔ `right_to_left=False` است. بنابراین metadata همین worksheet، نمایش RTL را تأیید نمی‌کند؛ فارسی بودن متن به‌تنهایی برای استنتاج RTL کافی نیست.
- همهٔ Borderهای گزارش‌شده از نوع `medium` هستند: `top=55`, `bottom=57`, `left=57`, `right=57`. هیچ Border از نوع `thick` گزارش نشده است.
- سلول‌های A1:A12 نیز Borderهای medium دارند. در محدودهٔ A16:E24، سلول‌های جدول و merged cells دارای Borderهای medium در پیرامون و شبکهٔ داخلی هستند.
- عنوان قرمز A14، header آبی در ردیف‌های 16–17 و برچسب سبز A19 دیده می‌شوند. بر این اساس A16:E24 یک **نامزد محدودهٔ جدول** با header در A16:E17 و برچسب sub-table احتمالی در A19 است؛ هنوز به‌عنوان bounds قطعی Template تأیید نمی‌شود، زیرا نشانهٔ قراردادی thick outside border در این شیت وجود ندارد و نقش A19 باید با مالک تطبیق داده شود.

**محدودیت transcript شیت اول:**
- ابتدای خروجی شیت اول در transcript موجود ناقص است و بخش summary مربوط به worksheet (از جمله right_to_left و BORDER_SIDE_STYLE_COUNTS) در آن قابل بازیابی نیست.
- انتهای خروجی شیت اول `COLOR_CELLS_PRINTED=1655` و `THICK_BORDER_CELLS_COUNT=0` را نشان می‌دهد؛ این مقدار صفر فقط دربارهٔ سبک دقیق thick است و به معنی نبود سایر سبک‌های Border نیست.
- بنابراین دربارهٔ جهت شیت اول یا تعداد/styleهای Border آن نتیجه‌گیری نمی‌شود.

**اصلاح ابزار:** خروجی `_color_descriptor` اصلاح شد تا فقط ویژگی فعال متناسب با نوع رنگ (rgb/indexed/theme/auto) را بخواند؛ نسخهٔ قبلی ویژگی‌های نامرتبط را نیز می‌خواند و پیام‌های `Values must be of type ...` تولید می‌کرد. این اصلاح برای خوانایی گزارش است و معنای رنگ‌ها یا قواعد تشخیص جدول را تغییر نمی‌دهد.

**گام بعدی مالک برای ثبت transcript کامل و کم‌حجم:** پس از دریافت آخرین تغییرات، فرمان را با سقف یک سلول رنگی اجرا کند تا summary هر دو شیت بدون خروجی حجیم رنگ‌ها ثبت شود:

```powershell
python src/scripts/excel_template_annotation_audit.py --max-color-cells 1 excel/parsian_periodic.xlsx
```

در صورت نیاز، جزئیات کامل annotationهای رنگی را می‌توان جداگانه با سقف بزرگ‌تر گرفت؛ برای تشخیص جهت و Border نیازی به چاپ هزاران سلول رنگی نیست. Task 033 همچنان PARTIAL است؛ دستیار تست اجرا نکرده و XLSX را مستقیماً بازبینی نکرده است.


## 8.31 — ممیزی کامل metadata فایل نهایی Parsian پس از حذف شیت آزمایشی — 2026-11-19

مالک ابزار `excel_template_annotation_audit.py` را با سقف 2000 سلول رنگی روی `excel/parsian_periodic.xlsx` اجرا کرد و خروجی کامل را به فایل `template_annotation_audit_full.txt` هدایت کرد. transcript فرمان و خروجی فیلترشده در `reply.md` ثبت شده است.

**شواهد قطعی این اجرا:**
- Reader: `ACCEPTED`.
- SHA-256 فایل فعلی: `55266751a5ae60666ebce05f1ed4ee1c4df94a4f78fa0c764aa4a0dc4325db85`.
- فقط یک worksheet گزارش شده: `Recovered_Sheet1`.
- Used range: `A1:L411`؛ تعداد merged ranges: `101`.
- `right_to_left=True`؛ ستون A در سمت راست نمایش داده می‌شود و لبهٔ بصری راستِ جدول‌هایی که از A شروع می‌شوند با `border.right` ستون A متناظر است.
- `THICK_OUTSIDE_RECTANGLES count=0`.
- Border counts: top: medium=1606, thin=1؛ bottom: medium=1649, thin=193؛ left: medium=1247, thin=2؛ right: medium=1526.

**تفسیر محدود و اصلاح سابقه:** این اجرا هویت تک‌شیتی و hash نسخهٔ فعلی را روشن می‌کند و نشان می‌دهد فرض «thick border دقیق» برای این فایل برقرار نیست. با این حال، شمارش medium/thin به‌تنهایی bounds جدول را ثابت نمی‌کند؛ ضمن اینکه zero thick rectangles به معنی نبود قاب‌های بصری با سبک medium نیست. ابزار فعلی فقط مستطیل‌های چهارضلعی با سبک دقیق thick را در بخش `THICK_OUTSIDE_RECTANGLES` تشخیص می‌دهد. بنابراین نباید از این خروجی نتیجه گرفت که جدول‌ها قاب ندارند یا هر محدودهٔ merged یک جدول مستقل است.

**محدودیت transcript رنگ‌ها:** خروجی فیلترشده در `reply.md` فقط سطر عنوان `COLOR_ANNOTATIONS` را نشان می‌دهد و هیچ سطر سلول رنگی یا `COLOR_CELLS_PRINTED` پس از آن در transcript قابل مشاهده نیست. از این رو، فهرست کامل red/blue/green annotationها در این اجرا قابل استناد نیست؛ آن را از خروجی قبلی یا مختصات گزارش 3 حدس نمی‌زنیم. فایل کامل محلی `template_annotation_audit_full.txt` ایجاد شده، اما محتوای آن به‌صورت کامل در مخزن ارائه نشده است.

**نتیجه:** مانع تک‌شیتی بودن و hash نسخهٔ فعلی رفع شد. مانع استخراج Template هنوز باقی است: فهرست کامل annotationها و نقش آن‌ها (table title/header/sub-table) باید از فایل کامل خروجی قابل مشاهده شود؛ سپس bounds هر جدول باید با بازبینی ساختاری و تصمیم مالک تأیید شوند. هیچ bounds یا partition جدیدی در این بخش تصویب نشده است. Task 033 همچنان PARTIAL است. دستیار XLSX را مستقیماً باز نکرد و هیچ تستی اجرا نکرد.

## 8.32 ثبت دفتر تأیید هندسهٔ 17 جدول و 15 زیرجدول — 2026-11-19

این دفتر، نقاط موردنیاز برای تأیید/اصلاح مالک را جدا می‌کند. **این فهرست تأییدشده یا Template نهایی نیست**؛ فقط candidateهای تاریخی برای بازبینی روی artifact فعلی است.

### 8.32.1 شکاف هویت artifact

سه hash متفاوت در شواهد موجود است و نباید آن‌ها را یک فایل واحد فرض کرد:

- 69186f1ad2b0e481a3588f2731b7027b0a9d9a543d1ca17fd24fc71d8c5aca06: workbook دو‌شیتی که گزارش مستقیم OOXML شمارهٔ 3 روی آن اجرا شد؛ شواهد هندسی زیر از همین گزارش آمده‌اند.
- 95f94e739632e48ae6552c562ecbf6c3e8182848718d17977f69bc984a6638b0: hash درج‌شده در annotation map و audit متنی قبلی.
- 55266751a5ae60666ebce05f1ed4ee1c4df94a4f78fa0c764aa4a0dc4325db85: hash فایل فعلی در اجرای 2026-11-19؛ این اجرا تک‌شیتی بودن، used range، RTL و خلاصهٔ Border را ثابت می‌کند، اما transcript قابل مشاهدهٔ آن فهرست کامل annotationها را ندارد.

هیچ worksheet-XML hash یا تطبیق مختصات مستقیمی ثابت نمی‌کند bounds و fillهای استخراج‌شده از دو hash قدیمی‌تر بدون تغییر به hash فعلی تعلق دارند. بنابراین جدول زیر فقط candidate تاریخی برای بازبینی روی artifact با hash فعلی است.

### 8.32.2 دفتر candidate bounds جدول‌های اصلی

| ID | عنوان قرمز | Candidate bounds تاریخی | نکتهٔ بازبینی |
|---|---|---|---|
| T01 | A8 | A10:D42 | مرز medium؛ header/سلول‌های بیرون از قاب خودکار وارد نشوند |
| T02 | A58 | A60:D68 | مرز medium؛ extensionهای Border موجب توسعهٔ محدوده نشوند |
| T03 | A77 | A79:C119 | مرز medium؛ ردیف 95 تکراری و نادیده‌گرفتنی است |
| T04 | A128 | A130:L165 | مرز medium؛ بلوک سیاه A131:L151 طبق تصمیم مالک excluded است |
| T05 | A174 | A176:D213 | مرز medium |
| T06 | A236 | A238:I253 | مرز medium؛ ردیف‌های 243–244 سیاه/بدون fill از extraction خارج‌اند |
| T07 | A264 | A266:C275 | مرز medium |
| T08 | A277 | A279:B283 | مرز medium؛ A297:D299 بیرون از محدوده و غیرقابل استخراج است |
| T09 | A300 | A302:C308 | مرز medium؛ B302 آبی نیست |
| T10 | A311 | A313:D332 | مرز medium |
| T11 | A334 | A336:C339 | مرز medium |
| T12 | A351 | A353:I358 | مرز medium |
| T13 | A359 | A361:C367 | مرز medium؛ ردیف 364 بدون fill و excluded است |
| T14 | A374 | A376:C378 | مرز medium |
| T15 | A384 | A386:C387 | مرز medium |
| T16 | A393 | A395:C398 | مرز thin؛ پیوستگی قاب روی فایل فعلی دوباره دیده شود |
| T17 | A403 | A404:E405 | مرز thin؛ استثنای معتبر بدون ستون زرد |

### 8.32.3 دفتر candidate زیرجدول‌ها

ردیف‌های زیر از ترتیب markerهای سبز در annotation map تاریخی به‌دست آمده‌اند. ستون‌های دقیق هر زیرجدول و اتصال Header آن هنوز مستقل از محدودهٔ parent تأیید نشده‌اند.

| Parent | Marker سبز | Candidate row partition | ستون‌های دقیق |
|---|---|---:|---|
| T01 | A12 | 12–31 | نیازمند تأیید |
| T01 | A32 | 32–34 | نیازمند تأیید |
| T01 | A35 | 35–42 | نیازمند تأیید |
| T02 | A63 | 63–68 | نیازمند تأیید |
| T03 | A81 | 81–94 | نیازمند تأیید |
| T03 | A96 | 96–107 | نیازمند تأیید |
| T03 | A108 | 108–119 | نیازمند تأیید |
| T04 | A152 | 152–165 | نیازمند تأیید |
| T05 | A178 | 178–181 | نیازمند تأیید |
| T05 | A182 | 182–190 | نیازمند تأیید |
| T05 | A191 | 191–213 | نیازمند تأیید |
| T07 | A268 | 268–275 | نیازمند تأیید |
| T10 | A314 | 314–332 | نیازمند تأیید |
| T13 | A362 | 362–365 | نیازمند تأیید |
| T13 | A366 | 366–367 | نیازمند تأیید |

تصمیم‌های قبلی مالک که باید در تأیید هندسه حفظ شوند:
- T02 ردیف 62 متعلق به parent است و داخل زیرجدول A63 قرار نمی‌گیرد.
- T03 ردیف 95 header تکراری است و زیرجدول دارایی‌ها در 94 پایان می‌یابد.
- T13 ردیف 364 بدون fill است و extraction نمی‌شود.
- هر مختصات gray دقیقاً یک owner node دارد؛ parent و child نباید یک مختصات را دوباره مالک شوند.
- ستون‌های child نباید از عرض parent یا مقدارهای uncolored حدس زده شوند.

### 8.32.4 معیار بسته‌شدن تأیید هندسه

برای هر یک از 17 جدول، مالک باید bounds کامل (چهار ضلع، شامل ستون آغاز/پایان) را برای hash فعلی 55266751...4325db85 تأیید یا اصلاح کند. برای هر یک از 15 زیرجدول نیز باید بازهٔ ردیف و ستون، رابطهٔ Header (موروثی/مستقل) و تعلق gray cells را تأیید یا اصلاح کند. تأیید کلی بدون اتصال به hash فعلی یا بدون پوشش همهٔ ردیف‌های دفتر، این gate را نمی‌بندد.

پس از ثبت تأیید:
1. annotation audit کامل روی همان artifact و hash اجرا شود و خروجی کامل red/blue/green/yellow/gray/black به مخزن برسد؛ theme-based black fill نیز باید در طبقه‌بندی لحاظ شود.
2. نقشهٔ مختصات از روی تأیید مالک بازتولید شود؛ انتظار فعلی 459 gray cells و 60 vertical spans صرفاً reconciliation تاریخی است، نه invariant تحمیلی.
3. validator مستقل ثابت کند هر مختصات مثبت دقیقاً یک owner node دارد، هیچ سلول uncolored/black وارد نشده، blank-gray حفظ شده و union parent/descendant duplicate ندارد.
4. سپس Template همان sample با deterministic worksheet identity و Header/row-axis matching اعتبارسنجی شود؛ workbook مستقل دورهٔ بعد همچنان gate جداگانهٔ drift است.

**وضعیت:** هیچ bounds یا child-column range در این بخش approved نیست. DB-ING-006 / Task 033 همچنان PARTIAL. این ثبت فقط مستندات review را ساخت؛ workbook باز/تغییر داده نشد، کد/ORM/schema/migration/DB تغییر نکرد و تستی اجرا نشد.

## 8.33 — اجرای audit روی workbook نهایی و matcher قطعی fail-closed — 2026-11-20

### Artifact and full annotation audit

فایل مبنا همان workbook نهایی `excel/parsian_periodic.xlsx` است؛ فایل آزمایشی یا نسخهٔ قدیمی جایگزین نشد. SHA-256 پیش و پس از audit برابر `55266751a5ae60666ebce05f1ed4ee1c4df94a4f78fa0c764aa4a0dc4325db85` و اندازه 34,450 bytes است. Reader آن را پذیرفت: یک worksheet به نام `Recovered_Sheet1`، used range برابر `A1:L411`، 101 merged ranges و `right_to_left=True`.

فرمان کامل اجراشده:

```powershell
$env:PYTHONIOENCODING='utf-8'
.\.venv\Scripts\python.exe -m src.scripts.excel_template_annotation_audit --max-color-cells 2000 --candidate-register database/reports/parsian_template_candidate_register.json --candidate-audit-json database/reports/parsian_template_candidate_audit_current.json excel/parsian_periodic.xlsx *> database/reports/template_annotation_audit_parsian_current.txt
```

خروجی نهایی: exit code 0؛ `Reader: ACCEPTED`؛ hash بالا؛ `THICK_OUTSIDE_RECTANGLES count=0` (در فایل هیچ قاب با style دقیق `thick` نیست)؛ `BORDER_SIDE_STYLE_COUNTS` در transcript همهٔ borderها را با مختصات نگه می‌دارد؛ `COLOR_CELLS_PRINTED=1656`؛ `THICK_BORDER_CELLS_COUNT=0`؛ `CANDIDATE_REVIEW_STATUS=REVIEW_READY`.

Audit fillها را مستقیماً از artifact شمرد: 17 سلول `RED_TITLE`، 15 `GREEN_SUBTABLE_MARKER`، 459 `GRAY_POSITIVE`، 489 `BLACK_THEME` (theme=1)، 178 `YELLOW_OPTIONAL`، 96 `BLUE_HEADER` با RGB `FF0197C8` و 4 fill آبی دیگر با RGB `FF0070C0`. عدد سیاه واقعی روی workbook فعلی 489 است؛ عدد تاریخی 492 و انتظار 60 span به‌عنوان invariant استفاده نشده‌اند. transcript کامل رنگ/فونت/مختصات، border-sideها و merged ranges در `template_annotation_audit_parsian_current.txt` است.

### Candidate geometry and ownership

`parsian_template_candidate_register.json` منبع ماشینیِ 17 parent bounds و 15 green-row partition است. `parsian_template_candidate_audit_current.json` همان‌ها را روی workbook و hash فعلی تطبیق می‌دهد و برای هر parent محدودهٔ A1، ستون شروع/پایان، header candidate و پیوستگی چهار ضلع را گزارش می‌کند. برای هر child، مختصات دقیق، column range مشتق از candidate parent، marker سبز و رابطهٔ پیشنهادی `PARENT_HEADER_CANDIDATE` با header محدد همان parent را ثبت می‌کند. این رابطه و bounds همچنان **candidate** هستند و مالک آن‌ها را approved نکرده است.

بررسی ماشینی: 17 parent و 15 partition؛ هر 17 قاب candidate چهار ضلع پیوستهٔ `medium` دارند؛ هیچ overlap بین parentها یا sibling partitionها دیده نشد؛ هر 459 gray-positive cell دقیقاً یک owner دارد؛ `unowned_gray_cells=[]` و `duplicate_ownership=[]`. Parent owner فقط gray cells داخل parent ولی خارج از child ranges را می‌گیرد؛ child فقط gray cells داخل partition خودش را می‌گیرد. این مالکیت، semantic mapping نیست.

### Deterministic matcher and tests

Matcher عمومی و بدون اثر جانبی در `src/ingestion/excel/deterministic_matcher.py` اضافه شد. Matcher فقط template نسخه‌دار و صریحاً approved را می‌پذیرد؛ worksheet identity، title/header text و partition marker را به‌صورت exact/fixed بررسی می‌کند؛ template/hash ورودی را در نتیجه ثبت می‌کند؛ ambiguity، coordinate drift، overlap در owned ranges، bounds نامعتبر یا fingerprint نامنطبق را fail-closed رد می‌کند. هیچ رنگ/Borderی در runtime matching به کار نمی‌رود. تست‌ها fixture مصنوعی دارند و matcher به workbook Parsian وصل یا با candidateهای آن اجرا نشده است، چون approval لازم موجود نیست.

فرمان تست ایزوله: `.\.venv\Scripts\python.exe -m pytest -q --basetemp .pytest_task033_matching_20261120 src/tests/test_excel_template_matching.py` — **7 passed in 1.08s**. سناریوها: match دقیق و trace hashها، template تأییدنشده، anchor مبهم، fingerprint نامنطبق، overlap مالکیت، partition خارج parent، و تغییر template hash.

### Status and gates

Task 033 / DB-ING-006 همچنان **PARTIAL** است. این اجرا gateهای hash جاری، audit کامل فایل، و ماشینی‌کردن کنترل overlap/ownership را بست. تأیید مالک برای تمام 17 bounds و 15 partition و header inheritance، workbook مستقل دورهٔ بعد برای drift، semantic approvalهای Metric/currency/scale/period/duration_basis و پیاده‌سازی writer transactional همچنان بازند. هیچ mapping پیشنهادی به mapping اجرایی تبدیل نشد؛ هیچ observation کاننیکال نوشته نشد. Excel-to-canonical persistence هنوز **آماده نیست**. مسیر PDF/Raw، legacy schema، ORM، schema، migration و دیتابیس واقعی دست‌نخورده ماندند.

یادداشت اجرا: فراخوانی مستقیم `python src/scripts/...` به علت `ModuleNotFoundError: src` شکست خورد؛ فراخوانی module بدون `PYTHONIOENCODING=utf-8` نیز هنگام چاپ متن فارسی با `UnicodeEncodeError` متوقف شد. اجرای نهایی بالا هر دو مشکل invocation/encoding را رفع کرد و audit کامل را با exit code صفر تولید کرد.

Regression run after the initial focused matcher run: `.\.venv\Scripts\python.exe -m pytest -q --basetemp .pytest_task033_final_verify_20261120 src/tests/test_excel_template_matching.py src/tests/test_excel_source_reader.py src/tests/test_excel_observation_dto.py` — **37 passed in 1.36s**, exit code 0.
