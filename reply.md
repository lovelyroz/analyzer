MIGRATION 9 HISTORY AND FULL SQLITE SCHEMA AUDIT
Repository: D:\winprojects\analyzer
Generated: 2026-11-18T00:54:22.145827


================================================================================
GIT STATUS
================================================================================
$ git status --short --branch
EXIT: 0
## master...origin/master
 M reply.md



================================================================================
BRANCHES
================================================================================
$ git branch -avv
EXIT: 0
* master                        0974528 [origin/master] reply
  stage7/remediation-2026-10-14 a7e120e [origin/stage7/remediation-2026-10-14: gone] Merge branch 'master' into stage7/remediation-2026-10-14
  remotes/origin/HEAD           -> origin/master
  remotes/origin/master         0974528 reply



================================================================================
ALL REFLOG ENTRIES
================================================================================
$ git reflog show --all --date=iso -n 100
EXIT: 0
0974528 refs/remotes/origin/HEAD@{2026-11-18 00:51:52 +0330}: remote set-head
0974528 refs/remotes/origin/master@{2026-11-18 00:51:50 +0330}: update by push
0974528 refs/heads/master@{2026-11-18 00:51:45 +0330}: commit: reply
0974528 HEAD@{2026-11-18 00:51:45 +0330}: commit: reply
2de04f4 refs/remotes/origin/HEAD@{2026-11-18 00:29:37 +0330}: remote set-head
2de04f4 refs/heads/master@{2026-11-18 00:29:35 +0330}: pull --ff --recurse-submodules --progress -- origin: Fast-forward
2de04f4 HEAD@{2026-11-18 00:29:35 +0330}: pull --ff --recurse-submodules --progress -- origin: Fast-forward
2de04f4 refs/remotes/origin/HEAD@{2026-11-18 00:29:29 +0330}: remote set-head
2de04f4 refs/remotes/origin/master@{2026-11-18 00:29:28 +0330}: fetch --progress --prune --recurse-submodules=on-demand -- origin: fast-forward
be6de88 refs/remotes/origin/HEAD@{2026-11-18 00:23:09 +0330}: remote set-head
be6de88 refs/heads/master@{2026-11-18 00:23:07 +0330}: pull --ff --recurse-submodules --progress -- origin: Fast-forward
be6de88 HEAD@{2026-11-18 00:23:07 +0330}: pull --ff --recurse-submodules --progress -- origin: Fast-forward
be6de88 refs/remotes/origin/HEAD@{2026-11-18 00:23:02 +0330}: remote set-head
be6de88 refs/remotes/origin/master@{2026-11-18 00:23:01 +0330}: fetch --progress --prune --recurse-submodules=on-demand -- origin: fast-forward
cef8f9a refs/remotes/origin/HEAD@{2026-11-18 00:20:56 +0330}: remote set-head
cef8f9a refs/heads/master@{2026-11-18 00:20:54 +0330}: pull --ff --recurse-submodules --progress -- origin: Fast-forward
cef8f9a HEAD@{2026-11-18 00:20:54 +0330}: pull --ff --recurse-submodules --progress -- origin: Fast-forward
cef8f9a refs/remotes/origin/HEAD@{2026-11-18 00:20:49 +0330}: remote set-head
cef8f9a refs/remotes/origin/master@{2026-11-18 00:20:48 +0330}: fetch --progress --prune --recurse-submodules=on-demand -- origin: fast-forward
752150c refs/remotes/origin/HEAD@{2026-11-18 00:16:09 +0330}: remote set-head
752150c refs/heads/master@{2026-11-18 00:16:07 +0330}: pull --ff --recurse-submodules --progress -- origin: Fast-forward
752150c refs/remotes/origin/master@{2026-11-18 00:16:07 +0330}: pull --ff --recurse-submodules --progress -- origin: fast-forward
752150c HEAD@{2026-11-18 00:16:07 +0330}: pull --ff --recurse-submodules --progress -- origin: Fast-forward
7bb4c47 refs/remotes/origin/HEAD@{2026-11-18 00:07:58 +0330}: remote set-head
7bb4c47 refs/remotes/origin/master@{2026-11-18 00:07:57 +0330}: fetch --progress --prune --recurse-submodules=on-demand -- origin: fast-forward
5c620be refs/remotes/origin/HEAD@{2026-11-18 00:04:26 +0330}: remote set-head
5c620be refs/remotes/origin/HEAD@{2026-11-17 13:27:03 +0330}: remote set-head
5c620be refs/heads/master@{2026-11-17 13:27:00 +0330}: pull --ff --recurse-submodules --progress -- origin: Fast-forward
5c620be HEAD@{2026-11-17 13:27:00 +0330}: pull --ff --recurse-submodules --progress -- origin: Fast-forward
5c620be refs/remotes/origin/HEAD@{2026-11-17 13:26:54 +0330}: remote set-head
5c620be refs/remotes/origin/master@{2026-11-17 13:26:52 +0330}: fetch --progress --prune --recurse-submodules=on-demand -- origin: fast-forward
eafc5a0 refs/remotes/origin/HEAD@{2026-11-17 13:05:48 +0330}: remote set-head
eafc5a0 refs/heads/master@{2026-11-17 13:05:45 +0330}: pull --ff --recurse-submodules --progress -- origin: Fast-forward
eafc5a0 HEAD@{2026-11-17 13:05:45 +0330}: pull --ff --recurse-submodules --progress -- origin: Fast-forward
eafc5a0 refs/remotes/origin/HEAD@{2026-11-17 13:05:39 +0330}: remote set-head
eafc5a0 refs/remotes/origin/master@{2026-11-17 13:05:37 +0330}: fetch --progress --prune --recurse-submodules=on-demand -- origin: fast-forward
8ca9de4 refs/remotes/origin/HEAD@{2026-11-17 12:49:14 +0330}: remote set-head
8ca9de4 refs/remotes/origin/master@{2026-11-17 12:49:10 +0330}: update by push
8ca9de4 refs/heads/master@{2026-11-17 12:49:04 +0330}: commit: parsian periodic 5
8ca9de4 HEAD@{2026-11-17 12:49:04 +0330}: commit: parsian periodic 5
3d12452 refs/remotes/origin/HEAD@{2026-11-17 12:45:40 +0330}: remote set-head
3d12452 refs/remotes/origin/master@{2026-11-17 12:45:36 +0330}: update by push
3d12452 refs/heads/master@{2026-11-17 12:45:30 +0330}: commit: parsian periodic 4
3d12452 HEAD@{2026-11-17 12:45:30 +0330}: commit: parsian periodic 4
a4e38c4 refs/remotes/origin/HEAD@{2026-11-17 12:15:47 +0330}: remote set-head
a4e38c4 refs/remotes/origin/master@{2026-11-17 12:15:43 +0330}: update by push
a4e38c4 refs/heads/master@{2026-11-17 12:15:38 +0330}: commit: parsian periodic 3
a4e38c4 HEAD@{2026-11-17 12:15:38 +0330}: commit: parsian periodic 3
b588261 refs/remotes/origin/HEAD@{2026-11-17 12:01:51 +0330}: remote set-head
b588261 refs/remotes/origin/HEAD@{2026-11-17 11:29:23 +0330}: remote set-head
b588261 refs/remotes/origin/master@{2026-11-17 11:29:20 +0330}: update by push
b588261 refs/heads/master@{2026-11-17 11:29:15 +0330}: commit: parsian report 2
b588261 HEAD@{2026-11-17 11:29:15 +0330}: commit: parsian report 2
3c4b03f refs/remotes/origin/HEAD@{2026-11-17 11:17:02 +0330}: remote set-head
3c4b03f refs/remotes/origin/HEAD@{2026-11-17 11:11:39 +0330}: remote set-head
3c4b03f refs/heads/master@{2026-11-17 11:11:37 +0330}: pull --ff --recurse-submodules --progress -- origin: Fast-forward
3c4b03f HEAD@{2026-11-17 11:11:37 +0330}: pull --ff --recurse-submodules --progress -- origin: Fast-forward
3c4b03f refs/remotes/origin/HEAD@{2026-11-17 11:11:31 +0330}: remote set-head
3c4b03f refs/remotes/origin/master@{2026-11-17 11:11:30 +0330}: fetch --progress --prune --recurse-submodules=on-demand -- origin: fast-forward
f244670 refs/remotes/origin/HEAD@{2026-11-17 11:04:01 +0330}: remote set-head
f244670 refs/remotes/origin/HEAD@{2026-11-16 23:14:03 +0330}: remote set-head
f244670 refs/heads/master@{2026-11-16 23:14:01 +0330}: pull --ff --recurse-submodules --progress -- origin: Fast-forward
f244670 HEAD@{2026-11-16 23:14:01 +0330}: pull --ff --recurse-submodules --progress -- origin: Fast-forward
f244670 refs/remotes/origin/HEAD@{2026-11-16 23:13:48 +0330}: remote set-head
f244670 refs/remotes/origin/master@{2026-11-16 23:13:47 +0330}: fetch --progress --prune --recurse-submodules=on-demand -- origin: fast-forward
8f10ee5 refs/remotes/origin/HEAD@{2026-11-16 23:12:42 +0330}: remote set-head
8f10ee5 refs/heads/master@{2026-11-16 23:12:40 +0330}: pull --ff --recurse-submodules --progress -- origin: Fast-forward
8f10ee5 HEAD@{2026-11-16 23:12:40 +0330}: pull --ff --recurse-submodules --progress -- origin: Fast-forward
8f10ee5 refs/remotes/origin/HEAD@{2026-11-16 23:10:51 +0330}: remote set-head
8f10ee5 refs/remotes/origin/master@{2026-11-16 23:10:50 +0330}: fetch --progress --prune --recurse-submodules=on-demand -- origin: fast-forward
ed63ec0 refs/remotes/origin/HEAD@{2026-11-16 22:47:09 +0330}: remote set-head
ed63ec0 refs/remotes/origin/master@{2026-11-16 22:47:07 +0330}: update by push
9ddb1ca refs/remotes/origin/HEAD@{2026-11-16 22:46:58 +0330}: remote set-head
ed63ec0 refs/heads/master@{2026-11-16 22:46:55 +0330}: pull --ff --recurse-submodules --progress -- origin: Merge made by the 'ort' strategy.
ed63ec0 HEAD@{2026-11-16 22:46:55 +0330}: pull --ff --recurse-submodules --progress -- origin: Merge made by the 'ort' strategy.
b042020 refs/heads/master@{2026-11-16 22:46:47 +0330}: commit: Audit the Completed Parsian Periodic
b042020 HEAD@{2026-11-16 22:46:47 +0330}: commit: Audit the Completed Parsian Periodic
9ddb1ca refs/remotes/origin/HEAD@{2026-11-16 22:29:23 +0330}: remote set-head
9ddb1ca refs/remotes/origin/HEAD@{2026-11-16 21:57:10 +0330}: remote set-head
9ddb1ca refs/remotes/origin/HEAD@{2026-11-16 15:33:10 +0330}: remote set-head
9ddb1ca refs/remotes/origin/master@{2026-11-16 15:33:09 +0330}: fetch --progress --prune --recurse-submodules=on-demand -- origin: fast-forward
7760732 refs/remotes/origin/HEAD@{2026-11-16 14:36:47 +0330}: remote set-head
7760732 refs/remotes/origin/master@{2026-11-16 14:36:45 +0330}: update by push
7760732 refs/heads/master@{2026-11-16 14:36:40 +0330}: commit: reply
7760732 HEAD@{2026-11-16 14:36:40 +0330}: commit: reply
af4c2d6 refs/remotes/origin/HEAD@{2026-11-16 14:33:43 +0330}: remote set-head
af4c2d6 refs/heads/master@{2026-11-16 14:33:41 +0330}: pull --ff --recurse-submodules --progress -- origin: Fast-forward
af4c2d6 HEAD@{2026-11-16 14:33:41 +0330}: pull --ff --recurse-submodules --progress -- origin: Fast-forward
af4c2d6 refs/remotes/origin/HEAD@{2026-11-16 14:08:27 +0330}: remote set-head
af4c2d6 refs/remotes/origin/master@{2026-11-16 14:08:26 +0330}: fetch --progress --prune --recurse-submodules=on-demand -- origin: fast-forward
7c1ab36 refs/remotes/origin/HEAD@{2026-11-16 13:33:53 +0330}: remote set-head
7c1ab36 refs/remotes/origin/master@{2026-11-16 13:33:50 +0330}: update by push
7c1ab36 refs/heads/master@{2026-11-16 13:33:42 +0330}: commit: reply
7c1ab36 HEAD@{2026-11-16 13:33:42 +0330}: commit: reply
c818a5e refs/remotes/origin/HEAD@{2026-11-16 13:31:51 +0330}: remote set-head
c818a5e refs/heads/master@{2026-11-16 13:31:48 +0330}: pull --ff --recurse-submodules --progress -- origin: Fast-forward
c818a5e HEAD@{2026-11-16 13:31:48 +0330}: pull --ff --recurse-submodules --progress -- origin: Fast-forward
c818a5e refs/remotes/origin/HEAD@{2026-11-16 13:31:42 +0330}: remote set-head
c818a5e refs/remotes/origin/master@{2026-11-16 13:31:40 +0330}: fetch --progress --prune --recurse-submodules=on-demand -- origin: fast-forward
09a2b4c refs/remotes/origin/HEAD@{2026-11-16 13:30:52 +0330}: remote set-head



