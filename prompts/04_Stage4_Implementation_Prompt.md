# Stage 4 — Historical, Seasonal & Trend Engine

## Execution Prompt

Implement or audit Stage 4 using `04_Stage4_Historical_Trend.md` as the detailed contract.

Stage 4 answers: **How does current fundamental performance compare with company history, and in which direction is it moving?**

It produces context and direction only. It does not change the Fundamental Score, create a new score, forecast, value the company, or generate a market/trading signal.

### Required analysis
- Historical: MoM, QoQ, YoY, same-period multi-year, multi-year trend
- Seasonal baseline: median of the same period across at least 3 valid historical observations
- Seasonal Surprise = Current / Seasonal Baseline − 1
- If baseline is zero or sign changes: surprise is NULL and appropriate flags are emitted
- Flow momentum: 3M sum vs prior 3M, 6M sum vs prior 6M, 12M current TTM vs TTM ending 12 months earlier
- Stock momentum: period-end value vs 3/6/12 months earlier; never sum stocks
- EPS trend: same-definition comparison, respecting share-count/corporate-action history

### Context controls
Support explicit flags:
- `LOSS_TO_PROFIT`
- `PROFIT_TO_LOSS`
- `SIGN_CHANGE`
- `ZERO_BASE`
- `LOW_BASE`

Low-base detection requires at least 3 comparable historical observations and uses median + MAD; robust z ≤ −2.5 identifies a low base. If evidence is insufficient, use UNKNOWN rather than FALSE.

### Relative trend strength
Use company-history momentum for the same horizon. Minimum 8 observations. Percentile of absolute momentum:
- <50 → Weak
- 50–<75 → Normal
- ≥75 → Strong

### Trend state
Combine valid 3M/6M/12M directional evidence:
- Strong Improvement
- Improving
- Stable
- Deteriorating
- Strong Deterioration

Strong Improvement/Strong Deterioration require all valid horizons to agree and at least two to be Strong. With two valid horizons, calculation is allowed with LIMITED confidence. With only one valid horizon, return `INSUFFICIENT_DATA`.

### Important separation
Trend Direction and Relative Strength are different concepts. Do not collapse them into one metric or one vote. TTM is a period construction, not an additional vote.

### Verification
Test flow vs stock treatment, true 12-month TTM comparison, zero/sign-change handling, low-base robustness, relative-strength minimum history, mixed horizons, one/two/three valid horizons, and the rule that Stage 4 never modifies Stage 3. Run the complete suite, audit every requirement, and verify actual CI evidence.