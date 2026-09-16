# Stage 9 — Decision Engine & Dashboard Contract

## Execution Prompt

Implement or audit Stage 9 strictly against `09_Stage9_Decision_Dashboard.md` and the Master Architecture.

Stage 9 is the final **Rule-Based Evidence Integration** layer. It consumes upstream outputs; it does not recreate upstream calculations or introduce a new analytical engine.

### Four evidence families
A. Fundamental Quality — Stage 3 score, axes, coverage, data quality.
B. Fundamental Direction & Future — Stage 4 trend/momentum, Stage 5 forecast state/outputs/revisions, Stage 6 reliability/accuracy/bias/calibration.
C. Valuation — Stage 7 status, expected upside/fair values, scenario probabilities/dispersion, valuation risk/confidence, P/E benchmarks, drivers, alerts.
D. Market State — Stage 8 trend, momentum, relative strength, volatility, drawdown, liquidity, price-volume, regime, alerts.

Market evidence is Context/Confirmation/Risk. It does not override fundamentals by itself.

### Decision states
`STRONG_BUY`, `BUY`, `HOLD`, `WATCH`, `REDUCE`, `SELL`, `STRONG_SELL`.

Decision is rule-based evidence integration, not a simple weighted score. Do not create `Market Score`, `Technical Score`, composite score, or position sizing.

### Locked conflict/safety behavior
Support explicit conflicts including:
- `CHEAP_BUT_WEAK`
- `STRONG_BUT_EXPENSIVE`
- `STRONG_FUNDAMENTAL_WEAK_MARKET`
- `WEAK_FUNDAMENTAL_STRONG_MARKET`
- `POSITIVE_FX_NEGATIVE_FUNDAMENTAL`
- `POSITIVE_FORECAST_LOW_RELIABILITY`
- `HIGH_EXPECTED_UPSIDE_HIGH_BEAR_RISK`
- `VALUATION_NOT_APPLICABLE`
- `LOW_LIQUIDITY`
- `INSUFFICIENT_DATA`

Cheap + weak fundamentals + negative trend/forecast must not automatically become BUY. Strong fundamentals + excessive valuation must not automatically become BUY. Low forecast reliability reduces confidence and constrains strong decisions; it does not mathematically alter P/E. Negative/zero EPS or sign-change valuation must not create artificial P/E. Scenario dispersion must remain visible.

### Holding status
Keep separate from Decision:
`STRONG_HOLD`, `HOLD`, `HOLD_WITH_CAUTION`, `REVIEW_HOLD`, `EXIT_CANDIDATE`.
No position sizing.

### Confidence, stability, history
Decision Confidence is separate from Fundamental Score and Decision. It must reflect data quality, evidence agreement, forecast reliability, valuation confidence, scenario dispersion, conflicts, market confirmation, and sufficiency.

Hysteresis is mandatory and parameterized. Decision History is mandatory: previous decision, current decision, change, date, reasons.

### Ranking
No new Ranking Score. Primary ranking is within industry and uses decision state/tier, confidence, expected upside, valuation risk, forecast reliability, and fundamental quality, subject to eligibility rules.

### FX
Consume Free-Market FX for market/USD valuation context and Operational FX for supported operating/earnings exposure. Never silently substitute one for the other. `fx_gap` is contextual only. FX must not create an independent decision vote.

### Dashboard contract
Level 1: company, price, decision, confidence.
Level 2: fundamental, trend, forecast, reliability, valuation, upside/risk, market, relative strength, liquidity, FX.
Level 3: why, risks, scenario, decision history.
Keep explanations compact and traceable.

### Verification
Test evidence-family integration, conflict states, reliability constraints, invalid valuation, scenario dispersion, hysteresis, decision history, ranking eligibility/order, FX separation, low liquidity, insufficient data, dashboard completeness, and absence of forbidden scores/signals/recalculation. Run the full suite, audit every contract boundary, and verify actual CI evidence.