# CONTINUE TEHRAN STOCK ANALYSIS PROJECT — V1

You are continuing an existing software/financial-analysis architecture project.

The uploaded NotebookLM sources are the authoritative project documentation.

## SOURCE PRIORITY

Use the uploaded sources as the primary and authoritative basis for understanding this project.

Priority order:

1. `00_a_Master_Architecture.md`
2. `00_Architecture_Freeze_Point.md` : Start Point
2. The locked specifications of Stages 1–9
3. Other project prompts / historical architecture documents

Do NOT silently replace, simplify, reinterpret, or redesign decisions that are already locked.

If two sources appear to conflict:

* First determine whether one is an older/historical version.
* Treat the final/current architecture documented in `00_Master_Architecture.md` as authoritative.
* Do not merge conflicting versions automatically.
* Clearly identify the conflict and explain which version is current.

## CURRENT PROJECT STATUS

The project architecture has already been designed and locked through Stage 9.

The current V1 architecture consists of exactly these nine stages:

1. Data Foundation & Data Model
2. KPI Specification
3. Fundamental Scoring
4. Historical, Seasonal & Trend Engine
5. Forecast Engine
6. Forecast Evaluation & Calibration
7. Valuation Engine
8. Market Engine
9. Decision Engine & Dashboard Contract

All nine stages are currently LOCKED.

Therefore:

* Do not redesign the architecture unless a genuine contradiction is demonstrated.
* Do not reopen locked decisions casually.
* Do not add new stages unless explicitly requested.
* Do not add unnecessary KPIs, indicators, data sources, or complexity.
* Preserve the modular boundaries between stages.

## DEVELOPMENT PRINCIPLE

The architecture is already frozen.

The next phase is implementation.

Implementation must follow the locked architecture rather than becoming an opportunity to redesign it.

For every implementation task:

1. Identify which stage(s) it belongs to.
2. Identify the relevant locked specification.
3. Identify the required inputs.
4. Identify the required outputs.
5. Identify dependencies on previous stages.
6. Implement only the necessary functionality.
7. Test it against the locked specification.
8. Report any architectural contradiction before changing anything.

## IMPORTANT ARCHITECTURAL RULE

Each stage owns its internal logic and exposes a defined contract.

Internal implementation may evolve without changing other stages as long as the contract remains compatible.

If a contract genuinely needs to change:

* explicitly identify the reason,
* identify affected downstream stages,
* propose a versioned contract change,
* do not silently break compatibility.

## DATA PRINCIPLES

The system is primarily based on Codal financial statements.

The system also uses:

* daily OHLC / market data
* FX data
* share-count history
* corporate actions

Raw data must remain traceable to its source.

Point-in-Time / look-ahead protection is mandatory.

Report corrections and restatements must be versioned.

IRR is the financial base currency.

USD values are derived.

## IMPORTANT FX ARCHITECTURE

Do NOT treat USD as one generic exchange rate.

The system distinguishes at least:

* FREE_MARKET
* OPERATIONAL / EXCHANGE

Operational FX is relevant to company sales/earnings exposure where appropriate.

Free-market FX is relevant to market valuation and USD-relative market value.

Operational FX must NOT silently fall back to free-market FX.

If operational FX is missing, it must be explicitly marked as missing or estimated/proxy data.

FX context must not become an independent Buy/Sell signal.

## DECISION ARCHITECTURE

The final decision integrates four evidence families:

A. Fundamental Quality
B. Fundamental Direction & Future
C. Valuation
D. Market State

Decision Engine integrates evidence; it does not recreate the analysis performed by previous stages.

The system must avoid double counting.

Decision states are:

* STRONG_BUY
* BUY
* HOLD
* WATCH
* REDUCE
* SELL
* STRONG_SELL

Holding is a legitimate investment state.

Decision Confidence is separate from Decision.

Decision Conflict must be explicitly represented.

Decision history and decision changes must be retained.

Hysteresis / decision stability must prevent insignificant fluctuations from causing repeated decision flipping.

