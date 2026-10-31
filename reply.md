(analyzer) PS D:\winprojects\analyzer> rg -n "ForecastRecordRepository|ForecastVersion|ForecastInputRefModel|generate_and_persist_forecast|forecast_versions|forecast_input_refs" src
src\valuation\engine.py
71:        forecast_input_refs: Optional[Sequence[ForecastInputRef]] = None,
131:            forecast_input_refs = tuple(forecast_input_refs or ()) + normalized_embedded_refs
133:            forecast_input_refs=forecast_input_refs,
355:        forecast_input_refs: Optional[Sequence[ForecastInputRef]],
370:        if not forecast_input_refs:
372:        for ref in forecast_input_refs:

src\forecast\__init__.py
12:from src.forecast.service import generate_and_persist_forecast
20:    "generate_and_persist_forecast",

src\models\forecast.py
26:class ForecastVersion(Base):
34:    __tablename__ = "forecast_versions"
84:class ForecastInputRefModel(Base):
92:    __tablename__ = "forecast_input_refs"
97:        ForeignKey("forecast_versions.forecast_version_id", ondelete="CASCADE"),

src\tests\test_stage1_database_integrity.py
37:    assert {"forecast_versions", "forecast_input_refs"}.issubset(tables)

src\forecast\service.py
10:        -> ForecastRecordRepository
11:        -> persistent ForecastVersion / ForecastInputRef
41:from src.forecast.repo import ForecastRecordRepository
294:def generate_and_persist_forecast(
408:        repository = ForecastRecordRepository(session)

src\migrations\runner.py
25:from src.models.forecast import ForecastInputRefModel, ForecastVersion  # noqa: F401
149:        Base.metadata.tables["forecast_versions"],
150:        Base.metadata.tables["forecast_input_refs"],

src\forecast\schema.py
227:class ForecastVersionExistsError(ValueError):
273:class ForecastVersionStore:
295:                    raise ForecastVersionExistsError(

src\forecast\repo.py
8:``ForecastVersionStore``. Both implement the same versioning contract — a new
27:    ForecastVersionExistsError,
30:from src.models.forecast import ForecastInputRefModel, ForecastVersion
45:class ForecastRecordRepository:
75:                raise ForecastVersionExistsError(
82:        row = ForecastVersion(
108:            self.session.add(ForecastInputRefModel(
126:            select(ForecastVersion)
128:            .order_by(ForecastVersion.version_number.asc())
170:            select(ForecastVersion)
171:            .where(ForecastVersion.data_cutoff_datetime <= cutoff)
180:            select(func.count()).select_from(ForecastVersion)
187:    def _to_record(self, row: ForecastVersion) -> ForecastRecord:
196:                select(ForecastInputRefModel)
197:                .where(ForecastInputRefModel.forecast_version_id == row.forecast_version_id)
198:                .order_by(ForecastInputRefModel.input_ref_id.asc())
231:                    scenario: str) -> Optional[ForecastVersion]:
233:            select(ForecastVersion)
235:            .order_by(ForecastVersion.version_number.desc())
239:                     scenario: str, version: int) -> Optional[ForecastVersion]:
241:            select(ForecastVersion)
244:                ForecastVersion.version_number == version,
248:    def _records_equal(self, row: ForecastVersion, record: ForecastRecord) -> bool:
284:        ForecastVersion.company_id == company_id,
285:        ForecastVersion.forecast_period_id == forecast_period_id,
286:        ForecastVersion.forecast_horizon == horizon,
287:        ForecastVersion.scenario == scenario.upper(),

src\tests\test_stage7_valuation.py
1350:    with_refs = engine.calculate_valuation(**_p32_kwargs(forecast_input_refs=refs))
1362:            **_p32_kwargs(forecast_input_refs=[_p32_ref(datetime(2026, 3, 1))])
1369:        **_p32_kwargs(forecast_input_refs=[_p32_ref(datetime(2026, 1, 1))])
1378:        engine.calculate_valuation(**_p32_kwargs(forecast_input_refs=[_p32_ref(None)]))
1383:    result = engine.calculate_valuation(**_p32_kwargs(forecast_input_refs=None))
1458:            **_p32_kwargs(forecast_result=forecast, forecast_input_refs=[])

src\forecast\engine.py
744:        declared = context.get("input_refs") or context.get("forecast_input_refs") or []

src\tests\test_stage6_production_pipeline.py
549:        "ForecastRecordRepository",
550:        "forecast_versions",

src\tests\test_stage5_forecast.py
13:    ForecastVersionExistsError,
14:    ForecastVersionStore,
347:    store = ForecastVersionStore()
367:    store = ForecastVersionStore()
381:    store = ForecastVersionStore()
432:    store = ForecastVersionStore()
439:    store = ForecastVersionStore()
443:    with pytest.raises(ForecastVersionExistsError):
458:    store = ForecastVersionStore()
465:    store2 = ForecastVersionStore()
472:    store3 = ForecastVersionStore()
478:    store = ForecastVersionStore()
517:    store = ForecastVersionStore()
552:    store = ForecastVersionStore()
558:    store = ForecastVersionStore()
569:    store = ForecastVersionStore()
996:from src.forecast.repo import ForecastRecordRepository  # noqa: E402
1006:    yield ForecastRecordRepository(session)
1109:    with pytest.raises(ForecastVersionExistsError):
1130:    with pytest.raises(ForecastVersionExistsError):
1230:#     ForecastRecord -> ForecastRecordRepository (spec sections 9, 15-16,
1236:    generate_and_persist_forecast,
1551:    forecast = generate_and_persist_forecast(
1567:    forecast = generate_and_persist_forecast(
1576:    persisted = ForecastRecordRepository(production_db).latest(
1592:    forecast = generate_and_persist_forecast(
1606:    forecast = generate_and_persist_forecast(
1619:    generate_and_persist_forecast(
1622:    repository = ForecastRecordRepository(production_db)
1634:    forecast = generate_and_persist_forecast(
1637:    reloaded = ForecastRecordRepository(production_db).latest(
1655:    forecast = generate_and_persist_forecast(
1658:    reloaded = ForecastRecordRepository(production_db).latest(
1681:    repository = ForecastRecordRepository(production_db)
1682:    generate_and_persist_forecast(
1687:    generate_and_persist_forecast(
1703:    forecast = generate_and_persist_forecast(
1711:    reloaded = ForecastRecordRepository(empty_share_db).latest(
1727:            return generate_and_persist_forecast(
3953:    forecast = generate_and_persist_forecast(
4094:    forecast = generate_and_persist_forecast(
4409:    forecast = generate_and_persist_forecast(

