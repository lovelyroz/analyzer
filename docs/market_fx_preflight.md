# Market/FX artifact preflight

Run from the repository root:

```powershell
python -m src.scripts.market_fx_preflight --market saman_price_history.csv --fx dollar-history.xlsx --json-out database/reports/market_fx_preflight_sample.json
```

The command reads files only and does not import database modules, open a database, or ingest rows. Relative paths resolve from the repository root by default; `--root` selects a different root for relative inputs and the FREE_MARKET sample scan. It prints a short status for each feed and writes a JSON report. A FAIL or BLOCKED result returns exit code 1. The CSV `Ticker` field supplies `codal_symbol` when it is present, non-empty, and consistent across all records. Company name is never used as the economic key. If symbol identity cannot be resolved, only economic-key checks are blocked; row structure, Jalali dates, and available numeric fields are still checked.

The MarketDaily allowlist is `J-Date`, `Close`, `Volume`, `No`, and `Value`; `Value` is checked and preserved as its own input. The validator does not map `Final`, `Open`, `High`, or `Low`. For FX it locates the approved date and sell-rate headers, reports the original cell addresses and values, and checks USD/IRR `EXCHANGE_CENTER` rates without converting them. It does not guess mappings when headers are missing.

`source_published_at`, `source_available_at`, and `ingested_at` are independent fields. Missing source evidence is `UNKNOWN`; this preflight does not ingest, so `ingested_at` is `NOT_INGESTED`. SHA-256 proves byte equality only. Successful structural checks do not establish publisher linkage, revision ordering, point-in-time availability, or production readiness. The FREE_MARKET scan reports `BLOCKED_NO_SAMPLE` when no actual sample file exists; no schema is inferred.

Tests: `pytest -q src/tests/test_market_fx_preflight.py` (temporary fixtures only).
