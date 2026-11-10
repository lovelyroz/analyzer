# CODAL Excel Preprocessing — Master Working Packet

## 1. Purpose and authority

This Master Working Packet governs the design, implementation, testing, and future maintenance of the standalone CODAL Excel preprocessing utility for Analyzer.

Its purpose is to standardize downloaded CODAL Excel workbooks **before** they enter the financial extraction/ingestion workflow.

The utility is an operational preprocessing tool. It is **not** a new analytical stage, financial-data extractor, metric mapper, or database ingestion engine.

This packet is the working authority for this utility's scope, task sequence, decisions, open questions, evidence, and completion status. It does not replace the Analyzer Master Architecture, Database Contract, or financial report standards.

**Current status: DESIGN IN PROGRESS — NO IMPLEMENTATION AUTHORIZED YET.**

## 2. Core operating principles

1. The user controls which company folder is processed on each run.
2. The utility must process only the explicitly supplied company folder; it must not crawl the entire `codal` tree or discover other companies.
3. Company identity and industry are determined from the selected folder path and the central company registry, not from workbook filenames, sheet names, workbook contents, or layout similarity.
4. Original input files must remain unchanged. The user decides when to delete them.
5. Converted workbooks are written to a separate `processed` output tree.
6. Input files are `.xls` files whose payload is HTML-formatted CODAL report content, not native binary XLS workbooks. The utility must parse that HTML-based representation and generate a genuine XLSX workbook; changing the extension is not conversion.
7. Processing must be deterministic, observable, safe to rerun, and must never silently overwrite an existing output.
8. The utility must not extract financial facts, infer financial periods, classify metrics, or write to the database. Those responsibilities belong to later stages.

## 3. Confirmed owner decisions

### 3.1 Input folder layout

The user's current layout is:

```text
codal/
└── bank/
    └── saman/
        ├── monthly/
        └── quarterly/
```

The user supplies the company folder, for example:

```text
codal/bank/saman/
```

The utility recursively scans **only that supplied company folder**.

It must not scan sibling company folders, the industry folder, or the complete `codal` tree.

### 3.2 Report types

There are exactly two CODAL financial report types in this preprocessing scope:

| Type code | Folder name | Meaning |
|---|---|---|
| `01` | `monthly` | Monthly activity report |
| `02` | `quarterly` | Quarterly/cumulative financial report |

The quarterly category includes reports covering 3, 6, 9, and 12 months. These are not four separate report types.

A workbook's actual financial period (for example, 3-month, 6-month, 9-month, or 12-month) is separate metadata. The preprocessing filename code identifies the report category, not the exact period length.

The presence of monthly and quarterly source values within one workbook must not cause the utility to split the workbook into multiple reports. The utility only converts and assigns an identity.

### 3.3 Company registry and company codes

- Company codes do not currently exist as a complete preassigned catalogue.
- The user wants to control company registration and add companies manually in the future.
- A central `companies.json` registry will hold industry and company codes and human-readable names.
- The utility must not silently invent or assign a code to an unknown company.
- If the selected company folder cannot be resolved unambiguously through the registry, processing must stop with a clear error.
- Registry changes are manual and owner-controlled.

Company codes are unique **within their industry**, not globally across all industries.
- The company identity is therefore the combination of industry code and company code.
- Example: company code `01` may be used by one bank and also by one cement company, because their industry codes differ.

### 3.4 Output naming convention

The agreed filename structure is:

```text
II-CC-TT-NNNN.xlsx
```

| Segment | Length | Meaning |
|---|---:|---|
| `II` | 2 digits | Industry code |
| `CC` | 2 digits | Company code |
| `TT` | 2 digits | Report type: `01` monthly, `02` quarterly |
| `NNNN` | 4 digits | Sequential report number |

Illustrative example only:

```text
01-01-01-0001.xlsx
01-01-01-0002.xlsx
01-01-02-0001.xlsx
```

The initial V1 industry-code catalogue is approved and fixed as follows:

| Industry code | Industry key | Name |
|---|---|---|
| `01` | `BANK` | Bank |
| `02` | `INVESTMENT` | Investment |
| `03` | `PETROCHEMICAL` | Petrochemical |
| `04` | `METALS` | Metals |
| `05` | `CEMENT` | Cement |
| `06` | `FOOD` | Food |
| `07` | `PHARMACEUTICAL` | Pharmaceutical |

These codes are stable identifiers and must not be renumbered if the catalogue is extended. A newly supported industry receives the next available two-digit code. Company-code uniqueness is also locked: codes are unique within an industry, and the pair `II-CC` identifies a company.