================================================================================
MIGRATION RUNNER HISTORY
================================================================================
$ git log --all --date=iso --format=%H | %ad | %s -- src/migrations/runner.py
EXIT: 0
5c0608e5e06dd6934c4fdb2196160ccfc39faa87 | 2026-11-01 14:05:26 +0330 | S7P054–057 — Remove Forecast Output Persistence and Preserve Runtime Integration
84f9940933e481fffcedfc2d2647b4ec7f4301e9 | 2026-10-22 22:39:42 +0330 | P45
1d6ae3e90fb90110ee4eb25b56b0479a7ff5437b | 2026-10-19 14:33:29 +0330 | Agent host session ce5b4e8d-41eb-4472-86b7-3e3c09155623 - baseline checkpoint
dc283e9a180f1321fffc23c2dde69c8a57ca0145 | 2026-10-01 20:22:07 +0330 | prompt4_stage5
77abe3840c6976aa0aef77006603c1a08606cfa6 | 2026-09-17 11:32:48 +0330 | fix: restore migration runner with version 6 fx_rates_jalali_components
9fb9541056a42dc29134c235dfef451ccca25410 | 2026-09-17 11:32:10 +0330 | feat(fx): service ingest_fx_xlsx + migration 6 runner + tests
07dab699195b008a7e030a695a657b0de6b32b02 | 2026-09-17 09:51:32 +0330 | fix: migration tests expect version 5; migration 5 skips if market_daily missing
99738b64273d460000e64a67ba7a9d9cd362f9ff | 2026-09-17 09:43:53 +0330 | feat(db): CHANGE-005 Jalali date components on market_daily (V1.2)
c8441fbf57dd1d56d7e65d001b62888d425e8c01 | 2026-09-17 00:30:55 +0330 | Make report-version integrity migration fail safely
cc696522ed9847014c0b43b0277ba50c010771f5 | 2026-09-17 00:30:42 +0330 | Add migration for single current report version invariant
249937f7946f326aa0b27534349ca7c724c28682 | 2026-09-17 00:28:13 +0330 | Add migration for normalized multi-source provenance
e411464f7b2177450b909e507a82c3bdfff3daca | 2026-09-17 00:16:38 +0330 | Stage 1 Database Architecture V1



