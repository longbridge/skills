# Install guide

## Prerequisites

Different tiers of skills have different runtime dependencies — install only what you need.

### Required (read-tier — 12 skills)

1. **Longbridge CLI** (Rust binary, runs in-process):

   ```bash
   # macOS / Linux — see https://github.com/longportapp/longbridge-terminal
   brew install longportapp/tap/longbridge          # macOS Homebrew
   # Or download a release binary onto your PATH
   ```

   Verify with `longbridge --version` — it should print a version string.

2. **Log in to your Longbridge account** (the OAuth token is cached at `~/.longbridge/terminal/.openapi-session`):

   ```bash
   longbridge login
   ```

   A browser opens for authorisation. **Tick the "Trade" permission** if you want the account-tier skills (`positions / orders / watchlist / watchlist-admin`). Quote-only access is sufficient for market-data skills.

3. **Python 3.8+** (`scripts/cli.py` is stdlib-only, no third-party dependencies):

   ```bash
   python3 --version  # ≥ 3.8
   ```

### Optional (required for the analysis tier — 5 skills)

4. **Longbridge MCP server** (the analysis-tier skills `valuation / fundamental / news / peer-comparison / portfolio` depend entirely on this):

   ```bash
   claude mcp add --transport http longbridge https://openapi.longbridge.com/mcp
   ```

   The first MCP tool call triggers an OAuth flow in your browser. `portfolio` requires the **Trade** permission; the other four analysis skills only need the **Quote** permission.

   Verify with `claude mcp list` — `longbridge` should appear in the output.

---

## Four install paths

### Path A — `npx` / `bun` (recommended; simplest)

**Install all 19 skills**:

```bash
npx skills add longbridge/skills            # via npx
bunx skills add longbridge/skills           # via bun (equivalent)
```

**Install just a few**:

```bash
npx skills add longbridge/skills --skill longbridge-quote
npx skills add longbridge/skills --skill longbridge-portfolio --skill longbridge-news
```

The skills land in `~/.claude/skills/` by default. Restart your Claude Code session and they're ready to use.

