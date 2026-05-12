# Output template — leaderboard + summary + data-source appendix

Loaded on demand by `longbridge-graham-screener`. Use the section order verbatim. Field names should be translated to match the user's input language (Simplified Chinese / Traditional Chinese / English).

---

## Layout

```
Graham Cigar-Butt Screener — {Market} / {Universe}
As-of: {YYYY-MM-DD HH:MM TZ}   Currency: {HKD / USD / CNY}
Filters: NCAV<{1.0|1.5}, PE<{10}, PB<{1.5}, Div>{3%}, CA/TL>{2.0}, ≥5y no-loss
Universe size: {N}   Hard-filter pass: {M}   Dynamic-clean: {K}

[Leaderboard — Top {10|20}]
┌──────┬──────────┬──────────┬─────────┬─────────────┬──────────┬──────┬──────┬────────┬─────────────┬──────────────────────────┬────────────┐
│ Rank │ Code     │ Name     │ Static  │ Adjusted    │ NCAV     │ PE   │ PB   │ Div Yd │ Graham Buy  │ Dynamic Warning          │ Data Note  │
├──────┼──────────┼──────────┼─────────┼─────────────┼──────────┼──────┼──────┼────────┼─────────────┼──────────────────────────┼────────────┤
│ 1    │ 0XXX.HK  │ Example  │ 82/100  │ 74/100 🟡   │ 0.61x    │ 7.2  │ 0.92 │ 4.50%  │ ≤ 2.27      │ NCAV 轻微收窄             │ —          │
│ 2    │ ...      │ ...      │ ...     │ ...         │ ...      │ ...  │ ...  │ ...    │ ...         │ ...                      │ ...        │
│ ...                                                                                                                                          │
└──────┴──────────┴──────────┴─────────┴─────────────┴──────────┴──────┴──────┴────────┴─────────────┴──────────────────────────┴────────────┘

Tier legend: 🟢 80–100 cigar-butt grade  ·  🟡 60–79 undervalued  ·  🟠 40–59 fair value  ·  🔴 0–39 / value-trap override

[Market Summary]
- Universe scanned: {N} symbols ({INDEX} constituents, as-of {date})
- Hard filters passed: {M} ({pct}% of universe)
- Dynamic layer clean (no value-trap flag): {K}
- Top-N average dividend yield: {X}% — "持有等待期间每年可获约 {X}% 股息回报作为补偿"
- Cohorts noted: {n_financials} financial-sector (PB/CAR/solvency model) · {n_ipo} IPO < 2y (pro-rated stability) · {n_suspended} suspended (last-trade snapshot)
- Reconciliation drops: {n_dropped} symbol(s) — see Data Anomaly footer below

[Substitute-Model Rows]
(Repeat for any 🏦 / 🛡 / 🏢 rows, since the leaderboard's NCAV column is N/A for them.)
| Code | Name | Sector | Substitute model | PB | Div Yd | CET1 / Solvency / LTV | Score |

[Data Anomaly Footer — rows dropped from leaderboard]
| Code | Failing reconciliation check | Gap | Action |
|---|---|---|---|
| 0YYY.HK | Current-assets sum vs reported total | +5.8% | Dropped — recommend manual review |

[Next-step Recommendation]
- For any candidate you want to act on, run `longbridge-graham-stock-analysis <CODE>` for a single-stock deep diagnostic (8-section report, includes value-trap rule-by-rule check and liquidation-value table).
- Reminder: this screener applies static hard filters + general dynamic factors; it does NOT capture company-specific qualitative traps (regulatory shock, fraud, niche-product obsolescence). Treat as a candidate list, not a buy list.

[Optional Hooks]
- Image card: «港股捡烟蒂 TOP10 / HK Cigar-Butt TOP10» — 带长桥品牌
- Subscription: «每周推送本榜单 / Weekly leaderboard push» (opt-in)

[Data Source Appendix — MANDATORY]
Every figure in the leaderboard, summary, and substitute-model rows must be traceable to one of the rows below.

| Field group                       | Source                                                | Fetch (UTC)        | Period             | Notes |
|-----------------------------------|-------------------------------------------------------|--------------------|--------------------|-------|
| Constituent list                  | Longbridge `constituent <INDEX>`                      | YYYY-MM-DD HH:MM   | Live               | {N} symbols |
| Snapshot (PE / PB / market cap)   | Longbridge `calc-index` + `quote`                     | YYYY-MM-DD HH:MM   | Live               | — |
| Dividend (TTM cash dividend)      | Longbridge `dividend`                                 | YYYY-MM-DD HH:MM   | TTM                | — |
| Balance-sheet items (NCAV inputs) | Longbridge `financial-report --kind BS --report af`   | YYYY-MM-DD HH:MM   | FY{YYYY} annual    | Per-symbol |
| NCAV trajectory (last 4Q)         | Longbridge `financial-statement --kind BS --report qf`| YYYY-MM-DD HH:MM   | Q{X}–Q{X+3} {YYYY} | Used for value-trap rule 1 |
| Income statement (5y no-loss)     | Longbridge `financial-report --kind IS --report af`   | YYYY-MM-DD HH:MM   | FY{YYYY-4}–FY{YYYY}| Pro-rated for IPO<2y |
| Operating cash flow (4Q)          | Longbridge `financial-report --kind CF --report qf`   | YYYY-MM-DD HH:MM   | Last 4Q            | Value-trap rule 4 |
| Major-holder / insider flow       | Longbridge `ownership` + `insresearch`                | YYYY-MM-DD HH:MM   | Last 2Q            | Value-trap rule 2 |
| Industry PMI / inventory cycle    | WebSearch — {Publisher}, {article date}, {URL}        | YYYY-MM-DD HH:MM   | {month YYYY}       | [substituted — Longbridge gap] |
| Capacity utilisation              | WebSearch — {Publisher}, {article date}, {URL}        | YYYY-MM-DD HH:MM   | {month YYYY}       | [substituted — Longbridge gap] |
| Bank CET1 / Insurance solvency / REIT NAV | WebSearch — {Publisher}, {date}, {URL}        | YYYY-MM-DD HH:MM   | {YYYY}             | Substitute-model rows only |
| (One row per WebSearch hit)       | …                                                     | …                  | …                  | … |

Footnote conventions:
- Every WebSearch row must carry publisher + URL + article date + access date.
- Any Longbridge field substituted via WebSearch is tagged `[substituted — Longbridge gap]`.
- Any row dropped at the reconciliation gate is named in the **Data Anomaly Footer** with the failing check and the gap; it is NOT silently removed.
- Cohort tags ("🏦 Bank — PB+CAR model", "⏸ Suspended", "数据局限 / IPO < 2y") must appear in the row's Data Note column AND be summarised in the Market Summary cohort line.
```

