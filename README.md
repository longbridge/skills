# Longbridge Skills

[Agent Skills](https://agentskills.io/specification) for [Longbridge Securities](https://longbridge.com) — query market quotes, charts, orderbook depth, fundamentals, news, and analyse personal portfolios across HK / US / A-share / SG markets.

**17 skills · multilingual triggers (Simplified Chinese / Traditional Chinese / English) · supports two install paths (single-skill symlink + plugin marketplace).**

```text
longbridge-skills/
├── .claude-plugin/marketplace.json     # plugin entry for /plugin install
├── skills/                             # 17 skill folders, lowercase ASCII slugs
│   ├── longbridge-quote/
│   ├── longbridge-kline/
│   ├── ...
│   └── longbridge-portfolio/
├── docs/
│   ├── architecture.md                 # how multilingual + CLI/MCP routing work
│   ├── install.md                      # full install / verify / FAQ
│   └── superpowers/                    # historical specs + plans (audit trail)
├── scripts/validate-skills.py          # frontmatter + test harness
├── LICENSE                             # MIT
└── README.md
```

## Quick install

Two install paths — full guide in [docs/install.md](./docs/install.md).

**A. Plugin marketplace** (one shot, all 17 skills):

```text
/plugin marketplace add longbridge/skills
/plugin install longbridge@longbridge-skills
```

**B. Single-skill symlink** (cherry-pick):

```bash
ln -s "$PWD/skills/longbridge-quote" ~/.claude/skills/longbridge-quote
```

Or batch-symlink all 17:

```bash
for d in "$PWD"/skills/*; do
  ln -sfn "$d" "$HOME/.claude/skills/$(basename $d)"
done
```

### Prerequisites

| Tier | Needs |
|---|---|
| Read tier (12 skills) | `longbridge` CLI installed + `longbridge login` (with trade scope for account skills); Python 3.8+ |
| Analysis tier (5 skills) | `claude mcp add --transport http longbridge https://openapi.longbridge.com/mcp` |

## Skill family

### Read tier (12) — wraps the local `longbridge` CLI; MCP fallback

| Skill | Purpose |
|---|---|
| [`longbridge-quote`](./skills/longbridge-quote) | Real-time quotes, static info, valuation indices |
| [`longbridge-kline`](./skills/longbridge-kline) | Candlestick (1m → year) + intraday |
| [`longbridge-depth`](./skills/longbridge-depth) | 5-level orderbook + brokers (HK) + tick trades |
| [`longbridge-capital-flow`](./skills/longbridge-capital-flow) | Capital flow + large/medium/small order distribution |
| [`longbridge-market-temp`](./skills/longbridge-market-temp) | Market temperature + sessions + trading days |
| [`longbridge-derivatives`](./skills/longbridge-derivatives) | Options + warrants + chain |
| [`longbridge-security-list`](./skills/longbridge-security-list) | Securities catalog + broker participants |
| [`longbridge-positions`](./skills/longbridge-positions) | Stock / fund holdings + balance + max-buy quantity |
| [`longbridge-orders`](./skills/longbridge-orders) | Today / history orders + executions + cash flow |
| [`longbridge-watchlist`](./skills/longbridge-watchlist) | Read-only watchlist groups |
| [`longbridge-watchlist-admin`](./skills/longbridge-watchlist-admin) | Watchlist mutations (with dry-run + confirm) |
| [`longbridge-subscriptions`](./skills/longbridge-subscriptions) | Active WebSocket subscriptions |

### Analysis tier (5) — `prompt-only`, **requires longbridge MCP**

| Skill | High-frequency questions |
|---|---|
| [`longbridge-valuation`](./skills/longbridge-valuation) | "Is X expensive?" PE/PB historical + industry percentiles |
| [`longbridge-fundamental`](./skills/longbridge-fundamental) | "How is X's business?" 5-dimension KPIs |
| [`longbridge-peer-comparison`](./skills/longbridge-peer-comparison) | "X vs Y vs Z?" 2–5 symbol matrix |
| [`longbridge-portfolio`](./skills/longbridge-portfolio) | "How is my account?" account-level analysis (trade scope) |
| [`longbridge-news`](./skills/longbridge-news) | "What's the news on X?" classified news + filings + community |

## Architecture

Two cross-cutting design decisions are documented in [docs/architecture.md](./docs/architecture.md):

- **Trilingual support** (Simplified Chinese / Traditional Chinese / English) — implemented entirely in prompt: triggers in `description`, `Response language` directive at top of each SKILL.md body, three-column field & error tables. Zero i18n code.
- **CLI vs MCP routing** — when each skill prefers `cli.py` (local subprocess) vs the official MCP server, plus four exception classes (security-list, subscriptions, analysis-tier, watchlist-admin dry-run).

## Validate

```bash
python3 scripts/validate-skills.py
```

Checks:
- Each SKILL.md frontmatter conforms to spec (slug, description ≤ 1024)
- `name` matches the parent directory name
- All read-tier `scripts/test_cli.py` pass

Errors block (exit 1); soft warnings (e.g. SKILL.md body > 500 lines) return exit 2.

## Output policy (all skills)

- **Data attribution**: cite "Longbridge Securities" / "数据来源:长桥证券" / "數據來源:長橋證券" when quoting prices, P&L, or valuation figures.
- **No investment advice**: analysis-tier skills end with "not investment advice" / "不构成投资建议". Read-tier may report numbers without the disclaim, but never recommend buy/sell.
- **Symbol convention**: `<CODE>.<MARKET>`, e.g. `NVDA.US`, `700.HK`, `600519.SH`, `300750.SZ`, `D05.SG`.
- **Response language**: each skill responds in the user's input language.

## Mutating skills

`longbridge-watchlist-admin` modifies the user's watchlist (no money, but persistent state). All mutations require `--confirm` plus a dry-run preview. See the skill's [SKILL.md](./skills/longbridge-watchlist-admin/SKILL.md).

A `longbridge-trading` skill (place / cancel / replace orders) is **designed but intentionally not implemented** in this release; it requires further risk gating and a deployment-time soft cap. See [docs/superpowers/specs/2026-04-28-skill-11-trading-risk-design.md](./docs/superpowers/specs/2026-04-28-skill-11-trading-risk-design.md).

## Historical / design docs

- [docs/superpowers/specs/](./docs/superpowers/specs/) — 18 design specs (platform protocol + per-skill differences). Pre-rename: still references the original Chinese skill names; preserved as audit trail.
- [docs/superpowers/plans/](./docs/superpowers/plans/) — implementation plans, in priority order.

## License

MIT — see [LICENSE](./LICENSE).
