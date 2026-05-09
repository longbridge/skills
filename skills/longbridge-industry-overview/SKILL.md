---
name: longbridge-industry-overview
description: |
  Industry / sector panorama report — generates a comprehensive industry overview covering market dynamics, competitive landscape, key players, thematic trends, valuation ranges, and catalysts/risks. Outputs industry sizing, growth rate, major-player market share estimates, and valuation bands. Triggers: "行业概览", "行业报告", "板块报告", "行业全景", "竞争格局", "行业分析", "板块分析", "行業概覽", "行業報告", "板塊報告", "行業全景", "競爭格局", "industry overview", "sector overview", "industry report", "sector analysis", "market landscape", "competitive landscape", "industry sizing", "sector deep dive", "semiconductor industry", "AI sector overview".
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

# longbridge-industry-overview

Generates an industry panorama report for a given sector or index, synthesising constituent stocks, peer valuation, and industry news into a structured landscape view.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

Trigger when the user wants an industry-level (not single-stock) analysis:

- *"给我做一份半导体行业的报告"* / *"幫我寫港股科技板塊全景"* / *"Give me an overview of the EV sector"*
- *"行业竞争格局"*, *"板块分析"*, *"market landscape for cloud computing"*

If the user mentions a specific stock as the entry point (*"NVDA 所在的行业"*), use that stock's industry as the anchor.

## Workflow

1. Identify the target industry or sector (from explicit mention or inferred from anchor symbol).
2. If an index or ETF covers the sector, fetch its constituents.
3. For each key constituent (top 5–8 by market cap), fetch industry-level valuation data.
4. Fetch recent industry news using representative symbols as proxies.
5. Synthesise into an industry overview report (see Output section).

## CLI

> If you're unsure of exact flag names or defaults, run `longbridge <subcommand> --help` first.

```bash
# Constituent list for a sector index or ETF
longbridge constituent <INDEX_SYMBOL> --format json

# Industry-level valuation comparison (anchored to a representative symbol)
longbridge industry-valuation <SYMBOL> --format json

# Recent news for top-N constituents (run per key company)
longbridge news <SYMBOL> --format json

# Static info for market cap / industry classification
longbridge static <SYMBOL> --format json
```

Common index symbols: `HSI.HK` (Hang Seng), `SPX.US` (S&P 500), `IXIC.US` (Nasdaq), `000300.SH` (CSI 300). Sector ETF examples: `SOXX.US` (semiconductors), `XLK.US` (US tech).

## Output

Structure the response as an industry report:

1. **Industry definition** — scope, SIC/GICS classification, geographic focus
2. **Market sizing** — estimated total addressable market, growth rate, stage (early / growth / mature / declining)
3. **Key players** (table — top 5–8 by market cap):

| Company | Symbol | Market Cap | Revenue Growth | PE | Market Share Est. |
|---|---|---|---|---|---|

4. **Competitive dynamics** — concentration (HHI), barriers to entry, switching costs, pricing power
5. **Valuation landscape** — PE / PB / PS range (min / median / max) across sector
6. **Thematic catalysts** — top 3–5 industry tailwinds (policy, technology, macro)
7. **Key risks** — top 3 headwinds or structural threats
8. **Conclusion** — overall industry attractiveness rating and investment angle

## Error handling

| Situation | Simplified Chinese | Traditional Chinese / English |
|---|---|---|
| `command not found: longbridge` | 回退到 MCP；否则提示安装 longbridge-terminal | 回退到 MCP；否則提示安裝 / Fall back to MCP; prompt to install |
| `not logged in` / `unauthorized` | 请运行 `longbridge auth login` | 請運行 `longbridge auth login` / Run `longbridge auth login` |
| Index symbol not found | 请提供正确的指数代码，如 SPX.US、HSI.HK | 請提供正確指數代碼 / Provide a valid index symbol e.g. SPX.US |
| Other stderr | 原样展示错误，不重试 | 原樣展示，不重試 / Surface verbatim, no silent retry |

## Related skills

| User asks | Route to |
|---|---|
| Single-company research | `longbridge-stock-research` |
| Peer valuation matrix | `longbridge-peer-comparison` |
| Index constituent list | `longbridge-constituent` |
| Competitive analysis for one company | `longbridge-competitive-analysis` |
| Coverage initiation | `longbridge-coverage-initiation` |

## File layout

```
longbridge-industry-overview/
└── SKILL.md
```

Prompt-only — no `scripts/`. Discover the latest CLI flags via `longbridge <subcommand> --help`.
