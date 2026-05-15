---
name: docs-sync
description: 代码变更需要同步产品、领域、架构或运维文档时使用。
---

# Docs Sync Skill

## 使用场景

- 行为发生变化。
- 业务规则发生变化。
- API、数据库或架构发生变化。
- 部署或运维行为发生变化。

## 工作流程

1. 读取 `.harness/rules/doc-boundary-rules.md`。
2. 判断更新应属于 `.harness/` 还是 `docs/`。
3. 只更新相关文档。
4. 保持 `AGENTS.md` 作为路由地图。
5. 验证被引用文件仍然存在。

## 输出格式

```text
修改文档：
- ...

原因：
- ...

边界检查：
- ...
```
