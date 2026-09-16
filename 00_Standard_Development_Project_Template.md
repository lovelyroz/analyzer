# STANDARD DEVELOPMENT PROJECT TEMPLATE

## Purpose

This document is a reusable development/process template derived from the actual development experience of Analyzer V1.

It defines **how a project is designed, implemented, tested, audited, locked, and advanced**.

It is a process template. It does not define the architecture of any specific project.

---

# 1. Core Principle

The project must move through explicit gates:

**Architecture / Specification → Implementation → Tests → Audit → CI → Lock → Next Stage**

No stage is considered complete merely because code exists.

A stage becomes complete only when its specification, implementation, tests, audit, and CI evidence are consistent.

---

# 2. Project Initialization

Before implementation begins, create:

- Master Architecture
- Architecture Freeze Point
- Architecture Change Log
- Stage/Module Map
- Implementation Status
- CI test workflow

Recommended files:

```text
00_Master_Architecture.md
00_Architecture_Freeze_Point.md
00_Standard_Development_Project_Template.md
10_Implementation_Status.md
99_Architecture_Change_Log.md
.github/workflows/tests.yml
```

If the project is staged, use:

```text
01_Stage1_<Name>.md
02_Stage2_<Name>.md
...
NN_StageN_<Name>.md
```

---

# 3. Phase A — Architecture / Specification

## A1. Define the objective

Write:

- What problem the stage solves
- What output it must produce
- What upstream information it may consume
- What downstream information it must provide

## A2. Define responsibility boundaries

Explicitly state:

- What belongs to the stage
- What does NOT belong to the stage
- Which calculations must remain upstream
- Which calculations must remain downstream

This prevents responsibility leakage and duplicate logic.

## A3. Define the contract

For every important output define:

- field name
- type
- meaning
- valid values
- missing-data behavior
- quality status
- timestamp/cutoff requirements
- model/specification version
- provenance where applicable

## A4. Define invariants

Examples:

- NULL must not silently become zero.
- Historical calculations must not use future information.
- Upstream outputs must not be silently recreated downstream.
- Old model versions must remain reproducible.
- A score must not be created unless scoring is explicitly part of the stage.

## A5. Define exclusions

Every stage should explicitly list prohibited scope.

Examples:

- no new KPI
- no valuation
- no trading signal
- no position sizing
- no external data requirement
- no machine-learning model

Only exclusions relevant to the project should be used.

## A6. Lock the specification

Once reviewed:

```text
Specification Status: LOCKED
```

Implementation may now begin.

A locked specification must not be silently edited during implementation.

If the specification is genuinely wrong, use the Architecture Change Log or an explicit specification-change process.

---

# 4. Phase B — Implementation

Implement only the locked contract.

## B1. Build the smallest complete implementation

Prefer:

- explicit modules
- deterministic behavior
- traceable calculations
- simple fallbacks
- versioned parameters
- clear data-quality handling

Avoid premature complexity.

## B2. Preserve modular boundaries

A module may change internally without forcing downstream changes when its public contract remains compatible.

Contract-breaking changes require:

1. identification
2. impact analysis
3. migration/versioning
4. test updates
5. audit

## B3. Never hide assumptions

Assumptions must be represented explicitly.

Examples:

- proxy data
- fallback methodology
- insufficient observations
- estimated values
- model parameters
- confidence limitations

Do not silently substitute a convenient value.

## B4. Preserve historical reproducibility

Where historical information matters:

- preserve source versions
- preserve publication/availability time
- preserve model version
- preserve calculation parameters
- never overwrite historical outputs without traceability

---

# 5. Phase C — Testing

Tests must validate the **contract**, not merely code execution.

## C1. Minimum test groups

### Happy Path

Normal valid inputs produce expected outputs.

### Edge Cases

Test:

- NULL
- zero
- negative values
- sign changes
- insufficient history
- insufficient peer count
- missing dependencies
- duplicate inputs
- boundary values

### Contract Tests

Verify exact output fields, states, types, and required invariants.

### Integration Tests

