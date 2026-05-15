# Copier 化落地方案：一行命令生成 Harness + 子 Agent + Skills + Codex 工程骨架

> 目标：把常用的 Harness 工程文件、子 Agent 角色协议、Skills、项目文档分层、验证命令和 Codex 工作流沉淀为一个 Copier 模板。后续新建项目时，通过一行命令生成标准工程骨架；旧项目也可以通过 `copier update` 跟随模板升级。

---

## 目录

1. 方案目标
2. 为什么选择 Copier
3. 最终使用效果
4. 本地环境准备
5. 创建模板仓库
6. 模板仓库目录设计
7. 编写 `copier.yml`
8. 编写核心模板文件
9. 编写 `.harness` 工程文件
10. 编写 Skills
11. 编写项目需求与架构文档模板
12. 生成项目并验证
13. 发布模板仓库
14. 旧项目如何跟随模板升级
15. 封装为 `harness-init` 一行命令
16. 给已有项目补 Harness 的 adopt 模式
17. 模板版本管理规范
18. 推荐落地节奏
19. Codex 日常使用 Prompt
20. 常见问题与避坑
21. 最终交付清单
22. 参考资料

---

## 1. 方案目标

你希望每次新建项目时，不再重复让 Codex 手动生成以下内容：

```text
AGENTS.md
.harness/agents/
.harness/skills/
.harness/workflows/
.harness/rules/
.harness/state/
docs/product/
docs/domain/
docs/architecture/
docs/operations/
Makefile
scripts/check.sh
```

因此我们要做一个 **Copier 模板仓库**，让新项目通过命令生成：

```bash
mkdir my-project
cd my-project
copier copy https://github.com/keyl0204/harness-template.git .
```

或者后续封装成自己的 CLI：

```bash
harness-init new my-project --type fastapi-react --pm uv --frontend-pm pnpm
```

生成后的项目天然支持：

```text
1. Codex 读取 AGENTS.md 后知道如何工作；
2. .harness/ 管 AI 工程协作文件；
3. docs/ 管项目需求、业务规则、架构事实；
4. .harness/agents/ 管子 Agent 角色协议；
5. .harness/skills/ 管可复用工作能力；
6. .harness/workflows/ 管标准任务流程；
7. Makefile / scripts/ 管可执行验证门禁；
8. 旧项目可通过 copier update 跟随模板升级。
```

---

## 2. 为什么选择 Copier

Copier 适合这个场景的原因：

```text
1. 支持模板变量和条件渲染；
2. 支持交互式提问；
3. 支持非交互式参数传入；
4. 支持 Git 模板仓库；
5. 支持模板版本更新；
6. 旧项目可以通过 copier update 同步模板变化；
7. 适合长期维护“组织级工程模板”。
```

和 Cookiecutter 相比，Copier 对你这个场景最大的价值是：

> Harness 模板后续一定会演进。你会不断增加新的子 Agent、Skills、规则、CI 门禁和文档规范。Copier 的 update 机制能让旧项目跟随模板升级，而不是每个项目手动复制。

---

## 3. 最终使用效果

### 3.1 新建项目

```bash
mkdir my-project
cd my-project
copier copy https://github.com/keyl0204/harness-template.git . \
  -d project_name="my-project" \
  -d project_type="fastapi-react" \
  -d package_manager="uv" \
  -d frontend_package_manager="pnpm"
```

生成：

```text
my-project/
├── AGENTS.md
├── README.md
├── Makefile
├── pyproject.toml
├── .harness/
├── docs/
├── src/
└── tests/
```

### 3.2 进入项目使用 Codex

```bash
cd my-project
codex
```

给 Codex 的第一条指令：

```text
请读取 AGENTS.md，并按 Harness + 子 Agent + Skills 工作流处理后续任务。
```

### 3.3 后续升级模板

模板仓库升级后，在旧项目执行：

```bash
copier check-update
copier update
```

---

## 4. 本地环境准备

### 4.1 安装 uv

如果你已经安装 uv，可以跳过。

```bash
uv --version
```

### 4.2 安装 Copier

推荐用 uv 安装为全局工具：

```bash
uv tool install copier
```

如果安装后命令不可用：

```bash
uv tool update-shell
```

然后重开终端。

检查：

```bash
copier --version
```

### 4.3 Git 要求

建议模板仓库和生成出来的项目都使用 Git：

```bash
git --version
```

原因：

```text
1. Copier update 对 Git 项目更稳；
2. 模板最好打 tag 管理版本；
3. update 后如果有冲突，可以按 Git 冲突流程处理；
4. 旧项目更新前可以先开分支，降低风险。
```

---

## 5. 创建模板仓库

```bash
mkdir harness-template
cd harness-template
git init
```

推荐远程仓库命名：

```text
harness-template
agent-native-template
codex-harness-template
```

初始化基础文件：

```bash
touch copier.yml
touch README.md.jinja
touch AGENTS.md.jinja
touch Makefile.jinja
touch pyproject.toml.jinja
touch package.json.jinja
touch .gitignore.jinja
```

---

