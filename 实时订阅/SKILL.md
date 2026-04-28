---
name: 实时订阅
description: 查询当前长桥会话活跃的实时数据订阅(WebSocket 订阅的标的、订阅类型、K 线 period)。当用户问"我订阅了哪些实时数据 / 当前推送状态 / 实时连接情况"等场景使用此技能。仅用于诊断和开发,日常无需。
license: Complete terms in LICENSE.txt
version: 1.0.0
risk_level: account_read
requires_login: true
default_install: false
---

# 实时订阅 使用指南

## 版本

`1.0.0`

## 技能概述

返回当前长桥会话的活跃 WebSocket 订阅清单(symbol / sub_types / candlestick_periods)。**主要用于诊断**,日常 LLM 用例少。

`default_install: false` —— 不批量安装,需要时手动 symlink。

数据来源:**长桥证券**(https://longbridge.com)

## 何时使用本技能

- "我现在订阅了哪些实时推送"
- "实时连接状态"
- "为什么没收到 NVDA 实时报价"(诊断用)

模糊问句:
- "订阅怎么样" / "实时数据" → LLM 应**反问**是不是问推送状态(避免与「自选股」/「行情查询」混淆)

## 核心处理流程

直接调:

```bash
python3 scripts/cli.py
```

返回:

```json
{
  "success": true, "source": "longbridge", "skill": "实时订阅", "skill_version": "1.0.0",
  "subscription_count": 5,
  "datas": [{"symbol": "NVDA.US", "sub_types": ["quote", "depth"], "candlestick_periods": [...]}, ...]
}
```

回答时**必须**强调"数据来源于长桥证券"。

## CLI 接口文档

```
python3 cli.py
```

通用参数:`--longbridge-bin / --format json / --timeout 30`。

退出码:`0` 业务成功 / `1` 业务错 / `2` 系统错。

## 输出 JSON Schema

见上。

## 数据来源标注

- 引用任何订阅数据时,**必须**强调"数据来源于长桥证券"

## 错误处理

| `error_kind` | 用户侧话术 |
|---|---|
| `binary_not_found` | "长桥 CLI 工具未安装" |
| `auth_expired` | "长桥登录态过期了,请跑 `longbridge login`" |
| `subprocess_failed` | "查询失败:<details.stderr>" |

## MCP 备选

**MCP 没有等效工具。** longbridge-mcp 是无状态 HTTP 服务,本身没有 WebSocket 订阅会话的概念,不存在"列出当前订阅"这种查询。本 skill 必须依赖本机 `longbridge` CLI(它维护着 OAuth + WebSocket 长连接)。

如果 cli.py 返回 `binary_not_found`,告诉用户:本 skill 仅本机可用,需要装 longbridge-terminal。

## 代码结构

```
实时订阅/
├── SKILL.md
└── scripts/
    ├── cli.py
    └── test_cli.py
```