The working numbering rule is an independent sequence for each company and report type. For example, a company's monthly sequence and quarterly sequence each start at `0001`. Sequence allocation is based on output files currently present: the utility must choose an available number and must never overwrite an existing output. If the user deletes processed outputs after database import, those numbers may be reused in a later run; output filenames are temporary processing identifiers, not permanent database identities.

### 3.5 Input filenames and deterministic ordering

- Input files in V1 are `.xls`-extension files containing HTML-formatted report content. The `.xls` extension does not mean that the payload is a native binary XLS workbook.
- Input filenames are not standardized and must never be used to identify the company or report type.
- Input filenames may be Persian, irregular, duplicated across different subfolders, or contain unusual characters.
- The utility enumerates eligible workbooks under the supplied company folder and sorts them by their **relative paths from that company folder**, not by absolute paths.
- For sorting only, each relative path is normalized to Unicode NFC. This normalization must not rename or otherwise modify the actual source file or path.
- The normalized relative paths are compared using Unicode code-point lexicographic ordering. Sorting is case-sensitive; no locale-dependent collation is used.
- If two distinct original relative paths become equal after NFC normalization, their original, unnormalized relative paths are compared using Unicode code-point lexicographic ordering as the final tie-breaker.
- Output sequence numbers are assigned according to this deterministic order, independently within each company/report-type sequence.
- A failed conversion must not be recorded as a successfully created output or consume a sequence number within that run.

### 3.6 Output location and source preservation

Converted files are stored separately under a `processed` tree, preserving the industry/company hierarchy. Example:

```text
processed/
└── bank/
    └── saman/
        ├── 01-01-01-0001.xlsx
        ├── 01-01-01-0002.xlsx
        └── 01-01-02-0001.xlsx
```

- Original XLS files remain in their input folders.
- The utility must not delete, move, rename, or modify original inputs.
- The user manually deletes input files later, after checking the processed outputs.
- Existing output files must never be overwritten silently.
- The user manually deletes input and processed output files after checking/importing the data into the database.
- No permanent processing history is required because the source and processed workbooks are temporary and are deleted by the user after successful import.

## 4. Proposed execution contract

The intended high-level execution is:

```text
User supplies one company-folder path
        |
        v
Validate the supplied folder and resolve its industry/company
        |
        v
Load and validate companies.json
        |
        v
Recursively enumerate eligible workbooks under that folder
        |
        v
Determine each report type from its monthly/quarterly folder ancestry
        |
        v
Sort eligible inputs deterministically
        |
        v
Parse each HTML-based `.xls` input and generate a genuine XLSX workbook
        |
        v
Assign the next valid identifier and standard filename
        |
        v
Write to processed/<industry>/<company>/
        |
        v
Validate output and record run results
```

This is a design outline, not an implementation mandate for a particular library or command-line interface.

### 4.1 Folder classification

The report type is determined from the path beneath the selected company folder:

- Files under a `monthly` directory belong to type `01`.
- Files under a `quarterly` directory belong to type `02`.
- Nested subdirectories beneath either folder are allowed.
- A file outside either recognized report-type subtree, or a file whose path yields conflicting classifications, must not be processed as a valid report. It must be reported as skipped/rejected with a reason.

### 4.2 HTML-based XLS input to genuine XLSX output

The owner has clarified that V1 does not receive native `.xlsx` inputs. The downloaded files have an `.xls` extension, but their contents are HTML-formatted CODAL report data. This mismatch between filename extension and actual payload format was the source of parsing difficulties and is the reason for the preprocessing step.

Accordingly, this is not a conventional native-XLS-to-XLSX conversion task. The utility must:
- read and parse the HTML payload contained in each `.xls` input;
- interpret the report's HTML table structure sufficiently to construct a genuine `.xlsx` workbook;
- preserve the report's tabular structure, cell values, and relevant row/column relationships as faithfully as the source permits;
- explicitly handle and report unsupported, malformed, ambiguous, or lossy cases rather than silently claiming full fidelity;
- validate that the resulting file is a genuine XLSX package that can be opened by an XLSX reader;
- never merely rename the `.xls` file or wrap its unchanged HTML payload in an `.xlsx` extension.

The parsing/conversion library and exact fidelity strategy have not yet been selected. They must be evaluated against representative CODAL inputs before implementation.

### 4.3 Output numbering and failure behavior

- Numbering is independent for each company and report type.
- At the start of a run, the utility inspects the relevant processed-output directory and allocates available four-digit numbers without overwriting existing files.
- Monthly and quarterly sequences remain separate.
- Failed conversions do not consume a successful-output number.
- A partially written output must be removed or clearly quarantined before the run continues.
- An existing output must never be overwritten.
- If the user has deleted all processed outputs after importing them into the database, numbering may start again at `0001` in a later run. The filename is a temporary processing identifier, not a permanent record identifier.
- If the same source is processed again while its previous output still exists, the utility may produce another output under a different available number. V1 does not promise cross-run source-to-output deduplication.

