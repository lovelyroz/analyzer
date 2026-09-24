# CODAL 19-PDF Validation Matrix

## Scope

This matrix governs validation for the full representative corpus currently present in the repository:

- seo-codal-report (1).pdf
- seo-codal-report (2).pdf
- seo-codal-report (3).pdf
- seo-codal-report (4).pdf
- seo-codal-report (6).pdf
- seo-codal-report (7).pdf
- seo-codal-report (8).pdf
- seo-codal-report (9).pdf
- seo-codal-report (10).pdf
- seo-codal-report (11).pdf
- seo-codal-report (12).pdf
- seo-codal-report (13).pdf
- seo-codal-report (14).pdf
- seo-codal-report (15).pdf
- seo-codal-report (16).pdf
- seo-codal-report (19).pdf
- seo-codal-report (20).pdf
- seo-codal-report (25).pdf
- seo-codal-report (26).pdf

These 19 PDFs are the current validation corpus. They are not replaced by the four earlier integration samples.

## Governing rules

- Production code must not be modified to satisfy validation.
- Golden expected values must not be fabricated.
- Golden status is blocked unless an independent authoritative source exists.
- The validation architecture is split into structural tests, repeated deterministic tests, repeated ingestion/idempotency tests, and independent Golden validation tests.

## Validation matrix

| Layer | Corpus | Repetitions | Primary invariant | Evidence | Status |
|---|---|---:|---|---|---|
| A. PDF extraction contract | All 19 PDFs | 1 per PDF baseline; repeated as required for regression | PDF → RawLineInput is deterministic, valid, and preserves raw identity fields without inventing values | Extraction output, normalized raw text, source section/row/column, raw item name/code, unit, currency, NULL semantics | ONE-TIME STRUCTURAL TEST |
| B. Persistence contract | All 19 PDFs | 1 per PDF baseline; repeated after schema or ingestion change | RawLineInput → database foundation preserves Decimal precision, NULL vs 0, provenance, identity, FK integrity, and raw immutability | Persisted Report, ReportVersion, FinancialPeriod, RawFinancialFact, IngestionRun records | ONE-TIME STRUCTURAL TEST |
| C. End-to-end production integration | All 19 PDFs | 1 pass baseline + rerun after relevant changes | PDF → acquisition → extraction → validation → persistence works end-to-end without partial writes | IngestionRun audit rows, persisted models, transactional boundaries, failure classification | ONE-TIME STRUCTURAL TEST |
| D. Independent Golden accuracy | Only PDFs with independent authoritative evidence | 0 until external authority exists; then per eligible PDF | Authoritative expected values match production results without deriving from the same production path | Official CODAL metadata, canonical URL, report ID, audited manifest, exact Decimal values, provenance trail | INDEPENDENT GOLDEN ACCURACY TEST |
| E. Idempotency | All 19 PDFs | Minimum 3 ingestion cycles per PDF | Re-running ingestion does not duplicate raw facts or report versions when identity/version is unchanged | Before/after database diffs, deduplicated fact keys, preserved source identity, version invariants | REPEATED INGESTION / IDEMPOTENCY TEST |
| F. Determinism | All 19 PDFs | Minimum 3 extraction executions per PDF | Extraction output remains stable across repeated runs for the same source | A == B == C for normalized RawLineInput outputs; no unexplained diffs | REPEATED DETERMINISTIC TEST |
| G. Failure / recovery | Representative failures plus corpus-relevant cases | Per failure class, repeated as needed | Failures are explicit, auditable, and recoverable without partial financial writes | IngestionRun failure states, rolled-back writes, retry safety, exception classification | ONE-TIME STRUCTURAL TEST + RECOVERY VALIDATION |
| H. PIT / version / restatement | All applicable reports in corpus | One baseline + rerun after version/date changes | Historical and current report versions remain reproducible and non-destructive | publication_datetime, financial period, version metadata, PIT logic, report-version lineage | ONE-TIME STRUCTURAL TEST + REPEATED VALIDATION |
| I. Regression | Full repo test suite | Full suite after relevant changes, plus final gate | Existing Stage 1–9 behavior stays green after CODAL validation changes | Full repository pytest run plus targeted regression | FINAL REGRESSION TEST |

## Category definitions

### ONE-TIME STRUCTURAL TESTS

These validate contract shape, database boundaries, failure classification, and implementation invariants once per code or schema change. They are not a substitute for repeated deterministic validation.

### REPEATED DETERMINISTIC TESTS

These validate that extraction output is stable across repeated runs for the exact same input PDF. They are intended to detect hidden nondeterminism, metadata drift, ordering drift, or normalization changes.

### REPEATED INGESTION / IDEMPOTENCY TESTS

These validate that repeated ingestion across 3 cycles does not change the logical database state after the first successful import. They are not the same as deterministic extraction tests.

### INDEPENDENT GOLDEN ACCURACY TESTS

These are only allowed when an independent authoritative source exists. They must compare authoritative expected values against production results. They must never compare production output to itself, to a copied production fixture, or to a second parser on the same PDF.

## Expected final status

- Structural validation: required
- Determinism checks: required
- Idempotency checks: required
- Repository regression: required
- Independent Golden validation: blocked until an authoritative external dataset exists
- Golden status: BLOCKED

## Golden status rule

The current repository does not contain an authoritative expected dataset for the 19 real PDF samples. Therefore:

GOLDEN STATUS: BLOCKED

No Golden expected-value fixture, copied database fixture, or second-parser-derived expected data may be used.
