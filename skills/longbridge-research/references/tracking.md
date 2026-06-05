# Research: Post-Investment Tracking and Filing Analysis

覆盖原技能：`longbridge-post-investment`, `longbridge-thesis-tracker`, `longbridge-sec-filings`, `longbridge-etf-analysis`

---

## longbridge-post-investment — 投后跟踪监控

**触发场景**：持有股票后的季度复盘，确认投资逻辑是否仍然成立。

**季度复盘框架**：
1. **业绩对比**：实际营收/EPS vs 入场时的预期
2. **逻辑验证**：当初的投资假设（增速/利润率/护城河）是否兑现
3. **估值变化**：当前估值 vs 买入时估值（是否更贵/更便宜）
4. **风险事项**：新出现的竞争对手/监管/管理层变化
5. **持有/止损决策**：逻辑未受损→持有；逻辑受损→重新评估

---

## longbridge-thesis-tracker — 投资逻辑追踪器

**触发场景**：持续维护和更新持仓或自选股的投资论点。

**追踪维度**：
- 核心假设（3-5条）+ 验证状态（成立/待验证/已证伪）
- 关键里程碑（产品发布/季报/市场份额）
- 逻辑完整性评分（满分100，下降到80以下触发复盘）

---

## longbridge-sec-filings — SEC EDGAR 文件分析

**触发场景**：分析美股公司的 10-K/10-Q/8-K/代理声明/内部人交易披露。

**文件类型与要点**：

| 文件 | 频率 | 关键读取要点 |
|---|---|---|
| 10-K | 年度 | 业务描述/风险因素/MD&A/审计意见 |
| 10-Q | 季度 | 最新财务数据/管理层讨论 |
| 8-K | 不定期 | 重大事件（并购/CEO变更/财报） |
| DEF 14A（Proxy） | 年度 | 管理层薪酬/关联交易/股东提案 |
| Form 4 | 内部人交易 | CEO/CFO/董事增持/减持记录 |

**工作流**：
1. `longbridge <sec-filing-subcommand> SYMBOL --format json`
2. 根据用户需要定位关键章节（风险因素/MD&A/财务报表）
3. 重点提取：forward-looking statements/重大不确定性/内部人立场

---

## longbridge-etf-analysis — ETF 分析

**触发场景**：_"哪个ETF更适合"_、_"比较跟踪误差"_、_"ETF流动性分析"_

**分析维度**：
1. **产品筛选**：按规模（AUM）/费率（expense ratio）/跟踪指数筛选
2. **跟踪误差**：ETF价格 vs 净值（NAV）差异；溢价/折价情况
3. **流动性**：日均成交量/买卖价差（Bid-Ask Spread）
4. **成分股集中度**：前10大持仓占比

**推荐逻辑**：低费率 + 低跟踪误差 + 流动性充足 = 优选 ETF
