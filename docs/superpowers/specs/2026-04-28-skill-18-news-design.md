# 资讯舆情(skill #18)— 差异化设计

**Date:** 2026-04-28
**Status:** Draft(analysis-tier,prompt-only,**强依赖 MCP**;可选 WebSearch fallback)
**Protocol:** 偏离同 #14

## 业务范围

回答 **"X 最近什么新闻 / 公告 / 市场怎么看"** 这一类问题,把零散新闻 / 公告 / 社区帖子聚合并分类。

跟 raw `mcp__longbridge__news` 单工具的区别:
- raw news 一次只返回新闻列表,LLM 直接把 10 条标题甩给用户
- 本 skill 让 LLM 在结果上做**分类(catalyst / 监管 / 解读 / 其它)+ 提炼关键事实 + 整体语义判断**,然后必要时 chain WebSearch

- 编排 MCP 工具:`news`、`filings`(公告)、`topic`(社区话题)、`topic_detail`、`topic_replies`
- chain:WebSearch(只在 MCP 数据不足时,且明确告知用户是网络搜索)
- 不做:**不做主观判断**(不说"利好 / 利空"原话,允许说"市场普遍解读为利好");不做投资建议

## front-matter

```yaml
---
name: 资讯舆情
description: 综合查询某只股票或某家公司的最近新闻、监管公告(filings)、长桥社区讨论。当用户询问 X 最近新闻 / X 公告 / 市场对 X 财报怎么看 / X 社区在聊什么 / X 公司动态等场景必须使用此技能。返回事实摘要 + 分类 + 整体语义,不构成投资建议。
license: Complete terms in LICENSE.txt
version: 1.0.0
risk_level: read_only
requires_login: false
default_install: true
requires_mcp: true
---
```

## 工具编排逻辑

| 用户语义 | 调用 |
|---|---|
| "X 最近新闻" | `news(symbol=X, limit=10)` |
| "X 公告 / 8-K / 港交所披露" | `filings(symbol=X, limit=10)` |
| "X 财报后市场怎么看" / "市场情绪" | `news` + `topic(symbol=X)` 综合 |
| "X 社区在聊什么" | `topic` + `topic_detail`(挑热门) + `topic_replies` |
| "X 全面综述"(默认) | news + filings + topic 三者并发 |

## SKILL.md 核心步骤

### 步骤 1:识别 symbol(同行情查询规则)+ 决定深度

| 关键词 | 深度 |
|---|---|
| "新闻 / news" | news only |
| "公告 / 披露 / filing / 8-K" | filings only |
| "市场怎么看 / 市场情绪" | news + topic |
| "全面 / 综述 / 看一下 X" | 三者并发 |

### 步骤 2:并发调对应工具

```
mcp__longbridge__news(symbol=X, limit=10)
mcp__longbridge__filings(symbol=X, limit=10)
mcp__longbridge__topic(symbol=X)  # 社区热门话题
```

### 步骤 3:LLM 在结果上做分类

LLM 把 news 数组按以下分类(必须做,不能直接列):

| 分类 | 关键词识别 |
|---|---|
| **catalyst**(基本面 / 业绩) | 财报 / 营收 / 利润 / 业绩 / EPS / earnings / revenue |
| **regulatory**(监管 / 合规) | 调查 / 处罚 / 合规 / SEC / 证监会 / fine / lawsuit |
| **strategic**(战略 / 业务) | 收购 / 合作 / 拆分 / 新产品 / launch / partnership |
| **financial**(资本动作) | 增发 / 回购 / 分红 / split / buyback / dividend |
| **opinion**(分析师 / 评级) | 评级 / 目标价 / upgrade / downgrade / analyst |
| **other** | 其他 |

### 步骤 4:输出结构化摘要

回答模板:

```
X 最近资讯综述(数据来源:长桥证券)

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

【社区讨论(若调了 topic)】
- 热门话题 N 个:话题标题 + 评论数
- 整体讨论倾向:(只允许说"积极/中性/消极占比",不允许说"利好"/"利空"原话)

【关键事实提炼】(LLM 必须给一段 100 字内的纯事实总结)
- ...

⚠️ 资讯解读受时效与立场影响,本数据不构成投资建议。
```

### 步骤 5:WebSearch fallback(可选)

仅在以下情况下 LLM 主动调 WebSearch:
- MCP `news` 返回为空 / 数据明显过时(最新一条 > 7 天前)
- 用户问的事件 MCP 数据集没覆盖(如刚发生的并购、突发监管事件)

调 WebSearch 时**必须明示**:"以下为网络搜索结果,非长桥数据"。

### 步骤 6:chain 到其它 skill

- 用户接着问财报详情 → 「基本面分析」(#15)
- 用户问估值是否反映了利空 → 「估值分析」(#14)
- 用户问"社区在炒哪只股票"(无具体 symbol) → raw `mcp__longbridge__topic` 不带 symbol 参数(若 MCP 支持),否则反问

## 输出形态约束

- **必须**分类(不能直接 dump 标题列表)
- **必须**关键事实段(100 字内,LLM 自己提炼)
- **必须**末尾"不构成投资建议"
- **不要**说"利好 / 利空 / 看多 / 看空"原话(主观判断);允许说"市场普遍解读为正面 / 负面"(因有 evidence)
- **不要**编新闻;若 MCP 数据稀少就如实告知,fallback WebSearch 也明示

## 验收清单

- [ ] 问"NVDA 最近新闻",LLM 调 news,分类后输出
- [ ] 问"NVDA 公告",LLM 调 filings(不调 news)
- [ ] 问"市场对 X 财报怎么看",LLM 调 news + topic 综合
- [ ] 分类标题准确(财报相关进 catalyst 类,监管处罚进 regulatory 类)
- [ ] 关键事实段控制在 100 字内
- [ ] MCP news 返回为空时,LLM 主动 WebSearch 并明示"网络搜索"
- [ ] 末尾"不构成投资建议"
- [ ] 不出现"利好 / 利空"原话

## 已知 trade-off

- MCP news 数据更新可能滞后(几小时到 1 天) → 用户问"突发新闻"时 LLM 应主动 WebSearch
- topic_replies 评论质量参差,LLM 不应直接引用具体评论(选择性 cherry-pick 风险),只统计倾向(正/中性/负各占多少)
- "情绪倾向"判断本身有偏差(NLP 难题),SKILL.md 让 LLM 用粗粒度("多数积极"/"明显消极")而不是给精确比例
- 公司中文名 ↔ 英文 ticker 映射偶尔失败(如"特斯拉"→ TSLA 大概率成功,但小盘股可能不成),失败时反问用户
- 社区讨论涉及合规边界,**不能让 LLM 引导炒作**;SKILL.md 让 LLM 在出现"涨停板 / 主升浪 / 建议买入"等 hype 词时降级为只统计、不重复
