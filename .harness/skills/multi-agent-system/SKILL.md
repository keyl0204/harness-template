---
name: multi-agent-system
description: 设计、实现、修改或审查 multi-agent 系统、Agent 角色、工具、handoff、memory、guardrails、终止条件、编排或 Agent 评估时使用。尤其适用于 project_type=multi-agent 和 OpenAI Agents SDK 风格系统。
---

# Multi-Agent System Skill

## 适用场景

- 新增或修改 agent 角色、工具、handoff、memory 或 orchestration。
- 设计 planner、researcher、executor、reviewer 等多角色协作。
- 排查 agent 循环、工具误用、上下文泄露、任务漂移或无法停止。
- 为 agent 工具调用、handoff、权限和失败路径补测试或评估。
- 审查 prompt、系统指令、工具 schema、输出结构和安全边界。

## 必须读取

1. `AGENTS.md`
2. `.harness/rules/coding-rules.md`
3. `.harness/rules/testing-rules.md`
4. `.harness/rules/security-rules.md`
5. `docs/architecture/overview.md`
6. 涉及业务行为时读取相关 `docs/product/` 和 `docs/domain/`
7. 现有 agent、tool、memory、handoff、eval 和测试代码

## Agent 设计边界

- Role：每个 agent 的职责、非职责和成功标准。
- Model：不同角色使用的模型、推理强度和成本/延迟取舍。
- Tools：可调用工具、参数 schema、权限、超时和失败处理。
- Handoff：交接条件、传递上下文、拒绝交接和回退策略。
- Memory：可保存内容、保留时间、隐私边界和检索方式。
- Termination：停止条件、最大轮次、错误终止和人工接管。
- Evaluation：任务完成率、工具正确率、安全拒绝、成本和延迟。

## 工作流程

1. 明确用户任务是否真的需要多 agent；单 agent 足够时保持简单。
2. 定义每个 agent 的职责边界，避免多个 agent 争夺同一决策。
3. 为每个工具定义 schema、allowlist、权限校验、超时和审计。
4. 设计 handoff 条件和停止条件，防止循环和任务漂移。
5. 控制上下文传递，最小化敏感信息和无关历史。
6. 实现最小可测试切片，优先让 agent 协作路径可观察。
7. 补测试或评估：工具成功、工具失败、拒绝、handoff、停止、越权。

## 安全门禁

- Agent 不直接获得不必要的密钥、凭据或全量用户隐私。
- LLM 输出不能直接作为 shell、SQL、文件路径、权限判断或高风险工具参数。
- 工具调用必须经过结构化校验，不能拼接自由文本。
- Handoff 不传递超出下游 agent 职责所需的敏感上下文。
- 必须有最大轮次、超时或其他终止保护。
- 高风险动作必须有服务端校验、人工确认或审计。

## 测试和评估重点

- 角色是否按职责行动。
- 工具参数是否符合 schema。
- 工具失败是否可恢复。
- Handoff 是否在正确条件触发。
- Agent 是否能停止，不进入循环。
- 安全边界是否拒绝越权和敏感操作。

## 验证命令

```bash
make test
make check
```

可聚焦运行：

```bash
uv run pytest tests/test_*agent*.py -q
```

## 输出格式

```text
Agent 设计：
- roles:
- tools:
- handoffs:
- termination:

核心改动：
- ...

安全边界：
- ...

测试或评估：
- ...

验证命令：
- ...

剩余风险：
- ...
```
