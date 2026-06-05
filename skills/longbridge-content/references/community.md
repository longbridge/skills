# Content: Community

覆盖原技能：`longbridge-topic`, `longbridge-sharelist`

---

## longbridge-topic — 社区话题与讨论

**触发场景**：_"AAPL 在社区里怎么讨论的"_、_"长桥社区最热门话题"_、_"我能参与社区讨论吗"_

**功能**：浏览长桥社区围绕特定股票或主题的讨论，查看热门帖子和用户观点。

### 操作类型

| 操作 | 说明 |
|---|---|
| 按股票查询 | 查看某只股票的社区讨论帖子 |
| 热门话题 | 全市场当前热门讨论排行 |
| 话题详情 | 查看单个话题的完整内容和回复 |

### 工作流

1. `longbridge --help` → 找到话题/社区子命令
2. `longbridge <topic-subcommand> {SYMBOL} --format json`（个股话题）
   或 `longbridge <topic-subcommand> --trending --format json`（热门排行）
3. 展示帖子标题、作者、发布时间、点赞数和摘要

### 输出模板

```
💬 {SYMBOL} 社区话题 — 近7日

【热门帖子】
1. "{标题}" — {作者}（{日期}，{点赞数}👍）
   {1句摘要}
2. ...

【社区情绪概览】
• 总帖数：{N}（近7日）
• 情绪倾向：看多 {X%} / 看空 {Y%} / 中性 {Z%}

---
数据来源：Longbridge 社区
```

---

## longbridge-sharelist — 社区股票列表

**触发场景**：_"长桥热门股票列表"_、_"有哪些社区分享的选股列表"_、_"创建我的选股列表"_

**功能**：浏览、创建和管理长桥社区公开的股票组合列表（Share List）。

### 列表类型

| 类型 | 说明 |
|---|---|
| 平台精选 | Longbridge 编辑精选的主题列表 |
| 热门列表 | 社区用户关注度最高的公开列表 |
| 个人列表 | 用户自己创建的可公开分享的列表 |

### 工作流

1. `longbridge --help` → 找到 sharelist 子命令
2. 浏览：`longbridge <sharelist-subcommand> --trending --format json`
3. 查看详情：`longbridge <sharelist-subcommand> <list_id> --format json`
4. 成分股分析：提取列表成分后路由到 `longbridge-market-data` 或 `longbridge-fundamentals`

### 输出模板

```
📋 热门股票列表 — {日期}

【平台精选】
1. "{列表名}" — {创建者}（{N}只股票，{M}人关注）
   {主题描述}

【用户热榜 Top3】
1. "{列表名}" — @{用户名}（近7日涨幅 {X%}）
   成分：{symbol1}, {symbol2}, ...
```

---

### 注意

- 社区列表内容由用户创建，不代表 Longbridge 投资建议
- 创建/修改个人列表属于账户变更操作，需要登录（`longbridge auth login`）
