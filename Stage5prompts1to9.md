PROMPT 1 — Stage 5 Preflight
TASK: Stage 5 — PREFLIGHT / DISCOVERY ONLY

Repository: analyzer

Stage 1, Stage 2, Stage 3, and Stage 4 are frozen.
Stage 4 is now frozen after final audit and full regression.

Stage 5 is the Forecast Engine.

IMPORTANT:
The Stage 5 specification currently says LOCKED, but implementation status must NOT be trusted blindly.
Audit the implementation against the specification before making any changes.

==================================================
LOCAL-ONLY / READ-ONLY
==================================================

Work ONLY on the local working tree.

DO NOT:
- access GitHub
- use GitHub API/CLI
- inspect remotes
- fetch/pull/push/clone
- create commits
- modify any file
- run broad repository tests
- perform implementation
- refactor anything

This is READ-ONLY discovery.

==================================================
READ ONLY THESE FILES
==================================================

1. 05_Stage5_Forecast_Engine.md
2. prompts/05_Stage5_Implementation_Prompt.md
3. src/forecast/schema.py
4. src/forecast/engine.py
5. src/forecast/drivers.py
6. src/tests/test_stage5_forecast.py

Do not inspect unrelated modules unless absolutely necessary to identify a direct Stage 5 boundary dependency.

==================================================
AUDIT ONLY THESE AREAS
==================================================

1. Forecast output schema
2. Forecast versioning
3. PIT / data_cutoff_datetime
4. Baseline hierarchy
5. Revenue forecast
6. Operating margin / operating profit
7. Net profit hierarchy
8. EPS / share-count handling
9. ROE
10. Bank forecast
11. Holding forecast
12. FX separation
13. Bear/Base/Bull scenarios
14. Low Base / Sign Change controls
15. Stage 4 integration boundary
16. Stage 3 isolation
17. Stage 6 isolation
18. Missing != 0
19. Current tests and their actual coverage

==================================================
IMPORTANT
==================================================

Do NOT fix anything.

Do NOT redesign anything.

Do NOT assume the specification is correct merely because it says LOCKED.

Identify actual implementation gaps.

Classify findings:

- COMPLIANT
- PARTIAL
- REAL GAP
- BLOCKER
- NON-BLOCKER
- OUT OF SCOPE

==================================================
FINAL REPORT
==================================================

Return:

1. Current implementation summary
2. What is actually implemented
3. What is missing
4. What is incorrect
5. BLOCKERS
6. NON-BLOCKERS
7. Exact files that need modification
8. Recommended implementation order
9. Existing Stage 5 test count and coverage
10. Maximum 10-line implementation plan

Do NOT modify anything.

Do NOT declare Stage 5 frozen.

STOP immediately after the report.
====================================================================================================

PROMPT 2 — Stage 5 Data Model / PIT / Versioning
TASK: Stage 5 — DATA MODEL / PIT / VERSIONING ONLY

Repository: analyzer

Stage 1–4 are frozen.
Stage 5 is NOT frozen.

Use the Stage 5 specification as the authority.

==================================================
LOCAL-ONLY
==================================================

Work ONLY on the local working tree.

No GitHub.
No remote access.
No GitHub CLI/API.
No push/pull/fetch/clone.
No commits.

Do NOT modify documentation or status files.

==================================================
ALLOWED FILES
==================================================

Prefer ONLY:

- src/forecast/schema.py
- src/forecast/engine.py
- src/tests/test_stage5_forecast.py

Do not modify other files unless absolutely required by this specific task.

==================================================
SCOPE
==================================================

Implement/fix ONLY:

1. ForecastRecord / output schema
2. forecast_horizon
3. forecast_timestamp
4. data_cutoff_datetime
5. model_version
6. scenario
7. forecast_method
8. data_quality
9. assumptions
10. Forecast version preservation
11. No-overwrite semantics
12. Point-in-Time protection
13. Auditability of forecast inputs
14. Missing != 0

A historical forecast must never see information published after its cutoff.

