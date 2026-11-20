# CORRECTION PROMPT — Task 015 / DB-ING-002
## Duplicate provenance determinism and ZERO_FALLBACK integration

**Mode:** CODE CORRECTION + focused tests  
**Do not broaden scope.**

### 1. Fix duplicate provenance handling

In `src/ingestion/canonical_admission.py`, inspect:

- `PlannedFact.payload`
- `PlannedFact.identity`
- `prepare_canonical_batch()` duplicate-collapse logic
- `_with_refs()`

Currently, economically identical facts can collapse even when their template/source-mapping provenance differs. `PlannedFact` retains only one template identity, so provenance from the other candidate can be lost.

Implement one explicit safe policy:

- Either reject duplicate candidates when their non-mergeable provenance differs, using a stable diagnostic code; or
- Preserve all distinct provenance in an immutable, normalized, deterministically sorted representation in the plan.

Do not silently select whichever candidate appeared first.

At minimum, account for:
- template ID, version and SHA-256;
- source label/header identities and their approval references;
- extraction owner;
- all approval references and their associated identities.

Economic payload equality alone must not imply provenance equivalence.

### 2. Test order-independent behavior

Add tests where two candidates have:
- Same economic identity and same value, but different template hashes.
- Same economic identity and same value, but different source header/label approvals.
- Same economic identity and same value, but different extraction owners.

For every case, reverse the input order and assert that:
- The result is identical in both orders; or
- Both orders reject with exactly the same diagnostics.

Retain the existing identical-duplicate and conflicting-value tests.

### 3. Resolve ZERO_FALLBACK builder integration

Inspect `src/ingestion/excel/canonical_input.py`.

`build_candidate()` currently rejects blank cells, while `prepare_canonical_batch()` permits `ZERO_FALLBACK` only when the Candidate represents a blank source cell.

Define a safe, explicit integration path that does not turn blanks into zero implicitly:

- A blank observation may become a Candidate only through an explicit, approved ZERO_FALLBACK rule supplied to the relevant preparation boundary.
- Without that explicit approval, blank remains rejected.
- The source observation must remain identifiable as BLANK; do not fabricate source text or a reported zero.
- Actual reported zero must remain distinct from ZERO_FALLBACK.

Add a focused test that exercises the actual supported construction path, not only direct manual construction of `CanonicalInputCandidate`.

If the current architecture cannot support this without changing the Task 014 contract, do not introduce a workaround. Document the exact incompatibility and propose the smallest required boundary adjustment.

### 4. Restrictions

- No ORM, schema, migration or database changes.
- No real workbook or production ingestion.
- Do not run tests; provide the exact owner test command.
- Do not modify `WORKFLOW_RULES.md`.
- Do not reopen unrelated Task 014 or Task 015 decisions.
- Do not mark Task 015 DONE.

### 5. Deliverables

Update:
- `src/ingestion/canonical_admission.py` if needed.
- `src/ingestion/excel/canonical_input.py` only if the explicit ZERO_FALLBACK boundary requires it.
- `src/tests/test_canonical_ingestion_admission.py`.
- `database/reports/DB_ING_002_CANONICAL_INGESTION_ALIGNMENT.md`.
- `reply.md`.
- Relevant Master Packet evidence/status only if necessary.

Report exact changed files, correction behavior, test command, and test execution status.

Task 015 remains PARTIAL.