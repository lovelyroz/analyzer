# Stage 1 — Data Foundation & Data Model

## Execution Prompt

You are implementing Stage 1 of Analyzer V1. Read `00_a_Master_Architecture.md`, `01_Stage1_Data_Foundation.md`, and `10_Implementation_Status.md` before changing code.

Implement only the locked Stage 1 contract. Do not implement Stage 2+ analytics.

### Scope
Build the auditable data foundation for Codal financial reports, market OHLC, FX, share-count history, corporate actions, data quality, provenance, and ingestion tracking.

### Required model
Support these entities/contracts:
- Company
- Industry
- FinancialPeriod, including derived TTM
- Report
- ReportVersion
- RawFinancialFact
- FinancialMetric
- NormalizedFinancialFact
- FXRate
- FXConversionRule
- MarketDaily
- ShareCountHistory
- CorporateAction
- IngestionRun

### Non-negotiable rules
- Raw facts are never destroyed or overwritten by normalization.
- `Report` and `ReportVersion` are distinct.
- Publication/availability time belongs to `ReportVersion`.
- Historical selection is Point-in-Time: only versions published on/before the cutoff are eligible.
- Restatements remain versioned; historical backtests use the version actually available at that time.
- `NULL != 0`.
- Financial base currency is IRR; USD is derived.
- Flow FX defaults to period-average FX; stock FX to period-end FX; market value to same-date FX.
- Free-market FX and operational/exchange FX remain distinct. Operational FX must never silently fall back to free-market FX.
- Close and adjusted close remain distinct.
- Historical share counts and corporate actions are preserved for EPS comparability.
- Data-quality states remain explicit: `VALID`, `MISSING`, `ESTIMATED`, `RESTATED`, `SUSPICIOUS`, `UNMAPPED`.
- Provenance must trace normalized facts back to source report/version, period, raw item, and normalization rule.
- TTM is derived, not a raw reporting period.

### Explicit exclusions
Do not add KPI scoring, Fundamental Score, forecasting, forecast evaluation, valuation, Market Score, trading signals, decision rules, or dashboard logic.

### Implementation method
1. Inspect the existing repository and reuse compatible structures.
2. Implement the smallest complete contract.
3. Add deterministic validation and constraints.
4. Add tests for normal cases, missing/zero values, restatements, PIT selection, provenance, FX conversion, share-count changes, and prohibited scope.
5. Run the full test suite.
6. Audit implementation against every Stage 1 requirement.
7. Fix the smallest responsible defect if anything fails.
8. Run the full suite again.
9. Verify actual CI evidence.
10. Report changed files, tests, CI run/job, and any non-blocking warnings.

Never silently invent source data, replace missing data, or weaken a correct contract to make tests pass.