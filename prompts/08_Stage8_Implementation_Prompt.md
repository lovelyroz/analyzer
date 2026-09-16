# Stage 8 — Market Engine

## Execution Prompt

Implement or audit Stage 8 strictly against `08_Stage8_Market_Engine.md`.

Stage 8 is a **Market State Engine**, not a Market Score Engine. It describes price/market context and must never output an investment decision or technical Buy/Sell signal.

### Inputs
Primary input is Stage 1 `MarketDaily`, with valid benchmark data and relevant corporate-action information when required. All calculations are Point-in-Time.

Prefer `adjusted_close` for performance/return, momentum, long-term moving-average context, and drawdown where corporate actions could otherwise create artificial moves. Preserve raw `close` separately for quoted price context.

### Required market state
Calculate:
- returns: 1D, 5D, 20D, 60D, 120D, 252D with trading-day handling
- price position in 20D/60D/252D ranges
- distance from 52-week high
- MA20/MA60/MA120 and price-vs-MA context
- trend states: `STRONG_UPTREND`, `UPTREND`, `NEUTRAL`, `DOWNTREND`, `STRONG_DOWNTREND`
- momentum over 20D/60D/120D: strong positive/positive/neutral/negative/strong negative
- momentum acceleration/deceleration context
- annualized volatility over representative 20D/60D windows
- current/max drawdown over required windows
- liquidity states: `HIGH`, `NORMAL`, `LOW`, `VERY_LOW`
- abnormal-volume context and price/volume confirmation
- relative strength versus a real industry or market benchmark
- market regime/context and market alerts

### Drawdown contract
Use the corrected V1.1 state set:
- `NEAR_PEAK`
- `RECOVERING`
- `DEEP_DRAWDOWN`
- `NEW_LOW`
- `STABLE_DRAWDOWN`

`RECOVERING` requires the configured material rebound from the recent low (V1 implementation uses a 5% recovery threshold). Moderate drawdown without recovery/deep/new-low evidence is `STABLE_DRAWDOWN`.

`market_contract_version` must be `MARKET_CONTRACT_V1.1`; `model_version` remains `STAGE8_V1` unless the model itself is intentionally versioned.

### Safety boundaries
- No Market Score.
- No technical Buy/Sell/Hold signal.
- No modification of Fundamental Score, Forecast EPS, Target P/E, or valuation.
- High volatility, abnormal volume, low liquidity, or weak market state are context/risk, not automatic decisions.
- Trend, momentum, moving averages, and volume evidence must not be treated as independent votes when derived from the same price series.
- Missing benchmark means relative strength is `INSUFFICIENT_DATA`; never invent a benchmark.

### Verification
Test trading-day horizons, adjusted-close behavior, flat ranges, missing data, conflicting horizons, volatility, drawdown classification including `STABLE_DRAWDOWN`, recovery threshold, liquidity, abnormal volume, benchmark absence, PIT filtering, and forbidden Market Score/decision outputs. Run the full suite, audit the contract, and verify actual CI evidence.