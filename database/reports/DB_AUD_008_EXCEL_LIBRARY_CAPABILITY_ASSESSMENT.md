# DB-AUD-008 — Excel Library Capability Assessment

**Date:** 2026-11-15  
**Status:** COMPLETE for V1 reader-profile assessment — repository inventory, owner-run synthetic observations/benchmarks, and source-workbook evidence crosswalk from five Markdown audit reports are complete. The V1 baseline profile is selected below; Calamine comparison is optional and not a release prerequisite.  
**Scope:** Excel reader selection for the CODAL Excel ingestion V1 and the logical observation contract in DB-DES-007. This report is not an implementation approval.

## 1. Executive decision

**Selected primary choice: `openpyxl` normal mode.** It is already present in `requirements.txt` and its object model exposes the workbook, worksheet, cell, merged-range, style/number-format, formula, and worksheet structure needed by the observation DTO. Its `data_only` option provides access to the last cached value stored for formula cells, while the default mode exposes formula expressions. These are separate views and should be read in coordinated passes when formula cells are encountered.

**Alternative to benchmark: `python-calamine`.** It offers a Rust-backed reader, broad format support, worksheet metadata including visibility, merged ranges, and row iteration. Its documented Python surface is more value/table-oriented; the reviewed API does not establish a complete formula-expression plus cached-result pair, nor the same breadth of cell-level style/number-format inspection needed by DB-DES-007. It remains a candidate if performance or additional file formats become material.

**Not recommended as the primary observation adapter: pandas.** Its Excel interface is designed to materialize tabular DataFrames. That is useful after structural interpretation, but is not the appropriate first boundary for preserving merged headers, sparse coordinates, cell-level states, formulas, and row/column hierarchy.

The V1 baseline reader profile is selected in Section 7.8. The assessment does not approve a Python DTO/API, production adapter implementation, ORM/schema/migration changes, or data persistence design.

## 2. Repository inventory

- `requirements.txt` currently lists `openpyxl` alongside SQLAlchemy, pytest, pypdf, and jdatetime.
- No `pyproject.toml` or `setup.py` was found at the repository root in this review.
- `python-calamine` is not listed in the reviewed requirements file.
- The existing dependency is evidence of project declaration, not a complete inventory of the active Python environment. Packages installed manually and omitted from requirements.txt may still be available to the user running the utility.
- The four workbook patterns discussed in DB-AUD-002 and DB-AUD-007 are represented here only through their Markdown audit reports. The XLSX files were not directly opened during this task.

## 3. Capability comparison

| Requirement from DB-DES-007 | openpyxl | python-calamine | pandas Excel interface |
|---|---|---|---|
| XLSX / XLSM reading | Yes | Yes | Yes, via engine |
| Legacy XLS / XLSB / ODS | Not its target formats | Yes, documented | Supported through calamine engine |
| Workbook / worksheet enumeration | Yes | Yes | Yes, but exposed through tabular reader |
| Hidden / very-hidden worksheet state | Worksheet state is exposed by workbook model | Sheet metadata documents Visible / Hidden / VeryHidden | Not a primary DataFrame concern |
| Merged-cell ranges | Yes, worksheet merged ranges | Yes, merged ranges are exposed for XLSX/XLS | Not preserved as first-class cell structure in DataFrame output |
| Cell coordinates and sparse observations | Strong cell-addressable object model | Row/cell iteration and range bounds | DataFrame-oriented; coordinates need reconstruction |
| Formula expression | Yes, default `data_only=False` | Not established as a complete public Python cell observation in reviewed API | Not a reliable formula-observation contract |
| Cached formula result | Yes, `data_only=True`, if present in file | Formula/cache semantics need a dedicated spike | Not a suitable control surface |
| Formula calculation | No; formulas are not evaluated | No calculation engine | No calculation engine |
| Number format / style metadata | Exposed at cell level | Not established at equivalent depth in reviewed API | Mostly outside normal DataFrame output |
| Excel tables / named structures | Exposed through worksheet tables | Table names and table ranges are exposed in current API typing | Not a structural-first representation |
| Streaming / memory behavior | Read-only mode reduces memory, but feature availability is limited | Row iteration is available; whole-sheet conversion also exists | Reads into DataFrame structures |
| Numeric lexical fidelity | Python numeric values may surface as int/float; exact original numeric token is not guaranteed by ordinary cell.value | Numeric values may surface as int/float; exact original token not guaranteed by ordinary value API | Numeric values are converted into tabular scalar types |
| Fit for DB-DES-007 DTO | **Best current fit** | Promising secondary candidate; formula/style gaps require proof | Not suitable as primary adapter |

