---
name: 自选股管理
description: 创建自选股分组、改名、添加股票、删除股票、删除分组。⚠️ 本技能会修改用户账户的自选股状态,需要二次确认。当用户**清楚命令式**说"加到自选 / 创建分组 / 删除自选 / 删除分组"且给出具体参数时使用此技能。模糊询问("整理我的自选")必须先反问具体动作。需要 longbridge login。
license: Complete terms in LICENSE.txt
version: 1.0.0
risk_level: mutating
requires_login: true
default_install: true
---

# 自选股管理(写) 使用指南

## 版本

`1.0.0`

## ⚠️ 高风险提示

**本技能会修改用户账户的自选股状态**(创建分组、加股、删股、删分组)。虽然不影响金钱,但改错可能导致用户的关注列表丢失或污染。

**必须严格遵守二步确认流程**(见下)。

## 技能概述

- **create-group**:新建自选分组
- **update-group**:改分组名 / 加股 / 删股 / 替换股票列表
- **delete-group**:删除分组(可选 --purge 同时删除分组内股票)

数据来源 / 写入目标:**长桥证券**(https://longbridge.com)

读取自选股请使用「自选股」(只读) skill。

## 二步确认流程(强制)

每次写入操作:

1. **第一步:dry-run**
   LLM 第一次跑 cli.py **不带 `--confirm`**。cli.py 返回 `dry_run: true` + plan 详情。

2. **第二步:朗读 + 等待用户确认**
   LLM 把 plan 内容**逐字朗读给用户**(分组名、要加 / 删的标的、是否 --purge 等)。然后等待用户回复**包含"确认"或"yes"或"是的"** 的明确同意。

3. **第三步:真实写入**
   LLM 第二次跑 cli.py,加 `--confirm`,完全相同的参数。

如果用户没明确确认,**必须再问一遍**,不要直接 --confirm 重跑。

## 何时使用本技能

- "把 NVDA 加到自选股「科技股」分组"
- "创建分组「半导体」"
- "把 TSLA、AAPL、NVDA 都加到我自选股"
- "删除分组「科技股」里的 700.HK"
- "把分组「科技股」改名叫「美股科技」"
- "删除整个「测试」分组"

模糊问句:
- "整理我的自选" → LLM **必须反问**:"想做什么具体动作:加股、删股、改名、删分组?"

## 与「自选股(只读)」skill 的路由

- 动词是"看 / 列 / 查" → 自选股(读)
- 动词是"加 / 删 / 创建 / 改名" → 本 skill

## 核心处理流程

### 步骤 1:决定子命令

| 用户语义 | 子命令 |
|---|---|
| "建分组 / 新建 / 创建" | create-group |
| "加股 / 添加 / 收藏到 / 改名" | update-group(--add / --name) |
| "删股 / 移除"(从某分组) | update-group --remove |
| "删分组 / 删整个 X" | delete-group(询问是否 --purge) |

### 步骤 2:取分组 ID(若需要)

update-group / delete-group 必须先有 `group_id`。如果用户给了分组名,先用「自选股(只读)」skill 查 group_id,再用本 skill 操作。

### 步骤 3:Dry-run 调用

```bash
# create
python3 scripts/cli.py create-group "科技股"

# update: 加股
python3 scripts/cli.py update-group 12345 --add NVDA.US --add AAPL.US

# update: 改名
python3 scripts/cli.py update-group 12345 --name "美股科技"

# update: 删股
python3 scripts/cli.py update-group 12345 --remove 700.HK

# delete
python3 scripts/cli.py delete-group 12345          # 不删股票
python3 scripts/cli.py delete-group 12345 --purge  # 同时删股票
```

返回 dry-run plan,LLM 朗读后等用户确认。

### 步骤 4:朗读 plan + 等用户确认

朗读模板:
> 即将{动作}:{plan 摘要}。是否确认执行?

例如:
> 即将创建自选股分组「科技股」。是否确认执行?
> 即将向分组 12345 添加 NVDA.US, AAPL.US。是否确认执行?
> 即将删除分组 12345 (--purge:同时删除分组内全部股票)。是否确认执行?

### 步骤 5:Confirm 调用

完全相同的参数,加 `--confirm`:

```bash
python3 scripts/cli.py create-group "科技股" --confirm
```

### 步骤 6:回答用户

返回 `dry_run: false, datas: ...`,告诉用户操作完成,引用"长桥证券"作为数据源。

## CLI 接口文档

```
python3 cli.py create-group <name> [--confirm]
python3 cli.py update-group <group_id> [--name <new>] [--add <s> ...] [--remove <s> ...] [--mode add|remove|replace] [--confirm]
python3 cli.py delete-group <group_id> [--purge] [--confirm]
```

通用参数:`--longbridge-bin / --format json / --timeout 30 / --confirm`。

退出码:`0` dry-run 或写入成功 / `1` 业务错 / `2` 系统错 / `risk_block`。

## 安全 Gate

- **Gate 1(--confirm gate)**:不带 `--confirm` 走 dry-run。
- **Gate 2(binary lock)**:`--confirm` 模式下,`--longbridge-bin` 只接受 PATH 上的 `longbridge`。任意路径(测试 fake binary)直接 `risk_block`,exit 2。

## 输出 JSON Schema

**Dry-run**:

```json
{
  "success": true, "dry_run": true, "subcommand": "create-group",
  "plan": { "action": "create-group", "name": "科技股" },
  "next_step": "若用户明确确认,以完全相同的参数加 --confirm 重跑 cli.py"
}
```

**真实写入成功**:

```json
{
  "success": true, "dry_run": false, "subcommand": "create-group",
  "datas": { /* 原 longbridge watchlist create 返回 */ }
}
```

**Risk block**:

```json
{
  "success": false, "error_kind": "risk_block",
  "error": "...",
  "details": { "gate": "binary_locked", ... }
}
```

## 数据来源标注

- 操作通过**长桥证券**完成,以长桥 App 内显示为准
- 操作完成后引导用户去 App 验证

## 错误处理

| `error_kind` | 用户侧话术 |
|---|---|
| `binary_not_found` | "长桥 CLI 工具未安装" |
| `auth_expired` | "长桥登录态过期了,请跑 `longbridge login`" |
| `subprocess_failed` | "操作失败:<details.stderr>。可能是分组 ID 不存在,或 symbol 格式不对。" |
| `no_input` | "请告诉我具体参数(分组 ID / 名字 / 要加的股票)" |
| `invalid_input_format` | "参数格式不对:<details>" |
| `risk_block` | "出于安全考虑,本技能 --confirm 时只接受 PATH 上的 longbridge,不接受任意路径" |

## MCP 备选

| cli.py 子命令 | 等效 MCP 工具 |
|---|---|
| `create-group` | `mcp__longbridge__create_watchlist_group` |
| `update-group` | `mcp__longbridge__update_watchlist_group` |
| `delete-group` | `mcp__longbridge__delete_watchlist_group` |

**重要**:走 MCP 路径时,**仍然必须遵守 dry-run + confirm 双步流程**。LLM 第一次不直接调 MCP 写工具;先用本 cli.py 跑一次 dry-run(不带 --confirm,不接 longbridge)拿到 plan → 朗读给用户 → 等"确认" → 第二次才调 MCP 写工具(或带 --confirm 调 cli.py)。

MCP 是无 dry-run 概念的纯写工具,SKILL 层负责确认流程,不能让 LLM 直接 MCP 一步到位。

## 代码结构

```
自选股管理/
├── SKILL.md
└── scripts/
    ├── cli.py
    └── test_cli.py
```
