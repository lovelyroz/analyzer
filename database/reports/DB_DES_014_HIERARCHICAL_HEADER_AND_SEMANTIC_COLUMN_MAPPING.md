# DB-DES-014 — Hierarchical Excel Header and Semantic Column Mapping Contract

**Status:** DESIGN PROPOSAL — no ORM, migration, runtime code, database data, or tests changed  
**Date:** 2026-11-18  
**Scope:** Resolve multi-level Excel headers and map physical row/column coordinates to canonical FinancialFacts  
**Depends on:** DB-DES-008, DB-DES-009, DB-DES-010, DB-DES-011, DB-DES-013, DB-ING-005, DB-ING-006, and the owner decisions in the Database Configuration Master Working Packet

## 1. Purpose and boundary

This contract defines how a later-period Excel workbook is interpreted after its worksheet, table/sub-table, and extraction coordinates have been resolved by the deterministic matcher.

It separates three independent concerns:

1. **Physical layout:** where a header, row label, column slot, and extractable value are located.
2. **Header interpretation:** the complete ordered meaning of a multi-level column header, including merged-cell propagation and contextual qualifiers.
3. **Semantic mapping:** which canonical FinancialMetric, dimensions, temporal interpretation, unit, and value semantics are represented by a particular row/column intersection.

A physical column slot is not a FinancialMetric. A row label is not necessarily a complete metric identity. A source header string alone is not necessarily unique. The semantic identity of a fact may require the resolved table node, full column-header path, row-label path, and approved report-family rules together.

This proposal extends DB-DES-008's explicit separation between layout and semantic mapping. It does not replace DB-DES-008, DB-DES-009, or DB-DES-011.

## 2. Core model

### 2.1 Header definition

A Header definition is an ordered, versioned description of the column-axis structure for one layout node. It contains:

- ordered header levels, from outer/group level to most specific leaf level;
- the exact source range and source coordinates for each level;
- merged-cell geometry and deterministic propagation rules;
- the resolved ordered header path for each physical column slot;
- approved normalized labels and explicit aliases, where needed;
- any explicitly established unit, currency, scale, basis, temporal, scenario, or presentation qualifier.

Do not flatten the entire Header into one unstructured text string. Preserve its level boundaries and ancestry. A repeated leaf label under two different parent groups is two different header paths.

### 2.2 Header level and path

Each header cell observation belongs to a specific level and source coordinate. The resolved path for a column is an ordered sequence, for example:

`[Group label, Measure label, Temporal label, Unit label]`

The example is illustrative only; actual levels are determined from the approved workbook template. A level may be absent when the source structure genuinely has no such level. Do not invent placeholder labels.

A path is scoped to its Header definition and TemplateVersion. Its identity is not just the concatenated display text.

### 2.3 Column slot

A ColumnSlot remains a physical positional slot owned by an OWN Header definition, as proposed in DB-DES-008. It identifies the source column position and its resolved Header path. A child node using Header inheritance resolves the parent's slots by reference; it does not create duplicate slots.

Column slots may be classified as DATA, LABEL, CONTEXT, or another controlled role. Only approved DATA slots can participate in fact extraction. LABEL and CONTEXT slots provide interpretation context and are not themselves persisted as FinancialFacts.

### 2.4 Row-axis definition

Row labels require a parallel hierarchical interpretation. A row-axis path can include parent headings, section labels, subcategory labels, and a leaf label. The path must preserve order and ancestry, just as the column Header path does.

A row-label path is not automatically a canonical metric. It becomes a semantic mapping input only after the applicable row-axis structure has been deterministically resolved and approved.

### 2.5 Semantic mapping rule

A SemanticMappingRule is a separately versioned, approved rule that binds a complete source context to canonical fact meaning.

Its logical match key may include:

- report type and approved industry/report-family interpretation scope;
- TemplateVersion and layout node (TABLE or SUBTABLE);
- resolved Header definition and exact ordered Header path;
- ColumnSlot identity or an explicitly defined slot group;
- resolved row-axis path / row-label identity;
- approved contextual qualifiers that alter meaning.

Its output declares the canonical interpretation:

- FinancialMetric;
- zero or more approved Dimension values / dimension-set identity;
- temporal kind: INSTANT or DURATION;
- duration basis: STANDALONE or YTD for applicable DURATION facts; not applicable for INSTANT;
- canonical unit, currency, scale, and measurement basis;
- value semantics and source value-state policy;
- any explicit scenario/actual-forecast distinction;
- interpretation rule/version provenance.

The semantic mapping is not embedded in the physical ColumnSlot record. A separate mapping layer allows the same physical layout to be revised without changing metric identity and allows the same metric to appear at different coordinates in different templates.

## 3. Header reconstruction rules

### 3.1 Merged cells

For a merged header cell, the top-left anchor is the source value. Its coverage across the merged range is represented as a structural relationship, not by copying the text into persisted raw-cell records.

When resolving a particular column's Header path, a merged parent label applies to the columns covered by that merge only. It must not propagate beyond the merged range. A non-merged blank cell is not automatically a continuation of the preceding label.

