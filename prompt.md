# Task 060 — S7-AUD-011
## Fzar PDF Extraction Failure Audit — PDFium Evidence-Based Evaluation

**Task Type: AUDIT-ONLY / REPORT-ONLY**

**ABSOLUTE RESTRICTION: DO NOT MODIFY ANY FILE. DO NOT IMPLEMENT ANY FIX. DO NOT RUN TESTS.**

You are the local engineering audit agent for the repository:

`analyzer`

This is a financial-data application. Financial correctness, deterministic behavior, traceability, and preservation of source data are mandatory.

Your task is to investigate the actual Fzar PDF extraction failure and evaluate the PDFium extraction path using the real source PDF.

You must follow the project's current instructions and constraints in:

1. `STAGE7_HANDOFF_INSTRUCTION.md`
2. `STAGE7_MASTER_WORKING_PACKET.md`
3. `WORKFLOW_RULES.md`
4. `STAGE7_COMPLETED_CHECKLIST.md`

These documents are the governing project references. Do not replace their decisions with assumptions or recommendations from previous reports.

---

## 1. Scope and permitted files

The following repository files are explicitly authorized for inspection:

- `src/tests/test_codal_extraction.py`
- `src/ingestion/codal/pdf_extract.py`
- `src/ingestion/codal/parser.py`
- `src/ingestion/codal/adapter.py`

The original source PDF is also authorized as an audit input:

- `pdf/Fzar.pdf` (provided locally by the user)

You may inspect the contents and visual layout of `Fzar.pdf`.

Do not inspect or modify unrelated repository files.

If you need to inspect another repository file to establish a fact, do not access it yet. Instead, report:

- Exact file path required
- Exact information you need from it
- Why the four authorized source files are insufficient
- Which audit conclusion cannot be established without it

Do not install, upgrade, or change any package or dependency.

You may inspect the locally available PDFium installation and its existing version, if accessible without modifying the environment. If it is not available, report that fact. Do not install it.

---

## 2. Mandatory restrictions

You MUST NOT:

- Modify production code.
- Modify tests.
- Modify project documentation.
- Create or edit files inside the repository.
- Install or upgrade packages.
- Change dependency declarations.
- Run pytest or any other project test suite.
- Commit, push, or create branches.
- Claim that a fix has been implemented.
- Infer a root cause without direct supporting evidence.
- Treat successful text extraction alone as proof of successful financial table extraction.

This task is strictly an investigation and reporting task.

You may execute read-only diagnostic operations on the supplied PDF and inspect the existing local environment.

Your final report must be returned directly in your response to the user. Do not save it into the repository.

---

## 3. Audit objective

Determine where the Fzar extraction pipeline fails, based on evidence from the actual PDF and the authorized source code.

The audit must distinguish these three stages:

**Stage A — Source PDF characteristics**

What information and structure are actually present in the original PDF?

**Stage B — PDF extraction**

What does the extraction engine actually return from the PDF?

**Stage C — Application mapping**

How does the application transform the extracted information into financial records, especially `item_name` and numeric values?

Do not combine these stages into one general statement such as "Persian PDF extraction fails."

---

## 4. Required investigation

### A. Inspect the actual Fzar PDF

Inspect the document visually and programmatically.

Identify and report:

- Number of pages.
- Relevant pages containing monthly sales or financial tables.
- Whether text is selectable or the document is image-based.
- Persian text encoding and character integrity.
- RTL text direction and reading order.
- Table structure and visible row/column boundaries.
- Whether cell positions can be identified reliably.
- Persian and Latin digits, if present.
- Decimal separators, thousands separators, negative values, and units.
- Product/item names and their relationship to their corresponding numeric values.

Use actual page numbers and representative examples.

Do not assume that extracted text order is the same as visual reading order.

### B. Evaluate PDFium

Use the existing local PDFium capability, if available, to inspect the original Fzar PDF.

Evaluate these dimensions independently:

1. Persian character integrity.
2. RTL reading order.
3. Table and row reconstruction.
4. Cell coordinates and bounding boxes.
5. Relationship between product names and numeric values.
6. Preservation of digits, decimal separators, and units.

For each dimension, provide:

- A representative example from the original PDF.
- The corresponding PDFium output.
- Whether the result is correct, partially correct, or incorrect.
- Evidence supporting that assessment.

If PDFium is unavailable, clearly report `NOT EVALUABLE` for the affected checks. Do not simulate or invent PDFium output.

Do not conclude that PDFium is suitable merely because it extracts readable Persian text.

### C. Audit the existing application extraction path

Inspect the four authorized source files.

