---
name: longbridge-catalyst-radar
description: |
  Watchlist catalyst radar — monitors the user's Longbridge watchlist and produces incremental morning / evening briefings. Scans 7 catalyst dimensions (earnings surprises, regulatory changes, abnormal capital flow, insider trades, analyst upgrades / downgrades, corporate events, sentiment / technicals) across HK / US / A-share / SG markets. Groups by market with the next-to-open market first. Triggers: "晨报", "晚报", "早报", "复盘", "今天有什么要关注的", "自选股有什么消息", "全景扫描", "档案卡", "晨報", "晚報", "早報", "複盤", "今天有什麼要關注", "自選股有什麼消息", "全景掃描", "檔案卡", "morning briefing", "evening briefing", "catalyst update", "catalyst radar", "watchlist update", "what's new on my watchlist".
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: account_read
  requires_login: true
  default_install: true
  requires_mcp: true
  tier: analysis
---

# Catalyst Radar

Watchlist event monitor that screens the noise and surfaces catalysts the user actually needs to act on. **Output is data, not advice** — no buy/sell calls, no price predictions; the skill discovers signals, ranks importance, and presents them.

> **Response language**: match the user's input language — Simplified Chinese (简体中文) / Traditional Chinese (繁體中文) / English. Briefing templates in [references/briefing-templates.md](references/briefing-templates.md) are written with Chinese as the primary, but can be rendered in any language.

## Prerequisites

- **Longbridge CLI** installed + `longbridge login` (read-only; trade scope optional but enables positions-weighted prioritisation).
- **Longbridge MCP** (recommended for fundamentals / news / community signals):
  ```bash
  claude mcp add --transport http longbridge https://openapi.longbridge.com/mcp
  ```

## Data sources, in priority order

1. **CLI (preferred)**: `longbridge <command>` — structured output, lowest latency.
2. **MCP (secondary)**: `https://openapi.longbridge.com/mcp` — when CLI lacks coverage (fundamentals deep dives, community topics, news classification).
3. **Web Search (fallback)**: only for policy interpretation, short-seller reports, rumour events, or notable-investor moves that neither CLI nor MCP capture.

## Core principles

**Push only changes; never re-state known signals.** Every output is incrementally filtered — if a signal was pushed yesterday and there is no new development, it does not reappear today.

**Group by market.** The market closest to its next open comes first.

**Three severity tiers**:
- 🔴 **Critical** (0–3 items): must-know today.
- 🟡 **Watch** (3–8 items): noteworthy changes, one line each.
- 🟢 **Quiet**: no new signals.

## Intent classification

After receiving the user's command, classify the intent first. Full rules in [references/intent-mapping.md](references/intent-mapping.md).

| Intent | Example triggers | Action |
|---|---|---|
| 1. View briefing (default) | "晨报", "今天有什么", "morning briefing" | Full-market scan → template 1 |
| 2. View specific market | "A股有什么信号", "港股早报" | Single-market scan → template 2 |
| 3. View specific stock | "NVDA 最近怎么样", "看看茅台" | Per-symbol full_scan → ad-hoc format |
| 4. Full profile snapshot | "全景扫描 NVDA", "腾讯档案卡" | 7-dimension scan → profile-card format |
| 5. Manage watchlist | "把 PDD 加到自选", "删掉 SE" | Defer to `longbridge-watchlist-admin` |
| 6. Adjust settings | "灵敏度调高", "A股只看早报" | Update user preferences |
| 7. Look back | "上周 NVDA 有哪些信号", "回顾一下" | Retrieve history |
| 8. Cross-market spillover | "美股半导体大涨 A 股哪些受影响" | Linkage analysis → template 4 |

**Default**: when the intent is unclear, treat it as intent 1 (briefing).

## Execution flow

**Step 1: Parse intent** — see [references/intent-mapping.md](references/intent-mapping.md) for the priority rules.

