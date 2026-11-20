# EXECUTION PROMPT — Task 014 Correction / DB-ING-001
## Close the implementation gaps found in code review

**Repository:** `lovelyroz/analyzer`  
**Branch:** `master`  
**Work type:** CODE CORRECTION + TESTS  
**Priority:** High

The initial implementation of Task 014 is present. Do not repeat its implementation or produce another general audit.

Fix the following concrete gaps in the existing implementation.

### Files

- `src/ingestion/excel/canonical_input.py`
- `src/ingestion/excel/deterministic_matcher.py`
- `src/ingestion/excel/dto.py`
- `src/tests/test_excel_canonical_input.py`
- `src/tests/test_excel_template_matching.py`

Read the relevant contracts before changing code.

### 1. Native numeric Excel values

The existing Reader supports `PRESENT_NUMBER`, but `build_candidate()` currently rejects every value except `PRESENT_TEXT`.

Implement safe handling:

- Accept native integer values without float conversion.
- Do not silently convert a binary float into an allegedly exact source Decimal.
- If the original numeric lexical representation is unavailable for a float, reject it explicitly with a stable diagnostic.
- Preserve the distinction between literal text, native integer, native float, blank and zero.
- Do not change the Reader's existing contract without a demonstrated need.

Add tests for native integer acceptance, native float rejection where exact source precision cannot be established, and explicit zero.

### 2. Preserve mapping approval references

`period_mapping` is currently validated but its identity is discarded.

The `ApprovedSelection.approval_ref` fields are also discarded after validation.

Extend the transient Candidate DTO to preserve the identities and approval references needed to audit:

- Company
- Report type
- Report version
- Metric
- Unit
- Currency
- Scale
- Period mapping
- Optional source label/header
- Dimensions and their values

Do not invent approval references. Preserve the exact values supplied by the approved selections.

Add tests proving that approval references and period-mapping identity survive candidate construction.

### 3. Validate actual coordinate ownership

Inspect the matcher's `coordinate_map` and ownership rules.

A coordinate must belong to an explicitly owned extraction range, not merely fall somewhere inside a parent table's broad bounds.

Reject coordinates in excluded, unowned, overlapping or ambiguous areas.

Add tests for:
- A valid owned coordinate.
- A coordinate inside table bounds but outside all owned ranges.
- A coordinate inside an excluded region.
- An ambiguous ownership case.

Do not weaken existing fail-closed matching.

### Constraints

- No ORM/schema/migration/database changes.
- No real workbook ingestion.
- No Parsian template approval or fabricated semantic mappings.
- Do not modify `WORKFLOW_RULES.md`.
- Do not mark Task 014 DONE while locale-specific parsing and authoritative production approval resolution remain unresolved.
- Do not rerun unrelated audits or tests.

### Deliverables

1. Corrected code and focused regression tests.
2. Exact changed-file list.
3. Actual test commands and outputs.
4. Update `database/reports/DB_ING_001_CANONICAL_INPUT_DTO_IMPLEMENTATION.md`.
5. Update `reply.md` and Master Packet §9.
6. Recalculate the progress dashboard only if the Task status actually changes.

Deliver code, not another proposal. Keep Task 014 PARTIAL if any acceptance gap remains.