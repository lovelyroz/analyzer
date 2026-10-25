# P66 — Stage 7 Consolidated Engineering Batch: Architecture Contracts, Specification Reconciliation, and D1–D6

## 1. Role and Project Context

Work in the local project folder:

`analyzer`

This is a financial-data application. Financial correctness, auditability, point-in-time correctness, deterministic behavior, and preservation of financial invariants are mandatory.

Use `stepsForStage7.md` as the authoritative Stage 7 roadmap and `07_Stage7_Valuation.md` as the valuation specification. Review the available findings in `reply.md`, including P63, P64, and P65 where present.

Also preserve these established constraints from prior Stage 7 planning:
- The production path across Stages 3, 5, 7, 8, and 9 has not yet been fully proven.
- Do not change the existing scenario-dispersion thresholds or comparison semantics without explicit specification approval.
- Do not invent industry mappings, sector-specific formulas, financial assumptions, parameter values, or historical effective dates.
- Keep D9 fail-closed where historical parameter selection cannot be established, and report the limitation truthfully.

Do not assume that any report ID exists in `reply.md` unless you verify it. If a referenced finding is unavailable, inspect the authoritative roadmap and relevant source files instead of inventing its contents.

## 2. Objectives for This Batch

Advance the following roadmap areas together:

- Stage 7 roadmap Phase 2: architecture gaps and interface contracts.
- Stage 7 roadmap Phase 3: specification, warning, implementation, and test discrepancies.
- Stage 7 roadmap Phase 6: policies D1–D6.

Do not begin the final `engine.py` redesign. Do not attempt to force a complete production integration when real sources, contracts, or consumers have not been established.

## 3. Objective A — Resolve the Architecture Contract Questions

Start from the evidence already recorded in P48. Verify only the specific interfaces and callers needed to establish the current contract. Avoid repository-wide exploration.

Trace and document the relevant existing interfaces for:

1. Stage 3 scoring outputs and their real producers/callers.
2. Stage 5 forecast generation, persistence, and returned results.
3. Stage 7 valuation inputs, market-price selection, date handling, and parameter selection.
4. Stage 8 market analysis inputs and `MarketSignalResult` production.
5. Stage 9 decision inputs, orchestration, and returned results.
6. Database `Session` ownership and the propagation of analysis dates/cutoffs.
7. The destination or consumer of the final decision result.

For each interface, establish:

- Actual function/class and file path.
- Required inputs and their proven sources.
- Output type and its actual consumer, if one exists.
- Date and session responsibilities.
- Whether the connection is proven, partial, or missing.

Distinguish an implemented service from a real application execution path. A unit test using mocks does not establish production integration.

### Required outcome

Produce a concrete interface/gap matrix that identifies the smallest viable next integration step using existing architecture.

Where a missing source, entry point, date contract, or result consumer prevents a valid connection, document that exact gap. Do not invent data, use synthetic financial inputs to disguise missing production functionality, or create a redundant orchestrator merely to make the architecture appear connected.

If the existing interfaces already support a safe, clearly bounded connection that does not depend on unresolved policy, implement it only if it belongs within this batch and can be validated without fabricating missing inputs. Otherwise, provide a precise implementation-ready contract.

## 4. Objective B — Reconcile Specification, Implementation, and Tests

Use the discrepancies and warnings already identified in `reply.md` as leads. Verify them against the actual code and authoritative specifications before deciding whether anything is wrong.

Prioritize:

1. Warning and alert names, semantics, and output contracts under D8.
2. Differences between documented warning behavior and warnings actually emitted.
3. The reported missing or incomplete sector-driver decomposition and industry-specific behavior.
4. Reported risk-warning discrepancies and the separation of risk, confidence, valuation status, and review priority.
5. Tests that may encode behavior inconsistent with the locked specification.
6. Contradictions between status summaries in `07_Stage7_Valuation.md` and factual implementation annotations elsewhere in that file.

For every discrepancy, classify it as one of:

- Confirmed implementation defect against an explicit requirement.
- Test/specification inconsistency.
- Unresolved or ambiguous specification.
- Documented limitation or deferred capability.
- Previously reported issue that cannot be reproduced from the available evidence.

### Implementation requirement

Fix confirmed, specification-backed defects that can safely be corrected within the existing architecture.

Update or add focused tests for the changed behavior, but do not execute them.

Do not change a test merely to make it pass if doing so would conceal a real defect. If a test conflicts with an explicit specification, correct the test only when the specification clearly determines the intended behavior.

If the financial meaning is ambiguous, do not guess. Record the exact decision needed and continue with independent work.

## 5. Objective C — Verify and Advance Policies D1–D6

For each policy, compare the authoritative specification with implementation and test coverage.

