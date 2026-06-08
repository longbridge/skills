#!/usr/bin/env bash
#
# reinstall.sh — fully (re)install the Longbridge skills from this repo into every
# agent skills directory, wiping any previously-installed `longbridge` / `longbridge-*`
# entries first.
#
# WHY THIS EXISTS
#   `npx skills update` only refreshes skills whose slug still exists upstream. It does
#   NOT delete skills that were renamed/removed, and does NOT add skills with brand-new
#   names. After a release that consolidates or renames skills, `update` leaves a mix of
#   stale orphans + missing new skills. This script does a clean wipe-and-install so the
#   target dirs exactly mirror this repo's skills/ folder.
#
# USAGE
#   scripts/reinstall.sh [--link] [--dry-run] [--target DIR ]...
#
#   --link        Symlink each skill back to this repo (live edits; for development).
#                 Default is copy (a self-contained install; for normal use).
#   --dry-run     Print what would change, touch nothing.
#   --target DIR  Install into DIR (the skills dir itself, e.g. ~/.claude/skills).
#                 Repeatable. Overrides the auto-detected defaults below.
#   -h, --help    Show this help.
#
# DEFAULT TARGETS (only those whose parent dir already exists are used)
#   ~/.claude/skills     Claude Code
#   ~/.agents/skills     vercel-labs/skills canonical store
#   ~/.gemini/skills     Gemini CLI
#   ~/.opencode/skills   OpenCode
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_SRC="$(cd "$SCRIPT_DIR/../skills" && pwd)"

MODE="copy"
DRY_RUN=0
declare -a TARGETS=()

usage() { sed -n '2,40p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; exit "${1:-0}"; }

while [ $# -gt 0 ]; do
  case "$1" in
    --link)    MODE="link"; shift ;;
    --dry-run) DRY_RUN=1; shift ;;
    --target)  [ $# -ge 2 ] || { echo "error: --target needs a directory" >&2; exit 2; }
               TARGETS+=("$2"); shift 2 ;;
    -h|--help) usage 0 ;;
    *)         echo "error: unknown argument: $1" >&2; usage 2 ;;
  esac
done

# --- sanity: the source must be a real skills dir ---
if [ ! -d "$SKILLS_SRC" ] || ! ls "$SKILLS_SRC"/*/SKILL.md >/dev/null 2>&1; then
  echo "error: no skills found under $SKILLS_SRC" >&2
  exit 1
fi

# --- collect the slugs we are going to install (dirs that contain a SKILL.md) ---
declare -a SLUGS=()
for d in "$SKILLS_SRC"/*/; do
  [ -f "$d/SKILL.md" ] || continue
  SLUGS+=("$(basename "$d")")
done

# --- resolve targets: explicit --target wins; otherwise auto-detect existing agents ---
if [ ${#TARGETS[@]} -eq 0 ]; then
  for cand in \
    "$HOME/.claude/skills" \
    "$HOME/.agents/skills" \
    "$HOME/.gemini/skills" \
    "$HOME/.opencode/skills"; do
    # only install where the agent's home (parent of skills/) already exists
    [ -d "$(dirname "$cand")" ] && TARGETS+=("$cand")
  done
fi

if [ ${#TARGETS[@]} -eq 0 ]; then
  echo "No agent directories detected (~/.claude, ~/.agents, ~/.gemini, ~/.opencode)." >&2
  echo "Pass one explicitly, e.g.:  scripts/reinstall.sh --target ~/.claude/skills" >&2
  exit 1
fi

run() { if [ "$DRY_RUN" -eq 1 ]; then echo "  [dry-run] $*"; else "$@"; fi; }

echo "Source : $SKILLS_SRC (${#SLUGS[@]} skills)"
echo "Mode   : $MODE$([ "$DRY_RUN" -eq 1 ] && echo '  (dry-run)')"
echo

for target in "${TARGETS[@]}"; do
  echo "→ $target"
  run mkdir -p "$target"

  # 1) wipe every existing longbridge entry, including broken symlinks
  removed=0
  for entry in "$target/longbridge" "$target"/longbridge-*; do
    # -e misses dangling symlinks; -L catches them
    if [ -e "$entry" ] || [ -L "$entry" ]; then
      run rm -rf "$entry"
      removed=$((removed + 1))
    fi
  done

  # 2) install the current repo's skills fresh
  installed=0
  for slug in "${SLUGS[@]}"; do
    src="$SKILLS_SRC/$slug"
    dst="$target/$slug"
    if [ "$MODE" = "link" ]; then
      run ln -sfn "$src" "$dst"
    else
      run cp -R "$src" "$dst"
    fi
    installed=$((installed + 1))
  done

  echo "  removed $removed old entr$([ "$removed" -eq 1 ] && echo y || echo ies), installed $installed skills"
  echo
done

if [ "$DRY_RUN" -eq 1 ]; then
  echo "Dry run complete — nothing was changed."
else
  echo "Done. Restart any open agent session so it re-scans the skills directory."
fi
