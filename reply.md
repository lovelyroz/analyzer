# Migration 9 Column Usage Audit
Database: D:\winprojects\analyzer\tehran_stock.db

## source_sheet
Total rows: 505
Non-null rows: 505
Distinct non-null values: 1
Sample values:
- 'Recovered_Sheet1'

## source_column_header
Total rows: 505
Non-null rows: 505
Distinct non-null values: 23
Sample values:
- 'دوره منتهي به ۱۴۰۵/۰۳/۳۱ | حسابرسی شده'
- 'به تاريخ ۱۴۰۵/۰۳/۳۱ | حسابرسی شده'
- 'دوره ۶ ماهه منتهی به ۱۴۰۵/۰۳/۳۱ | تعداد تولید'
- 'دوره ۶ ماهه منتهی به ۱۴۰۵/۰۳/۳۱ | تعداد فروش'
- 'دوره ۶ ماهه منتهی به ۱۴۰۵/۰۳/۳۱ | مبلغ فروش'
- 'دوره ۶ ماهه منتهی به ۱۴۰۵/۰۳/۳۱ | مبلغ بهای تمام شده'
- 'دوره ۶ ماهه منتهی به ۱۴۰۵/۰۳/۳۱ | سود ناخالص'
- 'دوره ۶ ماهه منتهی به ۱۴۰۵/۰۳/۳۱ | نرخ فروش'
- 'سال مالی ۱۴۰۵/۰۳/۳۱'
- 'دوره ۶ ماهه منتهی به ۱۴۰۵/۰۳/۳۱ (میلیون ریال)'
- 'دوره ۶ ماهه منتهی به ۱۴۰۵/۰۳/۳۱'
- 'دوره ۶ ماهه منتهی به ۱۴۰۵/۰۳/۳۱ | موجودي اول دوره'
- 'دوره ۶ ماهه منتهی به ۱۴۰۵/۰۳/۳۱ | خريد طي دوره'
- 'دوره ۶ ماهه منتهي به ۱۴۰۵/۰۳/۳۱ | نرخ ميانگين تسعير ارز'
- 'دوره ۶ ماهه منتهي به ۱۴۰۵/۰۳/۳۱ | مبلغ ارزي'
- 'دوره ۶ ماهه منتهي به ۱۴۰۵/۰۳/۳۱ | مبلغ ريالي-ميليون ريال'
- 'دوره یک ماهه منتهی به ۱۴۰۵/۰۷/۳۰ | تعداد تولید'
- 'دوره یک ماهه منتهی به ۱۴۰۵/۰۷/۳۰ | تعداد فروش'
- 'دوره یک ماهه منتهی به ۱۴۰۵/۰۷/۳۰ | مبلغ فروش (میلیون ریال)'
- 'دوره یک ماهه منتهی به ۱۴۰۵/۰۷/۳۰ | نرخ فروش (ریال)'

## Source Code References
src\scripts\audit_migration_9_column_usage.py:28: targets = ["source_sheet", "source_column_header"]
src\scripts\audit_migration_9_column_usage.py:85: for name in ["source_sheet", "source_column_header"]
src\scripts\audit_migration_9_recovery.py:10: "source_sheet",
src\scripts\audit_migration_9_recovery.py:11: "source_column_header",