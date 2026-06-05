# Fundamentals: Core KPIs, Ownership, and Business Segments

覆盖原技能：`longbridge-fundamental`, `longbridge-ownership`

---

## longbridge-fundamental — 最新财报 KPI 快览

**触发场景**：快速获取公司最新财报核心指标（营收/净利润/EPS/ROE/ROIC/利润率）。

**数据类型**：
- 最新季度/年度：营收/净利润/毛利率/净利率/经营利润率
- ROE（净资产收益率）、ROIC（投入资本回报率）
- EPS（基本/摊薄）、分红情况
- 分析师共识（当前EPS预测/目标价/评级）

**输出格式**：
```
{symbol} 基本面快览 — 来源：Longbridge Securities

最新财务数据（{期间}）：
- 营收：{X}（YoY {±Y%}）
- 净利润：{X}（YoY {±Y%}）
- 毛利率：{X}% | 净利率：{X}%
- EPS：{X} | ROE：{X}%

估值：PE {X}x | PB {X}x | PS {X}x
分析师：{X}买入/{Y}持有/{Z}卖出 | 平均目标价 ${X}

⚠️ 以上数据仅供参考，不构成投资建议。
```

**工作流**：
1. `longbridge <financial-report-subcommand> SYMBOL --latest --format json`
2. 同时获取估值指数和分析师共识数据
3. 合并输出 KPI 快览

---

## longbridge-ownership — 股权结构与主要股东

**触发场景**：大股东持仓、机构持仓比例、前十大股东。

**数据类型**：
- 股本结构（总股本/流通股/限售股/回购库存股）
- 前十大股东（持股比例/性质：创始人/机构/指数基金）
- 机构持仓比例（占流通股比例）

**关键解读**：
- 创始人/管理层高持仓 → 利益对齐，正面
- 机构持仓集中度高 → 流动性风险（同时减仓可能造成大幅波动）
- 限售股解禁 → 关注解禁日期和解禁规模（潜在抛压）

**工作流**：`longbridge <ownership-subcommand> SYMBOL --format json`
