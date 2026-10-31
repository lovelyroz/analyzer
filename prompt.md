# Stage 7 — Documentation Status Correction (Tasks 029–031)

**Task type:** Documentation-only. No code or test changes.

## Files to provide
1. `STAGE7_MASTER_WORKING_PACKET.md`
2. `07_Stage7_Valuation.md`
3. `reply.md`

## Instructions

Review the three files and make only the following corrections:

1. **Task 030 / S7-T008:** Change status from `DONE` to `PARTIAL`. Explicitly document that, for V1, sector-specific drivers and formulas (including bank/holding-specific formulas) are deferred because validated financial definitions and supporting evidence are not available. Retain the existing EPS and TARGET_PE drivers. Do not present D6 as fully resolved.

2. **R7:** Record the architectural decision that the V1 parameter registry is maintained in code under Git version control, not in the application database.

3. **R8:** Record that all output-affecting parameters, including weights, thresholds, and rounding/precision rules, must belong to an immutable model version. Any material change requires a new model version.

4. Keep Task 029 `PARTIAL`, Task 031 `DONE` (audit completion only), Task 032 `BLOCKED`, Task 033 `BLOCKED`, and Task 034 `OPEN`.

5. Do not mark R5 or any implementation/evidence-dependent item as resolved merely because an architectural decision has been recorded.

## Restrictions
- Do not modify source code, tests, migrations, or workflows.
- Do not change Forecast Persistence Tasks 053–057.
- Do not delete or rewrite historical reports.
- Preserve existing decisions and evidence. Do not invent missing evidence.
- Update the Master Packet dashboard and task register consistently.
- Append a concise correction report to `reply.md`.

## Final response
Report:
- Exact files changed.
- Exact status changes.
- Decisions recorded.
- Any unresolved items.
- Confirmation that no code or tests were changed.

Do not run tests. Do not commit or push.