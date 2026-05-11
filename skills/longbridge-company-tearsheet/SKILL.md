---
name: longbridge-company-tearsheet
description: |
  Company tear sheet / one-pager via Longbridge Securities — generates a high-density 1–2 page company snapshot: business overview, key financials (revenue / net income / EPS / ROE), valuation multiples (PE / PB / EV-EBITDA), price performance, major shareholders, and recent catalysts. Triggers: "公司单页", "公司快照", "公司简报", "公司画像", "一页纸分析", "公司概要", "股票简报", "公司單頁", "公司快照", "公司簡報", "公司畫像", "一頁紙分析", "company tearsheet", "company profile", "company snapshot", "one-pager", "company brief", "stock summary", "company factsheet".
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

# longbridge-company-tearsheet

High-density company snapshot — business, financials, valuation, shareholders, and catalysts on one page.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

Trigger on prompts asking for:

- A compact company overview — *"给我 AAPL 的公司简报"*, *"TSLA tearsheet"*, *"公司快照"*
- One-pager for a stock — *"one-pager for 9988.HK"*, *"一页纸分析"*
- Quick company factsheet — *"company factsheet"*, *"公司概要"*

For deep financial analysis defer to `longbridge-fundamental`. For investment proposal defer to `longbridge-investment-proposal`.

## Workflow

1. Extract and normalise the symbol.
2. Fetch in parallel:
   - Company profile (name, industry, founded, employees, IPO date, address)
   - Latest income statement KPIs (revenue, net income, EPS, ROE, gross margin)
   - Valuation multiples (PE, PB, EV-EBITDA)
   - Real-time quote and 52-week range
   - Major shareholders (top 5)
   - Recent news headlines (top 3)
3. Render the tearsheet as a structured markdown output.
4. Flag any data gaps explicitly.

> If unsure of exact flag names, run `longbridge <subcommand> --help` before proceeding.

## CLI

```bash
# Company profile
longbridge company <SYMBOL> --format json

# Valuation multiples (PE, PB, etc.)
longbridge calc-index <SYMBOL> --format json

# Latest income statement
longbridge financial-report <SYMBOL> --kind IS --format json

# Major shareholders
longbridge shareholder <SYMBOL> --format json

# Real-time quote
longbridge quote <SYMBOL> --format json

# Recent news
longbridge news <SYMBOL> --format json
```

## Output structure

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 <Company Name>  (<SYMBOL>)          <Date>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OVERVIEW
Industry: ...  Founded: ...  Employees: ...
IPO: ...  Exchange: ...

PRICE SNAPSHOT
Last: $xxx.xx  Change: +x.x%  52w: $xx–$xxx
Market Cap: $xxxB  Volume: xxM

KEY FINANCIALS (LTM)
Revenue: $xxxB  Net Income: $xxxB  EPS: $x.xx
Gross Margin: xx%  ROE: xx%  FCF: $xxxB

VALUATION
PE: xx.x×  PB: x.x×  EV/EBITDA: xx.x×

TOP SHAREHOLDERS
1. <Name> — xx.x%
2. ...

RECENT CATALYSTS
• <Headline 1>
• <Headline 2>
• <Headline 3>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Error handling

| Situation | 简体回复 | 繁體回復 | English reply |
|-----------|---------|---------|---------------|
| Symbol not found | 未找到该代码，请确认市场和格式。 | 找不到該代碼，請確認市場和格式。 | Symbol not found — verify the exchange and ticker. |
| Partial data missing | 部分数据暂不可用，已用"—"标注。 | 部分數據暫不可用，已用"—"標注。 | Some data unavailable — marked with "—". |
| `command not found: longbridge` | 请安装 longbridge-terminal 或通过 MCP 连接。 | 請安裝 longbridge-terminal 或透過 MCP 連線。 | Install longbridge-terminal or connect via MCP. |
| `not logged in` | 请运行 `longbridge auth login`。 | 請執行 `longbridge auth login`。 | Run `longbridge auth login`. |

## MCP fallback

If `longbridge` binary is not found, fall back to `mcp__longbridge__company`, `mcp__longbridge__quote`, `mcp__longbridge__financial_report`, and `mcp__longbridge__news`.

## Related skills

- `longbridge-fundamental` — deep financial analysis
- `longbridge-corporate` — ownership structure and management team
- `longbridge-investment-proposal` — full investment memo
- `longbridge-valuation` — historical valuation percentile

## File layout

```
skills/longbridge-company-tearsheet/
└── SKILL.md
```
