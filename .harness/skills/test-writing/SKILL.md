---
name: test-writing
description: 为变更行为补充单元测试、回归测试和 API 测试。
---

# Test Writing Skill

## 使用场景

- bugfix 后补回归测试。
- 新功能后补测试。
- 为 service 或 API 行为补覆盖。
- 固化权限或校验规则。

## 工作步骤

1. 识别变更行为。
2. 找到最接近的现有测试风格。
3. 覆盖成功路径。
4. 覆盖失败路径。
5. 覆盖重要边界条件。
6. 运行测试。
7. 完成前修复失败测试。

## 验证命令

```bash
make test
make check
```
