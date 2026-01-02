# Git Commit Message 规范

本文档定义了 Kratos Layout 项目中 Git 提交信息（commit message）的完整规范。

## 1. 格式规范

### 1.1 基本格式

```
<类型>(<范围>): <描述>

[可选的详细描述]

[可选的脚注]
```

### 1.2 格式解析

- **类型（Type）**：必需，11 种预定义类型之一
- **范围（Scope）**：可选，用于限定改动的具体模块或目录
- **描述（Description）**：必需，简洁的中文描述，说明改动的核心内容
- **详细描述（Body）**：可选，用于复杂改动的详细说明
- **脚注（Footer）**：可选，用于关联 issue、breaking change 等

### 1.3 格式验证

**正则表达式**：
```
^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([^)]+\))?: .+$
```

**示例**：
```
feat(web): 添加用户管理功能
fix(data): 修复数据库连接超时问题
docs: 更新 API 使用文档
```

## 2. 类型定义

### 2.1 完整类型列表

| 类型 | 名称 | 说明 | 示例 |
|------|------|------|------|
| **feat** | 新功能 | 添加新的功能特性 | `feat(api): 新增用户注册接口` |
| **fix** | 修复 | 修复 bug 或错误 | `fix(data): 修复查询逻辑错误` |
| **docs** | 文档 | 文档变更 | `docs(readme): 更新安装说明` |
| **style** | 格式 | 代码格式调整（不影响功能） | `style: 格式化代码缩进` |
| **refactor** | 重构 | 代码重构（不是新功能也不是修复） | `refactor(biz): 重构业务逻辑层` |
| **perf** | 性能 | 性能优化 | `perf(data): 优化数据库查询性能` |
| **test** | 测试 | 测试相关 | `test(biz): 添加单元测试` |
| **build** | 构建 | 构建系统或外部依赖变更 | `build: 升级 Go 版本至 1.21` |
| **ci** | CI | CI 配置和脚本 | `ci: 优化 GitHub Actions 配置` |
| **chore** | 杂项 | 其他不修改 src 或 test 的文件 | `chore: 更新 .gitignore` |
| **revert** | 回退 | 回退之前的 commit | `revert: 回滚 feat 添加的功能` |

### 2.2 使用场景详解

#### feat（新功能）

**适用场景**：
- 添加新的功能模块
- 新增 API 接口
- 实现新的业务逻辑
- 添加新的 SKILL 或工具

**示例**：
```
feat(web): 添加用户管理功能
feat(api): 新增用户注册接口
feat(.claude/skills/git-commit-writer): 新增 git commit message 智能生成工具
```

#### fix（修复）

**适用场景**：
- 修复逻辑错误
- 修复崩溃问题
- 修复性能问题
- 修复安全漏洞

**示例**：
```
fix(data): 修复数据库连接超时问题
fix(biz): 修复用户注册时的逻辑错误
fix(web): 紧急修复生产环境崩溃问题
```

#### docs（文档）

**适用场景**：
- 添加新文档
- 更新现有文档
- 修正文档错误

**示例**：
```
docs: 添加 API 设计文档
docs(readme): 修正安装步骤说明
docs(api): 更新 gRPC 接口文档
```

#### style（格式）

**适用场景**：
- 调整代码缩进
- 统一代码风格
- 格式化代码

**不适用场景**：
- 功能性变更 → 使用 feat 或 fix
- 逻辑性变更 → 使用 refactor

**示例**：
```
style: 格式化代码缩进
style(internal): 统一错误处理格式
```

#### refactor（重构）

**适用场景**：
- 修改代码结构但功能不变
- 提取公共方法
- 重新组织模块
- 优化设计模式

**与 fix 的区别**：
- fix: 修复错误，功能有修正
- refactor: 改进结构，功能行为不变

**示例**：
```
refactor(biz): 重构业务逻辑层以提升可维护性
refactor(internal): 重构内部模块路径
refactor(service): 优化服务层接口设计
```

#### perf（性能）

**适用场景**：
- 优化查询性能
- 优化算法
- 优化资源使用

**示例**：
```
perf(data): 优化数据库查询性能
perf(biz): 减少重复计算
```

#### test（测试）

**适用场景**：
- 添加测试用例
- 修复测试逻辑
- 更新测试数据

