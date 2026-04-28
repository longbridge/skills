# 自选股管理(写)(skill #12)— 差异化设计

**Date:** 2026-04-28
**Status:** Draft
**Protocol:** 遵循 `2026-04-28-skill-platform-protocol.md`,有少量加严
**Related:** 只读版见 #10 自选股

## 业务范围

写入自选股:创建分组、改名、加股、删股、删分组。

| 子命令 | longbridge 子命令 |
|---|---|
| `create-group` | `watchlist create <NAME>` |
| `update-group` | `watchlist update <ID> [--name --add --remove --mode]` |
| `delete-group` | `watchlist delete <ID> [--purge]` |

## 风险定位

中等风险:
- **不影响金钱**:自选股纯粹是用户关注列表,改错最坏是 UI 上少几只股票
- 但**会改账户状态**,所以归 `mutating`,要 confirm gate(简化版,不需要 #11 那套五道 gate)

## front-matter

```yaml
---
name: 自选股管理
description: 创建自选股分组、改名、添加股票、删除股票、删除分组。⚠️ 本技能会修改用户账户的自选股状态,需要二次确认。当用户**清楚命令式**说"加到自选 / 创建分组 / 删除自选 / 删除分组"且给出具体参数时使用此技能。模糊询问("整理我的自选")必须先反问具体动作。需要 longbridge login。
license: Complete terms in LICENSE.txt
version: 1.0.0
risk_level: mutating
requires_login: true
default_install: true
---
```

注意:`default_install: true`(中等风险,可以默认装,但每次操作仍需 confirm flag)。比 #11 宽松。

## 安全 gate(简化版)

只保留两道:

### Gate 1 — 显式 `--confirm`

不带 `--confirm` 走 dry-run,打印将要执行的动作 + 涉及的分组/标的;带 `--confirm` 真执行。

LLM 必须二步:dry-run → 用户确认 → 真执行。

### Gate 2 — 二进制路径锁(同 #11 Gate 2)

防止把 cli.py 测试 binary 接到真账户。逻辑同 #11。

不需要 amount cap、forbidden list、audit log——这是自选股,改错可以再改回来。

## scripts/cli.py 子命令风格

```
python3 cli.py create-group <name> [--confirm]
python3 cli.py update-group <id> [--name <new_name>] [--add <symbol> ...] [--remove <symbol> ...] [--mode add|remove|replace] [--confirm]
python3 cli.py delete-group <id> [--purge] [--confirm]
```

参数与底层 longbridge watchlist 一致,本 cli.py 不二次映射。

## 输出 JSON Schema

**Dry-run**:

```json
{
  "success": true, "source": "longbridge", "skill": "自选股管理", "skill_version": "1.0.0",
  "dry_run": true,
  "subcommand": "update-group",
  "plan": { "group_id": "12345", "add": ["NVDA.US", "TSLA.US"], "remove": [], "rename": null },
  "next_step": "若用户明确确认,以完全相同的参数加 --confirm 重跑"
}
```

**真实成功**:

```json
{
  "success": true, ..., "dry_run": false,
  "subcommand": "create-group",
  "datas": { /* 原 longbridge watchlist create 返回,含 group_id */ }
}
```

**`risk_block`**(Gate 2 拒绝):同 #11 schema。

## SKILL.md 提示词差异

### `## 何时使用本技能` 列举

- "把 NVDA 加到自选股「科技股」分组"
- "创建分组「半导体」"
- "把 TSLA、AAPL、NVDA 都加到我自选股"
- "删除分组「科技股」里的 700.HK"
- "把分组「科技股」改名叫「美股科技」"
- "删除整个「测试」分组"

### 与 #10 的路由分工

LLM 看到的 description 区别:
- **本 skill**(#12):动词是"加 / 删 / 创建 / 改名"
- **#10 自选股**:动词是"看 / 列 / 查"

模糊问句:
- "整理我的自选" → LLM 反问"你想做什么(加股、删股、改名、删分组)?"
- "让自选股更整洁" → 同上反问

### 二步确认流程

跟 #11 一样:

1. LLM 第一次不带 `--confirm` 跑 cli.py
2. 把 dry-run 内容朗读给用户(包括分组名、要加/删的标的)
3. 等用户回复包含"确认 / yes / OK / 是的"
4. 第二次带 `--confirm` 真执行

SKILL.md 必须明确步骤 2 的"朗读"在删除分组时尤其重要——告诉用户分组里有几只标的、是否 `--purge`。

## 验收清单

- [ ] dry-run create:`cli.py create-group "Test"` 不带 confirm,返回 dry_run plan
- [ ] confirm create:加 `--confirm`,返回 group_id
- [ ] dry-run update add:返回 plan 包含 add 列表
- [ ] confirm update add:成功后调 #10 自选股 verify 标的真出现
- [ ] dry-run delete:返回 plan 包含 group_id;若 `--purge` 在 plan 里说明
- [ ] confirm delete:成功后调 #10 verify 分组消失
- [ ] Gate 2:`--longbridge-bin /tmp/foo` → risk_block
- [ ] auth_expired:登出后 → 通常 auth_expired
- [ ] 集成层:5 句话验证(在测试分组上)
  - "把 NVDA 加到自选股「Test」"
  - "创建分组「Test2」"
  - "改名「Test」为「Demo」"
  - "删除「Test2」分组"(LLM 应朗读"将删除分组 Test2,是否 --purge?")
  - "整理我的自选股"(LLM 应反问)

## 与 #10 / #11 的对比

| 维度 | #10 自选股(读) | #12 自选股管理(写) | #11 股票交易(写) |
|---|---|---|---|
| 风险等级 | account_read | mutating | mutating |
| default_install | true | true | **false** |
| 二步 confirm | 不需要 | 需要 | 需要 |
| Amount cap | 无 | 无 | 有 |
| Audit log | 无 | 无 | 有 |
| 二进制锁 | 无 | 有 | 有 |
