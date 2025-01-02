# 函数和方法注释规范

## 概述

本文档定义了 Go 项目中函数和方法注释的规范要求。函数注释是 Go 代码文档的核心组成部分,所有函数（包括导出和非导出）都必须符合本规范。

## 标准格式

### 基本结构

所有函数和方法必须包含以下注释元素:

```go
// FunctionName 函数功能的简短描述（第一行,以句号结束）。
//
// 参数：
//   - paramName1: 参数1的用途说明。
//   - paramName2: 参数2的用途说明。
//
// 返回：
//   - returnType1: 返回值1的说明。
//   - error: 错误信息说明。
func FunctionName(paramName1 type1, paramName2 type2) (returnType1, error) {
    // 实现代码。
}
```

**格式要求**:
1. **功能描述**: 第一行,简短描述函数功能,以句号结束
2. **参数部分**: 如果有参数,必须说明每个参数的用途
3. **返回部分**: 如果有返回值,必须说明每个返回值的含义
4. **标准术语**: 参数和返回值的说明必须使用标准术语表
5. **中文标点**: 每行注释以中文标点符号结束

### 无参数函数

```go
// Init 初始化应用程序组件。
//
// 返回：
//   - error: 初始化失败时返回错误,成功时返回 nil。
func Init() error {
    // 实现代码。
}
```

### 无返回值函数

```go
// LogInfo 记录信息级别日志。
//
// 参数：
//   - message: 日志消息内容。
func LogInfo(message string) {
    // 实现代码。
}
```

### 多返回值函数

```go
// ParseGreeter 解析问候请求并返回实体。
//
// 参数：
//   - ctx: 请求上下文,用于取消与超时控制。
//   - req: 问候请求参数,包含 Name 字段。
//
// 返回：
//   - *Greeter: 解析后的问候实体,包含验证后的数据。
//   - error: 请求参数无效时返回错误,成功时返回 nil。
func ParseGreeter(ctx context.Context, req *GreeterRequest) (*Greeter, error) {
    // 实现代码。
}
```

### 方法注释

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

## 参数说明格式

### 标准格式

```
// 参数：
//   - paramName: 参数的用途说明。
```

**要求**:
- 参数说明必须以"参数："开头
- 每个参数单独一行,以 `- ` 开头
- 参数名和说明之间用冒号和空格分隔
- 说明必须以中文标点符号结束

### 常见参数标准表述

参见 [terminology_table.md](terminology_table.md) 中的"常见参数标准表述"部分。

**常用示例**:
- `context.Context` → "请求上下文,用于取消与超时控制。"
- `*Config` → "应用配置信息。"
- `kitlog.Logger` → "日志记录器。"
- `*Greeter` → "Greeter 实体。"

### 约束说明

如果参数有特定的约束或要求,必须在说明中明确指出:

```go
// CreateGreeter 创建一个新的 Greeter 实体。
//
// 参数：
//   - ctx: 请求上下文,用于取消与超时控制。
//   - g: 待创建的 Greeter 实体,Hello 字段不能为空。✅ 明确约束
//
// 返回：
//   - *Greeter: 创建成功的实体,包含生成的标识。
//   - error: Hello 字段为空时返回错误,成功时返回 nil。
func (u *greeterUsecase) CreateGreeter(ctx context.Context, g *Greeter) (*Greeter, error) {
    if "" == g.Hello {
        return nil, fmt.Errorf("Hello 字段不能为空")
    }
    // 实现代码。
}
```

## 返回值说明格式

### 标准格式

```
// 返回：
//   - returnType1: 返回值1的说明。
//   - error: 错误信息说明。
```

**要求**:
- 返回说明必须以"返回："开头
- 每个返回值单独一行,以 `- ` 开头
- 返回值类型和说明之间用冒号和空格分隔
- 说明必须以中文标点符号结束

### error 返回值标准表述

参见 [terminology_table.md](terminology_table_table.md) 中的"常见参数标准表述"部分。