## 4. Material technical findings

### 4.1 Formula and cached-value handling

DB-DES-007 requires the adapter to preserve both the formula expression (diagnostic) and cached result/availability, without executing formulas.

- In openpyxl, `data_only=False` returns the formula expression; `data_only=True` returns the value last stored by an application such as Excel.
- The two observations require separate workbook loads. They must be aligned by worksheet identity and cell coordinate, and both loads must operate on the same immutable input bytes/fingerprint.
- openpyxl does not calculate formulas. A missing cached result must remain `FORMULA_NO_CACHE`, not be recalculated or replaced with zero.
- The four workbook samples summarized in DB-AUD-007 were reported as having no formulas. Therefore formula-cache behavior is a required capability from the DTO contract, not a feature demonstrated by those four samples.

### 4.2 Structure and worksheet metadata

The observation layer needs worksheet order/state, merged ranges, table regions, cell coordinates, number formats, and sparse row/column context. openpyxl provides a cell-oriented workbook model and merged ranges. Its read-only mode is useful for large sheets but does not expose every normal-mode feature; the initial adapter should not silently select read-only mode until a spike proves that all required structure remains observable.

python-calamine provides worksheet names, sheet metadata (including visibility), merged-cell ranges, table metadata, and row iteration. Its lower-level and faster reading path is attractive, but the reviewed Python API does not yet prove the full cell-level metadata and formula/cache behavior needed by the DTO.

### 4.3 Date system

The workbook date system (1900 versus 1904) is relevant metadata and must be preserved as observation evidence. It must not be interpreted as the company's Jalali financial period. openpyxl exposes the workbook epoch; Calamine also has a 1904-epoch capability in its underlying library. This is a library-level date-serial concern, not a replacement for DB-DES-003 temporal interpretation.

### 4.4 Numeric representation and Decimal

The canonical numeric rule requires Decimal parsing and one final ROUND_HALF_UP conversion. A normal openpyxl cell read may expose numeric content as Python int/float rather than the original XML numeric token. Converting a float with `Decimal(str(value))` avoids importing its binary expansion, but it does not prove preservation of the exact source token or trailing decimal scale.

The spike must therefore determine whether the DTO needs the original worksheet XML numeric text in addition to the library's typed value. Do not treat number format as a unit/scale instruction, and do not infer currency or magnitude conversion.

### 4.5 Unsupported or non-required workbook content

The reviewed DTO contract requires hidden-sheet visibility and explicit unsupported-feature diagnostics. The library must not silently omit a relevant hidden worksheet or formula cell. Macro execution, external-link resolution, and formula calculation are not required; the adapter is read-only and must not execute workbook content.

## 5. Recommendation and proposed reader profile

For the first implementation spike, use **openpyxl in normal (non-read-only) mode** as the baseline reader. Keep the input bytes immutable and fingerprint them once. If formula cells exist, open two views of the same bytes:

1. formula view: `data_only=False`;
2. cached-value view: `data_only=True`.

Join the two views by worksheet and coordinate. Preserve formula text, cached-value state, cell data type, number format, merged membership, worksheet visibility, table/range metadata, and workbook epoch. Never calculate formulas.

This is a provisional reader profile, not a final Python DTO design. For very large files, benchmark read-only mode separately and reject it if it drops required structural evidence. Keep python-calamine as a performance/format-coverage comparison candidate, not a second production dependency yet.

## 6. Required feature spike before implementation

The next bounded spike should use synthetic workbooks created specifically for validation (not the four source XLSX files, which were not directly inspected in this task) and should report pass/fail/evidence for:

