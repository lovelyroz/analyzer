 ترتیب اجرای کار از اینجا
1. ثبت سیاست‌های V1: همین تصمیم‌ها مبنای بررسی مستندات قرار بگیرند؛ هنوز به معنی تغییر کد نیستند.
2. بررسی محدود مستندات: فقط بخش‌های مرتبط از stage_7_prompts.md، temp_report2.md و قراردادهای مرتبط بررسی شوند؛ فعلاً نیازی به اسکن کل مخزن نیست.
3. رفع تناقض مشخصات و تست‌ها: ابتدا تفاوت میان رفتار فعلی، نیازمندی مستند و دو تست شکست‌خورده روشن شود.
4. پیاده‌سازی مرحله‌ای: پس از مشخص‌شدن اصلاحات دقیق، تو کد را در محیط محلی تغییر می‌دهی و من در انتخاب تغییرات و بررسی نتایج راهنمایی‌ات می‌کنم.
5. اعتبارسنجی چندلایه: تست‌های هدفمند، تست‌های یکپارچه، مجموعهٔ کامل تست‌ها و بررسی نهایی محدودیت‌های مالی انجام می‌شوند.
6. بازنگری engine.py: فقط پس از رفع موارد باز Stage 7، طبق برنامهٔ قبلی بررسی می‌کنیم که آیا بازطراحی یا متمرکزسازی کد لازم است.


## 9. Final status
**PARTIALLY COMPLETED.** Parameter consumption, snapshot truthfulness, fail-closed as-of selection and provenance are implemented and tested against the Stage 7 file; full PIT, D1–D6/R8 behavior, production integration, real-pytest/Stage 9/full-suite/CI verification remain open. Stage 7 is not frozen.