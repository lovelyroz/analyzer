import copy
import math
from collections.abc import Mapping as _AbcMapping
from dataclasses import dataclass
from datetime import datetime
from types import MappingProxyType
from typing import Dict, Mapping, Optional, Tuple

from src.forecast.schema import normalize_datetime

# Backward-compatible export retained for existing package consumers.
# Stage 7 V1 no longer uses hard-coded industry target P/E values; target multiples
# come from the benchmark hierarchy and explicit, evidence-backed scenario inputs.
INDUSTRY_TARGET_PE: Dict[str, float] = {}

SCENARIO_WEIGHTS: Dict[str, float] = {
    "bear": 0.20,
    "base": 0.60,
    "bull": 0.20,
}

# Backward-compatible neutral export. V1 intentionally does not use arbitrary
# 0.9/1.0/1.1 scenario gaps; absent explicit economic evidence, all scenarios
# use the benchmark multiple unchanged.
SCENARIO_PE_MULTIPLIER: Dict[str, float] = {
    "bear": 1.00,
    "base": 1.00,
    "bull": 1.00,
}

# Scenario probabilities are built from four family-level evidence distributions.
# Each family receives one vote; correlated metrics must be aggregated before this
# contract. The blend is versioned and backtestable rather than an architecture constant.
PROBABILITY_EVIDENCE_FAMILIES: Tuple[str, ...] = (
    "FUNDAMENTAL_DIRECTION",
    "FORECAST_DIRECTION",
    "PROFITABILITY_ASSUMPTION_RISK",
    "DATA_STRUCTURAL_RISK",
)
PROBABILITY_EVIDENCE_BLEND = 0.25

# V1 does not impose an arbitrary Bear/Base/Bull P/E gap. With no explicit
# economic evidence, all scenarios use the same benchmark multiple. Scenario-
# specific multiple changes must be supplied with an economic rationale and are
# bounded so the mechanism remains explainable, versioned and backtestable.
SCENARIO_MULTIPLE_MAX_ABS_ADJUSTMENT = 0.20
SCENARIO_MULTIPLE_POLICY_VERSION = "STAGE7_V1_EVIDENCE_BACKED"

VALUATION_THRESHOLDS: Dict[str, float] = {
    "very_attractive_expected_upside": 30.0,
    "very_attractive_base_upside": 15.0,
    "attractive_expected_upside": 15.0,
    "attractive_base_upside": 5.0,
    "expensive_expected_upside": -10.0,
    "expensive_base_upside": 0.0,
    "very_expensive_expected_upside": -25.0,
    "very_expensive_base_upside": -10.0,
}

CONFIDENCE_THRESHOLDS: Dict[str, float] = {
    "very_high": 90.0,
    "high": 75.0,
    "moderate": 60.0,
    "low": 40.0,
}

RISK_THRESHOLDS: Dict[str, float] = {
    "extreme_confidence": 40.0,
    "high_scenario_dispersion": 0.50,
    "high_bear_downside": -30.0,
    "medium_confidence": 60.0,
    "medium_bear_downside": -15.0,
}

ALERT_THRESHOLDS: Dict[str, float] = {
    "high_scenario_dispersion": 0.50,
    "low_forecast_reliability": 40.0,
    "benchmark_divergence_ratio": 1.50,
    "historical_divergence_ratio": 1.50,
    "industry_divergence_ratio": 1.50,
    "high_dependence_share": 0.60,
}

# One-at-a-time sensitivity shock for V1 driver impact calculations.
SENSITIVITY_PERTURBATION = 0.10

MIN_INDUSTRY_PEERS = 8
MODEL_VERSION = "STAGE7_V1"
CONTRACT_VERSION = "VALUATION_CONTRACT_V1"

# ---------------------------------------------------------------------------
# P33 — Effective-dated parameter versioning (mechanism only; no policy)
# ---------------------------------------------------------------------------
"""Auditable parameter-version records for Stage 7 V1.

Provided today (verified facts only, no owner decision needed):

* A genesis snapshot built PROGRAMMATICALLY from the live module constants
  above, so recorded values cannot drift from executed values.
* Exact-key resolution (``resolve_parameter_set``): deterministic, with
  explicit errors for missing keys — never a silent fallback to current.
* Date-based selection (``resolve_parameter_set_as_of``) with honest
  semantics: only explicitly dated versions participate; the undated genesis
  record NEVER stands in for history; future-effective versions are never
  selected; overlaps raise instead of picking silently.

Deliberately NOT provided (needs R8/R7 owner decisions):

* ``effective_from`` dates for the existing constants (unknowable from any
  evidence — inventing them is forbidden, so genesis records carry ``None``
  with that meaning recorded explicitly);
* a database-backed registry (no architectural evidence supports one);
* any change to financial values, formulas, or thresholds (every record
  mirrors a live constant; descriptions describe, they do not decide).
"""

