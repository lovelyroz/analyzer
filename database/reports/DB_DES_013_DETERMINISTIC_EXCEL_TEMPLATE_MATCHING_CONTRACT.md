# DB-DES-013 — Deterministic Excel Template Matching Contract

Status: PROPOSED V1 CONTRACT  
Date: 2026-11-18  
Scope: Matching a later Excel report to an approved Company Table Layout Template  
Authority: Owner decisions recorded in `DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md`

## 1. Purpose and boundary

This contract defines how an incoming workbook is matched to an already approved, versioned Company Table Layout Template before any financial value is persisted.

It does not define Excel cell reading (DB-ING-005), visual annotation authoring, canonical metric/dimension mapping, fiscal-period interpretation, or the physical ORM/migration implementation. It does not approve the current Parsian candidate coordinates. It must not be used to bypass the approval and independent-period validation gates in DB-ING-006 / Task 033.

The matcher is a deterministic validator and locator, not an AI classifier. It must never choose the "closest" candidate or repair an ambiguous workbook by guessing.

## 2. Required inputs

The matching operation receives:

- resolved `company_id`;
- resolved report-family / `report_type_id`;
- a fully identified incoming ReportVersion (including its source workbook fingerprint);
- one exact APPROVED TemplateVersion applicable to that company and report family;
- read-only workbook observations from the Excel Reader;
- the approved matching rules and structural definitions belonging to that TemplateVersion.

Company identity, report family, publication status, audit/restatement priority, and financial-period identity are resolved outside the structural matcher. The matcher must not infer them from worksheet titles or numeric content.

If zero or more than one approved TemplateVersion is applicable, stop before workbook matching. Do not select the newest template merely because it is newest; template applicability must be explicit and deterministic.

## 3. Matching stages — all gates are mandatory

### Stage 0 — preconditions

1. Confirm the workbook is readable and its source fingerprint is available.
2. Confirm exactly one applicable approved TemplateVersion has been selected.
3. Confirm the TemplateVersion is internally valid: unique node codes, valid parent-child relationships, valid range containment, resolved Header inheritance, valid column slots, and no cross-node extraction-span overlap.
4. If a precondition fails, reject the report before extracting or persisting facts.

### Stage 1 — worksheet resolution

Resolve each required worksheet using only the worksheet identity rule explicitly stored in the TemplateVersion.

Permitted evidence may include exact worksheet name, ordinal, required/optional status, and an explicitly approved combination of these. The implementation must not silently fall back from a failed name match to an ordinal match, or vice versa.

- Every required worksheet must resolve to exactly one incoming worksheet.
- One incoming worksheet cannot satisfy two required worksheet definitions unless the Template explicitly allows reuse (not expected for V1).
- Missing, duplicate, or ambiguous matches reject the whole report.
- Unexpected worksheets are ignored only when the Template explicitly marks them as permitted extras; otherwise reject or route to review according to an explicit policy.

**Open evidence gate:** The Parsian sample contains one worksheet, `Recovered_Sheet1`. Its name and ordinal are sample facts, not yet a validated later-period identity rule. The exact V1 identity rule remains unselected until an independent workbook is compared.

### Stage 2 — top-level table candidate location

For each required top-level TABLE node, enumerate candidate locations only within its resolved worksheet and using approved deterministic anchors/rules.

An anchor may be an exact table-title label, an explicitly approved alias, a relative location rule, or another structural key stored in the Template. Any text normalization must be a finite, documented transformation (for example Unicode normalization, trimming, and approved whitespace normalization). Normalization must not rewrite words, translate labels, or collapse distinct labels.

- Exact label aliases must be explicitly stored and versioned; no inferred aliases.
- A candidate must satisfy all required structural constraints for that node.
- Each required table must have exactly one candidate.
- Candidate assignments must be globally one-to-one; one source region cannot satisfy multiple table nodes.
- Zero candidates, multiple candidates, or conflicting assignments reject the whole report.

A title label by itself is not sufficient evidence if the same label can occur more than once. The approved structural fingerprint and contextual constraints must also validate.

### Stage 3 — structural fingerprint validation

Validate the candidate against the Template's approved structural fingerprint. The fingerprint may include:

- ordered header text paths and their resolved levels;
- merged-cell geometry and merged-range relationships;
- number and order of columns;
- relative positions of title, header, body, and optional footer;
- approved parent/child node inventory and order;
- approved row/column shape constraints;
- stable non-value structural markers explicitly approved for matching.

The fingerprint must exclude financial values and formatting features that are not part of the runtime contract. In particular, runtime matching must not depend on annotation colors, borders, or sample-only visual styling.

No probabilistic score or similarity threshold is permitted in V1. Each required fingerprint condition is either satisfied by an explicit rule or it fails. If a future version introduces a bounded variation, that variation must be an explicit, versioned rule with positive and negative test cases.

### Stage 4 — sub-table resolution

Resolve each required SUBTABLE within its already matched parent table, using its own approved exact anchor/alias and structural constraints.

- A child must resolve to exactly one location inside its matched parent.
- Child order and parent-child containment must match the approved Template.
- A child cannot cross the parent boundary or overlap another child unless the Template explicitly defines a non-overlapping structural relationship.
- Missing, duplicate, ambiguous, unexpected, or out-of-parent child regions reject the report.

Header inheritance is resolved through the Template relationship. It is not inferred by comparing values or by copying the parent's header into the child.

### Stage 5 — coordinate mapping and drift policy

The matcher returns a deterministic mapping from every approved Template node/range/span to the corresponding incoming worksheet coordinates.

Sample A1 coordinates are provenance and the baseline. They are not permission to apply an unbounded row/column offset to a later workbook.

