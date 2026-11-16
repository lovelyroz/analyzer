(analyzer) PS D:\Winprojects\analyzer> python src/scripts/excel_table_boundary_signature_audit.py --max-bands 200 --context-before 6 --context-after 6 excel/cheshme.xlsx

## WORKBOOK excel\cheshme.xlsx
Reader: ACCEPTED
SHA-256: 75f8b499b7da397b330ea0f25b5e95062e3b76b9167e3e8d09db353dc0bac938

### SHEET 1 Recovered_Sheet1 | used=A1:V222 | bands=10

[BAND 1] rows=9:10 columns=A,B,C,D,E,F,G,H,I,J,K,L,M,N,O merges=A9:A10,B9:B10,C9:C10,D9:F9,G9:I9,J9:O9
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=12; gap=SINGLE_TEXT
  row 3 [SINGLE_TEXT n=1 columns=A]: A3='صورت وضعیت پرتفوی سهام قابل معامله در بازار سرمایه'
  row 4 [EMPTY]
  row 5 [EMPTY]
  row 6 [EMPTY]
  row 7 [EMPTY]
  row 8 [SINGLE_TEXT n=1 columns=A]: A8='صورت وضعیت پرتفوی سهام قابل معامله در بازار سرمایه'
  row 9 [MULTI_TEXT n=6 columns=A,B,C,D,G,J]: A9='نام شرکت' | B9='سرمایه (میلیون ریال)' | C9='ارزش اسمی هر سهم (ریال)' | D9='ابتدای دوره' | G9='تغییرات' | J9='انتهای دوره'
    MERGES A9:A10,B9:B10,C9:C10,D9:F9,G9:I9,J9:O9
  row 10 [MULTI_TEXT n=12 columns=D,E,F,G,H,I,J,K,L,M,N,O]: D10='تعداد سهام' | E10='بهای تمام شده' | F10='ارزش بازار' | G10='تعداد سهام' | H10='بهای تمام شده' | I10='ارزش بازار' | J10='درصد مالکیت' | K10='بهای تمام شده' | L10='ارزش بازار' | M10='بهای تمام شده هر سهم (ریال)' | N10='ارزش هر سهم (ریال)' | O10='افزایش (کاهش)'
    MERGES A9:A10,B9:B10,C9:C10
  row 11 [SINGLE_TEXT n=1 columns=A]: A11='سهام پذیرفته شده در بورس و فرابورس '
  row 12 [MIXED_NUMERIC n=13 columns=A,B,C,D,E,F,G,H,I,K,L,N,O]: A12='ملي صنايع مس ايران ' | B12=1440000000 | C12=1000 | D12=1437377936 | E12=5195175 | F12=34942657 | G12=0 | H12=0 | I12=6597565 | K12=5195175 | L12=41540222 | N12=28900 | O12=36345047
  row 13 [MIXED_NUMERIC n=13 columns=A,B,C,D,E,F,G,H,I,K,L,N,O]: A13='هلدينگ توسعه معادن و فلزات ' | B13=540000000 | C13=1000 | D13=33994325 | E13=125885 | F13=110821 | G13=0 | H13=0 | I13=44193 | K13=125885 | L13=155014 | N13=4560 | O13=29129
  row 14 [MIXED_NUMERIC n=13 columns=A,B,C,D,E,F,G,H,I,K,L,N,O]: A14='فولاد مبارکه اصفهان ' | B14=1935000000 | C14=1000 | D14=157894733 | E14=434720 | F14=514736 | G14=0 | H14=0 | I14=151579 | K14=434720 | L14=666315 | N14=4220 | O14=231595
  row 15 [MIXED_NUMERIC n=13 columns=A,B,C,D,E,F,G,H,I,K,L,N,O]: A15='سنگ آهن گل گهر ' | B15=593000000 | C15=1000 | D15=6683861 | E15=20912 | F15=18514 | G15=0 | H15=0 | I15=7352 | K15=20912 | L15=25866 | N15=3870 | O15=4954
  row 16 [MIXED_NUMERIC n=13 columns=A,B,C,D,E,F,G,H,I,K,L,N,O]: A16='سایر سهام پذیرفته شده در بورس و فرابورس ' | B16=0 | C16=0 | D16=600001 | E16=8405 | F16=4200 | G16=0 | H16=0 | I16=0 | K16=8405 | L16=4200 | N16=7000 | O16=-4205

