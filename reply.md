(analyzer) PS D:\Winprojects\analyzer> python src/scripts/excel_table_detector_review.py excel/cheshme.xlsx excel/fzar.xlsx excel/fzar2.xlsx excel/samanBank.xlsx excel/parsian_periodic.xlsx

## excel/cheshme.xlsx
- Reader result: **REJECTED** — text-only source contract violation.
- Source SHA-256: 75f8b499b7da397b330ea0f25b5e95062e3b76b9167e3e8d09db353dc0bac938
- Observed cells: 2153
- Text-only contract violations: **928 cells**
  - Worksheet 1: 928 cells
- Violation types:
  - UNEXPECTED_NON_TEXT / Excel data_type='n': 928
- First 12 example coordinates:
  - Sheet 1!B12: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]#,##0', value=1440000000
  - Sheet 1!C12: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]#,##0', value=1000
  - Sheet 1!D12: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]#,##0', value=1437377936
  - Sheet 1!E12: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]#,##0', value=5195175
  - Sheet 1!F12: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]#,##0', value=34942657
  - Sheet 1!G12: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]0', value=0
  - Sheet 1!H12: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]0', value=0
  - Sheet 1!I12: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]#,##0', value=6597565
  - Sheet 1!K12: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]#,##0', value=5195175
  - Sheet 1!L12: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]#,##0', value=41540222
  - Sheet 1!N12: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]#,##0', value=28900
  - Sheet 1!O12: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]#,##0', value=36345047
- Detector result: **DIAGNOSTIC PREVIEW ONLY**. The preview uses literal-text cells from a rejected workbook; it does not make the workbook eligible for ingestion.
- Tables/candidates in diagnostic preview: 9

### Worksheet 1: Recovered_Sheet1 (VISIBLE)
| Ordinal | Bounds | Status | Title evidence | Diagnostics |
|---:|---|---|---|---|
| 1 | A8:O25 | AMBIGUOUS | — | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 2 | A43:K63 | AMBIGUOUS | — | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 3 | A76:E81 | AMBIGUOUS | — | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 4 | A93:G97 | AMBIGUOUS | — | EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 5 | A106:K110 | AMBIGUOUS | — | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 6 | A129:G149 | AMBIGUOUS | — | EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 7 | A159:K164 | AMBIGUOUS | — | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 8 | A193:V214 | AMBIGUOUS | — | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR |
| 9 | A216:V221 | AMBIGUOUS | — | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR |

## excel/fzar.xlsx
- Reader result: **REJECTED** — text-only source contract violation.
- Source SHA-256: b8e1bd61d6f19a0d74f2243a9c4d5fa71945ebd0e0a3e1ad19834fc800abe3c7
- Observed cells: 953
- Text-only contract violations: **384 cells**
  - Worksheet 1: 384 cells
- Violation types:
  - UNEXPECTED_NON_TEXT / Excel data_type='n': 384
- First 12 example coordinates:
  - Sheet 1!C13: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]0', value=0
  - Sheet 1!D13: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]#,##0', value=2148
  - Sheet 1!E13: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]#,##0', value=17754190
  - Sheet 1!F13: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]#,##0', value=38136
  - Sheet 1!G13: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]0', value=0
  - Sheet 1!H13: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]0', value=0
  - Sheet 1!I13: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]0', value=0
  - Sheet 1!J13: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]0', value=0
  - Sheet 1!K13: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]#,##0', value=2148
  - Sheet 1!L13: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]#,##0', value=17754190
  - Sheet 1!M13: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]#,##0', value=38136
  - Sheet 1!N13: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]0', value=0
- Detector result: **DIAGNOSTIC PREVIEW ONLY**. The preview uses literal-text cells from a rejected workbook; it does not make the workbook eligible for ingestion.
- Tables/candidates in diagnostic preview: 4

### Worksheet 1: Recovered_Sheet1 (VISIBLE)
| Ordinal | Bounds | Status | Title evidence | Diagnostics |
|---:|---|---|---|---|
| 1 | A8:Z18 | AMBIGUOUS | — | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR |
| 2 | A29:T35 | AMBIGUOUS | — | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 3 | A40:X46 | AMBIGUOUS | — | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 4 | A48:W54 | AMBIGUOUS | — | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |

## excel/fzar2.xlsx
- Reader result: **REJECTED** — text-only source contract violation.
- Source SHA-256: 48272a0a5fe4635b9e7d877bf8748ae5a73cd3a025b1c055fd2ed582ac859a7f
- Observed cells: 6063
- Text-only contract violations: **2036 cells**
  - Worksheet 1: 2036 cells
- Violation types:
  - UNEXPECTED_NON_TEXT / Excel data_type='n': 2036