================================================================================
MIGRATION 9 STRING HISTORY
================================================================================
$ git log --all --oneline -S codal_excel_source_metadata -- .
EXIT: 0
0974528 reply
2de04f4 docs(database): record runtime migration source drift
8742704 docs(database): record runtime SQLite migration reconciliation



================================================================================
AUDIT SCRIPT HISTORY
================================================================================
$ git log --all --date=iso --format=%H | %ad | %s -- src/scripts/audit_migration_9.py
EXIT: 0



================================================================================
CURRENT COMMIT
================================================================================
$ git log -1 --format=%H%n%ad%n%s --date=iso
EXIT: 0
097452841d555f61c9cbddcd7f35df0190411384
2026-11-18 00:51:45 +0330
reply



================================================================================
FULL SQLITE SCHEMA
================================================================================
Database: D:\winprojects\analyzer\tehran_stock.db
Size: 688128 bytes
SQLite version: 3.45.3

----------------------------------------------------------------------
OBJECT: index | uq_report_current_version | TABLE: report_versions
DDL:
CREATE UNIQUE INDEX uq_report_current_version ON report_versions (report_id) WHERE is_current_version IS 1

----------------------------------------------------------------------
OBJECT: table | companies | TABLE: companies
DDL:
CREATE TABLE companies (
	company_id INTEGER NOT NULL, 
	national_id VARCHAR(20), 
	ticker VARCHAR(50) NOT NULL, 
	company_name VARCHAR(200) NOT NULL, 
	industry_id INTEGER NOT NULL, 
	codal_symbol VARCHAR(50), 
	fiscal_year_end VARCHAR(10), 
	status VARCHAR(30) NOT NULL, 
	is_active BOOLEAN NOT NULL, 
	created_at DATETIME, 
	PRIMARY KEY (company_id), 
	UNIQUE (national_id), 
	FOREIGN KEY(industry_id) REFERENCES industries (industry_id)
)
COLUMNS:
  0 | company_id | INTEGER | notnull=1 | pk=1 | default=None
  1 | national_id | VARCHAR(20) | notnull=0 | pk=0 | default=None
  2 | ticker | VARCHAR(50) | notnull=1 | pk=0 | default=None
  3 | company_name | VARCHAR(200) | notnull=1 | pk=0 | default=None
  4 | industry_id | INTEGER | notnull=1 | pk=0 | default=None
  5 | codal_symbol | VARCHAR(50) | notnull=0 | pk=0 | default=None
  6 | fiscal_year_end | VARCHAR(10) | notnull=0 | pk=0 | default=None
  7 | status | VARCHAR(30) | notnull=1 | pk=0 | default=None
  8 | is_active | BOOLEAN | notnull=1 | pk=0 | default=None
  9 | created_at | DATETIME | notnull=0 | pk=0 | default=None
FOREIGN KEYS:
  industry_id -> industries.industry_id | on_update=NO ACTION | on_delete=NO ACTION
INDEXES:
  sqlite_autoindex_companies_1 | unique=1 | origin=u

----------------------------------------------------------------------
OBJECT: table | corporate_actions | TABLE: corporate_actions
DDL:
CREATE TABLE corporate_actions (
	action_id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	announcement_date DATE, 
	effective_date DATE NOT NULL, 
	action_type VARCHAR(50) NOT NULL, 
	old_share_count INTEGER, 
	new_share_count INTEGER, 
	ratio NUMERIC(18, 8), 
	source VARCHAR(100), 
	PRIMARY KEY (action_id), 
	CONSTRAINT uq_company_action_date_type UNIQUE (company_id, effective_date, action_type), 
	FOREIGN KEY(company_id) REFERENCES companies (company_id)
)
COLUMNS:
  0 | action_id | INTEGER | notnull=1 | pk=1 | default=None
  1 | company_id | INTEGER | notnull=1 | pk=0 | default=None
  2 | announcement_date | DATE | notnull=0 | pk=0 | default=None
  3 | effective_date | DATE | notnull=1 | pk=0 | default=None
  4 | action_type | VARCHAR(50) | notnull=1 | pk=0 | default=None
  5 | old_share_count | INTEGER | notnull=0 | pk=0 | default=None
  6 | new_share_count | INTEGER | notnull=0 | pk=0 | default=None
  7 | ratio | NUMERIC(18, 8) | notnull=0 | pk=0 | default=None
  8 | source | VARCHAR(100) | notnull=0 | pk=0 | default=None
FOREIGN KEYS:
  company_id -> companies.company_id | on_update=NO ACTION | on_delete=NO ACTION
INDEXES:
  sqlite_autoindex_corporate_actions_1 | unique=1 | origin=u

----------------------------------------------------------------------
OBJECT: table | derived_financial_fact_inputs | TABLE: derived_financial_fact_inputs
DDL:
CREATE TABLE derived_financial_fact_inputs (
	input_id INTEGER NOT NULL, 
	derived_fact_id INTEGER NOT NULL, 
	normalized_fact_id INTEGER, 
	derived_input_fact_id INTEGER, 
	input_role VARCHAR(100) NOT NULL, 
	PRIMARY KEY (input_id), 
	CONSTRAINT chk_derived_input_source CHECK ((normalized_fact_id IS NOT NULL AND derived_input_fact_id IS NULL) OR (normalized_fact_id IS NULL AND derived_input_fact_id IS NOT NULL)), 
	CONSTRAINT uq_derived_fact_input UNIQUE (derived_fact_id, normalized_fact_id, derived_input_fact_id, input_role), 
	FOREIGN KEY(derived_fact_id) REFERENCES derived_financial_facts (derived_fact_id), 
	FOREIGN KEY(normalized_fact_id) REFERENCES normalized_financial_facts (fact_id), 
	FOREIGN KEY(derived_input_fact_id) REFERENCES derived_financial_facts (derived_fact_id)
)
COLUMNS:
  0 | input_id | INTEGER | notnull=1 | pk=1 | default=None
  1 | derived_fact_id | INTEGER | notnull=1 | pk=0 | default=None
  2 | normalized_fact_id | INTEGER | notnull=0 | pk=0 | default=None
  3 | derived_input_fact_id | INTEGER | notnull=0 | pk=0 | default=None
  4 | input_role | VARCHAR(100) | notnull=1 | pk=0 | default=None
