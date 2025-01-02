# 标准术语表

## 概述

本文档定义了 Go 代码注释中常用的标准术语和表述,确保项目注释的一致性和专业性。

**核心原则**:
1. **全局一致性**: 相同类型和概念使用统一表述
2. **参数优先**: 先说明参数,再说明返回值
3. **中文标点**: 所有表述以中文标点符号结束
4. **专业准确**: 使用技术领域专业术语

## 常见参数标准表述

### 上下文相关

| 参数类型 | 标准表述 | 示例 |
|---------|---------|------|
| `context.Context` | "请求上下文,用于取消与超时控制。" | `ctx context.Context` |
| `context.Context` | "上下文信息,用于取消与超时控制。" | `ctx context.Context` |

**使用场景**:
```go
// CreateGreeter 创建一个新的 Greeter 实体。
//
// 参数：
//   - ctx: 请求上下文,用于取消与超时控制。
//   - g: 待创建的 Greeter 实体。
//
// 返回：
//   - *Greeter: 创建成功的实体,包含生成的标识。
//   - error: 创建失败时返回错误,成功时返回 nil。
func CreateGreeter(ctx context.Context, g *Greeter) (*Greeter, error) {
    // 实现代码。
}
```

### 配置相关

| 参数类型 | 标准表述 | 示例 |
|---------|---------|------|
| `*Config` | "应用配置信息。" | `conf *appconf.Config` |
| `*conf.Config` | "应用配置信息。" | `conf *conf.Config` |
| `*conf.Data` | "数据配置信息。" | `dc *conf.Data` |
| `*conf.Server` | "服务器配置信息。" | `sc *conf.Server` |

**使用场景**:
```go
// NewGreeterUsecase 创建一个新的 Greeter 用例实例。
//
// 参数：
//   - logger: 日志记录器,用于记录业务日志。
//   - conf: 应用配置信息。
//   - repo: Greeter 仓储接口实现,提供数据访问能力。
//
// 返回：
//   - GreeterUsecase: Greeter 用例接口实现。
func NewGreeterUsecase(logger kitlog.Logger, conf *appconf.Config, repo GreeterRepo) GreeterUsecase {
    return &greeterUsecase{
        logger: logger,
        conf:   conf,
        repo:   repo,
    }
}
```

### 日志相关

| 参数类型 | 标准表述 | 示例 |
|---------|---------|------|
| `kitlog.Logger` | "日志记录器。" | `logger kitlog.Logger` |
| `log.Logger` | "日志记录器。" | `logger log.Logger` |

**使用场景**:
```go
// NewGreeterRepo 创建一个新的 Greeter 仓储实例。
//
// 参数：
//   - logger: 日志记录器。
//   - db: 数据库连接实例。
//
// 返回：
//   - GreeterRepo: Greeter 仓储接口实现。
func NewGreeterRepo(logger kitlog.Logger, db *sql.DB) GreeterRepo {
    return &greeterRepo{
        logger: logger,
        db:     db,
    }
}
```

### 实体相关

| 参数类型 | 标准表述 | 示例 |
|---------|---------|------|
| `*Greeter` | "Greeter 实体。" | `g *Greeter` |
| `*User` | "User 实体。" | `u *User` |
| `*Order` | "Order 实体。" | `o *Order` |
| `*Product` | "Product 实体。" | `p *Product` |

**使用场景**:
```go
// Save 保存一个 Greeter 实体。
//
// 参数：
//   - ctx: 请求上下文,用于取消与超时控制。
//   - g: Greeter 实体。
//
// 返回：
//   - *Greeter: 保存成功后的实体,可能包含生成的 ID。
//   - error: 保存失败时返回错误,成功时返回 nil。
func (r *greeterRepo) Save(ctx context.Context, g *Greeter) (*Greeter, error) {
    // 实现代码。
}
```

### 仓储接口相关

| 参数类型 | 标准表述 | 示例 |
|---------|---------|------|
| `GreeterRepo` | "Greeter 仓储接口实现,提供数据访问能力。" | `repo GreeterRepo` |
| `UserRepo` | "User 仓储接口实现,提供数据访问能力。" | `repo UserRepo` |
| `OrderRepo` | "Order 仓储接口实现,提供数据访问能力。" | `repo OrderRepo` |

