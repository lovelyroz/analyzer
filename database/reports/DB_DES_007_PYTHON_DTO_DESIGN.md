> **Historical reference/status as of 2026-11-21:** Any PDF extraction implementation, test command, corpus, or pre-retirement status described here is superseded. Excel/CSV are the supported file inputs, and CODAL PDF extraction is retired. See database/reports/DB_CODAL_RETIRE_001_EXCEL_CSV_ONLY_RETIREMENT.md.

# DB-DES-007A — Python DTO Design for Excel Source Observations

**Date:** 2026-11-15  
**Status:** DTO runtime types and the openpyxl structural/text reader are implemented and owner-run validated; visual table-region detection remains open.  
**Related contracts:** `DB_DES_007_EXCEL_SOURCE_OBSERVATION_DTO_CONTRACT.md`, `DB_AUD_008_EXCEL_LIBRARY_CAPABILITY_ASSESSMENT.md`, DB-DES-006.  
**Scope:** Transient CODAL Excel observations V1. This is not an ORM model, persistence schema, or migration.

## 1. Owner-confirmed source contract

The owner confirms that the XLSX input files contain no formulas and that all populated cells are text-only. This is a normative V1 input constraint.

- Every populated cell must be a literal text cell.
- Blank cells remain blank; blank is not zero and is not an empty string.
- Numeric-looking strings, dates, Persian digits, separators, and units remain exactly as source text.
- The reader performs no digit normalization, trimming, locale parsing, Decimal parsing, date conversion, unit conversion, or formula evaluation.
- Any populated non-text cell, formula cell, or Excel error cell violates the contract and must produce a deterministic error diagnostic. Never coerce it to text.
- Numeric/date interpretation occurs downstream under approved, versioned rules.
- A future workbook format with numeric-typed cells or formulas requires an explicit contract revision and new evidence.

Consequently, formula/cache DTO fields and the OOXML numeric-token sidecar are not part of V1. The text cell itself is the authoritative lexical source.

## 2. Implementation decisions

1. Use Python 3.12 standard-library `dataclasses`, `enum.StrEnum`, and immutable tuples. No Pydantic or additional dependency.
2. DTOs are immutable snapshots: `@dataclass(frozen=True, slots=True)`.
3. Keep reader observations separate from semantic interpretation. The reader does not assign company, industry, ReportType, Standard Database Header, Metric, dimensions, FinancialPeriod, audit/restatement rank, Actual/Forecast/Plan, or scope.
4. Preserve literal worksheet names, source text, merged ranges, cell coordinates, and row/column context.
5. Use 1-based worksheet, row, column, and table ordinals; A1 coordinates are also retained.
6. Keep the source bytes immutable during reading and compute SHA-256 over those exact bytes.
7. Use openpyxl normal mode. Do not add a second XML value parser.
8. DTOs and raw observations are transient; never persist raw worksheet rows/cells.

## 3. Module boundary

Implemented:
```text
src/ingestion/excel/
    __init__.py
    dto.py
```

Planned:
```text
src/ingestion/excel/
    reader.py          # openpyxl normal-mode structural/text observation
    diagnostics.py     # stable diagnostic codes/helpers
    table_regions.py  # deterministic candidate table-region detection
```

The reader returns one `WorkbookObservation`. It does not return canonical facts or fully interpreted `ValueCandidate` objects.

## 4. Type model

### 4.1 Enums

- `WorkbookDateSystem`: `WINDOWS_1900`, `MAC_1904`, `UNKNOWN` (metadata only; never used to interpret text values).
- `WorksheetVisibility`: `VISIBLE`, `HIDDEN`, `VERY_HIDDEN`, `UNKNOWN`.
- `StructureStatus`: `RESOLVED`, `CANDIDATE`, `AMBIGUOUS`, `UNSUPPORTED`.
- `CellValueKind`: `PRESENT_TEXT`, `BLANK`, `UNEXPECTED_NON_TEXT`, `ERROR_VALUE`.
- `HeaderAxisKind`: `GROUP`, `MEASURE`, `TEMPORAL`, `PRESENTATION`, `ROW_LABEL`, `UNIT_OR_BASIS`, `UNCLASSIFIED`.
- `FragmentPresence`: `EXPLICIT`, `MERGED_INHERITED`, `BLANK`, `UNRESOLVED`.
- `DiagnosticSeverity`: `INFO`, `WARNING`, `ERROR`.

### 4.2 Primitive references and ranges

- `CellRef`: worksheet ordinal, A1 coordinate, 1-based row index, 1-based column index.
- `CellRange`: inclusive 1-based min/max row and column plus optional original A1 range.
- `TableObservation` is identified by worksheet ordinal + table ordinal.
- Worksheet names are literal evidence, not stable identifiers across workbooks.

### 4.3 Source and reader provenance

`SourceArtifactObservation` carries caller reference, display filename, format, SHA-256, and byte length. Filename is not issuer identity or revision identity.

`ReaderProvenance` carries reader name/version, profile name/version, and DTO schema version. No OOXML token-reader version exists in V1.

