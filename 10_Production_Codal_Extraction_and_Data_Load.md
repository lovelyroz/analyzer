# Analyzer V1 — Production CODAL Extraction & Data Load

## Phase status

This is **not Analytical Stage 10**.

Stages 1–9 and `DATABASE_CONTRACT_V1.3` remain locked. This prompt starts the next operational implementation phase: turning the locked ingestion boundary into a production-capable data acquisition pipeline.

## Mission

Implement production data acquisition and loading on top of the existing locked ingestion framework, beginning with CODAL PDF acquisition/extraction and then integrating production market/FX sources where explicitly available.

The immediate gap intentionally deferred by CHANGE-007 is:

```text
CODAL PDF / external source
        ↓
PDF extraction adapter
        ↓
Sequence[RawLineInput]
        ↓
ingest_codal_report()
        ↓
DB foundation
```

Do not redesign this boundary.

## Authoritative sources

Read before changing anything:

1. `00_a_Master_Architecture.md`
2. `00_Architecture_Freeze_Point.md`
3. `01_Stage1_Data_Foundation.md`
4. `11_Database_Architecture_Stage1.md`
5. `12_Database_Architecture_V1.1.md` — current body is `DATABASE_CONTRACT_V1.3`
6. `99_Architecture_Change_Log.md` — especially CHANGE-001 through CHANGE-007
7. `10_Implementation_Status.md`
8. Existing ingestion code under `src/ingestion/`
9. Existing tests under `src/tests/`

Authority order remains unchanged. This prompt is an execution instruction, not a new architectural specification.

## Locked constraints

- Exactly nine analytical stages remain in Analyzer V1.
- Do not create an analytical Stage 10.
- Do not reopen or redesign Stages 1–9.
- Do not change `DATABASE_CONTRACT_V1.3` unless a genuine architectural contradiction is demonstrated.
- Do not silently add a new database entity because extraction is inconvenient.
- Preserve raw source data and provenance.
- `NULL != 0`.
- Point-in-Time correctness remains mandatory.
- Report and ReportVersion remain separate.
- Historical report versions must remain reproducible.
- Raw facts remain immutable.
- Use `NormalizedFinancialFactInput` for multi-source normalized provenance.
- FREE_MARKET and OPERATIONAL FX remain separate.
- Operational FX must never silently default to FREE_MARKET.
- Persist FX rates in IRR; explicit Toman→Rial conversion belongs at the adapter boundary.
- Market Jalali dates remain source components; do not silently convert them to Gregorian.
- CODAL extraction must produce `RawLineInput` and must not perform KPI mapping, scoring, forecasting, valuation, or decision logic.
- Production ingestion must be idempotent.
- Failed ingestion must be auditable through `IngestionRun` and must not leave partial report/raw writes.
- Never overwrite historical report versions merely to simplify ingestion.

## Workstream A — CODAL production extraction

Implement a real CODAL PDF extraction adapter behind the existing `extract_raw_lines_from_pdf()` boundary.

Requirements:

1. Inspect representative CODAL PDFs before choosing an extraction strategy.
2. Keep PDF acquisition separate from PDF parsing.
3. Preserve source metadata such as:
   - CODAL tracking ID
   - source URL
   - title
   - report type
   - publication datetime
   - restatement/correction information where available
4. Extract source lines into `RawLineInput` without mapping them to standardized financial metrics.
5. Preserve source section, row, column, item name/code, unit, currency, and value whenever available.
6. Handle Persian text, Persian/Arabic digits, separators, negative values, parentheses, blanks, and explicit missing values without turning missing into zero.
7. Do not invent values when extraction is uncertain. Record extraction failures or quality diagnostics explicitly.
8. Keep the extraction implementation replaceable. The selected PDF/OCR/table library is an implementation detail, not a new database contract.
9. Do not embed extraction-specific assumptions in `service.py`.

If a PDF requires OCR or a specialized table extractor, isolate that dependency under the CODAL extraction package and document why it is required.

## Workstream B — CODAL source acquisition

Add a source acquisition layer only if the available source can be accessed reliably and legally within the project environment.

Requirements:

- acquisition must be retryable and observable;
- preserve source URL and source identity;
- distinguish acquisition failure from extraction failure;
- never silently substitute a different report;
- make duplicate acquisition idempotent;
- do not couple acquisition to database persistence.

If live acquisition is environment-dependent, provide a deterministic local-file path through the same adapter boundary and document the limitation rather than faking live connectivity.

## Workstream C — Production loading

After extraction is validated, connect the adapter outputs to the existing core persistence functions.

For CODAL:

`extract → validate → RawLineInput[] → ingest_codal_report()`

For market:

`source adapter → existing market DTOs → existing market persistence`

For FX:

`source adapter → FxRateInput[] → existing FX persistence`

Do not introduce analytical calculations into these paths.

## Workstream D — Data quality and observability

Every production path must make the following distinguishable:

- acquired successfully;
- parsed successfully;
- partially parsed;
- rejected;
- failed;
- missing source;
- estimated value;
- suspicious value;
- unmapped value.

Use existing data-quality and `IngestionRun` mechanisms where applicable. Do not invent a parallel audit system.

## Tests required

Add focused tests for:

### CODAL
- PDF extraction of representative report layouts
- Persian digits and numeric normalization
- missing vs zero
- negative values
- item metadata preservation
- section/row/column provenance
- malformed/unsupported PDF behavior
- deterministic extraction
- adapter output compatibility with `RawLineInput`
- core persistence of extracted DTOs
- ReportVersion creation and version sequencing
- idempotent re-ingestion
- failed ingestion leaves no partial Report/RawFinancialFact writes
- IngestionRun audit
- PIT publication datetime preservation

### Acquisition
- successful acquisition
- duplicate/idempotent acquisition
- acquisition failure
- extraction failure after acquisition
- no silent source substitution

### Regression
- full existing test suite
- no regression in Market/OHLC ingestion
- no regression in FX ingestion
- no regression in Stages 1–9

## Architecture audit rules

Before modifying architecture, ask:

1. Is the requirement already covered by the locked contract?
2. Can it be implemented behind the existing adapter boundary?
3. Can it be solved without changing database ownership?
4. Can it be solved without changing analytical ownership?

If yes, implement without an architecture change.

If a genuine contradiction remains, **stop before changing the contract**, document the exact contradiction, and use the architecture change-control process.

## Execution sequence

**READ → INSPECT → IDENTIFY → DESIGN → IMPLEMENT → TEST → AUDIT → DIFF-CHECK → CI → AUDIT**

Do not skip CI.

CI evidence must come from the actual workflow run for the final audited commit.

## Completion criteria

This operational phase is complete only when:

- a real CODAL PDF extraction implementation exists behind the locked boundary;
- extraction is deterministic and tested on representative PDFs;
- extracted lines can flow into the existing CODAL core persistence path;
- provenance and PIT rules are preserved;
- acquisition and extraction failures are distinguishable and auditable;
- ingestion is idempotent;
- missing values are not converted to zero;
- no analytical logic has leaked into ingestion;
- existing Market/FX ingestion remains green;
- the complete regression suite passes;
- CI passes on the final commit;
- audit confirms no architecture drift.

## Final report

Return:

- files changed;
- source acquisition approach;
- PDF extraction approach and dependency;
- representative layouts tested;
- test count and result;
- CI run ID and final commit;
- audit result;
- remaining explicit limitations;
- confirmation that the nine-stage Analyzer architecture and `DATABASE_CONTRACT_V1.3` remain locked.
