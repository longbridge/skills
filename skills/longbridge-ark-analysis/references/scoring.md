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

**C — Data basis insufficient**
The company is pre-revenue, listed for less than two fiscal years, or has no scale revenue history; the TAM × share × margin model has no anchor point.
*Example phrasing — "The company has not yet reached commercial scale; the model lacks data anchors."*

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

## TAM rules

TAM numbers are central to the model and easy to fabricate. The skill enforces source priority and explicit labelling.

### Source priority

| Priority | Source type | Examples | Where to find it |
|---|---|---|---|
| 1 | Authoritative research house | Gartner, IDC, Forrester, BloombergNEF, IRENA, McKinsey Global Institute | WebSearch with publisher in query |
| 2 | Company self-disclosure | IR deck, annual report, prospectus TAM statement | `longbridge sec-filings` + WebSearch |
| 3 | Academic / think-tank | Stanford AI Index, Epoch AI, RethinkX, NHGRI | WebSearch |
| 4 | ARK Invest public reports | ARK Big Ideas annual (free) | `site:ark-invest.com big ideas` |
| 5 | Internal estimate | Logic-based bottom-up | Must be tagged `估算` (estimated) — never given a fake publisher |

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
| TAM | Use TAM-high | Use TAM-base | Use TAM-low |
| Company market share at year 5 | Aggressive but defensible | Mid-path | Slower share gain |
| Net margin at year 5 | Scale-economy + Wright's-Law tail | Industry-adjusted | Margin compression |
| Terminal multiple (P/E or P/S) | Sector mature-stage upper band | Sector mature-stage median | Sector mature-stage lower band |

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

- TAM assumption error (alternative authority's TAM differs by ≥ 3x).
- Market-share assumption error (competitor TBD; slower-than-expected adoption).
- Margin / Wright's-Law shortfall (learning rate stalls or commoditisation eats margin).
- Multiple compression (sector de-rates from current to mature-stage low band earlier than year 5).
- Regulatory / policy disruption (specific bill, agency, jurisdiction).
- Capital structure / dilution (cash burn forces equity raises; share count grows materially over 5 years).
- Technology substitution (a newer architecture leapfrogs the current curve — name it specifically).
- Concentration risk (single customer / single product / single regulator > 30%).

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
