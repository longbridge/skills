# Longbridge Skills

Make your AI assistant fluent in [Longbridge](https://longbridge.com) — ask about stock prices, your portfolio, news, and valuations in plain English, 中文, or 繁體, and get answers backed by real Longbridge data.

13 skills covering market data, technical analysis, derivatives, fundamentals, research, portfolio & account, quantitative strategies, watchlist, content, market intelligence, earnings, and value investing across HK / US / A-share / Singapore markets.

---

## Install

Pick whichever fits your workflow:

### Fresh install (never installed Longbridge skills before)

```bash
# npx — global install
npx skills add longbridge/skills -g

# bun
bunx skills add longbridge/skills -g

# Codex plugin marketplace
codex plugin marketplace add longbridge/skills
codex plugin add longbridge@longbridge-skills

# Claude Code plugin marketplace
/plugin marketplace add longbridge/skills
/plugin install longbridge@longbridge-skills
```

### Upgrading from v1.x (had the old 127-skill version)

> ⚠️ `npx skills add` and `npx skills update` will **not** remove the 127 old skills — they only add/refresh. Old skills will linger and compete with new triggers. Use the reinstall script instead:

```bash
# One-liner — wipes old longbridge-* skills, installs the new 13
curl -fsSL https://raw.githubusercontent.com/longbridge/skills/main/scripts/update.sh | bash
```

See [Full reinstall](#full-reinstall-use-this-after-a-release-that-renames-or-consolidates-skills) below for details and dry-run option.

📖 **Full guide** with prerequisites / verification / FAQ → [docs/install.md](./docs/install.md)

---

## Update

### npx

```bash
# Update all skills
npx skills update -g

# Update a single skill
npx skills update longbridge-market-data -g
```

### bun

```bash
bunx skills update -g
bunx skills update longbridge-market-data -g
```

### Full reinstall (use this after a release that renames or consolidates skills)

`npx skills update` only refreshes skills whose name is **unchanged**. It does *not* remove
skills that were renamed/removed, and does *not* add brand-new names — so after a
consolidation release you can be left with stale orphan skills plus missing new ones, and
their triggers fight each other. To wipe everything Longbridge-related and reinstall the
current set cleanly:

**One-liner (no clone needed, requires `git`):**

```bash
curl -fsSL https://raw.githubusercontent.com/longbridge/skills/main/scripts/update.sh | bash

# preview without changing anything:
curl -fsSL https://raw.githubusercontent.com/longbridge/skills/main/scripts/update.sh | bash -s -- --dry-run
```

It pulls the latest skills and wipes every old `longbridge` / `longbridge-*` entry (directories
**and** dangling symlinks) from each detected agent directory — `~/.claude`, `~/.agents`,
`~/.gemini`, `~/.opencode` — before installing the current set fresh.

Restart any open agent session afterwards so it re-scans the skills directory.

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
| **Foundation** | [`longbridge`](./skills/longbridge) — Longbridge CLI / Python SDK / Rust SDK / MCP integration |
| **Market Data** | [`longbridge-market-data`](./skills/longbridge-market-data) — quotes, K-line, depth, capital flow, IPO, exchange rates |
| **Technical Analysis** | [`longbridge-technical`](./skills/longbridge-technical) — Ichimoku, candlestick, SMC, Chan Theory, Elliott Wave, Turtle Trading |
| **Derivatives** | [`longbridge-derivatives`](./skills/longbridge-derivatives) — options chain, Greeks, IV, HK warrants |
| **Fundamentals** | [`longbridge-fundamentals`](./skills/longbridge-fundamentals) — financial statements, valuation, company info, DCF |
| **Research** | [`longbridge-research`](./skills/longbridge-research) — analyst ratings, consensus, insider trades, investment frameworks |
| **Portfolio** | [`longbridge-portfolio`](./skills/longbridge-portfolio) — positions, P&L, orders, DCA, risk analysis, rebalancing |
| **Quant** | [`longbridge-quant`](./skills/longbridge-quant) — pairs trading, multi-factor, ML strategies, statistical methods |
| **Watchlist** | [`longbridge-watchlist`](./skills/longbridge-watchlist) — watchlist groups, price alerts, community lists |
| **Content** | [`longbridge-content`](./skills/longbridge-content) — news, filings, topics, SEC EDGAR analysis |
| **Intel** | [`longbridge-intel`](./skills/longbridge-intel) — screener, rankings, anomalies, sector rotation, morning brief, ETF flow |
| **Earnings** | [`longbridge-earnings`](./skills/longbridge-earnings) — post-earnings analysis: summary card + full Markdown report |
| **Value Investing** | [`longbridge-value-investing`](./skills/longbridge-value-investing) — Graham NCAV/net-net + Buffett moat analysis |

Click any name above to see what it can do.

---

## Prerequisites

You need one or both of these set up:

- **Longbridge CLI** (for live quotes, your holdings, watchlist) — install [longbridge-terminal](https://github.com/longportapp/longbridge-terminal), then run `longbridge auth login`.
- **Longbridge MCP** (for analysis-tier features in fundamentals / research / portfolio / intel) — `claude mcp add --transport http longbridge https://mcp.longbridge.com`.

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

### Codex plugin development

This repo is also a Codex plugin. The plugin root is the repository root:

- [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json) declares the plugin and points Codex at `./skills/`.
- [`.agents/plugins/marketplace.json`](./.agents/plugins/marketplace.json) exposes the repo-local marketplace as `longbridge-skills`.

For local testing from a checkout:

```bash
codex plugin marketplace add .
codex plugin add longbridge@longbridge-skills
```

Restart Codex or open a new thread after reinstalling so the updated skills are reloaded.

### Maintainer rule: skill names are immutable

**Once a skill is published, its `name` / directory slug must never change.** Installers match
skills by slug, so renaming one does not upgrade the old install — it *orphans* it: the old
skill lingers on every user's machine (stale, and competing for the same triggers) while the
new name is never picked up by `npx skills update` at all.

When a skill needs reorganizing:

- **Prefer adding/editing content under the existing slug** rather than renaming it.
- If a new slug is genuinely unavoidable, treat it as a **breaking change**: call it out in the
  release notes and tell users to run the full reinstall (above), which is the only way to clear
  the orphaned old slugs.

License: [MIT](./LICENSE).

---

<a href="https://aiagentsdirectory.com/agent/longbridge" target="_blank" rel="noopener" title="Discover Longbridge on AI Agents Directory">
  <img src="https://aiagentsdirectory.com/featured-badge.svg?v=2024" alt="Longbridge - Featured on AI Agents Directory" width="200" height="50" />
</a>
