# P69 — Minimal Pipeline Contract and Integration Plan (Read-Only)

You are continuing Stage 7 remediation in the local project folder `analyzer`.

## Authoritative context

Read `stepsForStage7.md` first. Then review the latest P68-B report in `reply.md`.

P68-B is the current architecture-audit baseline. Do not repeat the earlier investigation into whether `select_market_history_as_of(...)` exists. It exists in `src/ingestion/market/queries.py`.

The verified findings to carry forward are:

- Stage 5 reads Stage 1 financial facts and accepts a Trend result; a production caller connecting Stage 3 to Stage 5 has not been established.
- Stage 7 has a service-level path into Stage 9.
- Stage 8's historical query exists, but a production adapter/caller connecting it to `MarketEngine.analyze_market(...)` has not been established.
- The query returns Jalali-dated observations, while the market engine requires Gregorian `datetime` values and dictionary rows with a `date` field.
- No application-level end-to-end orchestration path or confirmed downstream consumer/persistence destination for Stage 9 was identified in the audited source.
- `src/valuation/engine.py` redesign remains the final technical step and must stay deferred.

## Snapshot consistency requirement

Use the exact current `analyzer.zip` snapshot supplied for this review, and verify the relevant source files directly before relying on prior reports. The latest P68-A-Fix rerun confirms that `MarketHistoryObservation` and `select_market_history_as_of(...)` exist in `src/ingestion/market/queries.py`.

Treat P68-B as the current call-path audit, not as unquestionable truth: verify its material claims against the same snapshot, especially the Stage 3 → Stage 5 relationship, Stage 8 date-contract mismatch, application entry points, and Stage 9 downstream consumer. If a claim cannot be verified, label it unverified rather than repeating it as fact. Do not spend time re-proving the existence of the historical query unless the supplied snapshot differs.

## Objective

Produce a minimal, evidence-based architecture and integration plan that resolves the decisions required before implementation. This is a read-only design task.

Do not implement the plan in this prompt.

## Required analysis

### 1. Establish the actual stage responsibilities

Using source evidence, determine whether Stage 3 fundamental scoring is intended to be:

- a required input to Stage 5,
- an independent input to Stage 9, or
- part of another explicitly defined path.

Do not infer a dependency merely because two stages exist. Use specifications and existing service/schema contracts. If the intended relationship cannot be established, record it as an unresolved product/architecture decision.

### 2. Define the minimum Stage 8 integration contract

Review the existing historical query, observation dataclass, market engine input contract, and market result schema.

Specify the required contract for a future adapter, including:

- authoritative company identity;
- Jalali as-of date and inclusive cutoff semantics;
- source row ordering and duplicate handling;
- treatment of missing OHLCV values;
- the required `MarketEngine` input row shape;
- the origin and semantics of the engine's `as_of_date`;
- whether and how Jalali dates can be mapped to the engine's Gregorian `datetime` contract.

Do not invent a Jalali-to-Gregorian conversion rule. Do not assume that `trade_date` is authoritative when it may be null. If the existing project does not define a safe date mapping, state exactly what decision or source contract is needed before coding.

Do not invent lookback windows, minimum sample sizes, fallback price rules, synthetic observations, or benchmark series. Do not create a second historical query unless evidence shows the existing one cannot satisfy the required contract.

### 3. Define the minimum end-to-end orchestration contract

Identify the minimum inputs and outputs needed to coordinate the existing services without duplicating their responsibilities.

Address:

- where the database session is created, owned, and closed;
- where the authoritative Jalali as-of date comes from and how it is passed consistently;
- how the Stage 5 forecast result is obtained and passed to Stage 7;
- how a genuine Stage 8 result is generated and passed to Stage 9;
- how Stage 3 results are consumed, if required by an approved contract;
- what happens to the Stage 9 result after it is returned.

Do not assume a CLI, API, scheduler, new persistence model, or application framework. Present these only as alternatives if the repository does not establish an intended choice. Recommend the smallest architecture consistent with existing code and specifications, and clearly mark decisions that require owner approval.

### 4. Produce an implementation sequence

Give a dependency-ordered sequence of small implementation steps. For each step, specify:

- the exact files likely to require changes;
- the contract it establishes;
- prerequisite decisions;
- the financial/PIT invariants that must remain true;
- the specific test coverage needed, including negative and boundary cases.

Separate confirmed requirements from proposed design choices.

## Strict constraints

- Read-only: do not edit source, tests, specs, reports, or `stepsForStage7.md`.
- Do not run tests, the application, database commands, or Git commands.
- Do not redesign `src/valuation/engine.py`.
- Do not add formulas, data, dates, calendar conversions, thresholds, persistence schemas, or dependencies without evidence and approval.
- Do not claim end-to-end integration is complete merely because individual services or unit tests exist.
- Preserve Stage 5 EPS as the authoritative forecast EPS; Stage 7 must not recompute it.
- Preserve Jalali date handling and fail-closed PIT behavior. A cutoff date alone does not prove historical availability.
- Distinguish verified source behavior, inferred behavior, proposed design, and unresolved decisions.

## Required report

Return a concise but evidence-rich report containing:

1. Confirmed contracts and source evidence.
2. Unresolved architecture decisions, ranked by implementation impact.
3. A minimal proposed orchestration contract.
4. A dependency-ordered implementation plan with exact file paths.
5. Required tests for the owner to run later.
6. A clear decision on whether any coding is safe to begin before the unresolved decisions are settled.

Do not modify `reply.md`; return the report in your response so the owner can review it before deciding what to retain.