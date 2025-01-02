# 包级别注释规范

## 概述

本文档定义了 Go 项目中包级别注释的规范要求。包级别注释是 Go 代码文档的重要组成部分,必须严格遵守本规范。

## 强制要求

### 1. doc.go 文件强制要求

每个包**必须**有独立的 `doc.go` 文件用于存放包级别注释。

**目录结构**:
```
internal/
└── biz/
    ├── doc.go          # 包级别注释（必需）
    ├── greeter.go      # 业务逻辑实现
    └── greeter_test.go # 测试文件
```

**禁止做法**:
```
❌ 错误: 在非 doc.go 文件中添加包注释
// Package biz 提供业务逻辑层实现。
package biz

type Greeter struct {
    ...
}
```

**正确做法**:
```go
✅ 正确: doc.go 文件
// Copyright 2025 fsyyft-go
//
// Licensed under the MIT License.
// See LICENSE file in the project root for full license information.

// Package biz 提供业务逻辑层实现。
//
// 本包包含应用程序的核心业务逻辑和用例实现,
// 负责协调数据访问层和表现层。
package biz
```

### 2. doc.go 文件格式标准

`doc.go` 文件**仅包含**以下内容,不得包含任何代码实现:

```go
// Copyright 2025 fsyyft-go
//
// Licensed under the MIT License.
// See LICENSE file in the project root for full license information.

// Package [包名] 提供的简短描述（单行）。
//
// 包的详细功能说明（可选,多行）。
//
// 主要组件(可选):
//   - 组件1: 说明。
//   - 组件2: 说明。
//
// 使用示例(可选):
//
//	如何使用该包的代码示例
package [包名]
```

**格式要求**:
1. **版权声明**: 必须位于文件开头
2. **包注释**: 紧跟版权声明,至少包含一行功能描述
3. **package 声明**: 文件的最后一行,仅为 `package [包名]`
4. **无代码实现**: doc.go 文件中不得包含任何类型、函数、变量等代码

### 3. 其他 Go 文件禁止规则

除 `doc.go` 外的所有 `.go` 文件,**禁止**在 `package` 声明前后添加任何注释。

**禁止做法**:
```go
❌ 错误: greeter.go
// Package biz 实现问候功能。
package biz

// Greeter 定义问候实体。
type Greeter struct {
    Hello string
}
```

**正确做法**:
```go
✅ 正确: greeter.go
package biz

// Greeter 定义问候实体。
type Greeter struct {
    Hello string
}
```

## doc.go 内容规范

### 基本结构

**最小内容**（仅包含功能描述）:
```go
// Copyright 2025 fsyyft-go
//
// Licensed under the MIT License.
// See LICENSE file in the project root for full license information.

// Package biz 提供业务逻辑层实现。
package biz
```

**完整内容**（功能描述 + 详细说明）:
```go
// Copyright 2025 fsyyft-go
//
// Licensed under the MIT License.
// See LICENSE file in the project root for full license information.

// Package biz 提供业务逻辑层实现。
//
// 本包包含应用程序的核心业务逻辑和用例实现,
// 负责协调数据访问层和表现层。主要功能包括:
//   - 实体管理: 创建、更新、查询、删除实体
//   - 业务规则: 实现核心业务逻辑和验证
//   - 数据转换: 在不同层级之间转换数据格式
//
// 主要组件:
//   - GreeterUsecase: 问候相关业务逻辑
//   - GreeterRepo: 数据仓储接口定义
//
// 使用示例:
//
//	uc := biz.NewGreeterUsecase(logger, conf, repo)
//	greeter, err := uc.CreateGreeter(ctx, &biz.Greeter{Hello: "World"})
//	if nil != err {
//	    return err
//	}
//	fmt.Printf("Created: %v\n", greeter)
package biz
```

### 注释内容要求

1. **第一行**: 简短的功能描述,以句号结束
2. **详细说明** (可选): 多行详细说明,每行以句号或逗号结束
3. **主要组件** (可选): 列出包中主要的类型、接口、函数
4. **使用示例** (可选): 展示如何使用该包的代码示例

## 常见错误

### 错误 1: 缺少 doc.go 文件

**症状**: 包目录中没有 `doc.go` 文件

**示例**:
```
internal/
└── biz/
    ├── greeter.go
    └── greeter_test.go
❌ 缺少 doc.go
```

**解决方案**: 创建 `doc.go` 文件并添加包级别注释

**优先级**: 🔴 高（严重影响包文档的完整性）

### 错误 2: doc.go 包含代码实现

**症状**: `doc.go` 文件中包含类型、函数等代码

**示例**:
```go
❌ 错误
package biz

// Package biz 提供业务逻辑层实现。
package biz

// Greeter 定义问候实体。
type Greeter struct {
    Hello string
}

// SayHello 发送问候。
func SayHello(name string) string {
    return "Hello, " + name
}
```

**解决方案**: 将所有代码实现移到其他 `.go` 文件,`doc.go` 仅保留包注释和 `package` 声明

**优先级**: 🔴 高（违反 doc.go 文件格式标准）

### 错误 3: 在非 doc.go 文件中添加包注释

