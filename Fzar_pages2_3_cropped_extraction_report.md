# Fzar pages 2–3: cropped-section extraction experiment

## Environment

- Python: **3.12.9**
- PyMuPDF distribution: **2.1**
- `pymupdf.__version__`: **2.1**
- `fitz.VersionBind`: **2.1**
- `fitz.VersionFitz` (MuPDF engine): **1.28.6**
- Method: copied source pages in memory, applied an independent CropBox per section, then ran `find_tables()` on each crop. Crop-relative cell boxes were translated by crop x0/y0 back to original PDF coordinates.
- Each crop was rendered at **216 dpi** and compared with the original page image. No source or prior extraction artifact was modified.

PyMuPDF is the Python package/bindings; MuPDF is its underlying engine. `VersionFitz` is the MuPDF engine value, not the PyMuPDF distribution version.

## Boundaries and extraction comparison

The rendered pages confirm section rules at approximately page 2 y=345.835 and 465.863, and page 3 y=127.890 and 247.821 points. For page 3 energy, an exact-boundary crop returned no table; a small y=55–133 crop added whitespace around the same section and did not include the adjacent FX table. The page 2 energy crop retained the source text but `find_tables()` returned no table.

| Section | Full-page slice (rows×cols; non-empty cells) | Cropped find_tables (rows×cols; non-empty cells) | Unambiguous numeric cells | Ambiguous numeric-like cells |
|---|---:|---:|---:|---:|
| Production and sales (p.2) | 34×62 (191) | 12×25 (133) | 22 | 79 |
| Raw-material purchases (p.2) | 12×62 (93) | 10×19 (81) | 0 | 54 |
| Energy (p.2) | 8×62 (82) | no table (0) | 0 | 0 |
| Energy continuation (p.3) | 8×39 (77) | 4×23 (57) | 20 | 4 |
| Foreign-currency sources and uses (p.3) | 12×39 (150) | 9×22 (119) | 0 | 84 |

The original full-page detector returned one object per page: page 2 at 54×62 and page 3 at 21×39. The row slices above use the visual section row indices from the existing artifact; they are comparison baselines, not independent tables.

## Header association and visual findings

- **Page 2 production/sales:** reduced from a 34×62 full-page slice to a 12×25 crop. The cropped period and leaf-metric bands align with the numeric cells. Twenty-two actual numeric values are mapped to a period and metric. Seventy-nine cells whose text layer resembles zero are rendered as centered dot placeholders and remain ambiguous. The detected grid ends around source x=741.0 and omits the full product-description column (approximately x=740.2 to x=762.4); crop text blocks preserve the label.
- **Page 2 raw-material purchases:** reduced from 12×62 to 10×19. Headers localize better, but 54 numeric-like cells visibly render as dots; none is interpreted as numeric zero.
- **Page 2 energy:** the visual section is clear, but the crop returned no table. Raw text blocks and original-page coordinates are preserved; no column mapping is claimed.
- **Page 3 energy continuation:** with small padding, reduced from 8×39 to 4×23. Twenty values map to visible period/metric columns. Four zero-like cells render as dots and remain ambiguous. Product type and unit are visually legible.
- **Page 3 FX sources/uses:** reduced from 12×39 to 9×22. The headers localize, but 84 zero-like cells render as dots and remain ambiguous.

Raw extracted text, normalized text, row/column indices, crop-relative boxes, original-page boxes, and section header maps are included in the JSON. Empty and merged cells remain distinct. Dot placeholders are not coerced to zero. Persian labels and wrapped text were checked on the rendered crops.

## Financial validation

The cumulative check was applied only when row, metric, period, unit and rendered cell value were clear. A tolerance of 0.000001 is used for the source-text quantity residual.

| Section / row | Metric | Previous cumulative | Current period | Current cumulative | Difference | Result |
|---|---|---:|---:|---:|---:|---|
| p2_sales_production row 3 — sales_amount_million_rial | 25379857 | 6149881 | 31529738 | 0 | PASS |
| p2_sales_production row 3 — sales_quantity | 656997.71 | 138452.66999999998 | 795450.3799999999 | -8E-11 | PASS |
| p2_sales_production row 3 — production_quantity | 501333 | 131270 | 632603 | 0 | PASS |
| p3_energy_continuation row 2 — energy_amount_million_rial | 6981 | 963 | 7944 | 0 | PASS |
| p3_energy_continuation row 2 — energy_consumption_quantity | 601 | 56 | 657 | 0 | PASS |
| p2_sales_production row 2 — production_quantity | — | 19815 | 19815 | — | NOT_EVALUABLE |

**Counts:** 5 PASS, 0 FAIL, 1 NOT_EVALUABLE. The item-level production check stays not evaluable because its previous-period source cell is a dot. Three subtotal checks on sales amount, sales quantity and production quantity pass; two energy checks (amount and consumption quantity) pass. Rates are non-additive and were not checked.

## Assessment and next experiment

Geometric cropping materially improves section segmentation for four of five regions with detected tables: 34×62 → 12×25, 12×62 → 10×19, 8×39 → 4×23, and 12×39 → 9×22. It improves cell-to-header association enough to support five visually grounded PASS checks. It does not recover the page 2 energy table, and the sales product label falls outside the cropped detector grid. The extractor also confuses printed dots with zero-like text. Therefore, cropping is a real improvement but is not yet a reliable general-purpose automatic extraction solution.

**Recommended next experiment:** retain cropped `find_tables()` for sections it detects, use coordinate-aware text spans to cover the page 2 energy section and omitted product labels, and explicitly classify visual dot placeholders before interpreting numbers. Continue to preserve raw cells and abstain whenever the image/header mapping is uncertain.
