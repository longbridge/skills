---
name: longbridge-financial-analysis
description: |
  Deep financial statement analysis for listed companies via Longbridge — cross-statement reconciliation (IS↔BS↔CF), DuPont decomposition (ROE = net margin × asset turnover × equity multiplier), earnings-quality scoring (accrual ratio), and 10-item financial fraud red-flag checklist. Builds on raw data from longbridge-financial-report. Triggers: "三表勾稽", "杜邦分析", "杜邦拆解", "盈利质量", "应计利润", "财务造假", "财报深度", "财务红旗", "三表分析", "財務深度", "三表勾稽", "杜邦分析", "盈利質量", "應計利潤", "財務造假", "財報深度", "財務紅旗", "DuPont analysis", "accrual ratio", "earnings quality", "financial fraud red flags", "cross-statement reconciliation", "three-statement analysis".
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: read_only
  requires_login: false
  default_install: true
  requires_mcp: false
  tier: read
---

# longbridge-financial-analysis

Prompt-only analysis skill. Fetches complete three-statement financials via Longbridge CLI and performs deep in-LLM analysis: cross-statement reconciliation, DuPont decomposition, earnings-quality scoring, and fraud red-flag detection.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

- *"TSLA 三表勾稽"*, *"TSLA cross-statement reconciliation"*, *"TSLA 三表勾稽"*
- *"茅台杜邦分析"*, *"Maotai DuPont decomposition"*
- *"NVDA 盈利质量"*, *"NVDA accrual ratio"*, *"NVDA 盈利質量"*
- *"700.HK 有没有财务造假红旗"*, *"700.HK financial fraud red flags"*
- *"AAPL 三表分析"*, *"AAPL three-statement analysis"*

For raw statement data only use `longbridge-financial-report`. For health scoring use `longbridge-financial-checkup`.

## CLI

Always run `longbridge financial-report --help` to verify exact flags. Primary call:

```bash
# Fetch all three statements — required for reconciliation and DuPont
longbridge financial-report <SYMBOL> --kind ALL --format json

# If unsure about period flags, run:
longbridge financial-report --help
```

## Workflow

1. **Resolve symbol** to `<CODE>.<MARKET>` (e.g. `TSLA.US`, `700.HK`, `600519.SH`).
2. **Call CLI** with `--kind ALL` to retrieve IS, BS, and CF in one request.
3. **In-LLM analysis** — perform all three layers:

### Layer 1 — Cross-statement reconciliation (三表勾稽)

| Check | Formula |
|---|---|
| IS → BS | Net income (IS) ≈ ΔRetained earnings (BS); large gap flags earnings manipulation |
| IS → CF | Net income + non-cash items (depreciation, SBC, etc.) ≈ Operating CF (CF) |
| CF → BS | Net ΔCash (CF) = ΔCash & equivalents (BS) |

### Layer 2 — DuPont decomposition (杜邦拆解)

ROE = Net margin × Asset turnover × Equity multiplier

Compute each driver; compare YoY to diagnose whether ROE change is quality-driven (margin/turnover) or leverage-driven.

### Layer 3 — Earnings quality & fraud red flags

**Accrual ratio** = (Net income − Operating CF) / Avg total assets — lower is better; > 5% warrants scrutiny.

**10 fraud red flags** — flag each as present / absent:
1. Accounts receivable growth > Revenue growth
2. Inventory growth >> Revenue growth
3. Gross margin sharp unexpected change
4. Operating CF persistently below Net income (> 2 consecutive years)
5. Related-party receivables / revenue rising
6. Auditor change or qualified opinion
7. Large "other income" or non-recurring gains propping earnings
8. Revenue concentration spike (single customer > 50%)
9. Capex spike without revenue growth follow-through
10. Cash & equivalents declining while reported profit is rising

4. Output structured analysis report; cite **Longbridge Securities**; end with disclaimer.

## Output

```
{Symbol} Deep Financial Analysis — Source: Longbridge Securities
Period: {report_period}

[Cross-statement reconciliation]
- IS→BS: Net income {X} vs ΔRetained earnings {Y}: {Match / Gap of Z — flag}
- IS→CF: Net income + non-cash {X} vs Operating CF {Y}: {Match / Gap}
- CF→BS: Net ΔCash {X} vs ΔCash on BS {Y}: {Match / Gap}

[DuPont decomposition]
ROE {X%} = Net margin {Y%} × Asset turnover {Z×} × Equity multiplier {W×}
YoY: ROE {±Δ%} — driven by {margin / turnover / leverage / mix}

[Earnings quality]
Accrual ratio: {X%} ({Low <2% / Medium 2-5% / High >5%})
Assessment: {earnings are cash-backed / partly accrual-driven / accrual-heavy}

[Fraud red flags (10-item)]
✓ / ✗  1. AR growth vs revenue growth: ...
✓ / ✗  2. Inventory growth vs revenue: ...
... (all 10 items)
Red flags triggered: {N}/10

⚠️ 以上分析仅供参考，不构成投资建议。/ 以上分析僅供參考，不構成投資建議。/ For reference only. Not investment advice.
```

## Error handling

| Situation | 简体中文回复 | 繁體中文 / English |
|---|---|---|
| `command not found: longbridge` | 回退到 MCP；如 MCP 也不可用，请安装 longbridge-terminal。 | 回退到 MCP；如也不可用，請安裝 longbridge-terminal。/ Fall back to MCP; if also unavailable, install longbridge-terminal. |
| stderr `not logged in` | 请运行 `longbridge auth login` 登录。 | 請執行 `longbridge auth login`。/ Run `longbridge auth login`. |
| Missing one or more statements | 跳过依赖缺失报表的分析层，注明原因。 | 跳過依賴缺失報表的分析層，注明原因。/ Skip analysis layers that depend on missing statements; note reason. |
| Returns empty / no data | "{symbol} 暂无财务报表数据。" | "{symbol} 暫無財務報表數據。" / "{symbol} has no financial statement data." |
| Other stderr | 直接显示原始错误，不静默重试。 | 顯示原始錯誤。/ Surface verbatim — do not retry silently. |

## MCP fallback

If `longbridge` CLI is not installed, use MCP tools:

| MCP tool | CLI equivalent |
|---|---|
| `mcp__longbridge__financial_report` | `longbridge financial-report --kind ALL` |

MCP setup: `claude mcp add --transport http longbridge https://openapi.longbridge.com/mcp` (`quote` scope).

## Related skills

- Raw three-statement data → `longbridge-financial-report`
- Health scoring (100-point) → `longbridge-financial-checkup`
- Quick KPI snapshot → `longbridge-fundamental`
- Valuation (PE / PB) → `longbridge-valuation`

## File layout

```
longbridge-financial-analysis/
└── SKILL.md   # prompt-only, no scripts/
```
