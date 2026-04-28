# 盘口深度(skill #03)— 差异化设计

**Date:** 2026-04-28
**Status:** Draft
**Protocol:** 遵循 `2026-04-28-skill-platform-protocol.md`

## 业务范围

微观结构三件套:订单簿深度 + 经纪商队列 + 逐笔成交。

| 子命令 | 何时调 | 适用市场 |
|---|---|---|
| `depth` | 用户问"盘口"、"5 档"、"买卖盘"、"挂单" | 全部 |
| `brokers` | 用户问"经纪商队列"、"机构挂单" | **仅 HK**(底层 CLI 限制) |
| `trades` | 用户问"逐笔"、"tick"、"最近成交" | 全部 |

## front-matter

```yaml
---
name: 盘口深度
description: 查询股票盘口订单簿(5/10 档买卖盘)、经纪商队列、逐笔成交。当用户询问盘口、买卖盘、挂单、深度、经纪商队列、tick 数据、逐笔成交、机构资金等微观结构问题时必须使用此技能。支持港股/美股/A 股/新加坡;经纪商队列仅港股。
license: Complete terms in LICENSE.txt
version: 1.0.0
risk_level: read_only
requires_login: false
default_install: true
---
```

## scripts/cli.py 子命令风格

```
python3 cli.py depth   <symbol>
python3 cli.py brokers <symbol>                # symbol 必须 .HK,否则 invalid_input_format
python3 cli.py trades  <symbol> [--count 20]   # 1 ≤ count ≤ 1000
python3 cli.py all     <symbol> [--count 20]   # 一次取 depth + (brokers if .HK) + trades
```

`all` 是为"看一下 700.HK 全部盘口"这种综合问句设计的,LLM 用一次调用覆盖。

| 参数 | 适用 | 默认 | 说明 |
|---|---|---|---|
| `<symbol>` | 全部 | — | 必填,单标的 |
| `--count` | trades / all | `20` | 1-1000 整数,超出 → `invalid_input_format` |

## 输出 JSON Schema

**`depth`**:

```json
{
  "success": true, "source": "longbridge", "skill": "盘口深度", "skill_version": "1.0.0",
  "subcommand": "depth",
  "symbol": "700.HK",
  "datas": { /* 原 depth JSON 对象,含 asks[] / bids[],每档 {price, volume, order_num} */ }
}
```

**`brokers`**:

```json
{
  "success": true, ...,
  "subcommand": "brokers",
  "symbol": "700.HK",
  "datas": { /* 原 brokers JSON,asks/bids 每档列出 broker_id 数组 */ }
}
```

**`trades`**:

```json
{
  "success": true, ...,
  "subcommand": "trades",
  "symbol": "700.HK", "count": 20,
  "datas": [ /* 原 trades 数组,每条 {timestamp, price, volume, direction, trade_type} */ ]
}
```

**`all`**:

```json
{
  "success": true, ...,
  "subcommand": "all",
  "symbol": "700.HK",
  "datas": {
    "depth": { ... },
    "brokers": { ... } | null,    // null 当 symbol 非 .HK
    "trades": [ ... ]
  }
}
```

## SKILL.md 提示词差异

### `## 何时使用本技能` 列举

- "看下 700.HK 的盘口" / "TSLA 5 档买卖盘"
- "茅台经纪商队列"(LLM 应反问或直接换为深度查询,因为只有港股有 brokers)
- "NVDA 最近 50 笔成交"
- "腾讯 tick 数据"
- "看一下 700 全部盘口"(→ `all`)

### 步骤 3 子命令路由

| 用户语义 | 子命令 |
|---|---|
| "盘口"/"买卖盘"/"5 档" | depth |
| "经纪商队列"/"机构挂单" + symbol 是 `.HK` | brokers |
| "经纪商队列"/"机构挂单" + symbol 非 `.HK` | LLM **必须告知用户**:经纪商队列仅港股可查,然后改用 depth |
| "逐笔"/"tick"/"最近 N 笔成交" | trades(N → --count) |
| "全部盘口"/"看一下 X 微观结构" | all |

### 经纪商 ID 翻译(可选增强)

`brokers` 返回的 `broker_id` 是数字,要翻译成名字得调 `participants`(在 #07 证券查找 skill)。本 skill 不做翻译,SKILL.md 提示 LLM:**如果用户要看经纪商名字而不是 ID,引导调用 `证券查找` skill 的 `participants` 子命令**,或在回答里说"完整名字请查询经纪商列表"。

## 验收清单

- [ ] depth:`cli.py depth 700.HK` 返回 asks/bids 数组(非空)
- [ ] brokers HK:`cli.py brokers 700.HK` 返回非空 datas
- [ ] brokers 非 HK 拒绝:`cli.py brokers TSLA.US` → `invalid_input_format`(stderr 解释)
- [ ] trades:`cli.py trades 700.HK --count 50` 返回 50 条
- [ ] count 边界:`--count 0` 与 `--count 1001` 都 → `invalid_input_format`
- [ ] all:`cli.py all 700.HK` 三个子字段齐全;`cli.py all TSLA.US` brokers 字段为 null
- [ ] 集成层:5 句话验证
  - "看下 700.HK 盘口"
  - "TSLA 最近 30 笔成交"
  - "茅台经纪商队列"(LLM 应解释只有港股可查)
  - "看下 9988.HK 全部盘口"
  - "NVDA 5 档"

## 已知 trade-off

- 收盘后 `depth` 返回的可能是收盘瞬间快照,`trades` 返回的是当日最后 N 笔。SKILL.md 让 LLM 提示用户当前是非交易时段。
- `all` 子命令同时跑 3 个子进程,任一失败按 protocol 整体失败上抛,不做 partial success。
