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
