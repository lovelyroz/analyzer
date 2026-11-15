"""Generate a synthetic XLSX and report openpyxl observation capabilities.

This is an opt-in engineering spike utility, not a pytest test module and not
part of the production ingestion path. Run explicitly with:
    python src/scripts/excel_reader_feature_spike.py

It creates only a temporary workbook and writes a JSON report to stdout.
It never opens or modifies CODAL/source workbooks and never calculates formulas.
"""
from __future__ import annotations

import hashlib
import importlib.metadata
import importlib.util
import json
import tempfile
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
    hidden.append(["Metric", "Value"])\n    hidden.append(["HiddenMetric", 7])\n    hidden_table = Table(displayName="HiddenSheetFacts", ref="A1:B2")\n    hidden.add_table(hidden_table)

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


def run_spike() -> dict:
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

        try:
            openpyxl_version = importlib.metadata.version("openpyxl")
        except importlib.metadata.PackageNotFoundError:
            openpyxl_version = "unknown"

        calamine_available = importlib.util.find_spec("python_calamine") is not None

        result = {
            "utility": "excel_reader_feature_spike",
            "workbook_sha256": fingerprint,
            "workbook_epoch": formula_book.epoch.isoformat(),
            "openpyxl_version": openpyxl_version,
            "python_calamine_installed": calamine_available,
            "sheet_states": [
                {"title": sheet.title, "state": sheet.sheet_state}
                for sheet in formula_book.worksheets
            ],
            "merged_ranges": sorted(str(item) for item in main.merged_cells.ranges),
            "tables": {
                name: table.ref for name, table in main.tables.items()
            },
            "formula_view": _cell_observation(formula_cell),
            "cached_value_view": _cell_observation(cached_cell),\n            "formula_without_cache": {\n                "formula": main["H2"].value,\n                "cached_value": cached_main["H2"].value,\n            },
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
            ],
        }

        formula_book.close()
        cached_book.close()
        return result


if __name__ == "__main__":
    print(json.dumps(run_spike(), ensure_ascii=False, indent=2, sort_keys=True))