1. multiple worksheets with visible, hidden, and very-hidden states;
2. merged multi-level headers and merged-cell anchor/inherited context;
3. multiple independent tables and Excel structured tables;
4. formula cells with a populated cache and formula cells without a cache;
5. blank, zero, text, error, date, boolean, and numeric cells;
6. 1900 and 1904 date systems;
7. sparse sheets, hidden rows/columns, and large-sheet memory behavior;
8. cell coordinates and deterministic row/column iteration;
9. numeric source-token fidelity versus Python float/int values;
10. repeatability for identical workbook bytes and reader version.

No source workbook should be changed. No formula should be executed. No test suite was run as part of this documentation assessment.

## 7.1 Spike utility prepared (not executed)

A standalone opt-in utility was added at `src/scripts/excel_reader_feature_spike.py`. It generates a temporary synthetic workbook and emits JSON observations for worksheet visibility, merged ranges, structured tables on multiple sheets, formula-expression versus cached-value views (including a formula without a cache), cell types, 1904 epoch, hidden rows/columns, coordinates, a raw XML numeric token, and a SHA-256 fingerprint. The fixture injects a cached formula result into its own generated XLSX package; it does not calculate a formula. It now reports installed distribution versions and import-module availability for `openpyxl`, `python-calamine`, `pandas`, `xlrd`, `pyxlsb`, `odfpy`, and `fastexcel`. This runtime inventory is read from the Python interpreter executing the utility, so manually installed packages absent from `requirements.txt` can be detected. The utility still does not import or benchmark Calamine.

The utility is deliberately not a pytest test and was not run in this task. Static review also corrected malformed literal newline escapes in the script source. The current fixture does not yet compare 1900 and 1904 workbooks, benchmark large-sheet memory/time, establish repeatability across separate runs, or validate Calamine behavior. Those remain open evidence items.


## 7.2 Compatibility correction from owner-run execution

The first owner-run execution exposed an `openpyxl` API compatibility issue: in the installed version, `main.tables.items()` yielded table references as strings, while the utility assumed each value was a `Table` object and accessed `.ref`. The utility was corrected to iterate table names and resolve each entry through `main.tables[name]`, accepting either a table object with `.ref` or a string-like reference. This is a source-level correction only; the corrected utility has not been executed by the assistant. The owner should rerun it and provide the resulting JSON so the next environment-specific issue, if any, can be assessed.

## 7. Decision status

- `openpyxl` normal mode: **selected V1 baseline observation reader**.
- `python-calamine`: **not selected for V1**; optional future comparison only if measured performance or format coverage creates a concrete need.
- `pandas`: **not selected as the observation adapter**; may be considered downstream only after structural interpretation.
- Production dependency changes, Python DTO classes, production adapter code, ORM/schema/migrations, and data changes: **not authorized or performed by this assessment**. The standalone spike utility is diagnostic-only.


## 7.3 Successful owner-run synthetic probe and environment inventory

The owner reran the corrected utility and placed its complete JSON output in repository-root `reply.md`. The run completed and emitted the expected JSON; the earlier `TableList.items()` compatibility failure did not recur. This is owner-provided execution evidence, not an assistant-run test.

Observed in the owner's executing interpreter:

| Distribution / import module | Installed / available | Version |
|---|---:|---:|
| `openpyxl` | Yes | 3.1.5 |
| `xlrd` | Yes | 2.0.2 |
| `python-calamine` / `python_calamine` | No | — |
| `pandas` | No | — |
| `pyxlsb` | No | — |
| `odfpy` | No | — |
| `fastexcel` | No | — |

The synthetic fixture observations include:

- Worksheet states `visible`, `hidden`, and `veryHidden` were emitted for Main, HiddenSheet, and VeryHiddenSheet.
- Merged range `A4:B4`, hidden row 6, and hidden column H were observed.
- Structured table `SyntheticFacts` was reported over `A1:G2`.
- At coordinate `D2`, the formula view returned `=B2+1` and the data-only view returned cached value `1`; the paired coordinate matched. A separate formula `=B2+2` had no cached value.
- Cell observations distinguished text, zero, numeric, date, error, and boolean values.
- Workbook epoch was `1904-01-01T00:00:00`.
- The library scalar for the numeric cell was `123.45`, while the raw worksheet XML token was `123.4500`; ordinary cell-value access therefore does not preserve the lexical trailing-zero representation.
- The fixture emitted SHA-256 `ef710da9f73f90e0b2c825bd7b254cdd9aad06f378f9410ad84b0bb3cda56758`.

