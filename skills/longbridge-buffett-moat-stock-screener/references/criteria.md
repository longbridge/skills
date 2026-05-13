# Screening criteria — Layer-1 hard filters, Layer-2 moat scoring, verdict matrix, holding-period mapping

Loaded on demand by `longbridge-buffett-moat-stock-screener`. Numeric defaults align with Buffett's publicly stated reference points (Letters to Shareholders, *Berkshire Hathaway 1977–2024*, and *The Essays of Warren Buffett*). Do not change without updating SKILL.md examples in lockstep.

---

## 1. Layer-1 — Hard quantitative filter (pass / fail gate)

Apply as a binary pre-filter. A symbol that fails ≥ 2 filters drops out by default (user can relax to "fail ≤ 3" on request). The thresholds reflect Buffett's own framing: a great business should clear all of them under normal conditions — failing two simultaneously is a strong signal the business itself isn't good enough for the framework.

| # | Filter | Default threshold | Why this matters (Buffett anchor) | Source field |
|---|---|---|---|---|
| 1 | ROE (5y average) | ≥ 15% | *"The primary test of managerial economic performance is achievement of a high earnings rate on equity capital employed."* Sustained high ROE = the business itself is good. | derived from `financial-report --kind IS` (NI) ÷ avg equity from `financial-report --kind BS` |
| 2 | Debt-to-asset ratio | ≤ 50% | High leverage adds risk that's invisible until it isn't. Buffett: *"Leverage is the only way a smart guy can go broke."* | BS — total liabilities ÷ total assets |
| 3 | Free cash flow (OCF − Capex) | positive each of last 3 years | *"Accounting earnings can lie; cash cannot."* FCF is the "real money" test. | `financial-report --kind CF` |
| 4 | Years listed | ≥ 5 years | Need a track record to judge management & business quality; pro-rate the 5–10y window if 5–10 years available. | `basicinfo.listing_date` |
| 5 | Gross margin (TTM) | ≥ 30% | Low gross margin generally signals no pricing power, often commoditised. Buffett's favoured businesses (See's, Coke, Apple) all clear this comfortably. | IS — gross profit ÷ revenue |

### Sector-adjusted filter substitutions

Banks / insurance / brokerage business models have intentionally different balance-sheet shapes; the raw rules above produce false rejects. Substitute as follows and **note the substitution in the row's Data Note**:

| Sector | Substitution |
|---|---|
| Commercial banks | ROE rule kept; **debt rule** → CAR ≥ regulator-required + buffer · **FCF rule** → ROA ≥ 1.0% with stable NIM · **gross margin** → cost-to-income ratio ≤ 50% |
| Insurance | ROE kept; **debt** → solvency margin ≥ 200% · **FCF** → underwriting combined ratio < 100% over 5y · **gross margin** → omit |
| Brokerage / asset management | ROE kept; **debt** → capital-adequacy ratio per regulator · **FCF** → omit (replace with operating-cash-flow proxy from net commission income); **gross margin** → omit |

If the symbol's sector classifier is missing or ambiguous, default to the raw rules — better to flag a borderline name with a "sector data missing" note than silently mis-apply the wrong substitution.

### Pro-ration rules

- **Listed 5–10 years** (i.e. less than a full 10-year window): pro-rate filters 1 and 3 over the available years. Mark row "history-limited".
- **Sector mid-cycle dip** (e.g. one bad year in an otherwise clean record): the user may *manually* relax filter 1 ROE to "5y avg with worst year removed" — must be echoed in the Market Summary.

---

## 2. Excluded cohorts (no scoring, dropped from the universe)

These businesses are structurally outside Buffett's framework. The screener does **not** run substitute models for them — they are removed from the universe and counted in the Market Summary "Excluded" line. If the user explicitly asks for one of these, return an honest empty result with a redirect to the nearest non-excluded sector.