### 4.4 Run report and rerun behavior

- No permanent `processing_manifest.json` is required in V1.
- The utility may keep temporary run state in memory and produce a run report for the current execution.
- The run report must identify every input as converted, skipped, or failed, with a reason, and should include the generated output filename where applicable.
- The user may retain the run report temporarily for review and then delete it with the processed workbooks.
- SHA-256 source hashing, duplicate-content detection, and persistent source-to-output history are out of scope for V1.
- Rerun safety means preventing output overwrite and handling partial files safely; it does not mean guaranteeing that a source file will never be processed twice across separate executions.
- If a run is interrupted, the next run inspects the output directory, avoids existing filenames, and allocates other available numbers. It does not attempt to reconstruct a permanent processing history.

## 5. Central registry — preliminary shape

A JSON registry is approved in principle. The following is an illustrative shape only; actual company assignments are owner-controlled. The initial industry catalogue is finalized. Company codes are unique within each industry, while the industry/company code pair is unique across the registry.

```json
{
  "industries": {
    "bank": {
      "code": "01",
      "name": "Bank"
    }
  },
  "companies": {
    "bank/saman": {
      "code": "01",
      "name": "Bank Saman"
    },
    "bank/saderat": {
      "code": "02",
      "name": "Bank Saderat"
    }
  }
}
```

Registry requirements:
- codes are strings, preserving leading zeroes;
- industry and company codes must have exactly two decimal digits;
- duplicate industry codes must be rejected; company codes must be unique within their own industry, but may repeat in another industry;
- unknown industries or companies must cause a clear stop, not an inferred default;
- manual registry edits must be validated before processing;
- registry format should include a schema/version field before it is treated as a production contract.

## 6. Scope boundaries

### In scope

- one user-supplied company folder per execution;
- recursive discovery within that folder only;
- classification as monthly or quarterly from folder ancestry;
- manual company/industry registry lookup;
- deterministic input ordering;
- parsing HTML-based `.xls` inputs and generating genuine XLSX workbooks;
- standard output naming;
- separate processed output tree;
- collision prevention, rerun safety, and execution reporting.

### Explicitly out of scope

- crawling all companies or all of `codal`;
- automatic company identification from workbook content or filename;
- automatic creation of company codes;
- deleting or modifying source workbooks;
- extracting financial values or report periods;
- deciding whether a quarterly report contains standalone or year-to-date values;
- mapping rows/columns to financial metrics;
- validating financial semantics;
- database writes or migrations;
- changing downstream financial extraction/ingestion contracts.

## 7. Open design decisions — must resolve before implementation

| ID | Question | Current status |
|---|---|---|
| PREP-OPEN-001 | Are company codes unique globally or only within an industry? | CLOSED — unique within each industry; `II-CC` identifies the company. |
| PREP-OPEN-002 | What are the initial two-digit industry codes? | CLOSED — codes `01`–`07` assigned to BANK, INVESTMENT, PETROCHEMICAL, METALS, CEMENT, FOOD, PHARMACEUTICAL respectively; future additions receive the next available code and existing codes never change. |
| PREP-OPEN-003 | What exact sorting rule is used for Persian/Unicode filenames and nested paths? | CLOSED — sort by relative path; normalize to NFC for comparison only; compare normalized paths using case-sensitive Unicode code-point lexicographic order; use the original relative path as the tie-breaker when normalized paths are equal. |
| PREP-OPEN-004 | How are sequence numbers persisted and recovered after reruns? | CLOSED — no persistent sequence history; allocate around outputs currently present, and allow reuse after the user deletes outputs. |
| PREP-OPEN-005 | Should a manifest map source hashes/paths to prior outputs to prevent duplicate processing? | CLOSED — no permanent manifest or cross-run content deduplication in V1; use temporary in-memory state and a per-run report only. |
| PREP-OPEN-006 | What should happen when an input is already XLSX rather than XLS? | CLOSED — V1 inputs are `.xls`-extension files containing HTML-formatted CODAL report content; native XLSX input is not part of the current input contract. |
| PREP-OPEN-007 | Which conversion engine is reliable in the user's Windows environment, and what fidelity limits apply? | OPEN |
| PREP-OPEN-008 | What exact CLI/user interaction supplies and validates the company-folder path? | OPEN |
| PREP-OPEN-009 | What is the policy if a workbook is found outside monthly/quarterly, or both classifications appear in its ancestry? | OPEN |
| PREP-OPEN-010 | What happens when the 4-digit sequence reaches 9999? | OPEN |

