(analyzer) PS D:\Winprojects\analyzer> .\.venv\Scripts\python.exe -m pytest -q --basetemp .pytest_db_impl_001_20261121 src/tests/test_canonical_writer.py src/tests/test_task017_model_constraints.py src/tests/test_stage1_database_integrity.py src/tests/test_canonical_ingestion_admission.py src/tests/test_excel_adapter.py src/tests/test_excel_canonical_input.py src/tests/test_excel_template_matching.py
...F....F........F...........................................F................................                   [100%]
====================================================== FAILURES =======================================================
_____________________ test_failed_migration_nine_keeps_duplicate_legacy_rows_and_is_not_recorded ______________________

self = <sqlalchemy.engine.base.Connection object at 0x000001F4353FB110>
dialect = <sqlalchemy.dialects.sqlite.pysqlite.SQLiteDialect_pysqlite object at 0x000001F435670200>
context = <sqlalchemy.dialects.sqlite.base.SQLiteExecutionContext object at 0x000001F4355AEF00>
statement = <sqlalchemy.dialects.sqlite.base.SQLiteCompiler object at 0x000001F4355AD0D0>, parameters = [()]

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

self = <sqlalchemy.dialects.sqlite.pysqlite.SQLiteDialect_pysqlite object at 0x000001F435670200>
cursor = <sqlite3.Cursor object at 0x000001F4356120C0>
statement = "INSERT INTO companies (ticker, company_name, industry_id, codal_symbol) VALUES ('DUP','One',1,'A'),('DUP','Two',1,'B')"
parameters = (), context = <sqlalchemy.dialects.sqlite.base.SQLiteExecutionContext object at 0x000001F4355AEF00>

    def do_execute(self, cursor, statement, parameters, context=None):
>       cursor.execute(statement, parameters)
E       sqlite3.IntegrityError: NOT NULL constraint failed: companies.status

.venv\Lib\site-packages\sqlalchemy\engine\default.py:952: IntegrityError

The above exception was the direct cause of the following exception:

monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x000001F4327C2A20>
tmp_path = WindowsPath('D:/winprojects/analyzer/.pytest_db_impl_001_20261121/test_failed_migration_nine_kee0')

    def test_failed_migration_nine_keeps_duplicate_legacy_rows_and_is_not_recorded(monkeypatch, tmp_path):
        engine = create_engine(f"sqlite:///{tmp_path / 'duplicate-symbols.sqlite'}")
        all_migrations = tuple(migration_runner._migration_list())
        monkeypatch.setattr(migration_runner, "_migration_list", lambda: all_migrations[:8])
        assert MigrationRunner(engine).upgrade() == 8
        with engine.begin() as connection:
            connection.execute(text("INSERT INTO industries (industry_code, industry_name) VALUES ('BANK','Bank')"))
>           connection.execute(text("INSERT INTO companies (ticker, company_name, industry_id, codal_symbol) VALUES ('DUP','One',1,'A'),('DUP','Two',1,'B')"))

src\tests\test_canonical_writer.py:261:
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

self = <sqlalchemy.dialects.sqlite.pysqlite.SQLiteDialect_pysqlite object at 0x000001F435670200>
cursor = <sqlite3.Cursor object at 0x000001F4356120C0>
statement = "INSERT INTO companies (ticker, company_name, industry_id, codal_symbol) VALUES ('DUP','One',1,'A'),('DUP','Two',1,'B')"
parameters = (), context = <sqlalchemy.dialects.sqlite.base.SQLiteExecutionContext object at 0x000001F4355AEF00>

    def do_execute(self, cursor, statement, parameters, context=None):
