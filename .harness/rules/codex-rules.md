# Codex 规则

## 适用范围

本文件约束 Codex 在项目内的协作方式、上下文读取顺序、任务拆解、子 Agent 使用和交付标准。
业务事实写入 `docs/`，AI 协作规则写入 `.harness/`。

## 启动流程

1. 先读取 `AGENTS.md`，确认项目类型、文件路由和完成标准。
2. 判断任务类型：`feature`、`bugfix`、`refactor`、`security-fix`、`docs-update` 或 `ops`。
3. 读取匹配的 `.harness/workflows/` 文件，按工作流组织步骤。
4. 按影响面读取最小必要文档：
   - 业务行为：`docs/product/`、`docs/domain/`
   - API、模块、数据库：`docs/architecture/`
   - 部署、配置、回滚：`docs/operations/`
5. 修改前检查 `git status --short`，识别已有用户改动。

## 子 Agent 使用

1. 只有任务能被清晰拆分时才使用子 Agent。
2. 子 Agent 的角色、模型和推理强度以 `.harness/agents/*.md` 的元数据为准。
3. `planner` 用于拆解需求和验收标准，不直接改代码。
4. `code_mapper` 用于定位代码路径、调用链和风险，不直接改代码。
5. `backend_engineer`、`frontend_engineer`、`test_writer` 可执行文件修改。
6. `reviewer`、`security_reviewer` 必须保持审查视角，先列问题再给建议。
7. `reporter` 只在实现和验证完成后汇总事实，不补写未执行的验证结论。

## Skills 使用

1. Skills 位于 `.harness/skills/*/SKILL.md`，用于提供可复用的专业执行方法。
2. 选择 skill 时先看 frontmatter 的 `description`，再读取对应 `SKILL.md` 正文。
3. bugfix 任务优先读取 `bugfix` 和 `test-writing`。
4. FastAPI/API 任务优先读取 `fastapi-api`。
5. React/UI 任务优先读取 `react-page`。
6. RAG 任务优先读取 `rag-pipeline`。
7. workflow 编排任务优先读取 `workflow-orchestration`。
8. multi-agent 任务优先读取 `multi-agent-system`。
9. 安全、权限、密钥、文件、网络、shell 或高风险操作优先读取 `security-review`。
10. 文档同步任务优先读取 `docs-sync`。
11. Harness 结构审查或模板升级优先读取 `harness-review`。
12. Skill 只能指导执行方法，不能覆盖用户需求、项目文档或更具体的规则。

## 工作中

1. 保持改动小而可审查，优先修改与任务直接相关的文件。
2. 不回退用户已有改动；遇到冲突时先理解并兼容。
3. 不把临时调试、实验脚本或生成产物混入最终提交，除非它们是交付物。
4. 不新增依赖，除非现有代码和标准库无法合理完成目标。
5. 不扩大公开 API、配置项、数据库 schema 或权限模型，除非任务明确需要。
6. 修改行为、规则或架构时，同步更新对应文档。
7. 对不确定的外部事实、库版本或安全要求，必须查证后再落地。

## 完成前

1. 运行与改动范围匹配的最小验证。
2. 可行时运行 `make check`。
3. 若验证失败，先修复再交付；不能修复时说明失败命令、失败原因和剩余风险。
4. 最终回复必须包含：关键改动、验证结果、未解决风险。