**Interpretation and limits:** this confirms the corrected utility can complete against its synthetic fixture in the owner's environment and records the environment-specific package inventory. It does not establish behavior on CODAL source workbooks, compare the 1900 date system, demonstrate repeatability across independent runs, benchmark large-sheet time or memory, or compare Calamine. The output reports observations rather than pass/fail assertions; no formula was calculated, and no source workbook was opened.

The full owner-provided output is retained in repository-root `reply.md` as execution evidence. The assistant did not execute the utility or any tests.


## 7.4 Owner-run date-system and repeatability observations

The owner reran the enhanced utility and added its JSON output to repository-root `reply.md`. The emitted `date_epoch_comparison` reports:

| Workbook date system | Decoded calendar value | Raw worksheet XML date serial | Workbook epoch |
|---|---|---:|---|
| 1900 | `2024-01-01T00:00:00` | `45292` | `1899-12-30T00:00:00` |
| 1904 | `2024-01-01T00:00:00` | `43830` | `1904-01-01T00:00:00` |

The utility reports `same_calendar_value: true` and `serials_differ: true`. This confirms, for the synthetic fixtures and installed `openpyxl` version, that the same calendar date decodes consistently while its underlying serial differs by date system. The adapter must retain the workbook epoch and must not treat the raw serial as a date without that context.

The `repeatability` observation reports `same_input_sha256: true` and `same_observation_projection: true` for two independent loads of the same immutable synthetic XLSX bytes, using reader version `3.1.5` and input SHA-256 `fe97a73c7be51170e068ef9ae7671868b6ad54933078f2070764a3ef95f9ac2b`. This supports repeatability within one execution and one reader version only; it does not establish cross-process, cross-version, or cross-platform reproducibility.

**Evidence boundary:** these are owner-provided observations from synthetic workbooks, not direct inspection of CODAL source workbooks. The earlier fixture observations and interpreter inventory remain as recorded in section 7.3. Large-sheet elapsed-time/peak-memory benchmarking, practical Calamine comparison, and source-workbook validation remain open. The assistant did not execute the utility or any tests.

## 7.5 Owner-run large-sheet benchmark

The owner executed the opt-in benchmark with `--benchmark-rows 20000` under `openpyxl 3.1.5`. The synthetic value-only worksheet contained 20,000 data rows plus one header row and six columns (120,006 non-empty cells). The generated XLSX was 588,827 bytes.

| Observation | Owner-reported result |
|---|---:|
| Normal-mode workbook load | 6.545057 s |
| Load plus full cell traversal | 6.769802 s |
| Peak `tracemalloc` after load | 47,889,981 bytes (about 45.7 MiB) |
| Current `tracemalloc` after load | 46,093,935 bytes |
| Peak `tracemalloc` after load and traversal | 47,889,981 bytes |
| Current `tracemalloc` after load and traversal | 46,269,931 bytes |

These are single-run observations from the owner's environment, not a performance guarantee or a comparative benchmark. The memory figures track Python allocations through `tracemalloc`; native allocations outside Python's allocator may not be fully represented. No Calamine comparison was possible in this run because `python_calamine` was reported unavailable in that interpreter. The benchmark uses synthetic values and does not establish performance on representative CODAL workbooks. Repeated runs, a comparable Calamine run, and source-workbook validation remain open. The assistant did not execute the utility or benchmark.

## 8. Sources

- openpyxl tutorial and workbook loading options: https://openpyxl.readthedocs.io/en/stable/tutorial.html
- openpyxl reader API: https://openpyxl.readthedocs.io/en/stable/api/openpyxl.reader.excel.html
- openpyxl merged-cell behavior: https://openpyxl.readthedocs.io/en/stable/editing_worksheets.html
- openpyxl date systems: https://openpyxl.readthedocs.io/en/stable/datetime.html
- python-calamine README and Python usage: https://github.com/dimastbk/python-calamine
- python-calamine worksheet metadata / merged ranges API: https://github.com/dimastbk/python-calamine/blob/master/src/types/sheet.rs
- python-calamine Python type declarations: https://github.com/dimastbk/python-calamine/blob/master/python/python_calamine/_python_calamine.pyi
- pandas Excel I/O and calamine engine: https://pandas.pydata.org/docs/user_guide/io.html

