# PROJECT HANDOFF INSTRUCTIONS
# Repository: analyzer

## 0. PURPOSE OF THIS DOCUMENT

This document is the operational handoff for continuing the `analyzer` project in a new ChatGPT conversation.

It is NOT merely a project summary.

It defines:

- the current architectural state
- frozen stages
- active stage
- non-negotiable invariants
- how ChatGPT should supervise the project
- how Claude Code should be instructed
- how Claude context limitations must be handled
- how implementation work must be split
- how Git/GitHub responsibilities are divided
- lessons learned from Stage 4
- current Stage 5 findings
- rules for deciding when a stage may be frozen

The repository must always be referred to as:

    analyzer

Never refer to it as:

    lovelyroz/analyzer

The GitHub owner/repository identity is not relevant to implementation instructions.

---

# 1. PROJECT ROLE SPLIT

The project uses two AI agents with different responsibilities.

## ChatGPT

ChatGPT is the architecture / quality-control / supervision layer.

ChatGPT should:

- inspect architecture and specifications
- review Claude reports
- identify missing or incorrect implementation
- design small, scoped Claude prompts
- decide whether a stage is ready for the next verification step
- check architectural boundaries
- protect frozen stages
- identify blockers
- prevent scope creep
- prevent context exhaustion
- decide when a stage can be frozen

ChatGPT should NOT casually ask Claude to perform broad audits and implementation simultaneously.

---

## Claude Code

Claude Code is the implementation agent.

Claude Code should:

- work on the local working tree
- implement narrowly defined tasks
- run focused tests
- report exact changes
- stop when the assigned task is complete

Claude Code must NOT be treated as the architecture owner.

Claude must not independently redesign the architecture.

---

# 2. CRITICAL CLAUDE / GIT RULE

This is one of the most important project rules.

Claude Code must work ONLY on the local working tree.

Every implementation prompt must explicitly contain:

    Work ONLY on the local working tree on my laptop.

    Do NOT access GitHub or any remote repository.
    Do NOT use GitHub API or GitHub CLI.
    Do NOT inspect remotes.
    Do NOT fetch, pull, push, or clone.
    Do NOT create commits.
    I will handle all Git operations myself.

For READ-ONLY audit prompts:

    Do not modify any files.
    Do not create commits.
    Do not perform Git operations.

The user handles:

- git add
- git commit
- git push
- GitHub verification

unless the user explicitly changes this rule.

Never assume Claude should perform GitHub operations.

---

# 3. CONTEXT LIMITATION — CRITICAL OPERATING RULE

Claude Code has a finite context window.

This became a significant practical problem during Stage 4.

A broad Stage 4 prompt caused:

- excessive context consumption
- very long execution
- mixed implementation and audit work
- the user had to stop the run
- useful context was lost

Therefore:

## NEVER give Claude one giant implementation/audit prompt.

Large stages must be divided into multiple small tasks.

Preferred pattern:

    Chat 1 → discovery
    Chat 2 → implementation part A
    Chat 3 → implementation part B
    Chat 4 → implementation part C
    Chat 5 → test hardening
    Chat 6 → final audit
    Chat 7 → full regression

Each chat should have a narrow objective.

---

## New Claude chat rule

When a Claude chat has consumed substantial context, especially around 40–50% or more:

DO NOT continue adding unrelated work to that chat.

Start a new Claude chat.

This is especially important before:

- final audits
- full regression
- architecture reviews
- new major implementation areas

---

## Prompt size rule

A Claude prompt should generally specify:

1. exact task
2. exact allowed files
3. exact forbidden scope
4. exact tests
5. exact stop condition
6. exact final report

Do not ask Claude to:

- implement
- refactor
- audit
- optimize
- redesign
- run full regression

all in one prompt.

---

# 4. STOP CONDITIONS ARE MANDATORY

Every Claude prompt should have an explicit stop condition.

Example:

    STOP after the requested implementation and targeted tests.

    Do not perform a broad audit.
    Do not fix unrelated issues.
    Do not declare the stage frozen.

This prevents Claude from expanding the scope and consuming unnecessary context.

---

