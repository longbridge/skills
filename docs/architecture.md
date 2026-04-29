# Skill design: multilingual + tool selection

The two cross-cutting design decisions in this repo — **trilingual support** and **CLI vs MCP path selection** — are not runtime branches in code. They are written as instructions inside `SKILL.md`, **leaving the decision to the LLM at call time**. This document explains how both mechanisms work so future maintainers can stay consistent when adding or rewriting skills.

> Cross-references: [Agent Skills specification](https://agentskills.io/specification) · [microsoft/skills convention](https://github.com/microsoft/skills) · this repo's [README.md](../README.md)

---

## 1. Multilingual (Simplified Chinese / Traditional Chinese / English)

### Goals

Mainland-, Hong Kong-, and Taiwan-based users all use these skills. We need to support:

- A user prompt in any of the three languages — *"NVDA 现在多少钱"* / *"NVDA 現在多少錢"* / *"What's NVDA's price?"* — should route correctly to `longbridge-quote`.
- The reply should match **the user's input language**, not be hard-coded.
- Field names and error phrasing should follow the same language.

**Non-goals:** no i18n framework, no code-side language detection, no per-language SKILL.md files. **All in prompt — zero code cost.**

### Implementation: four layers

#### 1️⃣ Description triggers — decide **whether the skill activates**

Every `SKILL.md` writes the same semantic concept into multiple language flavours inside the `description`. Example: [longbridge-quote/SKILL.md](../skills/longbridge-quote/SKILL.md):

```yaml
description: |
  Real-time quotes, static reference, and valuation indices for stocks listed in HK / US / A-share / Singapore via Longbridge Securities. ... Triggers: "现在多少钱", "股价", "涨跌幅", "成交量", "市值", "市盈率", "PE", "PB", "换手率", "行业", "現在多少", "股價", "成交量", "市值", "市盈率", "stock price", "current price", "quote", "market cap", "PE ratio", "valuation", "NVDA price", "AAPL quote", "茅台市值", "腾讯股价", "700.HK", "600519.SH".
```

At startup, the agent only loads frontmatter (~100 tokens / skill — this is step 1 of [progressive disclosure](https://agentskills.io/specification#progressive-disclosure)). The LLM pattern-matches the user's prompt against these triggers — Simplified, Traditional, English, or ticker examples can each independently fire the skill.

> **Tip:** keywords identical across Simplified and Traditional (e.g. *"成交量"*, *"市值"*) only need to be written once. **Divergent characters** must be written twice (e.g. *"现在多少钱"* / *"現在多少錢"*, *"股价"* / *"股價"*).

#### 2️⃣ Response-language directive — decide **the output language**

Every `SKILL.md`, immediately below the `# <skill-name>` heading and the intro paragraph, includes this fixed line:

```markdown
> **Response language**: match the user's input language —
> Simplified Chinese / Traditional Chinese / English.
```

This instructs the LLM to **detect the user's input language** (Simplified, Traditional, or English) and **respond in the same language**. Modern LLMs already have this ability natively; we just have to surface the instruction inside the SKILL.

The data layer is language-agnostic — both the raw `longbridge` CLI (used by 17 skills) and the two Python wrappers (`longbridge-quote`, `longbridge-watchlist-admin`) emit English JSON only. Language switching happens when the LLM translates that JSON to natural language.

#### 3️⃣ Field translation tables — multilingual ingredients for data → prose

Underlying financial data uses English field names. Each `SKILL.md` (or, for longer ones, an offloaded `references/` file) provides a three-column lookup table; the LLM picks the column for the user's language. Example: [longbridge-fundamental/references/field-dictionary.md](../skills/longbridge-fundamental/references/field-dictionary.md):

```markdown
| MCP field            | 简体           | 繁體           | English         |
|---|---|---|---|
| `revenue` / `total_revenue` | 营业收入 / 营收 | 營業收入 / 營收 | Revenue        |
| `cost_of_revenue`    | 营业成本       | 營業成本       | Cost of revenue |
| `gross_margin`       | 毛利率         | 毛利率         | Gross margin   |
| `roe`                | 净资产收益率   | 淨資產收益率   | Return on equity |
```

When rendering the answer, the LLM consults the column matching the language detected in §2.

#### 4️⃣ Error-reply tables — three languages side by side

Each read-tier skill's `## Error handling` section is also three columns. Example: [longbridge-quote/SKILL.md](../skills/longbridge-quote/SKILL.md):

```markdown
| `error_kind` | What happened | Reply phrase (zh-Hans / zh-Hant / en) |
|---|---|---|
| `binary_not_found` | longbridge CLI not installed | "长桥 CLI 未安装,请先安装 longbridge-terminal" / "長橋 CLI 未安裝,請先安裝 longbridge-terminal" / "Longbridge CLI not installed: https://github.com/longportapp/longbridge-terminal" |
| `auth_expired` | OAuth token expired | "长桥登录态过期,请跑 `longbridge login`" / "登入過期,請執行 `longbridge login`" / "Login expired — run `longbridge login`." |
```

The 17 prompt-only skills surface raw `longbridge` stderr to the user. The two Python-wrapped skills (`longbridge-quote`, `longbridge-watchlist-admin`) collapse failures into stable `error_kind` enum values (`binary_not_found / auth_expired / subprocess_failed / no_input / invalid_input_format / empty_result / risk_block`); the LLM then looks up the matching language column. Either way, the user gets phrasing in their own language.

### End-to-end flow

```
                  User: "NVDA 現在股價"
                            ↓
             [Claude Code / agent boots up]
   1. Loads every SKILL.md frontmatter (~100 tokens / skill)
                            ↓
        LLM pattern-matches against description triggers.
        "現在股價" hits the zh-Hant trigger of longbridge-quote.
                            ↓
                [Activate longbridge-quote SKILL.md]
   2. Loads the full SKILL.md (English body + multilingual lookup tables)
   3. Response-language directive tells the LLM:
        user typed zh-Hant → reply in zh-Hant
                            ↓
              python3 scripts/cli.py -s NVDA.US     # quote-only wrapper
                            ↓
       cli.py returns JSON (English fields + canonical error_kind)
                            ↓
   4. LLM uses zh-Hant + the multilingual tables in §3/§4 to compose:
   "NVDA 現在 209.27 美元,當日下跌 -2.86%。數據來源:長橋證券。"
```

**The entire pipeline runs in the prompt layer.** Neither the raw `longbridge` CLI nor the two Python wrappers contain any i18n code. Adding a new language (Japanese, Korean, Spanish, …) means adding triggers to the description plus another column to the tables — **no code changes required**.

---

## 2. CLI vs MCP tool selection

### Goals

Each capability (quote, positions, capital flow, …) is reachable through two paths:

| Path | Interface | Latency | Dependency |
|---|---|:---:|---|
| **Local CLI** | subprocess into the `longbridge` binary | Fast (in-process, ~50 ms) | User has installed longbridge-terminal and run `longbridge login` |
| **Official MCP** | HTTP + OAuth (Anthropic MCP transport) | Slow (network + auth, ~500 ms+) | User has run `claude mcp add longbridge ...` |

Every `SKILL.md` tells the LLM the same rule: **default to CLI; fall back to MCP under specific conditions.**

### Default rule

```
1. LLM calls `longbridge <subcommand> --format json` directly.
2. Shell returns `command not found` → fall back to MCP.
3. Otherwise parse the JSON output (or surface stderr verbatim if non-zero exit).
4. MCP also unconfigured → tell the user: install longbridge-terminal or run `claude mcp add ...`.
```

Each read-tier `SKILL.md` ends with an `## MCP fallback` section that lists the **subcommand ↔ MCP tool** mapping. Example: [longbridge-quote/SKILL.md](../skills/longbridge-quote/SKILL.md):

```markdown
| CLI subcommand | MCP tool |
|---|---|
| `quote` | `mcp__longbridge__quote` |
| `static` | `mcp__longbridge__static_info` |
| `calc-index` | `mcp__longbridge__calc_indexes` |
```

> **Two skills retain a Python wrapper** (`scripts/cli.py`):
> - **`longbridge-quote`** — merges `quote` + `static` + `calc-index` outputs into one envelope so the LLM doesn't lose fields when stitching three subprocess calls.
> - **`longbridge-watchlist-admin`** — enforces a dry-run + `--confirm` gate plus a binary-lock guard. The wrapper turns the safety contract from a prompt convention into a runtime check.
>
> The other 17 skills are pure prompt orchestration: SKILL.md tells the LLM what `longbridge ...` command to run; the LLM calls it directly and reads the raw JSON.

### Four exceptions (each `SKILL.md` overrides the default explicitly)

| Exception | Default flips to | Why | Where it's written |
|---|---|---|---|
| **`longbridge-security-list securities`** | **MCP-preferred** | The current `longbridge` CLI hits an intermittent `param_error` on the security-list endpoint; MCP calls the SDK directly and avoids the CLI middle layer | [security-list/SKILL.md `## Path-selection note`](../skills/longbridge-security-list/SKILL.md) |
| **`longbridge-subscriptions`** | **CLI-only** | MCP is stateless HTTP — there is **no WebSocket session concept**, hence no equivalent tool | [subscriptions/SKILL.md `## Local-only`](../skills/longbridge-subscriptions/SKILL.md) |
| **Six analysis-tier skills** (valuation / fundamental / news / peer-comparison / portfolio / catalyst-radar) | **MCP-only** | `requires_mcp: true` in frontmatter; they invoke MCP-only tools (`valuation_history` / `profit_analysis` / `news` / `topic`, …) that the CLI does not expose | each analysis-tier SKILL.md `## Prerequisite` |
| **`longbridge-watchlist-admin` dry-run** | **CLI required** | Dry-run is the SKILL-layer confirmation gate — MCP write tools have no dry-run concept. Hybrid: dry-run goes through `cli.py` (no `--confirm`); after the user confirms, the actual write may go via `cli.py --confirm` or an MCP write tool | [watchlist-admin/SKILL.md `## Two-step protocol`](../skills/longbridge-watchlist-admin/SKILL.md) |

### Decision flow

```
                User prompt arrives
                       ↓
  ┌─ Analysis-tier skill? (valuation / fundamental / news / peer / portfolio / catalyst-radar)
  │    └─ yes ──→ MCP-only (no cli.py / no direct CLI)
  │            └─ MCP unconfigured? → ask user to run `claude mcp add longbridge ...`
  │    └─ no ──→ continue
  ↓
  ┌─ Mutating skill? (watchlist-admin — keeps cli.py for the safety gate)
  │    └─ yes ──→ ① dry-run via `python3 scripts/cli.py ...` (no --confirm)
  │              ② LLM reads the plan back, waits for explicit confirmation
  │                 (matches "确认" / "yes" / "是的" / "confirm")
  │              ③ once confirmed → `cli.py --confirm` OR MCP write tool
  │    └─ no ──→ continue
  ↓
  ┌─ Skill declares MCP-preferred? (security-list securities)
  │    └─ yes ──→ go to MCP directly
  │    └─ no ──→ continue
  ↓
  ┌─ Skill ships a Python wrapper? (longbridge-quote)
  │    └─ yes ──→ run `python3 scripts/cli.py ...` for the merged envelope
  │    └─ no ──→ run `longbridge <subcommand> ... --format json` directly
  ↓
  Result handling
       ├─ exit 0, JSON returned ──→ use the result
       ├─ shell `command not found` ──→ fall back to MCP if configured; otherwise prompt user to install CLI
       ├─ stderr contains "unauthorized" / "not in authorized scope" ──→ tell user to re-run `longbridge login` (MCP shares the same OAuth)
       └─ other stderr ──→ surface verbatim; never silently retry
```

### Capability matrix: CLI vs MCP

| Capability | CLI (`longbridge` binary) | MCP (`mcp__longbridge__*`) |
|---|---|---|
| Quote / candlestick / depth / capital flow / options / warrants | ✅ | ✅ |
| Positions / orders / balance | ✅ | ✅ |
| Watchlist (read) | ✅ | ✅ |
| Watchlist (write) | ✅ (with dry-run + confirm gate) | ✅ (raw write; SKILL-layer must add the gate) |
| **Historical market-temperature time series** | ❌ | ✅ `history_market_temperature` |
| **Finance calendar** (earnings / dividends / IPOs / macro) | ❌ | ✅ `finance_calendar` |
| **Short positions** | ❌ | ✅ `short_positions` |
| **Options volume analysis** | ❌ | ✅ `option_volume / option_volume_daily` |
| **Valuation history + industry distribution** | ❌ | ✅ `valuation_history` / `industry_valuation_dist` |
| **Full IS/BS/CF + analyst consensus** | ❌ | ✅ `financial_report` / `forecast_eps` / `consensus` |
| **Portfolio P&L analysis** | ❌ | ✅ `profit_analysis` / `profit_analysis_detail` |
| **News + filings + community topics** | ❌ | ✅ `news / filings / topic / topic_detail / topic_replies` |
| **Shared watch lists** | ❌ | ✅ `sharelist_*` (8 tools) |
| **WebSocket subscription diagnostics** | ✅ | ❌ (MCP is stateless) |
| **Statement / report exports** | ❌ | ✅ `statement_*` |

> **Observation**: the five analysis-tier skills are MCP-only **because the underlying tools they need (valuation history, full financial reports, news, portfolio P&L) simply have no CLI equivalent**. It is a capability-difference outcome, not a stylistic choice.

### Why default to CLI rather than MCP?

| Dimension | CLI | MCP |
|---|---|---|
| **Latency** | Local subprocess, ~50 ms | HTTP + OAuth, ~500 ms+ |
| **Network** | Not required (token cached after `longbridge login`) | Requires public reachability to `openapi.longbridge.com` |
| **Session state** | CLI maintains the WebSocket connection — push / subscribe usable | Stateless HTTP |
| **OAuth scope** | Decided at `longbridge login` on the user's machine | Decided when the user authorises in the browser after `claude mcp add` (re-authorisable for trade scope) |
| **Cross-skill consistency** | Same `--format json` flag across all subcommands; behaviour is documented per skill | MCP responses are whatever the MCP server returns; varies per tool |

In short: **when the local CLI is installed, it is faster than MCP.** MCP exists to (a) widen capability (analysis / history / async topics) and (b) act as a fallback when CLI is unavailable.

### Shell exit / stderr is the glue between CLI and MCP

For the 17 skills with no Python wrapper, the LLM reads:

| Signal | LLM response |
|---|---|
| Shell `command not found` (CLI binary missing) | **Path-switch signal** — try MCP |
| stderr contains `unauthorized` / `not in authorized scope` | Tell user to run `longbridge logout && longbridge login` (MCP shares the same OAuth — switching path won't fix scope) |
| stderr contains `param_error` (rare; see `security-list`) | If a known CLI bug, switch to MCP; otherwise surface to user |
| Other stderr / non-zero exit | Surface verbatim — never silently retry |
| Exit 0, empty JSON `[]` | Empty result is success in some skills, ambiguous in others — see each SKILL.md |

**A missing binary is the only signal that triggers a path switch.** Other errors must not push the LLM to MCP — the underlying error is unrelated to the path.

---

## 3. Maintainer guidelines

When adding or rewriting a skill, follow these:

1. **Trilingual triggers are required** — the description must cover Simplified Chinese, Traditional Chinese, and English keywords. Identical-glyph words appear once; divergent ones appear in both forms.
2. **Use the canonical Response-language directive verbatim** — copy the line from `quote` / `kline` / any shipped SKILL.md. Do not rephrase; consistency matters across skills.
3. **Field tables and error tables are three columns** — never "Chinese / English"; always 3 columns (Simplified / Traditional / English).
4. **Path rules are declared in SKILL.md according to category**:
   - Default read-tier → `## CLI` + `## MCP fallback`
   - MCP-preferred → add `## Path-selection note` explaining why
   - CLI-only → add `## Local-only` explaining why MCP has no equivalent
   - MCP-only (analysis tier) → frontmatter `requires_mcp: true` + `## Prerequisite` mentioning `claude mcp add longbridge ...`
   - Mutating → add `## Two-step protocol (mandatory)` describing the dry-run + confirm flow
5. **`cli.py` envelope fields are mandatory** — `success / source: "longbridge" / skill / skill_version / datas` on success; `success: false / error_kind / error / details` on failure. `error_kind` must be one of the seven enum values.
6. **`error_kind=binary_not_found` is the path-switch signal** — `cli.py` must return it when `shutil.which()` returns `None`, so the LLM can correctly fall back to MCP.

---

**One last note**: both mechanisms (multilingual + CLI/MCP) share the same essence — **express policy through prompt; push the decision to the LLM rather than coding it at runtime**. 17 of 19 skills are pure SKILL.md (no Python), and the remaining two keep a thin wrapper only where a runtime guarantee is needed (`longbridge-quote`'s multi-call envelope; `longbridge-watchlist-admin`'s dry-run + binary-lock gate). Adding a new policy almost always means editing one SKILL.md, not touching code.
