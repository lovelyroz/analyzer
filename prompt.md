# Package 2 — Implement Core OA1 Remediation
## Repository: lovelyroz/analyzer

### Agent Instructions

You are implementing Package 2 of Stage 7 in a financial-data application.

Financial correctness, auditability, deterministic behavior, point-in-time integrity, and preservation of financial invariants take priority over implementation completeness.

## 1. Work classification and boundaries

**Work type: CODE-CHANGING + TEST AUTHORING**

You are authorized to:
- Modify production code strictly within the scope of Tasks 022–027.
- Add or modify relevant automated tests.
- Update `STAGE7_MASTER_WORKING_PACKET.md` with factual implementation evidence and accurate task statuses.
- Update `07_Stage7_Valuation.md` only where a factual implementation annotation is necessary and supported by code.

You are NOT authorized to:
- Run tests, benchmarks, scripts, migrations, or application commands.
- Modify unrelated stages or perform repository-wide cleanup.
- Redesign the valuation engine.
- Invent financial formulas, thresholds, sector mappings, input contracts, historical data, or provenance.
- Create synthetic historical Forecast vintages or market observations.
- Persist any analytical output in the application database.
- Modify Forecast persistence models or migrations. Those belong to the separate Tasks 053–057.
- Change the locked Stage 7 architecture or introduce a new production orchestrator.
- Commit, push, pull, create branches, or make remote Git changes.

**Important:** The user runs all tests locally. Do not execute tests, even if you believe a test run would be useful. Provide exact commands for the user.

## 2. Authoritative references

Use these files as the controlling references:

1. `STAGE7_MASTER_WORKING_PACKET.md` — sole authority for task status, dependencies, acceptance criteria, and execution order.
2. `WORKFLOW_RULES.md` — required workflow and reporting rules.
3. `07_Stage7_Valuation.md` — binding Stage 7 specification and AMENDMENT-OA1.

Owner-approved OA1 policies are binding. Historical sections superseded by OA1 must not be treated as active requirements.

Do not use `temp_report2.md`, `reply.md`, historical reports, or agent recollection to infer current task status.

## 3. Explicit file scope

You may inspect and modify only the following files unless you first report an additional required file and explain why it is necessary.

### Reference documents
- `STAGE7_MASTER_WORKING_PACKET.md`
- `WORKFLOW_RULES.md`
- `07_Stage7_Valuation.md`

### Valuation and Forecast
- `src/valuation/engine.py`
- `src/valuation/models.py`
- `src/valuation/parameters.py`
- `src/valuation/schema.py`
- `src/valuation/service.py`
- `src/forecast/schema.py`

### Market and financial source data
- `src/ingestion/market/queries.py`
- `src/models/market.py`
- `src/models/normalized.py`
- `src/models/normalized_provenance.py`
- `src/models/report.py`
- `src/models/period.py`
- `src/models/entity.py`
- `src/core/jalali.py`
- `src/core/database.py`

### Tests
- `src/tests/test_stage7_valuation.py`
- `src/tests/test_market_history_query.py`
- `src/tests/test_stage789_service_interface.py`

If an additional file is essential, stop before relying on it. Report its exact path and explain the dependency. Do not broaden the inspection scope yourself.

## 4. Tasks

### Task 1 — 022 · S7-T013: Same-company historical Forward P/E

Implement the same-company historical Forward P/E as the sole active relative cheap/expensive comparison basis.

Requirements:
- Current Forward P/E and same-company historical Forward P/E observations must be distinct concepts in the calculation and output.
- Historical observations must be associated with the correct company and compatible financial period/forecast context.
- Use only historical observations genuinely supplied through an existing, verifiable input contract.
- Industry Forward P/E and Industry TTM P/E must not influence relative cheap/expensive assessment.
- Preserve actual dates and all provenance fields genuinely supplied by the caller.
- Do not invent a history, median, assessment threshold, or formula.
- If a valid historical Forward P/E series is unavailable, return an explicit unavailable/insufficient result or fail closed. Do not substitute industry values or fabricate history.
- Do not claim full PIT correctness unless the required publication/availability evidence is actually present and validated.

Acceptance evidence:
- Tests demonstrate that relative assessment uses only same-company historical Forward P/E.
- Tests demonstrate that industry values cannot influence the relative assessment.
- Missing or insufficient historical evidence does not produce a fabricated assessment.

### Task 2 — 023 · S7-T014: Derive Historical P/E from underlying data

Historical P/E must be derived at runtime from underlying company financial and market observations.

Requirements:
- Do not accept a precomputed numeric P/E series as a valid substitute for source observations and provenance.
- Keep financial period dates distinct from report publication and availability dates.
- Use the existing raw/normalized financial data contracts where they genuinely support the calculation.
- Preserve company identity, period identity, report version, source references, and market observation dates wherever available.
- Negative or zero EPS must not produce an artificial P/E.
- Do not combine incompatible financial periods, companies, report versions, or market observations.
- Do not persist calculated P/E values in the database.

