# Fundamentals: Valuation

覆盖原技能：`longbridge-valuation`, `longbridge-valuation-rank`, `longbridge-valuation-methodology`, `longbridge-dcf`, `longbridge-peer-comparison`, `longbridge-industry-valuation`

---

## longbridge-valuation — 当前估值快照

**触发场景**："贵不贵"、PE/PB/PS/EV-EBITDA 当前值 + 历史百分位。

**数据类型**：当前 PE TTM/PB/PS/EV-EBITDA + 5年历史百分位 + 行业均值对比

**工作流**：
1. `longbridge <valuation-subcommand> SYMBOL --format json`
2. 展示当前值 + 历史分位（高分位=贵，低分位=便宜）
3. 与行业中位数对比

---

## longbridge-valuation-rank — 估值历史分位时序

**触发场景**：估值历史分位的时间序列走势（PE band 图数据）。

**数据类型**：日频 PE/PB/PS 历史百分位时序（近1年/3年/5年）

**用途**：绘制 PE band 图；判断现在是贵还是便宜

---

## longbridge-valuation-methodology — 估值方法论

**触发场景**：解释各类估值方法，帮助用户理解如何给公司估值。

**方法论框架**：

| 方法 | 适用场景 |
|---|---|
| PE/PB/PS | 相对估值，行业横向比较 |
| EV/EBITDA | 资本密集型行业、杠杆不同的公司比较 |
| DCF | 现金流稳定的成熟公司 |
| DDM（股息折现） | 高股息成熟公司 |
| SOTP（分部加总） | 多元化业务集团 |
| PEG | 高成长股（PE/EPS增长率） |

---

## longbridge-dcf — DCF 自由现金流折现估值

**触发场景**：对公司进行 DCF 估值，计算内在价值。

**DCF 框架**（5步）：
1. 获取历史 FCF（近3-5年）：`FCF = 经营CF - 资本支出`
2. 预测未来 5-10 年 FCF（高/中/低三情景）
3. 确定折现率（WACC：加权平均资本成本）
4. 计算终值（Gordon增长模型）
5. 内在价值 = Σ(FCF_t / (1+WACC)^t) + 终值/(1+WACC)^n

**输出**：高/中/低三情景内在价值区间 + 当前股价对应的安全边际

---

## longbridge-peer-comparison — 同行横向对比

**触发场景**：2–5 只股票的多维横向比较（估值/盈利/成长/分红）。

**对比维度**：PE/PB/PS/股息率/ROE/净利率/营收增速/EPS增速

---

## longbridge-industry-valuation — 行业估值分布

**触发场景**：某行业内所有股票的估值分布、行业 PE/PB 中位数/分位数。

**数据类型**：行业估值分布矩阵（PE/PB/PS/股息率的最小值/中位数/最大值）
