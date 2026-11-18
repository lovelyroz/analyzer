# Normalized / Derived FinancialFact Linkage Audit

- Database: `D:\winprojects\analyzer\tehran_stock.db`
- Mode: SQLite read-only
- Scope: row counts, FK-like reference counts, per-parent linkage, dangling references and duplicate input links

## 1. Table population

| Table | Exists | Rows | Columns |
|---|---:|---:|---:|
| `normalized_financial_facts` | Yes | 0 | 10 |
| `normalized_financial_fact_inputs` | Yes | 0 | 5 |
| `derived_financial_facts` | Yes | 0 | 11 |
| `derived_financial_fact_inputs` | Yes | 0 | 5 |

## 2. Reference inventory

| Source reference | Target | Source rows | Non-NULL | Distinct target IDs | Dangling |
|---|---|---:|---:|---:|---:|
| `normalized_financial_facts.raw_fact_id` | `raw_financial_facts.raw_fact_id` | 0 | 0 | 0 | 0 |
| `normalized_financial_facts.mapping_decision_id` | `mapping_decisions.mapping_decision_id` | 0 | 0 | 0 | 0 |
| `normalized_financial_fact_inputs.normalized_fact_id` | `normalized_financial_facts.fact_id` | 0 | 0 | 0 | 0 |
| `normalized_financial_fact_inputs.raw_fact_id` | `raw_financial_facts.raw_fact_id` | 0 | 0 | 0 | 0 |
| `normalized_financial_fact_inputs.mapping_decision_id` | `mapping_decisions.mapping_decision_id` | 0 | 0 | 0 | 0 |
| `derived_financial_facts.source_report_version_id` | `report_versions.report_version_id` | 0 | 0 | 0 | 0 |
| `derived_financial_fact_inputs.derived_fact_id` | `derived_financial_facts.derived_fact_id` | 0 | 0 | 0 | 0 |
| `derived_financial_fact_inputs.normalized_fact_id` | `normalized_financial_facts.fact_id` | 0 | 0 | 0 | 0 |
| `derived_financial_fact_inputs.derived_input_fact_id` | `derived_financial_facts.derived_fact_id` | 0 | 0 | 0 | 0 |

## 3. Per-parent linkage distribution

### `normalized_financial_facts.raw_fact_id` → `raw_financial_facts.raw_fact_id`

| References per target row | Target rows |
|---:|---:|
| 0 | 505 |

### `normalized_financial_facts.mapping_decision_id` → `mapping_decisions.mapping_decision_id`

| References per target row | Target rows |
|---:|---:|
| — | 0 |

### `normalized_financial_fact_inputs.normalized_fact_id` → `normalized_financial_facts.fact_id`

| References per target row | Target rows |
|---:|---:|
| — | 0 |

### `normalized_financial_fact_inputs.raw_fact_id` → `raw_financial_facts.raw_fact_id`

| References per target row | Target rows |
|---:|---:|
| 0 | 505 |

### `normalized_financial_fact_inputs.mapping_decision_id` → `mapping_decisions.mapping_decision_id`

| References per target row | Target rows |
|---:|---:|
| — | 0 |

### `derived_financial_facts.source_report_version_id` → `report_versions.report_version_id`

| References per target row | Target rows |
|---:|---:|
| 0 | 2 |

### `derived_financial_fact_inputs.derived_fact_id` → `derived_financial_facts.derived_fact_id`

| References per target row | Target rows |
|---:|---:|
| — | 0 |

### `derived_financial_fact_inputs.normalized_fact_id` → `normalized_financial_facts.fact_id`

| References per target row | Target rows |
|---:|---:|
| — | 0 |

### `derived_financial_fact_inputs.derived_input_fact_id` → `derived_financial_facts.derived_fact_id`

| References per target row | Target rows |
|---:|---:|
| — | 0 |

## 4. Duplicate input-link groups

- `normalized_financial_fact_inputs`: duplicate key groups = **0**
- `derived_financial_fact_inputs`: duplicate key groups = **0**

## 5. SQLite foreign-key integrity

- Rows returned by `PRAGMA foreign_key_check`: **0**

## 6. Interpretation limits

- This is a read-only snapshot of this exact database file; it does not prove the state of other environments, backups or external consumers.
- Linkage counts do not prove semantic correctness or that a row is safe to delete.
- A zero-row result does not authorize table, column or FK removal.
- Missing tables/columns are reported explicitly; they are not interpreted as zero rows.
- No database schema or row was changed.
