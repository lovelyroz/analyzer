# Stage 2 — KPI Specification

## Execution Prompt

You are implementing or auditing Stage 2 of Analyzer V1. Read the Master Architecture, `02_Stage2_KPI_Specification.md`, and current implementation status first.

Stage 2 defines **what is measured**. It does not define final scoring, forecasting, valuation, market analysis, or decisions.

### Locked KPI inventory

Universal Core — exactly 11:

**Growth**
- Revenue Growth
- Operating Profit Growth
- Net Profit Growth
- EPS Growth

**Profitability**
- Gross Margin
- Operating Margin
- Net Profit Margin
- ROA
- ROE

**Risk & Quality**
- Cash Earnings Conversion = OCF / Net Profit
- Earnings Quality = composite analytical framework; do not reduce it to one simplistic ratio

Conditional:
- Financial Cost Pressure = Financial Costs / Operating Profit, only where economically meaningful and denominator-valid.

Base metrics are not extra KPIs: Revenue, Operating Profit, Net Profit, EPS, TTM Revenue, TTM Net Profit.

Period dimensions are not extra KPIs: MoM, QoQ, YoY, Multi-Year, Same-Period Multi-Year, Rolling/TTM, Seasonal Comparison.

### Industry scope
Exactly seven V1 groups:
1. Bank
2. Investment / Holding
3. Petrochemical / Chemical
4. Metals / Mining
5. Cement
6. Food
7. Pharmaceutical

Industry Core — exactly 11:
- Bank: NII, NIM, Loan Growth, Deposit Growth, NPL/Credit Quality
- Investment/Holding: NAV, NAV Growth, P/NAV
- Cement: Sales Volume
- Food: Sales Volume
- Pharmaceutical: Sales Volume
- Petrochemical/Chemical: none
- Metals/Mining: none

P/NAV may be specified here as an industry KPI, but its valuation use belongs to Stage 7 and it must not contaminate Stage 3 scoring.

### Locked principles
- Financial statements are the primary V1 source.
- External commodity, macro, export-price, feedstock, or other datasets are not mandatory Core KPI inputs.
- Industry KPIs must add economically meaningful information and map into Growth, Profitability, or Risk & Quality.
- Missing data remains missing; never convert it to zero.
- EPS growth must respect share-count history and corporate actions from Stage 1.
- KPI data quality must remain explicit.
- KPI definitions must remain compatible with Stage 1 PIT/versioning.

### Exclusions
Do not create Fundamental Score, KPI weights, valuation outputs, forecast outputs, forecast reliability, Market Score, trading signals, or decision states.

### Implementation and audit
Inspect the existing KPI implementation before changing it. Verify canonical industry codes, formulas, period semantics, TTM treatment, EPS comparability, data-quality propagation, and exclusion of out-of-scope metrics. Add contract and edge-case tests. Run the complete suite, audit against the locked specification, then verify actual CI evidence. Any discovered defect should be fixed at the smallest responsible layer; do not redesign the architecture for an implementation bug.