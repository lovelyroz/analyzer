# DB-STD-002 / DB-STD-003 — Cross-Task Reconciliation

**Date:** 2026-11-19  
**Purpose:** Consolidate existing evidence and separate completed sub-deliverables from genuine blockers. This document does not approve unresolved financial semantics or authorize implementation.

## 1. Executive result

| Task | Evidence/design already complete | Genuine remaining gate | Status |
|---|---|---|---|
| DB-STD-002 — Monthly activity reports | Six-category parent taxonomy approved; three bank workbooks reviewed; 18 candidate Metrics and 7 candidate Dimensions inventoried; owner-confirmed rules for issuer selection, blank-label rows, restatement selection, ambiguity questions and non-double-counting recorded | Final canonical Metric/Dimension and temporal/value contracts; several semantic owner decisions; complete coverage validation; explicit owner approval | PARTIAL |
| DB-STD-003 — Periodic financial reports | Independent report family defined; 17-entry bank periodic Header dictionary v1.1 exists; two bank samples compared; 16 initial Headers found in both and 17th added by decision; owner clarified period columns and extraction-scope principle | Restatement basis/bridge; supplementary and multi-level table scope; comprehensive-income output defect; representative validation of 3/6/9/12-month reports; issuer identity for the purported third sample | PARTIAL |

The completed work below must not be re-run as if it were absent. The tasks remain PARTIAL because their remaining gates are substantive, not merely because their reports are unfinished.

## 2. DB-STD-002 — monthly activity reports

### 2.1 Completed and evidenced

1. The parent taxonomy is exactly six peer categories, approved by the owner on 2026-11-11:
   - operating income;
   - non-operating income;
   - operating expenses;
   - non-operating expenses;
   - balances and positions;
   - operational amounts and volumes.
2. The taxonomy applies only to monthly activity reports; it must not be reused for periodic 3/6/9/12-month financial statements.
3. The monthly workbooks of Saman, Mellat and Saderat have been reviewed. Saderat issuer identity was explicitly confirmed by the owner; issuer identity must be selected/confirmed by the user on ingestion, not guessed from filename or workbook layout.
4. The consolidated candidate register contains 18 candidate Metrics and 7 candidate Dimensions. These remain candidates, not approved canonical definitions.
5. The following rules are already established and should not be reopened without new evidence:
   - a data row whose first/label cell is blank is ignored as a whole;
   - restated/final values are the primary analysis values; earlier/original and adjustment values are retained as related evidence and not double-counted;
   - an ambiguous Header or economic meaning stops processing for a specific clarification; unresolved ambiguity rejects the whole report;
   - totals and detailed rows are not both counted as independent economic inputs;
   - missing disclosure is not zero;
   - sign alone does not determine income versus expense;
   - source Header text is preserved; company-specific Header mapping is distinct from the six-category parent taxonomy.
6. Cross-bank observations support these candidate families across all three samples: loan income, deposit income, debt-security income, investment income, fee/commission income, deposit-interest expense, financial expense, fee/commission expense, loan balances/flows, customer-deposit balances/flows, and bank investment balances. Three-sample occurrence is evidence, not final semantic approval.

### 2.2 Remaining blockers — no guessing

| Blocker | Why it remains open | Safe current treatment |
|---|---|---|
| Non-operating profit/loss rows and dual-nature items | Positive/negative values and combined profit/loss labels do not define canonical category by themselves | Preserve source meaning; do not assign income/expense category until semantic rule is approved |
| Loan/guarantee receivable rows | Labels such as borrowers for paid letters of credit/guarantees do not uniquely establish income, receivable, recovery or fee nature | Keep unresolved source-specific mapping; block canonical admission |
| Financial expense classification | Observed in multiple tables but operating/non-operating classification is not yet evidenced uniformly | Do not force into either expense category |
| FX and multi-currency | FX open position is observed, but currency amount scale, FX income/expense and rate-date semantics are not complete | Preserve position/FX attributes separately; no inferred transaction volume or conversion |
| Net change versus gross activity | Net movement in investment balances is not gross purchase/sale volume | Store only the evidenced concept; do not derive gross flows |
| Restatement/reclassification embedded in flows | Saderat note indicates some flows include adjustment/reclassification without a separately identifiable adjustment column | Keep source-specific quality/interpretation flag; do not generalize from one sample |
| Coverage completeness | Saman explicitly warns that operating income/expense summaries are incomplete; absence in a sample is not evidence of zero or non-existence | Mark coverage limitations; do not treat unobserved categories as zero |
| Final canonical register and approval | Current 18 Metrics / 7 Dimensions are candidates, and Gates C–G are not approved | Do not mark parent standard complete or authorize implementation |

### 2.3 Decision

DB-STD-002's parent taxonomy and cross-bank evidence collection are complete sub-deliverables. The full monthly banking standard cannot be marked DONE until Metric/Dimension, temporal/value, reconciliation, cross-bank validation and owner-approval gates are completed. Other industries require their own real samples; the bank standard must not be silently generalized to all industries.

