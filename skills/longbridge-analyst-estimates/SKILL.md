---
name: longbridge-analyst-estimates
description: |
  Analyst EPS estimate time series for a listed stock via Longbridge — tracks how the consensus EPS forecast (high / low / mean / median / analyst count) has changed over time, and shows actual values where reported. Answers "have analysts been raising or cutting their estimates?" Complements longbridge-consensus (current snapshot) by focusing on the historical revision trajectory. Triggers: "分析师预测历史", "EPS预测趋势", "一致预期变化", "预期上调下调", "分析师预期轨迹", "分析师EPS", "预测时间序列", "分析師預測歷史", "EPS預測趨勢", "一致預期變化", "預期上調下調", "分析師EPS", "analyst estimate history", "EPS estimate trend", "consensus revision history", "estimate time series", "analyst forecast trajectory", "EPS upgrade downgrade history".
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

# longbridge-analyst-estimates

Prompt-only skill. Fetches the **historical EPS estimate time series** for a stock — each data point shows what analysts collectively expected at that moment in time (high / low / mean / median / count) plus the reported actual when available.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

- *"TSLA 分析师预期一年来怎么变化的"*, *"TSLA analyst estimates over the past year"*, *"TSLA 分析師預期一年來怎麼變化"*
- *"NVDA EPS 预期有没有被上调"*, *"has NVDA EPS estimate been revised up?"*, *"NVDA EPS 預期有沒有被上調"*
- *"苹果最近分析师是在下调还是上调预期"*, *"are analysts cutting or raising AAPL estimates"*
- *"700.HK 历史一致预期"*, *"700.HK consensus estimate history"*

For the **current** consensus snapshot (not the history) → `longbridge-consensus`.  
For beat/miss analysis and PEAD signals → `longbridge-consensus` (which also calls `analyst-estimates`).  
For full fundamentals → `longbridge-fundamental`.

## CLI

Run `longbridge analyst-estimates --help` to verify exact flags. Primary call:

```bash
# Full estimate time series for a symbol
longbridge analyst-estimates TSLA.US --format json
longbridge analyst-estimates 700.HK --format json

# Help — always verify flags before use
longbridge analyst-estimates --help
```

If the user asks for a specific period type (annual / quarterly) or fiscal year, check `--help` for the relevant flag and pass it. If unsure, omit and use the default.

## Workflow

1. **Resolve symbol** to `<CODE>.<MARKET>` format.
2. **Run** `longbridge analyst-estimates <SYMBOL> --format json`.
3. **Parse** the returned array. Each element typically contains:

   | Field | Description |
   |---|---|
   | `day` | Data point date |
   | `high` | Highest analyst estimate |
   | `low` | Lowest analyst estimate |
   | `mean` | Consensus mean estimate |
   | `median` | Consensus median estimate |
   | `num` | Number of analysts contributing |
   | `currency` | Estimate currency |
   | `value` | Actual reported value (null if not yet reported) |

4. **Identify trend**:
   - Direction of `mean` over time: rising (upgrades) / flat / falling (downgrades).
   - Spread (`high − low`): narrowing = greater consensus; widening = diverging views.
   - `num` changes: cover expansion or contraction.
   - Where `value` is present: compute surprise `(value − mean) / |mean| × 100%`.
5. **Present** as a table + trend narrative; note the reporting currency.

## Output

**TSLA.US — Analyst EPS estimate history**  
Source: Longbridge Securities

```
Date       | High  | Mean  | Median | Low   | Analysts | Actual | Surprise
2024-10-31 | 0.95  | 0.75  | 0.76   | 0.52  |    34    | 0.72   | −4.0%
2025-01-31 | 1.12  | 0.88  | 0.89   | 0.61  |    36    | —      | —
2025-04-30 | 1.25  | 0.97  | 0.98   | 0.70  |    37    | —      | —
…
```

*Trend*: Mean EPS estimates have risen +29% over 6 months (0.75 → 0.97); analyst count expanded from 34 to 37 — consistent upgrade cycle.

⚠️ 分析师预测仅供参考，不构成投资建议。  
⚠️ 分析師預測僅供參考，不構成投資建議。  
⚠️ Analyst estimates are for reference only. Not investment advice.

## Error handling

| Situation | 简体中文回复 | 繁體中文 / English |
|---|---|---|
| `command not found: longbridge` | 回退到 MCP；如也不可用，请安装 longbridge-terminal。 | 回退到 MCP；如也不可用，請安裝 longbridge-terminal。/ Fall back to MCP; if unavailable, install longbridge-terminal. |
| Returns empty array | "{symbol} 暂无分析师预期历史数据。" | "{symbol} 暫無分析師預期歷史數據。" / "{symbol} has no analyst estimate history." |
| `num` < 3 across all points | 覆盖分析师不足 3 位，预测可靠性较低，请谨慎参考。 | 覆蓋分析師不足 3 位，可靠性較低。/ Fewer than 3 analysts — estimates are indicative only. |
| Other stderr | 直接显示原始错误，不静默重试。 | 顯示原始錯誤。/ Surface verbatim — do not retry silently. |

## MCP fallback

If `longbridge` CLI is unavailable (`command not found`), use MCP tools:

When the CLI is unavailable, fall back to the MCP server. Discover available tools from the MCP server's tool list at runtime — do not rely on hardcoded tool names.

MCP setup: `claude mcp add --transport http longbridge https://openapi.longbridge.com/mcp` (`quote` scope).

## Related skills

- Current consensus snapshot (not history) → `longbridge-consensus`
- Beat/miss analysis and PEAD signals → `longbridge-consensus`
- Full fundamentals (revenue / margins / ROE) → `longbridge-fundamental`
- Valuation (PE / PB / industry rank) → `longbridge-valuation`

## File layout

```
longbridge-analyst-estimates/
└── SKILL.md   # prompt-only, no scripts/
```
