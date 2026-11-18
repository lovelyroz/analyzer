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
- no YTD/standalone field; FinancialPeriod identifies only actual dates and temporal shape

Constraints:
- INSTANT: start = end, months_length = 0; no duration basis exists on the period or its INSTANT facts.
- DURATION: start <= end; the source-supported interval and months_length rules apply. Each applicable FinancialFact carries `duration_basis=YTD` or `STANDALONE`.
- fiscal quarter, if present, is 1–4.
- unique logical period identity: company + temporal_kind + exact Jalali start + exact Jalali end. Period type/fiscal labels are validated attributes, not substitutes for exact dates.
- no TTM source-period rows; TTM is runtime-only.
- do not migrate existing Gregorian Date values by guessing their Jalali meaning. Existing data requires a separate evidence-based migration plan.

FinancialPeriod is reusable by facts that describe the same company, temporal kind and exact Jalali dates. It never stores YTD/standalone. This is a resolved design decision: `duration_basis` belongs on each applicable FinancialFact, not on a shared period row.

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
| `duration_basis` | `YTD` or `STANDALONE` for applicable DURATION values; NULL / NOT_APPLICABLE for INSTANT | Conditional
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
3. **Temporal basis constraints:** implement the resolved fact-level `duration_basis`; validate applicability against FinancialPeriod temporal_kind and the approved metric definition.
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
| Reuse FinancialPeriod as-is? | No; redesign to authoritative Jalali + INSTANT/DURATION, without YTD field | PROPOSED |
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


## 14. بررسی فنی Gate 6 — Company Consistency با SQLite — 2026-11-18

### 14.1 وضعیت فعلی مدل و زیرساخت
- `FinancialPeriod` دارای `company_id` و FK ساده به `companies.company_id` است؛ کلید یکتای فعلی آن `(company_id, fiscal_year, period_type, end_date)` است و کلید یکتای `(period_id, company_id)` ندارد.
- `Report` نیز `company_id` و `financial_period_id` را جداگانه نگه می‌دارد؛ FKها به‌تنهایی تضمین نمی‌کنند که دورهٔ گزارش متعلق به همان شرکت باشد.
- `ReportVersion` از طریق `report_id` به Report و سپس Company می‌رسد.
- `RawFinancialFact` در مدل legacy هم `company_id`، `report_version_id` و `period_id` را جداگانه دارد و در سطح DB رابطهٔ برابری شرکت را enforce نمی‌کند. writer فعلی CODAL این سازگاری را در Python بررسی می‌کند؛ این کنترل برای direct SQL کافی نیست.
- `src/core/database.py` روی engine اصلی پروژه با SQLAlchemy connect event، `PRAGMA foreign_keys=ON` را اجرا می‌کند. Migration runner نیز از `engine.begin()` و SQL خام برای migrationها استفاده می‌کند. در تست‌ها engineهای مستقل با `create_engine("sqlite:///:memory:")` ساخته می‌شوند و listener مربوط به engine اصلی را خودکار به ارث نمی‌برند.
- در migrationهای فعلی نمونه‌ای از ایجاد trigger دیده نشد؛ اما runner اجرای SQL خام را پشتیبانی می‌کند. Triggerهای SQLite را می‌توان در migration با `CREATE TRIGGER` ساخت؛ SQLAlchemy ORM برای تعریف آن‌ها به‌تنهایی کافی نیست و باید DDL صریح migration و تست جداگانه داشته باشد.

### 14.2 ارزیابی دو راهکار
**Composite Foreign Key:** برای enforce کردن برابری شرکت، باید company identity در هر دو سمت کلید مرکب قابل ارجاع باشد. در مدل فعلی `ReportVersion` شرکت را مستقیم نگه نمی‌دارد و از Report به آن می‌رسد؛ `financial_facts` نیز طبق پیشنهاد فعلی company_id تکراری ندارد. بنابراین راهکار composite FK بدون denormalization اضافی یا تغییر چند parent table به‌سادگی قابل اعمال نیست. اضافه کردن company_id فقط برای ساخت FK، هزینهٔ تکرار داده و مسیرهای update/immutability را افزایش می‌دهد.

**SQLite Trigger + Service Validation:** چون شرکت از زنجیرهٔ `FinancialFact → ReportVersion → Report → Company` قابل استخراج است و FinancialPeriod نیز company_id مستقل دارد، trigger می‌تواند دو مسیر را join و برابری را در خود DB enforce کند؛ نیازی به ذخیرهٔ مجدد company_id روی FinancialFact نیست. Service validation نیز پیام خطای زودهنگام و قابل‌فهم‌تری می‌دهد، اما جای trigger را نمی‌گیرد.

### 14.3 توصیهٔ طراحی
برای جدول جدید `financial_facts`، **SQLite triggers به‌همراه service validation** توصیه می‌شود؛ company_id در FinancialFact تکرار نشود، مگر آنکه بعداً نیاز query/کارایی با benchmark واقعی ثابت شود.

حداقل پوشش triggerها:
1. پیش از INSERT در `financial_facts`، شرکت ReportVersion (از مسیر Report) با شرکت FinancialPeriod مقایسه شود؛ نبود هر یک از دو مسیر نیز باید رد شود و FKهای معمولی همچنان برقرار بمانند.
2. پیش از UPDATE ستون‌های `report_version_id` یا `period_id` در `financial_facts`، همان invariant دوباره کنترل شود.
3. پس از ایجاد Fact، تغییر هویت رابطه‌ای والدها نباید invariant را بی‌صدا خراب کند. سیاست پیشنهادی این است که تغییر `reports.company_id`، `report_versions.report_id` یا `financial_periods.company_id` تا وقتی Fact وابسته وجود دارد ممنوع باشد؛ اصلاح هویت با ساخت رکورد صحیح و مسیر اصلاح کنترل‌شده انجام شود، نه reassignment خام.
4. اگر `Report.financial_period_id` در مدل نهایی به‌صورت optional metadata باقی بماند، trigger جداگانه باید در صورت non-NULL بودن، تطابق شرکت Report و FinancialPeriod را enforce کند؛ NULL بودن این metadata نباید مانع ثبت Fact دارای period_id مستقل شود.
5. حذف parentها باید با FKهای معمولی و رفتار RESTRICT/NO ACTION محافظت شود؛ cascade ناخواسته برای دادهٔ مالی مجاز نیست.

### 14.4 شروط پیش از بستن کامل gate
- پیش از نصب trigger روی دیتابیس واقعی، audit read-only باید تمام ردیف‌های موجود را از نظر mismatch شرکت بررسی کند؛ trigger جدید دادهٔ ناسازگار موجود را خودبه‌خود اصلاح نمی‌کند.
- DDL باید idempotent باشد (`DROP/CREATE` کنترل‌شده یا `CREATE TRIGGER IF NOT EXISTS` با versioning دقیق) و در migration مستقل/additive قرار گیرد.
- تست باید INSERT ناسازگار، UPDATE ناسازگار، تغییر هویت والد پس از ایجاد Fact، و حالت معتبر را پوشش دهد.
- تست trigger باید با SQLite واقعی اجرا شود. تست FKهای معمولی باید روی هر connection تست نیز صریحاً `PRAGMA foreign_keys=ON` داشته باشد؛ در غیر این صورت تست ممکن است constraintهای FK را بی‌اثر اجرا کند.
- هیچ‌یک از این triggerها نباید قبل از ممیزی داده و طراحی migration به جداول legacy اعمال شود.

**نتیجه Gate 6:** انتخاب راهکار در سطح طراحی انجام شد: Trigger + Service Validation برای `financial_facts`، بدون denormalized company_id. Gate از نظر انتخاب معماری قابل بستن است، اما پیاده‌سازی، DDL، migration، audit دیتابیس مقصد و تست‌های پذیرش همچنان باز و غیرمجاز هستند تا مجوز مرحلهٔ اجرا صادر شود. هیچ کد، ORM، schema، migration، دیتابیس یا تستی تغییر نکرد/اجرا نشد.


## 15. بررسی Gate 7 — کفایت Provenance ساختاری و معنایی — 2026-11-18

### 15.1 شواهد بررسی‌شده
- `DB-DES-008` ساختار فیزیکی Template را با شناسه‌های پایدار `template_layout_node`، `template_column_slot`، Header binding و extraction span پیشنهاد می‌کند. مختصات A1 فقط locator است؛ هویت معنایی نیست.
- `DB-DES-014` قرارداد معنایی را تکمیل می‌کند: معنای Fact در تقاطع row-axis path و column Header path تعیین می‌شود. Mapping باید به TemplateVersion، layout node، Header definition/path، ColumnSlot، row-axis path، Metric، Dimension، دوره و temporal/value semantics مقید باشد. هیچ column به‌تنهایی Metric نیست و هیچ row label به‌تنهایی در همهٔ جدول‌ها معنای ثابت ندارد.
- Excel Reader DTO فعلی `CellRef`، `RowObservation`، `ColumnObservation`، `TableObservation` و Header fragmentهای چندسطری/ادغام‌شده را به‌صورت immutable observation نگه می‌دارد. این DTOها مختصات و روابط مشاهده‌شده را ثبت می‌کنند، اما stable template IDs یا semantic mapping IDs تولید نمی‌کنند؛ این جداسازی با نقش read-only Reader سازگار است.
- مدل legacy `normalized_financial_fact_inputs` فقط پل میان NormalizedFact و RawFact/MappingDecision است و برای قرارداد جدید نباید به‌عنوان طرح فیزیکی مرجع استفاده شود.

### 15.2 کفایت ساختار پیشنهادی DB-DES-009
فیلدهای پیشنهادی `financial_fact_provenance`:
- `fact_id`
- `input_role`
- `template_node_id`
- `column_slot_id` در موارد مرتبط
- `semantic_mapping_id` یا مرجع immutable معادل
- `source_locator` اختیاری و صرفاً تشخیصی

