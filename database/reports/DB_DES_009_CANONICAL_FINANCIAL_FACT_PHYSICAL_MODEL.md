# DB-DES-009 — Canonical FinancialFact Physical Model and Provenance Proposal

**Status:** PROPOSED — physical design recommendation; no ORM, migration, runtime code, data, or tests changed  
**Date:** 2026-11-18  
**Scope:** Canonical financial input persistence for CODAL Excel, including dimension identity, value semantics, provenance, and compatibility with legacy models  
**Authority:** Database Contract V1.3, DB-DES-001, DB-DES-003, DB-DES-005, DB-DES-006, DB-DES-008, DB-AUD-009 through DB-AUD-013, and owner decisions recorded in the Master Working Packet

## 1. Executive decision

### 1.1 Recommended direction

Create a new canonical table named **`financial_facts`** for the new Excel ingestion path. Do not repurpose or alter `normalized_financial_facts` in place in this phase.

This is an additive transition design, not a decision to keep two canonical stores permanently:

- `financial_facts` becomes the only write target for the new Excel-to-canonical pipeline.
- Existing `normalized_financial_facts`, `normalized_financial_fact_inputs`, `raw_financial_facts`, their columns, rows, foreign keys, and legacy callers remain untouched until a separate compatibility and retirement task.
- Do not backfill old normalized/raw rows into the new table automatically. Their semantic equivalence, source value fidelity, dimension identity, and standard-version provenance have not been established.
- Do not dual-write one incoming Excel fact into both old and new fact tables.
- After the new pipeline is proven, legacy model/table retirement can be evaluated independently using actual environment, linkage, backup, migration-9, and consumer evidence.

### 1.2 Why not redesign `normalized_financial_facts` in place?

The current table is not a neutral empty shell. It has an existing schema and legacy semantics:
- `value_irr NUMERIC(30,4)` assumes Rial monetary values and conflicts with the owner-approved SQLite INTEGER policy.
- Its unique key omits dimensions.
- Its provenance fields point to legacy raw facts/mapping decisions.
- Existing model and foreign-key relationships may be consumed by legacy code or tests, even though the local linkage audit found no rows in three downstream tables.
- Migration 9 lineage and deployed database state remain unresolved.

Changing this table in place would couple the new Excel design to legacy data conversion and migration uncertainty before the new contract is validated. A new table allows an additive migration and a clean writer boundary while preserving every legacy row and schema object.

### 1.3 Important limitation

The new table is a transition boundary, not permission to leave two competing canonical APIs indefinitely. A later task must define when legacy consumers are migrated and when the old table can be retired. Until then, old and new facts must not be silently merged or treated as interchangeable.

## 2. Physical model overview

Recommended logical entities:

1. `report_types` — controlled catalog for the two V1 report types.
2. Existing `reports` and `report_versions` — retained and extended for source/revision and standard provenance.
3. `financial_periods` — redesigned for authoritative Jalali dates and INSTANT/DURATION semantics.
4. Existing `financial_metrics` — retained as the stable metric catalog and extended only where the semantic contract requires it.
5. `financial_dimensions`, `financial_dimension_values`, `financial_dimension_sets`, `financial_dimension_set_members` — approved, queryable dimension identity.
6. `financial_facts` — new canonical source-reported fact table.
7. `financial_fact_provenance` — one-to-many, minimal lineage to the structural/semantic source that produced a fact, without raw workbook rows or mandatory cell coordinates.
8. Existing `ingestion_runs` — retained and extended only as needed for the DB-DES-005 operational audit contract.

The exact SQLAlchemy naming convention and integer PK strategy can follow the repository's current conventions. This proposal defines semantics and constraints, not migration code.

## 3. Report and ReportVersion

### 3.1 ReportType catalog

Create `report_types` with stable integer PK and unique controlled `report_type_code`.

V1 allowed codes:
- `MONTHLY_ACTIVITY`
- `PERIODIC_FINANCIAL`

No arbitrary free-text report type is accepted by the new pipeline. The existing `reports.report_type` column must not be converted or backfilled until all existing values (including `CODAL_XLSX_TEMP_TEST`) have been classified. The local value `CODAL_XLSX_TEMP_TEST` is not automatically promoted to a production catalog entry.

### 3.2 Reuse Report and ReportVersion

Retain Report as the logical report identity and ReportVersion as the immutable published revision. Extend ReportVersion (or an equivalent one-to-one source-version record if required by migration compatibility) with:

| Field | Meaning |
|---|---|
| `source_artifact_ref` | External/source-system reference or URL; not a stored workbook path/archive |
| `source_artifact_sha256` | SHA-256 of the exact source artifact used |
| `source_revision_key` | Source-issued revision identity when available; not inferred from the file hash |
| `template_version_id` | Exact approved Company Table Layout Template version used |
| `interpretation_standard_version_id` | Exact approved industry/report-family semantic + temporal + value interpretation bundle used |
| `ingestion_run_id` | Run responsible for creating this ReportVersion, if the existing run model does not already provide the reverse link |

The source artifact hash establishes byte identity/integrity; it does **not** alone establish economic revision identity or publication precedence. CODAL publication datetime and the approved ReportVersion ranking/PIT rules remain authoritative.

A ReportVersion must be bound to exactly one template version and one interpretation-standard version before its facts can be admitted. These references are immutable after successful ingestion. Historical ReportVersions may remain NULL during transition; new Excel ingestion may not.

### 3.3 Report primary period

The report-level period is descriptive metadata only. A ReportVersion can publish facts for several actual periods, and every fact links to its own FinancialPeriod. The current NOT NULL `reports.financial_period_id` must not be allowed to impose one period on every fact.

Physical options:
- make the report-level period nullable for new/legacy compatibility and treat it as optional primary-period metadata; or
- move primary-period metadata to a separate optional report/version association.

Choose the least disruptive option after checking all current readers and migrations. Do not synthesize a primary period when the source does not establish one.

## 4. FinancialPeriod physical contract

The new/updated `financial_periods` model must use Jalali components as authoritative values; no Gregorian conversion is required or permitted as a substitute.

Required logical fields:
- `period_id`
- `company_id`
- `temporal_kind`: `INSTANT` or `DURATION`
- `period_type`: controlled source interval class (for example MONTH, QUARTER, SEMI_ANNUAL, NINE_MONTH, ANNUAL); TTM is not a source period
- `start_year_jalali`, `start_month_jalali`, `start_day_jalali`
- `end_year_jalali`, `end_month_jalali`, `end_day_jalali`
- `fiscal_year`, optional `fiscal_quarter`
- `months_length`
- nullable `is_ytd` where not applicable

Constraints:
- INSTANT: start = end, months_length = 0, is_ytd is not applicable/NULL.
- DURATION: start <= end, months_length > 0; YTD must be explicitly true/false when applicable to a flow value.
- fiscal quarter, if present, is 1–4.
- unique logical period identity: company + temporal_kind + exact Jalali start + exact Jalali end. Period type/fiscal labels are validated attributes, not substitutes for exact dates.
- no TTM source-period rows; TTM is runtime-only.
- do not migrate existing Gregorian Date values by guessing their Jalali meaning. Existing data requires a separate evidence-based migration plan.

If one FinancialPeriod can legitimately be shared across metrics with different YTD applicability, the period row should represent temporal shape and actual dates while YTD/standalone belongs to the fact's temporal interpretation. This must be reconciled with DB-DES-003 before implementation; do not force an ambiguous global `is_ytd` onto all facts.

## 5. Dimension identity

### 5.1 Why a dimension-set entity is required

A fact can have zero, one, or several approved value-defining dimensions. A unique key over only ReportVersion, period, and metric is insufficient. A relational many-to-many child table alone cannot enforce uniqueness of the complete dimension combination on the fact row.

Use a canonical `financial_dimension_sets` parent:
- `dimension_set_id` PK
- `canonical_key` TEXT NOT NULL UNIQUE
- optional schema/version metadata

Store the members in `financial_dimension_set_members`:
- `dimension_set_id`
- `dimension_id`
- `dimension_value_id`

Catalogs:
- `financial_dimensions`: stable `dimension_code`, name, data/industry scope and lifecycle.
- `financial_dimension_values`: approved stable value code/label belonging to one dimension.
- member constraints: one value per dimension per set; no duplicate member; every value must belong to the stated dimension.

Canonical key rules:
- build from approved dimension codes and approved value codes only;
- sort members deterministically by dimension code;
- use an unambiguous canonical encoding (for example compact canonical JSON with fixed key ordering and Unicode normalization);
- the empty dimension set is a real shared set (canonical key `[]`) and is used when a metric has no approved dimensions;
- application validation must verify that the stored members exactly reproduce canonical_key. Do not rely on a hash alone as the authoritative identity.

