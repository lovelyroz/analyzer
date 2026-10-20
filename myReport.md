# REPORT 1
## task 1 :
    "pytest.ini",
    "pyproject.toml",
    "setup.cfg",
    "tox.ini",
    "conftest.py"  
   result :  No such above files 


## task مرحله سوم: اگر هیچ تنظیماتی پیدا نشد :

.\.venv\Scripts\python.exe -m pytest --version
pytest 9.1.1

=================================================== short test summary info 
ERROR Lib/site-packages/colorama/tests/ansi_test.py
ERROR Lib/site-packages/colorama/tests/ansitowin32_test.py
ERROR Lib/site-packages/colorama/tests/initialise_test.py
ERROR Lib/site-packages/colorama/tests/isatty_test.py
ERROR Lib/site-packages/colorama/tests/winterm_test.py
ERROR Lib/site-packages/greenlet/tests/test_contextvars.py
ERROR Lib/site-packages/greenlet/tests/test_cpp.py
ERROR Lib/site-packages/greenlet/tests/test_extension_interface.py
ERROR Lib/site-packages/greenlet/tests/test_gc.py
ERROR Lib/site-packages/greenlet/tests/test_generator.py
ERROR Lib/site-packages/greenlet/tests/test_generator_nested.py
ERROR Lib/site-packages/greenlet/tests/test_greenlet.py
ERROR Lib/site-packages/greenlet/tests/test_greenlet_trash.py
ERROR Lib/site-packages/greenlet/tests/test_interpreter_shutdown.py
ERROR Lib/site-packages/greenlet/tests/test_leaks.py
ERROR Lib/site-packages/greenlet/tests/test_stack_saved.py
ERROR Lib/site-packages/greenlet/tests/test_throw.py
ERROR Lib/site-packages/greenlet/tests/test_tracing.py
ERROR Lib/site-packages/greenlet/tests/test_version.py
ERROR Lib/site-packages/greenlet/tests/test_weakref.py
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Interrupted: 20 errors during collection !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
========================================== 1054 tests collected, 20 errors in 4.88s 

# Report 2
## Get-Location
Path                   
----                   
D:\winprojects\analyzer

## Resolve-Path .\.venv\Scripts\python.exe

Path                                            
----                                            
D:\winprojects\analyzer\.venv\Scripts\python.exe
## Get-ChildItem -Force


    Directory: D:\winprojects\analyzer

# Report 3
## (analyzer) PS D:\winprojects\analyzer> Get-ChildItem -Force | Select-Object Mode, Name

Mode   Name                                                
----   ----                                                
d----- .claude                                             
d--h-- .git                                                
d----- .github                                             
d----- .pytest_cache                                       
d----- .venv                                               
d----- .venvــــ                                           
d----- Include                                             
d----- Lib                                                 
d----- pdf                                                 
d----- prompts                                             
d----- Scripts                                             
d----- src                                                 
d----- __pycache__                                         
-a---- .gitignore                                          
-a---- 00_Architecture_Freeze_Point.md                     
-a---- 00_a_Master_Architecture.md                         
-a---- 00_Standard_Development_Project_Template.md         
-a---- 01_Stage1_Data_Foundation.md                        
-a---- 02_Stage2_KPI_Specification.md                      
-a---- 03_Stage3_Fundamental_Scoring.md                    
-a---- 04_Stage4_Historical_Trend.md                       
-a---- 05_Stage5_Forecast_Engine.md                        
-a---- 06_Stage6_Forecast_Evaluation.md                    
-a---- 07_Stage7_Valuation.md                              
-a---- 08_Stage8_Market_Engine.md                          
-a---- 08_Stage8_Market_Engine_Contract_Amendment_V1.1.md  
-a---- 09_Stage9_Decision_Dashboard.md                     
-a---- 10_Production_Codal_Extraction_and_Data_Load.md     
-a---- 11_Database_Architecture_Stage1.md                  
-a---- 11_Production_Data_Load_and_Foundation_Validation.md
-a---- 12_Database_Architecture_V1.1.md                    
-a---- 99_Architecture_Change_Log.md                       
-a---- currentTestResults.md                               
-a---- debug_alerts.py                                     
-a---- newPrompt.md                                        
-a---- P35.md                                              
-a---- PROJECT_HANDOFF_INSTRUCTIONS.md                     
-a---- requirements.txt                                    
-a---- roadMap.md                                          
-a---- stage5prompt1-2report.md                            
-a---- Stage5prompts1to9.md                                
-a---- stage_6_prompts.md                                  
-a---- stage_7_prompts.md                                  
-a---- tehran_stock.db                                     
-a---- temp_report.md                                      
-a---- temp_report2.md                    
## (analyzer) PS D:\winprojects\analyzer> .\.venv\Scripts\python.exe -c "import sys, pytest; print('Python:', sys.executable); print('Pytest:', pytest.__file__)"
Python: D:\winprojects\analyzer\.venv\Scripts\python.exe
Pytest: D:\winprojects\analyzer\.venv\Lib\site-packages\pytest\__init__.py
## (analyzer) PS D:\winprojects\analyzer> .\.venv\Scripts\python.exe -m pytest --trace-config --collect-only -q 2>&1 | Select-String "rootdir:|configfile:|testpaths:|inifile:|site-packages|ERROR collecting"

