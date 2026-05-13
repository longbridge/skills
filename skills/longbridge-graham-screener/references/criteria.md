# Screening criteria — hard filters, static scoring, dynamic adjustments, value-trap override

Loaded on demand by `longbridge-graham-screener`. Numeric defaults are aligned with Graham's *Intelligent Investor* (defensive investor chapter) with light modernisation; do not change without updating SKILL.md and `output.md` examples in lockstep.

---

## 1. Hard filters (pass / fail gate)

Apply these as a binary pre-filter. A symbol that fails ≥ 2 filters drops out of the leaderboard by default (user can relax to "fail ≤ 3" on request).

| # | Filter | Default threshold | Source field |
|---|---|---|---|
| 1 | NCAV ratio = market cap ÷ haircut NCAV | < 1.0 ideal, < 1.5 acceptable | derived from `financial-report --kind BS` + `calc-index` market cap |
| 2 | PE (TTM) | < 10 (defensive investor) | `calc-index.pe_ttm` |
| 3 | PB | < 1.5 | `calc-index.pb` |
| 4 | Dividend yield (TTM, cash dividends only) | > 3% | `dividend` rollup ÷ `quote.last_done` |
| 5 | Current assets ÷ total liabilities | > 2.0 | BS — current assets total ÷ (ST + LT debt + other) |
| 6 | Consecutive no-loss years | ≥ 5 | `financial-report --kind IS --report af` — last 5 fiscal years |

**Haircut NCAV (industry-neutral defaults)** — used in filter #1 and in scoring:

```
Cash & equivalents          × 100%
Accounts receivable          ×  75%   (bad-debt risk)
Inventory                    ×  50%   (liquidity risk)
Other current assets         ×  25%   (weak realisation)
Total liabilities (ST + LT)  × 100%   (no haircut)
```

Adjusted NCAV per share = (Σ haircut current assets − total liabilities) ÷ shares outstanding. The Graham buy line = adjusted NCAV per share × 0.67.

---

## 2. Static composite score (0–100) — per symbol

Use this as the leaderboard rank key by default.

| Dimension | Calculation | Max | Full-marks rule |
|---|---|---|---|
| NCAV ratio | market cap ÷ haircut NCAV | 25 | < 0.67 full; linear to 1.5; 0 above |
| PE (TTM) | trailing 12-month | 20 | < 10 full; 0 at PE > 20; linear in between |
| PB | market cap ÷ equity | 15 | < 1.0 full; 0 at PB > 3.0; linear |
| Dividend yield | TTM cash dividend ÷ price | 15 | > 5% full; 0 at 0%; linear |
| Debt coverage | current assets ÷ total liabilities | 15 | > 2.0 full; 0 at < 1.0; linear |
| Earnings stability | 5y consecutive no-loss record | 10 | 5y full; −2 per loss year; pro-rata for IPOs < 5y of history |

Cap the total at 100. Pro-rated earnings-stability scoring must be annotated in the row note ("数据局限 / IPO < 2y").

---

## 3. Dynamic adjustment layer (applied after static)

Four factors. Each contributes a deduction or (in two cases) a credit. Use Longbridge data first; fall back to WebSearch only for industry-cycle inputs.

| Factor | What to evaluate | Score impact |
|---|---|---|
| **Industry cycle** | PMI / inventory cycle / capacity utilisation over last 3–6 months | Downturn: tighten haircuts (inventory 50% → 30%, AR 75% → 55%) and rescore NCAV; up to −15 from the dimension's contribution |
| **Earnings trend** | Last 4-quarter EPS direction (sequential) | Persistent decline up to −15; persistent improvement up to +10 |
| **Insider / market signal** | Major-holder net buy/sell over last 2 quarters; analyst rating shifts | Persistent selling → flag "⚠️ value-trap watch" and −10 |
| **Balance-sheet trajectory** | NCAV direction over last 3 quarters | Persistent shrinkage → ×0.8 multiplier on final score + warn; persistent expansion → +5 |

