# harness-template

这是一个基于 Copier 的 Harness 工程模板，用于一键生成支持 Codex 协作开发的项目骨架。

模板生成的项目会内置：

- `AGENTS.md`：Codex 入口和文档路由地图
- `.harness/agents/`：子 Agent 角色协议
- `.harness/skills/`：可复用任务技能
- `.harness/workflows/`：标准任务工作流
- `.harness/rules/`：AI 工程协作规则
- `.harness/state/`：任务状态和交接记录
- `docs/`：产品、领域、架构、运维和 ADR 文档
- `Makefile`：统一验证入口
- `src/`、`tests/`：最小代码与测试骨架

## 模板能力

支持的项目类型：

- `python`
- `fastapi`
- `fastapi-react`
- `react`
- `rag`
- `langgraph`

支持的包管理器：

- Python：`uv`、`pip`、`poetry`、`none`
- 前端：`pnpm`、`npm`、`yarn`、`none`

可选能力：

- `use_subagents`：是否生成子 Agent 角色协议
- `use_skills`：是否生成 Skills
- `use_security_rules`：是否生成安全规则和安全审查 Agent
- `use_ci`：是否生成 GitHub Actions CI
- `use_docker`：是否生成 `docker/` 目录下的 Dockerfile 和 compose 示例

## 本地生成项目

PowerShell 示例：

```powershell
uvx copier copy --trust --defaults `
  -d project_name=harness-project `
  -d project_type=fastapi-react `
  -d package_manager=uv `
  -d frontend_package_manager=pnpm `
  -d use_docker=true `
  D:\codeProject\ai\harness-template `
  D:\codeProject\ai\harness-project
```

注意：命令最后必须有两个位置参数：

```text
模板路径 目标项目路径
```

如果缺少这两个参数，Copier 会报：

```text
Expected at least 2 positional arguments
```

如果目标目录已存在，并且确认只是本地覆盖验证，可以加 `--force`：

```powershell
uvx copier copy --trust --defaults --force `
  -d project_name=harness-project `
  -d project_type=fastapi-react `
  -d package_manager=uv `
  -d frontend_package_manager=pnpm `
  -d use_docker=true `
  D:\codeProject\ai\harness-template `
  D:\codeProject\ai\harness-project
```

PowerShell 每行末尾的反引号 `` ` `` 后面不能有空格。

## 本地验证生成结果

进入生成项目：

```powershell
cd D:\codeProject\ai\harness-project
uv sync
make check
```

如果 Windows 环境没有 `make`，可以先手动运行后端检查：

```powershell
uv run ruff check .
uv run ruff format --check .
uv run pyright
uv run pytest
```

如果是 `fastapi-react` 或 `react` 项目，还需要运行前端检查：

```powershell
pnpm install
pnpm run lint
pnpm run typecheck
pnpm run test
pnpm run build
```

## Docker 文件位置

当 `use_docker=true` 时，生成项目会包含：

```text
docker/
├── Dockerfile
└── docker-compose.yml
```

`docker-compose.yml` 使用项目根目录作为 build context：

```yaml
build:
  context: ..
  dockerfile: docker/Dockerfile
```

## Git 发布模板

本地提交：

```powershell
cd D:\codeProject\ai\harness-template
git add .
git commit -m "update harness template"
git tag v0.2.1
```

推送远程：

```powershell
git push -u origin main
git push origin v0.2.1
```

如果 GitHub 拒绝推送 `.github/workflows/ci.yml.jinja`，说明当前 token 缺少 `workflow` scope。需要使用包含 `repo` 和 `workflow` 权限的 Personal Access Token。

## 从 Git 生成项目

模板推送到 Git 后，日常推荐不写 `--vcs-ref`，让 Copier 自动使用最新稳定 tag：

```powershell
uvx copier copy --trust `
  https://github.com/keyl0204/harness-template.git `
  D:\codeProject\ai\harness-project
```

如果需要可复现生成，再锁定指定版本：

```powershell
uvx copier copy --trust --vcs-ref v0.2.1 `
  https://github.com/keyl0204/harness-template.git `
  D:\codeProject\ai\harness-project
```

版本 tag 建议保持语义版本格式，例如 `v0.2.1`、`v0.2.2`、`v0.3.0`。

如果模板目录已经是 Git 仓库并且存在 tag，Copier 默认可能会使用最新 tag，而不是未提交的工作区内容。验证本地最新提交时可以加：

```powershell
uvx copier copy --trust --defaults --vcs-ref=HEAD `
  -d project_name=harness-project `
  -d project_type=fastapi-react `
  -d package_manager=uv `
  -d frontend_package_manager=pnpm `
  -d use_docker=true `
  D:\codeProject\ai\harness-template `
  D:\codeProject\ai\harness-project
```

## 旧项目升级模板

在生成项目中执行：

```powershell
cd D:\codeProject\ai\harness-project
git checkout -b chore/update-harness-template
uvx copier check-update
uvx copier update --trust
```

升级前建议确保工作区干净，并保留 `.copier-answers.yml`。不要手动修改 `.copier-answers.yml`，它记录模板来源和生成参数。

## 常见问题

| 问题 | 原因 | 处理方式 |
|---|---|---|
| `Expected at least 2 positional arguments` | 缺少模板路径和目标项目路径 | 在命令最后补上两个路径 |
| `Copying from template version None` | 使用的是本地非 Git tag 模板 | 本地验证时正常；正式使用建议从 Git tag 生成 |
| `src refspec main does not match any` | 本地没有 `main` 分支 | 执行 `git branch -M main` 后再推送 |
| GitHub 拒绝 workflow 文件 | PAT 缺少 `workflow` scope | 生成包含 `repo` 和 `workflow` 权限的新 token |
| `uv sync` 下载 PyPI 超时 | 网络无法访问 PyPI | 使用 `uv sync --index-url https://pypi.tuna.tsinghua.edu.cn/simple` |

## 目录结构

```text
harness-template/
├── copier.yml
├── README.md
├── README.md.jinja
├── AGENTS.md.jinja
├── Makefile.jinja
├── pyproject.toml.jinja
├── package.json.jinja
├── docker/
├── .harness/
├── docs/
├── src/
└── tests/
```

核心边界：

```text
.harness/ = AI 如何参与工程
docs/     = 项目事实文档
src/      = 代码实现
tests/    = 验证代码
```
