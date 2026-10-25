# P55 — Stage 7 D1–D6 V1 Policy Conformance and Safe Remediation

## Objective

Continue Stage 7 remediation in the local working folder `analyzer`.

The authoritative plan is `stepsForStage7.md`. Stage 7 remains OPEN and must not be frozen.

P53/P53.1 addressed part of D7, and P54 implemented cutoff-governed historical parameter selection for D9. Do not redo those tasks. The next planned task is to verify D1–D6 against the actual current implementation and make every independently justified, contract-supported correction.

## Required files — inspect these exact files

1. `stepsForStage7.md`
2. `07_Stage7_Valuation.md`
3. `src/valuation/engine.py`
4. `src/valuation/parameters.py`
5. `src/valuation/schema.py`
6. `src/tests/test_stage7_valuation.py`
7. `src/decision/engine.py`
8. `src/tests/test_stage9_decision.py`

Use only these files unless a specific dependency or consumer cannot be verified without one additional file. If another file is essential, identify its exact path and explain why before expanding scope. Do not scan the whole repository.

## Mandatory V1 policies

Treat the following as binding constraints:

- **D1 — `ASSESSMENT_FLIP_RISK`:** Do not emit a new alert until a valid, documented trigger for changes in valuation assumptions and assessment has been established.
- **D2 — `HIGH_MULTIPLE_DEPENDENCE`:** Do not treat the current undefined or invalid dependence metric as a validated risk measure. Do not emit this alert without a defensible, specified method.
- **D3 — `HIGH_EPS_DEPENDENCE`:** Preserve Stage 5 EPS as the authoritative forecast. Do not recalculate EPS or emit a new dependence alert without a valid criterion.
- **D4 — `MARGIN_ASSUMPTION_RISK`:** Do not emit a new alert without valid, dated inputs and a documented criterion.
- **D5 — `HIGH_IMPACT_HIGH_UNCERTAINTY`:** Preserve the existing `review_priority` contract. Do not turn it into a new alert without independently valid criteria.
- **D6 — Industry model:** Preserve the current V1 valuation-driver contract based on EPS and target P/E. Do not invent sector mappings, industry-specific formulas, or unavailable source fields.

## Work to perform

1. Inspect the current implementation of alert generation, driver ranking, risk metrics, `review_priority`, and relevant metadata.
2. Compare actual emitted alerts and driver outputs with the V1 policies above and the locked specification.
3. Review existing tests, including tests documenting intentionally deferred behaviors. Do not assume an old test requirement overrides the current V1 policy.
4. Check the Stage 9 consumer before changing any alert names, output shapes, or metadata contracts.
5. Identify each discrepancy and classify it as:
   - a concrete implementation defect with an existing authoritative rule;
   - behavior already compliant with V1;
   - an unresolved policy requiring a valid financial definition or owner decision.
6. Implement every independent correction that is justified by the existing specification and code contracts. Add or adjust focused tests only when needed to prove that behavior.
7. Preserve existing financial formulas, thresholds, EPS sourcing, output contracts, deterministic behavior, and missing-data semantics unless an explicit existing contract requires a correction.
8. Do not weaken or delete tests merely to make the suite pass. Do not add a test that asserts an unsupported financial rule.
9. Do not redesign or broadly refactor `engine.py`; that review remains the final Stage 7 task.

## Explicit exclusions

- Do not implement speculative alerts, financial thresholds, shock sizes, sector mappings, or formulas.
- Do not modify Stage 5, Stage 8, or Stage 9 production code unless a specific, demonstrable contract dependency makes a minimal change unavoidable. Explain such a dependency before changing another stage.
- Do not work on P54/D9 again unless you discover a concrete regression directly caused by P54; report it instead of expanding this task.
- Do not edit `reply.md`, `temp_report.md`, `temp_report2.md`, `stepsForStage7.md`, `stage_7_prompts.md`, or any report archive.
- Do not perform GitHub operations, use GitHub CLI/API, change remotes or branches, push, pull, or commit.
- Do not run pytest, CI, or other tests. The user will run the tests and provide the actual output.
- Do not claim tests passed.

## Required deliverable

Provide:

1. A concise D1–D6 compliance table showing the actual behavior, evidence from the named files, and disposition.
2. The exact source and test files changed, if any.
3. The specific changes made and why each is supported by V1.
4. The exact focused pytest command(s) for the user to run.
5. Any unresolved policy decisions and why the current evidence cannot safely resolve them.
6. A clear statement that tests were not run.

If the environment supports direct editing, apply the justified changes to the working files. If it does not, state that limitation clearly and provide the complete proposed content for each changed file; do not claim implementation occurred when it did not.

Do not write or append any report file. Stage 7 remains OPEN.