# CODAL 19-PDF Validation Plan

## Objective

Establish a repeatable, multi-layer validation strategy for the full representative CODAL corpus in the repository. The validation scope is the complete set of 19 real PDF files and not just the earlier four integration samples.

## Validation scope

Current corpus:

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

## Execution order

### 1. Inventory

- What is being tested: completeness of the 19-PDF validation corpus
- Why it matters: prevents accidental scope reduction to four samples
- Source of truth: filesystem inventory of the repository PDF directory
- Expected invariant: exactly 19 real PDF samples are included in the validation scope
- Repetition requirement: one baseline inventory pass, repeated after any file additions or removals
- Failure classification: SCOPE_ERROR if corpus size or file set differs from the expected 19-PDF representative corpus

### 2. Extraction validation

- What is being tested: PDF → RawLineInput conversion across the full corpus
- Why it matters: extraction contract is the first boundary and must preserve raw facts without inventing or normalizing away missingness
- Source of truth: PDF bytes and the extraction implementation contract
- Expected invariant: extraction succeeds explicitly or fails explicitly; no fabricated values; normalized digits; correct separators; negative values preserved; blanks remain missing; NULL is not converted to zero; source section/row/column and raw item metadata are preserved
- Repetition requirement: run on all 19 PDFs, re-run after contract or parser changes
- Failure classification: EXTRACTION_CONTRACT_FAILURE, INVALID_NORMALIZATION, NULL_ZERO_CONVERSION, SOURCE_METADATA_LOSS

### 3. Persistence validation

- What is being tested: RawLineInput → database foundation persistence
- Why it matters: financial integrity depends on exact Decimal values, NULL semantics, provenance, and FK correctness
- Source of truth: database contract and persisted foundation records
- Expected invariant: Report, ReportVersion, FinancialPeriod, RawFinancialFact, and IngestionRun are created with valid relationships and correct semantics
- Repetition requirement: run on all 19 PDFs and after schema or persistence changes
- Failure classification: PERSISTENCE_CONTRACT_FAILURE, DECIMAL_PRECISION_FAILURE, NULL_ZERO_ERROR, FK_INTEGRITY_FAILURE, PROVENANCE_FAILURE

### 4. End-to-end production integration

- What is being tested: full PDF → acquisition → extraction → validation → persistence path
- Why it matters: verifies that the real production flow works as a pipeline without partial writes or silent data loss
- Source of truth: full production ingestion path and IngestionRun audit trail
- Expected invariant: successful documents create expected foundation records; failed documents fail explicitly; all errors remain auditable; no partial financial writes occur
- Repetition requirement: run across all 19 PDFs and rerun after relevant pipeline changes
- Failure classification: ACQUISITION_FAILURE, EXTRACTION_FAILURE, VALIDATION_FAILURE, PERSISTENCE_FAILURE, PARTIAL_WRITE_FAILURE, AUDIT_FAILURE

### 5. Determinism

- What is being tested: repeated extraction stability for the same source PDF
- Why it matters: financial applications need deterministic extraction to avoid hidden drift
- Source of truth: repeated extraction results for each PDF
- Expected invariant: A == B == C for the same normalized RawLineInput outputs unless the extractor explicitly documents a nondeterministic field
- Repetition requirement: minimum 3 extraction runs per PDF
- Failure classification: NONDETERMINISTIC_EXTRACTION, OUTPUT_DRIFT, NORMALIZATION_DRIFT

### 6. Idempotency

- What is being tested: repeated ingestion behavior for each PDF
- Why it matters: the same source identity must not create duplicate immutables or logical drift
- Source of truth: persisted rows before and after repeated ingestion
- Expected invariant: after the first successful ingestion, repeated ingestion leaves the logical database unchanged; duplicates are prevented; provenance is preserved
- Repetition requirement: minimum 3 ingestion cycles per PDF
- Failure classification: IDEMPOTENCY_FAILURE, DUPLICATE_REPORT_VERSION, DUPLICATE_FACT, SOURCE_IDENTITY_DRIFT

### 7. Failure / recovery