## 6. 模板仓库目录设计

完整模板目录：

```text
harness-template/
├── copier.yml
├── README.md.jinja
├── AGENTS.md.jinja
├── Makefile.jinja
├── pyproject.toml.jinja
├── package.json.jinja
├── .gitignore.jinja
│
├── .harness/
│   ├── agents/
│   │   ├── planner.md
│   │   ├── code_mapper.md
│   │   ├── backend_engineer.md
│   │   ├── frontend_engineer.md
│   │   ├── test_writer.md
│   │   ├── reviewer.md
│   │   ├── security_reviewer.md
│   │   └── reporter.md
│   │
│   ├── workflows/
│   │   ├── bugfix.md
│   │   ├── feature.md
│   │   ├── refactor.md
│   │   ├── security-fix.md
│   │   └── docs-update.md
│   │
│   ├── rules/
│   │   ├── coding-rules.md
│   │   ├── testing-rules.md
│   │   ├── security-rules.md
│   │   ├── doc-boundary-rules.md
│   │   └── codex-rules.md
│   │
│   ├── skills/
│   │   ├── bugfix/
│   │   │   └── SKILL.md
│   │   ├── test-writing/
│   │   │   └── SKILL.md
│   │   ├── fastapi-api/
│   │   │   └── SKILL.md
│   │   ├── react-page/
│   │   │   └── SKILL.md
│   │   ├── docs-sync/
│   │   │   └── SKILL.md
│   │   ├── security-review/
│   │   │   └── SKILL.md
│   │   └── harness-review/
│   │       └── SKILL.md
│   │
│   ├── state/
│   │   ├── feature_list.json.jinja
│   │   ├── progress.md
│   │   └── handoff.md
│   │
│   └── scripts/
│       ├── check.sh.jinja
│       ├── agent-precheck.sh
│       └── agent-done-check.sh
│
├── docs/
│   ├── product/
│   │   ├── prd.md
│   │   ├── user-stories.md
│   │   ├── acceptance-criteria.md
│   │   └── roadmap.md
│   ├── domain/
│   │   ├── glossary.md
│   │   ├── business-rules.md
│   │   ├── state-machines.md
│   │   └── permission-model.md
│   ├── architecture/
│   │   ├── overview.md
│   │   ├── module-boundaries.md
│   │   ├── api-conventions.md
│   │   ├── database.md
│   │   └── integration.md
│   ├── operations/
│   │   ├── runbook.md
│   │   ├── deploy.md
│   │   └── rollback.md
│   └── decisions/
│       └── ADR-0001-template.md
│
├── src/
│   └── .gitkeep
└── tests/
    └── .gitkeep
```

核心边界：

```text
.harness/ = AI 如何参与工程
docs/     = 项目需求、业务规则、架构事实
src/      = 项目代码
tests/    = 验证代码
```

---

## 7. 编写 `copier.yml`

`copier.yml` 是模板配置入口。

```yaml
_min_copier_version: "9.0.0"

_envops:
  trim_blocks: true
  lstrip_blocks: true
  keep_trailing_newline: true

project_name:
  type: str
  help: 项目名称，例如 ai-article、water-delivery
  default: my-project

project_slug:
  type: str
  help: 项目目录名
  default: "{{ project_name|lower|replace(' ', '-')|replace('_', '-') }}"

project_description:
  type: str
  help: 项目描述
  default: "A project with Harness + Subagents + Skills scaffold."

project_type:
  type: str
  help: 项目类型
  choices:
    - python
    - fastapi
    - fastapi-react
    - react
    - rag
    - langgraph
  default: fastapi-react

package_manager:
  type: str
  help: Python 包管理器
  choices:
    - uv
    - pip
    - poetry
    - none
  default: uv

frontend_package_manager:
  type: str
  help: 前端包管理器
  choices:
    - pnpm
    - npm
    - yarn
    - none
  default: pnpm

use_subagents:
  type: bool
  help: 是否生成子 Agent 角色协议
  default: true

use_skills:
  type: bool
  help: 是否生成 Skills 管理目录
  default: true

use_security_rules:
  type: bool
  help: 是否生成安全规则和安全审查 Agent
  default: true

use_ci:
  type: bool
  help: 是否生成 GitHub Actions CI
  default: false

use_docker:
  type: bool
  help: 是否生成 Dockerfile 和 docker-compose 示例
  default: false

harness_level:
  type: str
  help: Harness 成熟度等级
  choices:
    - L1
    - L2
    - L3
  default: L2

author_name:
  type: str
  help: 作者名称
  default: kyle

python_version:
  type: str
  help: Python 版本
  default: "3.12"

node_version:
  type: str
  help: Node.js 版本
  default: "22"

_exclude:
  - ".git"
  - "__pycache__"
  - "*.pyc"
  - ".DS_Store"
```

### 参数说明

