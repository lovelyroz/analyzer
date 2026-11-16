# Parsian Periodic workbook annotation audit

Workbook: `excel/parsian_periodic.xlsx`

## 1. Executive summary

- Worksheets inspected: 2.
- Red names on `Recovered_Sheet1`: 17; extra red duplicate sample on `Sheet1`: 1.
- Main red-name candidates: 17; extra unmarked candidate `Recovered_Sheet1!A297:D299`; duplicate sample `Sheet1!A16:E24`.
- Explicit `thick` border sides: 0. Zero candidates meet the exact Thick Outside Border rule; the listed rectangles are medium-border candidates only.
- Green 16; blue 108; yellow 178; gray 459; black/dark excluded 489.

## 2. Workbook and worksheet overview

| Worksheet | Used range | rightToLeft | Merged ranges | Red names |
|---|---|---:|---:|---:|
| Recovered_Sheet1 | A1:L411 | True | 101 | 17 |
| Sheet1 | A1:E24 | None | 2 | 1 |

### Recovered_Sheet1 merged ranges

`A48:E48`, `E79:E80`, `C262:I262`, `A45:E45`, `E10:E11`, `A285:I285`, `F320:G320`, `F329:G329`, `A355:B355`, `F326:G326`, `A46:E46`, `D306:E306`, `B310:G310`, `A411:I411`, `F321:G321`, `F315:G315`, `A294:K294`, `F318:G318`, `J353:K354`, `A259:B259`, `F266:F267`, `D307:E307`, `F332:G332`, `A262:B262`, `A333:B333`, `B266:C266`, `F313:G313`, `A401:B401`, `A79:A80`, `D305:E305`, `A222:E222`, `J358:K358`, `A49:E49`, `F319:G319`, `F322:G322`, `D337:E337`, `C353:F353`, `D276:J276`, `D339:E339`, `F317:G317`, `C256:I256`, `A10:A11`, `C382:F382`, `J356:K356`, `F323:G323`, `F239:G239`, `H239:I239`, `A391:B391`, `D302:E302`, `A226:E226`, `A350:K350`, `E60:E61`, `C391:F391`, `G353:I353`, `A256:B256`, `A221:E221`, `F325:G325`, `A238:A239`, `A356:B356`, `A223:E223`, `E176:E177`, `C259:I259`, `F327:G327`, `A353:B354`, `D336:E336`, `A235:K235`, `C333:I333`, `A47:E47`, `J239:K239`, `D304:E304`, `B239:C239`, `A224:E224`, `B284:F284`, `A372:B372`, `D303:E303`, `B407:E407`, `A382:B382`, `A44:E44`, `A410:I410`, `A60:A61`, `A358:B358`, `F314:G314`, `A225:E225`, `D338:E338`, `F316:G316`, `D239:E239`, `D266:E266`, `F331:G331`, `D340:E340`, `F330:G330`, `F324:G324`, `D308:E308`, `C372:F372`, `J355:K355`, `C401:F401`, `J357:K357`, `A341:G341`, `A357:B357`, `A266:A267`, `F328:G328`, `A176:A177`

### Sheet1 merged ranges

`A16:A17`, `E16:E17`

## 3. Global color and border inventory

| Role/shade | Exact fill metadata | Recovered_Sheet1 | Sheet1 | Total |
|---|---|---:|---:|---:|
| Red main name | `{"fill_type": "solid", "color_type": "rgb", "rgb": "FFFF0000", "theme": null, "indexed": null, "tint": 0.0}` | 17 | 1 | 18 |
| Blue RGB FF0197C8 | `{"fill_type": "solid", "color_type": "rgb", "rgb": "FF0197C8", "theme": null, "indexed": null, "tint": 0.0}` | 96 | 8 | 104 |
| Blue RGB FF0070C0 | `{"fill_type": "solid", "color_type": "rgb", "rgb": "FF0070C0", "theme": null, "indexed": null, "tint": 0.0}` | 4 | 0 | 4 |
| Yellow RGB FFFFFF00 | `{"fill_type": "solid", "color_type": "rgb", "rgb": "FFFFFF00", "theme": null, "indexed": null, "tint": 0.0}` | 178 | 0 | 178 |
| Gray theme0 tint -0.249977111117893 | `{"fill_type": "solid", "color_type": "theme", "rgb": null, "theme": 0, "indexed": null, "tint": -0.249977111117893}` | 459 | 0 | 459 |
| Black theme1 tint 0 | `{"fill_type": "solid", "color_type": "theme", "rgb": null, "theme": 1, "indexed": null, "tint": 0.0}` | 237 | 0 | 237 |
| Dark theme1 tint 0.0499893185216834 | `{"fill_type": "solid", "color_type": "theme", "rgb": null, "theme": 1, "indexed": null, "tint": 0.0499893185216834}` | 252 | 0 | 252 |
| Green RGB FF00B050 | `{"fill_type": "solid", "color_type": "rgb", "rgb": "FF00B050", "theme": null, "indexed": null, "tint": 0.0}` | 15 | 1 | 16 |

| Border side | Style | Side count |
|---|---|---:|
| bottom | medium | 1698 |
| bottom | thin | 201 |
| left | medium | 1298 |
| left | thin | 8 |
| right | medium | 1577 |
| right | thin | 6 |
| top | medium | 1653 |
| top | thin | 9 |

Thick-side coordinates: `[]`.

## 4. Table inventory

| Seq | Worksheet | Candidate range | Red name | Distance | Edge styles/gaps | Merges |
|---:|---|---|---|---:|---|---:|
| 1 | Recovered_Sheet1 | A10:E42 | A8 | 2 | top 0 gap(s), {"medium": 5}; bottom 0 gap(s), {"medium": 5}; left 0 gap(s), {"medium": 33}; right 0 gap(s), {"medium": 33} | 2 |
| 2 | Recovered_Sheet1 | A60:E68 | A58 | 2 | top 0 gap(s), {"medium": 5}; bottom 0 gap(s), {"medium": 4, "thin": 1}; left 0 gap(s), {"medium": 9}; right 0 gap(s), {"medium": 9} | 2 |
| 3 | Recovered_Sheet1 | A79:E119 | A77 | 2 | top 1 gap(s), {"medium": 4, "null": 1}; bottom 1 gap(s), {"medium": 4, "null": 1}; left 0 gap(s), {"medium": 41}; right 0 gap(s), {"medium": 41} | 2 |
| 4 | Recovered_Sheet1 | A130:L165 | A128 | 2 | top 0 gap(s), {"medium": 12}; bottom 0 gap(s), {"medium": 12}; left 0 gap(s), {"medium": 36}; right 0 gap(s), {"medium": 36} | 0 |
| 5 | Recovered_Sheet1 | A176:E213 | A174 | 2 | top 0 gap(s), {"medium": 5}; bottom 0 gap(s), {"medium": 5}; left 0 gap(s), {"medium": 38}; right 0 gap(s), {"medium": 38} | 2 |
| 6 | Recovered_Sheet1 | A238:K254 | A236 | 2 | top 0 gap(s), {"medium": 11}; bottom 0 gap(s), {"medium": 11}; left 0 gap(s), {"medium": 17}; right 0 gap(s), {"medium": 17} | 6 |
| 7 | Recovered_Sheet1 | A266:F275 | A264 | 2 | top 0 gap(s), {"medium": 6}; bottom 0 gap(s), {"medium": 6}; left 0 gap(s), {"medium": 10}; right 0 gap(s), {"medium": 10} | 4 |
| 8 | Recovered_Sheet1 | A279:F284 | A277 | 2 | top 0 gap(s), {"medium": 6}; bottom 0 gap(s), {"medium": 6}; left 0 gap(s), {"medium": 6}; right 0 gap(s), {"medium": 6} | 1 |
| 9 | Recovered_Sheet1 | A302:E308 | A300 | 2 | top 0 gap(s), {"medium": 5}; bottom 0 gap(s), {"medium": 5}; left 0 gap(s), {"medium": 7}; right 0 gap(s), {"medium": 7} | 7 |
| 10 | Recovered_Sheet1 | A313:G332 | A311 | 2 | top 0 gap(s), {"medium": 7}; bottom 0 gap(s), {"medium": 7}; left 0 gap(s), {"medium": 20}; right 0 gap(s), {"medium": 20} | 20 |
| 11 | Recovered_Sheet1 | A336:E340 | A334 | 2 | top 0 gap(s), {"medium": 5}; bottom 0 gap(s), {"medium": 5}; left 0 gap(s), {"medium": 5}; right 0 gap(s), {"medium": 5} | 5 |
| 12 | Recovered_Sheet1 | A353:K358 | A351 | 2 | top 0 gap(s), {"medium": 11}; bottom 0 gap(s), {"medium": 11}; left 0 gap(s), {"medium": 6}; right 0 gap(s), {"medium": 6} | 12 |
| 13 | Recovered_Sheet1 | A361:C367 | A359 | 2 | top 0 gap(s), {"medium": 3}; bottom 0 gap(s), {"medium": 3}; left 0 gap(s), {"medium": 7}; right 0 gap(s), {"medium": 7} | 0 |
| 14 | Recovered_Sheet1 | A376:C378 | A374 | 2 | top 0 gap(s), {"medium": 3}; bottom 0 gap(s), {"medium": 3}; left 0 gap(s), {"medium": 3}; right 0 gap(s), {"medium": 3} | 0 |
| 15 | Recovered_Sheet1 | A386:C387 | A384 | 2 | top 0 gap(s), {"medium": 3}; bottom 0 gap(s), {"medium": 3}; left 0 gap(s), {"medium": 2}; right 0 gap(s), {"medium": 2} | 0 |
| 16 | Recovered_Sheet1 | A395:C399 | A393 | 2 | top 0 gap(s), {"thin": 3}; bottom 0 gap(s), {"medium": 3}; left 0 gap(s), {"thin": 4, "medium": 1}; right 0 gap(s), {"thin": 4, "medium": 1} | 0 |
| 17 | Recovered_Sheet1 | A404:E405 | A403 | 1 | top 0 gap(s), {"thin": 5}; bottom 0 gap(s), {"thin": 5}; left 0 gap(s), {"thin": 2}; right 0 gap(s), {"thin": 2} | 0 |
| 18 | Sheet1 | A16:E24 | A14 | 2 | top 0 gap(s), {"medium": 5}; bottom 0 gap(s), {"medium": 5}; left 0 gap(s), {"medium": 9}; right 0 gap(s), {"medium": 9} | 2 |
| 19 | Recovered_Sheet1 | A297:D299 | none | ? | top 0 gap(s), {"medium": 4}; bottom 0 gap(s), {"medium": 4}; left 0 gap(s), {"medium": 3}; right 0 gap(s), {"medium": 3} | 0 |

## 5. Detailed report for each candidate

Values are JSON-quoted; gray values retain the observed value and Excel data type. Black/dark cells are excluded from extraction. Columns are physical Excel positions.

### Candidate 01: Recovered_Sheet1!A10:E42

- Bounds A10 through E42; 33 rows ? 5 columns.
- Red name A8 = "صورت سود و زیان"; distance 2 row(s); fill `{"fill_type": "solid", "color_type": "rgb", "rgb": "FFFF0000", "theme": null, "indexed": null, "tint": 0.0}`.
- Thick outline not confirmed; medium edge properties `{"top": {"styles": {"medium": 5}, "gaps": 0}, "bottom": {"styles": {"medium": 5}, "gaps": 0}, "left": {"styles": {"medium": 33}, "gaps": 0}, "right": {"styles": {"medium": 33}, "gaps": 0}}`.
- Merged ranges: `E10:E11`, `A10:A11`.
- Blue header cells 6 on rows [10, 11]:
  - A10 = "شرح" (blue1)
  - B10 = "دوره منتهي به ۱۴۰۳/۰۶/۳۱" (blue1)
  - D10 = "تجدید ارائه شده ۱۴۰۲/۱۲/۲۹" (blue1)
  - E10 = "درصد تغييرات" (blue1)
  - B11 = "حسابرسی نشده" (blue1)
  - D11 = "حسابرسی شده" (blue1)
- Merged header ranges `["E10:E11", "A10:A11"]`.
- Yellow description/label cells 28:
  - A13 = "درآمد تسهيلات اعطايي و سپرده گذاری و اوراق بدهی "
  - A14 = "هزينه سود سپرده‌ها "
  - A15 = "خالص درآمد تسهیلات و سپرده گذاری "
  - A16 = "درآمد کارمزد "
  - A17 = "هزينه کارمزد "
  - A18 = "خالص درآمد کارمزد "
  - A19 = "خالص سود (زیان) سرمایه گذاری‌ها "
  - A20 = "خالص سود (زيان) مبادلات و معاملات ارزي "
  - A21 = "ساير درآمدها و هزینه های عملياتي "
  - A22 = "جمع درآمدهاي عملياتي "
  - A23 = "خالص ساير درآمدها و هزینه‌ها "
  - A24 = "هزينه‌هاي اداري و عمومي "
  - A25 = "هزينه مطالبات مشکوک الوصول "
  - A26 = "هزينه‌هاي مالي "
  - A27 = "هزينه استهلاک "
  - A28 = "سود(زیان) عملیات در حال تداوم قبل از مالیات "
  - A29 = "ماليات بر درآمد سال جاری "
  - A30 = "ماليات بر درآمد سال های قبل "
  - A31 = "سود (زيان) خالص عملیات در حال تداوم "
  - A33 = "سود(زیان) خالص عملیات متوقف شده "
  - A34 = "سود(زیان) خالص "
  - A36 = "عملياتي (ريال) "
  - A37 = "غيرعملياتي(ريال) "
  - A38 = "ناشی از عملیات در حال تداوم(ریال) "
  - A39 = "ناشي از عمليات متوقف شده(ريال) "
  - A40 = "سود(زیان) پایه هر سهم (ریال) "
  - A41 = "سود (زیان) خالص هر سهم– ریال "
  - A42 = "سرمایه "
