# Orders: DCA Plans and Price Alerts

覆盖原技能：`longbridge-dca`, `longbridge-alert`

---

## ⚠️ 变更操作说明

以下所有操作均为**持久性变更**，必须严格执行两步协议：

1. **预览** — 向用户描述即将执行的操作（标的/金额/频率/触发价位）
2. **等待明确确认**（"确认 / yes / 是的 / confirm"）
3. **执行** — 仅在确认后调用 CLI

---

## longbridge-dca — 定投计划管理

**触发场景**：_"设置每周买入AAPL 100美元的定投"_、_"查看我的定投计划"_、_"暂停茅台定投"_

**操作类型**：
- 列表（只读）：查看当前所有定投计划
- 创建：新建定投计划（标的/金额/频率/开始日期）
- 开启/暂停：切换计划状态
- 删除：永久删除计划（⚠️不可撤销）

**频率选项**：每日/每周/每月（具体参数值运行 `--help` 确认）

**工作流**：
1. `longbridge <dca-subcommand> --format json`（列表查看，无需确认）
2. 创建/变更：先预览 → 等待确认 → 执行
3. `longbridge <dca-subcommand> create SYMBOL --amount X --frequency <freq> --format json`

**创建预览模板**：
> 即将为 {symbol} 创建定投计划：每{频率}买入 ${金额}，从 {日期} 开始。是否确认执行？

---

## longbridge-alert — 价格提醒管理

**触发场景**：_"NVDA跌到100提醒我"_、_"删除TSLA的提醒"_、_"查看所有提醒"_

**操作类型**：
- 列表（只读）：查看当前所有价格提醒
- 添加：新建价格提醒（标的/触发条件/价位）
- 开启/关闭：切换提醒状态
- 删除：删除提醒（⚠️不可撤销）

**触发条件类型**：价格高于/低于/涨幅超过/跌幅超过（具体参数运行 `--help` 确认）

**工作流**：
1. `longbridge <alert-subcommand> --format json`（查看，无需确认）
2. 添加/删除：先预览 → 等待确认 → 执行
3. `longbridge <alert-subcommand> add SYMBOL --condition <type> --value X --format json`

**创建预览模板**：
> 即将为 {symbol} 添加价格提醒：当价格{条件} ${价位} 时触发。是否确认执行？
