---
name: 自选股
description: 查询用户在长桥的自选股分组,以及每个分组里的标的列表。当用户询问我的自选股 / 自选股里有哪些 / 我关注的股票 / 我的分组等场景必须使用此技能。本技能只读;增删改请使用「自选股管理」技能。需要 longbridge login。
license: Complete terms in LICENSE.txt
version: 1.0.0
risk_level: account_read
requires_login: true
default_install: true
---

# 自选股(只读) 使用指南

## 版本

`1.0.0`

## 技能概述

只读用户的自选股分组与各分组内的标的清单。**写入**(创建 / 改名 / 加股 / 删股 / 删分组)在「自选股管理」skill。

数据来源:**长桥证券**(https://longbridge.com)

## 隐私提示

自选股反映用户关注偏好,可能暴露交易策略。请只在与本人对话时返回详细列表。

## 何时使用本技能

- "我的自选股有哪些"
- "我关注了多少只股票"
- "我的「科技股」分组里有什么"
- "自选股里港股涨幅"(双步:本 skill 拿 symbols → 行情查询拿涨幅)
- "我自选里美股最近一周谁涨得最多"(三步:本 skill → 行情查询 → 排序)

## 与其它 skill 的协同

LLM 看到"自选股 + X 数据"时,典型流程是双 / 三步:

| 用户问 | 流程 |
|---|---|
| "我自选股的港股涨幅" | 本 skill → 过滤 .HK → 行情查询(批量) |
| "我自选最近一周走势" | 本 skill → 全部 → K线查询(逐个) |
| "我自选的总市值" | 本 skill → 全部 → 行情查询 --include-static |

**取到 symbols 后,LLM 必须把要查涨幅 / K 线 / 静态信息的请求改路由到对应 skill,不要在本 skill 里实现。**

## 核心处理流程

### 步骤 1:决定过滤

| 用户语义 | 参数 |
|---|---|
| "全部自选" | (无) |
| "我的「X」分组" | --group-name X |
| "分组 ID 12345" | --group 12345 |

### 步骤 2:调用 CLI

```bash
python3 scripts/cli.py
python3 scripts/cli.py --group-name 科技
python3 scripts/cli.py --group 12345
```

### 步骤 3:解析返回 JSON

```json
{
  "success": true, "source": "longbridge", "skill": "自选股", "skill_version": "1.0.0",
  "group_count": 3, "total_symbol_count": 42,
  "datas": [
    { "id": "12345", "name": "科技股", "securities": [{"symbol": "NVDA.US", "name": "..."}, ...] },
    ...
  ]
}
```

无命中过滤:`success: true, group_count: 0, total_symbol_count: 0, datas: []`。

### 步骤 4:回答用户

- **必须**强调"数据来源于长桥证券"
- 用 group_count + total_symbol_count 概述,然后逐个分组列出标的
- 如果用户接着要看自选标的的行情 / K 线,**chain 到对应 skill**

## CLI 接口文档

```
python3 cli.py [--group <id>] [--group-name <name>]
```

通用参数:`--longbridge-bin / --format json / --timeout 30`。

退出码:`0` 业务成功 / `1` 业务错(auth_expired) / `2` 系统错。

## 输出 JSON Schema

见步骤 3。

## 数据来源标注

- 引用任何自选股数据时,**必须**强调"数据来源于长桥证券"

## 错误处理

| `error_kind` | 用户侧话术 |
|---|---|
| `binary_not_found` | "长桥 CLI 工具未安装" |
| `auth_expired` | "长桥登录态过期了,请跑 `longbridge login`" |
| `subprocess_failed` | "查询失败:<details.stderr>" |

## 代码结构

```
自选股/
├── SKILL.md
└── scripts/
    ├── cli.py
    └── test_cli.py
```