- Gray value cells 56 with same-row yellow label(s):
  - B13 = 147186330 (type n; label A13 "درآمد تسهيلات اعطايي و سپرده گذاری و اوراق بدهی ")
  - D13 = 229849193 (type n; label A13 "درآمد تسهيلات اعطايي و سپرده گذاری و اوراق بدهی ")
  - B14 = -230307149 (type n; label A14 "هزينه سود سپرده‌ها ")
  - D14 = -345542486 (type n; label A14 "هزينه سود سپرده‌ها ")
  - B15 = -83120819 (type n; label A15 "خالص درآمد تسهیلات و سپرده گذاری ")
  - D15 = -115693293 (type n; label A15 "خالص درآمد تسهیلات و سپرده گذاری ")
  - B16 = 24646669 (type n; label A16 "درآمد کارمزد ")
  - D16 = 43403722 (type n; label A16 "درآمد کارمزد ")
  - B17 = -8624760 (type n; label A17 "هزينه کارمزد ")
  - D17 = -10854204 (type n; label A17 "هزينه کارمزد ")
  - B18 = 16021909 (type n; label A18 "خالص درآمد کارمزد ")
  - D18 = 32549518 (type n; label A18 "خالص درآمد کارمزد ")
  - B19 = 402420 (type n; label A19 "خالص سود (زیان) سرمایه گذاری‌ها ")
  - D19 = 2453194 (type n; label A19 "خالص سود (زیان) سرمایه گذاری‌ها ")
  - B20 = 2072623 (type n; label A20 "خالص سود (زيان) مبادلات و معاملات ارزي ")
  - D20 = 3775645 (type n; label A20 "خالص سود (زيان) مبادلات و معاملات ارزي ")
  - B21 = 84513662 (type n; label A21 "ساير درآمدها و هزینه های عملياتي ")
  - D21 = 151543669 (type n; label A21 "ساير درآمدها و هزینه های عملياتي ")
  - B22 = 19889795 (type n; label A22 "جمع درآمدهاي عملياتي ")
  - D22 = 74628733 (type n; label A22 "جمع درآمدهاي عملياتي ")
  - B23 = 2192360 (type n; label A23 "خالص ساير درآمدها و هزینه‌ها ")
  - D23 = 43015355 (type n; label A23 "خالص ساير درآمدها و هزینه‌ها ")
  - B24 = -28908689 (type n; label A24 "هزينه‌هاي اداري و عمومي ")
  - D24 = -52654898 (type n; label A24 "هزينه‌هاي اداري و عمومي ")
  - B25 = -11646662 (type n; label A25 "هزينه مطالبات مشکوک الوصول ")
  - D25 = -50322016 (type n; label A25 "هزينه مطالبات مشکوک الوصول ")
  - B26 = -5804157 (type n; label A26 "هزينه‌هاي مالي ")
  - D26 = -20082491 (type n; label A26 "هزينه‌هاي مالي ")
  - B27 = -918350 (type n; label A27 "هزينه استهلاک ")
  - D27 = -1161578 (type n; label A27 "هزينه استهلاک ")
  - B28 = -25195703 (type n; label A28 "سود(زیان) عملیات در حال تداوم قبل از مالیات ")
  - D28 = -6576895 (type n; label A28 "سود(زیان) عملیات در حال تداوم قبل از مالیات ")
  - B29 = 0 (type n; label A29 "ماليات بر درآمد سال جاری ")
  - D29 = -2548000 (type n; label A29 "ماليات بر درآمد سال جاری ")
  - B30 = 0 (type n; label A30 "ماليات بر درآمد سال های قبل ")
  - D30 = 0 (type n; label A30 "ماليات بر درآمد سال های قبل ")
  - B31 = -25195703 (type n; label A31 "سود (زيان) خالص عملیات در حال تداوم ")
  - D31 = -9124895 (type n; label A31 "سود (زيان) خالص عملیات در حال تداوم ")
  - B33 = 0 (type n; label A33 "سود(زیان) خالص عملیات متوقف شده ")
  - D33 = 0 (type n; label A33 "سود(زیان) خالص عملیات متوقف شده ")
  - B34 = -25195703 (type n; label A34 "سود(زیان) خالص ")
  - D34 = -9124895 (type n; label A34 "سود(زیان) خالص ")
  - B36 = -152 (type n; label A36 "عملياتي (ريال) ")
  - D36 = -237 (type n; label A36 "عملياتي (ريال) ")
  - B37 = -22 (type n; label A37 "غيرعملياتي(ريال) ")
  - D37 = 174 (type n; label A37 "غيرعملياتي(ريال) ")
  - B38 = -174 (type n; label A38 "ناشی از عملیات در حال تداوم(ریال) ")
  - D38 = -63 (type n; label A38 "ناشی از عملیات در حال تداوم(ریال) ")
  - B39 = 0 (type n; label A39 "ناشي از عمليات متوقف شده(ريال) ")
  - D39 = 0 (type n; label A39 "ناشي از عمليات متوقف شده(ريال) ")
  - B40 = -174 (type n; label A40 "سود(زیان) پایه هر سهم (ریال) ")
  - D40 = -63 (type n; label A40 "سود(زیان) پایه هر سهم (ریال) ")
  - B41 = -161 (type n; label A41 "سود (زیان) خالص هر سهم– ریال ")
  - D41 = -58 (type n; label A41 "سود (زیان) خالص هر سهم– ریال ")
  - B42 = 156340000 (type n; label A42 "سرمایه ")
  - D42 = 156340000 (type n; label A42 "سرمایه ")
- Black/dark excluded cells 33 coordinates `["C10", "C11", "C12", "C13", "C14", "C15", "C16", "C17", "C18", "C19", "C20", "C21", "C22", "C23", "C24", "C25", "C26", "C27", "C28", "C29", "C30", "C31", "C32", "C33", "C34", "C35", "C36", "C37", "C38", "C39", "C40", "C41", "C42"]`.
  - Physical columns ["C"]; header text in them `[]`.
- Green sub-table names 3:
  - A12 = "عملیات در حال تداوم: "; relative row 3; physical column A; exact sub-table bounds unresolved.
  - A32 = "عملیات متوقف شده: "; relative row 23; physical column A; exact sub-table bounds unresolved.
  - A35 = "سود (زیان)پایه هر سهم (ريال) "; relative row 26; physical column A; exact sub-table bounds unresolved.
- Other/unfilled cells 39 coordinates `["A11", "E11", "B12", "D12", "E12", "E13", "E14", "E15", "E16", "E17", "E18", "E19", "E20", "E21", "E22", "E23", "E24", "E25", "E26", "E27", "E28", "E29", "E30", "E31", "B32", "D32", "E32", "E33", "E34", "B35", "D35", "E35", "E36", "E37", "E38", "E39", "E40", "E41", "E42"]`.
- Yellow with no same-row gray: `[]`.
- Gray with no same-row yellow: `[]`.

### Candidate 02: Recovered_Sheet1!A60:E68

- Bounds A60 through E68; 9 rows ? 5 columns.
- Red name A58 = "صورت سود و زیان جامع"; distance 2 row(s); fill `{"fill_type": "solid", "color_type": "rgb", "rgb": "FFFF0000", "theme": null, "indexed": null, "tint": 0.0}`.
- Thick outline not confirmed; medium edge properties `{"top": {"styles": {"medium": 5}, "gaps": 0}, "bottom": {"styles": {"medium": 4, "thin": 1}, "gaps": 0}, "left": {"styles": {"medium": 9}, "gaps": 0}, "right": {"styles": {"medium": 9}, "gaps": 0}}`.
- Merged ranges: `E60:E61`, `A60:A61`.
- Blue header cells 6 on rows [60, 61]:
  - A60 = "شرح" (blue1)
  - B60 = "دوره منتهي به ۱۴۰۳/۰۶/۳۱" (blue1)
  - D60 = "تجدید ارائه شده ۱۴۰۲/۱۲/۲۹" (blue1)
  - E60 = "درصد تغییر" (blue1)
  - B61 = "حسابرسی نشده" (blue1)
  - D61 = "حسابرسی شده" (blue1)
- Merged header ranges `["E60:E61", "A60:A61"]`.
- Yellow description/label cells 6:
  - A62 = "سود(زیان) خالص "
  - A64 = "مازاد تجديد ارزيابي دارايي‌ها "
  - A65 = "تفاوت تسعیر ارز عملیات خارجی "
  - A66 = "مالیات مربوط به سایر اقلام سود و زیان جامع "
  - A67 = "سایر اقلام سود و زیان جامع سال پس از کسر مالیات "
  - A68 = "سود(زيان) جامع سال "
- Gray value cells 12 with same-row yellow label(s):
  - B62 = -25195703 (type n; label A62 "سود(زیان) خالص ")
  - D62 = -9124895 (type n; label A62 "سود(زیان) خالص ")
  - B64 = 0 (type n; label A64 "مازاد تجديد ارزيابي دارايي‌ها ")
  - D64 = 0 (type n; label A64 "مازاد تجديد ارزيابي دارايي‌ها ")
  - B65 = 0 (type n; label A65 "تفاوت تسعیر ارز عملیات خارجی ")
  - D65 = 0 (type n; label A65 "تفاوت تسعیر ارز عملیات خارجی ")
  - B66 = 0 (type n; label A66 "مالیات مربوط به سایر اقلام سود و زیان جامع ")
  - D66 = 0 (type n; label A66 "مالیات مربوط به سایر اقلام سود و زیان جامع ")
  - B67 = 0 (type n; label A67 "سایر اقلام سود و زیان جامع سال پس از کسر مالیات ")
  - D67 = 0 (type n; label A67 "سایر اقلام سود و زیان جامع سال پس از کسر مالیات ")
  - B68 = -25195703 (type n; label A68 "سود(زيان) جامع سال ")
  - D68 = -9124895 (type n; label A68 "سود(زيان) جامع سال ")
- Black/dark excluded cells 9 coordinates `["C60", "C61", "C62", "C63", "C64", "C65", "C66", "C67", "C68"]`.
  - Physical columns ["C"]; header text in them `[]`.
- Green sub-table names 1:
  - A63 = "سایر اقلام سود و زیان جامع: "; relative row 4; physical column A; exact sub-table bounds unresolved.
- Other/unfilled cells 11 coordinates `["A61", "E61", "E62", "B63", "D63", "E63", "E64", "E65", "E66", "E67", "E68"]`.
- Yellow with no same-row gray: `[]`.
- Gray with no same-row yellow: `[]`.

### Candidate 03: Recovered_Sheet1!A79:E119

- Bounds A79 through E119; 41 rows ? 5 columns.
- Red name A77 = "صورت وضعیت مالی"; distance 2 row(s); fill `{"fill_type": "solid", "color_type": "rgb", "rgb": "FFFF0000", "theme": null, "indexed": null, "tint": 0.0}`.
- Thick outline not confirmed; medium edge properties `{"top": {"styles": {"medium": 4, "null": 1}, "gaps": 1}, "bottom": {"styles": {"medium": 4, "null": 1}, "gaps": 1}, "left": {"styles": {"medium": 41}, "gaps": 0}, "right": {"styles": {"medium": 41}, "gaps": 0}}`.
- Merged ranges: `E79:E80`, `A79:A80`.
- Blue header cells 12 on rows [79, 80, 95]:
  - A79 = "شرح" (blue1)
  - B79 = "دوره منتهي به ۱۴۰۳/۰۶/۳۱" (blue1)
  - C79 = "تجدید ارائه شده ۱۴۰۲/۱۲/۲۹" (blue1)
  - D79 = "تجدید ارائه شده ۱۴۰۲/۰۱/۰۱" (blue1)
  - E79 = "درصد تغييرات" (blue1)
  - B80 = "حسابرسی نشده" (blue1)
  - C80 = "حسابرسی شده" (blue1)
  - D80 = "حسابرسی نشده" (blue1)
  - A95 = "حقوق مالکانه و بدهی‌ها " (blue2)
  - B95 = "دوره منتهی به ۱۴۰۳/۰۶/۳۱ " (blue2)
  - C95 = "تجدید ارائه شده ۱۴۰۲/۱۲/۲۹ " (blue2)
  - D95 = "تجدید ارائه شده۱۴۰۲/۰۱/۰۱ " (blue2)
- Merged header ranges `["E79:E80", "A79:A80"]`.
- Yellow description/label cells 35:
  - A82 = "موجودي نقد "
  - A83 = "مطالبات از بانک ها و ساير موسسات اعتباري "
  - A84 = "مطالبات از دولت "
  - A85 = "تسهيلات اعطايي و مطالبات از اشخاص دولتي "
  - A86 = "تسهيلات اعطايي و مطالبات از اشخاص غير دولتي "
  - A87 = "سرمایه‌گذاری در سهام و ساير اوراق بهادار "
  - A88 = "مطالبات از شرکت‌های فرعی و وابسته "
  - A89 = "ساير حسابهاي دريافتني "
  - A90 = "دارایی‌هاي ثابت مشهود "
  - A91 = "دارایی‌هاي نا مشهود "
  - A92 = "سپرده قانونی "
  - A93 = "ساير دارایی‌ها "
  - A94 = "جمع دارایی‌ها "
  - A97 = "سرمايه "
  - A98 = "افزايش سرمايه در جريان "
  - A99 = "صرف سهام "
  - A100 = "اندوخته صرف سهام "
  - A101 = "اندوخته قانوني "
  - A102 = "ساير اندوخته‌ها "
  - A103 = "مازاد تجديد ارزيابي دارايي‌ها "
  - A104 = "تفاوت تسعیر ارز "
  - A105 = "سود (زيان) انباشته "
  - A106 = "سهام خزانه "
  - A107 = "جمع حقوق مالکانه "
  - A109 = "بدهي به بانكها و ساير موسسات اعتباري "
  - A110 = "سپرده‌هاي مشتریان "
  - A111 = "سود سهام پرداختني "
  - A112 = "اوراق بدهی "
  - A113 = "ذخيره ماليات عملکرد "
  - A114 = "ذخاير و ساير بدهی‌ها "
  - A115 = "ذخيره مزاياي پايان خدمت و تعهدات بازنشستگی کارکنان "
  - A116 = "جمع بدهی های قبل از حقوق صاحبان سپرده های سرمایه گذاری "
  - A117 = "حقوق صاحبان سپرده‌های سرمایه‌گذاری "
  - A118 = "جمع بدهی‌ها "
  - A119 = "جمع بدهی‌ها و حقوق مالکانه "
- Gray value cells 70 with same-row yellow label(s):
  - B82 = 347110539 (type n; label A82 "موجودي نقد ")
  - C82 = 295173082 (type n; label A82 "موجودي نقد ")
  - B83 = 686275365 (type n; label A83 "مطالبات از بانک ها و ساير موسسات اعتباري ")
  - C83 = 696743016 (type n; label A83 "مطالبات از بانک ها و ساير موسسات اعتباري ")
  - B84 = 2920800 (type n; label A84 "مطالبات از دولت ")
  - C84 = 2925324 (type n; label A84 "مطالبات از دولت ")
  - B85 = 5517538 (type n; label A85 "تسهيلات اعطايي و مطالبات از اشخاص دولتي ")
  - C85 = 5024806 (type n; label A85 "تسهيلات اعطايي و مطالبات از اشخاص دولتي ")
  - B86 = 2826181422 (type n; label A86 "تسهيلات اعطايي و مطالبات از اشخاص غير دولتي ")
  - C86 = 2662958772 (type n; label A86 "تسهيلات اعطايي و مطالبات از اشخاص غير دولتي ")
  - B87 = 263166697 (type n; label A87 "سرمایه‌گذاری در سهام و ساير اوراق بهادار ")
  - C87 = 250958540 (type n; label A87 "سرمایه‌گذاری در سهام و ساير اوراق بهادار ")
  - B88 = 107179477 (type n; label A88 "مطالبات از شرکت‌های فرعی و وابسته ")
  - C88 = 107851311 (type n; label A88 "مطالبات از شرکت‌های فرعی و وابسته ")
  - B89 = 462006254 (type n; label A89 "ساير حسابهاي دريافتني ")
  - C89 = 432339509 (type n; label A89 "ساير حسابهاي دريافتني ")
  - B90 = 23049146 (type n; label A90 "دارایی‌هاي ثابت مشهود ")
  - C90 = 22273873 (type n; label A90 "دارایی‌هاي ثابت مشهود ")
  - B91 = 23180530 (type n; label A91 "دارایی‌هاي نا مشهود ")
  - C91 = 23237672 (type n; label A91 "دارایی‌هاي نا مشهود ")
  - B92 = 291130716 (type n; label A92 "سپرده قانونی ")
  - C92 = 275811706 (type n; label A92 "سپرده قانونی ")
  - B93 = 101636499 (type n; label A93 "ساير دارایی‌ها ")
  - C93 = 72855571 (type n; label A93 "ساير دارایی‌ها ")
  - B94 = 5139354983 (type n; label A94 "جمع دارایی‌ها ")
  - C94 = 4848153182 (type n; label A94 "جمع دارایی‌ها ")
  - B97 = 156340000 (type n; label A97 "سرمايه ")
  - C97 = 156340000 (type n; label A97 "سرمايه ")
  - B98 = 0 (type n; label A98 "افزايش سرمايه در جريان ")
  - C98 = 0 (type n; label A98 "افزايش سرمايه در جريان ")
  - B99 = 0 (type n; label A99 "صرف سهام ")
  - C99 = 0 (type n; label A99 "صرف سهام ")
  - B100 = 0 (type n; label A100 "اندوخته صرف سهام ")
  - C100 = 0 (type n; label A100 "اندوخته صرف سهام ")
  - B101 = 7393601 (type n; label A101 "اندوخته قانوني ")
  - C101 = 7393601 (type n; label A101 "اندوخته قانوني ")
  - B102 = 985814 (type n; label A102 "ساير اندوخته‌ها ")
  - C102 = 985814 (type n; label A102 "ساير اندوخته‌ها ")
  - B103 = 0 (type n; label A103 "مازاد تجديد ارزيابي دارايي‌ها ")
  - C103 = 0 (type n; label A103 "مازاد تجديد ارزيابي دارايي‌ها ")
  - B104 = 0 (type n; label A104 "تفاوت تسعیر ارز ")
  - C104 = 0 (type n; label A104 "تفاوت تسعیر ارز ")
  - B105 = -69959998 (type n; label A105 "سود (زيان) انباشته ")
  - C105 = -44764295 (type n; label A105 "سود (زيان) انباشته ")
  - B106 = -26884902 (type n; label A106 "سهام خزانه ")
  - C106 = -26163160 (type n; label A106 "سهام خزانه ")
  - B107 = 67874515 (type n; label A107 "جمع حقوق مالکانه ")
  - C107 = 93791960 (type n; label A107 "جمع حقوق مالکانه ")
  - B109 = 867341907 (type n; label A109 "بدهي به بانكها و ساير موسسات اعتباري ")
  - C109 = 772033496 (type n; label A109 "بدهي به بانكها و ساير موسسات اعتباري ")
  - B110 = 3215472710 (type n; label A110 "سپرده‌هاي مشتریان ")
  - C110 = 3081957372 (type n; label A110 "سپرده‌هاي مشتریان ")
  - B111 = 324154 (type n; label A111 "سود سهام پرداختني ")
  - C111 = 1815045 (type n; label A111 "سود سهام پرداختني ")
  - B112 = 0 (type n; label A112 "اوراق بدهی ")
  - C112 = 0 (type n; label A112 "اوراق بدهی ")
  - B113 = 0 (type n; label A113 "ذخيره ماليات عملکرد ")
  - C113 = 2548000 (type n; label A113 "ذخيره ماليات عملکرد ")
  - B114 = 974455743 (type n; label A114 "ذخاير و ساير بدهی‌ها ")
  - C114 = 883995351 (type n; label A114 "ذخاير و ساير بدهی‌ها ")
  - B115 = 13885954 (type n; label A115 "ذخيره مزاياي پايان خدمت و تعهدات بازنشستگی کارکنان ")
  - C115 = 12011958 (type n; label A115 "ذخيره مزاياي پايان خدمت و تعهدات بازنشستگی کارکنان ")
  - B116 = 5071480468 (type n; label A116 "جمع بدهی های قبل از حقوق صاحبان سپرده های سرمایه گذاری ")
  - C116 = 4754361222 (type n; label A116 "جمع بدهی های قبل از حقوق صاحبان سپرده های سرمایه گذاری ")
  - B117 = 0 (type n; label A117 "حقوق صاحبان سپرده‌های سرمایه‌گذاری ")
  - C117 = 0 (type n; label A117 "حقوق صاحبان سپرده‌های سرمایه‌گذاری ")
  - B118 = 5071480468 (type n; label A118 "جمع بدهی‌ها ")
  - C118 = 4754361222 (type n; label A118 "جمع بدهی‌ها ")
  - B119 = 5139354983 (type n; label A119 "جمع بدهی‌ها و حقوق مالکانه ")
  - C119 = 4848153182 (type n; label A119 "جمع بدهی‌ها و حقوق مالکانه ")