Verify that upstream and downstream contracts connect correctly.

### Safety Tests

Explicitly test prohibited behavior.

Examples:

- no hidden score
- no prohibited output
- no future-data leakage
- no silent fallback
- no double counting

### Regression Tests

Every discovered defect should receive a regression test when practical.

## C2. Test failure interpretation

A failing test is not automatically a reason to weaken the test.

First determine whether:

1. implementation is wrong
2. specification is wrong
3. test is obsolete
4. contract is incomplete

Then fix the smallest correct layer.

---

# 6. Phase D — Stage Audit

Before CI is treated as sufficient, perform an explicit audit against the locked specification.

## D1. Specification audit

Check every requirement line by line.

For each requirement classify:

- PASS
- FAIL
- NOT IMPLEMENTED
- NOT TESTED
- OUT OF SCOPE

Do not mark PASS based only on intention or code comments.

## D2. Contract audit

Verify:

- schema
- field names
- field types
- state values
- missing-data behavior
- quality propagation
- versioning
- timestamps
- provenance

## D3. Boundary audit

Verify that the stage:

- consumes only permitted upstream data
- does not duplicate upstream calculations
- does not leak downstream responsibilities
- does not introduce an undeclared engine

## D4. Double-counting audit

Where several metrics represent the same economic fact, determine whether they are genuinely independent.

Do not treat repeated representations of one fact as independent votes.

## D5. Point-in-Time audit

For historical analysis verify:

```text
available_at <= cutoff
```

Use the information version that was actually available at the historical decision/calculation date.

## D6. Versioning audit

Verify that material analytical logic is reproducible through a model/specification version.

Old versions must remain distinguishable.

---

# 7. Phase E — CI

CI is the reproducible execution gate.

Minimum CI should:

1. checkout repository
2. install dependencies
3. run the complete test suite
4. fail on test failure

Example:

```yaml
- name: Run test suite
  env:
    PYTHONPATH: .
  run: |
    pytest src/tests -v
```

CI configuration must be version-controlled.

The final status must be based on an actual workflow result, not an assumption.

Important:

- A missing result is not a PASS.
- A local test run is not a substitute for CI evidence when CI is required.
- A PR-only workflow and a push workflow are different evidence sources.
- Verify the actual workflow trigger before interpreting an empty workflow query.

---

# 8. Phase F — Fix Loop

When an audit or CI failure occurs, use this loop:

```text
Failure
  ↓
Identify exact requirement
  ↓
Identify smallest responsible layer
  ↓
Fix implementation/spec/test
  ↓
Add or strengthen regression test
  ↓
Run full test suite
  ↓
Run CI
  ↓
Re-audit affected contract
```

Do not redesign the architecture merely because an implementation has a defect.

Do not weaken a correct specification to make the implementation pass.

Do not introduce unrelated improvements during a focused defect fix.

---

# 9. Phase G — Lock the Stage

A stage can be marked COMPLETE / LOCKED only when all are true:

- Specification = LOCKED
- Implementation = COMPLETE
- Tests = PASS
- Stage Audit = PASS
- CI = PASS
- Cross-stage contract = PASS
- No unresolved critical defect

Recommended status:

```text
Design: LOCKED
Implementation: COMPLETE
Testing: PASS
Audit: PASS
Overall: COMPLETE / LOCKED
```

Record:

- final audited commit
- CI workflow/run
- CI job
- test count
- audit result
- known non-blocking warnings

---

# 10. Phase H — Cross-Stage Integration Audit

After a stage is locked, verify the boundary with adjacent stages.

For each dependency answer:

### Upstream

- What exact contract is consumed?
- Is it consumed as-is?
- Is any calculation unnecessarily repeated?

### Downstream

- What exact contract is produced?
- Are all required fields present?
- Are missing/quality/version states preserved?

### Semantics

- Does the same economic fact appear multiple times?
- Could it be counted twice?
- Is there a hidden vote/bonus/score?

### Historical Integrity

- Does PIT remain intact?
- Can the result be reproduced?

---

