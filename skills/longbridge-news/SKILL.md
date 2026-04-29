---
name: 资讯舆情
description: 综合查询某只股票或某家公司的最近新闻、监管公告(filings)、长桥社区讨论。当用户询问 X 最近新闻 / X 公告 / 市场对 X 财报怎么看 / X 社区在聊什么 / X 公司动态 / 市场情绪等场景必须使用此技能。返回事实摘要 + 分类 + 整体语义,不构成投资建议。
license: Complete terms in LICENSE.txt
version: 1.0.0
risk_level: read_only
requires_login: false
default_install: true
requires_mcp: true
---

# 资讯舆情 使用指南

## 版本

`1.0.0`

## 技能概述

本技能是 **prompt-only 分析层**(无 cli.py),把零散的新闻 / 公告 / 社区讨论聚合并**分类 + 提炼关键事实 + 给整体语义判断**,而不是直接 dump 标题列表。

跟单独 `mcp__longbridge__news` 工具的区别:
- raw news 一次返回新闻列表,容易被 LLM 直接朗读 10 条标题
- 本技能让 LLM 在结果上做**分类(catalyst / 监管 / 解读 / 其它)+ 关键事实提炼 + 倾向判断**,必要时 chain WebSearch

数据来源:**长桥证券**(https://longbridge.com)+ 必要时 WebSearch fallback(明示标注)

## 使用前(必读)

本技能**强依赖** longbridge 官方 MCP 服务,不走本地 CLI。用户必须先配置:

```bash
claude mcp add --transport http longbridge https://openapi.longbridge.com/mcp
```

首次工具调用会触发浏览器 OAuth 授权(只需 `quote` scope)。

## 何时使用本技能

当用户询问以下问题时,**必须**使用本技能:
- "NVDA 最近新闻"、"特斯拉最近怎么了"
- "茅台公告"、"700 港交所披露"、"NVDA 8-K"
- "市场对 X 财报怎么看"、"X 财报后股价为什么跌"
- "X 社区在聊什么"、"长桥社区怎么看 NVDA"
- "X 全面综述 / X 最近动态"

## 核心处理流程

### 步骤 0:确认 MCP 已就绪

如果用户的 `claude mcp list` 不含 `longbridge`,先提示装 MCP(见上「使用前」章节)。本技能没有 CLI 路径。

### 步骤 1:识别 symbol + 决定深度

从用户问句里抽出股票名 / 代码,补全 `<CODE>.<MARKET>`(规则同行情查询)。

按问句关键词决定调哪些工具:

| 关键词 | 深度 | 调用 |
|---|---|---|
| "新闻 / news / 最近怎么了" | news only | `news(symbol=X, limit=10)` |
| "公告 / 披露 / filing / 8-K / 中报 / 业绩预告" | filings only | `filings(symbol=X, limit=10)` |
| "市场怎么看 / 市场情绪 / 反应 / 解读" | news + topic | `news` + `topic(symbol=X)` |
| "社区 / 讨论 / 话题" | topic-heavy | `topic` + `topic_detail`(挑热门) + `topic_replies` |
| "全面 / 综述 / 看一下 X / X 动态"(默认) | 三者并发 | `news` + `filings` + `topic` |

### 步骤 2:并发调对应 MCP 工具

例(默认综述档):

```
mcp__longbridge__news(symbol=X, limit=10)
mcp__longbridge__filings(symbol=X, limit=10)
mcp__longbridge__topic(symbol=X)             # 社区热门话题
```

社区深挖时再追加:`topic_detail(topic_id=...)` + `topic_replies(topic_id=...)`。

### 步骤 3:LLM 在结果上做分类(必做,不能直接 dump)

把 news 数组按以下 6 类归档:

| 分类 | 关键词识别 |
|---|---|
| **catalyst**(基本面 / 业绩) | 财报 / 营收 / 利润 / 业绩 / EPS / earnings / revenue / guidance |
| **regulatory**(监管 / 合规) | 调查 / 处罚 / 合规 / SEC / 证监会 / fine / lawsuit / 罚款 |
| **strategic**(战略 / 业务) | 收购 / 合作 / 拆分 / 新产品 / launch / partnership / 上线 |
| **financial**(资本动作) | 增发 / 回购 / 分红 / split / buyback / dividend / 股权激励 |
| **opinion**(分析师 / 评级) | 评级 / 目标价 / upgrade / downgrade / analyst / 调高 / 调低 |
| **other** | 其他无法明确归类的 |

### 步骤 4:输出结构化摘要

**必须**用以下模板,空类略过(不要硬凑空段),但**关键事实段必填**:

```
X (代码) 最近资讯综述(数据来源:长桥证券)

【过去 X 天 N 条新闻 + M 条公告】

🟢 业绩 / 基本面(N 条)
- [日期] 标题:一句关键事实(数字 / 比例)
- [日期] 标题:...

🟡 战略 / 业务(N 条)
- [日期] ...

🔴 监管 / 合规(N 条)
- [日期] ...(若有,务必单独突出)

📈 分析师观点(N 条)
- [日期] X 评级 by 机构,目标价 ¥Y(原 ¥Z)

📃 监管公告 / Filings
- [日期] 8-K / 中报 / 业绩预告 / ...

💬 社区讨论(若调了 topic)
- 热门话题 N 个:话题标题 + 评论数
- 整体讨论倾向:积极 X% / 中性 Y% / 消极 Z%(粗粒度,不引用具体评论)

【关键事实提炼】(100 字内,纯事实)
- ...

⚠️ 资讯解读受时效与立场影响,本数据不构成投资建议。
```

### 步骤 5:WebSearch fallback(可选)

仅在以下情况下,LLM 主动调 WebSearch:
- MCP `news` 返回为空 / 数据明显过时(最新一条 > 7 天前)
- 用户问的事件 MCP 数据集没覆盖(如刚发生的并购、突发监管事件)

调 WebSearch 时**必须明示**:"以下为网络搜索结果,非长桥数据。"

### 步骤 6:chain 到其它 skill

| 用户后续问 | 路由到 |
|---|---|
| "X 财报详情" | 「基本面分析」(#15) |
| "估值是否反映了利空" | 「估值分析」(#14) |
| "X 跟 Y 谁受影响大" | 「同行对比」(#16) |
| "社区在炒哪只股票"(无具体 symbol) | raw `mcp__longbridge__topic` 不带 symbol(若 MCP 支持),否则反问 |

## 输出形态约束

- **必须**分类(不能直接 dump 标题列表)
- **必须**关键事实段(100 字内,LLM 自己提炼)
- **必须**末尾"不构成投资建议"
- **不要**说"利好 / 利空 / 看多 / 看空"原话(主观判断);允许说"市场普遍解读为正面 / 负面"(因有 evidence)
- **不要**编新闻;若 MCP 数据稀少就如实告知,fallback WebSearch 也明示
- **不要**引用具体社区评论原文(选择性 cherry-pick 风险),只统计倾向占比

## 合规边界

社区讨论涉及合规边界——**不能让 LLM 引导炒作**。

LLM 在 topic / topic_replies 结果中遇到以下 hype 词时,**只统计、不重复**:
- "涨停板"、"主升浪"、"建议买入"、"必涨"、"满仓"、"all in"
- "次新妖股"、"XX 概念龙头"、"庄家"、"游资"

这些词出现频率高时,可以**降级**为"社区讨论包含较多投机性话题",不引用原话。

## 错误处理

| 触发场景 | 用户侧话术 |
|---|---|
| MCP `longbridge` 未配置 | "本技能需要长桥 MCP,请先运行 `claude mcp add --transport http longbridge https://openapi.longbridge.com/mcp`。" |
| MCP `news` 返回为空 | "{symbol} 在长桥数据集里暂无近期新闻;尝试用 WebSearch 补充网络结果(以下为非长桥数据)。" |
| MCP `news` 数据明显过时(> 7 天) | "{symbol} 长桥新闻数据已 N 天未更新;切到 WebSearch 抓最新(以下为非长桥数据)。" |
| 公司中文名 ↔ ticker 映射失败 | "无法把「{用户输入}」映射到具体股票代码;请告诉我代码或英文 ticker。" |

## 已知 trade-off

- **MCP news 数据更新可能滞后**几小时到 1 天 → 突发新闻请 WebSearch
- **topic_replies 评论质量参差** → LLM 不直接引用,只统计倾向占比
- **情绪倾向判断本身有偏差**(NLP 难题) → LLM 用粗粒度("多数积极"/"明显消极"),不给精确比例
- **公司中文名映射**对小盘股可能失败(如"特斯拉"→ TSLA 大概率成功,但小众标的可能不成),失败时反问用户

## MCP 工具速查

| MCP 工具名 | 拿什么 |
|---|---|
| `mcp__longbridge__news` | 公司相关新闻列表 |
| `mcp__longbridge__filings` | 监管公告(港交所披露 / SEC / 证监会等) |
| `mcp__longbridge__topic` | 长桥社区相关话题 |
| `mcp__longbridge__topic_detail` | 单个话题详情 |
| `mcp__longbridge__topic_replies` | 话题下的评论 |

## 代码结构

```
资讯舆情/
└── SKILL.md          # 本文件(prompt-only,无 cli.py)
```
