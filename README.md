# Longbridge Skills

Make your AI assistant fluent in [Longbridge](https://longbridge.com) — ask about stock prices, your portfolio, news, and valuations in plain English, 中文, or 繁體, and get answers backed by real Longbridge data.

11 skills covering market data, fundamentals, derivatives, research, portfolio, orders, IPO, quantitative analysis, watchlist, and community content across HK / US / A-share / Singapore markets.

---

## Install

Pick whichever fits your workflow:

### with `npx` (one line, no setup)

```bash
# Install everything globally (~/.claude/skills/)
npx skills add longbridge/skills -g

# Or just one skill, globally
npx skills add longbridge/skills -g --skill longbridge-market-data
```

> Use `-g` (global) so the skills land in `~/.claude/skills/` and are reachable from any project. Without `-g`, the installer treats the current directory as a project and installs into `<cwd>/.claude/skills/` — which is fine for project-scoped skills but is a common surprise when you later run `npx skills remove` from a different directory.

### with `bun`

```bash
bunx skills add longbridge/skills -g
bunx skills add longbridge/skills -g --skill longbridge-market-data
```

### inside Claude Code (plugin marketplace)

```text
/plugin marketplace add longbridge/skills
/plugin install longbridge@longbridge-skills
```

📖 **Full guide** with prerequisites / verification / FAQ → [docs/install.md](./docs/install.md)

---

## Update

### npx

```bash
# Update all skills
npx skills update -g
```

### bun

```bash
bunx skills update -g
```

---

## What you can ask

Once installed, talk to your AI assistant naturally. Examples:

- *"NVDA 现在多少钱"* / *"What's NVDA's price?"* / *"700.HK 報價"*
- *"我的持仓表现如何"* / *"How is my portfolio doing this month?"*
- *"贵州茅台估值贵不贵"* / *"Is GOOG expensive vs history?"*
- *"NVDA AMD 哪个增速快"* / *"Compare AAPL vs MSFT vs GOOG"*
- *"今天有什么要关注的"* / *"Give me my morning briefing"*
- *"特斯拉最近怎么了"* / *"Recent news on TSLA"*

The right skill is picked automatically based on your question, in the language you used.

---

## What's inside

| Group | Skill |
|---|---|
| **Foundation** | [`longbridge`](./skills/longbridge) — Longbridge CLI / Python SDK / Rust SDK / MCP integration reference |
| **Market Data** | [`longbridge-market-data`](./skills/longbridge-market-data) — real-time quotes, K-lines, depth, capital flow, FX, indices, northbound flow, AH/ADR premiums, anomalies, microstructure, subscriptions |
| **Derivatives** | [`longbridge-derivatives`](./skills/longbridge-derivatives) — options chains, implied volatility, Greeks, P&L diagrams, warrants, CBBCs, volatility strategies |
| **Fundamentals** | [`longbridge-fundamentals`](./skills/longbridge-fundamentals) — financials, earnings, valuation, consensus, DCF, peer comparison, sector analysis, screening, ETF flow, institutional holdings |
| **Research** | [`longbridge-research`](./skills/longbridge-research) — news, calendar, morning brief, catalyst radar, thesis tracking, SEC filings, analyst ratings, supply chain, insider/short flows |
| **Portfolio & Account** | [`longbridge-portfolio`](./skills/longbridge-portfolio) — positions, P&L attribution, risk (VaR/stress), asset allocation, rebalancing, tax harvesting, financial planning, statements |
| **Orders & Trading** | [`longbridge-orders`](./skills/longbridge-orders) — order history, DCA plans, price alerts, VWAP/TWAP execution, hedging strategies |
| **IPO** | [`longbridge-ipo`](./skills/longbridge-ipo) — IPO calendar, subscription status, HK IPO analysis, grey market, cornerstone investors |
| **Quant** | [`longbridge-quant`](./skills/longbridge-quant) — technical indicators, candlestick/Elliott/Ichimoku/SMC/Chanlun/harmonic patterns, pairs trading, multi-factor, ML, Turtle, volatility, seasonality |
| **Watchlist** | [`longbridge-watchlist`](./skills/longbridge-watchlist) — read/manage personal watchlist groups, add/remove securities, share lists |
| **Content** | [`longbridge-content`](./skills/longbridge-content) — community discussions, business/financial queries, regulatory rules, DeFi yields, on-chain analytics |

Click any name above to see what it can do.

---

## Prerequisites

You need one or both of these set up:

- **Longbridge CLI** (for live quotes, your holdings, watchlist) — install [longbridge-terminal](https://github.com/longportapp/longbridge-terminal), then run `longbridge auth login`.
- **Longbridge MCP** (for valuation / news / fundamentals / portfolio analysis) — `claude mcp add --transport http longbridge https://openapi.longbridge.com/mcp`.

Both authenticate with your Longbridge account. Pick "trade" permission during login if you want account-level skills (positions, orders, P&L).

---

## Notes

- **No investment advice.** Skills surface data, never recommend buy/sell.
- **Your data stays yours.** Account values are private and only shown to you.
- **Languages:** ask in 简体中文 / 繁體中文 / English — answers come back in the same language.

---

## For developers

- [CLAUDE.md](./CLAUDE.md) — repo-level instructions for Claude Code when developing inside this repo
- [docs/architecture.md](./docs/architecture.md) — how the multilingual triggers + CLI/MCP routing work under the hood
- [docs/install.md](./docs/install.md) — every install path, verification, troubleshooting

License: [MIT](./LICENSE).
