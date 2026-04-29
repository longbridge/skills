---
name: longbridge-subscriptions
description: |
  List active real-time WebSocket subscriptions in the current Longbridge CLI session — symbols, sub_types (quote / depth / trades / brokers), candlestick periods. Diagnostic only; rarely needed in day-to-day use. Requires longbridge login. Triggers: "我订阅了哪些实时数据", "实时连接状态", "推送状态", "我訂閱了什麼", "推送狀態", "active subscriptions", "websocket subscriptions", "real-time stream status".
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: account_read
  requires_login: true
  default_install: false
---

# longbridge-subscriptions

Diagnostic listing of the active real-time subscriptions in the current `longbridge` CLI session.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

`default_install: false` — not installed by default. Manual symlink only.

## When to use

- *"我现在订阅了哪些实时推送"* → run
- *"为什么没收到 NVDA 实时报价"* → diagnostic
- *"实时数据"* (ambiguous) → ask back: subscriptions vs quotes vs watchlist?

## Workflow

```bash
python3 scripts/cli.py
```

Returns:

```json
{
  "success": true, "source": "longbridge", "skill": "longbridge-subscriptions", "skill_version": "1.0.0",
  "subscription_count": 5,
  "datas": [{"symbol": "NVDA.US", "sub_types": ["quote", "depth"], "candlestick_periods": [...]}, ...]
}
```

## Local-only

The Longbridge MCP service is stateless HTTP — it has **no** WebSocket session concept and **no** equivalent tool. This skill needs the local `longbridge` CLI (which holds the OAuth + WebSocket session).

If `cli.py` returns `binary_not_found`, tell the user this skill is local-only; install longbridge-terminal.

## File layout

```
longbridge-subscriptions/
├── SKILL.md
└── scripts/
    ├── cli.py
    └── test_cli.py
```