- Exact-coordinate matching is valid only where the approved Template explicitly requires fixed coordinates.
- Relocation is allowed only through a deterministic rule validated against independent later-period workbooks and stored in the TemplateVersion (for example, a uniquely identified title anchor plus approved relative offsets).
- No global shift, nearest-title search, fuzzy text matching, or silent coordinate repair is allowed.
- If a coordinate differs and no approved relocation rule explains it, reject the report for review.
- Every resolved source coordinate must remain within its matched node and its approved BODY/optional FOOTER range as applicable.

**Open evidence gate:** No second-period Parsian workbook has yet been validated. Therefore no general coordinate-drift tolerance or relocation rule is approved by this document.

### Stage 6 — extraction-plan validation

Before reading values for persistence, construct an immutable in-memory extraction plan and validate it as a whole:

1. Every expected required table and sub-table is present exactly once.
2. Every extraction span maps to a valid source range and resolved column slot.
3. Every positive extraction coordinate is owned by exactly one layout node.
4. No non-gray/unapproved sample coordinate is included in the generated sample plan; in later workbooks, only the Template's approved mapped spans are extracted (runtime colors are irrelevant).
5. Blank source cells at approved extraction coordinates remain present in the plan and are interpreted as numeric zero under the owner's rule.
6. Parent requests resolve parent-owned spans plus descendant-owned spans without duplicate coordinates.
7. No source coordinate is assigned to two canonical output positions unless a separately approved semantic rule explicitly permits it (none is assumed here).

Any violation rejects the entire report before persistence.

## 4. Fail-closed and atomic ingestion

The report is one structural acceptance unit.

- A missing, duplicated, ambiguous, or materially changed required worksheet/table/sub-table rejects the whole report.
- No partial table persistence is permitted.
- Structural matching and all downstream semantic/period/value validations must finish before canonical facts are committed.
- Canonical facts for one report are inserted in one database transaction. Any validation or insert failure rolls back the whole report.
- Diagnostics may be retained separately, but rejected raw workbook cell grids and derived financial outputs are not persisted under the current storage policy.

The matcher must return either:
- `MATCHED` with one complete, validated coordinate map and extraction plan; or
- `REJECTED` with one or more deterministic diagnostics.

There is no `PARTIALLY_MATCHED`, `BEST_EFFORT`, or auto-corrected success state in V1.

## 5. Diagnostics and reproducibility

Every rejection diagnostic must identify:

- company/report family and incoming ReportVersion reference;
- selected TemplateVersion ID and version;
- worksheet/node code;
- expected rule or fingerprint component;
- observed value/structure and source coordinates, where available;
- stable error code and human-readable explanation.

A successful match records the exact TemplateVersion and matching-rule version used, source workbook fingerprint, and the resolved source coordinate map/locator provenance required by the approved persistence contract. It must not store the raw workbook grid.

Given the same workbook bytes, TemplateVersion, and matcher implementation version, matching must produce the same result and coordinate map.

## 6. Explicitly prohibited behavior

V1 must not:

- use fuzzy string similarity, embeddings, an LLM, or numeric-content heuristics to select a table;
- use annotation colors or borders in later reports;
- infer missing company industry, fiscal start month, report type, period, metric, unit, or temporal meaning;
- treat a blank unannotated cell as zero;
- ignore unknown or extra in-scope structures silently;
- accept a partial workbook or persist only the tables that happened to match;
- silently pick the first, nearest, newest, or highest-scoring candidate;
- rewrite the approved TemplateVersion in place when a report differs.

## 7. Required acceptance tests before implementation approval

The matcher design is not implementation-ready until the following fixtures and tests exist:

1. Exact approved workbook matches and produces a stable coordinate map.
2. Each required worksheet missing, duplicated, or ambiguous is rejected.
3. Each required top-level table missing, duplicated, or ambiguous is rejected.
4. Repeated title text is disambiguated only by approved structural context; otherwise rejected.
5. Header text, order, merged ranges, or column count changed outside an explicit allowed rule is rejected.
6. Missing, duplicated, reordered, or out-of-parent sub-table is rejected.
7. A coordinate shift without an approved relocation rule is rejected.
8. A shift covered by an explicitly approved relocation rule maps to the correct cells.
9. Extra worksheet/table behavior follows explicit policy and is tested.
10. Cross-node extraction-span overlap and duplicate parent/child coordinates are rejected.
11. Blank approved extraction cells remain in the plan and become numeric zero.
12. One structural/semantic failure causes zero canonical facts to be committed.
13. Identical inputs produce byte-for-byte equivalent normalized match results/diagnostics.

Tests must use at least one independent later-period workbook for each report family being approved. Re-running audits on the same sample workbook does not satisfy this requirement.

## 8. Open decisions and gates — not guessed here

The following cannot be finalized from the current Parsian sample alone:

1. Worksheet identity rule for later reports (name, ordinal, or explicit combination).
2. Whether title text is stable across reporting periods; approved aliases, if any.
3. Which structural fingerprint components are stable across periods and which may vary.
4. Whether any tables move when earlier sections expand/collapse, and the deterministic relocation rule if so.
5. Exact policy for unexpected extra worksheets/tables.
6. Whether each of the 17 candidate parent bounds and 15 child partitions is approved.
7. Whether child-specific headers differ from inherited parent headers.
8. Independent-period drift validation using a second Parsian periodic workbook.

Until these gates are closed, the matcher contract is a design baseline only. Do not implement production matching, generate approved Template records, or ingest reports based on the candidate map.

## 9. Status

DB-DES-013 establishes the deterministic, fail-closed matching contract for V1. It does not close DB-ING-006 / Task 033. No ORM, migration, runtime code, database data, or tests are changed by this document.
