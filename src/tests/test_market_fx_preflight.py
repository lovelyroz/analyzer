import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys

from openpyxl import Workbook

from src.preflight.market_fx import validate_market, validate_fx, find_free_market_sample, artifact_identity


def market_file(tmp_path, headers=("J-Date", "Close", "Volume", "No", "Value", "Ticker"), rows=None):
    p = tmp_path / "market.csv"
    with p.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f); w.writerow(headers)
        for row in rows or [["1405-08-10", "20", "3", "1", "60", "SAMAN"]]: w.writerow(row)
    return p


def fx_file(tmp_path, headers=("تاریخ", "خرید (ریال)", "فروش (ریال)"), rows=None):
    p = tmp_path / "fx.xlsx"; wb = Workbook(); ws = wb.active
    ws.append(headers)
    for row in rows or [["1405-08-10", 100, 200]]: ws.append(row)
    wb.save(p); return p


def test_valid_market_daily(tmp_path):
    assert validate_market(market_file(tmp_path))["status"] == "WARNING"  # provenance gap


def test_missing_market_field(tmp_path):
    r = validate_market(market_file(tmp_path, ("J-Date", "Close")))
    assert any(x["code"] == "MISSING_REQUIRED_FIELDS" for x in r["issues"])


def test_invalid_jalali_date(tmp_path):
    r = validate_market(market_file(tmp_path, rows=[["1405-13-10", "20", "3", "1", "60", "SAMAN"]]))
    assert any(x["code"] == "INVALID_JALALI_DATE" for x in r["issues"])


def test_invalid_numeric(tmp_path):
    r = validate_market(market_file(tmp_path, rows=[["1405-08-10", "bad", "3", "1", "60", "SAMAN"]]))
    assert any(x["code"] == "INVALID_NUMERIC" for x in r["issues"])


def test_identical_duplicate_warning(tmp_path):
    row = ["1405-08-10", "20", "3", "1", "60", "SAMAN"]
    r = validate_market(market_file(tmp_path, rows=[row, row]))
    assert any(x["code"] == "IDENTICAL_DUPLICATE" for x in r["issues"])


def test_conflicting_duplicate_fail_closed(tmp_path):
    rows = [["1405-08-10", "20", "3", "1", "60", "SAMAN"], ["1405-08-10", "21", "3", "1", "60", "SAMAN"]]
    r = validate_market(market_file(tmp_path, rows=rows))
    assert r["status"] == "FAIL"


def test_valid_fx_workbook(tmp_path):
    assert validate_fx(fx_file(tmp_path))["validated_rows"] == 1


def test_missing_fx_sell_field(tmp_path):
    r = validate_fx(fx_file(tmp_path, ("تاریخ", "خرید (ریال)")))
    assert any(x["code"] == "FX_MAPPING_NOT_FOUND" for x in r["issues"])


def test_invalid_fx_date_or_rate(tmp_path):
    r = validate_fx(fx_file(tmp_path, rows=[["1405-13-10", 10, "bad"]]))
    assert any(x["code"] == "INVALID_FX_DATE" for x in r["issues"])


def test_free_market_absent(tmp_path):
    assert find_free_market_sample(tmp_path)["code"] == "BLOCKED_NO_SAMPLE"


def test_provenance_timestamps_unknown(tmp_path):
    p = validate_market(market_file(tmp_path))["provenance"]
    assert p["source_published_at"] == p["source_available_at"] == "UNKNOWN"


def test_hash_stability_and_source_immutability(tmp_path):
    p = market_file(tmp_path); before = hashlib.sha256(p.read_bytes()).hexdigest()
    artifact_identity(p); validate_market(p)
    assert hashlib.sha256(p.read_bytes()).hexdigest() == before


def run_cli(root, market, fx, report):
    return subprocess.run([sys.executable, "-m", "src.scripts.market_fx_preflight",
                          "--root", str(root), "--market", str(market), "--fx", str(fx),
                          "--json-out", str(report)], cwd=Path(__file__).resolve().parents[2],
                         text=True, capture_output=True)