- **D1:** Do not produce a status-change alert without a valid criterion.
- **D2:** Do not use an invalid P/E-dependency indicator.
- **D3:** Preserve Stage 5 EPS; do not recalculate it or emit unapproved warnings.
- **D4:** Do not produce a margin-risk alert without valid inputs.
- **D5:** Keep `review_priority` separate from risk alerts.
- **D6:** Preserve the current valuation contract and do not invent industry mappings or sector formulas.

For each policy:

1. Identify the actual relevant implementation and tests.
2. Verify whether the policy is correctly enforced, partially enforced, violated, or not implementable with current inputs.
3. Check relevant edge cases and invalid/missing-input behavior.
4. Add or revise focused tests where necessary.
5. Fix clear violations where the required behavior is explicit.
6. Record any remaining limitation or policy decision precisely.

Do not treat the existence of a test as proof that a policy is fully enforced. Inspect what the test actually asserts.

Do not invent industry classifications, sector formulas, financial thresholds, or new data sources.

## 6. Consolidated Implementation Rules

This batch should make real progress across all three objectives without expanding into an uncontrolled refactor.

- Inspect only the files needed to verify the reported findings and implement the relevant fixes.
- Prefer small, cohesive changes over a broad redesign.
- Preserve public interfaces unless a change is explicitly required and all known consumers can be updated safely.
- Maintain deterministic behavior and existing financial invariants.
- Add focused tests for implemented changes.
- Keep unrelated work moving even when one issue is blocked by missing evidence or an owner decision.
- Do not modify `src/valuation/engine.py` as part of a redesign or large refactor. Its redesign remains the final Stage 7 task.
- Do not introduce a new application entry point, orchestration layer, persistence model, or schema without first establishing the actual gap and a compatible contract.
- Do not change P61 scenario-dispersion thresholds or their semantics without explicit specification support.
- Do not invent or approve parameter values, effective dates, or historical validity to resolve D9. Preserve the current fail-closed historical parameter selection and truthful legacy metadata.
- Do not claim that point-in-time correctness or end-to-end production integration is achieved unless the relevant evidence actually proves it.

## 7. Tests and Validation

You may inspect and write tests, but **do not run any tests or application execution commands**. The project owner will run tests locally.

For every code change:

- Identify the behavior being protected.
- Identify the relevant test file and test cases.
- State the exact command the owner should run.
- Explain what a failure would mean, if it is not self-evident.

At minimum, provide targeted commands for affected tests. If changes span multiple test areas, provide a combined command and, where useful, a separate targeted command.

Do not report tests as passed, verified at runtime, or executed. Clearly label all unexecuted tests.

## 8. Guardrails

- Work only in the local `analyzer` folder.
- Do not use GitHub, GitHub CLI/API, or remote operations.
- Do not commit, push, pull, switch branches, or alter remote configuration.
- Do not run tests.
- Do not make unrelated changes.
- Do not modify `stepsForStage7.md`, `07_Stage7_Valuation.md`, `reply.md`, or other planning/report files just to record progress. Report findings in your final response for the owner to review.
- Do not perform the final `engine.py` redesign.
- Do not claim that the entire Stage 7 roadmap is complete after this batch.

## 9. Required Final Report

Return one consolidated report with the following sections:

### A. Work Completed
List actual code and test-file changes, grouped by objective. Include exact file paths and concise explanations.

### B. Architecture Contract and Remaining Gaps
Summarize proven interfaces, partial connections, missing sources/consumers, date/session ownership, and the smallest valid next integration step.

### C. Specification and Implementation Reconciliation
For each investigated discrepancy, state the evidence, classification, action taken, and remaining status.

### D. D1–D6 Status
Provide a compact matrix with policy, implementation status, evidence, changes made, and remaining limitations.

### E. Owner-Run Test Plan
Give exact PowerShell-compatible commands for the affected tests. Clearly state that none were executed during this task.

### F. Remaining Blockers and Next Roadmap Step
Separate:
- Items that can be implemented now.
- Items blocked by missing interfaces or data.
- Items requiring explicit financial/business approval.
- Work intentionally deferred to the final `engine.py` review.

### G. Execution Confirmation
State explicitly:
- Whether source code was changed.
- Whether tests were added or changed.
- Whether any tests or application commands were executed.
- Whether any Git or remote operations occurred.

The report must describe actual results, not intended work. If a task could not be completed, explain the exact reason and what evidence is missing.

**Acceptance criterion:** This batch must deliver verified progress on multiple roadmap objectives, not merely another audit. Implement all clear, safe, specification-backed fixes within scope, add appropriate tests without running them, and leave a precise, evidence-based path for the next batch.