Trace the actual path used by the application from the PDF input to the final `RawLineInput` records.

Specifically establish:

- Which extraction engine is called first.
- What conditions cause fallback to another engine.
- How table rows and cells are represented.
- How text lines and numeric tokens are identified.
- How Persian item labels are detected.
- How `item_name` is selected and normalized.
- How numeric values are parsed.
- How the adapter determines the extraction backend.
- What happens when no usable records are extracted.

Do not assume that `parser.py` is part of the production adapter path. Verify actual function calls and imports.

For every important conclusion, provide the exact file path, function name, and line numbers.

### D. Compare source PDF, PDFium output, and application mapping

Select representative rows from Fzar.

For each selected row, compare:

1. What is visibly present in the original PDF.
2. What PDFium extracts, including coordinates where available.
3. What the existing application extraction path produces.
4. What `item_name` and numeric values the adapter ultimately assigns.

Use a comparison table.

Include both successful and failed examples where possible.

If a comparison cannot be performed, state precisely why.

### E. Determine the failure location

Based on the evidence, classify the observed failure into one or more of these categories:

- Source PDF limitation.
- Text extraction failure.
- RTL or reading-order failure.
- Table reconstruction failure.
- Cell-coordinate or row-association failure.
- Persian text normalization failure.
- Item-name detection/mapping failure.
- Numeric token parsing failure.
- Adapter integration failure.
- Insufficient evidence.

Multiple categories may apply.

Do not force a single root cause if the evidence supports multiple independent failures.

---

## 5. Evidence and confidence requirements

Every material conclusion must be supported by evidence.

For source-code claims, provide:

- File path.
- Function or method name.
- Line numbers.
- Relevant behavior.

For PDF claims, provide:

- Page number.
- Representative visible text or table row.
- Corresponding extraction output.

For environment claims, provide:

- Available package or engine name.
- Version, if verifiable.
- Whether the capability was actually tested on Fzar.

Use these evidence labels:

- `CONFIRMED`: Directly established by inspected source or actual output.
- `PARTIALLY CONFIRMED`: Some supporting evidence exists, but the complete behavior is not established.
- `UNVERIFIED`: Not established.
- `NOT EVALUABLE`: The required input or capability was unavailable.

Never present an assumption as a confirmed finding.

If a prior failure log or diagnostic output is not available locally, state that limitation. Do not reconstruct it from memory.

---

## 6. Required final report structure

Return the report using exactly these sections:

### 1. Executive Summary
A concise statement of what was established and what remains unknown.

### 2. Environment and PDFium Availability
Report PDFium availability and version, if verifiable. State whether the actual Fzar PDF was processed.

### 3. Fzar PDF Characteristics
Describe the actual source document and relevant pages.

### 4. PDFium Evaluation
Report the six independent evaluation dimensions from Section 4B.

### 5. Existing Application Pipeline
Describe the verified production extraction path, including function names and line references.

### 6. Representative Row Comparison
Provide a table comparing source PDF, PDFium output, existing extraction output, and final mapping.

### 7. Failure Classification
List confirmed, partially confirmed, unverified, and non-evaluable failure categories.

### 8. Root-Cause Assessment
State the most defensible conclusion supported by evidence. If root cause cannot yet be established, say so explicitly.

### 9. Additional Evidence Required
List only the exact additional files, logs, or permissions needed to complete the audit. Explain why each is necessary.

### 10. Recommended Next Step
Recommend the next investigation or a separate implementation task, but do not implement it.

### 11. Task Status
Report:

`060 · S7-AUD-011: DONE` only if all feasible audit requirements were completed and evidence is sufficient.

Otherwise report:

`060 · S7-AUD-011: PARTIAL`

or:

`060 · S7-AUD-011: BLOCKED`

Explain every unresolved item.

---

## 7. Final verification statement

End your report with an explicit declaration:

- No repository files were modified.
- No production code was changed.
- No tests were executed.
- No packages were installed or upgraded.
- No commits or pushes were made.

If any restriction was inadvertently violated, disclose it clearly.

**Important:** This audit does not authorize implementation. The user and project decision-maker must review the evidence and explicitly approve any subsequent code-change task.

### Architecture Boundary

The final analyzer application must extract and process CODAL PDF data independently at runtime, without requiring ChatGPT, Luna, GapCode, an AI agent, or any external PDF-assistant skill.

External PDF skills and tools may only be used as diagnostic instruments during this audit.

Their output must never be treated as proof that the production application can perform the same extraction.

Any proposed production solution must identify the exact libraries, dependencies, integration points, and runtime behavior required within the analyzer application itself.