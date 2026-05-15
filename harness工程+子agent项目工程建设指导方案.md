OpenAI 关于 Harness Engineering 的文章也强调，`AGENTS.md` 不应当是百科全书，而应该是一个入口地图，指向更深层的事实来源；仓库知识库应放在结构化 `docs/` 中，`AGENTS.md` 保持短小。 Codex 官方也说明，Codex 会在执行任务前读取 `AGENTS.md`，它适合放项目级指导和一致性约束。

------

# 一、推荐目录结构

我建议你这样划分：

```
project/
├── AGENTS.md                         # Codex 总入口，只放 AI 工作规则和文档路由
├── README.md                         # 人类开发者入口
├── Makefile                          # 统一验证入口
│
├── .harness/                         # Harness 工程文件，只服务 AI 工程协作
│   ├── agents/                       # 子 Agent 角色协议
│   │   ├── planner.md
│   │   ├── code_mapper.md
│   │   ├── backend_engineer.md
│   │   ├── frontend_engineer.md
│   │   ├── test_writer.md
│   │   ├── reviewer.md
│   │   ├── security_reviewer.md
│   │   └── reporter.md
│   │
│   ├── skills/                       # Skills 管理
│   │   ├── bugfix/
│   │   │   └── SKILL.md
│   │   ├── fastapi-api/
│   │   │   └── SKILL.md
│   │   ├── react-page/
│   │   │   └── SKILL.md
│   │   ├── test-writing/
│   │   │   └── SKILL.md
│   │   ├── rag-pipeline/
│   │   │   └── SKILL.md
│   │   └── docs-sync/
│   │       └── SKILL.md
│   │
│   ├── workflows/                    # 标准工作流
│   │   ├── bugfix.md
│   │   ├── feature.md
│   │   ├── refactor.md
│   │   ├── security-fix.md
│   │   └── docs-update.md
│   │
│   ├── rules/                        # AI 工作规则，不放业务需求
│   │   ├── coding-rules.md
│   │   ├── review-rules.md
│   │   ├── testing-rules.md
│   │   ├── security-rules.md
│   │   └── doc-sync-rules.md
│   │
│   ├── state/                        # Agent 工作状态
│   │   ├── feature_list.json
│   │   ├── progress.md
│   │   └── handoff.md
│   │
│   └── scripts/                      # 可执行 Harness
│       ├── check.sh
│       ├── agent-precheck.sh
│       ├── agent-done-check.sh
│       └── security-check.sh
│
├── docs/                             # 项目文档，不直接等同于 Harness
│   ├── product/                      # 项目需求文档
│   │   ├── prd.md
│   │   ├── user-stories.md
│   │   ├── acceptance-criteria.md
│   │   └── roadmap.md
│   │
│   ├── domain/                       # 业务领域知识
│   │   ├── glossary.md
│   │   ├── business-rules.md
│   │   ├── state-machines.md
│   │   └── permission-model.md
│   │
│   ├── architecture/                 # 技术设计文档
│   │   ├── overview.md
│   │   ├── module-boundaries.md
│   │   ├── database.md
│   │   ├── api-conventions.md
│   │   └── integration.md
│   │
│   ├── operations/                   # 运维/排障/发布
│   │   ├── runbook.md
│   │   ├── deploy.md
│   │   └── rollback.md
│   │
│   └── decisions/                    # ADR 架构决策记录
│       ├── ADR-0001-use-fastapi.md
│       └── ADR-0002-use-mysql.md
│
├── src/
├── tests/
└── scripts/                          # 项目自身脚本，不是 Agent Harness 专用
```

这样区分后，你的项目会很清楚：

```
.harness/ = AI 如何参与工程
docs/     = 项目本身是什么
src/      = 项目代码
tests/    = 项目验证
```

------

# 二、两类文件的边界

可以用这个表判断文件放哪里：

