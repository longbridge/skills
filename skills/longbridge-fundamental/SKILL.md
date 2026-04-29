---
name: 基本面分析
description: 综合分析公司基本面——最新财报关键 KPI(营收 / 净利 / EPS / ROE / 毛利率 / 现金流)、同比变化、分红历史、未来 EPS 一致预期、机构评级、股本与公司基本信息。当用户询问 X 基本面 / 业绩 / 财报 / 财务健康 / 分红 / EPS 预期 / 研报评级 / X 公司怎么样等场景必须使用此技能。返回数据,不构成投资建议。
license: Complete terms in LICENSE.txt
version: 1.0.0
risk_level: read_only
requires_login: false
default_install: true
requires_mcp: true
---

# 基本面分析 使用指南

## 版本

`1.0.0`

## 技能概述

本技能是 **prompt-only 分析层**(无 cli.py),通过编排长桥官方 MCP 工具,回答**"X 业绩怎么样 / 财务健康吗"**这类公司级问题。

按 5 个维度组织数据:
- **盈利能力**:营收、净利、毛利率、净利率、ROE
- **财务健康**:资产负债率、经营现金流、自由现金流、流动比率
- **增长趋势**:近 4 季营收 / 净利同比
- **股东回报**:分红历史、股息率、回购 / 增发(corp_action)
- **市场预期**:分析师 EPS 一致预期、综合评级、目标价