- Black/dark excluded cells 0 coordinates `[]`.
  - Physical columns []; header text in them `[]`.
- Green sub-table names 3:
  - A81 = "دارایی ها "; relative row 3; physical column A; exact sub-table bounds unresolved.
  - A96 = "حقوق مالکانه "; relative row 18; physical column A; exact sub-table bounds unresolved.
  - A108 = "بدهی‌ها "; relative row 30; physical column A; exact sub-table bounds unresolved.
- Other/unfilled cells 85 coordinates `["A80", "E80", "B81", "C81", "D81", "E81", "D82", "E82", "D83", "E83", "D84", "E84", "D85", "E85", "D86", "E86", "D87", "E87", "D88", "E88", "D89", "E89", "D90", "E90", "D91", "E91", "D92", "E92", "D93", "E93", "D94", "E94", "E95", "B96", "C96", "D96", "E96", "D97", "E97", "D98", "E98", "D99", "E99", "D100", "E100", "D101", "E101", "D102", "E102", "D103", "E103", "D104", "E104", "D105", "E105", "D106", "E106", "D107", "E107", "B108", "C108", "D108", "E108", "D109", "E109", "D110", "E110", "D111", "E111", "D112", "E112", "D113", "E113", "D114", "E114", "D115", "E115", "D116", "E116", "D117", "E117", "D118", "E118", "D119", "E119"]`.
- Yellow with no same-row gray: `[]`.
- Gray with no same-row yellow: `[]`.

### Candidate 04: Recovered_Sheet1!A130:L165

- Bounds A130 through L165; 36 rows ? 12 columns.
- Red name A128 = "صورت تغییرات در حقوق مالکانه"; distance 2 row(s); fill `{"fill_type": "solid", "color_type": "rgb", "rgb": "FFFF0000", "theme": null, "indexed": null, "tint": 0.0}`.
- Thick outline not confirmed; medium edge properties `{"top": {"styles": {"medium": 12}, "gaps": 0}, "bottom": {"styles": {"medium": 12}, "gaps": 0}, "left": {"styles": {"medium": 36}, "gaps": 0}, "right": {"styles": {"medium": 36}, "gaps": 0}}`.
- Merged ranges: none.
- Blue header cells 12 on rows [130]:
  - A130 = "شرح" (blue1)
  - B130 = "سرمایه" (blue1)
  - C130 = "افزایش سرمایه در جریان" (blue1)
  - D130 = "صرف سهام" (blue1)
  - E130 = "صرف سهام خزانه" (blue1)
  - F130 = "اندوخته قانونی" (blue1)
  - G130 = "سایر اندوخته‌ها" (blue1)
  - H130 = "مازاد تجدید ارزیابی دارایی‌ها" (blue1)
  - I130 = "تفاوت تسعیر ارز عملیات خارجی" (blue1)
  - J130 = "سود انباشته" (blue1)
  - K130 = "سهام خزانه" (blue1)
  - L130 = "جمع کل" (blue1)
- Merged header ranges `[]`.
- Yellow description/label cells 13:
  - A153 = "سود خالص ۱۴۰۳/۰۶/۳۱ "
  - A154 = "سایر اقلام سود و زیان جامع پس از کسر مالیات "
  - A155 = "سود(زيان) جامع در ۱۴۰۳/۰۶/۳۱ "
  - A156 = "سود(زيان) سهام مصوب "
  - A157 = "افزایش سرمایه "
  - A158 = "افزایش سرمایه در جریان "
  - A159 = "خرید سهام خزانه "
  - A160 = "فروش سهام خزانه "
  - A161 = "سود (زیان) حاصل از فروش سهام خزانه "
  - A162 = "انتقال از سایر اقلام حقوق مالکانه به سود و زیان انباشته "
  - A163 = "تخصیص به اندوخته قانونی "
  - A164 = "تخصیص به سایر اندوخته‌ها "
  - A165 = "مانده در ۱۴۰۳/۰۶/۳۱ "
- Gray value cells 143 with same-row yellow label(s):
  - B153 = null (type n; label A153 "سود خالص ۱۴۰۳/۰۶/۳۱ ")
  - C153 = null (type n; label A153 "سود خالص ۱۴۰۳/۰۶/۳۱ ")
  - D153 = null (type n; label A153 "سود خالص ۱۴۰۳/۰۶/۳۱ ")
  - E153 = null (type n; label A153 "سود خالص ۱۴۰۳/۰۶/۳۱ ")
  - F153 = null (type n; label A153 "سود خالص ۱۴۰۳/۰۶/۳۱ ")
  - G153 = null (type n; label A153 "سود خالص ۱۴۰۳/۰۶/۳۱ ")
  - H153 = null (type n; label A153 "سود خالص ۱۴۰۳/۰۶/۳۱ ")
  - I153 = null (type n; label A153 "سود خالص ۱۴۰۳/۰۶/۳۱ ")
  - J153 = -25195703 (type n; label A153 "سود خالص ۱۴۰۳/۰۶/۳۱ ")
  - K153 = null (type n; label A153 "سود خالص ۱۴۰۳/۰۶/۳۱ ")
  - L153 = -25195703 (type n; label A153 "سود خالص ۱۴۰۳/۰۶/۳۱ ")
  - B154 = null (type n; label A154 "سایر اقلام سود و زیان جامع پس از کسر مالیات ")
  - C154 = null (type n; label A154 "سایر اقلام سود و زیان جامع پس از کسر مالیات ")
  - D154 = null (type n; label A154 "سایر اقلام سود و زیان جامع پس از کسر مالیات ")
  - E154 = null (type n; label A154 "سایر اقلام سود و زیان جامع پس از کسر مالیات ")
  - F154 = null (type n; label A154 "سایر اقلام سود و زیان جامع پس از کسر مالیات ")
  - G154 = null (type n; label A154 "سایر اقلام سود و زیان جامع پس از کسر مالیات ")
  - H154 = 0 (type n; label A154 "سایر اقلام سود و زیان جامع پس از کسر مالیات ")
  - I154 = 0 (type n; label A154 "سایر اقلام سود و زیان جامع پس از کسر مالیات ")
  - J154 = null (type n; label A154 "سایر اقلام سود و زیان جامع پس از کسر مالیات ")
  - K154 = null (type n; label A154 "سایر اقلام سود و زیان جامع پس از کسر مالیات ")
  - L154 = 0 (type n; label A154 "سایر اقلام سود و زیان جامع پس از کسر مالیات ")
  - B155 = 0 (type n; label A155 "سود(زيان) جامع در ۱۴۰۳/۰۶/۳۱ ")
  - C155 = 0 (type n; label A155 "سود(زيان) جامع در ۱۴۰۳/۰۶/۳۱ ")
  - D155 = 0 (type n; label A155 "سود(زيان) جامع در ۱۴۰۳/۰۶/۳۱ ")
  - E155 = 0 (type n; label A155 "سود(زيان) جامع در ۱۴۰۳/۰۶/۳۱ ")
  - F155 = 0 (type n; label A155 "سود(زيان) جامع در ۱۴۰۳/۰۶/۳۱ ")
  - G155 = 0 (type n; label A155 "سود(زيان) جامع در ۱۴۰۳/۰۶/۳۱ ")
  - H155 = 0 (type n; label A155 "سود(زيان) جامع در ۱۴۰۳/۰۶/۳۱ ")
  - I155 = 0 (type n; label A155 "سود(زيان) جامع در ۱۴۰۳/۰۶/۳۱ ")
  - J155 = -25195703 (type n; label A155 "سود(زيان) جامع در ۱۴۰۳/۰۶/۳۱ ")
  - K155 = 0 (type n; label A155 "سود(زيان) جامع در ۱۴۰۳/۰۶/۳۱ ")
  - L155 = -25195703 (type n; label A155 "سود(زيان) جامع در ۱۴۰۳/۰۶/۳۱ ")
  - B156 = null (type n; label A156 "سود(زيان) سهام مصوب ")
  - C156 = null (type n; label A156 "سود(زيان) سهام مصوب ")
  - D156 = null (type n; label A156 "سود(زيان) سهام مصوب ")
  - E156 = null (type n; label A156 "سود(زيان) سهام مصوب ")
  - F156 = null (type n; label A156 "سود(زيان) سهام مصوب ")
  - G156 = null (type n; label A156 "سود(زيان) سهام مصوب ")
  - H156 = null (type n; label A156 "سود(زيان) سهام مصوب ")
  - I156 = null (type n; label A156 "سود(زيان) سهام مصوب ")
  - J156 = 0 (type n; label A156 "سود(زيان) سهام مصوب ")
  - K156 = null (type n; label A156 "سود(زيان) سهام مصوب ")
  - L156 = 0 (type n; label A156 "سود(زيان) سهام مصوب ")
  - B157 = 0 (type n; label A157 "افزایش سرمایه ")
  - C157 = null (type n; label A157 "افزایش سرمایه ")
  - D157 = 0 (type n; label A157 "افزایش سرمایه ")
  - E157 = 0 (type n; label A157 "افزایش سرمایه ")
  - F157 = null (type n; label A157 "افزایش سرمایه ")
  - G157 = 0 (type n; label A157 "افزایش سرمایه ")
  - H157 = 0 (type n; label A157 "افزایش سرمایه ")
  - I157 = 0 (type n; label A157 "افزایش سرمایه ")
  - J157 = 0 (type n; label A157 "افزایش سرمایه ")
  - K157 = null (type n; label A157 "افزایش سرمایه ")
  - L157 = 0 (type n; label A157 "افزایش سرمایه ")
  - B158 = 0 (type n; label A158 "افزایش سرمایه در جریان ")
  - C158 = 0 (type n; label A158 "افزایش سرمایه در جریان ")
  - D158 = null (type n; label A158 "افزایش سرمایه در جریان ")
  - E158 = null (type n; label A158 "افزایش سرمایه در جریان ")
  - F158 = null (type n; label A158 "افزایش سرمایه در جریان ")
  - G158 = null (type n; label A158 "افزایش سرمایه در جریان ")
  - H158 = null (type n; label A158 "افزایش سرمایه در جریان ")
  - I158 = null (type n; label A158 "افزایش سرمایه در جریان ")
  - J158 = 0 (type n; label A158 "افزایش سرمایه در جریان ")
  - K158 = null (type n; label A158 "افزایش سرمایه در جریان ")
  - L158 = 0 (type n; label A158 "افزایش سرمایه در جریان ")
  - B159 = null (type n; label A159 "خرید سهام خزانه ")
  - C159 = null (type n; label A159 "خرید سهام خزانه ")
  - D159 = null (type n; label A159 "خرید سهام خزانه ")
  - E159 = null (type n; label A159 "خرید سهام خزانه ")
  - F159 = null (type n; label A159 "خرید سهام خزانه ")
  - G159 = null (type n; label A159 "خرید سهام خزانه ")
  - H159 = null (type n; label A159 "خرید سهام خزانه ")
  - I159 = null (type n; label A159 "خرید سهام خزانه ")
  - J159 = null (type n; label A159 "خرید سهام خزانه ")
  - K159 = -721742 (type n; label A159 "خرید سهام خزانه ")
  - L159 = -721742 (type n; label A159 "خرید سهام خزانه ")
  - B160 = null (type n; label A160 "فروش سهام خزانه ")
  - C160 = null (type n; label A160 "فروش سهام خزانه ")
  - D160 = null (type n; label A160 "فروش سهام خزانه ")
  - E160 = null (type n; label A160 "فروش سهام خزانه ")
  - F160 = null (type n; label A160 "فروش سهام خزانه ")
  - G160 = null (type n; label A160 "فروش سهام خزانه ")
  - H160 = null (type n; label A160 "فروش سهام خزانه ")
  - I160 = null (type n; label A160 "فروش سهام خزانه ")
  - J160 = null (type n; label A160 "فروش سهام خزانه ")
  - K160 = 0 (type n; label A160 "فروش سهام خزانه ")
  - L160 = 0 (type n; label A160 "فروش سهام خزانه ")
  - B161 = null (type n; label A161 "سود (زیان) حاصل از فروش سهام خزانه ")
  - C161 = null (type n; label A161 "سود (زیان) حاصل از فروش سهام خزانه ")
  - D161 = null (type n; label A161 "سود (زیان) حاصل از فروش سهام خزانه ")
  - E161 = 0 (type n; label A161 "سود (زیان) حاصل از فروش سهام خزانه ")
  - F161 = null (type n; label A161 "سود (زیان) حاصل از فروش سهام خزانه ")
  - G161 = null (type n; label A161 "سود (زیان) حاصل از فروش سهام خزانه ")
  - H161 = null (type n; label A161 "سود (زیان) حاصل از فروش سهام خزانه ")
  - I161 = null (type n; label A161 "سود (زیان) حاصل از فروش سهام خزانه ")
  - J161 = null (type n; label A161 "سود (زیان) حاصل از فروش سهام خزانه ")
  - K161 = null (type n; label A161 "سود (زیان) حاصل از فروش سهام خزانه ")
  - L161 = 0 (type n; label A161 "سود (زیان) حاصل از فروش سهام خزانه ")
  - B162 = null (type n; label A162 "انتقال از سایر اقلام حقوق مالکانه به سود و زیان انباشته ")
  - C162 = null (type n; label A162 "انتقال از سایر اقلام حقوق مالکانه به سود و زیان انباشته ")
  - D162 = null (type n; label A162 "انتقال از سایر اقلام حقوق مالکانه به سود و زیان انباشته ")
  - E162 = 0 (type n; label A162 "انتقال از سایر اقلام حقوق مالکانه به سود و زیان انباشته ")
  - F162 = null (type n; label A162 "انتقال از سایر اقلام حقوق مالکانه به سود و زیان انباشته ")
  - G162 = null (type n; label A162 "انتقال از سایر اقلام حقوق مالکانه به سود و زیان انباشته ")
  - H162 = 0 (type n; label A162 "انتقال از سایر اقلام حقوق مالکانه به سود و زیان انباشته ")
  - I162 = 0 (type n; label A162 "انتقال از سایر اقلام حقوق مالکانه به سود و زیان انباشته ")
  - J162 = 0 (type n; label A162 "انتقال از سایر اقلام حقوق مالکانه به سود و زیان انباشته ")
  - K162 = null (type n; label A162 "انتقال از سایر اقلام حقوق مالکانه به سود و زیان انباشته ")
  - L162 = 0 (type n; label A162 "انتقال از سایر اقلام حقوق مالکانه به سود و زیان انباشته ")
  - B163 = null (type n; label A163 "تخصیص به اندوخته قانونی ")
  - C163 = null (type n; label A163 "تخصیص به اندوخته قانونی ")
  - D163 = null (type n; label A163 "تخصیص به اندوخته قانونی ")
  - E163 = null (type n; label A163 "تخصیص به اندوخته قانونی ")
  - F163 = 0 (type n; label A163 "تخصیص به اندوخته قانونی ")
  - G163 = null (type n; label A163 "تخصیص به اندوخته قانونی ")
  - H163 = null (type n; label A163 "تخصیص به اندوخته قانونی ")
  - I163 = null (type n; label A163 "تخصیص به اندوخته قانونی ")
  - J163 = 0 (type n; label A163 "تخصیص به اندوخته قانونی ")
  - K163 = null (type n; label A163 "تخصیص به اندوخته قانونی ")
  - L163 = 0 (type n; label A163 "تخصیص به اندوخته قانونی ")
  - B164 = null (type n; label A164 "تخصیص به سایر اندوخته‌ها ")
  - C164 = null (type n; label A164 "تخصیص به سایر اندوخته‌ها ")
  - D164 = null (type n; label A164 "تخصیص به سایر اندوخته‌ها ")
  - E164 = null (type n; label A164 "تخصیص به سایر اندوخته‌ها ")
  - F164 = null (type n; label A164 "تخصیص به سایر اندوخته‌ها ")
  - G164 = 0 (type n; label A164 "تخصیص به سایر اندوخته‌ها ")
  - H164 = null (type n; label A164 "تخصیص به سایر اندوخته‌ها ")
  - I164 = null (type n; label A164 "تخصیص به سایر اندوخته‌ها ")
  - J164 = 0 (type n; label A164 "تخصیص به سایر اندوخته‌ها ")
  - K164 = null (type n; label A164 "تخصیص به سایر اندوخته‌ها ")
  - L164 = 0 (type n; label A164 "تخصیص به سایر اندوخته‌ها ")
  - B165 = 156340000 (type n; label A165 "مانده در ۱۴۰۳/۰۶/۳۱ ")
  - C165 = 0 (type n; label A165 "مانده در ۱۴۰۳/۰۶/۳۱ ")
  - D165 = 0 (type n; label A165 "مانده در ۱۴۰۳/۰۶/۳۱ ")
  - E165 = 0 (type n; label A165 "مانده در ۱۴۰۳/۰۶/۳۱ ")
  - F165 = 7393601 (type n; label A165 "مانده در ۱۴۰۳/۰۶/۳۱ ")
  - G165 = 985814 (type n; label A165 "مانده در ۱۴۰۳/۰۶/۳۱ ")
  - H165 = 0 (type n; label A165 "مانده در ۱۴۰۳/۰۶/۳۱ ")
  - I165 = 0 (type n; label A165 "مانده در ۱۴۰۳/۰۶/۳۱ ")
  - J165 = -69959998 (type n; label A165 "مانده در ۱۴۰۳/۰۶/۳۱ ")
  - K165 = -26884902 (type n; label A165 "مانده در ۱۴۰۳/۰۶/۳۱ ")
  - L165 = 67874515 (type n; label A165 "مانده در ۱۴۰۳/۰۶/۳۱ ")
