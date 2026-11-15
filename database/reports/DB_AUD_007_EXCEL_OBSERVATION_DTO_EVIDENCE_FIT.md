# DB-AUD-007 — Excel Observation DTO Evidence-Fit Assessment

**Date:** 2026-11-15  
**Status:** PARTIAL — assessment based exclusively on the existing Markdown audit DB-AUD-002; no workbook was opened in this task.  
**Related contract:** DB-DES-007 — `DB_DES_007_EXCEL_SOURCE_OBSERVATION_DTO_CONTRACT.md`  
**Purpose:** Validate whether the logical DTO contract can preserve the structures and ambiguities already documented for four Excel workbooks, and identify any necessary refinements before selecting a Python library or implementing an adapter.

## 1. Evidence boundary

This assessment uses the transcribed and summarized observations in `database/reports/DB-AUD-002_REAL_EXCEL_TEMPORAL_AUDIT.md`. It does not claim direct access to the XLSX files in this task. The four documented samples are:

- `cheshme.xlsx`: opening/change/closing portfolio blocks, dividend and income tables, dated and undated periods.
- `fzar.xlsx`: monthly activity with multiple grouped measures, YTD, corrections, restated YTD, monthly flow, prior-year YTD, forecast and status descriptors.
- `fzar2.xlsx`: formal statements and appended schedules on one worksheet, with duration and instant statements, comparative dates, restatements, and local dates that differ from workbook-title period context.
- `samanBank.xlsx`: many independent tables on one worksheet, repeated date pairs, balances, six-month flows, average rates, forecasts, and investee metadata.

All four samples were documented as one visible worksheet with no formulas and no Excel structured tables. They do not establish behavior for multi-sheet workbooks, formula caches, hidden sheets, external links, macros, or other Excel features. Those remain implementation test requirements, not observed evidence.

## 2. Evidence-to-DTO fit matrix

| Evidence pattern in DB-AUD-002 | Required DTO capability | DB-DES-007 fit | Assessment / refinement |
|---|---|---|---|
| One worksheet contains many independent tables (`samanBank`, `fzar2`, `cheshme`) | Multiple TableObservation instances per worksheet, each with its own local context | Supported | Table detection must not assume one statement per sheet. |
| Merged and multi-level headers (`cheshme`, `fzar`, `samanBank`) | Preserve individual header fragments, merge anchor/inheritance and axis hierarchy | Supported | Do not irreversibly flatten paths; retain source cell refs transiently. |
| Side-by-side grouped measures and periods (`fzar`, `samanBank`) | Column hierarchy with separate group and leaf observations | Supported, needs explicit axis grouping | A leaf column may inherit a group label but also carry its own measure label. |
| Adjustment block next to restated value block (`fzar`) | Distinguish presentation role from period identity | Supported in interpretation stage | “اصلاحات” is not a period; it may be a delta/adjustment block, and its economic role requires approved mapping. |
| Current YTD, one month, current YTD, prior-year YTD in one table (`fzar`) | Per-value temporal descriptor and distinct candidate groups | Supported | A single table-level period is insufficient. |
| Forecast estimate beside actual balance/flow (`fzar`, `samanBank`) | Separate unresolved presentation status from temporal shape | Supported | Forecast must not be inferred from future date alone; source wording/context must be preserved. |
| Point-in-time balance dates (`fzar2`, `samanBank`) | Candidate temporal phrase plus INSTANT interpretation | Supported | “به تاریخ” / “در تاریخ” are evidence; exact date parsing and semantic resolution remain separate. |
| Flow period with explicit end date but missing start date (`fzar2`) | Preserve partial temporal evidence and unresolved fields | Supported | Never fabricate a start date from title, fiscal convention or publication date without approved company-calendar evidence. |
| Workbook title period conflicts with appended local table date (`fzar2`) | Local table context and workbook metadata kept separate | Supported | Workbook metadata must not override table-local labels. |
| Comparative columns with different end dates and uncertain durations (`fzar2`) | Each candidate has its own period descriptor and resolution status | Supported | Do not assume comparatives are same-duration or same fiscal quarter. |
| Repeated date pairs under category groups (`samanBank`) | Header group identity preserved for each column | Supported | Date alone does not identify the measured category or metric. |
| Period date mixed with average-rate measure columns (`samanBank`) | Separate measure-axis and temporal-axis fragments | Needs explicit refinement | DTO should preserve orthogonal header dimensions, not treat every column fragment as a single linear “header path”. |
| Investee fiscal-year date embedded in a row (`samanBank`, `cheshme`) | Distinguish row-level entity attributes from column temporal descriptors | Needs explicit refinement | Dates in row values/labels are not automatically FinancialPeriod descriptors. |
| Opening/change/closing blocks without explicit dates (`cheshme`) | Preserve temporal role words with unresolved calendar dates | Supported | “ابتدای دوره” / “انتهای دوره” alone cannot establish exact dates. |
| Narrative section title describes period while table header does not (`samanBank`) | Capture nearby caption/context separately from column header | Supported | Context may inform mapping but must not silently resolve ambiguity unless an approved rule explicitly permits it. |
| Date-only header where section label suggests flow but header itself is ambiguous (`samanBank`) | Preserve both local table context and unresolved temporal status | Supported | If no approved standard resolves it, reject the candidate/report rather than assume instant or duration. |
| Non-period descriptor such as product status/unit or percentage change | Keep non-period columns as distinct structural/measure observations | Supported | Not every numeric/text column is a financial period or FinancialFact candidate. |

