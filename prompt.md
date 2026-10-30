# Stage 7 — Record Owner-Approved Financial Policies and Reconcile Documentation

## Task Type

**DOCS-ONLY — Documentation changes are authorized.**

This task must update and reconcile Stage 7 documentation based on the explicit owner decisions below.

**No source-code changes, no test changes, no database changes, no migrations, and no test execution are authorized.**

Repository: `lovelyroz/analyzer`

## 1. Required Files

Use only the following supplied files:

1. `WORKFLOW_RULES.md`
2. `stepsForStage7.md`
3. `tasksToDo.md`
4. `07_Stage7_Valuation.md`
5. `05_Stage5_Forecast_Engine.md`
6. `STAGE7_MASTER_WORKING_PACKET.md`
7. `STAGE7_COMPLETED_CHECKLIST.md`
8. `temp_report2.md`

Do not inspect other files unless you first identify the exact missing file and explain why it is necessary. Do not assume that an implementation behavior exists merely because a policy is documented.

## 2. Authoritative Owner Decisions

The following decisions are explicit and approved by the project owner. Treat them as binding requirements, not proposals.

### A. Forward P/E — Primary Relative Valuation Measure

The primary question is whether the company's share is cheap or expensive based on its Forward P/E.

The comparison must be made **only against the same company's own historical Forward P/E**.

Do not use industry peers or industry P/E as the basis for deciding whether this company is cheap or expensive.

The output must distinguish:

- Current Forward P/E.
- Historical Forward P/E series for the same company.
- Historical comparison statistic(s), such as median, where supported by valid observations.
- The resulting relative valuation assessment.
- The dates and provenance of the observations used.

Do not invent assessment thresholds or financial formulas that have not been approved.

### B. Historical P/E

Historical P/E must be calculated from the company's own underlying financial and market data.

It must not be accepted as a precomputed numeric input without its underlying source data and provenance.

The calculation must use the latest complete and valid input set available under the applicable date/cutoff rules.

If newer input data are incomplete:

- Continue the calculation using the latest earlier complete and valid input set.
- Clearly identify the actual date of the data used.
- Report that newer data are incomplete.
- List the exact missing inputs needed to complete the newer data set.

If no complete and valid input set exists, do not fabricate a P/E value. Report why calculation is unavailable and identify missing inputs.

Historical P/E must be reported separately from Forward P/E. It is not the primary cheap/expensive comparison measure.

### C. P/E Is a Derived Calculation, Not an Independent Input

P/E must be calculated from underlying financial and market observations.

It must not be supplied as an unexplained numeric sequence or accepted as a standalone database input.

Every underlying observation used in a P/E calculation must have sufficient traceability, including as applicable:

- Company identity.
- Financial period or observation date.
- Source identity.
- Publication date/time.
- Availability date/time or other evidence required by the approved temporal contract.
- Market-price observation date and source.
- Relevant forecast version and its input references for Forward P/E.
- Analysis cutoff and Jalali date context.

The financial period date and publication/availability date are different concepts and must not be conflated.

Do not claim full Point-in-Time correctness unless the required temporal evidence exists.

**Database rule:** No precomputed P/E values or analytical outputs may be persisted as independent database records. Raw source data may be persisted under the existing source-data contracts. P/E is calculated at runtime.

### D. Industry P/E Is Removed from the Cheap/Expensive Assessment

The owner explicitly changed the previous policy.

Remove industry Forward P/E and industry TTM P/E from the cheap/expensive assessment and from the target P/E fallback hierarchy.

Do not preserve old industry benchmark fallback behavior as an approved V1 policy.

If historical documentation contains industry valuation sections, do not silently erase historical context. Mark the old policy as superseded by this owner-approved amendment and make the active policy unambiguous.

### E. Latest Complete Input Set — General Runtime Selection Policy

The engine must not automatically use the newest individual records if they do not form a complete and valid input set.

For each calculation, it must select the latest complete and valid input set that satisfies the relevant company identity, period, source, cutoff, and temporal validity requirements.

When newer data are incomplete:

1. Use the latest earlier complete and valid input set.
2. Perform the calculation using that complete set.
3. Identify the actual date/version of the selected inputs.
4. Warn that newer inputs are incomplete.
5. List the exact missing inputs required to complete the newer set.

If no complete valid set exists, fail closed and explain the missing requirements.

Do not mix observations from different companies, incompatible periods, or incompatible forecast versions merely to create an apparently complete set.

Do not invent a universal completeness definition. The required fields must be defined for each calculation based on its actual input contract.

### F. Market Price — Latest Available Observation and Explicit Alert

The owner has also approved this policy:

- Use the latest available market-price observation on or before the Jalali analysis date.
- Do not silently present an older market price as if it belonged to the analysis date.
- Report the actual Jalali date of the selected market-price observation.
- If the selected price date differs from the analysis date, emit a clear alert identifying both dates.
- If no eligible price exists, preserve the current fail-closed behavior unless a separate owner decision authorizes a change.

This policy is transparent latest-available-data behavior; it must not be described as proof of complete PIT correctness.

### G. Analytical Output Persistence Is Prohibited

The owner has explicitly decided:

**All analytical outputs are temporary runtime results. No analytical output or decision history may be persisted in the database.**

This includes, without limitation:

- Forecast outputs.
- Valuation outputs.
- Calculated P/E values.
- Fair values and valuation assessments.
- Decision outputs.
- Decision history.

Stage 9 may receive `previous_decision` from its caller when available for runtime decision logic such as hysteresis. Stage 9 must not create or persist its own decision history.

Do not add database models, tables, repositories, or persistence mechanisms for analytical outputs.

