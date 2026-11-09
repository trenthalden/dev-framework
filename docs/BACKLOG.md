# DEV Framework backlog

Current release record, 24 September 2026: tag `dev-framework--v1.6.0` is on `origin/main`, and CI
for `9efa0d7` was green. The v0.2 notes below are the 31 August record. They are not the current
"not published" status.

## In progress

- Proportional engineering/testing rules — v1.6.2, owner-authorized Nov5, local only.
  Canonical AGENTS, agent guidelines, checklist and healthcheck wording now require
  a short periodic architecture/testing simplicity checkpoint and early authorized
  real-agent functional acceptance. Removed heavy-overlay delay justification,
  clarified synthetic regression vs real-agent evidence and full-gate boundaries.
  Synced process copies in the package and active consumer without reinstalling or
  overwriting project WIP. Existing installer propagation/conflict scenario PASS
  (1 test,0.116s); doctor READY and task diff whitespace check clean. Owner then
  authorized the1.6.2 version bump, local commit and active-profile plugin update.
  No runtime code changes, push, remote tag or publication authorized.

- Cursor adapter — authorized 2026-10-02, local only (no commit/push/publish). Plan, decisions and
  live result: [HOSTS_PLAN_2026-09-23.md](HOSTS_PLAN_2026-09-23.md) §4.

- DEV Framework as a product (Hermes plugin v0.4.0, host adapters, evals, hostcheck) — authorized
  2026-09-21; checklist [PLUGIN_CHECKLIST.md](PLUGIN_CHECKLIST.md); token analysis
  [TOKEN_BUDGET_2026-09-20.md](TOKEN_BUDGET_2026-09-20.md).

- Second-review hardening — authorized 2026-08-31; [PLAN.md](PLAN.md), portions 5-8.
  False-green verification, common secret formats and source-lesson coverage fixed;
  79 tests passed. Disposable pilot has real red/green evidence; native provider handoff
  BLOCKED by Claude expired OAuth and Codex read policy. No commit/push before acceptance.

## Earlier verification (not final acceptance)

- v0.2 — approved review improvements. Scope, evidence and handoff: [PLAN.md](PLAN.md).
  Out: application integrations, changes to Main OS, deployment and cross-provider account
  automation. Status: implementation verified, awaiting acceptance. Final local suite:
  63 tests passed; no commits/pushes. Hosted CI and live provider sessions not yet run.

## Next

- **Idea (operator, 2026-09-23): a separate repository for AI agents, NOT part of DEV Framework.** It would hold
  the human → agent → agent flow (an orchestrating agent directing an engineer agent that builds production
  agents), the engineer's known-errors memory, plan-review protocol and consultation log. Research to start
  from: `D:\DEV\Hermes\docs\research\HUMAN_AGENT_AGENT_FLOW_2026-09-23.md`. DEV Framework keeps only what a
  person needs to build an agent: `template/.devframework/agents/` (guidelines, agent card, eval set, retirement).
- Host adapters Cursor → Codex → OpenCode (D4 reordered 2026-10-02: Cursor first). Plan and decisions
  (D1 done, D2 cancelled, D3 project-local JS for OpenCode): [HOSTS_PLAN_2026-09-23.md](HOSTS_PLAN_2026-09-23.md) §3–§5.
- Acceptance follows second-review evidence, then authorized commit/push and hosted CI.

## Recently finished

- Initial documentation package — d3d63d2; historical plan in archive/PLAN.md.