**使用场景**:
```go
// NewGreeterUsecase 创建一个新的 Greeter 用例实例。
//
// 参数：
//   - logger: 日志记录器,用于记录业务日志。
//   - conf: 应用配置信息。
//   - repo: Greeter 仓储接口实现,提供数据访问能力。
//
// 返回：
//   - GreeterUsecase: Greeter 用例接口实现。
func NewGreeterUsecase(logger kitlog.Logger, conf *appconf.Config, repo GreeterRepo) GreeterUsecase {
    return &greeterUsecase{
        logger: logger,
        conf:   conf,
        repo:   repo,
    }
}
```

### 数据库相关

| 参数类型 | 标准表述 | 示例 |
|---------|---------|------|
| `*sql.DB` | "数据库连接实例。" | `db *sql.DB` |
| `*gorm.DB` | "GORM 数据库连接实例。" | `db *gorm.DB` |
| `*redis.Client` | "Redis 客户端实例。" | `rdb *redis.Client` |

**使用场景**:
```go
// NewGreeterRepo 创建一个新的 Greeter 仓储实例。
//
// 参数：
//   - logger: 日志记录器。
//   - db: 数据库连接实例。
//
// 返回：
//   - GreeterRepo: Greeter 仓储接口实现。
func NewGreeterRepo(logger kitlog.Logger, db *sql.DB) GreeterRepo {
    return &greeterRepo{
        logger: logger,
        db:     db,
    }
}
```

### HTTP 相关

| 参数类型 | 标准表述 | 示例 |
|---------|---------|------|
| `*http.Request` | "HTTP 请求对象。" | `req *http.Request` |
| `http.ResponseWriter` | "HTTP 响应写入器。" | `rw http.ResponseWriter` |
| `*GreeterRequest` | "Greeter 请求参数。" | `req *GreeterRequest` |
| `*GreeterResponse` | "Greeter 响应参数。" | `resp *GreeterResponse` |

**使用场景**:
```go
// SayHello 发送问候消息。
//
// 参数：
//   - ctx: 请求上下文,用于取消与超时控制。
//   - req: 问候请求参数,包含 Name 字段。
//
// 返回：
//   - *HelloReply: 问候响应,包含格式化的问候消息。
//   - error: 请求参数无效时返回错误,成功时返回 nil。
func (s *greeterService) SayHello(ctx context.Context, req *GreeterRequest) (*HelloReply, error) {
    // 实现代码。
}
```

### 字符串相关

| 参数类型 | 标准表述 | 示例 |
|---------|---------|------|
| `string` (ID) | "实体的唯一标识。" | `id string` |
| `string` (Name) | "实体的名称。" | `name string` |
| `string` (通用) | "字符串内容。" | `message string` |
| `[]string` | "字符串列表。" | `items []string` |

**使用场景**:
```go
// GetGreeter 根据 ID 获取 Greeter 实体。
//
// 参数：
//   - ctx: 请求上下文,用于取消与超时控制。
//   - id: Greeter 实体的唯一标识。
//
// 返回：
//   - *Greeter: 找到的 Greeter 实体,未找到时返回 nil。
//   - error: 数据库查询失败时返回错误,成功时返回 nil。
func (r *greeterRepo) GetGreeter(ctx context.Context, id string) (*Greeter, error) {
    // 实现代码。
}
```

### 接口相关

| 参数类型 | 标准表述 | 示例 |
|---------|---------|------|
| `GreeterRepo` | "Greeter 仓储接口。" | `repo GreeterRepo` |
| `GreeterUsecase` | "Greeter 用例接口。" | `uc GreeterUsecase` |
| `GreeterService` | "Greeter 服务接口。" | `svc GreeterService` |

**使用场景**:
```go
// NewGreeterUsecase 创建一个新的 Greeter 用例实例。
//
// 参数：
//   - logger: 日志记录器,用于记录业务日志。
//   - conf: 应用配置信息。
//   - repo: Greeter 仓储接口。
//
// 返回：
//   - GreeterUsecase: Greeter 用例接口实现。
func NewGreeterUsecase(logger kitlog.Logger, conf *appconf.Config, repo GreeterRepo) GreeterUsecase {
    return &greeterUsecase{
        logger: logger,
        conf:   conf,
        repo:   repo,
    }
}
```

## 常见动词标准表述

### 创建相关

