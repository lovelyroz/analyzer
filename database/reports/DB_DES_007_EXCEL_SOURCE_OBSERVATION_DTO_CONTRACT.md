# DB-DES-007 — Excel Source Observation DTO Contract

**Date:** 2026-11-15  
**Status:** PARTIAL — logical DTO boundary and companion Python DTO design are defined; production implementation, additional source evidence, and user-run validation remain open.  
**Scope:** CODAL Excel ingestion V1. This is a logical contract, not a Python API, ORM model, physical schema, or migration specification.

## 1. Purpose and boundary

Define the information that an Excel adapter must expose to the interpretation layer without prematurely deciding financial meaning. The DTO must preserve enough transient workbook structure to resolve:

- source workbook and worksheet context;
- table boundaries and multi-level row/column headers;
- source Header paths separately from row labels and cell values;
- value candidates and their source temporal context;
- formula/cache status, blankness, numeric representation, and source unit/basis clues;
- structural diagnostics needed to explain an unresolved candidate.

The adapter observes workbook content. It does **not** decide company identity, report type, Standard Database Header, FinancialMetric, approved dimensions, financial period, audit/restatement status, or whether a value is in scope. Those decisions belong to later, versioned interpretation and validation stages.

The DTO is transient and in-memory. It is not a new persistence model and does not authorize raw-row archival.

## 2. Design principles

1. **Structure before semantics:** preserve worksheet/table/row/column relationships; do not flatten a workbook into unrelated label/value pairs.
2. **One workbook, many contexts:** a report may contain multiple tables and multiple actual periods. A workbook-level `period_id` is prohibited as the sole temporal assignment.
3. **Literal source evidence:** preserve source text as observed. Normalized text may be supplied as a separate helper value but must never replace the literal.
4. **No semantic guessing:** the adapter must not infer metric, unit, currency, YTD, standalone quarter, actual/forecast/plan, stock/flow, or out-of-scope status from position or numeric shape.
5. **No formula execution:** use cached formula results only. Never evaluate workbook formulas in the adapter.
6. **No implicit zero:** blank, missing, formula-without-cache, text, numeric zero, and invalid numeric content are distinct states.
7. **No durable cell locator requirement:** coordinates are transient diagnostics, not mandatory persisted fact provenance.
8. **Deterministic parsing:** identical workbook bytes and adapter/profile version should yield the same observation structure.
9. **Whole-file admission:** later interpretation validates every in-scope candidate before any canonical write; unresolved in-scope ambiguity rejects the entire ingestion unit.

## 3. Logical DTO envelope

The adapter returns one immutable logical `WorkbookObservation` envelope containing:

| Component | Required content | Notes |
|---|---|---|
| Source identity | source kind, source identity/reference, SHA-256 content fingerprint, byte length when available | Fingerprint supports replay/audit; it does not alone prove economic revision identity. |
| Adapter provenance | adapter name/version, workbook profile/parser version | Exact versions are captured in run audit. |
| Workbook metadata | workbook format, date system if exposed by library, calculation mode if exposed | Metadata is evidence only; never a substitute for source-reported financial period. |
| Worksheet observations | ordered worksheet list, literal name, visibility/state, stable ordinal | Do not assume fixed sheet names or ignore hidden sheets without an approved rule. |
| Table observations | candidate table regions, structural confidence/status, row/column bounds | Boundaries may be explicit or unresolved; ambiguity must remain explicit. |
| Cell observations | sparse observed cells and relevant blank candidates | No need to materialize every empty cell in a large sheet. |
| Diagnostics | warnings, unsupported feature markers, parse errors | Diagnostics are transient until summarized into IngestionRun. |

The envelope also carries caller-supplied acquisition metadata separately from workbook-derived observations. User-supplied company/ticker/report-type hints are claims to validate, not proof of identity.

## 4. Structural observation DTOs

### 4.1 WorksheetObservation

Required logical attributes:

- worksheet ordinal and literal name;
- visibility/state (visible, hidden, very-hidden, or unknown if the library cannot distinguish);
- used-range bounds as reported by the workbook library;
- merged-cell ranges;
- table regions and structural diagnostics.

Worksheet order is evidence, not a semantic mapping rule. A hidden sheet is not automatically excluded.

