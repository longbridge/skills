# Scoring rubric — five dimensions + holding-period mapping + verdict matrix

Loaded by `longbridge-buffett-moat-analyzer` SKILL.md on demand. Each dimension gets an integer star rating 1–5 (five stars max). Half-stars are acceptable when evidence is split (✩ shown as ★★★★☆). Do not edit numeric thresholds without updating SKILL examples in lockstep.

## Star scale (shared across dimensions)

| Stars | Meaning | When to award |
|---|---|---|
| ★★★★★ | Buffett-grade exemplary | Multi-year data shows the dimension consistently meets or exceeds Buffett's stated reference points; structural advantage, not a cyclical fluke. |
| ★★★★ | Strong | Most criteria met; one minor concern. |
| ★★★ | Acceptable | Mixed evidence; not a deal-breaker but not a strength either. |
| ★★ | Weak | Most criteria miss; a real concern Buffett would call out. |
| ★ | Disqualifying | Fundamentally inconsistent with Buffett's framework. |

The overall verdict is **not** an arithmetic average of stars — it's an explicit matrix call (see [§Verdict matrix](#verdict-matrix)). Quality and price are kept separate; never collapse them into one number.

---

## Dimension 1 — Business model & moat

**Core question**: what stops a well-funded competitor from copying this company's economics?

| Sub-criterion | Strong (★★★★+) | Weak (★★ or below) |
|---|---|---|
| Moat type identified | One clear type: brand / network / cost / switching / regulatory or resource | No identifiable durable advantage |
| Pricing power evidence | Has raised prices ≥ inflation for 3+ years without volume loss | Pricing follows competitors / commoditised |
| Gross-margin behaviour | Stable or rising over 5+ years, ≥ industry median | Declining trend; below industry median |
| Market structure | Top 1–3 in a concentrated industry; barriers to entry visible | Fragmented industry, low entry barriers |
| "10-year survival" test | Highly likely to exist and dominate in 10 years | Existential or structural threats within 5 years |

Width labels: **Wide** (most sub-criteria strong, hard to disrupt), **Narrow** (some advantage, contestable), **None** (no durable edge). Width is a separate label from the star count; report both.

Buffett quote anchor: *"If you have to pray to keep your competitive position, you don't have one."*

---

## Dimension 2 — Financial health

**Core question**: does this company actually make money, and is the money real?

| Metric | Buffett reference | Plain-language framing | Where it comes from |
|---|---|---|---|
| ROE (净资产收益率) | ≥ 15% for 10 consecutive years | "Returns to owners over the long run" | `financial-report --kind IS` (NI) ÷ avg equity from BS |
| Free cash flow | OCF − Capex > 0 every year for 5+ years; growing | "Is the money on paper actually arriving" | `financial-report --kind CF` |
| Leverage | Interest-bearing debt / equity < 0.5; no covenant pressure | "How much is borrowed" | BS items |
| Gross margin trend | Stable or rising over 5+ years | "Are they still in charge of price" | IS |
| Capex / Net income | Low (< 50% multi-year) — capital-light preferred | "Does growth cost a fortune or arrive cheap" | CF |
| Earnings stability | No annual loss in last 10 years | "Have they ever lost money in a normal year" | IS |

Pro-rate the stability and 10-year ROE windows if history is shorter, and note the proration in the data-source appendix.

**Sector adjustments**:
- Bank / insurance / brokerage → replace FCF / leverage with **ROA, NIM, NPL ratio, capital adequacy**, and weight loan/asset growth quality.
- Heavy-capex utilities / industrials → relax capital-light requirement; emphasise return-on-invested-capital and regulated-return durability.
- Note any sector adjustment explicitly in the dimension write-up.

---

## Dimension 3 — Management & capital allocation

**Core question**: is the CEO creating value for owners, or for themselves?

| Sub-criterion | Strong | Weak |
|---|---|---|
| Insider ownership | Founders / long-tenure executives hold meaningful equity | Trivial insider stake |
| Insider transactions (last 2y) | Net buying or holding through cycles | Persistent net selling; option-heavy comp without skin |
| Capital allocation track record | Buybacks at low valuations; dividends sustainable; M&A disciplined and ROIC-accretive | Big-premium acquisitions at peak; dilutive equity issuance; serial empire-building |
| Communication | Plain-spoken, candid shareholder letters; admits mistakes | Hype-driven narratives; vague guidance; refuses to discuss misses |
| Strategy consistency | Pursues a clear long-term thesis with low pivot frequency | Strategy of the year; chases trends |

Data sources: `ownership`, `insresearch`, `corporate` (buybacks / splits), `dividend`, plus WebSearch for shareholder-letter signals / CEO interviews when needed.

---

## Dimension 4 — Valuation & margin of safety

**Core question**: even granting it's a great business, is *this price* sane?