| 操作 | 标准表述 | 示例 |
|------|---------|------|
| 创建 | "创建一个新的 {实体}。" | "创建一个新的 Greeter 实体。" |
| 初始化 | "初始化 {组件}。" | "初始化数据库连接。" |
| 构建 | "构建一个 {实体}。" | "构建一个查询条件。" |
| 组装 | "组装 {组件}。" | "组装 GreeterUsecase 的所有依赖。" |

**使用场景**:
```go
// CreateGreeter 创建一个新的 Greeter 实体。
//
// 参数：
//   - ctx: 请求上下文,用于取消与超时控制。
//   - g: 待创建的 Greeter 实体,Hello 字段不能为空。
//
// 返回：
//   - *Greeter: 创建成功的实体,包含生成的标识。
//   - error: 创建失败时返回错误,成功时返回 nil。
func (u *greeterUsecase) CreateGreeter(ctx context.Context, g *Greeter) (*Greeter, error) {
    // 实现代码。
}
```

### 查询相关

| 操作 | 标准表述 | 示例 |
|------|---------|------|
| 查找 | "根据 {条件} 查找 {实体}。" | "根据 ID 查找 Greeter 实体。" |
| 搜索 | "搜索符合 {条件} 的 {实体}。" | "搜索包含指定名称的 Greeter 实体。" |
| 获取 | "获取指定 {条件} 的 {实体}。" | "获取指定 ID 的 Greeter 实体。" |
| 查询 | "查询 {实体} 列表。" | "查询所有 Greeter 实体。" |

**使用场景**:
```go
// GetGreeter 获取指定 ID 的 Greeter 实体。
//
// 参数：
//   - ctx: 请求上下文,用于取消与超时控制。
//   - id: Greeter 实体的唯一标识。
//
// 返回：
//   - *Greeter: 找到的 Greeter 实体,未找到时返回 nil。
//   - error: 数据库查询失败时返回错误,成功时返回 nil。
func (r *greeterRepo) GetGreeter(ctx context.Context, id int64) (*Greeter, error) {
    // 实现代码。
}
```

### 修改相关

| 操作 | 标准表述 | 示例 |
|------|---------|------|
| 更新 | "更新一个 {实体}。" | "更新一个 Greeter 实体。" |
| 修改 | "修改 {实体} 的 {字段}。" | "修改 Greeter 实体的 Hello 字段。" |
| 设置 | "设置 {实体} 的 {字段}。" | "设置 Greeter 实体的 Hello 字段。" |

**使用场景**:
```go
// UpdateGreeter 更新一个 Greeter 实体。
//
// 参数：
//   - ctx: 请求上下文,用于取消与超时控制。
//   - g: 待更新的 Greeter 实体,ID 字段不能为空。
//
// 返回：
//   - *Greeter: 更新成功后的实体。
//   - error: 更新失败时返回错误,成功时返回 nil。
func (u *greeterUsecase) UpdateGreeter(ctx context.Context, g *Greeter) (*Greeter, error) {
    // 实现代码。
}
```

### 删除相关

| 操作 | 标准表述 | 示例 |
|------|---------|------|
| 删除 | "删除一个 {实体}。" | "删除一个 Greeter 实体。" |
| 移除 | "移除 {实体}。" | "移除指定的 Greeter 实体。" |

**使用场景**:
```go
// DeleteGreeter 删除一个 Greeter 实体。
//
// 参数：
//   - ctx: 请求上下文,用于取消与超时控制。
//   - id: Greeter 实体的唯一标识。
//
// 返回：
//   - error: 删除失败时返回错误,成功时返回 nil。
func (u *greeterUsecase) DeleteGreeter(ctx context.Context, id int64) error {
    // 实现代码。
}
```

### 保存相关

| 操作 | 标准表述 | 示例 |
|------|---------|------|
| 保存 | "保存一个 {实体}。" | "保存一个 Greeter 实体。" |
| 持久化 | "持久化 {实体}。" | "持久化 Greeter 实体到数据库。" |

**使用场景**:
```go
// Save 保存一个 Greeter 实体。
//
// 参数：
//   - ctx: 请求上下文,用于取消与超时控制。
//   - g: 待保存的 Greeter 实体。
//
// 返回：
//   - *Greeter: 保存成功后的实体,可能包含生成的 ID。
//   - error: 保存失败时返回错误,成功时返回 nil。
func (r *greeterRepo) Save(ctx context.Context, g *Greeter) (*Greeter, error) {
    // 实现代码。
}
```

