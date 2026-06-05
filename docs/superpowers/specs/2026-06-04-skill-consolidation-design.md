# Skill Consolidation Design — 11 大方向 Skills（终稿）

**Date:** 2026-06-04  
**Updated:** 2026-06-05  
**Status:** Approved — Final  
**Scope:** 全量 skill 重构，合并为 11 个大方向 skill

---

## 背景与目标

当前 `skills/` 目录有 127 个 skill，粒度过细，导致用户安装负担重、内容重复、维护成本高。

**目标**：将全部 skill 合并为 **11 个大方向 skill**，每个 skill 覆盖一个功能域的 CLI 命令 + 对应框架/分析内容。SKILL.md 正文 ≤ 200 行，细节内容迁入 `references/`。

**最终数量：127 → 21（-83%）**

| 类型 | 数量 |
|---|---|
| 11 个大方向 skill | 11 |
| 外部 PR 独立保留 | 9（来自 7 个 PR）|
| 基础 `longbridge` skill | 1 |
| **合计** | **21** |

---

## 不在范围内（保持原样）

### 基础 skill
- `longbridge` — Longbridge 开发者平台入口

### 外部 PR 贡献 skill（独立保留）

| Skill | 来源 PR |
|---|---|
| longbridge-earnings | PR #1（userjsabc1）|
| longbridge-earnings-preview | PR #14（userjsabc1）|
| longbridge-graham-screener | PR #24 |
| longbridge-graham-stock-analysis | PR #24 |
| longbridge-buffett-moat-analyzer | PR #25 |
| longbridge-buffett-moat-stock-screener | PR #25 / #42 |
| longbridge-elliott-wave | PR #28 |
| longbridge-ark-analysis | PR #29 |
| longbridge-turtle-signal | PR #36 |

---

## 11 个大方向 Skill

### 1. `longbridge-market-data`

**CLI 命令（18个）：**
`quote` `depth` `brokers` `trades` `intraday` `kline` `static` `calc-index`
`capital` `market-temp` `trading` `security-list` `participants` `subscriptions`
`ah-premium` `trade-stats` `market-status` `exchange-rate`

**框架内容（并入 references/）：**
ichimoku, candlestick, technical, harmonic, elliott（PR #17 中的 chanlun, smc）,
fx-carry, adr-premium

**退役旧 skills：**
longbridge-quote, longbridge-kline, longbridge-depth, longbridge-capital-flow,
longbridge-market-temp, longbridge-security-list, longbridge-subscriptions,
longbridge-ah-premium, longbridge-index-quote, longbridge-northbound-flow,
longbridge-ichimoku, longbridge-candlestick, longbridge-technical,
longbridge-harmonic, longbridge-elliott, longbridge-chanlun, longbridge-smc,
longbridge-fx-carry, longbridge-adr-premium, longbridge-fx

**触发场景：** 实时行情、K线、盘口、资金流、市场温度、汇率、技术分析、ADR溢价

---

### 2. `longbridge-derivatives`

**CLI 命令：**
`option` `warrant`

**退役旧 skills：**
longbridge-derivatives（slug 保留，内容重写）

**触发场景：** 期权链、认购认沽、窝轮、牛熊证、IV、Greeks

---

### 3. `longbridge-fundamentals`

**CLI 命令（13个）：**
`financial-report` `financial-statement` `business-segments` `dividend` `valuation`
`industry-valuation` `operating` `corp-action` `invest-relation` `company`
`executive` `valuation-rank` `compare`

**框架内容（并入 references/）：**
dcf, valuation-methodology, behavioral-finance, value-screen, smallcap-growth

**退役旧 skills：**
longbridge-fundamental, longbridge-financial-report, longbridge-financial-analysis,
longbridge-financial-checkup, longbridge-valuation, longbridge-valuation-rank,
longbridge-peer-comparison, longbridge-operating, longbridge-dividend-screen,
longbridge-basicinfo, longbridge-business-query, longbridge-finance-query,
longbridge-industry-valuation, longbridge-dcf, longbridge-valuation-methodology,
longbridge-behavioral-finance, longbridge-value-screen, longbridge-smallcap-growth

**触发场景：** 财报三表、估值、分红、行业估值、公司信息、DCF、行为金融、低估值筛选

---

### 4. `longbridge-research`

**CLI 命令（12个）：**
`institution-rating` `forecast-eps` `consensus` `finance-calendar` `shareholder`
`fund-holder` `insider-trades` `investors` `short-positions` `short-trades`
`industry-rank` `industry-peers`

**框架内容（并入 references/）：**
investment-ideas, investment-proposal, coverage-initiation, stock-research,
competitive-analysis, thesis-tracker, post-investment, hkipo-analysis,
financial-planning, defi-yield（PR #18）, onchain（PR #18）

