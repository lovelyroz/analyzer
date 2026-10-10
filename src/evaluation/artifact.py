"""Stage 6 Prompt 36 — versioned evaluation artifact identity and provenance.

A pipeline run produces an ``EvaluationArtifactIdentity`` alongside its
verdicts: a versioned, frozen identity naming the methodology, the quality
policy, the purpose (primary vs sensitivity), the evaluation cutoff, the
per-series ReportVersion provenance, and the supersedes link for reruns.

Determinism limits (stated, not solved): ``run_id`` is a uuid4 hex — unique
per execution, NOT deterministic from inputs. Two runs over identical inputs
never collide; identity equality across runs is by field comparison, never by
run_id. No hashing is introduced here (Prompt 36 hard boundary).

What this module does NOT do:

* No scoring, no formulas, no policy changes — purpose/sensitivity reuse the
  authorized P19 path verbatim (``exclude_estimated`` only quarantines
  ESTIMATED actuals with a named reason before the eligibility check).
* No persistence, no DB, no migration — the artifact is an in-memory carrier
  attached to ``EvaluationPipelineResult``.
* No Reliability — forbidden in this prompt.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Iterable, Mapping, Optional, Tuple, Union
from uuid import uuid4

from src.evaluation.aggregate import SeriesKey

ARTIFACT_CONTRACT_VERSION = "ARTIFACT_V1"
DATA_QUALITY_POLICY_VERSION = "DATA_QUALITY_P25"

ARTIFACT_PURPOSES = ("PRIMARY", "SENSITIVITY_ESTIMATED_EXCLUDED")

SENSITIVITY_EXCLUSION_REASON = "SENSITIVITY_ESTIMATED_EXCLUDED"


@dataclass(frozen=True)
class SeriesProvenance:
    """ReportVersion provenance for one evaluated series.

    Multi-period series legitimately span several ReportVersions, so the
    provenance is the distinct SET — never collapsed to one fabricated id:

    * ``report_version_ids`` — sorted distinct ``report_version_id`` values
      from the valid scored Actuals in this series; empty tuple when no
      scored observation carries a valid Actual (explicitly unavailable).
    * ``publication_datetimes`` — sorted distinct publication instants from
      those same Actuals; empty when unavailable.
    * ``data_quality_states`` — sorted distinct quality states of the scored
      observations in this series; empty when the series has no scored
      observations.
    """

    series: SeriesKey
    report_version_ids: Tuple[int, ...] = ()
    publication_datetimes: Tuple[datetime, ...] = ()
    data_quality_states: Tuple[str, ...] = ()


@dataclass(frozen=True)
class EvaluationArtifactIdentity:
    """Versioned identity for one evaluation pipeline execution."""

    run_id: str
    artifact_version: str
    methodology_version: str
    quality_policy_version: str
    purpose: str
    evaluation_cutoff: Optional[datetime]
    series_provenance: Tuple[SeriesProvenance, ...] = ()
    supersedes: Optional[str] = None

    def __post_init__(self) -> None:
        if self.purpose not in ARTIFACT_PURPOSES:
            raise ValueError(
                f"unknown artifact purpose: {self.purpose!r}; "
                f"expected one of {ARTIFACT_PURPOSES!r}"
            )
        if self.supersedes is not None and not self.supersedes:
            raise ValueError("supersedes must be None or a non-empty run id")
        if self.supersedes is not None and self.supersedes == self.run_id:
            raise ValueError("artifact must not supersede itself")


def build_artifact(
    *,
    purpose: str,
    methodology_version: str,
    quality_policy_version: str = DATA_QUALITY_POLICY_VERSION,
    evaluation_cutoff: Optional[datetime] = None,
    series_provenance: Union[
        Mapping[SeriesKey, SeriesProvenance], Iterable[SeriesProvenance]
    ] = (),
    supersedes: Optional[str] = None,
    run_id: Optional[str] = None,
) -> EvaluationArtifactIdentity:
    """Single construction boundary for artifact identities.

    ``run_id`` is generated (uuid4 hex) when not given; tests may force it
    for adversarial cases (e.g. forced duplicates stay distinguishable by
    the ``purpose`` field). ``methodology_version`` arrives as an argument —
    never imported — so this module stays import-cycle free.
    """
    if purpose not in ARTIFACT_PURPOSES:
        raise ValueError(
            f"unknown artifact purpose: {purpose!r}; "
            f"expected one of {ARTIFACT_PURPOSES!r}"
        )
    resolved_run_id = run_id if run_id is not None else uuid4().hex
    if supersedes is not None and not supersedes:
        raise ValueError("supersedes must be None or a non-empty run id")
    if supersedes is not None and supersedes == resolved_run_id:
        raise ValueError("artifact must not supersede itself")
    if isinstance(series_provenance, Mapping):
        provenance = tuple(
            series_provenance[key] for key in sorted(series_provenance)
        )
    else:
        provenance = tuple(
            sorted(series_provenance, key=lambda item: item.series)
        )
    return EvaluationArtifactIdentity(
        run_id=resolved_run_id,
        artifact_version=ARTIFACT_CONTRACT_VERSION,
        methodology_version=methodology_version,
        quality_policy_version=quality_policy_version,
        purpose=purpose,
        evaluation_cutoff=evaluation_cutoff,
        series_provenance=provenance,
        supersedes=supersedes,
    )


def provenance_for_series(
    provenance: Tuple[SeriesProvenance, ...],
) -> Dict[SeriesKey, SeriesProvenance]:
    """Index an artifact's provenance tuple back by series key."""
    return {item.series: item for item in provenance}
