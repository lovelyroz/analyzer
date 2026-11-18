# DB-DES-008 — Company Table Layout Template Relational Schema Proposal

**Status:** PROPOSED — architecture decision draft; no ORM, migration, or runtime implementation authorized  
**Date:** 2026-11-18  
**Scope:** Physical relational design for versioned company/report-type Excel layout templates  
**Authority:** `12_Database_Architecture_V1.1.md` (current content: Database Contract V1.3), owner decisions in `DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md`, and `COMPANY_TABLE_LAYOUT_TEMPLATE_SPEC.md`

## 1. Design objective

The database is not a place to browse or reconstruct Excel workbooks. Template metadata exists to make extraction deterministic and to support efficient application requests by stable identifiers. Excel coordinates are source locators, not the identity of financial information.

The design must:
- identify a template by company and report type, with immutable approved versions;
- identify worksheet, parent table, and nested sub-table structures deterministically;
- represent one or more ordered Header ranges and optional Footer ranges;
- support Header inheritance by reference without copying parent definitions;
- preserve Body structure separately from permission to extract;
- represent positive extraction targets precisely, including blank-gray-to-zero behavior;
- separate physical Excel layout from semantic financial Metric/Dimension mapping;
- preserve exact sample-workbook provenance and permit later coordinate/layout revisions without rewriting historical facts;
- reject ambiguous, conflicting, or incomplete definitions rather than infer them.

No raw workbook grid, raw cell values, duplicated header text, or calculated financial outputs are persisted by this Template model.

## 2. Recommended relational entities

Use a small normalized set of tables. Names below are logical physical-table proposals; final SQLAlchemy naming conventions can be aligned during implementation without changing the contract.

### 2.1 `company_table_template`

One logical template identity per company and report type.

| Column | Purpose / constraint |
|---|---|
| `template_id` | Stable PK |
| `company_id` | FK to companies; NOT NULL |
| `report_type_id` | FK to report-type catalog; NOT NULL |
| `created_at` | Template identity creation timestamp |
| `active_version_id` | Optional FK to the currently approved version, added only if circular-FK handling is clean; otherwise resolve approved version by status/version |

Unique: `(company_id, report_type_id)`.

### 2.2 `company_table_template_version`

Immutable revision of the layout contract.

| Column | Purpose / constraint |
|---|---|
| `template_version_id` | Stable PK |
| `template_id` | FK to logical template; NOT NULL |
| `version_number` | Positive integer, unique within template |
| `status` | DRAFT, APPROVED, RETIRED |
| `source_workbook_sha256` | Exact representative workbook fingerprint |
| `source_file_name` | Provenance label only; not identity |
| `template_schema_version` | Version of this metadata schema |
| `created_at`, `approved_at` | Lifecycle timestamps; approved_at required for APPROVED |
| `supersedes_version_id` | Optional self-FK to prior version |

Unique: `(template_id, version_number)`. At most one APPROVED version per logical template. Approved versions are immutable; a layout change creates a new DRAFT version and then approval. Historical ReportVersion records must reference the exact template version used.

Do not use a mutable boolean such as `is_current` as the sole lifecycle control. Do not overwrite an approved version in place.

### 2.3 `template_worksheet`

One record per worksheet represented in a template version.

| Column | Purpose / constraint |
|---|---|
| `worksheet_id` | Stable PK within the template version |
| `template_version_id` | FK; NOT NULL |
| `sample_ordinal` | One-based worksheet position in the sample |
| `sample_name` | Literal sample name |
| `identity_strategy` | Explicit deterministic matching strategy; initially unresolved |
| `is_required` | Whether a later workbook must contain a matching worksheet |

Unique: `(template_version_id, sample_ordinal)`; also unique sample name within version where names are required to be unique. Ordinal/name are sample evidence, not silently assumed stable runtime identifiers. Runtime matching policy remains a separate gate.

### 2.4 `template_layout_node`

A unified parent/child structure for top-level tables and sub-tables. This avoids separate table and sub-table schemas with duplicated columns.

| Column | Purpose / constraint |
|---|---|
| `node_id` | Stable PK |
| `worksheet_id` | FK; NOT NULL |
| `parent_node_id` | Nullable self-FK; NULL for top-level table |
| `node_kind` | TABLE or SUBTABLE |
| `node_code` | Stable code within this template version, e.g. T03 / T03-S01 |
| `display_name` | Approved structural label; not a canonical metric |
| `order_index` | Reading/order sequence |
| `min_row`, `max_row`, `min_column`, `max_column` | Exact sample bounds |
| `title_cell_coordinate` | Optional source locator for red/green title marker |
| `structural_fingerprint` | Optional deterministic fingerprint for matching; algorithm/version must be specified |