**退役旧 skills：**
longbridge-insresearch, longbridge-consensus, longbridge-earnings-revision,
longbridge-analyst-estimates, longbridge-flows, longbridge-ownership,
longbridge-investors, longbridge-calendar,
longbridge-investment-ideas, longbridge-investment-proposal,
longbridge-coverage-initiation, longbridge-stock-research,
longbridge-competitive-analysis, longbridge-thesis-tracker,
longbridge-post-investment, longbridge-hkipo-analysis,
longbridge-financial-planning, longbridge-defi-yield, longbridge-onchain

**触发场景：** 机构评级、目标价、内部人交易、空头、行业排名、投资研究、DeFi收益、链上数据

---

### 5. `longbridge-portfolio`

**CLI 命令（12个）：**
`assets` `cash-flow` `portfolio` `positions` `fund-positions` `margin-ratio`
`max-qty` `profit-analysis` `statement` `bank-cards` `withdrawals` `deposits`

**框架内容（并入 references/）：**
portfolio-diagnosis, portfolio-rebalance, asset-allocation, risk-analysis,
risk-return, performance-attribution, tax-harvesting

**退役旧 skills：**
longbridge-portfolio（slug 保留）, longbridge-positions, longbridge-statement,
longbridge-profit-analysis,
longbridge-portfolio-diagnosis, longbridge-portfolio-rebalance,
longbridge-asset-allocation, longbridge-risk-analysis, longbridge-risk-return,
longbridge-performance-attribution, longbridge-tax-harvesting

**触发场景：** 账户总览、持仓、盈亏、对账单、组合诊断、资产配置、风险分析、绩效归因

---

### 6. `longbridge-orders`

**CLI 命令：**
`order` `dca`

**退役旧 skills：**
longbridge-orders, longbridge-dca

**触发场景：** 下单、撤单、改单、定投

---

### 7. `longbridge-ipo`

**CLI 命令：**
`ipo`（subscriptions / calendar / orders / profit-loss）

**退役旧 skills：**
longbridge-ipo（slug 保留，内容核对更新）

**触发场景：** 新股认购、IPO 日历、打新盈亏

---

### 8. `longbridge-quant`

**CLI 命令：**
`quant`

**框架内容（并入 references/）：**
pairs-trading, volatility-strategy, seasonality, multifactor, factor-research,
factor-screen, correlation, quant-stats, strategy-optimizer, execution-model,
hedging, ml-strategy（PR #18）

**退役旧 skills：**
longbridge-quant（slug 保留）,
longbridge-pairs-trading, longbridge-volatility-strategy, longbridge-seasonality,
longbridge-multifactor, longbridge-factor-research, longbridge-factor-screen,
longbridge-correlation, longbridge-quant-stats, longbridge-strategy-optimizer,
longbridge-execution-model, longbridge-hedging, longbridge-ml-strategy

**触发场景：** 量化脚本、配对交易、波动率策略、多因子选股、机器学习策略、对冲

---

### 9. `longbridge-watchlist`

**CLI 命令：**
`watchlist` `alert` `sharelist`

**退役旧 skills：**
longbridge-watchlist（slug 保留）, longbridge-watchlist-admin,
longbridge-alert, longbridge-sharelist

**注意：** mutating 操作（create/update/delete）保留 dry-run + confirm 协议

**触发场景：** 自选股管理、价格提醒、公开股票清单

---

### 10. `longbridge-content`

**CLI 命令：**
`news` `filing` `topic`

**框架内容（并入 references/）：**
sec-filings

**退役旧 skills：**
longbridge-news, longbridge-sec-filings

**触发场景：** 股票新闻、公告/监管文件、SEC 申报、社区讨论

---

### 11. `longbridge-scanner`

**CLI 命令：**
`screener` `rank` `top-movers` `anomaly` `constituent`

**框架内容（并入 references/）：**
morning-brief, catalyst-radar, event-strategy, event-opportunity,
industry-overview, tech-hype, sector-rotation, sector-monitor,
market-microstructure, supply-chain, etf-analysis, etf-flow

**退役旧 skills：**
longbridge-market-scanner, longbridge-sector-screener,
longbridge-anomaly, longbridge-constituent,
longbridge-morning-brief, longbridge-catalyst-radar,
longbridge-event-strategy, longbridge-event-opportunity,
longbridge-industry-overview, longbridge-tech-hype,
longbridge-sector-rotation, longbridge-sector-monitor,
longbridge-market-microstructure, longbridge-supply-chain,
longbridge-etf-analysis, longbridge-etf-flow

**触发场景：** 策略筛选、热度排名、异动、成分股、晨报、催化剂、事件驱动、ETF分析、产业链

---

## SKILL.md 结构规范

