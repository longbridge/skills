# Quant: Strategy Tools

覆盖原技能：`longbridge-quant`, `longbridge-quant-stats`, `longbridge-seasonality`, `longbridge-correlation`, `longbridge-pairs-trading`

---

## longbridge-quant — 服务端量化指标运行器

**触发场景**：_"运行Pine Script指标"_、_"服务端量化分析"_

**功能**：在 Longbridge 服务端执行 Pine Script v6 语法子集，返回历史指标值

**工作流**：
1. `longbridge <quant-subcommand> SYMBOL --format json`
2. 指定 Pine Script 代码（符合 Longbridge 支持的语法子集）
3. 返回指标时序数据供 LLM 分析

---

## longbridge-quant-stats — 时序统计分析

**触发场景**：_"这只股票价格序列是平稳的吗"_、_"协整检验"_

**统计检验**：

1. **ADF 单位根检验**（平稳性）
   - H0：序列有单位根（不平稳）
   - p < 0.05 → 拒绝H0 → 平稳（适合均值回归策略）

2. **协整检验**（配对交易基础）
   - 两个非平稳序列的线性组合平稳 → 协整关系存在
   - p < 0.05 → 存在协整关系 → 可以配对交易

3. **半衰期（Half-life）**
   - 价差回归到均值所需时间
   - 半衰期越短 → 均值回归越快 → 策略交易机会更多

4. **自相关（ACF/PACF）**
   - 用于识别序列的 AR/MA 结构

---

## longbridge-seasonality — 季节性策略

**触发场景**：_"这只股票有季节性吗"_、_"一月效应"_

**分析框架**：
- 月度季节性：计算各月平均收益率（近5-10年）
- 节假日效应：节前/节后N日平均表现
- 财报季效应：财报前后N日平均波动

**输出**：季节性热图 + 统计显著性（t检验）

---

## longbridge-correlation — 多资产相关性分析

**触发场景**：_"NVDA和AMD的相关性"_、_"组合相关性矩阵"_

**分析方法**：
- Pearson 相关系数（线性相关）
- Spearman 相关系数（非线性/秩相关）
- 滚动相关性（N日窗口，识别相关性变化）

**解读**：相关系数 > 0.8 = 高度相关；< 0.3 = 低相关（好的分散化）

---

## longbridge-pairs-trading — 配对交易/统计套利

**触发场景**：_"NVDA和AMD可以配对交易吗"_、_"统计套利"_

**操作流程**：
1. 协整检验（`quant-stats`）+ 相关性确认
2. 计算对冲比率：β = Cov(A,B) / Var(B)
3. 价差 = 价格A - β × 价格B
4. 价差均值回归交易信号：
   - 价差 > 均值+2σ → 卖出A，买入B（做空价差）
   - 价差 < 均值-2σ → 买入A，卖出B（做多价差）
5. 止损：价差超过均值±3σ 时止损