# 5. ARCHITECTURE

The project has EXACTLY NINE analytical stages.

There is NO Stage 10.

The architecture is frozen at nine stages.

Stage order:

1. Data Foundation / Ingestion
2. KPI Specification
3. Fundamental Scoring
4. Historical / Seasonal / Trend
5. Forecast Engine
6. Reliability / Forecast Evaluation
7. Valuation
8. Decision / Portfolio Logic
9. Final Output / Decision Layer

Do not introduce a Stage 10.

Do not move responsibilities between stages without explicit architectural approval.

---

# 6. FROZEN STAGES

Current frozen status:

## Stage 1

FROZEN.

Data foundation / ingestion is complete.

Important invariant:

    CODAL PDF / external source
        ↓
    PDF extraction adapter
        ↓
    Sequence[RawLineInput]
        ↓
    ingest_codal_report()
        ↓
    database foundation

Extraction must not contain:

- KPI mapping
- scoring
- forecasting
- valuation
- decision logic

---

## Stage 2

FROZEN.

Stage 2 defines:

    What is measured?

It is KPI specification, not scoring.

Stage 1 → Stage 2 production wiring is a separate integration concern and must not be silently inserted into Stage 2.

---

## Stage 3

FROZEN.

Stage 3 produces the Fundamental Score.

Three axes:

- Growth = 30%
- Profitability = 45%
- Risk & Quality = 25%

Final score:

    0.30 × Growth
    + 0.45 × Profitability
    + 0.25 × RiskQuality

Stage 3 does NOT contain:

- valuation
- market price
- technical analysis
- momentum
- forecasting
- future expectations

RESTATED / ESTIMATED may remain numerically scoreable but must result in:

    score_data_quality = LIMITED

SUSPICIOUS remains unscored.

Do not reopen Stage 3 unless there is an explicit architectural reason.

---

## Stage 4

FROZEN / COMPLETE.

Stage 4 is:

    Historical
    Seasonal
    Trend

It provides context and direction.

It does NOT produce:

- Fundamental Score
- valuation
- forecast
- market signal
- independent Trend Score

Stage 4 final verification:

    Targeted:
    102 passed
    0 failed
    0 skipped
    0 errors

    Full regression:
    371 passed
    0 failed
    2 skipped
    0 errors

Important Stage 4 blockers that were discovered and fixed:

### B1
Stock 12M incorrectly used TTM/window aggregation.

Correct:

    FLOW 12M
        = current TTM / TTM ending 12 months earlier - 1

    STOCK 12M
        = current period-end / period-end 12 months earlier - 1

Stock values must NEVER be summed.

### B2
Flow/stock momentum semantics and several test expectations were inconsistent.

Correct:

    FLOW:
        window sum / previous window sum - 1

    STOCK:
        period-end / previous period-end - 1

Tests were corrected where tests contradicted the specification.

### B3
Relative Strength self-counting.

The current observation was accidentally included in its own historical percentile distribution.

This violated:

- PIT
- no-lookahead
- minimum historical observation requirements

The current observation must NOT be included in its own historical distribution.

This was fixed and regression-tested.

---

# 7. DATABASE CONTRACT

DATABASE_CONTRACT_V1.3 is LOCKED.

Important invariants:

- NULL != 0
- PIT is mandatory
- raw facts are immutable
- historical report versions must remain reproducible
- Report and ReportVersion are separate
- ingestion must be auditable
- failed ingestion must not create partial raw/report data
- production ingestion is idempotent
- historical versions must never be silently overwritten

---

# 8. FX RULES

FREE_MARKET and OPERATIONAL FX are separate concepts.

Never silently substitute:

    FREE_MARKET

for:

    OPERATIONAL

Operational FX is stored in IRR.

Toman → Rial conversion must happen explicitly at the adapter boundary.

Any FX proxy must be explicit and identifiable as an estimate.

---

# 9. MISSING DATA RULE

This is a global invariant.

    NULL != 0

Never convert missing data into zero merely to make calculations continue.

If insufficient information exists:

    INSUFFICIENT_DATA

is preferable to fabricated precision.

---