---

## Disclaimer (mandatory, end of every output)

```
⚠️ 免责声明：本筛选器由长桥 AI 基于格雷厄姆价值投资方法论自动生成，仅供参考，不构成投资建议。
   筛选器仅应用了静态硬指标与通用动态因子，未考虑公司层面的主观估值陷阱（监管冲击、舞弊、产品周期等）。
   格雷厄姆策略通常需要 1–3 年以上的持有周期才可能兑现。请在做出任何投资决策前进行独立研究，
   并考虑自身资金使用周期和风险承受能力。命中候选请用 `longbridge-graham-stock-analysis` 做单股深度诊断。

⚠️ 免責聲明：本篩選器由長橋 AI 基於格雷厄姆價值投資方法論自動生成，僅供參考，不構成投資建議。
   篩選器僅應用靜態硬指標與通用動態因子，未考量公司層面之主觀估值陷阱。
   格雷厄姆策略通常需要 1–3 年以上的持有週期方可兌現。請於投資決策前獨立研究，
   並結合自身資金週期與風險承受能力。命中候選請以 `longbridge-graham-stock-analysis` 做單股深度診斷。

⚠️ Disclaimer: This screener is generated by Longbridge AI using Graham's value-investing framework.
   For reference only — not investment advice. It applies static hard filters plus general dynamic
   factors only; it cannot capture company-specific qualitative traps (regulatory shocks, fraud,
   product-cycle obsolescence). Graham strategies typically need a 1–3 year holding period before
   value is realised. Do your own research and align with your capital horizon and risk tolerance.
   For any candidate, follow up with `longbridge-graham-stock-analysis` for a single-stock deep diagnostic.
```