[BAND 2] rows=44:45 columns=A,B,C,D,E,F,G,H,I,J,K merges=A44:A45,B44:B45,C44:C45,D44:E44,F44:G44,H44:J44,K44:K45
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=46; gap=none
  row 38 [SINGLE_TEXT n=1 columns=A]: A38='صورت وضعيت پرتفوي سهام سایر شركت\u200cها'
  row 39 [EMPTY]
  row 40 [EMPTY]
  row 41 [EMPTY]
  row 42 [EMPTY]
  row 43 [SINGLE_TEXT n=1 columns=A]: A43='صورت وضعيت پرتفوي سهام ساير شركت\u200cها'
  row 44 [MULTI_TEXT n=7 columns=A,B,C,D,F,H,K]: A44='نام شرکت' | B44='سرمایه (میلیون ریال)' | C44='ارزش اسمی هر سهم (ریال)' | D44='ابتدای دوره' | F44='تغییرات' | H44='انتهای دوره' | K44='تشریح آخرین وضعیت، سیاست تقسیم سود و برنامه\u200cهای آتی در شرکت\u20...
    MERGES A44:A45,B44:B45,C44:C45,D44:E44,F44:G44,H44:J44,K44:K45
  row 45 [MULTI_TEXT n=7 columns=D,E,F,G,H,I,J]: D45='تعداد سهام' | E45='بهای تمام شده' | F45='تعداد سهام' | G45='بهای تمام شده' | H45='درصد مالکیت' | I45='بهای تمام شده' | J45='بهای تمام شده هر سهم (ریال)'
    MERGES A44:A45,B44:B45,C44:C45,K44:K45
  row 46 [MIXED_NUMERIC n=8 columns=A,B,C,D,E,F,G,I]: A46='سرمايه گذاري بين المللي فريد گسترش ' | B46=1000 | C46=1000000 | D46=150 | E46=15150 | F46=0 | G46=0 | I46=15150
  row 47 [MIXED_NUMERIC n=8 columns=A,B,C,D,E,F,G,I]: A47='شرکت سرمايه گذاري راهيان سهام ' | B47=6000000 | C47=1000 | D47=3738750000 | E47=4114750 | F47=0 | G47=0 | I47=4114750
  row 48 [MIXED_NUMERIC n=8 columns=A,B,C,D,E,F,G,I]: A48='آلياژ کار مبين گستر کرمان ' | B48=10 | C48=1000 | D48=10000 | E48=10 | F48=0 | G48=0 | I48=10
  row 49 [MIXED_NUMERIC n=8 columns=A,B,C,D,E,F,G,I]: A49='آلياژ کار ' | B49=280000 | C49=1000 | D49=211679580 | E49=147244 | F49=0 | G49=0 | I49=147244
  row 50 [MIXED_NUMERIC n=8 columns=A,B,C,D,E,F,G,I]: A50='کارگزاري بورس فلزات سي ولکسي کالا ' | B50=1000 | C50=1000 | D50=300000 | E50=237720 | F50=0 | G50=0 | I50=237720
  row 51 [MIXED_NUMERIC n=8 columns=A,B,C,D,E,F,G,I]: A51='آرين ماهتاب گستر ' | B51=39256500 | C51=1000 | D51=3925649999 | E51=248001 | F51=0 | G51=0 | I51=248001