| 参数 | 说明 |
|---|---|
| `project_name` | 项目名称 |
| `project_slug` | 项目目录名 |
| `project_type` | 项目类型 |
| `package_manager` | Python 包管理器 |
| `frontend_package_manager` | 前端包管理器 |
| `use_subagents` | 是否生成子 Agent 角色协议 |
| `use_skills` | 是否生成 Skills |
| `use_security_rules` | 是否生成安全规则 |
| `use_ci` | 是否生成 CI |
| `harness_level` | Harness 成熟度等级 |
| `python_version` | Python 版本 |
| `node_version` | Node.js 版本 |

---

## 8. 编写核心模板文件

### 8.1 `AGENTS.md.jinja`

```markdown
# AGENTS.md

## 项目说明

项目名称：{{ project_name }}

项目类型：{{ project_type }}

项目描述：{{ project_description }}

本项目使用 Codex 进行辅助开发。Codex 必须优先遵守 `.harness/` 下的工作规则，并按需读取 `docs/` 下的项目事实文档。

## 文件分区

- `.harness/`：AI 工程协作文件，包括子 Agent、Skills、工作流、规则、状态。
- `docs/`：项目需求、业务规则、架构设计、运维说明。
- `src/`：业务代码。
- `tests/`：测试代码。

## Harness 文件路由

{% if use_subagents %}
- 子 Agent 角色：`.harness/agents/`
{% endif %}
{% if use_skills %}
- Skills：`.harness/skills/`
{% endif %}
- 工作流：`.harness/workflows/`
- AI 工作规则：`.harness/rules/`
- 当前任务状态：`.harness/state/progress.md`
- 任务列表：`.harness/state/feature_list.json`

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
- 运维手册：`docs/operations/runbook.md`

## 工作原则

1. 修改代码前，先判断任务类型并读取对应 Harness 工作流。
2. 涉及业务行为时，必须读取 `docs/product/` 和 `docs/domain/`。
3. 涉及架构、API、数据库时，必须读取 `docs/architecture/`。
4. 不允许把产品需求写进 `.harness/`。
5. 不允许把 Codex 工作规则写进 `docs/product/`。
6. 不做无关重构。
7. 不新增不必要依赖。
8. 任务完成前必须运行验证命令。
9. 测试失败时必须继续修复，不能直接宣称完成。

## 常用命令

{% if project_type in ["python", "fastapi", "fastapi-react", "rag", "langgraph"] %}
- Python 代码检查：`make lint`
- Python 类型检查：`make typecheck`
- Python 测试：`make test`
{% endif %}
{% if project_type in ["react", "fastapi-react"] %}
- 前端检查：`make frontend-check`
{% endif %}
- 完整验证：`make check`

## 完成标准

完成前必须执行：

```bash
make check
```

如果失败，必须根据错误继续修复。
```

### 8.2 `README.md.jinja`

```markdown
# {{ project_name }}

{{ project_description }}

## Project Type

`{{ project_type }}`

## Quick Start

```bash
make setup
make dev
```

## Harness

本项目内置 Harness + 子 Agent + Skills 工程结构：

- `AGENTS.md`：Codex 入口
- `.harness/agents/`：子 Agent 角色协议
- `.harness/skills/`：Codex Skills
- `.harness/workflows/`：标准工作流
- `.harness/rules/`：AI 工作规则
- `.harness/state/`：任务状态
- `docs/`：项目需求、业务规则、架构设计

## Verify

```bash
make check
```
```

### 8.3 `Makefile.jinja`

```makefile
.PHONY: setup dev lint typecheck test coverage frontend-check backend-check security check

setup:
{% if package_manager == "uv" %}
	uv sync
{% elif package_manager == "pip" %}
	pip install -r requirements.txt
{% elif package_manager == "poetry" %}
	poetry install
{% else %}
	@echo "No Python package manager configured"
{% endif %}
{% if project_type in ["react", "fastapi-react"] and frontend_package_manager != "none" %}
	cd frontend && {{ frontend_package_manager }} install
{% endif %}

dev:
{% if project_type in ["fastapi", "fastapi-react", "rag", "langgraph"] %}
	uv run uvicorn src.main:app --reload
{% elif project_type == "react" %}
	cd frontend && {{ frontend_package_manager }} run dev
{% else %}
	@echo "Configure dev command"
{% endif %}

lint:
{% if package_manager == "uv" %}
	uv run ruff check .
	uv run ruff format --check .
{% elif package_manager == "poetry" %}
	poetry run ruff check .
	poetry run ruff format --check .
{% else %}
	@echo "Configure lint command"
{% endif %}

typecheck:
{% if package_manager == "uv" %}
	uv run pyright
{% elif package_manager == "poetry" %}
	poetry run pyright
{% else %}
	@echo "Configure typecheck command"
{% endif %}

test:
{% if package_manager == "uv" %}
	uv run pytest
{% elif package_manager == "poetry" %}
	poetry run pytest
{% else %}
	@echo "Configure test command"
{% endif %}

coverage:
{% if package_manager == "uv" %}
	uv run pytest --cov=src --cov-report=term-missing
{% elif package_manager == "poetry" %}
	poetry run pytest --cov=src --cov-report=term-missing
{% else %}
	@echo "Configure coverage command"
{% endif %}

security:
{% if package_manager == "uv" %}
	uv run bandit -r src || true
{% else %}
	@echo "Configure security command"
{% endif %}

frontend-check:
{% if project_type in ["react", "fastapi-react"] and frontend_package_manager != "none" %}
	cd frontend && {{ frontend_package_manager }} run lint
	cd frontend && {{ frontend_package_manager }} run typecheck
	cd frontend && {{ frontend_package_manager }} run test
	cd frontend && {{ frontend_package_manager }} run build
{% else %}
	@echo "No frontend configured"
{% endif %}

backend-check: lint typecheck test

check:
{% if project_type == "fastapi-react" %}
	$(MAKE) backend-check
	$(MAKE) frontend-check
{% elif project_type == "react" %}
	$(MAKE) frontend-check
{% elif project_type in ["python", "fastapi", "rag", "langgraph"] %}
	$(MAKE) backend-check
{% else %}
	@echo "Configure check command"
{% endif %}
```