## 常见返回值标准表述

### error 返回值

| 场景 | 标准表述 | 示例 |
|------|---------|------|
| 通用 | "失败时返回错误,成功时返回 nil。" | `error` |
| 参数无效 | "参数无效时返回错误,成功时返回 nil。" | `error` |
| 未找到 | "未找到时返回错误,成功时返回 nil。" | `error` |
| 数据库操作 | "数据库操作失败时返回错误,成功时返回 nil。" | `error` |
| 验证失败 | "字段验证失败时返回错误,验证通过返回 nil。" | `error` |

**使用场景**:
```go
// CreateGreeter 创建一个新的 Greeter 实体。
//
// 参数：
//   - ctx: 请求上下文,用于取消与超时控制。
//   - g: 待创建的 Greeter 实体,Hello 字段不能为空。
//
// 返回：
//   - *Greeter: 创建成功的实体,包含生成的标识。
//   - error: Hello 字段为空或数据库操作失败时返回错误,成功时返回 nil。
func (u *greeterUsecase) CreateGreeter(ctx context.Context, g *Greeter) (*Greeter, error) {
    // 实现代码。
}
```

### 实体返回值

| 场景 | 标准表述 | 示例 |
|------|---------|------|
| 创建成功 | "创建成功的实体,包含生成的标识。" | `*Greeter` |
| 更新成功 | "更新成功后的实体。" | `*Greeter` |
| 查找成功 | "找到的实体,未找到时返回 nil。" | `*Greeter` |
| 保存成功 | "保存成功后的实体,可能包含生成的 ID。" | `*Greeter` |

**使用场景**:
```go
// Save 保存一个 Greeter 实体。
//
// 参数：
//   - ctx: 请求上下文,用于取消与超时控制。
//   - g: 待保存的 Greeter 实体。
//
// 返回：
//   - *Greeter: 保存成功后的实体,可能包含生成的 ID。
//   - error: 保存失败时返回错误,成功时返回 nil。
func (r *greeterRepo) Save(ctx context.Context, g *Greeter) (*Greeter, error) {
    // 实现代码。
}
```

### bool 返回值

| 场景 | 标准表述 | 示例 |
|------|---------|------|
| 是否找到 | "是否找到了匹配的实体,true 表示找到,false 表示未找到。" | `bool` |
| 是否有效 | "字段是否有效,true 表示有效,false 表示无效。" | `bool` |
| 是否存在 | "实体是否存在,true 表示存在,false 表示不存在。" | `bool` |

**使用场景**:
```go
// FindGreeter 根据名称查找 Greeter 实体。
//
// 参数：
//   - ctx: 请求上下文,用于取消与超时控制。
//   - name: Greeter 实体的名称,用于精确匹配。
//
// 返回：
//   - *Greeter: 找到的 Greeter 实体,未找到时返回 nil。
//   - bool: 是否找到了匹配的实体,true 表示找到,false 表示未找到。
//   - error: 数据库查询失败时返回错误,成功时返回 nil。
func (r *greeterRepo) FindGreeter(ctx context.Context, name string) (*Greeter, bool, error) {
    // 实现代码。
}
```

## 使用原则

### 1. 全局一致性

**原则**: 相同类型和概念在整个项目中必须使用统一表述。

**错误示例**:
```go
// 文件1: greeter_repo.go
// 参数：
//   - ctx: 请求上下文对象。❌
//   - g: Greeter 对象。❌

// 文件2: user_repo.go
// 参数：
//   - ctx: 请求上下文,用于取消与超时控制。✅
//   - u: User 实体。✅
```

**正确示例**:
```go
// 文件1: greeter_repo.go
// 参数：
//   - ctx: 请求上下文,用于取消与超时控制。✅
//   - g: Greeter 实体。✅

// 文件2: user_repo.go
// 参数：
//   - ctx: 请求上下文,用于取消与超时控制。✅
//   - u: User 实体。✅
```

### 2. 参数优先

**原则**: 注释中必须先说明参数,再说明返回值。

