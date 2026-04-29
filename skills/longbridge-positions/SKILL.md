---
name: longbridge-positions
description: |
  Account holdings — stock positions, fund positions, multi-currency cash balance, margin ratio (initial / maintenance / forced liquidation), and estimated max buy/sell quantity for a symbol. Requires longbridge login. Triggers: "我的持仓", "我有什么股票", "账户余额", "我有多少美金", "基金持仓", "我能买多少股", "保证金率", "杠杆要求", "账户全貌", "我的持倉", "賬戶餘額", "我有多少美金", "基金持倉", "保證金率", "賬戶全貌", "my holdings", "stock positions", "account balance", "how much can I buy", "margin ratio", "max buy qty", "portfolio snapshot".
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: account_read
  requires_login: true
  default_install: true
---

# longbridge-positions

Read-only account snapshot — what the user holds, how much cash, what they can buy/sell, and per-symbol margin ratios.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.
>
> **Privacy**: the data here is the user's private account state. Only return detailed numbers in direct conversation; if you suspect screen-sharing or third-party observation, confirm before showing exact figures.

## Subcommands

| Subcommand | Returns |
|---|---|
| `portfolio` | Combined `{positions, fund_positions, balance}` in one call. |
| `positions` | Stock holdings array. |
| `funds` | Fund holdings array. |
| `balance [--currency USD|HKD|CNY|SGD]` | Cash balance + financing limits per currency. |
| `margin-ratio <symbol>` | Initial / maintenance / forced-liquidation factors. |
| `max-qty <symbol> --side buy|sell [--price <p>] [--order-type LO|MO|ELO|ALO]` | Estimated max purchasable / sellable quantity (cash vs margin). |

## When to use

- *"我的持仓"*, *"我有什么股票"*, *"我的持倉"* → `positions`
- *"账户余额"*, *"我有多少美金 / 港币"*, *"current USD balance"* → `balance --currency USD`
- *"我的基金持仓"* → `funds`
- *"NVDA 我能买多少股"*, *"how many TSLA can I buy"* → `max-qty <s> --side buy --price <current>` (limit) or `--order-type MO` (market)
- *"茅台保证金率"* → `margin-ratio 600519.SH`
- *"看一下我的账户全貌"*, *"account snapshot"* → `portfolio`
- *"我的浮盈"* → `positions`, then LLM computes `(last - cost) × qty` from quote (chain to `longbridge-quote` for live last)

## max-qty workflow

1. **Limit order (default LO)**: first call `longbridge-quote -s <symbol>` for current last price → use as `--price`.
2. **Market order**: skip price; pass `--order-type MO`.
3. Response includes `cash_max_qty` (cash only) and `margin_max_qty` (with financing). Always disclose the difference and remind that financing has interest cost + forced-liquidation risk.

## CLI

```bash
python3 scripts/cli.py portfolio
python3 scripts/cli.py positions
python3 scripts/cli.py balance --currency USD
python3 scripts/cli.py margin-ratio TSLA.US
python3 scripts/cli.py max-qty TSLA.US --side buy --price 250
```

## Output

Per subcommand, `success / source / skill / skill_version / subcommand` plus:

- `portfolio`: `datas {positions, fund_positions, balance}`
- `positions / funds`: `datas` array
- `balance`: `datas` array (per currency); `currency` top-level field when filtered
- `margin-ratio`: `symbol / datas {im_factor, mm_factor, fm_factor}`
- `max-qty`: `symbol / side / order_type / [price] / datas {cash_max_qty, margin_max_qty}`

## OAuth scope

Requires the trade scope on the OAuth token. If the token lacks it, both CLI and MCP return `auth_expired` (stderr contains `authorized scope`). Tell the user to re-authorise with the trade scope checked.

## MCP fallback

| CLI subcommand | MCP tool |
|---|---|
| `positions` | `mcp__longbridge__stock_positions` |
| `funds` | `mcp__longbridge__fund_positions` |
| `balance` | `mcp__longbridge__account_balance` |
| `margin-ratio` | `mcp__longbridge__margin_ratio` |
| `max-qty` | `mcp__longbridge__estimate_max_purchase_quantity` |
| `portfolio` | merge `stock_positions` + `fund_positions` + `account_balance` (no combined MCP tool) |

MCP-only extensions: `mcp__longbridge__profit_analysis` / `profit_analysis_detail` (P/L analysis), `mcp__longbridge__exchange_rate` (currency conversion). For "how is my P&L this month?" route to `longbridge-portfolio`.

## Related skills

- Orders / executions / cash flow → `longbridge-orders`
- Watchlist (read) → `longbridge-watchlist`
- Account-level P&L analysis → `longbridge-portfolio`

## File layout

```
longbridge-positions/
├── SKILL.md
└── scripts/
    ├── cli.py
    └── test_cli.py
```
