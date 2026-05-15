---
name: security-review
description: 权限、密钥处理、文件、网络、shell 和敏感操作审查时使用。
---

# Security Review Skill

## 使用场景

- 认证或授权变更。
- 处理密钥或凭据。
- 基于用户输入读写文件。
- 调用外部系统。
- 执行 shell 命令。
- 实现管理员或破坏性操作。

## 检查清单

1. actor、resource、action 和 condition 清晰。
2. 越权访问已测试。
3. 密钥不会被记录或返回。
4. 信任边界已校验输入。
5. 文件路径被约束。
6. 错误响应不暴露内部细节。

## 验证命令

```bash
make test
make security
make check
```
