# Fundamentals: Earnings Tracking

覆盖原技能：`longbridge-earnings`, `longbridge-earnings-preview`, `longbridge-earnings-revision`, `longbridge-calendar`, `longbridge-corporate-events`

---

## longbridge-earnings — 业绩发布后深度分析

**触发场景**：财报发布后生成机构级深度分析报告（可含 DOCX 输出）。

**分析框架**（8-12页报告结构）：
1. 业绩摘要：实际 vs 预期（EPS beat/miss）
2. 核心指标：营收/净利润/毛利率/经营利润 YoY
3. 分部分析：各业务线增长拆解
4. 现金流质量：经营CF vs 净利润
5. 管理层指引：下季度/全年展望
6. 业绩催化剂与风险点
7. 估值更新：基于新数据调整目标价

**DOCX 生成**（如需）：调用 `scripts/generate_report.py`（如存在）；否则输出 Markdown 格式

---

## longbridge-earnings-preview — 财报前预期分析

**触发场景**：财报发布前，分析市场预期和潜在超预期/低于预期风险。

**分析框架**：
1. 分析师共识（EPS/营收高中低预测）
2. 历史超预期/不及预期频率
3. 公司此前指引 vs 共识
4. 关键跟踪指标（月活/GMV/订单量等业务数据）
5. 期权市场隐含波动预期（隐含涨跌幅）
6. 管理层可信度评分

---

## longbridge-earnings-revision — 盈利预测修订追踪

**触发场景**：追踪分析师 EPS 预测的修订趋势（上调/下调）。

**数据类型**：共识 EPS 预测时序（高/低/均值/中位数），过去3/6/12个月修订方向

**解读原则**：持续上修→动量正向；持续下修→信号转弱；分歧扩大→不确定性上升

---

## longbridge-calendar — 财务日历

**触发场景**：财报日期/业绩发布日/分红日/股东大会/债券到期等财务事件。

**数据类型**：公司财务日历（财报日/派息日/权益登记日/股东会等）

**工作流**：`longbridge <calendar-subcommand> SYMBOL --format json`

---

## longbridge-corporate-events — 公司事件驱动分析

**触发场景**：M&A（并购/被收购）/回购/增发/分拆/股息特别派发等事件影响分析。

**事件类型**：
| 事件 | 典型影响 |
|---|---|
| 并购（买方） | 短期支付溢价→股价承压；长期看协同效应 |
| 并购（被收购方） | 通常溢价收购→正面 |
| 股票回购 | 减少流通股→EPS 提升，正面信号 |
| 增发（稀释） | 股权稀释→负面（除非用于高回报投资） |
| 分拆 | 聚焦主业→通常中长期正面 |
| 特别股息 | 一次性正面；但可能意味着缺乏再投资机会 |
