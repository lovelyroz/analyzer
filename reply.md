(analyzer) PS D:\Winprojects\analyzer> .\.venv\Scripts\python.exe -m pytest -q --basetemp .pytest_db_consolidation_002_20261121 src/tests/test_approval_catalog.py src/tests/test_financial_numbers.py src/tests/test_excel_canonical_input.py src/tests/test_canonical_ingestion_admission.py src/tests/test_excel_adapter.py src/tests/test_canonical_writer.py src/tests/test_canonical_queries.py src/tests/test_market_fx_atomic_ingestion.py src/tests/test_market_fx_adapters.py src/tests/test_ingestion_fx.py src/tests/test_stage1_database_integrity.py src/tests/test_task017_model_constraints.py
................................................F..............................F.....F...F.FFFFFFFFF.....F...... [ 72%]
..........................................                                                                       [100%]
====================================================== FAILURES =======================================================
___________________________ test_rejects_missing_source_coordinate_and_invalid_numeric_text ___________________________

    def test_rejects_missing_source_coordinate_and_invalid_numeric_text():
        observation, match = _inputs()
        with pytest.raises(CandidateValidationError, match="SOURCE_COORDINATE_MISSING"):
            build_candidate(observation, match, coordinate="", spec=_spec())
        with pytest.raises(CandidateValidationError, match="STRUCTURAL_OWNERSHIP_MISSING"):
            build_candidate(observation, match, coordinate="C9", spec=_spec())
>       with pytest.raises(CandidateValidationError, match="SOURCE_NUMBER_INVALID"):
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E       Failed: DID NOT RAISE CandidateValidationError

src\tests\test_excel_canonical_input.py:216: Failed
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

