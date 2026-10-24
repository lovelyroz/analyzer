(analyzer) PS D:\winprojects\analyzer> python -m pytest src/tests/test_stage7_valuation.py -q

======================================================= ERRORS ========================================================
_________________________________ ERROR collecting src/tests/test_stage7_valuation.py _________________________________
ImportError while importing test module 'D:\winprojects\analyzer\src\tests\test_stage7_valuation.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
C:\Users\Papa\AppData\Local\Programs\Python\Python312\Lib\importlib\__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\tests\test_stage7_valuation.py:8: in <module>
    from src.valuation.parameters import (
E   ImportError: cannot import name 'GENESIS_PARAMETERS' from 'src.valuation.parameters' (D:\winprojects\analyzer\src\valuation\parameters.py)
=============================================== short test summary info ===============================================
ERROR src/tests/test_stage7_valuation.py
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
1 error in 0.98s
(analyzer) PS D:\winprojects\analyzer> python -m pytest src/tests/test_stage7_valuation.py src/tests/test_stage9_decision.py -q

======================================================= ERRORS ========================================================
_________________________________ ERROR collecting src/tests/test_stage7_valuation.py _________________________________
ImportError while importing test module 'D:\winprojects\analyzer\src\tests\test_stage7_valuation.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
C:\Users\Papa\AppData\Local\Programs\Python\Python312\Lib\importlib\__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\tests\test_stage7_valuation.py:8: in <module>
    from src.valuation.parameters import (
E   ImportError: cannot import name 'GENESIS_PARAMETERS' from 'src.valuation.parameters' (D:\winprojects\analyzer\src\valuation\parameters.py)
=============================================== short test summary info ===============================================
ERROR src/tests/test_stage7_valuation.py
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
1 error in 0.80s
(analyzer) PS D:\winprojects\analyzer> python -m pytest src/tests -q

======================================================= ERRORS ========================================================
_________________________________ ERROR collecting src/tests/test_stage7_valuation.py _________________________________
ImportError while importing test module 'D:\winprojects\analyzer\src\tests\test_stage7_valuation.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
C:\Users\Papa\AppData\Local\Programs\Python\Python312\Lib\importlib\__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\tests\test_stage7_valuation.py:8: in <module>
    from src.valuation.parameters import (
E   ImportError: cannot import name 'GENESIS_PARAMETERS' from 'src.valuation.parameters' (D:\winprojects\analyzer\src\valuation\parameters.py)
=============================================== short test summary info ===============================================
ERROR src/tests/test_stage7_valuation.py
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
1 error in 2.08s