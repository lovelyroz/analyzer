from dataclasses import dataclass, field
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

    def to_record(self, scenario: str, forecast_id: Optional[int] = None,
                  input_refs: Optional[Sequence["ForecastInputRef"]] = None
                  ) -> "ForecastRecord":
        """Freeze one scenario into an immutable runtime evaluation record.

        ``input_refs`` defaults to the references the caller declared while
        generating the forecast, so runtime auditability survives even when a
        caller passes none. ``forecast_id`` is accepted temporarily for source
        compatibility and deliberately ignored; runtime records have no
        database identity or version assignment. Missing metrics stay None.
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

    def records(self, forecast_id_start: Optional[int] = None,
                input_refs: Optional[Sequence["ForecastInputRef"]] = None
                ) -> List["ForecastRecord"]:
        """Freeze all scenarios into ordered runtime records.

        ``forecast_id_start`` is ignored for legacy source compatibility.
        Input provenance defaults to references captured during generation;
        records have no database ID or version history.
        """
        return [
            self.to_record(name, input_refs=input_refs)
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
class OperationalFx:
    """A resolved operational / company FX rate (spec §30).

    FREE_MARKET FX and OPERATIONAL FX are separate concepts that must never be
    silently substituted for one another. This type is the only way an
    operational rate reaches the forecast, and it always says where it came
    from and whether it had to be estimated.

    ``rate`` is ``None`` when no operational rate and no approved proxy could be
    found. A genuinely missing rate is not zero and is not a FREE_MARKET rate,
    so the FX-linked part of the chain stays missing rather than being priced
    at the wrong currency.
    """

    rate: Optional[float]
    source: str
    estimated: bool = False
    proxy_basis: Optional[str] = None
    reference_date: Optional[str] = None
    confidence: Optional[str] = None

    def is_proxy(self) -> bool:
        return self.estimated and self.proxy_basis is not None

    def provenance(self) -> Dict[str, Any]:
        return {
            "source": self.source,
            "estimated": self.estimated,
            "proxy_basis": self.proxy_basis,
            "reference_date": self.reference_date,
            "confidence": self.confidence,
        }


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
    """Immutable in-memory snapshot of one scenario forecast at one cutoff."""
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


SUPPORTED_HORIZONS = ("1M", "3M", "6M", "12M")

NON_FINANCIAL_INDUSTRIES = {
    "PETROCHEMICAL", "CHEMICAL", "METALS", "MINING", "CEMENT",
    "FOOD", "PHARMACEUTICAL"
}

FINANCIAL_INDUSTRIES = {"BANK", "INVESTMENT", "HOLDING"}
SUPPORTED_INDUSTRIES = NON_FINANCIAL_INDUSTRIES | FINANCIAL_INDUSTRIES
