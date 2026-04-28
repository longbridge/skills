# 实时订阅(skill #13)— 差异化设计

**Date:** 2026-04-28
**Status:** Draft (优先级 P3,最低)
**Protocol:** 遵循 `2026-04-28-skill-platform-protocol.md`

## 业务范围

查询当前会话的活跃 WebSocket 订阅。包装 `longbridge subscriptions`。

**这是 P3 优先级**——日常 LLM-driven 用例几乎不需要,主要用于诊断"为什么我没收到推送"或开发联调。如果验收 P0/P1/P2 后发现没有用户调用,可以删掉。

## front-matter

```yaml
---
name: 实时订阅
description: 查询当前长桥会话活跃的实时数据订阅(WebSocket 订阅的标的、订阅类型、K 线 period)。当用户问"我订阅了哪些实时数据 / 当前推送状态 / 实时连接情况"等场景使用此技能。仅用于诊断和开发,日常无需。
license: Complete terms in LICENSE.txt
version: 1.0.0
risk_level: account_read
requires_login: true
default_install: false
---
```

`default_install: false`——不批量装,需要时手动 symlink。理由:LLM 路由器看到这种诊断 skill 容易误触发("订阅"是个常见词)。

## scripts/cli.py 接口

无子命令,无参数:

```
python3 cli.py
```

## 输出 JSON Schema

```json
{
  "success": true, "source": "longbridge", "skill": "实时订阅", "skill_version": "1.0.0",
  "subscription_count": 5,
  "datas": [ /* 原 subscriptions 数组,每条 {symbol, sub_types, candlestick_periods} */ ]
}
```

空订阅:`success: true, subscription_count: 0, datas: []`。

## SKILL.md 提示词差异

### `## 何时使用本技能` 列举

- "我现在订阅了哪些实时推送"
- "实时连接状态"
- "为什么没收到 NVDA 实时报价"(诊断用)

模糊触发("订阅怎么样" / "实时数据") → LLM 应反问是不是问推送状态。否则容易跟"自选股 / 行情查询"混淆。

## 验收清单

- [ ] 跑通:`cli.py` 返回 subscription_count(可能是 0)
- [ ] auth_expired:登出后 → auth_expired
- [ ] 集成层:2 句话验证(更多 LLM 路由测试用例不必要)
  - "我现在订阅了什么"
  - "实时连接状态"