No implementation should begin while any open decision that affects identity, collision safety, conversion correctness, or data loss remains unresolved.

## 8. Documentation alignment required

The repository contains earlier CODAL documents that describe PDF extraction or use older monthly/accumulated terminology. The Excel preprocessing direction and the owner's clarified two-category model must be reconciled with those documents through explicit, reviewed amendments.

At minimum, review:
- `10_Production_Codal_Extraction_and_Data_Load.md`;
- `DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md`, especially its Excel/PDF transition and report-type sections;
- relevant Stage 1 / database ingestion contracts where the preprocessing output identity or file format affects their interface.

This packet does not silently supersede or rewrite those documents. Any required change must be recorded explicitly and must preserve the existing financial-data and database contracts unless an approved change is necessary.

## 9. Task plan and status

Status legend:
- `[x]` DONE — entire task completed with evidence.
- `[~]` PARTIAL — some work is complete, but a decision or evidence remains.
- `[ ]` OPEN — not started.
- `[!]` BLOCKED — cannot proceed without an external decision or dependency.

### Phase A — Design

- [~] PREP-001 — Record the owner's scope, folder, report-type, naming, and source-preservation decisions. The current packet records them; open details remain.
- [x] PREP-002 — Finalize industry and company code policy. Company codes are unique within industry; the initial seven industry codes are approved and stable.
- [x] PREP-003 — Finalize deterministic sorting and sequence allocation. Relative-path ordering, NFC comparison normalization, Unicode code-point ordering, original-path tie-breaking, and independent available-number allocation are specified.
- [x] PREP-004 — Finalize rerun/idempotency and manifest policy. No permanent manifest or cross-run deduplication; protect existing outputs, allocate available numbers, and produce a temporary per-run report.
- [ ] PREP-005 — Select and validate the HTML-based `.xls` to genuine XLSX parsing/conversion approach.
- [ ] PREP-006 — Finalize the command-line/user interaction and execution report contract.
- [ ] PREP-007 — Reconcile affected repository documentation.
- [ ] PREP-008 — Audit the complete preprocessing specification and obtain owner approval.
- [ ] PREP-009 — Freeze the V1 specification.

### Phase B — Implementation (not authorized yet)

- [ ] PREP-101 — Implement registry loading and validation.
- [ ] PREP-102 — Implement explicit company-folder validation and bounded recursive enumeration.
- [ ] PREP-103 — Implement monthly/quarterly path classification and deterministic ordering.
- [ ] PREP-104 — Implement safe parsing of HTML-based `.xls` inputs and generation of genuine XLSX workbooks.
- [ ] PREP-105 — Implement identifier allocation, output naming, and collision protection.
- [ ] PREP-106 — Implement output-collision/partial-file safety and temporary per-run state/report; do not implement a permanent processing manifest in V1.
- [ ] PREP-107 — Implement execution report and failure handling.

### Phase C — Verification (not authorized yet)

- [ ] PREP-201 — Add tests for path boundaries and prove sibling companies are never scanned.
- [ ] PREP-202 — Add tests for monthly/quarterly classification, nested folders, and invalid paths.
- [ ] PREP-203 — Add tests for unusual Persian/Unicode filenames, duplicate names in different folders, and deterministic ordering.
- [ ] PREP-204 — Add tests for conversion validity and unsupported/lossy workbook cases.
- [ ] PREP-205 — Add tests for numbering, collisions, failed conversions, and reruns.
- [ ] PREP-206 — Verify source XLS files remain unchanged and are never deleted.
- [ ] PREP-207 — Perform a requirement-by-requirement audit and record actual test evidence.

## 10. Implementation and workflow rules

- Design must be reviewed and approved before implementation.
- Do not modify database schema, migrations, financial extraction logic, or downstream ingestion as part of this utility unless a separate approved task explicitly requires it.
- The user runs tests locally unless explicitly authorizing otherwise. Provide exact commands; do not claim tests were run without evidence.
- Keep implementation changes limited to the approved file scope.
- Do not edit `WORKFLOW_RULES.md`.
- Do not mark a task complete based on intent, a prompt, or code presence alone.
- Any change to an approved decision must be recorded as an explicit amendment with reason and impact; do not silently rewrite prior decisions.

## 11. Current completion state

```text
Packet: CREATED — WORKING DRAFT
Design: IN PROGRESS
Owner approval of complete specification: PENDING
Implementation: NOT STARTED
Tests: NOT STARTED
Audit: NOT STARTED
Overall: DESIGN IN PROGRESS
```

The next action is to resolve the remaining open design decisions with the owner, then audit and freeze the specification. No code changes are authorized by this packet yet.
