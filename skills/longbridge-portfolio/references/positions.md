# Portfolio: Positions, Account Overview, and Statements

覆盖原技能：`longbridge-portfolio`, `longbridge-positions`, `longbridge-statement`

---

## longbridge-portfolio — 账户全貌与损益总览

**触发场景**：_"我账户表现"_、_"本月浮盈"_、_"哪只股票贡献最多"_

**数据获取**（并行）：
```bash
longbridge <profit-analysis-subcommand> --start YYYY-MM-DD --end YYYY-MM-DD --format json
longbridge <profit-analysis-detail-subcommand> --start ... --end ... --format json
longbridge <assets-subcommand> --format json
longbridge <positions-subcommand> --format json
longbridge <exchange-rate-subcommand> --format json
```

**时间窗口推断**：
| 用户表达 | 窗口 |
|---|---|
| 本月/this month | 本月1日 → 今天 |
| 本周/this week | 本周一 → 今天 |
| 近30天 | 今天-30 → 今天 |
| 今年/YTD | 1月1日 → 今天 |
| 全部/since opening | 默认使用 profit_analysis 自带默认值 |

**输出四节结构**：
1. 总览（NAV/现金/持仓/期间P&L）
2. 货币暴露（USD/HKD/CNY/SGD 各金额）
3. 单股贡献排名（前10，含盈亏方向）
4. 行业分布（持仓市值加权）

---

## longbridge-positions — 持仓快照

**触发场景**：_"我持有什么"_、_"我的仓位"_、_"多少保证金比率"_

**数据类型**：
- 股票持仓（标的/数量/成本价/现价/浮盈/浮亏%）
- 基金持仓
- 多币种现金余额
- 可用资金/融资额度/保证金比率（初始/维持）

**工作流**：
1. `longbridge <positions-subcommand> --format json`
2. 可同时获取 `longbridge <assets-subcommand>` 获取总资产概览

---

## longbridge-statement — 账户对账单

**触发场景**：_"我的月度对账单"_、_"历史现金流水"_

**数据类型**：
- 日度/月度对账单（权益持仓/现金/利息/手续费明细）
- 可选时间范围

**工作流**：
1. `longbridge <statement-subcommand> --help` 确认可用时间范围
2. 导出指定期间对账单；分段展示（权益/现金/手续费）
