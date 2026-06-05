# Skill Consolidation Design — 18 大方向 Skills

**Date:** 2026-06-04  
**Updated:** 2026-06-05  
**Status:** Approved  
**Scope:** 全量 skill 重构——CLI 对应 skill + 框架/分析类 skill，不涉及基础 `longbridge` skill 及 PR 外部贡献 skill

---

## 背景与目标

当前 `skills/` 目录有 127 个 skill，粒度过细，导致：

- 用户安装负担重（需选择合适的 skill）
- 内容重复（多个 skill 调用同一类命令）
- 维护成本高（CLI 升级需修改多个文件）

**目标**：将全部 skill 合并为 **18 个大方向 skill**（11 个 CLI 域 + 7 个框架域），正文不超过 200 行，细节移入 `references/`。

---

## 不在范围内（保持原样）

### 基础 skill
- `longbridge` — Longbridge 开发者平台入口，保持原样

### 外部 PR 贡献 skill（独立保留）

| Skill | 来源 PR |
|---|---|
| longbridge-earnings | PR #1（userjsabc1）|
| longbridge-earnings-preview | PR #14（userjsabc1）|
| longbridge-chanlun | PR #17（batch 1）→ 并入 `longbridge-technical` |
| longbridge-smc | PR #17（batch 1）→ 并入 `longbridge-technical` |
| longbridge-elliott | PR #17（batch 1）→ 并入 `longbridge-technical` |
| longbridge-harmonic | PR #17（batch 1）→ 并入 `longbridge-technical` |
| longbridge-ml-strategy | PR #18（batch 2）→ 并入 `longbridge-quant-strategy` |
| longbridge-defi-yield | PR #18（batch 2）→ 并入 `longbridge-cross-market` |
| longbridge-onchain | PR #18（batch 2）→ 并入 `longbridge-cross-market` |
| longbridge-graham-screener | PR #24 |
| longbridge-graham-stock-analysis | PR #24 |
| longbridge-buffett-moat-analyzer | PR #25 |
| longbridge-buffett-moat-stock-screener | PR #25 / #42 |
| longbridge-elliott-wave | PR #28 |
| longbridge-ark-analysis | PR #29 |
| longbridge-turtle-signal | PR #36 |

---

## Part 1：11 个 CLI 大方向 Skill

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
longbridge-insresearch, longbridge-consensus, longbridge-earnings-revision,
longbridge-analyst-estimates, longbridge-flows, longbridge-ownership,
longbridge-investors, longbridge-calendar

**注：** `longbridge-insresearch` 功能与本 skill 完全重叠（institution-rating / consensus / forecast-eps），直接合并，不保留旧 slug。

**触发场景：** 机构评级、一致预期、分析师目标价、内部人交易、空头数据、行业排名

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

**注意：** mutating 操作（create/update/delete）需保留 dry-run + confirm 协议

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

## Part 2：7 个框架大方向 Skill

框架 skill 没有直接对应的单一 CLI 命令，每个 SKILL.md 正文 ≤ 200 行，细节内容迁入 `references/<sub-skill>.md`。

### 12. `longbridge-portfolio-risk`

**覆盖：**
portfolio-diagnosis, portfolio-rebalance, asset-allocation, risk-analysis,
risk-return, performance-attribution, tax-harvesting

**references/：** portfolio-diagnosis.md, portfolio-rebalance.md, asset-allocation.md,
risk-analysis.md, risk-return.md, performance-attribution.md, tax-harvesting.md

**触发场景：** 组合诊断、再平衡、资产配置、风险分析、绩效归因、税损收割

---

### 13. `longbridge-investment-research`

**覆盖：**
investment-ideas, investment-proposal, coverage-initiation, stock-research,
competitive-analysis, thesis-tracker, post-investment, hkipo-analysis, financial-planning

**references/：** 9 个对应文件

**触发场景：** 投资想法、投资提案、首次覆盖报告、股票研究、竞争格局、投资逻辑跟踪

---

### 14. `longbridge-quant-strategy`

**覆盖：**
pairs-trading, volatility-strategy, seasonality, multifactor, factor-research,
factor-screen, correlation, quant-stats, strategy-optimizer, execution-model, hedging,
ml-strategy（PR #18）

**references/：** 12 个对应文件

**触发场景：** 配对交易、波动率策略、季节性、多因子选股、量化统计、对冲

---

### 15. `longbridge-technical`

**覆盖：**
ichimoku, candlestick, technical, harmonic, elliott,
chanlun（PR #17）, smc（PR #17）

（slug 保留，扩展为覆盖全部技术分析框架）

**references/：** ichimoku.md, candlestick.md, technical.md, harmonic.md, elliott.md, chanlun.md, smc.md

**触发场景：** 一目均衡表、蜡烛图形态、技术指标、谐波形态、艾略特波浪、缠论分型笔中枢、Smart Money Concepts

---

### 16. `longbridge-value-analysis`

**覆盖：**
dcf, valuation-methodology, behavioral-finance, value-screen, smallcap-growth

**references/：** 5 个对应文件

**触发场景：** DCF 现金流折现、估值方法论、行为金融、低估值筛选、小盘成长

---

### 17. `longbridge-market-intel`

