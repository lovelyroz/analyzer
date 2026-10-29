# Prompt 1-A — Complete the Existing Stage 7 Audit

**TASK TYPE: AUDIT ONLY + LIMITED REPORT CORRECTIONS**

This is a supplemental correction to the existing main Prompt 1. Do not treat it as a new main prompt number.

Use Sources for this Prompt

## Task IDs

- S7-T001 — Verify the real production execution path
- S7-T002 — Verify Stage 9 persistence
- S7-T003 — Verify D9 and actual consumption of versioned parameters
- S7-T004 — Verify PIT, provenance, and input contracts
- S7-T005 — Verify alert contracts and decisions D1–D8

Read `stepsForStage7.md` first. Follow their current instructions.


## Required work

### 1. Verify S7-T001 — Production execution path

Inspect the actual source and identify confirmed callers and entrypoints.

Distinguish:
- a function or service that exists;
- a caller that invokes it;
- a complete production execution path;
- a link that remains unverified.

Do not claim that an entrypoint or caller is absent based only on a limited file list or a previous report. Identify the files and search scope supporting any absence claim.

### 2. Verify S7-T002 — Stage 9 persistence

Inspect existing SQLAlchemy models, database table definitions, repositories, and relevant schema code.

Determine whether `FinalDecisionResult` is persisted, partially persisted, or not persisted. A schema or dataclass alone does not prove database persistence. Conversely, inspecting only `src/decision/schema.py` and `src/core/database.py` does not prove project-wide absence.

Do not implement persistence.

### 3. Verify S7-T003 — D9 parameter selection and consumption

Trace parameter selection through the valuation service into the actual calculation.

Determine whether the selected parameter set is actually consumed by the calculation or merely recorded in metadata. Verify the current behavior when a dated parameter selection has no eligible version.

Do not add a guessed effective date or change the existing policy. Keep D9 unresolved wherever approved policy or valid historical parameter evidence is missing.

### 4. Verify S7-T004 — PIT and provenance

Trace the actual date and provenance information available for:
- market prices;
- Stage 5 forecast inputs;
- benchmark series;
- market signals;
- valuation and decision outputs.

Distinguish date cutoff from proof that information was available at that time. Record missing contracts or evidence without inventing replacements.

### 5. Verify S7-T005 — D1–D8

Compare the current source and tests with the approved Stage 7 V1 specifications and the decisions recorded in `stepsForStage7.md`.

Preserve deferred features. Do not introduce unapproved formulas, thresholds, or industry-specific drivers. Do not change alert contracts without checking actual consumers.

### 6. Correct the existing report

Append a clearly titled **Prompt 1-A Supplemental Audit** section to `reply.md`.

For each Task ID, provide:
- verdict: VERIFIED, PARTIALLY VERIFIED, UNVERIFIED, or BLOCKED;
- exact source paths and function/model names;
- concise evidence for each material claim;
- remaining uncertainty and the evidence needed to resolve it;
- whether the prior report contained a false, unsupported, or overly broad claim.

Correct the following known risks explicitly:
- Stage 8 already has `select_market_history_as_of` and `analyze_market_as_of_jalali`; do not propose implementing them again.
- The earlier suggestion to use `2026-01-01` as a parameter effective date was unsupported and must not be used.
- Files created in an agent's temporary workspace must not be reported as repository changes unless verified in the actual repository.
- Do not assume that a missing file with a familiar name proves the capability is absent elsewhere.

Do not overwrite or erase the historical audit trail. Clearly label corrected conclusions and superseded claims.

## Required final report

Include:
1. Findings for S7-T001 through S7-T005.
2. Exact files inspected, including any additional models, repositories, or entrypoints.
3. Files actually modified and why.
4. Task status recommendations, without claiming tests passed.
5. A minimal recommendation for continuing the existing main Prompt 1.

Do not start implementation. Stop after the supplemental audit report.