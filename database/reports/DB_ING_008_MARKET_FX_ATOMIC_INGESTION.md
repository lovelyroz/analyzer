# DB-ING-008 — Market/FX Atomic Ingestion

**Status: PARTIAL.** Market and schema-supported FX ingestion now enforce whole-batch validation, atomic canonical writes, no overwrite, and sanitized failure auditing. EXCHANGE_CENTER persistence is blocked by the existing model constraint; Jalali concurrency uniqueness cannot be guaranteed without a schema migration.

## Implementation

- `src/ingestion/common/atomic.py` commits STARTED separately and durably. It commits FAILED after rollback in a separate transaction. Audit logs contain only controlled diagnostic codes and counts; raw payloads and exception strings are excluded.
- Market CSV ingestion validates all rows and company identities before staging any `MarketDaily`. An invalid row or conflicting key rejects the whole batch. Identical intra-batch and existing payloads are unchanged duplicates. A different payload for an existing Jalali key fails the batch without overwriting.
- FX DTO batches follow the same validation-before-write pattern. Rates are persisted as supplied by the adapter; persistence does not multiply by 10. Invalid rows or any conflict reject the whole batch.
- `Value` is a separate field. MarketDaily writes only `J-Date` identity, ticker-resolved company, `Close`, `Volume`, `No`, and `Value`; Open/High/Low/Final are not written.
- Ingestion result objects expose `records_duplicated` and `records_invalid`. The current `IngestionRun` schema has no dedicated columns for these two counts; they are written as explicit `duplicate_count` and `invalid_count` values in sanitized `error_log`. `records_updated` remains zero because replacement is prohibited.

## Schema and concurrency limitations

1. `FXRate` constraint `chk_fx_rate_type` and `VALID_FX_RATE_TYPES` do not include `EXCHANGE_CENTER`. The service rejects this feed with `SCHEMA_RATE_TYPE_UNSUPPORTED` before canonical writes. Supporting it requires an authorized schema/migration change; no constraint workaround was made.
2. MarketDaily uniqueness covers `(company_id, trade_date)` and FXRate uniqueness covers `(rate_date, currency_from, currency_to, rate_type)`. Jalali writes set the Gregorian date columns to NULL. These constraints therefore do not prevent duplicate Jalali keys under concurrent sessions. Application checks catch sequential replays/conflicts, but cannot claim a race-free uniqueness guarantee. A separately authorized Jalali uniqueness migration is required.
3. `IngestionRun` cannot store duplicate and invalid counts in separate typed fields without schema changes. Current results report them directly and audit `error_log` stores the counts; the legacy counters retain their existing semantics.
4. If both the STARTED audit commit and the fallback FAILED audit commit fail, no durable audit row can be guaranteed. The service raises a sanitized `IngestionAuditError` and has not written canonical data.

## Automated verification

The test suite uses isolated temporary SQLite files under pytest's temporary workspace, not the user's database. Coverage includes valid multirow batches, mixed-validity rejection, intra-batch and existing identical duplicates, intra-batch and existing conflicts, pending-write rollback, commit failure, audit failure, audit counts/status, FX adapter unit preservation, EXCHANGE_CENTER schema rejection, and two independent Sessions observing replay/conflict behavior.

Final verification command: `.\.venv\Scripts\python.exe -m pytest -q --basetemp .pytest_task035_final_20261120 src/tests/test_market_fx_atomic_ingestion.py src/tests/test_ingestion_ohlc.py src/tests/test_ingestion_fx.py src/tests/test_market_fx_adapters.py src/tests/test_market_fx_preflight.py` — **61 passed in 78.16s**.

## User acceptance

The owner may run the isolated acceptance fixture suite from the repository root:

```powershell
..\.venv\Scripts\python.exe -m pytest -q src/tests/test_market_fx_atomic_ingestion.py
```

This uses temporary test databases. It does not validate real-database Jalali concurrency or enable EXCHANGE_CENTER persistence.
