# Package 4 — Final Valuation Engine Review
## Stage 7 — Controlled Technical Review and Remediation

You are working on the financial-data application repository:

`analyzer`
# Required Files:
    WORKFLOW_RULES.md
    STAGE7_MASTER_WORKING_PACKET.md
    07_Stage7_Valuation.md
    src/valuation/engine.py
    src/valuation/models.py
    src/valuation/parameters.py
    src/valuation/schema.py
    src/valuation/service.py
    src/forecast/schema.py
    src/tests/test_stage7_valuation.py

This is a financial application. Financial correctness, auditability, point-in-time correctness, deterministic behavior, and preservation of approved financial invariants take priority over implementation convenience.

## 1. Work classification

**CODE-CHANGING + TEST AUTHORING + TECHNICAL AUDIT**

You may modify only:
- `src/valuation/engine.py`
- `src/tests/test_stage7_valuation.py`

All other supplied files are read-only.

Do not execute tests, application commands, database commands, Git commands, migrations, or any other commands. The user runs all tests locally.

Do not commit, push, pull, create branches, or modify remote repository settings.

Do not explore files outside the explicitly supplied file list. If another file is essential, stop and report its exact path and why it is needed. Do not inspect `PROMPT.md` or `prompt.md`.

## 2. Assigned tasks

### Task 1 — 033 · S7-T011 — Final Valuation Engine Review

Perform a complete but tightly scoped technical review of:

`src/valuation/engine.py`

Evaluate its implementation against the current approved Stage 7 contracts and the supplied Master Packet.

Review at least the following areas:

1. Financial calculations and preservation of existing approved formulas.
2. Scenario construction and scenario ordering.
3. Scenario probabilities, probability evidence, and probability normalization.
4. Parameter selection, parameter consumption, and model-version metadata.
5. Threshold consumption and valuation-status classification.
6. Rounding and numerical precision at every relevant calculation boundary.
7. EPS behavior, including positive, zero, negative, and sign-changing scenarios.
8. Missing, invalid, non-finite, and inconsistent inputs.
9. Fail-closed behavior and error handling.
10. Forecast input references and the existing PIT safeguards.
11. Target P/E selection and historical P/E handling.
12. Driver analysis, confidence, risk, alerts, and output metadata.
13. Output schema consistency and deterministic behavior, except for explicitly time-dependent metadata.

For every finding, provide:
- Exact function or code location.
- The relevant approved contract or invariant.
- A concrete explanation of the defect or risk.
- A reproducible input condition or test case.
- Financial or operational impact.
- Whether the issue can safely be fixed without resolving a blocked upstream contract.

Do not report a defect merely because a feature is deferred or because evidence is unavailable.

### Task 2 — 038 · S7-PLAN-004 — Controlled Remediation and Regression Tests

Correct only defects that satisfy all of these conditions:

- The defect is demonstrable from the supplied source and approved specification.
- The correction does not require inventing a financial formula, threshold, parameter, data source, provenance contract, or business rule.
- The correction does not depend on a blocked upstream task.
- The correction preserves existing approved financial calculations and public contracts unless a documented defect makes a minimal contract correction unavoidable.

For every correction:
- Make the smallest justified change.
- Add or update focused regression tests.
- Include negative tests for invalid or incomplete inputs where appropriate.
- Preserve existing tests and their financial assertions.
- Never weaken, delete, or bypass a test merely to obtain a passing result.

If a defect depends on an unresolved contract, do not implement a speculative workaround. Document the exact dependency and leave it unresolved.

## 3. Mandatory dependency restrictions

The following upstream tasks are not fully resolved:

- 029 · S7-T007 — D9/PIT and dated parameters: PARTIAL.
- 030 · S7-T008 — Alert and input contracts: PARTIAL.
- 032 · S7-T010 — Real production execution path / E2E: BLOCKED.
- 022 · S7-T013 — Same-company historical Forward P/E: BLOCKED.
- 023 · S7-T014 — Historical P/E from raw data: BLOCKED.
- 024 · S7-T015 — Latest complete input set: BLOCKED.
- 027 · S7-T018 — Reject unproven precomputed P/E: BLOCKED.

