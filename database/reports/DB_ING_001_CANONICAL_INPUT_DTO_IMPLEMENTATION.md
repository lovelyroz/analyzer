# DB-ING-001 / Task 014 — Canonical input candidate boundary

**Date:** 2026-11-20  
**Status:** PARTIAL — executable immutable candidate builder and focused tests are present. Locale-specific numeric parsing and approved production mapping catalogs/resolvers remain outside this implementation.

## Implementation

Added `src/ingestion/excel/canonical_input.py`. `CanonicalInputCandidate` is a frozen, transient DTO containing company, report type/version, exact approved template identity/version/hash, source workbook SHA-256, matched worksheet identity and source coordinate/unique extraction owner, literal/native numeric state, Metric, optional approved label/header, `Decimal` value, source unit/currency/scale, Jalali period endpoints and temporal type/basis, approved dimension/value identities, and the exact approval references supplied for each selection.

`build_candidate` is a pure boundary. It requires a successful deterministic template match and matching source hash, an exact coordinate with exactly one explicitly owned extraction range, explicit unique approval selections for semantic references, exact Jalali dates, and explicit duration basis. Literal text follows invariant ASCII Decimal syntax. Native integer cells are converted directly to `Decimal(int)` without passing through float; native floats are rejected with `SOURCE_FLOAT_PRECISION_UNAVAILABLE` because their original lexical representation is unavailable. Literal text, native integers, native floats, blank cells, and zero remain distinct; explicit text or integer zero stays zero. No implicit dimensions, units, currencies, scales, periods, or Metric mappings are created.

The matcher result includes matched worksheet identity and `owned_coordinate_map`. Table/partition broad bounds do not grant extraction ownership. Unowned and explicitly excluded coordinates have no eligible owner; overlaps between owned ranges or with excluded ranges reject the match. No observation DTO or Reader behavior was rebuilt, and `dto.py` was not changed because its existing `CellValueKind.PRESENT_NUMBER` already distinguishes native numbers. No ORM, schema, migration, database, financial workbook, Parsian mapping, writer, or activation path was changed.

## Validation evidence

Command:

```powershell
.\.venv\Scripts\python.exe -m pytest -q --basetemp .pytest_task014_20261120 src/tests/test_excel_canonical_input.py src/tests/test_excel_source_reader.py src/tests/test_excel_observation_dto.py src/tests/test_excel_template_matching.py
```

Actual final output: `51 passed in 1.55s` (exit code 0).

Correction regression command:

```powershell
.\.venv\Scripts\python.exe -m pytest -q --basetemp .pytest_task014_correction_20261120 src/tests/test_excel_canonical_input.py src/tests/test_excel_template_matching.py
```

Actual final correction output: `26 passed in 1.61s` (exit code 0).

The focused tests cover INSTANT, DURATION/YTD, DURATION/STANDALONE, missing/ambiguous/unapproved mappings, missing required semantic values, missing/invalid dates and period ranges, duration-basis rules, blank versus zero, high-precision Decimal preservation, exact native integer and native zero support, native float rejection, approval-reference retention, missing coordinates/provenance, unsupported numeric syntax, unique coordinate ownership, excluded/unowned/ambiguous ownership, dimensions, and source-hash mismatch. Fixtures use clearly synthetic identities solely for tests; none are approved production mappings.

`git diff --check` was also attempted. It reported existing trailing whitespace in the pre-existing modified `prompt.md`; that user-modified file was not changed for this task. A matcher file line-ending normalization notice was also emitted by Git.

## Remaining acceptance gaps

The input Reader contract preserves all populated cells as literal text, including Persian digits and separators. This builder deliberately accepts only invariant ASCII decimal syntax because no approved locale-specific numeric parser contract/catalog was supplied. Also, the repository has no authoritative runtime resolver/catalog that can establish that a caller's `ApprovedSelection` corresponds to a real approved Metric, unit, currency, scale, period, or dimension mapping. The DTO boundary validates explicit approval evidence fields and uniqueness claims but cannot independently authenticate an external approval catalog. Synthetic unit tests do not establish production template or semantic approval. For these reasons Task 014 is **PARTIAL**, not DONE.

## Changed files

- `src/ingestion/excel/canonical_input.py` (new)
- `src/ingestion/excel/deterministic_matcher.py`
- `src/tests/test_excel_canonical_input.py` (new)
- `src/tests/test_excel_template_matching.py`
- `database/reports/DB_ING_001_CANONICAL_INPUT_DTO_IMPLEMENTATION.md` (new)
- `database/DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md`
- `reply.md`

`src/ingestion/excel/dto.py` was inspected and left unchanged; it already exposes native `int | float` numeric observations and a distinct blank kind.

No real workbook was processed and no database was opened.
