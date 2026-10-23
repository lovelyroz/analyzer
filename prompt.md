# P53.1 — Correct Stage 5 Provenance Handoff to Stage 7

Continue Stage 7 remediation in the local working directory `analyzer`.

## Objective

Correct and verify the P53 change so Stage 7 validates the provenance structure actually produced by Stage 5, rather than relying only on a manually constructed `assumptions["input_refs"]` field.

## Evidence already established

- `src/valuation/engine.py` currently reads `forecast_result.assumptions.get("input_refs")`.
- `src/forecast/engine.py` stores actual provenance under `__input_refs` and `__declared_input_refs`.
- `CompanyForecastResult.to_record()` in `src/forecast/schema.py` also reads those underscored keys.
- Current P53 tests manually inject `assumptions["input_refs"]`; therefore, they do not establish that the actual Stage 5 output is validated by Stage 7.

## Required work

1. Inspect only the relevant code in:
   - `src/valuation/engine.py`
   - `src/tests/test_stage7_valuation.py`
   - `src/forecast/engine.py`
   - `src/forecast/schema.py`
   - The smallest additional directly related test/helper files needed to construct a genuine Stage 5 result.

2. Correct Stage 7's provenance handoff to use the actual Stage 5 output contract. Preserve compatibility only where justified by the existing contract. Do not silently discard provenance, and do not assume that a missing reference list proves PIT correctness.

3. Add focused tests using a `CompanyForecastResult` genuinely produced by the Stage 5 engine or its established production entry point. Verify that the provenance actually emitted by Stage 5 reaches the Stage 7 validator.

4. Cover these cases through the public Stage 7 valuation entry point:
   - A real Stage 5 provenance reference available exactly at the cutoff is accepted.
   - A real Stage 5 provenance reference after the cutoff is rejected if that reference represents an input Stage 7 must not accept.
   - Missing availability is handled conservatively.
   - An explicitly empty `forecast_input_refs` argument cannot bypass provenance already present in the forecast result.
   - Existing behavior remains correct when the forecast contains no provenance, without falsely claiming PIT verification.

5. Inspect how Stage 5 distinguishes accepted and rejected inputs. Do not accidentally make Stage 7 reject a valid forecast merely because Stage 5 records a future input that it demonstrably excluded from the calculation. Conversely, do not let rejected or undated inputs influence valuation as if they were verified. Follow the actual contract and document any unresolved ambiguity.

6. Keep this change narrowly scoped. Do not redesign `engine.py`, change financial formulas, invent availability timestamps, alter locked specifications, or add speculative alerts.

## Restrictions

- Do not run tests or CI. I will run them locally.
- You may add or modify focused tests and must give me the exact commands to run.
- No GitHub operations, GitHub CLI/API, remotes, push/pull, commits, or branch changes.
- Do not edit `reply.md`, `temp_report.md`, `temp_report2.md`, `ClaudeReports/`, `stepsForStage7.md`, or `stage_7_prompts.md`.
- Do not perform a repo-wide scan.

## Completion report

Report:
- Exact files changed and why.
- The actual Stage 5 provenance keys and which references represent inputs used versus inputs rejected.
- How the real Stage 5 result is constructed in the new tests.
- What each test establishes and what it does not establish.
- Exact test commands for me to run.
- Any remaining uncertainty about PIT correctness.

Do not claim tests passed. Stage 7 remains OPEN, and P53 is not considered complete until this handoff is verified.