## VALUATION PRINCIPLE

Forward P/E is the primary valuation axis.

Core sequence:

Forecast Net Profit
→ Forecast EPS
→ Current Market Price
→ Forward P/E
→ Historical / Industry Comparison
→ Forecast Reliability
→ Valuation Assessment

Do not create artificial P/E values when EPS is zero, negative, or subject to sign-change conditions.

## FORECAST PRINCIPLE

Forecasting is forward-looking and rolling.

Forecast versions must never be overwritten.

Forecast evaluation compares:

Forecast
→ Actual
→ Error
→ Accuracy
→ Bias
→ Baseline
→ Reliability
→ Calibration

Forecast Reliability is historical forecast performance.

It must not be confused with current scenario probability confidence.

## MARKET PRINCIPLE

Stage 8 is a Market State Engine, NOT a Market Score Engine.

Do not introduce a Market Score unless explicitly requested and architecturally reviewed.

Technical indicators are deliberately minimized.

Market context must remain separate from fundamental analysis until Stage 9.

## IMPLEMENTATION DISCIPLINE

The project must remain compact.

Prefer:

* simple
* explainable
* auditable
* modular
* testable
* versioned

over:

* unnecessarily complex
* highly parameterized
* machine-learning-heavy
* difficult to audit
* data-hungry

V1 explicitly avoids unnecessary ML complexity, large technical-indicator systems, and mandatory external datasets.

## WHEN I GIVE YOU A NEW TASK

Do not immediately redesign the system.

First state briefly:

* Which stage the task belongs to.
* Which locked specification governs it.
* What existing components it depends on.
* What the expected output is.

Then proceed with the task.

If the task conflicts with a locked architectural decision, STOP and explain the conflict before implementing.

## CURRENT STARTING POINT

The architecture is complete.

Stages 1–9 are locked.

We are now at the transition from:

ARCHITECTURE DESIGN

to

IMPLEMENTATION.

Continue the project from this exact point.

_____________________ end of 1st prompt __________________



بعد از این Prompt، فعلاً هیچ کاری از NotebookLM نخواه

یعنی همان لحظه نگو:

حالا Stage 1 را پیاده‌سازی کن.

اول بگذار NotebookLM کانتکست پروژه را تثبیت کند.

سپس یک پیام کوتاه دیگر بده:

Based strictly on the uploaded project sources, summarize the current architecture status and confirm the exact next implementation step. Do not redesign anything.




هدف این پیام این است که ببینی آیا NotebookLM درست متوجه شده که:

Stage 1 تا Stage 9 تمام شده‌اند و پروژه وارد فاز Implementation شده است.

_____________________ end of 2nd prompt __________________

بعد از اینکه پاسخ درست بود، وارد Implementation شو

اینجا من پیشنهاد می‌کنم از Stage 1 شروع کنیم؛ نه چون Stage 1 هنوز طراحی نشده، بلکه چون اولین چیزی است که باید در نرم‌افزار ساخته شود.

مثلاً پیام بعدی:

We are now starting implementation.

Implement Stage 1 — Data Foundation & Data Model strictly according to its locked specification.

Do not redesign Stage 1.
Do not proceed to Stage 2.
First define the implementation structure, database schema, relationships, constraints, and migration strategy.

After that, stop and wait for my review.


____________ Comment:
ما همان روش قبلی را حفظ می‌کنیم:

Stage 1
   ↓
Implementation
   ↓
Test
   ↓
Audit
   ↓
Approve
   ↓
Stage 2
   ↓
Implementation
   ↓
Test
   ↓
Audit
   ↓
Approve
...

__________________ Example : Prompt of Next stages ________________
We are continuing implementation of the Tehran Stock Analysis V1 project.

The architecture and Stages 1–9 are locked according to the uploaded sources.

Current implementation status:
Stage 1 — [مثلاً Database schema completed]
Stage 1 testing — [مثلاً pending]

Continue from this exact point.

Do not redesign locked architecture.
