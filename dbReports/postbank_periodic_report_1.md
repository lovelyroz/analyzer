# Postbank Quarterly Workbook Inspection — DB-STD-003

> **Source/title discrepancy:** The required title says Parsian, while the inspected file is `postbank_periodic.xlsx`; workbook title and subject metadata are blank. The title is retained as required. Findings describe this Postbank-named file; issuer identity needs confirmation.

## 1. Executive summary

The workbook contains one worksheet with primary financial statements and three pages of management interpretive disclosures. Income, comprehensive income and cash-flow statements compare current period ending at the date in B10/B60/B176 with restated prior-year comparable period and restated prior full year (headers C10:D10, C60:D60, C176:D176). Supplemental headers explicitly identify current nine-month values (C302, D313, C336). The best-supported interpretation is current nine-month YTD, prior-year nine-month YTD, and prior full year. No actual standalone-quarter value column is identified. The balance sheet presents point-in-time balances at the dates in B79:D79. Supplementary tables mix balances, flows, forecasts, rates, counts, ratios and narrative.

## 2. Workbook inventory

| File/format | Worksheet order and state | Used range | Structure |
|---|---|---|---|
| `postbank_periodic.xlsx` / XLSX | 1. `Recovered_Sheet1` — visible | `A1:L416` (416 x 12) | 158 merged ranges; no formulas, named ranges, hidden rows/columns, charts or images; no freeze panes. |

Workbook title and subject are blank; creator is Papa; created/modified properties are 2026-11-12. The sheet contains one report package. The recovered sheet name suggests a recovery/export, but completeness cannot be established from this file alone. The 158 merged ranges chiefly affect layout; they are not individually listed.

## 3. Report identity and period evidence

| Topic | Evidence and conclusion |
|---|---|
| Issuer/ticker | Filename says Postbank. Investee names at A361 and A363 refer to Postbank-related entities, but do not prove reporting-issuer identity. No verified issuer/ticker appears in metadata. Confirm against filing cover/exchange record. |
| Report type | Quarterly Financial Report sample per task; content is an interim nine-month package with management forecasts. No explicit report-type field found. |
| Current reporting date | Persian/Jalali date is preserved in B10, B60, B79 and B176. |
| Current flow duration | Nine months is explicit in C302, D313 and C336; core flow headers omit duration. Aligned supplemental labels support nine-month YTD, but no standalone-quarter figures are shown. |
| Flow comparatives | C10:D10, C60:D60 and C176:D176 label restated prior comparative and prior full-year periods. Supplemental evidence identifies the prior comparable as nine months. |
| Balance comparatives | C79:D79 show restated prior year-end and prior-year opening dates; both are point-in-time values. |
| Fiscal basis | Equity rows A131 and A151 show opening and closing dates for the represented year. This supports the source's year-start/year-end labels only; do not convert to Gregorian or generalize. |
| Restatement | Restated wording occurs in comparative headers and equity rows A134/A151. Reasons and adjustment bridges are absent. |

## 4. Financial statement and major-table inventory

| Worksheet range | Table | Structure, data and temporal/unit evidence |
|---|---|---|
| A3:E48, title A8 | Income statement | Row labels A; B:D values; E change percentage; data rows 12-42; explanation headings 44, 46, 48. Million rials at A9; current nine-month package, prior nine months, prior full year; statuses row 11. Net income row 34; EPS in rial/share row 41; capital row 42. |
| A53:E68, title A58 | Comprehensive income | Components rows 62-67; total row 68; same periods/status pattern; million rials at A59. Net income row 62 ties to income statement row 34; annual comprehensive total differs due to OCI. |
| A72:E119, title A77 | Statement of financial position | Assets/liabilities/equity rows 81-119; point-in-time dates B:D; million rials at A78; status row 80. Assets total row 94; equity row 107; liabilities subtotals 116/118; balancing total 119. |
| A123:L165, title A128 | Changes in equity | Components B:K and total L; rows 131-165; million rials at A129. Opening, restated opening, movements, prior close and current-period close; column headers row 130. |
| A169:E225, title A174 | Cash flows | Rows 178-213; values B:D, change E; explanatory headings 221/223/225; million rials at A175. Same flow-period/status pattern. Opening/change/FX/closing cash rows 209-212; 'year' wording is imprecise for nine-month columns. |
| A230:K285 | Management disclosures, page 1 | Summary/limitation (A230/A235); loan balances/reserves (A236:A254); rate/policy estimates (A255:A262); deposits (A264:A276); off-balance items (A277:A283); material-change note (A284:A285). Monetary tables specify million rials; balances and forward-looking narrative coexist. |
| A289:F341 | Management disclosures, page 2 | Summary/limitation (A289/A294); employee/branch counts (A295:A299); fee/capital adequacy (A300:A308); strategy (A309:A310); lending/deposit income and rates (A311:A333); investment profit/loss (A334:A341). Mixed annual, nine-month, forecast, ratio and count fields. |
| A345:L416 | Management disclosures, page 3 | Summary/limitation (A345/A350); investees (A351:A363); operating income/expenses (A364:A377); net other income/expenses (A378:A388); admin expenses (A389:A397); finance costs (A398:A407); dividend plan (A408:A410); other plans (A411:A413); explanations (A414:A416). Mixed monetary, percentage, date, narrative and forecast fields. |

Key relationships: net income B34:D34 repeats in comprehensive-income row 62; assets total row 94 equals liabilities/equity row 119; ending equity L165 ties to balance-sheet B107. Current cash reconciles: B210 (opening 39,678,831) + B209 (change 12,262,969) + B211 (FX 0) = B212 (closing 51,941,800), which ties to balance-sheet cash. Cash labels say beginning/end of year even in nine-month columns.

## 5. Complete source Header/text inventory

The source has many multi-level headers, labels and narrative cells. This appendix indexes every nonempty textual cell (486 total) with exact worksheet address and original text, grouped by row. It includes row/column headers, subheaders, units, titles, footnotes and narrative; numeric-only cells are not headers. Role follows section 4 context. Persian wording, spelling and digits are copied directly from the workbook. Merged blank cells are omitted.


**`Recovered_Sheet1`, row 3:**
- `A3` — صورت سود و زیان

**`Recovered_Sheet1`, row 8:**
- `A8` — صورت سود و زیان

**`Recovered_Sheet1`, row 9:**
- `A9` — کلیه مبالغ درج شده به میلیون ریال می باشد

**`Recovered_Sheet1`, row 10:**
- `A10` — شرح
- `B10` — دوره منتهي به ۱۴۰۱/۰۹/۳۰
- `C10` — تجدید ارائه شده ۱۴۰۰/۰۹/۳۰
- `D10` — تجدید ارائه شده ۱۴۰۰/۱۲/۲۹
- `E10` — درصد تغییرات

**`Recovered_Sheet1`, row 11:**
- `B11` — حسابرسی نشده
- `C11` — حسابرسی نشده
- `D11` — حسابرسی شده

**`Recovered_Sheet1`, row 12:**
- `A12` — عملیات در حال تداوم: 

**`Recovered_Sheet1`, row 13:**
- `A13` — درآمد تسهيلات اعطايي و سپرده گذاری و اوراق بدهی 

**`Recovered_Sheet1`, row 14:**
- `A14` — هزينه سود سپرده‌ها 

**`Recovered_Sheet1`, row 15:**
- `A15` — خالص درآمد تسهیلات و سپرده گذاری 

**`Recovered_Sheet1`, row 16:**
- `A16` — درآمد کارمزد 

**`Recovered_Sheet1`, row 17:**
- `A17` — هزينه کارمزد 

**`Recovered_Sheet1`, row 18:**
- `A18` — خالص درآمد کارمزد 

**`Recovered_Sheet1`, row 19:**
- `A19` — خالص سود (زیان) سرمایه گذاری‌ها 

**`Recovered_Sheet1`, row 20:**
- `A20` — خالص سود (زيان) مبادلات و معاملات ارزي 

**`Recovered_Sheet1`, row 21:**
- `A21` — ساير درآمدها و هزینه های عملياتي 

**`Recovered_Sheet1`, row 22:**
- `A22` — جمع درآمدهاي عملياتي 

**`Recovered_Sheet1`, row 23:**
- `A23` — خالص ساير درآمدها و هزینه‌ها 

**`Recovered_Sheet1`, row 24:**
- `A24` — هزينه‌هاي اداري و عمومي 

