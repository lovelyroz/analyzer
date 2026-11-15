# DB-AUD-008 — Excel Library Capability Assessment

**Date:** 2026-11-15  
**Status:** PARTIAL — repository inventory, documentation comparison, synthetic fixture observations, 1900/1904 epoch comparison, and same-input repeatability have been demonstrated by the owner in their environment. Large-sheet performance/memory, Calamine comparison, and source-workbook validation remain open.  
**Scope:** Excel reader selection for the CODAL Excel ingestion V1 and the logical observation contract in DB-DES-007. This report is not an implementation approval.

## 1. Executive decision

**Provisional primary choice: `openpyxl`.** It is already present in `requirements.txt` and its object model exposes the workbook, worksheet, cell, merged-range, style/number-format, formula, and worksheet structure needed by the observation DTO. Its `data_only` option provides access to the last cached value stored for formula cells, while the default mode exposes formula expressions. These are separate views and should be read in coordinated passes when formula cells are encountered.

**Alternative to benchmark: `python-calamine`.** It offers a Rust-backed reader, broad format support, worksheet metadata including visibility, merged ranges, and row iteration. Its documented Python surface is more value/table-oriented; the reviewed API does not establish a complete formula-expression plus cached-result pair, nor the same breadth of cell-level style/number-format inspection needed by DB-DES-007. It remains a candidate if performance or additional file formats become material.

**Not recommended as the primary observation adapter: pandas.** Its Excel interface is designed to materialize tabular DataFrames. That is useful after structural interpretation, but is not the appropriate first boundary for preserving merged headers, sparse coordinates, cell-level states, formulas, and row/column hierarchy.

No library is approved unconditionally. A small, controlled feature spike is still required before implementing the Python DTO or adapter.

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

- `openpyxl`: **provisional primary candidate**.
- `python-calamine`: **secondary candidate requiring feature spike**.
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