### 8.4 `pyproject.toml.jinja`

```toml
[project]
name = "{{ project_slug }}"
version = "0.1.0"
description = "{{ project_description }}"
requires-python = ">={{ python_version }}"
dependencies = []

[dependency-groups]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=5.0.0",
    "ruff>=0.8.0",
    "pyright>=1.1.0",
    "bandit>=1.7.0",
]

[tool.ruff]
line-length = 100
target-version = "py{{ python_version|replace('.', '') }}"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B"]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]
```

### 8.5 `package.json.jinja`

```json
{
  "name": "{{ project_slug }}",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "vite",
    "lint": "eslint .",
    "typecheck": "tsc --noEmit",
    "test": "vitest run",
    "coverage": "vitest run --coverage",
    "build": "vite build",
    "check": "{{ frontend_package_manager }} run lint && {{ frontend_package_manager }} run typecheck && {{ frontend_package_manager }} run test && {{ frontend_package_manager }} run build"
  }
}
```

---

## 9. 编写 `.harness` 工程文件

### 9.1 `.harness/agents/planner.md`

```markdown
# planner

## 角色

负责把用户需求拆成可执行任务，明确范围、验收标准、风险点和应使用的工作流。

## 工作内容

1. 复述用户需求。
2. 判断任务类型：bugfix / feature / refactor / security-fix / docs-update。
3. 判断是否涉及后端、前端、数据库、权限、安全、文档。
4. 给出验收标准。
5. 判断需要使用哪些子 Agent 和 Skills。

## 输出格式

```text
任务目标：
- ...

任务类型：
- ...

影响范围：
- backend:
- frontend:
- database:
- docs:
- tests:

验收标准：
- ...

建议工作流：
- ...

建议使用的角色：
- ...

建议使用的 Skills：
- ...
```

## 限制

- 不直接修改代码。
- 不扩大任务范围。
```

### 9.2 `.harness/agents/code_mapper.md`

```markdown
# code_mapper

## 角色

负责修改前分析代码路径、调用链、影响范围和风险点。

## 输入

- 用户任务
- AGENTS.md
- 相关 docs
- 当前代码结构

## 输出格式

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

不要修改：
- ...
```

## 限制

- 不写代码。
- 不做重构。
- 不修改文件。
```

### 9.3 `.harness/agents/backend_engineer.md`

```markdown
# backend_engineer

## 角色

负责后端最小必要修改。

## 工作要求

1. 修改前读取 `docs/architecture/overview.md`。
2. 涉及 API 时读取 `docs/architecture/api-conventions.md`。
3. 涉及数据库时读取 `docs/architecture/database.md`。
4. 涉及权限时读取 `docs/domain/permission-model.md`。
5. 只做当前任务需要的最小修改。
6. 不引入不必要依赖。

## 输出

```text
修改文件：
- ...

核心改动：
- ...

为什么这样改：
- ...

需要补充的测试：
- ...
```
```

### 9.4 `.harness/agents/frontend_engineer.md`

```markdown
# frontend_engineer

## 角色

负责前端最小必要修改。

## 工作要求

1. 修改前读取 `docs/architecture/overview.md`。
2. 涉及 API 调用时读取 `docs/architecture/api-conventions.md`。
3. 只做当前任务需要的最小修改。
4. 不引入不必要依赖。
5. 不绕过现有组件结构。
6. 不直接写 inline style，除非项目明确允许。

## 输出

```text
修改文件：
- ...

核心改动：
- ...

为什么这样改：
- ...

需要补充的测试：
- ...
```
```

### 9.5 `.harness/agents/test_writer.md`

```markdown
# test_writer

## 角色

负责补充或更新测试。

## 工作要求

1. bugfix 必须补回归测试。
2. 新功能至少覆盖成功路径和失败路径。
3. 涉及权限时必须补越权测试。
4. 不写无意义覆盖率测试。
5. 测试命名要表达业务行为。

## 输出

```text
新增/修改测试：
- ...

覆盖场景：
- 成功路径：
- 失败路径：
- 边界条件：

运行命令：
- ...
```
```

### 9.6 `.harness/agents/reviewer.md`

```markdown
# reviewer