این ساختار **از نظر منطقی کفایت می‌کند، مشروط به اینکه** `semantic_mapping_id` به یک mapping نسخه‌دار و دقیق اشاره کند که row-axis path کامل، Header path کامل، context جدول/زیرجدول، معنای Metric/Dimension، period و temporal basis، واحد/مبنای اندازه‌گیری و value semantics را در scope همان TemplateVersion و interpretation standard مشخص کند. در این صورت نیازی به ذخیرهٔ دائمی row index یا cell coordinate روی هر Fact نیست؛ semantic mapping هویت معنایی را اثبات می‌کند و template node/column slot هویت ساختاری را.

برای Provenance:
- Fact مستقیم: یک ردیف provenance با `input_role=DIRECT`.
- Fact دارای چند observation ورودی: یک ردیف برای هر منبع مستقل، با نقش مصوب همان ورودی (مانند COMPONENT/TOTAL/SUBTOTAL)؛ تمام ردیف‌ها به یک Fact متصل می‌شوند.
- هر ردیف provenance باید به ساختار و mapping دقیق همان ReportVersion و نسخه‌های Template/Interpretation متصل باشد.
- مختصات سلول/محدوده می‌تواند برای عیب‌یابی موقت ثبت شود، اما نه شرط اعتبار Fact است و نه هویت پایدار آن.
- raw cell value، raw row، workbook archive و legacy raw_fact_id/mapping_decision_id در این رابطه وارد نمی‌شوند.

### 15.3 شکاف فیزیکی حل‌نشده
DB-DES-014 قرارداد منطقی row-axis path و SemanticMappingRule را تعریف کرده، اما physical schema کامل برای ذخیرهٔ سلسله‌مراتب row-axis و mappingهای نسخه‌دار هنوز طراحی/تصویب نشده است. DB-DES-008 نیز عمدتاً layout node، range، Header binding، ColumnSlot و extraction span را تعریف می‌کند و به‌تنهایی row-axis semantic identity را کامل نمی‌کند.

بنابراین `semantic_mapping_id` فقط زمانی یک مرجع کافی است که جدول/مدل SemanticMapping واقعاً کل row-axis path و Header path را به‌شکل immutable و قابل اعتبارسنجی نگه دارد؛ یک شناسه به جدول mapping ناقص یا mapping متکی بر متن آزاد، این شرط را برآورده نمی‌کند.

همچنین پیش از physical design باید اثبات شود که برای چند ورودی یک Fact، ترکیب `fact_id + structural source identity + input_role` جلوی duplicate link را می‌گیرد و هر منبع متمایز را بدون ابهام حفظ می‌کند. اگر دو ورودی متمایز بتوانند دقیقاً همین هویت را داشته باشند، باید identity تکمیلیِ نسخه‌دار تعریف شود؛ نه اینکه مختصات سلول به‌صورت پیش‌فرض به کلید دائمی تبدیل شود.

### 15.4 تصمیم و وضعیت Gate 7
1. الگوی یک ردیف provenance برای هر منبع ورودی مستقل و چند ردیف برای Fact چندمنبعی تأیید طراحی می‌شود.
2. `template_node_id` و `column_slot_id` هویت ساختاری را می‌دهند؛ `semantic_mapping_id` باید هویت کامل row/column semantic intersection را ثابت کند.
3. ذخیرهٔ دائمی مختصات دقیق سلول یا raw cell data الزامی نیست.
4. physical schema مربوط به row-axis و SemanticMapping باید پیش از ORM/Migration طراحی و با یک نمونهٔ واقعی direct و یک نمونهٔ multi-input اثبات شود.

**نتیجه:** Gate 7 در سطح قرارداد منطقی تا حد زیادی حل شده، اما از نظر physical provenance **PARTIAL / OPEN** می‌ماند تا مدل نسخه‌دار row-axis و semantic mapping و مثال‌های پذیرش مشخص شوند. هیچ کد، ORM، schema، migration، دیتابیس یا تستی تغییر نکرد/اجرا نشد.


## 16. بررسی Gate 8 — کفایت یک TemplateVersion و یک Interpretation Bundle برای هر ReportVersion — 2026-11-18

### 16.1 زنجیرهٔ هویت
- هر `ReportVersion` به دقیقاً یک `Report` متصل است.
- هر `Report` یک `company_id` و یک `report_type` دارد؛ بنابراین هر نسخه از یک شرکت و یک خانواده/نوع گزارش به ارث می‌برد.
- Template در DB-DES-008 در scope شرکت + report type تعریف می‌شود و TemplateVersion تمام ساختار workbook را پوشش می‌دهد: worksheetها، parent tableها، sub-tableها، Headerها، column slotها و extraction spanها. Template به یک جدول منفرد محدود نیست.
- شرکت در دامنهٔ فعلی به یک Industry تعلق دارد؛ بنابراین استاندارد تفسیر می‌تواند در scope شرکت/industry + report family بسته‌بندی شود.
- DB-DES-014 صریحاً می‌خواهد هر ReportVersion پذیرفته‌شده در Excel pipeline دقیقاً یک interpretation-standard version داشته باشد؛ آن bundle می‌تواند به semantic mapping versionهای متعدد و مرتبط با TemplateVersion ارجاع دهد.

### 16.2 آزمون مفهومی سناریوها
- وجود چند worksheet، چند table/sub-table، چند Metric، چند Dimension یا چند FinancialPeriod در یک workbook، به‌تنهایی نیاز به چند TemplateVersion یا چند Interpretation Bundle ایجاد نمی‌کند؛ یک TemplateVersion تمام layout همان workbook و یک bundle تمام mapping ruleهای مصوب آن report family را پوشش می‌دهد.
- مقادیر comparative و primary در دوره‌های مختلف همچنان زیر همان ReportVersion منتشرکننده قرار می‌گیرند؛ تفاوت دوره و نقش زمانی در mapping/fact است، نه در هویت TemplateVersion.
- یک Fact چندمنبعی می‌تواند چند provenance row داشته باشد؛ این امر نیز به معنی چند interpretation bundle نیست، مشروط بر اینکه تمام ورودی‌ها تحت همان نسخهٔ استاندارد و template تفسیر شوند.
- اگر یک workbook واقعاً دو report family مستقل یا دو ساختار ناسازگار را در یک واحد انتشار ترکیب کند، نباید برای یک ReportVersion چند template/standard را بی‌قاعده مخلوط کرد. ابتدا باید identity/report-family آن ورودی تعیین شود؛ در V1 چنین ورودی‌ای تا زمان تعریف قرارداد مشخص باید reject/quarantine شود یا به واحدهای گزارش مستقل تقسیم شود، نه اینکه یک ReportVersion چند bundle بگیرد.
- تغییر Template یا Interpretation Bundle در بازپردازش همان ReportVersion، نسخهٔ جدیدی از همان انتشار محسوب نمی‌شود و نباید بی‌صدا روی نسخهٔ پذیرفته‌شده overwrite شود؛ reprocessing/reclassification باید مسیر کنترل‌شده و audit trail مستقل داشته باشد.

### 16.3 تصمیم طراحی
برای V1، هر ReportVersion دقیقاً:
1. به یک Report و در نتیجه یک Company و یک ReportType تعلق دارد؛
2. به یک TemplateVersion که کل workbook را پوشش می‌دهد bind می‌شود؛
3. به یک InterpretationStandardVersion واحد bind می‌شود؛ این bundle می‌تواند مجموعه‌ای از semantic mapping versionهای متعدد را در خود ارجاع دهد؛
4. تمام FinancialFactها و provenanceهای آن نسخه باید با همین دو binding سازگار باشند.

یک workbook چندجدولی/چنددوره‌ای دلیل کافی برای چند binding نیست. چند binding فقط در صورتی قابل طرح است که بعداً شواهد واقعی از یک واحد انتشار با چند report family مستقل ارائه شود؛ چنین موردی در scope فعلی تثبیت نشده است.

**نتیجه Gate 8:** فرض یک TemplateVersion + یک Interpretation Bundle برای هر ReportVersion در scope فعلی پذیرفته می‌شود و gate در سطح logical design بسته است. Physical schema باید bindingهای NOT NULL/immutable و ارجاع bundle به mapping versionهای مربوط را enforce کند. ReportType catalog و جزئیات physical bundle هنوز باید در gateهای catalog/implementation طراحی شوند. هیچ کد، ORM، schema، migration، دیتابیس یا تستی تغییر نکرد/اجرا نشد.


## 17. بررسی Gate 1 — تعریف دقیق Interpretation Standard Bundle — 2026-11-18

### 17.1 مرزبندی نسخه‌ها
- `TemplateVersion` فقط ساختار فیزیکی workbook را مشخص می‌کند: worksheet، table/sub-table، Header ranges/bindings، ColumnSlot و extraction spans.
- `InterpretationStandardVersion` معنای مالی ساختار را مشخص می‌کند؛ یعنی قواعدی که مشاهدهٔ row/column را به Metric، Dimension، FinancialPeriod، temporal basis، unit/measurement basis و value state تبدیل می‌کنند.
- نسخهٔ Reader/adapter، profile اجرا، DTO schema و پردازش عملیاتی متعلق به `IngestionRun`/operational provenance هستند؛ نباید با نسخهٔ معنایی استاندارد یکی شوند.
- source fingerprint، CODAL source revision و publication metadata در ReportVersion/source identity قرار می‌گیرند؛ بخشی از Interpretation Standard نیستند.
- FinancialMetric identity کاتالوگ پایدار است؛ استاندارد به Metricهای مصوب ارجاع می‌دهد و نباید تعریف Metric را در خود کپی یا بی‌صدا بازنویسی کند.

