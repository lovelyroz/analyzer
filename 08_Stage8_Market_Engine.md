# Stage 8 — Market Engine | Locked Specification

## 1. Status

This stage has completed:

* Design
* Review
* Stress Testing
* Audit

Final status:

**LOCKED**

Do not redesign this stage unless a genuine architectural contradiction with another locked stage is discovered.

Internal formulas, thresholds, windows, and calibration parameters may later be versioned without changing the Stage 8 contract, provided the external contract remains compatible.

If the contract itself must change, create a new explicit `market_contract_version` and migrate downstream dependencies deliberately.

---

# 2. Purpose

Stage 8 answers:

> «بازار در حال حاضر با خود سهم چه رفتاری دارد و وضعیت روند قیمت، مومنتوم، ریسک، نقدشوندگی و قدرت نسبی سهم چگونه است؟»

The Market Engine analyzes market behavior only.

It must NOT:

* change Fundamental Score,
* alter Forecast EPS,
* modify Target P/E,
* create a new fundamental judgment,
* generate a Buy/Sell/Hold decision,
* replace valuation analysis,
* merge market and fundamental logic prematurely.

Final investment decisions belong exclusively to:

**Stage 9 — Decision Engine**

---

# 3. Position in the Architecture

```text
                 MarketDaily
                     │
                     ▼
              STAGE 8
            MARKET ENGINE
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
      Trend       Momentum       Risk
        │            │            │
        ├────────────┼────────────┤
        ▼            ▼            ▼
 Relative Strength Liquidity   Alerts
                     │
                     ▼
               Market State
                     │
                     ▼
                 STAGE 9
             Decision Engine
```

Stage 8 runs independently from the Fundamental Engine.

Fundamental and Market evidence remain separate until Stage 9.

---

# 4. Core Architectural Principle

Stage 8 is:

**a State Engine, not a Score Engine.**

V1 must NOT create:

```text
Market Score = 0–100
```

There is intentionally no single aggregate Market Score in V1.

The engine should instead return interpretable market states such as:

* Trend
* Momentum
* Volatility
* Drawdown
* Relative Strength
* Liquidity
* Market Alerts

This avoids hiding materially different market conditions inside one number and reduces double counting in Stage 9.

---

# 5. Primary Input

The primary input comes from Stage 1:

`MarketDaily`

Required fields include:

```text
company_id
date
open
high
low
close
adjusted_close
volume
value
trade_count
source
```

Where applicable, the engine may also use:

* CorporateAction
* ShareCountHistory
* market benchmark series
* industry benchmark series

provided they satisfy Point-in-Time rules.

---

# 6. Close vs Adjusted Close

Raw `close` and `adjusted_close` must remain separate.

Use:

### Adjusted Close

Prefer for:

* historical return calculations,
* momentum,
* long-term performance,
* moving averages used for performance context,
* drawdown where corporate actions could otherwise create false moves.

### Raw Close

Retain for:

* actual observed market price,
* current trading-price structure,
* other contexts where the raw quoted price is required.

Corporate actions must not generate artificial returns, artificial trend breaks, or false drawdowns.

---

# 7. Point-in-Time Rule

Stage 8 is strictly Point-in-Time.

For a Market State calculated at date `T`:

> only market data available on or before date `T` may be used.

No future price, future benchmark value, future adjusted history, or future corporate-action information may leak backward into historical analysis.

The implementation must be suitable for legitimate historical backtesting.

---

# 8. Stage 8 Structure

Stage 8 has four analytical layers:

```text
1. Price Structure
2. Trend & Momentum
3. Risk & Liquidity
4. Relative Strength & Alerts
```

These layers are related but must not be treated as independent votes when they are derived from the same underlying price behavior.

---

# 9. Layer 1 — Price Structure

## 9.1 Return Horizons

Calculate representative cumulative returns for:

```text
1D
5D
20D
60D
120D
252D
```

Conceptually:

```text
Return_horizon
=
Current Adjusted Close
/
Historical Adjusted Close
- 1
```

Exact trading-day handling must account for missing trading days and suspension periods.

Do not assume every calendar day is a valid trading observation.

---

# 10. Price Position Within Range

For selected windows such as:

```text
20D
60D
252D
```

calculate:

```text
Price Position
=
(Current Price - Period Low)
/
(Period High - Period Low)
```

Interpretation:

* near 1 → near top of historical range,
* near 0 → near bottom of historical range.