FOREIGN KEYS:
  derived_input_fact_id -> derived_financial_facts.derived_fact_id | on_update=NO ACTION | on_delete=NO ACTION
  normalized_fact_id -> normalized_financial_facts.fact_id | on_update=NO ACTION | on_delete=NO ACTION
  derived_fact_id -> derived_financial_facts.derived_fact_id | on_update=NO ACTION | on_delete=NO ACTION
INDEXES:
  sqlite_autoindex_derived_financial_fact_inputs_1 | unique=1 | origin=u

----------------------------------------------------------------------
OBJECT: table | derived_financial_facts | TABLE: derived_financial_facts
DDL:
CREATE TABLE derived_financial_facts (
	derived_fact_id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	period_id INTEGER NOT NULL, 
	metric_id INTEGER NOT NULL, 
	value_irr NUMERIC(30, 4), 
	formula_code VARCHAR(100) NOT NULL, 
	formula_version VARCHAR(30) NOT NULL, 
	source_report_version_id INTEGER NOT NULL, 
	quality_status VARCHAR(20) NOT NULL, 
	data_cutoff_datetime DATETIME NOT NULL, 
	calculated_at DATETIME NOT NULL, 
	PRIMARY KEY (derived_fact_id), 
	CONSTRAINT uq_derived_financial_fact UNIQUE (company_id, period_id, metric_id, formula_code, formula_version, source_report_version_id), 
	CONSTRAINT chk_derived_quality_status CHECK (quality_status IN ('VALID','MISSING','ESTIMATED','SUSPICIOUS')), 
	FOREIGN KEY(company_id) REFERENCES companies (company_id), 
	FOREIGN KEY(period_id) REFERENCES financial_periods (period_id), 
	FOREIGN KEY(metric_id) REFERENCES financial_metrics (metric_id), 
	FOREIGN KEY(source_report_version_id) REFERENCES report_versions (report_version_id)
)
COLUMNS:
  0 | derived_fact_id | INTEGER | notnull=1 | pk=1 | default=None
  1 | company_id | INTEGER | notnull=1 | pk=0 | default=None
  2 | period_id | INTEGER | notnull=1 | pk=0 | default=None
  3 | metric_id | INTEGER | notnull=1 | pk=0 | default=None
  4 | value_irr | NUMERIC(30, 4) | notnull=0 | pk=0 | default=None
  5 | formula_code | VARCHAR(100) | notnull=1 | pk=0 | default=None
  6 | formula_version | VARCHAR(30) | notnull=1 | pk=0 | default=None
  7 | source_report_version_id | INTEGER | notnull=1 | pk=0 | default=None
  8 | quality_status | VARCHAR(20) | notnull=1 | pk=0 | default=None
  9 | data_cutoff_datetime | DATETIME | notnull=1 | pk=0 | default=None
  10 | calculated_at | DATETIME | notnull=1 | pk=0 | default=None
FOREIGN KEYS:
  source_report_version_id -> report_versions.report_version_id | on_update=NO ACTION | on_delete=NO ACTION
  metric_id -> financial_metrics.metric_id | on_update=NO ACTION | on_delete=NO ACTION
  period_id -> financial_periods.period_id | on_update=NO ACTION | on_delete=NO ACTION
  company_id -> companies.company_id | on_update=NO ACTION | on_delete=NO ACTION
INDEXES:
  sqlite_autoindex_derived_financial_facts_1 | unique=1 | origin=u

----------------------------------------------------------------------
OBJECT: table | financial_metrics | TABLE: financial_metrics
DDL:
CREATE TABLE financial_metrics (
	metric_id INTEGER NOT NULL, 
	metric_code VARCHAR(100) NOT NULL, 
	metric_name VARCHAR(200) NOT NULL, 
	category VARCHAR(50) NOT NULL, 
	industry_id INTEGER, 
	statement_type VARCHAR(30), 
	parent_metric_id INTEGER, 
	value_type VARCHAR(30) NOT NULL, 
	flow_or_stock VARCHAR(10) NOT NULL, 
	sign_convention VARCHAR(20) NOT NULL, 
	is_derived BOOLEAN NOT NULL, 
	PRIMARY KEY (metric_id), 
	CONSTRAINT chk_metric_flow_stock CHECK (flow_or_stock IN ('FLOW','STOCK')), 
	CONSTRAINT chk_metric_statement_type CHECK (statement_type IS NULL OR statement_type IN ('INCOME','BALANCE_SHEET','CASH_FLOW','EQUITY','GENERAL')), 
	CONSTRAINT chk_metric_sign_convention CHECK (sign_convention IN ('NATURAL','EXPENSE_POSITIVE','EXPENSE_NEGATIVE')), 
	UNIQUE (metric_code), 
	FOREIGN KEY(industry_id) REFERENCES industries (industry_id) ON DELETE SET NULL, 
	FOREIGN KEY(parent_metric_id) REFERENCES financial_metrics (metric_id) ON DELETE SET NULL
)
COLUMNS:
  0 | metric_id | INTEGER | notnull=1 | pk=1 | default=None
  1 | metric_code | VARCHAR(100) | notnull=1 | pk=0 | default=None
  2 | metric_name | VARCHAR(200) | notnull=1 | pk=0 | default=None
  3 | category | VARCHAR(50) | notnull=1 | pk=0 | default=None
  4 | industry_id | INTEGER | notnull=0 | pk=0 | default=None
  5 | statement_type | VARCHAR(30) | notnull=0 | pk=0 | default=None
  6 | parent_metric_id | INTEGER | notnull=0 | pk=0 | default=None
  7 | value_type | VARCHAR(30) | notnull=1 | pk=0 | default=None
  8 | flow_or_stock | VARCHAR(10) | notnull=1 | pk=0 | default=None
  9 | sign_convention | VARCHAR(20) | notnull=1 | pk=0 | default=None
  10 | is_derived | BOOLEAN | notnull=1 | pk=0 | default=None
FOREIGN KEYS:
  parent_metric_id -> financial_metrics.metric_id | on_update=NO ACTION | on_delete=SET NULL
  industry_id -> industries.industry_id | on_update=NO ACTION | on_delete=SET NULL
INDEXES:
  sqlite_autoindex_financial_metrics_1 | unique=1 | origin=u