**`Recovered_Sheet1`, row 25:**
- `A25` — هزينه مطالبات مشکوک الوصول 

**`Recovered_Sheet1`, row 26:**
- `A26` — هزينه‌هاي مالي 

**`Recovered_Sheet1`, row 27:**
- `A27` — هزينه استهلاک 

**`Recovered_Sheet1`, row 28:**
- `A28` — سود(زیان) عملیات در حال تداوم قبل از مالیات 

**`Recovered_Sheet1`, row 29:**
- `A29` — ماليات بر درآمد سال جاری 

**`Recovered_Sheet1`, row 30:**
- `A30` — ماليات بر درآمد سال های قبل 

**`Recovered_Sheet1`, row 31:**
- `A31` — سود (زيان) خالص عملیات در حال تداوم 

**`Recovered_Sheet1`, row 32:**
- `A32` — عملیات متوقف شده: 

**`Recovered_Sheet1`, row 33:**
- `A33` — سود(زیان) خالص عملیات متوقف شده 

**`Recovered_Sheet1`, row 34:**
- `A34` — سود(زیان) خالص 

**`Recovered_Sheet1`, row 35:**
- `A35` — سود (زیان)پایه هر سهم (ريال) 

**`Recovered_Sheet1`, row 36:**
- `A36` — عملياتي (ريال) 

**`Recovered_Sheet1`, row 37:**
- `A37` — غيرعملياتي(ريال) 

**`Recovered_Sheet1`, row 38:**
- `A38` — ناشی از عملیات در حال تداوم(ریال) 

**`Recovered_Sheet1`, row 39:**
- `A39` — ناشي از عمليات متوقف شده(ريال) 

**`Recovered_Sheet1`, row 40:**
- `A40` — سود(زیان) پایه هر سهم (ریال) 

**`Recovered_Sheet1`, row 41:**
- `A41` — سود (زیان) خالص هر سهم– ریال 

**`Recovered_Sheet1`, row 42:**
- `A42` — سرمایه 

**`Recovered_Sheet1`, row 44:**
- `A44` — دلایل تغییرات اطلاعات واقعی دوره منتهی به ۱۴۰۱/۰۹/۳۰ 

**`Recovered_Sheet1`, row 46:**
- `A46` — دلایل تغییرات اطلاعات واقعی دوره منتهی به ۱۴۰۰/۰۹/۳۰ 

**`Recovered_Sheet1`, row 48:**
- `A48` — دلایل تغییرات اطلاعات واقعی دوره منتهی به ۱۴۰۰/۱۲/۲۹ 

**`Recovered_Sheet1`, row 53:**
- `A53` — صورت سود و زیان جامع

**`Recovered_Sheet1`, row 58:**
- `A58` — صورت سود و زیان جامع

**`Recovered_Sheet1`, row 59:**
- `A59` — کلیه مبالغ درج شده به میلیون ریال می باشد

**`Recovered_Sheet1`, row 60:**
- `A60` — شرح
- `B60` — دوره منتهي به ۱۴۰۱/۰۹/۳۰
- `C60` — تجدید ارائه شده ۱۴۰۰/۰۹/۳۰
- `D60` — تجدید ارائه شده ۱۴۰۰/۱۲/۲۹
- `E60` — درصد تغییر

**`Recovered_Sheet1`, row 61:**
- `B61` — حسابرسی نشده
- `C61` — حسابرسی نشده
- `D61` — حسابرسی شده

**`Recovered_Sheet1`, row 62:**
- `A62` — سود(زیان) خالص 

**`Recovered_Sheet1`, row 63:**
- `A63` — سایر اقلام سود و زیان جامع: 

**`Recovered_Sheet1`, row 64:**
- `A64` — مازاد تجديد ارزيابي دارايي‌ها 

**`Recovered_Sheet1`, row 65:**
- `A65` — تفاوت تسعیر ارز عملیات خارجی 

**`Recovered_Sheet1`, row 66:**
- `A66` — مالیات مربوط به سایر اقلام سود و زیان جامع 

**`Recovered_Sheet1`, row 67:**
- `A67` — سایر اقلام سود و زیان جامع سال پس از کسر مالیات 

**`Recovered_Sheet1`, row 68:**
- `A68` — سود(زيان) جامع سال 

**`Recovered_Sheet1`, row 72:**
- `A72` — صورت وضعیت مالی

**`Recovered_Sheet1`, row 77:**
- `A77` — صورت وضعیت مالی

**`Recovered_Sheet1`, row 78:**
- `A78` — کلیه مبالغ درج شده به میلیون ریال می باشد

**`Recovered_Sheet1`, row 79:**
- `A79` — شرح
- `B79` — دوره منتهي به ۱۴۰۱/۰۹/۳۰
- `C79` — تجدید ارائه شده ۱۴۰۰/۱۲/۲۹
- `D79` — تجدید ارائه شده ۱۴۰۰/۰۱/۰۱
- `E79` — درصد تغییرات

**`Recovered_Sheet1`, row 80:**
- `B80` — حسابرسی نشده
- `C80` — حسابرسی شده
- `D80` — حسابرسی نشده

**`Recovered_Sheet1`, row 81:**
- `A81` — دارایی ها 

**`Recovered_Sheet1`, row 82:**
- `A82` — موجودي نقد 

**`Recovered_Sheet1`, row 83:**
- `A83` — مطالبات از بانک ها و ساير موسسات اعتباري 

**`Recovered_Sheet1`, row 84:**
- `A84` — مطالبات از دولت 

**`Recovered_Sheet1`, row 85:**
- `A85` — تسهيلات اعطايي و مطالبات از اشخاص دولتي 

**`Recovered_Sheet1`, row 86:**
- `A86` — تسهيلات اعطايي و مطالبات از اشخاص غير دولتي 

**`Recovered_Sheet1`, row 87:**
- `A87` — سرمایه‌گذاری در سهام و ساير اوراق بهادار 

**`Recovered_Sheet1`, row 88:**
- `A88` — مطالبات از شرکت‌های فرعی و وابسته 

**`Recovered_Sheet1`, row 89:**
- `A89` — ساير حسابهاي دريافتني 

**`Recovered_Sheet1`, row 90:**
- `A90` — دارایی‌هاي ثابت مشهود 

**`Recovered_Sheet1`, row 91:**
- `A91` — دارایی‌هاي نا مشهود 

**`Recovered_Sheet1`, row 92:**
- `A92` — سپرده قانونی 

**`Recovered_Sheet1`, row 93:**
- `A93` — ساير دارایی‌ها 

**`Recovered_Sheet1`, row 94:**
- `A94` — جمع دارایی‌ها 

**`Recovered_Sheet1`, row 95:**
- `A95` — حقوق مالکانه و بدهی‌ها 
- `B95` — دوره منتهی به ۱۴۰۱/۰۹/۳۰ 
- `C95` — تجدید ارائه شده ۱۴۰۰/۱۲/۲۹ 
- `D95` — تجدید ارائه شده۱۴۰۰/۰۱/۰۱ 
- `E95` — درصد تغییرات 

**`Recovered_Sheet1`, row 96:**
- `A96` — حقوق مالکانه 

**`Recovered_Sheet1`, row 97:**
- `A97` — سرمايه 

**`Recovered_Sheet1`, row 98:**
- `A98` — افزايش سرمايه در جريان 

**`Recovered_Sheet1`, row 99:**
- `A99` — صرف سهام 

**`Recovered_Sheet1`, row 100:**
- `A100` — اندوخته صرف سهام 

**`Recovered_Sheet1`, row 101:**
- `A101` — اندوخته قانوني 

**`Recovered_Sheet1`, row 102:**
- `A102` — ساير اندوخته‌ها 

**`Recovered_Sheet1`, row 103:**
- `A103` — مازاد تجديد ارزيابي دارايي‌ها 

**`Recovered_Sheet1`, row 104:**
- `A104` — تفاوت تسعیر ارز 

**`Recovered_Sheet1`, row 105:**
- `A105` — سود (زيان) انباشته 

**`Recovered_Sheet1`, row 106:**
- `A106` — سهام خزانه 

**`Recovered_Sheet1`, row 107:**
- `A107` — جمع حقوق مالکانه 

**`Recovered_Sheet1`, row 108:**
- `A108` — بدهی‌ها 

**`Recovered_Sheet1`, row 109:**
- `A109` — بدهي به بانكها و ساير موسسات اعتباري 

