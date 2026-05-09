---
name: longbridge-market-microstructure
description: |
  Market microstructure analysis via Longbridge Securities — bid-ask spread, order-flow toxicity (large-order pressure), liquidity depth, price impact, and institutional order direction. Covers A-share call-auction analysis and HK block-trade mechanics. Triggers: "盘口分析", "微观结构", "订单流", "大单分析", "买卖价差", "逐笔分析", "买卖盘深度", "挂单墙", "主力动向", "集合竞价", "盤口分析", "微觀結構", "訂單流", "大單分析", "買賣價差", "逐筆分析", "買賣盤深度", "掛單牆", "主力動向", "market microstructure", "order flow", "bid-ask spread", "depth analysis", "large order", "order book imbalance", "price impact", "auction analysis", "institutional order flow".
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: read_only
  requires_login: false
  default_install: true
  requires_mcp: false
  tier: read
---

# longbridge-market-microstructure

Combines orderbook depth, tick-by-tick trades, and capital-flow data to assess bid-ask spread, order-flow imbalance, liquidity depth, and short-term institutional pressure for a single symbol.

> **Response language**: match the user's input language —
> Simplified Chinese / Traditional Chinese / English.

## When to use

- *"TSLA 盘口分析"*, *"NVDA order flow"*, *"700.HK 买卖盘深度"* → full microstructure report
- *"挂单墙在哪里"*, *"order book imbalance"* → depth-only analysis (`depth`)
- *"大单主力方向"*, *"institutional order flow"* → trades + capital combined
- *"集合竞价分析"* (A-share pre-open auction) → depth + trades during auction session
- *"港股大宗交易"* (HK block trades) → trades with type filter + brokers queue

Do **not** use this skill for historical (multi-day) flow analysis — route to `longbridge-capital-flow` or `longbridge-kline`.

## Workflow

1. Resolve the user's symbol to `<CODE>.<MARKET>` (e.g. `NVDA.US`, `700.HK`, `600519.SH`).
2. Run `longbridge depth --help` and `longbridge trades --help` to confirm current flag names.
3. Fetch **orderbook depth** with `longbridge depth <SYMBOL> --format json`.
4. Fetch **recent tick trades** (last 100) with `longbridge trades <SYMBOL> --count 100 --format json`.
5. Fetch **capital-flow distribution** (large / medium / small orders) with `longbridge capital <SYMBOL> --format json`.
6. For **HK symbols only**, also fetch `longbridge brokers <SYMBOL> --format json` to identify large broker queues (potential institutional blocks).
7. Compute or estimate:
   - **Weighted bid-ask spread** = (best_ask − best_bid) / mid_price
   - **Depth asymmetry** = (total_bid_volume − total_ask_volume) / (total_bid_volume + total_ask_volume) across all levels
   - **Buy-initiated ratio** = buy-side active trades / total trades (from tick data)
   - **Large-order net pressure** = large_buy_amount − large_sell_amount (from capital snapshot)
   - **Order-wall levels** = price levels with volume ≥ 3× average level volume (potential support/resistance)
8. Output a structured microstructure report (see Output section).

## CLI

```bash
# Confirm current flags before use
longbridge depth --help
longbridge trades --help
longbridge capital --help
longbridge brokers --help

# Orderbook depth (5/10-level bid/ask)
longbridge depth NVDA.US --format json

# Recent 100 tick trades
longbridge trades NVDA.US --count 100 --format json

# Capital flow (large/medium/small order distribution)
longbridge capital NVDA.US --format json

# Broker queue — HK symbols only
longbridge brokers 700.HK --format json
```

## Output

Render a structured report with these sections:

| Section | 简体 | 繁體 | English |
|---|---|---|---|
| Spread & liquidity | 价差与流动性 | 價差與流動性 | Spread & Liquidity |
| Depth asymmetry | 盘口不对称 | 盤口不對稱 | Depth Asymmetry |
| Order-flow pressure | 订单流压力 | 訂單流壓力 | Order-Flow Pressure |
| Order walls | 挂单墙 | 掛單牆 | Order Walls |
| Direction bias | 短线方向偏向 | 短線方向偏向 | Short-Term Directional Bias |

Key field translations (LLM maps JSON keys → user language):

| Field | 简体 | 繁體 | English |
|---|---|---|---|
| `asks / bids` | 卖盘 / 买盘 | 賣盤 / 買盤 | Ask / Bid |
| `price / volume / order_num` | 价格 / 数量 / 委托笔数 | 價格 / 數量 / 委託筆數 | Price / Volume / Order count |
| `direction` | 方向（主买/主卖） | 方向（主買/主賣） | Direction (buy/sell initiated) |
| `large_in / large_out` | 大单流入 / 流出 | 大單流入 / 流出 | Large order in/out |

**Off-hours caveat**: outside regular trading hours, depth is a closing snapshot and trades are from the prior session — state this explicitly.

**A-share call-auction note**: during 09:15–09:25 CST (pre-open), depth reflects indicative auction prices, not continuous quotes. Mention this when the user's query occurs in that window.

**HK block trades**: trades with `type = block` or large-volume single prints may indicate off-exchange block deals — highlight these separately.

## Error handling

| Situation | 简体回复 | 繁體回復 | English reply |
|---|---|---|---|
| `command not found: longbridge` | 请安装 longbridge-terminal，或使用 MCP 回退 | 請安裝 longbridge-terminal，或使用 MCP 回退 | Install longbridge-terminal or use MCP fallback |
| stderr `not logged in` | 请运行 `longbridge auth login` | 請執行 `longbridge auth login` | Run `longbridge auth login` |
| `brokers` on non-HK symbol | 经纪商队列仅支持港股 | 經紀商隊列僅支援港股 | Broker queue is HK-only |
| Other stderr | 原样转述，不静默重试 | 原樣轉述，不靜默重試 | Relay verbatim, no silent retry |

## MCP fallback

| CLI subcommand | MCP tool |
|---|---|
| `depth` | `mcp__longbridge__depth` |
| `trades` | `mcp__longbridge__trades` |
| `brokers` | `mcp__longbridge__brokers` |
| `capital` | `mcp__longbridge__capital_distribution` |

## Related skills

| Skill | Why |
|---|---|
| `longbridge-depth` | Raw orderbook / tick data without microstructure analysis layer |
| `longbridge-capital-flow` | Intraday capital-flow time series and order-size distribution |
| `longbridge-anomaly` | Unusual price/volume movements and trade-statistics profile |
| `longbridge-quote` | Real-time price, volume, and valuation indices |

## File layout

```
longbridge-market-microstructure/
└── SKILL.md          # prompt-only, no scripts/
```
