# TASK 4 — CLOSE MARKET/FX SOURCE PROVENANCE GAPS

## Master Packet mapping

- Task 025 — DB-STD-005
- Task 009 — DB-DES-004
- DB-AUD-001 — Market/FX evidence review

This is an evidence acquisition and source-tracing task. The goal is to obtain concrete source evidence and close as many provenance gaps as possible. Do not merely restate existing documentation.

## 1. CODAL / MarketDaily — trace the actual CSV

Investigate `saman_price_history.csv`.

Actions:
1. Inspect project-local scripts and configuration that the owner has made available for downloading or producing this CSV.
2. Identify the exact CODAL endpoint, page, query parameters, company identifier, symbol, and extraction method used.
3. Determine whether the script retrieves official published data directly or transforms an intermediate source.
4. Identify available CODAL publication identifiers, tracking IDs, publication timestamps, correction indicators, and any source-issued revision identifiers.
5. If the original publication can be identified, retrieve or inspect its official public record and compare the relevant data with the local CSV.
6. Record whether the local CSV is a direct source download, transformed output, or manually assembled file.
7. Identify which transformations, filters, sorting, or field selections occur between source and CSV.

Do not infer a publication ID from the ticker or date.

## 2. EXCHANGE_CENTER — trace the actual workbook

Investigate `dollar-history.xlsx`.

Actions:
1. Inspect project-local scripts and configuration that the owner has made available.
2. Identify the exact official EXCHANGE_CENTER page, API, endpoint, or downloadable source profile used to obtain the workbook.
3. Determine whether the workbook is a direct download or a transformed/exported artifact.
4. Identify the exact source field corresponding to the approved sell-rate column.
5. Determine whether official source records expose publication timestamps, first-availability evidence, update timestamps, or correction/revision identifiers.
6. Compare available official records with the 19 workbook observations.
7. Record any transformations or manual steps between the official source and the workbook.

Do not assume that an official source page with similar values proves this exact workbook originated from it.

## 3. Provenance evidence model

For each artifact, report separately:

- `source_identity`
- `source_profile`
- `source_record_identity`
- `source_revision_identity`
- `source_published_at`
- `source_available_at`
- `ingested_at`
- `artifact_sha256`
- `artifact_created_at` if independently evidenced
- `transformation_method`

Use these evidence statuses:

- `OFFICIAL_SOURCE_VERIFIED`
- `LOCALLY_TRACEABLE`
- `ARTIFACT_OBSERVED`
- `INFERRED`
- `UNVERIFIED`
- `UNKNOWN`
- `BLOCKED`

A timestamp must not be inferred from a file modification time, upload time, row date, or Git timestamp.

A matching hash proves byte equality only.

## 4. Source comparison

For MarketDaily:
- Compare the official source record with the local CSV for the 21 observations.
- Report exact matching and differing fields.
- Preserve the distinction between source data and locally transformed output.

For EXCHANGE_CENTER:
- Compare all 19 sell-rate observations against official records where available.
- Record exact matching dates and values.
- Do not use the buy-rate column as canonical FXRate.
- Do not perform any unit conversion.

If historical official records cannot be retrieved, state the exact limitation and preserve the unresolved status.

## 5. Deliverables

Create:

1. `database/reports/DB_AUD_011_MARKET_FX_SOURCE_PROVENANCE_DOSSIER.md`
2. `database/reports/market_fx_source_evidence.json`
3. Append a concise result to `reply.md`, preserving all previous content.

The dossier must contain:
- Exact local artifact identity and SHA-256.
- Source URL/endpoint and source record identifiers, when verified.
- Local script/configuration references.
- Source-to-artifact transformation chain.
- Field-level comparison results.
- Publication, availability, and revision evidence.
- Explicit unresolved gaps.
- Evidence status for every important claim.
- Exact next prerequisite for ingestion readiness.

## 6. Restrictions

- Do not read shell history, browser profiles, cookies, credentials, tokens, or secrets.
- Do not expose private credentials or include them in reports.
- Do not execute owner scripts or download jobs.
- Do not modify source CSV/XLSX files.
- Do not modify application code, ORM, schemas, migrations, or database records.
- Do not change `WORKFLOW_RULES.md` or `prompt.md`.
- Do not invent missing source records or timestamps.
- Do not mark a feed production-ready merely because values match.
- Do not spend time reporting Git activity.

## 7. Completion criteria

Complete this task when:
1. Both artifacts have been traced as far as available evidence permits.
2. Official source URLs and records are independently verifiable wherever claimed.
3. Local extraction/transformation paths are documented.
4. All 21 MarketDaily and 19 FX observations have comparison outcomes, or an exact documented reason why comparison is impossible.
5. Unknown provenance fields remain explicitly UNKNOWN.
6. The dossier and JSON evidence manifest are created.
7. Remaining blockers are mapped to Task 025 and Task 009.

Investigation completion does not imply source verification or ingestion readiness. Close every gap that evidence allows; do not fabricate the rest.