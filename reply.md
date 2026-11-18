# Legacy RawFinancialFact Provenance Audit

- Database: `D:\winprojects\analyzer\tehran_stock.db`
- Mode: read-only

## 1. Raw fact population

- Total raw_financial_facts rows: **505**

## 2. Provenance field population

| Field | Exists | Non-null | Distinct non-null |
|---|---:|---:|---:|
| `source_sheet` | Yes | 505 | 1 |
| `source_column_header` | Yes | 505 | 23 |
| `source_section` | Yes | 245 | 9 |
| `source_row` | Yes | 505 | 336 |
| `source_column` | Yes | 505 | 15 |

## 3. Distinct-value samples

### `source_sheet`

- `Recovered_Sheet1`

### `source_column_header`

- `به تاريخ ۱۴۰۵/۰۳/۳۱ | حسابرسی شده`
- `خرید دوره یک ماهه منتهی به ۱۴۰۵/۰۷/۳۰ | مبلغ (میلیون ریال)`
- `خرید دوره یک ماهه منتهی به ۱۴۰۵/۰۷/۳۰ | مقدار`
- `خرید دوره یک ماهه منتهی به ۱۴۰۵/۰۷/۳۰ | نرخ (ريال)`
- `دوره منتهي به ۱۴۰۵/۰۳/۳۱ | حسابرسی شده`
- `دوره یک ماهه منتهی به ۱۴۰۵/۰۷/۳۰ | تعداد تولید`
- `دوره یک ماهه منتهی به ۱۴۰۵/۰۷/۳۰ | تعداد فروش`
- `دوره یک ماهه منتهی به ۱۴۰۵/۰۷/۳۰ | مبلغ فروش (میلیون ریال)`
- `دوره یک ماهه منتهی به ۱۴۰۵/۰۷/۳۰ | نرخ فروش (ریال)`
- `دوره ۶ ماهه منتهي به ۱۴۰۵/۰۳/۳۱ | مبلغ ارزي`
- `دوره ۶ ماهه منتهي به ۱۴۰۵/۰۳/۳۱ | مبلغ ريالي-ميليون ريال`
- `دوره ۶ ماهه منتهي به ۱۴۰۵/۰۳/۳۱ | نرخ ميانگين تسعير ارز`
- `دوره ۶ ماهه منتهی به ۱۴۰۵/۰۳/۳۱`
- `دوره ۶ ماهه منتهی به ۱۴۰۵/۰۳/۳۱ (میلیون ریال)`
- `دوره ۶ ماهه منتهی به ۱۴۰۵/۰۳/۳۱ | تعداد تولید`
- `دوره ۶ ماهه منتهی به ۱۴۰۵/۰۳/۳۱ | تعداد فروش`
- `دوره ۶ ماهه منتهی به ۱۴۰۵/۰۳/۳۱ | خريد طي دوره`
- `دوره ۶ ماهه منتهی به ۱۴۰۵/۰۳/۳۱ | سود ناخالص`
- `دوره ۶ ماهه منتهی به ۱۴۰۵/۰۳/۳۱ | مبلغ بهای تمام شده`
- `دوره ۶ ماهه منتهی به ۱۴۰۵/۰۳/۳۱ | مبلغ فروش`
- `دوره ۶ ماهه منتهی به ۱۴۰۵/۰۳/۳۱ | موجودي اول دوره`
- `دوره ۶ ماهه منتهی به ۱۴۰۵/۰۳/۳۱ | نرخ فروش`
- `سال مالی ۱۴۰۵/۰۳/۳۱`

### `source_section`

- `شرکت در صورت نیاز به تامین مالی نسبت به اخذ تسهیلات مالی اقدام خواهد کرد.`
- `صورت جريان هاي نقدي تلفيقي`
- `صورت جريان‌هاي نقدي`
- `صورت سود و زيان`
- `صورت سود و زيان تلفيقي`
- `صورت سود و زيان جامع`
- `صورت سود و زيان جامع تلفيقي`
- `صورت وضعيت مالي`
- `صورت وضعيت مالي تلفيقي`

### `source_row`

- `12`
- `13`
- `14`
- `15`
- `16`
- `17`
- `18`
- `19`
- `20`
- `21`
- `22`
- `23`
- `24`
- `25`
- `26`
- `27`
- `28`
- `29`
- `30`
- `31`
- `32`
- `34`
- `35`
- `37`
- `38`
- `39`
- `40`
- `41`
- `42`
- `43`

### `source_column`

- `B`
- `C`
- `D`
- `E`
- `F`
- `G`
- `H`
- `K`
- `L`
- `M`
- `N`
- `O`
- `P`
- `Q`
- `R`

## 4. Foreign-key references to raw_financial_facts

| Referencing table | Column | Target | ON DELETE |
|---|---|---|---|
| `mapping_decisions` | `raw_fact_id` | `raw_fact_id` | `NO ACTION` |
| `normalized_financial_fact_inputs` | `raw_fact_id` | `raw_fact_id` | `NO ACTION` |
| `normalized_financial_facts` | `raw_fact_id` | `raw_fact_id` | `NO ACTION` |

## 5. Application source references

### `source_sheet`

- No references found under `src` outside `src/scripts`.

### `source_column_header`

- No references found under `src` outside `src/scripts`.

### `source_section`

