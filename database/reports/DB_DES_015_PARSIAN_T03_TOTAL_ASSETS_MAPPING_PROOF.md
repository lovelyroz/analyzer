# DB-DES-015 — Parsian T03 / Total Assets Mapping Proof (Evidence-Limited Draft)

**Status:** PROOF OF DESIGN ONLY — candidate mapping; not owner-approved, not production-ready  
**Date:** 2026-11-18  
**Scope:** One row and two comparative value columns in Parsian periodic financial statement candidate T03  
**Depends on:** DB-DES-008, DB-DES-011, DB-DES-013, DB-DES-014, BANK_PERIODIC_METRIC_DIMENSION_MAPPING_PROPOSAL.md, PARSIAN_PERIODIC_ANNOTATION_MAP_DRAFT.md, PARSIAN_PERIODIC_REPORT_3_STRUCTURAL_REVIEW.md

## 1. Why T03 was selected

T03 is the candidate table titled `صورت وضعیت مالی` (statement of financial position). It is suitable for a first mapping proof because its principal values are point-in-time balances. This permits a focused test of the distinction between:
- a physical column and its complete Header path;
- a row-axis label and its canonical metric candidate;
- the reporting/measurement date and the audit-status qualifier;
- the source's unit/scale and the canonical storage unit.

This is a single-row proof, not a complete mapping of T03.

## 2. Evidence and provenance limitations

The current corrected sample workbook is recorded as:
- file: `excel/parsian_periodic.xlsx`
- SHA-256: `95f94e739632e48ae6552c562ecbf6c3e8182848718d17977f69bc984a6638b0`
- worksheet: `Recovered_Sheet1`
- used range: `A1:L411`

The available detailed cell-value/OOXML report (`parsian_periodic_report_3.md`) records an earlier two-sheet workbook package with SHA-256 `69186f1ad2b0e481a3588f2731b7027b0a9d9a543d1ca17fd24fc71d8c5aca06`. It includes detailed header, label, and numeric-cell evidence for Recovered_Sheet1, but there is no retained-sheet XML hash proving byte identity with the corrected workbook. The corrected workbook's annotation audit independently confirms the gray extraction range includes B82:C94, but does not by itself re-confirm every literal cell value/header text listed below.

Accordingly, all exact cell text and values below are **historical detailed evidence requiring confirmation against the corrected XLSX** before approval. This document does not claim direct inspection of the XLSX.

## 3. Physical sample

### 3.1 Candidate table geometry

| Attribute | Evidence |
|---|---|
| Candidate table | T03 — صورت وضعیت مالی |
| Title cell | A77 |
| Candidate bounds | A79:C119 |
| Header rows | 79–80 |
| Header/label column | A |
| Data columns | B and C |
| Relevant sub-table | T03 child marker A81 — دارایی‌ها |
| Candidate child partition | Rows 81–94 |
| Target row | 94 |

The bounds and child partition are evidence-supported candidates, not owner-approved production bounds. See the annotation map and structural review for the unresolved geometry/approval conditions.

### 3.2 Header evidence for the two data slots

Detailed report-3 cell inventory records:

| Coordinate | Literal source text | Structural role |
|---|---|---|
| A79:A80 | `شرح` at A79; merged vertically through A80 | Row-label header |
| B79 | `دوره منتهی به ۱۴۰۳/۰۶/۳۱` | Current measurement-date header |
| B80 | `حسابرسی نشده` | Audit-status qualifier for B |
| C79 | `تجدید ارائه شده ۱۴۰۲/۱۲/۲۹` | Comparative/restated measurement-date header |
| C80 | `حسابرسی شده` | Audit-status qualifier for C |

The recorded merged ranges include A79:A80 and E79:E80. The target table candidate ends at column C; E is outside this candidate. Do not add E merely because a blue header exists elsewhere in the worksheet.

The resolved candidate paths are therefore:

- B: `[دوره منتهی به ۱۴۰۳/۰۶/۳۱, حسابرسی نشده]`
- C: `[تجدید ارائه شده ۱۴۰۲/۱۲/۲۹, حسابرسی شده]`

These paths preserve the two distinct header levels. Do not collapse audit status into the date text.

### 3.3 Row-axis evidence

The detailed report-3 yellow-cell inventory records:

- A81: `دارایی‌ها` — child/sub-table marker;
- A94: `جمع دارایی‌ها` — target row label.

Candidate row-axis path:

`[دارایی‌ها, جمع دارایی‌ها]`

The parent/child partition and exact ownership still require owner approval. This path is a candidate based on the recorded marker and row label.

### 3.4 Target value evidence

The detailed report-3 gray-cell inventory records:

| Coordinate | Stored value |
|---|---:|
| B94 | 5,139,354,983 |
| C94 | 4,848,153,182 |

