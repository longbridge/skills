#!/usr/bin/env bash
#
# update.sh — ONE-LINER fresh update of the Longbridge skills (no git clone needed).
#
# Pulls the latest skills straight from GitHub, wipes every previously-installed
# `longbridge` / `longbridge-*` entry from each detected agent skills directory
# (~/.claude, ~/.agents, ~/.gemini, ~/.opencode), then installs the latest set fresh.
# This is the safe way to upgrade across a release that renamed or removed skills —
# unlike `npx skills update`, it leaves no stale orphans behind.
#
# RUN IT
#   curl -fsSL https://raw.githubusercontent.com/longbridge/skills/main/scripts/update.sh | bash
#
#   # preview without changing anything
#   curl -fsSL https://raw.githubusercontent.com/longbridge/skills/main/scripts/update.sh | bash -s -- --dry-run
#
# ENV OVERRIDES
#   LONGBRIDGE_SKILLS_REPO   GitHub owner/repo   (default: longbridge/skills)
#   LONGBRIDGE_SKILLS_REF    branch or tag       (default: main)
#
# Requires: git. All extra args are forwarded to reinstall.sh (e.g. --dry-run, --target DIR).
#
set -euo pipefail

REPO_SLUG="${LONGBRIDGE_SKILLS_REPO:-longbridge/skills}"
REF="${LONGBRIDGE_SKILLS_REF:-main}"

command -v git >/dev/null 2>&1 || { echo "error: git is required" >&2; exit 1; }

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "Fetching $REPO_SLUG@$REF ..."
git clone --depth 1 --branch "$REF" "https://github.com/$REPO_SLUG.git" "$TMP/repo" >/dev/null 2>&1 \
  || { echo "error: failed to clone https://github.com/$REPO_SLUG.git ($REF)" >&2; exit 1; }

# Delegate the wipe-and-install to the repo's own installer (copy mode is the default).
bash "$TMP/repo/scripts/reinstall.sh" "$@"
