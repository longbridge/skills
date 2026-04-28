# 持仓查询(skill #08)— 差异化设计

**Date:** 2026-04-28
**Status:** Draft
**Protocol:** 遵循 `2026-04-28-skill-platform-protocol.md`

## 业务范围

账户全景的"我有什么 + 我有多少钱 + 我能买多少 + 保证金率"。

| 子命令 | 何时调 |
|---|---|
| `positions` | 股票持仓 |
| `fund-positions` | 基金持仓 |
| `balance` | 现金余额 + 融资额度 |
| `margin-ratio` | 标的保证金率(im / mm / fm) |
| `max-qty` | 估算可买/可卖最大数量 |

## front-matter

```yaml
---
name: 持仓查询
description: 查询账户股票持仓 / 基金持仓 / 现金余额 / 融资额度,以及标的保证金率与可买可卖最大数量。当用户询问我的持仓 / 我有多少钱 / 账户余额 / 我能买多少股 X / X 保证金率 / 风险等级等账户级问题时必须使用此技能。需要 longbridge login。
license: Complete terms in LICENSE.txt
version: 1.0.0
risk_level: account_read
requires_login: true
default_install: true
---
```

## scripts/cli.py 子命令风格

```
python3 cli.py portfolio                                # positions + fund-positions + balance 一次取
python3 cli.py positions
python3 cli.py funds                                    # 别名 fund-positions
python3 cli.py balance       [--currency USD|HKD|CNY|SGD]
python3 cli.py margin-ratio  <symbol>
python3 cli.py max-qty       <symbol> --side buy|sell [--price <decimal>] [--order-type LO|MO|ELO|ALO]
```

| 参数 | 适用 | 默认 | 说明 |
|---|---|---|---|
| `<symbol>` | margin-ratio / max-qty | — | 必填 |
| `--side` | max-qty | — | 必填,`buy` / `sell` |
| `--price` | max-qty | — | LO 类必填,decimal 字符串 |
| `--order-type` | max-qty | `LO` | `LO / MO / ELO / ALO`,case-insensitive |
| `--currency` | balance | (空,返全部) | `USD / HKD / CNY / SGD` |

## 输出 JSON Schema

**`portfolio`**(combo):

```json
{
  "success": true, ..., "subcommand": "portfolio",
  "datas": {
    "positions": [ /* 原 positions */ ],
    "fund_positions": [ /* 原 fund-positions */ ],
    "balance": [ /* 原 balance,可能是按 currency 多条 */ ]
  }
}
```

各单子命令的 schema:`subcommand` 字段 + 顶层套上参数(如 `symbol` `currency`),`datas` 是原始 longbridge JSON。

## SKILL.md 提示词差异

### `## 何时使用本技能` 列举

- "我的持仓" / "我现在持有什么"
- "账户余额多少" / "我有多少美金 / 港币"
- "我的基金持仓"
- "NVDA 我能买多少股" / "TSLA 全仓买能买多少"
- "茅台保证金率" / "X 标的风险等级"
- "看一下我的账户全貌"(→ portfolio)

### 步骤 3 子命令路由

| 用户语义 | 子命令 |
|---|---|
| "持仓 / 我持有 / 我有什么股票" | positions |
| "基金持仓" | funds |
| "余额 / 现金 / X 货币多少钱" | balance(--currency 推断) |
| "X 我能买多少 / 全仓买" | max-qty --side buy(LLM 在没价格时先调 #01 行情拿当前价填 --price) |
| "X 我能卖多少" | max-qty --side sell |
| "X 保证金率 / 仓位 / 杠杆要求" | margin-ratio |
| "账户全貌 / 整个账户" | portfolio |
| "我能赚多少 / 浮盈" | positions(LLM 在 datas 里算 (last - cost) × qty)|

### 关于 max-qty 的两步流程

LLM 在用户说"X 我能买多少股"时:
1. 如果是限价 LO(默认),LLM 必须先用 #01 行情查询拿到当前价 → 填 `--price`
2. 如果是市价 MO,直接 `--order-type MO`,无需 `--price`
3. 返回 `cash_max_qty`(纯现金) 与 `margin_max_qty`(含融资);回答时区分两者并提示融资风险

### 数据敏感性

本 skill 涉及账户私有数据。SKILL.md 必须包含一段:

> **隐私提示**:本技能返回的持仓 / 余额 / 保证金等数据是用户账户的私有信息。请只在与本人对话时返回详细数字;若怀疑会话上下文有第三方观察(如截图、屏幕共享),先与用户确认是否要展示。

## 验收清单

- [ ] positions:返回 datas 数组(可能为空,空数组也是 success)
- [ ] balance:`--currency USD` 与无 `--currency` 行为正确
- [ ] max-qty:`cli.py max-qty TSLA.US --side buy --price 250` 返回 cash_max_qty / margin_max_qty
- [ ] portfolio:三个子字段齐全
- [ ] margin-ratio:返回 im/mm/fm 三个 factor
- [ ] auth_expired:登出后调任意子命令 → `auth_expired`
- [ ] 集成层:6 句话验证
  - "我的持仓"
  - "我账户里有多少钱"
  - "NVDA 我能买多少股"(双步:先 #01 拿价,再 max-qty)
  - "茅台保证金率"
  - "看一下我的账户全貌"
  - "我有多少 HKD"

## 已知 trade-off

- iwencai 没有此类账户类 skill,这是长桥独家。中文用户问"我账户怎么样" / "我能买多少"是高频问句,值得独立 skill。
- `max-qty` 需要先拿当前价,跨 skill 调用对 LLM 是认知负担。SKILL.md 给出明确两步示例,确保稳定。
- "我能赚多少 / 浮盈"靠 LLM 在 positions 数据上做算术(last - cost) × qty。底层 positions 不直接返浮盈字段,SKILL.md 说明这点。
