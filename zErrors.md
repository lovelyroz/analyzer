(analyzer) PS D:\winprojects\analyzer> python -m pytest src/tests/test_stage7_valuation.py -q

======================================================= ERRORS ========================================================
_________________________________ ERROR collecting src/tests/test_stage7_valuation.py _________________________________
src\tests\test_stage7_valuation.py:7: in <module>
    from src.valuation.engine import ValuationEngine
src\valuation\__init__.py:11: in <module>
    from src.valuation.engine import ValuationEngine
src\valuation\engine.py:44: in <module>
    class ValuationEngine:
src\valuation\engine.py:72: in ValuationEngine
    parameters: Optional[Union[ConsumedParameters, Any]] = None,
                                                   ^^^
E   NameError: name 'Any' is not defined
=============================================== short test summary info ===============================================
ERROR src/tests/test_stage7_valuation.py - NameError: name 'Any' is not defined
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
1 error in 0.83s
(analyzer) PS D:\winprojects\analyzer> python -m pytest src/tests/test_stage7_valuation.py src/tests/test_stage9_decision.py -q

======================================================= ERRORS ========================================================
_________________________________ ERROR collecting src/tests/test_stage7_valuation.py _________________________________
src\tests\test_stage7_valuation.py:7: in <module>
    from src.valuation.engine import ValuationEngine
src\valuation\__init__.py:11: in <module>
    from src.valuation.engine import ValuationEngine
src\valuation\engine.py:44: in <module>
    class ValuationEngine:
src\valuation\engine.py:72: in ValuationEngine
    parameters: Optional[Union[ConsumedParameters, Any]] = None,
                                                   ^^^
E   NameError: name 'Any' is not defined
_________________________________ ERROR collecting src/tests/test_stage9_decision.py __________________________________
src\tests\test_stage9_decision.py:9: in <module>
    from src.decision.engine import DecisionEngine
src\decision\__init__.py:8: in <module>
    from src.decision.service import ValuationDecisionResult, calculate_decision_as_of_jalali
src\decision\service.py:15: in <module>
    from src.valuation.service import calculate_valuation_as_of_jalali
src\valuation\__init__.py:11: in <module>
    from src.valuation.engine import ValuationEngine
src\valuation\engine.py:44: in <module>
    class ValuationEngine:
src\valuation\engine.py:72: in ValuationEngine
    parameters: Optional[Union[ConsumedParameters, Any]] = None,
                                                   ^^^
E   NameError: name 'Any' is not defined
=============================================== short test summary info ===============================================
ERROR src/tests/test_stage7_valuation.py - NameError: name 'Any' is not defined
ERROR src/tests/test_stage9_decision.py - NameError: name 'Any' is not defined
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Interrupted: 2 errors during collection !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
2 errors in 0.89s
(analyzer) PS D:\winprojects\analyzer> python -m pytest src/tests -q

======================================================= ERRORS ========================================================
_________________________________ ERROR collecting src/tests/test_stage7_valuation.py _________________________________
src\tests\test_stage7_valuation.py:7: in <module>
    from src.valuation.engine import ValuationEngine
src\valuation\__init__.py:11: in <module>
    from src.valuation.engine import ValuationEngine
src\valuation\engine.py:44: in <module>
    class ValuationEngine:
src\valuation\engine.py:72: in ValuationEngine
    parameters: Optional[Union[ConsumedParameters, Any]] = None,
                                                   ^^^
E   NameError: name 'Any' is not defined
_________________________________ ERROR collecting src/tests/test_stage9_decision.py __________________________________
src\tests\test_stage9_decision.py:9: in <module>
    from src.decision.engine import DecisionEngine
src\decision\__init__.py:8: in <module>
    from src.decision.service import ValuationDecisionResult, calculate_decision_as_of_jalali
src\decision\service.py:15: in <module>
    from src.valuation.service import calculate_valuation_as_of_jalali
src\valuation\__init__.py:11: in <module>
    from src.valuation.engine import ValuationEngine
src\valuation\engine.py:44: in <module>
    class ValuationEngine:
src\valuation\engine.py:72: in ValuationEngine
    parameters: Optional[Union[ConsumedParameters, Any]] = None,
                                                   ^^^
E   NameError: name 'Any' is not defined
=============================================== short test summary info ===============================================
ERROR src/tests/test_stage7_valuation.py - NameError: name 'Any' is not defined
ERROR src/tests/test_stage9_decision.py - NameError: name 'Any' is not defined
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Interrupted: 2 errors during collection !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
2 errors in 1.24s