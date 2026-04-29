---
name: longbridge-watchlist
description: |
  Read-only access to the user's Longbridge watchlist groups and the symbols inside each group. Mutations (create / rename / add / remove) belong in longbridge-watchlist-admin. Requires longbridge login. Triggers: "我的自选股", "自选股有哪些", "我关注的股票", "我的分组", "自選股", "關注的股票", "分組", "watchlist", "my watchlist", "favorited stocks", "watch groups".
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: account_read
  requires_login: true
  default_install: true
---

# longbridge-watchlist

Read-only listing of watchlist groups and member symbols. For mutations use `longbridge-watchlist-admin`.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.
>
> **Privacy**: a watchlist reveals trading interest. Only return detailed lists in direct conversation.

## Filter flags

| Flag | Effect |
|---|---|
| (none) | All groups |
| `--group <id>` | Single group by id |
| `--group-name <name>` | Single group by exact name |

## When to use

- *"我的自选股"*, *"watchlist contents"* → no flag
- *"我的「科技股」分组"*, *"my Tech group"* → `--group-name`
- *"分组 ID 12345 里有什么"* → `--group`

## Chained workflows (very common)

After getting symbols from this skill, route to other skills for the actual data:

| User asks | Flow |
|---|---|
| *"我自选股的港股涨幅"* | this skill → filter `.HK` → `longbridge-quote` (batch) |
| *"我自选最近一周走势"* | this skill → all symbols → `longbridge-kline` (loop) |
| *"我自选的总市值"* | this skill → all symbols → `longbridge-quote --include-static` |

**Get symbols here, then route the data query to the appropriate skill.** Don't try to compute change rates / charts inside this skill.

## CLI

```bash
python3 scripts/cli.py
python3 scripts/cli.py --group-name 科技
python3 scripts/cli.py --group 12345
```

## Output

```json
{
  "success": true, "source": "longbridge", "skill": "longbridge-watchlist", "skill_version": "1.0.0",
  "group_count": 3, "total_symbol_count": 42,
  "datas": [
    { "id": "12345", "name": "科技股", "securities": [{"symbol": "NVDA.US", "name": "..."}, ...] },
    ...
  ]
}
```

No matching group → `success: true`, `group_count: 0`, `total_symbol_count: 0`, `datas: []`.

## MCP fallback

| CLI behaviour | MCP tool |
|---|---|
| List watchlist (with optional filter) | `mcp__longbridge__watchlist` (returns all groups; LLM filters) |

MCP-only extensions: `mcp__longbridge__sharelist_*` — community-shared watchlists (8 tools: list / detail / create / update / delete / member_add / member_remove / popular). For *"hot lists"*, *"what's trending"*, route to `sharelist_*` directly.

## Related skills

- Watchlist mutations → `longbridge-watchlist-admin`
- Per-symbol quote / chart → `longbridge-quote`, `longbridge-kline`

## File layout

```
longbridge-watchlist/
├── SKILL.md
└── scripts/
    ├── cli.py
    └── test_cli.py
```
