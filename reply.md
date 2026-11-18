D:\Winprojects\analyzer\src\evaluation\observation.py:80: financial_period_id: int
D:\Winprojects\analyzer\src\evaluation\observation.py:105: self.financial_period_id,
D:\Winprojects\analyzer\src\evaluation\observation.py:125: financial_period_id=record.forecast_period_id,
D:\Winprojects\analyzer\src\evaluation\pipeline.py:151: ``(company_id, financial_period_id, metric_code)``. Each value is a
D:\Winprojects\analyzer\src\evaluation\reliability.py:267: Periods are opaque ordered identifiers (financial_period_id values); the
D:\Winprojects\analyzer\src\evaluation\schema.py:72: * ``financial_period_id`` — the period the value *describes*. It is not a
D:\Winprojects\analyzer\src\evaluation\schema.py:84: financial_period_id: int
D:\Winprojects\analyzer\src\forecast\queries.py:25: from src.models.period import FinancialPeriod
D:\Winprojects\analyzer\src\forecast\queries.py:60: FinancialPeriod.period_id,
D:\Winprojects\analyzer\src\forecast\queries.py:61: FinancialPeriod.end_date,
D:\Winprojects\analyzer\src\forecast\queries.py:73: .join(FinancialPeriod,
D:\Winprojects\analyzer\src\forecast\queries.py:74: NormalizedFinancialFact.period_id == FinancialPeriod.period_id)
D:\Winprojects\analyzer\src\ingestion\service.py:33: from src.models.period import FinancialPeriod
D:\Winprojects\analyzer\src\ingestion\service.py:143: period = session.get(FinancialPeriod, period_id)
D:\Winprojects\analyzer\src\ingestion\service.py:157: or report.financial_period_id != period_id
D:\Winprojects\analyzer\src\ingestion\service.py:170: financial_period_id=period_id,
D:\Winprojects\analyzer\src\migrations\runner.py:30: from src.models.period import FinancialPeriod  # noqa: F401
D:\Winprojects\analyzer\src\models\forecast.py:30: from src.models.period import FinancialPeriod  # noqa: E402,F401
D:\Winprojects\analyzer\src\models\forecast.py:33: for _model in (Company, FinancialPeriod, ReportVersion):
D:\Winprojects\analyzer\src\models\period.py:15: class FinancialPeriod(Base):
D:\Winprojects\analyzer\src\models\report.py:30: financial_period_id = Column(Integer, ForeignKey("financial_periods.period_id"), nullable=False)
D:\Winprojects\analyzer\src\scripts\init_db.py:6: from src.models.period import FinancialPeriod
D:\Winprojects\analyzer\src\tests\test_codal_extraction.py:24: from src.models.period import FinancialPeriod
D:\Winprojects\analyzer\src\tests\test_codal_extraction.py:90: period = FinancialPeriod(
D:\Winprojects\analyzer\src\tests\test_codal_extraction.py:304: other_period = FinancialPeriod(
D:\Winprojects\analyzer\src\tests\test_codal_extraction.py:353: other_period = FinancialPeriod(
D:\Winprojects\analyzer\src\tests\test_codal_pdf_extraction.py:21: from src.models.period import FinancialPeriod
D:\Winprojects\analyzer\src\tests\test_codal_pdf_extraction.py:91: period = FinancialPeriod(
D:\Winprojects\analyzer\src\tests\test_codal_pdf_extraction.py:403: assert report.financial_period_id == period.period_id
D:\Winprojects\analyzer\src\tests\test_codal_pdf_extraction.py:655: assert report.financial_period_id == period.period_id
D:\Winprojects\analyzer\src\tests\test_codal_pdf_extraction.py:728: assert report.financial_period_id == period.period_id
D:\Winprojects\analyzer\src\tests\test_codal_pdf_extraction.py:743: # FinancialPeriod linkage remains correct end to end.
D:\Winprojects\analyzer\src\tests\test_codal_pdf_extraction.py:744: persisted_period = session.get(FinancialPeriod, report.financial_period_id)
D:\Winprojects\analyzer\src\tests\test_stage1_database_architecture.py:10: from src.models.period import FinancialPeriod
D:\Winprojects\analyzer\src\tests\test_stage1_database_architecture.py:33: period = FinancialPeriod(
D:\Winprojects\analyzer\src\tests\test_stage1_database_architecture.py:49: financial_period_id=period.period_id,
D:\Winprojects\analyzer\src\tests\test_stage1_database_integrity.py:24: from src.models.period import FinancialPeriod
D:\Winprojects\analyzer\src\tests\test_stage1_database_integrity.py:67: connection.execute(text("INSERT INTO reports (company_id, report_type, title, financial_period_id, is_correction) VALUES (1, 'QUARTERLY', 'preserve-report', 1, 0)"))
D:\Winprojects\analyzer\src\tests\test_stage1_database_integrity.py:110: period = FinancialPeriod(
D:\Winprojects\analyzer\src\tests\test_stage1_database_integrity.py:126: financial_period_id=period.period_id,
D:\Winprojects\analyzer\src\tests\test_stage1_rules.py:25: from src.models.period import FinancialPeriod
D:\Winprojects\analyzer\src\tests\test_stage1_rules.py:58: period = FinancialPeriod(
D:\Winprojects\analyzer\src\tests\test_stage1_rules.py:88: report = Report(company_id=company.company_id, report_type="QUARTERLY", title="Test report", financial_period_id=period.period_id)
D:\Winprojects\analyzer\src\tests\test_stage1_rules.py:113: invalid_type = FinancialPeriod(company_id=company.company_id, period_type="INVALID", start_date=date(2024, 1, 1), end_date=date(2024, 3, 31), fiscal_year=1403, months_length=3)
D:\Winprojects\analyzer\src\tests\test_stage1_rules.py:118: invalid_company = FinancialPeriod(company_id=999999, period_type="MONTH", start_date=date(2024, 1, 1), end_date=date(2024, 1, 31), fiscal_year=1403, months_length=1)
D:\Winprojects\analyzer\src\tests\test_stage1_rules.py:127: report = Report(company_id=company.company_id, report_type="QUARTERLY", title="Test report", financial_period_id=period.period_id)
D:\Winprojects\analyzer\src\tests\test_stage1_rules.py:146: report = Report(company_id=company.company_id, report_type="QUARTERLY", title="PIT report", financial_period_id=period.period_id)
D:\Winprojects\analyzer\src\tests\test_stage1_rules.py:193: report = Report(company_id=company.company_id, report_type="QUARTERLY", title="EPS source", financial_period_id=period.period_id)
D:\Winprojects\analyzer\src\tests\test_stage5_forecast.py:814: from src.models.period import FinancialPeriod  # noqa: E402
D:\Winprojects\analyzer\src\tests\test_stage5_forecast.py:889: session.add(FinancialPeriod(
D:\Winprojects\analyzer\src\tests\test_stage5_forecast.py:918: financial_period_id=PERIOD_ID,
D:\Winprojects\analyzer\src\tests\test_stage6_artifact_boundary.py:62: financial_period_id=101,
D:\Winprojects\analyzer\src\tests\test_stage6_artifact_identity.py:74: financial_period_id=101,
D:\Winprojects\analyzer\src\tests\test_stage6_artifact_identity.py:339: financial_period_id=101, data_quality_state="ESTIMATED"
D:\Winprojects\analyzer\src\tests\test_stage6_artifact_identity.py:342: financial_period_id=102,
D:\Winprojects\analyzer\src\tests\test_stage6_artifact_identity.py:389: (7, 101, "REVENUE"): _actual(financial_period_id=101),
D:\Winprojects\analyzer\src\tests\test_stage6_artifact_identity.py:391: financial_period_id=102,
D:\Winprojects\analyzer\src\tests\test_stage6_evaluation.py:159: financial_period_id=period,
D:\Winprojects\analyzer\src\tests\test_stage6_evaluation_foundation.py:72: financial_period_id=101,
D:\Winprojects\analyzer\src\tests\test_stage6_evaluation_metrics.py:68: financial_period_id=101,
D:\Winprojects\analyzer\src\tests\test_stage6_evaluation_metrics.py:86: financial_period_id=record.forecast_period_id,
D:\Winprojects\analyzer\src\tests\test_stage6_p25_adversarial.py:57: financial_period_id=101,
D:\Winprojects\analyzer\src\tests\test_stage6_p25_adversarial.py:115: financial_period_id=102, publication_datetime=MID,
D:\Winprojects\analyzer\src\tests\test_stage6_p25_adversarial.py:118: financial_period_id=102, publication_datetime=MID,
D:\Winprojects\analyzer\src\tests\test_stage6_p25_adversarial.py:357: _actual(financial_period_id=101 + i,
D:\Winprojects\analyzer\src\tests\test_stage6_p25_selection.py:70: financial_period_id=101,
D:\Winprojects\analyzer\src\tests\test_stage6_p38_closure.py:72: financial_period_id=period,
D:\Winprojects\analyzer\src\tests\test_stage6_p39_cutoff.py:64: financial_period_id=period,
D:\Winprojects\analyzer\src\tests\test_stage6_p40_duplicates.py:65: financial_period_id=period,
D:\Winprojects\analyzer\src\tests\test_stage6_p41_cutoff_identity.py:64: financial_period_id=period,
D:\Winprojects\analyzer\src\tests\test_stage6_production_pipeline.py:97: financial_period_id=period,
D:\Winprojects\analyzer\src\tests\test_stage6_reliability_governance.py:86: financial_period_id=101,
D:\Winprojects\analyzer\src\tests\test_stage6_reliability_governance.py:105: financial_period_id=record.forecast_period_id,
D:\Winprojects\analyzer\src\tests\test_stage6_scenario_isolation.py:65: financial_period_id=101,
D:\Winprojects\analyzer\src\tests\test_stage6_scenario_isolation.py:83: financial_period_id=record.forecast_period_id,
D:\Winprojects\analyzer\src\tests\test_stage6_scenario_isolation.py:223: financial_period_id=101,