The dimension catalog and approved dimension values are semantic definitions; raw row labels or arbitrary strings must not create new dimensions at ingestion time.

## 6. Canonical FinancialFact table

### 6.1 Proposed fields

Table: `financial_facts`

| Field | Type / meaning | Required |
|---|---|---|
| `fact_id` | INTEGER PK | Yes |
| `report_version_id` | FK to publishing ReportVersion | Yes |
| `period_id` | FK to actual Jalali FinancialPeriod | Yes |
| `metric_id` | FK to stable FinancialMetric | Yes |
| `dimension_set_id` | FK to approved dimension set; empty set when no dimensions | Yes |
| `value_integer` | SQLite INTEGER canonical value; NULL only for explicit NULL state | Conditional |
| `value_state` | `REPORTED_VALUE`, `REPORTED_NULL`, `ZERO_FALLBACK` | Yes |
| `source_unit_code` | Unit as reported by source | As applicable |
| `source_currency_code` | Currency as reported by source | As applicable |
| `source_basis_code` | Source measurement basis (for example per-share, per-ton, period-total, closing-balance) | As applicable |
| `canonical_unit_code` | Unit of persisted canonical integer | As applicable |
| `canonical_currency_code` | Canonical currency, when monetary | As applicable |
| `canonical_basis_code` | Canonical measurement basis | As applicable |
| `scenario_code` | ACTUAL / FORECAST / PLAN when in-scope | Yes, default/explicit policy to be finalized |
| `created_at` | Operational creation timestamp | Yes |

Do not add a duplicated `company_id` unless a measured query or integrity requirement justifies it. Company is derivable through ReportVersion → Report → Company. If denormalized for query speed, enforce company consistency with composite foreign keys or equivalent database constraints, not only a Python check.

### 6.2 Value state rules

- `REPORTED_VALUE`: value_integer is NOT NULL. A genuine source zero is `REPORTED_VALUE` with integer 0.
- `REPORTED_NULL`: value_integer IS NULL; it means the source explicitly reported an applicable NULL/blank state under the approved extraction contract.
- `ZERO_FALLBACK`: value_integer = 0 and the applicable versioned standard explicitly authorizes fallback for that exact metric/context (currently only the narrow product-sales rule in the architecture contract).
- A missing observation, uncolored cell, excluded/black cell, unknown candidate, or absent fact is not a FinancialFact and must not be represented as NULL or ZERO_FALLBACK.
- Blank gray cells in the approved company template are interpreted as zero by the owner-approved extraction rule; the template/interpretation layer must explicitly convert that observation to the appropriate zero state. Do not make the structural Reader itself rewrite BLANK to numeric zero.
- DB CHECK constraints must enforce the allowed state/value combinations.

### 6.3 Integer and rounding policy

- Persist canonical values using SQLite signed 64-bit INTEGER.
- Parse and transform using Decimal, never binary float for financial normalization.
- Apply owner-approved ROUND_HALF_UP exactly once at the persistence boundary.
- Reject values outside signed 64-bit range; never wrap, truncate, or store approximate floats.
- The owner's approved policy intentionally stores numeric values as integers without decimal precision. Do not add a generic decimal-scale mechanism that silently reverses this decision.
- Unit/basis codes must make the integer's meaning explicit. No implicit conversion or rescaling is permitted; every allowed transformation must be part of the versioned interpretation standard and recorded through the source/canonical unit and basis fields.

### 6.4 Fact identity and uniqueness

Required unique logical identity:

`(report_version_id, period_id, metric_id, dimension_set_id)`

This is the database-level identity for a source fact within one published ReportVersion. A duplicate identity with the same canonical payload is an unchanged duplicate/replay. The same identity with a different payload is a hard conflict unless a separately approved source-revision rule creates a new ReportVersion. Never overwrite or last-write-wins.

Scenario and any other value-defining distinction must be represented as an approved dimension so it participates in dimension_set_id. A presentation distinction that is not an approved dimension must not create a second fact with the same identity; conflicting candidates must be resolved by the standard or reject the whole ingestion unit.

The database unique constraint is mandatory for concurrency safety.

## 7. Minimal multi-input provenance

### 7.1 Proposed `financial_fact_provenance`

One fact may derive from one source cell or several coordinated source observations. Preserve the source relationship without storing raw rows, cell payloads, or mandatory cell coordinates.

