# Fundamentals: Financial Statements and Analysis

覆盖原技能：`longbridge-financial-report`, `longbridge-financial-analysis`, `longbridge-financial-checkup`, `longbridge-finance-query`, `longbridge-business-query`, `longbridge-operating`

---

## longbridge-financial-report — 完整三表

**触发场景**：利润表/资产负债表/现金流量表，可选季报/半年报/年报。

**数据类型**：完整三表 + 同比/环比变化；支持年度/半年度/季度周期

**核心分析（LLM内）**：
- **三表勾稽**：净利润(IS) ≈ 留存收益变化(BS)；净利润 + 非现金项目 ≈ 经营CF；ΔCash(CF) = ΔCash(BS)
- **杜邦分解**：ROE = 净利率 × 资产周转率 × 权益乘数
- **盈利质量**：应计比率 = (净利润 − 经营CF) / 平均总资产；正值越高→盈利越不踏实

---

## longbridge-financial-analysis — 深度财务分析

**触发场景**：DuPont 分解、应计质量、跨期财务健康趋势分析。

**分析维度**：
- 三表勾稽校验（识别财务造假信号）
- 分部收入占比与盈利贡献
- 营运资本效率（应收账款周转/库存周转天数）
- 现金转换周期

---

## longbridge-financial-checkup — 100分财务健康评分

**触发场景**：对公司进行系统性财务体检，输出 0–100 综合评分。

**五维度评分框架**（各20分）：
1. **盈利能力**：净利率/ROE/ROIC
2. **成长性**：营收增速/EPS增速
3. **财务稳健**：负债率/利息保障倍数/Altman Z-Score
4. **现金流质量**：经营CF/净利润比、自由现金流率
5. **估值合理性**：PE/PB/PS相对历史与行业

**输出格式**：
```
{symbol} 财务健康评分 — 来源：Longbridge Securities

总分：{X}/100  {优秀/良好/及格/警示}
- 盈利能力：{X}/20
- 成长性：{X}/20
- 财务稳健：{X}/20
- 现金流：{X}/20
- 估值合理性：{X}/20

主要优势：{1-2点}
主要风险：{1-2点}
```

---

## longbridge-finance-query — 跨市场财务指标批量查询

**触发场景**：同时查询多只股票的财务指标（营收/净利润/ROE/负债率等）。

**数据类型**：批量财务指标（支持多标的）；适合行业横向对比

---

## longbridge-business-query — 主营业务构成

**触发场景**：分部收入/毛利构成、核心产品线占比。

**数据类型**：业务分部收入、毛利率、增长贡献

---

## longbridge-operating — 季度/年度经营数据

**触发场景**：近N季度营收趋势、净利润/净利率/毛利率走势图数据。

**数据类型**：季度/年度经营数据时序（营收/净利润/利润率）
