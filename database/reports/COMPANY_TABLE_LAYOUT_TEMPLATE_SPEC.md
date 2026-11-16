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

## 6. Sample annotation convention

The standardized sample workbook uses the owner's visual annotation convention:

- thick outside border: complete table bounds
- red table-name cell: one or two cells before the table; its exact coordinate is recorded
- blue header cells: header bounds/levels
- green sub-table-name cells: sub-table identity and bounds

These visual annotations are used only during one-time template authoring and validation. Later reports are not required to contain these colors or borders.

The annotation reader must inspect both font and fill color representations (RGB, indexed, and theme-based where present) rather than assuming that "cell color" means only font color or only fill color. It must preserve raw color metadata for review and avoid guessing when a color is ambiguous.

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
5. The approved storage location and serialization/persistence model for template versions.

Do not resolve these by assumption. First extract the annotations and bounds from the standardized Parsian sample, then inspect a later report from the same company to measure layout drift.
