# 状态机

## 示例：订单生命周期

```text
pending -> paid -> shipped -> completed
pending -> cancelled
```

禁止的状态流转：

```text
completed -> cancelled
refunded -> shipped
```