| Cohort | Reason | Display in Market Summary | Suggested redirect |
|---|---|---|---|
| Airlines | Buffett 1997 Annual Meeting: *"airline industry is a value-destroying industry"*; high capex, cyclical demand, no pricing power, undifferentiated product. | "Excluded — Buffett-disqualified industry (airlines)" | Regulated utilities; consumer staples with pricing power. |
| Pre-revenue / pure-loss biotech | Buffett framework requires a track record; pre-revenue biotech has no Dimension-2 evidence. | "Excluded — no operating track record" | `longbridge-fundamental` for early-stage view. |
| Hot-IPO concept names (no operating history) | Same as above; story ≠ business. | "Excluded — no operating track record" | `longbridge-fundamental`. |
| ST / 退市风险 / 高风险警示 | Buffett: *"Rule No. 1: never lose money."* — going-concern doubt is a hard stop. | "Excluded — ST / going-concern" | None inside Buffett framework. |
| Listed < 5 years | Insufficient history for a 5–10y ROE / FCF / earnings-stability read. | "Excluded — listing < 5y" | Re-check after 5y of public reporting. |
| Pure-shell / negative-equity firms | No real business to evaluate. | "Excluded — shell / negative equity" | None. |
| Pre-revenue commodity miners / pure resource concept | No realised cash flow track record. | "Excluded — pre-cash-flow resource concept" | `longbridge-fundamental`. |

Detection inputs: sector / industry code from `longbridge calc-index` or `longbridge basicinfo` (whichever exposes a GICS / industry tag); listing date from `basicinfo`; equity sign from BS; ST / 警示 tag from `quote` / `basicinfo`.

---

## 3. Layer-2 — Qualitative moat scoring (weighted composite, 0–100)

Applied only to Layer-1 passers. Five dimensions, fixed weights, each dimension also gets a 1–5 star rating shown on the candidate card. The composite is the default rank key; star ratings drive the verdict-matrix call (next section).

### Dimension 1 — Moat type & width (weight 35%)

**Core question**: what stops a well-funded competitor from copying this company's economics?

| Moat type | Recognise from … | Wide signal |
|---|---|---|
| Brand / pricing power | Has raised prices ≥ inflation for 3+ years without volume loss; brand-value ranking | Gross margin stable or rising, top-3 in category |
| Network effects | Two-sided platform with growing engagement metrics; ARPU stable | Top-1 in category with widening gap |
| Switching costs | High contract renewal rate; multi-year embedded customer contracts | Renewal > 90%, churn < 5% |
| Cost advantage | Scale-driven unit cost below median peer; structural input access | Margin lead > 5pp over median peer for 5y |
| Regulatory / resource scarcity | Licensed/concessioned operations, scarce reserves, government monopoly | Regulator-protected returns; long-dated concession |

| Stars | Award when … |
|---|---|
| ★★★★★ | One clearly identified moat type **with at least two pieces of concrete evidence** (pricing-power data + gross-margin trend, OR market share + entry-barrier proof) AND 10-year survival call "High". |
| ★★★★ | Clear moat type, slightly less concrete evidence OR one minor concern (e.g. one challenger emerging). |
| ★★★ | Some advantage, contestable — narrow moat. |
| ★★ | Mixed evidence; no clear durable advantage. |
| ★ | No identifiable moat — disqualifying for Buffett framework; redirect to Graham. |

Width labels: **Wide** (most sub-criteria strong), **Narrow** (some advantage, contestable), **None**. Width is a separate label from the star count; both are reported on the card.

Buffett quote anchor: *"If you have to pray to keep your competitive position, you don't have one."*

### Dimension 2 — Capital allocation (weight 20%)

**Core question**: is the CEO creating value for owners or for themselves?

| Sub-criterion | Strong (★★★★+) | Weak (★★ or below) |
|---|---|---|
| Insider ownership | Founders / long-tenure execs hold meaningful equity | Trivial insider stake |
| Insider transactions (last 2y) | Net buying or holding through cycles | Persistent net selling; option-heavy comp without skin |
| Dividend / buyback discipline | Buybacks at low valuations; dividends growing & sustainable | Dilutive issuance; buybacks at peaks; cuts in downturns |
| M&A track record | Disciplined, ROIC-accretive, no big premia | Big-premium peak deals; serial empire-building |
| Communication | Plain-spoken candid letters; admits mistakes | Hype, vague guidance, refuses to discuss misses |
| Strategy consistency | Clear long-term thesis, low pivot frequency | "Strategy of the year"; chases trends |

