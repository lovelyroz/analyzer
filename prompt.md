# P68-B — Production Call-Path Verification and Orchestration Gap Audit

## Objective

Continue the Stage 7 architecture investigation in the local project folder `analyzer`.

P68-A-Fix confirmed that `src/ingestion/market/queries.py` contains `select_market_history_as_of(...)`. Do not reopen the already-resolved question of whether that query exists.

The remaining task is to determine, from actual source code, which inter-stage execution paths are implemented, which are only tested or intended, and which connections are genuinely missing.

This is a read-only investigation. No implementation is authorized.

## Restrictions

- Inspect the supplied project broadly; do not restrict yourself to a predetermined file list.
- Do not assume that `main.py` is the only possible entry point.
- Inspect actual Python entry points, application factories, API routes, CLI configuration, scheduled jobs, service modules, and orchestration functions wherever they exist.
- Do not modify or create files.
- Do not run tests, application code, database commands, migrations, or Git/GitHub operations.
- Do not redesign `src/valuation/engine.py`.
- Do not invent financial formulas, data sources, date conversions, historical dates, parameter effective dates, lookback windows, or missing contract fields.
- Do not treat a unit test, import, class definition, or service's existence as proof that the application invokes it in production.
- Use exact source paths, function names, and line numbers where available. If a claim cannot be established, explicitly mark it unverified.

## Required Investigation

### 1. Application Entry Points

Identify every plausible real application entry point found in the supplied project. For each, state its path, function or command, and what it actually invokes.

Do not conclude that no entry point exists merely because `main.py` is absent. If no end-to-end orchestration path is found after examining the relevant source, explain what you inspected and what evidence supports that conclusion.

### 2. Trace These Five Boundaries

For each boundary, trace the actual source-level caller → callee chain:

1. Stage 3 ingestion/fundamental outputs → Stage 5 forecast generation.
2. Stage 5 forecast/EPS → Stage 7 valuation.
3. Persisted market history → `select_market_history_as_of(...)` → any adapter/service → `MarketEngine.analyze_market(...)`.
4. Stage 7 valuation and Stage 8 market result → Stage 9 decision.
5. Stage 9 decision output → actual persistence, API response, CLI output, scheduled consumer, or other downstream consumer, if any.

For every boundary, report:

- Exact caller and callee paths and function names.
- Whether each connection is invoked by production code, exists only in tests, or is only documented/intended.
- The actual data passed across the boundary.
- Where company identity, reporting period, as-of date, and session ownership are established or preserved, where applicable.
- Explicitly enforced point-in-time constraints and any unverified assumptions.
- Direct evidence and remaining gaps.

### 3. Stage 8 Contract Verification

Using the existing `MarketHistoryObservation` and `select_market_history_as_of(...)` implementation, determine whether a production caller maps the returned Jalali-dated records into the exact input shape required by `MarketEngine.analyze_market`.

Do not assume a Gregorian conversion or invent a mapping rule. If the required date contract is undefined, document the exact incompatibility and the decision needed before implementation.

Do not recommend creating a second historical query unless source evidence proves that the existing query cannot satisfy a specific required contract.

### 4. Final Gap Register

List only gaps supported by source evidence. For each gap, state:

- Evidence and exact source locations.
- Missing connection or contract.
- Why it matters.
- What architectural decision is needed before implementation.
- Whether it blocks a safe next step.

Keep architectural gaps separate from financial-policy questions such as D9 historical parameter approval.

## Required Output

Return a concise report with:

1. Entry-point inventory.
2. Five-boundary call-path matrix.
3. Stage 8 data-contract conclusion.
4. Evidence-backed gap register.
5. One recommended next engineering step.
6. Final status: verified, partially verified, or not determinable from the supplied snapshot.

Do not implement fixes, write files, or run tests. Return the report in your response only.