[BAND 3] rows=77:77 columns=A,B,C,D,E merges=—
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=78; gap=none
  row 71 [SINGLE_TEXT n=1 columns=A]: A71='صورت ريزمعاملات سهام - تحصیل شده'
  row 72 [EMPTY]
  row 73 [EMPTY]
  row 74 [EMPTY]
  row 75 [EMPTY]
  row 76 [SINGLE_TEXT n=1 columns=A]: A76='صورت ریز معاملات سهام تحصیل شده'
  row 77 [MULTI_TEXT n=5 columns=A,B,C,D,E]: A77='نام شرکت' | B77='تعداد سهام' | C77='بهاي تمام شده هر سهم (ريال)' | D77='کل مبلغ بهاي تمام شده قابل معامله در بازار سرمايه' | E77='کل مبلغ بهاي تمام شده سهام ساير شرکتها'
  row 78 [MIXED_NUMERIC n=4 columns=A,B,D,E]: A78='صنعتي پارس مينو ' | B78=48000000 | D78=101541 | E78=0
  row 79 [MIXED_NUMERIC n=4 columns=A,B,D,E]: A79='کشت و دام گلدشت نمونه اصفهان ' | B79=7100000 | D79=76795 | E79=0
  row 80 [MIXED_NUMERIC n=4 columns=A,B,D,E]: A80='لابراتوارهاي رازک ' | B80=6742609 | D80=32145 | E80=0
  row 81 [MIXED_NUMERIC n=4 columns=A,B,D,E]: A81='تامين سرمايه کيميا (حق تقدم) ' | B81=70234926 | D81=54432 | E81=0
  row 82 [EMPTY]
  row 83 [MIXED_NUMERIC n=3 columns=A,D,E]: A83='جمع ' | D83=264913 | E83=0

[BAND 4] rows=94:94 columns=A,B,C,D,E,F,G merges=—
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=95; gap=none
  row 88 [SINGLE_TEXT n=1 columns=A]: A88='صورت ريزمعاملات سهام - واگذار شده'
  row 89 [EMPTY]
  row 90 [EMPTY]
  row 91 [EMPTY]
  row 92 [EMPTY]
  row 93 [SINGLE_TEXT n=1 columns=A]: A93='صورت ریز معاملات سهام واگذار شده'
  row 94 [MULTI_TEXT n=7 columns=A,B,C,D,E,F,G]: A94='نام شرکت' | B94='تعداد سهام' | C94='بهای تمام شده هر سهم (ریال)' | D94='کل مبلغ بهای تمام شده' | E94='قیمت واگذاری هر سهم (ریال)' | F94='کل مبلغ واگذاری' | G94='سود (زیان) واگذاری'
  row 95 [MIXED_NUMERIC n=4 columns=A,D,F,G]: A95='جمع ' | D95=0 | F95=0 | G95=0
  row 96 [MIXED_NUMERIC n=2 columns=A,G]: A96='سود (زیان) فروش سهام غیرعملیاتی ' | G96=0
    MERGES A96:F96
  row 97 [MIXED_NUMERIC n=2 columns=A,G]: A97='سود (زیان) فروش سهام عملیاتی ' | G97=0
    MERGES A97:F97
  row 98 [EMPTY]
  row 99 [EMPTY]
  row 100 [EMPTY]