A newer forecast must create a new version, not overwrite an older forecast.

==================================================
DO NOT TOUCH
==================================================

- revenue algorithms
- margin algorithms
- net profit algorithms
- EPS calculations
- ROE
- Bank
- Holding
- scenarios
- Stage 4 calculations
- Stage 3
- Stage 6
- Stage 7
- valuation
- market data

==================================================
TEST
==================================================

Run ONLY:

pytest src/tests/test_stage5_forecast.py -v

Do NOT run full regression.

==================================================
STOP
==================================================

After implementation and targeted tests, STOP.

Final report:

1. Files changed
2. Exact changes
3. PIT behavior
4. Versioning behavior
5. Tests
6. Remaining failures
7. Explicitly state:

"Stage 5 is NOT declared frozen."
====================================================================================================

PROMPT 3 — Non-Financial Forecast Core:
TASK: Stage 5 — NON-FINANCIAL FORECAST CORE ONLY

Repository: analyzer

Stage 1–4 are frozen.
Stage 5 is NOT frozen.

==================================================
LOCAL-ONLY
==================================================

Local working tree only.

No GitHub.
No remote.
No Git operations.
No commits.
No documentation changes.

==================================================
ALLOWED FILES
==================================================

ONLY:

- src/forecast/engine.py
- src/forecast/drivers.py
- src/forecast/schema.py
- src/tests/test_stage5_forecast.py

==================================================
SCOPE
==================================================

Implement/fix ONLY the common Non-Financial Forecast Core:

Industries:

- Petrochemical/Chemical
- Metals/Mining
- Cement
- Food
- Pharmaceutical

There must be ONE common core.

Forecast chain:

Revenue
→ Operating Margin
→ Operating Profit
→ Net Profit
→ EPS
→ ROE

==================================================
REVENUE
==================================================

Respect this hierarchy:

1. Historical/Seasonal Baseline
2. Recent Run Rate
3. Driver-Based Adjustment

Drivers must be actual measurable inputs.

Never fabricate a missing driver.

==================================================
OPERATING PROFIT
==================================================

Operating Margin:

Operating Profit / Revenue

Forecast Operating Profit:

Forecast Revenue × Forecast Operating Margin

Revenue and margin must be independently changeable.

==================================================
NET PROFIT
==================================================

Use this hierarchy:

1. Component-Based
2. Historical Net/Operating conversion
3. Revenue × Net Margin
4. INSUFFICIENT_DATA

Never replace missing data with zero.

==================================================
IMPORTANT
==================================================

Do NOT implement:

- valuation
- P/E
- P/NAV
- market signals
- technical analysis
- ML
- Monte Carlo
- Stage 6 reliability
- Stage 4 recalculation

Do not map a Stage 4 momentum percentage directly into the same forecast growth percentage.

==================================================
TESTS
==================================================

Add focused tests for:

- baseline fallback
- seasonal baseline
- run-rate fallback
- driver present
- driver missing
- margin deterioration
- net-profit fallback hierarchy
- missing data
- determinism

Run ONLY:

pytest src/tests/test_stage5_forecast.py -v

==================================================
STOP
==================================================

Do not audit unrelated Stage 5 areas.

Do not declare Stage 5 frozen.

Report files, changes, tests, failures, and remaining gaps.

====================================================================================================
PROMPT 4 — EPS / ROE / Share Count
TASK: Stage 5 — EPS / ROE / SHARE COUNT ONLY

Repository: analyzer

Stage 1–4 are frozen.
Stage 5 is NOT frozen.

==================================================
LOCAL-ONLY
==================================================

Local only.

No GitHub.
No remote.
No Git operations.
No commits.

==================================================
ALLOWED FILES
==================================================

ONLY:

- src/forecast/engine.py
- src/forecast/schema.py
- src/tests/test_stage5_forecast.py

==================================================
SCOPE
==================================================

Implement/fix ONLY:

