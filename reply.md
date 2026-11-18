# Migration 9 database state audit

- Mode: strictly read-only SQLite connection (mode=ro).
- No schema changes, data changes, or tests are performed.
- Database: D:\winprojects\analyzer\tehran_stock.db

## Migration ledger

- version=9; name=codal_excel_source_metadata; applied_at=2026-11-07 11:15:36.865524

## raw_financial_facts schema

```sql
CREATE TABLE raw_financial_facts (
	raw_fact_id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	report_version_id INTEGER NOT NULL, 
	period_id INTEGER NOT NULL, 
	raw_item_name VARCHAR(300) NOT NULL, 
	raw_item_code VARCHAR(100), 
	value NUMERIC(30, 4), 
	unit VARCHAR(50), 
	currency VARCHAR(20), 
	source_section VARCHAR(150), 
	source_row INTEGER, 
	source_column VARCHAR(100), 
	source_sheet VARCHAR(150), 
	source_column_header VARCHAR(300), 
	PRIMARY KEY (raw_fact_id), 
	FOREIGN KEY(company_id) REFERENCES companies (company_id), 
	FOREIGN KEY(report_version_id) REFERENCES report_versions (report_version_id), 
	FOREIGN KEY(period_id) REFERENCES financial_periods (period_id)
)
```

| cid | column | type | not_null | default | primary_key |
|---:|---|---|---:|---|---:|
| 0 | raw_fact_id | INTEGER | 1 | None | 1 |
| 1 | company_id | INTEGER | 1 | None | 0 |
| 2 | report_version_id | INTEGER | 1 | None | 0 |
| 3 | period_id | INTEGER | 1 | None | 0 |
| 4 | raw_item_name | VARCHAR(300) | 1 | None | 0 |
| 5 | raw_item_code | VARCHAR(100) | 0 | None | 0 |
| 6 | value | NUMERIC(30, 4) | 0 | None | 0 |
| 7 | unit | VARCHAR(50) | 0 | None | 0 |
| 8 | currency | VARCHAR(20) | 0 | None | 0 |
| 9 | source_section | VARCHAR(150) | 0 | None | 0 |
| 10 | source_row | INTEGER | 0 | None | 0 |
| 11 | source_column | VARCHAR(100) | 0 | None | 0 |
| 12 | source_sheet | VARCHAR(150) | 0 | None | 0 |
| 13 | source_column_header | VARCHAR(300) | 0 | None | 0 |

### ORM comparison

- Columns in database but not in current RawFinancialFact ORM model: source_column_header, source_sheet
- Columns in current ORM model but absent from database: (none)

### Target-column population (counts only; no values exposed)

- source_sheet: total_rows=505; non_null=505; distinct_non_null=1
- source_column_header: total_rows=505; non_null=505; distinct_non_null=23

### Indexes

(none)

### Foreign keys

- period_id -> financial_periods.period_id; on_update=NO ACTION; on_delete=NO ACTION
- report_version_id -> report_versions.report_version_id; on_update=NO ACTION; on_delete=NO ACTION
- company_id -> companies.company_id; on_update=NO ACTION; on_delete=NO ACTION

### Triggers

(none)

## Scope limitation

This audit reports the current ledger row and the current structure of raw_financial_facts. Because the original Migration 9 implementation is unavailable, this output cannot prove that every possible Migration 9 side effect has been identified.
