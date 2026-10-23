# P50 — CODAL Raw-to-Normalized Mapping and Implementation Readiness

You are continuing Stage 7 remediation in the local project folder `analyzer`.

## Objective

Investigate the specific gap established by P49: raw CODAL facts are ingested, and normalized-fact models exist, but a production writer from raw facts to normalized facts was not found.

Determine whether the project contains enough explicit, authoritative mapping rules to implement this path safely. Implement the supported portion if the required contracts already exist. Do not invent financial mappings to force completion.

## Mandatory constraints

- Work only in the local `analyzer` folder.
- No GitHub, GitHub CLI/API, remote access, or Git operations.
- Do not run tests or CI. The user will run them.
- Do not perform a repository-wide scan. Follow the CODAL extraction, raw-fact ingestion, normalized models/provenance, existing metric mappings, and only directly relevant specifications or tests.
- Do not edit `reply.md`, `temp_report.md`, `temp_report2.md`, `ClaudeReports/`, `stepsForStage7.md`, or `stage_7_prompts.md`.
- Do not redesign or centralize `engine.py`.
- Do not fabricate metric codes, units, period mappings, publication timestamps, quality statuses, industry mappings, or financial values.
- Do not weaken existing tests or alter financial formulas to accommodate missing data.
- Do not claim tests were run.

## Targeted investigation

### 1. Trace the actual raw-fact contract

Inspect the relevant code to establish:
- how raw CODAL facts are extracted and represented;
- which identifiers, values, units, periods, and provenance fields are retained;
- how report publication/accessibility time is represented;
- whether raw facts retain enough source information to support an auditable normalized record.

Use concrete code evidence, not assumptions.

### 2. Find explicit mapping rules

Inspect only directly relevant mapping definitions, CODAL extraction rules, schemas, specifications, and existing tests.

Determine whether each mapping needed to create a `NormalizedFinancialFact` is explicitly defined, including:
- source fact identification;
- destination `FinancialMetric` identification;
- unit and scale handling;
- company and reporting-period association;
- publication/provenance linkage;
- quality-status rules and handling of ambiguous or conflicting facts.

Distinguish an explicit, approved rule from a mapping that would have to be inferred.

### 3. Review the normalized-fact contract

Inspect the relevant model and provenance fields and establish:
- required fields and integrity constraints;
- how `ReportVersion` and `FinancialPeriod` should be linked;
- how duplicate, conflicting, incomplete, or unmapped facts should be handled;
- whether normalized facts have an audit trail sufficient to trace a computed input back to the original CODAL fact;
- whether downstream financial queries should exclude any quality statuses.

Do not change existing query behavior merely because a quality filter appears desirable. First establish the intended semantics from explicit code, specifications, and tests. Report any unresolved conflict.

### 4. Implement only what the evidence supports

If the repository contains sufficient explicit mappings and contracts:
- implement the smallest coherent raw-to-normalized writer or adapter using existing project conventions;
- preserve source provenance and temporal information;
- make duplicate processing deterministic and safe;
- ensure unmapped or ambiguous facts cannot silently become valid financial metrics;
- add focused tests for supported mappings, provenance, invalid/unmapped facts, duplicate behavior, and relevant temporal boundaries;
- do not run those tests.

If essential mapping rules or source fields are missing:
- do not invent them;
- do not create a misleading generic mapping table populated with guessed values;
- implement only independently safe infrastructure that does not imply unsupported financial mappings;
- provide an exact list of missing mapping decisions, the affected metrics, and the evidence required to resolve each one.

Do not stop at a generic blocker if a useful, independently correct implementation is supported by existing contracts.

## Acceptance criteria

- Every implemented mapping must be traceable to an explicit source rule.
- No financial value may be silently guessed, rescaled, or assigned to an unsupported metric.
- Provenance and publication-time information must not be discarded.
- Repeated processing must not silently create conflicting normalized records.
- Existing downstream query contracts and financial formulas must not be changed without separate evidence and justification.
- Tests must be added for implemented behavior, but not executed by you.
- Clearly distinguish code changes made from unresolved mapping decisions.

## Final report

Provide:
1. Raw CODAL fact contract and evidence.
2. Mapping rules found, with source locations.
3. Normalized-fact and provenance requirements.
4. Exact implementation changes, if any.
5. Tests added, if any, and explicitly state they were not run.
6. Unresolved mappings or quality/PIT conflicts.
7. Files inspected and files changed.
8. The smallest safe next step.

Do not edit report or planning files. Complete the targeted task before reporting back.