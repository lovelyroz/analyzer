# P67 — Stage 7 Bounded Implementation: Stage 8 Market Data Contract, Integration, and Regression Coverage

You are working on the local project folder `analyzer`, a financial-data application.

The attached ZIP is a curated evidence package. It contains the latest available `reply.md`, including the NotebookLM analysis, the Stage 7 roadmap, the valuation specification, relevant implementation files, and relevant tests.

## 1. Mandatory starting procedure

1. Read the complete `reply.md`, including the newly appended NotebookLM report and the P66 findings.
2. Read `stepsForStage7.md` and `07_Stage7_Valuation.md`.
3. Inspect the actual source and test files in the supplied package and, if available, the current local project folder `analyzer`.
4. Treat current source code and explicit project contracts as authoritative for implementation details. Use NotebookLM's report as an analysis aid, not as proof that a behavior exists.
5. If the package and working folder disagree, identify the discrepancy before editing. Do not silently overwrite newer user work.
6. Do not repeat earlier report-only investigations. Implement every independent, bounded correction supported by existing contracts and evidence.

If the working project folder is not accessible or a required source file is missing, state the exact limitation. Do not pretend to have edited files that you could not access.

## 2. Non-negotiable restrictions

- Financial correctness, auditability, point-in-time correctness, deterministic behavior, and preservation of financial invariants take precedence over convenience.
- Do NOT execute pytest, any test, application command, database migration, or other code-execution command. I will run the tests myself.
- Static inspection and editing are permitted. Provide exact PowerShell commands for me to execute later.
- Do not use Git, GitHub, GitHub CLI/API, branches, remotes, commits, pushes, or pulls.
- Do not redesign or broadly refactor `src/valuation/engine.py`. Its redesign remains the final technical step in the Stage 7 roadmap.
- Do not edit `stepsForStage7.md`, `07_Stage7_Valuation.md`, `reply.md`, `temp_report.md`, `temp_report2.md`, or other planning/report files. Provide the complete implementation report in your final response so I can decide where to record it.
- Do not remove, skip, weaken, or relax existing tests to obtain a pass.
- Do not invent schemas, database fields, financial formulas, thresholds, industry mappings, parameter values, effective dates, benchmark data, provenance, or rounding rules.
- Do not claim that tests passed, code ran successfully, or a production path was verified at runtime. No tests or application commands may be run in this task.

## 3. Evidence and constraints already established

Use these as leads and verify them against the supplied files:

- `src/models/market.py` defines `MarketDaily`. Its date representation includes Jalali components, and `trade_date` may be nullable for legacy records.
- `src/ingestion/market/queries.py` contains the existing `JalaliDate` and `select_market_price_as_of` query path used by Stage 7. Do not assume that a query selecting one price observation can supply the historical OHLCV sequence required by Stage 8.
- `src/market/engine.py` accepts prepared market data and an as-of date. Establish its exact input contract from the actual code and tests.
- `src/valuation/service.py` selects a market-price observation for Stage 7 valuation.
- `src/decision/service.py` accepts a forecast result, a fundamental result, and a market result; its existence does not prove that a real caller produces all three correctly.
- Previous audits did not establish a complete, real production path from Stages 3 and 5 through Stage 7, Stage 8, and Stage 9.
- Stage 8 has not yet been shown to have an existing database query/service that supplies its required historical market-data sequence.
- Stage 5 EPS must remain authoritative. Stage 7 must not recalculate EPS or introduce a replacement share-count calculation.
- The project uses the Persian/Jalali calendar for the relevant market-date workflow. Do not introduce a Gregorian-calendar requirement where the existing contract does not require one.
- D9 remains OPEN. The current parameter values have not been formally ratified, and the Genesis parameter set has no approved `effective_from` timestamp. Do not invent one or silently enable dated selection by assigning an arbitrary date.
- Requests for dated parameter selection without an eligible dated version must retain the existing fail-closed behavior.
- Preserve the scenario-dispersion threshold `0.50` and its strict `>` comparison semantics.
- D1–D4 and D6 contain unresolved policy or input-contract gaps. Implement only behavior supported by an explicit existing contract; do not fabricate alert triggers, sector-specific formulas, or missing inputs.
- Keep `review_priority` distinct from risk alerts.
- `engine.py` redesign is the last technical step, not part of this task.

## 4. Workstream A — Establish the actual Stage 8 market-data contract

Inspect the following files together:

- `src/models/market.py`
- `src/ingestion/market/queries.py`
- `src/market/engine.py`
- `src/market/schema.py`
- `src/market/indicators.py`
- `src/market/parameters.py`
- `src/tests/test_stage8_market.py`
- `src/valuation/service.py`
- `src/decision/service.py`

Determine and document from the actual code:

1. The precise data shape and required fields accepted by `MarketEngine.analyze_market`.
2. The ordering, date semantics, and minimum history requirements, if explicitly defined.
3. The available `MarketDaily` fields and whether they can support the engine's required inputs without fabricated values.
4. Whether existing query functions can retrieve the necessary ordered historical observations for a company, bounded by the requested as-of date.
5. Whether the existing Jalali date representation supports a reliable as-of filter for the complete history.
6. How the resulting `MarketSignalResult` is supposed to reach Stage 9.
7. Which caller, query, service, or contract is actually missing.

