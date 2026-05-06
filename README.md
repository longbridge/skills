# Longbridge Skills

Make your AI assistant fluent in [Longbridge Securities](https://longbridge.com) — ask about stock prices, your portfolio, news, and valuations in plain English, 中文, or 繁體, and get answers backed by real Longbridge data.

30 skills covering market data, fundamentals, valuation, earnings, news, corporate ownership, institutional flows, account management, and automation across HK / US / A-share / Singapore markets.

---

## Install & Update

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
| **Live market data** | [`longbridge-quote`](./skills/longbridge-quote) · [`longbridge-kline`](./skills/longbridge-kline) · [`longbridge-depth`](./skills/longbridge-depth) · [`longbridge-capital-flow`](./skills/longbridge-capital-flow) · [`longbridge-market-temp`](./skills/longbridge-market-temp) · [`longbridge-derivatives`](./skills/longbridge-derivatives) · [`longbridge-security-list`](./skills/longbridge-security-list) · [`longbridge-anomaly`](./skills/longbridge-anomaly) · [`longbridge-ah-premium`](./skills/longbridge-ah-premium) · [`longbridge-constituent`](./skills/longbridge-constituent) · [`longbridge-fx`](./skills/longbridge-fx) |
| **Your account** | [`longbridge-positions`](./skills/longbridge-positions) · [`longbridge-orders`](./skills/longbridge-orders) · [`longbridge-watchlist`](./skills/longbridge-watchlist) · [`longbridge-watchlist-admin`](./skills/longbridge-watchlist-admin) · [`longbridge-subscriptions`](./skills/longbridge-subscriptions) · [`longbridge-statement`](./skills/longbridge-statement) · [`longbridge-alert`](./skills/longbridge-alert) · [`longbridge-dca`](./skills/longbridge-dca) |
| **Smart analysis** | [`longbridge-valuation`](./skills/longbridge-valuation) · [`longbridge-fundamental`](./skills/longbridge-fundamental) · [`longbridge-peer-comparison`](./skills/longbridge-peer-comparison) · [`longbridge-portfolio`](./skills/longbridge-portfolio) · [`longbridge-news`](./skills/longbridge-news) · [`longbridge-catalyst-radar`](./skills/longbridge-catalyst-radar) · [`longbridge-earnings`](./skills/longbridge-earnings) · [`longbridge-corporate`](./skills/longbridge-corporate) · [`longbridge-flows`](./skills/longbridge-flows) · [`longbridge-calendar`](./skills/longbridge-calendar) |

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