### 17.2 اجزای الزامی Interpretation Standard Bundle
یک Bundle نسخه‌دار باید اجزای زیر را به‌صورت immutable یا با reference نسخه‌دار در بر بگیرد:
1. **Scope:** دامنهٔ report family/type و Industry شرکت، با اتصال به TemplateVersion دقیق؛ شرکت در V1 یک Industry دارد.
2. **Semantic mapping rules:** نگاشت کامل row-axis path + Header path + layout node/ColumnSlot به Metric و Dimensionهای مصوب؛ یک mapping باید دقیقاً یک معنا داشته باشد.
3. **Temporal interpretation:** قواعد تبدیل Header/context به FinancialPeriod واقعی جلالی، temporal kind، نقش PRIMARY/COMPARATIVE/UNKNOWN و duration_basis برای Factهای DURATION؛ قواعد باید با DB-DES-003/011 همسو باشند و از عنوان گزارش/ترتیب ستون/شماره فصل به‌تنهایی دوره یا YTD حدس نزنند.
4. **Dimension interpretation:** شناسه و نسخهٔ scope/allowed values و قواعد استخراج Dimensionهایی که واقعاً هویت اقتصادی مقدار را تغییر می‌دهند؛ dimension catalog می‌تواند مستقل version شود اما Bundle باید نسخهٔ دقیق مورد استفاده را pin کند.
5. **Unit and measurement semantics:** قواعد تشخیص/اعتبارسنجی source unit، currency، scale و measurement basis و هر تبدیل صریحاً مجاز؛ تبدیل ضمنی یا rescaling مجاز نیست.
6. **Value-state rules:** قواعد تشخیص REPORTED_VALUE، REPORTED_NULL و ZERO_FALLBACK و سیاست blank/zero مختص template/report family؛ ZERO_FALLBACK فقط در دامنهٔ استثنای مصوب قابل استفاده است.
7. **Controlled source-label/header aliases:** aliasها و نرمال‌سازی‌های معنایی مصوب، با scope و نسخه؛ تطبیق fuzzy یا انتقال خودکار دیکشنری یک صنعت به صنعت دیگر ممنوع است.
8. **Approval/immutability metadata:** شناسه، شماره نسخه، وضعیت DRAFT/APPROVED/RETIRED، زمان/مرجع تأیید و تاریخچهٔ نسخه‌ها؛ Bundle مورد استفادهٔ Factهای پذیرفته‌شده نباید ویرایش درجا شود.

Bundle باید مجموعه‌ای از rule/version referenceها باشد، نه یک سند متنی یا یک نسخهٔ واحد برای تمام mappingهای مستقل. چندین SemanticMappingRule و چند catalog version می‌توانند درون یک InterpretationStandardVersion بسته‌بندی شوند؛ ReportVersion همچنان فقط یک Bundle را reference می‌کند.

### 17.3 Scope و هویت فیزیکی پیشنهادی
با توجه به اینکه Template در DB-DES-008 در scope یک Company + ReportType تعریف می‌شود و هر TemplateVersion تمام layout همان workbook را پوشش می‌دهد، پیشنهاد می‌شود InterpretationStandardVersion به **یک TemplateVersion دقیق** مقید باشد:
- هویت نسخه: `interpretation_standard_version_id` به‌عنوان PK و `version_number` در scope همان `template_version_id`.
- قید یکتا: `(template_version_id, version_number)`.
- Bundle شامل mapping/rule versionهای سازگار با همان TemplateVersion است.
- ReportVersion هم `template_version_id` و هم `interpretation_standard_version_id` را نگه می‌دارد؛ composite FK یا trigger باید ثابت کند TemplateVersion ارجاع‌شده توسط Bundle دقیقاً همان TemplateVersion متصل به ReportVersion است.
- Company، Industry و ReportType از زنجیرهٔ TemplateVersion → Template → Company/ReportType قابل اعتبارسنجی‌اند؛ از تکرار بی‌دلیل این scope fields در هر Fact پرهیز شود.
- تغییر layout، TemplateVersion جدید می‌سازد و Bundle سازگار جدید لازم دارد. تغییر معنای mapping/temporal/unit/value/alias بدون تغییر layout نیز InterpretationStandardVersion جدید می‌سازد.

### 17.4 Scope خاص دیکشنری‌ها
سند معماری، Header dictionary فعلی را فقط برای periodic reports صنعت بانک تأیید کرده است. این دیکشنری به‌تنهایی جایگزین Metric-level semantic mapping نیست و نباید به شرکت‌ها/صنایع دیگر تعمیم یابد. Bundle هر Template فقط ruleها و aliasهایی را می‌تواند فعال کند که برای همان Industry + ReportType و شواهد همان Template تأیید شده‌اند.

### 17.5 نتیجه Gate 1
**تصمیم طراحی:** InterpretationStandardVersion یک immutable bundle متصل به یک TemplateVersion است که semantic mapping، temporal interpretation، dimension references، unit/value-state rules و alias/normalization references را با نسخهٔ دقیق pin می‌کند. Reader/adapter version و source revision از آن جدا می‌مانند.

این تعریف، محتوای منطقی Bundle و scope آن را مشخص می‌کند؛ طراحی relational جزئی جدول‌های component/reference، workflow تأیید و قیدهای سازگاری ReportVersion هنوز باید در physical schema نهایی شود.

**وضعیت Gate 1:** در سطح logical definition بسته شد؛ physical catalog/bundle schema و approval workflow باز هستند. هیچ کد، ORM، schema، migration، دیتابیس یا تستی تغییر نکرد/اجرا نشد.


## 18. بررسی Gate 2 — Scope و Versioning کاتالوگ Dimension — 2026-11-18

### 18.1 مرز مفهومی Dimension
- Dimension فقط وقتی ثبت می‌شود که یک محور مصوب، هویت اقتصادی یک observation را از observation دیگر جدا کند؛ مانند محصول/گروه محصول یا نوع مشتری/سپرده، در صورتی که در استاندارد همان گزارش تأیید شده باشد.
- عنوان ردیف، نام جدول، نام worksheet، ستون، واحد، ارز، دوره، temporal basis و report type به‌طور خودکار Dimension نیستند. این‌ها به‌ترتیب ممکن است ساختار، Metric، unit/currency، period یا metadata باشند.
- اگر دو ردیف به دو Metric مستقل تعلق دارند، نباید صرفاً برای جا دادن آن‌ها در یک Metric به Dimension تبدیل شوند. اگر یک Metric واحد برای چند گروه اقتصادی گزارش شده، Dimension فقط با mapping مصوب ایجاد می‌شود.
- Dimension نباید برای پنهان کردن تکرار مبهم یا حل collision ناشی از mapping ناقص ساخته شود.

### 18.2 تصمیم دربارهٔ Scope
**تعریف Dimension به‌صورت کاتالوگ مشترک و global نگهداری شود؛ کاربرد و دامنهٔ مجاز آن در InterpretationStandardVersion تعیین شود.**
- یک Dimension code جهانی و پایدار دارد، اما global بودن شناسه به معنی قابل‌استفاده بودن آن در همهٔ صنایع/گزارش‌ها نیست.
- هر Interpretation Bundle تعیین می‌کند کدام Dimension برای کدام report family، table/node، Metric و context قابل استفاده است و کدام memberها مجازند.
- Dimension concept فقط زمانی بین صنایع مشترک است که معنای اقتصادی آن واقعاً یکسان باشد. اصطلاحات کلی و مبهم مانند SEGMENT نباید بدون تعریف دقیق مشترک استفاده شوند؛ در صورت تفاوت معنا، Dimension codeهای مستقل تعریف شوند.
- Dimension value/member نیز شناسهٔ پایدار global دارد. Memberهای مشترک با معنای یکسان می‌توانند در چند Bundle reuse شوند؛ memberهای company/industry/report-family-specific با شناسهٔ مستقل ساخته می‌شوند و فقط از طریق Bundleهای مجاز قابل استفاده‌اند. از scope polymorphic و مبهم روی خود Fact پرهیز می‌شود.
- نیاز نیست از ابتدا Dimensionها یا valueهای همهٔ صنایع/شرکت‌ها ساخته شوند؛ کاتالوگ به‌صورت incremental و فقط بر اساس شواهد workbook و نیاز استاندارد توسعه می‌یابد.

### 18.3 هویت و Versioning
1. `dimension_code` و هویت معنایی Dimension پس از approval immutable هستند؛ تغییر واقعی مفهوم، Dimension جدید می‌خواهد.
2. هر member با `dimension_id + stable value_code` هویت می‌گیرد؛ تغییر معنای اقتصادی member، member جدید می‌خواهد، نه ویرایش درجا یا reuse کد قدیمی.
3. تغییر صرف display label یا alias می‌تواند در نسخهٔ جدید InterpretationStandard/alias mapping ثبت شود؛ label متنی به‌تنهایی هویت member نیست.
4. retired member حذف نمی‌شود و ID آن reuse نمی‌شود. Bundleهای تاریخی همچنان می‌توانند آن را reference کنند؛ Bundle جدید استفاده از آن را فقط در صورت مجاز بودن صریح ادامه می‌دهد.
5. تغییر allowed-value scope، alias، normalization یا ruleهای applicability باید در InterpretationStandardVersion جدید pin شود؛ این تغییر نباید معنی Facts پذیرفته‌شدهٔ قبلی را بازنویسی کند.
6. DimensionSet با ترکیب canonical و مرتب‌شدهٔ member identityها ساخته می‌شود؛ display text، ترتیب ورود یا worksheet coordinate در canonical key دخالت ندارند. برای Fact بدون Dimension یک empty set یکتا استفاده می‌شود.
7. در V1، هر Dimension در یک DimensionSet حداکثر یک member دارد، مگر اینکه یک استاندارد مشخص و مصوب خلاف آن را لازم بداند؛ member تکراری برای یک Dimension در یک set رد می‌شود.

### 18.4 قیدهای کاربرد و عدم‌تداخل
- Interpretation Bundle باید مشخص کند Dimension روی چه Metricها و contextهایی قابل استفاده است؛ صرف وجود Dimension در global catalog مجوز استفاده نیست.
- اگر یک مقدار بدون Dimension و با Dimensionهای مختلف گزارش شده، این دو observation فقط وقتی جداگانه پذیرفته می‌شوند که ساختار و استاندارد آن تمایز اقتصادی را اثبات کنند.
- Dimension برای تفکیک comparative/current period، YTD/standalone، source version، audit/restatement، unit/currency یا table position استفاده نمی‌شود؛ این‌ها هویت/ویژگی‌های مستقل خود را دارند.
- اگر یک Dimension یا member هنوز تعریف/تأیید نشده باشد، سیستم نباید آن را از متن مشابه حدس بزند یا به OTHER_* تبدیل کند؛ ورودی in-scope مبهم رد/قرنطینه می‌شود.