GENESIS_VERSION_KEY = "STAGE7_V1/GENESIS"

_UNVERSIONED_GENESIS_NOTE = (
    "Genesis record: temporal validity unknown; never valid "
    "for historical date selection (R8 pending)."
)


# ---------------------------------------------------------------------------
# T4-2 — Deep immutability primitives (read behaviour preserved)
# ---------------------------------------------------------------------------
class FrozenDict(_AbcMapping):
    """Read-only mapping; every nested value is recursively frozen.

    Reads behave like a ``dict`` (indexing, iteration, ``len``, ``items`` and
    equality with plain mappings). Any write raises ``TypeError``/``AttributeError``.
    """

    __slots__ = ("_data",)

    def __init__(self, data=()):
        object.__setattr__(
            self,
            "_data",
            {key: freeze_parameter_value(item) for key, item in dict(data).items()},
        )

    def __getitem__(self, key):
        return self._data[key]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        return f"FrozenDict({self._data!r})"

    def __setattr__(self, name, value):
        raise AttributeError("FrozenDict is immutable.")

    def __delattr__(self, name):
        raise AttributeError("FrozenDict is immutable.")

    def __reduce__(self):
        # Supports copy.copy / copy.deepcopy / pickle; the constructor re-freezes.
        return (FrozenDict, (dict(self._data),))

    __hash__ = None


class FrozenList(tuple):
    """Immutable stand-in for a ``list`` value (marker type so snapshots restore a ``list``).

    Compares equal to a ``list`` with the same items, so existing read/compare
    behaviour is preserved.
    """

    __slots__ = ()

    def __new__(cls, items=()):
        return super().__new__(cls, tuple(freeze_parameter_value(item) for item in items))

    def __eq__(self, other):
        if isinstance(other, list):
            return tuple.__eq__(self, tuple(other))
        return tuple.__eq__(self, other)

    def __ne__(self, other):
        result = self.__eq__(other)
        return result if result is NotImplemented else not result

    __hash__ = tuple.__hash__

    def __repr__(self):
        return f"FrozenList({list(self)!r})"


class FrozenSet(frozenset):
    """Immutable stand-in for a ``set`` value (marker type so snapshots restore a ``set``)."""

    __slots__ = ()

    def __new__(cls, items=()):
        return super().__new__(cls, (freeze_parameter_value(item) for item in items))


def freeze_parameter_value(value: object) -> object:
    """Return an independent, recursively immutable copy of ``value``.

    dict/Mapping -> ``FrozenDict``; list -> ``FrozenList``; set -> ``FrozenSet``;
    tuple/frozenset keep their type with frozen members. Scalars and any other
    type are deep-copied (opaque custom objects cannot be proxied; parameter
    values are expected to be scalars, strings and these containers).
    """
    if isinstance(value, _AbcMapping):
        return FrozenDict(value)
    if isinstance(value, (list, FrozenList)):
        return FrozenList(value)
    if isinstance(value, (set, FrozenSet)):
        return FrozenSet(value)
    if type(value) is tuple:
        return tuple(freeze_parameter_value(item) for item in value)
    if type(value) is frozenset:
        return frozenset(freeze_parameter_value(item) for item in value)
    return copy.deepcopy(value)


def thaw_parameter_value(value: object) -> object:
    """Return a fresh, plain mutable copy (dict/list/set) of a frozen value.

    Used for audit snapshots so serialized output keeps its original shape.
    """
    if isinstance(value, _AbcMapping):
        return {key: thaw_parameter_value(item) for key, item in value.items()}
    if isinstance(value, FrozenList):
        return [thaw_parameter_value(item) for item in value]
    if isinstance(value, FrozenSet):
        return {thaw_parameter_value(item) for item in value}
    if type(value) is tuple:
        return tuple(thaw_parameter_value(item) for item in value)
    if type(value) is frozenset:
        return frozenset(thaw_parameter_value(item) for item in value)
    return copy.deepcopy(value)