**示例**：
```
test(biz): 添加用户管理单元测试
test(service): 修复接口测试错误
```

#### build（构建）

**适用场景**：
- 修改 Makefile
- 修改 go.mod
- 修改 Dockerfile
- 升级依赖版本

**示例**：
```
build: 升级 Go 版本至 1.21
build(makefile): 添加 docker 构建目标
```

#### ci（CI）

**适用场景**：
- 修改 GitHub Actions
- 修改 GitLab CI
- 修改 CI 配置

**示例**：
```
ci: 优化 GitHub Actions 工作流配置
ci(github): 添加自动化测试步骤
```

#### chore（杂项）

**适用场景**：
- 修改 .gitignore
- 添加配置文件
- 其他不修改代码的工作

**示例**：
```
chore: 更新 .gitignore 文件
chore(config): 添加开发环境配置
```

#### revert（回退）

**适用场景**：
- 完全回退之前的 commit

**格式要求**：
- 在 message 开头使用 `revert:`
- 在正文中包含被回退 commit 的完整 message
- 使用与原 commit 相同的范围

**示例**：
```
revert: feat: 添加用户管理功能

This reverts commit abc123def456.

原因是：功能设计需要重新评估
```

## 3. 范围定义

### 3.1 标准范围

| 范围 | 说明 | 示例 |
|------|------|------|
| **web** | Web 服务相关 | `feat(web): 添加实时通知功能` |
| **task** | 任务服务相关 | `fix(task): 修复定时任务执行时间错误` |
| **api** | API 定义相关 | `docs(api): 更新 gRPC 接口文档` |
| **internal** | 内部实现 | `refactor(internal): 重构内部模块路径` |
| **docs** | 文档相关 | `docs(readme): 修正安装步骤说明` |
| **build** | 构建相关 | `build: 升级 Go 版本` |
| **ci** | 持续集成 | `ci: 优化 GitHub Actions 工作流配置` |
| **chore** | 维护性工作 | `chore: 更新 .gitignore 文件` |

### 3.2 路径范围

当影响特定子模块时，使用点号分隔的路径：

**示例**：
```
.claude/skills/go-import-enforcer
.claude/skills/comment-enforcer
internal/biz
internal/data
internal/service
api/helloworld/v1
```

**使用规则**：
- 单一模块/目录 → 使用路径范围
  ```
  feat(.claude/skills/go-import-enforcer): 新增 go-import-enforcer 技能
  ```
- 跨多个模块 → 使用标准范围
  ```
  feat(internal): 重构内部模块路径
  ```

### 3.3 范围选择决策树

```
分析改动路径
  ↓
单一模块/目录？
  ├─ 是 → 使用路径范围（如 .claude/skills/go-import-enforcer）
  └─ 否 → 跨多个模块？
      ├─ 是 → 使用标准范围
      │     ├─ cmd/web/* → web
      │     ├─ cmd/task/* → task
      │     ├─ api/* → api
      │     ├─ internal/* → internal
      │     ├─ docs/* → docs
      │     └─ 配置/工具/脚本 → build/ci/chore
      └─ 否 → 特殊情况
            ├─ 全局性改动 → 不使用范围
            ├─ 配置性改动 → build 或 ci
            └─ 多个改动范围 → 选择最主要或最上层
```

## 4. 描述规范

### 4.1 语言要求

**必须使用中文**：
- ✅ 正确：`feat: 添加用户管理功能`
- ❌ 错误：`feat: add user management feature`

### 4.2 格式要求

**祈使句**：
- ✅ 正确：`feat: 添加用户管理功能`
- ❌ 错误：`feat: 添加了用户管理功能`（使用"了"）

**首字母小写**：
- ✅ 正确：`feat: 添加用户管理功能`
- ❌ 错误：`Feat: 添加用户管理功能`（首字母大写）

**结尾不加句号**：
- ✅ 正确：`feat: 添加用户管理功能`
- ❌ 错误：`feat: 添加用户管理功能。`（结尾有句号）

### 4.3 长度建议

- 描述建议在 50 字以内
- 保持简洁明了
- 避免过于笼统或过于细节

**示例**：
- ✅ 适中：`feat: 添加用户管理功能`
- ❌ 过于笼统：`feat: 添加功能`（未说明什么功能）
- ❌ 过于细节：`feat: 添加了包含增删改查的用户管理功能`（过于冗长）