PLUGIN registered: <module '_pytest.mark' from 
'D:\\winprojects\\analyzer\\.venv\\Lib\\site-packages\\_pytest\\mark\\__init__.py'>
PLUGIN registered: <module '_pytest.main' from 'D:\\winprojects\\analyzer\\.venv\\Lib\\site-packages\\_pytest\\main.py'>
PLUGIN registered: <module '_pytest.runner' from 'D:\\winprojects\\analyzer\\.venv\\Lib\\site-packages\\_pytest\\runner.py'>
PLUGIN registered: <module '_pytest.fixtures' from 
'D:\\winprojects\\analyzer\\.venv\\Lib\\site-packages\\_pytest\\fixtures.py'>
PLUGIN registered: <module '_pytest.helpconfig' from 
'D:\\winprojects\\analyzer\\.venv\\Lib\\site-packages\\_pytest\\helpconfig.py'>
PLUGIN registered: <module '_pytest.python' from 'D:\\winprojects\\analyzer\\.venv\\Lib\\site-packages\\_pytest\\python.py'>
PLUGIN registered: <module '_pytest.terminal' from 
'D:\\winprojects\\analyzer\\.venv\\Lib\\site-packages\\_pytest\\terminal.py'>
PLUGIN registered: <module '_pytest.debugging' from 
'D:\\winprojects\\analyzer\\.venv\\Lib\\site-packages\\_pytest\\debugging.py'>
PLUGIN registered: <module '_pytest.unittest' from 
'D:\\winprojects\\analyzer\\.venv\\Lib\\site-packages\\_pytest\\unittest.py'>
PLUGIN registered: <module '_pytest.capture' from 'D:\\winprojects\\analyzer\\.venv\\Lib\\site-packages\\_pytest\\capture.py'>
PLUGIN registered: <module '_pytest.skipping' from 
'D:\\winprojects\\analyzer\\.venv\\Lib\\site-packages\\_pytest\\skipping.py'>
PLUGIN registered: <module '_pytest.legacypath' from 
'D:\\winprojects\\analyzer\\.venv\\Lib\\site-packages\\_pytest\\legacypath.py'>
PLUGIN registered: <module '_pytest.tmpdir' from 'D:\\winprojects\\analyzer\\.venv\\Lib\\site-packages\\_pytest\\tmpdir.py'>
PLUGIN registered: <module '_pytest.monkeypatch' from 
'D:\\winprojects\\analyzer\\.venv\\Lib\\site-packages\\_pytest\\monkeypatch.py'>
PLUGIN registered: <module '_pytest.recwarn' from 'D:\\winprojects\\analyzer\\.venv\\Lib\\site-packages\\_pytest\\recwarn.py'>
PLUGIN registered: <module '_pytest.pastebin' from 
'D:\\winprojects\\analyzer\\.venv\\Lib\\site-packages\\_pytest\\pastebin.py'>
PLUGIN registered: <module '_pytest.assertion' from 
'D:\\winprojects\\analyzer\\.venv\\Lib\\site-packages\\_pytest\\assertion\\__init__.py'>
PLUGIN registered: <module '_pytest.junitxml' from 
'D:\\winprojects\\analyzer\\.venv\\Lib\\site-packages\\_pytest\\junitxml.py'>
PLUGIN registered: <module '_pytest.doctest' from 'D:\\winprojects\\analyzer\\.venv\\Lib\\site-packages\\_pytest\\doctest.py'>
PLUGIN registered: <module '_pytest.cacheprovider' from 
'D:\\winprojects\\analyzer\\.venv\\Lib\\site-packages\\_pytest\\cacheprovider.py'>
PLUGIN registered: <module '_pytest.setuponly' from 
'D:\\winprojects\\analyzer\\.venv\\Lib\\site-packages\\_pytest\\setuponly.py'>
PLUGIN registered: <module '_pytest.setupplan' from 
'D:\\winprojects\\analyzer\\.venv\\Lib\\site-packages\\_pytest\\setupplan.py'>
PLUGIN registered: <module '_pytest.stepwise' from 
'D:\\winprojects\\analyzer\\.venv\\Lib\\site-packages\\_pytest\\stepwise.py'>
PLUGIN registered: <module '_pytest.unraisableexception' from 
'D:\\winprojects\\analyzer\\.venv\\Lib\\site-packages\\_pytest\\unraisableexception.py'>
PLUGIN registered: <module '_pytest.threadexception' from 
'D:\\winprojects\\analyzer\\.venv\\Lib\\site-packages\\_pytest\\threadexception.py'>
PLUGIN registered: <module '_pytest.warnings' from 
'D:\\winprojects\\analyzer\\.venv\\Lib\\site-packages\\_pytest\\warnings.py'>
PLUGIN registered: <module '_pytest.logging' from 'D:\\winprojects\\analyzer\\.venv\\Lib\\site-packages\\_pytest\\logging.py'>
PLUGIN registered: <module '_pytest.reports' from 'D:\\winprojects\\analyzer\\.venv\\Lib\\site-packages\\_pytest\\reports.py'>
PLUGIN registered: <module '_pytest.faulthandler' from 
'D:\\winprojects\\analyzer\\.venv\\Lib\\site-packages\\_pytest\\faulthandler.py'>
PLUGIN registered: <module '_pytest.subtests' from 
'D:\\winprojects\\analyzer\\.venv\\Lib\\site-packages\\_pytest\\subtests.py'>
PLUGIN registered: <module '_pytest.terminalprogress' from 
'D:\\winprojects\\analyzer\\.venv\\Lib\\site-packages\\_pytest\\terminalprogress.py'>
_______ ERROR collecting Lib/site-packages/colorama/tests/ansi_test.py ________
  D:\winprojects\analyzer\.venv\Lib\site-packages\colorama\tests\ansi_test.py
  D:\winprojects\analyzer\Lib\site-packages\colorama\tests\ansi_test.py
