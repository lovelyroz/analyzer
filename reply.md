(analyzer) PS D:\winprojects\analyzer> cd D:\winprojects\analyzer
(analyzer) PS D:\winprojects\analyzer>
(analyzer) PS D:\winprojects\analyzer> @'
>> from pathlib import Path
>> from collections import Counter
>> from src.ingestion.codal.pdf_extract import extract_cell_rows
>>
>> pdf_path = Path("pdf/Fzar.pdf")
>> rows = extract_cell_rows(pdf_path)
>>
>> print("=" * 80)
>> print("TOTAL EXTRACTED ROWS:", len(rows))
>> print("ROWS PER PAGE:", dict(Counter(r.page for r in rows)))
>> print("=" * 80)
>>
>> for i, row in enumerate(rows, start=1):
>>     print(
>>         f"{i:03d} | "
>>         f"PAGE={row.page} | "
>>         f"ROW={row.source_row} | "
>>         f"COL={row.source_column!r} | "
>>         f"NAME={row.item_name!r} | "
>>         f"VALUE={row.value_text!r} | "
>>         f"SECTION={row.source_section!r}"
>>     )
>> '@ | & .\Scripts\python.exe -
================================================================================
TOTAL EXTRACTED ROWS: 77
ROWS PER PAGE: {1: 20, 2: 25, 3: 32}
================================================================================
001 | PAGE=1 | ROW=2 | COL='1' | NAME='ﺷﺮﮐﺖ:ﭘﻮﻳﺎ زرﮐﺎن آق درهﺳﺮﻣﺎﯾﻪ ﺛﺒﺖ ﺷﺪه' | VALUE='5,400,000' | SECTION='page_1'
002 | PAGE=1 | ROW=3 | COL='1' | NAME='ﻧﻤﺎدﻓﺰرﺳﺮﻣﺎﯾﻪ ﺛﺒﺖ ﻧﺸﺪه' | VALUE='0' | SECTION='page_1'
003 | PAGE=1 | ROW=4 | COL='1' | NAME='در ﺗﺎرﯾﺦ ﻣﻨﺘﮫﯽ ﺑﻪ  ﻣﺎھﻪ1 ﮔﺰارش ﻓﻌﺎﻟﯿﺖ ﻣﺎھﺎﻧﻪ' | VALUE='07' | SECTION='page_1'
004 | PAGE=1 | ROW=4 | COL='2' | NAME='در ﺗﺎرﯾﺦ ﻣﻨﺘﮫﯽ ﺑﻪ  ﻣﺎھﻪ1 ﮔﺰارش ﻓﻌﺎﻟﯿﺖ ﻣﺎھﺎﻧﻪ' | VALUE='30' | SECTION='page_1'
005 | PAGE=1 | ROW=5 | COL='1' | NAME='وﺿﻌﯿﺖ ﻧﺎﺷﺮﭘﺬﻳﺮﻓﺘﻪ ﺷﺪه در ﻓﺮاﺑﻮرس اﻳﺮان' | VALUE='1405' | SECTION='page_1'
006 | PAGE=1 | ROW=5 | COL='2' | NAME='وﺿﻌﯿﺖ ﻧﺎﺷﺮﭘﺬﻳﺮﻓﺘﻪ ﺷﺪه در ﻓﺮاﺑﻮرس اﻳﺮان' | VALUE='09' | SECTION='page_1'
007 | PAGE=1 | ROW=5 | COL='3' | NAME='وﺿﻌﯿﺖ ﻧﺎﺷﺮﭘﺬﻳﺮﻓﺘﻪ ﺷﺪه در ﻓﺮاﺑﻮرس اﻳﺮان' | VALUE='30' | SECTION='page_1'
008 | PAGE=1 | ROW=8 | COL='1' | NAME='/۵٠۴١از اﺑﺘﺪای ﺳﺎل ﻣﺎﻟﯽ ﺗﺎ ﺗﺎرﯾﺦ' | VALUE='۶٠' | SECTION='page_1'
009 | PAGE=1 | ROW=8 | COL='2' | NAME='/۵٠۴١از اﺑﺘﺪای ﺳﺎل ﻣﺎﻟﯽ ﺗﺎ ﺗﺎرﯾﺦ' | VALUE='۶٠' | SECTION='page_1'
010 | PAGE=1 | ROW=10 | COL='1' | NAME='/۴٠۴١از اﺑﺘﺪای ﺳﺎل ﻣﺎﻟﯽ ﺗﺎ ﺗﺎرﯾﺦ وﺿﻌﯿﺖ' | VALUE='٠٣' | SECTION='page_1'
011 | PAGE=1 | ROW=10 | COL='2' | NAME='/۴٠۴١از اﺑﺘﺪای ﺳﺎل ﻣﺎﻟﯽ ﺗﺎ ﺗﺎرﯾﺦ وﺿﻌﯿﺖ' | VALUE='٧٠' | SECTION='page_1'
012 | PAGE=1 | ROW=10 | COL='3' | NAME='/۴٠۴١از اﺑﺘﺪای ﺳﺎل ﻣﺎﻟﯽ ﺗﺎ ﺗﺎرﯾﺦ وﺿﻌﯿﺖ' | VALUE='٠٣' | SECTION='page_1'
013 | PAGE=1 | ROW=10 | COL='4' | NAME='/۴٠۴١از اﺑﺘﺪای ﺳﺎل ﻣﺎﻟﯽ ﺗﺎ ﺗﺎرﯾﺦ وﺿﻌﯿﺖ' | VALUE='٧٠' | SECTION='page_1'
014 | PAGE=1 | ROW=10 | COL='5' | NAME='/۴٠۴١از اﺑﺘﺪای ﺳﺎل ﻣﺎﻟﯽ ﺗﺎ ﺗﺎرﯾﺦ وﺿﻌﯿﺖ' | VALUE='٠٣' | SECTION='page_1'
015 | PAGE=1 | ROW=10 | COL='6' | NAME='/۴٠۴١از اﺑﺘﺪای ﺳﺎل ﻣﺎﻟﯽ ﺗﺎ ﺗﺎرﯾﺦ وﺿﻌﯿﺖ' | VALUE='٧٠' | SECTION='page_1'
016 | PAGE=1 | ROW=74 | COL='1' | NAME=',۴٠١ﺗﻮﻟﯿﺪ' | VALUE='٠٨۴١,٢٠٩١,۴۵٧,٧١۶٣١,٨٣٠٠٠٠٨۴١,٢٠٩١,۴۵٧,٧١۶٣١,٨٣٠٠٠٠٠٨۴١,٢٠٩١,۴۵٧,٧١۶٣١,٨٣٨٠.۶١٩,٠٢١۵.٨٢٣,١١٧٣۵,٨٠٢,٩٩١٣' | SECTION='page_1'
017 | PAGE=1 | ROW=86 | COL='1' | NAME=',٢ﺗﻮﻟﯿﺪ' | VALUE='٢٢٠,۴۶٣٠۴٠,٣٠۶,٩١٢۵٩,۵٣١,٧٠٠٠٠٣٧.٢٢٠,۴۶٣٠۴٠,٣٠۶,٩١٢۵٩,۵٣١,٧٠۵٢.۵٣٢,۵٩٠٠٢,٣۵٨,۵٢۶٣١,٢۶۴,٢٠٨٩.٧۵٢,٩۵۴١٢١,٩٩٨,٠٢٨٨٠,٨٩۵,٩٠٢۶.٢٩۴,٣٧٣۵۵٨,٠۴٨,۶٩٠٠,۵۵۵' | SECTION='page_1'
018 | PAGE=1 | ROW=92 | COL='1' | NAME=',۴١ﺗﻮﻟﯿﺪ' | VALUE='١٧٨.۴١٩,١۵۶۵,۴۵٨,۶٢٣٢۴,١۵٠٠٠٣٣٣,١٧٨.۴١٩,١۵۶۵,۴۵٨,۶٢٣٢۴,١۵۵۵٩۶٣.۶٠۵۴٩۴,٠۵٢,١٣۴٢٨,۵١٨٨٢,٢٣٢.١٢۴,٢٠٠٩,٣٧٧,٧٢٧۴٢,٧۶٧۴.۵۴۴,٣۵٢.۴٢۶,۴٨١۵,٧٢٠,٣٠٠٠' | SECTION='page_1'
019 | PAGE=1 | ROW=100 | COL='1' | NAME='ﺗﻦ٠٠٠٠٠٠٠٠٠٠٠٠٠٠٠٠٠٠٠٠,' | VALUE='۵١۵١٢.١٣۶,۵٧۴٨٩٧,٢٢٧,٧٢٨٢٨,۵٨١' | SECTION='page_1'
020 | PAGE=1 | ROW=108 | COL='1' | NAME=',٢٠١٠٠٠ﺗﻮﻟﯿﺪ' | VALUE='٠٠۵١١.٢١٩,٨٨٢۶١٩,۶٣٨,٢۶۶۴٣,۴۵١,٨١٠٠٠٠٠٠,٠٠۵١١.٢١٩,٨٨٢۶١٩,۶٣٨,٢۶۶۴٣,۴۵١,٨١٠٠۵,٠١١۶٠.١١٧,٢۴٨٩١,١٧٩,۵٨١٢٩,١٧۶,٣٠٠۵,٠١۶٧١.٣٢۶,١٣٣٢٧۴,۶١٨,۵۶٧۶٢,۶٢٨,١٢٠٠٠' | SECTION='page_1'
021 | PAGE=2 | ROW=1 | COL='1' | NAME='/۵٠۴١از اﺑﺘﺪای ﺳﺎل ﻣﺎﻟﯽ ﺗﺎ ﺗﺎرﯾﺦ' | VALUE='۶٠' | SECTION='page_2'
022 | PAGE=2 | ROW=1 | COL='2' | NAME='/۵٠۴١از اﺑﺘﺪای ﺳﺎل ﻣﺎﻟﯽ ﺗﺎ ﺗﺎرﯾﺦ' | VALUE='۶٠' | SECTION='page_2'
023 | PAGE=2 | ROW=3 | COL='1' | NAME='/۴٠۴١از اﺑﺘﺪای ﺳﺎل ﻣﺎﻟﯽ ﺗﺎ ﺗﺎرﯾﺦ وﺿﻌﯿﺖ' | VALUE='٠٣' | SECTION='page_2'
024 | PAGE=2 | ROW=3 | COL='2' | NAME='/۴٠۴١از اﺑﺘﺪای ﺳﺎل ﻣﺎﻟﯽ ﺗﺎ ﺗﺎرﯾﺦ وﺿﻌﯿﺖ' | VALUE='٧٠' | SECTION='page_2'
025 | PAGE=2 | ROW=3 | COL='3' | NAME='/۴٠۴١از اﺑﺘﺪای ﺳﺎل ﻣﺎﻟﯽ ﺗﺎ ﺗﺎرﯾﺦ وﺿﻌﯿﺖ' | VALUE='٠٣' | SECTION='page_2'
026 | PAGE=2 | ROW=3 | COL='4' | NAME='/۴٠۴١از اﺑﺘﺪای ﺳﺎل ﻣﺎﻟﯽ ﺗﺎ ﺗﺎرﯾﺦ وﺿﻌﯿﺖ' | VALUE='٧٠' | SECTION='page_2'
027 | PAGE=2 | ROW=3 | COL='5' | NAME='/۴٠۴١از اﺑﺘﺪای ﺳﺎل ﻣﺎﻟﯽ ﺗﺎ ﺗﺎرﯾﺦ وﺿﻌﯿﺖ' | VALUE='٠٣' | SECTION='page_2'
028 | PAGE=2 | ROW=3 | COL='6' | NAME='/۴٠۴١از اﺑﺘﺪای ﺳﺎل ﻣﺎﻟﯽ ﺗﺎ ﺗﺎرﯾﺦ وﺿﻌﯿﺖ' | VALUE='٧٠' | SECTION='page_2'
029 | PAGE=2 | ROW=60 | COL='1' | NAME='/٣ﻋﯿﺎر' | VALUE='٧' | SECTION='page_2'
030 | PAGE=2 | ROW=63 | COL='1' | NAME='ﺗﻦ٠٠٠٠٠٠٠٠٠٠٠۵١٨,' | VALUE='٩١٠٠٠۵١٨' | SECTION='page_2'
031 | PAGE=2 | ROW=89 | COL='1' | NAME='ﺟﻤﻊ٧۵٨,' | VALUE='٩٧٣,۵٢٠٧۵٨,٩٧٣,۵٢١٨٨,٩۴١,۶٨٣٧,٩٢۵,١٣۶۵١,٩۵٨,۵١' | SECTION='page_2'
032 | PAGE=2 | ROW=93 | COL='1' | NAME='/۵٠۴١ازاﺑﺘﺪای ﺳﺎل ﻣﺎﻟﯽ ﺗﺎ ﺗﺎرﯾﺦ' | VALUE='۶٠' | SECTION='page_2'
033 | PAGE=2 | ROW=125 | COL='1' | NAME=')اﺻﻼح ﺷﺪه(' | VALUE='١٣' | SECTION='page_2'
034 | PAGE=2 | ROW=125 | COL='2' | NAME=')اﺻﻼح ﺷﺪه(' | VALUE='۶٠' | SECTION='page_2'
035 | PAGE=2 | ROW=125 | COL='3' | NAME=')اﺻﻼح ﺷﺪه(' | VALUE='۵٠۴١' | SECTION='page_2'
036 | PAGE=2 | ROW=131 | COL='1' | NAME='/۴٠۴١ﺗﺎرﯾﺦ' | VALUE='٠٣' | SECTION='page_2'
037 | PAGE=2 | ROW=131 | COL='2' | NAME='/۴٠۴١ﺗﺎرﯾﺦ' | VALUE='٧٠' | SECTION='page_2'
038 | PAGE=2 | ROW=133 | COL='1' | NAME='/۵٠۴١ﻣﺎﻟﯽ' | VALUE='٠٣' | SECTION='page_2'
039 | PAGE=2 | ROW=133 | COL='2' | NAME='/۵٠۴١ﻣﺎﻟﯽ' | VALUE='٩٠' | SECTION='page_2'
040 | PAGE=2 | ROW=138 | COL='1' | NAME='ﻧﺮخ - رﯾﺎلﻣﺒﻠﻎ' | VALUE='-' | SECTION='page_2'
041 | PAGE=2 | ROW=142 | COL='1' | NAME='ﻧﺮخ' | VALUE='-' | SECTION='page_2'
042 | PAGE=2 | ROW=144 | COL='1' | NAME='ﻣﺒﻠﻎ' | VALUE='-' | SECTION='page_2'
043 | PAGE=2 | ROW=152 | COL='1' | NAME='ﻧﺮخ - رﯾﺎلﻣﺒﻠﻎ' | VALUE='-' | SECTION='page_2'
044 | PAGE=2 | ROW=156 | COL='1' | NAME='ﻧﺮخ - رﯾﺎلﻣﺒﻠﻎ' | VALUE='-' | SECTION='page_2'
045 | PAGE=2 | ROW=164 | COL='1' | NAME='ﻣﺘﺮﻣﮑﻌﺐ۴۵٣,' | VALUE='٢٠٧۴,١١٧٢٠٠٠۴۵٣,٢٠٧۴,١١٧٢٠٠٠۴۵٣,٢٠٧۴,١١٧٢١۶٧,٢۴٨٩,٣١١۶۴٠,١' | SECTION='page_2'
046 | PAGE=3 | ROW=10 | COL='1' | NAME=')اﺻﻼح ﺷﺪه(' | VALUE='١٣' | SECTION='page_3'
047 | PAGE=3 | ROW=10 | COL='2' | NAME=')اﺻﻼح ﺷﺪه(' | VALUE='۶٠' | SECTION='page_3'
048 | PAGE=3 | ROW=10 | COL='3' | NAME=')اﺻﻼح ﺷﺪه(' | VALUE='۵٠۴١' | SECTION='page_3'
049 | PAGE=3 | ROW=16 | COL='1' | NAME='/۴٠۴١ﺗﺎرﯾﺦ' | VALUE='٠٣' | SECTION='page_3'
050 | PAGE=3 | ROW=16 | COL='2' | NAME='/۴٠۴١ﺗﺎرﯾﺦ' | VALUE='٧٠' | SECTION='page_3'
051 | PAGE=3 | ROW=18 | COL='1' | NAME='/۵٠۴١ﻣﺎﻟﯽ' | VALUE='٠٣' | SECTION='page_3'
052 | PAGE=3 | ROW=18 | COL='2' | NAME='/۵٠۴١ﻣﺎﻟﯽ' | VALUE='٩٠' | SECTION='page_3'
053 | PAGE=3 | ROW=23 | COL='1' | NAME='ﻧﺮخ - رﯾﺎلﻣﺒﻠﻎ' | VALUE='-' | SECTION='page_3'
054 | PAGE=3 | ROW=27 | COL='1' | NAME='ﻧﺮخ' | VALUE='-' | SECTION='page_3'
055 | PAGE=3 | ROW=29 | COL='1' | NAME='ﻣﺒﻠﻎ' | VALUE='-' | SECTION='page_3'
056 | PAGE=3 | ROW=37 | COL='1' | NAME='ﻧﺮخ - رﯾﺎلﻣﺒﻠﻎ' | VALUE='-' | SECTION='page_3'
057 | PAGE=3 | ROW=41 | COL='1' | NAME='ﻧﺮخ - رﯾﺎلﻣﺒﻠﻎ' | VALUE='-' | SECTION='page_3'
058 | PAGE=3 | ROW=50 | COL='1' | NAME='ﺟﻤﻊ ﮐﻞ٨٠٠,' | VALUE='٧٠٨٠٠,٧٣۶٩١٧٩,٧' | SECTION='page_3'
059 | PAGE=3 | ROW=56 | COL='1' | NAME='/۵٠۴١از اﺑﺘﺪای ﺳﺎل ﻣﺎﻟﯽ ﺗﺎ ﺗﺎرﯾﺦ' | VALUE='۶٠' | SECTION='page_3'
060 | PAGE=3 | ROW=58 | COL='1' | NAME='/۵٠۴١دوره ﯾﮑﻤﺎھﻪ از اﺑﺘﺪای ﺳﺎل ﻣﺎﻟﯽ ﺗﺎ ﺗﺎرﯾﺦ' | VALUE='٠٣' | SECTION='page_3'
061 | PAGE=3 | ROW=58 | COL='2' | NAME='/۵٠۴١دوره ﯾﮑﻤﺎھﻪ از اﺑﺘﺪای ﺳﺎل ﻣﺎﻟﯽ ﺗﺎ ﺗﺎرﯾﺦ' | VALUE='٧٠' | SECTION='page_3'
062 | PAGE=3 | ROW=116 | COL='1' | NAME='ﻣﺎھﻪ ﻣﻨﺘﮫﯽ ﺑﻪ ١ﮐﺎدر ﺗﻮﺿﯿﺤﯽ ﻣﺮﺑﻮط ﺑﻪ اطﻼﻋﺎت دوره' | VALUE='٠٣' | SECTION='page_3'
063 | PAGE=3 | ROW=116 | COL='2' | NAME='ﻣﺎھﻪ ﻣﻨﺘﮫﯽ ﺑﻪ ١ﮐﺎدر ﺗﻮﺿﯿﺤﯽ ﻣﺮﺑﻮط ﺑﻪ اطﻼﻋﺎت دوره' | VALUE='٧٠' | SECTION='page_3'
064 | PAGE=3 | ROW=116 | COL='3' | NAME='ﻣﺎھﻪ ﻣﻨﺘﮫﯽ ﺑﻪ ١ﮐﺎدر ﺗﻮﺿﯿﺤﯽ ﻣﺮﺑﻮط ﺑﻪ اطﻼﻋﺎت دوره' | VALUE='۵٠۴١' | SECTION='page_3'
065 | PAGE=3 | ROW=117 | COL='1' | NAME='ھﯿﭽﮕﻮﻧﻪ ﻓﺮوش ﺷﻤﺶ طﻼ و ارز ﺑﻪ ﻣﻨﻈﻮر رﻓﻊ ﺗﻌﮫﺪ ارزی ﺻﺎدرات۵٠۴١-ﺷﺮﮐﺖ اﺳﺘﺤﺼﺎل ﻣﻮاد ﻣﻌﺪﻧﯽ ﺗﺨﺖ ﺳﻠﯿﻤﺎن )ﺷﺮﮐﺖ ﺗﺎﺑﻌﻪ( در ﻣﮫﺮ ﻣﺎه' | VALUE='٢' | SECTION='page_3'
066 | PAGE=3 | ROW=117 | COL='2' | NAME='ھﯿﭽﮕﻮﻧﻪ ﻓﺮوش ﺷﻤﺶ طﻼ و ارز ﺑﻪ ﻣﻨﻈﻮر رﻓﻊ ﺗﻌﮫﺪ ارزی ﺻﺎدرات۵٠۴١-ﺷﺮﮐﺖ اﺳﺘﺤﺼﺎل ﻣﻮاد ﻣﻌﺪﻧﯽ ﺗﺨﺖ ﺳﻠﯿﻤﺎن )ﺷﺮﮐﺖ ﺗﺎﺑﻌﻪ( در ﻣﮫﺮ ﻣﺎه' | VALUE='٩۵٧٣' | SECTION='page_3'
067 | PAGE=3 | ROW=117 | COL='3' | NAME='ھﯿﭽﮕﻮﻧﻪ ﻓﺮوش ﺷﻤﺶ طﻼ و ارز ﺑﻪ ﻣﻨﻈﻮر رﻓﻊ ﺗﻌﮫﺪ ارزی ﺻﺎدرات۵٠۴١-ﺷﺮﮐﺖ اﺳﺘﺤﺼﺎل ﻣﻮاد ﻣﻌﺪﻧﯽ ﺗﺨﺖ ﺳﻠﯿﻤﺎن )ﺷﺮﮐﺖ ﺗﺎﺑﻌﻪ( در ﻣﮫﺮ ﻣﺎه' | VALUE='٠' | SECTION='page_3'
068 | PAGE=3 | ROW=117 | COL='4' | NAME='ھﯿﭽﮕﻮﻧﻪ ﻓﺮوش ﺷﻤﺶ طﻼ و ارز ﺑﻪ ﻣﻨﻈﻮر رﻓﻊ ﺗﻌﮫﺪ ارزی ﺻﺎدرات۵٠۴١-ﺷﺮﮐﺖ اﺳﺘﺤﺼﺎل ﻣﻮاد ﻣﻌﺪﻧﯽ ﺗﺨﺖ ﺳﻠﯿﻤﺎن )ﺷﺮﮐﺖ ﺗﺎﺑﻌﻪ( در ﻣﮫﺮ ﻣﺎه' | VALUE='١' | SECTION='page_3'
069 | PAGE=3 | ROW=119 | COL='1' | NAME='/۵٠۴١ﮐﺎدر ﺗﻮﺿﯿﺤﯽ ﻣﺮﺑﻮط اطﻼﻋﺎت ﺗﺠﻤﻌﯽ از اﺑﺘﺪای ﺳﺎل ﺗﺎ ﭘﺎﯾﺎن ﻣﻮرخ' | VALUE='٠٣' | SECTION='page_3'
070 | PAGE=3 | ROW=119 | COL='2' | NAME='/۵٠۴١ﮐﺎدر ﺗﻮﺿﯿﺤﯽ ﻣﺮﺑﻮط اطﻼﻋﺎت ﺗﺠﻤﻌﯽ از اﺑﺘﺪای ﺳﺎل ﺗﺎ ﭘﺎﯾﺎن ﻣﻮرخ' | VALUE='٧٠' | SECTION='page_3'
071 | PAGE=3 | ROW=120 | COL='1' | NAME='ﻣﺠﻤﻮع ﻓﺮوش ﺷﻤﺶ طﻼ در ﺷﺮﮐﺖ اﺳﺘﺤﺼﺎل ﻣﻮاد ﻣﻌﺪﻧﯽ ﺗﺨﺖ ﺳﻠﯿﻤﺎن )ﺷﺮﮐﺖ ﺗﺎﺑﻌﻪ( ﺗﺎ ﭘﺎﯾﺎن ﻣﮫﺮ ﻣﺎه' | VALUE='۴٢٣.۵۴' | SECTION='page_3'
072 | PAGE=3 | ROW=120 | COL='2' | NAME='ﻣﺠﻤﻮع ﻓﺮوش ﺷﻤﺶ طﻼ در ﺷﺮﮐﺖ اﺳﺘﺤﺼﺎل ﻣﻮاد ﻣﻌﺪﻧﯽ ﺗﺨﺖ ﺳﻠﯿﻤﺎن )ﺷﺮﮐﺖ ﺗﺎﺑﻌﻪ( ﺗﺎ ﭘﺎﯾﺎن ﻣﮫﺮ ﻣﺎه' | VALUE='۵٣٨.٩٢٧.٠٣' | SECTION='page_3'
073 | PAGE=3 | ROW=120 | COL='3' | NAME='ﻣﺠﻤﻮع ﻓﺮوش ﺷﻤﺶ طﻼ در ﺷﺮﮐﺖ اﺳﺘﺤﺼﺎل ﻣﻮاد ﻣﻌﺪﻧﯽ ﺗﺨﺖ ﺳﻠﯿﻤﺎن )ﺷﺮﮐﺖ ﺗﺎﺑﻌﻪ( ﺗﺎ ﭘﺎﯾﺎن ﻣﮫﺮ ﻣﺎه' | VALUE='٠٠١.٠٠۶.۵' | SECTION='page_3'
074 | PAGE=3 | ROW=120 | COL='4' | NAME='ﻣﺠﻤﻮع ﻓﺮوش ﺷﻤﺶ طﻼ در ﺷﺮﮐﺖ اﺳﺘﺤﺼﺎل ﻣﻮاد ﻣﻌﺪﻧﯽ ﺗﺨﺖ ﺳﻠﯿﻤﺎن )ﺷﺮﮐﺖ ﺗﺎﺑﻌﻪ( ﺗﺎ ﭘﺎﯾﺎن ﻣﮫﺮ ﻣﺎه' | VALUE='١۵٩.٨٨٢.٢٩' | SECTION='page_3'
075 | PAGE=3 | ROW=120 | COL='5' | NAME='ﻣﺠﻤﻮع ﻓﺮوش ﺷﻤﺶ طﻼ در ﺷﺮﮐﺖ اﺳﺘﺤﺼﺎل ﻣﻮاد ﻣﻌﺪﻧﯽ ﺗﺨﺖ ﺳﻠﯿﻤﺎن )ﺷﺮﮐﺖ ﺗﺎﺑﻌﻪ( ﺗﺎ ﭘﺎﯾﺎن ﻣﮫﺮ ﻣﺎه' | VALUE='۵٠۴١' | SECTION='page_3'
076 | PAGE=3 | ROW=120 | COL='6' | NAME='ﻣﺠﻤﻮع ﻓﺮوش ﺷﻤﺶ طﻼ در ﺷﺮﮐﺖ اﺳﺘﺤﺼﺎل ﻣﻮاد ﻣﻌﺪﻧﯽ ﺗﺨﺖ ﺳﻠﯿﻤﺎن )ﺷﺮﮐﺖ ﺗﺎﺑﻌﻪ( ﺗﺎ ﭘﺎﯾﺎن ﻣﮫﺮ ﻣﺎه' | VALUE='۴۶٣،٧۴' | SECTION='page_3'
077 | PAGE=3 | ROW=120 | COL='7' | NAME='ﻣﺠﻤﻮع ﻓﺮوش ﺷﻤﺶ طﻼ در ﺷﺮﮐﺖ اﺳﺘﺤﺼﺎل ﻣﻮاد ﻣﻌﺪﻧﯽ ﺗﺨﺖ ﺳﻠﯿﻤﺎن )ﺷﺮﮐﺖ ﺗﺎﺑﻌﻪ( ﺗﺎ ﭘﺎﯾﺎن ﻣﮫﺮ ﻣﺎه' | VALUE='۵٠۴١' | SECTION='page_3'