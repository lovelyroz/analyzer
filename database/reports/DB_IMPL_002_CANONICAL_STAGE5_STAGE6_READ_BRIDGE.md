# DB-IMPL-002 - Opt-in Canonical BANK Read Bridge for Stage 5/6

Date: 2026-11-22. Status: PARTIAL. No tests were executed and no database or migration was used.

## Delivered contract

`src/forecast/canonical_adapter.py` defines the caller-supplied `CanonicalMetricBinding` and Stage 5 adapter. The Stage 5 mapping must explicitly cover the four source keys actually consumed by the current service: `REVENUE`, `OPERATING_PROFIT`, `NET_PROFIT`, and `TOTAL_EQUITY`. Every binding declares company scope, metric ID, temporal type, exact unit/currency/scale, and dimension selection; the four monetary inputs must share a compatible unit/currency/scale contract, and YTD facts for a common end date must match the approved company fiscal-start month and share the same Jalali start date. The loader checks active company, fiscal-calendar, and selected BANK metric bindings/approvals before reading. Duration inputs must be YTD and must explicitly declare `duration_aggregation="ADDITIVE_YTD"`; no metric is guessed from a label or code. Instant facts retain their Jalali observation date. The adapter uses the existing runtime-only YTD quarter derivation, preserves exact integer source values in its result, and attaches report-version/publication references, including both cumulative versions behind a derived quarter. Missing/null facts remain missing at their latest Jalali period; an older quarter is not substituted when a newer report explicitly reports NULL.

`generate_forecast(..., canonical_metric_bindings=...)` is the explicit opt-in. Omitting the argument preserves the existing legacy path. Supplying it selects only the canonical reader; invalid/missing mappings or facts raise stable `CanonicalReadError` codes and never trigger legacy fallback. Nonempty `extra_facts` and a `share_count` override are rejected in this mode to prevent mixed financial sources. Stage 5 requires the approved company fiscal calendar and uses its month to validate YTD identities. The Stage 5 ordinal used internally to preserve Jalali sorting is explicitly not a database period ID. The Stage 6 result carries the exact canonical period ID for every selected input. The current canonical schema has no share-history bridge, so weighted shares remain missing in canonical mode; EPS from share-based forecast output may consequently remain unavailable. Stage 4 inputs remain a separate caller-provided boundary; when canonical latest revenue is missing, its run-rate field cannot fill that gap. Stage 5's existing numeric context conversion occurs only after fact metadata has matched the explicit contract; no unit, currency, scale, or Jalali-to-Gregorian conversion is performed by the adapter.

`src/kpi/canonical_adapter.py` defines the opt-in Stage 6 loader and adapter. It requires an explicit mapping for every input key consumed by the current BANK KPI inventory, with a caller-selected metric ID, temporal metadata, exact unit/currency/scale, dimensions, and Jalali report-end for each input. It rejects duplicate metric-period assignments, incompatible units for formula operands, mismatched same-period operands, reversed current/prior order, output-date mismatch, and cross-company rows. This permits explicitly mapped current/prior facts without guessing their economic identity. It reads `PERIODIC_FINANCIAL` only, checks the company is BANK, and validates every selected duration fact against the approved company fiscal-start month (including Jalali month-end and 3/6/9/12-month YTD length). It preserves integer values, each selected canonical period ID and report-version reference, and marks absent/null inputs missing rather than zero. Existing `KPIEngine` formulas are called unchanged; no calculated metric is stored. Caller supplies the runtime KPI output period ID and Jalali end explicitly.

`load_canonical_financial_facts()` gained an optional exact report-type filter; its existing PIT cutoff and version-quality selection remain intact. Neither default Stage 5 nor default Stage 6 behavior was switched.

## Tests added (not run)

- `src/tests/test_canonical_stage5_adapter.py`: `test_stage5_ytd_is_adapted_to_exact_runtime_quarters_with_lineage`, `test_stage5_rejects_incomplete_or_ambiguous_metric_mapping`, `test_stage5_rejects_unit_mismatch_and_does_not_guess_dimension`, `test_stage5_ignores_other_report_types_and_rejects_non_actual_scenarios`, `test_stage5_requires_explicit_additive_ytd_declaration`, `test_stage5_keeps_latest_reported_null_period_missing_instead_of_using_older_quarter`, `test_stage5_rejects_cross_company_fact_rows`, `test_stage5_rejects_inconsistent_units_and_ytd_period_starts`, `test_stage5_uses_configured_company_fiscal_start_month`, `test_generate_forecast_canonical_opt_in_never_reads_legacy_financial_facts`, and `test_generate_forecast_canonical_failure_does_not_fall_back_to_legacy`.
- `src/tests/test_canonical_stage6_adapter.py`: `test_stage6_maps_explicit_bank_inputs_and_preserves_missing_zero_and_lineage`, `test_stage6_rejects_incomplete_mapping_and_wrong_unit`, `test_stage6_rejects_cross_company_fact_rows`, `test_stage6_rejects_inconsistent_expected_units_and_periods`, `test_stage6_requires_ordered_growth_periods_and_current_output_period`, `test_stage6_does_not_accept_monthly_facts_or_guess_dimensions`, `test_stage6_validates_ytd_start_against_approved_fiscal_month`, and `test_stage6_opt_in_loader_is_bank_only_and_queries_periodic_pit_facts`.
- `src/tests/test_canonical_writer.py`: `test_canonical_read_query_supports_explicit_report_type_filter` and `test_stage5_loader_requires_approved_company_calendar_and_metric_bindings`.

Existing PIT/version-ranking tests in `src/tests/test_canonical_writer.py`, Stage 5 behavior tests, and Stage 2 KPI formula tests should also be run by the owner.

## Owner validation commands

Focused adapter, canonical-query, and consumer suites:

```powershell
.\.venv\Scripts\python.exe -m pytest -q --basetemp .pytest_db_impl_002_bridge_20261122 src/tests/test_canonical_stage5_adapter.py src/tests/test_canonical_stage6_adapter.py src/tests/test_canonical_queries.py src/tests/test_canonical_writer.py src/tests/test_stage5_forecast.py src/tests/test_stage2_kpis.py
```

Broader Stage 5/6 regression suite:

```powershell
.\.venv\Scripts\python.exe -m pytest -q --basetemp .pytest_db_impl_002_bridge_regression_20261122 src/tests/test_canonical_stage5_adapter.py src/tests/test_canonical_stage6_adapter.py src/tests/test_canonical_queries.py src/tests/test_canonical_writer.py src/tests/test_stage5_forecast.py src/tests/test_stage2_kpis.py src/tests/test_stage6_p25_selection.py src/tests/test_stage6_p25_adversarial.py src/tests/test_stage6_production_pipeline.py src/tests/test_stage6_scenario_isolation.py src/tests/test_stage6_evaluation_foundation.py
```

## Remaining gates

DB-IMPL-002 remains PARTIAL pending owner execution of these suites and review of real caller-provided BANK metric bindings. No production metric mapping is included. Canonical share-count history is not yet available to Stage 5. No change was made to `WORKFLOW_RULES.md`, schema, migrations, production mappings, or stored data.
