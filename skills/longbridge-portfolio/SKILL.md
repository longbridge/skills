---
name: longbridge-portfolio
description: |
  Account-level analysis via Longbridge MCP — total market value, cash share, period P&L, single-stock contribution ranking, industry distribution, currency exposure, historical P/L curve. Requires longbridge login + MCP with **trade scope**. Returns data, never recommends rebalancing. Triggers: "我账户表现", "我本月浮盈", "我哪只股票贡献最多", "我组合配置", "我货币暴露", "我账户行业分布", "账户全貌", "我賬戶表現", "我本月浮盈", "我哪隻股貢獻最多", "我貨幣暴露", "我賬戶行業分佈", "my account performance", "monthly P&L", "biggest contributor", "portfolio breakdown", "currency exposure", "industry mix", "account-level analysis".
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: account_read
  requires_login: true
  default_install: true
  requires_mcp: true
  tier: analysis
---

# longbridge-portfolio

Prompt-only skill for **account-level** analysis. Distinguished from `longbridge-positions` (snapshot lookup): this skill answers *"how am I doing"*, not *"what do I hold"*.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.
>
> **Privacy**: returns the user's private P&L. Only render detailed numbers in direct conversation; if you suspect screen-sharing or third-party observation, ask before showing exact figures. Never echo amounts into PR descriptions, tickets, or other places third parties can read.

## Prerequisites (mandatory)

```bash
claude mcp add --transport http longbridge https://openapi.longbridge.com/mcp
```

This skill requires the **trade scope** OAuth token. If a tool returns *unauthorized* / *not in authorized scope*:

```bash
claude mcp logout longbridge
# Re-trigger any MCP tool call; in the browser auth screen, check "trade" / 「交易」 permission.
```

## When to use

- *"我账户表现如何"*, *"how is my account doing?"*
- *"我本月浮盈"*, *"this month's P&L"*
- *"我哪只股票贡献最多"*, *"top contributors"*
- *"我货币暴露"*, *"currency exposure"*
- *"我账户行业分布"*, *"industry mix"*

## "Me" disambiguation

By default, treat *我* / *me* / *my account* as **all-account aggregate**. If the user explicitly says *"我的港股账户"* / *"my US sub-account"*, restrict to that sub-account.

## Time-window inference

| Phrase | Window |
|---|---|
| 本月 / this month | first day of this month → today |
| 本周 / this week | this Monday → today |
| 近 30 天 / past 30 days | `today-30` → `today` |
| 今年 / YTD | Jan 1 → today |
| 全部 / since opening / no time | use `profit_analysis` defaults (typically since account opening) |

LLM uses today's date from system context.

## Tool selection by intent

| User intent | Tools |
|---|---|
| Full portfolio overview | `profit_analysis` + `stock_positions` + `account_balance` (combo) |
| This month's P&L | `profit_analysis(start=2026-04-01, end=2026-04-28)` |
| Biggest contributors | `profit_analysis_detail` + `stock_positions` |
| Currency exposure | `account_balance` + `exchange_rate` |
| Industry distribution | `stock_positions` + per-symbol `static_info` (industry field) |

## Workflow

1. **Confirm MCP + trade scope** — otherwise prompt the user to re-authorise.
2. Decide the time window (table above) and the toolset (table above).
3. Run MCP tools concurrently. Example for *"我本月账户表现"*:

   ```
   mcp__longbridge__profit_analysis(start_date="2026-04-01", end_date="2026-04-28")
   mcp__longbridge__profit_analysis_detail(start_date="2026-04-01", end_date="2026-04-28")
   mcp__longbridge__account_balance()
   mcp__longbridge__stock_positions()
   mcp__longbridge__exchange_rate()
   ```

4. **Convert FX** to USD-equivalent yourself (use `exchange_rate` from the same call day) — `profit_analysis` may return mixed currencies.
5. **Render the 4-section structure**. Cite Longbridge Securities. End with the not-investment-advice disclaimer.

## Output template

```
My account performance — Source: Longbridge Securities; period YYYY-MM-DD ~ YYYY-MM-DD

[1. Overview]
- Total NAV (USD-equivalent): $X
- Cash: $X (Y% of NAV)
- Holdings: $X (Y% of NAV)
- Period P&L: +$X (+Y%)

[2. Currency exposure]
- USD: $X
- HKD: HK$X (≈ $X USD)
- CNY: ¥X (≈ $X USD)
- SGD: S$X (if held)

[3. Single-stock contribution (this period)]
| Symbol | Name | P&L (USD-eq) | Share |
|---|---|---:|---:|
| NVDA.US | NVIDIA | +$5,200 | 42% |
| 700.HK  | 腾讯  | +$3,100 | 25% |
| TSLA.US | Tesla | -$1,800 | -15% |
| ...     | ...   | ...     | ... |

[4. Industry distribution] (stock_positions × static_info industry field, by market value)
- 半导体 / Semiconductors: 35%
- 互联网 / Internet:        20%
- ...

⚠️ Period P&L reflects short-term price moves and does not represent long-term return. Not rebalancing advice.
```

(Translate into the user's language.)

## Performance optimisation

Industry distribution requires `static_info` per symbol (N positions = N calls). When a user holds **≥ 30 names**:

- Tell the user *"computing industry distribution; this may take a moment..."*, OR
- Simplify: take the **top 10 by market value**, group the rest as *"other"*.

Same for the contribution ranking — list the top 10 (mix of leaders and laggards) by default; do not flood with the full position book.

## Hard prohibitions

- **No** "you should reduce / increase X" advice.
- **No** subjective verdicts ("your portfolio is poorly diversified"); data-driven phrasing only ("technology accounts for 60% of NAV — sector concentration is high").

## Output constraints

- **Must** include all 4 sections.
- **Must** label currency on every figure; mark USD-equivalent with `≈`.
- **Must** end with the not-rebalancing-advice disclaimer.

## Error handling

| Situation | Reply |
|---|---|
| MCP unconfigured | Prompt `claude mcp add ...` |
| Lacks trade scope | "This skill needs the trade-scope OAuth token. Run `claude mcp logout longbridge` and re-authorise with the trade permission ticked." |
| `profit_analysis` empty | "{window}: no recorded P&L (account had no positions or no trades)." |
| `account_balance` returns one currency | Skip the multi-currency section; show that one currency. |
| `stock_positions` empty | Skip sections 3 + 4; show cash-only overview. |

## MCP toolbelt

| MCP tool | Pulls | Scope |
|---|---|---|
| `mcp__longbridge__profit_analysis` | Period P&L summary | trade |
| `mcp__longbridge__profit_analysis_detail` | Per-stock P&L breakdown | trade |
| `mcp__longbridge__stock_positions` | Current holdings | trade |
| `mcp__longbridge__account_balance` | Multi-currency cash | trade |
| `mcp__longbridge__fund_positions` | Fund holdings | trade |
| `mcp__longbridge__exchange_rate` | FX conversion | quote |
| `mcp__longbridge__static_info` | Industry classification | quote |

## Related skills

- Position lookup ("what do I own?") → `longbridge-positions`
- Per-symbol drill-down → `longbridge-quote`, `longbridge-valuation`, `longbridge-fundamental`
- *"Why is X down?"* → `longbridge-news`
- *"Should I sell X?"* — **do not advise**; instead route to `longbridge-valuation` + `longbridge-fundamental` and let the user decide.

## File layout

```
longbridge-portfolio/
└── SKILL.md          # prompt-only, no scripts/
```
