# DB-DES-007A — Python DTO Design for Excel Source Observations

**Date:** 2026-11-15  
**Status:** DESIGN COMPLETE — implementation and user-run validation remain open.  
**Related contracts:** `DB_DES_007_EXCEL_SOURCE_OBSERVATION_DTO_CONTRACT.md`, `DB_AUD_008_EXCEL_LIBRARY_CAPABILITY_ASSESSMENT.md`, DB-DES-006.  
**Scope:** Concrete Python representation of transient Excel observations for CODAL ingestion V1. This is a design specification, not production code, ORM schema, persistence model, or migration.

## 1. Design decisions

1. Use Python 3.12 standard-library `dataclasses`, `enum.StrEnum`, and immutable `tuple` collections for the first DTO implementation. Do not add Pydantic or another runtime dependency for this boundary.
2. DTO instances are immutable snapshots: `@dataclass(frozen=True, slots=True)`. Nested collections must also be immutable tuples; do not place mutable lists/dicts inside frozen objects.
3. Separate **reader observations** from **interpretation candidates**. The reader reports literal structure and values; it does not assign FinancialMetric, dimensions, FinancialPeriod, report type, audit/restatement rank, or in-scope status.
4. Use stable, explicit identifiers within one observation envelope: worksheet ordinal, table ordinal, row number, column number, and A1 cell coordinate. These are transient references only.
5. Store literal source strings unchanged. Optional normalized helper text is separate and never replaces the literal.
6. Preserve the original numeric OOXML `<v>` token as a string when present. The adapter does not convert it to Decimal, round it, or normalize its lexical form.
7. Keep the source artifact bytes immutable for the duration of both openpyxl passes and the OOXML sidecar pass. Compute SHA-256 once over those exact bytes.
8. Use openpyxl normal mode as the primary workbook model. A read-only OOXML sidecar supplies numeric tokens only; it is not a second workbook interpretation engine.
9. The DTO is transient and must never be persisted as raw rows/cells. Only the later canonical ingestion contract controls persistence.

## 2. Module boundary

Proposed module layout (names are design targets, not files created in this task):

```text
src/ingestion/excel/
    __init__.py
    dto.py             # immutable observation types and enums
    reader.py          # openpyxl normal-mode observation
    ooxml_tokens.py    # narrow numeric <v> token extraction
    diagnostics.py     # stable diagnostic codes/helpers
    table_regions.py   # table-region candidate detection, separate from reader
```

The reader returns a `WorkbookObservation`. It does not return canonical facts or a fully interpreted `ValueCandidate`.

## 3. Type model

The following is the normative shape. Field names may be adjusted during implementation only if semantic distinctions and invariants are preserved.

### 3.1 Primitive identifiers and ranges

- `WorksheetId`: worksheet ordinal, 1-based, stable only within this workbook observation.
- `TableId`: worksheet ordinal + table ordinal, 1-based.
- `CellRef`: worksheet ordinal + A1 coordinate; row/column numeric indices are also retained.
- `CellRange`: inclusive 1-based min/max row and column plus the original A1 range string when available.
- `WorkbookDateSystem`: `WINDOWS_1900`, `MAC_1904`, or `UNKNOWN`.
- `WorksheetVisibility`: `VISIBLE`, `HIDDEN`, `VERY_HIDDEN`, `UNKNOWN`.
- `StructureStatus`: `RESOLVED`, `CANDIDATE`, `AMBIGUOUS`, `UNSUPPORTED`.

Do not use worksheet names as unique IDs; names are literal evidence and can be duplicated/renamed across different workbooks.

### 3.2 Value and formula states

`ObservedValueKind` must distinguish at least:

- `PRESENT_NUMERIC`
- `PRESENT_TEXT`
- `PRESENT_BOOLEAN`
- `PRESENT_DATE_OR_TIME`
- `BLANK`
- `FORMULA_CACHED_NUMERIC`
- `FORMULA_CACHED_TEXT`
- `FORMULA_CACHED_OTHER`
- `FORMULA_NO_CACHE`
- `ERROR_VALUE`
- `UNSUPPORTED_OR_UNREADABLE`

