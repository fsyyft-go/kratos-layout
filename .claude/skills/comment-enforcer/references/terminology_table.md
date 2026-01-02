# Go 代码注释标准术语映射表

本文档定义了 Kratos Layout 项目中 Go 代码注释使用的标准术语表述，确保全项目注释的专业性和一致性。

## 使用说明

1. **查找类型**：在表中查找参数或返回值的类型
2. **使用标准表述**：使用对应的标准注释表述
3. **保持一致性**：全局统一使用相同的表述
4. **检查一致性**：使用 `check_terminology.py` 脚本检查

---

## 标准术语表

### 上下文和配置相关

| 类型/参数 | 标准表述 | 说明 |
|----------|---------|------|
| `context.Context` | "请求上下文，用于取消与超时控制。" | 必须使用此表述 |
| `*Config` | "应用配置信息。" | 简洁明了 |
| `*conf.Config` | "应用配置信息。" | 同上 |
| `Config` | "配置结构体。" | 非指针版本 |

### 日志和监控相关

| 类型/参数 | 标准表述 | 说明 |
|----------|---------|------|
| `kitlog.Logger` | "日志记录器。" | 统一表述 |
| `Logger` | "日志记录器。" | 通用表述 |
| `log.Logger` | "日志记录器。" | 标准库版本 |

### 数据访问相关

| 类型/参数 | 标准表述 | 说明 |
|----------|---------|------|
| `*Data` | "数据仓储接口。" | 数据层抽象 |
| `*GreeterRepo` | "Greeter 仓储接口。" | 特定实体仓储 |
| `*UserRepo` | "User 仓储接口。" | 特定实体仓储 |
| `*Repository` | "数据仓储接口。" | 通用仓储 |

### 业务实体相关

| 类型/参数 | 标准表述 | 说明 |
|----------|---------|------|
| `*Greeter` | "Greeter 实体。" | 业务实体 |
| `*User` | "User 实体。" | 业务实体 |
| `*Task` | "Task 实体。" | 业务实体 |
| `Greeter` | "Greeter 对象。" | 非指针版本 |

### 服务和用例相关

| 类型/参数 | 标准表述 | 说明 |
|----------|---------|------|
| `GreeterUsecase` | "Greeter 业务逻辑接口。" | 业务层抽象 |
| `*GreeterUsecase` | "Greeter 用例实现。" | 业务层实现 |
| `GreeterService` | "Greeter 服务接口。" | 服务层接口 |

### HTTP 和服务器相关

| 类型/参数 | 标准表述 | 说明 |
|----------|---------|------|
| `*HTTPServer` | "HTTP 服务器实例。" | HTTP 服务器 |
| `*GRPCServer` | "gRPC 服务器实例。" | gRPC 服务器 |
| `*Server` | "服务器实例。" | 通用服务器 |

### 返回值相关

| 返回值类型 | 标准表述 | 说明 |
|----------|---------|------|
| `error`（失败时） | "失败时返回错误，成功时返回 nil。" | 统一错误返回表述 |
| `error`（成功时） | "操作成功返回 nil。" | 成功返回 nil |
| `*Greeter` | "返回的 Greeter 实体。" | 返回实体 |
| `bool` | "成功返回 true，失败返回 false。" | 布尔返回值 |
| `int` | "返回记录数量。" | 数量返回 |
| `int64` | "返回实体 ID。" | ID 返回 |
| `string` | "返回结果字符串。" | 字符串返回 |

### 中间件和拦截器相关

| 类型/参数 | 标准表述 | 说明 |
|----------|---------|------|
| `Middleware` | "中间件函数。" | 中间件 |
| `*Middleware` | "中间件实例。" | 中间件实例 |
| `Interceptor` | "拦截器函数。" | 拦截器 |

### 验证和转换相关

| 类型/参数 | 标准表述 | 说明 |
|----------|---------|------|
| `*Validator` | "验证器实例。" | 参数验证器 |
| `*Converter` | "转换器实例。" | 数据转换器 |
| `*Encoder` | "编码器实例。" | 编码器 |
| `*Decoder` | "解码器实例。" | 解码器 |

### 缓存和存储相关

| 类型/参数 | 标准表述 | 说明 |
|----------|---------|------|
| `*Cache` | "缓存接口。" | 缓存抽象 |
| `*Redis` | "Redis 客户端实例。" | Redis 客户端 |
| `*Database` | "数据库连接实例。" | 数据库连接 |

### 配置项相关

