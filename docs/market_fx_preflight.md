# Market/FX file adapter preflight

Run from the repository root:

```powershell
.\.venv\Scripts\python.exe -m src.scripts.market_fx_preflight --root . --market saman_price_history.csv --fx dollar-history.xlsx --fx-rate-type EXCHANGE_CENTER --json-out database/reports/market_fx_preflight_acceptance.json
```

The CLI reads files only. It does not connect to a database or ingest rows. Exit code 1 means at least one input failed validation; warnings about provenance may still accompany structurally valid files. `--fx-rate-type` is required when interpreting a workbook: `EXCHANGE_CENTER` preserves Rial values; `FREE_MARKET` multiplies Toman sell values by exactly 10. Both use the same header-detecting parser. The parser searches worksheets and rows for a Jalali date header and a sell header, and never maps the buy column. Invalid dates, invalid sell values, duplicate dates, conflicting payloads, and missing mappings are reported as diagnostics.

MarketDaily maps only `J-Date`, `Ticker`, `Close`, `Volume`, `No`, and `Value`. Source columns `Open`, `High`, `Low`, and `Final` are ignored. `Volume` and `No` must be integer-valued; all numeric fields must be finite. Duplicate approved headers, malformed rows, and duplicate economic keys are reported without selecting a winner. `Value` is validated and retained as supplied; it is never calculated from `Volume × Close`.

The FREE_MARKET conversion can be verified independently using the isolated workbook fixture tests:

```powershell
.\.venv\Scripts\python.exe -m pytest -q src/tests/test_market_fx_adapters.py
```

The fixture includes separate buy and sell values, an offset header row, and verifies `100 Toman → 1000 Rial`. This is a parser test, not user acceptance of a production workbook. Source publication/availability times and revision identities remain `UNKNOWN`; a successful preflight is not evidence of production readiness.