def test_cli_runs_and_writes_json(tmp_path):
    m, x = market_file(tmp_path), fx_file(tmp_path)
    (tmp_path / "free_market.csv").write_text("fixture", encoding="utf-8")
    out = tmp_path / "report.json"
    p = run_cli(tmp_path, m, x, out)
    assert p.returncode == 0, p.stdout + p.stderr
    assert json.loads(out.read_text(encoding="utf-8"))["results"][0]["economic_key"]["codal_symbol"] == "SAMAN"
    assert "MarketDaily:" in p.stdout


def test_cli_nonzero_for_blocked_or_fail(tmp_path):
    m = market_file(tmp_path, headers=("J-Date", "Close", "Volume", "No", "Value"),
                    rows=[["1405-08-10", "20", "3", "1", "60"]])
    x, out = fx_file(tmp_path), tmp_path / "blocked.json"
    p = run_cli(tmp_path, m, x, out)
    assert p.returncode == 1
    assert json.loads(out.read_text(encoding="utf-8"))["overall_status"] == "BLOCKED"


def test_ticker_is_codal_symbol_key(tmp_path):
    result = validate_market(market_file(tmp_path))
    assert result["economic_key"]["codal_symbol"] == "SAMAN"


def test_missing_ticker_does_not_skip_row_validation(tmp_path):
    p = market_file(tmp_path, headers=("J-Date", "Close", "Volume", "No", "Value"),
                    rows=[["bad-date", "bad", "", "1", "60"]])
    result = validate_market(p)
    codes = [i["code"] for i in result["issues"]]
    assert "CODAL_SYMBOL_MISSING" in codes
    assert "INVALID_JALALI_DATE" in codes and "INVALID_NUMERIC" in codes
    assert result["validated_rows"] == 1


def test_inconsistent_tickers_block_economic_keys(tmp_path):
    rows = [["1405-08-10", "20", "3", "1", "60", "A"],
            ["1405-08-11", "21", "3", "1", "63", "B"]]
    result = validate_market(market_file(tmp_path, rows=rows))
    assert any(i["code"] == "CODAL_SYMBOL_INCONSISTENT" for i in result["issues"])
    assert result["validated_rows"] == 2


def test_malformed_csv_row_width_is_detected(tmp_path):
    p = market_file(tmp_path, rows=[["1405-08-10", "20", "3", "1", "60", "SAMAN", "EXTRA"]])
    assert any(i["code"] == "CSV_ROW_WIDTH" for i in validate_market(p)["issues"])


def test_fx_duplicate_across_worksheets_detected(tmp_path):
    p = tmp_path / "cross_sheet.xlsx"; wb = Workbook(); ws1 = wb.active; ws1.title = "One"
    ws1.append(["تاریخ", "فروش (ریال)"]); ws1.append(["1405-08-10", 200])
    ws2 = wb.create_sheet("Two"); ws2.append(["تاریخ", "فروش (ریال)"]); ws2.append(["1405-08-10", 201])
    wb.save(p)
    result = validate_fx(p)
    issue = next(i for i in result["issues"] if i["code"] == "CONFLICTING_DUPLICATE")
    assert "One!A2/B2" in issue["message"] and "Two!A2/B2" in issue["message"]


def test_source_artifacts_unchanged_after_cli(tmp_path):
    m, x = market_file(tmp_path), fx_file(tmp_path)
    before = [hashlib.sha256(p.read_bytes()).hexdigest() for p in (m, x)]
    (tmp_path / "free_market.csv").write_text("fixture", encoding="utf-8")
    run_cli(tmp_path, m, x, tmp_path / "out.json")
    after = [hashlib.sha256(p.read_bytes()).hexdigest() for p in (m, x)]
    assert before == after