If:

```text
Period High = Period Low
```

return an appropriate undefined/insufficient status rather than divide by zero.

---

# 11. Distance From 52-Week High

Calculate:

```text
Distance From 52W High
=
Current Price
/
52W High
- 1
```

This is a context metric, not an automatic Buy/Sell signal.

A stock trading far below its historical high is not automatically cheap.

---

# 12. Moving Averages

V1 uses only a compact representative set:

```text
MA20
MA60
MA120
```

The exact window lengths may later be Model Version Parameters.

Calculate:

```text
Price vs MA
=
Current Price
/
Moving Average
- 1
```

Examples:

```text
price_vs_ma20
price_vs_ma60
price_vs_ma120
```

Moving averages are descriptive evidence.

They must not each be treated as independent votes in an aggregate score.

---

# 13. Technical Indicators Excluded From Core V1

Do not build a large technical-indicator library.

The following are NOT Core V1:

* RSI
* MACD
* Stochastic
* CCI
* Williams %R
* Bollinger Bands
* Ichimoku
* Fibonacci
* dozens of moving averages
* indicator voting systems
* technical indicator optimization

They may be reconsidered only in a later explicitly versioned extension if they demonstrate clear incremental decision value.

---

# 14. Layer 2 — Trend

Trend is evaluated across multiple horizons rather than a single time window.

Core horizons:

```text
Short   ≈ 20 trading days
Medium  ≈ 60 trading days
Long    ≈ 120 / 252 trading days
```

Exact periods are Model Version Parameters.

---

# 15. Trend Inputs

Trend may consider:

* cumulative return,
* price relative to moving averages,
* direction of representative moving averages,
* consistency across horizons,
* price structure,
* major recent reversal.

These must be integrated without double counting highly correlated evidence.

---

# 16. Trend States

Final Market Trend State:

```text
STRONG_UPTREND
UPTREND
NEUTRAL
DOWNTREND
STRONG_DOWNTREND
```

Short-, medium-, and long-horizon trend states may also be stored separately.

---

# 17. Trend Conflict Rule

Conflicting horizons must not create an exaggerated trend classification.

Example:

```text
20D Return   = +10%
60D Return   = +2%
120D Return  = -15%
```

This must NOT automatically become:

```text
STRONG_UPTREND
```

A result such as:

```text
NEUTRAL
```

or a transition/recovery context is more appropriate depending on the model version.

The engine must explicitly tolerate short-term reversals inside long-term trends.

---

# 18. Strong Trend Requirement

A Strong Trend should require broad directional agreement.

For example, Strong Uptrend should normally require:

* positive directional evidence across several horizons,
* supportive price structure,
* reasonable consistency,
* no major contradictory long-horizon evidence.

Likewise for Strong Downtrend.

Exact thresholds are Model Version Parameters and must be backtestable.

---

# 19. Momentum

Momentum answers:

> How strong is recent directional price movement?

Core momentum horizons:

```text
20D
60D
120D
```

Representative inputs:

```text
20D Return
60D Return
120D Return
```

---

# 20. Momentum States

```text
STRONG_POSITIVE
POSITIVE
NEUTRAL
NEGATIVE
STRONG_NEGATIVE
```

Momentum must remain distinct from Trend.

Trend describes broader directional structure.

Momentum describes recent directional force and change.

---

# 21. Momentum Acceleration

Optional but supported state:

```text
ACCELERATING
STABLE
DECELERATING
```

Examples:

```text
20D Return = +15%
60D Return = +10%
```

may indicate:

```text
POSITIVE
ACCELERATING
```

Whereas:

```text
60D Return = +20%
20D Return = +2%
```

may indicate:

```text
POSITIVE
DECELERATING
```

The engine must distinguish positive momentum from improving momentum.

---

# 22. No Double Counting Between Trend and Momentum

Trend and Momentum are separate descriptions of related market behavior.

Stage 9 must not treat them as two completely independent pieces of evidence when they originate from the same price series.

Stage 8 should expose both because they answer different questions, but downstream weighting must respect their correlation.

---

# 23. Layer 3 — Volatility

Calculate daily return as:

```text
Daily Return_t
=
Adjusted Close_t
/
Adjusted Close_(t-1)
- 1
```

Core volatility windows:

```text
20D
60D
```

---

# 24. Volatility Calculation

Basic realized volatility:

```text
Volatility
=
Standard Deviation of Daily Returns
```

