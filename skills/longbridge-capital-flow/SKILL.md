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

| Flag | Returns |
|---|---|
| (default) | `flow`: today's main-capital net inflow/outflow time series |
| `--include-dist` | adds `distribution`: cross-section of large / medium / small / super-large order buy & sell amounts |

**Single symbol per call** (the underlying CLI is per-symbol). Today's data only — no historical range.

## When to use

- *"今天 NVDA 主力净流入"*, *"今日資金流"* → default flow
- *"看下 TSLA 大单分布"*, *"大單/中單/小單"* → add `--include-dist`
- *"看一下 700 资金面"* (combined) → `--include-dist`
- *"过去 30 天资金流"* → unsupported, redirect to `longbridge-kline` (volume) or `longbridge-quote --index volume`
- *"今天哪些股票主力大幅流入"* (screener) → unsupported; ask user for a specific symbol

## Workflow

1. Resolve a single symbol to `<CODE>.<MARKET>`.
2. Decide flag: default (flow only) or `--include-dist` (flow + distribution).
3. Run via local CLI (preferred) or MCP fallback.
4. Summarise: net inflow direction (▲/▼), accumulated total, distribution skew. Cite Longbridge Securities.

## CLI

```bash
python3 scripts/cli.py -s NVDA.US
python3 scripts/cli.py -s TSLA.US --include-dist
python3 scripts/cli.py -s 600519.SH
```

## Output

```json
{
  "success": true,
  "source": "longbridge",
  "skill": "longbridge-capital-flow",
  "skill_version": "1.0.0",
  "symbol": "TSLA.US",
  "datas": {
    "flow": [ ... ],
    "distribution": { /* only with --include-dist */ }
  }
}
```

Field translations (LLM should map):

| Field (likely) | 简体 | 繁體 | English |
|---|---|---|---|
| `large_in / large_out` | 大单流入/流出 | 大單流入/流出 | Large order in/out |
| `medium_in / medium_out` | 中单流入/流出 | 中單流入/流出 | Medium order in/out |
| `small_in / small_out` | 小单流入/流出 | 小單流入/流出 | Small order in/out |
| `super_in / super_out` | 超大单流入/流出 | 超大單流入/流出 | Super-large order in/out |

(Field names follow Longbridge JSON; `cli.py` does no rewrite.)

## Error handling

Standard envelope. Multiple `-s` flags trigger `invalid_input_format` with hint *"this skill takes one symbol"*.

## MCP fallback

| CLI behaviour | MCP tool |
|---|---|
| default (flow only) | `mcp__longbridge__capital_flow` |
| `--include-dist` | `mcp__longbridge__capital_flow` + `mcp__longbridge__capital_distribution` (LLM merges) |

## Related skills

- Quote / change / volume → `longbridge-quote`
- Candlesticks / volume history → `longbridge-kline`
- Orderbook microstructure → `longbridge-depth`

## File layout

```
longbridge-capital-flow/
├── SKILL.md
└── scripts/
    ├── cli.py
    └── test_cli.py
```
