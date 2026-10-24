(analyzer) PS D:\winprojects\analyzer> python -m pytest src/tests/test_stage7_valuation.py -q

======================================================= ERRORS ========================================================
___________________________________ ERROR collecting tests/test_stage7_valuation.py ___________________________________
Lib\site-packages\_pytest\python.py:508: in importtestmodule
    mod = import_path(
Lib\site-packages\_pytest\pathlib.py:596: in import_path
    importlib.import_module(module_name)
C:\Users\Papa\AppData\Local\Programs\Python\Python312\Lib\importlib\__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
<frozen importlib._bootstrap>:1387: in _gcd_import
    ???
<frozen importlib._bootstrap>:1360: in _find_and_load
    ???
<frozen importlib._bootstrap>:1331: in _find_and_load_unlocked
    ???
<frozen importlib._bootstrap>:935: in _load_unlocked
    ???
Lib\site-packages\_pytest\assertion\rewrite.py:179: in exec_module
    source_stat, co = _rewrite_test(fn, self.config)
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Lib\site-packages\_pytest\assertion\rewrite.py:348: in _rewrite_test
    tree = ast.parse(source, filename=strfn)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
C:\Users\Papa\AppData\Local\Programs\Python\Python312\Lib\ast.py:52: in parse
    return compile(source, filename, mode, flags,
E     File "D:\winprojects\analyzer\src\tests\test_stage7_valuation.py", line 10
E       GENESIS_PARAMETERS if "GENESIS_PARAMETERS" in globals() else None,
E                          ^^
E   SyntaxError: invalid syntax
=============================================== short test summary info ===============================================
ERROR src\tests\test_stage7_valuation.py
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
1 error in 0.43s
(analyzer) PS D:\winprojects\analyzer> python -m pytest src/tests/test_stage7_valuation.py src/tests/test_stage9_decision.py -q

======================================================= ERRORS ========================================================
___________________________________ ERROR collecting tests/test_stage7_valuation.py ___________________________________
Lib\site-packages\_pytest\python.py:508: in importtestmodule
    mod = import_path(
Lib\site-packages\_pytest\pathlib.py:596: in import_path
    importlib.import_module(module_name)
C:\Users\Papa\AppData\Local\Programs\Python\Python312\Lib\importlib\__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
<frozen importlib._bootstrap>:1387: in _gcd_import
    ???
<frozen importlib._bootstrap>:1360: in _find_and_load
    ???
<frozen importlib._bootstrap>:1331: in _find_and_load_unlocked
    ???
<frozen importlib._bootstrap>:935: in _load_unlocked
    ???
Lib\site-packages\_pytest\assertion\rewrite.py:179: in exec_module
    source_stat, co = _rewrite_test(fn, self.config)
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Lib\site-packages\_pytest\assertion\rewrite.py:348: in _rewrite_test
    tree = ast.parse(source, filename=strfn)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
C:\Users\Papa\AppData\Local\Programs\Python\Python312\Lib\ast.py:52: in parse
    return compile(source, filename, mode, flags,
E     File "D:\winprojects\analyzer\src\tests\test_stage7_valuation.py", line 10
E       GENESIS_PARAMETERS if "GENESIS_PARAMETERS" in globals() else None,
E                          ^^
E   SyntaxError: invalid syntax
=============================================== short test summary info ===============================================
ERROR src\tests\test_stage7_valuation.py
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
1 error in 0.91s
(analyzer) PS D:\winprojects\analyzer> python -m pytest src/tests -q

======================================================= ERRORS ========================================================
___________________________________ ERROR collecting tests/test_stage7_valuation.py ___________________________________
Lib\site-packages\_pytest\python.py:508: in importtestmodule
    mod = import_path(
Lib\site-packages\_pytest\pathlib.py:596: in import_path
    importlib.import_module(module_name)
C:\Users\Papa\AppData\Local\Programs\Python\Python312\Lib\importlib\__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
<frozen importlib._bootstrap>:1387: in _gcd_import
    ???
<frozen importlib._bootstrap>:1360: in _find_and_load
    ???
<frozen importlib._bootstrap>:1331: in _find_and_load_unlocked
    ???
<frozen importlib._bootstrap>:935: in _load_unlocked
    ???
Lib\site-packages\_pytest\assertion\rewrite.py:179: in exec_module
    source_stat, co = _rewrite_test(fn, self.config)
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Lib\site-packages\_pytest\assertion\rewrite.py:348: in _rewrite_test
    tree = ast.parse(source, filename=strfn)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
C:\Users\Papa\AppData\Local\Programs\Python\Python312\Lib\ast.py:52: in parse
    return compile(source, filename, mode, flags,
E     File "D:\winprojects\analyzer\src\tests\test_stage7_valuation.py", line 10
E       GENESIS_PARAMETERS if "GENESIS_PARAMETERS" in globals() else None,
E                          ^^
E   SyntaxError: invalid syntax
=============================================== short test summary info ===============================================
ERROR src\tests\test_stage7_valuation.py
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
1 error in 1.27s