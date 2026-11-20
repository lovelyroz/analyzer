# DB-ING-001 / Task 014 — Canonical input candidate boundary

**Date:** 2026-11-20  
**Status:** PARTIAL — executable immutable candidate builder and focused tests are present. Locale-specific numeric parsing and approved production mapping catalogs/resolvers remain outside this implementation.

## Implementation

Added `src/ingestion/excel/canonical_input.py`. `CanonicalInputCandidate` is a frozen, transient DTO containing company, report type/version, exact approved template identity/version/hash, source workbook SHA-256, matched worksheet identity and source coordinate, source literal, Metric, optional approved label/header, `Decimal` value, source unit/currency/scale, Jalali period endpoints and temporal type/basis, and approved dimension/value identities.

`build_candidate` is a pure boundary. It requires a successful deterministic template match and matching source hash, an in-bounds exact coordinate, explicit unique approval selections for semantic references, exact Jalali dates, explicit duration basis, and literal text matching invariant ASCII Decimal syntax. It preserves the source text and does not convert through float or round. A sparse unobserved cell within the matched bounds is rejected as missing; explicit text `0` remains Decimal zero. No implicit dimensions, units, currencies, scales, periods, or Metric mappings are created.

The matcher result now includes the matched worksheet name and ordinal so source provenance remains resolvable even for sparse blank cells. No observation DTO or Reader behavior was rebuilt. No ORM, schema, migration, database, financial workbook, Parsian mapping, writer, or activation path was changed.

## Validation evidence

Command:

```powershell
.\.venv\Scripts\python.exe -m pytest -q --basetemp .pytest_task014_20261120 src/tests/test_excel_canonical_input.py src/tests/test_excel_source_reader.py src/tests/test_excel_observation_dto.py src/tests/test_excel_template_matching.py
```

Actual final output: `51 passed in 1.55s` (exit code 0).

The new tests cover INSTANT, DURATION/YTD, DURATION/STANDALONE, missing/ambiguous/unapproved mappings, missing required semantic values, missing/invalid dates and period ranges, duration-basis rules, blank versus zero, high-precision Decimal preservation, missing coordinates/provenance, unsupported numeric syntax, dimensions, and source-hash mismatch. Fixtures use clearly synthetic identities solely for tests; none are approved production mappings.

`git diff --check` was also attempted. It reported existing trailing whitespace in the pre-existing modified `prompt.md`; that user-modified file was not changed for this task. A matcher file line-ending normalization notice was also emitted by Git.

## Remaining acceptance gaps

The input Reader contract preserves all populated cells as literal text, including Persian digits and separators. This builder deliberately accepts only invariant ASCII decimal syntax because no approved locale-specific numeric parser contract/catalog was supplied. Also, the repository has no authoritative runtime resolver/catalog that can establish that a caller's `ApprovedSelection` corresponds to a real approved Metric, unit, currency, scale, period, or dimension mapping. The DTO boundary validates explicit approval evidence fields and uniqueness claims but cannot independently authenticate an external approval catalog. Synthetic unit tests do not establish production template or semantic approval. For these reasons Task 014 is **PARTIAL**, not DONE.

## Changed files

- `src/ingestion/excel/canonical_input.py` (new)
- `src/ingestion/excel/deterministic_matcher.py`
- `src/tests/test_excel_canonical_input.py` (new)
- `database/reports/DB_ING_001_CANONICAL_INPUT_DTO_IMPLEMENTATION.md` (new)
- `database/DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md`
- `reply.md`

No real workbook was processed and no database was opened.