Do not treat Stage 7's single-price selection query as proof of a valid Stage 8 historical-series source.

## 5. Workstream B — Implement the smallest safe Stage 8 connection when justified

If the existing model, query conventions, engine contract, and tests provide sufficient evidence, implement the smallest coherent production connection that retrieves historical market observations and supplies them to Stage 8.

Requirements:

- Reuse the established data model and query conventions where appropriate.
- Respect the as-of boundary: future observations must not leak into historical analysis.
- Preserve the existing Jalali date workflow and deterministic ordering.
- Do not substitute missing OHLCV fields with zero or fabricated observations.
- Do not invent a lookback window, indicator formula, fallback policy, or minimum observation count.
- Do not create a speculative schema, orchestration layer, or application entry point.
- Do not modify frozen upstream stages without explicit authorization.
- Add focused regression tests for the supported contract, including future-data exclusion and missing or insufficient data where those behaviors are defined.
- If a required policy or input is missing, complete every separable safe correction and report the exact blocker. Do not build a guessed service merely because a report suggested a possible filename.

If a new file such as `src/market/service.py` is justified, implement it only after confirming that the existing architecture and contracts support it.

## 6. Workstream C — Verify the Stage 7/8/9 interface

Inspect:

- `src/valuation/service.py`
- `src/valuation/schema.py`
- `src/decision/service.py`
- `src/decision/engine.py`
- `src/decision/schema.py`
- `src/tests/test_stage7_valuation.py`
- `src/tests/test_stage8_market.py`
- `src/tests/test_stage9_decision.py`

Verify that:

1. Stage 7 receives the existing Stage 5 forecast and preserves its EPS.
2. Stage 8 market results conform to the actual Stage 9 input contract.
3. Company identity, period identity, and date/as-of consistency are checked where required by existing contracts.
4. Missing market evidence cannot be misrepresented as valid market analysis.
5. The interfaces do not silently discard required metadata or provenance.
6. Any new integration test exercises the real service path, not only a private helper or a manually constructed result.
7. No test is treated as proof of production integration unless it actually exercises that integration.

Fix clear, contract-supported defects. Do not create an application-wide orchestration system or final-decision persistence model without an established contract.

## 7. Workstream D — Verify D1–D6 and related regression coverage

Use `reply.md`, the specification, and actual source/tests to verify the current status of D1–D6.

- D1: Do not emit an assessment-flip alert without a valid, defined criterion.
- D2: Do not activate an unwired or undefined multiple-dependence metric.
- D3: Preserve the authoritative Stage 5 EPS; do not recalculate it.
- D4: Do not emit margin-assumption risk without valid required inputs.
- D5: Keep review priority separate from risk alerts.
- D6: Do not invent bank, holding-company, or other sector-specific formulas without approved input and formula contracts.

Implement missing regression tests or corrections only where expected behavior is explicit and demonstrable from the existing specification. Do not force previously failing tests to pass by changing their expected assertions to match unsupported behavior.

If a test expects behavior that is not authorized by the current contract, preserve the test and explain precisely what policy or upstream contract is missing.

## 8. Workstream E — Parameter and PIT safeguards

Inspect `src/valuation/parameters.py`, `src/valuation/engine.py`, `src/valuation/service.py`, and the relevant tests.

Make only bounded, independently justified corrections. Confirm that:

- A dated parameter request cannot silently fall back to undated Genesis constants.
- No unapproved `effective_from` timestamp is introduced.
- No claim of complete PIT correctness is made without the required authoritative dates and provenance.
- The audit metadata does not claim that historical parameter selection occurred when it did not.
- No parameter values or financial thresholds are changed without approved evidence.

Do not attempt to resolve owner-controlled D9 decisions in code. Do not make the final `engine.py` redesign part of this workstream.

## 9. Final static review

Without executing code or tests:

1. Review every changed source file and test.
2. Check imports, type consistency, interface compatibility, missing-data behavior, as-of boundaries, and unintended changes to frozen contracts.
3. Identify any test expectations that still need the owner's execution.
4. Separate implemented corrections from unimplemented blockers and owner decisions.
5. Do not claim runtime correctness from static review.

## 10. Required final response

Return a concise but complete implementation report containing:

1. **Files changed:** exact paths and a summary of each change.
2. **Stage 8 contract:** actual accepted input shape, available database fields, date semantics, and any confirmed limitations.
3. **Integration status:** which real service/query path is now connected, or the exact reason a safe connection could not be completed.
4. **Regression coverage:** tests added or changed and the behavior each is intended to protect.
5. **D1–D6 and PIT/D9:** what was safely corrected, what remains open, and why.
6. **Static-review findings:** remaining compatibility or correctness concerns.
7. **Owner-run PowerShell commands:** exact commands I should execute, starting with the focused tests and then the relevant Stage 7/8/9 suites. Do not execute them.
8. **Next step:** identify the highest-priority remaining action in `stepsForStage7.md`. Keep the final `engine.py` redesign deferred until its designated last step.

Do not declare Stage 7 complete or frozen. Do not claim any test passed. The user will run tests and provide the actual output before the next implementation batch.