**标准格式**:
- 失败时返回错误,成功时返回 nil。
- 参数无效时返回错误,成功时返回 nil。
- 数据库操作失败时返回错误,成功时返回 nil。

**示例**:
```go
// Save 保存一个 Greeter 实体。
//
// 参数：
//   - ctx: 请求上下文,用于取消与超时控制。
//   - g: 待保存的 Greeter 实体,ID 字段为 0 时自动生成。
//
// 返回：
//   - *Greeter: 保存成功后的实体,可能包含生成的 ID。
//   - error: 数据库操作失败时返回错误,成功时返回 nil。
```

### 多返回值说明

当函数返回多个值时,必须逐个说明:

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

## 命名动词标准表述

参见 [terminology_table.md](terminology_table.md) 中的"常见动词标准表述"部分。

**常用示例**:
- **创建**: "创建一个新的 {实体}。"
- **保存**: "保存一个 {实体}。"
- **查找**: "根据 {条件} 查找 {实体}。"
- **更新**: "更新一个 {实体}。"
- **删除**: "删除一个 {实体}。"

## 常见错误

### 错误 1: 缺少函数注释

**症状**: 函数声明前没有任何注释

**示例**:
```go
❌ 错误
func CreateGreeter(ctx context.Context, g *Greeter) (*Greeter, error) {
    // 实现代码。
}
```

**解决方案**: 添加完整的函数注释（功能描述 + 参数 + 返回值）

**优先级**: 🔴 高（严重影响代码文档的完整性）

### 错误 2: 参数说明不完整

**症状**: 仅有部分参数的说明,或参数说明过于简略

**示例**:
```go
❌ 错误: 参数说明过于简略
// CreateGreeter 创建 Greeter。
//
// 参数：
//   - ctx: 上下文。
//   - g: 实体。
func CreateGreeter(ctx context.Context, g *Greeter) (*Greeter, error) {
    // 实现代码。
}
```

**解决方案**: 为每个参数提供详细的用途说明

**优先级**: 🟠 中（影响代码文档的质量）

### 错误 3: 返回值说明不完整

**症状**: 仅有部分返回值的说明,或返回值说明过于简略

**示例**:
```go
❌ 错误: 返回值说明过于简略
// CreateGreeter 创建一个新的 Greeter 实体。
//
// 参数：
//   - ctx: 请求上下文,用于取消与超时控制。
//   - g: 待创建的 Greeter 实体,Hello 字段不能为空。
//
// 返回：
//   - *Greeter: 实体。
//   - error: 错误。❌ 过于简略
func CreateGreeter(ctx context.Context, g *Greeter) (*Greeter, error) {
    // 实现代码。
}
```

**解决方案**: 为每个返回值提供详细的含义说明

**优先级**: 🟠 中（影响代码文档的质量）

### 错误 4: 未使用标准术语

**症状**: 参数或返回值的说明未使用标准术语表

**示例**:
```go
❌ 错误: 未使用标准术语
// CreateGreeter 创建一个新的 Greeter 实体。
//
// 参数：
//   - ctx: 请求上下文对象。❌ 非标准表述
//   - g: Greeter 对象。❌ 非标准表述
//
// 返回：
//   - *Greeter: Greeter 对象。❌ 非标准表述
//   - error: 如果创建失败返回错误。❌ 非标准表述
func CreateGreeter(ctx context.Context, g *Greeter) (*Greeter, error) {
    // 实现代码。
}
```

**解决方案**: 使用 [terminology_table.md](terminology_table.md) 中的标准表述

**优先级**: 🟡 低（不影响规范符合性,但影响文档的一致性）

### 错误 5: 注释格式不正确

**症状**: 注释缺少"参数："或"返回："部分,或格式混乱

**示例**:
```go
❌ 错误: 格式混乱
// CreateGreeter 创建一个新的 Greeter 实体
// ctx: 请求上下文❌ 缺少"参数："部分
// g: 待创建的 Greeter 实体,Hello 字段不能为空
// 返回*Greeter 和 error❌ 格式不正确
func CreateGreeter(ctx context.Context, g *Greeter) (*Greeter, error) {
    // 实现代码。
}
```

