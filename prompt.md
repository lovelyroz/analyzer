# P54 — Stage 7 Historical Parameter Versioning (D9)

## Project and objective

Work on the local project `analyzer`, a financial-data application. Review and safely improve Stage 7 historical parameter versioning under policy D9.

The priorities are financial correctness, auditability, deterministic behavior, and truthful Point-in-Time (PIT) claims. Do not invent historical parameter values or effective dates.

## Required source files

Use these files as the authoritative working set for this task:

1. `stepsForStage7.md` — authoritative Stage 7 execution order, policies D1–D9, and acceptance criteria.
2. `07_Stage7_Valuation.md` — current Stage 7 V1 contract.
3. `src/valuation/parameters.py` — parameter sets, registry, effective-date selection, genesis set, and parameter validation.
4. `src/valuation/engine.py` — Stage 7 parameter-selection call site and valuation metadata.
5. `src/valuation/schema.py` — valuation result and audit metadata contract.
6. `src/valuation/service.py` — Stage 7 service boundary and any date-related inputs passed into valuation.
7. `src/tests/test_stage7_valuation.py` — existing parameter-selection tests and regression coverage.

Inspect only these files and their directly relevant functions. Do not perform a repository-wide scan. If an additional file is genuinely required, name it and explain why before expanding the scope.

## Current established findings

- The parameter system has a genesis parameter set without `effective_from`.
- Explicit effective-dated selection exists through `parameter_as_of` and a parameter registry.
- The legacy path can use genesis parameters while reporting that PIT selection was not applied.
- Stage 7 records a parameter snapshot and version metadata, but a snapshot alone does not establish when those parameters were historically valid.
- Current valuation metadata reports `data_cutoff_used_for_parameter_selection=False`.
- No reliable historical effective dates may be inferred from model-version labels, current constants, commit dates, or assumptions.
- Stage 7 remains OPEN.
- User-run results for `src/tests/test_stage7_valuation.py` currently show 80 passed, including five P53 tests. Do not rerun tests; the user runs all tests and supplies the output.

## Required analysis and implementation

### 1. Audit the existing contract

Trace how parameter sets are created, validated, selected, consumed, and recorded in the valuation result. Identify the difference between:

- model version;
- parameter-set identifier;
- complete parameter snapshot;
- parameter effective date;
- valuation data cutoff;
- valuation date.

Explain which of these the code can prove today and which it cannot.

### 2. Use a consistent PIT selection rule

For historical valuation, use the valuation's effective **data cutoff** as the governing timestamp for parameter selection. Do not infer parameter validity from `valuation_date` when the information cutoff differs.

Make the smallest compatible implementation that ensures an explicitly requested effective-dated parameter selection uses a timestamp consistent with that cutoff. If a caller explicitly supplies a conflicting parameter-selection timestamp, reject the mismatch or handle it through an already documented contract; do not silently use whichever date is more convenient.

Preserve the existing legacy genesis path only where backward compatibility requires it, and make its lack of historical PIT verification explicit in metadata. Do not claim that genesis was historically valid.

Do not make every existing valuation fail solely because the current default registry contains only undated genesis parameters. Where no historically valid set exists, report the limitation truthfully and do not silently select a newer or undated set as if it were historically verified.

### 3. Preserve financial and API invariants

- Do not change valuation formulas, thresholds, alerts, EPS, or scenario logic.
- Do not invent parameter values, historical parameter versions, or effective dates.
- Do not silently modify the default parameter values.
- Preserve deterministic selection and reject ambiguous overlapping effective-date versions.
- Keep the change focused on parameter selection and audit metadata.
- Do not redesign `engine.py`; its final architectural review is a later Stage 7 step.
- Do not edit the locked specification unless a real contract contradiction is demonstrated. If documentation clarification is essential, explain the exact conflict instead of broadening the scope.

### 4. Add focused regression tests

Add or update tests covering, as applicable:

- selection of the uniquely valid parameter set at the data cutoff;
- the exact effective-date boundary;
- rejection when no effective-dated set exists for the requested historical cutoff;
- rejection of ambiguous overlapping versions;
- explicit mismatch between the cutoff and a caller-supplied parameter-selection timestamp;
- correct audit metadata distinguishing verified effective-dated selection from legacy genesis;
- deterministic parameter selection and snapshot recording;
- backward compatibility for the existing legacy path, without falsely claiming PIT verification.

Use synthetic test parameter sets only inside tests, clearly marked as test fixtures. Never register them as real production history.

Do not weaken or delete existing tests merely to make the suite pass.

### 5. Test execution restrictions

Do not execute tests, CI, or any commands that claim runtime validation. The user will run the tests and provide the actual output.

You may add or modify the focused test code. Provide exact PowerShell-compatible commands for the user to execute.

## Repository and reporting restrictions

- No GitHub operations, GitHub CLI/API, remotes, push/pull, commits, or branch changes.
- Do not edit `reply.md`, `temp_report.md`, `temp_report2.md`, `ClaudeReports/`, `stepsForStage7.md`, or `stage_7_prompts.md`.
- Do not perform unrelated cleanup or repo-wide exploration.
- Do not claim tests passed.

## Completion report

Report:

1. Exact files changed and the reason for each.
2. The parameter-selection rule now implemented.
3. What is and is not historically verifiable.
4. New or modified tests and the exact commands the user should run.
5. Any remaining D9 limitations.
6. Whether the change preserves the legacy path without overstating PIT guarantees.

Do not mark Stage 7 complete. Historical parameter versioning must remain explicitly unverified wherever authoritative effective dates and historical values are unavailable.