**`Recovered_Sheet1`, row 110:**
- `A110` — سپرده‌هاي مشتریان 

**`Recovered_Sheet1`, row 111:**
- `A111` — سود سهام پرداختني 

**`Recovered_Sheet1`, row 112:**
- `A112` — اوراق بدهی 

**`Recovered_Sheet1`, row 113:**
- `A113` — ذخيره ماليات عملکرد 

**`Recovered_Sheet1`, row 114:**
- `A114` — ذخاير و ساير بدهی‌ها 

**`Recovered_Sheet1`, row 115:**
- `A115` — ذخيره مزاياي پايان خدمت و تعهدات بازنشستگی کارکنان 

**`Recovered_Sheet1`, row 116:**
- `A116` — جمع بدهی های قبل از حقوق صاحبان سپرده های سرمایه گذاری 

**`Recovered_Sheet1`, row 117:**
- `A117` — حقوق صاحبان سپرده‌های سرمایه‌گذاری 

**`Recovered_Sheet1`, row 118:**
- `A118` — جمع بدهی‌ها 

**`Recovered_Sheet1`, row 119:**
- `A119` — جمع بدهی‌ها و حقوق مالکانه 

**`Recovered_Sheet1`, row 123:**
- `A123` — صورت تغییرات در حقوق مالکانه

**`Recovered_Sheet1`, row 128:**
- `A128` — صورت تغییرات در حقوق مالکانه

**`Recovered_Sheet1`, row 129:**
- `A129` — کلیه مبالغ درج شده به میلیون ریال می باشد

**`Recovered_Sheet1`, row 130:**
- `A130` — شرح
- `B130` — سرمایه
- `C130` — افزایش سرمایه در جریان
- `D130` — صرف سهام
- `E130` — صرف سهام خزانه
- `F130` — اندوخته قانونی
- `G130` — سایر اندوخته‌ها
- `H130` — مازاد تجدید ارزیابی دارایی‌ها
- `I130` — تفاوت تسعیر ارز عملیات خارجی
- `J130` — سود انباشته
- `K130` — سهام خزانه
- `L130` — جمع کل

**`Recovered_Sheet1`, row 131:**
- `A131` — مانده در ۱۴۰۰/۰۱/۰۱ 

**`Recovered_Sheet1`, row 132:**
- `A132` — اصلاح اشتباهات 

**`Recovered_Sheet1`, row 133:**
- `A133` — تغییر در رویه‌های حسابداری 

**`Recovered_Sheet1`, row 134:**
- `A134` — مانده تجدید ارائه شده در ۱۴۰۰/۰۱/۰۱ 

**`Recovered_Sheet1`, row 135:**
- `A135` — تغییرات حقوق مالکانه در سال ۱۴۰۰/۱۲/۲۹ 

**`Recovered_Sheet1`, row 136:**
- `A136` — سود(زيان) خالص گزارش شده در صورت‌هاي مالي سال ۱۴۰۰/۱۲/۲۹ 

**`Recovered_Sheet1`, row 137:**
- `A137` — اصلاح اشتباهات 

**`Recovered_Sheet1`, row 138:**
- `A138` — تغییر در رویه‌های حسابداری 

**`Recovered_Sheet1`, row 139:**
- `A139` — سود خالص تجدید ارائه شده سال ۱۴۰۰/۱۲/۲۹ 

**`Recovered_Sheet1`, row 140:**
- `A140` — سایر اقلام سود و زیان جامع پس از کسر مالیات 

**`Recovered_Sheet1`, row 141:**
- `A141` — سود(زيان) جامع سال ۱۴۰۰/۱۲/۲۹ 

**`Recovered_Sheet1`, row 142:**
- `A142` — سود سهام مصوب 

**`Recovered_Sheet1`, row 143:**
- `A143` — افزایش سرمایه 

**`Recovered_Sheet1`, row 144:**
- `A144` — افزایش سرمایه در جریان 

**`Recovered_Sheet1`, row 145:**
- `A145` — خرید سهام خزانه 

**`Recovered_Sheet1`, row 146:**
- `A146` — فروش سهام خزانه 

**`Recovered_Sheet1`, row 147:**
- `A147` — سود (زیان) حاصل از فروش سهام خزانه 

**`Recovered_Sheet1`, row 148:**
- `A148` — انتقال از سایر اقلام حقوق مالکانه به سود و زیان انباشته 

**`Recovered_Sheet1`, row 149:**
- `A149` — تخصیص به اندوخته قانونی 

**`Recovered_Sheet1`, row 150:**
- `A150` — تخصیص به سایر اندوخته‌ها 

**`Recovered_Sheet1`, row 151:**
- `A151` — مانده تجدید ارائه شده در ۱۴۰۰/۱۲/۲۹ 

**`Recovered_Sheet1`, row 152:**
- `A152` — تغییرات حقوق مالکانه در سال ۱۴۰۱/۰۹/۳۰ 

**`Recovered_Sheet1`, row 153:**
- `A153` — سود خالص ۱۴۰۱/۰۹/۳۰ 

**`Recovered_Sheet1`, row 154:**
- `A154` — سایر اقلام سود و زیان جامع پس از کسر مالیات 

**`Recovered_Sheet1`, row 155:**
- `A155` — سود(زيان) جامع در ۱۴۰۱/۰۹/۳۰ 

**`Recovered_Sheet1`, row 156:**
- `A156` — سود(زيان) سهام مصوب 

**`Recovered_Sheet1`, row 157:**
- `A157` — افزایش سرمایه 

**`Recovered_Sheet1`, row 158:**
- `A158` — افزایش سرمایه در جریان 

**`Recovered_Sheet1`, row 159:**
- `A159` — خرید سهام خزانه 

**`Recovered_Sheet1`, row 160:**
- `A160` — فروش سهام خزانه 

**`Recovered_Sheet1`, row 161:**
- `A161` — سود (زیان) حاصل از فروش سهام خزانه 

**`Recovered_Sheet1`, row 162:**
- `A162` — انتقال از سایر اقلام حقوق مالکانه به سود و زیان انباشته 

**`Recovered_Sheet1`, row 163:**
- `A163` — تخصیص به اندوخته قانونی 

**`Recovered_Sheet1`, row 164:**
- `A164` — تخصیص به سایر اندوخته‌ها 

**`Recovered_Sheet1`, row 165:**
- `A165` — مانده در ۱۴۰۱/۰۹/۳۰ 

**`Recovered_Sheet1`, row 169:**
- `A169` — صورت جریان های نقدی

**`Recovered_Sheet1`, row 174:**
- `A174` — صورت جریان های نقدی

**`Recovered_Sheet1`, row 175:**
- `A175` — کلیه مبالغ به میلیون ریال است

**`Recovered_Sheet1`, row 176:**
- `A176` — شرح
- `B176` — دوره منتهي به ۱۴۰۱/۰۹/۳۰
- `C176` — تجدید ارائه شده۱۴۰۰/۰۹/۳۰
- `D176` — تجدید ارائه شده۱۴۰۰/۱۲/۲۹
- `E176` — درصد تغییر

**`Recovered_Sheet1`, row 177:**
- `B177` — حسابرسی نشده
- `C177` — حسابرسی نشده
- `D177` — حسابرسی شده

**`Recovered_Sheet1`, row 178:**
- `A178` — جریان­های نقدی حاصل از فعاليت‌هاي عملياتي: 

**`Recovered_Sheet1`, row 179:**
- `A179` — نقد حاصل از عملیات 

**`Recovered_Sheet1`, row 180:**
- `A180` — پرداخت‌های نقدی بابت مالیات بر درآمد 
- `E180` — -Infinity 

**`Recovered_Sheet1`, row 181:**
- `A181` — جريان ‌خالص ‌ورود‌ (خروج) ‌نقد حاصل از فعاليت‌هاي ‌عملياتي 

**`Recovered_Sheet1`, row 182:**
- `A182` — فعاليت‌هاي سرمایه‌گذاری 

**`Recovered_Sheet1`, row 183:**
- `A183` — وجوه پرداختي بابت تحصیل دارایی‌هاي ثابت مشهود 

**`Recovered_Sheet1`, row 184:**
- `A184` — وجوه دریافتی بابت فروش دارایی‌هاي ثابت مشهود 

**`Recovered_Sheet1`, row 185:**
- `A185` — وجوه پرداختي بابت تحصیل دارایی‌هاي نامشهود 
- `E185` — -Infinity 

