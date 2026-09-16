# Stage 1 — Data Foundation & Data Model

## Execution Prompt

You are implementing or auditing Stage 1 of Analyzer V1. Read `00_a_Master_Architecture.md`, `01_Stage1_Data_Foundation.md`, `11_Database_Architecture_Stage1.md`, `12_Database_Architecture_V1.1.md`, and `10_Implementation_Status.md` before changing code.

Implement only the locked Stage 1/data-foundation contract. Do not implement Stage 2+ analytics.

### Scope
Build the auditable data foundation for Codal financial reports, heterogeneous source-line mapping, normalized and derived financial facts, market OHLC, FX, share-count history, corporate actions, data quality, provenance, Point-in-Time reconstruction, and ingestion tracking.

### Required model
Support these entities/contracts:
- Company
- Industry
- FinancialPeriod, including derived TTM
- Report
- ReportVersion
- RawFinancialFact
- FinancialMetric / standard concept catalog
- MappingRule
- MappingDecision
- NormalizedFinancialFact
- NormalizedFinancialFactInput for one-to-many raw-source provenance
- DerivedFinancialFact
- DerivedFinancialFactInput
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
- Mapping decisions are explicit, versioned, reviewable, and preserve confidence/status.
- A raw line may remain unmapped and visible without entering downstream analysis.
- Many raw lines may contribute to one standard concept. The normalized concept must retain all contributing raw facts through `NormalizedFinancialFactInput`; aggregate/component lines must not be blindly double-counted.
- Reported, normalized, and derived values remain distinguishable.
- Derived facts never overwrite reported/normalized facts and retain formula/version/cutoff/input provenance.
- A logical report has at most one current `ReportVersion`.
- TTM is derived, not a raw reporting period.

### Explicit exclusions
Do not add KPI scoring, Fundamental Score, forecasting, forecast evaluation, valuation, Market Score, trading signals, decision rules, or dashboard logic.

### Implementation method
1. Inspect the existing repository and all Stage 1/database architecture documents.
2. Identify any contradiction between the locked specification and the current schema/implementation before editing.
3. Implement the smallest complete contract.
4. Use versioned migrations for schema changes; `create_all()` is bootstrap-only for an empty database.
5. Add deterministic validation and database constraints.
6. Add tests for normal cases, missing/zero values, restatements, PIT selection, mapping ambiguity/unmapped data, multi-source provenance, raw immutability, reported-vs-derived distinction, FX conversion, share-count changes, migrations, single-current-version integrity, and prohibited scope.
7. Run the full test suite.
8. Audit implementation against every Stage 1 requirement and the database architecture.
9. Fix the smallest responsible defect if anything fails.
10. Run the full suite again.
11. Verify actual CI evidence.
12. Report changed files, migrations, tests, CI run/job, and any non-blocking warnings.

Never silently invent source data, replace missing data, weaken provenance, double-count aggregate/component lines, or weaken a correct contract to make tests pass.