Data sources: `ownership`, `insresearch`, `corporate` (buybacks / splits), `dividend`, plus WebSearch for shareholder-letter signals / CEO interviews when needed.

### Dimension 3 — Earnings predictability (weight 20%)

**Core question**: how stable and predictable is the business across cycles?

| Metric | Strong | Weak |
|---|---|---|
| EPS / NI growth volatility (5y CoV) | < 0.25 | > 0.50 |
| Loss years (last 10y) | 0 | Any annual loss |
| Revenue cyclicality | Low — defensive / staple / regulated | High — cyclical industrial / commodity |
| Revenue-mix stability | Top 3 segments stable over 5y | Frequent mix shifts |
| Customer concentration | Top-5 < 30% of revenue | Heavy single-customer dependence |

Sources: `financial-report --kind IS` (annual + quarterly), `company-profile` for segment breakdown.

### Dimension 4 — Valuation reasonableness (weight 15%)

**Core question**: even granting it's a great business, is *this price* sane?

| Lens | Method | Tier mapping |
|---|---|---|
| PE vs 10y history | Percentile rank of current PE inside the trailing 10-year (or longest available) band | < 30% → 充足; 30–60% → 一般; 60–85% → 偏贵; > 85% → 高估 |
| PB vs 10y history | Same percentile method | Same tier mapping |
| Dividend yield vs 10y history | Higher percentile → relatively cheaper | Cross-check only, never sole basis |
| Simplified owner-earnings concept band | DCF on owner-earnings (≈ NI + D&A − maintenance capex) with ≥ 10% discount rate | Report current price vs the conservative band; report the band, not a single number |

Report the **safety-margin tier** explicitly (充足 / 一般 / 偏贵 / 高估). If multiple lenses disagree, surface the disagreement and pick the more conservative tier.

> Buffett quote anchor: *"It's far better to buy a wonderful company at a fair price than a fair company at a wonderful price."* Map directly to the tier — Buffett **does** buy "fair" prices on wonderful companies; require "充足 / 一般" tiers for an active 🟢 buy lean, otherwise 🟡 watchlist with target price.

### Dimension 5 — Long-term industry runway (weight 10%)

**Core question**: in 10 years, will this business be larger, smaller, or non-existent?

| Sub-criterion | Strong | Weak |
|---|---|---|
| Industry ceiling | Large addressable market, multi-year runway | Saturated or shrinking |
| Disruption risk | Low — entrenched habits / regulated moats / network effects | Tech substitution / behaviour-change risk visible now |
| Regulatory exposure | Stable rules; if regulated, regulator-friendly model | Active regulatory tightening |
| Geographic / channel expansion | Real optionality outside home market | Already saturated globally |

Industry-runway evidence often lives outside Longbridge. Use WebSearch for outlook / regulatory news; tag each row in the appendix with publisher + URL + access date.

### Composite score

```
Layer-2 composite (0–100) = 0.35 × Moat + 0.20 × Capital_alloc + 0.20 × Predictability + 0.15 × Valuation + 0.10 × Runway
```

Where each dimension is rescaled to 0–100 from its star rating (★ = 20, ★★ = 40, ★★★ = 60, ★★★★ = 80, ★★★★★ = 100; half-stars allowed in 10-point steps).

Tier mapping for the composite (used to colour the card border):

| Composite | Tier | Display |
|---|---|---|
| 80–100 | 🟢 Buffett-grade | "Likely a Buffett candidate" |
| 65–79  | 🟡 Watchlist | "Buffett-grade quality, check price/data first" |
| 50–64  | 🟠 Borderline | "Mixed signals — not Buffett's typical pick" |
| 0–49   | 🔴 Not Buffett | "Outside the framework — consider Graham or other lens" |

---

## 4. Verdict matrix (quality × price)

