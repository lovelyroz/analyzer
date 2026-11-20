import csv
from decimal import Decimal

from openpyxl import Workbook

from src.ingestion.market.adapter import load_ohlc_csv_rows
from src.ingestion.fx.adapter import parse_fx_xlsx
from src.preflight.market_fx import validate_fx


def test_market_allowlist_ignores_ohlc_and_final(tmp_path):
    path = tmp_path / "market.csv"
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["J-Date", "Ticker", "Open", "High", "Low", "Close", "Final", "Volume", "No", "Value"])
        w.writerow(["1405-08-10", "SAMAN", "bad", "bad", "bad", "20", "999", "3", "1", "60"])
    result = load_ohlc_csv_rows(path)
    assert not result.errors
    assert len(result.rows) == 1
    row = result.rows[0]
    assert row.close_price == Decimal("20") and row.volume == 3 and row.trade_count == 1
    assert row.value == Decimal("60")
    assert row.open_price is row.high_price is row.low_price is row.adjusted_close is None


def make_fx(tmp_path, records):
    path = tmp_path / "rates.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.append(["Daily USD exchange rates"])
    ws.append(["note"])
    ws.append(["\u062a\u0627\u0631\u06cc\u062e", "\u062e\u0631\u06cc\u062f (\u0631\u06cc\u0627\u0644)", "\u0641\u0631\u0648\u0634 (\u0631\u06cc\u0627\u0644)"])
    for record in records:
        ws.append(record)
    wb.save(path)
    return path


def test_fx_shared_header_parser_selects_sell_and_free_market_x10(tmp_path):
    path = make_fx(tmp_path, [["1405-08-10", 90, 100]])
    free = parse_fx_xlsx(path, rate_type="FREE_MARKET")
    exchange = parse_fx_xlsx(path, rate_type="EXCHANGE_CENTER")
    assert not free["errors"] and not exchange["errors"]
    assert free["inputs"][0].rate == Decimal("1000")
    assert exchange["inputs"][0].rate == Decimal("100")
    assert free["mappings"][0]["sell_column"] == 3
    report = validate_fx(path, rate_type="FREE_MARKET")
    assert report["observations"][0]["source_sell_rate"] == "100"
    assert report["observations"][0]["canonical_rate"] == "1000"


def test_identical_fx_duplicate_is_warning_not_conflict(tmp_path):
    path = make_fx(tmp_path, [["1405-08-10", 90, 100], ["1405-08-10", 90, 100]])
    report = validate_fx(path, rate_type="EXCHANGE_CENTER")
    duplicate = next(i for i in report["issues"] if i["code"] == "IDENTICAL_DUPLICATE")
    assert duplicate["severity"] == "WARNING"
    assert not any(i["code"] == "CONFLICTING_DUPLICATE" for i in report["issues"])


def test_fx_invalid_and_conflicting_duplicate_are_reported(tmp_path):
    path = make_fx(tmp_path, [["bad", 1, 2], ["1405-08-10", 1, 2], ["1405-08-10", 1, 3]])
    result = parse_fx_xlsx(path, rate_type="EXCHANGE_CENTER")
    assert len(result["inputs"]) == 1
    assert any("invalid Jalali date" in e for e in result["errors"])
    assert any("conflicting duplicate" in e for e in result["errors"])
