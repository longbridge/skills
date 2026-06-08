#!/usr/bin/env bash
#
# update.sh — fully (re)install the Longbridge skills into every agent skills directory,
# wiping any previously-installed `longbridge` / `longbridge-*` entries first.
#
# Works two ways from the SAME script:
#   • Remote one-liner (no clone needed) — clones the latest skills and installs them:
#       curl -fsSL https://raw.githubusercontent.com/longbridge/skills/main/scripts/update.sh | bash
#       curl -fsSL .../scripts/update.sh | bash -s -- --dry-run        # preview
#   • Local repo (for development) — runs from a checkout and installs from ./skills:
#       scripts/update.sh                 # copy-install into every detected agent dir
#       scripts/update.sh --link          # symlink back to the repo for live edits
#       scripts/update.sh --dry-run       # preview only
#       scripts/update.sh --target DIR    # restrict to one dir (repeatable)
#
# WHY: `npx skills update` only refreshes skills whose slug still exists upstream — it
# leaves renamed/removed skills as stale orphans and never adds brand-new names. This
# does a clean wipe-and-install so each target mirrors the current skills/ set.
#
# OPTIONS
#   --link        Symlink each skill back to the repo (local mode only; ignored remotely).
#   --dry-run     Print what would change, touch nothing.
#   --target DIR  Install into DIR (the skills dir itself, e.g. ~/.claude/skills). Repeatable.
#   -h, --help    Show this help.
#
# ENV (remote mode)
#   LONGBRIDGE_SKILLS_REPO   GitHub owner/repo   (default: longbridge/skills)
#   LONGBRIDGE_SKILLS_REF    branch or tag       (default: main)
#
# DEFAULT TARGETS (only those whose parent dir already exists are used)
#   ~/.claude/skills  ·  ~/.agents/skills  ·  ~/.gemini/skills  ·  ~/.opencode/skills
#
set -euo pipefail

MODE="copy"
DRY_RUN=0
declare -a TARGETS=()

usage() { sed -n '2,33p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; exit "${1:-0}"; }

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

# --- resolve the skills source ---------------------------------------------------
# If this script is a real file inside a checkout with a sibling ../skills, use it
# (local mode). Otherwise — e.g. piped through `curl | bash` — clone the latest.
SKILLS_SRC=""
LOCAL=0
self="${BASH_SOURCE[0]:-}"
if [ -n "$self" ] && [ -f "$self" ]; then
  here="$(cd "$(dirname "$self")" && pwd)"
  if ls "$here/../skills"/*/SKILL.md >/dev/null 2>&1; then
    SKILLS_SRC="$(cd "$here/../skills" && pwd)"
    LOCAL=1
  fi
fi

if [ -z "$SKILLS_SRC" ]; then
  command -v git >/dev/null 2>&1 || { echo "error: git is required to fetch skills" >&2; exit 1; }
  REPO_SLUG="${LONGBRIDGE_SKILLS_REPO:-longbridge/skills}"
  REF="${LONGBRIDGE_SKILLS_REF:-main}"
  TMP="$(mktemp -d)"
  trap 'rm -rf "$TMP"' EXIT
  echo "Fetching $REPO_SLUG@$REF ..."
  git clone --depth 1 --branch "$REF" "https://github.com/$REPO_SLUG.git" "$TMP/repo" >/dev/null 2>&1 \
    || { echo "error: failed to clone https://github.com/$REPO_SLUG.git ($REF)" >&2; exit 1; }
  SKILLS_SRC="$TMP/repo/skills"
fi

if [ ! -d "$SKILLS_SRC" ] || ! ls "$SKILLS_SRC"/*/SKILL.md >/dev/null 2>&1; then
  echo "error: no skills found under $SKILLS_SRC" >&2
  exit 1
fi

# --link only makes sense against a persistent local checkout
if [ "$MODE" = "link" ] && [ "$LOCAL" -ne 1 ]; then
  echo "note: --link ignored (no local checkout; installing copies instead)" >&2
  MODE="copy"
fi

# --- collect the slugs to install (dirs containing a SKILL.md) -------------------
declare -a SLUGS=()
for d in "$SKILLS_SRC"/*/; do
  [ -f "$d/SKILL.md" ] || continue
  SLUGS+=("$(basename "$d")")
done

# --- resolve targets: explicit --target wins; else auto-detect existing agents ---
if [ ${#TARGETS[@]} -eq 0 ]; then
  for cand in \
    "$HOME/.claude/skills" \
    "$HOME/.agents/skills" \
    "$HOME/.gemini/skills" \
    "$HOME/.opencode/skills"; do
    [ -d "$(dirname "$cand")" ] && TARGETS+=("$cand")  # only where the agent home exists
  done
fi

if [ ${#TARGETS[@]} -eq 0 ]; then
  echo "No agent directories detected (~/.claude, ~/.agents, ~/.gemini, ~/.opencode)." >&2
  echo "Pass one explicitly, e.g.:  scripts/update.sh --target ~/.claude/skills" >&2
  exit 1
fi

run() { if [ "$DRY_RUN" -eq 1 ]; then echo "  [dry-run] $*"; else "$@"; fi; }

echo "Source : $SKILLS_SRC (${#SLUGS[@]} skills$([ "$LOCAL" -eq 1 ] && echo ', local' || echo ', cloned'))"
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

  # 2) install the current skills fresh
  for slug in "${SLUGS[@]}"; do
    if [ "$MODE" = "link" ]; then
      run ln -sfn "$SKILLS_SRC/$slug" "$target/$slug"
    else
      run cp -R "$SKILLS_SRC/$slug" "$target/$slug"
    fi
  done

  echo "  removed $removed old entr$([ "$removed" -eq 1 ] && echo y || echo ies), installed ${#SLUGS[@]} skills"
  echo
done

if [ "$DRY_RUN" -eq 1 ]; then
  echo "Dry run complete — nothing was changed."
else
  echo "Done. Restart any open agent session so it re-scans the skills directory."
fi
