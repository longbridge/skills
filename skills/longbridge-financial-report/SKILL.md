---
name: longbridge-financial-report
description: |
  Full three-statement financials (IS / BS / CF) for listed companies via Longbridge — income statement, balance sheet, cash flow statement; annual / semi-annual / quarterly periods. Use this skill to fetch raw financial data. For deep analysis (DuPont, accruals, fraud flags) use longbridge-financial-analysis; for health scoring use longbridge-financial-checkup. Triggers: "财务报表", "三张表", "利润表", "资产负债表", "现金流量表", "三表模型", "季报", "年报", "财报数据", "財務報表", "三張表", "利潤表", "資產負債表", "現金流量表", "三表模型", "季報", "年報", "財報數據", "financial statements", "income statement", "balance sheet", "cash flow statement", "three financial statements", "annual report data", "quarterly financials", "TSLA.US financials", "700.HK balance sheet".
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

# longbridge-financial-report

Prompt-only analysis skill. Fetches complete three-statement financials from Longbridge and performs cross-statement reconciliation, DuPont decomposition, and earnings-quality analysis in the LLM.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

- *"TSLA 三张表"*, *"TSLA three financial statements"*, *"TSLA 三張表"*
- *"700.HK 资产负债表"*, *"700.HK balance sheet"*, *"700.HK 資產負債表"*
- *"AAPL 现金流量表"*, *"AAPL cash flow statement"*, *"AAPL 現金流量表"*
- *"NVDA 三表勾稽分析"*, *"NVDA cross-statement reconciliation"*
- *"茅台 杜邦分析"*, *"Maotai DuPont decomposition"*
- *"TSLA 盈利质量"*, *"TSLA earnings quality"*, *"TSLA accruals"*

For a quick KPI snapshot use `longbridge-fundamental`. For valuation use `longbridge-valuation`.

## CLI

Run `longbridge financial-report --help` to verify exact flags before use. Primary calls:

```bash
# Fetch all three statements (preferred — one call)
longbridge financial-report TSLA.US --kind ALL --format json

# Or fetch individual statements
longbridge financial-report TSLA.US --kind IS --format json   # Income Statement
longbridge financial-report TSLA.US --kind BS --format json   # Balance Sheet
longbridge financial-report TSLA.US --kind CF --format json   # Cash Flow

# Period options (verify exact values with --help)
longbridge financial-report 700.HK --kind ALL --report af  --format json   # Annual
longbridge financial-report 700.HK --kind ALL --report saf --format json   # Semi-annual
longbridge financial-report 700.HK --kind ALL --report q1  --format json   # Q1
longbridge financial-report 700.HK --kind ALL --report 3q  --format json   # Three-quarter (9-month)
longbridge financial-report 700.HK --kind ALL --report qf  --format json   # Quarterly final

# If unsure about flags, always run first:
longbridge financial-report --help

# Note: v0.20.1 also adds `longbridge financial-statement` — different data structure
# (returns field-level rows with display_order/level hierarchy).
# Use financial-report for KPI extraction; use financial-statement for raw line-item access.
longbridge financial-statement <SYMBOL> --kind IS --report af --format json
```

## Workflow

1. **Resolve symbol** to `<CODE>.<MARKET>` format (e.g. `TSLA.US`, `700.HK`, `600519.SH`).
2. **Determine scope** from user intent:
   - Single statement requested → fetch that kind only.
   - Reconciliation / DuPont / earnings quality → fetch `--kind ALL`.
3. **Call CLI** (or MCP fallback). If `longbridge` not installed, fall back to MCP.
4. **In-LLM analysis** per requested depth:

   | Analysis | Method |
   |---|---|
   | **三表勾稽 / Cross-statement reconciliation** | Verify: net income (IS) ≈ change in retained earnings (BS); net income + non-cash items ≈ operating cash flow (CF); ΔCash (CF) = ΔCash (BS) |
   | **杜邦分解 / DuPont decomposition** | ROE = Net Margin × Asset Turnover × Equity Multiplier |
   | **盈利质量 / Earnings quality** | Accrual ratio = (Net Income − Operating CF) / Avg Total Assets; high positive ratio → earnings less cash-backed |

