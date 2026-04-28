# 投资组合分析(skill #17)— 差异化设计

**Date:** 2026-04-28
**Status:** Draft(analysis-tier,prompt-only,**强依赖 MCP + trade-scope OAuth token**)
**Protocol:** 偏离同 #14;另需 trade-scope token

## 业务范围

回答 **"我账户表现如何 / 哪只股票贡献最多 / 配置合不合理"** 这一类**账户级**问题。

跟 #08 持仓查询 的区别:
- #08 是**账户快照 lookup**(回答"我有什么 / 多少钱")
- #17 是**账户级分析**(回答"我表现如何 / 多赚多亏 / 配置怎么样")

- 编排 MCP 工具:`profit_analysis`、`profit_analysis_detail`、`exchange_rate`、`stock_positions`、`account_balance`、`fund_positions`
- chain 现有 skill:「持仓查询」(portfolio combo)+「行情查询」(批量当前价)
- 不做:**不给"调仓建议"**(只给数据 + 配置分析,绝对不说"建议减仓 / 加仓 X")

## front-matter

```yaml
---
name: 投资组合分析
description: 账户级分析——总市值 / 现金占比 / 浮盈浮亏 / 单股贡献排名 / 行业分布 / 货币暴露 / 历史 P/L 曲线。当用户询问我账户表现如何 / 我本月浮盈 / 哪只股贡献最多 / 我组合配置合理吗 / 我货币暴露等场景必须使用此技能。需要 longbridge login 且账户开通 trade scope。
license: Complete terms in LICENSE.txt
version: 1.0.0
risk_level: account_read
requires_login: true
default_install: true
requires_mcp: true
---
```

## OAuth scope 警告

`profit_analysis / profit_analysis_detail / stock_positions / account_balance` 都需要 **trade scope** OAuth token。如果用户当前 token 只有 quote scope,所有调用返回 auth_expired / not in authorized scope。

SKILL.md 必须在「使用前」段明确告诉用户:

> 本技能需要"交易"权限的 OAuth scope。若 `claude mcp` 已配置好但调用返回 auth scope 错误,请运行 `claude mcp logout longbridge && <retrigger>`,重新授权时**勾选交易权限**。

## 工具编排逻辑

| 用户语义 | 调用 |
|---|---|
| "我账户全貌 / 持仓 + 余额 + 浮盈" | 持仓查询 skill 的 portfolio combo + profit_analysis(默认时间段) |
| "我本月浮盈" | profit_analysis(start = 本月 1 日, end = today) |
| "我哪只股票贡献最多" | profit_analysis_detail(默认时间) + 当前 stock_positions(交叉验证) |
| "我货币暴露" | account_balance(全币种) + exchange_rate(USD 基准) |
| "我组合行业分布" | stock_positions + 对每个 symbol 调 quote 拿行业(行业字段在 static_info,需要拼) |

## SKILL.md 核心步骤

### 步骤 1:理解用户的"我"指什么

中文用户的"我"通常是单一账户;但长桥可能有多 sub-account。SKILL.md 让 LLM 默认按"全账户聚合"回答,如果用户特意问"我的 A 股账户" / "我的港股账户"再细分。

### 步骤 2:决定时间窗(若需要)

| 关键词 | 时间窗 |
|---|---|
| "本月" | 本月 1 日 - today |
| "本周" | 本周一 - today |
| "近 30 天" | today-30 - today |
| "今年" | 今年 1 月 1 日 - today |
| "全部" / 没说时间 | (使用 profit_analysis 默认,通常是开户至今) |

### 步骤 3:调工具

例:用户问"我本月账户表现"

```
mcp__longbridge__profit_analysis(start_date="2026-04-01", end_date="2026-04-28")
mcp__longbridge__profit_analysis_detail(start_date="2026-04-01", end_date="2026-04-28")
mcp__longbridge__account_balance()    # 当前余额(多币种)
mcp__longbridge__stock_positions()    # 当前持仓
mcp__longbridge__exchange_rate()      # 汇率(用于 USD 等价)
```

### 步骤 4:综合输出

回答模板:

```
我的账户表现(数据来源:长桥证券,统计期间 2026-04-01 ~ 2026-04-28)

【1. 总览】
- 总市值(以 USD 等价):$X
- 现金:$X(占比 Y%)
- 持仓市值:$X(占比 Y%)
- 期间浮盈:+$X(+Y%)

【2. 各币种敞口】
- USD: $X
- HKD: HK$X(≈ $X USD)
- CNY: ¥X(≈ $X USD)
- SGD: S$X(若有)

【3. 单股贡献排名(本期)】
| Symbol | 名字 | 浮盈 USD 等价 | 贡献占比 |
|---|---|---:|---:|
| NVDA.US | NVIDIA | +$5,200 | 42% |
| 700.HK | 腾讯 | +$3,100 | 25% |
| ... | ... | ... | ... |

【4. 行业分布】
(基于 stock_positions × static_info 行业字段聚合)
- 半导体:35%
- 互联网:20%
- ...

⚠️ 浮盈浮亏受市场短期波动影响,不代表长期收益。本数据不构成调仓建议。
```

### 步骤 5:chain 到其它 skill

- 用户问"我自选股有哪些"(读) → 「自选股」skill(#10)
- 用户接着问某只股票详情 → 行情查询(#01)/ 估值分析(#14)
- 用户问"我应该减仓 X 吗" → **不给建议**,改给该 symbol 的估值 + 基本面数据(链 #14 #15)让用户自己判

## 输出形态约束

- **必须**给 4 段(总览 / 币种 / 单股贡献 / 行业)
- **必须**所有金额标注币种,USD 等价用 ≈
- **必须**末尾"不构成调仓建议"+ "数据来源:长桥证券"
- **不要**给"建议减仓 / 加仓 X"建议
- **不要**给"你账户配置不合理"这类主观判断;允许说"科技板块占比 60%,行业集中度高"这类**数据描述**

## 隐私强提示

本 skill 返回**用户账户私有金额数据**。SKILL.md 必须包含一段:

> **隐私提示**:本技能返回的金额、持仓、浮盈浮亏数据是用户账户私有信息。请只在与本人对话时返回详细数字。若怀疑会话上下文有第三方观察(截图、屏幕共享),先与用户确认是否要展示。

## 验收清单

- [ ] 用户已配置 trade scope token,问"我账户本月表现",LLM 调上述工具,返回 4 段
- [ ] 缺 trade scope 时返回 auth_expired,SKILL.md 引导用户重新授权(勾交易权限)
- [ ] 货币标签齐全,USD 等价标 ≈
- [ ] 单股贡献排名按浮盈绝对值排序,正负都列
- [ ] 用户问"我应该卖 X 吗",LLM **不给建议**,改给该 symbol 数据
- [ ] 末尾"不构成调仓建议"

## 已知 trade-off

- profit_analysis 不一定按 USD 标准化,可能多币种汇总,LLM 要用 exchange_rate 工具自己换算到 USD 等价
- 行业分布需要对每只 symbol 调 static_info 拿行业字段,N 只持仓 = N 个调用,可能慢 → 当持仓 ≥ 30 只时让 LLM 提示"行业分布计算稍慢"或简化(只取 top 10 持仓的行业)
- 多 sub-account 聚合规则不明确(longbridge 是否合并,需要看 MCP 工具行为) → 实施时观察实际数据,SKILL.md 文案根据观察调整
- "贡献排名"按金额还是按百分比有不同口径,SKILL.md 默认按 USD 等价绝对值,如果用户问"哪只涨幅最大"就是按 % 排
