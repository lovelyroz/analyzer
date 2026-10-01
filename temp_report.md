REPORT : PROMPT 3 — Stage 4 → Stage 5 Production Boundary 
1. Files changed
File	Change
src/forecast/adapter.py	new — Stage 4 → Stage 5 translation boundary
src/forecast/builder.py	new — weighted average share builder
src/forecast/engine.py	modified — one _share_count() helper replacing 4 inline forecast_weighted_average_shares OR share_count lookups
src/tests/test_stage5_forecast.py	modified — +23 focused tests

No changes to schema.py, migrations, or Stage 1–4 modules.

2. Stage 4 adapter

Stage4Context is a frozen dataclass of translated evidence; adapt_stage4(TrendResult) and build_financial_context(...) are the entry points. It maps trend state, coverage, confidence, seasonal baseline/sufficiency, seasonal naive, run rate, 12M momentum + relative strength, low base, sign change, data sufficiency, and a stage4_provenance block (metric/period/timestamp/observation count) for §29 auditability.

It is strictly a translation: trend_state is carried as a direction, never converted to growth — no arithmetic except a sign test. The monetary baselines are caller-supplied because Stage 4 is metric-scoped and doesn't produce currency values. seasonality_valid requires Stage 4's own data_sufficiency == "FULL" plus a non-null baseline, so an insufficient seasonal baseline can't outrank the run rate. Sign change reads Layer 4 first, falling back to Layer 1/2 flags.

3. Weighted-share builder

build_weighted_average_shares(history, actions, cutoff=, window_start=) returns a frozen WeightedAverageShares. ShareCountHistory observations are the authoritative series; a CorporateAction beyond the last observation extends it. new_share_count is authoritative, ratio is the fallback. Supports unchanged, capital increase/decrease, and split/consolidation. Unresolvable actions are reported in notes and skipped, not guessed.

4. PIT / cutoff behavior

Three independent cutoff guards: history after the cutoff is invisible; actions effective after the cutoff are dropped; and an action effective before the cutoff but announced after it is dropped with a note — a forecast dated before the announcement couldn't have known the new count. Missing data propagates as shares=None (NO_SHARE_HISTORY / NO_OBSERVATION_AT_OR_BEFORE_CUTOFF), never zero and never fabricated. WeightedAverageShares objects pass straight through the engine's new _share_count() helper via its .get() method, so builder output feeds EPS without an intermediate field.

5. Tests

Before: 31 passed. After: 54 passed (31 original + 23 new) in 0.26s. The 12 required cases are covered — in several cases two tests per case for the Layer-4 vs Layer-1/2 fallback paths and the multiple cutoff guards. Stage 4 suite also re-checked: 102 passed, unaffected.

6. Failures

None. Two intermediate tool glitches were caught and fixed before they landed: a corrupted first write of adapter.py (rewrote, verified by AST parse) and a malformed forecast_ending_equity line in engine.py (fixed at line 308, compile-checked).

7. Remaining Stage 5 gaps
build_weighted_average_shares is not yet wired to a database session — no production caller queries ShareCountHistory/CorporateAction. Tests use duck-typed stand-ins matching the model shape.
No production caller assembles financial_context end-to-end via build_financial_context; the DB → Stage 1 facts join is still missing.
window_start defaults to the oldest observation, so the weighted average is over the full observed span rather than a strict forecast window; a caller that wants a narrower window must pass it explicitly.

Stage 5 is NOT declared frozen.

==================================================================================
REPORT PROMPT 4 — Forecast Persistence / Repository

گزارش نهایی
مدل‌های اضافه‌شده

فایل جدید src/models/forecast.py (هر دو مدل حداقلی مورد نیاز، هیچ مدل دیگری تغییر نکرد):

ForecastVersion در جدول forecast_versions — یک نسخه غیرقابل تغییر از یک پیش‌بینی scenario. کلید اصلی سوروگیت forecast_version_id؛ کلید کسب‌وکار (company، forecast period، horizon، scenario) + version_number تحت یک unique constraint (uq_forecast_version) قرار دارد تا یک save فقط بتواند یک سطر جدید را append کند، هرگز جایگزین نکند. تمام فیلدهای PIT/contract از §28: forecast_timestamp, data_cutoff_datetime, model_version, scenario, forecast_method, data_quality, baseline_method, industry_code, شش معیار + assumptions (JSON). مقادیر معیار nullable هستند تا NULL مساوی صفر فرض نشود (§27).
ForecastInputRefModel در جدول forecast_input_refs — پل provenance، یک سطر برای هر ref ورودی، با available_at که lookahead-پذیری پیش‌بینی را حفظ می‌کند (§29). FK به forecast_versions با ondelete=CASCADE و FK اختیاری به report_versions با ondelete=SET NULL (پیروی از قانونی که مدل‌های موجود برای FKهای اختیاری استفاده می‌کنند).
رفتار ریپازیتوری — src/forecast/repo.py (فایل جدید)

