**********************
Windows PowerShell transcript start
Start time: 20261115231317
Username: DESKTOP-QGC44BJ\Papa
RunAs User: DESKTOP-QGC44BJ\Papa
Configuration Name: 
Machine: DESKTOP-QGC44BJ (Microsoft Windows NT 10.0.19045.0)
Host Application: C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
Process ID: 5020
PSVersion: 5.1.19041.6456
PSEdition: Desktop
PSCompatibleVersions: 1.0, 2.0, 3.0, 4.0, 5.0, 5.1.19041.6456
BuildVersion: 10.0.19041.6456
CLRVersion: 4.0.30319.42000
WSManStackVersion: 3.0
PSRemotingProtocolVersion: 2.3
SerializationVersion: 1.1.0.1
**********************
Transcript started, output file is D:\Winprojects\analyzer\row_pattern_audit_v2.txt
PS D:\Winprojects\analyzer>
(analyzer) python src/scripts/excel_table_row_pattern_audit.py --max-per-sheet 200 excel/cheshme.xlsx excel/fzar.xlsx excel/fzar2.xlsx excel/samanBank.xlsx excel/parsian_periodic.xlsx
[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=33
  row 33 [n=1 text=1 number=0 other=0] merges=A33:Q33: A33='توضيحات '
  row 34: <EMPTY>
  row 35: <EMPTY>
  row 36: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=38
  row 38 [n=1 text=1 number=0 other=0]: A38='صورت وضعيت پرتفوي سهام سایر شركت\u200cها'
  row 39: <EMPTY>
  row 40: <EMPTY>
  row 41: <EMPTY>

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=43
  row 43 [n=1 text=1 number=0 other=0]: A43='صورت وضعيت پرتفوي سهام ساير شركت\u200cها'
  row 44 [n=7 text=7 number=0 other=0] merges=A44:A45,B44:B45,C44:C45,D44:E44,F44:G44,H44:J44,K44:K45: A44='نام شرکت' |
B44='سرمایه (میلیون ریال)' | C44='ارزش اسمی هر سهم (ریال)' | D44='ابتدای دوره' | F44='تغییرات' | H44='انتهای دوره' | K44
='تشریح آخرین وضعیت، سیاست تقسیم سود و برنامه\u200cهای آتی در شرکت\u200cهای فرعی و واب...
  row 45 [n=7 text=7 number=0 other=0] merges=A44:A45,B44:B45,C44:C45,K44:K45: D45='تعداد سهام' | E45='بهای تمام شده' |
F45='تعداد سهام' | G45='بهای تمام شده' | H45='درصد مالکیت' | I45='بهای تمام شده' | J45='بهای تمام شده هر سهم (ریال)'
  row 46 [n=8 text=1 number=7 other=0]: A46='سرمايه گذاري بين المللي فريد گسترش ' | B46=1000 | C46=1000000 | D46=150 | E
46=15150 | F46=0 | G46=0 | I46=15150

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=66
  row 66 [n=1 text=1 number=0 other=0] merges=A66:M66: A66='توضيحات '
  row 67: <EMPTY>
  row 68: <EMPTY>
  row 69: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=71
  row 71 [n=1 text=1 number=0 other=0]: A71='صورت ريزمعاملات سهام - تحصیل شده'
  row 72: <EMPTY>
  row 73: <EMPTY>
  row 74: <EMPTY>

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=76
  row 76 [n=1 text=1 number=0 other=0]: A76='صورت ریز معاملات سهام تحصیل شده'
  row 77 [n=5 text=5 number=0 other=0]: A77='نام شرکت' | B77='تعداد سهام' | C77='بهاي تمام شده هر سهم (ريال)' | D77='کل
مبلغ بهاي تمام شده قابل معامله در بازار سرمايه' | E77='کل مبلغ بهاي تمام شده سهام ساير شرکتها'
  row 78 [n=4 text=1 number=3 other=0]: A78='صنعتي پارس مينو ' | B78=48000000 | D78=101541 | E78=0
  row 79 [n=4 text=1 number=3 other=0]: A79='کشت و دام گلدشت نمونه اصفهان ' | B79=7100000 | D79=76795 | E79=0

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=84
  row 84 [n=1 text=1 number=0 other=0] merges=A84:E84: A84='توجه: در صورت تغييرات در سرمايه گذاري برخي از شرکتها ناشي از
 اجراي افزايش سرمايه, مر...
  row 85: <EMPTY>
  row 86: <EMPTY>
  row 87: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=88
  row 88 [n=1 text=1 number=0 other=0]: A88='صورت ريزمعاملات سهام - واگذار شده'
  row 89: <EMPTY>
  row 90: <EMPTY>
  row 91: <EMPTY>

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=93
  row 93 [n=1 text=1 number=0 other=0]: A93='صورت ریز معاملات سهام واگذار شده'
  row 94 [n=7 text=7 number=0 other=0]: A94='نام شرکت' | B94='تعداد سهام' | C94='بهای تمام شده هر سهم (ریال)' | D94='کل
مبلغ بهای تمام شده' | E94='قیمت واگذاری هر سهم (ریال)' | F94='کل مبلغ واگذاری' | G94='سود (زیان) واگذاری'
  row 95 [n=4 text=1 number=3 other=0]: A95='جمع ' | D95=0 | F95=0 | G95=0
  row 96 [n=2 text=1 number=1 other=0] merges=A96:F96: A96='سود (زیان) فروش سهام غیرعملیاتی ' | G96=0

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=101
  row 101 [n=1 text=1 number=0 other=0]: A101='درآمد حاصل از سود سهام محقق شده'
  row 102: <EMPTY>
  row 103: <EMPTY>
  row 104: <EMPTY>

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=106
  row 106 [n=1 text=1 number=0 other=0]: A106='درآمد حاصل از سود سهام محقق شده'
  row 107 [n=3 text=3 number=0 other=0] merges=A107:A109,B107:G107,H107:K107: A107='نام شرکت' | B107='وضعیت پورتفوی' | H
107='وضعیت سودآوری'
  row 108 [n=9 text=9 number=0 other=0] merges=A107:A109,B108:B109,C108:C109,D108:D109,E108:E109,F108:F109,G108:G109,H10
8:H109,I108:I109,J108:K108: B108='سال مالی شرکت سرمایه پذیر' | C108='تاریخ برگزاری مجمع' | D108='تعداد سهام در تاریخ مجم
ع' | E108='سرمایه (میلیون ریال)' | F108='ارزش اسمی هر سهم (ریال)' | G108='درصد مالکیت' | H108='سود (زیان) هر سهم (ریال)'
 | I108='سود تقسیمی هر سهم (ریال)' | J108='درآمد حاصل از سود سهام مجمع برگزار شده و سال مالی شناسایی درآمد'
  row 109 [n=2 text=2 number=0 other=0] merges=A107:A109,B108:B109,C108:C109,D108:D109,E108:E109,F108:F109,G108:G109,H10
8:H109,I108:I109: J109='۱۴۰۵/۱۲/۲۹' | K109='* ۱۴۰۴/۱۲/۲۹'

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=116
  row 116 [n=1 text=1 number=0 other=0] merges=A116:K116: A116='*مبالغ ستون فوق مربوط به درآمد حاصل از سود سهام مجامع آن
 دسته از شرکت\u200cهای فرعی ...
  row 117 [n=1 text=1 number=0 other=0] merges=A117:K117: A117='کادر توضيحي مربوط به اطلاعات دوره ۱ ماهه منتهي به ۱۴۰۵/۰
۷/۳۰ '
  row 118: <EMPTY>
  row 119 [n=1 text=1 number=0 other=0] merges=A119:K119: A119='کادر توضيحي مربوط به اطلاعات تجمعي از ابتداي سال تا پايا
ن تاريخ ۱۴۰۵/۰۷/۳۰ '

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=117
  row 117 [n=1 text=1 number=0 other=0] merges=A117:K117: A117='کادر توضيحي مربوط به اطلاعات دوره ۱ ماهه منتهي به ۱۴۰۵/۰
۷/۳۰ '
  row 118: <EMPTY>
  row 119 [n=1 text=1 number=0 other=0] merges=A119:K119: A119='کادر توضيحي مربوط به اطلاعات تجمعي از ابتداي سال تا پايا
ن تاريخ ۱۴۰۵/۰۷/۳۰ '
  row 120: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=119
  row 119 [n=1 text=1 number=0 other=0] merges=A119:K119: A119='کادر توضيحي مربوط به اطلاعات تجمعي از ابتداي سال تا پايا
ن تاريخ ۱۴۰۵/۰۷/۳۰ '
  row 120: <EMPTY>
  row 121: <EMPTY>
  row 122: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=124
  row 124 [n=1 text=1 number=0 other=0]: A124='جزئیات درآمدهای عملیاتی و سرمایه گذاری\u200cهای شرکت'
  row 125: <EMPTY>
  row 126: <EMPTY>
  row 127: <EMPTY>

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=129
  row 129 [n=1 text=1 number=0 other=0]: A129='درآمدهای عملیاتی شرکت'
  row 130 [n=7 text=7 number=0 other=0]: A130='شرح' | B130='از ابتدای سال مالی تا پایان دوره منتهی به ۱۴۰۵/۰۶/۳۱' | C130
='اصلاحات' | D130='از ابتدای سال مالی تا پایان دوره منتهی به ۱۴۰۵/۰۶/۳۱ (اصلاح شده)' | E130='دوره ۱ ماهه منتهی به ۱۴۰۵/۰
۷/۳۰' | F130='از ابتدای سال مالی تا پایان دوره منتهی به ۱۴۰۵/۰۷/۳۰' | G130='سال مالی منتهی به ۱۴۰۴/۱۲/۲۹'
  row 131 [n=7 text=1 number=6 other=0]: A131='درآمد سود سهام ' | B131=750315 | C131=0 | D131=750315 | E131=0 | F131=750
315 | G131=13841355
  row 132 [n=7 text=1 number=6 other=0]: A132='درآمد سود تضمین شده ' | B132=0 | C132=0 | D132=0 | E132=0 | F132=0 | G132
=0

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=137
  row 137 [n=1 text=1 number=0 other=0]: A137='سرمایه گذاری های شرکت'
  row 138 [n=3 text=3 number=0 other=0] merges=A138:A139: A138='شرح' | B138='دوره مالی منتهی به ۱۴۰۵/۰۷/۳۰' | C138='سال
مالی منتهی به ۱۴۰۴/۱۲/۲۹'
  row 139 [n=2 text=2 number=0 other=0] merges=A138:A139: B139='بهای تمام شده' | C139='بهای تمام شده'
  row 140 [n=3 text=1 number=2 other=0]: A140='سهام شرکت های قابل معامله در بازار سرمایه (شرکت های پذیرفته شده در بورس و
 فرابورس، د... | B140=10207407 | C140=11232028

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=149
  row 149 [n=1 text=1 number=0 other=0] merges=A149:C149: A149='توضیحات '
  row 150: <EMPTY>
  row 151: <EMPTY>
  row 152: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=154
  row 154 [n=1 text=1 number=0 other=0]: A154='صورت وضعیت سایر سرمایه گذاری\u200cها'
  row 155: <EMPTY>
  row 156: <EMPTY>
  row 157: <EMPTY>

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=159
  row 159 [n=1 text=1 number=0 other=0]: A159='صورت وضعیت سایر سرمایه گذاری\u200cها'
  row 160 [n=4 text=4 number=0 other=0] merges=A160:A161,B160:D160,E160:G160,H160:K160: A160='شرح' | B160='ابتدای دوره'
| E160='خالص خرید (فروش) طی دوره' | H160='انتهای دوره'
  row 161 [n=10 text=10 number=0 other=0] merges=A160:A161: B161='تعداد' | C161='بهای تمام شده' | D161='ارزش بازار' | E1
61='تعداد' | F161='بهای تمام شده' | G161='سود (زیان) فروش' | H161='تعداد' | I161='بهای تمام شده' | J161='ارزش بازار' | K
161='افزایش (کاهش)'
  row 162 [n=1 text=1 number=0 other=0]: A162='سرمایه گذاری در واحدهای صندوق\u200cهای سرمایه\u200c گذاری: '

[DIRECT_NEXT_ROW_MIXED] anchor_row=162
  row 162 [n=1 text=1 number=0 other=0]: A162='سرمایه گذاری در واحدهای صندوق\u200cهای سرمایه\u200c گذاری: '
  row 163 [n=11 text=1 number=10 other=0]: A163='صندوق سرمايه گذاري مشترک صنعت و معدن ' | B163=403447 | C163=400000 | D1
63=401421 | E163=0 | F163=0 | G163=0 | H163=403447 | I163=400000 | J163=401421 | K163=1421
  row 164 [n=11 text=1 number=10 other=0]: A164='در اوراق بهادار با درآمد ثابت کيميا ' | B164=82107257 | C164=1457189 |
D164=2043485 | E164=0 | F164=0 | G164=0 | H164=82107257 | I164=1457189 | J164=2100310 | K164=643121
  row 165: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=167
  row 167 [n=1 text=1 number=0 other=0]: A167='سرمایه گذاری در اوراق مشتقه و تامین مالی: '
  row 168: <EMPTY>
  row 169 [n=11 text=1 number=10 other=0]: A169='جمع اوراق مشتقه و تأمین مالی ' | B169=0 | C169=0 | D169=0 | E169=0 | F1
69=0 | G169=0 | H169=0 | I169=0 | J169=0 | K169=0
  row 170 [n=1 text=1 number=0 other=0]: A170='سپرده\u200f هاى\u200c سرمايه \u200fگذارى بانکی: '

[DIRECT_NEXT_ROW_MIXED] anchor_row=170
  row 170 [n=1 text=1 number=0 other=0]: A170='سپرده\u200f هاى\u200c سرمايه \u200fگذارى بانکی: '
  row 171 [n=8 text=1 number=7 other=0]: A171='سپرده های ریالی ' | B171=0 | C171=0 | E171=0 | F171=0 | G171=0 | H171=0 |
 I171=0
  row 172 [n=8 text=1 number=7 other=0]: A172='سپرده های ارزی ' | B172=0 | C172=0 | E172=0 | F172=0 | G172=0 | H172=0 |
I172=0
  row 173 [n=8 text=1 number=7 other=0]: A173='جمع سپرده\u200f هاى\u200c سرمايه\u200f گذارى بانکی ' | B173=0 | C173=0 |
E173=0 | F173=0 | G173=0 | H173=0 | I173=0

[DIRECT_NEXT_ROW_MIXED] anchor_row=174
  row 174 [n=1 text=1 number=0 other=0]: A174='سرمایه\u200c گذاری در املاک: '
  row 175 [n=8 text=1 number=7 other=0]: A175='زمین ' | B175=0 | C175=0 | E175=0 | F175=0 | G175=0 | H175=0 | I175=0
  row 176 [n=8 text=1 number=7 other=0]: A176='ساختمان ' | B176=0 | C176=0 | E176=0 | F176=0 | G176=0 | H176=0 | I176=0
  row 177 [n=8 text=1 number=7 other=0]: A177='پروژه در جریان ساخت ' | B177=0 | C177=0 | E177=0 | F177=0 | G177=0 | H177
=0 | I177=0

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=183
  row 183 [n=1 text=1 number=0 other=0] merges=A183:K183: A183='توضیحات '
  row 184: <EMPTY>
  row 185: <EMPTY>
  row 186: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=188
  row 188 [n=1 text=1 number=0 other=0]: A188='صورت خلاصه سرمایه گذاری در سهام به تفکیک صنعت'
  row 189: <EMPTY>
  row 190: <EMPTY>
  row 191: <EMPTY>

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=193
  row 193 [n=1 text=1 number=0 other=0]: A193='صورت خلاصه سرمايه گذاري در سهام به تفکيک گروه صنعت'
  row 194 [n=4 text=4 number=0 other=0] merges=A194:A196,B194:I194,J194:N194,O194:V194: A194='شرح سرمايه گذاري' | B194='
سهام قابل معامله در بازار سرمايه' | J194='سهام ساير شرکتها' | O194='کل سرمايه گذاري در سهام'
  row 195 [n=9 text=9 number=0 other=0] merges=A194:A196,B195:D195,E195:F195,G195:I195,J195:K195,M195:N195,O195:Q195,R19
5:S195,T195:V195: B195='ابتداي دوره' | E195='تغييرات' | G195='انتهاي دوره' | J195='ابتداي دوره' | L195='تغييرات' | M195=
'انتهاي دوره' | O195='ابتداي دوره' | R195='تغييرات' | T195='انتهاي دوره'
  row 196 [n=21 text=21 number=0 other=0] merges=A194:A196: B196='تعداد شرکت' | C196='بهاي تمام شده' | D196='ارزش بازار'
 | E196='بهاي تمام شده' | F196='ارزش بازار' | G196='تعداد شرکت' | H196='بهاي تمام شده' | I196='ارزش بازار' | J196='تعداد
 شرکت' | K196='بهاي تمام شده' | L196='بهاي تمام شده' | M196='تعداد شرکت' | N196='بهاي تمام شده' | O196='تعداد شرکت' | P1
96='بهاي تمام شده' | Q196='درصد به کل' | R196='بهاي تمام شده' | S196='درصد به کل' | T196='تعداد شرکت' | U196='بهاي تمام
شده' | V196='درصد به کل'

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=220
  row 220 [n=1 text=1 number=0 other=0]: A220='ذخيره کاهش ارزش سرمايه گذاري در سهام '
  row 221 [n=1 text=1 number=0 other=0] merges=A221:V221: A221='لطفا دلايل مغايرت اطلاعات ابتداي دوره ي دوره جاري با اطل
اعات انتهاي دوره ي دوره قبل ...
  row 222: <EMPTY>
  row 223: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=221
  row 221 [n=1 text=1 number=0 other=0] merges=A221:V221: A221='لطفا دلايل مغايرت اطلاعات ابتداي دوره ي دوره جاري با اطل
اعات انتهاي دوره ي دوره قبل ...
  row 222: <EMPTY>
  row 223: <EMPTY>
  row 224: <EMPTY>

## WORKBOOK excel\fzar.xlsx
Reader: ACCEPTED
SHA-256: b8e1bd61d6f19a0d74f2243a9c4d5fa71945ebd0e0a3e1ad19834fc800abe3c7

### SHEET 1 Recovered_Sheet1 | used=A1:Z63 | populated_rows=48 | single_text_rows=18

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=3
  row 3 [n=1 text=1 number=0 other=0]: A3='گزارش فعالیت ماهانه'
  row 4: <EMPTY>
  row 5: <EMPTY>
  row 6: <EMPTY>

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=8
  row 8 [n=1 text=1 number=0 other=0]: A8='تولید و فروش'
  row 9 [n=1 text=1 number=0 other=0]: A9='کلیه مبالغ به میلیون ریال است'
  row 10 [n=8 text=8 number=0 other=0] merges=A10:B10,C10:F10,G10:I10,J10:M10,N10:Q10,R10:U10,V10:Y10,Z10:Z11: A10='شرح'
 | C10='از ابتدای سال مالی تا تاریخ ۱۴۰۵/۰۶/۳۱' | G10='اصلاحات' | J10='از ابتدای سال مالی تا تاریخ ۱۴۰۵/۰۶/۳۱ (اصلاح شده
)' | N10='دوره یک ماهه منتهی به ۱۴۰۵/۰۷/۳۰' | R10='از ابتدای سال مالی تا تاریخ ۱۴۰۵/۰۷/۳۰' | V10='از ابتدای سال مالی تا
تاریخ ۱۴۰۴/۰۷/۳۰' | Z10='وضعیت محصول-واحد'
  row 11 [n=25 text=25 number=0 other=0] merges=Z10:Z11: A11='نام محصول' | B11='واحد' | C11='تعداد تولید' | D11='تعداد ف
روش' | E11='نرخ فروش (ریال)' | F11='مبلغ فروش (میلیون ریال)' | G11='تعداد تولید' | H11='تعداد فروش' | I11='مبلغ فروش (می
لیون ریال)' | J11='تعداد تولید' | K11='تعداد فروش' | L11='نرخ فروش (ریال)' | M11='مبلغ فروش (میلیون ریال)' | N11='تعداد
تولید' | O11='تعداد فروش' | P11='نرخ فروش (ریال)' | Q11='مبلغ فروش (میلیون ریال)' | R11='تعداد تولید' | S11='تعداد فروش'
 | T11='نرخ فروش (ریال)' | U11='مبلغ فروش (میلیون ریال)' | V11='تعداد تولید' | W11='تعداد فروش' | X11='نرخ فروش (ریال)'
| Y11='مبلغ فروش (میلیون ریال)'

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=9
  row 9 [n=1 text=1 number=0 other=0]: A9='کلیه مبالغ به میلیون ریال است'
  row 10 [n=8 text=8 number=0 other=0] merges=A10:B10,C10:F10,G10:I10,J10:M10,N10:Q10,R10:U10,V10:Y10,Z10:Z11: A10='شرح'
 | C10='از ابتدای سال مالی تا تاریخ ۱۴۰۵/۰۶/۳۱' | G10='اصلاحات' | J10='از ابتدای سال مالی تا تاریخ ۱۴۰۵/۰۶/۳۱ (اصلاح شده
)' | N10='دوره یک ماهه منتهی به ۱۴۰۵/۰۷/۳۰' | R10='از ابتدای سال مالی تا تاریخ ۱۴۰۵/۰۷/۳۰' | V10='از ابتدای سال مالی تا
تاریخ ۱۴۰۴/۰۷/۳۰' | Z10='وضعیت محصول-واحد'
  row 11 [n=25 text=25 number=0 other=0] merges=Z10:Z11: A11='نام محصول' | B11='واحد' | C11='تعداد تولید' | D11='تعداد ف
روش' | E11='نرخ فروش (ریال)' | F11='مبلغ فروش (میلیون ریال)' | G11='تعداد تولید' | H11='تعداد فروش' | I11='مبلغ فروش (می
لیون ریال)' | J11='تعداد تولید' | K11='تعداد فروش' | L11='نرخ فروش (ریال)' | M11='مبلغ فروش (میلیون ریال)' | N11='تعداد
تولید' | O11='تعداد فروش' | P11='نرخ فروش (ریال)' | Q11='مبلغ فروش (میلیون ریال)' | R11='تعداد تولید' | S11='تعداد فروش'
 | T11='نرخ فروش (ریال)' | U11='مبلغ فروش (میلیون ریال)' | V11='تعداد تولید' | W11='تعداد فروش' | X11='نرخ فروش (ریال)'
| Y11='مبلغ فروش (میلیون ریال)'
  row 12 [n=1 text=1 number=0 other=0]: A12='فروش داخلی: '

[DIRECT_NEXT_ROW_MIXED] anchor_row=12
  row 12 [n=1 text=1 number=0 other=0]: A12='فروش داخلی: '
  row 13 [n=25 text=3 number=22 other=0]: A13='انواع سنگ پلاک تراورتن شکلاتي درجه ۳ ' | B13='متر مربع ' | C13=0 | D13=21
48 | E13=17754190 | F13=38136 | G13=0 | H13=0 | I13=0 | J13=0 | K13=2148 | L13=17754190 | M13=38136 | N13=0 | O13=0 | Q1
3=0 | R13=0 | S13=2148 | T13=17754190 | U13=38136 | V13=20916.08 | W13=11328.51 | X13=9208537 | Y13=104319 | Z13='توليد
'
  row 14 [n=26 text=3 number=23 other=0]: A14='برداشت کانسنگ طلا با عيار ۰/۳۷۵۹ گرم بر تن از محل باطله سنوات قبل ' | B14
='تن ' | C14=0 | D14=364022.73 | E14=19603040 | F14=7135952 | G14=0 | H14=0 | I14=0 | J14=0 | K14=364022.73 | L14=196030
40 | M14=7135952 | N14=0 | O14=95235.25 | P14=25853200 | Q14=2462136 | R14=0 | S14=459257.98 | T14=20899121 | U14=959808
8 | V14=0 | W14=373492.62 | X14=6840855 | Y14=2555009 | Z14='توليد '
  row 15 [n=26 text=3 number=23 other=0]: A15='استخراج سنگ تراورتن شکلاتي درجه ۳ ' | B15='تن ' | C15=1333 | D15=1914.87
| E15=26854565 | F15=51423 | G15=0 | H15=0 | I15=0 | J15=1333 | K15=1914.87 | L15=26854565 | M15=51423 | N15=955 | O15=5
06.36 | P15=31250494 | Q15=15824 | R15=2288 | S15=2421.23 | T15=27773900 | U15=67247 | V15=3445.47 | W15=4624.25 | X15=3
027518 | Y15=14000 | Z15='توليد '

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=21
  row 21 [n=1 text=1 number=0 other=0]: A21='فروش صادراتی: '
  row 22: <EMPTY>
  row 23 [n=19 text=1 number=18 other=0]: A23='جمع فروش صادراتی ' | C23=0 | D23=0 | F23=0 | G23=0 | H23=0 | I23=0 | J23=
0 | K23=0 | M23=0 | N23=0 | O23=0 | Q23=0 | R23=0 | S23=0 | U23=0 | V23=0 | W23=0 | Y23=0
  row 24 [n=1 text=1 number=0 other=0]: A24='درآمد ارائه خدمات: '

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=24
  row 24 [n=1 text=1 number=0 other=0]: A24='درآمد ارائه خدمات: '
  row 25: <EMPTY>
  row 26 [n=19 text=1 number=18 other=0]: A26='جمع درآمد ارائه خدمات ' | C26=0 | D26=0 | F26=0 | G26=0 | H26=0 | I26=0 |
 J26=0 | K26=0 | M26=0 | N26=0 | O26=0 | Q26=0 | R26=0 | S26=0 | U26=0 | V26=0 | W26=0 | Y26=0
  row 27 [n=1 text=1 number=0 other=0]: A27='برگشت از فروش: '

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=27
  row 27 [n=1 text=1 number=0 other=0]: A27='برگشت از فروش: '
  row 28: <EMPTY>
  row 29 [n=13 text=1 number=12 other=0]: A29='جمع برگشت از فروش ' | D29=0 | F29=0 | H29=0 | I29=0 | K29=0 | M29=0 | O29
=0 | Q29=0 | S29=0 | U29=0 | W29=0 | Y29=0
  row 30 [n=7 text=1 number=6 other=0]: A30='تخفيفات ' | F30=0 | I30=0 | M30=0 | Q30=0 | U30=0 | Y30=0

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=32
  row 32 [n=1 text=1 number=0 other=0]: A32='خرید مواد اولیه'
  row 33 [n=8 text=8 number=0 other=0] merges=A33:A34,B33:B34,C33:E33,F33:H33,I33:K33,L33:N33,O33:Q33,R33:T33: A33='شرح'
 | B33='واحد' | C33='از ابتدای سال مالی تا تاریخ ۱۴۰۵/۰۶/۳۱' | F33='اصلاحات' | I33='ازابتدای سال مالی تا تاریخ ۱۴۰۵/۰۶/۳
۱ (اصلاح شده)' | L33='خرید دوره یک ماهه منتهی به ۱۴۰۵/۰۷/۳۰' | O33='مواد اولیه خریداری شده از ابتدای دوره تا پایان دوره
منتهی به ۱۴۰۵/۰۷/۳۰' | R33='از ابتدای سال مالی تا تاریخ ۱۴۰۴/۰۷/۳۰'
  row 34 [n=18 text=18 number=0 other=0] merges=A33:A34,B33:B34: C34='مقدار' | D34='نرخ (ریال)' | E34='مبلغ (میلیون ریال
)' | F34='مقدار' | G34='نرخ (ريال)' | H34='مبلغ ( میلیون ریال)' | I34='مقدار' | J34='نرخ (ريال)' | K34='مبلغ (میلیون ریا
ل)' | L34='مقدار' | M34='نرخ (ريال)' | N34='مبلغ (میلیون ریال)' | O34='مقدار' | P34='نرخ (ريال)' | Q34='مبلغ (میلیون ریا
ل)' | R34='مقدار' | S34='نرخ (ريال)' | T34='مبلغ (میلیون ریال)'
  row 35 [n=1 text=1 number=0 other=0]: A35='مواد اولیه داخلی '

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=35
  row 35 [n=1 text=1 number=0 other=0]: A35='مواد اولیه داخلی '
  row 36: <EMPTY>
  row 37 [n=19 text=1 number=18 other=0]: A37='جمع مواد اولیه داخلی ' | C37=0 | D37=0 | E37=0 | F37=0 | G37=0 | H37=0 |
I37=0 | J37=0 | K37=0 | L37=0 | M37=0 | N37=0 | O37=0 | P37=0 | Q37=0 | R37=0 | S37=0 | T37=0
  row 38 [n=1 text=1 number=0 other=0]: A38='مواد اولیه وارداتی '

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=38
  row 38 [n=1 text=1 number=0 other=0]: A38='مواد اولیه وارداتی '
  row 39: <EMPTY>
  row 40 [n=19 text=1 number=18 other=0]: A40='جمع مواد اولیه وارداتی ' | C40=0 | D40=0 | E40=0 | F40=0 | G40=0 | H40=0
| I40=0 | J40=0 | K40=0 | L40=0 | M40=0 | N40=0 | O40=0 | P40=0 | Q40=0 | R40=0 | S40=0 | T40=0
  row 41 [n=19 text=1 number=18 other=0]: A41='جمع کل ' | C41=0 | D41=0 | E41=0 | F41=0 | G41=0 | H41=0 | I41=0 | J41=0
| K41=0 | L41=0 | M41=0 | N41=0 | O41=0 | P41=0 | Q41=0 | R41=0 | S41=0 | T41=0

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=42
  row 42 [n=1 text=1 number=0 other=0]: A42='انرژی'
  row 43 [n=12 text=12 number=0 other=0] merges=A43:A44,B43:B44,C43:C44,D43:D44,E43:G43,H43:J43,K43:M43,N43:P43,Q43:S43,
T43:V43,X43:X44: A43='صنعت' | B43='طبقه بندی' | C43='نوع انرژی' | D43='واحد اندازه گیری' | E43='از ابتدای سال مالی تا تا
ریخ ۱۴۰۵/۰۶/۳۱' | H43='اصلاحات' | K43='از ابتدای سال مالی تا تاریخ ۱۴۰۵/۰۶/۳۱ (اصلاح شده)' | N43='دوره یک ماهه منتهی به
۱۴۰۵/۰۷/۳۰' | Q43='از ابتدای سال مالی تا تاریخ ۱۴۰۵/۰۷/۳۰' | T43='از ابتدای سال مالی تا تاریخ ۱۴۰۴/۰۷/۳۰' | W43='مانده پ
یش بینی تا انتهای سال مالی ۱۴۰۵/۰۹/۳۰' | X43='توضیحات در خصوص علت تغییر میزان مصرف'
  row 44 [n=19 text=19 number=0 other=0] merges=A43:A44,B43:B44,C43:C44,D43:D44,X43:X44: E44='مقدار مصرف' | F44='نرخ - ر
یال' | G44='مبلغ - میلیون ریال' | H44='مقدار مصرف' | I44='نرخ - ریال' | J44='مبلغ - میلیون ریال' | K44='مقدار مصرف' | L4
4='نرخ - ریال' | M44='مبلغ - میلیون ریال' | N44='مقدار مصرف' | O44='نرخ - ریال' | P44='مبلغ - میلیون ریال' | Q44='مقدار
مصرف' | R44='نرخ - ریال' | S44='مبلغ - میلیون ریال' | T44='مقدار' | U44='نرخ - ریال' | V44='مبلغ' | W44='مقدار مصرف'
  row 45 [n=23 text=4 number=19 other=0]: A45='استخراج کانه هاي فلزي ' | B45='سوخت ' | C45='گاز سوخت ' | D45='مترمکعب '
| E45=2354 | F45=11470 | G45=27 | H45=0 | I45=0 | J45=0 | K45=2354 | L45=11470 | M45=27 | N45=0 | O45=0 | P45=0 | Q45=23
54 | R45=11470 | S45=27 | T45=2761 | U45=3984 | V45=11 | W45=1046

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=49
  row 49 [n=1 text=1 number=0 other=0]: A49='منابع و مصارف ارزی'
  row 50 [n=9 text=9 number=0 other=0] merges=A50:A51,B50:B51,C50:E50,F50:H50,I50:K50,L50:N50,O50:Q50,R50:T50,U50:W50: A
50='منابع ارزی' | B50='نوع ارز' | C50='از ابتدای سال مالی تا تاریخ ۱۴۰۵/۰۶/۳۱' | F50='اصلاحات' | I50='از ابتدای سال مالی
 تا تاریخ ۱۴۰۵/۰۶/۳۱ (اصلاح شده)' | L50='دوره یکماهه ۱۴۰۵/۰۷/۳۰' | O50='از ابتدای سال مالی تا تاریخ ۱۴۰۵/۰۷/۳۰' | R50='ا
ز ابتدای سال مالی تا تاریخ ۱۴۰۴/۰۷/۳۰' | U50='برآورد مانده تا پایان سال مالی ۱۴۰۵/۰۹/۳۰'
  row 51 [n=21 text=21 number=0 other=0] merges=A50:A51,B50:B51: C51='مبلغ ارزی' | D51='نرخ ارز(ریال)' | E51='مبلغ ریالی