数据来源:**长桥证券**(https://longbridge.com)

## 使用前(必读)

本技能**强依赖** longbridge 官方 MCP 服务,不走本地 CLI。用户必须先配置:

```bash
claude mcp add --transport http longbridge https://openapi.longbridge.com/mcp
```

首次工具调用会触发浏览器 OAuth 授权(只需 `quote` scope,不写账户)。

## 何时使用本技能

当用户询问以下问题时,**必须**使用本技能:
- "贵州茅台 基本面"、"NVDA 业绩好不好"
- "腾讯财报怎么样"、"700 最新财报"
- "茅台分红历史"、"NVDA 股息率"
- "宁德时代 ROE"、"AAPL 毛利率"
- "X 下季度 EPS 预期"、"机构怎么看 NVDA"
- "X 财务健康吗"、"X 现金流怎么样"

## 核心处理流程

### 步骤 0:确认 MCP 已就绪

如果用户的 `claude mcp list` 不含 `longbridge`,先提示装 MCP(见上「使用前」章节)。本技能没有 CLI 路径。

### 步骤 1:识别 symbol

从用户问句里抽出股票名 / 代码,补全 `<CODE>.<MARKET>`(规则同行情查询:`.HK / .US / .SH / .SZ / .SG`)。

无法识别 / 多 symbol → 反问或路由(多 symbol 改路由到「同行对比」#16)。

### 步骤 2:决定深度档位

按用户问句里的关键词选档:

| 关键词 | 档位 | 工具集 |
|---|---|---|
| "怎么样 / 简单看一下" | **快照** | `latest_financial_report` + `forecast_eps` + `consensus` |
| "基本面 / 业绩 / 财报"(默认) | **标准** | + `financial_report` (IS/BS/CF latest period) + `dividend` |
| "全面 / 详细 / 全景" | **完整** | + `company` + `operating` + `corp_action` + `institution_rating` |

档位逐级累加(标准包含快照、完整包含标准),避免一次拉 8 个工具浪费 token。

### 步骤 3:并发调对应工具

**标准档示例**(默认):

```
mcp__longbridge__latest_financial_report(symbol=X)
mcp__longbridge__financial_report(symbol=X, kind="IS", period="qf")  # 单季利润表
mcp__longbridge__financial_report(symbol=X, kind="BS", period="qf")  # 单季资产负债表
mcp__longbridge__financial_report(symbol=X, kind="CF", period="qf")  # 单季现金流量表
mcp__longbridge__dividend(symbol=X)
mcp__longbridge__forecast_eps(symbol=X)
mcp__longbridge__consensus(symbol=X)
```

完整档再追加:`company`、`operating`、`corp_action`、`institution_rating`(可选)。

### 步骤 4:5 维输出(必填结构)

回答**必须**按以下 5 维组织——每维至少给 1 个数字 + 1 个同比/趋势/参照,某维数据缺失明示"暂未查到":

```
X (代码) 基本面快照(数据来源:长桥证券,披露期 fp_end / rpt_date)

【1. 盈利能力】
- 营收(最新季):¥X 亿,同比 +Y%
- 净利润:¥X 亿,同比 +Y%
- 毛利率 / 净利率:X% / Y%
- ROE:X%

【2. 财务健康】
- 资产负债率:X%
- 经营现金流(近 12M):¥X 亿
- 自由现金流:¥X 亿
- 流动比率 / 速动比率(若有)

【3. 增长】
- 近 4 季营收同比:+X% / +Y% / +Z% / +W%(看趋势)
- 近 4 季净利同比:同上

【4. 股东回报】
- 上次分红日期 + 金额
- 股息率:X%(若有)
- 近期回购 / 增发(corp_action,完整档才查)

【5. 市场预期(分析师)】
- 下季 EPS 一致预期:¥X
- 综合评级:N 家分析师覆盖,X 家买入 / X 家中性 / X 家卖出
- 目标价中位数:¥X

⚠️ 财报数据已发布即历史数据,未来业绩存在不确定性。本数据不构成投资建议。
```

### 步骤 5:chain 到其它 skill

| 用户后续问 | 路由到 |
|---|---|
| "X 估值贵不贵" | 「估值分析」(#14) |
| "X 跟 Y 业绩对比" | 「同行对比」(#16) |
| "X 财报后市场怎么看 / X 最近新闻" | 「资讯舆情」(#18) |
| "X 现在多少钱"(纯行情) | 「行情查询」(#01) |

## 中文术语映射(LLM 输出时翻译)

底层 MCP 字段是英文,LLM 输出必须翻译成中文:

| MCP 字段(常见) | 中文 |
|---|---|
| revenue / total_revenue | 营业收入 / 营收 |
| net_income | 净利润 |
| operating_income | 营业利润 |
| gross_margin | 毛利率 |
| net_margin | 净利率 |
| roe | 净资产收益率 ROE |
| roa | 总资产收益率 ROA |
| eps / eps_basic | 每股收益 EPS |
| bps / book_value | 每股净资产 BPS |
| dps / dividend_per_share | 每股分红 DPS |
| operating_cash_flow | 经营性现金流 |
| free_cash_flow | 自由现金流 |
| debt_to_equity / debt_ratio | 资产负债率 |
| current_ratio | 流动比率 |
| quick_ratio | 速动比率 |
| dividend_yield | 股息率 |
| fp_end / rpt_date | 报告期末 / 披露日 |

## 输出形态约束

- **必须**给 5 维(盈利 / 财务健康 / 增长 / 分红 / 预期),数据缺失明示
- **必须**所有比例 / 趋势数字带同比或绝对值参照
- **必须**注明披露日期(`fp_end / rpt_date`),让用户知道数据有多新
- **必须**末尾"不构成投资建议"
- **不要**给"业绩好 / 业绩差"的二元结论;允许说"营收增速 +20% 高于行业平均"这类**带数据锚的**判断
- **不要**预测下个季度业绩(让用户看 forecast_eps 的分析师一致预期就行)

## 行业差异提示

不同行业的"健康度"阈值差异极大,**不能用统一阈值套**:

- 银行 / 保险:资产负债率 90%+ 是常态(因为存款是负债);ROE 看 12-20% 是正常
- 科技 / 互联网:资产负债率 20-40% 常态;毛利率 60%+ 才算高
- 周期股(钢铁 / 化工 / 能源):净利率受行业景气度大幅波动,单季数据看不出长期趋势
- 重资产行业(航空 / 制造):自由现金流为负不一定是坏事(在投扩产)

LLM 输出时**用"vs 行业平均"或"vs 自身历史"参照,不用绝对阈值**。

## 错误处理

| 触发场景 | 用户侧话术 |
|---|---|
| MCP `longbridge` 未配置 | "本技能需要长桥 MCP,请先运行 `claude mcp add --transport http longbridge https://openapi.longbridge.com/mcp`。" |
| 调 MCP 返回 auth / unauthorized | "长桥授权过期,请重新触发授权。" |
| financial_report / latest_financial_report 返回空 | "{symbol} 暂无财报数据(可能是非主流标的或刚上市;新股上市后第一份财报披露前会查不到)。" |
| consensus / forecast_eps 覆盖稀疏(< 3 家分析师) | "{symbol} 分析师覆盖较少(N 家),市场预期数据仅供参考,不要把少数派中位数当强信号。" |
| dividend 工具返回空 | "{symbol} 暂无分红记录或不分红。" |

## MCP 工具速查

| MCP 工具名 | 拿什么 | 档位 |
|---|---|:---:|
| `mcp__longbridge__latest_financial_report` | 最新财报关键 KPI | 快照 |
| `mcp__longbridge__forecast_eps` | 未来 EPS 一致预期 | 快照 |
| `mcp__longbridge__consensus` | 分析师评级分布 + 目标价 | 快照 |
| `mcp__longbridge__financial_report` | IS / BS / CF 详细数据 | 标准 |
| `mcp__longbridge__dividend` | 分红历史 | 标准 |
| `mcp__longbridge__company` | 公司基本信息 | 完整 |
| `mcp__longbridge__operating` | 经营业绩(细分业务) | 完整 |
| `mcp__longbridge__corp_action` | 增发 / 回购 / 拆股 | 完整 |
| `mcp__longbridge__institution_rating` | 机构评级明细 | 完整 |

## 代码结构

```
基本面分析/
└── SKILL.md          # 本文件(prompt-only,无 cli.py)
```
