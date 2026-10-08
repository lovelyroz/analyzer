"""
Forecast Evaluation (Stage 6).

P23 — legacy de-authorization: this package exports nothing at the top
level. The unauthorized legacy path (``ForecastEvaluationEngine``,
legacy score/threshold helpers, legacy carriers) was removed. The
authorized P18–P21 production path lives in the ``observation``,
``aggregate``, ``reliability``, and ``pipeline`` submodules and is
imported directly from those modules.
"""
