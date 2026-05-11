---
name: longbridge-investment-proposal
description: |
  Investment proposal generation via Longbridge Securities — produces a structured investment memo covering: executive summary, company overview, investment thesis (3–5 core points), financial analysis, valuation, catalysts and timeline, risk factors, and position recommendation. Triggers: "投资提案", "投资建议书", "投资报告", "投资摘要", "核心逻辑", "投资理由", "建仓建议", "投資提案", "投資建議書", "投資報告", "投資摘要", "核心邏輯", "建倉建議", "investment proposal", "investment memo", "investment summary", "investment rationale", "position recommendation", "investment case", "buy memo".
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

# longbridge-investment-proposal

Generate a structured investment proposal for a single stock opportunity.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

Trigger on prompts asking for:

- A formal investment memo or proposal — *"帮我写一份 NVDA 的投资提案"*, *"generate an investment memo for TSLA"*
- Investment rationale write-up — *"投资逻辑"*, *"investment case"*, *"建仓建议"*
- Structured buy / hold / sell recommendation — *"position recommendation"*, *"investment summary"*

For post-earnings analysis defer to `longbridge-earnings`. For valuation-only analysis defer to `longbridge-valuation`.

## Workflow

1. Extract the target symbol; normalise to `<CODE>.<MARKET>`.
2. Gather data in parallel:
   - Company profile (name, business, employees, founding, IPO date)
   - Latest financials (revenue, net income, EPS, ROE, gross margin, FCF)
   - Valuation multiples (PE, PB, EV-EBITDA, PEG)
   - Analyst consensus (target price, rating distribution)
   - Recent news and catalysts
3. Synthesise into the proposal structure below.
4. Flag data gaps explicitly rather than fabricating figures.

> If unsure of exact flag names, run `longbridge <subcommand> --help` before proceeding.

## CLI

```bash
# Company profile
longbridge company <SYMBOL> --format json

# Financial statements
longbridge financial-report <SYMBOL> --kind ALL --format json

# Valuation multiples
longbridge valuation <SYMBOL> --format json

# Analyst consensus
longbridge consensus <SYMBOL> --format json

# Recent news
longbridge news <SYMBOL> --format json
```

## Output structure

```
# Investment Proposal: <Company Name> (<SYMBOL>)
Date: <today>

## Executive Summary
One-paragraph verdict: Buy / Hold / Avoid, price target, key thesis.

## Company Overview
Business description, market, employees, listing date.

## Investment Thesis
1. <Core point 1>
2. <Core point 2>
3. <Core point 3>
[4–5 if applicable]

## Financial Analysis
| Metric        | LTM     | YoY Δ |
|---------------|---------|--------|
| Revenue       |         |        |
| Net Income    |         |        |
| EPS           |         |        |
| Gross Margin  |         |        |
| ROE           |         |        |
| FCF           |         |        |

## Valuation
| Multiple   | Current | Industry Median | Assessment |
|------------|---------|-----------------|------------|
| PE         |         |                 |            |
| PB         |         |                 |            |
| EV/EBITDA  |         |                 |            |

Target price rationale and upside / downside.

## Catalysts & Timeline
- Near-term (0–3 months): ...
- Medium-term (3–12 months): ...

## Risk Factors
- <Risk 1>
- <Risk 2>
- <Risk 3>

## Position Recommendation
Suggested entry range, position size, stop-loss level, review trigger.
```

## Error handling

| Situation | 简体回复 | 繁體回復 | English reply |
|-----------|---------|---------|---------------|
| Symbol not found | 未找到该代码，请确认市场和代码格式。 | 找不到該代碼，請確認市場和代碼格式。 | Symbol not found — verify the exchange and ticker. |
| Financials unavailable | 财务数据暂不可用，提案中该部分留空。 | 財務數據暫不可用，提案中該部分留空。 | Financials unavailable — that section will be left blank. |
| `command not found: longbridge` | 请安装 longbridge-terminal 或通过 MCP 连接。 | 請安裝 longbridge-terminal 或透過 MCP 連線。 | Install longbridge-terminal or connect via MCP. |
| `not logged in` | 请运行 `longbridge auth login`。 | 請執行 `longbridge auth login`。 | Run `longbridge auth login`. |

## MCP fallback

If `longbridge` binary is not found, fall back to the equivalent `mcp__longbridge__*` tools for each data type.

## Related skills

- `longbridge-fundamental` — deep financial KPI analysis
- `longbridge-valuation` — historical valuation percentile
- `longbridge-earnings` — post-earnings update report
- `longbridge-news` — recent news and filings

## File layout

```
skills/longbridge-investment-proposal/
└── SKILL.md
```
