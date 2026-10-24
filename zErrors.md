(analyzer) PS D:\winprojects\analyzer> python -m pytest src/tests/test_stage7_valuation.py -q

======================================================= ERRORS ========================================================
_________________________________ ERROR collecting src/tests/test_stage7_valuation.py _________________________________
ImportError while importing test module 'D:\winprojects\analyzer\src\tests\test_stage7_valuation.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
C:\Users\Papa\AppData\Local\Programs\Python\Python312\Lib\importlib\__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\tests\test_stage7_valuation.py:9: in <module>
    from src.valuation.parameters import (
src\valuation\__init__.py:4: in <module>
    from src.valuation.parameters import SCENARIO_WEIGHTS, SCENARIO_PE_MULTIPLIER, MIN_INDUSTRY_PEERS, MODEL_VERSION
E   ImportError: cannot import name 'SCENARIO_WEIGHTS' from 'src.valuation.parameters' (D:\winprojects\analyzer\src\valuation\parameters.py)
=============================================== short test summary info ===============================================
ERROR src/tests/test_stage7_valuation.py
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
1 error in 0.21s
(analyzer) PS D:\winprojects\analyzer> python -m pytest src/tests/test_stage7_valuation.py src/tests/test_stage9_decision.py -q

======================================================= ERRORS ========================================================
_________________________________ ERROR collecting src/tests/test_stage7_valuation.py _________________________________
ImportError while importing test module 'D:\winprojects\analyzer\src\tests\test_stage7_valuation.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
C:\Users\Papa\AppData\Local\Programs\Python\Python312\Lib\importlib\__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\tests\test_stage7_valuation.py:9: in <module>
    from src.valuation.parameters import (
src\valuation\__init__.py:4: in <module>
    from src.valuation.parameters import SCENARIO_WEIGHTS, SCENARIO_PE_MULTIPLIER, MIN_INDUSTRY_PEERS, MODEL_VERSION
E   ImportError: cannot import name 'SCENARIO_WEIGHTS' from 'src.valuation.parameters' (D:\winprojects\analyzer\src\valuation\parameters.py)
_________________________________ ERROR collecting src/tests/test_stage9_decision.py __________________________________
ImportError while importing test module 'D:\winprojects\analyzer\src\tests\test_stage9_decision.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
C:\Users\Papa\AppData\Local\Programs\Python\Python312\Lib\importlib\__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\tests\test_stage9_decision.py:9: in <module>
    from src.decision.engine import DecisionEngine
src\decision\__init__.py:8: in <module>
    from src.decision.service import ValuationDecisionResult, calculate_decision_as_of_jalali
src\decision\service.py:15: in <module>
    from src.valuation.service import calculate_valuation_as_of_jalali
src\valuation\__init__.py:4: in <module>
    from src.valuation.parameters import SCENARIO_WEIGHTS, SCENARIO_PE_MULTIPLIER, MIN_INDUSTRY_PEERS, MODEL_VERSION
E   ImportError: cannot import name 'SCENARIO_WEIGHTS' from 'src.valuation.parameters' (D:\winprojects\analyzer\src\valuation\parameters.py)
=============================================== short test summary info ===============================================
ERROR src/tests/test_stage7_valuation.py
ERROR src/tests/test_stage9_decision.py
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Interrupted: 2 errors during collection !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
2 errors in 0.85s
(analyzer) PS D:\winprojects\analyzer> python -m pytest src/tests -q

======================================================= ERRORS ========================================================
_________________________________ ERROR collecting src/tests/test_stage7_valuation.py _________________________________
ImportError while importing test module 'D:\winprojects\analyzer\src\tests\test_stage7_valuation.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
C:\Users\Papa\AppData\Local\Programs\Python\Python312\Lib\importlib\__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\tests\test_stage7_valuation.py:9: in <module>
    from src.valuation.parameters import (
src\valuation\__init__.py:4: in <module>
    from src.valuation.parameters import SCENARIO_WEIGHTS, SCENARIO_PE_MULTIPLIER, MIN_INDUSTRY_PEERS, MODEL_VERSION
E   ImportError: cannot import name 'SCENARIO_WEIGHTS' from 'src.valuation.parameters' (D:\winprojects\analyzer\src\valuation\parameters.py)
_________________________________ ERROR collecting src/tests/test_stage9_decision.py __________________________________
ImportError while importing test module 'D:\winprojects\analyzer\src\tests\test_stage9_decision.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
C:\Users\Papa\AppData\Local\Programs\Python\Python312\Lib\importlib\__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\tests\test_stage9_decision.py:9: in <module>
    from src.decision.engine import DecisionEngine
src\decision\__init__.py:8: in <module>
    from src.decision.service import ValuationDecisionResult, calculate_decision_as_of_jalali
src\decision\service.py:15: in <module>
    from src.valuation.service import calculate_valuation_as_of_jalali
src\valuation\__init__.py:4: in <module>
    from src.valuation.parameters import SCENARIO_WEIGHTS, SCENARIO_PE_MULTIPLIER, MIN_INDUSTRY_PEERS, MODEL_VERSION
E   ImportError: cannot import name 'SCENARIO_WEIGHTS' from 'src.valuation.parameters' (D:\winprojects\analyzer\src\valuation\parameters.py)
=============================================== short test summary info ===============================================
ERROR src/tests/test_stage7_valuation.py
ERROR src/tests/test_stage9_decision.py
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Interrupted: 2 errors during collection