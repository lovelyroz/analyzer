"""Read-only probe of CODAL issuer and fiscal-year-end metadata.

Writes a compact audit report to reply.md. Does not modify the project database.
"""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = "https://search.codal.ir/api/search/v1"
SYMBOLS = ("فولاد", "زفارس")
TIMEOUT_SECONDS = 25
PAUSE_SECONDS = 2
OUTPUT = Path("reply.md")


def get_json(path: str, params: dict[str, str] | None = None):
    query = urllib.parse.urlencode(params or {})
    url = f"{BASE}/{path}" + (f"?{query}" if query else "")
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "analyzer-codal-metadata-audit/1.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "fa-IR,fa;q=0.9,en;q=0.8",
            "Referer": "https://www.codal.ir/",
            "Origin": "https://www.codal.ir",
            "sec-fetch-site": "same-site",
            "sec-fetch-mode": "cors",
        },
    )
    with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        raw = response.read().decode("utf-8-sig")
        return url, response.status, json.loads(raw)


def main() -> int:
    lines = [
        "# CODAL fiscal-year metadata live audit",
        "",
        f"- Retrieved UTC: {datetime.now(timezone.utc).isoformat()}",
        "- Mode: read-only; no database access or mutation",
        f"- Symbols requested: {', '.join(SYMBOLS)}",
        "",
    ]

    try:
        company_url, status, companies = get_json("companies")
        lines += [
            "## Issuer directory",
            f"- URL: {company_url}",
            f"- HTTP status: {status}",
            f"- Response type: {type(companies).__name__}",
        ]
        if not isinstance(companies, list):
            raise ValueError("CODAL companies endpoint did not return a JSON list.")

        for symbol in SYMBOLS:
            matches = [
                row for row in companies
                if isinstance(row, dict) and str(row.get("sy", "")).strip() == symbol
            ]
            lines.append(f"- Exact symbol {symbol}: {len(matches)} match(es)")
            for row in matches[:5]:
                lines.append(
                    "  - "
                    + json.dumps(
                        {
                            "symbol": row.get("sy"),
                            "name": row.get("n"),
                            "industry_group": row.get("IG"),
                            "market_type": row.get("st"),
                        },
                        ensure_ascii=False,
                    )
                )

        for index, symbol in enumerate(SYMBOLS):
            if index:
                time.sleep(PAUSE_SECONDS)
            url, status, values = get_json("financialYears", {"Symbol": symbol})
            lines += [
                "",
                f"## Fiscal year ends — {symbol}",
                f"- URL: {url}",
                f"- HTTP status: {status}",
                f"- Response type: {type(values).__name__}",
            ]
            if isinstance(values, list):
                lines.append(f"- Count: {len(values)}")
                lines.append("- Values (source order):")
                lines.extend(f"  - {value}" for value in values)
            else:
                lines.append(
                    "- Unexpected response: "
                    + json.dumps(values, ensure_ascii=False)[:4000]
                )

    except urllib.error.HTTPError as exc:
        lines += [
            "",
            "## ERROR",
            f"- HTTP error: {exc.code} {exc.reason}",
            f"- URL: {exc.url}",
            "- Do not retry repeatedly; CODAL may rate-limit requests.",
        ]
    except Exception as exc:  # noqa: BLE001 - report the exact audit failure
        lines += [
            "",
            "## ERROR",
            f"- {type(exc).__name__}: {exc}",
        ]

    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Audit report written to: {OUTPUT.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
