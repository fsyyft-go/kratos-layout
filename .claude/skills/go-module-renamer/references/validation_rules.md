# Go 模块重命名 - 验证规则

## 概述

本文档描述了 Go 模块重命名后的验证流程、规则和常见问题的解决方案。

## 验证流程

### 阶段 1：浅层验证（快速验证）

**目标**：快速发现明显的编译和语法错误

**时间**：1-3 分钟

**执行顺序**：
```
1. go fmt ./...
2. go mod tidy
3. make lint（可选）
4. make build（可选）
```

#### 步骤 1：代码格式化 (go fmt)

**命令**：
```bash
go fmt ./...
```

**预期结果**：
- 无输出或仅输出格式化的文件列表
- 返回码：0

**可能的错误**：
- ❌ 无（go fmt 几乎不会失败）

**验证通过条件**：
- 返回码为 0

**说明**：
- `go fmt` 会自动格式化代码
- 不会报错，只会修改文件
- 建议在所有操作前运行，确保代码格式一致

---

#### 步骤 2：依赖管理 (go mod tidy)

**命令**：
```bash
go mod tidy
```

**预期结果**：
- 可能会添加或删除依赖
- 返回码：0

**可能的错误**：

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `module XYZ: not found` | 模块路径不存在 | 检查 go.mod 中的模块名 |
| `cannot find module providing package ABC` | 依赖包未找到 | 检查导入路径是否正确 |
| `inconsistent vendoring` | vendor 目录不一致 | 删除 vendor 目录，重新运行 |

**验证通过条件**：
- 返回码为 0
- go.mod 和 go.sum 已更新

**说明**：
- 清理未使用的依赖
- 添加缺失的依赖
- 更新 go.sum 文件

---

#### 步骤 3：Lint 检查（可选）

**命令**：
```bash
make lint
```

**或**（如果没有 Makefile）：
```bash
golangci-lint run
```

**预期结果**：
- 无错误报告
- 返回码：0

**可能的错误**：

| 错误类型 | 常见原因 | 解决方案 |
|---------|---------|---------|
| Import shadowing | 导入包名冲突 | 使用别名：`import xxx "path"` |
| Unused imports | 未使用的导入 | 删除未使用的导入 |
| Missing comments | 缺少文档注释 | 添加文档注释 |
| Formatting issues | 格式问题 | 运行 `go fmt` |

**验证通过条件**：
- 返回码为 0
- 无关键错误（warnings 可以忽略）

**说明**：
- Lint 检查可以发现潜在问题
- 某些警告可以忽略（视团队规范而定）
- 如果没有配置 Lint 工具，可以跳过

---

#### 步骤 4：编译验证（可选）

**命令**：
```bash
make build
```

**或**（如果没有 Makefile）：
```bash
go build ./...
```

**预期结果**：
- 生成可执行文件
- 返回码：0

**可能的错误**：

| 错误类型 | 常见原因 | 解决方案 |
|---------|---------|---------|
| `undefined: XXX` | 函数或变量未定义 | 检查拼写，检查是否遗漏文件 |
| `cannot find package` | 包路径错误 | 检查导入路径 |
| `type mismatch` | 类型不匹配 | 检查类型定义 |
| `missing return` | 缺少返回语句 | 添加返回语句 |

**验证通过条件**：
- 返回码为 0
- 生成了所有预期的可执行文件

**说明**：
- 编译验证会检查所有语法和类型错误
- 如果有 main 包，会生成可执行文件
- 建议在所有平台上编译（使用交叉编译）

---

### 阶段 2：深层验证（全面检查）

**目标**：发现所有残留的旧模块名引用

**时间**：3-5 分钟

**执行方式**：
```bash
grep -r "旧模块名" --include="*.go" --include="*.proto" .
```

**或使用脚本**：
```bash
python3 validate_deep.py <旧模块名>
```

#### 验证规则

##### 规则 1：代码文件验证

**检查文件**：`.go`, `.proto`

**验证标准**：
- ✅ 不应包含任何旧模块名的引用
- ❌ 如果发现，必须修复

**处理方式**：
1. 定位文件
2. 检查上下文
3. 确定是否需要替换
4. 手动修复或使用脚本

**示例**：
```go
// ❌ 错误：残留引用
import "github.com/fsyyft-go/kratos-layout/internal/conf"

// ✅ 正确：已更新
import "github.com/new-org/new-project/internal/conf"
```

---

##### 规则 2：配置文件验证

**检查文件**：`Makefile`, `Dockerfile`, `*.yaml`, `*.yml`, `*.json`

