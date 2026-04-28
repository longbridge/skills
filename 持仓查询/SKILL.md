---
name: 持仓查询
description: 查询账户股票持仓 / 基金持仓 / 现金余额 / 融资额度,以及标的保证金率与可买可卖最大数量。当用户询问我的持仓 / 我有多少钱 / 账户余额 / 我能买多少股 X / X 保证金率 / 风险等级等账户级问题时必须使用此技能。需要 longbridge login。
license: Complete terms in LICENSE.txt
version: 1.0.0
risk_level: account_read
requires_login: true
default_install: true
---

# 持仓查询 使用指南

## 版本

`1.0.0`

## 技能概述

账户全景"我有什么 + 我有多少钱 + 我能买多少 + 保证金率":

- **portfolio**:三件套合一(持仓 + 基金 + 余额)
- **positions**:股票持仓
- **funds**:基金持仓
- **balance**:现金余额 + 融资额度(可按币种过滤)
- **margin-ratio**:标的保证金率(initial / maintenance / forced liquidation factor)
- **max-qty**:估算可买 / 可卖最大数量(纯现金 + 含融资)

数据来源:**长桥证券**(https://longbridge.com)

## 何时使用本技能

- "我的持仓" / "我现在持有什么"
- "账户余额多少" / "我有多少美金 / 港币"
- "我的基金持仓"
- "NVDA 我能买多少股" / "TSLA 全仓买能买多少"
- "茅台保证金率"
- "看一下我的账户全貌"(→ portfolio)

## 隐私提示

本技能返回的持仓 / 余额 / 保证金等数据是用户**账户私有信息**。请只在与本人对话时返回详细数字;若怀疑会话上下文有第三方观察(截图、屏幕共享),先与用户确认是否要展示。

## 核心处理流程

### 步骤 1:决定子命令

| 用户语义 | 子命令 |
|---|---|
| "持仓 / 我持有 / 我有什么股票" | positions |
| "基金持仓" | funds |
| "余额 / 现金 / X 货币多少钱" | balance(--currency 推断) |
| "X 我能买多少 / 全仓买" | max-qty --side buy |
| "X 我能卖多少" | max-qty --side sell |
| "X 保证金率 / 仓位 / 杠杆要求" | margin-ratio |
| "账户全貌 / 整个账户 / portfolio" | portfolio |
| "我能赚多少 / 浮盈" | positions(LLM 在 datas 上算 (last - cost) × qty) |

### 步骤 2:max-qty 的两步流程

用户说"X 我能买多少股"时:
1. 限价单(默认 LO):LLM 必须先用「行情查询」skill 拿到 X 的当前价 → 填 --price
2. 市价单(MO):无需 --price,加 --order-type MO
3. 返回 cash_max_qty(纯现金) 与 margin_max_qty(含融资);回答时要区分两者并提示融资风险

### 步骤 3:调用 CLI

```bash
python3 scripts/cli.py portfolio
python3 scripts/cli.py positions
python3 scripts/cli.py balance --currency USD
python3 scripts/cli.py margin-ratio TSLA.US
python3 scripts/cli.py max-qty TSLA.US --side buy --price 250
```

### 步骤 4:解析返回 JSON

各子命令的 envelope:`success / source: "longbridge" / skill: "持仓查询" / skill_version / subcommand / datas`,然后:

- portfolio:`datas` 为对象,含 `positions / fund_positions / balance` 三个子字段
- positions / funds:`datas` 为数组
- balance:`datas` 为数组(按币种,可能多条);带 currency 时多顶层 `currency` 字段
- margin-ratio:`symbol / datas`(对象,im_factor / mm_factor / fm_factor)
- max-qty:`symbol / side / order_type / [price] / datas`(对象,cash_max_qty / margin_max_qty)

### 步骤 5:回答用户

- **必须**强调"数据来源于长桥证券"
- positions:用表格列出 symbol / 名字 / 数量 / 成本价 / 当前市值(LLM 算)/ 浮盈
- balance:多币种时全列出,核心货币(USD)放最上
- max-qty:cash_max_qty 与 margin_max_qty 都要给,提示用户融资有利息成本与强平风险

## CLI 接口文档

```
python3 cli.py portfolio
python3 cli.py positions
python3 cli.py funds
python3 cli.py balance       [--currency USD|HKD|CNY|SGD]
python3 cli.py margin-ratio  <symbol>
python3 cli.py max-qty       <symbol> --side buy|sell [--price <decimal>] [--order-type LO|MO|ELO|ALO]
```

通用参数:`--longbridge-bin / --format json / --timeout 30`。

退出码:`0` 业务成功 / `1` 业务错 / `2` 系统错。

## 输出 JSON Schema

见步骤 4。

## 数据来源标注

- 引用任何持仓 / 余额 / 保证金率 / 可买卖数量数据时,**必须**强调"数据来源于长桥证券"
- 没查到数据(空数组,如未持有任何股票)时,直接告诉用户"账户当前无 X"

## 错误处理

| `error_kind` | 用户侧话术 |
|---|---|
| `binary_not_found` | "长桥 CLI 工具未安装" |
| `auth_expired` | "长桥登录态过期了,请跑 `longbridge login`" |
| `subprocess_failed` | "查询失败:<details.stderr>" |
| `no_input` | "请告诉我要查什么:portfolio / positions / funds / balance / margin-ratio / max-qty" |
| `invalid_input_format` | "标的代码或参数格式不对:<details>" |

## MCP 备选

| cli.py 子命令 | 等效 MCP 工具 |
|---|---|
| `positions` | `mcp__longbridge__stock_positions` |
| `funds` | `mcp__longbridge__fund_positions` |
| `balance` | `mcp__longbridge__account_balance` |
| `margin-ratio` | `mcp__longbridge__margin_ratio` |
| `max-qty` | `mcp__longbridge__estimate_max_purchase_quantity` |
| `portfolio` | 依次调 stock_positions + fund_positions + account_balance(MCP 没有合体工具) |

MCP 拓展能力(CLI 没有):`mcp__longbridge__profit_analysis` / `profit_analysis_detail`(组合 P/L 分析,可选日期范围)、`mcp__longbridge__exchange_rate`(汇率换算)。这两个对"看一下我的总浮盈"类问句尤其有用。

注意:本账户的 OAuth token 若不含交易 API scope,CLI 会报 `auth_expired`(stderr 含 "authorized scope" 关键词)。MCP 走的是同一个 OAuth,scope 限制相同——除非用户重新授权拿 trade scope,两条路都不通。

## 代码结构

```
持仓查询/
├── SKILL.md
└── scripts/
    ├── cli.py
    └── test_cli.py
```