| 类型           | 放哪里                           | 给谁看           | 内容是什么                                |
| -------------- | -------------------------------- | ---------------- | ----------------------------------------- |
| Codex 工作规则 | `.harness/rules/` 或 `AGENTS.md` | Codex / 子 Agent | AI 怎么分析、怎么改、怎么验证             |
| 子 Agent 角色  | `.harness/agents/`               | Codex            | planner、code_mapper、reviewer 等角色协议 |
| Skills         | `.harness/skills/`               | Codex            | 可复用工作方法，如 bugfix、test-writing   |
| Agent 工作流   | `.harness/workflows/`            | Codex            | bugfix、feature、refactor 的固定流程      |
| Agent 状态     | `.harness/state/`                | Codex / 人       | 当前任务、进度、交接                      |
| PRD            | `docs/product/`                  | 产品/研发/AI     | 业务要做什么                              |
| 业务规则       | `docs/domain/`                   | 产品/研发/AI     | 订单规则、权限规则、状态机                |
| 架构设计       | `docs/architecture/`             | 研发/AI          | 模块边界、API、DB、调用关系               |
| 运维文档       | `docs/operations/`               | 研发/运维/AI     | 启动、部署、回滚、排障                    |
| 决策记录       | `docs/decisions/`                | 团队/AI          | 为什么这么选型                            |

简单判断：

```
如果这个文件是在约束 Codex 怎么工作 → 放 .harness/
如果这个文件是在描述项目要做什么/系统怎么设计 → 放 docs/
如果这个文件是人类项目说明入口 → README.md
如果这个文件是 Codex 入口 → AGENTS.md
```

------

# 三、AGENTS.md 应该怎么连接这两类文档

`AGENTS.md` 只做入口，不放大量需求。

推荐写法：

```
# AGENTS.md

## 项目说明

本项目使用 Codex 进行辅助开发。  
Codex 必须优先遵守 `.harness/` 下的工作规则，并按需读取 `docs/` 下的项目事实文档。

## 文件分区

- `.harness/`：AI 工程协作文件，包括子 Agent、Skills、工作流、规则、状态。
- `docs/`：项目需求、业务规则、架构设计、运维说明。
- `src/`：业务代码。
- `tests/`：测试代码。

## 必读 Harness 文件

- 子 Agent 角色：`.harness/agents/`
- 工作流：`.harness/workflows/`
- AI 工作规则：`.harness/rules/`
- 当前任务状态：`.harness/state/progress.md`

## 项目文档路由

- 产品需求：`docs/product/prd.md`
- 用户故事：`docs/product/user-stories.md`
- 验收标准：`docs/product/acceptance-criteria.md`
- 业务术语：`docs/domain/glossary.md`
- 业务规则：`docs/domain/business-rules.md`
- 状态机：`docs/domain/state-machines.md`
- 权限模型：`docs/domain/permission-model.md`
- 架构概览：`docs/architecture/overview.md`
- 模块边界：`docs/architecture/module-boundaries.md`
- API 规范：`docs/architecture/api-conventions.md`
- 数据库设计：`docs/architecture/database.md`

## 工作原则

1. 修改代码前，先判断任务类型并读取对应 Harness 工作流。
2. 涉及业务行为时，必须读取 `docs/product/` 和 `docs/domain/`。
3. 涉及架构/API/数据库时，必须读取 `docs/architecture/`。
4. 不允许把产品需求写进 `.harness/`。
5. 不允许把 Codex 工作规则写进 `docs/product/`。
6. 任务完成前必须运行 `make check`。

## 常用命令

- `make lint`
- `make typecheck`
- `make test`
- `make check`
```

这样 Codex 一进来就知道：

```
.harness 是工作方式
docs 是项目事实
```

------

# 四、Harness 文件应该放什么

## 1. `.harness/agents/`

放角色，不放业务需求。

例如 `.harness/agents/code_mapper.md`：

```
# code_mapper

## 角色

负责修改前分析代码路径、调用链、影响范围和风险点。

## 输入

- 用户任务
- AGENTS.md
- 相关 docs
- 当前代码结构

## 输出

```text
相关文件：
- ...

调用链：
- ...

影响范围：
- ...

风险点：
- ...

