**********************
Windows PowerShell transcript start
Start time: 20261116125613
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
Transcript started, output file is D:\Winprojects\analyzer\boundary_signature_audit.txt
PS D:\Winprojects\analyzer>
(analyzer) python src/scripts/excel_table_boundary_signature_audit.py --max-bands 200 --context-before 6 --context-after 6 excel/cheshme.xlsx excel/fzar.xlsx excel/fzar2.xlsx excel/samanBank.xlsx excel/parsian_periodic.xlsx
  row 32 [SINGLE_TEXT n=1 columns=A]: A32='خرید مواد اولیه'
  row 33 [MULTI_TEXT n=8 columns=A,B,C,F,I,L,O,R]: A33='شرح' | B33='واحد' | C33='از ابتدای سال مالی تا تاریخ ۱۴۰۵/۰۶/۳۱'
 | F33='اصلاحات' | I33='ازابتدای سال مالی تا تاریخ ۱۴۰۵/۰۶/۳۱ (اصلاح شده)' | L33='خرید دوره یک ماهه منتهی به ۱۴۰۵/۰۷/۳۰'
 | O33='مواد اولیه خریداری شده از ابتدای دوره تا پایان دوره منتهی به ۱۴۰۵/۰۷... | R33='از ابتدای سال مالی تا تاریخ ۱۴۰۴/
۰۷/۳۰'
    MERGES A33:A34,B33:B34,C33:E33,F33:H33,I33:K33,L33:N33,O33:Q33,R33:T33
  row 34 [MULTI_TEXT n=18 columns=C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T]: C34='مقدار' | D34='نرخ (ریال)' | E34='مبلغ (میلی
ون ریال)' | F34='مقدار' | G34='نرخ (ريال)' | H34='مبلغ ( میلیون ریال)' | I34='مقدار' | J34='نرخ (ريال)' | K34='مبلغ (میل
یون ریال)' | L34='مقدار' | M34='نرخ (ريال)' | N34='مبلغ (میلیون ریال)' | O34='مقدار' | P34='نرخ (ريال)' | Q34='مبلغ (میل
یون ریال)' | R34='مقدار' | S34='نرخ (ريال)' | T34='مبلغ (میلیون ریال)'
    MERGES A33:A34,B33:B34
  row 35 [SINGLE_TEXT n=1 columns=A]: A35='مواد اولیه داخلی '
  row 36 [EMPTY]
  row 37 [MIXED_NUMERIC n=19 columns=A,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T]: A37='جمع مواد اولیه داخلی ' | C37=0 | D37=0
 | E37=0 | F37=0 | G37=0 | H37=0 | I37=0 | J37=0 | K37=0 | L37=0 | M37=0 | N37=0 | O37=0 | P37=0 | Q37=0 | R37=0 | S37=0
 | T37=0
  row 38 [SINGLE_TEXT n=1 columns=A]: A38='مواد اولیه وارداتی '
  row 39 [EMPTY]
  row 40 [MIXED_NUMERIC n=19 columns=A,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T]: A40='جمع مواد اولیه وارداتی ' | C40=0 | D40
=0 | E40=0 | F40=0 | G40=0 | H40=0 | I40=0 | J40=0 | K40=0 | L40=0 | M40=0 | N40=0 | O40=0 | P40=0 | Q40=0 | R40=0 | S40
=0 | T40=0

[BAND 3] rows=43:44 columns=A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X merges=A43:A44,B43:B44,C43:C44,D43:D44,E43:G
43,H43:J43,K43:M43,N43:P43,Q43:S43,T43:V43,X43:X44
  SIGNATURE=COMPOUND_CANDIDATE
  PRIOR prior_body=41; gap=SINGLE_TEXT
  FOLLOWING next_body=45; gap=none
  row 37 [MIXED_NUMERIC n=19 columns=A,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T]: A37='جمع مواد اولیه داخلی ' | C37=0 | D37=0
 | E37=0 | F37=0 | G37=0 | H37=0 | I37=0 | J37=0 | K37=0 | L37=0 | M37=0 | N37=0 | O37=0 | P37=0 | Q37=0 | R37=0 | S37=0
 | T37=0
  row 38 [SINGLE_TEXT n=1 columns=A]: A38='مواد اولیه وارداتی '
  row 39 [EMPTY]
  row 40 [MIXED_NUMERIC n=19 columns=A,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T]: A40='جمع مواد اولیه وارداتی ' | C40=0 | D40
=0 | E40=0 | F40=0 | G40=0 | H40=0 | I40=0 | J40=0 | K40=0 | L40=0 | M40=0 | N40=0 | O40=0 | P40=0 | Q40=0 | R40=0 | S40
=0 | T40=0
  row 41 [MIXED_NUMERIC n=19 columns=A,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T]: A41='جمع کل ' | C41=0 | D41=0 | E41=0 | F41
=0 | G41=0 | H41=0 | I41=0 | J41=0 | K41=0 | L41=0 | M41=0 | N41=0 | O41=0 | P41=0 | Q41=0 | R41=0 | S41=0 | T41=0
  row 42 [SINGLE_TEXT n=1 columns=A]: A42='انرژی'
  row 43 [MULTI_TEXT n=12 columns=A,B,C,D,E,H,K,N,Q,T,W,X]: A43='صنعت' | B43='طبقه بندی' | C43='نوع انرژی' | D43='واحد ا
ندازه گیری' | E43='از ابتدای سال مالی تا تاریخ ۱۴۰۵/۰۶/۳۱' | H43='اصلاحات' | K43='از ابتدای سال مالی تا تاریخ ۱۴۰۵/۰۶/۳۱
 (اصلاح شده)' | N43='دوره یک ماهه منتهی به ۱۴۰۵/۰۷/۳۰' | Q43='از ابتدای سال مالی تا تاریخ ۱۴۰۵/۰۷/۳۰' | T43='از ابتدای س
ال مالی تا تاریخ ۱۴۰۴/۰۷/۳۰' | W43='مانده پیش بینی تا انتهای سال مالی ۱۴۰۵/۰۹/۳۰' | X43='توضیحات در خصوص علت تغییر میزان
 مصرف'
    MERGES A43:A44,B43:B44,C43:C44,D43:D44,E43:G43,H43:J43,K43:M43,N43:P43,Q43:S43,T43:V43,X43:X44
  row 44 [MULTI_TEXT n=19 columns=E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W]: E44='مقدار مصرف' | F44='نرخ - ریال' | G44='مبل
غ - میلیون ریال' | H44='مقدار مصرف' | I44='نرخ - ریال' | J44='مبلغ - میلیون ریال' | K44='مقدار مصرف' | L44='نرخ - ریال'
| M44='مبلغ - میلیون ریال' | N44='مقدار مصرف' | O44='نرخ - ریال' | P44='مبلغ - میلیون ریال' | Q44='مقدار مصرف' | R44='نر
خ - ریال' | S44='مبلغ - میلیون ریال' | T44='مقدار' | U44='نرخ - ریال' | V44='مبلغ' | W44='مقدار مصرف'
    MERGES A43:A44,B43:B44,C43:C44,D43:D44,X43:X44
  row 45 [MIXED_NUMERIC n=23 columns=A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W]: A45='استخراج کانه هاي فلزي ' | B45=
'سوخت ' | C45='گاز سوخت ' | D45='مترمکعب ' | E45=2354 | F45=11470 | G45=27 | H45=0 | I45=0 | J45=0 | K45=2354 | L45=1147
0 | M45=27 | N45=0 | O45=0 | P45=0 | Q45=2354 | R45=11470 | S45=27 | T45=2761 | U45=3984 | V45=11 | W45=1046
  row 46 [MIXED_NUMERIC n=23 columns=A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W]: A46='استخراج کانه هاي فلزي ' | B46=
'سوخت ' | C46='برق ' | D46='مگاوات ساعت ' | E46=601 | F46=11615641 | G46=6981 | H46=0 | I46=0 | J46=0 | K46=601 | L46=11
615641 | M46=6981 | N46=56 | O46=17196429 | P46=963 | Q46=657 | R46=12091324 | S46=7944 | T46=648 | U46=6537037 | V46=42
36 | W46=243
  row 47 [EMPTY]
  row 48 [MIXED_NUMERIC n=6 columns=A,G,J,M,P,S]: A48='جمع کل ' | G48=7008 | J48=0 | M48=7008 | P48=963 | S48=7971
  row 49 [SINGLE_TEXT n=1 columns=A]: A49='منابع و مصارف ارزی'
  row 50 [MULTI_TEXT n=9 columns=A,B,C,F,I,L,O,R,U]: A50='منابع ارزی' | B50='نوع ارز' | C50='از ابتدای سال مالی تا تاریخ
 ۱۴۰۵/۰۶/۳۱' | F50='اصلاحات' | I50='از ابتدای سال مالی تا تاریخ ۱۴۰۵/۰۶/۳۱ (اصلاح شده)' | L50='دوره یکماهه ۱۴۰۵/۰۷/۳۰' |
 O50='از ابتدای سال مالی تا تاریخ ۱۴۰۵/۰۷/۳۰' | R50='از ابتدای سال مالی تا تاریخ ۱۴۰۴/۰۷/۳۰' | U50='برآورد مانده تا پایا
ن سال مالی ۱۴۰۵/۰۹/۳۰'
    MERGES A50:A51,B50:B51,C50:E50,F50:H50,I50:K50,L50:N50,O50:Q50,R50:T50,U50:W50

[BAND 4] rows=50:51 columns=A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W merges=A50:A51,B50:B51,C50:E50,F50:H50,I50:K50
,L50:N50,O50:Q50,R50:T50,U50:W50
  SIGNATURE=COMPOUND_CANDIDATE
  PRIOR prior_body=48; gap=SINGLE_TEXT
  FOLLOWING next_body=52; gap=none
  row 44 [MULTI_TEXT n=19 columns=E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W]: E44='مقدار مصرف' | F44='نرخ - ریال' | G44='مبل
غ - میلیون ریال' | H44='مقدار مصرف' | I44='نرخ - ریال' | J44='مبلغ - میلیون ریال' | K44='مقدار مصرف' | L44='نرخ - ریال'
| M44='مبلغ - میلیون ریال' | N44='مقدار مصرف' | O44='نرخ - ریال' | P44='مبلغ - میلیون ریال' | Q44='مقدار مصرف' | R44='نر
خ - ریال' | S44='مبلغ - میلیون ریال' | T44='مقدار' | U44='نرخ - ریال' | V44='مبلغ' | W44='مقدار مصرف'
    MERGES A43:A44,B43:B44,C43:C44,D43:D44,X43:X44
  row 45 [MIXED_NUMERIC n=23 columns=A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W]: A45='استخراج کانه هاي فلزي ' | B45=
'سوخت ' | C45='گاز سوخت ' | D45='مترمکعب ' | E45=2354 | F45=11470 | G45=27 | H45=0 | I45=0 | J45=0 | K45=2354 | L45=1147
0 | M45=27 | N45=0 | O45=0 | P45=0 | Q45=2354 | R45=11470 | S45=27 | T45=2761 | U45=3984 | V45=11 | W45=1046
  row 46 [MIXED_NUMERIC n=23 columns=A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W]: A46='استخراج کانه هاي فلزي ' | B46=
'سوخت ' | C46='برق ' | D46='مگاوات ساعت ' | E46=601 | F46=11615641 | G46=6981 | H46=0 | I46=0 | J46=0 | K46=601 | L46=11
615641 | M46=6981 | N46=56 | O46=17196429 | P46=963 | Q46=657 | R46=12091324 | S46=7944 | T46=648 | U46=6537037 | V46=42
36 | W46=243
  row 47 [EMPTY]
  row 48 [MIXED_NUMERIC n=6 columns=A,G,J,M,P,S]: A48='جمع کل ' | G48=7008 | J48=0 | M48=7008 | P48=963 | S48=7971
  row 49 [SINGLE_TEXT n=1 columns=A]: A49='منابع و مصارف ارزی'
  row 50 [MULTI_TEXT n=9 columns=A,B,C,F,I,L,O,R,U]: A50='منابع ارزی' | B50='نوع ارز' | C50='از ابتدای سال مالی تا تاریخ
 ۱۴۰۵/۰۶/۳۱' | F50='اصلاحات' | I50='از ابتدای سال مالی تا تاریخ ۱۴۰۵/۰۶/۳۱ (اصلاح شده)' | L50='دوره یکماهه ۱۴۰۵/۰۷/۳۰' |
 O50='از ابتدای سال مالی تا تاریخ ۱۴۰۵/۰۷/۳۰' | R50='از ابتدای سال مالی تا تاریخ ۱۴۰۴/۰۷/۳۰' | U50='برآورد مانده تا پایا
ن سال مالی ۱۴۰۵/۰۹/۳۰'
    MERGES A50:A51,B50:B51,C50:E50,F50:H50,I50:K50,L50:N50,O50:Q50,R50:T50,U50:W50
  row 51 [MULTI_TEXT n=21 columns=C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W]: C51='مبلغ ارزی' | D51='نرخ ارز(ریال)' | E5
1='مبلغ ریالی(میلیون ریال)' | F51='مبلغ ارزی' | G51='نرخ ارز(ریال)' | H51='مبلغ ریالی(میلیون ریال)' | I51='مبلغ ارزی' |
J51='نرخ ارز(ریال)' | K51='مبلغ ریالی(میلیون ریال)' | L51='مبلغ ارزی' | M51='نرخ ارز(ریال)' | N51='مبلغ ریالی(میلیون ریا
ل)' | O51='مبلغ ارزی' | P51='نرخ ارز(ریال)' | Q51='مبلغ ریالی(میلیون ریال)' | R51='مبلغ ارزی' | S51='نرخ ارز(ریال)' | T5
1='مبلغ ریالی(میلیون ریال)' | U51='مبلغ ارزی' | V51='نرخ ارز(ریال)' | W51='مبلغ ریالی(میلیون ریال)'
    MERGES A50:A51,B50:B51
  row 52 [MIXED_NUMERIC n=22 columns=A,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W]: A52='سایر ' | C52=0 | D52=0 | E52=0 |
 F52=0 | G52=0 | H52=0 | I52=0 | J52=0 | K52=0 | L52=0 | M52=0 | N52=0 | O52=0 | P52=0 | Q52=0 | R52=0 | S52=0 | T52=0 |
 U52=0 | V52=0 | W52=0
  row 53 [MIXED_NUMERIC n=22 columns=A,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W]: A53='جمع منابع ارزی ' | C53=0 | D53=0
 | E53=0 | F53=0 | G53=0 | H53=0 | I53=0 | J53=0 | K53=0 | L53=0 | M53=0 | N53=0 | O53=0 | P53=0 | Q53=0 | R53=0 | S53=0
 | T53=0 | U53=0 | V53=0 | W53=0
  row 54 [SINGLE_TEXT n=1 columns=A]: A54='مصارف ارزی: '
  row 55 [EMPTY]
  row 56 [MIXED_NUMERIC n=22 columns=A,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W]: A56='سایر ' | C56=0 | D56=0 | E56=0 |
 F56=0 | G56=0 | H56=0 | I56=0 | J56=0 | K56=0 | L56=0 | M56=0 | N56=0 | O56=0 | P56=0 | Q56=0 | R56=0 | S56=0 | T56=0 |
 U56=0 | V56=0 | W56=0
  row 57 [MIXED_NUMERIC n=22 columns=A,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W]: A57='جمع مصارف ارزی ' | C57=0 | D57=0
 | E57=0 | F57=0 | G57=0 | H57=0 | I57=0 | J57=0 | K57=0 | L57=0 | M57=0 | N57=0 | O57=0 | P57=0 | Q57=0 | R57=0 | S57=0
 | T57=0 | U57=0 | V57=0 | W57=0

SUMMARY bands_printed=4 compound_candidates=3

## WORKBOOK excel\fzar2.xlsx
Reader: ACCEPTED
SHA-256: 48272a0a5fe4635b9e7d877bf8748ae5a73cd3a025b1c055fd2ed582ac859a7f

### SHEET 1 Recovered_Sheet1 | used=A1:Z874 | bands=37

[BAND 1] rows=9:10 columns=A,B,C,D,E merges=A9:A10,E9:E10
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=12; gap=SINGLE_TEXT
  row 3 [SINGLE_TEXT n=1 columns=A]: A3='صورت سود و زیان تلفیقی'
  row 4 [EMPTY]
  row 5 [EMPTY]
  row 6 [EMPTY]
  row 7 [EMPTY]
  row 8 [SINGLE_TEXT n=1 columns=A]: A8='صورت سود و زيان تلفيقي'
  row 9 [MULTI_TEXT n=5 columns=A,B,C,D,E]: A9='شرح' | B9='دوره منتهي به ۱۴۰۵/۰۳/۳۱' | C9='تجديد ارائه شده دوره منتهي به
 ۱۴۰۴/۰۳/۳۱' | D9='تجديد ارائه شده دوره منتهي به ۱۴۰۴/۰۹/۳۰' | E9='درصد تغيير'
    MERGES A9:A10,E9:E10
  row 10 [MULTI_TEXT n=3 columns=B,C,D]: B10='حسابرسی شده' | C10='حسابرسی شده' | D10='حسابرسی شده'
    MERGES A9:A10,E9:E10
  row 11 [SINGLE_TEXT n=1 columns=A]: A11='عمليات در حال تداوم: '
  row 12 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A12='درآمدهاي عملياتي ' | B12=48780966 | C12=19317656 | D12=53952825 | E
12=153
  row 13 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A13='بهاى تمام شده درآمدهاي عملياتي ' | B13=-3658393 | C13=-1783279 | D1
3=-5708798 | E13=-105
  row 14 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A14='سود(زيان) ناخالص ' | B14=45122573 | C14=17534377 | D14=48244027 | E
14=157
  row 15 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A15='هزينه \u200fهاى فروش، ادارى و عمومى ' | B15=-1009360 | C15=-468801
| D15=-1381446 | E15=-115
  row 16 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A16='هزينه کاهش ارزش دريافتني\u200fها (هزينه استثنايي) ' | B16=0 | C16=0 |
 D16=0

[BAND 2] rows=60:61 columns=A,B,C,D,E merges=A60:A61,E60:E61
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=62; gap=none
  row 54 [SINGLE_TEXT n=1 columns=A]: A54='صورت سود و زیان جامع تلفیقی'
  row 55 [EMPTY]
  row 56 [EMPTY]
  row 57 [EMPTY]
  row 58 [EMPTY]
  row 59 [SINGLE_TEXT n=1 columns=A]: A59='صورت سود و زيان جامع تلفيقي'
  row 60 [MULTI_TEXT n=5 columns=A,B,C,D,E]: A60='شرح' | B60='دوره منتهي به ۱۴۰۵/۰۳/۳۱' | C60='تجديد ارائه شده دوره منته
ي به ۱۴۰۴/۰۳/۳۱' | D60='تجديد ارائه شده دوره منتهي به ۱۴۰۴/۰۹/۳۰' | E60='درصد تغيير'
    MERGES A60:A61,E60:E61
  row 61 [MULTI_TEXT n=3 columns=B,C,D]: B61='حسابرسی شده' | C61='حسابرسی شده' | D61='حسابرسی شده'
    MERGES A60:A61,E60:E61
  row 62 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A62='سود(زيان) خالص ' | B62=66493934 | C62=19184881 | D62=51084741 | E62
=247
  row 63 [SINGLE_TEXT n=1 columns=A]: A63='ساير اقلام سود و زيان جامع که در دوره هاي آتي به صورت سود و زيان تجد...
  row 64 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A64='مازاد تجديد ارزيابي دارايي\u200cهاي ثابت مشهود ' | B64=0 | C64=0 | D6
4=0
  row 65 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A65='تفاوت تسعير ارز عمليات خارجي ' | B65=0 | C65=0 | D65=0
  row 66 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A66='سهم گروه از ساير اقلام سود و زيان جامع مشارکت هاي خاص ' | B66=0 | C66
=0 | D66=0
  row 67 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A67='سهم گروه از ساير اقلام سود و زيان جامع شرکت هاي وابسته ' | B67=0 | C6
7=0 | D67=0

[BAND 3] rows=92:93 columns=A,B,C,D,E merges=A92:A93,E92:E93
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=96; gap=SINGLE_TEXT,SINGLE_TEXT
  row 86 [SINGLE_TEXT n=1 columns=A]: A86='صورت وضعیت مالی تلفیقی'
  row 87 [EMPTY]
  row 88 [EMPTY]
  row 89 [EMPTY]
  row 90 [EMPTY]
  row 91 [SINGLE_TEXT n=1 columns=A]: A91='صورت وضعيت مالي تلفيقي'
  row 92 [MULTI_TEXT n=5 columns=A,B,C,D,E]: A92='شرح' | B92='به تاريخ ۱۴۰۵/۰۳/۳۱' | C92='تجديد ارائه شده به تاريخ ۱۴۰۴/
۰۹/۳۰' | D92='تجديد ارائه شده به تاريخ ۱۴۰۳/۱۰/۰۱' | E92='درصد تغيير'
    MERGES A92:A93,E92:E93
  row 93 [MULTI_TEXT n=3 columns=B,C,D]: B93='حسابرسی شده' | C93='حسابرسی شده' | D93='حسابرسی شده'
    MERGES A92:A93,E92:E93
  row 94 [SINGLE_TEXT n=1 columns=A]: A94='دارايي\u200cها '
  row 95 [SINGLE_TEXT n=1 columns=A]: A95='دارايي\u200cهاي غيرجاري '
  row 96 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A96='دارايي\u200cهاي ثابت مشهود ' | B96=4980382 | C96=4292782 | D96=4292
782 | E96=16
  row 97 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A97='سرمايه\u200cگذاري در املاک ' | B97=0 | C97=0 | D97=0
  row 98 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A98='سرقفلي ' | B98=0 | C98=0 | D98=0
  row 99 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A99='دارايي\u200cهاي نامشهود ' | B99=36367 | C99=37691 | D99=37691 | E99
=-4

[BAND 4] rows=161:161 columns=A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P merges=—
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=162; gap=none
  row 155 [SINGLE_TEXT n=1 columns=A]: A155='صورت تغییرات در حقوق مالکانه تلفیقی'
  row 156 [EMPTY]
  row 157 [EMPTY]
  row 158 [EMPTY]
  row 159 [EMPTY]
  row 160 [SINGLE_TEXT n=1 columns=A]: A160='صورت تغييرات در حقوق مالکانه تلفيقي'
  row 161 [MULTI_TEXT n=16 columns=A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P]: A161='شرح' | B161='سرمايه' | C161='افزايش سرمايه در
 جريان' | D161='صرف سهام' | E161='صرف سهام خزانه' | F161='آثار معاملات سهام خزانه شرکت فرعي' | G161='آثار معاملات با منا
فع فاقد حق کنترل' | H161='اندوخته قانوني' | I161='ساير اندوخته\u200cها' | J161='مازاد تجديد ارزيابي دارايي\u200cها' | K1
61='تفاوت تسعير ارز عمليات خارجي' | L161='سود انباشته' | M161='سهام خزانه' | N161='قابل انتساب به مالکان شرکت اصلي' | O1
61='منافع فاقد حق کنترل' | P161='جمع حقوق مالکانه'
  row 162 [MIXED_NUMERIC n=16 columns=A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P]: A162='مانده در ۱۴۰۳/۱۰/۰۱ ' | B162=5400000 | C16
2=0 | D162=0 | E162=0 | F162=0 | G162=0 | H162=540000 | I162=0 | J162=0 | K162=0 | L162=31267030 | M162=0 | N162=3720703
0 | O162=627903 | P162=37834933
  row 163 [MIXED_NUMERIC n=14 columns=A,B,C,D,E,H,I,J,K,L,M,N,O,P]: A163='اصلاح اشتباهات ' | B163=0 | C163=0 | D163=0 |
E163=0 | H163=0 | I163=0 | J163=0 | K163=0 | L163=0 | M163=0 | N163=0 | O163=0 | P163=0
  row 164 [MIXED_NUMERIC n=14 columns=A,B,C,D,E,H,I,J,K,L,M,N,O,P]: A164='تغيير در رويه\u200cهاي حسابداري ' | B164=0 | C
164=0 | D164=0 | E164=0 | H164=0 | I164=0 | J164=0 | K164=0 | L164=0 | M164=0 | N164=0 | O164=0 | P164=0
  row 165 [MIXED_NUMERIC n=16 columns=A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P]: A165='مانده تجديد ارائه شده در ۱۴۰۳/۱۰/۰۱ ' | B1
65=5400000 | C165=0 | D165=0 | E165=0 | F165=0 | G165=0 | H165=540000 | I165=0 | J165=0 | K165=0 | L165=31267030 | M165=
0 | N165=37207030 | O165=627903 | P165=37834933
  row 166 [MIXED_NUMERIC n=2 columns=A,P]: A166='تغييرات حقوق مالکانه در سال ۱۴۰۴/۰۹/۳۰ ' | P166=0
  row 167 [MIXED_NUMERIC n=5 columns=A,L,N,O,P]: A167='سود(زيان) خالص گزارش شده در صورت\u200cهاي مالي سال ۱۴۰۴/۰۹/۳۰ ' |
 L167=50150540 | N167=50150540 | O167=934201 | P167=51084741

[BAND 5] rows=217:218 columns=A,B,C,D,E merges=A217:A218,E217:E218
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=220; gap=SINGLE_TEXT
  row 211 [SINGLE_TEXT n=1 columns=A]: A211='صورت جریان های نقدی تلفیقی'
  row 212 [EMPTY]
  row 213 [EMPTY]
  row 214 [EMPTY]
  row 215 [EMPTY]
  row 216 [SINGLE_TEXT n=1 columns=A]: A216='صورت جريان هاي نقدي تلفيقي'
  row 217 [MULTI_TEXT n=5 columns=A,B,C,D,E]: A217='شرح' | B217='دوره منتهي به ۱۴۰۵/۰۳/۳۱' | C217='تجديد ارائه شده دوره
منتهي به ۱۴۰۴/۰۳/۳۱' | D217='تجديد ارائه شده دوره منتهي به ۱۴۰۴/۰۹/۳۰' | E217='درصد تغيير'
    MERGES A217:A218,E217:E218
  row 218 [MULTI_TEXT n=3 columns=B,C,D]: B218='حسابرسی شده' | C218='حسابرسی شده' | D218='حسابرسی شده'
    MERGES A217:A218,E217:E218
  row 219 [SINGLE_TEXT n=1 columns=A]: A219='جريان\xadهاي نقدي حاصل از فعاليت\u200cهاي عملياتي: '
  row 220 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A220='نقد حاصل از عمليات ' | B220=64313762 | C220=12077128 | D220=35372
933 | E220=433
  row 221 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A221='پرداخت\u200cهاي نقدي بابت ماليات بر درآمد ' | B221=-487399 | C221
=-565285 | D221=-756535 | E221=14
  row 222 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A222='جريان \u200cخالص \u200cورود\u200c (خروج) \u200cنقد حاصل از فعاليت
\u2... | B222=63826363 | C222=11511843 | D222=34616398 | E222=454
  row 223 [SINGLE_TEXT n=1 columns=A]: A223='جريان\xadهاي نقدي حاصل از فعاليت\u200cهاي سرمايه\u200cگذاري: '
  row 224 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A224='دريافت\u200cهاي نقدي حاصل از فروش دارايي\u200cهاي ثابت مشهود ' |
B224=3091 | C224=69417 | D224=81023 | E224=-96

[BAND 6] rows=290:291 columns=A,B,C,D,E merges=A290:A291,E290:E291
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=293; gap=SINGLE_TEXT
  row 284 [SINGLE_TEXT n=1 columns=A]: A284='صورت سود و زیان'
  row 285 [EMPTY]
  row 286 [EMPTY]
  row 287 [EMPTY]
  row 288 [EMPTY]
  row 289 [SINGLE_TEXT n=1 columns=A]: A289='صورت سود و زيان'
  row 290 [MULTI_TEXT n=5 columns=A,B,C,D,E]: A290='شرح' | B290='دوره منتهي به ۱۴۰۵/۰۳/۳۱' | C290='تجديد ارائه شده دوره
منتهي به ۱۴۰۴/۰۳/۳۱' | D290='تجديد ارائه شده دوره منتهي به ۱۴۰۴/۰۹/۳۰' | E290='درصد تغيير'
    MERGES A290:A291,E290:E291
  row 291 [MULTI_TEXT n=3 columns=B,C,D]: B291='حسابرسی شده' | C291='حسابرسی شده' | D291='حسابرسی شده'
    MERGES A290:A291,E290:E291
  row 292 [SINGLE_TEXT n=1 columns=A]: A292='عمليات در حال تداوم: '
  row 293 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A293='درآمدهاي عملياتي ' | B293=10608198 | C293=2722392 | D293=22766727
 | E293=290
  row 294 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A294='بهاى تمام شده درآمدهاي عملياتي ' | B294=-7545045 | C294=-1905619
| D294=-13534520 | E294=-296
  row 295 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A295='سود(زيان) ناخالص ' | B295=3063153 | C295=816773 | D295=9232207 |
E295=275
  row 296 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A296='هزينه\u200f هاى فروش، ادارى و عمومى ' | B296=-483863 | C296=-1964
72 | D296=-704278 | E296=-146
  row 297 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A297='هزينه کاهش ارزش دريافتني\u200f ها (هزينه استثنايي) ' | B297=0 | C29
7=0 | D297=0

[BAND 7] rows=336:337 columns=A,B,C,D,E merges=A336:A337,E336:E337
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=338; gap=none
  row 330 [EMPTY]
  row 331 [EMPTY]
  row 332 [EMPTY]
  row 333 [EMPTY]
  row 334 [SINGLE_TEXT n=1 columns=A]: A334='صورت سود و زيان جامع'
  row 335 [SINGLE_TEXT n=1 columns=A]: A335='کليه مبالغ به ميليون ريال است'
  row 336 [MULTI_TEXT n=5 columns=A,B,C,D,E]: A336='شرح' | B336='دوره منتهي به ۱۴۰۵/۰۳/۳۱' | C336='تجديد ارائه شده دوره
منتهي به ۱۴۰۴/۰۳/۳۱' | D336='تجديد ارائه شده دوره منتهي به ۱۴۰۴/۰۹/۳۰' | E336='درصد تغيير'
    MERGES A336:A337,E336:E337
  row 337 [MULTI_TEXT n=3 columns=B,C,D]: B337='حسابرسی شده' | C337='حسابرسی شده' | D337='حسابرسی شده'
    MERGES A336:A337,E336:E337
  row 338 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A338='سود(زيان) خالص ' | B338=1783798 | C338=748773 | D338=50287149 | E
338=138
  row 339 [SINGLE_TEXT n=1 columns=A]: A339='ساير اقلام سود و زيان جامع که در دوره هاي آتي به صورت سود و زيان تجد...
  row 340 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A340='مازاد تجديد ارزيابي دارايي\u200cهاي ثابت مشهود ' | B340=0 | C340=0
| D340=0
  row 341 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A341='تفاوت تسعير ارز عمليات خارجي ' | B341=0 | C341=0 | D341=0
  row 342 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A342='ساير ' | B342=0 | C342=0 | D342=0
  row 343 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A343='ماليات بر درآمد اقلام فوق ' | B343=0 | C343=0 | D343=0

[BAND 8] rows=363:364 columns=A,B,C,D,E merges=A363:A364,E363:E364
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=367; gap=SINGLE_TEXT,SINGLE_TEXT
  row 357 [EMPTY]
  row 358 [EMPTY]
  row 359 [EMPTY]
  row 360 [EMPTY]
  row 361 [SINGLE_TEXT n=1 columns=A]: A361='صورت وضعيت مالي'
  row 362 [SINGLE_TEXT n=1 columns=A]: A362='کليه مبالغ به ميليون ريال است'
  row 363 [MULTI_TEXT n=5 columns=A,B,C,D,E]: A363='شرح' | B363='به تاريخ ۱۴۰۵/۰۳/۳۱' | C363='تجديد ارائه شده به تاريخ ۱
۴۰۴/۰۹/۳۰' | D363='تجديد ارائه شده به تاريخ ۱۴۰۳/۱۰/۰۱' | E363='درصد تغيير'
    MERGES A363:A364,E363:E364
  row 364 [MULTI_TEXT n=3 columns=B,C,D]: B364='حسابرسی شده' | C364='حسابرسی شده' | D364='حسابرسی شده'
    MERGES A363:A364,E363:E364
  row 365 [SINGLE_TEXT n=1 columns=A]: A365='دارايي\u200cها '
  row 366 [SINGLE_TEXT n=1 columns=A]: A366='دارايي\u200cهاي غيرجاري '
  row 367 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A367='دارايي\u200cهاي ثابت مشهود ' | B367=3477297 | C367=2846056 | D367
=2348091 | E367=22
  row 368 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A368='سرمايه\u200cگذاري در املاک ' | B368=0 | C368=0 | D368=0
  row 369 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A369='دارايي\u200cهاي نامشهود ' | B369=12806 | C369=11921 | D369=14494
| E369=7
  row 370 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A370='سرمايه\u200cگذاري\u200cهاي بلندمدت ' | B370=3594676 | C370=359467
6 | D370=2594696 | E370=0

[BAND 9] rows=427:427 columns=A,B,C,D,E,F,G,H,I,J,K,L merges=—
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=428; gap=none
  row 421 [EMPTY]
  row 422 [EMPTY]
  row 423 [EMPTY]
  row 424 [EMPTY]
  row 425 [SINGLE_TEXT n=1 columns=A]: A425='صورت تغييرات در حقوق مالکانه'
  row 426 [SINGLE_TEXT n=1 columns=A]: A426='کليه مبالغ به ميليون ريال است'
  row 427 [MULTI_TEXT n=12 columns=A,B,C,D,E,F,G,H,I,J,K,L]: A427='شرح' | B427='سرمايه' | C427='افزايش سرمايه در جريان'
| D427='صرف سهام' | E427='صرف سهام خزانه' | F427='اندوخته قانوني' | G427='ساير اندوخته\u200cها' | H427='مازاد تجديد ارزي
ابي دارايي\u200cها' | I427='تفاوت تسعير ارز عمليات خارجي' | J427='سود انباشته' | K427='سهام خزانه' | L427='جمع کل'
  row 428 [MIXED_NUMERIC n=12 columns=A,B,C,D,E,F,G,H,I,J,K,L]: A428='مانده در ۱۴۰۳/۱۰/۰۱ ' | B428=5400000 | C428=0 | D4
28=0 | E428=0 | F428=540000 | G428=0 | H428=0 | I428=0 | J428=31427418 | K428=0 | L428=37367418
  row 429 [MIXED_NUMERIC n=12 columns=A,B,C,D,E,F,G,H,I,J,K,L]: A429='اصلاح اشتباهات ' | B429=0 | C429=0 | D429=0 | E429
=0 | F429=0 | G429=0 | H429=0 | I429=0 | J429=0 | K429=0 | L429=0
  row 430 [MIXED_NUMERIC n=12 columns=A,B,C,D,E,F,G,H,I,J,K,L]: A430='تغيير در رويه\u200cهاي حسابداري ' | B430=0 | C430=
0 | D430=0 | E430=0 | F430=0 | G430=0 | H430=0 | I430=0 | J430=0 | K430=0 | L430=0
  row 431 [MIXED_NUMERIC n=12 columns=A,B,C,D,E,F,G,H,I,J,K,L]: A431='مانده تجديد ارائه شده در ۱۴۰۳/۱۰/۰۱ ' | B431=54000
00 | C431=0 | D431=0 | E431=0 | F431=540000 | G431=0 | H431=0 | I431=0 | J431=31427418 | K431=0 | L431=37367418
  row 432 [SINGLE_TEXT n=1 columns=A]: A432='تغييرات حقوق مالکانه در سال ۱۴۰۴/۰۹/۳۰ '
  row 433 [MIXED_NUMERIC n=3 columns=A,J,L]: A433='سود(زيان) خالص گزارش شده در صورت\u200cهاي مالي سال ۱۴۰۴/۰۹/۳۰ ' | J43
3=50287149 | L433=50287149

[BAND 10] rows=471:472 columns=A,B,C,D,E merges=A471:A472,E471:E472
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=474; gap=SINGLE_TEXT
  row 465 [EMPTY]
  row 466 [EMPTY]
  row 467 [EMPTY]
  row 468 [EMPTY]
  row 469 [SINGLE_TEXT n=1 columns=A]: A469='صورت جريان\u200cهاي نقدي'
  row 470 [SINGLE_TEXT n=1 columns=A]: A470='کليه مبالغ به ميليون ريال است'
  row 471 [MULTI_TEXT n=5 columns=A,B,C,D,E]: A471='شرح' | B471='دوره منتهي به ۱۴۰۵/۰۳/۳۱' | C471='تجديد ارائه شده دوره