| Lens | Method | Tier mapping |
|---|---|---|
| PE vs 10y history | Percentile rank of current PE inside the trailing 10-year (or longest available) band | < 30% → 充足; 30–60% → 一般; 60–85% → 偏贵; > 85% → 高估 |
| PB vs 10y history | Same percentile method | Same tier mapping |
| PEG | Forward / TTM PE ÷ sustainable growth | < 1.0 reasonable; 1.0–1.5 OK if moat wide; > 1.5 demands wide moat AND high visibility |
| Dividend yield vs 10y history | Higher percentile → relatively cheaper | Use as cross-check only, never sole basis |
| Owner-earnings concept value | Simplified DCF on owner-earnings (≈ NI + D&A − maintenance capex) with conservative growth & ≥ 10% discount rate | Compare current price to the conservative band; report the band, not a single number |

> Buffett quote anchor: *"It's far better to buy a wonderful company at a fair price than a fair company at a wonderful price."* Map this directly to the tier — Buffett **does** buy "fair" prices on wonderful companies; require "充足 / 一般" tiers for an active buy lean, otherwise classify as a watchlist with target price.

Report the **safety-margin tier** explicitly (充足 / 一般 / 偏贵 / 高估). If multiple lenses disagree, surface the disagreement and pick the more conservative tier.

---

## Dimension 5 — Long-term visibility & industry runway

**Core question**: in 10 years, will this business be larger, smaller, or non-existent?

| Sub-criterion | Strong | Weak |
|---|---|---|
| Industry ceiling | Large addressable market, multi-year runway | Saturated / shrinking |
| Disruption risk | Low — entrenched habits / regulated moats / network effects | Tech substitution risk; behaviour-change risk visible now |
| Regulatory exposure | Stable rules; if regulated, regulator-friendly model | Active regulatory tightening or political crosshairs |
| Geographic / channel expansion runway | Real optionality outside home market | Already saturated globally |
| Customer concentration | Diversified; no top-5 > 30% of revenue | Heavy single-customer / single-platform dependency |

Industry-runway evidence often lives outside Longbridge. Use WebSearch for industry outlook, regulatory news, disruption signals — tag each row in the appendix with publisher, date, and URL.

---

## Holding-period mapping

Derived from Dimension 1 width label combined with Dimension 4 tier. The output report must surface a holding-period line on the diagnostic card; never omit it.

| Moat width | Suggested minimum hold | Operating note |
|---|---|---|
| Wide (★★★★★) | 5+ years (Buffett ideal: forever) | Significant drawdowns are buying opportunities, not exit triggers, provided moat is intact |
| Wide (★★★★) | 3–5 years | Semi-annual re-check; no thesis change → keep holding |
| Narrow (★★★) | 1–3 years | More frequent re-check; watch competitive structure changes |
| None (★★ or below) | Buffett framework does not apply | Redirect: Graham (`longbridge-graham-stock-analysis`) or growth lens, with strict position-size cap |

If the user's stated capital horizon is < 3 years, warn explicitly in the user-education block that this framework is mismatched to the horizon — regardless of how high the moat rating is.

---

## Position-building rhythm (for the user-education block)

Buffett's actual practice translated into retail-friendly rules:

- **Phased entry**: split target position into 3–4 tranches; never go all-in on day one.
- **Lower-price adds**: a 15–20% drawdown with thesis intact is a signal to add, not exit. Define this *before* entering.
- **Anchor on price discipline, not market timing**: write a "personal buy line" tied to the valuation tier (Dimension 4), and act only when price reaches it.
- **Quarterly re-check cadence**: once held, re-verify the five dimensions each quarter. Material change to Dimension 1 or 2 (moat or financial health) is the only valid sell trigger; price moves alone are not.

---

## Verdict matrix (quality × price)

Final one-line verdict uses this matrix. Do **not** average stars; pick the cell.

| | Price 充足 / 一般 | Price 偏贵 | Price 高估 |
|---|---|---|---|
| **Moat wide + financials clean (★★★★+ on D1, D2)** | 🟢 "Buffett would likely buy" — initiate position, phased | 🟡 "Buffett would likely hold and wait" — watchlist with target price | 🟠 "Great business, wrong price" — wait; do not buy on hype |
| **Moat wide, financial concerns** | 🟡 "Buffett would likely watch" — small position only if financial concerns are explainable | 🟠 "Watch" — do not buy until financials clarify | 🔴 "Pass for now" |
| **Moat narrow** | 🟠 "Probably not a Buffett candidate" — consider Graham instead | 🔴 "Pass" | 🔴 "Pass" |
| **No moat / disqualifying** | 🔴 "Not a Buffett candidate" — redirect to Graham or skip | 🔴 "Pass" | 🔴 "Pass" |

Map the chosen cell to the colour badge on the diagnostic card and quote the one-line verdict directly. The Buffett-voice narrative in section [7] must then expand on the chosen cell with concrete evidence from the data.

---

## Anti-cheat reminders

- Never assert a "wide moat" without naming the moat type and pointing to at least two pieces of concrete evidence (pricing-power data, gross-margin trend, market share, or regulated barrier).
- Never call a stock "cheap" on PE alone — cross-check PB, dividend-yield percentile, and the conservative owner-earnings band.
- If Dimension 1 ≤ ★★, do not award Dimension 4 a high score regardless of headline multiples — a low price on a no-moat business is a Graham question, not a Buffett one.
- If history < 3 years and Dimension 2 cannot be evaluated on 5–10 year windows, you may still score it but cap it at ★★★ and explicitly tag "history-limited" in the dimension write-up and appendix.