**`Recovered_Sheet1`, row 186:**
- `A186` — وجوه دریافتی بابت فروش دارایی‌هاي نامشهود 

**`Recovered_Sheet1`, row 187:**
- `A187` — وجوه پرداختي بابت تحصیل املاک و مستغلات غیر عملیاتی 

**`Recovered_Sheet1`, row 188:**
- `A188` — وجوه دریافتی بابت فروش املاک و مستغلات غیر عملیاتی 

**`Recovered_Sheet1`, row 189:**
- `A189` — جريان خالص ورود (خروج) وجه نقد ناشی از فعاليت‌هاي سرمایه‌گذاری 

**`Recovered_Sheet1`, row 190:**
- `A190` — جريان خالص ورود (خروج) وجه نقد قبل از فعالیت‌های تامین مالی 

**`Recovered_Sheet1`, row 191:**
- `A191` — فعاليت‌هاي تأمين مالي 

**`Recovered_Sheet1`, row 192:**
- `A192` — دریافت‌های نقدی حاصل از افزايش سرمايه 

**`Recovered_Sheet1`, row 193:**
- `A193` — دریافت‌های نقدی حاصل از صرف سهام 

**`Recovered_Sheet1`, row 194:**
- `A194` — دریافت‌های نقدی حاصل از فروش سهام خزانه 

**`Recovered_Sheet1`, row 195:**
- `A195` — پرداخت‌های نقدی برای خرید سهام خزانه 

**`Recovered_Sheet1`, row 196:**
- `A196` — دریافت‌های نقدی حاصل از تسهيلات 

**`Recovered_Sheet1`, row 197:**
- `A197` — پرداخت‌های نقدی بابت اصل تسهيلات 

**`Recovered_Sheet1`, row 198:**
- `A198` — پرداخت‌های نقدی بابت سود تسهيلات 

**`Recovered_Sheet1`, row 199:**
- `A199` — دریافت‌های نقدی حاصل از انتشار اوراق مشارکت 

**`Recovered_Sheet1`, row 200:**
- `A200` — پرداخت‌های نقدی بابت اصل اوراق مشارکت 

**`Recovered_Sheet1`, row 201:**
- `A201` — پرداخت‌های نقدی بابت سود اوراق مشارکت 

**`Recovered_Sheet1`, row 202:**
- `A202` — دریافت‌های نقدی حاصل از انتشار اوراق خرید دین 

**`Recovered_Sheet1`, row 203:**
- `A203` — پرداخت‌های نقدی بابت اصل اوراق خرید دین 

**`Recovered_Sheet1`, row 204:**
- `A204` — پرداخت‌های نقدی بابت سود اوراق خرید دین 

**`Recovered_Sheet1`, row 205:**
- `A205` — پرداخت‌های نقدی بابت اصل اقساط اجاره سرمایه‌ای 

**`Recovered_Sheet1`, row 206:**
- `A206` — پرداخت‌های نقدی بابت سود اجاره سرمایه‌ای 

**`Recovered_Sheet1`, row 207:**
- `A207` — پرداخت‌های نقدی بابت سود سهام 

**`Recovered_Sheet1`, row 208:**
- `A208` — جريان خالص ورود (خروج) نقد حاصل از فعاليت‌هاي تامين مالي 

**`Recovered_Sheet1`, row 209:**
- `A209` — خالص افزايش (کاهش) در موجودی نقد 

**`Recovered_Sheet1`, row 210:**
- `A210` — مانده موجودی نقد در ابتدای سال 

**`Recovered_Sheet1`, row 211:**
- `A211` — تاثير تغييرات نرخ ارز 

**`Recovered_Sheet1`, row 212:**
- `A212` — مانده موجودی نقد در پايان سال 

**`Recovered_Sheet1`, row 213:**
- `A213` — معاملات غيرنقدي 

**`Recovered_Sheet1`, row 221:**
- `A221` — دلایل تغییرات اطلاعات واقعی دوره منتهی به ۱۴۰۱/۰۹/۳۰ 

**`Recovered_Sheet1`, row 223:**
- `A223` — دلایل تغییرات اطلاعات واقعی دوره منتهی به ۱۴۰۰/۰۹/۳۰ 

**`Recovered_Sheet1`, row 225:**
- `A225` — دلایل تغییرات اطلاعات واقعی دوره منتهی به ۱۴۰۰/۱۲/۲۹ 

**`Recovered_Sheet1`, row 230:**
- `A230` — خلاصه اطلاعات گزارش تفسیری - صفحه 1

**`Recovered_Sheet1`, row 235:**
- `A235` — اطلاعات این فرم گزیده ای از اطلاعات گزارش تفسیری مدیریت می باشد که هیئت مدیره شرکت مطابق با مفاد دستورالعمل اجرایی افشای اطلاعات شرکتهای ثبت شده نزد سازمان موظف به ارائه آن در پیوست این اطلاعیه می باشد و این اطلاعات جایگزین گزارش مذکور نیست. 

**`Recovered_Sheet1`, row 236:**
- `A236` — مانده تسهیلات اعطایی و ذخیره مطالبات مشکوک الوصول:

**`Recovered_Sheet1`, row 237:**
- `A237` — کلیه مبالغ درج شده به میلیون ریال می باشد

**`Recovered_Sheet1`, row 238:**
- `A238` — شرح
- `B238` — در تاریخ ۱۴۰۰/۱۲/۲۹
- `C238` — در تاریخ ۱۴۰۱/۰۹/۳۰
- `D238` — در تاریخ ۱۴۰۰/۱۲/۲۹
- `E238` — در تاریخ ۱۴۰۱/۰۹/۳۰
- `F238` — در تاریخ ۱۴۰۰/۱۲/۲۹
- `G238` — در تاریخ ۱۴۰۱/۰۹/۳۰
- `H238` — در تاریخ ۱۴۰۰/۱۲/۲۹
- `I238` — در تاریخ ۱۴۰۱/۰۹/۳۰
- `J238` — در تاریخ ۱۴۰۰/۱۲/۲۹
- `K238` — در تاریخ ۱۴۰۱/۰۹/۳۰

**`Recovered_Sheet1`, row 239:**
- `B239` — جاری
- `D239` — سررسید گذشته
- `F239` — معوق
- `H239` — مشکوک الوصول
- `J239` — جمع

**`Recovered_Sheet1`, row 240:**
- `A240` — تسهیلات اعطایی و مطالبات از اشخاص دولتی 

**`Recovered_Sheet1`, row 241:**
- `A241` — تسهیلات اعطایی و مطالبات از اشخاص غیر دولتی- ریالی 

**`Recovered_Sheet1`, row 242:**
- `A242` — تسهیلات اعطایی و مطالبات از اشخاص غیر دولتی- ارزی 

**`Recovered_Sheet1`, row 243:**
- `A243` — جمع 

**`Recovered_Sheet1`, row 244:**
- `A244` — کسر می شود: 

**`Recovered_Sheet1`, row 245:**
- `A245` — سود سالهای آتی 

**`Recovered_Sheet1`, row 246:**
- `A246` — سایر 

**`Recovered_Sheet1`, row 247:**
- `A247` — مانده تسهیلات پایان دوره 

**`Recovered_Sheet1`, row 248:**
- `A248` — ارزش وثایق دریافتی 

**`Recovered_Sheet1`, row 249:**
- `A249` — مانده مبنای محاسبه ذخیره اختصاصی 

**`Recovered_Sheet1`, row 250:**
- `A250` — ضریب مبنای احتساب ذخیره اختصاصی (درصد) 

**`Recovered_Sheet1`, row 251:**
- `A251` — ذخیره اختصاصی مطالبات مشکوک الوصول 

**`Recovered_Sheet1`, row 252:**
- `A252` — مانده مبنای محاسبه ذخیره عمومی 

**`Recovered_Sheet1`, row 253:**
- `A253` — ذخیره عمومی مطالبات مشکوک الوصول 

**`Recovered_Sheet1`, row 254:**
- `A254` — جمع 

**`Recovered_Sheet1`, row 255:**
- `A255` — برآورد شرکت از تغییرات در نرخ سود تسهیلات اعطایی :

**`Recovered_Sheet1`, row 256:**
- `A256` — دوره ۳ ماهه منتهي به ۱۴۰۱/۱۲/۲۹ 
- `C256` — نرخ سود تسهیلات اعطایی همواره وفق بخشنامه های ابلاغی بانک مرکزی صورت می پذیرد. 

