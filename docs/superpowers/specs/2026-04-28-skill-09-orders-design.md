# 订单与成交(skill #09)— 差异化设计

**Date:** 2026-04-28
**Status:** Draft
**Protocol:** 遵循 `2026-04-28-skill-platform-protocol.md`

## 业务范围

历史 / 当日订单与成交查询,加资金流水(出入金、分红、结算)。**只读**,不下单(下单见 #11)。

| 子命令 | 何时调 |
|---|---|
| `orders` | 用户问"今天的订单 / 历史订单 / X 标的的订单" |
| `order` | 用户问"订单 X 详情 / 这个订单成交了多少" |
| `executions` | 用户问"今天成交 / 历史成交 / X 标的的成交记录" |
| `cash-flow` | 用户问"出入金 / 分红记录 / 资金流水 / 账户结算" |

## front-matter

```yaml
---
name: 订单与成交
description: 查询账户订单(今日/历史/单条详情)、成交记录、资金流水(出入金 / 分红 / 结算)。当用户询问我的订单 / 这单成交了吗 / 历史成交 / 出入金记录 / 分红记录 / 资金流水等场景必须使用此技能。需要 longbridge login,只读不下单。
license: Complete terms in LICENSE.txt
version: 1.0.0
risk_level: account_read
requires_login: true
default_install: true
---
```

## scripts/cli.py 子命令风格

```
python3 cli.py orders     [--history] [--start YYYY-MM-DD] [--end YYYY-MM-DD] [--symbol <s>]
python3 cli.py order      <order_id>
python3 cli.py executions [--history] [--start ...] [--end ...] [--symbol <s>]
python3 cli.py cash-flow  [--start YYYY-MM-DD] [--end YYYY-MM-DD]
```

| 参数 | 适用 | 默认 | 说明 |
|---|---|---|---|
| `--history` | orders / executions | false | 切到历史模式 |
| `--start` `--end` | orders(history) / executions(history) / cash-flow | (按 longbridge 默认) | YYYY-MM-DD |
| `--symbol` | orders / executions | (空) | 过滤标的 |
| `<order_id>` | order | — | 必填 |

## 输出 JSON Schema

各子命令照搬原 longbridge JSON,顶层套 envelope + `subcommand` + 显式回写参数。

`order` 单条若查不到,按 protocol 走 `empty_result` 但**升级为业务错**(`success: false`,因为单条订单查不到通常是 ID 错):

```json
{
  "success": false, "source": "longbridge", "skill": "订单与成交", "skill_version": "1.0.0",
  "error_kind": "empty_result",
  "error": "未找到订单 <order_id>。请确认订单 ID 是否正确。",
  "details": { "subcommand": "order", "order_id": "..." }
}
```

其它子命令的空结果走默认 `success: true, datas: []`。

## SKILL.md 提示词差异

### `## 何时使用本技能` 列举

- "今天我下了哪些单"
- "上个月所有成交"
- "TSLA 历史订单"
- "订单 20240101-123456 详情"
- "我账户最近 30 天出入金"
- "上次分红是什么时候"
- "本月结算记录"

### 步骤 3 子命令路由

| 用户语义 | 子命令 |
|---|---|
| "今天 / 当前 / 我刚才下的单" | orders(无 --history)|
| "历史订单 / 上个月 / X 时间段订单" | orders --history --start --end |
| "X 标的的订单" | orders [--history] --symbol X |
| "订单 X 详情 / 这单成交了吗"(给定订单 ID) | order <id> |
| "今天成交 / fills" | executions(无 --history)|
| "历史成交 / X 时间段成交" | executions --history --start --end |
| "出入金 / 资金流水 / 分红 / 结算" | cash-flow [--start --end] |

### 时间窗推断

- "今天" → 不带 --start --end
- "上个月" → start = 上个月 1 号, end = 上个月最后一天
- "近 30 天" → start = today - 30, end = today
- "X 月 Y 日" → start = end = 该日

LLM 自己算日期,cli.py 只校验格式 `YYYY-MM-DD`。

### 隐私提示

同 #08:本技能返回订单 / 成交 / 资金流水属用户私有数据。

## 验收清单

- [ ] orders 当日:`cli.py orders` 返回当日订单数组
- [ ] orders 历史:`cli.py orders --history --start 2025-01-01 --end 2025-04-01` 返回数组
- [ ] orders 过滤:`--symbol TSLA.US` 只返该 symbol
- [ ] order 详情:用真实 order_id 跑通
- [ ] order 找不到:不存在的 ID → `empty_result` + success:false
- [ ] executions:同 orders 模式
- [ ] cash-flow:无参数返默认 30 天
- [ ] 集成层:6 句话验证
  - "今天我下了哪些单"
  - "上个月所有成交"
  - "TSLA 历史订单"
  - "订单 20240101-123456 详情"(用真订单 ID)
  - "近 30 天出入金"
  - "上次分红是什么时候"

## 已知 trade-off

- 订单 ID 格式不固定,cli.py 不校验,交给 longbridge 处理。
- "上次分红"需要在 cash-flow 里按 `business_type` 过滤,LLM 在 datas 上做(cli.py 不做业务过滤)。
