# Task: Inspect Parsian Quarterly Financial Report — DB-STD-003

You are working in the repository:

`analyzer`

## Objective

Inspect the local Excel workbook:

`excel/parsian_periodic.xlsx`

This is the second real sample for designing the **Quarterly Financial Report Standard (DB-STD-003)**.

The purpose is to extract and document the workbook's actual structure, financial statement layout, headers, period definitions, and data characteristics so ChatGPT can review the evidence and decide the standard.

**This is an inspection and evidence-reporting task only. Do not implement code, modify database schemas, create migrations, or finalize the standard.**

## Mandatory project constraints

1. There are exactly two report types in the current project:
   - Monthly Activity Reports
   - Quarterly Financial Reports

2. YTD/cumulative values and standalone-quarter values are temporal properties of data within a quarterly report. They are NOT separate report types.

3. Do not apply the monthly activity report standard to this quarterly report.

4. Do not automatically apply the Bank Master five-label taxonomy to quarterly financial statements. That taxonomy was defined for classifying bank-specific monthly-report Headers. Quarterly financial statements require their own evidence-based review.

5. Do not create a separate canonical Metric merely because a source Header exists.

6. Do not infer a Header's financial nature from its title alone. Consider its position, table context, notes, units, period columns, and relationships with other items.

7. If the nature or meaning of an item cannot be established from the workbook, mark it as requiring clarification. Do not guess.

8. Preserve Persian/Jalali date information as presented. Do not convert dates or assume a Gregorian fiscal year.

## Inspection scope

Inspect the entire workbook, including all worksheets, hidden worksheets if accessible, and relevant workbook metadata.

### 1. Workbook inventory

Report:
- File name and workbook format.
- Number of worksheets.
- Worksheet names and order.
- Hidden/visible status of each worksheet.
- Used range and approximate data dimensions of each worksheet.
- Merged cells, formulas, named ranges, and other structural features relevant to interpretation.
- Whether the workbook appears to contain one report or multiple reports/statements.

### 2. Report identity and period

Identify evidence for:
- Company name and ticker, if present.
- Report type and reporting period.
- Fiscal year, if identifiable.
- Fiscal-year start and end, if identifiable.
- Whether the report is quarterly, interim, or another type.
- Whether the workbook contains comparative periods.

Do not use the phrase «دوره منتهی به» alone as proof of a particular period interpretation.

### 3. Table and statement inventory

Identify every financial statement and major table.

For each one, report:
- Worksheet and exact location.
- Table title, if present.
- Row and column structure.
- Header rows and data rows.
- Units and scaling (e.g. ریال، میلیون ریال، هزار ریال).
- Whether the table contains monetary, quantity, ratio, descriptive, or other data.
- Relevant footnotes and explanatory text.

Do not omit tables simply because they are small or appear supplementary.

### 4. Source Header inventory

Create a complete inventory of actual source Headers.

For every Header, record:
- Exact Persian source text.
- Worksheet and cell/range location.
- Table/statement to which it belongs.
- Whether it is a row Header, column Header, subheader, unit Header, or descriptive label.
- Associated unit, where available.
- Relevant notes or contextual evidence.
- Any ambiguity that prevents reliable interpretation.

Preserve the original spelling and wording. Do not normalize or rename source Headers.

### 5. Temporal classification — critical

For every numeric value column or group of columns, determine whether it represents:

- Standalone quarter (only the three-month period).
- Year-to-date / cumulative period from fiscal-year start.
- Point-in-time balance at the reporting date.
- Prior-period comparative value.
- Opening balance.
- Closing balance.
- Other temporal meaning.
- Unknown / requires clarification.

Do not assume that all columns in one statement have the same temporal meaning.

For each classification, provide the exact source Header and supporting evidence.

Where a value is cumulative, do not calculate standalone-quarter values. Merely document the evidence and the possible relationship.

If the workbook does not clearly distinguish standalone-quarter from cumulative figures, explicitly report the ambiguity.

### 6. Financial nature and structure

Identify, without imposing a final taxonomy:
- Revenue/income items.
- Expense items.
- Assets, liabilities, and equity items.
- Cash-flow items.
- Quantity/operational items.
- Ratios and per-share data.
- Other disclosures.

For each item, distinguish between:
- Flow during a period.
- Stock/balance at a point in time.
- Ratio or derived measure.
- Descriptive/informational disclosure.

Pay special attention to:
- Summary versus detail rows.
- Parent/child row relationships.
- Totals and subtotals.
- Duplicate presentations of the same economic item.
- Potential double-counting risks.
- Restated or reclassified comparative figures.
- Notes that explain inclusions/exclusions.

Do not assume that a total should be stored independently if it can be calculated from detail rows. Just document the structure and evidence.

### 7. Fiscal-year and comparative-period issues

Determine whether:
- The fiscal year starts in January or another month.
- Period labels are Jalali/Persian, Gregorian, or another representation.
- Comparative figures use the same duration and fiscal-year basis.
- The workbook includes prior-year cumulative figures or prior-year standalone-quarter figures.
- Any comparative value is restated or reclassified.

If any of these cannot be determined, state exactly what is missing.

## Required output

Create or update:

`dbReports/parsian_persidic_report_1.md`

Append a clearly titled section:

`Parsian Quarterly Workbook Inspection — DB-STD-003`

The report must include:

1. Executive summary.
2. Workbook/worksheet inventory.
3. Report identity and period evidence.
4. Financial statement and table inventory.
5. Complete source Header inventory.
6. Temporal classification matrix.
7. Financial nature and row-hierarchy analysis.
8. Summary/detail and double-counting observations.
9. Ambiguities requiring ChatGPT/user clarification.
10. Recommended next inspection step.

Use tables where they make the evidence easier to review.

Every important conclusion must cite the relevant worksheet and cell/range. Include exact source text where useful.

If the workbook contains too many Headers for a concise report, do not silently omit them. Include the complete inventory in the report or a clearly referenced supplementary section.

## Restrictions

- Do not edit `WORKFLOW_RULES.md`.
- Do not edit the master packet or Bank Master documents.
- Do not edit any existing monthly-report standards.
- Do not change source Excel files.
- Do not implement code or tests.
- Do not make database/schema/migration changes.
- Do not declare DB-STD-003 complete.
- Do not make unresolved assumptions into facts.

## Final response

After completing the inspection:
- List the files you read.
- List the files you changed.
- Confirm that no code, schema, migration, or source workbook was modified.
- Summarize the main findings and unresolved questions.
- Report any technical limitations encountered.

Do not run the test suite; this task does not involve code changes.