____ ERROR collecting Lib/site-packages/colorama/tests/ansitowin32_test.py ____
  D:\winprojects\analyzer\.venv\Lib\site-packages\colorama\tests\ansitowin32_test.py
  D:\winprojects\analyzer\Lib\site-packages\colorama\tests\ansitowin32_test.py
____ ERROR collecting Lib/site-packages/colorama/tests/initialise_test.py _____
  D:\winprojects\analyzer\.venv\Lib\site-packages\colorama\tests\initialise_test.py
  D:\winprojects\analyzer\Lib\site-packages\colorama\tests\initialise_test.py
______ ERROR collecting Lib/site-packages/colorama/tests/isatty_test.py _______
  D:\winprojects\analyzer\.venv\Lib\site-packages\colorama\tests\isatty_test.py
  D:\winprojects\analyzer\Lib\site-packages\colorama\tests\isatty_test.py
______ ERROR collecting Lib/site-packages/colorama/tests/winterm_test.py ______
  D:\winprojects\analyzer\.venv\Lib\site-packages\colorama\tests\winterm_test.py
  D:\winprojects\analyzer\Lib\site-packages\colorama\tests\winterm_test.py
____ ERROR collecting Lib/site-packages/greenlet/tests/test_contextvars.py ____
ImportError while importing test module 'D:\winprojects\analyzer\Lib\site-packages\greenlet\tests\test_contextvars.py'.
Lib\site-packages\greenlet\tests\__init__.py:17: in <module>
________ ERROR collecting Lib/site-packages/greenlet/tests/test_cpp.py ________
ImportError while importing test module 'D:\winprojects\analyzer\Lib\site-packages\greenlet\tests\test_cpp.py'.
Lib\site-packages\greenlet\tests\__init__.py:17: in <module>
_ ERROR collecting Lib/site-packages/greenlet/tests/test_extension_interface.py _
ImportError while importing test module 'D:\winprojects\analyzer\Lib\site-packages\greenlet\tests\test_extension_interface.py'.
Lib\site-packages\greenlet\tests\__init__.py:17: in <module>
________ ERROR collecting Lib/site-packages/greenlet/tests/test_gc.py _________
ImportError while importing test module 'D:\winprojects\analyzer\Lib\site-packages\greenlet\tests\test_gc.py'.
Lib\site-packages\greenlet\tests\__init__.py:17: in <module>
_____ ERROR collecting Lib/site-packages/greenlet/tests/test_generator.py _____
ImportError while importing test module 'D:\winprojects\analyzer\Lib\site-packages\greenlet\tests\test_generator.py'.
Lib\site-packages\greenlet\tests\__init__.py:17: in <module>
_ ERROR collecting Lib/site-packages/greenlet/tests/test_generator_nested.py __
ImportError while importing test module 'D:\winprojects\analyzer\Lib\site-packages\greenlet\tests\test_generator_nested.py'.
Lib\site-packages\greenlet\tests\__init__.py:17: in <module>
_____ ERROR collecting Lib/site-packages/greenlet/tests/test_greenlet.py ______
ImportError while importing test module 'D:\winprojects\analyzer\Lib\site-packages\greenlet\tests\test_greenlet.py'.
Lib\site-packages\greenlet\tests\__init__.py:17: in <module>
__ ERROR collecting Lib/site-packages/greenlet/tests/test_greenlet_trash.py ___
ImportError while importing test module 'D:\winprojects\analyzer\Lib\site-packages\greenlet\tests\test_greenlet_trash.py'.
Lib\site-packages\greenlet\tests\__init__.py:17: in <module>
_ ERROR collecting Lib/site-packages/greenlet/tests/test_interpreter_shutdown.py _
ImportError while importing test module 
'D:\winprojects\analyzer\Lib\site-packages\greenlet\tests\test_interpreter_shutdown.py'.
Lib\site-packages\greenlet\tests\__init__.py:17: in <module>
_______ ERROR collecting Lib/site-packages/greenlet/tests/test_leaks.py _______
ImportError while importing test module 'D:\winprojects\analyzer\Lib\site-packages\greenlet\tests\test_leaks.py'.
Lib\site-packages\greenlet\tests\__init__.py:17: in <module>
____ ERROR collecting Lib/site-packages/greenlet/tests/test_stack_saved.py ____
ImportError while importing test module 'D:\winprojects\analyzer\Lib\site-packages\greenlet\tests\test_stack_saved.py'.
Lib\site-packages\greenlet\tests\__init__.py:17: in <module>
_______ ERROR collecting Lib/site-packages/greenlet/tests/test_throw.py _______
ImportError while importing test module 'D:\winprojects\analyzer\Lib\site-packages\greenlet\tests\test_throw.py'.
Lib\site-packages\greenlet\tests\__init__.py:17: in <module>
______ ERROR collecting Lib/site-packages/greenlet/tests/test_tracing.py ______
ImportError while importing test module 'D:\winprojects\analyzer\Lib\site-packages\greenlet\tests\test_tracing.py'.
Lib\site-packages\greenlet\tests\__init__.py:17: in <module>
______ ERROR collecting Lib/site-packages/greenlet/tests/test_version.py ______
ImportError while importing test module 'D:\winprojects\analyzer\Lib\site-packages\greenlet\tests\test_version.py'.
Lib\site-packages\greenlet\tests\__init__.py:17: in <module>
______ ERROR collecting Lib/site-packages/greenlet/tests/test_weakref.py ______
ImportError while importing test module 'D:\winprojects\analyzer\Lib\site-packages\greenlet\tests\test_weakref.py'.
Lib\site-packages\greenlet\tests\__init__.py:17: in <module>
ERROR Lib/site-packages/colorama/tests/ansi_test.py
ERROR Lib/site-packages/colorama/tests/ansitowin32_test.py
ERROR Lib/site-packages/colorama/tests/initialise_test.py
ERROR Lib/site-packages/colorama/tests/isatty_test.py
ERROR Lib/site-packages/colorama/tests/winterm_test.py
ERROR Lib/site-packages/greenlet/tests/test_contextvars.py
ERROR Lib/site-packages/greenlet/tests/test_cpp.py
ERROR Lib/site-packages/greenlet/tests/test_extension_interface.py
ERROR Lib/site-packages/greenlet/tests/test_gc.py
ERROR Lib/site-packages/greenlet/tests/test_generator.py
ERROR Lib/site-packages/greenlet/tests/test_generator_nested.py
ERROR Lib/site-packages/greenlet/tests/test_greenlet.py
ERROR Lib/site-packages/greenlet/tests/test_greenlet_trash.py
ERROR Lib/site-packages/greenlet/tests/test_interpreter_shutdown.py
ERROR Lib/site-packages/greenlet/tests/test_leaks.py
ERROR Lib/site-packages/greenlet/tests/test_stack_saved.py
ERROR Lib/site-packages/greenlet/tests/test_throw.py
ERROR Lib/site-packages/greenlet/tests/test_tracing.py
ERROR Lib/site-packages/greenlet/tests/test_version.py
ERROR Lib/site-packages/greenlet/tests/test_weakref.py