A numeric zero remains `PRESENT_NUMERIC` with a numeric token/value equal to zero; it is never represented as blank. Formula status is orthogonal metadata and must not be collapsed into an ordinary numeric state.

### 3.3 Header axes

Represent each header fragment independently:

- `GROUP`
- `MEASURE`
- `TEMPORAL`
- `PRESENTATION`
- `ROW_LABEL`
- `UNIT_OR_BASIS`
- `UNCLASSIFIED`

The adapter does not decide that a fragment is economically a measure or period. The axis designation at this boundary means a structural observation bucket supplied by a deterministic structural parser or left `UNCLASSIFIED`; semantic interpretation remains later. Each fragment carries literal text, source cell references/ranges, level/order, explicit/inherited/blank state, and merge anchor reference where applicable.

Do not construct one flattened header string as the canonical representation.

## 4. Normative DTO objects

### 4.1 `SourceArtifactObservation`

Fields:
- `source_ref: str | None` — caller-supplied reference, not assumed to be a path.
- `file_name: str | None` — display-only literal name.
- `format: str` — detected workbook format.
- `sha256: str` — hash of immutable input bytes.
- `byte_length: int`.

Invariant: the hash is calculated from the exact bytes used for all reader passes. A filename is not issuer identity or report revision identity.

### 4.2 `ReaderProvenance`

Fields:
- `reader_name: str` — `openpyxl`.
- `reader_version: str`.
- `profile_name: str` — selected V1 profile identifier.
- `profile_version: str`.
- `dto_schema_version: str`.
- `ooxml_token_reader_version: str`.

Invariant: the reader and profile versions are explicit so identical bytes parsed under different implementations can be distinguished.

### 4.3 `WorkbookMetadataObservation`

Fields:
- `date_system: WorkbookDateSystem`.
- `calculation_mode: str | None`.
- `workbook_properties: tuple[MetadataItem, ...]` for selected, non-sensitive workbook properties only.
- `unsupported_features: tuple[Diagnostic, ...]`.

Do not infer report period, fiscal year, issuer, or publication date from workbook properties.

### 4.4 `WorksheetObservation`

Fields:
- `worksheet_id`, `ordinal`, `literal_name`, `visibility`.
- `used_range: CellRange | None`.
- `merged_ranges: tuple[CellRange, ...]`.
- `declared_tables: tuple[DeclaredTableObservation, ...]`.
- `candidate_table_ids: tuple[TableId, ...]`.
- `diagnostics: tuple[Diagnostic, ...]`.
- `ooxml_part_ref: str | None` — transient internal package-part locator used only to align numeric tokens; never exposed as business identity or persisted.

Invariant: hidden/very-hidden worksheets remain in the observation. Exclusion is a later, explicit, versioned interpretation decision.

### 4.5 `TableObservation`

Fields:
- `table_id`, `worksheet_id`, `bounds: CellRange`.
- `detection_method: str`, `detection_version: str`.
- `status: StructureStatus`.
- `title_fragments: tuple[HeaderFragmentObservation, ...]`.
- `header_rows: tuple[RowObservationRef, ...]`.
- `header_columns: tuple[ColumnObservationRef, ...]`.
- `row_refs: tuple[RowObservationRef, ...]`.
- `column_refs: tuple[ColumnObservationRef, ...]`.
- `diagnostics: tuple[Diagnostic, ...]`.

A declared Excel structured table and a visually inferred financial table are different observations. The DTO must preserve that distinction. A worksheet may have multiple disjoint table candidates; unresolved boundaries remain `AMBIGUOUS`, not guessed.

### 4.6 `HeaderFragmentObservation` and `HeaderAxisObservation`

`HeaderFragmentObservation` fields:
- `literal_text: str | None`.
- `source_cells: tuple[CellRef, ...]`.
- `level: int`.
- `presence: EXPLICIT | MERGED_INHERITED | BLANK | UNRESOLVED`.
- `merge_anchor: CellRef | None`.
- `axis: GROUP | MEASURE | TEMPORAL | PRESENTATION | ROW_LABEL | UNIT_OR_BASIS | UNCLASSIFIED`.

`HeaderAxisObservation` fields:
- `axis`.
- `fragments: tuple[HeaderFragmentObservation, ...]`.
- `parent_axis_ref: str | None` only for structural relationships; it is not a semantic parent Metric.

