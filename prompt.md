# Task: Fzar PDF — Targeted Extraction Follow-up Experiment

**Task type: Experimental analysis and extraction only — NO production code changes.**

## Objective

Continue the previous Fzar PDF extraction experiments using the existing cropped extraction artifacts.

The previous experiment demonstrated that geometric cropping improves table segmentation, but three important limitations remain:

1. Product descriptions are not reliably connected to their numeric rows.
2. The page 2 energy table is not detected by `find_tables()`.
3. Printed dot placeholders can be mistaken for zero-like characters in the PDF text layer.

Investigate these three issues with a targeted, evidence-based experiment. Do not repeat the previous full extraction workflow.

## Allowed input files

Read only these files:

- `pdf_test/Fzar.pdf`
- `Fzar_pages2_3_cropped_extraction.json`
- `Fzar_pages2_3_cropped_extraction_report.md`

You may inspect the existing page images or render temporary crops from the PDF.

## Task 1 — Product description and numeric-row association

Focus on page 2, production and sales section.

The previous extraction report states that the detected table ends around x=741.0, while the product-description column extends approximately from x=740.2 to x=762.4.

Investigate whether coordinate-based text spans can reliably recover the complete product description and associate it with the correct numeric row.

Requirements:

- Extract text spans with their original-page coordinates.
- Preserve raw Persian text exactly as extracted.
- Normalize text separately; never overwrite raw text.
- Identify row boundaries using visual grid lines and text-span coordinates.
- Associate product descriptions with numeric rows only when vertical alignment and visual evidence support the association.
- Do not infer a product name from neighboring rows.
- Preserve wrapped descriptions as one logical label only when their line grouping is visually supported.
- Include the associated numeric row index and its original-page bounding box.
- If association is uncertain, explicitly mark it as `AMBIGUOUS`.

Important: Do not treat the fact that a text span is close to a row as sufficient evidence by itself. Verify against a rendered image.

## Task 2 — Page 2 energy section

The previous experiment found that `find_tables()` returned no table for this section, despite a visible grid.

Investigate an alternative extraction method based on:

- Text spans and their coordinates.
- Horizontal and vertical grid-line coordinates, if available.
- Visual row and column boundaries.
- Alignment of numeric text within the apparent cells.

Requirements:

- Do not depend on `find_tables()` succeeding.
- Attempt to reconstruct the table structure from geometric evidence.
- Preserve original-page coordinates.
- Identify period headers and metric headers separately.
- Map a value to a period and metric only if both associations are visually supported.
- Keep missing cells distinct from printed dots and numeric zero.
- Do not force a complete table if the available evidence is insufficient.

The output must distinguish:
- `NUMERIC`
- `DOT_PLACEHOLDER`
- `EMPTY`
- `TEXT`
- `AMBIGUOUS`

## Task 3 — Dot placeholder versus numeric zero

Investigate the dot/zero ambiguity in the following sections:

- Page 2 raw-material purchases.
- Page 3 foreign-currency sources and uses.
- Any other section where the previous JSON marked numeric-like cells as ambiguous.

Requirements:

- Inspect the original rendered PDF at adequate resolution.
- Compare the visual glyph with the raw PDF text-layer character.
- Record the original-page bounding box.
- Determine whether the visual symbol is a centered dot, a genuine zero, an empty cell, or another symbol.
- Do not classify based only on the extracted Unicode character.
- Do not convert an ambiguous symbol into zero.
- If visual evidence is insufficient, retain `AMBIGUOUS`.

Produce a classification summary with counts for each state and section.

## Task 4 — Financial validation

Only perform reconciliation when all required values have:

- A verified row identity.
- A verified period association.
- A verified metric association.
- A verified unit.
- A visually confirmed numeric value.

Use:

`Current cumulative = Previous cumulative + Current period`

Use exact decimal arithmetic (`Decimal`), not binary floating-point arithmetic.

Do not use a tolerance to conceal incorrect extraction. If source precision creates a legitimate rounding difference, document it explicitly.

Do not perform reconciliation using inferred zeros or ambiguous values.

Report:
- PASS
- FAIL
- NOT_EVALUABLE

A successful arithmetic reconciliation does not, by itself, prove that the row label or column mapping is correct.

## Task 5 — Final technical assessment

Answer these questions explicitly:

1. Can the product-description column be reliably associated with numeric rows using coordinate-based text spans?
2. Can the page 2 energy table be reconstructed without `find_tables()`?
3. Can dot placeholders be distinguished reliably from numeric zeros in the tested sections?
4. Which sections now have enough evidence for reliable structured extraction?
5. Which sections remain unsuitable for automatic financial extraction?
6. Does this experiment justify another targeted experiment, or have we reached the practical limit of this PDF extraction approach?

Do not claim success merely because a table-shaped JSON structure can be produced.

## Required output files

Create:

1. `Fzar_targeted_extraction_followup.json`
2. `Fzar_targeted_extraction_followup_report.md`

The JSON must preserve:
- Source page and section.
- Original-page coordinates.
- Raw text and normalized text as separate fields.
- Row and column identities, where established.
- Header associations and their evidence.
- Cell classification.
- Confidence or ambiguity status.
- Financial validation details.

The Markdown report must include:
- Environment and exact library versions.
- Methods used.
- Visual verification approach.
- Results for each task.
- Quantitative summary.
- Financial validation.
- Explicit limitations and final recommendation.

## Strict restrictions

- Do NOT modify production source code.
- Do NOT modify tests.
- Do NOT modify configuration or dependencies.
- Do NOT install or upgrade packages.
- Do NOT modify any existing extraction artifact.
- Do NOT modify `WORKFLOW_RULES.md` or any Stage 7 master/canonical document.
- Do NOT perform Git operations, commits, pushes, or branch changes.
- Do NOT process other PDFs.
- Do NOT invent values, labels, units, dates, or missing cells.
- Do NOT claim visual verification unless the relevant rendered region was actually inspected.

This is an experimental analysis task. Preserve uncertainty rather than manufacturing completeness.

## Final response

Report both output filenames, summarize the findings for all three target problems, list unresolved limitations, and state clearly whether the extraction method is ready for production use.

Do not run the project's test suite.