(میلیون ریال)' | F51='مبلغ ارزی' | G51='نرخ ارز(ریال)' | H51='مبلغ ریالی(میلیون ریال)' | I51='مبلغ ارزی' | J51='نرخ ارز(
ریال)' | K51='مبلغ ریالی(میلیون ریال)' | L51='مبلغ ارزی' | M51='نرخ ارز(ریال)' | N51='مبلغ ریالی(میلیون ریال)' | O51='مب
لغ ارزی' | P51='نرخ ارز(ریال)' | Q51='مبلغ ریالی(میلیون ریال)' | R51='مبلغ ارزی' | S51='نرخ ارز(ریال)' | T51='مبلغ ریالی
(میلیون ریال)' | U51='مبلغ ارزی' | V51='نرخ ارز(ریال)' | W51='مبلغ ریالی(میلیون ریال)'
  row 52 [n=22 text=1 number=21 other=0]: A52='سایر ' | C52=0 | D52=0 | E52=0 | F52=0 | G52=0 | H52=0 | I52=0 | J52=0 |
K52=0 | L52=0 | M52=0 | N52=0 | O52=0 | P52=0 | Q52=0 | R52=0 | S52=0 | T52=0 | U52=0 | V52=0 | W52=0

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=54
  row 54 [n=1 text=1 number=0 other=0]: A54='مصارف ارزی: '
  row 55: <EMPTY>
  row 56 [n=22 text=1 number=21 other=0]: A56='سایر ' | C56=0 | D56=0 | E56=0 | F56=0 | G56=0 | H56=0 | I56=0 | J56=0 |
K56=0 | L56=0 | M56=0 | N56=0 | O56=0 | P56=0 | Q56=0 | R56=0 | S56=0 | T56=0 | U56=0 | V56=0 | W56=0
  row 57 [n=22 text=1 number=21 other=0]: A57='جمع مصارف ارزی ' | C57=0 | D57=0 | E57=0 | F57=0 | G57=0 | H57=0 | I57=0
| J57=0 | K57=0 | L57=0 | M57=0 | N57=0 | O57=0 | P57=0 | Q57=0 | R57=0 | S57=0 | T57=0 | U57=0 | V57=0 | W57=0

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=58
  row 58 [n=1 text=1 number=0 other=0]: A58='کادر توضیحات در مورد اصلاحات '
  row 59: <EMPTY>
  row 60 [n=1 text=1 number=0 other=0]: A60='کادر توضیحی مربوط به اطلاعات دوره ۱ ماهه منتهی به ۱۴۰۵/۰۷/۳۰ '
  row 61 [n=1 text=1 number=0 other=0]: A61='١-در خصوص كانسنگ طلا با عیار ٠/٣٧۵٩ گرم بر تن : مقدار فروش رفته فوق از محل
دپوي كانس...

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=60
  row 60 [n=1 text=1 number=0 other=0]: A60='کادر توضیحی مربوط به اطلاعات دوره ۱ ماهه منتهی به ۱۴۰۵/۰۷/۳۰ '
  row 61 [n=1 text=1 number=0 other=0]: A61='١-در خصوص كانسنگ طلا با عیار ٠/٣٧۵٩ گرم بر تن : مقدار فروش رفته فوق از محل
دپوي كانس...
  row 62 [n=1 text=1 number=0 other=0]: A62='کادر توضیحی مربوط اطلاعات تجمعی از ابتدای سال تا پایان مورخ ۱۴۰۵/۰۷/۳۰ '
  row 63 [n=1 text=1 number=0 other=0]: A63='-مجموع فروش شمش طلا در شرکت استحصال مواد معدنی تخت سلیمان (شرکت تابعه) تا پ
ایان مهر ...

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=61
  row 61 [n=1 text=1 number=0 other=0]: A61='١-در خصوص كانسنگ طلا با عیار ٠/٣٧۵٩ گرم بر تن : مقدار فروش رفته فوق از محل
دپوي كانس...
  row 62 [n=1 text=1 number=0 other=0]: A62='کادر توضیحی مربوط اطلاعات تجمعی از ابتدای سال تا پایان مورخ ۱۴۰۵/۰۷/۳۰ '
  row 63 [n=1 text=1 number=0 other=0]: A63='-مجموع فروش شمش طلا در شرکت استحصال مواد معدنی تخت سلیمان (شرکت تابعه) تا پ
ایان مهر ...
  row 64: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=62
  row 62 [n=1 text=1 number=0 other=0]: A62='کادر توضیحی مربوط اطلاعات تجمعی از ابتدای سال تا پایان مورخ ۱۴۰۵/۰۷/۳۰ '
  row 63 [n=1 text=1 number=0 other=0]: A63='-مجموع فروش شمش طلا در شرکت استحصال مواد معدنی تخت سلیمان (شرکت تابعه) تا پ
ایان مهر ...
  row 64: <EMPTY>
  row 65: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=63
  row 63 [n=1 text=1 number=0 other=0]: A63='-مجموع فروش شمش طلا در شرکت استحصال مواد معدنی تخت سلیمان (شرکت تابعه) تا پ
ایان مهر ...
  row 64: <EMPTY>
  row 65: <EMPTY>
  row 66: <EMPTY>

## WORKBOOK excel\fzar2.xlsx
Reader: ACCEPTED
SHA-256: 48272a0a5fe4635b9e7d877bf8748ae5a73cd3a025b1c055fd2ed582ac859a7f

### SHEET 1 Recovered_Sheet1 | used=A1:Z874 | populated_rows=671 | single_text_rows=162

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=3
  row 3 [n=1 text=1 number=0 other=0]: A3='صورت سود و زیان تلفیقی'
  row 4: <EMPTY>
  row 5: <EMPTY>
  row 6: <EMPTY>

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=8
  row 8 [n=1 text=1 number=0 other=0]: A8='صورت سود و زيان تلفيقي'
  row 9 [n=5 text=5 number=0 other=0] merges=A9:A10,E9:E10: A9='شرح' | B9='دوره منتهي به ۱۴۰۵/۰۳/۳۱' | C9='تجديد ارائه ش
ده دوره منتهي به ۱۴۰۴/۰۳/۳۱' | D9='تجديد ارائه شده دوره منتهي به ۱۴۰۴/۰۹/۳۰' | E9='درصد تغيير'
  row 10 [n=3 text=3 number=0 other=0] merges=A9:A10,E9:E10: B10='حسابرسی شده' | C10='حسابرسی شده' | D10='حسابرسی شده'
  row 11 [n=1 text=1 number=0 other=0]: A11='عمليات در حال تداوم: '

[DIRECT_NEXT_ROW_MIXED] anchor_row=11
  row 11 [n=1 text=1 number=0 other=0]: A11='عمليات در حال تداوم: '
  row 12 [n=5 text=1 number=4 other=0]: A12='درآمدهاي عملياتي ' | B12=48780966 | C12=19317656 | D12=53952825 | E12=153
  row 13 [n=5 text=1 number=4 other=0]: A13='بهاى تمام شده درآمدهاي عملياتي ' | B13=-3658393 | C13=-1783279 | D13=-57087
98 | E13=-105
  row 14 [n=5 text=1 number=4 other=0]: A14='سود(زيان) ناخالص ' | B14=45122573 | C14=17534377 | D14=48244027 | E14=157

[DIRECT_NEXT_ROW_MIXED] anchor_row=26
  row 26 [n=1 text=1 number=0 other=0]: A26='هزينه ماليات بر درآمد: '
  row 27 [n=5 text=1 number=4 other=0]: A27='سال جاري ' | B27=-514787 | C27=-208160 | D27=-40643 | E27=-147
  row 28 [n=5 text=1 number=4 other=0]: A28='سال\u200cهاي قبل ' | B28=-601256 | C28=-7094 | D28=-7094 | E28=-8376
  row 29 [n=5 text=1 number=4 other=0]: A29='سود(زيان) خالص عمليات در حال تداوم ' | B29=66493934 | C29=19184881 | D29=51
084741 | E29=247

[DIRECT_NEXT_ROW_MIXED] anchor_row=30
  row 30 [n=1 text=1 number=0 other=0]: A30='عمليات متوقف شده: '
  row 31 [n=4 text=1 number=3 other=0]: A31='سود (زيان) خالص عمليات متوقف شده ' | B31=0 | C31=0 | D31=0
  row 32 [n=5 text=1 number=4 other=0]: A32='سود(زيان) خالص ' | B32=66493934 | C32=19184881 | D32=51084741 | E32=247
  row 33 [n=1 text=1 number=0 other=0]: A33='قابل انتساب به : '

[DIRECT_NEXT_ROW_MIXED] anchor_row=33
  row 33 [n=1 text=1 number=0 other=0]: A33='قابل انتساب به : '
  row 34 [n=5 text=1 number=4 other=0]: A34='مالکان شرکت اصلي ' | B34=65237127 | C34=18838612 | D34=50150540 | E34=246
  row 35 [n=5 text=1 number=4 other=0]: A35='منافع فاقد حق کنترل ' | B35=1256807 | C35=346269 | D35=934201 | E35=263
  row 36 [n=1 text=1 number=0 other=0]: A36='سود پايه هر سهم: '

[DIRECT_NEXT_ROW_MIXED] anchor_row=36
  row 36 [n=1 text=1 number=0 other=0]: A36='سود پايه هر سهم: '
  row 37 [n=5 text=1 number=4 other=0]: A37='عملياتي (ريال) ' | B37=12035 | C37=3534 | D37=9527 | E37=241
  row 38 [n=5 text=2 number=3 other=0]: A38='غيرعملياتي (ريال) ' | B38=47 | C38=-45 | D38=-240 | E38='-- '
  row 39 [n=5 text=1 number=4 other=0]: A39='ناشي از عمليات در حال تداوم ' | B39=12082 | C39=3489 | D39=9287 | E39=246

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=45
  row 45 [n=1 text=1 number=0 other=0] merges=A45:F45: A45='دلايل تغييرات اطلاعات واقعي دوره منتهي به ۱۴۰۵/۰۳/۳۱ '
  row 46: <EMPTY>
  row 47 [n=1 text=1 number=0 other=0] merges=A47:F47: A47='دلايل تغييرات اطلاعات واقعي دوره منتهي به ۱۴۰۴/۰۳/۳۱ '
  row 48: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=47
  row 47 [n=1 text=1 number=0 other=0] merges=A47:F47: A47='دلايل تغييرات اطلاعات واقعي دوره منتهي به ۱۴۰۴/۰۳/۳۱ '
  row 48: <EMPTY>
  row 49 [n=1 text=1 number=0 other=0] merges=A49:F49: A49='دلايل تغييرات اطلاعات واقعي دوره منتهي به ۱۴۰۴/۰۹/۳۰ '
  row 50: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=49
  row 49 [n=1 text=1 number=0 other=0] merges=A49:F49: A49='دلايل تغييرات اطلاعات واقعي دوره منتهي به ۱۴۰۴/۰۹/۳۰ '
  row 50: <EMPTY>
  row 51: <EMPTY>
  row 52: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=54
  row 54 [n=1 text=1 number=0 other=0]: A54='صورت سود و زیان جامع تلفیقی'
  row 55: <EMPTY>
  row 56: <EMPTY>
  row 57: <EMPTY>

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=59
  row 59 [n=1 text=1 number=0 other=0]: A59='صورت سود و زيان جامع تلفيقي'
  row 60 [n=5 text=5 number=0 other=0] merges=A60:A61,E60:E61: A60='شرح' | B60='دوره منتهي به ۱۴۰۵/۰۳/۳۱' | C60='تجديد ا
رائه شده دوره منتهي به ۱۴۰۴/۰۳/۳۱' | D60='تجديد ارائه شده دوره منتهي به ۱۴۰۴/۰۹/۳۰' | E60='درصد تغيير'
  row 61 [n=3 text=3 number=0 other=0] merges=A60:A61,E60:E61: B61='حسابرسی شده' | C61='حسابرسی شده' | D61='حسابرسی شده'

  row 62 [n=5 text=1 number=4 other=0]: A62='سود(زيان) خالص ' | B62=66493934 | C62=19184881 | D62=51084741 | E62=247

[DIRECT_NEXT_ROW_MIXED] anchor_row=63
  row 63 [n=1 text=1 number=0 other=0]: A63='ساير اقلام سود و زيان جامع که در دوره هاي آتي به صورت سود و زيان تجديد طبقه
 بندي نخو...
  row 64 [n=4 text=1 number=3 other=0]: A64='مازاد تجديد ارزيابي دارايي\u200cهاي ثابت مشهود ' | B64=0 | C64=0 | D64=0
  row 65 [n=4 text=1 number=3 other=0]: A65='تفاوت تسعير ارز عمليات خارجي ' | B65=0 | C65=0 | D65=0
  row 66 [n=4 text=1 number=3 other=0]: A66='سهم گروه از ساير اقلام سود و زيان جامع مشارکت هاي خاص ' | B66=0 | C66=0 | D
66=0

[DIRECT_NEXT_ROW_MIXED] anchor_row=71
  row 71 [n=1 text=1 number=0 other=0]: A71='ساير اقلام سود و زيان جامع که در دوره هاي آتي به صورت سود و زيان تجديد طبقه
 بندي خوا...
  row 72 [n=4 text=1 number=3 other=0]: A72='سهم گروه از ساير اقلام سود و زيان جامع مشارکت هاي خاص ' | B72=0 | C72=0 | D
72=0
  row 73 [n=4 text=1 number=3 other=0]: A73='سهم گروه از ساير اقلام سود و زيان جامع شرکت هاي وابسته ' | B73=0 | C73=0 |
D73=0
  row 74 [n=4 text=1 number=3 other=0]: A74='ماليات بر درآمد اقلام فوق ' | B74=0 | C74=0 | D74=0

[DIRECT_NEXT_ROW_MIXED] anchor_row=78
  row 78 [n=1 text=1 number=0 other=0]: A78='قابل انتساب به : '
  row 79 [n=5 text=1 number=4 other=0]: A79='مالکان شرکت اصلي ' | B79=65237127 | C79=18838612 | D79=50150540 | E79=246
  row 80 [n=5 text=1 number=4 other=0]: A80='منافع فاقد حق کنترل ' | B80=1256807 | C80=346269 | D80=934201 | E80=263
  row 81 [n=1 text=1 number=0 other=0] merges=A81:F81: A81='توضيحات '

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=81
  row 81 [n=1 text=1 number=0 other=0] merges=A81:F81: A81='توضيحات '
  row 82: <EMPTY>
  row 83: <EMPTY>
  row 84: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=86
  row 86 [n=1 text=1 number=0 other=0]: A86='صورت وضعیت مالی تلفیقی'
  row 87: <EMPTY>
  row 88: <EMPTY>
  row 89: <EMPTY>

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=91
  row 91 [n=1 text=1 number=0 other=0]: A91='صورت وضعيت مالي تلفيقي'
  row 92 [n=5 text=5 number=0 other=0] merges=A92:A93,E92:E93: A92='شرح' | B92='به تاريخ ۱۴۰۵/۰۳/۳۱' | C92='تجديد ارائه
شده به تاريخ ۱۴۰۴/۰۹/۳۰' | D92='تجديد ارائه شده به تاريخ ۱۴۰۳/۱۰/۰۱' | E92='درصد تغيير'
  row 93 [n=3 text=3 number=0 other=0] merges=A92:A93,E92:E93: B93='حسابرسی شده' | C93='حسابرسی شده' | D93='حسابرسی شده'

  row 94 [n=1 text=1 number=0 other=0]: A94='دارايي\u200cها '

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=94
  row 94 [n=1 text=1 number=0 other=0]: A94='دارايي\u200cها '
  row 95 [n=1 text=1 number=0 other=0]: A95='دارايي\u200cهاي غيرجاري '
  row 96 [n=5 text=1 number=4 other=0]: A96='دارايي\u200cهاي ثابت مشهود ' | B96=4980382 | C96=4292782 | D96=4292782 | E9
6=16
  row 97 [n=4 text=1 number=3 other=0]: A97='سرمايه\u200cگذاري در املاک ' | B97=0 | C97=0 | D97=0

[DIRECT_NEXT_ROW_MIXED] anchor_row=95
  row 95 [n=1 text=1 number=0 other=0]: A95='دارايي\u200cهاي غيرجاري '
  row 96 [n=5 text=1 number=4 other=0]: A96='دارايي\u200cهاي ثابت مشهود ' | B96=4980382 | C96=4292782 | D96=4292782 | E9
6=16
  row 97 [n=4 text=1 number=3 other=0]: A97='سرمايه\u200cگذاري در املاک ' | B97=0 | C97=0 | D97=0
  row 98 [n=4 text=1 number=3 other=0]: A98='سرقفلي ' | B98=0 | C98=0 | D98=0

[DIRECT_NEXT_ROW_MIXED] anchor_row=106
  row 106 [n=1 text=1 number=0 other=0]: A106='دارايي\u200cهاي جاري '
  row 107 [n=5 text=1 number=4 other=0]: A107='سفارشات و پيش\u200cپرداخت\u200cها ' | B107=650631 | C107=121414 | D107=12
1414 | E107=436
  row 108 [n=5 text=1 number=4 other=0]: A108='موجودي مواد و کالا ' | B108=38024393 | C108=28111801 | D108=28111801 | E1
08=35
  row 109 [n=5 text=1 number=4 other=0]: A109='دريافتني\u200cهاي تجاري و ساير دريافتني\u200cها ' | B109=24429907 | C109=
31326107 | D109=31326107 | E109=-22

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=116
  row 116 [n=1 text=1 number=0 other=0]: A116='حقوق مالکانه و بدهي\u200cها '
  row 117 [n=1 text=1 number=0 other=0]: A117='حقوق مالکانه '
  row 118 [n=5 text=1 number=4 other=0]: A118='سرمايه ' | B118=5400000 | C118=5400000 | D118=5400000 | E118=0
  row 119 [n=4 text=1 number=3 other=0]: A119='افزايش سرمايه در جريان ' | B119=0 | C119=0 | D119=0

[DIRECT_NEXT_ROW_MIXED] anchor_row=117
  row 117 [n=1 text=1 number=0 other=0]: A117='حقوق مالکانه '
  row 118 [n=5 text=1 number=4 other=0]: A118='سرمايه ' | B118=5400000 | C118=5400000 | D118=5400000 | E118=0
  row 119 [n=4 text=1 number=3 other=0]: A119='افزايش سرمايه در جريان ' | B119=0 | C119=0 | D119=0
  row 120 [n=4 text=1 number=3 other=0]: A120='صرف سهام ' | B120=0 | C120=0 | D120=0

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=133
  row 133 [n=1 text=1 number=0 other=0]: A133='بدهي\u200cها '
  row 134 [n=1 text=1 number=0 other=0]: A134='بدهي\u200cهاي غيرجاري '
  row 135 [n=4 text=1 number=3 other=0]: A135='پرداختني\u200cهاي بلندمدت ' | B135=0 | C135=0 | D135=0
  row 136 [n=4 text=1 number=3 other=0]: A136='تسهيلات مالي بلندمدت ' | B136=0 | C136=0 | D136=0

[DIRECT_NEXT_ROW_MIXED] anchor_row=134
  row 134 [n=1 text=1 number=0 other=0]: A134='بدهي\u200cهاي غيرجاري '
  row 135 [n=4 text=1 number=3 other=0]: A135='پرداختني\u200cهاي بلندمدت ' | B135=0 | C135=0 | D135=0
  row 136 [n=4 text=1 number=3 other=0]: A136='تسهيلات مالي بلندمدت ' | B136=0 | C136=0 | D136=0
  row 137 [n=4 text=1 number=3 other=0]: A137='بدهي ماليات انتقالي ' | B137=0 | C137=0 | D137=0

[DIRECT_NEXT_ROW_MIXED] anchor_row=140
  row 140 [n=1 text=1 number=0 other=0]: A140='بدهي\u200cهاي جاري '
  row 141 [n=5 text=1 number=4 other=0]: A141='پرداختني\u200cهاي تجاري و ساير پرداختني\u200cها ' | B141=9340968 | C141=8
295887 | D141=8426210 | E141=13
  row 142 [n=5 text=1 number=4 other=0]: A142='ماليات پرداختني ' | B142=1554633 | C142=925988 | D142=925988 | E142=68
  row 143 [n=5 text=1 number=4 other=0]: A143='سود سهام پرداختني ' | B143=643488 | C143=237918 | D143=237918 | E143=170

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=155
  row 155 [n=1 text=1 number=0 other=0]: A155='صورت تغییرات در حقوق مالکانه تلفیقی'
  row 156: <EMPTY>
  row 157: <EMPTY>
  row 158: <EMPTY>

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=160
  row 160 [n=1 text=1 number=0 other=0]: A160='صورت تغييرات در حقوق مالکانه تلفيقي'
  row 161 [n=16 text=16 number=0 other=0]: A161='شرح' | B161='سرمايه' | C161='افزايش سرمايه در جريان' | D161='صرف سهام'
| E161='صرف سهام خزانه' | F161='آثار معاملات سهام خزانه شرکت فرعي' | G161='آثار معاملات با منافع فاقد حق کنترل' | H161='
اندوخته قانوني' | I161='ساير اندوخته\u200cها' | J161='مازاد تجديد ارزيابي دارايي\u200cها' | K161='تفاوت تسعير ارز عمليات
 خارجي' | L161='سود انباشته' | M161='سهام خزانه' | N161='قابل انتساب به مالکان شرکت اصلي' | O161='منافع فاقد حق کنترل' |
 P161='جمع حقوق مالکانه'
  row 162 [n=16 text=1 number=15 other=0]: A162='مانده در ۱۴۰۳/۱۰/۰۱ ' | B162=5400000 | C162=0 | D162=0 | E162=0 | F162=
0 | G162=0 | H162=540000 | I162=0 | J162=0 | K162=0 | L162=31267030 | M162=0 | N162=37207030 | O162=627903 | P162=378349
33
  row 163 [n=14 text=1 number=13 other=0]: A163='اصلاح اشتباهات ' | B163=0 | C163=0 | D163=0 | E163=0 | H163=0 | I163=0
| J163=0 | K163=0 | L163=0 | M163=0 | N163=0 | O163=0 | P163=0

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=211
  row 211 [n=1 text=1 number=0 other=0]: A211='صورت جریان های نقدی تلفیقی'
  row 212: <EMPTY>
  row 213: <EMPTY>
  row 214: <EMPTY>

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=216
  row 216 [n=1 text=1 number=0 other=0]: A216='صورت جريان هاي نقدي تلفيقي'
  row 217 [n=5 text=5 number=0 other=0] merges=A217:A218,E217:E218: A217='شرح' | B217='دوره منتهي به ۱۴۰۵/۰۳/۳۱' | C217=
'تجديد ارائه شده دوره منتهي به ۱۴۰۴/۰۳/۳۱' | D217='تجديد ارائه شده دوره منتهي به ۱۴۰۴/۰۹/۳۰' | E217='درصد تغيير'
  row 218 [n=3 text=3 number=0 other=0] merges=A217:A218,E217:E218: B218='حسابرسی شده' | C218='حسابرسی شده' | D218='حساب
رسی شده'
  row 219 [n=1 text=1 number=0 other=0]: A219='جريان\xadهاي نقدي حاصل از فعاليت\u200cهاي عملياتي: '

[DIRECT_NEXT_ROW_MIXED] anchor_row=219
  row 219 [n=1 text=1 number=0 other=0]: A219='جريان\xadهاي نقدي حاصل از فعاليت\u200cهاي عملياتي: '
  row 220 [n=5 text=1 number=4 other=0]: A220='نقد حاصل از عمليات ' | B220=64313762 | C220=12077128 | D220=35372933 | E2
20=433
  row 221 [n=5 text=1 number=4 other=0]: A221='پرداخت\u200cهاي نقدي بابت ماليات بر درآمد ' | B221=-487399 | C221=-565285
 | D221=-756535 | E221=14
  row 222 [n=5 text=1 number=4 other=0]: A222='جريان \u200cخالص \u200cورود\u200c (خروج) \u200cنقد حاصل از فعاليت\u200cها
ي \u200cعمل... | B222=63826363 | C222=11511843 | D222=34616398 | E222=454

[DIRECT_NEXT_ROW_MIXED] anchor_row=223
  row 223 [n=1 text=1 number=0 other=0]: A223='جريان\xadهاي نقدي حاصل از فعاليت\u200cهاي سرمايه\u200cگذاري: '
  row 224 [n=5 text=1 number=4 other=0]: A224='دريافت\u200cهاي نقدي حاصل از فروش دارايي\u200cهاي ثابت مشهود ' | B224=309
1 | C224=69417 | D224=81023 | E224=-96
  row 225 [n=5 text=1 number=4 other=0]: A225='پرداخت\u200cهاي نقدي براي خريد دارايي\u200cهاي ثابت مشهود ' | B225=-10403
26 | C225=-752847 | D225=-1301978 | E225=-38
  row 226 [n=4 text=1 number=3 other=0]: A226='دريافت\u200cهاي نقدي حاصل از فروش دارايي\u200cهاي غيرجاري نگهداري\u200cشد
ه براي فروش ' | B226=0 | C226=0 | D226=0

[DIRECT_NEXT_ROW_MIXED] anchor_row=246
  row 246 [n=1 text=1 number=0 other=0]: A246='جريان\xadهاي نقدي حاصل از فعاليت\u200cهاي تامين مالي: '
  row 247 [n=4 text=1 number=3 other=0]: A247='دريافت\u200cهاي نقدي حاصل از افزايش سرمايه شرکت اصلي ' | B247=0 | C247=0
| D247=0
  row 248 [n=4 text=1 number=3 other=0]: A248='دريافت\u200cهاي نقدي حاصل از صرف سهام ' | B248=0 | C248=0 | D248=0
  row 249 [n=4 text=1 number=3 other=0]: A249='دريافت\u200cهاي نقدي حاصل از افزايش سرمايه شرکت\u200cهاي فرعي- سهم منافع
فاقد حق کنت... | B249=0 | C249=0 | D249=0

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=275
  row 275 [n=1 text=1 number=0 other=0] merges=A275:F275: A275='دلايل تغييرات اطلاعات واقعي دوره منتهي به ۱۴۰۵/۰۳/۳۱ '
  row 276: <EMPTY>
  row 277 [n=1 text=1 number=0 other=0] merges=A277:F277: A277='دلايل تغييرات اطلاعات واقعي دوره منتهي به ۱۴۰۴/۰۳/۳۱ '
  row 278: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=277
  row 277 [n=1 text=1 number=0 other=0] merges=A277:F277: A277='دلايل تغييرات اطلاعات واقعي دوره منتهي به ۱۴۰۴/۰۳/۳۱ '
  row 278: <EMPTY>
  row 279 [n=1 text=1 number=0 other=0] merges=A279:F279: A279='دلايل تغييرات اطلاعات واقعي دوره منتهي به ۱۴۰۴/۰۹/۳۰ '
  row 280: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=279
  row 279 [n=1 text=1 number=0 other=0] merges=A279:F279: A279='دلايل تغييرات اطلاعات واقعي دوره منتهي به ۱۴۰۴/۰۹/۳۰ '
  row 280: <EMPTY>
  row 281: <EMPTY>
  row 282: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=284
  row 284 [n=1 text=1 number=0 other=0]: A284='صورت سود و زیان'
  row 285: <EMPTY>
  row 286: <EMPTY>
  row 287: <EMPTY>

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=289
  row 289 [n=1 text=1 number=0 other=0]: A289='صورت سود و زيان'
  row 290 [n=5 text=5 number=0 other=0] merges=A290:A291,E290:E291: A290='شرح' | B290='دوره منتهي به ۱۴۰۵/۰۳/۳۱' | C290=
'تجديد ارائه شده دوره منتهي به ۱۴۰۴/۰۳/۳۱' | D290='تجديد ارائه شده دوره منتهي به ۱۴۰۴/۰۹/۳۰' | E290='درصد تغيير'
  row 291 [n=3 text=3 number=0 other=0] merges=A290:A291,E290:E291: B291='حسابرسی شده' | C291='حسابرسی شده' | D291='حساب
رسی شده'
  row 292 [n=1 text=1 number=0 other=0]: A292='عمليات در حال تداوم: '

[DIRECT_NEXT_ROW_MIXED] anchor_row=292
  row 292 [n=1 text=1 number=0 other=0]: A292='عمليات در حال تداوم: '
  row 293 [n=5 text=1 number=4 other=0]: A293='درآمدهاي عملياتي ' | B293=10608198 | C293=2722392 | D293=22766727 | E293=
290
  row 294 [n=5 text=1 number=4 other=0]: A294='بهاى تمام شده درآمدهاي عملياتي ' | B294=-7545045 | C294=-1905619 | D294=-
13534520 | E294=-296
  row 295 [n=5 text=1 number=4 other=0]: A295='سود(زيان) ناخالص ' | B295=3063153 | C295=816773 | D295=9232207 | E295=275


[DIRECT_NEXT_ROW_MIXED] anchor_row=304
  row 304 [n=1 text=1 number=0 other=0]: A304='هزينه ماليات بر درآمد: '
  row 305 [n=5 text=1 number=4 other=0]: A305='سال جاري ' | B305=-514016 | C305=-208160 | D305=-35376 | E305=-147
  row 306 [n=5 text=1 number=4 other=0]: A306='سال\u200cهاي قبل ' | B306=-550290 | C306=-2012 | D306=-2012 | E306=-27250

  row 307 [n=5 text=1 number=4 other=0]: A307='سود(زيان) خالص عمليات در حال تداوم ' | B307=1783798 | C307=748773 | D307=
50287149 | E307=138

[DIRECT_NEXT_ROW_MIXED] anchor_row=308
  row 308 [n=1 text=1 number=0 other=0]: A308='عمليات متوقف شده: '
  row 309 [n=4 text=1 number=3 other=0]: A309='سود (زيان) خالص عمليات متوقف شده ' | B309=0 | C309=0 | D309=0
  row 310 [n=5 text=1 number=4 other=0]: A310='سود(زيان) خالص ' | B310=1783798 | C310=748773 | D310=50287149 | E310=138
  row 311 [n=1 text=1 number=0 other=0]: A311='سود(زيان) پايه هر سهم: '

[DIRECT_NEXT_ROW_MIXED] anchor_row=311
  row 311 [n=1 text=1 number=0 other=0]: A311='سود(زيان) پايه هر سهم: '
  row 312 [n=5 text=1 number=4 other=0]: A312='عملياتي (ريال) ' | B312=334 | C312=133 | D312=9340 | E312=151
  row 313 [n=5 text=2 number=3 other=0]: A313='غيرعملياتي (ريال) ' | B313=-4 | C313=6 | D313=-28 | E313='-- '
  row 314 [n=5 text=1 number=4 other=0]: A314='ناشي از عمليات در حال تداوم ' | B314=330 | C314=139 | D314=9312 | E314=13
7

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=320
  row 320 [n=1 text=1 number=0 other=0] merges=A320:F320: A320='دلايل تغييرات اطلاعات واقعي دوره منتهي به ۱۴۰۵/۰۳/۳۱ '
  row 321: <EMPTY>
  row 322 [n=1 text=1 number=0 other=0] merges=A322:F322: A322='دلايل تغييرات اطلاعات واقعي دوره منتهي به ۱۴۰۴/۰۳/۳۱ '
  row 323: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=322
  row 322 [n=1 text=1 number=0 other=0] merges=A322:F322: A322='دلايل تغييرات اطلاعات واقعي دوره منتهي به ۱۴۰۴/۰۳/۳۱ '
  row 323: <EMPTY>
  row 324 [n=1 text=1 number=0 other=0] merges=A324:F324: A324='دلايل تغييرات اطلاعات واقعي دوره منتهي به ۱۴۰۴/۰۹/۳۰ '
  row 325: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=324
  row 324 [n=1 text=1 number=0 other=0] merges=A324:F324: A324='دلايل تغييرات اطلاعات واقعي دوره منتهي به ۱۴۰۴/۰۹/۳۰ '
  row 325: <EMPTY>
  row 326: <EMPTY>
  row 327: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=329
  row 329 [n=1 text=1 number=0 other=0]: A329='صورت سود و زیان جامع'
  row 330: <EMPTY>
  row 331: <EMPTY>
  row 332: <EMPTY>

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=334
  row 334 [n=1 text=1 number=0 other=0]: A334='صورت سود و زيان جامع'
  row 335 [n=1 text=1 number=0 other=0]: A335='کليه مبالغ به ميليون ريال است'
  row 336 [n=5 text=5 number=0 other=0] merges=A336:A337,E336:E337: A336='شرح' | B336='دوره منتهي به ۱۴۰۵/۰۳/۳۱' | C336=
'تجديد ارائه شده دوره منتهي به ۱۴۰۴/۰۳/۳۱' | D336='تجديد ارائه شده دوره منتهي به ۱۴۰۴/۰۹/۳۰' | E336='درصد تغيير'
  row 337 [n=3 text=3 number=0 other=0] merges=A336:A337,E336:E337: B337='حسابرسی شده' | C337='حسابرسی شده' | D337='حساب
رسی شده'

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=335
  row 335 [n=1 text=1 number=0 other=0]: A335='کليه مبالغ به ميليون ريال است'
  row 336 [n=5 text=5 number=0 other=0] merges=A336:A337,E336:E337: A336='شرح' | B336='دوره منتهي به ۱۴۰۵/۰۳/۳۱' | C336=