Annualized form may also be calculated:

```text
Annualized Volatility
=
Std(Daily Returns) × sqrt(252)
```

The implementation must state clearly whether reported volatility is daily or annualized.

---

# 25. Volatility Context

Where enough historical observations exist, interpret volatility relative to:

1. the company's own history,
2. optionally its industry.

Preferred states:

```text
LOW
NORMAL
HIGH
EXTREME
```

A fixed universal volatility threshold across all industries should be avoided when a historical relative benchmark is available.

---

# 26. Volatility Is Risk, Not Direction

Critical rule:

```text
High Volatility ≠ Sell
Low Volatility ≠ Buy
```

Volatility is a risk/context variable only.

A high-growth or strongly trending stock may have high volatility without being fundamentally negative.

---

# 27. Drawdown

Drawdown measures decline from a previous peak.

Current Drawdown:

```text
Current Drawdown
=
Current Price
/
Running Peak
- 1
```

---

# 28. Maximum Drawdown

Calculate representative maximum drawdown over:

```text
20D
60D
120D
252D
```

At minimum the output contract should include:

```text
max_drawdown_20d
max_drawdown_60d
max_drawdown_252d
```

Additional horizons may be internal Model Parameters.

---

# 29. Drawdown Context

Possible context states:

```text
NEAR_PEAK
RECOVERING
DEEP_DRAWDOWN
NEW_LOW
```

Drawdown should preferably be interpreted relative to the stock's own historical behavior.

A -20% drawdown may be normal for one stock and extreme for another.

---

# 30. Recovery Detection

The engine must distinguish:

```text
falling deeper into drawdown
```

from:

```text
recovering from a previous drawdown
```

A stock that remains below its historical peak but has recovered substantially from the recent low should not automatically be classified as still deteriorating.

---

# 31. Liquidity

Liquidity measures practical ease of entering or exiting a position.

Core inputs:

```text
Average Trading Value 20D
Average Volume 20D
Trading Value Stability
```

Possible future implementation may also use:

* percentage of active trading days,
* abnormal inactivity,
* trading concentration,

provided data exists reliably.

---

# 32. Liquidity States

```text
HIGH
NORMAL
LOW
VERY_LOW
```

Liquidity must not directly generate a Buy/Sell signal.

It is an execution/risk characteristic.

Example:

```text
Attractive stock + VERY_LOW liquidity
```

remains possible.

Stage 9 may treat that as a position-management risk.

---

# 33. Abnormal Volume

Calculate:

```text
Volume Ratio
=
Current Volume
/
Average Volume 20D
```

If materially above historical norms:

```text
ABNORMAL_VOLUME = TRUE
```

Exact thresholds are Model Version Parameters.

---

# 34. Abnormal Volume Is Direction-Neutral

Critical rule:

```text
Abnormal Volume ≠ Buy
Abnormal Volume ≠ Sell
```

Abnormal volume only indicates unusual market activity.

Its meaning depends on accompanying price behavior.

---

# 35. Price + Volume Confirmation

Contextual patterns may include:

```text
Price ↑ + Volume ↑
→ PRICE_VOLUME_CONFIRMATION
```

and:

```text
Price ↑ + Volume ↓
→ WEAK_PRICE_VOLUME_CONFIRMATION
```

Likewise downward moves may be assessed for volume confirmation.

These are contextual descriptors.

They must not be used as independent technical votes.

---

# 36. Layer 4 — Relative Strength

Relative Strength compares stock performance with an appropriate benchmark.

Preferred benchmarks:

```text
1. Industry
2. Broad Market
```

when valid benchmark data is available.

---

# 37. Relative Return

Conceptually:

```text
Relative Return
=
Stock Return
-
Benchmark Return
```

The same measurement horizon must be used for stock and benchmark.

Examples:

```text
Stock +15%
Industry +5%
```

→ strong relative performance.

```text
Stock +5%
Industry +15%
```

→ weak relative performance.

---

# 38. Absolute vs Relative Performance

Absolute return and Relative Strength must remain separate.

Example:

```text
Stock Return  = -5%
Market Return = -15%
```

The stock has:

```text
Negative Absolute Return
```

but may simultaneously have:

```text
Strong Relative Strength
```

This distinction must be preserved.

---

# 39. Relative Strength States

```text
STRONG
ABOVE_AVERAGE
NEUTRAL
BELOW_AVERAGE
WEAK
```

Market and Industry Relative Strength may be stored independently.

