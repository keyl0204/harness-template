---
name: fastapi-api
description: 新增或修改 FastAPI 路由、请求/响应 schema、service 逻辑、依赖注入、校验、错误处理、repository 或 API 测试时使用。该 Skill 保持 API 行为稳定、文档同步、权限可检查且易于测试。
---

# FastAPI API Skill

## 适用场景

- 新增、修改或删除 FastAPI endpoint。
- 修改请求参数、响应 schema、状态码、错误格式或 OpenAPI 行为。
- 新增 service、repository、dependency、middleware 或 background task。
- 调整权限、校验、分页、过滤、排序或外部系统调用。
- 为 API 行为补充路由测试、service 测试或契约测试。

## 必须读取

1. `AGENTS.md`
2. `.harness/rules/coding-rules.md`
3. `.harness/rules/testing-rules.md`
4. 涉及安全时读取 `.harness/rules/security-rules.md`
5. `docs/architecture/overview.md`
6. `docs/architecture/api-conventions.md`
7. 涉及数据库时读取 `docs/architecture/database.md`
8. 涉及权限时读取 `docs/domain/permission-model.md`

## 设计边界

- Router：请求解析、依赖注入、权限入口、调用 service、响应转换。
- Schema：输入输出结构、字段校验、兼容默认值和示例。
- Service/domain：业务规则、状态变化、错误映射和事务边界。
- Repository/infra：数据库、缓存、第三方 API、文件和网络 I/O。
- Tests：覆盖 API 契约、成功路径、失败路径、权限和边界条件。

## 工作流程

1. 找到相似 API，沿用本项目的路由、schema、service 和测试风格。
2. 明确 API 契约：method、path、request、response、status code、error code。
3. 检查权限和数据范围：actor、resource、action、condition。
4. 实现最小必要修改，保持公开契约兼容；破坏性变更必须更新文档。
5. 对外部 I/O 增加超时、错误映射和可测试边界。
6. 补测试：route 测试覆盖 HTTP 契约，service 测试覆盖业务行为。
7. 运行聚焦测试和必要的 lint/typecheck。

## 检查清单

- Router 中没有复杂业务逻辑。
- Service 不直接依赖 HTTP request，除非项目已有明确约定。
- 错误响应稳定，不泄露内部异常。
- 分页、过滤、排序结果稳定。
- 数据写入考虑幂等、并发、事务和回滚。
- API 文档和测试与实现一致。

## 验证命令

```bash
make lint
make test
make check
```

可聚焦运行：

```bash
uv run pytest tests/path_to_api_test.py -q
```

## 输出格式

```text
API 变化：
- ...

修改文件：
- ...

权限和数据范围：
- ...

测试覆盖：
- ...

验证命令：
- ...

剩余风险：
- ...
```