'تجديد ارائه شده دوره منتهي به ۱۴۰۴/۰۳/۳۱' | D336='تجديد ارائه شده دوره منتهي به ۱۴۰۴/۰۹/۳۰' | E336='درصد تغيير'
  row 337 [n=3 text=3 number=0 other=0] merges=A336:A337,E336:E337: B337='حسابرسی شده' | C337='حسابرسی شده' | D337='حساب
رسی شده'
  row 338 [n=5 text=1 number=4 other=0]: A338='سود(زيان) خالص ' | B338=1783798 | C338=748773 | D338=50287149 | E338=138

[DIRECT_NEXT_ROW_MIXED] anchor_row=339
  row 339 [n=1 text=1 number=0 other=0]: A339='ساير اقلام سود و زيان جامع که در دوره هاي آتي به صورت سود و زيان تجديد طب
قه بندي نخو...
  row 340 [n=4 text=1 number=3 other=0]: A340='مازاد تجديد ارزيابي دارايي\u200cهاي ثابت مشهود ' | B340=0 | C340=0 | D340
=0
  row 341 [n=4 text=1 number=3 other=0]: A341='تفاوت تسعير ارز عمليات خارجي ' | B341=0 | C341=0 | D341=0
  row 342 [n=4 text=1 number=3 other=0]: A342='ساير ' | B342=0 | C342=0 | D342=0

[DIRECT_NEXT_ROW_MIXED] anchor_row=345
  row 345 [n=1 text=1 number=0 other=0]: A345='ساير اقلام سود و زيان جامع که در دوره هاي آتي به صورت سود و زيان تجديد طب
قه بندي خوا...
  row 346 [n=4 text=1 number=3 other=0]: A346='ساير ' | B346=0 | C346=0 | D346=0
  row 347 [n=4 text=1 number=3 other=0]: A347='ماليات بر درآمد اقلام فوق ' | B347=0 | C347=0 | D347=0
  row 348 [n=4 text=1 number=3 other=0]: A348='جمع ' | B348=0 | C348=0 | D348=0

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=351
  row 351 [n=1 text=1 number=0 other=0] merges=A351:F351: A351='توضيحات '
  row 352: <EMPTY>
  row 353: <EMPTY>
  row 354: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=356
  row 356 [n=1 text=1 number=0 other=0]: A356='صورت وضعیت مالی'
  row 357: <EMPTY>
  row 358: <EMPTY>
  row 359: <EMPTY>

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=361
  row 361 [n=1 text=1 number=0 other=0]: A361='صورت وضعيت مالي'
  row 362 [n=1 text=1 number=0 other=0]: A362='کليه مبالغ به ميليون ريال است'
  row 363 [n=5 text=5 number=0 other=0] merges=A363:A364,E363:E364: A363='شرح' | B363='به تاريخ ۱۴۰۵/۰۳/۳۱' | C363='تجدي
د ارائه شده به تاريخ ۱۴۰۴/۰۹/۳۰' | D363='تجديد ارائه شده به تاريخ ۱۴۰۳/۱۰/۰۱' | E363='درصد تغيير'
  row 364 [n=3 text=3 number=0 other=0] merges=A363:A364,E363:E364: B364='حسابرسی شده' | C364='حسابرسی شده' | D364='حساب
رسی شده'

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=362
  row 362 [n=1 text=1 number=0 other=0]: A362='کليه مبالغ به ميليون ريال است'
  row 363 [n=5 text=5 number=0 other=0] merges=A363:A364,E363:E364: A363='شرح' | B363='به تاريخ ۱۴۰۵/۰۳/۳۱' | C363='تجدي
د ارائه شده به تاريخ ۱۴۰۴/۰۹/۳۰' | D363='تجديد ارائه شده به تاريخ ۱۴۰۳/۱۰/۰۱' | E363='درصد تغيير'
  row 364 [n=3 text=3 number=0 other=0] merges=A363:A364,E363:E364: B364='حسابرسی شده' | C364='حسابرسی شده' | D364='حساب
رسی شده'
  row 365 [n=1 text=1 number=0 other=0]: A365='دارايي\u200cها '

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=365
  row 365 [n=1 text=1 number=0 other=0]: A365='دارايي\u200cها '
  row 366 [n=1 text=1 number=0 other=0]: A366='دارايي\u200cهاي غيرجاري '
  row 367 [n=5 text=1 number=4 other=0]: A367='دارايي\u200cهاي ثابت مشهود ' | B367=3477297 | C367=2846056 | D367=2348091
 | E367=22
  row 368 [n=4 text=1 number=3 other=0]: A368='سرمايه\u200cگذاري در املاک ' | B368=0 | C368=0 | D368=0

[DIRECT_NEXT_ROW_MIXED] anchor_row=366
  row 366 [n=1 text=1 number=0 other=0]: A366='دارايي\u200cهاي غيرجاري '
  row 367 [n=5 text=1 number=4 other=0]: A367='دارايي\u200cهاي ثابت مشهود ' | B367=3477297 | C367=2846056 | D367=2348091
 | E367=22
  row 368 [n=4 text=1 number=3 other=0]: A368='سرمايه\u200cگذاري در املاک ' | B368=0 | C368=0 | D368=0
  row 369 [n=5 text=1 number=4 other=0]: A369='دارايي\u200cهاي نامشهود ' | B369=12806 | C369=11921 | D369=14494 | E369=7


[DIRECT_NEXT_ROW_MIXED] anchor_row=375
  row 375 [n=1 text=1 number=0 other=0]: A375='دارايي\u200cهاي جاري '
  row 376 [n=5 text=1 number=4 other=0]: A376='سفارشات و پيش\u200cپرداخت\u200cها ' | B376=430857 | C376=91645 | D376=325
65 | E376=370
  row 377 [n=5 text=1 number=4 other=0]: A377='موجودي مواد و کالا ' | B377=2973748 | C377=1419882 | D377=619366 | E377=1
09
  row 378 [n=5 text=1 number=4 other=0]: A378='دريافتني\u200cهاي تجاري و ساير دريافتني\u200cها ' | B378=8254816 | C378=5
7286869 | D378=31070220 | E378=-86

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=385
  row 385 [n=1 text=1 number=0 other=0]: A385='حقوق مالکانه و بدهي\u200cها '
  row 386 [n=1 text=1 number=0 other=0]: A386='حقوق مالکانه '
  row 387 [n=5 text=1 number=4 other=0]: A387='سرمايه ' | B387=5400000 | C387=5400000 | D387=5400000 | E387=0
  row 388 [n=4 text=1 number=3 other=0]: A388='افزايش سرمايه در جريان ' | B388=0 | C388=0 | D388=0

[DIRECT_NEXT_ROW_MIXED] anchor_row=386
  row 386 [n=1 text=1 number=0 other=0]: A386='حقوق مالکانه '
  row 387 [n=5 text=1 number=4 other=0]: A387='سرمايه ' | B387=5400000 | C387=5400000 | D387=5400000 | E387=0
  row 388 [n=4 text=1 number=3 other=0]: A388='افزايش سرمايه در جريان ' | B388=0 | C388=0 | D388=0
  row 389 [n=4 text=1 number=3 other=0]: A389='صرف سهام ' | B389=0 | C389=0 | D389=0

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=398
  row 398 [n=1 text=1 number=0 other=0]: A398='بدهي\u200cها '
  row 399 [n=1 text=1 number=0 other=0]: A399='بدهي\u200cهاي غيرجاري '
  row 400 [n=4 text=1 number=3 other=0]: A400='پرداختني\u200cهاي بلندمدت ' | B400=0 | C400=0 | D400=0
  row 401 [n=4 text=1 number=3 other=0]: A401='تسهيلات مالي بلندمدت ' | B401=0 | C401=0 | D401=0

[DIRECT_NEXT_ROW_MIXED] anchor_row=399
  row 399 [n=1 text=1 number=0 other=0]: A399='بدهي\u200cهاي غيرجاري '
  row 400 [n=4 text=1 number=3 other=0]: A400='پرداختني\u200cهاي بلندمدت ' | B400=0 | C400=0 | D400=0
  row 401 [n=4 text=1 number=3 other=0]: A401='تسهيلات مالي بلندمدت ' | B401=0 | C401=0 | D401=0
  row 402 [n=4 text=1 number=3 other=0]: A402='بدهي ماليات انتقالي ' | B402=0 | C402=0 | D402=0

[DIRECT_NEXT_ROW_MIXED] anchor_row=405
  row 405 [n=1 text=1 number=0 other=0]: A405='بدهي\u200cهاي جاري '
  row 406 [n=5 text=1 number=4 other=0]: A406='پرداختني\u200cهاي تجاري و ساير پرداختني\u200cها ' | B406=8081118 | C406=7
402045 | D406=3677828 | E406=9
  row 407 [n=5 text=1 number=4 other=0]: A407='ماليات پرداختني ' | B407=923517 | C407=35376 | D407=8598 | E407=2511
  row 408 [n=5 text=1 number=4 other=0]: A408='سود سهام پرداختني ' | B408=643488 | C408=237918 | D408=504858 | E408=170

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=420
  row 420 [n=1 text=1 number=0 other=0]: A420='صورت تغییرات در حقوق مالکانه'
  row 421: <EMPTY>
  row 422: <EMPTY>
  row 423: <EMPTY>

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=425
  row 425 [n=1 text=1 number=0 other=0]: A425='صورت تغييرات در حقوق مالکانه'
  row 426 [n=1 text=1 number=0 other=0]: A426='کليه مبالغ به ميليون ريال است'
  row 427 [n=12 text=12 number=0 other=0]: A427='شرح' | B427='سرمايه' | C427='افزايش سرمايه در جريان' | D427='صرف سهام'
| E427='صرف سهام خزانه' | F427='اندوخته قانوني' | G427='ساير اندوخته\u200cها' | H427='مازاد تجديد ارزيابي دارايي\u200cها
' | I427='تفاوت تسعير ارز عمليات خارجي' | J427='سود انباشته' | K427='سهام خزانه' | L427='جمع کل'
  row 428 [n=12 text=1 number=11 other=0]: A428='مانده در ۱۴۰۳/۱۰/۰۱ ' | B428=5400000 | C428=0 | D428=0 | E428=0 | F428=
540000 | G428=0 | H428=0 | I428=0 | J428=31427418 | K428=0 | L428=37367418

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=426
  row 426 [n=1 text=1 number=0 other=0]: A426='کليه مبالغ به ميليون ريال است'
  row 427 [n=12 text=12 number=0 other=0]: A427='شرح' | B427='سرمايه' | C427='افزايش سرمايه در جريان' | D427='صرف سهام'
| E427='صرف سهام خزانه' | F427='اندوخته قانوني' | G427='ساير اندوخته\u200cها' | H427='مازاد تجديد ارزيابي دارايي\u200cها
' | I427='تفاوت تسعير ارز عمليات خارجي' | J427='سود انباشته' | K427='سهام خزانه' | L427='جمع کل'
  row 428 [n=12 text=1 number=11 other=0]: A428='مانده در ۱۴۰۳/۱۰/۰۱ ' | B428=5400000 | C428=0 | D428=0 | E428=0 | F428=
540000 | G428=0 | H428=0 | I428=0 | J428=31427418 | K428=0 | L428=37367418
  row 429 [n=12 text=1 number=11 other=0]: A429='اصلاح اشتباهات ' | B429=0 | C429=0 | D429=0 | E429=0 | F429=0 | G429=0
| H429=0 | I429=0 | J429=0 | K429=0 | L429=0

[DIRECT_NEXT_ROW_MIXED] anchor_row=432
  row 432 [n=1 text=1 number=0 other=0]: A432='تغييرات حقوق مالکانه در سال ۱۴۰۴/۰۹/۳۰ '
  row 433 [n=3 text=1 number=2 other=0]: A433='سود(زيان) خالص گزارش شده در صورت\u200cهاي مالي سال ۱۴۰۴/۰۹/۳۰ ' | J433=50
287149 | L433=50287149
  row 434 [n=12 text=1 number=11 other=0]: A434='اصلاح اشتباهات ' | B434=0 | C434=0 | D434=0 | E434=0 | F434=0 | G434=0
| H434=0 | I434=0 | J434=130323 | K434=0 | L434=130323
  row 435 [n=12 text=1 number=11 other=0]: A435='تغيير در رويه\u200cهاي حسابداري ' | B435=0 | C435=0 | D435=0 | E435=0 |
 F435=0 | G435=0 | H435=0 | I435=0 | J435=0 | K435=0 | L435=0

[DIRECT_NEXT_ROW_MIXED] anchor_row=448
  row 448 [n=1 text=1 number=0 other=0]: A448='تغييرات حقوق مالکانه در دوره ۶ ماهه منتهي به ۱۴۰۵/۰۳/۳۱ '
  row 449 [n=3 text=1 number=2 other=0]: A449='سود (زيان) خالص در دوره ۶ ماهه منتهي به ۱۴۰۵/۰۳/۳۱ ' | J449=1783798 | L44
9=1783798
  row 450 [n=4 text=1 number=3 other=0]: A450='ساير اقلام سود و زيان جامع پس از کسر ماليات ' | H450=0 | I450=0 | L450=0
  row 451 [n=12 text=1 number=11 other=0]: A451='سود (زيان) جامع در دوره ۶ ماهه منتهي به ۱۴۰۵/۰۳/۳۱ ' | B451=0 | C451=0
| D451=0 | E451=0 | F451=0 | G451=0 | H451=0 | I451=0 | J451=1783798 | K451=0 | L451=1783798

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=464
  row 464 [n=1 text=1 number=0 other=0]: A464='صورت جریان های نقدی'
  row 465: <EMPTY>
  row 466: <EMPTY>
  row 467: <EMPTY>

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=469
  row 469 [n=1 text=1 number=0 other=0]: A469='صورت جريان\u200cهاي نقدي'
  row 470 [n=1 text=1 number=0 other=0]: A470='کليه مبالغ به ميليون ريال است'
  row 471 [n=5 text=5 number=0 other=0] merges=A471:A472,E471:E472: A471='شرح' | B471='دوره منتهي به ۱۴۰۵/۰۳/۳۱' | C471=
'تجديد ارائه شده دوره منتهي به ۱۴۰۴/۰۳/۳۱' | D471='تجديد ارائه شده دوره منتهي به ۱۴۰۴/۰۹/۳۰' | E471='درصد تغيير'
  row 472 [n=3 text=3 number=0 other=0] merges=A471:A472,E471:E472: B472='حسابرسی شده' | C472='حسابرسی شده' | D472='حساب
رسی شده'

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=470
  row 470 [n=1 text=1 number=0 other=0]: A470='کليه مبالغ به ميليون ريال است'
  row 471 [n=5 text=5 number=0 other=0] merges=A471:A472,E471:E472: A471='شرح' | B471='دوره منتهي به ۱۴۰۵/۰۳/۳۱' | C471=
'تجديد ارائه شده دوره منتهي به ۱۴۰۴/۰۳/۳۱' | D471='تجديد ارائه شده دوره منتهي به ۱۴۰۴/۰۹/۳۰' | E471='درصد تغيير'
  row 472 [n=3 text=3 number=0 other=0] merges=A471:A472,E471:E472: B472='حسابرسی شده' | C472='حسابرسی شده' | D472='حساب
رسی شده'
  row 473 [n=1 text=1 number=0 other=0]: A473='جريان\xadهاي نقدي حاصل از فعاليت\u200cهاي عملياتي: '

[DIRECT_NEXT_ROW_MIXED] anchor_row=473
  row 473 [n=1 text=1 number=0 other=0]: A473='جريان\xadهاي نقدي حاصل از فعاليت\u200cهاي عملياتي: '
  row 474 [n=5 text=1 number=4 other=0]: A474='نقد حاصل از عمليات ' | B474=49733213 | C474=9807563 | D474=27692127 | E47
4=407
  row 475 [n=5 text=1 number=4 other=0]: A475='پرداخت\u200cهاي نقدي بابت ماليات بر درآمد ' | B475=-176166 | C475=-10610
| D475=-10610 | E475=-1560
  row 476 [n=5 text=1 number=4 other=0]: A476='جريان \u200cخالص \u200cورود\u200c (خروج) \u200cنقد حاصل از فعاليت\u200cها
ي \u200cعمل... | B476=49557047 | C476=9796953 | D476=27681517 | E476=406

[DIRECT_NEXT_ROW_MIXED] anchor_row=477
  row 477 [n=1 text=1 number=0 other=0]: A477='جريان\xadهاي نقدي حاصل از فعاليت\u200cهاي سرمايه\u200cگذاري: '
  row 478 [n=5 text=2 number=3 other=0]: A478='دريافت\u200cهاي نقدي حاصل از فروش دارايي\u200cهاي ثابت مشهود ' | B478=0 |
 C478=69417 | D478=73650 | E478='-- '
  row 479 [n=5 text=1 number=4 other=0]: A479='پرداخت\u200cهاي نقدي براي خريد دارايي\u200cهاي ثابت مشهود ' | B479=-89073
2 | C479=-658782 | D479=-1003150 | E479=-35
  row 480 [n=4 text=1 number=3 other=0]: A480='دريافت\u200cهاي نقدي حاصل از فروش دارايي\u200cهاي غيرجاري نگهداري\u200cشد
ه براي فروش ' | B480=0 | C480=0 | D480=0

[DIRECT_NEXT_ROW_MIXED] anchor_row=496
  row 496 [n=1 text=1 number=0 other=0]: A496='جريان\xadهاي نقدي حاصل از فعاليت\u200cهاي تامين مالي: '
  row 497 [n=4 text=1 number=3 other=0]: A497='دريافت\u200cهاي نقدي حاصل از افزايش سرمايه ' | B497=0 | C497=0 | D497=0
  row 498 [n=4 text=1 number=3 other=0]: A498='دريافت\u200cهاي نقدي حاصل از صرف سهام ' | B498=0 | C498=0 | D498=0
  row 499 [n=4 text=1 number=3 other=0]: A499='دريافت\u200cهاي نقدي حاصل از فروش سهام خزانه ' | B499=0 | C499=0 | D499=0


