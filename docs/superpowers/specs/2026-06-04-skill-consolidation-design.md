# Skill Consolidation Design — 11 大方向 Skills

**Date:** 2026-06-04  
**Status:** Approved  
**Scope:** CLI 命令对应 skill 的合并重构，不涉及基础 `longbridge` skill 及 PR 外部贡献 skill

---

## 背景与目标

当前 `skills/` 目录有 127 个 skill，其中约 77 个与 `longbridge` CLI 命令一一对应，粒度过细，导致：

- 用户安装负担重（需选择合适的 skill）
- 内容重复（多个 skill 调用同一类命令）
- 维护成本高（CLI 升级需修改多个文件）

**目标**：将 CLI 对应的 skill 合并为 11 个「大方向 skill」，每个 skill 覆盖一个功能域的所有相关 CLI 命令。

---

## 不在范围内（保持原样）

### 基础 skill
- `longbridge` — Longbridge 开发者平台入口，保持原样

### 外部 PR 贡献 skill（独立保留）
- longbridge-turtle-signal、longbridge-chanlun、longbridge-smc、longbridge-elliott-wave
- longbridge-ark-analysis、longbridge-buffett-moat-analyzer、longbridge-buffett-moat-stock-screener
- longbridge-graham-stock-analysis、longbridge-graham-screener
- longbridge-ml-strategy、longbridge-defi-yield、longbridge-onchain
- longbridge-earnings（外部贡献）、longbridge-earnings-preview（外部贡献）

### 纯框架/分析类 skill（无 CLI 直接对应，独立保留）
longbridge-portfolio-diagnosis、longbridge-portfolio-rebalance、longbridge-asset-allocation、
longbridge-risk-analysis、longbridge-risk-return、longbridge-tax-harvesting、
longbridge-pairs-trading、longbridge-volatility-strategy、longbridge-seasonality、
longbridge-performance-attribution、longbridge-dcf、longbridge-behavioral-finance、
longbridge-competitive-analysis、longbridge-coverage-initiation、longbridge-investment-ideas、
longbridge-investment-proposal、longbridge-morning-brief、longbridge-catalyst-radar、
longbridge-stock-research、longbridge-industry-overview、longbridge-tech-hype、
longbridge-supply-chain、longbridge-event-strategy、longbridge-event-opportunity、
longbridge-etf-analysis、longbridge-etf-flow、longbridge-sector-rotation、
longbridge-sector-monitor、longbridge-market-microstructure、longbridge-hkipo-analysis、
longbridge-financial-planning、longbridge-smallcap-growth、longbridge-value-screen、
longbridge-multifactor、longbridge-factor-research、longbridge-factor-screen、
longbridge-correlation、longbridge-quant-stats、longbridge-strategy-optimizer、
longbridge-thesis-tracker、longbridge-post-investment、longbridge-hedging、
longbridge-execution-model、longbridge-valuation-methodology、longbridge-adr-premium、
longbridge-fx-carry、longbridge-sec-filings、longbridge-insresearch（部分框架）、
longbridge-ichimoku、longbridge-candlestick、longbridge-technical、longbridge-harmonic、
longbridge-elliott、longbridge-fx

---

## 11 个新 Skill 设计

### 1. `longbridge-market-data`

**覆盖 CLI 命令：**
`quote` `depth` `brokers` `trades` `intraday` `kline` `static` `calc-index` `capital` `market-temp` `trading` `security-list` `participants` `subscriptions` `ah-premium` `trade-stats` `market-status` `exchange-rate`

**取代的现有 skills：**
longbridge-quote, longbridge-kline, longbridge-depth, longbridge-capital-flow,
longbridge-market-temp, longbridge-security-list, longbridge-subscriptions,
longbridge-ah-premium, longbridge-index-quote, longbridge-northbound-flow

**触发场景：** 实时行情、K线、盘口、资金流、市场温度、汇率、交易日历

---

### 2. `longbridge-derivatives`

**覆盖 CLI 命令：**
`option` `warrant`

**取代的现有 skills：**
longbridge-derivatives（slug 保留，内容重写）

**触发场景：** 期权链、认购认沽、窝轮、牛熊证、IV、Greeks

---

### 3. `longbridge-fundamentals`

**覆盖 CLI 命令：**
`financial-report` `financial-statement` `business-segments` `dividend` `valuation`
`industry-valuation` `operating` `corp-action` `invest-relation` `company`
`executive` `valuation-rank` `compare`

**取代的现有 skills：**
longbridge-fundamental, longbridge-financial-report, longbridge-financial-analysis,
longbridge-financial-checkup, longbridge-valuation, longbridge-valuation-rank,
longbridge-peer-comparison, longbridge-operating, longbridge-dividend-screen,
longbridge-basicinfo, longbridge-business-query, longbridge-finance-query,
longbridge-industry-valuation

**触发场景：** 财报三表、估值、分红、行业估值、公司信息、高管、股权关系

---

### 4. `longbridge-research`

**覆盖 CLI 命令：**
`institution-rating` `forecast-eps` `consensus` `finance-calendar` `shareholder`
`fund-holder` `insider-trades` `investors` `short-positions` `short-trades`
`industry-rank` `industry-peers`