class ParameterRegistryInvalidError(ValueError):
    """A ``ParameterRegistry`` was constructed with an invalid version collection."""


@dataclass(frozen=True)
class ParameterRecord:
    parameter_name: str
    parameter_value: object
    effective_from: Optional[datetime]
    description: str

    def __post_init__(self) -> None:
        # T4-2: ``frozen=True`` only protects the attribute binding; freeze the
        # value itself recursively and detach it from the caller's object.
        object.__setattr__(self, "parameter_value", freeze_parameter_value(self.parameter_value))


@dataclass(frozen=True)
class ParameterSetVersion:
    model_version: str
    version_key: str
    effective_from: Optional[datetime]
    records: Tuple[ParameterRecord, ...]

    def __post_init__(self) -> None:
        # Normalise any sequence to a tuple so a caller's list cannot mutate the set later.
        object.__setattr__(self, "records", tuple(self.records))


def _rec(name: str, value: object, description: str) -> ParameterRecord:
    return ParameterRecord(
        parameter_name=name,
        parameter_value=copy.deepcopy(value),
        effective_from=None,
        description=description + " " + _UNVERSIONED_GENESIS_NOTE,
    )


def _genesis_records() -> Tuple[ParameterRecord, ...]:
    return (
        _rec("SCENARIO_WEIGHTS.bear", SCENARIO_WEIGHTS["bear"], "Bear prior probability weight."),
        _rec("SCENARIO_WEIGHTS.base", SCENARIO_WEIGHTS["base"], "Base prior probability weight."),
        _rec("SCENARIO_WEIGHTS.bull", SCENARIO_WEIGHTS["bull"], "Bull prior probability weight."),
        _rec("SCENARIO_PE_MULTIPLIER.bear", SCENARIO_PE_MULTIPLIER["bear"], "Neutral bear multiple (intentionally 1.00)."),
        _rec("SCENARIO_PE_MULTIPLIER.base", SCENARIO_PE_MULTIPLIER["base"], "Neutral base multiple (intentionally 1.00)."),
        _rec("SCENARIO_PE_MULTIPLIER.bull", SCENARIO_PE_MULTIPLIER["bull"], "Neutral bull multiple (intentionally 1.00)."),
        _rec("PROBABILITY_EVIDENCE_FAMILIES", PROBABILITY_EVIDENCE_FAMILIES, "Family-level evidence channels aggregated before this contract."),
        _rec("PROBABILITY_EVIDENCE_BLEND", PROBABILITY_EVIDENCE_BLEND, "Family-mean blend weight."),
        _rec("SCENARIO_MULTIPLE_MAX_ABS_ADJUSTMENT", SCENARIO_MULTIPLE_MAX_ABS_ADJUSTMENT, "Bound on explicit scenario multiple adjustments."),
        _rec("SCENARIO_MULTIPLE_POLICY_VERSION", SCENARIO_MULTIPLE_POLICY_VERSION, "Scenario-multiple policy identifier."),
        _rec("VALUATION_THRESHOLDS.very_attractive_expected_upside", VALUATION_THRESHOLDS["very_attractive_expected_upside"], "Status band gate; engine constant, spec-unratified (D9)."),
        _rec("VALUATION_THRESHOLDS.very_attractive_base_upside", VALUATION_THRESHOLDS["very_attractive_base_upside"], "Status band gate; engine constant, spec-unratified (D9)."),
        _rec("VALUATION_THRESHOLDS.attractive_expected_upside", VALUATION_THRESHOLDS["attractive_expected_upside"], "Status band gate; engine constant, spec-unratified (D9)."),
        _rec("VALUATION_THRESHOLDS.attractive_base_upside", VALUATION_THRESHOLDS["attractive_base_upside"], "Status band gate; engine constant, spec-unratified (D9)."),
        _rec("VALUATION_THRESHOLDS.expensive_expected_upside", VALUATION_THRESHOLDS["expensive_expected_upside"], "Status band gate; engine constant, spec-unratified (D9)."),
        _rec("VALUATION_THRESHOLDS.expensive_base_upside", VALUATION_THRESHOLDS["expensive_base_upside"], "Status band gate; engine constant, spec-unratified (D9)."),
        _rec("VALUATION_THRESHOLDS.very_expensive_expected_upside", VALUATION_THRESHOLDS["very_expensive_expected_upside"], "Status band gate; engine constant, spec-unratified (D9)."),
        _rec("VALUATION_THRESHOLDS.very_expensive_base_upside", VALUATION_THRESHOLDS["very_expensive_base_upside"], "Status band gate; engine constant, spec-unratified (D9)."),
        _rec("CONFIDENCE_THRESHOLDS.very_high", CONFIDENCE_THRESHOLDS["very_high"], "Confidence label gate; engine constant, spec-unratified (D9)."),
        _rec("CONFIDENCE_THRESHOLDS.high", CONFIDENCE_THRESHOLDS["high"], "Confidence label gate; engine constant, spec-unratified (D9)."),
        _rec("CONFIDENCE_THRESHOLDS.moderate", CONFIDENCE_THRESHOLDS["moderate"], "Confidence label gate; engine constant, spec-unratified (D9)."),
        _rec("CONFIDENCE_THRESHOLDS.low", CONFIDENCE_THRESHOLDS["low"], "Confidence label gate; engine constant, spec-unratified (D9)."),
        _rec("RISK_THRESHOLDS.extreme_confidence", RISK_THRESHOLDS["extreme_confidence"], "Risk grade gate; engine constant, spec-unratified (D9)."),
        _rec("RISK_THRESHOLDS.high_scenario_dispersion", RISK_THRESHOLDS["high_scenario_dispersion"], "Risk grade gate; engine constant, spec-unratified (D9)."),
        _rec("RISK_THRESHOLDS.high_bear_downside", RISK_THRESHOLDS["high_bear_downside"], "Risk grade gate; engine constant, spec-unratified (D9)."),
        _rec("RISK_THRESHOLDS.medium_confidence", RISK_THRESHOLDS["medium_confidence"], "Risk grade gate; engine constant, spec-unratified (D9)."),
        _rec("RISK_THRESHOLDS.medium_bear_downside", RISK_THRESHOLDS["medium_bear_downside"], "Risk grade gate; engine constant, spec-unratified (D9)."),
        _rec("ALERT_THRESHOLDS.high_scenario_dispersion", ALERT_THRESHOLDS["high_scenario_dispersion"], "Alert trigger; engine constant, spec-unratified (D9)."),
        _rec("ALERT_THRESHOLDS.low_forecast_reliability", ALERT_THRESHOLDS["low_forecast_reliability"], "Alert trigger; engine constant, spec-unratified (D9)."),
        _rec("ALERT_THRESHOLDS.benchmark_divergence_ratio", ALERT_THRESHOLDS["benchmark_divergence_ratio"], "Alert trigger; engine constant, spec-unratified (D9)."),
        _rec("ALERT_THRESHOLDS.historical_divergence_ratio", ALERT_THRESHOLDS["historical_divergence_ratio"], "Alert trigger; engine constant, spec-unratified (D9)."),
        _rec("ALERT_THRESHOLDS.industry_divergence_ratio", ALERT_THRESHOLDS["industry_divergence_ratio"], "Alert trigger; engine constant, spec-unratified (D9)."),
        _rec("ALERT_THRESHOLDS.high_dependence_share", ALERT_THRESHOLDS["high_dependence_share"], "Declared but unwired dead definition; must not be activated without D2 (P27)."),
        _rec("SENSITIVITY_PERTURBATION", SENSITIVITY_PERTURBATION, "Driver-impact shock size; not approved for flip detection (P27)."),
        _rec("MIN_INDUSTRY_PEERS", MIN_INDUSTRY_PEERS, "Minimum valid forward peers for industry benchmark selection."),
        _rec("MODEL_VERSION", MODEL_VERSION, "Build identifier stamped on every result; not a registry."),
        _rec("CONTRACT_VERSION", CONTRACT_VERSION, "Contract identifier stamped on every result; not a registry."),
        _rec("INDUSTRY_TARGET_PE", INDUSTRY_TARGET_PE, "Retained empty for backward compatibility; unused in V1."),
    )