Important: Existing persistence models, including any Forecast persistence models documented in the supplied files, must not be silently declared compliant with this policy. Record the apparent conflict as an explicit unresolved implementation/documentation issue requiring a separate controlled audit and owner-authorized remediation. Do not delete or modify those models in this documentation-only task.

## 3. Required Documentation Work

### Task 1 — Amend the locked V1 valuation specification

Update `07_Stage7_Valuation.md`.

Preserve its useful existing structure and financial definitions, but add a clearly identifiable owner-approved amendment to the V1 specification.

At minimum:

- Make same-company historical Forward P/E the sole basis for the cheap/expensive relative assessment.
- Remove industry P/E from the active benchmark and fallback hierarchy.
- Define Historical P/E as a derived calculation from underlying data.
- Document the latest-complete-input selection and incomplete-newer-data alert behavior.
- Document the required source and temporal provenance.
- Explicitly distinguish financial period date from publication/availability date.
- State that calculated P/E and all other analytical outputs are runtime-only and must not be persisted.
- Preserve the distinction between Forward P/E and Historical P/E.
- Do not invent thresholds, formulas, or new financial assumptions.

Do not leave contradictory old sections appearing to be active policy. Clearly mark superseded sections and point to the owner-approved amendment.

### Task 2 — Update the Stage 7 roadmap

Update `stepsForStage7.md`.

The roadmap must:

- Include all owner-approved policies above.
- Replace obsolete industry benchmark work with same-company historical Forward P/E work.
- Include the market-price date alert.
- Include complete-input fallback and missing-input reporting.
- Record the prohibition on analytical-output persistence.
- Record the existing Forecast persistence-model conflict as unresolved, without changing its implementation.
- Preserve the rule that `src/valuation/engine.py` is the final technical Stage 7 task.
- Preserve the Stage 7 OPEN status until all required implementation and user-run test evidence exists.

### Task 3 — Reconcile the active Task Register

Update `tasksToDo.md`.

- Review S7-T007 through S7-T012.
- Do not retain obsolete tasks that require industry P/E as an active valuation benchmark.
- Preserve completed audit history and do not reuse retired Task IDs.
- Add new Task IDs only where necessary.
- Explicitly separate documentation decisions from implementation work.
- Define implementation tasks for:
  - Same-company historical Forward P/E calculation.
  - Historical P/E calculation from raw inputs.
  - Provenance and temporal validity of all underlying observations.
  - Latest complete input selection and incomplete-data alerts.
  - Market-price observation date alert.
  - Removal/rejection of unsupported precomputed P/E inputs.
  - Audit of existing Forecast persistence models against the owner's no-analytical-persistence rule.
- Keep tasks OPEN or BLOCKED until actual code evidence and user-run tests support completion.
- Ensure dependencies are accurate.

Do not claim any of these implementation tasks are completed merely because the documentation is updated.

### Task 4 — Reconcile the master working packet and completed checklist

Update:

- `STAGE7_MASTER_WORKING_PACKET.md`
- `STAGE7_COMPLETED_CHECKLIST.md`

The master packet must reflect the new task order and current unresolved work.

The completed checklist must not mark newly approved policies as implemented. It may record that the owner decisions are now documented, but implementation and verification items must remain unchecked until evidenced.

### Task 5 — Preserve durable decision history

Append a clearly titled section to `temp_report2.md`:

`Stage 7 — Owner-Approved P/E, Complete-Input and Persistence Policies`

Record:

- The owner's approved decisions.
- Which old policies were superseded.
- Which implementation tasks remain.
- The existing Forecast persistence conflict.
- The fact that this prompt changed documentation only and did not modify source code or execute tests.

Do not rewrite or delete historical reports.

If `reply.md` is included in the supplied files, it may be used as a temporary execution report, but `temp_report2.md` must contain the durable decision record.

## 4. Cross-Document Consistency Requirements

After editing, reconcile the terminology and status across all updated documents.

In particular:

- Industry P/E must not remain an active cheap/expensive benchmark.
- P/E must not be described as an unexplained numeric input.
- Historical Forward P/E and Historical TTM P/E must not be confused.
- No analytical output persistence must be stated consistently.
- Existing Forecast persistence models must be identified as an unresolved conflict, not silently ignored.
- Latest-complete-input fallback must not be described as using arbitrary individual latest records.
- A selected older data set must always be accompanied by its actual date/version and missing-input alert.
- No full PIT guarantee may be claimed without publication/availability evidence.
- Stage 7 must remain OPEN.

## 5. Strict Restrictions

- Do not change any source-code file.
- Do not change any test file.
- Do not change database models, schemas, repositories, or migrations.
- Do not execute tests, applications, database commands, or Git commands.
- Do not invent data, sources, dates, thresholds, formulas, or financial assumptions.
- Do not mark implementation work DONE.
- Do not repeat completed audits without a specific evidence-based reason.
- Do not remove historical reports.
- Do not claim that documentation changes resolve implementation defects.

## 6. Required Final Report

Return a concise but complete report containing:

1. Exact files changed.
2. Summary of each document change.
3. Owner decisions recorded.
4. Superseded policies explicitly identified.
5. New or revised Task IDs and their statuses.
6. Unresolved implementation issues, especially the Forecast persistence conflict.
7. Confirmation that no source code or tests were changed.
8. Confirmation that no tests were executed.
9. Confirmation that Stage 7 remains OPEN.
10. Exact recommended next implementation task and its required source/test files.

Do not claim successful tests or implementation verification.

The task is complete only when all supplied documentation files are internally consistent and the final report accurately reflects the changes.