منتهي به ۱۴۰۴/۰۳/۳۱' | D471='تجديد ارائه شده دوره منتهي به ۱۴۰۴/۰۹/۳۰' | E471='درصد تغيير'
    MERGES A471:A472,E471:E472
  row 472 [MULTI_TEXT n=3 columns=B,C,D]: B472='حسابرسی شده' | C472='حسابرسی شده' | D472='حسابرسی شده'
    MERGES A471:A472,E471:E472
  row 473 [SINGLE_TEXT n=1 columns=A]: A473='جريان\xadهاي نقدي حاصل از فعاليت\u200cهاي عملياتي: '
  row 474 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A474='نقد حاصل از عمليات ' | B474=49733213 | C474=9807563 | D474=276921
27 | E474=407
  row 475 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A475='پرداخت\u200cهاي نقدي بابت ماليات بر درآمد ' | B475=-176166 | C475
=-10610 | D475=-10610 | E475=-1560
  row 476 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A476='جريان \u200cخالص \u200cورود\u200c (خروج) \u200cنقد حاصل از فعاليت
\u2... | B476=49557047 | C476=9796953 | D476=27681517 | E476=406
  row 477 [SINGLE_TEXT n=1 columns=A]: A477='جريان\xadهاي نقدي حاصل از فعاليت\u200cهاي سرمايه\u200cگذاري: '
  row 478 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A478='دريافت\u200cهاي نقدي حاصل از فروش دارايي\u200cهاي ثابت مشهود ' |
B478=0 | C478=69417 | D478=73650 | E478='-- '

[BAND 11] rows=536:537 columns=A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V merges=A536:A537,B536:B537,C536:C537,D536:D53
7,E536:F536,G536:L536,M536:R536,S536:V536
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=539; gap=SINGLE_TEXT
  row 530 [EMPTY]
  row 531 [EMPTY]
  row 532 [EMPTY]
  row 533 [SINGLE_TEXT n=1 columns=A]: A533='اطلاعات این فرم گزیده ای از اطلاعات گزارش تفسیری مدیریت می باشد که ه...
    MERGES A533:Z533
  row 534 [SINGLE_TEXT n=1 columns=A]: A534='درآمدهای عملیاتی و بهای تمام شده'
  row 535 [SINGLE_TEXT n=1 columns=A]: A535='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 536 [MULTI_TEXT n=8 columns=A,B,C,D,E,G,M,S]: A536='نوع کالا' | B536='واحد' | C536='ظرفیت عملی' | D536='مبانی و مر
جع قیمت گذاری' | E536='دوره ۶ ماهه منتهی به ۱۴۰۴/۰۳/۳۱' | G536='سال مالی منتهی به ۱۴۰۴/۰۹/۳۰' | M536='دوره ۶ ماهه منتهی
به ۱۴۰۵/۰۳/۳۱' | S536='برآورد دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰'
    MERGES A536:A537,B536:B537,C536:C537,D536:D537,E536:F536,G536:L536,M536:R536,S536:V536
  row 537 [MULTI_TEXT n=18 columns=E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V]: E537='تعداد فروش' | F537='مبلغ فروش' | G537='تع
داد تولید' | H537='تعداد فروش' | I537='نرخ فروش' | J537='مبلغ فروش' | K537='مبلغ بهای تمام شده' | L537='سود ناخالص' | M5
37='تعداد تولید' | N537='تعداد فروش' | O537='نرخ فروش' | P537='مبلغ فروش' | Q537='مبلغ بهای تمام شده' | R537='سود ناخالص
' | S537='تعداد تولید' | T537='تعداد فروش' | U537='نرخ فروش' | V537='مبلغ فروش'
    MERGES A536:A537,B536:B537,C536:C537,D536:D537
  row 538 [SINGLE_TEXT n=1 columns=A]: A538='فروش داخلي: '
  row 539 [MIXED_NUMERIC n=20 columns=A,B,C,D,E,F,G,H,I,J,K,L,M,N,P,Q,R,S,T,V]: A539='استخراج کانسنگ طلا با عيار ۱/۱۸ گر
م بر تن ' | B539='تن ' | C539=715000 | D539='سایر ' | E539=66545 | F539=1363653 | G539=515000 | H539=520154.18 | I539=28
256951 | J539=14697971 | K539=-9095571 | L539=5602400 | M539=0 | N539=0 | P539=0 | Q539=0 | R539=0 | S539=0 | T539=0 | V
539=0
  row 540 [MIXED_NUMERIC n=22 columns=A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V]: A540='برداشت کانسنگ طلا با عيار ۰/۳۷
۵۹ گرم بر تن از محل باطله سنوات قبل ' | B540='تن ' | C540=0 | D540='سایر ' | E540=6513468 | F540=1296635 | G540=373492 |
 H540=373492.62 | I540=6840855 | J540=2555009 | K540=-1582991 | L540=972018 | M540=146383 | N540=146383.28 | O540=176484
98 | P540=2583445 | Q540=-1718365 | R540=865080 | S540=403617 | T540=403617 | U540=15112954 | V540=6099845
  row 541 [MIXED_NUMERIC n=20 columns=A,B,C,D,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V]: A541='استخراج سنگ تراورتن شکلاتي درجه ۳
' | B541='تن ' | C541=9100 | D541='سایر ' | G541=3833 | H541=884.45 | I541=24999717 | J541=22111 | K541=-6633 | L541=154
78 | M541=158 | N541=613 | O541=25001631 | P541=15326 | Q541=-11363 | R541=3963 | S541=3675 | T541=271 | U541=25036900 |
 V541=6785
  row 542 [MIXED_NUMERIC n=21 columns=A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,V]: A542='انواع سنگ پلاک تراورتن شکلاتي در
جه ۳ ' | B542='متر مربع ' | C542=0 | D542='سایر ' | E542=9404752 | F542=62104 | G542=19490 | H542=11648.51 | I542=895556
6 | J542=104319 | K542=-82905 | L542=21414 | M542=0 | N542=316 | O542=21000000 | P542=6636 | Q542=-2084 | R542=4552 | S5
42=0 | T542=0 | V542=0
  row 543 [MIXED_NUMERIC n=20 columns=A,B,C,D,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V]: A543='استخراج کانسنگ طلا با عيار ۱/۲۵ گر
م بر تن ' | B543='تن ' | C543=723000 | D543='سایر ' | G543=204000 | H543=139727.94 | I543=38555761 | J543=5387317 | K543
=-2766420 | L543=2620897 | M543=206500 | N543=135203.39 | O543=59190757 | P543=8002791 | Q543=-5813233 | R543=2189558 |
S543=516500 | T543=264797 | U543=49083672 | V543=12997209

[BAND 12] rows=556:556 columns=A,B,C,D,E,F,G,H merges=—
  SIGNATURE=COMPOUND_CANDIDATE
  PRIOR prior_body=553; gap=SINGLE_TEXT,SINGLE_TEXT
  FOLLOWING next_body=557; gap=none
  row 550 [EMPTY]
  row 551 [MIXED_NUMERIC n=16 columns=A,E,F,G,H,J,K,L,M,N,P,Q,R,S,T,V]: A551='جمع درآمد ارائه خدمات ' | E551=0 | F551=0
| G551=0 | H551=0 | J551=0 | K551=0 | L551=0 | M551=0 | N551=0 | P551=0 | Q551=0 | R551=0 | S551=0 | T551=0 | V551=0
  row 552 [MIXED_NUMERIC n=8 columns=A,G,K,L,M,Q,R,S]: A552='ساير ' | G552=0 | K552=0 | L552=0 | M552=0 | Q552=0 | R552=
0 | S552=0
  row 553 [MIXED_NUMERIC n=16 columns=A,E,F,G,H,J,K,L,M,N,P,Q,R,S,T,V]: A553='جمع ' | E553=15984765 | F553=2722392 | G55
3=1115815 | H553=1045907.7 | J553=22766727 | K553=-13534520 | L553=9232207 | M553=353041 | N553=282515.67 | P553=1060819
8 | Q553=-7545045 | R553=3063153 | S553=923792 | T553=668685 | V553=19103839
  row 554 [SINGLE_TEXT n=1 columns=A]: A554='روند فروش و بهای تمام شده در 5 سال اخیر'
  row 555 [SINGLE_TEXT n=1 columns=A]: A555='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 556 [MULTI_TEXT n=8 columns=A,B,C,D,E,F,G,H]: A556='شرح' | B556='سال مالی ۱۴۰۰/۱۲/۲۹' | C556='سال مالی ۱۴۰۱/۰۹/۳۰'
 | D556='سال مالی ۱۴۰۲/۰۹/۳۰' | E556='سال مالی ۱۴۰۳/۰۹/۳۰' | F556='سال مالی ۱۴۰۴/۰۹/۳۰' | G556='سال مالی ۱۴۰۵/۰۳/۳۱' | H
556='برآورد دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰'
  row 557 [MIXED_NUMERIC n=8 columns=A,B,C,D,E,F,G,H]: A557='مبلغ فروش ' | B557=2072332 | C557=3057063 | D557=5441333 |
E557=11618949 | F557=22766727 | G557=10608198 | H557=19103839
  row 558 [MIXED_NUMERIC n=8 columns=A,B,C,D,E,F,G,H]: A558='مبلغ بهای تمام شده ' | B558=-1444346 | C558=-2032841 | D558
=-3106672 | E558=-6482191 | F558=-13534520 | G558=-7545045 | H558=-8574690
  row 559 [SINGLE_TEXT n=1 columns=A]: A559='اهداف و راهبردهای آتی مدیریت در خصوص تولید و فروش محصولات'
  row 560 [SINGLE_TEXT n=1 columns=A]: A560='تمامی تولیدات شرکت بر اساس قرارداد بلند مدت به شرکت استحصال مواد معد...
    MERGES A560:K560
  row 561 [SINGLE_TEXT n=1 columns=A]: A561='برآورد شرکت از تغییرات نرخ فروش محصولات'
  row 562 [MULTI_TEXT n=3 columns=A,B,C]: A562='نرخ فروش محصولات ' | B562='برآورد دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰ ' | C5
62='نرخ فروش کانسنگ بر اساس قرارداد فی ما بین با شرکت استحصال مواد معدنی...
    MERGES C562:K562

[BAND 13] rows=562:562 columns=A,B,C merges=C562:K562
  SIGNATURE=NO_MATCH
  PRIOR prior_body=558; gap=SINGLE_TEXT,SINGLE_TEXT,SINGLE_TEXT
  FOLLOWING next_body=567; gap=EMPTY,SINGLE_TEXT,SINGLE_TEXT,MULTI_TEXT
  row 556 [MULTI_TEXT n=8 columns=A,B,C,D,E,F,G,H]: A556='شرح' | B556='سال مالی ۱۴۰۰/۱۲/۲۹' | C556='سال مالی ۱۴۰۱/۰۹/۳۰'
 | D556='سال مالی ۱۴۰۲/۰۹/۳۰' | E556='سال مالی ۱۴۰۳/۰۹/۳۰' | F556='سال مالی ۱۴۰۴/۰۹/۳۰' | G556='سال مالی ۱۴۰۵/۰۳/۳۱' | H
556='برآورد دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰'
  row 557 [MIXED_NUMERIC n=8 columns=A,B,C,D,E,F,G,H]: A557='مبلغ فروش ' | B557=2072332 | C557=3057063 | D557=5441333 |
E557=11618949 | F557=22766727 | G557=10608198 | H557=19103839
  row 558 [MIXED_NUMERIC n=8 columns=A,B,C,D,E,F,G,H]: A558='مبلغ بهای تمام شده ' | B558=-1444346 | C558=-2032841 | D558
=-3106672 | E558=-6482191 | F558=-13534520 | G558=-7545045 | H558=-8574690
  row 559 [SINGLE_TEXT n=1 columns=A]: A559='اهداف و راهبردهای آتی مدیریت در خصوص تولید و فروش محصولات'
  row 560 [SINGLE_TEXT n=1 columns=A]: A560='تمامی تولیدات شرکت بر اساس قرارداد بلند مدت به شرکت استحصال مواد معد...
    MERGES A560:K560
  row 561 [SINGLE_TEXT n=1 columns=A]: A561='برآورد شرکت از تغییرات نرخ فروش محصولات'
  row 562 [MULTI_TEXT n=3 columns=A,B,C]: A562='نرخ فروش محصولات ' | B562='برآورد دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰ ' | C5
62='نرخ فروش کانسنگ بر اساس قرارداد فی ما بین با شرکت استحصال مواد معدنی...
    MERGES C562:K562
  row 563 [EMPTY]
  row 564 [SINGLE_TEXT n=1 columns=A]: A564='بهای تمام شده'
  row 565 [SINGLE_TEXT n=1 columns=A]: A565='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 566 [MULTI_TEXT n=4 columns=A,B,C,D]: A566='شرح' | B566='سال مالی منتهی به ۱۴۰۴/۰۹/۳۰ (میلیون ریال)' | C566='دوره
۶ ماهه منتهی به ۱۴۰۵/۰۳/۳۱ (میلیون ریال)' | D566='برآورد دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰'
  row 567 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A567='مواد مستقیم مصرفی ' | B567=0 | C567=0 | D567=0
  row 568 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A568='دستمزدمستقيم توليد ' | B568=2216300 | C568=1079645 | D568=1966034

[BAND 14] rows=566:566 columns=A,B,C,D merges=—
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=567; gap=none
  row 560 [SINGLE_TEXT n=1 columns=A]: A560='تمامی تولیدات شرکت بر اساس قرارداد بلند مدت به شرکت استحصال مواد معد...
    MERGES A560:K560
  row 561 [SINGLE_TEXT n=1 columns=A]: A561='برآورد شرکت از تغییرات نرخ فروش محصولات'
  row 562 [MULTI_TEXT n=3 columns=A,B,C]: A562='نرخ فروش محصولات ' | B562='برآورد دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰ ' | C5
62='نرخ فروش کانسنگ بر اساس قرارداد فی ما بین با شرکت استحصال مواد معدنی...
    MERGES C562:K562
  row 563 [EMPTY]
  row 564 [SINGLE_TEXT n=1 columns=A]: A564='بهای تمام شده'
  row 565 [SINGLE_TEXT n=1 columns=A]: A565='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 566 [MULTI_TEXT n=4 columns=A,B,C,D]: A566='شرح' | B566='سال مالی منتهی به ۱۴۰۴/۰۹/۳۰ (میلیون ریال)' | C566='دوره
۶ ماهه منتهی به ۱۴۰۵/۰۳/۳۱ (میلیون ریال)' | D566='برآورد دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰'
  row 567 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A567='مواد مستقیم مصرفی ' | B567=0 | C567=0 | D567=0
  row 568 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A568='دستمزدمستقيم توليد ' | B568=2216300 | C568=1079645 | D568=1966034
  row 569 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A569='سربارتوليد ' | B569=11782789 | C569=7326409 | D569=8695590
  row 570 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A570='جمع ' | B570=13999089 | C570=8406054 | D570=10661624
  row 571 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A571='هزينه جذب نشده درتوليد ' | B571=0 | C571=0 | D571=0
  row 572 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A572='جمع هزينه هاي توليد ' | B572=13999089 | C572=8406054 | D572=1066162
4

[BAND 15] rows=582:582 columns=A,B merges=B582:J582
  SIGNATURE=NO_MATCH
  PRIOR prior_body=580; gap=SINGLE_TEXT
  FOLLOWING next_body=None; gap=none
  row 576 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A576='موجودي كالاي ساخته شده اول دوره ' | B576=65767 | C576=530336 | D576
=1391345
  row 577 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A577='موجودي كالاي ساخته شده پايان دوره ' | B577=-530336 | C577=-1391345
| D577=-3478279
  row 578 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A578='بهاي تمام شده كالاي فروش رفته ' | B578=13534520 | C578=7545045 | D5
78=8574690
  row 579 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A579='بهاي تمام شده خدمات ارایه شده ' | B579=0 | C579=0 | D579=0
  row 580 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A580='جمع بهای تمام شده ' | B580=13534520 | C580=7545045 | D580=8574690
  row 581 [SINGLE_TEXT n=1 columns=A]: A581='برآورد شرکت از تغییرات عوامل بهای تمام شده'
  row 582 [MULTI_TEXT n=2 columns=A,B]: A582='برآورد دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰ ' | B582='انتظار می رود بهای تمام ش
ده تولید معادل نرخ تورم و افزایش حجم تولیدا...
    MERGES B582:J582
  row 583 [EMPTY]
  row 584 [SINGLE_TEXT n=1 columns=A]: A584='«جملات آینده\u200cنگر نشان\u200cدهنده انتظارات، باورها یا پیش\u200cب...
    MERGES A584:T584
  row 585 [EMPTY]
  row 586 [EMPTY]
  row 587 [EMPTY]
  row 588 [SINGLE_TEXT n=1 columns=A]: A588='خلاصه اطلاعات گزارش تفسیری - صفحه 2'

[BAND 16] rows=595:597 columns=A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q merges=A595:A597,B595:B597,C595:Q595,C596:E596,F596:H59
6,I596:K596,L596:N596,O596:Q596
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=598; gap=none
  row 589 [EMPTY]
  row 590 [EMPTY]
  row 591 [EMPTY]
  row 592 [EMPTY]
  row 593 [SINGLE_TEXT n=1 columns=A]: A593='اطلاعات این فرم گزیده ای از اطلاعات گزارش تفسیری مدیریت می باشد که ه...
    MERGES A593:T593
  row 594 [SINGLE_TEXT n=1 columns=A]: A594='گردش مقداری - ریالی موجودی کالا'
  row 595 [MULTI_TEXT n=3 columns=A,B,C]: A595='شرح محصول' | B595='واحد' | C595='دوره ۶ ماهه منتهی به ۱۴۰۵/۰۳/۳۱'
    MERGES A595:A597,B595:B597,C595:Q595
  row 596 [MULTI_TEXT n=5 columns=C,F,I,L,O]: C596='موجودي اول دوره' | F596='تولید' | I596='تعدیلات' | L596='فروش' | O59
6='موجودی پایان دوره'
    MERGES A595:A597,B595:B597,C596:E596,F596:H596,I596:K596,L596:N596,O596:Q596
  row 597 [MULTI_TEXT n=15 columns=C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q]: C597='مقدار' | D597='نرخ - ریال' | E597='بهای تمام شد
ه - میلیون ریال' | F597='مقدار' | G597='نرخ - ریال' | H597='بهای تمام شده - میلیون ریال' | I597='مقدار' | J597='نرخ - ری
ال' | K597='بهای تمام شده - میلیون ریال' | L597='مقدار' | M597='نرخ - ریال' | N597='بهای تمام شده - میلیون ریال' | O597=
'مقدار' | P597='نرخ - ریال' | Q597='بهای تمام شده - میلیون ریال'
    MERGES A595:A597,B595:B597
  row 598 [MIXED_NUMERIC n=14 columns=A,B,C,E,F,G,H,I,K,L,M,N,O,Q]: A598='برداشت کانسنگ طلا با عيار ۰/۳۷۵۹ گرم بر تن از
محل باطله سنوات قبل ' | B598='تن ' | C598=0 | E598=0 | F598=146383 | G598=11738829 | H598=1718365 | I598=0 | K598=0 | L5
98=146383 | M598=11738829 | N598=1718365 | O598=0 | Q598=0
  row 599 [MIXED_NUMERIC n=16 columns=A,B,C,D,E,F,G,H,I,K,L,M,N,O,P,Q]: A599='استخراج کانسنگ طلا با عيار ۱/۲۵ گرم بر تن
' | B599='تن ' | C599=64272 | D599=7014330 | E599=450825 | F599=206500 | G599=32324688 | H599=6675048 | I599=0 | K599=0
| L599=135203 | M599=42996331 | N599=5813233 | O599=135569 | P599=9682450 | Q599=1312640
  row 600 [MIXED_NUMERIC n=15 columns=A,B,C,D,E,F,H,I,K,L,M,N,O,P,Q]: A600='انواع سنگ پلاک تراورتن شکلاتي درجه ۳ ' | B60
0='متر مربع ' | C600=12145 | D600=5892137 | E600=71560 | F600=0 | H600=0 | I600=0 | K600=0 | L600=316 | M600=6594937 | N
600=2084 | O600=11829 | P600=5873362 | Q600=69476
  row 601 [MIXED_NUMERIC n=16 columns=A,B,C,D,E,F,G,H,I,K,L,M,N,O,P,Q]: A601='استخراج سنگ تراورتن شکلاتي درجه ۳ ' | B601
='تن ' | C601=952 | D601=8351891 | E601=7951 | F601=158 | G601=80006329 | H601=12641 | I601=0 | K601=0 | L601=613 | M601
=18536705 | N601=11363 | O601=497 | P601=18569416 | Q601=9229
  row 602 [EMPTY]
  row 603 [MIXED_NUMERIC n=6 columns=A,E,H,K,N,Q]: A603='جمع كـل ' | E603=530336 | H603=8406054 | K603=0 | N603=7545045
| Q603=1391345

[BAND 17] rows=605:607 columns=A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q merges=A605:A607,B605:B607,C605:Q605,C606:E606,F606:H60
6,I606:K606,L606:N606,O606:Q606
  SIGNATURE=COMPOUND_CANDIDATE
  PRIOR prior_body=603; gap=SINGLE_TEXT
  FOLLOWING next_body=608; gap=none
  row 599 [MIXED_NUMERIC n=16 columns=A,B,C,D,E,F,G,H,I,K,L,M,N,O,P,Q]: A599='استخراج کانسنگ طلا با عيار ۱/۲۵ گرم بر تن
' | B599='تن ' | C599=64272 | D599=7014330 | E599=450825 | F599=206500 | G599=32324688 | H599=6675048 | I599=0 | K599=0
| L599=135203 | M599=42996331 | N599=5813233 | O599=135569 | P599=9682450 | Q599=1312640
  row 600 [MIXED_NUMERIC n=15 columns=A,B,C,D,E,F,H,I,K,L,M,N,O,P,Q]: A600='انواع سنگ پلاک تراورتن شکلاتي درجه ۳ ' | B60
0='متر مربع ' | C600=12145 | D600=5892137 | E600=71560 | F600=0 | H600=0 | I600=0 | K600=0 | L600=316 | M600=6594937 | N
600=2084 | O600=11829 | P600=5873362 | Q600=69476
  row 601 [MIXED_NUMERIC n=16 columns=A,B,C,D,E,F,G,H,I,K,L,M,N,O,P,Q]: A601='استخراج سنگ تراورتن شکلاتي درجه ۳ ' | B601
='تن ' | C601=952 | D601=8351891 | E601=7951 | F601=158 | G601=80006329 | H601=12641 | I601=0 | K601=0 | L601=613 | M601
=18536705 | N601=11363 | O601=497 | P601=18569416 | Q601=9229
  row 602 [EMPTY]
  row 603 [MIXED_NUMERIC n=6 columns=A,E,H,K,N,Q]: A603='جمع كـل ' | E603=530336 | H603=8406054 | K603=0 | N603=7545045
| Q603=1391345
  row 604 [SINGLE_TEXT n=1 columns=A]: A604='گردش مقداری - ریالی موجودی کالا (برآوردی)'
  row 605 [MULTI_TEXT n=3 columns=A,B,C]: A605='شرح محصول' | B605='واحد' | C605='برآورد دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰'

    MERGES A605:A607,B605:B607,C605:Q605
  row 606 [MULTI_TEXT n=5 columns=C,F,I,L,O]: C606='موجودي اول دوره' | F606='تولید' | I606='تعدیلات' | L606='فروش' | O60
6='موجودی پایان دوره'
    MERGES A605:A607,B605:B607,C606:E606,F606:H606,I606:K606,L606:N606,O606:Q606
  row 607 [MULTI_TEXT n=15 columns=C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q]: C607='مقدار' | D607='نرخ - ریال' | E607='بهای تمام شد
ه - میلیون ریال' | F607='مقدار' | G607='نرخ - ریال' | H607='بهای تمام شده - میلیون ریال' | I607='مقدار' | J607='نرخ - ری
ال' | K607='بهای تمام شده - میلیون ریال' | L607='مقدار' | M607='نرخ - ریال' | N607='بهای تمام شده - میلیون ریال' | O607=
'مقدار' | P607='نرخ - ریال' | Q607='بهای تمام شده - میلیون ریال'
    MERGES A605:A607,B605:B607
  row 608 [MIXED_NUMERIC n=17 columns=A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q]: A608='برداشت کانسنگ طلا با عيار ۰/۳۷۵۹ گرم بر
تن از محل باطله سنوات قبل ' | B608='تن ' | C608=0 | D608=0 | E608=0 | F608=403617 | G608=5918083 | H608=2388639 | I608=0
 | J608=0 | K608=0 | L608=403617 | M608=5918083 | N608=2388639 | O608=0 | P608=0 | Q608=0
  row 609 [MIXED_NUMERIC n=17 columns=A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q]: A609='استخراج کانسنگ طلا با عيار ۱/۲۵ گرم بر ت
ن ' | B609='تن ' | C609=135569 | D609=9682450 | E609=1312640 | F609=193500 | G609=42174708 | H609=8160806 | I609=0 | J60
9=0 | K609=0 | L609=264797 | M609=23361484 | N609=6186051 | O609=64272 | P609=51148167 | Q609=3287395
  row 610 [MIXED_NUMERIC n=17 columns=A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q]: A610='انواع سنگ پلاک تراورتن شکلاتي درجه ۳ ' |
 B610='متر مربع ' | C610=11829 | D610=5873362 | E610=69476 | F610=0 | G610=0 | H610=0 | I610=0 | J610=0 | K610=0 | L610=
0 | M610=0 | N610=0 | O610=11829 | P610=5873362 | Q610=69476
  row 611 [MIXED_NUMERIC n=17 columns=A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q]: A611='استخراج سنگ تراورتن شکلاتي درجه ۳ ' | B6
11='تن ' | C611=497 | D611=18569416 | E611=9229 | F611=3675 | G611=30524898 | H611=112179 | I611=0 | J611=0 | K611=0 | L
611=0 | M611=0 | N611=0 | O611=4172 | P611=29100671 | Q611=121408
  row 612 [EMPTY]
  row 613 [MIXED_NUMERIC n=6 columns=A,E,H,K,N,Q]: A613='جمع كـل ' | E613=1391345 | H613=10661624 | K613=0 | N613=857469
0 | Q613=3478279

[BAND 18] rows=620:623 columns=A,B,C,D,E,F,G,H,I,J,K,L,M,N merges=A620:A623,B620:B623,C620:N620,C621:E621,F621:H621,I621
:K621,L621:N621
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=626; gap=SINGLE_TEXT,EMPTY
  row 614 [SINGLE_TEXT n=1 columns=A]: A614='گردش مقداری - ریالی موجودی کالا (برآوردی پایان سال آینده)'
  row 615 [EMPTY]
  row 616 [EMPTY]
  row 617 [EMPTY]
  row 618 [EMPTY]
  row 619 [SINGLE_TEXT n=1 columns=A]: A619='خرید و مصرف مواد اولیه'
  row 620 [MULTI_TEXT n=3 columns=A,B,C]: A620='شرح' | B620='واحد' | C620='دوره ۶ ماهه منتهی به ۱۴۰۵/۰۳/۳۱'
    MERGES A620:A623,B620:B623,C620:N620
  row 621 [MULTI_TEXT n=4 columns=C,F,I,L]: C621='موجودي اول دوره' | F621='خريد طي دوره' | I621='مصرف' | L621='موجودی پا
یان دوره'
    MERGES A620:A623,B620:B623,C621:E621,F621:H621,I621:K621,L621:N621
  row 622 [MULTI_TEXT n=12 columns=C,D,E,F,G,H,I,J,K,L,M,N]: C622='مقدار' | D622='نرخ' | E622='مبلغ' | F622='مقدار' | G6
22='نرخ' | H622='مبلغ' | I622='مقدار' | J622='نرخ' | K622='مبلغ' | L622='مقدار' | M622='نرخ' | N622='مبلغ'
    MERGES A620:A623,B620:B623
  row 623 [MULTI_TEXT n=8 columns=D,E,G,H,J,K,M,N]: D623='ریال' | E623='میلیون ریال' | G623='ریال' | H623='میلیون ریال'
| J623='ریال' | K623='میلیون ریال' | M623='ریال' | N623='میلیون ریال'
    MERGES A620:A623,B620:B623
  row 624 [SINGLE_TEXT n=1 columns=A]: A624='مواد اولیه داخلی: '
  row 625 [EMPTY]
  row 626 [MIXED_NUMERIC n=5 columns=A,E,H,K,N]: A626='جمع مواد اولیه داخلی ' | E626=0 | H626=0 | K626=0 | N626=0
  row 627 [SINGLE_TEXT n=1 columns=A]: A627='مواد اولیه وارداتی: '
  row 628 [EMPTY]
  row 629 [MIXED_NUMERIC n=5 columns=A,E,H,K,N]: A629='جمع مواد اولیه وارداتی ' | E629=0 | H629=0 | K629=0 | N629=0

[BAND 19] rows=632:635 columns=A,B,C,D,E,F,G,H,I,J,K,L,M,N merges=A632:A635,B632:B635,C632:N632,C633:E633,F633:H633,I633
:K633,L633:N633
  SIGNATURE=COMPOUND_CANDIDATE
  PRIOR prior_body=630; gap=SINGLE_TEXT
  FOLLOWING next_body=638; gap=SINGLE_TEXT,EMPTY
  row 626 [MIXED_NUMERIC n=5 columns=A,E,H,K,N]: A626='جمع مواد اولیه داخلی ' | E626=0 | H626=0 | K626=0 | N626=0
  row 627 [SINGLE_TEXT n=1 columns=A]: A627='مواد اولیه وارداتی: '
  row 628 [EMPTY]
  row 629 [MIXED_NUMERIC n=5 columns=A,E,H,K,N]: A629='جمع مواد اولیه وارداتی ' | E629=0 | H629=0 | K629=0 | N629=0
  row 630 [MIXED_NUMERIC n=5 columns=A,E,H,K,N]: A630='جمع كـل ' | E630=0 | H630=0 | K630=0 | N630=0
  row 631 [SINGLE_TEXT n=1 columns=A]: A631='خرید و مصرف مواد اولیه (برآوردی)'
  row 632 [MULTI_TEXT n=3 columns=A,B,C]: A632='شرح' | B632='واحد' | C632='برآورد دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰'
    MERGES A632:A635,B632:B635,C632:N632
  row 633 [MULTI_TEXT n=4 columns=C,F,I,L]: C633='موجودي اول دوره' | F633='خريد طي دوره' | I633='مصرف' | L633='موجودی پا
یان دوره'
    MERGES A632:A635,B632:B635,C633:E633,F633:H633,I633:K633,L633:N633
  row 634 [MULTI_TEXT n=12 columns=C,D,E,F,G,H,I,J,K,L,M,N]: C634='مقدار' | D634='نرخ' | E634='مبلغ' | F634='مقدار' | G6
34='نرخ' | H634='مبلغ' | I634='مقدار' | J634='نرخ' | K634='مبلغ' | L634='مقدار' | M634='نرخ' | N634='مبلغ'
    MERGES A632:A635,B632:B635
  row 635 [MULTI_TEXT n=8 columns=D,E,G,H,J,K,M,N]: D635='ریال' | E635='میلیون ریال' | G635='ریال' | H635='میلیون ریال'
| J635='ریال' | K635='میلیون ریال' | M635='ریال' | N635='میلیون ریال'
    MERGES A632:A635,B632:B635
  row 636 [SINGLE_TEXT n=1 columns=A]: A636='مواد اولیه داخلی: '
  row 637 [EMPTY]
  row 638 [MIXED_NUMERIC n=5 columns=A,E,H,K,N]: A638='جمع مواد اولیه داخلی ' | E638=0 | H638=0 | K638=0 | N638=0
  row 639 [SINGLE_TEXT n=1 columns=A]: A639='مواد اولیه وارداتی: '
  row 640 [EMPTY]
  row 641 [MIXED_NUMERIC n=5 columns=A,E,H,K,N]: A641='جمع مواد اولیه وارداتی ' | E641=0 | H641=0 | K641=0 | N641=0

[BAND 20] rows=656:656 columns=A,B,C merges=C656:I656
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=None; gap=none
  row 650 [EMPTY]
  row 651 [EMPTY]
  row 652 [EMPTY]
  row 653 [EMPTY]
  row 654 [EMPTY]
  row 655 [SINGLE_TEXT n=1 columns=A]: A655='برآورد شرکت از تغییرات نرخ خرید مواد اولیه'
  row 656 [MULTI_TEXT n=3 columns=A,B,C]: A656='نرخ خرید مواد اولیه ' | B656='برآورد دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰ ' |
 C656='نظر به اینکه ماهیت فعالیت شرکت استخراج کانسنگ (خاک معدنی) می باشد لذ...
    MERGES C656:I656
  row 657 [EMPTY]
  row 658 [SINGLE_TEXT n=1 columns=A]: A658='«جملات آینده\u200cنگر نشان\u200cدهنده انتظارات، باورها یا پیش\u200cب...
    MERGES A658:T658
  row 659 [EMPTY]
  row 660 [EMPTY]
  row 661 [EMPTY]
  row 662 [SINGLE_TEXT n=1 columns=A]: A662='خلاصه اطلاعات گزارش تفسیری - صفحه 3'

[BAND 21] rows=670:671 columns=A,B,C,D,E,F,G merges=A670:A671,B670:D670,E670:G670
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=672; gap=none
  row 664 [EMPTY]
  row 665 [EMPTY]
  row 666 [EMPTY]
  row 667 [SINGLE_TEXT n=1 columns=A]: A667='اطلاعات این فرم گزیده ای از اطلاعات گزارش تفسیری مدیریت می باشد که ه...
    MERGES A667:T667
  row 668 [SINGLE_TEXT n=1 columns=A]: A668='هزینه های سربار و هزینه های عمومی و اداری شرکت'
  row 669 [SINGLE_TEXT n=1 columns=A]: A669='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 670 [MULTI_TEXT n=3 columns=A,B,E]: A670='شرح' | B670='هزینه سربار' | E670='هزینه های اداری، عمومی و فروش'
    MERGES A670:A671,B670:D670,E670:G670
  row 671 [MULTI_TEXT n=6 columns=B,C,D,E,F,G]: B671='سال مالی منتهی به ۱۴۰۴/۰۹/۳۰' | C671='دوره ۶ ماهه منتهی به ۱۴۰۵/۰۳
/۳۱' | D671='برآورد دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰' | E671='سال مالی منتهی به ۱۴۰۴/۰۹/۳۰' | F671='دوره ۶ ماهه منتهی به
۱۴۰۵/۰۳/۳۱' | G671='برآورد دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰'
    MERGES A670:A671
  row 672 [MIXED_NUMERIC n=7 columns=A,B,C,D,E,F,G]: A672='هزینه حقوق و دستمزد ' | B672=0 | C672=0 | D672=0 | E672=60402
3 | F672=417256 | G672=368236
  row 673 [MIXED_NUMERIC n=7 columns=A,B,C,D,E,F,G]: A673='هزینه استهلاک ' | B673=9233179 | C673=6007525 | D673=7068160
| E673=23403 | F673=18270 | G673=7684
  row 674 [MIXED_NUMERIC n=7 columns=A,B,C,D,E,F,G]: A674='هزینه انرژی (آب، برق، گاز و سوخت) ' | B674=95564 | C674=3790
| D674=469131 | E674=6495 | F674=0 | G674=13888
  row 675 [MIXED_NUMERIC n=7 columns=A,B,C,D,E,F,G]: A675='هزینه مواد مصرفی ' | B675=0 | C675=0 | D675=0 | E675=0 | F675
=0 | G675=0
  row 676 [MIXED_NUMERIC n=7 columns=A,B,C,D,E,F,G]: A676='هزینه تبلیغات ' | B676=0 | C676=0 | D676=0 | E676=0 | F676=0
| G676=0
  row 677 [MIXED_NUMERIC n=7 columns=A,B,C,D,E,F,G]: A677='حق العمل و کمیسیون فروش ' | B677=0 | C677=0 | D677=0 | E677=0
 | F677=0 | G677=0

[BAND 22] rows=685:685 columns=A,B merges=B685:H685
  SIGNATURE=NO_MATCH
  PRIOR prior_body=683; gap=SINGLE_TEXT
  FOLLOWING next_body=689; gap=EMPTY,SINGLE_TEXT,MULTI_TEXT
  row 679 [MIXED_NUMERIC n=7 columns=A,B,C,D,E,F,G]: A679='هزینه مطالبات مشکوک الوصول ' | B679=0 | C679=0 | D679=0 | E67
