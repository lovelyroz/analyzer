### 1. Executive Summary

**PARTIALLY CONFIRMED:** The supplied `pdf/Fzar.pdf` has three pages and contains an extractable text layer. Direct `pypdf` extraction returns Persian glyphs and many numeric strings, but its output interleaves table headers, labels, and values rather than preserving clearly associated rows.

**NOT EVALUABLE:** PDFium is not available in the inspected local environment, so I could not assess its output or compare PDFium rows with the application’s final `RawLineInput` records. The application adapter also could not be run: importing it fails because `jdatetime` is missing. I did not install anything.

### 2. Environment and PDFium Availability

- **PDFium: NOT EVALUABLE.** `pypdfium2` is not importable, and no `pdfinfo`, `pdftotext`, `mutool`, or `qpdf` executable was found through the inspected commands. I found no usable local PDFium capability to test on Fzar.
- **Available extraction package:** `pypdf 6.21.2`. I used it to read the PDF’s page count and text. This is not a PDFium evaluation.
- **Other checked packages:** `pdfplumber`, `pymupdf`/`fitz`, and `pdfminer` were not importable.
- **Adapter execution: NOT EVALUABLE.** Importing `src.ingestion.codal.adapter` fails before extraction with `ModuleNotFoundError: No module named 'jdatetime'`.
- **Prior failure log:** No failure log or diagnostic output was provided or inspected.

### 3. Fzar PDF Characteristics

- **Page count — CONFIRMED:** 3 pages, from `pypdf 6.21.2`.
- **Text layer — CONFIRMED:** `page.extract_text()` returned 1,768 characters for page 1, 2,349 for page 2, and 2,273 for page 3.
- **Relevant content — PARTIALLY CONFIRMED:** The extracted text includes monthly production/sales table headings on pages 1–2 and additional financial tables and explanatory text on page 3. The text layer contains table-like headers such as product/unit, production, sales quantity, sales price, and sales amount. Repeated headers and numeric sequences occur in the extraction, but the text output alone does not establish reliable visual row boundaries or which number belongs to which column.
- **Persian text and reading order — PARTIALLY CONFIRMED:** The extraction contains Persian Arabic presentation-form glyphs, Arabic/Persian digits, and mixed RTL/LTR strings. The characters are not absent, but the returned text is visibly interleaved and does not establish correct visual reading order or intact item labels.
- **Visual layout, selectable text, boundaries, cell coordinates, units, and source-to-value associations — NOT EVALUABLE:** I did not have an available PDF renderer or PDFium capability for visual inspection, coordinate extraction, or verification against the rendered page. The extracted text includes unit/header text and numbers, but I cannot establish the complete visual formatting, separators, or row associations from it alone.
- **Representative programmatic evidence:** Page 1’s extraction returns repeated table headings followed by long comma-separated numeric runs and Persian presentation-form text. This demonstrates that text is extractable; it does **not** prove accurate table extraction.

### 4. PDFium Evaluation

All six dimensions are **NOT EVALUABLE** because PDFium was unavailable and no PDFium output was produced. I have not simulated PDFium results.

| Dimension | Status | Evidence |
|---|---|---|
| Persian character integrity | NOT EVALUABLE | No PDFium output. |
| RTL reading order | NOT EVALUABLE | No PDFium output. |
| Table and row reconstruction | NOT EVALUABLE | No PDFium output. |
| Cell coordinates and bounding boxes | NOT EVALUABLE | No PDFium output. |
| Product-name/value relationship | NOT EVALUABLE | No PDFium output. |
| Digits, separators, and units | NOT EVALUABLE | No PDFium output. |

### 5. Existing Application Pipeline

The following describes the inspected code, not a successful run on Fzar:

- **Backend order and fallback — CONFIRMED from source:** `extract_cell_rows()` calls `_extract_tables_pdfplumber()` first and returns those rows if any are found; otherwise it calls `_extract_text_pypdf()`. If PDF text exists but produces no financial rows, it raises `CodalExtractionError`. See `src/ingestion/codal/pdf_extract.py`, `extract_cell_rows()` lines 292–312.
- **Optional table backend — CONFIRMED from source:** `_extract_tables_pdfplumber()` returns an empty list if `pdfplumber` cannot be imported. It identifies a likely label cell using `_pick_name_cell()`, then emits each other date-excluded pure-number cell as an `ExtractedCellRow`. The row includes a table-derived source row/column label and page number, but this code does not expose cell bounding boxes. See `pdf_extract.py`, lines 128–202.
- **Text fallback — CONFIRMED from source:** `_extract_text_pypdf()` extracts page text with `pypdf`; `_lines_from_text_pages()` splits it into lines, identifies numeric tokens, chooses a label from the text before or after those tokens, and emits one row per numeric token. See `pdf_extract.py`, lines 97–117, 205–289.
- **Persian labels and RTL — CONFIRMED from source:** `_pick_name_cell()` scores text containing Persian characters. `_name_from_line_and_tokens()` compares text before and after numeric tokens and may select the trailing text, but `fix_persian_rtl()` simply returns its input unchanged. See `pdf_extract.py`, lines 52–58, 61–76, 128–140, and 230–254.
- **Numeric parsing — CONFIRMED from source:** The adapter passes each extracted value string to `parse_amount()` and stores the result, which may be `None`. It normalizes digits in persisted text fields. See `src/ingestion/codal/adapter.py`, lines 79–97. The implementation of `parse_amount()` is outside the authorized file list and was not inspected, so its detailed behavior is **UNVERIFIED** here.
- **Adapter backend label — CONFIRMED from source:** It labels the result `pdfplumber_tables` when a source section ends in `_table`, otherwise `pypdf_text`. See `adapter.py`, lines 102–115.
- **Zero usable rows — CONFIRMED from source:** The adapter raises `CodalExtractionError` if it has no `RawLineInput` rows. See `adapter.py`, lines 99–100.
- **Production adapter path — PARTIALLY CONFIRMED:** `src/tests/test_codal_extraction.py` imports and calls `extract_raw_lines_from_pdf()` for its extraction tests (lines 14–19, 131–153, and 399–414). The inspected adapter itself calls `extract_cell_rows()`. `parser.py` defines a separate pypdf text path, but the inspected adapter does not import or call it. Whether another production entry point invokes `parser.py` is **UNVERIFIED** because the relevant files were outside the authorized list.
- **Test file evidence is not a test run:** Its real-sample test expects either `pdfplumber_tables` or `pypdf_text` and checks for labels and values, but I did not execute it.

