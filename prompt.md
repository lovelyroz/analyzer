# Prompt 1-B — Evidence Gaps in the Existing Stage 7 Audit

**Prompt ID:** Prompt 1-B  
**Parent Prompt:** Prompt 1  
**Task IDs:** S7-T001, S7-T002, S7-T003, S7-T004, S7-T005  
**Task type:** AUDIT ONLY + SUPPLEMENTAL REPORT CORRECTION

## Objective

Continue the existing Prompt 1 audit. Do not restart the audit or repeat findings that are already adequately evidenced in `reply.md`.

Close only the evidence gaps listed below. Update `reply.md` with a clearly labelled `Prompt 1-B Supplemental Audit` section. Preserve previous reports as historical records.

## Required reading — before inspecting code

3. `stepsForStage7.md`
4. `reply.md`, including the Prompt 1-A report and earlier findings
5. `PROMPT.md`
6. `07_Stage7_Valuation.md`

Use the current task register and authoritative Stage 7 specifications. Do not infer that a previous report is correct merely because it exists.

## Required source and test inspection

Inspect the existing files relevant to each finding, including:

- **T001 — Production execution path:** `src/scoring/`, `src/forecast/`, `src/valuation/service.py`, `src/market/service.py`, `src/decision/service.py`, and the actual application entrypoints, callers, dependency wiring and session lifecycle files discovered in the repository.
- **T002 — Stage 9 persistence:** `src/decision/schema.py`, `src/decision/engine.py`, `src/decision/service.py`, `src/core/database.py`, and all relevant SQLAlchemy model, table, repository and persistence modules discovered in the repository.
- **T003 — D9:** `src/valuation/parameters.py`, `src/valuation/service.py`, the relevant sections of `src/valuation/engine.py`, and direct Stage 7 parameter-selection and consumption tests.
- **T004 — PIT and provenance:** Stage 5/7 specifications, `src/forecast/queries.py`, `src/forecast/schema.py`, `src/valuation/schema.py`, `src/valuation/service.py`, `src/valuation/engine.py`, `src/market/service.py`, `src/market/schema.py`, `src/ingestion/market/queries.py`, and relevant direct tests.
- **T005 — D1–D8:** `stepsForStage7.md`, `07_Stage7_Valuation.md`, `src/valuation/engine.py`, `src/valuation/parameters.py`, relevant schemas, tests, and actual consumers of alert/driver outputs.

Follow actual references and imports to identify additional relevant files. Do not claim a repository-wide absence based only on the initial file list. In the report, enumerate the additional files actually inspected and identify the evidence supporting each conclusion.

## Required corrections

### S7-T001
Establish the actual call chain using file and function names. Separate:
- an existing service;
- an internal service-to-service call;
- an actual production caller;
- a complete end-to-end path, including session ownership and upstream inputs.

If no production entrypoint or caller is found, document the search scope and inspected evidence. State “not found in the inspected scope” unless the evidence genuinely supports a broader conclusion. Do not design or implement an entrypoint.

### S7-T002
Determine whether Stage 9 persistence is absent, partial or present. Inspect the relevant model/table/repository/persistence code before deciding. Distinguish result schemas and dataclasses from persisted records.

List the relevant persistence files actually inspected. If the evidence cannot establish repository-wide absence, explicitly mark the finding unverified rather than asserting that persistence does not exist.

Do not design or implement persistence.

### S7-T003
Trace the selected parameter set from date-based resolution into the actual valuation calculations. Identify which calculations consume resolved parameters, which metadata is merely recorded, and what happens when no valid dated version exists.

List the direct tests inspected and what each test establishes. Do not invent an effective date, parameter value, fallback or owner approval.

### S7-T004
Create a concise evidence matrix covering at least:
- market price and historical observations;
- forecast inputs and their availability/publication provenance;
- historical and industry benchmark series;
- market signals and other Stage 7 inputs;
- the resulting valuation/decision outputs and their provenance.

For each category, state the available temporal fields, validation performed, evidence source and remaining limitation. Distinguish data cutoff, report date, publication time and actual availability time. Do not claim PIT correctness solely because a cutoff parameter exists.

### S7-T005
Cover **every decision D1–D8 individually**. For each, record:
- the governing policy/specification;
- implementation status;
- exact source symbols, if implemented;
- tests and actual consumers inspected;
- whether the capability is deferred, partially implemented, implemented or unverified.

Do not group D1–D6 together in a way that leaves D7 or D8 unexamined. Do not infer implementation from a test name or from a status string alone. Do not create financial formulas, thresholds or industry mappings that lack approved specifications.

## Global constraints

- **Audit and report only.**
- Do not modify source code, tests, configuration, schemas, task register or roadmap.
- The only permitted modification is appending the `Prompt 1-B Supplemental Audit` section to `reply.md`.
- Do not run tests, application code, database commands or Git commands.
- Do not create or propose synthetic financial data as evidence of real integration.
- Do not implement an orchestrator, entrypoint or Stage 9 persistence.
- Do not redesign `src/valuation/engine.py`; its final review remains reserved for the final technical bundle.
- Do not change the main prompt numbering or create a new main prompt.
- Do not mark any task DONE merely because this report was produced.
- Do not claim any file was inspected or modified unless that actually occurred.
- Do not claim tests passed unless their actual output was provided by the user.

## Required report format

Append a section to `reply.md` containing:

1. Prompt ID and Task IDs.
2. Evidence gaps addressed for T001–T005.
3. Findings with exact file paths and function/class names.
4. Additional files actually inspected, grouped by Task ID.
5. Tests inspected and what they establish; state explicitly that tests were not executed.
6. Any remaining uncertainty and the exact evidence or owner decision required.
7. Files modified — expected: `reply.md` only.
8. Recommended task statuses, with reasons; do not modify `tasksToDo.md`.
9. A concise decision on whether Prompt 1’s audit acceptance criteria are now satisfied. If not, list only the remaining gaps that genuinely block acceptance.

Stop after updating the supplemental report. Do not proceed to implementation or Prompt 2.