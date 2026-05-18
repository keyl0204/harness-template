---
name: harness-review
description: 审计、升级或验证 Harness 工程脚手架时使用。该 Skill 检查 AGENTS、子 Agent、Skills、工作流、规则、文档、脚本、验证命令、项目类型兼容性和整体成熟度缺口。
---

# Harness Review Skill

## 适用场景

- 审查项目是否具备完整 Harness 工程结构。
- 升级 Agent、Skills、工作流或规则目录。
- 检查模板生成后的文件路由、验证命令和文档边界。
- 评估 Harness 成熟度、缺失项和下一步补齐顺序。
- 清理旧项目类型、旧模型、旧命令或失效引用。

## 必须读取

1. `AGENTS.md` 或 `AGENTS.md.jinja`
2. `.harness/rules/codex-rules.md`
3. `.harness/rules/doc-boundary-rules.md`
4. `.harness/agents/*.md`
5. `.harness/config/models.yml`（存在时）
6. `.harness/skills/*/SKILL.md`
7. `.harness/workflows/*.md`
8. `README.md`、`README.md.jinja`、`Makefile` 或 `Makefile.jinja`
9. 模板项目还要读取 `copier.yml`

## 成熟度标准

### L1：可用

- 存在 `AGENTS.md` 作为入口和文档路由。
- 存在 `.harness/rules/`、`.harness/workflows/`、`.harness/skills/`。
- 存在最小 `make test` 或等价验证入口。
- 文档边界清楚，不混写业务需求和 AI 工作规则。

### L2：可协作

- 子 Agent 有清晰职责、输入、输出和限制。
- Skills 有触发描述、执行步骤、质量门禁和输出格式。
- 工作流能把 planner、mapper、engineer、tester、reviewer、reporter 串起来。
- 常见任务能落到明确 skill 和验证命令。
- README、AGENTS、workflows 和 scripts 引用一致。

### L3：可治理

- 子 Agent 有集中模型 profile、推理强度、兼容兜底模型和专业领域配置。
- 安全、测试、审查、文档边界规则可执行。
- 模板支持不同项目类型，并且生成后无旧分支残留。
- 有状态文件、handoff、feature list 和可重复验证脚本。
- 高风险变更有安全审查、权限测试和运维回滚路径。

## 检查清单

1. 文件结构完整：agents、skills、rules、workflows、state、scripts、docs。
2. `AGENTS.md` 路由准确，引用文件存在。
3. Agent 元数据完整：`agent_type`、`model_profile` 或 `model`、`reasoning_effort`、`specialization`。
4. `model_profile` 必须能在 `.harness/config/models.yml` 的 `profiles` 中找到；缺少集中配置时 agent 文件必须保留 `model` 兜底。
5. Skill frontmatter 完整：`name`、`description`，且 description 能准确触发。
6. Skill 内容包含适用场景、必须读取、流程、质量门禁、验证和输出格式。
7. 工作流引用的 agent 和 skill 都存在。
8. 项目类型、包管理器、命令示例和脚本分支一致。
9. 文档没有把业务事实写进 `.harness/` 或把 AI 工作规则写进 `docs/`。
10. `make check` 或等价验证可达，并包含 Harness 自检。
11. 安全、测试、审查规则能覆盖高风险改动。

## 输出格式

```text
Harness 成熟度：L1 / L2 / L3

通过项：
- ...

缺失项：
- [P1] ...

不一致项：
- ...

优先补齐：
- ...

建议：
- ...
```
