---
name: security-review
description: 审查或修改认证、授权、租户隔离、密钥、文件/网络/shell 操作、上传、Webhook、破坏性操作、RAG 访问控制、workflow 执行或 Agent 工具调用时使用。该 Skill 聚焦具体信任边界、攻击路径、测试和最小安全修复。
---

# Security Review Skill

## 适用场景

- 认证、授权、角色、租户隔离或权限模型变化。
- 处理密钥、令牌、凭据、Webhook secret 或敏感个人信息。
- 基于用户输入读写文件、访问网络、执行 shell 或调用外部系统。
- 实现管理员、删除、批量修改、导出、账单或不可逆操作。
- 修改 RAG 检索、Agent 工具调用、workflow 节点或 LLM prompt 拼接。
- 审查日志、监控、错误响应和数据脱敏。

## 必须读取

1. `AGENTS.md`
2. `.harness/rules/security-rules.md`
3. `.harness/rules/review-rules.md`
4. `docs/domain/permission-model.md`
5. 涉及业务约束：`docs/domain/business-rules.md`
6. 涉及 API、数据库、文件或外部系统：相关 `docs/architecture/`
7. 相关实现、配置、测试和日志路径

## 审查流程

1. 标出信任边界：外部输入、内部服务、数据库、文件、网络、LLM、工具。
2. 建模权限：actor、resource、action、condition。
3. 沿调用链检查服务端校验点，不能只看前端显示逻辑。
4. 检查敏感数据流：读取、传输、日志、错误、缓存、prompt、导出。
5. 检查注入风险：SQL/DSL、shell、模板、路径、SSRF、prompt injection。
6. 检查高风险操作：幂等、确认、审计、速率限制、回滚。
7. 验证测试覆盖：允许访问、拒绝访问、恶意输入、失败路径。
8. 输出具体风险和最小修复方向。

## AI 和工具调用专项

- Prompt 中不放入不必要的密钥、凭据、原始隐私或内部策略。
- RAG 检索必须保留来源和权限过滤，不允许越权上下文进入 prompt。
- LLM 输出不能直接作为 SQL、shell、文件路径、权限判断或工具参数。
- Agent 工具必须有 allowlist、schema、超时、审计和失败处理。
- workflow 重试不能重复扣费、重复发送、重复删除或重复执行破坏性动作。

## 输出格式

```text
安全结论：通过 / 不通过

信任边界：
- ...

权限模型：
- actor:
- resource:
- action:
- condition:

风险点：
- [P1] 文件:行 - ...

必须修复：
- ...

建议补充测试：
- ...

剩余风险：
- ...
```

## 验证命令

```bash
make test
make security
make check
```