## 3. DB-STD-003 — periodic financial reports

### 3.1 Completed and evidenced

1. Periodic financial reports are a separate report family from monthly activity reports. It covers 3-, 6-, 9- and 12-month fiscal periods; 12 months is the annual report.
2. “Cumulative/YTD” describes the temporal basis of flow values, not a separate report type. It does not apply to point-in-time balance-sheet facts.
3. The bank periodic Header dictionary exists at `database/dictionaries/header_dictionary.json`, version 1.1, with 17 Standard Headers and source Header variants.
4. The two compared samples are:
   - Saderat six-month report ending 1403/06/31, with issuer identity confirmed by the owner;
   - Parsian periodic workbook evidence recorded in `parsian_periodic_report_1.md` and follow-up reports.
5. All 16 initial Standard Headers were observed in both samples; the 17th was added by a later owner decision. Two punctuation-only source variants were reconciled under their existing Standard Headers. The phrase “توضیحات در خصوص تغییرات بااهمیت” in the second sample is not a principal Header and was not added.
6. The fiscal year in the validated sample runs 1403/01/01 through the end of Esfand.
7. The owner-confirmed Parsian column meanings are:
   - B: current six-month period ending 1403/06/31, unaudited;
   - C: comparative six-month period ending 1402/06/31, audited and restated;
   - D: prior full fiscal year ending 1402/12/29, audited and restated.
8. The approved scope rule is inverse: each extractable section must map to one of the 17 Standard Headers. Non-matching sections identified in the two samples are out of extraction scope; a page-level summary heading does not remove an otherwise matching standard section. Remaining in-scope Headers use the canonical database contract; no extra analytical taxonomy is created.
9. The user has confirmed that the dictionary file's current version is the working baseline. This is a design artifact, not proof that a software standard is activated.

### 3.2 Additional sample identity control

`postbank_periodic_report_1.md` is titled as a Postbank quarterly workbook inspection, but its own ambiguity register says the issuer/ticker must be confirmed because the filing title says Parsian while the filename says Postbank. It is not an admissible third-bank validation sample until issuer identity is established from an authoritative filing cover or exchange record. Do not count it as Postbank or Parsian evidence by filename.

Reports 1–3 for Parsian are audits/analyses of the same workbook, not three independent reporting-period samples. They cannot establish layout drift across different periods.

### 3.3 Remaining blockers — no guessing

| Blocker | Why it remains open | Safe current treatment |
|---|---|---|
| Restatement/reclassification basis | Comparative values are labelled restated, but the source evidence does not provide the reason or adjustment bridge | Keep audited/restated status separate from the numeric fact; do not invent restatement cause or bridge |
| Supplementary tables and multi-level structures | The 17-Header dictionary establishes principal sections, but some nested/supplementary tables need explicit in-scope/out-of-scope decisions and parent-child interpretation | Extract only when the table's meaning and relationship to a Standard Header are unambiguous |
| Comprehensive-income statement output defect | Existing review records a system/output error for this statement; the source-level mapping alone cannot establish whether the defect is in extraction, transformation or display | Keep this path blocked pending reproduction and root-cause evidence; do not mask it by excluding the statement |
| 3/6/9/12-month generalization | Current validated samples are six-month reports; a quarterly/three-month sample and a nine-month sample are needed to validate duration rules and year-end behavior | Do not infer standalone-quarter values or generalize all duration semantics from six-month samples |
| Third-sample identity | Postbank-named report conflicts with the issuer name in the filing evidence | Do not count it until issuer is confirmed |
| Temporal type per table | Flow, stock, ratio, quantity and narrative data coexist in a workbook; “period ended” alone is insufficient to classify every value | Assign duration/instant basis per fact/table only from its own header and row semantics |

### 3.4 Decision

The 17-Header dictionary and two-sample comparison are completed sub-deliverables. DB-STD-003 remains PARTIAL until the restatement basis, supplementary structures, comprehensive-income defect and representative 3/6/9/12-month validation are resolved. The dictionary is not an implementation-ready ingestion profile.

## 4. Work sequencing to prevent loops

1. Do not repeat the completed taxonomy, three-bank inventory, 17-Header dictionary creation, or two-sample comparison.
2. Resolve DB-STD-002 semantic blockers as a grouped decision set, then freeze the banking candidate register and complete the temporal/value and reconciliation gates.
3. For DB-STD-003, first establish an authenticated three-month and nine-month sample with verified issuer identity; then handle restatement and supplementary tables against the same standard.
4. Reproduce and isolate the comprehensive-income output defect separately; do not let a display/output issue silently change extraction scope.
5. Only after these gates are complete should either task be marked DONE. No code, ORM, schema, migration, database or tests were changed/run for this reconciliation.