[BAND 5] rows=107:109 columns=A,B,C,D,E,F,G,H,I,J,K merges=A107:A109,B107:G107,H107:K107,B108:B109,C108:C109,D108:D109,E108:E109,F108:F109,G108:G109,H108:H109,I108:I109,J108:K108
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=110; gap=none
  row 101 [SINGLE_TEXT n=1 columns=A]: A101='درآمد حاصل از سود سهام محقق شده'
  row 102 [EMPTY]
  row 103 [EMPTY]
  row 104 [EMPTY]
  row 105 [EMPTY]
  row 106 [SINGLE_TEXT n=1 columns=A]: A106='درآمد حاصل از سود سهام محقق شده'
  row 107 [MULTI_TEXT n=3 columns=A,B,H]: A107='نام شرکت' | B107='وضعیت پورتفوی' | H107='وضعیت سودآوری'
    MERGES A107:A109,B107:G107,H107:K107
  row 108 [MULTI_TEXT n=9 columns=B,C,D,E,F,G,H,I,J]: B108='سال مالی شرکت سرمایه پذیر' | C108='تاریخ برگزاری مجمع' | D108='تعداد سهام در تاریخ مجمع' | E108='سرمایه (میلیون ریال)' | F108='ارزش اسمی هر سهم (ریال)' | G108='درصد مالکیت' | H108='سود (زیان) هر سهم (ریال)' | I108='سود تقسیمی هر سهم (ریال)' | J108='درآمد حاصل از سود سهام مجمع برگزار شده و سال مالی شناسایی درآمد'
    MERGES A107:A109,B108:B109,C108:C109,D108:D109,E108:E109,F108:F109,G108:G109,H108:H109,I108:I109,J108:K108
  row 109 [MULTI_TEXT n=2 columns=J,K]: J109='۱۴۰۵/۱۲/۲۹' | K109='* ۱۴۰۴/۱۲/۲۹'
    MERGES A107:A109,B108:B109,C108:C109,D108:D109,E108:E109,F108:F109,G108:G109,H108:H109,I108:I109
  row 110 [MIXED_NUMERIC n=3 columns=A,J,K]: A110='جمع سود تقسیمی شرکتها ' | J110=0 | K110=0
  row 111 [EMPTY]
  row 112 [MIXED_NUMERIC n=3 columns=A,J,K]: A112='جمع سود تقسیمی صندوق ها ' | J112=0 | K112=0
  row 113 [MIXED_NUMERIC n=3 columns=A,J,K]: A113='جمع کل ' | J113=0 | K113=0
  row 114 [MIXED_NUMERIC n=2 columns=A,J]: A114='درآمد سود سهام محقق شده از ابتدای سال مالی تا پایان ماه گذشته ' | J114=750315
    MERGES A114:I114,J114:K114
  row 115 [MIXED_NUMERIC n=2 columns=A,J]: A115='درآمد سود سهام محقق شده از ابتدای سال مالی تا پایان ماه ' | J115=750315
    MERGES A115:I115,J115:K115

[BAND 6] rows=130:130 columns=A,B,C,D,E,F,G merges=—
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=131; gap=none
  row 124 [SINGLE_TEXT n=1 columns=A]: A124='جزئیات درآمدهای عملیاتی و سرمایه گذاری\u200cهای شرکت'
  row 125 [EMPTY]
  row 126 [EMPTY]
  row 127 [EMPTY]
  row 128 [EMPTY]
  row 129 [SINGLE_TEXT n=1 columns=A]: A129='درآمدهای عملیاتی شرکت'
  row 130 [MULTI_TEXT n=7 columns=A,B,C,D,E,F,G]: A130='شرح' | B130='از ابتدای سال مالی تا پایان دوره منتهی به ۱۴۰۵/۰۶/۳۱' | C130='اصلاحات' | D130='از ابتدای سال مالی تا پایان دوره منتهی به ۱۴۰۵/۰۶/۳۱ (اصلاح شده)' | E130='دوره ۱ ماهه منتهی به ۱۴۰۵/۰۷/۳۰' | F130='از ابتدای سال مالی تا پایان دوره منتهی به ۱۴۰۵/۰۷/۳۰' | G130='سال مالی منتهی به ۱۴۰۴/۱۲/۲۹'
  row 131 [MIXED_NUMERIC n=7 columns=A,B,C,D,E,F,G]: A131='درآمد سود سهام ' | B131=750315 | C131=0 | D131=750315 | E131=0 | F131=750315 | G131=13841355
  row 132 [MIXED_NUMERIC n=7 columns=A,B,C,D,E,F,G]: A132='درآمد سود تضمین شده ' | B132=0 | C132=0 | D132=0 | E132=0 | F132=0 | G132=0
  row 133 [MIXED_NUMERIC n=7 columns=A,B,C,D,E,F,G]: A133='سود (زیان) فروش سرمایه\u200cگذاری\u200cها ' | B133=57799 | C133=0 | D133=57799 | E133=0 | F133=57799 | G133=393484
  row 134 [MIXED_NUMERIC n=7 columns=A,B,C,D,E,F,G]: A134='سود (زیان) تغییر ارزش سرمایه\u200cگذاری\u200cها ' | B134=0 | C134=0 | D134=0 | E134=0 | F134=0 | G134=0
  row 135 [MIXED_NUMERIC n=7 columns=A,B,C,D,E,F,G]: A135='سایر درآمدها ' | B135=14983890 | C135=0 | D135=14983890 | E135=4123061 | F135=19106951 | G135=36789792
  row 136 [MIXED_NUMERIC n=7 columns=A,B,C,D,E,F,G]: A136='جمع ' | B136=15792004 | C136=0 | D136=15792004 | E136=4123061 | F136=19915065 | G136=51024631

