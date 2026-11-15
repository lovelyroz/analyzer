"""Generate a synthetic XLSX and report openpyxl observation capabilities.

This is an opt-in engineering spike utility, not a pytest test module and not
part of the production ingestion path. Run explicitly with:
    python src/scripts/excel_reader_feature_spike.py

It creates only a temporary workbook and writes a JSON report to stdout.
It never opens or modifies CODAL/source workbooks and never calculates formulas.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import importlib.util
import json
import tempfile
import time
import tracemalloc
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from openpyxl import Workbook, load_workbook
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.utils.datetime import CALENDAR_MAC_1904


MAIN_SHEET_XML = "xl/worksheets/sheet1.xml"
NS = {"x": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
ET.register_namespace("", NS["x"])


# Module import names and distribution names differ for several Excel engines.
_READER_PACKAGES = {
    "openpyxl": ("openpyxl",),
    "python_calamine": ("python_calamine",),
    "pandas": ("pandas",),
    "xlrd": ("xlrd",),
    "pyxlsb": ("pyxlsb",),
    "odfpy": ("odf",),
    "fastexcel": ("fastexcel",),
}


def _installed_reader_packages() -> dict:
    """Report this interpreter's installed reader-related distributions.

    requirements.txt is a declared-dependency snapshot, not an inventory of
    packages manually installed into the active Python environment.
    """
    inventory = {}
    for distribution, modules in _READER_PACKAGES.items():
        try:
            version = importlib.metadata.version(distribution)
            installed = True
        except importlib.metadata.PackageNotFoundError:
            version = None
            installed = False

        module_available = any(
            importlib.util.find_spec(module_name) is not None
            for module_name in modules
        )
        inventory[distribution] = {
            "distribution_installed": installed,
            "version": version,
            "import_module_available": module_available,
        }
    return inventory


def _patch_formula_cache_and_numeric_token(source: Path, destination: Path) -> None:
    """Patch synthetic worksheet XML to model a cached formula result and raw token."""
    with ZipFile(source, "r") as zin, ZipFile(destination, "w", ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            payload = zin.read(item.filename)
            if item.filename == MAIN_SHEET_XML:
                root = ET.fromstring(payload)
                for cell in root.findall(".//x:c", NS):
                    coordinate = cell.attrib.get("r")
                    if coordinate == "D2":
                        formula = cell.find("x:f", NS)
                        value = cell.find("x:v", NS)
                        if formula is None:
                            raise RuntimeError("Synthetic formula cell D2 is missing <f>.")
                        if value is None:
                            value = ET.SubElement(cell, f"{{{NS['x']}}}v")
                        value.text = "1"
                    elif coordinate == "C2":
                        value = cell.find("x:v", NS)
                        if value is None:
                            raise RuntimeError("Synthetic numeric cell C2 is missing <v>.")
                        value.text = "123.4500"
                payload = ET.tostring(root, encoding="utf-8", xml_declaration=True)
            zout.writestr(item, payload)


def _make_synthetic_workbook(path: Path) -> None:
    workbook = Workbook()
    workbook.epoch = CALENDAR_MAC_1904

    main = workbook.active
    main.title = "Main"
    main.append(["Metric", "Zero", "NumericToken", "Formula", "Date", "Error", "Boolean"])
    main.append(["Revenue", 0, 123.45, "=B2+1", datetime(2024, 1, 1), "#N/A", True, "=B2+2"])
    main["F2"].data_type = "e"
    main.merge_cells("A4:B4")
    main["A4"] = "Merged multi-level header"
    main.row_dimensions[6].hidden = True
    main.column_dimensions["H"].hidden = True

    table = Table(displayName="SyntheticFacts", ref="A1:G2")
    table.tableStyleInfo = TableStyleInfo(
        name="TableStyleMedium2",
        showFirstColumn=False,
        showLastColumn=False,
        showRowStripes=True,
        showColumnStripes=False,
    )
    main.add_table(table)

    hidden = workbook.create_sheet("HiddenSheet")
    hidden.sheet_state = "hidden"
    hidden.append(["Metric", "Value"])
    hidden.append(["HiddenMetric", 7])
    hidden_table = Table(displayName="HiddenSheetFacts", ref="A1:B2")
    hidden.add_table(hidden_table)

    very_hidden = workbook.create_sheet("VeryHiddenSheet")
    very_hidden.sheet_state = "veryHidden"
    very_hidden["A1"] = "very hidden content"

    workbook.save(path)


def _cell_observation(cell) -> dict:
    return {
        "coordinate": cell.coordinate,
        "value": cell.value.isoformat() if isinstance(cell.value, datetime) else cell.value,
        "data_type": cell.data_type,
        "number_format": cell.number_format,
    }



def _date_epoch_observations(root: Path) -> dict:
    """Compare the same calendar date stored under both Excel date systems."""
    observations = {}
    for label, epoch in (
        ("1900", None),
        ("1904", CALENDAR_MAC_1904),
    ):
        path = root / f"date_system_{label}.xlsx"
        workbook = Workbook()
        if epoch is not None:
            workbook.epoch = epoch
        sheet = workbook.active
        sheet.title = "DateSystem"
        sheet["A1"] = datetime(2024, 1, 1)
        workbook.save(path)
        workbook.close()

        loaded = load_workbook(path, data_only=False, read_only=False)
        with ZipFile(path, "r") as archive:
            sheet_root = ET.fromstring(archive.read(MAIN_SHEET_XML))
            date_serial = None
            for cell in sheet_root.findall(".//x:c", NS):
                if cell.attrib.get("r") == "A1":
                    value = cell.find("x:v", NS)
                    date_serial = value.text if value is not None else None
                    break
        observations[label] = {
            "workbook_epoch": loaded.epoch.isoformat(),
            "cell_value": loaded["DateSystem"]["A1"].value.isoformat(),
            "raw_date_serial": date_serial,
        }
        loaded.close()
    observations["same_calendar_value"] = (
        observations["1900"]["cell_value"] == observations["1904"]["cell_value"]
    )
    observations["serials_differ"] = (
        observations["1900"]["raw_date_serial"] != observations["1904"]["raw_date_serial"]
    )
    return observations


def _repeatability_observation(path: Path, expected: dict) -> dict:
    """Read identical immutable XLSX bytes twice and compare stable observations."""
    raw_bytes = path.read_bytes()
    fingerprint_first = hashlib.sha256(raw_bytes).hexdigest()
    first = load_workbook(path, data_only=False, read_only=False)
    first_cached = load_workbook(path, data_only=True, read_only=False)
    first_projection = {
        "epoch": first.epoch.isoformat(),
        "sheet_states": [
            (sheet.title, sheet.sheet_state) for sheet in first.worksheets
        ],
        "merged_ranges": sorted(str(item) for item in first["Main"].merged_cells.ranges),
        "table_names_and_refs": sorted(
            (
                name,
                first["Main"].tables[name].ref
                if hasattr(first["Main"].tables[name], "ref")
                else str(first["Main"].tables[name]),
            )
            for name in first["Main"].tables
        ),
        "formula": first["Main"]["D2"].value,
        "cached_value": first_cached["Main"]["D2"].value,
        "formula_without_cache": first_cached["Main"]["H2"].value,
        "numeric_value": first["Main"]["C2"].value,
        "coordinates": sorted(
            cell.coordinate
            for row in first["Main"].iter_rows()
            for cell in row
            if cell.value is not None
        ),
    }
    first.close()
    first_cached.close()

    fingerprint_second = hashlib.sha256(path.read_bytes()).hexdigest()
    second = load_workbook(path, data_only=False, read_only=False)
    second_cached = load_workbook(path, data_only=True, read_only=False)
    second_projection = {
        "epoch": second.epoch.isoformat(),
        "sheet_states": [
            (sheet.title, sheet.sheet_state) for sheet in second.worksheets
        ],
        "merged_ranges": sorted(str(item) for item in second["Main"].merged_cells.ranges),
        "table_names_and_refs": sorted(
            (
                name,
                second["Main"].tables[name].ref
                if hasattr(second["Main"].tables[name], "ref")
                else str(second["Main"].tables[name]),
            )
            for name in second["Main"].tables
        ),
        "formula": second["Main"]["D2"].value,
        "cached_value": second_cached["Main"]["D2"].value,
        "formula_without_cache": second_cached["Main"]["H2"].value,
        "numeric_value": second["Main"]["C2"].value,
        "coordinates": sorted(
            cell.coordinate
            for row in second["Main"].iter_rows()
            for cell in row
            if cell.value is not None
        ),
    }
    second.close()
    second_cached.close()

    return {
        "same_input_sha256": fingerprint_first == fingerprint_second,
        "input_sha256": fingerprint_first,
        "same_observation_projection": first_projection == second_projection,
        "reader_version": expected["openpyxl_version"],
        "comparison_scope": "two independent loads of the same immutable synthetic XLSX bytes",
    }

def _make_large_synthetic_workbook(path: Path, row_count: int) -> None:
    """Create a deterministic, value-only workbook for an opt-in load benchmark."""
    workbook = Workbook(write_only=True)
    sheet = workbook.create_sheet("LargeSheet")
    sheet.append(["row_id", "metric", "value", "period", "flag", "description"])
    for row_number in range(1, row_count + 1):
        sheet.append([
            row_number,
            "Revenue" if row_number % 2 else "Cost",
            row_number * 1.25,
            "1405/01",
            row_number % 2 == 0,
            f"Synthetic benchmark row {row_number}",
        ])
    workbook.save(path)


def _large_sheet_benchmark(root: Path, row_count: int) -> dict:
    """Measure normal-mode openpyxl load time and Python-tracked peak memory."""
    path = root / f"large_sheet_{row_count}_rows.xlsx"
    _make_large_synthetic_workbook(path, row_count)
    file_size_bytes = path.stat().st_size

    tracemalloc.start()
    started = time.perf_counter()
    workbook = load_workbook(path, data_only=False, read_only=False)
    loaded_at = time.perf_counter()
    current_after_load, peak_after_load = tracemalloc.get_traced_memory()

    sheet = workbook["LargeSheet"]
    non_empty_cells = sum(
        1
        for row in sheet.iter_rows()
        for cell in row
        if cell.value is not None
    )
    scanned_at = time.perf_counter()
    current_after_scan, peak_after_scan = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    result = {
        "enabled": True,
        "requested_data_rows": row_count,
        "observed_max_row_including_header": sheet.max_row,
        "observed_max_column": sheet.max_column,
        "observed_non_empty_cells": non_empty_cells,
        "xlsx_file_size_bytes": file_size_bytes,
        "load_elapsed_seconds": round(loaded_at - started, 6),
        "load_peak_tracemalloc_bytes": peak_after_load,
        "load_current_tracemalloc_bytes": current_after_load,
        "load_and_scan_elapsed_seconds": round(scanned_at - started, 6),
        "load_and_scan_peak_tracemalloc_bytes": peak_after_scan,
        "load_and_scan_current_tracemalloc_bytes": current_after_scan,
        "memory_measurement": (
            "Python allocations tracked by tracemalloc; native allocations outside "
            "Python's allocator may not be fully represented."
        ),
        "reader_mode": "normal",
        "reader_version": importlib.metadata.version("openpyxl"),
    }
    workbook.close()
    return result


def run_spike(benchmark_rows: int = 0) -> dict:
    with tempfile.TemporaryDirectory(prefix="excel-reader-spike-") as temp_dir:
        root = Path(temp_dir)
        generated = root / "generated.xlsx"
        patched = root / "synthetic_spike.xlsx"
        _make_synthetic_workbook(generated)
        _patch_formula_cache_and_numeric_token(generated, patched)

        raw_bytes = patched.read_bytes()
        fingerprint = hashlib.sha256(raw_bytes).hexdigest()

        formula_book = load_workbook(patched, data_only=False, read_only=False)
        cached_book = load_workbook(patched, data_only=True, read_only=False)

        main = formula_book["Main"]
        cached_main = cached_book["Main"]
        formula_cell = main["D2"]
        cached_cell = cached_main["D2"]

        with ZipFile(patched, "r") as archive:
            xml_root = ET.fromstring(archive.read(MAIN_SHEET_XML))
            raw_numeric_token = None
            for cell in xml_root.findall(".//x:c", NS):
                if cell.attrib.get("r") == "C2":
                    value = cell.find("x:v", NS)
                    raw_numeric_token = value.text if value is not None else None
                    break

        reader_packages = _installed_reader_packages()
        date_epoch_comparison = _date_epoch_observations(root)
        repeatability = _repeatability_observation(patched, {"openpyxl_version": reader_packages["openpyxl"]["version"] or "unknown"})
        large_sheet_benchmark = (
            _large_sheet_benchmark(root, benchmark_rows)
            if benchmark_rows > 0
            else {"enabled": False, "reason": "Pass --benchmark-rows to opt in."}
        )
        openpyxl_version = reader_packages["openpyxl"]["version"] or "unknown"
        calamine_available = reader_packages["python_calamine"]["import_module_available"]

        result = {
            "utility": "excel_reader_feature_spike",
            "workbook_sha256": fingerprint,
            "workbook_epoch": formula_book.epoch.isoformat(),
            "date_epoch_comparison": date_epoch_comparison,
            "repeatability": repeatability,
            "large_sheet_benchmark": large_sheet_benchmark,
            "openpyxl_version": openpyxl_version,
            "python_calamine_installed": calamine_available,
            "reader_package_inventory": reader_packages,
            "dependency_inventory_note": (
                "Reflects the interpreter running this utility; packages installed "
                "manually and absent from requirements.txt are reported when present."
            ),
            "sheet_states": [
                {"title": sheet.title, "state": sheet.sheet_state}
                for sheet in formula_book.worksheets
            ],
            "merged_ranges": sorted(str(item) for item in main.merged_cells.ranges),
            "tables": {
                name: (
                    main.tables[name].ref
                    if hasattr(main.tables[name], "ref")
                    else str(main.tables[name])
                )
                for name in main.tables
            },
            "formula_view": _cell_observation(formula_cell),
            "cached_value_view": _cell_observation(cached_cell),
            "formula_without_cache": {
                "formula": main["H2"].value,
                "cached_value": cached_main["H2"].value,
            },
            "formula_cache_pair": {
                "formula": formula_cell.value,
                "cached_value": cached_cell.value,
                "same_coordinate": formula_cell.coordinate == cached_cell.coordinate,
            },
            "sample_cells": {
                coordinate: _cell_observation(main[coordinate])
                for coordinate in ("A2", "B2", "C2", "E2", "F2", "G2")
            },
            "raw_numeric_xml_token": raw_numeric_token,
            "numeric_library_value": main["C2"].value,
            "hidden_row_6": main.row_dimensions[6].hidden,
            "hidden_column_H": main.column_dimensions["H"].hidden,
            "non_empty_coordinates": sorted(
                cell.coordinate
                for row in main.iter_rows()
                for cell in row
                if cell.value is not None
            ),
            "notes": [
                "Synthetic fixture only; no source workbook was opened.",
                "No formula was calculated; cached value was injected into synthetic XLSX XML.",
                "Raw numeric token is read from worksheet XML for comparison with the library scalar.",
                "This utility reports observations; it does not assert pass/fail or modify project data.",
                "1900/1904 comparison uses separate synthetic workbooks with the same calendar date.",
                "Repeatability compares two independent loads of the same immutable synthetic XLSX bytes.",
            ],
        }

        formula_book.close()
        cached_book.close()
        return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the synthetic Excel reader feature spike.")
    parser.add_argument(
        "--benchmark-rows",
        type=int,
        default=0,
        help="Opt in to a synthetic large-sheet load benchmark with this many data rows.",
    )
    arguments = parser.parse_args()
    if arguments.benchmark_rows < 0:
        parser.error("--benchmark-rows must be zero (disabled) or a positive integer.")
    print(json.dumps(
        run_spike(benchmark_rows=arguments.benchmark_rows),
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    ))