# 11. Project-Level Final Audit

After the final stage is complete, perform a whole-project audit.

## Checklist

### Architecture

- All intended stages exist.
- Responsibilities remain separated.
- No unauthorized engine was introduced.
- Master Architecture remains authoritative.

### Data

- Source provenance is preserved.
- Raw data is not destroyed by normalization.
- Missing data is distinct from zero.
- Versioning is preserved.

### Contracts

- Every stage boundary is compatible.
- No downstream stage recreates upstream calculations unnecessarily.
- Required outputs exist.
- Data quality propagates correctly.

### PIT

- No future information leaks into historical calculations.
- Historical versions remain reproducible.

### Scoring

- Scores exist only where explicitly defined.
- No hidden scoring exists.
- Weighting does not double count correlated evidence.

### Forecasting

- Forecast versions remain reproducible.
- Forecast evaluation uses the correct historical information set.
- Reliability is not misused as an unrelated mathematical input.

### Valuation

- Valuation consumes forecast outputs through the defined contract.
- Invalid EPS does not create artificial valuation metrics.
- Benchmark populations are semantically compatible.

### Market

- Market analysis remains contextual when the architecture requires it.
- No hidden trading signal or market score exists.

### Decision

- Decision integration consumes evidence from upstream engines.
- Decision logic does not silently become a weighted score.
- Conflicts and confidence are explicit.
- History and hysteresis are preserved when required.

### External Context

- Different data types with different economic meanings remain distinct.
- Proxies are explicit.
- No silent substitution occurs.

### CI

- Full project suite passes.
- Final commit is identified.
- Workflow/run/job are identified.

---

# 12. Architecture Change Control

The Architecture Change Log is the only normal route for intentional architectural change.

A change proposal must contain:

```text
CHANGE-XXX — Short Title

Status:
Version:
Date:
Affected Stage(s):

Previous Rule:
New Rule:

Reason:
Evidence / Trigger:

Architecture Impact:
Contract Impact:
Downstream Impact:

Migration Required:
Testing Required:

Approval:
Notes:
```

## Not normally an architecture change

- bug fix
- refactoring
- performance improvement
- database index
- code organization
- test improvement
- parameter tuning inside an existing model version

## Potential architecture change

- adding/removing a stage
- changing stage responsibility
- changing an inter-stage contract
- changing a fundamental data-model assumption
- changing a locked KPI definition
- changing scoring architecture
- changing valuation architecture
- changing decision architecture
- introducing a new required data source
- changing a core interpretation of an external variable

---

# 13. Specification Change Control

Not every specification correction is an architecture change.

If the architecture remains valid but a locked stage contract must change:

1. identify the exact contract change
2. explain why the existing specification is insufficient/incorrect
3. identify affected implementation
4. identify affected tests
5. identify downstream contracts
6. update version metadata
7. re-run audit and CI
8. record the change history

Never silently edit a locked specification.

---

# 14. Implementation Status Template

Use a status file that separates design, implementation, testing, and audit.

Recommended table:

| Stage | Design | Implementation | Testing | Audit | Overall |
|---|---|---|---|---|---|
| Stage 1 | LOCKED | COMPLETE | PASS | PASS | COMPLETE / LOCKED |
| Stage 2 | LOCKED | COMPLETE | PASS | PASS | COMPLETE / LOCKED |
| Stage N | LOCKED | IN PROGRESS | PENDING | PENDING | IN PROGRESS |

Project-level fields:

```text
Architecture:
Architecture Version:
Implementation:
Testing:
Whole-Project Audit:
Overall Status:
Final Audited Commit:
Final CI Workflow:
Final CI Run:
Final CI Job:
Final Test Count:
```

---

# 15. Stage Locked Specification Template

Every stage should have a standalone specification containing at least:

```text
# STAGE N — <NAME>

## LOCKED SPECIFICATION

Status:
Version:
Purpose:

## 1. Scope

## 2. Responsibilities

## 3. Inputs

## 4. Outputs

## 5. Core Definitions

## 6. Calculation Rules

## 7. Missing Data Rules

## 8. Data Quality Rules

## 9. Point-in-Time Rules

## 10. Versioning Rules

## 11. Cross-Stage Contract

## 12. Double-Counting Controls

## 13. Explicit Exclusions

## 14. Acceptance Criteria

## 15. Test Requirements

## 16. Audit Requirements
```

---

# 16. Standard New-Stage Execution Prompt

Use the following process when starting a new stage:

```text
We are implementing Stage N: <NAME>.

Use the existing Master Architecture and all previously locked stage specifications as authoritative.

Do not redesign the architecture unless a genuine architectural contradiction is discovered.

Process strictly in this order:

1. Read the Master Architecture.
2. Read the relevant upstream/downstream locked specifications.
3. Read the current Implementation Status.
4. Define/verify the Stage N Locked Specification.
5. Audit the specification for scope leakage and contract gaps.
6. Lock the specification.
7. Inspect the current implementation.
8. Implement only the locked contract.
9. Add/replace tests for the contract, edge cases, integration, and prohibited behavior.
10. Run the complete test suite.
11. Perform a formal stage audit against the specification.
12. Fix only the smallest responsible defect.
13. Run the complete test suite again.
14. Verify CI on the actual relevant workflow trigger.
15. Re-audit the affected contract after fixes.
16. Mark the stage COMPLETE / LOCKED only when Specification, Implementation, Tests, Audit, and CI all pass.
17. Record the final commit and CI evidence in Implementation Status.
18. Perform a cross-stage contract check before moving to the next stage.

Never:
- invent requirements
- silently change locked architecture
- silently change a locked contract
- weaken tests just to obtain green CI
- introduce hidden scoring
- duplicate upstream calculations without justification
- silently substitute missing data
- use future data in historical calculations
- claim CI success without actual evidence
```

---

# 17. Standard Stage Completion Record

At completion record:

```text
Stage:
Specification Version:
Implementation Commit:
Test Count:
Audit Result:
CI Workflow:
CI Run:
CI Job:
CI Result:
Warnings:
Final Status:
```

Then explicitly verify:

```text
Cross-Stage Contract: PASS
Point-in-Time: PASS
Versioning: PASS
Data Quality: PASS
Double Counting: PASS
Scope Boundary: PASS
```

---

# 18. Final Project Completion Gate

The project is complete only when:

```text
Architecture             = LOCKED
All Stage Specifications = LOCKED
All Implementations      = COMPLETE
Full Test Suite          = PASS
All Stage Audits         = PASS
Cross-Stage Audit        = PASS
Whole-Project Audit      = PASS
CI                       = PASS
Implementation Status    = COMPLETE / LOCKED
```

Only after this gate may a new project phase begin.

---

# 19. Lessons Embedded in This Template

This template intentionally captures the main process lessons learned during Analyzer V1:

1. **Specification must precede implementation.**
2. **A passing test suite does not prove contract completeness.**
3. **Audit must be explicit and requirement-driven.**
4. **Implementation defects should normally be fixed without redesigning architecture.**
5. **Tests must check forbidden behavior as well as desired behavior.**
6. **Cross-stage contracts require their own audit.**
7. **Point-in-Time correctness must be treated as a system-wide invariant.**
8. **Versioning is required for reproducibility.**
9. **Missing data must never be silently converted into a convenient assumption.**
10. **Repeated economic evidence must not become double-counted votes.**
11. **CI evidence must be verified from the actual workflow/run.**
12. **A stage is not locked until implementation, tests, audit, and CI agree.**
13. **The final project requires a whole-project audit, not just a collection of successful stage tests.**
14. **The development process itself should be reusable and version-controlled.**

---

# 20. Template Status

**Template Type:** Reusable Development Process

**Origin:** Analyzer V1 development experience

**Purpose:** Standardize future staged software/analytical projects

**Architecture Definition:** None — project-specific

**Required Adaptation:** Stage names, contracts, tests, CI environment, and domain-specific rules must be customized per project.

**Status:** READY FOR REUSE
