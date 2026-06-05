# Skill Consolidation Design — 10+2 Skills（终稿 v4）

**Date:** 2026-06-04  
**Updated:** 2026-06-05  
**Status:** Approved — Final  
**Scope:** 全量 skill 重构

---

## 背景与目标

当前 `skills/` 目录有 127 个 skill，粒度过细。目标：合并为 **10 个 CLI 大方向 skill + 2 个外部贡献 skill**，共 13 个（含基础 skill）。

**关键约束：**
- `description` ≤ 1024 字符（agentskills.io 硬限制），意图族控制在 12 个以内
- SKILL.md 正文 ≤ 200 行，细节迁入 `references/`
- description 语言：简体中文 + 英文为主，繁体只补字形差异词

**最终数量：127 → 13（-90%）**

| 类型 | 数量 |
|---|---|
| 10 个 CLI 大方向 skill | 10 |
| 2 个外部贡献 skill | 2 |
| 基础 `longbridge` skill | 1 |
| **合计** | **13** |

---

## 外部贡献 skill（独立保留）

| Skill | 来源 PR | 说明 |
|---|---|---|
| `longbridge-earnings` | PR #1 / #14 | 合并 earnings + earnings-preview；覆盖财报前瞻和财报后分析，生成 DOCX 报告 |
| `longbridge-value-investing` | PR #24 / #25 / #42 | 合并 graham-screener, graham-stock-analysis, buffett-moat-analyzer, buffett-moat-stock-screener；覆盖格雷厄姆/巴菲特价值投资方法论 |

**并入现有大 skill 的外部贡献：**
- `longbridge-elliott-wave`（PR #28）→ 并入 `longbridge-technical`
- `longbridge-turtle-signal`（PR #36）→ 并入 `longbridge-technical`
- `longbridge-ark-analysis`（PR #29）→ 并入 `longbridge-intel`

---

## 10 个 CLI 大方向 Skill

### 1. `longbridge-market-data`

**CLI 命令（19个）：**
`quote` `depth` `brokers` `trades` `intraday` `kline` `static` `calc-index`
`capital` `market-temp` `trading` `security-list` `participants` `subscriptions`
`ah-premium` `trade-stats` `market-status` `exchange-rate` `ipo`

> `ipo calendar/subscriptions/us-subscriptions` 为公开数据，无需登录；`ipo orders` 需要 🔐 Trade 权限，在 SKILL.md 正文中单独标注。

**框架内容（并入 references/）：**
fx-carry, adr-premium

**退役旧 skills：**
longbridge-quote, longbridge-kline, longbridge-depth, longbridge-capital-flow,
longbridge-market-temp, longbridge-security-list, longbridge-subscriptions,
longbridge-ah-premium, longbridge-index-quote, longbridge-northbound-flow,
longbridge-ipo, longbridge-fx-carry, longbridge-adr-premium, longbridge-fx

**估算 description 意图族：** ~10 个，约 350 字符 ✓

---

### 2. `longbridge-technical`

> 技术分析与原始行情查询是不同用户意图，独立为专属 skill。
> ⚠️ **数据依赖**：本 skill 所有技术分析框架均需 OHLCV 历史数据，通过 `longbridge kline`（market-data skill）获取。SKILL.md 中必须注明此依赖，并引导 LLM 在运行分析前先调用 kline。

**CLI 命令：** 无（纯框架 skill）

**框架内容（并入 references/）：**
ichimoku, candlestick, technical, harmonic, elliott,
chanlun（PR #17）, smc（PR #17）,
elliott-wave（PR #28）, turtle-signal（PR #36）

**退役旧 skills：**
longbridge-ichimoku, longbridge-candlestick, longbridge-technical,
longbridge-harmonic, longbridge-elliott, longbridge-chanlun, longbridge-smc,
longbridge-elliott-wave, longbridge-turtle-signal

**估算 description 意图族：** ~9 个，约 320 字符 ✓

---

### 3. `longbridge-derivatives`

**CLI 命令：**
`option` `warrant`

**退役旧 skills：**
longbridge-derivatives（slug 保留，内容重写）

**估算 description 意图族：** ~4 个，约 180 字符 ✓

---