## 角色

负责审查实现是否正确、是否过度修改、是否存在回归风险。

## 审查维度

1. 是否满足需求。
2. 是否破坏架构边界。
3. 是否有无关重构。
4. 是否缺少错误处理。
5. 是否缺少测试。
6. 是否存在性能或安全风险。
7. 是否需要更新文档。

## 输出格式

```text
结论：通过 / 不通过

必须修复：
- ...

建议优化：
- ...

风险：
- ...
```
```

### 9.7 `.harness/agents/security_reviewer.md`

```markdown
# security_reviewer

## 角色

负责安全、权限、敏感操作审查。

## 审查重点

1. actor/resource/action 是否清晰。
2. 是否存在越权访问。
3. 是否有敏感数据泄露。
4. 是否有危险命令、路径穿越、SQL 注入风险。
5. 是否需要审计日志。
6. 是否需要人工确认。

## 输出格式

```text
安全结论：通过 / 不通过

风险点：
- ...

必须修复：
- ...

建议增加的测试：
- ...
```
```

### 9.8 `.harness/workflows/bugfix.md`

```markdown
# Bugfix Workflow

## 适用场景

修复明确 bug。

## 流程

1. planner 判断任务范围。
2. code_mapper 定位相关代码。
3. engineer 做最小修复。
4. test_writer 补回归测试。
5. reviewer 审查是否有副作用。
6. verifier 运行 `make check`。
7. reporter 输出根因、修改、验证结果。

## 禁止

- 不做无关重构。
- 不跳过测试。
- 不只改表象不补测试。
```

### 9.9 `.harness/rules/doc-boundary-rules.md`

```markdown
# Document Boundary Rules

## `.harness/` 只允许放

- Agent 角色协议
- Codex 工作流
- AI 使用规则
- Skills
- 任务状态
- 验证脚本说明

## `docs/` 只允许放

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

---

## 10. 编写 Skills

### 10.1 `.harness/skills/bugfix/SKILL.md`

```markdown
---
name: bugfix
description: 修复 bug 时使用，强调根因分析、最小修复和回归测试
---

# Bugfix Skill

## 使用场景

- 修复线上 bug
- 修复测试失败
- 修复用户反馈的问题
- 修复回归问题

## 工作流程

1. 复现问题或定位触发路径。
2. 分析根因。
3. 分析影响范围。
4. 做最小修复。
5. 补回归测试。
6. 运行验证命令。
7. 总结根因和修复方式。

## 禁止

- 不允许顺手重构。
- 不允许只改表象。
- 不允许不补测试就结束。

## 验证命令

```bash
make test
make check
```
```

### 10.2 `.harness/skills/test-writing/SKILL.md`

```markdown
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
```
```

### 10.3 `.harness/skills/fastapi-api/SKILL.md`

```markdown
---
name: fastapi-api
description: 新增或修改 FastAPI API、Service、Schema、Repository 时使用
---

# FastAPI API Skill

## 使用场景

- 新增 API
- 修改 API 返回结构
- 新增 service 方法
- 调整请求/响应 schema

## 工作流程

1. 读取 `docs/architecture/api-conventions.md`。
2. 找到对应 router、schema、service、repository。
3. 先确认是否已有相似接口。
4. 做最小必要修改。
5. 补充单元测试或接口测试。
6. 运行验证命令。

## 约束

- 不允许在 router 中写复杂业务逻辑。
- 不允许绕过 service 层。
- 不允许直接返回未定义结构。
- 错误码必须符合 API 规范。

## 验证命令

```bash
make lint
make test
make check
```
```

### 10.4 `.harness/skills/harness-review/SKILL.md`

```markdown
---
name: harness-review
description: 审查项目是否具备 Harness 工程能力
---

# Harness Review Skill

## 检查项

1. 是否有 AGENTS.md。
2. 是否有 `.harness/agents/`。
3. 是否有 `.harness/workflows/`。
4. 是否有 `.harness/skills/`。
5. 是否有 `.harness/rules/`。
6. 是否有 `docs/product/` 和 `docs/architecture/`。
7. 是否有统一 `make check`。
8. 是否有 lint/typecheck/test。
9. 是否有任务状态文件。
10. 是否有文档边界规则。

## 输出

```text
Harness 成熟度：L1 / L2 / L3

缺失项：
- ...

优先补齐：
- ...

建议修改：
- ...
```
```

---

## 11. 编写项目需求与架构文档模板

### 11.1 `docs/product/prd.md`

```markdown
# PRD

## 背景

描述为什么要做这个项目或功能。

## 目标

描述项目要解决的问题。

## 用户角色

- 用户：
- 管理员：
- 运营：

## 功能范围

### 包含

- ...

### 不包含

- ...

## 验收标准

- ...
```

### 11.2 `docs/product/user-stories.md`

```markdown
# User Stories

## US-001 示例

作为一个用户，  
我希望完成某个动作，  
以便获得某个价值。

### 验收标准

- ...
```

### 11.3 `docs/domain/business-rules.md`

```markdown
# Business Rules

## 规则说明

