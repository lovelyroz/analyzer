"""Isolated acceptance tests for deterministic, fail-closed template matching."""
from io import BytesIO

import pytest
from openpyxl import Workbook

from src.ingestion.excel.reader import read_excel_source
from src.ingestion.excel.deterministic_matcher import (
    PartitionRule,
    TableRule,
    TemplateVersion,
    match_template,
)


def _observation(*, title="Revenue", duplicate_title=False):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Annual"
    sheet["A1"] = title
    sheet["B1"] = "Amount"
    sheet["A2"] = "Child"
    sheet["B2"] = 12
    if duplicate_title:
        sheet["A3"] = title
    stream = BytesIO()
    workbook.save(stream)
    return read_excel_source(stream.getvalue(), file_name="fixture.xlsx")


def _template(*, approved=True, title="Revenue", anchor_range=None,
              parent_owned=(), child_owned=("A2:B2",), child_bounds="A2:B2"):
    child = PartitionRule(
        code="T1-P1", marker_cell="A2", marker_text="Child",
        bounds=child_bounds, header_inheritance="PARENT",
        owned_ranges=child_owned,
    )
    table = TableRule(
        code="T1", title_cell="A1", title_text=title, bounds="A1:B2",
        title_search_range=anchor_range,
        header_cells=(("B1", "Amount"),), partitions=(child,),
        owned_ranges=parent_owned,
    )
    return TemplateVersion(
        template_id="fixture-template", version="2.1.0", approved=approved,
        source_workbook_sha256="a" * 64, worksheet_name="Annual",
        worksheet_ordinal=1, tables=(table,),
    )


def test_exact_approved_template_matches_and_records_both_hashes():
    result = match_template(_template(), _observation())

    assert result.status == "MATCHED"
    assert result.template_id == "fixture-template"
    assert result.template_version == "2.1.0"
    assert len(result.template_sha256) == 64
    assert result.source_workbook_sha256 == _observation().source.sha256
    assert result.coordinate_map == (("T1", "A1:B2"), ("T1-P1", "A2:B2"))
    assert result.owned_coordinate_map == (("T1-P1", "A2:B2"),)


def test_unapproved_candidate_is_rejected():
    result = match_template(_template(approved=False), _observation())

    assert result.status == "REJECTED"
    assert "TEMPLATE_NOT_APPROVED" in {item.code for item in result.diagnostics}
    assert result.coordinate_map == ()


def test_ambiguous_exact_title_anchor_is_rejected():
    result = match_template(
        _template(anchor_range="A1:A3"), _observation(duplicate_title=True)
    )

    assert result.status == "REJECTED"
    assert "AMBIGUOUS_TABLE_ANCHOR" in {item.code for item in result.diagnostics}


def test_template_fingerprint_mismatch_is_rejected():
    result = match_template(_template(title="Expenses"), _observation())

    assert result.status == "REJECTED"
    assert "TABLE_TITLE_MISMATCH" in {item.code for item in result.diagnostics}


def test_overlapping_extraction_ownership_is_rejected():
    result = match_template(
        _template(parent_owned=("A1:A2",), child_owned=("A2:B2",)),
        _observation(),
    )

    assert result.status == "REJECTED"
    assert "OWNERSHIP_OVERLAP" in {item.code for item in result.diagnostics}


def test_owned_range_overlapping_excluded_range_is_rejected():
    template = _template(child_owned=("A2:B2",))
    table = template.tables[0]
    child = table.partitions[0]
    changed_child = PartitionRule(
        code=child.code, marker_cell=child.marker_cell, marker_text=child.marker_text,
        bounds=child.bounds, header_inheritance=child.header_inheritance,
        owned_ranges=child.owned_ranges, excluded_ranges=("B2:B2",),
    )
    changed_table = TableRule(
        code=table.code, title_cell=table.title_cell, title_text=table.title_text,
        bounds=table.bounds, title_search_range=table.title_search_range,
        header_cells=table.header_cells, partitions=(changed_child,), owned_ranges=table.owned_ranges,
    )
    result = match_template(
        TemplateVersion(template.template_id, template.version, template.approved,
                        template.source_workbook_sha256, template.worksheet_name,
                        template.worksheet_ordinal, (changed_table,)),
        _observation(),
    )
    assert result.status == "REJECTED"
    assert "OWNED_EXCLUDED_RANGE_OVERLAP" in {item.code for item in result.diagnostics}


def test_partition_outside_parent_is_rejected():
    result = match_template(_template(child_bounds="A2:B3"), _observation())

    assert result.status == "REJECTED"
    codes = {item.code for item in result.diagnostics}
    assert "PARTITION_OUTSIDE_PARENT" in codes
    assert "TABLE_OUTSIDE_USED_RANGE" not in codes


def test_template_hash_changes_when_rule_version_or_bounds_change():
    original = _template()
    changed = TemplateVersion(
        template_id=original.template_id, version=original.version,
        approved=original.approved,
        source_workbook_sha256=original.source_workbook_sha256,
        worksheet_name=original.worksheet_name,
        worksheet_ordinal=original.worksheet_ordinal,
        tables=(TableRule(
            code="T1", title_cell="A1", title_text="Revenue", bounds="A1:C2",
            header_cells=(("B1", "Amount"),),
            partitions=original.tables[0].partitions,
            owned_ranges=original.tables[0].owned_ranges,
        ),),
    )
    assert changed.template_sha256 != original.template_sha256