- Black/dark excluded cells 252 coordinates `["A131", "B131", "C131", "D131", "E131", "F131", "G131", "H131", "I131", "J131", "K131", "L131", "A132", "B132", "C132", "D132", "E132", "F132", "G132", "H132", "I132", "J132", "K132", "L132", "A133", "B133", "C133", "D133", "E133", "F133", "G133", "H133", "I133", "J133", "K133", "L133", "A134", "B134", "C134", "D134", "E134", "F134", "G134", "H134", "I134", "J134", "K134", "L134", "A135", "B135", "C135", "D135", "E135", "F135", "G135", "H135", "I135", "J135", "K135", "L135", "A136", "B136", "C136", "D136", "E136", "F136", "G136", "H136", "I136", "J136", "K136", "L136", "A137", "B137", "C137", "D137", "E137", "F137", "G137", "H137", "I137", "J137", "K137", "L137", "A138", "B138", "C138", "D138", "E138", "F138", "G138", "H138", "I138", "J138", "K138", "L138", "A139", "B139", "C139", "D139", "E139", "F139", "G139", "H139", "I139", "J139", "K139", "L139", "A140", "B140", "C140", "D140", "E140", "F140", "G140", "H140", "I140", "J140", "K140", "L140", "A141", "B141", "C141", "D141", "E141", "F141", "G141", "H141", "I141", "J141", "K141", "L141", "A142", "B142", "C142", "D142", "E142", "F142", "G142", "H142", "I142", "J142", "K142", "L142", "A143", "B143", "C143", "D143", "E143", "F143", "G143", "H143", "I143", "J143", "K143", "L143", "A144", "B144", "C144", "D144", "E144", "F144", "G144", "H144", "I144", "J144", "K144", "L144", "A145", "B145", "C145", "D145", "E145", "F145", "G145", "H145", "I145", "J145", "K145", "L145", "A146", "B146", "C146", "D146", "E146", "F146", "G146", "H146", "I146", "J146", "K146", "L146", "A147", "B147", "C147", "D147", "E147", "F147", "G147", "H147", "I147", "J147", "K147", "L147", "A148", "B148", "C148", "D148", "E148", "F148", "G148", "H148", "I148", "J148", "K148", "L148", "A149", "B149", "C149", "D149", "E149", "F149", "G149", "H149", "I149", "J149", "K149", "L149", "A150", "B150", "C150", "D150", "E150", "F150", "G150", "H150", "I150", "J150", "K150", "L150", "A151", "B151", "C151", "D151", "E151", "F151", "G151", "H151", "I151", "J151", "K151", "L151"]`.
  - Physical columns ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]; header text in them `[["A130", "شرح", "blue1"], ["B130", "سرمایه", "blue1"], ["C130", "افزایش سرمایه در جریان", "blue1"], ["D130", "صرف سهام", "blue1"], ["E130", "صرف سهام خزانه", "blue1"], ["F130", "اندوخته قانونی", "blue1"], ["G130", "سایر اندوخته‌ها", "blue1"], ["H130", "مازاد تجدید ارزیابی دارایی‌ها", "blue1"], ["I130", "تفاوت تسعیر ارز عملیات خارجی", "blue1"], ["J130", "سود انباشته", "blue1"], ["K130", "سهام خزانه", "blue1"], ["L130", "جمع کل", "blue1"]]`.
- Green sub-table names 1:
  - A152 = "تغییرات حقوق مالکانه در سال ۱۴۰۳/۰۶/۳۱ "; relative row 23; physical column A; exact sub-table bounds unresolved.
- Other/unfilled cells 11 coordinates `["B152", "C152", "D152", "E152", "F152", "G152", "H152", "I152", "J152", "K152", "L152"]`.
- Yellow with no same-row gray: `[]`.
- Gray with no same-row yellow: `[]`.

### Candidate 05: Recovered_Sheet1!A176:E213

- Bounds A176 through E213; 38 rows ? 5 columns.
- Red name A174 = "صورت جریان های نقدی"; distance 2 row(s); fill `{"fill_type": "solid", "color_type": "rgb", "rgb": "FFFF0000", "theme": null, "indexed": null, "tint": 0.0}`.
- Thick outline not confirmed; medium edge properties `{"top": {"styles": {"medium": 5}, "gaps": 0}, "bottom": {"styles": {"medium": 5}, "gaps": 0}, "left": {"styles": {"medium": 38}, "gaps": 0}, "right": {"styles": {"medium": 38}, "gaps": 0}}`.
- Merged ranges: `E176:E177`, `A176:A177`.
- Blue header cells 6 on rows [176, 177]:
  - A176 = "شرح" (blue1)
  - B176 = "دوره منتهي به ۱۴۰۳/۰۶/۳۱" (blue1)
  - D176 = "تجدید ارائه شده۱۴۰۲/۱۲/۲۹" (blue1)
  - E176 = "درصد تغییر" (blue1)
  - B177 = "حسابرسی نشده" (blue1)
  - D177 = "حسابرسی شده" (blue1)
- Merged header ranges `["E176:E177", "A176:A177"]`.
- Yellow description/label cells 33:
  - A179 = "نقد حاصل از عملیات "
  - A180 = "پرداخت‌های نقدی بابت مالیات بر درآمد "
  - A181 = "جريان ‌خالص ‌ورود‌ (خروج) ‌نقد حاصل از فعاليت‌هاي ‌عملياتي "
  - A183 = "وجوه پرداختي بابت تحصیل دارایی‌هاي ثابت مشهود "
  - A184 = "وجوه دریافتی بابت فروش دارایی‌هاي ثابت مشهود "
  - A185 = "وجوه پرداختي بابت تحصیل دارایی‌هاي نامشهود "
  - A186 = "وجوه دریافتی بابت فروش دارایی‌هاي نامشهود "
  - A187 = "وجوه پرداختي بابت تحصیل املاک و مستغلات غیر عملیاتی "
  - A188 = "وجوه دریافتی بابت فروش املاک و مستغلات غیر عملیاتی "
  - A189 = "جريان خالص ورود (خروج) وجه نقد ناشی از فعاليت‌هاي سرمایه‌گذاری "
  - A190 = "جريان خالص ورود (خروج) وجه نقد قبل از فعالیت‌های تامین مالی "
  - A192 = "دریافت‌های نقدی حاصل از افزايش سرمايه "
  - A193 = "دریافت‌های نقدی حاصل از صرف سهام "
  - A194 = "دریافت‌های نقدی حاصل از فروش سهام خزانه "
  - A195 = "پرداخت‌های نقدی برای خرید سهام خزانه "
  - A196 = "دریافت‌های نقدی حاصل از تسهيلات "
  - A197 = "پرداخت‌های نقدی بابت اصل تسهيلات "
  - A198 = "پرداخت‌های نقدی بابت سود تسهيلات "
  - A199 = "دریافت‌های نقدی حاصل از انتشار اوراق مشارکت "
  - A200 = "پرداخت‌های نقدی بابت اصل اوراق مشارکت "
  - A201 = "پرداخت‌های نقدی بابت سود اوراق مشارکت "
  - A202 = "دریافت‌های نقدی حاصل از انتشار اوراق خرید دین "
  - A203 = "پرداخت‌های نقدی بابت اصل اوراق خرید دین "
  - A204 = "پرداخت‌های نقدی بابت سود اوراق خرید دین "
  - A205 = "پرداخت‌های نقدی بابت اصل اقساط اجاره سرمایه‌ای "
  - A206 = "پرداخت‌های نقدی بابت سود اجاره سرمایه‌ای "
  - A207 = "پرداخت‌های نقدی بابت سود سهام "
  - A208 = "جريان خالص ورود (خروج) نقد حاصل از فعاليت‌هاي تامين مالي "
  - A209 = "خالص افزايش (کاهش) در موجودی نقد "
  - A210 = "مانده موجودی نقد در ابتدای سال "
  - A211 = "تاثير تغييرات نرخ ارز "
  - A212 = "مانده موجودی نقد در پايان سال "
  - A213 = "معاملات غيرنقدي "
