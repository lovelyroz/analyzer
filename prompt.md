# P49 — Evidence-Based Data Source and Interface Mapping

You are continuing Stage 7 remediation in the local project folder `analyzer`.

## Objective

Following P48, determine which missing runtime inputs and interfaces can be supported by existing, authoritative project data and which are genuinely absent.

This is a targeted architecture and data-lineage investigation. Do not implement the runtime orchestration yet.

## Mandatory constraints

- Work only in the local `analyzer` project.
- Do not access GitHub, GitHub CLI/API, remotes, or perform any Git operations.
- Do not run tests or CI. The user runs tests.
- Do not inspect the entire repository indiscriminately. Follow only the source files and direct dependencies needed to establish each data path.
- Do not edit code, tests, dependencies, configuration, or reports.
- Do not edit `reply.md`, `temp_report.md`, `temp_report2.md`, `ClaudeReports/`, `stepsForStage7.md`, or `stage_7_prompts.md`.
- Do not redesign or centralize `engine.py`.
- Do not invent financial inputs, formulas, thresholds, industry mappings, benchmark values, publication timestamps, or historical parameter dates.
- Do not treat sample/debug data or unit-test fixtures as production data sources.
- Do not claim that a data source is authoritative unless the code and its provenance support that conclusion.

## Investigation scope

Start from the exact gaps identified by P48. Inspect only the relevant models, database queries, ingestion modules, schemas, and service contracts needed to establish the following.

### A. Stage 3 — Fundamental scoring

Determine:
- Which persisted financial records can supply the inputs required by the KPI and scoring engines.
- Whether existing queries can retrieve those records for a specific company and reporting period.
- Whether the source data is sufficient to produce the required KPI results without fabricated or inferred financial values.
- What is missing between persisted records and `FundamentalScoreResult`.

### B. Stage 4 and Stage 5 — Trend and forecast

Determine:
- Whether an existing authoritative source supplies the historical series required by `TrendEngine`.
- Whether the source can be filtered using a defensible evaluation cutoff.
- What existing interfaces can supply `TrendResult` to `generate_and_persist_forecast`.
- Whether the forecast service's current persistence and return contracts support downstream consumption without duplicating forecast calculations.

### C. Stage 8 — Market signal

Determine:
- How persisted `MarketDaily` records can be queried for the required evaluation date.
- Whether existing code can construct the exact inputs required by `MarketEngine`.
- Whether an authoritative benchmark source and compatible date contract actually exist.
- Which missing inputs cannot safely be supplied from the current repository.

Do not convert Jalali dates to Gregorian dates merely for convenience. Preserve existing date contracts unless concrete code evidence proves a necessary correction.

### D. Stage 7 and Stage 9 — Orchestration inputs and output

Using the existing services, establish:
- The required inputs and validation rules for `calculate_valuation_as_of_jalali` and `calculate_decision_as_of_jalali`.
- Which upstream results must be supplied by callers.
- What is already returned by `ValuationDecisionResult`.
- Whether any existing persistence model or consumer is suitable for the decision result. Do not assume that one exists.

### E. Shared execution contract

Identify the minimum contract a future runtime entry point would need:
- company and reporting-period identifiers;
- evaluation/as-of Jalali date and its legitimate source;
- SQLAlchemy session ownership and lifecycle;
- upstream result construction and validation;
- output delivery or persistence.

Separate existing, reusable interfaces from interfaces that would have to be introduced. Do not prescribe a new web API, CLI, scheduler, or user interface without repository evidence or an explicit product requirement.

## Required evidence standard

For every finding, use one of these statuses:

- `CONFIRMED`: directly supported by inspected code and call/data paths.
- `PARTIAL`: some required pieces exist, but the full path is not established.
- `MISSING`: the required source or interface was not found within the targeted inspection.
- `UNKNOWN`: evidence is insufficient to determine the answer.

Cite concrete file paths, functions/classes, relevant fields, and direct callers or queries. Distinguish persisted production data from fixtures, debug examples, and in-memory service inputs.

Do not interpret “not found” as proof that a capability is impossible. State the scope of each negative finding.

## Required final report

1. **Stage 3 data lineage:** source records → queries → KPI/scoring inputs → `FundamentalScoreResult`.
2. **Stage 4/5 data lineage:** historical source → `TrendResult` → forecast service → forecast consumer/persistence.
3. **Stage 8 data lineage:** `MarketDaily` and benchmark sources → `MarketEngine` inputs → `MarketSignalResult`.
4. **Stage 7/9 contract:** existing service inputs, validations, returned results, and any confirmed consumer/persistence path.
5. **Shared runtime contract:** session ownership, as-of date source, identifiers, output destination.
6. **Gap classification:** what can be reused, what is missing, and what remains unknown.
7. **Implementation readiness:** whether any real connection can be implemented without assumptions; identify the smallest safe next implementation unit, if supported by evidence.
8. **Files inspected:** exact list, with a brief reason for each.

Do not modify files or run tests. Finish the investigation and provide the complete report in the response. Do not stop at a generic blocker message.