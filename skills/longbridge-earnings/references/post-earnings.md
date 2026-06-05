# Earnings Update Skill

## Data Sources

Priority: **CLI (primary) → Web Search (supplement)**

Use the Longbridge CLI for all market data. Before using any command, run `longbridge <command> --help` to check available options — the CLI is updated frequently.

**CLI + Python pattern**: prefer reading from a file over piping into `python3 -c`. Multi-line JSON with embedded quotes can hit shell-quoting edge cases (especially under zsh's `-c` argument handling), so the safer pattern is:

```bash
longbridge institution-rating 700.HK --format json > /tmp/rating.json
python3 -c "import json; d = json.load(open('/tmp/rating.json')); print(d)"
```

If you do prefer pipes, use a heredoc-fed Python script (`python3 <<'PY' ... PY`) or save to a file and run a `.py` file.

**CLI docs**: https://open.longbridge.com/zh-CN/docs/cli/
**MCP endpoint**: `https://openapi.longbridge.com/mcp`

**CLI discovery**: Run `longbridge --help` to see all available subcommands, then `longbridge <subcommand> --help` before calling. Do not assume subcommand names — the CLI is updated frequently. Broad categories needed for earnings analysis:

- Earnings calendar / upcoming earnings dates
- Financial statements (income, balance sheet, cash flow)
- Earnings snapshot / AI beat-miss summary
- Analyst consensus & EPS estimates
- Quote & valuation metrics
- Price history (candlestick)
- Analyst ratings & target prices
- Regulatory filings (10-Q, 10-K, 8-K)
- News

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

| File                                                                | Contents                                                                     | When to Read             |
| ------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ------------------------ |
| [workflow.md](references/workflow.md)                               | Data collection steps, beat/miss framework, segment/margin/guidance analysis | Before analysis          |
| [valuation-methodologies.md](references/valuation-methodologies.md) | DCF, trading comps, precedent transactions — full methodology                | During valuation         |
| [report-structure.md](references/report-structure.md)               | Page-by-page DOCX templates, table and chart formatting, citation rules      | Before generating report |
| [summary-card-spec.md](references/summary-card-spec.md)             | 8-module conversation summary format with examples                           | When outputting summary  |
| [best-practices.md](references/best-practices.md)                   | Quality checklist, common mistakes, headline examples                        | Quality check            |
