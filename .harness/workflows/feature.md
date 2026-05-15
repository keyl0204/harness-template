# Feature 工作流

## 适用场景

新增用户可感知行为或项目能力。

## 流程

1. `planner` 明确范围、非目标和验收标准。
2. 读取相关产品、领域和架构文档。
3. `code_mapper` 识别实现路径和边界。
4. Engineer 实现最小但完整的功能切片。
5. `test_writer` 覆盖成功路径、失败路径和重要边界条件。
6. `reviewer` 检查范围、边界和文档更新。
7. 运行 `make check`。
8. `reporter` 总结行为、修改文件和验证结果。

## 文档要求

- 产品行为变化时更新 `docs/product/`。
- 业务规则变化时更新 `docs/domain/`。
- 系统设计变化时更新 `docs/architecture/`。
