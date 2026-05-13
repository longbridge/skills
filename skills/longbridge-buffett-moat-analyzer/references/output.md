# Output template — 7 fixed sections + mandatory data-source appendix

Loaded by `longbridge-buffett-moat-analyzer` SKILL.md on demand. Use the section order verbatim.

> **Single-language output (mandatory)**: the entire report — every heading, dimension label, narrative paragraph, table cell, education block, appendix row, and disclaimer — must be rendered in **one** language matching the user's input (Simplified Chinese, Traditional Chinese, or English). Do NOT mix languages within a single response. The canonical template below is written in English; before emitting, translate every label, value, narrative phrase, summary line, and disclaimer into the user's language using the [§Label translation lookup](#label-translation-lookup), [§Reconciliation summary variants](#reconciliation-summary-final-appendix-row--mandatory), and [§Disclaimer variants](#disclaimer-variants) sections.

> **Reconciliation visibility**: unlike most analysis skills, reconciliation results are **user-visible here** — a one-line summary always appears as the final row of the Data Source Appendix (in the user's chosen language only). If a check fails, scoring halts and the appendix still prints with the failure named on the summary line.

---

## Label translation lookup

When the user's input language is Chinese, render every English label in the template using the equivalent term below. If a label is not in the table, translate idiomatically and stay consistent throughout the response.

| English (canonical) | 简体中文 (zh-Hans) | 繁體中文 (zh-Hant) |
|---|---|---|
| Buffett Moat Diagnostic | 巴菲特护城河诊断 | 巴菲特護城河診斷 |
| As-of | 截至 | 截至 |
| Currency | 币种 | 幣種 |
| Source | 来源 | 來源 |
| Diagnostic summary card | 诊断摘要卡片 | 診斷摘要卡片 |
| Moat & business | 护城河与生意 | 護城河與生意 |
| Financial health | 财务健康 | 財務健康 |
| Management | 管理层 | 管理層 |
| Valuation / safety | 估值 / 安全边际 | 估值 / 安全邊際 |
| Long-term visibility | 长期可见度 | 長期可見度 |
| Wide / Narrow / None | 宽 / 窄 / 无 | 寬 / 窄 / 無 |
| Verdict | 结论 | 結論 |
| Buffett would likely buy this | 巴菲特大概率会买 | 巴菲特大概率會買 |
| Buffett would likely hold and wait | 巴菲特倾向持有并等待 | 巴菲特傾向持有並等待 |
| Great business, wrong price | 好生意，不对的价格 | 好生意，不對的價格 |
| Pass for now | 暂时回避 | 暫時迴避 |
| Probably not a Buffett candidate | 不是典型巴菲特候选 | 不是典型巴菲特候選 |
| Not a Buffett candidate | 非巴菲特候选 | 非巴菲特候選 |
| Min. holding period | 最短持有期 | 最短持有期 |
| 5+ years / 3–5 years / 1–3 years | 5 年以上 / 3–5 年 / 1–3 年 | 5 年以上 / 3–5 年 / 1–3 年 |
| One-line takeaway | 一句话总结 | 一句話總結 |
| Key strengths | 核心优势 | 核心優勢 |
| Main risks | 主要风险 | 主要風險 |
| Business model & moat | 业务模式与护城河 | 業務模式與護城河 |
| Moat type | 护城河类型 | 護城河類型 |
| Moat width | 护城河宽度 | 護城河寬度 |
| Pricing-power evidence | 定价权证据 | 定價權證據 |
| Competitive structure | 竞争结构 | 競爭結構 |
| 10-year survival call | 十年存续判断 | 十年存續判斷 |
| Buffett-style note | 巴菲特风格点评 | 巴菲特風格點評 |
| brand / network / cost / switching / regulatory / resource | 品牌 / 网络效应 / 成本 / 转换成本 / 监管 / 资源 | 品牌 / 網絡效應 / 成本 / 轉換成本 / 監管 / 資源 |
| Metric | 指标 | 指標 |
| Current | 当前值 | 當前值 |
| Buffett ref | 巴菲特参考 | 巴菲特參考 |
| 5/10-yr track | 5/10 年记录 | 5/10 年紀錄 |
| Stars | 评级 | 評級 |
| ROE | ROE（净资产收益率） | ROE（淨資產收益率） |
| FCF (OCF−Capex) | 自由现金流（OCF−Capex） | 自由現金流（OCF−Capex） |
| Debt / Equity | 负债 / 权益 | 負債 / 權益 |
| Gross margin | 毛利率 | 毛利率 |
| Capex / NI | 资本开支 / 净利润 | 資本開支 / 淨利潤 |
| Loss years (10y) | 亏损年数（10 年内） | 虧損年數（10 年內） |
| Sector-adjusted? | 是否做行业调整？ | 是否做行業調整？ |
| Management & capital allocation | 管理层与资本配置 | 管理層與資本配置 |
| Insider holding | 内部人持股 | 內部人持股 |
| Insider net buy/sell (last 2y) | 内部人近 2 年净买卖 | 內部人近 2 年淨買賣 |
| Buyback history | 回购历史 | 回購歷史 |
| Dividend policy | 分红政策 | 分紅政策 |
| M&A track record | 并购历史 | 併購歷史 |
| Capital-allocation grade | 资本配置评级 | 資本配置評級 |
| Communication quality | 沟通质量 | 溝通質量 |
| Valuation & margin of safety | 估值与安全边际 | 估值與安全邊際 |
| Lens | 视角 | 視角 |
| 10-yr median / band | 10 年中位 / 区间 | 10 年中位 / 區間 |
| Percentile | 分位 | 分位 |
| Read | 读数 | 讀數 |
| Owner-earnings concept value | 所有者收益概念价值 | 所有者收益概念價值 |
| Current price | 当前价 | 當前價 |
| Safety-margin tier | 安全边际等级 | 安全邊際等級 |
| Adequate / Fair / Rich / Overvalued | 充足 / 一般 / 偏贵 / 高估 | 充足 / 一般 / 偏貴 / 高估 |
| Personal buy-line guidance | 个人买入价指引 | 個人買入價指引 |
| Industry ceiling | 行业天花板 | 行業天花板 |
| Disruption risk | 颠覆风险 | 顛覆風險 |
| Regulatory exposure | 监管暴露 | 監管暴露 |
| Expansion runway | 扩张空间 | 擴張空間 |
| Customer concentration | 客户集中度 | 客戶集中度 |
| 10-year outlook one-liner | 十年展望一句话 | 十年展望一句話 |
| Buffett would probably say it this way | 如果让巴菲特来说，他大概会这样讲 | 如果讓巴菲特來說，他大概會這樣講 |
| Read this before acting on the report | 行动前请先读这一段 | 行動前請先讀這一段 |
| Dimension | 维度 | 維度 |
| Buffett-style expectation | 巴菲特式预期 | 巴菲特式預期 |
| Short-term / speculative expectation | 短线 / 投机式预期 | 短線 / 投機式預期 |
| Holding period | 持有时间 | 持有時間 |
| Entry pattern | 买入节奏 | 買入節奏 |
| Drawdown tolerance | 回撤容忍 | 回撤容忍 |
| Position logic | 仓位逻辑 | 倉位邏輯 |
| Action frequency | 操作频率 | 操作頻率 |
| Holding-period guidance for this stock | 本标的持有期建议 | 本標的持有期建議 |
| Position-building rhythm | 建仓节奏 | 建倉節奏 |
| Data Source Appendix | 数据来源附录 | 數據來源附錄 |
| Field group | 字段类别 | 欄位類別 |
| Fetch time | 抓取时间 | 抓取時間 |
| Period | 期间 | 期間 |
| HALTED | 已停止评分 | 已停止評分 |
| Failing check | 失败项 | 失敗項 |
| Recommendation | 建议 | 建議 |

---

## Layout — passing case (scores emitted; canonical English template)

Translate every label, header, and narrative phrase below into the user's language before emitting. Do not print multiple languages in the same output.

```
{Company name} ({code}) — Buffett Moat Diagnostic
As-of: {date}   Currency: {ccy}   Source: Longbridge Securities + WebSearch (see appendix)

[1] Diagnostic summary card
     ┌──────────────────────────────────────────────────┐
     │  {Company} — {code}                              │
     │                                                  │
     │  ① Moat & business         ★★★★★  Wide          │
     │  ② Financial health        ★★★★☆               │
     │  ③ Management              ★★★★☆               │
     │  ④ Valuation / safety      ★★★☆☆  Fair          │
     │  ⑤ Long-term visibility    ★★★★☆               │
     │                                                  │
     │  Verdict: 🟢 "Buffett would likely buy this"     │
     │  Min. holding period: 5+ years                   │
     └──────────────────────────────────────────────────┘
     One-line takeaway:
       "{Quote selected from §verdict matrix wording}"

     ⚡ Key strengths:  {top 2–3 concrete points}
     ⚠️ Main risks:    {top 2–3 concrete points}


[2] Dimension 1 — Business model & moat
     Moat type: {brand / network / cost / switching / regulatory / resource}
     Moat width: {Wide / Narrow / None}
     Pricing-power evidence:
       - {price increase history: timing, magnitude, volume impact}
       - {gross-margin trajectory: 5-yr trend with concrete %s}
       - {market-share / concentration evidence}
     Competitive structure: {top-N share, entry barriers, recent challengers}
     10-year survival call: {High / Medium / Low — with one-line reasoning}
     Buffett-style note: "{quote anchor or paraphrase tied to the evidence above}"


[3] Dimension 2 — Financial health
     | Metric          | Current  | Buffett ref   | 5/10-yr track          | Stars |
     |-----------------|----------|---------------|------------------------|-------|
     | ROE             | {x.x%}   | ≥ 15% × 10y   | {y-pass / total years} | ★★★★☆ |
     | FCF (OCF−Capex) | {amt}    | > 0 every yr  | {pass count}           | ★★★★★ |
     | Debt / Equity   | {x.xx}   | < 0.5         | {trend note}           | ★★★★☆ |
     | Gross margin    | {x.x%}   | stable / ↑    | {5-yr direction}       | ★★★☆☆ |
     | Capex / NI      | {x.x%}   | low (< 50%)   | {5-yr avg}             | ★★★★☆ |
     | Loss years (10y)| {count}  | 0             | {list any loss years}  | ★★★★★ |
     Sector-adjusted? {yes/no — if yes name the adjustment, e.g. "bank: ROA + NIM + NPL + CAR used in place of FCF/leverage"}


[4] Dimension 3 — Management & capital allocation
     - Insider holding:                  {%, tenure}
     - Insider net buy/sell (last 2y):   {direction, magnitude, dates of notable transactions}
     - Buyback history:                  {timing, volume, valuation level at execution}
     - Dividend policy:                  {payout %, growth trajectory, sustainability}
     - M&A track record:                 {recent material deals, post-deal ROIC, premium paid}
     - Capital-allocation grade:         {A / B / C — with one-line reasoning}
     - Communication quality:            {plain-spoken & candid / vague / hype — with source}


[5] Dimension 4 — Valuation & margin of safety
     | Lens               | Current   | 10-yr median / band | Percentile | Read       |
     |--------------------|-----------|---------------------|-----------|------------|
     | PE (TTM)           | {x.x}     | {a–b}               | {pct}%    | {tier}     |
     | PB                 | {x.x}     | {a–b}               | {pct}%    | {tier}     |
     | Dividend yield     | {x.x%}    | {a–b}               | {pct}%    | {tier}     |
     | PEG                | {x.x}     | < 1.0 ref           | —         | {tier}     |
     | Owner-earnings concept value: {low–high band, e.g. 220–290}
     Current price:                  {p}
     Safety-margin tier:             {Adequate / Fair / Rich / Overvalued}
     Personal buy-line guidance:     {explicit price level matching the tier promotion threshold}
     Note: owner-earnings band is a simplified concept estimate, not a published target.


[6] Dimension 5 — Long-term visibility
     - Industry ceiling:             {addressable-market description with source}
     - Disruption risk:              {Low / Medium / High, named threat if any}
     - Regulatory exposure:          {description + recent policy / litigation references}
     - Expansion runway:             {geography / channel / product extensions}
     - Customer concentration:       {top-5 share %}
     10-year outlook one-liner:      "{single sentence}"


[7] Buffett-voice narrative + user education block

     "Buffett would probably say it this way…"
     {3–5 short paragraphs in Buffett's register: plain-spoken, concrete, dryly humorous.
      First-person ("If I were sitting on this one…"), no jargon stacking. Each paragraph
      maps to one of: business quality / financial integrity / management / price / patience.
      Reference one Buffett quote with attribution. Avoid absolute buy/sell commands —
      Buffett's own voice is observational, not instructional.}

     ──────────────────────────────────────────────
     📌 Read this before acting on the report:

     This is a long-term-investing tool. It is not designed for short trading.
     The Buffett framework only makes sense under these assumptions:

     | Dimension          | Buffett-style expectation        | Short-term / speculative expectation |
     |--------------------|----------------------------------|--------------------------------------|
     | Holding period     | Minimum 3 years; ideally forever | Days to weeks                        |
     | Entry pattern      | Wait for a fair price (months / years) | Buy anytime                    |
     | Drawdown tolerance | 30–40% drawdowns are tolerable   | Stop-loss typically inside 10%       |
     | Position logic     | Concentrated in few high-conviction names | Diversified across many       |
     | Action frequency   | Very low; after buying, mostly do nothing | Frequent rebalancing          |

     If the capital being deployed is needed within 3 years, do not use this report's
     verdict as the basis for a buy decision.

     Holding-period guidance for this stock: {derived from §scoring.md holding-period mapping}.
     Position-building rhythm: phased 3–4 tranches; add on 15–20% drawdown only if thesis
     intact; quarterly re-check; only material moat or financial-health change triggers exit.


[8] Data Source Appendix (MANDATORY — every figure traceable; closes with reconciliation summary)

| Field group                         | Source                                         | Fetch time           | Period             |
|-------------------------------------|------------------------------------------------|----------------------|--------------------|
| Balance-sheet annual (5–10y)        | Longbridge `financial-report --kind BS --report af` | YYYY-MM-DD HH:MM | FY{a}–FY{b}        |
| Income-statement annual (5–10y)     | Longbridge `financial-report --kind IS --report af` | YYYY-MM-DD HH:MM | FY{a}–FY{b}        |
| Cash-flow annual (FCF base)         | Longbridge `financial-report --kind CF --report af` | YYYY-MM-DD HH:MM | FY{a}–FY{b}        |
| Quarterly financials (trend)        | Longbridge `financial-report --report qf`      | YYYY-MM-DD HH:MM     | last 4 quarters    |
| Current price / PE / PB / mkt cap   | Longbridge `quote` + `calc-index`              | YYYY-MM-DD HH:MM     | live               |
| Historical PE/PB band (10y)         | Longbridge `kline --period day --count 2500` + derived index | YYYY-MM-DD HH:MM | ~10y |
| Dividend history                    | Longbridge `dividend`                          | YYYY-MM-DD HH:MM     | TTM + 5y           |
| Buyback / corporate actions         | Longbridge `corporate`                         | YYYY-MM-DD HH:MM     | last 5y            |
| Insider / major-holder flow         | Longbridge `ownership` + `insresearch`         | YYYY-MM-DD HH:MM     | last 2 quarters    |
| Company profile / industry class    | Longbridge `basicinfo` + `company-profile`     | YYYY-MM-DD HH:MM     | latest             |
| Peer set (margin / ROE benchmark)   | Longbridge `peer-comparison`                   | YYYY-MM-DD HH:MM     | latest             |
| Industry outlook / disruption       | WebSearch — {publisher}, {article date}, {url} | YYYY-MM-DD HH:MM     | {article date}     |
| Regulatory / policy references      | WebSearch — {publisher}, {article date}, {url} | YYYY-MM-DD HH:MM     | {article date}     |
| Management qualitative signals      | WebSearch — {publisher}, {article date}, {url} | YYYY-MM-DD HH:MM     | {article date}     |
| (Add one row per WebSearch hit)     | …                                              | …                    | …                  |

Footnote conventions:
- Tag every WebSearch row with publisher + URL + access date.
- If a Longbridge field was unavailable and substituted via WebSearch, mark it `[substituted]` in the appendix row.
- If a field is missing entirely (no Longbridge, no WebSearch), mark the row `[unavailable]` and explain in the dimension write-up how it affected the score (e.g. "pro-rated", "qualitative-only").

Source-identifier values — endpoint names, URLs, fetch timestamps, dates — stay as-is regardless of language; only field-group labels are translated.
```

---

## Reconciliation summary (final appendix row — mandatory)

Pick exactly one outcome AND one language matching the user's input. Print only that single line — never print multiple language variants.

**Outcome 1 — Clean pass** (every check within tolerance, no material residuals):

| Language | Line |
|---|---|
| en | `✅ Reconciliation passed: 9/9 checks within tolerance (max residual {x}%).` |
| zh-Hans | `✅ 勾稽校验通过：9/9 检查项均在容差内（最大残差 {x}%）。` |
| zh-Hant | `✅ 勾稽校驗通過：9/9 檢查項均在容差內（最大殘差 {x}%）。` |

**Outcome 2 — Within-tolerance with material residual(s)** — list each affected field as a sub-line:

| Language | Line |
|---|---|
| en | `⚠️ Reconciliation passed within tolerance, with residuals worth flagging: · IS↔CF residual −2.1% (tol ±5%) — affects FCF row of the valuation dimension. · Period misalignment: BS at FY2024Q4 vs CF at FY2024H1 — actual periods labelled per row.` |
| zh-Hans | `⚠️ 勾稽校验通过但存在容差内残差： · IS↔CF 残差 −2.1%（容差 ±5%）— 影响估值维度的 FCF 行。 · 期间错位：BS 为 FY2024Q4，CF 为 FY2024H1 — 已按实际期间标注。` |
| zh-Hant | `⚠️ 勾稽校驗通過但存在容差內殘差： · IS↔CF 殘差 −2.1%（容差 ±5%）— 影響估值維度的 FCF 行。 · 期間錯位：BS 為 FY2024Q4，CF 為 FY2024H1 — 已按實際期間標注。` |

**Outcome 3 — Failed** (at least one check > tolerance — scoring halted; see halt layout below):

| Language | Line |
|---|---|
| en | `❌ Reconciliation failed: {check name} gap {gap}% (tolerance {tol}%) — scoring halted.` |
| zh-Hans | `❌ 勾稽校验未通过：{check name} 差距 {gap}%（容差 {tol}%）— 已停止评分。` |
| zh-Hant | `❌ 勾稽校驗未通過：{check name} 差距 {gap}%（容差 {tol}%）— 已停止評分。` |

The reconciliation summary is **the closing line** of the appendix — nothing else may come after it except the disclaimer block.

---

## Layout — failing case (reconciliation gate did not pass)

When any reconciliation check exceeds tolerance, do **not** emit scores; replace sections [1]–[7] with a halt message **in the user's language only**. Section [8] (appendix + reconciliation summary) is still printed and is the only place reconciliation details surface in the body.

Canonical English halt message (translate to user's language using the §Label translation lookup before emitting):

```
{Company} ({code}) — Buffett Moat Diagnostic — HALTED
As-of: {date}   Currency: {ccy}

⚠️ Reconciliation gate did not pass — scoring halted to avoid conclusions on inconsistent data.
   Failing check: {check name} — {formula} — gap {gap}% (tolerance {tol}%)
   Recommendation: review the source data or refetch, then retry.

[8] Data Source Appendix — still mandatory (list every fetch attempted, even failed ones, and close with the ❌ reconciliation-failed summary line in the user's language)
```

Equivalent halt-message phrasings for translation reference:

| Language | Halt message |
|---|---|
| zh-Hans | `⚠️ 数据勾稽校验未通过，已停止评分以避免基于不一致数据下结论。 失败项：{check name} — {formula} — 差距 {gap}%（容差 {tol}%） 建议：请用户复核或更换数据源后再次尝试。` |
| zh-Hant | `⚠️ 數據勾稽校驗未通過，已停止評分以避免基於不一致數據下結論。 失敗項：{check name} — {formula} — 差距 {gap}%（容差 {tol}%） 建議：請用戶複核或更換數據源後再次嘗試。` |

---

## Disclaimer variants

Print exactly **one** variant at the end of the output (pass or halt), matching the user's input language. Never print multiple language versions in the same output.

**English (en)**

```
⚠️ Disclaimer: This report is generated by AI using the Buffett value-investing framework on public data.
   It is for reference only and does not constitute investment advice. The tool emulates Buffett's
   analytical method and does not represent his actual views or actions. Markets carry risk; past
   performance does not guarantee future results. Do your own research and align with your capital
   horizon and risk tolerance before acting.
```

**Simplified Chinese (zh-Hans)**

```
⚠️ 免责声明：本报告由 AI 基于巴菲特价值投资框架与公开数据自动生成，仅供参考，
   不构成任何投资建议。本工具复刻巴菲特分析方法，不代表巴菲特本人的实际观点或操作。
   股票投资存在市场风险，过去的业绩不代表未来表现。请结合自身资金使用周期和风险承受能力
   独立做出投资决策。
```

**Traditional Chinese (zh-Hant)**

```
⚠️ 免責聲明：本報告由 AI 基於巴菲特價值投資框架與公開數據自動生成，僅供參考，
   不構成任何投資建議。本工具復刻巴菲特分析方法，不代表巴菲特本人的實際觀點或操作。
   股票投資存在市場風險，過去業績不代表未來表現。請結合自身資金使用週期與風險承受能力
   獨立做出投資決策。
```