**解决方案**: 按照"标准格式"章节修正格式

**优先级**: 🟠 中（影响代码文档的可读性）

### 错误 6: 注释未以标点结束

**症状**: 注释语句缺少中文标点符号

**示例**:
```go
❌ 错误: 缺少标点符号
// CreateGreeter 创建一个新的 Greeter 实体❌ 缺少句号
//
// 参数：
//   - ctx: 请求上下文❌ 缺少句号
//   - g: 待创建的 Greeter 实体❌ 缺少句号
func CreateGreeter(ctx context.Context, g *Greeter) (*Greeter, error) {
    // 实现代码。
}
```

**解决方案**: 为每个注释语句添加中文标点符号

**优先级**: 🟡 低（不影响规范符合性,但影响文档的专业性）

## 正确示例

### 示例 1: 简单函数

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

**适用场景**: 功能简单、参数和返回值明确的函数

### 示例 2: 复杂函数

```go
// CreateGreeter 创建一个新的 Greeter 实体并保存到数据库。
//
// 本方法会验证 Greeter 实体的字段约束,确保 Hello 字段不为空,
// 然后调用仓储接口保存数据。如果保存成功,会返回包含
// 生成的 ID 的实体。
//
// 参数：
//   - ctx: 请求上下文,用于取消与超时控制。
//   - g: 待创建的 Greeter 实体,Hello 字段不能为空,ID 字段会被忽略。
//
// 返回：
//   - *Greeter: 创建成功的实体,包含数据库生成的 ID 标识。
//   - error: Hello 字段为空或数据库操作失败时返回错误,成功时返回 nil。
func (u *greeterUsecase) CreateGreeter(ctx context.Context, g *Greeter) (*Greeter, error) {
    // 实现代码。
}
```

**适用场景**: 功能复杂、需要详细说明的函数

### 示例 3: 工厂函数

```go
// NewGreeterUsecase 创建一个新的 Greeter 用例实例。
//
// 本工厂函数会组装 GreeterUsecase 所需的所有依赖组件,
// 包括日志记录器、应用配置和仓储接口实现。
//
// 参数：
//   - logger: 日志记录器,用于记录业务日志。
//   - conf: 应用配置信息,包含数据库连接等配置。
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

**适用场景**: 工厂函数、构造函数

### 示例 4: 接口方法

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

**适用场景**: 接口方法实现（注释必须与接口定义完全一致,参见 [interface_rules.md](interface_rules.md)）

### 示例 5: 非导出函数

```go
// validateGreeter 验证 Greeter 实体的字段约束。
//
// 参数：
//   - g: 待验证的 Greeter 实体。
//
// 返回：
//   - error: 字段验证失败时返回错误,验证通过返回 nil。
func validateGreeter(g *Greeter) error {
    if "" == g.Hello {
        return fmt.Errorf("Hello 字段不能为空")
    }
    return nil
}
```

**适用场景**: 非导出函数（也必须包含注释）

## 特殊场景

### 可变参数函数

```go
// LogInfoWithFormat 记录格式化的信息级别日志。
//
// 参数：
//   - format: 日志格式化字符串。
//   - args: 格式化参数列表,用于填充 format。
func LogInfoWithFormat(format string, args ...interface{}) {
    // 实现代码。
}
```

### 泛型函数

```go
// FindByID 根据唯一标识查找实体。
//
// 参数：
//   - ctx: 请求上下文,用于取消与超时控制。
//   - id: 实体的唯一标识。
//
// 返回：
//   - T: 找到的实体,未找到时返回零值。
//   - bool: 是否找到了匹配的实体,true 表示找到,false 表示未找到。
//   - error: 数据库查询失败时返回错误,成功时返回 nil。
func FindByID[T any](ctx context.Context, id int64) (T, bool, error) {
    // 实现代码。
}
```

### 匿名函数

```go
type HandlerFunc func(ctx context.Context, req *Request) (*Response, error)