### 4. `longbridge-fundamentals`

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

**估算 description 意图族：** ~12 个，约 370 字符 ✓

---

### 5. `longbridge-research`

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
longbridge-investors, longbridge-calendar, longbridge-investment-ideas,
longbridge-investment-proposal, longbridge-coverage-initiation,
longbridge-stock-research, longbridge-competitive-analysis,
longbridge-thesis-tracker, longbridge-post-investment,
longbridge-hkipo-analysis, longbridge-financial-planning,
longbridge-defi-yield, longbridge-onchain

**估算 description 意图族：** ~12 个，约 420 字符 ✓

---

### 6. `longbridge-portfolio`

> 原 `longbridge-orders`（`order` + `dca`）并入此 skill。两者均需 Trade 权限，用户心智模型相近。

**CLI 命令（14个）：**
`assets` `cash-flow` `portfolio` `positions` `fund-positions` `margin-ratio`
`max-qty` `profit-analysis` `statement` `bank-cards` `withdrawals` `deposits`
`order` `dca`

> 🔐 以下命令需要 Trade 权限：`positions`, `assets`, `cash-flow`, `order`, `dca`, `statement`, `profit-analysis`, `withdrawals`, `deposits`, `bank-cards`

**框架内容（并入 references/）：**
portfolio-diagnosis, portfolio-rebalance, asset-allocation, risk-analysis,
risk-return, performance-attribution, tax-harvesting

**退役旧 skills：**
longbridge-portfolio（slug 保留）, longbridge-positions, longbridge-statement,
longbridge-profit-analysis, longbridge-orders, longbridge-dca,
longbridge-portfolio-diagnosis, longbridge-portfolio-rebalance,
longbridge-asset-allocation, longbridge-risk-analysis, longbridge-risk-return,
longbridge-performance-attribution, longbridge-tax-harvesting

**估算 description 意图族：** ~11 个，约 360 字符 ✓

---

### 7. `longbridge-quant`

> 本 skill 以量化框架为主体，CLI `quant` 命令（运行指标脚本）为辅助工具。SKILL.md 结构调整为：`## CLI: quant` 单独一节（简述 + --help 指引），其余内容以 `## Quantitative Frameworks` 组织。

**CLI 命令：**
`quant`（运行指标脚本，基于 kline 数据）

**框架内容（并入 references/）：**
pairs-trading, volatility-strategy, seasonality, multifactor, factor-research,
factor-screen, correlation, quant-stats, strategy-optimizer, execution-model,
hedging, ml-strategy（PR #18）

**退役旧 skills：**
longbridge-quant（slug 保留）, longbridge-pairs-trading, longbridge-volatility-strategy,
longbridge-seasonality, longbridge-multifactor, longbridge-factor-research,
longbridge-factor-screen, longbridge-correlation, longbridge-quant-stats,
longbridge-strategy-optimizer, longbridge-execution-model, longbridge-hedging,
longbridge-ml-strategy

**估算 description 意图族：** ~9 个，约 320 字符 ✓

---

### 8. `longbridge-watchlist`

**CLI 命令：**
`watchlist` `alert` `sharelist`

> mutating 操作（create/update/delete）保留 dry-run + confirm 协议。

**退役旧 skills：**
longbridge-watchlist（slug 保留）, longbridge-watchlist-admin,
longbridge-alert, longbridge-sharelist

**估算 description 意图族：** ~3 个，约 150 字符 ✓

---

### 9. `longbridge-content`

**CLI 命令：**
`news` `filing` `topic`

**框架内容（并入 references/）：**
sec-filings

**退役旧 skills：**
longbridge-news, longbridge-sec-filings

**估算 description 意图族：** ~4 个，约 180 字符 ✓

---

### 10. `longbridge-intel`

**CLI 命令：**
`screener` `rank` `top-movers` `anomaly` `constituent`

**框架内容（并入 references/）：**
morning-brief, catalyst-radar, event-strategy, event-opportunity,
industry-overview, tech-hype, sector-rotation, sector-monitor,
market-microstructure, supply-chain, etf-analysis, etf-flow,
ark-analysis（PR #29）

