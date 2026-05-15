# Docs Update 工作流

## 适用场景

更新产品、领域、架构、运维或 Harness 文档。

## 流程

1. `planner` 判断更新应属于 `.harness/` 还是 `docs/`。
2. 读取 `.harness/rules/doc-boundary-rules.md`。
3. 只更新相关文档区域。
4. 检查 `AGENTS.md` 中的引用是否仍指向有效文件。
5. 可用时运行轻量验证，例如链接或路径检查。
6. `reporter` 总结修改的文档。

## 边界

- `.harness/` 描述 AI 怎么工作。
- `docs/` 描述项目是什么以及系统如何运转。
