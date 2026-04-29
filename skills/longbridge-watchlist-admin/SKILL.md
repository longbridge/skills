---
name: longbridge-watchlist-admin
description: |
  Mutating operations on the user's Longbridge watchlist — create group, rename group, add / remove symbols, delete group (optionally purging members). Requires longbridge login. Every mutation requires a two-step dry-run + confirm protocol. Use only when the user gives a clear imperative ("add X to favourites", "delete the Tech group"); ambiguous prompts ("organise my watchlist") must ask back. Triggers: "把 X 加到自选", "添加到自选", "创建自选分组", "删除自选", "删除分组", "改名分组", "把 X 加到自選", "新增至自選", "建立自選分組", "刪除自選", "刪除分組", "重新命名", "add to watchlist", "create watchlist group", "remove from watchlist", "delete group", "rename group", "watchlist edit".
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: mutating
  requires_login: true
  default_install: true
---

# longbridge-watchlist-admin

⚠️ **Mutating skill**: changes the user's watchlist state on Longbridge. No money is involved, but the change is persistent.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## Two-step protocol (mandatory)

Every mutation runs **twice**:

1. **Dry-run**: first call `cli.py` **without `--confirm`**. The CLI returns `dry_run: true` with the plan it would execute.
2. **Read the plan back to the user verbatim** (group name, symbols added / removed, `--purge` y/n) and wait for **explicit confirmation** containing "确认 / yes / 是的 / confirm".
3. **Confirm**: re-run `cli.py` with **identical args + `--confirm`**.

If the user does not clearly confirm, **ask again** — do **not** silently re-run with `--confirm`.

> Never combine dry-run and the real write into one MCP call. MCP write tools have no dry-run concept; the SKILL is responsible for the confirmation gate.

## Subcommands

| Subcommand | Use when |
|---|---|
| `create-group <name>` | New watchlist group |
| `update-group <group_id> [--name <new>] [--add <s>...] [--remove <s>...] [--mode add|remove|replace]` | Rename, add, remove, or replace symbols in an existing group |
| `delete-group <group_id> [--purge]` | Delete the group (with `--purge` also removes member stocks) |

## Routing to read skill

If the user gives a group name (not id), call `longbridge-watchlist` first to look up the `group_id`, then run mutations here.

| User says | Skill |
|---|---|
| 看 / list / show | `longbridge-watchlist` (read) |
| 加 / 删 / 创建 / 改名 | `longbridge-watchlist-admin` (this skill) |

For ambiguous prompts (*"整理我的自选"*) — **ask** what specific action the user wants.

## CLI

Dry-run examples (no `--confirm`):

```bash
python3 scripts/cli.py create-group "科技股"
python3 scripts/cli.py update-group 12345 --add NVDA.US --add AAPL.US
python3 scripts/cli.py update-group 12345 --name "美股科技"
python3 scripts/cli.py update-group 12345 --remove 700.HK
python3 scripts/cli.py delete-group 12345
python3 scripts/cli.py delete-group 12345 --purge
```

After explicit confirmation, append `--confirm` to the same command.

## Read-back templates (LLM)

> 即将{动作}:{plan 摘要}。是否确认执行?
>
> About to {action}: {plan summary}. Confirm?
>
> 即將{動作}:{plan 摘要}。是否確認執行?

Examples:
- *"即将创建自选股分组「科技股」。是否确认执行?"*
- *"About to add NVDA.US, AAPL.US to group 12345. Confirm?"*
- *"即將刪除分組 12345(`--purge`:同時刪除分組內全部股票)。是否確認?"*

## Safety gates

| Gate | Enforced by |
|---|---|
| `--confirm` gate | Without `--confirm`, the CLI never calls Longbridge — only emits the plan |
| Binary-lock | When `--confirm` is set, `--longbridge-bin` must equal `shutil.which("longbridge")`. Arbitrary paths (test fakes) trigger `risk_block`, exit 2 |

## Output

**Dry-run**:

```json
{
  "success": true, "dry_run": true, "subcommand": "create-group",
  "plan": { "action": "create-group", "name": "科技股" },
  "next_step": "If the user confirms, re-run with the same args plus --confirm."
}
```

**Real write**:

```json
{ "success": true, "dry_run": false, "subcommand": "create-group", "datas": { ... } }
```

**Risk block**:

```json
{ "success": false, "error_kind": "risk_block",
  "error": "...", "details": { "gate": "binary_locked", ... } }
```

## OAuth scope

Same as account skills: requires trade scope. Lacking scope → `auth_expired` from both CLI and MCP.

## MCP fallback (after confirmation only)

| CLI subcommand | MCP tool |
|---|---|
| `create-group` | `mcp__longbridge__create_watchlist_group` |
| `update-group` | `mcp__longbridge__update_watchlist_group` |
| `delete-group` | `mcp__longbridge__delete_watchlist_group` |

> **Important**: the dry-run / confirm cycle still applies. Do the dry-run with `cli.py` (no `--confirm`); only after the user confirms may you call the MCP write tool (or `cli.py --confirm`).

## File layout

```
longbridge-watchlist-admin/
├── SKILL.md
└── scripts/
    ├── cli.py
    └── test_cli.py
```
