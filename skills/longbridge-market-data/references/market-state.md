# Market Data: Market State

覆盖原技能：`longbridge-index-quote`, `longbridge-market-temp`, `longbridge-market-scanner`, `longbridge-anomaly`

---

## longbridge-index-quote — 主要指数行情

**触发场景**：恒生指数/沪深300/创业板指/标普500/纳指/道指等今日行情。

**数据类型**：主要指数实时行情（最新点位/涨跌幅/成交量/成交额）

**工作流**：
1. `longbridge <index-quote-subcommand> --help`
2. 常见指数代码：`HSI.HK`（恒指）、`000300.SH`（沪深300）、`.SPX`（标普500）等；`--help` 确认可用代码

---

## longbridge-market-temp — 市场温度与情绪

**触发场景**：市场热度、涨跌家数、板块热力分布、市场情绪指数（0–100）。

**数据类型**：
- 市场温度指数（0=极度悲观，100=极度乐观）
- 涨跌家数、创新高/新低家数
- 板块涨跌分布

**工作流**：
1. `longbridge <market-temp-subcommand> --help`
2. 获取市场状态数据；可在早报和盘中分析中使用

---

## longbridge-market-scanner — 综合市场扫描器

**触发场景**：扫描全市场异动标的、综合行情+资金+动能排名。

**数据类型**：
- 结合实时行情/资金流向/价格动能的综合扫描
- 按涨跌幅/成交量/资金流入排序

**工作流**：
1. `longbridge <market-scanner-subcommand> --help` 确认筛选参数
2. 设定扫描条件；输出热门/异动标的列表

---

## longbridge-anomaly — 市场异常扫描

**触发场景**：价格/成交量异常、筹码分布、价量背离信号。

**数据类型**：
- 异常价格/成交量信号（与近N日均值对比）
- 价格-成交量分布（筹码峰）

**工作流**：
1. `longbridge <anomaly-subcommand> --help`
2. 获取异常信号；提示用户异常不代表方向，仅供关注
