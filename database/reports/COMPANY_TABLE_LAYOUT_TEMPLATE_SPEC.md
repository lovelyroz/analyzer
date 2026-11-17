# Company Table Layout Template — Specification

Status: PROPOSED DESIGN for DB-ING-006  
Date: 2026-11-16  
Authority: owner decisions recorded in `DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md`

## 1. Purpose

A company/report-family template is created once from one explicitly standardized representative workbook. The template records the approved table layout and becomes the structural contract for later reports of the same company and report family.

The template is not a copy of the workbook and does not store raw rows, cell values, or derived financial values.

## 2. Template identity and versioning

The logical template key is:

- `company_id`
- `report_type_id` (or the project's approved stable report-family identifier)

Each approved revision has:

- immutable `template_id`
- `template_version`
- source workbook SHA-256 and file name for provenance
- approval/creation metadata
- schema version

A changed table layout creates a new template version. Historical ReportVersions retain the template version used for extraction; existing template versions are never silently edited.

## 3. Workbook and worksheet identity

For each worksheet represented in the template, record:

- stable worksheet-template ID
- sample worksheet ordinal and literal name
- matching/identity rule for later workbooks
- whether the sheet is required or optional

Ordinal/name are sample evidence, not automatically assumed permanent identifiers. The matching rule must be explicit and deterministic.

## 4. Table definition

Each table definition records:

- stable `table_id` within the template
- exact approved `table_name` as annotated in the sample
- worksheet-template ID
- complete table bounds in sample coordinates (`min_row`, `max_row`, `min_column`, `max_column`, plus A1 notation)
- exact table-name cell coordinate and its observed relative position to the table
- header bounds, allowing one or multiple rows and merged cells
- body bounds or body-start rule
- optional footer/summary bounds where explicitly identified
- stable table order within its worksheet
- a structural fingerprint built from approved header labels, merged-cell geometry, and column layout; it is used for matching/validation, not fuzzy semantic guessing

The approved complete bounds are authoritative for the sample. A later workbook is mapped to this definition through the approved matching rule; sample absolute coordinates are not blindly assumed to remain fixed if preceding content can shift.

## 5. Sub-table definitions

A table may contain zero or more sub-tables. Each sub-table records:

- stable `sub_table_id`
- parent `table_id`
- exact approved sub-table name
- name-cell coordinate in the sample
- exact bounds within the parent table
- its own header bounds/levels when present
- order and structural fingerprint

A sub-table is not automatically a separate top-level table. The parent-child relationship is explicit.

### Owner-driven sub-table partition rule

For the standardized sample, a green cell is the sub-table title marker. In the approved table reading order, the yellow description/label column immediately after that marker begins the sub-table's data-label rows. The marker row belongs to the sub-table's structural range as its title row; data rows begin on the following row. The sub-table continues through the row immediately before the next green marker, or through the parent table's final row when no later marker exists. Its column bounds are inherited from the parent table. This is a coordinate-based partition rule, not a semantic/fuzzy inference. Black and uncolored cells remain excluded from extraction.

The corrected single-sheet audit on 2026-11-17 supersedes the earlier provisional coordinate inventory below. The current red-title candidates, header coordinates, gray extraction coordinates, and green-marker row partitions are recorded in `PARSIAN_PERIODIC_ANNOTATION_MAP_DRAFT.md`. That report explicitly separates title-to-next-title review intervals from actual table bounds; it does not claim that complete rectangular bounds have been approved.

The earlier `Sheet1!A16:E24` paragraph is withdrawn. The owner confirmed that `Sheet1` was a temporary test worksheet and deleted it. The corrected workbook contains only `Recovered_Sheet1`; no `Sheet1` region belongs to the template.

## 6. Sample annotation convention

The standardized sample workbook uses the owner's visual annotation convention:

- non-default outside border (the exact Excel style token may be `medium` or another visibly non-normal style): evidence for the complete table boundary; the annotation audit must preserve the four edge styles and exact coordinates rather than requiring the literal token `thick`
- red table-name cell: one or two cells before the table; its exact coordinate is recorded
- blue header cells: header bounds/levels; blue header cells alone do not establish an extractable table
- green sub-table-name cells: sub-table identity and the start of a sub-table partition
- yellow cells: row-description/label cells
- gray cells: value cells approved for extraction
- black cells: explicitly excluded columns/cells
- uncolored cells: never extracted

These visual annotations are used only during one-time template authoring and validation. Later reports are not required to contain these colors or borders.

The annotation reader must inspect both font and fill color representations (RGB, indexed, and theme-based where present) rather than assuming that "cell color" means only font color or only fill color. It must preserve raw color metadata for review and avoid guessing when a color is ambiguous.

A top-level extractable table requires all of the following: (a) a recognizable non-default border boundary, (b) at least one gray extraction cell, and (c) an approved table region. A blue header without gray extraction cells is not a table. A region with no annotation colors and no extraction cells is out of scope even if it has a header-like appearance. The table's normal case includes yellow description cells, but an owner-confirmed table may omit the description column; therefore yellow is not a universal admission requirement. Black cells/columns and all uncolored cells are excluded from extraction even when geometrically inside a table boundary. Gray cells are the positive extraction signal; the table bounds alone do not authorize extracting every enclosed cell.

The border detector must not hard-code `Side.style == "thick"` as the sole table-boundary test. The owner's rule is visual/structural: a border that is distinguishable from the ordinary cell grid can mark the table boundary. Preserve the raw styles and edge coordinates so the approved template records exactly what was observed. The Parsian audit's report of zero literal `thick` sides is therefore not, by itself, evidence that the sample has no table borders; the reported `medium` edges are potential valid boundary evidence and must be reviewed by geometry.

Sub-table partitions are driven by the green sub-table-name cells. In the table's approved reading order, the yellow description column immediately following each green name begins that sub-table's row-label region. That region continues until the next green sub-table-name marker or the parent table's end. The exact cell/range coordinates must be recorded in the template after the sample is reviewed; do not infer the bounds from text semantics. The final Parsian table is an owner-confirmed exception with no yellow description column and remains eligible because it contains gray extraction cells and a table border.

## 7. Matching and extraction of later reports

For a later workbook:

1. Resolve the company and report family before ingestion.
2. Load the approved template version for that company/report family.
3. Identify required worksheets using the template's deterministic worksheet matching rules.
4. Locate each table using the template's structural fingerprint and approved relative layout rules.
5. Validate that the located bounds, header structure, merged geometry, and expected table/sub-table inventory satisfy the template.
6. Extract only within the validated bounds and preserve exact source-cell locators.
7. If a required table is missing, duplicated, structurally ambiguous, or materially changed, reject the whole report for review; do not fuzzy-match, silently shift bounds, or partially ingest.

Borders and annotation colors in later reports are not part of this runtime matching contract.

## 8. Change control and provenance

- Every extraction records the exact `template_id` and `template_version`.
- A layout change requires a new reviewed template version.
- Old template versions remain available for historical provenance.
- Template matching diagnostics must identify the table, worksheet, expected versus observed structure, and source coordinates.
- The template stores structural metadata only; it does not persist raw workbook rows/cells or derived financial values.

## 9. Open implementation decisions

The following must be resolved with sample evidence before runtime matcher implementation:

1. Whether worksheet identity is stable by name, ordinal, or a combination.
2. Whether table bounds remain at fixed absolute coordinates across periods or can shift while preserving internal structure.
3. How the one-or-two-cell table-name placement is represented (exact cell coordinate plus row/column offset).
4. How header/body/footer boundaries are represented for each table, including headers with merged cells.
5. The exact coordinate bounds of every green-marker-driven sub-table partition.
6. The approved storage location and serialization/persistence model for template versions.

Do not resolve these by assumption. First extract the annotations and bounds from the standardized Parsian sample, then inspect a later report from the same company to measure layout drift.


## Owner clarification — blank gray cells and Sheet1 audit correction (2026-11-17)

- A cell annotated gray is an extraction cell even when its literal Excel value is blank. For canonical extraction, a blank gray cell must be interpreted as numeric zero (`0`), not NULL, missing, or an instruction to skip the cell.
- This rule is specific to gray extraction cells. Uncolored cells remain outside extraction; black cells/columns remain explicitly excluded. A blank cell without gray annotation does not become zero.
- The prior audit-based claim that `Sheet1!A16:E24` has 8 blue cells, a green marker at A19, no yellow/gray cells, and a red title at A14 is disputed by the owner and must not be treated as verified workbook fact. The earlier "Sheet1 extraction annotation conflict" and any conclusion based on those reported coordinates are withdrawn pending a corrected audit report. Do not infer the actual worksheet, range, title, or annotations from the disputed report.
- The report's candidate-18 classification and associated color inventory are therefore provisional/untrusted until the source workbook is re-audited and the owner confirms the corrected coordinates.


## Corrected Parsian audit evidence — 2026-11-17

The owner supplied a complete direct-output audit for `excel/parsian_periodic.xlsx`. The workbook SHA-256 is `95f94e739632e48ae6552c562ecbf6c3e8182848718d17977f69bc984a6638b0`. The workbook contains exactly one worksheet, `Recovered_Sheet1`, used range `A1:L411`, right-to-left. The temporary `Sheet1` referenced by earlier reports was deleted and is out of scope; all prior findings about that worksheet are withdrawn.

The corrected audit inventory is 17 red title cells, 96 blue header cells, 15 green sub-table markers, 178 yellow label cells, 459 gray extraction cells, and zero cells with the explicit black annotation fill. Of the gray cells, 89 are blank, 134 contain numeric zero, and 236 contain nonzero numeric values. Blank gray cells must be extracted as numeric zero under the owner's rule.

The audit reports zero exact `thick` outside rectangles but 101 border-evidence ranges using `medium` style. These are raw geometry evidence, not proof of complete table rectangles. The detailed candidate inventory and provisional row partitions are in `PARSIAN_PERIODIC_ANNOTATION_MAP_DRAFT.md`. That map is not an approved Template: full table rectangles/column bounds remain for owner review, and a second later Parsian periodic workbook is required to validate layout drift. Reports 1–3 are audits of the same sample workbook and do not count as an independent second workbook.

This corrected evidence supersedes the older two-worksheet narrative, the `Sheet1!A16:E24` claim, and the previous candidate-18 color inventory. Task DB-ING-006 remains PARTIAL. The assistant reviewed the text audit output and did not open the XLSX directly or run tests.


## Parsian sample — consolidated owner rules and coordinate draft (2026-11-18)

This section supersedes conflicting provisional statements in the earlier Parsian-specific paragraphs above. The general Template schema remains proposed; this section records the current sample-specific contract.

### Worksheet scope and provenance

- The only in-scope worksheet is `Recovered_Sheet1`.
- The temporary worksheet `Sheet1` was deleted and is excluded completely.
- Sample workbook SHA-256: `95f94e739632e48ae6552c562ecbf6c3e8182848718d17977f69bc984a6638b0`.
- Report-3 candidate geometry is historical structural evidence for the main worksheet. It is the working reference for this coordinate draft, but has not been silently promoted to owner-approved production geometry.

### Owner-confirmed annotation semantics

- Red title cells identify the top-level table sections. Border marks outside a candidate rectangle do not expand that table.
- Blue cells identify header annotations; duplicate header cells B95/C95 in T03 are redundant because they repeat B79/C79 and must be ignored.
- Green cells identify sub-table title markers.
- Yellow cells identify row descriptions/labels where present; yellow is not mandatory (T17 is a valid no-yellow exception).
- Gray cells are the only positive extraction signal. A blank gray cell is extracted as numeric zero.
- Black-filled cells and uncolored cells are excluded even when they contain numeric values.
- Theme-based black fills count as black exclusions. The earlier audit count of zero black cells is invalidated by report 3's theme-fill evidence; a new theme-fill audit is deferred and is not a prerequisite for recording the owner's exclusion rule.
- T06 rows 243–244 and T13 row 364 require no special-case semantics: uncolored cells are excluded by the general rule.
- T04 black block `A131:L151` is excluded by the general black-cell rule.

### Working coordinate draft

The report-3 evidence and owner decisions have been consolidated into `PARSIAN_PERIODIC_ANNOTATION_MAP_DRAFT.md`, section 10. It records:
- 17 candidate top-level A1 rectangles;
- 15 candidate green-marker sub-table ranges, derived from each marker's row partition and its parent's column span;
- observed header ranges and explicit exceptions.

These ranges are **candidate coordinates pending explicit owner approval**, not yet the approved production Template. The green-marker row partition rule is: include the green marker row as the sub-table title row; end immediately before the next marker or at the parent table's final row; inherit the parent table's column span. Only gray cells inside the validated structure are extracted.

### Remaining design gates

1. Owner approval or correction of the 17 candidate table rectangles and 15 derived sub-table ranges in annotation-map section 10.
2. Define exact header/body/footer segmentation and treatment of merged headers for each approved table.
3. Decide deterministic worksheet identity and later-report table matching/coordinate-drift behavior.
4. Decide template-version serialization/storage location.

A second-period Parsian workbook comparison and a theme-fill re-audit are explicitly deferred for now. No runtime matcher or extraction implementation should be started until the owner has approved the coordinate draft and the remaining schema/matching decisions are specified.


### Parsian owner spot-check — 2026-11-18

The owner checked several of the candidate A1 ranges recorded in `PARSIAN_PERIODIC_ANNOTATION_MAP_DRAFT.md` section 10 and reported no issue in those checked examples. This is a spot check, not blanket approval of all 17 parent-table bounds and 15 sub-table partitions. The coordinate set remains the working candidate map; header/body/footer segmentation may proceed provisionally, but must distinguish observed facts from unresolved boundaries. No production Template approval or layout-drift validation is implied.


### Parsian provisional Header / Body / Footer segmentation — 2026-11-18

PARSIAN_PERIODIC_ANNOTATION_MAP_DRAFT.md section 12 now records a provisional row segmentation for all 17 candidate tables. It separates the observed parent Header ranges from the remaining candidate Body ranges. No Footer range is currently evidenced; the schema must not infer a footer merely because rows are at the end of a table. Green sub-table markers remain structural elements inside the parent Body. T09 retains its mixed header fill exactly as observed, T03 repeated B95/C95 is ignored, and T08's separate A297:D297 blue region is outside its candidate table.

This segmentation remains provisional and does not approve all candidate bounds. Body membership is not extraction permission: only gray cells are extracted, black/uncolored cells are excluded, and blank gray cells map to zero. Before production serialization, decide how the schema represents multi-level/discontiguous headers and nested sub-table headers; keep footer ranges optional. A separate later-period workbook is still required for drift validation.


## Query-oriented Template persistence decision — 2026-11-18

The Company Table Layout Template is metadata for deterministic extraction and application requests, not a human-facing copy of the Excel workbook. Persist it in normalized relational records with stable identifiers, foreign keys, versioning, uniqueness constraints, and exact source-coordinate provenance.

Hierarchy: Company + ReportType -> TemplateVersion -> TableDefinition -> SubTableDefinition. A sub-table is a child record linked to its parent; it does not duplicate parent metadata.

**Header inheritance rule:** a sub-table references the parent Header/column definition when column meanings, order, units/basis, and temporal interpretation are unchanged. It stores an explicit own Header definition only when those semantics differ. Header definitions may consist of multiple ordered/discontiguous ranges and levels; do not assume one contiguous header rectangle. Conflicting inherited/overridden definitions must be rejected rather than guessed. For the Parsian draft, the 15 green-marker sub-tables provisionally inherit their parent's header by reference; this is the default pending evidence of a semantic difference, not a claim that the workbook has been fully validated.

Body and optional Footer are separate structural ranges. Footer is absent unless explicitly identified. Body membership does not authorize extraction: only Gray cells are extracted, Black and Uncolored are excluded, and Blank Gray maps to numeric zero.

Retain A1 coordinates as source locators/provenance, but runtime requests should use canonical table/sub-table/field IDs and report-period dimensions. Do not store duplicated header text, copied parent definitions, raw cell grids, or derived values for display purposes. This decision settles the storage direction; candidate coordinates and Task 033 remain provisional/partial pending full approval and independent-period drift validation.


## DB-DES-008 relational schema proposal — 2026-11-18

The proposed physical relational model is detailed in `DB_DES_008_COMPANY_TABLE_TEMPLATE_RELATIONAL_SCHEMA_PROPOSAL.md`. It uses a logical company/report-type template, immutable template versions, worksheet records, unified parent/child layout nodes, multiple structural ranges, explicit OWN/INHERIT Header bindings, parent-owned column slots, and compact positive extraction spans. Physical layout remains separate from canonical Metric/Dimension mapping. The proposal is query-oriented and does not persist raw workbook grids or duplicate inherited Header definitions. It is not yet approved for ORM/migration implementation; Task 033 remains PARTIAL.