建议修改点：
- ...
```

## 限制

- 不写代码
- 不做重构
- 不修改文件

```
## 2. `.harness/workflows/`

放流程。

例如 `.harness/workflows/bugfix.md`：

```markdown
# Bugfix Workflow

## 适用场景

修复明确 bug。

## 流程

1. code_mapper 定位相关代码。
2. 复现或推断问题原因。
3. engineer 做最小修复。
4. test_writer 补回归测试。
5. reviewer 审查是否有副作用。
6. verifier 运行 make check。
7. reporter 输出根因、修改、验证结果。

## 禁止

- 不做无关重构
- 不跳过测试
- 不只改表象不补测试
```

## 3. `.harness/skills/`

放可复用能力。

例如 `.harness/skills/test-writing/SKILL.md`：

```
---
name: test-writing
description: 为业务代码补充单元测试、回归测试和接口测试
---

# Test Writing Skill

## 使用场景

- bugfix 后补回归测试
- 新功能后补测试
- coverage 不达标
- 修改 service / API 后验证行为

## 工作步骤

1. 找到被修改文件。
2. 找到对应测试目录。
3. 补成功路径。
4. 补失败路径。
5. 补边界条件。
6. 运行测试。
7. 如果失败，继续修复。

## 验证命令

```bash
make test
make check
Codex 的 Skills 是面向任务的能力包；官方文档说明，Skills 会把任务专用的说明、资源和可选脚本打包给 Codex 使用，适合沉淀固定流程。:contentReference[oaicite:2]{index=2}

## 4. `.harness/rules/`

放 AI 工作规则。

例如 `.harness/rules/testing-rules.md`：

```markdown
# Testing Rules

## 强制要求

1. bugfix 必须补回归测试。
2. 新增 service 必须有 unit test。
3. 新增 API 必须有接口测试。
4. 修改权限逻辑必须有越权测试。
5. 测试失败不允许标记任务完成。

## 验证命令

```bash
make test
make coverage
## 5. `.harness/state/`

放任务状态。

例如 `.harness/state/feature_list.json`：

```json
[
  {
    "id": "F001",
    "title": "修复用户创建接口邮箱重复错误码",
    "type": "bugfix",
    "status": "active",
    "workflow": ".harness/workflows/bugfix.md",
    "agents": [
      "code_mapper",
      "backend_engineer",
      "test_writer",
      "reviewer"
    ],
    "related_docs": [
      "docs/architecture/api-conventions.md",
      "docs/domain/business-rules.md"
    ],
    "verification": [
      "make check"
    ],
    "evidence": ""
  }
]
```

------

# 五、项目需求文档应该放什么

需求文档不要写 Codex 工作细节。它只描述项目事实。

## 1. `docs/product/prd.md`

```
# PRD

## 背景

为什么做这个功能。

## 目标

这个功能要解决什么问题。

## 用户角色

- 普通用户
- 管理员
- 运营人员

## 功能范围

### 包含

- ...

### 不包含

- ...

## 验收标准

- ...
```

## 2. `docs/product/user-stories.md`

```
# User Stories

## US-001 用户创建账号

作为一个新用户，  
我希望可以通过邮箱注册账号，  
以便后续登录系统。

### 验收标准

- 邮箱格式错误时提示错误
- 邮箱重复时返回明确错误码
- 注册成功后返回用户 ID
```

## 3. `docs/domain/business-rules.md`

```
# Business Rules

## 用户注册

- 邮箱必须唯一。
- 密码必须符合安全策略。
- 禁止使用已封禁邮箱域名。
```

## 4. `docs/domain/state-machines.md`

```
# State Machines

## Order Lifecycle

pending -> paid -> shipped -> completed
pending -> cancelled

禁止：
- completed -> cancelled
- refunded -> shipped
```

## 5. `docs/architecture/api-conventions.md`

```
# API Conventions

## Error Response

```json
{
  "code": "USER_EMAIL_EXISTS",
  "message": "Email already exists",
  "request_id": "..."
}
```

## 幂等规则

- 创建订单接口必须支持 idempotency key。

```
---

