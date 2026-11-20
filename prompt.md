# TASK: MARKET/FX DOCUMENTATION CONSISTENCY AUDIT & CLOSURE

## Mission

Perform a complete, evidence-based consistency and traceability audit of the Market/FX ingestion documentation in the `lovelyroz/analyzer` repository.

The objective is to close documentation inconsistencies, verify that all approved decisions are represented consistently, and ensure that unresolved evidence gaps are explicitly recorded without being silently converted into assumptions.

This is a bounded documentation task. Do not expand its scope into implementation, database changes, or new business decisions.

You are expected to complete the task autonomously, verify your changes, commit the approved documentation changes, and provide a concise, auditable completion report.

## 1. Repository and branch

- Repository: `analyzer`
- Target branch: `master`
- Before editing, inspect the current branch, working tree, latest commit, and current versions of all target files.
- Fetch the latest version of each target file before modifying it.
- Do not overwrite newer remote changes.
- Preserve existing document structure, identifiers, historical decisions, and established terminology.
- Do not modify `WORKFLOW_RULES.md`.

## 2. Authoritative documents in scope

Inspect the latest versions of:

1. `database/reports/DB_DES_005_INGESTION_ATOMICITY_CONTRACT.md`
   - Focus: §13.7, §13.8, §13.9 and related acceptance criteria.

2. `database/DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md`
   - Focus: §9.28 and §9.29, plus any directly related Market/FX sections.

3. `database/reports/DB_STD_005_AND_DB_AUD_001_MARKET_FX_EVIDENCE_REVIEW.md`
   - Focus: §18 and all relevant preceding evidence and decision registers.

Search for additional directly relevant documents only when necessary to verify a cross-reference or identify a contradiction. Do not expand the audit into unrelated database domains.

## 3. Approved facts that must be preserved

Treat the following as established owner decisions. Do not reinterpret or reverse them.

### MarketDaily / CODAL

- The source is CODAL.
- The owner downloads the data using their own script.
- `J-Date` is a Jalali date in `YYYY-MM-DD` form.
- `Close` represents the daily closing market price in Rial per share.
- `Volume` represents the number of shares traded.
- `No` represents the transaction count.
- `Value` represents the source-provided total traded value in Rial.
- Preserve `Value` independently. Do not replace it with `Volume × Close`.
- `Final`, `Open`, `High`, and `Low` are excluded from the approved ingestion mapping.
- The reviewed sample contains 21 records from 1402-01-08 through 1402-02-12.
- Reviewed CSV SHA-256:
  `d94f27405f257b4010e1d2b7db4a554311484a6dde2b35a9c81c548f381c1413`
- Publication time, first availability time, and revision/correction identity have not yet been evidenced.

### FX / EXCHANGE_CENTER

- The owner has identified the reviewed FX source as `EXCHANGE_CENTER`.
- Use the sell-rate column only.
- The canonical rate is Rial per USD.
- Do not create an inferred buy/sell split in the canonical FX mapping.
- Reviewed workbook SHA-256:
  `eb85250100438335accb06ca1fdf364304887a71e361258b93836d3a90dd6fcf`
- The hash identifies the exact reviewed file bytes. It does not independently prove publisher identity, source-profile identity, publication time, or revision identity.
- The exact traceable link between this artifact and the `EXCHANGE_CENTER` source profile remains to be evidenced.

### FX / FREE_MARKET

- The approved unit conversion is Toman per USD multiplied by 10 to obtain canonical Rial per USD.
- A real sample artifact and its complete source/header/calendar/provenance audit are still outstanding.
- Do not copy the `EXCHANGE_CENTER` column mapping into `FREE_MARKET`.
- Do not activate this profile based only on the unit conversion decision.

### Provenance and revision controls

Keep these timestamps distinct:

- `source_published_at`: official source publication time.
- `source_available_at`: first provable availability time.
- `ingested_at`: system receipt/ingestion time.

Do not infer publication or availability times from:

- Upload time.
- Filesystem modification time.
- The date contained in a market or FX row.
- The order in which files were received.

A SHA-256 hash proves byte equality, not publisher identity or revision identity.

A changed payload for an existing economic key without valid revision evidence must remain a conflict/review case. Do not introduce overwrite or last-arrival-wins behavior.

Economic keys currently documented:

- MarketDaily: Company + Jalali date.
- FX: Jalali date + currency pair + rate type.

Do not invent a revision identifier, fingerprint algorithm, conflict winner, or final version-ranking policy.

## 4. Required work

### Task A — Build a source-of-truth comparison matrix

Compare the three authoritative documents.

For every material Market/FX decision, record:

- Decision or fact.
- Current value.
- Evidence type: owner-approved, artifact-observed, or unresolved.
- Documents and sections where it appears.
- Whether all documents agree.
- Any contradiction, omission, stale wording, or ambiguous statement.
- Required documentation correction, if any.

At minimum, audit:

1. CODAL source identity.
2. Market CSV hash and sample scope.
3. Market field mappings and units.
4. Jalali date handling.
5. EXCHANGE_CENTER source identity.
6. FX workbook hash and sell-column mapping.
7. FREE_MARKET conversion and missing evidence.
8. The three provenance timestamps.
9. Artifact hash limitations.
10. Economic keys.
11. Duplicate and conflicting payload behavior.
12. Revision/correction evidence requirements.
13. Feed activation restrictions.
14. DB-DES-005 acceptance criteria and unresolved decisions.
15. Cross-references between the report and master packet.