// HandleRequest 处理请求。
//
// 参数：
//   - ctx: 请求上下文,用于取消与超时控制。
//   - req: 请求数据。
//
// 返回：
//   - *Response: 响应数据。
//   - error: 处理失败时返回错误,成功时返回 nil。
var HandleRequest HandlerFunc = func(ctx context.Context, req *Request) (*Response, error) {
    // 实现代码。
}
```

## 函数体内注释规范

### 基本原则

函数体内的注释应该**解释"为什么"而非"是什么"**。

**注释时机**:
- ✅ 注释复杂业务逻辑的原因
- ✅ 注释特殊处理的原因
- ✅ 注释算法的关键步骤
- ❌ 不注释显而易见的代码
- ❌ 不过度注释简单逻辑

### 注释风格要求

1. **中文标点**: 每行函数体内的注释也必须以中文标点符号结束
2. **简洁明了**: 注释应该简短清晰,避免长篇大论
3. **位置正确**: 注释应该在被注释代码的上方,不放在右侧

### 正确示例

#### 示例 1: 业务逻辑验证

```go
// CreateGreeter 创建一个新的 Greeter 实体。
//
// 参数：
//   - ctx: 请求上下文,用于取消与超时控制。
//   - g: 待创建的 Greeter 实体,Hello 字段不能为空。
//
// 返回：
//   - *Greeter: 创建成功的实体,包含生成的标识。
//   - error: Hello 字段为空时返回错误,成功时返回 nil。
func (u *greeterUsecase) CreateGreeter(ctx context.Context, g *Greeter) (*Greeter, error) {
    // 验证字段约束,确保数据完整性。
    if "" == g.Hello {
        return nil, fmt.Errorf("Hello 字段不能为空")
    }

    // 调用仓储层持久化数据。
    greeter, err := u.repo.Save(ctx, g)
    if nil != err {
        return nil, fmt.Errorf("保存数据失败: %w", err)
    }

    return greeter, nil
}
```

#### 示例 2: 复杂查询逻辑

```go
// FindGreeterByName 根据名称查找 Greeter 实体。
//
// 参数：
//   - ctx: 请求上下文,用于取消与超时控制。
//   - name: Greeter 实体的名称,用于精确匹配。
//
// 返回：
//   - *Greeter: 找到的 Greeter 实体,未找到时返回 nil。
//   - bool: 是否找到了匹配的实体,true 表示找到,false 表示未找到。
//   - error: 数据库查询失败时返回错误,成功时返回 nil。
func (r *greeterRepo) FindGreeterByName(ctx context.Context, name string) (*Greeter, bool, error) {
    // 构建查询条件,添加索引字段优化查询性能。
    query := "SELECT id, hello FROM greeters WHERE name = ? LIMIT 1"

    // 执行数据库查询。
    row := r.db.QueryRowContext(ctx, query, name)

    var greeter Greeter
    if err := row.Scan(&greeter.ID, &greeter.Hello); nil != err {
        if errors.Is(err, sql.ErrNoRows) {
            // 未找到匹配记录。
            return nil, false, nil
        }
        // 查询执行失败。
        return nil, false, fmt.Errorf("查询数据库失败: %w", err)
    }

    // 查询成功,返回实体。
    return &greeter, true, nil
}
```

#### 示例 3: 数据转换逻辑

```go
// ToProto 将 Greeter 实体转换为 Proto 消息。
//
// 参数：
//   - g: Greeter 实体,包含完整的业务数据。
//
// 返回：
//   - *pb.Greeter: Proto 消息格式,用于 API 响应。
func (g *Greeter) ToProto() *pb.Greeter {
    // 转换为 Proto 格式,用于跨服务传输。
    return &pb.Greeter{
        Id:    g.ID,
        Hello: g.Hello,
    }
}
```

#### 示例 4: 错误处理和恢复

```go
// ProcessBatch 批量处理 Greeter 实体。
//
// 参数：
//   - ctx: 请求上下文,用于取消与超时控制。
//   - greeters: 待处理的 Greeter 实体列表。
//
// 返回：
//   - error: 部分或全部处理失败时返回错误,全部成功时返回 nil。
func (s *greeterService) ProcessBatch(ctx context.Context, greeters []*Greeter) error {
    var batchSize = 100

    // 分批处理,避免单次处理数据量过大。
    for i := 0; i < len(greeters); i += batchSize {
        end := i + batchSize
        if end > len(greeters) {
            end = len(greeters)
        }

        batch := greeters[i:end]

        // 并发处理批次内的实体,提高处理效率。
        if err := s.processBatch(ctx, batch); nil != err {
            // 批次处理失败,记录错误但不中断整个处理流程。
            kitlog.Errorf("处理批次 %d-%d 失败: %v", i, end, err)
            continue
        }
    }

    return nil
}
```

### 错误示例

#### 错误 1: 注释显而易见的代码

```go
❌ 错误: 注释过于简单,没有提供额外信息
func (g *Greeter) GetHello() string {
    // 返回 Hello 字段。❌ 过于简单,没有提供额外价值
    return g.Hello
}

