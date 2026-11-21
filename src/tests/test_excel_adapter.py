"""Synthetic end-to-end coverage; fixtures are not production approvals."""
from dataclasses import replace
from decimal import Decimal
from hashlib import sha256
from io import BytesIO

from openpyxl import Workbook
from openpyxl.styles import PatternFill

from src.ingestion.canonical_admission import RevisionContext, ValueOrigin
from src.ingestion.excel.adapter import adapt_excel_source
from src.ingestion.excel.canonical_input import (
    ApprovedSelection,
    CanonicalInputSpec,
    DurationBasis,
    JalaliPeriod,
    TemporalType,
)
from src.ingestion.excel.deterministic_matcher import TableRule, TemplateVersion
from src.ingestion.excel.dto import CellValueKind


def _approved(identity, *, count=1):
    return ApprovedSelection(identity, True, count, f"approval-{identity}")


def _spec(*, metric_count=1, period=None):
    return CanonicalInputSpec(
        company=_approved("company-1"),
        report_type=_approved("report-periodic"),
        report_version=_approved("version-1"),
        metric=_approved("metric-sales", count=metric_count),
        source_unit=_approved("unit-rial"),
        source_currency=_approved("currency-irr"),
        source_scale=_approved("scale-unit"),
        period=period or JalaliPeriod(
            TemporalType.DURATION,
            (1404, 1, 1),
            (1404, 12, 29),
            DurationBasis.YTD,
        ),
        period_mapping=_approved("period-1404-ytd"),
        source_label=_approved("label-sales"),
        source_header=_approved("header-current"),
    )


def _source_and_template(values=("125.50",)):
    """Build a synthetic workbook and matching test-only template fixture."""
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Annual"
    sheet["A1"] = "Revenue"
    sheet["B1"] = "Amount"
    coordinates = ("B2", "C2", "D2")
    for coordinate, value in zip(coordinates, values):
        if value is None:
            sheet[coordinate].fill = PatternFill(fill_type="solid", fgColor="FFFFFF")
        else:
            sheet[coordinate] = value
    stream = BytesIO()
    workbook.save(stream)
    source = stream.getvalue()
    last_column = coordinates[len(values) - 1][0]
    template = TemplateVersion(
        template_id="fixture-template",
        version="3",
        approved=True,
        source_workbook_sha256="a" * 64,
        worksheet_name="Annual",
        worksheet_ordinal=1,
        tables=(TableRule(
            code="income-statement",
            title_cell="A1",
            title_text="Revenue",
            bounds=f"A1:{last_column}2",
            header_cells=(("B1", "Amount"),),
            owned_ranges=(f"B2:{last_column}2",),
        ),),
    )
    return source, template


def _revision(source_hash):
    return RevisionContext(
        report_id="report-1",
        report_version_id="version-1",
        company_id="company-1",
        source_identity="fixture-source-1",
        revision_identity="fixture-revision-1",
        source_artifact_sha256=source_hash,
        extraction_standard_id="standard-v1",
        extraction_standard_approval_ref="approval-standard-v1",
    )


