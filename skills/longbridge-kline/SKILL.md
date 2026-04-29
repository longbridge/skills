---
name: K线查询
description: 查询股票历史 K 线和分时图(OHLCV、5 分钟/日/周/月 K、今日分时)。当用户询问股票走势、历史价格、最近一周/一月/一年走势、日 K、月 K、分时图等场景必须使用此技能。支持港股(.HK)、美股(.US)、A 股(.SH/.SZ)、新加坡(.SG),不支持期权/窝轮/指数。
license: Complete terms in LICENSE.txt
version: 1.0.0
risk_level: read_only
requires_login: false
default_install: true
---

# K线查询 使用指南

## 版本

`1.0.0`

## 技能概述

本技能查询长桥证券的历史 K 线 + 今日分时:

- **kline**:近 N 根 K 线(默认日 K 100 根),支持 1m/5m/15m/30m/1h/day/week/month/year
- **history**:指定起止日期的历史 K 线
- **intraday**:今日分时图(逐分钟价格 + 成交)

数据来源:**长桥证券**(https://longbridge.com)

不支持:期权、窝轮、指数 — 这些请用「期权与窝轮」或行情查询(指数走 quote 接口)。

## 何时使用本技能

- "NVDA 最近一周走势"、"茅台过去一年 K 线"
- "看下 TSLA 5 分钟 K"、"近 100 根 5 分钟"
- "今天 700.HK 分时图"、"AAPL 今日走势"
- "AAPL 2024 年 1-12 月日 K"(明确日期 → history)
- "贵州茅台月 K"、"季 K"
- "前复权日 K"

## 核心处理流程

### 步骤 1:识别标的

抽取股票名称或代码,补全为 `<CODE>.<MARKET>`(规则同行情查询 skill)。

### 步骤 2:决定子命令

| 用户语义 | 子命令 |
|---|---|
| "最近 X 天 / 最近一周一月一年 / 默认走势" | `kline` |
| "X 分钟 K / 月 K / 季 K"(无日期窗) | `kline` |
| "**X 月 X 日 至 X 月 X 日 / X 年走势 / 具体日期段**" | `history` |
| "今天分时 / 今日走势 / intraday" | `intraday` |

### 步骤 3:确定参数

| 用户语义 | period | count | start/end |
|---|---|---|---|
| "最近一周" | day | 7 | — |
| "最近一年" | day | 252 | — |
| "近 100 根 5 分钟" | 5m | 100 | — |
| "月 K" | month | 100(默认) | — |
| "2024 年走势" | day | — | 2024-01-01 / 2024-12-31 |
| "周 K" | week | 100 | — |

period 别名:longbridge 接受 `minute=1m`、`hour=1h`、`d/1d=day`、`w=week`、`m/1mo=month`、`y=year`(全部 case-insensitive),cli.py 不二次映射,直传给 longbridge。

`adjust`:`no_adjust`(默认)/ `forward_adjust`。"前复权" → `forward_adjust`。

### 步骤 4:调用工具(CLI 优先,必要时改 MCP)

**路径选择**:
- 本机有 longbridge CLI → 默认 `python3 scripts/cli.py`(快)
- 本机无 CLI / cli.py 报 `binary_not_found` → 改用末尾「MCP 备选」段的 `mcp__longbridge__candlesticks` / `history_candlesticks_*` / `intraday`
- 期权 / 窝轮 / 指数的 K 线本 skill 不包,引导到「期权与窝轮」或行情查询(指数走 quote)

```bash
# 默认 cli.py 调用
python3 scripts/cli.py kline NVDA.US --period day --count 100
python3 scripts/cli.py history NVDA.US --start 2025-01-01 --end 2025-12-31
python3 scripts/cli.py intraday 700.HK
```

### 步骤 5:解析返回的 JSON

```json
{
  "success": true,
  "source": "longbridge",
  "skill": "K线查询",
  "skill_version": "1.0.0",
  "subcommand": "kline",
  "symbol": "NVDA.US",
  "period": "day",
  "count": 5,
  "adjust": "no_adjust",
  "datas": [{"time": "...", "open": "...", "high": "...", "low": "...", "close": "...", "volume": "...", "turnover": "..."}, ...]
}
```

`history` 多 `start` `end` 字段;`intraday` datas 元素为 `{time, price, volume, turnover, avg_price}`。

错误时返回标准 envelope(见错误处理)。

### 步骤 6:回答用户

- **必须**强调"数据来源于长桥证券"
- 走势用文字描述(涨/跌区间、最高/最低、成交量),涨跌用 ▲/▼ 标记
- 不要把 datas 数组原样塞给用户,翻译成自然语言
- intraday 回答时说明是哪个 trading session(从 datas[0].time 推断当前/上一交易日)

## CLI 接口文档

### 子命令

```
python3 cli.py kline      <symbol> [--period day] [--count 100] [--adjust no_adjust]
python3 cli.py history    <symbol> --start YYYY-MM-DD --end YYYY-MM-DD [--period day] [--adjust no_adjust]
python3 cli.py intraday   <symbol>
```

通用参数(三个子命令都有):`--longbridge-bin` `--format json` `--timeout 30`。

### 退出码

- `0` 业务成功
- `1` 业务错误(参数错、登录态过期、空结果)
- `2` 系统错误(找不到 longbridge、subprocess 异常)

## 输出 JSON Schema

见步骤 5。`history` 与 `kline` 几乎相同,只多了 `start` `end`;`intraday` datas 形态不同。

## 数据来源标注

- 引用任何 K 线 / 分时数据时,**必须**强调"数据来源于长桥证券"
- 没查到数据时,引导用户去 https://longbridge.com 或长桥 App 确认

## 错误处理

| `error_kind` | 用户侧话术 |
|---|---|
| `binary_not_found` | "长桥 CLI 工具未安装,请先安装 longbridge-terminal: https://github.com/longportapp/longbridge-terminal" |
| `auth_expired` | "长桥登录态过期了,请在终端跑 `longbridge login` 重新授权" |
| `subprocess_failed` | "查询失败:<details.stderr>。可以稍后重试或检查参数。" |
| `no_input` | "请告诉我要查的标的代码,以及子命令(kline / history / intraday)" |
| `invalid_input_format` | "代码或日期格式不对:<details>。" |

## MCP 备选

cli.py 返回 `binary_not_found` 时,如果已配置 `claude mcp add longbridge ...`,可改用:

| cli.py 子命令 | 等效 MCP 工具 |
|---|---|
| `kline` | `mcp__longbridge__candlesticks` |
| `history` | `mcp__longbridge__history_candlesticks_by_offset` 或 `mcp__longbridge__history_candlesticks_by_date` |
| `intraday` | `mcp__longbridge__intraday` |

优先 cli.py,本机更快;MCP 仅作回退。

## 代码结构

```
K线查询/
├── SKILL.md
└── scripts/
    ├── cli.py
    └── test_cli.py
```