### 4.2 TableObservation

A table candidate represents a contiguous or otherwise structurally identified region that may contain one or more financial blocks.

Required attributes:

- transient worksheet reference;
- transient bounding range;
- detection method/version;
- structural status: resolved, candidate, or ambiguous;
- header-band observations;
- row observations and column observations;
- optional title/caption text and nearby context;
- warnings for merged, repeated, nested, or discontinuous structures.

A worksheet may contain multiple tables. A table may have multi-row headers. A visual page heading or wrapper title must not automatically replace the actual table identity.

### 4.3 HeaderPathObservation

For each relevant row/column axis, preserve the ordered hierarchy of literal header fragments, including:

- literal text per level;
- source cell references/ranges (transient);
- merged-cell inheritance relationship, if applicable;
- whether a level is explicit, inherited from a merged cell, blank, or unresolved.

Do not concatenate levels irreversibly. A derived display path may be provided in addition to the individual levels.

Row-axis labels and column-axis headers are distinct. A source Header mapped to a Standard Database Header does not by itself identify the Metric represented by each numeric cell.

### 4.3.1 Orthogonal header axes — evidence-driven refinement

DB-AUD-007 shows that a single linear header path is insufficient as the only representation for complex tables. Preserve these header dimensions independently, while retaining their structural relationships and source references:

- **Group hierarchy:** parent headers grouping one or more leaf columns, whether merged or unmerged.
- **Measure hierarchy:** quantity, rate, amount, count, percentage change, balance, and other literal measure labels.
- **Temporal hierarchy:** date/date-range phrases, fiscal-year labels, cumulative/standalone wording, and comparative qualifiers.
- **Presentation qualifiers:** actual, forecast, plan, correction, restatement, estimate, and other literal qualifiers.
- **Row-axis hierarchy:** row labels, category groups, unit labels, and entity attributes.

A leaf cell may inherit fragments from multiple axes. Keep literal fragments and their source references separate; a derived display path is optional and must not replace the original fragments. Dates found in row-level investee attributes, captions, or footnotes are not automatically column-period descriptors.

Temporal, measure, and presentation evidence are orthogonal. The adapter must not collapse them into one semantic header string or resolve their economic meaning.

### 4.4 RowObservation

Required logical attributes:

- transient row ordinal/range;
- literal row-label fragments and their hierarchy;
- row role only as an observation (e.g. explicit label text, indentation/style hints), not a final economic classification;
- parent/child structural relationship when detectable;
- cells associated with the row;
- optional outline/group level and merged-label context.

The adapter must not classify a row as detail, subtotal, total, summary, forecast, rate, stock, or flow solely from formatting or indentation. Those are interpretation-stage decisions supported by approved rules.

### 4.5 CellObservation

Each relevant cell observation preserves:

- transient coordinate;
- raw cell value/type as exposed by the library;
- literal text where present;
- formula expression where present (diagnostic only);
- cached result and cached-result availability for formula cells;
- number format/style identifier where available;
- blankness/value state;
- merged-cell membership/anchor relationship;
- source row and column observation references.

Logical value states must distinguish at least:

- `PRESENT_NUMERIC`
- `PRESENT_TEXT`
- `BLANK`
- `FORMULA_CACHED_NUMERIC`
- `FORMULA_CACHED_TEXT`
- `FORMULA_NO_CACHE`
- `ERROR_VALUE`
- `UNSUPPORTED_OR_UNREADABLE`

These are adapter observation states, not canonical FinancialFact states. A cached formula result is still a source-reported workbook value; the formula must not be recomputed by the application.

## 5. Candidate value context

The interpretation layer may construct a transient `ValueCandidate` from a cell plus its row, column, table, and worksheet context. It must retain references to the underlying observations until admission is complete.

A ValueCandidate must be able to carry:

- source cell observation;
- row Header/label hierarchy;
- column Header hierarchy;
- table and worksheet context;
- nearby caption/footnote context when relevant;
- raw numeric/text value and parse status;
- literal unit/currency/scale clues from source labels or workbook metadata;
- candidate temporal descriptors from the column/row context;
- candidate presentation role (Actual, Forecast, Plan, comparative, etc.) as unresolved evidence;
- diagnostics and ambiguity markers.