Constraints:
- TABLE has no parent; SUBTABLE has exactly one TABLE parent on the same worksheet and template version.
- No nested SUBTABLE under SUBTABLE in V1 unless a real workbook requires it and a separate decision expands the contract.
- Bounds must be positive and ordered; child bounds must lie inside parent bounds.
- `node_code` and `order_index` are unique within their worksheet/version scope.
- A sub-table's bounds and identity are independent records; parent definitions are referenced, not copied.

A unified node table gives runtime requests one stable path for both table and sub-table identifiers while retaining the explicit parent-child relationship.

### 2.5 `template_node_range`

Stores structural ranges for a layout node. Multiple ranges are allowed; a Header is not forced into one contiguous rectangle.

| Column | Purpose / constraint |
|---|---|
| `range_id` | PK |
| `node_id` | FK; NOT NULL |
| `range_role` | HEADER, BODY, FOOTER |
| `range_order` | Ordered range/level |
| `header_level` | Nullable; explicit level for HEADER ranges |
| `min_row`, `max_row`, `min_column`, `max_column` | Exact range bounds |
| `source_a1_range` | Human/debug locator, derived from numeric bounds or validated against them |

Unique: `(node_id, range_role, range_order)`. HEADER may contain multiple ordered ranges/levels. BODY may contain multiple disjoint ranges if later evidence requires it. FOOTER is optional and has no row by default. Do not infer FOOTER from final-row position.

For the first implementation, ranges are structural locators only. They do not grant extraction permission.

### 2.6 `template_header_binding`

One explicit Header resolution per layout node.

| Column | Purpose / constraint |
|---|---|
| `node_id` | PK and FK to layout node |
| `binding_mode` | OWN or INHERIT |
| `source_node_id` | Nullable FK to layout node; required for INHERIT, NULL for OWN |
| `definition_version` | Optional local revision marker if needed |

Rules:
- OWN means the node's Header ranges and column definitions are defined locally.
- INHERIT means the node resolves the Header/column definition from its parent node by reference.
- In V1, INHERIT may reference only the direct parent; no arbitrary cross-tree reference.
- An INHERIT node must not also define local HEADER ranges or duplicate column definitions.
- An OWN node must have at least one HEADER range and a complete local column definition.
- Cycles, missing parent bindings, conflicting inherited/own definitions, and partial silent overrides are hard validation failures.
- If a child differs semantically, switch the whole child binding to OWN in V1. Per-column partial override is deferred until a real requirement proves it necessary; this keeps resolution deterministic.

Header inheritance is based on unchanged column meaning, order, unit/basis, and temporal interpretation—not merely similar visible labels.

### 2.7 `template_column_slot`

Defines ordered physical column positions under an OWN Header definition. It describes layout slots, not financial values.

| Column | Purpose / constraint |
|---|---|
| `column_slot_id` | PK |
| `node_id` | FK to the node owning the Header definition |
| `slot_code` | Stable code within node, e.g. COL-01 |
| `ordinal` | Logical column order |
| `source_column_index` | Sample worksheet column index |
| `column_role` | DATA, LABEL, CONTEXT, or another explicitly controlled role |
| `header_path_key` | Optional stable key for the resolved multi-level header path; not copied display text |

Unique: `(node_id, slot_code)`, `(node_id, ordinal)`, and `(node_id, source_column_index)` unless an explicitly approved merged/multi-column structure requires a different representation. A child using INHERIT resolves the parent's slots by reference. Do not duplicate the parent's slots.

Canonical FinancialMetric/Dimension mapping is deliberately not stored in this table. A physical column slot is not itself a metric.

### 2.8 `template_extraction_span`

Compact, exact representation of positive extraction targets. Store vertical runs per source column rather than one row per raw cell or a broad rectangle that would accidentally include unannotated cells.

| Column | Purpose / constraint |
|---|---|
| `span_id` | PK |
| `node_id` | FK to owning table/sub-table |
| `source_column_index` | Sample worksheet column |
| `start_row`, `end_row` | Inclusive row interval |
| `value_state_policy` | V1 fixed policy: BLANK_GRAY_AS_ZERO |
| `span_order` | Stable ordering |

Unique: `(node_id, source_column_index, start_row, end_row)`. Spans must be non-overlapping within a node/column and lie inside that node's BODY ranges. Every span must map to a defined column slot (inherited or owned). If isolated cells exist, represent them as a one-row span. Do not expand spans across black or uncolored gaps. The approved annotation audit is the source for these positive targets; runtime matching later maps the template spans to the corresponding structure in a new workbook.

The template stores the positive extraction mask, not the original cell contents or a full copy of all gray/black/uncolored formatting. Blank gray means numeric zero; it is not NULL and not skipped. Black and uncolored cells are not represented as positive spans.

### 2.9 Semantic mapping boundary (separate contract)