[BAND 7] rows=138:139 columns=A,B,C merges=A138:A139
  SIGNATURE=COMPOUND_CANDIDATE
  PRIOR prior_body=136; gap=SINGLE_TEXT
  FOLLOWING next_body=140; gap=none
  row 132 [MIXED_NUMERIC n=7 columns=A,B,C,D,E,F,G]: A132='درآمد سود تضمین شده ' | B132=0 | C132=0 | D132=0 | E132=0 | F132=0 | G132=0
  row 133 [MIXED_NUMERIC n=7 columns=A,B,C,D,E,F,G]: A133='سود (زیان) فروش سرمایه\u200cگذاری\u200cها ' | B133=57799 | C133=0 | D133=57799 | E133=0 | F133=57799 | G133=393484
  row 134 [MIXED_NUMERIC n=7 columns=A,B,C,D,E,F,G]: A134='سود (زیان) تغییر ارزش سرمایه\u200cگذاری\u200cها ' | B134=0 | C134=0 | D134=0 | E134=0 | F134=0 | G134=0
  row 135 [MIXED_NUMERIC n=7 columns=A,B,C,D,E,F,G]: A135='سایر درآمدها ' | B135=14983890 | C135=0 | D135=14983890 | E135=4123061 | F135=19106951 | G135=36789792
  row 136 [MIXED_NUMERIC n=7 columns=A,B,C,D,E,F,G]: A136='جمع ' | B136=15792004 | C136=0 | D136=15792004 | E136=4123061 | F136=19915065 | G136=51024631
  row 137 [SINGLE_TEXT n=1 columns=A]: A137='سرمایه گذاری های شرکت'
  row 138 [MULTI_TEXT n=3 columns=A,B,C]: A138='شرح' | B138='دوره مالی منتهی به ۱۴۰۵/۰۷/۳۰' | C138='سال مالی منتهی به ۱۴۰۴/۱۲/۲۹'
    MERGES A138:A139
  row 139 [MULTI_TEXT n=2 columns=B,C]: B139='بهای تمام شده' | C139='بهای تمام شده'
    MERGES A138:A139
  row 140 [MIXED_NUMERIC n=3 columns=A,B,C]: A140='سهام شرکت های قابل معامله در بازار سرمایه (شرکت های پذیرفته شده در ب... | B140=10207407 | C140=11232028
  row 141 [MIXED_NUMERIC n=3 columns=A,B,C]: A141='واحدهای صندوق\u200cهای سرمایه\u200cگذاری (در سهام، مختلط، جسورانه، ب... | B141=1857189 | C141=924114
  row 142 [MIXED_NUMERIC n=3 columns=A,B,C]: A142='اوراق مشتقه و تأمین مالی (اختیار معامله، قراردادهای آتی، گواهی سپرده... | B142=0 | C142=0
  row 143 [MIXED_NUMERIC n=3 columns=A,B,C]: A143='سهام\u200c سایر شركت\u200c\u200cها ' | B143=10187841 | C143=10190841
  row 144 [MIXED_NUMERIC n=3 columns=A,B,C]: A144='سپرده هاى\u200c سرمايه\u200f گذارى بانکی ' | B144=0 | C144=0
  row 145 [MIXED_NUMERIC n=3 columns=A,B,C]: A145='سرمایه\u200cگذاری در املاک ' | B145=0 | C145=0

