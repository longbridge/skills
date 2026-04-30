---
name: longbridge-calendar
description: |
  Forward-looking events calendar via Longbridge Securities — earnings (financial / report), dividends, IPOs, macro data releases (with importance star filter), and market closure days. Filter by symbol (max 10), market (HK / US / CN / SG / JP / UK / DE / AU), and date range. Read-only. Triggers: "财报日历", "下周谁财报", "earnings calendar", "除权除息日", "派息日", "ex-dividend", "新股", "IPO 日历", "宏观数据", "非农", "CPI", "PCE", "美联储议息", "FOMC", "财报季", "休市日", "财經日曆", "下週誰財報", "除權除息日", "派息日", "新股", "IPO 日歷", "宏觀數據", "美聯儲", "FOMC", "財報季", "休市日", "earnings calendar", "ex-dividend dates", "IPO calendar", "macro calendar", "FOMC meeting", "CPI release", "non-farm payrolls", "market holidays", "trading closed days".
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: read_only
  requires_login: false
  default_install: true
---

# longbridge-calendar

Forward-looking calendar of corporate and macro events: earnings, dividends, IPOs, macro data, and market closures.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

- *"下周哪些公司财报"*, *"NVDA 下次财报什么时候"*, *"earnings next week"* → `report` (or `financial`)
- *"AAPL 下次除息日"*, *"港股下周派息"*, *"ex-dividend dates"* → `dividend`
- *"下周有什么新股"*, *"美股 IPO 日历"*, *"upcoming IPOs"* → `ipo`
- *"下周非农"*, *"CPI 什么时候"*, *"FOMC 议息"*, *"macro calendar"* → `macrodata` (use `--star 3` for top-importance only)
- *"美股下周休市吗"*, *"market holidays"* → `closed`
- *"下周市场全景"* → call `report` + `dividend` + `macrodata --star 3` concurrently

For a single stock's historical earnings → `longbridge-fundamental`. For watchlist-driven daily briefings → `longbridge-catalyst-radar`.

## Subcommands

> Run `longbridge finance-calendar --help` if unsure of current flags. The CLI's built-in help is the canonical source.

A single command handles all event types:

```
longbridge finance-calendar <EVENT_TYPE> [OPTIONS]
```

| `<EVENT_TYPE>` | Returns |
|---|---|
| `financial` | Financial-period events. |
| `report` | Earnings releases (V2 rule: includes `financial` automatically). |
| `dividend` | Dividend ex-dates / pay-dates. |
| `ipo` | Upcoming initial public offerings. |
| `macrodata` | Macro data releases (CPI / NFP / FOMC / GDP / etc.). Use `--star 1\|2\|3` (repeatable) to filter by importance. |
| `closed` | Market closure days. |

Common options:

| Flag | Meaning |
|---|---|
| `--symbol <SYM>` | Filter by symbol; repeatable up to 10. With `--symbol`, default start date is 3 months ago; without, today. |
| `--market <MKT>` | Filter by market: `HK / US / CN / SG / JP / UK / DE / AU`; repeatable. |
| `--start YYYY-MM-DD` | Start date. Default: today (or 3 months ago when `--symbol` is set). |
| `--end YYYY-MM-DD` | End date. Default: no limit. |
| `--count N` | Max events (default 100). |
| `--star 1\|2\|3` | Macro importance, repeatable. Only effective for `macrodata`. |
| `--next later\|earlier` | Pagination direction (default `later`). |
| `--offset N` | Pagination offset. |
| `--format json\|table` | Output format. |

## Workflow

1. Pick `<EVENT_TYPE>` from the prompt cue.
2. Decide scope: `--symbol` (1–10 specific tickers) and/or `--market` (one or more markets).
3. Decide window: `--start` / `--end`. For "next week" use `--start <today> --end <today+7>`.
4. For macro: add `--star 3` (or 2,3) when the user wants high-impact only.
5. Call the CLI; render a date-grouped table.
6. Cite **Longbridge Securities** and the queried date range.

## CLI

```bash
# Earnings releases for the next 14 days, US + HK
longbridge finance-calendar report --market US --market HK --end 2026-05-12 --format json

# Specific tickers' upcoming earnings
longbridge finance-calendar financial --symbol AAPL.US --symbol TSLA.US --format json

# This month's ex-dividend dates in US
longbridge finance-calendar dividend --market US --format json

# High-importance macro (FOMC / CPI / NFP)
longbridge finance-calendar macrodata --star 3 --format json

# Upcoming IPOs in HK
longbridge finance-calendar ipo --market HK --format json

# Market closure days
longbridge finance-calendar closed --market US --format json
```

If `--help` shows newer flags, follow the help output rather than hard-coding here.

## Output

Render in the user's language. Suggested layouts:

**`report` / `financial`** — table grouped by date: date / time (BMO/AMC if available) / symbol / company name / period / consensus EPS (if returned).

**`dividend`** — table: ex-date / record date / pay date / symbol / amount / currency.

**`ipo`** — table: subscription window / listing date / symbol / company / price range / market.

**`macrodata`** — table: date+time / region / event / importance stars / forecast / previous (when available). Group by date.

**`closed`** — list: date / market / reason (e.g. *"Memorial Day"*, *"中秋节"*).

When a result is empty for the chosen window, say so explicitly and offer to widen the window or check another market.

## Error handling

| Situation | Reply |
|---|---|
| Shell `command not found: longbridge` | Fall back to MCP if configured; otherwise tell the user to install longbridge-terminal. |
| stderr `not logged in` / `unauthorized` | Hint `longbridge auth login` (the calendar is generally public, but auth may be required for some markets). |
| Empty result | State explicitly. Offer to widen the window or remove a filter. |
| Invalid date format | Re-prompt with `YYYY-MM-DD`. |
| Other stderr | Relay verbatim — never silently retry. |

## MCP fallback

When the CLI binary is missing, fall back via the equivalent MCP tool. Tool names typically mirror CLI subcommand names (snake_case).

| CLI usage | MCP tool |
|---|---|
| `finance-calendar <event_type> ...` | `mcp__longbridge__finance_calendar` (event type passed as a parameter) |

If the name above does not resolve, fall back via the equivalent MCP tool when CLI is missing.

## Related skills

| Skill | Why |
|---|---|
| `longbridge-catalyst-radar` | Watchlist-scoped morning/evening briefings layered on this calendar. |
| `longbridge-earnings` | Single-symbol earnings deep-dive once the date arrives. |
| `longbridge-fundamental` | Historical earnings KPIs (the *past* counterpart). |
| `longbridge-news` | Filings and headline reaction around the event. |

## File layout

```
longbridge-calendar/
└── SKILL.md          # prompt-only, no scripts/
```
