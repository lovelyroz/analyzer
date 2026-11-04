# Fzar pages 2–3: structured extraction validation

## Scope and environment

- Source of truth: `pdf_test/Fzar.pdf`; analyzed PDF pages 2 and 3 only.
- Reference files: `Fzar_table_sample.json` and `Fzar_page1_full_structured.json`; interpretations were checked against the PDF images.
- Python: 3.12.9; PyMuPDF: 2.1; MuPDF: 1.28.6.
- Method: `pymupdf.Page.find_tables()` with default line strategies. Pages rendered at 144 dpi and inspected.

## Tables detected

`find_tables()` returned one continuous table object per page. Visual inspection showed the detector combined multiple distinct sections into each object:

| Page | Detector tables | Detector dimensions | Visually separable sections |
|---|---:|---:|---|
| 2 | 1 | 54 rows × 62 columns | تولید و فروش؛ خرید مواد اولیه؛ انرژی |
| 3 | 1 | 21 rows × 39 columns | ادامهٔ انرژی؛ منابع و مصارف ارزی؛ سرعنوان توضیحات اصلاحات |

The row indices and PDF-point bounding boxes for each visual subsection are recorded in the JSON. The page 3 caption is preserved within the detected table cells; the explanatory note paragraphs below the financial grid are stored separately as outside-table text blocks. `clip=` experiments did not isolate the sections; the detector continued returning the same full-page table object.

## Header, column order, and periods

The rendered pages use right-to-left Persian tables. The major period headers are visually readable and preserved in the JSON per section, including cumulative periods ending 1404/07/30 and 1405/07/30, the one-month period ending 1405/07/30, and prior-period columns ending 1405/06/31 (including an amended/corrected group). The energy section also includes a forecast through 1405/09/30.

Visible metric headers include sales amount (million rial), sales rate (rial), sales quantity and production quantity; purchase amount/rate/quantity; energy consumption quantity/rate/amount; and foreign currency amount, rate and rial equivalent. The raw cell arrays and coordinates are preserved. However, `find_tables()` split visible columns into 62/39 slots and combined multiple numeric tokens in some returned cells, so extracted column indices cannot consistently be equated with visual financial columns. No unsupported mapping was imposed.

## Persian text and units

Raw Persian text is retained without reversal. The normalized representation applies NFKC, Persian character mapping and digit conversion, while numeric normalization is stored separately and only for unambiguous single-value cells. The PDF visibly identifies a page 2 production/sales row for open-pit ore with a 2.7% grade, unit ton; the energy rows show gas in cubic meters (page 2) and electricity in megawatt-hours (page 3). Visual reading of these labels is high confidence. Raw extracted text contains presentation-form letters, wrapped fragments and some non-logical extraction order.

Empty strings and null/merged cells remain distinct in the JSON; neither is changed to zero. A printed dot or a literal zero remains source text and is not inferred to mean the other.

## Financial reconciliation

The requested formula is `current cumulative = previous cumulative + current period`. The main page 2 product row exposes production/sales metrics and period groups visually, but its returned numeric cells contain merged tokens and cannot be mapped to each metric and period with confidence.

| Row | Metric | Previous cumulative | Current period | Current cumulative | Difference | Result |
|---|---|---:|---:|---:|---:|---|
| Page 2 production/sales row (wrapped product rows 6–11) | Sales amount | — | — | — | — | NOT_EVALUABLE |
| Page 2 production/sales row (wrapped product rows 6–11) | Sales quantity | — | — | — | — | NOT_EVALUABLE |
| Page 2 production/sales row (wrapped product rows 6–11) | Production quantity | — | — | — | — | NOT_EVALUABLE |

**Counts:** 0 PASS, 0 FAIL, 3 NOT_EVALUABLE. Dashes/nulls mean unavailable or unverified values, never zero. No rounding difference or discrepancy is claimed.

## Comparison with page 1

The reference page 1 JSON reports an 8 × 26 table and five product records, with four period groups partially mapped. Pages 2–3 contain additional purchase, energy and foreign-exchange sections. Here, the current PyMuPDF environment returned much wider, fragmented grids (54 × 62 and 21 × 39) and grouped numeric text in some cells. Thus, page 1's previous mapping cannot safely be copied to these pages. The report PDF itself visually confirms shared report dates and the repeated amended-period structure, but the pages do not share one simple table schema.

## Failures and ambiguity

- One `find_tables()` result spans several visually separate sections on each page.
- High column counts and merged text fragments prevent reliable numeric-to-header association.
- Persian extraction preserves source glyphs but may return presentation forms and split text; normalized text does not attempt to invent visual reading order.
- Page 3 explanatory note text is outside the detected financial grid; it is retained separately with coordinates.
- Although PyMuPDF returned raw cells and coordinates, plausible dimensions alone do not establish correct financial extraction.

## Assessment

Pages 2 and 3 were extracted into a raw, coordinate-preserving JSON structure and visually reviewed. Their major column groups, period labels and units are identifiable from the page images, but the `find_tables()` cell grid does **not** reliably preserve numeric column associations in this environment. Persian source text is retained, with visual verification needed for logical reading order.

**Recommendation:** continue only with a controlled, comparative extraction experiment. Do not use this output for automatic financial calculations or treat the method as ready for a broader production corpus until section segmentation and cell-to-header mapping are improved and revalidated.
