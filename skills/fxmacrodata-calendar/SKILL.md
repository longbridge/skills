---
name: fxmacrodata-calendar
description: Fetch official-source macro release-calendar rows from FXMacroData for CPI, payrolls, GDP, PCE, retail sales, PMI, and central-bank decision risk checks. Use when a market, portfolio, or strategy question needs upcoming or historical macro event timing.
license: MIT
---

# FXMacroData Calendar

Use this skill when a market or strategy workflow needs official-source macro event timing. It fetches release-calendar rows from FXMacroData and is useful for:

- upcoming CPI, payrolls, GDP, PCE, retail sales, PMI, and central-bank decision checks
- filtering trades or backtests around known macro events
- explaining why a symbol, sector, or currency pair may face event risk on a date

## Endpoint

Public USD calendar rows are available without an API key:

```bash
curl "https://fxmacrodata.com/api/v1/calendar/usd?limit=25"
```

For higher limits or non-public access, pass an API key with the `X-API-Key` header or `api_key` query parameter:

```bash
curl \
  -H "X-API-Key: $FXMACRODATA_API_KEY" \
  "https://fxmacrodata.com/api/v1/calendar/eur?limit=50"
```

## Helper Script

The bundled helper prints normalized JSON calendar rows:

```bash
python skills/fxmacrodata-calendar/scripts/fetch_calendar.py --currency usd --limit 25 --min-tier 1
```

Set `FXMACRODATA_API_KEY` when using authenticated access.

## Response Fields

Calendar rows commonly include:

- `release`
- `name`
- `date`
- `announcement_datetime`
- `announcement_datetime_utc`
- `market_tier`
- `top_tier_for_currency`
- `source`
- `source_url`

Prefer `announcement_datetime` or `announcement_datetime_utc` for scheduling. Use `market_tier` to filter high-impact events.