**Step 2: Load context** —
- Watchlist API → user's watchlist (live, no local cache); chain to `longbridge-watchlist`.
- Positions API → holdings, used to weight relevance; chain to `longbridge-positions`.

**Step 3: Fetch data** — CLI first, MCP next, Web Search as fallback. Per-API parameter map in [references/longbridge-api-map.md](references/longbridge-api-map.md).

Batch-scan strategy for ~100 watchlist symbols, tiered:
- High priority (~10): `full_scan`, 8–12 API calls each
- Medium priority (~30): `quick_scan`, 3–4 calls each
- Low priority (~60): `quote_only`, 1 call each
- Total ~280 calls, target completion within 30 seconds.

**Step 4: Score & tier** — combine trigger dimension, importance, recency, and overlap with the user's holdings → 🔴 / 🟡 / 🟢.

**Step 5: Render** — group by market (next-to-open first), apply the relevant template from [references/briefing-templates.md](references/briefing-templates.md).

## Seven-dimension scan framework

Each symbol is scanned across these 7 dimensions; data is sourced via the Longbridge APIs (CLI / MCP).

| Dimension | US | A-share | HK | SG |
|---|:---:|:---:|:---:|:---:|
| 1. Financials & earnings | ✅ | ✅ | ✅ | ✅ |
| 2. Capital & flow | ✅ (incl. options) | ✅* (龙虎榜 / 北向 / 融资融券) | ✅* (CCASS / 沽空 / 窝轮) | ✅ |
| 3. Insider & institutional | ✅ | ✅ | ✅ | ⚠️ |
| 4. Policy & regulation | ✅ | ✅ | ✅ | ✅ |
| 5. Corporate events | ✅ | ✅ | ✅ | ✅ |
| 6. Market sentiment | ✅ | ✅ | ✅ | ⚠️ |
| 7. Technicals | ✅ | ✅ | ✅ | ✅ |

✅ = full · ✅\* = with market-specific signals · ⚠️ = partial

**Market-specific signals**:
- **A-share**: 龙虎榜 (Top-traders), 北向资金 (Northbound), 涨跌停板 (Limit-up/down), 两融余额 (Margin balance)
- **HK**: CCASS holdings shifts, sell-short ratio, warrant / CBBC street stock, 南向资金 (Southbound)
- **SG**: market data complete; analyst coverage and community data are relatively thin.

## Related skills (chain when needed)

| User intent | Route to |
|---|---|
| Live quote / valuation indices for a single name | `longbridge-quote` |
| Recent news / filings / community sentiment for a single name | `longbridge-news` |
| Historical PE / industry percentiles | `longbridge-valuation` |
| Earnings detail (5-dimension KPIs) | `longbridge-fundamental` |
| Multi-symbol comparison after spotting a sector signal | `longbridge-peer-comparison` |
| Account-level P&L / contribution | `longbridge-portfolio` |
| Watchlist read | `longbridge-watchlist` |
| Watchlist mutations (add / remove / rename) | `longbridge-watchlist-admin` |
| Capital flow on a specific symbol | `longbridge-capital-flow` |
| Orderbook / brokers / ticks | `longbridge-depth` |

## Reference files

| File | Purpose | Read when |
|---|---|---|
| [references/longbridge-api-map.md](references/longbridge-api-map.md) | Per-dimension Longbridge API call rules, parameters, return fields | Before fetching data |
| [references/briefing-templates.md](references/briefing-templates.md) | Four Markdown briefing templates + fill rules | Before rendering output |
| [references/intent-mapping.md](references/intent-mapping.md) | 8 user intents, trigger phrases, priority rules | While parsing the user prompt |

## File layout

```
longbridge-catalyst-radar/
├── SKILL.md
└── references/
    ├── longbridge-api-map.md
    ├── briefing-templates.md
    └── intent-mapping.md
```

Prompt-only — no `scripts/`. Catalyst data assembly is done by the LLM orchestrating CLI / MCP / WebSearch calls live; nothing is cached locally.
