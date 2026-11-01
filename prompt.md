# Task 060 — Fzar Monthly Sales PDF Extraction Audit

**Task type:** REPORT-ONLY — no code changes, no test changes.

## Objective

Diagnose why the real Fzar monthly sales report does not satisfy the existing extraction test, despite the expected Persian terms being present in the original company PDF.

The original PDF is `pdf/Fzar.pdf`. Its manually prepared Markdown conversion is `pdf/Fzar.md`.

Treat `pdf/Fzar.md` as the primary content source.

## Strict file scope

Read only these files:

1. `pdf/Fzar.md` — primary source content.
2. `pdf/Fzar.pdf` — only if necessary to verify a suspected Markdown conversion defect.
3. `src/tests/test_codal_extraction.py`
4. `src/tests/test_codal_pdf_extraction.py`
5. `src/ingestion/codal/pdf_extract.py`
6. `src/ingestion/codal/adapter.py`
7. `src/ingestion/codal/parser.py`
8. `src/ingestion/codal/numbers.py`
9. `codal_19_pdf_validation_plan.md`
10. `matrix.md`

Do NOT read or convert the other 19 PDF files. Do not scan the `pdf/` directory contents. Do not perform repository-wide exploration.

If another file is essential, report its exact path and why it is needed. Stop and request authorization before reading it.

## Ownership and execution restrictions

- Do not modify source code, tests, configuration, or documentation.
- Do not run tests.
- Do not install dependencies.
- Do not perform Git operations.
- `WORKFLOW_RULES.md` is exclusively owned by ChatGPT. Do not modify, rename, move, reformat, or indirectly change it.
- `STAGE7_MASTER_WORKING_PACKET.md` is read-only. Do not modify it.
- Do not edit `reply.md` or any report file.

## Corrected Strict File Scope

Read only the following files:

1. `pdf/Fzar.md` — primary source for the actual report content.
2. `pdf/Fzar.pdf` — only if necessary to verify a suspected Markdown conversion defect.
3. `src/tests/test_codal_extraction.py`
4. `src/tests/test_codal_pdf_extraction.py`
5. `src/ingestion/codal/pdf_extract.py`
6. `src/ingestion/codal/adapter.py`
7. `src/ingestion/codal/parser.py`
8. `src/ingestion/codal/numbers.py`

The following previously listed paths are removed from scope because they were not found at the specified locations:

- `codal_19_pdf_validation_plan.md`
- `matrix.md`

Do not search the repository for alternative copies or similarly named files.

Do not read any of the other 19 PDFs.

If another file is essential to establish the extraction failure, report its exact path and explain why it is necessary. Stop and request authorization before accessing it.

All other restrictions and audit requirements in the original prompt remain unchanged.

## Required investigation

### 1. Establish the actual Fzar report structure

Using `pdf/Fzar.md`, identify:

- Actual report title and report type.
- Reporting period.
- Table headings and column meanings.
- Product/item names and units.
- Quantity, sales, and monetary value columns.
- Whether the tables contain merged, multi-line, or split cells.
- Whether the Markdown conversion appears to have damaged row/column relationships.

Confirm the presence and context of these known terms:

`تراورتن`، `کانسنگ`، `طلا`، `فروش`، `تن`

Do not assume that the presence of these terms means the extraction test is correct. Determine where they occur and what they represent.

### 2. Audit the existing test

Inspect `test_real_codal_monthly_activity_pdf` and its helper functions.

Determine:

- Which PDF path the test actually selects.
- Whether the selected path can resolve to the local `pdf/Fzar.pdf`.
- Whether the test metadata matches the actual Fzar report.
- Whether its expected item-name assertions are appropriate.
- Whether the test is testing a general monthly report contract or one specific company/report layout.

### 3. Trace the extraction pipeline

Follow the relevant implementation:

PDF text/table extraction → extracted rows/cells → adapter → `RawLineInput`.

Determine precisely where the actual Fzar product names, units, quantities, and sales values could be lost or misclassified.

Examine:

- Persian RTL cell ordering.
- Header detection.
- Product-name cell selection.
- Numeric-cell extraction.
- Multi-line and merged-cell handling.
- Fallback extraction behavior.

Distinguish a PDF text/layout limitation from an implementation defect or a test-fixture/metadata problem.

### 4. Separate the test concerns

Decide whether the current test should be:

- A generic monthly-activity extraction test using a genuinely representative fixture.
- A dedicated Fzar-specific regression test.
- Both, with independent assertions and purposes.

Do not recommend replacing the real Fzar file with a similar report as a substitute for validating Fzar itself.

### 5. Final decision

Provide a concise evidence-based decision table:

| Question | Finding | Evidence |
|---|---|---|
| Is the Markdown conversion adequate? | | |
| Does test path selection reach Fzar? | | |
| Does test metadata match Fzar? | | |
| Are expected item-name assertions valid? | | |
| Is there an extraction implementation defect? | | |
| Is a separate Fzar regression test needed? | | |

Choose and justify one implementation direction:

A. Correct fixture/path selection only.

B. Separate generic monthly extraction testing from Fzar-specific regression testing.

C. Fix an identified extraction implementation defect.

D. Fzar requires a distinct extraction capability.

If evidence supports more than one, explain the order in which they should be addressed.

## Final report

Provide:

1. Confirmed facts about the Fzar report.
2. Exact failure mechanism, if identifiable.
3. Evidence from the specified source files.
4. Recommended implementation scope and exact files likely to change.
5. Any additional file access required, with justification.
6. A precise proposed test strategy.

This is an audit only. Do not implement the recommendation.