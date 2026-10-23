# P51 — Reconcile Stage 7 Alert Contract (D8)

You are working in the local project folder `analyzer`, a financial-data application where correctness, auditability, deterministic behavior, and preservation of financial invariants are mandatory.

## Objective

Resolve the Stage 7 alert-contract discrepancies under policy D8 in `stepsForStage7.md`. Determine which alert names and behaviors are required, which are actually emitted, and whether any safe implementation changes are justified.

This is a bounded implementation task, not a repository-wide audit.

## Required reading

Read only the relevant sections of:

- `stepsForStage7.md` — especially D1–D9, D8, and the execution sequence.
- `temp_report2.md` — the baseline Stage 7 audit, P2/P3 findings, P37 reconciliation, and the latest reports.
- `07_Stage7_Valuation.md` — alert requirements and output contract.
- `src/valuation/engine.py`
- `src/valuation/schema.py`
- `src/valuation/parameters.py`
- `src/decision/engine.py`
- Relevant tests in `src/tests/test_stage7_valuation.py` and `src/tests/test_stage9_decision.py`.

Inspect additional files only when needed to establish a specific alert consumer or dependency.

## Work to perform

1. Build an evidence-based comparison of:
   - Alert names required by the specification.
   - Alert names emitted by the current valuation engine.
   - Alert fields and severity values exposed by the output schema.
   - Alert information actually consumed by Stage 9 or other directly identified callers.

2. For each discrepancy, classify it as:
   - A demonstrable implementation defect against a sufficiently precise requirement.
   - A naming or contract mismatch that can be corrected without changing financial meaning.
   - An unresolved specification ambiguity.
   - A capability intentionally deferred by D1–D6 under V1.

3. Implement safe, specification-backed corrections where the expected behavior is unambiguous. Add focused regression tests for each correction.

4. Preserve the following constraints:
   - Do not invent alert triggers, financial formulas, thresholds, severities, or industry mappings.
   - Do not reactivate the deferred D1–D5 alerts unless the locked specification provides valid criteria.
   - Preserve the current two-driver contract, EPS × target-P/E valuation, scenario probabilities, invalid-EPS safeguards, and benchmark hierarchy.
   - Do not rename or remove an alert if that could silently break an identified consumer. Establish compatibility first.
   - Do not weaken or delete existing tests merely to obtain a passing result.
   - Do not redesign or centralize `engine.py`; final engine review belongs at the end of Stage 7.
   - Do not claim full Point-in-Time correctness or production integration based on this task.

5. If a discrepancy cannot safely be corrected, leave its behavior unchanged and record the exact missing specification or compatibility decision. Still complete all independent, safe implementation work; do not stop with a generic blocker report.

## Scope and execution restrictions

- Work only in local `analyzer`.
- No GitHub, GitHub CLI/API, remote operations, push, pull, commit, or branch changes.
- Do not run tests or CI; the user will execute them and provide actual output.
- Add or update focused tests, but clearly state that they were not executed.
- Do not edit `reply.md`, `temp_report.md`, `temp_report2.md`, `ClaudeReports/`, `stepsForStage7.md`, or `stage_7_prompts.md`.
- Do not explore the entire repository.
- Do not claim that a production caller or consumer exists without identifying its actual call site.

## Completion report

When the implementation and static review are complete, report:

1. The required-versus-actual alert comparison.
2. Every confirmed discrepancy and its classification.
3. Files changed and the purpose of each change.
4. Tests added or modified, with an explicit statement that they were not run.
5. Remaining D8 issues and the precise evidence or decision needed to resolve them.
6. The next recommended step in the existing Stage 7 execution plan.

Do not modify report files. Finish the entire bounded task before reporting. Stage 7 remains OPEN and must not be declared frozen.