# 10. PIT RULE

Point-in-Time correctness is mandatory.

A historical analysis or forecast using:

    data_cutoff_datetime

must NOT use information published after that cutoff.

The following are different:

- period date
- publication date
- data cutoff
- forecast timestamp

Never confuse them.

---

# 11. CURRENT ACTIVE STAGE: STAGE 5

Stage 5 is:

    Forecast Engine

Stage 5 is NOT frozen yet.

The Stage 5 specification exists, but the Preflight discovered that the implementation is substantially incomplete despite the specification describing Stage 5 as locked.

Therefore:

    specification status ≠ implementation status

The implementation must be audited against actual behavior.

---

# 12. STAGE 5 PREFLIGHT RESULT

The file:

    stage5report.md

contains the Stage 5 Preflight / Discovery report.

It is a critical source of truth for current implementation gaps.

The report found:

## Currently compliant

- output schema
- common non-financial chain
- net profit hierarchy
- Bank core
- Holding core
- Low Base control
- configurable model parameters
- Stage 6 separation at the current abstraction level
- margins as decimal ratios
- missing-data propagation
- Stage 7 consumption boundary
- no direct double-counting of TTM/Fundamental Score

---

# 13. STAGE 5 REAL GAPS

The Preflight identified these gaps.

## Forecast Versioning

REAL GAP.

There is currently no real forecast persistence/version repository.

CompanyForecastResult is only an in-memory dataclass.

Therefore:

- no actual version history
- no real never-overwrite enforcement
- no real earnings revision trend

---

## PIT enforcement

REAL GAP.

data_cutoff_datetime exists, but it is currently only stored.

There is no real filtering of source ReportVersions based on publication_date.

This means PIT is not actively enforced.

---

## Weighted Average Shares

REAL GAP.

ShareCountHistory and CorporateAction structures exist, but they are not actually queried.

There is no real weighted-average-share builder.

forecast_weighted_average_shares is not properly produced by a builder.

---

## Stage 4 → Stage 5 adapter

REAL GAP.

Stage 4 output does not directly match the Stage 5 financial_context input.

An explicit adapter is needed.

Do NOT manually reconstruct Stage 4 logic inside Stage 5.

The adapter should consume Stage 4 output.

---

## Drivers

PARTIAL.

driver_revenue_adjustment currently behaves as a raw single value.

The specification describes richer drivers such as:

- Volume
- Price
- Margin
- Financial Cost

These are not fully implemented.

---

## Bank

PARTIAL.

NPL is not currently exposed as context.

NIM is not currently represented as a real input despite specification language.

However, NPL must NOT automatically become a profit multiplier.

---

## FX

REAL GAP.

operational_fx currently exists only as an assumption/log.

It does not participate in forecast calculations.

There is no active validation preventing silent FX substitution.

---

## Scenario spread

REAL GAP / specification compliance issue.

Current defaults include hard-coded values such as:

- ±5% growth
- ±2% margin
- ±1% net margin

These are parameterized, but the default values are arbitrary and not derived from historical dispersion.

The specification expects scenario uncertainty to be explainable and preferably dispersion-based.

Do not replace these blindly with another arbitrary constant.

---

## Sign Change

REAL GAP.

The implementation logs sign change but does not actually prevent mechanical extrapolation.

Must properly handle:

- LOSS_TO_PROFIT
- PROFIT_TO_LOSS
- SIGN_CHANGE
- ZERO_BASE

Do not use ordinary percentage-growth arithmetic blindly across zero/sign changes.

---

## Baseline hierarchy

PARTIAL.

The intended multi-level baseline hierarchy is not fully implemented.

The current implementation selects a base rather than fully implementing the specified hierarchy.

---

## Forecast horizon

PARTIAL.

1M / 3M / 6M / 12M are validated, but the horizon is not fully connected to distinct forecast logic.

Currently, some horizons effectively produce the same result.

This must be corrected according to the specification, not through arbitrary multipliers.

---

# 14. STAGE 5 EXISTING TEST COVERAGE

The Preflight found only 8 Stage 5 tests initially.

All 8 passed.

However, coverage was poor.

