---
name: longbridge-depth
description: |
  Orderbook depth (5/10-level bid/ask), broker queue (HK only), and tick-by-tick trades for stocks via Longbridge Securities. Use for orderbook microstructure questions. Triggers: "盘口", "买卖盘", "5 档", "10 档", "深度", "经纪商队列", "逐笔", "tick", "成交明细", "盤口", "買賣盤", "5 檔", "10 檔", "經紀商隊列", "逐筆", "成交明細", "depth", "orderbook", "level 2", "broker queue", "tick data", "trades", "time and sales".
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: read_only
  requires_login: false
  default_install: true
---

# longbridge-depth

Orderbook depth, broker queue (HK-only), and tick-by-tick trades.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## Subcommands

| Subcommand | Returns |
|---|---|
| `depth` | 5/10-level orderbook: per-level price / volume / order_num |
| `brokers` | Per-level broker_id queue (**HK only**). For non-HK symbols, tell the user this is unavailable. |
| `trades` | Latest N trades: time / price / volume / direction / type. `--count 1..1000`. |
| `all` | depth + brokers (if HK) + trades, in one call. |

`broker_id` integers can be translated to names via `longbridge-security-list` → `participants`.

## When to use

- *"看下 700.HK 的盘口"*, *"TSLA 5 档买卖盘"* → `depth`
- *"茅台经纪商队列"* — non-HK symbol → tell user *"broker queue is HK-only"* and switch to `depth`
- *"NVDA 最近 50 笔成交"*, *"腾讯 tick 数据"* → `trades --count 50`
- *"700 全部盘口"*, *"microstructure overview"* → `all`

## Workflow

1. Resolve symbol to `<CODE>.<MARKET>`.
2. Pick subcommand by user intent (table above).
3. **Off-hours warning**: outside trading hours, `depth` is the closing snapshot and `trades` are the last N of the previous session — **call this out explicitly** when responding.
4. Run via local CLI (preferred) or MCP fallback.
5. Render `depth` as a bid/ask table; describe `trades` as direction summary (buy-dominant / sell-dominant) plus the latest few rows. Cite Longbridge Securities.

## CLI

```bash
python3 scripts/cli.py depth   700.HK
python3 scripts/cli.py brokers 700.HK              # HK-only
python3 scripts/cli.py trades  700.HK --count 50
python3 scripts/cli.py all     700.HK
```

## Output

Per-subcommand `datas`:

- `depth` / `brokers`: `{asks: [...], bids: [...]}` (`brokers[i]` includes `broker_id` array)
- `trades`: array (top-level `count`)
- `all`: `{depth, brokers, trades}` (`brokers: null` for non-HK)

## Error handling

Standard envelope. `invalid_input_format` includes the broker-queue HK constraint message.

## MCP fallback

| CLI subcommand | MCP tool |
|---|---|
| `depth` | `mcp__longbridge__depth` |
| `brokers` | `mcp__longbridge__brokers` |
| `trades` | `mcp__longbridge__trades` |
| `all` | call the above three sequentially and merge in the LLM (no combined MCP tool) |

MCP-only extensions: `mcp__longbridge__short_positions`, `mcp__longbridge__option_volume`, `mcp__longbridge__option_volume_daily`.

## Related skills

- Quote / static / indices → `longbridge-quote`
- Capital flow / large-order distribution → `longbridge-capital-flow`
- Broker_id → name lookup → `longbridge-security-list`

## File layout

```
longbridge-depth/
├── SKILL.md
└── scripts/
    ├── cli.py
    └── test_cli.py
```
