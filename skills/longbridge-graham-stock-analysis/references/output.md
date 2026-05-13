# Output template — 8 fixed sections + data-source appendix

Loaded by `longbridge-graham-stock-analysis` SKILL.md on demand. Use the section order below verbatim. Field names should be translated to match the user's input language (Simplified Chinese / Traditional Chinese / English).

> **Reconciliation note**: 勾稽校验 (cross-statement reconciliation) is an **internal correctness gate**, not a user-facing section. Do NOT print the check table, do NOT add a "✅ 勾稽通过" line anywhere in the output. The check runs silently before scoring. It only becomes user-visible in two cases:
> 1. **Fail (gap > tolerance)** → emit a halt message instead of a score, naming the failing check and the gap; do not produce sections [1]–[7].
> 2. **Within-tolerance residual that matters** → add a one-line note in the relevant **Data Source Appendix** row only (e.g. "BS current-assets sum −1.4% vs reported total — within tolerance"). Do not surface it in the body.

---

## Layout (passing case — scores emitted)

```
{Symbol} ({code}) — Graham Cigar-Butt Diagnostic
As-of: {date}   Currency: {ccy}   Source: Longbridge Securities + WebSearch (see appendix)

[1] Adjusted score card
     ┌──────────────────────────┐
     │   Adjusted score: 64 🟡  │
     │   Tier: Undervalued      │
     └──────────────────────────┘
     Static score:        82
     Dynamic adjustment:  −18
       · Industry downturn:                   −8
       · NCAV 3-quarter shrinkage:            −7
       · Mild insider selling:                −3
     One-line verdict: "Cheap on the surface — but watch the trend."


[2] Six-dimension static breakdown
| Dimension          | Value     | Threshold        | Score |
|--------------------|-----------|------------------|-------|
| NCAV ratio         | 0.71x     | < 0.67 full      | 22/25 |
| PE (TTM)           | 8.4       | < 10 full        | 20/20 |
| PB                 | 0.92      | < 1.0 full       | 15/15 |
| Dividend yield     | 4.3%      | > 5% full        | 13/15 |
| Debt coverage      | 1.7       | > 2.0 full       | 10/15 |
| Earnings stability | 4y no-loss| 5y full          | 8/10  |
| Total              |           |                  | 88/100 → 82 capped |


[3] Dynamic adjustment detail
- Industry cycle: <industry> PMI <value> for <period> → downturn.
  Inventory haircut tightened 50% → 30%; AR 75% → 55%. NCAV rescored.
  → −8
- Earnings trend: last 4 quarters EPS direction <…>. → <±N>
- Insider / market signal: <holder> reported <action> on <date>. → <±N>
- Balance-sheet trajectory: NCAV per share over last 3 quarters: 2.31 → 1.98 → 1.72. ×0.8 multiplier and warn. → −7
- Value-trap rules tripped: <list rules 1–5 with current state>; verdict: <pass / 1-flag watch / 2+ flags = VALUE TRAP>


[4] Holding-period view
- Catalysts present: <buyback / privatisation / spin-off / activist / none>
- Waiting cost: dividend yield 4.3% — pays you to wait ✅ (>3%)
- Expected horizon: 1–3 years (sector re-rating scenario) — confirm with user
- If no catalyst + low dividend: tag "requires high holding patience"


[5] Liquidation-value table (默认 vs 行业调整)
| Asset class               | Book      | Default % | Adjusted % | Liquidation value | Note |
|---------------------------|-----------|-----------|------------|-------------------|------|
| Cash & equivalents        | 120.5B    | 100%      | 100%       | 120.5B            | Highest quality |
| Accounts receivable       | 45.2B     | 75%       | 55% ↓      | 24.9B             | Industry downturn — bad-debt risk up |
| Inventory                 | 28.6B     | 50%       | 30% ↓      | 8.6B              | Inventory cycle down — deeper discount |
| Other current assets      | 12.1B     | 25%       | 25%        | 3.0B              | No adjustment |
| Total current (adjusted)  | —         | —         | —          | 157.0B            | 14.7B below default |
| Short-term debt           | (63.4B)   | 100%      | 100%       | (63.4B)           | Full deduction |
| Long-term debt            | (88.9B)   | 100%      | 100%       | (88.9B)           | Full deduction |
| **Adjusted NCAV**         |           |           |            | **4.7B**          | NCAV/sh = 0.56 |
| Default NCAV (reference)  |           |           |            | 19.4B             | NCAV/sh = 2.31 |
| Current price             |           |           |            | 1.68 / share      | Adjusted margin 0.33x ⚠️ |


[6] Safety-margin price band
  Current price:        1.68
  Default NCAV line:    2.31  ─── "cheap on default haircuts"
  Adjusted NCAV line:   0.56  ─── "cheap after industry haircut"
  Graham buy line:      0.38  ─── adjusted NCAV × 0.67


[7] Three-line verdict
  · Valuation level:     Static cheap, dynamic mixed.
  · Adjusted margin:     0.33x (below 1.0x — adjusted clear).
  · Recommendation:      Small position, observe NCAV trajectory for 2 more quarters.


[8] Data source appendix (MANDATORY)
Every figure in sections [1]–[7] must be traceable to one of the rows below.

| Field group                 | Source                       | Fetch                      | Period             |
|-----------------------------|------------------------------|-----------------------------|--------------------|
| Balance-sheet items         | Longbridge `financial-report --kind BS` | YYYY-MM-DD HH:MM      | FY2024 annual      |
| NCAV trajectory (last 4Q)   | Longbridge `financial-statement --kind BS --report qf` | YYYY-MM-DD HH:MM | Q1–Q4 2024 |
| Income statement            | Longbridge `financial-report --kind IS` | YYYY-MM-DD HH:MM      | FY2020–FY2024      |
| Cash flow (negative-OCF rule) | Longbridge `financial-report --kind CF --report qf` | YYYY-MM-DD HH:MM | Last 4Q |
| Current price / PE / PB / market cap | Longbridge `quote` + `calc-index` | YYYY-MM-DD HH:MM | Live |
| Dividend yield / TTM dividend | Longbridge `dividend`        | YYYY-MM-DD HH:MM           | TTM                |
| Insider / major-holder flow | Longbridge `ownership` + `insresearch` | YYYY-MM-DD HH:MM   | Last 2 quarters    |
| Industry PMI / cycle        | WebSearch — <publisher>, <article date>, <url> | YYYY-MM-DD HH:MM | <month> |
| Capacity utilisation        | WebSearch — <publisher>, <article date>, <url> | YYYY-MM-DD HH:MM | <month> |
| (Add row per WebSearch hit) | …                            | …                           | …                  |

Footnote conventions:
- Tag every WebSearch row with publisher + URL + access date.
- If a Longbridge field was unavailable and substituted via WebSearch, mark it `[substituted]` in the appendix row.
- Any field with a non-zero reconciliation residual (even within tolerance) where the residual could affect the figure shown in sections [1]–[7] must carry an inline `Reconciliation: <gap>` note in its appendix row. Do not surface it elsewhere in the body. Rows that reconciled cleanly need no note.
- If period alignment differs across statements (e.g. BS at Q4 but CF at H1), list the actual period per row — do not paper over.
```