1. Forecast EPS
2. Weighted Average Shares
3. ShareCountHistory
4. CorporateAction handling
5. Capital increase
6. Capital decrease
7. Stock split / equivalent share-count changes
8. Forecast Net Profit Attributable to Common Shareholders
9. ROE
10. Average Equity
11. insufficient-data behavior

==================================================
EPS
==================================================

EPS MUST be derived:

Forecast EPS =
Forecast Net Profit Attributable to Common Shareholders
/
Forecast Weighted Average Shares

EPS must NOT be independently guessed or directly forecast.

==================================================
ROE
==================================================

ROE:

Forecast Net Profit / Average Equity

Average Equity:

(Beginning Equity + Ending Equity) / 2

If reliable Equity Forecast is unavailable:

ROE = INSUFFICIENT_DATA

Do NOT fabricate equity.

==================================================
TESTS
==================================================

Add focused tests for:

- unchanged shares
- capital increase
- share-count change
- split/corporate action
- EPS derivation
- missing shares
- missing equity
- ROE calculation
- insufficient ROE data

Run ONLY:

pytest src/tests/test_stage5_forecast.py -v

Do NOT run full regression.

==================================================
BOUNDARIES
==================================================

Do not touch:

- revenue
- margin
- scenarios
- Bank
- Holding
- Stage 4
- Stage 6
- Stage 7

STOP after the targeted tests and report.

Stage 5 is NOT declared frozen.
====================================================================================================
PROMPT 5 — Bank / Holding / FX
TASK: Stage 5 — BANK / HOLDING / FX ONLY

Repository: analyzer

Stage 1–4 are frozen.
Stage 5 is NOT frozen.

==================================================
LOCAL-ONLY
==================================================

Local working tree only.

No GitHub.
No remote.
No Git operations.
No commits.

==================================================
ALLOWED FILES
==================================================

Prefer ONLY:

- src/forecast/engine.py
- src/forecast/drivers.py
- src/forecast/schema.py
- src/tests/test_stage5_forecast.py

==================================================
BANK
==================================================

Implement/fix the Bank specialized core:

Loans / Deposits
→ NII / NIM
→ Net Profit
→ EPS
→ ROE

Possible drivers:

- Loan Growth
- Deposit Growth
- NIM
- NII
- NPL / Credit Quality context

NPL must NOT become an arbitrary profit multiplier.

If no validated relationship exists, NPL remains Context.

==================================================
HOLDING
==================================================

Implement/fix:

NAV
→ NAV Growth
→ Net Profit
→ EPS
→ ROE

P/NAV is Stage 7 and MUST NOT enter Stage 5 forecasting.

==================================================
FX
==================================================

If operating earnings are genuinely FX-linked:

- Operational/exchange FX is preferred.
- FREE_MARKET must never silently substitute for OPERATIONAL.
- Missing operational FX must not silently become free-market FX.
- Any explicit proxy must be identifiable as estimated/low-confidence.

==================================================
TESTS
==================================================

Add focused tests for:

- Bank forecast
- missing NPL
- NPL as context only
- Holding forecast
- P/NAV exclusion
- operational FX
- missing operational FX
- FREE_MARKET ≠ OPERATIONAL
- explicit proxy behavior

Run ONLY:

pytest src/tests/test_stage5_forecast.py -v

Do not touch Stage 4 or Stage 6.

STOP after tests and report.
====================================================================================================
PROMPT 6 — Scenarios / Trend Integration / Controls
TASK: Stage 5 — SCENARIOS / TREND INTEGRATION / CONTROLS ONLY

Repository: analyzer

Stage 1–4 are frozen.
Stage 5 is NOT frozen.

==================================================
LOCAL-ONLY
==================================================

Local only.

No GitHub.
No remote.
No Git operations.
No commits.

==================================================
ALLOWED FILES
==================================================

ONLY:

- src/forecast/engine.py
- src/forecast/drivers.py
- src/forecast/schema.py
- src/tests/test_stage5_forecast.py

==================================================
SCOPE
==================================================

Implement/fix ONLY:

1. Stage 4 integration
2. Trend adjustment
3. Low Base control
4. Sign Change control
5. Bear/Base/Bull scenarios
6. Scenario ordering
7. Historical dispersion / uncertainty
8. Driver-based scenarios

==================================================
STAGE 4
==================================================

Consume Stage 4 outputs.

Do NOT recalculate Stage 4.

Do NOT turn:

Momentum = +10%

into:

Forecast Growth = +10%

Trend is evidence for a bounded, explainable adjustment.

Adjustment must be:

- bounded
- explainable
- recorded
- backtestable

==================================================
LOW BASE
==================================================

LOW_BASE = TRUE must prevent mechanical extrapolation of abnormal historical growth.

==================================================
SIGN CHANGE
==================================================

Loss → Profit and Profit → Loss must not use ordinary percentage growth mechanically.

Respect:

- LOSS_TO_PROFIT
- PROFIT_TO_LOSS
- SIGN_CHANGE
- ZERO_BASE

==================================================
SCENARIOS
==================================================

Produce:

Bear
Base
Bull

Do NOT use arbitrary fixed rules such as ±20%.

Use:

- driver uncertainty
- historical dispersion
- model uncertainty

Where economic ordering is valid:

Bear ≤ Base ≤ Bull

Do NOT artificially sort outputs if the economics do not justify ordering.

==================================================
TESTS
==================================================

Test:

- normal growth
- low base
- loss → profit
- profit → loss
- revenue ↑ / margin ↓
- trend positive
- trend negative
- Bear/Base/Bull
- scenario ordering
- insufficient data

Run ONLY:

pytest src/tests/test_stage5_forecast.py -v

STOP after the targeted tests.

Do not declare Stage 5 frozen.
====================================================================================================
PROMPT 7 — Stage 5 Test Hardening
این مرحله عمداً جداست تا Claude مجبور نشود همزمان implementation و audit و تست کل Stage 5 را در یک context انجام دهد.

TASK: Stage 5 — TEST HARDENING ONLY

Repository: analyzer

Stage 5 implementation work has been completed in previous isolated tasks.

This task is ONLY to strengthen Stage 5 tests.

==================================================
LOCAL-ONLY
==================================================

Read/write only local working tree.

No GitHub.
No remote.
No Git operations.
No commits.

==================================================
ALLOWED FILES
==================================================

ONLY:

- src/tests/test_stage5_forecast.py
- src/forecast/engine.py
- src/forecast/drivers.py
- src/forecast/schema.py

Prefer modifying ONLY tests.

==================================================
TEST REQUIREMENTS
==================================================

Ensure focused tests cover:

1. Non-financial common core
2. Revenue hierarchy
3. Margin independence
4. Net profit hierarchy
5. EPS derivation
6. Share-count changes
7. Corporate actions
8. ROE
9. Bank
10. Holding
11. Operational FX separation
12. Missing != zero
13. Low Base
14. Sign Change
15. Bear/Base/Bull
16. Scenario ordering
17. Stage 4 evidence consumption without recalculation
18. PIT cutoff
19. Forecast version preservation
20. Determinism
21. Missing drivers
22. insufficient data

Also test forbidden behavior where practical:

- no P/NAV in Stage 5
- no Fundamental Score multiplication
- no direct momentum→forecast mapping
- no future-data usage
- no overwrite of historical forecasts

==================================================
TEST
==================================================

Run ONLY:

pytest src/tests/test_stage5_forecast.py -v

Do NOT run full regression.

Do not redesign implementation merely to satisfy a bad test.

If an expectation conflicts with the specification, correct the test and explain why.

==================================================
STOP
==================================================

No broad audit.

No documentation.

No freeze.

Report:

- test count before/after
- tests added/changed
- failures
- remaining coverage gaps

Stage 5 is NOT declared frozen.
====================================================================================================
PROMPT 8 — Final Stage 5 Audit

این را حتماً در Chat جدید اجرا کن.
TASK: Stage 5 — FINAL READ-ONLY AUDIT

Repository: analyzer