Before implementing a new query or calculation path, establish that the existing source models and their relationships contain all required inputs.

If a required source field, valid mapping, publication/availability evidence, or data query does not exist, do not invent it. Implement only the independently supportable behavior and report the remaining dependency precisely.

Acceptance evidence:
- Negative tests reject unsupported precomputed P/E input.
- Tests verify derived values from actual underlying input records.
- Tests verify missing or invalid source data fails closed.
- Tests verify the actual selected observation dates are retained.

### Task 3 — 024 · S7-T015: Latest complete and valid input set

Implement the latest-complete-input-set rule only to the extent supported by the existing input contracts.

Requirements:
- Completeness must be defined from the actual calculation's existing input contract. Do not invent a universal completeness checklist.
- Select the latest complete and valid set for the same company and compatible period/source/version context.
- Never combine records from incompatible companies, periods, or Forecast versions.
- If a newer set is incomplete, use the latest earlier complete and valid set only when that earlier set is demonstrably valid under the applicable contract.
- Report the actual selected date/version.
- Emit an explicit warning and exact missing-input list for the newer incomplete set.
- If no complete valid set exists, fail closed and explain why.
- Do not infer publication or availability timestamps from observation dates.

Acceptance evidence:
- Tests cover latest complete set selection.
- Tests cover fallback to an earlier complete set.
- Tests verify the actual selected date/version.
- Tests verify warning content and exact missing-input identification.
- Tests verify fail-closed behavior when no complete set exists.

If the existing codebase does not define the required input contract or does not provide enough source evidence, do not create an arbitrary contract. Report the exact missing dependency and keep the affected part PARTIAL/BLOCKED.

### Task 4 — 025 · S7-T016: Market-price observation date alert

Implement OA1.6 using the existing Jalali-native market-price selection path.

Requirements:
- Select the latest eligible market-price observation on or before the requested Jalali analysis date.
- Preserve the actual selected Jalali observation date.
- If the selected date differs from the analysis date, emit an explicit alert that identifies both dates.
- If no eligible positive price exists, preserve fail-closed behavior.
- Do not convert Jalali components into invented Gregorian timestamps.
- Do not claim that observation-date selection proves publication/availability PIT correctness.
- Preserve the existing market-price basis convention unless a verified defect requires a narrow correction.

Acceptance evidence:
- Tests cover same-day price selection.
- Tests cover an earlier eligible price and verify both dates in the alert/output.
- Tests cover a price after the analysis date being excluded.
- Tests cover no eligible price and verify fail-closed behavior.
- Tests cover invalid or ambiguous market observations where relevant.

### Task 5 — 026 · S7-T017: Remove Industry P/E from the active valuation path

Implement OA1.4.

Requirements:
- Industry Forward P/E and Industry TTM P/E must not participate in:
  - Target P/E base selection;
  - Target P/E fallback selection;
  - cheap/expensive relative assessment.
- Remove or deactivate the old industry benchmark hierarchy.
- Do not replace it with another invented benchmark or formula.
- Existing Industry fields may remain temporarily for backward compatibility only if they are explicitly legacy/informational and cannot affect active valuation decisions.
- Do not change unrelated valuation formulas or thresholds.
- Update or replace tests that previously asserted active industry benchmark behavior.

Acceptance evidence:
- Tests prove changes to industry Forward/TTM inputs cannot change active Target P/E or relative assessment.
- Tests prove the active relative comparison uses same-company historical Forward P/E only.
- No active industry fallback remains reachable.

### Task 6 — 027 · S7-T018: Reject precomputed P/E without provenance

Implement the input boundary protections required by OA1.3.

Requirements:
- Any path accepting a numeric P/E sequence without underlying source observations and provenance must reject it or fail closed.
- P/E values must be derived at runtime from eligible raw observations.
- Do not silently accept legacy float arrays as valid historical P/E evidence.
- Preserve compatibility only where it does not weaken the OA1 contract.
- Do not invent provenance fields or backfill missing evidence.

Acceptance evidence:
- Negative tests prove unsupported precomputed P/E sequences are rejected.
- Tests prove that valid derived values are traceable to underlying observations.
- Tests prove missing/contradictory provenance fails closed.

## 5. Critical financial and architectural constraints

1. The application database stores source inputs and raw source data only. No Forecast, valuation, P/E, fair value, scenario, decision, or analytical history may be persisted.
2. Do not create new database tables or models for analytical outputs.
3. Do not create historical Forecast vintages or P/E observations from current data.
4. Do not infer publication/availability timestamps from financial-period dates, observation dates, ingestion timestamps, or current timestamps.
5. Do not claim full PIT correctness without actual temporal evidence.
6. Preserve Jalali-native date semantics. Gregorian dates must not be substituted for missing Jalali source dates.
7. Do not introduce new thresholds, formulas, benchmark hierarchies, or sector-specific behavior.
8. Preserve existing negative/zero EPS behavior and all financial invariants.
9. Keep changes narrowly scoped. `src/valuation/engine.py` must not be broadly redesigned in this package; make only targeted changes required by Tasks 022–027. The final engine review belongs to Task 033.
10. Do not modify Forecast persistence code or schema in this package. Tasks 053–057 are separate.

