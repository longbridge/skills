# Derivatives: Cross-Market Arbitrage and Premiums

覆盖原技能：`longbridge-fx-carry`, `longbridge-adr-premium`, `longbridge-ah-premium`

---

## longbridge-fx-carry — 外汇套利（Carry Trade）

**触发场景**：FX 利差分析、carry trade 策略、远期溢价/折价。

**核心概念**：
- **Carry Trade**：借入低息货币（如 JPY/CHF），买入高息货币（如 AUD/BRL）
- **利率平价（IRP）**：远期汇率 = 即期汇率 × (1 + 高息货币利率) / (1 + 低息货币利率)
- **远期溢价/折价**：高息货币的远期价格低于即期价格（隐含利差）

**分析框架**：
1. 获取目标货币对即期汇率（`longbridge-market-data` FX）
2. 获取两国基准利率（可用 WebSearch 补充，标注来源）
3. 计算 carry 收益率 = 利率差 - 汇率风险调整
4. 输出：carry 收益率排名 + 历史波动率风险 + 推荐与否

---

## longbridge-adr-premium — ADR/H股/A股跨市溢价

**触发场景**：美股 ADR 与港股/A股的跨市定价差异分析。

**核心概念**：
- **ADR 溢价** = (ADR价格 × 换算比例 × 汇率 - H股/A股价格) / H股/A股价格 × 100%
- 正溢价→ ADR 更贵；负溢价→ ADR 折价（理论上存在套利空间，但受流动性/交易成本限制）

**分析框架**：
1. 获取 ADR 报价（如 `BABA.US`、`NIO.US`）
2. 获取对应 H股（如 `9988.HK`、`9866.HK`）或 A股报价
3. 获取 USD/HKD 或 USD/CNY 汇率
4. 计算溢价率；解读套利可行性

---

## longbridge-ah-premium — A/H股溢价

**触发场景**：A股（沪深）与 H股（港股）的同一公司双重上市溢价分析。

**核心概念**：
- **A-H 溢价** = (A股价格 / H股价格 × CNY/HKD) - 1，以百分比表示
- A-H 溢价指数：一篮子 A+H 双重上市公司的平均溢价
- 高溢价 → A股贵；低溢价（折价）→ H股机会

**分析框架**：
1. 获取目标公司 A股（如 `601398.SH`）和 H股（如 `1398.HK`）报价
2. 获取 CNY/HKD 汇率
3. 计算当前溢价率；与历史均值对比
4. 输出：当前溢价率 + 历史分位 + 相对价值判断

**常见双重上市参考**：工商银行（601398.SH / 1398.HK）、建设银行（601939.SH / 939.HK）、小米集团（A股暂无 / 1810.HK）等；运行时从 Longbridge 数据获取实际报价。
