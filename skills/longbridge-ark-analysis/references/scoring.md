# Scoring rubric — suitability gate · TAM rules · Wright's-Law learning rates · scenario formula

Loaded by `longbridge-ark-analysis` SKILL.md on demand. Do not edit numeric thresholds without updating SKILL.md examples in lockstep.

---

## Suitability

ARK methodology is a gate, not a soft preference. A name is either inside the disruptive-innovation envelope or outside; if outside, do **not** produce a "for reference" ARK report.

### Five innovation platforms (one or more must apply)

Aligned with ARK Invest's most recent Big Ideas framing. Each platform is evaluated as a value chain — a company can sit on **any tier** (upstream / core / downstream) and still be in-platform, provided its revenue depends materially on that tier's economics.

> Example tickers below are for **orientation only**, not recommendations. If a name appears here, it does **not** auto-pass the suitability gate — the four-dimension scoring still applies.

#### Platform 1 — Artificial Intelligence

Foundation models, agentic AI, AI compute, AI-native applications. ARK's emphasis in recent reports has shifted from "AI as a feature" to "AI as a general-purpose platform" — compute infrastructure, software agents, and enterprise productivity.

| Tier | Examples of in-tier business | Example tickers |
|---|---|---|
| Upstream | AI accelerators, advanced-packaging, HBM memory, foundry capacity, networking silicon | NVDA, AVGO, AMD, TSM, ASML, MU |
| Core | Foundation-model platforms, hyperscale cloud, AI training/inference platforms | MSFT, GOOGL, META, ORCL |
| Downstream | AI-native enterprise software, agentic workflow, data-analytics platforms | PLTR, NOW, CRM, SNOW |
| Adjacent infra | Data-center power, cooling, electrical equipment for AI build-out | VRT, ETN, CEG, VST |

#### Platform 2 — Robotics & Autonomous Mobility

Autonomous taxis, humanoid robots, drones, industrial automation, machine vision. Humanoid robotics has been **newly elevated** in ARK's recent Big Ideas and should be treated as a first-class direction.

| Tier | Examples of in-tier business | Example tickers |
|---|---|---|
| Upstream | LIDAR, sensors, precision actuators, robotics motors, vision chips | MBLY, OUST, KEYS |
| Core | Autonomous platforms, humanoid robotics, robotaxi operators, drone platforms | TSLA, GOOGL (Waymo), PATH, ABB |
| Downstream | Autonomous ride-hailing demand, robotic logistics, automated warehouse | UBER, AMZN, SHOP (logistics arm) |
| Adjacent infra | Industrial-automation OEMs, machine-vision systems | ROK, FANUY, EMR |

#### Platform 3 — Energy Storage & EV Adoption

EVs, battery technology, grid storage, charging infrastructure. ARK frames this as the **EV S-curve adoption story** plus the Wright's-Law battery-cost curve.

| Tier | Examples of in-tier business | Example tickers |
|---|---|---|
| Upstream | Lithium / cobalt / nickel miners, battery materials, cell makers, separator film | ALB, SQM, CATL, LG Energy Solution, Panasonic |
| Core | EV OEMs, vertically integrated battery + vehicle platforms | TSLA, BYD, RIVN, LI, NIO |
| Downstream | Charging networks, fleet electrification, EV insurance / financing | CHPT, EVgo, BLNK |
| Adjacent infra | Stationary grid storage, home energy storage, microinverters, solar inverters | ENPH, SEDG, FLNC |

#### Platform 4 — Multiomic Sequencing & AI Drug Discovery

Gene editing, multiomic sequencing, AI-driven drug discovery, precision medicine, synthetic biology. ARK's recent emphasis is the **AI × Genomics convergence** — AI compressing both discovery cost and trial timelines.

| Tier | Examples of in-tier business | Example tickers |
|---|---|---|
| Upstream | Sequencers, long-read platforms, reagents, lab equipment | ILMN, PACB, ONT, TMO, DHR |
| Core | Gene-editing therapeutics, AI-drug-discovery platforms, mRNA platforms | CRSP, NTLA, BEAM, RXRX, SDGR, ABCL |
| Downstream | Liquid biopsy, cancer diagnostics, precision-medicine assays | EXAS, NTRA, GH, NVTA |
| Adjacent | Synthetic biology platforms, cell & gene therapy CDMOs | DNA, ZY, CRL |