A combined Relative Strength State may be produced only when the aggregation method is explicit and versioned.

---

# 40. Missing Benchmark

If market or industry benchmark data is unavailable or invalid:

```text
relative_strength_* = INSUFFICIENT_DATA
```

Do not create synthetic benchmark values.

Do not replace the missing industry benchmark with an unrelated index silently.

---

# 41. Market Regime

The engine may classify the broad market environment when benchmark data is available.

Suggested states:

```text
MARKET_UP
MARKET_NEUTRAL
MARKET_DOWN
HIGH_VOLATILITY
```

Market Regime is context only.

It must not directly change:

* Fundamental Score
* Forecast EPS
* Target P/E

unless another locked stage explicitly defines such a relationship.

---

# 42. Market Alerts

Stage 8 must provide a compact alert layer.

Alert severity:

```text
INFO
WATCH
WARNING
CRITICAL
```

Possible alert categories include:

```text
STRONG_DOWNTREND
HIGH_VOLATILITY
EXTREME_VOLATILITY
DEEP_DRAWDOWN
WEAK_RELATIVE_STRENGTH
LOW_LIQUIDITY
VERY_LOW_LIQUIDITY
ABNORMAL_VOLUME
PRICE_VOLUME_DIVERGENCE
EXTREME_PRICE_MOVE
TRADING_GAP
DATA_QUALITY_WARNING
```

---

# 43. Alert Philosophy

Alerts must tell the system/user:

> What deserves attention?

They must NOT directly say:

```text
BUY
SELL
```

Examples:

```text
WARNING:
High Volatility
```

or:

```text
WARNING:
Deep Drawdown with Weak Relative Strength
```

are valid.

But:

```text
SELL because volatility is high
```

is not allowed in Stage 8.

---

# 44. Suspension and Trading Gaps

Suspended trading, illiquidity, or long gaps between trading observations must be identifiable where data allows.

The engine must not interpret a multi-day suspension as normal zero-return observations.

Missing trading dates must not be automatically filled with fabricated market prices.

Possible context flag:

```text
TRADING_GAP
```

---

# 45. Missing Data Rule

If insufficient data exists for a requested calculation:

```text
INSUFFICIENT_DATA
```

must be returned.

Examples:

* fewer than required observations for MA120,
* no valid benchmark,
* no volume history,
* insufficient history for 252D return.

Never invent, extrapolate, or silently substitute data.

---

# 46. Data Quality

Market analysis should expose data quality.

Possible states may align with Stage 1 conventions such as:

```text
VALID
MISSING
ESTIMATED
SUSPICIOUS
```

Where useful, more specific Stage 8 flags may be attached, such as:

```text
TRADING_GAP
CORPORATE_ACTION_ADJUSTMENT
INSUFFICIENT_HISTORY
BENCHMARK_MISSING
```

Suspicious data must not silently flow into normal market-state calculations.

---

# 47. Corporate Actions

Corporate actions such as:

* stock splits,
* capital increases,
* rights-related adjustments,
* other price adjustments

must not generate false:

* returns,
* momentum,
* moving-average breaks,
* drawdowns,
* volatility spikes.

Adjusted Close should be preferred for historical performance analytics.

Raw Close remains stored separately.

---

# 48. Strong Market Does Not Override Weak Fundamentals

Example:

```text
Fundamental = WEAK
Forecast = DETERIORATING
Valuation = EXPENSIVE
Market = STRONG_UPTREND
```

Stage 8 must simply report:

```text
Market = STRONG_UPTREND
```

It must not convert the company into a fundamental Buy.

Stage 9 is responsible for resolving the conflict.

---

# 49. Weak Market Does Not Override Strong Fundamentals

Example:

```text
Fundamental = STRONG
Forecast = POSITIVE
Valuation = ATTRACTIVE
Market = STRONG_DOWNTREND
```

Stage 8 must preserve:

```text
STRONG_DOWNTREND
```

without altering the fundamental or valuation outputs.

Stage 9 may later classify this as:

```text
Fundamental Opportunity + Market Risk
```

but that is outside Stage 8.

---

# 50. No Hidden Market Influence

Market variables must NOT secretly enter:

* Stage 3 Fundamental Score
* Stage 4 Fundamental Trend
* Stage 5 Forecast
* Stage 6 Forecast Reliability
* Stage 7 Target P/E

unless an explicit upstream contract formally allows the input.

