# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个基于 [go-kratos/kratos](https://github.com/go-kratos/kratos) v2 框架的 Go 微服务模板项目，使用 Wire 进行依赖注入。

**关键信息**：
- Go 版本：1.25（以 [go.mod](go.mod) 为准）
- 核心框架：go-kratos/kratos v2
- 依赖注入：google/wire
- 配置管理：Protocol Buffers
- 日志库：logrus（通过 github.com/fsyyft-go/kit/log 封装）
- 工具库：github.com/fsyyft-go/kit

## 常用开发命令

### 代码生成
```bash
# 生成 API 相关的 Protocol Buffers 代码（修改 proto 文件后必须执行）
make api

# 生成配置相关代码
make config

# 生成验证相关代码
make validate

# 执行 Wire 依赖注入代码生成（修改 wire.go 后必须执行）
make generate
```

### 代码质量检查
```bash
# 基本代码质量检查
make lint

# 严格代码质量检查
make lint-strict
```

### 代码规范检查（使用项目技能工具）

项目提供了 Claude Code 技能工具用于代码规范检查：

- **comment-enforcer**：Go 代码注释规范检查与修复工具
- **go-import-enforcer**：Go 包导入规范检查与修复工具（纯 Claude 驱动，无脚本）
- **go-module-renamer**：Go 模块重命名自动化工具
- **git-commit-writer**：Git 提交信息智能生成工具

这些技能工具可通过 Claude Code 的 `/` 命令或技能调用方式使用。

### 测试
```bash
# 运行所有测试（带竞态检测）
make test

# 运行单个测试
go test -v -race ./internal/biz

# 运行单个测试函数
go test -v -run TestGreeter ./internal/biz
```

### 构建
```bash
# 构建多平台可执行文件
make build

# 构建 Docker 镜像
make image
```

### 项目初始化
```bash
# 初始化项目所需的工具链（安装 wire、protoc 等）
make init
```

## 项目架构

### 应用结构
项目包含两个独立的应用：
- **Web 服务** ([cmd/web/main.go](cmd/web/main.go))：HTTP API 服务
- **Task 服务** ([cmd/task/main.go](cmd/task/main.go))：后台任务服务

每个应用都有独立的入口和 Wire 配置。

### 分层架构

项目采用标准的 Kratos 分层架构：

```
internal/
├── app/              # 应用层（Wire 依赖注入配置）
│   ├── web/         # Web 应用的 Wire 配置
│   │   ├── wire.go  # Wire 依赖注入定义（编辑此文件）
│   │   ├── wire_gen.go  # Wire 生成的代码（勿手动修改）
│   │   └── app.go   # 应用启动逻辑
│   └── task/        # Task 应用的 Wire 配置
│       ├── wire.go
│       ├── wire_gen.go
│       └── app.go
├── biz/             # 业务逻辑层（Business Logic Layer）
│   ├── biz.go       # ProviderSet 定义
│   └── greeter.go   # 业务逻辑实现
├── data/            # 数据访问层（Data Access Layer）
│   ├── data.go      # ProviderSet 定义
│   └── greeter.go   # 数据访问实现
├── domain/          # 领域层（Domain Layer）
│   └── token.go     # 领域模型（实体、值对象等）
├── service/         # 服务层（Service Layer）
│   ├── service.go   # ProviderSet 定义
│   └── greeter.go   # gRPC/HTTP 服务实现
├── server/          # 服务器层（Server Layer）
│   ├── server.go    # ProviderSet 定义
│   └── web.go       # HTTP 服务器实现
├── task/            # 任务层（Task Layer）
│   ├── task.go      # ProviderSet 定义
│   └── hello.go     # 具体任务实现
└── pkg/             # 内部包（仅本项目内部可用）
    ├── conf/        # 配置管理（基于 Proto）
    └── log/         # 日志管理
```

### 依赖注入流程

使用 Wire 进行依赖注入，依赖关系从下往上：

1. **Data 层** → 实现 Data ProviderSet
2. **Biz 层** → 依赖 Data 层，实现 Biz ProviderSet
3. **Service 层** → 依赖 Biz 层，实现 Service ProviderSet
4. **Server 层** → 依赖 Service 层，实现 Server ProviderSet
5. **App 层** → 通过 `wire.go` 组装所有层

**修改依赖关系后**：
1. 编辑对应的 `wire.go` 文件
2. 运行 `make generate` 重新生成 `wire_gen.go`

### API 定义

API 使用 Protocol Buffers 定义，位于 [api/](api/) 目录：

```
api/
├── helloworld/v1/
│   ├── *.proto           # API 定义文件
│   └── *.pb.go          # 生成的 Go 代码（勿手动修改）
└── third_party/         # 第三方 proto 依赖
```

**修改 API 后**：
1. 编辑 `*.proto` 文件
2. 运行 `make api` 重新生成代码
3. 运行 `make validate` 生成验证代码

### 配置管理

配置使用 Protocol Buffers 定义，位于 [internal/pkg/conf/](internal/pkg/conf/)：

- **定义**：`conf.proto` 文件
- **加载**：`conf.go` 中的 `LoadConfig()` 函数
- **使用**：应用配置文件 [configs/config.yaml](configs/config.yaml)

**修改配置结构后**：
1. 编辑 `conf.proto`
2. 运行 `make config` 重新生成代码
3. 更新 `configs/config.yaml`

## 代码规范

### 版权声明

所有源代码文件必须在文件开头包含版权声明：

```go
// Copyright 2025 fsyyft-go
//
// Licensed under the MIT License.
// See LICENSE file in the project root for full license information.
```

### 注释规范

**所有代码必须包含中文注释**：