GENESIS_VERSION = ParameterSetVersion(
    model_version=MODEL_VERSION,
    version_key=GENESIS_VERSION_KEY,
    effective_from=None,
    records=_genesis_records(),
)


def live_genesis_parameter_set() -> ParameterSetVersion:
    """Genesis set rebuilt from the CURRENT module constants (not import time).

    The legacy, non-point-in-time valuation path calculates with the live module
    constants (existing, tested behavior). Rebuilding the set on every call makes
    the recorded values equal the values the calculation actually consumes, even
    if a module constant was modified after import.
    """
    return ParameterSetVersion(
        model_version=MODEL_VERSION,
        version_key=GENESIS_VERSION_KEY,
        effective_from=None,
        records=_genesis_records(),
    )


@dataclass(frozen=True)
class ParameterRegistry:
    versions: Tuple[ParameterSetVersion, ...] = (GENESIS_VERSION,)

    def __post_init__(self) -> None:
        # T4-1: exact-key resolution is only meaningful when keys are unique.
        versions = tuple(self.versions)
        seen = set()
        duplicated = set()
        for version in versions:
            key = version.version_key
            if key in seen:
                duplicated.add(key)
            seen.add(key)
        if duplicated:
            raise ParameterRegistryInvalidError(
                "Duplicate version_key in ParameterRegistry: "
                + ", ".join(repr(key) for key in sorted(duplicated, key=repr))
                + "; version keys must be unique."
            )
        object.__setattr__(self, "versions", versions)


