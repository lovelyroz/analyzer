"""Audit visual annotations in a standardized CODAL XLSX template.

This is a template-authoring utility, not a runtime report extractor. It validates
the workbook with the canonical Excel Reader, then reports color-coded cells,
thick-border edges, complete thick outside rectangles, and merged ranges.
It never changes the workbook or infers financial meaning.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
from typing import Any

from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.utils.cell import range_boundaries

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
    active_property = {
        "rgb": "rgb",
        "indexed": "indexed",
        "theme": "theme",
        "auto": "auto",
    }.get(color_type)
    if active_property is not None:
        value = getattr(color, active_property, None)
        if value is not None:
            parts.append(f"{active_property}={value}")
    tint = getattr(color, "tint", None)
    if tint not in (None, 0, 0.0):
        parts.append(f"tint={tint}")
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


def _fill_category(cell: Any) -> str:
    fill = cell.fill
    color = fill.fgColor
    if fill.fill_type != "solid":
        return "NO_SOLID_FILL"
    if color.type == "rgb":
        rgb = (color.rgb or "").upper()
        return {
            "FFFF0000": "RED_TITLE",
            "FF0197C8": "BLUE_HEADER",
            "FF0070C0": "BLUE_OTHER",
            "FF00B050": "GREEN_SUBTABLE_MARKER",
            "FFFFFF00": "YELLOW_OPTIONAL",
        }.get(rgb, f"RGB:{rgb}")
    if color.type == "theme":
        if color.theme == 0 and abs(float(color.tint or 0) + 0.249977111117893) < 1e-6:
            return "GRAY_POSITIVE"
        if color.theme == 1:
            return "BLACK_THEME"
        return f"THEME:{color.theme}:TINT:{color.tint}"
    return f"{color.type}:{getattr(color, color.type, None)}"


def _range_dict(a1: str) -> dict[str, int | str]:
    min_col, min_row, max_col, max_row = range_boundaries(a1)
    return {
        "a1": a1,
        "min_row": min_row,
        "max_row": max_row,
        "min_column": min_col,
        "max_column": max_col,
        "column_range": f"{get_column_letter(min_col)}:{get_column_letter(max_col)}",
    }


def build_candidate_review(workbook_path: Path, register_path: Path) -> dict[str, Any]:
    """Audit candidate geometry and gray-cell ownership without approving it."""
    observation = read_excel_source(workbook_path)
    register = json.loads(register_path.read_text(encoding="utf-8"))
    if observation.source.sha256.lower() != register["source_sha256"].lower():
        return {
            "status": "REJECTED_SOURCE_HASH_MISMATCH",
            "expected_source_sha256": register["source_sha256"],
            "observed_source_sha256": observation.source.sha256,
            "register_id": register.get("register_id"),
        }
    workbook = load_workbook(workbook_path, data_only=False, read_only=False, keep_links=False)
    try:
        matches = [
            (ordinal, sheet) for ordinal, sheet in enumerate(workbook.worksheets, start=1)
            if sheet.title == register["worksheet_name"]
        ]
        if len(matches) != 1 or matches[0][0] != register["worksheet_ordinal"]:
            return {
                "status": "REJECTED_WORKSHEET_IDENTITY",
                "register_id": register.get("register_id"),
                "matches": [ordinal for ordinal, _ in matches],
            }
        _, worksheet = matches[0]
        fill_cells: dict[str, list[str]] = {}
        for row in worksheet.iter_rows():
            for cell in row:
                category = _fill_category(cell)
                if category not in ("NO_SOLID_FILL",):
                    fill_cells.setdefault(category, []).append(cell.coordinate)

        tables_by_id = {item["id"]: item for item in register["tables"]}
        table_results: list[dict[str, Any]] = []
        ranges: dict[str, tuple[int, int, int, int]] = {}
        findings: list[str] = []
        for item in register["tables"]:
            bounds = _range_dict(item["bounds"])
            left, top, right, bottom = range_boundaries(item["bounds"])
            ranges[item["id"]] = (top, left, bottom, right)
            title = worksheet[item["title_cell"]]
            header = _range_dict(item["header"])
            hleft, htop, hright, hbottom = range_boundaries(item["header"])
            header_cells = [
                worksheet.cell(row, col).coordinate
                for row in range(htop, hbottom + 1)
                for col in range(hleft, hright + 1)
                if _fill_category(worksheet.cell(row, col)) == "BLUE_HEADER"
            ]
            edges: dict[str, Counter[str]] = {
                side: Counter() for side in ("top", "bottom", "left", "right")
            }
            for col in range(left, right + 1):
                for side, row in (("top", top), ("bottom", bottom)):
                    style = _border_style(worksheet.cell(row, col), side)
                    if style:
                        edges[side][style] += 1
            for row in range(top, bottom + 1):
                for side, col in (("left", left), ("right", right)):
                    style = _border_style(worksheet.cell(row, col), side)
                    if style:
                        edges[side][style] += 1
            lengths = {"top": right-left+1, "bottom": right-left+1,
                       "left": bottom-top+1, "right": bottom-top+1}
            complete = all(sum(edges[side].values()) == lengths[side] for side in edges)
            if not complete:
                findings.append(f"INCOMPLETE_CANDIDATE_BORDER:{item['id']}")
            table_results.append({
                "id": item["id"], "title_cell": item["title_cell"],
                "title_value": title.value, "title_fill_category": _fill_category(title),
                "bounds": bounds, "header_candidate": header,
                "blue_header_cells_observed": header_cells,
                "border_edge_styles": {side: dict(counts) for side, counts in edges.items()},
                "candidate_border_complete": complete,
                "approval_status": "CANDIDATE_NOT_APPROVED",
            })

        child_results: list[dict[str, Any]] = []
        child_ranges: dict[str, tuple[int, int, int, int]] = {}
        for item in register["partitions"]:
            parent = tables_by_id[item["parent"]]
            pleft, ptop, pright, pbottom = range_boundaries(parent["bounds"])
            start, end = item["rows"]
            if start > end or start < ptop or end > pbottom:
                findings.append(f"INVALID_PARTITION_ROWS:{item['id']}")
            a1 = f"{get_column_letter(pleft)}{start}:{get_column_letter(pright)}{end}"
            child_ranges[item["id"]] = (start, pleft, end, pright)
            marker = worksheet[item["marker"]]
            child_results.append({
                "id": item["id"], "parent": item["parent"], "marker": item["marker"],
                "marker_value": marker.value, "marker_fill_category": _fill_category(marker),
                "rows": item["rows"], "bounds": _range_dict(a1),
                "header_inheritance": "PARENT_HEADER_CANDIDATE",
                "inherited_header_candidate": parent["header"],
                "approval_status": "CANDIDATE_NOT_APPROVED",
            })
            if _fill_category(marker) != "GREEN_SUBTABLE_MARKER":
                findings.append(f"MARKER_NOT_GREEN:{item['id']}")

        table_ids = list(ranges)
        for idx, first in enumerate(table_ids):
            a = ranges[first]
            for second in table_ids[idx + 1:]:
                b = ranges[second]
                if a[0] <= b[2] and b[0] <= a[2] and a[1] <= b[3] and b[1] <= a[3]:
                    findings.append(f"OVERLAPPING_TABLE_CANDIDATES:{first}:{second}")
        for item in register["partitions"]:
            a = child_ranges[item["id"]]
            for other in register["partitions"]:
                if other["parent"] != item["parent"] or other["id"] <= item["id"]:
                    continue
                b = child_ranges[other["id"]]
                if a[0] <= b[2] and b[0] <= a[2]:
                    findings.append(f"OVERLAPPING_SIBLING_PARTITIONS:{item['id']}:{other['id']}")

        gray_cells = fill_cells.get("GRAY_POSITIVE", [])
        ownership: list[dict[str, str]] = []
        unowned: list[str] = []
        duplicate: list[dict[str, Any]] = []
        for coordinate in gray_cells:
            cell = worksheet[coordinate]
            row, col = cell.row, cell.column
            parents = [tid for tid, (t, l, b, r) in ranges.items()
                       if t <= row <= b and l <= col <= r]
            if len(parents) != 1:
                if not parents:
                    unowned.append(coordinate)
                else:
                    duplicate.append({"cell": coordinate, "owners": parents})
                continue
            parent_id = parents[0]
            children = [item["id"] for item in register["partitions"]
                        if item["parent"] == parent_id
                        and child_ranges[item["id"]][0] <= row <= child_ranges[item["id"]][2]
                        and child_ranges[item["id"]][1] <= col <= child_ranges[item["id"]][3]]
            if len(children) > 1:
                duplicate.append({"cell": coordinate, "owners": children})
            else:
                ownership.append({"cell": coordinate, "owner": children[0] if children else parent_id})
        checks = {
            "table_count_is_17": len(table_results) == 17,
            "partition_count_is_15": len(child_results) == 15,
            "all_candidate_borders_complete": all(item["candidate_border_complete"] for item in table_results),
            "all_green_markers_match": all(item["marker_fill_category"] == "GREEN_SUBTABLE_MARKER" for item in child_results),
            "no_overlapping_top_level_bounds": not any(x.startswith("OVERLAPPING_TABLE_CANDIDATES") for x in findings),
            "no_overlapping_sibling_partitions": not any(x.startswith("OVERLAPPING_SIBLING_PARTITIONS") for x in findings),
            "all_gray_positive_cells_owned_once": len(ownership) == len(gray_cells) and not unowned and not duplicate,
        }
        return {
            "status": "REVIEW_READY" if all(checks.values()) else "REVIEW_WITH_FINDINGS",
            "register_id": register["register_id"], "register_version": register["register_version"],
            "approval_status": register["approval_status"],
            "workbook": str(workbook_path), "source_sha256": observation.source.sha256,
            "worksheet": {"name": worksheet.title, "ordinal": matches[0][0],
                          "used_range": worksheet.calculate_dimension(),
                          "merged_ranges": sorted(str(r) for r in worksheet.merged_cells.ranges)},
            "fill_category_counts": {category: len(coords) for category, coords in sorted(fill_cells.items())},
            "fill_category_cells": fill_cells,
            "tables": table_results, "partitions": child_results,
            "ownership": ownership, "unowned_gray_cells": unowned,
            "duplicate_ownership": duplicate, "checks": checks, "findings": findings,
            "historical_gray_459_and_spans_60_are_not_assertions": True,
        }
    finally:
        workbook.close()


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
    parser.add_argument("--candidate-register", type=Path)
    parser.add_argument("--candidate-audit-json", type=Path)
    args = parser.parse_args()
    if args.max_color_cells < 1:
        parser.error("--max-color-cells must be positive")
    if bool(args.candidate_register) != bool(args.candidate_audit_json):
        parser.error("--candidate-register and --candidate-audit-json must be supplied together")
    status = audit_workbook(args.workbook, max_color_cells=args.max_color_cells)
    if status != 0:
        return status
    if args.candidate_register:
        result = build_candidate_review(args.workbook, args.candidate_register)
        args.candidate_audit_json.parent.mkdir(parents=True, exist_ok=True)
        args.candidate_audit_json.write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(f"CANDIDATE_REVIEW_JSON={args.candidate_audit_json}")
        print(f"CANDIDATE_REVIEW_STATUS={result['status']}")
        if result["status"] != "REVIEW_READY":
            print(f"CANDIDATE_REVIEW_FINDINGS={result.get('findings', [])}")
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