## 6. Test authoring requirements

Write or update tests for all implemented behavior, including:
- Same-company historical Forward P/E isolation;
- Derived P/E from underlying observations;
- Rejection of unsupported precomputed P/E;
- Latest complete input set and fallback;
- Exact missing-input warnings;
- Actual Jalali market-price date and alert;
- Fail-closed behavior when no eligible price or complete input set exists;
- No active Industry P/E dependency;
- Existing negative/zero EPS and scenario invariants.

Do not weaken existing tests merely to make the suite pass. Replace obsolete industry-path expectations with tests for the new owner-approved behavior.

**Do not run any tests.** Do not run any commands that execute application code or migrations.

At the end, provide exact focused and full-suite test commands for the user to execute locally.

## 7. Master Packet update

Update `STAGE7_MASTER_WORKING_PACKET.md` only with factual, evidence-backed information.

For each of Tasks 022–027:
- Preserve the exact task number and stable ID.
- Record what was implemented and which files changed.
- Record which acceptance criteria have test coverage.
- Distinguish implemented code from user-verified test results.
- Keep the task OPEN/PARTIAL until the user supplies successful test execution evidence.
- Mark a task BLOCKED where required source data or provenance is unavailable.
- Do not mark a task DONE merely because code or tests were written.

Do not change unrelated task statuses, package ordering, exit criteria, or owner decisions.

Do not create a separate report file. Do not use `reply.md` or `temp_report2.md` as an active report destination.

## 8. Required final report

Return a separate report for each task, using the exact task identifiers:

- 022 · S7-T013
- 023 · S7-T014
- 024 · S7-T015
- 025 · S7-T016
- 026 · S7-T017
- 027 · S7-T018

For each task include:
1. Status: DONE / PARTIAL / NOT DONE / BLOCKED.
2. Exact implementation performed.
3. Files inspected.
4. Files changed and reason.
5. Acceptance criteria covered by authored tests.
6. Tests not run (state explicitly that the agent did not run them).
7. Remaining missing data, provenance, or architectural dependencies.
8. Exact user-run test command(s).

Also include:
- A concise list of all changed files.
- Any required additional files that were not provided, with exact paths and reasons.
- Any scope deviations.
- Confirmation that no database analytical-output persistence was introduced.
- Confirmation that no synthetic data or provenance was created.
- Confirmation that no tests or application commands were executed.

Do not claim that Package 2 is complete unless every relevant acceptance criterion is supported by implementation evidence and subsequently verified by the user's test results.

---

### User Instructions (Persian)

**نوع کار:** کدنویسی و نوشتن/اصلاح تست‌ها؛ Agent نباید تست اجرا کند.

**فایل‌های لازم:**
- `STAGE7_MASTER_WORKING_PACKET.md`
- `WORKFLOW_RULES.md`
- `07_Stage7_Valuation.md`
- فایل‌های `src/valuation/`
- `src/forecast/schema.py`
- `src/ingestion/market/queries.py`
- مدل‌های `market.py`، `normalized.py`، `normalized_provenance.py`، `report.py`، `period.py`، `entity.py`
- `src/core/jalali.py`
- `src/core/database.py`
- تست‌های `test_stage7_valuation.py`، `test_market_history_query.py` و `test_stage789_service_interface.py`

**Taskها:**
1. 022 · S7-T013 — پیاده‌سازی مبنای Historical Forward P/E همان شرکت.
2. 023 · S7-T014 — محاسبهٔ Historical P/E از داده‌های خام و provenance واقعی.
3. 024 · S7-T015 — انتخاب آخرین مجموعهٔ کامل و معتبر اطلاعات مالی.
4. 025 · S7-T016 — اصلاح انتخاب قیمت بازار و هشدار تاریخ واقعی قیمت جلالی.
5. 026 · S7-T017 — حذف Industry P/E از مسیر فعال ارزش‌گذاری.
6. 027 · S7-T018 — رد P/E پیش‌محاسبه‌شدهٔ فاقد provenance.

**نتیجهٔ مورد انتظار:** اصلاحات قابل‌اثبات OA1 در کد و تست‌ها پیاده‌سازی شوند؛ موارد فاقد داده یا provenance واقعی صریحاً باز بمانند. هیچ داده، تاریخ، فرمول یا provenance ساختگی وارد محاسبات نشود. هیچ خروجی تحلیلی در DB ذخیره نشود.