- First 12 example coordinates:
  - Sheet 1!B12: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]#,##0', value=48780966
  - Sheet 1!C12: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]#,##0', value=19317656
  - Sheet 1!D12: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]#,##0', value=53952825
  - Sheet 1!E12: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]0', value=153
  - Sheet 1!B13: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]#,##0', value=-3658393
  - Sheet 1!C13: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]#,##0', value=-1783279
  - Sheet 1!D13: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]#,##0', value=-5708798
  - Sheet 1!E13: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]0', value=-105
  - Sheet 1!B14: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]#,##0', value=45122573
  - Sheet 1!C14: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]#,##0', value=17534377
  - Sheet 1!D14: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]#,##0', value=48244027
  - Sheet 1!E14: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]0', value=157
- Detector result: **DIAGNOSTIC PREVIEW ONLY**. The preview uses literal-text cells from a rejected workbook; it does not make the workbook eligible for ingestion.
- Tables/candidates in diagnostic preview: 33

### Worksheet 1: Recovered_Sheet1 (VISIBLE)
| Ordinal | Bounds | Status | Title evidence | Diagnostics |
|---:|---|---|---|---|
| 1 | A8:E43 | AMBIGUOUS | — | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 2 | A59:E81 | AMBIGUOUS | — | EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 3 | A91:E111 | AMBIGUOUS | — | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 4 | A160:P207 | AMBIGUOUS | — | EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 5 | A216:E275 | AMBIGUOUS | — | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 6 | A289:E318 | AMBIGUOUS | — | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 7 | A334:E351 | AMBIGUOUS | — | EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 8 | A361:E380 | AMBIGUOUS | — | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 9 | A425:L460 | AMBIGUOUS | — | EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 10 | A469:E519 | AMBIGUOUS | — | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 11 | A533:V543 | AMBIGUOUS | — | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 12 | A551:H562 | AMBIGUOUS | — | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 13 | A564:D582 | AMBIGUOUS | نرخ فروش کانسنگ بر اساس قرارداد فی ما بین با شرکت استحصال مواد معدنی تخت سلیمان (شرکت تابعه) و بر اساس قیمت جهانی طلا و دلار تعیین می گردد.  | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 14 | A593:Q601 | AMBIGUOUS | — | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 15 | A603:Q611 | AMBIGUOUS | — | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 16 | A619:N624 | AMBIGUOUS | — | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 17 | A629:N636 | AMBIGUOUS | — | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 18 | A655:C656 | AMBIGUOUS | — | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 19 | A667:G681 | AMBIGUOUS | — | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 20 | A683:B685 | AMBIGUOUS | — | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 21 | A687:K696 | AMBIGUOUS | انتظار می رود هزینه های عمومی ، اداری و تشکیلاتی شرکت متناسب با نرخ تورم و افزایش حجم فعالیت های شرکت رشد یابد.  | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 22 | A706:P715 | AMBIGUOUS | — | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 23 | A717:O726 | AMBIGUOUS | — | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 24 | A735:D740 | AMBIGUOUS | — | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 25 | A742:K753 | AMBIGUOUS | — | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 26 | A755:K765 | AMBIGUOUS | — | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 27 | A783:D794 | AMBIGUOUS | — | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 28 | A796:D805 | AMBIGUOUS | — | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 29 | A807:E810 | AMBIGUOUS | — | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 30 | A812:B813 | AMBIGUOUS | — | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 31 | A830:K836 | AMBIGUOUS | — | EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 32 | A849:M851 | AMBIGUOUS | — | EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 33 | A868:M870 | AMBIGUOUS | — | EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |

## excel/samanBank.xlsx
- Reader result: **REJECTED** — text-only source contract violation.
- Source SHA-256: 454985ba50ada23ee08ef7560ae1b892762b58b08375400f9536d797987cb4b5
- Observed cells: 2753
- Text-only contract violations: **914 cells**
  - Worksheet 1: 914 cells
- Violation types:
  - UNEXPECTED_NON_TEXT / Excel data_type='n': 914
- First 12 example coordinates:
  - Sheet 1!B13: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]0', value=0
  - Sheet 1!C13: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]0', value=0
  - Sheet 1!D13: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]0', value=0
  - Sheet 1!E13: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]0', value=0
  - Sheet 1!F13: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]0', value=0
  - Sheet 1!G13: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]0', value=0
  - Sheet 1!H13: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]0', value=0
  - Sheet 1!I13: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]0', value=0
  - Sheet 1!J13: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]0', value=0
  - Sheet 1!K13: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]0', value=0
  - Sheet 1!B14: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]#,##0', value=3893946956
  - Sheet 1!C14: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]#,##0', value=5269432573
- Detector result: **DIAGNOSTIC PREVIEW ONLY**. The preview uses literal-text cells from a rejected workbook; it does not make the workbook eligible for ingestion.
- Tables/candidates in diagnostic preview: 16

