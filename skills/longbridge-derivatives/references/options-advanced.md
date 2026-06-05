# Derivatives: Advanced Options and Volatility

覆盖原技能：`longbridge-options-volatility`, `longbridge-options-advanced`

---

## longbridge-options-volatility — 隐含波动率分析

**触发场景**：IV 水平、IV Rank/百分位、波动率期限结构、偏斜（Skew）。

**核心概念**：
- **隐含波动率（IV）**：从期权价格反推的市场预期波动率
- **IV Rank**：当前 IV 在近1年历史范围中的百分位（高=贵，低=便宜）
- **期限结构**：不同到期日的 IV 对比（正常曲线 vs 倒挂）
- **波动率偏斜（Skew）**：虚值认沽 vs 虚值认购 IV 差异

**工作流**：
1. 获取期权链数据（多个到期日）
2. 提取各到期日的隐含波动率
3. 与历史波动率（HV）对比（需获取历史K线计算）
4. 输出：IV Rank 判断（高/中/低）+ 策略倾向（IV高→卖方策略；IV低→买方策略）

**输出示例**：
```
{symbol} 波动率分析 — 数据来源：Longbridge Securities
当前 IV（30日到期）：{X}%
历史波动率（HV-20）：{Y}%
IV Rank（近1年）：{Z}%（{低/中/高}）
期限结构：{正常/倒挂/平坦}
波动率偏斜：认沽 IV {>/<} 认购 IV {X}%

策略倾向：IV Rank {高→适合卖方；低→适合买方}
```

---

## longbridge-options-advanced — 高阶期权分析

**触发场景**：波动率曲面、SABR/局部波动率模型、隐含波动率 Smile、期权定价模型。

**分析框架**：

1. **波动率曲面（Vol Surface）**
   - 维度：到期日 × 行权价
   - 通过期权链数据构建 IV 网格，呈现曲面形态
   - 识别异常定价区域（套利信号）

2. **波动率偏斜动态**
   - 25Delta Put Skew（风险逆转）
   - Butterfly（蝴蝶）：中部 vs 两翼 IV
   - 解读：负偏斜（Put IV > Call IV）→ 市场保护需求强

3. **模型框架**（概念性，LLM内解释）
   - Black-Scholes：基础定价，假设恒定波动率
   - SABR：随机波动率，能捕捉偏斜
   - 局部波动率：确定性波动率函数，拟合曲面

**工作流**：
1. 获取全期权链（多个到期日+多行权价）
2. 构建 IV 网格；识别曲面异常
3. 结合用户策略目标给出建议