[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=519
  row 519 [n=1 text=1 number=0 other=0] merges=A519:F519: A519='دلايل تغييرات اطلاعات واقعي دوره منتهي به ۱۴۰۵/۰۳/۳۱ '
  row 520: <EMPTY>
  row 521 [n=1 text=1 number=0 other=0] merges=A521:F521: A521='دلايل تغييرات اطلاعات واقعي دوره منتهي به ۱۴۰۴/۰۳/۳۱ '
  row 522: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=521
  row 521 [n=1 text=1 number=0 other=0] merges=A521:F521: A521='دلايل تغييرات اطلاعات واقعي دوره منتهي به ۱۴۰۴/۰۳/۳۱ '
  row 522: <EMPTY>
  row 523 [n=1 text=1 number=0 other=0] merges=A523:F523: A523='دلايل تغييرات اطلاعات واقعي دوره منتهي به ۱۴۰۴/۰۹/۳۰ '
  row 524: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=523
  row 523 [n=1 text=1 number=0 other=0] merges=A523:F523: A523='دلايل تغييرات اطلاعات واقعي دوره منتهي به ۱۴۰۴/۰۹/۳۰ '
  row 524: <EMPTY>
  row 525: <EMPTY>
  row 526: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=528
  row 528 [n=1 text=1 number=0 other=0]: A528='خلاصه اطلاعات گزارش تفسیری - صفحه 1'
  row 529: <EMPTY>
  row 530: <EMPTY>
  row 531: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=533
  row 533 [n=1 text=1 number=0 other=0] merges=A533:Z533: A533='اطلاعات این فرم گزیده ای از اطلاعات گزارش تفسیری مدیریت
می باشد که هیئت مدیره شرکت م...
  row 534 [n=1 text=1 number=0 other=0]: A534='درآمدهای عملیاتی و بهای تمام شده'
  row 535 [n=1 text=1 number=0 other=0]: A535='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 536 [n=8 text=8 number=0 other=0] merges=A536:A537,B536:B537,C536:C537,D536:D537,E536:F536,G536:L536,M536:R536,S53
6:V536: A536='نوع کالا' | B536='واحد' | C536='ظرفیت عملی' | D536='مبانی و مرجع قیمت گذاری' | E536='دوره ۶ ماهه منتهی به
۱۴۰۴/۰۳/۳۱' | G536='سال مالی منتهی به ۱۴۰۴/۰۹/۳۰' | M536='دوره ۶ ماهه منتهی به ۱۴۰۵/۰۳/۳۱' | S536='برآورد دوره ۶ ماهه من
تهی به ۱۴۰۵/۰۹/۳۰'

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=534
  row 534 [n=1 text=1 number=0 other=0]: A534='درآمدهای عملیاتی و بهای تمام شده'
  row 535 [n=1 text=1 number=0 other=0]: A535='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 536 [n=8 text=8 number=0 other=0] merges=A536:A537,B536:B537,C536:C537,D536:D537,E536:F536,G536:L536,M536:R536,S53
6:V536: A536='نوع کالا' | B536='واحد' | C536='ظرفیت عملی' | D536='مبانی و مرجع قیمت گذاری' | E536='دوره ۶ ماهه منتهی به
۱۴۰۴/۰۳/۳۱' | G536='سال مالی منتهی به ۱۴۰۴/۰۹/۳۰' | M536='دوره ۶ ماهه منتهی به ۱۴۰۵/۰۳/۳۱' | S536='برآورد دوره ۶ ماهه من
تهی به ۱۴۰۵/۰۹/۳۰'
  row 537 [n=18 text=18 number=0 other=0] merges=A536:A537,B536:B537,C536:C537,D536:D537: E537='تعداد فروش' | F537='مبلغ
 فروش' | G537='تعداد تولید' | H537='تعداد فروش' | I537='نرخ فروش' | J537='مبلغ فروش' | K537='مبلغ بهای تمام شده' | L537=
'سود ناخالص' | M537='تعداد تولید' | N537='تعداد فروش' | O537='نرخ فروش' | P537='مبلغ فروش' | Q537='مبلغ بهای تمام شده' |
 R537='سود ناخالص' | S537='تعداد تولید' | T537='تعداد فروش' | U537='نرخ فروش' | V537='مبلغ فروش'

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=535
  row 535 [n=1 text=1 number=0 other=0]: A535='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 536 [n=8 text=8 number=0 other=0] merges=A536:A537,B536:B537,C536:C537,D536:D537,E536:F536,G536:L536,M536:R536,S53
6:V536: A536='نوع کالا' | B536='واحد' | C536='ظرفیت عملی' | D536='مبانی و مرجع قیمت گذاری' | E536='دوره ۶ ماهه منتهی به
۱۴۰۴/۰۳/۳۱' | G536='سال مالی منتهی به ۱۴۰۴/۰۹/۳۰' | M536='دوره ۶ ماهه منتهی به ۱۴۰۵/۰۳/۳۱' | S536='برآورد دوره ۶ ماهه من
تهی به ۱۴۰۵/۰۹/۳۰'
  row 537 [n=18 text=18 number=0 other=0] merges=A536:A537,B536:B537,C536:C537,D536:D537: E537='تعداد فروش' | F537='مبلغ
 فروش' | G537='تعداد تولید' | H537='تعداد فروش' | I537='نرخ فروش' | J537='مبلغ فروش' | K537='مبلغ بهای تمام شده' | L537=
'سود ناخالص' | M537='تعداد تولید' | N537='تعداد فروش' | O537='نرخ فروش' | P537='مبلغ فروش' | Q537='مبلغ بهای تمام شده' |
 R537='سود ناخالص' | S537='تعداد تولید' | T537='تعداد فروش' | U537='نرخ فروش' | V537='مبلغ فروش'
  row 538 [n=1 text=1 number=0 other=0]: A538='فروش داخلي: '

[DIRECT_NEXT_ROW_MIXED] anchor_row=538
  row 538 [n=1 text=1 number=0 other=0]: A538='فروش داخلي: '
  row 539 [n=20 text=3 number=17 other=0]: A539='استخراج کانسنگ طلا با عيار ۱/۱۸ گرم بر تن ' | B539='تن ' | C539=715000
| D539='سایر ' | E539=66545 | F539=1363653 | G539=515000 | H539=520154.18 | I539=28256951 | J539=14697971 | K539=-909557
1 | L539=5602400 | M539=0 | N539=0 | P539=0 | Q539=0 | R539=0 | S539=0 | T539=0 | V539=0
  row 540 [n=22 text=3 number=19 other=0]: A540='برداشت کانسنگ طلا با عيار ۰/۳۷۵۹ گرم بر تن از محل باطله سنوات قبل ' | B
540='تن ' | C540=0 | D540='سایر ' | E540=6513468 | F540=1296635 | G540=373492 | H540=373492.62 | I540=6840855 | J540=255
5009 | K540=-1582991 | L540=972018 | M540=146383 | N540=146383.28 | O540=17648498 | P540=2583445 | Q540=-1718365 | R540=
865080 | S540=403617 | T540=403617 | U540=15112954 | V540=6099845
  row 541 [n=20 text=3 number=17 other=0]: A541='استخراج سنگ تراورتن شکلاتي درجه ۳ ' | B541='تن ' | C541=9100 | D541='سا
یر ' | G541=3833 | H541=884.45 | I541=24999717 | J541=22111 | K541=-6633 | L541=15478 | M541=158 | N541=613 | O541=25001
631 | P541=15326 | Q541=-11363 | R541=3963 | S541=3675 | T541=271 | U541=25036900 | V541=6785

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=546
  row 546 [n=1 text=1 number=0 other=0]: A546='فروش صادراتی: '
  row 547: <EMPTY>
  row 548 [n=16 text=1 number=15 other=0]: A548='جمع فروش صادراتی ' | E548=0 | F548=0 | G548=0 | H548=0 | J548=0 | K548=
0 | L548=0 | M548=0 | N548=0 | P548=0 | Q548=0 | R548=0 | S548=0 | T548=0 | V548=0
  row 549 [n=1 text=1 number=0 other=0]: A549='درآمد ارائه خدمات: '

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=549
  row 549 [n=1 text=1 number=0 other=0]: A549='درآمد ارائه خدمات: '
  row 550: <EMPTY>
  row 551 [n=16 text=1 number=15 other=0]: A551='جمع درآمد ارائه خدمات ' | E551=0 | F551=0 | G551=0 | H551=0 | J551=0 |
K551=0 | L551=0 | M551=0 | N551=0 | P551=0 | Q551=0 | R551=0 | S551=0 | T551=0 | V551=0
  row 552 [n=8 text=1 number=7 other=0]: A552='ساير ' | G552=0 | K552=0 | L552=0 | M552=0 | Q552=0 | R552=0 | S552=0

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=554
  row 554 [n=1 text=1 number=0 other=0]: A554='روند فروش و بهای تمام شده در 5 سال اخیر'
  row 555 [n=1 text=1 number=0 other=0]: A555='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 556 [n=8 text=8 number=0 other=0]: A556='شرح' | B556='سال مالی ۱۴۰۰/۱۲/۲۹' | C556='سال مالی ۱۴۰۱/۰۹/۳۰' | D556='سا
ل مالی ۱۴۰۲/۰۹/۳۰' | E556='سال مالی ۱۴۰۳/۰۹/۳۰' | F556='سال مالی ۱۴۰۴/۰۹/۳۰' | G556='سال مالی ۱۴۰۵/۰۳/۳۱' | H556='برآورد
 دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰'
  row 557 [n=8 text=1 number=7 other=0]: A557='مبلغ فروش ' | B557=2072332 | C557=3057063 | D557=5441333 | E557=11618949
| F557=22766727 | G557=10608198 | H557=19103839

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=555
  row 555 [n=1 text=1 number=0 other=0]: A555='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 556 [n=8 text=8 number=0 other=0]: A556='شرح' | B556='سال مالی ۱۴۰۰/۱۲/۲۹' | C556='سال مالی ۱۴۰۱/۰۹/۳۰' | D556='سا
ل مالی ۱۴۰۲/۰۹/۳۰' | E556='سال مالی ۱۴۰۳/۰۹/۳۰' | F556='سال مالی ۱۴۰۴/۰۹/۳۰' | G556='سال مالی ۱۴۰۵/۰۳/۳۱' | H556='برآورد
 دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰'
  row 557 [n=8 text=1 number=7 other=0]: A557='مبلغ فروش ' | B557=2072332 | C557=3057063 | D557=5441333 | E557=11618949
| F557=22766727 | G557=10608198 | H557=19103839
  row 558 [n=8 text=1 number=7 other=0]: A558='مبلغ بهای تمام شده ' | B558=-1444346 | C558=-2032841 | D558=-3106672 | E5
58=-6482191 | F558=-13534520 | G558=-7545045 | H558=-8574690

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=559
  row 559 [n=1 text=1 number=0 other=0]: A559='اهداف و راهبردهای آتی مدیریت در خصوص تولید و فروش محصولات'
  row 560 [n=1 text=1 number=0 other=0] merges=A560:K560: A560='تمامی تولیدات شرکت بر اساس قرارداد بلند مدت به شرکت استح
صال مواد معدنی تخت سلیمان (ش...
  row 561 [n=1 text=1 number=0 other=0]: A561='برآورد شرکت از تغییرات نرخ فروش محصولات'
  row 562 [n=3 text=3 number=0 other=0] merges=C562:K562: A562='نرخ فروش محصولات ' | B562='برآورد دوره ۶ ماهه منتهی به ۱
۴۰۵/۰۹/۳۰ ' | C562='نرخ فروش کانسنگ بر اساس قرارداد فی ما بین با شرکت استحصال مواد معدنی تخت سلیمان (شرک...

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=560
  row 560 [n=1 text=1 number=0 other=0] merges=A560:K560: A560='تمامی تولیدات شرکت بر اساس قرارداد بلند مدت به شرکت استح
صال مواد معدنی تخت سلیمان (ش...
  row 561 [n=1 text=1 number=0 other=0]: A561='برآورد شرکت از تغییرات نرخ فروش محصولات'
  row 562 [n=3 text=3 number=0 other=0] merges=C562:K562: A562='نرخ فروش محصولات ' | B562='برآورد دوره ۶ ماهه منتهی به ۱
۴۰۵/۰۹/۳۰ ' | C562='نرخ فروش کانسنگ بر اساس قرارداد فی ما بین با شرکت استحصال مواد معدنی تخت سلیمان (شرک...
  row 563: <EMPTY>

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=561
  row 561 [n=1 text=1 number=0 other=0]: A561='برآورد شرکت از تغییرات نرخ فروش محصولات'
  row 562 [n=3 text=3 number=0 other=0] merges=C562:K562: A562='نرخ فروش محصولات ' | B562='برآورد دوره ۶ ماهه منتهی به ۱
۴۰۵/۰۹/۳۰ ' | C562='نرخ فروش کانسنگ بر اساس قرارداد فی ما بین با شرکت استحصال مواد معدنی تخت سلیمان (شرک...
  row 563: <EMPTY>
  row 564 [n=1 text=1 number=0 other=0]: A564='بهای تمام شده'

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=564
  row 564 [n=1 text=1 number=0 other=0]: A564='بهای تمام شده'
  row 565 [n=1 text=1 number=0 other=0]: A565='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 566 [n=4 text=4 number=0 other=0]: A566='شرح' | B566='سال مالی منتهی به ۱۴۰۴/۰۹/۳۰ (میلیون ریال)' | C566='دوره ۶ م
اهه منتهی به ۱۴۰۵/۰۳/۳۱ (میلیون ریال)' | D566='برآورد دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰'
  row 567 [n=4 text=1 number=3 other=0]: A567='مواد مستقیم مصرفی ' | B567=0 | C567=0 | D567=0

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=565
  row 565 [n=1 text=1 number=0 other=0]: A565='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 566 [n=4 text=4 number=0 other=0]: A566='شرح' | B566='سال مالی منتهی به ۱۴۰۴/۰۹/۳۰ (میلیون ریال)' | C566='دوره ۶ م
اهه منتهی به ۱۴۰۵/۰۳/۳۱ (میلیون ریال)' | D566='برآورد دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰'
  row 567 [n=4 text=1 number=3 other=0]: A567='مواد مستقیم مصرفی ' | B567=0 | C567=0 | D567=0
  row 568 [n=4 text=1 number=3 other=0]: A568='دستمزدمستقيم توليد ' | B568=2216300 | C568=1079645 | D568=1966034

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=581
  row 581 [n=1 text=1 number=0 other=0]: A581='برآورد شرکت از تغییرات عوامل بهای تمام شده'
  row 582 [n=2 text=2 number=0 other=0] merges=B582:J582: A582='برآورد دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰ ' | B582='انتظار
می رود بهای تمام شده تولید معادل نرخ تورم و افزایش حجم تولیدات افزایش یابد. '
  row 583: <EMPTY>
  row 584 [n=1 text=1 number=0 other=0] merges=A584:T584: A584='«جملات آینده\u200cنگر نشان\u200cدهنده انتظارات، باورها ی
ا پیش\u200cبینی\u200cهای جار...

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=584
  row 584 [n=1 text=1 number=0 other=0] merges=A584:T584: A584='«جملات آینده\u200cنگر نشان\u200cدهنده انتظارات، باورها ی
ا پیش\u200cبینی\u200cهای جار...
  row 585: <EMPTY>
  row 586: <EMPTY>
  row 587: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=588
  row 588 [n=1 text=1 number=0 other=0]: A588='خلاصه اطلاعات گزارش تفسیری - صفحه 2'
  row 589: <EMPTY>
  row 590: <EMPTY>
  row 591: <EMPTY>

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=593
  row 593 [n=1 text=1 number=0 other=0] merges=A593:T593: A593='اطلاعات این فرم گزیده ای از اطلاعات گزارش تفسیری مدیریت
می باشد که هیئت مدیره شرکت م...
  row 594 [n=1 text=1 number=0 other=0]: A594='گردش مقداری - ریالی موجودی کالا'
  row 595 [n=3 text=3 number=0 other=0] merges=A595:A597,B595:B597,C595:Q595: A595='شرح محصول' | B595='واحد' | C595='دور
ه ۶ ماهه منتهی به ۱۴۰۵/۰۳/۳۱'
  row 596 [n=5 text=5 number=0 other=0] merges=A595:A597,B595:B597,C596:E596,F596:H596,I596:K596,L596:N596,O596:Q596: C5
96='موجودي اول دوره' | F596='تولید' | I596='تعدیلات' | L596='فروش' | O596='موجودی پایان دوره'

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=594
  row 594 [n=1 text=1 number=0 other=0]: A594='گردش مقداری - ریالی موجودی کالا'
  row 595 [n=3 text=3 number=0 other=0] merges=A595:A597,B595:B597,C595:Q595: A595='شرح محصول' | B595='واحد' | C595='دور
ه ۶ ماهه منتهی به ۱۴۰۵/۰۳/۳۱'
  row 596 [n=5 text=5 number=0 other=0] merges=A595:A597,B595:B597,C596:E596,F596:H596,I596:K596,L596:N596,O596:Q596: C5
96='موجودي اول دوره' | F596='تولید' | I596='تعدیلات' | L596='فروش' | O596='موجودی پایان دوره'
  row 597 [n=15 text=15 number=0 other=0] merges=A595:A597,B595:B597: C597='مقدار' | D597='نرخ - ریال' | E597='بهای تمام
 شده - میلیون ریال' | F597='مقدار' | G597='نرخ - ریال' | H597='بهای تمام شده - میلیون ریال' | I597='مقدار' | J597='نرخ -
 ریال' | K597='بهای تمام شده - میلیون ریال' | L597='مقدار' | M597='نرخ - ریال' | N597='بهای تمام شده - میلیون ریال' | O5
97='مقدار' | P597='نرخ - ریال' | Q597='بهای تمام شده - میلیون ریال'

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=604
  row 604 [n=1 text=1 number=0 other=0]: A604='گردش مقداری - ریالی موجودی کالا (برآوردی)'
  row 605 [n=3 text=3 number=0 other=0] merges=A605:A607,B605:B607,C605:Q605: A605='شرح محصول' | B605='واحد' | C605='برآ
ورد دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰'
  row 606 [n=5 text=5 number=0 other=0] merges=A605:A607,B605:B607,C606:E606,F606:H606,I606:K606,L606:N606,O606:Q606: C6
06='موجودي اول دوره' | F606='تولید' | I606='تعدیلات' | L606='فروش' | O606='موجودی پایان دوره'
  row 607 [n=15 text=15 number=0 other=0] merges=A605:A607,B605:B607: C607='مقدار' | D607='نرخ - ریال' | E607='بهای تمام
 شده - میلیون ریال' | F607='مقدار' | G607='نرخ - ریال' | H607='بهای تمام شده - میلیون ریال' | I607='مقدار' | J607='نرخ -
 ریال' | K607='بهای تمام شده - میلیون ریال' | L607='مقدار' | M607='نرخ - ریال' | N607='بهای تمام شده - میلیون ریال' | O6
07='مقدار' | P607='نرخ - ریال' | Q607='بهای تمام شده - میلیون ریال'

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=614
  row 614 [n=1 text=1 number=0 other=0]: A614='گردش مقداری - ریالی موجودی کالا (برآوردی پایان سال آینده)'
  row 615: <EMPTY>
  row 616: <EMPTY>
  row 617: <EMPTY>

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=619
  row 619 [n=1 text=1 number=0 other=0]: A619='خرید و مصرف مواد اولیه'
  row 620 [n=3 text=3 number=0 other=0] merges=A620:A623,B620:B623,C620:N620: A620='شرح' | B620='واحد' | C620='دوره ۶ ما
هه منتهی به ۱۴۰۵/۰۳/۳۱'
  row 621 [n=4 text=4 number=0 other=0] merges=A620:A623,B620:B623,C621:E621,F621:H621,I621:K621,L621:N621: C621='موجودي
 اول دوره' | F621='خريد طي دوره' | I621='مصرف' | L621='موجودی پایان دوره'
  row 622 [n=12 text=12 number=0 other=0] merges=A620:A623,B620:B623: C622='مقدار' | D622='نرخ' | E622='مبلغ' | F622='مق
دار' | G622='نرخ' | H622='مبلغ' | I622='مقدار' | J622='نرخ' | K622='مبلغ' | L622='مقدار' | M622='نرخ' | N622='مبلغ'

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=624
  row 624 [n=1 text=1 number=0 other=0]: A624='مواد اولیه داخلی: '
  row 625: <EMPTY>
  row 626 [n=5 text=1 number=4 other=0]: A626='جمع مواد اولیه داخلی ' | E626=0 | H626=0 | K626=0 | N626=0
  row 627 [n=1 text=1 number=0 other=0]: A627='مواد اولیه وارداتی: '

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=627
  row 627 [n=1 text=1 number=0 other=0]: A627='مواد اولیه وارداتی: '
  row 628: <EMPTY>
  row 629 [n=5 text=1 number=4 other=0]: A629='جمع مواد اولیه وارداتی ' | E629=0 | H629=0 | K629=0 | N629=0
  row 630 [n=5 text=1 number=4 other=0]: A630='جمع كـل ' | E630=0 | H630=0 | K630=0 | N630=0

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=631
  row 631 [n=1 text=1 number=0 other=0]: A631='خرید و مصرف مواد اولیه (برآوردی)'
  row 632 [n=3 text=3 number=0 other=0] merges=A632:A635,B632:B635,C632:N632: A632='شرح' | B632='واحد' | C632='برآورد دو
ره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰'
  row 633 [n=4 text=4 number=0 other=0] merges=A632:A635,B632:B635,C633:E633,F633:H633,I633:K633,L633:N633: C633='موجودي
 اول دوره' | F633='خريد طي دوره' | I633='مصرف' | L633='موجودی پایان دوره'
  row 634 [n=12 text=12 number=0 other=0] merges=A632:A635,B632:B635: C634='مقدار' | D634='نرخ' | E634='مبلغ' | F634='مق
دار' | G634='نرخ' | H634='مبلغ' | I634='مقدار' | J634='نرخ' | K634='مبلغ' | L634='مقدار' | M634='نرخ' | N634='مبلغ'

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=636
  row 636 [n=1 text=1 number=0 other=0]: A636='مواد اولیه داخلی: '
  row 637: <EMPTY>
  row 638 [n=5 text=1 number=4 other=0]: A638='جمع مواد اولیه داخلی ' | E638=0 | H638=0 | K638=0 | N638=0
  row 639 [n=1 text=1 number=0 other=0]: A639='مواد اولیه وارداتی: '

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=639
  row 639 [n=1 text=1 number=0 other=0]: A639='مواد اولیه وارداتی: '
  row 640: <EMPTY>
  row 641 [n=5 text=1 number=4 other=0]: A641='جمع مواد اولیه وارداتی ' | E641=0 | H641=0 | K641=0 | N641=0
  row 642 [n=5 text=1 number=4 other=0]: A642='جمع كـل ' | E642=0 | H642=0 | K642=0 | N642=0

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=643
  row 643 [n=1 text=1 number=0 other=0]: A643='خرید و مصرف مواد اولیه (برآوردی پایان سال آینده)'
  row 644: <EMPTY>
  row 645: <EMPTY>
  row 646: <EMPTY>

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=655
  row 655 [n=1 text=1 number=0 other=0]: A655='برآورد شرکت از تغییرات نرخ خرید مواد اولیه'
  row 656 [n=3 text=3 number=0 other=0] merges=C656:I656: A656='نرخ خرید مواد اولیه ' | B656='برآورد دوره ۶ ماهه منتهی ب
ه ۱۴۰۵/۰۹/۳۰ ' | C656='نظر به اینکه ماهیت فعالیت شرکت استخراج کانسنگ (خاک معدنی) می باشد لذا هزینه ای بابت ...
  row 657: <EMPTY>
  row 658 [n=1 text=1 number=0 other=0] merges=A658:T658: A658='«جملات آینده\u200cنگر نشان\u200cدهنده انتظارات، باورها ی
ا پیش\u200cبینی\u200cهای جار...

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=658
  row 658 [n=1 text=1 number=0 other=0] merges=A658:T658: A658='«جملات آینده\u200cنگر نشان\u200cدهنده انتظارات، باورها ی
ا پیش\u200cبینی\u200cهای جار...
  row 659: <EMPTY>
  row 660: <EMPTY>
  row 661: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=662
  row 662 [n=1 text=1 number=0 other=0]: A662='خلاصه اطلاعات گزارش تفسیری - صفحه 3'
  row 663: <EMPTY>
  row 664: <EMPTY>
  row 665: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=667
  row 667 [n=1 text=1 number=0 other=0] merges=A667:T667: A667='اطلاعات این فرم گزیده ای از اطلاعات گزارش تفسیری مدیریت
می باشد که هیئت مدیره شرکت م...
  row 668 [n=1 text=1 number=0 other=0]: A668='هزینه های سربار و هزینه های عمومی و اداری شرکت'
  row 669 [n=1 text=1 number=0 other=0]: A669='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 670 [n=3 text=3 number=0 other=0] merges=A670:A671,B670:D670,E670:G670: A670='شرح' | B670='هزینه سربار' | E670='هز
ینه های اداری، عمومی و فروش'

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=668
  row 668 [n=1 text=1 number=0 other=0]: A668='هزینه های سربار و هزینه های عمومی و اداری شرکت'
  row 669 [n=1 text=1 number=0 other=0]: A669='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 670 [n=3 text=3 number=0 other=0] merges=A670:A671,B670:D670,E670:G670: A670='شرح' | B670='هزینه سربار' | E670='هز
ینه های اداری، عمومی و فروش'
  row 671 [n=6 text=6 number=0 other=0] merges=A670:A671: B671='سال مالی منتهی به ۱۴۰۴/۰۹/۳۰' | C671='دوره ۶ ماهه منتهی
به ۱۴۰۵/۰۳/۳۱' | D671='برآورد دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰' | E671='سال مالی منتهی به ۱۴۰۴/۰۹/۳۰' | F671='دوره ۶ ماهه
 منتهی به ۱۴۰۵/۰۳/۳۱' | G671='برآورد دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰'

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=669
  row 669 [n=1 text=1 number=0 other=0]: A669='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 670 [n=3 text=3 number=0 other=0] merges=A670:A671,B670:D670,E670:G670: A670='شرح' | B670='هزینه سربار' | E670='هز
ینه های اداری، عمومی و فروش'
  row 671 [n=6 text=6 number=0 other=0] merges=A670:A671: B671='سال مالی منتهی به ۱۴۰۴/۰۹/۳۰' | C671='دوره ۶ ماهه منتهی
به ۱۴۰۵/۰۳/۳۱' | D671='برآورد دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰' | E671='سال مالی منتهی به ۱۴۰۴/۰۹/۳۰' | F671='دوره ۶ ماهه
 منتهی به ۱۴۰۵/۰۳/۳۱' | G671='برآورد دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰'
  row 672 [n=7 text=1 number=6 other=0]: A672='هزینه حقوق و دستمزد ' | B672=0 | C672=0 | D672=0 | E672=604023 | F672=417
256 | G672=368236

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=684
  row 684 [n=1 text=1 number=0 other=0]: A684='برآورد شرکت از تغییرات هزینه های عمومی ، اداری ، تشکیلاتی و خالص سایر درآ
مدها (هزینه...
  row 685 [n=2 text=2 number=0 other=0] merges=B685:H685: A685='برآورد دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰ ' | B685='انتظار
می رود هزینه های عمومی ، اداری و تشکیلاتی شرکت متناسب با نرخ تورم و افزایش حج...
  row 686: <EMPTY>
  row 687 [n=1 text=1 number=0 other=0]: A687='وضعیت کارکنان'

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=687
  row 687 [n=1 text=1 number=0 other=0]: A687='وضعیت کارکنان'
  row 688 [n=4 text=4 number=0 other=0]: A688='شرح' | B688='سال مالی منتهی به ۱۴۰۴/۰۹/۳۰' | C688='دوره ۶ ماهه منتهی به ۱
۴۰۵/۰۳/۳۱' | D688='برآورد دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰'
  row 689 [n=4 text=1 number=3 other=0]: A689='تعداد پرسنل تولیدی شرکت ' | B689=419 | C689=380 | D689=419
  row 690 [n=4 text=1 number=3 other=0]: A690='تعداد پرسنل غیر تولیدی شرکت ' | B690=125 | C690=131 | D690=125

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=691
  row 691 [n=1 text=1 number=0 other=0]: A691='وضعیت ارزی'
  row 692 [n=1 text=1 number=0 other=0]: A692='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 693 [n=5 text=5 number=0 other=0] merges=A693:A694,B693:B694,C693:E693,F693:H693,I693:K693: A693='شرح' | B693='نوع
 ارز' | C693='سال مالي منتهي به ۱۴۰۴/۰۹/۳۰' | F693='دوره ۶ ماهه منتهي به ۱۴۰۵/۰۳/۳۱' | I693='برآورد دوره ۶ ماهه منتهي به
 ۱۴۰۵/۰۹/۳۰'
  row 694 [n=9 text=9 number=0 other=0] merges=A693:A694,B693:B694: C694='نرخ ميانگين تسعير ارز' | D694='مبلغ ارزي' | E6
94='مبلغ ريالي-ميليون ريال' | F694='نرخ ميانگين تسعير ارز' | G694='مبلغ ارزي' | H694='مبلغ ريالي-ميليون ريال' | I694='نر
خ ميانگين تسعير ارز' | J694='مبلغ ارزي' | K694='مبلغ ريالي-ميليون ريال'

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=692
  row 692 [n=1 text=1 number=0 other=0]: A692='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 693 [n=5 text=5 number=0 other=0] merges=A693:A694,B693:B694,C693:E693,F693:H693,I693:K693: A693='شرح' | B693='نوع
 ارز' | C693='سال مالي منتهي به ۱۴۰۴/۰۹/۳۰' | F693='دوره ۶ ماهه منتهي به ۱۴۰۵/۰۳/۳۱' | I693='برآورد دوره ۶ ماهه منتهي به
 ۱۴۰۵/۰۹/۳۰'
  row 694 [n=9 text=9 number=0 other=0] merges=A693:A694,B693:B694: C694='نرخ ميانگين تسعير ارز' | D694='مبلغ ارزي' | E6
94='مبلغ ريالي-ميليون ريال' | F694='نرخ ميانگين تسعير ارز' | G694='مبلغ ارزي' | H694='مبلغ ريالي-ميليون ريال' | I694='نر
خ ميانگين تسعير ارز' | J694='مبلغ ارزي' | K694='مبلغ ريالي-ميليون ريال'
  row 695 [n=1 text=1 number=0 other=0] merges=A695:J695: A695='«جملات آینده\u200cنگر نشان\u200cدهنده انتظارات، باورها ی
ا پیش\u200cبینی\u200cهای جار...

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=695
  row 695 [n=1 text=1 number=0 other=0] merges=A695:J695: A695='«جملات آینده\u200cنگر نشان\u200cدهنده انتظارات، باورها ی
ا پیش\u200cبینی\u200cهای جار...
  row 696 [n=1 text=1 number=0 other=0] merges=A696:D696: A696='توضیحات درخصوص وضعیت ارزی '
  row 697: <EMPTY>
  row 698: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=696
  row 696 [n=1 text=1 number=0 other=0] merges=A696:D696: A696='توضیحات درخصوص وضعیت ارزی '
  row 697: <EMPTY>
  row 698: <EMPTY>
  row 699: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=701
  row 701 [n=1 text=1 number=0 other=0]: A701='خلاصه اطلاعات گزارش تفسیری - صفحه 4'
  row 702: <EMPTY>
  row 703: <EMPTY>
  row 704: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=706
  row 706 [n=1 text=1 number=0 other=0] merges=A706:T706: A706='اطلاعات این فرم گزیده ای از اطلاعات گزارش تفسیری مدیریت
می باشد که هیئت مدیره شرکت م...
  row 707 [n=1 text=1 number=0 other=0]: A707='تشریح برنامه های شرکت جهت تکمیل طرح های توسعه'
  row 708 [n=1 text=1 number=0 other=0]: A708='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 709 [n=15 text=15 number=0 other=0] merges=A709:A710,B709:B710,C709:C710,D709:D710,E709:E710,F709:F710,G709:H709,K
709:K710,L709:L710,M709:M710,N709:N710,O709:O710,P709:P710: A709='نام طرح' | B709='هزینه های برآوردی ریالی طرح - میلیون
ریال' | C709='هزینه های برآوردی ارزی طرح' | D709='نوع ارز' | E709='هزینه های انجام شده تا تاریخ ۱۴۰۵/۰۳/۳۱ - میلیون ریال
' | F709='هزینه های برآوردی تکمیل طرح- میلیون ریال' | G709='منابع تامین مالی' | I709='نرخNPV' | J709='نرخ IRR' | K709='د
رصد پیشرفت فیزیکی طرح در تاریخ ۱۴۰۴/۰۹/۳۰' | L709='درصد پیشرفت فیزیکی طرح در تاریخ ۱۴۰۵/۰۳/۳۱' | M709='درصد پیشرفت فیزیک
ی برآوردی طرح در تاریخ ۱۴۰۵/۰۹/۳۰' | N709='تاریخ برآوردی بهره برداری از طرح' | O709='تشریح تاثیر طرح در فعالیتهای آتی شر
کت' | P709='توضیحات'

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=707
  row 707 [n=1 text=1 number=0 other=0]: A707='تشریح برنامه های شرکت جهت تکمیل طرح های توسعه'
  row 708 [n=1 text=1 number=0 other=0]: A708='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 709 [n=15 text=15 number=0 other=0] merges=A709:A710,B709:B710,C709:C710,D709:D710,E709:E710,F709:F710,G709:H709,K
709:K710,L709:L710,M709:M710,N709:N710,O709:O710,P709:P710: A709='نام طرح' | B709='هزینه های برآوردی ریالی طرح - میلیون
ریال' | C709='هزینه های برآوردی ارزی طرح' | D709='نوع ارز' | E709='هزینه های انجام شده تا تاریخ ۱۴۰۵/۰۳/۳۱ - میلیون ریال
' | F709='هزینه های برآوردی تکمیل طرح- میلیون ریال' | G709='منابع تامین مالی' | I709='نرخNPV' | J709='نرخ IRR' | K709='د
رصد پیشرفت فیزیکی طرح در تاریخ ۱۴۰۴/۰۹/۳۰' | L709='درصد پیشرفت فیزیکی طرح در تاریخ ۱۴۰۵/۰۳/۳۱' | M709='درصد پیشرفت فیزیک
ی برآوردی طرح در تاریخ ۱۴۰۵/۰۹/۳۰' | N709='تاریخ برآوردی بهره برداری از طرح' | O709='تشریح تاثیر طرح در فعالیتهای آتی شر
کت' | P709='توضیحات'
  row 710 [n=2 text=2 number=0 other=0] merges=A709:A710,B709:B710,C709:C710,D709:D710,E709:E710,F709:F710,K709:K710,L70
9:L710,M709:M710,N709:N710,O709:O710,P709:P710: G710='ارزی' | H710='ریالی'

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=708
  row 708 [n=1 text=1 number=0 other=0]: A708='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 709 [n=15 text=15 number=0 other=0] merges=A709:A710,B709:B710,C709:C710,D709:D710,E709:E710,F709:F710,G709:H709,K
709:K710,L709:L710,M709:M710,N709:N710,O709:O710,P709:P710: A709='نام طرح' | B709='هزینه های برآوردی ریالی طرح - میلیون
ریال' | C709='هزینه های برآوردی ارزی طرح' | D709='نوع ارز' | E709='هزینه های انجام شده تا تاریخ ۱۴۰۵/۰۳/۳۱ - میلیون ریال
' | F709='هزینه های برآوردی تکمیل طرح- میلیون ریال' | G709='منابع تامین مالی' | I709='نرخNPV' | J709='نرخ IRR' | K709='د
رصد پیشرفت فیزیکی طرح در تاریخ ۱۴۰۴/۰۹/۳۰' | L709='درصد پیشرفت فیزیکی طرح در تاریخ ۱۴۰۵/۰۳/۳۱' | M709='درصد پیشرفت فیزیک
ی برآوردی طرح در تاریخ ۱۴۰۵/۰۹/۳۰' | N709='تاریخ برآوردی بهره برداری از طرح' | O709='تشریح تاثیر طرح در فعالیتهای آتی شر
کت' | P709='توضیحات'
  row 710 [n=2 text=2 number=0 other=0] merges=A709:A710,B709:B710,C709:C710,D709:D710,E709:E710,F709:F710,K709:K710,L70
9:L710,M709:M710,N709:N710,O709:O710,P709:P710: G710='ارزی' | H710='ریالی'
  row 711 [n=15 text=4 number=11 other=0]: A711='پروژه ساخت تصفيه خانه فاضلاب شماره يک ' | B711=30000 | C711=0 | E711=25
990 | F711=4010 | G711=0 | H711=0 | I711=0 | J711=0 | K711=55 | L711=87 | M711=100 | N711='۱۴۰۵/۰۴/۳۱ ' | O711='بهینه سا
زی و جلوگیری از هدر رفت آب مصرفی ' | P711='بهینه سازی و جلوگیری از هدر رفت آب مصرفی '

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=715
  row 715 [n=1 text=1 number=0 other=0]: A715='توضیحات درخصوص تشریح برنامه های شرکت جهت تکمیل طرح های توسعه'
  row 716: <EMPTY>
  row 717 [n=1 text=1 number=0 other=0]: A717='وضعیت شرکت\u200cهای سرمایه\u200cپذیر'
  row 718 [n=1 text=1 number=0 other=0]: A718='کلیه مبالغ درج شده به میلیون ریال می باشد'

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=717
  row 717 [n=1 text=1 number=0 other=0]: A717='وضعیت شرکت\u200cهای سرمایه\u200cپذیر'
  row 718 [n=1 text=1 number=0 other=0]: A718='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 719 [n=4 text=4 number=0 other=0] merges=A719:A720,B719:E719,F719:J719,K719:O719: A719='نام شرکت' | B719='سال مالی
 منتهی به ۱۴۰۴/۰۹/۳۰' | F719='دوره ۶ ماهه منتهی به ۱۴۰۵/۰۳/۳۱' | K719='برآورد دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰'
  row 720 [n=14 text=14 number=0 other=0] merges=A719:A720: B720='درصد مالکیت' | C720='بهای تمام شده' | D720='سال مالی ش
رکت سرمایه پذیر' | E720='درآمد سرمایه گذاری - میلیون ریال' | F720='درصد مالکیت' | G720='بهای تمام شده' | H720='درآمد هر
سهم' | I720='درآمد نقدی هر سهم' | J720='درآمد سرمایه گذاری - میلیون ریال' | K720='درصد مالکیت' | L720='بهای تمام شده' |
M720='درآمد هر سهم' | N720='درآمد نقدی هر سهم' | O720='درآمد سرمایه گذاری - میلیون ریال'

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=718
  row 718 [n=1 text=1 number=0 other=0]: A718='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 719 [n=4 text=4 number=0 other=0] merges=A719:A720,B719:E719,F719:J719,K719:O719: A719='نام شرکت' | B719='سال مالی
 منتهی به ۱۴۰۴/۰۹/۳۰' | F719='دوره ۶ ماهه منتهی به ۱۴۰۵/۰۳/۳۱' | K719='برآورد دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰'
  row 720 [n=14 text=14 number=0 other=0] merges=A719:A720: B720='درصد مالکیت' | C720='بهای تمام شده' | D720='سال مالی ش
رکت سرمایه پذیر' | E720='درآمد سرمایه گذاری - میلیون ریال' | F720='درصد مالکیت' | G720='بهای تمام شده' | H720='درآمد هر
سهم' | I720='درآمد نقدی هر سهم' | J720='درآمد سرمایه گذاری - میلیون ریال' | K720='درصد مالکیت' | L720='بهای تمام شده' |
M720='درآمد هر سهم' | N720='درآمد نقدی هر سهم' | O720='درآمد سرمایه گذاری - میلیون ریال'
  row 721 [n=15 text=2 number=13 other=0]: A721='استحصال مواد معدني تخت سليمان ' | B721=98 | C721=2594691 | D721='۱۴۰۴/۰
۹/۳۰ ' | E721=41602650 | F721=98 | G721=2594691 | H721=0 | I721=0 | J721=0 | K721=98 | L721=2594691 | M721=0 | N721=0 |
O721=133722320

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=724
  row 724 [n=1 text=1 number=0 other=0]: A724='توضیحات در خصوص وضعیت شرکت\u200cهای سرمایه\u200cپذیر'
  row 725 [n=1 text=1 number=0 other=0] merges=A725:T725: A725='شرکت در سال ۱۴۰۴ جهت سرمایه گذاری در یک صرافی (در شرف تا
سیس) مبلغ ۹۹۹،۹۸۰ میلیون ریا...
  row 726 [n=1 text=1 number=0 other=0] merges=A726:T726: A726='«جملات آینده\u200cنگر نشان\u200cدهنده انتظارات، باورها ی
ا پیش\u200cبینی\u200cهای جار...
  row 727: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=725
  row 725 [n=1 text=1 number=0 other=0] merges=A725:T725: A725='شرکت در سال ۱۴۰۴ جهت سرمایه گذاری در یک صرافی (در شرف تا
سیس) مبلغ ۹۹۹،۹۸۰ میلیون ریا...
  row 726 [n=1 text=1 number=0 other=0] merges=A726:T726: A726='«جملات آینده\u200cنگر نشان\u200cدهنده انتظارات، باورها ی
ا پیش\u200cبینی\u200cهای جار...
  row 727: <EMPTY>
  row 728: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=726
  row 726 [n=1 text=1 number=0 other=0] merges=A726:T726: A726='«جملات آینده\u200cنگر نشان\u200cدهنده انتظارات، باورها ی
ا پیش\u200cبینی\u200cهای جار...
  row 727: <EMPTY>
  row 728: <EMPTY>
  row 729: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=730
  row 730 [n=1 text=1 number=0 other=0]: A730='خلاصه اطلاعات گزارش تفسیری - صفحه 5'
  row 731: <EMPTY>
  row 732: <EMPTY>
  row 733: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=735
  row 735 [n=1 text=1 number=0 other=0] merges=A735:T735: A735='اطلاعات این فرم گزیده ای از اطلاعات گزارش تفسیری مدیریت
می باشد که هیئت مدیره شرکت م...
  row 736 [n=1 text=1 number=0 other=0]: A736='سایر درآمدهای عملیاتی'
  row 737 [n=1 text=1 number=0 other=0]: A737='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 738 [n=4 text=4 number=0 other=0]: A738='شرح' | B738='سال مالی منتهی به ۱۴۰۴/۰۹/۳۰' | C738='دوره ۶ ماهه منتهی به ۱
۴۰۵/۰۳/۳۱' | D738='برآورد دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰'

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=736
  row 736 [n=1 text=1 number=0 other=0]: A736='سایر درآمدهای عملیاتی'
  row 737 [n=1 text=1 number=0 other=0]: A737='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 738 [n=4 text=4 number=0 other=0]: A738='شرح' | B738='سال مالی منتهی به ۱۴۰۴/۰۹/۳۰' | C738='دوره ۶ ماهه منتهی به ۱
۴۰۵/۰۳/۳۱' | D738='برآورد دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰'
  row 739 [n=4 text=1 number=3 other=0]: A739='اجاره ماشين آلات ' | B739=303195 | C739=286052 | D739=213948

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=737
  row 737 [n=1 text=1 number=0 other=0]: A737='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 738 [n=4 text=4 number=0 other=0]: A738='شرح' | B738='سال مالی منتهی به ۱۴۰۴/۰۹/۳۰' | C738='دوره ۶ ماهه منتهی به ۱
۴۰۵/۰۳/۳۱' | D738='برآورد دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰'
  row 739 [n=4 text=1 number=3 other=0]: A739='اجاره ماشين آلات ' | B739=303195 | C739=286052 | D739=213948
  row 740 [n=4 text=1 number=3 other=0]: A740='سود سهام ' | B740=41602650 | C740=0 | D740=133722320

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=743
  row 743 [n=1 text=1 number=0 other=0]: A743='سایر هزینه\u200cهای عملیاتی'
  row 744 [n=1 text=1 number=0 other=0]: A744='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 745 [n=4 text=4 number=0 other=0]: A745='شرح' | B745='سال مالی منتهی به ۱۴۰۴/۰۹/۳۰' | C745='دوره ۶ ماهه منتهی به ۱
۴۰۵/۰۳/۳۱' | D745='برآورد دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰'
  row 746 [n=4 text=1 number=3 other=0]: A746='جمع ' | B746=0 | C746=0 | D746=0

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=744
  row 744 [n=1 text=1 number=0 other=0]: A744='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 745 [n=4 text=4 number=0 other=0]: A745='شرح' | B745='سال مالی منتهی به ۱۴۰۴/۰۹/۳۰' | C745='دوره ۶ ماهه منتهی به ۱
۴۰۵/۰۳/۳۱' | D745='برآورد دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰'
  row 746 [n=4 text=1 number=3 other=0]: A746='جمع ' | B746=0 | C746=0 | D746=0
  row 747 [n=1 text=1 number=0 other=0]: A747='منابع تامین مالی'

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=747
  row 747 [n=1 text=1 number=0 other=0]: A747='منابع تامین مالی'
  row 748 [n=1 text=1 number=0 other=0]: A748='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 749 [n=1 text=1 number=0 other=0] merges=A749:K749: A749='منابع تامین مالی شرکت در دوره ۶ ماهه منتهی به ۱۴۰۵/۰۳/۳۱
'
  row 750 [n=7 text=7 number=0 other=0] merges=A750:A752,B750:B752,C750:C752,D750:G750,H750:I751,J750:J752,K750:K752: A7
50='محل تامین' | B750='نرخ سود' | C750='مانده اول دوره تسهیلات ارزی و ریالی (میلیون ریال)' | D750='مانده پایان دوره (اصل
 و فرع)' | H750='مانده پایان دوره به تفکیک سررسید' | J750='مبلغ هزینه مالی طی دوره' | K750='سایر توضیحات'

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=748
  row 748 [n=1 text=1 number=0 other=0]: A748='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 749 [n=1 text=1 number=0 other=0] merges=A749:K749: A749='منابع تامین مالی شرکت در دوره ۶ ماهه منتهی به ۱۴۰۵/۰۳/۳۱
'
  row 750 [n=7 text=7 number=0 other=0] merges=A750:A752,B750:B752,C750:C752,D750:G750,H750:I751,J750:J752,K750:K752: A7
50='محل تامین' | B750='نرخ سود' | C750='مانده اول دوره تسهیلات ارزی و ریالی (میلیون ریال)' | D750='مانده پایان دوره (اصل
 و فرع)' | H750='مانده پایان دوره به تفکیک سررسید' | J750='مبلغ هزینه مالی طی دوره' | K750='سایر توضیحات'
  row 751 [n=2 text=2 number=0 other=0] merges=A750:A752,B750:B752,C750:C752,H750:I751,J750:J752,K750:K752,D751:D752,E75
1:G751: D751='ریالی' | E751='ارزی'

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=749
  row 749 [n=1 text=1 number=0 other=0] merges=A749:K749: A749='منابع تامین مالی شرکت در دوره ۶ ماهه منتهی به ۱۴۰۵/۰۳/۳۱
'
  row 750 [n=7 text=7 number=0 other=0] merges=A750:A752,B750:B752,C750:C752,D750:G750,H750:I751,J750:J752,K750:K752: A7
50='محل تامین' | B750='نرخ سود' | C750='مانده اول دوره تسهیلات ارزی و ریالی (میلیون ریال)' | D750='مانده پایان دوره (اصل
 و فرع)' | H750='مانده پایان دوره به تفکیک سررسید' | J750='مبلغ هزینه مالی طی دوره' | K750='سایر توضیحات'
  row 751 [n=2 text=2 number=0 other=0] merges=A750:A752,B750:B752,C750:C752,H750:I751,J750:J752,K750:K752,D751:D752,E75
1:G751: D751='ریالی' | E751='ارزی'
  row 752 [n=5 text=5 number=0 other=0] merges=A750:A752,B750:B752,C750:C752,J750:J752,K750:K752,D751:D752: E752='نوع ار
ز' | F752='مبلغ ارزی' | G752='معادل ریالی تسهیلات ارزی (میلیون ریال)' | H752='کوتاه مدت' | I752='بلند مدت'

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=759
  row 759 [n=1 text=1 number=0 other=0]: A759='منابع تامین مالی (برآوردی)'
  row 760 [n=1 text=1 number=0 other=0]: A760='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 761 [n=1 text=1 number=0 other=0] merges=A761:K761: A761='برآورد منابع تامین مالی شرکت در دوره ۶ ماهه منتهی به ۱۴۰
۵/۰۹/۳۰'
  row 762 [n=7 text=7 number=0 other=0] merges=A762:A764,B762:B764,C762:C764,D762:G762,H762:I763,J762:J764,K762:K764: A7
62='محل تامین' | B762='نرخ سود' | C762='مانده اول دوره تسهیلات ارزی و ریالی (میلیون ریال)' | D762='مانده پایان دوره (اصل
 و فرع)' | H762='مانده پایان دوره به تفکیک سررسید' | J762='مبلغ هزینه مالی طی دوره' | K762='سایر توضیحات'

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=760
  row 760 [n=1 text=1 number=0 other=0]: A760='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 761 [n=1 text=1 number=0 other=0] merges=A761:K761: A761='برآورد منابع تامین مالی شرکت در دوره ۶ ماهه منتهی به ۱۴۰
۵/۰۹/۳۰'
  row 762 [n=7 text=7 number=0 other=0] merges=A762:A764,B762:B764,C762:C764,D762:G762,H762:I763,J762:J764,K762:K764: A7
62='محل تامین' | B762='نرخ سود' | C762='مانده اول دوره تسهیلات ارزی و ریالی (میلیون ریال)' | D762='مانده پایان دوره (اصل
 و فرع)' | H762='مانده پایان دوره به تفکیک سررسید' | J762='مبلغ هزینه مالی طی دوره' | K762='سایر توضیحات'
  row 763 [n=2 text=2 number=0 other=0] merges=A762:A764,B762:B764,C762:C764,H762:I763,J762:J764,K762:K764,D763:D764,E76
