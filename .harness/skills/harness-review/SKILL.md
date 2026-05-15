---
name: harness-review
description: 审查项目是否具备完整 Harness 工程结构时使用。
---

# Harness Review Skill

## 检查项

1. 存在 `AGENTS.md`。
2. 存在 `.harness/agents/`。
3. 存在 `.harness/workflows/`。
4. 存在 `.harness/skills/`。
5. 存在 `.harness/rules/`。
6. 存在 `docs/product/` 和 `docs/architecture/`。
7. 存在 `make check`。
8. 存在 lint、typecheck 和 test 命令。
9. 存在任务状态文件。
10. 存在文档边界规则。

## 输出格式

```text
Harness 成熟度：L1 / L2 / L3

缺失项：
- ...

优先补齐：
- ...

建议：
- ...
```
