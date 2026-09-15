# Stage 8 — Market Engine | Contract Amendment V1.1

## Status

**APPROVED AMENDMENT — CONTRACT V1.1**

This amendment corrects a genuine classification gap discovered during the final Stage 8 implementation audit. It does not redesign the Market Engine.

## Reason for amendment

The original drawdown contract defined these context states:

- `NEAR_PEAK`
- `RECOVERING`
- `DEEP_DRAWDOWN`
- `NEW_LOW`

The implementation previously used `RECOVERING` as a fallback for a moderate drawdown that was neither near the peak, recovering from the recent low, deep, nor an extreme new low. That incorrectly implied recovery where the data did not establish recovery.

## Corrected state

Stage 8 V1.1 adds:

- `STABLE_DRAWDOWN`

Meaning:

> The stock is in a measurable drawdown, but the available price structure does not establish either a material recovery or a deep/new-low condition.

This is a **context state only**. It is not positive or negative investment guidance and does not create a market score or decision signal.

## Classification order

1. `NEAR_PEAK` when current drawdown is within the near-peak threshold.
2. `NEW_LOW` when drawdown is at or beyond the extreme threshold and the current price is the recent low.
3. `RECOVERING` when the current price has recovered by at least the configured recovery threshold from the recent low.
4. `DEEP_DRAWDOWN` when drawdown is at or beyond the deep threshold without recovery evidence.
5. `STABLE_DRAWDOWN` otherwise.

## Versioning

`market_contract_version` is now:

`MARKET_CONTRACT_V1.1`

`model_version` remains:

`STAGE8_V1`

The internal model was not redesigned; only the external drawdown-state contract was corrected to represent an existing analytical case honestly.

## Downstream rule

Stage 9 must treat `STABLE_DRAWDOWN` as contextual market information only. It must not interpret it as an automatic Buy, Sell, or Hold instruction.
