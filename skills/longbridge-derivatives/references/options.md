# Derivatives: Options Basics, Strategy, and P&L

覆盖原技能：`longbridge-derivatives`, `longbridge-options-strategy`, `longbridge-options-pnl`

---

## longbridge-derivatives — 期权与窝轮基础报价

**触发场景**：美股/港股期权链报价、港股认购/认沽证/牛证/熊证列表。

**数据类型**：
- 期权链（到期日/行权价/认购/认沽/最新价/成交量/持仓量/隐含波动率）
- 港股窝轮/牛熊证（发行商/行权价/到期日/杠杆比率/溢价）

**工作流**：
1. `longbridge <derivatives-subcommand> --help` 确认期权链/窝轮子命令
2. 指定标的（如 `NVDA.US`）和到期日范围
3. 返回衍生品列表；可按行权价或到期日筛选

---

## longbridge-options-strategy — 期权策略设计

**触发场景**：设计期权策略（备兑/保护/价差/跨式/宽跨式/铁鹰/日历价差等）。

**策略类型与适用场景**：

| 策略 | 适用场景 |
|---|---|
| 备兑开仓（Covered Call） | 持股增收，中性偏空 |
| 保护性认沽（Protective Put） | 持股对冲下行风险 |
| 领口策略（Collar） | 低成本对冲 |
| 牛市价差（Bull Call Spread） | 看涨但限制成本 |
| 熊市价差（Bear Put Spread） | 看跌但限制成本 |
| 跨式（Straddle） | 预期大幅波动，方向不确定 |
| 宽跨式（Strangle） | 同上，成本更低 |
| 铁鹰（Iron Condor） | 低波动率环境，收取权利金 |

**工作流**：
1. 获取当前标的价格和期权链数据
2. 根据用户意图选择策略类型
3. 构建策略参数（行权价/到期日/张数）
4. 计算并展示盈亏结构（需调用 P&L 分析）

---

## longbridge-options-pnl — 期权P&L分析

**触发场景**：期权盈亏图、盈亏平衡点、最大盈利/亏损、Greeks 快览。

**分析内容**：
- 到期盈亏图（payoff diagram）
- 盈亏平衡点（break-even）
- 最大盈利/最大亏损
- Delta/Gamma/Vega/Theta 快览

**计算方法**（LLM内计算）：
- 认购期权到期P&L = max(0, 正股价格 - 行权价) - 权利金
- 认沽期权到期P&L = max(0, 行权价 - 正股价格) - 权利金
- 组合策略叠加每条腿的P&L

**输出格式**：
```
策略：{名称}
标的：{symbol} @ {current_price}
腿：{方向 买/卖} {数量}张 {到期日} {行权价} {认购/认沽} @ {权利金}

盈亏平衡点：{价位}
最大盈利：{金额 或 无限}
最大亏损：{金额}

⚠️ 以上分析仅供参考，不构成投资建议。
```
