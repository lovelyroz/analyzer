"""Owner-run Markdown review of visual table candidates in representative XLSX files.

This utility does not modify source workbooks or persist observations. It prints
compact Markdown so the owner can paste the output into reply.md for review.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from src.ingestion.excel.reader import (
    ExcelSourceContractError,
    ExcelSourceReadError,
    read_excel_file,
)
from src.ingestion.excel.table_detector import detect_visual_table_candidates


def _print_workbook(path: Path) -> None:
    print(f"\n## {path.as_posix()}")

    try:
        observation = read_excel_file(path)
    except ExcelSourceContractError as exc:
        observation = exc.observation
        print("- Reader result: **REJECTED** — text-only source contract violation.")
        diagnostics = [
            diagnostic
            for cell in observation.cells
            for diagnostic in cell.diagnostics
        ]
        diagnostics.extend(observation.diagnostics)
        for diagnostic in diagnostics:
            print(f"  - {diagnostic.code}: {diagnostic.message}")
        return
    except ExcelSourceReadError as exc:
        print(f"- Reader result: **ERROR** — {exc.code}: {exc}")
        return

    detected = detect_visual_table_candidates(observation)
    print("- Reader result: **ACCEPTED**")
    print(f"- Source SHA-256: {observation.source.sha256}")
    print(f"- Observed cells: {len(observation.cells)}")
    print(f"- Worksheets: {len(observation.worksheets)}")
    print(f"- Tables/candidates: {len(detected.tables)}")

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
            print("- No table candidates.")
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
    args = parser.parse_args()

    for path in args.workbooks:
        if not path.is_file():
            print(f"\n## {path.as_posix()}\n- File not found.")
            continue
        _print_workbook(path)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
