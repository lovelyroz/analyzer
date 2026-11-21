# DB-IMPL-001 correction — 2026-11-21

Implemented and documented a focused correction:
- src/ingestion/canonical_writer.py: BANK periodic YTD alignment now applies only to exact report type PERIODIC_FINANCIAL; MONTHLY_ACTIVITY is excluded from this periodic-specific rule.
- src/tests/test_canonical_writer.py: added regression tests for monthly-activity two-month YTD acceptance and periodic-financial two-month YTD rejection.
- Rechecked the approved fiscal calendar decision: month only, day 1. No new day field or migration is needed.

No tests were run. No real database or migration was used. Full durable details are in database/reports/DB_IMPL_001_CANONICAL_DATABASE_AND_EXCEL_WRITER.md and Master Packet §9.47.