Only approximately 3 of the 16 specification scenarios were meaningfully covered.

Important missing tests include:

1. normal growth
2. seasonality / Low Base interaction
3. Loss → Profit
4. Profit → Loss
5. Revenue growth + margin decline
6. share-count change
7. Fundamental vs Trend separation
8. Stage integration
9. missing data
10. missing driver
11. Low Base
12. Bear/Base/Bull ordering
13. forecast versioning
14. PIT cutoff
15. Bank
16. Holding

Additionally:

- operational FX separation
- revision trend
- share-count corporate actions
- insufficient seasonality

need explicit tests.

---

# 15. STAGE 5 BLOCKERS FROM PREFLIGHT

The initial Stage 5 Preflight identified:

## B1 — Production Forecast Pipeline

ForecastEngine is not connected to a real production data path.

There is no proper:

    Stage 4 output
        ↓
    Stage 5 adapter
        ↓
    ForecastEngine
        ↓
    Forecast persistence

Without this, Stage 5 cannot actually produce auditable production forecasts.

---

## B2 — Forecast Versioning

Forecast versioning does not actually exist.

The specification requires never-overwrite/version preservation.

A real model/repository is required.

---

## B3 — PIT Enforcement

PIT is currently only represented as a field.

There is no actual:

    publication_date <= data_cutoff_datetime

enforcement path.

This is a blocker.

---

# 16. STAGE 5 SUGGESTED IMPLEMENTATION ORDER

The Preflight suggested:

1. Stage 4 → Stage 5 adapter
2. Weighted-average-share builder
3. ForecastVersion / ForecastScenario persistence model
4. Forecast repository with never-overwrite
5. PIT query based on publication_date
6. Sign-change enforcement
7. Forecast horizon application
8. Operational FX path
9. Dispersion-based scenario spreads
10. Comprehensive tests

This order should be reconsidered by ChatGPT after each implementation step if new evidence changes dependencies.

Do not blindly execute all ten steps in one Claude session.

---

# 17. CURRENT STAGE 5 WORKFLOW

Stage 5 implementation must be divided into multiple Claude chats.

Recommended structure:

    P1 — Preflight / Discovery
    P2 — Data model / PIT / Versioning
    P3 — Non-Financial Forecast Core
    P4 — EPS / ROE / Share Count
    P5 — Bank / Holding / FX
    P6 — Scenarios / Trend Integration / Controls
    P7 — Test Hardening
    P8 — Final Read-Only Audit
    P9 — Full Regression

Important:

P1 was already executed.

Its report is stored in:

    stage5report.md

At the time of this handoff, P2 is being executed.

Do NOT assume P2 has completed unless a new report explicitly says so.

---

# 18. RULE FOR USING stage5report.md

The Stage 5 Preflight report is evidence, not an unquestionable architectural authority.

Use it to understand:

- what was inspected
- what was found
- what was missing
- what was proposed

But subsequent implementation must still be checked against:

    05_Stage5_Forecast_Engine.md

and actual code behavior.

If implementation and report disagree, inspect the actual implementation.

If specification and implementation disagree, do not silently decide which one is correct.

Report the discrepancy to ChatGPT.

---

# 19. CLAUDE FILE-SCOPE RULE

Every implementation prompt should explicitly list allowed files.

Prefer:

    src/forecast/engine.py
    src/forecast/drivers.py
    src/forecast/schema.py
    src/tests/test_stage5_forecast.py

New files should be introduced only when justified.

For example, the Preflight proposed:

    src/forecast/repo.py
    src/forecast/builder.py
    src/forecast/adapter.py

and potentially new model/migration files.

But Claude must NOT create these merely because the report mentions them.

A prompt must explicitly authorize them.

---

# 20. DO NOT REOPEN FROZEN STAGES

Stage 4 is frozen.

Do not modify Stage 4 to make Stage 5 easier.

If Stage 5 cannot consume Stage 4 correctly:

    build an adapter

Do not rewrite Stage 4.

Likewise:

- do not modify Stage 3 to improve Stage 5
- do not add forecast logic to Stage 4
- do not add valuation logic to Stage 5

