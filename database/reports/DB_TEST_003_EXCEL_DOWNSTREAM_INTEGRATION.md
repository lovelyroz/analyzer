# DB-TEST-003 - Excel integration and downstream contracts

Status: `PARTIAL` (owner tests accepted)

## Integration path exercised

The integration tests call the public `adapt_excel_source()` interface with in-memory synthetic XLSX bytes. That function invokes the actual `read_excel_source()` reader, `match_template()` with a synthetic `TemplateVersion`, candidate construction and submission, and, when explicitly requested, `prepare_canonical_batch()`. These fixtures demonstrate the code path only; they are not production template or mapping approvals.

## Coverage added and strengthened

Two new test functions were added to `src/tests/test_excel_adapter.py`:

- `test_instant_period_and_exact_decimal_survive_the_full_chain` exercises an explicitly selected INSTANT Jalali period and verifies its type, equal start/end, absent duration basis, source coordinate on the candidate, and exact `Decimal` retained in the plan.
- `test_duplicate_and_conflicting_facts_keep_all_or_nothing_admission_semantics` verifies that identical same-identity facts collapse with `duplicate_count == 1`, while differing values for the same identity return `INTRA_BATCH_CONFLICT` and no partial plan or submissions.

Existing full-chain cases were strengthened:

- The successful admission case asserts explicit company, report type/version, metric, unit, currency, scale, period mapping, exact source decimal, the plan's integer projection, Jalali period identity, duration basis, source artifact hash, template identity/hash, extraction owner, approval references, and the execution-disabled/non-persistence-compatible plan flags.
- The YTD/STANDALONE multi-period case asserts both distinct period identities, explicit bases, exact source decimals, integer values, and source coordinates.
- Fingerprint rejection now uses a separately generated workbook with changed source content and the original expected hash.
- Selection validation now covers an explicitly unapproved currency mapping.
- The partially invalid owned unit is exercised with admission requested and verifies deterministic diagnostics, no submissions, and no plan.

Existing adapter tests continue to cover blank versus reported zero versus approved ZERO_FALLBACK, formula rejection, unapproved templates, wrong worksheet identity, missing and ambiguous selections, and deterministic fail-closed behavior. No existing assertions were weakened.

## Downstream contracts and concrete blocker

The chain genuinely exercises the reader observation contract, approved structural matcher, candidate/submission DTOs, and the pure all-or-nothing admission plan. It verifies period identity as `(temporal_type, Jalali start, Jalali end)`, explicit `duration_basis`, metric identity, source units/currency/scale, source `Decimal`, and the plan's separate rounded integer projection.

No supported production bridge currently accepts `CanonicalPersistencePlan` or `PlannedFact` and writes to the downstream ORM contracts. `src/forecast/queries.py` reads `NormalizedFinancialFact` joined to `FinancialMetric`, `ReportVersion`, and `FinancialPeriod`; `src/models/normalized.py` requires database IDs and stores `value_irr` as `Numeric(30,4)`; `src/models/period.py` stores Gregorian dates and period-wide `is_ytd`. The available `src/ingestion/service.py` is the existing raw-row ingestion path, not a canonical-plan writer. Creating a bridge would exceed this test task's boundaries, so consumer-level period/date, unit conversion, metric-ID mapping, numeric storage, publication, and transaction behavior remain unproven.

Source coordinates are retained on `CanonicalInputCandidate` in each adapter submission. They are not fields on `PlannedFact`, consistent with the current Section 3.11 decision not to require permanent exact cell locators. Therefore the tests assert the coordinate at the candidate/submission boundary and do not claim it is persisted downstream.

Synthetic fixtures do not establish production template approval, authenticated company/report/metric/unit/currency/scale mappings, production period mapping, or an approved extraction standard. Those approvals and the canonical ORM writer remain open blockers. No production approval is inferred by these tests.

## Changed files

- `src/tests/test_excel_adapter.py`
- `database/reports/DB_TEST_003_EXCEL_DOWNSTREAM_INTEGRATION.md` (this report)
- `database/reports/DB_TEST_002_CORRECTION.md` (owner acceptance recorded)
- `database/DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md` (Sections 9.40, 9.42, and new 9.43)
- `reply.md`

No production module, ORM/model, schema, migration, database, or `WORKFLOW_RULES.md` was changed. The pre-existing workspace modification to `prompt.md` was preserved.

## Static checks and test status

Static AST parsing and inspection of the public call chain and downstream interfaces were performed. The test file has two new test functions; existing functions were extended. `git diff --check` was run. Tests were not run by the agent, as required by `PROMPT.md`.

Owner command:

```powershell
.\.venv\Scripts\python.exe -m pytest -q --basetemp .pytest_task019_20261121 src/tests/test_excel_adapter.py src/tests/test_excel_canonical_input.py src/tests/test_excel_template_matching.py src/tests/test_excel_source_reader.py src/tests/test_canonical_ingestion_admission.py src/tests/test_stage6_evaluation_foundation.py src/tests/test_stage6_p25_selection.py
```

Owner acceptance for the command above was reported exactly as:

```text
115 passed in 2.75s
```

Task 019 remains `PARTIAL`: production template and semantic mapping approvals are unavailable, no physical writer connects the plan to downstream ORM models, and compatibility with `NormalizedFinancialFact` / `FinancialPeriod` has not been proven. The owner test result does not resolve those blockers. Dashboard totals were not changed.
