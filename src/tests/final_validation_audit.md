# Final Validation Audit — CODAL 19-PDF Corpus

This is the final independent audit required by the validation programme. It
records the verified state after all issues were addressed, distinguishes
DESIGNED / IMPLEMENTED / EXECUTED / PASSED / BLOCKED, and states exactly what
each test can and cannot catch.

No production code, architecture document, `DATABASE_CONTRACT_V1.3`, or
analytical stage was modified at any point in this series. Every change in the
series is test-only or documentation-only.

---

## 1. Issues addressed (one problem per change)

| # | Issue | Change | Verification |
|---|---|---|---|
| 1 | Layer E idempotency covered only 1 of 19 PDFs with 2 cycles, not 3 | `98ade7c` — corpus-wide idempotency test, 19 PDFs × 3 cycles with full persisted-state snapshots | 19/19 PASS; mutation (duplicate fact) killed |
| 2 | Layer B/C deep persistence invariants covered only 1 of 19 PDFs; aggregate load test asserted only row counts | `17e18ee` — corpus-wide deep persistence invariants | 19/19 PASS; mutation (FK drift, Persian digits) killed |
| 3 | Golden docs internally inconsistent: five documents described a 4-PDF corpus while the locked corpus is 19 | `5da477d` — corrected corpus scope; added DESIGNED/EXECUTED/PASSED evidence section | docs consistent; Golden still BLOCKED |
| 4 | `.gitignore` contained `pdf/`, silently excluding any new corpus PDF | `83c8760` — removed `pdf/` so the corpus stays version-controlled | corpus tracked; inventory gate holds |
| 5 | Documentation did not record the CI gate or its status terminology | `b976ab0` — added CI configuration + status terminology section | docs match workflow |
| 6 | Test fixture bound to the production on-disk engine; full suite non-hermetic, order-dependent, and polluting production DB | `e5b5536` — isolated in-memory fixture | full suite went 2 failed/5 errors → 234 passed/2 skipped; production DB untouched |
| 7 | NULL != 0 was not detectably enforced through the persistence path | `0b02e55` — extraction type check + blank/zero distinctness + NULL-vs-zero persistence test | mutation (NULL→0) killed |

---

## 2. Layer-by-layer verified status

Source of truth for coverage: `src/tests/test_codal_pdf_extraction.py` unless noted.

| Layer | Test(s) | Corpus | Repetitions | Status |
|---|---|---|---|---|
| Inventory gate | `test_codal_validation_corpus_inventory_is_exactly_locked_19_pdfs` | all 19 (locked) | 1 | EXECUTED / PASSED |
| A. Extraction contract | `test_representative_codal_layouts_extract_rows`, `test_all_supplied_codal_pdfs_have_explicit_extraction_outcomes`, `test_extraction_keeps_blank_and_explicit_zero_distinct`, normalization/RTL/date contract tests | all 19 | 1 per PDF | EXECUTED / PASSED |
| B. Persistence contract | `test_locked_codal_corpus_persistence_satisfies_hard_invariants`, `test_null_and_explicit_zero_persist_as_distinct_values`, `test_codal_raw_text_fields_are_ascii_normalized_before_persistence` | all 19 (deep) | 1 per PDF | EXECUTED / PASSED |
| C. End-to-end integration | `test_locked_codal_corpus_persistence_satisfies_hard_invariants`, `test_representative_codal_samples_load_into_core_persistence`, `test_codal_pdf_facade_connects_extraction_to_raw_persistence` | all 19 (deep) + aggregate | 1 per PDF | EXECUTED / PASSED |
| D. Independent Golden accuracy | none — no independent authoritative source exists | none | 0 | BLOCKED (correct, by design) |
| E. Idempotency | `test_locked_codal_corpus_ingestion_is_idempotent_across_three_cycles` | all 19 | 3 ingestion cycles per PDF | EXECUTED / PASSED |
| F. Determinism | `test_locked_codal_corpus_extraction_is_deterministic_across_three_independent_runs` | all 19 | 3 extraction runs per PDF (A == B == C) | EXECUTED / PASSED |
| G. Failure / recovery | `test_malformed_pdf_is_rejected_and_ingestion_is_audited`; `test_pipeline_acquisition_failure_is_audited_without_partial_writes`, `test_pipeline_extraction_failure_is_audited_without_partial_writes` (in `test_codal_extraction.py`) | representative failure classes | per class | EXECUTED / PASSED |
| H. PIT / version / restatement | `test_independent_final_foundation_audit_checks_pit_provenance_and_version_invariants` (single-PDF deep PIT); `test_pipeline_idempotent_version_chain` (in `test_codal_extraction.py`) | 1 deep + version chain | 1 | EXECUTED / PASSED (see scope note) |
| I. Regression | full repository `pytest src/tests` (CI command) | full repo | after each change + final gate | EXECUTED / PASSED |

### Layer H scope note (honest limitation)

Deep, PIT-specific assertions (publication-datetime cutoff ordering) are
executed on one representative PDF, not all 19. Per-PDF `publication_datetime`,
exactly-one-current-`ReportVersion`, and FK bookkeeping ARE asserted corpus-wide
by Layer B/C. Corpus-wide cutoff-ordering assertions remain a possible future
strengthening and are NOT claimed here.

---

## 3. Financial-data invariants — enforcement evidence

