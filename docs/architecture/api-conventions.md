# API 规范

## 成功响应

```json
{
  "code": "SUCCESS",
  "message": "ok",
  "data": {}
}
```

## 错误响应

```json
{
  "code": "ERROR_CODE",
  "message": "Human readable message",
  "request_id": "..."
}
```

## 规则

- 错误码必须稳定。
- 不直接暴露内部异常细节。
- 创建类操作需要考虑幂等性。
