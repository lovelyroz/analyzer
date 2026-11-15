# DB-AUD-008 — Excel Library Capability Assessment

**Date:** 2026-11-15  
**Status:** PARTIAL — repository inventory, documentation comparison, and a synthetic openpyxl probe utility are in place; the utility has not been executed, Calamine comparison and source-workbook validation remain open.  
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

## 7. Decision status

- `openpyxl`: **provisional primary candidate**.
- `python-calamine`: **secondary candidate requiring feature spike**.
- `pandas`: **not selected as the observation adapter**; may be considered downstream only after structural interpretation.
- Production dependency changes, Python DTO classes, production adapter code, ORM/schema/migrations, and data changes: **not authorized or performed by this assessment**. The standalone spike utility is diagnostic-only.

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

**Execution note:** The assessment report and a standalone synthetic spike utility were added and then statically corrected/extended with a runtime package inventory. The utility was not executed. No source XLSX was directly inspected, no package was installed or upgraded, no production ingestion code/DTO/ORM/schema/migration/data was changed, and no tests were run.
