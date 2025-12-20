# Kratos Layout 项目 AI 协作规范

> **版本**: 1.2.0  
> **最后更新**: 2025年12月26日  
> **适用范围**: 所有 AI 助手（Claude、GitHub Copilot、ChatGPT 等）  
> **项目类型**: Go 微服务框架（基于 Kratos）

本文档定义了在 Kratos Layout 项目中进行 AI 辅助开发时必须遵守的规则、规范和最佳实践。所有 AI 助手在参与本项目开发时，必须严格遵循本文档中的所有规范。

---

## 📚 目录

1. [关键约束](#关键约束)
2. [项目概览](#项目概览)
3. [核心思维模式](#核心思维模式)
4. [代码规范](#代码规范)
5. [注释规范](#注释规范)
6. [注释自检流程](#注释自检流程)
7. [包导入规范](#包导入规范)
8. [开发流程](#开发流程)
9. [自检清单](#自检清单)

---

## 关键约束

### 强制要求

| 约束类型 | 要求 | 说明 |
|---------|------|------|
| **语言** | 所有回复必须使用中文 | 包括代码注释、文档、交互说明 |
| **依赖版本** | 以 `go.mod` 为准 | 不在文档中硬编码具体版本号 |
| **生成代码** | 非必要不手动修改 | `*.pb.go`、`wire_gen.go` 等文件优先通过工具重新生成 |

### 版本控制规范

- ✅ Git 操作由人工负责，AI 不直接执行
- ✅ AI 可建议用户进行 Git 操作，但不执行 `git add`、`commit`、`push` 等命令
- ✅ 提交前确保代码通过 `make lint` 检查

### 生成代码管理

**基本原则**：
- ✅ `*.pb.go`、`wire_gen.go` 等文件由工具自动生成
- ✅ 修改 Proto 文件后运行 `make api` 重新生成
- ✅ 修改 Wire 配置后运行 `make generate` 重新生成
- ⚠️ 非必要情况下不手动修改生成的代码文件

**允许手动修改的情况**：
- 工具生成的代码存在明显错误，且无法通过修改源文件解决
- 需要添加临时调试代码（调试完成后应移除）
- 用户明确要求进行特定修改

**修改后的处理**：
- 手动修改后需在注释中说明修改原因
- 后续重新生成时需注意保留或重新应用手动修改

### 代码生成命令

| 命令 | 用途 |
|------|------|
| `make api` | 生成 Protocol Buffers 代码 |
| `make config` | 生成配置相关代码 |
| `make validate` | 生成验证代码 |
| `make generate` | 执行 Wire 依赖注入代码生成 |

---

## 项目概览

### 基本信息

| 属性 | 值 |
|------|-----|
| **项目名称** | Kratos Layout |
| **项目类型** | Go 微服务框架模板 |
| **Go 版本** | 1.25+（以 `go.mod` 为准） |
| **核心框架** | [go-kratos/kratos](https://github.com/go-kratos/kratos) v2 |
| **依赖注入** | [google/wire](https://github.com/google/wire) |
| **模块路径** | `github.com/fsyyft-go/kratos-layout` |

### 项目架构

```
kratos-layout/
├── api/                    # Protocol Buffers API 定义
│   ├── helloworld/v1/      # API 版本化目录
│   │   ├── *.proto         # Proto 定义文件
│   │   └── *.pb.go         # 生成的 Go 代码（禁止手动修改）
│   └── third_party/        # 第三方 proto 依赖
├── cmd/                    # 应用程序入口
│   ├── task/               # 定时任务应用入口
│   │   └── main.go
│   └── web/                # Web 服务应用入口
│       └── main.go
├── configs/                # 配置文件目录
├── internal/               # 内部实现（不对外暴露）
│   ├── app/                # 应用层（Wire 组装）
│   │   ├── task/           # 定时任务 Wire 配置
│   │   └── web/            # Web 服务 Wire 配置
│   ├── biz/                # 业务逻辑层（Usecase）
│   ├── data/               # 数据访问层（Repository）
│   ├── domain/             # 领域模型
│   ├── pkg/                # 内部公共包
│   │   ├── conf/           # 配置定义
│   │   └── log/            # 日志配置
│   ├── server/             # 服务器实现
│   ├── service/            # 服务层（API 实现）
│   └── task/               # 定时任务实现
├── pkg/                    # 外部可用公共包
└── scripts/                # 脚本工具
```

### 核心技术栈

| 类别 | 技术 |
|------|------|
| **编程语言** | Go 1.25+ |
| **微服务框架** | Kratos v2 |
| **依赖注入** | Wire |
| **API 协议** | Protocol Buffers / gRPC / HTTP |
| **配置管理** | Protobuf 定义 + YAML 文件 |
| **日志框架** | fsyyft-go/kit/log |
| **参数验证** | protoc-gen-validate |
| **代码检查** | golangci-lint |

### 分层架构说明

| 层级 | 目录 | 职责 |
|------|------|------|
| **表现层** | `internal/service/` | 实现 API 接口，处理请求响应 |
| **业务层** | `internal/biz/` | 实现业务用例，定义仓储接口 |
| **数据层** | `internal/data/` | 实现仓储接口，数据访问 |
| **领域层** | `internal/domain/` | 定义领域模型和实体 |
| **基础设施** | `internal/server/` | 服务器配置和中间件 |

---

## 核心思维模式

### 基本原则

AI 助手在处理任务时必须遵循以下原则：

| 原则 | 要求 |
|------|------|
| **深度优先** | 追求深度分析而非表面广度，寻求本质洞察 |
| **创新思维** | 突破常规模式，寻找创新解决方案 |
| **严谨验证** | 多角度验证和优化方案，确保完整性 |
| **资源最大化** | 充分利用计算能力和上下文信息 |

### 思维方式

**必须采用的思维方式**：

| 思维方式 | 说明 |
|---------|------|
| **系统思维** | 从整体架构到具体实现的立体思考 |
| **辩证思维** | 权衡多种解决方案的利弊 |
| **创造性思维** | 突破常规，寻找创新方案 |
| **批判性思维** | 多角度验证和优化 |

### 思维平衡要求

| 平衡维度 | 说明 |
|---------|------|
| 分析与直觉 | 数据驱动分析与经验直觉相结合 |
| 细节与全局 | 细节检查与整体架构视角并重 |
| 理论与实践 | 理论理解与实际应用相统一 |
| 深度与效率 | 深度思考与执行效率相平衡 |

### 思维过程规范

**`<think>` 标签使用要求**：

AI 助手在处理复杂问题时，应使用 `<think>` 标签展示思维过程：

```
<think>
1. 问题分析
   - 识别核心问题：[具体问题]
   - 确定约束条件：[约束列表]
   - 评估影响范围：[影响分析]

2. 方案设计
   - 方案 A：[方案描述] - 优点/缺点
   - 方案 B：[方案描述] - 优点/缺点
   - 选择理由：[决策依据]

3. 实现计划
   - 步骤 1：[具体操作]
   - 步骤 2：[具体操作]
   - 预期结果：[结果描述]
</think>
```

**使用场景**：
- ✅ 复杂架构设计决策
- ✅ 多方案比较选择
- ✅ 问题诊断和排查
- ✅ 重构方案制定
- ❌ 简单的代码修改（无需展示思维过程）
- ❌ 直接的问题回答（无需展示思维过程）

### 分析深度控制

| 问题类型 | 分析深度 | 判定标准 | 说明 |
|---------|---------|---------|------|
| 复杂架构问题 | 深入分析 | 涉及 3 个以上模块，或需要修改核心接口 | 全面评估影响范围和方案可行性 |
| 常规功能实现 | 适度分析 | 涉及 1-2 个模块，接口变更范围可控 | 确认需求后高效执行 |
| 简单修改任务 | 简洁处理 | 单文件修改，无接口变更 | 快速完成，避免过度分析 |

### 解决方案流程

```
1. 初步理解
   ├── 重述技术需求，确认理解正确
   ├── 识别关键技术点和约束条件
   ├── 考虑更广泛的上下文和影响
   └── 映射已知信息和待确认信息

2. 问题分析
   ├── 将任务分解为可管理的组件
   ├── 确定功能需求和非功能需求
   ├── 识别技术约束和业务约束
   └── 定义可衡量的成功标准

3. 方案设计
   ├── 考虑多种实现路径并比较
   ├── 评估架构方法的优劣
   ├── 选择最优方案并说明理由
   └── 逐步细化实现细节

4. 实现验证
   ├── 验证方案是否满足需求
   ├── 检查代码是否符合规范
   ├── 确保错误处理完整
   └── 验证与现有代码的兼容性
```

### 输出要求

**响应格式标准**：

| 要求 | 说明 |
|------|------|
| 使用 Markdown 格式 | 便于阅读和渲染 |
| 保持简洁 | 使用最少词语表达清晰含义 |
| 概念解释要透彻 | 复杂概念需要完整说明 |
| 避免过度使用列表 | 除非明确要求 |

**代码输出标准**：

| 要求 | 说明 |
|------|------|
| 展示完整上下文 | 确保代码可理解和可维护 |
| 仅显示必要修改 | 不修改与请求无关的代码 |
| 包含路径和语言标识 | 格式：`` ```go:path/to/file.go `` |
| 确保导入可见 | 显示所有必要的 import 语句 |
| 禁止使用占位符 | 不使用 `...` 或 `// 省略` 代替实际代码 |

### 禁止行为

| 禁止行为 | 说明 |
|---------|------|
| 使用未验证依赖 | 所有依赖必须在 `go.mod` 中声明 |
| 留下不完整功能 | 功能必须完整实现 |
| 包含未测试代码 | 代码必须可测试 |
| 使用过时方案 | 采用当前最佳实践 |
| 跳过代码部分 | 不使用省略号代替代码 |
| 修改无关代码 | 严格限定修改范围 |
| 手动修改生成文件 | `*.pb.go`、`wire_gen.go` 等禁止手动编辑 |

---

## 代码规范

### 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| **包名** | 小写单词，不使用下划线 | `server`、`biz`、`conf` |
| **文件名** | 小写单词，下划线分隔 | `wire_gen.go`、`error_reason.go` |
| **接口名** | 大驼峰，通常以 `er` 结尾 | `GreeterRepo`、`WebServer` |
| **结构体名** | 大驼峰（导出）或小驼峰（非导出） | `Greeter`、`greeterUsecase` |
| **方法名** | 大驼峰（导出）或小驼峰（非导出） | `CreateGreeter`、`save` |
| **常量名** | 大驼峰（导出）或小驼峰（非导出） | `ErrUserNotFound`、`meterName` |
| **变量名** | 小驼峰 | `logger`、`conf`、`repo` |

### 错误处理规范

**错误定义**：

```go
// ✅ 正确示例：在 biz 层定义业务错误。
var (
    // ErrUserNotFound 表示用户未找到的错误。
    ErrUserNotFound = errors.NotFound(
        apphelloworldv1.ErrorReason_USER_NOT_FOUND.String(),
        "user not found",
    )
)

// ❌ 错误示例：使用泛化的错误描述
var (
    ErrNotFound = errors.NotFound("NOT_FOUND", "not found")  // 过于泛化
)
```

**错误处理**：

```go
// ✅ 正确示例：检查错误并添加上下文信息。
result, err := someFunction()
if err != nil {
    // 添加上下文信息后返回，保持错误链。
    return fmt.Errorf("执行某操作失败: %w", err)
}

// ✅ 正确示例：区分错误类型进行处理。
user, err := repo.GetUser(ctx, userID)
if err != nil {
    if errors.Is(err, ErrUserNotFound) {
        // 用户不存在，返回特定业务错误。
        return nil, ErrUserNotFound
    }
    // 其他错误，包装后返回。
    return nil, fmt.Errorf("获取用户信息失败: %w", err)
}

// ❌ 错误示例：忽略错误。
result, _ := someFunction()  // 禁止忽略错误

// ❌ 错误示例：丢失错误链。
if err != nil {
    return fmt.Errorf("操作失败: %s", err.Error())  // 丢失了原始错误
}
```

### 接口设计规范

**接口定义位置**：

| 接口类型 | 定义位置 | 说明 |
|---------|---------|------|
| 仓储接口（Repository） | `internal/biz/` | 数据访问抽象 |
| 用例接口（Usecase） | `internal/biz/` | 业务逻辑抽象 |
| 服务器接口 | `internal/server/` | 服务器行为抽象 |

**接口实现验证**：

```go
// ✅ 正确示例：使用类型断言确保结构体实现了接口。
var _ GreeterUsecase = (*greeterUsecase)(nil)
var _ WebServer = (*webServer)(nil)

// ❌ 错误示例：缺少接口实现验证
// 不添加类型断言，可能导致编译时无法发现接口未完全实现
```

**接口设计原则**：

```go
// ✅ 正确示例：接口职责单一，方法数量适中。
type (
    // GreeterRepo 定义了 Greeter 仓储接口。
    GreeterRepo interface {
        // Save 保存一个 Greeter 实体。
        Save(ctx context.Context, g *Greeter) (*Greeter, error)
        // FindByID 根据 ID 查询 Greeter 实体。
        FindByID(ctx context.Context, id int64) (*Greeter, error)
    }
)

// ❌ 错误示例：接口过于庞大，职责不清。
type (
    // Repository 数据仓储接口（职责过于宽泛）。
    Repository interface {
        SaveGreeter(ctx context.Context, g *Greeter) error
        SaveUser(ctx context.Context, u *User) error
        SaveOrder(ctx context.Context, o *Order) error
        // ... 过多方法
    }
)
```

### Wire 依赖注入规范

**ProviderSet 定义**：

```go
// ✅ 正确示例：每个包提供一个 ProviderSet。
var ProviderSet = wire.NewSet(
    NewGreeterUsecase,
    NewGreeterRepo,
)

// ❌ 错误示例：ProviderSet 定义在错误的位置
// 不应在 main 包中定义 ProviderSet
```

**构造函数签名**：

```go
// ✅ 正确示例：构造函数返回接口类型，便于测试和替换。
func NewGreeterUsecase(
    logger kitlog.Logger,
    conf *appconf.Config,
    repo GreeterRepo,
) GreeterUsecase {
    return &greeterUsecase{
        logger: logger,
        conf:   conf,
        repo:   repo,
    }
}

// ❌ 错误示例：构造函数返回具体类型
func NewGreeterUsecase(
    logger kitlog.Logger,
    conf *appconf.Config,
    repo GreeterRepo,
) *greeterUsecase {  // 应返回接口类型
    return &greeterUsecase{
        logger: logger,
        conf:   conf,
        repo:   repo,
    }
}
```

**Wire 文件组织**：

```go
// ✅ 正确示例：wire.go 文件结构
//go:build wireinject
// +build wireinject

package web

import (
    "github.com/google/wire"

    // 导入所需的包...
)

// initApp 初始化应用程序。
func initApp(confPath string) (*kratos.App, func(), error) {
    panic(wire.Build(
        // 按层级组织 ProviderSet
        appconf.ProviderSet,    // 配置层
        applog.ProviderSet,     // 日志层
        data.ProviderSet,       // 数据层
        biz.ProviderSet,        // 业务层
        service.ProviderSet,    // 服务层
        server.ProviderSet,     // 服务器层
        newApp,                 // 应用构造
    ))
}
```

---

## 注释规范

### 注释语言规范

| 规范 | 要求 |
|------|------|
| **语言** | 使用标准现代汉语书面表达 |
| **语法** | 确保语句语法正确，符合汉语表达习惯 |
| **术语** | 使用技术领域专业术语，避免口语化表达 |
| **标点** | 每个注释语句以中文标点符号结束 |
| **一致性** | 相同语义的概念使用统一的注释表述 |

### 包级别注释

**强制要求**：
- 每个包必须在独立的 `doc.go` 文件中编写包级别注释
- `doc.go` 文件仅包含版权声明、包注释和 `package` 声明，不包含任何代码实现
- 除 `doc.go` 外的所有文件，`package` 声明前后不得有任何注释

**doc.go 文件格式**：

```go
// Copyright 2025 fsyyft-go
//
// Licensed under the MIT License. See LICENSE file in the project root for full license information.

// Package server 提供 HTTP 和 gRPC 服务器的实现。
//
// 本包包含服务器的初始化、配置和中间件设置功能，
// 支持基于 Kratos 框架的 Web 服务开发。
//
// 主要组件：
//   - HTTP 服务器（基于 Kratos HTTP）
//   - 中间件集成（日志、跟踪、恢复等）
//   - 依赖注入提供者（Wire ProviderSet）
//
// 使用示例：
//
//	srv := server.NewWebServer(logger, conf, greeter)
//	if err := srv.Start(ctx); err != nil {
//	    log.Fatal(err)
//	}
package server
```

**其他 Go 文件格式**：

```go
// Copyright 2025 fsyyft-go
//
// Licensed under the MIT License. See LICENSE file in the project root for full license information.

package server

import (
    // ...
)

// 代码实现...
```

### 类型定义注释

**接口定义**：

```go
type (
    // GreeterRepo 定义了 Greeter 仓储接口。
    // 该接口提供了对 Greeter 实体的基础操作方法，包括保存、更新、查询等功能。
    GreeterRepo interface {
        // Save 保存一个 Greeter 实体。
        // 参数：
        //   - ctx：请求上下文，用于取消与超时控制。
        //   - g：待保存的 Greeter 实体。
        //
        // 返回值：
        //   - *Greeter：保存成功后的实体（可能包含生成的 ID）。
        //   - error：保存失败时返回错误，成功时返回 nil。
        Save(ctx context.Context, g *Greeter) (*Greeter, error)
    }
)
```

**结构体定义**：

```go
type (
    // greeterUsecase 实现了 GreeterUsecase 接口。
    greeterUsecase struct {
        // logger 用于记录日志信息。
        logger kitlog.Logger
        // conf 存储应用配置信息。
        conf *appconf.Config
        // repo 提供数据访问能力。
        repo GreeterRepo
    }
)
```

### 函数和方法注释

**标准格式**：

```go
// CreateGreeter 创建一个新的 Greeter 实体。
// 参数：
//   - ctx：请求上下文，用于取消与超时控制。
//   - g：待创建的 Greeter 实体，Hello 字段不能为空。
//
// 返回值：
//   - *Greeter：创建成功的实体，包含生成的标识。
//   - error：创建失败时返回错误，成功时返回 nil。
func (u *greeterUsecase) CreateGreeter(ctx context.Context, g *Greeter) (*Greeter, error) {
    // 记录调试日志。
    u.logger.Debug("CreateGreeter: %v", g.Hello)

    // 调用仓储层保存实体。
    return u.repo.Save(ctx, g)
}
```

**注释要点**：

| 要点 | 说明 |
|------|------|
| **功能描述** | 第一行简洁说明函数用途 |
| **参数说明** | 每个参数的类型、含义、约束条件 |
| **返回值说明** | 每个返回值的类型、含义、可能的值 |
| **接口一致性** | 实现接口的方法注释必须与接口定义完全一致 |

### 函数体内注释

**业务逻辑注释**：

```go
func (u *greeterUsecase) CreateGreeter(ctx context.Context, g *Greeter) (*Greeter, error) {
    // 验证输入参数的有效性。
    if g == nil {
        return nil, errors.New("greeter 不能为空")
    }

    // 检查 Hello 字段是否为空。
    if strings.TrimSpace(g.Hello) == "" {
        return nil, errors.New("Hello 字段不能为空")
    }

    // 记录创建操作的调试日志。
    u.logger.Debug("开始创建 Greeter: %v", g.Hello)

    // 调用仓储层保存实体到数据库。
    result, err := u.repo.Save(ctx, g)
    if err != nil {
        // 保存失败，返回包含上下文的错误信息。
        return nil, fmt.Errorf("保存 Greeter 失败: %w", err)
    }

    // 返回创建成功的实体。
    return result, nil
}
```

**注释原则**：

| 原则 | 说明 |
|------|------|
| **关键步骤** | 为业务逻辑的关键步骤编写前置注释 |
| **复杂逻辑** | 复杂条件判断、循环、递归需要逻辑说明 |
| **数据处理** | 数据转换、计算的关键变量需要说明 |
| **前置注释** | 优先使用独立行的前置注释 |
| **标点结束** | 每条注释以中文标点符号结束 |

**"关键步骤"判定标准**：
- 业务决策点（影响流程走向的判断）
- 数据转换点（格式转换、类型转换）
- 外部调用点（调用其他服务、数据库操作）
- 状态变更点（修改对象状态、缓存更新）

**"复杂条件"判定标准**：
- 2 层以上的嵌套条件（`if` 中嵌套 `if`）
- 3 个以上的条件组合（使用 `&&` 或 `||` 连接）
- 涉及位运算或特殊逻辑的条件

### 行内注释规范

**仅在必要时使用行内注释，优先使用前置注释**：

```go
// ✅ 正确示例：前置注释（推荐）
// 计算平均响应时间（毫秒）。
avgResponseTime := sum(responseTimes) / len(responseTimes)

// ✅ 可接受：必要的行内注释
total := calculateTotal(items)  // 包含税费的总金额。
config := loadConfig(path)      // 从默认路径加载用户配置。

// ❌ 错误示例：不必要的行内注释
count := len(items)             // 获取元素数量
result := process(data)         // 处理数据并返回结果

// ❌ 错误示例：行内注释未以标点结束
total := calculateTotal(items)  // 包含税费的总金额
config := loadConfig(path)      // 从默认路径加载用户配置
```

**行内注释使用原则**：
- ✅ 仅用于解释复杂或非直观的逻辑
- ✅ 注释内容简洁明了，必须以标点结束
- ✅ 与代码保持适当距离（至少两个空格）
- ❌ 不用于解释显而易见的代码
- ❌ 不用于重复代码已表达的信息

### 条件分支注释

**复杂条件判断需要说明判断逻辑**：

```go
// ✅ 正确示例：清晰的条件说明
// 如果为根节点（dep == 0），计算百分比并输出信息。
if dep == 0 {
    per := smt / csmt * 100

    // 格式化输出消息。
    msg := fmt.Sprintf("%3d 任务: %s [%3.2f%% %3.2f %3.2f] %s\n", idx, taskID, per, smt, csmt, info.Title)
    // 根据完成度阈值着色输出。
    if csmt >= 8 {
        if per >= 60 {
            // 完成度高于 60%，使用黄色高亮。
            msg = color.HiYellowString(msg)
        } else if per <= 30 {
            // 完成度低于 30%，使用青色提示。
            msg = color.HiCyanString(msg)
        }
    }

    fmt.Print(msg)
}

// ❌ 错误示例：缺少条件说明
if dep == 0 {
    per := smt / csmt * 100
    msg := fmt.Sprintf("%3d 任务: %s [%3.2f%% %3.2f %3.2f] %s\n", idx, taskID, per, smt, csmt, info.Title)
    if csmt >= 8 {
        if per >= 60 {
            msg = color.HiYellowString(msg)
        } else if per <= 30 {
            msg = color.HiCyanString(msg)
        }
    }
    fmt.Print(msg)
}
```

### 循环和递归注释

**循环和递归逻辑需要说明处理目的**：

```go
// ✅ 正确示例：说明循环目的
// 递归处理当前任务的子任务列表。
if info.CurrentChildren != nil {
    for _, child := range info.CurrentChildren {
        childCount++
        // 递归计算子任务的时间消耗。
        totalTime += m.calculateTaskTime(ctx, child.ID, idx, dep+1)
    }
}
// 递归处理已转移的子任务列表。
if info.TransferredChildren != nil {
    for _, child := range info.TransferredChildren {
        childCount++
        // 递归计算转移子任务的时间消耗。
        totalTime += m.calculateTaskTime(ctx, child.ID, idx, dep+1)
    }
}

// ❌ 错误示例：缺少循环说明
if info.CurrentChildren != nil {
    for _, child := range info.CurrentChildren {
        childCount++
        totalTime += m.calculateTaskTime(ctx, child.ID, idx, dep+1)
    }
}
if info.TransferredChildren != nil {
    for _, child := range info.TransferredChildren {
        childCount++
        totalTime += m.calculateTaskTime(ctx, child.ID, idx, dep+1)
    }
}
```

### 错误处理注释

**错误处理需要说明处理逻辑**：

```go
// ✅ 正确示例：说明错误处理
// 检查上下文是否已取消，如果已取消则立即返回。
if ctx.Err() != nil {
    return 0
}

// 获取任务详细信息。
info, err := taskService.GetTaskInfo(ctx, taskID)
if err != nil {
    // 获取任务信息失败，记录错误并返回默认值。
    fmt.Printf("错误：获取任务 %s 失败: %s\n", taskID, err)
    return 0
}

// 提取并规范化任务短标识。
shortID := strings.TrimSpace(info.ShortID)
if shortID == "" {
    // 任务短标识为空，使用原始 ID 作为替代。
    shortID = taskID
}

// ❌ 错误示例：缺少错误处理说明
if ctx.Err() != nil {
    return 0
}
info, err := taskService.GetTaskInfo(ctx, taskID)
if err != nil {
    fmt.Printf("错误：%s %s\n", taskID, err)
    return 0
}
shortID := strings.TrimSpace(info.ShortID)
if shortID == "" {
    shortID = taskID
}
```

### 禁止的注释风格

**以下注释风格禁止出现**：

```go
// ❌ 错误：在非 doc.go 文件中添加包级别注释
// Package mywork 提供任务处理功能。
package mywork

// ❌ 错误：缺少 doc.go 文件
// 包下没有 doc.go 文件，但包含多个源文件

// ❌ 错误：doc.go 文件中包含代码实现
// Package mywork 提供任务处理功能。
package mywork

var globalVar = "value"  // doc.go 不应包含代码实现

// ❌ 错误：注释未以标点结束
// 这是一个示例函数
func example() {}

// ❌ 错误：口语化表达
// 这里我们要做的是把数据转换一下
data := transform(input)

// ❌ 错误：过于简略，无实际意义
// 处理
process()

// ❌ 错误：注释与代码不一致
// 获取用户信息
task := getTask(id)  // 实际是获取任务信息

// ❌ 错误：使用英文注释（除非是专有名词）
// Get user information
user := getUser(id)

// ❌ 错误：重复代码信息，无额外价值
// 调用 fmt.Println 打印消息
fmt.Println("message")

// ❌ 错误：非导出函数缺少注释
func processData(data []byte) error {
    // ...
}

// ❌ 错误：实现接口的方法注释与接口不一致
// 执行任务（接口定义为"运行指定的任务"）
func (m *myWork) Run(ctx context.Context, taskName string) error {
    // ...
}

// ❌ 错误：全局相同语义的注释表述不一致
// ctx 上下文对象
func foo(ctx context.Context) error { }
// ctx 请求上下文，用于取消与超时控制
func bar(ctx context.Context) error { }
```

| 禁止风格 | 原因 |
|---------|------|
| 非 doc.go 文件中的包注释 | 违反包注释集中管理原则 |
| 注释未以标点结束 | 违反中文书写规范 |
| 口语化表达 | 不符合技术文档专业性要求 |
| 过于简略 | 无法提供有效信息 |
| 注释与代码不一致 | 误导代码阅读者 |
| 无额外价值的注释 | 增加代码噪音 |
| 非导出函数缺少注释 | 影响代码可维护性 |
| 实现方法注释与接口不一致 | 造成理解混乱 |

### 标准注释术语表

为保证注释一致性，以下常见参数使用统一表述：

| 参数类型 | 标准表述 |
|---------|---------|
| `context.Context` | "请求上下文，用于取消与超时控制。" |
| `*Config` | "应用配置信息。" |
| `Logger` | "日志记录器。" |
| `error` 返回值 | "失败时返回错误，成功时返回 nil。" |

---

## 包导入规范

### 导入格式

**强制要求**：
- 所有 `import` 语句必须使用括号 `()` 包裹
- 按段分组，段与段之间使用空行分隔
- 每个段内的包按字母顺序排序

### 分段规则

| 段落 | 内容 | 别名要求 |
|------|------|---------|
| **第一段** | Go 标准库 | 无需别名 |
| **第二段** | 第三方包（github.com 等） | 按需取别名 |
| **第三段** | fsyyft-go 相关包 | **强制**使用 `kit` 前缀别名 |
| **第四段** | 项目内部包 | **强制**使用 `app` 前缀别名 |

### 别名规范

**fsyyft-go 包别名**：

| 包路径 | 别名 |
|-------|------|
| `github.com/fsyyft-go/kit/log` | `kitlog` |
| `github.com/fsyyft-go/kit/runtime` | `kitruntime` |
| `github.com/fsyyft-go/kit/kratos/middleware/validate` | `kitkratosmiddlewarevalidate` |

**项目内部包别名**：

| 包路径 | 别名 |
|-------|------|
| `github.com/fsyyft-go/kratos-layout/api/helloworld/v1` | `apphelloworldv1` |
| `github.com/fsyyft-go/kratos-layout/internal/pkg/conf` | `appconf` |
| `github.com/fsyyft-go/kratos-layout/internal/pkg/log` | `applog` |

### 正确示例

```go
import (
	"context"
	"fmt"
	"strings"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/go-kratos/kratos/v2/errors"
	kratoshttp "github.com/go-kratos/kratos/v2/transport/http"
	"github.com/prometheus/client_golang/prometheus/promhttp"

	kitlog "github.com/fsyyft-go/kit/log"
	kitruntime "github.com/fsyyft-go/kit/runtime"

	apphelloworldv1 "github.com/fsyyft-go/kratos-layout/api/helloworld/v1"
	appconf "github.com/fsyyft-go/kratos-layout/internal/pkg/conf"
)
```

### 错误示例

```go
// ❌ 错误：未使用括号包裹
import "context"
import "fmt"

// ❌ 错误：未分段，未排序
import (
	"github.com/go-kratos/kratos/v2/errors"
	"context"
	kitlog "github.com/fsyyft-go/kit/log"
	"fmt"
)

// ❌ 错误：fsyyft-go 包未取别名
import (
	"github.com/fsyyft-go/kit/log"
)

// ❌ 错误：项目内包未使用 app 前缀别名
import (
	conf "github.com/fsyyft-go/kratos-layout/internal/pkg/conf"
)
```

---

## 开发流程

### 常用命令

| 命令 | 用途 |
|------|------|
| `make init` | 初始化项目所需的工具链 |
| `make api` | 生成 API 相关的 Protocol Buffers 代码 |
| `make config` | 生成配置相关的 Protocol Buffers 代码 |
| `make validate` | 生成验证相关代码 |
| `make generate` | 执行代码生成任务（包括 Wire） |
| `make lint` | 执行基本的代码质量检查 |
| `make lint-strict` | 执行严格的代码质量检查 |
| `make test` | 运行所有测试 |
| `make build` | 构建多平台可执行文件 |
| `make clean` | 清理构建产物 |

### 开发工作流

```
1. 修改 Proto 文件（如需要）
   └── 运行 make api 和 make validate

2. 修改配置定义（如需要）
   └── 运行 make config

3. 编写业务代码
   ├── 定义接口和结构体
   ├── 实现业务逻辑
   └── 编写完整注释

4. 更新依赖注入
   ├── 修改 wire.go 文件
   └── 运行 make generate

5. 代码检查
   └── 运行 make lint 或 make lint-strict

6. 运行测试
   └── 运行 make test
```

### 代码质量检查

**基本检查**（`make lint`）：
- 使用 golangci-lint 进行静态分析
- 超时时间：3 分钟

**严格检查**（`make lint-strict`）：
- 启用更多 linter
- 超时时间：10 分钟
- 启用：govet, errcheck, staticcheck, ineffassign, unused, gosec, misspell, revive

---

## 注释自检流程

完成代码编写后，必须执行以下自检步骤，确保注释符合规范。如发现不符合项，必须立即修正后重新执行完整自检。

### 步骤 1：包级别注释检查

**检查项**：每个包是否存在 `doc.go` 文件

**判定标准**：
- ✅ 每个包必须包含一个 `doc.go` 文件
- ✅ `doc.go` 文件必须包含包级别注释，格式为 `// Package <包名> <简短描述>。`
- ✅ `doc.go` 文件只包含 `package` 声明和注释，不包含任何代码实现
- ✅ 除 `doc.go` 外的所有文件，`package` 声明前后不得有任何注释

**不符合处理**：
- 缺少 `doc.go` 文件：创建 `doc.go` 文件并添加包级别注释
- `doc.go` 包含代码：移除 `doc.go` 中的所有代码实现
- 其他文件有包注释：删除非 `doc.go` 文件中的包级别注释

### 步骤 2：类型定义注释完整性检查

**检查范围**：所有 `interface`、`struct`、`type` 别名定义

**判定标准**：
- ✅ 每个类型定义必须有功能说明注释
- ✅ `interface` 的每个方法必须有注释，且包含完整的参数说明和返回值说明
- ✅ `struct` 的每个字段必须有用途说明注释

**不符合处理**：为缺失注释的类型、方法、字段补充完整注释

### 步骤 3：函数和方法注释完整性检查

**检查范围**：所有 `func` 声明（包括导出和非导出函数）

**判定标准**：
- ✅ 每个函数必须有功能描述注释
- ✅ 函数有参数时，必须在注释中说明每个参数的用途
- ✅ 函数有返回值时，必须在注释中说明每个返回值的含义

**不符合处理**：为缺失注释的函数补充完整的功能、参数、返回值注释

### 步骤 4：interface 实现一致性检查

**检查范围**：所有实现 `interface` 的 `struct` 方法

**判定标准**：
- ✅ `struct` 方法的注释内容必须与 `interface` 方法的注释完全一致（逐字比对）

**不符合处理**：将 `struct` 方法的注释修改为与 `interface` 方法注释完全一致

### 步骤 5：函数体内注释检查

**检查范围**：所有函数的实现代码

**判定标准**：
- ✅ 函数包含业务逻辑时，关键业务步骤必须有说明注释
- ✅ 函数包含复杂条件判断（嵌套 `if`、多条件组合）时，必须有逻辑说明注释
- ✅ 函数包含循环或递归处理时，必须有处理目的说明注释
- ✅ 函数包含数据转换或计算时，关键变量必须有用途说明注释

**不符合处理**：分析函数的业务逻辑，为缺失注释的关键步骤补充说明注释

### 步骤 6：注释语义一致性检查

**检查方法**：搜索代码库中对相同概念的注释表述

**判定标准**：
- ✅ 相同概念的注释必须使用完全一致的表述
- ✅ 例如：所有 `context.Context` 参数的注释必须统一为"请求上下文，用于取消与超时控制。"

**不符合处理**：将不一致的注释统一修改为标准表述（参见"标准注释术语表"）

### 步骤 7：注释语言规范性检查

**检查范围**：所有注释文本

**判定标准**：
- ✅ 注释使用标准现代汉语，无语法错误
- ✅ 注释使用技术专业术语，不包含口语化表达（如"我们"、"这里"、"把...一下"等）
- ✅ 每个注释语句以中文标点符号结束（句号、感叹号等）

**不符合处理**：修改不规范注释，使其符合语言规范标准

### 步骤 8：注释准确性检查

**检查方法**：对照代码实现，验证注释描述是否准确

**判定标准**：
- ✅ 注释内容必须准确反映代码的实际功能和行为
- ✅ 不得出现与代码不符的描述

**不符合处理**：修正注释，使其准确描述代码功能

### 步骤 9：注释布局规范性检查

**检查范围**：所有注释的位置和格式

**判定标准**：
- ✅ 类型、函数、方法的注释位于声明的紧邻上方
- ✅ 函数体内逻辑的注释优先使用独立行前置注释
- ✅ 行尾注释仅用于简短说明，且内容简洁
- ✅ 注释的缩进层级与其描述的代码一致

**不符合处理**：调整注释位置和缩进，使其符合布局规范

### 自检结果判定

| 判定结果 | 处理方式 |
|---------|---------|
| 所有检查项均通过 | 注释符合规范，可以提交代码 |
| 存在任何检查项不通过 | 必须修正不符合项，重新执行完整自检流程 |

---

## 自检清单

### 代码提交前自检

完成代码编写后，逐项检查以下清单。所有项目必须全部通过方可提交代码。

**包级别注释检查**：
- [ ] 每个包存在 `doc.go` 文件
- [ ] `doc.go` 包含完整的包级别注释（格式：`// Package <包名> <描述>。`）
- [ ] `doc.go` 不包含任何代码实现（仅版权声明、包注释、package 声明）
- [ ] 其他文件的 `package` 声明前后无注释

**类型定义注释检查**：
- [ ] 所有 `interface` 定义有功能说明注释
- [ ] `interface` 的每个方法有完整的参数和返回值注释
- [ ] 所有 `struct` 定义有用途说明注释
- [ ] `struct` 的每个字段有用途说明注释

**函数注释检查**：
- [ ] 所有函数（含非导出）有功能描述注释
- [ ] 有参数时，注释中说明每个参数的用途
- [ ] 有返回值时，注释中说明每个返回值的含义
- [ ] 实现接口的方法注释与接口定义完全一致（逐字比对）

**函数体内注释检查**：
- [ ] 关键业务步骤有说明注释
- [ ] 复杂条件判断（2 层以上嵌套或 3 个以上条件组合）有逻辑说明注释
- [ ] 循环和递归处理有目的说明注释
- [ ] 注释使用独立行前置注释（非行尾注释）

**注释规范检查**：
- [ ] 注释使用规范的中文表述（无口语化表达）
- [ ] 每个注释以中文标点符号结束
- [ ] 相同语义使用统一的注释表述（参见"标准注释术语表"）
- [ ] 注释内容准确反映代码功能（无描述与代码不符的情况）

**包导入检查**：
- [ ] `import` 使用括号包裹
- [ ] 按四段分组（标准库、第三方、fsyyft-go、项目内），段间有空行
- [ ] 每段内按字母顺序排序
- [ ] `fsyyft-go` 包使用 `kit` 前缀别名（如 `kitlog`）
- [ ] 项目内包使用 `app` 前缀别名（如 `appconf`）

**代码规范检查**：
- [ ] 运行 `make lint` 无错误
- [ ] 运行 `make test` 全部通过
- [ ] 不修改生成的代码文件（`*.pb.go`、`wire_gen.go`）
- [ ] 不修改与请求无关的代码

**错误处理检查**：
- [ ] 所有可能返回错误的函数调用都有错误检查
- [ ] 错误返回时使用 `%w` 保持错误链
- [ ] 业务错误在 `biz` 层统一定义

---

## 变更历史

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| 1.2.0 | 2025-12-26 | 移除关键注意事项章节；优化生成代码管理规范（允许特定情况下手动修改）；调整版本控制规范表述 |
| 1.1.0 | 2025-12-26 | 增加详细注释自检流程（9 步）；补充条件分支、循环、错误处理的代码示例；增加 `<think>` 标签使用规范；优化文档结构与风格 |
| 1.0.0 | 2025-12-26 | 初始版本，基于项目实际规范整理 |

---

**维护者**: AI Assistant  
**项目**: github.com/fsyyft-go/kratos-layout
