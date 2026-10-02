from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


@dataclass
class SingleForecastChain:
    """Forecast chain for one scenario.

    The first four fields preserve the original Stage 5 positional contract.
    """
    revenue: Optional[float] = None
    operating_profit: Optional[float] = None
    net_profit: Optional[float] = None
    eps: Optional[float] = None
    operating_margin: Optional[float] = None
    roe: Optional[float] = None
    method: str = "INSUFFICIENT_DATA"
    quality: str = "INSUFFICIENT_DATA"
    assumptions: Dict[str, Any] = field(default_factory=dict)
    scenario: Optional[str] = None
    forecast_horizon: str = "12M"


@dataclass
class ScenarioForecastResult:
    """Bear/Base/Bull forecast set."""
    bear: SingleForecastChain
    base: SingleForecastChain
    bull: SingleForecastChain


@dataclass
class CompanyForecastResult:
    company_id: int
    forecast_period_id: int
    data_cutoff_datetime: datetime
    industry_code: str
    scenario_forecasts: ScenarioForecastResult
    forecast_method: str
    model_version: str
    calculation_timestamp: datetime
    horizon: str = "12M"
    baseline_method: str = "UNKNOWN"
    data_quality: str = "VALID"
    assumptions: Dict[str, Any] = field(default_factory=dict)
    benchmark: Optional[SingleForecastChain] = None

    @property
    def scenarios(self) -> ScenarioForecastResult:
        return self.scenario_forecasts

    def to_record(self, scenario: str, forecast_id: int,
                  input_refs: Optional[Sequence["ForecastInputRef"]] = None
                  ) -> "ForecastRecord":
        """Freeze one scenario chain into an immutable, versionable record.

        ``input_refs`` defaults to the references the caller declared while
        generating the forecast, so the audit trail survives even when a caller
        passes none. A missing metric is carried through as ``None`` and is
        never coerced to zero (spec §27).
        """
        chain = getattr(self.scenario_forecasts, scenario.lower())
        if input_refs is None:
            # Audit handles written by the engine: the caller's declared refs
            # are the audit trail, with the engine's own raw ref capture as the
            # last resort so a record always carries something traceable.
            input_refs = (
                self.assumptions.get("__declared_input_refs")
                or self.assumptions.get("__input_refs")
                or ()
            )
        return ForecastRecord(
            forecast_id=forecast_id,
            forecast_version=0,
            company_id=self.company_id,
            forecast_period_id=self.forecast_period_id,
            industry_code=self.industry_code,
            forecast_horizon=self.horizon,
            scenario=scenario.upper(),
            forecast_timestamp=self.calculation_timestamp,
            data_cutoff_datetime=normalize_datetime(self.data_cutoff_datetime),
            model_version=self.model_version,
            forecast_method=chain.method or self.forecast_method,
            data_quality=chain.quality or self.data_quality,
            baseline_method=self.baseline_method,
            revenue=chain.revenue,
            operating_profit=chain.operating_profit,
            operating_margin=chain.operating_margin,
            net_profit=chain.net_profit,
            eps=chain.eps,
            roe=chain.roe,
            assumptions=dict(chain.assumptions),
            input_refs=tuple(input_refs),
            stage4_provenance=self.assumptions.get("__stage4_provenance"),
        )

    def records(self, forecast_id_start: int = 1,
                input_refs: Sequence["ForecastInputRef"] = ()
                ) -> List["ForecastRecord"]:
        """Freeze all three scenarios into ordered audit records."""
        return [
            self.to_record(name, forecast_id_start + i, input_refs)
            for i, name in enumerate(("bear", "base", "bull"))
        ]


@dataclass
class ForecastInput:
    """Normalized input contract for Stage 5 calculations."""
    values: Dict[str, Any]

    def get(self, key: str, default: Any = None) -> Any:
        return self.values.get(key, default)

    def has(self, key: str) -> bool:
        return self.values.get(key) is not None