- Gray value cells 66 with same-row yellow label(s):
  - B179 = -29363629 (type n; label A179 "نقد حاصل از عملیات ")
  - D179 = -96174356 (type n; label A179 "نقد حاصل از عملیات ")
  - B180 = -2548000 (type n; label A180 "پرداخت‌های نقدی بابت مالیات بر درآمد ")
  - D180 = 0 (type n; label A180 "پرداخت‌های نقدی بابت مالیات بر درآمد ")
  - B181 = -31911629 (type n; label A181 "جريان ‌خالص ‌ورود‌ (خروج) ‌نقد حاصل از فعاليت‌هاي ‌عملياتي ")
  - D181 = -96174356 (type n; label A181 "جريان ‌خالص ‌ورود‌ (خروج) ‌نقد حاصل از فعاليت‌هاي ‌عملياتي ")
  - B183 = -1379698 (type n; label A183 "وجوه پرداختي بابت تحصیل دارایی‌هاي ثابت مشهود ")
  - D183 = -7657549 (type n; label A183 "وجوه پرداختي بابت تحصیل دارایی‌هاي ثابت مشهود ")
  - B184 = 36457 (type n; label A184 "وجوه دریافتی بابت فروش دارایی‌هاي ثابت مشهود ")
  - D184 = 470555 (type n; label A184 "وجوه دریافتی بابت فروش دارایی‌هاي ثابت مشهود ")
  - B185 = -293822 (type n; label A185 "وجوه پرداختي بابت تحصیل دارایی‌هاي نامشهود ")
  - D185 = -1183590 (type n; label A185 "وجوه پرداختي بابت تحصیل دارایی‌هاي نامشهود ")
  - B186 = 582 (type n; label A186 "وجوه دریافتی بابت فروش دارایی‌هاي نامشهود ")
  - D186 = 0 (type n; label A186 "وجوه دریافتی بابت فروش دارایی‌هاي نامشهود ")
  - B187 = -11630341 (type n; label A187 "وجوه پرداختي بابت تحصیل املاک و مستغلات غیر عملیاتی ")
  - D187 = -15217227 (type n; label A187 "وجوه پرداختي بابت تحصیل املاک و مستغلات غیر عملیاتی ")
  - B188 = 261931 (type n; label A188 "وجوه دریافتی بابت فروش املاک و مستغلات غیر عملیاتی ")
  - D188 = 47066880 (type n; label A188 "وجوه دریافتی بابت فروش املاک و مستغلات غیر عملیاتی ")
  - B189 = -13004891 (type n; label A189 "جريان خالص ورود (خروج) وجه نقد ناشی از فعاليت‌هاي سرمایه‌گذاری ")
  - D189 = 23479069 (type n; label A189 "جريان خالص ورود (خروج) وجه نقد ناشی از فعاليت‌هاي سرمایه‌گذاری ")
  - B190 = -44916520 (type n; label A190 "جريان خالص ورود (خروج) وجه نقد قبل از فعالیت‌های تامین مالی ")
  - D190 = -72695287 (type n; label A190 "جريان خالص ورود (خروج) وجه نقد قبل از فعالیت‌های تامین مالی ")
  - B192 = 0 (type n; label A192 "دریافت‌های نقدی حاصل از افزايش سرمايه ")
  - D192 = 0 (type n; label A192 "دریافت‌های نقدی حاصل از افزايش سرمايه ")
  - B193 = 0 (type n; label A193 "دریافت‌های نقدی حاصل از صرف سهام ")
  - D193 = 0 (type n; label A193 "دریافت‌های نقدی حاصل از صرف سهام ")
  - B194 = 0 (type n; label A194 "دریافت‌های نقدی حاصل از فروش سهام خزانه ")
  - D194 = 0 (type n; label A194 "دریافت‌های نقدی حاصل از فروش سهام خزانه ")
  - B195 = -721743 (type n; label A195 "پرداخت‌های نقدی برای خرید سهام خزانه ")
  - D195 = -1739980 (type n; label A195 "پرداخت‌های نقدی برای خرید سهام خزانه ")
  - B196 = 14552949 (type n; label A196 "دریافت‌های نقدی حاصل از تسهيلات ")
  - D196 = 8680859 (type n; label A196 "دریافت‌های نقدی حاصل از تسهيلات ")
  - B197 = 0 (type n; label A197 "پرداخت‌های نقدی بابت اصل تسهيلات ")
  - D197 = -20082491 (type n; label A197 "پرداخت‌های نقدی بابت اصل تسهيلات ")
  - B198 = 0 (type n; label A198 "پرداخت‌های نقدی بابت سود تسهيلات ")
  - D198 = 0 (type n; label A198 "پرداخت‌های نقدی بابت سود تسهيلات ")
  - B199 = 0 (type n; label A199 "دریافت‌های نقدی حاصل از انتشار اوراق مشارکت ")
  - D199 = 0 (type n; label A199 "دریافت‌های نقدی حاصل از انتشار اوراق مشارکت ")
  - B200 = 0 (type n; label A200 "پرداخت‌های نقدی بابت اصل اوراق مشارکت ")
  - D200 = 0 (type n; label A200 "پرداخت‌های نقدی بابت اصل اوراق مشارکت ")
  - B201 = 0 (type n; label A201 "پرداخت‌های نقدی بابت سود اوراق مشارکت ")
  - D201 = 0 (type n; label A201 "پرداخت‌های نقدی بابت سود اوراق مشارکت ")
  - B202 = 0 (type n; label A202 "دریافت‌های نقدی حاصل از انتشار اوراق خرید دین ")
  - D202 = 0 (type n; label A202 "دریافت‌های نقدی حاصل از انتشار اوراق خرید دین ")
  - B203 = 0 (type n; label A203 "پرداخت‌های نقدی بابت اصل اوراق خرید دین ")
  - D203 = 0 (type n; label A203 "پرداخت‌های نقدی بابت اصل اوراق خرید دین ")
  - B204 = 0 (type n; label A204 "پرداخت‌های نقدی بابت سود اوراق خرید دین ")
  - D204 = 0 (type n; label A204 "پرداخت‌های نقدی بابت سود اوراق خرید دین ")
  - B205 = 0 (type n; label A205 "پرداخت‌های نقدی بابت اصل اقساط اجاره سرمایه‌ای ")
  - D205 = 0 (type n; label A205 "پرداخت‌های نقدی بابت اصل اقساط اجاره سرمایه‌ای ")
  - B206 = 0 (type n; label A206 "پرداخت‌های نقدی بابت سود اجاره سرمایه‌ای ")
  - D206 = 0 (type n; label A206 "پرداخت‌های نقدی بابت سود اجاره سرمایه‌ای ")
  - B207 = -1490891 (type n; label A207 "پرداخت‌های نقدی بابت سود سهام ")
  - D207 = -341 (type n; label A207 "پرداخت‌های نقدی بابت سود سهام ")
  - B208 = 12340315 (type n; label A208 "جريان خالص ورود (خروج) نقد حاصل از فعاليت‌هاي تامين مالي ")
  - D208 = -13141953 (type n; label A208 "جريان خالص ورود (خروج) نقد حاصل از فعاليت‌هاي تامين مالي ")
  - B209 = -32576205 (type n; label A209 "خالص افزايش (کاهش) در موجودی نقد ")
  - D209 = -85837240 (type n; label A209 "خالص افزايش (کاهش) در موجودی نقد ")
  - B210 = 295173082 (type n; label A210 "مانده موجودی نقد در ابتدای سال ")
  - D210 = 229326967 (type n; label A210 "مانده موجودی نقد در ابتدای سال ")
  - B211 = 84513662 (type n; label A211 "تاثير تغييرات نرخ ارز ")
  - D211 = 151683355 (type n; label A211 "تاثير تغييرات نرخ ارز ")
  - B212 = 347110539 (type n; label A212 "مانده موجودی نقد در پايان سال ")
  - D212 = 295173082 (type n; label A212 "مانده موجودی نقد در پايان سال ")
  - B213 = 35419379 (type n; label A213 "معاملات غيرنقدي ")
  - D213 = 40841096 (type n; label A213 "معاملات غيرنقدي ")
- Black/dark excluded cells 38 coordinates `["C176", "C177", "C178", "C179", "C180", "C181", "C182", "C183", "C184", "C185", "C186", "C187", "C188", "C189", "C190", "C191", "C192", "C193", "C194", "C195", "C196", "C197", "C198", "C199", "C200", "C201", "C202", "C203", "C204", "C205", "C206", "C207", "C208", "C209", "C210", "C211", "C212", "C213"]`.
  - Physical columns ["C"]; header text in them `[]`.
- Green sub-table names 3:
  - A178 = "جریان­های نقدی حاصل از فعاليت‌هاي عملياتي: "; relative row 3; physical column A; exact sub-table bounds unresolved.
  - A182 = "فعاليت‌هاي سرمایه‌گذاری "; relative row 7; physical column A; exact sub-table bounds unresolved.
  - A191 = "فعاليت‌هاي تأمين مالي "; relative row 16; physical column A; exact sub-table bounds unresolved.
- Other/unfilled cells 44 coordinates `["A177", "E177", "B178", "D178", "E178", "E179", "E180", "E181", "B182", "D182", "E182", "E183", "E184", "E185", "E186", "E187", "E188", "E189", "E190", "B191", "D191", "E191", "E192", "E193", "E194", "E195", "E196", "E197", "E198", "E199", "E200", "E201", "E202", "E203", "E204", "E205", "E206", "E207", "E208", "E209", "E210", "E211", "E212", "E213"]`.
- Yellow with no same-row gray: `[]`.
- Gray with no same-row yellow: `[]`.

### Candidate 06: Recovered_Sheet1!A238:K254

- Bounds A238 through K254; 17 rows ? 11 columns.
- Red name A236 = "مانده تسهیلات اعطایی و ذخیره مطالبات مشکوک الوصول:"; distance 2 row(s); fill `{"fill_type": "solid", "color_type": "rgb", "rgb": "FFFF0000", "theme": null, "indexed": null, "tint": 0.0}`.
- Thick outline not confirmed; medium edge properties `{"top": {"styles": {"medium": 11}, "gaps": 0}, "bottom": {"styles": {"medium": 11}, "gaps": 0}, "left": {"styles": {"medium": 17}, "gaps": 0}, "right": {"styles": {"medium": 17}, "gaps": 0}}`.
- Merged ranges: `F239:G239`, `H239:I239`, `A238:A239`, `J239:K239`, `B239:C239`, `D239:E239`.
- Blue header cells 12 on rows [238, 239]:
  - A238 = "شرح" (blue1)
  - C238 = "در تاریخ ۱۴۰۳/۰۶/۳۱" (blue1)
  - E238 = "در تاریخ ۱۴۰۳/۰۶/۳۱" (blue1)
  - G238 = "در تاریخ ۱۴۰۳/۰۶/۳۱" (blue1)
  - I238 = "در تاریخ ۱۴۰۳/۰۶/۳۱" (blue1)
  - J238 = "در تاریخ ۱۴۰۲/۱۲/۲۹" (blue1)
  - K238 = "در تاریخ ۱۴۰۳/۰۶/۳۱" (blue1)
  - B239 = "جاری" (blue1)
  - D239 = "سررسید گذشته" (blue1)
  - F239 = "معوق" (blue1)
  - H239 = "مشکوک الوصول" (blue1)
  - J239 = "جمع" (blue1)
- Merged header ranges `["F239:G239", "H239:I239", "A238:A239", "J239:K239", "B239:C239", "D239:E239"]`.
- Yellow description/label cells 12:
  - A240 = "تسهیلات اعطایی و مطالبات از اشخاص دولتی "
  - A241 = "تسهیلات اعطایی و مطالبات از اشخاص غیر دولتی- ریالی "
  - A242 = "تسهیلات اعطایی و مطالبات از اشخاص غیر دولتی- ارزی "
  - A245 = "سود سالهای آتی "
  - A246 = "سایر "
  - A247 = "مانده تسهیلات پایان دوره "
  - A248 = "ارزش وثایق دریافتی "
  - A249 = "مانده مبنای محاسبه ذخیره اختصاصی "
  - A250 = "ضریب مبنای احتساب ذخیره اختصاصی (درصد) "
  - A251 = "ذخیره اختصاصی مطالبات مشکوک الوصول "
  - A252 = "مانده مبنای محاسبه ذخیره عمومی "
  - A253 = "ذخیره عمومی مطالبات مشکوک الوصول "
- Gray value cells 48 with same-row yellow label(s):
  - C240 = 0 (type n; label A240 "تسهیلات اعطایی و مطالبات از اشخاص دولتی ")
  - E240 = 5601562 (type n; label A240 "تسهیلات اعطایی و مطالبات از اشخاص دولتی ")
  - G240 = 0 (type n; label A240 "تسهیلات اعطایی و مطالبات از اشخاص دولتی ")
  - I240 = 0 (type n; label A240 "تسهیلات اعطایی و مطالبات از اشخاص دولتی ")
  - C241 = 898771183 (type n; label A241 "تسهیلات اعطایی و مطالبات از اشخاص غیر دولتی- ریالی ")
  - E241 = 280319073 (type n; label A241 "تسهیلات اعطایی و مطالبات از اشخاص غیر دولتی- ریالی ")
  - G241 = 16190626 (type n; label A241 "تسهیلات اعطایی و مطالبات از اشخاص غیر دولتی- ریالی ")
  - I241 = 241404928 (type n; label A241 "تسهیلات اعطایی و مطالبات از اشخاص غیر دولتی- ریالی ")
  - C242 = 1469776118 (type n; label A242 "تسهیلات اعطایی و مطالبات از اشخاص غیر دولتی- ارزی ")
  - E242 = 38793986 (type n; label A242 "تسهیلات اعطایی و مطالبات از اشخاص غیر دولتی- ارزی ")
  - G242 = 46096435 (type n; label A242 "تسهیلات اعطایی و مطالبات از اشخاص غیر دولتی- ارزی ")
  - I242 = 147254352 (type n; label A242 "تسهیلات اعطایی و مطالبات از اشخاص غیر دولتی- ارزی ")
  - C245 = 145007474 (type n; label A245 "سود سالهای آتی ")
  - E245 = 0 (type n; label A245 "سود سالهای آتی ")
  - G245 = 0 (type n; label A245 "سود سالهای آتی ")
  - I245 = 0 (type n; label A245 "سود سالهای آتی ")
  - C246 = 4817501 (type n; label A246 "سایر ")
  - E246 = 0 (type n; label A246 "سایر ")
  - G246 = 0 (type n; label A246 "سایر ")
  - I246 = 0 (type n; label A246 "سایر ")
  - C247 = 2218722326 (type n; label A247 "مانده تسهیلات پایان دوره ")
  - E247 = 324714621 (type n; label A247 "مانده تسهیلات پایان دوره ")
  - G247 = 62287061 (type n; label A247 "مانده تسهیلات پایان دوره ")
  - I247 = 388659280 (type n; label A247 "مانده تسهیلات پایان دوره ")
  - C248 = null (type n; label A248 "ارزش وثایق دریافتی ")
  - E248 = 140833161 (type n; label A248 "ارزش وثایق دریافتی ")
  - G248 = 2459935 (type n; label A248 "ارزش وثایق دریافتی ")
  - I248 = 92049597 (type n; label A248 "ارزش وثایق دریافتی ")
  - C249 = null (type n; label A249 "مانده مبنای محاسبه ذخیره اختصاصی ")
  - E249 = 464200531 (type n; label A249 "مانده مبنای محاسبه ذخیره اختصاصی ")
  - G249 = 76017753 (type n; label A249 "مانده مبنای محاسبه ذخیره اختصاصی ")
  - I249 = 538014611 (type n; label A249 "مانده مبنای محاسبه ذخیره اختصاصی ")
  - C250 = null (type n; label A250 "ضریب مبنای احتساب ذخیره اختصاصی (درصد) ")
  - E250 = 10 (type n; label A250 "ضریب مبنای احتساب ذخیره اختصاصی (درصد) ")
  - G250 = 20 (type n; label A250 "ضریب مبنای احتساب ذخیره اختصاصی (درصد) ")
  - I250 = 50 (type n; label A250 "ضریب مبنای احتساب ذخیره اختصاصی (درصد) ")
  - C251 = null (type n; label A251 "ذخیره اختصاصی مطالبات مشکوک الوصول ")
  - E251 = 14049291 (type n; label A251 "ذخیره اختصاصی مطالبات مشکوک الوصول ")
  - G251 = 539710 (type n; label A251 "ذخیره اختصاصی مطالبات مشکوک الوصول ")
  - I251 = 114730469 (type n; label A251 "ذخیره اختصاصی مطالبات مشکوک الوصول ")
  - C252 = 2218722326 (type n; label A252 "مانده مبنای محاسبه ذخیره عمومی ")
  - E252 = 310665330 (type n; label A252 "مانده مبنای محاسبه ذخیره عمومی ")
  - G252 = 61747351 (type n; label A252 "مانده مبنای محاسبه ذخیره عمومی ")
  - I252 = 273928811 (type n; label A252 "مانده مبنای محاسبه ذخیره عمومی ")
  - C253 = 46762403 (type n; label A253 "ذخیره عمومی مطالبات مشکوک الوصول ")
  - E253 = 84023 (type n; label A253 "ذخیره عمومی مطالبات مشکوک الوصول ")
  - G253 = 0 (type n; label A253 "ذخیره عمومی مطالبات مشکوک الوصول ")
  - I253 = 0 (type n; label A253 "ذخیره عمومی مطالبات مشکوک الوصول ")
- Black/dark excluded cells 60 coordinates `["B238", "D238", "F238", "H238", "B240", "D240", "F240", "H240", "B241", "D241", "F241", "H241", "B242", "D242", "F242", "H242", "B243", "D243", "F243", "H243", "B244", "D244", "F244", "H244", "B245", "D245", "F245", "H245", "B246", "D246", "F246", "H246", "B247", "D247", "F247", "H247", "B248", "D248", "F248", "H248", "B249", "D249", "F249", "H249", "B250", "D250", "F250", "H250", "B251", "D251", "F251", "H251", "B252", "D252", "F252", "H252", "B253", "D253", "F253", "H253"]`.
  - Physical columns ["B", "D", "F", "H"]; header text in them `[["B239", "جاری", "blue1"], ["D239", "سررسید گذشته", "blue1"], ["F239", "معوق", "blue1"], ["H239", "مشکوک الوصول", "blue1"]]`.
