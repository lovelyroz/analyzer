# DB-AUD-018 — CODAL Fiscal-Year Metadata Capability Audit

**Status:** SOURCE CAPABILITY DISCOVERED — direct live validation and source-governance approval still required  
**Date:** 2026-11-18  
**Mode:** Research/documentation only. No project code, ORM, migration, database, or tests changed.  
**Depends on:** DB-AUD-017, DB-DES-012, owner rule that every fiscal year is twelve months.

## 1. Executive result

A concrete CODAL fiscal-year metadata endpoint has been identified through an open-source, unofficial, read-only integration:

- Request path used by the integration: `/api/search/v1/financialYears`
- Request parameter: `Symbol` (exact Persian ticker)
- Response shape: a list of Jalali fiscal-year end dates, newest first.
- The integration also uses CODAL's `/api/search/v1/companies` endpoint for issuer lookup and the disclosure search API for annual/interim filings.

This is materially better than relying only on report titles: CODAL appears to expose a company-specific list of fiscal-year closing dates. However, the evidence inspected is the implementation and fixtures of a third-party client, not official CODAL API documentation or a live request made by this project. Treat it as a **high-value candidate source**, not yet as a fully validated production contract.

## 2. Evidence inspected

Repository: `https://github.com/sepehr071/codal-mcp` (unofficial, read-only CODAL client).

Files inspected:
- `src/codal_mcp/codal.py`
- `tests/test_codal.py`
- `tests/fixtures/financial_years_foolad.json`

The implementation calls:

```text
GET /api/search/v1/financialYears?Symbol=<Persian ticker>
```

It returns the values as `year_ends`, preserving Jalali date strings.

The test fixture for ticker فولاد contains a descending list of fiscal-year ends, including:
- 1405/12/29
- 1404/12/29
- 1403/12/30
- 1402/12/29
- 1401/12/29
- continuing historically to 1379/12/30

The client test asserts that the endpoint returns the newest dates first and that the exact symbol is sent. A separate statement-page parser extracts `period_months`, `period_end`, and `year_end` from a CODAL filing page. These are useful cross-check fields, but they are not substitutes for the company-level year-end list.

Public implementation references:
- `https://github.com/sepehr071/codal-mcp/blob/main/src/codal_mcp/codal.py`
- `https://github.com/sepehr071/codal-mcp/blob/main/tests/test_codal.py`
- `https://github.com/sepehr071/codal-mcp/blob/main/tests/fixtures/financial_years_foolad.json`

## 3. What the endpoint establishes — and what it does not

Potentially establishes:
- a CODAL-associated list of fiscal-year end dates for an exact issuer ticker;
- historical year-end values, not just one current scalar;
- a practical source for discovering changes in the reported closing date;
- an independent cross-check against annual statements whose report period is twelve months.

It does **not** establish from the inspected code alone:
- exact fiscal-year start dates;
- that every date in the endpoint is complete and historically exhaustive;
- the official effective date or source document for a change in closing date;
- why a date changed, whether it was corrected, or whether it reflects a data-entry correction;
- whether the endpoint's issuer identity/ticker history is stable;
- whether the endpoint response is guaranteed by CODAL as a supported public API.

Therefore, do not directly treat the endpoint response as an approved CompanyFiscalYear row without validation.

## 4. Application of the owner's twelve-month invariant

The owner has established that every fiscal year is exactly twelve Jalali calendar months.

Under that invariant, the year-end list becomes especially useful:

- If two consecutive year-end dates are verified, the start of the later fiscal year is the Jalali day immediately after the previous verified year-end.
- The interval must then be validated as exactly twelve consecutive Jalali calendar months and must end on the next listed year-end.
- If only one year-end is available, its start can be calculated by subtracting twelve Jalali calendar months and adding one day, but this derivation must be marked as derived and checked against an official filing or company document before approval.
- Do not use Gregorian 365/366-day subtraction. Use Jalali calendar arithmetic.
- If consecutive dates do not define a valid twelve-month sequence, do not create a short/long transition year. Mark the company calendar unresolved and stop automated classification.

A company may have a non-Farvardin fiscal year. The endpoint's history can reveal the end-month pattern; it must not be assumed to be 12/29 or 12/30.

## 5. Recommended evidence and validation flow

For a company entering V1:

1. Resolve the exact CODAL issuer and ticker through the company lookup; independently match the legal company identity to the app's Company record. Ticker text alone is not enough where names or symbols are ambiguous.
2. Retrieve the CODAL fiscal-year-end list for that exact ticker.
3. Retrieve the annual financial statements (12-month period) corresponding to the latest year-end and at least one preceding year-end.
4. Cross-check the annual filing title/period end and, where available, the filing's `year_end` / `period_end` metadata against the company-level endpoint.
5. Calculate candidate starts using Jalali calendar arithmetic and the strict twelve-month rule.
6. Require no unexplained gap, overlap, duplicate, invalid date, or disagreement between endpoint and annual filing.
7. Retain the endpoint observation and the exact annual filing/source reference as provenance. Record retrieval/verification time; do not archive raw workbooks merely to preserve this metadata.
8. Approve the resulting company fiscal-year intervals only after the cross-check succeeds. If the endpoint and annual statements disagree, fail closed and require source reconciliation.

A future change in the endpoint's year-end list is a **change signal**, not self-sufficient proof of a valid transition. Since every fiscal year must remain twelve months, any sequence that cannot be reconciled as contiguous twelve-month intervals is unresolved.

## 6. Remaining verification work

Before production reliance:
- Perform a small live read-only check against CODAL for two known companies: one with Farvardin-to-Esfand year-end and one known to have a non-Farvardin year-end.
- Compare the endpoint dates with official 12-month annual statements for at least two consecutive fiscal years per company.
- Confirm whether the endpoint's year-end list includes all available years and how it behaves for a company with a reported fiscal-year change or corrected disclosure.
- Verify the endpoint's issuer resolution against company legal name/identifier, not just ticker.
- Confirm request availability/rate limits and whether the endpoint can be consumed reliably from the project's deployment environment. Third-party client documentation reports that CODAL may block or time out from non-Iranian network exits; this is an operational risk, not a contract guarantee.
- Do not add a third-party MCP dependency to the analyzer application. The integration was used only to discover and inspect the underlying CODAL request pattern.

## 7. Outcome

**Decision:** Adopt the CODAL fiscal-year-end list as the leading candidate source for company-specific fiscal-year discovery and historical cross-checking, subject to direct live validation and official-filing reconciliation.

**Not yet authorized:** automatic approval from the endpoint alone, ORM/schema changes, Migration 10, or runtime integration.

No project code, ORM, schema, migration, database rows, workbook, or tests were changed.