A fragment may be inherited from a merged anchor. Preserve the anchor reference and do not copy inherited text as if it were explicitly present in every cell.

### 4.7 `RowObservation` and `ColumnObservation`

`RowObservation` fields:
- `worksheet_id`, `row_index`.
- `label_fragments: tuple[HeaderFragmentObservation, ...]`.
- `parent_row_index: int | None`.
- `outline_level: int | None`.
- `cell_refs: tuple[CellRef, ...]`.
- `diagnostics: tuple[Diagnostic, ...]`.

`ColumnObservation` fields:
- `worksheet_id`, `column_index`.
- `header_axes: tuple[HeaderAxisObservation, ...]`.
- `cell_refs: tuple[CellRef, ...]`.
- `diagnostics: tuple[Diagnostic, ...]`.

Indentation, outline level, style, and position are observations only; they do not assign detail/subtotal/total/stock/flow/forecast semantics.

### 4.8 `CellObservation`

Fields:
- `cell_ref: CellRef`.
- `value_kind: ObservedValueKind`.
- `data_type: str` — literal library data type code.
- `observed_value: str | int | float | bool | date | datetime | time | timedelta | None`.
- `formula_expression: str | None`.
- `formula_cache_present: bool | None`.
- `formula_cached_value: same scalar union | None`.
- `numeric_xml_token: str | None`.
- `number_format: str | None`.
- `style_id: int | None`.
- `merged_range: CellRange | None`.
- `merged_anchor: CellRef | None`.
- `diagnostics: tuple[Diagnostic, ...]`.

Invariants:
- `numeric_xml_token` is populated only when the source cell has an OOXML numeric `<v>` token; preserve the exact token string.
- The token is not parsed, rounded, or rewritten in the reader.
- A cell with formula and no usable cached result is `FORMULA_NO_CACHE`; do not substitute zero or evaluate the formula.
- Blank cells are included only when needed to explain a candidate region/header/merged range; do not materialize every empty cell in the worksheet.
- Error cells remain errors; they are not converted to text or NULL.

### 4.9 `Diagnostic`

Fields:
- `code: str` — stable machine-readable code.
- `severity: INFO | WARNING | ERROR`.
- `message: str` — concise diagnostic text, no full financial row payload.
- `worksheet_id: WorksheetId | None`.
- `table_id: TableId | None`.
- `cell_ref: CellRef | None`.
- `details: tuple[DiagnosticDetail, ...]` — scalar, non-sensitive details only.

Diagnostic codes should be stable and versioned. Do not make the message string itself the programmatic contract.

### 4.10 `WorkbookObservation`

Fields:
- `source: SourceArtifactObservation`.
- `reader: ReaderProvenance`.
- `metadata: WorkbookMetadataObservation`.
- `worksheets: tuple[WorksheetObservation, ...]`.
- `tables: tuple[TableObservation, ...]`.
- `rows: tuple[RowObservation, ...]`.
- `columns: tuple[ColumnObservation, ...]`.
- `cells: tuple[CellObservation, ...]`.
- `diagnostics: tuple[Diagnostic, ...]`.

Invariant: one immutable envelope describes exactly one immutable source byte sequence and one reader/profile version. It contains no canonical IDs or persistence objects.

## 5. OOXML numeric-token sidecar contract

The sidecar is deliberately narrow:

1. Open the same immutable XLSX bytes as a ZIP package in read-only mode.
2. Resolve worksheet names to OOXML worksheet part paths using workbook relationships; do not assume `sheet1.xml` corresponds to the first visible sheet.
3. For each worksheet cell element with a numeric value token (`<v>` and numeric cell type, including cells whose type attribute is omitted), record the exact text token keyed by worksheet part + A1 coordinate.
4. Preserve the token exactly; no Decimal conversion, locale parsing, rounding, or trailing-zero trimming occurs here.
5. Align sidecar tokens with openpyxl cell observations using worksheet identity and cell coordinate.
6. If a token cannot be aligned, emit an explicit diagnostic. Do not silently fall back to float for canonical financial parsing.
7. Formula cached numeric values may also have a numeric `<v>`; preserve that token separately from the formula expression and formula-cache-presence state.
8. Do not copy complete worksheet XML, all raw cells, or source rows into persistent storage.