---

## Layout (failing case — reconciliation gate did NOT pass)

When any reconciliation check exceeds tolerance, do **not** emit a score and do **not** produce sections [1]–[7]. Replace the body with a halt message naming the failing check:

```
{Symbol} ({code}) — Graham Cigar-Butt Diagnostic — HALTED
As-of: {date}   Currency: {ccy}

⚠️ 数据勾稽校验未通过，已停止评分以避免基于不一致数据下结论。
   失败项：{check name} — {formula} — 差距 {gap}% (容差 {tol}%)
   建议：请用户复核或更换数据源后再次尝试；如继续，需自行评估差异影响。

⚠️ Reconciliation gate did not pass — scoring halted to avoid conclusions on inconsistent data.
   Failing check: {check name} — {formula} — gap {gap}% (tolerance {tol}%)
   Recommendation: review the source data or refetch, then retry.

[Data source appendix — still mandatory, list all fetches that were attempted]
```

The halt message is the **only** time reconciliation results appear in the user-facing body. The Data Source Appendix is still required so the user can trace which fetch produced the bad number.

---

## Disclaimer (mandatory, end of every output)

```
⚠️ 免责声明：本分析由长桥 AI 基于格雷厄姆价值投资方法论自动生成，仅供参考，不构成投资建议。格雷厄姆策略通常需要 1–3 年以上的持有周期才可能兑现，动态调整因子基于公开数据的模型判断，不能完全规避价值陷阱风险。请在做出任何投资决策前进行独立研究，并考虑自身资金使用周期和风险承受能力。

⚠️ 免責聲明：本分析由長橋 AI 基於格雷厄姆價值投資方法論自動生成，僅供參考，不構成投資建議。格雷厄姆策略通常需要 1–3 年以上的持有週期才可能兌現。請在做出任何投資決策前進行獨立研究。

⚠️ Disclaimer: This analysis is generated by Longbridge AI using the Graham value-investing framework. It is for reference only and does not constitute investment advice. Graham strategies typically require a 1–3 year holding period before value is realised. Dynamic-adjustment factors are model-based and cannot fully eliminate value-trap risk. Do your own research and align with your capital horizon and risk tolerance before acting.
```
