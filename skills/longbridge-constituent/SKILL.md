---
name: longbridge-constituent
description: |
  Constituent stocks of an index or ETF via Longbridge Securities — list members of HSI / SPX / DJI / IXIC / CSI300 / a sector ETF, sortable by change, price, turnover, capital inflow, turnover-rate, or market cap. Returns a ranked roster, never a buy/sell call. Triggers: "标普500有哪些", "标普成分股", "恒生成分股", "纳斯达克成分", "道琼斯成分", "沪深300成分", "ETF 持仓", "ETF 成分股", "指数成分", "成分股涨幅榜", "標普500成分", "恒生成分股", "納斯達克成分", "道瓊成分", "滬深300成分", "ETF 持倉", "ETF 成分股", "指數成分", "成分股漲幅榜", "S&P 500 constituents", "Hang Seng constituents", "IXIC components", "Dow components", "CSI 300 members", "ETF holdings", "ETF constituents", "index members", "what's in SPX", "what's in HSI", "HSI.HK", "SPX.US", "IXIC.US", "DJI.US", "000300.SH".
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: read_only
  requires_login: false
  default_install: true
---

# longbridge-constituent

List the constituent stocks of an index or ETF, ranked by a chosen indicator.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

Trigger when the user wants the **members** of an index or ETF (not the index quote itself):

- *"标普 500 有哪些股票"*, *"S&P 500 constituents"* → `SPX.US`
- *"恒生指数成分股"*, *"Hang Seng constituents"* → `HSI.HK`
- *"纳斯达克 100 涨幅榜"*, *"IXIC components by gain"* → `IXIC.US`
- *"沪深 300 成分股"*, *"CSI 300 members"* → `000300.SH`
- *"QQQ 持仓"*, *"SPY holdings"* → ETF symbol like `QQQ.US`, `SPY.US`

For the index *quote* (level, change, volume), use `longbridge-quote` instead. For 2–5 explicit-symbol comparison, use `longbridge-peer-comparison`.

## Symbol format

`<CODE>.<MARKET>`. Common indices:

| Index | Symbol |
|---|---|
| 恒生指数 / Hang Seng | `HSI.HK` |
| 国企指数 / HSCEI | `HSCEI.HK` |
| 标普 500 / S&P 500 | `SPX.US` |
| 道琼斯 / Dow Jones | `DJI.US` |
| 纳斯达克综合 / Nasdaq | `IXIC.US` |
| 纳指 100 / Nasdaq 100 | `NDX.US` |
| 沪深 300 / CSI 300 | `000300.SH` |
| 上证指数 / SSE Composite | `000001.SH` |

ETFs use their own ticker (e.g. `SPY.US`, `QQQ.US`, `2800.HK`).

## Subcommand

> Single CLI command. Run `longbridge constituent --help` if unsure of current flags.

```bash
longbridge constituent <SYMBOL> [--limit N] [--sort INDICATOR] [--order desc|asc] --format json
```

| Flag | Default | Notes |
|---|---|---|
| `--limit` | `50` | Number of members to return |
| `--sort` | `change` | `change` / `price` / `turnover` / `inflow` / `turnover-rate` / `market-cap` |
| `--order` | `desc` | `desc` / `asc` |

## Workflow

1. Resolve the user's index/ETF name to `<CODE>.<MARKET>` (use the table above; if ambiguous between markets, ask).
2. Pick `--sort` from intent:
   - "涨幅榜 / gainers" → `--sort change --order desc`
   - "跌幅榜 / losers" → `--sort change --order asc`
   - "成交活跃 / most traded" → `--sort turnover`
   - "主力净流入 / net inflow" → `--sort inflow`
   - "权重股 / largest weight" → `--sort market-cap`
3. Pick `--limit`: default 50 unless user specifies (e.g. "前 10" → `--limit 10`).
4. Run `longbridge constituent ... --format json`, render the rows in a table.

## CLI examples

```bash
longbridge constituent HSI.HK                                     --format json
longbridge constituent HSI.HK --limit 20 --sort change            --format json
longbridge constituent SPX.US --sort market-cap --limit 10        --format json
longbridge constituent IXIC.US --sort inflow --order desc         --format json
longbridge constituent 000300.SH --sort turnover --limit 30       --format json
longbridge constituent QQQ.US                                     --format json
```

## Output

JSON array, one row per constituent — fields typically include `symbol`, `name`, `last`, `change_rate`, `volume`, `turnover`, `market_cap`, plus the indicator used for sorting. Render as a 5–8 column table; preserve `symbol` verbatim.

## Error handling

| Situation | LLM response |
|---|---|
| Shell `command not found: longbridge` | Fall back to MCP if configured; otherwise tell the user to install longbridge-terminal. |
| stderr `param_error` / "invalid symbol" | Confirm the index symbol — e.g. `SPX.US` not `S&P500`. |
| Empty array | "No constituents returned — confirm the symbol is an index or ETF, not a single stock." |
| Other stderr | Surface verbatim. |

## MCP fallback

| CLI subcommand | MCP tool |
|---|---|
| `constituent <SYMBOL>` | `mcp__longbridge__index_constituents` (or fall back via the equivalent MCP tool) |

If unsure of the exact MCP tool name, run the CLI; the binary is the canonical path.

## Related skills

| User asks | Route to |
|---|---|
| Index level / change / volume | `longbridge-quote` |
| 2–5 explicit-symbol comparison | `longbridge-peer-comparison` |
| Single-stock fundamentals after picking from the list | `longbridge-fundamental` |
| Single-stock valuation snapshot | `longbridge-valuation` |

## File layout

```
longbridge-constituent/
└── SKILL.md          # prompt-only, no scripts/
```