DEFAULT_REGISTRY = ParameterRegistry()


def resolve_parameter_set(
    version_key: str,
    registry: ParameterRegistry = DEFAULT_REGISTRY,
) -> ParameterSetVersion:
    """Return the exact versioned parameter set for ``version_key``.

    Missing keys raise ``KeyError`` — silently falling back to the current
    version is forbidden, so absence is always explicit and loud.
    """
    for version in registry.versions:
        if version.version_key == version_key:
            return version
    raise KeyError(f"Unknown Stage 7 parameter version: {version_key!r}.")


def resolve_parameter_set_as_of(
    as_of: Optional[datetime],
    registry: ParameterRegistry = DEFAULT_REGISTRY,
) -> ParameterSetVersion:
    """Select the parameter version effective at ``as_of`` — deterministically.

    Only explicitly dated versions participate: a version covers ``as_of``
    when its ``effective_from`` is set and ``<= as_of``; the newest covering
    version wins; future-effective versions never leak in. Undated records
    (including the whole genesis set) never stand in for history, so with
    only genesis registered this ALWAYS raises ``LookupError`` naming the
    missing R8-dated records — a loud, non-silent failure, never a quiet
    fallback to current values. Overlapping effective dates raise ambiguity
    instead of picking silently. ``as_of=None`` raises: selection without an
    as-of instant is undefined and none is invented.
    """
    if as_of is None:
        raise LookupError(
            "Stage 7 parameter as-of selection requires an as-of instant; "
            "refusing to guess one."
        )
    moment = normalize_datetime(as_of)
    candidates = [
        version
        for version in registry.versions
        if version.effective_from is not None
        and normalize_datetime(version.effective_from) <= moment
    ]
    if not candidates:
        raise LookupError(
            f"No dated Stage 7 parameter version covers as_of={moment.isoformat()}; "
            "historical selection requires R8-dated records (genesis is undated "
            "and never stands in for history)."
        )
    best = max(candidates, key=lambda version: normalize_datetime(version.effective_from))
    tied = [v for v in candidates if normalize_datetime(v.effective_from) == normalize_datetime(best.effective_from)]
    if len(tied) > 1:
        raise LookupError(
            "Ambiguous Stage 7 parameter versions for as_of="
            f"{moment.isoformat()}: {[v.version_key for v in tied]}."
        )
    return best


# ---------------------------------------------------------------------------
# Final P35 — consumed-parameter object and explicit selection (mechanism only)
# ---------------------------------------------------------------------------

class ParameterSetInvalidError(ValueError):
    """A selected parameter set lacks, duplicates, or malforms a consumed record.

    There is deliberately NO fallback to module constants or to another version.
    """


# Literals still hard-coded in ``engine.py`` formulas. They have no registry
# record and their ownership is not confirmed by the specification, so they are
# NOT governed by a parameter set; they are listed so audit metadata cannot
# imply that the snapshot covers them.
LITERALS_OUTSIDE_REGISTRY: Tuple[str, ...] = (
    "CONFIDENCE_FORMULA: component weights 0.40/0.20/0.20/0.20, benchmark scores 100/25, dispersion penalty min(40, dispersion*50)",
    "SCORE_DEFAULTS: reliability 50, probability confidence 50, data quality 100, clamp range 0-100",
    "DRIVER_UNCERTAINTY_FORMULA: weights 0.5/0.3/0.2 and impact normalization floor 1e-9",
    "ROUNDING: fair value 2 decimals, target/forward P/E and driver outputs 4 decimals",
)