@dataclass(frozen=True)
class ForecastInputRef:
    """Pointer from a forecast back to the fact that fed it (spec §29).

    ``available_at`` is the instant the input became knowable to the forecast
    (typically the report publication datetime). A forecast whose cutoff
    precedes ``available_at`` is a Point-in-Time violation (spec §25).
    """
    fact_key: str
    report_version_id: Optional[int] = None
    available_at: Optional[datetime] = None
    source: Optional[str] = None

    @classmethod
    def from_mapping(cls, mapping: Dict[str, Any]) -> "ForecastInputRef":
        return cls(
            fact_key=mapping["fact_key"],
            report_version_id=mapping.get("report_version_id"),
            available_at=normalize_datetime(mapping.get("available_at")),
            source=mapping.get("source"),
        )

    def available_at_or(self, fallback: datetime) -> datetime:
        if self.available_at is None:
            return fallback
        return self.available_at if self.available_at.tzinfo else self.available_at.replace(tzinfo=timezone.utc)


@dataclass(frozen=True)
class ForecastRecord:
    """Immutable, versioned snapshot of one scenario forecast at one cutoff.

    Records are append-only: once stored they are never mutated and never
    replaced (spec §24).
    """
    forecast_id: int
    forecast_version: int
    company_id: int
    forecast_period_id: int
    industry_code: str
    forecast_horizon: str
    scenario: str
    forecast_timestamp: datetime
    data_cutoff_datetime: datetime
    model_version: str
    forecast_method: str
    data_quality: str
    baseline_method: str
    revenue: Optional[float]
    operating_profit: Optional[float]
    operating_margin: Optional[float]
    net_profit: Optional[float]
    eps: Optional[float]
    roe: Optional[float]
    assumptions: Dict[str, Any] = field(default_factory=dict)
    input_refs: Tuple[ForecastInputRef, ...] = ()
    stage4_provenance: Optional[Dict[str, Any]] = None

    def key(self) -> Tuple[Any, ...]:
        """Natural identity of the forecast series this record belongs to."""
        return (
            self.company_id,
            self.forecast_period_id,
            self.forecast_horizon,
            self.scenario,
        )

    def is_missing(self, metric: str) -> bool:
        """Missing means genuinely unknown, never zero (spec §27)."""
        return getattr(self, metric) is None


class ForecastVersionExistsError(ValueError):
    """A caller-supplied forecast_version collides with a stored record."""


def normalize_datetime(value: Optional[Any]) -> Optional[datetime]:
    """Fold naive datetimes onto UTC so cutoffs remain comparable.

    Accepts ISO-8601 strings as well as ``datetime`` instances, since input
    provenance may arrive serialized (spec §29 audit trail).
    """
    if value is None:
        return None
    if isinstance(value, str):
        value = datetime.fromisoformat(value)
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def filter_pit_inputs(refs: Iterable[ForecastInputRef],
                      cutoff: datetime) -> Tuple[List[ForecastInputRef], List[ForecastInputRef]]:
    """Split inputs into those available at ``cutoff`` and those not (spec §25)."""
    cutoff = normalize_datetime(cutoff) or cutoff
    available: List[ForecastInputRef] = []
    dropped: List[ForecastInputRef] = []
    for ref in refs:
        if ref.available_at is None or normalize_datetime(ref.available_at) <= cutoff:
            available.append(ref)
        else:
            dropped.append(ref)
    return available, dropped


