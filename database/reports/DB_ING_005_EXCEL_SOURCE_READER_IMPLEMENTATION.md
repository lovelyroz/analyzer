# DB-ING-005 — Excel Source Reader Implementation

**Date:** 2026-11-15  
**Status:** PARTIAL — first reader implementation and owner-run test definitions are present; owner validation remains pending.  
**Task:** 032  
**Related:** DB-ING-004 / Task 031; DB-DES-007; DB-AUD-008; DB-DES-006.

## 1. Scope

Implement the V1 read-only adapter that converts one immutable XLSX byte sequence into the transient DTO envelope defined by DB-ING-004. The source contract is text-only: every populated cell must be literal text, with blanks kept distinct. The reader must not interpret financial meaning.

Implemented files:

- `src/ingestion/excel/reader.py`
- `src/ingestion/excel/__init__.py`
- `src/tests/test_excel_source_reader.py`

No ORM, schema, migration, database data, canonical writer, or persistence behavior was changed.

## 2. Public API

- `read_excel_source(source, *, source_ref=None, file_name=None, config=None)`
  - Accepts immutable bytes-like input or a filesystem path.
  - Reads one `.xlsx` source.
  - Returns a `WorkbookObservation` when the text-only contract is satisfied.
  - Raises `ExcelSourceContractError` for populated non-text/error cells. The exception exposes the complete `observation`, including every violation and its cell coordinate, so the caller can reject the entire report.
  - Raises `ExcelSourceReadError` for invalid packages, unsupported extensions, unreadable workbooks, and resource-limit violations.
- `read_excel_file(path, ...)`: path-oriented convenience wrapper.
- `ExcelReaderConfig`: explicit resource/provenance configuration.

The public API and exception/configuration types are exported from `src/ingestion/excel/__init__.py`.

## 3. Reader behavior

### 3.1 Source identity and provenance

- Reads path input as bytes once; byte input is copied to immutable `bytes`.
- Computes SHA-256 over the exact bytes passed to the reader.
- Records byte length, optional source reference, optional filename, reader package version, profile name/version, and DTO schema version.
- Accepts `.xlsx` only; it does not resolve external links or execute workbook content.

### 3.2 Workbook and worksheet structure

- Uses openpyxl normal mode with `read_only=False`, `data_only=False`, and `keep_links=False`.
- Preserves worksheet order, literal names, visibility state, merged ranges, workbook date-system metadata, and selected workbook properties.
- Computes a bounded used range from populated/styled cells and merged-range bounds.
- Produces ordered row and column observations with references to observed cells.
- Preserves sparse cell observations: ordinary unstyled empty cells are not materialized; blank cells inside merged ranges and styled blank cells are retained as structurally relevant blanks.
- Declared Excel structured tables are represented as resolved table observations, including bounds and header-row presence.

### 3.3 Text-only enforcement

- Literal string cells are copied exactly to `text_value`; no trimming, digit conversion, separator normalization, parsing, date conversion, or unit conversion occurs.
- Blank cells remain `BLANK`; no blank is converted to empty text or zero.
- Numeric, boolean, date-typed, formula, and other populated non-text cells are retained as `UNEXPECTED_NON_TEXT` with an error diagnostic.
- Excel error cells are retained as `ERROR_VALUE` with their literal error token and an error diagnostic.
- The reader scans the workbook and collects all violations before raising one `ExcelSourceContractError`. The attached observation is diagnostic evidence only; it is not an accepted report and must not be persisted.
- No formula evaluation or cached-value fallback exists.

Stable diagnostic codes currently implemented:

- `EXCEL_TEXT_ONLY_NON_TEXT_CELL`
- `EXCEL_TEXT_ONLY_ERROR_CELL`

Stable fatal read codes include:

- `EXCEL_INVALID_PACKAGE`
- `EXCEL_UNSUPPORTED_EXTENSION`
- `EXCEL_WORKBOOK_UNREADABLE`
- `EXCEL_WORKBOOK_STRUCTURE_UNREADABLE`
- `EXCEL_FILE_SIZE_LIMIT_EXCEEDED`
- `EXCEL_UNCOMPRESSED_SIZE_LIMIT_EXCEEDED`
- `EXCEL_PACKAGE_MEMBER_LIMIT_EXCEEDED`
- `EXCEL_WORKSHEET_LIMIT_EXCEEDED`
- `EXCEL_CELL_SCAN_LIMIT_EXCEEDED`

