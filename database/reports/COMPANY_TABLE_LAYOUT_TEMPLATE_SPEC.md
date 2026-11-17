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

The following bounds are mechanically derived from the current Parsian audit's parent-table bounds and green-marker coordinates. They are **provisional** until the owner reviews/approves them; they are not yet an approved template inventory:

| Parent table | Green marker | Provisional sub-table bounds | Data-label rows |
|---|---|---|---|
| Recovered_Sheet1!A10:E42 | A12 | A12:E31 | 13:31 |
| Recovered_Sheet1!A10:E42 | A32 | A32:E34 | 33:34 |
| Recovered_Sheet1!A10:E42 | A35 | A35:E42 | 36:42 |
| Recovered_Sheet1!A60:E68 | A63 | A63:E68 | 64:68 |
| Recovered_Sheet1!A79:E119 | A81 | A81:E94 | 82:94 |
| Recovered_Sheet1!A79:E119 | A96 | A96:E107 | 97:107 |
| Recovered_Sheet1!A79:E119 | A108 | A108:E119 | 109:119 |
| Recovered_Sheet1!A130:L165 | A152 | A152:L165 | 153:165 |
| Recovered_Sheet1!A176:E213 | A178 | A178:E181 | 179:181 |
| Recovered_Sheet1!A176:E213 | A182 | A182:E190 | 183:190 |
| Recovered_Sheet1!A176:E213 | A191 | A191:E213 | 192:213 |
| Recovered_Sheet1!A266:F275 | A268 | A268:F275 | 269:275 |
| Recovered_Sheet1!A313:G332 | A314 | A314:G332 | 315:332 |
| Recovered_Sheet1!A361:C367 | A362 | A362:C365 | 363:365 |
| Recovered_Sheet1!A361:C367 | A366 | A366:C367 | 367:367 |

The report also identifies `Sheet1!A16:E24` as an independent worksheet region, as confirmed by the owner. However, its current annotation audit records zero gray cells and zero yellow cells. It therefore cannot yet supply any positive extraction-cell coordinates under the approved gray-only rule. Keep it as an independently identified region, but do not infer that its uncolored cells are extractable; the owner must clarify whether it is intentionally structural-only/empty in this sample or whether its intended value cells still need gray annotation.


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
