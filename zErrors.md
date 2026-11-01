# zErrors — رفع شکست‌های ثبت‌شده

سه آزمون Stage 7 با `AttributeError` شکست می‌خوردند، چون helper آزمون `_d9_forecast_without_cutoff` یک `SimpleNamespace` بدون `company_id` و `forecast_period_id` می‌ساخت. پس از اضافه‌شدن guard تطبیق هویت در Engine، این fixture دیگر قرارداد ورودیِ حداقلی را رعایت نمی‌کرد.

اصلاح: helper اکنون شناسه‌های شرکت و دوره را از Forecast پایه کپی می‌کند و همچنان `data_cutoff_datetime=None` نگه می‌دارد؛ بنابراین آزمون‌های D9 همان رفتار بدون cutoff را می‌سنجند و guard هویت در Engine دست‌نخورده می‌ماند.

آزمون‌ها پس از اصلاح اجرا نشده‌اند. فرمان بررسی:
`pytest src/tests/test_stage7_valuation.py -q`
