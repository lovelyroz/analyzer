# Analyzer V1 — Database Architecture Amendment V1.1

## Status

**APPROVED — V1.1**

This amendment is part of the Database Architecture V1 contract. It resolves a provenance/granularity gap discovered during the post-implementation architecture audit. It does not add a new analytical stage and does not change ownership of Stages 2–9.

## 1. Finding

The database architecture permits many raw report lines to map to one standard financial concept, but a single `NormalizedFinancialFact.raw_fact_id` cannot represent all raw contributors when a concept is normalized from multiple source lines.

Keeping only one raw provenance link would make a valid many-to-one mapping technically possible but incompletely auditable.

## 2. Corrected architecture

`NormalizedFinancialFact` represents the standardized concept-level value for a company, period, metric, and report version.

Its source provenance is represented through:

`NormalizedFinancialFactInput`

The bridge supports one-to-many provenance:

```text
Raw Fact A ─┐
Raw Fact B ─┼──> NormalizedFinancialFact (COGS)
Raw Fact N ─┘
```

A direct one-line mapping is represented by one bridge row. A multi-line composition is represented by multiple bridge rows.

## 3. Double-counting rule

When both an aggregate line and its components exist, the mapping decisions must identify their composition roles. The normalization/resolution process must select either the valid aggregate or the non-overlapping components according to the applicable rule.

The database must never sum an aggregate and the components that are already included in that aggregate.

## 4. New table

`normalized_financial_fact_inputs`

Fields:

- `input_id`
- `normalized_fact_id`
- `raw_fact_id`
- `mapping_decision_id`
- `input_role`

Allowed `input_role` values:

- `DIRECT`
- `COMPONENT`
- `TOTAL`
- `SUBTOTAL`
- `DISCLOSURE`

The table enforces foreign-key provenance and uniqueness of the same normalized/raw/mapping relationship.

## 5. Existing fields

The existing nullable `raw_fact_id` and `mapping_decision_id` fields on `NormalizedFinancialFact` are retained for backward compatibility and direct provenance convenience.

For all new pipeline writes, the bridge is authoritative when a normalized value has multiple source inputs. A normalized fact with one direct source may retain the direct fields and must also be representable through the bridge.

## 6. Derived facts

`DerivedFinancialFact` remains the correct layer for values calculated by formulas or aggregations that are analytically derived rather than directly normalized from a report line.

Its existing `DerivedFinancialFactInput` table remains unchanged and continues to preserve normalized/derived calculation lineage.

## 7. Migration

Schema migration version **3** adds `normalized_financial_fact_inputs`.

The migration:

- is additive;
- does not rewrite raw values;
- does not delete existing facts;
- is idempotent;
- preserves existing schema versions;
- is applied after schema version 2.

No historical data is silently backfilled into the new bridge because a valid source mapping cannot be inferred safely from existing nullable provenance fields without an auditable mapping decision.

## 8. Downstream contract

Stages 2–9 continue to consume standardized concept values. They must not inspect raw report labels directly when a normalized concept is available.

This amendment only strengthens provenance and composition integrity; it does not introduce KPI, scoring, forecast, valuation, market, or decision logic into Stage 1.

## 9. Acceptance criteria

The database must support all of the following simultaneously:

1. one raw line → one standard concept;
2. many raw lines → one standard concept;
3. an unmapped raw line remains visible but unusable downstream;
4. aggregate/component double counting is prevented by explicit composition roles and resolution rules;
5. normalized values remain distinguishable from derived values;
6. every new multi-source normalized value can be traced to every contributing raw fact and mapping decision.

## 10. Version

`database_contract_version = DATABASE_CONTRACT_V1.1`

The overall Analyzer architecture remains **V1**. This is a compatible database-contract amendment, not a new analytical architecture.