这里记录业务规则，不记录 Codex 工作规则。

## 示例

- 用户邮箱必须唯一。
- 已完成订单不能取消。
- 敏感操作必须记录审计日志。
```

### 11.4 `docs/domain/state-machines.md`

```markdown
# State Machines

## 示例：Order Lifecycle

```text
pending -> paid -> shipped -> completed
pending -> cancelled
```

禁止：

```text
completed -> cancelled
refunded -> shipped
```
```

### 11.5 `docs/domain/permission-model.md`

```markdown
# Permission Model

## 角色

- user
- admin
- operator

## 权限表达

```text
actor + resource + action + condition
```

## 示例

- user can read own profile
- admin can manage users
- operator can process assigned orders
```

### 11.6 `docs/architecture/overview.md`

```markdown
# Architecture Overview

## 技术栈

项目类型：{{ project_type }}

后端：
{% if project_type in ["fastapi", "fastapi-react", "rag", "langgraph"] %}
- Python {{ python_version }}
- FastAPI / LangGraph / RAG 根据项目类型调整
{% else %}
- 待补充
{% endif %}

前端：
{% if project_type in ["react", "fastapi-react"] %}
- React
- Vite
- TypeScript
{% else %}
- 无前端或待补充
{% endif %}

## 模块边界

待补充。

## 数据流

待补充。
```

### 11.7 `docs/architecture/api-conventions.md`

```markdown
# API Conventions

## Response

```json
{
  "code": "SUCCESS",
  "message": "ok",
  "data": {}
}
```

## Error Response

```json
{
  "code": "ERROR_CODE",
  "message": "Human readable message",
  "request_id": "..."
}
```

## 规则

- 错误码必须稳定。
- 不直接暴露内部异常。
- 涉及创建操作时考虑幂等性。
```

---

## 12. 生成项目并验证

### 12.1 本地生成测试项目

在模板仓库同级目录执行：

```bash
copier copy ./harness-template ./demo-project
```

非交互方式：

```bash
copier copy ./harness-template ./demo-project \
  -d project_name="demo-project" \
  -d project_type="fastapi-react" \
  -d package_manager="uv" \
  -d frontend_package_manager="pnpm" \
  -d use_subagents=true \
  -d use_skills=true
```

### 12.2 检查生成结果

```bash
cd demo-project
tree -a -L 4
```

重点检查：

```text
AGENTS.md 是否正确渲染
Makefile 是否按 project_type 生成
.harness/ 是否完整
docs/ 是否完整
.copier-answers.yml 是否存在
```

### 12.3 初始化 Git

```bash
git init
git add .
git commit -m "init from harness template"
```

---

## 13. 发布模板仓库

提交模板：

```bash
cd harness-template
git add .
git commit -m "init harness copier template"
git tag v0.2.1
```

推送：

```bash
git remote add origin https://github.com/keyl0204/harness-template.git
git push -u origin main
git push origin v0.2.1
```

日常推荐不写 `--vcs-ref`，让 Copier 自动使用最新稳定 tag：

```bash
mkdir my-project
cd my-project
copier copy https://github.com/keyl0204/harness-template.git .
```

如果需要可复现生成，再锁定指定版本：

```bash
copier copy --vcs-ref v0.2.1 https://github.com/keyl0204/harness-template.git .
```

---

## 14. 旧项目如何跟随模板升级

### 14.1 模板升级

比如你新增：

```text
.harness/agents/database_reviewer.md
.harness/skills/sql-migration/SKILL.md
.harness/rules/database-rules.md
```

提交并打 tag：

```bash
cd harness-template
git add .
git commit -m "add database reviewer and sql migration skill"
git tag v0.2.0
git push origin main --tags
```

### 14.2 旧项目更新

```bash
cd my-project
git checkout -b chore/update-harness-template
git status
copier check-update
copier update
```

如果有冲突：

```bash
git status
# 手动解决冲突
git add .
git commit -m "update harness template to v0.2.0"
```

### 14.3 注意事项

```text
1. 不要手动修改 .copier-answers.yml。
2. 更新前确保 git status 是干净的。
3. 更新前先新建分支。
4. 模板仓库建议打 tag。
5. 旧项目必须保留 .copier-answers.yml。
```

---

## 15. 封装为 `harness-init` 一行命令

Copier 可以直接用，但你后续可以封装 CLI。

最终命令：

```bash
harness-init new my-project --type fastapi-react --pm uv --frontend-pm pnpm
```

### 15.1 创建 CLI 项目

```bash
mkdir harness-init
cd harness-init
uv init --package
```

修改 `pyproject.toml`：

```toml
[project]
name = "harness-init"
version = "0.1.0"
description = "Scaffold Harness + Subagents + Skills project structure"
requires-python = ">=3.10"
dependencies = [
  "typer>=0.12.0",
  "copier>=9.0.0"
]

[project.scripts]
harness-init = "harness_init.cli:app"
```

### 15.2 编写 CLI

`src/harness_init/cli.py`：

```python
from __future__ import annotations

import subprocess
from pathlib import Path

import typer

