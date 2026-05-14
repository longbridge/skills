---
name: longbridge-graham-stock-analysis
description: |
  Graham cigar-butt (NCAV / net-net) single-stock diagnostic. Combines a 100-point static cheapness score (NCAV, PE, PB, dividend yield, debt coverage, earnings stability) with a dynamic adjustment layer (industry cycle, earnings trend, insider activity, NCAV trajectory) to separate real bargains from value traps. Pulls data from Longbridge CLI first; MCP fallback if CLI unavailable; falls back to WebSearch only for gaps, runs cross-statement reconciliation (勾稽校验) before scoring, and footnotes every figure to its source. Triggers: "格雷厄姆", "捡烟蒂", "烟蒂股", "烟蒂投资", "NCAV", "净流动资产", "清算价值", "安全边际", "价值陷阱", "深度价值", "撿煙蒂", "煙蒂股", "煙蒂投資", "淨流動資產", "清算價值", "安全邊際", "價值陷阱", "深度價值", "Graham", "cigar butt", "net-net", "liquidation value", "value trap", "margin of safety", "deep value", "Benjamin Graham".
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: read_only
  requires_login: false
  default_install: true
  requires_mcp: false
  tier: analysis
---

# longbridge-graham-stock-analysis

Prompt-only deep-value diagnostic. Given a single ticker, produces a Graham-style cigar-butt verdict: static cheapness score, dynamic trend adjustments, value-trap flagging, liquidation-value table, and an expected holding-period view. Every numeric input is reconciled across statements and footnoted to its source.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

- *"帮我诊断一下腾讯控股 00700"* / *"幫我診斷一下騰訊控股 00700"* / *"diagnose 700.HK with Graham cigar-butt"*
- *"BABA 是不是烟蒂股"* / *"BABA 是不是煙蒂股"* / *"is BABA a Graham net-net"*
- *"600519 NCAV 多少"* / *"600519 NCAV 多少"* / *"what is 600519's NCAV"*
- *"我持有这只股 6 个月了，还值得继续拿吗"* / *"我持有這隻股 6 個月了，還值得繼續拿嗎"* / *"I've held this 6 months, still worth holding"*
- *"这只股是真便宜还是价值陷阱"* / *"這隻股是真便宜還是價值陷阱"* / *"is this a real bargain or a value trap"*

For multi-stock value screening use `longbridge-value-screen`. For DCF intrinsic value use `longbridge-dcf`. For three-statement reading use `longbridge-financial-report`.

## Cognitive frame (do not skip)

Graham cigar-butt is **patient arbitrage**, not a dip-buy signal. Expected holding periods: 6–18 months (explicit catalyst), 1–3 years (sector re-rating), 3–5 years (organic accrual), or never (value trap — exit). Every output must surface holding-period expectation alongside the score; never display a score number without it.

Two failure modes the user must be able to distinguish:
- **"Cheap but time hasn't come"** → NCAV stable, keep holding.
- **"Value trap"** → NCAV shrinking quarter on quarter, exit.

## Workflow