## 3. Required refinements to the logical DTO contract

The following refinements are required before implementation. They clarify structure; they do not introduce semantic inference.

### 3.1 Orthogonal header axes

A single concatenated `HeaderPathObservation` is not sufficient as the only representation for complex grouped tables. Preserve, independently:

- **group hierarchy:** merged or unmerged parent headers that group multiple leaf columns;
- **measure hierarchy:** labels such as quantity, rate, amount, percentage change, balance, and count;
- **temporal hierarchy:** dates, date ranges, fiscal-year labels, cumulative/standalone phrases, and comparative qualifiers;
- **presentation qualifiers:** correction, restatement, estimate, forecast, actual, and other literal source qualifiers;
- **row/column role evidence:** row labels, category group, units, and status descriptors.

A cell may inherit several orthogonal header fragments. The adapter preserves these fragments and their structural relationships; the interpretation layer decides whether they form a valid semantic mapping.

### 3.2 Candidate context must include both row and column axes

A value candidate must retain:

- all applicable row-axis header/label fragments;
- all applicable column-axis group/measure/temporal/presentation fragments;
- table title/caption and nearby section context;
- the exact transient source cells/ranges for those fragments.

This is necessary because a date may be a column period, a row-level investee fiscal-year attribute, a footnote date, or a forecast date. The adapter cannot classify the date's economic role from its format alone.

### 3.3 Temporal descriptor is evidence, not a resolved period

Represent a temporal descriptor as a collection of literal fragments and optional parser observations, not as an already accepted `FinancialPeriod`.

It must support:

- exact Jalali date;
- date range, if explicitly stated;
- explicit duration phrase (one month, six months, year-to-date, etc.);
- cumulative/YTD phrase;
- opening/change/closing role without dates;
- comparative/restated qualifier;
- forecast horizon;
- partial or contradictory evidence;
- explicit unresolved reason.

The parser may extract a date token or recognize a phrase, but only the versioned temporal interpretation stage may assign INSTANT/DURATION, start/end dates, fiscal year/quarter, months_length and is_ytd.

### 3.4 Presentation status is independent of time and value kind

Actual, Forecast, Plan, correction, restatement, and comparative status are not interchangeable with period shape or metric value kind. Preserve the literal source qualifiers independently. A future date does not by itself mean Forecast; “restated” does not by itself mean a new economic period; “correction” may describe an adjustment block rather than a new period.

### 3.5 Table segmentation may remain unresolved

Where table boundaries, parent headers, or merged-cell inheritance cannot be determined reliably, the DTO must preserve an ambiguous structural candidate and diagnostics. It must not force a guessed table boundary merely to produce a complete object graph. If an ambiguous region contains an in-scope candidate and cannot be resolved by the approved standard, reject the whole ingestion unit.

