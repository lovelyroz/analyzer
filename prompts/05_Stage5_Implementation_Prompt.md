# Stage 5 — Forecast Engine

## Execution Prompt

Implement or audit Stage 5 strictly against `05_Stage5_Forecast_Engine.md`.

Stage 5 forecasts future financial outcomes. It does not create a new KPI/score, evaluate its own accuracy, value the stock, or generate market/trading signals.

### Forecast families
**Non-financial:** Petrochemical/Chemical, Metals/Mining, Cement, Food, Pharmaceutical.
Core chain:
`Revenue → Operating Margin → Operating Profit → Net Profit → EPS → ROE`.

**Financial:** Bank and Investment/Holding.
- Bank: Loans/Deposits → NII/NIM → Net Profit → EPS → ROE; NPL is context unless a validated model relationship exists.
- Holding: NAV → NAV Growth → Net Profit → EPS → ROE; P/NAV belongs to Stage 7.

### Revenue hierarchy
1. Historical/Seasonal Baseline
2. Recent Run Rate
3. Driver-Based Adjustment

Drivers must be official/measurable and optional. Missing drivers are omitted, never fabricated.

### Profit chain
Operating Margin = Operating Profit / Revenue.
Forecast Operating Profit = Forecast Revenue × Forecast Operating Margin.
Net Profit hierarchy: component-based → historical Net/Operating conversion → Revenue × Net Margin → insufficient data.

### Per-share and return metrics
Forecast EPS = Forecast Net Profit Attributable / Forecast Weighted Average Shares. Share-count history and corporate actions must be respected. ROE uses forecast profit / average equity when equity forecast is reliable; otherwise insufficient data.

### Baselines and scenarios
Retain Recent Run Rate, Historical/Seasonal Baseline, and Seasonal Naive. Prefer Historical/Seasonal when seasonality is valid; otherwise Recent Run Rate. Seasonal Naive is retained for Stage 6 evaluation.

Produce Bear/Base/Bull scenarios. Scenario differences must be evidence/uncertainty based, not arbitrary fixed ±20% rules.

### Trend and risk controls
Stage 4 evidence is consumed, not recomputed. Trend is evidence for bounded, explainable forecast adjustment; never map a momentum percentage directly to the same forecast growth. Low Base and sign-change flags prevent mechanical extrapolation.

### FX
Where operating earnings are genuinely FX-linked, operational/exchange FX is preferred. Free-market FX must never silently substitute for missing operational FX. Any proxy must be explicit and low-confidence/estimated.

### Versioning and PIT
Forecasts are versioned and never overwritten. Forecast cutoff and model version must be stored. Historical forecasts must use only information available at cutoff.

### Verification
Test all forecast families, hierarchy fallbacks, missing data, sign changes, low base, share-count changes, scenario ordering, operational FX separation, PIT cutoff, and version preservation. Run the full suite, audit against the locked contract, and verify actual CI evidence. Do not redesign the architecture for an implementation defect.