3:G763: D763='ریالی' | E763='ارزی'

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=761
  row 761 [n=1 text=1 number=0 other=0] merges=A761:K761: A761='برآورد منابع تامین مالی شرکت در دوره ۶ ماهه منتهی به ۱۴۰
۵/۰۹/۳۰'
  row 762 [n=7 text=7 number=0 other=0] merges=A762:A764,B762:B764,C762:C764,D762:G762,H762:I763,J762:J764,K762:K764: A7
62='محل تامین' | B762='نرخ سود' | C762='مانده اول دوره تسهیلات ارزی و ریالی (میلیون ریال)' | D762='مانده پایان دوره (اصل
 و فرع)' | H762='مانده پایان دوره به تفکیک سررسید' | J762='مبلغ هزینه مالی طی دوره' | K762='سایر توضیحات'
  row 763 [n=2 text=2 number=0 other=0] merges=A762:A764,B762:B764,C762:C764,H762:I763,J762:J764,K762:K764,D763:D764,E76
3:G763: D763='ریالی' | E763='ارزی'
  row 764 [n=5 text=5 number=0 other=0] merges=A762:A764,B762:B764,C762:C764,J762:J764,K762:K764,D763:D764: E764='نوع ار
ز' | F764='مبلغ ارزی' | G764='معادل ریالی تسهیلات ارزی (میلیون ریال)' | H764='کوتاه مدت' | I764='بلند مدت'

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=771
  row 771 [n=1 text=1 number=0 other=0]: A771='منابع تامین مالی (برآوردی پایان سال آینده)'
  row 772 [n=1 text=1 number=0 other=0]: A772='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 773: <EMPTY>
  row 774: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=772
  row 772 [n=1 text=1 number=0 other=0]: A772='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 773: <EMPTY>
  row 774: <EMPTY>
  row 775: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=783
  row 783 [n=1 text=1 number=0 other=0]: A783='توضیحات در خصوص جزئیات منابع تامین مالی شرکت در پایان دوره'
  row 784 [n=1 text=1 number=0 other=0] merges=A784:K784: A784='شرکت در دوره مورد گزارش هیچگونه تسهیلاتی را دریافت نکرده
 است. '
  row 785 [n=1 text=1 number=0 other=0]: A785='برآورد شرکت از برنامه های تامین مالی و تغییرات هزینه های مالی شرکت'
  row 786 [n=1 text=1 number=0 other=0] merges=A786:K786: A786='شرکت در صورت نیاز به تامین مالی نسبت به اخذ تسهیلات مالی
 اقدام خواهد کرد. '

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=784
  row 784 [n=1 text=1 number=0 other=0] merges=A784:K784: A784='شرکت در دوره مورد گزارش هیچگونه تسهیلاتی را دریافت نکرده
 است. '
  row 785 [n=1 text=1 number=0 other=0]: A785='برآورد شرکت از برنامه های تامین مالی و تغییرات هزینه های مالی شرکت'
  row 786 [n=1 text=1 number=0 other=0] merges=A786:K786: A786='شرکت در صورت نیاز به تامین مالی نسبت به اخذ تسهیلات مالی
 اقدام خواهد کرد. '
  row 787 [n=1 text=1 number=0 other=0]: A787='سایر درآمدها و هزینه\u200cهای غیرعملیاتی - درآمد سرمایه\u200cگذاری\u200cه
ا'

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=785
  row 785 [n=1 text=1 number=0 other=0]: A785='برآورد شرکت از برنامه های تامین مالی و تغییرات هزینه های مالی شرکت'
  row 786 [n=1 text=1 number=0 other=0] merges=A786:K786: A786='شرکت در صورت نیاز به تامین مالی نسبت به اخذ تسهیلات مالی
 اقدام خواهد کرد. '
  row 787 [n=1 text=1 number=0 other=0]: A787='سایر درآمدها و هزینه\u200cهای غیرعملیاتی - درآمد سرمایه\u200cگذاری\u200cه
ا'
  row 788 [n=1 text=1 number=0 other=0]: A788='کلیه مبالغ درج شده به میلیون ریال می باشد'

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=786
  row 786 [n=1 text=1 number=0 other=0] merges=A786:K786: A786='شرکت در صورت نیاز به تامین مالی نسبت به اخذ تسهیلات مالی
 اقدام خواهد کرد. '
  row 787 [n=1 text=1 number=0 other=0]: A787='سایر درآمدها و هزینه\u200cهای غیرعملیاتی - درآمد سرمایه\u200cگذاری\u200cه
ا'
  row 788 [n=1 text=1 number=0 other=0]: A788='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 789 [n=4 text=4 number=0 other=0]: A789='شرح' | B789='سال مالی منتهی به ۱۴۰۴/۰۹/۳۰' | C789='دوره ۶ ماهه منتهی به ۱
۴۰۵/۰۳/۳۱' | D789='برآورد دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰'

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=787
  row 787 [n=1 text=1 number=0 other=0]: A787='سایر درآمدها و هزینه\u200cهای غیرعملیاتی - درآمد سرمایه\u200cگذاری\u200cه
ا'
  row 788 [n=1 text=1 number=0 other=0]: A788='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 789 [n=4 text=4 number=0 other=0]: A789='شرح' | B789='سال مالی منتهی به ۱۴۰۴/۰۹/۳۰' | C789='دوره ۶ ماهه منتهی به ۱
۴۰۵/۰۳/۳۱' | D789='برآورد دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰'
  row 790 [n=4 text=1 number=3 other=0]: A790='سود(زيان) ناشي از فروش سرمايه گذاري ها ' | B790=249 | C790=0 | D790=0

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=788
  row 788 [n=1 text=1 number=0 other=0]: A788='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 789 [n=4 text=4 number=0 other=0]: A789='شرح' | B789='سال مالی منتهی به ۱۴۰۴/۰۹/۳۰' | C789='دوره ۶ ماهه منتهی به ۱
۴۰۵/۰۳/۳۱' | D789='برآورد دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰'
  row 790 [n=4 text=1 number=3 other=0]: A790='سود(زيان) ناشي از فروش سرمايه گذاري ها ' | B790=249 | C790=0 | D790=0
  row 791 [n=4 text=1 number=3 other=0]: A791='سود حاصل از سرمايه گذاري در صندوق سرمايه گذاري ' | B791=-535 | C791=0 | D
791=0

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=797
  row 797 [n=1 text=1 number=0 other=0]: A797='سایر درآمدها و هزینه\u200cهای غیرعملیاتی - اقلام متفرقه'
  row 798 [n=1 text=1 number=0 other=0]: A798='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 799 [n=4 text=4 number=0 other=0]: A799='شرح' | B799='سال مالی منتهی به ۱۴۰۴/۰۹/۳۰' | C799='دوره ۶ ماهه منتهی به ۱
۴۰۵/۰۳/۳۱' | D799='برآورد دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰'
  row 800 [n=4 text=1 number=3 other=0]: A800='سود(زيان)ناشي از فروش دارايي ثابت مشهود ' | B800=73650 | C800=0 | D800=14
7301

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=798
  row 798 [n=1 text=1 number=0 other=0]: A798='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 799 [n=4 text=4 number=0 other=0]: A799='شرح' | B799='سال مالی منتهی به ۱۴۰۴/۰۹/۳۰' | C799='دوره ۶ ماهه منتهی به ۱
۴۰۵/۰۳/۳۱' | D799='برآورد دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰'
  row 800 [n=4 text=1 number=3 other=0]: A800='سود(زيان)ناشي از فروش دارايي ثابت مشهود ' | B800=73650 | C800=0 | D800=14
7301
  row 801 [n=4 text=1 number=3 other=0]: A801='سود(زيان)جبران خسارت از بيمه گران ' | B801=-28922 | C801=0 | D801=0

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=808
  row 808 [n=1 text=1 number=0 other=0]: A808='برنامه شرکت در خصوص تقسیم سود'
  row 809 [n=1 text=1 number=0 other=0]: A809='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 810 [n=5 text=5 number=0 other=0]: A810='مبلغ سود انباشته پایان سال مالی گذشته' | B810='سود سهام پیشنهادی هیئت مدی
ره در سال مالی گذشته' | C810='مبلغ سود خالص سال مالی گذشته' | D810='سود سهام مصوب مجمع سال مالی گذشته' | E810='پیشنهاد ه
یئت مدیره درخصوص درصد تقسیم سود سال مالی جاری'
  row 811 [n=5 text=0 number=5 other=0]: A811=56464890 | B811=40500000 | C811=50287149 | D811=49950000 | E811=0

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=809
  row 809 [n=1 text=1 number=0 other=0]: A809='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 810 [n=5 text=5 number=0 other=0]: A810='مبلغ سود انباشته پایان سال مالی گذشته' | B810='سود سهام پیشنهادی هیئت مدی
ره در سال مالی گذشته' | C810='مبلغ سود خالص سال مالی گذشته' | D810='سود سهام مصوب مجمع سال مالی گذشته' | E810='پیشنهاد ه
یئت مدیره درخصوص درصد تقسیم سود سال مالی جاری'
  row 811 [n=5 text=0 number=5 other=0]: A811=56464890 | B811=40500000 | C811=50287149 | D811=49950000 | E811=0
  row 812 [n=1 text=1 number=0 other=0]: A812='سایر برنامه های با اهمیت شرکت'

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=812
  row 812 [n=1 text=1 number=0 other=0]: A812='سایر برنامه های با اهمیت شرکت'
  row 813 [n=2 text=2 number=0 other=0] merges=B813:H813: A813='برآورد دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰ ' | B813='مهم تری
ن برنامه شرکت فعال سازی معادن جدید است. '
  row 814: <EMPTY>
  row 815 [n=1 text=1 number=0 other=0]: A815='سایر توضیحات با اهمیت'

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=815
  row 815 [n=1 text=1 number=0 other=0]: A815='سایر توضیحات با اهمیت'
  row 816 [n=1 text=1 number=0 other=0] merges=A816:K816: A816='به شرح گزارش تفسیری پیوست '
  row 817 [n=1 text=1 number=0 other=0] merges=A817:T817: A817='«جملات آینده\u200cنگر نشان\u200cدهنده انتظارات، باورها ی
ا پیش\u200cبینی\u200cهای جار...
  row 818: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=816
  row 816 [n=1 text=1 number=0 other=0] merges=A816:K816: A816='به شرح گزارش تفسیری پیوست '
  row 817 [n=1 text=1 number=0 other=0] merges=A817:T817: A817='«جملات آینده\u200cنگر نشان\u200cدهنده انتظارات، باورها ی
ا پیش\u200cبینی\u200cهای جار...
  row 818: <EMPTY>
  row 819: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=817
  row 817 [n=1 text=1 number=0 other=0] merges=A817:T817: A817='«جملات آینده\u200cنگر نشان\u200cدهنده انتظارات، باورها ی
ا پیش\u200cبینی\u200cهای جار...
  row 818: <EMPTY>
  row 819: <EMPTY>
  row 820: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=821
  row 821 [n=1 text=1 number=0 other=0]: A821='اعضاي هيئت مديره'
  row 822: <EMPTY>
  row 823: <EMPTY>
  row 824: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=826
  row 826 [n=1 text=1 number=0 other=0]: A826='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 827: <EMPTY>
  row 828: <EMPTY>
  row 829: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=840
  row 840 [n=1 text=1 number=0 other=0]: A840='شرکت های وابسته'
  row 841: <EMPTY>
  row 842: <EMPTY>
  row 843: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=845
  row 845 [n=1 text=1 number=0 other=0]: A845='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 846: <EMPTY>
  row 847: <EMPTY>
  row 848: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=854
  row 854 [n=1 text=1 number=0 other=0] merges=A854:M854: A854='اطلاعات نمایش داده شده با اطلاعات امضا شده مطابقت دارد'
  row 855: <EMPTY>
  row 856: <EMPTY>
  row 857: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=859
  row 859 [n=1 text=1 number=0 other=0]: A859='شرکت های فرعی'
  row 860: <EMPTY>
  row 861: <EMPTY>
  row 862: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=864
  row 864 [n=1 text=1 number=0 other=0]: A864='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 865: <EMPTY>
  row 866: <EMPTY>
  row 867: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=873
  row 873 [n=1 text=1 number=0 other=0] merges=A873:M873: A873='اطلاعات نمایش داده شده با اطلاعات امضا شده مطابقت دارد'
  row 874: <EMPTY>
  row 875: <EMPTY>
  row 876: <EMPTY>

## WORKBOOK excel\samanBank.xlsx
Reader: ACCEPTED
SHA-256: 454985ba50ada23ee08ef7560ae1b892762b58b08375400f9536d797987cb4b5

### SHEET 1 Recovered_Sheet1 | used=A1:M489 | populated_rows=386 | single_text_rows=85

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=3
  row 3 [n=1 text=1 number=0 other=0]: A3='خلاصه اطلاعات گزارش تفسیری - صفحه 1'
  row 4: <EMPTY>
  row 5: <EMPTY>
  row 6: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=8
  row 8 [n=1 text=1 number=0 other=0] merges=A8:K8: A8='اطلاعات این فرم گزیده ای از اطلاعات گزارش تفسیری مدیریت می باشد
که هیئت مدیره شرکت م...
  row 9 [n=1 text=1 number=0 other=0]: A9='مانده تسهیلات اعطایی و ذخیره مطالبات مشکوک الوصول:'
  row 10 [n=1 text=1 number=0 other=0]: A10='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 11 [n=11 text=11 number=0 other=0] merges=A11:A12: A11='شرح' | B11='در تاریخ ۱۴۰۴/۱۲/۲۹' | C11='در تاریخ ۱۴۰۵/۰۶/۳
۱' | D11='در تاریخ ۱۴۰۴/۱۲/۲۹' | E11='در تاریخ ۱۴۰۵/۰۶/۳۱' | F11='در تاریخ ۱۴۰۴/۱۲/۲۹' | G11='در تاریخ ۱۴۰۵/۰۶/۳۱' | H11
='در تاریخ ۱۴۰۴/۱۲/۲۹' | I11='در تاریخ ۱۴۰۵/۰۶/۳۱' | J11='در تاریخ ۱۴۰۴/۱۲/۲۹' | K11='در تاریخ ۱۴۰۵/۰۶/۳۱'

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=9
  row 9 [n=1 text=1 number=0 other=0]: A9='مانده تسهیلات اعطایی و ذخیره مطالبات مشکوک الوصول:'
  row 10 [n=1 text=1 number=0 other=0]: A10='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 11 [n=11 text=11 number=0 other=0] merges=A11:A12: A11='شرح' | B11='در تاریخ ۱۴۰۴/۱۲/۲۹' | C11='در تاریخ ۱۴۰۵/۰۶/۳
۱' | D11='در تاریخ ۱۴۰۴/۱۲/۲۹' | E11='در تاریخ ۱۴۰۵/۰۶/۳۱' | F11='در تاریخ ۱۴۰۴/۱۲/۲۹' | G11='در تاریخ ۱۴۰۵/۰۶/۳۱' | H11
='در تاریخ ۱۴۰۴/۱۲/۲۹' | I11='در تاریخ ۱۴۰۵/۰۶/۳۱' | J11='در تاریخ ۱۴۰۴/۱۲/۲۹' | K11='در تاریخ ۱۴۰۵/۰۶/۳۱'
  row 12 [n=5 text=5 number=0 other=0] merges=A11:A12,B12:C12,D12:E12,F12:G12,H12:I12,J12:K12: B12='جاری' | D12='سررسید
گذشته' | F12='معوق' | H12='مشکوک الوصول' | J12='جمع'

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=10
  row 10 [n=1 text=1 number=0 other=0]: A10='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 11 [n=11 text=11 number=0 other=0] merges=A11:A12: A11='شرح' | B11='در تاریخ ۱۴۰۴/۱۲/۲۹' | C11='در تاریخ ۱۴۰۵/۰۶/۳
۱' | D11='در تاریخ ۱۴۰۴/۱۲/۲۹' | E11='در تاریخ ۱۴۰۵/۰۶/۳۱' | F11='در تاریخ ۱۴۰۴/۱۲/۲۹' | G11='در تاریخ ۱۴۰۵/۰۶/۳۱' | H11
='در تاریخ ۱۴۰۴/۱۲/۲۹' | I11='در تاریخ ۱۴۰۵/۰۶/۳۱' | J11='در تاریخ ۱۴۰۴/۱۲/۲۹' | K11='در تاریخ ۱۴۰۵/۰۶/۳۱'
  row 12 [n=5 text=5 number=0 other=0] merges=A11:A12,B12:C12,D12:E12,F12:G12,H12:I12,J12:K12: B12='جاری' | D12='سررسید
گذشته' | F12='معوق' | H12='مشکوک الوصول' | J12='جمع'
  row 13 [n=11 text=1 number=10 other=0]: A13='تسهیلات اعطایی و مطالبات از اشخاص دولتی ' | B13=0 | C13=0 | D13=0 | E13=0
 | F13=0 | G13=0 | H13=0 | I13=0 | J13=0 | K13=0

[DIRECT_NEXT_ROW_MIXED] anchor_row=17
  row 17 [n=1 text=1 number=0 other=0]: A17='کسر می شود: '
  row 18 [n=11 text=1 number=10 other=0]: A18='سود سالهای آتی ' | B18=598533682 | C18=800232054 | D18=0 | E18=0 | F18=0
| G18=0 | H18=0 | I18=0 | J18=598533682 | K18=800232054
  row 19 [n=11 text=1 number=10 other=0]: A19='سایر ' | B19=71036519 | C19=36115078 | D19=1696766 | E19=429449 | F19=220
654 | G19=2441930 | H19=4165988 | I19=4549590 | J19=77119927 | K19=43536047
  row 20 [n=11 text=1 number=10 other=0]: A20='مانده تسهیلات پایان دوره ' | B20=3382253993 | C20=4583690119 | D20=763910
2 | E20=5067033 | F20=5300932 | G20=8094634 | H20=29173183 | I20=31551091 | J20=3424367210 | K20=4628402877

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=28
  row 28 [n=1 text=1 number=0 other=0]: A28='برآورد شرکت از تغییرات در نرخ سود تسهیلات اعطایی :'
  row 29 [n=2 text=2 number=0 other=0] merges=A29:B29,C29:I29: A29='دوره ۶ ماهه منتهي به ۱۴۰۵/۱۲/۲۹ ' | C29='سود تسهیلات
 تابع سیاستهای شورای پول و اعتبار و همچنین در چارچوب بخشنامه های بانک مرک...
  row 30: <EMPTY>
  row 31 [n=1 text=1 number=0 other=0]: A31='برآورد شرکت از تغییرات در مانده تسهیلات :'

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=31
  row 31 [n=1 text=1 number=0 other=0]: A31='برآورد شرکت از تغییرات در مانده تسهیلات :'
  row 32 [n=2 text=2 number=0 other=0] merges=A32:B32,C32:I32: A32='دوره ۶ ماهه منتهي به ۱۴۰۵/۱۲/۲۹ ' | C32='باتوجه به د
ستورالعمل کنترل مقداری ترازنامه بانکها و پیش بینی افزایش حجم تسهیلات اعطا...
  row 33: <EMPTY>
  row 34 [n=1 text=1 number=0 other=0]: A34='برآورد شرکت از تغییرات در مانده ذخایر مطالبات مشکوک الوصول :'

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=34
  row 34 [n=1 text=1 number=0 other=0]: A34='برآورد شرکت از تغییرات در مانده ذخایر مطالبات مشکوک الوصول :'
  row 35 [n=2 text=2 number=0 other=0] merges=A35:B35,C35:I35: A35='دوره ۶ ماهه منتهي به ۱۴۰۵/۱۲/۲۹ ' | C35='افزایش در ذ
خیره مطالبات مشکوک الوصول ناشی از افزایش ذخیره عام که تابعی از میزان تسهی...
  row 36: <EMPTY>
  row 37 [n=1 text=1 number=0 other=0]: A37='مانده سپرده های دریافتی از مشتریان :'

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=37
  row 37 [n=1 text=1 number=0 other=0]: A37='مانده سپرده های دریافتی از مشتریان :'
  row 38 [n=1 text=1 number=0 other=0]: A38='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 39 [n=4 text=4 number=0 other=0] merges=A39:A40,B39:C39,D39:E39,F39:F40: A39='شرح' | B39='مانده سپرده ها' | D39='م
توسط نرخ سود مانده سپرده ها' | F39='برآورد مدیریت از تغییر در نرخ سود سپرده ها و تغییر در مانده سپرده های دریافتی از مشت
...
  row 40 [n=4 text=4 number=0 other=0] merges=A39:A40,F39:F40: B40='در تاریخ ۱۴۰۴/۱۲/۲۹' | C40='در تاریخ ۱۴۰۵/۰۶/۳۱' | D
40='در تاریخ ۱۴۰۴/۱۲/۲۹' | E40='در تاریخ ۱۴۰۵/۰۶/۳۱'

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=38
  row 38 [n=1 text=1 number=0 other=0]: A38='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 39 [n=4 text=4 number=0 other=0] merges=A39:A40,B39:C39,D39:E39,F39:F40: A39='شرح' | B39='مانده سپرده ها' | D39='م
توسط نرخ سود مانده سپرده ها' | F39='برآورد مدیریت از تغییر در نرخ سود سپرده ها و تغییر در مانده سپرده های دریافتی از مشت
...
  row 40 [n=4 text=4 number=0 other=0] merges=A39:A40,F39:F40: B40='در تاریخ ۱۴۰۴/۱۲/۲۹' | C40='در تاریخ ۱۴۰۵/۰۶/۳۱' | D
40='در تاریخ ۱۴۰۴/۱۲/۲۹' | E40='در تاریخ ۱۴۰۵/۰۶/۳۱'
  row 41 [n=1 text=1 number=0 other=0]: A41='سپرده های ریالی: '

[DIRECT_NEXT_ROW_MIXED] anchor_row=41
  row 41 [n=1 text=1 number=0 other=0]: A41='سپرده های ریالی: '
  row 42 [n=6 text=2 number=4 other=0]: A42='سپرده های کوتاه مدت ' | B42=2336402133 | C42=2924929498 | D42=7 | E42=10 |
F42='متناسب با بخشنامه های بانک مرکزی و در محدوده مجاز میباشد. '
  row 43 [n=6 text=2 number=4 other=0]: A43='سپرده های کوتاه مدت ویژه ' | B43=7300546 | C43=10410409 | D43=14 | E43=13 |
 F43='متناسب با بخشنامه های بانک مرکزی و در محدوده مجاز میباشد. '
  row 44 [n=6 text=2 number=4 other=0]: A44='سپرده های بلند مدت ' | B44=1714598608 | C44=1943998290 | D44=26 | E44=26 |
F44='متناسب با بخشنامه های بانک مرکزی و در محدوده مجاز میباشد. '

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=50
  row 50 [n=1 text=1 number=0 other=0]: A50='اقلام زیر خط:'
  row 51 [n=1 text=1 number=0 other=0]: A51='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 52 [n=6 text=6 number=0 other=0]: A52='شرح' | B52='۱۴۰۵/۰۶/۳۱' | C52='۱۴۰۴/۱۲/۲۹' | D52='شرح' | E52='۱۴۰۵/۰۶/۳۱' |
 F52='۱۴۰۴/۱۲/۲۹'
  row 53 [n=6 text=2 number=4 other=0]: A53='تعهدات مشتریان بابت اعتبارات اسنادی ' | B53=81068897 | C53=47501877 | D53='
تعهدات بانک بابت اعتبارات اسنادی ' | E53=81068897 | F53=47501877

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=51
  row 51 [n=1 text=1 number=0 other=0]: A51='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 52 [n=6 text=6 number=0 other=0]: A52='شرح' | B52='۱۴۰۵/۰۶/۳۱' | C52='۱۴۰۴/۱۲/۲۹' | D52='شرح' | E52='۱۴۰۵/۰۶/۳۱' |
 F52='۱۴۰۴/۱۲/۲۹'
  row 53 [n=6 text=2 number=4 other=0]: A53='تعهدات مشتریان بابت اعتبارات اسنادی ' | B53=81068897 | C53=47501877 | D53='
تعهدات بانک بابت اعتبارات اسنادی ' | E53=81068897 | F53=47501877
  row 54 [n=6 text=2 number=4 other=0]: A54='تعهدات مشتریان بابت ضمانت نامه های صادره ' | B54=645477988 | C54=460435223
| D54='تعهدات بانک بابت ضمانت نامه های صادره ' | E54=645477988 | F54=460435223

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=58
  row 58 [n=1 text=1 number=0 other=0] merges=A58:I58: A58='«جملات آینده\u200cنگر نشان\u200cدهنده انتظارات، باورها یا پی
ش\u200cبینی\u200cهای جار...
  row 59: <EMPTY>
  row 60: <EMPTY>
  row 61: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=62
  row 62 [n=1 text=1 number=0 other=0]: A62='خلاصه اطلاعات گزارش تفسیری - صفحه 2'
  row 63: <EMPTY>
  row 64: <EMPTY>
  row 65: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=67
  row 67 [n=1 text=1 number=0 other=0]: A67='اطلاعات این فرم گزیده ای از اطلاعات گزارش تفسیری مدیریت می باشد که هیئت مدی
ره شرکت م...
  row 68 [n=1 text=1 number=0 other=0]: A68='وضعیت کارکنان:'
  row 69 [n=1 text=1 number=0 other=0]: A69='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 70 [n=4 text=4 number=0 other=0]: A70='شرح' | B70='در تاریخ ۱۴۰۵/۰۶/۳۱' | C70='در تاریخ ۱۴۰۴/۰۶/۳۱' | D70='برآورد
در تاریخ ۱۴۰۵/۱۲/۲۹'

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=68
  row 68 [n=1 text=1 number=0 other=0]: A68='وضعیت کارکنان:'
  row 69 [n=1 text=1 number=0 other=0]: A69='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 70 [n=4 text=4 number=0 other=0]: A70='شرح' | B70='در تاریخ ۱۴۰۵/۰۶/۳۱' | C70='در تاریخ ۱۴۰۴/۰۶/۳۱' | D70='برآورد
در تاریخ ۱۴۰۵/۱۲/۲۹'
  row 71 [n=4 text=1 number=3 other=0]: A71='تعداد شعب ' | B71=137 | C71=137 | D71=137

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=69
  row 69 [n=1 text=1 number=0 other=0]: A69='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 70 [n=4 text=4 number=0 other=0]: A70='شرح' | B70='در تاریخ ۱۴۰۵/۰۶/۳۱' | C70='در تاریخ ۱۴۰۴/۰۶/۳۱' | D70='برآورد
در تاریخ ۱۴۰۵/۱۲/۲۹'
  row 71 [n=4 text=1 number=3 other=0]: A71='تعداد شعب ' | B71=137 | C71=137 | D71=137
  row 72 [n=4 text=1 number=3 other=0]: A72='تعداد کارکنان ' | B72=2790 | C72=2817 | D72=2790

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=73
  row 73 [n=1 text=1 number=0 other=0]: A73='اطلاعات حق الوکاله و کفایت سرمایه'
  row 74 [n=1 text=1 number=0 other=0]: A74='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 75 [n=4 text=4 number=0 other=0] merges=D75:E75: A75='شرح' | B75='دوره ۶ ماهه منتهی به ۱۴۰۵/۰۶/۳۱' | C75='دوره ۶ م
اهه منتهی به ۱۴۰۴/۰۶/۳۱' | D75='برآورد تغییر روند در دوره ۶ ماهه منتهی به ۱۴۰۵/۱۲/۲۹'
  row 76 [n=4 text=2 number=2 other=0] merges=D76:E76: A76='سهم بانک از درآمدهای مشاع ' | B76=49624172 | C76=23107577 |
D76='پیش بینی میشود روند سالهای قبل در سال ۱۴۰۵ادامه داشته باشد. '

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=74
  row 74 [n=1 text=1 number=0 other=0]: A74='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 75 [n=4 text=4 number=0 other=0] merges=D75:E75: A75='شرح' | B75='دوره ۶ ماهه منتهی به ۱۴۰۵/۰۶/۳۱' | C75='دوره ۶ م
اهه منتهی به ۱۴۰۴/۰۶/۳۱' | D75='برآورد تغییر روند در دوره ۶ ماهه منتهی به ۱۴۰۵/۱۲/۲۹'
  row 76 [n=4 text=2 number=2 other=0] merges=D76:E76: A76='سهم بانک از درآمدهای مشاع ' | B76=49624172 | C76=23107577 |
D76='پیش بینی میشود روند سالهای قبل در سال ۱۴۰۵ادامه داشته باشد. '
  row 77 [n=4 text=2 number=2 other=0] merges=D77:E77: A77='سهم سپرده گذاران از درآمدهای مشاع ' | B77=458895930 | C77=23
6433874 | D77='پیش بینی میشود روند سالهای قبل در سال ۱۴۰۵ادامه داشته باشد. '

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=82
  row 82 [n=1 text=1 number=0 other=0]: A82='اهداف و راهبردهای آتی مدیریت در خصوص فعالیت شرکت:'
  row 83 [n=2 text=2 number=0 other=0]: A83='اهداف و راهبردهای آتی مدیریت در خصوص فعالیت شرکت: ' | B83='به شرح مندرج در
گزارش تفسیری مدیریت پیوست '
  row 84 [n=1 text=1 number=0 other=0]: A84='درآمد حاصل از تسهیلات اعطایی و سپرده گذاری'
  row 85 [n=6 text=6 number=0 other=0] merges=F85:G85: A85='شرح' | B85='دوره ۶ ماهه منتهی به ۱۴۰۵/۰۶/۳۱' | C85='متوسط نر
خ سود دوره ۶ ماهه منتهی به ۱۴۰۵/۰۶/۳۱ (درصد)' | D85='دوره ۶ ماهه منتهی به ۱۴۰۴/۰۶/۳۱' | E85='متوسط نرخ سود دوره ۶ ماهه م
نتهی به ۱۴۰۴/۰۶/۳۱ (درصد)' | F85='برآورد تغییر روند در دوره ۶ ماهه منتهی به ۱۴۰۵/۱۲/۲۹'

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=84
  row 84 [n=1 text=1 number=0 other=0]: A84='درآمد حاصل از تسهیلات اعطایی و سپرده گذاری'
  row 85 [n=6 text=6 number=0 other=0] merges=F85:G85: A85='شرح' | B85='دوره ۶ ماهه منتهی به ۱۴۰۵/۰۶/۳۱' | C85='متوسط نر
خ سود دوره ۶ ماهه منتهی به ۱۴۰۵/۰۶/۳۱ (درصد)' | D85='دوره ۶ ماهه منتهی به ۱۴۰۴/۰۶/۳۱' | E85='متوسط نرخ سود دوره ۶ ماهه م
نتهی به ۱۴۰۴/۰۶/۳۱ (درصد)' | F85='برآورد تغییر روند در دوره ۶ ماهه منتهی به ۱۴۰۵/۱۲/۲۹'
  row 86 [n=1 text=1 number=0 other=0] merges=F86:G86: A86='درآمد تسهیلات اعطایی: '
  row 87 [n=6 text=2 number=4 other=0] merges=F87:G87: A87='فروش اقساطی ' | B87=12849695 | C87=0 | D87=6871282 | E87=0 |
 F87='طبق سیاستهای شورای پول و اعتبار و بخشنامه های بانک مرکزی '

