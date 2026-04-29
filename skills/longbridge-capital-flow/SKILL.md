---
name: longbridge-capital-flow
description: |
  Intraday capital-flow time series and large/medium/small order distribution for a single stock via Longbridge Securities. Same-day data only (no historical range). Triggers: "资金流向", "主力资金", "净流入", "大单", "中单", "小单", "资金分布", "机构资金", "主力净流入", "資金流向", "主力資金", "淨流入", "大單", "中單", "小單", "資金分佈", "機構資金", "capital flow", "money flow", "net inflow", "large order distribution", "institutional flow".
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: read_only
  requires_login: false
  default_install: true
---

# longbridge-capital-flow

Today's capital flow time-series and order-size distribution for a single security.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## Subcommands

| CLI command | Returns |
|---|---|
| `longbridge capital-flow <SYMBOL> --format json` | Today's main-capital net inflow / outflow time series |
| `longbridge capital-dist <SYMBOL> --format json` | Cross-section: large / medium / small / super-large order buy & sell amounts |

**Single symbol per call.** Today's data only — no historical range.

## When to use

- *"今天 NVDA 主力净流入"*, *"今日資金流"* → `capital-flow` only
- *"看下 TSLA 大单分布"*, *"大單/中單/小單"* → `capital-dist` only
- *"看一下 700 资金面"* (combined) → call both and merge
- *"过去 30 天资金流"* → unsupported, redirect to `longbridge-kline` (volume) or `longbridge-quote` (`--index volume`)
- *"今天哪些股票主力大幅流入"* (screener) → unsupported; ask user for a specific symbol

## Workflow

1. Resolve a single symbol to `<CODE>.<MARKET>`.
2. Decide which subcommand(s) to call: `capital-flow` (time series), `capital-dist` (distribution snapshot), or both.
3. Call the Longbridge CLI directly (preferred) or fall back to MCP.
4. Summarise: net inflow direction (▲ / ▼), accumulated total, distribution skew. Cite Longbridge Securities.

## CLI

```bash
longbridge capital-flow NVDA.US        --format json
longbridge capital-dist TSLA.US        --format json
# Combined view → call both and merge in the LLM
```

## Output

`capital-flow` returns a time-series array; `capital-dist` returns a cross-section object.

Field translations (LLM should map):

| Field (likely) | 简体 | 繁體 | English |
|---|---|---|---|
| `large_in / large_out` | 大单流入/流出 | 大單流入/流出 | Large order in/out |
| `medium_in / medium_out` | 中单流入/流出 | 中單流入/流出 | Medium order in/out |
| `small_in / small_out` | 小单流入/流出 | 小單流入/流出 | Small order in/out |
| `super_in / super_out` | 超大单流入/流出 | 超大單流入/流出 | Super-large order in/out |

(Field names follow Longbridge JSON; LLM maps to the user's language.)

## Error handling

If `longbridge` is missing, fall back to MCP. Other stderr messages get relayed verbatim (auth issues → `longbridge login`; invalid symbol → re-check format).

## MCP fallback

| CLI subcommand | MCP tool |
|---|---|
| `capital-flow` | `mcp__longbridge__capital_flow` |
| `capital-dist` | `mcp__longbridge__capital_distribution` |

## Related skills

- Quote / change / volume → `longbridge-quote`
- Candlesticks / volume history → `longbridge-kline`
- Orderbook microstructure → `longbridge-depth`

## File layout

```
longbridge-capital-flow/
└── SKILL.md          # prompt-only, no scripts/
```