----------------------------------------------------------------------
OBJECT: table | financial_periods | TABLE: financial_periods
DDL:
CREATE TABLE financial_periods (
	period_id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	period_type VARCHAR(20) NOT NULL, 
	start_date DATE NOT NULL, 
	end_date DATE NOT NULL, 
	fiscal_year INTEGER NOT NULL, 
	fiscal_quarter INTEGER, 
	months_length INTEGER NOT NULL, 
	is_ytd BOOLEAN NOT NULL, 
	PRIMARY KEY (period_id), 
	CONSTRAINT chk_period_dates CHECK (end_date >= start_date), 
	CONSTRAINT chk_period_type CHECK (period_type IN ('MONTH','QUARTER','SEMI_ANNUAL','NINE_MONTH','ANNUAL','TTM')), 
	CONSTRAINT uq_company_period UNIQUE (company_id, fiscal_year, period_type, end_date), 
	FOREIGN KEY(company_id) REFERENCES companies (company_id)
)
COLUMNS:
  0 | period_id | INTEGER | notnull=1 | pk=1 | default=None
  1 | company_id | INTEGER | notnull=1 | pk=0 | default=None
  2 | period_type | VARCHAR(20) | notnull=1 | pk=0 | default=None
  3 | start_date | DATE | notnull=1 | pk=0 | default=None
  4 | end_date | DATE | notnull=1 | pk=0 | default=None
  5 | fiscal_year | INTEGER | notnull=1 | pk=0 | default=None
  6 | fiscal_quarter | INTEGER | notnull=0 | pk=0 | default=None
  7 | months_length | INTEGER | notnull=1 | pk=0 | default=None
  8 | is_ytd | BOOLEAN | notnull=1 | pk=0 | default=None
FOREIGN KEYS:
  company_id -> companies.company_id | on_update=NO ACTION | on_delete=NO ACTION
INDEXES:
  sqlite_autoindex_financial_periods_1 | unique=1 | origin=u

----------------------------------------------------------------------
OBJECT: table | fx_conversion_rules | TABLE: fx_conversion_rules
DDL:
CREATE TABLE fx_conversion_rules (
	rule_id INTEGER NOT NULL, 
	metric_type VARCHAR(30) NOT NULL, 
	conversion_method VARCHAR(50) NOT NULL, 
	rate_type VARCHAR(30) NOT NULL, 
	description VARCHAR(300), 
	PRIMARY KEY (rule_id), 
	CONSTRAINT chk_fx_metric_type CHECK (metric_type IN ('FLOW','STOCK','MARKET_VALUE')), 
	CONSTRAINT chk_fx_rule_rate_type CHECK (rate_type IN ('FREE_MARKET','OPERATIONAL','OFFICIAL','ESTIMATED','MANUAL_OPERATOR'))
)
COLUMNS:
  0 | rule_id | INTEGER | notnull=1 | pk=1 | default=None
  1 | metric_type | VARCHAR(30) | notnull=1 | pk=0 | default=None
  2 | conversion_method | VARCHAR(50) | notnull=1 | pk=0 | default=None
  3 | rate_type | VARCHAR(30) | notnull=1 | pk=0 | default=None
  4 | description | VARCHAR(300) | notnull=0 | pk=0 | default=None
FOREIGN KEYS:
INDEXES:

----------------------------------------------------------------------
OBJECT: table | fx_rates | TABLE: fx_rates
DDL:
CREATE TABLE fx_rates (
	fx_rate_id INTEGER NOT NULL, 
	rate_date DATE, 
	jalali_year INTEGER, 
	jalali_month INTEGER, 
	jalali_day INTEGER, 
	currency_from VARCHAR(10) NOT NULL, 
	currency_to VARCHAR(10) NOT NULL, 
	rate NUMERIC(18, 4) NOT NULL, 
	rate_type VARCHAR(30) NOT NULL, 
	source VARCHAR(100), 
	PRIMARY KEY (fx_rate_id), 
	CONSTRAINT uq_fx_rate UNIQUE (rate_date, currency_from, currency_to, rate_type), 
	CONSTRAINT chk_fx_rate_type CHECK (rate_type IN ('FREE_MARKET','OPERATIONAL','OFFICIAL','ESTIMATED','MANUAL_OPERATOR')), 
	CONSTRAINT chk_fx_jalali_month CHECK (jalali_month IS NULL OR (jalali_month >= 1 AND jalali_month <= 12)), 
	CONSTRAINT chk_fx_jalali_day CHECK (jalali_day IS NULL OR (jalali_day >= 1 AND jalali_day <= 31))
)
COLUMNS:
  0 | fx_rate_id | INTEGER | notnull=1 | pk=1 | default=None
  1 | rate_date | DATE | notnull=0 | pk=0 | default=None
  2 | jalali_year | INTEGER | notnull=0 | pk=0 | default=None
  3 | jalali_month | INTEGER | notnull=0 | pk=0 | default=None
  4 | jalali_day | INTEGER | notnull=0 | pk=0 | default=None
  5 | currency_from | VARCHAR(10) | notnull=1 | pk=0 | default=None
  6 | currency_to | VARCHAR(10) | notnull=1 | pk=0 | default=None
  7 | rate | NUMERIC(18, 4) | notnull=1 | pk=0 | default=None
  8 | rate_type | VARCHAR(30) | notnull=1 | pk=0 | default=None
  9 | source | VARCHAR(100) | notnull=0 | pk=0 | default=None
FOREIGN KEYS:
INDEXES:
  sqlite_autoindex_fx_rates_1 | unique=1 | origin=u

----------------------------------------------------------------------
OBJECT: table | industries | TABLE: industries
DDL:
CREATE TABLE industries (
	industry_id INTEGER NOT NULL, 
	industry_code VARCHAR(50) NOT NULL, 
	industry_name VARCHAR(150) NOT NULL, 
	parent_industry_id INTEGER, 
	PRIMARY KEY (industry_id), 
	UNIQUE (industry_code), 
	FOREIGN KEY(parent_industry_id) REFERENCES industries (industry_id) ON DELETE SET NULL
)
COLUMNS:
  0 | industry_id | INTEGER | notnull=1 | pk=1 | default=None
  1 | industry_code | VARCHAR(50) | notnull=1 | pk=0 | default=None
  2 | industry_name | VARCHAR(150) | notnull=1 | pk=0 | default=None
  3 | parent_industry_id | INTEGER | notnull=0 | pk=0 | default=None
FOREIGN KEYS:
  parent_industry_id -> industries.industry_id | on_update=NO ACTION | on_delete=SET NULL
INDEXES:
  sqlite_autoindex_industries_1 | unique=1 | origin=u