### 18.5 نتیجه Gate 2
**تصمیم طراحی:** Dimension definitions و member identities کاتالوگ global و پایدار دارند؛ scope کاربرد و allowed values در InterpretationStandardVersion محدود و نسخه‌دار می‌شود. Memberهای مختص شرکت/صنعت/خانوادهٔ گزارش شناسهٔ مستقل می‌گیرند و فقط از Bundleهای مجاز قابل دسترسی‌اند. بازنشستگی به معنی حذف نیست و تغییر معنا نیازمند identity جدید است.

Physical schema دقیق scope/allowed-value relations، approval workflow و canonical DimensionSet serialization هنوز باید طراحی شود. هیچ catalog یا Dimension واقعی از روی نمونه‌های ناقص فعلی به‌صورت production ساخته نمی‌شود.

**وضعیت Gate 2:** در سطح logical scope/versioning بسته شد؛ physical schema و approval workflow باز هستند. هیچ کد، ORM، schema، migration، دیتابیس یا تستی تغییر نکرد/اجرا نشد.


## 19. تطبیق Gate 3 با تصمیم پذیرفته‌شدهٔ DB-DES-011 — Temporal Basis در سطح Fact — 2026-11-18

بازخوانی DB-DES-011 و DB-AUD-016 نشان می‌دهد مالکیت temporal basis قبلاً به‌صورت هماهنگ در Architecture V1.3، DB-DES-003، DB-DES-009، DB-DES-010 و DB-DES-011 حل شده است؛ این gate نباید دوباره به‌عنوان تصمیم باز مطرح شود.

**قاعدهٔ قطعی طراحی:**
- FinancialPeriod فقط هویت بازه/لحظهٔ واقعی را نگه می‌دارد: شرکت، INSTANT/DURATION و تاریخ‌های دقیق جلالی.
- `duration_basis` متعلق به هر FinancialFact از نوع DURATION است و در موارد قابل‌اعمال باید صریحاً `YTD` یا `STANDALONE` باشد.
- برای INSTANT، duration_basis برابر NULL/NOT_APPLICABLE است؛ FALSE یا STANDALONE ساختگی ثبت نمی‌شود.
- YTD از ابتدای واقعی سال مالی شرکت تا پایان دوره است؛ سال مالی در دامنهٔ پروژه ۱۲ ماه متوالی دارد، اما ماه شروع آن نباید بدون مدرک به ماه ۱ فرض شود.
- Standalone فقط وقتی Fact منبع است که منبع آن را گزارش کرده باشد؛ تفاضل YTD برای ساخت standalone فقط محاسبهٔ runtime است و persist نمی‌شود.
- TTM دورهٔ منبع نیست و runtime-only باقی می‌ماند.
- Metric definition/binding باید temporal kindهای مجاز و basisهای مجاز/الزامی خود را مشخص کند. Stock با INSTANT و Flow با DURATION سازگار می‌شود؛ Rate/Ratio طبق معنای منبع تعیین می‌شود و default عمومی ندارد.
- دوره و basis نامشخص یا متعارض، پذیرش کل واحد ingestion را متوقف می‌کند؛ هیچ دوره یا YTD حدس زده نمی‌شود.

**باقی‌ماندهٔ فنی، نه ابهام مالکیت:**
1. physical schema باید قید کند duration_basis برای INSTANT فقط NULL و برای DURATIONهای نیازمند basis فقط YTD/STANDALONE باشد؛ applicability نهایی با Metric binding اعتبارسنجی شود.
2. `months_length` برای INSTANT صفر است؛ برای DURATION فقط طول دقیق ماه تقویمی ثبت می‌شود و در بازهٔ نامنظم می‌تواند NULL باشد، مشروط به شواهد V1 و پشتیبانی query.
3. منبع authoritative تاریخ شروع سال مالی هر شرکت و fiscal-calendar lifecycle باید از شواهد/تنظیمات مصوب تعیین شود. سال مالی ۱۲ ماهه است، اما start month ممکن است شرکت‌به‌شرکت متفاوت باشد.
4. نمونهٔ workbook دورهٔ بعد و adversarial tests در مرحلهٔ implementation لازم‌اند؛ این سند ادعای اجرای آن‌ها را ندارد.

**نتیجه Gate 3:** مالکیت fact-level `duration_basis` قبلاً ACCEPTED و اسناد هماهنگ شده‌اند؛ Gate 3 در سطح logical ownership بسته است. physical constraints، metric applicability، fiscal-calendar evidence و تست‌ها همچنان implementation gates هستند. هیچ کد، ORM، schema، migration، دیتابیس یا تستی تغییر نکرد/اجرا نشد.


## 20. بررسی Gate 4 — CODAL Source Revision Identity — 2026-11-18

### 20.1 شواهد واقعی کد فعلی
- `Report` فعلی `codal_tracking_id` و `source_url` دارد؛ اولی در سطح Report unique است.
- `ReportVersion` فعلی `publication_datetime`، `version_number`، `is_restated` و `supersedes_version_id` دارد، اما source-issued revision key و source content fingerprint ندارد.
- writer فعلی CODAL برای replay نسخه از `(codal_tracking_id, publication_datetime)` استفاده می‌کند. این قرارداد legacy است و تست موجود نسخه‌های دارای publication_datetime متفاوت را نشان می‌دهد؛ اما منبع metadata مستقل برای revision را اثبات نمی‌کند و payload متعارض با همان identity را نیز guard نمی‌کند.
- `AcquiredSource` در مسیر PDF دارای `source_url`، `codal_tracking_id`، `content_sha256` و `source_identity` است. در local acquisition، source_identity مسیر فایل است و در URL acquisition، URL؛ هیچ‌یک به‌تنهایی source-issued revision identity نیست. Hash فعلاً فقط در acquisition محاسبه می‌شود و به ReportVersion persist نمی‌شود.
- `CodalExtractionResult`، `codal_tracking_id` و `publication_datetime` را به‌عنوان پارامتر ورودی دریافت/منتقل می‌کند؛ در این مسیر استخراج‌شده از metadata رسمی CODAL به‌صورت مستقل اثبات نشده‌اند.
- Excel `SourceArtifactObservation` فعلی `source_ref`، `file_name`، `format`، `sha256` و `byte_length` را مشاهده می‌کند؛ اما CODAL letter/revision identity و source publication datetime در آن وجود ندارد. Reader فعلی read-only است و این داده‌ها را از API CODAL resolve نمی‌کند.

### 20.2 تفکیک سه هویت
1. **Report identity:** هویت پایدار جریان گزارش شرکت/ReportType؛ CODAL tracking identifier می‌تواند بخشی از آن باشد، مشروط بر تأیید معنای واقعی فیلد در منبع.
2. **ReportVersion/source revision identity:** شناسهٔ یک انتشار یا اصلاح مشخص از همان Report که باید از metadata رسمی منبع یا composite key اثبات‌شده به‌دست آید.
3. **Source artifact fingerprint:** SHA-256 و byte length برای تشخیص یکسان/متفاوت بودن bytes فایل؛ fingerprint ابزار integrity/replay conflict است، نه جایگزین source revision identity.

Filename، local path، download URL، ingestion timestamp یا SHA-256 به‌تنهایی source revision key نیستند. publication datetime نیز باید زمان انتشار منبع باشد، نه زمان دانلود/پردازش.

### 20.3 قرارداد پذیرش پیشنهادی
- اگر CODAL یک شناسهٔ رسمی و پایدار برای letter/revision منتشر می‌کند، همان شناسه با scope مناسب در ReportVersion ذخیره شود؛ نام فیلد منبع تا زمان مشاهدهٔ payload واقعی قطعی نشود.
- اگر منبع شناسهٔ revision مستقل ندارد، فقط پس از بررسی payload واقعی و اثبات یکتایی/معنای آن می‌توان composite key مانند `(codal_tracking_id, source_publication_datetime)` را پذیرفت. این fallback هنوز برای مسیر Excel تأیید نشده است.
- یک ReportVersion پذیرفته‌شده باید source revision key و artifact fingerprint را با هم نگه دارد.
- همان source revision key + همان fingerprint = replay بدون تغییر.
- همان source revision key + fingerprint متفاوت = hard conflict/quarantine؛ نه overwrite و نه ساخت نسخهٔ جدید بدون شواهد اینکه منبع واقعاً revision جدیدی منتشر کرده است.
- source revision key جدید و معتبر = ReportVersion جدید؛ نسخهٔ قبلی و facts/provenance آن حفظ می‌شوند.
- اگر source identity یا source publication datetime لازم ناموجود/مبهم باشد، ingestion باید fail closed کند؛ از hash یا زمان ingestion برای پر کردن آن استفاده نشود.

### 20.4 شکاف شواهد و اقدام لازم
در repository فعلی، CODAL API response/metadata contract برای Excel acquisition وجود ندارد؛ مسیر acquisition بررسی‌شده PDF-only است و Excel Reader فقط fingerprint فایل را می‌گیرد. بنابراین هنوز نمی‌توان نام فیلدهای واقعی CODAL، scope یکتایی آن‌ها یا رفتارشان در correction/restatement را تعیین کرد.

برای بستن این gate باید metadata واقعی یک یا چند گزارش Excel از CODAL (یا پاسخ رسمی endpoint/download manifest که فایل از آن دریافت می‌شود) بررسی شود؛ حداقل یک گزارش اصلی و یک نسخهٔ اصلاحی/بازانتشارشده لازم است تا تفاوت Report identity، revision identity، publication time و file fingerprint قابل مشاهده باشد. اگر نمونهٔ اصلاحی در دسترس نیست، gate تا دریافت شواهد باز می‌ماند.