**退役旧 skills：**
longbridge-market-scanner, longbridge-sector-screener, longbridge-anomaly,
longbridge-constituent, longbridge-morning-brief, longbridge-catalyst-radar,
longbridge-event-strategy, longbridge-event-opportunity, longbridge-industry-overview,
longbridge-tech-hype, longbridge-sector-rotation, longbridge-sector-monitor,
longbridge-market-microstructure, longbridge-supply-chain,
longbridge-etf-analysis, longbridge-etf-flow, longbridge-ark-analysis

**估算 description 意图族：** ~12 个，约 380 字符 ✓

---

## SKILL.md 结构规范

```yaml
---
name: longbridge-<domain>
description: |
  <功能概述>. Triggers: <触发词 ZH-Hans + EN，繁体仅补差异字>
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: read_only | account_read | mutating
  requires_login: false | true   # 只要有任一命令需要登录即为 true
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
## Sub-topic Routing      ← 必须：查询意图 → references/ 文件映射表
## CLI Commands           （每个命令简述；需要 🔐 Trade 权限的单独标注）
## Frameworks             （每个框架简述 + 加载对应 references/ 文件）
## Auth requirements      ← 汇总列出哪些命令/操作需要登录及权限级别
## Error handling
## MCP fallback
## Related skills         ← 必须：与相邻 skill 的路由边界
## File layout
```

**特殊情况：**
- **纯框架 skill**（如 `longbridge-technical`）：去掉 `## CLI Commands`，改为 `## Data dependency`，注明需要哪个 skill 的命令获取数据
- **框架为主的 skill**（如 `longbridge-quant`）：`## CLI Commands` 简化为 `## CLI: <command-name>`，保留但不展开

**约束：**
- 正文 ≤ 200 行；详情放 `references/<name>.md`
- description ≤ 1024 字符，意图族 ≤ 12 个
- 不硬编码 flag 名，用 `longbridge <cmd> --help` 发现
- mutating 操作保留 dry-run + confirm 协议

---

## 关键路由边界

| 用户意图 | 正确 skill | 容易混淆 |
|---|---|---|
| "NVDA 一目均衡表" | longbridge-technical | longbridge-market-data |
| "NVDA K线数据" | longbridge-market-data | longbridge-technical |
| "NVDA DCF 估值" | longbridge-fundamentals | longbridge-research |
| "NVDA 机构评级" | longbridge-research | longbridge-fundamentals |
| "NVDA 季报分析" | longbridge-earnings（外部）| longbridge-research |
| "财报前要关注什么" | longbridge-earnings（外部）| longbridge-research |
| "格雷厄姆/巴菲特选股" | longbridge-value-investing（外部）| longbridge-fundamentals |
| "ARK 颠覆式创新" | longbridge-intel | longbridge-research |
| "艾略特波浪/海龟交易" | longbridge-technical | longbridge-quant |
| "我的订单/定投" | longbridge-portfolio | longbridge-watchlist |
| "组合风险分析" | longbridge-portfolio | longbridge-research |
| "ETF 成分股" | longbridge-intel | longbridge-market-data |
| "IPO 日历" | longbridge-market-data | longbridge-intel |
| "港股打新" | longbridge-market-data（ipo命令）| longbridge-research（hkipo-analysis）|
| "期权波动率" | longbridge-derivatives | longbridge-technical |

---

## 备份策略

退役的旧 skill 目录在删除前统一备份到 `.deletions/`（已加入 `.gitignore`）：

```bash
mkdir -p .deletions
for slug in <退役列表>; do
  cp -r skills/$slug .deletions/$slug
done
```

---

## 退役 Skill 完整列表（约 105 个）

**market-data 退役：**
longbridge-quote, longbridge-kline, longbridge-depth, longbridge-capital-flow,
longbridge-market-temp, longbridge-security-list, longbridge-subscriptions,
longbridge-ah-premium, longbridge-index-quote, longbridge-northbound-flow,
longbridge-ipo, longbridge-fx-carry, longbridge-adr-premium, longbridge-fx

**technical 退役：**
longbridge-ichimoku, longbridge-candlestick, longbridge-technical,
longbridge-harmonic, longbridge-elliott, longbridge-chanlun, longbridge-smc,
longbridge-elliott-wave, longbridge-turtle-signal