class ForecastVersionStore:
    """Append-only registry of versioned forecast records (spec §24).

    Records are stored once and never overwritten. Re-saving the identical
    record is idempotent; saving a changed record under the same natural key
    creates the next version rather than replacing the previous one.
    """

    def __init__(self) -> None:
        self._by_key: Dict[Tuple[Any, ...], List[ForecastRecord]] = {}

    def save(self, record: ForecastRecord) -> ForecastRecord:
        key = record.key()
        versions = self._by_key.setdefault(key, [])

        # A caller-supplied version must match a stored record exactly, or not
        # at all: anything else is an attempted overwrite.
        if record.forecast_version != 0:
            for stored in versions:
                if stored.forecast_version == record.forecast_version:
                    if stored == record:
                        return stored
                    raise ForecastVersionExistsError(
                        f"forecast version {record.forecast_version} already stored for {key}"
                    )

        # Re-saving the identical latest record is a no-op rather than a new
        # version: the series is unchanged, so nothing was overwritten.
        if versions:
            latest = versions[-1]
            if replace(latest, forecast_version=0) == replace(record, forecast_version=0):
                return latest

        stored = replace(record, forecast_version=len(versions) + 1)
        versions.append(stored)
        return stored

    def history(self, company_id: int, forecast_period_id: int, horizon: str,
                scenario: str) -> List[ForecastRecord]:
        return list(self._by_key.get(
            (company_id, forecast_period_id, horizon, scenario.upper()), []
        ))

    def latest(self, company_id: int, forecast_period_id: int, horizon: str,
               scenario: str) -> Optional[ForecastRecord]:
        versions = self.history(company_id, forecast_period_id, horizon, scenario)
        return versions[-1] if versions else None

    def revision_trend(self, company_id: int, forecast_period_id: int, horizon: str,
                       scenario: str, metric: str = "eps") -> Optional[str]:
        """Earnings revision direction across preserved versions (spec §24)."""
        versions = self.history(company_id, forecast_period_id, horizon, scenario)
        values = [getattr(v, metric) for v in versions]
        if len(values) < 2 or any(v is None for v in values):
            return None
        if all(values[i] < values[i + 1] for i in range(len(values) - 1)):
            return "UPWARD"
        if all(values[i] > values[i + 1] for i in range(len(values) - 1)):
            return "DOWNWARD"
        return "MIXED"

    def read_at_cutoff(self, company_id: int, forecast_period_id: int, horizon: str,
                       scenario: str, cutoff_datetime: datetime) -> Optional[ForecastRecord]:
        """Newest record valid at ``cutoff_datetime`` (spec §25).

        Returns ``None`` when no record exists at that cutoff or when every
        surviving record depended on information published after it.
        """
        cutoff = normalize_datetime(cutoff_datetime)
        for record in reversed(self.history(company_id, forecast_period_id, horizon, scenario)):
            if normalize_datetime(record.data_cutoff_datetime) > cutoff:
                continue
            if self._late_inputs(record, cutoff):
                continue
            return record
        return None

    def pit_violations(self, cutoff_datetime: datetime) -> List[ForecastRecord]:
        """Records that saw information published after ``cutoff_datetime``."""
        cutoff = normalize_datetime(cutoff_datetime)
        return [
            record
            for versions in self._by_key.values()
            for record in versions
            if normalize_datetime(record.data_cutoff_datetime) <= cutoff
            and self._late_inputs(record, cutoff)
        ]

    @staticmethod
    def _late_inputs(record: ForecastRecord, cutoff: datetime) -> List[ForecastInputRef]:
        return [
            ref for ref in record.input_refs
            if ref.available_at is not None
            and normalize_datetime(ref.available_at) > cutoff
        ]

    def count(self) -> int:
        return sum(len(versions) for versions in self._by_key.values())


SUPPORTED_HORIZONS = ("1M", "3M", "6M", "12M")

NON_FINANCIAL_INDUSTRIES = {
    "PETROCHEMICAL", "CHEMICAL", "METALS", "MINING", "CEMENT",
    "FOOD", "PHARMACEUTICAL"
}

FINANCIAL_INDUSTRIES = {"BANK", "INVESTMENT", "HOLDING"}
SUPPORTED_INDUSTRIES = NON_FINANCIAL_INDUSTRIES | FINANCIAL_INDUSTRIES
