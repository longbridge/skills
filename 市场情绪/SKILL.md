---
name: 市场情绪
description: 查询市场是否开市、交易时段、交易日历,以及市场情绪温度计(0-100,越高越多头)。当用户询问今天/明天某市场是否开盘、几点开盘几点收盘、下个交易日、市场情绪、牛熊度数等场景必须使用此技能。支持港股、美股、A 股(沪深合并)、新加坡。
license: Complete terms in LICENSE.txt
version: 1.0.0
risk_level: read_only
requires_login: false
default_install: true
---

# 市场情绪 使用指南

## 版本

`1.0.0`

## 技能概述

市场层面的"是否开市 + 情绪温度"。标的层面在「行情查询」skill。

- **temp**:市场情绪温度计快照(0-100,越高越多头);加 `--history` 查时序
- **session**:全市场交易时段(开 / 收盘时间)
- **days**:某市场的交易日历(交易日 + 半日交易日)

数据来源:**长桥证券**(https://longbridge.com)

## 何时使用本技能

- "今天美股开盘了吗" / "现在港股交易吗"
- "美股几点开盘"
- "下个交易日是几号" / "这周还有几天交易"
- "圣诞节港股开市吗"
- "美股市场温度" / "现在情绪指数多少"
- "看一下今年港股市场情绪走势"(→ `temp --history`)

## 核心处理流程

### 步骤 1:决定子命令

| 用户语义 | 子命令 |
|---|---|
| "几点开盘 / 收盘" / "X 市场开市时间" | session |
| "今天 / 明天 X 市场开盘吗" | days |
| "下个交易日" / "本周交易日" | days |
| "市场情绪 / 温度 / 牛熊度数" | temp |
| "X 市场今年情绪走势" | temp --history --start ... --end ... |

### 步骤 2:市场识别

LLM 把用户口语映射到 `--market`:

- "美股 / US / 纳斯达克 / 道指 / 标普" → `US`
- "港股 / HK / 恒生" → `HK`
- "A 股 / 沪 / 深 / 上证 / 深证" → `CN`(也接受 `SH` `SZ` 别名)
- "新加坡 / SG / 海峡 / 星洲" → `SG`
- 不明 → 反问

`session` 不需要 market(返回所有市场)。

### 步骤 3:调用 CLI

```bash
python3 scripts/cli.py temp --market HK
python3 scripts/cli.py session
python3 scripts/cli.py days --market US --start 2026-04-28 --end 2026-05-31
python3 scripts/cli.py temp --market HK --history --start 2026-01-01 --end 2026-04-28
```

### 步骤 4:解析返回 JSON

各子命令的 envelope:`success / source: "longbridge" / skill: "市场情绪" / skill_version / subcommand`,然后:
- `temp`:`market` + `datas`(快照对象);`--history` 时多 `start` `end`,`datas` 为数组
- `session`:`datas` 为数组(跨全市场)
- `days`:`market` + `datas`(对象,含 `trading_days` / `half_trading_days`)

### 步骤 5:回答用户

- **必须**强调"数据来源于长桥证券"
- "今天 X 市场是否在交易"是个推理问题:结合本地时间 + trading-session 数据,LLM 自己推理(美股 = UTC-5/-4 夏令时、港股 = UTC+8、A 股 = UTC+8、新加坡 = UTC+8)
- temp 数值用文字描述:0-30 偏空、30-50 中性偏空、50-70 中性偏多、70-100 偏多

## CLI 接口文档

```
python3 cli.py temp     [--market HK|US|CN|SG] [--history --start YYYY-MM-DD --end YYYY-MM-DD]
python3 cli.py session
python3 cli.py days     [--market HK|US|CN|SG] [--start YYYY-MM-DD] [--end YYYY-MM-DD]
```

通用参数:`--longbridge-bin / --format json / --timeout 30`。

退出码:`0` 业务成功 / `1` 业务错 / `2` 系统错。

## 输出 JSON Schema

见步骤 4。

## 数据来源标注

- 引用任何市场温度、交易时段、交易日数据时,**必须**强调"数据来源于长桥证券"
- 没查到数据时,引导用户去 https://longbridge.com 或长桥 App 确认

## 错误处理

| `error_kind` | 用户侧话术 |
|---|---|
| `binary_not_found` | "长桥 CLI 工具未安装" |
| `auth_expired` | "长桥登录态过期了,请跑 `longbridge login`" |
| `subprocess_failed` | "查询失败:<details.stderr>" |
| `no_input` | "请告诉我要查什么:temp / session / days" |
| `invalid_input_format` | "市场或日期格式不对:<details>" |

## 代码结构

```
市场情绪/
├── SKILL.md
└── scripts/
    ├── cli.py
    └── test_cli.py
```
