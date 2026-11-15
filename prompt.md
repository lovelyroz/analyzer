# Task: Extract and Inventory All Bordered Tables from Parsian Excel Sample

You are working on the CODAL financial-data project:

`analyzer`

## 1. Task Type

**REPORT ONLY — NO CODE CHANGES**

Your task is to inspect the prepared Excel workbook and produce a complete, auditable inventory of all tables and their cell contents.

Do not modify application code, database schemas, project documentation, or the original Excel workbook.

Do not perform data cleaning, normalization, financial interpretation, or data transformation.

## 2. Input Workbook

Locate the prepared workbook:

`excel/parsian_periodic.xlsx`

The workbook has been manually annotated to identify its table structures.

Inspect the actual workbook and determine the relevant worksheet(s). Do not assume worksheet names or fixed cell coordinates without verifying them.

## 3. Manually Defined Visual Markers

The workbook uses the following conventions:

### A. Table boundaries — Borders

Every table that must be extracted has been marked with borders.

Use the cell border properties to identify the exact table boundaries.

Do not assume that every bordered region is necessarily a separate table. Inspect the complete border structure and identify each distinct table.

For every table, determine:
- Top-left cell coordinate.
- Bottom-right cell coordinate.
- Exact row and column boundaries.
- Number of rows and columns.
- Whether the table contains merged cells.

### B. Main category marker — Red cell

A red-filled cell is placed two rows above each table.

This cell identifies one of the 16 main report categories previously selected for extraction.

For every table:
- Locate the red marker associated with it.
- Record its exact cell coordinate.
- Record its raw cell value.
- Preserve the original Persian text.
- Associate the table with this category.

Do not infer or invent a category if the marker is missing or ambiguous. Report the problem explicitly.

### C. Subheaders — Green cells

One or more green-filled cells may exist inside each table.

These cells represent Sub Headers.

For each green cell, record:
- Exact cell coordinate.
- Raw cell value.
- Whether it is merged.
- Its position within the table.

Do not decide whether a Sub Header is financially valid. That decision will be made later.

### D. Column headers — Blue cells

Blue-filled cells represent table column headers.

For each blue cell, record:
- Exact cell coordinate.
- Raw cell value.
- Whether it is merged.
- Its position within the table.

Preserve all column headers, including multi-level headers.

## 4. Extraction Requirements

Extract **ALL cells inside every identified table boundary**, not just cells containing financial numbers.

This includes:
- Column headers.
- Subheaders.
- Data rows.
- Descriptive text.
- Totals and subtotals.
- Empty cells.
- Cells containing zero.
- Merged cells.
- Any other content inside the table boundaries.

For each cell, preserve:

1. Cell coordinate (e.g. A15).
2. Raw value.
3. Data type.
4. Formula, if present.
5. Number format.
6. Fill color information.
7. Border information.
8. Merged-cell membership, if applicable.

Important:

- Do not remove spaces.
- Do not normalize Persian characters.
- Do not convert Persian digits to English digits.
- Do not change date formats.
- Do not interpret numbers or financial values.
- Do not remove duplicate rows.
- Do not remove apparently irrelevant text.
- Do not fill empty cells.
- Do not calculate totals.
- Do not correct spelling or formatting.

The objective is to preserve the original workbook information as faithfully as possible.

## 5. Table Structure and Relationships

For every table, provide:

- A unique table ID.
- Worksheet name.
- Main category name and red marker coordinate.
- Exact table range.
- Row and column counts.
- All green Sub Header cells.
- All blue column-header cells.
- Merged ranges.
- A complete cell-by-cell extraction.

Preserve the original row and column positions.

Do not flatten the table into a list that loses its two-dimensional structure.

Where a cell is merged, preserve the original merged range and the actual value location. Do not duplicate its value into other cells.

## 6. Validation

Perform the following checks:

1. Every identified table must have a valid bordered range.
2. Every table should be associated with its red category marker.
3. Verify that the red marker is located two rows above the table, according to the prepared convention.
4. Identify all green cells inside each table.
5. Identify all blue cells inside each table.
6. Check for overlapping table ranges.
7. Check for adjacent tables that may have been incorrectly combined.
8. Check for tables that may have been missed.
9. Check whether any bordered cells or regions could not be classified confidently.

Do not silently resolve ambiguous cases. Report them separately.

## 7. Required Output Files

Create these two new files:

### A. `dbReports/parsian_table_inventory.md`

A readable report containing:

1. Workbook and worksheet information.
2. Total number of tables identified.
3. A summary table listing all tables.
4. For each table:
   - Table ID.
   - Main category.
   - Red marker coordinate and value.
   - Table range.
   - Dimensions.
   - Green Sub Headers.
   - Blue column headers.
   - Merged cells.
   - Complete cell-by-cell contents in a readable matrix.
5. Validation results.
6. Ambiguous or unresolved cases.

### B. `dbReports/parsian_table_inventory.json`

A machine-readable representation of the same inventory.

Requirements:
- Preserve original cell coordinates.
- Preserve raw values and data types.
- Preserve row and column positions.
- Preserve merged ranges.
- Preserve style and border metadata where available.
- Use valid JSON.
- Represent empty cells explicitly as null.
- Do not lose any information that exists in the Markdown report.

## 8. Important Restrictions

- Do not modify `parsian_periodic.xlsx`.
- Do not modify existing project files.
- Do not modify application code.
- Do not create or modify database tables.
- Do not run data-cleaning operations.
- Do not decide which Sub Headers are valid.
- Do not assume that all tables have identical dimensions.
- Do not assume fixed row numbers or column numbers.
- Do not use financial meaning to override the manually defined visual markers.

If a visual marker or border is ambiguous, report it rather than guessing.

## 9. Final Response

When finished, report:

1. Number of worksheets inspected.
2. Number of tables identified.
3. Number of tables successfully associated with a red category marker.
4. Number of green Sub Header cells.
5. Number of blue column-header cells.
6. Number of merged ranges.
7. Any unresolved or ambiguous cases.
8. Exact paths of the two output files.
9. Confirmation that no original project files or workbook contents were modified.

Do not claim complete extraction unless every identified table has been accounted for.