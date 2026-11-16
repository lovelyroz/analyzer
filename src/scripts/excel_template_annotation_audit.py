"""Audit visual annotations in a standardized CODAL XLSX template.

This is a template-authoring utility, not a runtime report extractor. It validates
the workbook with the canonical Excel Reader, then reports color-coded cells,
thick-border edges, complete thick outside rectangles, and merged ranges.
It never changes the workbook or infers financial meaning.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from openpyxl import load_workbook

from src.ingestion.excel.reader import (
    ExcelSourceContractError,
    ExcelSourceReadError,
    read_excel_source,
)


def _color_descriptor(color: Any) -> str:
    if color is None:
        return "none"
    color_type = getattr(color, "type", None)
    parts = [f"type={color_type}"]
    for name in ("rgb", "indexed", "theme", "tint", "auto"):
        value = getattr(color, name, None)
        if value is not None:
            parts.append(f"{name}={value}")
    return ",".join(parts)


def _cell_color_signature(cell: Any) -> tuple[str, str]:
    font_color = _color_descriptor(getattr(cell.font, "color", None))
    fill = cell.fill
    fill_color = _color_descriptor(getattr(fill, "fgColor", None))
    return font_color, fill_color


def _thick(cell: Any, side: str) -> bool:
    border_side = getattr(cell.border, side, None)
    return getattr(border_side, "style", None) == "thick"


def _find_thick_outline_rectangles(worksheet: Any) -> list[str]:
    """Find rectangles whose four complete outside edges use the 'thick' style."""
    max_row = max(int(worksheet.max_row or 1), 1)
    max_column = max(int(worksheet.max_column or 1), 1)
    rectangles: set[tuple[int, int, int, int]] = set()

    for top in range(1, max_row):
        top_columns = [
            col for col in range(1, max_column + 1)
            if _thick(worksheet.cell(top, col), "top")
        ]
        left_columns = [
            col for col in top_columns
            if _thick(worksheet.cell(top, col), "left")
        ]
        for left in left_columns:
            right_columns = [
                col for col in top_columns
                if col > left and _thick(worksheet.cell(top, col), "right")
            ]
            for right in right_columns:
                for bottom in range(top + 1, max_row + 1):
                    if not (_thick(worksheet.cell(bottom, left), "bottom")
                            and _thick(worksheet.cell(bottom, right), "bottom")):
                        continue
                    if not all(_thick(worksheet.cell(top, col), "top")
                               and _thick(worksheet.cell(bottom, col), "bottom")
                               for col in range(left, right + 1)):
                        continue
                    if not all(_thick(worksheet.cell(row, left), "left")
                               and _thick(worksheet.cell(row, right), "right")
                               for row in range(top, bottom + 1)):
                        continue
                    rectangles.add((top, left, bottom, right))

    from openpyxl.utils import get_column_letter

    result = []
    for top, left, bottom, right in sorted(rectangles):
        start = f"{get_column_letter(left)}{top}"
        end = f"{get_column_letter(right)}{bottom}"
        result.append(start if start == end else f"{start}:{end}")
    return result


def audit_workbook(path: Path, *, max_color_cells: int) -> int:
    try:
        observation = read_excel_source(path)
    except ExcelSourceContractError as exc:
        print(f"READER: REJECTED CONTRACT: {exc}")
        for diagnostic in exc.observation.diagnostics:
            print(f"  {diagnostic.code}: {diagnostic.message} {diagnostic.cell_ref}")
        return 2
    except ExcelSourceReadError as exc:
        print(f"READER: REJECTED {exc.code}: {exc}")
        return 2

    print(f"## WORKBOOK {path}")
    print("Reader: ACCEPTED")
    print(f"SHA-256: {observation.source_artifact.sha256}")
    workbook = load_workbook(path, data_only=False, read_only=False, keep_links=False)
    try:
        for ordinal, worksheet in enumerate(workbook.worksheets, start=1):
            print(
                f"\n### SHEET {ordinal} {worksheet.title} "
                f"| used={worksheet.calculate_dimension()} "
                f"| merged={len(worksheet.merged_cells.ranges)}"
            )

            rectangles = _find_thick_outline_rectangles(worksheet)
            print(f"THICK_OUTSIDE_RECTANGLES count={len(rectangles)}")
            for bounds in rectangles:
                print(f"  OUTLINE {bounds}")

            print("MERGED_RANGES")
            for merged in sorted(str(item) for item in worksheet.merged_cells.ranges):
                print(f"  {merged}")

            print("COLOR_ANNOTATIONS")
            color_count = 0
            for row in worksheet.iter_rows():
                for cell in row:
                    font_color, fill_color = _cell_color_signature(cell)
                    has_color = (
                        font_color != "none"
                        or fill_color not in ("none", "type=rgb,rgb=00000000")
                    )
                    if not has_color:
                        continue
                    if color_count >= max_color_cells:
                        print(f"  TRUNCATED after {max_color_cells} color-coded cells")
                        break
                    value = repr(cell.value)
                    print(
                        f"  {cell.coordinate} value={value} data_type={cell.data_type} "
                        f"style_id={cell.style_id} font_color=[{font_color}] "
                        f"fill_color=[{fill_color}] fill_type={cell.fill.fill_type}"
                    )
                    color_count += 1
                if color_count >= max_color_cells:
                    break
            print(f"COLOR_CELLS_PRINTED={color_count}")

            print("THICK_BORDER_CELLS")
            thick_count = 0
            for row in worksheet.iter_rows():
                for cell in row:
                    sides = [
                        side for side in ("top", "bottom", "left", "right")
                        if _thick(cell, side)
                    ]
                    if not sides:
                        continue
                    print(
                        f"  {cell.coordinate} value={repr(cell.value)} "
                        f"thick_sides={','.join(sides)} style_id={cell.style_id}"
                    )
                    thick_count += 1
            print(f"THICK_BORDER_CELLS_COUNT={thick_count}")
    finally:
        workbook.close()
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read-only audit of visual table annotations in a standardized XLSX template."
    )
    parser.add_argument("workbook", type=Path)
    parser.add_argument("--max-color-cells", type=int, default=1000)
    args = parser.parse_args()
    if args.max_color_cells < 1:
        parser.error("--max-color-cells must be positive")
    return audit_workbook(args.workbook, max_color_cells=args.max_color_cells)


if __name__ == "__main__":
    raise SystemExit(main())