#### Platform 5 — Public Blockchains & Digital Assets

Bitcoin, public layer-1 blockchains, stablecoins, on-chain finance, tokenization of real-world assets, on-chain payments. ARK's recent framing emphasizes **bitcoin as a monetary network**, **stablecoins as payment rails**, and **tokenization as the bridge to traditional finance**.

| Tier | Examples of in-tier business | Example tickers |
|---|---|---|
| Upstream | Mining ASICs, mining-fleet operators, low-cost power for mining | MARA, RIOT, CLSK, HUT |
| Core | Crypto exchanges, custody, on-chain protocols, bitcoin treasury vehicles | COIN, HOOD (crypto), MSTR |
| Downstream | Stablecoin issuers/distributors, on-chain payments, tokenization platforms | SQ / Block, PYPL (stablecoin rail) |
| Adjacent | Wallet infrastructure, smart-contract dev tools, RWA tokenization | (largely private; tag via WebSearch) |

### Convergence themes (cross-platform — ARK's recent emphasis)

ARK's recent Big Ideas reports lean heavily on **platform convergence**. Where a name straddles two platforms via convergence, name both in the suitability section and treat the convergence as a strengthening signal — not a weakening one.

| Convergence | Description | Example exposure |
|---|---|---|
| AI × Robotics | Foundation-model intelligence inside physical robots (humanoid, autonomous vehicles, factory bots) | TSLA (Optimus + FSD), Figure AI (private), GOOGL (Waymo) |
| AI × Multiomic | AI compresses drug-discovery cost & trial timelines; lab-in-the-loop biology | RXRX, SDGR, ABCL, NVDA (BioNeMo) |
| AI × Blockchain | Autonomous on-chain agents, AI-native crypto protocols | (mostly private; track via ARK Big Ideas + WebSearch) |
| Robotics × Energy Storage | EVs as data + battery platforms; vehicle-to-grid energy economics | TSLA, BYD |
| Blockchain × Energy | Bitcoin mining as flexible grid load; renewable-powered mining | CLSK, MARA |
| Multiomic × Robotics | Lab automation, automated cell engineering | (largely private; e.g. Ginkgo via DNA) |

A company can sit on more than one platform; for dual-platform / convergence names, name both in the report and treat the convergence as a positive signal in the management-vision dimension.

### Four-dimension suitability scoring

Each dimension is tagged **强 (strong) / 中 (medium) / 弱 (weak)** with one-line evidence.

| Dimension | Source | 强 (strong) | 中 (medium) | 弱 (weak) |
|---|---|---|---|---|
| Platform fit | `basicinfo` + `company-profile` + recent `news` | Core business clearly inside ≥ 1 platform's **core or upstream** tier, OR on a convergence (e.g. AI × Robotics) | Business sits in **downstream / adjacent infrastructure** tier of a platform, OR partial exposure not the main P&L | No meaningful overlap with the five platforms at any tier |
| Innovation revenue share | `financial-report --kind IS` (segment mix) + recent earnings deck | Innovation-related revenue (across all in-platform tiers) > 50% | 20% – 50% | < 20% |
| R&D intensity | `financial-report --kind IS` (R&D ÷ revenue) | Materially above industry median | Near industry median | Below industry median |
| Management innovation vision | `news` + `sec-filings` + IR materials | Quantified innovation roadmap in deck / call / letter; named platform or convergence direction | Innovation mentioned but no quantification | No clear innovation narrative |

