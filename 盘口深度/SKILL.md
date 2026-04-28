---
name: 盘口深度
description: 查询股票盘口订单簿(5/10 档买卖盘)、经纪商队列、逐笔成交。当用户询问盘口、买卖盘、挂单、深度、经纪商队列、tick 数据、逐笔成交、机构资金等微观结构问题时必须使用此技能。支持港股/美股/A 股/新加坡;经纪商队列仅港股。
license: Complete terms in LICENSE.txt
version: 1.0.0
risk_level: read_only
requires_login: false
default_install: true
---

# 盘口深度 使用指南

## 版本

`1.0.0`

## 技能概述

微观结构三件套 + 一个组合:

- **depth**:订单簿深度(5/10 档买卖盘,每档含 price / volume / order_num)
- **brokers**:经纪商队列(每档列出 broker_id 数组,**仅港股**)
- **trades**:逐笔成交(time / price / volume / direction / type)
- **all**:一次取齐 depth + (brokers if .HK) + trades,综合问句用

数据来源:**长桥证券**(https://longbridge.com)

## 何时使用本技能

- "看下 700.HK 的盘口" / "TSLA 5 档买卖盘"
- "茅台经纪商队列"(LLM 必须告知"经纪商队列仅港股可查",换 depth 或换港股代码)
- "NVDA 最近 50 笔成交" / "腾讯 tick 数据"
- "看一下 700 全部盘口"(→ all)

## 核心处理流程

### 步骤 1:识别标的并补全为 `<CODE>.<MARKET>`(规则同行情查询)

### 步骤 2:决定子命令

| 用户语义 | 子命令 |
|---|---|
| "盘口" / "买卖盘" / "5/10 档" / "depth" | depth |
| "经纪商队列" / "机构挂单" + symbol 是 .HK | brokers |
| "经纪商队列" + symbol 非 .HK | LLM **必须告知**仅港股可查,改用 depth 或换为对应港股代码 |
| "逐笔" / "tick" / "最近 N 笔成交" | trades(--count N) |
| "全部盘口" / "微观结构全貌" | all |

### 步骤 3:调用工具(CLI 优先,必要时改 MCP)

**路径选择**:
- 本机有 CLI → 默认 `python3 scripts/cli.py`
- 本机无 CLI(`binary_not_found`)→ 改用末尾「MCP 备选」段的 `mcp__longbridge__depth / brokers / trades`(`all` 组合在 MCP 上需要 LLM 自己合并三次调用)
- 用户问空头持仓 / 期权成交量等 CLI 不支持的微观结构指标 → 直接走 MCP 拓展工具(见末尾备选段)

```bash
# 默认 cli.py 调用
python3 scripts/cli.py depth 700.HK
python3 scripts/cli.py trades 700.HK --count 50
python3 scripts/cli.py all 700.HK
```

### 步骤 4:解析返回 JSON

各子命令的 envelope 都含 `success / source: "longbridge" / skill: "盘口深度" / skill_version / subcommand / symbol`,然后:
- depth:`datas` 为 `{asks: [...], bids: [...]}`
- brokers:`datas` 为 `{asks: [...], bids: [...]}`,每档含 broker_id 数组
- trades:`datas` 为数组,顶层多 `count`
- all:`datas` 为 `{depth, brokers, trades}`,brokers 在非 HK 时为 null

### 步骤 5:回答用户

- **必须**强调"数据来源于长桥证券"
- depth 用表格展示买卖档位
- trades 用文字概述方向(主动买 / 主动卖比例)+ 列前几笔
- brokers 返回 broker_id 数字,要翻译成名字得调「证券查找」skill 的 participants

## 经纪商 ID 翻译(可选增强)

`brokers` 返回 broker_id 数字。要翻译成中文名,引导用户调用「证券查找」skill 的 `participants` 子命令。本 skill 不内置翻译,因为 broker 列表是另一个数据域。

## CLI 接口文档

```
python3 cli.py depth   <symbol>
python3 cli.py brokers <symbol>            # symbol 必须 .HK
python3 cli.py trades  <symbol> [--count 20]   # 1 ≤ count ≤ 1000
python3 cli.py all     <symbol> [--count 20]
```

通用参数:`--longbridge-bin / --format json / --timeout 30`。

退出码:`0` 业务成功 / `1` 业务错 / `2` 系统错。

## 输出 JSON Schema

见步骤 4。

## 数据来源标注

- 引用任何盘口、经纪商、逐笔数据时,**必须**强调"数据来源于长桥证券"
- 收盘后的盘口可能是收盘瞬间快照、trades 是当日最后 N 笔。**必须**告知用户当前是非交易时段
- 没查到数据时,引导用户去 https://longbridge.com 或长桥 App 确认

## 错误处理

| `error_kind` | 用户侧话术 |
|---|---|
| `binary_not_found` | "长桥 CLI 工具未安装,请先安装 longbridge-terminal: https://github.com/longportapp/longbridge-terminal" |
| `auth_expired` | "长桥登录态过期了,请在终端跑 `longbridge login` 重新授权" |
| `subprocess_failed` | "查询失败:<details.stderr>。可以稍后重试或检查参数。" |
| `no_input` | "请告诉我要查的标的(格式 <CODE>.<MARKET>)" |
| `invalid_input_format` | "代码格式不对:<details>。或经纪商队列仅港股可查,请改用 depth 或换港股代码。" |

## MCP 备选

cli.py 返回 `binary_not_found` 时回退:

| cli.py 子命令 | 等效 MCP 工具 |
|---|---|
| `depth` | `mcp__longbridge__depth` |
| `brokers` | `mcp__longbridge__brokers` |
| `trades` | `mcp__longbridge__trades` |
| `all` | 依次调上面三个 + 用 LLM 合并(MCP 没有 all 组合工具) |

MCP 拓展能力(CLI 没有):`mcp__longbridge__short_positions`(空头持仓)、`mcp__longbridge__option_volume`、`mcp__longbridge__option_volume_daily`。

## 代码结构

```
盘口深度/
├── SKILL.md
└── scripts/
    ├── cli.py
    └── test_cli.py
```
