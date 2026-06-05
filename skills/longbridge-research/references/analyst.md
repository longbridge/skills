# Research: Analyst Research and Stock Snapshots

覆盖原技能：`longbridge-insresearch`, `longbridge-consensus`, `longbridge-analyst-estimates`, `longbridge-stock-research`

---

## longbridge-insresearch — 机构研报与分析师评级

**触发场景**：查看机构评级分布、研报摘要、分析师最新观点。

**数据类型**：
- 买入/持有/卖出评级分布（家数/百分比）
- 最新研报标题/机构/日期/摘要
- 综合推荐强度（加权评级 1-5 分）

**工作流**：`longbridge <insresearch-subcommand> SYMBOL --format json`

---

## longbridge-consensus — 分析师共识快照

**触发场景**：当前 EPS/营收共识预测、目标价共识、评级分布快照。

**数据类型**：
- 未来1-2年 EPS 共识（高/低/均值/中位数，修订趋势）
- 未来1-2年营收共识
- 目标价共识（高/低/均值）+ 当前价格隐含上涨空间
- 评级分布（强买入/买入/持有/卖出/强卖出）

**解读规则**：
- 共识目标价 > 当前价15%+ → 分析师整体看好
- 评级从买入向持有迁移 → 关注下行风险
- EPS 持续上修 → 业绩动量正向

---

## longbridge-analyst-estimates — EPS 预测时序追踪

**触发场景**：分析师 EPS 预测随时间的演变轨迹（修订历史）。

**数据类型**：季度/年度 EPS 预测时序（近N个月的均值变化）

**用途**：识别 EPS 修订趋势（持续上修/下修 = 分析师情绪变化的领先信号）

---

## longbridge-stock-research — 综合研究快照

**触发场景**：生成一份融合机构研报/基本面/技术面/资金流向的综合研究摘要。

**报告结构**：
1. 公司概述（业务/行业/竞争地位）
2. 最新财务 KPI（参见 fundamentals/core-data.md）
3. 估值（PE/PB 历史百分位）
4. 分析师共识（评级/目标价/最新观点）
5. 技术面信号（近期价格趋势/关键支撑阻力）
6. 近期催化剂与风险点
7. 综合结论（多空因素对比）

**工作流**：并行获取基本面/共识/行情数据；LLM 整合输出