The corrected annotation map also lists B82:C94 among gray extraction coordinates, but the two literal values above still require re-confirmation against the corrected workbook package because of the source-hash discrepancy in §2.

## 4. Candidate semantic mapping

| Mapping component | Candidate resolution | Status |
|---|---|---|
| Report family | PERIODIC_FINANCIAL | Candidate scope |
| Industry | BANK | Candidate scope; company/industry binding must be verified from authoritative company setup |
| Parent table | T03 / صورت وضعیت مالی | Candidate |
| Child node | T03 / دارایی‌ها | Candidate |
| Row-axis path | دارایی‌ها → جمع دارایی‌ها | Evidence-supported candidate |
| Canonical metric concept | Total assets / جمع دارایی‌ها | Candidate concept; not an approved stable metric code |
| Dimension set | Empty, if the canonical metric is company-wide total assets | Candidate; confirm no consolidation/entity dimension applies |
| Temporal kind | INSTANT | Strong semantic candidate because this is a statement-of-financial-position balance at a stated date |
| Duration basis | NOT APPLICABLE | Required for INSTANT under DB-DES-011 |
| Current measurement date | ۱۴۰۳/۰۶/۳۱ | Explicit in B79 |
| Comparative measurement date | ۱۴۰۲/۱۲/۲۹ | Explicit in C79 |
| Current audit status | حسابرسی نشده | Explicit qualifier in B80 |
| Comparative audit status | حسابرسی شده | Explicit qualifier in C80 |
| Source/canonical unit and scale | UNRESOLVED | Must not infer from magnitude or general convention |
| Scenario | Likely ACTUAL, but not approved by this proof | Must be bound by the approved interpretation standard |

### 4.1 Why the two columns are not interchangeable

B and C refer to different measurement dates and different audit statuses. They are not two values for one FinancialPeriod, nor should audit status be discarded. Each candidate fact has its own INSTANT period and ReportVersion/source provenance, while the audit-status qualifier participates in version eligibility/ranking according to the approved report-version contract. It must not automatically become a financial dimension merely because it appears in a Header level.

The phrase `تجدید ارائه شده` is evidence that C is a restated comparative column, but the exact ReportVersion relationship and its ranking must be resolved by the ReportVersion provenance/version rules. The Header phrase alone does not create a new ReportVersion.

### 4.2 Why unit/scale blocks canonical admission

The available header text shown above does not explicitly state currency or scale. The numeric magnitude is not valid evidence for deciding Rial, million Rial, or another scale. Until an approved source rule or explicit source evidence establishes the unit and scale:
- do not convert or rescale B94/C94;
- do not populate canonical currency/unit fields;
- do not admit these values as canonical FinancialFacts.

This is an intentional fail-closed result, not a failure of the mapping model.

## 5. What this proof establishes

1. The full column Header path is richer than the date label: it includes an independent audit-status level.
2. The row-axis path identifies a total asset balance within the assets section.
3. The semantic candidate is a stock/INSTANT fact, not a duration flow; therefore no YTD/STANDALONE basis is applicable.
4. Current and comparative columns have different measurement dates and must resolve to different FinancialPeriods.
5. Audit status is a source/version qualifier and should not be silently treated as a dimension or stripped from provenance.
6. A semantically recognizable metric is still not ingestible if unit/scale or source-package evidence is unresolved.

## 6. Explicit unresolved gates

Before this sample can be promoted to an approved mapping:

1. Re-open the corrected XLSX with SHA-256 `95f94e739632e48ae6552c562ecbf6c3e8182848718d17977f69bc984a6638b0` and confirm A79:C80, A81, A94, B94, and C94 literally.
2. Confirm owner-approved T03 bounds and the A81–A94 child partition, including whether the child Header is inherited from the parent.
3. Confirm the company's BANK classification and whether the table reports consolidated/company-level facts or another entity scope.
4. Establish the explicit source unit and scale for the two value columns.
5. Bind the concept to an approved stable FinancialMetric code and approve the empty-dimension-set policy (or the correct explicit dimension set).
6. Confirm that the comparative restated column's ReportVersion/audit ranking and publication provenance are represented independently of the Header text.
7. Validate the same Header and row-axis semantics against a genuinely independent later-period Parsian periodic workbook. Reports 1–3 are analyses of the same sample package, not independent-period drift evidence.

## 7. Result and next step

**Result: PARTIAL PROOF — semantic shape resolved; canonical admission blocked.**

This sample demonstrates the DB-DES-014 mapping structure, but it does not approve a production mapping or close DB-ING-006 / Task 033.

The next useful evidence action is to verify the listed coordinates and unit/scale against the corrected XLSX itself. If the corrected workbook is not available in the current project workspace, the owner must supply that exact file; do not substitute the older package or infer the missing unit.

No ORM, migration, runtime code, database data, or tests were changed.
