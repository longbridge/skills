---
name: 订单与成交
description: 查询账户订单(今日/历史/单条详情)、成交记录、资金流水(出入金 / 分红 / 结算)。当用户询问我的订单 / 这单成交了吗 / 历史成交 / 出入金记录 / 分红记录 / 资金流水等场景必须使用此技能。需要 longbridge login,只读不下单。
license: Complete terms in LICENSE.txt
version: 1.0.0
risk_level: account_read
requires_login: true
default_install: true
---

# 订单与成交 使用指南

## 版本

`1.0.0`

## 技能概述

只读账户订单 / 成交 / 资金流水(下单见**股票交易** skill,默认不安装):

- **orders**:今日订单(默认)或历史订单(--history),可按 symbol / 日期窗过滤
- **order**:单条订单完整详情(含手续费、状态历史)
- **executions**:今日成交(默认)或历史成交(--history)
- **cash-flow**:资金流水(出入金 / 分红 / 结算)

数据来源:**长桥证券**(https://longbridge.com)

## 隐私提示

订单 / 成交 / 资金流水属用户**账户私有数据**。请只在与本人对话时返回详细数字。

## 何时使用本技能

- "今天我下了哪些单"
- "上个月所有成交"
- "TSLA 历史订单"
- "订单 20240101-123456 详情"
- "我账户最近 30 天出入金"
- "上次分红是什么时候"
- "本月结算记录"

## 核心处理流程

### 步骤 1:决定子命令

| 用户语义 | 子命令 |
|---|---|
| "今天 / 当前 / 我刚才下的单" | orders(无 --history) |
| "历史订单 / 上个月 / X 时间段订单" | orders --history --start --end |
| "X 标的的订单" | orders [--history] --symbol X |
| "订单 X 详情 / 这单成交了吗"(给 order_id) | order <id> |
| "今天成交 / fills" | executions(无 --history) |
| "历史成交 / X 时间段成交" | executions --history --start --end |
| "出入金 / 资金流水 / 分红 / 结算" | cash-flow [--start --end] |

### 步骤 2:时间窗推断

- "今天" → 不带 --start --end
- "上个月" → start = 上个月 1 号, end = 上个月最后一天
- "近 30 天" → start = today - 30, end = today
- "X 月 Y 日" → start = end = 该日

LLM 自己算日期(用 today 当前日期),cli.py 只校验格式 YYYY-MM-DD。

### 步骤 3:调用工具(CLI 优先,必要时改 MCP)

**路径选择**:
- 本机有 CLI → 默认 `python3 scripts/cli.py`
- 本机无 CLI / `binary_not_found` → 改用末尾「MCP 备选」段的 `mcp__longbridge__today_orders` / `history_orders` / `order_detail` 等
- 用户问账单导出 / 报表期间统计 → CLI / 本 skill 不包,引导走 MCP 的 `statement_*` 工具
- **OAuth scope 提示**:本账户 token 若无交易 API scope,两条路都报 auth_expired

```bash
# 默认 cli.py 调用
python3 scripts/cli.py orders
python3 scripts/cli.py orders --history --start 2025-01-01 --end 2025-04-01 --symbol TSLA.US
python3 scripts/cli.py order 20240101-123456789
python3 scripts/cli.py executions --history --start 2025-01-01 --end 2025-04-01
python3 scripts/cli.py cash-flow --start 2025-04-01 --end 2025-04-30
```

### 步骤 4:解析返回 JSON

各子命令的 envelope:`success / source: "longbridge" / skill: "订单与成交" / skill_version / subcommand`,然后:

- orders / executions:`history` boolean + 可选 `start / end / symbol` + `datas`(数组)
- order:`order_id` + `datas`(对象,完整订单详情)
- cash-flow:可选 `start / end` + `datas`(数组)

### 步骤 5:回答用户

- **必须**强调"数据来源于长桥证券"
- 订单状态用中文:Filled→已成交, PartialFilled→部分成交, Canceled→已撤单, New→待成交, Rejected→被拒
- 表格化展示订单 / 成交记录;cash-flow 按 business_type 分类汇总
- "上次分红"在 cash-flow datas 上按 business_type 过滤(LLM 在结果里筛)

## CLI 接口文档

```
python3 cli.py orders     [--history] [--start YYYY-MM-DD] [--end YYYY-MM-DD] [--symbol <s>]
python3 cli.py order      <order_id>
python3 cli.py executions [--history] [--start YYYY-MM-DD] [--end YYYY-MM-DD] [--symbol <s>]
python3 cli.py cash-flow  [--start YYYY-MM-DD] [--end YYYY-MM-DD]
```

通用参数:`--longbridge-bin / --format json / --timeout 30`(历史长区间用 --timeout 60+)。

退出码:`0` 业务成功 / `1` 业务错(含 order 子命令查无此 ID 的 empty_result) / `2` 系统错。

## 输出 JSON Schema

见步骤 4。注意:`order` 子命令查不到时升级为业务错(success: false, error_kind: empty_result)。

## 数据来源标注

- 引用任何订单 / 成交 / 资金流水时,**必须**强调"数据来源于长桥证券"
- 没查到数据(空数组)时直接告诉用户"X 时间段无 X"

## 错误处理

| `error_kind` | 用户侧话术 |
|---|---|
| `binary_not_found` | "长桥 CLI 工具未安装" |
| `auth_expired` | "长桥登录态过期了,请跑 `longbridge login`" |
| `subprocess_failed` | "查询失败:<details.stderr>" |
| `no_input` | "请告诉我要查什么 / order_id" |
| `invalid_input_format` | "日期 / 标的格式不对:<details>" |
| `empty_result` | (仅 order 子命令)"未找到订单 <id>。请确认订单 ID。" |

## MCP 备选

| cli.py 子命令 | 等效 MCP 工具 |
|---|---|
| `orders`(当日) | `mcp__longbridge__today_orders` |
| `orders --history` | `mcp__longbridge__history_orders` |
| `order <id>` | `mcp__longbridge__order_detail` |
| `executions`(当日) | `mcp__longbridge__today_executions` |
| `executions --history` | `mcp__longbridge__history_executions` |
| `cash-flow` | `mcp__longbridge__cash_flow` |

MCP 拓展能力(CLI 没有):账单导出 `mcp__longbridge__statement_*`(详见账单 skill 路线)。

注意:同 #08 持仓,本账户 OAuth scope 不足时 cli.py 与 MCP 都会报 auth_expired。

## 代码结构

```
订单与成交/
├── SKILL.md
└── scripts/
    ├── cli.py
    └── test_cli.py
```