## 4. DTO acceptance scenarios derived from evidence

These scenarios are logical acceptance cases for future adapter/interpretation tests. They are not tests executed in this task.

| Scenario | Evidence source | Expected observation behavior | Expected interpretation/admission behavior |
|---|---|---|---|
| Multiple independent tables on one worksheet | All four samples | Emit distinct table candidates and local context | Resolve each table independently; no workbook-wide default period |
| Multi-level merged headers | `cheshme`, `fzar`, `samanBank` | Preserve parent and leaf fragments plus merge inheritance | Map only with exact approved structural rules |
| Mixed temporal groups in one table | `fzar` A10:Z31 | Preserve YTD, correction, restated YTD, one-month, current YTD and prior YTD groups separately | Assign period per candidate; correction block not automatically a period |
| Measure/period interleaving | `samanBank` A85:F105 | Preserve measure and temporal fragments as orthogonal axes | Do not parse rate column as a date-bearing amount candidate |
| Snapshot versus flow | `fzar2` income statement and balance sheet | Preserve literal “دوره منتهی” vs “به تاریخ” evidence | Duration and instant periods resolved distinctly |
| Missing start date | `fzar2` B9/C9 | Preserve end date and report-level six-month clue separately | Resolve only if approved company/report context supplies validated start; otherwise reject unresolved candidate |
| Conflicting workbook title and local table date | `fzar2` cash-flow block | Preserve both metadata sources independently | No workbook title override; local period ambiguity is explicit |
| Forecast beside actual | `samanBank` A70:D81 and `fzar` energy block | Preserve future/forecast literal qualifiers separately from date | Forecast remains distinct from Actual and requires approved mapping |
| Undated opening/change/closing roll-forward | `cheshme` A9:O32, A160:K182 | Preserve opening/change/closing labels with absent dates | Do not invent period endpoints; reject if in-scope fact requires unresolved period |
| Row-level date attribute | `samanBank` investee table | Preserve row cell and row-axis relation | Do not treat investee fiscal-year date as column FinancialPeriod |

## 5. Consequences for implementation design

1. The eventual Python DTO should model **header fragments and relationships**, not just a string header per column.
2. It should model temporal, measure and presentation evidence as separate collections/axes.
3. Table detection must support multiple disjoint regions within a single worksheet.
4. Candidate construction should be a later deterministic transformation over observations; it should not be conflated with low-level workbook reading.
5. Excel library selection must be tested against merged-cell semantics, hidden sheet/row/column metadata, cached formula values, date systems, sparse cells and read-only large-file behavior.
6. No algorithm may infer fiscal-year start, standalone-quarter status, stock/flow, actual/forecast, or issuer identity from filename, position, arithmetic coincidence, or workbook title alone.
7. The current four documented workbooks do not provide evidence for multi-sheet reports, formulas, hidden content, macros, or structured Excel tables. These remain explicit test fixtures/coverage gaps, not assumed capabilities.

## 6. Decision and remaining work

**Decision:** DB-DES-007 is structurally capable of representing the four documented workbook patterns, but it needs the orthogonal header-axis refinement in Section 3 before a Python DTO implementation is frozen.

**No implementation approval:** This assessment does not authorize choosing a library, writing an adapter, changing ORM/schema/migrations, or persisting observations.

**Open work:**

- validate the evidence transcription against the actual source workbooks when an authorized XLSX inspection workflow is available;
- choose a Python library based on a feature spike covering merged cells, formula caches, date systems, hidden content and large worksheets;
- draft concrete Python DTO class/interface definitions only after the feature spike;
- implement adapter and candidate builder as separate layers;
- create representative fixtures for observed and currently unobserved Excel features;
- execute user-owned tests and record results before marking DB-DES-007 complete.

**Scope statement:** This report relies only on existing Markdown audit evidence. No XLSX file was opened or inspected in this task. No code, tests, ORM, schema, migration, or database data were changed. Tests were not run.
