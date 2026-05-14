# Output template — 7 fixed sections + mandatory data-source appendix · pass case · reject case · reconciliation halt case

Loaded by `longbridge-ark-analysis` SKILL.md on demand. Use the section order verbatim.

> **Single-language output (mandatory)**: the entire report — every heading, label, narrative paragraph, table cell, action frame, appendix row, reconciliation summary, and disclaimer — must be rendered in **one** language matching the user's input (Simplified Chinese, Traditional Chinese, or English). Do NOT mix languages within a single response. The canonical template below is written in English; before emitting, translate every label, value, summary line, and disclaimer into the user's language using the [§Label translation lookup](#label-translation-lookup), [§Reconciliation summary variants](#reconciliation-summary-final-appendix-row--mandatory), and [§Disclaimer variants](#disclaimer-variants) sections.

> **Reconciliation visibility**: reconciliation results are **user-visible here** — a one-line summary always appears as the final row of the Data Source Appendix (in the user's chosen language only). If a check fails, analysis halts and the appendix still prints with the failure named on the summary line.

> **Independence statement (mandatory)**: every output's disclaimer must state that this skill is an independent implementation inspired by ARK Invest's public methodology and is not affiliated with or representative of ARK Invest or Cathie Wood's actual views or positions.

---

## Label translation lookup

When the user's input language is Chinese, render every English label in the template using the equivalent term below. If a label is not in the table, translate idiomatically and stay consistent throughout the response.

| English (canonical) | 简体中文 (zh-Hans) | 繁體中文 (zh-Hant) |
|---|---|---|
| ARK-Style Disruptive-Innovation Diagnostic | ARK 启发式创新诊断 | ARK 啟發式創新診斷 |
| As-of | 截至 | 截至 |
| Currency | 币种 | 幣種 |
| Source | 来源 | 來源 |
| Current price | 当前价 | 當前價 |
| Innovation platform | 创新平台 | 創新平台 |
| AI & data | AI 与大数据 | AI 與大數據 |
| Robotics & automation | 自动化与机器人 | 自動化與機器人 |
| Energy storage | 能源存储 | 能源存儲 |
| Genomic revolution | 基因革命 | 基因革命 |
| Blockchain & fintech | 区块链与金融科技 | 區塊鏈與金融科技 |
| One-line conclusion | 一句话结论 | 一句話結論 |
| Core bet | 核心赌注 | 核心賭注 |
| Suitability check | 适用性检查 | 適用性檢查 |
| Platform fit | 平台归属 | 平台歸屬 |
| Innovation revenue share | 创新收入占比 | 創新收入佔比 |
| R&D intensity | 研发强度 | 研發強度 |
| Management innovation vision | 管理层创新愿景 | 管理層創新願景 |
| Strong / Medium / Weak | 强 / 中 / 弱 | 強 / 中 / 弱 |
| Pass | 通过 | 通過 |
| Rejected | 不适用 | 不適用 |
| Reason | 原因 | 原因 |
| Recommended alternative method | 推荐替代方法 | 推薦替代方法 |
| Why this fits | 适合原因 | 適合原因 |
| TAM (Total Addressable Market) | TAM（潜在市场规模） | TAM（潛在市場規模） |
| Target market | 目标市场 | 目標市場 |
| Low / Base / High | 保守 / 基准 / 乐观 | 保守 / 基準 / 樂觀 |
| Plain-language analogy | 白话理解 | 白話理解 |
| Cost curve (Wright's Law) | 成本曲线（莱特定律） | 成本曲線（萊特定律） |
| Technology domain | 技术领域 | 技術領域 |
| Learning rate | 学习率 | 學習率 |
| Authoritative source | 权威来源 | 權威來源 |
| Current cost position | 当前成本位置 | 當前成本位置 |
| Cost-decline implication | 成本下降含义 | 成本下降含義 |
| 5-year target — three scenarios | 5 年目标价 · 三情景 | 5 年目標價 · 三情景 |
| Scenario | 情景 | 情景 |
| Probability weight | 概率权重 | 概率權重 |
| Bull (optimistic) | 🐂 乐观 | 🐂 樂觀 |
| Base | 📊 基准 | 📊 基準 |
| Bear (pessimistic) | 🐻 悲观 | 🐻 悲觀 |
| Market share | 市占率 | 市佔率 |
| Net margin | 净利率 | 淨利率 |
| Terminal multiple | 终值倍数 | 終值倍數 |
| 5-year implied price | 5 年隐含价 | 5 年隱含價 |
| Discounted target | 折现目标价 | 折現目標價 |
| Weighted target | 加权目标价 | 加權目標價 |
| Discount rate | 折现率 | 折現率 |
| Upside / Downside | 上行 / 下行空间 | 上行 / 下行空間 |
| Main risks | 主要风险 | 主要風險 |
| Action frame | 行动框架 | 行動框架 |
| Key observation node | 关键观察节点 | 關鍵觀察節點 |
| Data Source Appendix | 数据来源附录 | 數據來源附錄 |
| Field group | 字段类别 | 欄位類別 |
| Fetch time | 抓取时间 | 抓取時間 |
| Period | 期间 | 期間 |
| HALTED | 已停止分析 | 已停止分析 |
| Failing check | 失败项 | 失敗項 |
| Estimated | 估算 | 估算 |
| No authoritative source | 无权威数据 | 無權威數據 |
| Substituted | 替代来源 | 替代來源 |
| Unavailable | 不可得 | 不可得 |

---

## Layout — pass case (canonical English template)

Translate every label, header, and narrative phrase below into the user's language before emitting. Do not print multiple languages in the same output.

```
{Company name} ({code}) — ARK-Style Disruptive-Innovation Diagnostic
As-of: {date}   Currency: {ccy}   Current price: {p}
Source: Longbridge Securities + WebSearch (see appendix)

[1] One-line conclusion
     {Company} sits on the {platform name(s)} platform. Under the ARK-style model the
     weighted 5-year target price is {weighted_target}, implying {▲/▼ XX.X%} vs current price.
     Core bet: "{single-sentence statement of the long-run thesis, e.g. 'autonomous-ride-hail scales globally'}".

[2] Suitability check
     Platform fit:                    {Strong / Medium / Weak} — {one-line evidence}
     Innovation revenue share:        {Strong / Medium / Weak} — {one-line evidence + figure}
     R&D intensity:                   {Strong / Medium / Weak} — {one-line evidence + figure}
     Management innovation vision:    {Strong / Medium / Weak} — {one-line evidence + citation}
     → Pass {— note: "framework applies; some assumptions lower-confidence" if applicable}

[3] TAM (Total Addressable Market)
     Target market: {market description}
     ┌───────────┬──────────────┬──────────────────────────────────────────────────────┐
     │ Tier      │ Size         │ Assumption (one sentence)                            │
     ├───────────┼──────────────┼──────────────────────────────────────────────────────┤
     │ Low       │ {amount}     │ {slow adoption, narrow user base, low ARPU}          │
     │ Base      │ {amount}     │ {mid path}                                           │
     │ High      │ {amount}     │ {fast adoption, full penetration, premium pricing}   │
     └───────────┴──────────────┴──────────────────────────────────────────────────────┘
     Plain-language analogy: {one-sentence analogy a retail reader will grasp}

[4] Cost curve (Wright's Law)
     Technology domain:           {domain, e.g. lithium-ion battery cells}
     Learning rate:               ~{X}% per doubling of cumulative output
     Authoritative source:        {Publisher — report name — year}
     Current cost position:       {one-line description of where on the curve}
     Cost-decline implication:    {plain-language: when output doubles again, unit cost
                                   roughly drops to {Y}, which is when {use case} becomes
                                   economically viable}

[5] 5-year target — three scenarios
     | Scenario   | Weight | Market share | Net margin | Terminal multiple | Discounted target |
     |------------|--------|--------------|------------|-------------------|--------------------|
     | 🐂 Bull    | 25%    | {a}%         | {b}%       | {c}× P/E or P/S   | {price}            |
     | 📊 Base    | 50%    | {a}%         | {b}%       | {c}×              | {price}            |
     | 🐻 Bear    | 25%    | {a}%         | {b}%       | {c}×              | {price}            |

     Discount rate: 15% (5-year horizon)         {note any user override}
     Weighted target: {weighted_target}
     Current price:   {p}
     Upside / Downside: {▲/▼ XX.X%}
     Note: scenarios are model inputs, not predictions. The Bull case is one of three —
     not a forecast.

[6] Main risks   (3 named — tied to this company's data)
     1. {Risk one — one-sentence description tied to a specific figure/event}
     2. {Risk two — …}
     3. {Risk three — …}

[7] Action frame    (condition-based; no buy/sell commands)
     • If you believe {core thesis sentence}, the current price implies you are paying for
       the {Base / Bull} scenario's expected outcome.
     • If {specific signal showing the thesis is breaking — name the metric and threshold}
       fails to appear by {date / event}, reconsider the long-run case.
     • Key observation node: {explicit upcoming event + date — e.g. "Q3 deliveries on
       YYYY-MM-DD", "FDA decision on indication X by YYYY-MM-DD"}.
     {If user horizon stated as < 3 years, append: "Your stated horizon is < 3 years —
      this framework is a 5-year lens and may not fit that horizon."}


[8] Data Source Appendix (MANDATORY — every figure traceable; closes with reconciliation summary)

| Field group                          | Source                                              | Fetch time           | Period             |
|--------------------------------------|-----------------------------------------------------|----------------------|--------------------|
| Income-statement annual (segments)   | Longbridge `financial-report --kind IS --report af` | YYYY-MM-DD HH:MM     | FY{a}–FY{b}        |
| Balance-sheet annual                 | Longbridge `financial-report --kind BS --report af` | YYYY-MM-DD HH:MM     | FY{a}–FY{b}        |
| Cash-flow annual                     | Longbridge `financial-report --kind CF --report af` | YYYY-MM-DD HH:MM     | FY{a}–FY{b}        |
| Quarterly financials (trend)         | Longbridge `financial-report --report qf`           | YYYY-MM-DD HH:MM     | last 4 quarters    |
| Current price / PE / PB / mkt cap    | Longbridge `quote` + `calc-index`                   | YYYY-MM-DD HH:MM     | live               |
| Historical price band                | Longbridge `kline --period day --count 2500`        | YYYY-MM-DD HH:MM     | ~10y               |
| Company profile / classification     | Longbridge `basicinfo` + `company-profile`          | YYYY-MM-DD HH:MM     | latest             |
| Recent news (innovation narrative)   | Longbridge `news`                                   | YYYY-MM-DD HH:MM     | last 6 months      |
| SEC / HK filings                     | Longbridge `sec-filings`                            | YYYY-MM-DD HH:MM     | latest             |
| TAM — Low                            | WebSearch — {publisher}, {report name}, {year}, {url} | YYYY-MM-DD HH:MM   | {report year}      |
| TAM — Base                           | WebSearch — {publisher}, {report name}, {year}, {url} OR `估算 — {basis}` | YYYY-MM-DD HH:MM | {report year} |
| TAM — High                           | WebSearch — {publisher}, {report name}, {year}, {url} | YYYY-MM-DD HH:MM   | {report year}      |
| Wright's-Law learning rate           | WebSearch — {BloombergNEF / IRENA / NHGRI / Epoch AI / ARK}, {year}, {url} | YYYY-MM-DD HH:MM | {report year} |
| Industry runway / disruption signal  | WebSearch — {publisher}, {date}, {url}              | YYYY-MM-DD HH:MM     | {article date}     |
| Regulatory / policy references       | WebSearch — {publisher}, {date}, {url}              | YYYY-MM-DD HH:MM     | {article date}     |
| (Add one row per WebSearch hit)      | …                                                   | …                    | …                  |

Footnote conventions:
- Tag every WebSearch row with publisher + report or article + year + URL + access date.
- TAM rows without a citable publisher use `估算 — <one-line basis>`, never a fabricated publisher.
- Learning-rate rows without a citable publisher use `无权威数据 / no authoritative source` — and the cost-curve discussion in section [4] is qualitative, with no numeric learning rate displayed.
- If a Longbridge field was unavailable and substituted via WebSearch, mark the row `[substituted]`.
- If a field is missing entirely (no Longbridge, no WebSearch), mark the row `[unavailable]` and explain in the relevant section how it affected the analysis.

Source-identifier values — endpoint names, URLs, fetch timestamps, dates — stay as-is regardless of language; only field-group labels are translated.

{Reconciliation summary line — final line of the appendix, see §Reconciliation summary variants}
```

---

## Layout — reject case (suitability gate did not pass)

When suitability fails, do **not** emit any TAM / Wright's-Law / scenario analysis. Replace sections [3]–[7] with a reject block. Section [8] (appendix + reconciliation summary) is still printed.

Canonical English reject layout (translate to user's language before emitting):

```
{Company} ({code}) — ARK-Style Disruptive-Innovation Diagnostic — REJECTED
As-of: {date}   Currency: {ccy}

[1] One-line conclusion
     {Company} is outside the disruptive-innovation envelope this framework can analyse.
     No TAM / scenario / target price will be produced.

[2] Suitability check
     Platform fit:                    {Strong / Medium / Weak} — {evidence}
     Innovation revenue share:        {Strong / Medium / Weak} — {evidence}
     R&D intensity:                   {Strong / Medium / Weak} — {evidence}
     Management innovation vision:    {Strong / Medium / Weak} — {evidence}
     → Rejected

[3] Reason
     Category: {A — Traditional industry | B — Being disrupted |
                C — Data basis insufficient | D — Disruption premium already realised}

     {One-paragraph explanation tied to this company's data — e.g. "Construction Bank's
      revenue is driven by net interest spread and loan volume, not by a technology cost
      curve; a TAM × share × margin growth model cannot be built."}

[4] Recommended alternative method(s)
     → {Method name from the currently installed skill library}
       Why this fits: {one or two sentences citing this company's specific signals —
                       e.g. "Current PB 0.6×, 10-year low quantile, with stable dividend yield 4.5%"}
     → {Optional second method}
       Why this fits: {…}

     {If no method in the live library is a clean match:
      "No matching method in the current library; suggest reviewing basic financials first
       via `longbridge-financial-report` / `longbridge-quote`."}

[8] Data Source Appendix (still mandatory — list what was fetched for the suitability decision)

| Field group                          | Source                                              | Fetch time           | Period             |
|--------------------------------------|-----------------------------------------------------|----------------------|--------------------|
| Company profile / classification     | Longbridge `basicinfo` + `company-profile`          | YYYY-MM-DD HH:MM     | latest             |
| Income-statement (segment mix)       | Longbridge `financial-report --kind IS --report af` | YYYY-MM-DD HH:MM     | FY{a}–FY{b}        |
| R&D ratio                            | Longbridge `financial-report --kind IS`             | YYYY-MM-DD HH:MM     | FY{b}              |
| Recent news (innovation narrative)   | Longbridge `news`                                   | YYYY-MM-DD HH:MM     | last 6 months      |
| (Add other rows as fetched)          | …                                                   | …                    | …                  |

{Reconciliation summary line — final line, see §Reconciliation summary variants}
```

---

## Layout — reconciliation halt case

When any reconciliation check exceeds tolerance, do **not** emit suitability scores, TAM, learning rate, or scenarios. Replace sections [1]–[7] with a halt message. Section [8] (appendix + reconciliation summary) is still printed and is the only place reconciliation details surface in the body.

Canonical English halt message (translate to user's language using the §Label translation lookup before emitting):

```
{Company} ({code}) — ARK-Style Disruptive-Innovation Diagnostic — HALTED
As-of: {date}   Currency: {ccy}

⚠️ Reconciliation gate did not pass — analysis halted to avoid conclusions on inconsistent data.
   Failing check: {check name} — {formula} — gap {gap}% (tolerance {tol}%)
   Recommendation: review the source data or refetch, then retry.

[8] Data Source Appendix — still mandatory (list every fetch attempted, even failed ones)

{Reconciliation summary line — final line, see §Reconciliation summary variants — uses the ❌ variant}
```

Equivalent halt-message phrasings for translation reference:

| Language | Halt message |
|---|---|
| zh-Hans | `⚠️ 数据勾稽校验未通过，已停止分析以避免基于不一致数据下结论。 失败项：{check name} — {formula} — 差距 {gap}%（容差 {tol}%） 建议：请用户复核或更换数据源后再次尝试。` |
| zh-Hant | `⚠️ 數據勾稽校驗未通過，已停止分析以避免基於不一致數據下結論。 失敗項：{check name} — {formula} — 差距 {gap}%（容差 {tol}%） 建議：請用戶複核或更換數據源後再次嘗試。` |

---

## Reconciliation summary (final appendix row — mandatory)

Pick exactly one outcome AND one language matching the user's input. Print only that single line — never print multiple language variants.

**Outcome 1 — Clean pass** (every check within tolerance, no material residuals):

| Language | Line |
|---|---|
| en | `✅ Reconciliation passed: {n}/{n} checks within tolerance (max residual {x}%).` |
| zh-Hans | `✅ 勾稽校验通过：{n}/{n} 检查项均在容差内（最大残差 {x}%）。` |
| zh-Hant | `✅ 勾稽校驗通過：{n}/{n} 檢查項均在容差內（最大殘差 {x}%）。` |

**Outcome 2 — Within-tolerance with material residual(s)** — list each affected field as a sub-line:

| Language | Line |
|---|---|
| en | `⚠️ Reconciliation passed within tolerance, with residuals worth flagging: · IS↔CF residual −2.1% (tol ±5%) — affects FCF context in §4. · Period misalignment: IS at FY2025Q4 vs CF at FY2025H1 — actual periods labelled per row.` |
| zh-Hans | `⚠️ 勾稽校验通过但存在容差内残差： · IS↔CF 残差 −2.1%（容差 ±5%）— 影响第 4 节自由现金流上下文。 · 期间错位：IS 为 FY2025Q4，CF 为 FY2025H1 — 已按实际期间标注。` |
| zh-Hant | `⚠️ 勾稽校驗通過但存在容差內殘差： · IS↔CF 殘差 −2.1%（容差 ±5%）— 影響第 4 節自由現金流上下文。 · 期間錯位：IS 為 FY2025Q4，CF 為 FY2025H1 — 已按實際期間標注。` |

**Outcome 3 — Failed** (at least one check > tolerance — analysis halted; see halt layout above):

| Language | Line |
|---|---|
| en | `❌ Reconciliation failed: {check name} gap {gap}% (tolerance {tol}%) — analysis halted.` |
| zh-Hans | `❌ 勾稽校验未通过：{check name} 差距 {gap}%（容差 {tol}%）— 已停止分析。` |
| zh-Hant | `❌ 勾稽校驗未通過：{check name} 差距 {gap}%（容差 {tol}%）— 已停止分析。` |

The reconciliation summary is **the closing line** of the appendix — nothing else may come after it except the disclaimer block.

---

## Disclaimer variants

Print exactly **one** variant at the end of the output (pass, reject, or halt), matching the user's input language. Never print multiple language versions in the same output. The independence statement is mandatory.

**English (en)**

```
⚠️ Disclaimer: This report is generated by AI using an ARK-style disruptive-innovation
   framework on public data. It is an independent implementation inspired by ARK Invest's
   publicly described methodology and is NOT affiliated with, endorsed by, or representative
   of ARK Invest or Cathie Wood's actual views or positions. All assumptions (TAM, market
   share, net margin, terminal multiple, learning rate, scenario probabilities, discount
   rate) are model inputs with high uncertainty; 5-year predictions historically carry
   wide errors. The report does not constitute investment advice. Markets carry risk; past
   performance does not guarantee future results. Do your own research and align with your
   capital horizon and risk tolerance before acting.
```

**Simplified Chinese (zh-Hans)**

```
⚠️ 免责声明：本报告由 AI 基于 ARK 启发式颠覆性创新框架与公开数据自动生成。本框架由
   Longbridge 独立实现，灵感来自 ARK Invest 公开披露的方法论，与 ARK Invest 官方及
   Cathie Wood 本人无关联、未获背书，也不代表其任何实际观点或仓位。所有假设
   （TAM、市占率、净利率、终值倍数、学习率、情景概率、折现率）均为模型输入，具有高度
   不确定性，5 年预测在历史上误差较大。本报告仅供参考，不构成任何投资建议。股票投资
   存在市场风险，过去的业绩不代表未来表现。请结合自身资金使用周期和风险承受能力独立
   做出投资决策。
```

**Traditional Chinese (zh-Hant)**

```
⚠️ 免責聲明：本報告由 AI 基於 ARK 啟發式顛覆性創新框架與公開數據自動生成。本框架由
   Longbridge 獨立實現，靈感來自 ARK Invest 公開披露的方法論，與 ARK Invest 官方及
   Cathie Wood 本人無關聯、未獲背書，也不代表其任何實際觀點或倉位。所有假設
   （TAM、市佔率、淨利率、終值倍數、學習率、情景概率、折現率）均為模型輸入，具有高度
   不確定性，5 年預測在歷史上誤差較大。本報告僅供參考，不構成任何投資建議。股票投資
   存在市場風險，過去業績不代表未來表現。請結合自身資金使用週期與風險承受能力獨立做出
   投資決策。
```