**`Recovered_Sheet1`, row 257:**
- `A257` — دوره ۳ ماهه منتهي به ۱۴۰۲/۰۳/۳۱ 
- `C257` — نرخ سود تسهیلات اعطایی همواره وفق بخشنامه های ابلاغی بانک مرکزی صورت می پذیرد. 

**`Recovered_Sheet1`, row 258:**
- `A258` — برآورد شرکت از تغییرات در مانده تسهیلات :

**`Recovered_Sheet1`, row 259:**
- `A259` — دوره ۳ ماهه منتهي به ۱۴۰۱/۱۲/۲۹ 
- `C259` — سیاست های بانک در تخصیص منابع در چارچوب ایجاد پرتفوی اعتباری بهینه و همسو با سیاست های کلان اقتصادی کشور می باشد که در این راستا تخصیص منابع به بخشهای صنعتی ، تولیدی، کشاورزی ،بازرگانی و خدمات در جهت تامین مالی پروژه ها و سرمایه در گردش متقاضیان تسهیلات صورت می پذیرد. 

**`Recovered_Sheet1`, row 260:**
- `A260` — دوره ۳ ماهه منتهي به ۱۴۰۲/۰۳/۳۱ 
- `C260` — سیاست های بانک در تخصیص منابع در چارچوب ایجاد پرتفوی اعتباری بهینه و همسو با سیاست های کلان اقتصادی کشور می باشد که در این راستا تخصیص منابع به بخشهای صنعتی ، تولیدی، کشاورزی ،بازرگانی و خدمات در جهت تامین مالی پروژه ها و سرمایه در گردش متقاضیان تسهیلات صورت می پذیرد. 

**`Recovered_Sheet1`, row 261:**
- `A261` — برآورد شرکت از تغییرات در مانده ذخایر مطالبات مشکوک الوصول :

**`Recovered_Sheet1`, row 262:**
- `A262` — دوره ۳ ماهه منتهي به ۱۴۰۱/۱۲/۲۹ 
- `C262` — بر اساس سیاست ها و خط مشی های اعتباری تدوین شده و با توجه به اعتبار سنجی انجام شده درخصوص مشتریان اعتباری و همچنین تضامین و وثایق دریافتی از مشتریان کاهش ریسک اعتباری مشتریان و متعاقباً کاهش هزینه مطالبات مشکوک الوصول از سیاست های بانک می باشد. 

**`Recovered_Sheet1`, row 263:**
- `A263` — دوره ۳ ماهه منتهي به ۱۴۰۲/۰۳/۳۱ 
- `C263` — بر اساس سیاست ها و خط مشی های اعتباری تدوین شده و با توجه به اعتبار سنجی انجام شده درخصوص مشتریان اعتباری و همچنین تضامین و وثایق دریافتی از مشتریان کاهش ریسک اعتباری مشتریان و متعاقباً کاهش هزینه مطالبات مشکوک الوصول از سیاست های بانک می باشد. 

**`Recovered_Sheet1`, row 264:**
- `A264` — مانده سپرده های دریافتی از مشتریان :

**`Recovered_Sheet1`, row 265:**
- `A265` — کلیه مبالغ درج شده به میلیون ریال می باشد

**`Recovered_Sheet1`, row 266:**
- `A266` — شرح
- `B266` — مانده سپرده ها
- `D266` — متوسط نرخ سود مانده سپرده ها
- `F266` — برآورد مدیریت از تغییر در نرخ سود سپرده ها و تغییر در مانده سپرده های دریافتی از مشتریان

**`Recovered_Sheet1`, row 267:**
- `B267` — در تاریخ ۱۴۰۰/۱۲/۲۹
- `C267` — در تاریخ ۱۴۰۱/۰۹/۳۰
- `D267` — در تاریخ ۱۴۰۰/۱۲/۲۹
- `E267` — در تاریخ ۱۴۰۱/۰۹/۳۰

**`Recovered_Sheet1`, row 268:**
- `A268` — سپرده های ریالی: 

**`Recovered_Sheet1`, row 269:**
- `A269` — سپرده های کوتاه مدت 

**`Recovered_Sheet1`, row 270:**
- `A270` — سپرده های کوتاه مدت ویژه 

**`Recovered_Sheet1`, row 271:**
- `A271` — سپرده های بلند مدت 

**`Recovered_Sheet1`, row 272:**
- `A272` — جمع سپرده های هزینه زا 

**`Recovered_Sheet1`, row 273:**
- `A273` — سپرده های غیر هزینه زا 

**`Recovered_Sheet1`, row 274:**
- `A274` — جمع سپرده های ریالی 

**`Recovered_Sheet1`, row 275:**
- `A275` — سپرده های ارزی 

**`Recovered_Sheet1`, row 276:**
- `A276` — جمع سپرده های دریافتی 

**`Recovered_Sheet1`, row 277:**
- `A277` — اقلام زیر خط:

**`Recovered_Sheet1`, row 278:**
- `A278` — کلیه مبالغ درج شده به میلیون ریال می باشد

**`Recovered_Sheet1`, row 279:**
- `A279` — شرح
- `B279` — ۱۴۰۱/۰۹/۳۰
- `C279` — ۱۴۰۰/۱۲/۲۹
- `D279` — شرح
- `E279` — ۱۴۰۱/۰۹/۳۰
- `F279` — ۱۴۰۰/۱۲/۲۹

**`Recovered_Sheet1`, row 280:**
- `A280` — تعهدات مشتریان بابت اعتبارات اسنادی 
- `D280` — تعهدات بانک بابت اعتبارات اسنادی 

**`Recovered_Sheet1`, row 281:**
- `A281` — تعهدات مشتریان بابت ضمانت نامه های صادره 
- `D281` — تعهدات بانک بابت ضمانت نامه های صادره 

**`Recovered_Sheet1`, row 282:**
- `A282` — ساير تعهدات مشتريان بانک 
- `D282` — سایر تعهدات بانک 

**`Recovered_Sheet1`, row 283:**
- `A283` — وجوه اداره شده و موارد مشابه 
- `D283` — وجوه اداره شده و موارد مشابه 

**`Recovered_Sheet1`, row 284:**
- `A284` — توضیحات در خصوص تغییرات بااهمیت: 

**`Recovered_Sheet1`, row 285:**
- `A285` — «جملات آینده‌نگر نشان‌دهنده انتظارات، باورها یا پیش‌بینی‌های جاری از رویدادها و عملکرد مالی است. این جملات در معرض ریسک‌ها، عدم‌قطعیت‌ها و مفروضات غیرقطعی قرار دارند. بنابراین نتایج واقعی ممکن است متفاوت از نتایج مورد انتظار باشند.» 

**`Recovered_Sheet1`, row 289:**
- `A289` — خلاصه اطلاعات گزارش تفسیری - صفحه 2

**`Recovered_Sheet1`, row 294:**
- `A294` — اطلاعات این فرم گزیده ای از اطلاعات گزارش تفسیری مدیریت می باشد که هیئت مدیره شرکت مطابق با مفاد دستورالعمل اجرایی افشای اطلاعات شرکتهای ثبت شده نزد سازمان موظف به ارائه آن در پیوست این اطلاعیه می باشد و این اطلاعات جایگزین گزارش مذکور نیست. 

**`Recovered_Sheet1`, row 295:**
- `A295` — وضعیت کارکنان:

**`Recovered_Sheet1`, row 296:**
- `A296` — کلیه مبالغ درج شده به میلیون ریال می باشد

**`Recovered_Sheet1`, row 297:**
- `A297` — شرح
- `B297` — در تاریخ ۱۴۰۰/۱۲/۲۹
- `C297` — در تاریخ ۱۴۰۱/۰۹/۳۰
- `D297` — برآورد در تاریخ ۱۴۰۱/۱۲/۲۹
- `E297` — برآورد در تاریخ ۱۴۰۲/۰۳/۳۱

**`Recovered_Sheet1`, row 298:**
- `A298` — تعداد شعب 

**`Recovered_Sheet1`, row 299:**
- `A299` — تعداد کارکنان 

**`Recovered_Sheet1`, row 300:**
- `A300` — اطلاعات حق الوکاله و کفایت سرمایه

**`Recovered_Sheet1`, row 301:**
- `A301` — کلیه مبالغ درج شده به میلیون ریال می باشد

