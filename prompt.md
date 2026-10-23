# P52 — Freeze the Stage 7 Alert Vocabulary in the Specification (D8, Documentation-Only)

You are working in the local project folder `analyzer`, a financial-data application requiring financial correctness, auditability, deterministic behavior, and preservation of existing contracts.

## Objective

Complete the documentation-only D8 decision using the following approved direction for this task:

1. **Adopt the engine's existing emitted alert vocabulary in the Stage 7 specification.** Do not rename emitted tokens in production code.
2. Preserve directional distinctions such as above-target versus below-target, above-historical versus below-historical, and above-industry versus below-industry.
3. Document `alerts` and `valuation_risk_flags` as distinct output channels. A flag-only item must not be described as an alert with severity unless the implementation actually emits it through `alerts`.
4. Explicitly document deferred tokens whose triggers are not defined or implemented. Do not invent triggers, thresholds, severities, formulas, or financial policy.
5. Keep Stage 7 OPEN. This task does not establish Point-in-Time completeness or production integration.

## Required targeted reading

Read:

- `stepsForStage7.md` — D1–D9 and the execution order.
- `07_Stage7_Valuation.md` — especially section 49 and nearby alert/flag contract sections.
- `src/valuation/engine.py` — `_alerts` and the code that emits flags.
- `src/valuation/schema.py` — the actual `ValuationResult` fields.
- `src/tests/test_stage7_valuation.py` — existing contract assertions.
- The relevant D8 decision material in `temp_report2.md`.

Do not perform a repository-wide scan.

## Required implementation

Make the smallest documentation-only changes to `07_Stage7_Valuation.md` that:

- Replace any claim that the specification's three generic benchmark-divergence names are emitted literally, where that conflicts with the actual directional tokens.
- List the actual emitted directional tokens and explain their meaning without changing their trigger logic.
- Clearly distinguish severity-prefixed `alerts` from `valuation_risk_flags`.
- Record that `INSUFFICIENT_PEER_DATA`, `NEGATIVE_EPS`, and `SIGN_CHANGE` are currently flags, not severity-prefixed alerts, unless the source code proves otherwise.
- Record `ASSESSMENT_FLIP_RISK`, `HIGH_MULTIPLE_DEPENDENCE`, `HIGH_EPS_DEPENDENCE`, `MARGIN_ASSUMPTION_RISK`, and `HIGH_IMPACT_HIGH_UNCERTAINTY` as deferred under D1–D5, consistent with the locked V1 policy.
- Record `POOR_DATA_QUALITY` and `POINT_IN_TIME_WARNING` as not implemented because valid trigger criteria are not established. Do not imply that their absence proves data quality or PIT correctness.
- Preserve any unrelated specification content.

Do not change production code, schemas, parameters, database models, or tests. Do not introduce compatibility aliases or new output tokens.

## Validation and restrictions

- Do not run tests or CI; the user will run any necessary tests.
- No GitHub, GitHub CLI/API, remote operations, push, pull, commit, or branch changes.
- Do not edit `reply.md`, `temp_report.md`, `temp_report2.md`, `ClaudeReports/`, `stepsForStage7.md`, or `stage_7_prompts.md`.
- Do not change `engine.py` or redesign its responsibilities.
- Do not claim that documentation changes prove runtime correctness, production integration, or PIT compliance.
- If a requested statement conflicts with actual source code, preserve source behavior and explicitly report the conflict rather than fabricating a match.

## Completion report

Report:

1. The exact sections of `07_Stage7_Valuation.md` changed.
2. A before/after summary of the D8 vocabulary and channel distinctions.
3. Confirmation that production code, schemas, parameters, and tests were not changed.
4. Confirmation that tests were not run.
5. Any remaining D8 ambiguity that cannot be resolved by documenting the actual behavior.
6. Confirmation that Stage 7 remains OPEN.

Finish the bounded documentation task before reporting.