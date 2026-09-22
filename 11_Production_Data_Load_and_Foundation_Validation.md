# Analyzer V1 — Production Data Load & Foundation Validation

## Phase status

This is **not Analytical Stage 10 or any new analytical stage**.

It is the next operational phase after the locked CODAL PDF extraction implementation.

The following remain locked:

- Analyzer V1 — exactly nine analytical stages
- `DATABASE_CONTRACT_V1.3`
- Stage 1–9 contracts
- CHANGE-007 ingestion boundary
- CODAL PDF extraction implementation boundary

## Mission

Load the required real production data into the existing Stage 1 foundation through the already-validated ingestion paths, then prove that the resulting foundation dataset is complete, consistent, auditable, idempotent, and safe for downstream analytical stages.

The target is:

```text
Real source data
      ↓
Validated source acquisition
      ↓
Existing adapters
      ↓
Existing common DTOs
      ↓
Existing core persistence
      ↓
Stage 1 foundation DB
      ↓
Foundation validation
```

Do not introduce analytical calculations into this phase.

## Authoritative sources

Read before implementation:

1. `00_a_Master_Architecture.md`
2. `00_Architecture_Freeze_Point.md`
3. `01_Stage1_Data_Foundation.md`
4. `11_Database_Architecture_Stage1.md`
5. `12_Database_Architecture_V1.1.md` — current body = `DATABASE_CONTRACT_V1.3`
6. `99_Architecture_Change_Log.md`
7. `10_Implementation_Status.md`
8. `prompts/10_Production_Codal_Extraction_and_Data_Load.md`
9. Existing ingestion code under `src/ingestion/`
10. Existing tests under `src/tests/`

## Locked constraints

- Do not create an analytical Stage 10.
- Do not reopen Stages 1–9.
- Do not change `DATABASE_CONTRACT_V1.3` unless a genuine architectural contradiction is demonstrated.
- Do not add analytical logic to ingestion.
- Raw source data remains immutable.
- `NULL != 0`.
- PIT correctness is mandatory.
- Report and ReportVersion remain separate.
- Historical report versions must remain reproducible.
- FREE_MARKET and OPERATIONAL FX remain separate.
- Operational FX must not silently default to FREE_MARKET.
- Persisted FX rates are IRR; Toman→Rial conversion occurs only at the adapter boundary.
- Jalali source components must not be silently converted to Gregorian.
- Ingestion remains idempotent.
- Failed loads must be auditable through `IngestionRun`.
- No silent source substitution.
- No silent missing-data substitution.

## Workstream A — Define the production universe

Before loading large volumes, explicitly define:

### CODAL

- companies/symbols in scope;
- report types in scope;
- financial periods required;
- historical start/end dates;
- required report versions;
- correction/restatement handling;
- source acquisition identity.

### Market

- companies/symbols in scope;
- required date range;
- OHLC fields required;
- Jalali date policy;
- adjusted-close availability.

### FX

- required date range;
- FREE_MARKET sources;
- OPERATIONAL/EXCHANGE sources;
- source units;
- Jalali date policy;
- required currencies.

The production universe must be explicit and reproducible. Do not load arbitrary files merely because they exist locally.

## Workstream B — Acquisition

For each source:

1. Acquire the exact intended source.
2. Record source identity.
3. Validate file/content type.
4. Detect duplicates before persistence.
5. Distinguish acquisition failure from extraction/parsing failure.
6. Never substitute another report or source silently.
7. Preserve enough metadata to reproduce the acquisition decision.

Where live acquisition is unreliable, use deterministic local source manifests and document the limitation.

## Workstream C — CODAL production load

For each selected report:

```text
Acquire
  ↓
Extract
  ↓
Validate extraction
  ↓
RawLineInput[]
  ↓
ingest_codal_report()
  ↓
Report / ReportVersion / RawFinancialFact
```

Validate:

- company identity;
- tracking ID;
- source URL;
- report title/type;
- financial period;
- publication datetime;
- version sequence;
- correction/restatement relationships;
- section/row/column provenance;
- unit and currency;
- numeric values;
- explicit missing values;
- ASCII textual digits;
- raw immutability;
- PIT metadata.

Do not map source lines to Stage 2 KPIs in this phase.

## Workstream D — Market production load

Use the existing market adapter and persistence path.

Validate:

- company identity;
- Jalali year/month/day;
- trade date where available;
- OHLC;
- adjusted close;
- volume;
- value;
- trade count;
- source identity;
- duplicate handling;
- missing fields;
- date-range continuity.

