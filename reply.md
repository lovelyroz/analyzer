# Legacy RawFinancialFact Row-Linkage Audit

- Database: `D:\winprojects\analyzer\tehran_stock.db`
- Mode: read-only

## 1. Raw fact population

- Total raw facts: **505**

## 2. Downstream references

| Referencing table | Exists | Rows | Non-null raw_fact_id | Distinct raw facts referenced |
|---|---:|---:|---:|---:|
| `mapping_decisions` | Yes | 0 | 0 | 0 |
| `normalized_financial_fact_inputs` | Yes | 0 | 0 | 0 |
| `normalized_financial_facts` | Yes | 0 | 0 | 0 |

## 3. Per-raw-fact linkage distribution

### `mapping_decisions`

| Number of referencing rows per raw fact | Raw facts |
|---:|---:|
| 0 | 505 |

- Dangling non-NULL references: **0**

### `normalized_financial_fact_inputs`

| Number of referencing rows per raw fact | Raw facts |
|---:|---:|
| 0 | 505 |

- Dangling non-NULL references: **0**

### `normalized_financial_facts`

| Number of referencing rows per raw fact | Raw facts |
|---:|---:|
| 0 | 505 |

- Dangling non-NULL references: **0**

## 4. Combined linkage across all three tables

| Total references across all three tables per raw fact | Raw facts |
|---:|---:|
| 0 | 505 |

## 5. Interpretation limits

- A reference count measures relational linkage, not semantic correctness or whether the referenced record is still needed.
- A raw fact with zero references is not automatically safe to delete.
- A normalized fact with a raw_fact_id may also have other provenance through normalized_financial_fact_inputs and mapping_decisions.
- No rows were changed, deleted, updated, or migrated.