[DIRECT_NEXT_ROW_MIXED] anchor_row=86
  row 86 [n=1 text=1 number=0 other=0] merges=F86:G86: A86='درآمد تسهیلات اعطایی: '
  row 87 [n=6 text=2 number=4 other=0] merges=F87:G87: A87='فروش اقساطی ' | B87=12849695 | C87=0 | D87=6871282 | E87=0 |
 F87='طبق سیاستهای شورای پول و اعتبار و بخشنامه های بانک مرکزی '
  row 88 [n=6 text=2 number=4 other=0] merges=F88:G88: A88='جعاله ' | B88=44913856 | C88=0 | D88=8182100 | E88=0 | F88='
طبق سیاستهای شورای پول و اعتبار و بخشنامه های بانک مرکزی '
  row 89 [n=6 text=2 number=4 other=0] merges=F89:G89: A89='اجاره به شرط تملیک ' | B89=614904 | C89=0 | D89=8930 | E89=0
 | F89='طبق سیاستهای شورای پول و اعتبار و بخشنامه های بانک مرکزی '

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=106
  row 106 [n=1 text=1 number=0 other=0]: A106='خالص سود (زیان) سرمایه گذاری\u200c ها'
  row 107 [n=4 text=4 number=0 other=0] merges=D107:E107: A107='شرح' | B107='دوره ۶ ماهه منتهی به ۱۴۰۵/۰۶/۳۱' | C107='دو
ره ۶ ماهه منتهی به ۱۴۰۴/۰۶/۳۱' | D107='برآورد تغییر روند در دوره ۶ ماهه منتهی به ۱۴۰۵/۱۲/۲۹'
  row 108 [n=3 text=1 number=2 other=0] merges=D108:E108: A108='درآمد حاصل از سرمایه گذاری در سهام ' | B108=11253110 | C
108=2536016
  row 109 [n=3 text=1 number=2 other=0] merges=D109:E109: A109='سود(زیان) حاصل از فروش سرمایه گذاری ' | B109=5738603 | C
109=214739

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=112
  row 112 [n=1 text=1 number=0 other=0]: A112='«جملات آینده\u200cنگر نشان\u200cدهنده انتظارات، باورها یا پیش\u200cبینی\u
200cهای جار...
  row 113: <EMPTY>
  row 114: <EMPTY>
  row 115: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=116
  row 116 [n=1 text=1 number=0 other=0]: A116='خلاصه اطلاعات گزارش تفسیری - صفحه 3'
  row 117: <EMPTY>
  row 118: <EMPTY>
  row 119: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=121
  row 121 [n=1 text=1 number=0 other=0]: A121='اطلاعات این فرم گزیده ای از اطلاعات گزارش تفسیری مدیریت می باشد که هیئت م
دیره شرکت م...
  row 122 [n=1 text=1 number=0 other=0]: A122='وضعیت شرکتهای سرمایه پذیر:'
  row 123 [n=1 text=1 number=0 other=0]: A123='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 124 [n=4 text=4 number=0 other=0] merges=A124:B125,C124:F124,G124:I124,J124:K125: A124='نام شرکت' | C124='دوره ۶ م
اهه منتهي به ۱۴۰۵/۰۶/۳۱' | G124='دوره ۶ ماهه منتهي به ۱۴۰۴/۰۶/۳۱' | J124='تشریح آخرین وضعیت و برنامه های آتی شرکت در شرک
ت سرمایه پذیر'

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=122
  row 122 [n=1 text=1 number=0 other=0]: A122='وضعیت شرکتهای سرمایه پذیر:'
  row 123 [n=1 text=1 number=0 other=0]: A123='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 124 [n=4 text=4 number=0 other=0] merges=A124:B125,C124:F124,G124:I124,J124:K125: A124='نام شرکت' | C124='دوره ۶ م
اهه منتهي به ۱۴۰۵/۰۶/۳۱' | G124='دوره ۶ ماهه منتهي به ۱۴۰۴/۰۶/۳۱' | J124='تشریح آخرین وضعیت و برنامه های آتی شرکت در شرک
ت سرمایه پذیر'
  row 125 [n=7 text=7 number=0 other=0] merges=A124:B125,J124:K125: C125='درصد مالکیت' | D125='بهای تمام شده' | E125='سا
ل مالی شرکت سرمایه پذیر' | F125='درآمد سرمایه گذاری - میلیون ریال' | G125='درصد مالکیت' | H125='بهای تمام شده' | I125='د
رآمد سرمایه گذاری - میلیون ریال'

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=123
  row 123 [n=1 text=1 number=0 other=0]: A123='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 124 [n=4 text=4 number=0 other=0] merges=A124:B125,C124:F124,G124:I124,J124:K125: A124='نام شرکت' | C124='دوره ۶ م
اهه منتهي به ۱۴۰۵/۰۶/۳۱' | G124='دوره ۶ ماهه منتهي به ۱۴۰۴/۰۶/۳۱' | J124='تشریح آخرین وضعیت و برنامه های آتی شرکت در شرک
ت سرمایه پذیر'
  row 125 [n=7 text=7 number=0 other=0] merges=A124:B125,J124:K125: C125='درصد مالکیت' | D125='بهای تمام شده' | E125='سا
ل مالی شرکت سرمایه پذیر' | F125='درآمد سرمایه گذاری - میلیون ریال' | G125='درصد مالکیت' | H125='بهای تمام شده' | I125='د
رآمد سرمایه گذاری - میلیون ریال'
  row 126 [n=9 text=3 number=6 other=0] merges=A126:B126,J126:K126: A126='سازمان بورس و اوراق بهادار ' | C126=0 | D126=0
 | E126='۱۴۰۵/۱۲/۲۹ ' | F126=0 | G126=0 | H126=0 | I126=6929 | J126='مطابق روند سالهای قبل '

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=135
  row 135 [n=1 text=1 number=0 other=0]: A135='ساير درآمدها و هزینه های عملياتي:'
  row 136 [n=1 text=1 number=0 other=0]: A136='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 137 [n=3 text=3 number=0 other=0]: A137='شرح' | B137='۱۴۰۵/۰۶/۳۱' | C137='۱۴۰۴/۰۶/۳۱'
  row 138 [n=1 text=1 number=0 other=0]: A138='سایر درآمدهای عملیاتی: '

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=136
  row 136 [n=1 text=1 number=0 other=0]: A136='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 137 [n=3 text=3 number=0 other=0]: A137='شرح' | B137='۱۴۰۵/۰۶/۳۱' | C137='۱۴۰۴/۰۶/۳۱'
  row 138 [n=1 text=1 number=0 other=0]: A138='سایر درآمدهای عملیاتی: '
  row 139 [n=3 text=1 number=2 other=0]: A139='ساير درآمد ها ' | B139=61120834 | C139=0

[DIRECT_NEXT_ROW_MIXED] anchor_row=138
  row 138 [n=1 text=1 number=0 other=0]: A138='سایر درآمدهای عملیاتی: '
  row 139 [n=3 text=1 number=2 other=0]: A139='ساير درآمد ها ' | B139=61120834 | C139=0
  row 140: <EMPTY>
  row 141 [n=3 text=1 number=2 other=0]: A141='جمع سایر درآمدهای عملیاتی ' | B141=61120834 | C141=0

[DIRECT_NEXT_ROW_MIXED] anchor_row=142
  row 142 [n=1 text=1 number=0 other=0]: A142='سایر هزینه های عملیاتی: '
  row 143 [n=3 text=1 number=2 other=0]: A143='ساير هزينه ها ' | B143=-2464025 | C143=-1857935
  row 144: <EMPTY>
  row 145 [n=3 text=1 number=2 other=0]: A145='جمع سایر هزینه های عملیاتی ' | B145=-2464025 | C145=-1857935

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=147
  row 147 [n=1 text=1 number=0 other=0]: A147='برآورد شرکت از تغییرات خالص سایر درآمدها (هزینه ها)ی عملیاتی:'
  row 148 [n=2 text=2 number=0 other=0] merges=A148:B148: A148='دوره ۶ ماهه منتهي به ۱۴۰۵/۱۲/۲۹ ' | C148='تغییرات این بخ
ش متاثر از تغییرنرخ تسعیر ارز توسط بانک مرکزی ج.ا.ا میباشد. '
  row 149: <EMPTY>
  row 150 [n=1 text=1 number=0 other=0]: A150='خالص ساير درآمدها و هزینه ها:'

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=150
  row 150 [n=1 text=1 number=0 other=0]: A150='خالص ساير درآمدها و هزینه ها:'
  row 151 [n=1 text=1 number=0 other=0]: A151='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 152 [n=3 text=3 number=0 other=0]: A152='خالص سایر درآمدها و هزینه ها' | B152='۱۴۰۵/۰۶/۳۱' | C152='۱۴۰۴/۰۶/۳۱'
  row 153 [n=3 text=1 number=2 other=0]: A153='ساير درآمد ها ' | B153=19745098 | C153=23761039

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=151
  row 151 [n=1 text=1 number=0 other=0]: A151='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 152 [n=3 text=3 number=0 other=0]: A152='خالص سایر درآمدها و هزینه ها' | B152='۱۴۰۵/۰۶/۳۱' | C152='۱۴۰۴/۰۶/۳۱'
  row 153 [n=3 text=1 number=2 other=0]: A153='ساير درآمد ها ' | B153=19745098 | C153=23761039
  row 154: <EMPTY>

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=156
  row 156 [n=1 text=1 number=0 other=0]: A156='برآورد شرکت از تغییرات خالص ساير درآمدها و هزینه ها :'
  row 157 [n=2 text=2 number=0 other=0] merges=A157:B157: A157='دوره ۶ ماهه منتهي به ۱۴۰۵/۱۲/۲۹ ' | C157='پیش بینی میشود
 روند دوره های قبل ادامه داشته باشد. '
  row 158: <EMPTY>
  row 159 [n=1 text=1 number=0 other=0]: A159='هزینه های اداری و عمومی:'

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=159
  row 159 [n=1 text=1 number=0 other=0]: A159='هزینه های اداری و عمومی:'
  row 160 [n=1 text=1 number=0 other=0]: A160='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 161 [n=3 text=3 number=0 other=0]: A161='هزینه های اداری و عمومی' | B161='۱۴۰۵/۰۶/۳۱' | C161='۱۴۰۴/۰۶/۳۱'
  row 162 [n=3 text=1 number=2 other=0]: A162='هزينه هاي کارکنان ' | B162=-37878233 | C162=-30787973

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=160
  row 160 [n=1 text=1 number=0 other=0]: A160='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 161 [n=3 text=3 number=0 other=0]: A161='هزینه های اداری و عمومی' | B161='۱۴۰۵/۰۶/۳۱' | C161='۱۴۰۴/۰۶/۳۱'
  row 162 [n=3 text=1 number=2 other=0]: A162='هزينه هاي کارکنان ' | B162=-37878233 | C162=-30787973
  row 163 [n=3 text=1 number=2 other=0]: A163='هزينه هاي اداري ' | B163=-57657167 | C163=-20978933

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=167
  row 167 [n=1 text=1 number=0 other=0]: A167='برآورد شرکت از تغییرات هزینه های اداری و عمومی :'
  row 168 [n=2 text=2 number=0 other=0] merges=A168:B168: A168='دوره ۶ ماهه منتهي به ۱۴۰۵/۱۲/۲۹ ' | C168='هزینه های ادار
ی وعمومی شامل هزینه های کارکنان وسایرهزینه های اداری وعمومی میباشد.افز...
  row 169: <EMPTY>
  row 170 [n=1 text=1 number=0 other=0]: A170='هزینه مالی:'

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=170
  row 170 [n=1 text=1 number=0 other=0]: A170='هزینه مالی:'
  row 171 [n=1 text=1 number=0 other=0]: A171='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 172 [n=3 text=3 number=0 other=0]: A172='هزینه\u200cهای مالی' | B172='۱۴۰۵/۰۶/۳۱' | C172='۱۴۰۴/۰۶/۳۱'
  row 173 [n=3 text=1 number=2 other=0]: A173='هزینه مالی تسهیلات دریافتی از سایر بانکها و موسسات اعتباری ' | B173=0 | C
173=0

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=171
  row 171 [n=1 text=1 number=0 other=0]: A171='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 172 [n=3 text=3 number=0 other=0]: A172='هزینه\u200cهای مالی' | B172='۱۴۰۵/۰۶/۳۱' | C172='۱۴۰۴/۰۶/۳۱'
  row 173 [n=3 text=1 number=2 other=0]: A173='هزینه مالی تسهیلات دریافتی از سایر بانکها و موسسات اعتباری ' | B173=0 | C
173=0
  row 174 [n=3 text=1 number=2 other=0]: A174='جریمه اضافه برداشت از بانک مرکزی ' | B174=0 | C174=0

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=177
  row 177 [n=1 text=1 number=0 other=0]: A177='برآورد شرکت از تغییرات هزینه های مالی :'
  row 178 [n=2 text=2 number=0 other=0] merges=A178:B178: A178='دوره ۶ ماهه منتهي به ۱۴۰۵/۱۲/۲۹ ' | C178='پیش بینی میشود
 این رقم حدود ۱.۰۰۰.۰۰۰ میلیون ریال افزایش یابد '
  row 179: <EMPTY>
  row 180 [n=1 text=1 number=0 other=0]: A180='برنامه شرکت در خصوص تقسیم سود'

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=180
  row 180 [n=1 text=1 number=0 other=0]: A180='برنامه شرکت در خصوص تقسیم سود'
  row 181 [n=5 text=5 number=0 other=0]: A181='مبلغ سود (زيان) انباشته پايان سال مالي گذشته' | B181='سود سهام پیشنهادی ه
یئت مدیره در سال مالی گذشته' | C181='مبلغ سود (زيان) خالص سال مالي گذشته' | D181='سود سهام مصوب مجمع سال مالی گذشته' | E
181='پیشنهاد هیئت مدیره درخصوص درصد تقسیم سود سال مالی جاری'
  row 182 [n=5 text=0 number=5 other=0]: A182=150548777 | B182=18906793 | C182=177067928 | D182=-11000000 | E182=0
  row 183 [n=1 text=1 number=0 other=0]: A183='سایر برنامه های با اهمیت شرکت'

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=183
  row 183 [n=1 text=1 number=0 other=0]: A183='سایر برنامه های با اهمیت شرکت'
  row 184 [n=2 text=2 number=0 other=0]: A184='دوره ۶ ماهه منتهي به ۱۴۰۵/۱۲/۲۹ ' | B184='به شرح مندرج در گزارش تفسیری مد
یریت پیوست '
  row 185: <EMPTY>
  row 186 [n=1 text=1 number=0 other=0]: A186='سایر توضیحات با اهمیت'

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=186
  row 186 [n=1 text=1 number=0 other=0]: A186='سایر توضیحات با اهمیت'
  row 187 [n=1 text=1 number=0 other=0] merges=A187:K187: A187='به شرح مندرج در گزارش تفسیری مدیریت پیوست '
  row 188 [n=1 text=1 number=0 other=0]: A188='«جملات آینده\u200cنگر نشان\u200cدهنده انتظارات، باورها یا پیش\u200cبینی\u
200cهای جار...
  row 189: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=187
  row 187 [n=1 text=1 number=0 other=0] merges=A187:K187: A187='به شرح مندرج در گزارش تفسیری مدیریت پیوست '
  row 188 [n=1 text=1 number=0 other=0]: A188='«جملات آینده\u200cنگر نشان\u200cدهنده انتظارات، باورها یا پیش\u200cبینی\u
200cهای جار...
  row 189: <EMPTY>
  row 190: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=188
  row 188 [n=1 text=1 number=0 other=0]: A188='«جملات آینده\u200cنگر نشان\u200cدهنده انتظارات، باورها یا پیش\u200cبینی\u
200cهای جار...
  row 189: <EMPTY>
  row 190: <EMPTY>
  row 191: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=192
  row 192 [n=1 text=1 number=0 other=0]: A192='صورت سود و زیان'
  row 193: <EMPTY>
  row 194: <EMPTY>
  row 195: <EMPTY>

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=197
  row 197 [n=1 text=1 number=0 other=0]: A197='صورت سود و زیان'
  row 198 [n=1 text=1 number=0 other=0]: A198='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 199 [n=4 text=4 number=0 other=0] merges=A199:A200,D199:D200: A199='شرح' | B199='دوره منتهی به ۱۴۰۵/۰۶/۳۱' | C199=
'تجدید ارائه شده ۱۴۰۴/۰۶/۳۱' | D199='درصد تغییرات'
  row 200 [n=2 text=2 number=0 other=0] merges=A199:A200,D199:D200: B200='حسابرسی نشده' | C200='حسابرسی شده'

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=198
  row 198 [n=1 text=1 number=0 other=0]: A198='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 199 [n=4 text=4 number=0 other=0] merges=A199:A200,D199:D200: A199='شرح' | B199='دوره منتهی به ۱۴۰۵/۰۶/۳۱' | C199=
'تجدید ارائه شده ۱۴۰۴/۰۶/۳۱' | D199='درصد تغییرات'
  row 200 [n=2 text=2 number=0 other=0] merges=A199:A200,D199:D200: B200='حسابرسی نشده' | C200='حسابرسی شده'
  row 201 [n=1 text=1 number=0 other=0]: A201='عملیات در حال تداوم: '

[DIRECT_NEXT_ROW_MIXED] anchor_row=201
  row 201 [n=1 text=1 number=0 other=0]: A201='عملیات در حال تداوم: '
  row 202 [n=4 text=1 number=3 other=0]: A202='درآمد تسهيلات اعطايي ' | B202=432843600 | C202=242014199 | D202=79
  row 203 [n=4 text=1 number=3 other=0]: A203='درآمد سپرده گذاری در بانک ها و موسسات اعتباری غیر بانکی ' | B203=45119484
 | C203=10944795 | D203=312
  row 204 [n=4 text=1 number=3 other=0]: A204='درآمد سرمایه گذاری در اوراق بدهی ' | B204=31489756 | C204=12222406 | D204
=158

[DIRECT_NEXT_ROW_MIXED] anchor_row=223
  row 223 [n=1 text=1 number=0 other=0]: A223='عملیات متوقف شده: '
  row 224 [n=3 text=1 number=2 other=0]: A224='سود(زیان)خالص عملیات متوقف شده ' | B224=0 | C224=0
  row 225 [n=4 text=1 number=3 other=0]: A225='سود(زیان)خالص ' | B225=107051976 | C225=31248229 | D225=243
  row 226 [n=1 text=1 number=0 other=0]: A226='سود (زیان) هر سهم (ريال) '

[DIRECT_NEXT_ROW_MIXED] anchor_row=226
  row 226 [n=1 text=1 number=0 other=0]: A226='سود (زیان) هر سهم (ريال) '
  row 227 [n=4 text=1 number=3 other=0]: A227='عملیاتی (ریال) ' | B227=581 | C227=59 | D227=885
  row 228 [n=4 text=1 number=3 other=0]: A228='غیرعملیاتی(ریال) ' | B228=112 | C228=142 | D228=-21
  row 229 [n=4 text=1 number=3 other=0]: A229='ناشی از عملیات در حال تداوم(ریال) ' | B229=693 | C229=201 | D229=245

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=235
  row 235 [n=1 text=1 number=0 other=0] merges=A235:F235: A235='دلایل تغییرات اطلاعات واقعی دوره منتهی به ۱۴۰۵/۰۶/۳۱ '
  row 236: <EMPTY>
  row 237 [n=1 text=1 number=0 other=0] merges=A237:F237: A237='دلایل تغییرات اطلاعات واقعی دوره منتهی به ۱۴۰۴/۰۶/۳۱ '
  row 238: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=237
  row 237 [n=1 text=1 number=0 other=0] merges=A237:F237: A237='دلایل تغییرات اطلاعات واقعی دوره منتهی به ۱۴۰۴/۰۶/۳۱ '
  row 238: <EMPTY>
  row 239: <EMPTY>
  row 240: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=244
  row 244 [n=1 text=1 number=0 other=0]: A244='صورت سود و زیان جامع'
  row 245: <EMPTY>
  row 246: <EMPTY>
  row 247: <EMPTY>

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=249
  row 249 [n=1 text=1 number=0 other=0]: A249='صورت سود و زیان جامع'
  row 250 [n=1 text=1 number=0 other=0]: A250='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 251 [n=4 text=4 number=0 other=0] merges=A251:A252,D251:D252: A251='شرح' | B251='دوره منتهی به۱۴۰۵/۰۶/۳۱' | C251='
تجدید ارائه شده۱۴۰۴/۰۶/۳۱' | D251='درصد تغییر'
  row 252 [n=2 text=2 number=0 other=0] merges=A251:A252,D251:D252: B252='حسابرسی نشده' | C252='حسابرسی شده'

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=250
  row 250 [n=1 text=1 number=0 other=0]: A250='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 251 [n=4 text=4 number=0 other=0] merges=A251:A252,D251:D252: A251='شرح' | B251='دوره منتهی به۱۴۰۵/۰۶/۳۱' | C251='
تجدید ارائه شده۱۴۰۴/۰۶/۳۱' | D251='درصد تغییر'
  row 252 [n=2 text=2 number=0 other=0] merges=A251:A252,D251:D252: B252='حسابرسی نشده' | C252='حسابرسی شده'
  row 253 [n=4 text=1 number=3 other=0]: A253='سود(زیان) خالص ' | B253=107051976 | C253=31248229 | D253=243

[DIRECT_NEXT_ROW_MIXED] anchor_row=254
  row 254 [n=1 text=1 number=0 other=0]: A254='سایر اقلام سود و زیان جامع: '
  row 255 [n=3 text=1 number=2 other=0]: A255='مازاد تجديد ارزيابي دارايي\u200cها ' | B255=0 | C255=0
  row 256 [n=4 text=1 number=3 other=0]: A256='تفاوت تسعیر ارز عملیات خارجی ' | B256=5244549 | C256=1258917 | D256=317
  row 257 [n=3 text=1 number=2 other=0]: A257='مالیات مربوط به سایر اقلام سود و زیان جامع ' | B257=0 | C257=0

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=263
  row 263 [n=1 text=1 number=0 other=0]: A263='صورت وضعیت مالی'
  row 264: <EMPTY>
  row 265: <EMPTY>
  row 266: <EMPTY>

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=268
  row 268 [n=1 text=1 number=0 other=0]: A268='صورت وضعیت مالی'
  row 269 [n=1 text=1 number=0 other=0]: A269='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 270 [n=5 text=5 number=0 other=0] merges=A270:A271,E270:E271: A270='شرح' | B270='دوره منتهی به ۱۴۰۵/۰۶/۳۱' | C270=
'تجدید ارائه شده۱۴۰۴/۱۲/۲۹' | D270='تجدید ارائه شده۱۴۰۴/۰۱/۰۱' | E270='درصد تغییرات'
  row 271 [n=3 text=3 number=0 other=0] merges=A270:A271,E270:E271: B271='حسابرسی نشده' | C271='حسابرسی شده' | D271='حسا
برسی شده'

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=269
  row 269 [n=1 text=1 number=0 other=0]: A269='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 270 [n=5 text=5 number=0 other=0] merges=A270:A271,E270:E271: A270='شرح' | B270='دوره منتهی به ۱۴۰۵/۰۶/۳۱' | C270=
'تجدید ارائه شده۱۴۰۴/۱۲/۲۹' | D270='تجدید ارائه شده۱۴۰۴/۰۱/۰۱' | E270='درصد تغییرات'
  row 271 [n=3 text=3 number=0 other=0] merges=A270:A271,E270:E271: B271='حسابرسی نشده' | C271='حسابرسی شده' | D271='حسا
برسی شده'
  row 272 [n=4 text=4 number=0 other=0]: A272='دارایی ها ' | B272='ميليون ريال ' | C272='ميليون ريال ' | D272='میلیون ری
ال '

[DIRECT_NEXT_ROW_MIXED] anchor_row=289
  row 289 [n=1 text=1 number=0 other=0]: A289='بدهی\u200cها '
  row 290 [n=5 text=1 number=4 other=0]: A290='سپرده\u200cهاي مشتریان ' | B290=7948184039 | C290=6209237149 | D290=31732
14293 | E290=28
  row 291 [n=5 text=1 number=4 other=0]: A291='بدهي به بانكها و موسسات اعتباري غیر بانکی ' | B291=3701339828 | C291=2874
143188 | D291=1212198944 | E291=29
  row 292 [n=5 text=1 number=4 other=0]: A292='سود سهام پرداختني ' | B292=1598637 | C292=704699 | D292=370455 | E292=127


[DIRECT_NEXT_ROW_MIXED] anchor_row=300
  row 300 [n=1 text=1 number=0 other=0]: A300='حقوق مالکانه '
  row 301 [n=5 text=1 number=4 other=0]: A301='سرمايه ' | B301=158000000 | C301=158000000 | D301=110000000 | E301=0
  row 302 [n=4 text=1 number=3 other=0]: A302='افزايش سرمايه در جريان ' | B302=0 | C302=0 | D302=0
  row 303 [n=4 text=1 number=3 other=0]: A303='صرف سهام ' | B303=0 | C303=0 | D303=0

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=316
  row 316 [n=1 text=1 number=0 other=0]: A316='صورت تغییرات در حقوق مالکانه'
  row 317: <EMPTY>
  row 318: <EMPTY>
  row 319: <EMPTY>

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=321
  row 321 [n=1 text=1 number=0 other=0]: A321='صورت تغییرات در حقوق مالکانه'
  row 322 [n=1 text=1 number=0 other=0]: A322='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 323 [n=12 text=12 number=0 other=0]: A323='شرح' | B323='سرمایه' | C323='افزایش سرمایه در جریان' | D323='صرف سهام'
| E323='صرف سهام خزانه' | F323='اندوخته قانونی' | G323='سایر اندوخته\u200cها' | H323='مازاد تجدید ارزیابی دارایی\u200cها
' | I323='تفاوت تسعیر ارز عملیات خارجی' | J323='سود(زیان) انباشته' | K323='سهام خزانه' | L323='جمع کل'
  row 324 [n=12 text=1 number=11 other=0]: A324='مانده در۱۴۰۵/۰۱/۰۱ ' | B324=158000000 | C324=0 | D324=0 | E324=206737 |
 F324=58395017 | G324=28218 | H324=10187858 | I324=23712301 | J324=162548777 | K324=-11152721 | L324=401926187

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=322
  row 322 [n=1 text=1 number=0 other=0]: A322='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 323 [n=12 text=12 number=0 other=0]: A323='شرح' | B323='سرمایه' | C323='افزایش سرمایه در جریان' | D323='صرف سهام'
| E323='صرف سهام خزانه' | F323='اندوخته قانونی' | G323='سایر اندوخته\u200cها' | H323='مازاد تجدید ارزیابی دارایی\u200cها
' | I323='تفاوت تسعیر ارز عملیات خارجی' | J323='سود(زیان) انباشته' | K323='سهام خزانه' | L323='جمع کل'
  row 324 [n=12 text=1 number=11 other=0]: A324='مانده در۱۴۰۵/۰۱/۰۱ ' | B324=158000000 | C324=0 | D324=0 | E324=206737 |
 F324=58395017 | G324=28218 | H324=10187858 | I324=23712301 | J324=162548777 | K324=-11152721 | L324=401926187
  row 325 [n=3 text=1 number=2 other=0]: A325='اصلاح اشتباهات ' | J325=-12000000 | L325=-12000000

[DIRECT_NEXT_ROW_MIXED] anchor_row=329
  row 329 [n=1 text=1 number=0 other=0]: A329='سایر اقلام سود و زیان جامع '
  row 330 [n=3 text=1 number=2 other=0]: A330='مازاد تجدید ارزیابی دارایی ها ' | H330=0 | L330=0
  row 331 [n=3 text=1 number=2 other=0]: A331='تفاوت تسعیر ارز عملیات خارجی ' | I331=5244549 | L331=5244549
  row 332 [n=5 text=1 number=4 other=0]: A332='آثار مالیاتی سایر اقلام سود(زیان)جامع ' | H332=0 | I332=0 | J332=0 | L332
=0

[DIRECT_NEXT_ROW_MIXED] anchor_row=349
  row 349 [n=1 text=1 number=0 other=0]: A349='تغییرات حقوقی مالکانه سال ۱۴۰۴/۱۲/۲۹ '
  row 350 [n=3 text=1 number=2 other=0]: A350='سود(زیان) خالص گزارش شده در صورتهای مالی سال ۱۴۰۴/۱۲/۲۹ ' | J350=18906792
8 | L350=189067928
  row 351 [n=3 text=1 number=2 other=0]: A351='اصلاح اشتباهات ' | J351=-12000000 | L351=-12000000
  row 352 [n=3 text=1 number=2 other=0]: A352='تغییر در رویه حسابداری ' | J352=0 | L352=0

[DIRECT_NEXT_ROW_MIXED] anchor_row=354
  row 354 [n=1 text=1 number=0 other=0]: A354='سایر اقلام سود(زیان)جامع '
  row 355 [n=3 text=1 number=2 other=0]: A355='مازاد تجدید ارزیابی دارایی ها ' | H355=0 | L355=0
  row 356 [n=3 text=1 number=2 other=0]: A356='تفاوت تسعیر ارز عملیات خارجی ' | I356=14374026 | L356=14374026
  row 357 [n=5 text=1 number=4 other=0]: A357='آثار مالیاتی سایر اقلام سود(زیان)جامع ' | H357=0 | I357=0 | J357=0 | L357
=0

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=373
  row 373 [n=1 text=1 number=0 other=0]: A373='صورت جریان های نقدی'
  row 374: <EMPTY>
  row 375: <EMPTY>
  row 376: <EMPTY>

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=378
  row 378 [n=1 text=1 number=0 other=0]: A378='صورت جریان های نقدی'
  row 379 [n=1 text=1 number=0 other=0]: A379='کلیه مبالغ به میلیون ریال است'
  row 380 [n=4 text=4 number=0 other=0] merges=A380:A381,D380:D381: A380='شرح' | B380='دوره منتهی به۱۴۰۵/۰۶/۳۱' | C380='
تجدید ارائه شده۱۴۰۴/۰۶/۳۱' | D380='درصد تغییر'
  row 381 [n=2 text=2 number=0 other=0] merges=A380:A381,D380:D381: B381='حسابرسی نشده' | C381='حسابرسی شده'

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=379
  row 379 [n=1 text=1 number=0 other=0]: A379='کلیه مبالغ به میلیون ریال است'
  row 380 [n=4 text=4 number=0 other=0] merges=A380:A381,D380:D381: A380='شرح' | B380='دوره منتهی به۱۴۰۵/۰۶/۳۱' | C380='
تجدید ارائه شده۱۴۰۴/۰۶/۳۱' | D380='درصد تغییر'
  row 381 [n=2 text=2 number=0 other=0] merges=A380:A381,D380:D381: B381='حسابرسی نشده' | C381='حسابرسی شده'
  row 382 [n=1 text=1 number=0 other=0]: A382='جریان\xadهای نقدی حاصل از فعاليت\u200cهاي عملياتي: '

[DIRECT_NEXT_ROW_MIXED] anchor_row=382
  row 382 [n=1 text=1 number=0 other=0]: A382='جریان\xadهای نقدی حاصل از فعاليت\u200cهاي عملياتي: '
  row 383 [n=4 text=1 number=3 other=0]: A383='نقد حاصل از عملیات ' | B383=310867468 | C383=21130489 | D383=1371
  row 384 [n=3 text=1 number=2 other=0]: A384='پرداخت\u200cهای نقدی بابت مالیات بر درآمد ' | B384=0 | C384=0
  row 385 [n=4 text=1 number=3 other=0]: A385='جريان \u200cخالص \u200cورود\u200c (خروج) \u200cنقد حاصل از فعاليت\u200cها
ي \u200cعمل... | B385=310867468 | C385=21130489 | D385=1371

[DIRECT_NEXT_ROW_MIXED] anchor_row=386
  row 386 [n=1 text=1 number=0 other=0]: A386='جریان های نقدی حاصل از فعالیت های سرمایه گذاری '
  row 387 [n=4 text=1 number=3 other=0]: A387='پرداخت های نقدی برای تحصیل دارایی ثابت مشهود ' | B387=-104259778 | C387=-
3577275 | D387=-2815
  row 388 [n=4 text=1 number=3 other=0]: A388='دریافت های نقدی حاصل از فروش دارایی های ثابت مشهود ' | B388=2567296 | C38
8=6015 | D388=42582
  row 389 [n=4 text=1 number=3 other=0]: A389='پرداخت های نقدی برای تحصیل دارایی نا مشهود ' | B389=-849181 | C389=-50129
7 | D389=-69

[DIRECT_NEXT_ROW_MIXED] anchor_row=399
  row 399 [n=1 text=1 number=0 other=0]: A399='جریان های نقدی حاصل از فعالیت های تامین مالی '
  row 400 [n=3 text=1 number=2 other=0]: A400='دریافت های نقدی حاصل از افزایش سرمایه ' | B400=0 | C400=0
  row 401 [n=4 text=1 number=3 other=0]: A401='دریافت های نقدی حاصل از فروش سهام خزانه ' | B401=10890849 | C401=4825427
