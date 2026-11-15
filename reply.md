(analyzer) PS D:\Winprojects\analyzer> pytest src/tests/test_excel_observation_dto.py src/tests/test_excel_source_reader.py src/tests/test_excel_table_detector.py -q
.............................F........                                                                           [100%]
====================================================== FAILURES =======================================================
____________________________ test_reader_captures_cell_border_fill_font_and_style_evidence ____________________________

source = b'PK\x03\x04\x14\x00\x00\x00\x08\x00\xb8\xa6o]F\xc7MH\x95\x00\x00\x00\xcd\x00\x00\x00\x10\x00\x00\x00docProps/app.xmlM...x00\x80\x01q\x0f\x00\x00[Content_Types].xmlPK\x05\x06\x00\x00\x00\x00\t\x00\t\x00>\x02\x00\x00\xbd\x10\x00\x00\x00\x00'
source_ref = None, file_name = None, config = None

    def read_excel_source(
        source: BytesSource | PathSource,
        *,
        source_ref: str | None = None,
        file_name: str | None = None,
        config: ExcelReaderConfig | None = None,
    ) -> WorkbookObservation:
        """Read one XLSX source into an immutable observation.

        On a literal-value contract violation, raises ExcelSourceContractError after
        scanning the workbook; the exception exposes the complete observation and
        all cell-level diagnostics so the caller can reject the entire report.
        """
        settings = config or ExcelReaderConfig()
        payload, resolved_name, resolved_path = _read_source(
            source, file_name=file_name, max_file_bytes=settings.max_file_bytes
        )
        _preflight_package(payload, settings)

        try:
            workbook = load_workbook(
                BytesIO(payload),
                read_only=False,
                data_only=False,
                keep_links=False,
            )
        except Exception as exc:
            raise ExcelSourceReadError("EXCEL_WORKBOOK_UNREADABLE", f"openpyxl could not read XLSX: {exc}") from exc

        try:
            sheet_names = tuple(workbook.sheetnames)
            if not sheet_names:
                raise ExcelSourceReadError("EXCEL_NO_WORKSHEETS", "Workbook contains no worksheets.")
            if len(sheet_names) > settings.max_worksheets:
                raise ExcelSourceReadError(
                    "EXCEL_WORKSHEET_LIMIT_EXCEEDED",
                    f"Workbook has {len(sheet_names)} worksheets; configured limit is {settings.max_worksheets}.",
                )

            declared_table_specs: list[tuple[int, int, TableObservation]] = []
            worksheet_shells: list[tuple[object, int, tuple[CellRange, ...], tuple[object, ...]]] = []
            total_scan_cells = 0
            for worksheet_ordinal, worksheet_name in enumerate(sheet_names, start=1):
                worksheet = workbook[worksheet_name]
                max_row = max(int(worksheet.max_row or 1), 1)
                max_column = max(int(worksheet.max_column or 1), 1)
                scan_count = max_row * max_column
                total_scan_cells += scan_count
                if total_scan_cells > settings.max_total_cells:
                    raise ExcelSourceReadError(
                        "EXCEL_CELL_SCAN_LIMIT_EXCEEDED",
                        f"Workbook requires scanning {total_scan_cells} cells; configured limit is {settings.max_total_cells}.",
                    )
                merged_ranges = tuple(
                    sorted(
                        (_cell_range(r.min_row, r.min_col, r.max_row, r.max_col) for r in worksheet.merged_cells.ranges),
                        key=lambda item: (item.min_row, item.min_column, item.max_row, item.max_column),
                    )
                )
                worksheet_shells.append((worksheet, worksheet_ordinal, merged_ranges, ()))

            cell_observations: list[CellObservation] = []
            row_observations: list[RowObservation] = []
            column_observations: list[ColumnObservation] = []
            worksheet_observations: list[WorksheetObservation] = []
            table_observations: list[TableObservation] = []
            workbook_diagnostics: list[Diagnostic] = []

            for worksheet, worksheet_ordinal, merged_ranges, _ in worksheet_shells:
                populated_bounds: list[tuple[int, int]] = []
                row_cells: dict[int, list[CellRef]] = {}
                column_cells: dict[int, list[CellRef]] = {}
                local_diagnostics: list[Diagnostic] = []
                merged_by_coordinate: dict[tuple[int, int], CellRange] = {}
                for merged in merged_ranges:
                    for row_index in range(merged.min_row, merged.max_row + 1):
                        for column_index in range(merged.min_column, merged.max_column + 1):
                            merged_by_coordinate[(row_index, column_index)] = merged

                for row in worksheet.iter_rows():
                    for cell in row:
                        value = cell.value
                        has_literal = value is not None
                        has_style = bool(getattr(cell, "has_style", False))
                        in_merged_range = (cell.row, cell.column) in merged_by_coordinate
                        if not has_literal and not has_style and not in_merged_range:
                            continue
                        if has_literal or has_style:
                            populated_bounds.append((cell.row, cell.column))
                        cell_ref = CellRef(
                            worksheet_ordinal=worksheet_ordinal,
                            coordinate=cell.coordinate,
                            row_index=cell.row,
                            column_index=cell.column,
                        )
                        merged_range = merged_by_coordinate.get((cell.row, cell.column))
                        merged_anchor = None
                        if merged_range is not None:
                            anchor_coordinate = f"{get_column_letter(merged_range.min_column)}{merged_range.min_row}"
                            merged_anchor = CellRef(
                                worksheet_ordinal=worksheet_ordinal,
                                coordinate=anchor_coordinate,
                                row_index=merged_range.min_row,
                                column_index=merged_range.min_column,
                            )

                        diagnostic: Diagnostic | None = None
                        if value is None:
                            observation = CellObservation(
                                cell_ref=cell_ref,
                                value_kind=CellValueKind.BLANK,
                                data_type=cell.data_type or "n",
                                number_format=cell.number_format,
                                style_id=cell.style_id,
                                border_top=cell.border.top.style,
                                border_bottom=cell.border.bottom.style,
                                border_left=cell.border.left.style,
                                border_right=cell.border.right.style,
                                fill_type=cell.fill.fill_type,
                                font_bold=bool(cell.font.bold),
                                merged_range=merged_range,
                                merged_anchor=merged_anchor,
                            )
                        elif cell.data_type == "e":
                            diagnostic = Diagnostic(
                                code="EXCEL_UNSUPPORTED_ERROR_CELL",
                                severity=DiagnosticSeverity.ERROR,
                                message="Excel error cells are unsupported literal source values.",
                                worksheet_ordinal=worksheet_ordinal,
                                cell_ref=cell_ref,
                            )
                            observation = CellObservation(
                                cell_ref=cell_ref,
                                value_kind=CellValueKind.ERROR_VALUE,
                                data_type=cell.data_type,
                                unexpected_value=value if isinstance(value, str) else str(_diagnostic_scalar(value)),
                                number_format=cell.number_format,
                                style_id=cell.style_id,
                                border_top=cell.border.top.style,
                                border_bottom=cell.border.bottom.style,
                                border_left=cell.border.left.style,
                                border_right=cell.border.right.style,
                                fill_type=cell.fill.fill_type,
                                font_bold=bool(cell.font.bold),
                                merged_range=merged_range,
                                merged_anchor=merged_anchor,
                                diagnostics=(diagnostic,),
                            )
                        elif isinstance(value, str) and cell.data_type in ("s", "inlineStr", "str"):
                            observation = CellObservation(
                                cell_ref=cell_ref,
                                value_kind=CellValueKind.PRESENT_TEXT,
                                data_type=cell.data_type,
                                text_value=value,
                                number_format=cell.number_format,
                                style_id=cell.style_id,
>                               border_top=cell.border.top.style,
                                           ^^^^^^^^^^^^^^^^^^^^^
                                border_bottom=cell.border.bottom.style,
                                border_left=cell.border.left.style,
                                border_right=cell.border.right.style,
                                fill_type=cell.fill.fill_type,
                                font_bold=bool(cell.font.bold),
                                merged_range=merged_range,
                                merged_anchor=merged_anchor,
E                               AttributeError: 'NoneType' object has no attribute 'style'

src\ingestion\excel\reader.py:363: AttributeError

The above exception was the direct cause of the following exception:

    def test_reader_captures_cell_border_fill_font_and_style_evidence():
        workbook = Workbook()
        sheet = workbook.active
        sheet["A1"] = "Header"
        from openpyxl.styles import Border, Side, PatternFill, Font
        sheet["A1"].border = Border(bottom=Side(style="thin"))
        sheet["A1"].fill = PatternFill(fill_type="solid", fgColor="FFFF00")
        sheet["A1"].font = Font(bold=True)

>       result = read_excel_source(_xlsx_bytes(workbook))
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

src\tests\test_excel_source_reader.py:217:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

source = b'PK\x03\x04\x14\x00\x00\x00\x08\x00\xb8\xa6o]F\xc7MH\x95\x00\x00\x00\xcd\x00\x00\x00\x10\x00\x00\x00docProps/app.xmlM...x00\x80\x01q\x0f\x00\x00[Content_Types].xmlPK\x05\x06\x00\x00\x00\x00\t\x00\t\x00>\x02\x00\x00\xbd\x10\x00\x00\x00\x00'
source_ref = None, file_name = None, config = None

    def read_excel_source(
        source: BytesSource | PathSource,
        *,
        source_ref: str | None = None,
        file_name: str | None = None,
        config: ExcelReaderConfig | None = None,
    ) -> WorkbookObservation:
        """Read one XLSX source into an immutable observation.

        On a literal-value contract violation, raises ExcelSourceContractError after
        scanning the workbook; the exception exposes the complete observation and
        all cell-level diagnostics so the caller can reject the entire report.
        """
        settings = config or ExcelReaderConfig()
        payload, resolved_name, resolved_path = _read_source(
            source, file_name=file_name, max_file_bytes=settings.max_file_bytes
        )
        _preflight_package(payload, settings)

        try:
            workbook = load_workbook(
                BytesIO(payload),
                read_only=False,
                data_only=False,
                keep_links=False,
            )
        except Exception as exc:
            raise ExcelSourceReadError("EXCEL_WORKBOOK_UNREADABLE", f"openpyxl could not read XLSX: {exc}") from exc

        try:
            sheet_names = tuple(workbook.sheetnames)
            if not sheet_names:
                raise ExcelSourceReadError("EXCEL_NO_WORKSHEETS", "Workbook contains no worksheets.")
            if len(sheet_names) > settings.max_worksheets:
                raise ExcelSourceReadError(
                    "EXCEL_WORKSHEET_LIMIT_EXCEEDED",
                    f"Workbook has {len(sheet_names)} worksheets; configured limit is {settings.max_worksheets}.",
                )

            declared_table_specs: list[tuple[int, int, TableObservation]] = []
            worksheet_shells: list[tuple[object, int, tuple[CellRange, ...], tuple[object, ...]]] = []
            total_scan_cells = 0
            for worksheet_ordinal, worksheet_name in enumerate(sheet_names, start=1):
                worksheet = workbook[worksheet_name]
                max_row = max(int(worksheet.max_row or 1), 1)
                max_column = max(int(worksheet.max_column or 1), 1)
                scan_count = max_row * max_column
                total_scan_cells += scan_count
                if total_scan_cells > settings.max_total_cells:
                    raise ExcelSourceReadError(
                        "EXCEL_CELL_SCAN_LIMIT_EXCEEDED",
                        f"Workbook requires scanning {total_scan_cells} cells; configured limit is {settings.max_total_cells}.",
                    )
                merged_ranges = tuple(
                    sorted(
                        (_cell_range(r.min_row, r.min_col, r.max_row, r.max_col) for r in worksheet.merged_cells.ranges),
                        key=lambda item: (item.min_row, item.min_column, item.max_row, item.max_column),
                    )
                )
                worksheet_shells.append((worksheet, worksheet_ordinal, merged_ranges, ()))

            cell_observations: list[CellObservation] = []
            row_observations: list[RowObservation] = []
            column_observations: list[ColumnObservation] = []
            worksheet_observations: list[WorksheetObservation] = []
            table_observations: list[TableObservation] = []
            workbook_diagnostics: list[Diagnostic] = []

            for worksheet, worksheet_ordinal, merged_ranges, _ in worksheet_shells:
                populated_bounds: list[tuple[int, int]] = []
                row_cells: dict[int, list[CellRef]] = {}
                column_cells: dict[int, list[CellRef]] = {}
                local_diagnostics: list[Diagnostic] = []
                merged_by_coordinate: dict[tuple[int, int], CellRange] = {}
                for merged in merged_ranges:
                    for row_index in range(merged.min_row, merged.max_row + 1):
                        for column_index in range(merged.min_column, merged.max_column + 1):
                            merged_by_coordinate[(row_index, column_index)] = merged

                for row in worksheet.iter_rows():
                    for cell in row:
                        value = cell.value
                        has_literal = value is not None
                        has_style = bool(getattr(cell, "has_style", False))
                        in_merged_range = (cell.row, cell.column) in merged_by_coordinate
                        if not has_literal and not has_style and not in_merged_range:
                            continue
                        if has_literal or has_style:
                            populated_bounds.append((cell.row, cell.column))
                        cell_ref = CellRef(
                            worksheet_ordinal=worksheet_ordinal,
                            coordinate=cell.coordinate,
                            row_index=cell.row,
                            column_index=cell.column,
                        )
                        merged_range = merged_by_coordinate.get((cell.row, cell.column))
                        merged_anchor = None
                        if merged_range is not None:
                            anchor_coordinate = f"{get_column_letter(merged_range.min_column)}{merged_range.min_row}"
                            merged_anchor = CellRef(
                                worksheet_ordinal=worksheet_ordinal,
                                coordinate=anchor_coordinate,
                                row_index=merged_range.min_row,
                                column_index=merged_range.min_column,
                            )

                        diagnostic: Diagnostic | None = None
                        if value is None:
                            observation = CellObservation(
                                cell_ref=cell_ref,
                                value_kind=CellValueKind.BLANK,
                                data_type=cell.data_type or "n",
                                number_format=cell.number_format,
                                style_id=cell.style_id,
                                border_top=cell.border.top.style,
                                border_bottom=cell.border.bottom.style,
                                border_left=cell.border.left.style,
                                border_right=cell.border.right.style,
                                fill_type=cell.fill.fill_type,
                                font_bold=bool(cell.font.bold),
                                merged_range=merged_range,
                                merged_anchor=merged_anchor,
                            )
                        elif cell.data_type == "e":
                            diagnostic = Diagnostic(
                                code="EXCEL_UNSUPPORTED_ERROR_CELL",
                                severity=DiagnosticSeverity.ERROR,
                                message="Excel error cells are unsupported literal source values.",
                                worksheet_ordinal=worksheet_ordinal,
                                cell_ref=cell_ref,
                            )
                            observation = CellObservation(
                                cell_ref=cell_ref,
                                value_kind=CellValueKind.ERROR_VALUE,
                                data_type=cell.data_type,
                                unexpected_value=value if isinstance(value, str) else str(_diagnostic_scalar(value)),
                                number_format=cell.number_format,
                                style_id=cell.style_id,
                                border_top=cell.border.top.style,
                                border_bottom=cell.border.bottom.style,
                                border_left=cell.border.left.style,
                                border_right=cell.border.right.style,
                                fill_type=cell.fill.fill_type,
                                font_bold=bool(cell.font.bold),
                                merged_range=merged_range,
                                merged_anchor=merged_anchor,
                                diagnostics=(diagnostic,),
                            )
                        elif isinstance(value, str) and cell.data_type in ("s", "inlineStr", "str"):
                            observation = CellObservation(
                                cell_ref=cell_ref,
                                value_kind=CellValueKind.PRESENT_TEXT,
                                data_type=cell.data_type,
                                text_value=value,
                                number_format=cell.number_format,
                                style_id=cell.style_id,
                                border_top=cell.border.top.style,
                                border_bottom=cell.border.bottom.style,
                                border_left=cell.border.left.style,
                                border_right=cell.border.right.style,
                                fill_type=cell.fill.fill_type,
                                font_bold=bool(cell.font.bold),
                                merged_range=merged_range,
                                merged_anchor=merged_anchor,
                            )
                        elif isinstance(value, (int, float)) and not isinstance(value, bool) and cell.data_type == "n":
                            observation = CellObservation(
                                cell_ref=cell_ref,
                                value_kind=CellValueKind.PRESENT_NUMBER,
                                data_type=cell.data_type,
                                numeric_value=value,
                                number_format=cell.number_format,
                                style_id=cell.style_id,
                                border_top=cell.border.top.style,
                                border_bottom=cell.border.bottom.style,
                                border_left=cell.border.left.style,
                                border_right=cell.border.right.style,
                                fill_type=cell.fill.fill_type,
                                font_bold=bool(cell.font.bold),
                                merged_range=merged_range,
                                merged_anchor=merged_anchor,
                            )
                        else:
                            diagnostic = Diagnostic(
                                code="EXCEL_UNSUPPORTED_CELL_VALUE",
                                severity=DiagnosticSeverity.ERROR,
                                message="This populated cell kind is not an accepted literal text or numeric value; formulas are prohibited.",
                                worksheet_ordinal=worksheet_ordinal,
                                cell_ref=cell_ref,
                                details=(DiagnosticDetail("data_type", str(cell.data_type)),),
                            )
                            observation = CellObservation(
                                cell_ref=cell_ref,
                                value_kind=CellValueKind.UNEXPECTED_NON_TEXT,
                                data_type=cell.data_type or "n",
                                unexpected_value=_diagnostic_scalar(value),
                                number_format=cell.number_format,
                                style_id=cell.style_id,
                                border_top=cell.border.top.style,
                                border_bottom=cell.border.bottom.style,
                                border_left=cell.border.left.style,
                                border_right=cell.border.right.style,
                                fill_type=cell.fill.fill_type,
                                font_bold=bool(cell.font.bold),
                                merged_range=merged_range,
                                merged_anchor=merged_anchor,
                                diagnostics=(diagnostic,),
                            )

                        cell_observations.append(observation)
                        row_cells.setdefault(cell.row, []).append(cell_ref)
                        column_cells.setdefault(cell.column, []).append(cell_ref)
                        if diagnostic is not None:
                            local_diagnostics.append(diagnostic)
                            workbook_diagnostics.append(diagnostic)

                used_range = None
                for merged in merged_ranges:
                    populated_bounds.extend(((merged.min_row, merged.min_column), (merged.max_row, merged.max_column)))
                if populated_bounds:
                    used_range = _cell_range(
                        min(row for row, _ in populated_bounds),
                        min(column for _, column in populated_bounds),
                        max(row for row, _ in populated_bounds),
                        max(column for _, column in populated_bounds),
                    )

                declared_tables: list[tuple[str, str | None, CellRange]] = []
                for table_name in worksheet.tables:
                    table = worksheet.tables[table_name]
                    table_ref = getattr(table, "ref", None)
                    if not table_ref:
                        continue
                    try:
                        from openpyxl.utils.cell import range_boundaries
                        min_col, min_row, max_col, max_row = range_boundaries(table_ref)
                        bounds = _cell_range(min_row, min_col, max_row, max_col)
                    except Exception:
                        continue
                    declared_tables.append((str(table_name), getattr(table, "displayName", None), bounds))
                declared_tables.sort(key=lambda item: (item[2].min_row, item[2].min_column, item[0]))
                worksheet_table_ordinals: list[int] = []
                for name, display_name, bounds in declared_tables:
                    table_ordinal = len(table_observations) + 1
                    worksheet_table_ordinals.append(table_ordinal)
                    table_observations.append(
                        TableObservation(
                            worksheet_ordinal=worksheet_ordinal,
                            table_ordinal=table_ordinal,
                            bounds=bounds,
                            detection_method="excel_structured_table",
                            detection_version="1",
                            status=StructureStatus.RESOLVED,
                            header_rows=(bounds.min_row,) if getattr(table, "headerRowCount", 1) else (),
                            row_refs=tuple(range(bounds.min_row, bounds.max_row + 1)),
                            column_refs=tuple(range(bounds.min_column, bounds.max_column + 1)),
                            diagnostics=(),
                        )
                    )

                if used_range is not None:
                    for row_index in range(used_range.min_row, used_range.max_row + 1):
                        row_observations.append(
                            RowObservation(
                                worksheet_ordinal=worksheet_ordinal,
                                row_index=row_index,
                                cell_refs=tuple(sorted(row_cells.get(row_index, ()), key=lambda ref: ref.column_index)),
                            )
                        )
                    for column_index in range(used_range.min_column, used_range.max_column + 1):
                        column_observations.append(
                            ColumnObservation(
                                worksheet_ordinal=worksheet_ordinal,
                                column_index=column_index,
                                cell_refs=tuple(sorted(column_cells.get(column_index, ()), key=lambda ref: ref.row_index)),
                            )
                        )

                worksheet_observations.append(
                    WorksheetObservation(
                        ordinal=worksheet_ordinal,
                        literal_name=worksheet.title,
                        visibility=_visibility(worksheet.sheet_state),
                        used_range=used_range,
                        merged_ranges=merged_ranges,
                        declared_tables=tuple(
                            DeclaredTableObservation(name=name, display_name=display_name, bounds=bounds)
                            for name, display_name, bounds in declared_tables
                        ),
                        candidate_table_ordinals=tuple(worksheet_table_ordinals),
                        diagnostics=tuple(local_diagnostics),
                    )
                )

            date_system = _date_system(workbook.epoch)
            metadata = WorkbookMetadataObservation(
                date_system=date_system,
                workbook_properties=_workbook_properties(workbook),
                unsupported_features=(),
            )
            observation = WorkbookObservation(
                source=SourceArtifactObservation(
                    source_ref=source_ref or resolved_path,
                    file_name=resolved_name,
                    format="xlsx",
                    sha256=sha256(payload).hexdigest(),
                    byte_length=len(payload),
                ),
                reader=ReaderProvenance(
                    reader_name="openpyxl",
                    reader_version=openpyxl.__version__,
                    profile_name=settings.profile_name,
                    profile_version=settings.profile_version,
                    dto_schema_version=settings.dto_schema_version,
                ),
                metadata=metadata,
                worksheets=tuple(worksheet_observations),
                tables=tuple(table_observations),
                rows=tuple(row_observations),
                columns=tuple(column_observations),
                cells=tuple(cell_observations),
                diagnostics=tuple(workbook_diagnostics),
            )
            if workbook_diagnostics:
                raise ExcelSourceContractError(observation)
            return observation
        except ExcelSourceReadError:
            raise
        except Exception as exc:
>           raise ExcelSourceReadError(
                "EXCEL_WORKBOOK_STRUCTURE_UNREADABLE",
                f"Workbook structure could not be observed reliably: {exc}",
            ) from exc
E           src.ingestion.excel.reader.ExcelSourceReadError: Workbook structure could not be observed reliably: 'NoneType' object has no attribute 'style'

src\ingestion\excel\reader.py:536: ExcelSourceReadError
=============================================== short test summary info ===============================================
FAILED src/tests/test_excel_source_reader.py::test_reader_captures_cell_border_fill_font_and_style_evidence - src.ingestion.excel.reader.ExcelSourceReadError: Workbook structure could not be observed reliably: 'NoneType' obje...
1 failed, 37 passed in 1.63s