This sidecar must use public ZIP/XML APIs and avoid openpyxl private internals. OOXML package relationship resolution is required to support arbitrary sheet ordering/names.

## 6. Interpretation boundary

A later interpretation layer may construct a `ValueCandidate` that references:
- source `CellObservation`;
- row and column observations;
- table and worksheet observations;
- relevant title/caption/footnote fragments;
- unresolved temporal and presentation evidence;
- diagnostics.

It must not place `metric_id`, `period_id`, canonical unit, dimension IDs, or final Actual/Forecast status into the reader DTO. These are assigned only by approved versioned interpretation rules.

## 7. Memory and determinism

- Keep only non-empty cells plus structurally relevant blanks; avoid dense materialization of large sparse ranges.
- Use tuples for stable ordered collections. Sort observations by worksheet ordinal, then row, then column.
- Repeated loads of identical bytes with the same reader/profile version must produce identical DTO projections, excluding explicitly volatile timing metrics (which do not belong in the DTO).
- Do not store Python object identity, memory addresses, temporary paths, or timestamps generated during parsing as DTO identity.
- The large-sheet benchmark is environment-specific and does not define a universal row/cell limit. The implementation must expose a configurable safety limit and fail explicitly if exceeded; the actual default is a separate implementation decision backed by owner-run measurements.

## 8. Error and admission behavior

Reader-level fatal failures:
- corrupt/unreadable workbook package;
- unsupported encryption or file format;
- worksheet relationship/package inconsistency;
- inability to align required formula/cache or numeric token observations;
- resource safety limit exceeded;
- unsupported content that prevents reliable structural observation.

Non-fatal diagnostics:
- hidden sheet/row/column observation;
- ambiguous table boundary candidate;
- unknown but preserved cell data type;
- numeric XML token unavailable for a non-financial or non-numeric cell.

Whether a candidate is in-scope and whether the whole report must be rejected are interpretation/admission decisions under DB-DES-006 and DB-DES-005, not reader decisions.

## 9. Explicit non-goals

- No ORM, SQLAlchemy model, DB table, migration, or persistence DTO.
- No PDF support.
- No fuzzy Header/Metric matching or semantic period inference.
- No permanent raw workbook/cell/row archive.
- No formula calculation or external-link resolution.
- No full Excel calculation engine, macro execution, or workbook editing.
- No table-detection algorithm approval in this design.
- No assumption that five reported source workbooks represent every issuer/workbook variant.

## 10. Acceptance criteria for implementation

1. DTO classes are immutable and use immutable nested collections.
2. Worksheet order/name/visibility/used-range/merged-range metadata are preserved.
3. Multiple table candidates per worksheet are supported without workbook-wide period defaults.
4. Header fragments remain orthogonal across group, measure, temporal, presentation, row-label, and unit/basis axes.
5. Row and column contexts are independent and source references remain traceable during the run.
6. Cell states distinguish blank, explicit zero, text, numeric, errors, formulas with cache, and formulas without cache.
7. Formula and cached-value observations are aligned by worksheet and coordinate using the same immutable bytes.
8. Original numeric XML tokens are preserved exactly and can be aligned with the openpyxl observations.
9. Jalali period, Metric, unit, currency, dimensions, report type, issuer identity, and scope are not inferred by the reader.
10. The observation envelope is deterministic for identical bytes and reader/profile versions.
11. DTOs and raw observations are not persisted.
12. User-run tests cover source-shaped synthetic fixtures, malformed files, sparse/large sheets, and failure/diagnostic paths.

## 11. Remaining work

- Implement the DTO types and reader/OOXML sidecar under the separate Excel-ingestion implementation task.
- Implement deterministic table-region candidate detection as a separate component.
- Validate against additional authorized workbook examples and update the evidence matrix when available.
- Add user-run tests; no tests were run as part of this design task.

**Conclusion:** this design converts the logical DB-DES-007 contract into a concrete, dependency-light Python type boundary while preserving the V1 reader profile selected by DB-AUD-008. It is ready for implementation planning, but it does not claim that any Python DTO or adapter exists yet.
