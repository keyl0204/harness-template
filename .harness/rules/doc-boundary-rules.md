# 文档边界规则

## `.harness/` 可以包含

- Agent 角色协议
- Codex 工作流
- AI 工作规则
- Skills
- 任务状态
- 验证脚本说明

## `docs/` 可以包含

- 产品需求
- 用户故事
- 业务规则
- 架构设计
- API 规范
- 数据库设计
- 运维说明
- ADR

## 禁止

1. 不要在 PRD 中写 Codex 工作流。
2. 不要在 Skill 中写具体业务需求。
3. 不要把 `AGENTS.md` 写成完整需求文档。
4. 不要在 `.harness/agents/` 中写项目业务规则。
5. 不要在 `docs/product/` 中写 AI 角色分工。

## 更新规则

- 业务行为变化时更新 `docs/product/` 或 `docs/domain/`。
- AI 工作方式变化时更新 `.harness/`。
- 技术设计变化时更新 `docs/architecture/`。
