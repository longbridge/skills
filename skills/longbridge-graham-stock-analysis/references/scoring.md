# Scoring detail — static + dynamic + value trap

Loaded by `longbridge-graham-stock-analysis` SKILL.md on demand. Do not edit numeric defaults without updating the SKILL examples in lockstep.

## Formula

```
Adjusted cigar-butt score = Static score (0–100) − Dynamic deductions + Dynamic credits
```

The static score is a time-snapshot of cheapness. The dynamic layer corrects for trend signals that make a cheap statement either credible or treacherous.

---

## Static score (0–100)

| Dimension | Calculation | Max | Graham threshold |
|---|---|---|---|
| **NCAV ratio** | Market cap ÷ (haircut current assets − total liabilities) | 25 | Market cap < NCAV × 0.67 → full marks |
| **PE (TTM)** | Trailing 12-month | 20 | PE < 10 full marks; PE > 20 zero; linear in between |
| **PB** | Market cap ÷ shareholders' equity | 15 | PB < 1.0 full marks; PB > 3.0 zero; linear |
| **Dividend yield** | TTM dividend ÷ current price | 15 | > 5% full marks; 0% zero; linear |
| **Debt coverage** | Current assets ÷ total liabilities | 15 | > 2.0 full marks; < 1.0 zero; linear |
| **Earnings stability** | 5y consecutive no-loss record | 10 | 5y no loss full marks; subtract 2 per loss year |

If history < 5 years, score earnings stability pro-rata on available years and note this in the data-source appendix.

## NCAV haircut defaults (industry-neutral)

```
Cash & equivalents          × 100%
Accounts receivable          × 75%   (bad-debt risk)
Inventory                    × 50%   (liquidity risk)
Other current assets         × 25%   (weak realisation)

Total liabilities (ST + LT)  × 100%   (full deduction, no haircut)
```

These are defaults under industry-neutral conditions; the dynamic layer may revise them downward in downturns (see below). Adjusted NCAV must always be reported alongside the default NCAV, never in isolation.

---

## Dynamic adjustment layer

Four factors, applied **after** the static score. Each contributes a deduction (or in two cases a credit).

| Factor | What to evaluate | Score impact |
|---|---|---|
| **Industry cycle** | PMI / inventory cycle / capacity utilisation trend (last 3–6 months) | Downturn: cut inventory haircut from 50% → 30%, AR from 75% → 55%; rescore NCAV; up to −15 from the dimension's contribution |
| **Earnings trend** | Last 4-quarter EPS direction (sequential) | Persistent decline up to −15; persistent improvement up to +10 |
| **Insider / market signal** | Major-holder net buy/sell over last 2 quarters; analyst rating shifts; institutional flow | Persistent insider selling → flag "⚠️ value-trap watch" and −10 |
| **Balance-sheet trajectory** | NCAV direction over last 3 quarters | Persistent shrinkage → ×0.8 multiplier on final score and warn; persistent expansion → +5 |

**Adjustment cap**: industry haircut adjustments are clamped to ±30% of the default coefficient. Document the source for the industry-cycle judgment (Longbridge if available, otherwise WebSearch with publisher + date).

### Example breakdown

```
Static cigar-butt score:    82
Dynamic adjustments:        −18
  · Industry downturn (rescored NCAV with tightened haircuts):  −8
  · NCAV shrinking 3 quarters in a row:                          −7
  · Mild insider selling:                                        −3

Adjusted cigar-butt score:  64  🟡
⚠️ Cheap on the surface, but trend signals warrant caution.
   Recommendation: small position, wait for NCAV to stabilise before adding.
```

---

## Value-trap override (price-blind)

If **any 2 of the following 5** trip, override the final verdict to "⚠️ Value-trap risk — cigar-butt logic not recommended" regardless of static score:

1. NCAV has contracted > 10% for 3 consecutive quarters.
2. Major-holder net selling persists for > 2 consecutive quarters.
3. Industry PMI stays below 50 with no policy offset.
4. Operating cash flow has been negative for several consecutive quarters (paper profit, no cash).
5. Accounts-receivable growth persistently outpaces revenue growth (earnings-quality decay).

---

## Verdict wording matrix

| State | Output line |
|---|---|
| Static high + dynamic clean | "Cheap and stable — Graham would be interested. Plan for a 1–3-year hold." |
| Static high + mild dynamic warning | "Cheap, but the reason is real — try a small position and watch the trend." |
| Static high + strong dynamic warning | "⚠️ Numerically cheap, but fundamentals are deteriorating — could be a value trap, proceed cautiously." |
| Static low + dynamic improving | "Not cheap enough yet, but fundamentals are turning — add to watchlist and wait for a lower price." |

## Final score → tier mapping

| Adjusted score | Tier | Verdict line |
|---|---|---|
| 80–100 | 🟢 Cigar-butt grade | "Cheap and steady — be ready for a 1–3-year hold." |
| 60–79 | 🟡 Undervalued candidate | "Skewed cheap, but trend signals have nicks — small position, observe." |
| 40–59 | 🟠 Fair value | "Not cheap enough, or the discount is suspicious — watch only." |
| 0–39 | 🔴 Avoid | "Either expensive, or clear value-trap risk." |
