# Go 模块重命名 - 文件模式规则

## 概述

本文档描述了 Go 项目中常见的文件类型及其在模块重命名时的处理方式。

## 文件类型分类

### 1. Go 源代码文件

#### .go 文件

**模式**：`import "module/path/package"`

**示例**：
```go
import (
    "github.com/fsyyft-go/kratos-layout/internal/conf"
)
```

**替换策略**：全量替换（完整模块路径）

**注意事项**：
- 需要替换所有导入语句
- 包括测试文件（*_test.go）
- 包括生成的文件（*.pb.go, wire_gen.go）

---

### 2. Protocol Buffers 文件

#### .proto 文件

**模式**：`option go_package = "module/path/package"`

**示例**：
```protobuf
option go_package = "github.com/fsyyft-go/kratos-layout/api/helloworld/v1;helloworld";
```

**替换策略**：全量替换（完整模块路径）

**注意事项**：
- 仅替换 go_package 选项中的路径部分
- 保留包名部分（分号后的部分）
- 其他 import 语句也需要替换

---

### 3. Go 模块定义

#### go.mod 文件

**模式**：`module module/path`

**示例**：
```go
module github.com/fsyyft-go/kratos-layout
```

**替换策略**：全量替换（完整模块路径）

**注意事项**：
- 这是模块定义文件，必须更新
- 更新后需要运行 `go mod tidy`

---

### 4. 构建配置文件

#### Makefile

**常见模式**：

| 模式 | 示例 | 替换策略 |
|-----|------|---------|
| Docker 镜像名 | `IMAGE_NAME=fsyyft/kratos-layout` | 部分替换（项目名） |
| 应用名称 | `APP_NAME=kratos-layout` | 部分替换（项目名） |
| 二进制文件名 | `BINARY_NAME=kratos-layout` | 部分替换（项目名） |

**替换策略**：部分替换（仅项目名）

**注意事项**：
- 检查所有包含项目名的变量
- 注意 Docker 镜像仓库用户名
- 检查路径和目录名

---

#### Dockerfile

**常见模式**：

| 模式 | 示例 | 替换策略 |
|-----|------|---------|
| WORKDIR | `WORKDIR /src/kratos-layout` | 部分替换（项目名） |
| COPY/ADD | `COPY kratos-layout /app` | 部分替换（项目名） |

**替换策略**：部分替换（仅项目名）

**注意事项**：
- 检查路径引用
- 检查环境变量

---

#### docker-compose.yml

**常见模式**：

| 模式 | 示例 | 替换策略 |
|-----|------|---------|
| 服务名 | `service: kratos-layout` | 部分替换（项目名） |
| 容器名 | `container_name: kratos-layout` | 部分替换（项目名） |
| 镜像名 | `image: fsyyft/kratos-layout` | 部分替换（项目名） |

**替换策略**：部分替换（仅项目名）

---

### 5. 配置文件

#### config.proto（Kratos 框架）

**常见模式**：

| 模式 | 示例 | 替换策略 |
|-----|------|---------|
| Server 名称 | `server: kratos-layout` | 部分替换（项目名） |
| 服务名称 | `service_name: kratos-layout` | 部分替换（项目名） |

**替换策略**：部分替换（仅项目名）

**注意事项**：
- 这是 Kratos 框架的配置文件
- 更新后需要重新生成代码：`make config`

---

#### 其他配置文件

| 文件类型 | 常见模式 | 替换策略 |
|---------|---------|---------|
| .yaml, .yml | 应用名称、服务名 | 部分替换（项目名） |
| .json | 应用名称、服务名 | 部分替换（项目名） |
| .toml | 应用名称、服务名 | 部分替换（项目名） |
| .ini | 应用名称、服务名 | 部分替换（项目名） |

**注意事项**：
- 检查所有配置键值对
- 注意嵌套的配置结构
- 某些配置可能不需要更新

---

### 6. 文档文件

#### README.md

**常见模式**：

| 模式 | 示例 | 替换策略 |
|-----|------|---------|
| 项目名称 | `# kratos-layout` | 部分替换（项目名） |
| 仓库路径 | `github.com/fsyyft-go/kratos-layout` | 全量替换（完整路径） |
| 导入示例 | `import "github.com/..."` | 全量替换（完整路径） |

**替换策略**：根据上下文判断

**注意事项**：
- 标题通常使用项目名
- 代码示例使用完整模块路径
- 需要人工检查替换后的内容

---

#### OWNERS

**常见模式**：

| 模式 | 示例 | 替换策略 |
|-----|------|---------|
| 项目所有者 | `kratos-layout` | 部分替换（项目名） |

**替换策略**：部分替换（仅项目名）

---

#### 其他文档文件

| 文件类型 | 常见位置 | 替换策略 |
|---------|---------|---------|
| .md | docs/, .github/ | 根据上下文 |
| .txt | docs/, examples/ | 根据上下文 |
| .rst | docs/ | 根据上下文 |

**注意事项**：
- 检查教程和示例代码
- 检查 API 文档中的包路径
- 检查贡献指南中的引用

---

### 7. 持续集成/持续部署文件

#### GitHub Actions

**文件位置**：`.github/workflows/*.yml`

**常见模式**：

| 模式 | 示例 | 替换策略 |
|-----|------|---------|
| APP_NAME | `APP_NAME: kratos-layout` | 部分替换（项目名） |
| 路径引用 | `path: kratos-layout` | 部分替换（项目名） |

**替换策略**：部分替换（仅项目名）

---

#### 其他 CI/CD 文件

| 文件类型 | 常见模式 | 替换策略 |
|---------|---------|---------|
| .gitlab-ci.yml | 项目名引用 | 部分替换（项目名） |
| Jenkinsfile | 项目名引用 | 部分替换（项目名） |
| .travis.yml | 项目名引用 | 部分替换（项目名） |

