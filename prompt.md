# P62 — Define the Minimal Production Integration Contract for Stage 7



This is a financial-data application. Financial correctness, auditability, point-in-time correctness, deterministic behavior, and preservation of financial invariants take priority over speed or superficial test success.

## Task type

**ANALYSIS / DESIGN REPORT ONLY.**

Do not modify application code, tests, specifications, or project-planning files. Do not run tests or CI. The user will run tests personally.

## Mandatory operating constraints

- Work only within the local `analyzer` project.
- No GitHub, GitHub CLI/API, remote operations, commits, pushes, pulls, branch changes, or other repository synchronization.
- Do not perform a broad repository exploration. Read the specific files identified below and follow only directly relevant references.
- Do not redesign `src/valuation/engine.py`.
- Do not invent financial formulas, data sources, industry mappings, date semantics, persistence contracts, or point-in-time guarantees.
- Do not create an orchestrator, integration test, or synthetic execution path during this task.
- Do not edit `reply.md`, `temp_report.md`, `temp_report2.md`, `stepsForStage7.md`, `stage_7_prompts.md`, or anything under `ClaudeReports/`.
- Return the complete report in your Claude response. The user will decide what to preserve or append.

## Step 1 — Read the authoritative plan and prior findings

Read `stepsForStage7.md` first, especially the P48 audit findings dated 2026-10-25 and the remaining execution plan.

Use only the relevant earlier findings in `temp_report2.md` to clarify existing conclusions about:
- production-path and integration audits, including P38/P48 if present;
- parameter-selection and point-in-time constraints, including P54;
- scenario-dispersion threshold policy, P61/P61-R.

Do not repeat earlier investigations unless needed to resolve a specific contradiction. Treat the latest P48 findings in `stepsForStage7.md` as the current working baseline.

## Step 2 — Inspect only the minimum necessary implementation files

Start with these files:

- `src/scoring/engine.py`
- `src/forecast/service.py`
- `src/forecast/schema.py`
- `src/forecast/repo.py`
- `src/valuation/service.py`
- `src/valuation/schema.py`
- `src/decision/service.py`
- `src/decision/schema.py`
- `src/market/engine.py`
- `src/market/schema.py`
- `src/core/database.py`
- the market-data query/ingestion modules directly used by the services above
- the corresponding model files only where needed to verify existing persistence contracts

Inspect a caller, configuration, or model outside this list only when a specific symbol reference or direct dependency requires it. Record why that additional file was necessary.

Do not read the entire test suite. You may inspect a small, directly relevant test only to understand an existing contract. Do not run it.

## Step 3 — Define the minimal integration contract

For each boundary below, establish the existing contract and the missing information required to connect it safely:

1. **Stage 3 → downstream stages**
   - What produces `FundamentalScoreResult`?
   - What exact identity and period fields must match?
   - Are actual `KPIResult` production and aggregation connected to a caller, or is only the scoring engine present?

2. **Stage 5 Forecast production/retrieval**
   - What function produces `CompanyForecastResult`?
   - What data and cutoff does it require?
   - What persistence/retrieval capability already exists?
   - Is there an authoritative way to select the intended forecast version for a historical analysis date?
   - Do not treat model version alone as complete historical parameter versioning.

3. **Stage 7 Valuation**
   - What inputs does `calculate_valuation_as_of_jalali` require?
   - How is the Jalali analysis date supplied?
   - Which price observation is selected and what provenance is preserved?
   - What remains unavailable for full point-in-time verification?

4. **Stage 8 Market analysis**
   - What input shape does `MarketEngine.analyze_market` require?
   - What existing source or query can supply that input?
   - Can the market signal be produced using data eligible as of the same analysis date?
   - Do not assume that the Stage 7 market-price query also supplies all Stage 8 inputs.

5. **Stage 9 Decision**
   - What inputs are required by `calculate_decision_as_of_jalali`?
   - What identity checks already exist?
   - What does it return?
   - Is there an existing authoritative persistence or consumption contract for the final decision?

6. **Shared execution context**
   - Who should own/create/close the SQLAlchemy `Session`, based on existing conventions?
   - What explicit date values must be passed across boundaries?
   - Keep the Persian Jalali calendar as the relevant analysis-date convention. Do not introduce Gregorian-date conversion unless an existing contract explicitly requires it.
   - Distinguish forecast `data_cutoff_datetime`, Jalali market analysis date, calculation timestamp, and parameter-selection cutoff. They are not interchangeable.
   - Do not silently substitute the current date or `valuation_date` for a missing historical cutoff.

## Step 4 — Produce a contract matrix

Return a concise table with one row per boundary and these columns:

- Boundary
- Existing function/interface
- Required inputs and identity invariants
- Output
- Existing persistence or retrieval
- Evidence of a real caller
- Missing contract or blocker
- Classification: `EXISTS AND CONNECTED`, `EXISTS BUT CALLER UNPROVEN`, or `MISSING/UNDEFINED`

Cite exact file paths and function/class names. Include line numbers when available, but do not invent line numbers.

A function existing in a module or being called by a unit test does not, by itself, prove a production execution path.

## Step 5 — Recommend the smallest safe next implementation task

Based on the evidence, recommend the smallest next task that would move the real application toward a verifiable execution path.

Your recommendation must:
- name the exact file/interface responsibility that should be addressed first;
- explain why it is the first dependency;
- list prerequisites and unresolved decisions;
- identify which existing contracts must remain unchanged;
- state what evidence would prove completion;
- specify the tests the user should run later, but **do not run them**;
- avoid designing a speculative database schema or adding new public APIs before confirming they are necessary.

If the available code does not identify a legitimate source or owner for an input, state that explicitly rather than inventing one.

Do not implement anything in P62. Do not declare Stage 7 complete.

## Required report structure

1. Executive conclusion
2. Evidence and contract matrix
3. Confirmed gaps versus unknowns
4. Minimal recommended implementation task
5. User-run validation plan
6. Files inspected and any additional files inspected, with reasons
7. Explicit statement confirming no code changes and no tests/CI executed

Return the report in your Claude response only. The user will review it before authorizing any implementation work.