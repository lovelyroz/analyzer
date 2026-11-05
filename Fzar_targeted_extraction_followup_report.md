# Fzar targeted extraction follow-up

## Environment and method

- Python **3.12.9**; PyMuPDF distribution **2.1**; `fitz.VersionBind` **2.1**; MuPDF engine **1.28.6**.
- Rendered and inspected the relevant source regions at **216 dpi**. The original PDF and the previous extraction artifacts were not modified.
- Product descriptions were extracted as text spans with original-page boxes and checked against visible row rules. Page 2 energy was reconstructed from vector line rectangles and span coordinates without relying on `find_tables()`.
- Raw Persian text is preserved separately from NFKC and digit-normalized text. Every ambiguous zero-like cell is retained with its original-page box and raster-based classification.

## Results

### 1. Product description and numeric-row association

The rightmost description column can be associated with the corresponding numeric row in this page 2 sales table: **10 visible row labels associated; 0 ambiguous**. The long ore-extraction description occupies row index 2 in the cropped extraction and fits inside that row's rendered horizontal boundaries; its text is not borrowed from adjacent rows. Other visible row labels likewise fall within their own row boxes. This is reliable for the examined table and does not prove portability to different Codal layouts.

### 2. Page 2 energy section

The vector geometry exposes **1 data row and 24 columns**. The row and columns, source-page cell boxes, raw/normalized span text, and separate period/header bands are recorded in the JSON. Text spans align to the visible row, so the table shape is recoverable without `find_tables()`.

The reconstruction remains **partial**: some date glyphs in the PDF text layer differ from the rendered header (one span normalizes to 1405/06/13 while the inspected raster reads 1405/06/31), and several metric labels span combined header cells. Numeric values are kept as `NUMERIC` by geometric column but period/metric fields remain unmapped where the evidence does not securely establish both. Dot, empty, text, and ambiguous states remain distinct.

### 3. Dot placeholder versus numeric zero

The rendered cells previously flagged as zero-like show centered dots, while the text layer contains Arabic zero U+0660. For this PDF, the inspected cells are classified as `DOT_PLACEHOLDER`; none is converted to numeric zero. This applies to the inspected cells, not all Codal PDFs.

| Section | NUMERIC | DOT_PLACEHOLDER | EMPTY | TEXT | AMBIGUOUS |
|---|---:|---:|---:|---:|---:|
| p2_sales_production | 22 | 79 | 148 | 32 | 19 |
| p2_raw_material_purchases | 0 | 54 | 84 | 27 | 25 |
| p2_energy | 9 | 6 | 5 | 4 | 0 |
| p3_energy_continuation | 20 | 4 | 19 | 33 | 16 |
| p3_fx_sources_uses | 0 | 84 | 50 | 35 | 29 |
| **Total** | **51** | **227** | **306** | **131** | **89** |

The dot audit contains **227 individually boxed cells**, including the six zero-like glyphs in the reconstructed page 2 energy row.

## Financial validation

Formula: `Current cumulative = Previous cumulative + Current period`. Exact `Decimal` arithmetic was used with zero tolerance.

| Section / row | Metric | Previous | Period | Cumulative | Exact difference | Result |
|---|---|---:|---:|---:|---:|---|
| p2_sales_production row 3 | sales_amount_million_rial | 25379857 | 6149881 | 31529738 | 0 | PASS |
| p2_sales_production row 3 | sales_quantity | 656997.71 | 138452.66999999998 | 795450.3799999999 | -8E-11 | FAIL |
| p2_sales_production row 3 | production_quantity | 501333 | 131270 | 632603 | 0 | PASS |
| p3_energy_continuation row 2 | energy_amount_million_rial | 6981 | 963 | 7944 | 0 | PASS |
| p3_energy_continuation row 2 | energy_consumption_quantity | 601 | 56 | 657 | 0 | PASS |
| p2_sales_production row 2 | production_quantity | N/A (printed dot) | 19815 | 19815 | N/A | NOT_EVALUABLE |

**Counts:** 4 PASS, 1 FAIL, 1 NOT_EVALUABLE. The sales quantity source strings leave an exact residual of **-8E-11**. It may arise from source precision, but there is no printed precision rule to justify rounding it away, so it remains FAIL. The item-level production check is NOT_EVALUABLE because its previous-period cell is a printed dot.

## Technical assessment

1. **Product descriptions:** Yes, coordinate spans and visible row rules associate the descriptions with numeric rows in this page 2 section.
2. **Page 2 energy:** Partially. Grid geometry and one data row are reconstructed, but some value-to-period/metric mappings are not secure.
3. **Dots versus zeros:** Yes for the inspected cells in this PDF; the rendered marks are centered dots despite U+0660 in the text layer.
4. **Enough evidence for structured extraction:** The page 2 sales labels and the page 3 energy continuation have the strongest row, header, and visual evidence. Purchases and FX cells remain mostly placeholders; p2 energy has incomplete semantic mapping.
5. **Unsuitable for automatic financial extraction:** Page 2 energy, page 2 raw-material purchases, and page 3 FX. Dot handling also requires raster-aware checks.
6. **Next step:** One more targeted experiment on an independent Codal layout is justified to test generalization. This PDF alone does not justify production use.

### Final recommendation

**Not ready for production use.** This experiment provides useful page-specific evidence, but incomplete energy mapping, source text/raster discrepancies, and exact arithmetic residuals prevent dependable unattended financial extraction.