### 4.4 常见错误模式

**格式错误**：
- ❌ `添加用户管理功能`（缺少类型）
- ❌ `feat 添加用户管理功能`（缺少冒号和空格）
- ❌ `feat:添加用户管理功能`（冒号后缺少空格）

**语言错误**：
- ❌ `feat: 添加了用户管理功能`（使用"了"）
- ❌ `feat: 添加用户功能。`（结尾有句号）
- ❌ `fix: 修复数据库问题`（"的"字冗余）

**范围错误**：
- ❌ `feat: 添加用户功能`（过于简略、缺少范围）
- ❌ `feat(Web): 添加用户功能`（范围首字母大写）
- ❌ `feat(api/web): 添加接口`（范围选择不当）

**描述不当**：
- ❌ `feat: 搞定数据库连接`（口语化）
- ❌ `feat: 弄一下用户功能`（过于口语）
- ❌ `fix: 修复 bug`（过于简略、未说明具体问题）
- ❌ `feat: 修改代码`（过于笼统、未说明改动内容）

## 5. 正文和脚注

### 5.1 何时使用正文

**使用场景**：
- 复杂改动需要详细说明
- 多个文件或模块的改动
- 需要解释改动的背景或原因

**格式要求**：
- 放在描述之后，空一行分隔
- 每行不超过 72 个字符
- 可以包含多个段落

**示例**：
```
feat(web): 添加系统服务管理功能

支持将 Web 服务安装为 macOS 和 Linux 系统服务，
提供 install、uninstall、status、start、stop 等子命令。

主要功能：
- 支持服务安装和卸载
- 提供服务状态查询
- 支持服务启动和停止控制
```

### 5.2 何时使用脚注

**使用场景**：
- 关联 issue
- 标记 Breaking Change
- 关联 pull request

**格式要求**：
- 放在正文或描述之后
- 使用特定的关键词标记

**Breaking Change 示例**：
```
feat(api): 重构用户认证接口

BREAKING CHANGE: 认证接口从 HTTP Basic 认证迁移到 JWT 认证，
老版本的客户端将无法继续使用。
```

**Issue 关联示例**：
```
fix(data): 修复数据库连接池泄漏问题

Fixes #123
```

## 6. 最佳实践

### 6.1 单一职责原则

每个 commit 应该只关注一个特定的改动：

**推荐**：
```
feat: 添加用户注册功能
feat: 添加邮箱验证功能
```

**不推荐**：
```
feat: 添加用户注册功能和邮箱验证功能
```

### 6.2 提供足够的上下文

描述应该让其他开发者快速理解改动的目的：

**推荐**：
```
fix(data): 修复 MySQL 查询语句中的语法错误
```

**不推荐**：
```
fix: 修复数据库问题
```

### 6.3 影响范围明确

使用范围字段明确指出影响的模块：

**推荐**：
```
feat(web): 添加用户认证中间件
feat(task): 添加定时清理任务
```

**不推荐**：
```
feat: 添加认证功能  # 不清楚是 Web 还是 Task 服务
```

### 6.4 版本控制语义化

通过 commit 类型帮助自动化工具判断版本变更：

- **feat** → Minor version (x.Y.z)
- **fix** → Patch version (x.y.Z)
- **Breaking changes** → Major version (X.y.z)

## 7. 与 AI 协作的注意事项

根据项目规范，特别注意：

1. **Git 操作由人工负责**：AI 只提供建议，不执行 `git add`、`commit`、`push` 等命令
2. **提交前检查**：确保代码通过 `make lint` 检查
3. **注释规范一致**：commit message 也需要使用中文表述

## 8. 总结

本项目采用基于 Conventional Commits 的本地化规范，主要特点：

- **类型丰富**：涵盖了功能、修复、文档、重构等多种变更类型
- **中文描述**：所有 commit message 使用中文，便于团队协作
- **范围明确**：通过点号分隔的路径精确指定影响范围
- **语义化**：便于自动化工具解析和版本管理
- **团队友好**：格式统一，便于代码审查和问题追踪

这种规范既保持了 Conventional Commits 的结构化优势，又适应了中文开发团队的协作需求。