9=0 | F679=0 | G679=0
  row 680 [MIXED_NUMERIC n=7 columns=A,B,C,D,E,F,G]: A680='هزینه حمل و نقل و انتقال ' | B680=1276946 | C680=583185 | D68
0=1470991 | E680=0 | F680=0 | G680=0
  row 681 [MIXED_NUMERIC n=7 columns=A,B,C,D,E,F,G]: A681='سایر هزینه ها ' | B681=1177100 | C681=731909 | D681=999808 |
E681=70357 | F681=48337 | G681=43264
  row 682 [EMPTY]
  row 683 [MIXED_NUMERIC n=7 columns=A,B,C,D,E,F,G]: A683='جمع ' | B683=11782789 | C683=7326409 | D683=10008090 | E683=7
04278 | F683=483863 | G683=433072
  row 684 [SINGLE_TEXT n=1 columns=A]: A684='برآورد شرکت از تغییرات هزینه های عمومی ، اداری ، تشکیلاتی و خالص سای...
  row 685 [MULTI_TEXT n=2 columns=A,B]: A685='برآورد دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰ ' | B685='انتظار می رود هزینه های ع
مومی ، اداری و تشکیلاتی شرکت متناسب با نرخ ...
    MERGES B685:H685
  row 686 [EMPTY]
  row 687 [SINGLE_TEXT n=1 columns=A]: A687='وضعیت کارکنان'
  row 688 [MULTI_TEXT n=4 columns=A,B,C,D]: A688='شرح' | B688='سال مالی منتهی به ۱۴۰۴/۰۹/۳۰' | C688='دوره ۶ ماهه منتهی ب
ه ۱۴۰۵/۰۳/۳۱' | D688='برآورد دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰'
  row 689 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A689='تعداد پرسنل تولیدی شرکت ' | B689=419 | C689=380 | D689=419
  row 690 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A690='تعداد پرسنل غیر تولیدی شرکت ' | B690=125 | C690=131 | D690=125
  row 691 [SINGLE_TEXT n=1 columns=A]: A691='وضعیت ارزی'

[BAND 23] rows=688:688 columns=A,B,C,D merges=—
  SIGNATURE=NO_MATCH
  PRIOR prior_body=683; gap=SINGLE_TEXT,MULTI_TEXT,EMPTY,SINGLE_TEXT
  FOLLOWING next_body=689; gap=none
  row 682 [EMPTY]
  row 683 [MIXED_NUMERIC n=7 columns=A,B,C,D,E,F,G]: A683='جمع ' | B683=11782789 | C683=7326409 | D683=10008090 | E683=7
04278 | F683=483863 | G683=433072
  row 684 [SINGLE_TEXT n=1 columns=A]: A684='برآورد شرکت از تغییرات هزینه های عمومی ، اداری ، تشکیلاتی و خالص سای...
  row 685 [MULTI_TEXT n=2 columns=A,B]: A685='برآورد دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰ ' | B685='انتظار می رود هزینه های ع
مومی ، اداری و تشکیلاتی شرکت متناسب با نرخ ...
    MERGES B685:H685
  row 686 [EMPTY]
  row 687 [SINGLE_TEXT n=1 columns=A]: A687='وضعیت کارکنان'
  row 688 [MULTI_TEXT n=4 columns=A,B,C,D]: A688='شرح' | B688='سال مالی منتهی به ۱۴۰۴/۰۹/۳۰' | C688='دوره ۶ ماهه منتهی ب
ه ۱۴۰۵/۰۳/۳۱' | D688='برآورد دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰'
  row 689 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A689='تعداد پرسنل تولیدی شرکت ' | B689=419 | C689=380 | D689=419
  row 690 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A690='تعداد پرسنل غیر تولیدی شرکت ' | B690=125 | C690=131 | D690=125
  row 691 [SINGLE_TEXT n=1 columns=A]: A691='وضعیت ارزی'
  row 692 [SINGLE_TEXT n=1 columns=A]: A692='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 693 [MULTI_TEXT n=5 columns=A,B,C,F,I]: A693='شرح' | B693='نوع ارز' | C693='سال مالي منتهي به ۱۴۰۴/۰۹/۳۰' | F693='
دوره ۶ ماهه منتهي به ۱۴۰۵/۰۳/۳۱' | I693='برآورد دوره ۶ ماهه منتهي به ۱۴۰۵/۰۹/۳۰'
    MERGES A693:A694,B693:B694,C693:E693,F693:H693,I693:K693
  row 694 [MULTI_TEXT n=9 columns=C,D,E,F,G,H,I,J,K]: C694='نرخ ميانگين تسعير ارز' | D694='مبلغ ارزي' | E694='مبلغ ريالي
-ميليون ريال' | F694='نرخ ميانگين تسعير ارز' | G694='مبلغ ارزي' | H694='مبلغ ريالي-ميليون ريال' | I694='نرخ ميانگين تسعي
ر ارز' | J694='مبلغ ارزي' | K694='مبلغ ريالي-ميليون ريال'
    MERGES A693:A694,B693:B694

[BAND 24] rows=693:694 columns=A,B,C,D,E,F,G,H,I,J,K merges=A693:A694,B693:B694,C693:E693,F693:H693,I693:K693
  SIGNATURE=NO_MATCH
  PRIOR prior_body=690; gap=SINGLE_TEXT,SINGLE_TEXT
  FOLLOWING next_body=None; gap=none
  row 687 [SINGLE_TEXT n=1 columns=A]: A687='وضعیت کارکنان'
  row 688 [MULTI_TEXT n=4 columns=A,B,C,D]: A688='شرح' | B688='سال مالی منتهی به ۱۴۰۴/۰۹/۳۰' | C688='دوره ۶ ماهه منتهی ب
ه ۱۴۰۵/۰۳/۳۱' | D688='برآورد دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰'
  row 689 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A689='تعداد پرسنل تولیدی شرکت ' | B689=419 | C689=380 | D689=419
  row 690 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A690='تعداد پرسنل غیر تولیدی شرکت ' | B690=125 | C690=131 | D690=125
  row 691 [SINGLE_TEXT n=1 columns=A]: A691='وضعیت ارزی'
  row 692 [SINGLE_TEXT n=1 columns=A]: A692='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 693 [MULTI_TEXT n=5 columns=A,B,C,F,I]: A693='شرح' | B693='نوع ارز' | C693='سال مالي منتهي به ۱۴۰۴/۰۹/۳۰' | F693='
دوره ۶ ماهه منتهي به ۱۴۰۵/۰۳/۳۱' | I693='برآورد دوره ۶ ماهه منتهي به ۱۴۰۵/۰۹/۳۰'
    MERGES A693:A694,B693:B694,C693:E693,F693:H693,I693:K693
  row 694 [MULTI_TEXT n=9 columns=C,D,E,F,G,H,I,J,K]: C694='نرخ ميانگين تسعير ارز' | D694='مبلغ ارزي' | E694='مبلغ ريالي
-ميليون ريال' | F694='نرخ ميانگين تسعير ارز' | G694='مبلغ ارزي' | H694='مبلغ ريالي-ميليون ريال' | I694='نرخ ميانگين تسعي
ر ارز' | J694='مبلغ ارزي' | K694='مبلغ ريالي-ميليون ريال'
    MERGES A693:A694,B693:B694
  row 695 [SINGLE_TEXT n=1 columns=A]: A695='«جملات آینده\u200cنگر نشان\u200cدهنده انتظارات، باورها یا پیش\u200cب...
    MERGES A695:J695
  row 696 [SINGLE_TEXT n=1 columns=A]: A696='توضیحات درخصوص وضعیت ارزی '
    MERGES A696:D696
  row 697 [EMPTY]
  row 698 [EMPTY]
  row 699 [EMPTY]
  row 700 [EMPTY]

[BAND 25] rows=709:710 columns=A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P merges=A709:A710,B709:B710,C709:C710,D709:D710,E709:E710,
F709:F710,G709:H709,K709:K710,L709:L710,M709:M710,N709:N710,O709:O710,P709:P710
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=711; gap=none
  row 703 [EMPTY]
  row 704 [EMPTY]
  row 705 [EMPTY]
  row 706 [SINGLE_TEXT n=1 columns=A]: A706='اطلاعات این فرم گزیده ای از اطلاعات گزارش تفسیری مدیریت می باشد که ه...
    MERGES A706:T706
  row 707 [SINGLE_TEXT n=1 columns=A]: A707='تشریح برنامه های شرکت جهت تکمیل طرح های توسعه'
  row 708 [SINGLE_TEXT n=1 columns=A]: A708='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 709 [MULTI_TEXT n=15 columns=A,B,C,D,E,F,G,I,J,K,L,M,N,O,P]: A709='نام طرح' | B709='هزینه های برآوردی ریالی طرح -
میلیون ریال' | C709='هزینه های برآوردی ارزی طرح' | D709='نوع ارز' | E709='هزینه های انجام شده تا تاریخ ۱۴۰۵/۰۳/۳۱ - میلی
ون ریال' | F709='هزینه های برآوردی تکمیل طرح- میلیون ریال' | G709='منابع تامین مالی' | I709='نرخNPV' | J709='نرخ IRR' |
K709='درصد پیشرفت فیزیکی طرح در تاریخ ۱۴۰۴/۰۹/۳۰' | L709='درصد پیشرفت فیزیکی طرح در تاریخ ۱۴۰۵/۰۳/۳۱' | M709='درصد پیشرف
ت فیزیکی برآوردی طرح در تاریخ ۱۴۰۵/۰۹/۳۰' | N709='تاریخ برآوردی بهره برداری از طرح' | O709='تشریح تاثیر طرح در فعالیتهای
 آتی شرکت' | P709='توضیحات'
    MERGES A709:A710,B709:B710,C709:C710,D709:D710,E709:E710,F709:F710,G709:H709,K709:K710,L709:L710,M709:M710,N709:N710
,O709:O710,P709:P710
  row 710 [MULTI_TEXT n=2 columns=G,H]: G710='ارزی' | H710='ریالی'
    MERGES A709:A710,B709:B710,C709:C710,D709:D710,E709:E710,F709:F710,K709:K710,L709:L710,M709:M710,N709:N710,O709:O710
,P709:P710
  row 711 [MIXED_NUMERIC n=15 columns=A,B,C,E,F,G,H,I,J,K,L,M,N,O,P]: A711='پروژه ساخت تصفيه خانه فاضلاب شماره يک ' | B7
11=30000 | C711=0 | E711=25990 | F711=4010 | G711=0 | H711=0 | I711=0 | J711=0 | K711=55 | L711=87 | M711=100 | N711='۱۴
۰۵/۰۴/۳۱ ' | O711='بهینه سازی و جلوگیری از هدر رفت آب مصرفی ' | P711='بهینه سازی و جلوگیری از هدر رفت آب مصرفی '
  row 712 [MIXED_NUMERIC n=15 columns=A,B,C,E,F,G,H,I,J,K,L,M,N,O,P]: A712='پروژه گازرساني به معدن ' | B712=55000 | C712
=0 | E712=42750 | F712=12250 | G712=0 | H712=0 | I712=0 | J712=0 | K712=78 | L712=78 | M712=100 | N712='۱۴۰۵/۰۴/۳۱ ' | O
712='تامین گاز ساختمان های اداری و صنعتی معدن ' | P712='تامین گاز ساختمان های اداری و صنعتی معدن '
  row 713 [MIXED_NUMERIC n=15 columns=A,B,C,E,F,G,H,I,J,K,L,M,N,O,P]: A713='پروژه امکانات رفاهي ' | B713=28000 | C713=0
| E713=610 | F713=27390 | G713=0 | H713=0 | I713=0 | J713=0 | K713=0 | L713=2 | M713=100 | N713='۱۴۰۵/۰۷/۳۰ ' | O713='رف
اه پرسنل ' | P713='رفاه پرسنل '
  row 714 [MIXED_NUMERIC n=15 columns=A,B,C,E,F,G,H,I,J,K,L,M,N,O,P]: A714='پروژه اتاقک باسکول پيت سه معدن ' | B714=6200
 | C714=0 | E714=3785 | F714=2415 | G714=0 | H714=0 | I714=0 | J714=0 | K714=0 | L714=61 | M714=100 | N714='۱۴۰۵/۰۵/۳۱ '
 | O714='رفع خطرات ناشی از آتشباری ' | P714='رفع خطرات ناشی از آتشباری '
  row 715 [SINGLE_TEXT n=1 columns=A]: A715='توضیحات درخصوص تشریح برنامه های شرکت جهت تکمیل طرح های توسعه'
  row 716 [EMPTY]
    MERGES A716:T716

[BAND 26] rows=719:720 columns=A,B,C,D,E,F,G,H,I,J,K,L,M,N,O merges=A719:A720,B719:E719,F719:J719,K719:O719
  SIGNATURE=COMPOUND_CANDIDATE
  PRIOR prior_body=714; gap=SINGLE_TEXT,EMPTY,SINGLE_TEXT,SINGLE_TEXT
  FOLLOWING next_body=721; gap=none
  row 713 [MIXED_NUMERIC n=15 columns=A,B,C,E,F,G,H,I,J,K,L,M,N,O,P]: A713='پروژه امکانات رفاهي ' | B713=28000 | C713=0
| E713=610 | F713=27390 | G713=0 | H713=0 | I713=0 | J713=0 | K713=0 | L713=2 | M713=100 | N713='۱۴۰۵/۰۷/۳۰ ' | O713='رف
اه پرسنل ' | P713='رفاه پرسنل '
  row 714 [MIXED_NUMERIC n=15 columns=A,B,C,E,F,G,H,I,J,K,L,M,N,O,P]: A714='پروژه اتاقک باسکول پيت سه معدن ' | B714=6200
 | C714=0 | E714=3785 | F714=2415 | G714=0 | H714=0 | I714=0 | J714=0 | K714=0 | L714=61 | M714=100 | N714='۱۴۰۵/۰۵/۳۱ '
 | O714='رفع خطرات ناشی از آتشباری ' | P714='رفع خطرات ناشی از آتشباری '
  row 715 [SINGLE_TEXT n=1 columns=A]: A715='توضیحات درخصوص تشریح برنامه های شرکت جهت تکمیل طرح های توسعه'
  row 716 [EMPTY]
    MERGES A716:T716
  row 717 [SINGLE_TEXT n=1 columns=A]: A717='وضعیت شرکت\u200cهای سرمایه\u200cپذیر'
  row 718 [SINGLE_TEXT n=1 columns=A]: A718='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 719 [MULTI_TEXT n=4 columns=A,B,F,K]: A719='نام شرکت' | B719='سال مالی منتهی به ۱۴۰۴/۰۹/۳۰' | F719='دوره ۶ ماهه من
تهی به ۱۴۰۵/۰۳/۳۱' | K719='برآورد دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰'
    MERGES A719:A720,B719:E719,F719:J719,K719:O719
  row 720 [MULTI_TEXT n=14 columns=B,C,D,E,F,G,H,I,J,K,L,M,N,O]: B720='درصد مالکیت' | C720='بهای تمام شده' | D720='سال م
الی شرکت سرمایه پذیر' | E720='درآمد سرمایه گذاری - میلیون ریال' | F720='درصد مالکیت' | G720='بهای تمام شده' | H720='درآم
د هر سهم' | I720='درآمد نقدی هر سهم' | J720='درآمد سرمایه گذاری - میلیون ریال' | K720='درصد مالکیت' | L720='بهای تمام شد
ه' | M720='درآمد هر سهم' | N720='درآمد نقدی هر سهم' | O720='درآمد سرمایه گذاری - میلیون ریال'
    MERGES A719:A720
  row 721 [MIXED_NUMERIC n=15 columns=A,B,C,D,E,F,G,H,I,J,K,L,M,N,O]: A721='استحصال مواد معدني تخت سليمان ' | B721=98 |
C721=2594691 | D721='۱۴۰۴/۰۹/۳۰ ' | E721=41602650 | F721=98 | G721=2594691 | H721=0 | I721=0 | J721=0 | K721=98 | L721=2
594691 | M721=0 | N721=0 | O721=133722320
  row 722 [MIXED_NUMERIC n=15 columns=A,B,C,D,E,F,G,H,I,J,K,L,M,N,O]: A722='آجر سفالين صبا مهر ' | B722=49 | C722=3 | D7
22='۱۴۰۴/۰۹/۳۰ ' | E722=0 | F722=49 | G722=3 | H722=0 | I722=0 | J722=0 | K722=49 | L722=3 | M722=0 | N722=0 | O722=0
  row 723 [MIXED_NUMERIC n=15 columns=A,B,C,D,E,F,G,H,I,J,K,L,M,N,O]: A723='ياران تخت سليمان ' | B723=47 | C723=2 | D723
='۱۴۰۴/۰۹/۳۰ ' | E723=0 | F723=47 | G723=2 | H723=0 | I723=0 | J723=0 | K723=47 | L723=2 | M723=0 | N723=0 | O723=0
  row 724 [SINGLE_TEXT n=1 columns=A]: A724='توضیحات در خصوص وضعیت شرکت\u200cهای سرمایه\u200cپذیر'
  row 725 [SINGLE_TEXT n=1 columns=A]: A725='شرکت در سال ۱۴۰۴ جهت سرمایه گذاری در یک صرافی (در شرف تاسیس) مبلغ ۹۹...
    MERGES A725:T725
  row 726 [SINGLE_TEXT n=1 columns=A]: A726='«جملات آینده\u200cنگر نشان\u200cدهنده انتظارات، باورها یا پیش\u200cب...
    MERGES A726:T726

[BAND 27] rows=738:738 columns=A,B,C,D merges=—
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=739; gap=none
  row 732 [EMPTY]
  row 733 [EMPTY]
  row 734 [EMPTY]
  row 735 [SINGLE_TEXT n=1 columns=A]: A735='اطلاعات این فرم گزیده ای از اطلاعات گزارش تفسیری مدیریت می باشد که ه...
    MERGES A735:T735
  row 736 [SINGLE_TEXT n=1 columns=A]: A736='سایر درآمدهای عملیاتی'
  row 737 [SINGLE_TEXT n=1 columns=A]: A737='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 738 [MULTI_TEXT n=4 columns=A,B,C,D]: A738='شرح' | B738='سال مالی منتهی به ۱۴۰۴/۰۹/۳۰' | C738='دوره ۶ ماهه منتهی ب
ه ۱۴۰۵/۰۳/۳۱' | D738='برآورد دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰'
  row 739 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A739='اجاره ماشين آلات ' | B739=303195 | C739=286052 | D739=213948
  row 740 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A740='سود سهام ' | B740=41602650 | C740=0 | D740=133722320
  row 741 [EMPTY]
  row 742 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A742='جمع ' | B742=41905845 | C742=286052 | D742=133936268
  row 743 [SINGLE_TEXT n=1 columns=A]: A743='سایر هزینه\u200cهای عملیاتی'
  row 744 [SINGLE_TEXT n=1 columns=A]: A744='کلیه مبالغ درج شده به میلیون ریال می باشد'

[BAND 28] rows=745:745 columns=A,B,C,D merges=—
  SIGNATURE=COMPOUND_CANDIDATE
  PRIOR prior_body=742; gap=SINGLE_TEXT,SINGLE_TEXT
  FOLLOWING next_body=746; gap=none
  row 739 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A739='اجاره ماشين آلات ' | B739=303195 | C739=286052 | D739=213948
  row 740 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A740='سود سهام ' | B740=41602650 | C740=0 | D740=133722320
  row 741 [EMPTY]
  row 742 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A742='جمع ' | B742=41905845 | C742=286052 | D742=133936268
  row 743 [SINGLE_TEXT n=1 columns=A]: A743='سایر هزینه\u200cهای عملیاتی'
  row 744 [SINGLE_TEXT n=1 columns=A]: A744='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 745 [MULTI_TEXT n=4 columns=A,B,C,D]: A745='شرح' | B745='سال مالی منتهی به ۱۴۰۴/۰۹/۳۰' | C745='دوره ۶ ماهه منتهی ب
ه ۱۴۰۵/۰۳/۳۱' | D745='برآورد دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰'
  row 746 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A746='جمع ' | B746=0 | C746=0 | D746=0
  row 747 [SINGLE_TEXT n=1 columns=A]: A747='منابع تامین مالی'
  row 748 [SINGLE_TEXT n=1 columns=A]: A748='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 749 [SINGLE_TEXT n=1 columns=A]: A749='منابع تامین مالی شرکت در دوره ۶ ماهه منتهی به ۱۴۰۵/۰۳/۳۱'
    MERGES A749:K749
  row 750 [MULTI_TEXT n=7 columns=A,B,C,D,H,J,K]: A750='محل تامین' | B750='نرخ سود' | C750='مانده اول دوره تسهیلات ارزی
و ریالی (میلیون ریال)' | D750='مانده پایان دوره (اصل و فرع)' | H750='مانده پایان دوره به تفکیک سررسید' | J750='مبلغ هزین
ه مالی طی دوره' | K750='سایر توضیحات'
    MERGES A750:A752,B750:B752,C750:C752,D750:G750,H750:I751,J750:J752,K750:K752
  row 751 [MULTI_TEXT n=2 columns=D,E]: D751='ریالی' | E751='ارزی'
    MERGES A750:A752,B750:B752,C750:C752,H750:I751,J750:J752,K750:K752,D751:D752,E751:G751

[BAND 29] rows=750:752 columns=A,B,C,D,E,F,G,H,I,J,K merges=A750:A752,B750:B752,C750:C752,D750:G750,H750:I751,J750:J752,
K750:K752,D751:D752,E751:G751
  SIGNATURE=COMPOUND_CANDIDATE
  PRIOR prior_body=746; gap=SINGLE_TEXT,SINGLE_TEXT,SINGLE_TEXT
  FOLLOWING next_body=753; gap=none
  row 744 [SINGLE_TEXT n=1 columns=A]: A744='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 745 [MULTI_TEXT n=4 columns=A,B,C,D]: A745='شرح' | B745='سال مالی منتهی به ۱۴۰۴/۰۹/۳۰' | C745='دوره ۶ ماهه منتهی ب
ه ۱۴۰۵/۰۳/۳۱' | D745='برآورد دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰'
  row 746 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A746='جمع ' | B746=0 | C746=0 | D746=0
  row 747 [SINGLE_TEXT n=1 columns=A]: A747='منابع تامین مالی'
  row 748 [SINGLE_TEXT n=1 columns=A]: A748='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 749 [SINGLE_TEXT n=1 columns=A]: A749='منابع تامین مالی شرکت در دوره ۶ ماهه منتهی به ۱۴۰۵/۰۳/۳۱'
    MERGES A749:K749
  row 750 [MULTI_TEXT n=7 columns=A,B,C,D,H,J,K]: A750='محل تامین' | B750='نرخ سود' | C750='مانده اول دوره تسهیلات ارزی
و ریالی (میلیون ریال)' | D750='مانده پایان دوره (اصل و فرع)' | H750='مانده پایان دوره به تفکیک سررسید' | J750='مبلغ هزین
ه مالی طی دوره' | K750='سایر توضیحات'
    MERGES A750:A752,B750:B752,C750:C752,D750:G750,H750:I751,J750:J752,K750:K752
  row 751 [MULTI_TEXT n=2 columns=D,E]: D751='ریالی' | E751='ارزی'
    MERGES A750:A752,B750:B752,C750:C752,H750:I751,J750:J752,K750:K752,D751:D752,E751:G751
  row 752 [MULTI_TEXT n=5 columns=E,F,G,H,I]: E752='نوع ارز' | F752='مبلغ ارزی' | G752='معادل ریالی تسهیلات ارزی (میلیون
 ریال)' | H752='کوتاه مدت' | I752='بلند مدت'
    MERGES A750:A752,B750:B752,C750:C752,J750:J752,K750:K752,D751:D752
  row 753 [MIXED_NUMERIC n=9 columns=A,B,C,D,F,G,H,I,J]: A753='تسهیلات دریافتی از بانکها ' | B753=0 | C753=0 | D753=0 |
F753=0 | G753=0 | H753=0 | I753=0 | J753=13909
  row 754 [EMPTY]
  row 755 [MIXED_NUMERIC n=3 columns=A,C,J]: A755='تسهیلات تسویه شده از ابتدای سال مالی تا پایان دوره ' | C755=0 | J755=
0
  row 756 [MIXED_NUMERIC n=7 columns=A,C,D,G,H,I,J]: A756='جمع ' | C756=0 | D756=0 | G756=0 | H756=0 | I756=0 | J756=139
09
  row 757 [MIXED_NUMERIC n=2 columns=I,J]: I757='انتقال به دارایی ' | J757=0
    MERGES A757:H757
  row 758 [MIXED_NUMERIC n=2 columns=I,J]: I758='هزینه مالی دوره ' | J758=13909
    MERGES A758:H758

[BAND 30] rows=762:764 columns=A,B,C,D,E,F,G,H,I,J,K merges=A762:A764,B762:B764,C762:C764,D762:G762,H762:I763,J762:J764,
K762:K764,D763:D764,E763:G763
  SIGNATURE=COMPOUND_CANDIDATE
  PRIOR prior_body=758; gap=SINGLE_TEXT,SINGLE_TEXT,SINGLE_TEXT
  FOLLOWING next_body=765; gap=none
  row 756 [MIXED_NUMERIC n=7 columns=A,C,D,G,H,I,J]: A756='جمع ' | C756=0 | D756=0 | G756=0 | H756=0 | I756=0 | J756=139
09
  row 757 [MIXED_NUMERIC n=2 columns=I,J]: I757='انتقال به دارایی ' | J757=0
    MERGES A757:H757
  row 758 [MIXED_NUMERIC n=2 columns=I,J]: I758='هزینه مالی دوره ' | J758=13909
    MERGES A758:H758
  row 759 [SINGLE_TEXT n=1 columns=A]: A759='منابع تامین مالی (برآوردی)'
  row 760 [SINGLE_TEXT n=1 columns=A]: A760='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 761 [SINGLE_TEXT n=1 columns=A]: A761='برآورد منابع تامین مالی شرکت در دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰'
    MERGES A761:K761
  row 762 [MULTI_TEXT n=7 columns=A,B,C,D,H,J,K]: A762='محل تامین' | B762='نرخ سود' | C762='مانده اول دوره تسهیلات ارزی
و ریالی (میلیون ریال)' | D762='مانده پایان دوره (اصل و فرع)' | H762='مانده پایان دوره به تفکیک سررسید' | J762='مبلغ هزین
ه مالی طی دوره' | K762='سایر توضیحات'
    MERGES A762:A764,B762:B764,C762:C764,D762:G762,H762:I763,J762:J764,K762:K764
  row 763 [MULTI_TEXT n=2 columns=D,E]: D763='ریالی' | E763='ارزی'
    MERGES A762:A764,B762:B764,C762:C764,H762:I763,J762:J764,K762:K764,D763:D764,E763:G763
  row 764 [MULTI_TEXT n=5 columns=E,F,G,H,I]: E764='نوع ارز' | F764='مبلغ ارزی' | G764='معادل ریالی تسهیلات ارزی (میلیون
 ریال)' | H764='کوتاه مدت' | I764='بلند مدت'
    MERGES A762:A764,B762:B764,C762:C764,J762:J764,K762:K764,D763:D764
  row 765 [MIXED_NUMERIC n=9 columns=A,B,C,D,F,G,H,I,J]: A765='تسهیلات دریافتی از بانکها ' | B765=0 | C765=0 | D765=0 |
F765=0 | G765=0 | H765=0 | I765=0 | J765=41799
  row 766 [EMPTY]
  row 767 [MIXED_NUMERIC n=3 columns=A,C,J]: A767='تسهیلات تسویه شده از ابتدای سال مالی تا پایان دوره ' | C767=0 | J767=
0
  row 768 [MIXED_NUMERIC n=7 columns=A,C,D,G,H,I,J]: A768='جمع ' | C768=0 | D768=0 | G768=0 | H768=0 | I768=0 | J768=417
99
  row 769 [MIXED_NUMERIC n=2 columns=I,J]: I769='انتقال به دارایی ' | J769=0
    MERGES A769:H769
  row 770 [MIXED_NUMERIC n=2 columns=I,J]: I770='هزینه مالی دوره ' | J770=41799
    MERGES A770:H770

[BAND 31] rows=789:789 columns=A,B,C,D merges=—
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=790; gap=none
  row 783 [SINGLE_TEXT n=1 columns=A]: A783='توضیحات در خصوص جزئیات منابع تامین مالی شرکت در پایان دوره'
  row 784 [SINGLE_TEXT n=1 columns=A]: A784='شرکت در دوره مورد گزارش هیچگونه تسهیلاتی را دریافت نکرده است. '
    MERGES A784:K784
  row 785 [SINGLE_TEXT n=1 columns=A]: A785='برآورد شرکت از برنامه های تامین مالی و تغییرات هزینه های مالی شرکت'
  row 786 [SINGLE_TEXT n=1 columns=A]: A786='شرکت در صورت نیاز به تامین مالی نسبت به اخذ تسهیلات مالی اقدام خواهد...
    MERGES A786:K786
  row 787 [SINGLE_TEXT n=1 columns=A]: A787='سایر درآمدها و هزینه\u200cهای غیرعملیاتی - درآمد سرمایه\u200cگذاری\u...
  row 788 [SINGLE_TEXT n=1 columns=A]: A788='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 789 [MULTI_TEXT n=4 columns=A,B,C,D]: A789='شرح' | B789='سال مالی منتهی به ۱۴۰۴/۰۹/۳۰' | C789='دوره ۶ ماهه منتهی ب
ه ۱۴۰۵/۰۳/۳۱' | D789='برآورد دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰'
  row 790 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A790='سود(زيان) ناشي از فروش سرمايه گذاري ها ' | B790=249 | C790=0 | D790
=0
  row 791 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A791='سود حاصل از سرمايه گذاري در صندوق سرمايه گذاري ' | B791=-535 | C791
=0 | D791=0
  row 792 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A792='سود (زيان) حاصل از فروش اوراق مشارکت ' | B792=20336 | C792=0 | D792
=0
  row 793 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A793='زيان کاهش ارزش سرمايه گذاري ها ' | B793=-9995 | C793=-31755 | D793=
0
  row 794 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A794='سود سهام ' | B794=0 | C794=12375 | D794=0
  row 795 [EMPTY]

[BAND 32] rows=799:799 columns=A,B,C,D merges=—
  SIGNATURE=COMPOUND_CANDIDATE
  PRIOR prior_body=796; gap=SINGLE_TEXT,SINGLE_TEXT
  FOLLOWING next_body=800; gap=none
  row 793 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A793='زيان کاهش ارزش سرمايه گذاري ها ' | B793=-9995 | C793=-31755 | D793=
0
  row 794 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A794='سود سهام ' | B794=0 | C794=12375 | D794=0
  row 795 [EMPTY]
  row 796 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A796='جمع ' | B796=10055 | C796=-19380 | D796=0
  row 797 [SINGLE_TEXT n=1 columns=A]: A797='سایر درآمدها و هزینه\u200cهای غیرعملیاتی - اقلام متفرقه'
  row 798 [SINGLE_TEXT n=1 columns=A]: A798='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 799 [MULTI_TEXT n=4 columns=A,B,C,D]: A799='شرح' | B799='سال مالی منتهی به ۱۴۰۴/۰۹/۳۰' | C799='دوره ۶ ماهه منتهی ب
ه ۱۴۰۵/۰۳/۳۱' | D799='برآورد دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰'
  row 800 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A800='سود(زيان)ناشي از فروش دارايي ثابت مشهود ' | B800=73650 | C800=0 | D
800=147301
  row 801 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A801='سود(زيان)جبران خسارت از بيمه گران ' | B801=-28922 | C801=0 | D801=0

  row 802 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A802='فروش ضايعات ' | B802=22009 | C802=-1721 | D802=44739
  row 803 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A803='سود(زيان) حاصل از فروش قطعات و لوازم يدکي ' | B803=0 | C803=0 | D80
3=0
  row 804 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A804='ساير ' | B804=-130958 | C804=-82 | D804=2083
  row 805 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A805='درآمد حاصل از حمل و باربري ' | B805=37776 | C805=17854 | D805=11435
4

[BAND 33] rows=810:810 columns=A,B,C,D,E merges=—
  SIGNATURE=COMPOUND_CANDIDATE
  PRIOR prior_body=807; gap=SINGLE_TEXT,SINGLE_TEXT
  FOLLOWING next_body=811; gap=none
  row 804 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A804='ساير ' | B804=-130958 | C804=-82 | D804=2083
  row 805 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A805='درآمد حاصل از حمل و باربري ' | B805=37776 | C805=17854 | D805=11435
4
  row 806 [EMPTY]
  row 807 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A807='جمع ' | B807=-26445 | C807=16051 | D807=308477
  row 808 [SINGLE_TEXT n=1 columns=A]: A808='برنامه شرکت در خصوص تقسیم سود'
  row 809 [SINGLE_TEXT n=1 columns=A]: A809='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 810 [MULTI_TEXT n=5 columns=A,B,C,D,E]: A810='مبلغ سود انباشته پایان سال مالی گذشته' | B810='سود سهام پیشنهادی هیئ
ت مدیره در سال مالی گذشته' | C810='مبلغ سود خالص سال مالی گذشته' | D810='سود سهام مصوب مجمع سال مالی گذشته' | E810='پیشن
هاد هیئت مدیره درخصوص درصد تقسیم سود سال مالی جاری'
  row 811 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A811=56464890 | B811=40500000 | C811=50287149 | D811=49950000 | E811=0
  row 812 [SINGLE_TEXT n=1 columns=A]: A812='سایر برنامه های با اهمیت شرکت'
  row 813 [MULTI_TEXT n=2 columns=A,B]: A813='برآورد دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰ ' | B813='مهم ترین برنامه شرکت فعال
 سازی معادن جدید است. '
    MERGES B813:H813
  row 814 [EMPTY]
  row 815 [SINGLE_TEXT n=1 columns=A]: A815='سایر توضیحات با اهمیت'
  row 816 [SINGLE_TEXT n=1 columns=A]: A816='به شرح گزارش تفسیری پیوست '
    MERGES A816:K816

[BAND 34] rows=813:813 columns=A,B merges=B813:H813
  SIGNATURE=NO_MATCH
  PRIOR prior_body=811; gap=SINGLE_TEXT
  FOLLOWING next_body=None; gap=none
  row 807 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A807='جمع ' | B807=-26445 | C807=16051 | D807=308477
  row 808 [SINGLE_TEXT n=1 columns=A]: A808='برنامه شرکت در خصوص تقسیم سود'
  row 809 [SINGLE_TEXT n=1 columns=A]: A809='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 810 [MULTI_TEXT n=5 columns=A,B,C,D,E]: A810='مبلغ سود انباشته پایان سال مالی گذشته' | B810='سود سهام پیشنهادی هیئ
ت مدیره در سال مالی گذشته' | C810='مبلغ سود خالص سال مالی گذشته' | D810='سود سهام مصوب مجمع سال مالی گذشته' | E810='پیشن
هاد هیئت مدیره درخصوص درصد تقسیم سود سال مالی جاری'
  row 811 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A811=56464890 | B811=40500000 | C811=50287149 | D811=49950000 | E811=0
  row 812 [SINGLE_TEXT n=1 columns=A]: A812='سایر برنامه های با اهمیت شرکت'
  row 813 [MULTI_TEXT n=2 columns=A,B]: A813='برآورد دوره ۶ ماهه منتهی به ۱۴۰۵/۰۹/۳۰ ' | B813='مهم ترین برنامه شرکت فعال
 سازی معادن جدید است. '
    MERGES B813:H813
  row 814 [EMPTY]
  row 815 [SINGLE_TEXT n=1 columns=A]: A815='سایر توضیحات با اهمیت'
  row 816 [SINGLE_TEXT n=1 columns=A]: A816='به شرح گزارش تفسیری پیوست '
    MERGES A816:K816
  row 817 [SINGLE_TEXT n=1 columns=A]: A817='«جملات آینده\u200cنگر نشان\u200cدهنده انتظارات، باورها یا پیش\u200cب...
    MERGES A817:T817
  row 818 [EMPTY]
  row 819 [EMPTY]

[BAND 35] rows=830:831 columns=A,B,C,D,E,F,G,H,I,J,K merges=B830:B831,C830:C831,D830:D831,E830:E831,F830:F831,G830:G831,
H830:H831,J830:J831,K830:K831
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=832; gap=none
  row 824 [EMPTY]
  row 825 [EMPTY]
  row 826 [SINGLE_TEXT n=1 columns=A]: A826='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 827 [EMPTY]
  row 828 [EMPTY]
  row 829 [EMPTY]
  row 830 [MULTI_TEXT n=11 columns=A,B,C,D,E,F,G,H,I,J,K]: A830='نام عضو حقیقی یا حقوقی' | B830='نام عضو حقیقی یا حقوقی