5. Output structured report; cite **Longbridge Securities**; end with disclaimer.

## Output template

```
{Symbol} ({code}) Financial Statements — Source: Longbridge Securities
Period: {report_period} | Report date: {rpt_date}

[Income Statement (IS)]
- Revenue: X  YoY ±Y%
- Gross profit / margin: X / Y%
- Operating income: X
- Net income: X  YoY ±Y%
- EPS (basic / diluted): X / Y

[Balance Sheet (BS)]
- Total assets: X
- Total liabilities: X  |  Debt-to-equity: Y%
- Cash & equivalents: X
- Shareholders' equity: X  |  Book value per share: Y

[Cash Flow (CF)]
- Operating CF: X
- Investing CF: X
- Financing CF: X
- Free cash flow (OCF − capex): X

[Cross-statement reconciliation]
- IS→BS: Net income vs ΔRetained earnings: {match / gap of X}
- IS→CF: Net income vs OCF bridge: {match / key non-cash items}
- CF→BS: ΔCash: {match / gap}

[DuPont decomposition]
ROE {X%} = Net margin {Y%} × Asset turnover {Z×} × Equity multiplier {W×}

[Earnings quality]
- Accrual ratio: X% — {low / medium / high} accrual, earnings are {cash-backed / partly accrual-driven / accrual-heavy}

⚠️ 以上数据仅供参考，不构成投资建议。/ 以上數據僅供參考，不構成投資建議。/ For reference only. Not investment advice.
```

(Omit sections not requested; state "data unavailable" rather than inventing.)

## Error handling

| Situation | 简体中文回复 | 繁體中文 / English |
|---|---|---|
| `command not found: longbridge` | 回退到 MCP；如 MCP 也不可用，请用户安装 longbridge-terminal。 | 回退到 MCP；如 MCP 也不可用，請安裝 longbridge-terminal。/ Fall back to MCP; if also unavailable, tell user to install longbridge-terminal. |
| stderr `not logged in` | 请运行 `longbridge auth login` 登录。 | 請執行 `longbridge auth login`。/ Run `longbridge auth login`. |
| Returns empty / no data | "{symbol} 暂无财务报表数据（可能为新上市或未覆盖标的）。" | "{symbol} 暫無財務報表數據。" / "{symbol} has no financial statement data (newly listed or not covered)." |
| Only one or two statements returned | 仅展示已返回的报表，注明缺失部分，不做勾稽。 | 僅展示已返回報表，注明缺失。/ Show available statements only; note missing ones; skip reconciliation. |
| Other stderr | 直接显示原始错误，不静默重试。 | 顯示原始錯誤。/ Surface verbatim — do not retry silently. |

## MCP fallback

If `longbridge` CLI is not installed (`command not found`), use MCP tools:

| MCP tool | CLI equivalent |
|---|---|
| `mcp__longbridge__financial_report` | `longbridge financial-report --kind ALL` |
| `mcp__longbridge__financial_statement` | `longbridge financial-statement --kind ALL` |
| `mcp__longbridge__latest_financial_report` | `longbridge financial-report --latest` |

MCP setup: `claude mcp add --transport http longbridge https://openapi.longbridge.com/mcp` (`quote` scope).

## Related skills

- Quick KPI snapshot → `longbridge-fundamental`
- Valuation (PE / PB / industry) → `longbridge-valuation`
- Analyst consensus & EPS forecasts → `longbridge-consensus`
- Industry peer comparison → `longbridge-peer-comparison`

## File layout

```
longbridge-financial-report/
└── SKILL.md   # prompt-only, no scripts/
```