**fundamentals 退役：**
longbridge-fundamental, longbridge-financial-report, longbridge-financial-analysis,
longbridge-financial-checkup, longbridge-valuation, longbridge-valuation-rank,
longbridge-peer-comparison, longbridge-operating, longbridge-dividend-screen,
longbridge-basicinfo, longbridge-business-query, longbridge-finance-query,
longbridge-industry-valuation, longbridge-dcf, longbridge-valuation-methodology,
longbridge-behavioral-finance, longbridge-value-screen, longbridge-smallcap-growth

**research 退役：**
longbridge-insresearch, longbridge-consensus, longbridge-earnings-revision,
longbridge-analyst-estimates, longbridge-flows, longbridge-ownership,
longbridge-investors, longbridge-calendar, longbridge-investment-ideas,
longbridge-investment-proposal, longbridge-coverage-initiation,
longbridge-stock-research, longbridge-competitive-analysis,
longbridge-thesis-tracker, longbridge-post-investment,
longbridge-hkipo-analysis, longbridge-financial-planning,
longbridge-defi-yield, longbridge-onchain

**portfolio 退役：**
longbridge-positions, longbridge-statement, longbridge-profit-analysis,
longbridge-orders, longbridge-dca,
longbridge-portfolio-diagnosis, longbridge-portfolio-rebalance,
longbridge-asset-allocation, longbridge-risk-analysis, longbridge-risk-return,
longbridge-performance-attribution, longbridge-tax-harvesting

**quant 退役：**
longbridge-pairs-trading, longbridge-volatility-strategy, longbridge-seasonality,
longbridge-multifactor, longbridge-factor-research, longbridge-factor-screen,
longbridge-correlation, longbridge-quant-stats, longbridge-strategy-optimizer,
longbridge-execution-model, longbridge-hedging, longbridge-ml-strategy

**watchlist 退役：**
longbridge-watchlist-admin, longbridge-alert, longbridge-sharelist

**content 退役：**
longbridge-news, longbridge-sec-filings

**intel 退役：**
longbridge-market-scanner, longbridge-sector-screener, longbridge-anomaly,
longbridge-constituent, longbridge-morning-brief, longbridge-catalyst-radar,
longbridge-event-strategy, longbridge-event-opportunity, longbridge-industry-overview,
longbridge-tech-hype, longbridge-sector-rotation, longbridge-sector-monitor,
longbridge-market-microstructure, longbridge-supply-chain,
longbridge-etf-analysis, longbridge-etf-flow, longbridge-ark-analysis

**外部 PR 退役（内容合并）：**
longbridge-earnings-preview,
longbridge-graham-screener, longbridge-graham-stock-analysis,
longbridge-buffett-moat-analyzer, longbridge-buffett-moat-stock-screener

---

## 验收标准

1. 10 个新 SKILL.md 正文均 ≤ 200 行，description ≤ 1024 字符
2. 每个 skill 包含 `## Sub-topic Routing` 映射表
3. 每个 skill 包含 `## Auth requirements` 说明哪些命令需要登录
4. `longbridge-technical` 包含 `## Data dependency` 注明依赖 `longbridge kline`
5. `longbridge-quant` 的 CLI 部分改为 `## CLI: quant`，框架部分改为 `## Quantitative Frameworks`
6. 每个 skill 覆盖对应命令/框架的触发词（ZH-Hans + EN，繁体补差异字）
7. Response language + Data-source policy 指令存在于每个 SKILL.md
8. `## Related skills` 写明与相邻 skill 的路由边界
9. 框架内容已迁入 `references/<name>.md`
10. 旧目录已全部删除（删除前备份到 `.deletions/`）
11. README / CLAUDE.md / docs/install.md skill 数量更新为 13
12. `well-known-skills-index.json` 和 `index.json` 重新生成，包含旧 slug → 新 slug 映射说明
13. `longbridge-watchlist` mutating 操作保留 dry-run + confirm 协议
14. 外部贡献 skill `longbridge-earnings` 和 `longbridge-value-investing` 的 description / Related skills 更新以反映与新 10 个 skill 的路由边界