| D401=126
  row 402 [n=4 text=1 number=3 other=0]: A402='پرداخت های نقدی برای خرید سهام خزانه ' | B402=-21734108 | C402=-5108411 |
 D402=-325

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=423
  row 423 [n=1 text=1 number=0 other=0] merges=A423:F423: A423='دلایل تغییرات اطلاعات واقعی دوره منتهی به ۱۴۰۵/۰۶/۳۱ '
  row 424: <EMPTY>
  row 425 [n=1 text=1 number=0 other=0] merges=A425:F425: A425='دلایل تغییرات اطلاعات واقعی دوره منتهی به ۱۴۰۴/۰۶/۳۱ '
  row 426: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=425
  row 425 [n=1 text=1 number=0 other=0] merges=A425:F425: A425='دلایل تغییرات اطلاعات واقعی دوره منتهی به ۱۴۰۴/۰۶/۳۱ '
  row 426: <EMPTY>
  row 427: <EMPTY>
  row 428: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=432
  row 432 [n=1 text=1 number=0 other=0]: A432='شرکت های فرعی'
  row 433: <EMPTY>
  row 434: <EMPTY>
  row 435: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=437
  row 437 [n=1 text=1 number=0 other=0]: A437='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 438: <EMPTY>
  row 439: <EMPTY>
  row 440: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=469
  row 469 [n=1 text=1 number=0 other=0] merges=A469:M469: A469='اطلاعات نمایش داده شده با اطلاعات امضا شده مطابقت دارد'
  row 470: <EMPTY>
  row 471: <EMPTY>
  row 472: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=474
  row 474 [n=1 text=1 number=0 other=0]: A474='شرکت های وابسته'
  row 475: <EMPTY>
  row 476: <EMPTY>
  row 477: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=479
  row 479 [n=1 text=1 number=0 other=0]: A479='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 480: <EMPTY>
  row 481: <EMPTY>
  row 482: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=488
  row 488 [n=1 text=1 number=0 other=0] merges=A488:M488: A488='اطلاعات نمایش داده شده با اطلاعات امضا شده مطابقت دارد'
  row 489: <EMPTY>
  row 490: <EMPTY>
  row 491: <EMPTY>

## WORKBOOK excel\parsian_periodic.xlsx
Reader: ACCEPTED
SHA-256: b5623964d336dd679eaa8208fb800fdbf24351ff85bc996e05210b37f342e6da

### SHEET 1 Recovered_Sheet1 | used=A1:L411 | populated_rows=330 | single_text_rows=84

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=3
  row 3 [n=1 text=1 number=0 other=0]: A3='صورت سود و زیان'
  row 4: <EMPTY>
  row 5: <EMPTY>
  row 6: <EMPTY>

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=8
  row 8 [n=1 text=1 number=0 other=0]: A8='صورت سود و زیان'
  row 9 [n=1 text=1 number=0 other=0]: A9='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 10 [n=5 text=5 number=0 other=0] merges=A10:A11,E10:E11: A10='شرح' | B10='دوره منتهي به ۱۴۰۳/۰۶/۳۱' | C10='تجدید ا
رائه شده ۱۴۰۲/۰۶/۳۱' | D10='تجدید ارائه شده ۱۴۰۲/۱۲/۲۹' | E10='درصد تغييرات'
  row 11 [n=3 text=3 number=0 other=0] merges=A10:A11,E10:E11: B11='حسابرسی نشده' | C11='حسابرسی شده' | D11='حسابرسی شده
'

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=9
  row 9 [n=1 text=1 number=0 other=0]: A9='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 10 [n=5 text=5 number=0 other=0] merges=A10:A11,E10:E11: A10='شرح' | B10='دوره منتهي به ۱۴۰۳/۰۶/۳۱' | C10='تجدید ا
رائه شده ۱۴۰۲/۰۶/۳۱' | D10='تجدید ارائه شده ۱۴۰۲/۱۲/۲۹' | E10='درصد تغييرات'
  row 11 [n=3 text=3 number=0 other=0] merges=A10:A11,E10:E11: B11='حسابرسی نشده' | C11='حسابرسی شده' | D11='حسابرسی شده
'
  row 12 [n=1 text=1 number=0 other=0]: A12='عملیات در حال تداوم: '

[DIRECT_NEXT_ROW_MIXED] anchor_row=12
  row 12 [n=1 text=1 number=0 other=0]: A12='عملیات در حال تداوم: '
  row 13 [n=5 text=1 number=4 other=0]: A13='درآمد تسهيلات اعطايي و سپرده گذاری و اوراق بدهی ' | B13=147186330 | C13=870
74365 | D13=229849193 | E13=69
  row 14 [n=5 text=1 number=4 other=0]: A14='هزينه سود سپرده\u200cها ' | B14=-230307149 | C14=-157273597 | D14=-34554248
6 | E14=-46
  row 15 [n=5 text=1 number=4 other=0]: A15='خالص درآمد تسهیلات و سپرده گذاری ' | B15=-83120819 | C15=-70199232 | D15=-1
15693293 | E15=-18

[DIRECT_NEXT_ROW_MIXED] anchor_row=32
  row 32 [n=1 text=1 number=0 other=0]: A32='عملیات متوقف شده: '
  row 33 [n=4 text=1 number=3 other=0]: A33='سود(زیان) خالص عملیات متوقف شده ' | B33=0 | C33=0 | D33=0
  row 34 [n=5 text=1 number=4 other=0]: A34='سود(زیان) خالص ' | B34=-25195703 | C34=-35246257 | D34=-9124895 | E34=29
  row 35 [n=1 text=1 number=0 other=0]: A35='سود (زیان)پایه هر سهم (ريال) '

[DIRECT_NEXT_ROW_MIXED] anchor_row=35
  row 35 [n=1 text=1 number=0 other=0]: A35='سود (زیان)پایه هر سهم (ريال) '
  row 36 [n=5 text=1 number=4 other=0]: A36='عملياتي (ريال) ' | B36=-152 | C36=-416 | D36=-237 | E36=63
  row 37 [n=5 text=1 number=4 other=0]: A37='غيرعملياتي(ريال) ' | B37=-22 | C37=174 | D37=174 | E37=-113
  row 38 [n=5 text=1 number=4 other=0]: A38='ناشی از عملیات در حال تداوم(ریال) ' | B38=-174 | C38=-242 | D38=-63 | E38=2
8

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=44
  row 44 [n=1 text=1 number=0 other=0] merges=A44:E44: A44='دلایل تغییرات اطلاعات واقعی دوره منتهی به ۱۴۰۳/۰۶/۳۱ '
  row 45: <EMPTY>
  row 46 [n=1 text=1 number=0 other=0] merges=A46:E46: A46='دلایل تغییرات اطلاعات واقعی دوره منتهی به ۱۴۰۲/۰۶/۳۱ '
  row 47: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=46
  row 46 [n=1 text=1 number=0 other=0] merges=A46:E46: A46='دلایل تغییرات اطلاعات واقعی دوره منتهی به ۱۴۰۲/۰۶/۳۱ '
  row 47: <EMPTY>
  row 48 [n=1 text=1 number=0 other=0] merges=A48:E48: A48='دلایل تغییرات اطلاعات واقعی دوره منتهی به ۱۴۰۲/۱۲/۲۹ '
  row 49: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=48
  row 48 [n=1 text=1 number=0 other=0] merges=A48:E48: A48='دلایل تغییرات اطلاعات واقعی دوره منتهی به ۱۴۰۲/۱۲/۲۹ '
  row 49: <EMPTY>
  row 50: <EMPTY>
  row 51: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=53
  row 53 [n=1 text=1 number=0 other=0]: A53='صورت سود و زیان جامع'
  row 54: <EMPTY>
  row 55: <EMPTY>
  row 56: <EMPTY>

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=58
  row 58 [n=1 text=1 number=0 other=0]: A58='صورت سود و زیان جامع'
  row 59 [n=1 text=1 number=0 other=0]: A59='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 60 [n=5 text=5 number=0 other=0] merges=A60:A61,E60:E61: A60='شرح' | B60='دوره منتهي به ۱۴۰۳/۰۶/۳۱' | C60='تجدید ا
رائه شده ۱۴۰۲/۰۶/۳۱' | D60='تجدید ارائه شده ۱۴۰۲/۱۲/۲۹' | E60='درصد تغییر'
  row 61 [n=3 text=3 number=0 other=0] merges=A60:A61,E60:E61: B61='حسابرسی نشده' | C61='حسابرسی شده' | D61='حسابرسی شده
'

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=59
  row 59 [n=1 text=1 number=0 other=0]: A59='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 60 [n=5 text=5 number=0 other=0] merges=A60:A61,E60:E61: A60='شرح' | B60='دوره منتهي به ۱۴۰۳/۰۶/۳۱' | C60='تجدید ا
رائه شده ۱۴۰۲/۰۶/۳۱' | D60='تجدید ارائه شده ۱۴۰۲/۱۲/۲۹' | E60='درصد تغییر'
  row 61 [n=3 text=3 number=0 other=0] merges=A60:A61,E60:E61: B61='حسابرسی نشده' | C61='حسابرسی شده' | D61='حسابرسی شده
'
  row 62 [n=5 text=1 number=4 other=0]: A62='سود(زیان) خالص ' | B62=-25195703 | C62=-35246257 | D62=-9124895 | E62=29

[DIRECT_NEXT_ROW_MIXED] anchor_row=63
  row 63 [n=1 text=1 number=0 other=0]: A63='سایر اقلام سود و زیان جامع: '
  row 64 [n=4 text=1 number=3 other=0]: A64='مازاد تجديد ارزيابي دارايي\u200cها ' | B64=0 | C64=0 | D64=0
  row 65 [n=4 text=1 number=3 other=0]: A65='تفاوت تسعیر ارز عملیات خارجی ' | B65=0 | C65=0 | D65=0
  row 66 [n=4 text=1 number=3 other=0]: A66='مالیات مربوط به سایر اقلام سود و زیان جامع ' | B66=0 | C66=0 | D66=0

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=72
  row 72 [n=1 text=1 number=0 other=0]: A72='صورت وضعیت مالی'
  row 73: <EMPTY>
  row 74: <EMPTY>
  row 75: <EMPTY>

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=77
  row 77 [n=1 text=1 number=0 other=0]: A77='صورت وضعیت مالی'
  row 78 [n=1 text=1 number=0 other=0]: A78='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 79 [n=5 text=5 number=0 other=0] merges=A79:A80,E79:E80: A79='شرح' | B79='دوره منتهي به ۱۴۰۳/۰۶/۳۱' | C79='تجدید ا
رائه شده ۱۴۰۲/۱۲/۲۹' | D79='تجدید ارائه شده ۱۴۰۲/۰۱/۰۱' | E79='درصد تغييرات'
  row 80 [n=3 text=3 number=0 other=0] merges=A79:A80,E79:E80: B80='حسابرسی نشده' | C80='حسابرسی شده' | D80='حسابرسی نشد
ه'

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=78
  row 78 [n=1 text=1 number=0 other=0]: A78='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 79 [n=5 text=5 number=0 other=0] merges=A79:A80,E79:E80: A79='شرح' | B79='دوره منتهي به ۱۴۰۳/۰۶/۳۱' | C79='تجدید ا
رائه شده ۱۴۰۲/۱۲/۲۹' | D79='تجدید ارائه شده ۱۴۰۲/۰۱/۰۱' | E79='درصد تغييرات'
  row 80 [n=3 text=3 number=0 other=0] merges=A79:A80,E79:E80: B80='حسابرسی نشده' | C80='حسابرسی شده' | D80='حسابرسی نشد
ه'
  row 81 [n=1 text=1 number=0 other=0]: A81='دارایی ها '

[DIRECT_NEXT_ROW_MIXED] anchor_row=81
  row 81 [n=1 text=1 number=0 other=0]: A81='دارایی ها '
  row 82 [n=5 text=1 number=4 other=0]: A82='موجودي نقد ' | B82=347110539 | C82=295173082 | D82=229326967 | E82=18
  row 83 [n=5 text=1 number=4 other=0]: A83='مطالبات از بانک ها و ساير موسسات اعتباري ' | B83=686275365 | C83=696743016
| D83=445765962 | E83=-2
  row 84 [n=5 text=1 number=4 other=0]: A84='مطالبات از دولت ' | B84=2920800 | C84=2925324 | D84=3017721 | E84=0

[DIRECT_NEXT_ROW_MIXED] anchor_row=96
  row 96 [n=1 text=1 number=0 other=0]: A96='حقوق مالکانه '
  row 97 [n=5 text=1 number=4 other=0]: A97='سرمايه ' | B97=156340000 | C97=156340000 | D97=156340000 | E97=0
  row 98 [n=4 text=1 number=3 other=0]: A98='افزايش سرمايه در جريان ' | B98=0 | C98=0 | D98=0
  row 99 [n=4 text=1 number=3 other=0]: A99='صرف سهام ' | B99=0 | C99=0 | D99=0

[DIRECT_NEXT_ROW_MIXED] anchor_row=108
  row 108 [n=1 text=1 number=0 other=0]: A108='بدهی\u200cها '
  row 109 [n=5 text=1 number=4 other=0]: A109='بدهي به بانكها و ساير موسسات اعتباري ' | B109=867341907 | C109=772033496
| D109=499855530 | E109=12
  row 110 [n=5 text=1 number=4 other=0]: A110='سپرده\u200cهاي مشتریان ' | B110=3215472710 | C110=3081957372 | D110=24461
03556 | E110=4
  row 111 [n=5 text=1 number=4 other=0]: A111='سود سهام پرداختني ' | B111=324154 | C111=1815045 | D111=1815386 | E111=-8
2

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=123
  row 123 [n=1 text=1 number=0 other=0]: A123='صورت تغییرات در حقوق مالکانه'
  row 124: <EMPTY>
  row 125: <EMPTY>
  row 126: <EMPTY>

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=128
  row 128 [n=1 text=1 number=0 other=0]: A128='صورت تغییرات در حقوق مالکانه'
  row 129 [n=1 text=1 number=0 other=0]: A129='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 130 [n=12 text=12 number=0 other=0]: A130='شرح' | B130='سرمایه' | C130='افزایش سرمایه در جریان' | D130='صرف سهام'
| E130='صرف سهام خزانه' | F130='اندوخته قانونی' | G130='سایر اندوخته\u200cها' | H130='مازاد تجدید ارزیابی دارایی\u200cها
' | I130='تفاوت تسعیر ارز عملیات خارجی' | J130='سود انباشته' | K130='سهام خزانه' | L130='جمع کل'
  row 131 [n=12 text=1 number=11 other=0]: A131='مانده در ۱۴۰۲/۰۱/۰۱ ' | B131=156340000 | C131=0 | D131=0 | E131=0 | F13
1=7393601 | G131=985814 | H131=0 | I131=0 | J131=-20295950 | K131=-23976787 | L131=120446678

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=129
  row 129 [n=1 text=1 number=0 other=0]: A129='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 130 [n=12 text=12 number=0 other=0]: A130='شرح' | B130='سرمایه' | C130='افزایش سرمایه در جریان' | D130='صرف سهام'
| E130='صرف سهام خزانه' | F130='اندوخته قانونی' | G130='سایر اندوخته\u200cها' | H130='مازاد تجدید ارزیابی دارایی\u200cها
' | I130='تفاوت تسعیر ارز عملیات خارجی' | J130='سود انباشته' | K130='سهام خزانه' | L130='جمع کل'
  row 131 [n=12 text=1 number=11 other=0]: A131='مانده در ۱۴۰۲/۰۱/۰۱ ' | B131=156340000 | C131=0 | D131=0 | E131=0 | F13
1=7393601 | G131=985814 | H131=0 | I131=0 | J131=-20295950 | K131=-23976787 | L131=120446678
  row 132 [n=12 text=1 number=11 other=0]: A132='اصلاح اشتباهات ' | B132=0 | C132=0 | D132=0 | E132=0 | F132=0 | G132=0
| H132=0 | I132=0 | J132=-15789842 | K132=0 | L132=-15789842

[DIRECT_NEXT_ROW_MIXED] anchor_row=135
  row 135 [n=1 text=1 number=0 other=0]: A135='تغییرات حقوق مالکانه در سال ۱۴۰۲/۱۲/۲۹ '
  row 136 [n=3 text=1 number=2 other=0]: A136='سود(زيان) خالص گزارش شده در صورت\u200cهاي مالي سال ۱۴۰۲/۱۲/۲۹ ' | J136=-9
124895 | L136=-9124895
  row 137 [n=12 text=1 number=11 other=0]: A137='اصلاح اشتباهات ' | B137=0 | C137=0 | D137=0 | E137=0 | F137=0 | G137=0
| H137=0 | I137=0 | J137=0 | K137=0 | L137=0
  row 138 [n=12 text=1 number=11 other=0]: A138='تغییر در رویه\u200cهای حسابداری ' | B138=0 | C138=0 | D138=0 | E138=0 |
 F138=0 | G138=0 | H138=0 | I138=0 | J138=0 | K138=0 | L138=0

[DIRECT_NEXT_ROW_MIXED] anchor_row=152
  row 152 [n=1 text=1 number=0 other=0]: A152='تغییرات حقوق مالکانه در سال ۱۴۰۳/۰۶/۳۱ '
  row 153 [n=3 text=1 number=2 other=0]: A153='سود خالص ۱۴۰۳/۰۶/۳۱ ' | J153=-25195703 | L153=-25195703
  row 154 [n=4 text=1 number=3 other=0]: A154='سایر اقلام سود و زیان جامع پس از کسر مالیات ' | H154=0 | I154=0 | L154=0
  row 155 [n=12 text=1 number=11 other=0]: A155='سود(زيان) جامع در ۱۴۰۳/۰۶/۳۱ ' | B155=0 | C155=0 | D155=0 | E155=0 | F1
55=0 | G155=0 | H155=0 | I155=0 | J155=-25195703 | K155=0 | L155=-25195703

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=169
  row 169 [n=1 text=1 number=0 other=0]: A169='صورت جریان های نقدی'
  row 170: <EMPTY>
  row 171: <EMPTY>
  row 172: <EMPTY>

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=174
  row 174 [n=1 text=1 number=0 other=0]: A174='صورت جریان های نقدی'
  row 175 [n=1 text=1 number=0 other=0]: A175='کلیه مبالغ به میلیون ریال است'
  row 176 [n=5 text=5 number=0 other=0] merges=A176:A177,E176:E177: A176='شرح' | B176='دوره منتهي به ۱۴۰۳/۰۶/۳۱' | C176=
'تجدید ارائه شده۱۴۰۲/۰۶/۳۱' | D176='تجدید ارائه شده۱۴۰۲/۱۲/۲۹' | E176='درصد تغییر'
  row 177 [n=3 text=3 number=0 other=0] merges=A176:A177,E176:E177: B177='حسابرسی نشده' | C177='حسابرسی شده' | D177='حسا
برسی شده'

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=175
  row 175 [n=1 text=1 number=0 other=0]: A175='کلیه مبالغ به میلیون ریال است'
  row 176 [n=5 text=5 number=0 other=0] merges=A176:A177,E176:E177: A176='شرح' | B176='دوره منتهي به ۱۴۰۳/۰۶/۳۱' | C176=
'تجدید ارائه شده۱۴۰۲/۰۶/۳۱' | D176='تجدید ارائه شده۱۴۰۲/۱۲/۲۹' | E176='درصد تغییر'
  row 177 [n=3 text=3 number=0 other=0] merges=A176:A177,E176:E177: B177='حسابرسی نشده' | C177='حسابرسی شده' | D177='حسا
برسی شده'
  row 178 [n=1 text=1 number=0 other=0]: A178='جریان\xadهای نقدی حاصل از فعاليت\u200cهاي عملياتي: '

[DIRECT_NEXT_ROW_MIXED] anchor_row=178
  row 178 [n=1 text=1 number=0 other=0]: A178='جریان\xadهای نقدی حاصل از فعاليت\u200cهاي عملياتي: '
  row 179 [n=5 text=1 number=4 other=0]: A179='نقد حاصل از عملیات ' | B179=-29363629 | C179=-110187888 | D179=-96174356
| E179=73
  row 180 [n=5 text=2 number=3 other=0]: A180='پرداخت\u200cهای نقدی بابت مالیات بر درآمد ' | B180=-2548000 | C180=0 | D1
80=0 | E180='-Infinity '
  row 181 [n=5 text=1 number=4 other=0]: A181='جريان \u200cخالص \u200cورود\u200c (خروج) \u200cنقد حاصل از فعاليت\u200cها
ي \u200cعمل... | B181=-31911629 | C181=-110187888 | D181=-96174356 | E181=71

[DIRECT_NEXT_ROW_MIXED] anchor_row=182
  row 182 [n=1 text=1 number=0 other=0]: A182='فعاليت\u200cهاي سرمایه\u200cگذاری '
  row 183 [n=5 text=1 number=4 other=0]: A183='وجوه پرداختي بابت تحصیل دارایی\u200cهاي ثابت مشهود ' | B183=-1379698 | C1
83=-5726382 | D183=-7657549 | E183=76
  row 184 [n=5 text=1 number=4 other=0]: A184='وجوه دریافتی بابت فروش دارایی\u200cهاي ثابت مشهود ' | B184=36457 | C184=7
5915 | D184=470555 | E184=-52
  row 185 [n=5 text=1 number=4 other=0]: A185='وجوه پرداختي بابت تحصیل دارایی\u200cهاي نامشهود ' | B185=-293822 | C185=-
328217 | D185=-1183590 | E185=10

[DIRECT_NEXT_ROW_MIXED] anchor_row=191
  row 191 [n=1 text=1 number=0 other=0]: A191='فعاليت\u200cهاي تأمين مالي '
  row 192 [n=4 text=1 number=3 other=0]: A192='دریافت\u200cهای نقدی حاصل از افزايش سرمايه ' | B192=0 | C192=0 | D192=0
  row 193 [n=5 text=1 number=4 other=0]: A193='دریافت\u200cهای نقدی حاصل از صرف سهام ' | B193=0 | C193=424904 | D193=0 |
 E193=-100
  row 194 [n=4 text=1 number=3 other=0]: A194='دریافت\u200cهای نقدی حاصل از فروش سهام خزانه ' | B194=0 | C194=0 | D194=0


