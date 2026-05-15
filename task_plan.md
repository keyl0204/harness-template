# Task Plan

## Goal

Generate this repository as a Copier template for Harness + subagents + skills project scaffolding, based on:

- `copier_harness_landing_plan.md`
- `harness工程+子agent项目工程建设指导方案.md`

## Phases

| Phase | Status | Notes |
|---|---|---|
| Read source plans and current workspace | complete | Only two plan documents existed at start. |
| Create Copier template core files | complete | Added `copier.yml`, rendered root files, validation commands. |
| Create `.harness/` structure | complete | Agents, workflows, rules, skills, state, scripts. |
| Create `docs/` templates | complete | Product, domain, architecture, operations, ADR. |
| Add starter code and tests | complete | Minimal Python app/test placeholders. |
| Verify template shape | complete | Copier render checks, JSON/TOML/Python syntax checks. |
| Move Docker templates into `docker/` | complete | `docker/Dockerfile.jinja` and `docker/docker-compose.yml.jinja`; updated Copier exclude rules. |
| Localize generated docs to Simplified Chinese | complete | Updated generated README/AGENTS, docs, Harness agents/workflows/rules/skills/state text. |

## Decisions

- Treat `D:\codeProject\ai\harness-template` as the template repository.
- Keep `AGENTS.md` generated from `AGENTS.md.jinja`; do not create a rendered `AGENTS.md` in this template repo unless needed later.
- Keep `.harness/` and `docs/` mostly template-ready plain Markdown; use `.jinja` only where project variables are needed.

## Errors Encountered

| Error | Attempt | Resolution |
|---|---|---|
| Copier copy attempted interactive prompt in no-console shell | 1 | Re-ran with `--defaults` and explicit `-d` values. |
| Initial exclude rules matched source names or broad basenames | 1 | Switched to rendered destination names and root-only planning file excludes. |
