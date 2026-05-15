# 运维手册

## 本地开发

```bash
make setup
make dev
```

## 验证

```bash
make check
```

## Copier 生成到当前文件夹

从模板生成项目时，命令最后必须提供两个位置参数：

```text
模板源 目标目录
```

如果希望默认生成到当前文件夹，先进入目标目录，然后把目标目录写成 `.`。

PowerShell 示例：

```powershell
mkdir D:\codeProject\ai\harness-project
cd D:\codeProject\ai\harness-project

uvx copier copy --trust --defaults `
  -d project_name=harness-project `
  -d project_type=fastapi-react `
  -d package_manager=uv `
  -d frontend_package_manager=pnpm `
  -d use_docker=true `
  https://github.com/keyl0204/harness-template.git `
  .
```

如果目标目录已经存在，并且只是本地覆盖验证：

```powershell
uvx copier copy --trust --defaults --force `
  -d project_name=harness-project `
  -d project_type=fastapi-react `
  -d package_manager=uv `
  -d frontend_package_manager=pnpm `
  -d use_docker=true `
  https://github.com/keyl0204/harness-template.git `
  .
```

注意：

- PowerShell 每行末尾的反引号 `` ` `` 后面不能有空格。
- `.` 表示当前目录。只有当前目录就是模板仓库时，才能把 `.` 当作模板路径。
- 在这里，`.` 是目标目录，不是模板路径。
- 如果只写了 `-d use_docker=true`，但没有模板源和目标目录，Copier 会报 `Expected at least 2 positional arguments`。
- 使用 GitHub 模板源时，Copier 会自动选择最新稳定 tag。
- 如果模板目录已经是 Git 仓库并且存在 tag，Copier 默认可能会使用最新 tag，而不是未提交的工作区内容。修改模板后要先 `git commit` 并打新 tag，或在验证命令中明确使用需要的 `--vcs-ref`。

使用本地 Git 仓库当前 `HEAD` 验证：

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

如果要验证刚修改但尚未提交的模板内容，先提交到本地 Git：

```powershell
cd D:\codeProject\ai\harness-template
git add .
git commit -m "update template docs"
```

## 本地生成后验证

进入生成项目后运行：

```powershell
cd D:\codeProject\ai\harness-project
uv sync
make check
```

如果当前 Windows 环境没有 `make`，可以手动运行后端检查：

```powershell
uv run ruff check .
uv run ruff format --check .
uv run pyright
uv run pytest
```

前端项目还需要运行：

```powershell
pnpm install
pnpm run lint
pnpm run typecheck
pnpm run test
pnpm run build
```

## 模板 Git 发布

如果需要长期复用模板、固定版本、支持旧项目升级，建议把模板仓库提交到 Git 并打 tag：

```powershell
cd D:\codeProject\ai\harness-template
git init
git add .
git commit -m "init harness copier template"
git tag v0.2.1
```

推送远程仓库：

```powershell
git remote add origin https://github.com/keyl0204/harness-template.git
git push -u origin main
git push origin v0.2.1
```

之后新项目可以使用最新稳定 tag 生成。日常推荐不写 `--vcs-ref`，让 Copier 自动选择最新 tag：

```powershell
mkdir my-project
cd my-project
uvx copier copy --trust https://github.com/keyl0204/harness-template.git .
```

如果需要可复现生成，再锁定指定版本：

```powershell
uvx copier copy --trust --vcs-ref v0.2.1 https://github.com/keyl0204/harness-template.git .
```

版本 tag 建议保持语义版本格式，例如 `v0.2.1`、`v0.2.2`、`v0.3.0`。

## 旧项目升级模板

模板发布新版本后，在旧项目中执行：

```powershell
cd D:\codeProject\ai\harness-project
git checkout -b chore/update-harness-template
uvx copier check-update
uvx copier update --trust
```

升级前建议确保工作区干净，并保留 `.copier-answers.yml`。不要手动修改 `.copier-answers.yml`，它记录模板来源和生成参数。

## 常见问题

| 现象 | 检查项 | 修复方式 |
|---|---|---|
| `Expected at least 2 positional arguments` | 是否缺少模板源和目标目录 | 在命令最后补上 `https://github.com/keyl0204/harness-template.git .` |
| `Copying from template version None` | 是否使用本地模板路径 | 本地验证时正常；需要版本号时从 Git tag 生成 |
| 目标目录已存在 | 是否要覆盖本地验证结果 | 确认无重要改动后使用 `--force` |
| PowerShell 进入 `>>` 多行续写 | 行尾反引号后是否有空格，或命令是否未写完 | 删除反引号后的空格，并补齐最后两个路径参数 |
