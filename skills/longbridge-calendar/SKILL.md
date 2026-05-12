---
name: longbridge-calendar
description: |
  财经日历查询与持仓驱动的事件简报。默认生成持仓+自选股的完整财经日历报告（事件总览、影响解读、财报速递）；也支持按标的/市场/日期的轻量查询。Triggers: "财经日历", "今天有什么大事", "本周财报", "我的持仓近期有啥事件", "最近有啥事", "财报日历", "下周谁财报", "earnings calendar", "除权除息日", "派息日", "ex-dividend", "新股", "IPO 日历", "宏观数据", "非农", "CPI", "PCE", "美联储议息", "FOMC", "财报季", "休市日", "財經日曆", "下週誰財報", "除權除息日", "派息日", "新股", "IPO 日歷", "宏觀數據", "美聯儲", "FOMC", "財報季", "休市日", "earnings calendar", "ex-dividend dates", "IPO calendar", "macro calendar", "FOMC meeting", "CPI release", "non-farm payrolls", "market holidays", "trading closed days", "我的持倉近期有啥事件", "最近有啥事".
license: MIT
metadata:
  author: longbridge
  version: "1.1.0"
  risk_level: read_only
  requires_login: true
  default_install: true
---

# longbridge-calendar

财经日历：持仓驱动的事件简报 + 轻量事件查询。

> **Response language**: match the user's input language — Simplified Chinese / Traditional Chinese / English.

## When to use

**默认模式（生成报告）** — 用户问的是概览性问题时，走 `references/portfolio-briefing.md` 工作流：

- *"今天/本周/最近有什么大事"*
- *"我的持仓近期有啥事件"*
- *"财经日历"*、*"earnings calendar"*
- *"财报季来了，帮我看看"*

**轻量查询模式** — 用户指定了具体标的、事件类型或纯信息查询时，直接调 CLI 返回结果即可：

- *"NVDA 下次财报什么时候"* → `report --symbol NVDA.US`
- *"港股下周派息"* → `dividend --market HK`
- *"下周非农什么时候"* → `macrodata --star 3`
- *"美股下周休市吗"* → `closed --market US`

For a single stock's historical earnings → `longbridge-fundamental`. For watchlist-driven daily briefings → `longbridge-catalyst-radar`.

## Default workflow: portfolio briefing

这是默认执行路径。收到财经日历相关请求时，按 `references/portfolio-briefing.md` 完整执行：

1. 获取用户持仓与自选股（`references/data-fetching.md`）
2. 并行拉取所有日历数据（财报、宏观、分红、休市、拆合股）
3. 按时间范围筛选，生成三段式报告：
   - **事件总览** — 所有事件混合时间线（`references/output-template.md` 模板一）
   - **重点事件影响解读** — 高重要性事件深度展开（模板二，无则省略）
   - **财报结果速递** — 昨夜/盘前已出炉财报（模板三，无则省略）
4. 末尾附免责文案

详细字段规范、输出模板、语言规则均在 references 中定义。

## CLI reference

> Run `longbridge finance-calendar --help` if unsure of current flags. The CLI's built-in help is the canonical source.

```
longbridge finance-calendar <EVENT_TYPE> [OPTIONS]
```

| `<EVENT_TYPE>` | Returns |
|---|---|
| `financial` | Financial-period events. |
| `report` | Earnings releases (V2 rule: includes `financial` automatically). |
| `dividend` | Dividend ex-dates / pay-dates. |
| `ipo` | Upcoming initial public offerings. |
| `macrodata` | Macro data releases (CPI / NFP / FOMC / GDP / etc.). Use `--star 1\|2\|3` (repeatable) to filter by importance. |
| `closed` | Market closure days. |

Common options:

| Flag | Meaning |
|---|---|
| `--symbol <SYM>` | Filter by symbol; repeatable up to 10. With `--symbol`, default start date is 3 months ago; without, today. |
| `--market <MKT>` | Filter by market: `HK / US / CN / SG / JP / UK / DE / AU`; repeatable. |
| `--start YYYY-MM-DD` | Start date. Default: today (or 3 months ago when `--symbol` is set). |
| `--end YYYY-MM-DD` | End date. Default: no limit. |
| `--count N` | Max events (default 100). |
| `--star 1\|2\|3` | Macro importance, repeatable. Only effective for `macrodata`. |
| `--next later\|earlier` | Pagination direction (default `later`). |
| `--offset N` | Pagination offset. |
| `--format json\|table` | Output format. |

### CLI examples

```bash
# Earnings releases for the next 14 days, US + HK
longbridge finance-calendar report --market US --market HK --end 2026-05-12 --format json

# Specific tickers' upcoming earnings
longbridge finance-calendar financial --symbol AAPL.US --symbol TSLA.US --format json

# This month's ex-dividend dates in US
longbridge finance-calendar dividend --market US --format json

# High-importance macro (FOMC / CPI / NFP)
longbridge finance-calendar macrodata --star 3 --format json

# Upcoming IPOs in HK
longbridge finance-calendar ipo --market HK --format json

# Market closure days
longbridge finance-calendar closed --market US --format json
```

If `--help` shows newer flags, follow the help output rather than hard-coding here.

## Output

**Portfolio briefing mode** — follow `references/output-template.md` templates.

**Light query mode** — render in the user's language:

- **`report` / `financial`** — table grouped by date: date / time (BMO/AMC if available) / symbol / company name / period / consensus EPS (if returned).
- **`dividend`** — table: ex-date / record date / pay date / symbol / amount / currency.
- **`ipo`** — table: subscription window / listing date / symbol / company / price range / market.
- **`macrodata`** — table: date+time / region / event / importance stars / forecast / previous. Group by date.
- **`closed`** — list: date / market / reason.

When a result is empty for the chosen window, say so explicitly and offer to widen the window or check another market.

## Error handling

| Situation | Reply |
|---|---|
| Shell `command not found: longbridge` | Fall back to MCP if configured; otherwise tell the user to install longbridge-terminal. |
| stderr `not logged in` / `unauthorized` | Hint `longbridge auth login`. |
| Empty result | State explicitly. Offer to widen the window or remove a filter. |
| Invalid date format | Re-prompt with `YYYY-MM-DD`. |
| Other stderr | Relay verbatim — never silently retry. |

## MCP fallback

When the CLI binary is missing, fall back via the equivalent MCP tool.

| CLI usage | MCP tool |
|---|---|
| `finance-calendar <event_type> ...` | `mcp__longbridge__finance_calendar` (event type passed as a parameter) |

If the name above does not resolve, run `longbridge --help` or check MCP tool list.

## Related skills

| Skill | Why |
|---|---|
| `longbridge-catalyst-radar` | Watchlist-scoped morning/evening briefings layered on this calendar. |
| `longbridge-earnings` | Single-symbol earnings deep-dive once the date arrives. |
| `longbridge-fundamental` | Historical earnings KPIs (the *past* counterpart). |
| `longbridge-news` | Filings and headline reaction around the event. |

## File layout

```
longbridge-calendar/
├── SKILL.md
└── references/
    ├── portfolio-briefing.md   # 默认工作流：持仓驱动三段式报告
    ├── output-template.md      # 三个输出模板的字段规范
    └── data-fetching.md        # 数据来源优先级、降级规则与 CLI 调用说明
```