**验证标准**：
- ⚠️  可能包含旧项目名（视情况而定）
- 检查是否需要更新

**处理方式**：
1. 审查每个匹配
2. 判断是否为配置项
3. 根据实际需求决定是否更新

**示例**：
```makefile
# ⚠️  需要检查
IMAGE_NAME=fsyyft/kratos-layout

# ✅ 可能正确（Docker Hub 用户名）
IMAGE_NAME=fsyyft/new-project
```

---

##### 规则 3：文档文件验证

**检查文件**：`*.md`, `*.txt`, `docs/**`, `.github/**`

**验证标准**：
- ℹ️  可能包含旧模块名（历史说明）
- 建议更新明显的引用

**处理方式**：
1. 区分历史说明和实际引用
2. 更新代码示例
3. 更新仓库链接
4. 保留必要的历史说明

**示例**：
```markdown
# ❌ 需要更新
Clone the repository:
git clone https://github.com/fsyyft-go/kratos-layout.git

# ✅ 已更新
Clone the repository:
git clone https://github.com/new-org/new-project.git
```

---

##### 规则 4：注释验证

**检查位置**：代码文件中的注释

**验证标准**：
- ℹ️  可能包含旧模块名
- 视情况决定是否更新

**处理方式**：
1. 检查注释是否影响理解
2. 更新过时的示例
3. 保留有历史价值的注释

**示例**：
```go
// ❌ 过时
// Based on github.com/fsyyft-go/kratos-layout

// ✅ 已更新
// Based on github.com/new-org/new-project
```

---

#### 验证输出格式

```json
{
  "code": [
    {
      "path": "internal/server/server.go",
      "matches": [
        {
          "line": 10,
          "pattern": "github.com/fsyyft-go/kratos-layout",
          "content": "import \"github.com/fsyyft-go/kratos-layout/internal/conf\""
        }
      ]
    }
  ],
  "config": [
    {
      "path": "Makefile",
      "matches": [
        {
          "line": 5,
          "pattern": "kratos-layout",
          "content": "IMAGE_NAME := fsyyft/kratos-layout"
        }
      ]
    }
  ],
  "docs": [
    {
      "path": "README.md",
      "matches": [
        {
          "line": 20,
          "pattern": "kratos-layout",
          "content": "## kratos-layout 项目"
        }
      ]
    }
  ],
  "other": []
}
```

---

## 常见错误和解决方案

### 错误 1：导入路径错误

**症状**：
```
cannot find package "github.com/old/module/path" in any of [...]
```

**原因**：
- 导入路径未更新

**解决方案**：
1. 使用 grep 查找所有旧导入路径
2. 批量替换为新路径
3. 重新运行 `go mod tidy`

**示例**：
```bash
grep -r "github.com/old/module" --include="*.go" .
sed -i '' 's|github.com/old/module|github.com/new/module|g' file.go
```

---

### 错误 2：依赖包未找到

**症状**：
```
go: github.com/new/module@v1.0.0: reading https://...
404 Not Found
```

**原因**：
- 新模块路径在远程仓库中不存在
- Git 远程未推送

**解决方案**：
1. 推送代码到远程仓库
2. 确保仓库路径与模块路径匹配
3. 检查 Git 远程配置

**示例**：
```bash
git remote set-url origin git@github.com:new-org/new-project.git
git push -u origin main
```

---

### 错误 3：Proto 文件编译错误

**症状**：
```
protoc-gen-go: unable to determine Go import path for
```

**原因**：
- .proto 文件中的 go_package 选项未更新

**解决方案**：
1. 更新 go_package 选项
2. 重新生成代码：`make api`

**示例**：
```protobuf
// ❌ 错误
option go_package = "github.com/old/module/api/;api";

// ✅ 正确
option go_package = "github.com/new/module/api/;api";
```

---

### 错误 4：Wire 依赖注入错误

**症状**：
```
wire: no wire function found for ...
```

**原因**：
- wire_gen.go 文件未更新
- 需要重新运行 wire

**解决方案**：
1. 更新 wire.go 中的导入路径
2. 重新生成：`wire ./...`

**示例**：
```bash
go install github.com/google/wire/cmd/wire@latest
wire ./...
```

---

### 错误 5：Docker 构建失败

**症状**：
```
ERROR: Could not find a valid package ...
```

**原因**：
- Dockerfile 中的路径未更新
- go.mod 复制位置不正确

**解决方案**：
1. 更新 Dockerfile 中的路径
2. 确保 go.mod 路径正确

**示例**：
```dockerfile
# ❌ 错误
WORKDIR /src/old-module
COPY go.mod go.sum ./old-module/

# ✅ 正确
WORKDIR /src/new-module
COPY go.mod go.sum ./new-module/
```