The card's one-line verdict uses this matrix. Do **not** average stars — pick the cell. The matrix takes Dimension 1 (moat) + Dimension 3 (financials/predictability) as the "quality" axis and Dimension 4 (valuation) as the "price" axis.

| | Price 充足 / 一般 | Price 偏贵 | Price 高估 |
|---|---|---|---|
| **Moat wide + clean financials (★★★★+ on D1 and D3)** | 🟢 大概率会买 / Likely buy — initiate position, phased | 🟡 可能会考虑 / Maybe — wait for price | 🔴 目前估值不合适 / Not at this price — great business, wrong price |
| **Moat wide, financial concerns** | 🟡 观察 / Watch — small position only if concerns explainable | 🔴 目前估值不合适 | 🔴 目前估值不合适 |
| **Moat narrow (★★★)** | 🟠 不是典型巴菲特候选 / Not a typical Buffett pick — consider Graham | 🔴 Pass | 🔴 Pass |
| **No moat (★★ or below)** | 🔴 Not a Buffett candidate — redirect to Graham | 🔴 Pass | 🔴 Pass |

The card verdict is the chosen cell's label verbatim. The selection rationale block expands on the chosen cell with concrete evidence.

---

## 5. Holding-period mapping

Derived from Dimension 1 width label combined with Dimension 4 tier. Every card surfaces a holding-period line; never omit it.

| Moat width | Suggested minimum hold | Operating note |
|---|---|---|
| Wide (★★★★★) | 5+ years (Buffett ideal: forever) | Significant drawdowns are buying opportunities, not exit triggers, provided moat is intact |
| Wide (★★★★) | 3–5 years | Semi-annual re-check; no thesis change → keep holding |
| Narrow (★★★) | 1–3 years | More frequent re-check; watch competitive structure changes |
| None (★★ or below) | Buffett framework does not apply | Redirect: `longbridge-graham-screener` or growth lens, with strict position-size cap |

If the user's stated capital horizon is < 3 years, warn explicitly in the user-education block that this framework is mismatched to the horizon — regardless of how high the moat rating is.

---

## 6. Position-building rhythm (for the user-education block)

Buffett's actual practice translated into retail-friendly rules:

- **Phased entry**: split target position into 3–4 tranches; never go all-in on day one.
- **Lower-price adds**: a 15–20% drawdown with thesis intact is a signal to add, not exit. Define this *before* entering.
- **Anchor on price discipline, not market timing**: write a "personal buy line" tied to the valuation tier (Dimension 4), and act only when price reaches it.
- **Quarterly re-check cadence**: once held, re-verify the five dimensions each quarter. Material change to Dimension 1 (moat) or Dimension 3 (predictability) is the only valid sell trigger; price moves alone are not.

---

## 7. Sensitivity guards (anti-overfitting)

- Threshold relaxation: user can lower the ROE floor to 12% or the gross margin floor to 25%, but never weaken filters silently. Echo any override back to the user in the Market Summary.
- Currency: assume the home currency of the listing venue (HKD / USD / CNY); do **not** mix currencies inside one card set. If the user requests a multi-market screen, run separate per-market batches and stack outputs with explicit currency headers.
- T-period alignment: prefer the most recently reported fiscal period per market (HK semi-annual + annual, US/SH/SZ quarterly). If a row uses an older period than its market peers, flag in the row note.
- Reconciliation tolerance is **3%** for the per-row checks; rows failing tolerance are dropped (not silently smoothed) and listed in the Data Anomaly footer.
- **Anti-cheat reminders**:
  - Never assert "wide moat" without naming the moat type AND pointing to at least two pieces of concrete evidence.
  - Never call a stock "cheap" on PE alone — cross-check PB, dividend-yield percentile, and the owner-earnings band.
  - If Dimension 1 ≤ ★★, do not award Dimension 4 a high score regardless of headline multiples — a low price on a no-moat business is a Graham question, not a Buffett one.
  - If history < 5 years, the symbol is excluded from default top-N; if shown on request, cap all dimension stars at ★★★ and tag "history-limited" everywhere it appears.