app = typer.Typer(help="Generate Harness + Subagents + Skills project scaffold.")

DEFAULT_TEMPLATE = "https://github.com/keyl0204/harness-template.git"


@app.command()
def new(
    name: str = typer.Argument(..., help="Project directory name"),
    project_type: str = typer.Option("fastapi-react", "--type", help="Project type"),
    package_manager: str = typer.Option("uv", "--pm", help="Python package manager"),
    frontend_package_manager: str = typer.Option("pnpm", "--frontend-pm", help="Frontend package manager"),
    template: str = typer.Option(DEFAULT_TEMPLATE, "--template", help="Copier template repository"),
    ref: str | None = typer.Option(None, "--ref", help="Template git tag or branch"),
    no_subagents: bool = typer.Option(False, "--no-subagents", help="Do not generate subagents"),
    no_skills: bool = typer.Option(False, "--no-skills", help="Do not generate skills"),
) -> None:
    target = Path(name)

    if target.exists():
        raise typer.BadParameter(f"Target already exists: {target}")

    cmd = [
        "copier",
        "copy",
        template,
        str(target),
        "-d",
        f"project_name={name}",
        "-d",
        f"project_type={project_type}",
        "-d",
        f"package_manager={package_manager}",
        "-d",
        f"frontend_package_manager={frontend_package_manager}",
        "-d",
        f"use_subagents={str(not no_subagents).lower()}",
        "-d",
        f"use_skills={str(not no_skills).lower()}",
    ]

    if ref:
        cmd.insert(2, "--vcs-ref")
        cmd.insert(3, ref)

    typer.echo("Running: " + " ".join(cmd))
    subprocess.run(cmd, check=True)
    typer.echo(f"Generated project: {target}")


@app.command()
def update(
    path: str = typer.Argument(".", help="Existing project path"),
) -> None:
    project_dir = Path(path)

    if not project_dir.exists():
        raise typer.BadParameter(f"Path does not exist: {project_dir}")

    subprocess.run(["copier", "check-update"], cwd=project_dir, check=False)
    subprocess.run(["copier", "update"], cwd=project_dir, check=True)


if __name__ == "__main__":
    app()
```

### 15.3 本地安装 CLI

```bash
uv tool install . -e
```

使用：

```bash
harness-init new ai-article --type langgraph --pm uv
harness-init new water-delivery --type fastapi-react --pm uv --frontend-pm pnpm
harness-init update .
```

---

## 16. 给已有项目补 Harness 的 adopt 模式

### 16.1 简单方案

在已有项目根目录执行：

```bash
git checkout -b chore/adopt-harness

copier copy https://github.com/keyl0204/harness-template.git . \
  -d project_name="current-project" \
  -d project_type="fastapi-react"
```

### 16.2 风险

```text
1. 可能覆盖已有 README.md、Makefile、pyproject.toml。
2. 可能和已有 docs/ 结构冲突。
3. 需要人工确认差异。
```

### 16.3 推荐安全做法

```text
1. 先开分支；
2. 先用 copier 生成到临时目录；
3. 人工对比；
4. 只复制 .harness/ 和 AGENTS.md；
5. docs/ 按项目现状合并。
```

命令：

```bash
copier copy https://github.com/keyl0204/harness-template.git /tmp/harness-adopt \
  -d project_name="current-project" \
  -d project_type="fastapi-react"

cp -r /tmp/harness-adopt/.harness .
cp /tmp/harness-adopt/AGENTS.md .
```

---

## 17. 模板版本管理规范

推荐语义版本：

```text
v0.2.1：当前基础 Harness
v0.2.0：增加 Skills
v0.3.0：增加 CI
v0.4.0：增加 security reviewer
v1.0.0：稳定版
```

模板仓库维护 `CHANGELOG.md`：

```markdown
# Changelog

## v0.2.0

### Added

- `.harness/skills/docs-sync/SKILL.md`
- `.harness/agents/security_reviewer.md`

### Changed

- AGENTS.md 增加文档边界规则

### Migration

旧项目执行：

```bash
copier update
```
```

推荐模板分支：

```text
main：最新稳定
dev：开发中
v0.x tags：版本快照
```

---

## 18. 推荐落地节奏

### 第 1 天：搭模板骨架

```text
copier.yml
AGENTS.md.jinja
README.md.jinja
Makefile.jinja
.harness/
docs/
```

### 第 2 天：补子 Agent 和工作流

```text
planner
code_mapper
backend_engineer
frontend_engineer
test_writer
reviewer
security_reviewer
reporter
```

### 第 3 天：补 Skills

```text
bugfix
test-writing
fastapi-api
react-page
docs-sync
harness-review
```

### 第 4 天：补项目文档模板

```text
product
domain
architecture
operations
decisions
```

### 第 5 天：本地生成 demo 项目测试

```bash
copier copy ./harness-template ./demo-project
```

### 第 6 天：发布 v0.2.1

```bash
git tag v0.2.1
git push origin v0.2.1
```

### 第 7 天：接入真实项目试用

```bash
mkdir my-real-project
cd my-real-project
copier copy https://github.com/keyl0204/harness-template.git .
```

---

## 19. Codex 日常使用 Prompt

### 19.1 新项目初始化后

```text
请读取 AGENTS.md，并按项目 Harness 结构检查当前工程是否完整。