---

# 21. STAGE 4 → STAGE 5 BOUNDARY

Stage 5 may consume Stage 4 information.

It must NOT recalculate Stage 4.

For example, Stage 4 may provide:

- seasonal baseline
- seasonal surprise
- momentum
- direction
- relative strength
- low-base context
- sign-change context
- confidence
- data sufficiency

Stage 5 should consume these through an explicit adapter.

Do not duplicate the Stage 4 formulas in Stage 5.

---

# 22. STAGE 3 → STAGE 5 BOUNDARY

Stage 5 must not simply use:

    Fundamental Score × arbitrary multiplier

to produce a forecast.

Stage 3's score is contextual evidence, not a forecast-growth coefficient.

No direct:

    Fundamental Score → forecast growth

unless explicitly specified and justified by the architecture.

Avoid double counting.

---

# 23. STAGE 5 → STAGE 6 BOUNDARY

Stage 5 produces forecasts.

Stage 6 evaluates forecast reliability.

Do not put reliability scoring into Stage 5.

Do not let Stage 5 consume future realized outcomes.

---

# 24. STAGE 5 → STAGE 7 BOUNDARY

Stage 5 provides scenario forecasts.

Stage 7 may consume scenario forecasts for valuation.

Stage 5 must NOT perform:

- P/E valuation
- P/B valuation
- P/NAV valuation
- target price
- valuation multiple selection

Holding NAV forecasting is allowed where explicitly part of the Holding forecast core.

P/NAV valuation itself belongs to Stage 7.

---

# 25. QUALITY PRINCIPLES

The project prioritizes:

    correctness
    auditability
    reproducibility
    PIT correctness
    explicit provenance
    deterministic behavior

over:

    speed
    cleverness
    premature abstraction
    minimizing line count

Do not optimize prematurely.

A transparent implementation is preferable to a clever implementation.

---

# 26. TESTING STRATEGY

Do NOT immediately run the full repository suite after every tiny change.

Use:

    targeted test
        ↓
    inspect result
        ↓
    next scoped task
        ↓
    final focused suite
        ↓
    final full regression

For Stage 5:

    pytest src/tests/test_stage5_forecast.py -v

should normally be the targeted test.

Only after the final audit should the complete repository suite be executed.

---

# 27. FULL REGRESSION

The CI-equivalent full regression command is:

    PYTHONPATH=. pytest src/tests -v

If the shell resolves the wrong Python interpreter, use the project's existing virtual environment while preserving the same pytest arguments.

Do not treat an environment error as a code failure.

Example:

    system Python lacks sqlalchemy
        ≠
    project test failure

Use the project's actual development environment.

---

# 28. WARNINGS

Warnings are not automatically failures.

However:

- do not ignore correctness warnings
- distinguish deprecation warnings from behavioral warnings
- do not change unrelated code merely to eliminate warnings during a stage freeze

During Stage 4, many warnings were caused by:

    datetime.utcnow()

These were not considered correctness blockers.

---

# 29. FINAL AUDIT RULE

A final audit must be READ-ONLY.

It must not:

- fix code
- refactor code
- modify tests
- modify docs
- modify status files
- commit
- push

If the audit finds a blocker:

    STOP

Then create a new narrowly scoped implementation prompt.

Do not allow the audit chat to turn into an implementation chat.

---

# 30. FREEZE RULE

A stage may be called FROZEN only when all of the following are true:

1. specification has been compared against implementation
2. implementation gaps are resolved
3. blockers are resolved
4. targeted tests pass
5. edge cases are tested
6. boundaries with adjacent stages are verified
7. PIT behavior is verified where relevant
8. determinism is verified
9. full regression passes
10. CI for the final repository state passes
11. working tree / repository state is understood
12. no known unresolved correctness blocker remains

A stage must NOT be called frozen merely because:

- the code exists
- the specification says LOCKED
- unit tests pass
- one audit passes

---

# 31. IMPORTANT LESSON FROM STAGE 4

Stage 4 taught several important lessons.

## Lesson 1

A specification can say:

    LOCKED

while implementation is still incomplete.