ForecastRecordRepository(session) از همان ForecastRecord که توسط ForecastVersionStore در حافظه (in-memory) استفاده می‌شود، تغذیه می‌کند، بنابراین یک پیاده‌سازی PIT دوم وجود ندارد: normalize_datetime، ForecastInputRef و ForecastVersionExistsError از src/forecast/schema.py مجدداً استفاده می‌شوند. session در هر فراخوانی مورد انتظار است، بنابراین فراخوانی صاحب مرز تراکنش است؛ ریپازیتوری فقط insert/می‌خواند.

معناشناسی نسخه‌بندی

یک سری توسط (company_id, forecast_period_id, forecast_horizon, scenario) — همان ForecastRecord.key() — شناسایی می‌شود. برای هر save: نسخه caller-supplied که با محتوای متفاوت موجود است، ForecastVersionExistsError پرتاب می‌کند (بدون overwrite خاموش)؛ یک رکورد که با آخرین نسخه ذخیره‌شده برابر باشد، بدون insert برمی‌گردد (idempotent)؛ در غیر این صورت version_number آخرین + ۱ می‌شود. سطرهای قدیمی هرگز UPDATE نمی‌شوند.

معناشناسی persistence

فقط insert. history() تمام نسخه‌های حفظ شده را از قدیم به جدید برمی‌گرداند، latest()، count()، revision_trend() (UPWARD/DOWNWARD/MIXED، §24)، read_at_cutoff() و pit_violations() (§25) را برمی‌گرداند. datetimes در مسیر خواندن مجدداً نرمالایز می‌شوند زیرا SQLite آن‌ها را naive برمی‌گرداند، بنابراین رکوردهای بازیابی شده با همان قرارداد UTC-aware در حافظه مطابقت دارند.

تست‌ها

۱۴ تست persistence به src/tests/test_stage5_forecast.py اضافه شد (۱۱ مورد درخواستی + trend مختلط + PIT cutoff + اضافی): اولین save، نسخه دوم، قدیمی قابل خواندن باقی می‌ماند، عدم overwrite، duplicate idempotent، نسخه متعارض rejected (asserted به هیچ ردیفی پشت سر باقی نمی‌ماند)، جداسازی scenario، جداسازی horizon، تمام فیلدهای PIT حفظ می‌شوند، input provenance preserved، revision trend از نسخه‌های ذخیره‌شده. fixture از یک schema در حافظه (MigrationRunner(...).upgrade()) جدا از دیتابیس production on-disk استفاده می‌کند.

pytest src/tests/test_stage5_forecast.py -v → ۶۷ passed (۵۳ تست موجود بدون تغییر باقی ماند).

دو تست Stage 1 که hardcode شده بودند runner.upgrade() == 6 یک‌بار شکست خوردند (یک state واقع که migration جدید این انتظار را نامعتبر می‌کند)، بنابراین من آن‌ها را به ۷ به‌روزرسانی کردم — و نام اولین مورد را تغییر دادم تا آنچه را که بررسی می‌کند توصیف کند. test_stage1_database_integrity.py (۳ passed) و test_stage1_rules.py (۱۳ passed) هر دو سبز هستند.

حفره‌های باقی‌مانده
ForecastEngine به ریپازیتوری متصل نیست. هیچ مسیر تولید هنوز ForecastRecordRepository.save را صدا نمی‌زند؛ آن فقط توسط تست‌ها exercisable است. pipeline زیرسازی Stage 5 → Stage 6 خارج از محدوده این وظیفه بود.
برنامه‌ریزی کالیبراسیون Stage 6 (اختیاری، در اینجا اضافه نشد): _apply_forecast_version_repository از الگوی additive migrations پیروی می‌کند، اما یک migration پایه برای دیتابیس‌های legacy که از طریق migration 1 بوت‌استرپ می‌شوند نیاز دارد. چون migration 1 قبل از وجود این جداول ثبت شده بود، دیتابیس legacy تنها با upgrade به v7 به‌درستی بوت‌استرپ نمی‌شود. این حفره شناخته‌شده است: اگر پیاده‌سازی فعلی برای کالیبراسیون Stage 6 ضروری باشد، احتمالاً باید Base.metadata.create_all در migration 1 قرار می‌گرفت. اگر این موضوع اکنون مهم است، پذیرش صریح نیاز است (defaulting پنهان، مانند انتقال نقطه ورود، غیرقابل اجتناب است).
ساختار جدول، نه داده. مهاجرت schema ایجاد می‌کند اما چیزی seed نمی‌کند — پیش‌بینی‌های موجود تولید نمی‌شوند (طبق شرط توقف، هیچ forecasting واقعی پیاده‌سازی نشده است).

Stage 5 فریز نشده است.