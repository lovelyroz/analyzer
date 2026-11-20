# DB-AUD-011 ? Market/FX source provenance dossier

**Assessment date:** 2026-11-20 (UTC). **Scope:** read-only local source trace plus public-web checks; no owner download script executed; no database access.

## Executive result

Neither source artifact can be linked to a specific publisher record from evidence available in this checkout. The owner-approved source semantics remain recorded locally, but that is not proof of artifact lineage. The local market CSV and FX workbook hashes were computed directly. No source or revision timestamps were fabricated. The official ICE page identifies its currency market view and remittance-market category, but an inspectable 19-date historical record/export was not available in the retrieved page content or project files. A secondary page independently displays a matching 1405-08-28 sell value; it is corroboration only, not source authentication.

## Evidence status and local files

| Artifact | SHA-256 | Bytes | Status |
|---|---|---:|---|
| `saman_price_history.csv` | `d94f27405f257b4010e1d2b7db4a554311484a6dde2b35a9c81c548f381c1413` | 2400 | ARTIFACT_OBSERVED; CODAL source identity LOCALLY_TRACEABLE from owner decision, exact publisher record BLOCKED |
| `dollar-history.xlsx` | `eb85250100438335accb06ca1fdf364304887a71e361258b93836d3a90dd6fcf` | 14349 | ARTIFACT_OBSERVED; EXCHANGE_CENTER identity LOCALLY_TRACEABLE from owner decision, profile linkage UNVERIFIED |

## 1. CODAL / MarketDaily

### Local trace

- The owner-approved CODAL source and custom owner script are mentioned in the project decisions, including `database/DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md` ?9.30 and `database/reports/DB_DES_005_INGESTION_ATOMICITY_CONTRACT.md` ?13.10. Those entries do not name the script path, endpoint, query, company identifier, publication/TracingNo, or invocation.
- No project-local producer script/configuration references `saman_price_history.csv`. `src/scripts/audit_codal_fiscal_year_metadata.py` contains CODAL search API calls (`https://search.codal.ir/api/search/v1` and `/api/search/v2/q`) for a separate annual filing metadata audit of other issuers. It is not a daily-market downloader and does not reference this CSV. The CODAL acquisition modules in `src/ingestion/codal/` handle financial-report/PDF workflows, not this artifact.
- Thus the exact CODAL endpoint/query and company identifier used by the owner cannot be determined. The official record identity is UNKNOWN; no publication ID was inferred from the ticker/date. The file does not contain publication time, source availability, correction marker, or source revision identifier.
- Transformation classification is BLOCKED: direct official download, transformed extraction, or manual assembly cannot be distinguished without the owner script/input response. Column names and values alone are not proof of acquisition method.
- CSV observed: 12 columns, 21 data rows (CSV lines 2-22), ticker `سامان`, J-Date 1402-01-08 through 1402-02-12. Approved mappings remain `Close`, `Volume`, `No`, `Value`; `Final/Open/High/Low` remain outside the approved mapping; `Value` remains an independent local source field.

### Record-level comparison

No corresponding CODAL record could be selected from official evidence because there is no source ID, page URL, source response, or owner producer manifest. Therefore 0/21 official matches and 0/21 differences are asserted; all 21 outcomes are `NOT_COMPARABLE` / BLOCKED. Each exact local value and CSV line reference is listed in the JSON manifest. No record ID was guessed.

### Market provenance fields

| Field | Value | Status |
|---|---|---|
| `source_identity` | CODAL, as owner-approved semantic source | LOCALLY_TRACEABLE |
| `source_profile` | UNKNOWN | UNKNOWN |
| `source_record_identity` | UNKNOWN | BLOCKED |
| `source_revision_identity` | UNKNOWN | UNKNOWN |
| `source_published_at` | UNKNOWN | UNKNOWN |
| `source_available_at` | UNKNOWN | UNKNOWN |
| `ingested_at` | UNKNOWN; no ingestion audit performed | UNKNOWN |
| `artifact_sha256` | `d94f27405f257b4010e1d2b7db4a554311484a6dde2b35a9c81c548f381c1413` | ARTIFACT_OBSERVED |
| `artifact_created_at` | UNKNOWN; no embedded creation metadata; filesystem time excluded | UNKNOWN |
| `transformation_method` | UNKNOWN | BLOCKED |

## 2. EXCHANGE_CENTER / FX

### Official and local source evidence

