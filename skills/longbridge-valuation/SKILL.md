---
name: longbridge-valuation
description: |
  Valuation analysis for a single stock via the Longbridge MCP — current PE / PB / PS / EV-EBITDA snapshot, historical percentile (1–3 years), industry median + relative premium, industry rank. Returns data, never a buy/sell call. Triggers: "估值贵不贵", "是不是被低估", "PE 历史百分位", "PB 分位", "行业溢价", "行业折价", "X 现在适合买不", "估值水平", "估值貴不貴", "是否被低估", "PE 歷史分位", "行業溢價", "行業折價", "is X expensive", "is X undervalued", "PE percentile", "industry valuation premium", "valuation snapshot".
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: read_only
  requires_login: false
  default_install: true
  requires_mcp: true
  tier: analysis
---

# longbridge-valuation

Prompt-only analysis skill. Orchestrates Longbridge MCP tools to answer *"is X expensive?"* with three dimensions: current snapshot, historical percentile, industry context. **No `cli.py`** — this skill works only when MCP is configured.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## Prerequisite (mandatory)

```bash
claude mcp add --transport http longbridge https://openapi.longbridge.com/mcp
```

First MCP call triggers OAuth in the browser (`quote` scope is enough for this skill).

## When to use

- *"NVDA 估值贵不贵"*, *"is NVDA expensive?"*, *"NVDA 估值貴不貴"*
- *"茅台是不是被低估了"*, *"is Maotai undervalued?"*
- *"700 估值在历史什么位置"*, *"700 historical PE percentile"*
- *"宁德时代相对行业贵多少"*, *"how much does CATL trade above industry median"*
- *"GOOG 现在适合买入吗"* (valuation lens, **no buy/sell verdict**)

For multi-symbol comparison route to `longbridge-peer-comparison`. For business-fundamentals questions route to `longbridge-fundamental`.

## Workflow

1. **Confirm MCP is ready** — if `claude mcp list` lacks `longbridge`, prompt the user to add it (this skill has no CLI fallback).
2. **Resolve symbol** to `<CODE>.<MARKET>` (rules in `longbridge-quote`). Multiple symbols → route to `longbridge-peer-comparison`.
3. **Concurrently call** four MCP tools:

   ```
   mcp__longbridge__valuation(symbol=X)
   mcp__longbridge__valuation_history(symbol=X)        # ≥ 1y, prefer 3y
   mcp__longbridge__industry_valuation(symbol=X)
   mcp__longbridge__industry_valuation_dist(symbol=X)
   ```

   Optional intraday correction (only when needed): `mcp__longbridge__calc_indexes(symbol=X, indexes="pe,pb")` — `valuation` is often EOD; `calc_indexes` reflects the live mid-day price.

4. **Compute** in the LLM:

   | Quantity | Method |
   |---|---|
   | Historical PE percentile | rank current PE against `valuation_history` series |
   | Historical PB percentile | same |
   | Industry premium | `(current PE − industry median PE) / industry median PE` |
   | Industry rank | bucket from `industry_valuation_dist` |

   If history is sparse (< 1y) or the industry has fewer than 5 peers, **degrade gracefully** — show snapshot + relative-to-industry only, drop the percentile claim.

5. **Output the three sections** (template below). Cite **Longbridge Securities**.

## Output template

```
{Symbol} ({code}) valuation snapshot — Source: Longbridge Securities

[Current snapshot]
- PE (TTM): X
- PB:        X
- PS:        X
- EV/EBITDA: X (if available)
- Dividend yield: X%

[Historical (past 3y)]
- PE in N-th percentile (low / mid / high)
- PB in N-th percentile

[Industry (N peers)]
- Industry median PE: X → currently {premium/discount} of N%
- Industry rank: {position} / N (high / mid / low bucket)

[Combined]
From historical + industry views, valuation is {low / neutral / high} — historical N-th pct, {N% above/below} industry median.

⚠️ High valuation does not imply "do not buy" — growth stocks frequently sustain high multiples. This is data, not investment advice.
```

(Translate into the user's language; keep numeric values as-is.)

## Cyclical industries — special handling

Energy / chemicals / steel / shipping / banks / property are cyclical: PE inverts (high PE near troughs because earnings are depressed; low PE near peaks may signal a top). When the symbol is in such an industry, **add the caveat**: *"Cyclical industry — PE percentile must be interpreted alongside industry cycle position; do not read 'high PE = expensive' mechanically."*

## Output constraints

- **Must** include three dimensions (snapshot + historical + industry); state "data unavailable" if a dimension fails.
- **Must** cite "Longbridge Securities" / "数据来源:长桥证券" / "數據來源:長橋證券".
- **Must** end with the not-investment-advice disclaimer.
- **Do not** say "I recommend buying / selling".
- **Do not** predict future PE.
- **May** characterise combinations like "high-historical + high-industry" as a recognised hedge phrase, but qualify.

## Error handling

| Situation | Reply |
|---|---|
| MCP `longbridge` not configured | Prompt for `claude mcp add ...` |
| Auth / unauthorised | Re-trigger MCP OAuth |
| `valuation` empty | "{symbol} has no valuation data (likely an obscure or newly listed name)." |
| `valuation_history` < 1 year | Degrade to snapshot + industry-only |
| Industry < 5 peers | Caveat: "industry sample sparse; industry percentile is indicative only" |

## MCP toolbelt

| MCP tool | What it returns |
|---|---|
| `mcp__longbridge__valuation` | Current valuation snapshot |
| `mcp__longbridge__valuation_history` | Historical valuation series for percentile calc |
| `mcp__longbridge__industry_valuation` | Industry mean / median |
| `mcp__longbridge__industry_valuation_dist` | Industry percentile buckets |
| `mcp__longbridge__latest_financial_report` | Optional EPS/BPS cross-check |
| `mcp__longbridge__calc_indexes` | Optional intraday PE correction |

## Related skills

- 2–5 symbol valuation comparison → `longbridge-peer-comparison`
- Business fundamentals (revenue, ROE, margins) → `longbridge-fundamental`
- News / market reaction → `longbridge-news`
- Real-time price alert → `mcp__longbridge__alert_add` directly

## File layout

```
longbridge-valuation/
└── SKILL.md          # prompt-only, no scripts/
```
