# Bugfix 工作流

## 适用场景

修复已确认或高度疑似的缺陷。

## 流程

1. `planner` 确认范围和验收标准。
2. 读取 `.harness/skills/bugfix/SKILL.md`，按根因分析和最小修复流程执行。
3. `code_mapper` 定位相关文件和影响范围。
4. Engineer 做最小修复。
5. `test_writer` 使用 `.harness/skills/test-writing/SKILL.md` 补回归测试。
6. `reviewer` 检查副作用和缺失覆盖。
7. 运行 `make check`。
8. `reporter` 总结根因、改动和验证结果。

## 禁止

- 无关重构。
- 跳过测试。
- 只改表象但不补回归测试。
