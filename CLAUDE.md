# CLAUDE.md — repo conventions for Claude Code

This file briefs Claude Code when working **inside this repo** (adding new skills, editing existing ones, fixing docs). It's not for end-users — they install via the methods in [docs/install.md](./docs/install.md).

## What this repo is

19 [Agent Skills](https://agentskills.io/specification) that wrap the [Longbridge Securities](https://longbridge.com) platform — quotes, charts, fundamentals, valuation, news, watchlist, account analytics, etc. Multilingual triggers (Simplified Chinese / Traditional Chinese / English). The default style is **prompt-only** (SKILL.md tells the LLM what `longbridge ...` command to run); `scripts/` and `commands/` subfolders are allowed but should be opt-in for clear runtime needs (DOCX generation, chart helpers, slash commands), not as a wrapper-by-default.

## Layout

```
longbridge-skills/
├── .claude-plugin/marketplace.json    # plugin marketplace entry
├── skills/                            # 19 skill folders
│   ├── <slug>/
│   │   ├── SKILL.md                   # required
│   │   ├── references/                # optional — on-demand detail loaded by the LLM
│   │   ├── scripts/                   # optional — Python helpers (e.g. DOCX, charts) when there's a clear runtime need
│   │   └── commands/                  # optional — Claude Code slash commands (`/<command>`)
│   └── ...
├── docs/
│   ├── architecture.md                # multilingual + CLI/MCP routing design
│   └── install.md                     # install / verify / FAQ
├── CLAUDE.md                          # this file
├── README.md
├── LICENSE                            # MIT
└── .gitignore
```

## Conventions for adding or editing a skill

### 1. Slug + directory

- Directory name must match `^[a-z0-9]+(-[a-z0-9]+)*$` (lowercase ASCII + hyphens).
- It MUST equal the `name:` value in the SKILL.md frontmatter.
- Existing skills are namespaced `longbridge-*` (e.g. `longbridge-quote`). The single base skill is just `longbridge`.

### 2. Frontmatter

Required: `name`, `description`. Recommended: `license: MIT`, `metadata`.

```yaml
---
name: longbridge-foo
description: |
  One-paragraph what + when. Triggers: "<zh-Hans keyword>", "<zh-Hant keyword>", "<English keyword>", ...
license: MIT
metadata:
  author: longbridge
  version: "1.0.0"
  risk_level: read_only       # or account_read | mutating
  requires_login: false       # or true
  default_install: true       # or false (mutating skills sometimes opt out)
  requires_mcp: false         # true for analysis-tier skills
  tier: read                  # or analysis (informational)
---
```

`description` must be **≤ 1024 characters total**. The `Triggers:` list inside it is the **only** thing Claude Code uses to decide whether to activate the skill — pack it with multilingual keywords (see §3).

### 3. Trilingual triggers

`description` MUST cover all three languages explicitly:

- **Simplified Chinese**: 现在多少钱 / 涨跌幅 / 持仓 / ...
- **Traditional Chinese**: 現在多少 / 漲跌幅 / 持倉 / ...
- **English**: stock price / current quote / my holdings / ...
- **Ticker examples**: NVDA.US, 700.HK, 600519.SH

Glyphs identical in Simplified and Traditional only need to appear once. Divergent glyphs (`股价`/`股價`, `经纪`/`經紀`) must appear in both forms.

### 4. Body — "Response language" directive (mandatory)

Every SKILL.md must include this line right after the H1 + intro paragraph:

```markdown
> **Response language**: match the user's input language —
> Simplified Chinese / Traditional Chinese / English.
```

This instructs the LLM to detect the user's input language and reply in the same language. Field tables and error reply tables must be 3-column (Simplified / Traditional / English).

### 5. CLI calls — prefer prompt-only, but `scripts/` is allowed when justified

**Default**: SKILL.md instructs the LLM to call the Longbridge CLI directly:

```bash
longbridge <subcommand> --format json
```

When SKILL.md isn't sure about the exact flag spelling, defaults, or argument order, it must instruct the LLM to run:

```bash
longbridge <subcommand> --help
```

— the CLI's built-in help is the canonical source. **Do not hard-code flag names in SKILL.md** without telling the LLM to verify them against `--help` first; that creates version-coupling.

**When `scripts/` is justified**: a Python (or other) helper is acceptable when the skill needs something the LLM can't (or shouldn't try to) do inline — for example:

- DOCX / XLSX / PDF generation (`python-docx`, `openpyxl`, etc.)
- Chart generation with bilingual fonts (`matplotlib` + CJK font fallback)
- A safety-gate runtime check (e.g. dry-run + binary lock for mutating writes)