Each hard rule is listed with the test that can actually catch its violation.
For every rule below, a mutation audit confirmed the listed test fails when the
rule is broken (mutation killed), rather than passing silently.

| Hard rule | Enforcement test(s) | Mutation verdict |
|---|---|---|
| NULL != 0 | `test_extraction_keeps_blank_and_explicit_zero_distinct`; `test_null_and_explicit_zero_persist_as_distinct_values` | NULL→0 coercion KILLED |
| Exact Decimal values | `test_representative_codal_layouts_extract_rows` (value is None or Decimal); `test_locked_codal_corpus_persistence_satisfies_hard_invariants` | type mutation KILLED |
| Provenance / FK integrity | `test_locked_codal_corpus_persistence_satisfies_hard_invariants` | company_id drift KILLED |
| ASCII-normalized text (no Persian digits) | `test_locked_codal_corpus_persistence_satisfies_hard_invariants`; `test_codal_raw_text_fields_are_ascii_normalized_before_persistence` | Persian-digit injection KILLED |
| Exactly one current ReportVersion | `test_locked_codal_corpus_persistence_satisfies_hard_invariants` (per PDF) | extra-version KILLED |
| Deterministic extraction (A == B == C) | `test_locked_codal_corpus_extraction_is_deterministic_across_three_independent_runs` | by construction (compares 3 independent runs) |
| Idempotent ingestion (no duplicate facts/versions) | `test_locked_codal_corpus_ingestion_is_idempotent_across_three_cycles` | duplicate fact KILLED |
| No partial writes on failure | `test_malformed_pdf_is_rejected_and_ingestion_is_audited` (asserts 0 reports / 0 facts after failure) | failure leaves nothing by construction |
| Unit and currency distinct / preserved | fact fields persisted verbatim in `test_locked_codal_corpus_persistence_satisfies_hard_invariants` | preserved by snapshot equality in Layer E |

Rules that are structural to FX/market paths (IRR vs Toman, FREE_MARKET vs
OPERATIONAL FX) are outside the CODAL corpus scope and remain covered by the
existing FX ingestion tests (`test_ingestion_fx.py`), which were part of the
green full-suite regression.

---

## 4. Golden status

```text
GOLDEN SOURCE STATUS: BLOCKED
```

This is unchanged and is the correct state. No independent authoritative
source exists for any of the 19 PDFs, so no Golden expected values may be
constructed. This is a required safety rule for a financial-data system, not a
gap to close. Evidence and the unblocking criteria are recorded in
`golden_source_verification_report.md` and `golden_dataset_schema.md`.

Specifically rejected as Golden evidence: production extractor output,
production database rows, fixtures copied from production, a second parser on
the same PDF, reconstructed PDF text, and synthetic test metadata.

---

## 5. CI status

Workflow: `.github/workflows/tests.yml` (job `test`, `ubuntu-latest`, Python
3.12), command `PYTHONPATH=. pytest src/tests -v`, on push/PR to `master`.

The local CI-equivalent run (same command, same corpus) is the evidence used
here, because the new commits had not been pushed at audit time. Status by the
documented terminology:

- Before the fixture isolation fix, the full suite was **CI FAILED**
  (2 failed, 5 errors) though single-file runs were green — the exact
  "local PASS is not final evidence" hazard the validation programme warns
  about. That failure is fixed and verified.
- Final state: **234 passed, 2 skipped**, no failures, no errors.

CI status for the pushed commits themselves is **CI NOT RUN** until the commits
are pushed and the workflow executes; the local CI-equivalent evidence above is
what the final state was validated against.

---

## 6. Architecture and contract integrity

```text
PRODUCTION CODE CHANGED: NO
ARCHITECTURE CHANGED: NO
DATABASE_CONTRACT_V1.3 CHANGED: NO
NINE-STAGE ARCHITECTURE: UNCHANGED
STAGE 10 CREATED: NO
ANALYTICAL LOGIC IN INGESTION: NO
GOLDEN VALUES INVENTED: NO
TESTS WEAKENED: NO
```

Every commit in the series touched only files under `src/tests/` plus
`.gitignore`. Zero production source files were modified. The locked CODAL
boundary is intact:

```text
PDF / external source
  → extraction adapter
  → Sequence[RawLineInput]
  → ingest_codal_report()
  → database foundation
```

No KPI mapping, scoring, forecasting, valuation, or decision logic was
introduced into the ingestion path.

---

## 7. Honest remaining limitations

1. **Layer H** deep PIT assertions are single-PDF (see scope note).
2. **Golden accuracy** remains BLOCKED pending an independent authoritative
   source; this is intentional and correct.
3. **CI on the remote** has not executed for the new commits (not yet pushed);
   evidence is the local CI-equivalent run of the identical command and corpus.
4. **No production load** was performed or claimed; this series validates the
   validation system and ingestion invariants, not a populated production
   database.

---

## 8. Completion of the original programme

The original programme required evidence for: all 19 PDFs covered; extraction
validation; persistence validation; end-to-end validation; deterministic
repeated extraction; repeated idempotent ingestion; failure/recovery;
PIT/version integrity; full regression; CI verification; Golden validation
where and only where independent authoritative data exists; no architecture
drift; no `DATABASE_CONTRACT_V1.3` drift; no silent financial-data corruption.

Each is addressed above with its verification status. The single intentionally
unresolved item is Golden accuracy, which is BLOCKED by design and must not be
resolved by fabricating expected values.
