# Longbridge Skills

Make your AI assistant fluent in [Longbridge](https://longbridge.com) — ask about stock prices, your portfolio, news, and valuations in plain English, 中文, or 繁體, and get answers backed by real Longbridge data.

120 skills covering market data, fundamentals, valuation, options, technical analysis, quantitative strategies, portfolio risk, research, cross-market analysis, community, IPO, and automation across HK / US / A-share / Singapore markets.

---

## Install

Pick whichever fits your workflow:

### with `npx` (one line, no setup)

```bash
# Install everything globally (~/.claude/skills/)
npx skills add longbridge/skills -g

# Or just one skill, globally
npx skills add longbridge/skills -g --skill longbridge-quote
```

> Use `-g` (global) so the skills land in `~/.claude/skills/` and are reachable from any project. Without `-g`, the installer treats the current directory as a project and installs into `<cwd>/.claude/skills/` — which is fine for project-scoped skills but is a common surprise when you later run `npx skills remove` from a different directory.

### with `bun`

```bash
bunx skills add longbridge/skills -g
bunx skills add longbridge/skills -g --skill longbridge-quote
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

# Update a single skill
npx skills update longbridge-quote -g
```

### bun

```bash
bunx skills update -g
bunx skills update longbridge-quote -g
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

| Group | Skills |
|---|---|
| **Foundation** | [`longbridge`](./skills/longbridge) — Longbridge CLI / Python SDK / Rust SDK / MCP integration reference |
| **Live market data** | [`longbridge-quote`](./skills/longbridge-quote) · [`longbridge-kline`](./skills/longbridge-kline) · [`longbridge-depth`](./skills/longbridge-depth) · [`longbridge-capital-flow`](./skills/longbridge-capital-flow) · [`longbridge-market-temp`](./skills/longbridge-market-temp) · [`longbridge-derivatives`](./skills/longbridge-derivatives) · [`longbridge-security-list`](./skills/longbridge-security-list) · [`longbridge-anomaly`](./skills/longbridge-anomaly) · [`longbridge-ah-premium`](./skills/longbridge-ah-premium) · [`longbridge-constituent`](./skills/longbridge-constituent) · [`longbridge-fx`](./skills/longbridge-fx) · [`longbridge-northbound-flow`](./skills/longbridge-northbound-flow) |
| **Your account** | [`longbridge-positions`](./skills/longbridge-positions) · [`longbridge-orders`](./skills/longbridge-orders) · [`longbridge-watchlist`](./skills/longbridge-watchlist) · [`longbridge-watchlist-admin`](./skills/longbridge-watchlist-admin) · [`longbridge-subscriptions`](./skills/longbridge-subscriptions) · [`longbridge-statement`](./skills/longbridge-statement) · [`longbridge-alert`](./skills/longbridge-alert) · [`longbridge-dca`](./skills/longbridge-dca) · [`longbridge-profit-analysis`](./skills/longbridge-profit-analysis) · [`longbridge-ipo`](./skills/longbridge-ipo) |
| **Fundamentals & earnings** | [`longbridge-valuation`](./skills/longbridge-valuation) · [`longbridge-fundamental`](./skills/longbridge-fundamental) · [`longbridge-peer-comparison`](./skills/longbridge-peer-comparison) · [`longbridge-financial-report`](./skills/longbridge-financial-report) · [`longbridge-financial-analysis`](./skills/longbridge-financial-analysis) · [`longbridge-financial-checkup`](./skills/longbridge-financial-checkup) · [`longbridge-consensus`](./skills/longbridge-consensus) · [`longbridge-earnings-revision`](./skills/longbridge-earnings-revision) · [`longbridge-industry-valuation`](./skills/longbridge-industry-valuation) · [`longbridge-factor-screen`](./skills/longbridge-factor-screen) · [`longbridge-operating`](./skills/longbridge-operating) · [`longbridge-valuation-rank`](./skills/longbridge-valuation-rank) · [`longbridge-analyst-estimates`](./skills/longbridge-analyst-estimates) |
| **Research & events** | [`longbridge-news`](./skills/longbridge-news) · [`longbridge-calendar`](./skills/longbridge-calendar) · [`longbridge-catalyst-radar`](./skills/longbridge-catalyst-radar) · [`longbridge-earnings`](./skills/longbridge-earnings) · [`longbridge-earnings-preview`](./skills/longbridge-earnings-preview) · [`longbridge-corporate`](./skills/longbridge-corporate) · [`longbridge-flows`](./skills/longbridge-flows) · [`longbridge-corporate-events`](./skills/longbridge-corporate-events) · [`longbridge-portfolio`](./skills/longbridge-portfolio) · [`longbridge-topic`](./skills/longbridge-topic) · [`longbridge-sharelist`](./skills/longbridge-sharelist) |
| **Sector & market** | [`longbridge-sector-rotation`](./skills/longbridge-sector-rotation) · [`longbridge-sector-monitor`](./skills/longbridge-sector-monitor) · [`longbridge-market-microstructure`](./skills/longbridge-market-microstructure) |
| **Technical analysis** ⚠️ | [`longbridge-candlestick`](./skills/longbridge-candlestick) · [`longbridge-technical`](./skills/longbridge-technical) · [`longbridge-ichimoku`](./skills/longbridge-ichimoku) · [`longbridge-chanlun`](./skills/longbridge-chanlun)¹ · [`longbridge-elliott`](./skills/longbridge-elliott) · [`longbridge-harmonic`](./skills/longbridge-harmonic) · [`longbridge-smc`](./skills/longbridge-smc)² |
| **Options & derivatives** | [`longbridge-options-volatility`](./skills/longbridge-options-volatility) · [`longbridge-options-pnl`](./skills/longbridge-options-pnl) · [`longbridge-options-strategy`](./skills/longbridge-options-strategy) · [`longbridge-options-advanced`](./skills/longbridge-options-advanced) |
| **Portfolio & risk** | [`longbridge-portfolio-diagnosis`](./skills/longbridge-portfolio-diagnosis) · [`longbridge-portfolio-rebalance`](./skills/longbridge-portfolio-rebalance) · [`longbridge-asset-allocation`](./skills/longbridge-asset-allocation) · [`longbridge-risk-analysis`](./skills/longbridge-risk-analysis) · [`longbridge-tax-harvesting`](./skills/longbridge-tax-harvesting) · [`longbridge-financial-planning`](./skills/longbridge-financial-planning) · [`longbridge-risk-return`](./skills/longbridge-risk-return) |
| **Value & screening** | [`longbridge-value-screen`](./skills/longbridge-value-screen) · [`longbridge-buffett-moat-analyzer`](./skills/longbridge-buffett-moat-analyzer) · [`longbridge-buffett-moat-stock-screener`](./skills/longbridge-buffett-moat-stock-screener) · [`longbridge-graham-stock-analysis`](./skills/longbridge-graham-stock-analysis) · [`longbridge-graham-screener`](./skills/longbridge-graham-screener) · [`longbridge-ark-analysis`](./skills/longbridge-ark-analysis) · [`longbridge-dividend-screen`](./skills/longbridge-dividend-screen) · [`longbridge-smallcap-growth`](./skills/longbridge-smallcap-growth) · [`longbridge-etf-analysis`](./skills/longbridge-etf-analysis) · [`longbridge-etf-flow`](./skills/longbridge-etf-flow) |
| **Deep research** | [`longbridge-stock-research`](./skills/longbridge-stock-research) · [`longbridge-coverage-initiation`](./skills/longbridge-coverage-initiation) · [`longbridge-industry-overview`](./skills/longbridge-industry-overview) · [`longbridge-morning-brief`](./skills/longbridge-morning-brief) · [`longbridge-thesis-tracker`](./skills/longbridge-thesis-tracker) · [`longbridge-investment-ideas`](./skills/longbridge-investment-ideas) · [`longbridge-competitive-analysis`](./skills/longbridge-competitive-analysis) · [`longbridge-investment-proposal`](./skills/longbridge-investment-proposal) · [`longbridge-company-profile`](./skills/longbridge-company-profile) · [`longbridge-company-tearsheet`](./skills/longbridge-company-tearsheet) |
| **Quantitative strategies** ⚠️ | [`longbridge-volatility-strategy`](./skills/longbridge-volatility-strategy) · [`longbridge-seasonality`](./skills/longbridge-seasonality) · [`longbridge-pairs-trading`](./skills/longbridge-pairs-trading) · [`longbridge-ml-strategy`](./skills/longbridge-ml-strategy)³ · [`longbridge-performance-attribution`](./skills/longbridge-performance-attribution) · [`longbridge-correlation`](./skills/longbridge-correlation) · [`longbridge-multifactor`](./skills/longbridge-multifactor) · [`longbridge-factor-research`](./skills/longbridge-factor-research) · [`longbridge-quant`](./skills/longbridge-quant)⁵ |
| **Frameworks & methodology** ⚠️ | [`longbridge-valuation-methodology`](./skills/longbridge-valuation-methodology) · [`longbridge-dcf`](./skills/longbridge-dcf) · [`longbridge-hedging`](./skills/longbridge-hedging) · [`longbridge-behavioral-finance`](./skills/longbridge-behavioral-finance) · [`longbridge-quant-stats`](./skills/longbridge-quant-stats)⁴ · [`longbridge-regulatory-kb`](./skills/longbridge-regulatory-kb) · [`longbridge-execution-model`](./skills/longbridge-execution-model) |
| **Cross-market & data** | [`longbridge-adr-premium`](./skills/longbridge-adr-premium) · [`longbridge-index-quote`](./skills/longbridge-index-quote) · [`longbridge-fx-carry`](./skills/longbridge-fx-carry) · [`longbridge-sec-filings`](./skills/longbridge-sec-filings) · [`longbridge-basicinfo`](./skills/longbridge-basicinfo) · [`longbridge-ownership`](./skills/longbridge-ownership) · [`longbridge-insresearch`](./skills/longbridge-insresearch) · [`longbridge-investors`](./skills/longbridge-investors) · [`longbridge-market-scanner`](./skills/longbridge-market-scanner) · [`longbridge-sector-screener`](./skills/longbridge-sector-screener) · [`longbridge-supply-chain`](./skills/longbridge-supply-chain) · [`longbridge-tech-hype`](./skills/longbridge-tech-hype) |
| **Events & strategy** | [`longbridge-event-strategy`](./skills/longbridge-event-strategy) · [`longbridge-event-opportunity`](./skills/longbridge-event-opportunity) · [`longbridge-strategy-optimizer`](./skills/longbridge-strategy-optimizer) · [`longbridge-post-investment`](./skills/longbridge-post-investment) · [`longbridge-finance-query`](./skills/longbridge-finance-query) · [`longbridge-business-query`](./skills/longbridge-business-query) |
| **Crypto / DeFi** ⚠️ | [`longbridge-defi-yield`](./skills/longbridge-defi-yield) · [`longbridge-onchain`](./skills/longbridge-onchain) — require Crypto account permission; DeFi protocol data via WebSearch |

> ¹ `longbridge-chanlun` requires `pip install czsc`
> ² `longbridge-smc` requires `pip install smartmoneyconcepts` (falls back to manual implementation if unavailable)
> ³ `longbridge-ml-strategy` requires `pip install scikit-learn` (usually pre-installed)
> ⁴ `longbridge-quant-stats` requires `pip install statsmodels scipy arch`
> ⁵ `longbridge-quant` (Pine Script runner) is a beta feature — requires account activation by Longbridge support

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
