# 行情查询(skill #01)— 差异化设计

**Date:** 2026-04-28
**Status:** Draft
**Protocol:** 遵循 `2026-04-28-skill-platform-protocol.md`
**Prior MVP spec:** `2026-04-27-longbridge-skill-mvp-design.md`(实施计划仍走那份的 Task 1–10,本文档只是把 MVP 的内容裁剪到差异化形态,作为整套范式的样板)

## 业务范围

实时报价 + 静态参考 + 计算指数,三者合一,一次查询多个标的。

包装的 longbridge 子命令:`quote` / `static` / `calc-index`

| 子命令 | 何时调 |
|---|---|
| `quote` | 总是调 |
| `static` | `--include-static` 或 LLM 判定用户问"行业 / 市值 / 上市状态 / EPS / 股息率"等静态属性 |
| `calc-index` | `--index <name,...>` 或 LLM 判定用户问"PE / PB / 换手率 / YTD" 等需要计算的指标 |

## front-matter

```yaml
---
name: 行情查询
description: 查询股票实时行情、静态参考、估值指标(报价、涨跌、成交量、行业、市值、PE、PB、换手率等)。当用户询问股票当前价格、涨跌幅、成交、所属行业、市值、估值、上市状态等场景必须使用此技能。支持港股(.HK)、美股(.US)、A股(.SH/.SZ)、新加坡(.SG)。
license: Complete terms in LICENSE.txt
version: 1.0.0
risk_level: read_only
requires_login: false
default_install: true
---
```

## scripts/cli.py 业务参数

| 参数 | 简写 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|---|
| `--symbol` | `-s` | str(可重复) | 是 | — | 标的代码,可重复 |
| `--include-static` | — | flag | 否 | false | 同时查 static |
| `--index` | — | csv | 否 | (空) | 计算指数,逗号分隔(如 `pe,pb,turnover_rate`)。非空时调 calc-index |

symbol 校验:`^[A-Z0-9]+\.(US|HK|SH|SZ|SG)$`,违反 → `invalid_input_format`。

## 输出 JSON Schema

**默认**(只调 quote):

```json
{
  "success": true,
  "source": "longbridge",
  "skill": "行情查询",
  "skill_version": "1.0.0",
  "count": 2,
  "symbols": ["NVDA.US", "700.HK"],
  "datas": [ /* longbridge quote --format json 原数组,每条至少含 symbol */ ]
}
```

**`--include-static` 或 `--index` 时**,`datas[i]` 形态:

```json
{
  "symbol": "NVDA.US",
  "quote": { /* 原 quote 对象 */ },
  "static": { /* 原 static 对象,无 --include-static 时省略本字段 */ },
  "calc_index": { /* 原 calc-index 对象,无 --index 时省略本字段 */ }
}
```

合并算法:三个子进程的返回各自按 `symbol` 字段映射,缺失填 null,**整体不失败**。

## SKILL.md 提示词差异

### `## 何时使用本技能` 列举

- "NVDA 现在多少钱"、"特斯拉股价"
- "AAPL 和 NVDA 哪个涨得多"、"对比 700 和 9988 涨幅"
- "腾讯今天成交量多少"
- "贵州茅台市值多少" / "宁德时代属于什么行业" → `--include-static`
- "NVDA 的 PE" / "茅台换手率" → `--index pe,turnover_rate`
- "苹果还在交易吗"、"今天美股开盘了吗"(单只)

### `## 核心处理流程` 步骤 2(参数补全)

按以下规则把名字/代码补全为 `<CODE>.<MARKET>`:
- 全大写英文 + 美股常见 ticker → `.US`
- 4 位数字 → `.HK`
- 6 位数字以 `60` 开头 → `.SH`;以 `00`/`30` 开头 → `.SZ`
- 中文公司名 → 用 LLM 自有知识(腾讯 → `700.HK`,贵州茅台 → `600519.SH`,特斯拉 → `TSLA.US`)
- 无法判断市场 → 反问用户,不要瞎猜

### `## 核心处理流程` 步骤 3(子命令路由)

| 用户问的 | 调用 |
|---|---|
| 价格、涨跌、成交量、最高/最低 | `cli.py -s ...` |
| 行业、市值、上市市场、币种、EPS、BPS、股息率 | `cli.py -s ... --include-static` |
| PE、PB、换手率、YTD、成交额、振幅、量比 | `cli.py -s ... --index pe,pb,turnover_rate,...` |
| 综合("看看 NVDA 全貌") | 同时加 `--include-static --index pe,pb,turnover_rate,total_market_value` |

calc-index 支持的字段全集见 `longbridge calc-index --help`(在 SKILL.md 里粘一份完整列表,LLM 才能映射"换手率"→`turnover_rate`)。

## 验收清单(在 MVP 计划 Task 9/10 基础上扩充)

- [ ] 单元层:`-s NVDA.US -s 700.HK` 返回 success / count=2 / datas 含两条
- [ ] 静态层:`--include-static` 时每条 data 含非空 quote 和 static
- [ ] 估值层:`--index pe,pb` 时每条 data 含非空 calc_index 子对象,含 pe / pb 字段
- [ ] 错误层:5 种通用 error_kind 测试全过
- [ ] 集成层:Claude Code 4 句话验证(MVP 那 4 句)+ 新增 2 句:
  - "NVDA 现在 PE 多少" → 触发 `--index pe`
  - "看下 茅台 全貌" → 同时触发 `--include-static --index ...`

## 与 MVP plan 的关系

MVP plan 已经写好的 10 个 Task **基本可以直接跑**,只需要在以下几处微调以匹配本规约:

1. **Task 2 SKILL.md** 增 `version` `risk_level` `requires_login` `default_install` 四个 front-matter 字段
2. **Task 3 cli.py** 的 emit JSON 加 `source / skill / skill_version` 三个 envelope 字段
3. **Task 5** 的 `binary_not_found` 检测改用规约里的 `resolve_bin` 算法
4. **新增 Task 11**:`--index` 参数 + calc-index 子进程 + 三方合并(参考 Task 8 的双方合并模板)

这些差异在写 plan 阶段对齐,不影响 spec 已有结构。
