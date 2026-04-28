# 同行对比(skill #16)— 差异化设计

**Date:** 2026-04-28
**Status:** Draft(analysis-tier,prompt-only,**强依赖 MCP**)
**Protocol:** 偏离同 #14

## 业务范围

回答 **"X 和 Y 谁更值得买 / 哪个贵 / 哪个增速快"** 这一类**多 symbol 横向对比**问题。

这是 skill 最大的价值场景——单 MCP 工具一次只查一个 symbol,LLM 调 10 个工具拼对比表很容易丢字段、忘归一化。本 skill 就是**多 symbol orchestration 的标准化**。

- 编排:对每个 symbol 并发调一组工具,聚合成对比表
- 不做:不挑出"赢家",给数据矩阵让用户自己选;**不超过 5 个 symbol**(再多对话不易读)

## front-matter

```yaml
---
name: 同行对比
description: 横向对比 2-5 只股票——估值(PE/PB/PS)+ 当前涨跌 + 最新业绩 + 市值规模 + 分红率,生成数据矩阵。当用户询问 X 和 Y 哪个值得买 / 哪个贵 / 哪个增速快 / 几只股票对比 / 同行业谁最强等场景必须使用此技能。返回数据,不构成投资建议。
license: Complete terms in LICENSE.txt
version: 1.0.0
risk_level: read_only
requires_login: false
default_install: true
requires_mcp: true
---
```

## 工具编排逻辑

对**每个** symbol 并发调:

| 工具 | 拿什么 |
|---|---|
| `mcp__longbridge__quote` | 当前价、涨跌幅、成交量、币种 |
| `mcp__longbridge__calc_indexes`(参数 `pe,pb,ps,dividend_yield,total_market_value,turnover_rate`) | 当前估值快照 |
| `mcp__longbridge__latest_financial_report` | 营收 / 净利同比、ROE |
| `mcp__longbridge__valuation` | 完整估值(交叉验证 calc_indexes)|

**不调** financial_report (IS/BS/CF) 完整三表——多 symbol 时数据爆炸,只取 latest_financial_report 的 KPI 就够。

## SKILL.md 核心步骤

### 步骤 1:解析多个 symbol(2-5 个)

用户问句里抽出股票名 / ticker,补全 `<CODE>.<MARKET>`(同行情查询规则)。

**保护**:
- 0 个 symbol → 反问"想对比哪几只?"
- 1 个 symbol → 改路由到「估值分析」(#14)或「基本面分析」(#15),不在本 skill 跑
- ≥ 6 个 symbol → 反问用户"对比 6 只以上数据矩阵不易读,挑核心 3-5 只如何?"

### 步骤 2:对每个 symbol 并发拉数据

```
并发对每个 symbol 调:
  mcp__longbridge__quote(symbol=X)
  mcp__longbridge__calc_indexes(symbol=X, indexes="pe,pb,ps,dividend_yield,total_market_value,turnover_rate")
  mcp__longbridge__latest_financial_report(symbol=X)
  mcp__longbridge__valuation(symbol=X)
```

### 步骤 3:归一化 + 对比表

LLM 必须把不同币种的数据**注明币种**(不强行换算,因为汇率引入误差;让用户看数字 + 货币标签)。

输出模板:

```
| 维度 | 茅台 (600519.SH) | 五粮液 (000858.SZ) | 泸州老窖 (000568.SZ) |
|---|---|---|---|
| 当前价 (CNY) | 1450.20 | 156.30 | 165.40 |
| 今日涨跌 | +1.2% | -0.5% | +0.8% |
| 总市值 | 1.82 万亿 | 6068 亿 | 2434 亿 |
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
- 估值:茅台 PE/PB/PS 三项都最贵
- 增长:茅台营收和净利同比领先
- 分红率:五粮液最高
- 规模:茅台市值约为五粮液 3 倍

⚠️ 估值 + 增长不能直接定结论;高估值通常对应更高确定性 / 品牌溢价。本数据不构成投资建议,请结合自身风险偏好判断。
数据来源:长桥证券
```

### 步骤 4:绝对禁止

- 不输出"我推荐 X"或"X 更值得买"
- 不基于以上数据给"应该买 X 不应该买 Y"建议
- 综合观察段只能讲**数据呈现的事实**(谁高谁低 / 趋势谁强),不能下结论

### 步骤 5:chain 到其它 skill

- 用户对某只感兴趣,问详情 → 路由到「估值分析」(#14)或「基本面分析」(#15),传该 symbol
- 用户问"哪个最近资金流入多" → 把每只都调资金流向 skill,然后回答(本 skill 默认不带资金面,但可临时拓展)

## 输出形态约束

- **必须**用 markdown 表格,行=维度,列=symbol
- **必须**注明每个数字的货币(CNY / USD / HKD / SGD)
- **必须**末尾"综合观察"用纯数据描述,不下结论
- **必须**末尾"不构成投资建议"
- **不要**自动汇率换算(不同币种保留原币 + 标签)

## 验收清单

- [ ] 问"茅台 五粮液 泸州老窖 哪个最便宜",LLM 对 3 个 symbol 并发调上述工具,生成对比表
- [ ] 表格表头 / 表行齐整,每数字有货币标签
- [ ] 综合观察纯数据描述,不出现"推荐 / 我建议 / 更值得买"
- [ ] 末尾"不构成投资建议"
- [ ] 问"GOOG 跟 5 个其它科技股对比",LLM 反问"挑 3-5 只就好"
- [ ] 问"NVDA 跟茅台谁好"(跨币种 + 跨行业),LLM **必须**警告"跨行业 / 跨币种对比意义有限",仍出表但加强 disclaimer

## 已知 trade-off

- 跨币种 + 跨行业对比意义不大但用户有时会问 → SKILL.md 让 LLM 在表格上方加一段 disclaimer,数据照给但**强烈提示**对比有局限
- 不同财报口径(IFRS / US GAAP / 中国会计准则)的数字不严格可比 → SKILL.md 让 LLM 在跨市场对比时注明这一点
- "ROE" 等比率在不同市场计算口径略不同(摊薄 vs 加权),作为粗略对比足够,作为精细分析需用户去查原报表
