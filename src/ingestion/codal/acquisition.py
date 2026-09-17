"""CODAL source acquisition — independent of DB persistence (Workstream B).

Acquisition failure must be distinguishable from extraction failure.
"""

from __future__ import annotations

import hashlib
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class CodalAcquisitionError(Exception):
    """Source could not be acquired (network, missing file, HTTP error)."""


@dataclass(frozen=True)
class AcquiredSource:
    """Local path to acquired bytes + preserved source identity."""

    local_path: Path
    source_url: Optional[str] = None
    codal_tracking_id: Optional[str] = None
    content_sha256: Optional[str] = None

    @property
    def path(self) -> Path:
        """Backward-compatible destination-path name used by acquisition tests."""
        return self.local_path

    @property
    def source_identity(self) -> Optional[str]:
        """Stable local source identity for audit/tests."""
        if self.local_path is None:
            return None
        return str(self.local_path.resolve())


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def acquire_local_pdf(
    path: Union[str, Path],
    *,
    codal_tracking_id: Optional[str] = None,
    source_url: Optional[str] = None,
) -> AcquiredSource:
    """Deterministic local-file acquisition path (no network)."""
    p = Path(path)
    if not p.is_file():
        raise CodalAcquisitionError(f"local PDF not found: {p}")
    if p.suffix.lower() != ".pdf":
        raise CodalAcquisitionError(f"expected .pdf file, got: {p.suffix!r}")
    return AcquiredSource(
        local_path=p.resolve(),
        source_url=source_url or str(p),
        codal_tracking_id=codal_tracking_id,
        content_sha256=_sha256_file(p),
    )


def acquire_codal_pdf(
    source: Union[str, Path],
    destination: Union[str, Path],
    *,
    retries: int = 2,
) -> AcquiredSource:
    """Acquire a local CODAL PDF into an exact destination path.

    This compatibility entry point is intentionally local-only. Network
    acquisition remains available through acquire_pdf_from_url().
    """
    del retries  # local acquisition has no retryable network operation
    acquired = acquire_local_pdf(source)
    target = Path(destination)
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        shutil.copy2(acquired.local_path, target)
    except OSError as exc:
        raise CodalAcquisitionError(
            f"failed to copy acquired PDF to {target}: {exc}"
        ) from exc
    return AcquiredSource(
        local_path=target,
        source_url=str(source),
        codal_tracking_id=acquired.codal_tracking_id,
        content_sha256=_sha256_file(target),
    )


def acquire_pdf_from_url(
    url: str,
    dest_dir: Union[str, Path],
    *,
    codal_tracking_id: Optional[str] = None,
    timeout_sec: int = 60,
    filename: Optional[str] = None,
) -> AcquiredSource:
    """Download PDF to dest_dir. Idempotent on existing non-empty target."""
    dest = Path(dest_dir)
    dest.mkdir(parents=True, exist_ok=True)
    name = filename or (f"{codal_tracking_id}.pdf" if codal_tracking_id else "codal_download.pdf")
    target = dest / name

    if target.is_file() and target.stat().st_size > 0:
        return AcquiredSource(
            local_path=target.resolve(),
            source_url=url,
            codal_tracking_id=codal_tracking_id,
            content_sha256=_sha256_file(target),
        )

    req = Request(url, headers={"User-Agent": "analyzer-codal-acquisition/1.0"})
    try:
        with urlopen(req, timeout=timeout_sec) as resp:
            data = resp.read()
    except HTTPError as exc:
        raise CodalAcquisitionError(f"HTTP {exc.code} acquiring {url}") from exc
    except URLError as exc:
        raise CodalAcquisitionError(f"URL error acquiring {url}: {exc.reason}") from exc
    except Exception as exc:
        raise CodalAcquisitionError(f"acquisition failed for {url}: {exc}") from exc

    if not data:
        raise CodalAcquisitionError(f"empty response from {url}")
    if data[:4] != b"%PDF":
        raise CodalAcquisitionError(f"response is not a PDF from {url}")

    tmp = target.with_suffix(".partial")
    tmp.write_bytes(data)
    tmp.replace(target)

    return AcquiredSource(
        local_path=target.resolve(),
        source_url=url,
        codal_tracking_id=codal_tracking_id,
        content_sha256=_sha256_file(target),
    )


def copy_acquired(source: AcquiredSource, dest_dir: Union[str, Path]) -> AcquiredSource:
    """Copy acquired file into a working directory (optional staging)."""
    dest = Path(dest_dir)
    dest.mkdir(parents=True, exist_ok=True)
    target = dest / source.local_path.name
    if not target.exists() or _sha256_file(target) != source.content_sha256:
        shutil.copy2(source.local_path, target)
    return AcquiredSource(
        local_path=target.resolve(),
        source_url=source.source_url,
        codal_tracking_id=source.codal_tracking_id,
        content_sha256=_sha256_file(target),
    )
