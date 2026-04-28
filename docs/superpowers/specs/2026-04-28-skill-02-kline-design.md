# K 线查询(skill #02)— 差异化设计

**Date:** 2026-04-28
**Status:** Draft
**Protocol:** 遵循 `2026-04-28-skill-platform-protocol.md`

## 业务范围

历史 K 线 + 分时图。包装 `kline` / `kline-history` / `intraday`。

| 子命令 | 何时调 |
|---|---|
| `kline` | 用户问"最近 N 根 K"、"今日日 K"、"5 分钟 K"等不指定区间的需求,默认走它(支持 1m/5m/15m/30m/1h/day/week/month/year) |
| `kline-history` | 用户**明确给出起止日期**(如"2024-01-01 到 2024-12-31") |
| `intraday` | 用户问"今日分时图"、"intraday curve",cli.py 用单独子命令 `intraday` 走 |

## front-matter

```yaml
---
name: K线查询
description: 查询股票历史 K 线和分时图(OHLCV、5 分钟/日/周/月 K、今日分时)。当用户询问股票走势、历史价格、最近一周/一月/一年走势、日 K、月 K、分时图等场景必须使用此技能。支持港股(.HK)、美股(.US)、A 股(.SH/.SZ)、新加坡(.SG),不支持期权/窝轮/指数。
license: Complete terms in LICENSE.txt
version: 1.0.0
risk_level: read_only
requires_login: false
default_install: true
---
```

## scripts/cli.py 子命令风格

K 线 skill 的 cli.py 用 **subcommand 风格**(argparse subparsers),不是 flag 风格——因为 kline / kline-history / intraday 是三种结构差异较大的查询。

```
python3 cli.py kline      <symbol> [--period day] [--count 100] [--adjust no_adjust]
python3 cli.py history    <symbol> --start YYYY-MM-DD --end YYYY-MM-DD [--period day] [--adjust no_adjust]
python3 cli.py intraday   <symbol>
```

通用参数(`--longbridge-bin / --format / --timeout`)在三个子命令上都有。

| 参数 | 适用 | 默认 | 说明 |
|---|---|---|---|
| `<symbol>` | 全部 | — | 必填,单标的 |
| `--period` | kline / history | `day` | `1m / 5m / 15m / 30m / 1h / day / week / month / year` (按 longbridge 别名,内部不二次映射) |
| `--count` | kline | `100` | 返回根数 |
| `--start` `--end` | history | — | 必须**同时**给,YYYY-MM-DD;否则 `invalid_input_format` |
| `--adjust` | kline / history | `no_adjust` | `no_adjust / forward_adjust`(LLM 别名:`无 → no_adjust, 前复权 → forward_adjust`) |

## 输出 JSON Schema

**`kline`**:

```json
{
  "success": true, "source": "longbridge", "skill": "K线查询", "skill_version": "1.0.0",
  "subcommand": "kline",
  "symbol": "TSLA.US", "period": "day", "count": 100, "adjust": "no_adjust",
  "datas": [ /* 原 kline JSON 数组,每条 {timestamp, open, high, low, close, volume, turnover} */ ]
}
```

**`history`**:同上,`subcommand: "history"`,顶层加 `start` `end`,`datas` 同 kline。

**`intraday`**:

```json
{
  "success": true, "source": "longbridge", "skill": "K线查询", "skill_version": "1.0.0",
  "subcommand": "intraday",
  "symbol": "TSLA.US",
  "datas": [ /* 原 intraday JSON 数组,每条 {timestamp, price, volume, turnover, avg_price} */ ]
}
```

## SKILL.md 提示词差异

### `## 何时使用本技能` 列举

- "NVDA 最近一周走势" / "茅台过去一年 K 线"
- "看下 TSLA 5 分钟 K"
- "今天 700.HK 分时图"
- "AAPL 2024 年 1-12 月日 K"(明确日期 → history)
- "贵州茅台月 K"(period=month)
- "前复权日 K"(adjust=forward_adjust)

### 用户问句 → cli.py 参数映射

| 用户语义 | 子命令 | period | count | start/end | adjust |
|---|---|---|---|---|---|
| "最近一周" | kline | day | 7 | — | — |
| "最近一年" | kline | day | 252(美股)/ 244(港股)/ 244(A 股) | — | — |
| "5 分钟 K" / "近 100 根 5 分钟" | kline | 5m | 100 | — | — |
| "月 K" / "看月线" | kline | month | 100 | — | — |
| "2024 年走势" | history | day | — | 2024-01-01 / 2024-12-31 | — |
| "今天分时" / "今日走势" | intraday | — | — | — | — |
| "前复权" | (kline 或 history) | (按上下文) | (按上下文) | (按上下文) | forward_adjust |

`count` 估算:LLM 不需要精确,kline 子命令默认 100 根日 K 已经覆盖近半年 trading days,大部分"最近 X 月"问题直接用 default 即可。

### 核心处理流程

跟 #01 行情查询同结构(识别 → 补全 symbol → 路由子命令 → 调用 → 解析 → 回答)。差异只在步骤 3:LLM 必须**先决定 subcommand**,再决定 period / count / start / end / adjust。

## 验收清单

- [ ] 单元层:`cli.py kline TSLA.US --period day --count 50` 返回 50 条 datas
- [ ] history 层:`cli.py history TSLA.US --start 2025-01-01 --end 2025-03-31` 返回该区间数据
- [ ] intraday 层:盘中跑 `cli.py intraday TSLA.US`,返回非空数组(收盘后用真实标的也可)
- [ ] 错误层:`history` 缺 `--start` 或 `--end` → `invalid_input_format`
- [ ] 集成层:6 句话验证
  - "NVDA 最近一周走势"
  - "茅台过去一年 K 线"
  - "看下 TSLA 5 分钟 K"
  - "AAPL 2025 年 1-3 月日 K"(必须命中 history)
  - "贵州茅台月 K"
  - "今天 700.HK 分时图"

## 已知 trade-off

- `kline-history` 的"百根回退"行为(只给 `--start` 不给 `--end` 会忽略 `--start` 直接返回近 100 根):cli.py 在两者**同时给**才走 history,否则强制 `invalid_input_format`,避免 LLM 困惑。
- `intraday` 在非交易时段返回的数据可能是上一交易日,SKILL.md 让 LLM 在回答里说明是哪个 trading session 的数据(从 datas[0].timestamp 推断)。
