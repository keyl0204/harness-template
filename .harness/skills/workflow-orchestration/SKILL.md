---
name: workflow-orchestration
description: 设计、实现、修改或调试 workflow 编排、状态机、graph 节点、重试、幂等、定时任务、长任务、补偿逻辑或失败恢复时使用。尤其适用于 project_type=workflow 和 LangGraph 风格执行。
---

# Workflow Orchestration Skill

## 适用场景

- 新增或修改工作流、状态机、graph、pipeline、job 或长任务。
- 设计节点输入输出、边条件、重试、补偿、回滚或恢复。
- 排查重复执行、任务卡死、顺序错误、状态不一致或部分失败。
- 接入队列、定时任务、外部服务、人工审批或异步回调。
- 为 workflow 行为补充测试、观测和运维说明。

## 必须读取

1. `AGENTS.md`
2. `.harness/rules/coding-rules.md`
3. `.harness/rules/testing-rules.md`
4. `.harness/rules/security-rules.md`
5. `docs/domain/state-machines.md`
6. `docs/architecture/overview.md`
7. 涉及运维时读取 `docs/operations/runbook.md`
8. 现有 workflow、job、queue、state 和测试代码

## 设计边界

- Trigger：谁启动工作流，输入是什么，是否允许重复启动。
- State：持久化哪些状态，状态转移是否合法。
- Node：每个节点的输入、输出、副作用、失败行为。
- Edge：分支条件、终止条件、重试和跳转规则。
- Idempotency：重复请求、重试、恢复和并发执行如何处理。
- Compensation：部分成功后如何撤销、补偿或人工处理。
- Observability：trace id、run id、node id、状态、耗时、错误和审计。

## 工作流程

1. 画清楚工作流边界：触发器、状态、节点、边、终止条件。
2. 明确每个节点是否有副作用，以及副作用是否幂等。
3. 设计失败策略：重试次数、退避、可恢复错误、不可恢复错误。
4. 检查权限和数据范围，尤其是人工审批、批量操作和外部回调。
5. 实现最小改动，保持节点输入输出结构化。
6. 补测试：成功路径、失败路径、重试、重复执行、非法状态转移。
7. 更新架构或运维文档，说明如何观察、恢复和回滚。

## 质量门禁

- 不把整个流程写成不可测试的单个大函数。
- 节点之间不共享隐式全局状态。
- 重试不能造成重复扣费、重复通知、重复删除或重复写入。
- 状态转移必须可验证，不接受任意字符串状态跳转。
- 外部回调必须验证来源、签名或关联 run id。
- 长任务必须有超时、取消或恢复策略。

## 验证命令

```bash
make test
make check
```

可聚焦运行：

```bash
uv run pytest tests/test_*workflow*.py -q
```

## 输出格式

```text
工作流边界：
- trigger:
- state:
- nodes:
- terminal states:

核心改动：
- ...

幂等和失败恢复：
- ...

测试覆盖：
- ...

验证命令：
- ...

剩余风险：
- ...
```
