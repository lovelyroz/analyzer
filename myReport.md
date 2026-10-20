# task 1 :
    "pytest.ini",
    "pyproject.toml",
    "setup.cfg",
    "tox.ini",
    "conftest.py"  
   result :  No such above files 


# task مرحله سوم: اگر هیچ تنظیماتی پیدا نشد :

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