**覆盖：**
morning-brief, catalyst-radar, event-strategy, event-opportunity, industry-overview,
tech-hype, sector-rotation, sector-monitor, market-microstructure, supply-chain

**references/：** 10 个对应文件

**触发场景：** 晨报、催化剂雷达、事件驱动、行业概览、科技炒作识别、产业链

---

### 18. `longbridge-cross-market`

**覆盖：**
etf-analysis, etf-flow, adr-premium, fx-carry, sec-filings, fx,
defi-yield（PR #18）, onchain（PR #18）

**references/：** 8 个对应文件

**触发场景：** ETF 分析、ETF 资金流、ADR 溢价、外汇套息、SEC 文件、外汇、DeFi 收益、链上数据

---

## SKILL.md 结构规范

```yaml
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
```

**正文结构：**
```
# Longbridge <Domain>

> Response language directive
> Data-source policy directive

## When to use
## Workflow
## Commands / Frameworks  （每个子命令/子框架一节，简述 + 加载对应 references/ 文件）
## Error handling
## MCP fallback
## Related skills
## File layout
```

**约束：**
- 正文 ≤ 200 行
- 不硬编码 flag 名，指示 LLM 用 `longbridge <cmd> --help` 发现
- description ≤ 1024 字符
- 框架 skill 每个子框架的完整内容在 `references/<sub>.md`

---

## 退役 Skill 列表

重构完成后删除以下旧目录（约 55 个）：

**CLI 类退役：**
longbridge-quote, longbridge-kline, longbridge-depth, longbridge-capital-flow,
longbridge-market-temp, longbridge-security-list, longbridge-subscriptions,
longbridge-ah-premium, longbridge-index-quote, longbridge-northbound-flow,
longbridge-fundamental, longbridge-financial-report, longbridge-financial-analysis,
longbridge-financial-checkup, longbridge-valuation, longbridge-valuation-rank,
longbridge-peer-comparison, longbridge-operating, longbridge-dividend-screen,
longbridge-basicinfo, longbridge-business-query, longbridge-finance-query,
longbridge-industry-valuation, longbridge-insresearch, longbridge-consensus,
longbridge-earnings-revision, longbridge-analyst-estimates, longbridge-flows,
longbridge-ownership, longbridge-investors, longbridge-calendar,
longbridge-positions, longbridge-statement, longbridge-profit-analysis, longbridge-dca,
longbridge-watchlist-admin, longbridge-alert, longbridge-sharelist, longbridge-news,
longbridge-market-scanner, longbridge-sector-screener, longbridge-anomaly,
longbridge-constituent

**框架类退役（内容迁入 references/）：**
longbridge-portfolio-diagnosis, longbridge-portfolio-rebalance, longbridge-asset-allocation,
longbridge-risk-analysis, longbridge-risk-return, longbridge-performance-attribution,
longbridge-tax-harvesting, longbridge-investment-ideas, longbridge-investment-proposal,
longbridge-coverage-initiation, longbridge-stock-research, longbridge-competitive-analysis,
longbridge-thesis-tracker, longbridge-post-investment, longbridge-hkipo-analysis,
longbridge-financial-planning, longbridge-pairs-trading, longbridge-volatility-strategy,
longbridge-seasonality, longbridge-multifactor, longbridge-factor-research,
longbridge-factor-screen, longbridge-correlation, longbridge-quant-stats,
longbridge-strategy-optimizer, longbridge-execution-model, longbridge-hedging,
longbridge-ml-strategy,
longbridge-ichimoku, longbridge-candlestick, longbridge-harmonic, longbridge-elliott,
longbridge-chanlun, longbridge-smc,
longbridge-dcf, longbridge-valuation-methodology, longbridge-behavioral-finance,
longbridge-value-screen, longbridge-smallcap-growth, longbridge-morning-brief,
longbridge-catalyst-radar, longbridge-event-strategy, longbridge-event-opportunity,
longbridge-industry-overview, longbridge-tech-hype, longbridge-sector-rotation,
longbridge-sector-monitor, longbridge-market-microstructure, longbridge-supply-chain,
longbridge-etf-analysis, longbridge-etf-flow, longbridge-adr-premium,
longbridge-fx-carry, longbridge-sec-filings, longbridge-fx,
longbridge-defi-yield, longbridge-onchain

---

## 重构后 Skill 总数

| 类型 | 数量 |
|---|---|
| 11 个 CLI 大方向 skill | 11 |
| 7 个框架大方向 skill | 7 |
| 外部 PR 贡献 skill（保留） | 7 |
| 基础 `longbridge` skill | 1 |
| **合计** | **26** |

从 127 → 26，减少 80%。

---

## 验收标准

1. 18 个新 SKILL.md 正文均 ≤ 200 行
2. 每个新 skill 覆盖所有对应命令/框架的触发词（ZH-Hans / ZH-Hant / EN）
3. Response language + Data-source policy 指令存在于每个 SKILL.md
4. 框架 skill 各子框架内容已迁入 `references/<sub>.md`
5. 旧目录已删除，README / docs/install.md / CLAUDE.md skill 数量更新为 33
6. `well-known-skills-index.json` 和 `index.json` 重新生成
7. `longbridge-watchlist` mutating 操作保留 dry-run + confirm 协议