The candidate is not yet a FinancialFact. In particular, it must not contain an invented `metric_id`, `period_id`, canonical unit, or dimension identity before the relevant standards resolve them.

## 6. Temporal context — mandatory per candidate

A workbook may publish several periods side by side, including current YTD, prior-year comparative, prior full year, and forecast columns. Therefore:

- temporal descriptors are attached to each candidate value, not just to the workbook or report;
- preserve literal date/period labels and their header hierarchy;
- distinguish source-reported date endpoints from inferred fiscal labels;
- allow multiple candidates from one table to resolve to different FinancialPeriod identities;
- preserve whether the source explicitly labels a value as cumulative/YTD or standalone, while leaving unresolved cases ambiguous;
- do not infer a quarter by subtracting adjacent values or by relying on column order;
- do not assume the company's fiscal year begins on Farvardin 1;
- instant/duration, actual start/end Jalali dates, months_length, fiscal year/quarter, and is_ytd are assigned only by temporal interpretation under DB-DES-003.

If the period context for an in-scope candidate cannot be resolved, the whole report is rejected. The DTO must not silently attach a workbook-level default period.

## 7. Numeric and unit fidelity

The adapter preserves the source numeric representation without converting it to the final canonical integer.

- Numeric parsing uses Decimal in the interpretation/validation layer; binary floating-point conversion is not an acceptable canonical parsing path.
- Do not round in the adapter. The approved Decimal → signed 64-bit SQLite INTEGER conversion with one ROUND_HALF_UP occurs once at canonical validation.
- Preserve literal unit/currency/scale clues; do not multiply/divide by 1,000, 1,000,000, or convert Toman/Rial based on number format or magnitude.
- The sole approved automatic unit conversion is the separately specified FX Toman×10→Rial exception; it does not apply to CODAL financial observations.
- Blank is not zero. Zero is valid only when explicitly source-reported. ZERO_FALLBACK remains narrowly limited to product sales amount under the existing approved rule and must be distinguishable from source zero.
- Percentages, ratios, quantities, rates, money, and counts must remain distinguishable; do not coerce every numeric cell to a currency amount.

## 8. Interpretation-stage responsibilities

The following sequence consumes the DTO; no stage may be collapsed into fuzzy matching:

1. Resolve company identity and its single industry from trusted input/source metadata.
2. Resolve ReportType as MONTHLY_ACTIVITY or PERIODIC_FINANCIAL.
3. Select the exact approved company/industry/report-family extraction standard version.
4. Resolve worksheet/table structure and source Header → Standard Database Header mappings.
5. Resolve row/column roles and each in-scope value candidate to Metric plus approved value-defining dimensions.
6. Resolve Actual/Forecast/Plan and source audit/restatement metadata independently.
7. Resolve each candidate's actual Jalali FinancialPeriod and INSTANT/DURATION/YTD semantics.
8. Parse and validate value, unit, currency, basis, NULL/zero state, integer bounds, and any specifically approved conversion.
9. Detect same-identity duplicates and payload conflicts across the entire workbook.
10. Admit the entire unit or reject it. Only explicitly out-of-scope content under the exact versioned standard may be skipped.

An unknown or ambiguous in-scope candidate is not an adapter warning that can be ignored. It is a hard report-level admission failure unless resolved before ingestion.

## 9. Persistence boundary

The DTO and all raw observations are transient. The target database stores only accepted canonical facts and minimum operational provenance under DB-DES-001/005/006.

Not persisted as a general archive:

- raw worksheet rows/cells;
- source Header strings as permanent raw facts;
- formulas or cached cell values as raw archive;
- workbook formatting/style payload;
- mandatory per-fact sheet/row/cell locators.

Persisted canonical provenance remains: ReportVersion, actual FinancialPeriod, FinancialMetric, approved dimensions, exact extraction/mapping standard version, canonical value/state, source unit/basis and required source/revision/publication metadata. IngestionRun retains operational counts, versions, source fingerprint/identity, errors and warnings.

## 10. Rejection and diagnostics

The DTO must support diagnostics that identify the unresolved worksheet/table/row/column candidate during the active run. Diagnostics may include transient coordinates for user-facing correction.

Hard reject the whole file for:

- unresolved company/industry/report type;
- unknown or ambiguous in-scope Header, Metric, dimension, temporal meaning, unit, basis, or value;
- formula without usable cached result where the cell is required;
- invalid numeric value or signed 64-bit overflow;
- conflicting duplicate canonical identity;
- unsupported workbook feature that prevents reliable interpretation of an in-scope region.

Explicitly out-of-scope content may be skipped only under a versioned approved standard. Do not create OTHER, UNKNOWN, or generic catch-all mappings.

## 11. Explicit non-goals and open decisions

This contract does not select or mandate:

- production Python DTO/reader implementation (the companion design selects immutable standard-library dataclasses);
- a specific Excel library (selected separately by DB-AUD-008);
- exact table-detection algorithms;
- physical ORM classes, database tables, columns, or migrations;
- permanent raw staging or workbook archival;
- final mapping content for any company beyond already approved standards;
- automatic inference from color, number format, formulas, position, or workbook filename;
- PDF compatibility or PDF ingestion support.

Before implementation, validate the contract against representative real Excel workbooks, including multi-level headers, merged cells, multiple tables per worksheet, formula cached values, comparative periods, YTD and standalone values, and blank/error cells. The actual XLSX files have not been inspected as part of this task; this report defines the DTO contract from approved architecture and existing Markdown evidence only.

## 12. Acceptance criteria and status

DB-DES-007 is PARTIAL until all of the following are satisfied:

1. DTO preserves workbook/sheet/table/row/column hierarchy without flattening.
2. Every value candidate retains its own temporal and presentation context.
3. Literal labels and numeric source values remain distinct from interpreted/canonical fields.
4. Formula cached-result status, blanks, explicit zero, and invalid cells are distinguishable.
5. Adapter does not infer metric, dimensions, units, periods, or scope.
6. Transient source observations are not persisted as raw-row archives.
7. Group, measure, temporal, presentation and row-axis header evidence remain independently observable.
8. Whole-file validation and DB-DES-005 atomicity are supported.
9. Representative workbook evidence validates the DTO shape.
10. Implementation and user-run tests demonstrate deterministic extraction and rejection behavior.

**Current result:** logical DTO contract drafted; no adapter, DTO code, ORM, schema, migration, data, or tests changed. Tests were not run.


## 13. Companion Python DTO design

The logical contract is now accompanied by `reports/DB_DES_007_PYTHON_DTO_DESIGN.md`, which specifies the concrete immutable Python observation types, stable transient references, orthogonal header axes, value/formula states, OOXML numeric-token sidecar, diagnostic model, and reader/interpretation boundary. The design uses Python 3.12 standard-library frozen/slots dataclasses and immutable tuples; it does not introduce Pydantic or a new dependency.

The reader profile is selected separately in DB-AUD-008: openpyxl normal mode plus a narrow read-only OOXML numeric-token sidecar. The DTO design remains transient and does not authorize raw-row persistence.

**Status remains PARTIAL:** the design is complete, but DTO/reader implementation, table-region candidate detection, additional authorized source evidence, and user-run acceptance tests remain open. No production code or tests were changed/run in this design step.


## 14. Owner-confirmed text-only V1 input amendment (2026-11-15)

The owner confirms that CODAL XLSX inputs contain no formulas and that all populated cells are stored as text. This is now the normative V1 source contract and supersedes formula/cache and native numeric-cell assumptions in earlier sections:

- Populated cells must be text cells; preserve literal text exactly.
- Blank remains distinct from text and from zero.
- Numeric-looking/date-looking strings are not parsed or normalized by the reader; parsing occurs in the interpretation/validation layer.
- Numeric-typed, boolean, date-typed, formula, or Excel error cells violate the contract. The reader emits a stable error diagnostic and the whole report is rejected; no coercion or cached-value fallback is allowed.
- Formula expression/cache fields and raw OOXML numeric-token extraction are removed from the V1 DTO/reader boundary.
- openpyxl normal mode remains the selected reader; one structural/text pass is sufficient.

The companion concrete DTO design is `reports/DB_DES_007_PYTHON_DTO_DESIGN.md`; initial immutable runtime types now exist in `src/ingestion/excel/dto.py`. Implementation of the structural/text reader, table-region detection, and owner-run validation remains open. Raw observations remain transient and are never persisted.
