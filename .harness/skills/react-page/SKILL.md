---
name: react-page
description: 构建或修改 React 页面、组件、状态、数据加载或 UI 测试时使用。
---

# React Page Skill

## 使用场景

- 创建 React 页面。
- 更新组件。
- 将 API 数据接入 UI。
- 新增 UI 状态或测试。

## 工作流程

1. 读取相关架构和 API 文档。
2. 识别现有组件、路由和状态模式。
3. 设计完整 UI 状态：loading、empty、error、success。
4. 实现最小组件改动。
5. 在项目已有测试模式时补测试。
6. 运行前端验证。

## 约束

- 未经允许不要新增 UI 框架。
- 不要绕过现有数据获取约定。
- 不要留下文本溢出或响应式断裂状态。

## 验证命令

```bash
make frontend-check
make check
```
