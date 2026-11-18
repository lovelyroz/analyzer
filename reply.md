
src\evaluation\observation.py:80:    financial_period_id: int
src\evaluation\observation.py:105:            self.financial_period_id,
src\evaluation\observation.py:125:        financial_period_id=record.forecast_period_id,
src\evaluation\pipeline.py:151:      ``(company_id, financial_period_id, metric_code)``. Each value is a
src\evaluation\reliability.py:267:    Periods are opaque ordered identifiers (financial_period_id values); the
src\evaluation\schema.py:72:    * ``financial_period_id`` — the period the value *describes*. It is not a
src\evaluation\schema.py:84:    financial_period_id: int
src\ingestion\service.py:13:  - CODAL raw persistence (ingest_codal_report)
src\ingestion\service.py:112:def ingest_codal_report(
src\ingestion\service.py:157:            or report.financial_period_id != period_id
src\ingestion\service.py:170:                financial_period_id=period_id,
src\ingestion\__init__.py:22:    ingest_codal_report,
src\ingestion\__init__.py:34:    "ingest_codal_report",
src\ingestion\codal\ingestion.py:17:def ingest_codal_report(
src\ingestion\codal\ingestion.py:31:    from src.ingestion.service import ingest_codal_report as _persist
src\ingestion\codal\ingestion.py:47:def ingest_codal_pdf(
src\ingestion\codal\ingestion.py:90:    return ingest_codal_report(
src\ingestion\codal\ingestion.py:104:__all__ = ["ingest_codal_report", "ingest_codal_pdf"]
src\ingestion\codal\pipeline.py:19:from src.ingestion.service import ReportIngestionResult, ingest_codal_report
src\ingestion\codal\pipeline.py:72:    return ingest_codal_report(
src\ingestion\codal\pipeline.py:86:def load_codal_pdf(
src\ingestion\codal\pipeline.py:131:def load_codal_pdf_from_url(
src\ingestion\codal\__init__.py:10:from src.ingestion.codal.ingestion import ingest_codal_report
src\ingestion\codal\__init__.py:21:    "ingest_codal_report",
src\models\report.py:30:    financial_period_id = Column(Integer, ForeignKey("financial_periods.period_id"), 
nullable=False)
src\scripts\audit_codal_pdf_dependencies.py:32:    "ingest_codal_report",
src\scripts\audit_codal_pdf_dependencies.py:33:    "ingest_codal_pdf",
src\scripts\audit_codal_pdf_dependencies.py:34:    "load_codal_pdf",
src\scripts\audit_codal_pdf_dependencies.py:35:    "load_codal_pdf_from_url",
src\tests\test_codal_extraction.py:19:from src.ingestion.codal.pipeline import load_codal_pdf
src\tests\test_codal_extraction.py:20:from src.ingestion.service import RawLineInput, ingest_codal_report
src\tests\test_codal_extraction.py:185:    result = load_codal_pdf(
src\tests\test_codal_extraction.py:211:    from src.ingestion.codal.pipeline import load_codal_pdf
src\tests\test_codal_extraction.py:214:        load_codal_pdf(
src\tests\test_codal_extraction.py:233:    from src.ingestion.codal.pipeline import load_codal_pdf
src\tests\test_codal_extraction.py:239:        load_codal_pdf(
src\tests\test_codal_extraction.py:259:    r1 = load_codal_pdf(
src\tests\test_codal_extraction.py:269:    r2 = load_codal_pdf(
src\tests\test_codal_extraction.py:318:        ingest_codal_report(
src\tests\test_codal_extraction.py:333:    first = ingest_codal_report(
src\tests\test_codal_extraction.py:367:        ingest_codal_report(
src\tests\test_codal_pdf_extraction.py:10:from src.ingestion.codal.ingestion import ingest_codal_pdf
src\tests\test_codal_pdf_extraction.py:17:from src.ingestion.service import RawLineInput, ingest_codal_report
src\tests\test_codal_pdf_extraction.py:271:        ingest_codal_pdf(
src\tests\test_codal_pdf_extraction.py:306:    result = ingest_codal_report(
src\tests\test_codal_pdf_extraction.py:339:    result = ingest_codal_report(
src\tests\test_codal_pdf_extraction.py:369:        results.append(ingest_codal_pdf(
src\tests\test_codal_pdf_extraction.py:393:    result = ingest_codal_pdf(
src\tests\test_codal_pdf_extraction.py:403:    assert report.financial_period_id == period.period_id
src\tests\test_codal_pdf_extraction.py:456:    first = ingest_codal_report(
src\tests\test_codal_pdf_extraction.py:462:    second = ingest_codal_report(
src\tests\test_codal_pdf_extraction.py:506:    The idempotency key in ingest_codal_report() is (codal_tracking_id,
src\tests\test_codal_pdf_extraction.py:539:    first = ingest_codal_report(**ingest_kwargs)
src\tests\test_codal_pdf_extraction.py:548:    second = ingest_codal_report(**ingest_kwargs)
src\tests\test_codal_pdf_extraction.py:549:    third = ingest_codal_report(**ingest_kwargs)
src\tests\test_codal_pdf_extraction.py:638:    result = ingest_codal_pdf(
src\tests\test_codal_pdf_extraction.py:655:    assert report.financial_period_id == period.period_id
src\tests\test_codal_pdf_extraction.py:710:    result = ingest_codal_pdf(
src\tests\test_codal_pdf_extraction.py:728:    assert report.financial_period_id == period.period_id
src\tests\test_codal_pdf_extraction.py:744:    persisted_period = session.get(FinancialPeriod, 
report.financial_period_id)
src\tests\test_codal_pdf_extraction.py:797:    first = ingest_codal_pdf(
src\tests\test_codal_pdf_extraction.py:807:    second = ingest_codal_pdf(
src\tests\test_codal_pdf_extraction.py:886:    result = ingest_codal_pdf(
src\tests\test_stage1_database_architecture.py:49:        financial_period_id=period.period_id,
src\tests\test_stage1_database_integrity.py:67:        connection.execute(text("INSERT INTO reports (company_id, 
report_type, title, financial_period_id, is_correction) VALUES (1, 'QUARTERLY', 'preserve-report', 1, 0)"))
src\tests\test_stage1_database_integrity.py:126:        financial_period_id=period.period_id,
src\tests\test_stage1_rules.py:11:from src.ingestion.service import RawLineInput, ingest_codal_report
src\tests\test_stage1_rules.py:88:    report = Report(company_id=company.company_id, report_type="QUARTERLY", 
title="Test report", financial_period_id=period.period_id)
src\tests\test_stage1_rules.py:127:    report = Report(company_id=company.company_id, report_type="QUARTERLY", 
title="Test report", financial_period_id=period.period_id)
src\tests\test_stage1_rules.py:146:    report = Report(company_id=company.company_id, report_type="QUARTERLY", 
title="PIT report", financial_period_id=period.period_id)
src\tests\test_stage1_rules.py:193:    report = Report(company_id=company.company_id, report_type="QUARTERLY", 
title="EPS source", financial_period_id=period.period_id)
src\tests\test_stage5_forecast.py:918:        financial_period_id=PERIOD_ID,
src\tests\test_stage6_artifact_boundary.py:62:        financial_period_id=101,
src\tests\test_stage6_artifact_identity.py:74:        financial_period_id=101,
src\tests\test_stage6_artifact_identity.py:339:            financial_period_id=101, data_quality_state="ESTIMATED"
src\tests\test_stage6_artifact_identity.py:342:            financial_period_id=102,
src\tests\test_stage6_artifact_identity.py:389:        (7, 101, "REVENUE"): _actual(financial_period_id=101),
src\tests\test_stage6_artifact_identity.py:391:            financial_period_id=102,
src\tests\test_stage6_evaluation.py:159:            financial_period_id=period,
src\tests\test_stage6_evaluation_foundation.py:72:        financial_period_id=101,
src\tests\test_stage6_evaluation_metrics.py:68:        financial_period_id=101,
src\tests\test_stage6_evaluation_metrics.py:86:            financial_period_id=record.forecast_period_id,
src\tests\test_stage6_p25_adversarial.py:57:        financial_period_id=101,
src\tests\test_stage6_p25_adversarial.py:115:                      financial_period_id=102, publication_datetime=MID,
src\tests\test_stage6_p25_adversarial.py:118:                     financial_period_id=102, publication_datetime=MID,
src\tests\test_stage6_p25_adversarial.py:357:            _actual(financial_period_id=101 + i,
src\tests\test_stage6_p25_selection.py:70:        financial_period_id=101,
src\tests\test_stage6_p38_closure.py:72:        financial_period_id=period,
src\tests\test_stage6_p39_cutoff.py:64:        financial_period_id=period,
src\tests\test_stage6_p40_duplicates.py:65:        financial_period_id=period,
src\tests\test_stage6_p41_cutoff_identity.py:64:        financial_period_id=period,
src\tests\test_stage6_production_pipeline.py:97:        financial_period_id=period,
src\tests\test_stage6_reliability_governance.py:86:        financial_period_id=101,
src\tests\test_stage6_reliability_governance.py:105:            financial_period_id=record.forecast_period_id,
src\tests\test_stage6_scenario_isolation.py:65:        financial_period_id=101,
src\tests\test_stage6_scenario_isolation.py:83:            financial_period_id=record.forecast_period_id,
src\tests\test_stage6_scenario_isolation.py:223:            financial_period_id=101,