Tasks 025 · S7-T016 and 026 · S7-T017 have been implemented and verified within their documented scope.

These unresolved tasks impose strict limitations:

1. Do not claim that full OA1 compliance has been achieved.
2. Do not invent historical P/E observations or provenance.
3. Do not treat the existing numeric `historical_pe_values` sequence as verified provenance.
4. Do not invent a latest-complete-input selection policy.
5. Do not claim full PIT based only on observation dates or data cutoffs.
6. Do not introduce Industry P/E into active Target P/E or cheap/expensive assessment.
7. Do not activate deferred D1–D5 or sector-specific D6 formulas.
8. Do not invent thresholds or alter Genesis parameter values.
9. Do not create an artificial production execution path or claim E2E verification.

You must distinguish between:
- Defects that can be safely corrected now.
- Findings blocked by missing upstream contracts or evidence.
- Deliberately deferred or legacy behavior.
- Findings that are not actual defects.

**Important:** The final review may identify that Task 033 cannot be fully closed yet. Do not mark it DONE merely because this review was performed.

## 4. Financial invariants and change restrictions

Preserve all approved financial formulas and their meanings.

In particular:

- Do not change the underlying Forward P/E or fair-value formulas without explicit specification evidence.
- Do not change scenario weights or probability rules without an approved parameter contract.
- Do not invent or recalibrate thresholds.
- Do not change rounding precision simply for stylistic consistency.
- Do not reintroduce Industry P/E into active valuation decisions.
- Do not recalculate Stage 5 EPS inside Stage 7.
- Do not silently convert invalid or missing financial inputs into apparently valid financial values.
- Do not allow NaN or infinity to contaminate financial outputs.
- Do not make unsupported PIT or historical-validity claims.
- Preserve the existing output contract unless a concrete defect justifies a minimal correction.

If a potential financial correction cannot be justified from the supplied specification, leave the code unchanged and explain the issue.

## 5. Required test coverage

Review the existing tests and add focused regression tests for every defect you correct.

Where relevant, verify:
- Scenario probability validity and sum.
- Missing or malformed scenario inputs.
- Non-finite numeric values.
- Zero and negative EPS.
- Sign changes between scenarios.
- Missing target multiple and insufficient data.
- Invalid or conflicting parameter selection.
- Invalid forecast input references and cutoff violations.
- Rounding boundaries.
- Stability of output status, alerts, and metadata.

Do not create tests that assert invented financial policies.

Do not run any tests or commands.

At the end, provide the exact commands for the user to execute. At minimum, provide:

`pytest src/tests/test_stage7_valuation.py -q`

If your changes affect the Stage 7/9 service interface, also provide:

`pytest src/tests/test_stage789_service_interface.py -q`

Do not claim that any test passed unless the user supplies its execution output.

## 6. Required final report

Provide a structured report with these exact task identifiers:

### 033 · S7-T011 — Final Valuation Engine Review
Report one of:
- DONE
- PARTIAL
- NOT DONE
- BLOCKED

Explain the review coverage, findings, unresolved dependencies, and evidence.

### 038 · S7-PLAN-004 — Controlled Remediation and Regression Tests
Report one of:
- DONE
- PARTIAL
- NOT DONE
- BLOCKED

List every code change and test change, with the reason and the defect it addresses.

### File control
List:
- Every file inspected.
- Every file modified.
- Confirmation that no file outside the allowed modification list was changed.
- Any additional file that was needed but not supplied.

### Financial safety
Explicitly state:
- Whether any financial formula changed.
- Whether any parameter, threshold, scenario weight, or rounding rule changed.
- Whether any new financial assumption was introduced.
- Whether any PIT or provenance claim was strengthened.
- Whether any unresolved dependency remains.

### User test commands
Provide exact commands for the user. Clearly state that tests were not executed by you.

### Final conclusion
Separate:
1. What is technically corrected.
2. What is only audited.
3. What remains blocked by upstream contracts.
4. Whether Task 033 can genuinely be closed.

Do not update `STAGE7_MASTER_WORKING_PACKET.md` or change any task status. The user and ChatGPT will verify your report and evidence before updating the authoritative task register.

Do not claim Stage 7 is complete.