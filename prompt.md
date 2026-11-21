# Task 019 — DB-TEST-003: Excel Integration and Downstream Contract Tests

## Execution mode
**CODE + TEST IMPLEMENTATION.** Do not perform a report-only audit. Make concrete progress on Task 019.

## Mandatory first action: record owner acceptance

The owner has executed the DB-TEST-002 correction test command. Exact result:

`167 passed in 55.40s`

Update all relevant records:
1. `database/DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md`, §9.42
2. `database/reports/DB_TEST_002_CORRECTION.md`
3. The Task 018 / DB-TEST-002 status entry, where appropriate.

Record this as owner-run acceptance of the corrected Stage 6 test suites. Do not mark DB-TEST-002 fully DONE if its broader integration or production limitations remain. Do not change dashboard percentages unless you recalculate the complete task denominator and all task statuses.

## Main implementation: Task 019 / DB-TEST-003

The Master Packet defines Task 019 as:

> تست یکپارچهٔ Excel و downstream contracts: adapter و مسیر Excel صورت‌های مالی به ورودی canonical مصوب برسند و مصرف‌کنندگان downstream بدون تغییر معنای دوره/مقدار کار کنند. این Task شامل تست PDF نیست.

Implement the strongest integration coverage currently possible, using the existing architecture and real public interfaces.

### Required inspection
Read the actual implementations and existing tests for:
- `src/ingestion/excel/reader.py`
- `src/ingestion/excel/deterministic_matcher.py`
- `src/ingestion/excel/canonical_input.py`
- `src/ingestion/excel/adapter.py`
- `src/ingestion/canonical_admission.py`
- Relevant Stage 1 / downstream period and financial-value consumers.
- Existing Excel adapter, canonical admission, temporal semantics, and Stage 6 tests.

Do not repeat broad repository audits. Follow the actual call chain and identify which downstream interfaces can currently consume the canonical output.

### Implementation requirements

1. Add or extend focused integration tests that exercise the real chain:

   `synthetic XLSX → read_excel_source → approved synthetic TemplateVersion → match_template → adapt_excel_source → canonical candidate submission → prepare_canonical_batch`

2. The synthetic template and explicit semantic/temporal selections are test fixtures only. Label them clearly as synthetic; they are not production approvals.

3. Test both successful and fail-closed paths:
   - Correct source fingerprint and matching template.
   - Explicit company/report/version/metric/unit/currency/scale approvals.
   - Explicit Jalali period mapping.
   - INSTANT versus DURATION.
   - YTD versus STANDALONE.
   - Exact preservation of source value, including zero versus missing.
   - Provenance and source coordinates survive the entire chain.
   - A changed source workbook or mismatched fingerprint is rejected.
   - Missing, ambiguous, or unapproved selections are rejected.
   - A partially invalid batch does not produce an accepted partial plan.
   - Duplicate/conflicting facts retain the existing admission semantics.

4. Test downstream compatibility using existing real consumer interfaces wherever a supported bridge exists. In particular, check that period identity, duration basis, metric identity, and numeric value are not silently changed or inferred.

5. If there is no actual production bridge from `CanonicalPersistencePlan` / `PlannedFact` to a downstream consumer, do not invent one merely to make an integration test pass. Record the missing bridge as a concrete blocker, with exact modules/interfaces involved.

6. Do not introduce inferred financial semantics, automatic YTD-to-standalone conversion, guessed metric mappings, or guessed units/scales.

7. Keep the implementation deterministic and independent of external CODAL access or user-specific workbook files. Do not claim that synthetic fixtures prove production template readiness.

### Strict boundaries

- No ORM/model changes.
- No schema or migration changes.
- No database writes or real ingestion.
- No changes to `WORKFLOW_RULES.md`.
- No PDF extraction code, tests, fixtures, or fallback.
- Do not weaken existing tests or alter production contracts just to satisfy fixtures.
- Do not add a production template or mark any synthetic mapping as owner-approved.
- Do not run tests; the owner runs them.

### Deliverables

1. Focused integration test file(s), preferably extending existing relevant test files rather than creating unnecessary duplicate suites.
2. `database/reports/DB_TEST_003_EXCEL_DOWNSTREAM_INTEGRATION.md`, containing:
   - Exact integration path exercised.
   - Test cases and assertions added.
   - Which downstream contracts were genuinely exercised.
   - Which bridges or production approvals remain unavailable.
   - Exact changed-file list.
   - Static checks performed.
   - Explicit statement that tests were not run by the agent.
   - Exact owner test command.
3. Update `reply.md` with:
   - Owner acceptance: `167 passed in 55.40s`.
   - Task 019 implementation summary and status.
4. Update `database/DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md`:
   - Record the 167-pass owner acceptance under §9.42.
   - Add a new evidence section for Task 019.
   - Update Task 019's status accurately.
   - Do not mark it DONE while production template/mapping approval or a required downstream bridge remains unproven.
   - Do not silently alter dashboard totals.

### Final response format

Return:
- `DONE`, `PARTIAL`, or `BLOCKED` for Task 019.
- Owner acceptance recording status for Task 018.
- Exact files created/modified.
- Number and purpose of tests added.
- Concrete blockers, if any.
- Exact owner test command.
- Explicit confirmation that no tests were run by the agent.

Do actual implementation. Do not return another broad audit or a list of recommendations instead of code.