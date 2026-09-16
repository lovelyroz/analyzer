# Stage 6 — Forecast Evaluation & Calibration

## Execution Prompt

Implement or audit Stage 6 strictly against `06_Stage6_Forecast_Evaluation.md`.

Stage 6 evaluates forecasts produced by Stage 5. It never generates a new forecast and never recalculates valuation or market analysis.

### Evaluation key
Match by:
`Company + Metric + Financial Period + Horizon + Model Version + Forecast Cutoff`.

Actuals must come from the correct Point-in-Time ReportVersion and must use the same metric definition.

### Error metrics
- Error = Actual − Forecast
- Percentage Error = (Actual − Forecast) / |Forecast| × 100 when valid
- APE = absolute percentage error
- MAPE = mean APE; primary V1 accuracy metric
- Bias = mean signed percentage error

For zero forecast/base, loss→profit, profit→loss, or sign-change regimes, percentage metrics are normally NULL and the regime flag is preserved; absolute error may still be stored.

### Horizons and sample size
Evaluate 1M, 3M, 6M, 12M independently. Do not pool horizons.

Confidence by valid observations:
- <5: `INSUFFICIENT_DATA`
- 5–7: `LOW_CONFIDENCE`
- 8–11: `MODERATE_CONFIDENCE`
- ≥12: `ADEQUATE`

### Baseline
Use Point-in-Time Seasonal Naive as the V1 baseline. Compare model error and baseline error using a compatible metric. Persistent model underperformance is explicitly identified as `MODEL_UNDERPERFORMS_BASELINE`.

### Reliability
Reliability is 0–100 and represents historical forecast trustworthiness, not scenario probability. V1 performance architecture:
- Accuracy 50%
- Bias Control 20%
- Baseline Advantage 30%

Reliability must not mathematically modify Forward P/E.

### Calibration
Calibration is allowed only for persistent, repeatable bias/performance evidence. A new calibration creates a new model version, is evaluated out-of-sample/holdout, and preserves prior versions.

### PIT and exclusions
No future information may enter evaluation or baseline construction. Do not create a Fundamental Score, Valuation, Market Score, Decision, or new forecast.

### Verification
Test matching, PIT, horizons, zero/sign-change regimes, MAPE/Bias, baseline comparison, observation thresholds, model-version separation, reliability bounds, persistent-bias calibration, and preservation of old forecasts/models. Run the full suite, audit the contract, and verify actual CI evidence.