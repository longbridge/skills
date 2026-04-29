---
name: longbridge-orders
description: |
  Read-only account orders, executions, and cash flow — today's or historical orders (filterable by symbol / date), single-order detail with status history, today/historical fills, and cash flow (deposits, withdrawals, dividends, settlements). Requires longbridge login. Read-only — no order placement here. Triggers: "今天我下了哪些单", "我的订单", "历史成交", "上个月成交", "出入金", "分红记录", "资金流水", "結算記錄", "我的訂單", "歷史成交", "上個月", "出入金記錄", "分紅", "資金流水", "today's orders", "order history", "executions", "fills", "cash flow", "deposits and withdrawals", "dividend record", "settlement".
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: account_read
  requires_login: true
  default_install: true
---

# longbridge-orders

Read-only orders / executions / cash flow. **Order placement, cancellation, replacement** are not in this skill — those would belong in a separate `longbridge-trading` skill (designed but intentionally not shipped in this release).

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.
>
> **Privacy**: orders, fills, and cash-flow data are private account state. Only return details in direct conversation.

## Subcommands

| Subcommand | Returns |
|---|---|
| `orders` (default = today) | Today's orders. With `--history --start --end --symbol`, queries history. |
| `order <order_id>` | Full single-order detail (status history, fees). |
| `executions` (default = today) | Today's fills. With `--history --start --end --symbol`, queries history. |
| `cash-flow [--start --end]` | Deposits / withdrawals / dividends / settlements. |

## Time-window inference

LLM converts natural-language windows to `--start` / `--end` (ISO `YYYY-MM-DD`):

| User says | Window |
|---|---|
| 今天 / today | no `--start --end` |
| 上个月 / last month | first → last day of previous month |
| 近 30 天 / past 30 days | `today-30` → `today` |
| 4 月 5 日 / April 5 | `--start = --end = 2026-04-05` |

Use today's date from the system context.

## When to use

- *"今天我下了哪些单"* → `orders`
- *"上个月所有成交"* → `executions --history --start --end`
- *"TSLA 历史订单"* → `orders --history --symbol TSLA.US --start ... --end ...`
- *"订单 20240101-123456789 详情"* → `order <id>`
- *"近 30 天出入金"*, *"上次分红"* → `cash-flow --start --end`

## CLI

```bash
python3 scripts/cli.py orders
python3 scripts/cli.py orders --history --start 2025-01-01 --end 2025-04-01 --symbol TSLA.US
python3 scripts/cli.py order 20240101-123456789
python3 scripts/cli.py executions --history --start 2025-01-01 --end 2025-04-01
python3 scripts/cli.py cash-flow --start 2025-04-01 --end 2025-04-30
```

For long history ranges, raise `--timeout 60`+.

## Output

`success / source / skill / skill_version / subcommand`, plus:

- `orders / executions`: `history` boolean + optional `start / end / symbol` + `datas` array
- `order`: `order_id` + `datas` (full object). Returns `error_kind: empty_result` if id not found.
- `cash-flow`: optional `start / end` + `datas` array

Status translation (LLM should map):

| Raw | 简体 | 繁體 | English |
|---|---|---|---|
| `Filled` | 已成交 | 已成交 | Filled |
| `PartialFilled` | 部分成交 | 部分成交 | Partially filled |
| `Canceled` | 已撤单 | 已撤單 | Cancelled |
| `New` | 待成交 | 待成交 | Working |
| `Rejected` | 被拒 | 被拒 | Rejected |

## OAuth scope

Same as `longbridge-positions`: needs trade scope. Lacking scope → both CLI and MCP return `auth_expired`.

## MCP fallback

| CLI subcommand | MCP tool |
|---|---|
| `orders` (today) | `mcp__longbridge__today_orders` |
| `orders --history` | `mcp__longbridge__history_orders` |
| `order <id>` | `mcp__longbridge__order_detail` |
| `executions` (today) | `mcp__longbridge__today_executions` |
| `executions --history` | `mcp__longbridge__history_executions` |
| `cash-flow` | `mcp__longbridge__cash_flow` |

MCP-only extensions: `mcp__longbridge__statement_*` (account statements / report exports).

## Related skills

- Holdings + balance → `longbridge-positions`
- Account-level P&L analysis → `longbridge-portfolio`

## File layout

```
longbridge-orders/
├── SKILL.md
└── scripts/
    ├── cli.py
    └── test_cli.py
```