Do not add `financial_metric_id`, canonical units, period IDs, or row-label-to-metric assumptions directly to the layout node or column-slot tables at this stage.

A later, versioned semantic mapping layer must connect:
- a resolved table/sub-table and column slot;
- approved row-axis/label definitions and any dimensions;
- source header identity/path;
- canonical FinancialMetric and approved Dimension values;
- temporal meaning (INSTANT/DURATION, YTD/standalone, comparative period);
- unit/basis and value semantics.

This separation is necessary because the same physical layout slot can change meaning between template versions, and the same semantic metric can appear at different coordinates in different templates. The mapping layer must be separately versioned and immutable after approval. Unknown in-scope labels/headers must reject the report; no fuzzy fallback or generic OTHER is introduced by this proposal.

## 3. Runtime request path

The intended request path is:

1. Resolve `company_id` and `report_type_id`.
2. Resolve the exact approved `template_version_id` applicable to the ReportVersion; historical facts retain the version used.
3. Resolve the requested `node_id` (top-level table or sub-table) by stable `node_code`.
4. Resolve Header binding: OWN uses local Header/column slots; INHERIT follows the direct parent reference.
5. Resolve canonical semantic mapping version and requested metric/dimension/period.
6. Use approved extraction spans and the deterministic workbook matcher to locate source observations.
7. Return canonical input facts through the existing financial data contract; do not query the workbook by display title or reconstruct an Excel grid.

The application-facing request should be conceptually expressible as:
`company_id + report_type_id + table_node_code + metric_id + financial_period + dimensions`.
The exact service/API signature is outside this schema proposal.

## 4. Parsian application to the current draft

- One template identity for Parsian + PERIODIC_FINANCIAL; one version for the standardized sample once approved.
- One worksheet record for `Recovered_Sheet1`; the deleted temporary `Sheet1` is excluded.
- 17 parent TABLE nodes and 15 SUBTABLE child nodes, using the candidate bounds in `PARSIAN_PERIODIC_ANNOTATION_MAP_DRAFT.md`.
- All 15 current child nodes provisionally use `INHERIT` to the direct parent's Header definition. A child changes to OWN only if its column meaning, order, unit/basis, or temporal interpretation differs.
- Header/Body ranges follow the provisional section 12 map. No Footer rows are created because no Footer is evidenced.
- Positive extraction spans are generated only from validated gray-cell coordinates, compressed into contiguous vertical runs per column. Do not infer targets from Body membership or include black/uncolored cells.
- These 17+15 nodes and their coordinates remain candidate data, not approved production template records. Owner spot-check is not blanket approval.

## 5. Integrity and query-performance rules

- Use integer surrogate primary keys for SQLite joins; keep stable human-readable node codes unique within a template version for request readability.
- Add indexes on `company_table_template(company_id, report_type_id)`, `company_table_template_version(template_id, status, version_number)`, `template_worksheet(template_version_id)`, `template_layout_node(worksheet_id, parent_node_id, node_kind, order_index)`, `template_node_range(node_id, range_role, range_order)`, `template_column_slot(node_id, ordinal)`, and `template_extraction_span(node_id, source_column_index, start_row)`.
- Enforce foreign keys and CHECK constraints in SQLite; enable foreign-key enforcement for every connection.
- Use composite uniqueness/foreign-key constraints where needed to prevent a child node, range, slot, or span from crossing template-version/worksheet ownership boundaries.
- Resolve inherited Header definitions in one parent lookup; do not materialize/copy inherited slots into child rows.
- No JSON blob as the primary persistence format. JSON may be used only for non-authoritative diagnostics/fingerprints if a later requirement justifies it.
- Keep the approved template version immutable. A new sample/layout produces a new version; historical report extraction remains reproducible.

## 6. Explicit exclusions

This proposal does not define:
- production semantic metric/dimension catalogs or source-label mappings;
- deterministic worksheet/table matcher algorithm or coordinate-drift policy;
- report-version/template-version selection if a company has multiple approved templates for the same report type;
- full template approval for Parsian;
- workbook archival or raw cell persistence;
- canonical financial fact schema, report-period schema, or runtime API shape;
- ORM classes, Alembic migrations, code, tests, or data migration.

These are separate tasks/gates. Do not begin implementation solely from this proposal.

## 7. Open implementation checks before ORM/migration

1. Inspect current ORM models and migration history to identify existing template-like tables or naming conflicts before adding any table.
2. Confirm report-type FK target and whether the existing ReportVersion can reference `template_version_id` without violating migration safety.
3. Decide whether `active_version_id` is needed; the safe baseline is to query the one APPROVED version and enforce a partial unique index.
4. Verify SQLite CHECK/partial-index support in the project's supported SQLite version.
5. Specify deterministic worksheet identity and layout matcher before accepting later workbooks.
6. Validate the proposed extraction-span compression against all gray coordinates, including blank-gray cells and gaps, before generating any template records.
7. Complete owner approval of candidate bounds and a separate-period drift-validation workbook before production approval.