def test_valid_source_matches_builds_explicit_candidate_and_admits_only_on_request():
    source, template = _source_and_template()
    source_hash = sha256(source).hexdigest()
    selections = {"B2": _spec()}

    prepared = adapt_excel_source(
        source,
        template=template,
        selections_by_coordinate=selections,
        expected_source_sha256=source_hash,
    )
    assert prepared.accepted
    assert prepared.admission_plan is None
    assert len(prepared.submissions) == 1
    candidate = prepared.submissions[0].candidate
    assert candidate.source_workbook_sha256 == source_hash
    assert candidate.worksheet_name == "Annual"
    assert candidate.source_coordinate == "B2"
    assert candidate.source_text == "125.50"
    assert candidate.template_id == template.template_id
    assert candidate.template_version == template.version
    assert candidate.template_sha256 == template.template_sha256
    assert prepared.observation is not None
    assert next(cell for cell in prepared.observation.cells if cell.cell_ref.coordinate == "B1").text_value == "Amount"
    assert prepared.match is not None and prepared.match.coordinate_map == (("income-statement", "A1:B2"),)

    admitted = adapt_excel_source(
        source,
        template=template,
        selections_by_coordinate=selections,
        admit=True,
        revision=_revision(source_hash),
    )
    assert admitted.accepted
    assert admitted.admission_plan is not None
    assert admitted.admission_plan.execution_allowed is False
    assert admitted.admission_plan.physical_persistence_compatible is False
    assert admitted.admission_plan.atomicity_unit == "REPORT_VERSION"
    fact, = admitted.admission_plan.facts
    assert fact.company_id == "company-1"
    assert fact.report_type_id == "report-periodic"
    assert fact.report_version_id == "version-1"
    assert fact.metric_id == "metric-sales"
    assert fact.source_unit == "unit-rial"
    assert fact.source_currency == "currency-irr"
    assert fact.source_scale == "scale-unit"
    assert fact.period_identity == ("DURATION", (1404, 1, 1), (1404, 12, 29))
    assert fact.duration_basis == "YTD"
    assert fact.source_value_decimal == Decimal("125.50")
    assert fact.value_integer == 126
    assert fact.source_artifact_sha256 == source_hash
    assert fact.template_id == "fixture-template"
    assert fact.template_version == "3"
    assert fact.template_sha256 == template.template_sha256
    assert fact.extraction_owner == "income-statement"
    assert set(fact.approval_references) >= {
        ("company", "company-1", "approval-company-1"),
        ("report_type", "report-periodic", "approval-report-periodic"),
        ("report_version", "version-1", "approval-version-1"),
        ("metric", "metric-sales", "approval-metric-sales"),
        ("unit", "unit-rial", "approval-unit-rial"),
        ("currency", "currency-irr", "approval-currency-irr"),
        ("scale", "scale-unit", "approval-scale-unit"),
        ("period_mapping", "period-1404-ytd", "approval-period-1404-ytd"),
    }
    # The source locator is available on the submission candidate. PlannedFact
    # intentionally does not persist cell coordinates under the current contract.
    assert admitted.submissions[0].candidate.source_coordinate == "B2"


def test_multi_period_report_preserves_explicit_ytd_and_standalone_semantics():
    source, template = _source_and_template(("1240", "330"))
    ytd = replace(
        _spec(),
        period=JalaliPeriod(
            TemporalType.DURATION,
            (1404, 1, 1),
            (1404, 6, 31),
            DurationBasis.YTD,
        ),
        period_mapping=_approved("period-1404-six-month-ytd"),
    )
    standalone = replace(
        _spec(),
        period=JalaliPeriod(
            TemporalType.DURATION,
            (1404, 4, 1),
            (1404, 6, 31),
            DurationBasis.STANDALONE,
        ),
        period_mapping=_approved("period-1404-q2-standalone"),
    )
    source_hash = sha256(source).hexdigest()

    result = adapt_excel_source(
        source,
        template=template,
        selections_by_coordinate={"B2": ytd, "C2": standalone},
        admit=True,
        revision=_revision(source_hash),
    )

    assert result.accepted
    assert result.admission_plan is not None
    facts_by_period = {fact.period_identity: fact for fact in result.admission_plan.facts}
    assert len(facts_by_period) == 2
    assert facts_by_period[("DURATION", (1404, 1, 1), (1404, 6, 31))].duration_basis == "YTD"
    assert facts_by_period[("DURATION", (1404, 4, 1), (1404, 6, 31))].duration_basis == "STANDALONE"
    assert {fact.value_integer for fact in facts_by_period.values()} == {1240, 330}
    assert facts_by_period[("DURATION", (1404, 1, 1), (1404, 6, 31))].source_value_decimal == Decimal("1240")
    assert facts_by_period[("DURATION", (1404, 4, 1), (1404, 6, 31))].source_value_decimal == Decimal("330")
    assert {submission.candidate.source_coordinate for submission in result.submissions} == {"B2", "C2"}


