"""Read-only probe of CODAL issuer and fiscal-year-end metadata.

Annual filing search excludes subsidiary issuers (Childs=false) and includes
main-company filings (Mains=true). Writes reply.md; never accesses the database.
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



def get_annual_filings(symbol: str):
    """Fetch CODAL annual financial-statement filing metadata for one exact symbol."""
    params = {
        "Symbol": symbol, "Category": "1", "LetterType": "6", "Length": "12",
        "PageNumber": "1", "Audited": "true", "NotAudited": "true",
        "Consolidatable": "true", "NotConsolidatable": "true",
        "Childs": "false", "Mains": "true", "Publisher": "false", "search": "true",
    }
    query = urllib.parse.urlencode(params)
    url = f"https://search.codal.ir/api/search/v2/q?{query}"
    request = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "fa-IR,fa;q=0.9,en;q=0.8",
        "Referer": "https://www.codal.ir/",
        "Origin": "https://www.codal.ir",
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
    })
    with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        payload = json.loads(response.read().decode("utf-8-sig"))
        return url, response.status, payload


def get_filings_for_year_end(symbol: str, year_end: str):
    """Fetch main-issuer financial-statement filings for one exact Jalali year-end."""
    params = {
        "Symbol": symbol, "YearEndToDate": year_end, "PageNumber": "1",
        "Childs": "false", "Mains": "true", "search": "true",
    }
    query = urllib.parse.urlencode(params)
    url = f"https://search.codal.ir/api/search/v2/q?{query}"
    request = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "fa-IR,fa;q=0.9,en;q=0.8",
        "Referer": "https://www.codal.ir/",
        "Origin": "https://www.codal.ir",
    })
    with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        payload = json.loads(response.read().decode("utf-8-sig"))
        return url, response.status, payload


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

            time.sleep(PAUSE_SECONDS)
            search_url, search_status, search_result = get_annual_filings(symbol)
            letters = search_result.get("Letters", []) if isinstance(search_result, dict) else []
            lines += [
                "",
                f"## Annual financial-statement filings — {symbol} (main issuer; subsidiaries excluded)",
                f"- URL: {search_url}",
                f"- HTTP status: {search_status}",
                f"- Total matches reported by CODAL: {search_result.get('Total') if isinstance(search_result, dict) else 'invalid'}",
                f"- Page count reported by CODAL: {search_result.get('Page') if isinstance(search_result, dict) else 'invalid'}",
                f"- Records on first page: {len(letters) if isinstance(letters, list) else 'invalid'}",
                "- Query scope: Childs=false, Mains=true",
            ]
            if isinstance(letters, list):
                for letter in letters:
                    if isinstance(letter, dict):
                        lines.append("  - " + json.dumps({
                            "tracing_no": letter.get("TracingNo"),
                            "symbol": letter.get("Symbol"),
                            "company_name": letter.get("CompanyName"),
                            "title": letter.get("Title"),
                            "sent": letter.get("SentDateTime"),
                            "published": letter.get("PublishDateTime"),
                            "letter_code": letter.get("LetterCode"),
                            "url": letter.get("Url"),
                        }, ensure_ascii=False))

        # Broad ZFars checks: omit Category, LetterType and Length so the
        # exact dates can be traced across filing types, not only annual FS.
        focused_year_ends = (
            "1403/10/30", "1402/12/29", "1403/09/30",
        )
        for year_end in focused_year_ends:
            time.sleep(PAUSE_SECONDS)
            url, status, payload = get_filings_for_year_end("زفارس", year_end)
            letters = payload.get("Letters", []) if isinstance(payload, dict) else []
            lines += [
                "",
                f"## ZFars filings for exact date {year_end} (all filing categories/types)",
                f"- URL: {url}",
                f"- HTTP status: {status}",
                f"- Total matches reported by CODAL: {payload.get('Total') if isinstance(payload, dict) else 'invalid'}",
                "- Query scope: no Category, LetterType or Length filter; Childs=false, Mains=true",
                f"- Records on first page: {len(letters) if isinstance(letters, list) else 'invalid'}",
            ]
            if isinstance(letters, list):
                for letter in letters:
                    if isinstance(letter, dict):
                        lines.append("  - " + json.dumps({
                            "tracing_no": letter.get("TracingNo"),
                            "symbol": letter.get("Symbol"),
                            "company_name": letter.get("CompanyName"),
                            "title": letter.get("Title"),
                            "sent": letter.get("SentDateTime"),
                            "published": letter.get("PublishDateTime"),
                            "period_length": letter.get("Length"),
                            "year_end_to_date": letter.get("YearEndToDate"),
                            "letter_code": letter.get("LetterCode"),
                            "url": letter.get("Url"),
                        }, ensure_ascii=False))


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