Do not invent missing OHLC values.

## Workstream E — FX production load

Use the existing FX adapter and persistence path.

Validate separately:

- FREE_MARKET;
- OPERATIONAL;
- OFFICIAL where applicable;
- source identity;
- Jalali components;
- Gregorian date only where legitimately supplied;
- rate unit;
- Toman→Rial conversion;
- duplicate identity;
- same-day coexistence of different rate types.

Never merge FREE_MARKET and OPERATIONAL into one rate.

## Workstream F — Foundation validation

After loading, run deterministic validation reports/checks for:

### Completeness

- expected companies vs loaded companies;
- expected report periods vs loaded periods;
- expected market dates vs loaded dates;
- expected FX dates vs loaded dates.

### Uniqueness

- duplicate reports;
- duplicate ReportVersions;
- duplicate market rows;
- duplicate FX identities.

### PIT

For selected historical cutoffs:

```text
publication_datetime <= cutoff
```

must be enforced when selecting report versions.

### Data quality

Count and surface:

- VALID
- MISSING
- ESTIMATED
- RESTATED
- SUSPICIOUS
- UNMAPPED

Do not hide these categories.

### Units

Verify:

- financial facts in expected accounting currency;
- FX persisted in IRR;
- free-market Toman inputs converted exactly once;
- no downstream Toman/Rial ambiguity.

### Provenance

For important loaded facts, verify the trace:

```text
RawFinancialFact
 → ReportVersion
 → Report
 → source metadata
```

For normalized multi-source facts:

```text
NormalizedFinancialFact
 → NormalizedFinancialFactInput[]
 → RawFinancialFact
 → MappingDecision
```

## Workstream G — Idempotency and failure safety

Repeat representative loads.

Expected behavior:

- no duplicate logical records;
- no second current ReportVersion for the same Report;
- no corruption of existing raw records;
- deterministic result.

Also test:

- malformed CODAL PDF;
- invalid market row;
- invalid FX row;
- acquisition failure;
- extraction failure.

Failed operations must not leave partial foundation records.

## Workstream H — Regression

Run the complete existing suite:

```text
pytest src/tests -v
```

The following must remain green:

- Stage 1 database tests;
- CODAL extraction tests;
- Market/OHLC ingestion;
- FX ingestion;
- migrations;
- all Stage 1–9 regression tests.

## Audit requirements

Before declaring completion, verify:

1. No architecture drift.
2. No contract changes.
3. No analytical logic leaked into ingestion.
4. No silent substitutions.
5. No missing→zero conversions.
6. No FREE_MARKET/OPERATIONAL merge.
7. No PIT violation.
8. No raw immutability violation.
9. No duplicate current ReportVersion.
10. No unexplained production gaps.
11. All material failures are observable through existing audit mechanisms.
12. The loaded foundation can support downstream Stage 2–9 execution without changing the Stage 1 contract.

## Execution sequence

**READ → INSPECT → DEFINE UNIVERSE → ACQUIRE → LOAD → VALIDATE → IDEMPOTENCY TEST → REGRESSION → AUDIT → DIFF-CHECK → CI → FINAL AUDIT**

Do not skip CI.

CI evidence must correspond to the final audited commit.

## Completion criteria

This operational phase is complete only when:

- the production universe is explicitly defined;
- required CODAL data is loaded;
- required market data is loaded;
- required FX data is loaded;
- acquisition and ingestion failures are distinguishable;
- completeness and duplicate checks pass or have explicitly documented exceptions;
- PIT selection is validated;
- provenance is validated;
- units are validated;
- idempotent re-run is validated;
- failure safety is validated;
- full regression passes;
- CI passes on the final commit;
- final audit confirms no architecture drift.

## Important boundary

Completion of this phase means the **Stage 1 production foundation is loaded and validated**.

It does **not** mean that downstream analytical stages should immediately be recalculated blindly.

After this phase, the next controlled activity is to run Stage 2–9 analytical pipelines against the validated foundation data, with the existing contracts and versioning rules.

## Final report

Return:

- production universe;
- source inventory;
- acquisition results;
- loaded record counts by domain;
- rejected/failed records and reasons;
- data-quality summary;
- PIT validation result;
- idempotency result;
- regression test count/result;
- CI run ID and final commit;
- audit result;
- explicit limitations;
- confirmation that Analyzer V1 architecture and `DATABASE_CONTRACT_V1.3` remain locked.