- `src\ingestion\service.py:49`: `source_section: Optional[str] = None`
- `src\ingestion\service.py:238`: `source_section=_ascii_text(line.source_section),`
- `src\models\normalized.py:35`: `source_section = Column(String(150), nullable=True)`
- `src\tests\test_codal_extraction.py:153`: `assert all(r.source_section for r in result.raw_lines)`
- `src\tests\test_codal_extraction.py:414`: `assert all(r.source_section for r in result.raw_lines)`
- `src\tests\test_codal_pdf_extraction.py:160`: `line.source_section,`
- `src\tests\test_codal_pdf_extraction.py:346`: `source_section="بخش ۹", source_column="ستون ۱۰", value=Decimal("123.45"),`
- `src\tests\test_codal_pdf_extraction.py:360`: `assert fact.source_section == "بخش 9"`
- `src\tests\test_codal_pdf_extraction.py:430`: `assert not contains_non_ascii_digit(fact.source_section)`
- `src\tests\test_codal_pdf_extraction.py:492`: `fact.source_section,`
- `src\tests\test_codal_pdf_extraction.py:606`: `fact.source_section,`
- `src\tests\test_stage1_rules.py:97`: `source_section="Income Statement", source_row=12, source_column="D",`
- `src\tests\test_stage1_rules.py:104`: `assert saved.source_section == "Income Statement"`
- `src\ingestion\codal\adapter.py:93`: `source_section=_ascii_text(cell.source_section),`
- `src\ingestion\codal\adapter.py:103`: `(r.source_section or "").endswith("_table") for r in cell_rows`
- `src\ingestion\codal\pdf_extract.py:32`: `source_section: Optional[str]`
- `src\ingestion\codal\pdf_extract.py:193`: `source_section=section,`
- `src\ingestion\codal\pdf_extract.py:282`: `source_section=section,`

### `source_row`

- `src\ingestion\service.py:50`: `source_row: Optional[int] = None`
- `src\ingestion\service.py:239`: `source_row=line.source_row,`
- `src\models\normalized.py:36`: `source_row = Column(Integer, nullable=True)`
- `src\tests\test_codal_pdf_extraction.py:130`: `assert all(line.source_row is not None for line in lines)`
- `src\tests\test_codal_pdf_extraction.py:161`: `line.source_row,`
- `src\tests\test_codal_pdf_extraction.py:225`: `assert all(line.source_row is not None for line in result.raw_lines)`
- `src\tests\test_codal_pdf_extraction.py:493`: `fact.source_row,`
- `src\tests\test_codal_pdf_extraction.py:618`: `assert fact.source_row is None or isinstance(fact.source_row, int)`
- `src\tests\test_stage1_rules.py:97`: `source_section="Income Statement", source_row=12, source_column="D",`
- `src\tests\test_stage1_rules.py:105`: `assert saved.source_row == 12`
- `src\ingestion\codal\adapter.py:82`: `warnings.append(f"page {cell.page} row {cell.source_row}: empty item name skipped")`
- `src\ingestion\codal\adapter.py:94`: `source_row=cell.source_row,`
- `src\ingestion\codal\parser.py:98`: `source_row=row_number,`
- `src\ingestion\codal\pdf_extract.py:33`: `source_row: Optional[int]`
- `src\ingestion\codal\pdf_extract.py:194`: `source_row=r_i + 1,`
- `src\ingestion\codal\pdf_extract.py:283`: `source_row=line_no,`

### `source_column`

- `src\ingestion\service.py:51`: `source_column: Optional[str] = None`
- `src\ingestion\service.py:240`: `source_column=_ascii_text(line.source_column),`
- `src\models\normalized.py:37`: `source_column = Column(String(100), nullable=True)`
- `src\tests\test_codal_pdf_extraction.py:129`: `assert [line.source_column for line in lines] == ["1", "2", "3"]`
- `src\tests\test_codal_pdf_extraction.py:148`: `assert [row.source_column for row in rows] == ["1", "2", "3"]`
- `src\tests\test_codal_pdf_extraction.py:162`: `line.source_column,`
- `src\tests\test_codal_pdf_extraction.py:315`: `RawLineInput(item_name="absent amount", value=None, source_column="1"),`
- `src\tests\test_codal_pdf_extraction.py:316`: `RawLineInput(item_name="explicit zero", value=Decimal("0"), source_column="2"),`
- `src\tests\test_codal_pdf_extraction.py:346`: `source_section="بخش ۹", source_column="ستون ۱۰", value=Decimal("123.45"),`
- `src\tests\test_codal_pdf_extraction.py:361`: `assert fact.source_column == "ستون 10"`
- `src\tests\test_codal_pdf_extraction.py:431`: `assert not contains_non_ascii_digit(fact.source_column)`
- `src\tests\test_codal_pdf_extraction.py:494`: `fact.source_column,`
- `src\tests\test_codal_pdf_extraction.py:607`: `fact.source_column,`
- `src\tests\test_stage1_rules.py:97`: `source_section="Income Statement", source_row=12, source_column="D",`
- `src\tests\test_stage1_rules.py:106`: `assert saved.source_column == "D"`
- `src\ingestion\codal\adapter.py:95`: `source_column=_ascii_text(cell.source_column),`
- `src\ingestion\codal\parser.py:99`: `source_column=str(column_number),`
- `src\ingestion\codal\pdf_extract.py:34`: `source_column: Optional[str]`
- `src\ingestion\codal\pdf_extract.py:195`: `source_column=col_label,`
- `src\ingestion\codal\pdf_extract.py:284`: `source_column=str(column_number),`

## 6. Interpretation boundary

- This report measures legacy data population and source references only.
- It does not decide which fields belong in the future canonical schema.
- Do not drop or rewrite any field based on this report alone.
- Migration 9 source/revision reconciliation remains a separate issue.