**نتیجه Gate 4:** قرارداد منطقی تفکیک Report identity، source revision identity و artifact fingerprint تعیین شد؛ اما source-issued key و metadata واقعی مسیر Excel هنوز اثبات نشده است. Gate 4 **OPEN / EVIDENCE BLOCKED** است. هیچ کد، ORM، schema، migration، دیتابیس یا تستی تغییر نکرد/اجرا نشد.


## 21. تطبیق Gateهای 9 و 10 با ممیزی‌های تکمیل‌شده — 2026-11-18

### Gate 9 — Normalized/Derived consumer inventory
این gate قبلاً در DB-AUD-014 / Master §8.50 انجام شده است:
- تنها reader مستقیم runtime/production برای `NormalizedFinancialFact`، Stage 5 از طریق `src/forecast/queries.py` است.
- writer تولیدی برای `NormalizedFinancialFact` در branch بررسی‌شده پیدا نشد؛ CODAL فعلی فقط RawFinancialFact می‌نویسد و Excel canonical writer هنوز وجود ندارد.
- `NormalizedFinancialFactInput` و جدول‌های Derived reader/writer تولیدی ندارند؛ صرفاً مدل/metadata/migration و تست‌های legacy به آن‌ها ارجاع می‌دهند.
- Stage 5 consumer و تست‌های مربوط نباید به‌علت خالی بودن DB حذف شوند؛ در انتقال آینده باید PIT، ReportVersion selection، Dimension، provenance و رفتار عددی حفظ شود.
- DB-AUD-015 / Master §8.52 ممیزی دیتابیس محلی را تکمیل کرد: چهار جدول Normalized/Derived در snapshot محلی صفر ردیف داشتند؛ linkage/reference و duplicate groups بررسی‌شده صفر و foreign_key_check بدون violation بود؛ 505 RawFinancialFact حفظ شدند.

**نتیجه Gate 9:** source consumer inventory برای branch بررسی‌شده COMPLETE و local snapshot linkage COMPLETE است. وضعیت محیط‌های دیگر، backupها و consumerهای خارجی اثبات نشده است. این gate مانع طراحی additive مقصد جدید نیست، اما حذف legacy tables یا مهاجرت destructive را مجاز نمی‌کند.

### Gate 10 — Migration 9 lineage reconciliation
این gate با DB-AUD-010 و Master §8.64 فقط تا حد آثار قابل‌مشاهدهٔ دیتابیس محلی پیش رفته است:
- implementation اصلی Migration 9 در repository/runner پیدا نشد؛ runner فعلی تا Migration 8 است.
- آثار قابل‌مشاهدهٔ local DB cleanup شد: دو ستون اضافه و ledger row نسخه 9 حذف شدند، 505 RawFinancialFact حفظ شدند و audit پس از cleanup موفق بود.
- backup محلی قبل از cleanup در مسیر ثبت‌شدهٔ Master §8.64 نگهداری شده است.
- چون source implementation و provenance تاریخی Migration 9 در دسترس نیست، side effectهای تاریخی ناشناخته قابل نفی نیستند.

**نتیجه Gate 10:** local visible-state reconciliation COMPLETE؛ historical source/side-effect reconciliation و target-environment/backup verification همچنان PARTIAL / OPEN هستند. Migration 9 جایگزین ساخته نمی‌شود و برای ادامهٔ کار، دوباره‌سازی migration یا تکرار cleanup محلی لازم نیست.

**اثر بر DB-DES-009:** additive design و توسعهٔ جدول جدید `financial_facts` می‌تواند در سطح طراحی ادامه یابد؛ هیچ حذف/بازنویسی legacy، backfill خودکار یا migration مخرب تا زمان مجوز مستقل و audit محیط مقصد مجاز نیست. هیچ کد، ORM، schema، migration، دیتابیس یا تستی تغییر نکرد/اجرا نشد.


## 22. تکمیل پیشنهاد فیزیکی Row-Axis برای بستن Gate 7 — 2026-11-18

### 22.1 شکاف ساختاری
- DB-DES-008 ساختار Template را برای layout node، Header binding، ColumnSlot و extraction span تعریف می‌کند؛ اما entity فیزیکی متناظری برای سلسله‌مراتب row-axis ندارد.
- DB-DES-014 برای هر semantic mapping، row-axis path کامل و ordered Header path را لازم می‌داند؛ mapping در تقاطع این دو محور resolve می‌شود.
- DTO فعلی Excel، `RowObservation` را با `row_index`، `label_fragments`، `parent_row_index` و `outline_level` ثبت می‌کند. این داده برای ساخت observation موقت کافی است، ولی row-axis identity پایدار تولید نمی‌کند؛ Reader نباید مسئول mapping معنایی باشد.

### 22.2 پیشنهاد حداقلی مدل فیزیکی
**الف) `template_row_axis_node`**
- `row_axis_node_id` PK
- `template_version_id` و `layout_node_id` برای scope دقیق
- `parent_row_axis_node_id` self-FK برای حفظ سلسله‌مراتب
- `node_code` پایدار در همان layout node
- `node_kind`: SECTION / SUBSECTION / LEAF (controlled)
- `order_index`
- locatorهای اختیاری نمونه، مانند worksheet و source row range؛ فقط برای تطبیق Template، نه هویت Fact

قیدها:
- node باید به یک TemplateVersion و layout node تعلق داشته باشد.
- parent باید در همان TemplateVersion و همان layout node باشد؛ parent cycle ممنوع است.
- node_code در scope layout node یکتا باشد.
- leaf node هویت کامل row-axis path را از طریق زنجیرهٔ parentها نشان می‌دهد؛ تکرار leaf label زیر دو parent متفاوت، دو identity متفاوت خواهد داشت.
- متن خام تمام سلول‌های ردیف ذخیره نمی‌شود. تشخیص label و alias در لایهٔ versioned interpretation/row-label identity انجام می‌شود.

**ب) `semantic_mapping_rule`**
هر rule نسخه‌دار باید حداقل این references را داشته باشد:
- `interpretation_standard_version_id`
- `template_version_id`
- `layout_node_id`
- `row_axis_node_id` (leaf/path identity)
- `column_slot_id` یا slot group مصوب
- `metric_id`
- referenceهای دقیق temporal, dimension, unit/value-semantics rules

قید یکتایی منطقی: یک تقاطع مشخص از InterpretationStandardVersion + row-axis path + ColumnSlot در یک layout node باید حداکثر یک mapping مصوب داشته باشد. صفر mapping یا بیش از یک mapping، شرط reject است. composite FK/trigger باید ثابت کند row node و column slot هر دو متعلق به همان node و TemplateVersion هستند که استاندارد به آن مقید است.

**ج) `financial_fact_provenance`**
پس از تعریف SemanticMappingRule دقیق، `semantic_mapping_rule_id` باید به یک rule مشخص اشاره کند، نه صرفاً به یک نسخهٔ کلی از mapping catalog. در این صورت node/row path/column slot از همان rule قابل بازیابی‌اند و ذخیرهٔ تکراری آن‌ها روی هر provenance row ضروری نیست. ساختار حداقلی پیشنهادی:
- `provenance_id`
- `fact_id`
- `input_role`
- `semantic_mapping_rule_id`
- `source_locator` اختیاری و diagnostic-only

هر ورودی مستقل یک provenance row دارد؛ direct معمولاً یک row و multi-input چند row با roleهای مصوب. اگر در شواهد واقعی چند ورودی متمایز بتوانند به یک mapping rule و یک role یکسان برسند، قبل از implementation باید identity تکمیلی آن ورودی‌ها مشخص شود؛ مختصات سلول به‌صورت پیش‌فرض کلید دائمی نمی‌شود.

### 22.3 قواعد تغییر نسخه و تطبیق
- row-axis nodes بخشی از TemplateVersion immutable هستند. تغییر ساختار، ترتیب یا ancestry ردیف‌ها TemplateVersion جدید می‌خواهد.
- تغییر alias/معنای row label بدون تغییر layout، InterpretationStandardVersion جدید می‌خواهد.
- هر semantic mapping به دقیقاً یک row path و یک column slot/path کامل محدود می‌شود؛ matching صرفاً با متن leaf label کافی نیست.
- row_index/CellRef در WorkbookObservation locator موقت است. در Fact یا Provenance اجباری ذخیره نمی‌شود.
- Header inheritance و extraction-span ownership طبق DB-DES-008 بدون تغییر باقی می‌ماند؛ row-axis hierarchy نیز نباید extraction permission ایجاد کند.
- برای header/row path ناشناخته، duplicate مبهم یا mapping چندگانه، کل واحد ingestion رد می‌شود.

### 22.4 محدودیت شواهد و وضعیت
این مدل physical proposal است، نه ORM authorization. Parsian annotation map فعلی هنوز candidate/provisional است؛ تمام table bounds و row-axis paths production-approved نیستند و workbook مستقل دورهٔ بعد برای drift validation در دسترس این بررسی نبود. پیش از تصویب physical schema باید حداقل یک table با row-axis کامل از دو workbook مستقل، یک direct fact و یک multi-input fact، بدون تکیه بر cell coordinate دائمی، end-to-end مدل‌سازی شود.

**نتیجه Gate 7:** پیشنهاد physical row-axis و semantic intersection اکنون مشخص‌تر شده است؛ اما تا زمان evidence validation و تکمیل مثال‌های direct/multi-input، Gate 7 همچنان **PARTIAL / OPEN** است. هیچ کد، ORM، schema، migration، دیتابیس یا تستی تغییر نکرد/اجرا نشد.


## 23. تکمیل شواهد عمومی CODAL برای Gate 4 و ریسک هویت Report — 2026-11-18

### 23.1 شواهد فنی بیرونی (غیررسمی)
دو مرجع فنی عمومی که ساختار Search API کدال را reverse-engineer کرده‌اند، این فیلدها را در نتیجهٔ جست‌وجوی هر filing نشان می‌دهند:
- `TracingNo`: شناسهٔ عددی یکتای filing.
- `Url`: شامل `LetterSerial`.
- `LetterSerial`: شناسهٔ opaque یکتای هر letter و کلید دسترسی به صفحه و فایل Excel/PDF.
- `PublishDateTime` و `SentDateTime`: metadata زمانی منبع.
- `Title`، `LetterCode`، `HasExcel` و `ExcelUrl`: metadata و دسترسی به artifact.