| 类型/参数 | 标准表述 | 说明 |
|----------|---------|------|
| `ServerConfig` | "服务器配置。" | 服务器配置项 |
| `DatabaseConfig` | "数据库配置。" | 数据库配置项 |
| `CacheConfig` | "缓存配置。" | 缓存配置项 |

### 工具和辅助类

| 类型/参数 | 标准表述 | 说明 |
|----------|---------|------|
| `*Util` | "工具类实例。" | 通用工具 |
| `*Helper` | "辅助类实例。" | 辅助类 |
| `*Builder` | "构建器实例。" | 构建器模式 |

---

## 使用示例

### 函数参数注释

```go
// ✅ 正确示例：使用标准术语
func (u *greeterUsecase) CreateGreeter(
    ctx context.Context,  // 请求上下文，用于取消与超时控制。
    conf *Config,          // 应用配置信息。
    logger kitlog.Logger,  // 日志记录器。
    g *Greeter,            // Greeter 实体。
) (*Greeter, error) {
    // ...
    return result, nil  // 失败时返回错误，成功时返回 nil。
}
```

### 接口定义注释

```go
// ✅ 正确示例：接口方法使用标准术语
type GreeterRepo interface {
    // Save 保存 Greeter 实体到数据库。
    // 参数：
    //   - ctx：请求上下文，用于取消与超时控制。
    //   - g：Greeter 实体。
    //
    // 返回值：
    //   - *Greeter：保存后的实体。
    //   - error：失败时返回错误，成功时返回 nil。
    Save(ctx context.Context, g *Greeter) (*Greeter, error)
}
```

### 结构体字段注释

```go
// ✅ 正确示例：结构体字段使用标准术语
type greeterUsecase struct {
    logger kitlog.Logger  // 日志记录器。
    conf   *Config        // 应用配置信息。
    repo   GreeterRepo    // Greeter 仓储接口。
}
```

---

## 一致性检查

### 自动化检查

使用 `check_terminology.py` 脚本检查项目中的术语一致性：

```bash
# 检查所有标准术语
python3 .claude/skills/comment-enforcer/scripts/check_terminology.py

# 检查特定类型
python3 .claude/skills/comment-enforcer/scripts/check_terminology.py \
  --type context.Context
```

### 手动检查

**检查清单**：
- [ ] 所有 `context.Context` 参数都使用 "请求上下文，用于取消与超时控制。"
- [ ] 所有 `*Config` 参数都使用 "应用配置信息。"
- [ ] 所有 `Logger` 参数都使用 "日志记录器。"
- [ ] 所有 `error` 返回值都使用 "失败时返回错误，成功时返回 nil。"
- [ ] 相同类型使用相同的注释表述
- [ ] 注释以中文标点符号结束

---

## 常见错误

### 错误示例

```go
// ❌ 错误：不一致的表述
func foo(ctx context.Context) error {
    // ctx 上下文对象
}

func bar(ctx context.Context) error {
    // ctx 请求上下文
}

// ❌ 错误：未使用标准表述
func baz(conf *Config) error {
    // conf 配置对象（应为"应用配置信息。"）
}

// ❌ 错误：缺少标准标点
func qux(logger kitlog.Logger) error {
    // logger 日志记录器（缺少句号）
}
```

### 正确示例

```go
// ✅ 正确：一致使用标准表述
func foo(ctx context.Context) error {
    // ctx 请求上下文，用于取消与超时控制。
}

func bar(ctx context.Context) error {
    // ctx 请求上下文，用于取消与超时控制。
}

func baz(conf *Config) error {
    // conf 应用配置信息。
}

func qux(logger kitlog.Logger) error {
    // logger 日志记录器。
}
```

---

## 扩展标准

### 添加新的标准术语

如果需要添加新的标准术语：

1. 在本文档中添加新条目
2. 在 `check_terminology.py` 中更新 `STANDARD_TERMINOLOGY` 字典
3. 在整个项目中统一使用新的表述
4. 运行检查脚本验证一致性

### 术语命名建议

| 原则 | 说明 |
|------|------|
| **简洁明了** | 避免冗长，确保清晰 |
| **专业准确** | 使用技术术语，避免口语化 |
| **统一表述** | 相同语义使用相同表述 |
| **完整句子** | 以标点符号结束的完整句子 |

---

## 参考资源

- **完整规范**：`comment_standards.md`
- **原始规范**：`.ai/rule.md.bak`
- **检查脚本**：`.claude/skills/comment-enforcer/scripts/check_terminology.py`

---

**版本**：1.0.0
**最后更新**：2026-01-06
**维护者**：Kratos Layout 项目组