[BAND 8] rows=160:161 columns=A,B,C,D,E,F,G,H,I,J,K merges=A160:A161,B160:D160,E160:G160,H160:K160
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=163; gap=SINGLE_TEXT
  row 154 [SINGLE_TEXT n=1 columns=A]: A154='صورت وضعیت سایر سرمایه گذاری\u200cها'
  row 155 [EMPTY]
  row 156 [EMPTY]
  row 157 [EMPTY]
  row 158 [EMPTY]
  row 159 [SINGLE_TEXT n=1 columns=A]: A159='صورت وضعیت سایر سرمایه گذاری\u200cها'
  row 160 [MULTI_TEXT n=4 columns=A,B,E,H]: A160='شرح' | B160='ابتدای دوره' | E160='خالص خرید (فروش) طی دوره' | H160='انتهای دوره'
    MERGES A160:A161,B160:D160,E160:G160,H160:K160
  row 161 [MULTI_TEXT n=10 columns=B,C,D,E,F,G,H,I,J,K]: B161='تعداد' | C161='بهای تمام شده' | D161='ارزش بازار' | E161='تعداد' | F161='بهای تمام شده' | G161='سود (زیان) فروش' | H161='تعداد' | I161='بهای تمام شده' | J161='ارزش بازار' | K161='افزایش (کاهش)'
    MERGES A160:A161
  row 162 [SINGLE_TEXT n=1 columns=A]: A162='سرمایه گذاری در واحدهای صندوق\u200cهای سرمایه\u200c گذاری: '
  row 163 [MIXED_NUMERIC n=11 columns=A,B,C,D,E,F,G,H,I,J,K]: A163='صندوق سرمايه گذاري مشترک صنعت و معدن ' | B163=403447 | C163=400000 | D163=401421 | E163=0 | F163=0 | G163=0 | H163=403447 | I163=400000 | J163=401421 | K163=1421
  row 164 [MIXED_NUMERIC n=11 columns=A,B,C,D,E,F,G,H,I,J,K]: A164='در اوراق بهادار با درآمد ثابت کيميا ' | B164=82107257 | C164=1457189 | D164=2043485 | E164=0 | F164=0 | G164=0 | H164=82107257 | I164=1457189 | J164=2100310 | K164=643121
  row 165 [EMPTY]
  row 166 [MIXED_NUMERIC n=11 columns=A,B,C,D,E,F,G,H,I,J,K]: A166='جمع واحدهای صندوق\u200cهای سرمایه\u200c گذاری ' | B166=82510704 | C166=1857189 | D166=2444906 | E166=0 | F166=0 | G166=0 | H166=82510704 | I166=1857189 | J166=2501731 | K166=644542
  row 167 [SINGLE_TEXT n=1 columns=A]: A167='سرمایه گذاری در اوراق مشتقه و تامین مالی: '

