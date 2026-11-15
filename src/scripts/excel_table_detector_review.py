"""Owner-run Markdown review of visual table candidates in representative XLSX files.

This utility is diagnostic only. It never changes source workbooks or persists
observations. A text-contract-invalid workbook is still rejected for ingestion,
but its literal-text cells may be used for a clearly labelled detector preview.
"""
from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from src.ingestion.excel.dto import CellValueKind
from src.ingestion.excel.reader import (
    ExcelSourceContractError,
    ExcelSourceReadError,
    read_excel_file,
)
from src.ingestion.excel.table_detector import detect_visual_table_candidates


def _print_contract_violations(observation: object, sample_limit: int) -> None:
    invalid_cells = [
        cell for cell in observation.cells
        if cell.value_kind in (
            CellValueKind.UNEXPECTED_NON_TEXT,
            CellValueKind.ERROR_VALUE,
        )
    ]
    print(f"- Text-only contract violations: **{len(invalid_cells)} cells**")

    by_sheet = Counter(cell.cell_ref.worksheet_ordinal for cell in invalid_cells)
    for worksheet_ordinal, count in sorted(by_sheet.items()):
        print(f"  - Worksheet {worksheet_ordinal}: {count} cells")

    by_type = Counter(
        (cell.value_kind.value, cell.data_type)
        for cell in invalid_cells
    )
    print("- Violation types:")
    for (kind, data_type), count in sorted(by_type.items()):
        print(f"  - {kind} / Excel data_type={data_type!r}: {count}")

    print(f"- First {min(sample_limit, len(invalid_cells))} example coordinates:")
    for cell in invalid_cells[:sample_limit]:
        value = repr(cell.unexpected_value)
        if len(value) > 70:
            value = value[:67] + "..."
        print(
            f"  - Sheet {cell.cell_ref.worksheet_ordinal}!"
            f"{cell.cell_ref.coordinate}: kind={cell.value_kind.value}, "
            f"data_type={cell.data_type!r}, number_format={cell.number_format!r}, "
            f"value={value}"
        )


def _print_candidates(observation: object) -> None:
    detected = detect_visual_table_candidates(observation)
    print(f"- Tables/candidates in diagnostic preview: {len(detected.tables)}")

    for sheet in detected.worksheets:
        print(
            f"\n### Worksheet {sheet.ordinal}: {sheet.literal_name} "
            f"({sheet.visibility.value})"
        )
        sheet_tables = [
            table for table in detected.tables
            if table.worksheet_ordinal == sheet.ordinal
        ]
        if not sheet_tables:
            print("- No visual table candidates.")
            continue

        print("| Ordinal | Bounds | Status | Title evidence | Diagnostics |")
        print("|---:|---|---|---|---|")
        for table in sheet_tables:
            titles = "; ".join(
                fragment.literal_text or ""
                for fragment in table.title_fragments
            ).replace("|", "\\|")
            diagnostics = "; ".join(
                item.code for item in table.diagnostics
            )
            print(
                f"| {table.table_ordinal} | {table.bounds.a1_range} "
                f"| {table.status.value} | {titles or '—'} "
                f"| {diagnostics or '—'} |"
            )


def _print_workbook(path: Path, sample_limit: int) -> None:
    print(f"\n## {path.as_posix()}")

    try:
        observation = read_excel_file(path)
    except ExcelSourceContractError as exc:
        observation = exc.observation
        print("- Reader result: **REJECTED** — text-only source contract violation.")
        print(f"- Source SHA-256: {observation.source.sha256}")
        print(f"- Observed cells: {len(observation.cells)}")
        _print_contract_violations(observation, sample_limit)
        print(
            "- Detector result: **DIAGNOSTIC PREVIEW ONLY**. "
            "The preview uses literal-text cells from a rejected workbook; "
            "it does not make the workbook eligible for ingestion."
        )
        _print_candidates(observation)
        return
    except ExcelSourceReadError as exc:
        print(f"- Reader result: **ERROR** — {exc.code}: {exc}")
        return

    print("- Reader result: **ACCEPTED**")
    print(f"- Source SHA-256: {observation.source.sha256}")
    print(f"- Observed cells: {len(observation.cells)}")
    print(f"- Worksheets: {len(observation.worksheets)}")
    _print_candidates(observation)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print visual table detector candidates for XLSX source files."
    )
    parser.add_argument(
        "workbooks",
        nargs="+",
        type=Path,
        help="One or more representative .xlsx paths.",
    )
    parser.add_argument(
        "--sample-limit",
        type=int,
        default=12,
        help="Maximum non-text cell examples printed per workbook (default: 12).",
    )
    args = parser.parse_args()
    if args.sample_limit < 0:
        parser.error("--sample-limit must be zero or greater")

    for path in args.workbooks:
        if not path.is_file():
            print(f"\n## {path.as_posix()}\n- File not found.")
            continue
        _print_workbook(path, args.sample_limit)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