1. **Resolve symbol** to `<CODE>.<MARKET>` (e.g. `00700.HK`, `BABA.US`, `600519.SH`).
2. **Detect sector**. If banking / insurance / REIT / pure financial → halt and tell the user NCAV is not the right model; suggest `longbridge-valuation-methodology` instead.
3. **Fetch raw data via Longbridge CLI first** (parallel where possible). See [§CLI](#cli).
4. **Reconciliation gate** (勾稽校验) — internal correctness check; must pass before scoring. Do **not** print this check or its results in the report unless it fails. See [§Reconciliation](#reconciliation-勾稽校验-internal-gate-not-user-facing).
5. **Static score** (0–100). See `references/scoring.md` for the six-dimension table and NCAV haircut defaults.
6. **Dynamic adjustments** — four factors (industry cycle, earnings trend, insider activity, NCAV trajectory). Industry-cycle data may not be in Longbridge; use WebSearch for PMI / inventory cycle / capacity utilisation. See `references/scoring.md` §Dynamic.
7. **Value-trap check** — if any 2 of 5 rules trip, override to "⚠️ value trap" regardless of static score. See `references/scoring.md` §Value-trap.
8. **Output** the 8-section report defined in `references/output.md`; finish with the **Data source appendix** (mandatory — every figure tagged to its source).

## CLI

Run `longbridge <subcommand> --help` to verify exact flags before each call. Primary calls (run in parallel):

```bash
# Balance sheet — NCAV inputs (cash, AR, inventory, other CA, ST/LT debt)
longbridge financial-report <SYMBOL> --kind BS --report af --format json   # last 5 annual
longbridge financial-statement <SYMBOL> --kind BS --report qf --format json   # last 4 quarterly (NCAV trajectory)

# Income statement — PE, earnings stability (5y no-loss), EPS trend (4q)
longbridge financial-report <SYMBOL> --kind IS --report af --format json
longbridge financial-report <SYMBOL> --kind IS --report qf --format json

# Cash flow — operating CF (value-trap rule 4: persistent negative OCF)
longbridge financial-report <SYMBOL> --kind CF --report qf --format json

# Snapshot: PE, PB, market cap, dividend yield, shares outstanding
longbridge calc-index <SYMBOL> --format json
longbridge quote <SYMBOL> --format json

# Dividend history (for "等待成本" — 3% threshold)
longbridge dividend <SYMBOL> --format json

# Ownership / insider activity (value-trap rule 2: 大股东持续减持)
longbridge ownership <SYMBOL> --format json
longbridge insresearch <SYMBOL> --format json
```

### WebSearch fallback (only when Longbridge has a gap)

Use WebSearch **only** for items not available from Longbridge:

| Missing data | WebSearch query pattern |
|---|---|
| Industry PMI / inventory cycle | `"<industry name> PMI 2025"`, `"<industry> inventory cycle"`, `"中国制造业PMI"` |
| Capacity utilisation | `"<industry> capacity utilization"` |
| Sector outlook (qualitative) | `"<sector> outlook 2025 site:reuters.com OR site:bloomberg.com"` |
| Recent insider transactions if `ownership` is stale | `"<ticker> insider selling 2025"` |

Each WebSearch-sourced figure must be tagged `[Source: WebSearch — <publisher>, <date>]` in the appendix; do **not** mix it silently with Longbridge data.

## Reconciliation (勾稽校验) — internal gate, not user-facing

Before any scoring, verify the fetched figures internally. **Reconciliation is a correctness gate for the analysis pipeline; it is not part of the user-facing report.** Do not print the check table, do not show per-row gap percentages, do not narrate "勾稽通过" in the conclusion. Reconciliation results only surface to the user in two situations:
- A check fails by > tolerance → **halt scoring**, tell the user which specific figure(s) cannot be relied on and why no score is emitted.
- A field carries a residual gap *within* tolerance that materially affects a downstream number → note it inline in the **Data Source Appendix** row for that field (e.g. "BS current-assets sum −1.4% vs reported total — within tolerance").

| Check | Formula | Tolerance |
|---|---|---|
| IS↔BS | This-period net income ≈ Δ Retained earnings (BS) − dividends paid (CF) | ±3% |
| IS↔CF | Net income + non-cash items (D&A + impairments + WC changes) ≈ Operating CF | ±5% |
| CF↔BS | ΔCash from CF = Cash(t) − Cash(t−1) on BS | ±1% |
| Current assets sum | Cash + AR + Inventory + Other CA ≈ Total current assets (BS) | ±2% |
| Liabilities sum | ST debt + LT debt + Other liabilities ≈ Total liabilities (BS) | ±2% |
| Shares outstanding | `calc-index` shares × current price ≈ market cap from `quote` | ±2% |
| Period alignment | All statements from the same fiscal period (or note the lag) | exact |

Silent-pass principle: if everything passes within tolerance, emit the scored report directly without referencing the reconciliation step at all.

## Output

Single-stock diagnostic with **8 fixed sections** (full template in `references/output.md`). The reconciliation check is an internal gate — do NOT include its table or pass/fail rows in the user-facing report; reconciliation only appears if a check failed (in which case no score is emitted) or if a residual within-tolerance gap needs to be flagged inline against a specific Data Source Appendix row.

1. Adjusted cigar-butt score card (静态分 → 动态调整 → 调整后分, with verdict tier 🟢🟡🟠🔴)
2. Six-dimension static breakdown (NCAV / PE / PB / dividend / debt coverage / earnings stability)
3. Dynamic adjustment detail (industry cycle, EPS trend, insider activity, NCAV trajectory, value-trap verdict)
4. Holding-period view (catalyst presence, waiting cost via dividend yield, expected horizon range)
5. Liquidation-value table (default vs industry-adjusted haircuts, adjusted NCAV per share)
6. Safety-margin price band (current price / default NCAV line / adjusted NCAV line / Graham buy line = adjusted NCAV × 0.67)
7. Three-line summary (valuation level / adjusted safety margin / Graham quantitative assessment — neutral, factual, no buy/sell recommendation)
8. **Data source appendix** — mandatory; every figure tagged with source, fetch time, and period (and any within-tolerance reconciliation note for that field)

Always close with the boilerplate disclaimer (see `references/output.md` §Disclaimer).

> **Compliance note**: The three-line summary in section 7 must be stated as objective metric readings, not directional recommendations. For example:
> - "当前价格低于格雷厄姆计算的内在价值估算，符合格雷厄姆 NCAV 量化标准（仅供参考）" — not "建议买入 / 低估值建议关注".
> - "Current price is below the Graham-derived intrinsic value estimate and meets Graham NCAV quantitative criteria (for reference only)" — not "consider buying" or "recommended".
> - The output must conclude with: 以上内容仅供参考，不构成投资建议。投资决策请结合自身风险承受能力独立判断。/ The above is for reference only and does not constitute investment advice. Please make investment decisions independently based on your own risk tolerance.

## Error handling

| Situation | 简体回复 | 繁體回覆 | English reply |
|---|---|---|---|
| `command not found: longbridge` | 回退到 MCP；若不可用，请安装 longbridge-terminal。 | 回退到 MCP；若不可用，請安裝 longbridge-terminal。 | Fall back to MCP; if unavailable install longbridge-terminal. |
| stderr `not logged in` | 请运行 `longbridge auth login`。 | 請執行 `longbridge auth login`。 | Run `longbridge auth login`. |
| Sector = bank / insurance / REIT | NCAV 模型不适用于金融业，已切换提示；建议使用 `longbridge-valuation-methodology`。 | NCAV 模型不適用於金融業，建議使用 `longbridge-valuation-methodology`。 | NCAV does not fit financials; use `longbridge-valuation-methodology`. |
| Reconciliation fails >3% | 明确披露差异项与差异比例，不输出评分；建议用户复核或换数据源。 | 明確披露差異項與差異比例，不輸出評分。 | Disclose the failing check and the gap; do not emit a score. |
| Industry cycle data missing (WebSearch also empty) | 标注「动态调整层数据不足，仅显示静态评分」。 | 標注「動態調整層數據不足，僅顯示靜態評分」。 | Mark "dynamic layer unavailable, static score only". |
| < 5 years of financial history | 盈利稳定性维度按已披露年限按比例打分，并在数据源附录注明。 | 盈利穩定性按已披露年限比例打分，並於附錄註明。 | Score earnings stability pro-rata and note in source appendix. |

## MCP fallback

If `longbridge` CLI is not installed, use MCP tools:

| MCP tool | CLI equivalent |
|---|---|
| `mcp__longbridge__financial_report` | `longbridge financial-report` |
| `mcp__longbridge__financial_statement` | `longbridge financial-statement` |
| `mcp__longbridge__calc_indexes` | `longbridge calc-index` |
| `mcp__longbridge__quote` | `longbridge quote` |
| `mcp__longbridge__dividend` | `longbridge dividend` |
| `mcp__longbridge__ownership` | `longbridge ownership` |

MCP setup: `claude mcp add --transport http longbridge https://openapi.longbridge.com/mcp` (`quote` scope).

## Related skills

- Single-stock valuation (PE / PB / EV-EBITDA) → `longbridge-valuation`
- DCF intrinsic value → `longbridge-dcf`
- Multi-stock value screen → `longbridge-value-screen`
- Three-statement reading → `longbridge-financial-report`
- Cross-statement deep analysis → `longbridge-financial-analysis`
- Method selection guide → `longbridge-valuation-methodology`

## File layout

```
longbridge-graham-stock-analysis/
├── SKILL.md
└── references/
    ├── scoring.md      # static six-dimension table + NCAV haircuts + dynamic factors + value-trap rules
    └── output.md       # full 8-section output template + data-source appendix + disclaimer
```