منابع فنی (غیررسمی و نه قرارداد رسمی منتشرشده از CODAL):
- `https://github.com/amirziveh/codal-skill/blob/master/SKILL.md` — بخش‌های LetterSerial، TracingNo و Letter Response Schema.
- `https://mohsenebrahimyir.github.io/codal-tsetmc/codal.html` — نمونهٔ خروجی Search API و فیلدهای TracingNo/PublishDateTime/Url/ExcelUrl.

این شواهد برای شناسایی candidate fieldها کافی است، اما جایگزین دریافت payload واقعی از endpoint و بررسی یک زوج گزارش اصلی/اصلاحی نیست.

### 23.2 اصلاح و دقیق‌سازی تصمیم source identity
- `LetterSerial` candidate قوی برای `source_revision_key` است، چون هر filing/letter را مشخص می‌کند و مستقیماً برای دریافت Excel استفاده می‌شود.
- `TracingNo` باید به‌عنوان source filing identifier عددی و cross-reference حفظ شود؛ در صورت اثبات one-to-one بودن با LetterSerial، هر دو در ReportVersion نگهداری و متقابلاً validate شوند.
- `PublishDateTime` زمان انتشار منبع است؛ `SentDateTime` نیز در صورت نیاز به‌عنوان metadata جدا حفظ شود. این دو نباید با ingestion timestamp جایگزین شوند.
- SHA-256 همچنان فقط artifact fingerprint است؛ LetterSerial/TracingNo را جایگزین نمی‌کند.
- اصلاحیه/بازانتشار باید با filing identity جدید و رابطهٔ نسخه‌ای/اصلاحی مناسب ثبت شود، اما اینکه CODAL برای correction دقیقاً چه فیلد یا رابطه‌ای منتشر می‌کند هنوز با نمونهٔ واقعی اثبات نشده است.

### 23.3 ریسک مهم در مدل فعلی Report
در ORM فعلی، `Report.codal_tracking_id` unique است و در writer legacy به‌عنوان شناسهٔ پایدار Report برای grouping چند ReportVersion استفاده می‌شود. اما اگر این فیلد در ورودی واقعی همان `TracingNo` باشد، چون TracingNo طبق شواهد فنی برای هر filing یکتا است، دیگر نمی‌تواند شناسهٔ پایدار یک Report stream باشد؛ هر filing جدید ممکن است Report جدا بسازد و version grouping از دست برود.

بنابراین پیش از هر تغییر schema باید semantics دقیق `codal_tracking_id` فعلی روشن شود:
- آیا واقعاً TracingNo یک filing است؟
- آیا یک شناسهٔ دیگری برای Report stream وجود دارد؟
- CODAL چگونه filing اصلاحی را به filing قبلی مرتبط می‌کند؟
- اگر شناسهٔ stream رسمی وجود ندارد، تعریف Report identity باید جداگانه و بر اساس شواهد شرکت/ReportType/period/نوع صورت/تلفیقی-غیرتلفیقی و رابطهٔ اصلاحیه طراحی شود؛ هیچ composite key حدسی در این مرحله پذیرفته نیست.

**نتیجه به‌روزشده Gate 4:** فیلدهای source filing candidate شناسایی شدند و `LetterSerial` به‌عنوان candidate اصلی source revision key توصیه می‌شود؛ اما زوج واقعی original/correction و semantics فعلی `codal_tracking_id` هنوز بررسی نشده‌اند. Gate 4 از EVIDENCE BLOCKED به **PARTIAL / SOURCE-FIELD CANDIDATES IDENTIFIED; REPORT-GROUPING UNVERIFIED** تغییر می‌کند. هیچ کد، ORM، schema، migration، دیتابیس یا تستی تغییر نکرد/اجرا نشد.


## 21. بازبینی تجمیعی آمادگی پیاده‌سازی Gateهای 7 و 8 — 2026-11-19

برای جلوگیری از بررسی تکراری و پراکنده، Gate 7 (Provenance) و Gate 8 (binding نسخهٔ گزارش) به‌صورت یک بسته بازبینی شدند؛ چون هر دو به هویت ساختاری/معنایی واحد ReportVersion وابسته‌اند.

### 21.1 شواهد اجرایی فعلی
- `src/ingestion/excel/reader.py` صریحاً Reader را read-only معرفی می‌کند: ساختار workbook و literal values را مشاهده می‌کند، financial semantics را تفسیر نمی‌کند و persistence ندارد.
- `src/ingestion/excel/dto.py` observationهای immutable شامل CellRef/CellRange، worksheet، Header fragments/axes، RowObservation، ColumnObservation و TableObservation را تعریف می‌کند. این DTOها source locator و ساختار مشاهده‌شده را حمل می‌کنند؛ stable TemplateVersion، row-axis semantic identity، SemanticMapping ID یا InterpretationStandardVersion تولید نمی‌کنند.
- `src/migrations/runner.py` مدل‌های فعلی Report/ReportVersion، Company/Industry، FinancialPeriod، FinancialMetric و مدل‌های legacy را import می‌کند؛ در inventory مدل‌های importشده، مدل‌های TemplateVersion، InterpretationStandardVersion، SemanticMapping یا FinancialFact جدید دیده نشد.
- مسیرهای شناخته‌شدهٔ `src/ingestion/excel` شامل Reader/DTO هستند؛ در مسیرهای مورد بررسی، Excel-to-canonical persistence حاضر نیست. این با DB-AUD-013 هم‌راستاست.
- تلاش برای بازیابی فایل‌های طراحی مرجع DB-DES-008 و DB-DES-014 از مسیرهای حدس‌زده‌شده در `database/reports/` به 404 رسید؛ بنابراین در این گام محتوای کامل آن دو سند مستقلاً بازخوانی نشد و برای آن‌ها فقط به خلاصه/تصمیم‌های ثبت‌شده در این سند و Master Packet تکیه شده است.

### 21.2 نتیجهٔ تجمیعی Gate 7
تصمیم منطقی قبلی پابرجاست: یک provenance row برای هر منبع ورودی مستقل؛ چند provenance row برای Fact چندمنبعی؛ ترکیب هویت ساختاری Template node/ColumnSlot با semantic mapping نسخه‌دار؛ cell coordinate فقط locator تشخیصی و نه هویت دائمی. بااین‌حال physical row-axis hierarchy، semantic mapping identity/versioning و uniqueness واقعی چند ورودی هنوز طراحی و با نمونهٔ واقعی direct + multi-input اثبات نشده است.

**Gate 7: PARTIAL / OPEN.** این مرحله نباید با ساختن یک جدول provenance ساده و اتصال به شناسهٔ mapping ناقص بسته شود. تا وقتی semantic mapping تمام row path و header path و context را immutable pin نکند، provenance قابل‌ممیزی نیست.

### 21.3 نتیجهٔ تجمیعی Gate 8
تصمیم منطقی قبلی پابرجاست: هر ReportVersion پذیرفته‌شده دقیقاً یک TemplateVersion و یک InterpretationStandardVersion دارد؛ bundle می‌تواند چند semantic mapping/version reference را در خود نگه دارد. Workbook چند worksheet/table/period یا Fact چندمنبعی، به‌تنهایی مجوز چند binding نیست. ورودی با چند report family ناسازگار باید پیش از پذیرش تفکیک یا reject/quarantine شود.

**Gate 8: CLOSED در سطح logical design؛ OPEN در physical implementation.** باید schema، NOT NULL، immutability، FK/composite-FK یا trigger سازگاری TemplateVersion داخل Interpretation bundle و bindingهای ReportVersion را enforce کند. Reprocessing با Template/Bundle جدید نباید نسخهٔ پذیرفته‌شده را درجا overwrite کند.

### 21.4 جمع‌بندی مرز Reader و persistence
Reader فعلی درست در مرز مشاهده متوقف می‌شود؛ این کمبود نیست و نباید با افزودن منطق معنایی/DB به Reader برطرف شود. مرحلهٔ بعد باید لایه‌های مستقل را طراحی کند: (1) Template matching/version resolution، (2) interpretation bundle و semantic mapping، (3) period/dimension/value validation، (4) canonical writer و provenance persistence. تا آن زمان DTOهای فعلی صرفاً observation باقی می‌مانند.

این بازبینی static/read-only بود. هیچ کد، ORM، schema، migration، دیتابیس یا داده‌ای تغییر نکرد و هیچ تستی اجرا نشد.


## 22. طرح فیزیکی یکپارچه برای Template، Interpretation، Dimension و Provenance — 2026-11-19

### 22.1 اصل طراحی و مرز مسئولیت‌ها
این طرح، Gateهای 1، 2، 7 و 8 را به یک زنجیرهٔ قابل enforce تبدیل می‌کند:

`ReportVersion → TemplateVersion → InterpretationStandardVersion → SemanticMapping → FinancialFact → FinancialFactProvenance`

- TemplateVersion فقط ساختار فیزیکی workbook را نسخه‌بندی می‌کند؛ worksheet/table/sub-table، مسیر سلسله‌مراتبی ردیف‌ها، مسیر Headerها و ColumnSlotها.
- InterpretationStandardVersion معنای مالی را نسخه‌بندی می‌کند؛ mapping دقیق row/header intersection به Metric، Dimension، دوره، temporal basis، unit/basis و value-state rules.
- Dimension catalog هویت مفاهیم و memberها را نگه می‌دارد؛ Bundle فقط دامنهٔ مجاز کاربرد آن‌ها را pin می‌کند.
- FinancialFact مقدار canonical را نگه می‌دارد؛ Provenance اتصال Fact به source structure و semantic mapping دقیق را نگه می‌دارد.
- Reader/DTO همچنان observation موقت است و نباید Template، Interpretation، Dimension یا Fact را خودش ایجاد/تأیید کند.