Proposed fields:
- `provenance_id` INTEGER PK
- `fact_id` FK to `financial_facts`
- `input_role`: DIRECT, COMPONENT, TOTAL, SUBTOTAL, or another explicitly approved role
- `template_node_id`: stable table/sub-table node in the exact template version
- `column_slot_id`: stable physical column slot, where relevant
- `semantic_mapping_id` or equivalent immutable mapping-version reference
- optional `source_locator` for short-lived diagnostics only; not required for canonical validity and not a raw value

One fact can have multiple provenance rows. Use a unique constraint over fact + source structural identity + input role to prevent accidental duplicate links. Enforce that referenced node/slot/mapping belongs to the same template/interpretation versions bound to the ReportVersion.

Do not store:
- raw cell value/text;
- entire source row;
- workbook binary/archive;
- a permanent cell-coordinate requirement;
- legacy `raw_fact_id` or `mapping_decision_id` as a required bridge.

If a fact cannot be traced to at least one valid structural/semantic source reference, reject it unless an explicitly approved non-workbook source type defines another provenance shape.

### 7.2 Version inheritance

The exact template and interpretation standard are fixed on ReportVersion. Provenance rows refer to nodes/slots/mapping definitions within those exact versions. This avoids copying version IDs to every fact while still making the version chain provable. If facts from one ReportVersion can legitimately use different standard versions, this assumption is invalid and the model must instead bind standard versions at fact level; no such mixed-version case is currently established.

## 8. IngestionRun, atomicity, and idempotency

Keep DB-DES-005 as the transaction authority:
- Run STARTED is durably created before parsing/validation.
- Parsing and interpretation stage facts in memory; no canonical rows are written before whole-unit admission.
- On any hard error, no ReportVersion, FinancialFact, or provenance row is committed; Run becomes FAILED in an independent transaction.
- On success, Report/ReportVersion, all FinancialFacts, all provenance rows, and Run COMPLETED commit in one transaction.
- A failure in any write/constraint rolls back all canonical writes.
- Retry creates a new Run; the prior Run remains terminal and immutable.
- Exact source revision + profile + interpretation/template versions + canonical payload determine idempotent replay. File hash alone is not revision identity.
- Same fact identity + same payload is unchanged; same identity + different payload is a hard conflict.
- No per-row commit, partial batch acceptance, or dual-write to legacy normalized facts.

Run should record the source identity/fingerprint and adapter/profile/standard versions needed for operational replay. It must not become a raw workbook archive.

## 9. Integrity and indexing requirements

Minimum constraints/indexes:
1. `financial_facts` UNIQUE(report_version_id, period_id, metric_id, dimension_set_id).
2. FK constraints from every fact to ReportVersion, FinancialPeriod, FinancialMetric and DimensionSet.
3. CHECK constraints for value_state/value_integer combinations and allowed scenario codes.
4. UNIQUE report type code, metric code, dimension code/value code, template version number and interpretation-standard version identity.
5. Jalali component range checks and period-kind/date-shape checks; full Jalali leap-year/day validation belongs in the domain validator unless a deterministic SQLite function is deliberately deployed.
6. UNIQUE dimension set canonical_key and UNIQUE dimension member per dimension.
7. FK/validation rules that ensure a provenance node, column slot and semantic mapping belong to the exact versions attached to the publishing ReportVersion.
8. Indexes for common reads beginning with ReportVersion, period, metric, dimension set; add company/industry indexes only where the query plan justifies them.
9. Enable and verify SQLite foreign keys on every connection, as current project infrastructure already intends.

Cross-entity company consistency must be enforced. Prefer composite FKs backed by matching UNIQUE keys where practical; otherwise use database triggers plus service validation. Python-only checks are not sufficient for relationships whose violation would produce a fact assigned to another company's period or metric scope.

## 10. Compatibility and migration strategy

This proposal authorizes no migration. The later migration plan should be additive and staged:

**Migration A — catalogs and new canonical structures**
- Add ReportType and interpretation-standard catalogs/records.
- Add/extend ReportVersion source artifact and exact standard/template bindings.
- Add Jalali FinancialPeriod representation with a non-destructive transition strategy.
- Add dimension catalogs/sets/members.
- Add `financial_facts` and `financial_fact_provenance`.
- Preserve every existing table, column, row, FK and index unless a separate approved compatibility task authorizes a specific change.

**Migration B — new Excel writer**
- Implement Excel interpretation and canonical write to `financial_facts` only.
- Keep the legacy PDF/RawFinancialFact writer isolated until PDF retirement gates are satisfied.
- No dual-write to `normalized_financial_facts`.
- Prove idempotency, atomicity, uniqueness, dimension identity, provenance, NULL/zero/fallback and signed 64-bit boundaries.