---

**Execution note:** The standalone synthetic spike utility was executed by the owner in their environment; its JSON output is retained in repository-root `reply.md` and summarized in section 7.3. The assistant did not execute the utility or any tests. No source XLSX was directly inspected, no package was installed or upgraded, no production ingestion code/DTO/ORM/schema/migration/data was changed, and no tests were run.


## 7.6 Conditional same-file Calamine benchmark prepared

The standalone utility now includes an optional python-calamine large-sheet benchmark alongside the existing openpyxl benchmark. When --benchmark-rows N is supplied, both readers are measured against the **same generated XLSX file**. Calamine loads the workbook through CalamineWorkbook.from_path(path), obtains LargeSheet, and traverses its native iter_rows() iterator while counting non-empty scalar values. The report includes load time, load-plus-traversal time, observed range bounds, Python-tracked current/peak memory, and the installed distribution version.

If python_calamine is not importable, the utility emits calamine_large_sheet_benchmark.enabled: false with an explicit reason and continues normally; it does not install packages or fail solely because the optional reader is absent. If import succeeds but the comparative read fails, the failure is captured as an error observation.

**Comparison caveat:** both readers use the same generated file and count non-empty values, but their internal representations and allocation strategies differ. tracemalloc does not reliably account for native Rust allocations, so the memory values are not total process-memory measurements and must not be interpreted as a strict memory winner. This is a controlled indicative comparison, not a production acceptance test. The utility has only been edited; it has not been executed by the assistant or owner after this change. The current owner-reported environment previously lacked python-calamine, so the first rerun may report the optional comparison as unavailable until the owner makes that package available in the intended interpreter.