**错误示例**:
```go
❌ 错误: 返回值在参数之前
// Save 保存一个 Greeter 实体。
//
// 返回：
//   - *Greeter: 保存成功后的实体,可能包含生成的 ID。
//   - error: 保存失败时返回错误,成功时返回 nil。
//
// 参数：❌ 返回值在参数之前
//   - ctx: 请求上下文,用于取消与超时控制。
//   - g: 待保存的 Greeter 实体。
func (r *greeterRepo) Save(ctx context.Context, g *Greeter) (*Greeter, error) {
    // 实现代码。
}
```

**正确示例**:
```go
✅ 正确: 参数在返回值之前
// Save 保存一个 Greeter 实体。
//
// 参数：
//   - ctx: 请求上下文,用于取消与超时控制。
//   - g: 待保存的 Greeter 实体。✅ 参数在前
//
// 返回：
//   - *Greeter: 保存成功后的实体,可能包含生成的 ID。
//   - error: 保存失败时返回错误,成功时返回 nil。
func (r *greeterRepo) Save(ctx context.Context, g *Greeter) (*Greeter, error) {
    // 实现代码。
}
```

### 3. 中文标点

**原则**: 所有注释语句必须以中文标点符号结束。

**错误示例**:
```go
❌ 错误: 缺少标点符号
// CreateGreeter 创建一个新的 Greeter 实体❌
//
// 参数：
//   - ctx: 请求上下文❌
//   - g: 待创建的 Greeter 实体❌
func CreateGreeter(ctx context.Context, g *Greeter) (*Greeter, error) {
    // 实现代码。
}
```

**正确示例**:
```go
✅ 正确: 使用标点符号
// CreateGreeter 创建一个新的 Greeter 实体。✅
//
// 参数：
//   - ctx: 请求上下文,用于取消与超时控制。✅
//   - g: 待创建的 Greeter 实体。✅
func CreateGreeter(ctx context.Context, g *Greeter) (*Greeter, error) {
    // 实现代码。
}
```

### 4. 专业准确

**原则**: 使用技术领域专业术语,避免口语化表达。

**错误示例**:
```go
❌ 错误: 口语化表达
// CreateGreeter 新建一个 Greeter 对象,把数据存到数据库里。❌ 口语化
//
// 参数：
//   - ctx: 上下文。❌ 过于简略
//   - g: Greeter 数据。❌ 表述不准确
func CreateGreeter(ctx context.Context, g *Greeter) (*Greeter, error) {
    // 实现代码。
}
```

**正确示例**:
```go
✅ 正确: 使用专业术语
// CreateGreeter 创建一个新的 Greeter 实体。✅ 专业准确
//
// 参数：
//   - ctx: 请求上下文,用于取消与超时控制。✅ 专业准确
//   - g: 待创建的 Greeter 实体,Hello 字段不能为空。✅ 专业准确
func CreateGreeter(ctx context.Context, g *Greeter) (*Greeter, error) {
    // 实现代码。
}
```

## 扩展术语表

**如何添加新术语**:

1. **识别新的类型或概念**: 当项目中出现新的类型或概念时
2. **定义标准表述**: 为该类型定义统一的描述格式
3. **添加到本表**: 将新术语添加到对应的章节
4. **全局应用**: 在整个项目中统一使用该表述

**示例**:

假设项目新增了 `Product` 实体:

1. 在"实体相关"章节添加:
   ```
   | `*Product` | "Product 实体。" | `p *Product` |
   ```

2. 在后续的函数注释中统一使用:
   ```go
   // SaveProduct 保存一个 Product 实体。
   //
   // 参数：
   //   - ctx: 请求上下文,用于取消与超时控制。
   //   - p: Product 实体。✅ 使用标准表述
   //
   // 返回：
   //   - *Product: 保存成功后的实体,可能包含生成的 ID。
   //   - error: 保存失败时返回错误,成功时返回 nil。
   func SaveProduct(ctx context.Context, p *Product) (*Product, error) {
       // 实现代码
   }
   ```

## 检查清单

使用以下清单检查术语使用是否符合规范:

- [ ] 参数说明使用标准术语表中的表述
- [ ] 返回值说明使用标准术语表中的表述
- [ ] 相同类型在不同文件中使用统一表述
- [ ] 所有注释语句以中文标点符号结束
- [ ] 注释使用专业术语,避免口语化表达
- [ ] 注释准确反映参数和返回值的实际用途