----------------------------------------------------------------------
OBJECT: table | ingestion_runs | TABLE: ingestion_runs
DDL:
CREATE TABLE ingestion_runs (
	ingestion_id INTEGER NOT NULL, 
	source VARCHAR(50) NOT NULL, 
	started_at DATETIME NOT NULL, 
	finished_at DATETIME, 
	status VARCHAR(20) NOT NULL, 
	records_found INTEGER, 
	records_inserted INTEGER, 
	records_updated INTEGER, 
	records_failed INTEGER, 
	error_log VARCHAR, 
	PRIMARY KEY (ingestion_id)
)
COLUMNS:
  0 | ingestion_id | INTEGER | notnull=1 | pk=1 | default=None
  1 | source | VARCHAR(50) | notnull=1 | pk=0 | default=None
  2 | started_at | DATETIME | notnull=1 | pk=0 | default=None
  3 | finished_at | DATETIME | notnull=0 | pk=0 | default=None
  4 | status | VARCHAR(20) | notnull=1 | pk=0 | default=None
  5 | records_found | INTEGER | notnull=0 | pk=0 | default=None
  6 | records_inserted | INTEGER | notnull=0 | pk=0 | default=None
  7 | records_updated | INTEGER | notnull=0 | pk=0 | default=None
  8 | records_failed | INTEGER | notnull=0 | pk=0 | default=None
  9 | error_log | VARCHAR | notnull=0 | pk=0 | default=None
FOREIGN KEYS:
INDEXES:

----------------------------------------------------------------------
OBJECT: table | mapping_decisions | TABLE: mapping_decisions
DDL:
CREATE TABLE mapping_decisions (
	mapping_decision_id INTEGER NOT NULL, 
	raw_fact_id INTEGER NOT NULL, 
	metric_id INTEGER, 
	mapping_rule_id INTEGER, 
	mapping_method VARCHAR(30) NOT NULL, 
	confidence NUMERIC(5, 2), 
	review_status VARCHAR(20) NOT NULL, 
	composition_role VARCHAR(20), 
	transformation_spec TEXT, 
	reviewer VARCHAR(150), 
	reviewed_at DATETIME, 
	note TEXT, 
	PRIMARY KEY (mapping_decision_id), 
	CONSTRAINT chk_mapping_method CHECK (mapping_method IN ('TITLE_EXACT','ALIAS','PATTERN','POSITION','MANUAL','DERIVED')), 
	CONSTRAINT chk_mapping_review_status CHECK (review_status IN ('AUTO_MAPPED','REVIEW_REQUIRED','APPROVED','REJECTED','UNMAPPED')), 
	CONSTRAINT chk_mapping_composition_role CHECK (composition_role IS NULL OR composition_role IN ('COMPONENT','SUBTOTAL','TOTAL','DISCLOSURE')), 
	CONSTRAINT chk_mapping_confidence CHECK (confidence IS NULL OR (confidence >= 0 AND confidence <= 100)), 
	FOREIGN KEY(raw_fact_id) REFERENCES raw_financial_facts (raw_fact_id), 
	FOREIGN KEY(metric_id) REFERENCES financial_metrics (metric_id), 
	FOREIGN KEY(mapping_rule_id) REFERENCES mapping_rules (mapping_rule_id)
)
COLUMNS:
  0 | mapping_decision_id | INTEGER | notnull=1 | pk=1 | default=None
  1 | raw_fact_id | INTEGER | notnull=1 | pk=0 | default=None
  2 | metric_id | INTEGER | notnull=0 | pk=0 | default=None
  3 | mapping_rule_id | INTEGER | notnull=0 | pk=0 | default=None
  4 | mapping_method | VARCHAR(30) | notnull=1 | pk=0 | default=None
  5 | confidence | NUMERIC(5, 2) | notnull=0 | pk=0 | default=None
  6 | review_status | VARCHAR(20) | notnull=1 | pk=0 | default=None
  7 | composition_role | VARCHAR(20) | notnull=0 | pk=0 | default=None
  8 | transformation_spec | TEXT | notnull=0 | pk=0 | default=None
  9 | reviewer | VARCHAR(150) | notnull=0 | pk=0 | default=None
  10 | reviewed_at | DATETIME | notnull=0 | pk=0 | default=None
  11 | note | TEXT | notnull=0 | pk=0 | default=None
FOREIGN KEYS:
  mapping_rule_id -> mapping_rules.mapping_rule_id | on_update=NO ACTION | on_delete=NO ACTION
  metric_id -> financial_metrics.metric_id | on_update=NO ACTION | on_delete=NO ACTION
  raw_fact_id -> raw_financial_facts.raw_fact_id | on_update=NO ACTION | on_delete=NO ACTION
INDEXES:

----------------------------------------------------------------------
OBJECT: table | mapping_rules | TABLE: mapping_rules
DDL:
CREATE TABLE mapping_rules (
	mapping_rule_id INTEGER NOT NULL, 
	rule_code VARCHAR(100) NOT NULL, 
	rule_version VARCHAR(30) NOT NULL, 
	description TEXT, 
	is_active BOOLEAN NOT NULL, 
	PRIMARY KEY (mapping_rule_id), 
	CONSTRAINT uq_mapping_rule_version UNIQUE (rule_code, rule_version)
)
COLUMNS:
  0 | mapping_rule_id | INTEGER | notnull=1 | pk=1 | default=None
  1 | rule_code | VARCHAR(100) | notnull=1 | pk=0 | default=None
  2 | rule_version | VARCHAR(30) | notnull=1 | pk=0 | default=None
  3 | description | TEXT | notnull=0 | pk=0 | default=None
  4 | is_active | BOOLEAN | notnull=1 | pk=0 | default=None
FOREIGN KEYS:
INDEXES:
  sqlite_autoindex_mapping_rules_1 | unique=1 | origin=u

----------------------------------------------------------------------
OBJECT: table | market_daily | TABLE: market_daily
DDL:
CREATE TABLE market_daily (
	market_data_id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	trade_date DATE, 
	jalali_year INTEGER, 
	jalali_month INTEGER, 
	jalali_day INTEGER, 
	open_price NUMERIC(18, 2), 
	high_price NUMERIC(18, 2), 
	low_price NUMERIC(18, 2), 
	close_price NUMERIC(18, 2), 
	adjusted_close NUMERIC(18, 2), 
	volume INTEGER, 
	value NUMERIC(24, 2), 
	trade_count INTEGER, 
	source VARCHAR(100), 
	PRIMARY KEY (market_data_id), 
	CONSTRAINT uq_company_trade_date UNIQUE (company_id, trade_date), 
	CONSTRAINT chk_jalali_month CHECK (jalali_month IS NULL OR (jalali_month >= 1 AND jalali_month <= 12)), 
	CONSTRAINT chk_jalali_day CHECK (jalali_day IS NULL OR (jalali_day >= 1 AND jalali_day <= 31)), 
	FOREIGN KEY(company_id) REFERENCES companies (company_id)
)
COLUMNS:
  0 | market_data_id | INTEGER | notnull=1 | pk=1 | default=None
  1 | company_id | INTEGER | notnull=1 | pk=0 | default=None
  2 | trade_date | DATE | notnull=0 | pk=0 | default=None
  3 | jalali_year | INTEGER | notnull=0 | pk=0 | default=None
  4 | jalali_month | INTEGER | notnull=0 | pk=0 | default=None
  5 | jalali_day | INTEGER | notnull=0 | pk=0 | default=None
  6 | open_price | NUMERIC(18, 2) | notnull=0 | pk=0 | default=None
  7 | high_price | NUMERIC(18, 2) | notnull=0 | pk=0 | default=None
  8 | low_price | NUMERIC(18, 2) | notnull=0 | pk=0 | default=None
  9 | close_price | NUMERIC(18, 2) | notnull=0 | pk=0 | default=None
  10 | adjusted_close | NUMERIC(18, 2) | notnull=0 | pk=0 | default=None
  11 | volume | INTEGER | notnull=0 | pk=0 | default=None
  12 | value | NUMERIC(24, 2) | notnull=0 | pk=0 | default=None
  13 | trade_count | INTEGER | notnull=0 | pk=0 | default=None
  14 | source | VARCHAR(100) | notnull=0 | pk=0 | default=None