>       cursor.execute(statement, parameters)
E       sqlalchemy.exc.IntegrityError: (sqlite3.IntegrityError) NOT NULL constraint failed: companies.status
E       [SQL: INSERT INTO companies (ticker, company_name, industry_id, codal_symbol) VALUES ('DUP','One',1,'A'),('DUP','Two',1,'B')]
E       (Background on this error at: https://sqlalche.me/e/20/gkpj)

.venv\Lib\site-packages\sqlalchemy\engine\default.py:952: IntegrityError
_______________________ test_monthly_activity_ytd_is_not_subject_to_periodic_quarter_alignment ________________________

db = (Engine(sqlite:///D:\winprojects\analyzer\.pytest_db_impl_001_20261121\test_monthly_activity_ytd_is_n0\canonical.sqlit...pytest_db_impl_001_20261121\test_monthly_activity_ytd_is_n0\canonical.sqlite), autoflush=True, expire_on_commit=False))

    def test_monthly_activity_ytd_is_not_subject_to_periodic_quarter_alignment(db):
        _engine, factory = db
        with factory.begin() as session:
            session.add(CanonicalApproval(
                approval_kind="report_type", external_identity="MONTHLY_ACTIVITY",
                approval_ref="approval-monthly-activity", is_active=True,
            ))
        plan = _plan(
            report_type_id="MONTHLY_ACTIVITY",
            period_identity=("DURATION", (1404, 1, 1), (1404, 2, 31)),
        )
>       result = write_canonical_plan(plan, _metadata(), factory)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

src\tests\test_canonical_writer.py:337:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\ingestion\canonical_writer.py:81: in write_canonical_plan
    result = _write_in_transaction(session, plan, metadata, effective_ingestion_id)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\ingestion\canonical_writer.py:123: in _write_in_transaction
    _validate_fact(session, fact, company_id, plan) for fact in plan.facts
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\ingestion\canonical_writer.py:412: in _validate_fact
    _check_approval(session, _APPROVAL_KIND_ALIASES.get(approval_kind, approval_kind), identity, ref)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

session = <sqlalchemy.orm.session.Session object at 0x000001F435797D70>, kind = 'report_type'
identity = 'MONTHLY_ACTIVITY', ref = 'approval-report-type'

    def _check_approval(session: Session, kind: str, identity: str, ref: str | None) -> None:
        query = select(CanonicalApproval).where(
            CanonicalApproval.approval_kind == kind,
            CanonicalApproval.external_identity == identity,
            CanonicalApproval.is_active.is_(True),
        )
        if ref is not None:
            query = query.where(CanonicalApproval.approval_ref == ref)
        if session.scalar(query.limit(1)) is None:
>           raise CanonicalWriteError("APPROVAL_NOT_RESOLVED")
E           src.ingestion.canonical_writer.CanonicalWriteError: APPROVAL_NOT_RESOLVED

src\ingestion\canonical_writer.py:435: CanonicalWriteError
__________________________ test_company_required_fields_industry_fk_and_supported_uniqueness __________________________

db = Engine(sqlite:///D:\winprojects\analyzer\.pytest_db_impl_001_20261121\test_company_required_fields_i0\constraints.sqlite)

    def test_company_required_fields_industry_fk_and_supported_uniqueness(db):
        with Session(db) as s:
            industry, company, *_ = _base_rows(s)
            s.commit()
            s.add(Company(ticker="BAD", company_name="Bad FK", industry_id=999))
            with pytest.raises(IntegrityError):
                s.flush()
            s.rollback()
            _rejected(s, Company(company_name="Missing ticker", industry_id=industry.industry_id))
            _rejected(s, Company(ticker="NO-NAME", industry_id=industry.industry_id))
            _rejected(s, Industry(industry_code="NO-NAME"))
            _rejected(s, Industry(industry_code="BANK", industry_name="Duplicate"))
            s.add_all([Company(ticker="A", company_name="A", industry_id=industry.industry_id),
                       Company(ticker="B", company_name="B", industry_id=industry.industry_id)])
            s.flush()  # Multiple NULL national IDs are allowed by SQLite UNIQUE semantics.
>           _rejected(s, Company(ticker="A", company_name="Duplicate ticker", industry_id=industry.industry_id))

src\tests\test_task017_model_constraints.py:97:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

session = <sqlalchemy.orm.session.Session object at 0x000001F435918CE0>
row = <src.models.entity.Company object at 0x000001F435796930>

    def _rejected(session, row):
        session.add(row)
>       with pytest.raises(IntegrityError):
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E       Failed: DID NOT RAISE IntegrityError

src\tests\test_task017_model_constraints.py:77: Failed
____________________ test_duplicate_and_conflicting_facts_keep_all_or_nothing_admission_semantics _____________________

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
>       assert same.accepted
E       assert False
E        +  where False = ExcelAdapterResult(observation=WorkbookObservation(source=SourceArtifactObservation(source_ref=None, file_name=None, f...ksheet_ordinal=None, identity=("'version-1'", "('DURATION', (1404, 1, 1), (1404, 12, 29))", "'metric-sales'", '()')),)).accepted

src\tests\test_excel_adapter.py:254: AssertionError
=============================================== short test summary info ===============================================
FAILED src/tests/test_canonical_writer.py::test_failed_migration_nine_keeps_duplicate_legacy_rows_and_is_not_recorded - sqlalchemy.exc.IntegrityError: (sqlite3.IntegrityError) NOT NULL constraint failed: companies.status
FAILED src/tests/test_canonical_writer.py::test_monthly_activity_ytd_is_not_subject_to_periodic_quarter_alignment - src.ingestion.canonical_writer.CanonicalWriteError: APPROVAL_NOT_RESOLVED
FAILED src/tests/test_task017_model_constraints.py::test_company_required_fields_industry_fk_and_supported_uniqueness - Failed: DID NOT RAISE IntegrityError
FAILED src/tests/test_excel_adapter.py::test_duplicate_and_conflicting_facts_keep_all_or_nothing_admission_semantics - assert False
4 failed, 90 passed in 406.69s (0:06:46)