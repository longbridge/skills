---
name: 估值分析
description: 综合分析股票的估值水平——当前 PE / PB / EV/EBITDA / PS 位置,在自身历史中的分位数,跟同行业平均/中位数的对比。当用户询问 X 估值贵不贵 / 是不是被低估 / 历史百分位 / 行业溢价折价 / X 现在适合买不等场景必须使用此技能。返回数据驱动的对比,不构成投资建议。
license: Complete terms in LICENSE.txt
version: 1.0.0
risk_level: read_only
requires_login: false
default_install: true
requires_mcp: true
---

# 估值分析 使用指南

## 版本

`1.0.0`

## 技能概述

本技能是 **prompt-only 分析层**(无 cli.py),通过编排长桥官方 MCP 工具,回答**"X 估值贵不贵"**这一类问题。

具体提供:
- **当前估值快照**:PE (TTM) / PB / PS / EV/EBITDA / 股息率
- **历史分位**:当前估值在过去 1-3 年里的百分位
- **行业对比**:相对于同行业的平均/中位数估值的溢价或折价
- **行业排名**:在行业内估值梯队的位置(贵 / 中等 / 便宜)

数据来源:**长桥证券**(https://longbridge.com)

## 使用前(必读)

本技能**强依赖** longbridge 官方 MCP 服务,不走本地 CLI。用户必须先配置:

```bash
claude mcp add --transport http longbridge https://openapi.longbridge.com/mcp
```

首次工具调用会触发浏览器 OAuth 授权(只需 `quote` scope,本技能不写账户)。

## 何时使用本技能

当用户询问以下问题时,**必须**使用本技能:
- "NVDA 估值贵不贵"、"特斯拉现在 PE 高吗"
- "茅台是不是被低估了"、"700 估值在历史什么位置"
- "宁德时代相对行业贵多少"、"半导体里 NVDA 算贵吗"
- "GOOG 现在适合买入吗"(估值角度,不给买卖建议)
- "X 历史 PE 分位数"

## 核心处理流程

### 步骤 0:确认 MCP 已就绪

如果用户的 `claude mcp list` 不含 `longbridge`,先提示装 MCP(见上「使用前」章节),不要硬撑去调本机 CLI——本技能没有 CLI 路径。

### 步骤 1:识别 symbol

从用户问句里抽出股票名 / 代码,补全为 `<CODE>.<MARKET>` 格式:
- 全大写英文 → `.US`(NVDA → `NVDA.US`)
- 4 位数字 → `.HK`(700 → `700.HK`)
- 6 位数字以 60 开头 → `.SH`(600519 → `600519.SH`)
- 6 位数字以 00/30 开头 → `.SZ`(300750 → `300750.SZ`)
- 中文公司名 → 用知识映射(腾讯 → `700.HK`,贵州茅台 → `600519.SH`,特斯拉 → `TSLA.US`)
- 多个 symbol(2-5 只) → **改路由到「同行对比」skill(#16)**,不在本技能跑
- 1 个 symbol 也没识别出 → 反问用户

### 步骤 2:并发调 MCP 工具

对单个 symbol 并发调 4 个工具:

```
mcp__longbridge__valuation(symbol=X)                 # 当前估值快照
mcp__longbridge__valuation_history(symbol=X)         # 历史时序,至少 1 年(推荐 3 年)
mcp__longbridge__industry_valuation(symbol=X)        # 行业平均/中位数
mcp__longbridge__industry_valuation_dist(symbol=X)   # 行业分位桶,看自己排第几
```

**可选**:盘中需要实时 PE 矫正时,额外调:
- 「行情查询」skill 的 `cli.py -s X --index pe,pb` (本机有 longbridge CLI 时)
- 或 `mcp__longbridge__calc_indexes(symbol=X, indexes="pe,pb")`(否则)

> 为什么:`valuation` 工具数据可能是收盘后才更新,盘中比对当前价用 calc-index 更准。

### 步骤 3:综合计算(LLM 在 datas 上做)

| 计算 | 方法 |
|---|---|
| 历史 PE 分位数 | 当前 PE 在 valuation_history 时间序列里的百分位 |
| 历史 PB 分位数 | 同上 |
| 行业相对溢价 | (当前 PE − 行业中位数 PE) / 行业中位数 PE |
| 行业排名 | 用 industry_valuation_dist 看自己在行业的哪个分位桶 |

如果 valuation_history 数据稀疏(< 1 年)或 industry_valuation 行业稀疏(< 5 家),**必须降级**——只给当前快照 + 行业相对值,不强行算分位数。

### 步骤 4:输出综合判断

**必须**用以下三段结构(LLM 不能省略任何一段;某段数据缺失要明确写"暂未查到"):

```
X (代码) 估值快照(数据来源:长桥证券)

【当前估值】
- PE (TTM): X
- PB:        X
- PS:        X
- EV/EBITDA: X(若有)
- 股息率:    X%

【历史维度(过去 3 年)】
- PE 在历史 X 分位(描述:偏低 / 中性 / 偏高)
- PB 在历史 X 分位

【行业维度(同行业 N 家公司)】
- PE 行业中位数 X → 当前比行业贵 / 便宜 X%
- 在行业内 PE 分位:第 X 位 / 共 N 位(高估 / 中等 / 低估梯队)

【综合】
从历史 + 行业两个维度看,当前估值 [偏低 / 中性 / 偏高]——X 维度处于 N 分位,Y 维度比行业 [贵/便宜] N%。

⚠️ 估值高低不等于"不能买"——成长股长期高估值是常态,需要结合业绩增速看。
本数据不构成投资建议。
```

### 步骤 5:必要时 chain 到其它 skill

| 用户后续问 | 路由到 |
|---|---|
| "X 业绩怎么样 / 财报" | 「基本面分析」(#15) |
| "X 跟同行 Y、Z 比哪个贵" | 「同行对比」(#16) |
| "X 跌到 N 提醒我" | raw `mcp__longbridge__alert_add` |
| "X 最近新闻 / 财报后市场怎么看" | 「资讯舆情」(#18) |

## 输出形态约束

- **必须**三个维度齐(当前快照 + 历史分位 + 行业分位);某段缺失明示"暂未查到"
- **必须**写"数据来源:长桥证券"
- **必须**末尾加"不构成投资建议"
- **不要**给"建议买 / 不建议买"这类话
- **不要**预测未来 PE 走势
- **可以**指出"历史 X 分位 + 行业 X 分位"组合下的常见解读(如"高估梯队"),但要带 hedge

## 周期性行业的特别提示

能源 / 化工 / 钢铁 / 航运 / 银行 / 地产等周期股的估值是**反向**的——行业谷底时 PE 反而高(因为净利润很低),那未必是"贵";行业高峰时 PE 低反而可能是顶部信号。

LLM 在判断这些行业的 PE 分位时,**必须额外说明**:"周期性行业的 PE 分位需结合行业景气周期解读,不能机械按数字判断贵贱"。

## 错误处理

| 触发场景 | 用户侧话术 |
|---|---|
| MCP `longbridge` 未配置 | "本技能需要长桥 MCP,请先运行 `claude mcp add --transport http longbridge https://openapi.longbridge.com/mcp`,首次调用会触发浏览器授权。" |
| 调 MCP 返回 auth / unauthorized | "长桥授权过期,请重新触发授权(任意 MCP 工具调用都会弹浏览器)。" |
| valuation 工具返回空 / 字段缺失 | "{symbol} 暂无估值数据(可能是非主流标的或刚上市)。" |
| valuation_history 数据稀疏 | "{symbol} 历史估值数据不足 1 年,无法给出可信的历史分位,只给当前快照 + 行业相对值。" |
| industry_valuation 行业样本稀疏 | "{symbol} 所在行业可比公司不足 5 家,行业分位仅供参考。" |

## MCP 工具速查

| MCP 工具名 | 拿什么 |
|---|---|
| `mcp__longbridge__valuation` | 当前估值快照(PE / PB / PS / EV/EBITDA / 股息率) |
| `mcp__longbridge__valuation_history` | 历史估值时序,用于算分位数 |
| `mcp__longbridge__industry_valuation` | 行业平均 / 中位数 |
| `mcp__longbridge__industry_valuation_dist` | 行业分位桶 |
| `mcp__longbridge__latest_financial_report` | 最新 EPS / BPS,可选用于交叉验证 |
| `mcp__longbridge__calc_indexes` | 盘中实时 PE / PB(可选) |

## 代码结构

```
估值分析/
└── SKILL.md          # 本文件(prompt-only,无 cli.py)
```

本技能不需要本地脚本——所有工具调用都是 LLM 直接发 MCP 请求,长桥服务端处理。