[BAND 9] rows=194:196 columns=A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V merges=A194:A196,B194:I194,J194:N194,O194:V194,B195:D195,E195:F195,G195:I195,J195:K195,M195:N195,O195:Q195,R195:S195,T195:V195
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=197; gap=none
  row 188 [SINGLE_TEXT n=1 columns=A]: A188='صورت خلاصه سرمایه گذاری در سهام به تفکیک صنعت'
  row 189 [EMPTY]
  row 190 [EMPTY]
  row 191 [EMPTY]
  row 192 [EMPTY]
  row 193 [SINGLE_TEXT n=1 columns=A]: A193='صورت خلاصه سرمايه گذاري در سهام به تفکيک گروه صنعت'
  row 194 [MULTI_TEXT n=4 columns=A,B,J,O]: A194='شرح سرمايه گذاري' | B194='سهام قابل معامله در بازار سرمايه' | J194='سهام ساير شرکتها' | O194='کل سرمايه گذاري در سهام'
    MERGES A194:A196,B194:I194,J194:N194,O194:V194
  row 195 [MULTI_TEXT n=9 columns=B,E,G,J,L,M,O,R,T]: B195='ابتداي دوره' | E195='تغييرات' | G195='انتهاي دوره' | J195='ابتداي دوره' | L195='تغييرات' | M195='انتهاي دوره' | O195='ابتداي دوره' | R195='تغييرات' | T195='انتهاي دوره'
    MERGES A194:A196,B195:D195,E195:F195,G195:I195,J195:K195,M195:N195,O195:Q195,R195:S195,T195:V195
  row 196 [MULTI_TEXT n=21 columns=B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V]: B196='تعداد شرکت' | C196='بهاي تمام شده' | D196='ارزش بازار' | E196='بهاي تمام شده' | F196='ارزش بازار' | G196='تعداد شرکت' | H196='بهاي تمام شده' | I196='ارزش بازار' | J196='تعداد شرکت' | K196='بهاي تمام شده' | L196='بهاي تمام شده' | M196='تعداد شرکت' | N196='بهاي تمام شده' | O196='تعداد شرکت' | P196='بهاي تمام شده' | Q196='درصد به کل' | R196='بهاي تمام شده' | S196='درصد به کل' | T196='تعداد شرکت' | U196='بهاي تمام شده' | V196='درصد به کل'
    MERGES A194:A196
  row 197 [MIXED_NUMERIC n=22 columns=A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V]: A197='استخراج کانه هاي فلزي ' | B197=4 | C197=149433 | D197=133854 | E197=0 | F197=55891 | G197=4 | H197=149433 | I197=189745 | J197=0 | K197=0 | L197=0 | M197=0 | N197=0 | O197=4 | P197=149433 | Q197=0.74 | R197=0 | S197=0 | T197=4 | U197=149433 | V197=0.73
  row 198 [MIXED_NUMERIC n=22 columns=A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V]: A198='استخراج ساير معادن ' | B198=0 | C198=0 | D198=0 | E198=0 | F198=0 | G198=0 | H198=0 | I198=0 | J198=2 | K198=3213530 | L198=0 | M198=2 | N198=3213530 | O198=2 | P198=3213530 | Q198=15.96 | R198=0 | S198=0 | T198=2 | U198=3213530 | V198=15.76
  row 199 [MIXED_NUMERIC n=22 columns=A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V]: A199='مواد و محصولات شيميايي ' | B199=0 | C199=0 | D199=0 | E199=0 | F199=0 | G199=0 | H199=0 | I199=0 | J199=3 | K199=439475 | L199=0 | M199=3 | N199=439475 | O199=3 | P199=439475 | Q199=2.18 | R199=0 | S199=0 | T199=3 | U199=439475 | V199=2.15
  row 200 [MIXED_NUMERIC n=22 columns=A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V]: A200='واسطه\u200cگريهاي مالي و پولي ' | B200=0 | C200=0 | D200=0 | E200=0 | F200=0 | G200=0 | H200=0 | I200=0 | J200=1 | K200=600144 | L200=0 | M200=1 | N200=600144 | O200=1 | P200=600144 | Q200=2.98 | R200=0 | S200=0 | T200=1 | U200=600144 | V200=2.94
  row 201 [MIXED_NUMERIC n=22 columns=A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V]: A201='انبوه سازي، املاک و مستغلات ' | B201=0 | C201=0 | D201=0 | E201=0 | F201=0 | G201=0 | H201=0 | I201=0 | J201=1 | K201=358888 | L201=0 | M201=1 | N201=358888 | O201=1 | P201=358888 | Q201=1.78 | R201=0 | S201=0 | T201=1 | U201=358888 | V201=1.76
  row 202 [MIXED_NUMERIC n=22 columns=A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V]: A202='فعاليتهاي کمکي به نهادهاي مالي واسط ' | B202=1 | C202=215625 | D202=345321 | E202=54432 | F202=34837 | G202=2 | H202=270057 | I202=380158 | J202=1 | K202=237720 | L202=0 | M202=1 | N202=237720 | O202=2 | P202=453345 | Q202=2.25 | R202=54432 | S202=20.55 | T202=3 | U202=507777 | V202=2.49

