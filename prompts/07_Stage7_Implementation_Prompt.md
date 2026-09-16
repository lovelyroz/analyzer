# Stage 7 — Valuation Engine

## Execution Prompt

Implement or audit Stage 7 strictly against `07_Stage7_Valuation.md`.

Stage 7 evaluates valuation; it does not issue Buy/Sell/Hold, create a new forecast, recalculate Forecast Reliability, modify Fundamental Score, or perform technical analysis.

### Primary valuation chain
`Forecast Net Profit → Forecast EPS → Current Market Price → Forward P/E → Historical/Industry Comparison → Valuation Assessment`.

Forward P/E = Current Price / Forecast EPS.

Calculate Bear/Base/Bull Forward P/E independently. If EPS is zero, negative, or in a sign-change regime, P/E is NULL/NOT_APPLICABLE with the relevant flag. Never invent a P/E or fair value from invalid EPS.

### Benchmarks
Historical valuation is Point-in-Time TTM P/E using the price and TTM EPS available at that date. Preserve the historical P/E series and median when data exists.

Industry benchmark uses same-industry peers, minimum 8 valid peers. Do not mix Forward P/E and TTM P/E populations.

Base Target P/E hierarchy:
1. Industry Forward P/E Median
2. Historical Median P/E
3. Industry TTM P/E Median
4. `INSUFFICIENT_DATA`

Record the benchmark source.

### Scenario valuation
Target multiples for Bear/Base/Bull must be economically explainable, versioned, and backtestable. Do not use arbitrary fixed 0.8/1.0/1.2 or similar multipliers as an architectural rule.

Fair Value = Scenario EPS × Scenario Target P/E.
Scenario upside/downside = Fair Value / Current Price − 1.
Scenario probabilities must sum to 100%; initial V1 prior is Bear 20%, Base 60%, Bull 20%, with evidence-based adjustment and anti-double-counting.

Probability evidence is organized into Fundamental Direction, Forecast Direction, Profitability Assumption Risk, and Data/Structural Risk. Forecast Reliability is confidence evidence, not a direct P/E multiplier.

### Risk and confidence
Produce valuation status, expected fair value, expected upside, scenario dispersion, valuation risk/confidence, sensitivity/driver information, and alerts. Expected Upside must not hide high Bear-case risk.

Fundamental quality and trend may influence assessment, risk, confidence, or scenario evidence, but must not mechanically scale Target P/E.

### PIT/versioning
Valuation date, market price date, data cutoff, model version, and contract version must be explicit. Historical valuation must use only information available at the relevant date.

### Exclusions
No Buy/Sell/Hold output. No Market Score. No technical signal. No new forecast. No direct reliability multiplier on P/E.

### Verification
Test invalid EPS, PIT historical P/E, peer minimum, benchmark fallback, Forward-vs-TTM separation, scenario probabilities, scenario dispersion, target-multiple logic, sensitivity/alerts, reliability separation, and forbidden decision outputs. Run the full suite, audit the locked contract, and verify actual CI evidence.