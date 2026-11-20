# DB-IMP-003 — Market/FX artifact preflight validator

**Status:** Implemented as a read-only artifact validator; this does not activate or certify feeds for production.

## Implementation

- Reusable module: `src/preflight/market_fx.py`.
- CLI: `python -m src.scripts.market_fx_preflight`.
- Tests: `src/tests/test_market_fx_preflight.py`.
- Usage: `docs/market_fx_preflight.md`.
- Sample output: `database/reports/market_fx_preflight_sample.json`.

The validator computes SHA-256, byte size, type, and Excel worksheet names. MarketDaily checks the approved date and numeric fields only, preserves `Value` independently, and requires an explicit stable company key to test economic keys. FX checks the approved Jalali date and sell-rate column only, preserves source cell coordinates and values, uses the approved `EXCHANGE_CENTER` USD/IRR identity, and performs no rate conversion. Both report source identity, publication identity, artifact identity, revision identity, and separate provenance timestamps. The tool makes no database connection and performs no ingestion.

## Current evidence and limitations

The checkout contains the two named artifacts. The FREE_MARKET file scan returned `BLOCKED_NO_SAMPLE`. CODAL and EXCHANGE_CENTER are owner-approved semantic identities, but publisher/profile linkage remains unverified. `source_published_at`, `source_available_at`, and revision identity are `UNKNOWN`; `ingested_at` is `NOT_INGESTED`. A missing stable company key blocks MarketDaily economic-key checks. A matching artifact hash does not establish publisher identity or revision order. Validation does not imply production readiness.

The validator does not infer FREE_MARKET structure, use `Final/Open/High/Low`, calculate `Volume × Close`, select a winning duplicate, use last-arrival-wins, or convert FX values. Identical duplicate economic rows are warnings; conflicting duplicates fail closed.

## Verification record

Executed `python -m pytest -q src/tests/test_market_fx_preflight.py`: **12 passed**. Executed the CLI against both repository artifacts; it returned the expected non-zero result because MarketDaily lacks a supplied stable company key and FREE_MARKET has no sample. The results were MarketDaily **BLOCKED** (21 CSV records), EXCHANGE_CENTER **WARNING** (19 observations, worksheet `Sheet`), FREE_MARKET **BLOCKED_NO_SAMPLE**, overall **BLOCKED**. JSON is in `database/reports/market_fx_preflight_sample.json`.

SHA-256 before and after the test/CLI run matched: `saman_price_history.csv` = `d94f27405f257b4010e1d2b7db4a554311484a6dde2b35a9c81c548f381c1413`; `dollar-history.xlsx` = `eb85250100438335accb06ca1fdf364304887a71e361258b93836d3a90dd6fcf`. No database connection or write occurred. `git diff --check` passed. Full CLI/run details are appended to `reply.md`.
