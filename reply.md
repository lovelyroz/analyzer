(analyzer) PS D:\Winprojects\analyzer> .\.venv\Scripts\python.exe -m pytest -q --basetemp .pytest_db_consolidation_002_20261121 src/tests/test_approval_catalog.py src/tests/test_financial_numbers.py src/tests/test_excel_canonical_input.py src/tests/test_canonical_ingestion_admission.py src/tests/test_excel_adapter.py src/tests/test_canonical_writer.py src/tests/test_canonical_queries.py src/tests/test_market_fx_atomic_ingestion.py src/tests/test_market_fx_adapters.py src/tests/test_ingestion_fx.py src/tests/test_stage1_database_integrity.py src/tests/test_task017_model_constraints.py
...............................................................................F................................ [ 72%]
..........................................                                                                       [100%]
====================================================== FAILURES =======================================================
_________________________ test_synthetic_xlsx_runs_reader_match_admission_writer_and_readback _________________________

db = (Engine(sqlite:///D:\winprojects\analyzer\.pytest_db_consolidation_002_20261121\test_synthetic_xlsx_runs_reade0\canoni..._consolidation_002_20261121\test_synthetic_xlsx_runs_reade0\canonical.sqlite), autoflush=True, expire_on_commit=False))

    def test_synthetic_xlsx_runs_reader_match_admission_writer_and_readback(db):
        _engine, factory = db
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Annual"
        sheet["A1"] = "Revenue"
        sheet["B1"] = "Amount"
        sheet["B2"] = "125.50"
        stream = BytesIO()
        workbook.save(stream)
        source = stream.getvalue()
        source_hash = sha256(source).hexdigest()
        template = TemplateVersion(
            template_id="template-fixture", version="1", approved=True,
            source_workbook_sha256="a" * 64, worksheet_name="Annual", worksheet_ordinal=1,
            tables=(TableRule(code="income", title_cell="A1", title_text="Revenue",
                              bounds="A1:B2", header_cells=(("B1", "Amount"),),
                              owned_ranges=("B2:B2",)),),
        )
        with factory.begin() as session:
            session.add(CanonicalApproval(
                approval_kind="template",
                external_identity=f"{template.template_id}:{template.version}:{template.template_sha256}",
                approval_ref="approval-template-e2e", is_active=True,
                scope_json=json.dumps({"company_id": "company-1", "report_type_id": "PERIODIC_FINANCIAL",
                                       "template_id": template.template_id, "template_version": template.version,
                                       "template_sha256": template.template_sha256}, sort_keys=True, separators=(",", ":")),
            ))

        def approved(identity, reference):
            return ApprovedSelection(identity=identity, approved=True, candidate_count=1,
                                     approval_ref=reference)

        spec = CanonicalInputSpec(
            company=approved("company-1", "approval-company"),
            report_type=approved("PERIODIC_FINANCIAL", "approval-report-type"),
            report_version=approved("version-1", "approval-version-1"),
            metric=approved("metric-sales", "approval-metric"),
            source_unit=approved("unit-rial", "approval-unit"),
            source_currency=approved("currency-irr", "approval-currency"),
            source_scale=approved("scale-unit", "approval-scale"),
            period=JalaliPeriod(TemporalType.DURATION, (1404, 1, 1), (1404, 3, 31), DurationBasis.YTD),
            period_mapping=approved("period-map-q1", "approval-period"),
            source_label=approved("label-sales", "approval-label-sales"),
            source_header=approved("header-current", "approval-header-current"),
        )
        revision = RevisionContext(
            report_id="report-1", report_version_id="version-1", company_id="company-1",
            source_identity="source-e2e", revision_identity="revision-e2e",
            source_artifact_sha256=source_hash, extraction_standard_id="standard-v1",
            extraction_standard_approval_ref="approval-standard-v1",
        )
>       adapted, result = ingest_excel_source(
            source, template=template, selections_by_coordinate={"B2": spec},
            revision=revision, metadata=_metadata(), session_factory=factory,
            expected_source_sha256=source_hash,
        )

src\tests\test_canonical_writer.py:230:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

source = b'PK\x03\x04\x14\x00\x00\x00\x08\x00a\x9fu]F\xc7MH\x95\x00\x00\x00\xcd\x00\x00\x00\x10\x00\x00\x00docProps/app.xmlM\xc...x00\x80\x01X\x0f\x00\x00[Content_Types].xmlPK\x05\x06\x00\x00\x00\x00\t\x00\t\x00>\x02\x00\x00\xa4\x10\x00\x00\x00\x00'
template = TemplateVersion(template_id='template-fixture', version='1', approved=True, source_workbook_sha256='aaaaaaaaaaaaaaaaaa...tle_search_range=None, header_cells=(('B1', 'Amount'),), partitions=(), owned_ranges=('B2:B2',), excluded_ranges=()),))
selections_by_coordinate = {'B2': CanonicalInputSpec(company=ApprovedSelection(identity='company-1', approved=True, candidate_count=1, approval_r...n(identity='header-current', approved=True, candidate_count=1, approval_ref='approval-header-current'), dimensions=())}
revision = RevisionContext(report_id='report-1', report_version_id='version-1', company_id='company-1', source_identity='source-e...raction_standard_id='standard-v1', extraction_standard_approval_ref='approval-standard-v1', supersedes_version_id=None)
metadata = ReportWriteMetadata(title='Periodic report', version_number=1, publication_datetime=datetime.datetime(2025, 4, 1, 0, 0...imezone.utc), is_audited=False, is_restated=False, scenario_approval_ref='approval-scenario-actual', scenario='ACTUAL')
session_factory = sessionmaker(class_='Session', bind=Engine(sqlite:///D:\winprojects\analyzer\.pytest_db_consolidation_002_20261121\test_synthetic_xlsx_runs_reade0\canonical.sqlite), autoflush=True, expire_on_commit=False)
adapter_options = {'expected_source_sha256': 'c7a1138941f0292161d402441d40b91b44a3892ac2ca127bca1925ee65e30a72'}

    def ingest_excel_source(
        source: object,
        *,
        template: object,
        selections_by_coordinate: Mapping[str, object],
        revision: object,
        metadata: ReportWriteMetadata,
        session_factory: sessionmaker[Session],
        **adapter_options: object,
    ) -> tuple[object, CanonicalWriteResult]:
        """Run reader→matcher→admission→writer with a durable STARTED audit row."""
        from src.ingestion.excel.adapter import adapt_excel_source

        with session_factory() as session:
            run = IngestionRun(source="EXCEL", status="STARTED", records_found=0,
                               records_inserted=0, records_updated=0, records_failed=0)
            session.add(run)
            session.commit()
            ingestion_id = run.ingestion_id

        def validate_approvals(plan: CanonicalPersistencePlan) -> None:
            with session_factory() as validation_session:
                with validation_session.begin():
                    resolve_plan_approvals(validation_session, plan, metadata)

        try:
            adapted = adapt_excel_source(
                source, template=template, selections_by_coordinate=selections_by_coordinate,
                admit=True, revision=revision, approval_validator=validate_approvals,
                **adapter_options,
            )
            if adapted.diagnostics or adapted.admission_plan is None:
                failure_code = adapted.diagnostics[0].code if adapted.diagnostics else "EXCEL_ADMISSION_REJECTED"
                _mark_failed(session_factory, ingestion_id, failure_code, max(1, len(adapted.submissions)))
>               raise CanonicalWriteError(failure_code)
E               src.ingestion.canonical_writer.CanonicalWriteError: APPROVAL_SCOPE_MISMATCH

src\ingestion\canonical_writer.py:315: CanonicalWriteError
=============================================== short test summary info ===============================================
FAILED src/tests/test_canonical_writer.py::test_synthetic_xlsx_runs_reader_match_admission_writer_and_readback - src.ingestion.canonical_writer.CanonicalWriteError: APPROVAL_SCOPE_MISMATCH
1 failed, 153 passed in 628.73s (0:10:28)