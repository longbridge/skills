# 市场情绪(skill #05)— 差异化设计

**Date:** 2026-04-28
**Status:** Draft
**Protocol:** 遵循 `2026-04-28-skill-platform-protocol.md`

## 业务范围

市场层面的"是否开市 + 情绪温度",标的层面在 #01 行情查询解决。

| 子命令 | 何时调 |
|---|---|
| `market-temp` | 用户问"市场温度 / 情绪 / 牛熊度数" |
| `trading-session` | 用户问"今天 X 市场什么时候开盘 / 收盘" |
| `trading-days` | 用户问"下个交易日 / 这个月有几个交易日 / 圣诞节港股开市吗" |

## front-matter

```yaml
---
name: 市场情绪
description: 查询市场是否开市、交易时段、交易日历,以及市场情绪温度计(0-100,越高越多头)。当用户询问今天/明天某市场是否开盘、几点开盘几点收盘、下个交易日、市场情绪、牛熊度数等场景必须使用此技能。支持港股、美股、A 股(沪深合并)、新加坡。
license: Complete terms in LICENSE.txt
version: 1.0.0
risk_level: read_only
requires_login: false
default_install: true
---
```

## scripts/cli.py 子命令风格

```
python3 cli.py temp     [--market HK|US|CN|SG] [--history --start ... --end ...]
python3 cli.py session                          # 全市场,无参数
python3 cli.py days     [--market HK|US|CN|SG] [--start YYYY-MM-DD] [--end YYYY-MM-DD]
```

| 参数 | 适用 | 默认 | 说明 |
|---|---|---|---|
| `--market` | temp / days | `HK` | `HK / US / CN / SG`(case-insensitive)。SH / SZ → CN |
| `--history` | temp | false | 历史时序,需配 `--start --end` |
| `--start` `--end` | temp(history) / days | (按 longbridge 默认) | YYYY-MM-DD;temp 历史模式必须给两个,days 可缺省 |

## 输出 JSON Schema

**`temp`** 默认:

```json
{
  "success": true, ...,
  "subcommand": "temp",
  "market": "HK",
  "datas": { /* 原 market-temp 当前快照对象 */ }
}
```

**`temp --history`**:

```json
{
  "success": true, ...,
  "subcommand": "temp",
  "market": "HK", "start": "2025-01-01", "end": "2025-12-31",
  "datas": [ /* 原 market-temp --history 数组 */ ]
}
```

**`session`**:

```json
{
  "success": true, ...,
  "subcommand": "session",
  "datas": [ /* 原 trading-session 数组,跨全市场 */ ]
}
```

**`days`**:

```json
{
  "success": true, ...,
  "subcommand": "days",
  "market": "HK", "start": "2025-04-01", "end": "2025-04-30",
  "datas": { /* 原 trading-days 对象,含 trading_days[] / half_trading_days[] */ }
}
```

## SKILL.md 提示词差异

### `## 何时使用本技能` 列举

- "今天美股开盘了吗" / "现在港股交易吗"
- "美股几点开盘"
- "下个交易日是几号" / "这周还有几天交易"
- "圣诞节港股开市吗"
- "美股市场温度" / "现在情绪指数多少"
- "看一下今年港股市场情绪走势"(→ `temp --history`)

### 步骤 3 子命令路由

| 用户语义 | 子命令 | 参数推断 |
|---|---|---|
| "几点开盘 / 收盘" / "X 市场开市时间" | session | — |
| "今天 / 明天 X 市场开盘吗" | days | --market 推断;--start --end 用今天/明天 |
| "下个交易日" / "本周交易日" | days | --start 今天,--end 7 天后 |
| "市场情绪 / 温度 / 牛熊度数" | temp | 默认快照,加 --market |
| "X 市场今年情绪走势" | temp | --history --start 今年 1 月 1 日 --end 今天 |

### 市场识别规则

LLM 把用户口语映射到 `--market`:
- "美股 / US / 纳斯达克 / 道指 / 标普" → `US`
- "港股 / HK / 恒生" → `HK`
- "A 股 / 沪 / 深 / 上证 / 深证" → `CN`
- "新加坡 / SG / 海峡 / 星洲" → `SG`
- 不明 → 反问

`session` 不需要 market 参数,返回全市场。

## 验收清单

- [ ] temp 快照:`cli.py temp --market HK` 返回 datas 含 temperature 字段
- [ ] temp 历史:`cli.py temp --market US --history --start 2025-01-01 --end 2025-04-01` 返回数组
- [ ] session:`cli.py session` 返回所有市场
- [ ] days:`cli.py days --market HK --start 2025-04-01 --end 2025-04-30` 返回 trading_days
- [ ] 市场别名:`cli.py temp --market sh` 应被接受并归一化为 CN
- [ ] 集成层:6 句话验证
  - "今天美股开盘了吗"
  - "下个港股交易日是几号"
  - "美股几点开盘"
  - "看一下今年港股情绪走势"
  - "圣诞节港股开市吗"
  - "现在哪些市场在交易"

## 已知 trade-off

- "今天 X 市场是否在交易"是个推理问题,需要结合本地时间 + trading-session 数据。本 skill 不在 cli.py 里做这个推理,只返回原始数据,让 LLM 自己推理(对 LLM 来说是 trivial 推理)。
- `trading-session` 不返回时区,LLM 需要知道 HK = UTC+8、US = UTC-5(夏令时 -4)等市场时区(LLM 自有知识足够)。