[BAND 10] rows=217:219 columns=A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V merges=A217:A219,B217:I217,J217:N217,O217:V217,B218:D218,E218:F218,G218:I218,J218:K218,M218:N218,O218:Q218,R218:S218,T218:V218
  SIGNATURE=NO_MATCH
  PRIOR prior_body=216; gap=none
  FOLLOWING next_body=None; gap=none
  row 211 [MIXED_NUMERIC n=22 columns=A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V]: A211='پيمانکاري صنعتي ' | B211=0 | C211=0 | D211=0 | E211=0 | F211=0 | G211=0 | H211=0 | I211=0 | J211=2 | K211=175704 | L211=0 | M211=2 | N211=175704 | O211=2 | P211=175704 | Q211=0.87 | R211=0 | S211=0 | T211=2 | U211=175704 | V211=0.86
  row 212 [MIXED_NUMERIC n=22 columns=A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V]: A212='حمل ونقل، انبارداري و ارتباطات ' | B212=0 | C212=0 | D212=0 | E212=0 | F212=0 | G212=0 | H212=0 | I212=0 | J212=1 | K212=0 | L212=0 | M212=1 | N212=0 | O212=1 | P212=0 | Q212=0 | R212=0 | S212=0 | T212=1 | U212=0 | V212=0
  row 213 [MIXED_NUMERIC n=22 columns=A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V]: A213='ساير صنايع ' | B213=0 | C213=0 | D213=0 | E213=76795 | F213=98477 | G213=1 | H213=76795 | I213=98477 | J213=1 | K213=202500 | L213=0 | M213=1 | N213=202500 | O213=1 | P213=202500 | Q213=1.01 | R213=76795 | S213=28.99 | T213=2 | U213=279295 | V213=1.37
  row 214 [MIXED_NUMERIC n=22 columns=A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V]: A214='ساير فعاليتها ' | B214=1 | C214=8405 | D214=4200 | E214=0 | F214=0 | G214=1 | H214=8405 | I214=4200 | J214=2 | K214=449875 | L214=0 | M214=2 | N214=449875 | O214=3 | P214=458280 | Q214=2.28 | R214=0 | S214=0 | T214=3 | U214=458280 | V214=2.25
  row 215 [EMPTY]
  row 216 [MIXED_NUMERIC n=22 columns=A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V]: A216='جمع ' | B216=0 | C216=0 | D216=0 | E216=0 | F216=0 | G216=0 | H216=0 | I216=0 | J216=0 | K216=0 | L216=0 | M216=0 | N216=0 | O216=0 | P216=0 | Q216=0 | R216=0 | S216=0 | T216=0 | U216=0 | V216=0
  row 217 [MULTI_TEXT n=4 columns=A,B,J,O]: A217='شرح' | B217='سهام قابل معامله در بازار سرمايه' | J217='سهام ساير شرکتها' | O217='کل سرمايه گذاري در سهام'
    MERGES A217:A219,B217:I217,J217:N217,O217:V217
  row 218 [MULTI_TEXT n=9 columns=B,E,G,J,L,M,O,R,T]: B218='ابتداي دوره' | E218='تغييرات' | G218='انتهاي دوره' | J218='ابتداي دوره' | L218='تغييرات' | M218='انتهاي دوره' | O218='ابتداي دوره' | R218='تغييرات' | T218='انتهاي دوره'
    MERGES A217:A219,B218:D218,E218:F218,G218:I218,J218:K218,M218:N218,O218:Q218,R218:S218,T218:V218
  row 219 [MULTI_TEXT n=21 columns=B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V]: B219='تعداد شرکت' | C219='بهاي تمام شده' | D219='ارزش بازار' | E219='بهاي تمام شده' | F219='ارزش بازار' | G219='تعداد شرکت' | H219='بهاي تمام شده' | I219='ارزش بازار' | J219='تعداد شرکت' | K219='بهاي تمام شده' | L219='بهاي تمام شده' | M219='تعداد شرکت' | N219='بهاي تمام شده' | O219='تعداد شرکت' | P219='بهاي تمام شده' | Q219='درصد به کل' | R219='بهاي تمام شده' | S219='درصد به کل' | T219='تعداد شرکت' | U219='بهاي تمام شده' | V219='درصد به کل'
    MERGES A217:A219
  row 220 [SINGLE_TEXT n=1 columns=A]: A220='ذخيره کاهش ارزش سرمايه گذاري در سهام '
  row 221 [SINGLE_TEXT n=1 columns=A]: A221='لطفا دلايل مغايرت اطلاعات ابتداي دوره ي دوره جاري با اطلاعات انتهاي ...
    MERGES A221:V221
  row 222 [EMPTY]
    MERGES A222:V222
  row 223 [EMPTY]
  row 224 [EMPTY]
  row 225 [EMPTY]

SUMMARY bands_printed=10 compound_candidates=1