- Green sub-table names 0:
- Other/unfilled cells 55 coordinates `["A239", "C239", "E239", "G239", "I239", "K239", "J240", "K240", "J241", "K241", "J242", "K242", "A243", "C243", "E243", "G243", "I243", "J243", "K243", "A244", "C244", "E244", "G244", "I244", "J244", "K244", "J245", "K245", "J246", "K246", "J247", "K247", "J248", "K248", "J249", "K249", "J250", "K250", "J251", "K251", "J252", "K252", "J253", "K253", "A254", "B254", "C254", "D254", "E254", "F254", "G254", "H254", "I254", "J254", "K254"]`.
- Yellow with no same-row gray: `[]`.
- Gray with no same-row yellow: `[]`.

### Candidate 07: Recovered_Sheet1!A266:F275

- Bounds A266 through F275; 10 rows ? 6 columns.
- Red name A264 = "مانده سپرده های دریافتی از مشتریان :"; distance 2 row(s); fill `{"fill_type": "solid", "color_type": "rgb", "rgb": "FFFF0000", "theme": null, "indexed": null, "tint": 0.0}`.
- Thick outline not confirmed; medium edge properties `{"top": {"styles": {"medium": 6}, "gaps": 0}, "bottom": {"styles": {"medium": 6}, "gaps": 0}, "left": {"styles": {"medium": 10}, "gaps": 0}, "right": {"styles": {"medium": 10}, "gaps": 0}}`.
- Merged ranges: `F266:F267`, `B266:C266`, `D266:E266`, `A266:A267`.
- Blue header cells 7 on rows [266, 267]:
  - A266 = "شرح" (blue1)
  - B266 = "مانده سپرده ها" (blue1)
  - D266 = "متوسط نرخ سود مانده سپرده ها" (blue1)
  - F266 = "برآورد مدیریت از تغییر در نرخ سود سپرده ها و تغییر در مانده سپرده های دریافتی از مشتریان" (blue1)
  - C267 = "در تاریخ ۱۴۰۳/۰۶/۳۱" (blue1)
  - D267 = "در تاریخ ۱۴۰۲/۱۲/۲۹" (blue1)
  - E267 = "در تاریخ ۱۴۰۳/۰۶/۳۱" (blue1)
- Merged header ranges `["F266:F267", "B266:C266", "D266:E266", "A266:A267"]`.
- Yellow description/label cells 7:
  - A269 = "سپرده های کوتاه مدت "
  - A270 = "سپرده های کوتاه مدت ویژه "
  - A271 = "سپرده های بلند مدت "
  - A272 = "جمع سپرده های هزینه زا "
  - A273 = "سپرده های غیر هزینه زا "
  - A274 = "جمع سپرده های ریالی "
  - A275 = "سپرده های ارزی "
- Gray value cells 7 with same-row yellow label(s):
  - C269 = 470781277 (type n; label A269 "سپرده های کوتاه مدت ")
  - C270 = 453951 (type n; label A270 "سپرده های کوتاه مدت ویژه ")
  - C271 = 1678516940 (type n; label A271 "سپرده های بلند مدت ")
  - C272 = 2149752168 (type n; label A272 "جمع سپرده های هزینه زا ")
  - C273 = 710993381 (type n; label A273 "سپرده های غیر هزینه زا ")
  - C274 = 2860745549 (type n; label A274 "جمع سپرده های ریالی ")
  - C275 = 418802062 (type n; label A275 "سپرده های ارزی ")
- Black/dark excluded cells 9 coordinates `["B267", "B268", "B269", "B270", "B271", "B272", "B273", "B274", "B275"]`.
  - Physical columns ["B"]; header text in them `[["B266", "مانده سپرده ها", "blue1"]]`.
- Green sub-table names 1:
  - A268 = "سپرده های ریالی: "; relative row 3; physical column A; exact sub-table bounds unresolved.
- Other/unfilled cells 29 coordinates `["C266", "E266", "A267", "F267", "C268", "D268", "E268", "F268", "D269", "E269", "F269", "D270", "E270", "F270", "D271", "E271", "F271", "D272", "E272", "F272", "D273", "E273", "F273", "D274", "E274", "F274", "D275", "E275", "F275"]`.
- Yellow with no same-row gray: `[]`.
- Gray with no same-row yellow: `[]`.

### Candidate 08: Recovered_Sheet1!A279:F284

- Bounds A279 through F284; 6 rows ? 6 columns.
- Red name A277 = "اقلام زیر خط:"; distance 2 row(s); fill `{"fill_type": "solid", "color_type": "rgb", "rgb": "FFFF0000", "theme": null, "indexed": null, "tint": 0.0}`.
- Thick outline not confirmed; medium edge properties `{"top": {"styles": {"medium": 6}, "gaps": 0}, "bottom": {"styles": {"medium": 6}, "gaps": 0}, "left": {"styles": {"medium": 6}, "gaps": 0}, "right": {"styles": {"medium": 6}, "gaps": 0}}`.
- Merged ranges: `B284:F284`.
- Blue header cells 6 on rows [279]:
  - A279 = "شرح" (blue1)
  - B279 = "۱۴۰۳/۰۶/۳۱" (blue1)
  - C279 = "۱۴۰۲/۱۲/۲۹" (blue1)
  - D279 = "شرح" (blue1)
  - E279 = "۱۴۰۳/۰۶/۳۱" (blue1)
  - F279 = "۱۴۰۲/۱۲/۲۹" (blue1)
- Merged header ranges `[]`.
- Yellow description/label cells 4:
  - A280 = "تعهدات مشتریان بابت اعتبارات اسنادی "
  - A281 = "تعهدات مشتریان بابت ضمانت نامه های صادره "
  - A282 = "ساير تعهدات مشتريان بانک "
  - A283 = "وجوه اداره شده و موارد مشابه "
- Gray value cells 4 with same-row yellow label(s):
  - B280 = 439498515 (type n; label A280 "تعهدات مشتریان بابت اعتبارات اسنادی ")
  - B281 = 705682218 (type n; label A281 "تعهدات مشتریان بابت ضمانت نامه های صادره ")
  - B282 = 19498400 (type n; label A282 "ساير تعهدات مشتريان بانک ")
  - B283 = 547 (type n; label A283 "وجوه اداره شده و موارد مشابه ")
- Black/dark excluded cells 0 coordinates `[]`.
  - Physical columns []; header text in them `[]`.
- Green sub-table names 0:
- Other/unfilled cells 22 coordinates `["C280", "D280", "E280", "F280", "C281", "D281", "E281", "F281", "C282", "D282", "E282", "F282", "C283", "D283", "E283", "F283", "A284", "B284", "C284", "D284", "E284", "F284"]`.
- Yellow with no same-row gray: `[]`.
- Gray with no same-row yellow: `[]`.

### Candidate 09: Recovered_Sheet1!A302:E308

- Bounds A302 through E308; 7 rows ? 5 columns.
- Red name A300 = "اطلاعات حق الوکاله و کفایت سرمایه"; distance 2 row(s); fill `{"fill_type": "solid", "color_type": "rgb", "rgb": "FFFF0000", "theme": null, "indexed": null, "tint": 0.0}`.
- Thick outline not confirmed; medium edge properties `{"top": {"styles": {"medium": 5}, "gaps": 0}, "bottom": {"styles": {"medium": 5}, "gaps": 0}, "left": {"styles": {"medium": 7}, "gaps": 0}, "right": {"styles": {"medium": 7}, "gaps": 0}}`.
- Merged ranges: `D306:E306`, `D307:E307`, `D305:E305`, `D302:E302`, `D304:E304`, `D303:E303`, `D308:E308`.
- Blue header cells 3 on rows [302]:
  - A302 = "شرح" (blue1)
  - C302 = "دوره ۶ ماهه منتهی به ۱۴۰۳/۰۶/۳۱" (blue1)
  - D302 = "برآورد تغییر روند در دوره ۶ ماهه منتهی به ۱۴۰۳/۱۲/۳۰" (blue1)
- Merged header ranges `["D302:E302"]`.
- Yellow description/label cells 6:
  - A303 = "سهم بانک از درآمدهای مشاع "
  - A304 = "سهم سپرده گذاران از درآمدهای مشاع "
  - A305 = "نرخ حق الوکاله اعلام شده "
  - A306 = "مبلغ حق الوکاله اعمال شده "
  - A307 = "مابه التفاوت سود قابل پرداخت (مازاد سود پرداختی) به سپرده گذاران "
  - A308 = "نسبت کفایت سرمایه "
- Gray value cells 6 with same-row yellow label(s):
  - C303 = 0 (type n; label A303 "سهم بانک از درآمدهای مشاع ")
  - C304 = 112241232 (type n; label A304 "سهم سپرده گذاران از درآمدهای مشاع ")
  - C305 = 0 (type n; label A305 "نرخ حق الوکاله اعلام شده ")
  - C306 = 0 (type n; label A306 "مبلغ حق الوکاله اعمال شده ")
  - C307 = -78487638 (type n; label A307 "مابه التفاوت سود قابل پرداخت (مازاد سود پرداختی) به سپرده گذاران ")
  - C308 = -3.38 (type n; label A308 "نسبت کفایت سرمایه ")
- Black/dark excluded cells 7 coordinates `["B302", "B303", "B304", "B305", "B306", "B307", "B308"]`.
  - Physical columns ["B"]; header text in them `[]`.
- Green sub-table names 0:
- Other/unfilled cells 13 coordinates `["E302", "D303", "E303", "D304", "E304", "D305", "E305", "D306", "E306", "D307", "E307", "D308", "E308"]`.
- Yellow with no same-row gray: `[]`.
- Gray with no same-row yellow: `[]`.

### Candidate 10: Recovered_Sheet1!A313:G332

- Bounds A313 through G332; 20 rows ? 7 columns.
- Red name A311 = "درآمد حاصل از تسهيلات اعطايي و سپرده گذاري"; distance 2 row(s); fill `{"fill_type": "solid", "color_type": "rgb", "rgb": "FFFF0000", "theme": null, "indexed": null, "tint": 0.0}`.
- Thick outline not confirmed; medium edge properties `{"top": {"styles": {"medium": 7}, "gaps": 0}, "bottom": {"styles": {"medium": 7}, "gaps": 0}, "left": {"styles": {"medium": 20}, "gaps": 0}, "right": {"styles": {"medium": 20}, "gaps": 0}}`.
- Merged ranges: `F320:G320`, `F329:G329`, `F326:G326`, `F321:G321`, `F315:G315`, `F318:G318`, `F332:G332`, `F313:G313`, `F319:G319`, `F322:G322`, `F317:G317`, `F323:G323`, `F325:G325`, `F327:G327`, `F314:G314`, `F316:G316`, `F331:G331`, `F330:G330`, `F324:G324`, `F328:G328`.
- Blue header cells 4 on rows [313]:
  - A313 = "شرح" (blue1)
  - D313 = "دوره ۶ ماهه منتهی به ۱۴۰۳/۰۶/۳۱" (blue1)
  - E313 = "متوسط نرخ سود دوره ۶ ماهه منتهی به ۱۴۰۳/۰۶/۳۱ (درصد)" (blue1)
  - F313 = "برآورد تغییر روند در دوره ۶ ماهه منتهی به ۱۴۰۳/۱۲/۳۰" (blue1)
- Merged header ranges `["F313:G313"]`.
- Yellow description/label cells 18:
  - A315 = "فروش اقساطی "
  - A316 = "جعاله "
  - A317 = "اجاره به شرط تملیک "
  - A318 = "سلف "
  - A319 = "مضاربه "
  - A320 = "مشارکت مدنی "
  - A321 = "خرید دین "
  - A322 = "بدهکاران بابت اعتبارات اسنادی پرداخت شده "
  - A323 = "بدهکاران بابت ضمانت نامه های پرداخت شده "
  - A324 = "تسهیلات ارزی "
  - A325 = "تسهیلات قرض الحسنه "
  - A326 = "سایر درآمد تسهیلات اعطایی "
  - A327 = "جمع درآمد حاصل از تسهیلات اعطایی "
  - A328 = "جایزه سپرده قانونی "
  - A329 = "سود حاصل از سپرده گذاری در بانکها "
  - A330 = "جمع سود حاصل از سپرده گذاری ها "
  - A331 = "درآمد اوراق بدهی و سایر درآمدهای ناشی از سپرده گذاری "
  - A332 = "درآمد حاصل ازتسهیلات اعطایی و سپرده‌گذاری‌ها "
- Gray value cells 18 with same-row yellow label(s):
  - D315 = 2134924 (type n; label A315 "فروش اقساطی ")
  - D316 = 613663 (type n; label A316 "جعاله ")
  - D317 = 0 (type n; label A317 "اجاره به شرط تملیک ")
  - D318 = 0 (type n; label A318 "سلف ")
  - D319 = 0 (type n; label A319 "مضاربه ")
  - D320 = 10538469 (type n; label A320 "مشارکت مدنی ")
  - D321 = 1610763 (type n; label A321 "خرید دین ")
  - D322 = 6889454 (type n; label A322 "بدهکاران بابت اعتبارات اسنادی پرداخت شده ")
  - D323 = 148563 (type n; label A323 "بدهکاران بابت ضمانت نامه های پرداخت شده ")
  - D324 = 25729592 (type n; label A324 "تسهیلات ارزی ")
  - D325 = 0 (type n; label A325 "تسهیلات قرض الحسنه ")
  - D326 = 82315994 (type n; label A326 "سایر درآمد تسهیلات اعطایی ")
  - D327 = 129981422 (type n; label A327 "جمع درآمد حاصل از تسهیلات اعطایی ")
  - D328 = 1422354 (type n; label A328 "جایزه سپرده قانونی ")
  - D329 = 4580248 (type n; label A329 "سود حاصل از سپرده گذاری در بانکها ")
  - D330 = 6002602 (type n; label A330 "جمع سود حاصل از سپرده گذاری ها ")
  - D331 = 11202306 (type n; label A331 "درآمد اوراق بدهی و سایر درآمدهای ناشی از سپرده گذاری ")
  - D332 = 147186330 (type n; label A332 "درآمد حاصل ازتسهیلات اعطایی و سپرده‌گذاری‌ها ")
- Black/dark excluded cells 40 coordinates `["B313", "C313", "B314", "C314", "B315", "C315", "B316", "C316", "B317", "C317", "B318", "C318", "B319", "C319", "B320", "C320", "B321", "C321", "B322", "C322", "B323", "C323", "B324", "C324", "B325", "C325", "B326", "C326", "B327", "C327", "B328", "C328", "B329", "C329", "B330", "C330", "B331", "C331", "B332", "C332"]`.
  - Physical columns ["B", "C"]; header text in them `[]`.
- Green sub-table names 1:
  - A314 = "درآمد تسهیلات اعطایی: "; relative row 2; physical column A; exact sub-table bounds unresolved.
- Other/unfilled cells 59 coordinates `["G313", "D314", "E314", "F314", "G314", "E315", "F315", "G315", "E316", "F316", "G316", "E317", "F317", "G317", "E318", "F318", "G318", "E319", "F319", "G319", "E320", "F320", "G320", "E321", "F321", "G321", "E322", "F322", "G322", "E323", "F323", "G323", "E324", "F324", "G324", "E325", "F325", "G325", "E326", "F326", "G326", "E327", "F327", "G327", "E328", "F328", "G328", "E329", "F329", "G329", "E330", "F330", "G330", "E331", "F331", "G331", "E332", "F332", "G332"]`.
- Yellow with no same-row gray: `[]`.
- Gray with no same-row yellow: `[]`.

### Candidate 11: Recovered_Sheet1!A336:E340