FOREIGN KEYS:
  company_id -> companies.company_id | on_update=NO ACTION | on_delete=NO ACTION
INDEXES:
  sqlite_autoindex_market_daily_1 | unique=1 | origin=u

----------------------------------------------------------------------
OBJECT: table | normalized_financial_fact_inputs | TABLE: normalized_financial_fact_inputs
DDL:
CREATE TABLE normalized_financial_fact_inputs (
	input_id INTEGER NOT NULL, 
	normalized_fact_id INTEGER NOT NULL, 
	raw_fact_id INTEGER NOT NULL, 
	mapping_decision_id INTEGER NOT NULL, 
	input_role VARCHAR(20) NOT NULL, 
	PRIMARY KEY (input_id), 
	CONSTRAINT chk_normalized_input_role CHECK (input_role IN ('DIRECT','COMPONENT','TOTAL','SUBTOTAL','DISCLOSURE')), 
	CONSTRAINT uq_normalized_fact_input UNIQUE (normalized_fact_id, raw_fact_id, mapping_decision_id), 
	FOREIGN KEY(normalized_fact_id) REFERENCES normalized_financial_facts (fact_id), 
	FOREIGN KEY(raw_fact_id) REFERENCES raw_financial_facts (raw_fact_id), 
	FOREIGN KEY(mapping_decision_id) REFERENCES mapping_decisions (mapping_decision_id)
)
COLUMNS:
  0 | input_id | INTEGER | notnull=1 | pk=1 | default=None
  1 | normalized_fact_id | INTEGER | notnull=1 | pk=0 | default=None
  2 | raw_fact_id | INTEGER | notnull=1 | pk=0 | default=None
  3 | mapping_decision_id | INTEGER | notnull=1 | pk=0 | default=None
  4 | input_role | VARCHAR(20) | notnull=1 | pk=0 | default=None
FOREIGN KEYS:
  mapping_decision_id -> mapping_decisions.mapping_decision_id | on_update=NO ACTION | on_delete=NO ACTION
  raw_fact_id -> raw_financial_facts.raw_fact_id | on_update=NO ACTION | on_delete=NO ACTION
  normalized_fact_id -> normalized_financial_facts.fact_id | on_update=NO ACTION | on_delete=NO ACTION
INDEXES:
  sqlite_autoindex_normalized_financial_fact_inputs_1 | unique=1 | origin=u

----------------------------------------------------------------------
OBJECT: table | normalized_financial_facts | TABLE: normalized_financial_facts
DDL:
CREATE TABLE normalized_financial_facts (
	fact_id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	period_id INTEGER NOT NULL, 
	metric_id INTEGER NOT NULL, 
	raw_fact_id INTEGER, 
	mapping_decision_id INTEGER, 
	value_irr NUMERIC(30, 4), 
	source_report_version_id INTEGER NOT NULL, 
	normalization_rule_id INTEGER, 
	quality_status VARCHAR(20) NOT NULL, 
	PRIMARY KEY (fact_id), 
	CONSTRAINT uq_normalized_fact UNIQUE (company_id, period_id, metric_id, source_report_version_id), 
	CONSTRAINT chk_normalized_quality_status CHECK (quality_status IN ('VALID','MISSING','ESTIMATED','RESTATED','SUSPICIOUS','UNMAPPED')), 
	FOREIGN KEY(company_id) REFERENCES companies (company_id), 
	FOREIGN KEY(period_id) REFERENCES financial_periods (period_id), 
	FOREIGN KEY(metric_id) REFERENCES financial_metrics (metric_id), 
	FOREIGN KEY(raw_fact_id) REFERENCES raw_financial_facts (raw_fact_id), 
	FOREIGN KEY(mapping_decision_id) REFERENCES mapping_decisions (mapping_decision_id), 
	FOREIGN KEY(source_report_version_id) REFERENCES report_versions (report_version_id)
)
COLUMNS:
  0 | fact_id | INTEGER | notnull=1 | pk=1 | default=None
  1 | company_id | INTEGER | notnull=1 | pk=0 | default=None
  2 | period_id | INTEGER | notnull=1 | pk=0 | default=None
  3 | metric_id | INTEGER | notnull=1 | pk=0 | default=None
  4 | raw_fact_id | INTEGER | notnull=0 | pk=0 | default=None
  5 | mapping_decision_id | INTEGER | notnull=0 | pk=0 | default=None
  6 | value_irr | NUMERIC(30, 4) | notnull=0 | pk=0 | default=None
  7 | source_report_version_id | INTEGER | notnull=1 | pk=0 | default=None
  8 | normalization_rule_id | INTEGER | notnull=0 | pk=0 | default=None
  9 | quality_status | VARCHAR(20) | notnull=1 | pk=0 | default=None
FOREIGN KEYS:
  source_report_version_id -> report_versions.report_version_id | on_update=NO ACTION | on_delete=NO ACTION
  mapping_decision_id -> mapping_decisions.mapping_decision_id | on_update=NO ACTION | on_delete=NO ACTION
  raw_fact_id -> raw_financial_facts.raw_fact_id | on_update=NO ACTION | on_delete=NO ACTION
  metric_id -> financial_metrics.metric_id | on_update=NO ACTION | on_delete=NO ACTION
  period_id -> financial_periods.period_id | on_update=NO ACTION | on_delete=NO ACTION
  company_id -> companies.company_id | on_update=NO ACTION | on_delete=NO ACTION
INDEXES:
  sqlite_autoindex_normalized_financial_facts_1 | unique=1 | origin=u

----------------------------------------------------------------------
OBJECT: table | raw_financial_facts | TABLE: raw_financial_facts
DDL:
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
COLUMNS:
  0 | raw_fact_id | INTEGER | notnull=1 | pk=1 | default=None
  1 | company_id | INTEGER | notnull=1 | pk=0 | default=None
  2 | report_version_id | INTEGER | notnull=1 | pk=0 | default=None
  3 | period_id | INTEGER | notnull=1 | pk=0 | default=None
  4 | raw_item_name | VARCHAR(300) | notnull=1 | pk=0 | default=None
  5 | raw_item_code | VARCHAR(100) | notnull=0 | pk=0 | default=None
  6 | value | NUMERIC(30, 4) | notnull=0 | pk=0 | default=None
  7 | unit | VARCHAR(50) | notnull=0 | pk=0 | default=None
  8 | currency | VARCHAR(20) | notnull=0 | pk=0 | default=None
  9 | source_section | VARCHAR(150) | notnull=0 | pk=0 | default=None
  10 | source_row | INTEGER | notnull=0 | pk=0 | default=None
  11 | source_column | VARCHAR(100) | notnull=0 | pk=0 | default=None
  12 | source_sheet | VARCHAR(150) | notnull=0 | pk=0 | default=None
  13 | source_column_header | VARCHAR(300) | notnull=0 | pk=0 | default=None