### 3.2 Blank header cells

A blank header position is handled only by an explicit approved structural rule, such as:
- a merged range whose anchor supplies the parent label; or
- an explicitly approved blank level that is semantically non-applicable.

Do not forward-fill arbitrary blanks, borrow a neighboring label, or infer a label from data values. If a required level cannot be resolved uniquely, reject the affected report.

### 3.3 Duplicate labels

Duplicate leaf labels are allowed only when their full ordered paths are distinct and each path has an unambiguous approved semantic mapping.

If two columns have the same complete Header path and the same row context but represent distinct values with no approved differentiating qualifier, the mapping is ambiguous and the report must be rejected. Column position alone is not a semantic disambiguator unless the approved template explicitly defines a positional distinction that remains structurally validated.

### 3.4 Text normalization

Matching uses exact text after a finite, deterministic normalization policy. The policy may normalize presentation-only differences such as:
- Unicode normalization;
- Persian/Arabic character variants explicitly listed in the policy;
- approved whitespace normalization;
- approved punctuation/formatting normalization;
- digit glyph normalization only where digits are not semantically meaningful text.

Normalization must not remove words, merge distinct terms, reorder tokens, translate labels, or infer synonyms.

Semantic aliases are explicit, versioned entries requiring approval. An alias is not a fuzzy match. An unrecognized in-scope label is rejected pending review.

The exact normalization profile and alias catalog are implementation gates; they must be specified and tested before production mapping is enabled.

## 4. Header inheritance across sub-tables

DB-DES-008's OWN / INHERIT binding remains authoritative.

A child may use INHERIT only when the complete resolved column meaning is unchanged, including:
- number and order of columns;
- full Header paths and their level structure;
- unit, currency, scale, and measurement basis;
- temporal interpretation and comparative-period meaning;
- scenario/actual-forecast meaning;
- physical slot roles.

A visual resemblance or matching leaf labels is insufficient.

If any of these meanings differs, the child must use OWN and define a complete local Header and slot set. V1 does not support silent per-column overrides or mixed parent/child partial inheritance.

Header inheritance does not transfer extraction-span ownership. Every extractable coordinate still belongs to exactly one layout node under DB-DES-008 §9.

## 5. Semantic mapping uses both axes

A mapping is resolved at the row/column intersection, not from a column in isolation.

For example, the same column Header path such as `[Current period, Amount]` could contain:
- revenue on one row;
- operating expenses on another row;
- cash balance in a different table.

The Header path may describe temporal or measurement context while the row path identifies the financial concept. Conversely, a row label may identify a product or deposit category while the Header path identifies amount, rate, or period.

Therefore the mapping key must include every axis/context element required to establish meaning. It must not assume that:
- one column equals one metric;
- one row label equals one metric across every table;
- the same visible label has the same meaning in every table;
- the same metric always occupies the same Excel coordinate.

A row/column intersection must resolve to exactly one approved semantic mapping rule. Zero matches or multiple matches are rejection conditions.

## 6. Temporal interpretation

Temporal meaning is part of the semantic mapping output and must comply with DB-DES-011.

### 6.1 Period interval versus value basis

- FinancialPeriod records the actual Jalali interval or instant.
- A duration FinancialFact carries its own `duration_basis`: YTD or STANDALONE.
- INSTANT facts have no duration basis.
- The report publication date, table position, fiscal-quarter label, or a generic word such as "quarterly" does not independently establish YTD/standalone.

### 6.2 Header-driven interpretation

An explicit Header level such as a named comparative period or a clearly stated cumulative interval may establish temporal meaning only after that Header pattern is approved for the applicable report family and template.

The mapping must resolve both:
- the actual Jalali period boundaries; and
- the value basis for the metric.

If the Header identifies a period end but does not establish whether the amount is cumulative or standalone, the mapping is incomplete. Do not infer the basis from the fact that the report is a three-month, six-month, nine-month, or annual publication.

### 6.3 Comparative columns

A table may contain several temporal columns, such as current period, prior comparable period, current fiscal-year cumulative, or prior fiscal-year cumulative. Each column path must be mapped independently to its actual interval and temporal basis.

A label like "previous year" is not enough to create a period without an approved deterministic rule that establishes the exact Jalali dates. Missing or conflicting period boundaries reject the report.

A source-reported standalone amount is stored as STANDALONE. A source-reported cumulative amount is stored as YTD. A standalone quarter calculated by subtracting YTD amounts remains runtime-derived and is not persisted as a source FinancialFact.

## 7. Units, scale, and value semantics

The mapping must explicitly resolve the unit and basis required to interpret a numeric cell. Possible attributes include:
- currency (for monetary values);
- unit of quantity;
- scale (ones, thousands, millions, etc.);
- rate/percentage basis;
- per-unit or per-share denominator;
- stock versus flow semantics;
- actual, forecast, budget, or other scenario when present and approved.

No scale or unit is inferred from magnitude, neighboring values, number formatting alone, or industry convention. Number formats may be supporting structural evidence only when the relevant interpretation is explicitly approved.

