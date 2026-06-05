# Research: Institutional Investors and Smart Money

覆盖原技能：`longbridge-investors`, `longbridge-flows`

---

## longbridge-investors — SEC 13F 机构投资者追踪

**触发场景**：查看顶级机构投资者的持仓、追踪"聪明钱"的选股。

**数据类型**：
- 顶50活跃机构投资者（按AUM排序）
- 单一机构的详细持仓（最新13F季报）
- 机构入场/离场信号（新建仓/增持/减持/清仓）

**工作流**：
1. `longbridge <investors-subcommand> --format json`（列出顶级投资者）
2. `longbridge <investors-subcommand> <CIK> --format json`（单一机构持仓详情）
3. 追踪：Berkshire/Bridgewater/Appaloosa 等知名机构的最新动向

**重要注意**：13F 报告为季度披露，存在45天滞后。当前13F的持仓不代表现在的真实持仓。

---

## longbridge-flows — 聪明钱与机构资金流信号

**触发场景**：综合 SEC 13F 持仓变化、短期资金流向信号分析。

**信号类型**：

| 信号 | 含义 |
|---|---|
| 多家知名机构同期新建仓 | 强看多信号 |
| 明星基金经理增持 | 关注（但需验证逻辑） |
| 集中减仓/清仓 | 谨慎信号 |
| 内部人增持（SEC Form 4） | 正面信号（管理层自信） |
| 内部人在高位大量减持 | 谨慎（但需区分计划性减持） |

**工作流**：
1. 获取 13F 持仓变化（`longbridge-investors`）
2. 获取内部人交易（`longbridge <insider-trades-subcommand> SYMBOL --format json`）
3. 综合分析：机构方向 + 内部人方向 → 综合判断
