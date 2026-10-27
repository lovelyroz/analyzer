## Stage 7 Prompt 1 — Audit Corrections Only

**TASK TYPE: AUDIT ONLY + LIMITED DOCS ONLY**



### Allowed changes

- Read-only inspection of the source, tests, and specifications listed below or strictly necessary to verify a specific finding.


### Required corrections

1. Reconcile the claim that Stage 8 market-history retrieval is missing with:
   - `src/ingestion/market/queries.py`
   - `src/market/service.py`

   Identify what is already implemented and what remains unverified. Do not recommend reimplementing existing functionality.

2. Reassess D9 parameter selection and consumption in:
   - `src/valuation/parameters.py`
   - `src/valuation/service.py`
   - `src/valuation/engine.py`

   Do not invent an effective date or financial policy. Identify the exact unresolved contract or evidence.

3. Recheck claims about the production entrypoint, Stage 3/5 callers, and Stage 9 persistence using the actual relevant source files. Distinguish confirmed absence from an unverified path. Do not invent an orchestrator or persistence model.

4. Reassess every proposed Prompt 2 change against the current source and specifications. Remove items based on incorrect findings, unsupported dates, or unapproved financial assumptions.



### Required output

Return:
- Corrected gap matrix with exact file/function evidence.
- Files actually modified and the reason for each change.
- Unresolved policy decisions and missing evidence.
- Revised Prompt 2 scope based only on confirmed findings.

Stop after the audit corrections. Do not begin implementation.