# Bugfix 工作流

## 适用场景

修复已确认或高度疑似的缺陷。

## 流程

1. `planner` 确认范围和验收标准。
2. `code_mapper` 定位相关文件和影响范围。
3. Engineer 做最小修复。
4. `test_writer` 补回归测试。
5. `reviewer` 检查副作用和缺失覆盖。
6. 运行 `make check`。
7. `reporter` 总结根因、改动和验证结果。

## 禁止

- 无关重构。
- 跳过测试。
- 只改表象但不补回归测试。