```go
// Package greeter 提供问候服务。
// 该服务实现了基本的问候功能，支持自定义问候消息。
package greeter

// Greeter 是问候服务的数据结构。
// 包含依赖的其他服务组件。
type Greeter struct {
    // data 是数据访问层组件。
    data *Data
}

// SayHello 返回问候消息。
//
// 参数:
//   ctx - 请求上下文
//   in - 问候请求参数
//
// 返回:
//   *pb.HelloReply - 问候响应
//   error - 错误信息
func (g *Greeter) SayHello(ctx context.Context, in *pb.HelloReq) (*pb.HelloReply, error) {
    // 实现业务逻辑
    return &pb.HelloReply{}, nil
}
```

### 错误处理

**保持错误链**：

```go
// ✅ 正确：保持错误链
if err := g.data.Save(ctx, data); nil != err {
    return fmt.Errorf("保存数据失败: %w", err)
}

// ❌ 错误：丢失原始错误
if err := g.data.Save(ctx, data); nil != err {
    return fmt.Errorf("保存数据失败")
}
```

### 包导入顺序

使用标准顺序：

```go
// 1. 标准库
import (
    "context"
    "fmt"
)

// 2. 第三方库
import (
    "github.com/go-kratos/kratos/v2/log"
)

// 3. 项目内部包
import (
    "github.com/fsyyft-go/kratos-layout/internal/biz"
)
```

### 生成代码管理

**勿手动修改的文件**：
- `*.pb.go` - Protocol Buffers 生成
- `wire_gen.go` - Wire 生成
- `*.openapi.json` - OpenAPI 规范生成

**修改流程**：
1. 修改源文件（`*.proto`、`wire.go`）
2. 运行对应的 `make` 命令重新生成
3. 检查生成的代码是否符合预期

## 开发流程

### 添加新功能

1. **定义 API**（[api/](api/)）
   - 创建或修改 `*.proto` 文件
   - 运行 `make api` 生成代码

2. **实现 Data 层**（[internal/data/](internal/data/)）
   - 在 `data.go` 的 ProviderSet 中添加新的 Provider
   - 实现数据访问逻辑

3. **实现 Biz 层**（[internal/biz/](internal/biz/)）
   - 在 `biz.go` 的 ProviderSet 中添加新的 UseCase
   - 实现业务逻辑

4. **实现 Service 层**（[internal/service/](internal/service/)）
   - 在 `service.go` 的 ProviderSet 中添加新的 Service
   - 实现 gRPC/HTTP 服务

5. **更新 Wire 配置**（[internal/app/web/wire.go](internal/app/web/wire.go)）
   - Wire 会自动识别新的 ProviderSet
   - 运行 `make generate` 生成代码

6. **测试**
   - 编写单元测试
   - 运行 `make test` 确保通过

7. **代码质量检查**
   - 运行 `make lint` 确保无错误

### 添加新任务

1. 在 [internal/task/](internal/task/) 定义任务接口
2. 在 `task.go` 的 ProviderSet 中注册
3. 在 [internal/app/task/](internal/app/task/) 的 Wire 配置中组装
4. 在 [cmd/task/main.go](cmd/task/main.go) 中调用

## 测试

### 测试文件组织

测试文件与源文件放在同一目录，命名为 `*_test.go`：

```
internal/
├── biz/
│   ├── greeter.go
│   └── greeter_test.go    # 业务逻辑测试
├── data/
│   ├── greeter.go
│   └── greeter_test.go    # 数据访问测试
└── service/
    ├── greeter.go
    └── greeter_test.go    # 服务层测试
```

### 测试最佳实践

```go
func TestGreeter_SayHello(t *testing.T) {
    // 准备测试数据
    tests := []struct {
        name    string
        input   *pb.HelloReq
        wantErr bool
    }{
        {
            name:    "正常情况",
            input:   &pb.HelloReq{Name: "test"},
            wantErr: false,
        },
    }

    // 执行测试
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            // 测试逻辑
        })
    }
}
```

## 重要文件

| 文件 | 说明 |
|------|------|
| [Makefile](Makefile) | 构建和开发命令定义 |
| [go.mod](go.mod) | Go 模块依赖定义 |
| [configs/config.yaml](configs/config.yaml) | 应用配置文件 |
| [cmd/web/main.go](cmd/web/main.go) | Web 服务入口 |
| [cmd/task/main.go](cmd/task/main.go) | Task 服务入口 |
| [internal/app/web/wire.go](internal/app/web/wire.go) | Web 应用依赖注入配置 |
| [internal/app/task/wire.go](internal/app/task/wire.go) | Task 应用依赖注入配置 |
| [.editorconfig](.editorconfig) | 编辑器配置（编码、缩进等） |

## 注意事项

1. **修改 Proto 文件后必须运行 `make api`**
2. **修改 Wire 配置后必须运行 `make generate`**
3. **所有代码注释使用中文**
4. **提交前运行 `make lint` 确保代码质量**
5. **测试必须通过 (`make test`)**
6. **保持错误链，使用 `%w` 包装错误**
7. **不要手动修改 `*_gen.go` 和 `*.pb.go` 文件**

## 调试技巧

### 查看 Wire 依赖图

如果 Wire 生成失败，可以手动运行查看详细错误：

```bash
cd internal/app/web
wire
```

### 运行单个服务

```bash
# 运行 Web 服务
go run cmd/web/main.go -conf ./configs/config.yaml

# 运行 Task 服务
go run cmd/task/main.go -conf ./configs/config.yaml
```

### 查看日志

日志文件位于 [logs/](logs/) 目录，根据配置文件中的 `log.output` 设置。