def test_instant_period_and_exact_decimal_survive_the_full_chain():
    source, template = _source_and_template(("0.1250",))
    instant = replace(
        _spec(),
        period=JalaliPeriod(TemporalType.INSTANT, (1404, 6, 31), (1404, 6, 31)),
        period_mapping=_approved("period-1404-06-instant"),
    )
    source_hash = sha256(source).hexdigest()

    result = adapt_excel_source(
        source,
        template=template,
        selections_by_coordinate={"B2": instant},
        expected_source_sha256=source_hash,
        admit=True,
        revision=_revision(source_hash),
    )

    assert result.accepted
    submission, = result.submissions
    assert submission.candidate.source_coordinate == "B2"
    assert submission.candidate.temporal_type is TemporalType.INSTANT
    assert submission.candidate.period_start_jalali == (1404, 6, 31)
    assert submission.candidate.period_end_jalali == (1404, 6, 31)
    assert result.admission_plan is not None
    fact, = result.admission_plan.facts
    assert fact.period_identity == ("INSTANT", (1404, 6, 31), (1404, 6, 31))
    assert fact.duration_basis is None
    assert fact.source_value_decimal == Decimal("0.1250")
    assert fact.value_integer == 0


def test_duplicate_and_conflicting_facts_keep_all_or_nothing_admission_semantics():
    same_source, same_template = _source_and_template(("42", "42"))
    same_hash = sha256(same_source).hexdigest()
    same = adapt_excel_source(
        same_source,
        template=same_template,
        selections_by_coordinate={"B2": _spec(), "C2": _spec()},
        admit=True,
        revision=_revision(same_hash),
    )
    assert same.accepted
    assert same.admission_plan is not None
    assert len(same.admission_plan.facts) == 1
    assert same.admission_plan.duplicate_count == 1

    conflict_source, conflict_template = _source_and_template(("42", "43"))
    conflict_hash = sha256(conflict_source).hexdigest()
    conflict = adapt_excel_source(
        conflict_source,
        template=conflict_template,
        selections_by_coordinate={"B2": _spec(), "C2": _spec()},
        admit=True,
        revision=_revision(conflict_hash),
    )
    assert not conflict.accepted
    assert "INTRA_BATCH_CONFLICT" in {item.code for item in conflict.diagnostics}
    assert conflict.admission_plan is None
    assert conflict.submissions == ()


def test_unapproved_template_and_wrong_worksheet_fail_closed():
    source, template = _source_and_template()
    unapproved = adapt_excel_source(
        source,
        template=replace(template, approved=False),
        selections_by_coordinate={"B2": _spec()},
    )
    assert not unapproved.accepted
    assert "TEMPLATE_NOT_APPROVED" in {item.code for item in unapproved.diagnostics}
    assert unapproved.submissions == ()

    wrong_sheet = adapt_excel_source(
        source,
        template=replace(template, worksheet_name="Other"),
        selections_by_coordinate={"B2": _spec()},
    )
    assert "WORKSHEET_IDENTITY_MISMATCH" in {item.code for item in wrong_sheet.diagnostics}
    assert wrong_sheet.submissions == ()


def test_expected_source_hash_mismatch_is_rejected():
    source, template = _source_and_template()
    original_hash = sha256(source).hexdigest()
    changed_source, _ = _source_and_template(("125.51",))
    assert sha256(changed_source).hexdigest() != original_hash
    result = adapt_excel_source(
        changed_source,
        template=template,
        selections_by_coordinate={"B2": _spec()},
        expected_source_sha256=original_hash,
    )
    assert [item.code for item in result.diagnostics] == ["SOURCE_HASH_MISMATCH"]
    assert result.submissions == ()


def test_formula_source_is_rejected_by_existing_reader_contract():
    source, template = _source_and_template(("=1+1",))
    result = adapt_excel_source(
        source,
        template=template,
        selections_by_coordinate={"B2": _spec()},
    )
    assert not result.accepted
    assert "EXCEL_UNSUPPORTED_CELL_VALUE" in {item.code for item in result.diagnostics}
    assert result.match is None
    assert result.submissions == ()