Do not treat repeated statements in multiple documents as independent evidence. Identify the original evidence or owner decision where possible.

### Task B — Verify evidence traceability

Inspect the repository for the actual reviewed artifacts, evidence records, and references.

For each artifact:

- Determine whether the exact file is present.
- If present, independently calculate its SHA-256.
- Compare it with the documented hash.
- Record the path and verification result.
- Do not modify or resave source artifacts.
- Do not claim an artifact was verified if it was not accessible.

For CODAL, distinguish the owner's source decision from proof of publication/availability/revision metadata.

For EXCHANGE_CENTER, distinguish the owner's source decision from proof that the exact workbook bytes came from that source.

For FREE_MARKET, explicitly state whether a real sample and source evidence exist in the repository.

If evidence is missing, record the exact missing item. Do not search for a substitute artifact and silently treat it as the reviewed source.

### Task C — Correct documentation inconsistencies

If the comparison reveals contradictions, stale statements, missing cross-references, or inconsistent status labels:

- Correct them in the appropriate existing documents.
- Preserve approved facts exactly.
- Keep unresolved facts explicitly unresolved.
- Make the smallest sufficient edits.
- Do not duplicate entire sections unnecessarily.
- Ensure the master packet accurately summarizes the detailed evidence report and ingestion contract.
- Ensure the ingestion contract does not present provisional controls as final approved implementation policy.

Do not create new business decisions merely to make the documents appear complete.

### Task D — Produce a final audit register

Add or update an appropriately located section in the existing Market/FX evidence review report.

The register must contain:

| ID | Subject | Evidence/status | Verified result | Remaining gap | Closure condition |
|---|---|---|---|---|---|

Include separate entries for:

- CODAL source and mapping.
- CODAL publication/availability evidence.
- CODAL revision/correction behavior.
- EXCHANGE_CENTER source and artifact linkage.
- EXCHANGE_CENTER publication/availability evidence.
- EXCHANGE_CENTER revision/correction behavior.
- FREE_MARKET artifact and source audit.
- Provenance timestamp policy.
- Economic-key and conflict policy.
- Feed activation status.

Use precise status terminology. At minimum distinguish:

- VERIFIED
- OWNER-APPROVED
- ARTIFACT-OBSERVED
- UNVERIFIED
- BLOCKED
- PARTIAL

Do not label an item VERIFIED merely because an owner decision exists.

### Task E — Cross-document validation

After editing:

1. Re-read all modified sections.
2. Check every hash character by character.
3. Check that dates, units, field names, and economic keys agree.
4. Check that the detailed report and master packet do not contradict each other.
5. Check that no provisional control is described as a final implementation decision.
6. Check that all unresolved evidence gaps remain visible.
7. Check Markdown tables, headings, section numbering, and internal references.
8. Check the final Git diff for unrelated changes.

If an inconsistency cannot be resolved from repository evidence, preserve it as an explicit blocker rather than guessing.

## 5. Strict change restrictions

You are authorized to edit documentation files in scope only.

You are NOT authorized to:

- Modify Python source code.
- Modify tests.
- Modify ORM models.
- Modify schemas or migrations.
- Open, create, modify, or query any database.
- Modify ingestion behavior.
- Activate or deactivate a feed in runtime configuration.
- Change source mappings or units.
- Invent a revision policy or conflict winner.
- Modify `WORKFLOW_RULES.md`.
- Delete or rewrite historical evidence.
- Change any source artifact.

Do not run application code or database scripts.

Do not claim tests were run. This is a documentation audit, not an implementation test.

## 6. Completion criteria

The task is complete only when all of the following are true:

1. All three authoritative documents have been inspected at their latest available versions.
2. A source-of-truth comparison has been completed.
3. Artifact availability and hash verification have been reported honestly.
4. Every identified documentation contradiction has either been corrected or explicitly recorded as unresolved with a reason.
5. The final audit register exists and covers every required subject.
6. The master packet accurately reflects the detailed report.
7. Cross-document validation has been completed.
8. The Git diff contains only authorized documentation changes.
9. All authorized changes have been committed to `master`.
10. The final report includes commit SHA, modified paths, and verification results.

Important: Missing external evidence does not prevent closure of this bounded documentation-consistency task. It does, however, prevent the relevant source-provenance item or feed from being marked VERIFIED or production-ready. Record those items as BLOCKED/UNVERIFIED with exact closure conditions.

Do not claim that the underlying Market/FX ingestion design is fully approved merely because this documentation task is complete.

## 7. Required final response

Return a concise but complete report with these headings:

### A. Completion
- COMPLETE or NOT COMPLETE.
- Exact reason.

### B. Changes
- Each modified path.
- Sections changed.
- Short description of each correction.

### C. Evidence verification
- Each artifact path, expected hash, actual hash, and result.
- Explicitly identify artifacts that were unavailable.

### D. Remaining blockers
- Exact missing evidence.
- What would close each blocker.
- Whether any feed remains blocked from activation.

### E. Validation
- Cross-document checks performed.
- Git diff scope check.
- Confirm no code, tests, ORM, schema, migration, or database changes.
- Confirm no tests were run.

### F. Git
- Branch.
- Commit SHA.
- Working-tree status after commit.

### G. Next action
Identify the single highest-value next task. Do not begin that next task without authorization.

Be factual. Do not report success based on intention. A task is complete only when the requested outputs and verification evidence actually exist.