### 4.4 Workbook and worksheet

`WorkbookMetadataObservation` contains optional non-semantic workbook metadata and diagnostics. It must not infer issuer, report period, fiscal year, or publication date.

`WorksheetObservation` preserves ordinal, literal name, visibility, used range, merged ranges, declared Excel tables, table candidate ordinals, and diagnostics. Hidden and very-hidden worksheets remain observable; exclusion is a later explicit rule.

### 4.5 Table and header observations

`TableObservation` preserves worksheet/table identity, bounds, detection method/version, structural status, title fragments, header rows/columns, row/column references, and diagnostics.

A declared Excel structured table and a visually inferred financial table are distinct observations. A worksheet may contain multiple independent table candidates. Ambiguous boundaries remain ambiguous; never guess.

Each `HeaderFragmentObservation` preserves literal text, source cell references, hierarchy level, explicit/inherited/blank/unresolved state, merge anchor, and axis. `HeaderAxisObservation` groups fragments along one independent axis.

The independent axes are:
- group hierarchy;
- measure hierarchy;
- temporal hierarchy;
- presentation qualifiers;
- row-label hierarchy;
- unit/basis clues.

Do not irreversibly flatten these into one header string. Structural axis assignment is not final financial interpretation.

### 4.6 Row and column observations

`RowObservation` preserves worksheet ordinal, row index, label fragments, parent row, outline level, cell references, and diagnostics.

`ColumnObservation` preserves worksheet ordinal, column index, header axes, cell references, and diagnostics.

Indentation, style, position, and outline level are structural evidence only. They do not classify detail/subtotal/total, stock/flow, rate, forecast, or other financial semantics.

### 4.7 Cell observation — text-only

`CellObservation` carries:
- `cell_ref`;
- `value_kind`;
- literal openpyxl `data_type`;
- `text_value` only for `PRESENT_TEXT`;
- `unexpected_value` only when a populated non-text value violates the contract;
- merged-range and merged-anchor references;
- diagnostics.

Rules:
- Preserve source text exactly, including whitespace, Persian/Arabic digits, punctuation, separators, and signs.
- Never turn a numeric, boolean, date-typed, formula, or error cell into a string to make it pass.
- Formula cells are `UNEXPECTED_NON_TEXT` and cause an error diagnostic; there is no formula/cache state in this DTO.
- Error cells use `ERROR_VALUE` and preserve their error token for diagnostics.
- Blank cells are materialized only where structurally relevant; do not create every empty cell in a sparse range.

### 4.8 Diagnostics

`Diagnostic` carries stable code, severity, concise message, optional worksheet/table/cell reference, and immutable scalar details. Programmatic behavior depends on the code, not message wording.

### 4.9 Workbook envelope

`WorkbookObservation` contains source artifact, reader provenance, workbook metadata, ordered worksheets, tables, rows, columns, cells, and diagnostics.

One envelope describes exactly one immutable source byte sequence and one reader/profile version. It contains no canonical IDs or persistence objects.

## 5. Interpretation boundary

A later interpretation layer may construct a `ValueCandidate` referencing the source cell, row, column, table, worksheet, captions/footnotes, temporal evidence, presentation evidence, and diagnostics.

It must not assign Metric, dimensions, canonical unit, currency, FinancialPeriod, ReportType, issuer identity, or scope inside the reader DTO. These are resolved only by approved, versioned interpretation rules.

Text-to-number/date parsing is downstream. Numeric-looking strings are not automatically numeric merely because their characters resemble digits. The interpretation layer uses the approved Jalali/date and Decimal parsing rules, validates unit/basis, and applies canonical rounding exactly once at persistence validation.

## 6. Determinism, memory, and failure behavior

- Use immutable tuples and stable ordering by worksheet ordinal, row, and column.
- Identical source bytes and reader/profile versions must yield identical DTO projections, excluding runtime timing metrics (which do not belong in the DTO).
- Keep non-empty cells plus structurally relevant blanks; avoid dense materialization.
- Expose a configurable resource safety limit and fail explicitly if exceeded; choose its default from owner-run measurements.
- Fatal failures include corrupt/unreadable workbook, unsupported encryption/format, invalid worksheet/package structure, resource limit exceeded, or inability to obtain reliable cell structure.
- Any populated non-text/formula/error cell violates the V1 input contract and must produce an error diagnostic. The ingestion admission layer rejects the complete report; it must not silently skip or coerce that cell.
- Ambiguous in-scope table/value meaning remains an interpretation/admission failure under DB-DES-005/006, not a reader guess.

## 7. Explicit non-goals

- No ORM, SQLAlchemy model, DB table, migration, or persistence DTO.
- No PDF support.
- No formula calculation, cached formula values, or OOXML numeric-token extraction.
- No fuzzy Header/Metric matching or semantic period inference.
- No permanent raw workbook/cell/row archive.
- No macros, external-link resolution, or workbook editing.
- No approval of a table-detection algorithm in this design.
- No assumption that the currently documented workbooks represent every issuer/workbook variant.

## 8. Implementation acceptance criteria

