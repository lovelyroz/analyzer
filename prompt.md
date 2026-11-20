# TASK 3 — IMPLEMENT MARKET/FX ARTIFACT PREFLIGHT VALIDATOR

## Objective

Implement a working, read-only preflight validation tool for the existing MarketDaily and FX source artifacts.

This is an implementation task, not an investigation or documentation-only task.

The deliverable must include executable code, automated tests, and a sample validation report.

## Scope

Inspect the existing repository structure and implement a validator for:

1. `saman_price_history.csv`
2. `dollar-history.xlsx`

Also inspect whether a FREE_MARKET sample exists. If it does not exist, report that feed as `BLOCKED_NO_SAMPLE`; do not fabricate a sample or infer its schema.

## Required implementation

Create a reusable validation module and a command-line entry point consistent with the project's existing language, architecture, and conventions.

The validator must:

### A. Artifact identity
- Resolve input paths safely.
- Calculate SHA-256.
- Record file size and file type.
- Record worksheet names for Excel files.
- Never modify, rename, or overwrite source artifacts.

### B. MarketDaily validation
- Inspect CSV headers and actual row structure.
- Validate the approved fields where present:
  - `J-Date`
  - `Close`
  - `Volume`
  - `No`
  - `Value`
- Validate Jalali date format without silently converting or changing the source value.
- Detect missing values, malformed numeric values, duplicate economic keys, and conflicting payloads for the same economic key.
- Preserve `Value` independently. Never replace it with `Volume × Close`.
- Do not introduce mappings for `Final`, `Open`, `High`, or `Low`.

### C. FX validation
- Inspect workbook sheets and actual headers.
- Validate the approved sell-rate mapping only.
- Validate Jalali date values and numeric sell rates.
- Preserve the original source values and row references.
- Detect duplicate economic keys and conflicting rates.
- Do not infer a buy/sell mapping beyond the approved sell-rate field.
- Do not multiply or divide rates unless the existing approved mapping explicitly requires it.

### D. Provenance checks
For every artifact, report these fields separately:
- `source_published_at`
- `source_available_at`
- `ingested_at`

Do not derive the first two from filesystem timestamps, file upload times, row dates, or Git timestamps.

If a timestamp is not evidenced, return `UNKNOWN`, not a guessed value.

Clearly distinguish:
- artifact identity,
- source identity,
- source publication identity,
- revision identity.

A matching SHA-256 proves byte equality only. It does not prove publisher identity or revision order.

### E. Validation result
Produce structured results with:
- `PASS`
- `WARNING`
- `FAIL`
- `BLOCKED`

The overall status must fail closed when required fields are missing, economic keys are invalid, or conflicting payloads cannot be resolved.

Do not invent a winning revision. Do not use last-arrival-wins.

## Tests

Write automated tests covering at least:

1. Valid MarketDaily input.
2. Missing required MarketDaily field.
3. Invalid Jalali date.
4. Invalid numeric value.
5. Duplicate identical economic key and payload.
6. Duplicate economic key with conflicting payload.
7. Valid FX workbook.
8. Missing FX sell-rate field.
9. Invalid FX date or rate.
10. Missing FREE_MARKET sample.
11. Unknown provenance timestamps.
12. SHA-256 stability and source-file immutability.

Use temporary test fixtures. Never modify the actual source artifacts during tests.

## CLI behavior

Provide a documented command that runs validation against the existing artifacts.

The command must:
- Run without opening a database connection.
- Perform no ingestion or database writes.
- Return a non-zero exit code when validation has FAIL or BLOCKED status.
- Produce a machine-readable JSON report.
- Produce a concise human-readable summary.

## Output files

Create:
1. The validator implementation.
2. Automated tests.
3. A usage document.
4. A sample JSON validation report.
5. `database/reports/DB_IMP_003_MARKET_FX_PREFLIGHT_VALIDATOR.md`

Append a concise completion entry to `reply.md`. Preserve all previous content.

## Restrictions

- Do not modify database schemas, ORM models, migrations, migration runners, or database records.
- Do not run ingestion.
- Do not modify source CSV/XLSX files.
- Do not fabricate missing provenance.
- Do not claim that validation success means a feed is production-ready.
- Do not change approved source mappings.
- Do not spend this task on prompt.md or Git reporting.
- Do not stop after writing a plan. Implement the code and tests.

## Completion criteria

This task is complete only when:
1. The implementation exists.
2. Automated tests execute and their actual results are reported.
3. The CLI runs against the available real artifacts.
4. The JSON report is generated.
5. Source artifact hashes before and after execution match.
6. No database connection or write occurred.
7. Known limitations and blocked feeds are explicitly reported.

If an implementation detail is genuinely blocked by missing project information, implement all independent parts and document the exact blocker. Do not replace implementation with another investigation report.