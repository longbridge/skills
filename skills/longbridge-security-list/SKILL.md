---
name: longbridge-security-list
description: |
  Securities directory and HK broker participant directory via Longbridge Securities — full listed-stock catalog (symbol, English name, Chinese name) per market, and HK broker_id ↔ name lookup. Triggers: "港股一共多少只", "美股 listed", "经纪商 ID", "broker_id", "全部股票列表", "港股全部股票", "港股一共多少", "經紀商 ID", "list of stocks", "all listed stocks", "broker directory", "participant lookup".
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: read_only
  requires_login: false
  default_install: true
---

# longbridge-security-list

Catalog lookups: full listed-securities lists per market, and the HK broker_id → name dictionary.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## Subcommands

| Subcommand | Returns |
|---|---|
| `securities --market HK | US | CN | SG` | All listed securities `[{symbol, name_en, name_cn}]`. Large payload (HK ≈ 2.5k, CN ≈ 5k+). |
| `participants` | HK broker directory `[{broker_id, name_en, name_cn}]`. |

## When to use

- *"港股一共有多少只股票"*, *"US listed count"* → `securities`
- *"经纪商 ID 9000 是谁"*, *"broker 0001"* → `participants`
- *"翻译一下经纪商列表"* → `participants`
- *"列出 A 股全部股票"* → ask user to narrow scope (industry, name search) and route to `longbridge-quote` for individual lookups

## Usage rules

- Reply with `count` for "how many" questions; do **not** dump full `datas`.
- For broker_id translation, grep `datas` for the specific id.
- For the full broker directory, list up to 100 rows; for more, return total count and ask user which IDs to translate.
- For "list all stocks" requests, ask the user to filter (industry / market / name search) and route them to `longbridge-quote`.

## CLI

```bash
longbridge security-list HK   --format json
longbridge security-list US   --format json
longbridge participants       --format json
```

`security-list` returns a large payload (HK ≈ 2.5k rows, CN ≈ 5k+); allow extra time for the call.

## Output

- `security-list`: array of `{symbol, name_en, name_cn}`.
- `participants`: array of `{broker_id, name_en, name_cn}`.

## Path-selection note

`participants` → CLI is preferred (local subprocess, faster). `security-list` → **MCP is preferred** because the current `longbridge` CLI has an intermittent `param_error` for that endpoint; MCP bypasses the CLI by calling the SDK directly.

## Error handling

If `longbridge` is missing, fall back to MCP. On `security-list`, if stderr includes `param_error`, switch to `mcp__longbridge__security_list` instead — this is a known CLI issue.

## MCP fallback / preferred

| CLI subcommand | MCP tool | Note |
|---|---|---|
| `security-list` | `mcp__longbridge__security_list` | **Prefer MCP** if available |
| `participants` | `mcp__longbridge__participants` | CLI fine |

## Related skills

- Single quote / static → `longbridge-quote`
- broker_id appears in → `longbridge-depth` (broker queue)

## File layout

```
longbridge-security-list/
└── SKILL.md          # prompt-only, no scripts/
```
