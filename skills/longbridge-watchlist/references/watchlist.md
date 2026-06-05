# Watchlist: Read & Manage

覆盖原技能：`longbridge-watchlist`, `longbridge-watchlist-admin`

---

## longbridge-watchlist — 自选股只读查询

**触发场景**：_"我的自选股"_、_"科技组里有哪些股票"_

**输出内容**：
- 所有自选股分组（group_id、名称、成员数）
- 指定分组的成员股票（symbol、名称、当前涨跌幅）

**工作流**：
1. 运行 `longbridge --help` 找到自选股查询子命令
2. `longbridge <watchlist-subcommand> --format json`
3. 列出分组及成员；如需行情数据，路由到 `longbridge-market-data`

---

## longbridge-watchlist-admin — 自选股变更操作

**触发场景**：_"把 NVDA 加到科技组"_、_"新建一个 AI 概念分组"_、_"重命名科技组为半导体"_

⚠️ **所有变更操作必须执行两步协议（预览 + 确认）**

### 支持的操作

| 操作 | 说明 |
|---|---|
| 创建分组 | 新建自选股分组，指定名称 |
| 重命名分组 | 修改现有分组名称 |
| 删除分组 | 删除分组（注意：成员股票不会被删除） |
| 添加标的 | 将股票/ETF 添加到指定分组 |
| 移除标的 | 从指定分组移除股票/ETF |

### 两步协议

**第一步 — 预览**（不调用 CLI，仅描述）：
> "即将把 NVDA.US 添加到「科技」分组，确认执行？"

**第二步 — 执行**（收到确认后）：
```bash
longbridge <watchlist-subcommand> add --group <group_id> --symbol NVDA.US --format json
```

### group_id 获取

变更前必须先查询只读接口获取正确的 group_id，不得硬编码或猜测。

### 预览模板

```
操作：添加标的
分组：科技（group_id: xxx）
标的：NVDA.US（英伟达）
---
确认执行请回复"确认 / yes / confirm"
```

```
操作：创建分组
分组名称："AI 概念"
---
确认执行请回复"确认 / yes / confirm"
```