- Bounds A336 through E340; 5 rows ? 5 columns.
- Red name A334 = "خالص سود (زیان) سرمایه گذاری‌ ها"; distance 2 row(s); fill `{"fill_type": "solid", "color_type": "rgb", "rgb": "FFFF0000", "theme": null, "indexed": null, "tint": 0.0}`.
- Thick outline not confirmed; medium edge properties `{"top": {"styles": {"medium": 5}, "gaps": 0}, "bottom": {"styles": {"medium": 5}, "gaps": 0}, "left": {"styles": {"medium": 5}, "gaps": 0}, "right": {"styles": {"medium": 5}, "gaps": 0}}`.
- Merged ranges: `D337:E337`, `D339:E339`, `D336:E336`, `D338:E338`, `D340:E340`.
- Blue header cells 3 on rows [336]:
  - A336 = "شرح" (blue1)
  - C336 = "دوره ۶ ماهه منتهی به ۱۴۰۳/۰۶/۳۱" (blue1)
  - D336 = "برآورد تغییر روند در دوره ۶ ماهه منتهی به ۱۴۰۳/۱۲/۳۰" (blue1)
- Merged header ranges `["D336:E336"]`.
- Yellow description/label cells 3:
  - A337 = "درآمد حاصل از سرمایه گذاری در سهام "
  - A338 = "سود(زیان) حاصل از فروش سرمایه گذاری "
  - A339 = "سود (زیان) تعدیل ذخیره کاهش ارزش سرمایه گذاریها "
- Gray value cells 3 with same-row yellow label(s):
  - C337 = 402420 (type n; label A337 "درآمد حاصل از سرمایه گذاری در سهام ")
  - C338 = 0 (type n; label A338 "سود(زیان) حاصل از فروش سرمایه گذاری ")
  - C339 = 0 (type n; label A339 "سود (زیان) تعدیل ذخیره کاهش ارزش سرمایه گذاریها ")
- Black/dark excluded cells 4 coordinates `["B336", "B337", "B338", "B339"]`.
  - Physical columns ["B"]; header text in them `[]`.
- Green sub-table names 0:
- Other/unfilled cells 12 coordinates `["E336", "D337", "E337", "D338", "E338", "D339", "E339", "A340", "B340", "C340", "D340", "E340"]`.
- Yellow with no same-row gray: `[]`.
- Gray with no same-row yellow: `[]`.

### Candidate 12: Recovered_Sheet1!A353:K358

- Bounds A353 through K358; 6 rows ? 11 columns.
- Red name A351 = "وضعیت شرکتهای سرمایه پذیر:"; distance 2 row(s); fill `{"fill_type": "solid", "color_type": "rgb", "rgb": "FFFF0000", "theme": null, "indexed": null, "tint": 0.0}`.
- Thick outline not confirmed; medium edge properties `{"top": {"styles": {"medium": 11}, "gaps": 0}, "bottom": {"styles": {"medium": 11}, "gaps": 0}, "left": {"styles": {"medium": 6}, "gaps": 0}, "right": {"styles": {"medium": 6}, "gaps": 0}}`.
- Merged ranges: `A355:B355`, `J353:K354`, `J358:K358`, `C353:F353`, `J356:K356`, `G353:I353`, `A356:B356`, `A353:B354`, `A358:B358`, `J355:K355`, `J357:K357`, `A357:B357`.
- Blue header cells 6 on rows [353, 354]:
  - A353 = "نام شرکت" (blue1)
  - G353 = "دوره ۶ ماهه منتهي به ۱۴۰۳/۰۶/۳۱" (blue1)
  - J353 = "تشريح آخرين وضعيت و برنامه هاي آتي شرکت در شرکت سرمايه پذير" (blue1)
  - G354 = "درصد مالکيت" (blue1)
  - H354 = "بهاي تمام شده" (blue1)
  - I354 = "درآمد سرمايه گذاري" (blue1)
- Merged header ranges `["J353:K354", "G353:I353", "A353:B354"]`.
- Yellow description/label cells 4:
  - A355 = "صرافي پارسيان "
  - A356 = "ساير شرکتهاي خارج از بورس "
  - A357 = "گروه داده پردازي پارسيان "
  - A358 = "گروه مالي بانک پارسيان "
- Gray value cells 12 with same-row yellow label(s):
  - G355 = 79 (type n; label A355 "صرافي پارسيان ")
  - H355 = 1191004 (type n; label A355 "صرافي پارسيان ")
  - I355 = 0 (type n; label A355 "صرافي پارسيان ")
  - G356 = 1 (type n; label A356 "ساير شرکتهاي خارج از بورس ")
  - H356 = 122338363 (type n; label A356 "ساير شرکتهاي خارج از بورس ")
  - I356 = 0 (type n; label A356 "ساير شرکتهاي خارج از بورس ")
  - G357 = 100 (type n; label A357 "گروه داده پردازي پارسيان ")
  - H357 = 36279443 (type n; label A357 "گروه داده پردازي پارسيان ")
  - I357 = 0 (type n; label A357 "گروه داده پردازي پارسيان ")
  - G358 = 100 (type n; label A358 "گروه مالي بانک پارسيان ")
  - H358 = 45109293 (type n; label A358 "گروه مالي بانک پارسيان ")
  - I358 = 0 (type n; label A358 "گروه مالي بانک پارسيان ")
- Black/dark excluded cells 21 coordinates `["C353", "C354", "D354", "E354", "F354", "C355", "D355", "E355", "F355", "C356", "D356", "E356", "F356", "C357", "D357", "E357", "F357", "C358", "D358", "E358", "F358"]`.
  - Physical columns ["C", "D", "E", "F"]; header text in them `[]`.
- Green sub-table names 0:
- Other/unfilled cells 23 coordinates `["B353", "D353", "E353", "F353", "H353", "I353", "K353", "A354", "B354", "J354", "K354", "B355", "J355", "K355", "B356", "J356", "K356", "B357", "J357", "K357", "B358", "J358", "K358"]`.
- Yellow with no same-row gray: `[]`.
- Gray with no same-row yellow: `[]`.

### Candidate 13: Recovered_Sheet1!A361:C367

- Bounds A361 through C367; 7 rows ? 3 columns.
- Red name A359 = "ساير درآمدها و هزینه های عملياتي:"; distance 2 row(s); fill `{"fill_type": "solid", "color_type": "rgb", "rgb": "FFFF0000", "theme": null, "indexed": null, "tint": 0.0}`.
- Thick outline not confirmed; medium edge properties `{"top": {"styles": {"medium": 3}, "gaps": 0}, "bottom": {"styles": {"medium": 3}, "gaps": 0}, "left": {"styles": {"medium": 7}, "gaps": 0}, "right": {"styles": {"medium": 7}, "gaps": 0}}`.
- Merged ranges: none.
- Blue header cells 2 on rows [361]:
  - A361 = "شرح" (blue1)
  - C361 = "۱۴۰۳/۰۶/۳۱" (blue1)
- Merged header ranges `[]`.
- Yellow description/label cells 3:
  - A363 = "ساير درآمدهاي عملياتي "
  - A365 = "جمع ساير درآمدهاي عملياتي "
  - A367 = "ساير هزينه هاي عملياتي "
- Gray value cells 3 with same-row yellow label(s):
  - C363 = 84513662 (type n; label A363 "ساير درآمدهاي عملياتي ")
  - C365 = 84513662 (type n; label A365 "جمع ساير درآمدهاي عملياتي ")
  - C367 = 0 (type n; label A367 "ساير هزينه هاي عملياتي ")
- Black/dark excluded cells 7 coordinates `["B361", "B362", "B363", "B364", "B365", "B366", "B367"]`.
  - Physical columns ["B"]; header text in them `[]`.
- Green sub-table names 2:
  - A362 = "ساير درآمدهاي عملياتي: "; relative row 2; physical column A; exact sub-table bounds unresolved.
  - A366 = "ساير هزينه هاي عملياتي: "; relative row 6; physical column A; exact sub-table bounds unresolved.
- Other/unfilled cells 4 coordinates `["C362", "A364", "C364", "C366"]`.
- Yellow with no same-row gray: `[]`.
- Gray with no same-row yellow: `[]`.

### Candidate 14: Recovered_Sheet1!A376:C378

- Bounds A376 through C378; 3 rows ? 3 columns.
- Red name A374 = "خالص ساير درآمدها و هزینه ها:"; distance 2 row(s); fill `{"fill_type": "solid", "color_type": "rgb", "rgb": "FFFF0000", "theme": null, "indexed": null, "tint": 0.0}`.
- Thick outline not confirmed; medium edge properties `{"top": {"styles": {"medium": 3}, "gaps": 0}, "bottom": {"styles": {"medium": 3}, "gaps": 0}, "left": {"styles": {"medium": 3}, "gaps": 0}, "right": {"styles": {"medium": 3}, "gaps": 0}}`.
- Merged ranges: none.
- Blue header cells 2 on rows [376]:
  - A376 = "خالص ساير درآمدها و هزينه ها" (blue1)
  - C376 = "۱۴۰۳/۰۶/۳۱" (blue1)
- Merged header ranges `[]`.
- Yellow description/label cells 2:
  - A377 = "ساير درامدها "
  - A378 = "ساير هزينه ها "
- Gray value cells 2 with same-row yellow label(s):
  - C377 = 2192360 (type n; label A377 "ساير درامدها ")
  - C378 = 0 (type n; label A378 "ساير هزينه ها ")
- Black/dark excluded cells 3 coordinates `["B376", "B377", "B378"]`.
  - Physical columns ["B"]; header text in them `[]`.
- Green sub-table names 0:
- Other/unfilled cells 0 coordinates `[]`.
- Yellow with no same-row gray: `[]`.
- Gray with no same-row yellow: `[]`.

### Candidate 15: Recovered_Sheet1!A386:C387

- Bounds A386 through C387; 2 rows ? 3 columns.
- Red name A384 = "هزینه های اداری و عمومی:"; distance 2 row(s); fill `{"fill_type": "solid", "color_type": "rgb", "rgb": "FFFF0000", "theme": null, "indexed": null, "tint": 0.0}`.
- Thick outline not confirmed; medium edge properties `{"top": {"styles": {"medium": 3}, "gaps": 0}, "bottom": {"styles": {"medium": 3}, "gaps": 0}, "left": {"styles": {"medium": 2}, "gaps": 0}, "right": {"styles": {"medium": 2}, "gaps": 0}}`.
- Merged ranges: none.
- Blue header cells 2 on rows [386]:
  - A386 = "هزينه هاي اداري و عمومي" (blue1)
  - C386 = "۱۴۰۳/۰۶/۳۱" (blue1)
- Merged header ranges `[]`.
- Yellow description/label cells 1:
  - A387 = "هزينه هاي اداري و عمومي "
- Gray value cells 1 with same-row yellow label(s):
  - C387 = -28908689 (type n; label A387 "هزينه هاي اداري و عمومي ")
- Black/dark excluded cells 2 coordinates `["B386", "B387"]`.
  - Physical columns ["B"]; header text in them `[]`.
- Green sub-table names 0:
- Other/unfilled cells 0 coordinates `[]`.
- Yellow with no same-row gray: `[]`.
- Gray with no same-row yellow: `[]`.

### Candidate 16: Recovered_Sheet1!A395:C399

- Bounds A395 through C399; 5 rows ? 3 columns.
- Red name A393 = "هزینه مالی:"; distance 2 row(s); fill `{"fill_type": "solid", "color_type": "rgb", "rgb": "FFFF0000", "theme": null, "indexed": null, "tint": 0.0}`.
- Thick outline not confirmed; medium edge properties `{"top": {"styles": {"thin": 3}, "gaps": 0}, "bottom": {"styles": {"medium": 3}, "gaps": 0}, "left": {"styles": {"thin": 4, "medium": 1}, "gaps": 0}, "right": {"styles": {"thin": 4, "medium": 1}, "gaps": 0}}`.
- Merged ranges: none.
- Blue header cells 2 on rows [395]:
  - A395 = "هزينه‌هاي مالي" (blue1)
  - C395 = "۱۴۰۳/۰۶/۳۱" (blue1)
- Merged header ranges `[]`.
- Yellow description/label cells 3:
  - A396 = "هزينه مالي تسهيلات دريافتي از ساير بانکها و موسسات اعتباري "
  - A397 = "جريمه اضافه برداشت از بانک مرکزي "
  - A398 = "ساير هزينه هاي مالي "
- Gray value cells 3 with same-row yellow label(s):
  - C396 = 0 (type n; label A396 "هزينه مالي تسهيلات دريافتي از ساير بانکها و موسسات اعتباري ")
  - C397 = 0 (type n; label A397 "جريمه اضافه برداشت از بانک مرکزي ")
  - C398 = -5804157 (type n; label A398 "ساير هزينه هاي مالي ")
- Black/dark excluded cells 4 coordinates `["B395", "B396", "B397", "B398"]`.
  - Physical columns ["B"]; header text in them `[]`.
- Green sub-table names 0:
- Other/unfilled cells 3 coordinates `["A399", "B399", "C399"]`.
- Yellow with no same-row gray: `[]`.
- Gray with no same-row yellow: `[]`.

### Candidate 17: Recovered_Sheet1!A404:E405

- Bounds A404 through E405; 2 rows ? 5 columns.
- Red name A403 = "برنامه شرکت در خصوص تقسیم سود"; distance 1 row(s); fill `{"fill_type": "solid", "color_type": "rgb", "rgb": "FFFF0000", "theme": null, "indexed": null, "tint": 0.0}`.
- Thick outline not confirmed; medium edge properties `{"top": {"styles": {"thin": 5}, "gaps": 0}, "bottom": {"styles": {"thin": 5}, "gaps": 0}, "left": {"styles": {"thin": 2}, "gaps": 0}, "right": {"styles": {"thin": 2}, "gaps": 0}}`.
- Merged ranges: none.
- Blue header cells 5 on rows [404]:
  - A404 = "مبلغ سود (زيان) انباشته پايان سال مالي گذشته" (blue1)
  - B404 = "سود سهام پيشنهادي هيئت مديره در سال مالي گذشته" (blue1)
  - C404 = "مبلغ سود (زيان) خالص سال مالي گذشته" (blue1)
  - D404 = "سود سهام مصوب مجمع سال مالي گذشته" (blue1)
  - E404 = "پيشنهاد هيئت مديره درخصوص درصد تقسيم سود سال مالي جاري" (blue1)
- Merged header ranges `[]`.
- Yellow description/label cells 0:
- Gray value cells 5 with same-row yellow label(s):
  - A405 = -44764295 (type n; label NO SAME-ROW YELLOW LABEL)
  - B405 = 0 (type n; label NO SAME-ROW YELLOW LABEL)
  - C405 = -9124895 (type n; label NO SAME-ROW YELLOW LABEL)
  - D405 = 0 (type n; label NO SAME-ROW YELLOW LABEL)
  - E405 = 0 (type n; label NO SAME-ROW YELLOW LABEL)
- Black/dark excluded cells 0 coordinates `[]`.
  - Physical columns []; header text in them `[]`.
- Green sub-table names 0:
- Other/unfilled cells 0 coordinates `[]`.
- Yellow with no same-row gray: `[]`.
- Gray with no same-row yellow: `["A405", "B405", "C405", "D405", "E405"]`.

### Candidate 18: Sheet1!A16:E24

- Bounds A16 through E24; 9 rows ? 5 columns.
- Red name A14 = "صورت سود و زیان جامع"; distance 2 row(s); fill `{"fill_type": "solid", "color_type": "rgb", "rgb": "FFFF0000", "theme": null, "indexed": null, "tint": 0.0}`.
- Thick outline not confirmed; medium edge properties `{"top": {"styles": {"medium": 5}, "gaps": 0}, "bottom": {"styles": {"medium": 5}, "gaps": 0}, "left": {"styles": {"medium": 9}, "gaps": 0}, "right": {"styles": {"medium": 9}, "gaps": 0}}`.
- Merged ranges: `A16:A17`, `E16:E17`.
- Blue header cells 8 on rows [16, 17]:
  - A16 = "شرح" (blue1)
  - B16 = "دوره منتهي به ۱۴۰۳/۰۶/۳۱" (blue1)
  - C16 = "تجدید ارائه شده ۱۴۰۲/۰۶/۳۱" (blue1)
  - D16 = "تجدید ارائه شده ۱۴۰۲/۱۲/۲۹" (blue1)
  - E16 = "درصد تغییر" (blue1)
  - B17 = "حسابرسی نشده" (blue1)
  - C17 = "حسابرسی شده" (blue1)
  - D17 = "حسابرسی شده" (blue1)
