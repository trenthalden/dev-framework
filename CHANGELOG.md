# Changelog

This repository uses semantic versions. `1.x` is still a beta: a minor tag in this beta has already
changed defaults. Read this file before updating. Tags use `dev-framework--vX.Y.Z`.

## Unreleased

Fixes from installing into a content repository (KnowledgeBase, 2026-10-02):

- `install.py --help` crashed with `UnicodeEncodeError` on a cp1251 console (the `→` in `--kind` help).
  It now writes UTF-8 with replacement, as `check.py` already did; `finish` runs child commands with
  `PYTHONIOENCODING=utf-8`. KE-2026-10-02-CONSOLE-ENCODING.
- The secret heuristic accepts documentation stand-ins (`your-key`, `fc-your-key`, `<your key>`, `sk-...`, `fc-***`, `xxxx`)
  and `max_tokens: 4096`; real-shaped keys are still caught.
- New `secret_scan.exclude` in project.json: path globs left out of the worktree scan only. Doctor and
  `finish` name them every run; `commit-check` still scans those paths staged. KE-2026-10-02-SECRET-STANDINS.

## 1.6.1 — 2026-09-24

Tag `dev-framework--v1.6.1`. Public page, MIT license file, and a fix: `doctor` and package verify no longer treat a local Devlog as product documentation.

## 1.6.0 — 2026-09-23

Tag `dev-framework--v1.6.0`. Architecture healthcheck and templates for building an AI agent.

## 1.5.0 — 2026-09-23

Tag `dev-framework--v1.5.0`. Project kinds, lean/advanced testing, and a smaller gate.

## 1.4.1 — 2026-09-23

Tag `dev-framework--v1.4.1`. Fixes from the first agent-run live test.

## 1.4.0 — 2026-09-23

Tag `dev-framework--v1.4.0`. Under-construction marker. Devlog can be filled from the session log.

## 1.3.1 — 2026-09-23

Tag `dev-framework--v1.3.1`. Fixes from a live tool install.

## 1.3.0 — 2026-09-23

Tag `dev-framework--v1.3.0`. Development kinds: product, tool, explore.

## 1.2.4 — 2026-09-22

Tag `dev-framework--v1.2.4`. Counted evidence for a pytest suite.

## 1.2.3 — 2026-09-22

Tag `dev-framework--v1.2.3`. Fixes from a from-scratch Claude Code install.

## 1.2.2 — 2026-09-22

Tag `dev-framework--v1.2.2`. Package verification on Python 3.10–3.13, Linux and Windows.

## 1.2.1 — 2026-09-22

Tag `dev-framework--v1.2.1`. The session-start hook no longer runs code from the opened repository.

## 1.2.0 — 2026-09-22

Tag `dev-framework--v1.2.0`. The cost of a repeated check is part of the contract.

## 1.0.0-beta — 2026-09-22

Tag `v1.0.0-beta`. First tagged Hermes plugin beta: navigation, gates, and hostcheck.
