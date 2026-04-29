---
name: 投资组合分析
description: 账户级分析——总市值 / 现金占比 / 浮盈浮亏 / 单股贡献排名 / 行业分布 / 货币暴露 / 历史 P/L 曲线。当用户询问我账户表现如何 / 我本月浮盈 / 哪只股贡献最多 / 我组合配置合理吗 / 我货币暴露 / 我账户行业分布等场景必须使用此技能。需要 longbridge login 且账户已开通 trade scope。
license: Complete terms in LICENSE.txt
version: 1.0.0
risk_level: account_read
requires_login: true
default_install: true
requires_mcp: true
---

# 投资组合分析 使用指南

## 版本

`1.0.0`

## 技能概述

本技能是 **prompt-only 分析层**(无 cli.py),回答**"我账户表现如何 / 哪只股贡献最多"**这类**账户级**问题。

跟「持仓查询」(#08)的区别:
- **#08 持仓查询**:账户**快照 lookup**(回答"我有什么 / 多少钱 / 当前余额")
- **#17 投资组合分析**:账户级**分析**(回答"我表现如何 / 多赚多亏 / 配置怎么样")

输出按 4 段组织:
- **总览**:总市值 / 现金 / 持仓占比 / 期间浮盈浮亏
- **币种敞口**:USD / HKD / CNY / SGD 各占多少
- **单股贡献**:哪只股票本期贡献了多少浮盈 / 浮亏(排名)
- **行业分布**:持仓的行业聚合占比

数据来源:**长桥证券**(https://longbridge.com)

## 使用前(必读)

### 1. 配置 MCP

```bash
claude mcp add --transport http longbridge https://openapi.longbridge.com/mcp
```

### 2. ⚠️ trade scope 警告

`profit_analysis / profit_analysis_detail / stock_positions / account_balance` 都需要 **trade scope** OAuth token。

**首次调用 MCP 工具时弹浏览器授权,务必勾选「交易」权限**。

如果 `claude mcp` 已配置但调用返回 auth scope 错误(`unauthorized` / `not in authorized scope`),请运行:

```bash
claude mcp logout longbridge
# 再触发任意 MCP 工具调用,重新授权时勾选「交易」权限
```

## 何时使用本技能

当用户询问以下问题时,**必须**使用本技能:
- "我账户表现如何"、"我本月浮盈"、"我今年赚了多少"
- "我哪只股票贡献最多"、"我账户里谁拖后腿"
- "我货币暴露"、"我 USD / HKD / CNY 各占多少"
- "我组合行业分布"、"我科技股占比"
- "我账户全貌"

## 隐私强提示

本技能返回**用户账户私有金额数据**(总市值 / 浮盈 / 持仓金额)。

**LLM 必须**:
- 只在与本人对话时返回详细数字
- 若怀疑会话上下文有第三方观察(截图、屏幕共享、录屏),先与用户确认是否要展示具体数字
- 不主动把账户金额数字写入 PR / 提交日志 / 工单等会被第三方看到的位置

## 核心处理流程

### 步骤 0:确认 MCP + trade scope

如果用户的 `claude mcp list` 不含 `longbridge`,先提示装 MCP。

如果调任意工具返回 unauthorized,引导用户重新授权(见上「使用前 - 2」)。

### 步骤 1:理解用户的"我"指什么

中文用户的"我"通常是单一账户。但长桥可能有多 sub-account。**默认按"全账户聚合"回答**,如果用户特意问"我的 A 股账户" / "我的港股账户"再细分。

### 步骤 2:决定时间窗(若需要)

按用户问句关键词:

| 关键词 | 时间窗 |
|---|---|
| "本月" | 本月 1 日 → today |
| "本周" | 本周一 → today |
| "近 30 天" | today-30 → today |
| "今年" | 今年 1 月 1 日 → today |
| "全部" / 没说时间 | 用 profit_analysis 默认(通常是开户至今) |

> 今天日期由 LLM 上下文获取(系统提示 `Today's date is YYYY-MM-DD`)。

### 步骤 3:并发调 MCP 工具

按用户问题选工具集:

| 用户语义 | 调用 |
|---|---|
| "我账户全貌 / 持仓 + 余额 + 浮盈" | 全调:portfolio combo + profit_analysis(默认时间) |
| "我本月浮盈" | profit_analysis(start=本月 1 日, end=today) |
| "哪只股贡献最多" | profit_analysis_detail + stock_positions(交叉验证) |
| "我货币暴露" | account_balance(全币种) + exchange_rate(USD 基准) |
| "我组合行业分布" | stock_positions + 对每只 symbol 调 static_info 拿行业 |

例(用户问"我本月账户表现"):

```
mcp__longbridge__profit_analysis(start_date="2026-04-01", end_date="2026-04-28")
mcp__longbridge__profit_analysis_detail(start_date="2026-04-01", end_date="2026-04-28")
mcp__longbridge__account_balance()
mcp__longbridge__stock_positions()
mcp__longbridge__exchange_rate()
```

### 步骤 4:综合输出(4 段必填结构)

**必须**用以下模板,某段数据缺失明示"暂未查到":

```
我的账户表现(数据来源:长桥证券,统计期间 YYYY-MM-DD ~ YYYY-MM-DD)

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
| TSLA.US | Tesla | -$1,800 | -15% |
| ... | ... | ... | ... |

【4. 行业分布】(基于 stock_positions × static_info 行业字段聚合)
- 半导体:35%
- 互联网:20%
- ...

⚠️ 浮盈浮亏受市场短期波动影响,不代表长期收益。本数据不构成调仓建议。
```

### 步骤 5:chain 到其它 skill

| 用户后续问 | 路由到 |
|---|---|
| "我自选股有哪些"(读) | 「自选股」(#10) |
| 对某只股票详情 | 「行情查询」(#01)/「估值分析」(#14)/「基本面分析」(#15) |
| "我应该减仓 X 吗" | **不给建议**,改给该 symbol 的估值 + 基本面数据(链 #14 #15)让用户自己判 |
| "X 最近新闻 / 我手上 X 为什么跌" | 「资讯舆情」(#18) |

## 输出形态约束

- **必须**给 4 段(总览 / 币种 / 单股贡献 / 行业)
- **必须**所有金额标注币种,USD 等价用 `≈`
- **必须**末尾"不构成调仓建议" + "数据来源:长桥证券"
- **不要**给"建议减仓 / 加仓 X"建议
- **不要**给"你账户配置不合理"这类**主观判断**;允许说"科技板块占比 60%,行业集中度高"这类**数据描述**

## 行业分布性能优化

行业分布需要对每只持仓调 `static_info` 拿 industry 字段,**N 只持仓 = N 个调用**。

- 持仓 ≥ 30 只时,LLM 应**提示**"行业分布计算稍慢,正在并发拉取..." 或**简化**(只取按市值 top 10 的行业,其余归"其它")
- 单股贡献排名同理,默认列 top 10(正负各取重要的),不全部铺出

## 错误处理

| 触发场景 | 用户侧话术 |
|---|---|
| MCP `longbridge` 未配置 | "本技能需要长桥 MCP,请先运行 `claude mcp add --transport http longbridge https://openapi.longbridge.com/mcp`。" |
| 缺 trade scope | "本技能需要交易权限的 OAuth scope。请运行 `claude mcp logout longbridge`,下次触发任意 MCP 工具调用时,在浏览器授权页**勾选「交易」权限**。" |
| profit_analysis 返回空 | "{时间窗}内长桥未记录任何盈亏(可能账户当期无持仓 / 无成交)。" |
| account_balance 返回单币种 | "你的账户目前只有 {币种} 余额,跳过多币种敞口段。" |
| stock_positions 返回空 | "你目前无持仓,'单股贡献'与'行业分布'两段跳过,只显示现金余额。" |

## 已知 trade-off

- **profit_analysis 不一定按 USD 标准化**,可能多币种汇总 → LLM 用 `exchange_rate` 工具自己换算到 USD 等价(汇率取调用当日)
- **行业分布对 N 只持仓需要 N 个 static_info 调用** → 持仓 ≥ 30 只时简化到 top 10
- **多 sub-account 聚合规则不明**(longbridge 是否合并需看 MCP 工具实际行为) → 实施时观察实际数据,文案根据观察调整
- **"贡献排名"按金额还是按 % 有不同口径** → 默认按 USD 等价绝对值;用户问"哪只涨幅最大"时切到 % 排序

## MCP 工具速查

| MCP 工具名 | 拿什么 | 必需 scope |
|---|---|---|
| `mcp__longbridge__profit_analysis` | 期间盈亏汇总 | trade |
| `mcp__longbridge__profit_analysis_detail` | 单股盈亏明细 | trade |
| `mcp__longbridge__stock_positions` | 当前持仓快照 | trade |
| `mcp__longbridge__account_balance` | 多币种余额 | trade |
| `mcp__longbridge__fund_positions` | 基金持仓(若有) | trade |
| `mcp__longbridge__exchange_rate` | 货币换算 | quote |
| `mcp__longbridge__static_info` | 行业字段(用于行业分布聚合) | quote |

## 代码结构

```
投资组合分析/
└── SKILL.md          # 本文件(prompt-only,无 cli.py)
```
