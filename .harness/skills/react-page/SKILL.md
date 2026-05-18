---
name: react-page
description: 创建或修改 React 页面、组件、路由、状态、数据加载、表单、UI 状态、可访问性行为、响应式布局或前端测试时使用。该 Skill 保持 UI 实现符合既有模式，并覆盖 loading、empty、error、success 等完整状态。
---

# React Page Skill

## 适用场景

- 创建或修改 React 页面、组件、路由或布局。
- 接入 API 数据、缓存、状态管理或表单提交。
- 新增 loading、empty、error、success、权限不足等 UI 状态。
- 修复响应式布局、可访问性、文本溢出或交互问题。
- 为 UI 行为补充测试、lint、typecheck 或 build 验证。

## 必须读取

1. `AGENTS.md`
2. `.harness/rules/coding-rules.md`
3. `.harness/rules/testing-rules.md`
4. `docs/architecture/overview.md`
5. 涉及 API：`docs/architecture/api-conventions.md`
6. 涉及用户路径：`docs/product/user-stories.md` 和 `docs/product/acceptance-criteria.md`
7. 现有组件、路由、样式、状态管理和测试模式

## UI 工作流程

1. 确认用户任务、入口页面、主要操作和完成状态。
2. 找到相似组件和数据加载方式，沿用现有模式。
3. 设计完整状态：loading、empty、error、success、permission denied、submitting。
4. 明确 API 契约：请求参数、响应字段、错误码和重试方式。
5. 实现最小组件改动，保持状态边界和组件职责清晰。
6. 检查响应式布局、键盘可达性、焦点管理和文本溢出。
7. 按项目测试模式补充 UI 测试或至少运行前端验证。

## 结构设计和文件大小

1. 先识别项目现有页面、组件、状态和数据访问组织方式，再决定落点，不要求固定目录名。
2. API 请求和响应适配应有清晰边界，不散落在多个组件中。
3. 业务状态和副作用应靠近对应业务模块，不塞进通用工具。
4. `utils`、`helpers`、`shared` 只放业务无关纯工具；包含权限、领域状态、API 字段含义或用户路径的逻辑不放入通用工具。
5. 业务源码文件默认不超过 800 行；预计超出时按页面区块、表单、列表、详情、hook 或 API client 拆分。
6. 复杂交互可评估 reducer、custom hook、strategy map、adapter 或 compound component；简单组件保持直接。

## 设计和交互门禁

- 不新增 UI 框架、图标库或状态库，除非项目已有约定或用户明确要求。
- 不绕过现有数据获取、路由或权限显示模式。
- 不把内部错误、调试字段或实现细节展示给用户。
- 表单必须防重复提交，并能展示服务端错误。
- 文本必须在移动端和桌面端容器内可读，不遮挡交互元素。
- 按钮、输入、列表、表格和空状态必须有稳定尺寸或合理响应式约束。
- 图标和颜色使用必须服务于操作识别，不制造只靠颜色理解的状态。
- 文件大小没有超过 800 行；超过时已按业务区块或状态逻辑拆分。

## 测试重点

- 主要用户路径成功。
- API 失败或无数据。
- 表单校验和提交中状态。
- 权限不足或会话失效。
- 条件渲染不会产生空白页面或不可点击控件。

## 验证命令

```bash
make frontend-check
make check
```

可聚焦运行：

```bash
pnpm run test
pnpm run lint
pnpm run typecheck
pnpm run build
```

## 输出格式

```text
用户路径：
- ...

修改文件：
- ...

UI 状态覆盖：
- loading:
- empty:
- error:
- success:
- permission:

结构设计和拆分：
- ...

验证命令：
- ...

剩余风险：
- ...
```