In that case, keep the helper **narrow** (does one thing, accepts CLI args, no business templates baked in), document the inputs/outputs in SKILL.md, and still keep SKILL.md the primary instruction surface.

**Anti-pattern**: `scripts/cli.py` that wraps the longbridge CLI itself by hard-coding flag names like `-s NVDA.US --include-static`. The longbridge CLI evolves; wrappers like that desync. The original repo had these and we removed them in favour of LLM + `--help` discovery.

### 5b. `commands/` — optional Claude Code slash commands

A `<skill>/commands/<name>.md` file declares a `/<name>` slash command that triggers this skill with optional arguments (`argument-hint`). Add only when a slash command is genuinely useful (e.g. *"give me an earnings update on TSLA.US"* → `/earnings TSLA.US`); otherwise rely on description triggers.

### 6. Path selection: CLI vs MCP

Default rule: `longbridge <subcmd> --format json` first; fall back to `mcp__longbridge__*` when:

- Shell `command not found: longbridge` (binary not installed)
- A specific subcommand has known issues (e.g. `security-list` `param_error`)

Mark exceptions in the SKILL.md explicitly:

- **Analysis tier** (valuation / fundamental / news / peer-comparison / portfolio / catalyst-radar): MCP-only, no CLI equivalent. Frontmatter `requires_mcp: true`. `## Prerequisite` section tells the user to run `claude mcp add --transport http longbridge https://openapi.longbridge.com/mcp`.
- **Mutating** (`longbridge-watchlist-admin`): two-turn protocol — preview the action in plain language, wait for explicit confirmation (`确认`/`yes`/`是的`/`confirm`), then execute. Never combine into one turn.

### 7. Error handling

`SKILL.md` `## Error handling` table maps a class of failure (recognised by shell behaviour or stderr keyword) to a multilingual reply phrase:

| Situation | LLM response |
|---|---|
| Shell `command not found: longbridge` | Fall back to MCP if configured; otherwise tell the user to install longbridge-terminal. |
| stderr contains `not logged in` / `unauthorized` | Tell the user to run `longbridge auth login` (with `Trade` permission for account skills). |
| Other stderr | Surface verbatim — never silently retry. |

### 8. references/ for overflow

Keep SKILL.md under ~200 lines. Push detail (long field dictionaries, multi-page reference material, briefing templates) into `references/<topic>.md` and link from the main file. The LLM only loads `references/` files on demand.

## Quick checklist for adding a new skill

1. Create `skills/<slug>/` with `SKILL.md`.
2. Frontmatter: `name`, multilingual `description` (≤1024 chars), `license: MIT`, `metadata`.
3. Body: H1, intro, **Response language** directive.
4. Sections: `## When to use`, `## Workflow`, `## CLI` (with `longbridge ... --format json` examples and a "run `--help` if unsure" note), `## Output`, `## Error handling`, `## MCP fallback`, `## Related skills`, `## File layout`.
5. If the body grows past ~200 lines, move detail into `references/<topic>.md`.
6. If the skill genuinely needs a runtime helper (DOCX / chart / safety gate), add `scripts/<helper>.py` and document inputs/outputs in SKILL.md. Otherwise stay prompt-only.
7. If a slash command makes sense (`/<name> <arg>` → run this skill), add `commands/<name>.md` with `description:` and `argument-hint:`.
8. Update [README.md](./README.md) "What's inside" table to include the new skill.
9. Plugin marketplace auto-discovers it (`.claude-plugin/marketplace.json` declares `skills: ["./skills/"]`); no marketplace edit needed.
10. Sanity-check by hand:
    - Slug matches dir name? `ls skills/<slug>/` and `grep '^name:' skills/<slug>/SKILL.md`
    - All three languages in triggers?
    - Response language directive present?

## Anti-patterns to avoid

- **`scripts/cli.py` wrapping the longbridge CLI itself with hard-coded flags** (`-s NVDA.US --include-static`). The CLI evolves; wrappers desync. Either call `longbridge ... --format json` directly from the prompt, or — if you really need a helper — keep it narrow and pass arguments through (don't bake business templates into Python).
- **Bilingual tables**: never write "Chinese / English" — must be 3-column (Simplified / Traditional / English).
- **Skipping the Response language directive**: every SKILL.md needs it, otherwise output language is unstable.
- **Combining preview + execute** for mutating skills: must be two distinct turns, separated by an explicit user confirmation.

## Reference docs

- [docs/architecture.md](./docs/architecture.md) — design rationale: how multilingual + CLI/MCP routing actually work in prompt-only fashion.
- [docs/install.md](./docs/install.md) — install paths (npx / bun / Claude Code marketplace / clone+symlink), verification, FAQ.

## License

MIT. See [LICENSE](./LICENSE).
