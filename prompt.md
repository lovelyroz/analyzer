# Stage 7 — Target 4: Parameter Registry Technical Remediation


This is a financial-data application. Financial correctness, deterministic behavior, auditability, compatibility, and preservation of existing financial invariants are mandatory.

## 1. Work classification

**CODE-CHANGING — Modify implementation and tests.**

Do not run tests, application code, database commands, or Git commands. The user will execute all tests locally.

Do not repeat the previous Target 4 audit. The findings and required scope are already documented in `STAGE7_Target4.md`.

## 2. Required files

Examine only these explicitly supplied files:

1. `STAGE7_Target4.md`
2. `src/valuation/parameters.py`
3. `src/valuation/engine.py`
4. `src/tests/test_stage7_valuation.py`

If another file is essential to verify compatibility with existing consumers, do not inspect it automatically. Report its exact path and why it is required before proceeding with the affected change.

## 3. Implementation tasks

### T4-1 — Enforce unique version keys

- Ensure `ParameterRegistry` rejects duplicate `version_key` values during construction.
- Preserve deterministic exact-key resolution.
- Provide a clear and appropriate validation error.
- Add tests proving that duplicate keys are rejected and unique keys continue to resolve correctly.

### T4-2 — Enforce deep immutability

- Correct the incomplete immutability of nested parameter values.
- Protect mutable nested structures such as dictionaries and lists recursively.
- Apply the protection consistently to parameter records and consumed parameter values where applicable.
- Preserve existing public interfaces and expected read behavior wherever possible.
- Do not silently alter parameter meaning, serialization expectations, or valuation calculations.
- Add tests proving that nested mutation cannot alter stored parameter state or consumed values.

If compatibility with existing consumers cannot be established from the supplied files, stop the affected implementation and identify the exact additional files needed. Do not guess.

### T4-3 — Preserve and test existing resolver behavior

Ensure the changes do not regress:

- Date-based parameter resolution.
- Resolution with different tuple orderings.
- Rejection of ambiguous effective dates.
- Legacy Genesis behavior.
- Timestamp governance and cutoff conflict handling.
- Snapshot independence.

Add or adjust targeted tests only where existing coverage is insufficient.

Do not change timestamp semantics or resolver policies as part of these corrections.

## 4. Strict boundaries

- Do not invent historical parameter values or effective dates.
- Do not change or approve Genesis financial parameters.
- Do not decide R5, R6, R7, R8, or R9/D7 on behalf of the owner.
- Do not implement database persistence or external Registry storage.
- Do not change PIT benchmark provenance responsibilities.
- Do not activate deferred financial rules or industry mappings.
- Do not modify valuation formulas or unrelated modules.
- Do not weaken, delete, or bypass existing tests.
- Do not refactor unrelated code.
- Do not modify `stepsForStage7.md`, `tasksToDo.md`, `temp_report2.md`, or other documentation.

## 5. Required deliverables

Report:

1. Files changed and the reason for each change.
2. T4-1 implementation details.
3. T4-2 implementation details.
4. T4-3 tests added or adjusted, with exact test names.
5. Compatibility considerations.
6. Any unresolved issue or additional required file.
7. Exact local test commands for the user.
8. Any remaining Target 4 blockers, especially owner decisions R5–R9.

Do not claim tests passed. Tests must be marked **NOT RUN — USER EXECUTION REQUIRED**.

Do not mark Target 4 complete. This task addresses only the confirmed technical defects and their regression coverage.