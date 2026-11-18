# DB-DES-016 — Parsian T01 / Income Statement Mapping Proof

**Status:** EVIDENCE-LIMITED DESIGN PROOF — candidate only; not owner-approved or production-ready  
**Date:** 2026-11-18  
**Scope:** Header paths, row-axis paths, and candidate fact semantics in T01 (statement of profit or loss)  
**Depends on:** DB-DES-008, DB-DES-011, DB-DES-013, DB-DES-014, DB-DES-015, `parsian_periodic_report_3.md`, and `PARSIAN_PERIODIC_REPORT_3_STRUCTURAL_REVIEW.md`

## 1. Purpose and selection

DB-DES-015 demonstrated the mapping structure on T03, a point-in-time balance-sheet table. This proof selects T01, the statement of profit or loss, to test a different case: duration/flow metrics with comparative columns, audit qualifiers, a black excluded column, and a unit note outside the table.

This is still a mapping proof, not a complete T01 mapping and not authorization to ingest values.

## 2. Evidence identity and limitations

The detailed report `database/reports/parsian_periodic_report_3.md` records workbook SHA-256:

`69186f1ad2b0e481a3588f2731b7027b0a9d9a543d1ca17fd24fc71d8c5aca06`

The corrected workbook is recorded elsewhere as:

`95f94e739632e48ae6552c562ecbf6c3e8182848718d17977f69bc984a6638b0`

The structural review explicitly says the detailed report is an earlier package and no retained-sheet XML hash proves byte identity with the corrected workbook. Therefore all literal cell values and exact text below are historical evidence requiring confirmation against the corrected XLSX. This proof does not claim direct inspection of that corrected workbook.

Only `Recovered_Sheet1` is considered. The temporary `Sheet1` described in report 3 is excluded.

## 3. Physical candidate structure

| Attribute | Candidate evidence |
|---|---|
| Table | T01 — صورت سود و زیان |
| Title | A8 |
| Candidate bounds | A10:D42 |
| Header rows | 10–11 |
| Label column | A |
| Data columns | B and D |
| Excluded column | C (black fill throughout T01) |
| Candidate green section markers | A12, A32, A35 |
| Candidate row-label ranges | A13:A31, A33:A34, A36:A42 |
| Gray extraction cells | B/D across those row ranges; 56 numeric cells, no blank gray cells |
| Cells outside candidate bounds | E10:E11 and E13:E42 include percentage-change header/data; excluded from T01 under current candidate bounds and gray-only extraction convention |

The T01 rectangle and color/role inventory are evidence-supported candidates from the structural review, not owner-approved production bounds.

## 4. Header reconstruction

The detailed report records these source labels:

| Coordinate | Literal text | Candidate level / role |
|---|---|---|
| A10:A11 | A10 = `شرح`, merged vertically through A11 | Row-label header |
| B10 | `دوره منتهي به ۱۴۰۳/۰۶/۳۱` | Period/date header for B |
| B11 | `حسابرسی نشده` | Audit-status qualifier for B |
| D10 | `تجدید ارائه شده ۱۴۰۲/۱۲/۲۹` | Restated comparative-period header for D |
| D11 | `حسابرسی شده` | Audit-status qualifier for D |
| C10:C11 | Black-filled, excluded | Not an extractable data slot |

Candidate ordered paths:

- B: [`دوره منتهي به ۱۴۰۳/۰۶/۳۱`, `حسابرسی نشده`]
- D: [`تجدید ارائه شده ۱۴۰۲/۱۲/۲۹`, `حسابرسی شده`]

The path preserves period/date wording and audit status as separate levels. B and D must not be collapsed into one generic “current/prior” label. The black C column is excluded; it must not be interpreted as a third data column merely because it contains values in the historical workbook.

The percentage-change information in column E is outside the candidate T01 rectangle and its values are uncolored. It is not a canonical financial fact under the current gray-only extraction rule. It must not be silently appended to T01.

## 5. Row-axis hierarchy and candidate semantic examples

The report records three green markers:

- A12: `عملیات در حال تداوم:`
- A32: `عملیات متوقف شده:`
- A35: `سود (زیان)پایه هر سهم (ريال)`

Candidate row paths include:

| Row | Source label | Candidate row-axis path | Candidate meaning |
|---|---|---|---|
| A22 | `جمع درآمدهاي عملياتي` | [عملیات در حال تداوم, جمع درآمدهای عملیاتی] | Total operating income (flow) |
| A31 | `سود (زيان) خالص عملیات در حال تداوم` | [عملیات در حال تداوم, سود خالص عملیات در حال تداوم] | Net profit from continuing operations (flow) |
| A34 | `سود(زیان) خالص` | [عملیات متوقف شده, سود(زیان) خالص] | Net profit/loss from discontinued operations (flow) |
| A41 | `سود (زیان) خالص هر سهم– ریال` | [سود (زیان) پایه هر سهم, سود (زیان) خالص هر سهم] | Per-share measure; exact metric definition requires metric-dictionary confirmation |

