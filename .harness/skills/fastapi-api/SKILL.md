---
name: fastapi-api
description: 新增或修改 FastAPI router、service、schema 或 repository 时使用。
---

# FastAPI API Skill

## 使用场景

- 新增 API endpoint。
- 修改请求或响应 schema。
- 新增 service 行为。
- 调整校验、错误或 repository 访问。

## 工作流程

1. 读取 `docs/architecture/api-conventions.md`。
2. 找到相关 router、schema、service 和 repository。
3. 检查是否已有相似接口。
4. 实现最小必要修改。
5. 按需补 route 和 service 测试。
6. 运行验证。

## 约束

- 不要把复杂业务逻辑写进 router。
- 存在 service 层时不要绕过 service。
- 不要返回未记录的响应结构。
- 错误码必须稳定并有文档记录。

## 验证命令

```bash
make lint
make test
make check
```
