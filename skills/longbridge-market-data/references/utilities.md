# Market Data: Utilities

覆盖原技能：`longbridge-fx`, `longbridge-security-list`, `longbridge-constituent`, `longbridge-subscriptions`

---

## longbridge-fx — 外汇汇率

**触发场景**：港币/美元/人民币/新加坡元/日元/欧元等汇率查询。

**数据类型**：Longbridge 支持的所有货币对实时汇率（HKD/USD/CNY/SGD/JPY/EUR/GBP 等）

**工作流**：
1. `longbridge <fx-subcommand> --help`
2. 获取指定货币对汇率（`--format json`）；可批量查询多个货币对

---

## longbridge-security-list — 证券目录

**触发场景**：美股隔夜交易可融券目录、港股经纪商参与者目录。

**数据类型**：
- 美股隔夜可交易证券列表（用于隔夜盘资质查询）
- 港股经纪商参与者列表（用于盘口经纪商解读）

**工作流**：
1. `longbridge <security-list-subcommand> --help` 确认子命令
2. 按需获取目录；数据量可能较大，建议按关键字过滤

---

## longbridge-constituent — 指数/ETF成分股

**触发场景**：恒生指数/标普500/沪深300/创业板/纳指/道指等成分股查询。

**数据类型**：指定指数或 ETF 的全量成分股列表（含权重）

**工作流**：
1. `longbridge <constituent-subcommand> --help` 确认支持的指数代码
2. 获取成分股列表（`--format json`）
3. 大型指数（标普500等）成分股多，按需截取前N名或按权重排序

---

## longbridge-subscriptions — 实时订阅诊断

**触发场景**：查看当前 WebSocket 行情订阅状态、诊断订阅问题。

**数据类型**：当前 Longbridge CLI 会话中的活跃实时订阅（标的、订阅类型如 quote/depth/trade 等）

**工作流**：
1. `longbridge <subscriptions-subcommand> --help`
2. 列出活跃订阅；用于调试实时数据推送问题
