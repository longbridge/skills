# Orders: Order History and Cash Flow

覆盖原技能：`longbridge-orders`

---

## longbridge-orders — 订单/成交/现金流水（只读）

**触发场景**：查看历史成交、当日委托、现金流水记录。

**数据类型**：
- 今日委托（含已成交/未成交/已撤销）
- 历史成交记录（可按标的/日期/方向筛选）
- 账户现金流水（入金/出金/手续费/股息/利息）

**工作流**：
1. 确认 trade 权限登录：`longbridge auth login`
2. `longbridge <orders-subcommand> --help` 确认过滤参数（日期/标的/状态）
3. 获取数据（`--format json`）

**输出示例**：
```
历史成交记录 — 来源：Longbridge Securities

| 日期 | 标的 | 方向 | 数量 | 成交价 | 成交金额 | 手续费 |
|---|---|---|---|---|---|---|
| 2026-06-01 | NVDA.US | 买入 | 10 | $110.5 | $1,105 | $1.1 |
| 2026-05-28 | 700.HK | 卖出 | 100 | HK$380 | HK$38,000 | HK$9.5 |
```

**注意**：本 skill 为只读操作；下单/撤单等交易操作需通过 Longbridge APP 或 SDK 执行。