### Worksheet 1: Recovered_Sheet1 (VISIBLE)
| Ordinal | Bounds | Status | Title evidence | Diagnostics |
|---:|---|---|---|---|
| 1 | A8:K29 | AMBIGUOUS | — | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 2 | A37:F58 | AMBIGUOUS | دوره ۶ ماهه منتهي به ۱۴۰۵/۱۲/۲۹ ; افزایش در ذخیره مطالبات مشکوک الوصول ناشی از افزایش ذخیره عام که تابعی از میزان تسهیلات اعطایی طی سال ۱۴۰۵ و میزان مطالبات ایجاد شده خواهد بود.  | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 3 | A67:F112 | AMBIGUOUS | — | EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 4 | A121:J139 | AMBIGUOUS | — | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 5 | A150:C153 | AMBIGUOUS | دوره ۶ ماهه منتهي به ۱۴۰۵/۱۲/۲۹  | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 6 | A159:C164 | AMBIGUOUS | دوره ۶ ماهه منتهي به ۱۴۰۵/۱۲/۲۹  | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 7 | A170:C178 | AMBIGUOUS | دوره ۶ ماهه منتهي به ۱۴۰۵/۱۲/۲۹  | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 8 | A180:E181 | AMBIGUOUS | دوره ۶ ماهه منتهي به ۱۴۰۵/۱۲/۲۹  | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 9 | A183:B184 | AMBIGUOUS | — | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 10 | A197:D233 | AMBIGUOUS | — | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 11 | A249:D259 | AMBIGUOUS | — | EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 12 | A268:E312 | AMBIGUOUS | — | EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 13 | A321:L369 | AMBIGUOUS | — | EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 14 | A378:D421 | AMBIGUOUS | — | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 15 | A441:M466 | CANDIDATE | — | — |
| 16 | A483:M485 | CANDIDATE | — | — |

## excel/parsian_periodic.xlsx
- Reader result: **REJECTED** — text-only source contract violation.
- Source SHA-256: b5623964d336dd679eaa8208fb800fdbf24351ff85bc996e05210b37f342e6da
- Observed cells: 2183
- Text-only contract violations: **920 cells**
  - Worksheet 1: 900 cells
  - Worksheet 2: 20 cells
- Violation types:
  - UNEXPECTED_NON_TEXT / Excel data_type='n': 920
- First 12 example coordinates:
  - Sheet 1!B13: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]#,##0', value=147186330
  - Sheet 1!C13: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]#,##0', value=87074365
  - Sheet 1!D13: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]#,##0', value=229849193
  - Sheet 1!E13: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]0', value=69
  - Sheet 1!B14: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]#,##0', value=-230307149
  - Sheet 1!C14: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]#,##0', value=-157273597
  - Sheet 1!D14: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]#,##0', value=-345542486
  - Sheet 1!E14: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]0', value=-46
  - Sheet 1!B15: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]#,##0', value=-83120819
  - Sheet 1!C15: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]#,##0', value=-70199232
  - Sheet 1!D15: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]#,##0', value=-115693293
  - Sheet 1!E15: kind=UNEXPECTED_NON_TEXT, data_type='n', number_format='[$-3000401]0', value=-18
- Detector result: **DIAGNOSTIC PREVIEW ONLY**. The preview uses literal-text cells from a rejected workbook; it does not make the workbook eligible for ingestion.
- Tables/candidates in diagnostic preview: 15

### Worksheet 1: Recovered_Sheet1 (VISIBLE)
| Ordinal | Bounds | Status | Title evidence | Diagnostics |
|---:|---|---|---|---|
| 1 | A8:E42 | AMBIGUOUS | — | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 2 | A58:E68 | AMBIGUOUS | — | EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 3 | A77:E119 | AMBIGUOUS | — | EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 4 | A128:L165 | CANDIDATE | — | — |
| 5 | A174:E213 | AMBIGUOUS | — | EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 6 | A235:K256 | AMBIGUOUS | — | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR |
| 7 | A264:F285 | AMBIGUOUS | دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ; با توجه به افزایش در حجم تسهیلات اعطایی پیش بینی می گردد مانده ذخیره مطالبات مشکوک الوصول عام افزایش و بر اساس روند وصول مطالبات ذخیره مطالبات مشکوک الوصول خاص تغییری نداشته باشد.  | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 8 | A294:F341 | AMBIGUOUS | — | EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 9 | A350:J363 | AMBIGUOUS | — | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 10 | A374:C378 | AMBIGUOUS | دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ; ---------------------------------------------------------------------------  | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 11 | A384:C387 | AMBIGUOUS | دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ; --------------------------------------------------------------------------------  | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 12 | A393:C401 | AMBIGUOUS | دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ; --------------------------------------------------------------------------------  | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 13 | A403:E404 | AMBIGUOUS | دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ; ----------------------------------------------------------------------------------------  | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |
| 14 | A406:B407 | AMBIGUOUS | — | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR; EXCEL_TABLE_BOUNDARY_CROSSED_BY_MERGE |

### Worksheet 2: Sheet1 (VISIBLE)
| Ordinal | Bounds | Status | Title evidence | Diagnostics |
|---:|---|---|---|---|
| 1 | A14:E24 | AMBIGUOUS | — | EXCEL_TABLE_SINGLE_BLANK_SEPARATOR |