> `npx skills` / `bunx skills` is a community installer that works for any Agent-Skills-compatible GitHub repo. See [agentskills.io](https://agentskills.io) for the spec.

---

### Path B — Claude Code plugin marketplace (carries marketplace metadata)

**B1. Remote repo:**

```text
/plugin marketplace add longbridge/skills
/plugin install longbridge@longbridge-skills
```

**B2. Local path (during development / testing):**

```text
/plugin marketplace add <path-to-the-cloned-repo>
/plugin install longbridge@longbridge-skills
```

> `longbridge` is the plugin name (matches `plugins[0].name` in `.claude-plugin/marketplace.json`); `longbridge-skills` is the marketplace name (matches the top-level `name` field).

**B3. Verify:**

```text
/plugin list
```

You should see `longbridge@longbridge-skills` enabled. Open a new Claude Code session and ask *"NVDA 现在多少钱"* to check that the skill triggers.

---

### Path C — Symlink individual skills to `~/.claude/skills/` (cherry-pick; clone first)

Useful when you want only a few skills out of the 19. Clone the repo first, then create symlinks from your local checkout into `~/.claude/skills/`.

```bash
# Clone the repo locally (anywhere is fine)
git clone https://github.com/longbridge/skills.git
cd skills
mkdir -p ~/.claude/skills

# Single skill
ln -s "$PWD/skills/longbridge-quote" ~/.claude/skills/longbridge-quote

# Or another individual skill
ln -s "$PWD/skills/longbridge-kline"  ~/.claude/skills/longbridge-kline
```

**Batch-symlink all 19**:

```bash
for d in "$PWD"/skills/*; do
  ln -sfn "$d" "$HOME/.claude/skills/$(basename "$d")"
done
ls -la ~/.claude/skills/ | grep longbridge
```

> **Why symlink and not `cp`?** The repo itself is the live source — edits to a SKILL.md take effect immediately, with no redeploy. For production distribution, swap `ln -s` for `cp -R`.

#### ⚠️ Special case: the mutating skill

**`longbridge-watchlist-admin`** modifies the user's watchlist state. The batch script above will install it; the SKILL.md enforces a dry-run + confirm protocol, so it's safe by default. If you'd rather audit it before enabling, install the other 18 first and skip this one:

```bash
for d in "$PWD"/skills/*; do
  slug=$(basename "$d")
  [[ "$slug" == "longbridge-watchlist-admin" ]] && continue
  ln -sfn "$d" "$HOME/.claude/skills/$slug"
done
```

Run a separate `ln -s` for `longbridge-watchlist-admin` once you're ready.

---

### Path D — Other agent products

Skills are pure Markdown + Python and portable to any Agent-Skills-compatible product. Only the install directory differs:

| Agent product | Default skill directory |
|---|---|
| Claude Code | `~/.claude/skills/` |
| Gemini CLI | `~/.gemini/skills/` |
| OpenCode | `~/.opencode/skills/` |
| OpenAI Codex | see vendor docs |

Example (Gemini CLI), assuming the repo is cloned locally:

```bash
mkdir -p ~/.gemini/skills
for d in "$PWD"/skills/*; do
  ln -sfn "$d" "$HOME/.gemini/skills/$(basename "$d")"
done
```

> Different products implement different parts of the spec — `compatibility` and `allowed-tools` are experimental. Every field used in this repo is part of the canonical Agent Skills spec, so cross-product portability should be safe.

---

## Verify

### 1. Repo self-test

From the repo root:

```bash
python3 scripts/validate-skills.py
```

Expected output:

```
Inspected 19 skill(s).
All clean ✓
```

The validator checks:
- Every SKILL.md frontmatter conforms to spec (`name` is a valid slug, `description` ≤ 1024 chars).
- `name` matches the parent directory name.
- All read-tier `scripts/test_cli.py` files pass (~1 s per skill).

### 2. Real-account smoke test (only if you've installed the longbridge CLI and run `longbridge login`)

From the repo root:

```bash
# Quote
python3 skills/longbridge-quote/scripts/cli.py -s NVDA.US

# 5 daily candles
python3 skills/longbridge-kline/scripts/cli.py kline NVDA.US --period day --count 5

# Watchlist
python3 skills/longbridge-watchlist/scripts/cli.py
```

Each call should return a JSON envelope with `"success": true`.

### 3. End-to-end through Claude Code

Open a new session and try one prompt per skill family:

| Prompt | Expected skill |
|---|---|
| *"NVDA 现在多少钱"* | `longbridge-quote` |
| *"特斯拉过去一年走势"* | `longbridge-kline` |
| *"700.HK 盘口"* | `longbridge-depth` |
| *"我的自选股"* | `longbridge-watchlist` |
| *"NVDA 估值贵不贵"* | `longbridge-valuation` (analysis tier — needs MCP) |

Each reply should include "Source: Longbridge Securities" / "数据来源:长桥证券".

---

## Uninstall

### Path A (npx / bun) installs

```bash
npx skills remove longbridge/skills                              # remove all
npx skills remove longbridge/skills --skill longbridge-quote     # remove one
```

### Path B (plugin marketplace) installs

```text
/plugin uninstall longbridge@longbridge-skills
/plugin marketplace remove longbridge-skills          # optional — drop the marketplace registration
```

### Path C (symlink) installs

```bash
rm ~/.claude/skills/longbridge ~/.claude/skills/longbridge-*
ls ~/.claude/skills/                                  # verify
```

### Revoke Longbridge CLI authorisation

```bash
longbridge logout                                     # clears the local token
```

### Revoke Longbridge MCP authorisation

```bash
claude mcp logout longbridge                          # revoke the OAuth scope
claude mcp remove longbridge                          # remove the MCP registration
```

---

## FAQ

### A skill never triggers after install

1. Check that the trigger keywords cover what the user typed — see [`docs/architecture.md` §1.1](./architecture.md).
2. Check that the directory name is a valid lowercase ASCII slug — run `python3 scripts/validate-skills.py`.
3. Claude Code scans `~/.claude/skills/` once per session start. Restart the session if you installed while a session was open.

### `auth_expired`

- Read-tier market-data skills (quote / kline / depth / …) only need the **Quote** permission at `longbridge login`.
- Account-tier skills (positions / orders / watchlist) **require the Trade permission**:
  ```bash
  longbridge logout && longbridge login   # re-authorise; tick "Trade" in the browser
  ```
- MCP behaves the same — `claude mcp logout longbridge` and re-authorise on the next MCP tool call.

### `binary_not_found`

`cli.py` cannot locate the `longbridge` binary. Two fixes:

- **Recommended:** install [longbridge-terminal](https://github.com/longportapp/longbridge-terminal).
- **Alternative:** install MCP (`claude mcp add ...`) so the LLM falls back automatically.

### `param_error` on `security-list securities`

A known issue in the underlying Longbridge CLI. The SKILL.md tells the LLM to switch to `mcp__longbridge__security_list` automatically — **no manual intervention required**.

### Analysis-tier skill says "this skill has no CLI fallback"

Expected. The five analysis-tier skills (valuation / fundamental / news / peer-comparison / portfolio) are prompt-only and **MCP-only**. Run `claude mcp add longbridge ...` and authorise — `portfolio` needs Trade scope, the other four only need Quote scope.

For the design rationale, see [docs/architecture.md §2 — CLI vs MCP tool selection](./architecture.md).