A unit or scale change across columns must be represented in the full Header path or an explicit approved mapping rule. If the source does not establish the unit/scale unambiguously, reject rather than store a guessed canonical value.

The numeric persistence boundary remains governed by DB-DES-009 and the owner-approved SQLite INTEGER / Decimal / ROUND_HALF_UP policy. Header mapping does not authorize binary-float arithmetic or additional rounding.

## 8. Versioning and approval

Semantic mapping is immutable after approval. A change to any of the following requires a new mapping version:
- canonical metric or dimension target;
- Header path or approved alias meaning;
- row-axis meaning;
- unit, currency, scale, or measurement basis;
- temporal interpretation;
- scenario or value semantics;
- matching scope or rule precedence.

Each ReportVersion accepted by the new Excel pipeline must reference exactly one approved interpretation-standard version, consistent with DB-DES-009. That interpretation standard must resolve to the applicable semantic mapping version(s) for the report family and TemplateVersion. The exact packaging of those version references is a physical-schema decision for a later design/implementation task; do not create unversioned mutable mappings.

No new semantic mapping becomes active merely because it was observed in a workbook. Unknown or ambiguous in-scope mappings remain pending approval and block ingestion of the entire report.

## 9. Mapping resolution and acceptance algorithm

For each extractable coordinate after DB-DES-013 has produced a complete coordinate map:

1. Resolve its unique owning layout node and ColumnSlot (including valid Header inheritance).
2. Resolve the full ordered Header path for that slot.
3. Resolve the full row-axis path and required contextual labels for the coordinate.
4. Apply only the normalization profile and aliases in the selected approved interpretation version.
5. Find the exact applicable SemanticMappingRule using its complete scope and axis/context key.
6. Validate that exactly one rule matches.
7. Validate the rule's metric, dimensions, temporal kind/basis, period boundaries, unit/scale, scenario, and value-state policy.
8. Construct the canonical fact candidate and provenance references in memory.
9. Validate cross-fact consistency and duplicate identity across the entire report.
10. Admit all canonical facts atomically only after every required in-scope mapping and validation succeeds.

Reject the entire report if:
- any required Header path or row-axis path is unresolved;
- a required in-scope label is unknown or ambiguously normalized;
- no semantic mapping or more than one semantic mapping matches;
- a mapping produces an invalid metric/dimension combination;
- temporal kind, duration basis, or actual Jalali dates are unknown/conflicting;
- unit, currency, scale, or measurement basis is unresolved;
- two source coordinates map to the same canonical fact identity with conflicting values and no approved duplicate/reconciliation rule;
- a required in-scope observation is omitted from the mapping plan.

No partial ingestion, fallback to a nearby mapping, fuzzy matching, or generic OTHER mapping is permitted.

## 10. Scope and non-goals

This is a reusable mapping architecture, not a claim that every industry or report family already has a populated semantic dictionary.

The owner-approved decision to standardize periodic-report Headers using the existing Header dictionary is specifically scoped to banks at this stage. This document does not silently extend that bank-specific policy to other industries. Other industry/report-family mappings must be established under their own approved scope and evidence.

This contract does not:
- assign actual Parsian Header paths or metric mappings;
- approve the 17 Parsian parent bounds or 15 child partitions;
- approve the provisional Header inheritance of all Parsian sub-tables;
- create a complete metric taxonomy for every industry;
- authorize storing raw workbook cells, grids, or derived values;
- define the final SQLAlchemy tables, ORM classes, migrations, or runtime API;
- authorize code, tests, database writes, or production ingestion.

## 11. Evidence required before production mapping

For each company/report-family template:
1. An owner-approved Header range and level inventory.
2. A deterministic merged-cell and blank-header interpretation map.
3. A complete row-axis hierarchy for every in-scope extraction region.
4. Explicit OWN/INHERIT approval for each table/sub-table.
5. An approved mapping inventory covering every in-scope row/column intersection.
6. Explicit temporal, unit, scale, dimension, and value semantics for every mapping.
7. An independent later-period workbook proving Header and row-axis stability or a controlled, explicitly approved template/mapping revision.
8. Negative tests for duplicate paths, unknown labels, ambiguous aliases, missing levels, conflicting units, and YTD/standalone confusion.

For Parsian specifically, the current annotation map and structural reports are candidate evidence only. They do not provide sufficient owner-approved semantic Header paths or a second independent-period workbook. No actual Parsian semantic mapping should be populated from assumptions.

## 12. Status and next gates

DB-DES-014 is a design proposal only. It closes the logical separation between hierarchical Header resolution and semantic mapping at the contract level, but it does not close DB-ING-006 / Task 033.

Next work should be evidence-driven:
1. complete and approve the Header-level and row-axis inventory for one selected template;
2. use an independent workbook from a later period to validate structural and semantic stability;
3. produce a small, explicit mapping inventory for one table as a proof of the contract;
4. only after those gates, design the physical mapping tables and implementation sequence.

No ORM, migration, runtime code, database data, or tests were changed by this document.