---

### 8. 版本控制文件

#### .gitignore

**常见模式**：通常不需要更新

**注意事项**：
- 检查是否有项目特定的忽略规则
- 一般情况下不需要修改

---

#### .gitattributes

**常见模式**：通常不需要更新

**注意事项**：
- 检查 Git LFS 配置
- 一般情况下不需要修改

---

## 全量 vs 部分替换判断规则

### 全量替换（完整模块路径）

**触发条件**：
- 模块名的前两个部分（域名、用户名）发生变化

**示例**：
```
github.com/fsyyft-go/kratos-layout → github.com/new-org/new-project
```

**影响范围**：
- go.mod 模块声明
- .go 文件导入语句
- .proto 文件 go_package 选项
- 文档中的代码示例

---

### 部分替换（仅项目名）

**触发条件**：
- 仅模块名的最后一个部分（项目名）发生变化

**示例**：
```
github.com/fsyyft-go/kratos-layout → github.com/fsyyft-go/new-project
```

**影响范围**：
- Makefile 变量（IMAGE_NAME, APP_NAME）
- 配置文件中的应用名称
- 文档中的项目名称
- Docker 镜像名

---

## 特殊文件处理

### 生成文件

| 文件类型 | 生成方式 | 替换策略 |
|---------|---------|---------|
| *.pb.go | protoc | 文本替换优先 |
| wire_gen.go | wire | 文本替换优先 |
| *.pb.gw.go | protoc | 文本替换优先 |

**策略说明**：
- **文本替换优先**：更快，无需工具链
- **重新生成**：如果文本替换失败，可使用 `make api`、`make config`

---

### 模板文件

**特征**：包含 `// 模板：` 注释

**处理方式**：
- 自动删除所有模板注释行
- 保留其他内容

**示例**：
```go
// 模板：这是一个模板文件，使用前请修改
package main
```

---

### 二进制文件

| 文件类型 | 处理方式 |
|---------|---------|
| *.exe | 忽略，重新编译 |
| *.dll | 忽略，重新编译 |
| *.so | 忽略，重新编译 |
| *.dylib | 忽略，重新编译 |
| *.a | 忽略，重新编译 |

---

## 文件搜索优先级

### 高优先级（必须处理）

1. go.mod - 模块定义
2. **/*.go - 所有 Go 源代码
3. **/*.proto - 所有 Proto 文件
4. Makefile - 构建配置

### 中优先级（建议处理）

5. Dockerfile - Docker 配置
6. docker-compose.yml - Docker Compose 配置
7. **/*.yaml - YAML 配置文件
8. **/*.yml - YAML 配置文件
9. internal/conf/config.proto - Kratos 配置

### 低优先级（可选处理）

10. **/*.md - Markdown 文档
11. OWNERS - 项目所有者
12. .github/**/* - GitHub 相关文件
13. docs/**/* - 文档目录

---

## 注意事项

### 1. 路径分隔符

- **Unix/Linux/macOS**：使用 `/`
- **Windows**：使用 `\`
- **跨平台兼容**：始终使用 `/`（Go 自动处理）

### 2. 大小写敏感性

- **Linux**：区分大小写
- **Windows**：不区分大小写
- **macOS**：通常区分大小写（取决于文件系统）
- **建议**：保持原始大小写

### 3. 特殊字符

Go 模块名中不应包含以下字符：
- 空格
- 特殊符号（!@#$%^&*()）
- 非ASCII字符（除非使用 Go modules 的转义机制）

### 4. 路径长度

- **Windows**：路径长度限制为 260 字符（MAX_PATH）
- **Linux/macOS**：通常限制为 4096 字符
- **建议**：保持模块名简洁

### 5. Go Modules 私有仓库

私有模块的路径格式：
```
github.com/username/private-repo.git
```

或使用 GOPRIVATE 环境变量：
```bash
export GOPRIVATE=github.com/username
```

---

## 最佳实践

### 1. 重命名前准备

- [ ] 创建完整备份
- [ ] 通知团队成员
- [ ] 更新 CI/CD 配置
- [ ] 更新文档

### 2. 重命名过程

- [ ] 使用脚本批量替换
- [ ] 验证每个替换结果
- [ ] 测试编译
- [ ] 运行测试套件

### 3. 重命名后验证

- [ ] 运行 `go mod tidy`
- [ ] 运行 `go build ./...`
- [ ] 运行 `go test ./...`
- [ ] 运行 `make lint`（如果有）
- [ ] 检查所有文档

### 4. 回滚准备

- [ ] 保留备份直到验证完成
- [ ] 准备回滚脚本
- [ ] 记录所有修改

---

## 常见问题

### Q1: 为什么不直接重新生成代码？

**A**: 文本替换更快，且不依赖工具链。重新生成需要：
- 安装 protoc
- 安装 Go 插件
- 配置生成选项
- 可能丢失自定义配置

### Q2: 如何处理 vendor 目录？

**A**:
- 如果使用 vendor，删除 vendor 目录后重新运行 `go mod vendor`
- 或者更新 vendor 中的所有导入路径

### Q3: 如何处理子模块？

**A**:
- 如果有 Go submodules，需要分别重命名每个子模块
- 更新 go.work 文件（如果使用 Go workspaces）

### Q4: 如何处理 Git 子模块？

**A**:
- Git submodules 不受影响
- 但需要更新子模块中的引用（如果适用）

---

## 相关资源

- [Go Modules Reference](https://golang.org/ref/mod)
- [Protocol Buffers Style Guide](https://developers.google.com/protocol-buffers/docs/style)
- [Kratos Framework Documentation](https://go-kratos.dev/)
- [Go Module Mirror and Checksum Database](https://sum.golang.org/)