جدید هیئت مدیره' | C830='شمارۀ ثبت / کد ملی' | D830='نام نماینده قبلی عضو حقوقی' | E830='نام نماینده جدید عضو حقوقی' | F
830='کد ملی' | G830='سمت' | H830='موظف/غیر موظف' | I830='مقطع' | J830='رشته تحصیلی' | K830='امضا کننده صورت مالی'
    MERGES B830:B831,C830:C831,D830:D831,E830:E831,F830:F831,G830:G831,H830:H831,J830:J831,K830:K831
  row 831 [MULTI_TEXT n=2 columns=A,I]: A831='قدیم هیئت مدیره' | I831='تحصیلی'
    MERGES B830:B831,C830:C831,D830:D831,E830:E831,F830:F831,G830:G831,H830:H831,J830:J831,K830:K831
  row 832 [MIXED_NUMERIC n=10 columns=A,B,C,D,E,F,G,H,I,J]: A832='کوشش آذين قشم' | B832='کوشش آذين قشم' | C832=108615036
29 | D832='سيدامير سراج هاشمي' | E832='سيدامير سراج هاشمي' | F832=81088167 | G832='نایب رئیس هیئت\u200cمدیره' | H832='غی
ر موظف' | I832='کارشناسي ارشد' | J832='مديريت کسب و کار'
  row 833 [MIXED_NUMERIC n=10 columns=A,B,C,D,E,F,G,H,I,J]: A833='سرمايه گذاري گلومينکو قشم' | B833='سرمايه گذاري گلومين
کو قشم' | C833=10861394039 | D833='محمد سالارزاده اميري' | E833='محمد سالارزاده اميري' | F833=1380680913 | G833='عضو هیئ
ت\u200cمدیره' | H833='غیر موظف' | I833='کارشناسي ارشد' | J833='زمين شناسي'
  row 834 [MIXED_NUMERIC n=10 columns=A,B,C,D,E,F,G,H,I,J]: A834='کاوندگان قشم' | B834='کاوندگان قشم' | C834=10861504332
 | D834='مصطفي خرم نژاد' | E834='مصطفي خرم نژاد' | F834=63151898 | G834='رئیس هیئت\u200cمدیره' | H834='غیر موظف' | I834=
'کارشناسي ارشد' | J834='حسابداري'
  row 835 [MIXED_NUMERIC n=10 columns=A,B,C,D,E,F,G,H,I,J]: A835='تابان کيش' | B835='تابان کيش' | C835=10861394189 | D83
5='عليرضا هوشنگي' | E835='عليرضا هوشنگي' | F835=72448903 | G835='عضو هیئت\u200cمدیره' | H835='موظف' | I835='کارشناسي' |
J835='مديريت بيمه'
  row 836 [MIXED_NUMERIC n=10 columns=A,B,C,D,E,F,G,H,I,J]: A836='فرا انديشان نيک فرجام قشم' | B836='فرا انديشان نيک فرج
ام قشم' | C836=10861394307 | D836='ابوالفضل رستمخاني' | E836='ابوالفضل رستمخاني' | F836=4284542869 | G836='عضو هیئت\u200
cمدیره' | H836='موظف' | I836='کارشناسي' | J836='مهندسي عمران'
  row 837 [EMPTY]

[BAND 36] rows=849:851 columns=A,B,C,D,E,F,G,H,I,J,K,L,M merges=—
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=None; gap=none
  row 843 [EMPTY]
  row 844 [EMPTY]
  row 845 [SINGLE_TEXT n=1 columns=A]: A845='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 846 [EMPTY]
  row 847 [EMPTY]
  row 848 [EMPTY]
  row 849 [MULTI_TEXT n=13 columns=A,B,C,D,E,F,G,H,I,J,K,L,M]: A849='نماد شرکت' | B849='نام شرکت' | C849='نماد ثبت شده ن
زد سازمان' | D849='وضعیت ثبت شده نزد سازمان' | E849='نوع فعالیت' | F849='حسابرس' | G849='سال مالی' | H849='فعال/غیر فعال
' | I849='وضعیت' | J849='آخرین تاریخ مجمع تغییر سال مالی' | K849='تاریخ شمولیت' | L849='تاریخ خروج از شمولیت' | M849='تو
ضیحات'
  row 850 [MULTI_TEXT n=13 columns=A,B,C,D,E,F,G,H,I,J,K,L,M]: A850='فزر3' | B850='ياران تخت سليمان' | C850='*' | D850='
