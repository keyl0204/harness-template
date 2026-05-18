# Security Fix 工作流

## 适用场景

修复安全、权限、数据暴露或敏感操作问题。

## 流程

1. `planner` 识别受影响的 actor、resource、action 和 condition。
2. 读取 `.harness/skills/security-review/SKILL.md`。
3. 读取 `docs/domain/permission-model.md` 和相关架构文档。
4. `code_mapper` 梳理校验点和绕过风险。
5. Engineer 实现最小安全修复。
6. `test_writer` 使用 `.harness/skills/test-writing/SKILL.md` 补滥用、绕过和回归测试。
7. `security_reviewer` 审查改动。
8. 配置了安全检查时运行 `make check` 和 `make security`。
9. `reporter` 总结影响范围和验证结果。

## 禁止

- 记录密钥。
- 静默削弱授权逻辑。
- 把安全测试当作可选项。