**`Recovered_Sheet1`, row 302:**
- `A302` — شرح
- `B302` — سال مالی منتهی به۱۴۰۰/۱۲/۲۹
- `C302` — دوره ۹ ماهه منتهی به ۱۴۰۱/۰۹/۳۰
- `D302` — برآورد تغییر روند در دوره ۳ ماهه منتهی به ۱۴۰۱/۱۲/۲۹
- `F302` — برآورد تغییر روند در دوره ۳ ماهه منتهی به ۱۴۰۲/۰۳/۳۱

**`Recovered_Sheet1`, row 303:**
- `A303` — سهم بانک از درآمدهای مشاع 

**`Recovered_Sheet1`, row 304:**
- `A304` — سهم سپرده گذاران از درآمدهای مشاع 

**`Recovered_Sheet1`, row 305:**
- `A305` — نرخ حق الوکاله اعلام شده 
- `F305` — نرخ حق الوکاله بانک معادل ۳% تصویب و از طریق روزنامه های کثیرالانتشار اعلام گردیده است. 

**`Recovered_Sheet1`, row 306:**
- `A306` — مبلغ حق الوکاله اعمال شده 

**`Recovered_Sheet1`, row 307:**
- `A307` — مابه التفاوت سود قابل پرداخت (مازاد سود پرداختی) به سپرده گذاران 

**`Recovered_Sheet1`, row 308:**
- `A308` — نسبت کفایت سرمایه 

**`Recovered_Sheet1`, row 309:**
- `A309` — اهداف و راهبردهای آتی مدیریت در خصوص فعالیت شرکت:

**`Recovered_Sheet1`, row 310:**
- `A310` — اهداف و راهبردهای آتی مدیریت در خصوص فعالیت شرکت: 
- `B310` — مدیریت و توسعه منابع انسانی،ارتقاء بهره وری، رضایت مشتری،توسعه خدمات خرده بانکداری،توسعه بانکداری الکترونیک،کمک به کاهش مسافرتهای شهری و روستایی و هزینه های مربوط وانضباط مالی و مدیریت نقدینگی 

**`Recovered_Sheet1`, row 311:**
- `A311` — درآمد حاصل از تسهيلات اعطايي و سپرده گذاري

**`Recovered_Sheet1`, row 312:**
- `A312` — کلیه مبالغ درج شده به میلیون ریال می باشد

**`Recovered_Sheet1`, row 313:**
- `A313` — شرح
- `B313` — سال مالی منتهی به ۱۴۰۰/۱۲/۲۹
- `C313` — متوسط نرخ سود سال مالی منتهی به ۱۴۰۰/۱۲/۲۹ (درصد)
- `D313` — دوره ۹ ماهه منتهی به ۱۴۰۱/۰۹/۳۰
- `E313` — متوسط نرخ سود دوره ۹ ماهه منتهی به ۱۴۰۱/۰۹/۳۰ (درصد)
- `F313` — برآورد تغییر روند در دوره ۳ ماهه منتهی به ۱۴۰۱/۱۲/۲۹
- `H313` — برآورد تغییر روند در دوره ۳ ماهه منتهی به ۱۴۰۲/۰۳/۳۱

**`Recovered_Sheet1`, row 314:**
- `A314` — درآمد تسهیلات اعطایی: 

**`Recovered_Sheet1`, row 315:**
- `A315` — فروش اقساطی 

**`Recovered_Sheet1`, row 316:**
- `A316` — جعاله 

**`Recovered_Sheet1`, row 317:**
- `A317` — اجاره به شرط تملیک 

**`Recovered_Sheet1`, row 318:**
- `A318` — سلف 

**`Recovered_Sheet1`, row 319:**
- `A319` — مضاربه 

**`Recovered_Sheet1`, row 320:**
- `A320` — مشارکت مدنی 

**`Recovered_Sheet1`, row 321:**
- `A321` — خرید دین 

**`Recovered_Sheet1`, row 322:**
- `A322` — بدهکاران بابت اعتبارات اسنادی پرداخت شده 

**`Recovered_Sheet1`, row 323:**
- `A323` — بدهکاران بابت ضمانت نامه های پرداخت شده 

**`Recovered_Sheet1`, row 324:**
- `A324` — تسهیلات ارزی 

**`Recovered_Sheet1`, row 325:**
- `A325` — تسهیلات قرض الحسنه 

**`Recovered_Sheet1`, row 326:**
- `A326` — سایر درآمد تسهیلات اعطایی 

**`Recovered_Sheet1`, row 327:**
- `A327` — جمع درآمد حاصل از تسهیلات اعطایی 

**`Recovered_Sheet1`, row 328:**
- `A328` — جایزه سپرده قانونی 

**`Recovered_Sheet1`, row 329:**
- `A329` — سود حاصل از سپرده گذاری در بانکها 

**`Recovered_Sheet1`, row 330:**
- `A330` — جمع سود حاصل از سپرده گذاری ها 

**`Recovered_Sheet1`, row 331:**
- `A331` — درآمد اوراق بدهی و سایر درآمدهای ناشی از سپرده گذاری 

**`Recovered_Sheet1`, row 332:**
- `A332` — درآمد حاصل ازتسهیلات اعطایی و سپرده‌گذاری‌ها 

**`Recovered_Sheet1`, row 333:**
- `A333` — ارائه توضیحات در خصوص نحوه محاسبه متوسط نرخ سود تسهیلات: 
- `C333` — متوسط نرخ سود تسهیلات بر اساس ضوابط ابلاغی بانک مرکزی جمهوری اسلامی ایران و نرخ ابلاغی شورای پول و اعتبار محاسبه شده است. 

**`Recovered_Sheet1`, row 334:**
- `A334` — خالص سود (زیان) سرمایه گذاری‌ ها

**`Recovered_Sheet1`, row 335:**
- `A335` — کلیه مبالغ درج شده به میلیون ریال می باشد

**`Recovered_Sheet1`, row 336:**
- `A336` — شرح
- `B336` — سال مالی منتهی به۱۴۰۰/۱۲/۲۹
- `C336` — دوره ۹ ماهه منتهی به ۱۴۰۱/۰۹/۳۰
- `D336` — برآورد تغییر روند در دوره ۳ ماهه منتهی به ۱۴۰۱/۱۲/۲۹
- `F336` — برآورد تغییر روند در دوره ۳ ماهه منتهی به ۱۴۰۲/۰۳/۳۱

**`Recovered_Sheet1`, row 337:**
- `A337` — درآمد حاصل از سرمایه گذاری در سهام 

**`Recovered_Sheet1`, row 338:**
- `A338` — سود(زیان) حاصل از فروش سرمایه گذاری 

**`Recovered_Sheet1`, row 339:**
- `A339` — سود (زیان) تعدیل ذخیره کاهش ارزش سرمایه گذاریها 

**`Recovered_Sheet1`, row 340:**
- `A340` — جمع درآمدهای حاصل از سرمایه گذاری 

**`Recovered_Sheet1`, row 341:**
- `A341` — «جملات آینده‌نگر نشان‌دهنده انتظارات، باورها یا پیش‌بینی‌های جاری از رویدادها و عملکرد مالی است. این جملات در معرض ریسک‌ها، عدم‌قطعیت‌ها و مفروضات غیرقطعی قرار دارند. بنابراین نتایج واقعی ممکن است متفاوت از نتایج مورد انتظار باشند.» 

**`Recovered_Sheet1`, row 345:**
- `A345` — خلاصه اطلاعات گزارش تفسیری - صفحه 3

**`Recovered_Sheet1`, row 350:**
- `A350` — اطلاعات اين فرم گزيده اي از اطلاعات گزارش تفسيري مديريت مي باشد که هيئت مديره شرکت مطابق با مفاد دستورالعمل اجرايي افشاي اطلاعات شرکتهاي ثبت شده نزد سازمان موظف به ارائه آن در پيوست اين اطلاعيه مي باشد و اين اطلاعات جايگزين گزارش مذکور نيست. 

**`Recovered_Sheet1`, row 351:**
- `A351` — وضعیت شرکتهای سرمایه پذیر:

**`Recovered_Sheet1`, row 352:**
- `A352` — کلیه مبالغ درج شده به میلیون ریال می باشد

