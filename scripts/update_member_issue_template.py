#!/usr/bin/env python3
"""Update member issue form dropdown options from _members/*.md files."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import List


START_MARKER = "# member-slug-options:start"
END_MARKER = "# member-slug-options:end"


def member_slugs(root: Path) -> List[str]:
    members_dir = root / "_members"
    if not members_dir.exists():
        return []
    return sorted(path.stem for path in members_dir.glob("*.md"))


def update_template(root: Path) -> None:
    template_path = root / ".github" / "ISSUE_TEMPLATE" / "member-update.yml"
    content = template_path.read_text(encoding="utf-8")
    start = content.index(START_MARKER)
    end = content.index(END_MARKER)
    line_start = content.rfind("\n", 0, start) + 1
    line_end = content.find("\n", end)
    if line_end == -1:
        line_end = len(content)

    options = ["        " + START_MARKER, "        - 不适用"]
    options.extend(f"        - {slug}" for slug in member_slugs(root))
    options.append("        " + END_MARKER)
    updated = content[:line_start] + "\n".join(options) + content[line_end:]
    template_path.write_text(updated, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="Repository root.")
    args = parser.parse_args()
    update_template(Path(args.root).resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
