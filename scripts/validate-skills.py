#!/usr/bin/env python3
"""
Validate every SKILL.md under skills/<skill>/.

Checks (per the Agent Skills spec at https://agentskills.io/specification):
- Frontmatter is present and parseable.
- `name` matches `^[a-z0-9]+(-[a-z0-9]+)*$` and equals the parent directory name.
- `description` is present and ≤ 1024 characters.
- SKILL.md body is ≤ 500 lines (a soft warning, per spec recommendation).
- Marketplace declares the plugin under .claude-plugin/.

All 19 skills are prompt-only — no Python tests to run. The skill folders should
contain SKILL.md (and optionally references/ files); a `scripts/` dir would be a
red flag suggesting drift back to a Python wrapper.

Exit 0 = all clean. Exit 1 = at least one error. Exit 2 = warnings only.
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_ROOT = ROOT / "skills"
SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def parse_frontmatter(path: Path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return None, text
    fm = {}
    for line in m.group(1).splitlines():
        line_match = re.match(r"^([a-zA-Z_-]+):\s*(.*)$", line)
        if line_match:
            fm[line_match.group(1)] = line_match.group(2).strip()
    body = text[m.end():]
    return fm, body


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    marketplace = ROOT / ".claude-plugin" / "marketplace.json"
    if not marketplace.exists():
        errors.append(".claude-plugin/marketplace.json missing")
    else:
        try:
            json.loads(marketplace.read_text())
        except json.JSONDecodeError as exc:
            errors.append(f"marketplace.json: invalid JSON — {exc}")

    if not SKILLS_ROOT.exists():
        errors.append("skills/ directory missing")
        print("\n".join(errors))
        return 1

    skills_seen = 0
    for skill_dir in sorted(SKILLS_ROOT.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill = skill_dir.name
        skills_seen += 1
        md = skill_dir / "SKILL.md"
        if not md.exists():
            errors.append(f"{skill}: missing SKILL.md")
            continue

        fm, body = parse_frontmatter(md)
        if fm is None:
            errors.append(f"{skill}: no YAML frontmatter")
            continue

        name = fm.get("name", "")
        if not name:
            errors.append(f"{skill}: frontmatter missing `name`")
        elif not SLUG_RE.fullmatch(name):
            errors.append(f"{skill}: name '{name}' fails slug regex {SLUG_RE.pattern}")
        elif name != skill:
            errors.append(f"{skill}: name '{name}' must match parent dir '{skill}'")

        desc = fm.get("description", "")
        if not desc:
            errors.append(f"{skill}: frontmatter missing `description`")
        elif len(desc) > 1024:
            full_desc = re.search(
                r"^description:\s*\|?\s*\n?(.*?)(?=\n[a-zA-Z_-]+:|\n---)",
                md.read_text(encoding="utf-8"),
                re.DOTALL | re.MULTILINE,
            )
            actual_len = len(full_desc.group(1).strip()) if full_desc else len(desc)
            if actual_len > 1024:
                errors.append(f"{skill}: description {actual_len} chars > 1024 limit")

        line_count = body.count("\n")
        if line_count > 500:
            warnings.append(f"{skill}: SKILL.md body is {line_count} lines (spec recommends ≤ 500)")

        test_file = skill_dir / "scripts" / "test_cli.py"
        if test_file.exists():
            proc = subprocess.run(
                [sys.executable, str(test_file)],
                capture_output=True, text=True, cwd=str(skill_dir),
            )
            if proc.returncode != 0:
                errors.append(f"{skill}: test_cli.py failed (exit {proc.returncode})\n  stderr tail: {proc.stderr.strip()[-300:]}")

    print(f"Inspected {skills_seen} skill(s).")
    for w in warnings:
        print(f"  ⚠ {w}")
    for e in errors:
        print(f"  ✗ {e}")
    if errors:
        return 1
    if warnings:
        return 2
    print("All clean ✓")
    return 0


if __name__ == "__main__":
    sys.exit(main())