## 4. Resource guardrails

Default `ExcelReaderConfig` limits:

| Limit | Default |
|---|---:|
| Compressed source file | 25 MiB |
| Sum of worksheet rectangular scan areas | 500,000 cells |
| Worksheet count | 100 |
| XLSX ZIP member count | 10,000 |
| Uncompressed package size | 250 MiB |

The first three reader limits are configurable through `ExcelReaderConfig`. ZIP package member and uncompressed-size limits are fixed defensive preflight bounds in this increment.

These values are provisional safety guardrails, not measured capacity guarantees. The largest workbook range documented in the current Markdown evidence is approximately 22.7k cells; the owner-run synthetic benchmark covered 120,006 non-empty cells in a six-column sheet. The 500,000 rectangular-cell default provides headroom over those observations, but the actual source XLSX files have not been directly inspected by the assistant. Resource limits must be revisited if representative owner-run source workbooks exceed them.

## 5. Table-region boundary

This increment recognizes **explicit Excel structured tables only**. It does not attempt to infer visual financial table regions from blank rows, merged headings, styles, borders, or text patterns.

The five Markdown-audited source examples contain multiple independent visual tables within a worksheet and do not report structured Excel tables. Therefore, treating a whole used range as one financial table would be incorrect, while inventing segmentation rules without direct source evidence would be unsafe.

Visual table-region candidate detection is deliberately separated into **DB-ING-006 / Task 033**. That task must use deterministic conservative evidence, preserve ambiguous boundaries, and must not assign financial semantics. Until it is implemented, the reader's `tables` collection contains only declared structured tables; the worksheet used range is not represented as a financial table.

## 6. Owner-run tests

Added `src/tests/test_excel_source_reader.py` covering:

- exact Persian text and source fingerprint;
- worksheet order, visibility, merged ranges, and used-range bounds;
- blank merged cells and sparse blank handling;
- numeric, boolean, formula, and Excel error rejection;
- collection of multiple violations before whole-workbook rejection;
- deterministic repeated observations from identical bytes;
- malformed package rejection;
- configurable cell-scan limit;
- declared structured-table observation.

The assistant did not execute tests. Owner command:

```powershell
pytest src/tests/test_excel_source_reader.py -q
```

The existing DTO test module remains:

```powershell
pytest src/tests/test_excel_observation_dto.py -q
```

## 7. Acceptance status

| Requirement | Status |
|---|---|
| Read-only openpyxl normal-mode XLSX reader | Implemented |
| Source SHA-256 and reader provenance | Implemented |
| Worksheet order/name/visibility and merged ranges | Implemented |
| Sparse exact-text cell observations | Implemented |
| Explicit relevant blank observations | Implemented |
| Whole-file text-only rejection with all cell diagnostics | Implemented |
| Declared structured Excel table observations | Implemented |
| Visual financial table-region segmentation | Deferred to Task 033 |
| Owner-run tests | Authored; execution pending |
| Direct source-XLSX validation | Not performed by assistant; owner workflow/evidence required |

**Current Task 032 status: PARTIAL.** Do not mark complete until the owner-run reader tests pass and any failures are resolved. Task 033 is the next independent increment for visual table-region detection.

No tests were run by the assistant. No dependency was installed or changed. No ORM/schema/migration/data was modified.


## 7. Owner-run validation result and corrective change (2026-11-15)

The owner ran the combined command:

```powershell
pytest src/tests/test_excel_observation_dto.py src/tests/test_excel_source_reader.py -q
```

Result: **21 passed, 5 failed**. All five failures shared one root cause: `DiagnosticSeverity` was referenced while creating non-text/error diagnostics in `reader.py`, but the enum had not been imported from the DTO module. This raised `NameError` before the intended whole-workbook contract exception could be constructed; the tests therefore exposed a real implementation defect in the rejection/diagnostic path, not five independent behavioral defects.

**Correction applied:** added the missing `DiagnosticSeverity` import to `src/ingestion/excel/reader.py`. No behavior or contract was otherwise changed. Task 032 remains PARTIAL until the owner reruns the same combined command and reports a clean result. The assistant did not execute tests.
