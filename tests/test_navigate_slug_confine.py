"""Slug confinement for vendored navigate.py checklist/handoff (path traversal fix, 1.6.3).

RED on 1.6.2: ``docs / f"{slug}.md"`` with ``../x`` created/appended/deleted
``.md`` files outside ``docs/``. GREEN: only ``[A-Za-z0-9._-]+``, resolved path
must stay under ``root/docs`` before any read/write/unlink.
"""
from __future__ import annotations

import importlib.util
import os
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

NAV_PATH = ROOT / "template" / ".devframework" / "navigate.py"
TEMPLATE = ROOT / "template" / "docs" / "CHECKLIST_TEMPLATE.md"


def _load_nav():
    spec = importlib.util.spec_from_file_location("df_navigate_under_test", NAV_PATH)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def _seed_repo(base: Path) -> Path:
    repo = base / "repo"
    docs = repo / "docs"
    docs.mkdir(parents=True)
    shutil.copy(TEMPLATE, docs / "CHECKLIST_TEMPLATE.md")
    (base / "outside").mkdir(parents=True, exist_ok=True)
    return repo


class NavigateSlugConfineTests(unittest.TestCase):
    def setUp(self):
        self.nav = _load_nav()
        root = str(Path("/tmp").resolve()) if os.name != "nt" else None
        self.base = Path(tempfile.mkdtemp(prefix="nav-slug-", dir=root))
        self.addCleanup(lambda: shutil.rmtree(self.base, ignore_errors=True))
        self.repo = _seed_repo(self.base)
        self.outside = self.base / "outside"
        # Sibling of docs inside repo (classic ../ escape target).
        self.repo_outside = self.repo / "outside"
        self.repo_outside.mkdir(exist_ok=True)
        (self.repo_outside / "sentinel.md").write_text("keep\n", encoding="utf-8")

    def _outside_snapshot(self):
        snap = {}
        for root in (self.outside, self.repo_outside):
            for p in root.rglob("*"):
                if p.is_file():
                    snap[str(p)] = p.read_text(encoding="utf-8")
        return snap

    def _assert_refused(self, action: str, slug: str, text: str = ""):
        before = self._outside_snapshot()
        docs_before = {p.name: p.read_text(encoding="utf-8") for p in (self.repo / "docs").glob("*.md")}
        with self.assertRaises(ValueError) as ctx:
            if action == "handoff":
                self.nav.handoff(self.repo, slug, text or "note")
            else:
                self.nav.checklist(self.repo, action, slug, text)
        self.assertIn("invalid checklist slug", str(ctx.exception).lower() + str(ctx.exception))
        self.assertEqual(self._outside_snapshot(), before)
        docs_after = {p.name: p.read_text(encoding="utf-8") for p in (self.repo / "docs").glob("*.md")}
        self.assertEqual(docs_after, docs_before)

    def test_refuse_traversal_slugs_new(self):
        for slug in ("../x", "../../x", "a/b", "/tmp/x", "..", ".", "...", ".hidden"):
            with self.subTest(slug=slug):
                self._assert_refused("new", slug, "evil")

    def test_refuse_traversal_slugs_add_tick_archive_handoff(self):
        # Legitimate checklist first.
        self.nav.checklist(self.repo, "new", "ok-plan", "title")
        for action, slug, text in (
            ("add", "../x", "item"),
            ("tick", "../../x", "1"),
            ("archive", "../x", ""),
            ("handoff", "../x", "note"),
            ("add", "a/b", "item"),
            ("handoff", "/abs", "note"),
        ):
            with self.subTest(action=action, slug=slug):
                self._assert_refused(action, slug, text)

    def test_refuse_symlinked_docs_escaping_root(self):
        """If docs/ is a symlink outside the repo, refuse before any write."""
        evil_docs = self.outside / "evil-docs"
        evil_docs.mkdir()
        shutil.copy(TEMPLATE, evil_docs / "CHECKLIST_TEMPLATE.md")
        repo2 = self.base / "symlink-repo"
        repo2.mkdir()
        (repo2 / "docs").symlink_to(evil_docs)
        before = list(evil_docs.iterdir())
        with self.assertRaises(ValueError) as ctx:
            self.nav.checklist(repo2, "new", "pwn", "title")
        self.assertIn("escapes", str(ctx.exception).lower())
        self.assertEqual(list(evil_docs.iterdir()), before)

    def test_refuse_symlinked_checklist_file_escaping_docs(self):
        """Existing docs/<slug>.md that is a symlink outside docs/ → refuse."""
        target = self.repo_outside / "linked.md"
        target.write_text(
            "# linked\n**Status:** in progress\n**Started:** 2026-01-01\n\n- [ ] one\n\n## Handoff\n",
            encoding="utf-8",
        )
        link = self.repo / "docs" / "linked.md"
        link.symlink_to(target)
        before = target.read_text(encoding="utf-8")
        with self.assertRaises(ValueError):
            self.nav.handoff(self.repo, "linked", "should not append")
        self.assertEqual(target.read_text(encoding="utf-8"), before)
        with self.assertRaises(ValueError):
            self.nav.checklist(self.repo, "add", "linked", "nope")
        self.assertEqual(target.read_text(encoding="utf-8"), before)

    def test_legitimate_slug_still_works(self):
        out = self.nav.checklist(self.repo, "new", "sprint-1", "Ship it")
        self.assertIn("created docs/sprint-1.md", out)
        path = self.repo / "docs" / "sprint-1.md"
        self.assertTrue(path.is_file())
        self.nav.checklist(self.repo, "add", "sprint-1", "do the thing")
        self.nav.handoff(self.repo, "sprint-1", "paused")
        text = path.read_text(encoding="utf-8")
        self.assertIn("do the thing", text)
        self.assertIn("paused", text)
        # Tick + archive stay inside docs/
        self.nav.checklist(self.repo, "tick", "sprint-1", "1")
        archived = self.nav.checklist(self.repo, "archive", "sprint-1", "")
        self.assertIn("docs/archive/sprint-1.md", archived)
        self.assertFalse(path.exists())
        self.assertTrue((self.repo / "docs" / "archive" / "sprint-1.md").is_file())
        self.assertEqual((self.repo_outside / "sentinel.md").read_text(encoding="utf-8"), "keep\n")

if __name__ == "__main__":
    unittest.main()