```yaml
---
name: longbridge-<domain>
description: |
  <功能概述>. Triggers: <触发词 ZH-Hans / ZH-Hant / EN>
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

**正文结构（≤ 200 行）：**
```
# Longbridge <Domain>

> Response language directive
> Data-source policy directive

## When to use
## CLI Commands          （每个命令一节，简述 + --help 发现指引）
## Frameworks            （每个框架一节，简述 + 加载对应 references/ 文件）
## Error handling
## MCP fallback
## Related skills
## File layout
```

**约束：**
- 正文 ≤ 200 行；子命令/框架详情放 `references/<name>.md`
- 不硬编码 flag 名，指示 LLM 用 `longbridge <cmd> --help` 发现
- description ≤ 1024 字符
- mutating 操作（watchlist 写）保留 dry-run + confirm 协议

---

## 备份策略

退役的旧 skill 目录在删除前统一备份到 `.deletions/` 目录（已加入 `.gitignore`，不进入版本控制）：

```bash
# 实施前执行
mkdir -p .deletions
for slug in <退役列表>; do
  cp -r skills/$slug .deletions/$slug
done
```

备份目的：实施期间可随时参考旧内容；全量验收通过后可手动清理 `.deletions/`。

---

## 退役 Skill 完整列表（约 96 个）

重构完成后删除以下旧目录（删除前先备份到 `.deletions/`）：

longbridge-quote, longbridge-kline, longbridge-depth, longbridge-capital-flow,
longbridge-market-temp, longbridge-security-list, longbridge-subscriptions,
longbridge-ah-premium, longbridge-index-quote, longbridge-northbound-flow,
longbridge-ichimoku, longbridge-candlestick, longbridge-technical,
longbridge-harmonic, longbridge-elliott, longbridge-chanlun, longbridge-smc,
longbridge-fx-carry, longbridge-adr-premium, longbridge-fx,
longbridge-fundamental, longbridge-financial-report, longbridge-financial-analysis,
longbridge-financial-checkup, longbridge-valuation, longbridge-valuation-rank,
longbridge-peer-comparison, longbridge-operating, longbridge-dividend-screen,
longbridge-basicinfo, longbridge-business-query, longbridge-finance-query,
longbridge-industry-valuation, longbridge-dcf, longbridge-valuation-methodology,
longbridge-behavioral-finance, longbridge-value-screen, longbridge-smallcap-growth,
longbridge-insresearch, longbridge-consensus, longbridge-earnings-revision,
longbridge-analyst-estimates, longbridge-flows, longbridge-ownership,
longbridge-investors, longbridge-calendar,
longbridge-investment-ideas, longbridge-investment-proposal,
longbridge-coverage-initiation, longbridge-stock-research,
longbridge-competitive-analysis, longbridge-thesis-tracker,
longbridge-post-investment, longbridge-hkipo-analysis,
longbridge-financial-planning, longbridge-defi-yield, longbridge-onchain,
longbridge-positions, longbridge-statement, longbridge-profit-analysis,
longbridge-portfolio-diagnosis, longbridge-portfolio-rebalance,
longbridge-asset-allocation, longbridge-risk-analysis, longbridge-risk-return,
longbridge-performance-attribution, longbridge-tax-harvesting,
longbridge-dca, longbridge-watchlist-admin, longbridge-alert, longbridge-sharelist,
longbridge-news, longbridge-sec-filings,
longbridge-market-scanner, longbridge-sector-screener,
longbridge-anomaly, longbridge-constituent,
longbridge-morning-brief, longbridge-catalyst-radar,
longbridge-event-strategy, longbridge-event-opportunity,
longbridge-industry-overview, longbridge-tech-hype,
longbridge-sector-rotation, longbridge-sector-monitor,
longbridge-market-microstructure, longbridge-supply-chain,
longbridge-etf-analysis, longbridge-etf-flow,
longbridge-pairs-trading, longbridge-volatility-strategy, longbridge-seasonality,
longbridge-multifactor, longbridge-factor-research, longbridge-factor-screen,
longbridge-correlation, longbridge-quant-stats, longbridge-strategy-optimizer,
longbridge-execution-model, longbridge-hedging, longbridge-ml-strategy

---

## 验收标准

1. 11 个新 SKILL.md 正文均 ≤ 200 行
2. 每个 skill 覆盖对应命令/框架的触发词（ZH-Hans / ZH-Hant / EN）
3. Response language + Data-source policy 指令存在于每个 SKILL.md
4. 框架内容已迁入 `references/<name>.md`
5. 旧目录已全部删除
6. README / CLAUDE.md / docs/install.md skill 数量更新为 21
7. `well-known-skills-index.json` 和 `index.json` 重新生成
8. `longbridge-watchlist` mutating 操作保留 dry-run + confirm 协议
