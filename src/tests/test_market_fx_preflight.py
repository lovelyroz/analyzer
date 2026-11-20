import csv
import hashlib
from pathlib import Path

from openpyxl import Workbook

from src.preflight.market_fx import validate_market, validate_fx, find_free_market_sample, artifact_identity


def market_file(tmp_path, headers=("J-Date", "Close", "Volume", "No", "Value"), rows=None):
    p = tmp_path / "market.csv"
    with p.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f); w.writerow(headers)
        for row in rows or [["1405-08-10", "20", "3", "1", "60"]]: w.writerow(row)
    return p


def fx_file(tmp_path, headers=("تاریخ", "خرید (ریال)", "فروش (ریال)"), rows=None):
    p = tmp_path / "fx.xlsx"; wb = Workbook(); ws = wb.active
    ws.append(headers)
    for row in rows or [["1405-08-10", 100, 200]]: ws.append(row)
    wb.save(p); return p


def test_valid_market_daily(tmp_path):
    assert validate_market(market_file(tmp_path), "company-1")["status"] == "WARNING"  # provenance gap


def test_missing_market_field(tmp_path):
    r = validate_market(market_file(tmp_path, ("J-Date", "Close")), "company-1")
    assert any(x["code"] == "MISSING_REQUIRED_FIELDS" for x in r["issues"])


def test_invalid_jalali_date(tmp_path):
    r = validate_market(market_file(tmp_path, rows=[["1405-13-10", "20", "3", "1", "60"]]), "company-1")
    assert any(x["code"] == "INVALID_JALALI_DATE" for x in r["issues"])


def test_invalid_numeric(tmp_path):
    r = validate_market(market_file(tmp_path, rows=[["1405-08-10", "bad", "3", "1", "60"]]), "company-1")
    assert any(x["code"] == "INVALID_NUMERIC" for x in r["issues"])


def test_identical_duplicate_warning(tmp_path):
    row = ["1405-08-10", "20", "3", "1", "60"]
    r = validate_market(market_file(tmp_path, rows=[row, row]), "company-1")
    assert any(x["code"] == "IDENTICAL_DUPLICATE" for x in r["issues"])


def test_conflicting_duplicate_fail_closed(tmp_path):
    rows = [["1405-08-10", "20", "3", "1", "60"], ["1405-08-10", "21", "3", "1", "60"]]
    r = validate_market(market_file(tmp_path, rows=rows), "company-1")
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
    p = validate_market(market_file(tmp_path), "company-1")["provenance"]
    assert p["source_published_at"] == p["source_available_at"] == "UNKNOWN"


def test_hash_stability_and_source_immutability(tmp_path):
    p = market_file(tmp_path); before = hashlib.sha256(p.read_bytes()).hexdigest()
    artifact_identity(p); validate_market(p, "company-1")
    assert hashlib.sha256(p.read_bytes()).hexdigest() == before
