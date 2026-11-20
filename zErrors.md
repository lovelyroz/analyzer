(analyzer) PS D:\Winprojects\analyzer> .\.venv\Scripts\python.exe -m pytest -q --basetemp .pytest_task015_20261120 src/tests/test_canonical_ingestion_admission.py
.F......F.........                                                                                               [100%]
====================================================== FAILURES =======================================================
_________________________________ test_one_invalid_candidate_rejects_the_entire_batch _________________________________

    def test_one_invalid_candidate_rejects_the_entire_batch():
        valid = _candidate()
        invalid = replace(valid, metric_id="", metric_approval_ref="")
        with pytest.raises(AdmissionRejected) as exc:
            prepare_canonical_batch((valid, invalid), revision=_revision())
        assert AdmissionCode.IDENTITY_MISSING in _codes(exc)
>       assert AdmissionCode.APPROVAL_REFERENCE_MISSING in _codes(exc)
E       AssertionError: assert <AdmissionCode.APPROVAL_REFERENCE_MISSING: 'APPROVAL_REFERENCE_MISSING'> in {<AdmissionCode.IDENTITY_MISSING: 'IDENTITY_MISSING'>}
E        +  where <AdmissionCode.APPROVAL_REFERENCE_MISSING: 'APPROVAL_REFERENCE_MISSING'> = AdmissionCode.APPROVAL_REFERENCE_MISSING
E        +  and   {<AdmissionCode.IDENTITY_MISSING: 'IDENTITY_MISSING'>} = _codes(<ExceptionInfo AdmissionRejected('IDENTITY_MISSING') tblen=2>)

src\tests\test_canonical_ingestion_admission.py:162: AssertionError
________________ test_blank_observation_builds_candidate_only_through_explicit_approved_fallback_path _________________

    def test_blank_observation_builds_candidate_only_through_explicit_approved_fallback_path():
        observation, match, spec = _blank_observation_and_match()
        with pytest.raises(CandidateValidationError) as exc:
            build_candidate_submission(observation, match, coordinate="B2", spec=spec)
>       assert exc.value.code == "SOURCE_VALUE_MISSING"
E       AssertionError: assert 'STRUCTURE_NOT_APPROVED' == 'SOURCE_VALUE_MISSING'
E
E         - SOURCE_VALUE_MISSING
E         + STRUCTURE_NOT_APPROVED

src\tests\test_canonical_ingestion_admission.py:222: AssertionError
=============================================== short test summary info ===============================================
FAILED src/tests/test_canonical_ingestion_admission.py::test_one_invalid_candidate_rejects_the_entire_batch - AssertionError: assert <AdmissionCode.APPROVAL_REFERENCE_MISSING: 'APPROVAL_REFERENCE_MISSING'> in {<AdmissionCode....
FAILED src/tests/test_canonical_ingestion_admission.py::test_blank_observation_builds_candidate_only_through_explicit_approved_fallback_path - AssertionError: assert 'STRUCTURE_NOT_APPROVED' == 'SOURCE_VALUE_MISSING'
2 failed, 16 passed in 1.08s
(analyzer) PS D:\Winprojects\analyzer> .\.venv\Scripts\python.exe -m pytest -q --basetemp .pytest_task015_20261120 src/tests/test_canonical_ingestion_admission.py src/tests/test_excel_canonical_input.py
.F......F...........................                                                                             [100%]
====================================================== FAILURES =======================================================
_________________________________ test_one_invalid_candidate_rejects_the_entire_batch _________________________________

    def test_one_invalid_candidate_rejects_the_entire_batch():
        valid = _candidate()
        invalid = replace(valid, metric_id="", metric_approval_ref="")
        with pytest.raises(AdmissionRejected) as exc:
            prepare_canonical_batch((valid, invalid), revision=_revision())
        assert AdmissionCode.IDENTITY_MISSING in _codes(exc)
>       assert AdmissionCode.APPROVAL_REFERENCE_MISSING in _codes(exc)
E       AssertionError: assert <AdmissionCode.APPROVAL_REFERENCE_MISSING: 'APPROVAL_REFERENCE_MISSING'> in {<AdmissionCode.IDENTITY_MISSING: 'IDENTITY_MISSING'>}
E        +  where <AdmissionCode.APPROVAL_REFERENCE_MISSING: 'APPROVAL_REFERENCE_MISSING'> = AdmissionCode.APPROVAL_REFERENCE_MISSING
E        +  and   {<AdmissionCode.IDENTITY_MISSING: 'IDENTITY_MISSING'>} = _codes(<ExceptionInfo AdmissionRejected('IDENTITY_MISSING') tblen=2>)

src\tests\test_canonical_ingestion_admission.py:162: AssertionError
________________ test_blank_observation_builds_candidate_only_through_explicit_approved_fallback_path _________________

    def test_blank_observation_builds_candidate_only_through_explicit_approved_fallback_path():
        observation, match, spec = _blank_observation_and_match()
        with pytest.raises(CandidateValidationError) as exc:
            build_candidate_submission(observation, match, coordinate="B2", spec=spec)
>       assert exc.value.code == "SOURCE_VALUE_MISSING"
E       AssertionError: assert 'STRUCTURE_NOT_APPROVED' == 'SOURCE_VALUE_MISSING'
E
E         - SOURCE_VALUE_MISSING
E         + STRUCTURE_NOT_APPROVED

src\tests\test_canonical_ingestion_admission.py:222: AssertionError
=============================================== short test summary info ===============================================
FAILED src/tests/test_canonical_ingestion_admission.py::test_one_invalid_candidate_rejects_the_entire_batch - AssertionError: assert <AdmissionCode.APPROVAL_REFERENCE_MISSING: 'APPROVAL_REFERENCE_MISSING'> in {<AdmissionCode....
FAILED src/tests/test_canonical_ingestion_admission.py::test_blank_observation_builds_candidate_only_through_explicit_approved_fallback_path - AssertionError: assert 'STRUCTURE_NOT_APPROVED' == 'SOURCE_VALUE_MISSING'
2 failed, 34 passed in 1.43s