- Merged header ranges `["A16:A17", "E16:E17"]`.
- Yellow description/label cells 0:
- Gray value cells 0 with same-row yellow label(s):
- Black/dark excluded cells 0 coordinates `[]`.
  - Physical columns []; header text in them `[]`.
- Green sub-table names 1:
  - A19 = "سایر اقلام سود و زیان جامع: "; relative row 4; physical column A; exact sub-table bounds unresolved.
- Other/unfilled cells 36 coordinates `["A17", "E17", "A18", "B18", "C18", "D18", "E18", "B19", "C19", "D19", "E19", "A20", "B20", "C20", "D20", "E20", "A21", "B21", "C21", "D21", "E21", "A22", "B22", "C22", "D22", "E22", "A23", "B23", "C23", "D23", "E23", "A24", "B24", "C24", "D24", "E24"]`.
- Yellow with no same-row gray: `[]`.
- Gray with no same-row yellow: `[]`.

### Candidate 19: Recovered_Sheet1!A297:D299

- Bounds A297 through D299; 3 rows ? 4 columns.
- Red name absent; preceding non-red title A295 = "وضعیت کارکنان:".
- Thick outline not confirmed; medium edge properties `{"top": {"styles": {"medium": 4}, "gaps": 0}, "bottom": {"styles": {"medium": 4}, "gaps": 0}, "left": {"styles": {"medium": 3}, "gaps": 0}, "right": {"styles": {"medium": 3}, "gaps": 0}}`.
- Merged ranges: none.
- Blue header cells 4 on rows [297]:
  - A297 = "شرح" (blue1)
  - B297 = "در تاریخ ۱۴۰۲/۱۲/۲۹" (blue1)
  - C297 = "در تاریخ ۱۴۰۳/۰۶/۳۱" (blue1)
  - D297 = "برآورد در تاریخ ۱۴۰۳/۱۲/۳۰" (blue1)
- Merged header ranges `[]`.
- Yellow description/label cells 0:
- Gray value cells 0 with same-row yellow label(s):
- Black/dark excluded cells 0 coordinates `[]`.
  - Physical columns []; header text in them `[]`.
- Green sub-table names 0:
- Other/unfilled cells 8 coordinates `["A298", "B298", "C298", "D298", "A299", "B299", "C299", "D299"]`.
- Yellow with no same-row gray: `[]`.
- Gray with no same-row yellow: `[]`.

## 6. Sub-table inventory

Green fill identifies a name but does not define sub-table bounds; ranges are unresolved without a closed outline. Total names: 16.

| Worksheet | Cell | Text | Candidate | Relative row | Physical column |
|---|---|---|---:|---:|---|
| Recovered_Sheet1 | A12 | "عملیات در حال تداوم: " | 01 | 3 | A |
| Recovered_Sheet1 | A32 | "عملیات متوقف شده: " | 01 | 23 | A |
| Recovered_Sheet1 | A35 | "سود (زیان)پایه هر سهم (ريال) " | 01 | 26 | A |
| Recovered_Sheet1 | A63 | "سایر اقلام سود و زیان جامع: " | 02 | 4 | A |
| Recovered_Sheet1 | A81 | "دارایی ها " | 03 | 3 | A |
| Recovered_Sheet1 | A96 | "حقوق مالکانه " | 03 | 18 | A |
| Recovered_Sheet1 | A108 | "بدهی‌ها " | 03 | 30 | A |
| Recovered_Sheet1 | A152 | "تغییرات حقوق مالکانه در سال ۱۴۰۳/۰۶/۳۱ " | 04 | 23 | A |
| Recovered_Sheet1 | A178 | "جریان­های نقدی حاصل از فعاليت‌هاي عملياتي: " | 05 | 3 | A |
| Recovered_Sheet1 | A182 | "فعاليت‌هاي سرمایه‌گذاری " | 05 | 7 | A |
| Recovered_Sheet1 | A191 | "فعاليت‌هاي تأمين مالي " | 05 | 16 | A |
| Recovered_Sheet1 | A268 | "سپرده های ریالی: " | 07 | 3 | A |
| Recovered_Sheet1 | A314 | "درآمد تسهیلات اعطایی: " | 10 | 2 | A |
| Recovered_Sheet1 | A362 | "ساير درآمدهاي عملياتي: " | 13 | 2 | A |
| Recovered_Sheet1 | A366 | "ساير هزينه هاي عملياتي: " | 13 | 6 | A |
| Sheet1 | A19 | "سایر اقلام سود و زیان جامع: " | 18 | 4 | A |

## 7. RTL and visual column-order analysis

- `Recovered_Sheet1` rightToLeft=True; visual RTL; yellow cols `["A"]`, gray cols `["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]`, black cols `["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]`.
  - A is physically leftmost and visually rightmost, matching the usual RTL label position.
- `Sheet1` rightToLeft=None; visual LTR/default; yellow cols `[]`, gray cols `[]`, black cols `[]`.

## 8. Structural validation results

- Thick outside-border rule: 0 confirmed; no explicit `thick` side exists.
- Red associations: 17 main-sheet names, one duplicate sample, plus one likely unmarked candidate.
- Blue cells outside red-associated candidate ranges: `[["Recovered_Sheet1", "A297", "شرح", "FF0197C8"], ["Recovered_Sheet1", "B297", "در تاریخ ۱۴۰۲/۱۲/۲۹", "FF0197C8"], ["Recovered_Sheet1", "C297", "در تاریخ ۱۴۰۳/۰۶/۳۱", "FF0197C8"], ["Recovered_Sheet1", "D297", "برآورد در تاریخ ۱۴۰۳/۱۲/۳۰", "FF0197C8"]]`; these are the four blue headers in the unmarked candidate `Recovered_Sheet1!A297:D299`.
- Overlaps `[]`.
- Incomplete medium perimeter A79:E119: {"top": {"styles": {"medium": 4, "null": 1}, "gaps": 1}, "bottom": {"styles": {"medium": 4, "null": 1}, "gaps": 1}}.
- Yellow/gray row mismatches are listed per candidate; black/dark cells are excluded. Sheet1 sample lacks yellow/gray/black fills.

Other bordered cells outside candidates:
- Recovered_Sheet1: `["A1", "B1", "C1", "D1", "E1", "F1", "G1", "H1", "I1", "J1", "K1", "L1", "A5", "B5", "C5", "D5", "E5", "F5", "G5", "H5", "I5", "J5", "K5", "L5", "A44", "B44", "C44", "D44", "E44", "A45", "B45", "C45", "D45", "E45", "A46", "B46", "C46", "D46", "E46", "A47", "B47", "C47", "D47", "E47", "A48", "B48", "C48", "D48", "E48", "A49", "B49", "C49", "D49", "E49", "A51", "B51", "C51", "D51", "E51", "F51", "G51", "H51", "I51", "J51", "K51", "L51", "A55", "B55", "C55", "D55", "E55", "F55", "G55", "H55", "I55", "J55", "K55", "L55", "A58", "A59", "A70", "B70", "C70", "D70", "E70", "F70", "G70", "H70", "I70", "J70", "K70", "L70", "A74", "B74", "C74", "D74", "E74", "F74", "G74", "H74", "I74", "J74", "K74", "L74", "A121", "B121", "C121", "D121", "E121", "F121", "G121", "H121", "I121", "J121", "K121", "L121", "A125", "B125", "C125", "D125", "E125", "F125", "G125", "H125", "I125", "J125", "K125", "L125", "A167", "B167", "C167", "D167", "E167", "F167", "G167", "H167", "I167", "J167", "K167", "L167", "A171", "B171", "C171", "D171", "E171", "F171", "G171", "H171", "I171", "J171", "K171", "L171", "A221", "B221", "C221", "D221", "E221", "A222", "B222", "C222", "D222", "E222", "A223", "B223", "C223", "D223", "E223", "A224", "B224", "C224", "D224", "E224", "A225", "B225", "C225", "D225", "E225", "A226", "B226", "C226", "D226", "E226", "A228", "B228", "C228", "D228", "E228", "F228", "G228", "H228", "I228", "J228", "K228", "L228", "A232", "B232", "C232", "D232", "E232", "F232", "G232", "H232", "I232", "J232", "K232", "L232", "A235", "B235", "C235", "D235", "E235", "F235", "G235", "H235", "I235", "J235", "K235", "A256", "B256", "C256", "D256", "E256", "F256", "G256", "H256", "I256", "A259", "B259", "C259", "D259", "E259", "F259", "G259", "H259", "I259", "A262", "B262", "C262", "D262", "E262", "F262", "G262", "H262", "I262", "A276", "B276", "C276", "D276", "E276", "F276", "G276", "H276", "I276", "J276", "A285", "B285", "C285", "D285", "E285", "F285", "G285", "H285", "I285", "A287", "B287", "C287", "D287", "E287", "F287", "G287", "H287", "I287", "J287", "K287", "L287", "A291", "B291", "C291", "D291", "E291", "F291", "G291", "H291", "I291", "J291", "K291", "L291", "A294", "B294", "C294", "D294", "E294", "F294", "G294", "H294", "I294", "J294", "K294", "A310", "B310", "C310", "D310", "E310", "F310", "G310", "A333", "B333", "C333", "D333", "E333", "F333", "G333", "H333", "I333", "A341", "B341", "C341", "D341", "E341", "F341", "G341", "A343", "B343", "C343", "D343", "E343", "F343", "G343", "H343", "I343", "J343", "K343", "L343", "A347", "B347", "C347", "D347", "E347", "F347", "G347", "H347", "I347", "J347", "K347", "L347", "A350", "B350", "C350", "D350", "E350", "F350", "G350", "H350", "I350", "J350", "K350", "A369", "B369", "C369", "A370", "B370", "C370", "A372", "B372", "C372", "D372", "E372", "F372", "A380", "B380", "C380", "A382", "B382", "C382", "D382", "E382", "F382", "A389", "B389", "C389", "A391", "B391", "C391", "D391", "E391", "F391", "A401", "B401", "C401", "D401", "E401", "F401", "A407", "B407", "C407", "D407", "E407", "A410", "B410", "C410", "D410", "E410", "F410", "G410", "H410", "I410", "A411", "B411", "C411", "D411", "E411", "F411", "G411", "H411", "I411"]`.
- Sheet1: `["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10", "A11", "A12"]`.

## 9. Exceptions and unresolved ambiguities

- No explicit thick border exists, so formal bounds cannot be confirmed under the stated rule.
- `Recovered_Sheet1!A79:E119` has top/bottom medium-border gaps at column D.
- `Recovered_Sheet1!A297:D299` looks like a table with blue/yellow/gray cells, but its preceding title A295 is not red.
- `Sheet1!A16:E24` is a duplicate sample with incomplete semantic fills.
- Four blue cells are outside red-associated ranges; all four are the header row of the unmarked candidate `Recovered_Sheet1!A297:D299`.
- Two theme-1 dark shades are counted separately and excluded. Green sub-table names have no separately closed bounds; some blue header text is dark-filled.

## 10. Final assessment

**The workbook is not sufficiently annotated for a deterministic Company Table Layout Template under the authoritative convention.** Seventeen red-named main-sheet candidates exist, but none has the required explicit `thick` border. One likely table lacks a red name; one medium outline has gaps; blue headers sit outside associated ranges or use dark fills; and green sub-table extents are unresolved.

## Method and scope

Read-only inspection of worksheet used ranges, RTL flags, merged ranges, fill metadata, values/types, formulas, and border sides. Red-associated medium-border ranges are recorded as candidates, not silently upgraded to confirmed thick-bordered tables. Workbook and source code were not modified.

## 14. Owner clarification and interpretation (2026-11-16)

The following owner clarifications supersede any tentative interpretation in this audit report. The report's raw observations (cell coordinates, color metadata, and observed border styles) remain evidence; its candidate classifications are not authoritative where they conflict with these rules.

- `Recovered_Sheet1!A297:D299` is not an extractable table: it has no colored cells and requires no extraction. A blue/header-like appearance alone is insufficient; an eligible table must also contain gray extraction cells and have a recognizable table border.
- `Sheet1!A16:E24` is an independent valid table, not a duplicate. It remains in the Parsian periodic template.
- The report's `black/dark excluded` grouping refers to the owner's black excluded columns. There is no separate dark-fill semantic category in this workbook. Preserve raw color metadata, but do not invent a distinct role for the dark grouping.
- The final table is a valid owner-approved exception without a yellow description column. Its lack of a yellow label column must not cause rejection.
- Cells without an annotation color are not extracted, even when they fall inside a table's geometric bounds. Black cells/columns are also excluded. Gray cells are the positive extraction signal.
- A border need not have the literal Excel style token `thick`. The owner's criterion is a visible/non-default border that distinguishes the table boundary from ordinary cell grid borders. The report's zero literal-thick count does not invalidate the observed medium-style boundary candidates. Preserve exact border styles and coordinates in the template.
- Green cells identify sub-table names. In the table's reading order, the yellow description column immediately after a green marker begins that sub-table's label region; it continues until the next green marker or the parent table's end. The exact sub-table ranges still need to be recorded from the standardized sample.

Accordingly, this audit is evidence for template authoring, not an automatic table inventory. No template bounds are approved solely by this report. The owner-confirmed table list and exact green-marker sub-table ranges must be transcribed into the versioned template.


## 15. Provisional sub-table bounds and unresolved Sheet1 extraction annotation (2026-11-16)

Applying the owner-confirmed green-marker rule to the parent candidate bounds yields the following provisional partitions. The green marker row is the sub-table title row; data-label rows begin immediately below it. Each partition inherits the parent's column bounds and ends immediately before the next green marker, or at the parent table's last row.

| Parent candidate | Green marker | Provisional sub-table bounds | Data-label rows |
|---|---|---|---|
| 01 `A10:E42` | A12 | `A12:E31` | 13:31 |
| 01 `A10:E42` | A32 | `A32:E34` | 33:34 |
| 01 `A10:E42` | A35 | `A35:E42` | 36:42 |
| 02 `A60:E68` | A63 | `A63:E68` | 64:68 |
| 03 `A79:E119` | A81 | `A81:E94` | 82:94 |
| 03 `A79:E119` | A96 | `A96:E107` | 97:107 |
| 03 `A79:E119` | A108 | `A108:E119` | 109:119 |
| 04 `A130:L165` | A152 | `A152:L165` | 153:165 |
| 05 `A176:E213` | A178 | `A178:E181` | 179:181 |
| 05 `A176:E213` | A182 | `A182:E190` | 183:190 |
| 05 `A176:E213` | A191 | `A191:E213` | 192:213 |
| 07 `A266:F275` | A268 | `A268:F275` | 269:275 |
| 10 `A313:G332` | A314 | `A314:G332` | 315:332 |
| 13 `A361:C367` | A362 | `A362:C365` | 363:365 |
| 13 `A361:C367` | A366 | `A366:C367` | 367:367 |

These are mechanically derived candidate ranges, not owner-approved final coordinates. They must be checked against the standardized workbook before template approval.

### Sheet1 independent region — extraction annotation conflict

The owner confirmed that `Sheet1!A16:E24` is an independent region and not a duplicate. The current audit, however, reports 8 blue header cells and one green marker at A19, but zero yellow cells and zero gray extraction cells; its other cells are uncolored. Under the owner's explicit rule that uncolored cells are never extracted and an extractable table requires gray value cells, this region currently has no approved extraction cells. Retain the region as independently identified, but do not extract its uncolored contents. Clarification is required whether it is intentionally structural-only/empty in this sample or whether the intended value cells still need gray annotation.
