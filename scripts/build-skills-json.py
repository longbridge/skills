#!/usr/bin/env python3
"""Generate skills.json from all skills/<slug>/SKILL.md frontmatter.

Usage:
    python3 scripts/build-skills-json.py [--output PATH]

Output defaults to skills.json at the repository root.
"""
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    print("pyyaml is required: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

REPO_ROOT = Path(__file__).parent.parent
SKILLS_DIR = REPO_ROOT / "skills"


def parse_frontmatter(content: str) -> dict:
    if not content.startswith("---"):
        return {}
    end = content.find("\n---", 4)
    if end == -1:
        return {}
    return yaml.safe_load(content[4:end]) or {}


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate skills.json")
    parser.add_argument(
        "--output",
        default=str(REPO_ROOT / "skills.json"),
        help="Output file path (default: skills.json at repo root)",
    )
    args = parser.parse_args()

    skills = []
    errors = 0

    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue
        try:
            fm = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
            description = (fm.get("description") or "").strip()
            skills.append(
                {
                    "slug": skill_dir.name,
                    "name": fm.get("name", skill_dir.name),
                    "description": description,
                    "metadata": fm.get("metadata") or {},
                }
            )
        except Exception as exc:
            print(f"Warning: failed to parse {skill_md}: {exc}", file=sys.stderr)
            errors += 1

    output = {
        "version": "1.0",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "skills": skills,
    }

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"Generated {out_path} with {len(skills)} skills ({errors} errors)")


if __name__ == "__main__":
    main()
