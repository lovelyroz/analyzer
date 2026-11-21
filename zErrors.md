(analyzer) PS D:\Winprojects\analyzer> .\.venv\Scripts\python.exe -m pytest -q --basetemp .pytest_db_impl_001_20261121 src/tests/test_canonical_writer.py src/tests/test_task017_model_constraints.py src/tests/test_stage1_database_integrity.py src/tests/test_canonical_ingestion_admission.py src/tests/test_excel_adapter.py src/tests/test_excel_canonical_input.py src/tests/test_excel_template_matching.py
...F..........................................................................................                   [100%]
====================================================== FAILURES =======================================================
_____________________ test_failed_migration_nine_keeps_duplicate_legacy_rows_and_is_not_recorded ______________________

self = <sqlalchemy.engine.base.Connection object at 0x000002D7C1015EE0>
dialect = <sqlalchemy.dialects.sqlite.pysqlite.SQLiteDialect_pysqlite object at 0x000002D7C123AC60>
context = <sqlalchemy.dialects.sqlite.base.SQLiteExecutionContext object at 0x000002D7C124BE30>
statement = <sqlalchemy.dialects.sqlite.base.SQLiteCompiler object at 0x000002D7C124BCB0>, parameters = [()]

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

self = <sqlalchemy.dialects.sqlite.pysqlite.SQLiteDialect_pysqlite object at 0x000002D7C123AC60>
cursor = <sqlite3.Cursor object at 0x000002D7C123E5C0>
statement = "INSERT INTO companies (ticker, company_name, industry_id, codal_symbol, status) VALUES ('DUP','One',1,'A','ACTIVE'),('DUP','Two',1,'B','ACTIVE')"
parameters = (), context = <sqlalchemy.dialects.sqlite.base.SQLiteExecutionContext object at 0x000002D7C124BE30>

    def do_execute(self, cursor, statement, parameters, context=None):
>       cursor.execute(statement, parameters)
E       sqlite3.IntegrityError: NOT NULL constraint failed: companies.is_active

.venv\Lib\site-packages\sqlalchemy\engine\default.py:952: IntegrityError

The above exception was the direct cause of the following exception:

monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x000002D7C123BE90>
tmp_path = WindowsPath('D:/winprojects/analyzer/.pytest_db_impl_001_20261121/test_failed_migration_nine_kee0')

    def test_failed_migration_nine_keeps_duplicate_legacy_rows_and_is_not_recorded(monkeypatch, tmp_path):
        engine = create_engine(f"sqlite:///{tmp_path / 'duplicate-symbols.sqlite'}")
        all_migrations = tuple(migration_runner._migration_list())
        monkeypatch.setattr(migration_runner, "_migration_list", lambda: all_migrations[:8])
        assert MigrationRunner(engine).upgrade() == 8
        with engine.begin() as connection:
            connection.execute(text("INSERT INTO industries (industry_code, industry_name) VALUES ('BANK','Bank')"))
>           connection.execute(text("INSERT INTO companies (ticker, company_name, industry_id, codal_symbol, status) VALUES ('DUP','One',1,'A','ACTIVE'),('DUP','Two',1,'B','ACTIVE')"))

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

self = <sqlalchemy.dialects.sqlite.pysqlite.SQLiteDialect_pysqlite object at 0x000002D7C123AC60>
cursor = <sqlite3.Cursor object at 0x000002D7C123E5C0>
statement = "INSERT INTO companies (ticker, company_name, industry_id, codal_symbol, status) VALUES ('DUP','One',1,'A','ACTIVE'),('DUP','Two',1,'B','ACTIVE')"
parameters = (), context = <sqlalchemy.dialects.sqlite.base.SQLiteExecutionContext object at 0x000002D7C124BE30>

    def do_execute(self, cursor, statement, parameters, context=None):
>       cursor.execute(statement, parameters)
E       sqlalchemy.exc.IntegrityError: (sqlite3.IntegrityError) NOT NULL constraint failed: companies.is_active
E       [SQL: INSERT INTO companies (ticker, company_name, industry_id, codal_symbol, status) VALUES ('DUP','One',1,'A','ACTIVE'),('DUP','Two',1,'B','ACTIVE')]
E       (Background on this error at: https://sqlalche.me/e/20/gkpj)

.venv\Lib\site-packages\sqlalchemy\engine\default.py:952: IntegrityError
=============================================== short test summary info ===============================================
FAILED src/tests/test_canonical_writer.py::test_failed_migration_nine_keeps_duplicate_legacy_rows_and_is_not_recorded - sqlalchemy.exc.IntegrityError: (sqlite3.IntegrityError) NOT NULL constraint failed: companies.is_active
1 failed, 93 passed in 390.35s (0:06:30)