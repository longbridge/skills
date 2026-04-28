---
name: 期权与窝轮
description: 查询期权合约行情、期权链(到期日 / strike)、港股窝轮行情、窝轮列表与发行商。当用户询问期权、option、call/put、行权价、到期日、IV、希腊字母、窝轮、牛熊证、认购证、认沽证等衍生品场景必须使用此技能。期权支持美股 / 港股,窝轮仅港股。
license: Complete terms in LICENSE.txt
version: 1.0.0
risk_level: read_only
requires_login: false
default_install: true
---

# 期权与窝轮 使用指南

## 版本

`1.0.0`

## 技能概述

衍生品行情五件套:

- **option-quote**:期权合约报价(IV / delta / strike / expiry)
- **option-chain**:期权链(列到期日,或给到期日列 strike)
- **warrant-quote**:窝轮报价(港股,杠杆比 / IV)
- **warrant-list**:某标的的窝轮列表(港股)
- **warrant-issuers**:窝轮发行商(港股)

数据来源:**长桥证券**(https://longbridge.com)

## 何时使用本技能

- "TSLA 下个月期权链" → option-chain 列到期日
- "AAPL 1 月 19 日的期权" → option-chain --date
- "AAPL240119C190000 现在多少"(完整 OCC 合约符) → option-quote
- "700.HK 的窝轮" / "腾讯牛熊证" → warrant-list
- "12345.HK 现在价格" → warrant-quote
- "港股窝轮发行商有哪些" → warrant-issuers

## 核心处理流程

### 步骤 1:决定子命令

| 用户语义 | 子命令 |
|---|---|
| OCC 期权符直接报价 | option-quote |
| underlying + "期权链 / option chain" | option-chain |
| underlying + 到期日 + "strike 列表" | option-chain --date |
| HK 窝轮代码报价 | warrant-quote |
| underlying + "窝轮 / 牛熊 / 认购证 / 认沽证" | warrant-list |
| "窝轮发行商" | warrant-issuers |
| underlying 非 .HK + warrant 关键词 | LLM **必须告知**"窝轮仅港股可查" |

### 步骤 2:期权两步发现

OCC 期权合约符格式:`<TICKER><YYMMDD><C|P><STRIKE×1000,8 位>`,例如 `AAPL240119C190000` = AAPL,2024-01-19 到期,Call,strike $190.00。

LLM 路由策略:
1. 用户给完整 OCC 符 → option-quote 直接查
2. 用户给 underlying + 到期 + strike + call/put → 先 option-chain --date 拿合约符,再 option-quote
3. 用户只给 underlying + 时间窗 → option-chain(列到期日),返回让用户挑

### 步骤 3:中文术语映射

LLM 自有知识:
- 认购证 / 牛证 / call → Call
- 认沽证 / 熊证 / put → Put
- 行权价 / strike price → Strike
- 到期日 / expiry → Expiry

### 步骤 4:调用 CLI

```bash
python3 scripts/cli.py option-quote AAPL250117C190000 AAPL250117P190000
python3 scripts/cli.py option-chain AAPL.US
python3 scripts/cli.py option-chain AAPL.US --date 2025-01-17
python3 scripts/cli.py warrant-list 700.HK
python3 scripts/cli.py warrant-issuers
```

### 步骤 5:解析返回 JSON

各子命令的 envelope:`success / source: "longbridge" / skill: "期权与窝轮" / skill_version / subcommand / datas`,然后:

- option-quote:`count / contracts / datas`(数组,每条含 IV / delta / strike / expiry)
- option-chain 不带 date:`underlying / datas`(对象,含 expiry_dates 数组)
- option-chain 带 date:`underlying / date / datas`(数组,每条含 strike / call_symbol / put_symbol)
- warrant-quote:`count / warrants / datas`
- warrant-list:`underlying / datas`(数组)
- warrant-issuers:`datas`(数组)

### 步骤 6:回答用户

- **必须**强调"数据来源于长桥证券"
- 期权链返回的到期日列表可以全展示;strike 列表如果太多(>30)挑近 ATM 的展示
- 希腊字母 / IV 用"中文 + 数字"格式(如"隐含波动率 32.5%")

## CLI 接口文档

```
python3 cli.py option-quote    <contract> [<contract> ...]
python3 cli.py option-chain    <underlying> [--date YYYY-MM-DD]
python3 cli.py warrant-quote   <warrant> [<warrant> ...]
python3 cli.py warrant-list    <underlying>           # underlying 必须 .HK
python3 cli.py warrant-issuers
```

通用参数:`--longbridge-bin / --format json / --timeout 30`。

退出码:`0` 业务成功 / `1` 业务错 / `2` 系统错。

## 输出 JSON Schema

见步骤 5。

## 数据来源标注

- 引用任何衍生品数据时,**必须**强调"数据来源于长桥证券"
- IV、delta 等希腊字母数据可能在收盘后是上一交易日快照,SKILL 不强制说明,但用户问"实时"时要解释当前是非交易时段

## 错误处理

| `error_kind` | 用户侧话术 |
|---|---|
| `binary_not_found` | "长桥 CLI 工具未安装" |
| `auth_expired` | "长桥登录态过期了,请跑 `longbridge login`" |
| `subprocess_failed` | "查询失败:<details.stderr>" |
| `no_input` | "请告诉我合约 / 标的代码" |
| `invalid_input_format` | "代码或日期格式不对;窝轮仅港股可查" |

## MCP 备选

| cli.py 子命令 | 等效 MCP 工具 |
|---|---|
| `option-quote` | `mcp__longbridge__option_quote` |
| `option-chain`(无 date) | `mcp__longbridge__option_chain_expiry_date_list` |
| `option-chain --date` | `mcp__longbridge__option_chain_info_by_date` |
| `warrant-quote` | `mcp__longbridge__warrant_quote` |
| `warrant-list` | `mcp__longbridge__warrant_list` |
| `warrant-issuers` | `mcp__longbridge__warrant_issuers` |

MCP 拓展能力:`mcp__longbridge__option_volume`、`mcp__longbridge__option_volume_daily`(期权成交量分析,CLI 没有)。

## 代码结构

```
期权与窝轮/
├── SKILL.md
└── scripts/
    ├── cli.py
    └── test_cli.py
```
