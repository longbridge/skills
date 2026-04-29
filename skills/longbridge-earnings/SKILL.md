---
name: longbridge-earnings
description: >
  Post-earnings analysis skill — generates institutional-grade earnings update reports
  (8–12 page DOCX) and structured conversation summaries for companies under coverage.
  Covers beat/miss analysis, segment breakdown, margin trends, guidance assessment,
  updated estimates, and valuation. Supports US, HK, and A-share markets.
  Use this skill whenever the user wants a post-earnings analysis or quarterly-results
  writeup, even if they do not say "earnings update" verbatim. Triggers: "earnings update",
  "quarterly results", "Q1/Q2/Q3/Q4 results", "earnings report", "post-earnings analysis",
  "beat/miss", "guidance update", "财报分析", "业绩更新", "季度业绩", "季报", "年报",
  "盈利分析", "财报点评", "財報分析", "業績更新", "季度業績", "季報", "年報", "財報點評".
---

# Earnings Update Skill

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English. Both the DOCX report body and the in-chat summary follow the user's language; chart labels, axis titles, and file names always stay in English.
## When to Use

| Trigger | Example |
|---------|---------|
| Post-earnings analysis | "Analyze TSLA.US latest earnings" / "帮我分析腾讯最新财报" |
| Specific quarter update | "Tencent Q4 2024 earnings update" / "业绩更新" |
| Quarterly results | "Q1/Q2/Q3/Q4 results for [company]" |

**Do not trigger if:** user wants an initiation report.

## Output Language
## Data Sources

Priority: **CLI (primary) → Web Search (supplement)**

Use the Longbridge CLI for all market data. Before using any command, run `longbridge <command> --help` to check available options — the CLI is updated frequently.

**⚠️ CLI + Python pattern — always use temp file, never inline pipe:**

```bash
# CORRECT
longbridge institution-rating 700.HK --format json > /tmp/rating.json
python3 -c "import json; d=json.load(open('/tmp/rating.json')); print(d)"

# WRONG — zsh escapes characters inside -c "..." and causes TypeError/SyntaxError
longbridge institution-rating 700.HK --format json | python3 -c "import json,sys; ..."
```

**CLI docs**: https://open.longbridge.com/zh-CN/docs/cli/
**MCP endpoint**: `https://openapi.longbridge.com/mcp`

Key CLI entry points for earnings analysis:

| Data Needed | CLI Entry Point |
|-------------|----------------|
| Filings & reports | `longbridge filing --help` |
| Financial statements | `longbridge financial-report --help` |
| Analyst consensus & estimates | `longbridge consensus --help` |
| Quote & valuation metrics | `longbridge quote --help` / `longbridge calc-index --help` |
| Price history | `longbridge kline --help` |
| Analyst ratings | `longbridge institution-rating --help` |
| News | `longbridge news --help` |

Web Search supplements for content not in CLI: consensus estimates vintage, earnings call transcripts, M&A precedent data.

## Execution Workflow

**Step 1 — Identify reporting period**
Use `longbridge filing --help` to find the latest quarterly or annual filing. Confirm the period with the user before proceeding.

**Step 2 — Collect data & analyze**
See [references/workflow.md](references/workflow.md)

**Step 3 — Update valuation**
See [references/valuation-methodologies.md](references/valuation-methodologies.md)

**Step 4 — Generate DOCX report**
See [references/report-structure.md](references/report-structure.md)

**Step 5 — Output conversation summary**
See [references/summary-card-spec.md](references/summary-card-spec.md)

## Output

1. **DOCX report**: `[SYMBOL]_Q[N]_[YEAR]_Earnings_Update.docx` (8-12 pages, 8-12 charts)
2. **Conversation summary**: 8-module structured output directly in chat

**IMPORTANT**: Do NOT append a Sources section or reference links to the conversation output. All citations belong in the DOCX only.

## Reference Files

| File | Contents | When to Read |
|------|----------|--------------|
| [workflow.md](references/workflow.md) | Data collection steps, beat/miss framework, segment/margin/guidance analysis | Before analysis |
| [valuation-methodologies.md](references/valuation-methodologies.md) | DCF, trading comps, precedent transactions — full methodology | During valuation |
| [report-structure.md](references/report-structure.md) | Page-by-page DOCX templates, table and chart formatting, citation rules | Before generating report |
| [summary-card-spec.md](references/summary-card-spec.md) | 8-module conversation summary format with examples | When outputting summary |
| [best-practices.md](references/best-practices.md) | Quality checklist, common mistakes, headline examples | Quality check |