_GROUP_SPECS: Dict[str, Tuple[str, Tuple[str, ...]]] = {
    "scenario_weights": ("SCENARIO_WEIGHTS", ("bear", "base", "bull")),
    "valuation_thresholds": (
        "VALUATION_THRESHOLDS",
        (
            "very_attractive_expected_upside", "very_attractive_base_upside",
            "attractive_expected_upside", "attractive_base_upside",
            "expensive_expected_upside", "expensive_base_upside",
            "very_expensive_expected_upside", "very_expensive_base_upside",
        ),
    ),
    "confidence_thresholds": ("CONFIDENCE_THRESHOLDS", ("very_high", "high", "moderate", "low")),
    "risk_thresholds": (
        "RISK_THRESHOLDS",
        ("extreme_confidence", "high_scenario_dispersion", "high_bear_downside",
         "medium_confidence", "medium_bear_downside"),
    ),
    "alert_thresholds": (
        "ALERT_THRESHOLDS",
        ("high_scenario_dispersion", "low_forecast_reliability", "benchmark_divergence_ratio",
         "historical_divergence_ratio", "industry_divergence_ratio"),
    ),
}
_SCALAR_NAMES: Tuple[str, ...] = (
    "PROBABILITY_EVIDENCE_BLEND",
    "SCENARIO_MULTIPLE_MAX_ABS_ADJUSTMENT",
    "SENSITIVITY_PERTURBATION",
    "MIN_INDUSTRY_PEERS",
)
_STRING_NAMES: Tuple[str, ...] = ("SCENARIO_MULTIPLE_POLICY_VERSION", "MODEL_VERSION", "CONTRACT_VERSION")
_FAMILIES_NAME = "PROBABILITY_EVIDENCE_FAMILIES"


def _number(name: str, value: object) -> object:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ParameterSetInvalidError(f"Parameter {name!r} must be a finite number, got {value!r}.")
    return value


@dataclass(frozen=True)
class ConsumedParameters:
    """Immutable view of the parameter values the valuation actually consumes.

    The engine reads ONLY from this object for registry-governed values, and the
    audit snapshot is produced from the same ``values`` mapping, so recorded and
    consumed values cannot disagree.
    """

    version_key: str
    set_model_version: str
    effective_from: Optional[datetime]
    values: Mapping[str, object]
    consumed_names: Tuple[str, ...]
    recorded_not_consumed_names: Tuple[str, ...]
    scenario_weights: Mapping[str, object]
    valuation_thresholds: Mapping[str, object]
    confidence_thresholds: Mapping[str, object]
    risk_thresholds: Mapping[str, object]
    alert_thresholds: Mapping[str, object]
    probability_evidence_blend: object
    probability_evidence_families: Tuple[str, ...]
    scenario_multiple_max_abs_adjustment: object
    scenario_multiple_policy_version: str
    sensitivity_perturbation: object
    min_industry_peers: object
    model_version: str
    contract_version: str

    def snapshot(self) -> Dict[str, object]:
        """Fresh plain (dict/list) deep copy of every recorded value.

        Mutating it cannot alter this object; nested frozen values are thawed so
        the audit payload keeps its original, serializable shape.
        """
        return {name: thaw_parameter_value(value) for name, value in self.values.items()}


