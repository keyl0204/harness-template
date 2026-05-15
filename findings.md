# Findings

## Source Documents

- `copier_harness_landing_plan.md` defines the target as a Copier template that can generate `AGENTS.md`, `.harness/`, `docs/`, `Makefile`, scripts, source and test placeholders.
- `harness工程+子agent项目工程建设指导方案.md` reinforces the boundary: `.harness/` describes how AI participates in engineering; `docs/` describes product, domain, architecture and operations facts.

## Implementation Notes

- The template should include short `AGENTS.md` routing, not a large knowledge base.
- The generated project must expose `make setup`, `make dev`, `make lint`, `make typecheck`, `make test`, and `make check`.