1. DTO classes are frozen/slots dataclasses with immutable nested tuples.
2. Worksheet order/name/visibility/used-range/merged-range metadata are preserved.
3. Multiple table candidates per worksheet are supported without workbook-wide period defaults.
4. Header fragments remain orthogonal across group, measure, temporal, presentation, row-label, and unit/basis axes.
5. Row and column contexts remain independent and traceable.
6. Populated text is preserved byte-for-character at the Python string level; blanks remain distinct.
7. Any populated non-text/formula/error cell is diagnosed and rejected without coercion.
8. Jalali period, Metric, unit, currency, dimensions, report type, issuer, and scope are not inferred by the reader.
9. The observation envelope is deterministic for identical bytes and reader/profile versions.
10. DTOs and raw observations are not persisted.
11. Owner-run tests cover text cells, blanks, Persian digits/separators, merged headers, unexpected numeric/formula/error cells, sparse/large sheets, malformed files, and diagnostics.

## 9. Runtime implementation status

The immutable DTO definitions and package exports have been created in:
- `src/ingestion/excel/dto.py`
- `src/ingestion/excel/__init__.py`

The implementation follows the text-only value model and contains no formula/cache fields or numeric XML sidecar. Owner-run tests in `src/tests/test_excel_observation_dto.py` cover literal text, blank/non-text/error states, immutability, tuple-only collections, and worksheet ordering. The owner reported `pytest src/tests/test_excel_observation_dto.py -q` → `13 passed in 2.49s`; the assistant did not run tests. DB-ING-004 / Task 031 is complete. The next implementation increment is DB-ING-005 / Task 032: the openpyxl structural/text reader and deterministic diagnostics, with table-region detection kept conservative and ambiguity explicit.



## 10. Reader implementation increment — DB-ING-005 / Task 032

The first read-only adapter is implemented in `src/ingestion/excel/reader.py` and exported through `src/ingestion/excel/__init__.py`.

- Public entry points: `read_excel_source` and `read_excel_file`.
- Uses openpyxl normal mode over one immutable byte sequence; computes SHA-256 and records reader/profile provenance.
- Captures worksheet order/name/visibility, merged ranges, bounded used ranges, sparse cell observations, row/column references, workbook date-system metadata, and declared structured tables.
- Preserves populated text exactly. Numeric, boolean, date-typed, formula, and error cells are diagnostic contract violations; the reader scans all worksheets and raises `ExcelSourceContractError` with the complete transient observation.
- No numeric/date parsing, normalization, formula execution, semantic mapping, or persistence occurs.
- Configurable defaults are 25 MiB source bytes, 500,000 total rectangular scan cells, and 100 worksheets; package preflight additionally limits ZIP members and uncompressed package size. These are provisional guardrails pending owner-run validation against representative source files.
- Visual financial table segmentation is intentionally not inferred in this reader. Only declared Excel structured tables are resolved; visual table-region detection is a separate next increment.

Owner-run reader tests have been added in `src/tests/test_excel_source_reader.py`; they have not been executed by the assistant. The exact command is `pytest src/tests/test_excel_source_reader.py -q`. Task 032 remains PARTIAL until owner validation passes. See `reports/DB_ING_005_EXCEL_SOURCE_READER_IMPLEMENTATION.md`.


### 10.1 Owner-run validation correction (2026-11-15)

The owner executed the combined DTO/reader suite and reported **21 passed, 5 failed**. All five failures had the same root cause: `DiagnosticSeverity` was used by the reader but missing from its DTO imports, causing a `NameError` when non-text/error diagnostics were constructed. The missing import was added to `src/ingestion/excel/reader.py`. The reader acceptance status remains pending rerun by the owner; the assistant did not execute tests.


### 10.2 Final owner-run validation — Task 032 complete (2026-11-15)

Following the missing `DiagnosticSeverity` import correction, the owner reran the combined DTO/reader test suite and reported **26 passed in 1.35s**. Task 032 / DB-ING-005 is complete. This confirms the tested reader and DTO contracts, but does not implement visual financial table-region detection; that remains the separate Task 033 / DB-ING-006. The assistant did not execute tests.


## 11. Corrected owner intent — literal values, no formulas (2026-11-15)

The previous "text-only" wording was an assistant interpretation error. The owner's intent is not restricted to Excel string-typed cells. Populated source cells may contain literal text or literal numeric values; formulas are prohibited.

The DTO/reader contract therefore distinguishes:
- `PRESENT_TEXT`: exact literal string;
- `PRESENT_NUMBER`: literal numeric int/float as exposed by openpyxl, without stringification, parsing, rounding, or semantic interpretation;
- `BLANK`: no value, distinct from zero and empty text;
- `UNEXPECTED_NON_TEXT` / `ERROR_VALUE`: unsupported kinds or Excel errors, rejected with diagnostics.

Boolean and date-typed values are not accepted by this correction; they remain a separate explicit decision if encountered in an approved input. Formula cells remain rejected. The table detector must treat both PRESENT_TEXT and PRESENT_NUMBER as populated cells, while only text values may be retained as literal header/title fragments.