**`Recovered_Sheet1`, row 353:**
- `A353` — نام شرکت
- `C353` — سال مالي منتهي به ۱۴۰۰/۱۲/۲۹
- `G353` — دوره ۹ ماهه منتهي به ۱۴۰۱/۰۹/۳۰
- `J353` — تشريح آخرين وضعيت و برنامه هاي آتي شرکت در شرکت سرمايه پذير

**`Recovered_Sheet1`, row 354:**
- `C354` — درصد مالکيت
- `D354` — بهاي تمام شده
- `E354` — سال مالي شرکت سرمايه پذير
- `F354` — درآمد سرمايه گذاري
- `G354` — درصد مالکيت
- `H354` — بهاي تمام شده
- `I354` — درآمد سرمايه گذاري

**`Recovered_Sheet1`, row 355:**
- `A355` — بيمه تجارت نو 
- `E355` — ۱۴۰۰/۱۲/۲۹ 
- `J355` — در راستای اجرای قانون رفع موانع تولید رقابت پذیر و ارتقای مالی کشور فروش سهام مزبور در حال پیگیری می باشد. 

**`Recovered_Sheet1`, row 356:**
- `A356` — شبکه الکترونيکي پرداخت کارت شاپرک 
- `E356` — ۱۴۰۰/۰۹/۳۰ 
- `J356` — تکلیفی می باشد. 

**`Recovered_Sheet1`, row 357:**
- `A357` — ساماندهي مطالبات معوق 
- `E357` — ۱۴۰۰/۱۲/۲۹ 
- `J357` — تکلیفی می باشد. 

**`Recovered_Sheet1`, row 358:**
- `A358` — سامانه هاي کاربردي کلان همگام 
- `E358` — ۱۴۰۰/۰۹/۳۰ 

**`Recovered_Sheet1`, row 359:**
- `A359` — صرافي فراز اعتماد 
- `E359` — ۱۴۰۰/۱۲/۲۹ 

**`Recovered_Sheet1`, row 360:**
- `A360` — بورس اوراق بهادار تهران 
- `E360` — ۱۴۰۰/۱۲/۲۹ 
- `J360` — در راستای اجرای قانون رفع موانع تولید رقابت پذیر و ارتقای نظام مالی کشور فروش سهام مزبور در حال پیگیری می باشد. 

**`Recovered_Sheet1`, row 361:**
- `A361` — اختصاصي بازارگرداني پست بانك ايران 
- `E361` — ۱۴۰۰/۰۸/۳۰ 
- `J361` — بر اساس دستورالعمل پذیرش بانک ملزم به داشتن بازارگردان می باشد. 

**`Recovered_Sheet1`, row 362:**
- `A362` — مديريت بازار متشکل معاملات ارز ايران 
- `E362` — ۱۴۰۰/۱۲/۲۹ 
- `J362` — تکلیفی می باشد. 

**`Recovered_Sheet1`, row 363:**
- `A363` — توسعه پست بانك 
- `E363` — ۱۴۰۰/۰۹/۳۰ 
- `J363` — فروخته شد. 

**`Recovered_Sheet1`, row 364:**
- `A364` — ساير درآمدها و هزینه های عملياتي:

**`Recovered_Sheet1`, row 365:**
- `A365` — کلیه مبالغ درج شده به میلیون ریال می باشد

**`Recovered_Sheet1`, row 366:**
- `A366` — شرح
- `B366` — ۱۴۰۰/۱۲/۲۹
- `C366` — ۱۴۰۱/۰۹/۳۰

**`Recovered_Sheet1`, row 367:**
- `A367` — ساير درآمدهاي عملياتي: 

**`Recovered_Sheet1`, row 368:**
- `A368` — ساير درآمدهاي عملياتي 

**`Recovered_Sheet1`, row 370:**
- `A370` — جمع ساير درآمدهاي عملياتي 

**`Recovered_Sheet1`, row 371:**
- `A371` — ساير هزينه هاي عملياتي: 

**`Recovered_Sheet1`, row 373:**
- `A373` — جمع ساير هزينه هاي عملياتي 

**`Recovered_Sheet1`, row 374:**
- `A374` — جمع ساير درآمدها و هزينه هاي عملياتي 

**`Recovered_Sheet1`, row 375:**
- `A375` — برآورد شرکت از تغییرات خالص سایر درآمدها (هزینه ها)ی عملیاتی:

**`Recovered_Sheet1`, row 376:**
- `A376` — دوره ۳ ماهه منتهي به ۱۴۰۱/۱۲/۲۹ 
- `C376` — مطابق نه ماهه اول سالجاری برآورد می شود. 

**`Recovered_Sheet1`, row 377:**
- `A377` — دوره ۳ ماهه منتهي به ۱۴۰۲/۰۳/۳۱ 
- `C377` — مطابق رویه سالجاری پیش بینی می شود. 

**`Recovered_Sheet1`, row 378:**
- `A378` — خالص ساير درآمدها و هزینه ها:

**`Recovered_Sheet1`, row 379:**
- `A379` — کلیه مبالغ درج شده به میلیون ریال می باشد

**`Recovered_Sheet1`, row 380:**
- `A380` — خالص ساير درآمدها و هزينه ها
- `B380` — ۱۴۰۰/۱۲/۲۹
- `C380` — ۱۴۰۱/۰۹/۳۰

**`Recovered_Sheet1`, row 381:**
- `A381` — سود حاصل از فروش داراييهاي ثابت و نامشهود 

**`Recovered_Sheet1`, row 382:**
- `A382` — درآمد حاصل از فروش اموال تمليکي 

**`Recovered_Sheet1`, row 383:**
- `A383` — ساير 

**`Recovered_Sheet1`, row 385:**
- `A385` — جمع خالص ساير درآمدها و هزينه ها 

**`Recovered_Sheet1`, row 386:**
- `A386` — برآورد شرکت از تغییرات خالص ساير درآمدها و هزینه ها :

**`Recovered_Sheet1`, row 387:**
- `A387` — دوره ۳ ماهه منتهي به ۱۴۰۱/۱۲/۲۹ 
- `C387` — مطابق نه ماهه اول سالجاری برآورد می شود. 

**`Recovered_Sheet1`, row 388:**
- `A388` — دوره ۳ ماهه منتهي به ۱۴۰۲/۰۳/۳۱ 
- `C388` — مطابق رویه سالجاری پیش بینی می شود. 

**`Recovered_Sheet1`, row 389:**
- `A389` — هزینه های اداری و عمومی:

**`Recovered_Sheet1`, row 390:**
- `A390` — کلیه مبالغ درج شده به میلیون ریال می باشد

**`Recovered_Sheet1`, row 391:**
- `A391` — هزينه هاي اداري و عمومي
- `B391` — ۱۴۰۰/۱۲/۲۹
- `C391` — ۱۴۰۱/۰۹/۳۰

**`Recovered_Sheet1`, row 392:**
- `A392` — هزينه هاي اداري و عمومي 

**`Recovered_Sheet1`, row 394:**
- `A394` — جمع هزينه هاي اداري و عمومي 

**`Recovered_Sheet1`, row 395:**
- `A395` — برآورد شرکت از تغییرات هزینه های اداری و عمومی :

**`Recovered_Sheet1`, row 396:**
- `A396` — دوره ۳ ماهه منتهي به ۱۴۰۱/۱۲/۲۹ 
- `C396` — مطابق نه ماهه اول سالجاری برآورد می شود. 

**`Recovered_Sheet1`, row 397:**
- `A397` — دوره ۳ ماهه منتهي به ۱۴۰۲/۰۳/۳۱ 
- `C397` — مطابق عملکرد سالجاری پیش بینی می شود. 

**`Recovered_Sheet1`, row 398:**
- `A398` — هزینه مالی:

**`Recovered_Sheet1`, row 399:**
- `A399` — کلیه مبالغ درج شده به میلیون ریال می باشد

**`Recovered_Sheet1`, row 400:**
- `A400` — هزينه‌هاي مالي
- `B400` — ۱۴۰۰/۱۲/۲۹
- `C400` — ۱۴۰۱/۰۹/۳۰

**`Recovered_Sheet1`, row 401:**
- `A401` — هزينه مالي تسهيلات دريافتي از ساير بانکها و موسسات اعتباري 

**`Recovered_Sheet1`, row 402:**
- `A402` — جريمه اضافه برداشت از بانک مرکزي 

**`Recovered_Sheet1`, row 403:**
- `A403` — ساير هزينه هاي مالي 

