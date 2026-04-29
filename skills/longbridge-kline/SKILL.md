---
name: longbridge-kline
description: |
  Candlestick / OHLCV data and intraday minute series for stocks listed in HK / US / A-share / Singapore via Longbridge Securities. Supports 1m / 5m / 15m / 30m / 1h / day / week / month / year periods, history by date range, and today's intraday curve. Triggers: "K线", "K 线", "走势", "历史价格", "日K", "月K", "周K", "分时图", "近一周走势", "K線", "走勢", "歷史價格", "日K", "月K", "週K", "分時圖", "candlestick", "candles", "OHLCV", "intraday chart", "price history", "weekly chart", "monthly chart", "1-year chart", "前复权", "前復權", "forward adjusted".
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: read_only
  requires_login: false
  default_install: true
---

# longbridge-kline

Historical candlesticks and today's intraday curve for Longbridge-supported securities (HK / US / A-share / Singapore). Does **not** support options, warrants, or indices — defer to `longbridge-derivatives` (derivatives) or `longbridge-quote` (indices).

> **Response language**: respond in the user's input language — Simplified Chinese, Traditional Chinese, or English.

## Subcommands

| Subcommand | Use when |
|---|---|
| `kline` | Latest N candles (default 100 daily). Periods: `1m / 5m / 15m / 30m / 1h / day / week / month / year`. |
| `history` | OHLCV across an explicit date range (`--start`, `--end`). |
| `intraday` | Today's per-minute curve (price + volume + avg_price). |

Period aliases: `minute=1m`, `hour=1h`, `d/1d=day`, `w=week`, `m/1mo=month`, `y=year`. `--adjust no_adjust` (default) or `forward_adjust` (前复权 / 前復權).

## When to use

- *"NVDA 最近一周走势"*, *"近一年走勢"*, *"AAPL 1-month chart"* → `kline --period day`
- *"TSLA 5 分钟 K"*, *"近 100 根 5 分钟"* → `kline --period 5m --count 100`
- *"今天 700.HK 分时图"*, *"AAPL today's intraday"* → `intraday`
- *"AAPL 2024 年 1-12 月日 K"* (explicit dates) → `history --start --end`
- *"前复权日 K"* → add `--adjust forward_adjust`

## Workflow

1. Resolve symbol to `<CODE>.<MARKET>` (rules in `longbridge-quote`).
2. Pick the subcommand:
   - Has explicit start/end dates → `history`.
   - "Today" / "intraday" → `intraday`.
   - Otherwise → `kline` with sensible defaults (day / 100).
3. Map natural-language windows to (`period`, `count`) — examples: "最近一周" → `day,7`, "最近一年" → `day,252`, "月 K" → `month,100`.
4. Run via local CLI (preferred) or MCP fallback.
5. Translate datasets into prose (range high/low, net move, volume note); use ▲/▼ for direction. Cite Longbridge Securities.

## CLI

```bash
python3 scripts/cli.py kline    NVDA.US --period day --count 100
python3 scripts/cli.py kline    700.HK  --period 5m  --count 100 --adjust forward_adjust
python3 scripts/cli.py history  NVDA.US --start 2025-01-01 --end 2025-12-31
python3 scripts/cli.py intraday 700.HK
```

## Output

```json
{
  "success": true,
  "source": "longbridge",
  "skill": "longbridge-kline",
  "skill_version": "1.0.0",
  "subcommand": "kline",
  "symbol": "NVDA.US",
  "period": "day",
  "count": 100,
  "adjust": "no_adjust",
  "datas": [{"time": "...", "open": "...", "high": "...", "low": "...", "close": "...", "volume": "...", "turnover": "..."}, ...]
}
```

`history` adds `start` / `end`. `intraday`'s `datas[i]` is `{time, price, volume, turnover, avg_price}`.

## Error handling

Standard `error_kind` envelope: `binary_not_found / auth_expired / subprocess_failed / no_input / invalid_input_format`. See `longbridge-quote` for response phrasing.

## MCP fallback

| CLI subcommand | MCP tool |
|---|---|
| `kline` | `mcp__longbridge__candlesticks` |
| `history` | `mcp__longbridge__history_candlesticks_by_offset` or `mcp__longbridge__history_candlesticks_by_date` |
| `intraday` | `mcp__longbridge__intraday` |

## Related skills

- Quote / static / valuation indices → `longbridge-quote`
- Orderbook / brokers / ticks → `longbridge-depth`
- Capital flow → `longbridge-capital-flow`

## File layout

```
longbridge-kline/
├── SKILL.md
└── scripts/
    ├── cli.py
    └── test_cli.py
```
