# Root Cause Analysis Methods

## 5 Whys Method

For each problem, ask "为什么" 5 times to get to the root cause.

Example:
```
问题: 推送失败
1. 为什么失败? → 网络超时
2. 为什么超时? → GitHub 连接不稳定
3. 为什么连接不稳定? → 可能是防火墙
4. 为什么是防火墙? → 可能是公司网络限制
5. 为什么? → 需要用 HTTPS 而不是 SSH
```

## 4P Method

Analyze from 4 perspectives:
- **People**: 谁涉及?
- **Process**: 流程有什么问题?
- **Product**: 工具有什么问题?
- **Place**: 环境有什么影响?

## Fishbone Diagram

```
         问题
           │
    ┌──────┼──────┬──────────┐
    │      │      │          │
  方法   沟通   工具     预期
```

## Reflection Questions

### For AI (me)
- 我做了什么假设？这些假设对吗？
- 我有什么没问清楚的？
- 我应该什么时候停止并确认？
- 用户给我的信号我读懂了吗？

### For Human (you)
- 你当时想说什么但没说？
- 你期望我怎么处理？
- 有什么我应该直接问的？

## Common Pitfall Patterns

| Pattern | Description | Solution |
|---------|-------------|----------|
| 重复失败 | Same failure repeated | Stop and ask after 1-2 tries |
| 假设理解 | Assumed understanding | Confirm before proceeding |
| 忽略信号 | Missed frustration signals | Watch for "算了" / "直接说" |
| 过度解释 | Too much explanation | Give choices, not just info |
| 等待太久 | Too long without update | Check in periodically |
