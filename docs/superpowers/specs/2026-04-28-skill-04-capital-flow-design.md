# 资金流向(skill #04)— 差异化设计

**Date:** 2026-04-28
**Status:** Draft
**Protocol:** 遵循 `2026-04-28-skill-platform-protocol.md`

## 业务范围

主力资金流向 = 时序 (`capital-flow`) + 截面快照 (`capital-dist`)。

| 子命令 | 何时调 |
|---|---|
| `capital-flow` | 用户问"资金流向"、"主力净流入"、"今日资金流入流出曲线" |
| `capital-dist` | 用户问"大单分布"、"主力 / 大 / 中 / 小单"、"今天大单买入多少" |

## front-matter

```yaml
---
name: 资金流向
description: 查询股票当日主力资金流向时序与大中小单分布(主力净流入、大单买卖、资金分布)。当用户询问主力资金、净流入、大单 / 中单 / 小单、资金分布、机构资金流等场景必须使用此技能。支持港股/美股/A 股/新加坡。
license: Complete terms in LICENSE.txt
version: 1.0.0
risk_level: read_only
requires_login: false
default_install: true
---
```

## scripts/cli.py 接口

flag 风格(两个子命令 schema 相近,合一即可):

```
python3 cli.py -s <symbol> [--include-dist]
```

| 参数 | 简写 | 默认 | 说明 |
|---|---|---|---|
| `--symbol` | `-s` | — | 必填,单标的(底层 capital-flow / capital-dist 都只接受单 symbol) |
| `--include-dist` | — | false | 同时取 capital-dist;不带时只调 capital-flow |

## 输出 JSON Schema

**默认**(只 capital-flow):

```json
{
  "success": true, "source": "longbridge", "skill": "资金流向", "skill_version": "1.0.0",
  "symbol": "TSLA.US",
  "datas": {
    "flow": [ /* 原 capital-flow 数组,时序 */ ]
  }
}
```

**`--include-dist`**:

```json
{
  "success": true, ...,
  "symbol": "TSLA.US",
  "datas": {
    "flow": [ ... ],
    "distribution": { /* 原 capital-dist 对象 */ }
  }
}
```

## SKILL.md 提示词差异

### `## 何时使用本技能` 列举

- "今天 NVDA 主力净流入多少" / "茅台资金流向"
- "看下 TSLA 大单分布"
- "腾讯今日资金流入曲线"
- "贵州茅台主力 / 大单 / 中单 / 小单"(→ `--include-dist`)
- "今天哪些股票主力大幅流入"(LLM 应回答:本 skill 不支持筛选,只能看单只;引导用户提供具体标的)

### 步骤 3 子命令路由

| 用户语义 | flag |
|---|---|
| 时序 / 流向 / 净流入(随时间) | (默认,只 flow) |
| 大单/中单/小单分布 / 截面 | `--include-dist` |
| 综合("看一下资金面") | `--include-dist` |

### 名词翻译

底层 capital-dist 字段名是英文,SKILL.md 让 LLM 在回答时按以下映射翻译:

| 字段(假设) | 中文 |
|---|---|
| `large_in` / `large_out` | 大单流入 / 流出 |
| `medium_in` / `medium_out` | 中单流入 / 流出 |
| `small_in` / `small_out` | 小单流入 / 流出 |
| `super_in` / `super_out`(若有) | 超大单流入 / 流出 |

(实际字段名以 longbridge JSON 输出为准,LLM 根据语义猜测;不在 cli.py 做映射,避免 longbridge 改字段名时 cli.py 跟着改。)

## 验收清单

- [ ] 单元层:`cli.py -s TSLA.US` 返回 datas.flow 非空数组
- [ ] include-dist:`cli.py -s TSLA.US --include-dist` 同时含 flow + distribution
- [ ] symbol 校验:`cli.py -s nvda.US` → `invalid_input_format`
- [ ] 集成层:5 句话验证
  - "今天 NVDA 主力净流入多少"
  - "茅台资金流向" / "茅台资金面" → 触发 `--include-dist`
  - "TSLA 大单分布"
  - "腾讯今日资金流入曲线"
  - "看一下 700 主力 / 大 / 中 / 小单"

## 已知 trade-off

- iwencai 把"资金流向"并入 `hithink-market-query`(行情大类下);我们独立成 skill,理由:中文用户高频问句"主力净流入" / "大单"非常清晰,独立 skill 让 LLM 路由更稳。
- 当日数据为主,不支持历史(底层 capital-flow 只给当日)。SKILL.md 让 LLM 在用户问"过去 X 天资金流"时明确告知"本 skill 只能查当日资金流向,历史资金面请查 K 线/成交量"。
