"""Read-only CLI: python -m src.scripts.market_fx_preflight"""
from __future__ import annotations
import argparse
from pathlib import Path
from src.preflight.market_fx import validate_all, report_json

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]

def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only MarketDaily / FX artifact preflight; no database access.")
    parser.add_argument("--market", type=Path, default=Path("saman_price_history.csv"))
    parser.add_argument("--fx", type=Path, default=Path("dollar-history.xlsx"))
    parser.add_argument("--fx-rate-type", choices=("EXCHANGE_CENTER", "FREE_MARKET"),
                        default="EXCHANGE_CENTER", help="Interpret sell values as Rial or Toman source rates.")
    parser.add_argument("--json-out", type=Path, help="Write JSON report to this path; otherwise stdout.")
    parser.add_argument("--root", type=Path, default=REPOSITORY_ROOT,
                        help="Root used to resolve relative inputs and scan for FREE_MARKET samples.")
    args = parser.parse_args()
    root = args.root.expanduser().resolve()
    def resolve_input(p: Path) -> Path:
        return (p.expanduser() if p.is_absolute() else root / p).resolve()
    market_path, fx_path = resolve_input(args.market), resolve_input(args.fx)
    if args.json_out:
        out_path = resolve_input(args.json_out)
        if out_path in {market_path, fx_path}:
            parser.error("--json-out must not overwrite either input artifact")
    report = validate_all(market_path, fx_path, root=root, fx_rate_type=args.fx_rate_type)
    out = report_json(report)
    if args.json_out:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(out, encoding="utf-8")
    else: print(out, end="")
    for result in report["results"]:
        print(f"{result['feed']}: {result['status']}")
    print(f"Overall: {report['overall_status']} (read-only; no DB/ingestion)")
    return 1 if report["overall_status"] in {"FAIL", "BLOCKED"} or any(r.get("status") in {"FAIL", "BLOCKED"} for r in report["results"]) else 0

if __name__ == "__main__":
    raise SystemExit(main())