✅ 正确: 如果代码显而易见,不需要注释
func (g *Greeter) GetHello() string {
    return g.Hello
}
```

#### 错误 2: 注释放在代码右侧

```go
❌ 错误: 注释应该放在代码上方
func (g *Greeter) ToProto() *pb.Greeter {
    return &pb.Greeter{ // 转换为 Proto 格式 ❌ 位置不正确
        Id:    g.ID,
        Hello: g.Hello,
    }
}

✅ 正确: 注释放在代码上方
func (g *Greeter) ToProto() *pb.Greeter {
    // 转换为 Proto 格式,用于跨服务传输。✅ 位置正确
    return &pb.Greeter{
        Id:    g.ID,
        Hello: g.Hello,
    }
}
```

#### 错误 3: 注释缺少标点符号

```go
❌ 错误: 注释缺少中文标点符号
func (g *Greeter) ToProto() *pb.Greeter {
    // 转换为 Proto 格式 ❌ 缺少句号
    return &pb.Greeter{
        Id:    g.ID,
        Hello: g.Hello,
    }
}

✅ 正确: 注释以中文标点符号结束
func (g *Greeter) ToProto() *pb.Greeter {
    // 转换为 Proto 格式,用于跨服务传输。✅ 有句号
    return &pb.Greeter{
        Id:    g.ID,
        Hello: g.Hello,
    }
}
```

## 检查清单

使用以下清单检查函数注释是否符合规范:

### 函数签名注释
- [ ] 所有函数都有功能描述注释
- [ ] 参数说明完整,每个参数都有用途说明
- [ ] 返回值说明完整,每个返回值都有含义说明
- [ ] 参数说明使用标准术语表
- [ ] 返回值说明使用标准术语表
- [ ] 注释语句以中文标点符号结束
- [ ] 注释准确反映函数功能
- [ ] 注释使用专业术语
- [ ] 接口实现方法注释与接口定义一致

### 函数体内注释
- [ ] 注释解释"为什么"而非"是什么"
- [ ] 注释复杂业务逻辑和特殊处理
- [ ] 注释简洁明了,不过度注释
- [ ] 注释放在代码上方,不放在右侧
- [ ] 每行注释以中文标点符号结束

## 与接口方法注释的关系

**重要**: 实现接口的方法,其注释必须与接口定义**完全一致**。

详细规则参见 [interface_rules.md](interface_rules.md)。

**基本要求**:
- 实现方法的注释应该完全复制接口定义的注释
- 不要在实现方法中添加额外的解释
- 如果接口定义缺少注释,先为接口添加注释

**示例**:

**接口定义**:
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
type GreeterRepo interface {
    Save(ctx context.Context, g *Greeter) (*Greeter, error)
}
```

**正确实现**:
```go
// Save 保存一个 Greeter 实体。✅ 与接口定义完全一致
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

**错误实现**:
```go
// Save 实现 GreeterRepo 接口,保存数据到数据库。❌ 添加了额外解释
func (r *greeterRepo) Save(ctx context.Context, g *Greeter) (*Greeter, error) {
    // 实现代码。
}
```
