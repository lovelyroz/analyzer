### 1. Mandatory context and exact access boundary

You may inspect ONLY the files explicitly listed below and actually provided to you.

**Required files:**

- `stepsForStage7.md`
- `reply.md`
- `07_Stage7_Valuation.md`
- `src/core/database.py`
- `src/decision/schema.py`
- `src/decision/engine.py`
- `src/decision/service.py`
- `src/valuation/service.py`
- `src/valuation/parameters.py`
- `src/forecast/service.py`
- `src/market/service.py`
- `src/tests/test_stage7_valuation.py`

**Additional files already provided, if any:** You may inspect them only when they are included in the files explicitly supplied for this task.

Do not assume that you have access to the entire repository or the entire `src/` directory.

If an important conclusion requires a file that is not in the supplied list:

1. Identify the exact missing file or files.
2. Explain which unresolved question each file would help answer.
3. State which conclusion cannot yet be verified.
4. Stop short of making claims that require the missing evidence.

Do not request broad access to the whole repository when a small, specific list of additional files would suffice.

### 2. S7-T001 — Production execution path

Use only the supplied files to trace the definitions and callers of the relevant Stage services.

For every conclusion, distinguish:
- Directly verified from supplied source
- Partially verified from supplied source
- Not verifiable because a required caller or entrypoint file was not supplied

A search across the supplied files is NOT proof that no production caller exists elsewhere in the repository.

Do not claim that a production entrypoint or caller is absent from the entire project unless the relevant project-wide evidence has actually been supplied and inspected.

### 3. S7-T002 — Stage 9 persistence

Inspect only the supplied database, decision, and model-related files.

If the available files do not include the relevant repositories, persistence services, model definitions, migrations, or application callers, list the exact missing files needed to verify persistence.

Do not conclude that persistence is absent from the entire project merely because it is absent from the supplied files.

Classify the finding as:
- `PRESENT` — a persistence path is directly evidenced
- `PARTIAL` — only part of the path is evidenced
- `NOT FOUND IN SUPPLIED FILES` — no path was found within the actual inspection boundary

### 4. S7-T005 — D1/D6 test interpretation

Inspect `src/tests/test_stage7_valuation.py` and the supplied implementation files only.

For each relevant test, identify its assertions and what those assertions logically establish. If an assertion depends on an implementation or specification file that was not supplied, identify that dependency and leave the conclusion unresolved.

Do not execute tests or infer runtime pass/fail status from their names.

### 5. Reporting and access limitations

In the final report, include:
- The exact files supplied and actually inspected
- Any supplied files that could not be inspected
- Additional files needed to resolve remaining questions
- Conclusions supported by the supplied evidence
- Conclusions that remain unverified because of access limitations


Do not run tests, application code, database commands, or Git commands. Do not perform remote GitHub operations, commits, pushes, pulls, or branch changes.