Stage 1–4 are frozen.
Stage 5 implementation and focused tests are now complete.

This is READ-ONLY.

==================================================
DO NOT MODIFY
==================================================

No file modifications.

No GitHub.
No remote.
No Git operations.
No commits.

Do not fix anything.

==================================================
READ
==================================================

Read:

1. 05_Stage5_Forecast_Engine.md
2. src/forecast/schema.py
3. src/forecast/engine.py
4. src/forecast/drivers.py
5. src/tests/test_stage5_forecast.py

Read Stage 3/4 boundary definitions only where required.

==================================================
AUDIT
==================================================

Audit:

1. Non-financial common core
2. Revenue hierarchy
3. Operating margin
4. Operating profit
5. Net profit hierarchy
6. EPS
7. Share count / corporate actions
8. ROE
9. Bank
10. Holding
11. FX separation
12. Baselines
13. Trend integration
14. Low Base
15. Sign Change
16. Bear/Base/Bull
17. Scenario ordering
18. PIT
19. Versioning
20. Auditability
21. Missing != zero
22. Data quality
23. Determinism
24. Stage 3 isolation
25. Stage 4 isolation
26. Stage 6 isolation
27. Stage 7 isolation
28. No double counting
29. Complexity control

==================================================
IMPORTANT
==================================================

Pay special attention to:

- look-ahead bias
- forecast cutoff
- forecast version overwrite
- operational FX silently becoming FREE_MARKET
- direct Fundamental Score → forecast multiplier
- direct momentum → forecast growth
- arbitrary Bear/Base/Bull percentages
- fabricated missing drivers
- fabricated equity/share count
- P/NAV leaking into Stage 5
- Stage 4 being recalculated instead of consumed

==================================================
TEST
==================================================

Run ONLY:

pytest src/tests/test_stage5_forecast.py -v

==================================================
FINAL REPORT
==================================================

Return:

1. Forecast Core
2. Revenue
3. Profit Chain
4. EPS / Share Count
5. ROE
6. Bank
7. Holding
8. FX
9. Scenarios
10. Stage 4 integration
11. PIT / Versioning
12. Data Integrity
13. Stage Boundaries
14. Test Result
15. BLOCKERS
16. NON-BLOCKERS
17. FINAL STATUS

FINAL STATUS must be exactly:

READY FOR FULL REGRESSION

or

NOT READY FOR FULL REGRESSION

Never write Stage 5 FROZEN.

No modifications.
====================================================================================================
PROMPT 9 — Full Regression / Freeze

این آخرین Prompt است و باز هم Chat جدید.
TASK: Stage 5 — FINAL FULL REGRESSION VERIFICATION

Repository: analyzer

Stage 1–4 are frozen.
Stage 5 has passed its final focused audit.

This task is READ-ONLY verification only.

==================================================
NO MODIFICATIONS
==================================================

Do NOT modify files.

Do NOT fix failures.

Do NOT access GitHub or any remote repository.

Do NOT use Git operations.

Do NOT create commits.

==================================================
TEST
==================================================

Run the project's complete CI-equivalent test command:

PYTHONPATH=. pytest src/tests -v

If the bare command resolves to the wrong Python interpreter, use the project's existing virtualenv interpreter while preserving the exact pytest arguments.

Do NOT change source or tests to make failures pass.

==================================================
IF FAILURE
==================================================

If any test fails:

- do not fix it
- identify exact tests
- identify exact reason
- determine whether Stage 5 regression, unrelated failure, or environment issue
- Stage 5 is NOT ready for freeze

==================================================
IF SUCCESS
==================================================

Report:

- passed
- failed
- skipped
- errors
- warnings
- runtime

Also confirm Stage 5 focused tests ran without failures.

==================================================
FINAL STATUS
==================================================

Choose exactly:

READY FOR STAGE 5 FREEZE

or

NOT READY FOR STAGE 5 FREEZE

Do NOT declare Stage 5 frozen.

Confirm:

- no files modified
- no GitHub/remote access
- no Git operations
- no commits