要求：
1. 检查 .harness/agents 是否完整；
2. 检查 .harness/skills 是否完整；
3. 检查 .harness/workflows 是否完整；
4. 检查 docs/product、docs/domain、docs/architecture 是否完整；
5. 检查 Makefile 是否有 make check；
6. 输出 Harness 成熟度和建议补齐项。
```

### 19.2 通用开发任务

```text
请按 Harness + 子 Agent + Skills 工作流处理这个任务：

任务：
<填写任务>

要求：
1. 读取 AGENTS.md；
2. 根据任务类型读取 .harness/workflows/；
3. 读取相关 .harness/agents/ 角色协议；
4. 需要时使用 .harness/skills/；
5. 涉及业务行为时读取 docs/product/ 和 docs/domain/；
6. 涉及架构/API/数据库时读取 docs/architecture/；
7. 做最小必要修改；
8. 运行 make check；
9. 输出修改内容、验证结果、是否更新 docs 或 .harness。
```

### 19.3 Bug 修复任务

```text
请按 bugfix Skill 和 Harness 工作流修复这个问题：

问题：
<描述 bug>

要求：
1. 读取 AGENTS.md；
2. 读取 .harness/workflows/bugfix.md；
3. 读取 .harness/skills/bugfix/SKILL.md；
4. 先定位根因；
5. 做最小修复；
6. 补回归测试；
7. 运行 make check；
8. 输出根因、修改文件、测试覆盖、验证结果。
```

### 19.4 新增接口任务

```text
请按 FastAPI API Skill 新增接口：

需求：
<接口需求>

要求：
1. 读取 AGENTS.md；
2. 读取 docs/architecture/api-conventions.md；
3. 读取 .harness/skills/fastapi-api/SKILL.md；
4. 分析 router / schema / service / repository 应该如何修改；
5. 做最小必要实现；
6. 补接口测试和 service 测试；
7. 运行 make check；
8. 总结 API 路径、请求参数、响应结构和验证结果。
```

---

## 20. 常见问题与避坑

### 20.1 AGENTS.md 不要写太长

错误做法：

```text
把 PRD、架构、API、业务规则、Codex 规则全塞进 AGENTS.md。
```

正确做法：

```text
AGENTS.md 只做入口路由。
详细内容放 docs/ 和 .harness/。
```

### 20.2 `.harness/` 和 `docs/` 不要混

```text
.harness/ 管 AI 怎么工作。
docs/ 管项目是什么。
```

### 20.3 不要手动改 `.copier-answers.yml`

```text
它是 Copier 追踪模板答案和版本的重要文件。
手动修改会影响 update。
```

### 20.4 模板要打 tag

```text
不要所有项目都跟 main。
日常可以不写 --vcs-ref，让 Copier 自动使用最新稳定 tag；需要可复现时再使用 --vcs-ref v0.2.1。
```

### 20.5 更新旧项目前先开分支

```bash
git checkout -b chore/update-harness-template
copier update
```

### 20.6 第一版不要过度复杂

第一版只做：

```text
AGENTS.md
.harness/
docs/
Makefile
```

不要一开始就做复杂业务模板。

---

## 21. 最终交付清单

### 模板仓库必须包含

```text
copier.yml
AGENTS.md.jinja
README.md.jinja
Makefile.jinja
pyproject.toml.jinja
package.json.jinja
.gitignore.jinja
.harness/
docs/
src/.gitkeep
tests/.gitkeep
```

### 生成项目必须包含

```text
AGENTS.md
README.md
Makefile
.copier-answers.yml
.harness/agents/
.harness/skills/
.harness/workflows/
.harness/rules/
.harness/state/
docs/product/
docs/domain/
docs/architecture/
docs/operations/
src/
tests/
```

### 必须支持的命令

```bash
make setup
make dev
make lint
make typecheck
make test
make check
```

### 必须支持的 Copier 命令

```bash
mkdir my-project
cd my-project
copier copy https://github.com/keyl0204/harness-template.git .
copier check-update
copier update
```

### 后续 CLI 命令

```bash
harness-init new my-project --type fastapi-react --pm uv --frontend-pm pnpm
harness-init update .
```

---

## 22. 参考资料

- Copier 官方文档：https://copier.readthedocs.io/
- Copier 配置文档：https://copier.readthedocs.io/en/stable/configuring/
- Copier 更新项目文档：https://copier.readthedocs.io/en/stable/updating/
- Codex AGENTS.md 文档：https://developers.openai.com/codex/guides/agents-md
- Codex Skills 文档：https://developers.openai.com/codex/skills
- Codex Non-interactive mode：https://developers.openai.com/codex/noninteractive
- Codex Sandbox 文档：https://developers.openai.com/codex/concepts/sandboxing
- Codex Subagents 文档：https://developers.openai.com/codex/subagents
