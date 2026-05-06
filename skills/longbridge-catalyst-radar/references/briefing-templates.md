# 晨晚报输出模板

定义催化剂雷达对外输出的四种 Markdown 模板。所有输出均为纯 Markdown 格式，通过 CLI 直接呈现。

## 目录
- [模板一: 完整晨报（多市场聚合）](#模板一)
- [模板二: 单市场早报](#模板二)
- [模板三: 单市场晚报](#模板三)
- [模板四: 跨市场联动提示](#模板四)
- [篇幅控制标准](#篇幅控制标准)
- [无信号时的输出](#无信号时的输出)

---

## 模板一

**触发**: 用户说"今天有什么要关注的"、"晨报"时使用。按市场分组，距开盘时间由近到远排列。

```markdown
# 📋 催化剂晨报 | {date} {weekday}
> {user_timezone} {current_time} | 自选股 {total_count} 只 | {signal_count} 条新信号

---

## {market_flag} {market_name}早报 | 距开盘 {minutes_to_open} 分钟
> {index_name} {index_price} ({index_change_pct}) | {market_status}

### 🔴 重要
**{stock_name}({code})** {price} ({change_pct}) {resonance_tag}
- [{level}] {signal_title} {signal_detail_2_3_sentences}
- 研判: {analysis_1_sentence}
- 关注: {action_suggestion}

{如有第二条头条，同样格式}

### 🟡 关注
- **{stock}** {price}({pct}): {signal_one_line} | {key_metric}
- **{stock}** {price}({pct}): {signal_one_line} | {key_metric}
- **{stock}** {price}({pct}): {signal_one_line} | {key_metric}

---

{重复上述结构，下一个市场}

---

### 🔗 跨市场联动
- {insight_1}
- {insight_2}

---
> 数据来源: Longbridge OpenAPI | {generation_time} | 以上数据仅供参考，不构成投资建议。/ 以上數據僅供參考，不構成投資建議。/ For reference only. Not investment advice.
```

### 模板一填充规则

**重点（🔴）**:
- 最多 3 条，仅展示"重大"级信号
- 如果无重大信号，此区域不显示（不要用关注级填充）
- 每条包含: 信号标题 + 2-3句详情 + 1句研判 + 1句行动建议
- 共振标记: 如同股多维共振，在股票名后加 `⬆共振预警`
- 详情控制在 5 行以内

**关注（🟡）**:
- 最多 8 条，展示"关注"级信号
- 每条严格一行: 股票名 + 价格 + 信号摘要 + 关键指标
- 格式示例: `腾讯(0700.HK) $375.2(+1.8%): Bernstein上调目标价至$420 | +12%`

**静默区（🟢）**:
- 一行总结: "{N}只自选股今日无新增信号"

**市场排序**:
- 按当前时刻距各市场开盘时间由近到远
- 已收盘的市场排在最后，标题改为"{market_name}晚报回顾"
- 休市的市场不显示

**跨市场联动**:
- 仅在检测到联动信号时显示
- 如无联动，此区域不显示

---

## 模板二

**触发**: 用户说"A股有什么信号"、"港股早报"时使用。

```markdown
# {market_flag} {market_name}早报 | {date} {weekday}
> 距开盘 {minutes_to_open} 分钟 | {index_name} {index_price} ({index_change_pct})
> 自选股 {market_stock_count} 只 | 今日 {signal_count} 条新信号

### 🔴 重点
{同模板一格式}

### 🟡 关注
{同模板一格式}

### 📅 今日关注时点
- {time}: {event}（如"20:30 美国CPI数据公布，可能影响XX板块"）
- {time}: {event}

---
> 数据来源: Longbridge OpenAPI | {generation_time} | 以上数据仅供参考，不构成投资建议。/ 以上數據僅供參考，不構成投資建議。/ For reference only. Not investment advice.
```

**与模板一的差异**:
- 增加"今日关注时点"区域（当日有关键事件时显示）
- 头条详情可以更丰富（因为只有一个市场，篇幅更充裕）

---

## 模板三

**触发**: 用户说"关注/自选的美股昨晚怎么样"、收盘后自动推送时使用。侧重复盘而非前瞻。

```markdown
# {market_flag} {market_name}晚报 | {date} {weekday}
> 今日收盘 | {index_name} {index_price} ({index_change_pct}) | 成交额 {turnover}

### 📊 今日复盘
**{stock_name}({code})** 收盘 {price} ({change_pct})
- [{level}] {signal_title} {what_happened_detail}
- 归因: {why_it_happened}
- 明日关注: {what_to_watch_tomorrow}

### 🟡 盘后动态
- {after_hours_signal_1}（如"NVDA盘后发布财报，EPS beat 5%"）
- {after_hours_signal_2}（如"茅台公告回购计划"）

### 📈 今日自选股涨跌榜
| 涨幅前三 | | 跌幅前三 | |
|---------|---|---------|---|
| {stock1} | {pct1} | {stock1} | {pct1} |
| {stock2} | {pct2} | {stock2} | {pct2} |
| {stock3} | {pct3} | {stock3} | {pct3} |

---
> 数据来源: Longbridge OpenAPI | {generation_time} | 以上数据仅供参考，不构成投资建议。/ 以上數據僅供參考，不構成投資建議。/ For reference only. Not investment advice.
```

**晚报特有内容**:
- **归因**: 解释今天股价波动的原因（基于当日触发的信号）
- **盘后动态**: 收盘后发布的公告、财报、盘后交易价格异动
- **涨跌榜**: 自选股中今日涨幅/跌幅前三，快速总览
- **明日关注**: 基于今日信号推导明日需要关注什么

---

## 模板四

**触发**: 检测到跨市场联动信号时，独立使用或嵌入晨报。

```markdown
### 🔗 跨市场联动
**{source_market} → {target_market}**
- {source_stock}({source_code}) {source_event} → 关注 {target_market} [{target_stock_1}, {target_stock_2}] 开盘表现
  关联类型: {relation_type}（AH联动/ADR/板块传导/供应链）
```

---

## 篇幅控制标准

| 区域 | 最大条数 | 超出处理 |
|------|---------|---------|
| 🔴 重点 | 3条 | 保持不变，不可压缩 |
| 🟡 关注 | 8条 | 截断，多余折叠为"更多快讯({N}条)" |
| 🟢 静默 | 1行 | 始终一行 |

---

## 无信号时的输出

如果所有市场所有自选股都没有新增信号:

```markdown
# 📋 催化剂晨报 | {date} {weekday}
> {user_timezone} {current_time}
> ☀️ 今日所有自选股无新增催化剂信号。

**最近一次信号**: {last_signal_stock} {last_signal_date} — {last_signal_summary}
**下一个关注节点**: {next_key_date} — {next_key_event}
```

> 不要为了填充而降低信号标准。宁可推一份"无新增"的简报，也不要推一堆噪音。
