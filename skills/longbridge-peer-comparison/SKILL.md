---
name: 同行对比
description: 横向对比 2-5 只股票——估值(PE/PB/PS)+ 当前涨跌 + 最新业绩 + 市值规模 + 分红率,生成数据矩阵。当用户询问 X 和 Y 哪个值得买 / 哪个贵 / 哪个增速快 / 几只股票对比 / 同行业谁最强 / X vs Y 等场景必须使用此技能。返回数据,不构成投资建议。
license: Complete terms in LICENSE.txt
version: 1.0.0
risk_level: read_only
requires_login: false
default_install: true
requires_mcp: true
---

# 同行对比 使用指南

## 版本

`1.0.0`

## 技能概述

本技能是 **prompt-only 分析层**(无 cli.py),用于**多 symbol 横向对比**(2-5 只)。

这是分析层最大价值场景——单 MCP 工具一次只查一个 symbol,LLM 直接调 10 个工具拼对比表很容易丢字段、忘归一化。本技能就是**多 symbol orchestration 的标准化**,生成统一的对比矩阵。

数据来源:**长桥证券**(https://longbridge.com)

## 使用前(必读)

本技能**强依赖** longbridge 官方 MCP 服务,不走本地 CLI。用户必须先配置:

```bash
claude mcp add --transport http longbridge https://openapi.longbridge.com/mcp
```

首次工具调用会触发浏览器 OAuth 授权(只需 `quote` scope)。

## 何时使用本技能

当用户询问以下问题时,**必须**使用本技能:
- "茅台 五粮液 哪个便宜"、"NVDA AMD 哪个增速快"
- "AAPL vs GOOG vs MSFT"
- "几只股票对比"、"科技七姐妹谁最强"
- "茅台跟 700 谁估值低"(跨币种 + 跨行业,要 disclaim 但仍出表)
- "同行业谁最值得买"(给数据矩阵,不下结论)

## 核心处理流程

### 步骤 0:确认 MCP 已就绪

如果用户的 `claude mcp list` 不含 `longbridge`,先提示装 MCP(见上「使用前」章节)。本技能没有 CLI 路径。

### 步骤 1:解析多个 symbol(2-5 个)

从用户问句里抽出每只股票的名 / ticker,逐个补全 `<CODE>.<MARKET>`(规则同行情查询)。

**保护**:
- 0 个 symbol → 反问"想对比哪几只?"
- **1 个 symbol** → 改路由到「估值分析」(#14)或「基本面分析」(#15),**不在本 skill 跑**(本 skill 是"对比"而不是"单股分析")
- ≥ 6 个 symbol → 反问用户"对比 6 只以上数据矩阵不易读,挑核心 3-5 只如何?"
- 跨币种(如 NVDA.US + 600519.SH) → 仍可对比,但**表格上方加 disclaimer**:"跨币种对比仅看相对水平,不直接换算"
- 跨行业(如 NVDA + 茅台) → 仍可对比,但**强 disclaim**:"跨行业对比意义有限,估值阈值不可比"

### 步骤 2:对每个 symbol 并发拉数据

对**每一个** symbol 都并发调以下 4 个工具:

```
mcp__longbridge__quote(symbol=X)
mcp__longbridge__calc_indexes(symbol=X, indexes="pe,pb,ps,dividend_yield,total_market_value,turnover_rate")
mcp__longbridge__latest_financial_report(symbol=X)
mcp__longbridge__valuation(symbol=X)
```

**不调** `financial_report (IS/BS/CF)` 完整三表——多 symbol 时数据爆炸,只取 latest_financial_report 的 KPI 就够。

### 步骤 3:归一化 + 生成对比表

LLM 必须把不同币种数据**注明币种**(不强行换算,因为汇率引入误差;让用户看数字 + 货币标签)。

**必须**用 markdown 表格,行 = 维度,列 = symbol。模板:

```
{symbol₁ vs symbol₂ vs ...} 对比(数据来源:长桥证券)
[若跨币种 / 跨行业,在此加 disclaimer]

| 维度 | 茅台 (600519.SH) | 五粮液 (000858.SZ) | 泸州老窖 (000568.SZ) |
|---|---|---|---|
| 当前价 (CNY) | 1450.20 | 156.30 | 165.40 |
| 今日涨跌 | +1.2% | -0.5% | +0.8% |
| 总市值 | 1.82 万亿 CNY | 6068 亿 CNY | 2434 亿 CNY |
| **估值** | | | |
| PE (TTM) | 22.4 | 18.1 | 19.6 |
| PB | 7.8 | 5.2 | 6.5 |
| PS | 9.1 | 4.8 | 5.5 |
| 股息率 | 2.5% | 2.8% | 1.6% |
| **业绩(最近报告期)** | | | |
| 营收同比 | +14.7% | +8.2% | +12.3% |
| 净利同比 | +18.3% | +6.5% | +14.0% |
| ROE | 33.2% | 24.8% | 30.1% |

【综合观察】(数据驱动,不构成建议)
- 估值:茅台 PE / PB / PS 三项都最贵
- 增长:茅台营收和净利同比领先
- 分红率:五粮液最高
- 规模:茅台市值约为五粮液 3 倍

⚠️ 估值 + 增长不能直接定结论;高估值通常对应更高确定性 / 品牌溢价。
本数据不构成投资建议,请结合自身风险偏好判断。
```

### 步骤 4:绝对禁止

- **不**输出"我推荐 X"或"X 更值得买"
- **不**基于以上数据给"应该买 X 不应该买 Y"建议
- **综合观察**段只能讲**数据呈现的事实**(谁高谁低 / 趋势谁强),不能下结论
- **不**自动汇率换算(不同币种保留原币 + 标签)

### 步骤 5:chain 到其它 skill

| 用户后续问 | 路由到 |
|---|---|
| 对某只感兴趣,问详情 | 「估值分析」(#14)或「基本面分析」(#15),传该 symbol |
| "哪个最近资金流入多" | 对每只调「资金流向」skill,聚合返回 |
| "X 最近新闻 / 财报反应" | 「资讯舆情」(#18) |

## 输出形态约束

- **必须**用 markdown 表格,行 = 维度,列 = symbol
- **必须**注明每个数字的货币(CNY / USD / HKD / SGD)
- **必须**末尾"综合观察"用纯数据描述,不下结论
- **必须**末尾"不构成投资建议"
- **不要**自动汇率换算(不同币种保留原币 + 标签)
- 跨币种或跨行业时**必须**在表格上方加显式 disclaimer

## 跨市场对比的口径警告

不同市场的财报口径不严格可比:
- **A 股 / 港股 / 美股**用不同会计准则(IFRS / US GAAP / 中国会计准则)
- **ROE / 毛利率**计算口径有摊薄 vs 加权差异
- **披露节奏**不同(美股季度 / 港股半年 / A 股季度但慢)

LLM 在跨市场对比时**必须注明**:"以上数据来自不同会计准则下的财报,可作为粗略对比参考,精细分析请查原报表。"

## 错误处理

| 触发场景 | 用户侧话术 |
|---|---|
| MCP `longbridge` 未配置 | "本技能需要长桥 MCP,请先运行 `claude mcp add --transport http longbridge https://openapi.longbridge.com/mcp`。" |
| 部分 symbol 数据查不到 | "{symbol} 暂无 [estim/财报/quote] 数据,本行用 N/A 占位,其余 symbol 正常对比。" |
| 仅 1 个 symbol | "你只给了 1 只股票({symbol}),本技能用于横向对比 2-5 只;单股分析已切换到「估值分析」/「基本面分析」。" |
| ≥ 6 个 symbol | "你给了 N 只股票,对比 6+ 数据矩阵不易读;我挑前 5 只({symbol₁..symbol₅}),其余想看请单独问。" |

## 已知 trade-off

- **跨币种 + 跨行业对比意义有限**但用户有时会问 → 表格上方加 disclaimer,数据照给但**强烈提示**对比有局限
- **不同财报口径**(IFRS / US GAAP / CN GAAP)的数字不严格可比 → 跨市场注明
- **"ROE" 等比率计算口径**不同市场略不同(摊薄 vs 加权),粗略对比足够,精细分析需查原报表
- **2-5 只 × 4 工具 = 8-20 次 MCP 调用**,延迟会比单股分析高 — 必要时让 LLM 提示用户"对比拉取中,稍候"

## MCP 工具速查

| MCP 工具名 | 拿什么(对每个 symbol) |
|---|---|
| `mcp__longbridge__quote` | 当前价、涨跌幅、成交量、币种 |
| `mcp__longbridge__calc_indexes` | 估值指标(`pe,pb,ps,dividend_yield,total_market_value,turnover_rate`) |
| `mcp__longbridge__latest_financial_report` | 营收 / 净利同比、ROE |
| `mcp__longbridge__valuation` | 完整估值(交叉验证 calc_indexes) |

## 代码结构

```
同行对比/
└── SKILL.md          # 本文件(prompt-only,无 cli.py)
```