---

## 回滚触发条件

### 应该回滚的情况

1. **编译失败**
   - 无法修复的类型错误
   - 缺失的关键依赖
   - 大量导入路径错误

2. **测试失败**
   - 核心功能测试失败
   - 大量测试用例失败

3. **Lint 报错**
   - 大量关键错误
   - 无法自动修复的问题

4. **深层验证失败**
   - 代码文件中有残留引用
   - 无法快速修复

### 可以继续的情况

1. **仅文档残留**
   - 可以稍后手动更新

2. **配置文件警告**
   - 可以根据实际需求调整

3. **注释残留**
   - 不影响功能，可以稍后更新

---

## 回滚流程

### 自动回滚（使用脚本）

**步骤**：
1. 使用 `perform_rename.py` 创建的备份
2. 运行回滚命令

**示例**：
```bash
python3 .claude/skills/go-module-renamer/scripts/perform_rename.py --rollback
```

---

### 手动回滚

**步骤**：
1. 删除当前更改
2. 恢复备份文件

**示例**：
```bash
# 恢复备份
cp -r .backup/* .

# 或使用 Git
git checkout .
git clean -fd
```

---

## 最佳实践

### 1. 验证前准备

- [ ] 确保已创建备份
- [ ] 确保在干净的分支上工作
- [ ] 通知团队成员
- [ ] 准备回滚计划

### 2. 验证顺序

1. **快速验证**（1-3 分钟）
   - go fmt
   - go mod tidy
   - make lint
   - make build

2. **深度验证**（3-5 分钟）
   - grep 搜索
   - 代码审查
   - 文档检查

3. **功能验证**（5-10 分钟）
   - 运行测试套件
   - 手动测试核心功能
   - 检查日志输出

### 3. 验证通过标准

**必须满足**：
- ✅ 编译成功
- ✅ 测试通过
- ✅ 无代码残留

**建议满足**：
- ⭐ Lint 通过
- ⭐ 文档更新
- ⭐ 无配置残留

### 4. 验证后处理

- [ ] 提交更改
- [ ] 推送到远程仓库
- [ ] 创建 Pull Request
- [ ] 更新相关文档
- [ ] 通知团队

---

## 验证检查清单

### 浅层验证检查清单

- [ ] `go fmt ./...` 执行成功
- [ ] `go mod tidy` 执行成功
- [ ] `go build ./...` 执行成功
- [ ] `go test ./...` 执行成功
- [ ] `make lint` 执行成功（如果配置）
- [ ] `make build` 执行成功（如果配置）

### 深层验证检查清单

- [ ] .go 文件中无旧模块名引用
- [ ] .proto 文件中无旧模块名引用
- [ ] Makefile 已更新（如果需要）
- [ ] Dockerfile 已更新（如果需要）
- [ ] 配置文件已更新（如果需要）
- [ ] README.md 已更新
- [ ] 其他文档已更新

### 功能验证检查清单

- [ ] 应用启动成功
- [ ] API 接口正常
- [ ] 数据库连接正常
- [ ] 日志输出正常
- [ ] 监控指标正常

---

## 故障排除工具

### grep 命令

**查找所有 .go 文件**：
```bash
grep -r "old-module" --include="*.go" .
```

**查找所有 .proto 文件**：
```bash
grep -r "old-module" --include="*.proto" .
```

**查找所有配置文件**：
```bash
grep -r "old-project" --include="*.yaml" --include="*.yml" --include="Makefile" .
```

**查找并显示行号**：
```bash
grep -rn "old-module" --include="*.go" .
```

---

### find 命令

**查找所有 .go 文件**：
```bash
find . -name "*.go" -type f
```

**查找所有 .proto 文件**：
```bash
find . -name "*.proto" -type f
```

**查找并执行命令**：
```bash
find . -name "*.go" -type f -exec grep -l "old-module" {} \;
```

---

### sed 命令

**替换文件中的文本**（macOS）：
```bash
sed -i '' 's|old-module|new-module|g' file.go
```

**替换文件中的文本**（Linux）：
```bash
sed -i 's|old-module|new-module|g' file.go
```

**批量替换**：
```bash
find . -name "*.go" -type f -exec sed -i '' 's|old-module|new-module|g' {} \;
```

---

## 相关资源

- [Go Testing](https://golang.org/pkg/testing/)
- [golangci-lint](https://golangci-lint.run/)
- [Go Module Proxy](https://proxy.golang.org/)
- [Protocol Buffers](https://developers.google.com/protocol-buffers)
