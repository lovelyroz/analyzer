# Task: Independent Re-Audit of Parsian Periodic Excel Workbook

**Task ID:** DB-ING-006-AUDIT-02  
**Mode:** REPORT ONLY — NO CODE CHANGES

## 1. Objective

Perform a completely independent, fresh audit of the original workbook:

`parsian_periodic.xlsx`

Save the new report at:

`parsian_periodic_report_2.md`




The purpose is to establish reliable, coordinate-level evidence for creating a Company Table Layout Template.

## 2. Strict Restrictions

- Do not modify the source XLSX.
- Do not modify application code.
- Do not modify existing reports, specifications, or architecture documents.
- Do not run tests.
- Do not create or modify any other project file.
- Do not infer financial meaning from cell contents.
- Do not guess table boundaries or cell roles.
- Do not silently resolve contradictory evidence.
- Do not use the previous report as a substitute for inspecting the workbook.
- The only permitted output is the new Markdown report at the specified path.

## 3. Authoritative Annotation Convention

The workbook has been standardized manually by its owner. The following rules describe the intended annotations.

| Color | Meaning |
|---|---|
| Red | Main table name; located outside the table, normally one or two rows before it |
| Blue | Table header cells |
| Yellow | Description/label cells for rows |
| Gray | Numeric/value cells that must be extracted |
| Black | Columns whose values must NOT be extracted |
| Green | Sub-table name |

Additional rules:

1. Every table is intended to have a recognizable outside border. It does not have to use Excel's literal `thick` border style. A visibly distinguishable non-default border may be used.
2. The owner colors cells so that table regions can still be recognized even when a border is incomplete.
3. Most tables are read right-to-left. In the common layout, yellow description cells are on the right.
4. Green cells identify sub-table names. In the reading order, the yellow description column immediately following a green marker begins the corresponding sub-table's label region. This continues until the next green marker or the parent table's end.
5. Cells without an annotation color are NOT extracted.
6. Black cells/columns are NOT extracted.
7. A gray cell is an extraction cell even if its Excel value is blank. A blank gray cell must be interpreted as numeric zero (`0`), not NULL or missing. Therefore, blank gray cells must be included in the gray-cell inventory and explicitly identified as blank.
8. A valid table may have no yellow description column if its gray extraction cells and table structure establish that it is a valid owner-annotated exception.
9. A blue header alone is not sufficient evidence that a region is an extractable table. Record the evidence without independently inventing a table classification.

These are annotation rules, not permission to infer missing annotations.

## 4. Workbook and Worksheet Inventory

Inspect every worksheet independently.

For each worksheet, report:

- Exact worksheet name.
- Used range.
- `rightToLeft` property.
- Merged cell ranges.
- Dimensions and non-empty cell counts.
- Formula cell count and exact coordinates, if any.
- Any unusual worksheet properties that affect interpretation.

Do not assume that a worksheet is a duplicate of another worksheet. Treat each worksheet as independent unless the workbook itself provides clear evidence otherwise.

## 5. Raw Color Inventory

Inspect all cells in the used range, including blank cells that have formatting.

For every annotated cell, report:

- Worksheet name.
- Exact cell coordinate.
- Observed cell value.
- Excel data type.
- Whether the cell is blank.
- Fill type.
- Color type (`rgb`, `indexed`, or `theme`).
- Raw RGB value, if applicable.
- Theme index, if applicable.
- Indexed color, if applicable.
- Tint.

Classify the cells by the owner's annotation roles:

- Red
- Blue
- Yellow
- Gray
- Black
- Green
- Uncolored

Do not invent a separate semantic category for a slightly different shade of black. Preserve the raw color metadata and report the visual/color difference objectively. The owner has clarified that dark-looking cells in this workbook belong to the black excluded-column role unless the source workbook proves otherwise.

Provide per-worksheet and workbook-wide counts for every color role.

### Critical: Gray cells

For gray cells, provide a complete coordinate-level inventory.

Separate them into:

- Gray cells with literal numeric values.
- Gray cells with literal text values.
- Gray cells with blank values.
- Gray cells with other data types.

Do not omit blank gray cells. Do not treat them as uncolored or as absent data.

## 6. Border Audit

Inspect border properties for all relevant cells, including cells with blank values.

For each candidate table region, report:

- Exact outer boundary coordinates.
- Top, bottom, left, and right border styles.
- Border color metadata where available.
- Whether each edge is continuous or has gaps.
- Exact coordinates of missing or different-style edge segments.
- Whether the boundary is visually distinguishable from ordinary cell borders.

Do not require the literal `thick` style.

Do not automatically reject a candidate because its border is `medium`, `thin`, or mixed. Report the observed evidence and let the owner make the final decision.

Also report formatted/bordered regions that are not associated with a red main table name.

## 7. Main Table Inventory

Identify every red main-table name independently.

For each red cell, report:

- Worksheet and exact coordinate.
- Exact cell value.
- Raw fill metadata.
- Its position relative to nearby bordered/annotated regions.

For every possible associated table region, report:

- Worksheet.
- Exact rectangular bounds in A1 notation.
- Top-left and bottom-right coordinates.
- Red main-name cell coordinate.
- Number of rows and columns.
- Border evidence.
- Blue header coordinates.
- Yellow description coordinates.
- Gray extraction coordinates.
- Black excluded coordinates.
- Green sub-table marker coordinates.
- Uncolored coordinates.
- Any cells outside the rectangle that appear related, but do not include them without evidence.

Do not assume that every red name necessarily identifies a valid extractable table. Report the evidence and any uncertainty.

Do not assume that every bordered rectangle is a table.

## 8. Sub-table Inventory

For every green cell, report:

- Worksheet and exact coordinate.
- Exact cell value.
- Parent table candidate, if objectively identifiable.
- Yellow description cells that follow it in the table's reading order.
- Exact coordinates of the first and last associated yellow cells.
- The next green marker, if any.
- Whether the sub-table boundary is clear or ambiguous.

Provide provisional sub-table ranges only when the source workbook's annotations and geometry support them.

Do not invent missing yellow or gray annotations.

## 9. Direction and Reading Order

For each table candidate:

- Record the worksheet's `rightToLeft` property.
- Determine the actual physical position of yellow description cells and gray value cells.
- Report the observed column order.
- Record any merged cells that affect the reading order.
- Do not assume that `rightToLeft=True` alone proves the logical reading order.
- Do not assume that visual column A is on the left or right without checking the actual workbook layout.

## 10. Independent Worksheet Examination

Pay particular attention to the secondary worksheet.

Do not rely on any previous claim about its name, range, title, colors, or contents.

For every possible table-like region on that worksheet, report the same evidence required in sections 5–9.

In particular, verify independently:

- Whether a red main-table name exists.
- Whether blue header cells exist.
- Whether yellow description cells exist.
- Whether gray extraction cells exist.
- Whether any gray extraction cells are blank.
- Whether green sub-table markers exist.
- Whether black excluded columns exist.
- Whether a recognizable border exists.
- Exact coordinates and values of all these cells.

Do not call the worksheet a duplicate merely because its contents resemble another worksheet.

## 11. Anomaly and Conflict Register

Create a separate section listing all anomalies, including:

- A red name without an identifiable table.
- A table-like bordered region without a red name.
- Blue headers without gray extraction cells.
- Gray cells without yellow descriptions.
- Blank gray cells.
- Yellow cells without corresponding gray cells.
- Green markers without clear sub-table extents.
- Black columns mixed with gray extraction columns.
- Missing or incomplete borders.
- Uncolored cells inside otherwise annotated regions.
- Merged cells that complicate bounds or interpretation.
- Formula cells or unsupported cell types.
- Any discrepancy between visual appearance and raw formatting metadata.

For each anomaly, provide exact worksheet and cell coordinates. Do not resolve it by guessing.

## 12. Required Report Structure

Save the report with these sections:

1. Audit scope, workbook identity, and source SHA-256.
2. Worksheet inventory.
3. Global raw color inventory.
4. Complete coordinate inventory of annotated cells, grouped by worksheet and color.
5. Border inventory.
6. Main table candidates.
7. Detailed evidence for every candidate table.
8. Green sub-table marker inventory and provisional partitions.
9. Reading direction and column order.
10. Independent secondary worksheet analysis.
11. Blank gray cell inventory and zero interpretation.
12. Anomaly and conflict register.
13. Final factual summary and unresolved questions.

Use Markdown tables where useful. For long coordinate lists, use compact grouped lists, but never omit coordinates.

## 13. Quality Requirements

- All counts must be reproducible from the coordinate-level inventory.
- Every reported range must be traceable to actual worksheet coordinates.
- Distinguish observed facts from interpretations.
- Preserve raw formatting metadata rather than reporting only semantic color names.
- Do not silently merge similar colors into one category.
- Do not infer a table solely from a title, header, or border.
- Explicitly distinguish blank cells from cells containing numeric zero.
- Include source workbook SHA-256 so the inspected file can be identified.
- State which inspection library and method were used.
- If any part of the workbook could not be inspected reliably, state that limitation explicitly.

## 14. Final Output

Create only:

`parsian_periodic_report_2.md`

At the end of your response, report:

- Confirmation that the original XLSX was inspected from scratch.
- Source workbook SHA-256.
- Report path.
- Number of worksheets inspected.
- Number of red, blue, yellow, gray, black, and green cells per worksheet.
- Number of blank gray cells.
- Any unresolved inspection limitations.

Do not edit or overwrite `parsian_periodic_report_1.md`.

**Remember: This is an evidence-gathering task, not a template-design or code-implementation task.**