source = b'PK\x03\x04\x14\x00\x00\x00\x08\x00\xa0\x9cu]F\xc7MH\x95\x00\x00\x00\xcd\x00\x00\x00\x10\x00\x00\x00docProps/app.xmlM...x00\x80\x01X\x0f\x00\x00[Content_Types].xmlPK\x05\x06\x00\x00\x00\x00\t\x00\t\x00>\x02\x00\x00\xa4\x10\x00\x00\x00\x00'
template = TemplateVersion(template_id='template-fixture', version='1', approved=True, source_workbook_sha256='aaaaaaaaaaaaaaaaaa...tle_search_range=None, header_cells=(('B1', 'Amount'),), partitions=(), owned_ranges=('B2:B2',), excluded_ranges=()),))
selections_by_coordinate = {'B2': CanonicalInputSpec(company=ApprovedSelection(identity='company-1', approved=True, candidate_count=1, approval_r...n(identity='header-current', approved=True, candidate_count=1, approval_ref='approval-header-current'), dimensions=())}
revision = RevisionContext(report_id='report-1', report_version_id='version-1', company_id='company-1', source_identity='source-e...raction_standard_id='standard-v1', extraction_standard_approval_ref='approval-standard-v1', supersedes_version_id=None)
metadata = ReportWriteMetadata(title='Periodic report', version_number=1, publication_datetime=datetime.datetime(2025, 4, 1, 0, 0...imezone.utc), is_audited=False, is_restated=False, scenario_approval_ref='approval-scenario-actual', scenario='ACTUAL')
session_factory = sessionmaker(class_='Session', bind=Engine(sqlite:///D:\winprojects\analyzer\.pytest_db_consolidation_002_20261121\test_synthetic_xlsx_runs_reade0\canonical.sqlite), autoflush=True, expire_on_commit=False)
adapter_options = {'expected_source_sha256': '7f7bd7b450518f62eb1f6bb9db61bfefa1efa6f512ad1ec074696a010471021d'}

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
_ test_migration_ten_duplicate_preflight_rolls_back_and_preserves_rows[market_daily-uq_market_daily_jalali_identity-INSERT INTO market_daily (company_id,jalali_year,jalali_month,jalali_day) VALUES (1,1404,1,1),(1,1404,1,1)] _

self = <sqlalchemy.engine.base.Connection object at 0x000001FEF9C8EBA0>
dialect = <sqlalchemy.dialects.sqlite.pysqlite.SQLiteDialect_pysqlite object at 0x000001FEF9E3D5E0>
context = <sqlalchemy.dialects.sqlite.base.SQLiteExecutionContext object at 0x000001FEF9EADDF0>
statement = <sqlalchemy.dialects.sqlite.base.SQLiteCompiler object at 0x000001FEF9EAE060>, parameters = [()]

    def _exec_single_context(
        self,
        dialect: Dialect,
        context: ExecutionContext,
        statement: Union[str, Compiled],
        parameters: Optional[_AnyMultiExecuteParams],
    ) -> CursorResult[Any]:
        """continue the _execute_context() method for a single DBAPI
        cursor.execute() or cursor.executemany() call.

        """
        if dialect.bind_typing is BindTyping.SETINPUTSIZES:
            generic_setinputsizes = context._prepare_set_input_sizes()

            if generic_setinputsizes:
                try:
                    dialect.do_set_input_sizes(
                        context.cursor, generic_setinputsizes, context
                    )
                except BaseException as e:
                    self._handle_dbapi_exception(
                        e, str(statement), parameters, None, context
                    )

        cursor, str_statement, parameters = (
            context.cursor,
            context.statement,
            context.parameters,
        )

        effective_parameters: Optional[_AnyExecuteParams]

        if not context.executemany:
            effective_parameters = parameters[0]
        else:
            effective_parameters = parameters

        if self._has_events or self.engine._has_events:
            for fn in self.dispatch.before_cursor_execute:
                str_statement, effective_parameters = fn(
                    self,
                    cursor,
                    str_statement,
                    effective_parameters,
                    context,
                    context.executemany,
                )

        if self._echo:
            self._log_info(str_statement)

            stats = context._get_cache_stats()

            if not self.engine.hide_parameters:
                self._log_info(
                    "[%s] %r",
                    stats,
                    sql_util._repr_params(
                        effective_parameters,
                        batches=10,
                        ismulti=context.executemany,
                    ),
                )
            else:
                self._log_info(
                    "[%s] [SQL parameters hidden due to hide_parameters=True]",
                    stats,
                )

        evt_handled: bool = False
        try:
            if context.execute_style is ExecuteStyle.EXECUTEMANY:
                effective_parameters = cast(
                    "_CoreMultiExecuteParams", effective_parameters
                )
                if self.dialect._has_events:
                    for fn in self.dialect.dispatch.do_executemany:
                        if fn(
                            cursor,
                            str_statement,
                            effective_parameters,
                            context,
                        ):
                            evt_handled = True
                            break
                if not evt_handled:
                    self.dialect.do_executemany(
                        cursor,
                        str_statement,
                        effective_parameters,
                        context,
                    )
            elif not effective_parameters and context.no_parameters:
                if self.dialect._has_events:
                    for fn in self.dialect.dispatch.do_execute_no_params:
                        if fn(cursor, str_statement, context):
                            evt_handled = True
                            break
                if not evt_handled:
                    self.dialect.do_execute_no_params(
                        cursor, str_statement, context
                    )
            else:
                effective_parameters = cast(
                    "_CoreSingleExecuteParams", effective_parameters
                )
                if self.dialect._has_events:
                    for fn in self.dialect.dispatch.do_execute:
                        if fn(
                            cursor,
                            str_statement,
                            effective_parameters,
                            context,
                        ):
                            evt_handled = True
                            break
                if not evt_handled:
>                   self.dialect.do_execute(
                        cursor, str_statement, effective_parameters, context
                    )

.venv\Lib\site-packages\sqlalchemy\engine\base.py:1969:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = <sqlalchemy.dialects.sqlite.pysqlite.SQLiteDialect_pysqlite object at 0x000001FEF9E3D5E0>
cursor = <sqlite3.Cursor object at 0x000001FEF7137440>
statement = "INSERT INTO companies (ticker,company_name,industry_id) VALUES ('DUP','Duplicate',1)", parameters = ()
context = <sqlalchemy.dialects.sqlite.base.SQLiteExecutionContext object at 0x000001FEF9EADDF0>

    def do_execute(self, cursor, statement, parameters, context=None):
>       cursor.execute(statement, parameters)
E       sqlite3.IntegrityError: NOT NULL constraint failed: companies.status

.venv\Lib\site-packages\sqlalchemy\engine\default.py:952: IntegrityError

The above exception was the direct cause of the following exception:

monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x000001FEF9E32B10>
tmp_path = WindowsPath('D:/winprojects/analyzer/.pytest_db_consolidation_002_20261121/test_migration_ten_duplicate_p0')
table_name = 'market_daily', drop_index = 'uq_market_daily_jalali_identity'
insert_sql = 'INSERT INTO market_daily (company_id,jalali_year,jalali_month,jalali_day) VALUES (1,1404,1,1),(1,1404,1,1)'

    @pytest.mark.parametrize("table_name,drop_index,insert_sql", [
        ("market_daily", "uq_market_daily_jalali_identity",
         "INSERT INTO market_daily (company_id,jalali_year,jalali_month,jalali_day) VALUES (1,1404,1,1),(1,1404,1,1)"),
        ("fx_rates", "uq_fx_jalali_identity",
         "INSERT INTO fx_rates (jalali_year,jalali_month,jalali_day,currency_from,currency_to,rate,rate_type) "
         "VALUES (1404,1,1,'USD','IRR',100,'FREE_MARKET'),(1404,1,1,'USD','IRR',101,'FREE_MARKET')"),
    ])
    def test_migration_ten_duplicate_preflight_rolls_back_and_preserves_rows(
        monkeypatch, tmp_path, table_name, drop_index, insert_sql,
    ):
        engine = create_engine(f"sqlite:///{tmp_path / (table_name + '-duplicate.sqlite')}")
        migrations = tuple(migration_runner._migration_list())
        monkeypatch.setattr(migration_runner, "_migration_list", lambda: migrations[:9])
        assert MigrationRunner(engine).upgrade() == 9
        if table_name == "market_daily":
            with engine.begin() as connection:
                connection.execute(text("INSERT INTO industries (industry_code,industry_name) VALUES ('BANK','Bank')"))
>               connection.execute(text("INSERT INTO companies (ticker,company_name,industry_id) VALUES ('DUP','Duplicate',1)"))

src\tests\test_canonical_writer.py:345:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
.venv\Lib\site-packages\sqlalchemy\engine\base.py:1421: in execute
    return meth(
.venv\Lib\site-packages\sqlalchemy\sql\elements.py:526: in _execute_on_connection
    return connection._execute_clauseelement(
.venv\Lib\site-packages\sqlalchemy\engine\base.py:1643: in _execute_clauseelement
    ret = self._execute_context(
.venv\Lib\site-packages\sqlalchemy\engine\base.py:1848: in _execute_context
    return self._exec_single_context(
.venv\Lib\site-packages\sqlalchemy\engine\base.py:1988: in _exec_single_context
    self._handle_dbapi_exception(
.venv\Lib\site-packages\sqlalchemy\engine\base.py:2365: in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
.venv\Lib\site-packages\sqlalchemy\engine\base.py:1969: in _exec_single_context
    self.dialect.do_execute(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = <sqlalchemy.dialects.sqlite.pysqlite.SQLiteDialect_pysqlite object at 0x000001FEF9E3D5E0>
cursor = <sqlite3.Cursor object at 0x000001FEF7137440>
statement = "INSERT INTO companies (ticker,company_name,industry_id) VALUES ('DUP','Duplicate',1)", parameters = ()
context = <sqlalchemy.dialects.sqlite.base.SQLiteExecutionContext object at 0x000001FEF9EADDF0>

    def do_execute(self, cursor, statement, parameters, context=None):
>       cursor.execute(statement, parameters)
E       sqlalchemy.exc.IntegrityError: (sqlite3.IntegrityError) NOT NULL constraint failed: companies.status
E       [SQL: INSERT INTO companies (ticker,company_name,industry_id) VALUES ('DUP','Duplicate',1)]
E       (Background on this error at: https://sqlalche.me/e/20/gkpj)

.venv\Lib\site-packages\sqlalchemy\engine\default.py:952: IntegrityError
__________________________ test_writer_persists_jalali_ytd_integer_fact_and_exact_provenance __________________________

db = (Engine(sqlite:///D:\winprojects\analyzer\.pytest_db_consolidation_002_20261121\test_writer_persists_jalali_yt0\canoni..._consolidation_002_20261121\test_writer_persists_jalali_yt0\canonical.sqlite), autoflush=True, expire_on_commit=False))

    def test_writer_persists_jalali_ytd_integer_fact_and_exact_provenance(db):
        _engine, factory = db
>       result = write_canonical_plan(_plan(), _metadata(), factory)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

src\tests\test_canonical_writer.py:398:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\ingestion\canonical_writer.py:82: in write_canonical_plan
    result = _write_in_transaction(session, plan, metadata, effective_ingestion_id)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\ingestion\canonical_writer.py:98: in _write_in_transaction
    company_id, industry_code, template_approval_ref = resolve_plan_approvals(session, plan, metadata)
                                                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\ingestion\canonical_writer.py:272: in resolve_plan_approvals
    _validate_fact(session, fact, company_id, plan, industry.industry_code) for fact in plan.facts
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\ingestion\canonical_writer.py:451: in _validate_fact
    scope=_approval_scope(fact, resolved_kind, industry_code, identity=identity))
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

fact = PlannedFact(company_id='company-1', report_type_id='PERIODIC_FINANCIAL', report_id='report-1', report_version_id='vers...ksheet_ordinal=1, worksheet_name='Annual', source_coordinate='B2', source_value_kind='PRESENT_TEXT', source_token=None)
kind = 'industry', industry_code = 'BANK', identity = 'BANK'

    def _approval_scope(fact: PlannedFact, kind: str, industry_code: str,
                        *, identity: str | None = None) -> dict[str, str]:
        scopes: dict[str, dict[str, str]] = {
            "company": {"industry_code": industry_code},
            "report_type": {"company_id": fact.company_id},
            "report_version": {"company_id": fact.company_id, "report_type_id": fact.report_type_id},
            "metric": {"industry_code": industry_code},
            "source_unit": {"metric_id": fact.metric_id},
            "source_currency": {"metric_id": fact.metric_id},
            "source_scale": {"metric_id": fact.metric_id},
            "period_mapping": {"report_type_id": fact.report_type_id,
                               "temporal_type": fact.period_identity[0],
                               "duration_basis": fact.duration_basis or "INSTANT"},
            "source_label": {"report_type_id": fact.report_type_id,
                             "template_id": fact.template_id, "template_version": fact.template_version,
                             "template_sha256": fact.template_sha256.lower()},
            "source_header": {"report_type_id": fact.report_type_id,
                              "template_id": fact.template_id, "template_version": fact.template_version,
                              "template_sha256": fact.template_sha256.lower()},
            "dimension": {"company_id": fact.company_id, "report_type_id": fact.report_type_id},
            "other_metric_rule": {"report_type_id": fact.report_type_id, "metric_id": fact.metric_id},
            "zero_fallback_rule": {"report_type_id": fact.report_type_id, "metric_id": fact.metric_id},
        }
        if kind == "dimension_value":
            dimensions = [dimension for dimension, value in fact.dimensions
                          if value == identity]
            if len(dimensions) != 1:
                raise CanonicalWriteError("APPROVAL_SCOPE_AMBIGUOUS")
            scopes[kind] = {"company_id": fact.company_id, "report_type_id": fact.report_type_id,
                            "dimension_id": dimensions[0]}
        if kind not in scopes:
>           raise CanonicalWriteError("APPROVAL_SCOPE_KIND_UNSUPPORTED")
E           src.ingestion.canonical_writer.CanonicalWriteError: APPROVAL_SCOPE_KIND_UNSUPPORTED

src\ingestion\canonical_writer.py:496: CanonicalWriteError
_______________________ test_monthly_activity_ytd_is_not_subject_to_periodic_quarter_alignment ________________________

db = (Engine(sqlite:///D:\winprojects\analyzer\.pytest_db_consolidation_002_20261121\test_monthly_activity_ytd_is_n0\canoni..._consolidation_002_20261121\test_monthly_activity_ytd_is_n0\canonical.sqlite), autoflush=True, expire_on_commit=False))

    def test_monthly_activity_ytd_is_not_subject_to_periodic_quarter_alignment(db):
        _engine, factory = db
        with factory.begin() as session:
            shared_kinds = {"company", "industry", "metric", "source_unit", "source_currency", "source_scale"}
            for kind, identity, reference in _approval_rows("version-1", "MONTHLY_ACTIVITY"):
                if kind in shared_kinds:
                    continue
                session.add(CanonicalApproval(
                    approval_kind=kind, external_identity=identity, approval_ref=reference,
                    is_active=True,
                    scope_json=json.dumps(_approval_scope(kind, "MONTHLY_ACTIVITY", identity),
                                          sort_keys=True, separators=(",", ":")),
                ))
        plan = _plan(
            report_type_id="MONTHLY_ACTIVITY",
            period_identity=("DURATION", (1404, 1, 1), (1404, 2, 31)),
        )
>       result = write_canonical_plan(plan, _metadata(), factory)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

src\tests\test_canonical_writer.py:436:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\ingestion\canonical_writer.py:82: in write_canonical_plan
    result = _write_in_transaction(session, plan, metadata, effective_ingestion_id)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\ingestion\canonical_writer.py:98: in _write_in_transaction
    company_id, industry_code, template_approval_ref = resolve_plan_approvals(session, plan, metadata)
                                                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\ingestion\canonical_writer.py:272: in resolve_plan_approvals
    _validate_fact(session, fact, company_id, plan, industry.industry_code) for fact in plan.facts
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\ingestion\canonical_writer.py:451: in _validate_fact
    scope=_approval_scope(fact, resolved_kind, industry_code, identity=identity))
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

fact = PlannedFact(company_id='company-1', report_type_id='MONTHLY_ACTIVITY', report_id='report-1', report_version_id='versio...ksheet_ordinal=1, worksheet_name='Annual', source_coordinate='B2', source_value_kind='PRESENT_TEXT', source_token=None)
kind = 'industry', industry_code = 'BANK', identity = 'BANK'

    def _approval_scope(fact: PlannedFact, kind: str, industry_code: str,
                        *, identity: str | None = None) -> dict[str, str]:
        scopes: dict[str, dict[str, str]] = {
            "company": {"industry_code": industry_code},
            "report_type": {"company_id": fact.company_id},
            "report_version": {"company_id": fact.company_id, "report_type_id": fact.report_type_id},
            "metric": {"industry_code": industry_code},
            "source_unit": {"metric_id": fact.metric_id},
            "source_currency": {"metric_id": fact.metric_id},
            "source_scale": {"metric_id": fact.metric_id},
            "period_mapping": {"report_type_id": fact.report_type_id,
                               "temporal_type": fact.period_identity[0],
                               "duration_basis": fact.duration_basis or "INSTANT"},
            "source_label": {"report_type_id": fact.report_type_id,
                             "template_id": fact.template_id, "template_version": fact.template_version,
                             "template_sha256": fact.template_sha256.lower()},
            "source_header": {"report_type_id": fact.report_type_id,
                              "template_id": fact.template_id, "template_version": fact.template_version,
                              "template_sha256": fact.template_sha256.lower()},
            "dimension": {"company_id": fact.company_id, "report_type_id": fact.report_type_id},
            "other_metric_rule": {"report_type_id": fact.report_type_id, "metric_id": fact.metric_id},
            "zero_fallback_rule": {"report_type_id": fact.report_type_id, "metric_id": fact.metric_id},
        }
        if kind == "dimension_value":
            dimensions = [dimension for dimension, value in fact.dimensions
                          if value == identity]
            if len(dimensions) != 1:
                raise CanonicalWriteError("APPROVAL_SCOPE_AMBIGUOUS")
            scopes[kind] = {"company_id": fact.company_id, "report_type_id": fact.report_type_id,
                            "dimension_id": dimensions[0]}
        if kind not in scopes:
>           raise CanonicalWriteError("APPROVAL_SCOPE_KIND_UNSUPPORTED")
E           src.ingestion.canonical_writer.CanonicalWriteError: APPROVAL_SCOPE_KIND_UNSUPPORTED

src\ingestion\canonical_writer.py:496: CanonicalWriteError
_____________________ test_periodic_financial_ytd_still_requires_three_six_nine_or_twelve_months ______________________

db = (Engine(sqlite:///D:\winprojects\analyzer\.pytest_db_consolidation_002_20261121\test_periodic_financial_ytd_st0\canoni..._consolidation_002_20261121\test_periodic_financial_ytd_st0\canonical.sqlite), autoflush=True, expire_on_commit=False))

    def test_periodic_financial_ytd_still_requires_three_six_nine_or_twelve_months(db):
        _engine, factory = db
        plan = _plan(period_identity=("DURATION", (1404, 1, 1), (1404, 2, 31)))
>       with pytest.raises(CanonicalWriteError, match="BANK_YTD_PERIOD_ALIGNMENT_INVALID"):
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E       AssertionError: Regex pattern did not match.
E         Expected regex: 'BANK_YTD_PERIOD_ALIGNMENT_INVALID'
E         Actual message: 'APPROVAL_SCOPE_KIND_UNSUPPORTED'

src\tests\test_canonical_writer.py:448: AssertionError
________________________ test_writer_accepts_explicit_non_calendar_fiscal_start_and_ytd_period ________________________

db = (Engine(sqlite:///D:\winprojects\analyzer\.pytest_db_consolidation_002_20261121\test_writer_accepts_explicit_n0\canoni..._consolidation_002_20261121\test_writer_accepts_explicit_n0\canonical.sqlite), autoflush=True, expire_on_commit=False))

    def test_writer_accepts_explicit_non_calendar_fiscal_start_and_ytd_period(db):
        _engine, factory = db
        with factory.begin() as session:
            session.add(CanonicalApproval(
                approval_kind="fiscal_year_start_month", external_identity="company-1:7",
                approval_ref="approval-fiscal-start-7", is_active=True,
                scope_json=json.dumps({"company_id": "company-1", "industry_code": "BANK"}, sort_keys=True, separators=(",", ":")),
            ))
            session.flush()
            calendar = session.get(CanonicalCompanyFiscalCalendar, 1)
            calendar.fiscal_year_start_month = 7
            calendar.approval_ref = "approval-fiscal-start-7"
        plan = _plan()
        non_calendar = replace(plan.facts[0],
                               period_identity=("DURATION", (1404, 7, 1), (1404, 9, 30)))
>       result = write_canonical_plan(replace(plan, facts=(non_calendar,)), _metadata(), factory)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

src\tests\test_canonical_writer.py:469:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\ingestion\canonical_writer.py:82: in write_canonical_plan
    result = _write_in_transaction(session, plan, metadata, effective_ingestion_id)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\ingestion\canonical_writer.py:98: in _write_in_transaction
    company_id, industry_code, template_approval_ref = resolve_plan_approvals(session, plan, metadata)
                                                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\ingestion\canonical_writer.py:272: in resolve_plan_approvals
    _validate_fact(session, fact, company_id, plan, industry.industry_code) for fact in plan.facts
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\ingestion\canonical_writer.py:451: in _validate_fact
    scope=_approval_scope(fact, resolved_kind, industry_code, identity=identity))
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

fact = PlannedFact(company_id='company-1', report_type_id='PERIODIC_FINANCIAL', report_id='report-1', report_version_id='vers...ksheet_ordinal=1, worksheet_name='Annual', source_coordinate='B2', source_value_kind='PRESENT_TEXT', source_token=None)
kind = 'industry', industry_code = 'BANK', identity = 'BANK'

    def _approval_scope(fact: PlannedFact, kind: str, industry_code: str,
                        *, identity: str | None = None) -> dict[str, str]:
        scopes: dict[str, dict[str, str]] = {
            "company": {"industry_code": industry_code},
            "report_type": {"company_id": fact.company_id},
            "report_version": {"company_id": fact.company_id, "report_type_id": fact.report_type_id},
            "metric": {"industry_code": industry_code},
            "source_unit": {"metric_id": fact.metric_id},
            "source_currency": {"metric_id": fact.metric_id},
            "source_scale": {"metric_id": fact.metric_id},
            "period_mapping": {"report_type_id": fact.report_type_id,
                               "temporal_type": fact.period_identity[0],
                               "duration_basis": fact.duration_basis or "INSTANT"},
            "source_label": {"report_type_id": fact.report_type_id,
                             "template_id": fact.template_id, "template_version": fact.template_version,
                             "template_sha256": fact.template_sha256.lower()},
            "source_header": {"report_type_id": fact.report_type_id,
                              "template_id": fact.template_id, "template_version": fact.template_version,
                              "template_sha256": fact.template_sha256.lower()},
            "dimension": {"company_id": fact.company_id, "report_type_id": fact.report_type_id},
            "other_metric_rule": {"report_type_id": fact.report_type_id, "metric_id": fact.metric_id},
            "zero_fallback_rule": {"report_type_id": fact.report_type_id, "metric_id": fact.metric_id},
        }
        if kind == "dimension_value":
            dimensions = [dimension for dimension, value in fact.dimensions
                          if value == identity]
            if len(dimensions) != 1:
                raise CanonicalWriteError("APPROVAL_SCOPE_AMBIGUOUS")
            scopes[kind] = {"company_id": fact.company_id, "report_type_id": fact.report_type_id,
                            "dimension_id": dimensions[0]}
        if kind not in scopes:
>           raise CanonicalWriteError("APPROVAL_SCOPE_KIND_UNSUPPORTED")
E           src.ingestion.canonical_writer.CanonicalWriteError: APPROVAL_SCOPE_KIND_UNSUPPORTED

src\ingestion\canonical_writer.py:496: CanonicalWriteError
_________________________ test_writer_persists_only_approved_blank_zero_fallback_as_fallback __________________________

db = (Engine(sqlite:///D:\winprojects\analyzer\.pytest_db_consolidation_002_20261121\test_writer_persists_only_appr0\canoni..._consolidation_002_20261121\test_writer_persists_only_appr0\canonical.sqlite), autoflush=True, expire_on_commit=False))

    def test_writer_persists_only_approved_blank_zero_fallback_as_fallback(db):
        _engine, factory = db
        with factory.begin() as session:
            session.add(CanonicalApproval(approval_kind="zero_fallback_rule",
                                          external_identity="rule-zero", approval_ref="approval-zero",
                                          is_active=True,
                                          scope_json=json.dumps({"report_type_id": "PERIODIC_FINANCIAL", "metric_id": "metric-sales"}, sort_keys=True, separators=(",", ":"))))
        plan = _plan()
        fact = replace(
            plan.facts[0], source_value_decimal=Decimal(0), value_integer=0,
            value_origin=ValueOrigin.ZERO_FALLBACK, source_value_kind="BLANK",
            approval_references=plan.facts[0].approval_references
            + (("zero_fallback_rule", "rule-zero", "approval-zero"),),
        )
>       result = write_canonical_plan(replace(plan, facts=(fact,)), _metadata(), factory)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

src\tests\test_canonical_writer.py:490:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\ingestion\canonical_writer.py:82: in write_canonical_plan
    result = _write_in_transaction(session, plan, metadata, effective_ingestion_id)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\ingestion\canonical_writer.py:98: in _write_in_transaction
    company_id, industry_code, template_approval_ref = resolve_plan_approvals(session, plan, metadata)
                                                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\ingestion\canonical_writer.py:272: in resolve_plan_approvals
    _validate_fact(session, fact, company_id, plan, industry.industry_code) for fact in plan.facts
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\ingestion\canonical_writer.py:451: in _validate_fact
    scope=_approval_scope(fact, resolved_kind, industry_code, identity=identity))
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

fact = PlannedFact(company_id='company-1', report_type_id='PERIODIC_FINANCIAL', report_id='report-1', report_version_id='vers...)), worksheet_ordinal=1, worksheet_name='Annual', source_coordinate='B2', source_value_kind='BLANK', source_token=None)
kind = 'industry', industry_code = 'BANK', identity = 'BANK'

    def _approval_scope(fact: PlannedFact, kind: str, industry_code: str,
                        *, identity: str | None = None) -> dict[str, str]:
        scopes: dict[str, dict[str, str]] = {
            "company": {"industry_code": industry_code},
            "report_type": {"company_id": fact.company_id},
            "report_version": {"company_id": fact.company_id, "report_type_id": fact.report_type_id},
            "metric": {"industry_code": industry_code},
            "source_unit": {"metric_id": fact.metric_id},
            "source_currency": {"metric_id": fact.metric_id},
            "source_scale": {"metric_id": fact.metric_id},
            "period_mapping": {"report_type_id": fact.report_type_id,
                               "temporal_type": fact.period_identity[0],
                               "duration_basis": fact.duration_basis or "INSTANT"},
            "source_label": {"report_type_id": fact.report_type_id,
                             "template_id": fact.template_id, "template_version": fact.template_version,
                             "template_sha256": fact.template_sha256.lower()},
            "source_header": {"report_type_id": fact.report_type_id,
                              "template_id": fact.template_id, "template_version": fact.template_version,
                              "template_sha256": fact.template_sha256.lower()},
            "dimension": {"company_id": fact.company_id, "report_type_id": fact.report_type_id},
            "other_metric_rule": {"report_type_id": fact.report_type_id, "metric_id": fact.metric_id},
            "zero_fallback_rule": {"report_type_id": fact.report_type_id, "metric_id": fact.metric_id},
        }
        if kind == "dimension_value":
            dimensions = [dimension for dimension, value in fact.dimensions
                          if value == identity]
            if len(dimensions) != 1:
                raise CanonicalWriteError("APPROVAL_SCOPE_AMBIGUOUS")
            scopes[kind] = {"company_id": fact.company_id, "report_type_id": fact.report_type_id,
                            "dimension_id": dimensions[0]}
        if kind not in scopes:
>           raise CanonicalWriteError("APPROVAL_SCOPE_KIND_UNSUPPORTED")
E           src.ingestion.canonical_writer.CanonicalWriteError: APPROVAL_SCOPE_KIND_UNSUPPORTED

src\ingestion\canonical_writer.py:496: CanonicalWriteError
______________________ test_identical_version_replay_is_duplicate_and_changed_payload_conflicts _______________________

db = (Engine(sqlite:///D:\winprojects\analyzer\.pytest_db_consolidation_002_20261121\test_identical_version_replay_0\canoni..._consolidation_002_20261121\test_identical_version_replay_0\canonical.sqlite), autoflush=True, expire_on_commit=False))

    def test_identical_version_replay_is_duplicate_and_changed_payload_conflicts(db):
        _engine, factory = db
>       first = write_canonical_plan(_plan(), _metadata(), factory)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

src\tests\test_canonical_writer.py:501:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\ingestion\canonical_writer.py:82: in write_canonical_plan
    result = _write_in_transaction(session, plan, metadata, effective_ingestion_id)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\ingestion\canonical_writer.py:98: in _write_in_transaction
    company_id, industry_code, template_approval_ref = resolve_plan_approvals(session, plan, metadata)
                                                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\ingestion\canonical_writer.py:272: in resolve_plan_approvals
    _validate_fact(session, fact, company_id, plan, industry.industry_code) for fact in plan.facts
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\ingestion\canonical_writer.py:451: in _validate_fact
    scope=_approval_scope(fact, resolved_kind, industry_code, identity=identity))
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

fact = PlannedFact(company_id='company-1', report_type_id='PERIODIC_FINANCIAL', report_id='report-1', report_version_id='vers...ksheet_ordinal=1, worksheet_name='Annual', source_coordinate='B2', source_value_kind='PRESENT_TEXT', source_token=None)
kind = 'industry', industry_code = 'BANK', identity = 'BANK'

    def _approval_scope(fact: PlannedFact, kind: str, industry_code: str,
                        *, identity: str | None = None) -> dict[str, str]:
        scopes: dict[str, dict[str, str]] = {
            "company": {"industry_code": industry_code},
            "report_type": {"company_id": fact.company_id},
            "report_version": {"company_id": fact.company_id, "report_type_id": fact.report_type_id},
            "metric": {"industry_code": industry_code},
            "source_unit": {"metric_id": fact.metric_id},
            "source_currency": {"metric_id": fact.metric_id},
            "source_scale": {"metric_id": fact.metric_id},
            "period_mapping": {"report_type_id": fact.report_type_id,
                               "temporal_type": fact.period_identity[0],
                               "duration_basis": fact.duration_basis or "INSTANT"},
            "source_label": {"report_type_id": fact.report_type_id,
                             "template_id": fact.template_id, "template_version": fact.template_version,
                             "template_sha256": fact.template_sha256.lower()},
            "source_header": {"report_type_id": fact.report_type_id,
                              "template_id": fact.template_id, "template_version": fact.template_version,
                              "template_sha256": fact.template_sha256.lower()},
            "dimension": {"company_id": fact.company_id, "report_type_id": fact.report_type_id},
            "other_metric_rule": {"report_type_id": fact.report_type_id, "metric_id": fact.metric_id},
            "zero_fallback_rule": {"report_type_id": fact.report_type_id, "metric_id": fact.metric_id},
        }
        if kind == "dimension_value":
            dimensions = [dimension for dimension, value in fact.dimensions
                          if value == identity]
            if len(dimensions) != 1:
                raise CanonicalWriteError("APPROVAL_SCOPE_AMBIGUOUS")
            scopes[kind] = {"company_id": fact.company_id, "report_type_id": fact.report_type_id,
                            "dimension_id": dimensions[0]}
        if kind not in scopes:
>           raise CanonicalWriteError("APPROVAL_SCOPE_KIND_UNSUPPORTED")
E           src.ingestion.canonical_writer.CanonicalWriteError: APPROVAL_SCOPE_KIND_UNSUPPORTED

src\ingestion\canonical_writer.py:496: CanonicalWriteError
_______________________ test_correction_appends_a_report_version_and_pit_uses_publication_time ________________________

db = (Engine(sqlite:///D:\winprojects\analyzer\.pytest_db_consolidation_002_20261121\test_correction_appends_a_repo0\canoni..._consolidation_002_20261121\test_correction_appends_a_repo0\canonical.sqlite), autoflush=True, expire_on_commit=False))

    def test_correction_appends_a_report_version_and_pit_uses_publication_time(db):
        _engine, factory = db
>       write_canonical_plan(_plan(), _metadata(), factory)

src\tests\test_canonical_writer.py:516:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\ingestion\canonical_writer.py:82: in write_canonical_plan
    result = _write_in_transaction(session, plan, metadata, effective_ingestion_id)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\ingestion\canonical_writer.py:98: in _write_in_transaction
    company_id, industry_code, template_approval_ref = resolve_plan_approvals(session, plan, metadata)
                                                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\ingestion\canonical_writer.py:272: in resolve_plan_approvals
    _validate_fact(session, fact, company_id, plan, industry.industry_code) for fact in plan.facts
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\ingestion\canonical_writer.py:451: in _validate_fact
    scope=_approval_scope(fact, resolved_kind, industry_code, identity=identity))
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

fact = PlannedFact(company_id='company-1', report_type_id='PERIODIC_FINANCIAL', report_id='report-1', report_version_id='vers...ksheet_ordinal=1, worksheet_name='Annual', source_coordinate='B2', source_value_kind='PRESENT_TEXT', source_token=None)
kind = 'industry', industry_code = 'BANK', identity = 'BANK'

    def _approval_scope(fact: PlannedFact, kind: str, industry_code: str,
                        *, identity: str | None = None) -> dict[str, str]:
        scopes: dict[str, dict[str, str]] = {
            "company": {"industry_code": industry_code},
            "report_type": {"company_id": fact.company_id},
            "report_version": {"company_id": fact.company_id, "report_type_id": fact.report_type_id},
            "metric": {"industry_code": industry_code},
            "source_unit": {"metric_id": fact.metric_id},
            "source_currency": {"metric_id": fact.metric_id},
            "source_scale": {"metric_id": fact.metric_id},
            "period_mapping": {"report_type_id": fact.report_type_id,
                               "temporal_type": fact.period_identity[0],
                               "duration_basis": fact.duration_basis or "INSTANT"},
            "source_label": {"report_type_id": fact.report_type_id,
                             "template_id": fact.template_id, "template_version": fact.template_version,
                             "template_sha256": fact.template_sha256.lower()},
            "source_header": {"report_type_id": fact.report_type_id,
                              "template_id": fact.template_id, "template_version": fact.template_version,
                              "template_sha256": fact.template_sha256.lower()},
            "dimension": {"company_id": fact.company_id, "report_type_id": fact.report_type_id},
            "other_metric_rule": {"report_type_id": fact.report_type_id, "metric_id": fact.metric_id},
            "zero_fallback_rule": {"report_type_id": fact.report_type_id, "metric_id": fact.metric_id},
        }
        if kind == "dimension_value":
            dimensions = [dimension for dimension, value in fact.dimensions
                          if value == identity]
            if len(dimensions) != 1:
                raise CanonicalWriteError("APPROVAL_SCOPE_AMBIGUOUS")
            scopes[kind] = {"company_id": fact.company_id, "report_type_id": fact.report_type_id,
                            "dimension_id": dimensions[0]}
        if kind not in scopes:
>           raise CanonicalWriteError("APPROVAL_SCOPE_KIND_UNSUPPORTED")
E           src.ingestion.canonical_writer.CanonicalWriteError: APPROVAL_SCOPE_KIND_UNSUPPORTED

src\ingestion\canonical_writer.py:496: CanonicalWriteError
___________________ test_pit_quality_order_prefers_audited_initial_over_later_unaudited_restatement ___________________

db = (Engine(sqlite:///D:\winprojects\analyzer\.pytest_db_consolidation_002_20261121\test_pit_quality_order_prefers0\canoni..._consolidation_002_20261121\test_pit_quality_order_prefers0\canonical.sqlite), autoflush=True, expire_on_commit=False))

    def test_pit_quality_order_prefers_audited_initial_over_later_unaudited_restatement(db):
        _engine, factory = db
>       write_canonical_plan(_plan(), _metadata(), factory)

src\tests\test_canonical_writer.py:532:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\ingestion\canonical_writer.py:82: in write_canonical_plan
    result = _write_in_transaction(session, plan, metadata, effective_ingestion_id)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\ingestion\canonical_writer.py:98: in _write_in_transaction
    company_id, industry_code, template_approval_ref = resolve_plan_approvals(session, plan, metadata)
                                                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\ingestion\canonical_writer.py:272: in resolve_plan_approvals
    _validate_fact(session, fact, company_id, plan, industry.industry_code) for fact in plan.facts
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\ingestion\canonical_writer.py:451: in _validate_fact
    scope=_approval_scope(fact, resolved_kind, industry_code, identity=identity))
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

fact = PlannedFact(company_id='company-1', report_type_id='PERIODIC_FINANCIAL', report_id='report-1', report_version_id='vers...ksheet_ordinal=1, worksheet_name='Annual', source_coordinate='B2', source_value_kind='PRESENT_TEXT', source_token=None)
kind = 'industry', industry_code = 'BANK', identity = 'BANK'

    def _approval_scope(fact: PlannedFact, kind: str, industry_code: str,
                        *, identity: str | None = None) -> dict[str, str]:
        scopes: dict[str, dict[str, str]] = {
            "company": {"industry_code": industry_code},
            "report_type": {"company_id": fact.company_id},
            "report_version": {"company_id": fact.company_id, "report_type_id": fact.report_type_id},
            "metric": {"industry_code": industry_code},
            "source_unit": {"metric_id": fact.metric_id},
            "source_currency": {"metric_id": fact.metric_id},
            "source_scale": {"metric_id": fact.metric_id},
            "period_mapping": {"report_type_id": fact.report_type_id,
                               "temporal_type": fact.period_identity[0],
                               "duration_basis": fact.duration_basis or "INSTANT"},
            "source_label": {"report_type_id": fact.report_type_id,
                             "template_id": fact.template_id, "template_version": fact.template_version,
                             "template_sha256": fact.template_sha256.lower()},
            "source_header": {"report_type_id": fact.report_type_id,
                              "template_id": fact.template_id, "template_version": fact.template_version,
                              "template_sha256": fact.template_sha256.lower()},
            "dimension": {"company_id": fact.company_id, "report_type_id": fact.report_type_id},
            "other_metric_rule": {"report_type_id": fact.report_type_id, "metric_id": fact.metric_id},
            "zero_fallback_rule": {"report_type_id": fact.report_type_id, "metric_id": fact.metric_id},
        }
        if kind == "dimension_value":
            dimensions = [dimension for dimension, value in fact.dimensions
                          if value == identity]
            if len(dimensions) != 1:
                raise CanonicalWriteError("APPROVAL_SCOPE_AMBIGUOUS")
            scopes[kind] = {"company_id": fact.company_id, "report_type_id": fact.report_type_id,
                            "dimension_id": dimensions[0]}
        if kind not in scopes:
>           raise CanonicalWriteError("APPROVAL_SCOPE_KIND_UNSUPPORTED")
E           src.ingestion.canonical_writer.CanonicalWriteError: APPROVAL_SCOPE_KIND_UNSUPPORTED

src\ingestion\canonical_writer.py:496: CanonicalWriteError
______________________________ test_invalid_fact_rolls_back_entire_report_version_batch _______________________________

db = (Engine(sqlite:///D:\winprojects\analyzer\.pytest_db_consolidation_002_20261121\test_invalid_fact_rolls_back_e0\canoni..._consolidation_002_20261121\test_invalid_fact_rolls_back_e0\canonical.sqlite), autoflush=True, expire_on_commit=False))

    def test_invalid_fact_rolls_back_entire_report_version_batch(db):
        _engine, factory = db
        plan = _plan()
        invalid = replace(plan.facts[0], metric_id="unbound-metric")
>       with pytest.raises(CanonicalWriteError, match="IDENTITY_BINDING_NOT_RESOLVED") as error:
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E       AssertionError: Regex pattern did not match.
E         Expected regex: 'IDENTITY_BINDING_NOT_RESOLVED'
E         Actual message: 'APPROVAL_SCOPE_KIND_UNSUPPORTED'

src\tests\test_canonical_writer.py:553: AssertionError
________________ test_database_fact_identity_and_value_state_constraints_reject_null_dimension_bypass _________________

db = (Engine(sqlite:///D:\winprojects\analyzer\.pytest_db_consolidation_002_20261121\test_database_fact_identity_an0\canoni..._consolidation_002_20261121\test_database_fact_identity_an0\canonical.sqlite), autoflush=True, expire_on_commit=False))

    def test_database_fact_identity_and_value_state_constraints_reject_null_dimension_bypass(db):
        engine, _factory = db
        assert "uq_canonical_fact_identity" in {constraint.get("name") for constraint in inspect(engine).get_unique_constraints("canonical_financial_facts")}
        with engine.connect() as connection:
            columns = {item["name"] for item in inspect(connection).get_columns("canonical_financial_facts")}
            assert "dimension_set_id" in columns and "value_state" in columns
>       _result = write_canonical_plan(_plan(), _metadata(), _factory)
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

src\tests\test_canonical_writer.py:571:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\ingestion\canonical_writer.py:82: in write_canonical_plan
    result = _write_in_transaction(session, plan, metadata, effective_ingestion_id)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\ingestion\canonical_writer.py:98: in _write_in_transaction
    company_id, industry_code, template_approval_ref = resolve_plan_approvals(session, plan, metadata)
                                                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\ingestion\canonical_writer.py:272: in resolve_plan_approvals
    _validate_fact(session, fact, company_id, plan, industry.industry_code) for fact in plan.facts
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\ingestion\canonical_writer.py:451: in _validate_fact
    scope=_approval_scope(fact, resolved_kind, industry_code, identity=identity))
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

fact = PlannedFact(company_id='company-1', report_type_id='PERIODIC_FINANCIAL', report_id='report-1', report_version_id='vers...ksheet_ordinal=1, worksheet_name='Annual', source_coordinate='B2', source_value_kind='PRESENT_TEXT', source_token=None)
kind = 'industry', industry_code = 'BANK', identity = 'BANK'

    def _approval_scope(fact: PlannedFact, kind: str, industry_code: str,
                        *, identity: str | None = None) -> dict[str, str]:
        scopes: dict[str, dict[str, str]] = {
            "company": {"industry_code": industry_code},
            "report_type": {"company_id": fact.company_id},
            "report_version": {"company_id": fact.company_id, "report_type_id": fact.report_type_id},
            "metric": {"industry_code": industry_code},
            "source_unit": {"metric_id": fact.metric_id},
            "source_currency": {"metric_id": fact.metric_id},
            "source_scale": {"metric_id": fact.metric_id},
            "period_mapping": {"report_type_id": fact.report_type_id,
                               "temporal_type": fact.period_identity[0],
                               "duration_basis": fact.duration_basis or "INSTANT"},
            "source_label": {"report_type_id": fact.report_type_id,
                             "template_id": fact.template_id, "template_version": fact.template_version,
                             "template_sha256": fact.template_sha256.lower()},
            "source_header": {"report_type_id": fact.report_type_id,
                              "template_id": fact.template_id, "template_version": fact.template_version,
                              "template_sha256": fact.template_sha256.lower()},
            "dimension": {"company_id": fact.company_id, "report_type_id": fact.report_type_id},
            "other_metric_rule": {"report_type_id": fact.report_type_id, "metric_id": fact.metric_id},
            "zero_fallback_rule": {"report_type_id": fact.report_type_id, "metric_id": fact.metric_id},
        }
        if kind == "dimension_value":
            dimensions = [dimension for dimension, value in fact.dimensions
                          if value == identity]
            if len(dimensions) != 1:
                raise CanonicalWriteError("APPROVAL_SCOPE_AMBIGUOUS")
            scopes[kind] = {"company_id": fact.company_id, "report_type_id": fact.report_type_id,
                            "dimension_id": dimensions[0]}
        if kind not in scopes:
>           raise CanonicalWriteError("APPROVAL_SCOPE_KIND_UNSUPPORTED")
E           src.ingestion.canonical_writer.CanonicalWriteError: APPROVAL_SCOPE_KIND_UNSUPPORTED

src\ingestion\canonical_writer.py:496: CanonicalWriteError
_______________________________ test_market_ticker_codal_symbol_conflict_rejects_batch ________________________________

db = (Engine(sqlite:///D:\winprojects\analyzer\.pytest_db_consolidation_002_20261121\test_market_ticker_codal_symbo0\atomic...db_consolidation_002_20261121\test_market_ticker_codal_symbo0\atomic-test.db), autoflush=True, expire_on_commit=False))
tmp_path = WindowsPath('D:/winprojects/analyzer/.pytest_db_consolidation_002_20261121/test_market_ticker_codal_symbo0')

    def test_market_ticker_codal_symbol_conflict_rejects_batch(db, tmp_path):
        _, factory = db
        with factory() as session:
            original = session.query(Company).filter_by(ticker="SAMAN").one()
            session.add(Company(ticker="OTHER", company_name="Other", industry_id=original.industry_id,
                                codal_symbol="SAMAN-ALT", status="ACTIVE", is_active=True))
            session.commit()
            result = ingest_ohlc_csv(session, market_csv(tmp_path, [market_row(1)]))
>           assert result.status == "FAILED"
E           AssertionError: assert 'COMPLETED' == 'FAILED'
E
E             - FAILED
E             + COMPLETED

src\tests\test_market_fx_atomic_ingestion.py:80: AssertionError
=============================================== short test summary info ===============================================
FAILED src/tests/test_excel_canonical_input.py::test_rejects_missing_source_coordinate_and_invalid_numeric_text - Failed: DID NOT RAISE CandidateValidationError
FAILED src/tests/test_canonical_writer.py::test_synthetic_xlsx_runs_reader_match_admission_writer_and_readback - src.ingestion.canonical_writer.CanonicalWriteError: APPROVAL_SCOPE_MISMATCH
FAILED src/tests/test_canonical_writer.py::test_migration_ten_duplicate_preflight_rolls_back_and_preserves_rows[market_daily-uq_market_daily_jalali_identity-INSERT INTO market_daily (company_id,jalali_year,jalali_month,jalali_day) VALUES (1,1404,1,1),(1,1404,1,1)] - sqlalchemy.exc.IntegrityError: (sqlite3.IntegrityError) NOT NULL constraint failed: companies.status
FAILED src/tests/test_canonical_writer.py::test_writer_persists_jalali_ytd_integer_fact_and_exact_provenance - src.ingestion.canonical_writer.CanonicalWriteError: APPROVAL_SCOPE_KIND_UNSUPPORTED
FAILED src/tests/test_canonical_writer.py::test_monthly_activity_ytd_is_not_subject_to_periodic_quarter_alignment - src.ingestion.canonical_writer.CanonicalWriteError: APPROVAL_SCOPE_KIND_UNSUPPORTED
FAILED src/tests/test_canonical_writer.py::test_periodic_financial_ytd_still_requires_three_six_nine_or_twelve_months - AssertionError: Regex pattern did not match.
FAILED src/tests/test_canonical_writer.py::test_writer_accepts_explicit_non_calendar_fiscal_start_and_ytd_period - src.ingestion.canonical_writer.CanonicalWriteError: APPROVAL_SCOPE_KIND_UNSUPPORTED
FAILED src/tests/test_canonical_writer.py::test_writer_persists_only_approved_blank_zero_fallback_as_fallback - src.ingestion.canonical_writer.CanonicalWriteError: APPROVAL_SCOPE_KIND_UNSUPPORTED
FAILED src/tests/test_canonical_writer.py::test_identical_version_replay_is_duplicate_and_changed_payload_conflicts - src.ingestion.canonical_writer.CanonicalWriteError: APPROVAL_SCOPE_KIND_UNSUPPORTED
FAILED src/tests/test_canonical_writer.py::test_correction_appends_a_report_version_and_pit_uses_publication_time - src.ingestion.canonical_writer.CanonicalWriteError: APPROVAL_SCOPE_KIND_UNSUPPORTED
FAILED src/tests/test_canonical_writer.py::test_pit_quality_order_prefers_audited_initial_over_later_unaudited_restatement - src.ingestion.canonical_writer.CanonicalWriteError: APPROVAL_SCOPE_KIND_UNSUPPORTED
FAILED src/tests/test_canonical_writer.py::test_invalid_fact_rolls_back_entire_report_version_batch - AssertionError: Regex pattern did not match.
FAILED src/tests/test_canonical_writer.py::test_database_fact_identity_and_value_state_constraints_reject_null_dimension_bypass - src.ingestion.canonical_writer.CanonicalWriteError: APPROVAL_SCOPE_KIND_UNSUPPORTED
FAILED src/tests/test_market_fx_atomic_ingestion.py::test_market_ticker_codal_symbol_conflict_rejects_batch - AssertionError: assert 'COMPLETED' == 'FAILED'
14 failed, 140 passed in 645.51s (0:10:45)