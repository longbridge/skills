# Market Data: Capital Flows

覆盖原技能：`longbridge-capital-flow`, `longbridge-northbound-flow`, `longbridge-etf-flow`

---

## longbridge-capital-flow — 盘中资金流向

**触发场景**：单股大单/中单/小单分布、资金净流入/流出、超大单方向。

**数据类型**：
- 盘中资金流向时序（5分钟/1小时区间）
- 大单/中单/小单买入/卖出分布
- 净流入金额与方向

**工作流**：
1. `longbridge <capital-flow-subcommand> --help` 确认时间区间参数
2. 获取数据（`--format json`）
3. 解读：大单净流入为正时，通常反映机构/主力买入意向

---

## longbridge-northbound-flow — 沪深港通北向/南向资金

**触发场景**：北向资金（外资买A股）、南向资金（陆资买港股）、沪股通/深股通分类。

**数据类型**：
- 北向资金（今日/近N日）净买入/净卖出总量
- 分沪股通/深股通分类
- 南向资金（陆资通过港股通买港股）

**工作流**：
1. `longbridge <northbound-subcommand> --help`
2. 获取数据；解读：北向大规模净买入往往是 A 股积极信号

---

## longbridge-etf-flow — 美国ETF资金流向

**触发场景**：ETF 净申购/赎回、机构通过 ETF 的资金迁移。

**数据类型**：
- 近期 ETF 资金净流入（按 ETF 品种）
- 大盘/行业/主题 ETF 分类

**工作流**：
1. `longbridge <etf-flow-subcommand> --help`
2. 获取数据；结合 ETF 跟踪指数解读机构资金流向趋势
