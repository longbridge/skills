# longbridge-skills

[Agent Skills](https://agentskills.io/specification) that wrap the [Longbridge Securities](https://longbridge.com) platform — quotes, charts, fundamentals, valuation, news, watchlist, account analytics, and more. Multilingual support: Simplified Chinese / Traditional Chinese / English.

## Install

```bash
# Claude Code marketplace
claude skills install longbridge-skills

# or via npx
npx @agentskills/cli install longbridge-skills
```

See [docs/install.md](./docs/install.md) for all install methods and verification steps.

## What's inside

11 skills covering the full Longbridge platform:

| Skill | Description | Risk Level |
|---|---|---|
| `longbridge` | Platform entry point — routes to the 10 category skills below | read_only |
| `longbridge-market-data` | Real-time quotes, K-lines, order book depth, capital flows, FX, ETF flows, northbound flows, market scanners | read_only |
| `longbridge-derivatives` | Options strategies, Greeks, IV/volatility surface, futures, AH premium, ADR premium, FX carry | read_only |
| `longbridge-fundamentals` | Financial statements, valuation (PE/PB/DCF), earnings calendar, industry analysis, ownership data | read_only |
| `longbridge-research` | Analyst ratings, institutional holdings (13F), sector rotation, value/growth screeners, thematic research, ETF analysis | read_only |
| `longbridge-portfolio` | Holdings, P&L attribution, risk analysis (VaR/CVaR), asset allocation, rebalancing, tax harvesting | account_read |
| `longbridge-orders` | Order history queries, DCA setup, price alerts, execution model analysis | mutating |
| `longbridge-ipo` | IPO calendar, subscription management, allotment queries, HK IPO scoring framework | account_read |
| `longbridge-quant` | Technical indicators, candlestick/Elliott/Harmonic/SMC patterns, multi-factor models, pairs trading, backtesting | read_only |
| `longbridge-watchlist` | Watchlist read/write, group management, catalyst radar monitoring | mutating |
| `longbridge-content` | Daily pre-market briefing, stock news/announcements, community topics, regulatory knowledge base | read_only |

## Usage examples

```
# Market data
"NVDA 现在多少钱"          → longbridge-market-data
"特斯拉 K 线图"             → longbridge-market-data

# Fundamentals
"AAPL 最新财报"             → longbridge-fundamentals
"帮我做 TSLA 的 DCF 估值"   → longbridge-fundamentals

# Portfolio
"我的持仓分析"              → longbridge-portfolio
"组合最大回撤是多少"        → longbridge-portfolio

# Quant
"NVDA RSI 超卖了吗"         → longbridge-quant
"帮我回测这个策略"          → longbridge-quant

# Trading (two-step: preview + confirm)
"设置 AAPL 价格提醒 200"    → longbridge-orders
"把 NVDA 加到自选股"        → longbridge-watchlist
```

## Architecture

See [docs/architecture.md](./docs/architecture.md) for how multilingual triggers, CLI/MCP routing, and the two-step mutation protocol work.

## License

MIT. See [LICENSE](./LICENSE).
