# P45 — Implement Reliable Jalali Calendar Validation for Market-Price Selection

You are continuing Stage 7 remediation in the local project directory `analyzer`.

## Context and confirmed P44 outcome

P44 corrected the Stage 7 → Stage 9 orchestration test. The user subsequently ran `src/tests/test_stage9_decision.py`; all 15 tests passed.

The market-price selector is implemented in `src/ingestion/market/queries.py` as `select_market_price_as_of(...)`. Its current date parsing relies on `parse_jalali_components`, which checks the date format and basic month/day ranges but does not guarantee that the date exists in the Jalali calendar.

P44 confirmed that no complete Jalali calendar validator was identified during its inspection. Impossible stored dates could therefore be considered by the selector.

## Mandatory operating constraints

- Work locally and only inside the existing `analyzer` project.
- Do not use GitHub, GitHub CLI/API, remotes, push, pull, commit, or branch-changing operations.
- Do not run tests or CI. The user will run tests and provide the actual results.
- Do not edit `reply.md`, `temp_report.md`, `temp_report2.md`, `ClaudeReports/`, `stepsForStage7.md`, or `stage_7_prompts.md`.
- Do not perform a repository-wide scan. Inspect only the date parser, market-price selector, dependency manifests, and directly relevant tests.
- Do not redesign `engine.py`, change valuation formulas, alter EPS, convert Jalali dates to Gregorian dates, or change the market-price selection policy.
- Do not weaken, delete, skip, or rewrite existing tests merely to make them pass.

## Required implementation

### 1. Select a reliable calendar validator

Inspect the existing dependency manifests and current date-related imports. Determine whether the project already has a dependable Jalali calendar validator.

- Prefer a suitable validator already declared and used by the project.
- If none exists, evaluate whether a maintained Jalali-date library can be added consistently with the project's dependency-management conventions. If you add one, update the correct dependency manifest and use its actual calendar-validation behavior.
- Do not implement a homemade Jalali leap-year or month-length algorithm.
- Do not claim a dependency is available merely because it appears importable in your environment; account for whether it is declared for project installation.

### 2. Validate both requested and stored dates

Use the reliable validator at the narrowest appropriate boundary so that:

- An impossible requested as-of Jalali date is rejected clearly.
- An impossible stored market observation cannot be selected.
- Valid Jalali dates, including valid leap-year boundary dates, remain supported.
- Existing behavior for company isolation, latest eligible prior date, adjusted-close preference, close fallback, missing observations, duplicate latest-date observations, and provenance is preserved.
- Existing malformed or undated records are handled consistently with the established ingestion and selection contract.
- No Jalali date is silently converted to Gregorian or written into a Gregorian database field.

### 3. Add focused regression tests

Add tests for at least:

- A requested Jalali date with an impossible month/day combination.
- An impossible Jalali date already stored as a market observation; prove it cannot be selected.
- A valid month-end date.
- A valid leap-year boundary case, using the chosen library's authoritative behavior.
- No regression to existing ordering, company isolation, price fallback, duplicate detection, or provenance.

Tests must exercise the actual selector and its date-validation boundary, not only a standalone library call.

## Scope and completion standard

Make the smallest complete code change that safely resolves this date-validation defect. Do not stop at a report describing the missing dependency if a suitable implementation can be made within the project conventions.

If dependency governance or another concrete constraint prevents a safe implementation, do not invent a calendar algorithm. State the exact blocker and the minimum decision needed.

Do not attempt to connect the main application flow to Stage 9 in this prompt; that is the next separate task.

## Final response

Report:

1. Exact files changed and the purpose of each.
2. The validator selected and whether its dependency is declared.
3. Which requested and stored date cases are now rejected or accepted.
4. The new regression tests added.
5. The exact test commands the user should run.
6. Explicitly confirm that you did not run tests or CI.
7. Any remaining date-validation limitations.

Do not claim the Stage 7 → Stage 9 production path is connected, and do not declare Stage 7 frozen.