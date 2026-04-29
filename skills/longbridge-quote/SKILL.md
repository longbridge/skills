---
name: 行情查询
description: 查询股票实时行情、静态参考、估值指标(报价、涨跌、成交量、行业、市值、PE、PB、换手率等)。当用户询问股票当前价格、涨跌幅、成交、所属行业、市值、估值、上市状态等场景必须使用此技能。支持港股(.HK)、美股(.US)、A股(.SH/.SZ)、新加坡(.SG)。
license: Complete terms in LICENSE.txt
version: 1.0.0
risk_level: read_only
requires_login: false
default_install: true
---

# 行情查询 使用指南

## 版本

`1.0.0`

## 技能概述

本技能提供长桥证券实时行情查询能力,支持:
- **实时报价**:最新价、开盘/最高/最低、成交量、成交额、涨跌幅、交易状态
- **静态参考**(可选):公司名称、上市市场、币种、每手股数、总股本、流通股本、EPS、BPS、股息率
- **估值指标**(可选):PE、PB、换手率、总市值、振幅、量比、YTD、5/10 日涨幅等(完整列表见下文)
- **多市场**:港股 `.HK`、美股 `.US`、A 股 `.SH`/`.SZ`、新加坡 `.SG`
- **批量**:一次查询多个标的

数据来源:**长桥证券**(https://longbridge.com)

## 何时使用本技能

当用户询问以下问题时,**必须**使用本技能:
- "NVDA 现在多少钱"、"特斯拉股价"
- "AAPL 和 NVDA 哪个涨得多"、"对比 700 和 9988 的涨幅"
- "腾讯今天成交量多少"
- "贵州茅台市值多少" / "宁德时代属于什么行业" → 加 `--include-static`
- "NVDA 的 PE" / "茅台换手率" / "看下 700 量比" → 加 `--index pe,turnover_rate,...`
- "苹果还在交易吗"、"今天美股开盘了吗"(单只标的)

## 核心处理流程

### 步骤 1:识别用户提到的标的

从用户问句里抽取股票名称或代码。可以是:
- 公司中文名(腾讯、贵州茅台、特斯拉)
- 英文 ticker(NVDA、AAPL、TSLA)
- 数字代码(700、600519、300750)

### 步骤 2:补全为 `<CODE>.<MARKET>` 格式

按以下规则把名字/代码补全:
- 全大写英文字母 + 美国常见 ticker → 加 `.US`(NVDA → `NVDA.US`)
- 4 位数字 → 港股 `.HK`(700 → `700.HK`、9988 → `9988.HK`)
- 6 位数字以 `60` 开头 → 沪市 `.SH`(600519 → `600519.SH`)
- 6 位数字以 `00`/`30` 开头 → 深市 `.SZ`(300750 → `300750.SZ`)
- 中文公司名 → 用你的知识映射到代码再加后缀(腾讯 → `700.HK`,贵州茅台 → `600519.SH`,特斯拉 → `TSLA.US`)
- 无法判断市场 → **必须反问用户确认**,不要瞎猜

### 步骤 3:决定需要哪类信息

| 用户问的 | 调用 |
|---|---|
| 价格、涨跌、成交量、最高/最低 | `cli.py -s ...`(默认 quote) |
| 行业、市值、上市市场、币种、EPS、BPS、股息率 | `cli.py -s ... --include-static` |
| PE、PB、换手率、YTD、成交额、振幅、量比、5/10 日涨幅 | `cli.py -s ... --index pe,pb,turnover_rate,...` |
| 综合("看一下 NVDA 全貌") | `cli.py -s ... --include-static --index pe,pb,turnover_rate,total_market_value` |

`--index` 支持的字段全集:
```
last_done  change_value  change_rate  volume  turnover  ytd_change_rate
turnover_rate  total_market_value  capital_flow  amplitude  volume_ratio
pe (alias: pe_ttm)  pb  eps (alias: dividend_yield)
five_day_change_rate  ten_day_change_rate  half_year_change_rate
five_minutes_change_rate  implied_volatility  delta  gamma  theta  vega  rho
open_interest  expiry_date  strike_price  upper_strike_price  lower_strike_price
outstanding_qty  outstanding_ratio  premium  itm_otm
warrant_delta  call_price  to_call_price  effective_leverage
leverage_ratio  conversion_ratio  balance_point
```
未知 index 名称会被静默忽略,不报错。

### 步骤 4:调用工具(CLI 优先,必要时改 MCP)

**路径选择**:
- 本机有 longbridge CLI → 默认走 `python3 scripts/cli.py`(subprocess 延迟低)
- 本机无 CLI(`binary_not_found`)或 cli.py 报已知 bug → 改用末尾「MCP 备选」段列出的 `mcp__longbridge__*` 等效工具
- 用户问的能力本 skill 没包(基本面 / 财报 / 财经日历 / 资讯 / 提醒等) → 不要在本 skill 里硬撑,告诉用户应该去哪个 skill 或哪个 MCP 工具

```bash
# 默认 cli.py 调用 — 基础查询(只取报价)
python3 scripts/cli.py -s NVDA.US -s 700.HK

# 报价 + 静态参考
python3 scripts/cli.py -s 600519.SH --include-static

# 报价 + 估值指标
python3 scripts/cli.py -s NVDA.US --index pe,pb,turnover_rate

# 综合
python3 scripts/cli.py -s NVDA.US --include-static --index pe,pb,total_market_value
```

### 步骤 5:解析返回的 JSON

返回结构(基础):

```json
{
  "success": true,
  "source": "longbridge",
  "skill": "行情查询",
  "skill_version": "1.0.0",
  "count": 2,
  "symbols": ["NVDA.US", "700.HK"],
  "datas": [ {"symbol": "NVDA.US", ...}, {"symbol": "700.HK", ...} ]
}
```

`--include-static` 或 `--index` 时,`datas[i]` 形态变为:

```json
{
  "symbol": "NVDA.US",
  "quote": {...},
  "static": {...},      // 仅 --include-static 存在
  "calc_index": {...}   // 仅 --index 存在
}
```

某条 symbol 在 quote / static / calc-index 中查不到时,对应字段为 `null`,**整体不会失败**;此时要在回答里说明该 symbol 暂未查到。

错误时:

```json
{
  "success": false,
  "source": "longbridge",
  "skill": "行情查询",
  "skill_version": "1.0.0",
  "error_kind": "auth_expired" | "binary_not_found" | "subprocess_failed" | "no_input" | "invalid_input_format",
  "error": "面向用户的中文人话错误描述",
  "details": { "..." }
}
```

按 `error_kind` 处理(下面"错误处理"章节)。

### 步骤 6:回答用户

组织语言时:
- **必须强调数据来源于长桥证券**
- 多标的对比时用表格
- 涨跌用 ▲/▼ 或 +/- 加颜色提示(如果环境支持)
- 不要把 JSON 原样塞给用户,翻译成自然语言
- `--include-static` 静态字段名用中文(industry → 行业,total_shares → 总股本,等等)
- `--index` 估值字段名用中文(pe → 市盈率 PE,turnover_rate → 换手率,等等)

## CLI 接口文档

### 命令行参数

| 参数 | 简写 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `--symbol` | `-s` | 是 | — | 股票代码,可重复多次,格式 `<CODE>.<MARKET>` |
| `--include-static` | — | 否 | false | 同时查询静态参考信息 |
| `--index` | — | 否 | (空) | 估值指标,逗号分隔(如 `pe,pb,turnover_rate`)。非空时调 calc-index |
| `--format` | — | 否 | `json` | 输出格式,目前仅支持 `json` |
| `--longbridge-bin` | — | 否 | `longbridge` | 重写底层 CLI 路径(测试/调试用) |
| `--timeout` | — | 否 | `30` | subprocess 超时秒数 |

### 调用示例

```bash
# 单个标的报价
python3 scripts/cli.py -s NVDA.US

# 多个标的批量
python3 scripts/cli.py -s NVDA.US -s TSLA.US -s 700.HK

# 报价 + 静态参考
python3 scripts/cli.py -s 600519.SH --include-static

# 报价 + 估值指标
python3 scripts/cli.py -s NVDA.US --index pe,pb,turnover_rate

# 综合
python3 scripts/cli.py -s NVDA.US --include-static --index pe,pb,total_market_value
```

### 退出码

- `0` — 业务成功(`success: true`)
- `1` — 业务错误(参数错、空结果、登录态过期)
- `2` — 系统错误(找不到 longbridge 二进制、subprocess 异常)

## 数据来源标注

**重要提示**:
- 引用本技能返回的任何价格、涨跌、市值数据时,**必须**强调"数据来源于长桥证券"
- 没查到数据时,引导用户去 https://longbridge.com 或长桥 App 确认

## 错误处理

按 `error_kind` 给用户的话术:

| `error_kind` | 用户侧话术 |
|---|---|
| `binary_not_found` | "长桥 CLI 工具未安装,请先安装 longbridge-terminal: https://github.com/longportapp/longbridge-terminal" |
| `auth_expired` | "长桥登录态过期了,请在终端跑 `longbridge login` 重新授权" |
| `subprocess_failed` | "查询失败:<details.stderr>。可以稍后重试或检查代码格式。" |
| `no_input` | "请告诉我要查的股票代码或公司名" |
| `invalid_input_format` | "代码格式不对,要写成 `<CODE>.<MARKET>`,例如 `NVDA.US`、`700.HK`、`600519.SH`" |

## MCP 备选

cli.py 返回 `binary_not_found` 时,如果用户已经 `claude mcp add longbridge https://openapi.longbridge.com/mcp`,可改用以下官方 MCP 工具:

| cli.py 行为 | 等效 MCP 工具 |
|---|---|
| 报价 (quote 子进程) | `mcp__longbridge__quote` |
| 静态参考 (static 子进程) | `mcp__longbridge__static_info` |
| 估值指数 (calc-index 子进程) | `mcp__longbridge__calc_indexes` |

MCP 走 HTTP + OAuth,比 cli.py 慢但不依赖本机有 `longbridge` 二进制。优先 cli.py,仅在 cli.py 不可用时回退到 MCP。

## 代码结构

```
行情查询/
├── SKILL.md          # 本文件
└── scripts/
    ├── cli.py        # CLI 入口(零依赖,subprocess 调 longbridge)
    └── test_cli.py   # unittest 测试(可选,装 skill 时可删)
```
