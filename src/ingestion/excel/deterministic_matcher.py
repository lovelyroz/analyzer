"""Deterministic, fail-closed matching for explicitly versioned Excel templates.

This is a pure structural matcher. It does not interpret financial meaning,
read annotation colors at runtime, or persist observations. A candidate template
must be explicitly marked approved before it can produce a MATCHED result.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
import re

from openpyxl.utils.cell import coordinate_to_tuple, range_boundaries

from src.ingestion.excel.dto import WorkbookObservation


@dataclass(frozen=True, slots=True)
class PartitionRule:
    code: str
    marker_cell: str
    marker_text: str
    bounds: str
    header_inheritance: str
    owned_ranges: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class TableRule:
    code: str
    title_cell: str
    title_text: str
    bounds: str
    title_search_range: str | None = None
    header_cells: tuple[tuple[str, str], ...] = ()
    partitions: tuple[PartitionRule, ...] = ()
    owned_ranges: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class TemplateVersion:
    template_id: str
    version: str
    approved: bool
    source_workbook_sha256: str
    worksheet_name: str
    worksheet_ordinal: int
    tables: tuple[TableRule, ...]

    @property
    def template_sha256(self) -> str:
        payload = {
            "template_id": self.template_id,
            "version": self.version,
            "approved": self.approved,
            "source_workbook_sha256": self.source_workbook_sha256.lower(),
            "worksheet_name": self.worksheet_name,
            "worksheet_ordinal": self.worksheet_ordinal,
            "tables": [
                {
                    "code": t.code, "title_cell": t.title_cell,
                    "title_text": t.title_text, "bounds": t.bounds,
                    "title_search_range": t.title_search_range,
                    "header_cells": list(t.header_cells),
                    "owned_ranges": list(t.owned_ranges),
                    "partitions": [
                        {
                            "code": p.code, "marker_cell": p.marker_cell,
                            "marker_text": p.marker_text, "bounds": p.bounds,
                            "header_inheritance": p.header_inheritance,
                            "owned_ranges": list(p.owned_ranges),
                        } for p in t.partitions
                    ],
                } for t in self.tables
            ],
        }
        canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        return sha256(canonical.encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class MatchDiagnostic:
    code: str
    message: str
    node_code: str | None = None
    coordinate: str | None = None


@dataclass(frozen=True, slots=True)
class TemplateMatchResult:
    status: str
    template_id: str
    template_version: str
    template_sha256: str
    source_workbook_sha256: str
    coordinate_map: tuple[tuple[str, str], ...] = ()
    diagnostics: tuple[MatchDiagnostic, ...] = ()
    worksheet_name: str | None = None
    worksheet_ordinal: int | None = None


def _inside(inner: str, outer: str) -> bool:
    il, it, ir, ib = range_boundaries(inner)
    ol, ot, or_, ob = range_boundaries(outer)
    return ol <= il <= ir <= or_ and ot <= it <= ib <= ob


def _overlaps(first: str, second: str) -> bool:
    al, at, ar, ab = range_boundaries(first)
    bl, bt, br, bb = range_boundaries(second)
    return al <= br and bl <= ar and at <= bb and bt <= ab


def _valid_sha256(value: str) -> bool:
    return bool(re.fullmatch(r"[0-9a-fA-F]{64}", value or ""))


def _template_diagnostics(template: TemplateVersion) -> list[MatchDiagnostic]:
    diagnostics: list[MatchDiagnostic] = []
    if not template.template_id or not template.version or not template.worksheet_name:
        diagnostics.append(MatchDiagnostic("TEMPLATE_METADATA_MISSING", "Template identity, version, and worksheet are required."))
    if not _valid_sha256(template.source_workbook_sha256):
        diagnostics.append(MatchDiagnostic("TEMPLATE_SOURCE_FINGERPRINT_INVALID", "Template source workbook SHA-256 is invalid."))
    if template.worksheet_ordinal < 1:
        diagnostics.append(MatchDiagnostic("TEMPLATE_WORKSHEET_ORDINAL_INVALID", "Worksheet ordinal must be 1-based."))
    if not template.tables:
        diagnostics.append(MatchDiagnostic("TEMPLATE_HAS_NO_TABLES", "At least one table rule is required."))
    codes = [table.code for table in template.tables]
    if len(codes) != len(set(codes)):
        diagnostics.append(MatchDiagnostic("DUPLICATE_TABLE_CODE", "Table codes must be unique."))
    all_node_codes = codes + [p.code for table in template.tables for p in table.partitions]
    if len(all_node_codes) != len(set(all_node_codes)):
        diagnostics.append(MatchDiagnostic("DUPLICATE_NODE_CODE", "Table and partition codes must be unique."))
    ownership: list[tuple[str, str]] = []
    partition_codes: set[str] = set()
    for table in template.tables:
        try:
            range_boundaries(table.bounds)
            coordinate_to_tuple(table.title_cell)
            if table.title_search_range:
                range_boundaries(table.title_search_range)
            for cell, _ in table.header_cells:
                coordinate_to_tuple(cell)
            for owned in table.owned_ranges:
                if not _inside(owned, table.bounds):
                    diagnostics.append(MatchDiagnostic("OWNED_RANGE_OUTSIDE_TABLE", "Owned range must be inside its table bounds.", table.code))
                ownership.append((table.code, owned))
            sibling_ranges: list[tuple[str, str]] = []
            for partition in table.partitions:
                if partition.code in partition_codes:
                    diagnostics.append(MatchDiagnostic("DUPLICATE_NODE_CODE", "Table and partition codes must be unique.", partition.code))
                partition_codes.add(partition.code)
                if not _inside(partition.bounds, table.bounds):
                    diagnostics.append(MatchDiagnostic("PARTITION_OUTSIDE_PARENT", "Partition bounds must be contained by its parent table.", partition.code))
                if partition.header_inheritance not in {"PARENT", "INDEPENDENT"}:
                    diagnostics.append(MatchDiagnostic("PARTITION_HEADER_POLICY_INVALID", "Header inheritance must be explicit.", partition.code))
                for prior_code, prior_range in sibling_ranges:
                    if _overlaps(partition.bounds, prior_range):
                        diagnostics.append(MatchDiagnostic("SIBLING_PARTITIONS_OVERLAP", f"Partition overlaps {prior_code}.", partition.code))
                sibling_ranges.append((partition.code, partition.bounds))
                for owned in partition.owned_ranges:
                    if not _inside(owned, partition.bounds):
                        diagnostics.append(MatchDiagnostic("OWNED_RANGE_OUTSIDE_PARTITION", "Owned range must be inside its partition.", partition.code))
                    ownership.append((partition.code, owned))
        except (ValueError, TypeError):
            diagnostics.append(MatchDiagnostic("TEMPLATE_RANGE_INVALID", "Template contains an invalid A1 reference.", table.code))
    for index, (code, first) in enumerate(ownership):
        for other_code, second in ownership[index + 1:]:
            if _overlaps(first, second):
                diagnostics.append(MatchDiagnostic("OWNERSHIP_OVERLAP", f"Owned range overlaps node {other_code}.", code))
    for index, (code, first) in enumerate((t.code, t.bounds) for t in template.tables):
        for other_code, second in ((t.code, t.bounds) for t in template.tables[index + 1:]):
            if _overlaps(first, second):
                diagnostics.append(MatchDiagnostic("TABLE_BOUNDS_OVERLAP", f"Table bounds overlap node {other_code}.", code))
    return diagnostics


def match_template(template: TemplateVersion, observation: WorkbookObservation) -> TemplateMatchResult:
    """Return a complete exact structural match or deterministic rejection."""
    diagnostics = _template_diagnostics(template)
    if not template.approved:
        diagnostics.append(MatchDiagnostic("TEMPLATE_NOT_APPROVED", "Candidate templates cannot be used for matching."))
    if not _valid_sha256(observation.source.sha256):
        diagnostics.append(MatchDiagnostic("SOURCE_FINGERPRINT_INVALID", "Incoming workbook SHA-256 is invalid."))

    sheets = [sheet for sheet in observation.worksheets if sheet.literal_name == template.worksheet_name]
    if len(sheets) != 1 or (sheets and sheets[0].ordinal != template.worksheet_ordinal):
        diagnostics.append(MatchDiagnostic("WORKSHEET_IDENTITY_MISMATCH", "Exact worksheet name and ordinal did not resolve uniquely."))
        sheet_ordinal = None
    else:
        sheet_ordinal = sheets[0].ordinal
        used = sheets[0].used_range
        if used is None:
            diagnostics.append(MatchDiagnostic("WORKSHEET_EMPTY", "Required worksheet has no used range."))
        else:
            for table in template.tables:
                if not _inside(table.bounds, used.a1_range or "A1:A1"):
                    diagnostics.append(MatchDiagnostic("TABLE_OUTSIDE_USED_RANGE", "Template table bounds exceed the observed worksheet range.", table.code))

    cells = {
        cell.cell_ref.coordinate: cell
        for cell in observation.cells
        if sheet_ordinal is not None and cell.cell_ref.worksheet_ordinal == sheet_ordinal
    }
    coordinate_map: list[tuple[str, str]] = []
    for table in template.tables:
        try:
            if table.title_search_range and sheet_ordinal is not None:
                left, top, right, bottom = range_boundaries(table.title_search_range)
                hits = []
                for coordinate, observed_cell in cells.items():
                    row, col = coordinate_to_tuple(coordinate)
                    if top <= row <= bottom and left <= col <= right and observed_cell.text_value == table.title_text:
                        hits.append(coordinate)
                if len(hits) > 1:
                    diagnostics.append(MatchDiagnostic("AMBIGUOUS_TABLE_ANCHOR", "Exact title has multiple hits in its explicit search range.", table.code))
                elif len(hits) == 1 and hits[0] != table.title_cell:
                    diagnostics.append(MatchDiagnostic("UNAPPROVED_COORDINATE_DRIFT", "Unique title moved from its fixed template coordinate.", table.code, hits[0]))
            if sheet_ordinal is not None:
                title = cells.get(table.title_cell)
                if title is None or title.text_value != table.title_text:
                    diagnostics.append(MatchDiagnostic("TABLE_TITLE_MISMATCH", "Exact approved title text was not found at its fixed anchor.", table.code, table.title_cell))
                else:
                    coordinate_map.append((table.code, table.bounds))
                for coordinate, expected in table.header_cells:
                    observed = cells.get(coordinate)
                    if observed is None or observed.text_value != expected:
                        diagnostics.append(MatchDiagnostic("HEADER_FINGERPRINT_MISMATCH", "Exact approved header text differs.", table.code, coordinate))
                for partition in table.partitions:
                    marker = cells.get(partition.marker_cell)
                    if marker is None or marker.text_value != partition.marker_text:
                        diagnostics.append(MatchDiagnostic("PARTITION_MARKER_MISMATCH", "Exact approved partition marker differs.", partition.code, partition.marker_cell))
                    else:
                        coordinate_map.append((partition.code, partition.bounds))
        except (ValueError, TypeError):
            diagnostics.append(MatchDiagnostic("TEMPLATE_REFERENCE_INVALID", "Template contains an invalid coordinate.", table.code))

    status = "REJECTED" if diagnostics else "MATCHED"
    return TemplateMatchResult(
        status=status,
        template_id=template.template_id,
        template_version=template.version,
        template_sha256=template.template_sha256,
        source_workbook_sha256=observation.source.sha256,
        coordinate_map=tuple(coordinate_map) if status == "MATCHED" else (),
        diagnostics=tuple(diagnostics),
        worksheet_name=template.worksheet_name if status == "MATCHED" else None,
        worksheet_ordinal=template.worksheet_ordinal if status == "MATCHED" else None,
    )
    