[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=221
  row 221 [n=1 text=1 number=0 other=0] merges=A221:E221: A221='دلایل تغییرات اطلاعات واقعی دوره منتهی به ۱۴۰۳/۰۶/۳۱ '
  row 222: <EMPTY>
  row 223 [n=1 text=1 number=0 other=0] merges=A223:E223: A223='دلایل تغییرات اطلاعات واقعی دوره منتهی به ۱۴۰۲/۰۶/۳۱ '
  row 224: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=223
  row 223 [n=1 text=1 number=0 other=0] merges=A223:E223: A223='دلایل تغییرات اطلاعات واقعی دوره منتهی به ۱۴۰۲/۰۶/۳۱ '
  row 224: <EMPTY>
  row 225 [n=1 text=1 number=0 other=0] merges=A225:E225: A225='دلایل تغییرات اطلاعات واقعی دوره منتهی به ۱۴۰۲/۱۲/۲۹ '
  row 226: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=225
  row 225 [n=1 text=1 number=0 other=0] merges=A225:E225: A225='دلایل تغییرات اطلاعات واقعی دوره منتهی به ۱۴۰۲/۱۲/۲۹ '
  row 226: <EMPTY>
  row 227: <EMPTY>
  row 228: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=230
  row 230 [n=1 text=1 number=0 other=0]: A230='خلاصه اطلاعات گزارش تفسیری - صفحه 1'
  row 231: <EMPTY>
  row 232: <EMPTY>
  row 233: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=235
  row 235 [n=1 text=1 number=0 other=0] merges=A235:K235: A235='اطلاعات این فرم گزیده ای از اطلاعات گزارش تفسیری مدیریت
می باشد که هیئت مدیره شرکت م...
  row 236 [n=1 text=1 number=0 other=0]: A236='مانده تسهیلات اعطایی و ذخیره مطالبات مشکوک الوصول:'
  row 237 [n=1 text=1 number=0 other=0]: A237='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 238 [n=11 text=11 number=0 other=0] merges=A238:A239: A238='شرح' | B238='در تاریخ ۱۴۰۲/۱۲/۲۹' | C238='در تاریخ ۱۴۰
۳/۰۶/۳۱' | D238='در تاریخ ۱۴۰۲/۱۲/۲۹' | E238='در تاریخ ۱۴۰۳/۰۶/۳۱' | F238='در تاریخ ۱۴۰۲/۱۲/۲۹' | G238='در تاریخ ۱۴۰۳/۰۶
/۳۱' | H238='در تاریخ ۱۴۰۲/۱۲/۲۹' | I238='در تاریخ ۱۴۰۳/۰۶/۳۱' | J238='در تاریخ ۱۴۰۲/۱۲/۲۹' | K238='در تاریخ ۱۴۰۳/۰۶/۳۱'


[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=236
  row 236 [n=1 text=1 number=0 other=0]: A236='مانده تسهیلات اعطایی و ذخیره مطالبات مشکوک الوصول:'
  row 237 [n=1 text=1 number=0 other=0]: A237='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 238 [n=11 text=11 number=0 other=0] merges=A238:A239: A238='شرح' | B238='در تاریخ ۱۴۰۲/۱۲/۲۹' | C238='در تاریخ ۱۴۰
۳/۰۶/۳۱' | D238='در تاریخ ۱۴۰۲/۱۲/۲۹' | E238='در تاریخ ۱۴۰۳/۰۶/۳۱' | F238='در تاریخ ۱۴۰۲/۱۲/۲۹' | G238='در تاریخ ۱۴۰۳/۰۶
/۳۱' | H238='در تاریخ ۱۴۰۲/۱۲/۲۹' | I238='در تاریخ ۱۴۰۳/۰۶/۳۱' | J238='در تاریخ ۱۴۰۲/۱۲/۲۹' | K238='در تاریخ ۱۴۰۳/۰۶/۳۱'

  row 239 [n=5 text=5 number=0 other=0] merges=A238:A239,B239:C239,D239:E239,F239:G239,H239:I239,J239:K239: B239='جاری'
| D239='سررسید گذشته' | F239='معوق' | H239='مشکوک الوصول' | J239='جمع'

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=237
  row 237 [n=1 text=1 number=0 other=0]: A237='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 238 [n=11 text=11 number=0 other=0] merges=A238:A239: A238='شرح' | B238='در تاریخ ۱۴۰۲/۱۲/۲۹' | C238='در تاریخ ۱۴۰
۳/۰۶/۳۱' | D238='در تاریخ ۱۴۰۲/۱۲/۲۹' | E238='در تاریخ ۱۴۰۳/۰۶/۳۱' | F238='در تاریخ ۱۴۰۲/۱۲/۲۹' | G238='در تاریخ ۱۴۰۳/۰۶
/۳۱' | H238='در تاریخ ۱۴۰۲/۱۲/۲۹' | I238='در تاریخ ۱۴۰۳/۰۶/۳۱' | J238='در تاریخ ۱۴۰۲/۱۲/۲۹' | K238='در تاریخ ۱۴۰۳/۰۶/۳۱'

  row 239 [n=5 text=5 number=0 other=0] merges=A238:A239,B239:C239,D239:E239,F239:G239,H239:I239,J239:K239: B239='جاری'
| D239='سررسید گذشته' | F239='معوق' | H239='مشکوک الوصول' | J239='جمع'
  row 240 [n=11 text=1 number=10 other=0]: A240='تسهیلات اعطایی و مطالبات از اشخاص دولتی ' | B240=943937 | C240=0 | D240
=4080869 | E240=5601562 | F240=0 | G240=0 | H240=0 | I240=0 | J240=5024806 | K240=5601562

[DIRECT_NEXT_ROW_MIXED] anchor_row=244
  row 244 [n=1 text=1 number=0 other=0]: A244='کسر می شود: '
  row 245 [n=11 text=1 number=10 other=0]: A245='سود سالهای آتی ' | B245=161368315 | C245=145007474 | D245=0 | E245=0 |
F245=0 | G245=0 | H245=0 | I245=0 | J245=161368315 | K245=145007474
  row 246 [n=11 text=1 number=10 other=0]: A246='سایر ' | B246=1 | C246=4817501 | D246=0 | E246=0 | F246=0 | G246=0 | H2
46=0 | I246=0 | J246=1 | K246=4817501
  row 247 [n=11 text=1 number=10 other=0]: A247='مانده تسهیلات پایان دوره ' | B247=2157436491 | C247=2218722326 | D247=3
54263923 | E247=324714621 | F247=5158486 | G247=62287061 | H247=321510533 | I247=388659280 | J247=2838369433 | K247=2994
383288

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=255
  row 255 [n=1 text=1 number=0 other=0]: A255='برآورد شرکت از تغییرات در نرخ سود تسهیلات اعطایی :'
  row 256 [n=2 text=2 number=0 other=0] merges=A256:B256,C256:I256: A256='دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ' | C256='با ت
وجه به سیاستهای پولی و بانکی انتظار در تغییر نرخ سود تسهیلات اعطایی در سال آتی پ...
  row 257: <EMPTY>
  row 258 [n=1 text=1 number=0 other=0]: A258='برآورد شرکت از تغییرات در مانده تسهیلات :'

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=258
  row 258 [n=1 text=1 number=0 other=0]: A258='برآورد شرکت از تغییرات در مانده تسهیلات :'
  row 259 [n=2 text=2 number=0 other=0] merges=A259:B259,C259:I259: A259='دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ' | C259='با ت
وجه به رشد منابع بانک در سال آتی پیش بینی می گردد مانده تسهیلات بانک افزایش یابد. '
  row 260: <EMPTY>
  row 261 [n=1 text=1 number=0 other=0]: A261='برآورد شرکت از تغییرات در مانده ذخایر مطالبات مشکوک الوصول :'

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=261
  row 261 [n=1 text=1 number=0 other=0]: A261='برآورد شرکت از تغییرات در مانده ذخایر مطالبات مشکوک الوصول :'
  row 262 [n=2 text=2 number=0 other=0] merges=A262:B262,C262:I262: A262='دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ' | C262='با ت
وجه به افزایش در حجم تسهیلات اعطایی پیش بینی می گردد مانده ذخیره مطالبات مشکوک ا...
  row 263: <EMPTY>
  row 264 [n=1 text=1 number=0 other=0]: A264='مانده سپرده های دریافتی از مشتریان :'

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=264
  row 264 [n=1 text=1 number=0 other=0]: A264='مانده سپرده های دریافتی از مشتریان :'
  row 265 [n=1 text=1 number=0 other=0]: A265='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 266 [n=4 text=4 number=0 other=0] merges=A266:A267,B266:C266,D266:E266,F266:F267: A266='شرح' | B266='مانده سپرده ه
ا' | D266='متوسط نرخ سود مانده سپرده ها' | F266='برآورد مدیریت از تغییر در نرخ سود سپرده ها و تغییر در مانده سپرده های د
ریافتی از مشت...
  row 267 [n=4 text=4 number=0 other=0] merges=A266:A267,F266:F267: B267='در تاریخ ۱۴۰۲/۱۲/۲۹' | C267='در تاریخ ۱۴۰۳/۰۶/
۳۱' | D267='در تاریخ ۱۴۰۲/۱۲/۲۹' | E267='در تاریخ ۱۴۰۳/۰۶/۳۱'

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=265
  row 265 [n=1 text=1 number=0 other=0]: A265='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 266 [n=4 text=4 number=0 other=0] merges=A266:A267,B266:C266,D266:E266,F266:F267: A266='شرح' | B266='مانده سپرده ه
ا' | D266='متوسط نرخ سود مانده سپرده ها' | F266='برآورد مدیریت از تغییر در نرخ سود سپرده ها و تغییر در مانده سپرده های د
ریافتی از مشت...
  row 267 [n=4 text=4 number=0 other=0] merges=A266:A267,F266:F267: B267='در تاریخ ۱۴۰۲/۱۲/۲۹' | C267='در تاریخ ۱۴۰۳/۰۶/
۳۱' | D267='در تاریخ ۱۴۰۲/۱۲/۲۹' | E267='در تاریخ ۱۴۰۳/۰۶/۳۱'
  row 268 [n=1 text=1 number=0 other=0]: A268='سپرده های ریالی: '

[DIRECT_NEXT_ROW_MIXED] anchor_row=268
  row 268 [n=1 text=1 number=0 other=0]: A268='سپرده های ریالی: '
  row 269 [n=6 text=2 number=4 other=0]: A269='سپرده های کوتاه مدت ' | B269=449329293 | C269=470781277 | D269=0 | E269=0
 | F269='با توجه به سیاستهای پولی و بانکی تغییری درنرخ سود سپرده ها پیش بینی نمی گردد. '
  row 270 [n=6 text=2 number=4 other=0]: A270='سپرده های کوتاه مدت ویژه ' | B270=145711 | C270=453951 | D270=0 | E270=0
| F270='با توجه به سیاستهای پولی و بانکی تغییری درنرخ سود سپرده ها پیش بینی نمی گردد. '
  row 271 [n=6 text=2 number=4 other=0]: A271='سپرده های بلند مدت ' | B271=1634208566 | C271=1678516940 | D271=0 | E271=
0 | F271='با توجه به سیاستهای پولی و بانکی تغییری درنرخ سود سپرده ها پیش بینی نمی گردد. '

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=277
  row 277 [n=1 text=1 number=0 other=0]: A277='اقلام زیر خط:'
  row 278 [n=1 text=1 number=0 other=0]: A278='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 279 [n=6 text=6 number=0 other=0]: A279='شرح' | B279='۱۴۰۳/۰۶/۳۱' | C279='۱۴۰۲/۱۲/۲۹' | D279='شرح' | E279='۱۴۰۳/۰۶
/۳۱' | F279='۱۴۰۲/۱۲/۲۹'
  row 280 [n=6 text=2 number=4 other=0]: A280='تعهدات مشتریان بابت اعتبارات اسنادی ' | B280=439498515 | C280=425497756 |
 D280='تعهدات بانک بابت اعتبارات اسنادی ' | E280=439498515 | F280=425497756

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=278
  row 278 [n=1 text=1 number=0 other=0]: A278='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 279 [n=6 text=6 number=0 other=0]: A279='شرح' | B279='۱۴۰۳/۰۶/۳۱' | C279='۱۴۰۲/۱۲/۲۹' | D279='شرح' | E279='۱۴۰۳/۰۶
/۳۱' | F279='۱۴۰۲/۱۲/۲۹'
  row 280 [n=6 text=2 number=4 other=0]: A280='تعهدات مشتریان بابت اعتبارات اسنادی ' | B280=439498515 | C280=425497756 |
 D280='تعهدات بانک بابت اعتبارات اسنادی ' | E280=439498515 | F280=425497756
  row 281 [n=6 text=2 number=4 other=0]: A281='تعهدات مشتریان بابت ضمانت نامه های صادره ' | B281=705682218 | C281=620594
993 | D281='تعهدات بانک بابت ضمانت نامه های صادره ' | E281=705682218 | F281=620594993

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=284
  row 284 [n=1 text=1 number=0 other=0] merges=B284:F284: A284='توضیحات در خصوص تغییرات بااهمیت: '
  row 285 [n=1 text=1 number=0 other=0] merges=A285:I285: A285='«جملات آینده\u200cنگر نشان\u200cدهنده انتظارات، باورها ی
ا پیش\u200cبینی\u200cهای جار...
  row 286: <EMPTY>
  row 287: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=285
  row 285 [n=1 text=1 number=0 other=0] merges=A285:I285: A285='«جملات آینده\u200cنگر نشان\u200cدهنده انتظارات، باورها ی
ا پیش\u200cبینی\u200cهای جار...
  row 286: <EMPTY>
  row 287: <EMPTY>
  row 288: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=289
  row 289 [n=1 text=1 number=0 other=0]: A289='خلاصه اطلاعات گزارش تفسیری - صفحه 2'
  row 290: <EMPTY>
  row 291: <EMPTY>
  row 292: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=294
  row 294 [n=1 text=1 number=0 other=0] merges=A294:K294: A294='اطلاعات این فرم گزیده ای از اطلاعات گزارش تفسیری مدیریت
می باشد که هیئت مدیره شرکت م...
  row 295 [n=1 text=1 number=0 other=0]: A295='وضعیت کارکنان:'
  row 296 [n=1 text=1 number=0 other=0]: A296='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 297 [n=4 text=4 number=0 other=0]: A297='شرح' | B297='در تاریخ ۱۴۰۲/۱۲/۲۹' | C297='در تاریخ ۱۴۰۳/۰۶/۳۱' | D297='بر
آورد در تاریخ ۱۴۰۳/۱۲/۳۰'

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=295
  row 295 [n=1 text=1 number=0 other=0]: A295='وضعیت کارکنان:'
  row 296 [n=1 text=1 number=0 other=0]: A296='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 297 [n=4 text=4 number=0 other=0]: A297='شرح' | B297='در تاریخ ۱۴۰۲/۱۲/۲۹' | C297='در تاریخ ۱۴۰۳/۰۶/۳۱' | D297='بر
آورد در تاریخ ۱۴۰۳/۱۲/۳۰'
  row 298 [n=4 text=1 number=3 other=0]: A298='تعداد شعب ' | B298=351 | C298=351 | D298=351

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=296
  row 296 [n=1 text=1 number=0 other=0]: A296='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 297 [n=4 text=4 number=0 other=0]: A297='شرح' | B297='در تاریخ ۱۴۰۲/۱۲/۲۹' | C297='در تاریخ ۱۴۰۳/۰۶/۳۱' | D297='بر
آورد در تاریخ ۱۴۰۳/۱۲/۳۰'
  row 298 [n=4 text=1 number=3 other=0]: A298='تعداد شعب ' | B298=351 | C298=351 | D298=351
  row 299 [n=4 text=1 number=3 other=0]: A299='تعداد کارکنان ' | B299=4769 | C299=4707 | D299=4707

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=300
  row 300 [n=1 text=1 number=0 other=0]: A300='اطلاعات حق الوکاله و کفایت سرمایه'
  row 301 [n=1 text=1 number=0 other=0]: A301='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 302 [n=4 text=4 number=0 other=0] merges=D302:E302: A302='شرح' | B302='سال مالی منتهی به۱۴۰۲/۱۲/۲۹' | C302='دوره ۶
 ماهه منتهی به ۱۴۰۳/۰۶/۳۱' | D302='برآورد تغییر روند در دوره ۶ ماهه منتهی به ۱۴۰۳/۱۲/۳۰'
  row 303 [n=4 text=2 number=2 other=0] merges=D303:E303: A303='سهم بانک از درآمدهای مشاع ' | B303=0 | C303=0 | D303='--
----------------------------------------------------------- '

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=301
  row 301 [n=1 text=1 number=0 other=0]: A301='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 302 [n=4 text=4 number=0 other=0] merges=D302:E302: A302='شرح' | B302='سال مالی منتهی به۱۴۰۲/۱۲/۲۹' | C302='دوره ۶
 ماهه منتهی به ۱۴۰۳/۰۶/۳۱' | D302='برآورد تغییر روند در دوره ۶ ماهه منتهی به ۱۴۰۳/۱۲/۳۰'
  row 303 [n=4 text=2 number=2 other=0] merges=D303:E303: A303='سهم بانک از درآمدهای مشاع ' | B303=0 | C303=0 | D303='--
----------------------------------------------------------- '
  row 304 [n=4 text=2 number=2 other=0] merges=D304:E304: A304='سهم سپرده گذاران از درآمدهای مشاع ' | B304=194221502 | C
304=112241232 | D304='------------------------------------------------------------- '

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=309
  row 309 [n=1 text=1 number=0 other=0]: A309='اهداف و راهبردهای آتی مدیریت در خصوص فعالیت شرکت:'
  row 310 [n=2 text=2 number=0 other=0] merges=B310:G310: A310='اهداف و راهبردهای آتی مدیریت در خصوص فعالیت شرکت: ' | B3
10='-------------------------------------------------------------------- '
  row 311 [n=1 text=1 number=0 other=0]: A311='درآمد حاصل از تسهيلات اعطايي و سپرده گذاري'
  row 312 [n=1 text=1 number=0 other=0]: A312='کلیه مبالغ درج شده به میلیون ریال می باشد'

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=311
  row 311 [n=1 text=1 number=0 other=0]: A311='درآمد حاصل از تسهيلات اعطايي و سپرده گذاري'
  row 312 [n=1 text=1 number=0 other=0]: A312='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 313 [n=6 text=6 number=0 other=0] merges=F313:G313: A313='شرح' | B313='سال مالی منتهی به ۱۴۰۲/۱۲/۲۹' | C313='متوسط
 نرخ سود سال مالی منتهی به ۱۴۰۲/۱۲/۲۹ (درصد)' | D313='دوره ۶ ماهه منتهی به ۱۴۰۳/۰۶/۳۱' | E313='متوسط نرخ سود دوره ۶ ماهه
 منتهی به ۱۴۰۳/۰۶/۳۱ (درصد)' | F313='برآورد تغییر روند در دوره ۶ ماهه منتهی به ۱۴۰۳/۱۲/۳۰'
  row 314 [n=1 text=1 number=0 other=0] merges=F314:G314: A314='درآمد تسهیلات اعطایی: '

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=312
  row 312 [n=1 text=1 number=0 other=0]: A312='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 313 [n=6 text=6 number=0 other=0] merges=F313:G313: A313='شرح' | B313='سال مالی منتهی به ۱۴۰۲/۱۲/۲۹' | C313='متوسط
 نرخ سود سال مالی منتهی به ۱۴۰۲/۱۲/۲۹ (درصد)' | D313='دوره ۶ ماهه منتهی به ۱۴۰۳/۰۶/۳۱' | E313='متوسط نرخ سود دوره ۶ ماهه
 منتهی به ۱۴۰۳/۰۶/۳۱ (درصد)' | F313='برآورد تغییر روند در دوره ۶ ماهه منتهی به ۱۴۰۳/۱۲/۳۰'
  row 314 [n=1 text=1 number=0 other=0] merges=F314:G314: A314='درآمد تسهیلات اعطایی: '
  row 315 [n=6 text=2 number=4 other=0] merges=F315:G315: A315='فروش اقساطی ' | B315=3892061 | C315=0 | D315=2134924 | E
315=0 | F315='مبلغ درآمدسرمایه گذاریهای بانک درسال۱۴۰۳باافزایش مواجه گردد '

[DIRECT_NEXT_ROW_MIXED] anchor_row=314
  row 314 [n=1 text=1 number=0 other=0] merges=F314:G314: A314='درآمد تسهیلات اعطایی: '
  row 315 [n=6 text=2 number=4 other=0] merges=F315:G315: A315='فروش اقساطی ' | B315=3892061 | C315=0 | D315=2134924 | E
315=0 | F315='مبلغ درآمدسرمایه گذاریهای بانک درسال۱۴۰۳باافزایش مواجه گردد '
  row 316 [n=6 text=2 number=4 other=0] merges=F316:G316: A316='جعاله ' | B316=1753389 | C316=0 | D316=613663 | E316=0 |
 F316='مبلغ درآمدسرمایه گذاریهای بانک درسال۱۴۰۳باافزایش مواجه گردد '
  row 317 [n=6 text=2 number=4 other=0] merges=F317:G317: A317='اجاره به شرط تملیک ' | B317=0 | C317=0 | D317=0 | E317=0
 | F317='مبلغ درآمدسرمایه گذاریهای بانک درسال۱۴۰۳باافزایش مواجه گردد '

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=334
  row 334 [n=1 text=1 number=0 other=0]: A334='خالص سود (زیان) سرمایه گذاری\u200c ها'
  row 335 [n=1 text=1 number=0 other=0]: A335='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 336 [n=4 text=4 number=0 other=0] merges=D336:E336: A336='شرح' | B336='سال مالی منتهی به۱۴۰۲/۱۲/۲۹' | C336='دوره ۶
 ماهه منتهی به ۱۴۰۳/۰۶/۳۱' | D336='برآورد تغییر روند در دوره ۶ ماهه منتهی به ۱۴۰۳/۱۲/۳۰'
  row 337 [n=4 text=2 number=2 other=0] merges=D337:E337: A337='درآمد حاصل از سرمایه گذاری در سهام ' | B337=2453194 | C3
37=402420 | D337='مبلغ درآمدسرمایه گذاریهای بانک درسال ۱۴۰۳ باافزایش مواجه گردد '

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=335
  row 335 [n=1 text=1 number=0 other=0]: A335='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 336 [n=4 text=4 number=0 other=0] merges=D336:E336: A336='شرح' | B336='سال مالی منتهی به۱۴۰۲/۱۲/۲۹' | C336='دوره ۶
 ماهه منتهی به ۱۴۰۳/۰۶/۳۱' | D336='برآورد تغییر روند در دوره ۶ ماهه منتهی به ۱۴۰۳/۱۲/۳۰'
  row 337 [n=4 text=2 number=2 other=0] merges=D337:E337: A337='درآمد حاصل از سرمایه گذاری در سهام ' | B337=2453194 | C3
37=402420 | D337='مبلغ درآمدسرمایه گذاریهای بانک درسال ۱۴۰۳ باافزایش مواجه گردد '
  row 338 [n=4 text=2 number=2 other=0] merges=D338:E338: A338='سود(زیان) حاصل از فروش سرمایه گذاری ' | B338=0 | C338=0
| D338='مبلغ درآمدسرمایه گذاریهای بانک درسال ۱۴۰۳ باافزایش مواجه گردد '

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=341
  row 341 [n=1 text=1 number=0 other=0] merges=A341:G341: A341='«جملات آینده\u200cنگر نشان\u200cدهنده انتظارات، باورها ی
ا پیش\u200cبینی\u200cهای جار...
  row 342: <EMPTY>
  row 343: <EMPTY>
  row 344: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=345
  row 345 [n=1 text=1 number=0 other=0]: A345='خلاصه اطلاعات گزارش تفسیری - صفحه 3'
  row 346: <EMPTY>
  row 347: <EMPTY>
  row 348: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=350
  row 350 [n=1 text=1 number=0 other=0] merges=A350:K350: A350='اطلاعات اين فرم گزيده اي از اطلاعات گزارش تفسيري مديريت
مي باشد که هيئت مديره شرکت م...
  row 351 [n=1 text=1 number=0 other=0]: A351='وضعیت شرکتهای سرمایه پذیر:'
  row 352 [n=1 text=1 number=0 other=0]: A352='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 353 [n=4 text=4 number=0 other=0] merges=A353:B354,C353:F353,G353:I353,J353:K354: A353='نام شرکت' | C353='سال مالي
 منتهي به ۱۴۰۲/۱۲/۲۹' | G353='دوره ۶ ماهه منتهي به ۱۴۰۳/۰۶/۳۱' | J353='تشريح آخرين وضعيت و برنامه هاي آتي شرکت در شرکت س
رمايه پذير'

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=351
  row 351 [n=1 text=1 number=0 other=0]: A351='وضعیت شرکتهای سرمایه پذیر:'
  row 352 [n=1 text=1 number=0 other=0]: A352='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 353 [n=4 text=4 number=0 other=0] merges=A353:B354,C353:F353,G353:I353,J353:K354: A353='نام شرکت' | C353='سال مالي
 منتهي به ۱۴۰۲/۱۲/۲۹' | G353='دوره ۶ ماهه منتهي به ۱۴۰۳/۰۶/۳۱' | J353='تشريح آخرين وضعيت و برنامه هاي آتي شرکت در شرکت س
رمايه پذير'
  row 354 [n=7 text=7 number=0 other=0] merges=A353:B354,J353:K354: C354='درصد مالکيت' | D354='بهاي تمام شده' | E354='سا
ل مالي شرکت سرمايه پذير' | F354='درآمد سرمايه گذاري' | G354='درصد مالکيت' | H354='بهاي تمام شده' | I354='درآمد سرمايه گذ
اري'

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=352
  row 352 [n=1 text=1 number=0 other=0]: A352='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 353 [n=4 text=4 number=0 other=0] merges=A353:B354,C353:F353,G353:I353,J353:K354: A353='نام شرکت' | C353='سال مالي
 منتهي به ۱۴۰۲/۱۲/۲۹' | G353='دوره ۶ ماهه منتهي به ۱۴۰۳/۰۶/۳۱' | J353='تشريح آخرين وضعيت و برنامه هاي آتي شرکت در شرکت س
رمايه پذير'
  row 354 [n=7 text=7 number=0 other=0] merges=A353:B354,J353:K354: C354='درصد مالکيت' | D354='بهاي تمام شده' | E354='سا
ل مالي شرکت سرمايه پذير' | F354='درآمد سرمايه گذاري' | G354='درصد مالکيت' | H354='بهاي تمام شده' | I354='درآمد سرمايه گذ
اري'
  row 355 [n=9 text=3 number=6 other=0] merges=A355:B355,J355:K355: A355='صرافي پارسيان ' | C355=79 | D355=1191004 | E35
5='۱۴۰۲/۱۰/۳۰ ' | F355=237598 | G355=79 | H355=1191004 | I355=0 | J355='سود نقدی سرمایه گذاری ها تا پایان سال جاری نسبت
به سال ۱۴۰۳ افزایش می یابد '

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=359
  row 359 [n=1 text=1 number=0 other=0]: A359='ساير درآمدها و هزینه های عملياتي:'
  row 360 [n=1 text=1 number=0 other=0]: A360='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 361 [n=3 text=3 number=0 other=0]: A361='شرح' | B361='۱۴۰۲/۱۲/۲۹' | C361='۱۴۰۳/۰۶/۳۱'
  row 362 [n=1 text=1 number=0 other=0]: A362='ساير درآمدهاي عملياتي: '

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=360
  row 360 [n=1 text=1 number=0 other=0]: A360='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 361 [n=3 text=3 number=0 other=0]: A361='شرح' | B361='۱۴۰۲/۱۲/۲۹' | C361='۱۴۰۳/۰۶/۳۱'
  row 362 [n=1 text=1 number=0 other=0]: A362='ساير درآمدهاي عملياتي: '
  row 363 [n=3 text=1 number=2 other=0]: A363='ساير درآمدهاي عملياتي ' | B363=151543669 | C363=84513662

[DIRECT_NEXT_ROW_MIXED] anchor_row=362
  row 362 [n=1 text=1 number=0 other=0]: A362='ساير درآمدهاي عملياتي: '
  row 363 [n=3 text=1 number=2 other=0]: A363='ساير درآمدهاي عملياتي ' | B363=151543669 | C363=84513662
  row 364: <EMPTY>
  row 365 [n=3 text=1 number=2 other=0]: A365='جمع ساير درآمدهاي عملياتي ' | B365=151543669 | C365=84513662

[DIRECT_NEXT_ROW_MIXED] anchor_row=366
  row 366 [n=1 text=1 number=0 other=0]: A366='ساير هزينه هاي عملياتي: '
  row 367 [n=3 text=1 number=2 other=0]: A367='ساير هزينه هاي عملياتي ' | B367=0 | C367=0
  row 368: <EMPTY>
  row 369 [n=3 text=1 number=2 other=0]: A369='جمع ساير هزينه هاي عملياتي ' | B369=0 | C369=0

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=371
  row 371 [n=1 text=1 number=0 other=0]: A371='برآورد شرکت از تغییرات خالص سایر درآمدها (هزینه ها)ی عملیاتی:'
  row 372 [n=2 text=2 number=0 other=0] merges=A372:B372,C372:F372: A372='دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ' | C372='----
----------------------------------------------------------------------- '
  row 373: <EMPTY>
  row 374 [n=1 text=1 number=0 other=0]: A374='خالص ساير درآمدها و هزینه ها:'

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=374
  row 374 [n=1 text=1 number=0 other=0]: A374='خالص ساير درآمدها و هزینه ها:'
  row 375 [n=1 text=1 number=0 other=0]: A375='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 376 [n=3 text=3 number=0 other=0]: A376='خالص ساير درآمدها و هزينه ها' | B376='۱۴۰۲/۱۲/۲۹' | C376='۱۴۰۳/۰۶/۳۱'
  row 377 [n=3 text=1 number=2 other=0]: A377='ساير درامدها ' | B377=43015355 | C377=2192360

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=375
  row 375 [n=1 text=1 number=0 other=0]: A375='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 376 [n=3 text=3 number=0 other=0]: A376='خالص ساير درآمدها و هزينه ها' | B376='۱۴۰۲/۱۲/۲۹' | C376='۱۴۰۳/۰۶/۳۱'
  row 377 [n=3 text=1 number=2 other=0]: A377='ساير درامدها ' | B377=43015355 | C377=2192360
  row 378 [n=3 text=1 number=2 other=0]: A378='ساير هزينه ها ' | B378=0 | C378=0

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=381
  row 381 [n=1 text=1 number=0 other=0]: A381='برآورد شرکت از تغییرات خالص ساير درآمدها و هزینه ها :'
  row 382 [n=2 text=2 number=0 other=0] merges=A382:B382,C382:F382: A382='دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ' | C382='----
---------------------------------------------------------------------------- '
  row 383: <EMPTY>
  row 384 [n=1 text=1 number=0 other=0]: A384='هزینه های اداری و عمومی:'

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=384
  row 384 [n=1 text=1 number=0 other=0]: A384='هزینه های اداری و عمومی:'
  row 385 [n=1 text=1 number=0 other=0]: A385='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 386 [n=3 text=3 number=0 other=0]: A386='هزينه هاي اداري و عمومي' | B386='۱۴۰۲/۱۲/۲۹' | C386='۱۴۰۳/۰۶/۳۱'
  row 387 [n=3 text=1 number=2 other=0]: A387='هزينه هاي اداري و عمومي ' | B387=-52654898 | C387=-28908689

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=385
  row 385 [n=1 text=1 number=0 other=0]: A385='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 386 [n=3 text=3 number=0 other=0]: A386='هزينه هاي اداري و عمومي' | B386='۱۴۰۲/۱۲/۲۹' | C386='۱۴۰۳/۰۶/۳۱'
  row 387 [n=3 text=1 number=2 other=0]: A387='هزينه هاي اداري و عمومي ' | B387=-52654898 | C387=-28908689
  row 388: <EMPTY>

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=390
  row 390 [n=1 text=1 number=0 other=0]: A390='برآورد شرکت از تغییرات هزینه های اداری و عمومی :'
  row 391 [n=2 text=2 number=0 other=0] merges=A391:B391,C391:F391: A391='دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ' | C391='----
---------------------------------------------------------------------------- '
  row 392: <EMPTY>
  row 393 [n=1 text=1 number=0 other=0]: A393='هزینه مالی:'

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=393
  row 393 [n=1 text=1 number=0 other=0]: A393='هزینه مالی:'
  row 394 [n=1 text=1 number=0 other=0]: A394='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 395 [n=3 text=3 number=0 other=0]: A395='هزينه\u200cهاي مالي' | B395='۱۴۰۲/۱۲/۲۹' | C395='۱۴۰۳/۰۶/۳۱'
  row 396 [n=3 text=1 number=2 other=0]: A396='هزينه مالي تسهيلات دريافتي از ساير بانکها و موسسات اعتباري ' | B396=0 | C
396=0

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=394
  row 394 [n=1 text=1 number=0 other=0]: A394='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 395 [n=3 text=3 number=0 other=0]: A395='هزينه\u200cهاي مالي' | B395='۱۴۰۲/۱۲/۲۹' | C395='۱۴۰۳/۰۶/۳۱'
  row 396 [n=3 text=1 number=2 other=0]: A396='هزينه مالي تسهيلات دريافتي از ساير بانکها و موسسات اعتباري ' | B396=0 | C
396=0
  row 397 [n=3 text=1 number=2 other=0]: A397='جريمه اضافه برداشت از بانک مرکزي ' | B397=0 | C397=0

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=400
  row 400 [n=1 text=1 number=0 other=0]: A400='برآورد شرکت از تغییرات هزینه های مالی :'
  row 401 [n=2 text=2 number=0 other=0] merges=A401:B401,C401:F401: A401='دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ' | C401='----
--------------------------------------------------------------------------------...
  row 402: <EMPTY>
  row 403 [n=1 text=1 number=0 other=0]: A403='برنامه شرکت در خصوص تقسیم سود'

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=403
  row 403 [n=1 text=1 number=0 other=0]: A403='برنامه شرکت در خصوص تقسیم سود'
  row 404 [n=5 text=5 number=0 other=0]: A404='مبلغ سود (زيان) انباشته پايان سال مالي گذشته' | B404='سود سهام پيشنهادي ه
يئت مديره در سال مالي گذشته' | C404='مبلغ سود (زيان) خالص سال مالي گذشته' | D404='سود سهام مصوب مجمع سال مالي گذشته' | E
404='پيشنهاد هيئت مديره درخصوص درصد تقسيم سود سال مالي جاري'
  row 405 [n=5 text=0 number=5 other=0]: A405=-44764295 | B405=0 | C405=-9124895 | D405=0 | E405=0
  row 406 [n=1 text=1 number=0 other=0]: A406='سایر برنامه های با اهمیت شرکت'

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=406
  row 406 [n=1 text=1 number=0 other=0]: A406='سایر برنامه های با اهمیت شرکت'
  row 407 [n=2 text=2 number=0 other=0] merges=B407:E407: A407='دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ' | B407='--------------
------------------------------------------------------ '
  row 408: <EMPTY>
  row 409 [n=1 text=1 number=0 other=0]: A409='سایر توضیحات با اهمیت'

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=409
  row 409 [n=1 text=1 number=0 other=0]: A409='سایر توضیحات با اهمیت'
  row 410 [n=1 text=1 number=0 other=0] merges=A410:I410: A410='--------------------------------------------------------
----------------------------...
  row 411 [n=1 text=1 number=0 other=0] merges=A411:I411: A411='«جملات آينده\u200cنگر نشان\u200cدهنده انتظارات، باورها ي
ا پيش\u200cبيني\u200cهاي جار...
  row 412: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=410
  row 410 [n=1 text=1 number=0 other=0] merges=A410:I410: A410='--------------------------------------------------------
----------------------------...
  row 411 [n=1 text=1 number=0 other=0] merges=A411:I411: A411='«جملات آينده\u200cنگر نشان\u200cدهنده انتظارات، باورها ي
ا پيش\u200cبيني\u200cهاي جار...
  row 412: <EMPTY>
  row 413: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=411
  row 411 [n=1 text=1 number=0 other=0] merges=A411:I411: A411='«جملات آينده\u200cنگر نشان\u200cدهنده انتظارات، باورها ي
ا پيش\u200cبيني\u200cهاي جار...
  row 412: <EMPTY>
  row 413: <EMPTY>
  row 414: <EMPTY>

### SHEET 2 Sheet1 | used=A1:E24 | populated_rows=23 | single_text_rows=15

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=1
  row 1 [n=1 text=1 number=0 other=0]: A1='عملیات در حال تداوم: '
  row 2 [n=1 text=1 number=0 other=0]: A2='عملیات متوقف شده: '
  row 3 [n=1 text=1 number=0 other=0]: A3='سود (زیان)پایه هر سهم (ريال) '
  row 4 [n=1 text=1 number=0 other=0]: A4='سایر اقلام سود و زیان جامع: '

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=2
  row 2 [n=1 text=1 number=0 other=0]: A2='عملیات متوقف شده: '
  row 3 [n=1 text=1 number=0 other=0]: A3='سود (زیان)پایه هر سهم (ريال) '
  row 4 [n=1 text=1 number=0 other=0]: A4='سایر اقلام سود و زیان جامع: '
  row 5 [n=1 text=1 number=0 other=0]: A5='دارایی ها '

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=3
  row 3 [n=1 text=1 number=0 other=0]: A3='سود (زیان)پایه هر سهم (ريال) '
  row 4 [n=1 text=1 number=0 other=0]: A4='سایر اقلام سود و زیان جامع: '
  row 5 [n=1 text=1 number=0 other=0]: A5='دارایی ها '
  row 6 [n=1 text=1 number=0 other=0]: A6='حقوق مالکانه '

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=4
  row 4 [n=1 text=1 number=0 other=0]: A4='سایر اقلام سود و زیان جامع: '
  row 5 [n=1 text=1 number=0 other=0]: A5='دارایی ها '
  row 6 [n=1 text=1 number=0 other=0]: A6='حقوق مالکانه '
  row 7 [n=1 text=1 number=0 other=0]: A7='بدهی\u200cها '

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=5
  row 5 [n=1 text=1 number=0 other=0]: A5='دارایی ها '
  row 6 [n=1 text=1 number=0 other=0]: A6='حقوق مالکانه '
  row 7 [n=1 text=1 number=0 other=0]: A7='بدهی\u200cها '
  row 8 [n=1 text=1 number=0 other=0]: A8='جریان\xadهای نقدی حاصل از فعاليت\u200cهاي عملياتي: '

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=6
  row 6 [n=1 text=1 number=0 other=0]: A6='حقوق مالکانه '
  row 7 [n=1 text=1 number=0 other=0]: A7='بدهی\u200cها '
  row 8 [n=1 text=1 number=0 other=0]: A8='جریان\xadهای نقدی حاصل از فعاليت\u200cهاي عملياتي: '
  row 9 [n=1 text=1 number=0 other=0]: A9='فعاليت\u200cهاي سرمایه\u200cگذاری '

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=7
  row 7 [n=1 text=1 number=0 other=0]: A7='بدهی\u200cها '
  row 8 [n=1 text=1 number=0 other=0]: A8='جریان\xadهای نقدی حاصل از فعاليت\u200cهاي عملياتي: '
  row 9 [n=1 text=1 number=0 other=0]: A9='فعاليت\u200cهاي سرمایه\u200cگذاری '
  row 10 [n=1 text=1 number=0 other=0]: A10='فعاليت\u200cهاي تأمين مالي '

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=8
  row 8 [n=1 text=1 number=0 other=0]: A8='جریان\xadهای نقدی حاصل از فعاليت\u200cهاي عملياتي: '
  row 9 [n=1 text=1 number=0 other=0]: A9='فعاليت\u200cهاي سرمایه\u200cگذاری '
  row 10 [n=1 text=1 number=0 other=0]: A10='فعاليت\u200cهاي تأمين مالي '
  row 11 [n=1 text=1 number=0 other=0]: A11='سپرده های ریالی: '

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=9
  row 9 [n=1 text=1 number=0 other=0]: A9='فعاليت\u200cهاي سرمایه\u200cگذاری '
  row 10 [n=1 text=1 number=0 other=0]: A10='فعاليت\u200cهاي تأمين مالي '
  row 11 [n=1 text=1 number=0 other=0]: A11='سپرده های ریالی: '
  row 12 [n=1 text=1 number=0 other=0]: A12='درآمد تسهیلات اعطایی: '

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=10
  row 10 [n=1 text=1 number=0 other=0]: A10='فعاليت\u200cهاي تأمين مالي '
  row 11 [n=1 text=1 number=0 other=0]: A11='سپرده های ریالی: '
  row 12 [n=1 text=1 number=0 other=0]: A12='درآمد تسهیلات اعطایی: '
  row 13: <EMPTY>

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=11
  row 11 [n=1 text=1 number=0 other=0]: A11='سپرده های ریالی: '
  row 12 [n=1 text=1 number=0 other=0]: A12='درآمد تسهیلات اعطایی: '
  row 13: <EMPTY>
  row 14 [n=1 text=1 number=0 other=0]: A14='صورت سود و زیان جامع'

[NO_MATCH_IN_NEXT_2_PHYSICAL_ROWS] anchor_row=12
  row 12 [n=1 text=1 number=0 other=0]: A12='درآمد تسهیلات اعطایی: '
  row 13: <EMPTY>
  row 14 [n=1 text=1 number=0 other=0]: A14='صورت سود و زیان جامع'
  row 15 [n=1 text=1 number=0 other=0]: A15='کلیه مبالغ درج شده به میلیون ریال می باشد'

[NEXT_ROW_SINGLE_TEXT_NOTE_THEN_ALL_TEXT] anchor_row=14
  row 14 [n=1 text=1 number=0 other=0]: A14='صورت سود و زیان جامع'
  row 15 [n=1 text=1 number=0 other=0]: A15='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 16 [n=5 text=5 number=0 other=0] merges=A16:A17,E16:E17: A16='شرح' | B16='دوره منتهي به ۱۴۰۳/۰۶/۳۱' | C16='تجدید ا
رائه شده ۱۴۰۲/۰۶/۳۱' | D16='تجدید ارائه شده ۱۴۰۲/۱۲/۲۹' | E16='درصد تغییر'
  row 17 [n=3 text=3 number=0 other=0] merges=A16:A17,E16:E17: B17='حسابرسی نشده' | C17='حسابرسی شده' | D17='حسابرسی شده
'

[DIRECT_NEXT_ROW_ALL_TEXT] anchor_row=15
  row 15 [n=1 text=1 number=0 other=0]: A15='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 16 [n=5 text=5 number=0 other=0] merges=A16:A17,E16:E17: A16='شرح' | B16='دوره منتهي به ۱۴۰۳/۰۶/۳۱' | C16='تجدید ا
رائه شده ۱۴۰۲/۰۶/۳۱' | D16='تجدید ارائه شده ۱۴۰۲/۱۲/۲۹' | E16='درصد تغییر'
  row 17 [n=3 text=3 number=0 other=0] merges=A16:A17,E16:E17: B17='حسابرسی نشده' | C17='حسابرسی شده' | D17='حسابرسی شده
'
  row 18 [n=5 text=1 number=4 other=0]: A18='سود(زیان) خالص ' | B18=-25195703 | C18=-35246257 | D18=-9124895 | E18=29

[DIRECT_NEXT_ROW_MIXED] anchor_row=19
  row 19 [n=1 text=1 number=0 other=0]: A19='سایر اقلام سود و زیان جامع: '
  row 20 [n=4 text=1 number=3 other=0]: A20='مازاد تجديد ارزيابي دارايي\u200cها ' | B20=0 | C20=0 | D20=0
  row 21 [n=4 text=1 number=3 other=0]: A21='تفاوت تسعیر ارز عملیات خارجی ' | B21=0 | C21=0 | D21=0
  row 22 [n=4 text=1 number=3 other=0]: A22='مالیات مربوط به سایر اقلام سود و زیان جامع ' | B22=0 | C22=0 | D22=0
PS D:\Winprojects\analyzer>
(analyzer) Stop-Transcript
**********************
Windows PowerShell transcript end
End time: 20261115231342
**********************