# 六、如何防止两类文档混乱

建议加一个文档边界规则：`.harness/rules/doc-boundary-rules.md`

```markdown
# Document Boundary Rules

## .harness/ 只允许放

- Agent 角色协议
- Codex 工作流
- AI 使用规则
- Skills
- 任务状态
- 验证脚本说明

## docs/ 只允许放

- 产品需求
- 用户故事
- 业务规则
- 架构设计
- API 规范
- 数据库设计
- 运维说明
- ADR

## 禁止

1. 不要在 PRD 中写 Codex 工作流程。
2. 不要在 Skill 中写具体业务需求。
3. 不要在 AGENTS.md 中堆完整需求。
4. 不要在 `.harness/agents/` 中写项目业务规则。
5. 不要在 `docs/product/` 中写 AI 角色分工。

## 修改要求

- 如果修改了业务行为，更新 `docs/product/` 或 `docs/domain/`。
- 如果修改了 AI 工作方式，更新 `.harness/`。
- 如果修改了技术设计，更新 `docs/architecture/`。
```

然后在 `AGENTS.md` 中引用它：

```
文档边界规则：`.harness/rules/doc-boundary-rules.md`
```

------

# 七、Codex 实际使用 Prompt

以后你可以这样使用 Codex：

```
请按项目 Harness 工作流处理这个任务：

任务：
修复用户创建接口邮箱重复时没有返回明确错误码的问题。

要求：
1. 先读取 AGENTS.md；
2. 区分 Harness 文件和项目文档：
   - 工作流程读取 .harness/workflows/bugfix.md；
   - 角色协议读取 .harness/agents/code_mapper.md、backend_engineer.md、test_writer.md、reviewer.md；
   - 业务/API 事实读取 docs/product/ 和 docs/architecture/api-conventions.md；
3. 不要把业务需求写进 .harness/；
4. 不要把 AI 工作规则写进 docs/product/；
5. 做最小必要修改；
6. 补回归测试；
7. 运行 make check；
8. 最终说明：
   - 修改了哪些代码；
   - 是否更新了项目文档；
   - 是否更新了 Harness 文件；
   - 验证结果。
```

------

# 八、什么时候更新 Harness，什么时候更新需求文档

用这个判断：

| 场景                    | 更新哪里                                       |
| ----------------------- | ---------------------------------------------- |
| 新增业务功能            | `docs/product/`、`docs/domain/`                |
| 修改业务规则            | `docs/domain/business-rules.md`                |
| 修改状态流转            | `docs/domain/state-machines.md`                |
| 修改 API 规范           | `docs/architecture/api-conventions.md`         |
| 修改数据库设计          | `docs/architecture/database.md`                |
| 新增 Codex 工作流程     | `.harness/workflows/`                          |
| 新增子 Agent 角色       | `.harness/agents/`                             |
| 新增常用任务 Skill      | `.harness/skills/`                             |
| 新增 AI 约束规则        | `.harness/rules/`                              |
| 记录当前 Agent 任务状态 | `.harness/state/`                              |
| CI/验证命令变化         | `Makefile` + `.harness/rules/testing-rules.md` |
| 部署/回滚变化           | `docs/operations/`                             |

一句话：

```
项目发生业务或架构变化 → 更新 docs/
AI 协作方式发生变化 → 更新 .harness/
```

------

# 九、最终推荐命名

你可以把这套规范命名成：

```
Agent-Native Project Structure
```

或者中文叫：

```
面向 Agent 的项目工程结构
```

它的核心边界是：

```
.harness/：AI 工程协作层
docs/：项目事实文档层
src/：代码实现层
tests/：验证层
```

最终总结：

> `.harness/` 管“AI 怎么干活”，`docs/` 管“项目是什么和要做什么”。
>  `AGENTS.md` 是入口地图，不是需求文档，也不是规则百科。
>  Codex 每次任务先读 `AGENTS.md`，再按任务类型读取 `.harness/` 的工作流和 `docs/` 的项目事实，最后通过 `make check` 做硬验证。