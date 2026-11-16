"""Audit visual annotations in a standardized CODAL XLSX template.

This is a template-authoring utility, not a runtime report extractor. It validates
the workbook with the canonical Excel Reader, then reports color-coded cells,
thick-border edges, complete thick outside rectangles, and merged ranges.
It never changes the workbook or infers financial meaning.
"""
from __future__ import annotations

import argparse
from collections import Counter
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


def _cell_color_signature(cell: Any) -> tuple[str, str, bool]:
    font = getattr(cell.font, "color", None)
    fill = cell.fill
    fill_color_obj = getattr(fill, "fgColor", None)
    font_color = _color_descriptor(font)
    fill_color = _color_descriptor(fill_color_obj)

    # Ignore the common default black font and default no-fill values.
    font_is_default = (
        font is None
        or (getattr(font, "type", None) == "theme"
            and getattr(font, "theme", None) == 1
            and getattr(font, "tint", 0) in (None, 0, 0.0))
        or (getattr(font, "type", None) == "indexed"
            and getattr(font, "indexed", None) == 64)
    )
    fill_is_default = (
        fill_color_obj is None
        or (getattr(fill_color_obj, "type", None) == "rgb"
            and getattr(fill_color_obj, "rgb", None) in ("00000000", "000000"))
        or (getattr(fill_color_obj, "type", None) == "indexed"
            and getattr(fill_color_obj, "indexed", None) == 64)
    )
    return font_color, fill_color, not (font_is_default and fill_is_default)


def _border_style(cell: Any, side: str) -> str | None:
    border_side = getattr(cell.border, side, None)
    return getattr(border_side, "style", None)


def _thick(cell: Any, side: str) -> bool:
    return _border_style(cell, side) == "thick"


def _report_border_evidence(worksheet: Any) -> None:
    """Report actual per-cell border styles without assuming a table rectangle."""
    sides = ("top", "bottom", "left", "right")
    counts: dict[str, Counter[str]] = {side: Counter() for side in sides}
    entries: list[tuple[str, str, str]] = []
    for row in worksheet.iter_rows():
        for cell in row:
            for side in sides:
                style = _border_style(cell, side)
                if style is not None:
                    counts[side][style] += 1
                    entries.append((cell.coordinate, side, style))
    print("BORDER_SIDE_STYLE_COUNTS")
    for side in sides:
        summary = ", ".join(
            f"{style}={count}" for style, count in sorted(counts[side].items())
        ) or "none"
        print(f"  {side}: {summary}")
    print("BORDER_SIDE_CELLS")
    if not entries:
        print("  none")
    for coordinate, side, style in entries:
        print(f"  {coordinate} {side}={style}")
    print("MERGED_RANGE_BORDER_EDGES")
    merged_ranges = sorted(
        worksheet.merged_cells.ranges, key=lambda item: (item.min_row, item.min_col)
    )
    if not merged_ranges:
        print("  none")
    for merged in merged_ranges:
        evidence: list[str] = []
        for col in range(merged.min_col, merged.max_col + 1):
            for side, row_num in (("top", merged.min_row), ("bottom", merged.max_row)):
                cell = worksheet.cell(row_num, col)
                style = _border_style(cell, side)
                if style is not None:
                    evidence.append(f"{cell.coordinate}.{side}={style}")
        for row_num in range(merged.min_row, merged.max_row + 1):
            for side, col_num in (("left", merged.min_col), ("right", merged.max_col)):
                cell = worksheet.cell(row_num, col_num)
                style = _border_style(cell, side)
                if style is not None:
                    evidence.append(f"{cell.coordinate}.{side}={style}")
        print(f"  {merged}: {', '.join(evidence) if evidence else 'no perimeter styles'}")


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
    print(f"SHA-256: {observation.source.sha256}")
    workbook = load_workbook(path, data_only=False, read_only=False, keep_links=False)
    try:
        for ordinal, worksheet in enumerate(workbook.worksheets, start=1):
            print(
                f"\n### SHEET {ordinal} {worksheet.title} "
                f"| used={worksheet.calculate_dimension()} "
                f"| merged={len(worksheet.merged_cells.ranges)} "
                f"| right_to_left={bool(worksheet.sheet_view.rightToLeft)}"
            )
            if worksheet.sheet_view.rightToLeft:
                print(
                    "VISUAL_EDGE_MAPPING: column A is displayed at the right; "
                    "the visual right edge of a table beginning in A maps to "
                    "the right border of its column-A cells."
                )
            else:
                print(
                    "VISUAL_EDGE_MAPPING: column A is displayed at the left; "
                    "the visual left edge of a table beginning in A maps to "
                    "the left border of its column-A cells."
                )

            rectangles = _find_thick_outline_rectangles(worksheet)
            print(f"THICK_OUTSIDE_RECTANGLES count={len(rectangles)}")
            for bounds in rectangles:
                print(f"  OUTLINE {bounds}")

            print("MERGED_RANGES")
            for merged in sorted(str(item) for item in worksheet.merged_cells.ranges):
                print(f"  {merged}")

            _report_border_evidence(worksheet)

            print("COLOR_ANNOTATIONS")
            color_count = 0
            for row in worksheet.iter_rows():
                for cell in row:
                    font_color, fill_color, has_color = _cell_color_signature(cell)
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
