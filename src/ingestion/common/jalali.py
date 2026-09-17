"""Minimal Jalali (Persian) \u2194 Gregorian date conversion.

No external dependency (jdatetime) to keep CI surface minimal.
Algorithm based on the standard astronomical conversion used by Iranian systems.
"""

from __future__ import annotations

from datetime import date


def jalali_to_gregorian(jy: int, jm: int, jd: int) -> date:
    """Convert Jalali year/month/day to Gregorian date.

    Raises ValueError on obviously invalid inputs.
    """
    if not (1 <= jm <= 12):
        raise ValueError(f"Invalid Jalali month: {jm}")
    if not (1 <= jd <= 31):
        raise ValueError(f"Invalid Jalali day: {jd}")

    jy -= 979
    days = 365 * jy + (jy // 33) * 8 + ((jy % 33) + 3) // 4
    for i in range(1, jm):
        days += 31 if i <= 6 else 30
    days += jd - 1

    g_days = days + 79

    gy = 1600 + 400 * (g_days // 146097)
    g_days %= 146097

    leap = True
    if g_days >= 36525:
        g_days -= 1
        gy += 100 * (g_days // 36524)
        g_days %= 36524
        if g_days >= 365:
            g_days += 1
        else:
            leap = False

    gy += 4 * (g_days // 1461)
    g_days %= 1461

    if g_days >= 366:
        leap = False
        g_days -= 1
        gy += g_days // 365
        g_days %= 365

    gd = g_days + 1
    sal_a = [0, 31, 29 if leap else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    gm = 1
    while gm < 13 and gd > sal_a[gm]:
        gd -= sal_a[gm]
        gm += 1

    return date(gy, gm, gd)


def parse_jalali_date(s: str) -> date:
    """Parse 'YYYY-MM-DD' or 'YYYY/MM/DD' Jalali string to Gregorian date."""
    s = s.strip().replace("/", "-")
    parts = s.split("-")
    if len(parts) != 3:
        raise ValueError(f"Invalid Jalali date format: {s!r}")
    jy, jm, jd = int(parts[0]), int(parts[1]), int(parts[2])
    return jalali_to_gregorian(jy, jm, jd)
