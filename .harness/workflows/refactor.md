# Refactor 工作流

## 适用场景

在不改变预期行为的前提下改进结构。

## 流程

1. `planner` 确认重构目标和不改变行为的边界。
2. `code_mapper` 识别受影响代码和测试。
3. Engineer 做小步机械修改。
4. 结构变化影响测试时，`test_writer` 读取 `.harness/skills/test-writing/SKILL.md` 更新等价覆盖。
5. `reviewer` 检查是否出现行为漂移。
6. 运行 `make check`。
7. `reporter` 说明改了什么，以及为什么行为应保持不变。

## 禁止

- 未经明确允许就改变公开行为。
- 把功能开发混入重构。
- 删除测试但不提供等价覆盖。