Always verify implementation against the specification.

---

## Lesson 2

Tests can themselves be wrong.

During Stage 4 several test expectations contradicted the documented flow/stock semantics.

Do not change correct implementation merely to satisfy an incorrect test.

First determine:

    specification
        vs
    implementation
        vs
    test expectation

Then fix the incorrect layer.

---

## Lesson 3

A small hidden bug can be architecturally important.

Stage 4 B3 was only a one-line range error:

    len(values) + 1

instead of:

    len(values)

But it caused:

- self-counting
- invalid minimum observation count
- percentile distortion
- potential Trend State distortion
- PIT/no-lookahead violation

Therefore tiny code changes must still be audited conceptually.

---

## Lesson 4

Do not assume production integration exists.

Stage 2 had a similar discovery:

the analytical engine existed, but production wiring was not necessarily present.

Stage 5 Preflight found the same pattern:

    ForecastEngine exists

but:

    real production pipeline does not yet exist.

Always distinguish:

    "function exists"

from:

    "production system actually uses the function"

---

## Lesson 5

Do not allow context exhaustion.

A large prompt can cause Claude to spend most of its context on:

- reading unrelated files
- broad audits
- repeated explanations
- unnecessary test runs

Instead:

    small task
    → focused files
    → focused test
    → report
    → new chat

---

# 32. CHATGPT OPERATING PROCEDURE

For every new Claude report:

1. Read the report carefully.
2. Compare it with the current specification.
3. Identify real blockers.
4. Do not automatically accept Claude's conclusion.
5. If correct, design the next smallest task.
6. If incorrect, explain the discrepancy and create a corrective prompt.
7. Keep frozen stages protected.
8. Avoid broad prompts.
9. Preserve context budget.
10. Keep implementation and audit separate.

---

# 33. WHEN A USER SAYS "CONTINUE"

Do not assume continuation means:

    "continue coding"

First determine the current state:

- which stage
- which prompt
- which chat
- which files changed
- which tests passed
- whether the current task is implementation or audit
- whether the current stage is frozen

If this information is not available, inspect the project handoff/status/report files first.

---

# 34. WHEN A REPORT CLAIMS "COMPLETE"

Do not immediately accept:

    COMPLETE

as:

    FROZEN

Instead distinguish:

    implementation complete
    targeted tests pass
    audit complete
    full regression pass
    CI pass
    freeze

These are different states.

---

# 35. GIT / GITHUB RESPONSIBILITY

The user normally manages Git.

Claude:

    local implementation only

User:

    commit
    push
    GitHub verification

ChatGPT may inspect GitHub when necessary for architectural verification or repository-state verification, but Claude implementation instructions must remain local-only.

---

# 36. CURRENT HANDOFF STATE

At the time this document is being created:

    Stage 1 = FROZEN
    Stage 2 = FROZEN
    Stage 3 = FROZEN
    Stage 4 = FROZEN
    Stage 5 = ACTIVE / NOT FROZEN

Stage 5 Preflight has been completed.

Preflight report:

    stage5report.md

P2 is currently being executed.

Do not assume P2 is complete until its final report is available.

---

# 37. NEXT ACTION

After P2 finishes:

1. Bring the complete P2 report to ChatGPT.
2. Do not immediately execute all remaining prompts.
3. ChatGPT should inspect P2 against:
   - Stage 5 specification
   - stage5report.md
   - actual implementation claims
4. Only then authorize P3 or revise the plan.

Continue with one narrowly scoped Claude chat at a time.

---

# 38. FINAL PRINCIPLE

The project is not being optimized for the fastest path to "working code".

It is being optimized for:

    auditable correctness
    reproducibility
    PIT safety
    architectural separation
    deterministic behavior
    explicit data provenance
    controlled complexity

When speed conflicts with correctness:

    correctness wins.

When a broad task conflicts with Claude context limitations:

    split the task.

When a convenient shortcut crosses a stage boundary:

    do not take the shortcut.

When data is missing:

    preserve missingness.

When a historical result must be reproduced:

    preserve the information available at that point in time.

When a stage is frozen:

    protect it.