**Migration C — consumer transition**
- Inventory every reader of `normalized_financial_facts` and its provenance tables.
- Migrate consumers deliberately, with explicit compatibility adapters only where necessary.
- Do not union old and new rows without a proven equivalence and version policy.

**Migration D — legacy retirement (separate authorization)**
- Reconcile Migration 9 with source and all target environments.
- Re-run linkage and consumer/backup audits on the exact target DB.
- Retire PDF write paths first.
- Only then decide whether RawFinancialFact, NormalizedFinancialFact, their FKs, and legacy mapping/provenance models can be removed. This proposal does not authorize their removal.

## 11. Open decisions / implementation gates

The following must be resolved before ORM/migration implementation:

1. **Interpretation standard catalog:** confirm the exact logical bundle represented by `interpretation_standard_version_id` (industry + report type/family + semantic/temporal/value mapping version) and whether it can be singular for one ReportVersion.
2. **Dimension catalog scope:** define which dimensions are globally shared versus industry/report-family scoped, and how approved values are versioned/retired without changing historical meaning.
3. **Temporal ownership:** reconcile whether `is_ytd` belongs on FinancialPeriod or on a fact-level temporal interpretation, because one ReportVersion can contain facts with different temporal bases and one period may be reused.
4. **Source revision key:** establish the CODAL source identifier/revision fields available in the actual acquisition contract; do not infer revision from SHA-256.
5. **Report primary period:** inspect consumers before making current `reports.financial_period_id` nullable or moving it.
6. **Company consistency constraints:** choose composite FK/trigger strategy after examining SQLite migration patterns and SQLAlchemy model support.
7. **Provenance granularity:** validate that table node + column slot + semantic mapping reference is enough for direct and multi-input facts; exact cell coordinates remain optional.
8. **ReportVersion standard binding:** verify that one template + one interpretation bundle is sufficient for all facts in one version.
9. **Existing model consumer inventory:** inspect all reads/writes of NormalizedFinancialFact, NormalizedFinancialFactInput and Derived* before planning transition.
10. **Migration 9:** reconcile the local DB migration 9 with repository runner before any migration sequence is drafted.

## 12. Decision table

| Question | Recommendation | Status |
|---|---|---|
| Reuse Report / ReportVersion? | Yes, extend; ReportVersion remains publication/revision anchor | PROPOSED |
| Reuse FinancialPeriod as-is? | No; redesign to authoritative Jalali + INSTANT/DURATION | PROPOSED |
| Reuse FinancialMetric? | Yes, retain stable identity; extend semantic constraints/catalog separately | PROPOSED |
| Redesign NormalizedFinancialFact in place? | No, not in this transition; preserve as legacy | PROPOSED |
| Create a new FinancialFact table? | Yes: `financial_facts` | PROPOSED |
| Store dimension members directly on fact? | No; use a canonical dimension-set parent and members | PROPOSED |
| Store raw Excel rows/cells? | No | ALREADY OWNER-APPROVED |
| Require permanent exact cell locator? | No | ALREADY OWNER-APPROVED |
| Store canonical values as INTEGER? | Yes, signed 64-bit; Decimal + ROUND_HALF_UP once | ALREADY OWNER-APPROVED |
| Remove legacy Raw/Normalized tables now? | No | NOT AUTHORIZED |

## 13. Acceptance criteria for DB-DES-009

- The comparison of in-place redesign vs additive new table is explicit.
- A physical canonical fact identity includes the complete approved dimension-set identity.
- NULL, genuine zero, and ZERO_FALLBACK are distinguishable and constrained.
- Source and canonical unit/currency/basis semantics are preserved.
- Exact ReportVersion, period, metric, template and interpretation-standard lineage is provable.
- Multi-input provenance does not require RawFinancialFact or permanent raw-cell storage.
- INTEGER/Decimal/ROUND_HALF_UP and signed 64-bit rules are preserved.
- Atomicity, replay, duplicate and conflict behavior align with DB-DES-005.
- Existing legacy schema/data/FKs are preserved; Migration 9 remains a gate.
- No ORM, migration, data or test change is performed by this proposal.

**Current result:** DB-DES-009 proposal drafted. Owner review and resolution of the listed implementation gates are required before physical implementation. No code, ORM, migration, data or tests changed.
