# Output template — candidate cards + selection rationale + education block + data-source appendix

Loaded on demand by `longbridge-buffett-moat-stock-screener`. Use the section order verbatim. Card count: **3–5 candidates** (deliberate cap from the design doc — this is a high-conviction selector, not a giant leaderboard).

> **Single-language output (mandatory)**: the entire report — every heading, label, card field, narrative phrase, summary block, appendix row, and disclaimer — must be rendered in **one** language matching the user's input (Simplified Chinese, Traditional Chinese, or English). Do NOT mix languages within a single response. The canonical template below is written in English; before emitting, translate every label, value, narrative phrase, and disclaimer into the user's language using the [§Label translation lookup](#label-translation-lookup) and [§Disclaimer variants](#disclaimer-variants) sections.

> **Data-source transparency**: every figure on every card must be traceable to a row in the **Data Source Appendix** at the end of the output. The appendix closes with a one-line reconciliation summary (clean pass / within-tolerance residuals / per-row drops).

---

## Label translation lookup

Use this when the user's input language is Chinese. Pick the column matching the user's variant; render every cell of the canonical English template using the equivalent term. If you encounter a label not in the table, translate idiomatically and stay consistent throughout the response.

| English (canonical) | 简体中文 (zh-Hans) | 繁體中文 (zh-Hant) |
|---|---|---|
| Buffett Moat Stock Screener | 巴菲特护城河筛股 | 巴菲特護城河篩股 |
| Market | 市场 | 市場 |
| Universe | 候选池 | 候選池 |
| As-of | 截至 | 截至 |
| Currency | 币种 | 幣種 |
| Filters | 筛选条件 | 篩選條件 |
| Raw universe | 原始样本 | 原始樣本 |
| Buffett-disqualified excluded | 巴菲特排除项 | 巴菲特排除項 |
| Layer-1 pass | 第一层通过 | 第一層通過 |
| Layer-2 scored | 第二层评分 | 第二層評分 |
| Candidate Cards | 候选股票卡片 | 候選股票卡片 |
| Moat type | 护城河类型 | 護城河類型 |
| Core highlights | 核心亮点 | 核心亮點 |
| Buffett verdict | 巴菲特态度 | 巴菲特態度 |
| Likely buy | 大概率会买 | 大概率會買 |
| Maybe — wait for price | 可能会考虑 — 等更好的价格 | 可能會考慮 — 等更好的價格 |
| Not at this price | 目前估值不合适 | 目前估值不合適 |
| Not a typical Buffett pick | 不是典型巴菲特候选 | 不是典型巴菲特候選 |
| Pass | 回避 | 迴避 |
| Watch | 观察 | 觀察 |
| Valuation read | 估值读数 | 估值讀數 |
| Adequate / Fair / Rich / Overvalued | 充足 / 一般 / 偏贵 / 高估 | 充足 / 一般 / 偏貴 / 高估 |
| Min. holding period | 最短持有期 | 最短持有期 |
| 5+ years / 3–5 years / 1–3 years | 5 年以上 / 3–5 年 / 1–3 年 | 5 年以上 / 3–5 年 / 1–3 年 |
| Deep-dive | 深度诊断 | 深度診斷 |
| Market Summary | 市场总结 | 市場總結 |
| Selection rationale | 筛股理由 | 篩股理由 |
| Data Anomaly Footer | 数据异常脚注 | 數據異常腳註 |
| Failing reconciliation check | 失败的勾稽校验项 | 失敗的勾稽校驗項 |
| Gap | 差距 | 差距 |
| Action | 处理方式 | 處理方式 |
| Dropped — recommend manual review | 已剔除 — 建议人工复核 | 已剔除 — 建議人工複核 |
| Read this before acting on the screen | 行动前请先读这一段 | 行動前請先讀這一段 |
| Holding period | 持有时间 | 持有時間 |
| Entry pattern | 买入节奏 | 買入節奏 |
| Drawdown tolerance | 回撤容忍 | 回撤容忍 |
| Position logic | 仓位逻辑 | 倉位邏輯 |
| Action frequency | 操作频率 | 操作頻率 |
| Buffett-style expectation | 巴菲特式预期 | 巴菲特式預期 |
| Short-term / speculative expectation | 短线 / 投机式预期 | 短線 / 投機式預期 |
| Position-building rhythm | 建仓节奏 | 建倉節奏 |
| Phased entry | 分批建仓 | 分批建倉 |
| Lower-price adds | 下跌加仓 | 下跌加倉 |
| Personal buy-line | 个人买入价 | 個人買入價 |
| Quarterly re-check | 季度复盘 | 季度複盤 |
| Next step | 下一步建议 | 下一步建議 |
| Data Source Appendix | 数据来源附录 | 數據來源附錄 |
| Field group | 字段类别 | 欄位類別 |
| Source | 来源 | 來源 |
| Fetch | 抓取时间 | 抓取時間 |
| Period | 期间 | 期間 |
| Notes | 备注 | 備註 |
| Reconciliation passed | 勾稽校验通过 | 勾稽校驗通過 |
| Reconciliation dropped | 勾稽校验剔除 | 勾稽校驗剔除 |

---

## Layout (canonical English template — translate as a whole into the user's language)

```
Buffett Moat Stock Screener — {Market} / {Universe label}
As-of: {YYYY-MM-DD HH:MM TZ}   Currency: {HKD / USD / CNY}
Filters: ROE 5y≥{15%}, Debt/Asset≤{50%}, FCF 3y positive, Listed≥{5y}, Gross margin≥{30%}
Raw universe: {N_raw}   Buffett-disqualified excluded: {N_excl}   Layer-1 pass: {M}   Layer-2 scored: {K}

[Candidate Cards — Top {3–5}]

┌───────────────────────────────────────────────────────────────────┐
│ {Company name} ({code}) · {Market} · {Sector}        ★★★★★         │
│                                                                    │
│ Moat type: {brand · pricing power}                                 │
│ Core highlights:                                                   │
│   • ROE 5y avg {31.2%}  — well above 15% floor                     │
│   • Gross margin {91.6%} — industry-top                             │
│   • FCF positive 10/10 last decade — very strong FCF                │
│                                                                    │
│ Buffett verdict: 🟢 Likely buy                                     │
│ Valuation read: Fair — PE percentile 52%                           │
│ Min. holding period: 5+ years                                      │
│                                                                    │
│ [Deep-dive → Run `longbridge-buffett-moat-analyzer {CODE}`]        │
└───────────────────────────────────────────────────────────────────┘

(repeat 2–4 more cards; total 3–5 cards)

Tier legend on the card frame colour:
  🟢 Buffett-grade (composite 80–100, wide moat + price Adequate/Fair)
  🟡 Watchlist     (composite 65–79 OR price Rich with wide moat — wait for better price)
  🟠 Borderline    (composite 50–64 OR narrow moat — consider Graham instead)
  🔴 Not Buffett   (composite < 50 OR wide moat at price Overvalued — pass for now)
```

### Per-card field rules

| Field | Format | Source |
|---|---|---|
| Quality stars | Composite 5-star rounded to half-star (★★★★½ shown as ★★★★☆) | Layer-2 composite, see `criteria.md` §3 |
| Moat type | 1–2 keywords (e.g. "brand + pricing power") | Layer-2 D1 |
| Core highlights | Exactly 3, **quantitative first**, each ≤ 12 words with the metric + Buffett-anchor reading | Layer-1 + Layer-2 evidence |
| Buffett verdict | Verbatim from verdict matrix (criteria.md §4) | Verdict matrix |
| Valuation read | Tier (Adequate / Fair / Rich / Overvalued) + the most decisive percentile | Layer-2 D4 |
| Min. holding period | From holding-period mapping (criteria.md §5) | Width → period |
| Deep-dive CTA | Always present, always points to `longbridge-buffett-moat-analyzer <CODE>` | Fixed |

### Market Summary (always emitted after the cards)

```
[Market Summary]
- Raw universe: {N_raw} symbols ({INDEX or universe label}, as-of {date})
- Excluded — Buffett-disqualified: {N_excl}
    breakdown: {n_airline} airlines · {n_biotech} pre-revenue biotech · {n_st} ST/warning · {n_listing<5y} listed<5y · {n_negeq} negative-equity · {n_shell} shell · {n_other} other
    (for these cohorts, use `longbridge-fundamental` for early-stage views or remove the sector filter)
- Layer-1 hard-filter pass: {M} of {N_raw - N_excl}
- Layer-2 scored: {K}
- User-overridden thresholds (if any): {echo}
- Reconciliation drops: {n_dropped} symbol(s) — see Data Anomaly footer below
- Currency basis: {HKD / USD / CNY} — single-market batch
```

### Selection rationale (2–3 sentences, mandatory)

After the Market Summary, write 2–3 short sentences covering:

1. **Why these names together** — the shared Buffett signal (e.g. "all three combine wide brand moat with mid-cycle valuation"; "two consumer staples + one regulated utility cover the defensive corner of the universe").
2. **Current market caveat** — one honest caveat from the market regime right now (e.g. "consumer staples are at 70th-percentile valuation across the cohort — entry timing matters more than name selection").
3. **Deep-dive priority** — which name to run `longbridge-buffett-moat-analyzer` on first and why.

### Data Anomaly Footer (only if any rows were dropped)

```
[Data Anomaly Footer — rows dropped from candidate cards]
| Code | Failing reconciliation check | Gap | Action |
|---|---|---|---|
| 0XXX.HK | Current-assets sum vs reported total | +5.8% | Dropped — recommend manual review |
```

### Holding-period & user-education block (mandatory)

Insert this block in the user's input language only — do NOT print multiple language variants. The canonical English layout below is the template; translate the table headers and cells using the §Label-translation lookup.

```
──────────────────────────────────────────────
📌 Read this before acting on the screen:

This is a long-term-investing screener. It is not designed for short trading.
The Buffett framework only makes sense under these assumptions:

| Dimension          | Buffett-style expectation              | Short-term / speculative expectation |
|--------------------|----------------------------------------|--------------------------------------|
| Holding period     | Min 3 years; ideally forever           | Days to weeks                        |
| Entry pattern      | Wait for a fair price (months / years) | Buy anytime                          |
| Drawdown tolerance | 30–40% drawdowns tolerable             | Stop-loss typically inside 10%       |
| Position logic     | Concentrated in few high-conviction names | Diversified across many            |
| Action frequency   | Very low; mostly do nothing after buying | Frequent rebalancing                |

If the capital being deployed is needed within 3 years, do not use this screener's
output as the basis for a buy decision.

Position-building rhythm (apply per candidate):
  • Phased entry — split target position into 3–4 tranches
  • Lower-price adds — 15–20% drawdown with thesis intact is a signal to add
  • Personal buy-line — set price discipline tied to the valuation tier on each card
  • Quarterly re-check — only material moat or earnings-predictability change triggers exit
```

### Next-step recommendation

```
[Next step]
For any candidate you want to act on, run `longbridge-buffett-moat-analyzer <CODE>`
for a single-stock deep diagnostic (7-section report — moat, financials, management,
valuation, runway, Buffett-voice narrative, plus reconciliation gate before scoring).
Reminder: this screener applies Layer-1 hard filters + Layer-2 weighted moat scoring;
company-specific qualitative traps (regulatory shocks, fraud, single-product
obsolescence) are not captured here. Treat as a candidate list, not a buy list.
```

---

## Data Source Appendix (MANDATORY — every figure traceable; closes with reconciliation summary)

Every figure on every card and in the Market Summary must be traceable to a row below. Group by source; one row per Longbridge endpoint hit and one row per WebSearch hit. The column headers in the canonical template are English; translate them using §Label-translation lookup when the user's language is Chinese (the source-identifier values — endpoint names, URLs, dates — stay as-is regardless of language).

```
[Data Source Appendix]

| Field group                          | Source                                                | Fetch (UTC)        | Period               | Notes |
|--------------------------------------|-------------------------------------------------------|--------------------|----------------------|-------|
| Universe / constituent list          | Longbridge `constituent <INDEX>`                      | YYYY-MM-DD HH:MM   | Live                 | {N} symbols |
| Sector / industry classifier         | Longbridge `calc-index` / `basicinfo`                 | YYYY-MM-DD HH:MM   | Live                 | Drives the Buffett-disqualified exclusion |
| Listing date                         | Longbridge `basicinfo`                                | YYYY-MM-DD HH:MM   | Live                 | Filter #4 (years listed) |
| Snapshot (PE / PB / market cap / yld)| Longbridge `calc-index` + `quote`                     | YYYY-MM-DD HH:MM   | Live                 | Layer-2 D4 |
| Balance-sheet annual (5–10y)         | Longbridge `financial-report --kind BS --report af`   | YYYY-MM-DD HH:MM   | FY{a}–FY{b}          | Leverage / equity / debt ratio (Filter #2) |
| Balance-sheet quarterly (last 4Q)    | Longbridge `financial-report --kind BS --report qf`   | YYYY-MM-DD HH:MM   | Q{X}–Q{X+3} {YYYY}   | Recent trajectory |
| Income-statement annual (5–10y)      | Longbridge `financial-report --kind IS --report af`   | YYYY-MM-DD HH:MM   | FY{a}–FY{b}          | ROE / gross margin / earnings stability (Filters #1, #5; D3) |
| Income-statement quarterly (last 4Q) | Longbridge `financial-report --kind IS --report qf`   | YYYY-MM-DD HH:MM   | Q{X}–Q{X+3} {YYYY}   | Quarterly trend |
| Cash-flow annual (FCF base)          | Longbridge `financial-report --kind CF --report af`   | YYYY-MM-DD HH:MM   | FY{a}–FY{b}          | FCF = OCF − Capex (Filter #3) |
| Cash-flow quarterly                  | Longbridge `financial-report --kind CF --report qf`   | YYYY-MM-DD HH:MM   | last 4Q              | OCF persistence sanity |
| Historical PE / PB band (≈10y)       | Longbridge `kline --period day --count 2500` + derived percentile | YYYY-MM-DD HH:MM | ~10y           | Layer-2 D4 percentile rank |
| Dividend history                     | Longbridge `dividend`                                 | YYYY-MM-DD HH:MM   | TTM + 5y             | Layer-2 D2 capital-allocation track |
| Buyback / corporate actions          | Longbridge `corporate`                                | YYYY-MM-DD HH:MM   | last 5y              | Layer-2 D2 |
| Insider / major-holder flow          | Longbridge `ownership` + `insresearch`                | YYYY-MM-DD HH:MM   | last 2 quarters      | Layer-2 D2 alignment |
| Company profile (segment mix)        | Longbridge `company-profile`                          | YYYY-MM-DD HH:MM   | latest               | Layer-2 D3 revenue-mix stability |
| Peer set (margin / ROE benchmark)    | Longbridge `peer-comparison`                          | YYYY-MM-DD HH:MM   | latest               | Layer-2 D1 cost / margin comparison |
| Sector / theme universe pre-narrow   | Longbridge `sector-screener`                          | YYYY-MM-DD HH:MM   | latest               | Used only if user gave a sector / theme phrase |
| Industry outlook / disruption        | WebSearch — {Publisher}, {article date}, {URL}        | YYYY-MM-DD HH:MM   | {month YYYY}         | [substituted — Longbridge gap] |
| Brand / pricing-power signals        | WebSearch — {Publisher}, {article date}, {URL}        | YYYY-MM-DD HH:MM   | {month YYYY}         | [substituted — Longbridge gap] |
| Regulatory / policy references       | WebSearch — {Publisher}, {article date}, {URL}        | YYYY-MM-DD HH:MM   | {month YYYY}         | [substituted — Longbridge gap] |
| Buffett / Berkshire 13F holdings     | WebSearch — SEC EDGAR / {Publisher}, {filing date}, {URL} | YYYY-MM-DD HH:MM | Q{X} {YYYY} filing  | Only when user asked for "Buffett's actual holdings" |
| Management qualitative signals       | WebSearch — {Publisher}, {article date}, {URL}        | YYYY-MM-DD HH:MM   | {month YYYY}         | Shareholder letters / interviews |
| (Add one row per WebSearch hit)      | …                                                     | …                  | …                    | … |
```

Footnote conventions:
- Tag every WebSearch row with **publisher + URL + article date + access date**.
- Any Longbridge field substituted via WebSearch is tagged `[substituted — Longbridge gap]`.
- If a field is missing entirely (no Longbridge, no WebSearch), mark the row `[unavailable]` and explain in the affected dimension how it was handled (e.g. "pro-rated", "qualitative-only", "dimension capped at ★★★").
- Rows dropped at the reconciliation gate are named in the **Data Anomaly Footer** above with the failing check and the gap; they are NOT silently removed.
- Cohort tags ("history-limited", "sector-adjusted (banking)") must appear in the candidate card AND be summarised in the Market Summary.

### Reconciliation summary (final appendix line — mandatory)

Pick exactly one variant based on outcome AND one language matching the user's input. Print only that one line — never print multiple language versions of the summary.

**Variant 1 — Clean pass** (every check on every kept row within tolerance):

| Language | Line |
|---|---|
| en | `✅ Reconciliation passed — all {N_kept} candidate cards within 3% tolerance (max residual {x}%).` |
| zh-Hans | `✅ 勾稽校验通过 — {N_kept} 张候选卡片全部通过 3% 容差检查（最大残差 {x}%）。` |
| zh-Hant | `✅ 勾稽校驗通過 — {N_kept} 張候選卡片全部通過 3% 容差檢查（最大殘差 {x}%）。` |

**Variant 2 — Within-tolerance with material residual(s)** (list each affected row + field):

| Language | Line |
|---|---|
| en | `⚠️ Reconciliation passed within tolerance, with residuals worth flagging: · {Code A} IS↔CF residual −2.1% (tol ±3%) — affects FCF display. · {Code B} Period misalignment: BS at FY2024Q4 vs CF at FY2024H1.` |
| zh-Hans | `⚠️ 勾稽校验通过但存在容差内残差： · {Code A} IS↔CF 残差 −2.1%（容差 ±3%）— 影响 FCF 行显示。 · {Code B} 期间错位：BS 为 FY2024Q4，CF 为 FY2024H1。` |
| zh-Hant | `⚠️ 勾稽校驗通過但存在容差內殘差： · {Code A} IS↔CF 殘差 −2.1%（容差 ±3%）— 影響 FCF 行顯示。 · {Code B} 期間錯位：BS 為 FY2024Q4，CF 為 FY2024H1。` |

**Variant 3 — Per-row drops** (rows that failed > 3% tolerance were removed):

| Language | Line |
|---|---|
| en | `❌ Reconciliation dropped {n_dropped} row(s) (see Data Anomaly Footer above); the remaining {N_kept} cards are within tolerance.` |
| zh-Hans | `❌ 勾稽校验剔除 {n_dropped} 行（详见上方数据异常脚注）；其余 {N_kept} 张卡片均通过容差检查。` |
| zh-Hant | `❌ 勾稽校驗剔除 {n_dropped} 行（詳見上方數據異常腳註）；其餘 {N_kept} 張卡片均通過容差檢查。` |

The reconciliation summary is **the closing line** of the appendix — nothing else may appear after it except the disclaimer.

---

## Disclaimer variants

Print exactly **one** variant, matching the user's input language. Never print multiple language versions in the same output.

**English (en)**

```
⚠️ Disclaimer: This screen is generated by Longbridge AI using the Buffett value-investing
   framework on public data. For reference only — not investment advice. The tool emulates
   Buffett's selection method (quantitative hard filters + five-dimension qualitative scoring)
   and does not represent his actual views or actions. The Buffett framework typically requires
   a 3+ year holding period before value is realised, and is unsuitable for capital with a
   defined use within 3 years. For any candidate, follow up with `longbridge-buffett-moat-analyzer`
   for a single-stock deep diagnostic. Align with your capital horizon and risk tolerance before
   acting.
```

**Simplified Chinese (zh-Hans)**

```
⚠️ 免责声明：本筛选结果由长桥 AI 基于巴菲特价值投资框架与公开数据自动生成，仅供参考，
   不构成任何投资建议。本工具复刻巴菲特筛股方法（量化硬指标 + 五维质性评估），
   不代表巴菲特本人的实际观点或操作。巴菲特策略需要 3 年以上持有周期才可能兑现，
   不适合 3 年内有明确资金使用计划的资金。命中候选请用 `longbridge-buffett-moat-analyzer`
   做单股深度诊断，并结合自身资金使用周期与风险承受能力独立做出决策。
```

**Traditional Chinese (zh-Hant)**

```
⚠️ 免責聲明：本篩選結果由長橋 AI 基於巴菲特價值投資框架與公開資料自動生成，僅供參考，
   不構成任何投資建議。本工具復刻巴菲特篩股方法（量化硬指標 + 五維質性評估），
   不代表巴菲特本人之實際觀點或操作。巴菲特策略需 3 年以上持有週期方可兌現，
   不適合 3 年內有明確資金使用計畫之資金。命中候選請以 `longbridge-buffett-moat-analyzer`
   做單股深度診斷，並結合自身資金週期與風險承受能力獨立決策。
```