The public package usage reviewed for this implementation documents CalamineWorkbook.from_path(path), sheet_names, get_sheet_by_name(name), and sheet row iteration; see the [python-calamine package documentation](https://pypi.org/project/python-calamine/) and [Python API type declarations](https://github.com/dimastbk/python-calamine/blob/master/python/python_calamine/_python_calamine.pyi). No dependency declaration or installation was changed.


## 7.7 Second owner-run benchmark and repeatability of performance observations

The owner supplied a second execution in repository-root `reply.md`, again using `--benchmark-rows 20000` and `openpyxl 3.1.5`. The second run observed the same dimensions and non-empty cell count as the first run: 20,000 data rows, one header row, six columns, and 120,006 non-empty cells.

| Observation | First run | Second run |
|---|---:|---:|
| XLSX file size | 588,827 bytes | 588,828 bytes |
| Normal-mode load | 6.545057 s | 6.462552 s |
| Load plus full traversal | 6.769802 s | 6.679082 s |
| Peak `tracemalloc` after load | 47,889,981 bytes | 47,890,009 bytes |
| Current `tracemalloc` after load | 46,093,935 bytes | 46,094,009 bytes |
| Current `tracemalloc` after traversal | 46,269,931 bytes | 46,269,959 bytes |
| Peak `tracemalloc` after traversal | 47,889,981 bytes | 47,890,009 bytes |

The two observations are close in this owner's environment. They provide a modest repeat-run consistency check for this specific synthetic value-only workbook and openpyxl version; they do not establish a general performance distribution, a production capacity limit, or behavior on CODAL source workbooks. The one-byte file-size difference also indicates the generated XLSX package is not byte-identical between runs, so the earlier repeatability finding remains correctly scoped to two loads of the same immutable bytes within one run, not byte-for-byte deterministic fixture generation across runs.

The optional Calamine section reports `enabled: false` because `python_calamine` remains unavailable in the executing interpreter. Thus no comparative timing or memory result exists. The owner has not been asked to change project dependency declarations; package availability remains an optional environment decision. The source-workbook validation gap also remains open. These results were supplied by the owner in `reply.md`; the assistant did not execute the utility, benchmark, or tests.


## 7.8 Source-workbook evidence crosswalk (Markdown audit reports only)

This section evaluates the source-workbook evidence already transcribed in repository reports. The assistant did **not** open or inspect any XLSX file. The observations below are attributed to the existing audit reports, principally `DB-AUD-002_REAL_EXCEL_TEMPORAL_AUDIT.md` and `parsian_periodic_report_1.md`.

### 7.8.1 Evidence inventory

| Workbook evidence documented in Markdown | Reported structure | Reader implications |
|---|---|---|
| `cheshme.xlsx` | One visible worksheet; used range A1:V222; 76 merged ranges; no formulas, hidden rows/columns, or structured tables. Multiple portfolio, dividend, income, and investment tables coexist. | Must expose merged ranges and preserve local table/caption context; a worksheet is not equivalent to one table or one period. |
| `fzar.xlsx` | One visible worksheet; A1:Z63; 36 merged ranges; no formulas, hidden rows/columns, or structured tables. Production/sales, purchases, energy, and currency blocks use different grouped column layouts. | Must preserve multi-row merged headers and column coordinates; grouped measure and temporal labels must not be flattened or globally inherited. |
| `fzar2.xlsx` | One visible worksheet; A1:Z874; 168 merged ranges; no formulas, hidden rows/columns, or structured tables. Formal statements and appended schedules coexist; period labels differ between local tables. | Must support a large used range, multiple independent tables, and local temporal context; workbook-title period must not override table-local headers. |
| `samanBank.xlsx` | One visible worksheet; A1:M489; 103 merged ranges; no formulas, hidden rows/columns, or structured tables. Many independent tables include repeated date pairs, balance/flow/forecast labels, and row-level investee dates. | Must preserve row/column axes and distinguish dates in row attributes from column-period evidence. |
| `excel/parsian_periodic.xlsx` as described in `parsian_periodic_report_1.md` | One visible worksheet named `Recovered_Sheet1`; A1:L411; 101 merged ranges; no formulas, hidden rows/columns, structured tables, charts, images, or comments reported. Multiple formal statements and management schedules coexist. | Adds a formal interim financial-report example with dense merged headers and multiple statement/schedule contexts; supports the same normal-mode structural requirements. |

**Evidence boundary:** the first four workbook descriptions come from DB-AUD-002, while the Parsian example comes from its separate Markdown inspection report. These are report-derived observations, not a fresh independent inspection in DB-AUD-008. The Parsian report itself notes that the workbook body does not conclusively identify the reporting entity; the filename must not be used as issuer proof.

### 7.8.2 Capability fit against observed source patterns

| Observed requirement | openpyxl normal mode | Assessment |
|---|---|---|
| One worksheet containing many independent table regions | Cell-addressable worksheet model | Suitable as the low-level reader; table segmentation remains a separate deterministic layer, not a library feature to assume. |
| Merged and multi-level headers (present in all five documented examples) | Worksheet merged-range metadata and cell coordinates | Direct fit; preserve anchor/inherited relationships in the observation DTO. |
| Different period structures within one worksheet | Cell-level values, coordinates, and local ranges | Suitable to expose evidence; temporal interpretation remains outside the reader. |
| Sparse cells, row/column labels, and row-level dates | Cell-oriented access | Suitable; do not infer semantic role from cell type or date formatting. |
| Formula expression and cached value | Coordinated `data_only=False` and `data_only=True` views | Required by DTO even though none of these five reports records formula cells. |
| Hidden worksheets/rows/columns and structured tables | Workbook/worksheet metadata and table APIs | Required defensive capability; the five source reports do not demonstrate these features. Synthetic owner-run fixture observations provide limited library-level evidence. |
| Workbook date epoch | Workbook epoch metadata | Required technical context; the owner-run synthetic comparison covered 1900 and 1904 epochs, not the source reports' Jalali period semantics. |
| Exact numeric XML lexical token | Ordinary `cell.value` is not sufficient | Open issue: synthetic evidence showed `123.45` as the library scalar while the worksheet XML token was `123.4500`. If exact lexical representation is required, add a narrow read-only XML-token observation alongside openpyxl; do not infer it from number format. |
| Large worksheet behavior | Normal-mode synthetic benchmark only | Two owner runs at 20,000 rows were close, but do not establish source-workbook capacity or a general performance guarantee. |

### 7.8.3 Reader-profile conclusion

The five documented workbook patterns strengthen the case for **openpyxl normal (non-read-only) mode as the V1 baseline observation reader**. The common observed complexity is not multi-sheet or formula-heavy content; it is dense merged headers and many semantically independent tables within one worksheet. openpyxl's cell-addressable model and merged-range support align directly with that observed shape.

This is an approved bounded V1 reader-profile decision, not a claim that the library alone detects or interprets tables. The adapter/observation layer must still preserve multiple candidate table regions, row and column axes, local captions, merged-cell inheritance, cell coordinates, and unresolved ambiguity. It must not assign FinancialPeriod, metric, unit, or issuer identity.

The existing evidence does **not** justify switching to Calamine or adding it as a production dependency. Its benchmark remains optional and has not run because the owner's reported interpreter did not have `python_calamine`. Nor does the evidence justify selecting openpyxl read-only mode; its structural coverage remains unproven for this DTO.

**Remaining technical qualification:** decide whether raw worksheet XML numeric tokens (including trailing zeros) are part of the required transient observation contract. If yes, implement a small, read-only OOXML supplement keyed by worksheet and cell coordinate; keep openpyxl as the primary workbook model. This is not authorization to change production code or the DTO now.

### 7.8.4 Scope and completion status

- Source evidence validation against the existing Markdown reports: **completed for the five documented examples**, subject to the reports' own accuracy and without direct XLSX reinspection.
- Baseline reader profile: **openpyxl normal mode + read-only OOXML numeric-token sidecar**.
- Calamine comparative benchmark: not required for V1; revisit only if representative production-scale measurements or format requirements justify it.
- Multi-sheet, formula-cache, hidden-content, and structured-table behavior: not evidenced by the five source workbooks; retain synthetic coverage and explicit diagnostics.
- Numeric XML lexical fidelity: **resolved — preserve transiently; do not persist raw rows**.
- No production adapter, Python DTO, ORM, schema, migration, or data was changed. No package was installed. No test or benchmark was run by the assistant.


### 7.8.5 Final V1 profile decision

**Selected profile:**

1. Use `openpyxl` in normal (non-read-only) mode as the primary workbook/worksheet/cell reader.
2. Read formula and cached-value views from the same immutable input bytes when formulas are present; never calculate formulas.
3. Preserve workbook epoch, worksheet order/state, merged ranges, cell coordinates, cell types, number formats, and explicit structural diagnostics.
4. Add a narrow read-only OOXML pass to obtain original numeric `<v>` tokens keyed by worksheet and cell coordinate. Use these tokens as the exact lexical input for Decimal parsing where applicable; retain the typed openpyxl value as a parallel observation. This sidecar must not become a general raw-row archive.
5. Keep table segmentation, header-axis construction, semantic interpretation, temporal resolution, and admission outside the library reader.
6. Do not add `python-calamine` or `pandas` as V1 observation dependencies. Reconsider only with measured need.

**Task 030 completion:** the reader capability assessment and bounded profile selection are complete. This does not authorize production adapter/DTO implementation; those remain governed by their own tasks and contracts.


### 7.9 Owner-confirmed text-only V1 source contract (2026-11-15)

The owner confirms that all CODAL XLSX input files contain no formulas and that every populated cell is text-only. This confirmation supersedes the formula/cache and numeric-typed-cell assumptions in the earlier feature inventory and profile notes.

**Final V1 reader profile:**

- `openpyxl` normal mode, one structural/text observation pass.
- Preserve each populated cell's literal string exactly; do not normalize Persian/Arabic digits, separators, whitespace, signs, or punctuation in the reader.
- Preserve blanks as blanks; never coerce blank to zero or empty string.
- A populated non-text cell, formula, or Excel error is a contract violation: emit an error diagnostic and reject the report; do not coerce or read cached formula values.
- No formula/cache dual pass and no OOXML numeric-token sidecar.
- Parse numeric-looking/date-looking strings only in the later interpretation/validation layer using approved rules.
- Retain merged ranges, worksheet visibility/order, cell coordinates, and structural diagnostics. Table segmentation remains a separate deterministic layer.

The previously documented synthetic formula/cache and XML numeric-token spike remains historical capability evidence only; those capabilities are not part of the V1 reader contract. No additional package is required. This amendment does not authorize production persistence changes.