ثبت نشده نزد سازمان' | E850='خدماتی' | F850='موسسه حسابرسي هادي حساب تهران' | G850='1404/12/29' | H850='فعال' | I850='فا
قد صورتهای مالی حسابرسی شده و دارای اظهارنامه مالیاتی' | J850='*' | K850='1391/10/12' | L850='*' | M850='به دلیل حجم فعا
لیت مالی پایین شرکت یاران تخت سلیمان (ارزش دارایی بسی...
  row 851 [MULTI_TEXT n=13 columns=A,B,C,D,E,F,G,H,I,J,K,L,M]: A851='فزر4' | B851='آجر سفالين صبا مهر' | C851='*' | D851
='ثبت نشده نزد سازمان' | E851='تولیدی' | F851='موسسه حسابرسي هادي حساب تهران' | G851='1404/12/29' | H851='فعال' | I851='
در حال تصفیه' | J851='*' | K851='1388/02/31' | L851='*' | M851='به دلیل عدم فعالیت و کم اهمیت بودن شرکت آجر سفالین صبامه
ر (ارزش دارا...
  row 852 [EMPTY]
  row 853 [EMPTY]
    MERGES A853:M853
  row 854 [SINGLE_TEXT n=1 columns=A]: A854='اطلاعات نمایش داده شده با اطلاعات امضا شده مطابقت دارد'
    MERGES A854:M854
  row 855 [EMPTY]
    MERGES A855:M855
  row 856 [EMPTY]
  row 857 [EMPTY]

[BAND 37] rows=868:870 columns=A,B,C,D,E,F,G,H,I,J,K,L,M merges=—
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=None; gap=none
  row 862 [EMPTY]
  row 863 [EMPTY]
  row 864 [SINGLE_TEXT n=1 columns=A]: A864='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 865 [EMPTY]
  row 866 [EMPTY]
  row 867 [EMPTY]
  row 868 [MULTI_TEXT n=13 columns=A,B,C,D,E,F,G,H,I,J,K,L,M]: A868='نماد شرکت' | B868='نام شرکت' | C868='نماد ثبت شده ن
زد سازمان' | D868='وضعیت ثبت شده نزد سازمان' | E868='نوع فعالیت' | F868='حسابرس' | G868='سال مالی' | H868='فعال/غیر فعال
' | I868='وضعیت' | J868='آخرین تاریخ مجمع تغییر سال مالی' | K868='تاریخ شمولیت' | L868='تاریخ خروج از شمولیت' | M868='تو
ضیحات'
  row 869 [MULTI_TEXT n=12 columns=A,B,C,D,E,F,G,H,I,J,K,L]: A869='فزر2' | B869='استحصال مواد معدني تخت سليمان' | C869='
*' | D869='ثبت نشده نزد سازمان' | E869='تولیدی' | F869='موسسه حسابرسي امجد تراز' | G869='1405/09/30' | H869='فعال' | I86
9='دارای صورتهای مالی حسابرسی شده' | J869='1401/09/20' | K869='1398/05/02' | L869='*'
  row 870 [MULTI_TEXT n=12 columns=A,B,C,D,E,F,G,H,I,J,K,L]: A870='فزر1' | B870='فرآوري پويا زرکان آق دره' | C870='*' |
D870='ثبت نشده نزد سازمان' | E870='تولیدی' | F870='موسسه حسابرسي و خدمات آرمان نوين رسيدگي' | G870='1401/12/29' | H870='
غیر فعال' | I870='دارای صورتهای مالی حسابرسی شده' | J870='*' | K870='*' | L870='*'
  row 871 [EMPTY]
  row 872 [EMPTY]
    MERGES A872:M872
  row 873 [SINGLE_TEXT n=1 columns=A]: A873='اطلاعات نمایش داده شده با اطلاعات امضا شده مطابقت دارد'
    MERGES A873:M873
  row 874 [EMPTY]
    MERGES A874:M874
  row 875 [EMPTY]
  row 876 [EMPTY]

SUMMARY bands_printed=37 compound_candidates=9

## WORKBOOK excel\samanBank.xlsx
Reader: ACCEPTED
SHA-256: 454985ba50ada23ee08ef7560ae1b892762b58b08375400f9536d797987cb4b5

### SHEET 1 Recovered_Sheet1 | used=A1:M489 | bands=32

[BAND 1] rows=11:12 columns=A,B,C,D,E,F,G,H,I,J,K merges=A11:A12,B12:C12,D12:E12,F12:G12,H12:I12,J12:K12
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=13; gap=none
  row 5 [EMPTY]
  row 6 [EMPTY]
  row 7 [EMPTY]
  row 8 [SINGLE_TEXT n=1 columns=A]: A8='اطلاعات این فرم گزیده ای از اطلاعات گزارش تفسیری مدیریت می باشد که ه...
    MERGES A8:K8
  row 9 [SINGLE_TEXT n=1 columns=A]: A9='مانده تسهیلات اعطایی و ذخیره مطالبات مشکوک الوصول:'
  row 10 [SINGLE_TEXT n=1 columns=A]: A10='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 11 [MULTI_TEXT n=11 columns=A,B,C,D,E,F,G,H,I,J,K]: A11='شرح' | B11='در تاریخ ۱۴۰۴/۱۲/۲۹' | C11='در تاریخ ۱۴۰۵/۰۶/
۳۱' | D11='در تاریخ ۱۴۰۴/۱۲/۲۹' | E11='در تاریخ ۱۴۰۵/۰۶/۳۱' | F11='در تاریخ ۱۴۰۴/۱۲/۲۹' | G11='در تاریخ ۱۴۰۵/۰۶/۳۱' | H1
1='در تاریخ ۱۴۰۴/۱۲/۲۹' | I11='در تاریخ ۱۴۰۵/۰۶/۳۱' | J11='در تاریخ ۱۴۰۴/۱۲/۲۹' | K11='در تاریخ ۱۴۰۵/۰۶/۳۱'
    MERGES A11:A12
  row 12 [MULTI_TEXT n=5 columns=B,D,F,H,J]: B12='جاری' | D12='سررسید گذشته' | F12='معوق' | H12='مشکوک الوصول' | J12='جم
ع'
    MERGES A11:A12,B12:C12,D12:E12,F12:G12,H12:I12,J12:K12
  row 13 [MIXED_NUMERIC n=11 columns=A,B,C,D,E,F,G,H,I,J,K]: A13='تسهیلات اعطایی و مطالبات از اشخاص دولتی ' | B13=0 | C1
3=0 | D13=0 | E13=0 | F13=0 | G13=0 | H13=0 | I13=0 | J13=0 | K13=0
  row 14 [MIXED_NUMERIC n=11 columns=A,B,C,D,E,F,G,H,I,J,K]: A14='تسهیلات اعطایی و مطالبات از اشخاص غیر دولتی- ریالی ' |
 B14=3893946956 | C14=5269432573 | D14=9335868 | E14=5496482 | F14=5521586 | G14=10536564 | H14=32532565 | I14=31768820
| J14=3941336975 | K14=5317234439
  row 15 [MIXED_NUMERIC n=11 columns=A,B,C,D,E,F,G,H,I,J,K]: A15='تسهیلات اعطایی و مطالبات از اشخاص غیر دولتی- ارزی ' |
B15=157877238 | C15=150604678 | D15=0 | E15=0 | F15=0 | G15=0 | H15=806606 | I15=4331861 | J15=158683844 | K15=154936539

  row 16 [MIXED_NUMERIC n=11 columns=A,B,C,D,E,F,G,H,I,J,K]: A16='جمع ' | B16=4051824194 | C16=5420037251 | D16=9335868
| E16=5496482 | F16=5521586 | G16=10536564 | H16=33339171 | I16=36100681 | J16=4100020819 | K16=5472170978
  row 17 [SINGLE_TEXT n=1 columns=A]: A17='کسر می شود: '
  row 18 [MIXED_NUMERIC n=11 columns=A,B,C,D,E,F,G,H,I,J,K]: A18='سود سالهای آتی ' | B18=598533682 | C18=800232054 | D18
=0 | E18=0 | F18=0 | G18=0 | H18=0 | I18=0 | J18=598533682 | K18=800232054

[BAND 2] rows=29:29 columns=A,C merges=A29:B29,C29:I29
  SIGNATURE=NO_MATCH
  PRIOR prior_body=27; gap=SINGLE_TEXT
  FOLLOWING next_body=None; gap=none
  row 23 [MIXED_NUMERIC n=7 columns=A,D,E,F,G,H,I]: A23='ضریب مبنای احتساب ذخیره اختصاصی (درصد) ' | D23=10 | E23=10 | F2
3=20 | G23=20 | H23=100 | I23=95
  row 24 [MIXED_NUMERIC n=9 columns=A,D,E,F,G,H,I,J,K]: A24='ذخیره اختصاصی مطالبات مشکوک الوصول ' | D24=576707 | E24=400
369 | F24=914070 | G24=1459552 | H24=28536282 | I24=30083853 | J24=30027059 | K24=31943774
  row 25 [MIXED_NUMERIC n=11 columns=A,B,C,D,E,F,G,H,I,J,K]: A25='مانده مبنای محاسبه ذخیره عمومی ' | B25=3382253993 | C2
5=4583690119 | D25=7062395 | E25=4666664 | F25=4386862 | G25=6635082 | H25=636901 | I25=1467238 | J25=3394340151 | K25=4
596459103
  row 26 [MIXED_NUMERIC n=11 columns=A,B,C,D,E,F,G,H,I,J,K]: A26='ذخیره عمومی مطالبات مشکوک الوصول ' | B26=62739105 | C2
6=68702958 | D26=29976 | E26=9874 | F26=11255 | G26=50734 | H26=30437 | I26=20436 | J26=62810773 | K26=68784002
  row 27 [MIXED_NUMERIC n=11 columns=A,B,C,D,E,F,G,H,I,J,K]: A27='جمع ' | B27=3319514888 | C27=4514987161 | D27=7032419
| E27=4656790 | F27=4375607 | G27=6584348 | H27=606464 | I27=1446802 | J27=3331529378 | K27=4527675101
  row 28 [SINGLE_TEXT n=1 columns=A]: A28='برآورد شرکت از تغییرات در نرخ سود تسهیلات اعطایی :'
  row 29 [MULTI_TEXT n=2 columns=A,C]: A29='دوره ۶ ماهه منتهي به ۱۴۰۵/۱۲/۲۹ ' | C29='سود تسهیلات تابع سیاستهای شورای پول
 و اعتبار و همچنین در چارچوب بخشن...
    MERGES A29:B29,C29:I29
  row 30 [EMPTY]
  row 31 [SINGLE_TEXT n=1 columns=A]: A31='برآورد شرکت از تغییرات در مانده تسهیلات :'
  row 32 [MULTI_TEXT n=2 columns=A,C]: A32='دوره ۶ ماهه منتهي به ۱۴۰۵/۱۲/۲۹ ' | C32='باتوجه به دستورالعمل کنترل مقداری ت
رازنامه بانکها و پیش بینی افزایش ...
    MERGES A32:B32,C32:I32
  row 33 [EMPTY]
  row 34 [SINGLE_TEXT n=1 columns=A]: A34='برآورد شرکت از تغییرات در مانده ذخایر مطالبات مشکوک الوصول :'
  row 35 [MULTI_TEXT n=2 columns=A,C]: A35='دوره ۶ ماهه منتهي به ۱۴۰۵/۱۲/۲۹ ' | C35='افزایش در ذخیره مطالبات مشکوک الوصو
ل ناشی از افزایش ذخیره عام که تاب...
    MERGES A35:B35,C35:I35

[BAND 3] rows=32:32 columns=A,C merges=A32:B32,C32:I32
  SIGNATURE=NO_MATCH
  PRIOR prior_body=27; gap=SINGLE_TEXT,MULTI_TEXT,EMPTY,SINGLE_TEXT
  FOLLOWING next_body=None; gap=none
  row 26 [MIXED_NUMERIC n=11 columns=A,B,C,D,E,F,G,H,I,J,K]: A26='ذخیره عمومی مطالبات مشکوک الوصول ' | B26=62739105 | C2
6=68702958 | D26=29976 | E26=9874 | F26=11255 | G26=50734 | H26=30437 | I26=20436 | J26=62810773 | K26=68784002
  row 27 [MIXED_NUMERIC n=11 columns=A,B,C,D,E,F,G,H,I,J,K]: A27='جمع ' | B27=3319514888 | C27=4514987161 | D27=7032419
| E27=4656790 | F27=4375607 | G27=6584348 | H27=606464 | I27=1446802 | J27=3331529378 | K27=4527675101
  row 28 [SINGLE_TEXT n=1 columns=A]: A28='برآورد شرکت از تغییرات در نرخ سود تسهیلات اعطایی :'
  row 29 [MULTI_TEXT n=2 columns=A,C]: A29='دوره ۶ ماهه منتهي به ۱۴۰۵/۱۲/۲۹ ' | C29='سود تسهیلات تابع سیاستهای شورای پول
 و اعتبار و همچنین در چارچوب بخشن...
    MERGES A29:B29,C29:I29
  row 30 [EMPTY]
  row 31 [SINGLE_TEXT n=1 columns=A]: A31='برآورد شرکت از تغییرات در مانده تسهیلات :'
  row 32 [MULTI_TEXT n=2 columns=A,C]: A32='دوره ۶ ماهه منتهي به ۱۴۰۵/۱۲/۲۹ ' | C32='باتوجه به دستورالعمل کنترل مقداری ت
رازنامه بانکها و پیش بینی افزایش ...
    MERGES A32:B32,C32:I32
  row 33 [EMPTY]
  row 34 [SINGLE_TEXT n=1 columns=A]: A34='برآورد شرکت از تغییرات در مانده ذخایر مطالبات مشکوک الوصول :'
  row 35 [MULTI_TEXT n=2 columns=A,C]: A35='دوره ۶ ماهه منتهي به ۱۴۰۵/۱۲/۲۹ ' | C35='افزایش در ذخیره مطالبات مشکوک الوصو
ل ناشی از افزایش ذخیره عام که تاب...
    MERGES A35:B35,C35:I35
  row 36 [EMPTY]
  row 37 [SINGLE_TEXT n=1 columns=A]: A37='مانده سپرده های دریافتی از مشتریان :'
  row 38 [SINGLE_TEXT n=1 columns=A]: A38='کلیه مبالغ درج شده به میلیون ریال می باشد'

[BAND 4] rows=35:35 columns=A,C merges=A35:B35,C35:I35
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=None; gap=none
  row 29 [MULTI_TEXT n=2 columns=A,C]: A29='دوره ۶ ماهه منتهي به ۱۴۰۵/۱۲/۲۹ ' | C29='سود تسهیلات تابع سیاستهای شورای پول
 و اعتبار و همچنین در چارچوب بخشن...
    MERGES A29:B29,C29:I29
  row 30 [EMPTY]
  row 31 [SINGLE_TEXT n=1 columns=A]: A31='برآورد شرکت از تغییرات در مانده تسهیلات :'
  row 32 [MULTI_TEXT n=2 columns=A,C]: A32='دوره ۶ ماهه منتهي به ۱۴۰۵/۱۲/۲۹ ' | C32='باتوجه به دستورالعمل کنترل مقداری ت
رازنامه بانکها و پیش بینی افزایش ...
    MERGES A32:B32,C32:I32
  row 33 [EMPTY]
  row 34 [SINGLE_TEXT n=1 columns=A]: A34='برآورد شرکت از تغییرات در مانده ذخایر مطالبات مشکوک الوصول :'
  row 35 [MULTI_TEXT n=2 columns=A,C]: A35='دوره ۶ ماهه منتهي به ۱۴۰۵/۱۲/۲۹ ' | C35='افزایش در ذخیره مطالبات مشکوک الوصو
ل ناشی از افزایش ذخیره عام که تاب...
    MERGES A35:B35,C35:I35
  row 36 [EMPTY]
  row 37 [SINGLE_TEXT n=1 columns=A]: A37='مانده سپرده های دریافتی از مشتریان :'
  row 38 [SINGLE_TEXT n=1 columns=A]: A38='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 39 [MULTI_TEXT n=4 columns=A,B,D,F]: A39='شرح' | B39='مانده سپرده ها' | D39='متوسط نرخ سود مانده سپرده ها' | F39='
برآورد مدیریت از تغییر در نرخ سود سپرده ها و تغییر در مانده سپرده ها...
    MERGES A39:A40,B39:C39,D39:E39,F39:F40
  row 40 [MULTI_TEXT n=4 columns=B,C,D,E]: B40='در تاریخ ۱۴۰۴/۱۲/۲۹' | C40='در تاریخ ۱۴۰۵/۰۶/۳۱' | D40='در تاریخ ۱۴۰۴/۱۲
/۲۹' | E40='در تاریخ ۱۴۰۵/۰۶/۳۱'
    MERGES A39:A40,F39:F40
  row 41 [SINGLE_TEXT n=1 columns=A]: A41='سپرده های ریالی: '

[BAND 5] rows=39:40 columns=A,B,C,D,E,F merges=A39:A40,B39:C39,D39:E39,F39:F40
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=42; gap=SINGLE_TEXT
  row 33 [EMPTY]
  row 34 [SINGLE_TEXT n=1 columns=A]: A34='برآورد شرکت از تغییرات در مانده ذخایر مطالبات مشکوک الوصول :'
  row 35 [MULTI_TEXT n=2 columns=A,C]: A35='دوره ۶ ماهه منتهي به ۱۴۰۵/۱۲/۲۹ ' | C35='افزایش در ذخیره مطالبات مشکوک الوصو
ل ناشی از افزایش ذخیره عام که تاب...
    MERGES A35:B35,C35:I35
  row 36 [EMPTY]
  row 37 [SINGLE_TEXT n=1 columns=A]: A37='مانده سپرده های دریافتی از مشتریان :'
  row 38 [SINGLE_TEXT n=1 columns=A]: A38='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 39 [MULTI_TEXT n=4 columns=A,B,D,F]: A39='شرح' | B39='مانده سپرده ها' | D39='متوسط نرخ سود مانده سپرده ها' | F39='
برآورد مدیریت از تغییر در نرخ سود سپرده ها و تغییر در مانده سپرده ها...
    MERGES A39:A40,B39:C39,D39:E39,F39:F40
  row 40 [MULTI_TEXT n=4 columns=B,C,D,E]: B40='در تاریخ ۱۴۰۴/۱۲/۲۹' | C40='در تاریخ ۱۴۰۵/۰۶/۳۱' | D40='در تاریخ ۱۴۰۴/۱۲
/۲۹' | E40='در تاریخ ۱۴۰۵/۰۶/۳۱'
    MERGES A39:A40,F39:F40
  row 41 [SINGLE_TEXT n=1 columns=A]: A41='سپرده های ریالی: '
  row 42 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A42='سپرده های کوتاه مدت ' | B42=2336402133 | C42=2924929498 | D42=7 |
 E42=10 | F42='متناسب با بخشنامه های بانک مرکزی و در محدوده مجاز میباشد. '
  row 43 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A43='سپرده های کوتاه مدت ویژه ' | B43=7300546 | C43=10410409 | D43=14
| E43=13 | F43='متناسب با بخشنامه های بانک مرکزی و در محدوده مجاز میباشد. '
  row 44 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A44='سپرده های بلند مدت ' | B44=1714598608 | C44=1943998290 | D44=26 |
 E44=26 | F44='متناسب با بخشنامه های بانک مرکزی و در محدوده مجاز میباشد. '
  row 45 [MIXED_NUMERIC n=3 columns=A,B,C]: A45='جمع سپرده های هزینه زا ' | B45=4058301287 | C45=4879338197
  row 46 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A46='سپرده های غیر هزینه زا ' | B46=1050793679 | C46=1391380906 | D46=
0 | E46=0 | F46='طبق افزایش نرخ رشد نقدینگی در کشور و نیز برنامه های بانک برای جذب سپ...

[BAND 6] rows=52:52 columns=A,B,C,D,E,F merges=—
  SIGNATURE=COMPOUND_CANDIDATE
  PRIOR prior_body=49; gap=SINGLE_TEXT,SINGLE_TEXT
  FOLLOWING next_body=53; gap=none
  row 46 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A46='سپرده های غیر هزینه زا ' | B46=1050793679 | C46=1391380906 | D46=
0 | E46=0 | F46='طبق افزایش نرخ رشد نقدینگی در کشور و نیز برنامه های بانک برای جذب سپ...
  row 47 [MIXED_NUMERIC n=3 columns=A,B,C]: A47='جمع سپرده های ریالی ' | B47=5109094966 | C47=6270719103
  row 48 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A48='سپرده های ارزی ' | B48=1076376399 | C48=1648885982 | D48=0 | E48=
0 | F48='طبق افزایش نرخ رشد نقدینگی در کشور و نیز برنامه های بانک برای جذب سپ...
  row 49 [MIXED_NUMERIC n=3 columns=A,B,C]: A49='جمع سپرده های دریافتی ' | B49=6185471365 | C49=7919605085
    MERGES D49:J49
  row 50 [SINGLE_TEXT n=1 columns=A]: A50='اقلام زیر خط:'
  row 51 [SINGLE_TEXT n=1 columns=A]: A51='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 52 [MULTI_TEXT n=6 columns=A,B,C,D,E,F]: A52='شرح' | B52='۱۴۰۵/۰۶/۳۱' | C52='۱۴۰۴/۱۲/۲۹' | D52='شرح' | E52='۱۴۰۵/۰
۶/۳۱' | F52='۱۴۰۴/۱۲/۲۹'
  row 53 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A53='تعهدات مشتریان بابت اعتبارات اسنادی ' | B53=81068897 | C53=475018
77 | D53='تعهدات بانک بابت اعتبارات اسنادی ' | E53=81068897 | F53=47501877
  row 54 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A54='تعهدات مشتریان بابت ضمانت نامه های صادره ' | B54=645477988 | C54=
460435223 | D54='تعهدات بانک بابت ضمانت نامه های صادره ' | E54=645477988 | F54=460435223
  row 55 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A55='ساير تعهدات مشتريان بانک ' | B55=773952249 | C55=636283171 | D55=
'سایر تعهدات بانک ' | E55=773952249 | F55=636283171
  row 56 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A56='وجوه اداره شده و موارد مشابه ' | B56=498309 | C56=644136 | D56='و
جوه اداره شده و موارد مشابه ' | E56=498309 | F56=644136
  row 57 [MULTI_TEXT n=2 columns=A,B]: A57='توضیحات در خصوص تغییرات بااهمیت: ' | B57='تعهدات ایجاد شده متناسب با درخواست
 مشتریان و سیاستهای کلان اقتصادی و...
    MERGES B57:F57
  row 58 [SINGLE_TEXT n=1 columns=A]: A58='«جملات آینده\u200cنگر نشان\u200cدهنده انتظارات، باورها یا پیش\u200cب...
    MERGES A58:I58

[BAND 7] rows=57:57 columns=A,B merges=B57:F57
  SIGNATURE=NO_MATCH
  PRIOR prior_body=56; gap=none
  FOLLOWING next_body=None; gap=none
  row 51 [SINGLE_TEXT n=1 columns=A]: A51='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 52 [MULTI_TEXT n=6 columns=A,B,C,D,E,F]: A52='شرح' | B52='۱۴۰۵/۰۶/۳۱' | C52='۱۴۰۴/۱۲/۲۹' | D52='شرح' | E52='۱۴۰۵/۰
۶/۳۱' | F52='۱۴۰۴/۱۲/۲۹'
  row 53 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A53='تعهدات مشتریان بابت اعتبارات اسنادی ' | B53=81068897 | C53=475018
77 | D53='تعهدات بانک بابت اعتبارات اسنادی ' | E53=81068897 | F53=47501877
  row 54 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A54='تعهدات مشتریان بابت ضمانت نامه های صادره ' | B54=645477988 | C54=
460435223 | D54='تعهدات بانک بابت ضمانت نامه های صادره ' | E54=645477988 | F54=460435223
  row 55 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A55='ساير تعهدات مشتريان بانک ' | B55=773952249 | C55=636283171 | D55=
'سایر تعهدات بانک ' | E55=773952249 | F55=636283171
  row 56 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A56='وجوه اداره شده و موارد مشابه ' | B56=498309 | C56=644136 | D56='و
جوه اداره شده و موارد مشابه ' | E56=498309 | F56=644136
  row 57 [MULTI_TEXT n=2 columns=A,B]: A57='توضیحات در خصوص تغییرات بااهمیت: ' | B57='تعهدات ایجاد شده متناسب با درخواست
 مشتریان و سیاستهای کلان اقتصادی و...
    MERGES B57:F57
  row 58 [SINGLE_TEXT n=1 columns=A]: A58='«جملات آینده\u200cنگر نشان\u200cدهنده انتظارات، باورها یا پیش\u200cب...
    MERGES A58:I58
  row 59 [EMPTY]
  row 60 [EMPTY]
  row 61 [EMPTY]
  row 62 [SINGLE_TEXT n=1 columns=A]: A62='خلاصه اطلاعات گزارش تفسیری - صفحه 2'
  row 63 [EMPTY]

[BAND 8] rows=70:70 columns=A,B,C,D merges=—
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=71; gap=none
  row 64 [EMPTY]
  row 65 [EMPTY]
  row 66 [EMPTY]
  row 67 [SINGLE_TEXT n=1 columns=A]: A67='اطلاعات این فرم گزیده ای از اطلاعات گزارش تفسیری مدیریت می باشد که ه...
  row 68 [SINGLE_TEXT n=1 columns=A]: A68='وضعیت کارکنان:'
  row 69 [SINGLE_TEXT n=1 columns=A]: A69='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 70 [MULTI_TEXT n=4 columns=A,B,C,D]: A70='شرح' | B70='در تاریخ ۱۴۰۵/۰۶/۳۱' | C70='در تاریخ ۱۴۰۴/۰۶/۳۱' | D70='برآو
رد در تاریخ ۱۴۰۵/۱۲/۲۹'
  row 71 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A71='تعداد شعب ' | B71=137 | C71=137 | D71=137
  row 72 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A72='تعداد کارکنان ' | B72=2790 | C72=2817 | D72=2790
  row 73 [SINGLE_TEXT n=1 columns=A]: A73='اطلاعات حق الوکاله و کفایت سرمایه'
  row 74 [SINGLE_TEXT n=1 columns=A]: A74='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 75 [MULTI_TEXT n=4 columns=A,B,C,D]: A75='شرح' | B75='دوره ۶ ماهه منتهی به ۱۴۰۵/۰۶/۳۱' | C75='دوره ۶ ماهه منتهی به
 ۱۴۰۴/۰۶/۳۱' | D75='برآورد تغییر روند در دوره ۶ ماهه منتهی به ۱۴۰۵/۱۲/۲۹'
    MERGES D75:E75
  row 76 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A76='سهم بانک از درآمدهای مشاع ' | B76=49624172 | C76=23107577 | D76='پیش
بینی میشود روند سالهای قبل در سال ۱۴۰۵ادامه داشته باشد. '
    MERGES D76:E76

[BAND 9] rows=75:75 columns=A,B,C,D merges=D75:E75
  SIGNATURE=COMPOUND_CANDIDATE
  PRIOR prior_body=72; gap=SINGLE_TEXT,SINGLE_TEXT
  FOLLOWING next_body=76; gap=none
  row 69 [SINGLE_TEXT n=1 columns=A]: A69='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 70 [MULTI_TEXT n=4 columns=A,B,C,D]: A70='شرح' | B70='در تاریخ ۱۴۰۵/۰۶/۳۱' | C70='در تاریخ ۱۴۰۴/۰۶/۳۱' | D70='برآو
رد در تاریخ ۱۴۰۵/۱۲/۲۹'
  row 71 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A71='تعداد شعب ' | B71=137 | C71=137 | D71=137
  row 72 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A72='تعداد کارکنان ' | B72=2790 | C72=2817 | D72=2790
  row 73 [SINGLE_TEXT n=1 columns=A]: A73='اطلاعات حق الوکاله و کفایت سرمایه'
  row 74 [SINGLE_TEXT n=1 columns=A]: A74='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 75 [MULTI_TEXT n=4 columns=A,B,C,D]: A75='شرح' | B75='دوره ۶ ماهه منتهی به ۱۴۰۵/۰۶/۳۱' | C75='دوره ۶ ماهه منتهی به
 ۱۴۰۴/۰۶/۳۱' | D75='برآورد تغییر روند در دوره ۶ ماهه منتهی به ۱۴۰۵/۱۲/۲۹'
    MERGES D75:E75
  row 76 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A76='سهم بانک از درآمدهای مشاع ' | B76=49624172 | C76=23107577 | D76='پیش
بینی میشود روند سالهای قبل در سال ۱۴۰۵ادامه داشته باشد. '
    MERGES D76:E76
  row 77 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A77='سهم سپرده گذاران از درآمدهای مشاع ' | B77=458895930 | C77=236433874 |
 D77='پیش بینی میشود روند سالهای قبل در سال ۱۴۰۵ادامه داشته باشد. '
    MERGES D77:E77
  row 78 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A78='نرخ حق الوکاله اعلام شده ' | B78=3 | C78=3 | D78='معادل ۳ درصد در سال
 خواهد بود. '
    MERGES D78:E78
  row 79 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A79='مبلغ حق الوکاله اعمال شده ' | B79=56600082 | C79=32115462 | D79='معاد
ل نرخ حق الوکاله اعلام شده با اعمال دوره زمانی سپری شده طی سال م...
    MERGES D79:E79
  row 80 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A80='مابه التفاوت سود قابل پرداخت (مازاد سود پرداختی) به سپرده گذاران ' |
B80=-410512 | C80=-8347186 | D80='برای سال ۱۴۰۵ پیش بینی میشود روند سالهای قبل ادامه داشته باشد. '
    MERGES D80:E80
  row 81 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A81='نسبت کفایت سرمایه ' | B81=0 | C81=10 | D81='آخرین نسبت کفایت سرمایه ح
سابرسی شده معادل ۱۱.۰۵درصد میباشد '
    MERGES D81:E81

[BAND 10] rows=83:83 columns=A,B merges=—
  SIGNATURE=NO_MATCH
  PRIOR prior_body=81; gap=SINGLE_TEXT
  FOLLOWING next_body=87; gap=SINGLE_TEXT,MULTI_TEXT,SINGLE_TEXT
  row 77 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A77='سهم سپرده گذاران از درآمدهای مشاع ' | B77=458895930 | C77=236433874 |
 D77='پیش بینی میشود روند سالهای قبل در سال ۱۴۰۵ادامه داشته باشد. '
    MERGES D77:E77
  row 78 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A78='نرخ حق الوکاله اعلام شده ' | B78=3 | C78=3 | D78='معادل ۳ درصد در سال
 خواهد بود. '
    MERGES D78:E78
  row 79 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A79='مبلغ حق الوکاله اعمال شده ' | B79=56600082 | C79=32115462 | D79='معاد
ل نرخ حق الوکاله اعلام شده با اعمال دوره زمانی سپری شده طی سال م...
    MERGES D79:E79
  row 80 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A80='مابه التفاوت سود قابل پرداخت (مازاد سود پرداختی) به سپرده گذاران ' |
B80=-410512 | C80=-8347186 | D80='برای سال ۱۴۰۵ پیش بینی میشود روند سالهای قبل ادامه داشته باشد. '
    MERGES D80:E80
  row 81 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A81='نسبت کفایت سرمایه ' | B81=0 | C81=10 | D81='آخرین نسبت کفایت سرمایه ح
سابرسی شده معادل ۱۱.۰۵درصد میباشد '
    MERGES D81:E81
  row 82 [SINGLE_TEXT n=1 columns=A]: A82='اهداف و راهبردهای آتی مدیریت در خصوص فعالیت شرکت:'
  row 83 [MULTI_TEXT n=2 columns=A,B]: A83='اهداف و راهبردهای آتی مدیریت در خصوص فعالیت شرکت: ' | B83='به شرح مندرج در گ
زارش تفسیری مدیریت پیوست '
  row 84 [SINGLE_TEXT n=1 columns=A]: A84='درآمد حاصل از تسهیلات اعطایی و سپرده گذاری'
  row 85 [MULTI_TEXT n=6 columns=A,B,C,D,E,F]: A85='شرح' | B85='دوره ۶ ماهه منتهی به ۱۴۰۵/۰۶/۳۱' | C85='متوسط نرخ سود دو
ره ۶ ماهه منتهی به ۱۴۰۵/۰۶/۳۱ (درصد)' | D85='دوره ۶ ماهه منتهی به ۱۴۰۴/۰۶/۳۱' | E85='متوسط نرخ سود دوره ۶ ماهه منتهی به
۱۴۰۴/۰۶/۳۱ (درصد)' | F85='برآورد تغییر روند در دوره ۶ ماهه منتهی به ۱۴۰۵/۱۲/۲۹'
    MERGES F85:G85
  row 86 [SINGLE_TEXT n=1 columns=A]: A86='درآمد تسهیلات اعطایی: '
    MERGES F86:G86
  row 87 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A87='فروش اقساطی ' | B87=12849695 | C87=0 | D87=6871282 | E87=0 | F87=
'طبق سیاستهای شورای پول و اعتبار و بخشنامه های بانک مرکزی '
    MERGES F87:G87
  row 88 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A88='جعاله ' | B88=44913856 | C88=0 | D88=8182100 | E88=0 | F88='طبق س
یاستهای شورای پول و اعتبار و بخشنامه های بانک مرکزی '
    MERGES F88:G88
  row 89 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A89='اجاره به شرط تملیک ' | B89=614904 | C89=0 | D89=8930 | E89=0 | F8
9='طبق سیاستهای شورای پول و اعتبار و بخشنامه های بانک مرکزی '
    MERGES F89:G89

[BAND 11] rows=85:85 columns=A,B,C,D,E,F merges=F85:G85
  SIGNATURE=NO_MATCH
  PRIOR prior_body=81; gap=SINGLE_TEXT,MULTI_TEXT,SINGLE_TEXT
  FOLLOWING next_body=87; gap=SINGLE_TEXT
  row 79 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A79='مبلغ حق الوکاله اعمال شده ' | B79=56600082 | C79=32115462 | D79='معاد
ل نرخ حق الوکاله اعلام شده با اعمال دوره زمانی سپری شده طی سال م...
    MERGES D79:E79
  row 80 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A80='مابه التفاوت سود قابل پرداخت (مازاد سود پرداختی) به سپرده گذاران ' |
B80=-410512 | C80=-8347186 | D80='برای سال ۱۴۰۵ پیش بینی میشود روند سالهای قبل ادامه داشته باشد. '
    MERGES D80:E80
  row 81 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A81='نسبت کفایت سرمایه ' | B81=0 | C81=10 | D81='آخرین نسبت کفایت سرمایه ح
سابرسی شده معادل ۱۱.۰۵درصد میباشد '
    MERGES D81:E81
  row 82 [SINGLE_TEXT n=1 columns=A]: A82='اهداف و راهبردهای آتی مدیریت در خصوص فعالیت شرکت:'
  row 83 [MULTI_TEXT n=2 columns=A,B]: A83='اهداف و راهبردهای آتی مدیریت در خصوص فعالیت شرکت: ' | B83='به شرح مندرج در گ
زارش تفسیری مدیریت پیوست '
  row 84 [SINGLE_TEXT n=1 columns=A]: A84='درآمد حاصل از تسهیلات اعطایی و سپرده گذاری'
  row 85 [MULTI_TEXT n=6 columns=A,B,C,D,E,F]: A85='شرح' | B85='دوره ۶ ماهه منتهی به ۱۴۰۵/۰۶/۳۱' | C85='متوسط نرخ سود دو
ره ۶ ماهه منتهی به ۱۴۰۵/۰۶/۳۱ (درصد)' | D85='دوره ۶ ماهه منتهی به ۱۴۰۴/۰۶/۳۱' | E85='متوسط نرخ سود دوره ۶ ماهه منتهی به
۱۴۰۴/۰۶/۳۱ (درصد)' | F85='برآورد تغییر روند در دوره ۶ ماهه منتهی به ۱۴۰۵/۱۲/۲۹'
    MERGES F85:G85
  row 86 [SINGLE_TEXT n=1 columns=A]: A86='درآمد تسهیلات اعطایی: '
    MERGES F86:G86
  row 87 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A87='فروش اقساطی ' | B87=12849695 | C87=0 | D87=6871282 | E87=0 | F87=
'طبق سیاستهای شورای پول و اعتبار و بخشنامه های بانک مرکزی '
    MERGES F87:G87
  row 88 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A88='جعاله ' | B88=44913856 | C88=0 | D88=8182100 | E88=0 | F88='طبق س
یاستهای شورای پول و اعتبار و بخشنامه های بانک مرکزی '
    MERGES F88:G88
  row 89 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A89='اجاره به شرط تملیک ' | B89=614904 | C89=0 | D89=8930 | E89=0 | F8
9='طبق سیاستهای شورای پول و اعتبار و بخشنامه های بانک مرکزی '
    MERGES F89:G89
  row 90 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A90='سلف ' | B90=0 | C90=0 | D90=962 | E90=0 | F90='طبق سیاستهای شورای
 پول و اعتبار و بخشنامه های بانک مرکزی '
    MERGES F90:G90
  row 91 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A91='مضاربه ' | B91=303392 | C91=0 | D91=427207 | E91=0 | F91='طبق سیا
ستهای شورای پول و اعتبار و بخشنامه های بانک مرکزی '
    MERGES F91:G91

[BAND 12] rows=105:105 columns=A,C merges=A105:B105,C105:I105
  SIGNATURE=NO_MATCH
  PRIOR prior_body=104; gap=none
  FOLLOWING next_body=108; gap=SINGLE_TEXT,MULTI_TEXT
  row 99 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A99='جمع درآمد حاصل از تسهیلات اعطایی ' | B99=432843600 | C99=0 | D99=24
2014199 | E99=0
    MERGES F99:G99
  row 100 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A100='جایزه سپرده قانونی ' | B100=4663922 | C100=0 | D100=2207129 | E
100=0 | F100='متناسب با مانده جذب سپرده ها '
    MERGES F100:G100
  row 101 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A101='سود حاصل از سپرده گذاری در بانکها ' | B101=45119484 | C101=0 |
D101=10944795 | E101=0 | F101='متناسب با وجوه مازاد در سیاستهای بانک درمدیریت نقدینگی '
    MERGES F101:G101
  row 102 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A102='جمع سود حاصل از سپرده گذاری ها ' | B102=49783406 | C102=0 | D102=
13151924 | E102=0
    MERGES F102:G102
  row 103 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A103='درآمد اوراق بدهی و سایر درآمدهای ناشی از سپرده گذاری ' | B103=3
1489756 | C103=0 | D103=12222406 | E103=0 | F103='متناسب با مازاد نقدینگی در سال ۱۴۰۵ '
    MERGES F103:G103
  row 104 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A104='درآمد حاصل ازتسهیلات اعطایی و سپرده\u200cگذاری\u200cها ' | B104=5
14116762 | C104=0 | D104=267388529 | E104=0
    MERGES F104:G104
  row 105 [MULTI_TEXT n=2 columns=A,C]: A105='ارائه توضیحات در خصوص نحوه محاسبه متوسط نرخ سود تسهیلات: ' | C105='نرخ سود
 تسهیلات متناسب با بخشنامه ها و در چارچوب قوانین بانک مرکزی م...
    MERGES A105:B105,C105:I105
  row 106 [SINGLE_TEXT n=1 columns=A]: A106='خالص سود (زیان) سرمایه گذاری\u200c ها'
  row 107 [MULTI_TEXT n=4 columns=A,B,C,D]: A107='شرح' | B107='دوره ۶ ماهه منتهی به ۱۴۰۵/۰۶/۳۱' | C107='دوره ۶ ماهه منته
ی به ۱۴۰۴/۰۶/۳۱' | D107='برآورد تغییر روند در دوره ۶ ماهه منتهی به ۱۴۰۵/۱۲/۲۹'
    MERGES D107:E107
  row 108 [MIXED_NUMERIC n=3 columns=A,B,C]: A108='درآمد حاصل از سرمایه گذاری در سهام ' | B108=11253110 | C108=2536016
    MERGES D108:E108
  row 109 [MIXED_NUMERIC n=3 columns=A,B,C]: A109='سود(زیان) حاصل از فروش سرمایه گذاری ' | B109=5738603 | C109=214739
    MERGES D109:E109
  row 110 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A110='سود (زیان) تعدیل ذخیره کاهش ارزش سرمایه گذاریها ' | B110=0 | C110=0
 | D110='باتوجه به ترکیب سرمایه گذاریهای بانک در سال ۱۴۰۵ متاثر از میزان سودا...
    MERGES D110:E110
  row 111 [MIXED_NUMERIC n=3 columns=A,B,C]: A111='جمع درآمدهای حاصل از سرمایه گذاری ' | B111=16991713 | C111=2750755
    MERGES D111:E111

[BAND 13] rows=107:107 columns=A,B,C,D merges=D107:E107
  SIGNATURE=NO_MATCH
  PRIOR prior_body=104; gap=MULTI_TEXT,SINGLE_TEXT
  FOLLOWING next_body=108; gap=none
  row 101 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A101='سود حاصل از سپرده گذاری در بانکها ' | B101=45119484 | C101=0 |
D101=10944795 | E101=0 | F101='متناسب با وجوه مازاد در سیاستهای بانک درمدیریت نقدینگی '
    MERGES F101:G101
  row 102 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A102='جمع سود حاصل از سپرده گذاری ها ' | B102=49783406 | C102=0 | D102=
13151924 | E102=0
    MERGES F102:G102
  row 103 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A103='درآمد اوراق بدهی و سایر درآمدهای ناشی از سپرده گذاری ' | B103=3
1489756 | C103=0 | D103=12222406 | E103=0 | F103='متناسب با مازاد نقدینگی در سال ۱۴۰۵ '
    MERGES F103:G103
  row 104 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A104='درآمد حاصل ازتسهیلات اعطایی و سپرده\u200cگذاری\u200cها ' | B104=5
14116762 | C104=0 | D104=267388529 | E104=0
    MERGES F104:G104
  row 105 [MULTI_TEXT n=2 columns=A,C]: A105='ارائه توضیحات در خصوص نحوه محاسبه متوسط نرخ سود تسهیلات: ' | C105='نرخ سود
 تسهیلات متناسب با بخشنامه ها و در چارچوب قوانین بانک مرکزی م...
    MERGES A105:B105,C105:I105
  row 106 [SINGLE_TEXT n=1 columns=A]: A106='خالص سود (زیان) سرمایه گذاری\u200c ها'
  row 107 [MULTI_TEXT n=4 columns=A,B,C,D]: A107='شرح' | B107='دوره ۶ ماهه منتهی به ۱۴۰۵/۰۶/۳۱' | C107='دوره ۶ ماهه منته
ی به ۱۴۰۴/۰۶/۳۱' | D107='برآورد تغییر روند در دوره ۶ ماهه منتهی به ۱۴۰۵/۱۲/۲۹'
    MERGES D107:E107
  row 108 [MIXED_NUMERIC n=3 columns=A,B,C]: A108='درآمد حاصل از سرمایه گذاری در سهام ' | B108=11253110 | C108=2536016
    MERGES D108:E108
  row 109 [MIXED_NUMERIC n=3 columns=A,B,C]: A109='سود(زیان) حاصل از فروش سرمایه گذاری ' | B109=5738603 | C109=214739
    MERGES D109:E109
  row 110 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A110='سود (زیان) تعدیل ذخیره کاهش ارزش سرمایه گذاریها ' | B110=0 | C110=0
 | D110='باتوجه به ترکیب سرمایه گذاریهای بانک در سال ۱۴۰۵ متاثر از میزان سودا...
    MERGES D110:E110
  row 111 [MIXED_NUMERIC n=3 columns=A,B,C]: A111='جمع درآمدهای حاصل از سرمایه گذاری ' | B111=16991713 | C111=2750755
    MERGES D111:E111
  row 112 [SINGLE_TEXT n=1 columns=A]: A112='«جملات آینده\u200cنگر نشان\u200cدهنده انتظارات، باورها یا پیش\u200cب...
  row 113 [EMPTY]

[BAND 14] rows=124:125 columns=A,C,D,E,F,G,H,I,J merges=A124:B125,C124:F124,G124:I124,J124:K125
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=126; gap=none
  row 118 [EMPTY]
  row 119 [EMPTY]
  row 120 [EMPTY]
  row 121 [SINGLE_TEXT n=1 columns=A]: A121='اطلاعات این فرم گزیده ای از اطلاعات گزارش تفسیری مدیریت می باشد که ه...
  row 122 [SINGLE_TEXT n=1 columns=A]: A122='وضعیت شرکتهای سرمایه پذیر:'
  row 123 [SINGLE_TEXT n=1 columns=A]: A123='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 124 [MULTI_TEXT n=4 columns=A,C,G,J]: A124='نام شرکت' | C124='دوره ۶ ماهه منتهي به ۱۴۰۵/۰۶/۳۱' | G124='دوره ۶ ماهه
 منتهي به ۱۴۰۴/۰۶/۳۱' | J124='تشریح آخرین وضعیت و برنامه های آتی شرکت در شرکت سرمایه پذیر'
    MERGES A124:B125,C124:F124,G124:I124,J124:K125
  row 125 [MULTI_TEXT n=7 columns=C,D,E,F,G,H,I]: C125='درصد مالکیت' | D125='بهای تمام شده' | E125='سال مالی شرکت سرمایه
 پذیر' | F125='درآمد سرمایه گذاری - میلیون ریال' | G125='درصد مالکیت' | H125='بهای تمام شده' | I125='درآمد سرمایه گذاری
- میلیون ریال'
    MERGES A124:B125,J124:K125
  row 126 [MIXED_NUMERIC n=9 columns=A,C,D,E,F,G,H,I,J]: A126='سازمان بورس و اوراق بهادار ' | C126=0 | D126=0 | E126='۱۴
۰۵/۱۲/۲۹ ' | F126=0 | G126=0 | H126=0 | I126=6929 | J126='مطابق روند سالهای قبل '
    MERGES A126:B126,J126:K126
  row 127 [MIXED_NUMERIC n=9 columns=A,C,D,E,F,G,H,I,J]: A127='بورس انرژي ايران (بورس انرژي) ' | C127=0 | D127=0 | E127=
'۱۴۰۵/۱۲/۲۹ ' | F127=0 | G127=0 | H127=0 | I127=174490 | J127='مطابق روند سالهای قبل '
    MERGES A127:B127,J127:K127
  row 128 [MIXED_NUMERIC n=9 columns=A,C,D,E,F,G,H,I,J]: A128='پرداخت الکترونيک سامان کيش ' | C128=57 | D128=19619165 |
E128='۱۴۰۵/۰۹/۳۰ ' | F128=0 | G128=57 | H128=19619165 | I128=0 | J128='مطابق روند سالهای قبل '
    MERGES A128:B128,J128:K128
  row 129 [MIXED_NUMERIC n=9 columns=A,C,D,E,F,G,H,I,J]: A129='سپرده گذاري مرکزي اوراق بهادار و تسويه وجوه ' | C129=3 |
D129=7975 | E129='۱۴۰۵/۱۲/۲۹ ' | F129=46702 | G129=3 | H129=7975 | I129=28117 | J129='مطابق روند سالهای قبل '
    MERGES A129:B129,J129:K129
  row 130 [MIXED_NUMERIC n=9 columns=A,C,D,E,F,G,H,I,J]: A130='بيمه سامان ' | C130=3 | D130=378958 | E130='۱۴۰۵/۱۲/۲۹ '
| F130=54792 | G130=9 | H130=1104951 | I130=21916 | J130='مطابق روند سالهای قبل '
    MERGES A130:B130,J130:K130
  row 131 [MIXED_NUMERIC n=9 columns=A,C,D,E,F,G,H,I,J]: A131='ساير شرکت هاي پذيرفته شده در بورس ' | C131=0 | D131=4956
| E131='۱۴۰۵/۱۲/۲۹ ' | F131=0 | G131=0 | H131=4956 | I131=0 | J131='مطابق روند سالهای قبل '
    MERGES A131:B131,J131:K131

[BAND 15] rows=137:137 columns=A,B,C merges=—
  SIGNATURE=COMPOUND_CANDIDATE
  PRIOR prior_body=134; gap=SINGLE_TEXT,SINGLE_TEXT
  FOLLOWING next_body=139; gap=SINGLE_TEXT
  row 131 [MIXED_NUMERIC n=9 columns=A,C,D,E,F,G,H,I,J]: A131='ساير شرکت هاي پذيرفته شده در بورس ' | C131=0 | D131=4956
| E131='۱۴۰۵/۱۲/۲۹ ' | F131=0 | G131=0 | H131=4956 | I131=0 | J131='مطابق روند سالهای قبل '
    MERGES A131:B131,J131:K131
  row 132 [MIXED_NUMERIC n=9 columns=A,C,D,E,F,G,H,I,J]: A132='ساير شرکت هاي خارج از بورس ' | C132=0 | D132=25925948 | E
132='۱۴۰۵/۱۲/۲۹ ' | F132=283422 | G132=0 | H132=20483885 | I132=119192 | J132='مطابق روند سالهای قبل '
    MERGES A132:B132,J132:K132
  row 133 [MIXED_NUMERIC n=9 columns=A,C,D,E,F,G,H,I,J]: A133='تأمين سرمايه کاردان ' | C133=41 | D133=11069898 | E133='۱
۴۰۵/۰۹/۳۰ ' | F133=0 | G133=31 | H133=3186756 | I133=0 | J133='مطابق روند سالهای قبل '
    MERGES A133:B133,J133:K133
  row 134 [MIXED_NUMERIC n=9 columns=A,C,D,E,F,G,H,I,J]: A134='شيشه همدان ' | C134=0 | D134=0 | E134='۱۴۰۵/۰۳/۳۱ ' | F13
4=0 | G134=0 | H134=0 | I134=0 | J134='مطابق روند سالهای قبل '
    MERGES A134:B134,J134:K134
  row 135 [SINGLE_TEXT n=1 columns=A]: A135='ساير درآمدها و هزینه های عملياتي:'
  row 136 [SINGLE_TEXT n=1 columns=A]: A136='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 137 [MULTI_TEXT n=3 columns=A,B,C]: A137='شرح' | B137='۱۴۰۵/۰۶/۳۱' | C137='۱۴۰۴/۰۶/۳۱'
  row 138 [SINGLE_TEXT n=1 columns=A]: A138='سایر درآمدهای عملیاتی: '
  row 139 [MIXED_NUMERIC n=3 columns=A,B,C]: A139='ساير درآمد ها ' | B139=61120834 | C139=0
  row 140 [EMPTY]
  row 141 [MIXED_NUMERIC n=3 columns=A,B,C]: A141='جمع سایر درآمدهای عملیاتی ' | B141=61120834 | C141=0
  row 142 [SINGLE_TEXT n=1 columns=A]: A142='سایر هزینه های عملیاتی: '
  row 143 [MIXED_NUMERIC n=3 columns=A,B,C]: A143='ساير هزينه ها ' | B143=-2464025 | C143=-1857935

[BAND 16] rows=148:148 columns=A,C merges=A148:B148
  SIGNATURE=NO_MATCH
  PRIOR prior_body=146; gap=SINGLE_TEXT
  FOLLOWING next_body=153; gap=EMPTY,SINGLE_TEXT,SINGLE_TEXT,MULTI_TEXT
  row 142 [SINGLE_TEXT n=1 columns=A]: A142='سایر هزینه های عملیاتی: '
  row 143 [MIXED_NUMERIC n=3 columns=A,B,C]: A143='ساير هزينه ها ' | B143=-2464025 | C143=-1857935
  row 144 [EMPTY]
  row 145 [MIXED_NUMERIC n=3 columns=A,B,C]: A145='جمع سایر هزینه های عملیاتی ' | B145=-2464025 | C145=-1857935
  row 146 [MIXED_NUMERIC n=3 columns=A,B,C]: A146='جمع سایر درآمدها و هزینه های عملیاتی ' | B146=58656809 | C146=-185793
5
  row 147 [SINGLE_TEXT n=1 columns=A]: A147='برآورد شرکت از تغییرات خالص سایر درآمدها (هزینه ها)ی عملیاتی:'
  row 148 [MULTI_TEXT n=2 columns=A,C]: A148='دوره ۶ ماهه منتهي به ۱۴۰۵/۱۲/۲۹ ' | C148='تغییرات این بخش متاثر از تغییرنر
خ تسعیر ارز توسط بانک مرکزی ج.ا.ا می...
    MERGES A148:B148
  row 149 [EMPTY]
  row 150 [SINGLE_TEXT n=1 columns=A]: A150='خالص ساير درآمدها و هزینه ها:'
  row 151 [SINGLE_TEXT n=1 columns=A]: A151='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 152 [MULTI_TEXT n=3 columns=A,B,C]: A152='خالص سایر درآمدها و هزینه ها' | B152='۱۴۰۵/۰۶/۳۱' | C152='۱۴۰۴/۰۶/۳۱'
  row 153 [MIXED_NUMERIC n=3 columns=A,B,C]: A153='ساير درآمد ها ' | B153=19745098 | C153=23761039
  row 154 [EMPTY]

[BAND 17] rows=152:152 columns=A,B,C merges=—
  SIGNATURE=NO_MATCH
  PRIOR prior_body=146; gap=SINGLE_TEXT,MULTI_TEXT,EMPTY,SINGLE_TEXT,SINGLE_TEXT
  FOLLOWING next_body=153; gap=none
  row 146 [MIXED_NUMERIC n=3 columns=A,B,C]: A146='جمع سایر درآمدها و هزینه های عملیاتی ' | B146=58656809 | C146=-185793
5
  row 147 [SINGLE_TEXT n=1 columns=A]: A147='برآورد شرکت از تغییرات خالص سایر درآمدها (هزینه ها)ی عملیاتی:'
  row 148 [MULTI_TEXT n=2 columns=A,C]: A148='دوره ۶ ماهه منتهي به ۱۴۰۵/۱۲/۲۹ ' | C148='تغییرات این بخش متاثر از تغییرنر
خ تسعیر ارز توسط بانک مرکزی ج.ا.ا می...
    MERGES A148:B148
  row 149 [EMPTY]
  row 150 [SINGLE_TEXT n=1 columns=A]: A150='خالص ساير درآمدها و هزینه ها:'
  row 151 [SINGLE_TEXT n=1 columns=A]: A151='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 152 [MULTI_TEXT n=3 columns=A,B,C]: A152='خالص سایر درآمدها و هزینه ها' | B152='۱۴۰۵/۰۶/۳۱' | C152='۱۴۰۴/۰۶/۳۱'
  row 153 [MIXED_NUMERIC n=3 columns=A,B,C]: A153='ساير درآمد ها ' | B153=19745098 | C153=23761039
  row 154 [EMPTY]
  row 155 [MIXED_NUMERIC n=3 columns=A,B,C]: A155='جمع خالص سایر درآمدها و هزینه ها ' | B155=19745098 | C155=23761039
  row 156 [SINGLE_TEXT n=1 columns=A]: A156='برآورد شرکت از تغییرات خالص ساير درآمدها و هزینه ها :'
  row 157 [MULTI_TEXT n=2 columns=A,C]: A157='دوره ۶ ماهه منتهي به ۱۴۰۵/۱۲/۲۹ ' | C157='پیش بینی میشود روند دوره های قبل
 ادامه داشته باشد. '
    MERGES A157:B157
  row 158 [EMPTY]

[BAND 18] rows=157:157 columns=A,C merges=A157:B157
  SIGNATURE=NO_MATCH
  PRIOR prior_body=155; gap=SINGLE_TEXT
  FOLLOWING next_body=162; gap=EMPTY,SINGLE_TEXT,SINGLE_TEXT,MULTI_TEXT
  row 151 [SINGLE_TEXT n=1 columns=A]: A151='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 152 [MULTI_TEXT n=3 columns=A,B,C]: A152='خالص سایر درآمدها و هزینه ها' | B152='۱۴۰۵/۰۶/۳۱' | C152='۱۴۰۴/۰۶/۳۱'
  row 153 [MIXED_NUMERIC n=3 columns=A,B,C]: A153='ساير درآمد ها ' | B153=19745098 | C153=23761039
  row 154 [EMPTY]
  row 155 [MIXED_NUMERIC n=3 columns=A,B,C]: A155='جمع خالص سایر درآمدها و هزینه ها ' | B155=19745098 | C155=23761039
  row 156 [SINGLE_TEXT n=1 columns=A]: A156='برآورد شرکت از تغییرات خالص ساير درآمدها و هزینه ها :'
  row 157 [MULTI_TEXT n=2 columns=A,C]: A157='دوره ۶ ماهه منتهي به ۱۴۰۵/۱۲/۲۹ ' | C157='پیش بینی میشود روند دوره های قبل
 ادامه داشته باشد. '
    MERGES A157:B157
  row 158 [EMPTY]
  row 159 [SINGLE_TEXT n=1 columns=A]: A159='هزینه های اداری و عمومی:'
  row 160 [SINGLE_TEXT n=1 columns=A]: A160='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 161 [MULTI_TEXT n=3 columns=A,B,C]: A161='هزینه های اداری و عمومی' | B161='۱۴۰۵/۰۶/۳۱' | C161='۱۴۰۴/۰۶/۳۱'
  row 162 [MIXED_NUMERIC n=3 columns=A,B,C]: A162='هزينه هاي کارکنان ' | B162=-37878233 | C162=-30787973
  row 163 [MIXED_NUMERIC n=3 columns=A,B,C]: A163='هزينه هاي اداري ' | B163=-57657167 | C163=-20978933

[BAND 19] rows=161:161 columns=A,B,C merges=—
  SIGNATURE=NO_MATCH
  PRIOR prior_body=155; gap=SINGLE_TEXT,MULTI_TEXT,EMPTY,SINGLE_TEXT,SINGLE_TEXT
  FOLLOWING next_body=162; gap=none
  row 155 [MIXED_NUMERIC n=3 columns=A,B,C]: A155='جمع خالص سایر درآمدها و هزینه ها ' | B155=19745098 | C155=23761039
  row 156 [SINGLE_TEXT n=1 columns=A]: A156='برآورد شرکت از تغییرات خالص ساير درآمدها و هزینه ها :'
  row 157 [MULTI_TEXT n=2 columns=A,C]: A157='دوره ۶ ماهه منتهي به ۱۴۰۵/۱۲/۲۹ ' | C157='پیش بینی میشود روند دوره های قبل
 ادامه داشته باشد. '
    MERGES A157:B157
  row 158 [EMPTY]
  row 159 [SINGLE_TEXT n=1 columns=A]: A159='هزینه های اداری و عمومی:'
  row 160 [SINGLE_TEXT n=1 columns=A]: A160='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 161 [MULTI_TEXT n=3 columns=A,B,C]: A161='هزینه های اداری و عمومی' | B161='۱۴۰۵/۰۶/۳۱' | C161='۱۴۰۴/۰۶/۳۱'
  row 162 [MIXED_NUMERIC n=3 columns=A,B,C]: A162='هزينه هاي کارکنان ' | B162=-37878233 | C162=-30787973
  row 163 [MIXED_NUMERIC n=3 columns=A,B,C]: A163='هزينه هاي اداري ' | B163=-57657167 | C163=-20978933
  row 164 [MIXED_NUMERIC n=3 columns=A,B,C]: A164='هزينه استهلاک ' | B164=-3917010 | C164=-2621961
  row 165 [EMPTY]
  row 166 [MIXED_NUMERIC n=3 columns=A,B,C]: A166='جمع هزینه های اداری و عمومی ' | B166=-99452410 | C166=-54388867
  row 167 [SINGLE_TEXT n=1 columns=A]: A167='برآورد شرکت از تغییرات هزینه های اداری و عمومی :'

[BAND 20] rows=168:168 columns=A,C merges=A168:B168
  SIGNATURE=NO_MATCH
  PRIOR prior_body=166; gap=SINGLE_TEXT
  FOLLOWING next_body=173; gap=EMPTY,SINGLE_TEXT,SINGLE_TEXT,MULTI_TEXT
  row 162 [MIXED_NUMERIC n=3 columns=A,B,C]: A162='هزينه هاي کارکنان ' | B162=-37878233 | C162=-30787973
  row 163 [MIXED_NUMERIC n=3 columns=A,B,C]: A163='هزينه هاي اداري ' | B163=-57657167 | C163=-20978933
  row 164 [MIXED_NUMERIC n=3 columns=A,B,C]: A164='هزينه استهلاک ' | B164=-3917010 | C164=-2621961
  row 165 [EMPTY]
  row 166 [MIXED_NUMERIC n=3 columns=A,B,C]: A166='جمع هزینه های اداری و عمومی ' | B166=-99452410 | C166=-54388867
  row 167 [SINGLE_TEXT n=1 columns=A]: A167='برآورد شرکت از تغییرات هزینه های اداری و عمومی :'
  row 168 [MULTI_TEXT n=2 columns=A,C]: A168='دوره ۶ ماهه منتهي به ۱۴۰۵/۱۲/۲۹ ' | C168='هزینه های اداری وعمومی شامل هزین
ه های کارکنان وسایرهزینه های اداری و...
    MERGES A168:B168
  row 169 [EMPTY]
  row 170 [SINGLE_TEXT n=1 columns=A]: A170='هزینه مالی:'
  row 171 [SINGLE_TEXT n=1 columns=A]: A171='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 172 [MULTI_TEXT n=3 columns=A,B,C]: A172='هزینه\u200cهای مالی' | B172='۱۴۰۵/۰۶/۳۱' | C172='۱۴۰۴/۰۶/۳۱'
  row 173 [MIXED_NUMERIC n=3 columns=A,B,C]: A173='هزینه مالی تسهیلات دریافتی از سایر بانکها و موسسات اعتباری ' | B173=0
 | C173=0
  row 174 [MIXED_NUMERIC n=3 columns=A,B,C]: A174='جریمه اضافه برداشت از بانک مرکزی ' | B174=0 | C174=0

[BAND 21] rows=172:172 columns=A,B,C merges=—
  SIGNATURE=NO_MATCH
  PRIOR prior_body=166; gap=SINGLE_TEXT,MULTI_TEXT,EMPTY,SINGLE_TEXT,SINGLE_TEXT
  FOLLOWING next_body=173; gap=none
  row 166 [MIXED_NUMERIC n=3 columns=A,B,C]: A166='جمع هزینه های اداری و عمومی ' | B166=-99452410 | C166=-54388867
  row 167 [SINGLE_TEXT n=1 columns=A]: A167='برآورد شرکت از تغییرات هزینه های اداری و عمومی :'
  row 168 [MULTI_TEXT n=2 columns=A,C]: A168='دوره ۶ ماهه منتهي به ۱۴۰۵/۱۲/۲۹ ' | C168='هزینه های اداری وعمومی شامل هزین
ه های کارکنان وسایرهزینه های اداری و...
    MERGES A168:B168
  row 169 [EMPTY]
  row 170 [SINGLE_TEXT n=1 columns=A]: A170='هزینه مالی:'
  row 171 [SINGLE_TEXT n=1 columns=A]: A171='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 172 [MULTI_TEXT n=3 columns=A,B,C]: A172='هزینه\u200cهای مالی' | B172='۱۴۰۵/۰۶/۳۱' | C172='۱۴۰۴/۰۶/۳۱'
  row 173 [MIXED_NUMERIC n=3 columns=A,B,C]: A173='هزینه مالی تسهیلات دریافتی از سایر بانکها و موسسات اعتباری ' | B173=0
 | C173=0
  row 174 [MIXED_NUMERIC n=3 columns=A,B,C]: A174='جریمه اضافه برداشت از بانک مرکزی ' | B174=0 | C174=0
  row 175 [MIXED_NUMERIC n=3 columns=A,B,C]: A175='سایر هزینه های مالی ' | B175=-3000000 | C175=-2000000
  row 176 [MIXED_NUMERIC n=3 columns=A,B,C]: A176='جمع هزینه\u200cهای مالی ' | B176=-3000000 | C176=-2000000
  row 177 [SINGLE_TEXT n=1 columns=A]: A177='برآورد شرکت از تغییرات هزینه های مالی :'
  row 178 [MULTI_TEXT n=2 columns=A,C]: A178='دوره ۶ ماهه منتهي به ۱۴۰۵/۱۲/۲۹ ' | C178='پیش بینی میشود این رقم حدود ۱.۰۰
۰.۰۰۰ میلیون ریال افزایش یابد '
    MERGES A178:B178

[BAND 22] rows=178:178 columns=A,C merges=A178:B178
  SIGNATURE=NO_MATCH
  PRIOR prior_body=176; gap=SINGLE_TEXT
  FOLLOWING next_body=182; gap=EMPTY,SINGLE_TEXT,MULTI_TEXT
  row 172 [MULTI_TEXT n=3 columns=A,B,C]: A172='هزینه\u200cهای مالی' | B172='۱۴۰۵/۰۶/۳۱' | C172='۱۴۰۴/۰۶/۳۱'
  row 173 [MIXED_NUMERIC n=3 columns=A,B,C]: A173='هزینه مالی تسهیلات دریافتی از سایر بانکها و موسسات اعتباری ' | B173=0
 | C173=0
  row 174 [MIXED_NUMERIC n=3 columns=A,B,C]: A174='جریمه اضافه برداشت از بانک مرکزی ' | B174=0 | C174=0
  row 175 [MIXED_NUMERIC n=3 columns=A,B,C]: A175='سایر هزینه های مالی ' | B175=-3000000 | C175=-2000000
  row 176 [MIXED_NUMERIC n=3 columns=A,B,C]: A176='جمع هزینه\u200cهای مالی ' | B176=-3000000 | C176=-2000000
  row 177 [SINGLE_TEXT n=1 columns=A]: A177='برآورد شرکت از تغییرات هزینه های مالی :'
  row 178 [MULTI_TEXT n=2 columns=A,C]: A178='دوره ۶ ماهه منتهي به ۱۴۰۵/۱۲/۲۹ ' | C178='پیش بینی میشود این رقم حدود ۱.۰۰
۰.۰۰۰ میلیون ریال افزایش یابد '
    MERGES A178:B178
  row 179 [EMPTY]
  row 180 [SINGLE_TEXT n=1 columns=A]: A180='برنامه شرکت در خصوص تقسیم سود'
  row 181 [MULTI_TEXT n=5 columns=A,B,C,D,E]: A181='مبلغ سود (زيان) انباشته پايان سال مالي گذشته' | B181='سود سهام پیشنه
ادی هیئت مدیره در سال مالی گذشته' | C181='مبلغ سود (زيان) خالص سال مالي گذشته' | D181='سود سهام مصوب مجمع سال مالی گذشته
' | E181='پیشنهاد هیئت مدیره درخصوص درصد تقسیم سود سال مالی جاری'
  row 182 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A182=150548777 | B182=18906793 | C182=177067928 | D182=-11000000 | E182
=0
  row 183 [SINGLE_TEXT n=1 columns=A]: A183='سایر برنامه های با اهمیت شرکت'
  row 184 [MULTI_TEXT n=2 columns=A,B]: A184='دوره ۶ ماهه منتهي به ۱۴۰۵/۱۲/۲۹ ' | B184='به شرح مندرج در گزارش تفسیری مدی
ریت پیوست '

[BAND 23] rows=181:181 columns=A,B,C,D,E merges=—
  SIGNATURE=NO_MATCH
  PRIOR prior_body=176; gap=SINGLE_TEXT,MULTI_TEXT,EMPTY,SINGLE_TEXT
  FOLLOWING next_body=182; gap=none
  row 175 [MIXED_NUMERIC n=3 columns=A,B,C]: A175='سایر هزینه های مالی ' | B175=-3000000 | C175=-2000000
  row 176 [MIXED_NUMERIC n=3 columns=A,B,C]: A176='جمع هزینه\u200cهای مالی ' | B176=-3000000 | C176=-2000000
  row 177 [SINGLE_TEXT n=1 columns=A]: A177='برآورد شرکت از تغییرات هزینه های مالی :'
  row 178 [MULTI_TEXT n=2 columns=A,C]: A178='دوره ۶ ماهه منتهي به ۱۴۰۵/۱۲/۲۹ ' | C178='پیش بینی میشود این رقم حدود ۱.۰۰
۰.۰۰۰ میلیون ریال افزایش یابد '
    MERGES A178:B178
  row 179 [EMPTY]
  row 180 [SINGLE_TEXT n=1 columns=A]: A180='برنامه شرکت در خصوص تقسیم سود'
  row 181 [MULTI_TEXT n=5 columns=A,B,C,D,E]: A181='مبلغ سود (زيان) انباشته پايان سال مالي گذشته' | B181='سود سهام پیشنه
ادی هیئت مدیره در سال مالی گذشته' | C181='مبلغ سود (زيان) خالص سال مالي گذشته' | D181='سود سهام مصوب مجمع سال مالی گذشته
' | E181='پیشنهاد هیئت مدیره درخصوص درصد تقسیم سود سال مالی جاری'
  row 182 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A182=150548777 | B182=18906793 | C182=177067928 | D182=-11000000 | E182
=0
  row 183 [SINGLE_TEXT n=1 columns=A]: A183='سایر برنامه های با اهمیت شرکت'
  row 184 [MULTI_TEXT n=2 columns=A,B]: A184='دوره ۶ ماهه منتهي به ۱۴۰۵/۱۲/۲۹ ' | B184='به شرح مندرج در گزارش تفسیری مدی
ریت پیوست '
  row 185 [EMPTY]
  row 186 [SINGLE_TEXT n=1 columns=A]: A186='سایر توضیحات با اهمیت'
  row 187 [SINGLE_TEXT n=1 columns=A]: A187='به شرح مندرج در گزارش تفسیری مدیریت پیوست '
    MERGES A187:K187

[BAND 24] rows=184:184 columns=A,B merges=—
  SIGNATURE=NO_MATCH
  PRIOR prior_body=182; gap=SINGLE_TEXT
  FOLLOWING next_body=None; gap=none
  row 178 [MULTI_TEXT n=2 columns=A,C]: A178='دوره ۶ ماهه منتهي به ۱۴۰۵/۱۲/۲۹ ' | C178='پیش بینی میشود این رقم حدود ۱.۰۰
۰.۰۰۰ میلیون ریال افزایش یابد '
    MERGES A178:B178
  row 179 [EMPTY]
  row 180 [SINGLE_TEXT n=1 columns=A]: A180='برنامه شرکت در خصوص تقسیم سود'
  row 181 [MULTI_TEXT n=5 columns=A,B,C,D,E]: A181='مبلغ سود (زيان) انباشته پايان سال مالي گذشته' | B181='سود سهام پیشنه
ادی هیئت مدیره در سال مالی گذشته' | C181='مبلغ سود (زيان) خالص سال مالي گذشته' | D181='سود سهام مصوب مجمع سال مالی گذشته
' | E181='پیشنهاد هیئت مدیره درخصوص درصد تقسیم سود سال مالی جاری'
  row 182 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A182=150548777 | B182=18906793 | C182=177067928 | D182=-11000000 | E182
=0
  row 183 [SINGLE_TEXT n=1 columns=A]: A183='سایر برنامه های با اهمیت شرکت'
  row 184 [MULTI_TEXT n=2 columns=A,B]: A184='دوره ۶ ماهه منتهي به ۱۴۰۵/۱۲/۲۹ ' | B184='به شرح مندرج در گزارش تفسیری مدی
ریت پیوست '
  row 185 [EMPTY]
  row 186 [SINGLE_TEXT n=1 columns=A]: A186='سایر توضیحات با اهمیت'
  row 187 [SINGLE_TEXT n=1 columns=A]: A187='به شرح مندرج در گزارش تفسیری مدیریت پیوست '
    MERGES A187:K187
  row 188 [SINGLE_TEXT n=1 columns=A]: A188='«جملات آینده\u200cنگر نشان\u200cدهنده انتظارات، باورها یا پیش\u200cب...
  row 189 [EMPTY]
  row 190 [EMPTY]

[BAND 25] rows=199:200 columns=A,B,C,D merges=A199:A200,D199:D200
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=202; gap=SINGLE_TEXT
  row 193 [EMPTY]
  row 194 [EMPTY]
  row 195 [EMPTY]
  row 196 [EMPTY]
  row 197 [SINGLE_TEXT n=1 columns=A]: A197='صورت سود و زیان'
  row 198 [SINGLE_TEXT n=1 columns=A]: A198='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 199 [MULTI_TEXT n=4 columns=A,B,C,D]: A199='شرح' | B199='دوره منتهی به ۱۴۰۵/۰۶/۳۱' | C199='تجدید ارائه شده ۱۴۰۴/۰۶
/۳۱' | D199='درصد تغییرات'
    MERGES A199:A200,D199:D200
  row 200 [MULTI_TEXT n=2 columns=B,C]: B200='حسابرسی نشده' | C200='حسابرسی شده'
    MERGES A199:A200,D199:D200
  row 201 [SINGLE_TEXT n=1 columns=A]: A201='عملیات در حال تداوم: '
  row 202 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A202='درآمد تسهيلات اعطايي ' | B202=432843600 | C202=242014199 | D202=79
  row 203 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A203='درآمد سپرده گذاری در بانک ها و موسسات اعتباری غیر بانکی ' | B203=45
119484 | C203=10944795 | D203=312
  row 204 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A204='درآمد سرمایه گذاری در اوراق بدهی ' | B204=31489756 | C204=12222406
| D204=158
  row 205 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A205='سود(زیان)سرمایه گذاری در سهام و سایر اوراق بهادار ' | B205=16405308
 | C205=2500083 | D205=556
  row 206 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A206='جایزه سپرده قانونی ' | B206=4663922 | C206=2207129 | D206=111

[BAND 26] rows=251:252 columns=A,B,C,D merges=A251:A252,D251:D252
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=253; gap=none
  row 245 [EMPTY]
  row 246 [EMPTY]
  row 247 [EMPTY]
  row 248 [EMPTY]
  row 249 [SINGLE_TEXT n=1 columns=A]: A249='صورت سود و زیان جامع'
  row 250 [SINGLE_TEXT n=1 columns=A]: A250='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 251 [MULTI_TEXT n=4 columns=A,B,C,D]: A251='شرح' | B251='دوره منتهی به۱۴۰۵/۰۶/۳۱' | C251='تجدید ارائه شده۱۴۰۴/۰۶/۳
۱' | D251='درصد تغییر'
    MERGES A251:A252,D251:D252
  row 252 [MULTI_TEXT n=2 columns=B,C]: B252='حسابرسی نشده' | C252='حسابرسی شده'
    MERGES A251:A252,D251:D252
  row 253 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A253='سود(زیان) خالص ' | B253=107051976 | C253=31248229 | D253=243
  row 254 [SINGLE_TEXT n=1 columns=A]: A254='سایر اقلام سود و زیان جامع: '
  row 255 [MIXED_NUMERIC n=3 columns=A,B,C]: A255='مازاد تجديد ارزيابي دارايي\u200cها ' | B255=0 | C255=0
  row 256 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A256='تفاوت تسعیر ارز عملیات خارجی ' | B256=5244549 | C256=1258917 | D256
=317
  row 257 [MIXED_NUMERIC n=3 columns=A,B,C]: A257='مالیات مربوط به سایر اقلام سود و زیان جامع ' | B257=0 | C257=0
  row 258 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A258='سایر اقلام سود و زیان جامع سال پس از کسر مالیات ' | B258=5244549 |
C258=1258917 | D258=317

[BAND 27] rows=270:272 columns=A,B,C,D,E merges=A270:A271,E270:E271
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=273; gap=none
  row 264 [EMPTY]
  row 265 [EMPTY]
  row 266 [EMPTY]
  row 267 [EMPTY]
  row 268 [SINGLE_TEXT n=1 columns=A]: A268='صورت وضعیت مالی'
  row 269 [SINGLE_TEXT n=1 columns=A]: A269='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 270 [MULTI_TEXT n=5 columns=A,B,C,D,E]: A270='شرح' | B270='دوره منتهی به ۱۴۰۵/۰۶/۳۱' | C270='تجدید ارائه شده۱۴۰۴/۱
۲/۲۹' | D270='تجدید ارائه شده۱۴۰۴/۰۱/۰۱' | E270='درصد تغییرات'
    MERGES A270:A271,E270:E271
  row 271 [MULTI_TEXT n=3 columns=B,C,D]: B271='حسابرسی نشده' | C271='حسابرسی شده' | D271='حسابرسی شده'
    MERGES A270:A271,E270:E271
  row 272 [MULTI_TEXT n=4 columns=A,B,C,D]: A272='دارایی ها ' | B272='ميليون ريال ' | C272='ميليون ريال ' | D272='میلیون
 ریال '
  row 273 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A273='موجودي نقد ' | B273=4564343655 | C273=4067657797 | D273=131630485
2 | E273=12
  row 274 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A274='مطالبات از بانک ها و موسسات اعتباري غیربانکی ' | B274=56294753 |
C274=28638646 | D274=26293517 | E274=97
  row 275 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A275='مطالبات از دولت ' | B275=0 | C275=0 | D275=0
  row 276 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A276='تسهيلات اعطايي و مطالبات از اشخاص دولتي ' | B276=0 | C276=0 | D276=
0
  row 277 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A277='تسهيلات اعطايي و مطالبات از اشخاص غير دولتي ' | B277=4527675101 |
 C277=3331529378 | D277=2115568239 | E277=36
  row 278 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A278='مطالبات از شرکت\u200cهای فرعی و وابسته ' | B278=792812091 | C278=
552419199 | D278=189045037 | E278=44

[BAND 28] rows=288:288 columns=A,B,C,D,E merges=—
  SIGNATURE=NO_MATCH
  PRIOR prior_body=287; gap=none
  FOLLOWING next_body=290; gap=SINGLE_TEXT
  row 282 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A282='دارایی\u200cهاي ثابت مشهود ' | B282=457082322 | C282=357305445 |
D282=100396960 | E282=28
  row 283 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A283='دارایی\u200cهاي نا مشهود ' | B283=45821855 | C283=45542496 | D283
=44748984 | E283=1
  row 284 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A284='سپرده قانونی ' | B284=1085923602 | C284=636258744 | D284=38661900
8 | E284=71
  row 285 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A285='دارایی مالیات انتقالی ' | B285=0 | C285=0 | D285=0
  row 286 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A286='ساير دارایی\u200cها ' | B286=105363367 | C286=76730269 | D286=397
03741 | E286=37
  row 287 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A287='جمع دارایی\u200cها ' | B287=12401580969 | C287=9661918925 | D287=
4719359640 | E287=28
  row 288 [MULTI_TEXT n=5 columns=A,B,C,D,E]: A288='بدهی\u200cها و حقوق مالکانه ' | B288='دوره منتهی به ۱۴۰۵/۰۶/۳۱ ' | C
288='تجدید ارائه شده۱۴۰۴/۱۲/۲۹ ' | D288='تجدید ارائه شده۱۴۰۴/۰۱/۰۱ ' | E288='درصد تغییرات '
  row 289 [SINGLE_TEXT n=1 columns=A]: A289='بدهی\u200cها '
  row 290 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A290='سپرده\u200cهاي مشتریان ' | B290=7948184039 | C290=6209237149 | D2
90=3173214293 | E290=28
  row 291 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A291='بدهي به بانكها و موسسات اعتباري غیر بانکی ' | B291=3701339828 | C
291=2874143188 | D291=1212198944 | E291=29
  row 292 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A292='سود سهام پرداختني ' | B292=1598637 | C292=704699 | D292=370455 |
E292=127
  row 293 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A293='اوراق بدهی و مشارکت ' | B293=0 | C293=0 | D293=0
  row 294 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A294='مالیات پرداختنی ' | B294=14498667 | C294=21355365 | D294=10000000
 | E294=-32

[BAND 29] rows=323:323 columns=A,B,C,D,E,F,G,H,I,J,K,L merges=—
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=324; gap=none
  row 317 [EMPTY]
  row 318 [EMPTY]
  row 319 [EMPTY]
  row 320 [EMPTY]
  row 321 [SINGLE_TEXT n=1 columns=A]: A321='صورت تغییرات در حقوق مالکانه'
  row 322 [SINGLE_TEXT n=1 columns=A]: A322='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 323 [MULTI_TEXT n=12 columns=A,B,C,D,E,F,G,H,I,J,K,L]: A323='شرح' | B323='سرمایه' | C323='افزایش سرمایه در جریان'
| D323='صرف سهام' | E323='صرف سهام خزانه' | F323='اندوخته قانونی' | G323='سایر اندوخته\u200cها' | H323='مازاد تجدید ارزی
ابی دارایی\u200cها' | I323='تفاوت تسعیر ارز عملیات خارجی' | J323='سود(زیان) انباشته' | K323='سهام خزانه' | L323='جمع کل'

  row 324 [MIXED_NUMERIC n=12 columns=A,B,C,D,E,F,G,H,I,J,K,L]: A324='مانده در۱۴۰۵/۰۱/۰۱ ' | B324=158000000 | C324=0 | D
324=0 | E324=206737 | F324=58395017 | G324=28218 | H324=10187858 | I324=23712301 | J324=162548777 | K324=-11152721 | L32
4=401926187
  row 325 [MIXED_NUMERIC n=3 columns=A,J,L]: A325='اصلاح اشتباهات ' | J325=-12000000 | L325=-12000000
  row 326 [MIXED_NUMERIC n=3 columns=A,J,L]: A326='تغییر در رویه\u200cهای حسابداری ' | J326=0 | L326=0
  row 327 [MIXED_NUMERIC n=12 columns=A,B,C,D,E,F,G,H,I,J,K,L]: A327='مانده تجدید ارائه شده در ۱۴۰۵/۰۱/۰۱ ' | B327=15800
0000 | C327=0 | D327=0 | E327=206737 | F327=58395017 | G327=28218 | H327=10187858 | I327=23712301 | J327=150548777 | K32
7=-11152721 | L327=389926187
  row 328 [MIXED_NUMERIC n=3 columns=A,J,L]: A328='سود (زیان)خالص \u200cسال ۱۴۰۵/۰۶/۳۱ ' | J328=107051976 | L328=1070519
76
  row 329 [SINGLE_TEXT n=1 columns=A]: A329='سایر اقلام سود و زیان جامع '

[BAND 30] rows=380:381 columns=A,B,C,D merges=A380:A381,D380:D381
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=383; gap=SINGLE_TEXT
  row 374 [EMPTY]
  row 375 [EMPTY]
  row 376 [EMPTY]
  row 377 [EMPTY]
  row 378 [SINGLE_TEXT n=1 columns=A]: A378='صورت جریان های نقدی'
  row 379 [SINGLE_TEXT n=1 columns=A]: A379='کلیه مبالغ به میلیون ریال است'
  row 380 [MULTI_TEXT n=4 columns=A,B,C,D]: A380='شرح' | B380='دوره منتهی به۱۴۰۵/۰۶/۳۱' | C380='تجدید ارائه شده۱۴۰۴/۰۶/۳
۱' | D380='درصد تغییر'
    MERGES A380:A381,D380:D381
  row 381 [MULTI_TEXT n=2 columns=B,C]: B381='حسابرسی نشده' | C381='حسابرسی شده'
    MERGES A380:A381,D380:D381
  row 382 [SINGLE_TEXT n=1 columns=A]: A382='جریان\xadهای نقدی حاصل از فعاليت\u200cهاي عملياتي: '
  row 383 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A383='نقد حاصل از عملیات ' | B383=310867468 | C383=21130489 | D383=1371
  row 384 [MIXED_NUMERIC n=3 columns=A,B,C]: A384='پرداخت\u200cهای نقدی بابت مالیات بر درآمد ' | B384=0 | C384=0
  row 385 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A385='جريان \u200cخالص \u200cورود\u200c (خروج) \u200cنقد حاصل از فعاليت\u
2... | B385=310867468 | C385=21130489 | D385=1371
  row 386 [SINGLE_TEXT n=1 columns=A]: A386='جریان های نقدی حاصل از فعالیت های سرمایه گذاری '
  row 387 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A387='پرداخت های نقدی برای تحصیل دارایی ثابت مشهود ' | B387=-104259778 |
C387=-3577275 | D387=-2815

[BAND 31] rows=441:466 columns=A,B,C,D,E,F,G,H,I,J,K,L,M merges=—
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=None; gap=none
  row 435 [EMPTY]
  row 436 [EMPTY]
  row 437 [SINGLE_TEXT n=1 columns=A]: A437='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 438 [EMPTY]
  row 439 [EMPTY]
  row 440 [EMPTY]
  row 441 [MULTI_TEXT n=13 columns=A,B,C,D,E,F,G,H,I,J,K,L,M]: A441='نماد شرکت' | B441='نام شرکت' | C441='نماد ثبت شده ن
زد سازمان' | D441='وضعیت ثبت شده نزد سازمان' | E441='نوع فعالیت' | F441='حسابرس' | G441='سال مالی' | H441='فعال/غیر فعال
' | I441='وضعیت' | J441='آخرین تاریخ مجمع تغییر سال مالی' | K441='تاریخ شمولیت' | L441='تاریخ خروج از شمولیت' | M441='تو
ضیحات'
  row 442 [MULTI_TEXT n=12 columns=A,B,C,D,E,F,G,H,I,J,K,L]: A442='سامان2' | B442='اعتبارسنجي حافظ سامان ايرانيان' | C44
2='*' | D442='ثبت نشده نزد سازمان' | E442='خدماتی' | F442='موسسه حسابرسي تدوين و همکاران' | G442='1405/09/30' | H442='فع
ال' | I442='دارای صورتهای مالی حسابرسی شده' | J442='*' | K442='1389/12/29' | L442='*'
  row 443 [MULTI_TEXT n=12 columns=A,B,C,D,E,F,G,H,I,J,K,L]: A443='سامان5' | B443='صرافي سامان' | C443='*' | D443='ثبت ن
شده نزد سازمان' | E443='خدماتی' | F443='موسسه حسابرسي بيات رايان' | G443='1405/09/30' | H443='فعال' | I443='دارای صورتها
ی مالی حسابرسی شده' | J443='*' | K443='1389/12/29' | L443='*'
  row 444 [MULTI_TEXT n=12 columns=A,B,C,D,E,F,G,H,I,J,K,L]: A444='سامان6' | B444='کارگزاري بانک سامان' | C444='*' | D44
4='ثبت نشده نزد سازمان' | E444='خدماتی' | F444='موسسه حسابرسي بيات رايان' | G444='1405/09/30' | H444='فعال' | I444='دارا
ی صورتهای مالی حسابرسی شده' | J444='*' | K444='1390/12/29' | L444='*'
  row 445 [MULTI_TEXT n=12 columns=A,B,C,D,E,F,G,H,I,J,K,L]: A445='سامان8' | B445='پردازشگران سامان' | C445='*' | D445='
ثبت نشده نزد سازمان' | E445='تولیدی' | F445='موسسه حسابرسي بيات رايان' | G445='1405/09/30' | H445='فعال' | I445='دارای ص
ورتهای مالی حسابرسی شده' | J445='*' | K445='1389/12/29' | L445='*'
  row 446 [MULTI_TEXT n=12 columns=A,B,C,D,E,F,G,H,I,J,K,L]: A446='سامان10' | B446='گسترش خدمات اتيه انديشان سپهر شرق' |
 C446='*' | D446='ثبت نشده نزد سازمان' | E446='تولیدی' | F446='موسسه حسابرسي تدوين و همکاران' | G446='1405/09/30' | H446
='فعال' | I446='دارای صورتهای مالی حسابرسی شده' | J446='*' | K446='1395/12/30' | L446='*'
  row 447 [MULTI_TEXT n=12 columns=A,B,C,D,E,F,G,H,I,J,K,L]: A447='سامان11' | B447='آتيه انديشان سپهر مهر' | C447='*' |
D447='ثبت نشده نزد سازمان' | E447='خدماتی' | F447='موسسه حسابرسي بيات رايان' | G447='1405/09/30' | H447='فعال' | I447='د
ارای صورتهای مالی حسابرسی شده' | J447='*' | K447='1394/12/29' | L447='*'
  row 448 [MULTI_TEXT n=12 columns=A,B,C,D,E,F,G,H,I,J,K,L]: A448='سامان12' | B448='کيش سل پارس' | C448='*' | D448='ثبت
نشده نزد سازمان' | E448='خدماتی' | F448='موسسه حسابرسي بيات رايان' | G448='1405/09/30' | H448='فعال' | I448='دارای صورته
ای مالی حسابرسی شده' | J448='1401/07/24' | K448='1398/12/29' | L448='*'
  row 449 [MULTI_TEXT n=12 columns=A,B,C,D,E,F,G,H,I,J,K,L]: A449='سامان13' | B449='راهکارهاي مالي هوشمند سامان' | C449=
'*' | D449='ثبت نشده نزد سازمان' | E449='تولیدی' | F449='موسسه حسابرسي بيات رايان' | G449='1405/09/30' | H449='فعال' | I
449='دارای صورتهای مالی حسابرسی شده' | J449='*' | K449='1398/12/29' | L449='*'
  row 450 [MULTI_TEXT n=12 columns=A,B,C,D,E,F,G,H,I,J,K,L]: A450='سامان14' | B450='گروه ارتباطات ماهواره اي سامان' | C4
50='اساما' | D450='ثبت نشده نزد سازمان' | E450='خدماتی' | F450='موسسه حسابرسي تدوين و همکاران' | G450='1405/09/30' | H45
0='فعال' | I450='دارای مجوز عدم انتشار از مراجع ذیربط' | J450='*' | K450='1389/12/29' | L450='*'
  row 451 [MULTI_TEXT n=12 columns=A,B,C,D,E,F,G,H,I,J,K,L]: A451='سامان20' | B451='توسعه و گسترش سرو سامان' | C451='*'
| D451='ثبت نشده نزد سازمان' | E451='خدماتی' | F451='موسسه حسابرسي بيات رايان' | G451='1405/09/30' | H451='فعال' | I451=
'دارای صورتهای مالی حسابرسی شده' | J451='*' | K451='1403/12/30' | L451='*'
  row 452 [MULTI_TEXT n=12 columns=A,B,C,D,E,F,G,H,I,J,K,L]: A452='سامان21' | B452='توسعه خدمات الکترونيکي آدونيس' | C45
2='*' | D452='ثبت نشده نزد سازمان' | E452='خدماتی' | F452='موسسه حسابرسي رازدار' | G452='1404/10/30' | H452='فعال' | I45
2='دارای صورتهای مالی حسابرسی شده' | J452='1395/02/05' | K452='1392/12/29' | L452='*'
  row 453 [MULTI_TEXT n=12 columns=A,B,C,D,E,F,G,H,I,J,K,L]: A453='سامان22' | B453='ابنيه نگهدار سامان' | C453='*' | D45
3='ثبت نشده نزد سازمان' | E453='خدماتی' | F453='موسسه حسابرسي بيات رايان' | G453='1405/09/30' | H453='فعال' | I453='دارا
ی صورتهای مالی حسابرسی شده' | J453='*' | K453='1404/01/01' | L453='*'
  row 454 [MULTI_TEXT n=12 columns=A,B,C,D,E,F,G,H,I,J,K,L]: A454='سامان23' | B454='مديريت اموال و ابنيه سامان' | C454='
*' | D454='ثبت نشده نزد سازمان' | E454='خدماتی' | F454='موسسه حسابرسي بيات رايان' | G454='1405/09/30' | H454='فعال' | I4
54='دارای صورتهای مالی حسابرسی شده' | J454='*' | K454='1404/01/25' | L454='*'
  row 455 [MULTI_TEXT n=12 columns=A,B,C,D,E,F,G,H,I,J,K,L]: A455='سامان24' | B455='سازه البرز تجارت هامون' | C455='*' |
 D455='ثبت نشده نزد سازمان' | E455='خدماتی' | F455='موسسه حسابرسي تدوين و همکاران' | G455='1405/09/30' | H455='فعال' | I
455='دارای صورتهای مالی حسابرسی شده' | J455='*' | K455='1404/04/21' | L455='*'
  row 456 [MULTI_TEXT n=12 columns=A,B,C,D,E,F,G,H,I,J,K,L]: A456='سامان26' | B456='هم راستا نوآوران سامان' | C456='*' |
 D456='ثبت نشده نزد سازمان' | E456='خدماتی' | F456='موسسه حسابرسي بيات رايان' | G456='1405/09/30' | H456='فعال' | I456='
دارای صورتهای مالی حسابرسی شده' | J456='1398/06/06' | K456='1404/08/10' | L456='*'
  row 457 [MULTI_TEXT n=12 columns=A,B,C,D,E,F,G,H,I,J,K,L]: A457='سامان27' | B457='سامان به افزار تامين زنجيره اي' | C4
57='*' | D457='ثبت نشده نزد سازمان' | E457='خدماتی' | F457='موسسه حسابرسي بيات رايان' | G457='1405/09/30' | H457='فعال'
| I457='دارای صورتهای مالی حسابرسی شده' | J457='1404/06/01' | K457='1404/09/30' | L457='*'
  row 458 [MULTI_TEXT n=12 columns=A,B,C,D,E,F,G,H,I,J,K,L]: A458='سامان28' | B458='خدمات ارزي و صرافي بانک سامان' | C45
8='*' | D458='ثبت نشده نزد سازمان' | E458='خدماتی' | F458='موسسه حسابرسي بيات رايان' | G458='1405/09/30' | H458='فعال' |
 I458='دارای صورتهای مالی حسابرسی شده' | J458='*' | K458='1404/12/29' | L458='*'
  row 459 [MULTI_TEXT n=12 columns=A,B,C,D,E,F,G,H,I,J,K,L]: A459='سامان29' | B459='آوا سامان انرژي' | C459='*' | D459='
ثبت نشده نزد سازمان' | E459='خدماتی' | F459='موسسه حسابرسي بيات رايان' | G459='1405/12/29' | H459='فعال' | I459='دارای ص
ورتهای مالی حسابرسی شده' | J459='*' | K459='1404/12/29' | L459='*'
  row 460 [MULTI_TEXT n=12 columns=A,B,C,D,E,F,G,H,I,J,K,L]: A460='سامان30' | B460='سيستم هاي مخابراتي بيس تاک' | C460='
*' | D460='ثبت نشده نزد سازمان' | E460='خدماتی' | F460='موسسه حسابرسي بيات رايان' | G460='1405/09/30' | H460='فعال' | I4
60='دارای صورتهای مالی حسابرسی شده' | J460='1405/02/01' | K460='1404/12/29' | L460='*'
  row 461 [MULTI_TEXT n=12 columns=A,B,C,D,E,F,G,H,I,J,K,L]: A461='سامان4' | B461='نرم افزاري تندر نور' | C461='*' | D46
1='ثبت نشده نزد سازمان' | E461='تولیدی' | F461='موسسه حسابرسي رايمند و همکاران' | G461='1405/09/30' | H461='غیر فعال' |
I461='دارای صورتهای مالی حسابرسی شده' | J461='*' | K461='1392/12/29' | L461='1397/12/29'
  row 462 [MULTI_TEXT n=12 columns=A,B,C,D,E,F,G,H,I,J,K,L]: A462='سامان9' | B462='گروه توسعه مالي و اقتصادي سامان' | C4
62='*' | D462='ثبت نشده نزد سازمان' | E462='خدماتی' | F462='موسسه حسابرسي آگاهان و همکاران' | G462='1404/09/30' | H462='
غیر فعال' | I462='دارای صورتهای مالی حسابرسی شده' | J462='*' | K462='1391/12/30' | L462='1404/09/30'
  row 463 [MULTI_TEXT n=12 columns=A,B,C,D,E,F,G,H,I,J,K,L]: A463='سامان15' | B463='پرداخت الکترونيک سامان کيش' | C463='
سپ' | D463='ثبت نشده نزد سازمان' | E463='خدماتی' | F463='موسسه حسابرسي بيات رايان' | G463='1405/09/30' | H463='غیر فعال'
 | I463='ناشر ثبت شده نزد سازمان' | J463='*' | K463='1399/12/30' | L463='*'
  row 464 [MULTI_TEXT n=12 columns=A,B,C,D,E,F,G,H,I,J,K,L]: A464='سامان16' | B464='توسعه فناوري تحليلگر اميد' | C464='*
' | D464='ثبت نشده نزد سازمان' | E464='خدماتی' | F464='موسسه حسابرسي بيات رايان' | G464='1403/12/30' | H464='غیر فعال' |
 I464='دارای صورتهای مالی حسابرسی شده' | J464='*' | K464='1399/12/30' | L464='1404/02/03'
  row 465 [MULTI_TEXT n=12 columns=A,B,C,D,E,F,G,H,I,J,K,L]: A465='سامان18' | B465='تجارت ورزان پيشگام سامان قشم' | C465
='*' | D465='ثبت نشده نزد سازمان' | E465='خدماتی' | F465='موسسه حسابرسي بيات رايان' | G465='1404/12/29' | H465='غیر فعال
' | I465='دارای صورتهای مالی حسابرسی شده' | J465='*' | K465='1401/12/29' | L465='1404/09/30'
  row 466 [MULTI_TEXT n=12 columns=A,B,C,D,E,F,G,H,I,J,K,L]: A466='سامان19' | B466='توسعه تجارت فاخر سامان' | C466='*' |
 D466='ثبت نشده نزد سازمان' | E466='خدماتی' | F466='موسسه حسابرسي آگاهان و همکاران' | G466='1404/12/29' | H466='غیر فعال
' | I466='دارای صورتهای مالی حسابرسی شده' | J466='*' | K466='1403/12/30' | L466='1404/09/30'
  row 467 [EMPTY]
  row 468 [EMPTY]
    MERGES A468:M468
  row 469 [SINGLE_TEXT n=1 columns=A]: A469='اطلاعات نمایش داده شده با اطلاعات امضا شده مطابقت دارد'
    MERGES A469:M469
  row 470 [EMPTY]
    MERGES A470:M470
  row 471 [EMPTY]
  row 472 [EMPTY]

[BAND 32] rows=483:485 columns=A,B,C,D,E,F,G,H,I,J,K,L,M merges=—
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=None; gap=none
  row 477 [EMPTY]
  row 478 [EMPTY]
  row 479 [SINGLE_TEXT n=1 columns=A]: A479='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 480 [EMPTY]
  row 481 [EMPTY]
  row 482 [EMPTY]
  row 483 [MULTI_TEXT n=13 columns=A,B,C,D,E,F,G,H,I,J,K,L,M]: A483='نماد شرکت' | B483='نام شرکت' | C483='نماد ثبت شده ن
زد سازمان' | D483='وضعیت ثبت شده نزد سازمان' | E483='نوع فعالیت' | F483='حسابرس' | G483='سال مالی' | H483='فعال/غیر فعال
' | I483='وضعیت' | J483='آخرین تاریخ مجمع تغییر سال مالی' | K483='تاریخ شمولیت' | L483='تاریخ خروج از شمولیت' | M483='تو
ضیحات'
  row 484 [MULTI_TEXT n=12 columns=A,B,C,D,E,F,G,H,I,J,K,L]: A484='سامان17' | B484='ميزبان گستر حافظ سامان' | C484='*' |
 D484='ثبت نشده نزد سازمان' | E484='خدماتی' | F484='موسسه حسابرسي بيات رايان' | G484='1405/12/29' | H484='فعال' | I484='
دارای صورتهای مالی حسابرسی شده' | J484='*' | K484='1401/12/29' | L484='*'
  row 485 [MULTI_TEXT n=12 columns=A,B,C,D,E,F,G,H,I,J,K,L]: A485='سامان25' | B485='تأمين سرمايه کاردان' | C485='تکاردان
' | D485='ثبت نشده نزد سازمان' | E485='تامین سرمایه' | F485='موسسه حسابرسي بيات رايان' | G485='1405/09/30' | H485='فعال'
 | I485='ناشر ثبت شده نزد سازمان' | J485='1403/09/19' | K485='1392/12/29' | L485='*'
  row 486 [EMPTY]
  row 487 [EMPTY]
    MERGES A487:M487
  row 488 [SINGLE_TEXT n=1 columns=A]: A488='اطلاعات نمایش داده شده با اطلاعات امضا شده مطابقت دارد'
    MERGES A488:M488
  row 489 [EMPTY]
    MERGES A489:M489
  row 490 [EMPTY]
  row 491 [EMPTY]

SUMMARY bands_printed=32 compound_candidates=3

## WORKBOOK excel\parsian_periodic.xlsx
Reader: ACCEPTED
SHA-256: b5623964d336dd679eaa8208fb800fdbf24351ff85bc996e05210b37f342e6da

### SHEET 1 Recovered_Sheet1 | used=A1:L411 | bands=29

[BAND 1] rows=10:11 columns=A,B,C,D,E merges=A10:A11,E10:E11
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=13; gap=SINGLE_TEXT
  row 4 [EMPTY]
  row 5 [EMPTY]
  row 6 [EMPTY]
  row 7 [EMPTY]
  row 8 [SINGLE_TEXT n=1 columns=A]: A8='صورت سود و زیان'
  row 9 [SINGLE_TEXT n=1 columns=A]: A9='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 10 [MULTI_TEXT n=5 columns=A,B,C,D,E]: A10='شرح' | B10='دوره منتهي به ۱۴۰۳/۰۶/۳۱' | C10='تجدید ارائه شده ۱۴۰۲/۰۶/۳
۱' | D10='تجدید ارائه شده ۱۴۰۲/۱۲/۲۹' | E10='درصد تغييرات'
    MERGES A10:A11,E10:E11
  row 11 [MULTI_TEXT n=3 columns=B,C,D]: B11='حسابرسی نشده' | C11='حسابرسی شده' | D11='حسابرسی شده'
    MERGES A10:A11,E10:E11
  row 12 [SINGLE_TEXT n=1 columns=A]: A12='عملیات در حال تداوم: '
  row 13 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A13='درآمد تسهيلات اعطايي و سپرده گذاری و اوراق بدهی ' | B13=147186330 |
 C13=87074365 | D13=229849193 | E13=69
  row 14 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A14='هزينه سود سپرده\u200cها ' | B14=-230307149 | C14=-157273597 | D14=-
345542486 | E14=-46
  row 15 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A15='خالص درآمد تسهیلات و سپرده گذاری ' | B15=-83120819 | C15=-70199232
| D15=-115693293 | E15=-18
  row 16 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A16='درآمد کارمزد ' | B16=24646669 | C16=17434558 | D16=43403722 | E16=4
1
  row 17 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A17='هزينه کارمزد ' | B17=-8624760 | C17=-4224997 | D17=-10854204 | E17=
-104

[BAND 2] rows=60:61 columns=A,B,C,D,E merges=A60:A61,E60:E61
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=62; gap=none
  row 54 [EMPTY]
  row 55 [EMPTY]
  row 56 [EMPTY]
  row 57 [EMPTY]
  row 58 [SINGLE_TEXT n=1 columns=A]: A58='صورت سود و زیان جامع'
  row 59 [SINGLE_TEXT n=1 columns=A]: A59='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 60 [MULTI_TEXT n=5 columns=A,B,C,D,E]: A60='شرح' | B60='دوره منتهي به ۱۴۰۳/۰۶/۳۱' | C60='تجدید ارائه شده ۱۴۰۲/۰۶/۳
۱' | D60='تجدید ارائه شده ۱۴۰۲/۱۲/۲۹' | E60='درصد تغییر'
    MERGES A60:A61,E60:E61
  row 61 [MULTI_TEXT n=3 columns=B,C,D]: B61='حسابرسی نشده' | C61='حسابرسی شده' | D61='حسابرسی شده'
    MERGES A60:A61,E60:E61
  row 62 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A62='سود(زیان) خالص ' | B62=-25195703 | C62=-35246257 | D62=-9124895 | E
62=29
  row 63 [SINGLE_TEXT n=1 columns=A]: A63='سایر اقلام سود و زیان جامع: '
  row 64 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A64='مازاد تجديد ارزيابي دارايي\u200cها ' | B64=0 | C64=0 | D64=0
  row 65 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A65='تفاوت تسعیر ارز عملیات خارجی ' | B65=0 | C65=0 | D65=0
  row 66 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A66='مالیات مربوط به سایر اقلام سود و زیان جامع ' | B66=0 | C66=0 | D66=0
  row 67 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A67='سایر اقلام سود و زیان جامع سال پس از کسر مالیات ' | B67=0 | C67=0 | D
67=0

[BAND 3] rows=79:80 columns=A,B,C,D,E merges=A79:A80,E79:E80
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=82; gap=SINGLE_TEXT
  row 73 [EMPTY]
  row 74 [EMPTY]
  row 75 [EMPTY]
  row 76 [EMPTY]
  row 77 [SINGLE_TEXT n=1 columns=A]: A77='صورت وضعیت مالی'
  row 78 [SINGLE_TEXT n=1 columns=A]: A78='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 79 [MULTI_TEXT n=5 columns=A,B,C,D,E]: A79='شرح' | B79='دوره منتهي به ۱۴۰۳/۰۶/۳۱' | C79='تجدید ارائه شده ۱۴۰۲/۱۲/۲
۹' | D79='تجدید ارائه شده ۱۴۰۲/۰۱/۰۱' | E79='درصد تغييرات'
    MERGES A79:A80,E79:E80
  row 80 [MULTI_TEXT n=3 columns=B,C,D]: B80='حسابرسی نشده' | C80='حسابرسی شده' | D80='حسابرسی نشده'
    MERGES A79:A80,E79:E80
  row 81 [SINGLE_TEXT n=1 columns=A]: A81='دارایی ها '
  row 82 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A82='موجودي نقد ' | B82=347110539 | C82=295173082 | D82=229326967 | E82=
18
  row 83 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A83='مطالبات از بانک ها و ساير موسسات اعتباري ' | B83=686275365 | C83=69
6743016 | D83=445765962 | E83=-2
  row 84 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A84='مطالبات از دولت ' | B84=2920800 | C84=2925324 | D84=3017721 | E84=0

  row 85 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A85='تسهيلات اعطايي و مطالبات از اشخاص دولتي ' | B85=5517538 | C85=50248
06 | D85=21974278 | E85=10
  row 86 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A86='تسهيلات اعطايي و مطالبات از اشخاص غير دولتي ' | B86=2826181422 | C8
6=2662958772 | D86=2127527442 | E86=6

[BAND 4] rows=95:95 columns=A,B,C,D,E merges=—
  SIGNATURE=NO_MATCH
  PRIOR prior_body=94; gap=none
  FOLLOWING next_body=97; gap=SINGLE_TEXT
  row 89 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A89='ساير حسابهاي دريافتني ' | B89=462006254 | C89=432339509 | D89=30884
5970 | E89=7
  row 90 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A90='دارایی\u200cهاي ثابت مشهود ' | B90=23049146 | C90=22273873 | D90=15
760214 | E90=3
  row 91 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A91='دارایی\u200cهاي نا مشهود ' | B91=23180530 | C91=23237672 | D91=2249
1788 | E91=0
  row 92 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A92='سپرده قانونی ' | B92=291130716 | C92=275811706 | D92=212206595 | E9
2=6
  row 93 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A93='ساير دارایی\u200cها ' | B93=101636499 | C93=72855571 | D93=64703437
 | E93=40
  row 94 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A94='جمع دارایی\u200cها ' | B94=5139354983 | C94=4848153182 | D94=374409
1280 | E94=6
  row 95 [MULTI_TEXT n=5 columns=A,B,C,D,E]: A95='حقوق مالکانه و بدهی\u200cها ' | B95='دوره منتهی به ۱۴۰۳/۰۶/۳۱ ' | C95=
'تجدید ارائه شده ۱۴۰۲/۱۲/۲۹ ' | D95='تجدید ارائه شده۱۴۰۲/۰۱/۰۱ ' | E95='درصد تغييرات '
  row 96 [SINGLE_TEXT n=1 columns=A]: A96='حقوق مالکانه '
  row 97 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A97='سرمايه ' | B97=156340000 | C97=156340000 | D97=156340000 | E97=0
  row 98 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A98='افزايش سرمايه در جريان ' | B98=0 | C98=0 | D98=0
  row 99 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A99='صرف سهام ' | B99=0 | C99=0 | D99=0
  row 100 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A100='اندوخته صرف سهام ' | B100=0 | C100=0 | D100=0
  row 101 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A101='اندوخته قانوني ' | B101=7393601 | C101=7393601 | D101=7393601 | E
101=0

[BAND 5] rows=130:130 columns=A,B,C,D,E,F,G,H,I,J,K,L merges=—
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=131; gap=none
  row 124 [EMPTY]
  row 125 [EMPTY]
  row 126 [EMPTY]
  row 127 [EMPTY]
  row 128 [SINGLE_TEXT n=1 columns=A]: A128='صورت تغییرات در حقوق مالکانه'
  row 129 [SINGLE_TEXT n=1 columns=A]: A129='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 130 [MULTI_TEXT n=12 columns=A,B,C,D,E,F,G,H,I,J,K,L]: A130='شرح' | B130='سرمایه' | C130='افزایش سرمایه در جریان'
| D130='صرف سهام' | E130='صرف سهام خزانه' | F130='اندوخته قانونی' | G130='سایر اندوخته\u200cها' | H130='مازاد تجدید ارزی
ابی دارایی\u200cها' | I130='تفاوت تسعیر ارز عملیات خارجی' | J130='سود انباشته' | K130='سهام خزانه' | L130='جمع کل'
  row 131 [MIXED_NUMERIC n=12 columns=A,B,C,D,E,F,G,H,I,J,K,L]: A131='مانده در ۱۴۰۲/۰۱/۰۱ ' | B131=156340000 | C131=0 |
D131=0 | E131=0 | F131=7393601 | G131=985814 | H131=0 | I131=0 | J131=-20295950 | K131=-23976787 | L131=120446678
  row 132 [MIXED_NUMERIC n=12 columns=A,B,C,D,E,F,G,H,I,J,K,L]: A132='اصلاح اشتباهات ' | B132=0 | C132=0 | D132=0 | E132
=0 | F132=0 | G132=0 | H132=0 | I132=0 | J132=-15789842 | K132=0 | L132=-15789842
  row 133 [MIXED_NUMERIC n=12 columns=A,B,C,D,E,F,G,H,I,J,K,L]: A133='تغییر در رویه\u200cهای حسابداری ' | B133=0 | C133=
0 | D133=0 | E133=0 | F133=0 | G133=0 | H133=0 | I133=0 | J133=0 | K133=0 | L133=0
  row 134 [MIXED_NUMERIC n=12 columns=A,B,C,D,E,F,G,H,I,J,K,L]: A134='مانده تجدید ارائه شده در ۱۴۰۲/۰۱/۰۱ ' | B134=15634
0000 | C134=0 | D134=0 | E134=0 | F134=7393601 | G134=985814 | H134=0 | I134=0 | J134=-36085792 | K134=-23976787 | L134=
104656836
  row 135 [SINGLE_TEXT n=1 columns=A]: A135='تغییرات حقوق مالکانه در سال ۱۴۰۲/۱۲/۲۹ '
  row 136 [MIXED_NUMERIC n=3 columns=A,J,L]: A136='سود(زيان) خالص گزارش شده در صورت\u200cهاي مالي سال ۱۴۰۲/۱۲/۲۹ ' | J13
6=-9124895 | L136=-9124895

[BAND 6] rows=176:177 columns=A,B,C,D,E merges=A176:A177,E176:E177
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=179; gap=SINGLE_TEXT
  row 170 [EMPTY]
  row 171 [EMPTY]
  row 172 [EMPTY]
  row 173 [EMPTY]
  row 174 [SINGLE_TEXT n=1 columns=A]: A174='صورت جریان های نقدی'
  row 175 [SINGLE_TEXT n=1 columns=A]: A175='کلیه مبالغ به میلیون ریال است'
  row 176 [MULTI_TEXT n=5 columns=A,B,C,D,E]: A176='شرح' | B176='دوره منتهي به ۱۴۰۳/۰۶/۳۱' | C176='تجدید ارائه شده۱۴۰۲/۰
۶/۳۱' | D176='تجدید ارائه شده۱۴۰۲/۱۲/۲۹' | E176='درصد تغییر'
    MERGES A176:A177,E176:E177
  row 177 [MULTI_TEXT n=3 columns=B,C,D]: B177='حسابرسی نشده' | C177='حسابرسی شده' | D177='حسابرسی شده'
    MERGES A176:A177,E176:E177
  row 178 [SINGLE_TEXT n=1 columns=A]: A178='جریان\xadهای نقدی حاصل از فعاليت\u200cهاي عملياتي: '
  row 179 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A179='نقد حاصل از عملیات ' | B179=-29363629 | C179=-110187888 | D179=-9
6174356 | E179=73
  row 180 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A180='پرداخت\u200cهای نقدی بابت مالیات بر درآمد ' | B180=-2548000 | C18
0=0 | D180=0 | E180='-Infinity '
  row 181 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A181='جريان \u200cخالص \u200cورود\u200c (خروج) \u200cنقد حاصل از فعاليت
\u2... | B181=-31911629 | C181=-110187888 | D181=-96174356 | E181=71
  row 182 [SINGLE_TEXT n=1 columns=A]: A182='فعاليت\u200cهاي سرمایه\u200cگذاری '
  row 183 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A183='وجوه پرداختي بابت تحصیل دارایی\u200cهاي ثابت مشهود ' | B183=-1379
698 | C183=-5726382 | D183=-7657549 | E183=76

[BAND 7] rows=238:239 columns=A,B,C,D,E,F,G,H,I,J,K merges=A238:A239,B239:C239,D239:E239,F239:G239,H239:I239,J239:K239
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=240; gap=none
  row 232 [EMPTY]
  row 233 [EMPTY]
  row 234 [EMPTY]
  row 235 [SINGLE_TEXT n=1 columns=A]: A235='اطلاعات این فرم گزیده ای از اطلاعات گزارش تفسیری مدیریت می باشد که ه...
    MERGES A235:K235
  row 236 [SINGLE_TEXT n=1 columns=A]: A236='مانده تسهیلات اعطایی و ذخیره مطالبات مشکوک الوصول:'
  row 237 [SINGLE_TEXT n=1 columns=A]: A237='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 238 [MULTI_TEXT n=11 columns=A,B,C,D,E,F,G,H,I,J,K]: A238='شرح' | B238='در تاریخ ۱۴۰۲/۱۲/۲۹' | C238='در تاریخ ۱۴۰۳
/۰۶/۳۱' | D238='در تاریخ ۱۴۰۲/۱۲/۲۹' | E238='در تاریخ ۱۴۰۳/۰۶/۳۱' | F238='در تاریخ ۱۴۰۲/۱۲/۲۹' | G238='در تاریخ ۱۴۰۳/۰۶/
۳۱' | H238='در تاریخ ۱۴۰۲/۱۲/۲۹' | I238='در تاریخ ۱۴۰۳/۰۶/۳۱' | J238='در تاریخ ۱۴۰۲/۱۲/۲۹' | K238='در تاریخ ۱۴۰۳/۰۶/۳۱'
    MERGES A238:A239
  row 239 [MULTI_TEXT n=5 columns=B,D,F,H,J]: B239='جاری' | D239='سررسید گذشته' | F239='معوق' | H239='مشکوک الوصول' | J2
39='جمع'
    MERGES A238:A239,B239:C239,D239:E239,F239:G239,H239:I239,J239:K239
  row 240 [MIXED_NUMERIC n=11 columns=A,B,C,D,E,F,G,H,I,J,K]: A240='تسهیلات اعطایی و مطالبات از اشخاص دولتی ' | B240=943
937 | C240=0 | D240=4080869 | E240=5601562 | F240=0 | G240=0 | H240=0 | I240=0 | J240=5024806 | K240=5601562
  row 241 [MIXED_NUMERIC n=11 columns=A,B,C,D,E,F,G,H,I,J,K]: A241='تسهیلات اعطایی و مطالبات از اشخاص غیر دولتی- ریالی '
 | B241=870619839 | C241=898771183 | D241=316695405 | E241=280319073 | F241=5109498 | G241=16190626 | H241=198375341 | I
241=241404928 | J241=1390800083 | K241=1436685810
  row 242 [MIXED_NUMERIC n=11 columns=A,B,C,D,E,F,G,H,I,J,K]: A242='تسهیلات اعطایی و مطالبات از اشخاص غیر دولتی- ارزی '
| B242=1447241031 | C242=1469776118 | D242=33487649 | E242=38793986 | F242=48988 | G242=46096435 | H242=123135192 | I242
=147254352 | J242=1603912860 | K242=1701920891
  row 243 [MIXED_NUMERIC n=11 columns=A,B,C,D,E,F,G,H,I,J,K]: A243='جمع ' | B243=2318804807 | C243=2368547301 | D243=354
263923 | E243=324714621 | F243=5158486 | G243=62287061 | H243=321510533 | I243=388659280 | J243=2999737749 | K243=314420
8263
  row 244 [SINGLE_TEXT n=1 columns=A]: A244='کسر می شود: '
  row 245 [MIXED_NUMERIC n=11 columns=A,B,C,D,E,F,G,H,I,J,K]: A245='سود سالهای آتی ' | B245=161368315 | C245=145007474 |
 D245=0 | E245=0 | F245=0 | G245=0 | H245=0 | I245=0 | J245=161368315 | K245=145007474

[BAND 8] rows=256:256 columns=A,C merges=A256:B256,C256:I256
  SIGNATURE=NO_MATCH
  PRIOR prior_body=254; gap=SINGLE_TEXT
  FOLLOWING next_body=None; gap=none
  row 250 [MIXED_NUMERIC n=7 columns=A,D,E,F,G,H,I]: A250='ضریب مبنای احتساب ذخیره اختصاصی (درصد) ' | D250=10 | E250=10
| F250=20 | G250=20 | H250=50 | I250=50
  row 251 [MIXED_NUMERIC n=9 columns=A,D,E,F,G,H,I,J,K]: A251='ذخیره اختصاصی مطالبات مشکوک الوصول ' | D251=3049291 | E25
1=14049291 | F251=539710 | G251=539710 | H251=114730469 | I251=114730469 | J251=118319470 | K251=129319470
  row 252 [MIXED_NUMERIC n=11 columns=A,B,C,D,E,F,G,H,I,J,K]: A252='مانده مبنای محاسبه ذخیره عمومی ' | B252=2157436491 |
 C252=2218722326 | D252=351214632 | E252=310665330 | F252=4618776 | G252=61747351 | H252=206780064 | I252=273928811 | J2
52=2720049963 | K252=2865063818
  row 253 [MIXED_NUMERIC n=11 columns=A,B,C,D,E,F,G,H,I,J,K]: A253='ذخیره عمومی مطالبات مشکوک الوصول ' | B253=32361761 |
 C253=46762403 | D253=62145 | E253=84023 | F253=0 | G253=0 | H253=0 | I253=0 | J253=32423906 | K253=46846426
  row 254 [MIXED_NUMERIC n=11 columns=A,B,C,D,E,F,G,H,I,J,K]: A254='جمع ' | B254=2125074730 | C254=2171959923 | D254=351
152487 | E254=310581307 | F254=4618776 | G254=61747351 | H254=206780064 | I254=273928811 | J254=2687626057 | K254=281821
7392
  row 255 [SINGLE_TEXT n=1 columns=A]: A255='برآورد شرکت از تغییرات در نرخ سود تسهیلات اعطایی :'
  row 256 [MULTI_TEXT n=2 columns=A,C]: A256='دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ' | C256='با توجه به سیاستهای پولی و بانکی
 انتظار در تغییر نرخ سود تسهیلات اعط...
    MERGES A256:B256,C256:I256
  row 257 [EMPTY]
  row 258 [SINGLE_TEXT n=1 columns=A]: A258='برآورد شرکت از تغییرات در مانده تسهیلات :'
  row 259 [MULTI_TEXT n=2 columns=A,C]: A259='دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ' | C259='با توجه به رشد منابع بانک در سال
 آتی پیش بینی می گردد مانده تسهیلات ...
    MERGES A259:B259,C259:I259
  row 260 [EMPTY]
  row 261 [SINGLE_TEXT n=1 columns=A]: A261='برآورد شرکت از تغییرات در مانده ذخایر مطالبات مشکوک الوصول :'
  row 262 [MULTI_TEXT n=2 columns=A,C]: A262='دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ' | C262='با توجه به افزایش در حجم تسهیلات
 اعطایی پیش بینی می گردد مانده ذخیره...
    MERGES A262:B262,C262:I262

[BAND 9] rows=259:259 columns=A,C merges=A259:B259,C259:I259
  SIGNATURE=NO_MATCH
  PRIOR prior_body=254; gap=SINGLE_TEXT,MULTI_TEXT,EMPTY,SINGLE_TEXT
  FOLLOWING next_body=None; gap=none
  row 253 [MIXED_NUMERIC n=11 columns=A,B,C,D,E,F,G,H,I,J,K]: A253='ذخیره عمومی مطالبات مشکوک الوصول ' | B253=32361761 |
 C253=46762403 | D253=62145 | E253=84023 | F253=0 | G253=0 | H253=0 | I253=0 | J253=32423906 | K253=46846426
  row 254 [MIXED_NUMERIC n=11 columns=A,B,C,D,E,F,G,H,I,J,K]: A254='جمع ' | B254=2125074730 | C254=2171959923 | D254=351
152487 | E254=310581307 | F254=4618776 | G254=61747351 | H254=206780064 | I254=273928811 | J254=2687626057 | K254=281821
7392
  row 255 [SINGLE_TEXT n=1 columns=A]: A255='برآورد شرکت از تغییرات در نرخ سود تسهیلات اعطایی :'
  row 256 [MULTI_TEXT n=2 columns=A,C]: A256='دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ' | C256='با توجه به سیاستهای پولی و بانکی
 انتظار در تغییر نرخ سود تسهیلات اعط...
    MERGES A256:B256,C256:I256
  row 257 [EMPTY]
  row 258 [SINGLE_TEXT n=1 columns=A]: A258='برآورد شرکت از تغییرات در مانده تسهیلات :'
  row 259 [MULTI_TEXT n=2 columns=A,C]: A259='دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ' | C259='با توجه به رشد منابع بانک در سال
 آتی پیش بینی می گردد مانده تسهیلات ...
    MERGES A259:B259,C259:I259
  row 260 [EMPTY]
  row 261 [SINGLE_TEXT n=1 columns=A]: A261='برآورد شرکت از تغییرات در مانده ذخایر مطالبات مشکوک الوصول :'
  row 262 [MULTI_TEXT n=2 columns=A,C]: A262='دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ' | C262='با توجه به افزایش در حجم تسهیلات
 اعطایی پیش بینی می گردد مانده ذخیره...
    MERGES A262:B262,C262:I262
  row 263 [EMPTY]
  row 264 [SINGLE_TEXT n=1 columns=A]: A264='مانده سپرده های دریافتی از مشتریان :'
  row 265 [SINGLE_TEXT n=1 columns=A]: A265='کلیه مبالغ درج شده به میلیون ریال می باشد'

[BAND 10] rows=262:262 columns=A,C merges=A262:B262,C262:I262
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=None; gap=none
  row 256 [MULTI_TEXT n=2 columns=A,C]: A256='دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ' | C256='با توجه به سیاستهای پولی و بانکی
 انتظار در تغییر نرخ سود تسهیلات اعط...
    MERGES A256:B256,C256:I256
  row 257 [EMPTY]
  row 258 [SINGLE_TEXT n=1 columns=A]: A258='برآورد شرکت از تغییرات در مانده تسهیلات :'
  row 259 [MULTI_TEXT n=2 columns=A,C]: A259='دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ' | C259='با توجه به رشد منابع بانک در سال
 آتی پیش بینی می گردد مانده تسهیلات ...
    MERGES A259:B259,C259:I259
  row 260 [EMPTY]
  row 261 [SINGLE_TEXT n=1 columns=A]: A261='برآورد شرکت از تغییرات در مانده ذخایر مطالبات مشکوک الوصول :'
  row 262 [MULTI_TEXT n=2 columns=A,C]: A262='دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ' | C262='با توجه به افزایش در حجم تسهیلات
 اعطایی پیش بینی می گردد مانده ذخیره...
    MERGES A262:B262,C262:I262
  row 263 [EMPTY]
  row 264 [SINGLE_TEXT n=1 columns=A]: A264='مانده سپرده های دریافتی از مشتریان :'
  row 265 [SINGLE_TEXT n=1 columns=A]: A265='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 266 [MULTI_TEXT n=4 columns=A,B,D,F]: A266='شرح' | B266='مانده سپرده ها' | D266='متوسط نرخ سود مانده سپرده ها' | F
266='برآورد مدیریت از تغییر در نرخ سود سپرده ها و تغییر در مانده سپرده ها...
    MERGES A266:A267,B266:C266,D266:E266,F266:F267
  row 267 [MULTI_TEXT n=4 columns=B,C,D,E]: B267='در تاریخ ۱۴۰۲/۱۲/۲۹' | C267='در تاریخ ۱۴۰۳/۰۶/۳۱' | D267='در تاریخ ۱۴۰
۲/۱۲/۲۹' | E267='در تاریخ ۱۴۰۳/۰۶/۳۱'
    MERGES A266:A267,F266:F267
  row 268 [SINGLE_TEXT n=1 columns=A]: A268='سپرده های ریالی: '

[BAND 11] rows=266:267 columns=A,B,C,D,E,F merges=A266:A267,B266:C266,D266:E266,F266:F267
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=269; gap=SINGLE_TEXT
  row 260 [EMPTY]
  row 261 [SINGLE_TEXT n=1 columns=A]: A261='برآورد شرکت از تغییرات در مانده ذخایر مطالبات مشکوک الوصول :'
  row 262 [MULTI_TEXT n=2 columns=A,C]: A262='دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ' | C262='با توجه به افزایش در حجم تسهیلات
 اعطایی پیش بینی می گردد مانده ذخیره...
    MERGES A262:B262,C262:I262
  row 263 [EMPTY]
  row 264 [SINGLE_TEXT n=1 columns=A]: A264='مانده سپرده های دریافتی از مشتریان :'
  row 265 [SINGLE_TEXT n=1 columns=A]: A265='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 266 [MULTI_TEXT n=4 columns=A,B,D,F]: A266='شرح' | B266='مانده سپرده ها' | D266='متوسط نرخ سود مانده سپرده ها' | F
266='برآورد مدیریت از تغییر در نرخ سود سپرده ها و تغییر در مانده سپرده ها...
    MERGES A266:A267,B266:C266,D266:E266,F266:F267
  row 267 [MULTI_TEXT n=4 columns=B,C,D,E]: B267='در تاریخ ۱۴۰۲/۱۲/۲۹' | C267='در تاریخ ۱۴۰۳/۰۶/۳۱' | D267='در تاریخ ۱۴۰
۲/۱۲/۲۹' | E267='در تاریخ ۱۴۰۳/۰۶/۳۱'
    MERGES A266:A267,F266:F267
  row 268 [SINGLE_TEXT n=1 columns=A]: A268='سپرده های ریالی: '
  row 269 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A269='سپرده های کوتاه مدت ' | B269=449329293 | C269=470781277 | D269=
0 | E269=0 | F269='با توجه به سیاستهای پولی و بانکی تغییری درنرخ سود سپرده ها پیش بینی ...
  row 270 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A270='سپرده های کوتاه مدت ویژه ' | B270=145711 | C270=453951 | D270=0
 | E270=0 | F270='با توجه به سیاستهای پولی و بانکی تغییری درنرخ سود سپرده ها پیش بینی ...
  row 271 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A271='سپرده های بلند مدت ' | B271=1634208566 | C271=1678516940 | D271
=0 | E271=0 | F271='با توجه به سیاستهای پولی و بانکی تغییری درنرخ سود سپرده ها پیش بینی ...
  row 272 [MIXED_NUMERIC n=3 columns=A,B,C]: A272='جمع سپرده های هزینه زا ' | B272=2083683570 | C272=2149752168
  row 273 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A273='سپرده های غیر هزینه زا ' | B273=689131598 | C273=710993381 | D2
73=0 | E273=0 | F273='با توجه به سیاستهای پولی و بانکی تغییری درنرخ سود سپرده ها پیش بینی ...

[BAND 12] rows=279:279 columns=A,B,C,D,E,F merges=—
  SIGNATURE=COMPOUND_CANDIDATE
  PRIOR prior_body=276; gap=SINGLE_TEXT,SINGLE_TEXT
  FOLLOWING next_body=280; gap=none
  row 273 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A273='سپرده های غیر هزینه زا ' | B273=689131598 | C273=710993381 | D2
73=0 | E273=0 | F273='با توجه به سیاستهای پولی و بانکی تغییری درنرخ سود سپرده ها پیش بینی ...
  row 274 [MIXED_NUMERIC n=3 columns=A,B,C]: A274='جمع سپرده های ریالی ' | B274=2772815168 | C274=2860745549
  row 275 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A275='سپرده های ارزی ' | B275=360010761 | C275=418802062 | D275=0 | E
275=0 | F275='با توجه به سیاستهای پولی و بانکی تغییری درنرخ سود سپرده ها پیش بینی ...
  row 276 [MIXED_NUMERIC n=3 columns=A,B,C]: A276='جمع سپرده های دریافتی ' | B276=3132825929 | C276=3279547611
    MERGES D276:J276
  row 277 [SINGLE_TEXT n=1 columns=A]: A277='اقلام زیر خط:'
  row 278 [SINGLE_TEXT n=1 columns=A]: A278='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 279 [MULTI_TEXT n=6 columns=A,B,C,D,E,F]: A279='شرح' | B279='۱۴۰۳/۰۶/۳۱' | C279='۱۴۰۲/۱۲/۲۹' | D279='شرح' | E279='
۱۴۰۳/۰۶/۳۱' | F279='۱۴۰۲/۱۲/۲۹'
  row 280 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A280='تعهدات مشتریان بابت اعتبارات اسنادی ' | B280=439498515 | C280=4
25497756 | D280='تعهدات بانک بابت اعتبارات اسنادی ' | E280=439498515 | F280=425497756
  row 281 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A281='تعهدات مشتریان بابت ضمانت نامه های صادره ' | B281=705682218 | C
281=620594993 | D281='تعهدات بانک بابت ضمانت نامه های صادره ' | E281=705682218 | F281=620594993
  row 282 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A282='ساير تعهدات مشتريان بانک ' | B282=19498400 | C282=12748156 | D2
82='سایر تعهدات بانک ' | E282=19498400 | F282=12748156
  row 283 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A283='وجوه اداره شده و موارد مشابه ' | B283=547 | C283=547 | D283='وج
وه اداره شده و موارد مشابه ' | E283=547 | F283=547
  row 284 [SINGLE_TEXT n=1 columns=A]: A284='توضیحات در خصوص تغییرات بااهمیت: '
    MERGES B284:F284
  row 285 [SINGLE_TEXT n=1 columns=A]: A285='«جملات آینده\u200cنگر نشان\u200cدهنده انتظارات، باورها یا پیش\u200cب...
    MERGES A285:I285

[BAND 13] rows=297:297 columns=A,B,C,D merges=—
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=298; gap=none
  row 291 [EMPTY]
  row 292 [EMPTY]
  row 293 [EMPTY]
  row 294 [SINGLE_TEXT n=1 columns=A]: A294='اطلاعات این فرم گزیده ای از اطلاعات گزارش تفسیری مدیریت می باشد که ه...
    MERGES A294:K294
  row 295 [SINGLE_TEXT n=1 columns=A]: A295='وضعیت کارکنان:'
  row 296 [SINGLE_TEXT n=1 columns=A]: A296='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 297 [MULTI_TEXT n=4 columns=A,B,C,D]: A297='شرح' | B297='در تاریخ ۱۴۰۲/۱۲/۲۹' | C297='در تاریخ ۱۴۰۳/۰۶/۳۱' | D297=
'برآورد در تاریخ ۱۴۰۳/۱۲/۳۰'
  row 298 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A298='تعداد شعب ' | B298=351 | C298=351 | D298=351
  row 299 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A299='تعداد کارکنان ' | B299=4769 | C299=4707 | D299=4707
  row 300 [SINGLE_TEXT n=1 columns=A]: A300='اطلاعات حق الوکاله و کفایت سرمایه'
  row 301 [SINGLE_TEXT n=1 columns=A]: A301='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 302 [MULTI_TEXT n=4 columns=A,B,C,D]: A302='شرح' | B302='سال مالی منتهی به۱۴۰۲/۱۲/۲۹' | C302='دوره ۶ ماهه منتهی به
 ۱۴۰۳/۰۶/۳۱' | D302='برآورد تغییر روند در دوره ۶ ماهه منتهی به ۱۴۰۳/۱۲/۳۰'
    MERGES D302:E302
  row 303 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A303='سهم بانک از درآمدهای مشاع ' | B303=0 | C303=0 | D303='-------------
------------------------------------------------ '
    MERGES D303:E303

[BAND 14] rows=302:302 columns=A,B,C,D merges=D302:E302
  SIGNATURE=COMPOUND_CANDIDATE
  PRIOR prior_body=299; gap=SINGLE_TEXT,SINGLE_TEXT
  FOLLOWING next_body=303; gap=none
  row 296 [SINGLE_TEXT n=1 columns=A]: A296='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 297 [MULTI_TEXT n=4 columns=A,B,C,D]: A297='شرح' | B297='در تاریخ ۱۴۰۲/۱۲/۲۹' | C297='در تاریخ ۱۴۰۳/۰۶/۳۱' | D297=
'برآورد در تاریخ ۱۴۰۳/۱۲/۳۰'
  row 298 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A298='تعداد شعب ' | B298=351 | C298=351 | D298=351
  row 299 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A299='تعداد کارکنان ' | B299=4769 | C299=4707 | D299=4707
  row 300 [SINGLE_TEXT n=1 columns=A]: A300='اطلاعات حق الوکاله و کفایت سرمایه'
  row 301 [SINGLE_TEXT n=1 columns=A]: A301='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 302 [MULTI_TEXT n=4 columns=A,B,C,D]: A302='شرح' | B302='سال مالی منتهی به۱۴۰۲/۱۲/۲۹' | C302='دوره ۶ ماهه منتهی به
 ۱۴۰۳/۰۶/۳۱' | D302='برآورد تغییر روند در دوره ۶ ماهه منتهی به ۱۴۰۳/۱۲/۳۰'
    MERGES D302:E302
  row 303 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A303='سهم بانک از درآمدهای مشاع ' | B303=0 | C303=0 | D303='-------------
------------------------------------------------ '
    MERGES D303:E303
  row 304 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A304='سهم سپرده گذاران از درآمدهای مشاع ' | B304=194221502 | C304=1122412
32 | D304='------------------------------------------------------------- '
    MERGES D304:E304
  row 305 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A305='نرخ حق الوکاله اعلام شده ' | B305=0 | C305=0 | D305='--------------
----------------------------------------------- '
    MERGES D305:E305
  row 306 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A306='مبلغ حق الوکاله اعمال شده ' | B306=0 | C306=0 | D306='-------------
------------------------------------------------ '
    MERGES D306:E306
  row 307 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A307='مابه التفاوت سود قابل پرداخت (مازاد سود پرداختی) به سپرده گذاران '
| B307=-69338916 | C307=-78487638 | D307='------------------------------------------------------------- '
    MERGES D307:E307
  row 308 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A308='نسبت کفایت سرمایه ' | B308=-3.4 | C308=-3.38 | D308='--------------
----------------------------------------------- '
    MERGES D308:E308

[BAND 15] rows=310:310 columns=A,B merges=B310:G310
  SIGNATURE=NO_MATCH
  PRIOR prior_body=308; gap=SINGLE_TEXT
  FOLLOWING next_body=315; gap=SINGLE_TEXT,SINGLE_TEXT,MULTI_TEXT,SINGLE_TEXT
  row 304 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A304='سهم سپرده گذاران از درآمدهای مشاع ' | B304=194221502 | C304=1122412
32 | D304='------------------------------------------------------------- '
    MERGES D304:E304
  row 305 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A305='نرخ حق الوکاله اعلام شده ' | B305=0 | C305=0 | D305='--------------
----------------------------------------------- '
    MERGES D305:E305
  row 306 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A306='مبلغ حق الوکاله اعمال شده ' | B306=0 | C306=0 | D306='-------------
------------------------------------------------ '
    MERGES D306:E306
  row 307 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A307='مابه التفاوت سود قابل پرداخت (مازاد سود پرداختی) به سپرده گذاران '
| B307=-69338916 | C307=-78487638 | D307='------------------------------------------------------------- '
    MERGES D307:E307
  row 308 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A308='نسبت کفایت سرمایه ' | B308=-3.4 | C308=-3.38 | D308='--------------
----------------------------------------------- '
    MERGES D308:E308
  row 309 [SINGLE_TEXT n=1 columns=A]: A309='اهداف و راهبردهای آتی مدیریت در خصوص فعالیت شرکت:'
  row 310 [MULTI_TEXT n=2 columns=A,B]: A310='اهداف و راهبردهای آتی مدیریت در خصوص فعالیت شرکت: ' | B310='--------------
------------------------------------------------------ '
    MERGES B310:G310
  row 311 [SINGLE_TEXT n=1 columns=A]: A311='درآمد حاصل از تسهيلات اعطايي و سپرده گذاري'
  row 312 [SINGLE_TEXT n=1 columns=A]: A312='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 313 [MULTI_TEXT n=6 columns=A,B,C,D,E,F]: A313='شرح' | B313='سال مالی منتهی به ۱۴۰۲/۱۲/۲۹' | C313='متوسط نرخ سود س
ال مالی منتهی به ۱۴۰۲/۱۲/۲۹ (درصد)' | D313='دوره ۶ ماهه منتهی به ۱۴۰۳/۰۶/۳۱' | E313='متوسط نرخ سود دوره ۶ ماهه منتهی به
۱۴۰۳/۰۶/۳۱ (درصد)' | F313='برآورد تغییر روند در دوره ۶ ماهه منتهی به ۱۴۰۳/۱۲/۳۰'
    MERGES F313:G313
  row 314 [SINGLE_TEXT n=1 columns=A]: A314='درآمد تسهیلات اعطایی: '
    MERGES F314:G314
  row 315 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A315='فروش اقساطی ' | B315=3892061 | C315=0 | D315=2134924 | E315=0 |
 F315='مبلغ درآمدسرمایه گذاریهای بانک درسال۱۴۰۳باافزایش مواجه گردد '
    MERGES F315:G315
  row 316 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A316='جعاله ' | B316=1753389 | C316=0 | D316=613663 | E316=0 | F316='
مبلغ درآمدسرمایه گذاریهای بانک درسال۱۴۰۳باافزایش مواجه گردد '
    MERGES F316:G316

[BAND 16] rows=313:313 columns=A,B,C,D,E,F merges=F313:G313
  SIGNATURE=NO_MATCH
  PRIOR prior_body=308; gap=SINGLE_TEXT,MULTI_TEXT,SINGLE_TEXT,SINGLE_TEXT
  FOLLOWING next_body=315; gap=SINGLE_TEXT
  row 307 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A307='مابه التفاوت سود قابل پرداخت (مازاد سود پرداختی) به سپرده گذاران '
| B307=-69338916 | C307=-78487638 | D307='------------------------------------------------------------- '
    MERGES D307:E307
  row 308 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A308='نسبت کفایت سرمایه ' | B308=-3.4 | C308=-3.38 | D308='--------------
----------------------------------------------- '
    MERGES D308:E308
  row 309 [SINGLE_TEXT n=1 columns=A]: A309='اهداف و راهبردهای آتی مدیریت در خصوص فعالیت شرکت:'
  row 310 [MULTI_TEXT n=2 columns=A,B]: A310='اهداف و راهبردهای آتی مدیریت در خصوص فعالیت شرکت: ' | B310='--------------
------------------------------------------------------ '
    MERGES B310:G310
  row 311 [SINGLE_TEXT n=1 columns=A]: A311='درآمد حاصل از تسهيلات اعطايي و سپرده گذاري'
  row 312 [SINGLE_TEXT n=1 columns=A]: A312='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 313 [MULTI_TEXT n=6 columns=A,B,C,D,E,F]: A313='شرح' | B313='سال مالی منتهی به ۱۴۰۲/۱۲/۲۹' | C313='متوسط نرخ سود س
ال مالی منتهی به ۱۴۰۲/۱۲/۲۹ (درصد)' | D313='دوره ۶ ماهه منتهی به ۱۴۰۳/۰۶/۳۱' | E313='متوسط نرخ سود دوره ۶ ماهه منتهی به
۱۴۰۳/۰۶/۳۱ (درصد)' | F313='برآورد تغییر روند در دوره ۶ ماهه منتهی به ۱۴۰۳/۱۲/۳۰'
    MERGES F313:G313
  row 314 [SINGLE_TEXT n=1 columns=A]: A314='درآمد تسهیلات اعطایی: '
    MERGES F314:G314
  row 315 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A315='فروش اقساطی ' | B315=3892061 | C315=0 | D315=2134924 | E315=0 |
 F315='مبلغ درآمدسرمایه گذاریهای بانک درسال۱۴۰۳باافزایش مواجه گردد '
    MERGES F315:G315
  row 316 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A316='جعاله ' | B316=1753389 | C316=0 | D316=613663 | E316=0 | F316='
مبلغ درآمدسرمایه گذاریهای بانک درسال۱۴۰۳باافزایش مواجه گردد '
    MERGES F316:G316
  row 317 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A317='اجاره به شرط تملیک ' | B317=0 | C317=0 | D317=0 | E317=0 | F317
='مبلغ درآمدسرمایه گذاریهای بانک درسال۱۴۰۳باافزایش مواجه گردد '
    MERGES F317:G317
  row 318 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A318='سلف ' | B318=0 | C318=0 | D318=0 | E318=0 | F318='مبلغ درآمدسرم
ایه گذاریهای بانک درسال۱۴۰۳باافزایش مواجه گردد '
    MERGES F318:G318
  row 319 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A319='مضاربه ' | B319=284 | C319=0 | D319=0 | E319=0 | F319='مبلغ درآ
مدسرمایه گذاریهای بانک درسال۱۴۰۳باافزایش مواجه گردد '
    MERGES F319:G319

[BAND 17] rows=333:333 columns=A,C merges=A333:B333,C333:I333
  SIGNATURE=NO_MATCH
  PRIOR prior_body=332; gap=none
  FOLLOWING next_body=337; gap=SINGLE_TEXT,SINGLE_TEXT,MULTI_TEXT
  row 327 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A327='جمع درآمد حاصل از تسهیلات اعطایی ' | B327=167675885 | C327=0 |
D327=129981422 | E327=0 | F327='مبلغ درآمدسرمایه گذاریهای بانک درسال۱۴۰۳باافزایش مواجه گردد '
    MERGES F327:G327
  row 328 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A328='جایزه سپرده قانونی ' | B328=2326102 | C328=0 | D328=1422354 | E
328=0 | F328='مبلغ درآمدسرمایه گذاریهای بانک درسال۱۴۰۳باافزایش مواجه گردد '
    MERGES F328:G328
  row 329 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A329='سود حاصل از سپرده گذاری در بانکها ' | B329=5443442 | C329=0 | D
329=4580248 | E329=0 | F329='مبلغ درآمدسرمایه گذاریهای بانک درسال۱۴۰۳باافزایش مواجه گردد '
    MERGES F329:G329
  row 330 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A330='جمع سود حاصل از سپرده گذاری ها ' | B330=7769544 | C330=0 | D330
=6002602 | E330=0 | F330='مبلغ درآمدسرمایه گذاریهای بانک درسال۱۴۰۳باافزایش مواجه گردد '
    MERGES F330:G330
  row 331 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A331='درآمد اوراق بدهی و سایر درآمدهای ناشی از سپرده گذاری ' | B331=5
4403764 | C331=0 | D331=11202306 | E331=0 | F331='مبلغ درآمدسرمایه گذاریهای بانک درسال۱۴۰۳باافزایش مواجه گردد '
    MERGES F331:G331
  row 332 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A332='درآمد حاصل ازتسهیلات اعطایی و سپرده\u200cگذاری\u200cها ' | B332
=229849193 | C332=0 | D332=147186330 | E332=0 | F332='مبلغ درآمدسرمایه گذاریهای بانک درسال۱۴۰۳باافزایش مواجه گردد '
    MERGES F332:G332
  row 333 [MULTI_TEXT n=2 columns=A,C]: A333='ارائه توضیحات در خصوص نحوه محاسبه متوسط نرخ سود تسهیلات: ' | C333='-------
-------------------------------------------------------------...
    MERGES A333:B333,C333:I333
  row 334 [SINGLE_TEXT n=1 columns=A]: A334='خالص سود (زیان) سرمایه گذاری\u200c ها'
  row 335 [SINGLE_TEXT n=1 columns=A]: A335='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 336 [MULTI_TEXT n=4 columns=A,B,C,D]: A336='شرح' | B336='سال مالی منتهی به۱۴۰۲/۱۲/۲۹' | C336='دوره ۶ ماهه منتهی به
 ۱۴۰۳/۰۶/۳۱' | D336='برآورد تغییر روند در دوره ۶ ماهه منتهی به ۱۴۰۳/۱۲/۳۰'
    MERGES D336:E336
  row 337 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A337='درآمد حاصل از سرمایه گذاری در سهام ' | B337=2453194 | C337=402420 |
 D337='مبلغ درآمدسرمایه گذاریهای بانک درسال ۱۴۰۳ باافزایش مواجه گردد '
    MERGES D337:E337
  row 338 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A338='سود(زیان) حاصل از فروش سرمایه گذاری ' | B338=0 | C338=0 | D338='مبل
غ درآمدسرمایه گذاریهای بانک درسال ۱۴۰۳ باافزایش مواجه گردد '
    MERGES D338:E338
  row 339 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A339='سود (زیان) تعدیل ذخیره کاهش ارزش سرمایه گذاریها ' | B339=0 | C339=0
 | D339='مبلغ درآمدسرمایه گذاریهای بانک درسال ۱۴۰۳ باافزایش مواجه گردد '
    MERGES D339:E339

[BAND 18] rows=336:336 columns=A,B,C,D merges=D336:E336
  SIGNATURE=NO_MATCH
  PRIOR prior_body=332; gap=MULTI_TEXT,SINGLE_TEXT,SINGLE_TEXT
  FOLLOWING next_body=337; gap=none
  row 330 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A330='جمع سود حاصل از سپرده گذاری ها ' | B330=7769544 | C330=0 | D330
=6002602 | E330=0 | F330='مبلغ درآمدسرمایه گذاریهای بانک درسال۱۴۰۳باافزایش مواجه گردد '
    MERGES F330:G330
  row 331 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A331='درآمد اوراق بدهی و سایر درآمدهای ناشی از سپرده گذاری ' | B331=5
4403764 | C331=0 | D331=11202306 | E331=0 | F331='مبلغ درآمدسرمایه گذاریهای بانک درسال۱۴۰۳باافزایش مواجه گردد '
    MERGES F331:G331
  row 332 [MIXED_NUMERIC n=6 columns=A,B,C,D,E,F]: A332='درآمد حاصل ازتسهیلات اعطایی و سپرده\u200cگذاری\u200cها ' | B332
=229849193 | C332=0 | D332=147186330 | E332=0 | F332='مبلغ درآمدسرمایه گذاریهای بانک درسال۱۴۰۳باافزایش مواجه گردد '
    MERGES F332:G332
  row 333 [MULTI_TEXT n=2 columns=A,C]: A333='ارائه توضیحات در خصوص نحوه محاسبه متوسط نرخ سود تسهیلات: ' | C333='-------
-------------------------------------------------------------...
    MERGES A333:B333,C333:I333
  row 334 [SINGLE_TEXT n=1 columns=A]: A334='خالص سود (زیان) سرمایه گذاری\u200c ها'
  row 335 [SINGLE_TEXT n=1 columns=A]: A335='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 336 [MULTI_TEXT n=4 columns=A,B,C,D]: A336='شرح' | B336='سال مالی منتهی به۱۴۰۲/۱۲/۲۹' | C336='دوره ۶ ماهه منتهی به
 ۱۴۰۳/۰۶/۳۱' | D336='برآورد تغییر روند در دوره ۶ ماهه منتهی به ۱۴۰۳/۱۲/۳۰'
    MERGES D336:E336
  row 337 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A337='درآمد حاصل از سرمایه گذاری در سهام ' | B337=2453194 | C337=402420 |
 D337='مبلغ درآمدسرمایه گذاریهای بانک درسال ۱۴۰۳ باافزایش مواجه گردد '
    MERGES D337:E337
  row 338 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A338='سود(زیان) حاصل از فروش سرمایه گذاری ' | B338=0 | C338=0 | D338='مبل
غ درآمدسرمایه گذاریهای بانک درسال ۱۴۰۳ باافزایش مواجه گردد '
    MERGES D338:E338
  row 339 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A339='سود (زیان) تعدیل ذخیره کاهش ارزش سرمایه گذاریها ' | B339=0 | C339=0
 | D339='مبلغ درآمدسرمایه گذاریهای بانک درسال ۱۴۰۳ باافزایش مواجه گردد '
    MERGES D339:E339
  row 340 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A340='جمع درآمدهای حاصل از سرمایه گذاری ' | B340=2453194 | C340=402420 |
D340='مبلغ درآمدسرمایه گذاریهای بانک درسال ۱۴۰۳ باافزایش مواجه گردد '
    MERGES D340:E340
  row 341 [SINGLE_TEXT n=1 columns=A]: A341='«جملات آینده\u200cنگر نشان\u200cدهنده انتظارات، باورها یا پیش\u200cب...
    MERGES A341:G341
  row 342 [EMPTY]

[BAND 19] rows=353:354 columns=A,C,D,E,F,G,H,I,J merges=A353:B354,C353:F353,G353:I353,J353:K354
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=355; gap=none
  row 347 [EMPTY]
  row 348 [EMPTY]
  row 349 [EMPTY]
  row 350 [SINGLE_TEXT n=1 columns=A]: A350='اطلاعات اين فرم گزيده اي از اطلاعات گزارش تفسيري مديريت مي باشد که ه...
    MERGES A350:K350
  row 351 [SINGLE_TEXT n=1 columns=A]: A351='وضعیت شرکتهای سرمایه پذیر:'
  row 352 [SINGLE_TEXT n=1 columns=A]: A352='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 353 [MULTI_TEXT n=4 columns=A,C,G,J]: A353='نام شرکت' | C353='سال مالي منتهي به ۱۴۰۲/۱۲/۲۹' | G353='دوره ۶ ماهه من
تهي به ۱۴۰۳/۰۶/۳۱' | J353='تشريح آخرين وضعيت و برنامه هاي آتي شرکت در شرکت سرمايه پذير'
    MERGES A353:B354,C353:F353,G353:I353,J353:K354
  row 354 [MULTI_TEXT n=7 columns=C,D,E,F,G,H,I]: C354='درصد مالکيت' | D354='بهاي تمام شده' | E354='سال مالي شرکت سرمايه
 پذير' | F354='درآمد سرمايه گذاري' | G354='درصد مالکيت' | H354='بهاي تمام شده' | I354='درآمد سرمايه گذاري'
    MERGES A353:B354,J353:K354
  row 355 [MIXED_NUMERIC n=9 columns=A,C,D,E,F,G,H,I,J]: A355='صرافي پارسيان ' | C355=79 | D355=1191004 | E355='۱۴۰۲/۱۰/
۳۰ ' | F355=237598 | G355=79 | H355=1191004 | I355=0 | J355='سود نقدی سرمایه گذاری ها تا پایان سال جاری نسبت به سال ۱۴۰۳
 افزایش م...
    MERGES A355:B355,J355:K355
  row 356 [MIXED_NUMERIC n=9 columns=A,C,D,E,F,G,H,I,J]: A356='ساير شرکتهاي خارج از بورس ' | C356=1 | D356=122338363 | E
356='۱۴۰۲/۱۰/۳۰ ' | F356=20723284 | G356=1 | H356=122338363 | I356=0 | J356='سود نقدی سرمایه گذاری ها تا پایان سال جاری
نسبت به سال ۱۴۰۳ افزایش م...
    MERGES A356:B356,J356:K356
  row 357 [MIXED_NUMERIC n=9 columns=A,C,D,E,F,G,H,I,J]: A357='گروه داده پردازي پارسيان ' | C357=100 | D357=36279443 | E
357='۱۴۰۲/۱۰/۳۰ ' | F357=2339955 | G357=100 | H357=36279443 | I357=0 | J357='سود نقدی سرمایه گذاری ها تا پایان سال جاری
نسبت به سال ۱۴۰۳ افزایش م...
    MERGES A357:B357,J357:K357
  row 358 [MIXED_NUMERIC n=9 columns=A,C,D,E,F,G,H,I,J]: A358='گروه مالي بانک پارسيان ' | C358=100 | D358=45109293 | E35
8='۱۴۰۲/۱۰/۳۰ ' | F358=19999990 | G358=100 | H358=45109293 | I358=0 | J358='سود نقدی سرمایه گذاری ها تا پایان سال جاری ن
سبت به سال ۱۴۰۳ افزایش م...
    MERGES A358:B358,J358:K358
  row 359 [SINGLE_TEXT n=1 columns=A]: A359='ساير درآمدها و هزینه های عملياتي:'
  row 360 [SINGLE_TEXT n=1 columns=A]: A360='کلیه مبالغ درج شده به میلیون ریال می باشد'

[BAND 20] rows=361:361 columns=A,B,C merges=—
  SIGNATURE=COMPOUND_CANDIDATE
  PRIOR prior_body=358; gap=SINGLE_TEXT,SINGLE_TEXT
  FOLLOWING next_body=363; gap=SINGLE_TEXT
  row 355 [MIXED_NUMERIC n=9 columns=A,C,D,E,F,G,H,I,J]: A355='صرافي پارسيان ' | C355=79 | D355=1191004 | E355='۱۴۰۲/۱۰/
۳۰ ' | F355=237598 | G355=79 | H355=1191004 | I355=0 | J355='سود نقدی سرمایه گذاری ها تا پایان سال جاری نسبت به سال ۱۴۰۳
 افزایش م...
    MERGES A355:B355,J355:K355
  row 356 [MIXED_NUMERIC n=9 columns=A,C,D,E,F,G,H,I,J]: A356='ساير شرکتهاي خارج از بورس ' | C356=1 | D356=122338363 | E
356='۱۴۰۲/۱۰/۳۰ ' | F356=20723284 | G356=1 | H356=122338363 | I356=0 | J356='سود نقدی سرمایه گذاری ها تا پایان سال جاری
نسبت به سال ۱۴۰۳ افزایش م...
    MERGES A356:B356,J356:K356
  row 357 [MIXED_NUMERIC n=9 columns=A,C,D,E,F,G,H,I,J]: A357='گروه داده پردازي پارسيان ' | C357=100 | D357=36279443 | E
357='۱۴۰۲/۱۰/۳۰ ' | F357=2339955 | G357=100 | H357=36279443 | I357=0 | J357='سود نقدی سرمایه گذاری ها تا پایان سال جاری
نسبت به سال ۱۴۰۳ افزایش م...
    MERGES A357:B357,J357:K357
  row 358 [MIXED_NUMERIC n=9 columns=A,C,D,E,F,G,H,I,J]: A358='گروه مالي بانک پارسيان ' | C358=100 | D358=45109293 | E35
8='۱۴۰۲/۱۰/۳۰ ' | F358=19999990 | G358=100 | H358=45109293 | I358=0 | J358='سود نقدی سرمایه گذاری ها تا پایان سال جاری ن
سبت به سال ۱۴۰۳ افزایش م...
    MERGES A358:B358,J358:K358
  row 359 [SINGLE_TEXT n=1 columns=A]: A359='ساير درآمدها و هزینه های عملياتي:'
  row 360 [SINGLE_TEXT n=1 columns=A]: A360='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 361 [MULTI_TEXT n=3 columns=A,B,C]: A361='شرح' | B361='۱۴۰۲/۱۲/۲۹' | C361='۱۴۰۳/۰۶/۳۱'
  row 362 [SINGLE_TEXT n=1 columns=A]: A362='ساير درآمدهاي عملياتي: '
  row 363 [MIXED_NUMERIC n=3 columns=A,B,C]: A363='ساير درآمدهاي عملياتي ' | B363=151543669 | C363=84513662
  row 364 [EMPTY]
  row 365 [MIXED_NUMERIC n=3 columns=A,B,C]: A365='جمع ساير درآمدهاي عملياتي ' | B365=151543669 | C365=84513662
  row 366 [SINGLE_TEXT n=1 columns=A]: A366='ساير هزينه هاي عملياتي: '
  row 367 [MIXED_NUMERIC n=3 columns=A,B,C]: A367='ساير هزينه هاي عملياتي ' | B367=0 | C367=0

[BAND 21] rows=372:372 columns=A,C merges=A372:B372,C372:F372
  SIGNATURE=NO_MATCH
  PRIOR prior_body=370; gap=SINGLE_TEXT
  FOLLOWING next_body=377; gap=EMPTY,SINGLE_TEXT,SINGLE_TEXT,MULTI_TEXT
  row 366 [SINGLE_TEXT n=1 columns=A]: A366='ساير هزينه هاي عملياتي: '
  row 367 [MIXED_NUMERIC n=3 columns=A,B,C]: A367='ساير هزينه هاي عملياتي ' | B367=0 | C367=0
  row 368 [EMPTY]
  row 369 [MIXED_NUMERIC n=3 columns=A,B,C]: A369='جمع ساير هزينه هاي عملياتي ' | B369=0 | C369=0
  row 370 [MIXED_NUMERIC n=3 columns=A,B,C]: A370='جمع ساير درآمدها و هزينه هاي عملياتي ' | B370=151543669 | C370=845136
62
  row 371 [SINGLE_TEXT n=1 columns=A]: A371='برآورد شرکت از تغییرات خالص سایر درآمدها (هزینه ها)ی عملیاتی:'
  row 372 [MULTI_TEXT n=2 columns=A,C]: A372='دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ' | C372='--------------------------------
------------------------------------...
    MERGES A372:B372,C372:F372
  row 373 [EMPTY]
  row 374 [SINGLE_TEXT n=1 columns=A]: A374='خالص ساير درآمدها و هزینه ها:'
  row 375 [SINGLE_TEXT n=1 columns=A]: A375='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 376 [MULTI_TEXT n=3 columns=A,B,C]: A376='خالص ساير درآمدها و هزينه ها' | B376='۱۴۰۲/۱۲/۲۹' | C376='۱۴۰۳/۰۶/۳۱'
  row 377 [MIXED_NUMERIC n=3 columns=A,B,C]: A377='ساير درامدها ' | B377=43015355 | C377=2192360
  row 378 [MIXED_NUMERIC n=3 columns=A,B,C]: A378='ساير هزينه ها ' | B378=0 | C378=0

[BAND 22] rows=376:376 columns=A,B,C merges=—
  SIGNATURE=NO_MATCH
  PRIOR prior_body=370; gap=SINGLE_TEXT,MULTI_TEXT,EMPTY,SINGLE_TEXT,SINGLE_TEXT
  FOLLOWING next_body=377; gap=none
  row 370 [MIXED_NUMERIC n=3 columns=A,B,C]: A370='جمع ساير درآمدها و هزينه هاي عملياتي ' | B370=151543669 | C370=845136
62
  row 371 [SINGLE_TEXT n=1 columns=A]: A371='برآورد شرکت از تغییرات خالص سایر درآمدها (هزینه ها)ی عملیاتی:'
  row 372 [MULTI_TEXT n=2 columns=A,C]: A372='دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ' | C372='--------------------------------
------------------------------------...
    MERGES A372:B372,C372:F372
  row 373 [EMPTY]
  row 374 [SINGLE_TEXT n=1 columns=A]: A374='خالص ساير درآمدها و هزینه ها:'
  row 375 [SINGLE_TEXT n=1 columns=A]: A375='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 376 [MULTI_TEXT n=3 columns=A,B,C]: A376='خالص ساير درآمدها و هزينه ها' | B376='۱۴۰۲/۱۲/۲۹' | C376='۱۴۰۳/۰۶/۳۱'
  row 377 [MIXED_NUMERIC n=3 columns=A,B,C]: A377='ساير درامدها ' | B377=43015355 | C377=2192360
  row 378 [MIXED_NUMERIC n=3 columns=A,B,C]: A378='ساير هزينه ها ' | B378=0 | C378=0
  row 379 [EMPTY]
  row 380 [MIXED_NUMERIC n=3 columns=A,B,C]: A380='جمع خالص ساير درآمدها و هزينه ها ' | B380=43015355 | C380=2192360
  row 381 [SINGLE_TEXT n=1 columns=A]: A381='برآورد شرکت از تغییرات خالص ساير درآمدها و هزینه ها :'
  row 382 [MULTI_TEXT n=2 columns=A,C]: A382='دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ' | C382='--------------------------------
------------------------------------...
    MERGES A382:B382,C382:F382

[BAND 23] rows=382:382 columns=A,C merges=A382:B382,C382:F382
  SIGNATURE=NO_MATCH
  PRIOR prior_body=380; gap=SINGLE_TEXT
  FOLLOWING next_body=387; gap=EMPTY,SINGLE_TEXT,SINGLE_TEXT,MULTI_TEXT
  row 376 [MULTI_TEXT n=3 columns=A,B,C]: A376='خالص ساير درآمدها و هزينه ها' | B376='۱۴۰۲/۱۲/۲۹' | C376='۱۴۰۳/۰۶/۳۱'
  row 377 [MIXED_NUMERIC n=3 columns=A,B,C]: A377='ساير درامدها ' | B377=43015355 | C377=2192360
  row 378 [MIXED_NUMERIC n=3 columns=A,B,C]: A378='ساير هزينه ها ' | B378=0 | C378=0
  row 379 [EMPTY]
  row 380 [MIXED_NUMERIC n=3 columns=A,B,C]: A380='جمع خالص ساير درآمدها و هزينه ها ' | B380=43015355 | C380=2192360
  row 381 [SINGLE_TEXT n=1 columns=A]: A381='برآورد شرکت از تغییرات خالص ساير درآمدها و هزینه ها :'
  row 382 [MULTI_TEXT n=2 columns=A,C]: A382='دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ' | C382='--------------------------------
------------------------------------...
    MERGES A382:B382,C382:F382
  row 383 [EMPTY]
  row 384 [SINGLE_TEXT n=1 columns=A]: A384='هزینه های اداری و عمومی:'
  row 385 [SINGLE_TEXT n=1 columns=A]: A385='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 386 [MULTI_TEXT n=3 columns=A,B,C]: A386='هزينه هاي اداري و عمومي' | B386='۱۴۰۲/۱۲/۲۹' | C386='۱۴۰۳/۰۶/۳۱'
  row 387 [MIXED_NUMERIC n=3 columns=A,B,C]: A387='هزينه هاي اداري و عمومي ' | B387=-52654898 | C387=-28908689
  row 388 [EMPTY]

[BAND 24] rows=386:386 columns=A,B,C merges=—
  SIGNATURE=NO_MATCH
  PRIOR prior_body=380; gap=SINGLE_TEXT,MULTI_TEXT,EMPTY,SINGLE_TEXT,SINGLE_TEXT
  FOLLOWING next_body=387; gap=none
  row 380 [MIXED_NUMERIC n=3 columns=A,B,C]: A380='جمع خالص ساير درآمدها و هزينه ها ' | B380=43015355 | C380=2192360
  row 381 [SINGLE_TEXT n=1 columns=A]: A381='برآورد شرکت از تغییرات خالص ساير درآمدها و هزینه ها :'
  row 382 [MULTI_TEXT n=2 columns=A,C]: A382='دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ' | C382='--------------------------------
------------------------------------...
    MERGES A382:B382,C382:F382
  row 383 [EMPTY]
  row 384 [SINGLE_TEXT n=1 columns=A]: A384='هزینه های اداری و عمومی:'
  row 385 [SINGLE_TEXT n=1 columns=A]: A385='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 386 [MULTI_TEXT n=3 columns=A,B,C]: A386='هزينه هاي اداري و عمومي' | B386='۱۴۰۲/۱۲/۲۹' | C386='۱۴۰۳/۰۶/۳۱'
  row 387 [MIXED_NUMERIC n=3 columns=A,B,C]: A387='هزينه هاي اداري و عمومي ' | B387=-52654898 | C387=-28908689
  row 388 [EMPTY]
  row 389 [MIXED_NUMERIC n=3 columns=A,B,C]: A389='جمع هزينه هاي اداري و عمومي ' | B389=-52654898 | C389=-28908689
  row 390 [SINGLE_TEXT n=1 columns=A]: A390='برآورد شرکت از تغییرات هزینه های اداری و عمومی :'
  row 391 [MULTI_TEXT n=2 columns=A,C]: A391='دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ' | C391='--------------------------------
------------------------------------...
    MERGES A391:B391,C391:F391
  row 392 [EMPTY]

[BAND 25] rows=391:391 columns=A,C merges=A391:B391,C391:F391
  SIGNATURE=NO_MATCH
  PRIOR prior_body=389; gap=SINGLE_TEXT
  FOLLOWING next_body=396; gap=EMPTY,SINGLE_TEXT,SINGLE_TEXT,MULTI_TEXT
  row 385 [SINGLE_TEXT n=1 columns=A]: A385='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 386 [MULTI_TEXT n=3 columns=A,B,C]: A386='هزينه هاي اداري و عمومي' | B386='۱۴۰۲/۱۲/۲۹' | C386='۱۴۰۳/۰۶/۳۱'
  row 387 [MIXED_NUMERIC n=3 columns=A,B,C]: A387='هزينه هاي اداري و عمومي ' | B387=-52654898 | C387=-28908689
  row 388 [EMPTY]
  row 389 [MIXED_NUMERIC n=3 columns=A,B,C]: A389='جمع هزينه هاي اداري و عمومي ' | B389=-52654898 | C389=-28908689
  row 390 [SINGLE_TEXT n=1 columns=A]: A390='برآورد شرکت از تغییرات هزینه های اداری و عمومی :'
  row 391 [MULTI_TEXT n=2 columns=A,C]: A391='دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ' | C391='--------------------------------
------------------------------------...
    MERGES A391:B391,C391:F391
  row 392 [EMPTY]
  row 393 [SINGLE_TEXT n=1 columns=A]: A393='هزینه مالی:'
  row 394 [SINGLE_TEXT n=1 columns=A]: A394='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 395 [MULTI_TEXT n=3 columns=A,B,C]: A395='هزينه\u200cهاي مالي' | B395='۱۴۰۲/۱۲/۲۹' | C395='۱۴۰۳/۰۶/۳۱'
  row 396 [MIXED_NUMERIC n=3 columns=A,B,C]: A396='هزينه مالي تسهيلات دريافتي از ساير بانکها و موسسات اعتباري ' | B396=0
 | C396=0
  row 397 [MIXED_NUMERIC n=3 columns=A,B,C]: A397='جريمه اضافه برداشت از بانک مرکزي ' | B397=0 | C397=0

[BAND 26] rows=395:395 columns=A,B,C merges=—
  SIGNATURE=NO_MATCH
  PRIOR prior_body=389; gap=SINGLE_TEXT,MULTI_TEXT,EMPTY,SINGLE_TEXT,SINGLE_TEXT
  FOLLOWING next_body=396; gap=none
  row 389 [MIXED_NUMERIC n=3 columns=A,B,C]: A389='جمع هزينه هاي اداري و عمومي ' | B389=-52654898 | C389=-28908689
  row 390 [SINGLE_TEXT n=1 columns=A]: A390='برآورد شرکت از تغییرات هزینه های اداری و عمومی :'
  row 391 [MULTI_TEXT n=2 columns=A,C]: A391='دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ' | C391='--------------------------------
------------------------------------...
    MERGES A391:B391,C391:F391
  row 392 [EMPTY]
  row 393 [SINGLE_TEXT n=1 columns=A]: A393='هزینه مالی:'
  row 394 [SINGLE_TEXT n=1 columns=A]: A394='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 395 [MULTI_TEXT n=3 columns=A,B,C]: A395='هزينه\u200cهاي مالي' | B395='۱۴۰۲/۱۲/۲۹' | C395='۱۴۰۳/۰۶/۳۱'
  row 396 [MIXED_NUMERIC n=3 columns=A,B,C]: A396='هزينه مالي تسهيلات دريافتي از ساير بانکها و موسسات اعتباري ' | B396=0
 | C396=0
  row 397 [MIXED_NUMERIC n=3 columns=A,B,C]: A397='جريمه اضافه برداشت از بانک مرکزي ' | B397=0 | C397=0
  row 398 [MIXED_NUMERIC n=3 columns=A,B,C]: A398='ساير هزينه هاي مالي ' | B398=-20082491 | C398=-5804157
  row 399 [MIXED_NUMERIC n=3 columns=A,B,C]: A399='جمع هزينه\u200cهاي مالي ' | B399=-20082491 | C399=-5804157
  row 400 [SINGLE_TEXT n=1 columns=A]: A400='برآورد شرکت از تغییرات هزینه های مالی :'
  row 401 [MULTI_TEXT n=2 columns=A,C]: A401='دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ' | C401='--------------------------------
------------------------------------...
    MERGES A401:B401,C401:F401

[BAND 27] rows=401:401 columns=A,C merges=A401:B401,C401:F401
  SIGNATURE=NO_MATCH
  PRIOR prior_body=399; gap=SINGLE_TEXT
  FOLLOWING next_body=405; gap=EMPTY,SINGLE_TEXT,MULTI_TEXT
  row 395 [MULTI_TEXT n=3 columns=A,B,C]: A395='هزينه\u200cهاي مالي' | B395='۱۴۰۲/۱۲/۲۹' | C395='۱۴۰۳/۰۶/۳۱'
  row 396 [MIXED_NUMERIC n=3 columns=A,B,C]: A396='هزينه مالي تسهيلات دريافتي از ساير بانکها و موسسات اعتباري ' | B396=0
 | C396=0
  row 397 [MIXED_NUMERIC n=3 columns=A,B,C]: A397='جريمه اضافه برداشت از بانک مرکزي ' | B397=0 | C397=0
  row 398 [MIXED_NUMERIC n=3 columns=A,B,C]: A398='ساير هزينه هاي مالي ' | B398=-20082491 | C398=-5804157
  row 399 [MIXED_NUMERIC n=3 columns=A,B,C]: A399='جمع هزينه\u200cهاي مالي ' | B399=-20082491 | C399=-5804157
  row 400 [SINGLE_TEXT n=1 columns=A]: A400='برآورد شرکت از تغییرات هزینه های مالی :'
  row 401 [MULTI_TEXT n=2 columns=A,C]: A401='دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ' | C401='--------------------------------
------------------------------------...
    MERGES A401:B401,C401:F401
  row 402 [EMPTY]
  row 403 [SINGLE_TEXT n=1 columns=A]: A403='برنامه شرکت در خصوص تقسیم سود'
  row 404 [MULTI_TEXT n=5 columns=A,B,C,D,E]: A404='مبلغ سود (زيان) انباشته پايان سال مالي گذشته' | B404='سود سهام پيشنه
ادي هيئت مديره در سال مالي گذشته' | C404='مبلغ سود (زيان) خالص سال مالي گذشته' | D404='سود سهام مصوب مجمع سال مالي گذشته
' | E404='پيشنهاد هيئت مديره درخصوص درصد تقسيم سود سال مالي جاري'
  row 405 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A405=-44764295 | B405=0 | C405=-9124895 | D405=0 | E405=0
  row 406 [SINGLE_TEXT n=1 columns=A]: A406='سایر برنامه های با اهمیت شرکت'
  row 407 [MULTI_TEXT n=2 columns=A,B]: A407='دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ' | B407='--------------------------------
------------------------------------ '
    MERGES B407:E407

[BAND 28] rows=404:404 columns=A,B,C,D,E merges=—
  SIGNATURE=NO_MATCH
  PRIOR prior_body=399; gap=SINGLE_TEXT,MULTI_TEXT,EMPTY,SINGLE_TEXT
  FOLLOWING next_body=405; gap=none
  row 398 [MIXED_NUMERIC n=3 columns=A,B,C]: A398='ساير هزينه هاي مالي ' | B398=-20082491 | C398=-5804157
  row 399 [MIXED_NUMERIC n=3 columns=A,B,C]: A399='جمع هزينه\u200cهاي مالي ' | B399=-20082491 | C399=-5804157
  row 400 [SINGLE_TEXT n=1 columns=A]: A400='برآورد شرکت از تغییرات هزینه های مالی :'
  row 401 [MULTI_TEXT n=2 columns=A,C]: A401='دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ' | C401='--------------------------------
------------------------------------...
    MERGES A401:B401,C401:F401
  row 402 [EMPTY]
  row 403 [SINGLE_TEXT n=1 columns=A]: A403='برنامه شرکت در خصوص تقسیم سود'
  row 404 [MULTI_TEXT n=5 columns=A,B,C,D,E]: A404='مبلغ سود (زيان) انباشته پايان سال مالي گذشته' | B404='سود سهام پيشنه
ادي هيئت مديره در سال مالي گذشته' | C404='مبلغ سود (زيان) خالص سال مالي گذشته' | D404='سود سهام مصوب مجمع سال مالي گذشته
' | E404='پيشنهاد هيئت مديره درخصوص درصد تقسيم سود سال مالي جاري'
  row 405 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A405=-44764295 | B405=0 | C405=-9124895 | D405=0 | E405=0
  row 406 [SINGLE_TEXT n=1 columns=A]: A406='سایر برنامه های با اهمیت شرکت'
  row 407 [MULTI_TEXT n=2 columns=A,B]: A407='دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ' | B407='--------------------------------
------------------------------------ '
    MERGES B407:E407
  row 408 [EMPTY]
  row 409 [SINGLE_TEXT n=1 columns=A]: A409='سایر توضیحات با اهمیت'
  row 410 [SINGLE_TEXT n=1 columns=A]: A410='--------------------------------------------------------------------...
    MERGES A410:I410

[BAND 29] rows=407:407 columns=A,B merges=B407:E407
  SIGNATURE=NO_MATCH
  PRIOR prior_body=405; gap=SINGLE_TEXT
  FOLLOWING next_body=None; gap=none
  row 401 [MULTI_TEXT n=2 columns=A,C]: A401='دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ' | C401='--------------------------------
------------------------------------...
    MERGES A401:B401,C401:F401
  row 402 [EMPTY]
  row 403 [SINGLE_TEXT n=1 columns=A]: A403='برنامه شرکت در خصوص تقسیم سود'
  row 404 [MULTI_TEXT n=5 columns=A,B,C,D,E]: A404='مبلغ سود (زيان) انباشته پايان سال مالي گذشته' | B404='سود سهام پيشنه
ادي هيئت مديره در سال مالي گذشته' | C404='مبلغ سود (زيان) خالص سال مالي گذشته' | D404='سود سهام مصوب مجمع سال مالي گذشته
' | E404='پيشنهاد هيئت مديره درخصوص درصد تقسيم سود سال مالي جاري'
  row 405 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A405=-44764295 | B405=0 | C405=-9124895 | D405=0 | E405=0
  row 406 [SINGLE_TEXT n=1 columns=A]: A406='سایر برنامه های با اهمیت شرکت'
  row 407 [MULTI_TEXT n=2 columns=A,B]: A407='دوره ۶ ماهه منتهي به ۱۴۰۳/۱۲/۳۰ ' | B407='--------------------------------
------------------------------------ '
    MERGES B407:E407
  row 408 [EMPTY]
  row 409 [SINGLE_TEXT n=1 columns=A]: A409='سایر توضیحات با اهمیت'
  row 410 [SINGLE_TEXT n=1 columns=A]: A410='--------------------------------------------------------------------...
    MERGES A410:I410
  row 411 [SINGLE_TEXT n=1 columns=A]: A411='«جملات آينده\u200cنگر نشان\u200cدهنده انتظارات، باورها يا پيش\u200cب...
    MERGES A411:I411
  row 412 [EMPTY]
  row 413 [EMPTY]

SUMMARY bands_printed=29 compound_candidates=3

### SHEET 2 Sheet1 | used=A1:E24 | bands=1

[BAND 1] rows=16:17 columns=A,B,C,D,E merges=A16:A17,E16:E17
  SIGNATURE=NO_MATCH
  PRIOR prior_body=None; gap=none
  FOLLOWING next_body=18; gap=none
  row 10 [SINGLE_TEXT n=1 columns=A]: A10='فعاليت\u200cهاي تأمين مالي '
  row 11 [SINGLE_TEXT n=1 columns=A]: A11='سپرده های ریالی: '
  row 12 [SINGLE_TEXT n=1 columns=A]: A12='درآمد تسهیلات اعطایی: '
  row 13 [EMPTY]
  row 14 [SINGLE_TEXT n=1 columns=A]: A14='صورت سود و زیان جامع'
  row 15 [SINGLE_TEXT n=1 columns=A]: A15='کلیه مبالغ درج شده به میلیون ریال می باشد'
  row 16 [MULTI_TEXT n=5 columns=A,B,C,D,E]: A16='شرح' | B16='دوره منتهي به ۱۴۰۳/۰۶/۳۱' | C16='تجدید ارائه شده ۱۴۰۲/۰۶/۳
۱' | D16='تجدید ارائه شده ۱۴۰۲/۱۲/۲۹' | E16='درصد تغییر'
    MERGES A16:A17,E16:E17
  row 17 [MULTI_TEXT n=3 columns=B,C,D]: B17='حسابرسی نشده' | C17='حسابرسی شده' | D17='حسابرسی شده'
    MERGES A16:A17,E16:E17
  row 18 [MIXED_NUMERIC n=5 columns=A,B,C,D,E]: A18='سود(زیان) خالص ' | B18=-25195703 | C18=-35246257 | D18=-9124895 | E
18=29
  row 19 [SINGLE_TEXT n=1 columns=A]: A19='سایر اقلام سود و زیان جامع: '
  row 20 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A20='مازاد تجديد ارزيابي دارايي\u200cها ' | B20=0 | C20=0 | D20=0
  row 21 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A21='تفاوت تسعیر ارز عملیات خارجی ' | B21=0 | C21=0 | D21=0
  row 22 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A22='مالیات مربوط به سایر اقلام سود و زیان جامع ' | B22=0 | C22=0 | D22=0
  row 23 [MIXED_NUMERIC n=4 columns=A,B,C,D]: A23='سایر اقلام سود و زیان جامع سال پس از کسر مالیات ' | B23=0 | C23=0 | D
23=0

SUMMARY bands_printed=1 compound_candidates=0
PS D:\Winprojects\analyzer>
(analyzer) Stop-Transcript
**********************
Windows PowerShell transcript end
End time: 20261116125640
**********************