**`Recovered_Sheet1`, row 404:**
- `A404` — جمع هزينه‌هاي مالي 

**`Recovered_Sheet1`, row 405:**
- `A405` — برآورد شرکت از تغییرات هزینه های مالی :

**`Recovered_Sheet1`, row 406:**
- `A406` — دوره ۳ ماهه منتهي به ۱۴۰۱/۱۲/۲۹ 
- `C406` — مطابق نه ماهه اول سالجاری برآورد می شود. 

**`Recovered_Sheet1`, row 407:**
- `A407` — دوره ۳ ماهه منتهي به ۱۴۰۲/۰۳/۳۱ 
- `C407` — مطابق عملکرد سالجاری پیش بینی می شود. 

**`Recovered_Sheet1`, row 408:**
- `A408` — برنامه شرکت در خصوص تقسیم سود

**`Recovered_Sheet1`, row 409:**
- `A409` — مبلغ سود (زيان) انباشته پايان سال مالي گذشته
- `B409` — سود سهام پيشنهادي هيئت مديره در سال مالي گذشته
- `C409` — مبلغ سود (زيان) خالص سال مالي گذشته
- `D409` — سود سهام مصوب مجمع سال مالي گذشته
- `E409` — پيشنهاد هيئت مديره درخصوص درصد تقسيم سود سال مالي جاري

**`Recovered_Sheet1`, row 411:**
- `A411` — سایر برنامه های با اهمیت شرکت

**`Recovered_Sheet1`, row 412:**
- `A412` — دوره ۳ ماهه منتهي به ۱۴۰۱/۱۲/۲۹ 
- `B412` — رعایت دستورالعملها و بخشنامه های ابلاغی از سوی بانک مرکزی و سازمان بورس اوراق بهادار و پیگیری مستمر وصول مطالبات مشکوک الوصول بانک 

**`Recovered_Sheet1`, row 413:**
- `A413` — دوره ۳ ماهه منتهي به ۱۴۰۲/۰۳/۳۱ 
- `B413` — رعایت دستورالعملها و بخشنامه های ابلاغی از سوی بانک مرکزی و سازمان بورس اوراق بهادار و پیگیری مستمر وصول مطالبات مشکوک الوصول بانک همانند رویه جاری 

**`Recovered_Sheet1`, row 414:**
- `A414` — سایر توضیحات با اهمیت

**`Recovered_Sheet1`, row 415:**
- `A415` — هرگونه تغییر در دستورالعمل ها و بخشنامه های ابلاغی از سوی بانک مرکزی بر سود و زیان دوره های آتی بانک اثرگذار خواهدبود. 

**`Recovered_Sheet1`, row 416:**
- `A416` — «جملات آينده‌نگر نشان‌دهنده انتظارات، باورها يا پيش‌بيني‌هاي جاري از رويدادها و عملکرد مالي است. اين جملات در معرض ريسک‌ها، عدم‌قطعيت‌ها و مفروضات غيرقطعي قرار دارند. بنابراين نتايج واقعي ممکن است متفاوت از نتايج مورد انتظار باشند.» 

## 6. Temporal classification matrix

| Source header/location | Column/group | Classification | Evidence and limits |
|---|---|---|---|
| B10, B60, B176: current-period-end headers | B | Current flow; nine-month cumulative is best supported | Supplemental explicit nine-month headers C302, D313, C336; core duration omitted. Do not calculate standalone quarter. |
| C10, C60, C176: restated prior-date headers | C | Restated prior-period comparative flow; prior nine months supported | Same-date supplemental nine-month evidence; adjustment details absent. |
| D10, D60, D176: restated year-end headers | D | Restated prior full-year flow | Equity schedule supports year-end interpretation; audited status at rows 11/61/177. |
| B79:D79 date headers | B/C/D | Current balance / prior year-end balance / prior opening balance | Point-in-time statement; C and D are marked restated. |
| Equity labels A131/A134/A151/A152/A165 | B:L | Opening; restated opening; prior close; current movements; closing balance | Row labels distinguish stocks and movements. |
| Cash labels A209:A212 | B:D | Change during period; opening stock; FX effect; closing stock | B/C nine-month, D annual. 'Year' wording conflicts with B/C durations. |
| Loan headers B238:K254 | Paired groups | Point-in-time balances by credit status | Multi-level dates/status headers at rows 238-239; verify merged grouping before mapping. |
| Three-month forecast labels, e.g. A256/A259/A262/A377/A388/A397/A407/A413 | Adjacent cells | Forecast horizon, mainly narrative | Future periods are forecasts, not actual quarter results. |
| Deposits A266:E276 | B:C / D:E | Dated balances / associated average rates | Dates row 267; estimate narrative in F. |
| Off-balance A279:F283 | B:C and E:F | Dated item values; meaning depends on row | Two side-by-side description groups. |
| Staff A297:E299 | B:C / D:E | Dated counts / forecast counts | Quantity values despite broad unit note A296. |
| Fee/capital adequacy A302:F308 | B/C / D/F | Annual and nine-month measures / forecast trends | Metric nature varies by row; headers B302/C302/D302/F302. |
| Lending/deposit income A313:H332 | B / D / F,H | Prior annual / current nine-month / forecast quarters | D313 explicitly nine months; E is average rate. |
| Investments A336:F340 | B/C / D,F | Prior annual / current nine-month / forecast quarters | Period headers at row 336. |
| Date-only sections A366:C377, A380:C388, A391:C397, A400:C407 | B:C | Prior/current date; flow duration unclear | Date alone does not establish duration. |
| Dividend plan A409:E410 | A:E | Mixed retained-earnings stock, proposed/approved dividends, prior net income and proposed payout ratio | Different natures and statuses in one table. |

No actual standalone-quarter result column was identified. Current date-only flow schedules do not disclose duration and need clarification. Keep forecast quarters distinct from actuals.

## 7. Financial nature, hierarchy and double-counting

- **Flows:** revenue, expenses, net profit, OCI, cash movements, investment income and dividend activity where described as period amounts (A12:A42, A62:A68, A178:A209).
- **Stocks:** assets, liabilities, equity, loans/reserves, deposits, opening and closing cash (A81:A119, A131:L165, A240:A254, A268:A276, A210:A212).
- **Ratios/derived measures:** change percentages, EPS (A41), average rates (A313:E332), capital adequacy (A308), ownership (A353:I363) and payout percentage (E409). Do not assign monetary units.
- **Quantities:** employee/branch counts (A297:A299); the broad unit note at A296 does not make them monetary.
- **Descriptive disclosures:** strategy, credit policy, estimates, material-change explanations and forward-looking disclaimers (A235, A255:A262, A309:A310, A341, A350, A413, A416).
- Totals are nested: assets row 94 and liabilities/equity row 119; net income repeats in comprehensive income; loan total row 254 aggregates statuses. Do not add totals to child rows.
- Supplementary values repeat statement concepts: lending income row 332 corresponds to statement income; net income repeats in comprehensive income/dividend schedule. Treat as cross-presentations unless proven otherwise. Investee detail may overlap investment-income totals; no reconciliation is supplied.
- Comparative figures are marked restated, but no bridge is provided. No formulas exist to validate subtotal or percentage logic. Literal `-Infinity` may occur in zero-denominator change cells; preserve and flag the source representation.

## 8. Ambiguities requiring clarification

1. Confirm issuer/ticker from filing cover or exchange record; required title says Parsian, filename says Postbank, and investee names do not establish issuer.
2. Confirm core current flow duration; supplemental headers support nine months, but core headers state only period end. No standalone-quarter values found.
3. Confirm current-period duration in date-only sections A366:C377, A380:C388, A391:C397 and A400:C407.
4. Obtain restatement/reclassification basis and adjustment bridge for comparative values marked restated.
5. Confirm merged date/status grouping and reserve definitions in loan schedule A238:K254.
6. Clarify broad unit labels where monetary, count, rate, ratio and narrative fields coexist.
7. Clarify representation of literal zero-denominator changes such as `-Infinity`.
8. Confirm recovered sheet completeness and obtain source notes for issuer identity, accounting policies and restatement explanations.

## 9. Recommended next inspection step

Compare this worksheet with the original exchange filing/PDF or authenticated export to verify issuer, duration, restatement notes and merged headers. Review it with the other quarterly sample before proposing DB-STD-003 rules. Do not infer standalone-quarter amounts or declare the standard complete from this workbook alone.