## 8. Status

DB-DES-008 is a design proposal only. No code, ORM, migration, test, or database data has changed. It does not close DB-ING-006 / Task 033. Task 033 remains PARTIAL.


## 9. Gray extraction-span ownership audit — 2026-11-18

A coordinate-level reconciliation was performed from section 3 of `PARSIAN_PERIODIC_ANNOTATION_MAP_DRAFT.md` against the candidate parent/sub-table bounds and owner-confirmed gray-only extraction rule. This is a reconciliation of the recorded Markdown coordinate inventory; the assistant did not open the XLSX directly. All counts remain provisional until the owner approves the candidate geometry and the source workbook is validated.

### 9.1 Count reconciliation

The 17 table entries in the annotation map resolve to 459 gray target cells, matching the owner-supplied audit total. Compressing consecutive gray rows independently for each source column yields 60 vertical extraction spans. No span crosses an unannotated row gap.

| Table | Gray cells | Assigned to child sub-tables | Assigned to parent only | Total spans |
|---|---:|---:|---:|---:|
| T01 | 56 | 56 | 0 | 6 |
| T02 | 12 | 10 | 2 | 4 |
| T03 | 70 | 70 | 0 | 6 |
| T04 | 143 | 143 | 0 | 11 |
| T05 | 66 | 66 | 0 | 6 |
| T06 | 48 | 0 | 48 | 8 |
| T07 | 7 | 7 | 0 | 1 |
| T08 | 4 | 0 | 4 | 1 |
| T09 | 6 | 0 | 6 | 1 |
| T10 | 18 | 18 | 0 | 1 |
| T11 | 3 | 0 | 3 | 1 |
| T12 | 12 | 0 | 12 | 3 |
| T13 | 3 | 3 | 0 | 3 |
| T14 | 2 | 0 | 2 | 1 |
| T15 | 1 | 0 | 1 | 1 |
| T16 | 3 | 0 | 3 | 1 |
| T17 | 5 | 0 | 5 | 5 |
| **Total** | **459** | **373** | **86** | **60** |

The 60 spans comprise 36 child-owned spans and 24 parent-owned spans. T02's gray cells at row 62 remain parent-owned; its rows 64–68 fall within its green-marker child. All gray cells in the other listed child partitions are assigned to the corresponding child. Tables without a green-marker child retain their gray spans at the parent node.

### 9.2 Required ownership rule

To prevent duplicate extraction:

1. Every positive extraction coordinate belongs to exactly one `template_layout_node`.
2. If a gray coordinate lies inside a validated child SUBTABLE, assign it to that child node. Otherwise assign it to the parent TABLE node.
3. A parent-table request resolves the parent's own spans plus the spans of its descendants, each coordinate exactly once. A sub-table request resolves only that sub-table's own spans and any descendants it may have under a future explicitly approved extension.
4. Do not persist the same coordinate as both a parent span and a child span. Header inheritance does not change extraction-span ownership.
5. The validator must reject overlapping spans across nodes within the same worksheet/template version, not merely overlaps within one node. It must also reject a span outside its node's BODY range, outside the node's bounds, or mapped to an undefined/inherited-unresolved column slot.
6. A span is a contiguous vertical run in one source column. Split it at every non-gray row, including black or uncolored cells. A blank gray cell remains inside the span and is extracted as zero.

This makes parent-level retrieval a hierarchical query over node ownership, rather than duplicate persistence of parent and child targets.

### 9.3 Limits and acceptance conditions

- The 459-cell and 60-span reconciliation is based on the Markdown coordinate inventory and must not be represented as a fresh XLSX audit or production approval.
- Candidate bounds and child partitions remain unapproved except for the owner's reported spot checks.
- Before serialization, an owner-approved coordinate map must be used to regenerate spans, and an independent validator must prove: total target-cell count equals 459 for this sample; every target is inside exactly one node; no non-gray coordinate is included; all blank-gray coordinates remain included; and parent queries equal the union of parent-owned plus descendant-owned targets without duplicates.
- The current 60-span count is an expected result for the present candidate map, not a permanent schema invariant. A corrected annotation or approved layout revision may change it.

### 9.4 Design consequence

Keep `template_extraction_span.node_id` as the exclusive owner of each target. Add a cross-node overlap validation at TemplateVersion/worksheet scope. Parent retrieval must traverse the node hierarchy and union descendant spans; do not materialize duplicate parent copies of child spans. This is a refinement of DB-DES-008's proposed extraction-span model and does not authorize ORM, migration, runtime code, or production Template records.