**取代的现有 skills：**
longbridge-insresearch（部分）, longbridge-consensus, longbridge-earnings-revision,
longbridge-analyst-estimates, longbridge-flows, longbridge-ownership,
longbridge-investors, longbridge-calendar

**触发场景：** 机构评级、一致预期、内部人交易、空头数据、行业排名

---

### 5. `longbridge-portfolio`

**覆盖 CLI 命令：**
`assets` `cash-flow` `portfolio` `positions` `fund-positions` `margin-ratio`
`max-qty` `profit-analysis` `statement` `bank-cards` `withdrawals` `deposits`

**取代的现有 skills：**
longbridge-portfolio（slug 保留）, longbridge-positions, longbridge-statement,
longbridge-profit-analysis

**触发场景：** 账户总览、持仓、盈亏、资金记录、对账单

---

### 6. `longbridge-orders`

**覆盖 CLI 命令：**
`order` `dca`

**取代的现有 skills：**
longbridge-orders, longbridge-dca

**触发场景：** 下单、撤单、改单、定投

---

### 7. `longbridge-ipo`

**覆盖 CLI 命令：**
`ipo`（子命令：subscriptions、calendar、orders、profit-loss）

**取代的现有 skills：**
longbridge-ipo（slug 保留，内容核对更新）

**触发场景：** 新股认购、IPO 日历、打新盈亏

---

### 8. `longbridge-quant`

**覆盖 CLI 命令：**
`quant`（运行指标脚本）

**取代的现有 skills：**
longbridge-quant（slug 保留，内容核对更新）

**触发场景：** 量化指标脚本、K 线数据回测输入

---

### 9. `longbridge-watchlist`

**覆盖 CLI 命令：**
`watchlist` `alert` `sharelist`

**取代的现有 skills：**
longbridge-watchlist, longbridge-watchlist-admin, longbridge-alert, longbridge-sharelist

**注意：** `watchlist` 包含读写操作（create/update/delete），mutating 操作需保留 dry-run + confirm 协议

**触发场景：** 自选股管理、价格提醒、公开股票清单

---

### 10. `longbridge-content`

**覆盖 CLI 命令：**
`news` `filing` `topic`

**取代的现有 skills：**
longbridge-news

**触发场景：** 股票新闻、公告/文件、社区讨论话题

---

### 11. `longbridge-scanner`

**覆盖 CLI 命令：**
`screener` `rank` `top-movers` `anomaly` `constituent`

**取代的现有 skills：**
longbridge-market-scanner, longbridge-sector-screener, longbridge-anomaly,
longbridge-constituent

**触发场景：** 策略筛选器、热度排名、异动榜、成分股

---

## SKILL.md 结构规范

每个新 skill 的 SKILL.md：

```
---
name: longbridge-<domain>
description: |
  <功能概述>. Triggers: <触发词列表 ZH-Hans / ZH-Hant / EN>
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: read_only | account_read | mutating
  requires_login: false | true
  default_install: true
  requires_mcp: false
  tier: read
---

# Longbridge <Domain>

> **Response language**: match the user's input language —
> Simplified Chinese / Traditional Chinese / English.

## When to use
## Workflow
## Commands
  ### <command-name>
  ### <command-name>
  ...
## Output
## Error handling
## MCP fallback
## Related skills
## File layout
```

- **正文不超过 200 行**，命令详情（字段表、示例）移入 `references/<command>.md`
- **不硬编码子命令 flag 名**，指示 LLM 用 `longbridge <cmd> --help` 发现
- description 不超过 1024 字符

---

## 退役处理

重构完成后，以下 slug 对应的旧 skill 目录**删除**（用户重新安装新 skill 获取等效功能）：

共约 40 个旧目录，主要包括：
longbridge-quote, longbridge-kline, longbridge-depth, longbridge-capital-flow,
longbridge-market-temp, longbridge-security-list, longbridge-subscriptions,
longbridge-ah-premium, longbridge-index-quote, longbridge-northbound-flow,
longbridge-fundamental, longbridge-financial-report, longbridge-financial-analysis,
longbridge-financial-checkup, longbridge-valuation, longbridge-valuation-rank,
longbridge-peer-comparison, longbridge-operating, longbridge-dividend-screen,
longbridge-basicinfo, longbridge-business-query, longbridge-finance-query,
longbridge-industry-valuation, longbridge-consensus, longbridge-earnings-revision,
longbridge-analyst-estimates, longbridge-flows, longbridge-ownership,
longbridge-investors, longbridge-calendar, longbridge-positions,
longbridge-statement, longbridge-profit-analysis, longbridge-dca,
longbridge-watchlist-admin, longbridge-alert, longbridge-sharelist,
longbridge-news, longbridge-market-scanner, longbridge-sector-screener,
longbridge-anomaly, longbridge-constituent

---

## 验收标准

1. 11 个新 SKILL.md 均通过 `brew style`（如适用）和手动 trigger 测试
2. 每个新 skill 覆盖所有对应 CLI 命令的触发词（中/繁/英）
3. Response language 指令存在于每个 SKILL.md
4. 旧目录已删除，README/docs/install.md skill 数量更新
5. `well-known-skills-index.json` 和 `index.json` 重新生成
