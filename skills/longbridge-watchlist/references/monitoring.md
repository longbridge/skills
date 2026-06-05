# Watchlist: Catalyst Monitoring

覆盖原技能：`longbridge-catalyst-radar`

---

## longbridge-catalyst-radar — 自选股催化剂雷达

**触发场景**：_"帮我设置自选股晨报"_、_"催化剂雷达"_、_"监控我的自选股"_

**功能**：扫描自选股列表，自动识别潜在催化剂事件，生成晨/晚报摘要。

---

### 催化剂类型

| 类型 | 示例 |
|---|---|
| 财报公布 | 本周/下周财报日期 |
| 分析师评级变化 | 评级上调/下调 |
| 重大新闻 | 并购、监管、产品发布 |
| 技术面信号 | 突破关键支撑/阻力位 |
| 宏观事件 | FOMC、CPI、非农等 |

---

### 晨报输出模板

```
📋 自选股催化剂雷达 — {日期} 盘前

🔥 高优先级
• {symbol}：{催化剂描述}（来源：{数据源}）

📅 本周事件
• {symbol}：财报日期 {日期}，预期 EPS {值}

📊 技术面信号
• {symbol}：{信号描述}

---
数据来源：Longbridge Securities
```

---

### 工作流

1. 运行 `longbridge --help` 获取自选股查询子命令
2. 获取自选股列表（所有分组）
3. 对每只股票并行获取：
   - 财报日历（路由到 `longbridge-fundamentals` → references/earnings.md）
   - 近期新闻（路由到 `longbridge-content` → references/news.md）
   - 分析师评级变化（路由到 `longbridge-research` → references/analyst.md）
4. 按优先级排序催化剂，生成摘要报告

---

### 注意事项

- 自选股数量较多时，优先覆盖仓位占比最大或用户最近查询的标的
- 催化剂雷达为信息汇总服务，不构成交易建议
- 实时数据依赖 Longbridge 数据服务，部分数据可能有延迟