**Industry haircut adjustments are clamped to ±30% of the default coefficient.** Document the source for the industry-cycle judgement in the Data Source Appendix (Longbridge if available, WebSearch otherwise with publisher + URL + date).

```
Adjusted score = Static (0–100) − Dynamic deductions + Dynamic credits
```

---

## 4. Value-trap override (price-blind)

If **any 2 of the following 5** trip for a row, override the row's verdict to **"⚠️ 价值陷阱风险 / Value-trap risk — 不建议捡烟蒂"** regardless of static or adjusted score. The row stays in the table but its tier becomes 🔴.

1. NCAV contracted > 10% for 3 consecutive quarters.
2. Major-holder net selling persists for > 2 consecutive quarters.
3. Industry PMI stays below 50 with no policy offset.
4. Operating cash flow negative for several consecutive quarters (paper profit, no cash).
5. Accounts-receivable growth persistently outpaces revenue growth (earnings-quality decay).

---

## 5. Tier mapping (used in the leaderboard "动态预警" column)

| Adjusted score | Tier | Display |
|---|---|---|
| 80–100 | 🟢 Cigar-butt grade | "便宜且稳定 / Cheap and steady" |
| 60–79  | 🟡 Undervalued candidate | "倾向便宜，趋势有缺口 / Skewed cheap, trend nicks" |
| 40–59  | 🟠 Fair value | "不够便宜或折价可疑 / Not cheap enough or discount suspicious" |
| 0–39   | 🔴 Avoid | "太贵或明显价值陷阱风险 / Expensive or clear trap risk" |

Any row with the value-trap override set is forced to 🔴 with verdict "⚠️ Value-trap risk".

---

## 6. NCAV-inapplicable cohorts — excluded from the universe

NCAV is meaningless for businesses whose balance sheet is dominated by financial assets. The screener **excludes** these from the universe before scoring; it does NOT run substitute models. This keeps the leaderboard a clean Graham/NCAV ranking instead of mixing different valuation lenses under one rank key.

| Sector / state | Action | Display in Market Summary |
|---|---|---|
| Banks (commercial / investment) | Excluded | "Excluded — NCAV inapplicable (banks)" |
| Insurance (life / P&C / reinsurance) | Excluded | "Excluded — NCAV inapplicable (insurance)" |
| REITs / real-estate income trusts | Excluded | "Excluded — NCAV inapplicable (REITs)" |
| Pure financial holdings / asset managers / brokers | Excluded | "Excluded — NCAV inapplicable (financial holdings)" |
| Negative-equity firms | Excluded | "Excluded — negative equity" |
| Pure holding / shell companies | Excluded | "Excluded — holding/shell" |

Detection inputs: sector / industry code from `longbridge calc-index` or `longbridge basicinfo` (whichever exposes a GICS / industry tag); equity sign from the BS fetch. If sector classification is ambiguous, default to **include** and let the hard filters / reconciliation gate take care of it — better to keep a borderline candidate than silently drop it.

If the user wants any of these analysed, point them to `longbridge-valuation-methodology` (model selection) or `longbridge-valuation` (multi-method valuation). Do **not** add per-row scoring for excluded names in this skill.

---

## 7. Sensitivity guards (anti-overfitting)

- Threshold relaxation: user can raise NCAV-ratio ceiling to 2.0 or PE to 15, but never weaken filters silently. Echo any override back to the user in the market-summary block.
- Currency: assume the home currency of the listing venue (HKD / USD / CNY); do **not** mix currencies inside one leaderboard. If user requests a multi-market screen, run separate per-market batches and stack the outputs with explicit currency headers.
- T-period alignment: prefer the most recently reported fiscal period per market (HK semi-annual + annual, US/SH/SZ quarterly). If a row uses an older period than its market peers (e.g. half-year vs Q3), flag in the row note.
- Reconciliation tolerance is **3%** for the row-level checks; rows failing tolerance are dropped (not silently smoothed).