def test_missing_or_ambiguous_semantic_and_temporal_selections_reject():
    source, template = _source_and_template()
    missing = adapt_excel_source(source, template=template, selections_by_coordinate={})
    assert "IN_SCOPE_SELECTION_MISSING" in {item.code for item in missing.diagnostics}

    ambiguous = adapt_excel_source(
        source,
        template=template,
        selections_by_coordinate={"B2": _spec(metric_count=2)},
    )
    assert "MAPPING_AMBIGUOUS" in {item.code for item in ambiguous.diagnostics}

    unapproved = adapt_excel_source(
        source,
        template=template,
        selections_by_coordinate={
            "B2": replace(_spec(), source_currency=ApprovedSelection("currency-irr", False, 1, None))
        },
    )
    assert "MAPPING_NOT_APPROVED" in {item.code for item in unapproved.diagnostics}

    # A missing temporal selection is rejected by the existing candidate builder.
    missing_period = adapt_excel_source(
        source,
        template=template,
        selections_by_coordinate={"B2": replace(_spec(), period=None)},
    )
    assert "PERIOD_MISSING" in {item.code for item in missing_period.diagnostics}


def test_blank_zero_and_zero_fallback_remain_distinct_through_adapter():
    blank_source, blank_template = _source_and_template((None,))
    without_rule = adapt_excel_source(
        blank_source,
        template=blank_template,
        selections_by_coordinate={"B2": _spec()},
    )
    assert "SOURCE_VALUE_MISSING" in {item.code for item in without_rule.diagnostics}
    assert without_rule.submissions == ()

    rule = ApprovedSelection("metric-sales", True, 1, "approved-zero-rule")
    with_fallback = adapt_excel_source(
        blank_source,
        template=blank_template,
        selections_by_coordinate={"B2": _spec()},
        zero_fallback_rules_by_coordinate={"B2": rule},
        admit=True,
        revision=_revision(sha256(blank_source).hexdigest()),
    )
    assert with_fallback.accepted
    fallback_candidate = with_fallback.submissions[0].candidate
    assert fallback_candidate.source_value_kind is CellValueKind.BLANK
    assert fallback_candidate.source_text is None
    assert fallback_candidate.source_native_integer is None
    assert fallback_candidate.value == Decimal(0)
    assert with_fallback.submissions[0].value_origin is ValueOrigin.ZERO_FALLBACK
    assert with_fallback.admission_plan is not None
    assert with_fallback.admission_plan.facts[0].value_origin is ValueOrigin.ZERO_FALLBACK

    zero_source, zero_template = _source_and_template(("0",))
    actual_zero = adapt_excel_source(
        zero_source,
        template=zero_template,
        selections_by_coordinate={"B2": _spec()},
    )
    assert actual_zero.accepted
    assert actual_zero.submissions[0].candidate.source_text == "0"
    assert actual_zero.submissions[0].candidate.value == Decimal(0)
    assert actual_zero.submissions[0].value_origin is ValueOrigin.SOURCE_REPORTED


def test_unknown_in_scope_observation_rejects_whole_unit_with_stable_diagnostics():
    source, template = _source_and_template(("1", "2", "3"))
    source_hash = sha256(source).hexdigest()
    first = {"B2": _spec(), "C2": _spec(metric_count=2)}
    second = {"C2": _spec(metric_count=2), "B2": _spec()}
    left = adapt_excel_source(
        source, template=template, selections_by_coordinate=first,
        expected_source_sha256=source_hash, admit=True, revision=_revision(source_hash),
    )
    right = adapt_excel_source(
        source, template=template, selections_by_coordinate=second,
        expected_source_sha256=source_hash, admit=True, revision=_revision(source_hash),
    )
    assert left.diagnostics == right.diagnostics
    assert {item.code for item in left.diagnostics} == {"MAPPING_AMBIGUOUS", "IN_SCOPE_SELECTION_MISSING"}
    assert left.submissions == right.submissions == ()
    assert left.admission_plan is right.admission_plan is None
