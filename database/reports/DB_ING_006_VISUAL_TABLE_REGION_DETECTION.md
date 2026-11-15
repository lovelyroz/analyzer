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