> When **Young-company mode** is active, dimensions are evaluated on whatever periods exist (pro-rated, tagged history-limited in the appendix) and the **Management innovation vision** bar is raised — see [§Young-company mode](#young-company-mode) for the exact adjustments and the additional forward-looking inputs required.

### Pass / reject matrix

| Combination | Result |
|---|---|
| All four 强, OR three 强 + one 中 | ✅ Pass — proceed with full analysis |
| Two 强 + two 中 | ✅ Pass — mark in report: *"Framework applies; some assumptions are lower-confidence"* |
| Any single dimension is **弱** on platform fit OR innovation revenue | ❌ Reject |
| Two or more dimensions are **弱** | ❌ Reject |

---

## Reject reasons (use the closest fit; quote it verbatim in the report)

When the suitability gate fails, the report must say *why* using one of these four canonical reasons (do **not** invent a fifth, do **not** dilute with "but maybe a partial view…").

**A — Traditional industry**
Revenue is driven by macro cycles, regulation, brand & distribution; growth path does not ride a technology cost curve, so a TAM × share × margin disruptive-growth model cannot be built.
*Example phrasing — "Construction Bank's profits depend on net interest spread and loan volume, not on technology diffusion speed."*

**B — Being disrupted**
The company belongs to a legacy industry that is the target of disruption. This framework analyses **disruptors**, not the disrupted.
*Example phrasing — "ExxonMobil is on the receiving end of storage / EV displacement, not the disruptor."*

**C — Data basis insufficient (genuinely pre-revenue)**
The company is **truly pre-revenue** — no recurring product or service revenue, or revenue is < ~$10M annualised with no clear path to commercial scale within 18 months; the TAM × share × margin model has no anchor point at all.
*Example phrasing — "The company has not yet reached commercial revenue scale; the model lacks any data anchor."*

> ⚠️ **Important distinction**: do **not** use reason C just because a company has been listed for < 3 years. Many ARK-style disruptors (RIVN, RXRX, IONQ, BEAM, NTLA, COIN's recent business pivot) have **scale revenue but short public history** — those names enter [§Young-company mode](#young-company-mode), they are **not rejected**. Reason C is reserved for names with **no commercial revenue base at all**.

**D — Disruption premium already realised**
The core technology has matured; Wright's-Law cost decline is already largely priced into the current multiple, with limited remaining curve.
*Example phrasing — "Apple's supply-chain efficiency is already industry benchmark; the cost-curve dividend is largely tapped out."*

---

## Alternative-method matching (when rejecting)

Recommend 1–2 methods from the **currently installed skill library** based on the rejected name's signals. Do not hard-code specific skill names here — the actual recommendation must be drawn from the live skill set; this table is the **matching logic**, not the recommendation itself.

Match priorities (higher priority wins):

1. **Valuation signal** — PB or PE in historical / sector low quantile → recommend a value / safety-margin method (e.g. Graham, Buffett).
2. **Dividend signal** — dividend yield > 3%, ≥ 5 consecutive years of payouts, healthy FCF → recommend a dividend / income method.
3. **Growth signal** — revenue growth > 15%, ROE consistently > 15%, but **not** in a disruptive platform → recommend a fundamental-growth method.
4. **Short-horizon signal** — user phrasing contains "短期 / 今天 / 明天 / pattern / signal" → recommend a technical / price-action method.
5. **Cross-market / asset-class signal** — HK-specific, A-share-specific, options, ETF → recommend the market / asset-class method.

Output format (per alternative recommended):
- **Method name** (from the live skill library)
- **Why this fits**: one or two specific sentences citing *this* company's data — never generic.

If no method in the live library is a clean match, say so plainly: *"No matching method in the current library; suggest reviewing basic data first."* Never force-fit an unrelated method.

---

## Young-company mode

Many ARK-style disruptors have **scale revenue but short public history**: 1–3 fiscal years since IPO, often pre-profit, capital structures that are still evolving, and a thesis that lives almost entirely in the **next** 3–5 years rather than in the past 5–10. The skill must analyse these names — not reject them — and lean explicitly on forward-looking inputs.

### Trigger (any one is sufficient)

A name enters Young-company mode if **any** of the following holds:

- Listed (or commercial revenue-recognising) for **< 3 fiscal years** at the as-of date.
- **< 3 fiscal years** of scale revenue (≥ ~$50M trailing 12 months — adjust threshold to industry; for biotech / hardware-pre-launch, use commercial milestone instead).
- Business model **pivoted within the last 2 years** to a new platform tier (e.g. MSTR's bitcoin-treasury pivot, COIN's stablecoin/derivatives pivot, PLTR's commercial AI pivot) — old history is not meaningful for the new thesis.
- Post-SPAC / post-IPO < 12 months and no comparable peer with similar revenue mix.

If none of these hold but commercial revenue exists with ≥ 3 years of history → **standard mode**. If revenue is truly absent or trivial (< ~$10M annualised, no commercial pathway in 18 months) → **reject under reason C**, not Young-company mode.

### What changes when Young-company mode is active

| Aspect | Standard mode | Young-company mode |
|---|---|---|
| History windows | 5–10 years preferred | **Whatever exists**, pro-rated; tagged `history-limited (N quarters)` in appendix |
| Innovation revenue share dimension | Computed on TTM with multi-year trend | Computed on TTM; trend window may be a single year; tag the short window |
| R&D intensity dimension | Compared to multi-year sector median | Compared to current-year sector median; one-off spikes from a small revenue base are explained, not penalised |
| Management innovation vision dimension | Quantified roadmap is "strong" | **Higher bar** — quantified roadmap **with specific milestones, capacity numbers, and dated regulatory or commercial gates** is now the "strong" bar. Vague "we believe in this market" is "weak". |
| Reconciliation gate | All 12 checks at full tolerance | Same 12 checks, but **period-alignment** uses whatever periods exist; checks that require N-year history are pro-rated and the appendix says so |
| Three-scenario inputs | Anchored on revenue-growth trajectory + margin history | Anchored on **TAM × share × margin** plus **dilution-adjusted share count**; backward operating leverage is a secondary input only |
| Risk catalogue | Standard 8 items | Standard 8 + 4 young-company-specific items (see [§Risk catalogue](#risk-catalogue)) |

### Forward-looking inputs (required in Young-company mode)

These inputs **must** appear in section [2b] of the output and have appendix rows. If any cannot be sourced (no consensus, no IR deck guidance, no regulatory pathway disclosure), the report must say so and **cap suitability at 中 (medium) on the management-vision dimension**.

| Input | Source priority | Why it matters |
|---|---|---|
| **Forward revenue consensus (next 4–8 quarters)** | `longbridge analyst-estimates` → `longbridge consensus` → IR deck guidance | Anchors the slope from current revenue to year-5 implied revenue |
| **Cash runway** = cash + ST investments ÷ trailing-4Q burn rate | `financial-report --kind BS` + `financial-report --kind CF` | If runway < 18 months, equity raise is near-certain — affects dilution assumption |
| **5-year dilution path** | `longbridge corporate` (share-count history) + S-1 / 10-K share-authorisation footnotes + recent ATM filings | The model's year-5 shares-outstanding input — must reflect realistic dilution, not current count |
| **Capex / capacity roadmap** | IR deck, earnings call transcripts, `sec-filings` | Anchors when scale economics turn on |
| **Regulatory / commercial milestone calendar** | `sec-filings` + WebSearch (FDA, FCC, agency dockets), industry calendar | The next observation node for the action frame |
| **Customer pipeline / pilot list** | IR deck, recent `news`, earnings call transcripts | Validates the "demand exists" leg of the thesis |
| **Technology readiness signal** | Peer-reviewed papers, regulatory clearances, certified benchmarks | Distinguishes "technology proved" from "technology hoped-for" |

### How the three-scenario model adjusts

- **Year-5 shares outstanding** must use the dilution path, not current shares. If model implies a 30% share-count increase by year 5 from cash-burn raises, all three scenarios use the diluted count.
- **Bull case** still uses ARK incumbent-displacement TAM, but the **path from current revenue to year-5 revenue** must clear a sanity check: implied CAGR consistent with the highest analyst forecast within 1.5× headroom. If Bull implies a CAGR more than 1.5× the high-end consensus, **flag it explicitly** in the assumption row — "this Bull case assumes execution materially above current sell-side consensus".
- **Bear case** must include a **runway-exhaustion sub-scenario**: if cash runway < 24 months, Bear scenarios must price in a dilutive raise at a discount to current price.
- The output report **must show year-5 implied share count next to year-5 implied price** so the reader can spot dilution drag.

### Reconciliation under Young-company mode

The 12 reconciliation checks still apply. Specific accommodations:

- **History windows** in checks that span periods (e.g. "BS — current assets sum") apply to whatever periods exist; the appendix labels each affected row `history-limited (N quarters)`.
- **Innovation-revenue share / R&D ratio** consistency checks still apply on the available period — these are intra-period, not multi-year.
- **Period alignment** is enforced strictly: if IS covers FY{a}–FY{b} but CF only covers FY{b−1}–FY{b}, the appendix names both periods.
- The reconciliation summary line in the appendix still uses the standard variants (✅ / ⚠️ / ❌); no separate "young-company" variant — the history-limited tag lives on individual appendix rows, not on the summary.

---

## TAM rules

TAM numbers are central to the model and easy to fabricate. The skill enforces source priority and explicit labelling.

### ARK TAM definition (use this lens, not consensus new-market TAM)

ARK's TAM is **not** "the size of the new service market" — it is **the total incumbent spend that the technology is going to displace**, computed bottom-up:

```
TAM = incumbent-market unit count × $/unit (the old-economy spend being replaced)
```

This lens is typically **10–100× larger** than consensus research-house TAM, because it measures the entire economy block being substituted, not the new service's standalone market.

| Disruption area | ❌ Consensus new-market TAM (do not use as primary) | ✅ ARK-lens TAM (use this) | WebSearch suggestion |
|---|---|---|---|
| Autonomous driving / Robotaxi | Mobility-as-a-service market $100–400B | Global passenger miles × $/mile ≈ $10T+ total transport spend | `"global transportation spending" 2030` |
| Energy storage / EV | EV sales market $1–2T | Global ICE car + fuel + maintenance total spend ≈ $5–8T | `"global automotive market" "fuel spend" 2030` |
| AI & data | Cloud-AI services market $500B | Global enterprise IT / software spend being displaced by AI ≈ $3–5T | `"global enterprise IT spending" 2030` |
| Genomic revolution | Gene therapy / diagnostics market $500B | Global pharma R&D + treatment spend being displaced ≈ $1–2T | `"global pharmaceutical market" 2030` |
| Blockchain / fintech | Crypto market / DeFi TVL | Global financial-services revenue being disintermediated ≈ $20T+ | `"global financial services revenue" 2030` |

**Bottom-up computation (when no single authority covers the full incumbent market):**

1. Find the incumbent unit count (vehicles on the road, annual approved drugs, enterprise data bytes, etc.).
2. Find the average spend per unit ($/mile, $/prescription, $/GB).
3. Multiply: incumbent units × $/unit = displacement TAM.
4. Tag it `估算 — bottom-up incumbent displacement` — the method itself is ARK's published approach and the components have sources, so this does not count as fabrication.

**Tier mapping under the ARK lens:**

- **High / optimistic** → use the **ARK incumbent-displacement TAM** above.
- **Base** → use a **consensus research-house figure** (Grand View, Mordor, MarketsandMarkets, Gartner, IDC, etc.).
- **Low / conservative** → use a **serviceable sub-segment** (e.g. for RKLB only small-launch; for TSLA only robotaxi share-gain).

The plain-language analogy in the report must explain to the reader why these three tiers can differ by 10–30×, and which lens each tier reflects.

### Source priority

| Priority | Source type | Examples | Where to find it |
|---|---|---|---|
| 1 | Authoritative research house | Gartner, IDC, Forrester, BloombergNEF, IRENA, McKinsey Global Institute | WebSearch with publisher in query |
| 2 | Company self-disclosure | IR deck, annual report, prospectus TAM statement | `longbridge sec-filings` + WebSearch |
| 3 | Academic / think-tank | Stanford AI Index, Epoch AI, RethinkX, NHGRI | WebSearch |
| 4 | ARK Invest public reports | ARK Big Ideas annual (free) | `site:ark-invest.com big ideas` |
| 5 | Internal estimate | Logic-based bottom-up (incl. ARK incumbent-displacement) | Must be tagged `估算` (estimated) — never given a fake publisher |

### Three tiers

| Tier | Definition |
|---|---|
| Low / conservative | Slower adoption curve, narrower addressable users, lower per-user spend |
| Base | Mid-point assumption with current trajectory |
| High / optimistic | Faster adoption, full TAM penetration, higher per-user value |

Each tier line in the report must carry: numeric value, **assumption-in-one-sentence**, source row reference.

### When no authoritative TAM exists

- Use phrasing: *"TAM has no citable authoritative figure; the range shown is a logic-based estimate."*
- Appendix row must say `估算 — <one-line basis>`, never a fabricated publisher name.
- Do not present estimated TAM in deterministic tone (use "approx.", "in the range of").

---

## Wright's Law

**Wright's Law**: each doubling of cumulative production cuts unit cost by a fixed percentage (the learning rate).

### Reference learning rates (use as **lookup direction**, verify current value via WebSearch)

| Technology domain | Historical learning rate | Authoritative source | Verification query |
|---|---|---|---|
| Lithium-ion battery cells | ~18% | BloombergNEF Electric Vehicle Outlook (annual) | `"battery learning rate" BloombergNEF` |
| Solar PV modules | ~28% | IRENA Renewable Power Generation Costs (annual) | `"solar PV learning rate" IRENA` |
| DNA sequencing cost | ~40% | NHGRI (US National Human Genome Research Institute) | `"DNA sequencing cost" NHGRI learning rate` |
| LLM / AI compute & inference | ~30–40% | Epoch AI, MLCommons benchmark series | `"AI compute cost" learning rate "Epoch AI"` |
| Autonomous-driving miles cost | per ARK Big Ideas | ARK Invest Big Ideas | `site:ark-invest.com "autonomous" learning rate` |

### Rules

- **Never** present the historical figure above as the current learning rate without a verifying WebSearch. The embedded numbers are search direction, not citable data.
- If the WebSearch turns up nothing for the technology in question, the report must say: *"No publicly available authoritative learning rate for this technology; the curve discussion is qualitative."* — and the appendix row says `无权威数据 / no authoritative source` rather than carrying a number.
- The plain-language framing must always explain why this matters: *"If the technology's cumulative output doubles again, the unit cost roughly drops by X%, which is when the market unlocks."*

---

## Scenario — 5-year target price formula

### Variables (must be visible per scenario)

| Variable | Bull (optimistic) | Base | Bear (pessimistic) |
|---|---|---|---|
| TAM | ARK incumbent-displacement TAM (存量市场口径) | Consensus research-house TAM | Serviceable sub-segment (conservative subset) |
| Company market share at year 5 | Platform winner-take-most: **40–70%** (strong network effects) / **20–40%** (defensible moat, competitive market) | Competitive equilibrium midpoint: **15–30%** | Penetration stalls: **5–15%** |
| Net margin at year 5 | Pure software / platform (zero marginal cost): **60–90%**; hardware + software hybrid: **25–45%** | Industry-adjusted midpoint: **15–30%** | Competitive compression: **5–15%** |
| Terminal multiple (P/E or P/S) | Still in high-growth at year 5 (>30%/yr revenue growth): **P/E 60–100×** or **P/S 15–25×**; growth slowing (15–30%): **P/E 35–60×** | Growth normalising (10–20%): **P/E 25–40×** | Growth into single digits: **P/E 15–25×** |

**Terminal-multiple selection logic (key ARK-method departure):**

ARK does **not** mechanically compress the multiple to a "mature-stage P/E". Instead, the multiple is chosen based on **which point on the growth curve the company is still on at year 5**.

- Decision rule: if year-5 revenue growth is projected to still be >30%/yr, disruption is **not yet complete** — use a growth-stage multiple, not a mature-stage one.
- Calibration anchor: **PEG ≈ 1**.
  - Growth ~40% → reasonable P/E ≈ 40×.
  - Growth ~70% → reasonable P/E ≈ 70×.
- The chosen multiple per scenario must be reported alongside the implied year-5 growth rate so the reader can spot-check the PEG.

### Formula (per scenario)

```
Year-5 revenue         = TAM × market share
Year-5 net income      = Year-5 revenue × net margin
Year-5 enterprise val  = Year-5 net income × terminal P/E
                          OR Year-5 revenue × terminal P/S
Year-5 implied price   = Year-5 enterprise val ÷ year-5 shares outstanding
Discounted target      = Year-5 implied price ÷ (1 + r)^5     where r = 0.15 by default
```

Default discount rate is **15%** (ARK reference for innovation risk). If the user supplies a different discount rate, use theirs and **note the override on the diagnostic line**.

### Weighting

Default scenario weights: **Bull 25% / Base 50% / Bear 25%**.

```
Weighted target = Bull-target × 0.25 + Base-target × 0.50 + Bear-target × 0.25
```

If the user supplies custom weights, must sum to 1.0 and be visible in the report.

### Upside framing

```
Upside vs current = (weighted target − current price) ÷ current price
```

Framing in the report:
- Upside **> 50%**: per ARK heuristics, significant model-implied upside (not a guarantee — restate the disclaimer in this line).
- Upside **0% – 50%**: model expectation in line with current price; the bet is on scenario probabilities.
- Upside **< 0%**: current price exceeds the model's weighted expectation; the bet must rely on TAM, share, or multiple exceeding the bull case.

Never use the phrase "expected return"; use "model-implied 5-year price" / "model expectation". The Bull case is **not** a prediction.

---

## Risk catalogue (pick 3 named risks — never generic boilerplate)

For each report, surface exactly **three** risks, drawn from this catalogue. Each must be tied to *this* company's data, not abstract.

**Standard items (all modes):**

- TAM assumption error (alternative authority's TAM differs by ≥ 3x).
- Market-share assumption error (competitor TBD; slower-than-expected adoption).
- Margin / Wright's-Law shortfall (learning rate stalls or commoditisation eats margin).
- Multiple compression (sector de-rates from current to mature-stage low band earlier than year 5).
- Regulatory / policy disruption (specific bill, agency, jurisdiction).
- Capital structure / dilution (cash burn forces equity raises; share count grows materially over 5 years).
- Technology substitution (a newer architecture leapfrogs the current curve — name it specifically).
- Concentration risk (single customer / single product / single regulator > 30%).

**Young-company-specific items (in Young-company mode, at least one of the three risks must come from this group):**

- **Cash runway exhaustion** — current cash + ST investments ÷ burn rate is < 24 months, equity raise is near-certain, at what valuation is uncertain.
- **Dilution path** — if cash burn continues, year-5 share count grows by N% (cite source) — anything above ~25% materially erodes per-share target.
- **Execution / scale-up risk** — unit economics inflection has not yet been demonstrated; bull case requires it within 18–36 months.
- **Tech-readiness gap** — bull-case assumptions require regulatory / technical milestones (named, with target dates) that are not yet achieved; risk that they slip beyond 5-year horizon.

---

## Holding-period framing (for the action-frame block)

ARK methodology is a **5-year** lens.

- If the user states a horizon < 3 years, the report's action frame must include a warning that this framework is mismatched to the horizon — regardless of the upside number.
- The action-frame block uses condition-based sentences only: *"If you believe X, the current price implies you are paying for scenario Y. If signal Z fails to appear by date D, reconsider the thesis."* — never a buy/sell command.
- Always include one explicit next-observation node (e.g. *"Q3 vehicle delivery print on YYYY-MM-DD"*, *"FDA decision on indication X by YYYY-MM-DD"*).

---

## Anti-cheat reminders

- Never produce a "partial / for reference" ARK report on a rejected name. Reject means reject.
- Never present a single point target. Always Bull / Base / Bear with assumptions visible.
- Never use the embedded historical learning rates as the current value without verifying via WebSearch.
- Never give TAM a fabricated publisher. Estimates are labelled `估算`.
- Never use the words "buy", "sell", "strongly recommend", or "must hold" in the action frame.
- Never present ARK's historical performance (ARKK ETF) as a credibility anchor for this skill — the skill is independent from ARK Invest.
- Never default to "mature-stage P/E" for a company still growing revenue at >30% at year 5 — use PEG ≈ 1 as the calibration anchor.
- Never use consensus new-market TAM as the High tier. The High tier must be ARK-style incumbent-displacement TAM; consensus goes to Base; conservative sub-market goes to Low. Explain the difference in the plain-language block.
- Never reject a name under reason C just because it has short public history. If it has commercial revenue, enter Young-company mode and lean on the forward-looking inputs — reject reason C is reserved for **truly pre-revenue** names.
- In Young-company mode, never skip the forward-looking inputs (cash runway, dilution path, capacity roadmap, regulatory milestones, customer pipeline). If any cannot be sourced, cap management-vision at 中 and say so — do **not** silently fill them with optimistic placeholders.
- In Young-company mode, never use current shares outstanding as the year-5 input if the model's cash runway is < 24 months — use the dilution-adjusted share count and show it in the output.
- Never let a Bull-case revenue CAGR exceed 1.5× the highest sell-side analyst forecast without an explicit flag in the assumption row.
