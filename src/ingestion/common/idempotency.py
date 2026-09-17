"""Idempotency policy notes for Stage 1 ingestion.

Upsert identity is domain-specific:
- MarketDaily Jalali: (company_id, jalali_year, jalali_month, jalali_day)
- FXRate Jalali: (jalali_year, jalali_month, jalali_day, currency_from, currency_to, rate_type)
- FXRate Gregorian: (rate_date, currency_from, currency_to, rate_type)
- Report: codal_tracking_id when present; ReportVersion version_number chain

Lookups live in identity.py; this module documents the contract only.
"""
