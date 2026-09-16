# Stage 3 — Fundamental Scoring

## Execution Prompt

Implement or audit Stage 3 strictly against `03_Stage3_Fundamental_Scoring.md` and the Master Architecture.

Stage 3 produces the **Fundamental Score (0–100)** representing current fundamental condition only.

### Inputs allowed
- Stage 2 standardized KPIs and KPI definitions
- Industry classification and peer groups
- Historical company data only as the defined fallback benchmark/context
- Data quality from Stage 1

### Locked score architecture
Top-level axes:
- Growth 30%
- Profitability 45%
- Risk & Quality 25%

Universal internal weights:
- Growth: Revenue 15%, Operating Profit 25%, Net Profit 30%, EPS 30%
- Profitability: Gross Margin 10%, Operating Margin 25%, Net Margin 20%, ROA 20%, ROE 25%
- Risk & Quality: Cash Earnings Conversion 40%, Earnings Quality 60%

KPI scoring path:
`Raw KPI → Comparable KPI → Benchmark → KPI Score (0–100)`.

Directions must be explicit, including lower-is-better for NPL.

### Benchmark hierarchy
- Primary: industry-relative percentile
- Minimum peer count: 8
- If fewer than 8 peers: historical company benchmark
- If neither is sufficient: `INSUFFICIENT_DATA`

Historical data is a fallback benchmark, not a second vote.

### Industry redistribution — V1 locked
Industry KPIs use **20% of an affected axis as a redistribution budget**, not a bonus. The remaining 80% is allocated proportionally to universal KPI weights; the 20% is divided equally among applicable industry KPIs. Axis totals remain unchanged.

Mappings:
- Bank: Loan Growth + Deposit Growth → Growth; NII + NIM → Profitability; NPL → Risk & Quality
- Investment/Holding: NAV Growth → Growth; NAV → Profitability; P/NAV → valuation-only/excluded from Stage 3
- Cement/Food/Pharmaceutical: Sales Volume → Growth
- Petrochemical/Chemical and Metals/Mining: no Stage 3 industry KPI in V1

### Missing-data rule
Missing KPI ≠ poor KPI. Do not assign score 0. Redistribute the missing KPI's original weight among available KPIs in the same axis. Minimum axis coverage is 60%; below that, the axis is `INSUFFICIENT_DATA`.

### Hard exclusions
Never use price, P/E, P/NAV, valuation, forecast, forecast reliability, technical/market data, volume, or future expectations in the Fundamental Score.

### Output
At minimum preserve company_id, fundamental_score, three axis scores, axis coverage, score data quality, timestamp, scoring method version, and enough component detail to explain every score.

### Verification
Test percentile endpoints, directionality, peer fallback, historical fallback, missing-weight redistribution, 60% coverage, industry redistribution, P/NAV exclusion, data quality, and forbidden inputs. Run the full suite, perform a requirement-by-requirement audit, and verify actual CI evidence. Do not weaken tests or alter architecture to obtain a green result.