- What is being tested: malformed PDFs, unsupported structures, acquisition failure, extraction failure, validation failure, and rollback behavior
- Why it matters: financial systems must fail explicitly and never leave partial records behind
- Source of truth: negative-path tests and IngestionRun failure records
- Expected invariant: explicit failure status, no partial financial writes, safe retry behavior, auditable error classification
- Repetition requirement: representative failures across the corpus, repeated after code or failure-path changes
- Failure classification: MALFORMED_PDF, ACQUISITION_FAILURE, EXTRACTION_FAILURE, VALIDATION_FAILURE, DATABASE_ROLLBACK_FAILURE, RETRY_CORRUPTION

### 8. PIT / version / restatement

- What is being tested: publication datetime, report/version identity, and correction/restatement semantics
- Why it matters: historical report versions must remain reproducible and must not be overwritten silently
- Source of truth: version metadata, publication datetime, period metadata, and report lineage
- Expected invariant: PIT uses publication datetime; historical version preservation remains intact; corrections/restatements are handled without destructive overwrite
- Repetition requirement: applicable to all reports that carry version or period metadata, repeated after data or version logic changes
- Failure classification: PIT_FAILURE, VERSION_COLLISION, RESTATEMENT_MISCLASSIFICATION, HISTORICAL_OVERWRITE

### 9. Independent Golden validation where available

- What is being tested: authoritative expected data vs production result
- Why it matters: only independent evidence is allowed in Golden validation
- Source of truth: official CODAL records or another independent authoritative source
- Expected invariant: authoritative expected values match production outputs exactly, with explicit NULL vs Decimal("0") and independent provenance
- Repetition requirement: only when an authoritative source exists; no repetition without source quality evidence
- Failure classification: GOLDEN_NOT_AVAILABLE, GOLDEN_STATUS_BLOCKED, SOURCE_SUBSTITUTION, PROVENANCE_INCOMPLETE

### 10. Full regression

- What is being tested: repo-wide regressions after relevant changes
- Why it matters: CODAL validation must not destabilize other Stage 1–9 behavior
- Source of truth: full repository test suite
- Expected invariant: Stage 1–9 and related modules remain green after CODAL validation changes
- Repetition requirement: full regression run after modifications and again at final gate
- Failure classification: REGRESSION_FAILURE, STAGE_INTEGRATION_FAILURE

### 11. Final repeated validation

- What is being tested: multi-pass final evidence collection after all layers pass or remain intentionally blocked
- Why it matters: single successful run is not sufficient evidence for a financial system
- Source of truth: same set of validation steps executed in a defined repeat matrix
- Expected invariant: repeated runs confirm stable behavior and stable blocked status where authoritative Golden data is absent
- Repetition requirement: apply a defined repeatability matrix for extraction, persistence, idempotency, and final regression
- Failure classification: REPEATABILITY_FAILURE, UNSTABLE_BEHAVIOR, UNEXPLAINED_DRIFT

### 12. Final audit

- What is being tested: final gate review against the locked architecture and validation scope
- Why it matters: ensures that architecture controls and scope rules are preserved
- Source of truth: locked architecture, database contract, and validation artifacts
- Expected invariant: no architecture changes, no database-contract changes, no production-code changes for the validation-only phase, and no Golden values created without independent authority
- Repetition requirement: final pass before completion
- Failure classification: ARCHITECTURE_VIOLATION, DB_CONTRACT_CHANGE, PRODUCTION_CODE_CHANGE, GOLDEN_VALUE_INVENTION

## Required invariants

The following are hard invariants for this system:

- NULL != 0
- Exact Decimal values are compared exactly where exactness is required
- Unit != currency
- IRR remains distinct from Toman
- FREE_MARKET FX remains distinct from OPERATIONAL FX
- Operational FX must never silently fall back to FREE_MARKET
- Historical ReportVersions remain reproducible
- RawFinancialFact is immutable
- PIT is based on publication datetime
- No silent value invention
- No silent source substitution
- No partial writes on failed ingestion

## Golden gate

The Golden status remains BLOCKED unless an independently verified authoritative source exists for a given PDF or for the corpus as a whole.

This is not a quality concession. It is a required safety rule for a financial-data system.

## Acceptance criteria

The validation plan is considered complete only when:

- all 19 PDFs are included in the validation scope;
- the relevant validation layers are executed in order;
- repeated deterministic checks are executed;
- repeated idempotency checks are executed;
- full repository regression is executed after changes;
- Golden validation remains blocked unless external authoritative evidence exists;
- no production code or architecture boundary is changed during this validation-only phase.