**症状**: 在 `greeter.go`、`greeter_test.go` 等文件的 `package` 声明前后有注释

**示例**:
```go
❌ 错误
// Package biz 实现问候功能。
package biz

type Greeter struct {
    Hello string
}
```

**解决方案**: 删除 `package` 声明前后的所有注释,将其移到 `doc.go` 文件

**优先级**: 🟠 中（违反包注释集中管理原则）

### 错误 4: doc.go 格式不正确

**症状**: `doc.go` 文件缺少版权声明、包注释格式不正确

**示例**:
```go
❌ 错误: 缺少版权声明
package biz
```

```go
❌ 错误: 缺少包注释
// Copyright 2025 fsyyft-go
//
// Licensed under the MIT License.
package biz
```

```go
❌ 错误: 注释位置错误
// Copyright 2025 fsyyft-go
//
// Licensed under the MIT License.
package biz

// Package biz 提供业务逻辑层实现。❌ 注释在 package 之后
```

**解决方案**: 按照"doc.go 文件格式标准"章节修正格式

**优先级**: 🟠 中（影响包注释的专业性）

### 错误 5: 包注释过于简略

**症状**: 包注释仅有一行,没有提供足够的信息

**示例**:
```go
❌ 错误: 过于简略
// Package biz.
package biz
```

**解决方案**: 添加功能描述,说明包的主要职责和组件

**优先级**: 🟡 低（不影响规范符合性,但影响文档质量）

## 正确示例

### 示例 1: 简单包注释

**文件**: `internal/biz/doc.go`

```go
// Copyright 2025 fsyyft-go
//
// Licensed under the MIT License.
// See LICENSE file in the project root for full license information.

// Package biz 提供业务逻辑层实现。
package biz
```

**适用场景**: 功能简单、一目了然的包

### 示例 2: 详细包注释

**文件**: `internal/biz/doc.go`

```go
// Copyright 2025 fsyyft-go
//
// Licensed under the MIT License.
// See LICENSE file in the project root for full license information.

// Package biz 提供业务逻辑层实现。
//
// 本包包含应用程序的核心业务逻辑和用例实现,
// 负责协调数据访问层和表现层。主要功能包括:
//   - 实体管理: 创建、更新、查询、删除实体
//   - 业务规则: 实现核心业务逻辑和验证
//   - 数据转换: 在不同层级之间转换数据格式
//
// 主要组件:
//   - GreeterUsecase: 问候相关业务逻辑
//   - GreeterRepo: 数据仓储接口定义
package biz
```

**适用场景**: 功能复杂、包含多个主要组件的包

### 示例 3: 带使用示例的包注释

**文件**: `internal/biz/doc.go`

```go
// Copyright 2025 fsyyft-go
//
// Licensed under the MIT License.
// See LICENSE file in the project root for full license information.

// Package biz 提供业务逻辑层实现。
//
// 本包包含应用程序的核心业务逻辑和用例实现,
// 负责协调数据访问层和表现层。
//
// 主要组件:
//   - GreeterUsecase: 问候相关业务逻辑
//   - GreeterRepo: 数据仓储接口定义
//
// 使用示例:
//
//	uc := biz.NewGreeterUsecase(logger, conf, repo)
//	greeter, err := uc.CreateGreeter(ctx, &biz.Greeter{Hello: "World"})
//	if nil != err {
//	    return err
//	}
//	fmt.Printf("Created: %v\n", greeter)
package biz
```

**适用场景**: 需要展示如何使用该包的场景

### 示例 4: 应用入口包注释

**文件**: `cmd/web/doc.go`

```go
// Copyright 2025 fsyyft-go
//
// Licensed under the MIT License.
// See LICENSE file in the project root for full license information.

// Package main 提供 Web 应用程序入口。
//
// 本程序启动 HTTP 服务器,提供 RESTful API 服务。
// 支持的功能:
//   - HTTP 路由处理
//   - 中间件集成（日志、跟踪、恢复）
//   - 配置管理
//   - 优雅关闭
//
// 启动命令:
//
//	go run cmd/web/main.go -conf ./configs/config.yaml
package main
```

**适用场景**: 应用程序入口包

## 检查清单

使用以下清单检查包注释是否符合规范:

- [ ] 每个包都有独立的 `doc.go` 文件
- [ ] `doc.go` 文件包含版权声明
- [ ] `doc.go` 文件包含包级别注释
- [ ] `doc.go` 文件仅包含版权声明、包注释、package 声明
- [ ] 非 `doc.go` 文件的 `package` 声明前后没有任何注释
- [ ] 包注释以中文标点符号结束
- [ ] 包注释准确描述包的功能
- [ ] 包注释使用专业术语

## 与 Go 官方文档的关系

本规范基于 Go 官方文档要求:
- Go 官方要求包级别注释应该放在 `doc.go` 文件中
- Go 官方要求包注释的第一行应该是简短的功能描述
- 本规范在此基础上增加了版权声明的强制要求和中文注释的要求

**参考**: [Go 官方文档: How to write Go code - Package comments](https://go.dev/doc/effective_go#commentary)