### 22.2 ساختار فیزیکی TemplateVersion و Row Axis
پیشنهاد می‌شود ساختار موجود DB-DES-008 با این الزامات تطبیق داده شود؛ نام جدول‌های زیر نام منطقی پیشنهادی‌اند و پیش از migration باید با نام‌گذاری نهایی DB-DES-008 reconcile شوند:

1. `templates`: هویت پایدار Template در scope Company + ReportType؛ قید UNIQUE روی این scope مطابق تصمیم DB-DES-008.
2. `template_versions`: نسخهٔ immutable با `template_version_id`, `template_id`, `version_number`, lifecycle/approval metadata؛ UNIQUE(`template_id`, `version_number`). هر نسخه تمام workbook layout را پوشش می‌دهد.
3. `template_layout_nodes`: درخت worksheet/table/sub-table و سایر containerهای ساختاری؛ هر node به یک TemplateVersion تعلق دارد و parent آن نیز باید در همان نسخه باشد. node identity باید stable داخل همان TemplateVersion باشد؛ cell coordinates فقط attributes/locators همان نسخه‌اند.
4. `template_row_axis_nodes` یا معادل آن: مسیر سلسله‌مراتبی row-axis را به‌صورت parent-child ذخیره کند؛ هر node به layout node/table و TemplateVersion دقیق متصل باشد. هویت معنایی یک ردیف باید از مسیر کامل root-to-leaf حاصل شود، نه فقط label نهایی یا row index.
5. `template_column_slots`: ستون معنایی/فیزیکی پایدار در scope layout node و TemplateVersion؛ هر slot می‌تواند به Header path ساختاریافته متصل باشد. شماره ستون و A1 coordinate فقط locator نسخه‌ای‌اند، نه هویت دائمی بین TemplateVersionها.
6. Header path باید component/levelهای ordered و parent relationship را حفظ کند؛ flatten کردن چندسطحی Header به یک رشتهٔ آزاد، semantic identity کافی نیست.

هر FK میان child structure و parent structure باید علاوه بر ID، TemplateVersion scope را نیز ثابت کند؛ در SQLite این کار با UNIQUE composite parent keys و composite FKs انجام شود، یا در مواردی که طراحی موجود مانع آن است، triggerهای محدود و صریح به‌همراه service validation.

### 22.3 Interpretation Bundle و Semantic Mapping
پیشنهاد می‌شود:

1. `interpretation_standard_versions`: شامل `interpretation_standard_version_id`, `template_version_id`, `version_number`, status، approval metadata و lifecycle؛ UNIQUE(`template_version_id`, `version_number`). Bundle به یک TemplateVersion دقیق مقید است.
2. یک کلید یکتای مرکب روی (`interpretation_standard_version_id`, `template_version_id`) در جدول Bundle ایجاد شود تا ReportVersion بتواند با composite FK ثابت کند Template متصل به آن دقیقاً همان Template داخل Bundle است.
3. `semantic_mapping_rules`: هر rule متعلق به یک InterpretationStandardVersion و به یک layout node، row-axis path دقیق، Header path/ColumnSlot دقیق و یک FinancialMetric متصل باشد. mapping باید دقیقاً یک تفسیر داشته باشد؛ چندمعنایی یا match صرفاً fuzzy در پذیرش ممنوع است.
4. هر mapping علاوه بر Metric باید به ruleهای نسخه‌دار period/temporal، Dimension assignment، unit/measurement basis و value-state دسترسی مشخص داشته باشد؛ این اجزا می‌توانند child tables یا versioned rule references باشند، اما نباید در JSON آزاد و غیرقابل‌اعتبارسنجی پنهان شوند.
5. `report_versions` برای ورودی‌های Excel پذیرفته‌شده هر دو `template_version_id` و `interpretation_standard_version_id` را NOT NULL نگه دارد. FK مرکب ReportVersion به Bundle باید برابری TemplateVersion را enforce کند. رکوردهای تاریخی legacy می‌توانند طی دورهٔ گذار NULL بمانند؛ این استثنا برای ورودی جدید Excel مجاز نیست.
6. Bundle و mappingهای استفاده‌شده immutable باشند. تغییر layout، TemplateVersion جدید و Bundle سازگار می‌خواهد؛ تغییر صرف معنا/period/unit/value rule بدون تغییر layout، Bundle جدید می‌خواهد. بازپردازش نباید binding نسخهٔ پذیرفته‌شده را درجا عوض کند.

### 22.4 Dimension Catalog و مجازبودن در Bundle
ساختار relational پیشنهادی:

- `financial_dimensions`: Dimension identity global با `dimension_code` یکتا و تعریف معنایی immutable.
- `financial_dimension_values`: memberهای پایدار هر Dimension؛ علاوه بر PK، UNIQUE(`dimension_value_id`, `dimension_id`) برای enforce کردن تعلق value به Dimension.
- `interpretation_dimension_rules`: اتصال Bundle به Dimensionهای مجاز، با scope کاربرد مثل Metric و layout/mapping context در صورت نیاز واقعی؛ global بودن catalog به معنی مجازبودن عمومی نیست.
- `interpretation_dimension_allowed_values`: در صورت محدودیت memberها، allowed valueها را به rule/Bundle متصل کند و با composite FK ثابت کند value متعلق به همان Dimension است.
- `financial_dimension_sets`: یک parent canonical با `canonical_key` یکتا؛ empty set با کلید canonical `[]` برای Factهای بدون Dimension.
- `financial_dimension_set_members`: هر ردیف شامل dimension_set_id، dimension_id و dimension_value_id؛ UNIQUE(`dimension_set_id`, `dimension_id`) تا هر Dimension حداکثر یک member در هر set داشته باشد؛ composite FK به (`dimension_value_id`, `dimension_id`) برای جلوگیری از اتصال value به Dimension اشتباه.

Canonical key فقط از codeهای مصوب و به ترتیب قطعی ساخته شود؛ display label، ترتیب ورود و مختصات سلول در آن دخالت نکنند. اعتبارسنجی سرویس باید ثابت کند members دقیقاً canonical_key را بازتولید می‌کنند و هر member برای همان Bundle مجاز است. Dimension/member جدید هنگام ingestion و از روی متن خام ساخته نمی‌شود.

### 22.5 اتصال Fact و Provenance و کلیدهای یکتا
- Fact فقط به ReportVersion، FinancialPeriod، FinancialMetric و DimensionSet متصل می‌شود؛ company_id تکراری نمی‌شود.
- هویت Fact طبق تصمیم بخش 6.4 برابر (`report_version_id`, `period_id`, `metric_id`, `dimension_set_id`) باقی می‌ماند. Scenario یا هر تمایز value-defining دیگر باید به‌صورت Dimension مصوب وارد DimensionSet شود؛ افزودن ستون آزاد scenario به‌تنهایی مجاز نیست مگر کلید یکتا و قرارداد معنایی هم‌زمان بازطراحی شود.
- هر Provenance row به یک Fact، یک Template layout node، یک ColumnSlot در صورت کاربرد، و یک SemanticMapping دقیق وصل می‌شود. Composite FK/trigger باید ثابت کند همهٔ این ارجاع‌ها از همان TemplateVersion و InterpretationStandardVersion متصل به ReportVersion هستند.
- UNIQUE provenance پیشنهادی: (`fact_id`, `template_node_id`, `column_slot_id`, `semantic_mapping_id`, `input_role`)؛ nullable slot نباید uniqueness را در SQLite تضعیف کند. برای موارد بدون slot باید identity صریح/جایگزین یا partial unique indexهای مجزا طراحی شود؛ اتکا به UNIQUE مرکب شامل NULL کافی نیست.
- Fact مستقیم یک provenance با DIRECT دارد؛ Fact چندمنبعی چند provenance با roleهای مصوب دارد. اگر دو observation مستقل با همین structural identity و role ممکن باشند، مدل باید یک source-observation identity نسخه‌دار اضافه کند؛ مختصات سلول نباید بدون اثبات به کلید دائمی تبدیل شود.
- هر Fact پذیرفته‌شده حداقل یک provenance معتبر دارد. این قید cross-table با service validation و در صورت نیاز trigger/transaction-level validation enforce می‌شود؛ CHECK سادهٔ همان جدول برای آن کافی نیست.

### 22.6 قواعد پذیرش و سناریوهای لازم برای اثبات
پیش از migration، حداقل دو fixture واقعی از workbookهای تأییدشده لازم است:

A. Direct fact: یک مقدار از یک row-axis path و یک Header/ColumnSlot به یک Metric/Period/DimensionSet نگاشت شود؛ زنجیرهٔ کامل ReportVersion تا Provenance بدون ambiguity قابل query باشد.

B. Multi-input fact: چند observation ساختاری متمایز با roleهای مشخص به یک Fact واحد وصل شوند؛ duplicate link رد شود و هر input مستقل حفظ شود.

همچنین adversarial cases باید شامل این موارد باشند: row label تکراری در دو table؛ Header مشابه با parent path متفاوت؛ slot یا row node از TemplateVersion دیگر؛ mapping از Bundle دیگر؛ Dimension value متعلق به Dimension اشتباه؛ member مجازنشده در Bundle؛ duplicate fact با payload متفاوت؛ provenance با slot NULL و duplicate؛ تغییر Template/Bundle پس از پذیرش؛ و ReportVersion با دو report family ناسازگار.

### 22.7 وضعیت و محدودیت
این طرح، recommendation فیزیکی برای طراحی بعدی است و هنوز باید با متن کامل DB-DES-008 و DB-DES-014 تطبیق داده شود. نسخه‌های کامل این دو سند در مسیرهای حدس‌زده‌شدهٔ قبلی repository قابل بازیابی نبودند؛ بنابراین هیچ نام جدول موجود یا جزئیات پیاده‌سازی آن اسناد را قطعی فرض نمی‌کنیم. همچنین fixtureهای واقعی direct و multi-input هنوز در این مرحله اجرا/اثبات نشده‌اند.