FOREIGN KEYS:
  period_id -> financial_periods.period_id | on_update=NO ACTION | on_delete=NO ACTION
  report_version_id -> report_versions.report_version_id | on_update=NO ACTION | on_delete=NO ACTION
  company_id -> companies.company_id | on_update=NO ACTION | on_delete=NO ACTION
INDEXES:

----------------------------------------------------------------------
OBJECT: table | report_versions | TABLE: report_versions
DDL:
CREATE TABLE report_versions (
	report_version_id INTEGER NOT NULL, 
	report_id INTEGER NOT NULL, 
	version_number INTEGER NOT NULL, 
	publication_datetime DATETIME NOT NULL, 
	is_current_version BOOLEAN NOT NULL, 
	is_restated BOOLEAN NOT NULL, 
	supersedes_version_id INTEGER, 
	created_at DATETIME, 
	PRIMARY KEY (report_version_id), 
	CONSTRAINT uq_report_version UNIQUE (report_id, version_number), 
	FOREIGN KEY(report_id) REFERENCES reports (report_id), 
	FOREIGN KEY(supersedes_version_id) REFERENCES report_versions (report_version_id)
)
COLUMNS:
  0 | report_version_id | INTEGER | notnull=1 | pk=1 | default=None
  1 | report_id | INTEGER | notnull=1 | pk=0 | default=None
  2 | version_number | INTEGER | notnull=1 | pk=0 | default=None
  3 | publication_datetime | DATETIME | notnull=1 | pk=0 | default=None
  4 | is_current_version | BOOLEAN | notnull=1 | pk=0 | default=None
  5 | is_restated | BOOLEAN | notnull=1 | pk=0 | default=None
  6 | supersedes_version_id | INTEGER | notnull=0 | pk=0 | default=None
  7 | created_at | DATETIME | notnull=0 | pk=0 | default=None
FOREIGN KEYS:
  supersedes_version_id -> report_versions.report_version_id | on_update=NO ACTION | on_delete=NO ACTION
  report_id -> reports.report_id | on_update=NO ACTION | on_delete=NO ACTION
INDEXES:
  uq_report_current_version | unique=1 | origin=c
  sqlite_autoindex_report_versions_1 | unique=1 | origin=u

----------------------------------------------------------------------
OBJECT: table | reports | TABLE: reports
DDL:
CREATE TABLE reports (
	report_id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	report_type VARCHAR(100) NOT NULL, 
	codal_tracking_id VARCHAR(100), 
	title VARCHAR(300) NOT NULL, 
	financial_period_id INTEGER NOT NULL, 
	source_url VARCHAR(500), 
	original_report_id INTEGER, 
	is_correction BOOLEAN NOT NULL, 
	created_at DATETIME, 
	PRIMARY KEY (report_id), 
	FOREIGN KEY(company_id) REFERENCES companies (company_id), 
	UNIQUE (codal_tracking_id), 
	FOREIGN KEY(financial_period_id) REFERENCES financial_periods (period_id), 
	FOREIGN KEY(original_report_id) REFERENCES reports (report_id)
)
COLUMNS:
  0 | report_id | INTEGER | notnull=1 | pk=1 | default=None
  1 | company_id | INTEGER | notnull=1 | pk=0 | default=None
  2 | report_type | VARCHAR(100) | notnull=1 | pk=0 | default=None
  3 | codal_tracking_id | VARCHAR(100) | notnull=0 | pk=0 | default=None
  4 | title | VARCHAR(300) | notnull=1 | pk=0 | default=None
  5 | financial_period_id | INTEGER | notnull=1 | pk=0 | default=None
  6 | source_url | VARCHAR(500) | notnull=0 | pk=0 | default=None
  7 | original_report_id | INTEGER | notnull=0 | pk=0 | default=None
  8 | is_correction | BOOLEAN | notnull=1 | pk=0 | default=None
  9 | created_at | DATETIME | notnull=0 | pk=0 | default=None
FOREIGN KEYS:
  original_report_id -> reports.report_id | on_update=NO ACTION | on_delete=NO ACTION
  financial_period_id -> financial_periods.period_id | on_update=NO ACTION | on_delete=NO ACTION
  company_id -> companies.company_id | on_update=NO ACTION | on_delete=NO ACTION
INDEXES:
  sqlite_autoindex_reports_1 | unique=1 | origin=u

----------------------------------------------------------------------
OBJECT: table | schema_migrations | TABLE: schema_migrations
DDL:
CREATE TABLE schema_migrations (version INTEGER PRIMARY KEY, name VARCHAR(200) NOT NULL, applied_at DATETIME NOT NULL)
COLUMNS:
  0 | version | INTEGER | notnull=0 | pk=1 | default=None
  1 | name | VARCHAR(200) | notnull=1 | pk=0 | default=None
  2 | applied_at | DATETIME | notnull=1 | pk=0 | default=None
FOREIGN KEYS:
INDEXES:

----------------------------------------------------------------------
OBJECT: table | share_count_history | TABLE: share_count_history
DDL:
CREATE TABLE share_count_history (
	share_history_id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	effective_date DATE NOT NULL, 
	shares_outstanding INTEGER NOT NULL, 
	capital NUMERIC(24, 2) NOT NULL, 
	source VARCHAR(100), 
	PRIMARY KEY (share_history_id), 
	CONSTRAINT uq_company_share_date UNIQUE (company_id, effective_date), 
	FOREIGN KEY(company_id) REFERENCES companies (company_id)
)
COLUMNS:
  0 | share_history_id | INTEGER | notnull=1 | pk=1 | default=None
  1 | company_id | INTEGER | notnull=1 | pk=0 | default=None
  2 | effective_date | DATE | notnull=1 | pk=0 | default=None
  3 | shares_outstanding | INTEGER | notnull=1 | pk=0 | default=None
  4 | capital | NUMERIC(24, 2) | notnull=1 | pk=0 | default=None
  5 | source | VARCHAR(100) | notnull=0 | pk=0 | default=None
FOREIGN KEYS:
  company_id -> companies.company_id | on_update=NO ACTION | on_delete=NO ACTION
INDEXES:
  sqlite_autoindex_share_count_history_1 | unique=1 | origin=u

MIGRATION HISTORY:
1 | baseline_schema | 2026-11-07 11:15:33.002433
2 | mapping_and_derived_schema | 2026-11-07 11:15:33.284333
3 | normalized_fact_multi_source_provenance | 2026-11-07 11:15:33.552182
4 | one_current_report_version | 2026-11-07 11:15:33.861452
5 | market_daily_jalali_components | 2026-11-07 11:15:34.147308
6 | fx_rates_jalali_components | 2026-11-07 11:15:34.434280
7 | forecast_version_repository | 2026-11-07 11:15:35.767386
8 | remove_forecast_output_persistence | 2026-11-07 11:15:36.573913
9 | codal_excel_source_metadata | 2026-11-07 11:15:36.865524

================================================================================
END OF AUDIT
================================================================================
Read-only audit. No database rows or project source files changed.