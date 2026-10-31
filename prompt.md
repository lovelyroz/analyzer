# Stage 7 — Documentation Consistency Correction (AMENDMENT-OA1)

**Repository:** `lovelyroz/analyzer`

**Task type:** DOCS-ONLY — documentation edits are required. This is NOT a report-only task.

## Required files

Read:
- `WORKFLOW_RULES.md`
- `07_Stage7_Valuation.md`
- `stepsForStage7.md`
- `tasksToDo.md`
- `STAGE7_MASTER_WORKING_PACKET.md`
- `STAGE7_COMPLETED_CHECKLIST.md`
- Relevant OA1 documentation in `temp_report2.md`
- `reply.md`

Edit only the files that genuinely require correction from this list:
- `07_Stage7_Valuation.md`
- `tasksToDo.md`
- `stepsForStage7.md`
- `STAGE7_MASTER_WORKING_PACKET.md`
- `STAGE7_COMPLETED_CHECKLIST.md`
- `temp_report2.md`
- `reply.md` only if its temporary report needs correction.

## Required corrections

1. Audit the entire `07_Stage7_Valuation.md` for remaining active Industry P/E references, including sections 48, 49, 55, 63, and the Output Contract. Clearly distinguish superseded functionality, inactive legacy fields, and informational metadata. Industry Forward P/E and Industry TTM P/E must not remain active in cheap/expensive assessment or Target P/E selection. Do not unnecessarily remove legacy fields needed for compatibility.

2. Review S7-T013 dependencies. Do not imply that historical Forward P/E implementation can proceed without required source, temporal provenance, company identity, period, cutoff, and availability contracts. Clearly identify which implementation parts are independently actionable and which depend on S7-T007 or other unresolved prerequisites. Do not invent data sources or contracts.

3. Correct PIT status terminology throughout the relevant documents. Distinguish:
   - Architecture/design review: PASS where supported.
   - Runtime PIT implementation and verification: OPEN or BLOCKED until actual temporal provenance evidence exists.
   - Full PIT must never be claimed based solely on Jalali observation dates.

4. Clarify `Ready for implementation` and `Ready for Stage 8` statements so they cannot be interpreted as proof that OA1 implementation, runtime PIT, or Stage 7 completion has been achieved.

5. Ensure all six primary documents tell a consistent story:
   - Owner-approved OA1 policies are documented.
   - S7-T013 through S7-T018 remain OPEN until code and user-run test evidence exists.
   - S7-T019 remains OPEN until the Forecast persistence audit is completed.
   - Stage 7 remains OPEN.
   - Analytical-output persistence remains prohibited.
   - Existing Forecast persistence models must not be deleted or modified in this task.

6. Update `temp_report2.md` with a concise correction report, recording exactly what was changed and the final status of each affected issue. Do not overwrite historical reports.

## Strict boundaries

- No Python or other code changes.
- No database/model/schema changes.
- No test creation, modification, or execution.
- No changes outside the explicitly listed documentation files.
- Do not mark implementation or audit tasks DONE merely because documentation was corrected.
- Do not invent thresholds, formulas, provenance, data sources, or financial rules.
- Follow `WORKFLOW_RULES.md`.

## Final report

Report:
- Exact files changed.
- Exact sections corrected in each file.
- How each of the four identified issues was resolved.
- Remaining OPEN/BLOCKED items and their prerequisites.
- Explicit confirmation that no code was changed and no tests were executed.

**Important:** Actually edit and save the required documentation files. A report describing proposed edits without applying them does not complete this task.