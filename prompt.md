# EXECUTION PROMPT — Task 014 / DB-ING-001
## Implement the canonical Excel-to-financial-input DTO boundary

**Repository:** `analyzer`  
**Branch:** `master`  
**Project:** `analyzer`  
**Work type:** CODE IMPLEMENTATION + TESTS  
**Priority:** High

### Objective

Implement the next concrete layer of the Excel-to-canonical ingestion path.

The current Excel observation DTO and Reader already exist. Do not rebuild them. Implement the missing boundary that converts structurally identified Excel observations into validated, immutable canonical-input candidates, with explicit per-value temporal and semantic context.

The purpose is to make each selected financial value independently identifiable and prevent guessing of its Metric, unit, period, or YTD/standalone basis.

### Authoritative documents — read first

1. `database/DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md`
2. `12_Database_Architecture_V1.1.md`
3. `database/reports/DB_DES_007_EXCEL_OBSERVATION_DTO_CONTRACT.md`
4. `database/reports/DB_DES_009_CANONICAL_FINANCIAL_FACT_PHYSICAL_MODEL.md`
5. `database/reports/DB_DES_011_JALALI_FINANCIAL_PERIOD_AND_TEMPORAL_BASIS.md`
6. `database/reports/DB_DES_013_DETERMINISTIC_EXCEL_TEMPLATE_MATCHING.md`
7. `database/reports/DB_DES_014_HIERARCHICAL_HEADER_SEMANTIC_COLUMN_MAPPING.md`

If a referenced path differs, locate the exact existing file. Do not create a replacement document.

### Existing implementation — inspect before editing

- `src/ingestion/excel/dto.py`
- `src/ingestion/excel/reader.py`
- `src/ingestion/excel/deterministic_matcher.py`
- `src/tests/test_excel_observation_dto.py`
- `src/tests/test_excel_source_reader.py`
- `src/tests/test_excel_template_matching.py`

### Required implementation

1. Add an immutable canonical-input candidate DTO. It must preserve:
   - Company identity reference.
   - Report type and report-version reference.
   - Approved template identity/version/hash.
   - Source workbook hash.
   - Source worksheet and exact cell/coordinate references.
   - Approved Metric identity.
   - Source label/header identity where applicable.
   - Numeric value without binary-float conversion or silent rounding.
   - Explicit source unit, currency and scale.
   - Explicit temporal type: `INSTANT` or `DURATION`.
   - Explicit Jalali period start/end components.
   - Explicit `duration_basis=YTD|STANDALONE` for DURATION only.
   - Approved dimensions and their identities, where applicable.

2. Implement a pure validation/builder boundary:
   - Accept only explicitly approved structural and semantic mappings.
   - Reject missing or ambiguous Metric, unit, currency, scale, period, or duration basis.
   - Reject inconsistent INSTANT/DURATION combinations.
   - Reject invalid Jalali dates and invalid period ranges.
   - Reject a DURATION fact without an explicit valid duration basis.
   - Reject an INSTANT fact with a duration basis.
   - Preserve zero versus missing; never turn missing into zero.
   - Never infer a period from column order, workbook title, publication date, or neighboring values.
   - Never infer a Metric from a Header name alone.
   - Never create implicit dimensions or default units.

3. Keep the implementation independent of persistence:
   - No ORM changes.
   - No schema or migration changes.
   - No database writes.
   - No canonical writer or ingestion activation.
   - No changes to existing financial data or workbook files.

4. Add focused tests for:
   - Valid INSTANT candidate.
   - Valid DURATION/YTD candidate.
   - Valid DURATION/STANDALONE candidate.
   - Missing Metric.
   - Ambiguous mapping.
   - Missing currency/unit/scale.
   - Missing period.
   - Invalid Jalali date/range.
   - Missing or invalid duration basis.
   - INSTANT with duration basis.
   - Missing versus explicit zero.
   - Numeric precision preservation.
   - Missing source coordinate/provenance.
   - Rejection of implicit/default semantic values.

### Important constraints

- Do not modify `WORKFLOW_RULES.md`.
- Do not modify existing approved owner decisions.
- Do not reopen decisions already settled in the Master Packet.
- Do not connect this implementation to the Parsian draft template.
- Do not create fake approved mappings or fake Metric IDs.
- Do not weaken fail-closed behavior to make tests pass.
- Do not run tests on the owner's real database.
- Do not claim Task 014 is DONE merely because the DTO is implemented.

### Deliverables

1. Working implementation and focused tests.
2. Exact list of changed/added files.
3. Exact test commands and actual outputs.
4. A short implementation report:
   `database/reports/DB_ING_001_CANONICAL_INPUT_DTO_IMPLEMENTATION.md`
5. Update `reply.md` with the execution result.
6. Update the Master Packet:
   - Record the implementation evidence under a new §9 entry.
   - Update Task 014 status only according to its actual acceptance criteria.
   - Recalculate the progress dashboard.
   - Do not mark Task 014 DONE if any required behavior remains unimplemented.

### Completion standard

Deliver executable code and tests, not another architecture proposal or inventory report.

If a contract conflict blocks implementation, identify the exact conflicting clauses and implement every independent, non-conflicting part. Do not stop the entire task because one isolated item is unresolved.