- Official public homepage: `https://ice.ir/`. Official market-view page: `https://ice.ir/market-view/currency`. The page identifies the public currency market view under the remittance category and a date label, but the accessible rendering did not expose a historical archive/export or record-level identifiers for the workbook dates.
- The local workbook contains one worksheet `Sheet`; title in A1; headers at row 3; 19 observations in rows 4-22. The local sell field is `Sheet!C3` (sell-rate header, original Persian text preserved in the JSON manifest), selected by the owner for canonical `EXCHANGE_CENTER` USD/IRR without conversion. The exact official source field ID/profile remains UNKNOWN; a visually similar official field does not prove this workbook originated there.
- No project-local FX download/export code or workbook acquisition profile was found. Direct download vs transformed/exported/manual generation cannot be determined. There are no source record IDs or explicit publication/availability/revision fields in the workbook.
- Embedded core properties were observed (`created=2026-11-19 08:07:13`, `modified=2026-11-19 08:12:50`, creator `openpyxl`, lastModifiedBy `Papa`). These are workbook self-asserted properties only (ARTIFACT_OBSERVED), not independent artifact creation evidence and not source publication/availability timestamps. Accordingly `artifact_created_at` remains UNKNOWN.

### Record-level comparison

No dated 19-row official archive/export was retrievable from the official page rendering, and no acquisition manifest exists. Accordingly all 19 official comparisons are `NOT_COMPARABLE` / BLOCKED (0 official exact matches asserted, 0 official differences asserted). Row-by-row dates, original sell values, and workbook cell references are preserved in the JSON manifest.

One public secondary cross-check: the secondary TGJU market page displays a Center-of-Exchange remittance sell value of `1,936,329` on `28 Aban` and the local row `1405-08-28` has sell `1936329`. This is an exact date/value corroboration (INFERRED) only; it does not provide source-profile linkage, an official record ID, or proof that this workbook came from ICE. All other 18 rows have no comparable public record in the sources retrieved for this audit. No unit conversion was performed and buy values were not used as canonical rates.

### FX provenance fields

| Field | Value | Status |
|---|---|---|
| `source_identity` | EXCHANGE_CENTER, as owner-approved source/type | LOCALLY_TRACEABLE |
| `source_profile` | UNKNOWN | UNVERIFIED |
| `source_record_identity` | UNKNOWN | UNKNOWN |
| `source_revision_identity` | UNKNOWN | UNKNOWN |
| `source_published_at` | UNKNOWN | UNKNOWN |
| `source_available_at` | UNKNOWN | UNKNOWN |
| `ingested_at` | UNKNOWN; no ingestion audit performed | UNKNOWN |
| `artifact_sha256` | `eb85250100438335accb06ca1fdf364304887a71e361258b93836d3a90dd6fcf` | ARTIFACT_OBSERVED |
| `artifact_created_at` | UNKNOWN; only self-asserted embedded properties observed | UNKNOWN |
| `transformation_method` | UNKNOWN | BLOCKED |

## Official/public references checked

- CODAL public homepage: `https://www.codal.ir/` (official publication page not identified for the CSV).
- CODAL search endpoint referenced by a separate local fiscal-year audit: `https://search.codal.ir/api/search/v2/q`; NOT verified as the CSV producer endpoint.
- Exchange Center official homepage: `https://ice.ir/`.
- Exchange Center official market view: `https://ice.ir/market-view/currency`.
- Secondary matching rate page: `https://www.tgju.org/%D9%85%D8%B1%DA%A9%D8%B2-%D9%85%D8%A8%D8%A7%D8%AF%D9%84%D9%87-%D8%A7%D8%B1%D8%B2-%D9%88-%D8%B7%D9%84%D8%A7%DB%8C-%D8%A7%DB%8C%D8%B1%D8%A7%D9%86` - used only for one cross-check, never treated as the artifact source.

## Unresolved gaps and exact closure prerequisites

1. **MarketDaily (Task 025 / DB-STD-005):** obtain the original owner script/configuration and exact invocation or a non-secret acquisition manifest linking the CSV SHA-256 to endpoint, query parameters, response, stable CODAL publication/record identifier, and transformations. For the 21-row comparison, obtain the actual official record(s) selected by that evidence; do not derive IDs from symbol/date.
2. **EXCHANGE_CENTER (Task 025 / DB-STD-005):** obtain the original download/export URL or non-secret manifest linking this XLSX hash to the exact official profile/endpoint and parameters, plus an official archive/record set for the 19 dates and any published timestamps/revision indicators.
3. **Task 009 / DB-DES-004:** keep semantic mappings as approved but do not treat them as source-lineage evidence. Resolve source profile, record identity, timestamps, and correction chronology before ingestion readiness; all unresolved timestamps/revisions remain UNKNOWN.

This dossier records evidence acquisition limits, not production readiness. No official source identity for the exact artifacts or ingestion authorization is claimed.
