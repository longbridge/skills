---
name: longbridge-market-temp
description: |
  Market-level state from Longbridge Securities — market temperature index (0–100, higher = more bullish), trading session times (open/close), and the trading day calendar (with half-days). Triggers: "今天开盘吗", "今天美股开市吗", "几点开盘", "下个交易日", "市场情绪", "牛熊度数", "温度计", "市场温度", "今天開盤嗎", "幾點開盤", "下個交易日", "市場情緒", "溫度計", "is the market open", "trading hours", "next trading day", "market temperature", "market sentiment".
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: read_only
  requires_login: false
  default_install: true
---

# longbridge-market-temp

Market-level state: open/close, calendar, sentiment temperature. Symbol-level questions belong in `longbridge-quote`.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## Subcommands

| Subcommand | Returns |
|---|---|
| `temp` | Today's market temperature (0–100). With `--history --start --end`, returns the time series. |
| `session` | Trading sessions for all markets (open / close times). |
| `days` | Trading day calendar for `--market HK | US | CN | SG`, optional `--start` / `--end`. |

## Market mapping

LLM maps colloquial names to `--market`:

| User says | `--market` |
|---|---|
| 美股 / US / Nasdaq / S&P / Dow | `US` |
| 港股 / HK / Hang Seng / 恒生 | `HK` |
| A 股 / 沪 / 深 / 上证 / 深证 / SH / SZ | `CN` |
| 新加坡 / SG / Straits / 海峡 | `SG` |

`session` does not need `--market`; it returns all markets.

## When to use

- *"今天美股开盘了吗"*, *"is HK open?"* — combine `session` + local time inference (US = UTC-5/-4 DST, HK/CN/SG = UTC+8)
- *"几点开盘"* → `session`
- *"下个交易日"*, *"this week's trading days"* → `days`
- *"圣诞节港股开市吗"* → `days --market HK --start <Christmas> --end <Christmas>`
- *"市场情绪"*, *"温度多少"* → `temp --market <X>`
- *"今年港股市场情绪走势"* → `temp --market HK --history --start ... --end ...`

## Workflow

1. Pick subcommand (table above).
2. Resolve `--market` if needed.
3. For "is the market open?" — call `session`, then reason against current local time and the user's target market.
4. Run via local CLI (preferred) or MCP fallback.
5. Translate `temp` value into wording: 0–30 *偏空*, 30–50 *中性偏空*, 50–70 *中性偏多*, 70–100 *偏多* (translate into user's language).

## CLI

```bash
python3 scripts/cli.py temp    --market HK
python3 scripts/cli.py session
python3 scripts/cli.py days    --market US --start 2026-04-28 --end 2026-05-31
python3 scripts/cli.py temp    --market HK --history --start 2026-01-01 --end 2026-04-28
```

## Output

`success / source / skill / skill_version / subcommand`, plus:

- `temp`: `market` + `datas` (snapshot object); with `--history`, additional `start / end`, `datas` is an array.
- `session`: `datas` is an array spanning all markets.
- `days`: `market` + `datas` `{trading_days, half_trading_days}`.

## MCP fallback

| CLI subcommand | MCP tool |
|---|---|
| `temp` (snapshot) | `mcp__longbridge__market_temperature` |
| `temp --history` | `mcp__longbridge__history_market_temperature` |
| `session` | `mcp__longbridge__trading_session` |
| `days` | `mcp__longbridge__trading_days` |

MCP-only extensions: `mcp__longbridge__market_status` (finer state), `mcp__longbridge__finance_calendar` (earnings / dividends / IPO / macro).

## Related skills

- Single-stock quote / status → `longbridge-quote`
- Earnings calendar / IPO / macro events → use `mcp__longbridge__finance_calendar` directly

## File layout

```
longbridge-market-temp/
├── SKILL.md
└── scripts/
    ├── cli.py
    └── test_cli.py
```
