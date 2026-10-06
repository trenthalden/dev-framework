#!/usr/bin/env python3
"""Session-start hook: print the project's DEV Framework brief so the agent starts from context, not archaeology.

`--format text` (default) for hosts whose hook stdout becomes context (Claude Code); `--format cursor-json`
wraps the same text as `{"additional_context": ...}` for Cursor's sessionStart hook.

Silent (exit 0, no output) when the working directory is not a framework project — a hook must never
add noise to an unrelated session. Standard library only.

The brief is produced by the plugin's own copy of navigate.py, pointed at the project with --root.
The project supplies only data (Markdown, project.json, git state); no code from the opened
repository runs at session start, so opening a cloned stranger's repository is safe.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

MAX_CHARS = 4000
NAVIGATE = Path(__file__).resolve().parents[1] / "template" / ".devframework" / "navigate.py"  # plugin-owned code


def project_root() -> Path | None:
    start = Path(os.environ.get("CURSOR_PROJECT_DIR") or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()).resolve()
    for candidate in (start, *start.parents):
        if (candidate / ".devframework" / "navigate.py").is_file():
            return candidate
        if (candidate / ".git").exists():  # the project ends at its git root: a parent's framework is not ours
            return None
    return None


def brief(root: Path) -> str:
    try:
        run = subprocess.run([sys.executable, "-B", str(NAVIGATE), "--root", str(root), "brief"],
                             cwd=str(root), capture_output=True, text=True, encoding="utf-8",
                             errors="replace", timeout=60)
    except (OSError, subprocess.TimeoutExpired) as error:
        return f"DEV Framework brief unavailable ({error}); run `python .devframework/navigate.py brief` by hand."
    if run.returncode != 0:
        return ""
    return ("DEV Framework — session brief (read this before opening documents; "
            "`python .devframework/navigate.py find <ID|keyword>` returns one block, not a file):\n"
            + run.stdout.strip()[:MAX_CHARS])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--format", choices=("text", "cursor-json"), default="text")
    form = parser.parse_args().format
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    root = project_root()
    text = brief(root) if root else ""
    if text:  # silent outside a project in every format: a hook must not add noise
        print(json.dumps({"additional_context": text}, ensure_ascii=False) if form == "cursor-json" else text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
