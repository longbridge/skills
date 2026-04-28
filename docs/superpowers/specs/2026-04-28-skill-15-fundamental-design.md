# 基本面分析(skill #15)— 差异化设计

**Date:** 2026-04-28
**Status:** Draft(analysis-tier,prompt-only,**强依赖 MCP**)
**Protocol:** 遵循 `2026-04-28-skill-platform-protocol.md`,偏离同 #14(无 cli.py、强依赖 MCP)

## 业务范围

回答 **"X 公司基本面怎么样 / 业绩如何 / 财务健康吗"** 这一类问题。

中文用户的"基本面"通常指三件事:**业绩(IS)** + **财务健康(BS / CF)** + **股东回报(分红 / 回购)**。本 skill 必须三块齐全,不能只看 PE。

- 编排的 MCP 工具:`financial_report`、`latest_financial_report`、`dividend`、`forecast_eps`、`consensus`、`company`、`operating`、`corp_action`、`institution_rating`(可选)
- chain 到的现有 skill:无(基本面是公司级别问题,不需要再调行情)
- 不做:**不给"业绩好不好"的主观结论**(给数字 + 同比 + 行业排名,让用户自己判断);不做财报预测(LLM 不该预测)

## front-matter

```yaml
---
name: 基本面分析
description: 综合分析公司基本面——最新财报关键 KPI(营收 / 净利 / EPS / ROE / 毛利率 / 现金流)、同比变化、分红历史、未来 EPS 一致预期、机构评级、股本与公司基本信息。当用户询问 X 基本面 / 业绩 / 财报 / 财务健康 / 分红 / EPS 预期 / 研报评级等场景必须使用此技能。返回数据,不构成投资建议。
license: Complete terms in LICENSE.txt
version: 1.0.0
risk_level: read_only
requires_login: false
default_install: true
requires_mcp: true
---
```

## 工具编排逻辑

收到基本面问句后,LLM 决定**深度档位**:

| 用户语义 | 调用档位 | 工具集 |
|---|---|---|
| 简版("X 怎么样") | 快照 | `latest_financial_report` + `forecast_eps` + `consensus` |
| 标准("X 基本面 / 业绩") | 标准 | + `financial_report` (IS/BS/CF latest period) + `dividend` (recent) |
| 全景("X 全面分析 / 详细财报") | 完整 | + `company` + `operating` + `corp_action` + `institution_rating` |

只在需要时上更深的档,避免一次拉 8 个工具浪费 token。

## SKILL.md 核心步骤

### 步骤 1:识别 symbol(同行情查询规则)

### 步骤 2:估算档位

按用户问句关键词:
- "怎么样 / 简单看一下" → 快照档
- "基本面 / 业绩 / 财报" → 标准档(默认)
- "全面 / 详细 / 全景" → 完整档

### 步骤 3:调对应工具(并发)

举例标准档:
```
mcp__longbridge__latest_financial_report(symbol=X)
mcp__longbridge__financial_report(symbol=X, kind="IS", period="qf")  # 单季报
mcp__longbridge__financial_report(symbol=X, kind="BS", period="qf")
mcp__longbridge__financial_report(symbol=X, kind="CF", period="qf")
mcp__longbridge__dividend(symbol=X)
mcp__longbridge__forecast_eps(symbol=X)
mcp__longbridge__consensus(symbol=X)
```

### 步骤 4:5 维输出

回答必须按以下 5 个维度组织(每维至少给 1 个数字 + 1 个同比/趋势):

```
X 基本面快照(数据来源:长桥证券)

【1. 盈利能力】
- 营收(最新季):¥X亿,同比 +Y%
- 净利润:¥X亿,同比 +Y%
- 毛利率 / 净利率:X%
- ROE:X%

【2. 财务健康】
- 资产负债率:X%
- 经营现金流(近 12M):¥X亿
- 自由现金流:¥X亿
- 速动比率(若有)

【3. 增长】
- 近 4 季营收同比:+X% / +Y% / +Z% / +W%(看趋势)
- 近 4 季净利同比:同上

【4. 股东回报】
- 上次分红日期 + 金额
- 股息率:X%(若有)
- 近期回购 / 增发(corp_action)

【5. 市场预期(分析师)】
- 下季 EPS 一致预期:¥X
- 综合评级:N 家分析师覆盖,X 家买入 / X 家中性 / X 家卖出
- 目标价中位数:¥X

⚠️ 财报数据已发布即历史数据,未来业绩存在不确定性。本数据不构成投资建议。
```

### 步骤 5:chain 到其它 skill(必要时)

- 用户接着问估值 → 路由到「估值分析」skill(#14)
- 用户问业绩 vs 同行 → 路由到「同行对比」skill(#16)
- 用户问最近新闻 / 财报后市场反应 → 路由到「资讯舆情」skill(#18)

## 输出形态约束(SKILL.md 强制)

- **必须**给 5 维(盈利 / 财务健康 / 增长 / 分红 / 预期),哪一维数据缺失明确说"暂未查到"
- **必须**所有比例 / 趋势数字带同比或绝对值参照
- **必须**末尾"不构成投资建议"
- **不要**给"业绩好 / 业绩差"的二元结论;允许说"营收增速 +20% 高于行业平均"这类**带数据锚的**判断
- **不要**预测下个季度业绩(让用户看 forecast_eps 的分析师一致预期就行)

## 中文术语映射(必须在 SKILL.md 里教 LLM)

底层 MCP 返回的字段名是英文,LLM 输出时翻译:

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

## 验收清单

- [ ] 问"贵州茅台 基本面",LLM 调 latest_financial_report + financial_report (IS/BS/CF) + dividend + consensus
- [ ] 回答含 5 维(各维数字齐全;若数据缺失明示)
- [ ] 末尾"不构成投资建议"
- [ ] 问"NVDA 业绩好不好",LLM 不直接说"好/不好",改给数字对比
- [ ] 问"X 跟 Y 业绩对比" → 路由到 #16
- [ ] 问"X 估值在历史什么位置" → 路由到 #14

## 已知 trade-off

- A 股 / 港股 / 美股的财报披露节奏不同,数据可能滞后(美股季度 / 港股半年 / A 股季度但披露慢)→ SKILL.md 让 LLM 在回答时**注明披露日期**(`fp_end / rpt_date`),用户知道数据有多新
- 行业差异极大(银行的资产负债率 95% 是常态,科技公司 30% 才是常态),五维"健康度"不能用统一阈值套 → SKILL.md 让 LLM 用"vs 行业平均"或"vs 自身历史"参照,不用绝对阈值
- 中小盘股的"市场预期"(forecast_eps / consensus)可能稀疏(3 家以下分析师覆盖)→ 此时 LLM 标注"覆盖较少",不要把 3 个人的中位数当强信号
- corp_action 数据(增发 / 回购 / 分红再投资)字段差异大,LLM 在解析时要 robust(字段缺失时降级)
