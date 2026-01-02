# Go 代码注释规范

本文档从 `.ai/rule.md.bak` 提取，定义了 Kratos Layout 项目中 Go 代码注释的强制标准和最佳实践。

## 目录

1. [注释语言规范](#注释语言规范)
2. [包级别注释](#包级别注释)
3. [类型定义注释](#类型定义注释)
4. [函数和方法注释](#函数和方法注释)
5. [函数体内注释](#函数体内注释)
6. [行内注释规范](#行内注释规范)
7. [条件分支注释](#条件分支注释)
8. [循环和递归注释](#循环和递归注释)
9. [错误处理注释](#错误处理注释)
10. [禁止的注释风格](#禁止的注释风格)
11. [标准术语表](#标准术语表)

---

## 注释语言规范

| 规范 | 要求 |
|------|------|
| **语言** | 使用标准现代汉语书面表达 |
| **语法** | 确保语句语法正确，符合汉语表达习惯 |
| **术语** | 使用技术领域专业术语，避免口语化表达 |
| **标点** | 每个注释语句以中文标点符号结束 |
| **一致性** | 相同语义的概念使用统一的注释表述 |

---

## 包级别注释

### 强制要求

- 每个包**必须**在独立的 `doc.go` 文件中编写包级别注释
- `doc.go` 文件**仅**包含版权声明、包注释和 `package` 声明，**不**包含任何代码实现
- 除 `doc.go` 外的所有文件，`package` 声明前后**不得**有任何注释

### doc.go 文件格式

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

### 其他 Go 文件格式

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

---

## 类型定义注释

### 接口定义

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

### 结构体定义

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

---

## 函数和方法注释

### 标准格式

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

### 注释要点

| 要点 | 说明 |
|------|------|
| **功能描述** | 第一行简洁说明函数用途 |
| **参数说明** | 每个参数的类型、含义、约束条件 |
| **返回值说明** | 每个返回值的类型、含义、可能的值 |
| **接口一致性** | 实现接口的方法注释必须与接口定义完全一致 |

---

## 函数体内注释

### 业务逻辑注释

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

### 注释原则

| 原则 | 说明 |
|------|------|
| **关键步骤** | 为业务逻辑的关键步骤编写前置注释 |
| **复杂逻辑** | 复杂条件判断、循环、递归需要逻辑说明 |
| **数据处理** | 数据转换、计算的关键变量需要说明 |
| **前置注释** | 优先使用独立行的前置注释 |
| **标点结束** | 每条注释以中文标点符号结束 |

### "关键步骤"判定标准

- 业务决策点（影响流程走向的判断）
- 数据转换点（格式转换、类型转换）
- 外部调用点（调用其他服务、数据库操作）
- 状态变更点（修改对象状态、缓存更新）

### "复杂条件"判定标准

- 2 层以上的嵌套条件（`if` 中嵌套 `if`）
- 3 个以上的条件组合（使用 `&&` 或 `||` 连接）
- 涉及位运算或特殊逻辑的条件

---

## 行内注释规范

### 仅在必要时使用行内注释，优先使用前置注释

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

### 行内注释使用原则

- ✅ 仅用于解释复杂或非直观的逻辑
- ✅ 注释内容简洁明了，必须以标点结束
- ✅ 与代码保持适当距离（至少两个空格）
- ❌ 不用于解释显而易见的代码
- ❌ 不用于重复代码已表达的信息

---

## 条件分支注释

### 复杂条件判断需要说明判断逻辑

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

---

## 循环和递归注释

### 循环和递归逻辑需要说明处理目的

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

---

## 错误处理注释

### 错误处理需要说明处理逻辑

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

---

## 禁止的注释风格

### 以下注释风格禁止出现

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

### 禁止风格及原因

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

---

## 标准术语表

为保证注释一致性，以下常见参数使用统一表述：

| 参数类型 | 标准表述 |
|---------|---------|
| `context.Context` | "请求上下文，用于取消与超时控制。" |
| `*Config` | "应用配置信息。" |
| `Logger` | "日志记录器。" |
| `*Data` | "数据仓储接口。" |
| `*Greeter` | "Greeter 实体。" |
| `error` 返回值 | "失败时返回错误，成功时返回 nil。" |

**一致性要求**：
- 全局统一使用相同的参数注释表述
- 使用 `check_terminology.py` 脚本检查一致性
- 发现不一致时，必须统一为标准表述

---

## 参考资源

- **完整规范文档**：`.ai/rule.md.bak`
- **Go 官方注释指南**：[Effective Go: Commentary](https://golang.org/doc/effective_go.html#commentary)
- **项目仓库**：[github.com/fsyyft-go/kratos-layout](https://github.com/fsyyft-go/kratos-layout)
