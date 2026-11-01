# Technical Maintenance — Timestamp and openpyxl
## Repository: `analyzer`

### GLOBAL RESTRICTIONS

This is a code-changing implementation task.

You must follow these rules:

1. Inspect only the files explicitly listed below. Do not perform repository-wide exploration.
2. Do not run tests, start test loops, or claim that tests passed. The user will execute all tests locally.
3. Do not perform Git operations, database operations, commits, pushes, or changes to remote state.
4. **`WORKFLOW_RULES.md` is exclusively controlled by ChatGPT. You must not edit, delete, rename, move, reformat, or otherwise modify it.**
5. **Do not edit `STAGE7_MASTER_WORKING_PACKET.md`.** Only ChatGPT may update its task statuses.
6. Do not modify unrelated files or broaden the scope silently.
7. Preserve all existing financial calculations, business logic, public interfaces, and data contracts.

### Explicit file scope

**Files permitted to change:**

- `src/ingestion/codal/ingestion.py`
- `src/kpi/universal.py`
- `src/kpi/conditional.py`
- `src/kpi/industry.py`
- `src/trend/engine.py`
- `src/tests/test_stage1_rules.py`
- `src/tests/test_stage2_kpis.py`
- `src/tests/test_stage4_trend.py`
- `src/tests/test_ingestion_fx.py`

**Read-only reference files:**

- `src/models/audit.py`
- `requirements.txt`
- `.github/workflows/tests.yml`
- `WORKFLOW_RULES.md`
- `STAGE7_MASTER_WORKING_PACKET.md`

If another file is essential, do not inspect or modify it without authorization. Report its exact path and explain why it is needed.

---

## Task 1 — 058 · S7-REMED-001
### Replace deprecated timestamps while preserving naive UTC

The audit identified 24 uses of `datetime.utcnow()` in the following files:

- `src/ingestion/codal/ingestion.py` — 1 occurrence
- `src/kpi/universal.py` — 11 occurrences
- `src/kpi/conditional.py` — 1 occurrence
- `src/kpi/industry.py` — 9 occurrences
- `src/trend/engine.py` — 1 occurrence
- `src/tests/test_stage1_rules.py` — 1 occurrence
- `src/tests/test_stage2_kpis.py` — 1 occurrence
- `src/tests/test_stage4_trend.py` — 1 occurrence

#### 1.1 Inspect before changing

Inspect the existing timestamp construction, imports, and test clock mechanisms in the permitted files.

Determine whether a shared helper already exists in an appropriate architectural layer. Do not introduce a dependency on `src/models/audit.py` into higher-level application modules merely to reuse its helper.

If no suitable shared helper is available within the authorized files, prefer a direct standard-library implementation that preserves the existing contract, such as:

`datetime.now(timezone.utc).replace(tzinfo=None)`

Use the appropriate imports and adapt the expression to each file's existing structure.

Do not create a new shared helper in an unapproved file.

#### 1.2 Required implementation

- Replace all 24 identified `datetime.utcnow()` occurrences.
- Preserve the existing **naive UTC** output contract.
- Ensure timestamps represent UTC, not local machine time.
- Repair the Trend freeze-clock test to work with the replacement clock API.
- Add or strengthen regression tests for the naive UTC contract in the relevant Audit, KPI, and Trend paths.
- Keep timestamps deterministic in tests wherever a controlled clock is currently used.

#### 1.3 Strict invariants

- Do not convert outputs to timezone-aware datetimes.
- Do not change database timestamp contracts or serialization behavior.
- Do not change KPI formulas, financial calculations, or Trend behavior.
- Do not suppress or filter deprecation warnings as a substitute for fixing the calls.
- Do not change unrelated date/calendar logic. The project's financial date logic remains Jalali.

#### 1.4 Acceptance criteria

This task can be reported DONE only when:

1. All 24 targeted `datetime.utcnow()` occurrences have been replaced.
2. No targeted occurrence remains in the listed files.
3. Produced timestamps remain naive UTC.
4. Regression tests explicitly protect the naive UTC contract.
5. Trend's controlled-clock test remains deterministic and valid.
6. No financial calculation or unrelated behavior was changed.

---

## Task 2 — 059 · S7-REMED-002
### Make openpyxl a clearly enforced required dependency in the XLSX test

The project declares `openpyxl` in `requirements.txt`, and `.github/workflows/tests.yml` installs project requirements. However, `src/tests/test_ingestion_fx.py` currently uses `pytest.importorskip("openpyxl")`, which can silently skip an XLSX test when the required dependency is missing.

#### 2.1 Required implementation

Modify only:

`src/tests/test_ingestion_fx.py`

Replace the optional-skip behavior with an explicit required-dependency behavior.

The XLSX test must not silently skip when `openpyxl` is unavailable. Missing `openpyxl` must produce a clear dependency/import failure.

Keep the real XLSX test and its existing assertions. Do not delete, weaken, bypass, or replace the test with a superficial import-only test.

#### 2.2 Read-only dependency verification

Use `requirements.txt` and `.github/workflows/tests.yml` only to verify the existing dependency declaration and CI installation behavior.

Do not change either file unless you first report a concrete inconsistency and obtain separate authorization.

Do not install packages or change the user's environment.

#### 2.3 Acceptance criteria

1. With project requirements installed, the real XLSX test executes rather than skips.
2. Without `openpyxl`, the test produces a clear failure rather than a skip.
3. The XLSX test and its meaningful assertions remain intact.
4. No unrelated ingestion or financial logic is changed.

---

## Final report requirements

Report each task separately using the exact identifiers and titles:

- `058 · S7-REMED-001`
- `059 · S7-REMED-002`

For each task provide:

1. **Status:** DONE, PARTIAL, NOT DONE, or BLOCKED.
2. Exact files changed.
3. Exact changes made.
4. Before/after explanation of timestamp construction and the preserved naive UTC contract.
5. Confirmation of how many targeted `datetime.utcnow()` occurrences remain (the expected count is zero).
6. Explanation of the Trend freeze-clock test adjustment.
7. Explanation of how the XLSX test now handles a missing `openpyxl` dependency.
8. Confirmation that financial formulas, business logic, database contracts, and unrelated files were not changed.
9. Any additional file required, with exact path and reason.
10. Exact recommended local test commands, explaining what each command covers.

### Recommended test commands for the user

Provide commands covering at least:

`pytest src/tests/test_stage1_rules.py src/tests/test_stage2_kpis.py src/tests/test_stage4_trend.py -q`

`pytest src/tests/test_ingestion_fx.py -q`

Also recommend the full suite after the focused tests pass:

`pytest src/tests -q`

Do not execute these commands yourself.

Do not edit `WORKFLOW_RULES.md` or `STAGE7_MASTER_WORKING_PACKET.md` under any circumstances.

The work is not complete merely because code was edited. Report implementation evidence separately from test evidence; the user will provide the actual test results.