In V1, Stage 8 remains structurally separate.

---

# 51. No Market Score

Explicit non-negotiable V1 rule:

```text
NO MARKET SCORE 0–100
```

Rationale:

A single score would mix:

* trend,
* momentum,
* volatility,
* drawdown,
* liquidity,
* relative strength,

which represent different dimensions and may have conflicting meanings.

Example:

```text
Strong Trend
High Volatility
Low Liquidity
Strong Relative Strength
```

cannot be represented faithfully by one arbitrary number without losing information.

Therefore Stage 8 returns state variables, not one score.

---

# 52. Model Parameters

The following should remain configurable Model Version Parameters rather than permanent architectural constants:

* Trend windows
* Moving-average windows
* Momentum windows
* Volatility windows
* Relative-strength horizons
* Abnormal-volume thresholds
* Trend classification thresholds
* Volatility classification thresholds
* Drawdown thresholds
* Liquidity thresholds
* Alert thresholds
* minimum valid observation counts

Parameter changes create a new model version where necessary.

---

# 53. Auditability

Every output must be traceable to:

```text
Market Output
    ↓
Market Model Version
    ↓
Input Date Range
    ↓
MarketDaily Records
    ↓
Corporate Action Adjustment if applicable
    ↓
Source
```

For benchmark-relative metrics:

```text
Relative Strength
    ↓
Stock Price Series
    +
Benchmark Price Series
```

must both be traceable.

---

# 54. Market Model Versioning

Stage 8 calculations must store:

```text
market_model_version
```

This allows later changes such as:

* new Trend thresholds,
* different MA periods,
* revised volatility classification,
* improved liquidity logic,

without destroying historical reproducibility.

Old market states must remain reproducible under their original model version.

---

# 55. Contract Versioning

Stage 8 must also expose:

```text
market_contract_version
```

Difference:

```text
market_model_version
```

= internal logic / parameters.

```text
market_contract_version
```

= external interface expected by Stage 9.

Internal model changes that preserve the output contract do not require downstream architecture redesign.

A breaking output change requires an explicit new contract version.

---

# 56. Final Output Contract

Stage 8 should expose at minimum:

```text
company_id

market_date

return_1d
return_5d
return_20d
return_60d
return_120d
return_252d

price_position_20d
price_position_60d
price_position_252d

distance_from_52w_high

price_vs_ma20
price_vs_ma60
price_vs_ma120

market_trend_short
market_trend_medium
market_trend_long
market_trend_state

momentum_short
momentum_medium
momentum_long
momentum_state
momentum_acceleration_state

volatility_20d
volatility_60d
volatility_state

drawdown_current
max_drawdown_20d
max_drawdown_60d
max_drawdown_252d
drawdown_state

relative_strength_market
relative_strength_industry
relative_strength_state

avg_volume_20d
avg_trading_value_20d
liquidity_state

volume_ratio
abnormal_volume_flag
price_volume_state

market_regime

market_alerts

market_data_quality

market_timestamp
market_model_version
market_contract_version
```

Fields may internally be normalized or split into child tables where implementation efficiency requires it, but the logical contract must remain available to Stage 9.

---

# 57. Recommended Internal State Structure

Conceptually:

```text
Market State
│
├── Price Structure
│   ├── Returns
│   ├── Range Position
│   ├── Distance From High
│   └── Moving Average Context
│
├── Trend
│   ├── Short
│   ├── Medium
│   ├── Long
│   └── Final Trend State
│
├── Momentum
│   ├── Short
│   ├── Medium
│   ├── Long
│   └── Acceleration
│
├── Risk
│   ├── Volatility
│   └── Drawdown
│
├── Relative Performance
│   ├── Market Relative Strength
│   └── Industry Relative Strength
│
├── Liquidity
│   ├── Average Value
│   ├── Average Volume
│   └── Liquidity State
│
└── Alerts
```

---

# 58. V1 Scope Discipline

V1 should remain compact.

Do NOT add complexity merely because data exists.

V1 deliberately excludes:

```text
Large Technical Indicator Library
Indicator Voting Systems
Market Score
ML Price Prediction
Neural Networks
Pattern Recognition Engine
Candlestick Pattern Library
Wave Analysis
Fibonacci Systems
Automated Trading Rules
Intraday Strategy Engine
Order Book Analysis
Buy/Sell Signal Generator
```

These are outside the current architecture.

---

# 59. Stage 8 Does Not Predict Price

