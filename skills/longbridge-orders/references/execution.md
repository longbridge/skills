# Orders: Execution Model and Market Microstructure

覆盖原技能：`longbridge-execution-model`, `longbridge-market-microstructure`

---

## longbridge-execution-model — 交易执行模型分析

**触发场景**：_"分析这笔交易的执行质量"_、_"滑点分析"_、_"回测执行模型"_

**核心概念**：

1. **滑点（Slippage）**
   - 实际成交价 vs 决策时市价的差异
   - 滑点 = (成交价 - 决策时市价) / 决策时市价 × 100%
   - 买入正滑点=超额成本；卖出负滑点=执行损耗

2. **市场冲击（Market Impact）**
   - 大单拆分策略：VWAP/TWAP/POV（量占比）
   - 市场冲击成本 ≈ √(订单量 / 日均成交量) × 波动率 × 系数

3. **执行策略对比**：
   | 策略 | 适用场景 | 特点 |
   |---|---|---|
   | 市价单（Market） | 小单/流动性好 | 快速成交，滑点不确定 |
   | 限价单（Limit） | 精确价格 | 可能未成交 |
   | VWAP | 大单执行 | 减少市场冲击 |
   | TWAP | 时间均匀分配 | 简单，适合中等流动性 |

**工作流**：
1. 获取历史成交记录（`longbridge-orders`）
2. 获取执行时间点的盘口数据（`longbridge-market-data`）
3. 计算实际滑点；与理论最优执行对比

---

## longbridge-market-microstructure — 市场微观结构分析

**触发场景**：_"这只股票买卖价差大吗"_、_"订单流分析"_、_"价格发现"_

**核心指标**：

1. **买卖价差（Bid-Ask Spread）**
   - 相对价差 = (卖一价 - 买一价) / 中间价
   - 相对价差越小 → 流动性越好 → 交易成本越低

2. **订单流毒性（Order Flow Toxicity）**
   - 用于识别知情交易者（内幕）vs 噪音交易者
   - VPIN = |净买入量| / 总成交量（高VPIN = 知情交易者活跃）

3. **价格冲击函数（Price Impact）**
   - λ = ΔPrice / ΔVolume（单位成交量对价格的影响）
   - λ 大 → 流动性差，大单容易冲击价格

**工作流**：
1. 获取盘口深度数据（`longbridge-market-data`，depth 子模块）
2. 获取逐笔成交数据
3. 计算实时买卖价差和订单流指标