**نتیجه:** Gate 1/2/7/8 از نظر رابطه‌ها و integrity requirements به یک طرح منسجم رسیده‌اند، اما physical design هنوز PROPOSED / NOT IMPLEMENTATION-READY است تا (الف) DB-DES-008 و DB-DES-014 با این طرح reconcile شوند، (ب) دو fixture واقعی direct/multi-input تأیید شوند، و (ج) جزئیات SQLite composite FK/trigger و NULL uniqueness نهایی شوند. هیچ کد، ORM، schema، migration، دیتابیس یا تستی تغییر نکرد/اجرا نشد.



## 23. بازبینی طرح فیزیکی با شواهد واقعی parsian_periodic_report_3 — 2026-11-19

### 23.1 منبع شواهد و اصلاح مسیر بررسی
فایل اصلی parsian_periodic.xlsx برای این مرحله لازم نیست؛ گزارش database/reports/parsian_periodic_report_3.md مبنای شواهد ساختاری است. گزارش، workbook با SHA-256 برابر 69186f1ad2b0e481a3588f2731b7027b0a9d9a543d1ca17fd24fc71d8c5aca06 را توصیف می‌کند: دو worksheet، 0 formula، 101 merged range در Recovered_Sheet1 و 2 در Sheet1، و جزئیات cell/style/header/row/border. عنوان داخلی فایل گزارش عبارت «Independent Re-Audit Report 2» و نام فایل report_3 است؛ این اختلاف نام‌گذاری ثبت می‌شود و در این مرحله فرض نمی‌کنیم محتوای گزارش با گزارش دیگری یکسان یا متفاوت است.

### 23.2 نمونهٔ واقعی Direct Mapping: T01
T01 در Recovered_Sheet1!A10:D42 یک نمونهٔ قابل اتکای direct mapping در سطح ساختار است:
- عنوان جدول در A8 و دو ردیف بالاتر از مرز جدول قرار دارد؛ A10:A11 یک Header ادغام‌شدهٔ «شرح» است.
- Headerهای B10:B11 و D10:D11 دو سطحی‌اند: تاریخ/وضعیت گزارش در سطح بالایی و audit status در سطح پایینی. C10:C42 کاملاً Black و طبق قرارداد استخراج خارج از دامنه است.
- ردیف‌های A13:A31، A33:A34 و A36:A42 labelهای Yellow هستند؛ B و D در همین ردیف‌ها Gray و دارای مقدارند.
- Green markerهای A12، A32 و A35 سه row group مستقل می‌سازند؛ گزارش برای هر سه، بازهٔ روشن و پیوسته ارائه می‌کند.
- یک source coordinate مفهومی برای mapping، صرفاً «ستون B» یا «ردیف 13» نیست؛ باید این مسیر را تعیین کند: worksheet → candidate/table T01 → row-group marker A12 → row label A13 → column header path B10:B11 → value cell B13. مسیر D13 مستقل است و Header path خودش را دارد.
- E10:E11 و مقادیر E13:E42 خارج از border هستند. تا زمان تصمیم مالک، نباید به mapping جدول T01 اضافه شوند؛ حتی اگر از نظر مکانی شبیه درصد تغییر باشند.

این مثال، وجود ساختار لازم برای RowAxisPath و HeaderPath را اثبات می‌کند. مختصات دقیق A1 برای نسخهٔ Template می‌تواند locator باشد، ولی هویت معنایی پایدار باید از node/pathهای نسخه‌دار به دست آید.

### 23.3 نمونهٔ واقعی Row Axis چندسطحی: T03
T03 در Recovered_Sheet1!A79:C119 سه marker سبز دارد: A81 «دارایی‌ها»، A96 «حقوق مالکانه» و A108 «بدهی‌ها». دو گروه آخر clear هستند؛ گروه اول به‌دلیل A95 که Blue است و در span سبز اول قرار می‌گیرد ambiguous است. در نتیجه:
- RowAxisPath باید parent group و leaf row label را جداگانه نگه دارد؛ صرف ذخیرهٔ متن A82 یا row number کافی نیست.
- Header path B79:B80 و C79:C80 مستقل است. A79:A80 Header شرحِ merged است.
- A95:C95 یک Header آبی دوم داخل محدودهٔ border است؛ نقش آن هنوز از گزارش قطعی نیست. نباید آن را خودکار leaf row یا آغاز sub-table فرض کرد.
- ستون‌های D و E خارج از border هستند و داده دارند؛ ورودشان به T03 نیازمند تصمیم مالک است.

این مثال نشان می‌دهد Row Axis همیشه یک گروه marker + label ساده و بدون استثنا نیست؛ مدل باید nodeهای ساختاری و وضعیت unresolved/ambiguous را پشتیبانی کند، اما هیچ mapping مبهمی قابل approval/ingestion نیست.

### 23.4 نمونهٔ واقعی چندستونی و استثناهای ارزش
T04 در Recovered_Sheet1!A130:L165 دارای 12 ستون Header، ردیف‌های Black کامل A131:L151، marker سبز A152 و labelهای A153:A165 است. 143 سلول Gray دارد که 85 موردشان blank هستند. طبق rule 7 مالک که در گزارش نقل شده، blank Gray برابر numeric zero است، نه NULL. این تبدیل باید در Interpretation rule صریح و versioned باشد؛ از رنگ/blank بودن به‌تنهایی نباید یک قاعدهٔ عمومی خارج از قرارداد مالک استخراج کرد.

T06 در Recovered_Sheet1!A238:I253 چهار ستون Gray یعنی C/E/G/I و چهار ستون Black بین آن‌ها دارد؛ C248:C251 چهار Gray blank هستند و گزارش آن‌ها را با rule 7 صفر می‌داند. با این حال، معنای Headerها و ردیف‌های A243:A244 و داده‌های uncolored داخل جدول، در گزارش ابهام دارند. بنابراین T06 برای اثبات ساختار interleaved column slots مفید است، اما هنوز نمونهٔ مناسب برای SemanticMapping پذیرفته‌شده نیست.

### 23.5 آیا گزارش Multi-input Fact را اثبات می‌کند؟
خیر. گزارش نمونه‌های متعدد از یک ردیف با چند ستون مقداری و چند دوره/وضعیت را نشان می‌دهد؛ این‌ها در مدل فعلی به‌طور طبیعی observationهای جداگانه و در صورت تفاوت دوره یا وضعیت، Factهای جداگانه‌اند. گزارش هیچ محاسبه یا canonical fact واحدی را نشان نمی‌دهد که از دو یا چند input مستقل ترکیب شده باشد. بنابراین مثال واقعی Multi-input Fact هنوز نداریم و نباید چند ستون B/D یا C/E/G/I را به‌اشتباه multi-input یک Fact بنامیم.

تا زمان یافتن یک rule مالی واقعی که چند ورودی را برای ساخت یک Fact واحد مصرف کند، Provenance چندردیفی همچنان یک قابلیت طراحی‌شده است، نه یک رفتار اثبات‌شده توسط این workbook. Direct mapping اثبات شده؛ multi-input mapping نیازمند مثال و قاعدهٔ مستقل است.

### 23.6 اثر بر physical model
1. RowAxis باید درختی و version-scoped باشد؛ markerها group node و yellow labels leaf/row-label node هستند، اما قابلیت nodeهای ساختاری دیگر و ambiguity را نیز لازم دارد.
2. HeaderPath باید چندسطحی و ordered باشد و mergeها را به‌صورت ساختار Header حفظ کند؛ merged cell نباید به‌عنوان چند Header مستقل تکرار شود.
3. ColumnSlotها در scope table/layout node تعریف شوند؛ یک جدول می‌تواند چند ColumnSlot مجاز داشته باشد و ستون‌های خارج از border فقط با rule/approval صریح وارد template می‌شوند.
4. SemanticMapping باید intersection دقیق RowAxisPath و HeaderPath را هدف بگیرد؛ رنگ و border برای کشف/تأیید Template مفیدند، اما به‌تنهایی semantic identity یا metric mapping نیستند.
5. Ruleهای مقدار باید وضعیت‌های numeric، blank، explicit zero، excluded/black و uncolored را از هم جدا کنند. فقط blank Gray طبق rule 7 مالک صفر می‌شود؛ blank در هر رنگ/موقعیت دیگر خودکار صفر نیست.
6. TemplateVersion باید worksheet direction (RTL/LTR)، merged ranges، layout nodeها، header rows، border bounds و column slotهای پذیرفته‌شده را به‌عنوان ویژگی‌های ساختاری نسخه نگه دارد. رنگ‌ها می‌توانند evidence/locator برای template recognition باشند، نه شرط لازم برای هر بار استخراج پس از تثبیت TemplateVersion.
7. نام‌های T01–T17/U01/S01 و مختصات سلول‌ها شناسه‌های audit report هستند، نه کلیدهای دائمی DB. TemplateNode IDها باید در نسخهٔ Template داخلی و stable باشند.

### 23.7 مرزهای حل‌نشده و نتیجه
گزارش 13 ابهام مالک را باز گذاشته است؛ از جمله ستون‌های بیرون border، نقش A95:D95 در T03، ردیف‌های black در T04، سلول‌های uncolored در T06، U01، T13 row 364، T17 بدون Yellow، و وضعیت Sheet1. این موارد نباید با heuristic یا رنگ‌خوانی خودکار حل شوند. گزارش همچنین بصری render نشده و RTL display فقط از metadata استنباط شده؛ پس ترتیب منطقی خواندن از روی RTL به‌تنهایی قطعی نیست.

**نتیجهٔ بازبینی:** نمونه‌های واقعی اکنون برای طراحی RowAxisPath، HeaderPath، ColumnSlot و direct SemanticMapping در دست است؛ نیازی به آپلود دوبارهٔ workbook برای این مرحله نیست. Gate 7 از نظر مدل مفهومی شواهد بهتری دارد، ولی تا تعیین تکلیف ambiguityهای لازم و اثبات mapping عملی، همچنان PARTIAL/OPEN می‌ماند. Multi-input همچنان UNPROVEN. طرح فیزیکی Gateهای 1/2/7/8 هنوز PROPOSED است. هیچ کد، ORM، schema، migration، دیتابیس یا تستی تغییر نکرد/اجرا نشد.
