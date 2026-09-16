# Stage 8 — Market Engine Contract Amendment V1.1

## Status

**APPROVED — V1.1**

This amendment records the corrected drawdown-state contract discovered during implementation audit. It does not add a new analytical engine or change Stage 8 ownership.

## Correction

The Stage 8 locked contract previously listed four drawdown states but did not explicitly represent a measurable moderate drawdown that was neither near-peak, recovering, deep, nor a new low.

The corrected state set is:

- `NEAR_PEAK`
- `RECOVERING`
- `DEEP_DRAWDOWN`
- `NEW_LOW`
- `STABLE_DRAWDOWN`

## Classification

1. `NEAR_PEAK` when current drawdown is within the configured near-peak threshold.
2. `NEW_LOW` when the extreme drawdown threshold is reached and current price is the relevant recent low.
3. `RECOVERING` only when the configured material rebound from the recent low is established.
4. `DEEP_DRAWDOWN` when drawdown is deep without recovery evidence.
5. `STABLE_DRAWDOWN` otherwise.

The V1 implementation uses a 5% material-rebound threshold for recovery.

## Semantics

`STABLE_DRAWDOWN` is a context state only. It does not imply positive or negative investment guidance and does not create a Market Score or Decision signal.

## Versioning

`market_contract_version = MARKET_CONTRACT_V1.1`

`model_version = STAGE8_V1` remains unchanged because the correction is to the external state contract, not the analytical model family.

## Downstream

Stage 9 must consume `STABLE_DRAWDOWN` only as contextual market evidence. It must not interpret it as an automatic Buy, Sell, or Hold instruction.