Stage 8 describes current and historical market state.

It does NOT answer:

```text
What will the stock price be next month?
```

Future financial forecasting belongs to Stage 5.

Valuation belongs to Stage 7.

Investment decision integration belongs to Stage 9.

If a future price-forecasting subsystem is ever added, it must be a separate formally designed module and must not silently enter Stage 8.

---

# 60. Stress Test — Strong Uptrend

Example:

```text
20D Return  = +12%
60D Return  = +24%
120D Return = +38%

Price > MA20
Price > MA60
Price > MA120
```

Expected:

```text
market_trend_state = STRONG_UPTREND
```

PASS.

---

# 61. Stress Test — Strong Downtrend

Example:

```text
20D Return  = -14%
60D Return  = -25%
120D Return = -36%

Price < MA20
Price < MA60
Price < MA120
```

Expected:

```text
market_trend_state = STRONG_DOWNTREND
```

PASS.

---

# 62. Stress Test — Conflicting Horizons

Example:

```text
20D  = +10%
60D  = +2%
120D = -15%
```

Expected:

Do NOT return Strong Uptrend.

Appropriate output:

```text
NEUTRAL
```

or transition/recovery state according to model parameters.

PASS.

---

# 63. Stress Test — Momentum Acceleration

Example:

```text
60D Return = +10%
20D Return = +15%
```

Expected:

```text
Momentum = POSITIVE
Acceleration = ACCELERATING
```

PASS.

---

# 64. Stress Test — Momentum Deceleration

Example:

```text
60D Return = +20%
20D Return = +2%
```

Expected:

```text
Momentum = POSITIVE
Acceleration = DECELERATING
```

PASS.

---

# 65. Stress Test — High Volatility

Example:

Price trend remains positive while realized volatility becomes extreme.

Expected:

```text
Trend = positive
Volatility = HIGH / EXTREME
```

Do NOT automatically produce Sell.

PASS.

---

# 66. Stress Test — Deep Drawdown

Example:

```text
Current Price = 65
Recent Peak = 100
```

Current Drawdown:

```text
-35%
```

Expected:

```text
DEEP_DRAWDOWN
```

subject to model context.

Do not automatically infer cheap valuation.

PASS.

---

# 67. Stress Test — Recovery

Example:

```text
Peak = 100
Low = 55
Current = 80
```

Stock remains below the peak but has recovered strongly from the low.

Expected:

```text
RECOVERING
```

rather than simply "still falling."

PASS.

---

# 68. Stress Test — Strong Relative Strength With Negative Return

Example:

```text
Stock  = -5%
Market = -15%
```

Expected:

```text
Absolute Performance = Negative
Relative Strength = Strong
```

PASS.

---

# 69. Stress Test — Low Liquidity

Example:

Very small average trading value and irregular trading.

Expected:

```text
liquidity_state = LOW / VERY_LOW
```

No automatic Buy/Sell decision.

PASS.

---

# 70. Stress Test — Abnormal Volume

Example:

```text
Current Volume = 4 × Average 20D Volume
```

Expected:

```text
abnormal_volume_flag = TRUE
```

Do not infer direction without price context.

PASS.

---

# 71. Stress Test — Price + Volume Confirmation

Example:

```text
Price ↑
Volume ↑ materially
```

Expected:

```text
PRICE_VOLUME_CONFIRMATION
```

Context only.

PASS.

---

# 72. Stress Test — Corporate Action

Example:

A capital increase mechanically changes raw quoted price.

Expected:

Historical performance calculations using properly adjusted price do not create:

* false crash,
* false volatility spike,
* false drawdown,
* false negative momentum.

PASS.

---

# 73. Stress Test — Fundamental / Market Conflict

Example:

```text
Fundamental = STRONG
Forecast = POSITIVE
Valuation = ATTRACTIVE

Market Trend = STRONG_DOWNTREND
```

Expected Stage 8 output:

```text
STRONG_DOWNTREND
```

Stage 8 does not modify fundamental outputs.

PASS.

---

# 74. Stress Test — Market / Fundamental Agreement

Example:

```text
Fundamental = STRONG
Forecast = POSITIVE
Valuation = ATTRACTIVE
Market = UPTREND
```

Expected:

Market Engine reports positive market state.

No extra Buy decision generated inside Stage 8.

PASS.

---

# 75. Stress Test — Weak Fundamental + Strong Market

Example:

```text
Fundamental = WEAK
Market = STRONG_UPTREND
```

Expected:

Both facts remain simultaneously valid.

Stage 8 does not override fundamentals.

PASS.

---

# 76. Stress Test — Missing Data

Example:

Only 10 valid trading observations exist.

Expected:

Long-horizon metrics such as:

```text
return_60d
return_120d
MA60
MA120
```

return:

```text
INSUFFICIENT_DATA
```

No fabricated history.

PASS.

---

# 77. Stress Test — Suspension / Trading Gap

Example:

Stock does not trade for multiple sessions.

Expected:

The engine must not create normal zero-return daily observations or treat the gap as ordinary continuous trading.

Flag where appropriate:

```text
TRADING_GAP
```

PASS.

---

# 78. Stress Test — Look-Ahead Bias

Historical Market State for date `T` is recalculated.

Expected:

Only data known at `T` is available.

Future prices cannot influence:

* Trend
* Momentum
* Volatility
* Relative Strength
* Liquidity
* Alerts

PASS.

---

# 79. Stress Test — Double Counting

Example:

20D Return, Price vs MA20, and Short Trend all describe similar recent price behavior.

Expected:

All may be exposed descriptively.

They must not be treated as three independent votes in a hidden aggregate score.

PASS.

---

# 80. Stress Test — No Market Score

Expected:

No field such as:

```text
market_score = 82
```

exists in Core V1.

PASS.

---

# 81. Audit Result

The following architectural requirements have been verified:

```text
Price structure                         PASS
Multi-horizon trend                     PASS
Momentum                                PASS
Momentum acceleration                   PASS
Volatility                              PASS
Drawdown                                PASS
Recovery context                        PASS
Relative strength                       PASS
Liquidity                               PASS
Abnormal volume                         PASS
Price-volume context                    PASS
Corporate-action handling               PASS
Point-in-Time                           PASS
Missing-data handling                   PASS
Trading-gap handling                    PASS
Fundamental/Market separation           PASS
No hidden valuation influence           PASS
No double counting                      PASS
No Market Score                         PASS
Model versioning                        PASS
Contract versioning                     PASS
Auditability                            PASS
Compact V1 architecture                 PASS
```

Final Audit Result:

**PASS**

---

# 82. Non-Negotiable Stage 8 Rules

The following rules are locked:

1. Stage 8 is a Market State Engine, not a Market Score Engine.
2. No Market Score 0–100 exists in V1.
3. Fundamental and Market analysis remain separate until Stage 9.
4. Stage 8 does not modify Fundamental Score.
5. Stage 8 does not modify Forecast EPS.
6. Stage 8 does not modify Target P/E.
7. Stage 8 does not generate Buy/Sell/Hold.
8. Adjusted Close is preferred for historical-return analytics.
9. Raw Close remains preserved.
10. Corporate actions must not create false market movements.
11. Point-in-Time rules are mandatory.
12. No future data may leak into historical Market States.
13. Missing data produces INSUFFICIENT_DATA.
14. Suspensions and trading gaps must not be treated as ordinary observations.
15. Trend uses multiple horizons.
16. Conflicting horizons must not create exaggerated Strong Trend labels.
17. Momentum and Trend remain distinct.
18. Volatility is risk, not direction.
19. Drawdown is not valuation.
20. Relative Strength is distinct from absolute return.
21. Liquidity is execution/risk context, not a Buy/Sell signal.
22. Abnormal volume is direction-neutral until interpreted with price context.
23. Moving averages are context variables, not independent votes.
24. A large technical-indicator library is excluded from Core V1.
25. No hidden double counting is permitted.
26. Internal model logic must be versioned.
27. Breaking output-contract changes require explicit contract versioning.
28. All outputs must be auditable and traceable to underlying MarketDaily data.

---

# 83. Final Stage 8 Definition

Stage 8 transforms raw OHLC/market activity into a compact, interpretable description of:

```text
Price Structure
Trend
Momentum
Volatility
Drawdown
Relative Strength
Liquidity
Market Alerts
```

without converting those variables into a single opaque score and without making the final investment decision.

Its output exists to provide Stage 9 with an independent description of current market behavior.

---

# 84. Final Status

```text
STAGE 8
MARKET ENGINE

DESIGNED
→ REVIEWED
→ STRESS TESTED
→ AUDITED
→ LOCKED
```

Any future implementation must preserve the above architecture unless a formally documented contract migration is approved.