### 6. Representative Row Comparison

A full comparison cannot be completed: PDFium output is unavailable, the adapter could not be imported, and the PDF was not visually rendered. The following table records the evidence that is available without treating extracted text as a verified financial row.

| Representative evidence | Original PDF / visual source | PDFium output | Existing application extraction | Final adapter mapping |
|---|---|---|---|---|
| Page 1 monthly production/sales table | Page 1 text layer includes Persian presentation-form headers for product/unit and production/sales fields, followed by numeric sequences. Exact visible row and value pairing is NOT EVALUABLE. | NOT EVALUABLE | Direct `pypdf` extraction returns the table text, but interleaves headings and values. Adapter execution was blocked by the missing `jdatetime` import dependency. | NOT EVALUABLE |
| Page 2 continuation of monthly table | Page 2 text layer includes repeated headers and numeric sequences. Exact visible row and value pairing is NOT EVALUABLE. | NOT EVALUABLE | Direct `pypdf` extraction returns text; no application `ExtractedCellRow` output was obtained. | NOT EVALUABLE |
| Page 3 other financial and explanatory content | Page 3 text layer includes financial-table headings, numeric sequences, and explanatory prose. A specific visible source row and its mapped value could not be confirmed. | NOT EVALUABLE | Direct `pypdf` extraction returns the page text. No application mapping output was obtained. | NOT EVALUABLE |

### 7. Failure Classification

- **CONFIRMED:** PDF text extraction failure is **not** established: `pypdf` successfully extracted text from all three pages.
- **PARTIALLY CONFIRMED:** The direct `pypdf` output has weak visible row/column organization and interleaves table headings and values. This supports concern about reading order and table reconstruction, but does not by itself prove the application’s failure on Fzar.
- **UNVERIFIED:** Source-PDF limitation; incorrect RTL order relative to the rendered page; exact table reconstruction failure; cell-coordinate or row-association failure; Persian normalization failure; item-name mapping failure; numeric parsing failure; and adapter integration failure on Fzar.
- **NOT EVALUABLE:** PDFium’s performance in all six required dimensions and the adapter’s final Fzar records. The adapter import was blocked by the missing `jdatetime` dependency.

### 8. Root-Cause Assessment

**Insufficient evidence to establish the actual Fzar extraction failure’s root cause.** Direct `pypdf` extraction confirms a text layer but produces output that does not make financial row/value associations clear. The adapter could not be run, PDFium was unavailable, and I could not compare either output to the visual table. It would be unsupported to attribute the failure to Persian text, RTL handling, table reconstruction, item-name mapping, or numeric parsing as a confirmed root cause.

### 9. Additional Evidence Required

- **`STAGE7_HANDOFF_INSTRUCTION.md`, `STAGE7_MASTER_WORKING_PACKET.md`, `WORKFLOW_RULES.md`, and `STAGE7_COMPLETED_CHECKLIST.md`:** The prompt names these as governing references, but its scope restriction says not to access additional repository files and to report the exact files needed first. These are the exact additional files needed to establish project-specific audit constraints and decisions; the four authorized source files do not contain those governing decisions.
- **A locally available PDFium installation or approved permission to use one:** Needed to produce and assess actual PDFium output on `pdf/Fzar.pdf`, including coordinates.
- **A usable environment containing the already-required `jdatetime` dependency, or permission to inspect the exact dependency setup needed to resolve that import:** Needed to invoke the adapter on Fzar and observe its final `RawLineInput` mappings. No package was installed.
- **A rendered view of `pdf/Fzar.pdf`:** Needed to verify visible table boundaries, exact page rows, reading direction, and source label/value associations against extraction output.
- **The actual failure log/diagnostic output, if one exists:** Needed to connect this investigation to the reported failure event rather than infer it from source code and the PDF alone.
- **`src/ingestion/codal/numbers.py` and the production entry-point caller, if detailed numeric parsing behavior and complete runtime path must be established:** They are outside the authorized source list. The inspected files do not establish the `parse_amount()` implementation or whether another production caller uses `parser.py`.

### 10. Recommended Next Step

Review the evidence and authorize the specific additional reads and environment access listed above. Then repeat the comparison on Fzar with PDFium output, rendered page references, and successful adapter output before assigning a root cause or proposing a production change.

### 11. Task Status

**060 · S7-AUD-011: PARTIAL**

The PDF’s page count and text-layer extraction, local package availability, and inspected source behavior were established. PDFium evaluation, visual inspection, adapter output, project-reference review, and the underlying failure log remain unresolved.

**Final verification:** No repository files were modified by me. No production code was changed. No tests were executed. No packages were installed or upgraded. No commits or pushes were made. At the start of this audit, `git status --short` already reported `M prompt.md`; I did not modify that file.