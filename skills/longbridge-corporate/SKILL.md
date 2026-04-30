---
name: longbridge-corporate
description: |
  Corporate-structure profile for a single listed company via Longbridge Securities — institutional/major shareholders, executives and key personnel, company overview (founding, employees, IPO, address), corporate actions (splits / dividends / rights / bonus), and parent–subsidiary investment relations. Read-only, single-symbol per call. Triggers: "谁是大股东", "股东结构", "管理层", "董事会", "公司简介", "公司基本信息", "拆股", "送股", "派息历史", "配股", "母公司", "子公司", "持股变动", "誰是大股東", "股東結構", "管理層", "公司簡介", "派息歷史", "持股變動", "shareholders", "major shareholders", "ownership structure", "executives", "management team", "board of directors", "company profile", "corporate actions", "splits", "rights issue", "bonus issue", "parent company", "subsidiaries", "AAPL.US shareholders", "700.HK executives".
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: read_only
  requires_login: false
  default_install: true
---

# longbridge-corporate

Single-symbol corporate profile: who owns the company, who runs it, what corporate actions it has taken, and how it relates to its parent / subsidiaries.

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

- *"AAPL 大股东都有谁"*, *"AAPL major shareholders"*, *"AAPL 大股東"* → `shareholder`
- *"700.HK 高管", "腾讯管理层", "AAPL board"* → `executive`
- *"NVDA 公司简介", "company overview", "員工人數", "上市价格"* → `company`
- *"特斯拉历史拆股", "TSLA splits", "700.HK 派息历史", "rights issue"* → `corp-action`
- *"700 母公司是谁", "AAPL 子公司有哪些", "subsidiaries"* → `invest-relation`
- *"X 公司基本面 (结构维度)", "全面公司画像"* → call several subcommands and merge

For financial KPIs (revenue / margin / EPS), use `longbridge-fundamental`. For valuation, use `longbridge-valuation`. For news / filings, use `longbridge-news`.

## Subcommands

> Run `longbridge <subcommand> --help` if unsure of current flags. The CLI's built-in help is the canonical source.

| CLI command | Returns |
|---|---|
| `longbridge shareholder <SYMBOL> --format json` | Institutional shareholders: name, related ticker, % held, share change, report date. Filters: `--range all\|inc\|dec`, `--sort chg\|owned\|time`, `--order desc\|asc`. |
| `longbridge executive <SYMBOL> --format json` | Executives and key personnel (officers, directors, key roles). |
| `longbridge company <SYMBOL> --format json` | Company overview: founding date, employees, IPO price, listing date, address, business description. |
| `longbridge corp-action <SYMBOL> --format json` | Corporate actions: stock splits, dividends, rights issues, bonus issues. |
| `longbridge invest-relation <SYMBOL> --format json` | Investment relations: parent company / subsidiaries / sister listings. |

Single symbol per call. The CLI accepts `--lang zh-CN` or `--lang en` for content fetched from longbridge.com (defaults to system `LANG`).

## Workflow

1. Resolve to `<CODE>.<MARKET>` (e.g. `AAPL.US`, `700.HK`).
2. Pick the matching subcommand from the prompt cue (table above).
3. For composite questions ("give me a full picture of X as a company") — call several subcommands concurrently and merge.
4. Render a structured summary; cite **Longbridge Securities** and the report date when applicable.

## CLI

```bash
longbridge shareholder AAPL.US                       --format json
longbridge shareholder AAPL.US --range inc --sort owned --format json
longbridge executive 700.HK                          --format json
longbridge company NVDA.US                           --format json
longbridge corp-action 700.HK                        --format json
longbridge invest-relation 700.HK                    --format json
```

If `--help` shows newer flags, follow the help output rather than hard-coding here.

## Output

Render results in the user's language. Suggested layouts:

**`shareholder`** — table of name / % held / change / report date. Highlight the top 3 by holding and any change > ±10% if `--range` is `all`.

**`executive`** — list of name / title / appointment date (if available). Group by role (CEO / CFO / Chair / others).

**`company`** — short profile paragraph: founding year, headquarters, employees, IPO date + price, business description.

**`corp-action`** — chronological list (most recent first): date / type (split / dividend / rights / bonus) / ratio or amount. Annotate split adjustments.

**`invest-relation`** — tree-like list: parent → company → subsidiaries (with stake % when available). Note cross-listed sister tickers.

When data is empty, state so explicitly (e.g. *"No corporate actions on record."*) — do not invent.

## Error handling

| Situation | Reply |
|---|---|
| Shell `command not found: longbridge` | Fall back to MCP if configured; otherwise tell the user to install longbridge-terminal. |
| stderr `not logged in` / `unauthorized` | These subcommands are public quote scope; if auth is requested, hint `longbridge auth login`. |
| Empty result (no shareholders / no actions) | State explicitly: *"No data for this symbol."* Do not invent. |
| Symbol mapping fails | Ask the user for the `<CODE>.<MARKET>` form. |
| Other stderr | Relay verbatim — never silently retry. |

## MCP fallback

When the CLI binary is missing, fall back via the equivalent MCP tool. Tool names typically mirror CLI subcommand names (snake_case).

| CLI subcommand | MCP tool |
|---|---|
| `shareholder` | `mcp__longbridge__shareholder` |
| `executive` | `mcp__longbridge__executive` |
| `company` | `mcp__longbridge__company` |
| `corp-action` | `mcp__longbridge__corp_action` |
| `invest-relation` | `mcp__longbridge__invest_relation` |

If a name above does not resolve, fall back via the equivalent MCP tool when CLI is missing.

## Related skills

| Skill | Why |
|---|---|
| `longbridge-fundamental` | Profitability / cash flow / dividend KPIs (the *numbers* side of the company). |
| `longbridge-flows` | Fund / ETF holders, insider trades, short interest, HK broker holdings. |
| `longbridge-news` | Recent filings and community discussion of corporate events. |
| `longbridge-valuation` | PE / PB lens once you know the company structure. |

## File layout

```
longbridge-corporate/
└── SKILL.md          # prompt-only, no scripts/
```