These are source-label paths and candidate concepts, not approved FinancialMetric codes. In particular, A34 is a distinct discontinued-operations row and must not be merged with A31 or treated as a duplicate of continuing-operations profit. The total net-profit row A34 and the continuing-operations row A31 need a formal accounting-semantic reconciliation before both are mapped into canonical metrics.

### 5.1 Example intersections

The historical detailed report records:

| Coordinate | Stored value | Candidate row | Candidate column |
|---|---:|---|---|
| B31 | -25,195,703 | Continuing-operations net profit | Current period, unaudited |
| D31 | -9,124,895 | Continuing-operations net profit | Restated comparative period, audited |
| B41 | -161 | Basic EPS / net profit per share | Current period, unaudited |
| D41 | -58 | Basic EPS / net profit per share | Restated comparative period, audited |

These literal values are not revalidated against the corrected workbook and are not approved for persistence.

## 6. Temporal and unit interpretation: deliberate fail-closed outcome

### 6.1 Flow versus period basis

Rows such as total operating income and net profit are duration/flow candidates, not INSTANT balances. However, the recorded T01 header provides period-ending dates but does not explicitly provide the start date or establish whether each amount is YTD or STANDALONE.

Accordingly:
- candidate temporal kind for A22/A31/A34 is DURATION;
- `duration_basis` remains UNRESOLVED;
- the exact Jalali interval remains UNRESOLVED;
- neither YTD nor STANDALONE may be inferred from the report's publication cadence, the phrase “period ending”, or a comparative year-end date;
- no standalone quarter may be manufactured from these source columns at ingestion time.

This is consistent with DB-DES-011: duration basis belongs to each FinancialFact; it is not a property of FinancialPeriod.

### 6.2 Unit and scale

The cell A9 immediately above T01 is recorded as:

`کلیه مبالغ درج شده به میلیون`

This is evidence for a “millions” scale note for amounts in the statement, but the note does not explicitly name the currency in the recorded text. Therefore:
- scale candidate: MILLION;
- currency: UNRESOLVED from this evidence alone;
- canonical monetary unit and conversion remain blocked pending explicit source/approved report-family evidence.

A41 explicitly contains `ریال` in its row label. This per-share unit must not inherit the general “millions” scale blindly. The exact EPS metric/unit rule must be explicitly approved. Do not multiply or divide EPS values by one million.

### 6.3 Audit and restatement qualifiers

B11 and D11 are source audit-status qualifiers. D10 also explicitly says “restated”. They must remain attached to source/report-version interpretation and provenance. They are not automatically financial dimensions, and the Header wording alone does not create or identify a ReportVersion. Version identity, publication date, audit status, restatement relationships, and ranking must be resolved by the ReportVersion contract.

## 7. Mapping proof result

| Component | Candidate result | Status |
|---|---|---|
| T01 geometry | A10:D42 | Provisional |
| B Header path | Period ending 1403/06/31 + unaudited | Historical evidence; confirm corrected XLSX |
| D Header path | Restated 1402/12/29 + audited | Historical evidence; confirm corrected XLSX |
| C slot | Black/excluded | Historical evidence; confirm corrected XLSX |
| E percentage-change column | Outside candidate bounds; uncolored values | Excluded under current convention |
| A31 row meaning | Continuing-operations net profit | Candidate |
| A31 temporal kind | DURATION | Strong semantic candidate |
| A31 duration basis / exact interval | Unknown | BLOCKED |
| A31 currency | Unknown | BLOCKED |
| General amount scale | Million | Candidate from A9 |
| A41 per-share unit | Rial stated in row label | Candidate; metric/unit approval required |
| Canonical metric codes | Not assigned | BLOCKED |

**Result: PARTIAL PROOF.** The example demonstrates why Header paths, row-axis paths, temporal basis, audit qualifiers, and unit/scale must be resolved separately. It does not establish canonical facts and does not close DB-ING-006 / Task 033.

## 8. Required gates before approval

1. Confirm the corrected workbook SHA-256 and re-read A8:A12, B10:B11, C10:C11, D10:D11, A22, A31, A34, A41, B31/D31, B41/D41, and A9 directly from that exact workbook.
2. Owner-approve T01 bounds and confirm the A12/A32/A35 row partitions.
3. Establish the actual Jalali period interval and whether B/D values are YTD or standalone from explicit source evidence.
4. Establish currency for monetary values and approve the scope of the million-scale note.
5. Approve the EPS metric definition and per-share unit handling independently of the general monetary scale.
6. Resolve continuing/discontinued/total net-profit relationships to avoid duplicate or inconsistent canonical facts.
7. Resolve B/D ReportVersion provenance and audit/restatement ranking independently of the Header text.
8. Validate the same Header and row-axis structure against a genuinely independent later-period Parsian workbook.

No ORM, migration, runtime code, database data, or tests were changed. No ingestion is authorized.