def consume_parameter_set(version: ParameterSetVersion) -> ConsumedParameters:
    """Validate ``version`` and freeze the values the valuation will consume.

    Missing, duplicated or non-numeric consumed records raise
    ``ParameterSetInvalidError``; nothing is ever filled from module constants.
    """
    values: Dict[str, object] = {}
    for record in version.records:
        if record.parameter_name in values:
            raise ParameterSetInvalidError(
                f"Duplicate parameter {record.parameter_name!r} in version {version.version_key!r}."
            )
        values[record.parameter_name] = freeze_parameter_value(record.parameter_value)

    consumed: list = []
    groups: Dict[str, Mapping[str, object]] = {}
    missing: list = []
    for attr, (prefix, keys) in _GROUP_SPECS.items():
        group: Dict[str, object] = {}
        for key in keys:
            full = f"{prefix}.{key}"
            consumed.append(full)
            if full not in values:
                missing.append(full)
            else:
                group[key] = _number(full, values[full])
        groups[attr] = MappingProxyType(group)
    for name in _SCALAR_NAMES + _STRING_NAMES + (_FAMILIES_NAME,):
        consumed.append(name)
        if name not in values:
            missing.append(name)
    if missing:
        raise ParameterSetInvalidError(
            f"Parameter set {version.version_key!r} is missing consumed records: {sorted(missing)}."
        )
    scalars = {name: _number(name, values[name]) for name in _SCALAR_NAMES}
    strings = {}
    for name in _STRING_NAMES:
        if not isinstance(values[name], str) or not values[name].strip():
            raise ParameterSetInvalidError(f"Parameter {name!r} must be a non-empty string.")
        strings[name] = values[name]
    families = values[_FAMILIES_NAME]
    if (
        not isinstance(families, (tuple, list))
        or not families
        or not all(isinstance(item, str) and item.strip() for item in families)
    ):
        raise ParameterSetInvalidError(f"Parameter {_FAMILIES_NAME!r} must be a non-empty sequence of strings.")

    consumed_names = tuple(sorted(consumed))
    return ConsumedParameters(
        version_key=version.version_key,
        set_model_version=version.model_version,
        effective_from=version.effective_from,
        values=MappingProxyType(values),
        consumed_names=consumed_names,
        recorded_not_consumed_names=tuple(sorted(set(values) - set(consumed_names))),
        scenario_weights=groups["scenario_weights"],
        valuation_thresholds=groups["valuation_thresholds"],
        confidence_thresholds=groups["confidence_thresholds"],
        risk_thresholds=groups["risk_thresholds"],
        alert_thresholds=groups["alert_thresholds"],
        probability_evidence_blend=scalars["PROBABILITY_EVIDENCE_BLEND"],
        probability_evidence_families=tuple(families),
        scenario_multiple_max_abs_adjustment=scalars["SCENARIO_MULTIPLE_MAX_ABS_ADJUSTMENT"],
        scenario_multiple_policy_version=strings["SCENARIO_MULTIPLE_POLICY_VERSION"],
        sensitivity_perturbation=scalars["SENSITIVITY_PERTURBATION"],
        min_industry_peers=scalars["MIN_INDUSTRY_PEERS"],
        model_version=strings["MODEL_VERSION"],
        contract_version=strings["CONTRACT_VERSION"],
    )


def select_parameter_set_for_valuation(
    parameter_registry: Optional[ParameterRegistry] = None,
    parameter_as_of: Optional[datetime] = None,
) -> Tuple[ParameterSetVersion, Dict[str, object]]:
    """Choose the parameter set for one valuation, with truthful provenance.

    * Neither argument supplied (legacy): live genesis constants, labelled
      ``FIXED_GENESIS_LEGACY`` and ``point_in_time_selection_applied=False``.
      This never claims historical validity.
    * Either argument supplied: explicit effective-dated selection through
      ``resolve_parameter_set_as_of``. A missing as-of instant, an empty or
      overlapping registry, or a registry holding only undated genesis raises
      ``LookupError`` — no silent fallback to genesis or to a newer version.

    Which date governs selection (cutoff, valuation date, other) is the
    unresolved R8/D9 decision, so the as-of instant is never inferred here; the
    caller supplies it and provenance records it as caller-supplied.
    """
    if parameter_registry is None and parameter_as_of is None:
        live = live_genesis_parameter_set()
        live_values = {r.parameter_name: r.parameter_value for r in live.records}
        import_values = {r.parameter_name: r.parameter_value for r in GENESIS_VERSION.records}
        return live, {
            "mode": "FIXED_GENESIS_LEGACY",
            "point_in_time_selection_applied": False,
            "as_of_requested": None,
            "as_of_source": None,
            "module_constants_modified_since_import": live_values != import_values,
            "caveat": (
                "Undated genesis constants; temporal validity for historical "
                "valuation is NOT verified (R8/D9 pending)."
            ),
        }
    registry = DEFAULT_REGISTRY if parameter_registry is None else parameter_registry
    version = resolve_parameter_set_as_of(parameter_as_of, registry)
    return version, {
        "mode": "AS_OF_EFFECTIVE_DATED",
        "point_in_time_selection_applied": True,
        "as_of_requested": normalize_datetime(parameter_as_of).isoformat(),
        "as_of_source": "CALLER_SUPPLIED",
        "module_constants_modified_since_import": None,
        "caveat": None,
    }